from __future__ import annotations

import hashlib
import json

from scripts.qaudits_evolution_planner import build_evolution_plan


def test_build_evolution_plan_discovers_contracts_and_is_deterministic(tmp_path):
    contract_files = {
        "AUTODEV.md": "# Autodev\n\nremote-continuity-and-failover\n",
        "MODELEVUTIONO.md": "# Model evolution\n\nmodel evolution\n",
        "Qvillageevolutions.md": "# QVillage evolution\n\nmodel and memory lifecycle\n",
        "INTERNALRESEARCH.md": "# Internal research\n\nrepository surface audit\n",
        "EXTERNALRESEARCH.md": "# External research\n\nofficial guidance\n",
        "QSEED.md": "# QSeed\n\nseed lineage\n",
        "QVERSIONMANAGER.md": "# Q version manager\n\nQ_VERSION_FINALIZATION\n",
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
    }
    assert all(stage["source_sha256"] for stage in first["stages"])
    assert all(stage["state"] == "PLANNED" for stage in first["stages"])
    assert all(stage["metrics"]["source_manifest_sha256"] == "manifest-a" for stage in first["stages"])
