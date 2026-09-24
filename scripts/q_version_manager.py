"""Collision-resistant local Q.0.0.N reservation and pair verification."""
from __future__ import annotations

import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


class QVersionManager:
    pattern = re.compile(r"^Q\.0\.0\.(\d+)(?:\.md|$)")

    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.reservations = self.root / "ollamatracks" / "q_versions.json"

    def discover(self, roots: list[Path] | None = None) -> int:
        maximum = 0
        for root in roots or [self.root]:
            for path in root.iterdir() if root.is_dir() else ():
                match = self.pattern.match(path.name)
                if match:
                    maximum = max(maximum, int(match.group(1)))
        if self.reservations.is_file():
            try:
                data = json.loads(self.reservations.read_text(encoding="utf-8"))
                maximum = max(maximum, int(data.get("reserved", 0)))
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                pass
        return maximum

    def reserve(self, roots: list[Path] | None = None) -> str:
        self.reservations.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.reservations.with_suffix(".lock")
        try:
            lock_fd = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise RuntimeError("Q-version reservation is busy; retry remotely") from None
        try:
            next_number = self.discover(roots) + 1
            payload = {
                "reserved": next_number,
                "version": f"Q.0.0.{next_number}",
                "reservation_id": os.urandom(12).hex(),
            }
            fd, temporary_name = tempfile.mkstemp(
                prefix="q-version-", suffix=".tmp", dir=self.reservations.parent
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as stream:
                    json.dump(payload, stream, indent=2, sort_keys=True)
                    stream.write("\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary_name, self.reservations)
            finally:
                if os.path.exists(temporary_name):
                    os.unlink(temporary_name)
            return payload["version"]
        finally:
            os.close(lock_fd)
            os.unlink(lock_path)

    @staticmethod
    def verify_pair(version: str, roots: list[Path]) -> dict[str, Any]:
        results = {str(root): (root / version).is_dir() and (root / f"{version}.md").is_file() for root in roots}
        return {"version": version, "repositories": results, "verified": bool(results) and all(results.values())}
