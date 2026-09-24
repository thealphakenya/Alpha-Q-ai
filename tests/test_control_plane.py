import json
from pathlib import Path

from scripts.autonomous_completion_engine import AutonomousCompletionEngine, REQUIRED_GATES
from scripts.checkpoint_manager import CheckpointManager
from scripts.execution_lock import ExecutionLock
from scripts.live_activity_events import LiveActivity
from scripts.q_version_manager import QVersionManager
from scripts.sync_contract import build_sync_contract
from scripts.control_plane_supervisor import ControlPlaneSupervisor
from scripts.repository_contract_audit import audit_repository_contract


def make_root(tmp_path: Path) -> Path:
    (tmp_path / "QMOI_Ollama_Autonomous_Production_Completion_Master_Plan.md").write_text("## 1. One\n## 2. Two\n", encoding="utf-8")
    (tmp_path / "ollama_master_topic_index.txt").write_text("1. One\n2. Two\n", encoding="utf-8")
    return tmp_path


def test_completion_is_fail_closed_and_writes_topic_metrics(tmp_path):
    root = make_root(tmp_path)
    result = AutonomousCompletionEngine(root, "execution-1").evaluate()
    assert result.status == "BLOCKED_REQUIRES_HUMAN"
    assert result.stage == "DISCOVERY"
    metrics = json.loads((root / "ollamatracks" / "topic_metrics.json").read_text(encoding="utf-8"))
    assert metrics["master_plan_topics"] == 2
    assert metrics["fully_completed"] == 0


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
