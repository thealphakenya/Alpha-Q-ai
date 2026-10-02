#!/usr/bin/env python3
"""Validate JSONL telemetry and quarantine malformed legacy rows by hash."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_path, stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600)
        os.replace(temporary_path, path)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise


def _line_ending(raw_line: bytes) -> tuple[bytes, bytes]:
    if raw_line.endswith(b"\r\n"):
        return raw_line[:-2], b"\r\n"
    if raw_line.endswith((b"\n", b"\r")):
        return raw_line[:-1], raw_line[-1:]
    return raw_line, b""


def quarantine_invalid_jsonl(
    telemetry_path: Path | str,
    *,
    revision: str | None = None,
    report_path: Path | str | None = None,
) -> dict[str, Any]:
    """Replace invalid rows with hash-only quarantine events, preserving valid bytes."""
    source_path = Path(telemetry_path)
    original = source_path.read_bytes()
    source_revision = revision if revision and re.fullmatch(r"[0-9a-fA-F]{40}", revision) else None
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    repaired_lines: list[bytes] = []
    quarantined: list[dict[str, Any]] = []
    valid_rows = 0
    source_lines = original.splitlines(keepends=True)

    for line_number, raw_line in enumerate(source_lines, 1):
        row, ending = _line_ending(raw_line)
        if not row.strip():
            repaired_lines.append(raw_line)
            continue

        try:
            json.loads(row.decode("utf-8"))
        except UnicodeDecodeError:
            reason = "invalid_utf8"
        except json.JSONDecodeError:
            reason = "invalid_json"
        else:
            valid_rows += 1
            repaired_lines.append(raw_line)
            continue

        record = {
            "event": "legacy_telemetry_record_quarantined",
            "timestamp_utc": generated_at,
            "status": "quarantined",
            "phase": "integrity",
            "details": {
                "source_file": source_path.name,
                "source_line": line_number,
                "source_bytes": len(row),
                "source_sha256": hashlib.sha256(row).hexdigest(),
                "reason": reason,
                "raw_content_included": False,
                "source_revision": source_revision,
            },
        }
        quarantined.append(record["details"])
        repaired_lines.append(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        )

    if quarantined:
        _atomic_write(source_path, b"".join(repaired_lines))
        audit_path = Path(report_path) if report_path else source_path.with_name("telemetry_integrity_report.json")
        report = {
            "schema_version": "1.0",
            "status": "quarantined",
            "generated_at": generated_at,
            "source_file": source_path.name,
            "source_revision": source_revision,
            "valid_rows_preserved": valid_rows,
            "quarantined_rows": quarantined,
            "raw_content_included": False,
        }
        _atomic_write(audit_path, (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    else:
        audit_path = Path(report_path) if report_path else source_path.with_name("telemetry_integrity_report.json")
        report = {
            "schema_version": "1.0",
            "status": "clean",
            "generated_at": generated_at,
            "source_file": source_path.name,
            "source_revision": source_revision,
            "valid_rows_preserved": valid_rows,
            "quarantined_rows": [],
            "raw_content_included": False,
        }

    return {
        **report,
        "quarantined_count": len(quarantined),
        "integrity_report_path": str(audit_path) if quarantined else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=Path("ollamatracks/telemetry.jsonl"))
    parser.add_argument("--revision", default=os.getenv("GITHUB_SHA"))
    args = parser.parse_args()

    try:
        result = quarantine_invalid_jsonl(args.path, revision=args.revision)
    except OSError as exc:
        print(f"Telemetry integrity check failed: {type(exc).__name__}")
        return 1

    print(
        "Telemetry JSONL integrity: "
        f"status={result['status']} quarantined={result['quarantined_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())