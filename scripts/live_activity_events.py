"""Append-only correlated live activity events and freshness checks."""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATUSES = {"RUNNING", "WAITING", "RETRYING", "SELF_HEALING", "STALE", "RECOVERING", "BLOCKED", "FAILED", "SUCCESS", "OFFLINE", "UNKNOWN"}


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class LiveActivity:
    def __init__(self, root: Path | str, execution_id: str, source: str = "OLLAMA_AGENT", parent_execution_id: str | None = None):
        self.track_dir = Path(root).resolve() / "ollamatracks"
        self.execution_id = execution_id
        self.source = source
        self.parent_execution_id = parent_execution_id
        self.sequence = 0

    @property
    def events_path(self) -> Path:
        return self.track_dir / "events.jsonl"

    def publish(self, event: str, status: str, stage: str, message: str, **details: Any) -> dict[str, Any]:
        status = status.upper()
        if status not in STATUSES:
            raise ValueError(f"unsupported live activity status: {status}")
        self.track_dir.mkdir(parents=True, exist_ok=True)
        self.sequence += 1
        payload = {
            "timestamp": utc_iso(),
            "execution_id": self.execution_id,
            "parent_execution_id": self.parent_execution_id,
            "source": self.source,
            "component": "completion_engine",
            "event": event,
            "status": status,
            "message": message,
            "stage": stage,
            "sequence": self.sequence,
            "heartbeat": event.endswith("HEARTBEAT") or event == "HEARTBEAT",
            **details,
        }
        with self.events_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(payload, sort_keys=True) + "\n")
        (self.track_dir / "current_state.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return payload

    def heartbeat(self, stage: str) -> dict[str, Any]:
        return self.publish("HEARTBEAT", "RUNNING", stage, f"Heartbeat for {stage}")

    def freshness(self, max_age_seconds: int = 120) -> dict[str, Any]:
        if not self.events_path.is_file():
            return {"status": "OFFLINE", "fresh": False, "age_seconds": None}
        lines = [line for line in self.events_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not lines:
            return {"status": "OFFLINE", "fresh": False, "age_seconds": None}
        try:
            latest = json.loads(lines[-1])
            timestamp = datetime.fromisoformat(str(latest["timestamp"]).replace("Z", "+00:00"))
            age = max(0.0, (datetime.now(timezone.utc) - timestamp).total_seconds())
        except (KeyError, TypeError, ValueError, json.JSONDecodeError):
            return {"status": "UNKNOWN", "fresh": False, "age_seconds": None}
        fresh = age <= max_age_seconds
        status = latest.get("status", "UNKNOWN") if fresh else "STALE"
        return {"status": status, "fresh": fresh, "age_seconds": age, "latest": latest}
