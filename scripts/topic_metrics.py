"""Shared evidence-backed metrics for indexed Ollama master-plan topics."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_PLAN_HEADING = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
_INDEX_ENTRY = re.compile(r"^(\d+)\.\s+")
_TOPIC_EVIDENCE = re.compile(r"(?:topic[-_]?|/)(\d{1,3})(?:\.json|/|$)")
_COMPLETED = {"SUCCESS", "FULLY_COMPLETED"}
_BLOCKED = {"BLOCKED", "FAILED", "FAILED_AT"}
_NOT_STARTED = {"NOT_STARTED", "NOT_APPLICABLE"}
_IN_PROGRESS = {"ACTIVE", "IN_PROGRESS", "PARTIALLY_COMPLETE", "RUNNING"}


def build_topic_execution_metrics(root: Path | str) -> dict[str, Any]:
    """Compute topic counts while excluding missing, invalid, or ambiguous evidence."""
    repository_root = Path(root).resolve()
    plan_path = repository_root / "QMOI_Ollama_Autonomous_Production_Completion_Master_Plan.md"
    index_path = repository_root / "ollama_master_topic_index.txt"
    source_errors: list[str] = []
    plan_entries: list[tuple[int, str]] = []
    index_numbers: list[int] = []

    try:
        plan_text = plan_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        source_errors.append(f"master plan unavailable: {type(exc).__name__}")
    else:
        plan_entries = [
            (int(match.group(1)), match.group(2))
            for line in plan_text.splitlines()
            if (match := _PLAN_HEADING.match(line))
        ]

    try:
        index_text = index_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        source_errors.append(f"topic index unavailable: {type(exc).__name__}")
    else:
        index_numbers = [
            int(match.group(1))
            for line in index_text.splitlines()
            if (match := _INDEX_ENTRY.match(line))
        ]

    topics = dict(plan_entries)
    plan_numbers = [number for number, _ in plan_entries]
    duplicate_plan_numbers = sorted(
        number for number in set(plan_numbers) if plan_numbers.count(number) > 1
    )
    duplicate_index_numbers = sorted(
        number for number in set(index_numbers) if index_numbers.count(number) > 1
    )
    evidence_root = repository_root / "Q.0.0.N" / "evidence"
    candidates: dict[int, list[tuple[Path, dict[str, Any] | None]]] = {}
    invalid_evidence_files: list[str] = []
    evidence_files_scanned = 0

    for path in sorted(evidence_root.rglob("*.json")) if evidence_root.is_dir() else ():
        match = _TOPIC_EVIDENCE.search(path.as_posix())
        if not match:
            continue
        number = int(match.group(1))
        if number not in topics:
            continue
        evidence_files_scanned += 1
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            payload = None
        if not isinstance(payload, dict):
            invalid_evidence_files.append(path.relative_to(repository_root).as_posix())
            candidates.setdefault(number, []).append((path, None))
            continue
        evidence_complete = payload.get("evidence_complete")
        candidates.setdefault(number, []).append((path, {
            "path": path.relative_to(repository_root).as_posix(),
            "status": str(payload.get("status", "")).upper(),
            "evidence_complete": evidence_complete is True,
            "evidence_complete_is_boolean": isinstance(evidence_complete, bool),
        }))

    duplicate_evidence_topics = sorted(
        number for number, records in candidates.items() if len(records) > 1
    )
    ambiguous_topics = sorted(set(duplicate_evidence_topics) | {
        number
        for number, records in candidates.items()
        if any(record is None for _, record in records)
    })
    evidence_records = {
        number: records[0][1]
        for number, records in candidates.items()
        if number not in ambiguous_topics and records and records[0][1] is not None
    }
    statuses = {
        number: record["status"]
        for number, record in evidence_records.items()
    }
    fully_completed = sum(
        status in _COMPLETED and evidence_records[number]["evidence_complete"]
        for number, status in statuses.items()
    )
    blocked = sum(status in _BLOCKED for status in statuses.values())
    not_started = sum(status in _NOT_STARTED for status in statuses.values())
    in_progress = sum(status in _IN_PROGRESS for status in statuses.values())
    unmeasured = max(
        len(topics) - fully_completed - blocked - not_started - in_progress,
        0,
    )
    proven_numbers = {
        number
        for number, record in evidence_records.items()
        if record["status"] in _COMPLETED and record["evidence_complete"]
    }

    return {
        "generated": (
            datetime.now(UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        ),
        "plan_path": str(plan_path),
        "index_path": str(index_path),
        "source_errors": source_errors,
        "master_plan_topics": len(topics),
        "master_plan_topic_entries": len(plan_entries),
        "duplicate_plan_topic_numbers": duplicate_plan_numbers,
        "topic_index_entries": len(index_numbers),
        "duplicate_index_numbers": duplicate_index_numbers,
        "missing_index_numbers": sorted(set(topics) - set(index_numbers)),
        "unexpected_index_numbers": sorted(set(index_numbers) - set(topics)),
        "topic_index_matches_plan": (
            not source_errors
            and not duplicate_plan_numbers
            and not duplicate_index_numbers
            and sorted(topics) == index_numbers
        ),
        "evidence_files_scanned": evidence_files_scanned,
        "evidence_records": len(evidence_records),
        "evidence_coverage_percent": round(
            len(evidence_records) / len(topics) * 100, 2
        ) if topics else 0.0,
        "duplicate_evidence_topics": duplicate_evidence_topics,
        "ambiguous_evidence_topics": ambiguous_topics,
        "invalid_evidence_files": sorted(invalid_evidence_files),
        "unknown_status_topics": sorted(
            number
            for number, status in statuses.items()
            if status not in _COMPLETED | _BLOCKED | _NOT_STARTED | _IN_PROGRESS
        ),
        "invalid_evidence_complete_topics": sorted(
            number
            for number, record in evidence_records.items()
            if not record["evidence_complete_is_boolean"]
        ),
        "incomplete_success_topics": sorted(
            number
            for number, record in evidence_records.items()
            if record["status"] in _COMPLETED and not record["evidence_complete"]
        ),
        "fully_completed": fully_completed,
        "in_progress": in_progress,
        "not_started": not_started,
        "blocked": blocked,
        "unmeasured": unmeasured,
        "unproven_topics": sorted(set(topics) - proven_numbers),
        "evidence_records_by_topic": evidence_records,
        "status_sum_matches_inventory": (
            fully_completed + in_progress + not_started + blocked + unmeasured == len(topics)
        ),
    }
