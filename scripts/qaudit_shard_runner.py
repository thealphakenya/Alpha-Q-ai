"""Bounded, resumable QAUDITS path/hash shards for materialized local trees."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any

from scripts.qaudit_checkpoint import record_qaudit_checkpoint

SCHEMA_VERSION = 1
MAX_FILES_PER_SHARD = 500
MAX_SHARDS_PER_CALL = 10
MAX_HASH_BYTES = 100_000_000
IGNORED_DIRECTORIES = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "dist", "build", "target", "coverage", ".cache",
}
EXCLUDED_PATHS = {
    "oe2.txt",
    "remotecompletion.md",
    "remote-completion.json",
    "remote-evidence-ledger.jsonl",
    "ollamatracks/STATE.txt",
    "ollamatracks/LATEST_ACTIVITY.txt",
    "ollamatracks/CURRENT_STATUS.txt",
    "ollamatracks/TRACKING_INDEX.txt",
    "ollamatracks/PR_STATUS.txt",
    "ollamatracks/LAST_RECONCILIATION.txt",
    "ollamatracks/agent.log",
    "ollamatracks/telemetry.jsonl",
    "ollamatracks/live_activity_stream.json",
    "ollamatracks/qmoi_live_activity.json",
    "ollamatracks/ollama_autonomous_agent_live_activity.json",
    "ollamatracks/current_state.json",
    "ollamatracks/qaudit_universe.json",
    "ollamatracks/qaudits_evolution_plan.json",
    "ollamatracks/qaudit_shards",
    "ollamatracks/ollama_reference_audit.json",
    "ollamatracks/repository_surface_audit.json",
    "ollamatracks/feature_test_hook_coverage.json",
    "ollamatracks/system_accountability_audit.json",
    "ollamatracks/production_gap_inventory.json",
    "QMOItracks/style_universal_candidate_tree.md",
}


def _git_value(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip()


def _enumerate_inputs(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, str]], str]:
    files: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    for current, directory_names, filenames in os.walk(root, topdown=True, followlinks=False):
        parent = Path(current)
        retained = []
        for name in sorted(directory_names):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if name in IGNORED_DIRECTORIES:
                skipped.append({"path": relative, "reason": "dependency_or_cache_directory_excluded"})
            elif path.is_symlink():
                skipped.append({"path": relative, "reason": "symlink_directory_not_followed"})
            elif relative in EXCLUDED_PATHS:
                continue
            else:
                retained.append(name)
        directory_names[:] = retained
        for name in sorted(filenames):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if relative in EXCLUDED_PATHS or any(relative.startswith(item + "/") for item in EXCLUDED_PATHS):
                continue
            if path.is_symlink():
                skipped.append({"path": relative, "reason": "symlink_file_not_followed"})
                continue
            try:
                stat = path.stat(follow_symlinks=False)
            except OSError as exc:
                skipped.append({"path": relative, "reason": f"stat:{type(exc).__name__}"})
                continue
            files.append({
                "path": relative,
                "bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
                "inode": stat.st_ino,
            })

    files.sort(key=lambda item: item["path"])
    skipped.sort(key=lambda item: (item["path"], item["reason"]))
    identity = {
        "schema_version": SCHEMA_VERSION,
        "root_name": root.name,
        "head_sha": _git_value(root, "rev-parse", "HEAD"),
        "tree_sha": _git_value(root, "rev-parse", "HEAD^{tree}"),
        "files": files,
        "skipped": skipped,
        "ignored_directories": sorted(IGNORED_DIRECTORIES),
        "excluded_paths": sorted(EXCLUDED_PATHS),
    }
    source_manifest = hashlib.sha256(
        json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return files, skipped, source_manifest


def _sha256_stable(path: Path, expected: dict[str, Any]) -> tuple[str | None, str, int]:
    if expected["bytes"] > MAX_HASH_BYTES:
        return None, "metadata_only_oversized", 0
    digest = hashlib.sha256()
    hashed_bytes = 0
    try:
        before = path.stat(follow_symlinks=False)
        if (before.st_size, before.st_mtime_ns, before.st_ino) != (
            expected["bytes"], expected["mtime_ns"], expected["inode"]
        ):
            return None, "changed_before_hash", 0
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
                hashed_bytes += len(chunk)
        after = path.stat(follow_symlinks=False)
        if (after.st_size, after.st_mtime_ns, after.st_ino) != (
            expected["bytes"], expected["mtime_ns"], expected["inode"]
        ):
            return None, "changed_during_hash", hashed_bytes
    except OSError as exc:
        return None, f"unreadable:{type(exc).__name__}", hashed_bytes
    return digest.hexdigest(), "hashed", hashed_bytes


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _valid_existing_shard(path: Path, manifest: str, number: int) -> dict[str, Any] | None:
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        isinstance(record, dict)
        and record.get("schema_version") == SCHEMA_VERSION
        and record.get("source_manifest_sha256") == manifest
        and record.get("shard_number") == number
        and isinstance(record.get("records"), list)
        and record.get("status") == "SHARD_COMPLETE"
    ):
        return record
    return None


def _number_ranges(numbers: list[int]) -> list[list[int]]:
    ranges: list[list[int]] = []
    for number in numbers:
        if not ranges or number > ranges[-1][1] + 1:
            ranges.append([number, number])
        else:
            ranges[-1][1] = number
    return ranges


def run_bounded_audit_shards(
    root: Path | str,
    *,
    shard_size: int = 100,
    max_shards: int = 1,
) -> dict[str, Any]:
    """Hash a bounded number of deterministic path slices and resume on the next call."""
    if not 1 <= shard_size <= MAX_FILES_PER_SHARD:
        raise ValueError(f"shard_size must be between 1 and {MAX_FILES_PER_SHARD}")
    if not 1 <= max_shards <= MAX_SHARDS_PER_CALL:
        raise ValueError(f"max_shards must be between 1 and {MAX_SHARDS_PER_CALL}")
    target = Path(root).resolve()
    if not target.is_dir():
        raise ValueError("repository root must be an existing directory")

    correlation_id = str(uuid.uuid4())
    record_qaudit_checkpoint(
        target,
        "audit-inventory-shard",
        {
            "status": "IN_PROGRESS",
            "metrics": {"phase": "shard_start", "shard_size": shard_size, "max_shards": max_shards},
            "blockers": ["bounded_shard_run_not_terminal", "remote_completion_not_verified"],
            "next_action": "Resume this deterministic shard run from its source-manifest-bound completed shard list.",
        },
        correlation_id=correlation_id,
    )

    started = time.monotonic()
    files, skipped, manifest = _enumerate_inputs(target)
    total_shards = (len(files) + shard_size - 1) // shard_size
    run_dir = target / "ollamatracks" / "qaudit_shards" / manifest[:20]
    shard_paths = [run_dir / f"shard-{number:06d}.json" for number in range(1, total_shards + 1)]
    completed_records = {
        number: record
        for number, path in enumerate(shard_paths, start=1)
        if (record := _valid_existing_shard(path, manifest, number)) is not None
    }
    processed_this_call = 0
    bytes_hashed_this_call = 0
    written: list[dict[str, Any]] = []

    for number, artifact_path in enumerate(shard_paths, start=1):
        if number in completed_records:
            continue
        if processed_this_call >= max_shards:
            break
        first = (number - 1) * shard_size
        shard_inputs = files[first : first + shard_size]
        records = []
        for source in shard_inputs:
            digest, status, hashed_bytes = _sha256_stable(target / source["path"], source)
            bytes_hashed_this_call += hashed_bytes
            records.append({
                "path": source["path"],
                "bytes": source["bytes"],
                "sha256": digest,
                "status": status,
                "scope": "historical_or_archive_candidate" if any(
                    part in {"archive", "archives", "history", "historical", "backups", "snapshots", "qmoi-enhanced-history-14", "Alpha-Q-ai-2025"}
                    for part in Path(source["path"]).parts
                ) else "materialized_local",
            })
        shard = {
            "schema_version": SCHEMA_VERSION,
            "source_manifest_sha256": manifest,
            "shard_number": number,
            "shard_count": total_shards,
            "path_start": shard_inputs[0]["path"] if shard_inputs else None,
            "path_end": shard_inputs[-1]["path"] if shard_inputs else None,
            "file_count": len(shard_inputs),
            "records": records,
            "status": "SHARD_COMPLETE",
            "source_text_recorded": False,
            "remote_verified": False,
        }
        _atomic_json(artifact_path, shard)
        completed_records[number] = shard
        processed_this_call += 1
        written.append(shard)

    completed_numbers = sorted(completed_records)
    remaining = [number for number in range(1, total_shards + 1) if number not in completed_records]
    completed_file_count = sum(record.get("file_count", 0) for record in completed_records.values())
    total_hash_errors = sum(
        item.get("status", "").startswith("unreadable")
        or item.get("status", "").startswith("changed_")
        for shard in completed_records.values()
        for item in shard.get("records", [])
    )
    status = "IN_PROGRESS" if remaining else "NEEDS_REVIEW"
    result = {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "source_scope": "materialized_local_path_hash_shards_only",
        "source_manifest_sha256": manifest,
        "total_file_count": len(files),
        "total_shard_count": total_shards,
        "completed_shard_numbers": completed_numbers,
        "remaining_shard_numbers": remaining,
        "remaining_shard_count": len(remaining),
        "remaining_shard_ranges": _number_ranges(remaining),
        "completed_file_count": completed_file_count,
        "skipped_path_count": len(skipped),
        "hash_error_count": total_hash_errors,
        "bytes_hashed_this_call": bytes_hashed_this_call,
        "duration_seconds": round(time.monotonic() - started, 6),
        "shards_written_this_call": [
            {"number": item["shard_number"], "file_count": item["file_count"], "path_start": item["path_start"], "path_end": item["path_end"]}
            for item in written
        ],
        "artifact_directory": run_dir.relative_to(target).as_posix(),
        "skipped_paths": skipped,
        "excluded_paths": sorted(EXCLUDED_PATHS),
        "remote_verified": False,
        "semantic_review_complete": False,
        "next_action": (
            f"Invoke audit-inventory-shard again for the next missing shard ({remaining[0]} of {total_shards})."
            if remaining
            else "All local path/hash shards are present; run semantic, feature/test, security, QLion, and remote exact-SHA gates before any completion claim."
        ),
    }
    _atomic_json(run_dir / "shard_run.json", result)
    artifact_sha = hashlib.sha256((run_dir / "shard_run.json").read_bytes()).hexdigest()
    record_qaudit_checkpoint(
        target,
        "audit-inventory-shard",
        {
            "status": status,
            "source_manifest_sha256": manifest,
            "artifact_path": (run_dir / "shard_run.json").relative_to(target).as_posix(),
            "artifact_sha256": artifact_sha,
            "artifact_bytes": (run_dir / "shard_run.json").stat().st_size,
            "artifact_refs": {
                "shard_directory": result["artifact_directory"],
                "completed_shards": completed_numbers,
            },
            "metrics": {
                "source_scope": result["source_scope"],
                "total_file_count": result["total_file_count"],
                "completed_file_count": completed_file_count,
                "completed_shard_count": len(completed_numbers),
                "total_shard_count": total_shards,
                "next_shard_number": remaining[0] if remaining else None,
                "remaining_shard_count": len(remaining),
                "remaining_shard_ranges": _number_ranges(remaining),
                "skipped_path_count": len(skipped),
                "hash_error_count": total_hash_errors,
                "bytes_hashed_this_call": bytes_hashed_this_call,
                "duration_seconds": result["duration_seconds"],
                "remote_verified": False,
                "semantic_review_complete": False,
            },
            "blockers": [
                *( ["audit_inventory_shards_remaining"] if remaining else [] ),
                "semantic_feature_test_security_and_remote_gates_not_run",
                "target_owned_terminal_remote_sha_proof_unavailable",
            ],
            "next_action": result["next_action"],
        },
        correlation_id=correlation_id,
    )
    return result