"""Safely maintain requirement tasks, 18 canonical mission phases, and checkpoints."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from scripts.execution_lock import ExecutionLock
from scripts.qaudit_checkpoint import record_qaudit_checkpoint


ROOT = Path(__file__).resolve().parents[1]
LEDGER_RELATIVE_PATH = Path("ollamatracks/mission-task-ledger.json")
MISSION_SOURCE_PATH = Path("latest mission.md")
MISSION_PHASE_START = "<!-- BEGIN QMOI MISSION PHASE METRICS -->"
MISSION_PHASE_END = "<!-- END QMOI MISSION PHASE METRICS -->"
MISSION_PHASE_COUNT = 18
MISSION_MIRROR_PATHS = (
    Path("MISSION.md"),
    Path("NEWMISSION.md"),
    Path("MISSIONEW.md"),
    Path("MISSIONNEW.md"),
    Path("MISSIONNEWEST.md"),
    Path(".github/instructions/MISSION.md"),
)
MISSION_STATUSES = {
    "PENDING",
    "IN_PROGRESS",
    "VERIFIED_COMPLETE",
    "PARTIALLY_COMPLETE",
    "BLOCKED",
    "FAILED",
}
TERMINAL_TASK_STATUSES = {
    "VERIFIED_COMPLETE",
    "PARTIALLY_COMPLETE",
    "BLOCKED",
    "FAILED",
}
REQUIREMENT_COVERAGE_FIELDS = (
    "owner_refs",
    "implementation_refs",
    "test_refs",
    "security_refs",
    "documentation_refs",
    "integration_refs",
    "remote_evidence_refs",
)


class LedgerError(RuntimeError):
    """A mission ledger cannot be safely read or transitioned."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_utc(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise LedgerError(f"Invalid UTC timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise LedgerError("Mission timestamps must include a timezone")
    return parsed.astimezone(timezone.utc)


def _git(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        raise LedgerError(f"Unable to verify local repository state ({type(exc).__name__})") from exc
    return result.stdout.strip()


def _verify_repository(
    root: Path,
    ledger: dict[str, Any],
    *,
    require_target_branch: bool = True,
) -> str:
    branch = _verify_repository_identity(
        root,
        ledger,
        require_target_branch=require_target_branch,
    )
    expected_hash = ledger["canonical_source"]["sha256"]
    for relative in [ledger["canonical_source"]["path"], *ledger["canonical_source"]["byte_identical_mirrors"]]:
        source = root / relative
        if source.is_symlink() or not source.is_file():
            raise LedgerError(f"Mission source is missing or symlinked: {relative}")
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected_hash:
            raise LedgerError(f"Mission source changed after ledger initialization: {relative}")
    return branch


def _verify_repository_identity(
    root: Path,
    ledger: dict[str, Any],
    *,
    require_target_branch: bool,
) -> str:
    branch = _git(root, "branch", "--show-current")
    if require_target_branch and branch != ledger.get("target_branch"):
        raise LedgerError(
            f"Refusing mission update on branch {branch!r}; expected {ledger.get('target_branch')!r}"
        )
    remote = _git(root, "remote", "get-url", "origin")
    match = re.fullmatch(
        r"(?:https://github\.com/|git@github\.com:)([^/\s]+)/([^/\s]+?)(?:\.git)?",
        remote,
        flags=re.IGNORECASE,
    )
    if not match or f"{match.group(1)}/{match.group(2)}".lower() != ledger.get("repository", "").lower():
        raise LedgerError("Refusing mission update: origin does not identify the expected GitHub repository")
    return branch


def validate_ledger(ledger: Any) -> dict[str, Any]:
    if not isinstance(ledger, dict) or ledger.get("schema_version") != "1.0":
        raise LedgerError("Mission task ledger has an unsupported or malformed schema")
    clock = ledger.get("mission_clock")
    tasks = ledger.get("tasks")
    if not isinstance(clock, dict) or not isinstance(tasks, list) or len(tasks) != 16:
        raise LedgerError("Mission task ledger must contain its clock and all 16 mission sections")
    start = _parse_utc(clock.get("started_at"))
    deadline = _parse_utc(clock.get("deadline_at"))
    if deadline - start != timedelta(minutes=120):
        raise LedgerError("Mission deadline must be exactly 120 minutes after its start")
    ids = [item.get("id") for item in tasks if isinstance(item, dict)]
    expected = [f"M{index:02d}" for index in range(1, 17)]
    if ids != expected:
        raise LedgerError("Mission task IDs must be unique and ordered M01 through M16")
    known_ids = set(expected)
    phase_metrics = ledger.get("mission_phase_metrics")
    if phase_metrics is not None:
        phase_ids = [phase.get("id") for phase in phase_metrics if isinstance(phase, dict)]
        if phase_ids != [f"PH{index:02d}" for index in range(1, MISSION_PHASE_COUNT + 1)]:
            raise LedgerError("Mission phase metrics must contain ordered PH01 through PH18 entries")
        mission_phase_status_counts(ledger)
    requirement_lines = ledger.get("mission_requirement_line_records")
    if requirement_lines is not None:
        if ledger.get("mission_requirement_line_count") != len(requirement_lines):
            raise LedgerError("Mission requirement-line count does not match its source records")
        line_ids = [item.get("id") for item in requirement_lines if isinstance(item, dict)]
        if len(line_ids) != len(requirement_lines) or len(line_ids) != len(set(line_ids)):
            raise LedgerError("Mission requirement-line IDs must be valid and unique")
        phase_ids = {f"PH{index:02d}" for index in range(1, MISSION_PHASE_COUNT + 1)}
        for item in requirement_lines:
            if item.get("phase_id") is not None and item.get("phase_id") not in phase_ids:
                raise LedgerError(f"{item.get('id')} references an unknown mission phase")
            if not re.fullmatch(r"[0-9a-f]{64}", str(item.get("line_sha256", ""))):
                raise LedgerError(f"{item.get('id')} has an invalid source-line hash")
            if not isinstance(item.get("semantic_reviewed"), bool):
                raise LedgerError(f"{item.get('id')} has an invalid semantic-review state")
            coverage_refs = item.get("coverage_refs")
            if coverage_refs is not None:
                if not isinstance(coverage_refs, dict) or set(coverage_refs) != set(REQUIREMENT_COVERAGE_FIELDS):
                    raise LedgerError(f"{item.get('id')} has an invalid requirement-coverage mapping")
                for field in REQUIREMENT_COVERAGE_FIELDS:
                    refs = coverage_refs[field]
                    if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref.strip() for ref in refs):
                        raise LedgerError(f"{item.get('id')} has invalid {field}")
    run_history = ledger.get("mission_run_history", [])
    if not isinstance(run_history, list):
        raise LedgerError("Mission run history must be a list")
    for run in run_history:
        if not isinstance(run, dict):
            raise LedgerError("Mission run history contains a malformed record")
        archived_clock = run.get("mission_clock")
        if not isinstance(archived_clock, dict):
            raise LedgerError("Mission run history is missing the archived clock")
        run_started = _parse_utc(run.get("started_at"))
        run_deadline = _parse_utc(run.get("deadline_at"))
        if (
            run_started != _parse_utc(archived_clock.get("started_at"))
            or run_deadline != _parse_utc(archived_clock.get("deadline_at"))
        ):
            raise LedgerError("Archived mission clock does not match its indexed timestamps")
        _parse_utc(run.get("archived_at"))
        if run_deadline - run_started != timedelta(minutes=120):
            raise LedgerError("Archived mission runs must retain their original 120-minute clock")
        for field in ("ledger_id", "correlation_id", "superseded_by_ledger_id", "superseded_by_correlation_id"):
            if not isinstance(run.get(field), str) or not run[field]:
                raise LedgerError(f"Mission run history has an invalid {field}")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,119}", str(run.get("authorization_ref", ""))):
            raise LedgerError("Mission run history has an invalid authorization reference")
    for task in tasks:
        if task.get("status") not in MISSION_STATUSES:
            raise LedgerError(f"{task['id']} has an unsupported status")
        dependencies = task.get("dependencies")
        if not isinstance(dependencies, list) or any(dep not in known_ids for dep in dependencies):
            raise LedgerError(f"{task['id']} has an invalid dependency list")
        if task["id"] in dependencies:
            raise LedgerError(f"{task['id']} cannot depend on itself")
        for timestamp_field in ("started_at", "finished_at"):
            timestamp = task.get(timestamp_field)
            if timestamp is not None:
                _parse_utc(timestamp)
    if ledger.get("status_counts") != status_counts(ledger):
        raise LedgerError("Mission task status counts do not match the authoritative task entries")
    return ledger


def load_ledger(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise LedgerError("Refusing to follow a symlink for the mission ledger")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LedgerError(f"Mission task ledger is missing or unreadable ({type(exc).__name__})") from exc
    return validate_ledger(value)


def status_counts(ledger: dict[str, Any]) -> dict[str, int]:
    counts = {status.lower(): 0 for status in MISSION_STATUSES}
    for task in ledger["tasks"]:
        counts[task["status"].lower()] += 1
    return counts


def sync_mission_phase_catalog(ledger: dict[str, Any], mission_text: str) -> list[dict[str, Any]]:
    matches = list(re.finditer(r"^PHASE\s+(\d+)\s+\u2014\s+(.+?)\s*$", mission_text, re.MULTILINE))
    headings = [(match.group(1), match.group(2)) for match in matches]
    expected_numbers = [str(number) for number in range(1, MISSION_PHASE_COUNT + 1)]
    if [number for number, _ in headings] != expected_numbers:
        raise LedgerError("Canonical mission must contain exactly ordered phase headings 1 through 18")

    existing = {
        item.get("id"): item
        for item in ledger.get("mission_phase_metrics", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    phases = []
    source_lines = mission_text.splitlines()
    existing_requirement_lines = {
        item.get("id"): item
        for item in ledger.get("mission_requirement_line_records", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for index, (number, heading) in enumerate(headings):
        phase_id = f"PH{int(number):02d}"
        first_line = mission_text.count("\n", 0, matches[index].start()) + 1
        last_line = (
            mission_text.count("\n", 0, matches[index + 1].start())
            if index + 1 < len(matches)
            else len(source_lines)
        )
        phase_lines = source_lines[first_line:last_line]
        bullet_candidates = sum(
            1 for line in phase_lines
            if re.match(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", line)
        )
        phase = existing.get(phase_id, {
            "id": phase_id,
            "number": int(number),
            "status": "PENDING",
            "started_at": None,
            "finished_at": None,
            "elapsed_seconds": 0.0,
            "attempt_history": [],
            "evidence_refs": [],
            "blockers": [],
            "next_action": "Start this phase through scripts.mission_task_ledger.",
        })
        phase["number"] = int(number)
        phase["heading"] = heading
        phase["source_path"] = MISSION_SOURCE_PATH.as_posix()
        phase["source_line_start"] = first_line
        phase["source_line_end"] = last_line
        phase["source_ref"] = f"{MISSION_SOURCE_PATH.as_posix()}#L{first_line}-L{last_line}"
        phase["requirement_bullet_candidates"] = bullet_candidates
        phases.append(phase)

    authored_line_records = []
    current_phase_by_line = {
        line_number: phase["id"]
        for phase in phases
        for line_number in range(phase["source_line_start"], phase["source_line_end"] + 1)
    }
    in_managed_audit = False
    for line_number, raw_line in enumerate(source_lines, start=1):
        stripped = raw_line.strip()
        if stripped == "<!-- BEGIN QMOI MANAGED: repository-surface-audit -->":
            in_managed_audit = True
            continue
        if stripped == "<!-- END QMOI MANAGED: repository-surface-audit -->":
            in_managed_audit = False
            continue
        if in_managed_audit or not stripped or re.fullmatch(r"[=\-_*\s]+", stripped):
            continue
        line_sha256 = hashlib.sha256(raw_line.encode("utf-8")).hexdigest()
        record_id = f"MREQ-L{line_number:04d}-{line_sha256[:8]}"
        previous = existing_requirement_lines.get(record_id, {})
        line_kind = (
            "phase_heading" if re.match(r"^PHASE\s+\d+\s+", stripped) else
            "heading_candidate" if re.match(r"^#{1,6}\s+", stripped) else
            "list_candidate" if re.match(r"^(?:[-*+]\s+|\d+[.)]\s+)", stripped) else
            "table_row_candidate" if stripped.startswith("|") else
            "prose_candidate"
        )
        authored_line_records.append({
            "id": record_id,
            "source_path": MISSION_SOURCE_PATH.as_posix(),
            "source_line": line_number,
            "source_ref": f"{MISSION_SOURCE_PATH.as_posix()}#L{line_number}",
            "line_sha256": line_sha256,
            "line_kind": line_kind,
            "phase_id": current_phase_by_line.get(line_number),
            "status": previous.get("status", "NOT_REVIEWED"),
            "semantic_reviewed": bool(previous.get("semantic_reviewed", False)),
            "acceptance_refs": list(previous.get("acceptance_refs", [])),
            "coverage_refs": {
                field: list(previous.get("coverage_refs", {}).get(field, []))
                for field in REQUIREMENT_COVERAGE_FIELDS
            },
        })
    for phase in phases:
        phase["requirement_line_count"] = sum(
            record["phase_id"] == phase["id"] for record in authored_line_records
        )
        phase["unreviewed_requirement_line_count"] = sum(
            record["phase_id"] == phase["id"] and not record["semantic_reviewed"]
            for record in authored_line_records
        )
    ledger["mission_phase_metrics"] = phases
    ledger["mission_requirement_line_records"] = authored_line_records
    ledger["mission_requirement_line_count"] = len(authored_line_records)
    ledger["mission_requirement_line_review_counts"] = {
        "not_reviewed": sum(not item["semantic_reviewed"] for item in authored_line_records),
        "reviewed": sum(item["semantic_reviewed"] for item in authored_line_records),
    }
    ledger["mission_phase_metric_source"] = {
        "path": MISSION_SOURCE_PATH.as_posix(),
        "sha256": hashlib.sha256(mission_text.encode("utf-8")).hexdigest(),
        "phase_count": MISSION_PHASE_COUNT,
    }
    return phases


def mission_phase_status_counts(ledger: dict[str, Any]) -> dict[str, int]:
    phases = ledger.get("mission_phase_metrics", [])
    counts = {status: 0 for status in ("PENDING", "IN_PROGRESS", "PASS", "PARTIALLY_COMPLETE", "BLOCKED", "FAILED")}
    for phase in phases:
        status = phase.get("status")
        if status not in counts:
            raise LedgerError(f"Mission phase {phase.get('id')} has an unsupported status")
        counts[status] += 1
    return counts


def build_resume_plan(
    ledger: dict[str, Any],
    *,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Describe dependency-ready work without changing mission state or authorizing execution."""
    validate_ledger(ledger)
    instant = now or datetime.now(timezone.utc)
    deadline = _parse_utc(ledger["mission_clock"]["deadline_at"])
    deadline_expired = instant >= deadline
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    status_order = {
        "BLOCKED": 0,
        "IN_PROGRESS": 1,
        "PARTIALLY_COMPLETE": 2,
        "FAILED": 3,
        "VERIFIED_COMPLETE": 4,
        "PENDING": 5,
    }
    requirement_records = ledger.get("mission_requirement_line_records", [])
    records_by_phase: dict[str, list[dict[str, Any]]] = {}
    unassigned_records = []
    for record in requirement_records:
        phase_id = record.get("phase_id")
        if isinstance(phase_id, str):
            records_by_phase.setdefault(phase_id, []).append(record)
        else:
            unassigned_records.append(record)

    task_records = []
    for task in ledger["tasks"]:
        unmet_dependencies = [
            dependency
            for dependency in task["dependencies"]
            if _task(ledger, dependency)["status"] != "VERIFIED_COMPLETE"
        ]
        task_records.append({
            "id": task["id"],
            "priority": task["priority"],
            "status": task["status"],
            "dependencies": list(task["dependencies"]),
            "unmet_dependencies": unmet_dependencies,
            "dependency_ready": not unmet_dependencies,
            "blocker_count": len(task.get("blockers", [])),
        })

    resumable_statuses = {"BLOCKED", "IN_PROGRESS", "PARTIALLY_COMPLETE", "FAILED", "PENDING", "VERIFIED_COMPLETE"}
    candidates = [
        task
        for task in task_records
        if task["dependency_ready"] and task["status"] in resumable_statuses
    ]
    candidates.sort(
        key=lambda task: (
            priority_order.get(task["priority"], len(priority_order)),
            status_order[task["status"]],
            task["id"],
        )
    )
    safe_execution_statuses = {"IN_PROGRESS", "PARTIALLY_COMPLETE", "FAILED", "PENDING"}
    safe_candidates = [
        task for task in candidates if task["status"] in safe_execution_statuses
    ]
    blocked_ready_task_ids = [
        task["id"] for task in candidates if task["status"] == "BLOCKED"
    ]
    completed_ready_task_ids = [
        task["id"] for task in candidates if task["status"] == "VERIFIED_COMPLETE"
    ]
    phase_records = []
    for phase in ledger.get("mission_phase_metrics", []):
        requirements = records_by_phase.get(phase["id"], [])
        unreviewed_requirements = [
            record for record in requirements
            if not record.get("semantic_reviewed", False)
        ]
        reviewed_unmapped_requirements = [
            record for record in requirements
            if record.get("semantic_reviewed", False) and not record.get("acceptance_refs")
        ]
        acceptance_mapped_requirements = [
            record for record in requirements
            if record.get("semantic_reviewed", False) and record.get("acceptance_refs")
        ]
        unmapped_coverage = {
            field: [
                record for record in requirements
                if not record.get("coverage_refs", {}).get(field)
            ]
            for field in REQUIREMENT_COVERAGE_FIELDS
        }
        local_pass_gate_blockers = []
        if phase.get("status") != "IN_PROGRESS":
            local_pass_gate_blockers.append("phase_not_in_progress")
        if not requirements:
            local_pass_gate_blockers.append("no_indexed_requirement_lines")
        if unreviewed_requirements:
            local_pass_gate_blockers.append(
                f"{len(unreviewed_requirements)}_unreviewed_requirement_lines"
            )
        if reviewed_unmapped_requirements:
            local_pass_gate_blockers.append(
                f"{len(reviewed_unmapped_requirements)}_reviewed_lines_without_acceptance_refs"
            )
        local_pass_gate_blockers.extend(
            f"{len(records)}_unmapped_{field}"
            for field, records in unmapped_coverage.items()
            if records
        )
        if not phase.get("evidence_refs"):
            local_pass_gate_blockers.append("no_phase_evidence_refs")
        coverage_mapped_counts = {
            field: len(requirements) - len(records)
            for field, records in unmapped_coverage.items()
        }
        phase_records.append({
            "id": phase["id"],
            "status": phase["status"],
            "source_ref": phase.get("source_ref"),
            "requirement_line_count": len(requirements),
            "reviewed_requirement_line_count": len(requirements) - len(unreviewed_requirements),
            "acceptance_mapped_requirement_line_count": len(acceptance_mapped_requirements),
            "reviewed_unmapped_requirement_line_count": len(reviewed_unmapped_requirements),
            "coverage_mapped_counts": coverage_mapped_counts,
            "coverage_unmapped_counts": {
                field: len(records) for field, records in unmapped_coverage.items()
            },
            "acceptance_mapped_requirement_line_ids": [
                record["id"] for record in acceptance_mapped_requirements
            ],
            "local_pass_gate_ready": not local_pass_gate_blockers,
            "local_pass_gate_blockers": local_pass_gate_blockers,
            "reviewed_requirement_line_ids": [
                record["id"]
                for record in requirements
                if record.get("semantic_reviewed", False)
            ],
            "unreviewed_requirement_line_count": len(unreviewed_requirements),
            "unreviewed_requirement_line_ids": [
                record["id"] for record in unreviewed_requirements
            ],
        })

    if deadline_expired:
        status = "PAUSED_EXPIRED_CLOCK"
    elif candidates:
        status = "READY_FOR_AUTHORIZED_EXECUTOR"
    else:
        status = "BLOCKED_NO_DEPENDENCY_READY_TASK"
    if deadline_expired:
        safe_execution_status = "PAUSED_EXPIRED_CLOCK"
    elif safe_candidates:
        safe_execution_status = "SAFE_LOCAL_TASKS_AVAILABLE"
    elif blocked_ready_task_ids or completed_ready_task_ids:
        safe_execution_status = "BLOCKED_NO_SAFE_DEPENDENCY_READY_TASK"
    else:
        safe_execution_status = "BLOCKED_NO_DEPENDENCY_READY_TASK"

    return {
        "status": status,
        "safe_execution_status": safe_execution_status,
        "safe_execution_authorized": False,
        "safe_execution_task_ids": [task["id"] for task in safe_candidates],
        "next_safe_task_id": safe_candidates[0]["id"] if safe_candidates else None,
        "blocked_dependency_ready_task_ids": blocked_ready_task_ids,
        "completed_dependency_ready_task_ids": completed_ready_task_ids,
        "deadline_expired": deadline_expired,
        "task_transitions_performed": False,
        "execution_authorized": False,
        "remote_mutation_performed": False,
        "remote_verified": False,
        "dependency_ready_task_ids": [task["id"] for task in candidates],
        "next_task_id": candidates[0]["id"] if candidates else None,
        "tasks": task_records,
        "phases": phase_records,
        "phase_count": len(phase_records),
        "requirement_line_count": len(requirement_records),
        "unreviewed_requirement_line_count": sum(
            not record.get("semantic_reviewed", False)
            for record in requirement_records
        ),
        "acceptance_mapped_requirement_line_count": sum(
            record.get("semantic_reviewed", False) and bool(record.get("acceptance_refs"))
            for record in requirement_records
        ),
        "reviewed_unmapped_requirement_line_count": sum(
            record.get("semantic_reviewed", False) and not record.get("acceptance_refs")
            for record in requirement_records
        ),
        "requirement_coverage_mapped_counts": {
            field: sum(bool(record.get("coverage_refs", {}).get(field)) for record in requirement_records)
            for field in REQUIREMENT_COVERAGE_FIELDS
        },
        "unassigned_requirement_line_count": len(unassigned_records),
        "unassigned_reviewed_requirement_line_ids": [
            record["id"]
            for record in unassigned_records
            if record.get("semantic_reviewed", False)
        ],
        "unassigned_unreviewed_requirement_line_ids": [
            record["id"]
            for record in unassigned_records
            if not record.get("semantic_reviewed", False)
        ],
        "unassigned_unreviewed_requirement_line_count": sum(
            not record.get("semantic_reviewed", False)
            for record in unassigned_records
        ),
    }


def _phase_elapsed_seconds(phase: dict[str, Any], now: datetime) -> float:
    elapsed = sum(
        float(attempt["elapsed_seconds"])
        for attempt in phase.get("attempt_history", [])
        if attempt.get("elapsed_seconds") is not None
    )
    if phase.get("status") == "IN_PROGRESS":
        started = phase.get("last_started_at") or phase.get("started_at")
        if started:
            elapsed += max(0.0, (now - _parse_utc(started)).total_seconds())
    return round(elapsed, 3)


def render_mission_phase_metrics(ledger: dict[str, Any], *, now: datetime | None = None) -> str:
    phases = ledger.get("mission_phase_metrics", [])
    if len(phases) != MISSION_PHASE_COUNT:
        raise LedgerError("Cannot render mission metrics until all 18 phases are indexed")
    instant = now or datetime.now(timezone.utc)
    counts = mission_phase_status_counts(ledger)
    task_counts = status_counts(ledger)
    source = ledger.get("mission_phase_metric_source", {})
    resume_plan = build_resume_plan(ledger, now=instant)
    mission_clock = ledger["mission_clock"]
    mission_started = _parse_utc(mission_clock["started_at"])
    mission_deadline = _parse_utc(mission_clock["deadline_at"])
    mission_elapsed = max(0.0, (instant - mission_started).total_seconds())
    mission_remaining = max(0.0, (mission_deadline - instant).total_seconds())
    mission_clock_status = "ACTIVE" if mission_remaining > 0 else "EXPIRED"
    lines = [
        MISSION_PHASE_START,
        "## Mission Phase Metrics",
        "",
        f"- Canonical source: `{source.get('path', MISSION_SOURCE_PATH.as_posix())}`; SHA-256: `{source.get('sha256', 'unavailable')}`.",
        f"- Generated at: `{instant.isoformat().replace('+00:00', 'Z')}`; ledger correlation ID: `{ledger.get('correlation_id', 'unavailable')}`.",
        f"- Phase count: {len(phases)}; PASS: {counts['PASS']}; in progress: {counts['IN_PROGRESS']}; partial: {counts['PARTIALLY_COMPLETE']}; blocked: {counts['BLOCKED']}; failed: {counts['FAILED']}; pending: {counts['PENDING']}.",
        f"- Legacy task status counts (M01-M16): verified_complete={task_counts['verified_complete']}; in_progress={task_counts['in_progress']}; partially_complete={task_counts['partially_complete']}; blocked={task_counts['blocked']}; failed={task_counts['failed']}; pending={task_counts['pending']}.",
        f"- Mission clock: status `{mission_clock_status}`; started `{mission_clock['started_at']}`; deadline `{mission_clock['deadline_at']}`; UTC wall elapsed={mission_elapsed:.3f}s; remaining={mission_remaining:.3f}s; process-active monotonic time `NOT_MEASURED`.",
        f"- Mission authored content-line candidates indexed: {ledger.get('mission_requirement_line_count', 0)}; semantic review complete: {ledger.get('mission_requirement_line_review_counts', {}).get('reviewed', 0)}; review pending: {ledger.get('mission_requirement_line_review_counts', {}).get('not_reviewed', 0)}. Counts are line locators, not semantic requirement completion.",
        f"- Acceptance mapping: {resume_plan['acceptance_mapped_requirement_line_count']} lines mapped to acceptance references; {resume_plan['reviewed_unmapped_requirement_line_count']} reviewed lines still unmapped. This is local ledger metadata, not semantic or test proof.",
        "- Requirement coverage refs mapped / indexed: " + "; ".join(
            f"{field.removesuffix('_refs')} {count}/{resume_plan['requirement_line_count']}"
            for field, count in resume_plan["requirement_coverage_mapped_counts"].items()
        ) + ". Missing refs remain unmapped and do not imply missing or present implementations.",
        f"- Resume planner: `{resume_plan['status']}`; dependency-ready task IDs: `{', '.join(resume_plan['dependency_ready_task_ids']) or 'none'}`; next candidate: `{resume_plan['next_task_id'] or 'none'}`; source-line candidates tracked / unreviewed / not assigned to a phase: {resume_plan['requirement_line_count']} / {resume_plan['unreviewed_requirement_line_count']} / {resume_plan['unassigned_requirement_line_count']}; planner authorizes execution: `False`.",
        f"- Safe local task queue: status `{resume_plan['safe_execution_status']}`; task IDs: `{', '.join(resume_plan['safe_execution_task_ids']) or 'none'}`; next safe task: `{resume_plan['next_safe_task_id'] or 'none'}`; blocked ready IDs: `{', '.join(resume_plan['blocked_dependency_ready_task_ids']) or 'none'}`; completed ready IDs: `{', '.join(resume_plan['completed_dependency_ready_task_ids']) or 'none'}`; authorization: `False`.",
        "- Completion percentage is not inferred from phase count; local PASS preconditions require indexed, reviewed, acceptance-mapped lines, per-dimension coverage refs, and phase evidence. These refs do not prove semantic truth or remote completion. Remote verification remains `False` until independently proven.",
        "",
        "| Phase | Mission scope | Source lines | Status | Recorded wall span (seconds) | Attempts | Requirement lines indexed / acceptance-mapped / pending review | Coverage refs mapped / indexed (owner/implementation/test/security/docs/integration/remote) | Local PASS preconditions | Evidence refs | Blockers | Next action |",
        "|---|---|---:|---|---:|---:|---:|---|---|---:|---|---|",
    ]
    resume_phases = {phase["id"]: phase for phase in resume_plan["phases"]}
    for phase in phases:
        safe = lambda value: str(value or "").replace("|", "\\|").replace("\n", " ").strip()
        attempts = phase.get("attempt_history", [])
        phase_plan = resume_phases[phase["id"]]
        local_gate = (
            "READY" if phase_plan["local_pass_gate_ready"] else
            "BLOCKED: " + "; ".join(phase_plan["local_pass_gate_blockers"])
        )
        coverage_summary = "; ".join(
            f"{field.removesuffix('_refs')} {count}/{phase_plan['requirement_line_count']}"
            for field, count in phase_plan["coverage_mapped_counts"].items()
        )
        lines.append(
            f"| {phase['id']} | {safe(phase.get('heading'))} | {phase.get('source_line_start')}-{phase.get('source_line_end')} | {phase['status']} | "
            f"{_phase_elapsed_seconds(phase, instant):.3f} | {len(attempts)} | {phase_plan['requirement_line_count']} / {phase_plan['acceptance_mapped_requirement_line_count']} / {phase_plan['unreviewed_requirement_line_count']} pending | "
            f"{safe(coverage_summary)} | {safe(local_gate)} | {len(phase.get('evidence_refs', []))} | {safe('; '.join(phase.get('blockers', [])) or 'None recorded')} | "
            f"{safe(phase.get('next_action') or 'Start phase and record evidence')} |"
        )
    lines.extend(["", MISSION_PHASE_END])
    return "\n".join(lines)


def refresh_paired_mission_phase_metrics(root: Path, ledger: dict[str, Any]) -> None:
    block = render_mission_phase_metrics(ledger)
    marker_pattern = re.compile(
        re.escape(MISSION_PHASE_START) + r".*?" + re.escape(MISSION_PHASE_END),
        re.DOTALL,
    )
    legacy_pattern = re.compile(
        r"^## Mission phase dashboard.*?(?=^## Live time accounting)",
        re.MULTILINE | re.DOTALL,
    )
    updated: dict[Path, str] = {}
    for relative in (Path("oe2.txt"), Path("remotecompletion.md"), Path("oe2.md")):
        path = root / relative
        if path.is_symlink() or not path.is_file():
            raise LedgerError(f"Mission metrics target is missing or symlinked: {relative.as_posix()}")
        text = path.read_text(encoding="utf-8")
        if marker_pattern.search(text):
            text, replacements = marker_pattern.subn(lambda _: block, text, count=1)
            if replacements != 1:
                raise LedgerError(f"Mission metrics markers are ambiguous in {relative.as_posix()}")
        elif legacy_pattern.search(text):
            text, replacements = legacy_pattern.subn(block + "\n\n", text, count=1)
            if replacements != 1:
                raise LedgerError(f"Legacy mission dashboard is ambiguous in {relative.as_posix()}")
        else:
            raise LedgerError(f"Mission metrics insertion point is missing in {relative.as_posix()}")
        updated[path] = text

    for path, text in updated.items():
        if path.is_symlink():
            raise LedgerError(f"Refusing to replace mission metrics through symlink: {path}")
        descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                stream.write(text)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def refresh_mission_source_hash(root: Path) -> dict[str, Any]:
    """Refresh local ledger hashes only when every mission mirror is byte-identical."""
    ledger_path = root / LEDGER_RELATIVE_PATH
    ledger = load_ledger(ledger_path)
    branch = _verify_repository_identity(root, ledger, require_target_branch=False)
    if ledger.get("remote_verified") is not False:
        raise LedgerError("Refusing local hash refresh when remote verification is not explicitly false")

    relative_paths = [
        ledger["canonical_source"]["path"],
        *ledger["canonical_source"]["byte_identical_mirrors"],
    ]
    source_bytes: list[bytes] = []
    for relative in relative_paths:
        source = root / relative
        if source.is_symlink() or not source.is_file():
            raise LedgerError(f"Mission source is missing or symlinked: {relative}")
        source_bytes.append(source.read_bytes())
    if any(content != source_bytes[0] for content in source_bytes[1:]):
        raise LedgerError("Refusing hash refresh: mission source mirrors are not byte-identical")
    observed_hash = hashlib.sha256(source_bytes[0]).hexdigest()

    invocation_id = str(uuid.uuid4())
    lock = ExecutionLock(root, "mission-task-ledger", stale_after=900)
    lock.acquire(invocation_id)
    try:
        ledger = load_ledger(ledger_path)
        branch = _verify_repository_identity(root, ledger, require_target_branch=False)
        if ledger.get("remote_verified") is not False:
            raise LedgerError("Refusing local hash refresh when remote verification is not explicitly false")
        refreshed_paths = [
            ledger["canonical_source"]["path"],
            *ledger["canonical_source"]["byte_identical_mirrors"],
        ]
        if refreshed_paths != relative_paths:
            raise LedgerError("Mission source paths changed during the hash refresh")
        source_bytes = []
        for relative in relative_paths:
            source = root / relative
            if source.is_symlink() or not source.is_file():
                raise LedgerError(f"Mission source is missing or symlinked: {relative}")
            source_bytes.append(source.read_bytes())
        if any(content != source_bytes[0] for content in source_bytes[1:]):
            raise LedgerError("Refusing hash refresh: mission source mirrors changed during refresh")
        observed_hash = hashlib.sha256(source_bytes[0]).hexdigest()
        previous_hash = ledger["canonical_source"]["sha256"]
        if previous_hash != observed_hash:
            ledger.setdefault("canonical_source", {}).setdefault("hash_history", []).append(
                {
                    "previous_sha256": previous_hash,
                    "observed_sha256": observed_hash,
                    "observed_at": utc_now(),
                    "local_branch": branch,
                    "target_branch_matches_local": branch == ledger.get("target_branch"),
                    "basis": "All listed local mission source mirrors were read and byte-compared.",
                    "remote_verified": False,
                }
            )
            ledger["canonical_source"]["sha256"] = observed_hash
            ledger["canonical_source"]["mirror_sha256"] = observed_hash
        ledger["updated_at"] = utc_now()
        validate_ledger(ledger)
        _atomic_write(ledger_path, ledger)
        checkpoint = _record_checkpoint(
            root,
            ledger_path,
            ledger,
            "mission-source-hash-refresh",
            None,
        )
        return {
            "ledger_id": ledger["ledger_id"],
            "correlation_id": ledger["correlation_id"],
            "status": "REFRESHED" if previous_hash != observed_hash else "ALREADY_CURRENT",
            "source_sha256": observed_hash,
            "mirror_count": len(relative_paths) - 1,
            "local_branch": branch,
            "target_branch": ledger["target_branch"],
            "target_branch_matches_local": branch == ledger["target_branch"],
            "checkpoint_timestamp": checkpoint["generated_at"],
            "remote_verified": False,
        }
    finally:
        lock.release(invocation_id)


def sync_mission_source(root: Path) -> dict[str, Any]:
    invocation_id = str(uuid.uuid4())
    lock = ExecutionLock(root, "mission-task-ledger", stale_after=900)
    lock.acquire(invocation_id)
    try:
        return _sync_mission_source_unlocked(root)
    finally:
        lock.release(invocation_id)


def _sync_mission_source_unlocked(root: Path) -> dict[str, Any]:
    ledger_path = root / LEDGER_RELATIVE_PATH
    ledger = load_ledger(ledger_path)
    branch = _verify_repository_identity(root, ledger, require_target_branch=True)
    source_path = root / MISSION_SOURCE_PATH
    if source_path.is_symlink() or not source_path.is_file():
        raise LedgerError("Canonical latest mission source is missing or symlinked")
    source_bytes = source_path.read_bytes()
    try:
        source_text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise LedgerError("Canonical latest mission source is not valid UTF-8") from exc
    sync_mission_phase_catalog(ledger, source_text)

    targets = [root / relative for relative in MISSION_MIRROR_PATHS]
    for relative, target in zip(MISSION_MIRROR_PATHS, targets):
        if target.is_symlink() or not target.is_file():
            raise LedgerError(f"Mission mirror is missing or symlinked: {relative.as_posix()}")
    previous_hash = ledger["canonical_source"].get("sha256")
    observed_hash = hashlib.sha256(source_bytes).hexdigest()
    for target in targets:
        descriptor, temporary = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(source_bytes)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    canonical = ledger.setdefault("canonical_source", {})
    canonical["path"] = MISSION_SOURCE_PATH.as_posix()
    canonical["byte_identical_mirrors"] = [path.as_posix() for path in MISSION_MIRROR_PATHS]
    canonical["sha256"] = observed_hash
    canonical["mirror_sha256"] = observed_hash
    canonical["mission_section_count"] = MISSION_PHASE_COUNT
    if previous_hash != observed_hash:
        canonical.setdefault("hash_history", []).append(
            {
                "previous_sha256": previous_hash,
                "observed_sha256": observed_hash,
                "observed_at": utc_now(),
                "local_branch": branch,
                "target_branch_matches_local": True,
                "basis": "Explicit user-requested adoption of latest mission.md; six established mirrors were written and byte-verified.",
                "remote_verified": False,
            }
        )
    ledger["mission_phase_catalog"] = {
        "source_path": MISSION_SOURCE_PATH.as_posix(),
        "phase_count": MISSION_PHASE_COUNT,
        "status": "ALL_PHASES_SOURCE_INDEXED; SEMANTIC_REQUIREMENT_ACCEPTANCE_MAPPING_REMAINS_IN_PROGRESS",
    }
    ledger["updated_at"] = utc_now()
    validate_ledger(ledger)
    if any(target.read_bytes() != source_bytes for target in targets):
        raise LedgerError("Mission mirror byte verification failed")
    _atomic_write(ledger_path, ledger)
    checkpoint = _record_checkpoint(root, ledger_path, ledger, "mission-source-sync", None)
    return {
        "status": "LOCAL_MIRRORS_SYNCHRONIZED",
        "source_path": MISSION_SOURCE_PATH.as_posix(),
        "source_sha256": observed_hash,
        "phase_count": MISSION_PHASE_COUNT,
        "mirror_paths": [path.as_posix() for path in MISSION_MIRROR_PATHS],
        "local_branch": branch,
        "checkpoint_timestamp": checkpoint["generated_at"],
        "remote_verified": False,
    }


def refresh_mission_metrics(root: Path) -> dict[str, Any]:
    ledger_path = root / LEDGER_RELATIVE_PATH
    ledger = load_ledger(ledger_path)
    _verify_repository(root, ledger)
    invocation_id = str(uuid.uuid4())
    lock = ExecutionLock(root, "mission-task-ledger", stale_after=900)
    lock.acquire(invocation_id)
    try:
        ledger = load_ledger(ledger_path)
        _verify_repository(root, ledger)
        source_text = (root / MISSION_SOURCE_PATH).read_text(encoding="utf-8")
        sync_mission_phase_catalog(ledger, source_text)
        ledger["updated_at"] = utc_now()
        validate_ledger(ledger)
        _atomic_write(ledger_path, ledger)
        checkpoint = _record_checkpoint(root, ledger_path, ledger, "mission-metrics-refresh", None)
        return {
            "status": "REFRESHED",
            "phase_count": len(ledger["mission_phase_metrics"]),
            "phase_status_counts": mission_phase_status_counts(ledger),
            "resume_plan": build_resume_plan(ledger),
            "checkpoint_timestamp": checkpoint["generated_at"],
            "remote_verified": False,
        }
    finally:
        lock.release(invocation_id)


def begin_new_mission_run(
    ledger: dict[str, Any],
    *,
    authorization_ref: str,
    now: str | None = None,
) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,119}", authorization_ref):
        raise LedgerError("A short, non-secret authorization reference is required")
    timestamp = now or utc_now()
    instant = _parse_utc(timestamp)
    previous_clock = ledger["mission_clock"]
    previous_deadline = _parse_utc(previous_clock["deadline_at"])
    if instant < previous_deadline:
        raise LedgerError("A new mission run can start only after the current clock expires")

    previous_ledger_id = ledger["ledger_id"]
    previous_correlation_id = ledger["correlation_id"]
    new_correlation_id = str(uuid.uuid4())
    new_ledger_id = f"newmission-120-minute-{instant.date().isoformat()}-{new_correlation_id[:8]}"
    history = ledger.setdefault("mission_run_history", [])
    history.append(
        {
            "ledger_id": previous_ledger_id,
            "correlation_id": previous_correlation_id,
            "started_at": previous_clock["started_at"],
            "deadline_at": previous_clock["deadline_at"],
            "mission_clock": dict(previous_clock),
            "archived_at": instant.isoformat().replace("+00:00", "Z"),
            "phase_status_counts": mission_phase_status_counts(ledger),
            "task_status_counts": status_counts(ledger),
            "superseded_by_ledger_id": new_ledger_id,
            "superseded_by_correlation_id": new_correlation_id,
            "authorization_ref": authorization_ref,
        }
    )
    ledger["ledger_id"] = new_ledger_id
    ledger["correlation_id"] = new_correlation_id
    ledger["mission_run_authorization"] = {
        "source": "explicit_user_request",
        "reference": authorization_ref,
        "authorized_at": instant.isoformat().replace("+00:00", "Z"),
        "scope": "local and read-only continuation; protected and remote actions remain gated",
    }
    ledger["mission_clock"] = {
        "started_at": instant.isoformat().replace("+00:00", "Z"),
        "deadline_at": (instant + timedelta(minutes=120)).isoformat().replace("+00:00", "Z"),
        "clock_source": "explicit_user_authorized_new_run",
        "monotonic_continuity_available": False,
        "checkpoint_cadence": previous_clock.get(
            "checkpoint_cadence",
            "phase/task start and finish, material outcomes, and at least every two minutes during active work when supported",
        ),
    }
    return {
        "ledger_id": new_ledger_id,
        "correlation_id": new_correlation_id,
        "mission_clock": ledger["mission_clock"],
        "archived_ledger_id": previous_ledger_id,
        "archived_correlation_id": previous_correlation_id,
        "phase_status_counts": mission_phase_status_counts(ledger),
        "task_status_counts": status_counts(ledger),
    }


def start_new_mission_run(root: Path, *, authorization_ref: str) -> dict[str, Any]:
    ledger_path = root / LEDGER_RELATIVE_PATH
    ledger = load_ledger(ledger_path)
    _verify_repository(root, ledger)
    invocation_id = str(uuid.uuid4())
    lock = ExecutionLock(root, "mission-task-ledger", stale_after=900)
    lock.acquire(invocation_id)
    try:
        ledger = load_ledger(ledger_path)
        _verify_repository(root, ledger)
        run = begin_new_mission_run(ledger, authorization_ref=authorization_ref)
        ledger["updated_at"] = utc_now()
        validate_ledger(ledger)
        _atomic_write(ledger_path, ledger)
        checkpoint = _record_checkpoint(root, ledger_path, ledger, "mission-new-run", None)
        return {
            **run,
            "checkpoint_timestamp": checkpoint["generated_at"],
            "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
            "remote_verified": False,
            "remote_mutation_performed": False,
        }
    finally:
        lock.release(invocation_id)


def _task(ledger: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in ledger["tasks"]:
        if task["id"] == task_id:
            return task
    raise LedgerError(f"Unknown mission task ID: {task_id}")


def _mission_phase(ledger: dict[str, Any], phase_id: str) -> dict[str, Any] | None:
    return next(
        (item for item in ledger.get("mission_phase_metrics", []) if item.get("id") == phase_id),
        None,
    )


def _ensure_mission_clock_open(ledger: dict[str, Any], timestamp: str) -> None:
    deadline = _parse_utc(ledger["mission_clock"]["deadline_at"])
    if _parse_utc(timestamp) >= deadline:
        raise LedgerError("Mission clock expired; task and phase transitions are paused")


def start_task(ledger: dict[str, Any], task_id: str, *, now: str | None = None) -> dict[str, Any]:
    task = _task(ledger, task_id)
    timestamp = now or utc_now()
    _ensure_mission_clock_open(ledger, timestamp)
    instant = _parse_utc(timestamp)
    prior_status = task["status"]
    attempts = task.setdefault("attempt_history", [])
    if (
        not attempts
        and prior_status in TERMINAL_TASK_STATUSES
        and task.get("elapsed_seconds") is not None
    ):
        previous_elapsed = float(task["elapsed_seconds"])
        if previous_elapsed > 0:
            attempts.append(
                {
                    "started_at": task.get("started_at"),
                    "finished_at": task.get("finished_at"),
                    "elapsed_seconds": previous_elapsed,
                    "outcome": (
                        prior_status
                        if prior_status in TERMINAL_TASK_STATUSES
                        else "INTERRUPTED_OR_RESTARTED"
                    ),
                    "active_time_known": False,
                }
            )
    if prior_status == "IN_PROGRESS":
        if attempts and attempts[-1].get("finished_at") is None:
            previous_start = _parse_utc(attempts[-1]["started_at"])
            attempts[-1].update(
                {
                    "finished_at": timestamp,
                    "elapsed_seconds": max(0.0, (instant - previous_start).total_seconds()),
                    "outcome": "INTERRUPTED_OR_RESTARTED",
                    "active_time_known": False,
                }
            )
    elif prior_status not in {"PENDING", "PARTIALLY_COMPLETE", "FAILED"}:
        raise LedgerError(f"Cannot start {task_id} while its status is {prior_status}")

    unmet = [
        dependency for dependency in task["dependencies"]
        if _task(ledger, dependency)["status"] != "VERIFIED_COMPLETE"
    ]
    if unmet and prior_status != "IN_PROGRESS":
        raise LedgerError(f"Cannot start {task_id}; dependencies are not verified: {', '.join(unmet)}")

    if attempts:
        task["retries"] = int(task.get("retries", 0)) + 1
    attempts.append(
        {
            "started_at": timestamp,
            "finished_at": None,
            "elapsed_seconds": None,
            "outcome": "IN_PROGRESS",
            "active_time_known": False,
        }
    )
    task["status"] = "IN_PROGRESS"
    task["started_at"] = task.get("started_at") or timestamp
    task["finished_at"] = None
    task["last_started_at"] = timestamp
    return task


def finish_task(
    ledger: dict[str, Any],
    task_id: str,
    status: str,
    *,
    evidence_refs: list[str],
    next_action: str,
    blocker: str | None = None,
    result: str | None = None,
    now: str | None = None,
) -> dict[str, Any]:
    if status not in TERMINAL_TASK_STATUSES:
        raise LedgerError(f"Task finish status must be one of {sorted(TERMINAL_TASK_STATUSES)}")
    task = _task(ledger, task_id)
    if task["status"] != "IN_PROGRESS":
        raise LedgerError(f"Cannot finish {task_id}; it is not in progress")
    if status == "VERIFIED_COMPLETE" and not evidence_refs:
        raise LedgerError("Verified completion requires at least one evidence reference")
    if status != "VERIFIED_COMPLETE" and not next_action.strip():
        raise LedgerError("Partial, blocked, and failed tasks require a concrete next action")
    timestamp = now or utc_now()
    _ensure_mission_clock_open(ledger, timestamp)
    instant = _parse_utc(timestamp)
    attempts = task.get("attempt_history", [])
    legacy_attempt_recovered = False
    if not attempts:
        legacy_started_at = task.get("last_started_at") or task.get("started_at")
        if not legacy_started_at:
            raise LedgerError(f"Cannot finish {task_id}; start timestamp is missing")
        legacy_started = _parse_utc(legacy_started_at)
        legacy_elapsed = (instant - legacy_started).total_seconds()
        if legacy_elapsed < 0:
            raise LedgerError("Task finish timestamp precedes its start")
        attempts.append(
            {
                "started_at": legacy_started_at,
                "finished_at": timestamp,
                "elapsed_seconds": round(legacy_elapsed, 3),
                "outcome": status,
                "active_time_known": False,
                "timing_basis": "utc_wall_interval_process_activity_unknown",
            }
        )
        task["attempt_history"] = attempts
        legacy_attempt_recovered = True
    elif attempts[-1].get("finished_at") is not None:
        raise LedgerError(f"{task_id} has no open task attempt to finish")
    if not legacy_attempt_recovered:
        started = _parse_utc(attempts[-1]["started_at"])
        elapsed = (instant - started).total_seconds()
        if elapsed < 0:
            raise LedgerError("Task finish timestamp precedes its start")
        attempts[-1].update(
            {
                "finished_at": timestamp,
                "elapsed_seconds": round(elapsed, 3),
                "outcome": status,
                "active_time_known": False,
            }
        )
    completed_attempt_seconds = sum(
        float(attempt["elapsed_seconds"])
        for attempt in attempts
        if attempt.get("elapsed_seconds") is not None
    )
    task.update(
        {
            "status": status,
            "finished_at": timestamp,
            "elapsed_seconds": round(completed_attempt_seconds, 3),
            "evidence_refs": list(dict.fromkeys([*task.get("evidence_refs", []), *evidence_refs])),
            "next_action": next_action,
            "result": result,
        }
    )
    if blocker:
        task["blockers"] = list(dict.fromkeys([*task.get("blockers", []), blocker]))
    if status == "VERIFIED_COMPLETE":
        task["blockers"] = []
    return task


def start_phase(ledger: dict[str, Any], phase_id: str, *, now: str | None = None) -> dict[str, Any]:
    phase = _mission_phase(ledger, phase_id)
    if phase is None:
        phases = ledger.get("phase_history")
        if not isinstance(phases, list):
            raise LedgerError("Mission phase history is missing")
        phase = next((item for item in phases if item.get("id") == phase_id), None)
    if phase is None:
        raise LedgerError(f"Unknown mission phase ID: {phase_id}")
    timestamp = now or utc_now()
    _ensure_mission_clock_open(ledger, timestamp)
    instant = _parse_utc(timestamp)
    attempts = phase.setdefault("attempt_history", [])
    if phase.get("status") == "IN_PROGRESS" and attempts and attempts[-1].get("finished_at") is None:
        started = _parse_utc(attempts[-1]["started_at"])
        attempts[-1].update(
            {
                "finished_at": timestamp,
                "elapsed_seconds": max(0.0, (instant - started).total_seconds()),
                "outcome": "INTERRUPTED_OR_RESTARTED",
                "active_time_known": False,
            }
        )
    elif phase.get("status") not in {"PENDING", "PARTIALLY_COMPLETE", "FAILED", "IN_PROGRESS"}:
        raise LedgerError(f"Cannot start phase {phase_id} while its status is {phase.get('status')}")
    attempts.append(
        {
            "started_at": timestamp,
            "finished_at": None,
            "elapsed_seconds": None,
            "outcome": "IN_PROGRESS",
            "active_time_known": False,
        }
    )
    phase["status"] = "IN_PROGRESS"
    phase["started_at"] = phase.get("started_at") or timestamp
    phase["finished_at"] = None
    phase["last_started_at"] = timestamp
    ledger["current_phase"] = phase_id
    return phase


def finish_phase(
    ledger: dict[str, Any],
    phase_id: str,
    status: str,
    *,
    evidence_refs: list[str],
    next_action: str,
    now: str | None = None,
) -> dict[str, Any]:
    if status not in {"PASS", "PARTIALLY_COMPLETE", "BLOCKED", "FAILED"}:
        raise LedgerError("Unsupported mission phase outcome")
    phase = _mission_phase(ledger, phase_id)
    if phase is None:
        phases = ledger.get("phase_history")
        phase = next((item for item in phases or [] if item.get("id") == phase_id), None)
    if phase is None or phase.get("status") != "IN_PROGRESS":
        raise LedgerError(f"Cannot finish phase {phase_id}; it is not in progress")
    if status == "PASS" and not evidence_refs:
        raise LedgerError("A passed phase requires evidence references")
    if status == "PASS" and re.fullmatch(r"PH\d{2}", phase_id):
        requirement_records = [
            record
            for record in ledger.get("mission_requirement_line_records", [])
            if record.get("phase_id") == phase_id
        ]
        if not requirement_records:
            raise LedgerError(f"Cannot pass {phase_id}; no indexed requirement lines are available")
        unreviewed_count = sum(not record.get("semantic_reviewed", False) for record in requirement_records)
        if unreviewed_count:
            raise LedgerError(
                f"Cannot pass {phase_id}; {unreviewed_count} unreviewed requirement lines remain"
            )
        unmapped_count = sum(not record.get("acceptance_refs") for record in requirement_records)
        if unmapped_count:
            raise LedgerError(
                f"Cannot pass {phase_id}; {unmapped_count} reviewed requirement lines lack acceptance references"
            )
        unmapped_coverage = {
            field: sum(
                not record.get("coverage_refs", {}).get(field)
                for record in requirement_records
            )
            for field in REQUIREMENT_COVERAGE_FIELDS
        }
        missing_coverage = [
            f"{count} {field}"
            for field, count in unmapped_coverage.items()
            if count
        ]
        if missing_coverage:
            raise LedgerError(
                f"Cannot pass {phase_id}; requirement lines lack coverage references: "
                + ", ".join(missing_coverage)
            )
    if status != "PASS" and not next_action.strip():
        raise LedgerError("An incomplete phase requires a concrete next action")
    timestamp = now or utc_now()
    _ensure_mission_clock_open(ledger, timestamp)
    instant = _parse_utc(timestamp)
    attempts = phase.get("attempt_history", [])
    if not attempts or attempts[-1].get("finished_at") is not None:
        raise LedgerError(f"{phase_id} has no open phase attempt to finish")
    started = _parse_utc(attempts[-1]["started_at"])
    elapsed = (instant - started).total_seconds()
    if elapsed < 0:
        raise LedgerError("Phase finish timestamp precedes its start")
    attempts[-1].update(
        {
            "finished_at": timestamp,
            "elapsed_seconds": round(elapsed, 3),
            "outcome": status,
            "active_time_known": False,
        }
    )
    phase.update(
        {
            "status": status,
            "finished_at": timestamp,
            "elapsed_seconds": round(
                sum(float(item["elapsed_seconds"]) for item in attempts if item.get("elapsed_seconds") is not None),
                3,
            ),
            "evidence_refs": list(dict.fromkeys([*phase.get("evidence_refs", []), *evidence_refs])),
            "next_action": next_action,
        }
    )
    return phase


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    if path.is_symlink():
        raise LedgerError("Refusing to replace a symlinked mission ledger")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _record_checkpoint(
    root: Path,
    ledger_path: Path,
    ledger: dict[str, Any],
    operation: str,
    task_id: str | None,
    phase_id: str | None = None,
) -> dict[str, Any]:
    digest = hashlib.sha256(ledger_path.read_bytes()).hexdigest()
    now = datetime.now(timezone.utc)
    start = _parse_utc(ledger["mission_clock"]["started_at"])
    deadline = _parse_utc(ledger["mission_clock"]["deadline_at"])
    active = _task(ledger, task_id) if task_id else None
    mission_phases = ledger.get("mission_phase_metrics", [])
    elapsed = max(0.0, (now - start).total_seconds())
    remaining = max(0.0, (deadline - now).total_seconds())
    evidence = {
        "status": "IN_PROGRESS",
        "remote_verified": False,
        "artifact_path": str(ledger_path.relative_to(root)),
        "artifact_sha256": digest,
        "artifact_bytes": ledger_path.stat().st_size,
        "artifact_refs": {
            "mission_task_ledger": {
                "path": str(ledger_path.relative_to(root)),
                "sha256": digest,
                "bytes": ledger_path.stat().st_size,
            }
        },
        "metrics": {
            "ledger_id": ledger["ledger_id"],
            "ledger_version": ledger["schema_version"],
            "ledger_sha256": digest,
            "mission_start_utc": ledger["mission_clock"]["started_at"],
            "deadline_utc": ledger["mission_clock"]["deadline_at"],
            "checkpoint_utc": now.isoformat(),
            "elapsed_seconds": round(elapsed, 3),
            "remaining_seconds": round(remaining, 3),
            "monotonic_duration_available": False,
            "mission_status_counts": status_counts(ledger),
            "mission_phase_count": len(mission_phases),
            "mission_phase_status_counts": mission_phase_status_counts(ledger),
            "mission_phase_source": ledger.get("mission_phase_metric_source"),
            "mission_requirement_line_count": ledger.get("mission_requirement_line_count", 0),
            "mission_requirement_line_review_counts": ledger.get("mission_requirement_line_review_counts", {}),
            "mission_phase_metrics": [
                {
                    "id": phase["id"],
                    "status": phase["status"],
                    "elapsed_seconds": _phase_elapsed_seconds(phase, now),
                    "attempt_count": len(phase.get("attempt_history", [])),
                    "requirement_bullet_candidates": phase.get("requirement_bullet_candidates", 0),
                    "source_ref": phase.get("source_ref"),
                }
                for phase in mission_phases
            ],
            "mission_resume_plan": build_resume_plan(ledger, now=now),
            "active_task_id": task_id,
            "active_task_status": active["status"] if active else None,
            "task_elapsed_seconds": active["elapsed_seconds"] if active else None,
            "active_phase_id": phase_id or ledger.get("current_phase"),
            "remote_verified": False,
        },
        "blockers": [
            blocker
            for task in ledger["tasks"]
            if task["status"] == "BLOCKED"
            for blocker in task.get("blockers", [])
        ],
        "next_action": active.get("next_action") if active else "Resume the highest-priority dependency-ready mission task.",
    }
    refresh_paired_mission_phase_metrics(root, ledger)
    return record_qaudit_checkpoint(
        root,
        operation,
        evidence,
        correlation_id=ledger["correlation_id"],
    )


def update_task(
    root: Path,
    operation: str,
    task_id: str,
    *,
    status: str | None = None,
    evidence_refs: list[str] | None = None,
    next_action: str = "",
    blocker: str | None = None,
    result: str | None = None,
) -> dict[str, Any]:
    ledger_path = root / LEDGER_RELATIVE_PATH
    ledger = load_ledger(ledger_path)
    _verify_repository(root, ledger)
    invocation_id = str(uuid.uuid4())
    lock = ExecutionLock(root, "mission-task-ledger", stale_after=900)
    lock.acquire(invocation_id)
    try:
        ledger = load_ledger(ledger_path)
        _verify_repository(root, ledger)
        sync_mission_phase_catalog(ledger, (root / MISSION_SOURCE_PATH).read_text(encoding="utf-8"))
        if operation == "start":
            task = start_task(ledger, task_id)
        elif operation == "finish":
            if status is None:
                raise LedgerError("Finishing a task requires a status")
            task = finish_task(
                ledger,
                task_id,
                status,
                evidence_refs=evidence_refs or [],
                next_action=next_action,
                blocker=blocker,
                result=result,
            )
        else:
            raise LedgerError(f"Unsupported mission task operation: {operation}")
        ledger["updated_at"] = utc_now()
        ledger["status_counts"] = status_counts(ledger)
        validate_ledger(ledger)
        _atomic_write(ledger_path, ledger)
        checkpoint = _record_checkpoint(root, ledger_path, ledger, f"mission-task-{operation}", task_id)
        return {
            "ledger_id": ledger["ledger_id"],
            "correlation_id": ledger["correlation_id"],
            "task_id": task_id,
            "status": task["status"],
            "task_elapsed_seconds": task.get("elapsed_seconds"),
            "status_counts": ledger["status_counts"],
            "checkpoint_timestamp": checkpoint["generated_at"],
            "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
            "remote_verified": False,
        }
    finally:
        lock.release(invocation_id)


def update_phase(
    root: Path,
    operation: str,
    phase_id: str,
    *,
    status: str | None = None,
    evidence_refs: list[str] | None = None,
    next_action: str = "",
) -> dict[str, Any]:
    ledger_path = root / LEDGER_RELATIVE_PATH
    ledger = load_ledger(ledger_path)
    _verify_repository(root, ledger)
    invocation_id = str(uuid.uuid4())
    lock = ExecutionLock(root, "mission-task-ledger", stale_after=900)
    lock.acquire(invocation_id)
    try:
        ledger = load_ledger(ledger_path)
        _verify_repository(root, ledger)
        sync_mission_phase_catalog(ledger, (root / MISSION_SOURCE_PATH).read_text(encoding="utf-8"))
        if operation == "phase-start":
            phase = start_phase(ledger, phase_id)
        elif operation == "phase-finish":
            if status is None:
                raise LedgerError("Finishing a phase requires a status")
            phase = finish_phase(
                ledger,
                phase_id,
                status,
                evidence_refs=evidence_refs or [],
                next_action=next_action,
            )
        else:
            raise LedgerError(f"Unsupported mission phase operation: {operation}")
        ledger["updated_at"] = utc_now()
        validate_ledger(ledger)
        _atomic_write(ledger_path, ledger)
        checkpoint = _record_checkpoint(root, ledger_path, ledger, operation, None, phase_id)
        return {
            "ledger_id": ledger["ledger_id"],
            "correlation_id": ledger["correlation_id"],
            "phase_id": phase_id,
            "status": phase["status"],
            "elapsed_seconds": phase.get("elapsed_seconds"),
            "checkpoint_timestamp": checkpoint["generated_at"],
            "ledger_sha256": hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
            "remote_verified": False,
        }
    finally:
        lock.release(invocation_id)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    subparsers = parser.add_subparsers(dest="operation", required=True)
    start = subparsers.add_parser("start", help="Start or resume a mission task.")
    start.add_argument("task_id", choices=[f"M{i:02d}" for i in range(1, 17)])
    finish = subparsers.add_parser("finish", help="Record an evidence-backed task outcome.")
    finish.add_argument("task_id", choices=[f"M{i:02d}" for i in range(1, 17)])
    finish.add_argument("--status", required=True, choices=sorted(TERMINAL_TASK_STATUSES))
    finish.add_argument("--evidence", action="append", default=[])
    finish.add_argument("--next-action", default="")
    finish.add_argument("--blocker")
    finish.add_argument("--result")
    new_run = subparsers.add_parser(
        "new-run",
        help="Start a separately authorized 120-minute run after expiry, preserving the previous run and statuses.",
    )
    new_run.add_argument("--authorization-ref", required=True, help="Short non-secret reference to the active user authorization.")
    phase_start = subparsers.add_parser("phase-start", help="Start or resume a mission phase.")
    phase_start.add_argument("phase_id")
    phase_finish = subparsers.add_parser("phase-finish", help="Record a mission phase outcome.")
    phase_finish.add_argument("phase_id")
    phase_finish.add_argument("--status", required=True, choices=["PASS", "PARTIALLY_COMPLETE", "BLOCKED", "FAILED"])
    phase_finish.add_argument("--evidence", action="append", default=[])
    phase_finish.add_argument("--next-action", default="")
    subparsers.add_parser(
        "refresh-source-hash",
        help="Refresh ledger hashes only after verifying byte-identical local mission mirrors.",
    )
    subparsers.add_parser("refresh-metrics", help="Refresh the canonical 18-phase catalog and dashboards.")
    subparsers.add_parser("sync-mission", help="Adopt latest mission.md and synchronize its established mirrors.")
    subparsers.add_parser("status", help="Validate and summarize the current ledger.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = args.root.resolve()
    try:
        if args.operation == "status":
            ledger = load_ledger(root / LEDGER_RELATIVE_PATH)
            local_branch = _verify_repository(root, ledger, require_target_branch=False)
            now = datetime.now(timezone.utc)
            start = _parse_utc(ledger["mission_clock"]["started_at"])
            deadline = _parse_utc(ledger["mission_clock"]["deadline_at"])
            active_tasks = {
                task["id"]: round(
                    max(
                        0.0,
                        (
                            now
                            - _parse_utc(task.get("last_started_at") or task["started_at"])
                        ).total_seconds(),
                    ),
                    3,
                )
                for task in ledger["tasks"]
                if task["status"] == "IN_PROGRESS" and (task.get("last_started_at") or task.get("started_at"))
            }
            active_phases = {
                phase["id"]: round(
                    max(
                        0.0,
                        (
                            now
                            - _parse_utc(phase.get("last_started_at") or phase["started_at"])
                        ).total_seconds(),
                    ),
                    3,
                )
                for phase in ledger.get("mission_phase_metrics", [])
                if phase["status"] == "IN_PROGRESS" and (phase.get("last_started_at") or phase.get("started_at"))
            }
            active_legacy_phases = {
                phase["id"]: round(
                    max(
                        0.0,
                        (
                            now
                            - _parse_utc(phase.get("last_started_at") or phase["started_at"])
                        ).total_seconds(),
                    ),
                    3,
                )
                for phase in ledger.get("phase_history", [])
                if phase["status"] == "IN_PROGRESS" and (phase.get("last_started_at") or phase.get("started_at"))
            }
            print(json.dumps(
                {
                    "ledger_id": ledger["ledger_id"],
                    "correlation_id": ledger["correlation_id"],
                    "status": ledger["status"],
                    "local_branch": local_branch,
                    "target_branch": ledger["target_branch"],
                    "target_branch_matches_local": local_branch == ledger["target_branch"],
                    "status_counts": status_counts(ledger),
                    "elapsed_seconds": round((now - start).total_seconds(), 3),
                    "remaining_seconds": round(max(0.0, (deadline - now).total_seconds()), 3),
                    "active_task_wall_seconds_since_latest_start": active_tasks,
                    "active_phase_wall_seconds_since_latest_start": active_phases,
                    "active_legacy_phase_wall_seconds_since_latest_start": active_legacy_phases,
                    "mission_phase_status_counts": mission_phase_status_counts(ledger),
                    "mission_phase_count": len(ledger.get("mission_phase_metrics", [])),
                    "mission_requirement_line_count": ledger.get("mission_requirement_line_count", 0),
                    "mission_requirement_line_review_counts": ledger.get("mission_requirement_line_review_counts", {}),
                    "mission_resume_plan": build_resume_plan(ledger, now=now),
                    "active_duration_basis": "UTC wall-clock interval; process-active monotonic time unavailable",
                    "remote_verified": False,
                },
                indent=2,
                sort_keys=True,
            ))
            return 0
        if args.operation == "refresh-source-hash":
            result = refresh_mission_source_hash(root)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        if args.operation == "sync-mission":
            result = sync_mission_source(root)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        if args.operation == "refresh-metrics":
            result = refresh_mission_metrics(root)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        if args.operation == "new-run":
            result = start_new_mission_run(root, authorization_ref=args.authorization_ref)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        if args.operation in {"start", "finish"}:
            result = update_task(
                root,
                args.operation,
                args.task_id,
                status=getattr(args, "status", None),
                evidence_refs=getattr(args, "evidence", []),
                next_action=getattr(args, "next_action", ""),
                blocker=getattr(args, "blocker", None),
                result=getattr(args, "result", None),
            )
        else:
            result = update_phase(
                root,
                args.operation,
                args.phase_id,
                status=getattr(args, "status", None),
                evidence_refs=getattr(args, "evidence", []),
                next_action=getattr(args, "next_action", ""),
            )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (LedgerError, OSError, RuntimeError, ValueError) as exc:
        print(f"Mission ledger update failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
