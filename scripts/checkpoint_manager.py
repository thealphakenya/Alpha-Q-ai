"""Atomic, resumable lifecycle checkpoints."""
from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class CheckpointManager:
    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.directory = self.root / "ollamatracks" / "checkpoints"

    def path(self, execution_id: str) -> Path:
        return self.directory / f"{execution_id}.json"

    def write(self, execution_id: str, state: Mapping[str, Any]) -> Path:
        payload = {"execution_id": execution_id, "updated_at": utc_iso(), **dict(state)}
        self.directory.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=f".{execution_id}.", suffix=".tmp", dir=self.directory)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(payload, stream, indent=2, sort_keys=True)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path(execution_id))
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return self.path(execution_id)

    def load(self, execution_id: str) -> dict[str, Any] | None:
        target = self.path(execution_id)
        if not target.is_file():
            return None
        try:
            value = json.loads(target.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def record_stage(self, execution_id: str, stage: str, status: str, **details: Any) -> Path:
        state = self.load(execution_id) or {"completed_stages": [], "failed_stages": [], "retry_counts": {}}
        state.update({"current_stage": stage, "status": status, **details})
        if status == "PASS" and stage not in state["completed_stages"]:
            state["completed_stages"].append(stage)
        if status in {"FAIL", "BLOCKED"} and stage not in state["failed_stages"]:
            state["failed_stages"].append(stage)
        return self.write(execution_id, state)

    def resume_state(self, execution_id: str) -> dict[str, Any]:
        return self.load(execution_id) or {"execution_id": execution_id, "current_stage": "DISCOVERY", "completed_stages": [], "failed_stages": [], "retry_counts": {}}
