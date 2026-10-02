import json

from scripts.telemetry_jsonl import quarantine_invalid_jsonl


def test_quarantine_preserves_valid_rows_and_omits_invalid_payload(tmp_path):
    telemetry = tmp_path / "telemetry.jsonl"
    report_path = tmp_path / "telemetry_integrity_report.json"
    valid_before = b'{"event":"before"}\n'
    invalid = b"legacy tracker marker\n"
    valid_after = b'{"event":"after"}\r\n'
    telemetry.write_bytes(valid_before + invalid + valid_after)

    result = quarantine_invalid_jsonl(telemetry, revision="a" * 40, report_path=report_path)
    rows = telemetry.read_bytes().splitlines(keepends=True)
    quarantine = json.loads(rows[1])
    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert result["quarantined_count"] == 1
    assert rows[0] == valid_before
    assert rows[2] == valid_after
    assert invalid not in telemetry.read_bytes()
    assert quarantine["event"] == "legacy_telemetry_record_quarantined"
    assert quarantine["details"]["source_line"] == 2
    assert quarantine["details"]["source_bytes"] == len(invalid.rstrip(b"\n"))
    assert quarantine["details"]["raw_content_included"] is False
    assert report["quarantined_rows"] == [quarantine["details"]]
    assert report["source_revision"] == "a" * 40


def test_quarantine_handles_invalid_utf8_and_is_idempotent(tmp_path):
    telemetry = tmp_path / "telemetry.jsonl"
    telemetry.write_bytes(b'{"event":"ok"}\n\xff\xfe\n')

    first = quarantine_invalid_jsonl(telemetry)
    repaired = telemetry.read_bytes()
    second = quarantine_invalid_jsonl(telemetry)

    assert first["quarantined_count"] == 1
    assert first["quarantined_rows"][0]["reason"] == "invalid_utf8"
    assert second["quarantined_count"] == 0
    assert telemetry.read_bytes() == repaired
    assert all(json.loads(line) for line in telemetry.read_text(encoding="utf-8").splitlines())


def test_clean_telemetry_is_unchanged_and_creates_no_report(tmp_path):
    telemetry = tmp_path / "telemetry.jsonl"
    original = b'{"event":"one"}\n\n{"event":"two"}\n'
    telemetry.write_bytes(original)

    result = quarantine_invalid_jsonl(telemetry)

    assert result["status"] == "clean"
    assert result["quarantined_count"] == 0
    assert telemetry.read_bytes() == original
    assert not (tmp_path / "telemetry_integrity_report.json").exists()