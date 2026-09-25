"""Inventory documented and executable workspace commands.

The inventory is metadata-only: it reads Markdown and source files, records
command evidence, and updates the generated Commands section in
``ALLMDFILESREFS.md``. It never executes commands or mutates target repos.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any


COMMAND_PATTERNS = (
    re.compile(r"(?m)^\s*(?:bash|sh|python(?:3)?|pytest|gh|git)\s+[^\n`]+"),
    re.compile(r"(?m)^\s*q\s+(?:status|health|sync|validate|workflows|evidence|repair|logs|release|deploy)\b[^\n`]*"),
    re.compile(r"(?m)^\s*python\s+scripts/[^\n`]+"),
)
COMMAND_NAMING_PATTERN = re.compile(r"(?:^|[-_.])(command|commands|cli|quickstart|runbook|terminal|shell|workflow)(?:[-_.]|$)", re.IGNORECASE)
EXCLUDED_PARTS = {".git", "node_modules", "dist", "build", "coverage", "__pycache__"}


def _command_lines(text: str) -> list[str]:
    found: set[str] = set()
    for pattern in COMMAND_PATTERNS:
        for match in pattern.findall(text):
            command = " ".join(match.strip().split())
            if command:
                found.add(command)
    return sorted(found)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def inventory_commands(root: Path | str) -> dict[str, Any]:
    """Return command-bearing Markdown files and command-named Markdown files."""
    base = Path(root).resolve()
    records: list[dict[str, Any]] = []
    for path in sorted(base.rglob("*.md")):
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        relative = path.relative_to(base).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        commands = _command_lines(text)
        named = bool(COMMAND_NAMING_PATTERN.search(path.stem))
        if not commands and not named:
            continue
        records.append({
            "path": relative,
            "sha256": _sha256(path),
            "commands": commands,
            "command_count": len(commands),
            "name_matches_commands": named,
        })
    return {
        "root": str(base),
        "markdown_files_with_commands": [item for item in records if item["commands"]],
        "markdown_files_named_for_commands": [item for item in records if item["name_matches_commands"]],
        "files": len(records),
        "command_count": sum(item["command_count"] for item in records),
    }


def refresh_commands_category(root: Path | str) -> dict[str, Any]:
    """Replace the generated Commands category in the root Markdown inventory."""
    base = Path(root).resolve()
    index_path = base / "ALLMDFILESREFS.md"
    inventory = inventory_commands(base)
    existing = index_path.read_text(encoding="utf-8") if index_path.is_file() else "# ALLMDFILESREFS.md\n"
    marker = "\n## Commands\n"
    prefix = existing.split(marker, 1)[0].rstrip()
    lines = [
        marker.rstrip(),
        "",
        "Generated from current Markdown content and filenames. This category is evidence-only and does not execute commands.",
        "",
        f"- Markdown files with command evidence: `{len(inventory['markdown_files_with_commands'])}`",
        f"- Markdown files with command-oriented names: `{len(inventory['markdown_files_named_for_commands'])}`",
        f"- Discovered command lines: `{inventory['command_count']}`",
        "",
        "### Markdown Files With Commands",
        "",
    ]
    for item in inventory["markdown_files_with_commands"]:
        lines.append(f"- `{item['path']}` ({item['command_count']} commands, SHA-256 `{item['sha256']}`)")
        for command in item["commands"]:
            lines.append(f"  - `{command}`")
    lines.extend(["", "### Markdown Files Named For Commands", ""])
    for item in inventory["markdown_files_named_for_commands"]:
        lines.append(f"- `{item['path']}` (SHA-256 `{item['sha256']}`)")
    index_path.write_text(prefix + "\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return {"index": str(index_path), "inventory": inventory}


__all__ = ["inventory_commands", "refresh_commands_category"]