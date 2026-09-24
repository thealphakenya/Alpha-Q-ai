"""Remote-first workspace broker.

A workspace can submit and observe an authorized target-repository workflow.
It never pushes, merges, or changes a target repository directly.
"""
from __future__ import annotations

import json
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from remote_state import read_workflow_run


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def submit_remote_workflow(
    target_repository: str,
    workflow: str = "cross-repository-sync.yml",
    *,
    direction: str,
    source_repository: str,
    source_sha: str,
    mode: str = "dry-run",
    sync_id: str | None = None,
    reason: str = "workspace remote completion request",
) -> dict[str, Any]:
    if mode not in {"dry-run", "apply"}:
        raise ValueError("mode must be dry-run or apply")
    sync_id = sync_id or f"sync-{uuid.uuid4().hex}"
    payload = {
        "direction": direction,
        "source_repository": source_repository,
        "source_sha": source_sha,
        "mode": mode,
        "sync_id": sync_id,
        "reason": reason,
    }
    command = [
        "gh", "workflow", "run", workflow, "-R", target_repository,
        "-f", f"direction={direction}",
        "-f", f"source_repository={source_repository}",
        "-f", f"source_sha={source_sha}",
        "-f", f"mode={mode}",
        "-f", f"sync_id={sync_id}",
        "-f", f"reason={reason}",
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "REMOTE_SUBMIT_UNAVAILABLE", "sync_id": sync_id, "payload": payload, "error": str(exc), "submitted_at": utc_iso()}
    if result.returncode != 0:
        return {"status": "AUTH_BLOCKED" if "403" in result.stderr else "REMOTE_SUBMIT_FAILED", "sync_id": sync_id, "payload": payload, "error": result.stderr.strip(), "submitted_at": utc_iso()}
    return {"status": "QUEUED", "sync_id": sync_id, "payload": payload, "submitted_at": utc_iso(), "message": result.stdout.strip()}


def observe_remote_workflow(repository: str, run_id: str) -> dict[str, Any]:
    return read_workflow_run(repository, str(run_id))


def write_request(root: Path | str, request: dict[str, Any]) -> Path:
    path = Path(root).resolve() / "ollamatracks" / "remote_requests" / f"{request['sync_id']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


__all__ = ["submit_remote_workflow", "observe_remote_workflow", "write_request"]
