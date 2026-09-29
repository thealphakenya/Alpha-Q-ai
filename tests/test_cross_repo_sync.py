import json
import subprocess
import sys

import pytest

from scripts import cross_repo_sync
from scripts.cross_repo_sync import push_fast_forward, run_git


def init_repo(root, filename, content):
    root.mkdir()
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
    (root / filename).write_text(content, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", filename], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "initial"], check=True)
    commit = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    subprocess.run(
        ["git", "-C", str(root), "update-ref", "refs/remotes/origin/main", commit],
        check=True,
    )
    return root


def test_push_fast_forward_refuses_source_commit_missing_from_target(tmp_path):
    source = init_repo(tmp_path / "source", "source.txt", "source")
    target = init_repo(tmp_path / "target", "target.txt", "target")

    with pytest.raises(
        RuntimeError,
        match="source commit .* is not available in target checkout",
    ):
        push_fast_forward(target, source, "autosync-backup", "main")


def test_run_git_returns_empty_for_missing_optional_ref(tmp_path):
    repo = init_repo(tmp_path / "repo", "tracked.txt", "content")

    result = run_git(repo, "rev-parse", "refs/remotes/origin/missing", check=False)

    assert result == ""


def test_promoted_sync_reports_blocked_preflight_without_mutating_target(tmp_path, monkeypatch):
    source = init_repo(tmp_path / "source", "source.txt", "source")
    target = init_repo(tmp_path / "target", "target.txt", "target")
    target_main = run_git(target, "rev-parse", "refs/remotes/origin/main")
    report_path = tmp_path / "sync-report.json"
    monkeypatch.setattr(cross_repo_sync, "audit", lambda *_args: {"directions": {}})
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cross_repo_sync.py",
            "--qmoi",
            str(target),
            "--alpha",
            str(source),
            "--direction",
            "alpha-to-qmoi",
            "--apply",
            "--promote",
            "--report",
            str(report_path),
        ],
    )

    result = cross_repo_sync.main()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert result == 2
    assert report["status"] == "blocked"
    assert report["apply_preflight"]["status"] == "blocked"
    assert report["applied"] is False
    assert run_git(target, "rev-parse", "refs/remotes/origin/main") == target_main
    assert run_git(target, "rev-parse", "refs/remotes/origin/autosync-backup", check=False) == ""