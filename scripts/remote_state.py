"""Read-only remote GitHub state helpers for remote-first execution."""
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class RemoteState:
    repository: str
    branch: str
    sha: str | None
    reachable: bool
    status: str
    checked_at: str
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def gh_json(args: list[str]) -> tuple[Any | None, str | None]:
    try:
        result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc)
    if result.returncode != 0:
        return None, result.stderr.strip() or "GitHub CLI request failed"
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError as exc:
        return None, f"invalid GitHub response: {exc}"


def read_branch(repository: str, branch: str) -> RemoteState:
    payload, error = gh_json(["api", f"repos/{repository}/git/ref/heads/{branch}"])
    if error or not isinstance(payload, dict):
        return RemoteState(repository, branch, None, False, "REMOTE_STATUS_UNAVAILABLE", utc_iso(), error)
    sha = ((payload.get("object") or {}).get("sha"))
    if not isinstance(sha, str) or not sha:
        return RemoteState(repository, branch, None, False, "REMOTE_STATUS_UNKNOWN", utc_iso(), "remote response omitted SHA")
    return RemoteState(repository, branch, sha, True, "REMOTE_VERIFIED", utc_iso())


def read_workflow_run(repository: str, run_id: str) -> dict[str, Any]:
    payload, error = gh_json(["run", "view", run_id, "-R", repository, "--json", "databaseId,status,conclusion,headSha,headBranch,url,workflowName,createdAt,updatedAt,completedAt"])
    if error:
        return {"status": "REMOTE_STATUS_UNAVAILABLE", "run_id": run_id, "error": error, "checked_at": utc_iso()}
    return {"status": "REMOTE_VERIFIED", "run_id": run_id, "run": payload, "checked_at": utc_iso()}


__all__ = ["RemoteState", "read_branch", "read_workflow_run"]
