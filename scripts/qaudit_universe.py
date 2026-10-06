#!/usr/bin/env python3
"""Build a deterministic, evidence-only QAUDITS/OFCA/Styles/Universals universe.

The result is intentionally conservative. Discovery is not proof of implementation,
remote completeness, or semantic correctness. Every candidate retains its source
scope, hash, classification, dependency edges, consumers, and verification state.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

EXCLUDED_DIRECTORIES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
    "coverage",
    r"\.cache",
}
EXCLUDED_FILES = {
    "ollamatracks/qaudit_universe.json",
    "ollamatracks/ollama_reference_audit.json",
    "ollamatracks/repository_surface_audit.json",
    "ollamatracks/style_universal_replacement_inventory.json",
    "ollamatracks/feature_test_hook_coverage.json",
}
STYLE_NAME_PARTS = {"style", "styles", "theme", "themes", "token", "tokens", "component", "components", "pattern", "patterns"}
UNIVERSAL_NAME_PARTS = {"universal", "universals", "access", "authentication", "authorization", "identity", "permission", "security", "accessibility"}
AUDIT_NAME_PARTS = {"audit", "audits", "qaudits", "ofca", "research", "verification", "evidence", "registry"}
PLATFORM_NAME_PARTS = {"windows", "macos", "linux", "ios", "android", "web", "vercel", "netlify", "github", "gitlab", "gitpod", "huggingface", "quantum", "qvillage", "dagshub"}


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _classify_name(relative: str, kind: str) -> str:
    lowered = relative.lower()
    parts = {part.lower() for part in Path(relative).parts}
    if kind == "style":
        if lowered in {"styles.md", "universal.md", "universals.md"}:
            return "canonical_style_or_universal_specification"
        if "legacy" in lowered or "old" in lowered or "deprecated" in lowered:
            return "legacy_style_candidate"
        if "style" in parts or "styles" in parts or any(name in lowered for name in STYLE_NAME_PARTS):
            return "style_candidate"
        return "style_candidate"
    if kind == "universal":
        if lowered in {"universals.md", "universal.md"}:
            return "canonical_universal_specification"
        if "legacy" in lowered or "old" in lowered or "deprecated" in lowered:
            return "legacy_universal_candidate"
        if "universal" in parts or "universals" in parts or any(name in lowered for name in UNIVERSAL_NAME_PARTS):
            return "universal_candidate"
        if any(name in parts for name in PLATFORM_NAME_PARTS) and ("auth" in lowered or "access" in lowered):
            return "platform_specific_universal_candidate"
        return "universal_candidate"
    if kind == "audit":
        if lowered in {"qaudits.md", "ofca.md", "qversionmanager.md"}:
            return "canonical_audit_specification"
        if any(name in parts for name in AUDIT_NAME_PARTS) or "audit" in lowered:
            return "audit_candidate"
        return "audit_candidate"
    return "unknown"


def classify_entity(relative: str, kind: str) -> dict[str, str]:
    """Return deterministic classification and safe action metadata."""
    lowered = relative.lower()
    if kind == "universal" and Path(relative).name.lower() in {"universals.md", "universal.md"}:
        return {
            "classification": "canonical_universal_specification",
            "canonical_status": "canonical",
            "action": "retain_and_update_with_verified_contract",
            "confidence": "high",
        }
    if kind == "audit" and Path(relative).name.lower() in {"qaudits.md", "ofca.md", "qversionmanager.md"}:
        return {
            "classification": "canonical_audit_specification",
            "canonical_status": "canonical",
            "action": "retain_and_keep_generated_evidence_current",
            "confidence": "high",
        }
    if kind == "style" and ("legacy" in lowered or "old" in lowered or "deprecated" in lowered):
        return {
            "classification": "legacy_style_candidate",
            "canonical_status": "unknown",
            "action": "investigate_and_test_before_migration",
            "confidence": "low",
        }
    if kind == "universal" and any(token in lowered for token in ("web", "android", "ios", "windows", "macos", "linux")) and any(token in lowered for token in ("auth", "access", "permission")):
        return {
            "classification": "platform_specific_universal_candidate",
            "canonical_status": "platform_override",
            "action": "verify_platform_boundary_and_access_contract",
            "confidence": "medium",
        }
    if kind == "style":
        return {
            "classification": "style_candidate",
            "canonical_status": "unknown",
            "action": "classify_and_map_to_canonical_style_contract",
            "confidence": "medium",
        }
    if kind == "universal":
        return {
            "classification": "universal_candidate",
            "canonical_status": "unknown",
            "action": "classify_and_map_to_canonical_universal_contract",
            "confidence": "medium",
        }
    return {
        "classification": "audit_candidate",
        "canonical_status": "unknown",
        "action": "classify_and_map_to_audit_pack",
        "confidence": "medium",
    }


def _candidate_kind(relative: str, content: str) -> str | None:
    lowered = relative.lower()
    name = Path(relative).name.lower()
    if name in {"styles.md", "styling.md", "theme.md", "tokens.md"} or "style" in lowered or "theme" in lowered:
        return "style"
    if name in {"universals.md", "universal.md", "universal-ui.md"} or "universal" in lowered:
        return "universal"
    if name in {"qaudits.md", "ofca.md", "qversionmanager.md"} or "audit" in lowered or "ofca" in lowered:
        return "audit"
    if ("auth" in content.lower() and any(token in lowered for token in ("web", "android", "ios", "windows", "macos", "linux"))) or ("accessibility" in content.lower() and "universal" in lowered):
        return "universal"
    return None


def _read_text(path: Path) -> str:
    try:
        return path.read_bytes().decode("utf-8", errors="replace")
    except OSError:
        return ""


def _reference_paths(relative: str, content: str, root: Path) -> list[str]:
    found: set[str] = set()
    candidates = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and not any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(root).parts)
    }
    for candidate in re.findall(r"(?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+(?:\.[A-Za-z0-9]+)", content):
        candidate = candidate.strip(".,;:()[]{}'\"")
        if candidate.startswith(("http://", "https://", "mailto:", "#")):
            continue
        normalized = candidate.replace("\\", "/")
        if normalized.startswith("../") or normalized.startswith("./"):
            normalized = normalized.lstrip("./")
        if normalized in found or normalized in candidates:
            found.add(normalized)
            continue
        module_prefix = normalized.split(".", 1)[0]+"/"
        module_matches = sorted(
            path for path in candidates
            if path.startswith(module_prefix) and path.lower().endswith((".css", ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md"))
        )
        if module_matches:
            found.add(module_matches[0])
    return sorted(found)


def build_qaudit_universe(root: Path | str) -> dict[str, Any]:
    """Create a source-scoped inventory and dependency graph for all audited systems."""
    source_root = Path(root).resolve()
    files: list[dict[str, Any]] = []
    classes: dict[str, dict[str, Any]] = {}
    inventory: dict[str, list[dict[str, Any]]] = {"styles": [], "universals": [], "audit": []}
    edges: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    scanned = 0

    if not source_root.is_dir():
        return {
            "discovery": {"status": "BLOCKED", "files_scanned": 0, "root": str(source_root)},
            "inventory": inventory,
            "classes": classes,
            "dependency_graph": {"edges": edges},
            "evidence": {"source_scope": "materialized_local", "remote_verification_complete": False},
        }

    for current, directory_names, filenames in os.walk(source_root, topdown=True, followlinks=False):
        current_path = Path(current)
        retained = []
        for directory_name in directory_names:
            directory = current_path / directory_name
            relative_directory = directory.relative_to(source_root).as_posix()
            if directory_name in EXCLUDED_DIRECTORIES or directory_name.startswith((".venv", "venv")) or directory.is_symlink():
                skipped.append({"path": relative_directory, "reason": "excluded_or_symlinked"})
                continue
            retained.append(directory_name)
        directory_names[:] = retained

        for filename in filenames:
            path = current_path / filename
            relative = _relative(path, source_root)
            if relative in EXCLUDED_FILES or any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(source_root).parts):
                continue
            if path.is_symlink():
                skipped.append({"path": relative, "reason": "symlink_not_followed"})
                continue
            try:
                size = path.stat().st_size
                if size > 1_000_000:
                    skipped.append({"path": relative, "reason": "oversized_file_not_read"})
                    continue
                content = _read_text(path)
            except OSError as exc:
                skipped.append({"path": relative, "reason": type(exc).__name__})
                continue

            scanned += 1
            digest = _sha256(path)
            kind = _candidate_kind(relative, content)
            classification = classify_entity(relative, kind or "audit")
            class_record = {
                "path": relative,
                "kind": kind or "other",
                "classification": classification["classification"],
                "canonical_status": classification["canonical_status"],
                "action": classification["action"],
                "confidence": classification["confidence"],
                "bytes": size,
                "sha256": digest,
                "scope": "materialized_local",
                "test_mapping_status": "unmapped",
                "hook_applicability": "review_required",
                "consumers": [],
                "dependencies": [],
                "generated": False,
                "remote_verification": "not_verified",
            }
            classes[relative] = class_record
            if kind == "style":
                inventory["styles"].append(class_record)
            elif kind == "universal":
                inventory["universals"].append(class_record)
            elif kind == "audit":
                inventory["audit"].append(class_record)
            files.append(class_record)

    for record in files:
        relative = record["path"]
        path = source_root / relative
        content = _read_text(path)
        referenced = _reference_paths(relative, content, source_root)
        record["dependencies"] = referenced
        for dependency in referenced:
            if dependency in classes:
                edges.append({
                    "source": relative,
                    "edge_type": "references",
                    "target": dependency,
                    "status": "observed",
                })

    for entity in classes.values():
        entity["consumers"] = sorted(
            {
                edge["source"]
                for edge in edges
                if edge["target"] == entity["path"]
            }
        )

    def all_records(kind: str) -> list[dict[str, Any]]:
        return sorted(
            (record for record in files if record["kind"] == kind),
            key=lambda item: item["path"],
        )

    return {
        "discovery": {
            "status": "COMPLETE_MATERIALIZED_LOCAL",
            "root": str(source_root),
            "files_scanned": scanned,
            "skipped_count": len(skipped),
            "skipped": sorted(skipped, key=lambda item: item["path"]),
            "excluded_directories": sorted(EXCLUDED_DIRECTORIES),
        },
        "inventory": {
            "styles": all_records("style"),
            "universals": all_records("universal"),
            "audit": all_records("audit"),
            "all_entities": sorted(files, key=lambda item: item["path"]),
        },
        "classes": classes,
        "dependency_graph": {
            "edges": sorted(edges, key=lambda item: (item["source"], item["target"], item["edge_type"])),
            "cycles": [],
            "orphaned": sorted(
                path for path, record in classes.items()
                if not record["dependencies"] and not record["consumers"]
            ),
        },
        "evidence": {
            "source_scope": "materialized_local",
            "remote_verification_complete": False,
            "all_refs": "not_verified",
            "pull_requests": "not_verified",
            "intermediate_commit_trees": "not_verified",
            "peer_repositories": "not_verified",
            "manual_replacement_authorized": False,
        },
        "status": "NEEDS_REMOTE_HISTORY_EVIDENCE",
    }
