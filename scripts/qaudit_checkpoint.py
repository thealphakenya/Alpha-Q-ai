"""Persist paired, value-free QAUDITS continuation evidence."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import uuid
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

try:
    import fcntl
except ImportError:
    fcntl = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            check=True,
            timeout=15,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip()


def _canonical_repository(root: Path) -> tuple[str, bool]:
    remote = _git(root, "remote", "get-url", "origin")
    if not remote:
        return root.name, False
    match = re.fullmatch(
        r"(?:https://github\.com/|git@github\.com:)([^/\s]+)/([^/\s]+?)(?:\.git)?",
        remote,
        flags=re.IGNORECASE,
    )
    if not match:
        return root.name, False
    return f"{match.group(1)}/{match.group(2)}", True


def _append_locked(path: Path, content: bytes) -> None:
    if path.is_symlink():
        raise RuntimeError(f"Refusing to append QAUDITS evidence through symlink: {path}")
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        if fcntl is not None:
            fcntl.flock(descriptor, fcntl.LOCK_EX)
        if not stat.S_ISREG(os.fstat(descriptor).st_mode) or not content.endswith(b"\n"):
            raise RuntimeError(f"QAUDITS evidence target is not a regular newline-terminated record: {path}")
        view = memoryview(content)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError(f"Short append while writing QAUDITS evidence: {path}")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        if fcntl is not None:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    if path.is_symlink():
        raise RuntimeError(f"Refusing to replace QAUDITS JSON through symlink: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _instruction_inventory(root: Path) -> list[dict[str, Any]]:
    candidates = [
        (root / "AGENTS.md", "repository-root"),
        (root / ".github" / "copilot-instructions.md", "repository-root"),
    ]
    instruction_dir = root / ".github" / "instructions"
    if instruction_dir.is_dir():
        candidates.extend(
            (path, ".github/instructions/**")
            for path in sorted(instruction_dir.rglob("*"))
            if path.is_file()
        )

    inventory = []
    for path, scope in candidates:
        relative = path.relative_to(root).as_posix()
        record: dict[str, Any] = {"path": relative, "scope": scope}
        try:
            content = path.read_bytes()
            content.decode("utf-8")
            record.update(
                {
                    "bytes": len(content),
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "read_parse": "read_utf8; syntax_not_parsed",
                }
            )
            if not content.strip():
                record["read_parse"] = "empty_file"
        except FileNotFoundError:
            record.update({"bytes": None, "sha256": None, "read_parse": "missing"})
        except (OSError, UnicodeDecodeError) as exc:
            record.update(
                {
                    "bytes": None,
                    "sha256": None,
                    "read_parse": f"unreadable:{type(exc).__name__}",
                }
            )
        inventory.append(record)
    return inventory


def record_qaudit_checkpoint(
    root: Path | str,
    operation: str,
    evidence: Mapping[str, Any],
    *,
    correlation_id: str | None = None,
) -> dict[str, Any]:
    """Append the same checkpoint to both ledgers and refresh machine evidence."""
    target = Path(root).resolve()
    correlation_id = correlation_id or str(uuid.uuid4())
    generated_at = _utc_now()
    repository, repository_identity_verified = _canonical_repository(target)
    branch = _git(target, "symbolic-ref", "--quiet", "--short", "HEAD")
    head_sha = _git(target, "rev-parse", "HEAD")
    tree_sha = _git(target, "rev-parse", "HEAD^{tree}")
    dirty_status = _git(target, "status", "--porcelain")
    blockers = [str(item) for item in evidence.get("blockers", [])]
    if not repository_identity_verified:
        blockers.append("canonical_origin_repository_identity_unavailable")
    if not head_sha or not tree_sha:
        blockers.append("local_commit_or_tree_identity_unavailable")
    if dirty_status is None or dirty_status:
        blockers.append("worktree_dirty_or_status_unavailable")
    if evidence.get("remote_verified") is not True:
        blockers.append("target_owned_terminal_remote_sha_proof_unavailable")

    instruction_inventory = _instruction_inventory(target)
    instruction_inventory_digest = hashlib.sha256(
        json.dumps(instruction_inventory, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    instruction_failures = [
        item for item in instruction_inventory
        if item["read_parse"] in {"missing", "empty_file"}
        or item["read_parse"].startswith("unreadable:")
    ]
    if instruction_failures:
        blockers.append("repository_instruction_inventory_incomplete")

    checkpoint = {
        "correlation_id": correlation_id,
        "generated_at": generated_at,
        "repository": repository,
        "repository_identity_verified": repository_identity_verified,
        "ref": f"refs/heads/{branch}" if branch else "HEAD",
        "local_head_sha": head_sha,
        "local_tree_sha": tree_sha,
        "worktree_dirty": bool(dirty_status),
        "operation": operation,
        "status": str(evidence.get("status", "UNKNOWN")),
        "verification_level": "local_artifact_integrity_only",
        "remote_verified": False,
        "remote_mutation_performed": False,
        "source_manifest_sha256": evidence.get("source_manifest_sha256"),
        "artifact_refs": dict(evidence.get("artifact_refs", {})),
        "instruction_inventory": instruction_inventory,
        "instruction_inventory_sha256": instruction_inventory_digest,
        "artifact_path": evidence.get("artifact_path"),
        "artifact_sha256": evidence.get("artifact_sha256"),
        "artifact_bytes": evidence.get("artifact_bytes"),
        "metrics": dict(evidence.get("metrics", {})),
        "blockers": sorted(set(blockers)),
        "next_action": str(evidence.get(
            "next_action",
            "Resolve local audit blockers and obtain target-owned terminal exact-ref/SHA/tree evidence before protected completion.",
        )),
    }
    serialized = json.dumps(checkpoint, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ledger_record = {
        "schema_version": 1,
        "event_id": str(uuid.uuid4()),
        "correlation_id": correlation_id,
        "timestamp": generated_at,
        "actor_type": "autonomous_agent",
        "actor_id": "qaudit_checkpoint",
        "repository": repository,
        "stage": "LOCAL_AUDIT_EVIDENCE",
        "operation": operation,
        "request": {
            "ref": checkpoint["ref"],
            "local_head_sha": head_sha,
            "source_manifest_sha256": checkpoint["source_manifest_sha256"],
            "instruction_inventory_sha256": instruction_inventory_digest,
        },
        "response": {"status": checkpoint["status"]},
        "result": {
            "remote_verified": False,
            "remote_mutation_performed": False,
            "artifact_path": checkpoint["artifact_path"],
            "artifact_sha256": checkpoint["artifact_sha256"],
            "artifact_bytes": checkpoint["artifact_bytes"],
            "metrics": checkpoint["metrics"],
            "artifact_refs": checkpoint["artifact_refs"],
            "instruction_inventory": instruction_inventory,
            "instruction_inventory_sha256": instruction_inventory_digest,
        },
        "verification": {
            "level": checkpoint["verification_level"],
            "repository_identity_verified": repository_identity_verified,
            "terminal": False,
        },
        "diagnosis": checkpoint["blockers"],
        "next_action": checkpoint["next_action"],
        "evidence_refs": [
            "oe2.txt",
            "remotecompletion.md",
            "remote-completion.json",
            "remote-evidence-ledger.jsonl",
        ],
    }
    completion_path = target / "remote-completion.json"
    completion = json.loads(completion_path.read_text(encoding="utf-8"))
    if not isinstance(completion, dict) or not isinstance(completion.get("state"), dict):
        raise RuntimeError("remote-completion.json has an unsupported checkpoint shape")

    pair_text = (
        f"\n## Paired QAUDITS checkpoint — {generated_at}\n\n"
        f"- Correlation ID: `{correlation_id}`; repository: `{repository}`; ref: `{checkpoint['ref']}`.\n"
        f"- Local HEAD: `{head_sha or 'unavailable'}`; local tree: `{tree_sha or 'unavailable'}`; dirty: `{checkpoint['worktree_dirty']}`.\n"
        f"- Operation: `{operation}`; status: `{checkpoint['status']}`; verification: `local_artifact_integrity_only`.\n"
        f"- Source manifest: `{checkpoint['source_manifest_sha256'] or 'unavailable'}`; artifact: `{checkpoint['artifact_path'] or 'unavailable'}`; artifact SHA-256: `{checkpoint['artifact_sha256'] or 'unavailable'}`.\n"
        f"- Additional artifact references: `{json.dumps(checkpoint['artifact_refs'], sort_keys=True, separators=(',', ':'))}`.\n"
        f"- Metrics: `{json.dumps(checkpoint['metrics'], sort_keys=True, separators=(',', ':'))}`.\n"
        f"- Instruction files: `{len(instruction_inventory)}` inventoried; metadata SHA-256: `{instruction_inventory_digest}`.\n"
        f"- Remote verified: `False`; remote mutation performed: `False`.\n"
        f"- Blockers: `{json.dumps(checkpoint['blockers'], sort_keys=True, separators=(',', ':'))}`.\n"
        f"- Next action: {checkpoint['next_action']}\n"
    ).encode("utf-8")
    _append_locked(target / "oe2.txt", pair_text)
    _append_locked(target / "remotecompletion.md", pair_text)
    checkpoint["paired_document_sha256"] = {
        "oe2.txt": _sha256(target / "oe2.txt"),
        "remotecompletion.md": _sha256(target / "remotecompletion.md"),
    }
    ledger_record["result"]["paired_document_sha256"] = checkpoint["paired_document_sha256"]
    _append_locked(
        target / "remote-evidence-ledger.jsonl",
        json.dumps(ledger_record, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n",
    )

    completion["correlation_id"] = correlation_id
    completion["generated_at"] = generated_at
    completion["status"] = "LOCAL_AUDIT_RECORDED_REMOTE_COMPLETION_BLOCKED"
    completion["current_local_checkpoint"] = checkpoint
    completion["state"]["latest_qaudit_checkpoint"] = checkpoint
    completion["state"]["local_head_sha"] = head_sha
    completion["state"]["worktree_dirty"] = checkpoint["worktree_dirty"]
    completion["state"]["remote_completion"] = "BLOCKED"
    completion["state"]["remote_verified"] = False
    existing_blockers = completion.get("blockers", [])
    resolved_blockers = {
        str(item) for item in evidence.get("resolved_blockers", [])
    }
    completion["blockers"] = sorted(set(
        [str(item) for item in existing_blockers]
        + checkpoint["blockers"]
        + ["Remote completion remains blocked until independently verified target-owned terminal exact-SHA and tree evidence is recorded."]
    ) - resolved_blockers)
    _atomic_json(completion_path, completion)
    return checkpoint
