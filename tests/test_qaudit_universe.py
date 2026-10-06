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
