from __future__ import annotations

import hashlib
import json

from scripts.qaudits_evolution_planner import (
    QVIRTUAL_LAB_DOMAIN_MARKERS,
    build_evolution_plan,
    build_qvirtual_labs_plan,
)


def test_build_evolution_plan_discovers_contracts_and_is_deterministic(tmp_path):
    contract_files = {
        "AUTODEV.md": "# Autodev\n\nremote-continuity-and-failover\n",
        "MODELEVUTIONO.md": "# Model evolution\n\nmodel evolution\n",
        "Qvillageevolutions.md": "# QVillage evolution\n\nmodel and memory lifecycle\n",
        "INTERNALRESEARCH.md": "# Internal research\n\nrepository surface audit\n",
        "EXTERNALRESEARCH.md": "# External research\n\nofficial guidance\n",
        "QSEED.md": "# QSeed\n\nseed lineage\n",
        "QVERSIONMANAGER.md": "# Q version manager\n\nQ_VERSION_FINALIZATION\n",
        "SYNC.md": "# Sync\n\nBranch roles\n",
        "QAUDITS.md": "# QAUDITS\n\nLocal plan\n",
        "ALLFEATURES.md": "# Features\n\nCapability registry\n",
        "ALLTESTSAUTOTESTS.md": "# Tests\n\nFeature tests\n",
        "ALLVALIDATIONS.md": "# Validation\n\nValidation gates\n",
        "remotecompletion.md": "# Remote completion\n\nExact SHA evidence\n",
    }
    for name, content in contract_files.items():
        (tmp_path / name).write_text(content, encoding="utf-8")

    first = build_evolution_plan(tmp_path, source_manifest_sha256="manifest-a")
    second = build_evolution_plan(tmp_path, source_manifest_sha256="manifest-a")

    assert first == second
    assert first["status"] == "PLANNED"
    assert first["remote_verification_complete"] is False
    assert first["source_manifest_sha256"] == "manifest-a"
    assert first["plan_sha256"] == hashlib.sha256(
        json.dumps(first["stages"], sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    domains = {stage["domain"] for stage in first["stages"]}
    assert domains == {
        "autodev",
        "model_evolution",
        "qvillage_evolution",
        "qvirtual_labs",
        "internal_research",
        "external_research",
        "q_seed",
        "q_version",
        "instruction_inventory",
        "repository_surface_audit",
        "markdown_refresh",
        "production_gate",
        "validation",
        "remote_verification",
        "evolutiono_pre_retirement",
        "qmoi_capability_parity",
        "qreplaceo_archive",
        "evolutiono_clean_branch_audit",
        "evolutiono_ofca_metrics",
    }
    assert all(stage["source_sha256"] for stage in first["stages"])
    assert all(stage["state"] == "PLANNED" for stage in first["stages"])
    assert all(stage["metrics"]["source_manifest_sha256"] == "manifest-a" for stage in first["stages"])
    assert first["qstats"]["evolutiono_transition_stage_count"] == 5
    assert first["qstats"]["evolutiono_transition_completed_stage_count"] == 0
    assert first["evolutiono_transition"]["remote_verified"] is False
    assert first["evolutiono_transition"]["automatic_mutation_enabled"] is False
    ofca_stage = next(stage for stage in first["stages"] if stage["domain"] == "evolutiono_ofca_metrics")
    assert ofca_stage["target_documents"] == ["OFCA.md"]


def test_qvirtual_labs_plan_tracks_source_and_separates_simulated_from_physical(tmp_path):
    start_marker, end_marker = QVIRTUAL_LAB_DOMAIN_MARKERS
    (tmp_path / "QVIRTUALLABS.md").write_text(
        f"# Labs\n\n{start_marker}\n1. **Finite-element analysis** — candidate.\n"
        f"2. **Robotics** — candidate.\n{end_marker}\n",
        encoding="utf-8",
    )
    historical = tmp_path / "qmoi-enhanced-history-14" / "QVIRTUALLABS.md"
    historical.parent.mkdir()
    historical.write_text("# Historical snapshot\n", encoding="utf-8")

    first = build_qvirtual_labs_plan(tmp_path, source_manifest_sha256="manifest-qv")
    second = build_qvirtual_labs_plan(tmp_path, source_manifest_sha256="manifest-qv")

    assert first == second
    assert first["status"] == "BLOCKED_SOURCE_RECONCILIATION"
    assert first["metrics"]["source_requirement_count"] is None
    assert first["metrics"]["starter_domain_candidate_count"] == 2
    assert first["metrics"]["cross_cutting_gate_candidate_count"] == 19
    assert first["metrics"]["starter_plan_requirement_count"] == 21
    assert first["metrics"]["simulation_runs_verified_count"] == 0
    assert first["metrics"]["benchmark_validations_verified_count"] == 0
    assert first["metrics"]["accuracy_claims_verified_count"] == 0
    assert first["metrics"]["physical_experiment_records_verified_count"] == 0
    assert first["metrics"]["physical_calibration_correlations_verified_count"] == 0
    assert first["metrics"]["official_research_source_count"] == 8
    assert first["metrics"]["official_research_retrieval_time_not_captured_count"] == 8
    assert first["metrics"]["fresh_external_research_observations_count"] in {0, 8}
    assert first["research"]["status"] in {"OBSERVED_DATE_ONLY", "STALE"}
    assert first["recommended_adapter_stack"]["initial_pilot"] == "ngspice circuit reference case"
    assert any(
        candidate["tool"] == "FreeCAD"
        for candidate in first["recommended_adapter_stack"]["tool_candidates"]
    )
    assert first["public_qengineer_probe"]["status"] == "UNKNOWN_NOT_FOUND_OR_PRIVATE"
    assert first["research"]["observations"][0]["source_sha256"]
    assert first["metrics"]["remote_verified"] is False
    assert first["historical_reference"]["scope"] == "historical_snapshot_candidate"
    assert first["historical_reference"]["not_authoritative"] is True
    assert any("QENGINEER.md" in blocker for blocker in first["blockers"])

    (tmp_path / "QENGINEER.md").write_text("# Engineering requirements\n", encoding="utf-8")
    reconciled = build_qvirtual_labs_plan(tmp_path, source_manifest_sha256="manifest-qv")
    assert reconciled["status"] == "NEEDS_REVIEW"
    assert not any("QENGINEER.md" in blocker for blocker in reconciled["blockers"])
