from pathlib import Path

from scripts.qaudit_universe import build_qaudit_universe, classify_entity


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
