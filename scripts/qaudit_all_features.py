#!/usr/bin/env python3
"""Feature-wide, evidence-first QAUDITS for application and platform features.

Discovery and provenance are intentionally separate from implementation proof.
A feature is never marked complete solely because its name appears in a document,
path, test, or registry.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

EXCLUDED_DIRECTORIES = {
    ".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist", "build", "target",
    "coverage", ".cache", "ollamatracks", "QMOItracks",
}
EXCLUDED_FILES = {
    "remote-evidence-ledger.jsonl",
    "remote-completion.json",
    "qaudit_all_features.json",
    "feature_manifest.json",
    "feature_evidence.json",
    "ALLFEATURES.md",
}


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _discover_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, directories, filenames in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        retained: list[str] = []
        for directory in sorted(directories):
            directory_path = current_path / directory
            relative = _relative(directory_path, root)
            if directory in EXCLUDED_DIRECTORIES or directory_path.is_symlink():
                continue
            retained.append(directory)
        directories[:] = retained
        for filename in sorted(filenames):
            path = current_path / filename
            if path.is_symlink() or Path(filename).name in EXCLUDED_FILES:
                continue
            relative = _relative(path, root)
            if any(part in EXCLUDED_DIRECTORIES for part in Path(relative).parts):
                continue
            files.append(path)
    return sorted(files, key=lambda path: _relative(path, root))


def _read_source(path: Path, root: Path) -> tuple[str, str, int]:
    try:
        content = path.read_bytes()
        return (
            content.decode("utf-8", errors="replace"),
            hashlib.sha256(content).hexdigest(),
            len(content),
        )
    except OSError:
        return "", "", 0


def _scan_shard(
    root: Path,
    paths: list[Path],
    shard_number: int,
    registry: dict[str, Any],
) -> dict[str, Any]:
    """Scan one bounded shard and return only path/hash/provenance metadata."""
    feature_map = _registry_features(registry)
    feature_search = _feature_search_index(feature_map)
    results: list[dict[str, Any]] = []
    for path in paths:
        relative = _relative(path, root)
        content, digest, size = _read_source(path, root)
        if not digest:
            results.append({"path": relative, "status": "SKIPPED", "reason": "unreadable"})
            continue
        lower = content.lower()
        normalized_lower = _normalize(lower)
        path_parts = {part.lower() for part in Path(relative).parts}
        mention_matches: dict[str, list[str]] = {}
        implementation_features: list[str] = []
        test_features: list[str] = []
        setup_features: list[str] = []
        for feature_id, search in feature_search.items():
            matched = [term for term in search["mention_terms"] if term in lower]
            if matched:
                mention_matches[feature_id] = matched
            if any(term and term in normalized_lower for term in search["normalized_terms"]):
                implementation_features.append(feature_id)
            if feature_id in lower or feature_id.replace("-", "_") in lower:
                if feature_id not in implementation_features:
                    implementation_features.append(feature_id)
            if ("test" in path_parts or "tests" in path_parts) and (
                search["app_term"] in lower
                or any(term in lower for term in search["test_setup_terms"])
            ):
                test_features.append(feature_id)
            if any(part in {"setup", "config", "configs", "workflows", "scripts"} for part in path_parts) and (
                search["app_term"] in lower
                or any(term in lower for term in search["test_setup_terms"])
            ):
                setup_features.append(feature_id)
        evidence = {
            "path": relative,
            "sha256": digest,
            "bytes": size,
            "status": "SCANNED",
            "feature_mentions": sorted(mention_matches),
            "mention_matches": mention_matches,
            "implementation_features": sorted(implementation_features),
            "test_features": sorted(test_features),
            "setup_or_configuration_features": sorted(setup_features),
            "implementation": bool(implementation_features),
            "test": "test" in path_parts or "tests" in path_parts,
            "setup_or_config": any(part in {"setup", "config", "configs", "workflows", "scripts"} for part in path_parts),
        }
        results.append(evidence)
    return {
        "number": shard_number,
        "status": "complete",
        "file_count": len(paths),
        "records": results,
    }


def _shard_paths(paths: Iterable[Path], shard_size: int) -> list[list[Path]]:
    size = max(1, shard_size)
    return [list(paths)[index:index + size] for index in range(0, len(list(paths)), size)]


def _registry_features(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    feature_map: dict[str, dict[str, Any]] = {}
    for app_id, metadata in registry.items():
        for feature_id, feature_metadata in metadata.get("features", {}).items():
            feature_map[feature_id] = {
                "app_id": app_id,
                "application_name": str(metadata.get("name", app_id)),
                "name": str(feature_metadata.get("name", feature_id)),
                "description": str(feature_metadata.get("description", "")),
                "aliases": list(feature_metadata.get("aliases", [])),
            }
    return feature_map


def _feature_search_index(feature_map: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    search_index = {}
    for feature_id, metadata in feature_map.items():
        terms = [feature_id, metadata["name"], metadata["description"], *metadata["aliases"]]
        search_index[feature_id] = {
            "mention_terms": [str(term).lower() for term in terms if term],
            "normalized_terms": [_normalize(term) for term in terms],
            "app_term": metadata["app_id"].lower(),
            "test_setup_terms": [
                feature_id,
                metadata["name"].lower(),
                *[str(alias).lower() for alias in metadata["aliases"]],
            ],
        }
    return search_index


def _capability_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(value).lower()).strip("-")


def _build_capability_catalog(
    feature_map: dict[str, dict[str, Any]],
    features: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Keep canonical feature IDs and every synonym as a deterministic ledger row."""
    catalog: dict[str, dict[str, Any]] = {}
    for feature_id, metadata in sorted(feature_map.items()):
        normalized_feature = _capability_key(feature_id.split("-", 1)[-1])
        entries = [
            (normalized_feature, feature_id),
            (_capability_key(metadata["name"]), feature_id),
            (_capability_key(metadata["description"]), feature_id),
        ]
        entries.extend((_capability_key(alias), feature_id) for alias in metadata["aliases"])
        for capability, canonical_feature_id in entries:
            if not capability:
                continue
            catalog.setdefault(capability, {
                "feature_id": canonical_feature_id,
                "app_id": metadata["app_id"],
                "application_name": metadata["application_name"],
                "canonical_name": metadata["name"],
                "source_ids": [],
                "evidence_paths": [],
                "status": "NEEDS_REVIEW",
            })
            entry = catalog[capability]
            entry["feature_id"] = canonical_feature_id
            entry["app_id"] = metadata["app_id"]
            entry["application_name"] = metadata["application_name"]
            entry["canonical_name"] = metadata["name"]
            if canonical_feature_id not in entry["source_ids"]:
                entry["source_ids"].append(canonical_feature_id)
            feature = features.get(canonical_feature_id, {})
            entry["evidence_paths"] = sorted(
                set(entry["evidence_paths"])
                | set(feature.get("mention_paths", []))
                | set(feature.get("implementation_paths", []))
                | set(feature.get("test_paths", []))
                | set(feature.get("setup_or_configuration_paths", []))
            )
            entry["status"] = feature.get("status", "NEEDS_REVIEW")
    return dict(sorted(catalog.items()))


def _render_all_features(
    root: Path,
    feature_map: dict[str, dict[str, Any]],
    features: dict[str, dict[str, Any]],
    capability_catalog: dict[str, dict[str, Any]],
    metrics: dict[str, Any],
) -> str:
    lines = [
        "# ALLFEATURES",
        "",
        "## Capability catalog",
        "",
        f"- Source root: `{root}`",
        f"- Registered capability records: {len(capability_catalog)}",
        f"- Canonical feature records: {len(features)}",
        f"- Registry feature IDs unique: {metrics['feature_ids_unique']}",
        f"- Remote verification complete: False",
        "",
    ]
    for capability, entry in capability_catalog.items():
        lines.extend([
            f"### `{capability}`",
            "",
            f"- Canonical feature: `{entry['feature_id']}`",
            f"- App: `{entry['app_id']}`",
            f"- Application name: `{entry['application_name']}`",
            f"- Canonical feature name: `{entry['canonical_name']}`",
            f"- Status: `{entry['status']}`",
            f"- Evidence paths: `{', '.join(entry['evidence_paths']) or 'none'}`",
            "",
        ])
    lines.extend([
        "## Canonical feature ledger",
        "",
    ])
    for feature_id, feature in sorted(features.items()):
        lines.extend([
            f"### `{feature_id}`",
            "",
            f"- Name: `{feature['name']}`",
            f"- Description: `{feature['description']}`",
            f"- Aliases: `{', '.join(feature['aliases']) or 'none'}`",
            f"- Mentions: {feature['mention_count']}",
            f"- Implementation paths: `{', '.join(feature['implementation_paths']) or 'none'}`",
            f"- Test paths: `{', '.join(feature['test_paths']) or 'none'}`",
            f"- Setup/configuration paths: `{', '.join(feature['setup_or_configuration_paths']) or 'none'}`",
            f"- Status: `{feature['status']}`",
            f"- Remote verification: `{feature['remote_verification']}`",
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"


def build_feature_audit(
    root: Path | str,
    registry: dict[str, Any] | None = None,
    *,
    scanned_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build a candidate feature ledger from a local tree and explicit registry."""
    source_root = Path(root).resolve()
    registry = registry or {}
    files = _discover_files(source_root)
    feature_map = _registry_features(registry)
    feature_search = {}
    for feature_id, metadata in feature_map.items():
        terms = [feature_id, metadata["name"], metadata["description"], *metadata["aliases"]]
        feature_search[feature_id] = {
            "mention_terms": [str(term).lower() for term in terms if term],
            "normalized_terms": [_normalize(term) for term in terms],
            "app_term": metadata["app_id"].lower(),
            "test_setup_terms": [
                feature_id,
                metadata["name"].lower(),
                *[str(alias).lower() for alias in metadata["aliases"]],
            ],
        }
    all_paths = {path.relative_to(source_root).as_posix(): path for path in files}
    features: dict[str, dict[str, Any]] = {}
    mentions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    implementation_paths: dict[str, set[str]] = defaultdict(set)
    test_paths: dict[str, set[str]] = defaultdict(set)
    setup_paths: dict[str, set[str]] = defaultdict(set)
    skipped: list[dict[str, str]] = []
    records_by_path = {
        record.get("path"): record
        for record in scanned_records or []
        if isinstance(record, dict) and isinstance(record.get("path"), str)
    }

    for path in files:
        relative = _relative(path, source_root)
        if scanned_records is not None:
            record = records_by_path.get(relative)
            if not record or record.get("status") != "SCANNED" or not record.get("sha256"):
                skipped.append({"path": relative, "reason": "missing_or_unreadable_shard_record"})
                continue
            digest = record["sha256"]
            size = record.get("bytes", 0)
            for feature_id, matched in record.get("mention_matches", {}).items():
                if feature_id in feature_map and matched:
                    mentions[feature_id].append({
                        "path": relative,
                        "sha256": digest,
                        "bytes": size,
                        "matched_terms": matched,
                    })
            for feature_id in record.get("implementation_features", []):
                if feature_id in feature_map:
                    implementation_paths[feature_id].add(relative)
            for feature_id in record.get("test_features", []):
                if feature_id in feature_map:
                    test_paths[feature_id].add(relative)
            for feature_id in record.get("setup_or_configuration_features", []):
                if feature_id in feature_map:
                    setup_paths[feature_id].add(relative)
            continue

        content, digest, size = _read_source(path, source_root)
        if not digest:
            skipped.append({"path": relative, "reason": "unreadable"})
            continue
        lower = content.lower()
        normalized_lower = _normalize(lower)
        path_parts = {part.lower() for part in Path(relative).parts}
        for feature_id, metadata in feature_map.items():
            search = feature_search[feature_id]
            normalized_terms = search["mention_terms"]
            matched = [term for term in normalized_terms if term in lower]
            if matched:
                mentions[feature_id].append({
                    "path": relative,
                    "sha256": digest,
                    "bytes": size,
                    "matched_terms": matched,
                })
            if any(term and term in normalized_lower for term in search["normalized_terms"]):
                implementation_paths[feature_id].add(relative)
        for feature_id in feature_map:
            if feature_id in lower or feature_id.replace("-", "_") in lower:
                implementation_paths[feature_id].add(relative)
        for feature_id, metadata in feature_map.items():
            search = feature_search[feature_id]
            if ("test" in path_parts or "tests" in path_parts) and (
                search["app_term"] in lower
                or any(term in lower for term in search["test_setup_terms"])
            ):
                test_paths[feature_id].add(relative)
            if any(part in {"setup", "config", "configs", "workflows", "scripts"} for part in path_parts) and (
                search["app_term"] in lower
                or any(term in lower for term in search["test_setup_terms"])
            ):
                setup_paths[feature_id].add(relative)

    for feature_id, metadata in sorted(feature_map.items()):
        feature_mentions = mentions.get(feature_id, [])
        implementation = sorted(implementation_paths.get(feature_id, set()))
        test = sorted(test_paths.get(feature_id, set()))
        setup = sorted(setup_paths.get(feature_id, set()))
        feature = {
            "feature_id": feature_id,
            "app_id": metadata["app_id"],
            "name": metadata["name"],
            "description": metadata["description"],
            "aliases": metadata["aliases"],
            "mention_count": len(feature_mentions),
            "mention_paths": sorted({item["path"] for item in feature_mentions}),
            "mention_sha256": hashlib.sha256(
                json.dumps(sorted(feature_mentions, key=lambda item: item["path"]), sort_keys=True).encode("utf-8")
            ).hexdigest(),
            "implementation_paths": implementation,
            "test_paths": test,
            "setup_or_configuration_paths": setup,
            "status": "NEEDS_REVIEW",
            "remote_verification": False,
            "source_scope": "materialized_local",
            "coverage_complete": False,
        }
        if implementation and test:
            feature["status"] = "MAPPED_LOCAL"
        elif implementation or test or feature_mentions:
            feature["status"] = "MAPPED_CANDIDATE"
        features[feature_id] = feature

    capability_catalog = _build_capability_catalog(feature_map, features)
    metrics = {
        "registered_feature_count": len(features),
        "feature_ids_unique": len(features) == len(feature_map),
        "capability_count": len(capability_catalog),
        "mentioned_feature_count": sum(feature["mention_count"] > 0 for feature in features.values()),
        "mapped_local_feature_count": sum(feature["status"] == "MAPPED_LOCAL" for feature in features.values()),
        "candidate_feature_count": sum(feature["status"] == "MAPPED_CANDIDATE" for feature in features.values()),
        "unmapped_feature_count": sum(feature["status"] == "NEEDS_REVIEW" for feature in features.values()),
    }
    return {
        "schema_version": 1,
        "root": str(source_root),
        "status": "NEEDS_REVIEW",
        "remote_verification_complete": False,
        "registry_feature_count": len(features),
        "discovered_file_count": len(files),
        "all_feature_ids_unique": len(features) == len(feature_map),
        "capability_catalog": capability_catalog,
        "features": features,
        "unavailable_sources": sorted(skipped, key=lambda item: item["path"]),
        "metrics": metrics,
        "all_features_document": _render_all_features(
            source_root,
            feature_map,
            features,
            capability_catalog,
            metrics,
        ),
    }


def _scan_feature_shard(
    root: Path,
    paths: list[Path],
    shard_number: int,
    registry: dict[str, Any],
) -> dict[str, Any]:
    records = _scan_shard(root, paths, shard_number, registry)
    return {
        "number": shard_number,
        "status": records["status"],
        "file_count": records["file_count"],
        "records": records["records"],
    }


def run_parallel_feature_audit(
    root: Path | str,
    *,
    shard_size: int = 250,
    worker_count: int = 4,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run bounded parallel feature provenance scanning and persist deterministic evidence."""
    source_root = Path(root).resolve()
    started = time.monotonic()
    registry = registry or {}
    files = _discover_files(source_root)
    shards = _shard_paths(files, shard_size)
    work_count = min(max(1, worker_count), max(1, len(shards)))
    shard_results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=work_count, thread_name_prefix="qaudits-feature-shard") as executor:
        futures = {
            executor.submit(_scan_feature_shard, source_root, shard, number, registry):
            (number, shard)
            for number, shard in enumerate(shards, start=1)
        }
        for future in as_completed(futures):
            shard_results.append(future.result())
    shard_results.sort(key=lambda item: item["number"])

    scanned_records = [record for shard in shard_results for record in shard["records"]]
    audit = build_feature_audit(source_root, registry, scanned_records=scanned_records)
    feature_manifest = {
        "schema_version": 1,
        "root": str(source_root),
        "status": "NEEDS_REVIEW",
        "remote_verification_complete": False,
        "remote_mutation_performed": False,
        "capability_catalog": audit["capability_catalog"],
        "metrics": {
            "shard_count": len(shard_results),
            "files_scanned": sum(shard["file_count"] for shard in shard_results),
            "registered_feature_count": audit["metrics"]["registered_feature_count"],
            "capability_count": audit["metrics"]["capability_count"],
            "mentioned_feature_count": audit["metrics"]["mentioned_feature_count"],
            "mapped_local_feature_count": audit["metrics"]["mapped_local_feature_count"],
            "candidate_feature_count": audit["metrics"]["candidate_feature_count"],
            "unmapped_feature_count": audit["metrics"]["unmapped_feature_count"],
            "all_feature_ids_unique": audit["all_feature_ids_unique"],
            "all_indexed_paths_ledgered": True,
        },
        "features": audit["features"],
        "shards": [
            {
                "number": shard["number"],
                "status": shard["status"],
                "file_count": shard["file_count"],
                "record_count": len(shard["records"]),
            }
            for shard in shard_results
        ],
        "unavailable_sources": audit["unavailable_sources"],
        "evidence_scope": "local_materialized_tree_only",
    }
    artifact_dir = source_root / "ollamatracks" / "qaudits_all_features"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = artifact_dir / "feature_manifest.json"
    evidence_path = artifact_dir / "feature_evidence.json"
    all_features_path = source_root / "ALLFEATURES.md"
    manifest_path.write_text(json.dumps(feature_manifest, indent=2, sort_keys=True), encoding="utf-8")
    evidence_path.write_text(json.dumps({
        "schema_version": 1,
        "status": "NEEDS_REVIEW",
        "shards": shard_results,
        "remote_verification_complete": False,
    }, indent=2, sort_keys=True), encoding="utf-8")
    all_features_path.write_text(audit["all_features_document"], encoding="utf-8")
    manifest_sha256 = _hash_file(manifest_path)
    evidence_sha256 = _hash_file(evidence_path)
    return {
        "status": "NEEDS_REVIEW",
        "root": str(source_root),
        "remote_verification_complete": False,
        "remote_mutation_performed": False,
        "metrics": {
            "shard_count": len(shard_results),
            "files_scanned": sum(shard["file_count"] for shard in shard_results),
            "registered_feature_count": audit["metrics"]["registered_feature_count"],
            "capability_count": audit["metrics"]["capability_count"],
            "mentioned_feature_count": audit["metrics"]["mentioned_feature_count"],
            "mapped_local_feature_count": audit["metrics"]["mapped_local_feature_count"],
            "candidate_feature_count": audit["metrics"]["candidate_feature_count"],
            "remaining_feature_count": audit["metrics"]["unmapped_feature_count"],
            "feature_manifest_sha256": manifest_sha256,
            "feature_evidence_sha256": evidence_sha256,
            "duration_seconds": round(time.monotonic() - started, 6),
        },
        "artifacts": {
            "feature_manifest": manifest_path,
            "feature_evidence": evidence_path,
            "all_features": all_features_path,
        },
        "contract": {
            "all_feature_ids_unique": audit["all_feature_ids_unique"],
            "remote_verification_complete": False,
            "complete": False,
        },
    }
