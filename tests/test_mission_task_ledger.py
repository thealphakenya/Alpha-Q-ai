from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from scripts.mission_task_ledger import (
    LedgerError,
    _verify_repository,
    build_resume_plan,
    begin_new_mission_run,
    finish_phase,
    finish_task,
    load_ledger,
    mission_phase_status_counts,
    refresh_paired_mission_phase_metrics,
    render_mission_phase_metrics,
    refresh_mission_source_hash,
    start_phase,
    start_task,
    status_counts,
    sync_mission_phase_catalog,
    sync_mission_source,
    validate_ledger,
)


ROOT = Path(__file__).resolve().parents[1]


def _ledger() -> dict:
    return load_ledger(ROOT / "ollamatracks" / "mission-task-ledger.json")


def _set_task_state(ledger: dict, task_id: str, status: str) -> dict:
    task = next(item for item in ledger["tasks"] if item["id"] == task_id)
    task.update(
        {
            "status": status,
            "started_at": None,
            "finished_at": None,
            "last_started_at": None,
            "elapsed_seconds": None,
            "retries": 0,
            "attempt_history": [],
        }
    )
    ledger["status_counts"] = status_counts(ledger)
    return task


def test_ledger_contains_all_sixteen_sections_and_consistent_counts():
    ledger = _ledger()

    assert [task["id"] for task in ledger["tasks"]] == [f"M{i:02d}" for i in range(1, 17)]
    assert ledger["status_counts"] == status_counts(ledger)
    assert ledger["remote_verified"] is False


def test_task_transitions_record_actual_elapsed_time_and_require_evidence():
    ledger = _ledger()
    _set_task_state(ledger, "M04", "PENDING")
    task = start_task(ledger, "M04", now="2026-10-13T14:00:00Z")

    assert task["status"] == "IN_PROGRESS"
    with pytest.raises(LedgerError, match="evidence reference"):
        finish_task(
            ledger,
            "M04",
            "VERIFIED_COMPLETE",
            evidence_refs=[],
            next_action="",
            now="2026-10-13T14:00:30Z",
        )

    task = finish_task(
        ledger,
        "M04",
        "VERIFIED_COMPLETE",
        evidence_refs=["test://clock"],
        next_action="",
        now="2026-10-13T14:00:30Z",
    )
    assert task["elapsed_seconds"] == 30
    assert task["attempt_history"][-1]["outcome"] == "VERIFIED_COMPLETE"


def test_dependency_gate_blocks_work_until_prerequisite_is_verified():
    ledger = _ledger()

    with pytest.raises(LedgerError, match="dependencies are not verified"):
        start_task(ledger, "M05", now="2026-10-13T14:00:00Z")


def test_resuming_an_interrupted_task_preserves_attempt_history():
    ledger = _ledger()
    _set_task_state(ledger, "M04", "PENDING")
    task = start_task(ledger, "M04", now="2026-10-13T14:00:00Z")
    task = start_task(ledger, "M04", now="2026-10-13T14:02:00Z")

    assert task["status"] == "IN_PROGRESS"
    assert task["retries"] == 1
    assert task["attempt_history"][0]["outcome"] == "INTERRUPTED_OR_RESTARTED"
    assert task["attempt_history"][0]["elapsed_seconds"] == 120


def test_resuming_partially_completed_task_preserves_prior_elapsed_time():
    ledger = _ledger()
    task = next(item for item in ledger["tasks"] if item["id"] == "M04")
    task.update(
        {
            "status": "PARTIALLY_COMPLETE",
            "started_at": "2026-10-13T14:00:00Z",
            "finished_at": "2026-10-13T14:01:00Z",
            "elapsed_seconds": 60,
        }
    )
    task.pop("attempt_history", None)

    task = start_task(ledger, "M04", now="2026-10-13T14:02:00Z")
    assert task["attempt_history"][0]["elapsed_seconds"] == 60
    assert task["attempt_history"][0]["outcome"] == "PARTIALLY_COMPLETE"

    task = finish_task(
        ledger,
        "M04",
        "PARTIALLY_COMPLETE",
        evidence_refs=["test://resumed-task"],
        next_action="Continue the task.",
        now="2026-10-13T14:02:30Z",
    )
    assert task["elapsed_seconds"] == 90


def test_finishing_legacy_in_progress_task_records_wall_interval_not_active_time():
    ledger = _ledger()
    _set_task_state(ledger, "M04", "PENDING")
    task = next(item for item in ledger["tasks"] if item["id"] == "M04")
    task.update(
        {
            "status": "IN_PROGRESS",
            "started_at": "2026-10-13T14:00:00Z",
            "finished_at": None,
            "elapsed_seconds": None,
        }
    )
    task.pop("attempt_history", None)

    finished = finish_task(
        ledger,
        "M04",
        "PARTIALLY_COMPLETE",
        evidence_refs=["oe2.txt", "remotecompletion.md"],
        next_action="Resume in a newly authorized mission run.",
        now="2026-10-13T14:01:30Z",
    )

    attempt = finished["attempt_history"][-1]
    assert finished["status"] == "PARTIALLY_COMPLETE"
    assert finished["elapsed_seconds"] == 90
    assert attempt["outcome"] == "PARTIALLY_COMPLETE"
    assert attempt["active_time_known"] is False
    assert attempt["timing_basis"] == "utc_wall_interval_process_activity_unknown"


def test_finishing_legacy_in_progress_task_requires_start_timestamp():
    ledger = _ledger()
    _set_task_state(ledger, "M04", "PENDING")
    task = next(item for item in ledger["tasks"] if item["id"] == "M04")
    task.update(
        {
            "status": "IN_PROGRESS",
            "started_at": None,
            "finished_at": None,
            "last_started_at": None,
        }
    )
    task.pop("attempt_history", None)

    with pytest.raises(LedgerError, match="start timestamp is missing"):
        finish_task(
            ledger,
            "M04",
            "PARTIALLY_COMPLETE",
            evidence_refs=["oe2.txt"],
            next_action="Reconstruct timing evidence before finalizing this task.",
            now="2026-10-13T14:01:30Z",
        )


def test_phase_transitions_record_elapsed_time_and_evidence():
    ledger = _ledger()
    phase_id = "P02_REQUIREMENT_AND_CONTINUATION_INSPECTION"
    phase_record = next(item for item in ledger["phase_history"] if item["id"] == phase_id)
    phase_record.update({"status": "PENDING", "started_at": None, "finished_at": None})
    phase_record.pop("attempt_history", None)
    phase_record.pop("elapsed_seconds", None)
    phase = start_phase(ledger, phase_id, now="2026-10-13T14:00:00Z")

    assert phase["status"] == "IN_PROGRESS"
    phase = finish_phase(
        ledger,
        phase["id"],
        "PARTIALLY_COMPLETE",
        evidence_refs=["remote-completion.json"],
        next_action="Continue source reconciliation.",
        now="2026-10-13T14:01:15Z",
    )
    assert phase["elapsed_seconds"] == 75
    assert phase["status"] == "PARTIALLY_COMPLETE"


def test_canonical_phase_catalog_indexes_all_eighteen_source_headings():
    ledger = _ledger()
    mission_text = (ROOT / "latest mission.md").read_text(encoding="utf-8")

    phases = sync_mission_phase_catalog(ledger, mission_text)

    assert len(phases) == 18
    assert [phase["id"] for phase in phases] == [f"PH{i:02d}" for i in range(1, 19)]
    assert phases[16]["heading"] == "IMPLEMENT A STRUCTURED COPILOT-TO-OLLAMA BRIDGE"
    assert phases[17]["heading"] == "FINAL EXECUTION AND DELIVERABLES"
    assert sum(mission_phase_status_counts(ledger).values()) == 18


def test_resume_plan_indexes_all_phases_and_selects_only_dependency_ready_tasks():
    ledger = _ledger()
    _set_task_state(ledger, "M01", "PARTIALLY_COMPLETE")
    _set_task_state(ledger, "M04", "PARTIALLY_COMPLETE")
    original = copy.deepcopy(ledger)
    deadline = datetime.fromisoformat(
        ledger["mission_clock"]["deadline_at"].replace("Z", "+00:00")
    )

    plan = build_resume_plan(ledger, now=deadline - timedelta(seconds=1))

    assert plan["status"] == "READY_FOR_AUTHORIZED_EXECUTOR"
    assert plan["dependency_ready_task_ids"] == ["M01", "M04"]
    assert plan["next_task_id"] == "M01"
    assert plan["phase_count"] == 18
    assert plan["unreviewed_requirement_line_count"] == ledger["mission_requirement_line_count"]
    assert plan["acceptance_mapped_requirement_line_count"] == 0
    assert plan["reviewed_unmapped_requirement_line_count"] == 0
    coverage_fields = (
        "owner_refs",
        "implementation_refs",
        "test_refs",
        "security_refs",
        "documentation_refs",
        "integration_refs",
        "remote_evidence_refs",
    )
    assert plan["requirement_coverage_mapped_counts"] == {field: 0 for field in coverage_fields}
    assert plan["unassigned_requirement_line_count"] == 22
    assert plan["unassigned_unreviewed_requirement_line_count"] == 22
    phase_18 = next(phase for phase in plan["phases"] if phase["id"] == "PH18")
    assert phase_18["acceptance_mapped_requirement_line_count"] == 0
    assert phase_18["coverage_unmapped_counts"] == {
        field: phase_18["requirement_line_count"] for field in coverage_fields
    }
    assert phase_18["local_pass_gate_ready"] is False
    assert any("unreviewed_requirement_lines" in item for item in phase_18["local_pass_gate_blockers"])
    assert any("unmapped_implementation_refs" in item for item in phase_18["local_pass_gate_blockers"])
    all_planned_requirement_ids = [
        requirement_id
        for phase in plan["phases"]
        for requirement_id in (
            phase["reviewed_requirement_line_ids"]
            + phase["unreviewed_requirement_line_ids"]
        )
    ] + plan["unassigned_reviewed_requirement_line_ids"] + plan[
        "unassigned_unreviewed_requirement_line_ids"
    ]
    expected_requirement_ids = [
        record["id"] for record in ledger["mission_requirement_line_records"]
    ]
    assert len(all_planned_requirement_ids) == len(expected_requirement_ids)
    assert set(all_planned_requirement_ids) == set(expected_requirement_ids)
    planned_unreviewed_requirement_ids = {
        requirement_id
        for phase in plan["phases"]
        for requirement_id in phase["unreviewed_requirement_line_ids"]
    } | set(plan["unassigned_unreviewed_requirement_line_ids"])
    assert planned_unreviewed_requirement_ids == {
        record["id"]
        for record in ledger["mission_requirement_line_records"]
        if not record.get("semantic_reviewed", False)
    }
    assert all(phase["unreviewed_requirement_line_count"] >= 0 for phase in plan["phases"])
    assert plan["task_transitions_performed"] is False
    assert plan["execution_authorized"] is False
    assert plan["remote_mutation_performed"] is False
    assert plan["remote_verified"] is False
    assert ledger == original


def test_resume_plan_marks_fully_mapped_in_progress_phase_locally_ready():
    ledger = _ledger()
    sync_mission_phase_catalog(ledger, (ROOT / "latest mission.md").read_text(encoding="utf-8"))
    for record in ledger["mission_requirement_line_records"]:
        if record["phase_id"] == "PH18":
            record["semantic_reviewed"] = True
            record["status"] = "REVIEWED"
            record["acceptance_refs"] = ["tests/test_mission_task_ledger.py"]
            record["coverage_refs"] = {
                field: ["tests/test_mission_task_ledger.py"]
                for field in (
                    "owner_refs",
                    "implementation_refs",
                    "test_refs",
                    "security_refs",
                    "documentation_refs",
                    "integration_refs",
                    "remote_evidence_refs",
                )
            }
            record["coverage_refs"] = {
                field: ["tests/test_mission_task_ledger.py"]
                for field in (
                    "owner_refs",
                    "implementation_refs",
                    "test_refs",
                    "security_refs",
                    "documentation_refs",
                    "integration_refs",
                    "remote_evidence_refs",
                )
            }
    reviewed_count = sum(
        record["semantic_reviewed"] for record in ledger["mission_requirement_line_records"]
    )
    ledger["mission_requirement_line_review_counts"] = {
        "not_reviewed": ledger["mission_requirement_line_count"] - reviewed_count,
        "reviewed": reviewed_count,
    }
    phase = start_phase(ledger, "PH18", now="2026-10-13T14:00:00Z")
    phase["evidence_refs"] = ["tests/test_mission_task_ledger.py"]

    plan = build_resume_plan(ledger)
    phase_18 = next(item for item in plan["phases"] if item["id"] == "PH18")

    assert phase_18["local_pass_gate_ready"] is True
    assert phase_18["acceptance_mapped_requirement_line_count"] == phase_18["requirement_line_count"]
    assert phase_18["reviewed_unmapped_requirement_line_count"] == 0
    assert phase_18["local_pass_gate_blockers"] == []
    assert plan["execution_authorized"] is False
    assert plan["remote_verified"] is False


def test_resume_plan_pauses_expired_clock_without_discarding_queue():
    ledger = _ledger()
    _set_task_state(ledger, "M01", "PARTIALLY_COMPLETE")
    _set_task_state(ledger, "M04", "PARTIALLY_COMPLETE")
    deadline = datetime.fromisoformat(
        ledger["mission_clock"]["deadline_at"].replace("Z", "+00:00")
    )

    plan = build_resume_plan(ledger, now=deadline)

    assert plan["status"] == "PAUSED_EXPIRED_CLOCK"
    assert plan["deadline_expired"] is True
    assert plan["dependency_ready_task_ids"] == ["M01", "M04"]
    assert plan["next_task_id"] == "M01"
    assert plan["task_transitions_performed"] is False
    assert plan["remote_verified"] is False


def test_task_and_phase_transitions_pause_at_expired_clock_without_mutation():
    ledger = _ledger()
    _set_task_state(ledger, "M04", "PENDING")
    deadline = datetime.fromisoformat(
        ledger["mission_clock"]["deadline_at"].replace("Z", "+00:00")
    )
    deadline_text = deadline.isoformat()

    before_task_start = copy.deepcopy(ledger)
    with pytest.raises(LedgerError, match="Mission clock expired"):
        start_task(ledger, "M04", now=deadline_text)
    assert ledger == before_task_start

    start_task(ledger, "M04", now=(deadline - timedelta(seconds=30)).isoformat())
    before_task_finish = copy.deepcopy(ledger)
    with pytest.raises(LedgerError, match="Mission clock expired"):
        finish_task(
            ledger,
            "M04",
            "PARTIALLY_COMPLETE",
            evidence_refs=["test://expired-task"],
            next_action="Resume in an authorized mission run.",
            now=deadline_text,
        )
    assert ledger == before_task_finish

    before_phase_start = copy.deepcopy(ledger)
    with pytest.raises(LedgerError, match="Mission clock expired"):
        start_phase(ledger, "PH03", now=deadline_text)
    assert ledger == before_phase_start

    start_phase(ledger, "PH03", now=(deadline - timedelta(seconds=30)).isoformat())
    before_phase_finish = copy.deepcopy(ledger)
    with pytest.raises(LedgerError, match="Mission clock expired"):
        finish_phase(
            ledger,
            "PH03",
            "PARTIALLY_COMPLETE",
            evidence_refs=["test://expired-phase"],
            next_action="Resume in an authorized mission run.",
            now=deadline_text,
        )
    assert ledger == before_phase_finish


def test_new_mission_run_archives_expired_clock_and_preserves_all_statuses():
    ledger = _ledger()
    ledger["mission_clock"].update(
        {
            "started_at": "2026-10-13T13:50:19.075+00:00",
            "deadline_at": "2026-10-13T15:50:19.075+00:00",
        }
    )
    old_ledger_id = ledger["ledger_id"]
    old_correlation_id = ledger["correlation_id"]
    old_clock = copy.deepcopy(ledger["mission_clock"])
    old_task_statuses = [task["status"] for task in ledger["tasks"]]
    old_phase_statuses = [phase["status"] for phase in ledger["mission_phase_metrics"]]

    run = begin_new_mission_run(
        ledger,
        authorization_ref="active-user-request-2026-10-17",
        now="2026-10-17T02:10:00Z",
    )

    assert run["archived_ledger_id"] == old_ledger_id
    assert run["archived_correlation_id"] == old_correlation_id
    assert run["ledger_id"] != old_ledger_id
    assert run["correlation_id"] != old_correlation_id
    assert run["mission_clock"]["started_at"] == "2026-10-17T02:10:00Z"
    assert run["mission_clock"]["deadline_at"] == "2026-10-17T04:10:00Z"
    assert ledger["mission_run_history"][-1]["started_at"] == old_clock["started_at"]
    assert ledger["mission_run_history"][-1]["deadline_at"] == old_clock["deadline_at"]
    assert ledger["mission_run_history"][-1]["mission_clock"] == old_clock
    assert ledger["mission_run_history"][-1]["authorization_ref"] == "active-user-request-2026-10-17"
    assert [task["status"] for task in ledger["tasks"]] == old_task_statuses
    assert [phase["status"] for phase in ledger["mission_phase_metrics"]] == old_phase_statuses
    assert build_resume_plan(
        ledger,
        now=datetime.fromisoformat("2026-10-17T02:10:01+00:00"),
    )["status"] != "PAUSED_EXPIRED_CLOCK"
    validate_ledger(ledger)


def test_new_mission_run_rejects_early_or_missing_authorization_without_mutation():
    ledger = _ledger()
    ledger["mission_clock"].update(
        {
            "started_at": "2026-10-17T02:00:00Z",
            "deadline_at": "2026-10-17T04:00:00Z",
        }
    )
    original = copy.deepcopy(ledger)

    with pytest.raises(LedgerError, match="authorization reference"):
        begin_new_mission_run(ledger, authorization_ref="", now="2026-10-17T02:10:00Z")
    assert ledger == original

    with pytest.raises(LedgerError, match="only after the current clock expires"):
        begin_new_mission_run(
            ledger,
            authorization_ref="active-user-request-2026-10-17",
            now="2026-10-13T14:00:00Z",
        )
    assert ledger == original


def test_mission_requirement_lines_are_hash_indexed_without_copying_source_text():
    ledger = _ledger()
    mission_text = (ROOT / "latest mission.md").read_text(encoding="utf-8")
    sync_mission_phase_catalog(ledger, mission_text)

    records = ledger["mission_requirement_line_records"]
    assert ledger["mission_requirement_line_count"] == len(records)
    assert len(records) > 500
    assert len({record["id"] for record in records}) == len(records)
    assert all(record["status"] == "NOT_REVIEWED" for record in records)
    assert all(record["semantic_reviewed"] is False for record in records)
    assert all(len(record["line_sha256"]) == 64 for record in records)
    expected_coverage_fields = {
        "owner_refs",
        "implementation_refs",
        "test_refs",
        "security_refs",
        "documentation_refs",
        "integration_refs",
        "remote_evidence_refs",
    }
    assert all(set(record["coverage_refs"]) == expected_coverage_fields for record in records)
    assert all(not refs for record in records for refs in record["coverage_refs"].values())
    assert all("text" not in record and "source_text" not in record for record in records)
    assert {record["phase_id"] for record in records if record["phase_id"]} == {
        f"PH{index:02d}" for index in range(1, 19)
    }
    assert ledger["mission_requirement_line_review_counts"] == {
        "not_reviewed": len(records),
        "reviewed": 0,
    }


def test_mission_phase_transition_records_elapsed_evidence_and_status():
    ledger = _ledger()
    sync_mission_phase_catalog(ledger, (ROOT / "latest mission.md").read_text(encoding="utf-8"))
    partial_before = mission_phase_status_counts(ledger)["PARTIALLY_COMPLETE"]

    phase = start_phase(ledger, "PH18", now="2026-10-13T14:00:00Z")
    phase = finish_phase(
        ledger,
        "PH18",
        "PARTIALLY_COMPLETE",
        evidence_refs=["tests/test_mission_task_ledger.py"],
        next_action="Continue the remaining final deliverables.",
        now="2026-10-13T14:00:05Z",
    )

    assert phase["elapsed_seconds"] == 5
    assert phase["evidence_refs"] == ["tests/test_mission_task_ledger.py"]
    assert mission_phase_status_counts(ledger)["PARTIALLY_COMPLETE"] == partial_before + 1


def test_phase_cannot_pass_with_unreviewed_requirement_lines():
    ledger = _ledger()
    sync_mission_phase_catalog(ledger, (ROOT / "latest mission.md").read_text(encoding="utf-8"))
    phase = start_phase(ledger, "PH18", now="2026-10-13T14:00:00Z")

    with pytest.raises(LedgerError, match="unreviewed requirement lines"):
        finish_phase(
            ledger,
            "PH18",
            "PASS",
            evidence_refs=["tests/test_mission_task_ledger.py"],
            next_action="",
            now="2026-10-13T14:00:05Z",
        )

    assert phase["status"] == "IN_PROGRESS"
    assert phase["attempt_history"][-1]["finished_at"] is None


def test_phase_cannot_pass_without_acceptance_references():
    ledger = _ledger()
    sync_mission_phase_catalog(ledger, (ROOT / "latest mission.md").read_text(encoding="utf-8"))
    for record in ledger["mission_requirement_line_records"]:
        if record["phase_id"] == "PH18":
            record["semantic_reviewed"] = True
    phase = start_phase(ledger, "PH18", now="2026-10-13T14:00:00Z")

    with pytest.raises(LedgerError, match="lack acceptance references"):
        finish_phase(
            ledger,
            "PH18",
            "PASS",
            evidence_refs=["tests/test_mission_task_ledger.py"],
            next_action="",
            now="2026-10-13T14:00:05Z",
        )

    assert phase["status"] == "IN_PROGRESS"


def test_phase_cannot_pass_without_coverage_references():
    ledger = _ledger()
    sync_mission_phase_catalog(ledger, (ROOT / "latest mission.md").read_text(encoding="utf-8"))
    for record in ledger["mission_requirement_line_records"]:
        if record["phase_id"] == "PH18":
            record["semantic_reviewed"] = True
            record["status"] = "REVIEWED"
            record["acceptance_refs"] = ["tests/test_mission_task_ledger.py"]
    phase = start_phase(ledger, "PH18", now="2026-10-13T14:00:00Z")

    with pytest.raises(LedgerError, match="requirement lines lack coverage references"):
        finish_phase(
            ledger,
            "PH18",
            "PASS",
            evidence_refs=["tests/test_mission_task_ledger.py"],
            next_action="",
            now="2026-10-13T14:00:05Z",
        )

    assert phase["status"] == "IN_PROGRESS"
    assert phase["attempt_history"][-1]["finished_at"] is None


def test_dashboard_refresh_replaces_stale_metrics_and_preserves_later_history(tmp_path):
    ledger = _ledger()
    sync_mission_phase_catalog(ledger, (ROOT / "latest mission.md").read_text(encoding="utf-8"))
    legacy = "## Mission phase dashboard (live metrics)\nold metrics\n\n## Live time accounting\nkeep history\n"
    for name in ("oe2.txt", "remotecompletion.md", "oe2.md"):
        (tmp_path / name).write_text(legacy, encoding="utf-8")

    refresh_paired_mission_phase_metrics(tmp_path, ledger)

    for name in ("oe2.txt", "remotecompletion.md", "oe2.md"):
        refreshed = (tmp_path / name).read_text(encoding="utf-8")
        assert refreshed.count("| PH") == 18
        assert "old metrics" not in refreshed
        assert "keep history" in refreshed
        assert "Remote verification remains `False`" in refreshed


def test_mission_metrics_include_task_counts_and_elapsed_deadline_state():
    ledger = _ledger()
    clock_start = datetime.fromisoformat(
        ledger["mission_clock"]["started_at"].replace("Z", "+00:00")
    )
    clock_deadline = datetime.fromisoformat(
        ledger["mission_clock"]["deadline_at"].replace("Z", "+00:00")
    )
    task_counts = status_counts(ledger)
    expected_task_counts = (
        "- Legacy task status counts (M01-M16): "
        f"verified_complete={task_counts['verified_complete']}; "
        f"in_progress={task_counts['in_progress']}; "
        f"partially_complete={task_counts['partially_complete']}; "
        f"blocked={task_counts['blocked']}; failed={task_counts['failed']}; "
        f"pending={task_counts['pending']}."
    )

    active = render_mission_phase_metrics(
        ledger,
        now=clock_start + timedelta(minutes=30),
    )
    expired = render_mission_phase_metrics(
        ledger,
        now=clock_deadline + timedelta(seconds=10),
    )

    assert expected_task_counts in active
    assert "Mission clock: status `ACTIVE`" in active
    assert "UTC wall elapsed=1800.000s; remaining=5400.000s" in active
    assert "process-active monotonic time `NOT_MEASURED`" in active
    assert "Mission clock: status `EXPIRED`" in expired
    assert "UTC wall elapsed=7210.000s; remaining=0.000s" in expired


def test_sync_mission_source_adopts_latest_mission_and_preserves_task_ledger(tmp_path, monkeypatch):
    ledger = copy.deepcopy(_ledger())
    branch = ledger["target_branch"]
    subprocess.run(["git", "init", "-q", "-b", branch, str(tmp_path)], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "remote", "add", "origin", "https://github.com/thealphakenya/Alpha-Q-ai"],
        check=True,
    )
    source = (ROOT / "latest mission.md").read_bytes()
    (tmp_path / "latest mission.md").write_bytes(source)
    for relative in ["MISSION.md", "NEWMISSION.md", "MISSIONEW.md", "MISSIONNEW.md", "MISSIONNEWEST.md", ".github/instructions/MISSION.md"]:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"old mission\n")
    ledger_path = tmp_path / "ollamatracks" / "mission-task-ledger.json"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
    monkeypatch.setattr(
        "scripts.mission_task_ledger._record_checkpoint",
        lambda *args, **kwargs: {"generated_at": "2026-10-15T14:00:00Z"},
    )

    result = sync_mission_source(tmp_path)
    refreshed = json.loads(ledger_path.read_text(encoding="utf-8"))

    assert result["phase_count"] == 18
    assert len(refreshed["tasks"]) == 16
    assert len(refreshed["mission_phase_metrics"]) == 18
    assert refreshed["canonical_source"]["path"] == "latest mission.md"
    assert all((tmp_path / path).read_bytes() == source for path in result["mirror_paths"])


def test_malformed_ledger_is_rejected_without_success_fallback():
    ledger = copy.deepcopy(_ledger())
    ledger["tasks"].pop()

    with pytest.raises(LedgerError, match="all 16"):
        validate_ledger(ledger)


def test_read_only_status_can_report_branch_mismatch_but_updates_are_blocked(monkeypatch):
    ledger = _ledger()

    def fake_git(root, *args):
        if args == ("branch", "--show-current"):
            return "diagnostic-only-branch"
        if args == ("remote", "get-url", "origin"):
            return "https://github.com/thealphakenya/Alpha-Q-ai"
        raise AssertionError(args)

    monkeypatch.setattr("scripts.mission_task_ledger._git", fake_git)
    with pytest.raises(LedgerError, match="Refusing mission update on branch"):
        _verify_repository(ROOT, ledger)
    assert _verify_repository(ROOT, ledger, require_target_branch=False) == "diagnostic-only-branch"


def test_source_hash_refresh_requires_identical_mirrors_and_preserves_branch_blocker(tmp_path, monkeypatch):
    ledger = copy.deepcopy(_ledger())
    target_branch = ledger["target_branch"]
    branch = "diagnostic-only-branch"
    subprocess.run(["git", "init", "-q", "-b", branch, str(tmp_path)], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "remote", "add", "origin", "https://github.com/thealphakenya/Alpha-Q-ai"],
        check=True,
    )
    source_text = "# Mission source with additive local requirements\n"
    for relative in [
        ledger["canonical_source"]["path"],
        *ledger["canonical_source"]["byte_identical_mirrors"],
    ]:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source_text, encoding="utf-8")
    ledger_path = tmp_path / "ollamatracks" / "mission-task-ledger.json"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
    monkeypatch.setattr(
        "scripts.mission_task_ledger._record_checkpoint",
        lambda *args, **kwargs: {"generated_at": "2026-10-13T15:10:00Z"},
    )

    result = refresh_mission_source_hash(tmp_path)
    refreshed = json.loads(ledger_path.read_text(encoding="utf-8"))
    expected_hash = hashlib.sha256(source_text.encode("utf-8")).hexdigest()

    assert result["status"] == "REFRESHED"
    assert result["source_sha256"] == expected_hash
    assert result["local_branch"] == branch
    assert result["target_branch"] == target_branch
    assert result["target_branch_matches_local"] is False
    assert result["remote_verified"] is False
    assert refreshed["canonical_source"]["sha256"] == expected_hash
    assert refreshed["canonical_source"]["mirror_sha256"] == expected_hash
    assert refreshed["canonical_source"]["hash_history"][-1]["previous_sha256"] != expected_hash
    assert refreshed["remote_verified"] is False


def test_source_hash_refresh_fails_closed_on_mirror_drift(tmp_path, monkeypatch):
    ledger = copy.deepcopy(_ledger())
    target_branch = ledger["target_branch"]
    subprocess.run(["git", "init", "-q", "-b", target_branch, str(tmp_path)], check=True)
    subprocess.run(
        ["git", "-C", str(tmp_path), "remote", "add", "origin", "https://github.com/thealphakenya/Alpha-Q-ai"],
        check=True,
    )
    for relative in [
        ledger["canonical_source"]["path"],
        *ledger["canonical_source"]["byte_identical_mirrors"],
    ]:
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {relative}\n", encoding="utf-8")
    ledger_path = tmp_path / "ollamatracks" / "mission-task-ledger.json"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger), encoding="utf-8")

    with pytest.raises(LedgerError, match="not byte-identical"):
        refresh_mission_source_hash(tmp_path)
