"""Build a deterministic, local-only QAUDITS evolution plan."""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTRACTS = (
    ("autodev", ("AUTODEV.md",)),
    ("model_evolution", ("MODELEVOLUTIONO.md", "MODELEVUTIONO.md")),
    ("qvillage_evolution", ("Qvillageevolutions.md",)),
    (
        "auto_evolving_environments",
        ("ALLQMOIAUTOEVOLVINGENVS.md", "AUTODEV.md", "Qvillageevolutions.md"),
    ),
    (
        "qcity_feature_monitoring",
        ("QCITY.md", "QCITYUI.md", "ALLFEATURES.md", "ALLTRACKS.md"),
    ),
    (
        "language_capability_research",
        ("ALLLANGUAGES.md", "ALLLANGUAGESCOMPARE.md", "QLIONPROGRAMMINGLANGUAGE.md", "QVILLAGE.md"),
    ),
    ("qvirtual_labs", ("QVIRTUALLABS.md", "QENGINEER.md", "Qvillageevolutions.md")),
    ("internal_research", ("INTERNALRESEARCH.md",)),
    ("external_research", ("EXTERNALRESEARCH.md", "EXTERIORRESEARCH.md")),
    ("q_seed", ("QSEED.md",)),
    ("q_version", ("QVERSIONMANAGER.md",)),
    ("instruction_inventory", ("AGENTS.md", ".github/copilot-instructions.md")),
    ("repository_surface_audit", ("scripts/qaudit_universe.py", "scripts/ollama_research.py")),
    (
        "markdown_refresh",
        (
            "ALLMDFILESREFS.md",
            "TRANSION.md",
            "TRANSIONQ.md",
            "TRANSITION.md",
            "QVIRTUALLAB.md",
            "QVIRTUALLABS.md",
        ),
    ),
    ("production_gate", ("production.md", "productionenhanced.md")),
    ("validation", ("ALLVALIDATIONS.md",)),
    ("remote_verification", ("remotecompletion.md", "remote-completion.json")),
    ("evolutiono_pre_retirement", ("MODELEVOLUTIONO.md", "scripts/q_version_manager.py", "AUTODEV.md")),
    ("qmoi_capability_parity", ("AUTODEV.md", "ALLFEATURES.md", "ALLTESTSAUTOTESTS.md")),
    ("qreplaceo_archive", ("SYNC.md", "MODELEVOLUTIONO.md")),
    ("evolutiono_clean_branch_audit", ("SYNC.md", "scripts/qaudit_universe.py", "scripts/qaudits_evolution_planner.py")),
    ("evolutiono_ofca_metrics", ("MODELEVOLUTIONO.md", "scripts/qaudits_evolution_planner.py", "scripts/q_version_manager.py")),
    ("model_comparison", ("QAUDITS.md", "QVILLAGE.md", "Qvillageevolutions.md", "QMOI_MODEL_CARD.md", "QMOI_BEST_MODEL_PROOF.md")),
    ("dataset_comparison", ("QAUDITS.md", "DATASETS.md", "ALLCOMPARETYPES.md", "QVILLAGE.md")),
)

EVOLUTIONO_TRANSITION_DOMAINS = (
    "evolutiono_pre_retirement",
    "qmoi_capability_parity",
    "qreplaceo_archive",
    "evolutiono_clean_branch_audit",
    "evolutiono_ofca_metrics",
)
PLAN_TARGETS = {
    "repository_surface_audit": ("QAUDITS.md", "OFCA.md"),
    "auto_evolving_environments": (
        "ALLQMOIAUTOEVOLVINGENVS.md",
        "QAUDITS.md",
        "ALLFEATURES.md",
    ),
    "qcity_feature_monitoring": (
        "QCITY.md",
        "QCITYUI.md",
        "ALLTRACKS.md",
    ),
    "language_capability_research": (
        "ALLLANGUAGES.md",
        "ALLLANGUAGESCOMPARE.md",
        "QVILLAGE.md",
    ),
    "qvirtual_labs": (
        "QVIRTUALLAB.md",
        "QVIRTUALLABS.md",
        "QAUDITS.md",
        "TRANSION.md",
        "TRANSIONQ.md",
        "TRANSITION.md",
        "QVILLAGE.md",
        "Qvillageevolutions.md",
    ),
    "evolutiono_ofca_metrics": ("OFCA.md",),
    "model_comparison": (
        "QAUDITS.md",
        "QVILLAGE.md",
        "Qvillageevolutions.md",
        "QMOI_MODEL_CARD.md",
        "QMOI_BEST_MODEL_PROOF.md",
    ),
    "dataset_comparison": (
        "QAUDITS.md",
        "DATASETS.md",
        "ALLCOMPARETYPES.md",
        "QVILLAGE.md",
        "QMOI_MODEL_CARD.md",
    ),
}

MODEL_COMPARISON_EVIDENCE_PATH = "ollamatracks/model_comparison_evidence.json"
DATASET_COMPARISON_EVIDENCE_PATH = "ollamatracks/dataset_comparison_evidence.json"

ASSET_CONTINUITY_CONTRACTS = {
    "model_dataset_replacement": {
        "documents": ("ALLCOMPARETYPES.md", "QAUDITS.md", "QVERSIONMANAGER.md"),
        "implementation_sources": (
            "scripts/qaudits_evolution_planner.py",
            "scripts/q_version_manager.py",
        ),
        "tests": ("tests/test_qaudits_evolution_planner.py",),
        "evidence_artifacts": (
            MODEL_COMPARISON_EVIDENCE_PATH,
            DATASET_COMPARISON_EVIDENCE_PATH,
        ),
    },
    "project_memory_continuity": {
        "documents": (
            "MEMORY_INDEX.md",
            "QMOI_REALTIME_MEMORY_INDEX.md",
            "projectandautoprojects.md",
            "projectsandautoprojects.md",
        ),
        "implementation_sources": (
            "Alpha-Q-ai-2025/src/services/QmoiMemory.ts",
            "Alpha-Q-ai-2025/src/hooks/useAutoProjects.ts",
            "scripts/ollama_autonomous_agent.py",
        ),
        "tests": ("tests/test_ollama_autonomous_agent.py",),
        "evidence_artifacts": ("ollamatracks/restore_point_memory.json",),
    },
    "project_finance_accountability": {
        "documents": ("FINANCIALMANAGER.md", "projectsandautoprojects.md"),
        "implementation_sources": ("Alpha-Q-ai-2025/src/hooks/useAutoProjects.ts",),
        "tests": ("Alpha-Q-ai-2025/tests/integration/test_financial_verification.py",),
        "evidence_artifacts": (),
    },
    "engineering_validation": {
        "documents": ("QENGINEER.md", "QVIRTUALLABS.md", "ALLCOMPARETYPES.md"),
        "implementation_sources": ("scripts/qaudits_evolution_planner.py",),
        "tests": ("tests/test_qaudits_evolution_planner.py",),
        "evidence_artifacts": (),
    },
    "connectivity_starlink": {
        "documents": ("Qstarlink.md",),
        "implementation_sources": ("Alpha-Q-ai-2025/src/services/NetworkManager.ts",),
        "tests": ("Alpha-Q-ai-2025/src/services/NetworkManager.test.ts",),
        "evidence_artifacts": (),
    },
}

EVOLUTION_MARKER = re.compile(
    r"\b(?:evol\w*|self[- ]?improv\w*|adapt\w*|capability growth)\b",
    re.IGNORECASE,
)
MODEL_COMPARISON_MARKER = re.compile(
    r"\b(?:model comparison|compare(?:d|s|ing)? models?|benchmark(?:ing)?|"
    r"model evaluation|model parity|replace(?:ment)? model)\b",
    re.IGNORECASE,
)
DATASET_COMPARISON_MARKER = re.compile(
    r"\b(?:dataset comparison|compare(?:d|s|ing)? datasets?|dataset replacement|"
    r"data(?:set)? (?:quality|provenance|leakage|contamination))\b",
    re.IGNORECASE,
)
QVILLAGE_MODEL_MARKER = re.compile(
    r"\b(?:qvillage|qvs)\b.*\b(?:model|evol\w*|benchmark|compar\w*)\b|"
    r"\b(?:model|evol\w*|benchmark|compar\w*)\b.*\b(?:qvillage|qvs)\b",
    re.IGNORECASE,
)
FEATURE_DECLARATION = re.compile(
    r"^\s*(?:#{1,6}\s*)?(?:[-*]\s*)?(?:feature|capability)\s*[:—-]",
    re.IGNORECASE,
)
MODEL_COMPARISON_EVIDENCE_SCHEMA_VERSION = 2
DATASET_COMPARISON_EVIDENCE_SCHEMA_VERSION = 1
MODEL_COMPARISON_DIMENSIONS = {
    "task_quality": "higher",
    "reasoning": "higher",
    "coding": "higher",
    "factuality": "higher",
    "safety": "higher",
    "privacy": "higher",
    "security": "higher",
    "reliability": "higher",
    "throughput": "higher",
    "offline_independence": "higher",
    "latency": "lower",
    "resource_cost": "lower",
}
MODEL_COMPARISON_HARD_GATES = (
    "model_artifact_provenance_verified",
    "model_runtime_compatibility_passed",
    "safety_review_passed",
    "privacy_review_passed",
    "security_review_passed",
    "license_review_passed",
    "offline_test_passed",
    "regression_suite_passed",
    "rollback_tested",
    "independent_reviewer_approved",
)
DATASET_COMPARISON_METRICS = {
    "task_quality": "higher",
    "coverage": "higher",
    "data_quality": "higher",
    "offline_independence": "higher",
    "resource_cost": "lower",
}
DATASET_COMPARISON_HARD_GATES = (
    "candidate_qmoi_owned_or_explicitly_authorized",
    "source_provenance_verified",
    "license_and_allowed_use_verified",
    "privacy_review_passed",
    "schema_compatibility_passed",
    "split_leakage_check_passed",
    "benchmark_contamination_check_passed",
    "security_review_passed",
    "regression_suite_passed",
    "offline_test_passed",
    "rollback_tested",
    "independent_reviewer_approved",
)
QVILLAGE_PLATFORM_ALIASES = {
    "huggingface": ("hugging face", "huggingface", "hf hub", "hf.co"),
    "kaggle": ("kaggle", "kaggle.com"),
    "dagshub": ("dagshub", "dagshub.com"),
    "github": ("github", "github.com"),
    "gitlab": ("gitlab", "gitlab.com"),
    "modelscope": ("modelscope", "modelscope.cn"),
    "openxlab": ("openxlab", "openxlab.org.cn"),
    "weights_and_biases": ("weights & biases", "weights and biases", "wandb"),
    "mlflow": ("mlflow", "model registry"),
}
QVILLAGE_PLATFORM_SURFACES = {
    "model_catalog": ("model", "models", "model card", "inference"),
    "dataset_catalog": ("dataset", "datasets", "dataset card"),
    "app_space": ("space", "spaces", "app demo", "hosted app"),
    "discussion": ("discussion", "discussions", "community", "thread"),
    "competition": ("competition", "competitions", "leaderboard", "challenge"),
    "notebook": ("notebook", "notebooks", "kernel"),
    "repository": ("repository", "repositories", "git", "source code"),
    "experiment_tracking": ("experiment", "experiments", "run tracking", "metrics"),
    "automation_events": ("webhook", "webhooks", "event", "automation"),
    "access_control": ("authentication", "authorization", "permissions", "access control"),
}
MODEL_INVENTORY_EXCLUDED_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "dist", "build", "target", "coverage",
}
MODEL_INVENTORY_MAX_BYTES = 5_000_000


def _load_comparison_evidence(source_root: Path, evidence_path: str) -> tuple[Any, str]:
    path = source_root / evidence_path
    if not path.exists():
        return None, "NOT_PRESENT"
    if path.is_symlink():
        return None, "SYMLINK_NOT_FOLLOWED"
    try:
        if path.stat(follow_symlinks=False).st_size > 1_000_000:
            return None, "OVERSIZED"
        return json.loads(path.read_text(encoding="utf-8")), "PARSED"
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None, "INVALID"


def _comparison_interval_is_valid(interval: Any) -> bool:
    return (
        isinstance(interval, list)
        and len(interval) == 2
        and all(
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
            for value in interval
        )
        and interval[0] <= interval[1]
    )


def _candidate_is_better(direction: str, candidate_interval: list[Any], incumbent_interval: list[Any]) -> bool:
    if direction == "higher":
        return candidate_interval[0] > incumbent_interval[1]
    return candidate_interval[1] < incumbent_interval[0]


def _comparison_run_identity_blockers(evidence: dict[str, Any], subject: str) -> list[str]:
    blockers = []
    for field in ("run_id", "correlation_id", "repository", "ref"):
        value = evidence.get(field)
        if not isinstance(value, str) or not value.strip():
            blockers.append(f"missing_{subject}_{field}")
    repository = evidence.get("repository")
    if isinstance(repository, str) and not re.fullmatch(r"[^/\s]+/[^/\s]+", repository):
        blockers.append(f"invalid_{subject}_repository")
    for field in ("source_sha256", "tree_sha256"):
        value = evidence.get(field)
        if not isinstance(value, str) or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value):
            blockers.append(f"invalid_or_missing_{subject}_{field}")
    return blockers


def evaluate_dataset_comparison_evidence(evidence: Any) -> dict[str, Any]:
    """Assess dataset comparison completeness; never authorize a data switch."""
    blockers: list[str] = []
    if not isinstance(evidence, dict):
        evidence = {}
        blockers.append("dataset_comparison_evidence_missing_or_not_an_object")

    if evidence.get("schema_version") != DATASET_COMPARISON_EVIDENCE_SCHEMA_VERSION:
        blockers.append("unsupported_or_missing_dataset_evidence_schema")
    blockers.extend(_comparison_run_identity_blockers(evidence, "dataset_comparison"))

    incumbent_id = evidence.get("incumbent_dataset_id")
    candidate_id = evidence.get("qmoi_dataset_id")
    for field, value in (
        ("incumbent_dataset_id", incumbent_id),
        ("qmoi_dataset_id", candidate_id),
    ):
        if not isinstance(value, str) or not value.strip():
            blockers.append(f"missing_{field}")
    if (
        isinstance(incumbent_id, str)
        and isinstance(candidate_id, str)
        and incumbent_id == candidate_id
    ):
        blockers.append("incumbent_and_candidate_dataset_ids_must_differ")
    if isinstance(candidate_id, str) and not candidate_id.casefold().startswith("qvillage/"):
        blockers.append("candidate_dataset_not_in_qmoi_namespace")

    artifact_hashes = evidence.get("artifact_sha256")
    artifact_hashes = artifact_hashes if isinstance(artifact_hashes, dict) else {}
    for key in ("incumbent", "qmoi"):
        digest = artifact_hashes.get(key)
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            blockers.append(f"invalid_or_missing_{key}_dataset_sha256")

    benchmark = evidence.get("benchmark")
    benchmark = benchmark if isinstance(benchmark, dict) else {}
    for field in ("suite_id", "suite_sha256", "evaluator_sha256", "environment_sha256"):
        value = benchmark.get(field)
        if field.endswith("_sha256"):
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                blockers.append(f"invalid_or_missing_benchmark_{field}")
        elif not isinstance(value, str) or not value.strip():
            blockers.append(f"missing_benchmark_{field}")
    if benchmark.get("matched_protocol") is not True:
        blockers.append("matched_dataset_protocol_not_verified")
    if not isinstance(benchmark.get("replicated_runs"), int) or benchmark["replicated_runs"] < 3:
        blockers.append("fewer_than_three_dataset_replicated_runs")

    metrics = evidence.get("metrics")
    metrics = metrics if isinstance(metrics, dict) else {}
    missing_metrics = sorted(set(DATASET_COMPARISON_METRICS) - set(metrics))
    blockers.extend(f"dataset_metric_not_measured:{name}" for name in missing_metrics)
    failed_metrics: list[str] = []
    for name, required_direction in DATASET_COMPARISON_METRICS.items():
        record = metrics.get(name)
        if not isinstance(record, dict):
            continue
        incumbent_interval = record.get("incumbent_confidence_interval")
        candidate_interval = record.get("qmoi_confidence_interval")
        valid_scores = all(
            isinstance(record.get(key), (int, float))
            and not isinstance(record.get(key), bool)
            and math.isfinite(record[key])
            for key in ("incumbent_score", "qmoi_score")
        )
        if (
            record.get("direction") != required_direction
            or not valid_scores
            or not _comparison_interval_is_valid(incumbent_interval)
            or not _comparison_interval_is_valid(candidate_interval)
            or not isinstance(record.get("sample_count"), int)
            or isinstance(record.get("sample_count"), bool)
            or record["sample_count"] < 30
        ):
            blockers.append(f"invalid_or_underpowered_dataset_metric:{name}")
            continue
        score_improved = (
            record["qmoi_score"] > record["incumbent_score"]
            if required_direction == "higher"
            else record["qmoi_score"] < record["incumbent_score"]
        )
        if not score_improved or not _candidate_is_better(
            required_direction,
            candidate_interval,
            incumbent_interval,
        ):
            failed_metrics.append(name)

    canonical_feature_ids = evidence.get("canonical_feature_ids")
    if (
        not isinstance(canonical_feature_ids, list)
        or not canonical_feature_ids
        or any(not isinstance(item, str) or not item for item in canonical_feature_ids)
        or len(set(canonical_feature_ids)) != len(canonical_feature_ids)
    ):
        blockers.append("canonical_feature_registry_feature_list_missing_or_invalid")
        canonical_feature_ids = []
    feature_comparisons = evidence.get("feature_comparisons")
    feature_comparisons = feature_comparisons if isinstance(feature_comparisons, list) else []
    if not feature_comparisons:
        blockers.append("dataset_feature_comparison_missing")
    feature_ids: set[str] = set()
    failed_features: list[str] = []
    for feature in feature_comparisons:
        if not isinstance(feature, dict):
            blockers.append("malformed_dataset_feature_comparison")
            continue
        feature_id = feature.get("feature_id")
        direction = feature.get("direction")
        incumbent_interval = feature.get("incumbent_confidence_interval")
        candidate_interval = feature.get("qmoi_confidence_interval")
        valid = (
            isinstance(feature_id, str)
            and bool(feature_id)
            and feature_id not in feature_ids
            and direction in {"higher", "lower"}
            and direction == feature.get("required_direction")
            and all(
                isinstance(feature.get(key), (int, float))
                and not isinstance(feature.get(key), bool)
                and math.isfinite(feature[key])
                for key in ("incumbent_score", "qmoi_score")
            )
            and _comparison_interval_is_valid(incumbent_interval)
            and _comparison_interval_is_valid(candidate_interval)
            and isinstance(feature.get("sample_count"), int)
            and not isinstance(feature.get("sample_count"), bool)
            and feature["sample_count"] >= 30
        )
        if not valid:
            blockers.append("invalid_or_duplicate_dataset_feature_comparison")
            continue
        feature_ids.add(feature_id)
        score_improved = (
            feature["qmoi_score"] > feature["incumbent_score"]
            if direction == "higher"
            else feature["qmoi_score"] < feature["incumbent_score"]
        )
        if not score_improved or not _candidate_is_better(
            direction,
            candidate_interval,
            incumbent_interval,
        ):
            failed_features.append(feature_id)
    if feature_ids != set(canonical_feature_ids):
        blockers.append("dataset_feature_comparison_does_not_cover_canonical_registry")
    registry_hash = evidence.get("canonical_feature_registry_sha256")
    if not isinstance(registry_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", registry_hash):
        blockers.append("canonical_feature_registry_hash_missing_or_invalid")

    hard_gates = evidence.get("hard_gates")
    hard_gates = hard_gates if isinstance(hard_gates, dict) else {}
    failed_hard_gates = [
        name for name in DATASET_COMPARISON_HARD_GATES if hard_gates.get(name) is not True
    ]
    blockers.extend(f"dataset_hard_gate_not_passed:{name}" for name in failed_hard_gates)
    blockers.extend(f"qmoi_dataset_not_better_on_metric:{name}" for name in failed_metrics)
    blockers.extend(f"qmoi_dataset_not_better_on_feature:{name}" for name in failed_features)

    complete = not blockers
    return {
        "status": "ELIGIBLE_FOR_INDEPENDENT_REVIEW" if complete else "NOT_ELIGIBLE",
        "comparison_evidence_complete": complete,
        "required_metric_count": len(DATASET_COMPARISON_METRICS),
        "measured_metric_count": len(set(DATASET_COMPARISON_METRICS) & set(metrics)),
        "required_feature_comparison_count": len(canonical_feature_ids),
        "measured_feature_comparison_count": len(feature_ids),
        "failed_metric_count": len(failed_metrics),
        "failed_feature_count": len(failed_features),
        "failed_hard_gate_count": len(failed_hard_gates),
        "blockers": sorted(set(blockers)),
        "replacement_status": "NOT_REPLACED",
        "automatic_replacement_enabled": False,
        "remote_verified": False,
        "verification_level": "reported_local_evidence_only",
        "next_action": (
            "Obtain independent review and exact-SHA remote proof; replacement still requires separate explicit authorization."
            if complete
            else "Collect matched, hash-bound dataset evidence and resolve every metric, feature, rights, privacy, offline, security, and rollback blocker."
        ),
    }


def evaluate_model_comparison_evidence(evidence: Any) -> dict[str, Any]:
    """Assess reported benchmark completeness; never authorize a model switch."""
    blockers: list[str] = []
    if not isinstance(evidence, dict):
        evidence = {}
        blockers.append("comparison_evidence_missing_or_not_an_object")

    benchmark = evidence.get("benchmark")
    benchmark = benchmark if isinstance(benchmark, dict) else {}
    if evidence.get("schema_version") != MODEL_COMPARISON_EVIDENCE_SCHEMA_VERSION:
        blockers.append("unsupported_or_missing_evidence_schema")
    blockers.extend(_comparison_run_identity_blockers(evidence, "model_comparison"))
    for field in ("incumbent_model_id", "qmoi_model_id"):
        value = evidence.get(field)
        if not isinstance(value, str) or not value.strip():
            blockers.append(f"missing_{field}")
    if (
        isinstance(evidence.get("incumbent_model_id"), str)
        and evidence.get("incumbent_model_id") == evidence.get("qmoi_model_id")
    ):
        blockers.append("incumbent_and_candidate_model_ids_must_differ")
    if (
        isinstance(evidence.get("qmoi_model_id"), str)
        and not evidence["qmoi_model_id"].casefold().startswith("qmoi")
    ):
        blockers.append("candidate_model_is_not_identified_as_qmoi")
    for field in ("suite_id", "suite_sha256", "dataset_sha256", "environment_sha256"):
        value = benchmark.get(field)
        if field.endswith("_sha256"):
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                blockers.append(f"invalid_or_missing_benchmark_{field}")
        elif not isinstance(value, str) or not value.strip():
            blockers.append(f"missing_benchmark_{field}")
    if benchmark.get("matched_protocol") is not True:
        blockers.append("matched_benchmark_protocol_not_verified")
    if not isinstance(benchmark.get("replicated_runs"), int) or benchmark["replicated_runs"] < 3:
        blockers.append("fewer_than_three_replicated_runs")

    dimensions = evidence.get("dimensions")
    dimensions = dimensions if isinstance(dimensions, dict) else {}
    missing_dimensions = sorted(set(MODEL_COMPARISON_DIMENSIONS) - set(dimensions))
    blockers.extend(f"dimension_not_measured:{name}" for name in missing_dimensions)
    failed_dimensions: list[str] = []
    for name, direction in MODEL_COMPARISON_DIMENSIONS.items():
        record = dimensions.get(name)
        if not isinstance(record, dict):
            continue
        incumbent = record.get("incumbent_score")
        candidate = record.get("qmoi_score")
        incumbent_ci = record.get("incumbent_confidence_interval")
        candidate_ci = record.get("qmoi_confidence_interval")
        sample_count = record.get("sample_count")
        valid_scores = (
            isinstance(incumbent, (int, float))
            and not isinstance(incumbent, bool)
            and math.isfinite(incumbent)
            and isinstance(candidate, (int, float))
            and not isinstance(candidate, bool)
            and math.isfinite(candidate)
        )
        valid_intervals = (
            isinstance(incumbent_ci, list)
            and len(incumbent_ci) == 2
            and isinstance(candidate_ci, list)
            and len(candidate_ci) == 2
            and all(isinstance(value, (int, float)) and math.isfinite(value) for value in [*incumbent_ci, *candidate_ci])
            and incumbent_ci[0] <= incumbent_ci[1]
            and candidate_ci[0] <= candidate_ci[1]
        )
        if (
            record.get("direction") != direction
            or not valid_scores
            or not valid_intervals
            or not isinstance(sample_count, int)
            or sample_count < 30
        ):
            blockers.append(f"invalid_or_underpowered_dimension_evidence:{name}")
            continue
        candidate_clearly_better = (
            candidate_ci[0] > incumbent_ci[1]
            if direction == "higher"
            else candidate_ci[1] < incumbent_ci[0]
        )
        if not candidate_clearly_better:
            failed_dimensions.append(name)

    feature_comparisons = evidence.get("feature_comparisons")
    if not isinstance(feature_comparisons, list) or not feature_comparisons:
        blockers.append("feature_level_comparison_missing")
        feature_comparisons = []
    canonical_feature_ids = evidence.get("canonical_feature_ids")
    if (
        not isinstance(canonical_feature_ids, list)
        or not canonical_feature_ids
        or any(not isinstance(item, str) or not item for item in canonical_feature_ids)
        or len(set(canonical_feature_ids)) != len(canonical_feature_ids)
    ):
        blockers.append("canonical_feature_registry_feature_list_missing_or_invalid")
        canonical_feature_ids = []
    feature_ids: set[str] = set()
    failed_features: list[str] = []
    for feature in feature_comparisons:
        if not isinstance(feature, dict):
            blockers.append("malformed_feature_comparison")
            continue
        feature_id = feature.get("feature_id")
        incumbent_score = feature.get("incumbent_score")
        candidate_score = feature.get("qmoi_score")
        incumbent_ci = feature.get("incumbent_confidence_interval")
        candidate_ci = feature.get("qmoi_confidence_interval")
        direction = feature.get("direction")
        if (
            not isinstance(feature_id, str)
            or not feature_id
            or feature_id in feature_ids
            or not isinstance(incumbent_score, (int, float))
            or isinstance(incumbent_score, bool)
            or not math.isfinite(incumbent_score)
            or not isinstance(candidate_score, (int, float))
            or isinstance(candidate_score, bool)
            or not math.isfinite(candidate_score)
            or direction not in {"higher", "lower"}
            or not isinstance(incumbent_ci, list)
            or len(incumbent_ci) != 2
            or not isinstance(candidate_ci, list)
            or len(candidate_ci) != 2
            or any(
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(value)
                for value in [*(incumbent_ci if isinstance(incumbent_ci, list) else []),
                              *(candidate_ci if isinstance(candidate_ci, list) else [])]
            )
            or incumbent_ci[0] > incumbent_ci[1]
            or candidate_ci[0] > candidate_ci[1]
            or not isinstance(feature.get("sample_count"), int)
            or feature["sample_count"] < 30
        ):
            blockers.append("invalid_or_duplicate_feature_comparison")
            continue
        feature_ids.add(feature_id)
        feature_improved = (
            candidate_ci[0] > incumbent_ci[1]
            if direction == "higher"
            else candidate_ci[1] < incumbent_ci[0]
        )
        score_improved = (
            candidate_score > incumbent_score
            if direction == "higher"
            else candidate_score < incumbent_score
        )
        if not score_improved or not feature_improved:
            failed_features.append(feature_id)
    if feature_ids != set(canonical_feature_ids):
        blockers.append("feature_comparison_does_not_cover_canonical_registry")
    if not isinstance(evidence.get("canonical_feature_registry_sha256"), str) or not re.fullmatch(
        r"[0-9a-f]{64}", evidence.get("canonical_feature_registry_sha256", "")
    ):
        blockers.append("canonical_feature_registry_hash_missing_or_invalid")

    hard_gates = evidence.get("hard_gates")
    hard_gates = hard_gates if isinstance(hard_gates, dict) else {}
    failed_hard_gates = [
        name for name in MODEL_COMPARISON_HARD_GATES if hard_gates.get(name) is not True
    ]
    blockers.extend(f"hard_gate_not_passed:{name}" for name in failed_hard_gates)
    blockers.extend(f"candidate_not_better_on_dimension:{name}" for name in failed_dimensions)
    blockers.extend(f"candidate_not_better_on_feature:{name}" for name in failed_features)

    evidence_complete = not blockers
    return {
        "status": "ELIGIBLE_FOR_INDEPENDENT_REVIEW" if evidence_complete else "NOT_ELIGIBLE",
        "comparison_evidence_complete": evidence_complete,
        "required_dimension_count": len(MODEL_COMPARISON_DIMENSIONS),
        "measured_dimension_count": len(set(MODEL_COMPARISON_DIMENSIONS) & set(dimensions)),
        "required_feature_comparison_count": len(feature_comparisons),
        "failed_dimension_count": len(failed_dimensions),
        "failed_feature_count": len(failed_features),
        "failed_hard_gate_count": len(failed_hard_gates),
        "blockers": sorted(set(blockers)),
        "replacement_status": "NOT_REPLACED",
        "automatic_replacement_enabled": False,
        "remote_verified": False,
        "verification_level": "reported_local_evidence_only",
        "next_action": (
            "Obtain independent review and exact-SHA remote proof; replacement still requires separate explicit authorization."
            if evidence_complete
            else "Run a matched, reproducible comparison covering every required dimension and canonical feature, then review all blockers."
        ),
    }


def build_model_comparison_inventory(root: Path | str) -> dict[str, Any]:
    """Count evolution and model-comparison documentation without storing prose."""
    source_root = Path(root).resolve()
    records: list[dict[str, Any]] = []
    unavailable: list[dict[str, str]] = []
    platform_manifest: list[tuple[str, str, str, tuple[str, ...]]] = []
    scanned_markdown_count = 0
    platform_mentions: dict[str, dict[str, Any]] = {
        platform: {
            "document_candidate_count": 0,
            "surface_candidate_counts": {surface: 0 for surface in QVILLAGE_PLATFORM_SURFACES},
            "integration_verified": False,
        }
        for platform in QVILLAGE_PLATFORM_ALIASES
    }
    if source_root.is_dir():
        for current, dirnames, filenames in os.walk(source_root, followlinks=False):
            current_path = Path(current)
            dirnames[:] = sorted(
                name for name in dirnames
                if name not in MODEL_INVENTORY_EXCLUDED_DIRS
                and not (current_path / name).is_symlink()
            )
            for filename in sorted(filenames):
                path = current_path / filename
                if path.suffix.lower() != ".md":
                    continue
                relative = path.relative_to(source_root).as_posix()
                if path.is_symlink():
                    unavailable.append({"path": relative, "reason": "symlink_not_followed"})
                    continue
                try:
                    metadata = path.stat(follow_symlinks=False)
                    if metadata.st_size > MODEL_INVENTORY_MAX_BYTES:
                        unavailable.append({"path": relative, "reason": "oversized_not_parsed"})
                        continue
                    data = path.read_bytes()
                    text = data.decode("utf-8")
                except UnicodeDecodeError:
                    unavailable.append({"path": relative, "reason": "invalid_utf8"})
                    continue
                except OSError as exc:
                    unavailable.append({"path": relative, "reason": type(exc).__name__})
                    continue
                scanned_markdown_count += 1
                lines = text.splitlines()
                searchable = f"{relative}\n{text}".casefold()
                matched_platforms: list[str] = []
                for platform, aliases in QVILLAGE_PLATFORM_ALIASES.items():
                    if not any(alias in searchable for alias in aliases):
                        continue
                    matched_platforms.append(platform)
                    platform_record = platform_mentions[platform]
                    platform_record["document_candidate_count"] += 1
                    for surface, markers in QVILLAGE_PLATFORM_SURFACES.items():
                        if any(marker in searchable for marker in markers):
                            platform_record["surface_candidate_counts"][surface] += 1
                if matched_platforms:
                    scope = (
                        "historical_or_archive"
                        if any(
                            part.lower().startswith(("alpha-q-ai-2025", "qmoi-enhanced-history"))
                            or "archive" in part.lower()
                            for part in Path(relative).parts
                        )
                        else "active_materialized"
                    )
                    platform_manifest.append((
                        relative,
                        hashlib.sha256(data).hexdigest(),
                        scope,
                        tuple(sorted(matched_platforms)),
                    ))
                evolution_related = bool(EVOLUTION_MARKER.search(relative) or EVOLUTION_MARKER.search(text))
                qvillage_model = bool(
                    "qvillage" in relative.lower()
                    or "qvs" in Path(relative).parts
                    or QVILLAGE_MODEL_MARKER.search(text)
                )
                model_comparison = bool(
                    MODEL_COMPARISON_MARKER.search(relative)
                    or MODEL_COMPARISON_MARKER.search(text)
                )
                dataset_comparison = bool(
                    DATASET_COMPARISON_MARKER.search(relative)
                    or DATASET_COMPARISON_MARKER.search(text)
                )
                if not (evolution_related or qvillage_model or model_comparison or dataset_comparison):
                    continue
                declarations = sum(bool(FEATURE_DECLARATION.search(line)) for line in lines)
                records.append({
                    "path": relative,
                    "scope": (
                        "historical_or_archive"
                        if any(
                            part.lower().startswith(("alpha-q-ai-2025", "qmoi-enhanced-history"))
                            or "archive" in part.lower()
                            for part in Path(relative).parts
                        )
                        else "active_materialized"
                    ),
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "evolution_related": evolution_related,
                    "qvillage_model_related": qvillage_model,
                    "model_comparison_related": model_comparison,
                    "dataset_comparison_related": dataset_comparison,
                    "feature_declaration_count": declarations,
                    "evolution_feature_declaration_count": declarations if evolution_related else 0,
                    "model_comparison_candidate_line_count": sum(
                        bool(MODEL_COMPARISON_MARKER.search(line)) for line in lines
                    ),
                    "qvillage_model_candidate_line_count": sum(
                        bool(QVILLAGE_MODEL_MARKER.search(line)) for line in lines
                    ),
                    "dataset_comparison_candidate_line_count": sum(
                        bool(DATASET_COMPARISON_MARKER.search(line)) for line in lines
                    ),
                    "source_text_recorded": False,
                })
    records.sort(key=lambda item: item["path"])
    manifest = [
        (item["path"], item["sha256"], item["scope"])
        for item in records
    ]
    platform_manifest.sort()
    evidence, evidence_status = _load_comparison_evidence(
        source_root,
        MODEL_COMPARISON_EVIDENCE_PATH,
    )
    dataset_evidence, dataset_evidence_status = _load_comparison_evidence(
        source_root,
        DATASET_COMPARISON_EVIDENCE_PATH,
    )
    assessment = evaluate_model_comparison_evidence(evidence)
    dataset_assessment = evaluate_dataset_comparison_evidence(dataset_evidence)
    return {
        "status": "NEEDS_REVIEW",
        "source_scope": "materialized_local_markdown_only",
        "markdown_scan_count": scanned_markdown_count,
        "evolution_document_count": sum(item["evolution_related"] for item in records),
        "qvillage_model_document_count": sum(item["qvillage_model_related"] for item in records),
        "model_comparison_document_count": sum(item["model_comparison_related"] for item in records),
        "dataset_comparison_document_count": sum(item["dataset_comparison_related"] for item in records),
        "feature_declaration_count": sum(item["feature_declaration_count"] for item in records),
        "evolution_feature_declaration_count": sum(item["evolution_feature_declaration_count"] for item in records),
        "model_comparison_candidate_line_count": sum(item["model_comparison_candidate_line_count"] for item in records),
        "qvillage_model_candidate_line_count": sum(item["qvillage_model_candidate_line_count"] for item in records),
        "dataset_comparison_candidate_line_count": sum(item["dataset_comparison_candidate_line_count"] for item in records),
        "qvillage_platform_inventory": {
            "status": "CANDIDATE_DISCOVERY_ONLY",
            "source_scope": "materialized_parseable_local_markdown",
            "platform_count": len(platform_mentions),
            "document_candidate_count": len(platform_manifest),
            "source_manifest_sha256": hashlib.sha256(
                json.dumps(
                    platform_manifest,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
            ).hexdigest(),
            "platforms": platform_mentions,
            "limitations": [
                "provider-name and feature-term matches are documentation candidates, not verified adapters or feature parity",
                "authentication, permissions, visibility, pagination, rate limits, freshness, and live API behavior are not measured",
                "platform list is an explicit initial scope, not an exhaustive inventory of every possible provider",
            ],
        },
        "unavailable_document_count": len(unavailable),
        "unavailable_documents": unavailable,
        "documents": records,
        "source_manifest_sha256": hashlib.sha256(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "comparison_evidence_path": MODEL_COMPARISON_EVIDENCE_PATH,
        "comparison_evidence_status": evidence_status,
        "comparison_assessment": assessment,
        "dataset_comparison_evidence_path": DATASET_COMPARISON_EVIDENCE_PATH,
        "dataset_comparison_evidence_status": dataset_evidence_status,
        "dataset_comparison_assessment": dataset_assessment,
        "models_replaced_count": 0,
        "datasets_replaced_count": 0,
        "automatic_replacement_enabled": False,
        "remote_verified": False,
        "limitations": [
            "keyword and explicit Feature/Capability declarations are discovery metrics, not semantic review",
            "a locally reported benchmark file is not independently verified benchmark or remote evidence",
            "all candidate dimensions and feature IDs must be reconciled to the canonical feature registry",
            "model replacement is never performed by QAUDITS; independent review, explicit authorization, rollback, and exact-SHA remote proof are separate gates",
            "dataset replacement is never performed by QAUDITS; independent review, rights/privacy checks, explicit authorization, rollback, and exact-SHA remote proof are separate gates",
            "QVillage platform metrics are local documentation mention counts, not Hugging Face, Kaggle, or cross-platform capability parity",
        ],
    }

QVIRTUAL_LAB_DOMAIN_MARKERS = (
    "<!-- BEGIN QMOI MANAGED: qvirtual-lab-domain-inventory -->",
    "<!-- END QMOI MANAGED: qvirtual-lab-domain-inventory -->",
)
QVIRTUAL_LAB_METRIC_MARKERS = (
    "<!-- BEGIN QMOI MANAGED: qaudit-qvirtual-labs-coverage -->",
    "<!-- END QMOI MANAGED: qaudit-qvirtual-labs-coverage -->",
)
QVIRTUAL_LAB_METRIC_DOCUMENTS = frozenset({
    "QVIRTUALLAB.md",
    "QVIRTUALLABS.md",
    "QAUDITS.md",
    "TRANSION.md",
    "TRANSIONQ.md",
    "TRANSITION.md",
    "QVILLAGE.md",
    "Qvillageevolutions.md",
})

QVIRTUAL_LAB_CROSSCUTTING_REQUIREMENTS = (
    ("ownership_traceability", "Requirement, owner, implementation, test, and source lineage"),
    ("access_and_privacy", "Role boundaries, consent, privacy, and protected invention access"),
    ("input_validation", "Geometry, materials, boundary conditions, units, and dimensional validation"),
    ("solver_selection", "Solver and model selection with documented applicability limits"),
    ("convergence", "Numerical stability, mesh or resolution convergence, and repeatability"),
    ("provenance", "Versioned inputs, solver/model versions, seeds, environment, and result hashes"),
    ("uncertainty", "Sensitivity analysis, uncertainty bounds, and assumptions"),
    ("reference_benchmarks", "Independent reference cases and regression baselines"),
    ("physical_calibration", "Calibration and correlation to traceable physical measurements"),
    ("physical_safety", "Human-reviewed risk assessment and approved physical test protocol"),
    ("instrument_provenance", "Instrument identity, calibration status, operator, time, and raw-data hash"),
    ("result_classification", "Unambiguous simulated, measured, inferred, and unknown result labels"),
    ("execution_isolation", "Sandboxing, resource limits, bounded jobs, and network restrictions"),
    ("failure_recovery", "Cancellation, timeout, retry, partial-result, and recovery behavior"),
    ("interaction_transitions", "Accessible progress, empty, running, success, failure, stale, and cancelled states"),
    ("universal_ui", "Shared design tokens, responsive layouts, keyboard access, and assistive technology"),
    ("project_preview_integration", "Project, auto-project, and preview-window integrations with permission checks"),
    ("qvillage_research", "Source-backed QVillage discovery, review, experiments, and evolution history"),
    ("gated_promotion", "Independent regression review, rollback plan, and authorized promotion"),
)

QVIRTUAL_LAB_RESEARCH_CAPTURED_DATE_UTC = "2026-10-16"
QVIRTUAL_LAB_RESEARCH_FRESH_UNTIL = "2026-10-30"
QVIRTUAL_LAB_RESEARCH_COLLECTOR = "manual-official-document-review/1"
QVIRTUAL_LAB_RESEARCH_SOURCES = (
    {
        "source_url": "https://www.calculix.de/",
        "subject": "CalculiX finite-element analysis",
        "observed_fact": "Official project describes linear/nonlinear static, dynamic, and thermal finite-element analyses.",
        "http_status": 200,
        "retrieved_bytes": 9839,
        "source_sha256": "771c31efba047f9a70685d9232398c3c39390cac3bcea681747395b8f072d6dd",
    },
    {
        "source_url": "https://ngspice.sourceforge.io/",
        "subject": "ngspice circuit simulation",
        "observed_fact": "Official project identifies ngspice as an open-source SPICE circuit simulator.",
        "http_status": 200,
        "retrieved_bytes": 7948,
        "source_sha256": "ec33b25455c0267bebf487f13be7ff64b8aa1aae2923d3f8a7942b360013d3a5",
    },
    {
        "source_url": "https://cfd.direct/openfoam/features/",
        "subject": "OpenFOAM computational fluid dynamics",
        "observed_fact": "Official feature page lists CFD models including RAS, LES, multiphase, reacting flow, dynamic meshes, and parallel processing.",
        "http_status": 200,
        "retrieved_bytes": 98952,
        "source_sha256": "8c7f75b9e56e333d666d87eac7ed51963b1c1fd05ae1b80f6441046a2b742461",
    },
    {
        "source_url": "https://gazebosim.org/docs/latest/getstarted/",
        "subject": "Gazebo robotics simulation",
        "observed_fact": "Official guide documents Gazebo Sim as a 3D robotics simulator with server-only headless mode, SDF worlds, and separate user/developer workflows.",
        "http_status": 200,
        "retrieved_bytes": 41843,
        "source_sha256": "7f21d9fa5aaacd2b849351a93a647f6e712b07b452a4c4a1b74cd88c5e268cad",
    },
    {
        "source_url": "https://dwsim.org/",
        "subject": "DWSIM chemical process simulation",
        "observed_fact": "Official project describes the standard process-simulator release as free and open source; separately offered editions may have different capabilities.",
        "http_status": 200,
        "retrieved_bytes": 245468,
        "source_sha256": "c33f1edcd3f0191978e958a9642f4210182455a5a06c215e141d6c0a1c6c8fe0",
    },
    {
        "source_url": "https://www.freecad.org/",
        "subject": "FreeCAD geometry authoring",
        "observed_fact": "Official project presents FreeCAD as an open-source CAD design application; CAD authoring does not itself validate a physics solver.",
        "http_status": 200,
        "retrieved_bytes": 45200,
        "source_sha256": "3825726c8e40c316f9680edbd85e8ab435e728e65b8c87bcdeff34c345561346",
    },
    {
        "source_url": "https://docs.ollama.com/api/introduction",
        "subject": "Ollama runtime/API boundary",
        "observed_fact": "Official API documentation distinguishes local-server inference from cloud API requests that require an API key.",
        "http_status": 200,
        "retrieved_bytes": 270032,
        "source_sha256": "4cdff4e784bf13edeeeccdcf5a04d811311ea9d35800d421f8c028737c5f6428",
    },
    {
        "source_url": "https://docs.ollama.com/capabilities/structured-outputs",
        "subject": "Ollama structured outputs",
        "observed_fact": "Official docs describe schema-constrained JSON responses and validating them against an application schema; cloud structured outputs are currently unsupported.",
        "http_status": 200,
        "retrieved_bytes": 366050,
        "source_sha256": "5c8d318dba75d40cf7d1ee0bc8c1a6a13413b2418feab1822ec46c131158b3b3",
    },
)
QVIRTUAL_LAB_TOOL_RECOMMENDATIONS = (
    {
        "domain": "electrical circuits",
        "tool": "ngspice",
        "fit": "Dedicated SPICE circuit simulation; best first bounded adapter pilot, subject to a local reference-case test.",
        "decision": "PILOT_CANDIDATE",
    },
    {
        "domain": "finite-element analysis",
        "tool": "CalculiX",
        "fit": "Dedicated structural FEA with documented static, dynamic, thermal, and nonlinear capabilities.",
        "decision": "DOMAIN_ADAPTER_CANDIDATE",
    },
    {
        "domain": "computational fluid dynamics",
        "tool": "OpenFOAM",
        "fit": "Broad CFD capability; defer until isolated resource-bounded worker and solver validation exist.",
        "decision": "DOMAIN_ADAPTER_CANDIDATE",
    },
    {
        "domain": "robotics",
        "tool": "Gazebo Sim",
        "fit": "3D robotics simulation with headless server operation and SDF-described worlds.",
        "decision": "DOMAIN_ADAPTER_CANDIDATE",
    },
    {
        "domain": "chemical processes",
        "tool": "DWSIM",
        "fit": "Open-source process-simulation option; verify the exact edition, automation interface, and license before integration.",
        "decision": "DOMAIN_ADAPTER_CANDIDATE",
    },
    {
        "domain": "CAD and geometry authoring",
        "tool": "FreeCAD",
        "fit": "Open-source CAD/design surface; treat as geometry authoring, not as a universal physics solver.",
        "decision": "OPTIONAL_GEOMETRY_ADAPTER_CANDIDATE",
    },
)


def _candidate_virtual_lab_domains(root: Path) -> list[dict[str, str]]:
    source = root / "QVIRTUALLABS.md"
    if not source.is_file() or source.is_symlink():
        return []
    try:
        content = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    start_marker, end_marker = QVIRTUAL_LAB_DOMAIN_MARKERS
    start = content.find(start_marker)
    end = content.find(end_marker)
    if start < 0 or end <= start:
        return []

    domains: list[dict[str, str]] = []
    for line in content[start + len(start_marker):end].splitlines():
        match = re.match(r"^\s*\d+\.\s+\*\*(.+?)\*\*", line)
        if match:
            name = match.group(1).strip()
            domains.append({
                "id": f"QVLAB-DOM-{len(domains) + 1:02d}",
                "name": name,
                "status": "candidate_unmapped",
            })
    return domains


def build_qvirtual_labs_plan(
    root: Path | str,
    *,
    source_manifest_sha256: str | None = None,
) -> dict[str, Any]:
    """Build local-only QVirtualLabs coverage metrics without claiming execution."""
    source_root = Path(root).resolve()
    active_sources = [
        _file_evidence(source_root, "QVIRTUALLABS.md"),
        _file_evidence(source_root, "QENGINEER.md"),
    ]
    historical_source = _file_evidence(
        source_root,
        "qmoi-enhanced-history-14/QVIRTUALLABS.md",
    )
    research_is_fresh = (
        datetime.now(timezone.utc).date().isoformat()
        <= QVIRTUAL_LAB_RESEARCH_FRESH_UNTIL
    )
    research_observations = [
        {
            **source,
            "retrieved_date_utc": QVIRTUAL_LAB_RESEARCH_CAPTURED_DATE_UTC,
            "retrieved_at_utc": None,
            "retrieval_time_status": "NOT_CAPTURED",
            "freshness_deadline": QVIRTUAL_LAB_RESEARCH_FRESH_UNTIL,
            "collector_version": QVIRTUAL_LAB_RESEARCH_COLLECTOR,
            "result_status": "OBSERVED_DATE_ONLY" if research_is_fresh else "STALE",
        }
        for source in QVIRTUAL_LAB_RESEARCH_SOURCES
    ]
    domains = _candidate_virtual_lab_domains(source_root)
    requirements = [
        {
            "id": domain["id"],
            "name": domain["name"],
            "category": "engineering_domain_candidate",
            "status": domain["status"],
            "implementation_evidence": "NOT_MAPPED",
            "test_evidence": "NOT_MAPPED",
            "simulation_evidence": "NOT_RUN",
            "physical_evidence": "NOT_VERIFIED",
        }
        for domain in domains
    ]
    requirements.extend(
        {
            "id": f"QVLAB-CORE-{index:02d}",
            "name": name,
            "category": "cross_cutting_gate",
            "status": "candidate_unmapped",
            "implementation_evidence": "NOT_MAPPED",
            "test_evidence": "NOT_MAPPED",
            "simulation_evidence": "NOT_RUN",
            "physical_evidence": "NOT_VERIFIED",
        }
        for index, (_, name) in enumerate(QVIRTUAL_LAB_CROSSCUTTING_REQUIREMENTS, start=1)
    )
    missing_authoritative = [
        item["path"]
        for item in active_sources
        if item["path"] == "QENGINEER.md" and item["status"] != "observed_local"
    ]
    manifest_subjects = {
        "active_source_files": active_sources,
        "historical_reference": historical_source,
    }
    scoped_manifest_sha256 = hashlib.sha256(
        json.dumps(manifest_subjects, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    blockers = []
    if missing_authoritative:
        blockers.append("Authoritative QENGINEER.md feature source is missing or unreadable.")
    if not domains:
        blockers.append("Canonical QVIRTUALLABS.md domain inventory is missing or malformed.")
    blockers.extend([
        "No requirement-to-implementation, owner, or focused-test mappings are recorded by this plan.",
        "No simulation, benchmark, calibration, or physical experiment was run by this plan.",
        "Ollama inference, QVillage external research, and UI/project integration are not measured by this plan.",
        "Remote verification is unavailable to this local planner.",
    ])
    metrics = {
        "source_manifest_sha256": source_manifest_sha256 or scoped_manifest_sha256,
        "source_manifest_scope": (
            "qaudit_universe" if source_manifest_sha256 else "qvirtual_labs_source_files"
        ),
        "source_requirement_count": None,
        "starter_domain_candidate_count": len(domains),
        "cross_cutting_gate_candidate_count": len(QVIRTUAL_LAB_CROSSCUTTING_REQUIREMENTS),
        "starter_plan_requirement_count": len(requirements),
        "requirements_mapped_to_implementation_count": 0,
        "requirements_mapped_to_tests_count": 0,
        "simulation_runs_verified_count": 0,
        "benchmark_validations_verified_count": 0,
        "solver_convergence_cases_verified_count": 0,
        "uncertainty_reports_verified_count": 0,
        "accuracy_claims_verified_count": 0,
        "safety_protocols_reviewed_count": 0,
        "physical_experiment_records_verified_count": 0,
        "physical_calibration_correlations_verified_count": 0,
        "fresh_external_research_observations_count": (
            len(research_observations) if research_is_fresh else 0
        ),
        "stale_external_research_observations_count": (
            0 if research_is_fresh else len(research_observations)
        ),
        "official_research_source_count": len(research_observations),
        "official_research_retrieval_time_not_captured_count": len(research_observations),
        "autonomous_evolution_cycles_verified_count": 0,
        "ui_accessibility_mappings_verified_count": 0,
        "project_autoproject_preview_integrations_verified_count": 0,
        "remote_verified": False,
        "interpretation": "plan_and_candidate_inventory_only_not_implementation_or_execution_evidence",
    }
    plan: dict[str, Any] = {
        "schema_version": 1,
        "status": (
            "BLOCKED_SOURCE_RECONCILIATION"
            if missing_authoritative or not domains
            else "NEEDS_REVIEW"
        ),
        "source_scope": "materialized_local_only",
        "active_source_files": active_sources,
        "research": {
            "status": "OBSERVED_DATE_ONLY" if research_is_fresh else "STALE",
            "retrieved_date_utc": QVIRTUAL_LAB_RESEARCH_CAPTURED_DATE_UTC,
            "retrieved_at_utc": None,
            "retrieval_time_status": "NOT_CAPTURED",
            "freshness_deadline": QVIRTUAL_LAB_RESEARCH_FRESH_UNTIL,
            "collector_version": QVIRTUAL_LAB_RESEARCH_COLLECTOR,
            "observations": research_observations,
            "interpretation": "official capability documentation review_not_independent_benchmark_or_performance_validation",
        },
        "recommended_adapter_stack": {
            "architecture": "one bounded, auditable adapter contract with specialist solvers; no monolithic all-domain solver selected",
            "initial_pilot": "ngspice circuit reference case",
            "tool_candidates": list(QVIRTUAL_LAB_TOOL_RECOMMENDATIONS),
            "decision_basis": "domain fit from official documentation, implementation isolation, and a bounded first regression; not a comparative performance benchmark",
            "requirements_dependent": True,
        },
        "historical_reference": {
            **historical_source,
            "scope": "historical_snapshot_candidate",
            "not_authoritative": True,
        },
        "domains": domains,
        "requirements": requirements,
        "metrics": metrics,
        "blockers": blockers,
        "public_qengineer_probe": {
            "source_url": "https://raw.githubusercontent.com/thealphakenya/qmoi-enhanced/main/QENGINEER.md",
            "observed_http_status": 404,
            "status": "UNKNOWN_NOT_FOUND_OR_PRIVATE",
            "interpretation": "A public raw URL returning 404 without authenticated repository access cannot distinguish a missing path from a private repo, ref mismatch, or inaccessible source.",
            "retrieved_date_utc": QVIRTUAL_LAB_RESEARCH_CAPTURED_DATE_UTC,
            "retrieved_at_utc": None,
            "retrieval_time_status": "NOT_CAPTURED",
        },
        "next_action": (
            "Restore or identify the authoritative QENGINEER.md, reconcile every source requirement, "
            "then map owners, implementations, focused tests, simulation evidence, and physical-validation gates."
        ),
    }
    canonical = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode("utf-8")
    plan["plan_sha256"] = hashlib.sha256(canonical).hexdigest()
    return plan


def _file_evidence(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    if not path.is_file() or path.is_symlink():
        return {"path": relative, "status": "missing_or_unsafe", "bytes": None, "sha256": None}
    try:
        content = path.read_bytes()
        text = content.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return {
            "path": relative,
            "status": f"unavailable:{type(exc).__name__}",
            "bytes": None,
            "sha256": None,
        }
    if relative in QVIRTUAL_LAB_METRIC_DOCUMENTS:
        start_marker, end_marker = QVIRTUAL_LAB_METRIC_MARKERS
        start_count, end_count = text.count(start_marker), text.count(end_marker)
        if (start_count, end_count) not in {(0, 0), (1, 1)}:
            return {
                "path": relative,
                "status": "unavailable:invalid_qvirtual_managed_section",
                "bytes": None,
                "sha256": None,
            }
        if start_count:
            start = text.index(start_marker)
            end = text.index(end_marker, start) + len(end_marker)
            text = (text[:start] + text[end:]).rstrip() + "\n"
        content = text.encode("utf-8")
    return {
        "path": relative,
        "status": "observed_local",
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "hash_scope": (
            "authored_content_excluding_qvirtual_metrics"
            if relative in QVIRTUAL_LAB_METRIC_DOCUMENTS
            else "full_file"
        ),
    }


def build_asset_continuity_inventory(root: Path | str) -> dict[str, Any]:
    """Inventory explicit continuity source paths without claiming feature coverage."""
    source_root = Path(root).resolve()
    domains: dict[str, dict[str, Any]] = {}
    all_files: list[dict[str, Any]] = []
    for domain, contracts in ASSET_CONTINUITY_CONTRACTS.items():
        files = {
            kind: [_file_evidence(source_root, path) for path in paths]
            for kind, paths in contracts.items()
        }
        flattened = [item for group in files.values() for item in group]
        observed_count = sum(item["status"] == "observed_local" for item in flattened)
        missing_count = len(flattened) - observed_count
        domains[domain] = {
            "status": "CANDIDATE_DISCOVERY_ONLY",
            "files": files,
            "metrics": {
                "required_path_count": len(flattened),
                "observed_path_count": observed_count,
                "missing_or_unavailable_path_count": missing_count,
                "required_test_count": len(files["tests"]),
                "observed_test_count": sum(
                    item["status"] == "observed_local" for item in files["tests"]
                ),
                "remote_verified": False,
            },
        }
        all_files.extend(flattened)

    observed_count = sum(item["status"] == "observed_local" for item in all_files)
    missing_count = len(all_files) - observed_count
    inventory = {
        "schema_version": 1,
        "status": "CANDIDATE_DISCOVERY_ONLY",
        "source_scope": "explicit_local_contract_paths",
        "domains": domains,
        "metrics": {
            "required_domain_count": len(domains),
            "domain_count_with_all_paths_observed": sum(
                domain["metrics"]["missing_or_unavailable_path_count"] == 0
                for domain in domains.values()
            ),
            "required_path_count": len(all_files),
            "observed_path_count": observed_count,
            "missing_or_unavailable_path_count": missing_count,
            "remote_verified": False,
            "automatic_replacement_enabled": False,
            "financial_actions_authorized": False,
            "network_changes_authorized": False,
        },
        "limitations": [
            "path presence and hashes do not establish semantic completeness, implementation, test success, ownership, authorization, or synchronization",
            "file contents are not included; financial, wallet, banking, credential, and private project values are not inspected or recorded",
            "the fixed path list is a bounded local contract, not an exhaustive project, provider, repository, or remote-history census",
        ],
    }
    inventory["source_manifest_sha256"] = hashlib.sha256(
        json.dumps(all_files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return inventory


def build_evolution_plan(
    root: Path | str,
    *,
    source_manifest_sha256: str | None = None,
) -> dict[str, Any]:
    """Map existing governance contracts to planned gates without passing them."""
    source_root = Path(root).resolve()
    stages = []
    for sequence, (domain, paths) in enumerate(CONTRACTS, start=1):
        sources = [_file_evidence(source_root, relative) for relative in paths]
        stage_manifest = hashlib.sha256(
            json.dumps(sources, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        stages.append({
            "sequence": sequence,
            "domain": domain,
            "state": "PLANNED",
            "status": "PLANNED",
            "target_documents": list(PLAN_TARGETS.get(domain, ())),
            "source_files": sources,
            "source_sha256": stage_manifest,
            "metrics": {
                "source_manifest_sha256": source_manifest_sha256 or stage_manifest,
                "source_file_count": len(sources),
                "available_source_file_count": sum(item["status"] == "observed_local" for item in sources),
                "missing_or_unavailable_source_file_count": sum(item["status"] != "observed_local" for item in sources),
                "remote_verified": False,
            },
            "blockers": [
                "planned_only; implementation, tests, and semantic review are not inferred",
                "remote exact-SHA evidence is unavailable to this local planner",
            ],
        })

    serialized_stages = json.dumps(stages, sort_keys=True, separators=(",", ":")).encode("utf-8")
    plan_sha256 = hashlib.sha256(serialized_stages).hexdigest()
    manifest_for_plan = source_manifest_sha256 or plan_sha256
    qstats = {
        "stage_count": len(stages),
        "planned_stage_count": len(stages),
        "evolutiono_transition_stage_count": len(EVOLUTIONO_TRANSITION_DOMAINS),
        "evolutiono_transition_completed_stage_count": 0,
        "available_contract_file_count": sum(stage["metrics"]["available_source_file_count"] for stage in stages),
        "missing_or_unavailable_contract_file_count": sum(stage["metrics"]["missing_or_unavailable_source_file_count"] for stage in stages),
        "remote_verified_stage_count": 0,
        "source_manifest_sha256": manifest_for_plan,
        "interpretation": "derived_local_inventory_counts_not_completion_or_remote_proof",
    }
    evolutiono_transition = {
        "status": "PLANNED",
        "stage_domains": list(EVOLUTIONO_TRANSITION_DOMAINS),
        "planned_stage_count": len(EVOLUTIONO_TRANSITION_DOMAINS),
        "completed_stage_count": 0,
        "archive_branch": "qmoi",
        "archive_path_prefix": "qreplaceo/",
        "archive_optional_for_core_runtime": True,
        "automatic_mutation_enabled": False,
        "remote_verified": False,
        "ofca_target_document": "OFCA.md",
        "plan_sha256": plan_sha256,
    }
    return {
        "status": "PLANNED",
        "source_root": str(source_root),
        "source_manifest_sha256": manifest_for_plan,
        "source_scope": "materialized_local_only",
        "remote_verification_complete": False,
        "stages": stages,
        "qstats": qstats,
        "model_comparison": build_model_comparison_inventory(source_root),
        "asset_continuity": build_asset_continuity_inventory(source_root),
        "qvirtual_labs": build_qvirtual_labs_plan(
            source_root,
        ),
        "evolutiono_transition": evolutiono_transition,
        "plan_sha256": plan_sha256,
        "blockers": [
            "Plan entries are not execution results or production implementations.",
            "Remote completion requires authorized target-owned terminal exact-SHA and tree evidence.",
        ],
    }