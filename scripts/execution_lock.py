"""Repository-aware operation locks with stale-lock recovery."""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ExecutionLock:
    def __init__(self, root: Path | str, operation_id: str, stale_after: int = 1800):
        self.path = Path(root).resolve() / "ollamatracks" / "locks" / f"{operation_id}.json"
        self.operation_id = operation_id
        self.stale_after = stale_after

    def acquire(self, execution_id: str) -> dict[str, Any]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        now = time.time()
        if self.path.exists():
            try:
                current = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                current = None
            if isinstance(current, dict) and now - float(current.get("epoch", 0)) <= self.stale_after:
                if current.get("execution_id") != execution_id:
                    raise RuntimeError(f"operation lock is held by {current.get('execution_id', 'unknown')}")
                return current
        payload = {"operation_id": self.operation_id, "execution_id": execution_id, "epoch": now, "acquired_at": utc_iso()}
        temporary = self.path.with_suffix(".tmp")
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        try:
            fd = os.open(temporary, flags, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                json.dump(payload, stream, sort_keys=True)
            os.replace(temporary, self.path)
        except FileExistsError:
            raise RuntimeError("operation lock acquisition raced with another execution") from None
        finally:
            temporary.unlink(missing_ok=True)
        return payload

    def release(self, execution_id: str) -> bool:
        if not self.path.exists():
            return False
        try:
            current = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False
        if current.get("execution_id") != execution_id:
            raise RuntimeError("cannot release a lock owned by another execution")
        self.path.unlink()
        return True

    def recover_stale(self) -> bool:
        if not self.path.exists():
            return False
        try:
            current = json.loads(self.path.read_text(encoding="utf-8"))
            stale = time.time() - float(current.get("epoch", 0)) > self.stale_after
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            stale = True
        if stale:
            self.path.unlink(missing_ok=True)
        return stale
