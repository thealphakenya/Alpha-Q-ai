import json
from pathlib import Path

from scripts.qaudit_shard_runner import run_bounded_audit_shards


def test_bounded_audit_shards_resume_deterministically_without_source_text(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    for index in range(5):
        path = root / "docs" / f"doc-{index}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# Document {index}\nprivate prose marker {index}\n", encoding="utf-8")
    tracker = root / "ollamatracks" / "STATE.txt"
    tracker.parent.mkdir(parents=True)
    tracker.write_text("agent started\n", encoding="utf-8")

    checkpoints = []
    monkeypatch.setattr(
        "scripts.qaudit_shard_runner.record_qaudit_checkpoint",
        lambda root, operation, evidence, correlation_id=None: checkpoints.append({
            "operation": operation,
            "evidence": evidence,
            "correlation_id": correlation_id,
        }) or {"correlation_id": correlation_id},
    )

    first = run_bounded_audit_shards(root, shard_size=2, max_shards=1)
    tracker.write_text("agent updated state between invocations\n", encoding="utf-8")
    second = run_bounded_audit_shards(root, shard_size=2, max_shards=2)
    third = run_bounded_audit_shards(root, shard_size=2, max_shards=1)

    assert first["status"] == "IN_PROGRESS"
    assert first["completed_shard_numbers"] == [1]
    assert first["remaining_shard_numbers"] == [2, 3]
    assert first["remaining_shard_count"] == 2
    assert first["remaining_shard_ranges"] == [[2, 3]]
    assert second["source_manifest_sha256"] == first["source_manifest_sha256"]
    assert second["completed_shard_numbers"] == [1, 2, 3]
    assert second["remaining_shard_numbers"] == []
    assert second["status"] == "NEEDS_REVIEW"
    assert "ollamatracks/STATE.txt" in second["excluded_paths"]
    assert third["source_manifest_sha256"] == first["source_manifest_sha256"]
    assert third["shards_written_this_call"] == []
    assert len(checkpoints) == 6

    shard_path = root / second["artifact_directory"] / "shard-000001.json"
    shard = json.loads(shard_path.read_text(encoding="utf-8"))
    assert all("content" not in item for item in shard["records"])
    assert all(item["status"] == "hashed" for item in shard["records"])