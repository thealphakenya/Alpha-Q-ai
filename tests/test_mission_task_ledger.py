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


def test_ledger_contains_all_sixteen_sections_and_consistent_counts():
    ledger = _ledger()

    assert [task["id"] for task in ledger["tasks"]] == [f"M{i:02d}" for i in range(1, 17)]
    assert ledger["status_counts"] == status_counts(ledger)
    assert ledger["remote_verified"] is False


def test_task_transitions_record_actual_elapsed_time_and_require_evidence():
    ledger = _ledger()
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
    task = next(item for item in ledger["tasks"] if item["id"] == "M04")
    task.update({"status": "IN_PROGRESS", "started_at": None, "finished_at": None})
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

    phase = start_phase(ledger, "PH18", now="2026-10-15T14:00:00Z")
    phase = finish_phase(
        ledger,
        "PH18",
        "PARTIALLY_COMPLETE",
        evidence_refs=["tests/test_mission_task_ledger.py"],
        next_action="Continue the remaining final deliverables.",
        now="2026-10-15T14:00:05Z",
    )

    assert phase["elapsed_seconds"] == 5
    assert phase["evidence_refs"] == ["tests/test_mission_task_ledger.py"]
    assert mission_phase_status_counts(ledger)["PARTIALLY_COMPLETE"] == partial_before + 1


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
