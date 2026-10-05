import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import cross_repo_sync
from scripts.cross_repo_sync import (
    evaluate_qmoi_restore_preflight,
    push_fast_forward,
    publish_qmoi_branch,
    run_git,
)


def successful_agent_evidence(source_sha):
    return {
        "verified": True,
        "conclusion": "success",
        "workflow_run_id": "test-agent-run-1",
        "source_sha": source_sha,
        "source_repository": "thealphakenya/Alpha-Q-ai",
    }


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
        for branch in ("main", "autosync-backup", "master"):
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

    evidence = successful_agent_evidence(workspace_sha)
    blocked = publish_qmoi_branch(repositories, workspace_sha, agent_success_evidence=evidence)
    assert blocked["status"] == "BLOCKED_REQUIRES_AUTHORIZATION"
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)

    published = publish_qmoi_branch(
        repositories, workspace_sha, authorized=True, agent_success_evidence=evidence
    )
    assert published["status"] == "SUCCESS"
    assert published["workspace_sha"] == workspace_sha
    assert all(remote_sha(repo, "qmoi") == workspace_sha for repo in repositories)
    assert all(item["branch_tree_sha"] for item in published["repositories"].values())
    assert all(item["qmoi_sha"] == workspace_sha for item in published["repositories"].values())
    assert all(item["remote_verification"]["verified"] for item in published["repositories"].values())
    assert published["agent_success_evidence"]["workflow_run_id"] == "test-agent-run-1"
    assert published["required_doc_sha256"]["oe2.txt"]
    assert published["required_doc_sha256"]["remotecompletion.md"]

    repeated = publish_qmoi_branch(
        repositories, workspace_sha, authorized=True, agent_success_evidence=evidence
    )
    assert repeated["status"] == "SUCCESS"
    assert all(item["action"] == "already_current" for item in repeated["repositories"].values())


def test_qmoi_branch_creation_rejects_dirty_workspace_and_missing_completion_docs(tmp_path):
    seed, repositories, bare_repositories = make_synchronized_repositories(tmp_path)
    workspace_sha = run_git(repositories[0], "rev-parse", "HEAD")
    (repositories[0] / "uncommitted.txt").write_text("not part of the restore point\n", encoding="utf-8")

    evidence = successful_agent_evidence(workspace_sha)
    dirty = publish_qmoi_branch(
        repositories, workspace_sha, authorized=True, agent_success_evidence=evidence
    )
    assert dirty["status"] == "BLOCKED"
    assert "dirty checkout" in dirty["blocker"]
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)

    (repositories[0] / "uncommitted.txt").unlink()
    (seed / "oe2.txt").unlink()
    subprocess.run(["git", "-C", str(seed), "add", "-u", "oe2.txt"], check=True)
    subprocess.run(["git", "-C", str(seed), "commit", "-qm", "remove required evidence"], check=True)
    missing_doc_sha = run_git(seed, "rev-parse", "HEAD")
    for bare in bare_repositories:
        for branch in ("main", "autosync-backup", "master"):
            subprocess.run(
                ["git", "-C", str(seed), "push", str(bare), f"{missing_doc_sha}:refs/heads/{branch}"],
                check=True,
                capture_output=True,
                text=True,
            )
    for repo in repositories:
        run_git(repo, "fetch", "origin", "--prune")

    missing_doc = publish_qmoi_branch(
        repositories,
        missing_doc_sha,
        authorized=True,
        agent_success_evidence=successful_agent_evidence(missing_doc_sha),
    )
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

    evidence = successful_agent_evidence(workspace_sha)
    drift = publish_qmoi_branch(
        repositories, workspace_sha, authorized=True, agent_success_evidence=evidence
    )
    assert drift["status"] == "BLOCKED"
    assert "main, autosync-backup, and master" in drift["blocker"]
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
    conflict = publish_qmoi_branch(
        repositories, workspace_sha, authorized=True, agent_success_evidence=evidence
    )
    assert conflict["status"] == "BLOCKED"
    assert "existing qmoi branch" in conflict["blocker"]
    assert remote_sha(repositories[0], "qmoi") == divergent_sha
    assert remote_sha(repositories[1], "qmoi") is None


def test_qmoi_restore_point_advances_only_by_fast_forward(tmp_path):
    seed, repositories, bare_repositories = make_synchronized_repositories(tmp_path)
    initial_sha = run_git(seed, "rev-parse", "HEAD")
    evidence = successful_agent_evidence(initial_sha)
    initial = publish_qmoi_branch(
        repositories, initial_sha, authorized=True, agent_success_evidence=evidence
    )
    assert initial["status"] == "SUCCESS"

    (seed / "README.md").write_text("new synchronized workspace tree\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(seed), "commit", "-qam", "new successful baseline"], check=True)
    next_sha = run_git(seed, "rev-parse", "HEAD")
    for branch in ("main", "autosync-backup", "master"):
        for bare in bare_repositories:
            subprocess.run(
                ["git", "-C", str(seed), "push", str(bare), f"{next_sha}:refs/heads/{branch}"],
                check=True,
                capture_output=True,
                text=True,
            )
    for repo in repositories:
        run_git(repo, "fetch", "origin", "--prune")

    updated = publish_qmoi_branch(
        repositories,
        next_sha,
        authorized=True,
        agent_success_evidence=successful_agent_evidence(initial_sha),
    )
    assert updated["status"] == "SUCCESS", updated
    assert all(item["action"] == "fast_forwarded" for item in updated["repositories"].values())
    assert all(remote_sha(repo, "qmoi") == next_sha for repo in repositories)


def test_qmoi_publication_requires_terminal_agent_success_and_candidate_ancestry(tmp_path):
    _, repositories, _ = make_synchronized_repositories(tmp_path)
    workspace_sha = run_git(repositories[0], "rev-parse", "HEAD")

    missing_evidence = publish_qmoi_branch(repositories, workspace_sha, authorized=True)
    assert missing_evidence["status"] == "BLOCKED"
    assert "verified terminal success evidence" in missing_evidence["blocker"]
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)

    invalid_evidence = successful_agent_evidence("a" * 40)
    invalid = publish_qmoi_branch(
        repositories,
        workspace_sha,
        authorized=True,
        agent_success_evidence=invalid_evidence,
    )
    assert invalid["status"] == "BLOCKED"
    assert "source SHA is unavailable" in invalid["blocker"]


def test_qmoi_publication_blocks_ref_drift_after_preflight(tmp_path, monkeypatch):
    _, repositories, _ = make_synchronized_repositories(tmp_path)
    workspace_sha = run_git(repositories[0], "rev-parse", "HEAD")
    original = cross_repo_sync._remote_branch_shas
    calls = 0

    def drift_on_publish_check(repo, branches):
        nonlocal calls
        calls += 1
        refs = original(repo, branches)
        if calls == 3:
            refs["autosync-backup"] = "f" * 40
        return refs

    monkeypatch.setattr(cross_repo_sync, "_remote_branch_shas", drift_on_publish_check)
    report = publish_qmoi_branch(
        repositories,
        workspace_sha,
        authorized=True,
        agent_success_evidence=successful_agent_evidence(workspace_sha),
    )

    assert report["status"] == "BLOCKED"
    assert "drifted after preflight" in report["blocker"]
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)


def test_restore_preflight_allows_only_authorized_aligned_first_run_bootstrap():
    common = {
        "current_main": "a" * 40,
        "current_backup": "a" * 40,
        "current_qmoi": "",
        "current_master": "",
        "peer_main": "a" * 40,
        "peer_backup": "a" * 40,
        "peer_qmoi": "",
        "peer_master": "",
        "checkout_sha": "a" * 40,
        "tree_sha": "tree-sha",
        "required_docs_present": True,
    }

    unauthorized = evaluate_qmoi_restore_preflight(**common, bootstrap_authorized=False)
    assert unauthorized["status"] == "BLOCKED_REQUIRES_AUTHORIZATION"
    authorized = evaluate_qmoi_restore_preflight(**common, bootstrap_authorized=True)
    assert authorized["status"] == "BOOTSTRAP_READY"
    assert authorized["bootstrap_allowed"] is True

    mismatched = evaluate_qmoi_restore_preflight(
        **{**common, "peer_backup": "b" * 40}, bootstrap_authorized=True
    )
    assert mismatched["status"] == "BLOCKED"


def test_restore_preflight_blocks_one_sided_or_stale_qmoi_branch():
    result = evaluate_qmoi_restore_preflight(
        current_main="a" * 40,
        current_backup="a" * 40,
        current_qmoi="a" * 40,
        current_master="",
        peer_main="a" * 40,
        peer_backup="a" * 40,
        peer_qmoi="",
        peer_master="",
        checkout_sha="a" * 40,
        tree_sha="tree-sha",
        required_docs_present=True,
        bootstrap_authorized=True,
    )

    assert result["status"] == "BLOCKED"
    assert "both restore refs must be absent" in result["blocker"]


def test_restore_preflight_allows_authorized_master_migration_only_when_qmoi_and_main_are_aligned():
    common = {
        "current_main": "a" * 40,
        "current_backup": "a" * 40,
        "current_qmoi": "a" * 40,
        "current_master": "",
        "peer_main": "a" * 40,
        "peer_backup": "a" * 40,
        "peer_qmoi": "a" * 40,
        "peer_master": "",
        "checkout_sha": "a" * 40,
        "tree_sha": "tree-sha",
        "required_docs_present": True,
    }

    unauthorized = evaluate_qmoi_restore_preflight(**common, bootstrap_authorized=False)
    assert unauthorized["status"] == "BLOCKED_REQUIRES_AUTHORIZATION"
    authorized = evaluate_qmoi_restore_preflight(**common, bootstrap_authorized=True)
    assert authorized["status"] == "MASTER_BOOTSTRAP_READY"

    one_sided_master = evaluate_qmoi_restore_preflight(
        **{**common, "peer_master": "a" * 40}, bootstrap_authorized=True
    )
    assert one_sided_master["status"] == "BLOCKED"


def test_promoted_sync_publishes_qmoi_restore_point_after_both_branches(tmp_path, monkeypatch):
    _, repositories, _ = make_synchronized_repositories(tmp_path)
    qmoi, alpha = repositories[1], repositories[0]
    report_path = tmp_path / "sync-report.json"
    monkeypatch.setattr(cross_repo_sync, "audit", lambda *_args: {"directions": {}})
    monkeypatch.setenv("QMOI_BRANCH_PUBLICATION_AUTHORIZED", "true")
    expected_sha = run_git(qmoi, "rev-parse", "refs/remotes/origin/main")
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_VERIFIED", "true")
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_CONCLUSION", "success")
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_RUN_ID", "test-agent-run-1")
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_SOURCE_SHA", expected_sha)
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_REPOSITORY", "thealphakenya/qmoi-enhanced")
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
    assert result == 0
    assert report["qmoi_restore_point"]["status"] == "SUCCESS"
    assert report["qmoi_restore_point"]["master_verified"] is True
    assert all(remote_sha(repo, "qmoi") == expected_sha for repo in repositories)
    assert all(remote_sha(repo, "master") == expected_sha for repo in repositories)
    assert all(item["remote_verification"]["master_sha"] == expected_sha for item in report["qmoi_restore_point"]["repositories"].values())


def test_promoted_sync_keeps_qmoi_restore_point_blocked_without_auth_gate(tmp_path, monkeypatch):
    _, repositories, _ = make_synchronized_repositories(tmp_path)
    qmoi, alpha = repositories[1], repositories[0]
    report_path = tmp_path / "sync-report.json"
    monkeypatch.setattr(cross_repo_sync, "audit", lambda *_args: {"directions": {}})
    monkeypatch.delenv("QMOI_BRANCH_PUBLICATION_AUTHORIZED", raising=False)
    expected_sha = run_git(qmoi, "rev-parse", "refs/remotes/origin/main")
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_VERIFIED", "true")
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_CONCLUSION", "success")
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_RUN_ID", "test-agent-run-1")
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_SOURCE_SHA", expected_sha)
    monkeypatch.setenv("QMOI_AGENT_SUCCESS_REPOSITORY", "thealphakenya/qmoi-enhanced")
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


def test_promoted_sync_defers_qmoi_when_no_successful_agent_run_is_verified(tmp_path, monkeypatch):
    _, repositories, _ = make_synchronized_repositories(tmp_path)
    qmoi, alpha = repositories[1], repositories[0]
    report_path = tmp_path / "sync-report.json"
    monkeypatch.setattr(cross_repo_sync, "audit", lambda *_args: {"directions": {}})
    monkeypatch.setenv("QMOI_BRANCH_PUBLICATION_AUTHORIZED", "true")
    for name in (
        "QMOI_AGENT_SUCCESS_VERIFIED",
        "QMOI_AGENT_SUCCESS_CONCLUSION",
        "QMOI_AGENT_SUCCESS_RUN_ID",
        "QMOI_AGENT_SUCCESS_SOURCE_SHA",
        "QMOI_AGENT_SUCCESS_REPOSITORY",
    ):
        monkeypatch.delenv(name, raising=False)
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
    assert result == 0
    assert report["status"] == "success_restore_point_deferred"
    assert report["qmoi_restore_point"]["status"] == "SKIPPED_NO_VERIFIED_AGENT_SUCCESS"
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)


def test_promoted_sync_creates_master_in_both_repositories_when_absent(tmp_path, monkeypatch):
    _, repositories, bare_repositories = make_synchronized_repositories(tmp_path)
    qmoi, alpha = repositories[1], repositories[0]
    report_path = tmp_path / "sync-report.json"
    expected_sha = run_git(qmoi, "rev-parse", "refs/remotes/origin/main")
    for bare in bare_repositories:
        subprocess.run(["git", "-C", str(bare), "update-ref", "-d", "refs/heads/master"], check=True)
    for repo in repositories:
        run_git(repo, "fetch", "origin", "--prune")
    monkeypatch.setattr(cross_repo_sync, "audit", lambda *_args: {"directions": {}})
    monkeypatch.setenv("QMOI_BRANCH_PUBLICATION_AUTHORIZED", "true")
    for name in (
        "QMOI_AGENT_SUCCESS_VERIFIED",
        "QMOI_AGENT_SUCCESS_CONCLUSION",
        "QMOI_AGENT_SUCCESS_RUN_ID",
        "QMOI_AGENT_SUCCESS_SOURCE_SHA",
        "QMOI_AGENT_SUCCESS_REPOSITORY",
    ):
        monkeypatch.delenv(name, raising=False)
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
    assert result == 0
    assert report["applied"]["completed_branches"] == ["autosync-backup", "main", "master"]
    assert all(remote_sha(repo, "master") == expected_sha for repo in repositories)
    assert report["qmoi_restore_point"]["status"] == "SKIPPED_NO_VERIFIED_AGENT_SUCCESS"
    assert all(remote_sha(repo, "qmoi") is None for repo in repositories)


def test_restore_workflow_contract_requires_success_checks_and_reported_secret_alias():
    root = Path(__file__).resolve().parents[1]
    autosync = (root / ".github/workflows/cross-repo-autosync.yml").read_text(encoding="utf-8")
    agent = (root / ".github/workflows/ollama-autonomous-agent.yml").read_text(encoding="utf-8")
    branch_sync = (root / ".github/workflows/branch-sync.yml").read_text(encoding="utf-8")

    assert '"Ollama Autonomous Agent & Live Tracker"' in autosync
    assert "run?.head_repository?.full_name === expectedRepository" in autosync
    assert "listJobsForWorkflowRun" in autosync
    for required_step in (
        "Execute Autonomous Agent with Circuit-Breaker Loop Protection",
        "Execute repository test suite",
        "Final lightweight validation",
        "Validate repository and hosted links",
        "Enforce final health gate",
    ):
        assert required_step in autosync
    assert "QMOI_AGENT_SUCCESS_VERIFIED" in autosync
    assert "branches: [main, autosync-backup, master]" in autosync
    assert "BOOTSTRAP_READY" in agent
    assert "MASTER_BOOTSTRAP_READY" in agent
    assert "QMOI_BRANCH_PUBLICATION_AUTHORIZED" in agent
    assert "secrets.MY_CUSTUOM_TOKEN || secrets.MY_CUSTOM_TOKEN" in autosync
    assert "secrets.MY_CUSTUOM_TOKEN || secrets.MY_CUSTOM_TOKEN" in branch_sync