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
