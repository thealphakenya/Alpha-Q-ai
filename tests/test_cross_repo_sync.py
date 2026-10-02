import json
import subprocess
import sys

import pytest

from scripts import cross_repo_sync
from scripts.cross_repo_sync import (
    classify_branch_name,
    compare_branch_inventories,
    fetch_all_remote_branches,
    push_fast_forward,
    remote_branch_inventory,
    run_git,
    validate_new_branch_name,
)


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


def test_branch_names_classify_roles_and_keep_unrecognized_names_review_only():
    assert classify_branch_name("main")["merge_policy"] == "protected_review_and_checks"
    assert classify_branch_name("autosync-backup")["merge_policy"] == "fast_forward_before_main"
    assert classify_branch_name("feature/123-audit-branches")["naming_status"] == "valid"
    assert classify_branch_name("release/v2.3.1")["role"] == "release"
    assert classify_branch_name("dependabot/pip/requests-gte-2.34.2")["role"] == "dependency_update"
    assert classify_branch_name(
        "dependabot/npm_and_yarn/Alpha-Q-ai-2025/npm_and_yarn-c3809050de"
    )["role"] == "dependency_update"
    assert classify_branch_name("codespace-sample-branch")["merge_policy"] == "never_cross_repo_sync"
    assert classify_branch_name("old-branch")["merge_policy"] == "review_only"
    assert validate_new_branch_name("feature/123-add-branch-audit") is True
    assert validate_new_branch_name("release/v2.3.1-rc1") is True
    assert validate_new_branch_name("main") is False
    assert validate_new_branch_name("dependabot/pip/requests-gte-2.34.2") is False
    assert validate_new_branch_name("feature/Bad Name") is False


def test_remote_branch_inventory_includes_all_fetched_refs(tmp_path):
    repo = init_repo(tmp_path / "repo", "tracked.txt", "content")
    main_sha = run_git(repo, "rev-parse", "refs/remotes/origin/main")
    subprocess.run(
        ["git", "-C", str(repo), "update-ref", "refs/remotes/origin/autosync-backup", main_sha],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "update-ref", "refs/remotes/origin/feature/123-audit-branches", main_sha],
        check=True,
    )

    inventory = remote_branch_inventory(repo)

    assert [branch["name"] for branch in inventory] == [
        "autosync-backup",
        "feature/123-audit-branches",
        "main",
    ]
    assert all(branch["tree_sha"] for branch in inventory)
    assert next(branch for branch in inventory if branch["name"].startswith("feature/"))[
        "automatic_publication_allowed"
    ] is False


def test_audit_fetches_all_remote_branch_heads_independent_of_configured_refspec(tmp_path, monkeypatch):
    calls = []

    def record_git_call(repo, *args, **_kwargs):
        calls.append((repo, args))
        return ""

    monkeypatch.setattr(cross_repo_sync, "run_git", record_git_call)

    fetch_all_remote_branches(tmp_path)

    assert calls == [
        (
            tmp_path,
            ("fetch", "--prune", "origin", "+refs/heads/*:refs/remotes/origin/*"),
        )
    ]


def test_compare_branch_inventories_reports_orphans_for_review(tmp_path):
    qmoi = init_repo(tmp_path / "qmoi", "q.txt", "q")
    alpha = init_repo(tmp_path / "alpha", "a.txt", "a")
    qmoi_branches = remote_branch_inventory(qmoi)
    alpha_branches = remote_branch_inventory(alpha)

    report = compare_branch_inventories(qmoi, alpha, qmoi_branches, alpha_branches)

    assert report["qmoi_branch_count"] == 1
    assert report["alpha_branch_count"] == 1
    assert report["branches"][0]["status"] == "diverged_or_objects_unavailable"
    assert report["branches"][0]["automatic_publication_allowed"] is True


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