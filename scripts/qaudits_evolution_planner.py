"""Build a deterministic, local-only QAUDITS evolution plan."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


CONTRACTS = (
    ("autodev", ("AUTODEV.md",)),
    ("model_evolution", ("MODELEVOLUTIONO.md", "MODELEVUTIONO.md")),
    ("qvillage_evolution", ("Qvillageevolutions.md",)),
    ("internal_research", ("INTERNALRESEARCH.md",)),
    ("external_research", ("EXTERNALRESEARCH.md", "EXTERIORRESEARCH.md")),
    ("q_seed", ("QSEED.md",)),
    ("q_version", ("QVERSIONMANAGER.md",)),
    ("instruction_inventory", ("AGENTS.md", ".github/copilot-instructions.md")),
    ("repository_surface_audit", ("scripts/qaudit_universe.py", "scripts/ollama_research.py")),
    ("markdown_refresh", ("ALLMDFILESREFS.md", "TRANSION.md", "TRANSITION.md")),
    ("production_gate", ("production.md", "productionenhanced.md")),
    ("validation", ("ALLVALIDATIONS.md",)),
    ("remote_verification", ("remotecompletion.md", "remote-completion.json")),
    ("evolutiono_pre_retirement", ("MODELEVOLUTIONO.md", "scripts/q_version_manager.py", "AUTODEV.md")),
    ("qmoi_capability_parity", ("AUTODEV.md", "ALLFEATURES.md", "ALLTESTSAUTOTESTS.md")),
    ("qreplaceo_archive", ("SYNC.md", "MODELEVOLUTIONO.md")),
    ("evolutiono_clean_branch_audit", ("SYNC.md", "scripts/qaudit_universe.py", "scripts/qaudits_evolution_planner.py")),
    ("evolutiono_ofca_metrics", ("MODELEVOLUTIONO.md", "scripts/qaudits_evolution_planner.py", "scripts/q_version_manager.py")),
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
    "evolutiono_ofca_metrics": ("OFCA.md",),
}


def _file_evidence(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    if not path.is_file() or path.is_symlink():
        return {"path": relative, "status": "missing_or_unsafe", "bytes": None, "sha256": None}
    try:
        content = path.read_bytes()
        content.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return {
            "path": relative,
            "status": f"unavailable:{type(exc).__name__}",
            "bytes": None,
            "sha256": None,
        }
    return {
        "path": relative,
        "status": "observed_local",
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


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
        "evolutiono_transition": evolutiono_transition,
        "plan_sha256": plan_sha256,
        "blockers": [
            "Plan entries are not execution results or production implementations.",
            "Remote completion requires authorized target-owned terminal exact-SHA and tree evidence.",
        ],
    }