"""Explicit, local QSeed payload encryption using a user-managed Fernet key."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import stat
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from cryptography.fernet import Fernet, InvalidToken

from scripts.qaudit_checkpoint import record_qaudit_checkpoint

DEFAULT_VAULT_DIR = Path.home() / ".local" / "share" / "qmoi" / "qseeds"
MAX_PAYLOAD_BYTES = 16 * 1024 * 1024
QSEED_SCHEMA_VERSION = 1


class QSeedError(ValueError):
    """A safe, user-actionable QSeed validation or cryptographic error."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _external_path(raw_path: str | Path, repository_root: Path, purpose: str) -> Path:
    candidate = Path(os.path.abspath(Path(raw_path).expanduser()))
    cursor = Path(candidate.anchor)
    for component in candidate.parts[1:]:
        cursor /= component
        if cursor.is_symlink():
            raise QSeedError(f"Refusing symlinked {purpose} path")
    resolved = candidate.resolve()
    if _inside(resolved, repository_root):
        raise QSeedError(f"{purpose.capitalize()} path must be outside the repository")
    return resolved


def _read_regular_file(path: Path, purpose: str, *, max_bytes: int) -> bytes:
    if path.is_symlink():
        raise QSeedError(f"Refusing symlinked {purpose}")
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise QSeedError(f"Unable to open {purpose}: {type(exc).__name__}") from exc
    try:
        details = os.fstat(descriptor)
        if not stat.S_ISREG(details.st_mode):
            raise QSeedError(f"{purpose.capitalize()} must be a regular file")
        if details.st_size > max_bytes:
            raise QSeedError(f"{purpose.capitalize()} exceeds the {max_bytes}-byte limit")
        chunks: list[bytes] = []
        total = 0
        while chunk := os.read(descriptor, min(1024 * 1024, max_bytes + 1 - total)):
            total += len(chunk)
            if total > max_bytes:
                raise QSeedError(f"{purpose.capitalize()} exceeds the {max_bytes}-byte limit")
            chunks.append(chunk)
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _read_key(raw_path: str | Path, repository_root: Path) -> Fernet:
    key_path = _external_path(raw_path, repository_root, "key")
    try:
        descriptor = os.open(
            key_path,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        )
    except OSError as exc:
        raise QSeedError(f"Unable to open key file: {type(exc).__name__}") from exc
    try:
        details = os.fstat(descriptor)
        if (
            not stat.S_ISREG(details.st_mode)
            or stat.S_IMODE(details.st_mode) != 0o600
            or details.st_nlink != 1
        ):
            raise QSeedError(
                "Key file must be a regular owner-only mode 0600 file with a single hard link"
            )
        if details.st_size > 128:
            raise QSeedError("Key file exceeds the 128-byte limit")
        key_bytes = bytearray()
        while chunk := os.read(descriptor, 129 - len(key_bytes)):
            key_bytes.extend(chunk)
            if len(key_bytes) > 128:
                raise QSeedError("Key file exceeds the 128-byte limit")
        key = bytes(key_bytes)
    finally:
        os.close(descriptor)
    try:
        return Fernet(key.strip())
    except (TypeError, ValueError) as exc:
        raise QSeedError("Key file does not contain a valid Fernet key") from exc


def _open_directory_without_symlinks(path: Path) -> int:
    absolute = Path(os.path.abspath(path))
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(absolute.anchor, flags)
    try:
        for component in absolute.parts[1:]:
            try:
                next_descriptor = os.open(component, flags, dir_fd=descriptor)
            except FileNotFoundError:
                os.mkdir(component, mode=0o700, dir_fd=descriptor)
                next_descriptor = os.open(component, flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _write_new_private_file(path: Path, data: bytes) -> None:
    directory_descriptor = _open_directory_without_symlinks(path.parent)
    temporary_name = f".qseed-{uuid.uuid4().hex}"
    descriptor: int | None = None
    try:
        descriptor = os.open(
            temporary_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
            dir_fd=directory_descriptor,
        )
        view = memoryview(data)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("Short write while creating private QSeed file")
            view = view[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        os.link(
            temporary_name,
            path.name,
            src_dir_fd=directory_descriptor,
            dst_dir_fd=directory_descriptor,
            follow_symlinks=False,
        )
        os.fsync(directory_descriptor)
    except FileExistsError as exc:
        raise QSeedError("Refusing to overwrite an existing QSeed file") from exc
    except OSError as exc:
        raise QSeedError(
            f"Unable to create private QSeed file: {type(exc).__name__}"
        ) from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
        try:
            os.unlink(temporary_name, dir_fd=directory_descriptor)
        except FileNotFoundError:
            pass
        os.close(directory_descriptor)


def _git_value(repository_root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(repository_root), *args],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() or None


def generate_key(key_file: str | Path, repository_root: str | Path) -> dict[str, Any]:
    root = Path(repository_root).expanduser().resolve()
    target = _external_path(key_file, root, "key")
    _write_new_private_file(target, Fernet.generate_key() + b"\n")
    return {
        "status": "KEY_CREATED",
        "credential_values_recorded": False,
        "key_permissions": "0600",
        "next_action": "Back up the key securely outside this repository; QSeeds cannot be recovered without it.",
    }


def encrypt_file(
    input_path: str | Path,
    key_file: str | Path,
    repository_root: str | Path,
    *,
    output_path: str | Path | None = None,
    label: str | None = None,
    kind: str = "other",
    parent_seed_id: str | None = None,
) -> dict[str, Any]:
    root = Path(repository_root).expanduser().resolve()
    if not root.is_dir():
        raise QSeedError("Repository root must be an existing directory")
    source = Path(input_path).expanduser()
    if source.is_symlink():
        raise QSeedError("Refusing symlinked QSeed input")
    source = source.resolve()
    plaintext = _read_regular_file(source, "QSeed input", max_bytes=MAX_PAYLOAD_BYTES)
    fernet = _read_key(key_file, root)
    seed_id = str(uuid.uuid4())
    payload = {
        "schema_version": QSEED_SCHEMA_VERSION,
        "seed_id": seed_id,
        "parent_seed_id": parent_seed_id,
        "created_at": _utc_now(),
        "kind": kind,
        "label": label or source.name,
        "repository": root.name,
        "ref": _git_value(root, "symbolic-ref", "--quiet", "--short", "HEAD"),
        "source_sha": _git_value(root, "rev-parse", "HEAD"),
        "source_path": str(source),
        "content_sha256": hashlib.sha256(plaintext).hexdigest(),
        "content_bytes": len(plaintext),
        "content_base64": base64.b64encode(plaintext).decode("ascii"),
    }
    encrypted = fernet.encrypt(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    envelope = json.dumps(
        {
            "format": "qseed-fernet",
            "schema_version": QSEED_SCHEMA_VERSION,
            "ciphertext": encrypted.decode("ascii"),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    destination = (
        _external_path(output_path, root, "encrypted output")
        if output_path is not None
        else DEFAULT_VAULT_DIR / f"{seed_id}.qseed"
    )
    destination = destination.resolve()
    if _inside(destination, root):
        raise QSeedError("Encrypted output must be outside the repository")
    _write_new_private_file(destination, envelope)
    return {
        "status": "ENCRYPTED",
        "seed_id": seed_id,
        "encrypted_path": str(destination),
        "encrypted_sha256": hashlib.sha256(envelope).hexdigest(),
        "encrypted_bytes": len(envelope),
        "plaintext_persisted": False,
        "key_material_recorded": False,
    }


def decrypt_file(
    encrypted_path: str | Path,
    key_file: str | Path,
    output_path: str | Path,
    repository_root: str | Path,
) -> dict[str, Any]:
    root = Path(repository_root).expanduser().resolve()
    encrypted_source = _external_path(encrypted_path, root, "encrypted input")
    output = _external_path(output_path, root, "decrypted output")
    envelope_bytes = _read_regular_file(
        encrypted_source, "encrypted QSeed", max_bytes=MAX_PAYLOAD_BYTES * 2
    )
    try:
        envelope = json.loads(envelope_bytes)
        if (
            not isinstance(envelope, dict)
            or envelope.get("format") != "qseed-fernet"
            or envelope.get("schema_version") != QSEED_SCHEMA_VERSION
        ):
            raise QSeedError("Unsupported QSeed envelope")
        fernet = _read_key(key_file, root)
        plaintext_payload = fernet.decrypt(str(envelope["ciphertext"]).encode("ascii"))
        payload = json.loads(plaintext_payload)
        if not isinstance(payload, dict) or payload.get("schema_version") != QSEED_SCHEMA_VERSION:
            raise QSeedError("Unsupported encrypted QSeed payload")
        plaintext = base64.b64decode(payload["content_base64"], validate=True)
        if len(plaintext) > MAX_PAYLOAD_BYTES or hashlib.sha256(plaintext).hexdigest() != payload.get("content_sha256"):
            raise QSeedError("QSeed payload integrity check failed")
    except (InvalidToken, UnicodeError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        if isinstance(exc, QSeedError):
            raise
        raise QSeedError("QSeed authentication, format, or integrity validation failed") from exc
    _write_new_private_file(output, plaintext)
    return {
        "status": "DECRYPTED",
        "seed_id": str(payload.get("seed_id", "")),
        "decrypted_path": str(output),
        "decrypted_bytes": len(plaintext),
        "plaintext_sha256_verified": True,
        "key_material_recorded": False,
    }


def audit_vault(vault_dir: str | Path, repository_root: str | Path) -> dict[str, Any]:
    root = Path(repository_root).expanduser().resolve()
    directory = _external_path(vault_dir, root, "vault directory")
    if not directory.exists():
        return {
            "status": "EMPTY",
            "seed_count": 0,
            "unreadable_count": 0,
            "seeds": [],
            "plaintext_read": False,
        }
    if not directory.is_dir():
        raise QSeedError("QSeed vault path must be a directory")
    seeds = []
    unreadable = 0
    for path in sorted(directory.iterdir()):
        if path.suffix != ".qseed":
            continue
        if path.is_symlink() or not path.is_file():
            unreadable += 1
            seeds.append({"status": "UNAVAILABLE"})
            continue
        try:
            data = _read_regular_file(path, "encrypted QSeed", max_bytes=MAX_PAYLOAD_BYTES * 2)
        except (OSError, QSeedError):
            unreadable += 1
            seeds.append({"status": "UNAVAILABLE"})
            continue
        seeds.append({
            "status": "CIPHERTEXT_INTEGRITY_ONLY",
            "encrypted_sha256": hashlib.sha256(data).hexdigest(),
            "encrypted_bytes": len(data),
        })
    return {
        "status": "NEEDS_REVIEW" if unreadable else "INVENTORIED",
        "seed_count": len(seeds),
        "unreadable_count": unreadable,
        "seeds": seeds,
        "plaintext_read": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage explicitly selected QSeed payloads.")
    parser.add_argument("--repository-root", default=".")
    commands = parser.add_subparsers(dest="action", required=True)
    key_parser = commands.add_parser("generate-key")
    key_parser.add_argument("--key-file", required=True)
    encrypt_parser = commands.add_parser("encrypt")
    encrypt_parser.add_argument("--input", required=True)
    encrypt_parser.add_argument("--key-file", required=True)
    encrypt_parser.add_argument("--output")
    encrypt_parser.add_argument("--label")
    encrypt_parser.add_argument("--kind", choices=("memory", "restore-point", "dataset", "project", "research", "other"), default="other")
    encrypt_parser.add_argument("--parent-seed-id")
    decrypt_parser = commands.add_parser("decrypt")
    decrypt_parser.add_argument("--input", required=True)
    decrypt_parser.add_argument("--key-file", required=True)
    decrypt_parser.add_argument("--output", required=True)
    audit_parser = commands.add_parser("audit")
    audit_parser.add_argument("--vault-dir", default=str(DEFAULT_VAULT_DIR))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.repository_root).expanduser().resolve()
    if args.action == "generate-key":
        result = generate_key(args.key_file, root)
        checkpoint_evidence = {
            "status": result["status"],
            "metrics": {"key_created": True, "credential_values_recorded": False},
            "next_action": result["next_action"],
        }
    elif args.action == "encrypt":
        result = encrypt_file(
            args.input,
            args.key_file,
            root,
            output_path=args.output,
            label=args.label,
            kind=args.kind,
            parent_seed_id=args.parent_seed_id,
        )
        checkpoint_evidence = {
            "status": result["status"],
            "artifact_sha256": result["encrypted_sha256"],
            "artifact_bytes": result["encrypted_bytes"],
            "artifact_refs": {
                "encrypted_qseed": {
                    "status": "ciphertext_written",
                    "sha256": result["encrypted_sha256"],
                    "bytes": result["encrypted_bytes"],
                },
            },
            "metrics": {"plaintext_persisted": False, "key_material_recorded": False},
        }
    elif args.action == "decrypt":
        result = decrypt_file(args.input, args.key_file, args.output, root)
        checkpoint_evidence = {
            "status": result["status"],
            "metrics": {
                "plaintext_sha256_verified": True,
                "key_material_recorded": False,
            },
        }
    else:
        result = audit_vault(args.vault_dir, root)
        checkpoint_evidence = {
            "status": result["status"],
            "metrics": {
                "seed_count": result["seed_count"],
                "unreadable_count": result["unreadable_count"],
                "plaintext_read": False,
            },
            "blockers": (
                [f"qseed_vault_unreadable_files:{result['unreadable_count']}"]
                if result["unreadable_count"]
                else []
            ),
        }
    checkpoint = record_qaudit_checkpoint(
        root,
        f"qseed-{args.action}",
        checkpoint_evidence,
    )
    print(json.dumps({**result, "checkpoint": checkpoint}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except QSeedError as exc:
        print(f"QSeed operation blocked: {exc}", file=sys.stderr)
        raise SystemExit(2)
