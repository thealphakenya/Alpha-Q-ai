#!/usr/bin/env python3
"""Bounded parallel QAUDITS merge audit and production-hardening orchestration."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Iterable


EXCLUDED_DIRECTORIES = {
    ".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist", "build", "target",
    "coverage", ".cache", "ollamatracks", "QMOItracks",
}


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
            if path.is_symlink():
                continue
            relative = _relative(path, root)
            if any(part in EXCLUDED_DIRECTORIES for part in Path(relative).parts):
                continue
            files.append(path)
    return sorted(files, key=lambda path: _relative(path, root))


def _scan_shard(root: Path, paths: list[Path], shard_number: int) -> dict[str, Any]:
    merge_candidates: list[dict[str, Any]] = []
    production_candidates: list[dict[str, Any]] = []
    for path in paths:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            digest = _hash_file(path)
            relative = _relative(path, root)
            lower = content.lower()
            if re.search(r"\bmerge\b|merge_target|mergeable|merge_policy", lower):
                merge_candidates.append({
                    "path": relative,
                    "sha256": digest,
                    "bytes": path.stat().st_size,
                    "category": "merge_surface",
                })
            if re.search(r"\b(?:todo|stub|minimal|placeholder|not implemented|not implemented yet)\b", lower):
                production_candidates.append({
                    "path": relative,
                    "sha256": digest,
                    "bytes": path.stat().st_size,
                    "category": "production_marker",
                })
        except OSError:
            continue
    return {
        "number": shard_number,
        "status": "complete",
        "file_count": len(paths),
        "merge_candidate_count": len(merge_candidates),
        "production_candidate_count": len(production_candidates),
        "merge_candidates": merge_candidates,
        "production_candidates": production_candidates,
    }


def _shard_paths(paths: list[Path], shard_size: int) -> list[list[Path]]:
    return [paths[index:index + shard_size] for index in range(0, len(paths), shard_size)]


def build_merge_operating_contract(
    roots: list[Path],
    *,
    merge_candidate_count: int,
    production_candidate_count: int,
    remote_verified: bool,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "merge_mode": "canonical_evidence_and_preserve",
        "remote_verification_complete": remote_verified,
        "required_evidence": {
            "source_sha": "exact local source SHA-256",
            "target_sha": "exact target repository or branch SHA-256",
            "artifact_sha": "hash of the generated artifact",
            "test_sha": "hash of the focused validation result",
        },
        "safe_merge_sequence": [
            "enumerate and hash every candidate path",
            "assign ownership and canonical source precedence",
            "map implementation, tests, workflows, documentation, and release evidence",
            "reconcile conflicts without deleting historical or authored content",
            "run focused validation and full validation", 
            "refresh production.md and productionenhanced.md from verified evidence",
            "record merge decisions, blockers, and exact SHAs",
            "stop before remote mutation unless exact authority and terminal evidence are present",
        ],
        "metrics": {
            "merge_candidate_count": merge_candidate_count,
            "production_candidate_count": production_candidate_count,
            "remote_verified": remote_verified,
            "all_candidates_ledgered": True,
        },
        "blockers": [] if remote_verified else [
            "remote completion and protected mutation authority were not verified",
        ],
    }


def run_parallel_merge_audit(
    root: Path | str,
    *,
    shard_size: int = 250,
    worker_count: int = 4,
) -> dict[str, Any]:
    source_root = Path(root).resolve()
    started = time.monotonic()
    files = _discover_files(source_root)
    shards = _shard_paths(files, max(1, shard_size))
    work_count = min(max(1, worker_count), len(shards) or 1)
    shard_results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=work_count, thread_name_prefix="qaudits-merge-shard") as executor:
        futures = {
            executor.submit(_scan_shard, source_root, shard, number):
            (number, shard)
            for number, shard in enumerate(shards, start=1)
        }
        for future in as_completed(futures):
            shard_results.append(future.result())
    shard_results.sort(key=lambda item: item["number"])

    artifact_dir = source_root / "ollamatracks" / "qaudits_parallel_merge"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    merge_manifest_path = artifact_dir / "merge_manifest.json"
    production_inventory_path = artifact_dir / "production_gap_inventory.json"
    operating_contract_path = artifact_dir / "merge_operating_contract.json"
    merge_candidates = [
        candidate
        for shard in shard_results
        for candidate in shard["merge_candidates"]
    ]
    production_candidates = [
        candidate
        for shard in shard_results
        for candidate in shard["production_candidates"]
    ]
    manifest = {
        "schema_version": 1,
        "root": str(source_root),
        "status": "NEEDS_REVIEW",
        "shard_count": len(shard_results),
        "files_scanned": sum(shard["file_count"] for shard in shard_results),
        "shards": [
            {
                "number": shard["number"],
                "status": shard["status"],
                "file_count": shard["file_count"],
                "merge_candidate_count": shard["merge_candidate_count"],
                "production_candidate_count": shard["production_candidate_count"],
            }
            for shard in shard_results
        ],
        "merge_candidates": merge_candidates,
        "production_candidates": production_candidates,
        "remote_verification_complete": False,
    }
    merge_manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    production_inventory = {
        "schema_version": 1,
        "status": "NEEDS_REVIEW",
        "specification": "production.md and productionenhanced.md remain evidence-ledgers",
        "candidates": production_candidates,
        "remote_verification_complete": False,
        "coverage_complete": False,
    }
    production_inventory_path.write_text(
        json.dumps(production_inventory, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    contract = build_merge_operating_contract(
        roots=[source_root],
        merge_candidate_count=len(merge_candidates),
        production_candidate_count=len(production_candidates),
        remote_verified=False,
    )
    operating_contract_path.write_text(
        json.dumps(contract, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    artifact_hashes = {
        "merge_manifest_sha256": _hash_file(merge_manifest_path),
        "production_inventory_sha256": _hash_file(production_inventory_path),
        "operating_contract_sha256": _hash_file(operating_contract_path),
    }
    return {
        "status": "NEEDS_REVIEW",
        "root": str(source_root),
        "remote_verification_complete": False,
        "remote_mutation_performed": False,
        "metrics": {
            "shard_count": len(shard_results),
            "files_scanned": manifest["files_scanned"],
            "merge_candidate_count": len(merge_candidates),
            "production_candidate_count": len(production_candidates),
            "workers": work_count,
            "duration_seconds": round(time.monotonic() - started, 6),
            **artifact_hashes,
        },
        "artifacts": {
            "merge_manifest": merge_manifest_path,
            "production_inventory": production_inventory_path,
            "operating_contract": operating_contract_path,
        },
        "contract": contract,
    }
