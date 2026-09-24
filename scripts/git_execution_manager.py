"""Explicit Git mutation and remote verification primitives."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Iterable


class GitExecutionError(RuntimeError):
    pass


class GitExecutionManager:
    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()

    def run(self, *args: str, check: bool = True) -> str:
        result = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True, check=False)
        if check and result.returncode:
            raise GitExecutionError(result.stderr.strip() or "git command failed")
        return result.stdout.strip()

    def prepare_commit(self) -> dict[str, Any]:
        return {"before_sha": self.run("rev-parse", "HEAD", check=False) or None, "branch": self.run("branch", "--show-current", check=False) or None, "changed_files": self.run("status", "--short", check=False).splitlines()}

    def create_commit(self, message: str, paths: Iterable[str]) -> str:
        paths = tuple(paths)
        if not paths:
            raise GitExecutionError("refusing empty commit")
        self.run("add", "--", *paths)
        self.run("diff", "--cached", "--check")
        self.run("commit", "-m", message)
        return self.run("rev-parse", "HEAD")

    def verify_commit(self, commit_sha: str) -> bool:
        return bool(commit_sha) and self.run("rev-parse", "HEAD", check=False) == commit_sha

    def push_branch(self, branch: str, remote: str = "origin") -> str:
        self.run("push", remote, f"HEAD:refs/heads/{branch}")
        return self.run("rev-parse", "HEAD")

    def verify_remote_branch(self, branch: str, expected_sha: str, remote: str = "origin") -> dict[str, Any]:
        remote_sha = self.run("ls-remote", remote, f"refs/heads/{branch}", check=False).split()[0] if self.run("ls-remote", remote, f"refs/heads/{branch}", check=False) else None
        return {"branch": branch, "expected_sha": expected_sha, "remote_sha": remote_sha, "verified": bool(remote_sha and remote_sha == expected_sha)}

    def verify_remote_files(self, branch: str, paths: Iterable[str], remote: str = "origin") -> dict[str, Any]:
        missing: list[str] = []
        for path in paths:
            probe = self.run("cat-file", "-e", f"{remote}/{branch}:{path}", check=False)
            if not probe and self.run("ls-tree", "-r", "--name-only", f"{remote}/{branch}", check=False).find(path) < 0:
                missing.append(path)
        return {"branch": branch, "paths": list(paths), "missing": missing, "verified": not missing}
