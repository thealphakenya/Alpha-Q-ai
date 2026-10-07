from scripts.live_github_verifier import build_completion_status


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
        repository_identity_verified=True,
    )

    assert result["remote_matches_local"] is True
    assert result["remote_ref"] == "refs/heads/main"
    assert result["completion_status"] == "READY"
    assert result["blockers"] == []
    assert result["exact_sha_workflow_runs"][0]["workflow_run_id"] == 42


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
