import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import autonomous_evidence_monitor as monitor


def test_qaudit_summary_reads_required_evidence_markers():
    summary = monitor.extract_qaudit_summary(ROOT / "QAUDITS.md")
    assert "NEEDS_REVIEW" in summary
    assert "repository surface audit" in summary.lower()


def test_status_is_blocked_when_remote_and_protection_evidence_are_missing():
    result = monitor.evaluate_completion_status(
        local_head="abc",
        remote_main_sha="def",
        auth_verified=True,
        branch_protection_status="unavailable",
        exact_sha_successful_workflow=False,
        workflow_inventory_count=2,
    )
    joined = " ".join(result["blockers"]).lower()
    assert result["completion_status"] == "BLOCKED"
    assert "local/remote sha parity" in joined
    assert "branch protection" in joined


def test_update_evidence_files_replaces_previous_monitor_section(tmp_path):
    evidence_path = tmp_path / "oe2.txt"
    evidence_path.write_text(
        "historical evidence\n\n"
        "## Autonomous evidence monitor\nold checkpoint one\n\n"
        "## Autonomous evidence monitor\nold checkpoint two\n",
        encoding="utf-8",
    )
    payload = {
        "timestamp": "2026-10-05T23:58:56.176569Z",
        "repo": "thealphakenya/Alpha-Q-ai",
        "branch": "main",
        "auth_verified": False,
        "local_head": "7d33581d7e14f169ef659ec37b24baa90c96caef",
        "remote_main_sha": "",
        "remote_matches_local": False,
        "branch_protection_status": "unavailable",
        "workflow_inventory_count": 1,
        "exact_sha_successful_workflow": False,
        "completion_status": "BLOCKED",
        "blockers": ["GitHub authentication is not verified"],
        "next_actions": ["Authenticate the target repository"],
        "qaudit_summary": "Status: NEEDS_REVIEW",
    }

    monitor.update_evidence_files(tmp_path, payload)

    updated = evidence_path.read_text(encoding="utf-8")
    assert updated.count("## Autonomous evidence monitor") == 1
    assert "historical evidence" in updated
    assert "old checkpoint one" not in updated
    assert "old checkpoint two" not in updated
