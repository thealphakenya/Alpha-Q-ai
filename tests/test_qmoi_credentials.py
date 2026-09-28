import json
from pathlib import Path
import subprocess

import pytest

from scripts.qmoi_credentials import CredentialVault, audit_credentials, parse_qtrade_bitget, verify_bitget_read_only


def test_parse_dated_bitget_section_without_exposing_values():
    text = """# Trading
## Bitget 26/6/2026 TEST_API_KEY_123456
Created 27/9/2026 API Passphrase = TEST_PASSPHRASE
Secret key = TEST_SECRET_VALUE API key TEST_API_KEY_123456
"""

    fields, start, heading_date, created_date = parse_qtrade_bitget(text)

    assert fields == {
        "api_key": "TEST_API_KEY_123456",
        "api_secret": "TEST_SECRET_VALUE",
        "passphrase": "TEST_PASSPHRASE",
    }
    assert start == text.index("## Bitget")
    assert heading_date == "2026-06-26"
    assert created_date == "2026-09-27"


def test_vault_encrypts_values_and_records_timestamped_value_free_audit(tmp_path: Path):
    vault = CredentialVault(tmp_path / "credentials")
    fields = {"api_key": "TOP_SECRET_API_KEY", "api_secret": "TOP_SECRET_SECRET", "passphrase": "TOP_SECRET_PASS"}

    metadata = vault.put(
        "bitget", fields, tags=["bitget 27/9/2026"], source="test",
        source_created_date="2026-09-27", verification={"status": "not_checked", "checked_at": "2026-09-27T00:00:00Z"},
    )

    assert vault.get("bitget")["fields"] == fields
    assert metadata["added_at"] == metadata["updated_at"]
    assert metadata["created_at"]
    assert f"created_at:{metadata['created_at']}" in metadata["tags"]
    assert f"added_at:{metadata['added_at']}" in metadata["tags"]
    assert f"updated_at:{metadata['updated_at']}" in metadata["tags"]
    assert "last_verified_at:2026-09-27T00:00:00Z" in metadata["tags"]
    assert (tmp_path / "credentials" / "master.key").stat().st_mode & 0o777 == 0o600
    assert (tmp_path / "credentials" / "vault.enc").stat().st_mode & 0o777 == 0o600
    assert all(secret.encode() not in (tmp_path / "credentials" / name).read_bytes() for name in ("vault.enc", "audit.jsonl") for secret in fields.values())
    event = json.loads((tmp_path / "credentials" / "audit.jsonl").read_text().splitlines()[0])
    assert "bitget 27/9/2026" in event["tags"]
    assert all(tag.startswith(("created_at:", "added_at:", "updated_at:", "last_verified_at:")) or tag == "bitget 27/9/2026" for tag in event["tags"])
    assert not any(secret in json.dumps(event) for secret in fields.values())


def test_bitget_verification_fails_closed_for_incomplete_credentials():
    result = verify_bitget_read_only({"api_key": "only-key"})

    assert result["status"] == "incomplete"
    assert result["http_status"] is None


def test_bitget_verification_records_code_but_never_response_message(monkeypatch):
    from scripts import qmoi_credentials

    class Response:
        status = 400

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self, _size):
            return b'{"code":"40009","msg":"sensitive provider response text"}'

    monkeypatch.setattr(qmoi_credentials, "urlopen", lambda *_args, **_kwargs: Response())
    result = verify_bitget_read_only({"api_key": "test-key", "api_secret": "test-secret", "passphrase": "test-pass"})

    assert result["status"] == "authentication_rejected"
    assert result["provider_code"] == "40009"
    assert "sensitive provider response text" not in json.dumps(result)


def test_successful_bitget_read_stores_balances_encrypted_without_cli_output(monkeypatch, tmp_path: Path):
    from scripts import qmoi_credentials

    class Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self, _size):
            return b'{"code":"00000","data":[{"coin":"USDT","available":"12.34","frozen":"1.00"}]}'

    monkeypatch.setattr(qmoi_credentials, "urlopen", lambda *_args, **_kwargs: Response())
    vault = CredentialVault(tmp_path / "vault")
    vault.put("bitget", {"api_key": "K_SECRET_123", "api_secret": "S_SECRET_123", "passphrase": "P_SECRET_123"}, tags=["bitget 27/9/2026"], source="test")

    verification = verify_bitget_read_only(vault.get("bitget")["fields"])
    vault.update_verification("bitget", verification)
    public_result = {key: value for key, value in verification.items() if key != "balance_snapshot"}
    stored = vault.get("bitget")

    assert public_result["status"] == "verified"
    assert "balance_snapshot" not in public_result
    assert stored["balance_snapshot"]["assets"] == [{"currency": "USDT", "available": "12.34", "locked": "1.00", "total": ""}]
    assert b"12.34" not in (tmp_path / "vault" / "vault.enc").read_bytes()
    assert "12.34" not in (tmp_path / "vault" / "audit.jsonl").read_text()


def test_parser_rejects_incomplete_dated_bitget_section():
    with pytest.raises(ValueError, match="missing parseable fields"):
        parse_qtrade_bitget("## Bitget 27/9/2026\nSecret key = only-secret\n")


def test_migration_removes_credential_tail_after_encrypted_save(tmp_path: Path, monkeypatch):
    from scripts import qmoi_credentials

    path = tmp_path / "Qtrade.md"
    path.write_text(
        "# Existing trading notes\n\n## Bitget 26/6/2026\n"
        "Created 27/9/2026 API Passphrase = TEST_PASSPHRASE\n"
        "Secret key = TEST_SECRET_VALUE API key TEST_API_KEY_123456\n"
    )
    monkeypatch.setattr(qmoi_credentials, "verify_bitget_read_only", lambda _fields: {
        "status": "verified", "checked_at": "2026-09-27T12:00:00Z", "http_status": 200,
    })
    vault = CredentialVault(tmp_path / "vault")

    result = qmoi_credentials.migrate_qtrade(path, vault)
    qtrade = path.read_text()

    assert result["status"] == "verified"
    assert "## bitget 27/9/2026" in qtrade
    assert "TEST_PASSPHRASE" not in qtrade
    assert "TEST_SECRET_VALUE" not in qtrade
    assert "TEST_API_KEY_123456" not in qtrade
    assert "TEST_API_KEY_123456" in vault.get("bitget")["fields"]["api_key"]
    assert "Credential creation date reported by the source: `2026-09-27`" in qtrade


def test_verification_update_refreshes_qtrade_metadata_without_secrets(tmp_path: Path):
    from scripts.qmoi_credentials import write_qtrade_metadata

    path = tmp_path / "Qtrade.md"
    path.write_text("# Notes\n\n## bitget 27/9/2026\nold metadata\n")
    vault = CredentialVault(tmp_path / "vault")
    vault.put(
        "bitget", {"api_key": "K_SECRET_123", "api_secret": "S_SECRET_123", "passphrase": "P_SECRET_123"},
        tags=["bitget 27/9/2026"], source="test", verification={
            "status": "request_or_permission_rejected", "checked_at": "2026-09-27T12:00:00Z",
            "http_status": 400, "provider_code": "40085",
        },
    )

    assert write_qtrade_metadata(path, vault)
    result = path.read_text()
    assert "request_or_permission_rejected" in result
    assert "40085" in result
    assert all(secret not in result for secret in ("K_SECRET_123", "S_SECRET_123", "P_SECRET_123"))


def test_source_date_repair_updates_metadata_without_changing_secret_values(tmp_path: Path):
    vault = CredentialVault(tmp_path / "vault")
    fields = {"api_key": "K_SECRET_123", "api_secret": "S_SECRET_123", "passphrase": "P_SECRET_123"}
    vault.put("bitget", fields, tags=["bitget 27/9/2026"], source="test")

    vault.update_source_dates("bitget", heading_date="2026-06-26", created_date="2026-09-27")

    record = vault.get("bitget")
    assert record["source_heading_date"] == "2026-06-26"
    assert record["source_created_date"] == "2026-09-27"
    assert record["fields"] == fields


def test_audit_covers_materialized_markdown_and_never_persists_values(tmp_path: Path):
    root = tmp_path / "repo"
    (root / "Alpha-Q-ai-2025").mkdir(parents=True)
    (root / "qmoi-enhanced-history-14").mkdir()
    (root / "Qtrade.md").write_text("## Bitget\nAPI key = DO_NOT_PERSIST_THIS_VALUE\n")
    (root / "Alpha-Q-ai-2025" / "rotation.md").write_text("Rotate the API secret through the provider.\n")
    (root / "qmoi-enhanced-history-14" / "old.md").write_text("Passphrase: do-not-save-secret\n")
    (root / "settings.py").write_text("api_secret = CURRENT_CODE_SECRET_MUST_NOT_ESCAPE\n")
    report_path = tmp_path / "report.json"

    result = audit_credentials(root, report_path)
    report = json.loads(report_path.read_text())

    assert result["markdown_files"] == 3
    assert result["current_references"] >= 3
    assert report["secret_values_recorded"] is False
    assert report["future_or_unfetched_history"].startswith("not covered")
    assert report["markdown_scopes"]["active_repository"]["source_config_files"] >= 1
    assert "DO_NOT_PERSIST_THIS_VALUE" not in report_path.read_text()
    assert "do-not-save-secret" not in report_path.read_text()
    assert "CURRENT_CODE_SECRET_MUST_NOT_ESCAPE" not in report_path.read_text()
    assert report_path.stat().st_mode & 0o777 == 0o600


def test_git_history_audit_reports_commit_and_path_without_secret_values(tmp_path: Path):
    root = tmp_path / "history-repo"
    root.mkdir()
    subprocess.run(["git", "init", str(root)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
    secret_marker = "HISTORICAL_TEST_SECRET_MUST_NOT_ESCAPE"
    (root / "credential-notes.md").write_text(f"API key = {secret_marker}\n")
    (root / "settings.py").write_text("api_secret = HISTORICAL_CODE_SECRET_MUST_NOT_ESCAPE\n")
    subprocess.run(["git", "-C", str(root), "add", "credential-notes.md"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "settings.py"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-m", "test credential history"], check=True, capture_output=True)

    result = audit_credentials(root, tmp_path / "history-report.json")
    report_text = (tmp_path / "history-report.json").read_text()
    report = json.loads(report_text)

    assert result["history_commit_paths"] == 2
    assert {item["path"] for item in report["git_history"]["matching_commit_paths"]} == {"credential-notes.md", "settings.py"}
    assert secret_marker not in report_text
    assert "HISTORICAL_CODE_SECRET_MUST_NOT_ESCAPE" not in report_text