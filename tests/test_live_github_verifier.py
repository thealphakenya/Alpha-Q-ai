import json

from scripts.live_github_verifier import (
    build_completion_status,
    parse_branch_protection,
    parse_effective_branch_rules,
    parse_workflow_runs,
    summarize_codeql_evidence,
)


def test_codeql_summary_uses_existing_runs_and_ignores_stale_sha():
    result = summarize_codeql_evidence(
        workflows=[{"name": "CodeQL Advanced", "state": "active"}],
        workflow_runs=[
            {
                "databaseId": 10,
                "workflowName": "CodeQL Advanced",
                "headSha": "b" * 40,
                "headBranch": "main",
                "status": "completed",
                "conclusion": "success",
                "updatedAt": "2026-10-09T12:00:00Z",
            },
            {
                "databaseId": 11,
                "workflowName": "CodeQL Advanced",
                "headSha": "a" * 40,
                "headBranch": "main",
                "status": "completed",
                "conclusion": "success",
                "updatedAt": "2026-10-10T12:00:00Z",
            },
        ],
        remote_sha="a" * 40,
        branch="main",
    )

    assert result["status"] == "SUCCESS"
    assert result["exact_sha_run_count"] == 1
    assert result["latest_exact_sha_run"]["workflow_run_id"] == 11
    assert result["analysis_triggered_by_verifier"] is False


def test_codeql_summary_does_not_treat_missing_exact_sha_run_as_success():
    result = summarize_codeql_evidence(
        workflows=[{"name": "CodeQL Advanced", "state": "active"}],
        workflow_runs=[{
            "databaseId": 12,
            "workflowName": "CodeQL Advanced",
            "headSha": "b" * 40,
            "headBranch": "main",
            "status": "completed",
            "conclusion": "success",
        }],
        remote_sha="a" * 40,
        branch="main",
    )

    assert result["status"] == "NOT_OBSERVED"
    assert result["latest_exact_sha_run"] is None


def test_codeql_success_alone_does_not_satisfy_remote_completion_gate():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="a" * 40,
        remote_main_sha="a" * 40,
        auth_verified=True,
        branch_protection_status="verified",
        workflows=[{"name": "CodeQL Advanced", "state": "active"}],
        workflow_runs=[{
            "databaseId": 13,
            "workflowName": "CodeQL Advanced",
            "headSha": "a" * 40,
            "headBranch": "main",
            "status": "completed",
            "conclusion": "success",
        }],
        remote_tree_sha="a" * 40,
        default_branch="main",
        repository_identity_verified=True,
    )

    assert result["codeql_evidence"]["status"] == "SUCCESS"
    assert result["exact_sha_successful_workflow"] is False
    assert result["completion_status"] == "BLOCKED"


def test_build_completion_status_blocks_when_local_head_differs_from_remote_main():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="a" * 40,
        remote_main_sha="b" * 40,
        auth_verified=True,
        branch_protection_status="unknown",
        workflows=[
            {"name": "Cross-Repository Target-Owned Sync", "state": "active"},
            {"name": "Cross-Repository Auth Preflight", "state": "active"},
        ],
        repository_identity_verified=True,
    )

    assert result["repo"] == "thealphakenya/Alpha-Q-ai"
    assert result["remote_matches_local"] is False
    assert result["completion_status"] == "BLOCKED"
    assert "remote main sha does not match" in " ".join(result["blockers"]).lower()
    assert "exact remote sha" in result["next_actions"][0].lower()


def test_build_completion_status_requires_workflow_proof_for_exact_remote_sha():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="a" * 40,
        remote_main_sha="a" * 40,
        auth_verified=True,
        branch_protection_status="verified",
        workflows=[
            {"name": "Cross-Repository Target-Owned Sync", "state": "active"},
        ],
        workflow_runs=[
            {
                "name": "Cross-Repository Target-Owned Sync",
                "databaseId": 11,
                "headSha": "b" * 40,
                "headBranch": "main",
                "status": "completed",
                "conclusion": "success",
            },
        ],
        repository_identity_verified=True,
    )

    assert result["completion_status"] == "BLOCKED"
    assert any("workflow" in blocker.lower() and "exact remote" in blocker.lower() for blocker in result["blockers"])


def test_build_completion_status_allows_ready_only_when_sha_auth_and_exact_workflow_proof_match():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="a" * 40,
        remote_main_sha="a" * 40,
        auth_verified=True,
        branch_protection_status="verified",
        workflows=[
            {"name": "Cross-Repository Target-Owned Sync", "state": "active"},
        ],
        workflow_runs=[
            {
                "name": "Ollama Master Orchestrator - Enhanced Auto-Healing",
                "databaseId": 42,
                "headSha": "a" * 40,
                "headBranch": "main",
                "status": "completed",
                "conclusion": "success",
            },
        ],
        remote_tree_sha="c" * 40,
        repository_identity_verified=True,
        check_runs=[],
        check_runs_status="observed",
    )

    assert result["remote_matches_local"] is True
    assert result["remote_ref"] == "refs/heads/main"
    assert result["completion_status"] == "READY"
    assert result["blockers"] == []
    assert result["exact_sha_workflow_runs"][0]["workflow_run_id"] == 42


def test_failed_exact_sha_check_run_blocks_otherwise_ready_completion():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="a" * 40,
        remote_main_sha="a" * 40,
        auth_verified=True,
        branch_protection_status="verified",
        workflows=[{"name": "Push on main", "state": "active"}],
        workflow_runs=[{
            "databaseId": 42,
            "workflowName": "Push on main",
            "headSha": "a" * 40,
            "headBranch": "main",
            "status": "completed",
            "conclusion": "success",
        }],
        remote_tree_sha="c" * 40,
        repository_identity_verified=True,
        check_runs=[
            {"name": "stale failure", "head_sha": "b" * 40, "status": "completed", "conclusion": "failure"},
            {"name": "Pages changed", "head_sha": "a" * 40, "status": "completed", "conclusion": "failure"},
        ],
        check_runs_status="observed",
    )

    assert result["completion_status"] == "BLOCKED"
    assert result["check_run_observation"]["exact_sha_count"] == 1
    assert result["check_run_observation"]["unsuccessful_count"] == 1
    assert any("check runs" in blocker.lower() for blocker in result["blockers"])


def test_build_completion_status_rejects_nonterminal_or_unidentified_run():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="a" * 40,
        remote_main_sha="a" * 40,
        auth_verified=True,
        branch_protection_status="verified",
        workflows=[{"name": "Ollama"}],
        workflow_runs=[{
            "databaseId": 42,
            "headSha": "a" * 40,
            "headBranch": "main",
            "status": "in_progress",
            "conclusion": "success",
        }],
        repository_identity_verified=True,
    )

    assert result["completion_status"] == "BLOCKED"
    assert result["exact_sha_successful_workflow"] is False


def test_build_completion_status_requires_repository_identity_verification():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="a" * 40,
        remote_main_sha="a" * 40,
        auth_verified=True,
        branch_protection_status="verified",
        workflows=[{"name": "Ollama"}],
        workflow_runs=[{
            "databaseId": 42,
            "headSha": "a" * 40,
            "headBranch": "main",
            "status": "completed",
            "conclusion": "success",
        }],
    )

    assert result["completion_status"] == "BLOCKED"
    assert result["exact_sha_successful_workflow"] is False
    assert "repository identity" in " ".join(result["blockers"]).lower()


def test_branch_protection_http_403_from_gh_is_unknown(monkeypatch):
    monkeypatch.setattr(
        "scripts.live_github_verifier.run_gh",
        lambda args: (None, "gh: Resource not accessible by integration (HTTP 403)", 1),
    )

    assert parse_branch_protection("thealphakenya/Alpha-Q-ai", "main") == "unknown"


def test_empty_effective_branch_rules_are_observed_not_unavailable(monkeypatch):
    monkeypatch.setattr(
        "scripts.live_github_verifier.run_gh",
        lambda args: ("[]", "", 0),
    )

    result = parse_effective_branch_rules("thealphakenya/Alpha-Q-ai", "main")

    assert result == {"status": "observed", "count": 0, "rules": []}


def test_workflow_runs_use_exact_sha_api_and_filter_other_refs(monkeypatch):
    sha = "a" * 40
    calls = []
    payload = {
        "workflow_runs": [
            {"id": 42, "name": "Push on main", "head_sha": sha, "head_branch": "main", "status": "completed", "conclusion": "success"},
            {"id": 43, "name": "PR #55", "head_sha": sha, "head_branch": "refs/pull/55/head", "status": "completed", "conclusion": "success"},
            {"id": 44, "name": "stale run", "head_sha": "b" * 40, "head_branch": "main", "status": "completed", "conclusion": "success"},
        ]
    }

    def fake_run_gh(args):
        calls.append(args)
        return json.dumps(payload), "", 0

    monkeypatch.setattr("scripts.live_github_verifier.run_gh", fake_run_gh)
    runs = parse_workflow_runs("thealphakenya/Alpha-Q-ai", sha, branch="main")

    assert calls == [
        ["api", f"repos/thealphakenya/Alpha-Q-ai/actions/runs?per_page=50&head_sha={sha}"]
    ]
    assert [run["databaseId"] for run in runs] == [42]
    assert runs[0]["workflowName"] == "Push on main"
