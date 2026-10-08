import json
from pathlib import Path

from scripts.qaudit_all_features import build_feature_audit, run_parallel_feature_audit


def test_feature_audit_creates_stable_ids_and_provenance(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "qcity.py").write_text(
        "# QCity file manager\nFEATURE_ID = 'qcity-file-management'\n",
        encoding="utf-8",
    )
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_qcity.py").write_text(
        "def test_qcity_file_management():\n    assert True\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text(
        "QCity file manager and qcity-file-management\n",
        encoding="utf-8",
    )

    audit = build_feature_audit(
        tmp_path,
        registry={
            "qcity": {
                "name": "QCity",
                "features": {
                    "qcity-file-management": {
                        "description": "File manager",
                        "aliases": ["QCity file manager", "file manager"],
                    }
                },
            }
        },
    )

    feature = audit["features"]["qcity-file-management"]
    assert feature["feature_id"] == "qcity-file-management"
    assert feature["app_id"] == "qcity"
    assert feature["mention_count"] >= 2
    assert "README.md" in feature["mention_paths"]
    assert "src/qcity.py" in feature["implementation_paths"]
    assert "tests/test_qcity.py" in feature["test_paths"]
    assert feature["status"] == "MAPPED_LOCAL"
    assert feature["remote_verification"] is False
    assert feature["coverage_complete"] is False


def test_parallel_feature_audit_is_deterministic_and_hashes_artifacts(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "qalpha.py").write_text("QALPHA_FEATURE = True\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_qalpha.py").write_text("assert True\n", encoding="utf-8")

    first = run_parallel_feature_audit(repo, shard_size=1, worker_count=2)
    second = run_parallel_feature_audit(repo, shard_size=1, worker_count=2)

    assert first["status"] == "NEEDS_REVIEW"
    assert first["metrics"]["shard_count"] == 2
    assert first["metrics"]["files_scanned"] == 2
    assert first["metrics"]["remaining_feature_count"] >= 0
    assert first["metrics"]["feature_manifest_sha256"] == second["metrics"]["feature_manifest_sha256"]
    assert first["metrics"]["feature_evidence_sha256"] == second["metrics"]["feature_evidence_sha256"]

    manifest_path = first["artifacts"]["feature_manifest"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["schema_version"] == 1
    assert manifest["remote_verification_complete"] is False
    assert manifest["metrics"]["all_feature_ids_unique"] is True


def test_capability_aliases_are_ledgered_and_allfeatures_is_regenerated(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "qcity.py").write_text(
        "def manage_files(): return True\n",
        encoding="utf-8",
    )

    result = run_parallel_feature_audit(
        repo,
        shard_size=1,
        worker_count=1,
        registry={
            "qcity": {
                "name": "QCity",
                "features": {
                    "qcity-file-management": {
                        "description": "File manager",
                        "aliases": ["file manager", "manage files", "files"],
                    }
                },
            }
        },
    )

    manifest = json.loads(result["artifacts"]["feature_manifest"].read_text(encoding="utf-8"))
    assert manifest["capability_catalog"]["file-management"]
    assert "file-manager" in manifest["capability_catalog"]
    assert "manage-files" in manifest["capability_catalog"]
    assert result["artifacts"]["all_features"]
    all_features = result["artifacts"]["all_features"].read_text(encoding="utf-8")
    assert "## Capability catalog" in all_features
    assert "QCity" in all_features
    assert "file-manager" in all_features
    assert manifest["metrics"]["capability_count"] == len(manifest["capability_catalog"])
