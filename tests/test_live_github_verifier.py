from scripts.live_github_verifier import build_completion_status


def test_build_completion_status_blocks_when_local_head_differs_from_remote_main():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="local-sha",
        remote_main_sha="remote-sha",
        auth_verified=True,
        branch_protection_status="unknown",
        workflows=[
            {"name": "Cross-Repository Target-Owned Sync", "state": "active"},
            {"name": "Cross-Repository Auth Preflight", "state": "active"},
        ],
    )

    assert result["repo"] == "thealphakenya/Alpha-Q-ai"
    assert result["remote_matches_local"] is False
    assert result["completion_status"] == "BLOCKED"
    assert "remote main sha" in result["blockers"][0].lower()
    assert "exact remote sha" in result["next_actions"][0].lower()


def test_build_completion_status_requires_workflow_proof_for_exact_remote_sha():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="same-sha",
        remote_main_sha="same-sha",
        auth_verified=True,
        branch_protection_status="verified",
        workflows=[
            {"name": "Cross-Repository Target-Owned Sync", "state": "active"},
        ],
        workflow_runs=[
            {"name": "Cross-Repository Target-Owned Sync", "headSha": "other-sha", "conclusion": "success"},
        ],
    )

    assert result["completion_status"] == "BLOCKED"
    assert any("workflow" in blocker.lower() and "exact remote" in blocker.lower() for blocker in result["blockers"])


def test_build_completion_status_allows_ready_only_when_sha_auth_and_exact_workflow_proof_match():
    result = build_completion_status(
        repo="thealphakenya/Alpha-Q-ai",
        local_head="same-sha",
        remote_main_sha="same-sha",
        auth_verified=True,
        branch_protection_status="verified",
        workflows=[
            {"name": "Cross-Repository Target-Owned Sync", "state": "active"},
        ],
        workflow_runs=[
            {"name": "Ollama Master Orchestrator - Enhanced Auto-Healing", "headSha": "same-sha", "conclusion": "success"},
        ],
    )

    assert result["remote_matches_local"] is True
    assert result["completion_status"] == "READY"
    assert result["blockers"] == []
