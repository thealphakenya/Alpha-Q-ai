"""Atomic, resumable lifecycle checkpoints."""
from __future__ import annotations

import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class CheckpointManager:
    HISTORY_KEY = "_undo_redo"
    HISTORY_SCHEMA_VERSION = 1
    MAX_HISTORY_SNAPSHOTS = 50

    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.directory = self.root / "ollamatracks" / "checkpoints"

    def path(self, execution_id: str) -> Path:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", execution_id):
            raise ValueError("Invalid checkpoint execution identifier")
        return self.directory / f"{execution_id}.json"

    @contextmanager
    def _lock(self, execution_id: str):
        self.path(execution_id)
        self.directory.mkdir(parents=True, exist_ok=True)
        lock_path = self.directory / f".{execution_id}.lock"
        try:
            fd = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise RuntimeError(f"Checkpoint {execution_id!r} is busy; retry later") from None
        try:
            os.write(fd, json.dumps({"pid": os.getpid(), "created_at": utc_iso()}).encode("utf-8"))
            os.fsync(fd)
            yield
        finally:
            os.close(fd)
            try:
                os.unlink(lock_path)
            except FileNotFoundError:
                pass

    @classmethod
    def _validate_history(cls, value: Any) -> dict[str, Any]:
        if value is None:
            return {"schema_version": cls.HISTORY_SCHEMA_VERSION, "snapshots": [], "cursor": -1}
        if (
            not isinstance(value, dict)
            or value.get("schema_version") != cls.HISTORY_SCHEMA_VERSION
            or not isinstance(value.get("snapshots"), list)
            or not isinstance(value.get("cursor"), int)
            or isinstance(value.get("cursor"), bool)
        ):
            raise RuntimeError("Checkpoint undo/redo history is malformed; refusing to alter checkpoint state")
        snapshots = value["snapshots"]
        cursor = value["cursor"]
        if any(not isinstance(item, dict) for item in snapshots) or not (-1 <= cursor < len(snapshots)):
            raise RuntimeError("Checkpoint undo/redo cursor is invalid; refusing to alter checkpoint state")
        return {"schema_version": cls.HISTORY_SCHEMA_VERSION, "snapshots": snapshots, "cursor": cursor}

    @classmethod
    def _public_state(cls, payload: Mapping[str, Any]) -> dict[str, Any]:
        return {key: value for key, value in payload.items() if key != cls.HISTORY_KEY}

    @staticmethod
    def _state_fingerprint(value: Mapping[str, Any]) -> str:
        comparable = {key: item for key, item in value.items() if key != "updated_at"}
        return json.dumps(comparable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

    def _read_raw(self, execution_id: str) -> dict[str, Any] | None:
        target = self.path(execution_id)
        if not target.is_file():
            return None
        try:
            value = json.loads(target.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Checkpoint {execution_id!r} is unreadable; refusing to overwrite it") from exc
        if not isinstance(value, dict):
            raise RuntimeError(f"Checkpoint {execution_id!r} is not a JSON object; refusing to overwrite it")
        return value

    def _persist(self, execution_id: str, payload: Mapping[str, Any]) -> Path:
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

    def write(self, execution_id: str, state: Mapping[str, Any]) -> Path:
        with self._lock(execution_id):
            return self._write_locked(execution_id, state)

    def _write_locked(self, execution_id: str, state: Mapping[str, Any]) -> Path:
        previous = self._read_raw(execution_id)
        payload = {**dict(state), "execution_id": execution_id, "updated_at": utc_iso()}
        history = self._validate_history(previous.get(self.HISTORY_KEY) if previous else None)
        old_public = self._public_state(previous) if previous else None
        if not history["snapshots"]:
            history["snapshots"] = [payload]
            history["cursor"] = 0
        elif old_public is None or self._state_fingerprint(old_public) != self._state_fingerprint(payload):
            history["snapshots"] = history["snapshots"][: history["cursor"] + 1]
            history["snapshots"].append(payload)
            if len(history["snapshots"]) > self.MAX_HISTORY_SNAPSHOTS:
                history["snapshots"] = history["snapshots"][-self.MAX_HISTORY_SNAPSHOTS :]
            history["cursor"] = len(history["snapshots"]) - 1
        payload[self.HISTORY_KEY] = history
        return self._persist(execution_id, payload)

    def load(self, execution_id: str) -> dict[str, Any] | None:
        value = self._read_raw(execution_id)
        return self._public_state(value) if value is not None else None

    def history_status(self, execution_id: str) -> dict[str, Any]:
        """Report undo/redo availability without exposing checkpoint contents."""
        payload = self._read_raw(execution_id)
        history = self._validate_history(payload.get(self.HISTORY_KEY) if payload else None)
        cursor = history["cursor"]
        snapshots = history["snapshots"]
        return {
            "execution_id": execution_id,
            "undo_available": cursor > 0,
            "redo_available": 0 <= cursor < len(snapshots) - 1,
            "retained_snapshots": len(snapshots),
            "maximum_snapshots": self.MAX_HISTORY_SNAPSHOTS,
        }

    def undo(self, execution_id: str) -> Path:
        """Restore the previous lifecycle checkpoint state; this does not revert repository files."""
        return self._move_history_cursor(execution_id, -1)

    def redo(self, execution_id: str) -> Path:
        """Reapply the next lifecycle checkpoint state; this does not publish a restore point."""
        return self._move_history_cursor(execution_id, 1)

    def _move_history_cursor(self, execution_id: str, offset: int) -> Path:
        with self._lock(execution_id):
            payload = self._read_raw(execution_id)
            if payload is None:
                raise RuntimeError(f"Checkpoint {execution_id!r} does not exist")
            history = self._validate_history(payload.get(self.HISTORY_KEY))
            next_cursor = history["cursor"] + offset
            if next_cursor < 0 or next_cursor >= len(history["snapshots"]):
                action = "undo" if offset < 0 else "redo"
                raise RuntimeError(f"No checkpoint state is available to {action}")
            restored = dict(history["snapshots"][next_cursor])
            restored["updated_at"] = utc_iso()
            history["cursor"] = next_cursor
            restored[self.HISTORY_KEY] = history
            return self._persist(execution_id, restored)

    def record_stage(self, execution_id: str, stage: str, status: str, **details: Any) -> Path:
        with self._lock(execution_id):
            raw = self._read_raw(execution_id)
            state = self._public_state(raw) if raw else {
                "completed_stages": [],
                "failed_stages": [],
                "retry_counts": {},
            }
            state.update({"current_stage": stage, "status": status, **details})
            if status == "PASS" and stage not in state["completed_stages"]:
                state["completed_stages"].append(stage)
            if status in {"FAIL", "BLOCKED"} and stage not in state["failed_stages"]:
                state["failed_stages"].append(stage)
            return self._write_locked(execution_id, state)

    def resume_state(self, execution_id: str) -> dict[str, Any]:
        return self.load(execution_id) or {"execution_id": execution_id, "current_stage": "DISCOVERY", "completed_stages": [], "failed_stages": [], "retry_counts": {}}
