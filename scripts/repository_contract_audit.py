#!/usr/bin/env python3
"""Audit repository contract surfaces without mutating either repository."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

INVENTORY_FILES = ("API.md", "ENDPOINTS.md", "ROUTES.md", "ALLPORTS.md")
SOURCE_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}
CANONICAL_ROOTS = (".", "Alpha-Q-ai-2025", "qmoi-enhanced-history-14")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _file_record(path: Path, root: Path) -> dict[str, Any]:
    content = path.read_bytes()
    return {
        "path": path.relative_to(root).as_posix(),
        "exists": True,
        "bytes": len(content),
        "lines": content.count(b"\n"),
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def _source_files(root: Path) -> list[str]:
    return sorted(
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.suffix.lower() in SOURCE_EXTENSIONS
    )


def _candidate_apps(root: Path, source_files: Iterable[str]) -> list[str]:
    names: set[str] = set()
    for relative in source_files:
        parts = Path(relative).parts
        if len(parts) > 1 and parts[0].lower() not in {"scripts", "src", "tests", "lib", "docs"}:
            names.add(parts[0])
    return sorted(names, key=str.casefold)


def _remote_state(repository: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repository), "ls-remote", "--heads", "origin", "main", "autosync-backup"],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "REMOTE_STATUS_UNAVAILABLE", "reachable": False, "error": str(exc)}
    if result.returncode != 0:
        return {
            "status": "REMOTE_STATUS_UNAVAILABLE",
            "reachable": False,
            "error": result.stderr.strip() or "git ls-remote failed",
        }
    refs = {}
    for line in result.stdout.splitlines():
        sha, separator, ref = line.partition("\t")
        if separator and ref.startswith("refs/heads/"):
            refs[ref.removeprefix("refs/heads/")] = sha
    main_sha = refs.get("main")
    backup_sha = refs.get("autosync-backup")
    return {
        "status": "REMOTE_VERIFIED" if main_sha and backup_sha else "REMOTE_STATUS_UNKNOWN",
        "reachable": True,
        "refs": refs,
        "main_sha": main_sha,
        "backup_sha": backup_sha,
        "backup_matches_main": bool(main_sha and backup_sha and main_sha == backup_sha),
    }


def audit_repository_contract(root: Path | str, source_roots: Iterable[str] = CANONICAL_ROOTS) -> dict[str, Any]:
    """Return evidence for inventory docs and source-tree contract inputs."""
    repository = Path(root).resolve()
    inventory: dict[str, Any] = {}
    missing_inventory: list[str] = []
    for name in INVENTORY_FILES:
        path = repository / name
        if path.is_file():
            inventory[name] = _file_record(path, repository)
        else:
            inventory[name] = {"path": name, "exists": False}
            missing_inventory.append(name)

    roots: dict[str, Any] = {}
    for relative in source_roots:
        source_root = repository / relative
        files = _source_files(source_root) if source_root.is_dir() else []
        root_missing_inventory = [
            name for name in INVENTORY_FILES if not (source_root / name).is_file()
        ] if source_root.is_dir() else list(INVENTORY_FILES)
        roots[relative] = {
            "exists": source_root.is_dir(),
            "source_file_count": len(files),
            "source_files_sha256": hashlib.sha256("\n".join(files).encode()).hexdigest(),
            "candidate_apps": _candidate_apps(source_root, files),
            "inventory_files": [
                name for name in INVENTORY_FILES if (source_root / name).is_file()
            ],
            "missing_inventory_files": root_missing_inventory,
        }

    existing_roots = [name for name, record in roots.items() if record["exists"]]
    remote = _remote_state(repository)
    return {
        "generated": utc_now(),
        "repository": str(repository),
        "remote_only": True,
        "inventory_files": inventory,
        "missing_inventory_files": missing_inventory,
        "source_roots": roots,
        "available_source_roots": existing_roots,
        "remote_state": remote,
        "parity_proven": False,
        "status": "READY" if not missing_inventory and existing_roots else "BLOCKED",
        "blockers": (
            ([f"missing inventory file: {name}" for name in missing_inventory])
            + (["no canonical or historical source root is materialized"] if not existing_roots else [])
        ),
        "next_actions": [
            "compare inventory contents and source manifests in target-owned remote workflow",
            "record duplicate and variant path decisions before any merge mutation",
        ],
    }


def write_audit_report(root: Path | str, report: dict[str, Any]) -> Path:
    repository = Path(root).resolve()
    target = repository / "ollamatracks" / "repository_contract_audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write", action="store_true", help="Write the audit report under ollamatracks")
    args = parser.parse_args()
    report = audit_repository_contract(args.root)
    if args.write:
        report["report_path"] = str(write_audit_report(args.root, report))
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
