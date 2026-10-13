"""Update the canonical, time-bounded NEWMISSION task ledger safely."""
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


def _task(ledger: dict[str, Any], task_id: str) -> dict[str, Any]:
    for task in ledger["tasks"]:
        if task["id"] == task_id:
            return task
    raise LedgerError(f"Unknown mission task ID: {task_id}")


def start_task(ledger: dict[str, Any], task_id: str, *, now: str | None = None) -> dict[str, Any]:
    task = _task(ledger, task_id)
    timestamp = now or utc_now()
    instant = _parse_utc(timestamp)
    prior_status = task["status"]
    if prior_status == "IN_PROGRESS":
        attempts = task.setdefault("attempt_history", [])
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

    attempts = task.setdefault("attempt_history", [])
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
    instant = _parse_utc(timestamp)
    attempts = task.get("attempt_history", [])
    if not attempts or attempts[-1].get("finished_at") is not None:
        raise LedgerError(f"{task_id} has no open task attempt to finish")
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
    phases = ledger.get("phase_history")
    if not isinstance(phases, list):
        raise LedgerError("Mission phase history is missing")
    phase = next((item for item in phases if item.get("id") == phase_id), None)
    if phase is None:
        raise LedgerError(f"Unknown mission phase ID: {phase_id}")
    timestamp = now or utc_now()
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
    phases = ledger.get("phase_history")
    phase = next((item for item in phases or [] if item.get("id") == phase_id), None)
    if phase is None or phase.get("status") != "IN_PROGRESS":
        raise LedgerError(f"Cannot finish phase {phase_id}; it is not in progress")
    if status == "PASS" and not evidence_refs:
        raise LedgerError("A passed phase requires evidence references")
    if status != "PASS" and not next_action.strip():
        raise LedgerError("An incomplete phase requires a concrete next action")
    timestamp = now or utc_now()
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
