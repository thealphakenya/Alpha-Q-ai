from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from scripts.mission_task_ledger import (
    LedgerError,
    _verify_repository,
    finish_phase,
    finish_task,
    load_ledger,
    refresh_mission_source_hash,
    start_phase,
    start_task,
    status_counts,
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


def test_phase_transitions_record_elapsed_time_and_evidence():
    ledger = _ledger()
    phase = start_phase(ledger, "P02_REQUIREMENT_AND_CONTINUATION_INSPECTION", now="2026-10-13T14:00:00Z")

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
