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
    ("repository_surface_audit", ("QAUDITS.md", "OFCA.md")),
    ("markdown_refresh", ("ALLMDFILESREFS.md", "TRANSION.md", "TRANSITION.md")),
    ("production_gate", ("production.md", "productionenhanced.md")),
    ("validation", ("ALLVALIDATIONS.md",)),
    ("remote_verification", ("remotecompletion.md", "remote-completion.json")),
)


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
    qstats = {
        "stage_count": len(stages),
        "planned_stage_count": len(stages),
        "available_contract_file_count": sum(stage["metrics"]["available_source_file_count"] for stage in stages),
        "missing_or_unavailable_contract_file_count": sum(stage["metrics"]["missing_or_unavailable_source_file_count"] for stage in stages),
        "remote_verified_stage_count": 0,
        "source_manifest_sha256": source_manifest_sha256,
        "interpretation": "derived_local_inventory_counts_not_completion_or_remote_proof",
    }
    return {
        "status": "PLANNED",
        "source_root": str(source_root),
        "source_manifest_sha256": source_manifest_sha256,
        "source_scope": "materialized_local_only",
        "remote_verification_complete": False,
        "stages": stages,
        "qstats": qstats,
        "plan_sha256": plan_sha256,
        "blockers": [
            "Plan entries are not execution results or production implementations.",
            "Remote completion requires authorized target-owned terminal exact-SHA and tree evidence.",
        ],
    }