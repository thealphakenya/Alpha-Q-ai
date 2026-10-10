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


def test_feature_audit_normalizes_each_source_file_once(tmp_path: Path, monkeypatch) -> None:
    import scripts.qaudit_all_features as auditor

    source = "QCity file management and QAlpha data export"
    (tmp_path / "README.md").write_text(source, encoding="utf-8")
    normalize = auditor._normalize
    source_normalizations = 0

    def count_source_normalizations(value: str) -> str:
        nonlocal source_normalizations
        if value == source.lower():
            source_normalizations += 1
        return normalize(value)

    monkeypatch.setattr(auditor, "_normalize", count_source_normalizations)
    auditor.build_feature_audit(
        tmp_path,
        registry={
            "qcity": {
                "name": "QCity",
                "features": {
                    "qcity-file-management": {
                        "description": "File management",
                        "aliases": ["file manager"],
                    }
                },
            },
            "qalpha": {
                "name": "QAlpha",
                "features": {
                    "qalpha-data-export": {
                        "description": "Data export",
                        "aliases": ["export data"],
                    }
                },
            },
        },
    )

    assert source_normalizations == 1


def test_read_source_hashes_the_bytes_already_read(tmp_path: Path, monkeypatch) -> None:
    import hashlib
    import scripts.qaudit_all_features as auditor

    source = b"QCity file management\n"
    path = tmp_path / "README.md"
    path.write_bytes(source)

    def reject_second_read(_path: Path) -> str:
        raise AssertionError("source hash must reuse the bytes already read")

    monkeypatch.setattr(auditor, "_hash_file", reject_second_read)
    content, digest, size = auditor._read_source(path, tmp_path)

    assert content == source.decode("utf-8")
    assert digest == hashlib.sha256(source).hexdigest()
    assert size == len(source)


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


def test_parallel_feature_audit_reads_each_source_once(tmp_path: Path, monkeypatch) -> None:
    import scripts.qaudit_all_features as auditor

    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "app.py").write_text("QCity file manager\n", encoding="utf-8")
    (repo / "tests").mkdir()
    (repo / "tests" / "test_app.py").write_text("def test_qcity(): pass\n", encoding="utf-8")
    read_source = auditor._read_source
    reads: dict[str, int] = {}

    def count_reads(path: Path, root: Path):
        relative = path.relative_to(root).as_posix()
        reads[relative] = reads.get(relative, 0) + 1
        return read_source(path, root)

    monkeypatch.setattr(auditor, "_read_source", count_reads)
    auditor.run_parallel_feature_audit(
        repo,
        shard_size=1,
        worker_count=2,
        registry={
            "qcity": {
                "name": "QCity",
                "features": {
                    "qcity-file-management": {
                        "description": "File manager",
                        "aliases": ["QCity file manager"],
                    }
                },
            }
        },
    )

    assert reads == {"src/app.py": 1, "tests/test_app.py": 1}


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
    assert result["metrics"]["capability_count"] == manifest["metrics"]["capability_count"]
    all_features = result["artifacts"]["all_features"].read_text(encoding="utf-8")
    assert "## Capability catalog" in all_features
    assert "QCity" in all_features
    assert "file-manager" in all_features
    assert manifest["metrics"]["capability_count"] == len(manifest["capability_catalog"])
