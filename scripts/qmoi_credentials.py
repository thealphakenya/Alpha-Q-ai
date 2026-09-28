#!/usr/bin/env python3
"""Secure local credential vault and read-only provider verification."""

from __future__ import annotations

import argparse
import base64
import fcntl
import hashlib
import hmac
import json
import os
import re
import subprocess
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from cryptography.fernet import Fernet, InvalidToken


VAULT_DIR = Path.home() / ".config" / "qmoi" / "credentials"
BITGET_FIELDS = ("api_key", "api_secret", "passphrase")
BITGET_SECTION = re.compile(r"(?im)^\s*#{0,6}\s*Bitget\s+\d{1,2}/\d{1,2}/\d{4}.*$")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)(api[_ -]?(?:key|secret|passphrase)|access[_ -]?(?:key|secret|token)|private[_ -]?key|client[_ -]?(?:secret|token)|(?:password|passphrase|token|secret))\s*[:=]\s*\S+"
)
SECRET_REFERENCE = re.compile(
    r"(?i)(api[_ -]?(?:key|secret|passphrase)|access[_ -]?(?:key|secret|token)|private[_ -]?key|client[_ -]?(?:secret|token)|credential(?:s)?|secret(?:s)?)"
)
AUDIT_EXCLUDED_PARTS = {".git"}
SOURCE_EXCLUDED_PARTS = {".git", "node_modules", "__pycache__", ".pytest_cache", "dist", "build", ".venv", "venv", "target", "coverage"}
SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".sh", ".bash", ".env", ".pem", ".key", ".crt"}
GIT_CREDENTIAL_PATHS = (
    "*.md", "*.mdx", "*.txt", "*.py", "*.js", "*.jsx", "*.ts", "*.tsx",
    "*.json", "*.jsonl", "*.yaml", "*.yml", "*.toml", "*.ini", "*.cfg",
    "*.conf", "*.sh", "*.env", "*.pem", "*.key", "*.crt",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _credential_category(line: str) -> str:
    lower = line.lower()
    for category, pattern in (
        ("api_key", r"api[_ -]?key|access[_ -]?key"),
        ("api_secret", r"api[_ -]?secret|secret[_ -]?key|access[_ -]?secret"),
        ("passphrase", r"passphrase"),
        ("private_key", r"private[_ -]?key"),
        ("token", r"token|client[_ -]?secret"),
        ("password", r"password"),
        ("credential_reference", r"credential|secret"),
    ):
        if re.search(pattern, lower):
            return category
    return "credential_reference"


def scan_markdown_tree(root: Path, *, excluded_roots: set[str] | None = None) -> dict[str, Any]:
    """Scan Markdown for credential references without retaining or returning line contents."""
    findings = []
    markdown_count = 0
    excluded_roots = excluded_roots or set()
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() != ".md":
            continue
        if any(part in AUDIT_EXCLUDED_PARTS for part in path.parts):
            continue
        if path.relative_to(root).parts[0] in excluded_roots:
            continue
        markdown_count += 1
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, 1):
            if not SECRET_REFERENCE.search(line):
                continue
            findings.append({
                "path": path.relative_to(root).as_posix(),
                "line": line_number,
                "category": _credential_category(line),
                "assignment_like": bool(SECRET_ASSIGNMENT.search(line)),
            })
    return {"markdown_files": markdown_count, "references": findings}


def scan_source_tree(root: Path, *, excluded_roots: set[str] | None = None) -> dict[str, Any]:
    """Scan current source/config text files while excluding generated dependency/build trees."""
    findings = []
    source_count = 0
    excluded_roots = excluded_roots or set()
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SOURCE_SUFFIXES and not path.name.lower().startswith(".env"):
            continue
        relative = path.relative_to(root)
        if any(part in SOURCE_EXCLUDED_PARTS for part in relative.parts) or relative.parts[0] in excluded_roots:
            continue
        source_count += 1
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, 1):
            if not SECRET_REFERENCE.search(line):
                continue
            findings.append({
                "path": relative.as_posix(),
                "line": line_number,
                "category": _credential_category(line),
                "assignment_like": bool(SECRET_ASSIGNMENT.search(line)),
            })
    return {"source_files": source_count, "references": findings}


def scan_local_git_history(root: Path) -> dict[str, Any]:
    """Find credential-like Markdown changes on locally available refs; emit only SHA/path metadata."""
    pattern = r"(api[_ -]?(key|secret|passphrase)|access[_ -]?(key|secret|token)|private[_ -]?key|client[_ -]?(secret|token)|(password|passphrase|token|secret))[[:space:]]*[:=][[:space:]]*[^[:space:]]+"
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "log", "--all", "--regexp-ignore-case", "--format=@@%H", "--name-only", "-G", pattern, "--", *GIT_CREDENTIAL_PATHS],
            check=True, capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"status": "unavailable", "error_class": type(exc).__name__, "matches": []}
    matches: list[dict[str, str]] = []
    current_sha = ""
    for line in result.stdout.splitlines():
        if line.startswith("@@"):
            current_sha = line[2:]
        elif line.strip() and current_sha:
            matches.append({"commit": current_sha, "path": line.strip()})
    unique = {(item["commit"], item["path"]): item for item in matches}
    return {"status": "scanned_local_refs", "matching_commit_paths": list(unique.values())}


def audit_credentials(root: Path, report_path: Path) -> dict[str, Any]:
    root = root.resolve()
    scopes = {
        "active_repository": root,
        "Alpha-Q-ai-2025": root / "Alpha-Q-ai-2025",
        "qmoi-enhanced-history-14": root / "qmoi-enhanced-history-14",
    }
    tree_reports = {}
    for name, scope in scopes.items():
        if scope.is_dir():
            excluded = {"Alpha-Q-ai-2025", "qmoi-enhanced-history-14"} if name == "active_repository" else set()
            markdown_report = scan_markdown_tree(scope, excluded_roots=excluded)
            source_report = scan_source_tree(scope, excluded_roots=excluded)
            tree_reports[name] = {
                "markdown_files": markdown_report["markdown_files"],
                "source_config_files": source_report["source_files"],
                "references": markdown_report["references"] + source_report["references"],
            }
        else:
            tree_reports[name] = {"status": "unavailable", "markdown_files": 0, "references": []}
    history_report = scan_local_git_history(root)
    try:
        commit_count = int(subprocess.run(
            ["git", "-C", str(root), "rev-list", "--all", "--count"],
            check=True, capture_output=True, text=True, timeout=30,
        ).stdout.strip())
        refs = subprocess.run(
            ["git", "-C", str(root), "for-each-ref", "--format=%(refname)"],
            check=True, capture_output=True, text=True, timeout=30,
        ).stdout.splitlines()
    except (OSError, subprocess.SubprocessError, ValueError):
        commit_count, refs = 0, []
    report = {
        "schema_version": 1,
        "audited_at": utc_now(),
        "repository_root": str(root),
        "scope": "current accessible Markdown trees plus locally available Git refs only",
        "future_or_unfetched_history": "not covered; must be refreshed after fetch or remote tree access",
        "commit_count_across_local_refs": commit_count,
        "local_ref_count": len(refs),
        "markdown_scopes": tree_reports,
        "git_history": history_report,
        "secret_values_recorded": False,
    }
    _atomic_private_write(report_path, json.dumps(report, sort_keys=True, indent=2).encode())
    return {
        "status": "completed_with_scope_limits",
        "report_path": str(report_path),
        "markdown_files": sum(item.get("markdown_files", 0) for item in tree_reports.values()),
        "current_references": sum(len(item.get("references", [])) for item in tree_reports.values()),
        "history_commit_paths": len(history_report.get("matching_commit_paths", [])),
        "local_commits": commit_count,
        "local_refs": len(refs),
    }


def _secure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path, 0o700)


def _atomic_private_write(path: Path, data: bytes) -> None:
    _secure_dir(path.parent)
    fd, temporary = tempfile.mkstemp(prefix=".qmoi-", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        os.chmod(path, 0o600)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


class CredentialVault:
    """Fernet-encrypted vault stored outside repository worktrees."""

    def __init__(self, directory: Path = VAULT_DIR):
        self.directory = Path(directory).expanduser()
        self.key_path = self.directory / "master.key"
        self.vault_path = self.directory / "vault.enc"
        self.audit_path = self.directory / "audit.jsonl"
        self.lock_path = self.directory / "vault.lock"
        _secure_dir(self.directory)
        self.fernet = Fernet(self._load_or_create_key())

    def _load_or_create_key(self) -> bytes:
        if self.key_path.exists():
            os.chmod(self.key_path, 0o600)
            return self.key_path.read_bytes()
        key = Fernet.generate_key()
        _atomic_private_write(self.key_path, key)
        return key

    @contextmanager
    def _locked(self):
        fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "a+b") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            yield

    def _read(self) -> dict[str, Any]:
        if not self.vault_path.exists():
            return {"schema_version": 1, "credentials": {}}
        try:
            return json.loads(self.fernet.decrypt(self.vault_path.read_bytes()))
        except (InvalidToken, json.JSONDecodeError) as exc:
            raise RuntimeError("Credential vault cannot be decrypted; refusing to overwrite it") from exc

    def _write(self, payload: dict[str, Any]) -> None:
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        _atomic_private_write(self.vault_path, self.fernet.encrypt(encoded))

    def _audit(self, provider: str, action: str, tags: list[str], status: str) -> None:
        event = {
            "event_id": hashlib.sha256(f"{utc_now()}:{provider}:{action}:{os.urandom(8).hex()}".encode()).hexdigest()[:24],
            "provider": provider,
            "action": action,
            "tags": tags,
            "status": status,
            "occurred_at": utc_now(),
        }
        fd = os.open(self.audit_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            os.fchmod(fd, 0o600)
            os.write(fd, (json.dumps(event, sort_keys=True) + "\n").encode())
            os.fsync(fd)
        finally:
            os.close(fd)

    def put(
        self,
        provider: str,
        fields: dict[str, str],
        *,
        tags: list[str],
        source_created_date: str | None = None,
        source_heading_date: str | None = None,
        source: str,
        verification: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not provider or not fields or any(not isinstance(v, str) or not v for v in fields.values()):
            raise ValueError("Provider and non-empty string credential fields are required")
        now = utc_now()
        with self._locked():
            payload = self._read()
            previous = payload["credentials"].get(provider, {})
            created_at = previous.get("created_at", now)
            added_at = previous.get("added_at", now)
            record_tags = {tag for tag in tags if not tag.startswith(("created_at:", "added_at:", "updated_at:", "last_verified_at:"))}
            record_tags.update({f"created_at:{created_at}", f"added_at:{added_at}", f"updated_at:{now}"})
            if (verification or {}).get("checked_at"):
                record_tags.add(f"last_verified_at:{verification['checked_at']}")
            metadata = {
                "fields": fields,
                "tags": sorted(record_tags),
                "source": source,
                "source_created_date": source_created_date,
                "source_heading_date": source_heading_date,
                "created_at": created_at,
                "added_at": added_at,
                "updated_at": now,
                "last_verified_at": (verification or {}).get("checked_at"),
                "verification": verification or {"status": "not_checked"},
            }
            payload["credentials"][provider] = metadata
            self._write(payload)
            self._audit(provider, "updated" if previous else "added", metadata["tags"], metadata["verification"]["status"])
            return {key: value for key, value in metadata.items() if key != "fields"}

    def get(self, provider: str) -> dict[str, Any] | None:
        return self._read()["credentials"].get(provider)

    def update_verification(self, provider: str, verification: dict[str, Any]) -> None:
        with self._locked():
            payload = self._read()
            record = payload["credentials"].get(provider)
            if record is None:
                raise KeyError(provider)
            now = utc_now()
            verification = dict(verification)
            balance_snapshot = verification.pop("balance_snapshot", None)
            if balance_snapshot is not None:
                record["balance_snapshot"] = balance_snapshot
                record["balance_snapshot_at"] = verification["checked_at"]
            record["verification"] = verification
            record["last_verified_at"] = verification["checked_at"]
            record["updated_at"] = now
            record["tags"] = sorted(
                {tag for tag in record["tags"] if not tag.startswith(("created_at:", "added_at:", "updated_at:", "last_verified_at:"))}
                | {
                    f"created_at:{record['created_at']}",
                    f"added_at:{record['added_at']}",
                    f"updated_at:{now}",
                    f"last_verified_at:{verification['checked_at']}",
                }
            )
            self._write(payload)
            self._audit(provider, "verification", record["tags"], verification["status"])

    def update_source_dates(self, provider: str, *, heading_date: str, created_date: str) -> None:
        with self._locked():
            payload = self._read()
            record = payload["credentials"].get(provider)
            if record is None:
                raise KeyError(provider)
            record["source_heading_date"] = heading_date
            record["source_created_date"] = created_date
            now = utc_now()
            record["updated_at"] = now
            record["tags"] = sorted(
                {tag for tag in record["tags"] if not tag.startswith("updated_at:")}
                | {f"updated_at:{now}"}
            )
            self._write(payload)
            self._audit(provider, "provenance", record["tags"], record["verification"]["status"])


def _assignment(line: str, label: str) -> str | None:
    parts = re.split(r"[:=]", line, maxsplit=1)
    if len(parts) != 2 or not re.search(rf"(?i){label}", parts[0]):
        return None
    value = parts[1].strip().split(maxsplit=1)[0].strip("`|\"'")
    return value or None


def parse_qtrade_bitget(text: str) -> tuple[dict[str, str], int, str, str]:
    """Return the final dated Bitget block's fields, offset, heading date, and reported creation date."""
    matches = list(BITGET_SECTION.finditer(text))
    if not matches:
        raise ValueError("No dated Bitget section found")
    match = matches[-1]
    tail = text[match.start():]
    date_match = re.search(r"Bitget\s+(\d{1,2})/(\d{1,2})/(\d{4})", match.group(0), re.I)
    assert date_match
    heading_date = f"{date_match.group(3)}-{int(date_match.group(2)):02d}-{int(date_match.group(1)):02d}"
    created_match = re.search(r"(?i)created\s+(\d{1,2})/(\d{1,2})/(\d{4})", tail)
    reported_created_date = (
        f"{created_match.group(3)}-{int(created_match.group(2)):02d}-{int(created_match.group(1)):02d}"
        if created_match else "unknown"
    )
    fields: dict[str, str] = {}
    for line in tail.splitlines():
        for key, label in (("api_key", r"API\s*key"), ("api_secret", r"(?:API\s*)?secret\s*key|API\s*secret"), ("passphrase", r"API\s*passphrase|passphrase")):
            value = _assignment(line, label)
            if value:
                fields[key] = value
        inline_api_key = re.search(r"(?i)API\s*key\s*(?:[:=]\s*|\s+)([A-Za-z0-9_-]{8,})", line)
        if inline_api_key:
            fields["api_key"] = inline_api_key.group(1)
    missing = sorted(set(BITGET_FIELDS) - fields.keys())
    if missing:
        raise ValueError("Bitget block is missing parseable fields: " + ", ".join(missing))
    return {key: fields[key] for key in BITGET_FIELDS}, match.start(), heading_date, reported_created_date


def verify_bitget_read_only(credentials: dict[str, str], timeout: float = 12.0) -> dict[str, Any]:
    """Sign a read-only account-assets request; never return the response body."""
    checked_at = utc_now()
    if any(not credentials.get(field) for field in BITGET_FIELDS):
        return {"status": "incomplete", "checked_at": checked_at, "http_status": None}
    timestamp = str(int(time.time() * 1000))
    request_path = "/api/v2/spot/account/assets"
    prehash = f"{timestamp}GET{request_path}".encode()
    signature = base64.b64encode(hmac.new(credentials["api_secret"].encode(), prehash, hashlib.sha256).digest()).decode()
    request = Request(
        "https://api.bitget.com" + request_path,
        headers={
            "ACCESS-KEY": credentials["api_key"],
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": credentials["passphrase"],
            "locale": "en-US",
            "Content-Type": "application/json",
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            status_code = response.status
            body = response.read(64 * 1024)
    except HTTPError as exc:
        status_code = exc.code
        body = exc.read(64 * 1024)
    except (URLError, TimeoutError, OSError):
        return {"status": "network_error", "checked_at": checked_at, "http_status": None}
    try:
        result = json.loads(body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"status": "invalid_response", "checked_at": checked_at, "http_status": status_code}
    provider_code = str(result.get("code", ""))
    success = status_code == 200 and provider_code == "00000"
    auth_rejections = {"40006", "40009", "40011", "40012", "40017", "40037"}
    outcome = {
        "status": "verified" if success else "authentication_rejected" if provider_code in auth_rejections else "request_or_permission_rejected",
        "checked_at": checked_at,
        "http_status": status_code,
        "provider_code": provider_code or None,
    }
    if success:
        rows = result.get("data")
        if isinstance(rows, dict):
            rows = [rows]
        if isinstance(rows, list):
            outcome["balance_snapshot"] = {
                "account_type": "spot",
                "observed_at": checked_at,
                "assets": [
                    {
                        "currency": str(row.get("coin", "unknown")),
                        "available": str(row.get("available", "0")),
                        "locked": str(row.get("locked", row.get("frozen", "0"))),
                        "total": str(row.get("equity", row.get("usdtEquity", ""))),
                    }
                    for row in rows if isinstance(row, dict)
                ],
            }
    return outcome


def write_qtrade_metadata(path: Path, vault: CredentialVault) -> bool:
    source = path.read_text(encoding="utf-8")
    marker = re.search(r"(?im)^## bitget 27/9/2026\s*$", source)
    record = vault.get("bitget")
    if not marker or not record:
        return False
    verification = record["verification"]
    http_status = verification.get("http_status")
    provider_code = verification.get("provider_code")
    code_note = f"; provider code `{provider_code}`" if provider_code else ""
    balance = record.get("balance_snapshot")
    balance_note = (
        f"- Read-only spot balance snapshot: captured at `{record.get('balance_snapshot_at')}` for `{len(balance.get('assets', []))}` assets; amounts remain encrypted in the vault.\n"
        if balance else "- Read-only spot balance snapshot: not available; provider verification has not succeeded.\n"
    )
    safe_tail = (
        "## bitget 27/9/2026\n\n"
        "- Credential values are stored outside the repository in the encrypted QMOI credential vault.\n"
        f"- Vault location: `{vault.vault_path}`; key location: `{vault.key_path}` (both mode `600`, parent mode `700`).\n"
        "- Setup: imported from this dated Qtrade block; timestamps and value-free audit events are recorded by `scripts/qmoi_credentials.py`.\n"
        f"- Credential creation date reported by the source: `{record.get('source_created_date') or 'unknown'}`; exact provider-side creation time was not available.\n"
        f"- Saved to the vault at `{record['added_at']}`; record created at `{record['created_at']}`; last updated at `{record['updated_at']}`.\n"
        f"- Last read-only Bitget account check: `{verification['status']}` at `{verification.get('checked_at') or 'unknown'}` (HTTP {http_status if http_status is not None else 'unavailable'}{code_note}).\n"
        + balance_note
        + "- This section contains metadata only. Never place API keys, secrets, passphrases, or tokens here.\n"
    )
    path.write_text(source[:marker.start()].rstrip() + "\n\n" + safe_tail, encoding="utf-8")
    return True


def migrate_qtrade(path: Path, vault: CredentialVault) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    fields, start, heading_date, created_date = parse_qtrade_bitget(source)
    verification = verify_bitget_read_only(fields)
    tags = ["bitget 27/9/2026", "trading", "qtrade"]
    vault.put(
        "bitget",
        fields,
        tags=tags,
        source="Qtrade.md dated Bitget section",
        source_created_date=created_date,
        source_heading_date=heading_date,
        verification=verification,
    )
    # Do not remove the source tail unless all parsed values are encrypted successfully.
    path.write_text(source[:start].rstrip() + "\n\n## bitget 27/9/2026\n", encoding="utf-8")
    write_qtrade_metadata(path, vault)
    return {"status": verification["status"], "checked_at": verification["checked_at"], "http_status": verification["http_status"], "vault_path": str(vault.vault_path)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("migrate-qtrade", "verify-bitget", "status", "audit"))
    parser.add_argument("--qtrade", type=Path, default=Path("Qtrade.md"))
    parser.add_argument("--vault-dir", type=Path, default=VAULT_DIR)
    args = parser.parse_args(argv)
    vault = CredentialVault(args.vault_dir)
    if args.command == "migrate-qtrade":
        result = migrate_qtrade(args.qtrade, vault)
    elif args.command == "audit":
        result = audit_credentials(args.qtrade.resolve().parent, vault.directory / "credential-inventory.json")
    elif args.command == "verify-bitget":
        record = vault.get("bitget")
        if not record:
            print(json.dumps({"status": "missing"}))
            return 2
        verification = verify_bitget_read_only(record["fields"])
        vault.update_verification("bitget", verification)
        write_qtrade_metadata(args.qtrade, vault)
        result = {key: value for key, value in verification.items() if key != "balance_snapshot"}
        snapshot = vault.get("bitget").get("balance_snapshot")
        if snapshot:
            result["balance_snapshot_status"] = "encrypted"
            result["balance_snapshot_at"] = snapshot["observed_at"]
            result["balance_asset_count"] = len(snapshot["assets"])
    else:
        record = vault.get("bitget")
        result = {"status": record["verification"]["status"], "tags": record["tags"], "created_at": record["created_at"], "added_at": record["added_at"], "updated_at": record["updated_at"], "last_verified_at": record["last_verified_at"], "balance_snapshot_status": "encrypted" if record.get("balance_snapshot") else "unavailable", "balance_snapshot_at": record.get("balance_snapshot_at")} if record else {"status": "missing"}
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())