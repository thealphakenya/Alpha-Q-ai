"""Fail-closed GitHub authorization preflight helpers."""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Iterable


def utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class AuthPreflightResult:
    status: str
    actor: str | None
    repositories: tuple[str, ...]
    required_operations: tuple[str, ...]
    scopes: tuple[str, ...]
    errors: tuple[str, ...]
    checked_at: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def preflight_auth(repositories: Iterable[str], required_operations: Iterable[str] = ()) -> AuthPreflightResult:
    repos = tuple(sorted(set(repositories)))
    operations = tuple(sorted(set(required_operations)))
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        return AuthPreflightResult("AUTH_BLOCKED", None, repos, operations, (), ("GitHub token is unavailable",), utc_iso())
    try:
        result = subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True, check=False, timeout=20)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return AuthPreflightResult("AUTH_UNKNOWN", None, repos, operations, (), (f"GitHub CLI unavailable: {exc}",), utc_iso())
    actor = result.stdout.strip() or None
    if result.returncode != 0 or not actor:
        return AuthPreflightResult("AUTH_BLOCKED", actor, repos, operations, (), (result.stderr.strip() or "GitHub identity lookup failed",), utc_iso())
    errors: list[str] = []
    for repository in repos:
        check = subprocess.run(["gh", "repo", "view", repository, "--json", "nameWithOwner"], capture_output=True, text=True, check=False, timeout=20)
        if check.returncode != 0:
            errors.append(f"repository access failed for {repository}: {check.stderr.strip() or 'unknown error'}")
    return AuthPreflightResult("AUTH_READY" if not errors else "AUTH_BLOCKED", actor, repos, operations, (), tuple(errors), utc_iso())


__all__ = ["AuthPreflightResult", "preflight_auth"]
