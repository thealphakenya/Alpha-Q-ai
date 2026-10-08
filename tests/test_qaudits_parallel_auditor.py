import json
from pathlib import Path

from scripts.qaudits_parallel_auditor import (
    build_merge_operating_contract,
    run_parallel_merge_audit,
)


def test_parallel_merge_audit_shards_large_repository_and_preserves_evidence(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    for index in range(12):
        path = repo / "src" / f"module_{index}.py"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            f"# module {index}\nMERGE_TARGET = True\n"
            if index % 2 == 0
            else f"# module {index}\n",
            encoding="utf-8",
        )
    (repo / "production.md").write_text("# production\n", encoding="utf-8")
    (repo / "productionenhanced.md").write_text("# enhanced\n", encoding="utf-8")

    result = run_parallel_merge_audit(repo, shard_size=3, worker_count=2)

    assert result["status"] == "NEEDS_REVIEW"
    assert result["remote_verification_complete"] is False
    assert result["metrics"]["shard_count"] == 5
    assert result["metrics"]["files_scanned"] == 14
    assert result["metrics"]["merge_candidate_count"] >= 6
    assert result["metrics"]["production_candidate_count"] >= 0
    assert result["artifacts"]["merge_manifest"].is_file()
    assert result["artifacts"]["production_inventory"].is_file()
    assert result["artifacts"]["operating_contract"].is_file()
    manifest = json.loads(result["artifacts"]["merge_manifest"].read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert len(manifest["shards"]) == 5
    assert all(shard["status"] == "complete" for shard in manifest["shards"])
    assert result["metrics"]["merge_manifest_sha256"]
    assert result["metrics"]["production_inventory_sha256"]
    assert result["metrics"]["operating_contract_sha256"]


def test_merge_operating_contract_includes_safe_merge_steps_and_metrics() -> None:
    contract = build_merge_operating_contract(
        roots=[Path("/repo")],
        merge_candidate_count=4,
        production_candidate_count=2,
        remote_verified=False,
    )

    assert contract["merge_mode"] == "canonical_evidence_and_preserve"
    assert contract["safe_merge_sequence"]
    assert "source_sha" in contract["required_evidence"]
    assert "target_sha" in contract["required_evidence"]
    assert contract["metrics"]["merge_candidate_count"] == 4
    assert contract["metrics"]["production_candidate_count"] == 2
    assert contract["remote_verification_complete"] is False
