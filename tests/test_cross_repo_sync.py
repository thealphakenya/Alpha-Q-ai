import json
import subprocess
import sys

import pytest

from scripts import cross_repo_sync
from scripts.cross_repo_sync import push_fast_forward, publish_qmoi_branch, run_git


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


def make_synchronized_repositories(tmp_path):
    seed = init_repo(tmp_path / "seed", "README.md", "committed workspace tree\n")
    for filename in ("oe2.txt", "remotecompletion.md"):
        (seed / filename).write_text(f"# {filename}\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(seed), "add", "oe2.txt", "remotecompletion.md"], check=True)
    subprocess.run(["git", "-C", str(seed), "commit", "-qm", "completion evidence"], check=True)
    seed_sha = run_git(seed, "rev-parse", "HEAD")
    repositories = []
    bare_repositories = []
    for name in ("Alpha-Q-ai", "qmoi-enhanced"):
        bare = tmp_path / f"{name}.git"
        bare_repositories.append(bare)
        subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
        subprocess.run(["git", "-C", str(bare), "symbolic-ref", "HEAD", "refs/heads/main"], check=True)
        for branch in ("main", "autosync-backup"):
            subprocess.run(
                ["git", "-C", str(seed), "push", str(bare), f"{seed_sha}:refs/heads/{branch}"],
                check=True,
                capture_output=True,
                text=True,
            )
        checkout = tmp_path / name
        subprocess.run(["git", "clone", "-q", str(bare), str(checkout)], check=True)
        repositories.append(checkout)
    subprocess.run(["git", "-C", str(seed), "remote", "add", "origin", str(bare_repositories[0])], check=True)
    return seed, repositories, bare_repositories


def remote_sha(repo, branch):
    output = subprocess.run(
        ["git", "-C", str(repo), "ls-remote", "--heads", "origin", f"refs/heads/{branch}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return output.split()[0] if output else None


def test_qmoi_branch_creation_requires_authorization_and_is_idempotent(tmp_path):
    _, repositories, _ = make_synchronized_repositories(tmp_path)
    workspace_sha = run_git(repositories[0], "rev-parse", "HEAD")

    blocked = publish_qmoi_branch(repositories, workspace_sha)
    assert blocked["status"] == "BLOCKED_REQUIRES_AUTHORIZATION"
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)

    published = publish_qmoi_branch(repositories, workspace_sha, authorized=True)
    assert published["status"] == "SUCCESS"
    assert published["workspace_sha"] == workspace_sha
    assert all(remote_sha(repo, "qmoi") == workspace_sha for repo in repositories)
    assert all(item["branch_tree_sha"] for item in published["repositories"].values())

    repeated = publish_qmoi_branch(repositories, workspace_sha, authorized=True)
    assert repeated["status"] == "SUCCESS"
    assert all(item["action"] == "already_current" for item in repeated["repositories"].values())


def test_qmoi_branch_creation_rejects_dirty_workspace_and_missing_completion_docs(tmp_path):
    seed, repositories, bare_repositories = make_synchronized_repositories(tmp_path)
    workspace_sha = run_git(repositories[0], "rev-parse", "HEAD")
    (repositories[0] / "uncommitted.txt").write_text("not part of the restore point\n", encoding="utf-8")

    dirty = publish_qmoi_branch(repositories, workspace_sha, authorized=True)
    assert dirty["status"] == "BLOCKED"
    assert "dirty checkout" in dirty["blocker"]
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)

    (repositories[0] / "uncommitted.txt").unlink()
    (seed / "oe2.txt").unlink()
    subprocess.run(["git", "-C", str(seed), "add", "-u", "oe2.txt"], check=True)
    subprocess.run(["git", "-C", str(seed), "commit", "-qm", "remove required evidence"], check=True)
    missing_doc_sha = run_git(seed, "rev-parse", "HEAD")
    for bare in bare_repositories:
        for branch in ("main", "autosync-backup"):
            subprocess.run(
                ["git", "-C", str(seed), "push", str(bare), f"{missing_doc_sha}:refs/heads/{branch}"],
                check=True,
                capture_output=True,
                text=True,
            )
    for repo in repositories:
        run_git(repo, "fetch", "origin", "--prune")

    missing_doc = publish_qmoi_branch(repositories, missing_doc_sha, authorized=True)
    assert missing_doc["status"] == "BLOCKED"
    assert "oe2.txt" in missing_doc["blocker"]
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)


def test_qmoi_branch_creation_blocks_backup_drift_and_conflicting_branch(tmp_path):
    seed, repositories, bare_repositories = make_synchronized_repositories(tmp_path)
    workspace_sha = run_git(seed, "rev-parse", "HEAD")
    (seed / "README.md").write_text("different backup tree\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(seed), "commit", "-qam", "divergent backup"], check=True)
    divergent_sha = run_git(seed, "rev-parse", "HEAD")
    subprocess.run(
        ["git", "-C", str(seed), "push", "origin", f"{divergent_sha}:refs/heads/autosync-backup"],
        check=True,
        capture_output=True,
        text=True,
    )

    drift = publish_qmoi_branch(repositories, workspace_sha, authorized=True)
    assert drift["status"] == "BLOCKED"
    assert "main and autosync-backup" in drift["blocker"]
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)

    subprocess.run(
        ["git", "-C", str(bare_repositories[0]), "update-ref", "refs/heads/autosync-backup", workspace_sha],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(seed), "push", "origin", f"{divergent_sha}:refs/heads/qmoi"],
        check=True,
        capture_output=True,
        text=True,
    )
    conflict = publish_qmoi_branch(repositories, workspace_sha, authorized=True)
    assert conflict["status"] == "BLOCKED"
    assert "existing qmoi branch" in conflict["blocker"]
    assert remote_sha(repositories[0], "qmoi") == divergent_sha
    assert remote_sha(repositories[1], "qmoi") is None


def test_qmoi_restore_point_advances_only_by_fast_forward(tmp_path):
    seed, repositories, bare_repositories = make_synchronized_repositories(tmp_path)
    initial_sha = run_git(seed, "rev-parse", "HEAD")
    initial = publish_qmoi_branch(repositories, initial_sha, authorized=True)
    assert initial["status"] == "SUCCESS"

    (seed / "README.md").write_text("new synchronized workspace tree\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(seed), "commit", "-qam", "new successful baseline"], check=True)
    next_sha = run_git(seed, "rev-parse", "HEAD")
    for branch in ("main", "autosync-backup"):
        for bare in bare_repositories:
            subprocess.run(
                ["git", "-C", str(seed), "push", str(bare), f"{next_sha}:refs/heads/{branch}"],
                check=True,
                capture_output=True,
                text=True,
            )
    for repo in repositories:
        run_git(repo, "fetch", "origin", "--prune")

    updated = publish_qmoi_branch(repositories, next_sha, authorized=True)
    assert updated["status"] == "SUCCESS", updated
    assert all(item["action"] == "fast_forwarded" for item in updated["repositories"].values())
    assert all(remote_sha(repo, "qmoi") == next_sha for repo in repositories)


def test_promoted_sync_publishes_qmoi_restore_point_after_both_branches(tmp_path, monkeypatch):
    _, repositories, _ = make_synchronized_repositories(tmp_path)
    qmoi, alpha = repositories[1], repositories[0]
    report_path = tmp_path / "sync-report.json"
    monkeypatch.setattr(cross_repo_sync, "audit", lambda *_args: {"directions": {}})
    monkeypatch.setenv("QMOI_BRANCH_PUBLICATION_AUTHORIZED", "true")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cross_repo_sync.py",
            "--qmoi",
            str(qmoi),
            "--alpha",
            str(alpha),
            "--direction",
            "qmoi-to-alpha",
            "--apply",
            "--promote",
            "--report",
            str(report_path),
        ],
    )

    result = cross_repo_sync.main()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    expected_sha = run_git(qmoi, "rev-parse", "refs/remotes/origin/main")
    assert result == 0
    assert report["qmoi_restore_point"]["status"] == "SUCCESS"
    assert all(remote_sha(repo, "qmoi") == expected_sha for repo in repositories)


def test_promoted_sync_keeps_qmoi_restore_point_blocked_without_auth_gate(tmp_path, monkeypatch):
    _, repositories, _ = make_synchronized_repositories(tmp_path)
    qmoi, alpha = repositories[1], repositories[0]
    report_path = tmp_path / "sync-report.json"
    monkeypatch.setattr(cross_repo_sync, "audit", lambda *_args: {"directions": {}})
    monkeypatch.delenv("QMOI_BRANCH_PUBLICATION_AUTHORIZED", raising=False)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "cross_repo_sync.py",
            "--qmoi",
            str(qmoi),
            "--alpha",
            str(alpha),
            "--direction",
            "qmoi-to-alpha",
            "--apply",
            "--promote",
            "--report",
            str(report_path),
        ],
    )

    result = cross_repo_sync.main()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert result == 2
    assert report["qmoi_restore_point"]["status"] == "BLOCKED_REQUIRES_AUTHORIZATION"
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)