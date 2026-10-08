import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

import pytest

from scripts.autonomous_completion_engine import (
    AutonomousCompletionEngine,
    REQUIRED_GATES,
    audit_instruction_files,
    audit_ollama_reference_files,
)
from scripts.checkpoint_manager import CheckpointManager
from scripts.execution_lock import ExecutionLock
from scripts.live_activity_events import LiveActivity
from scripts.qaudit_checkpoint import _append_pair_locked, record_qaudit_checkpoint
from scripts.q_version_manager import QVersionManager
from scripts.ollama_research import (
    EXTERNAL_RESEARCH_CONTROLS,
    INTERNAL_RESEARCH_CONTROLS,
    _markdown_sentence_evidence,
    audit_repository_surfaces,
    build_internal_research_plan,
    discover_resource_candidates,
    fetch_official_resource,
    record_research_visit,
    write_markdown_sentence_audit,
)
from scripts.ollama_autonomous_agent import (
    OllamaAutonomousAgent,
    sanitize_repo_ollama_mentions,
)
from scripts.sync_contract import build_sync_contract
from scripts.control_plane_supervisor import ControlPlaneSupervisor
from scripts.repository_contract_audit import audit_repository_contract


def make_root(tmp_path: Path) -> Path:
    (tmp_path / "QMOI_Ollama_Autonomous_Production_Completion_Master_Plan.md").write_text("## 1. One\n## 2. Two\n", encoding="utf-8")
    (tmp_path / "ollama_master_topic_index.txt").write_text("1. One\n2. Two\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# Root instructions\n", encoding="utf-8")
    (tmp_path / ".github" / "copilot-instructions.md").parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / ".github" / "copilot-instructions.md").write_text("# Copilot instructions\n", encoding="utf-8")
    (tmp_path / ".github" / "instructions").mkdir(parents=True, exist_ok=True)
    return tmp_path


def make_git_repo(root: Path, name: str, *, with_instructions: bool = False) -> Path:
    repository = root / name
    repository.mkdir()
    subprocess.run(["git", "-C", str(repository), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(repository), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(repository), "config", "user.email", "test@example.com"], check=True)
    (repository / "src").mkdir()
    (repository / "src" / "app.py").write_text("print('ready')\n", encoding="utf-8")
    if with_instructions:
        (repository / "AGENTS.md").write_text("# Repository instructions\n", encoding="utf-8")
        (repository / ".github" / "copilot-instructions.md").parent.mkdir(parents=True, exist_ok=True)
        (repository / ".github" / "copilot-instructions.md").write_text("# Copilot instructions\n", encoding="utf-8")
        (repository / ".github" / "instructions").mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(repository), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repository), "commit", "-m", "initial"], check=True, capture_output=True)
    return repository


def q_version_instruction_evidence(roots: list[Path]) -> dict[str, dict[str, object]]:
    return {str(root.resolve()): audit_instruction_files(root) for root in roots}


def q_version_autonomous_completion() -> dict[str, object]:
    return {
        "execution_id": "completion-final-test",
        "status": "SUCCESS",
        "gates": {name: "PASS" for name in REQUIRED_GATES},
        "next_actions": [],
    }


def q_version_production_readiness() -> dict[str, object]:
    return {
        "status": "CLEAR",
        "coverage_complete": True,
        "candidate_count": 0,
        "unreadable_files": [],
        "oversized_files_not_read": 0,
    }


def qaudit_precondition(stage: str, manifest: str = "a" * 64) -> dict[str, object]:
    return {
        "stage": stage,
        "status": "PASS",
        "source_manifest_sha256": manifest,
        "required_metrics_complete": True,
        "required_metrics": [{
            "name": "required-evidence-coverage",
            "numerator": 1,
            "denominator": 1,
            "formula": "validated_required_items / required_items",
            "status": "PASS",
            "source_manifest_sha256": manifest,
        }],
        "source_scope": "target_remote_exact_sha",
        "blockers": [],
    }


def terminal_remote_sha_binding(
    repository: str,
    sha: str,
    run_id: str,
    tree_sha: str = "c" * 40,
) -> dict[str, object]:
    return {
        "repository": repository,
        "repository_identity_verified": True,
        "remote_verified": True,
        "remote_ref": "refs/heads/main",
        "remote_ref_sha": sha,
        "workflow_head_sha": sha,
        "remote_tree_sha": tree_sha,
        "workflow_tree_sha": tree_sha,
        "run_status": "completed",
        "terminal_conclusion": "success",
        "workflow_run_id": run_id,
    }


def git_tree_sha(root: Path, commit_sha: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), "rev-parse", f"{commit_sha}^{{tree}}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def q_version_live_github_verifier(sha: str) -> dict[str, object]:
    tree_sha = "c" * 40
    return {
        "completion_status": "READY",
        "auth_verified": True,
        "branch_protection_status": "verified",
        "remote_matches_local": True,
        "exact_sha_successful_workflow": True,
        "repository_identity_verified": True,
        "repo": "thealphakenya/Alpha-Q-ai",
        "remote_ref": "refs/heads/main",
        "local_head": sha,
        "remote_main_sha": sha,
        "remote_tree_sha": tree_sha,
        "exact_sha_workflow_runs": [{
            "workflow_run_id": 12345,
            "head_sha": sha,
            "head_branch": "main",
            "tree_sha": tree_sha,
            "status": "completed",
            "conclusion": "success",
        }],
    }


def q_version_ollama_reference_audit(
    shas: list[str],
    tree_shas: list[str] | None = None,
) -> dict[str, object]:
    return {
        "status": "PASS",
        "coverage_complete": True,
        "materialized_scope_complete": True,
        "source_manifest_sha256": "c" * 64,
        "unavailable_sources": [],
        "repositories": {
            name: {
                **terminal_remote_sha_binding(
                    name,
                    sha,
                    "run-ollama-audit",
                    tree_shas[index] if tree_shas else "c" * 40,
                ),
                "final_sha": sha,
                "all_refs_enumerated": True,
                "all_pull_requests_included": True,
                "all_intermediate_commit_trees_scanned": True,
                "unavailable_sources": [],
            }
            for index, (name, sha) in enumerate(zip(
                ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"),
                shas,
            ))
        },
    }


def q_version_repository_surface_audit(
    shas: list[str],
    tree_shas: list[str] | None = None,
) -> dict[str, object]:
    surfaces = [
        "markdown", "api", "endpoints", "routes", "ports", "automation", "links",
        "components", "tree", "styles", "universals", "qvillage_qvs", "comparison",
        "qtrade_metrics", "percentages", "production_gaps", "memory",
    ]
    return {
        "status": "PASS",
        "coverage_complete": True,
        "remote_verified": True,
        "semantic_review_complete": True,
        "all_required_surfaces_inventoried": True,
        "all_metrics_mapped": True,
        "source_manifest_sha256": "e" * 64,
        "unavailable_sources": [],
        "repositories": {
            name: {
                **terminal_remote_sha_binding(
                    name,
                    sha,
                    "run-surface-audit",
                    tree_shas[index] if tree_shas else "c" * 40,
                ),
                "final_sha": sha,
                "validated_surfaces": surfaces,
                "all_markdown_structurally_validated": True,
                "all_percentages_mapped": True,
                "all_metric_candidates_mapped": True,
                "unavailable_sources": [],
            }
            for index, (name, sha) in enumerate(zip(
                ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"),
                shas,
            ))
        },
    }


def ui_test_hook_coverage_evidence(
    shas: list[str],
    tree_shas: list[str] | None = None,
) -> dict[str, object]:
    return {
        "status": "PASS",
        "coverage_verified": True,
        "source_manifest_sha256": "d" * 64,
        "unavailable_sources": [],
        "repositories": {
            name: {
                **terminal_remote_sha_binding(
                    name,
                    sha,
                    "run-ui-coverage",
                    tree_shas[index] if tree_shas else "c" * 40,
                ),
                "final_sha": sha,
                "feature_count": 2,
                "test_mapped_feature_count": 2,
                "hook_applicability_reviewed_count": 2,
                "unmapped_feature_count": 0,
                "unreviewed_hook_applicability_count": 0,
                "unmapped_event_hook_count": 0,
                "all_feature_tests_passed": True,
                "all_event_hook_tests_passed": True,
                "unavailable_sources": [],
            }
            for index, (name, sha) in enumerate(zip(
                ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"),
                shas,
            ))
        },
    }


def q_version_qmoi_restore_point_evidence(roots: list[Path], shas: list[str], workflow_run_id: str) -> dict[str, object]:
    repositories = ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced")
    tree_shas = {
        str(root.resolve()): git_tree_sha(root, sha)
        for root, sha in zip(roots, shas)
    }
    return {
        "status": "SUCCESS",
        "branch": "qmoi",
        "master_verified": True,
        "coverage_complete": True,
        "remote_verified": True,
        "workflow_conclusion": "success",
        "workflow_run_id": workflow_run_id,
        "repositories": {
            str(root.resolve()): {
                **terminal_remote_sha_binding(repository, sha, workflow_run_id),
                "branch": "qmoi",
                "checks_passed": True,
                "qmoi_sha": sha,
                "main_sha": sha,
                "backup_sha": sha,
                "master_sha": sha,
                "branch_tree_sha": tree_shas[str(root.resolve())],
                "remote_tree_sha": tree_shas[str(root.resolve())],
                "workflow_tree_sha": tree_shas[str(root.resolve())],
                "remote_ref": "refs/heads/qmoi",
                "remote_ref_sha": sha,
                "workflow_head_sha": sha,
                "required_docs_present": True,
            }
            for root, sha, repository in zip(roots, shas, repositories)
        },
    }


def completion_qmoi_restore_point_evidence(sha: str = "a" * 40) -> dict[str, object]:
    return {
        "status": "PASS",
        "branch": "qmoi",
        "master_verified": True,
        "workspace_sha": sha,
        "tree_sha": "b" * 40,
        "coverage_complete": True,
        "remote_verified": True,
        "workflow_run_id": "run-qmoi-preflight",
        "repositories": {
            name: {
                **terminal_remote_sha_binding(name, sha, "run-qmoi-preflight"),
                "branch": "qmoi",
                "qmoi_sha": sha,
                "main_sha": sha,
                "backup_sha": sha,
                "master_sha": sha,
                "branch_tree_sha": "b" * 40,
                "remote_tree_sha": "b" * 40,
                "workflow_tree_sha": "b" * 40,
                "remote_ref": "refs/heads/qmoi",
                "remote_ref_sha": sha,
                "workflow_head_sha": sha,
                "required_docs_present": True,
            }
            for name in ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced")
        },
    }


def record_successful_q_lifecycle(
    manager: QVersionManager,
    roots: list[Path],
    execution_id: str,
    *,
    status_overrides: dict[str, str] | None = None,
    details_overrides: dict[str, dict[str, object]] | None = None,
) -> None:
    stage_details = {
        "PRODUCT_PLATFORM_CATALOG": {
            "status": "PASS", "coverage_complete": True, "remote_verified": True,
            "unmapped_requirement_count": 0, "unavailable_sources": [], "source_manifest_sha256": "f" * 64,
        },
        "LION_AND_EXTENSION_VARIANTS": {
            "status": "PASS", "coverage_complete": True, "remote_verified": True,
            "unmapped_requirement_count": 0, "unavailable_sources": [], "source_manifest_sha256": "f" * 64,
        },
        "RELEASE_DELIVERY_LIFECYCLE": {
            "status": "PASS", "coverage_complete": True, "remote_verified": True,
            "unmapped_requirement_count": 0, "unavailable_sources": [], "source_manifest_sha256": "f" * 64,
        },
        "QTEAM_ACCOUNTABILITY": {
            "status": "PASS", "coverage_complete": True, "remote_verified": True,
            "unmapped_requirement_count": 0, "unavailable_sources": [], "source_manifest_sha256": "f" * 64,
        },
        "MERGE_APPLY": {
            "decision_ledger_complete": True,
            "conflicts_reviewed": True,
            "unresolved_conflicts": 0,
        },
        "PRODUCTION_SCAN": {
            "production_md_present": True,
            "productionenhanced_md_present": True,
            "unresolved_findings": 0,
        },
        "PRODUCTION_REPLACEMENTS": {
            "replacement_records_verified": True,
            "unresolved_findings": 0,
        },
        "FULL_VALIDATION": {
            "all_required_tests_passed": True,
            "all_markdown_validated": True,
            "inventory_documents_current": True,
        },
        "REMOTE_VERIFICATION": {
            "terminal_conclusion": "success",
            "remote_verified": True,
        },
        "QMOI_RESTORE_POINT": {
            "status": "SUCCESS",
            "branch": "qmoi",
            "master_verified": True,
            "remote_verified": True,
            "coverage_complete": True,
            "workflow_run_id": "run-qmoi-restore",
        },
        "INSTRUCTION_INVENTORY": {
            "repositories": {
                str(root.resolve()): {
                    "status": "PASS",
                    "files_discovered": inventory["files_discovered"],
                    "files_read": inventory["files_read"],
                    "unreadable_or_invalid": [],
                    "source_contents_recorded": False,
                    "files": inventory["files"],
                }
                for root in roots
                for inventory in [audit_instruction_files(root)]
            },
        },
        "MARKDOWN_SOURCE_INDEX": {
            "index_complete": True,
        },
        "UI_TEST_HOOK_COVERAGE": {
            "status": "PASS",
            "coverage_verified": True,
            "feature_count": 2,
            "test_mapped_feature_count": 2,
            "hook_applicability_reviewed_count": 2,
            "unmapped_feature_count": 0,
            "unreviewed_hook_applicability_count": 0,
            "unmapped_event_hook_count": 0,
        },
        "PRODUCTION_READINESS": {
            "status": "CLEAR",
            "coverage_complete": True,
            "candidate_count": 0,
            "unreadable_files": [],
            "oversized_files_not_read": 0,
        },
        "AUTO_CONTINUE_LOOP": {
            "loop_completed": True,
            "iteration_count": 1,
            "retry_limit": 3,
            "retry_limit_respected": True,
            "termination_reason": "success_contract",
            "final_status": "SUCCESS",
        },
        "AUTONOMOUS_COMPLETION": {
            "status": "SUCCESS",
            "execution_id": "completion-final-test",
            "gates": {name: "PASS" for name in REQUIRED_GATES},
            "pending_action_count": 0,
        },
        "REPOSITORY_SURFACE_AUDIT": {
            "coverage_complete": True,
            "source_manifest_sha256": "e" * 64,
            "unavailable_sources": [],
        },
    }
    for stage in QVersionManager.LIFECYCLE_STAGES[:-1]:
        stage_status = (status_overrides or {}).get(stage, "PASS")
        details = dict((details_overrides or {}).get(
            stage,
            stage_details.get(stage, {"decision_ledger_complete": True}),
        ))
        if stage_status == "PASS":
            details.setdefault("source_manifest_sha256", "a" * 64)
            details.setdefault(
                "qaudit_precondition",
                qaudit_precondition(stage, str(details["source_manifest_sha256"])),
            )
        manager.record_lifecycle_stage(
            execution_id,
            stage,
            roots,
            status=stage_status,
            details=details,
            include_inventory=stage == "PRE_MERGE_INVENTORY",
        )


def test_q_version_manager_tracks_complete_autonomous_system_stages():
    assert QVersionManager.LIFECYCLE_STAGES == (
        "MERGE_START",
        "PRE_MERGE_INVENTORY",
        "INSTRUCTION_INVENTORY",
        "INTERNAL_RESEARCH",
        "EXTERNAL_RESEARCH",
        "REPOSITORY_SURFACE_AUDIT",
        "OLLAMA_FULL_COVERAGE_AUDIT",
        "PRODUCT_PLATFORM_CATALOG",
        "LION_AND_EXTENSION_VARIANTS",
        "RELEASE_DELIVERY_LIFECYCLE",
        "QTEAM_ACCOUNTABILITY",
        "MARKDOWN_SOURCE_INDEX",
        "UI_TEST_HOOK_COVERAGE",
        "MERGE_PLAN",
        "MERGE_APPLY",
        "POST_MERGE_AUDIT",
        "POST_AGENT_MERGE_PLAN",
        "POST_AGENT_MERGE_APPLY",
        "POST_AGENT_MERGE_AUDIT",
        "PRODUCTION_SCAN",
        "PRODUCTION_REPLACEMENTS",
        "PRODUCTION_READINESS",
        "FULL_VALIDATION",
        "REMOTE_VERIFICATION",
        "QMOI_RESTORE_POINT",
        "AUTO_CONTINUE_LOOP",
        "AUTONOMOUS_COMPLETION",
        "Q_VERSION_FINALIZATION",
    )


@pytest.mark.parametrize(
    "stage_name",
    [
        "PRODUCT_PLATFORM_CATALOG",
        "LION_AND_EXTENSION_VARIANTS",
        "RELEASE_DELIVERY_LIFECYCLE",
        "QTEAM_ACCOUNTABILITY",
    ],
)
def test_q_version_accountability_stages_require_complete_remote_evidence(stage_name):
    record = {
        "stage_status": "PASS",
        "details": {
            "status": "PASS",
            "coverage_complete": True,
            "remote_verified": True,
            "unmapped_requirement_count": 0,
            "unavailable_sources": [],
            "source_manifest_sha256": "f" * 64,
        },
    }

    QVersionManager.validate_accountability_stage(stage_name, record)

    incomplete = {**record, "details": {**record["details"], "coverage_complete": False}}
    with pytest.raises(RuntimeError, match=f"complete {stage_name} evidence"):
        QVersionManager.validate_accountability_stage(stage_name, incomplete)


def test_q_version_lifecycle_latest_stage_attempt_controls_status(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = "lifecycle-latest-attempt"
    record_successful_q_lifecycle(manager, [root], execution_id)

    manager.record_lifecycle_stage(
        execution_id,
        "AUTONOMOUS_COMPLETION",
        [root],
        status="NEEDS_REVIEW",
        details={"pending_actions": ["remote verification"]},
        include_inventory=False,
    )

    audit = manager.audit_lifecycle(execution_id)
    assert audit["valid"] is True
    assert audit["status"] == "incomplete"
    assert "AUTONOMOUS_COMPLETION" in audit["missing_or_unpassed_stages"]


def test_q_version_pass_without_qaudit_precondition_is_recorded_as_needs_review(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)

    record = manager.record_lifecycle_stage(
        "qaudit-required",
        "MERGE_START",
        [root],
        status="PASS",
        details={"remote_mutation": False},
        include_inventory=False,
    )

    assert record["stage_status"] == "NEEDS_REVIEW"
    assert record["details"]["qaudit_gate"]["status"] == "BLOCKED"
    assert "QAUDITS precondition" in record["details"]["qaudit_gate"]["blocker"]
    audit = manager.audit_lifecycle("qaudit-required")
    assert audit["valid"] is True
    assert "MERGE_START" in audit["missing_or_unpassed_stages"]
    assert audit["qaudit_blocked_stages"] == ["MERGE_START"]
    assert audit["next_stage"] == "MERGE_START"
    assert "Run QAUDITS" in audit["next_action"]


def test_q_version_lifecycle_requires_every_stage_in_canonical_order(tmp_path):
    required_stages = QVersionManager.LIFECYCLE_STAGES[:-1]
    for missing_stage in required_stages:
        root = tmp_path / missing_stage.lower()
        root.mkdir()
        manager = QVersionManager(root)
        execution_id = f"missing-{missing_stage.lower()}"
        for stage in required_stages:
            if stage == missing_stage:
                continue
            manager.record_lifecycle_stage(
                execution_id,
                stage,
                [root],
                status="PASS",
                details={
                    "source_manifest_sha256": "a" * 64,
                    "qaudit_precondition": qaudit_precondition(stage),
                },
                include_inventory=False,
            )

        audit = manager.audit_lifecycle(execution_id)
        assert audit["valid"] is True
        assert audit["status"] == "incomplete"
        assert audit["next_stage"] == missing_stage


def test_q_version_lifecycle_requires_live_remote_completion_gate_before_any_final_readiness(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = "remote-completion-gate"
    record_successful_q_lifecycle(manager, [root], execution_id)

    result = manager.verify_remote_completion_gate(
        execution_id,
        [root],
        {
            "completion_status": "BLOCKED",
            "auth_verified": True,
            "branch_protection_status": "unavailable",
            "remote_matches_local": False,
            "remote_main_sha": "abc" * 10,
            "local_head": "def" * 10,
        },
    )

    assert result["status"] == "BLOCKED"
    assert any("remote completion" in item.lower() for item in result["blockers"])
    assert result["lifecycle_complete"] is True


def test_q_version_remote_gate_does_not_infer_readiness_from_success_flags(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = "remote-completion-no-inference"
    record_successful_q_lifecycle(manager, [root], execution_id)

    result = manager.verify_remote_completion_gate(
        execution_id,
        [root],
        {"status": "SUCCESS", "remote_verified": True, "workflow_conclusion": "success"},
    )

    assert result["status"] == "BLOCKED"
    assert any("exact ref/commit/tree SHA" in item for item in result["blockers"])


@pytest.mark.parametrize("failed_stage", QVersionManager.LIFECYCLE_STAGES[:-1])
def test_q_version_lifecycle_latest_non_pass_blocks_each_stage(tmp_path, failed_stage):
    root = tmp_path / failed_stage.lower()
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = f"failed-{failed_stage.lower()}"
    for stage in QVersionManager.LIFECYCLE_STAGES[:-1]:
        details = {"source_manifest_sha256": "a" * 64}
        stage_status = "NEEDS_REVIEW" if stage == failed_stage else "PASS"
        if stage_status == "PASS":
            details["qaudit_precondition"] = qaudit_precondition(stage)
        manager.record_lifecycle_stage(
            execution_id,
            stage,
            [root],
            status=stage_status,
            details=details,
            include_inventory=False,
        )
        if stage == failed_stage:
            break

    audit = manager.audit_lifecycle(execution_id)
    assert audit["valid"] is True
    assert audit["status"] == "incomplete"
    assert failed_stage in audit["missing_or_unpassed_stages"]
    assert audit["next_stage"] == failed_stage


def test_q_version_lifecycle_rejects_unknown_status_and_tampering(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = "lifecycle-integrity"
    with pytest.raises(ValueError, match="Unsupported lifecycle status"):
        manager.record_lifecycle_stage(
            execution_id,
            "MERGE_START",
            [root],
            status="SUCCESS",
            include_inventory=False,
        )

    manager.record_lifecycle_stage(
        execution_id,
        "MERGE_START",
        [root],
        status="PASS",
        include_inventory=False,
    )
    ledger = root / "ollamatracks" / "q_versions" / execution_id / "lifecycle.jsonl"
    record = json.loads(ledger.read_text(encoding="utf-8"))
    record["stage_status"] = "SUCCESS"
    ledger.write_text(json.dumps(record) + "\n", encoding="utf-8")

    audit = manager.audit_lifecycle(execution_id)
    assert audit["valid"] is False
    assert audit["status"] == "invalid"


def test_q_version_lifecycle_malformed_record_fails_closed(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = "lifecycle-malformed-record"
    ledger = root / "ollamatracks" / "q_versions" / execution_id / "lifecycle.jsonl"
    ledger.parent.mkdir(parents=True)
    ledger.write_text("{}\n", encoding="utf-8")

    audit = manager.audit_lifecycle(execution_id)
    assert audit["valid"] is False
    assert audit["status"] == "invalid"
    assert audit["reason"] == "sequence"
    assert audit["missing_or_unpassed_stages"] == list(QVersionManager.LIFECYCLE_STAGES[:-1])


def test_q_version_lifecycle_rejects_hash_valid_wrong_record_shape(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = "lifecycle-invalid-shape"
    manager.record_lifecycle_stage(
        execution_id,
        "MERGE_START",
        [root],
        status="PASS",
        include_inventory=False,
    )
    ledger = root / "ollamatracks" / "q_versions" / execution_id / "lifecycle.jsonl"
    record = json.loads(ledger.read_text(encoding="utf-8"))
    record["details"] = "not an object"
    unsigned = {key: value for key, value in record.items() if key != "record_sha256"}
    record["record_sha256"] = hashlib.sha256(
        json.dumps(unsigned, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    ledger.write_text(json.dumps(record) + "\n", encoding="utf-8")

    audit = manager.audit_lifecycle(execution_id)
    assert audit["valid"] is False
    assert audit["status"] == "invalid"
    assert audit["reason"] == "record_shape"


def test_q_version_lifecycle_rejects_out_of_order_stage(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = "lifecycle-order"
    manager.record_lifecycle_stage(execution_id, "MERGE_START", [root], include_inventory=False)
    manager.record_lifecycle_stage(execution_id, "INTERNAL_RESEARCH", [root], include_inventory=False)

    with pytest.raises(RuntimeError, match="out of order"):
        manager.record_lifecycle_stage(execution_id, "PRE_MERGE_INVENTORY", [root], include_inventory=False)


def test_q_version_lifecycle_research_sources_strip_url_secrets_and_reject_userinfo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    manager = QVersionManager(root)
    execution_id = "lifecycle-research-source"
    manager.record_lifecycle_stage(
        execution_id,
        "EXTERNAL_RESEARCH",
        [root],
        status="PASS",
        research_sources=[{
            "url": "https://example.com/research?token=not-for-ledger#private",
            "title": "Research source",
            "purpose": "Validate a public documentation claim",
            "content_sha256": "a" * 64,
        }],
        include_inventory=False,
    )
    ledger = root / "ollamatracks" / "q_versions" / execution_id / "lifecycle.jsonl"
    record = json.loads(ledger.read_text(encoding="utf-8"))
    assert record["external_research_sources"][0]["url"] == "https://example.com/research"
    assert "not-for-ledger" not in ledger.read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="must not contain credentials"):
        manager.record_lifecycle_stage(
            execution_id,
            "EXTERNAL_RESEARCH",
            [root],
            status="PASS",
            research_sources=[{"url": "https://user:secret@example.com/private"}],
            include_inventory=False,
        )


def test_completion_is_fail_closed_and_writes_topic_metrics(tmp_path):
    root = make_root(tmp_path)
    result = AutonomousCompletionEngine(root, "execution-1").evaluate()
    assert result.status == "BLOCKED_REQUIRES_HUMAN"
    assert result.stage == "DISCOVERY"
    assert result.evidence["q_version"] is None
    assert result.evidence["q_version_audit"]["latest_materialized_version"] is None
    assert result.evidence["q_version_audit"]["pair"] is None
    assert not list(root.glob("Q.0.0.*"))
    metrics = json.loads((root / "ollamatracks" / "topic_metrics.json").read_text(encoding="utf-8"))
    assert metrics["master_plan_topics"] == 2
    assert metrics["fully_completed"] == 0
    current_state = json.loads((root / "ollamatracks" / "current_state.json").read_text(encoding="utf-8"))
    assert current_state["execution_id"] == "execution-1"
    assert current_state["pending_actions"]
    assert current_state["local_evidence_checks"]["values_recorded"] is False
    inventory = json.loads((root / "ollamatracks" / "instruction_inventory.json").read_text(encoding="utf-8"))
    assert inventory["status"] == "PASS"
    assert inventory["source_contents_recorded"] is False


def test_completion_refreshes_current_state_and_keeps_remote_actions_gated(tmp_path):
    root = make_root(tmp_path)
    (root / "AGENTS.md").write_text("# Repository instructions\n", encoding="utf-8")
    engine = AutonomousCompletionEngine(root, "execution-first")
    first = engine.evaluate()
    first_state = json.loads((root / "ollamatracks" / "current_state.json").read_text(encoding="utf-8"))

    gates = {name: "PASS" for name in REQUIRED_GATES}
    gates["ollama_reference_audit"] = None
    gates["ui_test_hook_coverage"] = None
    markdown_evidence = {
        "remote_verified": True,
        "all_document_content_validated": True,
        "all_remote_refs_enumerated": True,
        "all_pull_requests_included": True,
        "all_intermediate_commit_trees_validated": True,
        "unavailable_sources": [],
        "repositories": {
            name: {
                "terminal_conclusion": "success",
                "remote_verified": True,
                "final_sha": "a" * 40 if name.endswith("Alpha-Q-ai") else "b" * 40,
                "workflow_run_id": "run-verified",
                "markdown_total": 2,
                "markdown_validated": 2,
                "failed_documents": 0,
                "unfetched_refs": 0,
                "unfetched_pull_requests": 0,
                "unvalidated_intermediate_trees": 0,
            }
            for name in ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced")
        },
    }
    second = AutonomousCompletionEngine(root, "execution-second").evaluate(
        gates,
        repository_results={
            "markdown_inventory": markdown_evidence,
            "repository_surface_audit": q_version_repository_surface_audit(["a" * 40, "b" * 40]),
            "ollama_reference_audit": q_version_ollama_reference_audit(["a" * 40, "b" * 40]),
            "ui_test_hook_coverage": ui_test_hook_coverage_evidence(["a" * 40, "b" * 40]),
            "qmoi_restore_point": completion_qmoi_restore_point_evidence(),
        },
    )
    current_state = json.loads((root / "ollamatracks" / "current_state.json").read_text(encoding="utf-8"))

    assert first.status == "BLOCKED_REQUIRES_HUMAN"
    assert first_state["status"] == "BLOCKED_REQUIRES_HUMAN"
    assert second.status == "NO_CHANGES_REQUIRED"
    assert second.gates["ollama_reference_audit"] == "PASS"
    assert second.gates["ui_test_hook_coverage"] == "PASS"
    assert second.gates["qmoi_restore_point"] == "PASS"
    assert current_state["execution_id"] == "execution-second"
    assert current_state["status"] == "NO_CHANGES_REQUIRED"
    assert current_state["pending_actions"] == []
    assert second.evidence["next_actions"] == []
    remote_action = next(action for action in first.evidence["next_actions"] if action["gate"] == "remote_main")
    assert remote_action["status"] == "BLOCKED_REQUIRES_AUTHORIZATION"
    assert remote_action["authorization_required"] is True


def test_completion_requires_complete_dual_repository_ollama_history_audit(tmp_path):
    root = make_root(tmp_path)
    gates = {name: "PASS" for name in REQUIRED_GATES}

    result = AutonomousCompletionEngine(root, "execution-ollama-history").evaluate(gates)

    assert result.gates["ollama_reference_audit"] == "UNKNOWN"
    assert result.evidence["ollama_reference_audit"]["coverage_complete"] is False
    assert result.status == "BLOCKED_REQUIRES_HUMAN"


def test_completion_requires_feature_level_style_test_and_hook_evidence(tmp_path):
    root = make_root(tmp_path)
    gates = {name: "PASS" for name in REQUIRED_GATES}

    result = AutonomousCompletionEngine(root, "execution-ui-test-hooks").evaluate(gates)

    assert result.gates["ui_test_hook_coverage"] == "UNKNOWN"
    assert result.evidence["ui_test_hook_coverage"]["coverage_complete"] is False


def test_completion_requires_current_dual_repository_qmoi_restore_point(tmp_path):
    root = make_root(tmp_path)
    gates = {name: "PASS" for name in REQUIRED_GATES}

    missing = AutonomousCompletionEngine(root, "execution-qmoi-missing").evaluate(gates)
    assert missing.status == "BLOCKED_REQUIRES_HUMAN"
    assert missing.gates["qmoi_restore_point"] == "UNKNOWN"
    assert any(action["gate"] == "qmoi_restore_point" for action in missing.evidence["next_actions"])

    evidence = completion_qmoi_restore_point_evidence()
    verified = AutonomousCompletionEngine(root, "execution-qmoi-present").evaluate(
        gates,
        repository_results={"qmoi_restore_point": evidence},
    )
    assert verified.gates["qmoi_restore_point"] == "PASS"
    assert verified.evidence["qmoi_restore_point"]["coverage_complete"] is True

    missing_master = completion_qmoi_restore_point_evidence()
    del missing_master["repositories"]["thealphakenya/Alpha-Q-ai"]["master_sha"]
    incomplete_master = AutonomousCompletionEngine(root, "execution-qmoi-master-missing").evaluate(
        gates,
        repository_results={"qmoi_restore_point": missing_master},
    )
    assert incomplete_master.gates["qmoi_restore_point"] == "UNKNOWN"

    evidence["repositories"]["thealphakenya/qmoi-enhanced"]["backup_sha"] = "c" * 40
    divergent = AutonomousCompletionEngine(root, "execution-qmoi-divergent").evaluate(
        gates,
        repository_results={"qmoi_restore_point": evidence},
    )
    assert divergent.gates["qmoi_restore_point"] == "UNKNOWN"
    assert divergent.status == "BLOCKED_REQUIRES_HUMAN"


def test_completion_requires_surface_audit_with_all_metrics_and_exact_sha_evidence(tmp_path):
    root = make_root(tmp_path)
    gates = {name: "PASS" for name in REQUIRED_GATES}
    gates["repository_surface_audit"] = None

    missing = AutonomousCompletionEngine(root, "execution-surface-missing").evaluate(gates)
    assert missing.gates["repository_surface_audit"] == "UNKNOWN"

    complete = AutonomousCompletionEngine(root, "execution-surface-complete").evaluate(
        gates,
        repository_results={
            "repository_surface_audit": q_version_repository_surface_audit(["a" * 40, "b" * 40]),
        },
    )
    assert complete.gates["repository_surface_audit"] == "PASS"
    assert complete.evidence["repository_surface_audit"]["coverage_complete"] is True


def test_invalid_local_evidence_forces_final_verification_failure(tmp_path):
    root = make_root(tmp_path)
    (root / "ollamatracks").mkdir(exist_ok=True)
    (root / "ollamatracks" / "telemetry.jsonl").write_text('{"event":\n', encoding="utf-8")

    result = AutonomousCompletionEngine(root, "execution-invalid-evidence").evaluate(
        {name: "PASS" for name in REQUIRED_GATES},
    )

    assert result.evidence["local_evidence_checks"]["status"] == "FAIL"
    assert result.gates["final_verification"] == "FAIL"
    assert result.status == "BLOCKED_REQUIRES_HUMAN"


def test_production_readiness_gap_creates_ranked_action_and_blocks_completion(tmp_path):
    root = make_root(tmp_path)
    gates = {name: "PASS" for name in REQUIRED_GATES}
    gates["production_readiness"] = False

    result = AutonomousCompletionEngine(root, "execution-production-gap").evaluate(gates)

    assert result.status == "BLOCKED_REQUIRES_HUMAN"
    action = next(item for item in result.evidence["next_actions"] if item["gate"] == "production_readiness")
    assert action["priority"] == REQUIRED_GATES.index("production_readiness") + 1
    assert action["status"] == "QUEUED_SAFE_AUTOMATION"


def test_instruction_inventory_reads_scoped_files_without_recording_contents(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# Repository policy\nDo not bypass protections.\n", encoding="utf-8")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "copilot-instructions.md").write_text("# Copilot policy\n", encoding="utf-8")
    (tmp_path / ".github" / "instructions").mkdir(parents=True)
    (tmp_path / ".github" / "instructions" / "api.instructions.md").write_text(
        "# API policy\n\nVerify identity before mutations.\n",
        encoding="utf-8",
    )
    (tmp_path / ".github" / "instructions" / "scoped.instructions.md").write_text(
        "---\napplyTo: \"src/**\"\n---\n# Source policy\nUse focused checks.\n",
        encoding="utf-8",
    )

    result = audit_instruction_files(tmp_path)

    assert result["status"] == "PASS"
    assert result["files_discovered"] == 4
    assert result["files_read"] == 4
    assert result["source_contents_recorded"] is False
    assert {item["apply_to"] for item in result["files"]} == {"repository-wide", "src/**"}
    assert all(len(item["sha256"]) == 64 for item in result["files"])


def test_instruction_inventory_blocks_symlinked_policy_sources(tmp_path):
    outside = tmp_path / "outside.instructions.md"
    outside.write_text("# External instructions\n", encoding="utf-8")
    (tmp_path / "AGENTS.md").write_text("# Root policy\n", encoding="utf-8")
    (tmp_path / ".github" / "copilot-instructions.md").parent.mkdir(parents=True)
    (tmp_path / ".github" / "copilot-instructions.md").write_text("# Copilot policy\n", encoding="utf-8")
    instruction_root = tmp_path / ".github" / "instructions"
    instruction_root.mkdir(parents=True)
    (instruction_root / "linked.instructions.md").symlink_to(outside)

    result = audit_instruction_files(tmp_path)

    assert result["status"] == "FAIL"
    assert result["unreadable_or_invalid"] == [
        {"path": ".github/instructions/linked.instructions.md", "error_type": "SymlinkInstruction"}
    ]


def test_ollama_reference_audit_indexes_materialized_history_without_source_text(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "ollama_agent.py").write_text(
        "# Ollama runtime and model inference\n", encoding="utf-8"
    )
    archived = tmp_path / "qmoi-enhanced-history-14" / "docs"
    archived.mkdir(parents=True)
    (archived / "agent.md").write_text(
        "Ollama workflow history and Q.0.0.N evidence\n", encoding="utf-8"
    )
    qvs_docs = tmp_path / "qmoi-enhanced-history-14" / "QVS"
    qvs_docs.mkdir()
    (qvs_docs / "QVSREADME.md").write_text("# QVS history\n", encoding="utf-8")
    (tmp_path / "QVILLAGE.md").write_text("# QVillage\n", encoding="utf-8")
    (tmp_path / "node_modules" / "third-party").mkdir(parents=True)
    (tmp_path / "node_modules" / "third-party" / "README.md").write_text(
        "Ollama dependency mention\n", encoding="utf-8"
    )

    report = audit_ollama_reference_files(tmp_path)

    assert report["status"] == "NEEDS_REMOTE_HISTORY_EVIDENCE"
    assert report["local_scan"]["complete"] is True
    assert report["local_scan"]["matched_file_count"] == 2
    assert report["local_scan"]["matched_files_by_scope"]["qmoi_enhanced_history"] == 1
    archived_file = next(item for item in report["matched_files"] if item["scope"] == "qmoi_enhanced_history")
    assert "history_and_merges" in archived_file["categories"]
    assert "runtime_and_models" not in archived_file["categories"]
    assert report["coverage_complete"] is False
    assert report["remote_history"]["all_intermediate_commit_trees_scanned"] is False
    qvs_inventory = report["qvillage_qvs_inventory"]
    assert qvs_inventory["coverage_complete"] is False
    assert qvs_inventory["markdown_file_count"] == 2
    assert {item["path"] for item in qvs_inventory["files"]} == {
        "QVILLAGE.md",
        "qmoi-enhanced-history-14/QVS/QVSREADME.md",
    }
    assert all(len(item["sha256"]) == 64 for item in qvs_inventory["files"])
    assert "source_text" not in json.dumps(report)
    assert all(len(item["sha256"]) == 64 for item in report["matched_files"])


def test_ollama_reference_audit_includes_all_local_ref_diff_candidates(tmp_path):
    repository = make_git_repo(tmp_path, "history")
    source = repository / "docs" / "agent.md"
    source.parent.mkdir()
    source.write_text("Ollama is referenced here.\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repository), "add", "docs/agent.md"], check=True)
    subprocess.run(
        ["git", "-C", str(repository), "commit", "-m", "document Ollama agent"],
        check=True,
        capture_output=True,
        text=True,
    )
    source.write_text("Agent documentation remains.\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repository), "add", "docs/agent.md"], check=True)
    subprocess.run(
        ["git", "-C", str(repository), "commit", "-m", "remove old runtime name"],
        check=True,
        capture_output=True,
        text=True,
    )

    report = audit_ollama_reference_files(repository)

    assert report["local_git_history"]["ollama_mention_diff_status"] == "all_local_ref_diffs_scanned"
    assert report["local_git_history"]["ollama_mention_diff_commit_count"] == 2
    historical_path = next(
        item for item in report["local_git_history"]["ollama_mention_diff_paths"]
        if item["path"] == "docs/agent.md"
    )
    assert historical_path["matching_change_commit_count"] == 2


def test_research_system_has_ten_internal_and_ten_external_controls():
    assert len(INTERNAL_RESEARCH_CONTROLS) >= 10
    assert len(EXTERNAL_RESEARCH_CONTROLS) >= 10
    assert len(set(INTERNAL_RESEARCH_CONTROLS)) == len(INTERNAL_RESEARCH_CONTROLS)
    assert len(set(EXTERNAL_RESEARCH_CONTROLS)) == len(EXTERNAL_RESEARCH_CONTROLS)


def test_internal_research_plan_records_roots_and_file_type_metrics(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "agent.py").write_text("print('research')\n", encoding="utf-8")
    (tmp_path / "Guide.MD").write_text("# Research\n", encoding="utf-8")

    plan = build_internal_research_plan([tmp_path])

    assert plan["source_roots"][0]["file_count"] == 2
    assert plan["source_roots"][0]["directory_count"] == 1
    assert plan["source_roots"][0]["file_types"][".py"] == 1
    assert plan["source_roots"][0]["file_types"][".md"] == 1
    assert plan["automatic_merge_authorized"] is False


def test_repository_surface_audit_tracks_markdown_metrics_without_source_text(tmp_path):
    (tmp_path / "src" / "components").mkdir(parents=True)
    (tmp_path / "src" / "api").mkdir(parents=True)
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / "README.md").write_text(
        "# Audit fixture\n\nNever emit this exact sentence. Accuracy is 70%.\n[API](API.md) [missing](missing.md)\n",
        encoding="utf-8",
    )
    (tmp_path / "API.md").write_text("# API\n\nGET /health\n", encoding="utf-8")
    (tmp_path / "compare.md").write_text(
        "# Model comparison\n\n| Model | Accuracy |\n| --- | --- |\n| QMOI | 80% |\n",
        encoding="utf-8",
    )
    (tmp_path / "Qtrade.md").write_text(
        "# Qtrade metrics\n\nWin rate: 61%; Sharpe ratio is a metric candidate.\n",
        encoding="utf-8",
    )
    (tmp_path / "projectsandautoprojects.md").write_text(
        "# Master projects\n\nExisting project registry.\n", encoding="utf-8"
    )
    (tmp_path / "QVILLAGE.md").write_text("# QVillage\n", encoding="utf-8")
    (tmp_path / "QVS.md").write_text("# QVS\n", encoding="utf-8")
    historical_qvs = tmp_path / "qmoi-enhanced-history-14" / "QVS"
    historical_qvs.mkdir(parents=True)
    (historical_qvs / "ENHANCEDQVS.md").write_text("# Enhanced QVS\n", encoding="utf-8")
    (tmp_path / "src" / "components" / "Button.tsx").write_text(
        "export const Button = () => null;\n", encoding="utf-8"
    )
    (tmp_path / "src" / "api" / "route.py").write_text(
        "def get_health():\n    return {}\n", encoding="utf-8"
    )
    (tmp_path / "src" / "metrics.py").write_text(
        "# confidence threshold 55%\n", encoding="utf-8"
    )
    (tmp_path / ".github" / "workflows" / "audit.yml").write_text(
        "name: Audit\non: [push]\n", encoding="utf-8"
    )
    tracker_dir = tmp_path / "ollamatracks"
    tracker_dir.mkdir()
    (tracker_dir / "repository_surface_audit.json").write_text(
        '{"previous":"generated report"}\n', encoding="utf-8"
    )
    (tracker_dir / "qaudit_markdown_sentence_audit.json").write_text(
        '{"previous":"generated sentence manifest"}\n', encoding="utf-8"
    )
    (tracker_dir / "qaudit_markdown_sentence_audit.jsonl.gz").write_bytes(b"generated report")
    for filename in ("oe2.txt", "remotecompletion.md", "remote-completion.json", "remote-evidence-ledger.jsonl"):
        (tmp_path / filename).write_text("mutable evidence output\n", encoding="utf-8")

    report = audit_repository_surfaces([tmp_path])
    serialized = json.dumps(report)
    root_report = report["roots"][0]
    markdown = {item["path"]: item for item in root_report["markdown_records"]}

    assert report["status"] == "NEEDS_REVIEW"
    assert report["surface_document_counts"]["api"] == 1
    assert report["surface_document_counts"]["comparison"] == 1
    assert report["surface_document_counts"]["trading"] == 1
    assert report["surface_document_counts"]["qvillage_qvs"] == 3
    assert report["surface_document_counts"]["projects_autoprojects"] == 1
    assert report["component_source_count"] == 1
    assert report["api_or_endpoint_source_count"] == 1
    assert report["percentage_occurrence_count"] == 4
    assert len(report["percentage_summary_by_path"]) == 4
    assert report["calculation_candidate_line_count"] >= 1
    assert report["instruction_candidate_line_count"] >= 1
    assert report["instruction_candidate_file_count"] >= 1
    assert all(
        item["interpretation"] == "descriptive_unclassified_percentages_not_comparable_performance_proof"
        for item in report["percentage_summary_by_path"]
    )
    assert "model-evaluation" in report["research_topics"]
    assert "metrics_and_comparisons" in report["research_domains"]
    assert "projects_and_autoprojects" in report["research_domains"]
    assert markdown["README.md"]["local_link_error_count"] == 1
    assert markdown["compare.md"]["comparison_table_row_count"] == 3
    assert root_report["git_history"]["intermediate_commit_trees_scanned"] is False
    assert "Never emit this exact sentence." not in serialized
    assert "must be fulfilled" not in serialized
    assert report["source_text_recorded"] is False
    self_record = next(
        item for item in report["all_file_records"]
        if item["path"] == "ollamatracks/repository_surface_audit.json"
    )
    assert self_record["status"] == "self_referential_excluded"
    assert self_record["sha256"] is None
    assert report["self_referential_exclusions"] == [
        "ollamatracks/qaudit_markdown_sentence_audit.json",
        "ollamatracks/qaudit_markdown_sentence_audit.jsonl.gz",
        "ollamatracks/repository_surface_audit.json",
        "oe2.txt",
        "remote-completion.json",
        "remote-evidence-ledger.jsonl",
        "remotecompletion.md",
    ]
    assert "remotecompletion.md" not in {item["path"] for item in root_report["markdown_records"]}
    for filename in ("oe2.txt", "remotecompletion.md", "remote-completion.json", "remote-evidence-ledger.jsonl"):
        record = next(item for item in report["all_file_records"] if item["path"] == filename)
        assert record["status"] == "self_referential_excluded"
        assert record["bytes"] is None
        (tmp_path / filename).write_text("refreshed evidence with different size\n", encoding="utf-8")
    refreshed = audit_repository_surfaces([tmp_path])
    assert refreshed["source_manifest_sha256"] == report["source_manifest_sha256"]
    assert all(item["source_text_recorded"] is False for item in report["instruction_candidates"])
    assert all(len(item["sha256"]) == 64 for item in report["all_file_records"] if item["sha256"])
    assert report["markdown_sentence_records_indexed"] >= 0


def test_markdown_sentence_evidence_writer_is_compressed_and_source_text_free(tmp_path):
    sentence = {
        "text": "The sentence text itself.",
        "sentence_index": 1,
        "line_start": 1,
        "line_end": 1,
        "word_count": 4,
        "sentence_sha256": "a" * 64,
        "word_sequence_sha256": "b" * 64,
        "duplicate_adjacent_word_candidate": False,
        "metric_claim_candidate": False,
        "completion_claim_candidate": True,
        "reference_marker_present": True,
        "semantic_status": "unverified_requires_source_and_owner_mapping",
    }
    report = {
        "generated_at": "2026-10-07T00:00:00Z",
        "scope": "materialized repository roots and local refs only",
        "status": "MATERIALIZED_AUDIT_COMPLETE_REMOTE_HISTORY_INCOMPLETE",
        "source_manifest_sha256": "c" * 64,
        "source_text_recorded": False,
        "roots": [{
            "root": str(tmp_path.resolve()),
            "markdown_records": [{
                "path": "README.md",
                "scope": "materialized_repository",
                "bytes": 45,
                "sha256": "d" * 64,
                "line_count": 1,
                "word_count": 4,
                "sentence_count_heuristic": 1,
                "sentence_records": [sentence],
                "sentence_records_omitted_by_bound": 0,
                "status": "structurally_validated",
                "review_reasons": [],
                "local_link_error_count": 0,
                "semantic_validation": "integrity_is_hash_checked; each sentence still requires source_and_owner_review",
            }],
        }],
        "unreadable_file_count": 0,
        "skipped_source_count": 0,
    }

    manifest = write_markdown_sentence_audit(
        tmp_path,
        report,
        correlation_id="sentence-audit-test",
    )
    artifact = tmp_path / manifest["artifact_path"]
    rows = [json.loads(line) for line in gzip.decompress(artifact.read_bytes()).splitlines()]

    assert manifest["correlation_id"] == "sentence-audit-test"
    assert manifest["schema_version"] == 4
    assert manifest["totals"]["sentence_records_indexed"] == 1
    assert manifest["remote_verified"] is False
    assert manifest["source_text_recorded"] is False
    assert [row["record_type"] for row in rows] == ["manifest", "document", "sentence"]
    assert rows[-1]["sentence_sha256"] == "a" * 64
    serialized = gzip.decompress(artifact.read_bytes()).decode("utf-8")
    assert "The sentence text itself." not in serialized
    assert rows[-1]["source_text_recorded"] is False
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == manifest["artifact_sha256"]
    assert len(artifact.read_bytes()) == manifest["artifact_bytes"]


def test_markdown_sentence_evidence_tracks_lines_and_counts_candidates_past_bound(monkeypatch):
    monkeypatch.setattr("scripts.ollama_research.MAX_MARKDOWN_SENTENCE_RECORDS", 2)

    evidence = _markdown_sentence_evidence(
        "Repeated repeated words.\n\nMetric accuracy 80%.\nSuccessful completion."
    )

    assert evidence["sentence_count_heuristic"] == 3
    assert len(evidence["sentence_records"]) == 2
    assert evidence["sentence_records_omitted_by_bound"] == 1
    assert evidence["sentence_records"][0]["line_start"] == 1
    assert evidence["sentence_records"][0]["line_end"] == 1
    assert evidence["sentence_records"][1]["line_start"] == 3
    assert evidence["sentence_records"][1]["line_end"] == 3
    assert evidence["duplicate_adjacent_word_candidate_count"] == 1
    assert evidence["metric_claim_candidate_count"] == 1
    assert evidence["completion_claim_candidate_count"] == 1
    assert evidence["unreferenced_metric_claim_candidate_count"] == 1
    assert evidence["unreferenced_completion_claim_candidate_count"] == 1


def test_qaudit_checkpoint_appends_paired_ledgers_and_keeps_remote_blocked(tmp_path):
    root = tmp_path / "Alpha-Q-ai"
    root.mkdir()
    for filename in ("oe2.txt", "remotecompletion.md", "remote-evidence-ledger.jsonl"):
        (root / filename).write_text("", encoding="utf-8")
    (root / "remote-completion.json").write_text(
        json.dumps({"schema_version": "1.0", "state": {}, "blockers": []}),
        encoding="utf-8",
    )
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "audit@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Audit Test"], check=True)
    (root / "README.md").write_text("# Test\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "test checkpoint"], check=True, capture_output=True)
    subprocess.run(
        ["git", "-C", str(root), "remote", "add", "origin", "git@github.com:thealphakenya/Alpha-Q-ai.git"],
        check=True,
    )

    checkpoint = record_qaudit_checkpoint(
        root,
        "qaudit-test",
        {
            "status": "NEEDS_REVIEW",
            "source_manifest_sha256": "a" * 64,
            "artifact_path": "ollamatracks/audit.json",
            "artifact_sha256": "b" * 64,
            "artifact_bytes": 123,
            "metrics": {"files": 1},
            "blockers": ["incomplete_local_input"],
        },
    )

    oe2 = (root / "oe2.txt").read_text(encoding="utf-8")
    remote = (root / "remotecompletion.md").read_text(encoding="utf-8")
    completion = json.loads((root / "remote-completion.json").read_text(encoding="utf-8"))
    ledger = [json.loads(line) for line in (root / "remote-evidence-ledger.jsonl").read_text().splitlines()]
    assert checkpoint["repository"] == "thealphakenya/Alpha-Q-ai"
    assert checkpoint["repository_identity_verified"] is True
    assert checkpoint["remote_verified"] is False
    assert oe2 == remote
    assert checkpoint["correlation_id"] in oe2
    assert completion["correlation_id"] == checkpoint["correlation_id"]
    assert completion["state"]["remote_completion"] == "BLOCKED"
    assert completion["state"]["remote_verified"] is False
    assert len(ledger) == 1
    assert ledger[0]["correlation_id"] == checkpoint["correlation_id"]
    assert ledger[0]["verification"]["terminal"] is False


def test_qaudit_paired_append_rolls_back_when_one_target_is_a_symlink(tmp_path):
    oe2 = tmp_path / "oe2.txt"
    remote = tmp_path / "remotecompletion.md"
    remote_target = tmp_path / "remote-target.md"
    oe2.write_text("prior continuation\n", encoding="utf-8")
    remote_target.write_text("prior remote evidence\n", encoding="utf-8")
    remote.symlink_to(remote_target)

    with pytest.raises(RuntimeError, match="through symlink"):
        _append_pair_locked((oe2, remote), b"new checkpoint\n")

    assert oe2.read_text(encoding="utf-8") == "prior continuation\n"
    assert remote_target.read_text(encoding="utf-8") == "prior remote evidence\n"


def test_qaudit_paired_append_rolls_back_after_partial_write(tmp_path, monkeypatch):
    oe2 = tmp_path / "oe2.txt"
    remote = tmp_path / "remotecompletion.md"
    oe2.write_text("prior continuation\n", encoding="utf-8")
    remote.write_text("prior remote evidence\n", encoding="utf-8")
    original_write = os.write
    write_count = 0

    def fail_second_write(descriptor, content):
        nonlocal write_count
        write_count += 1
        if write_count == 2:
            raise OSError("simulated paired-write failure")
        return original_write(descriptor, content)

    monkeypatch.setattr("scripts.qaudit_checkpoint.os.write", fail_second_write)
    with pytest.raises(OSError, match="simulated paired-write failure"):
        _append_pair_locked((oe2, remote), b"new checkpoint\n")

    assert oe2.read_text(encoding="utf-8") == "prior continuation\n"
    assert remote.read_text(encoding="utf-8") == "prior remote evidence\n"


def test_qaudit_checkpoint_resolves_only_explicitly_closed_run_blockers(tmp_path):
    root = tmp_path / "Alpha-Q-ai"
    root.mkdir()
    for filename in ("oe2.txt", "remotecompletion.md", "remote-evidence-ledger.jsonl"):
        (root / filename).write_text("", encoding="utf-8")
    (root / "remote-completion.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "state": {},
                "blockers": ["audit_inventory_run_not_yet_terminal", "historical_remote_blocker"],
            }
        ),
        encoding="utf-8",
    )
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "audit@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Audit Test"], check=True)
    (root / "README.md").write_text("# Test\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-m", "test checkpoint recovery"],
        check=True,
        capture_output=True,
    )

    checkpoint = record_qaudit_checkpoint(
        root,
        "audit-inventory",
        {
            "status": "NEEDS_REVIEW",
            "resolved_blockers": ["audit_inventory_run_not_yet_terminal"],
            "blockers": ["local_audit_needs_review"],
        },
        correlation_id="audit-run-correlation",
    )

    completion = json.loads((root / "remote-completion.json").read_text(encoding="utf-8"))
    assert checkpoint["correlation_id"] == "audit-run-correlation"
    assert "audit_inventory_run_not_yet_terminal" not in completion["blockers"]
    assert "historical_remote_blocker" in completion["blockers"]
    assert "local_audit_needs_review" in completion["blockers"]
    assert completion["state"]["remote_verified"] is False


def test_markdown_audit_indexes_sentence_and_word_sequence_evidence_without_prose(tmp_path):
    (tmp_path / "README.md").write_text(
        "## Release status\nThe build passed 3 tests. Release is complete. A a repeated word.\n",
        encoding="utf-8",
    )
    (tmp_path / "ORCHESTRATION.md").write_text(
        "# Orchestration\n\nA coordinated orchestration pipeline.\n",
        encoding="utf-8",
    )
    (tmp_path / "TREE.md").write_text("# Tree inventory\n", encoding="utf-8")
    archived_release = tmp_path / "Alpha-Q-ai-2025" / "RELEASES.md"
    archived_release.parent.mkdir()
    archived_release.write_text("# Historical release snapshot\n", encoding="utf-8")

    report = audit_repository_surfaces([tmp_path])
    markdown = report["roots"][0]["markdown_records"][0]
    serialized = json.dumps(report)

    assert markdown["sentence_count_heuristic"] == 4
    assert len(markdown["sentence_records"]) == 4
    assert markdown["sentence_records"][1]["line_start"] == 2
    assert markdown["sentence_records"][1]["line_end"] == 2
    assert len(markdown["sentence_records"][1]["sentence_sha256"]) == 64
    assert len(markdown["sentence_records"][1]["word_sequence_sha256"]) == 64
    assert markdown["sentence_records"][1]["completion_claim_candidate"] is True
    assert markdown["sentence_records"][1]["reference_marker_present"] is False
    assert markdown["sentence_records"][3]["duplicate_adjacent_word_candidate"] is True
    assert report["markdown_sentence_records_indexed"] == 4
    assert report["markdown_unreferenced_completion_claim_candidate_count"] == 2
    by_path = {item["path"]: item for item in report["roots"][0]["markdown_records"]}
    assert "orchestration" in by_path["ORCHESTRATION.md"]["document_families"]
    assert "tree_inventory" in by_path["TREE.md"]["document_families"]
    assert by_path["Alpha-Q-ai-2025/RELEASES.md"]["scope"] == "historical_or_archive_candidate"
    assert report["document_family_counts"]["orchestration"] == 1
    assert report["document_family_counts"]["release_tag_publish"] == 2
    assert "The build passed 3 tests." not in serialized


def test_repository_audit_refreshes_release_and_all_contract_docs_in_managed_sections(tmp_path):
    root = tmp_path.resolve()
    (root / "RELEASES.md").write_text("# Releases\n\nHuman release policy.\n", encoding="utf-8")
    (root / "ALLBUILD.md").write_text("# Build contract\n\nHuman build notes.\n", encoding="utf-8")
    (root / "QTEAM.md").write_text("# QTeam\n\nHuman ownership notes.\n", encoding="utf-8")
    (root / "ORCHESTRATION.md").write_text(
        "# Orchestration\n\nThe orchestration pipeline runs coordinated project actions.\n",
        encoding="utf-8",
    )
    (root / "TREE_FULL_STRUCTURE.md").write_text(
        "# Full tree\n\nHuman tree documentation.\n",
        encoding="utf-8",
    )
    (root / "NOTES.md").write_text("# Notes\n\nUnaffected.\n", encoding="utf-8")
    historical = root / "qmoi-enhanced-history-14" / "RELEASES.md"
    historical.parent.mkdir()
    historical.write_text("# Historical releases\n\nPreserved snapshot.\n", encoding="utf-8")
    markdown_records = [
        {
            "root": str(root),
            "path": name,
            "suffix": ".md",
            "scope": source_scope,
            "document_families": families,
            "bytes": 10,
            "status": "indexed",
        }
        for name, families, source_scope in (
            ("RELEASES.md", ["release_tag_publish"], "materialized_repository"),
            ("ALLBUILD.md", ["build_download_install"], "materialized_repository"),
            ("QTEAM.md", ["qteam_accountability"], "materialized_repository"),
            ("ORCHESTRATION.md", ["orchestration"], "materialized_repository"),
            ("TREE_FULL_STRUCTURE.md", ["tree_inventory"], "materialized_repository"),
            ("NOTES.md", [], "materialized_repository"),
            ("qmoi-enhanced-history-14/RELEASES.md", ["release_tag_publish"], "historical_or_archive_candidate"),
        )
    ]
    audit = {
        "all_file_records": markdown_records,
        "all_directory_records": [{
            "root": str(root),
            "path": "src",
            "file_count_in_subtree": 2,
        }],
        "roots": [{
            "root": str(root),
            "markdown_records": [],
            "skipped": [{"path": "node_modules", "reason": "excluded_generated_or_dependency_directory"}],
            "unreadable": [],
            "git_history": {"refs": ["refs/tags/v1.0.0"]},
        }],
        "links": [],
        "document_family_counts": {
            "build_download_install": 1,
            "orchestration": 1,
            "qteam_accountability": 1,
            "release_tag_publish": 2,
            "tree_inventory": 1,
        },
    }

    OllamaAutonomousAgent.refresh_repository_audit_documents(
        OllamaAutonomousAgent.__new__(OllamaAutonomousAgent),
        root,
        audit,
    )

    releases = (root / "RELEASES.md").read_text(encoding="utf-8")
    build = (root / "ALLBUILD.md").read_text(encoding="utf-8")
    qteam = (root / "QTEAM.md").read_text(encoding="utf-8")
    orchestration = (root / "ORCHESTRATION.md").read_text(encoding="utf-8")
    tree_full = (root / "TREE_FULL_STRUCTURE.md").read_text(encoding="utf-8")
    tree = (root / "TREE.md").read_text(encoding="utf-8")
    notes = (root / "NOTES.md").read_text(encoding="utf-8")
    archived_releases = historical.read_text(encoding="utf-8")
    assert "Human release policy." in releases
    assert "<!-- BEGIN QMOI MANAGED: release-evidence -->" in releases
    assert "local tag refs observed: `1`" in releases
    assert "<!-- BEGIN QMOI MANAGED: repository-surface-audit -->" in build
    assert "<!-- BEGIN QMOI MANAGED: repository-surface-audit -->" in qteam
    assert "<!-- BEGIN QMOI MANAGED: repository-surface-audit -->" in orchestration
    assert "<!-- BEGIN QMOI MANAGED: repository-surface-audit -->" in tree_full
    assert "Indexed files" in tree
    assert "ALLBUILD.md" in tree
    assert "node_modules" in tree
    assert "Unaffected." in notes
    assert "Preserved snapshot." in archived_releases
    assert "<!-- BEGIN QMOI MANAGED:" not in archived_releases
    assert "<!-- BEGIN QMOI MANAGED:" not in notes


def test_repository_audit_refresh_preserves_history_policy_and_q_version_files(tmp_path):
    root = tmp_path.resolve()
    protected_files = {
        "AGENTS.md": "# Agent policy\n\nRelease requirements must be preserved.\n",
        ".github/copilot-instructions.md": "# Copilot policy\n\nRelease requirements must be preserved.\n",
        ".github/instructions/security.instructions.md": "---\napplyTo: '**'\n---\nRelease requirements must be preserved.\n",
        "Q.0.0.N/COMPLETION.md": "# Q completion\n\nRelease requirements must be preserved.\n",
        "qmoi-enhanced-history-14/RELEASES.md": "# Archived releases\n\nRelease requirements must be preserved.\n",
        "SESSION_COMPLETION_REPORT_2025_10_05.md": "# Historical report\n\nRelease requirements must be preserved.\n",
    }
    for relative, content in protected_files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    releases_path = root / "RELEASES.md"
    releases_path.write_text("# Releases\n\nHuman release policy.\n", encoding="utf-8")

    audit = audit_repository_surfaces([root])
    scope_by_path = {
        item["path"]: item["scope"]
        for item in audit["roots"][0]["markdown_records"]
    }
    assert scope_by_path["qmoi-enhanced-history-14/RELEASES.md"] == "historical_or_archive_candidate"
    assert scope_by_path["SESSION_COMPLETION_REPORT_2025_10_05.md"] == "historical_or_archive_candidate"

    OllamaAutonomousAgent.refresh_repository_audit_documents(
        OllamaAutonomousAgent.__new__(OllamaAutonomousAgent),
        root,
        audit,
    )

    assert "<!-- BEGIN QMOI MANAGED: release-evidence -->" in releases_path.read_text(encoding="utf-8")
    for relative, original in protected_files.items():
        assert (root / relative).read_text(encoding="utf-8") == original


def test_qaudit_refreshes_style_universal_and_transition_docs_from_one_manifest(tmp_path):
    documents = (
        "STYLES.md",
        "QAUDITS.md",
        "UNIVERSALS.md",
        "UNIVERSAL.md",
        "TRANSION.md",
        "TRANSITION.md",
    )
    for filename in documents:
        (tmp_path / filename).write_text(f"# {filename}\n\nAuthored content.\n", encoding="utf-8")
    universe = {
        "correlation_id": "audit-correlation-123",
        "generated_at": "2026-10-08T00:00:00Z",
        "metrics": {
            "source_scope": "materialized_local_only",
            "source_manifest_sha256": "a" * 64,
            "category_candidate_path_counts": {"disability_accessibility": 2},
            "test_mapped_candidate_count": 0,
            "hook_reviewed_candidate_count": 0,
        },
        "inventory": {"styles": [{"path": "styles/tokens.css"}], "universals": []},
        "accountability": {"lion_variation_candidate_count": 3, "registered_extension_count": 2},
        "classes": {
            "docs/accessibility.md": {
                "path": "docs/accessibility.md",
                "categories": ["disability_accessibility"],
            },
            "src/chat.tsx": {"path": "src/chat.tsx", "categories": ["chat_interfaces"]},
        },
    }
    agent = OllamaAutonomousAgent.__new__(OllamaAutonomousAgent)

    result = agent.refresh_qaudit_governance_documents(tmp_path, universe)
    repeated = agent.refresh_qaudit_governance_documents(tmp_path, universe)

    assert result["status"] == "UPDATED"
    assert result["updated_documents"] == list(documents)
    assert result["accessibility_markdown_candidate_count"] == 1
    assert result["evolution_plan_artifact"] == "ollamatracks/qaudits_evolution_plan.json"
    plan = json.loads((tmp_path / result["evolution_plan_artifact"]).read_text(encoding="utf-8"))
    assert plan["qstats"]["source_manifest_sha256"] == "a" * 64
    assert result["qlion"] == {
        "variation_candidate_count": 3,
        "registered_extension_count": 2,
        "remote_verified": False,
    }
    assert repeated["status"] == "UPDATED"
    for filename in documents:
        content = (tmp_path / filename).read_text(encoding="utf-8")
        assert "Authored content." in content
        assert content.count("BEGIN QMOI MANAGED: qaudit-style-universal-accessibility-coverage") == 1
        assert "audit-correlation-123" in content
        assert "disability is inferred" in content
        assert "QStats:" in content
        assert "QLion:" in content


def test_external_research_allowlist_rejects_credentials_and_unapproved_domains():
    source_url = "https://docs.github.com/rest?access_token=not-stored#section"
    candidate = discover_resource_candidates(
        source_url,
        ["https://docs.python.org/3/library/", "https://docs.github.com.attacker.invalid/page"],
    )
    assert candidate[0]["status"] == "allowlisted_candidate"
    assert "?" not in candidate[0]["source_url"]
    assert candidate[1]["status"] == "review_required"
    with pytest.raises(ValueError, match="credentials"):
        discover_resource_candidates("https://user:pass@docs.github.com/page", [])


def test_external_research_fetch_is_bounded_and_records_digest(monkeypatch):
    class Response:
        status = 200

        class Headers:
            @staticmethod
            def get_content_type():
                return "text/plain"

        headers = Headers()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return None

        def read(self, amount):
            assert amount == 1025
            return b"official docs"

    class Opener:
        def open(self, request, timeout):
            assert request.full_url == "https://docs.python.org/3/"
            assert timeout == 5
            return Response()

    monkeypatch.setattr("scripts.ollama_research.urllib.request.build_opener", lambda *_: Opener())
    result = fetch_official_resource("https://docs.python.org/3/?tracking=removed", timeout_seconds=5, max_bytes=1024)
    assert result["status"] == "FETCHED"
    assert result["content_sha256"]
    assert result["credential_values_recorded"] is False


def test_research_visit_requires_exact_source_and_records_content_hash():
    visit = record_research_visit(
        url="https://docs.github.com/actions",
        title="Actions docs",
        question="How do workflow permissions work?",
        purpose="Validate least-privilege workflow permissions",
        content=b"official source bytes",
        findings=["workflow token permissions are explicit"],
        limitations=["does not prove this repository permission"],
        repository="thealphakenya/Alpha-Q-ai",
        ref="main",
        source_sha="a" * 40,
    )
    assert visit["content_sha256"] == hashlib.sha256(b"official source bytes").hexdigest()
    assert visit["visited_at"].endswith("Z")
    assert visit["validation_case_ids"] == []
    with pytest.raises(ValueError, match="exact source SHA"):
        record_research_visit(
            url="https://docs.github.com/actions",
            title="Actions docs",
            question="question",
            purpose="purpose",
            content=b"x",
            findings=[],
            limitations=[],
            repository="repo",
            ref="main",
            source_sha="unknown",
        )


def test_repo_cleanup_policy_keeps_ollama_outside_q_version_only(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "README.md").write_text("# QMOI\nOllama is not the product name.\n", encoding="utf-8")
    qdir = repo / "Q.0.0.N"
    qdir.mkdir()
    (qdir / "manifest.md").write_text("Ollama final version artifact.\n", encoding="utf-8")

    result = sanitize_repo_ollama_mentions(repo)

    text = (repo / "README.md").read_text(encoding="utf-8")
    q_text = (qdir / "manifest.md").read_text(encoding="utf-8")
    assert "Ollama" not in text and "ollama" not in text.lower()
    assert "Ollama" in q_text or "ollama" in q_text.lower()
    assert result["files_sanitized"] >= 1
    assert result["status"] == "OK"


def test_completion_rejects_markdown_gate_without_full_remote_inventory_evidence(tmp_path):
    root = make_root(tmp_path)
    gates = {name: "PASS" for name in REQUIRED_GATES}

    result = AutonomousCompletionEngine(root, "execution-markdown").evaluate(
        gates,
        repository_results={"markdown_inventory": {"remote_verified": True}},
    )

    assert result.status == "BLOCKED_REQUIRES_HUMAN"
    assert result.gates["markdown_inventory"] == "UNKNOWN"
    assert "markdown_inventory=UNKNOWN" in result.errors


def test_completion_accepts_markdown_gate_only_with_complete_dual_repo_evidence(tmp_path):
    root = make_root(tmp_path)
    gates = {name: "PASS" for name in REQUIRED_GATES}
    repository_evidence = {
        name: {
            **terminal_remote_sha_binding(
                name,
                "a" * 40 if name.endswith("Alpha-Q-ai") else "b" * 40,
                "run-123",
            ),
            "final_sha": "a" * 40 if name.endswith("Alpha-Q-ai") else "b" * 40,
            "markdown_total": 4,
            "markdown_validated": 4,
            "failed_documents": 0,
            "unfetched_refs": 0,
            "unfetched_pull_requests": 0,
            "unvalidated_intermediate_trees": 0,
        }
        for name in ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced")
    }
    markdown_evidence = {
        "remote_verified": True,
        "all_document_content_validated": True,
        "all_remote_refs_enumerated": True,
        "all_pull_requests_included": True,
        "all_intermediate_commit_trees_validated": True,
        "unavailable_sources": [],
        "repositories": repository_evidence,
    }

    result = AutonomousCompletionEngine(root, "execution-markdown-complete").evaluate(
        gates,
        repository_results={
            "primary": {"changed_files": ["QVERSIONMANAGER.md"]},
            "secondary": {"changed_files": ["QVERSIONMANAGER.md"]},
            "markdown_inventory": markdown_evidence,
            "repository_surface_audit": q_version_repository_surface_audit(
                [item["final_sha"] for item in repository_evidence.values()],
                [item["remote_tree_sha"] for item in repository_evidence.values()],
            ),
                "ollama_reference_audit": q_version_ollama_reference_audit(
                    [item["final_sha"] for item in repository_evidence.values()],
                    [item["remote_tree_sha"] for item in repository_evidence.values()],
                ),
                "ui_test_hook_coverage": ui_test_hook_coverage_evidence(
                    [item["final_sha"] for item in repository_evidence.values()],
                    [item["remote_tree_sha"] for item in repository_evidence.values()],
                ),
                "qmoi_restore_point": completion_qmoi_restore_point_evidence(),
        },
    )

    assert result.status == "SUCCESS"
    assert result.gates["markdown_inventory"] == "PASS"


def test_checkpoint_and_lock_are_resumable_and_exclusive(tmp_path):
    root = make_root(tmp_path)
    manager = CheckpointManager(root)
    manager.record_stage("e1", "DISCOVERY", "PASS", next_operation="INSPECTION")
    assert manager.resume_state("e1")["completed_stages"] == ["DISCOVERY"]
    lock = ExecutionLock(root, "sync-1")
    lock.acquire("e1")
    try:
        ExecutionLock(root, "sync-1").acquire("e2")
    except RuntimeError:
        pass
    else:
        raise AssertionError("active lock was not enforced")
    assert lock.release("e1") is True


def test_q_version_and_sync_contract_are_explicit(tmp_path):
    root = make_root(tmp_path)
    version = QVersionManager(root).reserve()
    assert version == "Q.0.0.1"
    contract = build_sync_contract("sync-1", "Alpha-Q-ai", "qmoi-enhanced", "a", "b", mode="apply", authorization="AUTH_BLOCKED")
    assert contract.requires_target_workflow() is True
    assert contract.as_dict()["contract_hash"]


def test_q_version_identifiers_are_canonical_and_strict():
    assert QVersionManager.parse_version("Q.0.0.12") == 12
    for value in ("Q.0.0.0", "Q.0.0.01", "Q.0.0.1.md", "Q.0.0.1-extra", "Q.1.0.1"):
        with pytest.raises(ValueError):
            QVersionManager.parse_version(value)


def test_qaudit_precondition_requires_matching_complete_manifest(tmp_path):
    precondition = qaudit_precondition("UI_TEST_HOOK_COVERAGE")
    QVersionManager.validate_qaudit_precondition(
        "UI_TEST_HOOK_COVERAGE",
        precondition,
        expected_manifest_sha256="a" * 64,
    )

    with pytest.raises(RuntimeError, match="complete current QAUDITS precondition"):
        QVersionManager.validate_qaudit_precondition(
            "UI_TEST_HOOK_COVERAGE",
            {**precondition, "source_manifest_sha256": "b" * 64},
            expected_manifest_sha256="a" * 64,
        )
    incomplete_metric = {
        **precondition,
        "required_metrics": [{
            **precondition["required_metrics"][0],
            "numerator": 0,
        }],
    }
    with pytest.raises(RuntimeError, match="complete current QAUDITS precondition"):
        QVersionManager.validate_qaudit_precondition(
            "UI_TEST_HOOK_COVERAGE",
            incomplete_metric,
            expected_manifest_sha256="a" * 64,
        )

    root = tmp_path / "qaudit-precondition-repo"
    root.mkdir()
    manager = QVersionManager(root)
    with pytest.raises(RuntimeError, match="complete current QAUDITS precondition"):
        manager.record_lifecycle_stage(
            "qaudit-precondition",
            "UI_TEST_HOOK_COVERAGE",
            [root],
            details={
                "source_manifest_sha256": "a" * 64,
                "qaudit_precondition": {**precondition, "blockers": ["unmapped feature"]},
            },
            include_inventory=False,
        )


def test_q_version_discovery_scans_each_explicit_root_and_ignores_near_matches(tmp_path):
    primary = tmp_path / "primary"
    secondary = tmp_path / "secondary"
    primary.mkdir()
    secondary.mkdir()
    (primary / "Q.0.0.4").mkdir()
    (secondary / "Q.0.0.9.md").write_text("version\n", encoding="utf-8")
    (secondary / "Q.0.0.100.md.backup").write_text("not a version\n", encoding="utf-8")

    assert QVersionManager(primary).discover([primary, secondary]) == 9


def test_q_version_reservation_persists_integrity_and_metadata(tmp_path):
    manager = QVersionManager(tmp_path)
    assert manager.reserve() == "Q.0.0.1"
    payload = json.loads(manager.reservations.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["reservation_id"]
    assert payload["created_at"].endswith("Z")
    assert payload["integrity_sha256"]
    assert manager.audit()["reservation_integrity_verified"] is True


def test_q_version_discovery_fails_closed_on_corrupt_reservation(tmp_path):
    manager = QVersionManager(tmp_path)
    manager.reservations.parent.mkdir(parents=True)
    manager.reservations.write_text("{invalid", encoding="utf-8")

    with pytest.raises(RuntimeError, match="unreadable"):
        manager.discover()


def test_q_version_discovery_fails_closed_on_integrity_mismatch(tmp_path):
    manager = QVersionManager(tmp_path)
    manager.reserve()
    payload = json.loads(manager.reservations.read_text(encoding="utf-8"))
    payload["reserved"] = 7
    manager.reservations.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RuntimeError, match="does not match"):
        manager.discover()


def test_q_version_reservation_lock_is_exclusive_and_preserved(tmp_path):
    manager = QVersionManager(tmp_path)
    manager.reservations.parent.mkdir(parents=True)
    lock = manager.reservations.with_suffix(".lock")
    lock.write_text("active reservation", encoding="utf-8")

    with pytest.raises(RuntimeError, match="busy"):
        manager.reserve()
    assert lock.read_text(encoding="utf-8") == "active reservation"


def test_q_version_pair_verification_reports_per_root_metrics(tmp_path):
    roots = [tmp_path / "alpha", tmp_path / "qmoi"]
    for root in roots:
        (root / "Q.0.0.2").mkdir(parents=True)
        (root / "Q.0.0.2" / "README.md").write_text("# Version\n", encoding="utf-8")
        (root / "Q.0.0.2.md").write_text("# Metrics\n", encoding="utf-8")

    result = QVersionManager(tmp_path / "unrelated").verify_pair("Q.0.0.2", roots)
    assert result["verified"] is True
    assert set(result["repositories"]) == {str(root.resolve()) for root in roots}
    assert result["repositories"][str(roots[0].resolve())]["directory_metrics"]["file_count"] == 1
    assert QVersionManager.verify_pair("Q.0.0.2", roots)["verified"] is True


def test_q_version_tree_inventory_records_every_file_hash_and_directory(tmp_path):
    (tmp_path / "src" / "nested").mkdir(parents=True)
    source = tmp_path / "src" / "nested" / "app.py"
    source.write_text("print('metrics')\n", encoding="utf-8")

    report = QVersionManager.inventory_repository(tmp_path)
    record = next(item for item in report["files"] if item["path"] == "src/nested/app.py")
    assert report["status"] == "READY"
    assert report["file_count"] == 1
    assert report["directory_count"] == 2
    assert report["total_bytes"] == source.stat().st_size
    assert record["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()


def test_q_version_final_metrics_require_remote_terminal_evidence(tmp_path):
    first = make_git_repo(tmp_path, "alpha", with_instructions=True)
    second = make_git_repo(tmp_path, "qmoi", with_instructions=True)
    manager = QVersionManager(first)

    with pytest.raises(RuntimeError, match="remote completion"):
        manager.write_final_metrics("Q.0.0.3", [first, second], {
            "status": "SUCCESS",
            "instruction_inventories": q_version_instruction_evidence([first, second]),
            "autonomous_completion": q_version_autonomous_completion(),
            "production_readiness": q_version_production_readiness(),
        })
    assert not (first / "Q.0.0.3").exists()


def test_q_version_final_metrics_require_dual_instruction_and_completion_evidence(tmp_path):
    first = make_git_repo(tmp_path, "alpha")
    second = make_git_repo(tmp_path, "qmoi")
    manager = QVersionManager(first)

    with pytest.raises(RuntimeError, match="instruction inventories"):
        manager.write_final_metrics(
            "Q.0.0.3",
            [first, second],
            {"status": "SUCCESS", "remote_verified": True},
        )
    assert not (first / "Q.0.0.3").exists()

def test_q_version_final_metrics_reject_tampered_instruction_hashes(tmp_path):
    first = make_git_repo(tmp_path, "alpha", with_instructions=True)
    second = make_git_repo(tmp_path, "qmoi", with_instructions=True)
    inventories = q_version_instruction_evidence([first, second])
    inventories[str(first.resolve())]["files"][0]["sha256"] = "0" * 64

    with pytest.raises(RuntimeError, match="Instruction inventory is incomplete or unsafe"):
        QVersionManager.verify_instruction_inventory(first, inventories[str(first.resolve())])
    assert not (first / "Q.0.0.3").exists()


def test_q_version_instruction_inventory_rejects_missing_required_sources(tmp_path):
    root = make_git_repo(tmp_path, "alpha", with_instructions=False)
    inventory = {
        "status": "PASS",
        "files_discovered": 0,
        "files_read": 0,
        "unreadable_or_invalid": [],
        "source_contents_recorded": False,
        "files": [],
    }

    with pytest.raises(RuntimeError, match="Instruction inventory is incomplete or unsafe"):
        QVersionManager.verify_instruction_inventory(root, inventory)


def test_q_version_instruction_inventory_rejects_symlink_instructions(tmp_path):
    root = make_git_repo(tmp_path, "alpha", with_instructions=True)
    inventory = audit_instruction_files(root)
    source = root / "AGENTS.md"
    (root / ".github" / "instructions" / "linked.instructions.md").symlink_to(source)

    with pytest.raises(RuntimeError, match="Instruction inventory is incomplete or unsafe"):
        QVersionManager.verify_instruction_inventory(root, inventory)


def test_q_version_instruction_inventory_rejects_symlinked_github_directory(tmp_path):
    root = make_git_repo(tmp_path, "alpha", with_instructions=True)
    inventory = audit_instruction_files(root)
    github_root = root / ".github"
    real_github_root = root / ".github-real"
    github_root.rename(real_github_root)
    github_root.symlink_to(real_github_root, target_is_directory=True)

    with pytest.raises(RuntimeError, match="Instruction inventory is incomplete or unsafe"):
        QVersionManager.verify_instruction_inventory(root, inventory)


@pytest.mark.parametrize(
    ("content", "reported_scope"),
    [
        ("", "repository-wide"),
        ("---\napplyTo: src/**\n", "src/**"),
        ("---\napplyTo: src/**\n---\n# Scoped rule\n", "repository-wide"),
    ],
)
def test_q_version_instruction_inventory_rejects_invalid_content_and_scope(
    tmp_path,
    content,
    reported_scope,
):
    root = make_git_repo(tmp_path, "alpha", with_instructions=True)
    inventory = audit_instruction_files(root)
    instruction = next(item for item in inventory["files"] if item["path"] == "AGENTS.md")
    source = root / instruction["path"]
    source.write_text(content, encoding="utf-8")
    instruction["bytes"] = source.stat().st_size
    instruction["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    instruction["apply_to"] = reported_scope

    with pytest.raises(RuntimeError, match="Instruction inventory is incomplete or unsafe"):
        QVersionManager.verify_instruction_inventory(root, inventory)


def test_q_version_instruction_inventory_rejects_embedded_policy_text(tmp_path):
    root = make_git_repo(tmp_path, "alpha", with_instructions=True)
    inventory = q_version_instruction_evidence([root])[str(root.resolve())]
    inventory["files"][0]["instruction_text"] = "private policy content"

    with pytest.raises(RuntimeError, match="Instruction inventory is incomplete or unsafe"):
        QVersionManager.verify_instruction_inventory(root, inventory)


def test_q_version_final_metrics_write_exact_sha_manifests_for_both_repositories(tmp_path):
    roots = [
        make_git_repo(tmp_path, "alpha", with_instructions=True),
        make_git_repo(tmp_path, "qmoi", with_instructions=True),
    ]
    manager = QVersionManager(roots[0])
    execution_id = "qversion-final-success"
    record_successful_q_lifecycle(manager, roots, execution_id)
    repository_evidence = {}
    for root, repository in zip(
        roots,
        ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"),
    ):
        sha = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        tree_sha = git_tree_sha(root, sha)
        repository_evidence[str(root.resolve())] = {
            **terminal_remote_sha_binding(repository, sha, "run-final-123"),
            "remote_tree_sha": tree_sha,
            "workflow_tree_sha": tree_sha,
            "final_sha": sha,
            "checks_passed": True,
        }
    evidence = {
        "status": "SUCCESS",
        "remote_verified": True,
        "workflow_conclusion": "success",
        "workflow_run_id": "12345",
        "live_github_verifier": q_version_live_github_verifier(
            next(iter(repository_evidence.values()))["final_sha"]
        ),
        "lifecycle_execution_id": execution_id,
        "correlation_id": "qversion-test-1",
        "instruction_inventories": q_version_instruction_evidence(roots),
        "autonomous_completion": q_version_autonomous_completion(),
        "repository_surface_audit": q_version_repository_surface_audit(
            [item["final_sha"] for item in repository_evidence.values()],
            [item["remote_tree_sha"] for item in repository_evidence.values()],
        ),
        "ollama_reference_audit": q_version_ollama_reference_audit(
            [item["final_sha"] for item in repository_evidence.values()],
            [item["remote_tree_sha"] for item in repository_evidence.values()],
        ),
        "ui_test_hook_coverage": ui_test_hook_coverage_evidence(
            [item["final_sha"] for item in repository_evidence.values()],
            [item["remote_tree_sha"] for item in repository_evidence.values()],
        ),
        "production_readiness": q_version_production_readiness(),
        "qmoi_restore_point": q_version_qmoi_restore_point_evidence(
            roots,
            [item["final_sha"] for item in repository_evidence.values()],
            "run-qmoi-restore",
        ),
        "repositories": repository_evidence,
    }

    completion = q_version_autonomous_completion()
    mismatched_completion = {
        "status": completion["status"],
        "execution_id": "another-execution",
        "gates": completion["gates"],
        "pending_action_count": 0,
    }
    completion_manifest = "a" * 64
    completion_qaudit = {
        "source_manifest_sha256": completion_manifest,
        "qaudit_precondition": qaudit_precondition(
            "AUTONOMOUS_COMPLETION",
            completion_manifest,
        ),
    }
    manager.record_lifecycle_stage(
        execution_id,
        "AUTONOMOUS_COMPLETION",
        roots,
        status="PASS",
        details={**mismatched_completion, **completion_qaudit},
        include_inventory=False,
    )
    with pytest.raises(RuntimeError, match="autonomous-completion record does not match"):
        manager.write_final_metrics("Q.0.0.3", roots, evidence)
    manager.record_lifecycle_stage(
        execution_id,
        "AUTONOMOUS_COMPLETION",
        roots,
        status="PASS",
        details={
            **mismatched_completion,
            "execution_id": completion["execution_id"],
            **completion_qaudit,
        },
        include_inventory=False,
    )

    instruction_details = {
        str(root.resolve()): {
            "status": "PASS",
            "files_discovered": inventory["files_discovered"],
            "files_read": inventory["files_read"],
            "unreadable_or_invalid": [],
            "source_contents_recorded": False,
            "files": inventory["files"],
        }
        for root in roots
        for inventory in [audit_instruction_files(root)]
    }
    inconsistent_stages = [
        (
            "INSTRUCTION_INVENTORY",
            {"repositories": {**instruction_details, str(roots[0].resolve()): {"status": "PASS"}}},
            instruction_details,
                "instruction lifecycle evidence does not match final inventories",
        ),
        (
            "MARKDOWN_SOURCE_INDEX",
            {"index_complete": False},
            {"index_complete": True},
            "Markdown-source-index lifecycle",
        ),
        (
            "UI_TEST_HOOK_COVERAGE",
            {"status": "PASS", "coverage_verified": False},
            {
                "status": "PASS",
                "coverage_verified": True,
                "feature_count": 2,
                "test_mapped_feature_count": 2,
                "hook_applicability_reviewed_count": 2,
                "unmapped_feature_count": 0,
                "unreviewed_hook_applicability_count": 0,
                "unmapped_event_hook_count": 0,
            },
            "UI test and hook lifecycle",
        ),
        (
            "PRODUCTION_READINESS",
            {"status": "NEEDS_REVIEW", "coverage_complete": False},
            {
                "status": "CLEAR",
                "coverage_complete": True,
                "candidate_count": 0,
                "unreadable_files": [],
                "oversized_files_not_read": 0,
            },
            "clear production-readiness lifecycle",
        ),
    ]
    lifecycle_ledger = roots[0] / "ollamatracks" / "q_versions" / execution_id / "lifecycle.jsonl"
    for stage, invalid_details, _valid_details, error_text in inconsistent_stages:
        lifecycle_ledger.unlink()
        record_successful_q_lifecycle(
            manager,
            roots,
            execution_id,
            details_overrides={stage: invalid_details},
        )
        with pytest.raises(RuntimeError, match=error_text):
            manager.write_final_metrics("Q.0.0.3", roots, evidence)
    lifecycle_ledger.unlink()
    record_successful_q_lifecycle(manager, roots, execution_id)

    ollama_reference_audit = evidence.pop("ollama_reference_audit")
    with pytest.raises(RuntimeError, match="complete dual-repository Ollama history evidence"):
        manager.write_final_metrics("Q.0.0.3", roots, evidence)
    evidence["ollama_reference_audit"] = ollama_reference_audit
    ui_coverage = evidence.pop("ui_test_hook_coverage")
    with pytest.raises(RuntimeError, match="complete styles/universals test and hook evidence"):
        manager.write_final_metrics("Q.0.0.3", roots, evidence)
    evidence["ui_test_hook_coverage"] = ui_coverage
    surface_audit = evidence.pop("repository_surface_audit")
    with pytest.raises(RuntimeError, match="complete dual-repository surface-audit evidence"):
        manager.write_final_metrics("Q.0.0.3", roots, evidence)
    evidence["repository_surface_audit"] = surface_audit
    restore_point = evidence.pop("qmoi_restore_point")
    with pytest.raises(RuntimeError, match="terminal exact-SHA qmoi restore-point evidence"):
        manager.write_final_metrics("Q.0.0.3", roots, evidence)
    evidence["qmoi_restore_point"] = restore_point

    repository_key = str(roots[0].resolve())
    missing_master = restore_point["repositories"][repository_key].pop("master_sha")
    with pytest.raises(RuntimeError, match="qmoi restore-point evidence is incomplete"):
        manager.write_final_metrics("Q.0.0.3", roots, evidence)
    restore_point["repositories"][repository_key]["master_sha"] = missing_master

    result = manager.write_final_metrics("Q.0.0.3", roots, evidence)

    assert result["status"] == "PREPARED_PENDING_REMOTE_VERIFICATION"
    publication_evidence = {}
    for root, repository in zip(
        roots,
        ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"),
    ):
        metrics_path = root / "Q.0.0.3" / "REPOSITORY_METRICS.json"
        document_path = root / "Q.0.0.3.md"
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        assert metrics["source_sha"] == repository_evidence[str(root.resolve())]["final_sha"]
        assert metrics["metrics"]["file_count"] >= 1
        assert metrics["instruction_inventory"]["files_read"] == 2
        assert metrics["autonomous_completion"]["next_actions"] == []
        assert metrics["ollama_reference_audit"]["coverage_complete"] is True
        assert metrics["ui_test_hook_coverage"]["coverage_verified"] is True
        assert metrics["repository_surface_audit"]["coverage_complete"] is True
        assert metrics["production_readiness"]["candidate_count"] == 0
        assert document_path.is_file()
        assert "Directories inventoried:" in document_path.read_text(encoding="utf-8")
        paths_to_add = ["Q.0.0.3", "Q.0.0.3.md"]
        if root == roots[0]:
            paths_to_add.append(f"ollamatracks/q_versions/{execution_id}")
        subprocess.run(["git", "-C", str(root), "add", *paths_to_add], check=True)
        subprocess.run(
            ["git", "-C", str(root), "commit", "-m", "add Q-version metrics"],
            check=True,
            capture_output=True,
            text=True,
        )
        published_sha = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        published_tree_sha = subprocess.run(
            ["git", "-C", str(root), "rev-parse", f"{published_sha}^{{tree}}"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        publication_evidence[str(root.resolve())] = {
            **terminal_remote_sha_binding(repository, published_sha, "run-final-456"),
            "remote_tree_sha": published_tree_sha,
            "workflow_tree_sha": published_tree_sha,
            "final_sha": published_sha,
            "prepared_source_sha": metrics["source_sha"],
            "checks_passed": True,
            "metrics_sha256": hashlib.sha256(metrics_path.read_bytes()).hexdigest(),
            "version_document_sha256": hashlib.sha256(document_path.read_bytes()).hexdigest(),
        }

    published_restore_point = q_version_qmoi_restore_point_evidence(
        roots,
        [item["final_sha"] for item in publication_evidence.values()],
        "run-final-456",
    )

    published = manager.verify_final_publication(
        "Q.0.0.3",
        roots,
        {
            "status": "SUCCESS",
            "remote_verified": True,
            "workflow_conclusion": "success",
            "workflow_run_id": "run-final-456",
            "correlation_id": "qversion-publish-test",
            "repositories": publication_evidence,
            "qmoi_restore_point": published_restore_point,
        },
    )
    assert published["status"] == "SUCCESS"

    divergent_restore = {
        **published_restore_point,
        "repositories": {
            key: dict(value)
            for key, value in published_restore_point["repositories"].items()
        },
    }
    divergent_restore["repositories"][str(roots[0].resolve())]["qmoi_sha"] = "0" * 40
    with pytest.raises(RuntimeError, match="Published qmoi restore point does not match final repository SHA"):
        manager.verify_final_publication(
            "Q.0.0.3",
            roots,
            {
                "status": "SUCCESS",
                "remote_verified": True,
                "workflow_conclusion": "success",
                "workflow_run_id": "run-final-456",
                "correlation_id": "qversion-publish-divergent-qmoi",
                "repositories": publication_evidence,
                "qmoi_restore_point": divergent_restore,
            },
        )

    tampered_publication = {
        str(root.resolve()): dict(item)
        for root, item in ((Path(path), value) for path, value in publication_evidence.items())
    }
    first_root_key = str(roots[0].resolve())
    tampered_publication[first_root_key]["metrics_sha256"] = "0" * 64
    with pytest.raises(RuntimeError, match="artifact hashes do not match"):
        manager.verify_final_publication(
            "Q.0.0.3",
            roots,
            {
                "status": "SUCCESS",
                "remote_verified": True,
                "workflow_conclusion": "success",
                "workflow_run_id": "run-final-456",
                "correlation_id": "qversion-publish-tampered",
                "repositories": tampered_publication,
                "qmoi_restore_point": published_restore_point,
            },
        )


def test_q_version_publication_rejects_nonterminal_workflow_result(tmp_path):
    roots = [tmp_path / "alpha", tmp_path / "qmoi"]
    for root in roots:
        root.mkdir()
    manager = QVersionManager(roots[0])

    with pytest.raises(RuntimeError, match="independently verified remote success"):
        manager.verify_final_publication(
            "Q.0.0.1",
            roots,
            {
                "status": "QUEUED",
                "remote_verified": False,
                "workflow_conclusion": "in_progress",
                "workflow_run_id": "run-pending",
                "correlation_id": "qversion-publish-pending",
            },
        )


def test_q_version_publication_requires_exact_dual_repository_evidence(tmp_path):
    roots = [tmp_path / "alpha", tmp_path / "qmoi"]
    for root in roots:
        root.mkdir()
    manager = QVersionManager(roots[0])
    evidence = {
        "status": "SUCCESS",
        "remote_verified": True,
        "workflow_conclusion": "success",
        "workflow_run_id": "run-final",
        "correlation_id": "qversion-publish-dual",
        "repositories": {str(roots[0].resolve()): {}},
    }

    with pytest.raises(RuntimeError, match="both repository records"):
        manager.verify_final_publication("Q.0.0.1", roots[:1], evidence)
    with pytest.raises(RuntimeError, match="exactly match the requested repositories"):
        manager.verify_final_publication("Q.0.0.1", roots, evidence)


def test_q_version_final_metrics_reject_dirty_or_mismatched_repository(tmp_path):
    roots = [
        make_git_repo(tmp_path, "alpha", with_instructions=True),
        make_git_repo(tmp_path, "qmoi", with_instructions=True),
    ]
    manager = QVersionManager(roots[0])
    execution_id = "qversion-final-dirty"
    record_successful_q_lifecycle(manager, roots, execution_id)
    repository_shas = [
        subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        for root in roots
    ]
    (roots[0] / "uncommitted.txt").write_text("not final\n", encoding="utf-8")
    evidence = {
        "status": "SUCCESS",
        "remote_verified": True,
        "workflow_conclusion": "success",
        "workflow_run_id": "12345",
        "live_github_verifier": q_version_live_github_verifier(repository_shas[0]),
        "lifecycle_execution_id": execution_id,
        "correlation_id": "qversion-test-2",
        "instruction_inventories": q_version_instruction_evidence(roots),
        "autonomous_completion": q_version_autonomous_completion(),
        "repository_surface_audit": q_version_repository_surface_audit(
            repository_shas,
            [git_tree_sha(root, sha) for root, sha in zip(roots, repository_shas)],
        ),
        "ollama_reference_audit": q_version_ollama_reference_audit(
            repository_shas,
            [git_tree_sha(root, sha) for root, sha in zip(roots, repository_shas)],
        ),
        "ui_test_hook_coverage": ui_test_hook_coverage_evidence(
            repository_shas,
            [git_tree_sha(root, sha) for root, sha in zip(roots, repository_shas)],
        ),
        "production_readiness": q_version_production_readiness(),
        "qmoi_restore_point": q_version_qmoi_restore_point_evidence(roots, repository_shas, "run-qmoi-restore"),
        "repositories": {
            str(root.resolve()): {
                **terminal_remote_sha_binding(repository, sha, "run-final-dirty"),
                "remote_tree_sha": subprocess.run(
                    ["git", "-C", str(root), "rev-parse", f"{sha}^{{tree}}"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip(),
                "workflow_tree_sha": subprocess.run(
                    ["git", "-C", str(root), "rev-parse", f"{sha}^{{tree}}"],
                    check=True,
                    capture_output=True,
                    text=True,
                ).stdout.strip(),
                "final_sha": sha,
                "checks_passed": True,
            }
            for root, sha, repository in zip(
                roots,
                repository_shas,
                ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"),
            )
        },
    }

    with pytest.raises(RuntimeError, match="clean verified remote SHA"):
        manager.write_final_metrics("Q.0.0.4", roots, evidence)
    assert not (roots[0] / "Q.0.0.4").exists()


def test_live_activity_detects_fresh_and_stale_states(tmp_path):
    activity = LiveActivity(tmp_path, "e1")
    event = activity.publish("DISCOVERY", "RUNNING", "DISCOVERY", "started")
    assert event["execution_id"] == "e1"
    assert activity.freshness()["fresh"] is True
    payload = json.loads((tmp_path / "ollamatracks" / "current_state.json").read_text(encoding="utf-8"))
    assert payload["sequence"] == 1


def test_control_plane_bootstrap_creates_only_runtime_scaffolding(tmp_path):
    root = make_root(tmp_path)
    report = ControlPlaneSupervisor(root).bootstrap_runtime()
    assert report.status == "BLOCKED"
    assert report.remote_only is True
    assert all((root / directory).is_dir() for directory in (
        "ollamatracks/checkpoints",
        "ollamatracks/executions",
        "ollamatracks/requests",
    ))
    assert not (root / "scripts" / "generated_control_plane.py").exists()
    assert (root / "ollamatracks" / "control_plane_state.json").is_file()


def test_control_plane_audit_is_ready_for_complete_repository():
    root = Path(__file__).resolve().parents[1]
    report = ControlPlaneSupervisor(root).audit()
    assert report.status == "READY"
    assert report.remote_only is True
    assert not report.blockers


def test_repository_contract_audit_records_inventory_and_source_manifest(tmp_path):
    for name in ("API.md", "ENDPOINTS.md", "ROUTES.md", "ALLPORTS.md"):
        (tmp_path / name).write_text(f"# {name}\n", encoding="utf-8")
    source = tmp_path / "Alpha-Q-ai-2025" / "qcity"
    source.mkdir(parents=True)
    (source / "app.tsx").write_text("export const app = true;\n", encoding="utf-8")

    report = audit_repository_contract(tmp_path)

    assert report["status"] == "READY"
    assert report["remote_only"] is True
    assert report["parity_proven"] is False
    assert report["inventory_files"]["API.md"]["sha256"]
    assert report["source_roots"]["Alpha-Q-ai-2025"]["source_file_count"] == 1
    assert report["source_roots"]["Alpha-Q-ai-2025"]["candidate_apps"] == ["qcity"]
    assert "remote_state" in report
    assert report["remote_state"]["reachable"] is False


def test_repository_contract_audit_fail_closes_missing_surfaces(tmp_path):
    report = audit_repository_contract(tmp_path)

    assert report["status"] == "BLOCKED"
    assert len(report["missing_inventory_files"]) == 4
    assert report["parity_proven"] is False
    assert report["blockers"]
