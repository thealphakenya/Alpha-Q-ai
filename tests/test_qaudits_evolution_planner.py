from __future__ import annotations

import hashlib
import json

from scripts.qaudits_evolution_planner import (
    DATASET_COMPARISON_HARD_GATES,
    DATASET_COMPARISON_METRICS,
    DATASET_COMPARISON_EVIDENCE_SCHEMA_VERSION,
    MODEL_COMPARISON_EVIDENCE_SCHEMA_VERSION,
    MODEL_COMPARISON_DIMENSIONS,
    MODEL_COMPARISON_HARD_GATES,
    QVIRTUAL_LAB_DOMAIN_MARKERS,
    build_evolution_plan,
    build_model_comparison_inventory,
    build_qvirtual_labs_plan,
    evaluate_dataset_comparison_evidence,
    evaluate_model_comparison_evidence,
)


def test_build_evolution_plan_discovers_contracts_and_is_deterministic(tmp_path):
    contract_files = {
        "AUTODEV.md": "# Autodev\n\nremote-continuity-and-failover\n",
        "ALLQMOIAUTOEVOLVINGENVS.md": "# Auto-evolving environments\n",
        "QCITY.md": "# QCity\n",
        "QCITYUI.md": "# QCity UI\n",
        "ALLTRACKS.md": "# Tracking\n",
        "ALLLANGUAGES.md": "# Languages\n",
        "ALLLANGUAGESCOMPARE.md": "# Language comparison\n",
        "QLIONPROGRAMMINGLANGUAGE.md": "# QLion language\n",
        "QVILLAGE.md": "# QVillage\n",
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
        "auto_evolving_environments",
        "qcity_feature_monitoring",
        "language_capability_research",
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
        "model_comparison",
        "dataset_comparison",
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
    auto_evolving_stage = next(
        stage for stage in first["stages"]
        if stage["domain"] == "auto_evolving_environments"
    )
    assert auto_evolving_stage["metrics"]["available_source_file_count"] == 3
    assert auto_evolving_stage["target_documents"] == [
        "ALLQMOIAUTOEVOLVINGENVS.md",
        "QAUDITS.md",
        "ALLFEATURES.md",
    ]
    qcity_stage = next(
        stage for stage in first["stages"]
        if stage["domain"] == "qcity_feature_monitoring"
    )
    assert qcity_stage["metrics"]["available_source_file_count"] == 4
    language_stage = next(
        stage for stage in first["stages"]
        if stage["domain"] == "language_capability_research"
    )
    assert language_stage["metrics"]["available_source_file_count"] == 4
    comparison_stage = next(stage for stage in first["stages"] if stage["domain"] == "model_comparison")
    assert comparison_stage["target_documents"] == [
        "QAUDITS.md",
        "QVILLAGE.md",
        "Qvillageevolutions.md",
        "QMOI_MODEL_CARD.md",
        "QMOI_BEST_MODEL_PROOF.md",
    ]
    comparison = first["model_comparison"]
    assert comparison["models_replaced_count"] == 0
    assert comparison["automatic_replacement_enabled"] is False
    assert comparison["comparison_assessment"]["status"] == "NOT_ELIGIBLE"
    assert comparison["remote_verified"] is False
    assert comparison["datasets_replaced_count"] == 0
    assert comparison["dataset_comparison_assessment"]["status"] == "NOT_ELIGIBLE"


def test_model_comparison_inventory_counts_evolution_documents_by_scope(tmp_path):
    (tmp_path / "Qvillageevolutions.md").write_text(
        "# QVillage evolution\n"
        "Feature: source-backed experiments\n"
        "Compare models against the same feature set.\n"
        "QVillage model benchmark evidence remains review-only.\n",
        encoding="utf-8",
    )
    historical = tmp_path / "Alpha-Q-ai-2025" / "MODELEVOLUTIONO.md"
    historical.parent.mkdir()
    historical.write_text(
        "# Historical evolution\nCapability: test matrix\n",
        encoding="utf-8",
    )

    inventory = build_model_comparison_inventory(tmp_path)

    assert inventory["markdown_scan_count"] == 2
    assert inventory["evolution_document_count"] == 2
    assert inventory["qvillage_model_document_count"] == 1
    assert inventory["model_comparison_document_count"] == 1
    assert inventory["evolution_feature_declaration_count"] == 2
    assert inventory["models_replaced_count"] == 0
    records = {item["path"]: item for item in inventory["documents"]}
    assert records["Qvillageevolutions.md"]["scope"] == "active_materialized"
    assert records["Alpha-Q-ai-2025/MODELEVOLUTIONO.md"]["scope"] == "historical_or_archive"
    assert all(item["source_text_recorded"] is False for item in records.values())
    assert inventory["datasets_replaced_count"] == 0
    assert inventory["automatic_replacement_enabled"] is False
    assert inventory["qvillage_platform_inventory"]["status"] == "CANDIDATE_DISCOVERY_ONLY"
    assert all(
        item["integration_verified"] is False
        for item in inventory["qvillage_platform_inventory"]["platforms"].values()
    )


def test_evolution_plan_reports_asset_continuity_paths_without_claiming_success(tmp_path):
    for relative, content in (
        ("Qstarlink.md", "# Connectivity policy\n"),
        ("Alpha-Q-ai-2025/src/services/NetworkManager.ts", "export class NetworkManager {}\n"),
        ("tests/test_qaudits_evolution_planner.py", "def test_contract(): pass\n"),
    ):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    continuity = build_evolution_plan(tmp_path)["asset_continuity"]
    metrics = continuity["metrics"]
    starlink = continuity["domains"]["connectivity_starlink"]

    assert continuity["schema_version"] == 1
    assert continuity["status"] == "CANDIDATE_DISCOVERY_ONLY"
    assert metrics["required_domain_count"] == 5
    assert metrics["remote_verified"] is False
    assert metrics["automatic_replacement_enabled"] is False
    assert metrics["financial_actions_authorized"] is False
    assert metrics["network_changes_authorized"] is False
    assert starlink["metrics"]["observed_path_count"] == 2
    assert starlink["metrics"]["missing_or_unavailable_path_count"] == 1
    assert starlink["metrics"]["observed_test_count"] == 0
    assert "export class NetworkManager" not in json.dumps(continuity)


def _eligible_dataset_evidence():
    evidence = {
        "schema_version": DATASET_COMPARISON_EVIDENCE_SCHEMA_VERSION,
        "run_id": "dataset-run-001",
        "correlation_id": "test-correlation",
        "repository": "thealphakenya/Alpha-Q-ai",
        "ref": "refs/heads/test",
        "source_sha256": "1" * 40,
        "tree_sha256": "2" * 40,
        "incumbent_dataset_id": "publisher/dataset:rev1",
        "qmoi_dataset_id": "qvillage/engineering/circuits/v1",
        "artifact_sha256": {"incumbent": "a" * 64, "qmoi": "b" * 64},
        "benchmark": {
            "suite_id": "qvillage-dataset-suite-v1",
            "suite_sha256": "c" * 64,
            "evaluator_sha256": "d" * 64,
            "environment_sha256": "e" * 64,
            "matched_protocol": True,
            "replicated_runs": 3,
        },
        "metrics": {},
        "canonical_feature_ids": ["circuit_simulation"],
        "feature_comparisons": [{
            "feature_id": "circuit_simulation",
            "required_direction": "higher",
            "direction": "higher",
            "incumbent_score": 0.7,
            "qmoi_score": 0.9,
            "incumbent_confidence_interval": [0.68, 0.72],
            "qmoi_confidence_interval": [0.88, 0.92],
            "sample_count": 40,
        }],
        "canonical_feature_registry_sha256": "f" * 64,
        "hard_gates": {gate: True for gate in DATASET_COMPARISON_HARD_GATES},
    }
    for name, direction in DATASET_COMPARISON_METRICS.items():
        incumbent = 100 if direction == "lower" else 0.7
        candidate = 50 if direction == "lower" else 0.9
        evidence["metrics"][name] = {
            "direction": direction,
            "incumbent_score": incumbent,
            "qmoi_score": candidate,
            "incumbent_confidence_interval": (
                [95, 105] if direction == "lower" else [0.68, 0.72]
            ),
            "qmoi_confidence_interval": (
                [45, 55] if direction == "lower" else [0.88, 0.92]
            ),
            "sample_count": 40,
        }
    return evidence


def test_dataset_replacement_assessment_requires_complete_superiority_and_gates():
    evidence = _eligible_dataset_evidence()

    assessment = evaluate_dataset_comparison_evidence(evidence)
    assert assessment["status"] == "ELIGIBLE_FOR_INDEPENDENT_REVIEW"
    assert assessment["replacement_status"] == "NOT_REPLACED"
    assert assessment["automatic_replacement_enabled"] is False
    assert assessment["remote_verified"] is False

    evidence["hard_gates"]["license_and_allowed_use_verified"] = False
    evidence["metrics"]["task_quality"]["qmoi_score"] = 0.7
    evidence["metrics"]["task_quality"]["qmoi_confidence_interval"] = [0.68, 0.72]
    evidence["metrics"]["coverage"]["sample_count"] = 10
    evidence["artifact_sha256"]["qmoi"] = "invalid"
    evidence["source_sha256"] = "invalid"
    rejected = evaluate_dataset_comparison_evidence(evidence)
    assert rejected["status"] == "NOT_ELIGIBLE"
    assert "dataset_hard_gate_not_passed:license_and_allowed_use_verified" in rejected["blockers"]
    assert "qmoi_dataset_not_better_on_metric:task_quality" in rejected["blockers"]
    assert "invalid_or_underpowered_dataset_metric:coverage" in rejected["blockers"]
    assert "invalid_or_missing_qmoi_dataset_sha256" in rejected["blockers"]
    assert "invalid_or_missing_dataset_comparison_source_sha256" in rejected["blockers"]


def test_dataset_assessment_rejects_unowned_candidate_and_incomplete_feature_coverage():
    evidence = _eligible_dataset_evidence()
    evidence["qmoi_dataset_id"] = "publisher/rebranded-dataset"
    evidence["feature_comparisons"] = []
    evidence["hard_gates"]["candidate_qmoi_owned_or_explicitly_authorized"] = False

    assessment = evaluate_dataset_comparison_evidence(evidence)
    assert assessment["status"] == "NOT_ELIGIBLE"
    assert "candidate_dataset_not_in_qmoi_namespace" in assessment["blockers"]
    assert (
        "dataset_hard_gate_not_passed:candidate_qmoi_owned_or_explicitly_authorized"
        in assessment["blockers"]
    )
    assert "dataset_feature_comparison_missing" in assessment["blockers"]
    assert "dataset_feature_comparison_does_not_cover_canonical_registry" in assessment["blockers"]


def test_inventory_reports_dataset_evidence_and_provider_mentions_as_candidates(tmp_path):
    (tmp_path / "QVILLAGE.md").write_text(
        "# QVillage\nHugging Face datasets and Kaggle notebooks, models, discussions.\n",
        encoding="utf-8",
    )
    (tmp_path / "DATASETS.md").write_text(
        "# Dataset comparison\nCompare datasets for provenance, leakage, and offline quality.\n",
        encoding="utf-8",
    )

    inventory = build_model_comparison_inventory(tmp_path)
    providers = inventory["qvillage_platform_inventory"]["platforms"]
    assert inventory["dataset_comparison_document_count"] == 1
    assert inventory["dataset_comparison_evidence_status"] == "NOT_PRESENT"
    assert inventory["dataset_comparison_assessment"]["status"] == "NOT_ELIGIBLE"
    assert inventory["qvillage_platform_inventory"]["document_candidate_count"] == 1
    assert len(inventory["qvillage_platform_inventory"]["source_manifest_sha256"]) == 64
    assert providers["huggingface"]["document_candidate_count"] == 1
    assert providers["kaggle"]["document_candidate_count"] == 1
    assert providers["huggingface"]["integration_verified"] is False


def test_inventory_assesses_hash_bound_dataset_evidence_without_replacement(tmp_path):
    evidence_path = tmp_path / "ollamatracks" / "dataset_comparison_evidence.json"
    evidence_path.parent.mkdir()
    evidence_path.write_text(
        json.dumps(_eligible_dataset_evidence()),
        encoding="utf-8",
    )

    inventory = build_model_comparison_inventory(tmp_path)

    assert inventory["dataset_comparison_evidence_status"] == "PARSED"
    assert inventory["dataset_comparison_assessment"]["status"] == "ELIGIBLE_FOR_INDEPENDENT_REVIEW"
    assert inventory["datasets_replaced_count"] == 0
    assert inventory["automatic_replacement_enabled"] is False
    assert inventory["remote_verified"] is False


def test_model_replacement_assessment_requires_superiority_on_every_dimension_and_gate():
    evidence = {
        "schema_version": MODEL_COMPARISON_EVIDENCE_SCHEMA_VERSION,
        "run_id": "model-run-001",
        "correlation_id": "test-correlation",
        "repository": "thealphakenya/Alpha-Q-ai",
        "ref": "refs/heads/test",
        "source_sha256": "1" * 40,
        "tree_sha256": "2" * 40,
        "incumbent_model_id": "incumbent:latest",
        "qmoi_model_id": "QMOI:verified-candidate",
        "benchmark": {
            "suite_id": "qvillage-full-suite-v1",
            "suite_sha256": "a" * 64,
            "dataset_sha256": "b" * 64,
            "environment_sha256": "c" * 64,
            "matched_protocol": True,
            "replicated_runs": 3,
        },
        "dimensions": {},
        "canonical_feature_ids": ["chat"],
        "feature_comparisons": [{
            "feature_id": "chat",
            "direction": "higher",
            "incumbent_score": 0.7,
            "qmoi_score": 0.9,
            "incumbent_confidence_interval": [0.68, 0.72],
            "qmoi_confidence_interval": [0.88, 0.92],
            "sample_count": 40,
        }],
        "canonical_feature_registry_sha256": "d" * 64,
        "hard_gates": {gate: True for gate in MODEL_COMPARISON_HARD_GATES},
    }
    for name, direction in MODEL_COMPARISON_DIMENSIONS.items():
        if direction == "higher":
            evidence["dimensions"][name] = {
                "direction": direction,
                "incumbent_score": 0.7,
                "qmoi_score": 0.9,
                "incumbent_confidence_interval": [0.68, 0.72],
                "qmoi_confidence_interval": [0.88, 0.92],
                "sample_count": 40,
            }
        else:
            evidence["dimensions"][name] = {
                "direction": direction,
                "incumbent_score": 100,
                "qmoi_score": 50,
                "incumbent_confidence_interval": [95, 105],
                "qmoi_confidence_interval": [45, 55],
                "sample_count": 40,
            }

    assessment = evaluate_model_comparison_evidence(evidence)
    assert assessment["status"] == "ELIGIBLE_FOR_INDEPENDENT_REVIEW"
    assert assessment["replacement_status"] == "NOT_REPLACED"
    assert assessment["automatic_replacement_enabled"] is False
    assert assessment["remote_verified"] is False

    evidence["dimensions"]["coding"]["qmoi_confidence_interval"] = [0.70, 0.75]
    rejected = evaluate_model_comparison_evidence(evidence)
    assert rejected["status"] == "NOT_ELIGIBLE"
    assert "candidate_not_better_on_dimension:coding" in rejected["blockers"]

    del evidence["tree_sha256"]
    rejected_identity = evaluate_model_comparison_evidence(evidence)
    assert "invalid_or_missing_model_comparison_tree_sha256" in rejected_identity["blockers"]


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

    (tmp_path / "QENGINEER.md").write_text("# Engineering requirements\n\n1. Preserve mission evidence.\n2. Keep QVillage research review-only.\n3. Map each requirement to tests.\n", encoding="utf-8")
    reconciled = build_qvirtual_labs_plan(tmp_path, source_manifest_sha256="manifest-qv")
    assert reconciled["status"] == "NEEDS_REVIEW"
    assert reconciled["metrics"]["source_requirement_count"] == 3
    assert not any("QENGINEER.md" in blocker for blocker in reconciled["blockers"])


def test_qengineer_requirement_count_is_detected_for_local_contract(tmp_path):
    (tmp_path / "QVIRTUALLABS.md").write_text(
        "# Labs\n\n" + QVIRTUAL_LAB_DOMAIN_MARKERS[0] + "\n1. **Circuit design** — candidate.\n" + QVIRTUAL_LAB_DOMAIN_MARKERS[1] + "\n",
        encoding="utf-8",
    )
    (tmp_path / "QENGINEER.md").write_text(
        "# QEngineer\n\n## Required safeguards\n\n- Preserve mission state.\n- Keep checkpoints and evidence aligned.\n- Block remote completion without exact SHA proof.\n",
        encoding="utf-8",
    )

    plan = build_qvirtual_labs_plan(tmp_path)
    assert plan["status"] == "NEEDS_REVIEW"
    assert plan["metrics"]["source_requirement_count"] == 3
