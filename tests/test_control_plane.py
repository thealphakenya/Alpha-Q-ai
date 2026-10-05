import json
import hashlib
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
from scripts.q_version_manager import QVersionManager
from scripts.ollama_research import (
    EXTERNAL_RESEARCH_CONTROLS,
    INTERNAL_RESEARCH_CONTROLS,
    build_internal_research_plan,
    discover_resource_candidates,
    fetch_official_resource,
    record_research_visit,
)
from scripts.ollama_autonomous_agent import sanitize_repo_ollama_mentions
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


def q_version_ollama_reference_audit(shas: list[str]) -> dict[str, object]:
    return {
        "status": "PASS",
        "coverage_complete": True,
        "materialized_scope_complete": True,
        "source_manifest_sha256": "c" * 64,
        "unavailable_sources": [],
        "repositories": {
            name: {
                "terminal_conclusion": "success",
                "remote_verified": True,
                "final_sha": sha,
                "workflow_run_id": "run-ollama-audit",
                "all_refs_enumerated": True,
                "all_pull_requests_included": True,
                "all_intermediate_commit_trees_scanned": True,
                "unavailable_sources": [],
            }
            for name, sha in zip(
                ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"),
                shas,
            )
        },
    }


def ui_test_hook_coverage_evidence(shas: list[str]) -> dict[str, object]:
    return {
        "status": "PASS",
        "coverage_verified": True,
        "source_manifest_sha256": "d" * 64,
        "unavailable_sources": [],
        "repositories": {
            name: {
                "remote_verified": True,
                "terminal_conclusion": "success",
                "final_sha": sha,
                "workflow_run_id": "run-ui-coverage",
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
            for name, sha in zip(
                ("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"),
                shas,
            )
        },
    }


def record_successful_q_lifecycle(manager: QVersionManager, roots: list[Path], execution_id: str) -> None:
    stage_details = {
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
    }
    for stage in QVersionManager.LIFECYCLE_STAGES[:-1]:
        manager.record_lifecycle_stage(
            execution_id,
            stage,
            roots,
            status="PASS",
            details=stage_details.get(stage, {"decision_ledger_complete": True}),
            include_inventory=stage == "PRE_MERGE_INVENTORY",
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
            "ollama_reference_audit": q_version_ollama_reference_audit(["a" * 40, "b" * 40]),
            "ui_test_hook_coverage": ui_test_hook_coverage_evidence(["a" * 40, "b" * 40]),
        },
    )
    current_state = json.loads((root / "ollamatracks" / "current_state.json").read_text(encoding="utf-8"))

    assert first.status == "BLOCKED_REQUIRES_HUMAN"
    assert first_state["status"] == "BLOCKED_REQUIRES_HUMAN"
    assert second.status == "NO_CHANGES_REQUIRED"
    assert second.gates["ollama_reference_audit"] == "PASS"
    assert second.gates["ui_test_hook_coverage"] == "PASS"
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
    assert result.status == "BLOCKED_REQUIRES_HUMAN"


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
            "terminal_conclusion": "success",
            "remote_verified": True,
            "final_sha": "a" * 40 if name.endswith("Alpha-Q-ai") else "b" * 40,
            "workflow_run_id": "run-123",
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
                "ollama_reference_audit": q_version_ollama_reference_audit(
                    [item["final_sha"] for item in repository_evidence.values()]
                ),
                "ui_test_hook_coverage": ui_test_hook_coverage_evidence(
                    [item["final_sha"] for item in repository_evidence.values()]
                ),
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
    for root in roots:
        sha = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        repository_evidence[str(root.resolve())] = {
            "final_sha": sha,
            "terminal_conclusion": "success",
            "checks_passed": True,
            "remote_verified": True,
        }
    evidence = {
        "status": "SUCCESS",
        "remote_verified": True,
        "workflow_conclusion": "success",
        "workflow_run_id": "12345",
        "lifecycle_execution_id": execution_id,
        "correlation_id": "qversion-test-1",
        "instruction_inventories": q_version_instruction_evidence(roots),
        "autonomous_completion": q_version_autonomous_completion(),
        "ollama_reference_audit": q_version_ollama_reference_audit(
            [item["final_sha"] for item in repository_evidence.values()]
        ),
        "ui_test_hook_coverage": ui_test_hook_coverage_evidence(
            [item["final_sha"] for item in repository_evidence.values()]
        ),
        "production_readiness": q_version_production_readiness(),
        "repositories": repository_evidence,
    }

    ollama_reference_audit = evidence.pop("ollama_reference_audit")
    with pytest.raises(RuntimeError, match="complete dual-repository Ollama history evidence"):
        manager.write_final_metrics("Q.0.0.3", roots, evidence)
    evidence["ollama_reference_audit"] = ollama_reference_audit
    ui_coverage = evidence.pop("ui_test_hook_coverage")
    with pytest.raises(RuntimeError, match="complete styles/universals test and hook evidence"):
        manager.write_final_metrics("Q.0.0.3", roots, evidence)
    evidence["ui_test_hook_coverage"] = ui_coverage

    result = manager.write_final_metrics("Q.0.0.3", roots, evidence)

    assert result["status"] == "PREPARED_PENDING_REMOTE_VERIFICATION"
    publication_evidence = {}
    for root in roots:
        metrics_path = root / "Q.0.0.3" / "REPOSITORY_METRICS.json"
        document_path = root / "Q.0.0.3.md"
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        assert metrics["source_sha"] == repository_evidence[str(root.resolve())]["final_sha"]
        assert metrics["metrics"]["file_count"] >= 1
        assert metrics["instruction_inventory"]["files_read"] == 2
        assert metrics["autonomous_completion"]["next_actions"] == []
        assert metrics["ollama_reference_audit"]["coverage_complete"] is True
        assert metrics["ui_test_hook_coverage"]["coverage_verified"] is True
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
        publication_evidence[str(root.resolve())] = {
            "final_sha": published_sha,
            "prepared_source_sha": metrics["source_sha"],
            "terminal_conclusion": "success",
            "checks_passed": True,
            "remote_verified": True,
            "metrics_sha256": hashlib.sha256(metrics_path.read_bytes()).hexdigest(),
            "version_document_sha256": hashlib.sha256(document_path.read_bytes()).hexdigest(),
        }

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
        },
    )
    assert published["status"] == "SUCCESS"


def test_q_version_final_metrics_reject_dirty_or_mismatched_repository(tmp_path):
    roots = [
        make_git_repo(tmp_path, "alpha", with_instructions=True),
        make_git_repo(tmp_path, "qmoi", with_instructions=True),
    ]
    manager = QVersionManager(roots[0])
    execution_id = "qversion-final-dirty"
    record_successful_q_lifecycle(manager, roots, execution_id)
    (roots[0] / "uncommitted.txt").write_text("not final\n", encoding="utf-8")
    evidence = {
        "status": "SUCCESS",
        "remote_verified": True,
        "workflow_conclusion": "success",
        "workflow_run_id": "12345",
        "lifecycle_execution_id": execution_id,
        "correlation_id": "qversion-test-2",
        "instruction_inventories": q_version_instruction_evidence(roots),
        "autonomous_completion": q_version_autonomous_completion(),
        "ollama_reference_audit": q_version_ollama_reference_audit(["a" * 40, "a" * 40]),
        "ui_test_hook_coverage": ui_test_hook_coverage_evidence(["a" * 40, "a" * 40]),
        "production_readiness": q_version_production_readiness(),
        "repositories": {
            str(root.resolve()): {
                "final_sha": "a" * 40,
                "terminal_conclusion": "success",
                "checks_passed": True,
                "remote_verified": True,
            }
            for root in roots
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
