from scripts.language_strategy import (
    aggregate_language_counts,
    classify_language,
    language_inventory,
    recommend_languages,
)


def test_language_inventory_counts_source_paths_once_and_marks_unknowns() -> None:
    paths = ["api/main.py", "ui/App.tsx", "core/lib.rs", "generated/data.unknown"]

    result = language_inventory(paths)

    assert result["file_count"] == 4
    assert result["language_counts"] == {
        "Python": 1,
        "Rust": 1,
        "TypeScript": 1,
        "unclassified": 1,
    }
    assert result["unclassified_file_count"] == 1
    assert result["catalog_coverage_complete_for_all_languages"] is False


def test_language_classification_is_case_insensitive_and_conservative() -> None:
    assert classify_language("src/MAIN.PY") == "Python"
    assert classify_language("include/shared.h") == "C/C++"
    assert classify_language("src/unknown.xyz") == "unclassified"
    assert aggregate_language_counts(["a.py", "b.py", "c.rs"]) == {
        "Python": 2,
        "Rust": 1,
    }


def test_task_fit_advice_prefers_safe_systems_candidates_without_authorizing_migration() -> None:
    result = recommend_languages(
        ["security", "systems"],
        available_languages=["Python"],
    )

    assert result["recommendations"][0]["language"] == "Rust"
    assert result["recommendations"][0]["matched_domains"] == ["security", "systems"]
    assert result["migration_recommended"] is False
    assert result["remote_research_verified"] is False


def test_language_advice_reports_unknown_domains_instead_of_guessing() -> None:
    result = recommend_languages(["quantum-entanglement"])

    assert result["recommendations"] == []
    assert result["unknown_task_domains"] == ["quantum-entanglement"]
