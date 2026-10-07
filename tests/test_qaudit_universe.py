import hashlib
import json
from pathlib import Path

from scripts.qaudit_universe import (
    build_audit_priority_queue,
    build_qaudit_universe,
    classify_entity,
    render_style_universal_candidate_tree,
    write_qaudit_artifacts,
)


def test_qaudit_universe_covers_style_universal_and_audit_objects(tmp_path: Path) -> None:
    (tmp_path / "styles").mkdir()
    (tmp_path / "styles" / "button.css").write_text(".button { color: #fff; }\n", encoding="utf-8")
    (tmp_path / "UNIVERSALS.md").write_text("# Universal capabilities\n- authentication\n", encoding="utf-8")
    (tmp_path / "QAUDITS.md").write_text("# Audit contract\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "consumer.py").write_text("from styles.button import Button\n", encoding="utf-8")

    universe = build_qaudit_universe(tmp_path)

    assert universe["discovery"]["files_scanned"] >= 4
    assert universe["inventory"]["styles"]
    assert universe["inventory"]["universals"]
    assert universe["inventory"]["audit"]
    assert universe["dependency_graph"]["edges"]
    assert universe["classes"]["styles/button.css"]["classification"] == "style_candidate"
    assert universe["classes"]["UNIVERSALS.md"]["classification"] == "canonical_universal_specification"
    assert universe["classes"]["QAUDITS.md"]["classification"] == "canonical_audit_specification"
    assert universe["classes"]["docs/consumer.py"]["dependencies"] == ["styles/button.css"]
    assert universe["classes"]["styles/button.css"]["consumers"] == ["docs/consumer.py"]
    assert universe["evidence"]["source_scope"] == "materialized_local"
    assert universe["evidence"]["remote_verification_complete"] is False
    assert "Category ALL" in universe["classes"]["UNIVERSALS.md"]["categories"]
    assert "universal" in universe["classes"]["UNIVERSALS.md"]["categories"]
    assert "Category D — Product applications, feature surfaces, and UI experience" in universe["classes"]["UNIVERSALS.md"]["categories"]
    assert universe["metrics"]["remote_verified_candidate_count"] == 0
    assert len(universe["metrics"]["source_manifest_sha256"]) == 64
    assert universe["metrics"]["total_duration_seconds"] > 0
    assert universe["metrics"]["dependency_edge_count"] == len(universe["dependency_graph"]["edges"])
    assert universe["metrics"]["files_with_parsed_content_count"] == universe["discovery"]["files_scanned"]
    assert "styles/button.css" in render_style_universal_candidate_tree(universe)
    assert universe["metrics"]["source_manifest_sha256"] == build_qaudit_universe(tmp_path)["metrics"]["source_manifest_sha256"]


def test_classify_entity_records_legacy_and_platform_override_status() -> None:
    assert classify_entity("legacy.css", "style") == {
        "classification": "legacy_style_candidate",
        "canonical_status": "unknown",
        "action": "investigate_and_test_before_migration",
        "confidence": "low",
    }
    assert classify_entity("web/auth.py", "universal") == {
        "classification": "platform_specific_universal_candidate",
        "canonical_status": "platform_override",
        "action": "verify_platform_boundary_and_access_contract",
        "confidence": "medium",
    }


def test_qaudit_universe_tracks_product_delivery_and_accountability_domains(tmp_path: Path) -> None:
    (tmp_path / "apps").mkdir()
    (tmp_path / "apps" / "qcity.py").write_text("# QCity product source\n", encoding="utf-8")
    (tmp_path / "platforms" / "web").mkdir(parents=True)
    (tmp_path / "platforms" / "web" / "install.js").write_text("// web install workflow\n", encoding="utf-8")
    (tmp_path / "releases").mkdir()
    (tmp_path / "releases" / "publish_release.yml").write_text("name: build tag publish download deploy\n", encoding="utf-8")
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "ACCOUNTABILITY.md").write_text("# QMOI accountability to master\n", encoding="utf-8")
    (tmp_path / "docs" / "QTEAM.md").write_text("# QTeam friendship process\n", encoding="utf-8")
    historical_lion = tmp_path / "qmoi-enhanced-history-14" / "docs" / "lion_variations" / "lion-cloud.md"
    historical_lion.parent.mkdir(parents=True)
    historical_lion.write_text("# Lion Cloud variation\nExtension install and release notes.\n", encoding="utf-8")
    historical_style = tmp_path / "Alpha-Q-ai-2025" / "styles" / "legacy.css"
    historical_style.parent.mkdir(parents=True)
    historical_style.write_text("/* historical style candidate */\n", encoding="utf-8")

    universe = build_qaudit_universe(
        tmp_path,
        product_registry={
            "applications": {"qcity": {"name": "QCity", "category": "file-management"}, "qalpha": {"name": "QAlpha"}},
            "platforms": ["web", "linux"],
        },
    )
    accountability = universe["accountability"]

    assert accountability["status"] == "NEEDS_REVIEW"
    assert accountability["coverage_complete"] is False
    assert accountability["remote_verification_complete"] is False
    assert accountability["registered_application_count"] == 2
    assert accountability["applications"][0]["implementation_status"] == "not_verified"
    assert accountability["registered_platform_count"] == 2
    assert accountability["lion_variation_candidate_count"] == 1
    assert accountability["lion_variation_candidates"][0]["scope"] == "historical_snapshot"
    assert universe["classes"]["Alpha-Q-ai-2025/styles/legacy.css"]["scope"] == "historical_snapshot"
    assert accountability["extension_candidate_count"] >= 1
    assert accountability["extension_file_types"][".py"]["file_count"] >= 1
    assert accountability["delivery_stages"]["release"]["candidate_file_count"] >= 1
    assert accountability["delivery_stages"]["tag"]["candidate_file_count"] >= 1
    assert accountability["delivery_stages"]["download"]["candidate_file_count"] >= 1
    assert accountability["delivery_stages"]["install"]["candidate_file_count"] >= 1
    assert accountability["delivery_stages"]["deploy"]["candidate_file_count"] >= 1
    assert accountability["governance_domains"]["qteam"]["candidate_file_count"] >= 1
    assert accountability["governance_domains"]["friendship"]["candidate_file_count"] >= 1
    assert accountability["governance_domains"]["accountability"]["candidate_file_count"] >= 1
    assert accountability["governance_domains"]["master"]["candidate_file_count"] >= 1
    assert len(accountability["source_manifest_sha256"]) == 64


def test_qaudit_artifacts_include_tree_hash_and_fail_closed_source_counts(tmp_path: Path) -> None:
    (tmp_path / "styles").mkdir()
    (tmp_path / "styles" / "base.css").write_text("body { color: black; }\n", encoding="utf-8")

    universe = write_qaudit_artifacts(tmp_path)

    tree = tmp_path / "QMOItracks" / "style_universal_candidate_tree.md"
    manifest = tmp_path / "ollamatracks" / "qaudit_universe.json"
    assert tree.is_file()
    assert manifest.is_file()
    assert universe["artifacts"]["candidate_tree_markdown"] == "QMOItracks/style_universal_candidate_tree.md"
    assert universe["artifacts"]["candidate_tree_sha256"] == hashlib.sha256(tree.read_bytes()).hexdigest()
    persisted = json.loads(manifest.read_text(encoding="utf-8"))
    assert persisted["schema_version"] == 3
    assert persisted["artifacts"] == universe["artifacts"]
    assert persisted["metrics"]["test_mapped_candidate_count"] == 0
    assert persisted["metrics"]["hook_reviewed_candidate_count"] == 0
    assert persisted["inventory"]["styles"] == ["styles/base.css"]
    assert "all_entities" not in persisted["inventory"]
    assert "edges" not in persisted["dependency_graph"]
    assert persisted["dependency_graph"]["edge_count"] == len(universe["dependency_graph"]["edges"])
    assert persisted["classes"]["styles/base.css"]["sha256"] == universe["classes"]["styles/base.css"]["sha256"]


def test_audit_priority_queue_ranks_risk_and_keeps_every_path() -> None:
    records = [
        {
            "path": "docs/README.md",
            "sha256": "a" * 64,
            "scope": "materialized_repository",
            "categories": [],
            "content_scan_status": "scanned",
            "test_mapping_status": "unmapped",
            "hook_applicability": "review_required",
        },
        {
            "path": "payments/transfer.py",
            "sha256": "b" * 64,
            "scope": "materialized_repository",
            "categories": ["finance_qtrade"],
            "content_scan_status": "scanned",
            "test_mapping_status": "unmapped",
            "hook_applicability": "review_required",
        },
        {
            "path": "src/auth.py",
            "sha256": "c" * 64,
            "scope": "materialized_repository",
            "categories": ["security"],
            "content_scan_status": "scanned",
            "test_mapping_status": "mapped",
            "hook_applicability": "reviewed",
        },
        {
            "path": "src/unreadable.py",
            "sha256": None,
            "scope": "materialized_repository",
            "categories": [],
            "content_scan_status": "unreadable_hash",
            "test_mapping_status": "unmapped",
            "hook_applicability": "review_required",
        },
    ]

    queue = build_audit_priority_queue(records, "manifest")

    assert queue["all_indexed_paths_queued"] is True
    assert queue["model_assistance"] == "not_used_for_selection_or_status"
    assert queue["candidate_count"] == len(records)
    assert [item["path"] for item in queue["items"]] == [
        "src/unreadable.py",
        "src/auth.py",
        "payments/transfer.py",
        "docs/README.md",
    ]
    assert queue["items"][0]["priority"] == 120
    assert queue["items"][1]["priority"] == 100
    assert queue["items"][2]["priority"] == 95
    assert all(item["status"] == "pending_review" for item in queue["items"])
    assert queue["queue_sha256"] == build_audit_priority_queue(records, "manifest")["queue_sha256"]


def test_qaudit_hashes_large_files_but_marks_content_as_unparsed(tmp_path: Path) -> None:
    large = tmp_path / "docs" / "large-audit.md"
    large.parent.mkdir()
    large.write_bytes(b"# large audit\n" + b"x" * 1_000_001)

    universe = build_qaudit_universe(tmp_path)

    record = universe["classes"]["docs/large-audit.md"]
    assert len(record["sha256"]) == 64
    assert record["content_scan_status"] == "oversized_content_not_parsed"
    assert universe["metrics"]["content_parse_skipped_count"] == 1
    assert universe["discovery"]["status"] == "NEEDS_REVIEW"


def test_qaudit_excludes_and_reports_mutable_evidence_outputs(tmp_path: Path) -> None:
    evidence = tmp_path / "remote-evidence-ledger.jsonl"
    evidence.write_text('{"event":"first"}\n', encoding="utf-8")

    first = build_qaudit_universe(tmp_path)
    evidence.write_text('{"event":"updated"}\n', encoding="utf-8")
    second = build_qaudit_universe(tmp_path)

    assert "remote-evidence-ledger.jsonl" in first["discovery"]["excluded_files"]
    assert first["metrics"]["excluded_file_count"] == 1
    assert "remote-evidence-ledger.jsonl" not in first["classes"]
    assert first["metrics"]["source_manifest_sha256"] == second["metrics"]["source_manifest_sha256"]
