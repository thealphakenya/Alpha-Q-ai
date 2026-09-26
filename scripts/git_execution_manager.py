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

    def fetch_remote(self, remote: str = "origin", branch: str | None = None) -> str:
        args = ["fetch", "--prune", remote]
        if branch:
            args.extend(["refs/heads/" + branch])
        return self.run(*args, check=False)

    def prepare_commit(self) -> dict[str, Any]:
        return {
            "before_sha": self.run("rev-parse", "HEAD", check=False) or None,
            "branch": self.run("branch", "--show-current", check=False) or None,
            "changed_files": self.run("status", "--short", check=False).splitlines(),
        }

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
        self.fetch_remote(remote=remote, branch=branch)
        ls_remote = self.run("ls-remote", remote, f"refs/heads/{branch}", check=False)
        remote_sha = ls_remote.split()[0] if ls_remote else None
        if not remote_sha:
            return {"branch": branch, "expected_sha": expected_sha, "remote_sha": None, "verified": False}
        if not expected_sha:
            return {"branch": branch, "expected_sha": expected_sha, "remote_sha": remote_sha, "verified": True}
        return {"branch": branch, "expected_sha": expected_sha, "remote_sha": remote_sha, "verified": remote_sha == expected_sha}

    def verify_remote_files(self, branch: str, paths: Iterable[str], remote: str = "origin") -> dict[str, Any]:
        self.fetch_remote(remote=remote, branch=branch)
        remote_ref = f"refs/remotes/{remote}/{branch}"
        missing: list[str] = []
        for path in paths:
            probe = self.run("cat-file", "-e", f"{remote_ref}:{path}", check=False)
            tracked = self.run("ls-tree", "-r", "--name-only", remote_ref, check=False)
            if not probe and path not in tracked.splitlines():
                missing.append(path)
        return {"branch": branch, "paths": list(paths), "missing": missing, "verified": not missing}
