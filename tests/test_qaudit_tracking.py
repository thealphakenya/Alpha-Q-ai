import json
from pathlib import Path

from scripts.qaudit_tracking import (
    build_tracking_inventory,
    render_qmoi_tracks_markdown,
    render_tracking_markdown,
)


def test_tracking_inventory_calculates_coverage_and_keeps_metric_values_private(
    tmp_path: Path,
) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "qmoi_health_monitor.py").write_text(
        "def read_health():\n    return {'status': 'unknown'}\n",
        encoding="utf-8",
    )
    tracks = tmp_path / "TRACKS.md"
    tracks.write_text("# Existing tracks\n", encoding="utf-8")
    metric_dir = tmp_path / "ollamatracks"
    metric_dir.mkdir()
    metric_path = metric_dir / "qaudit_metrics.json"
    metric_path.write_text(
        json.dumps(
            {
                "metrics": {"files_scanned": 10},
                "email": "private@example.test",
                "token": "never-copy-this-token",
            }
        ),
        encoding="utf-8",
    )
    historical = tmp_path / "Alpha-Q-ai-2025" / "TRACKS.md"
    historical.parent.mkdir()
    historical.write_text("# Historical tracker\n", encoding="utf-8")

    inventory = build_tracking_inventory(
        tmp_path,
        feature_registry={
            "web": {
                "qcity": ["Public files", "Private files"],
            }
        },
        master_ui_features=["System health overview", "Incident controls"],
        access_modes={
            "public_guest": (),
            "authenticated_user": (),
            "master_operator": (),
        },
    )

    assert inventory["status"] == "NEEDS_REVIEW"
    assert inventory["source_scope"].startswith("materialized_nonignored")
    assert inventory["metrics"]["feature_requirement_count"] == 2
    assert inventory["metrics"]["master_ui_requirement_count"] == 2
    assert inventory["metrics"]["monitoring_requirement_count"] == 4
    assert inventory["metrics"]["monitoring_source_candidate_count"] == 1
    assert inventory["metrics"]["metric_artifact_reference_count"] == 1
    assert inventory["metrics"]["tracking_document_reference_count"] == 2
    assert inventory["metrics"]["monitoring_mappings_verified_count"] == 0
    assert inventory["metrics"]["feature_monitoring_mapping_rate_percent"] == 0.0
    assert inventory["metrics"]["source_hash_coverage_percent"] == 100.0
    assert inventory["live_metric_values_observed"] is False
    assert inventory["live_metric_provider_connections_verified"] == 0
    assert inventory["feature_requirements"][0]["access_classification"] == "review_required"
    assert inventory["master_ui_requirements"][0]["access_classification"] == "master_operator_contract"

    serialized = json.dumps(inventory)
    assert "private@example.test" not in serialized
    assert "never-copy-this-token" not in serialized
    assert "no live metric endpoint" in " ".join(inventory["blockers"]).lower()
    assert any(
        item["path"] == "Alpha-Q-ai-2025/TRACKS.md"
        and item["scope"] == "snapshot"
        for item in inventory["tracking_document_references"]
    )

    markdown = render_tracking_markdown(inventory)
    assert "public_guest" in markdown
    assert "authenticated_user" in markdown
    assert "master_operator" in markdown
    assert "System health overview" in markdown
    assert "zero currently verified" in markdown
    assert "never-copy-this-token" not in markdown


def test_tracking_inventory_reports_null_rate_for_empty_requirement_denominator(
    tmp_path: Path,
) -> None:
    inventory = build_tracking_inventory(
        tmp_path,
        feature_registry={},
        master_ui_features=[],
        access_modes={},
        source_paths=[],
    )

    assert inventory["metrics"]["monitoring_requirement_count"] == 0
    assert inventory["metrics"]["feature_monitoring_mapping_rate_percent"] is None
    assert inventory["metrics"]["source_hash_coverage_percent"] is None


def test_planned_and_uis_requirements_get_review_actions_without_copying_source_text(
    tmp_path: Path,
) -> None:
    private_source_text = "UIS requirement with sensitive source wording"
    inventory = build_tracking_inventory(
        tmp_path,
        feature_registry={},
        master_ui_features=["Master health panel"],
        access_modes={"master_operator": ()},
        source_paths=[],
        planned_feature_requirements={
            "public_ui": ["Public service status"],
            "future_runtime": ["Quantum provider health"],
        },
        uis_plan={
            "status": "NEEDS_REVIEW",
            "source_path": "QMOIUNIVERSALINTELLIGENCESYSTEM.md",
            "source_sha256": "a" * 64,
            "sections": [{
                "id": "UIS-01",
                "requirements": [{
                    "id": "UIS-01-R01",
                    "source_line": 8,
                    "description": private_source_text,
                }],
            }],
        },
    )

    assert inventory["metrics"]["planned_feature_requirement_count"] == 2
    assert inventory["metrics"]["universal_intelligence_requirement_count"] == 1
    assert inventory["metrics"]["monitoring_requirement_count"] == 4
    assert inventory["metrics"]["monitoring_action_queue_count"] == 4
    assert {item["status"] for item in inventory["monitoring_action_queue"]} == {
        "PENDING_REVIEW"
    }

    serialized = json.dumps(inventory)
    qmoi_tracks = render_qmoi_tracks_markdown(inventory)
    assert private_source_text not in serialized
    assert private_source_text not in qmoi_tracks
    assert "Master health panel" in qmoi_tracks
    assert "public_guest_contract" in qmoi_tracks
    assert "uis.uis-01-r01" in qmoi_tracks


def test_tracker_directory_inventory_bounds_hashing_of_oversized_files(
    tmp_path: Path,
) -> None:
    tracker_dir = tmp_path / "ollamatracks"
    tracker_dir.mkdir()
    large_file = tracker_dir / "large_metrics.json"
    large_file.write_bytes(b"x" * 1_000_001)

    inventory = build_tracking_inventory(
        tmp_path,
        feature_registry={},
        master_ui_features=[],
        access_modes={},
        source_paths=["ollamatracks/large_metrics.json"],
    )

    reference = inventory["tracking_system_source_references"][0]
    assert inventory["metrics"]["tracking_system_file_reference_count"] == 1
    assert reference["status"] == "oversized_not_hashed"
    assert reference["sha256"] is None
    assert reference["metric_values_read"] is False
    assert inventory["metrics"]["source_hash_failure_count"] == 1


def test_ollama_refreshes_alltracks_and_qaudits_without_overwriting_authored_text(
    tmp_path: Path,
) -> None:
    from scripts.ollama_autonomous_agent import OllamaAutonomousAgent

    all_tracks = tmp_path / "ALLTRACKS.md"
    all_tracks.write_text("# Local tracking notes\n\nKeep this paragraph.\n", encoding="utf-8")
    qaudits = tmp_path / "QAUDITS.md"
    qaudits.write_text("# Audit policy\n\nPreserve authored QAUDITS text.\n", encoding="utf-8")
    qmoi_tracks = tmp_path / "QMOITACKS.md"
    qmoi_tracks.write_text("# QMOI tracking notes\n\nKeep QMOI-authored notes.\n", encoding="utf-8")
    canonical_qmoi_tracks = tmp_path / "QMOITRACKS.md"
    canonical_qmoi_tracks.write_text(
        "# Canonical QMOI tracking notes\n\nKeep canonical QMOI notes.\n",
        encoding="utf-8",
    )
    ollama_tracks_dir = tmp_path / "ollamatracks"
    ollama_tracks_dir.mkdir()
    (ollama_tracks_dir / "ALLTRACKS.md").write_text(
        "# Ollama tracker notes\n\nKeep Ollama tracker notes.\n",
        encoding="utf-8",
    )
    (ollama_tracks_dir / "agent_metrics.json").write_text(
        json.dumps({"metric": 4, "token": "ollama-private-token"}),
        encoding="utf-8",
    )
    qmoi_tracks_dir = tmp_path / "QMOItracks"
    qmoi_tracks_dir.mkdir()
    (qmoi_tracks_dir / "QMOITRACKS.md").write_text(
        "# QMOI tracker directory notes\n\nKeep QMOI directory notes.\n",
        encoding="utf-8",
    )
    (qmoi_tracks_dir / "runtime_metrics.json").write_text(
        json.dumps({"metric": 7, "email": "private-qmoi@example.test"}),
        encoding="utf-8",
    )
    (tmp_path / "QMOIUNIVERSALINTELLIGENCESYSTEM.md").write_text(
        "# Universal Intelligence plan\n\n1. Monitoring requirements\n- Include a freshness signal for each planned capability.\n",
        encoding="utf-8",
    )

    result = OllamaAutonomousAgent(base_path=tmp_path).refresh_test_hook_coverage_documents()

    inventory_path = tmp_path / "ollamatracks" / "alltracks_monitoring_inventory.json"
    qmoi_inventory_path = tmp_path / "QMOItracks" / "qmoitracks_monitoring_inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    refreshed_all_tracks = all_tracks.read_text(encoding="utf-8")
    refreshed_qaudits = qaudits.read_text(encoding="utf-8")
    refreshed_qmoi_tracks = qmoi_tracks.read_text(encoding="utf-8")
    refreshed_canonical_qmoi_tracks = canonical_qmoi_tracks.read_text(encoding="utf-8")
    refreshed_ollama_dir_tracks = (ollama_tracks_dir / "ALLTRACKS.md").read_text(encoding="utf-8")
    refreshed_qmoi_dir_tracks = (qmoi_tracks_dir / "QMOITRACKS.md").read_text(encoding="utf-8")

    assert result["tracking_inventory_path"] == inventory_path
    assert result["qmoi_tracking_inventory_path"] == qmoi_inventory_path
    assert result["tracking_inventory_path_sha256"]
    assert inventory["metrics"]["feature_requirement_count"] > 0
    assert inventory["metrics"]["master_ui_requirement_count"] > 0
    assert inventory["metrics"]["planned_feature_requirement_count"] > 0
    assert inventory["metrics"]["universal_intelligence_requirement_count"] > 0
    assert inventory["metrics"]["monitoring_action_queue_count"] == inventory["metrics"]["monitoring_requirement_count"]
    assert inventory["tracking_artifacts_by_system"]["ollamatracks"]["artifact_reference_count"] > 0
    assert inventory["tracking_artifacts_by_system"]["qmoitracks"]["artifact_reference_count"] > 0
    assert inventory["tracking_artifacts_by_system"]["ollamatracks"]["file_reference_count"] > 0
    assert inventory["tracking_artifacts_by_system"]["qmoitracks"]["file_reference_count"] > 0
    assert "ollama-private-token" not in json.dumps(inventory)
    assert "private-qmoi@example.test" not in json.dumps(inventory)
    assert json.loads(qmoi_inventory_path.read_text(encoding="utf-8")) == inventory
    assert inventory["coverage_verified"] is False
    assert "Keep this paragraph." in refreshed_all_tracks
    assert "alltracks-monitoring-inventory" in refreshed_all_tracks
    assert "Preserve authored QAUDITS text." in refreshed_qaudits
    assert "tracking-and-live-metric-inventory" in refreshed_qaudits
    assert "Keep QMOI-authored notes." in refreshed_qmoi_tracks
    assert "qmoitacks-monitoring-inventory" in refreshed_qmoi_tracks
    assert "master monitoring access" in refreshed_qmoi_tracks.lower()
    assert "Keep canonical QMOI notes." in refreshed_canonical_qmoi_tracks
    assert "qmoitracks-monitoring-inventory" in refreshed_canonical_qmoi_tracks
    assert "Keep Ollama tracker notes." in refreshed_ollama_dir_tracks
    assert "ollamatracks-monitoring-inventory" in refreshed_ollama_dir_tracks
    assert "Keep QMOI directory notes." in refreshed_qmoi_dir_tracks
    assert "qmoitracks-monitoring-inventory" in refreshed_qmoi_dir_tracks
    assert "ollama-private-token" not in refreshed_all_tracks
    assert "private-qmoi@example.test" not in refreshed_qmoi_tracks
    assert result["documents"]["ALLTRACKS.md"] == all_tracks
    assert result["documents"]["QMOITACKS.md"] == qmoi_tracks
    assert result["documents"]["QMOITRACKS.md"] == canonical_qmoi_tracks
    assert result["documents"]["ollamatracks/ALLTRACKS.md"] == ollama_tracks_dir / "ALLTRACKS.md"
    assert result["documents"]["QMOItracks/QMOITRACKS.md"] == qmoi_tracks_dir / "QMOITRACKS.md"
    assert result["documents"]["QAUDITS.md"] == qaudits
