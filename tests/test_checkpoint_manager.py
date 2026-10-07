from __future__ import annotations

import json

import pytest

from scripts.checkpoint_manager import CheckpointManager


def test_checkpoint_undo_redo_and_new_write_discards_redo(tmp_path):
    manager = CheckpointManager(tmp_path)
    manager.write("run-1", {"status": "DISCOVERY", "completed_stages": []})
    manager.write("run-1", {"status": "VALIDATION", "completed_stages": ["DISCOVERY"]})

    manager.undo("run-1")
    assert manager.load("run-1")["status"] == "DISCOVERY"
    assert manager.history_status("run-1")["redo_available"] is True

    manager.redo("run-1")
    assert manager.load("run-1")["status"] == "VALIDATION"

    manager.undo("run-1")
    manager.write("run-1", {"status": "SECURITY", "completed_stages": ["DISCOVERY"]})
    assert manager.history_status("run-1")["redo_available"] is False
    with pytest.raises(RuntimeError, match="No checkpoint state"):
        manager.redo("run-1")


def test_checkpoint_history_is_bounded_and_corruption_fails_closed(tmp_path):
    manager = CheckpointManager(tmp_path)
    for index in range(manager.MAX_HISTORY_SNAPSHOTS + 10):
        manager.write("run-2", {"step": index})
    assert manager.history_status("run-2")["retained_snapshots"] == manager.MAX_HISTORY_SNAPSHOTS

    checkpoint = manager.path("run-2")
    checkpoint.write_text("{not-json", encoding="utf-8")
    with pytest.raises(RuntimeError, match="unreadable"):
        manager.load("run-2")
