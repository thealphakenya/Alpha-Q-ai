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
DELIVERY_AUDIT_STAGES = {
    "release": re.compile(r"\breleases?\b|release[_ -]notes|release[_ -]workflow", re.I),
    "tag": re.compile(r"\b(?:git\s+)?tags?\b|refs/tags|tag[_ -]trigger", re.I),
    "publish": re.compile(r"\bpublish(?:es|ed|ing)?\b|publication", re.I),
    "build": re.compile(r"\bbuild(?:s|ing)?\b|compile|packag(?:e|ing)", re.I),
    "install": re.compile(r"\binstall(?:s|ed|ing|ation)?\b", re.I),
    "download": re.compile(r"\bdownloads?\b|artifact[_ -]retrieval", re.I),
    "deploy": re.compile(r"\bdeploy(?:s|ed|ing|ment)?\b|hosting", re.I),
    "update_rollback": re.compile(r"\bupdat(?:e|es|ed|ing)|rollback|roll[_ -]back", re.I),
}
GOVERNANCE_AUDIT_DOMAINS = {
    "qteam": re.compile(r"\bqteam\b|team[_ -](?:owner|responsib|workflow)", re.I),
    "friendship": re.compile(r"\bfriendship\b|relationship[_ -](?:system|feature)", re.I),
    "accountability": re.compile(r"\baccountability\b|responsibility[_ -]matrix", re.I),
    "master": re.compile(r"\bmaster\b|repository[_ -]owner|owner[_ -]approval", re.I),
}
CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".kt", ".swift", ".c", ".h", ".cpp", ".cs", ".rb", ".php"}
PACKAGE_SUFFIXES = {".apk", ".aab", ".ipa", ".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".whl", ".tar", ".gz", ".zip", ".appx", ".wasm"}


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


def _scope_for_path(relative: str) -> str:
    parts = Path(relative).parts
    if parts and parts[0] in {"Alpha-Q-ai-2025", "qmoi-enhanced-history-14"}:
        return "historical_snapshot"
    if any(part in {"_archive_qmoi-enhanced", "archive", "archives", "legacy"} for part in parts):
        return "local_archive_candidate"
    return "materialized_local"


def _file_facets(relative: str) -> set[str]:
    lowered = relative.lower()
    parts = {part.lower() for part in Path(relative).parts}
    facets = set()
    if Path(relative).suffix.lower() == ".md" or "docs" in parts:
        facets.add("documentation")
    if "test" in parts or "tests" in parts or Path(relative).name.lower().startswith(("test_", "*_test.")):
        facets.add("tests")
    if ".github/workflows/" in f"/{lowered}/" or "workflow" in parts or "workflows" in parts:
        facets.add("workflows")
    if Path(relative).suffix.lower() in CODE_SUFFIXES or "scripts" in parts or "src" in parts:
        facets.add("implementation_candidates")
    if Path(relative).suffix.lower() in PACKAGE_SUFFIXES or any(term in lowered for term in ("release", "download", "installer", "artifact")):
        facets.add("package_or_delivery_candidates")
    return facets


def build_system_accountability_audit(
    root: Path,
    file_records: list[dict[str, Any]],
    product_registry: dict[str, Any] | None = None,
    unavailable_sources: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Inventory shipping, product, variant, extension, and governance candidates without claiming completion."""
    product_registry = product_registry or {}
    unavailable_sources = sorted(unavailable_sources or [], key=lambda item: item.get("path", ""))
    stage_records: dict[str, list[dict[str, Any]]] = {stage: [] for stage in DELIVERY_AUDIT_STAGES}
    governance_records: dict[str, list[dict[str, Any]]] = {domain: [] for domain in GOVERNANCE_AUDIT_DOMAINS}
    lion_paths: dict[str, dict[str, Any]] = {}
    extension_paths: dict[str, dict[str, Any]] = {}
    extension_types: dict[str, dict[str, Any]] = defaultdict(lambda: {"file_count": 0, "candidate_paths": []})
    app_records: list[dict[str, Any]] = []
    platform_records: list[dict[str, Any]] = []

    for record in file_records:
        relative = str(record.get("path", ""))
        if not relative:
            continue
        path = root / relative
        lowered_path = relative.lower()
        suffix = path.suffix.lower() or "[no_extension]"
        type_record = extension_types[suffix]
        type_record["file_count"] += 1
        if suffix in CODE_SUFFIXES | PACKAGE_SUFFIXES:
            type_record["candidate_paths"].append(relative)
        try:
            text = path.read_bytes().decode("utf-8", errors="replace") if int(record.get("bytes", 0)) <= 1_000_000 else ""
        except OSError:
            text = ""
        searchable = f"{relative}\n{text}"
        facets = sorted(_file_facets(relative))
        evidence = {
            "path": relative,
            "sha256": record.get("sha256"),
            "scope": _scope_for_path(relative),
            "facets": facets,
        }

        for stage, pattern in DELIVERY_AUDIT_STAGES.items():
            if pattern.search(searchable):
                stage_records[stage].append(evidence)
        for domain, pattern in GOVERNANCE_AUDIT_DOMAINS.items():
            if pattern.search(searchable):
                governance_records[domain].append(evidence)

        lion_matches = re.findall(r"(?i)\blion(?:[._ -][a-z0-9][a-z0-9._-]*)?", Path(relative).name)
        if "lion" in lowered_path or lion_matches or re.search(r"(?i)\blion\b", text):
            lion_paths[relative] = {
                **evidence,
                "variation_candidates": sorted({item.lower().replace("_", "-").replace(" ", "-") for item in lion_matches}),
            }
        if any(term in lowered_path for term in ("extension", "extensions", "plugin", "plugins", "addon", "add-on")) or re.search(r"(?i)\b(?:extension|plugin|add-on)\b", text):
            extension_paths[relative] = evidence

    def stage_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
        facet_counts: dict[str, int] = defaultdict(int)
        scope_counts: dict[str, int] = defaultdict(int)
        for record in records:
            scope_counts[record["scope"]] += 1
            for facet in record["facets"]:
                facet_counts[facet] += 1
        paths = sorted({record["path"] for record in records})
        return {
            "candidate_file_count": len(paths),
            "scope_counts": dict(sorted(scope_counts.items())),
            "facet_candidate_counts": dict(sorted(facet_counts.items())),
            "candidate_paths": paths,
            "status": "CANDIDATE_ONLY" if paths else "NO_CANDIDATES_FOUND",
            "verification": "not_verified",
            "coverage_complete": False,
        }

    for entity_id, metadata in sorted((product_registry.get("applications") or {}).items()):
        terms = [entity_id, str(metadata.get("name", ""))]
        matching = []
        for record in file_records:
            relative = str(record.get("path", ""))
            if not relative:
                continue
            haystack = relative.lower()
            aliases = [re.sub(r"[^a-z0-9]+", "", term.lower()) for term in terms if term]
            normalized_path = re.sub(r"[^a-z0-9]+", "", haystack)
            if any(alias and alias in normalized_path for alias in aliases):
                matching.append(relative)
        app_records.append({
            "id": entity_id,
            "name": str(metadata.get("name", entity_id)),
            "category": str(metadata.get("category", "unknown")),
            "candidate_file_count": len(matching),
            "candidate_paths": sorted(matching),
            "implementation_status": "not_verified",
            "release_status": "not_verified",
        })

    for platform in sorted(set(str(item) for item in product_registry.get("platforms", []))):
        matches = sorted({
            str(record.get("path", ""))
            for record in file_records
            if platform.lower() in str(record.get("path", "")).lower().split("/")
            or re.search(rf"(?i)(?<![a-z0-9]){re.escape(platform)}(?![a-z0-9])", str(record.get("path", "")))
        })
        platform_records.append({
            "id": platform,
            "candidate_file_count": len(matches),
            "candidate_paths": matches,
            "compatibility_status": "not_verified",
            "release_status": "not_verified",
        })

    delivery = {stage: stage_summary(records) for stage, records in sorted(stage_records.items())}
    governance = {domain: stage_summary(records) for domain, records in sorted(governance_records.items())}
    extension_type_summary = {
        suffix: {**values, "candidate_paths": sorted(values["candidate_paths"])}
        for suffix, values in sorted(extension_types.items())
    }
    registered_extensions = [
        {"id": str(item), "coverage_status": "mapping_required", "source_paths": []}
        for item in sorted(set(str(value) for value in product_registry.get("extensions", [])))
    ]
    requirement_counts = {
        "applications": len(app_records),
        "platforms": len(platform_records),
        "registered_extension_features": len(registered_extensions),
        "release_delivery_stages": len(DELIVERY_AUDIT_STAGES),
        "governance_domains": len(GOVERNANCE_AUDIT_DOMAINS),
    }
    expected_requirement_count = sum(requirement_counts.values())
    accountability_blockers = [
        "No canonical Lion-variation registry is configured; discovered paths are candidates only.",
        "No requirement-to-owner/source/test/workflow mapping is supplied to this local scanner.",
        "Remote releases, tags, artifacts, download URLs, and deployment state were not queried.",
    ]
    if not product_registry.get("applications"):
        accountability_blockers.append("Application registry is unavailable; registered application denominator is unknown.")
    if not product_registry.get("platforms"):
        accountability_blockers.append("Platform registry is unavailable; registered platform denominator is unknown.")
    if not product_registry.get("extensions"):
        accountability_blockers.append("Extension registry is unavailable; registered extension denominator is unknown.")
    if unavailable_sources:
        accountability_blockers.append("One or more local files/directories were skipped or unavailable during discovery.")
    canonical_manifest = {
        "applications": app_records,
        "platforms": platform_records,
        "lion_variation_candidates": sorted(lion_paths.values(), key=lambda item: item["path"]),
        "extension_candidate_paths": sorted(extension_paths.values(), key=lambda item: item["path"]),
        "extension_file_types": extension_type_summary,
        "registered_extensions": registered_extensions,
        "delivery_stages": delivery,
        "governance_domains": governance,
        "unavailable_sources": unavailable_sources,
    }
    manifest_sha256 = hashlib.sha256(
        json.dumps(canonical_manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "status": "NEEDS_REVIEW",
        "source_scope": "materialized_local_and_marked_snapshots",
        "remote_verification_complete": False,
        "registered_application_count": len(app_records),
        "registered_platform_count": len(platform_records),
        "requirement_counts": requirement_counts,
        "expected_requirement_count": expected_requirement_count,
        "mapped_requirement_count": 0,
        "unmapped_requirement_count": expected_requirement_count,
        "applications": app_records,
        "platforms": platform_records,
        "lion_variation_candidate_count": len(lion_paths),
        "lion_variation_candidates": sorted(lion_paths.values(), key=lambda item: item["path"]),
        "extension_candidate_count": len(extension_paths),
        "extension_candidates": sorted(extension_paths.values(), key=lambda item: item["path"]),
        "extension_file_types": extension_type_summary,
        "registered_extension_count": len(registered_extensions),
        "registered_extensions": registered_extensions,
        "delivery_stages": delivery,
        "governance_domains": governance,
        "source_manifest_sha256": manifest_sha256,
        "unavailable_sources": unavailable_sources,
        "blockers": accountability_blockers,
        "coverage_complete": False,
        "limitations": [
            "Path or text matches are candidates, not proof of implementation, ownership, release, installability, or deployment.",
            "No remote refs, releases, tags, artifacts, download endpoints, deployments, or peer repository settings are verified by this local scan.",
            "Each candidate must map to an owner, source, tests, workflow, and exact-SHA evidence; missing facets remain unmapped.",
            "Oversized, unreadable, binary, excluded, or unfetched material remains a coverage limitation and cannot be counted as complete.",
        ],
    }


def build_qaudit_universe(
    root: Path | str,
    product_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
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
        "accountability": build_system_accountability_audit(
            source_root,
            files,
            product_registry=product_registry,
            unavailable_sources=skipped,
        ),
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
