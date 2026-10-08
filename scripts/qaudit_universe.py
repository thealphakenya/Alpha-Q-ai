#!/usr/bin/env python3
"""Build a deterministic, evidence-only QAUDITS/OFCA/Styles/Universals universe.

The result is intentionally conservative. Discovery is not proof of implementation,
remote completeness, or semantic correctness. Every candidate retains its source
scope, hash, classification, dependency edges, consumers, and verification state.
"""

from __future__ import annotations

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import uuid
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
    ".cache",
}
EXCLUDED_FILES = {
    "oe2.txt",
    "remotecompletion.md",
    "remote-completion.json",
    "remote-evidence-ledger.jsonl",
    "ollamatracks/telemetry.jsonl",
    "ollamatracks/qaudit_universe.json",
    "ollamatracks/ollama_reference_audit.json",
    "ollamatracks/repository_surface_audit.json",
    "ollamatracks/style_universal_replacement_inventory.json",
    "ollamatracks/feature_test_hook_coverage.json",
    "ollamatracks/system_accountability_audit.json",
    "ollamatracks/qaudit_markdown_sentence_audit.json",
    "ollamatracks/qaudit_markdown_sentence_audit.jsonl.gz",
    "QMOItracks/style_universal_candidate_tree.md",
}
EXCLUDED_DIRECTORY_PATHS = {"ollamatracks/qaudit_model_reviews"}
STYLE_NAME_PARTS = {"style", "styles", "theme", "themes", "token", "tokens", "component", "components", "pattern", "patterns"}
UNIVERSAL_NAME_PARTS = {"universal", "universals", "access", "authentication", "authorization", "identity", "permission", "security", "accessibility"}
AUDIT_NAME_PARTS = {"audit", "audits", "qaudits", "ofca", "research", "verification", "evidence", "registry"}
PLATFORM_NAME_PARTS = {"windows", "macos", "linux", "ios", "android", "web", "vercel", "netlify", "github", "gitlab", "gitpod", "huggingface", "quantum", "qvillage", "dagshub"}
AUDIT_CATEGORY_PATTERNS = {
    "Category A — Governance, repo continuity, and documentation integrity": re.compile(r"\b(?:policy|governance|documentation|continuity|repository|markdown|readme|integrity)\b", re.I),
    "Category B — Platform, build, install, deployment, and workflow execution": re.compile(r"\b(?:platform|build|compile|install|deployment|workflow|release|download|artifact)\b", re.I),
    "Category C — Automation, monitoring, autonomous operations, and self-healing": re.compile(r"\b(?:automation|autonomous|monitor|monitoring|self.heal|telemetry|heartbeat|agent)\b", re.I),
    "Category D — Product applications, feature surfaces, and UI experience": re.compile(r"\b(?:application|product|feature|capability|authentication|authorization|ui|user interface|component|style|theme|accessibility)\b", re.I),
    "Category E — Trading, finance, wallets, and real-funds lifecycle": re.compile(r"\b(?:trading|qtrade|wallet|payment|real.funds|market|drawdown|capital|risk limit)\b", re.I),
    "Category F — Security, privacy, masks, memory, and cross-system awareness": re.compile(r"\b(?:security|privacy|credential|secret|memory|identity|authorization|permission|cross.system)\b", re.I),
    "Category G — GitHub, Vercel, and developer platform operating model": re.compile(r"\b(?:github|vercel|gitlab|gitpod|hugging.?face|developer platform|branch protection)\b", re.I),
    "Category G1 — Clone, autoclone, and hosted platform parity": re.compile(r"\b(?:clone|autoclone|mirror|parity|hosted platform)\b", re.I),
    "Category H — Historical/archival references that remain relevant to live production planning": re.compile(r"\b(?:historical|archive|archived|legacy|snapshot|migration)\b", re.I),
    "Category I — Q Financial Manager, wallets, accounts, trading, revenue, and money-making operations": re.compile(r"\b(?:financial manager|finance|account|revenue|profit|money.making|qtrade|wallet)\b", re.I),
    "Category J — Release, deployment, Vercel, and production verification": re.compile(r"\b(?:release|deploy|vercel|production|publish|artifact retrieval)\b", re.I),
    "Category: API & Integration": re.compile(r"\b(?:api|endpoint|route|port|integration|rpc|webhook)\b", re.I),
    "Category: User Interface": re.compile(r"\b(?:ui|interface|component|style|theme|accessibility|responsive)\b", re.I),
    "Category: Operations & Automation": re.compile(r"\b(?:operations|automation|workflow|monitoring|agent|recovery)\b", re.I),
    "Category: Applications": re.compile(r"\b(?:application|app|qcity|qstore|qstream|qalpha|qmoispace)\b", re.I),
    "Category: Platform Support": re.compile(r"\b(?:platform|windows|macos|linux|ios|android|web|clone)\b", re.I),
    "Category: Governance & Accountability": re.compile(r"\b(?:governance|accountability|qteam|master|approval|owner)\b", re.I),
    "Category: System & Model": re.compile(r"\b(?:system|model|ollama|qversion|q\.0\.0|audit|metrics)\b", re.I),
    "Category: Repository Management": re.compile(r"\b(?:repository|git|branch|merge|ref|commit|pull request)\b", re.I),
    "style": re.compile(r"\b(?:style|styles|theme|token|typography|color|spacing|layout|accessibility)\b", re.I),
    "universal": re.compile(r"\b(?:universal|authentication|authorization|identity|permission|access control|rbac|mfa)\b", re.I),
    "tests": re.compile(r"\b(?:test|tests|pytest|jest|playwright|coverage|assertion)\b", re.I),
    "hooks": re.compile(r"\b(?:hook|hooks|webhook|event handler|listener)\b", re.I),
    "release_delivery": re.compile(r"\b(?:release|tag|publish|build|install|download|deploy|rollback|artifact)\b", re.I),
    "finance_qtrade": re.compile(r"\b(?:finance|financial|qtrade|trading|wallet|payment|profit|drawdown|capital|risk limit)\b", re.I),
    "monitoring": re.compile(r"\b(?:monitor|monitoring|telemetry|health|heartbeat|alert|observability)\b", re.I),
    "memory": re.compile(r"\b(?:memory|checkpoint|restore point|restore-point|retention)\b", re.I),
    "qaudits": re.compile(r"\b(?:qaudits|audit|ofca|evidence|verification)\b", re.I),
    "q_version": re.compile(r"\b(?:q\.0\.0|q.version|qversion|lifecycle finalization)\b", re.I),
    "api_routes_ports": re.compile(r"\b(?:api|endpoint|route|port|http|rpc)\b", re.I),
    "security": re.compile(r"\b(?:security|secret|credential|csrf|signature|encryption|vulnerability)\b", re.I),
    "product_platform": re.compile(r"\b(?:application|product|platform|windows|macos|linux|ios|android|web)\b", re.I),
    "metrics_comparison": re.compile(r"\b(?:metric|metrics|percentage|percent|statistic|benchmark|compare|score)\b", re.I),
    "documentation": re.compile(r"\b(?:documentation|markdown|readme|runbook|policy|specification)\b", re.I),
}
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
UNIVERSE_SCHEMA_VERSION = 3
SCANNER_VERSION = "2.3"
AUDIT_PRIORITY_POLICY_VERSION = "1"


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _sha256(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def _scan_source_file(source_root: Path, relative: str) -> dict[str, Any]:
    path = source_root / relative
    try:
        if path.is_symlink():
            return {"path": relative, "status": "SKIPPED", "reason": "symlink_not_followed"}
        before = path.stat()
        size = before.st_size
        digest = _sha256(path)
        if digest is None:
            return {"path": relative, "status": "SKIPPED", "reason": "unreadable_hash"}
        if size > 1_000_000:
            after = path.stat()
            if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
                return {"path": relative, "status": "SKIPPED", "reason": "changed_during_scan"}
            return {
                "path": relative,
                "status": "SCANNED_METADATA_ONLY",
                "bytes": size,
                "sha256": digest,
                "content": "",
                "reason": "oversized_content_not_parsed",
            }
        raw_content = path.read_bytes()
        try:
            content = raw_content.decode("utf-8")
        except UnicodeDecodeError:
            after = path.stat()
            if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
                return {"path": relative, "status": "SKIPPED", "reason": "changed_during_scan"}
            return {
                "path": relative,
                "status": "SCANNED_METADATA_ONLY",
                "bytes": size,
                "sha256": digest,
                "content": "",
                "reason": "invalid_utf8_content",
            }
        after = path.stat()
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
            return {"path": relative, "status": "SKIPPED", "reason": "changed_during_scan"}
        return {
            "path": relative,
            "status": "SCANNED",
            "bytes": size,
            "sha256": digest,
            "content": content,
            "reason": None,
        }
    except OSError as exc:
        return {"path": relative, "status": "SKIPPED", "reason": type(exc).__name__}


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


def build_audit_priority_queue(
    file_records: list[dict[str, Any]],
    source_manifest_sha256: str,
) -> dict[str, Any]:
    """Rank follow-up review without dropping any inventoried path or inferring a pass."""
    queue = []
    for record in file_records:
        relative = str(record.get("path", ""))
        if not relative:
            continue
        lowered = relative.lower()
        categories = set(record.get("categories", []))
        reasons: list[str] = []
        priority = 10
        if record.get("content_scan_status") != "scanned":
            priority = 120
            reasons.append("source_content_unavailable_or_metadata_only")
        if "security" in categories or any(
            token in lowered for token in ("auth", "credential", "secret", "permission", "security")
        ):
            priority = max(priority, 100)
            reasons.append("security_or_authorization_surface")
        if "finance_qtrade" in categories or any(
            token in lowered for token in ("finance", "wallet", "payment", "trading", "qtrade")
        ):
            priority = max(priority, 95)
            reasons.append("financial_or_real_funds_surface")
        if "release_delivery" in categories or any(
            token in lowered for token in ("release", "deploy", "publish", "workflow", "install")
        ):
            priority = max(priority, 85)
            reasons.append("delivery_or_workflow_surface")
        if "tests" in categories or any(
            part in {"test", "tests"} for part in Path(relative).parts
        ):
            priority = max(priority, 75)
            reasons.append("validation_and_test_mapping")
        if any(
            token in lowered for token in ("qseed", "seed", "restore", "backup", "undo", "redo", "memory")
        ):
            priority = max(priority, 70)
            reasons.append("seed_memory_or_recovery_surface")
        if record.get("test_mapping_status") != "mapped":
            reasons.append("requirement_test_mapping_not_verified")
        if record.get("hook_applicability") != "reviewed":
            reasons.append("hook_applicability_not_reviewed")
        if not reasons:
            reasons.append("baseline_path_integrity_and_requirement_mapping")
        queue.append({
            "path": relative,
            "sha256": record.get("sha256"),
            "scope": record.get("scope", "unknown"),
            "priority": priority,
            "reasons": sorted(set(reasons)),
            "status": "pending_review",
            "semantic_status": "not_evaluated",
            "remote_verified": False,
        })
    queue.sort(key=lambda item: (-item["priority"], item["path"]))
    queue_digest = hashlib.sha256(
        json.dumps(
            {
                "policy_version": AUDIT_PRIORITY_POLICY_VERSION,
                "source_manifest_sha256": source_manifest_sha256,
                "items": queue,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "policy_version": AUDIT_PRIORITY_POLICY_VERSION,
        "selection_method": "deterministic_risk_rules",
        "source_manifest_sha256": source_manifest_sha256,
        "queue_sha256": queue_digest,
        "candidate_count": len(queue),
        "pending_count": len(queue),
        "priority_counts": {
            str(priority): sum(item["priority"] == priority for item in queue)
            for priority in sorted({item["priority"] for item in queue}, reverse=True)
        },
        "model_assistance": "not_used_for_selection_or_status",
        "all_indexed_paths_queued": True,
        "items": queue,
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


def _reference_paths(
    relative: str,
    content: str,
    root: Path,
    candidates: set[str] | None = None,
    candidates_by_first_segment: dict[str, list[str]] | None = None,
) -> list[str]:
    found: set[str] = set()
    if candidates is None:
        candidates = {
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file() and not any(part in EXCLUDED_DIRECTORIES for part in path.relative_to(root).parts)
        }
    if candidates_by_first_segment is None:
        candidates_by_first_segment = defaultdict(list)
        for path in candidates:
            candidates_by_first_segment[path.split("/", 1)[0] + "/"].append(path)
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
            path for path in candidates_by_first_segment.get(module_prefix.split("/", 1)[0] + "/", [])
            if path.startswith(module_prefix) and path.lower().endswith((".css", ".py", ".ts", ".tsx", ".js", ".jsx", ".json", ".md"))
        )
        if module_matches:
            found.add(module_matches[0])
    return sorted(found)


def _audit_categories(relative: str, content: str) -> list[str]:
    searchable = f"{relative}\n{content}"
    categories = ["Category ALL"]
    categories.extend(
        category
        for category, pattern in AUDIT_CATEGORY_PATTERNS.items()
        if pattern.search(searchable)
    )
    return categories


def render_style_universal_candidate_tree(universe: dict[str, Any]) -> str:
    """Render a path/hash crosswalk; discovered candidates are never replacement proof."""
    all_records = universe.get("inventory", {}).get("all_entities", [])
    records = [
        record
        for record in all_records
        if record.get("kind") in {"style", "universal"}
    ]
    markdown_records = [
        record
        for record in all_records
        if Path(str(record.get("path", ""))).suffix.lower() == ".md"
    ]
    markdown_name_groups: dict[str, list[str]] = defaultdict(list)
    for record in markdown_records:
        normalized_name = re.sub(r"[^a-z0-9]+", "", Path(str(record["path"])).stem.lower())
        markdown_name_groups[normalized_name].append(str(record["path"]))
    markdown_collision_group_count = sum(
        len(paths) > 1 for paths in markdown_name_groups.values()
    )
    directories: set[str] = set()
    for record in [*records, *markdown_records]:
        parent = Path(str(record["path"])).parent
        while str(parent) not in {"", "."}:
            directories.add(parent.as_posix())
            parent = parent.parent
    lines = [
        "# Style and universal candidate tree",
        "",
        "Generated from the materialized local scan. A matching path or basename is a candidate only; this tree does not assert replacement, implementation, or remote verification.",
        "",
        f"- Universe status: `{universe.get('discovery', {}).get('status', 'UNKNOWN')}`",
        f"- Candidate files: `{len(records)}`",
        f"- Markdown category crosswalk entries: `{len(markdown_records)}`",
        f"- Parent directories represented: `{len(directories)}`",
        f"- Normalized Markdown basename collision groups: `{markdown_collision_group_count}`",
        f"- Skipped sources: `{universe.get('discovery', {}).get('skipped_count', 0)}`",
        "- Verified replacements: `0` unless a separate, reviewed lineage record says otherwise.",
        "",
        "## Candidate directories",
        "",
    ]
    lines.extend(f"- `{path}/` — candidate parent; replacement status `review_required`" for path in sorted(directories))
    lines.extend(["", "## Candidate files", ""])
    for record in records:
        categories = ", ".join(f"`{item}`" for item in record.get("categories", []))
        lines.append(
            f"- `{record['path']}` — kind `{record['kind']}`, scope `{record['scope']}`, "
            f"SHA-256 `{record['sha256'] or 'unavailable'}`, categories {categories}; "
            "status `candidate_not_verified_as_replaced`."
        )
    lines.extend(["", "## Markdown path and category crosswalk", ""])
    for record in markdown_records:
        categories = ", ".join(f"`{item}`" for item in record.get("categories", []))
        lines.append(
            f"- `{record['path']}` — scope `{record['scope']}`, {record['bytes']} bytes, "
            f"SHA-256 `{record['sha256'] or 'unavailable'}`, categories {categories}; "
            f"test `{record['test_mapping_status']}`, hook `{record['hook_applicability']}`, "
            f"remote `{record['remote_verification']}`."
        )
    lines.extend(["", "## Ambiguous normalized Markdown basenames", ""])
    collision_groups = {
        name: sorted(paths)
        for name, paths in markdown_name_groups.items()
        if len(paths) > 1
    }
    if not collision_groups:
        lines.append("- None discovered in the materialized local scan.")
    else:
        for normalized_name, paths in sorted(collision_groups.items()):
            lines.append(
                f"- Normalized basename `{normalized_name}` is ambiguous across: "
                + ", ".join(f"`{path}`" for path in paths)
                + "; no replacement or ownership is inferred."
            )
    lines.append("")
    return "\n".join(lines)


def _git_ref_inventory(root: Path) -> tuple[list[str], list[str], list[str]]:
    """Return local refs, branch refs, and commit hashes without remote access."""
    try:
        refs = subprocess.run(
            ["git", "-C", str(root), "for-each-ref", "--format=%(refname)"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        commit_hashes = subprocess.run(
            ["git", "-C", str(root), "rev-list", "--all"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        branches = subprocess.run(
            ["git", "-C", str(root), "branch", "--format=%(refname:short)"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        return sorted(set(refs + ["HEAD"])), branches, sorted(set(commit_hashes))
    except (OSError, subprocess.CalledProcessError):
        return [], [], []


def build_lion_universe(root: Path | str) -> dict[str, Any]:
    """Build a deterministic, evidence-only Lion/variation/extension universe.

    Discovery is intentionally conservative. Every candidate has a source path,
    hash, scope, feature facet, and verification state. No candidate is upgraded
    to a production implementation, release, or remote-completion proof.
    """
    source_root = Path(root).resolve()
    started = time.monotonic()
    variations: list[dict[str, Any]] = []
    extension_candidates: list[dict[str, Any]] = []
    logo_candidates: list[dict[str, Any]] = []
    settings_candidates: list[dict[str, Any]] = []
    automation_candidates: list[dict[str, Any]] = []
    release_candidates: list[dict[str, Any]] = []
    documentation_candidates: list[dict[str, Any]] = []
    delivery_candidates: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    source_records: list[dict[str, Any]] = []
    source_lines: dict[str, str] = {}

    if not source_root.is_dir():
        return {
            "status": "BLOCKED",
            "source_root": str(source_root),
            "remote_verification_complete": False,
            "metrics": {
                "source_manifest_sha256": "",
                "ref_count": 0,
                "ref_coverage_complete": False,
                "local_tree_verified": False,
                "variation_count": 0,
                "extension_candidate_count": 0,
                "logo_candidate_count": 0,
                "settings_candidate_count": 0,
                "automation_candidate_count": 0,
                "release_candidate_count": 0,
                "documentation_candidate_count": 0,
            },
            "blockers": ["source root is unavailable"],
            "artifacts": {},
        }

    refs, branches, commit_hashes = _git_ref_inventory(source_root)
    excluded = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache", "dist", "build", "coverage", ".cache"}
    for current, directory_names, filenames in os.walk(source_root, topdown=True, followlinks=False):
        current_path = Path(current)
        retained_dirs: list[str] = []
        for directory_name in sorted(directory_names):
            directory = current_path / directory_name
            relative = directory.relative_to(source_root).as_posix()
            if directory_name in excluded or directory.is_symlink():
                skipped.append({"path": relative, "reason": "excluded_or_symlinked"})
                continue
            retained_dirs.append(directory_name)
        directory_names[:] = retained_dirs
        for filename in sorted(filenames):
            path = current_path / filename
            relative = path.relative_to(source_root).as_posix()
            if any(part in excluded for part in Path(relative).parts) or path.is_symlink():
                skipped.append({"path": relative, "reason": "excluded_or_symlinked"})
                continue
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                size = path.stat().st_size
                text = path.read_text(encoding="utf-8", errors="replace")
                source_records.append({
                    "path": relative,
                    "size": size,
                    "sha256": digest,
                    "scope": "historical_snapshot" if any(part in {"Alpha-Q-ai-2025", "qmoi-enhanced-history-14", "archive", "archives", "legacy"} for part in Path(relative).parts) else "materialized_local",
                    "content": text,
                })
                source_lines[relative] = text
            except OSError as exc:
                skipped.append({"path": relative, "reason": type(exc).__name__})

    def candidate_record(record: dict[str, Any], category: str, matches: list[str]) -> dict[str, Any]:
        return {
            "path": record["path"],
            "scope": record["scope"],
            "sha256": record["sha256"],
            "bytes": record["size"],
            "category": category,
            "matching_terms": sorted(set(matches)),
            "verification": "candidate_only",
            "implementation_verified": False,
            "release_verified": False,
            "remote_verified": False,
        }

    for record in source_records:
        relative = record["path"].lower()
        text = record["content"]
        path = Path(record["path"])
        variation_document = "lion_variations" in relative or (
            path.suffix.lower() == ".md"
            and re.match(r"^lion[-._ ]", path.name, flags=re.IGNORECASE) is not None
        )
        if variation_document and re.search(r"(?i)\blion\b", text):
            lion_variation = re.findall(
                r"(?i)\blion(?:[._ -]([a-z0-9][a-z0-9._-]*))?",
                path.name,
            )
            variations.append({
                "path": record["path"],
                "scope": record["scope"],
                "sha256": record["sha256"],
                "bytes": record["size"],
                "classification": "lion_variation_document_candidate",
                "variation_candidates": sorted({
                    item.lower().replace("_", "-") for item in lion_variation
                }),
                "verification": "candidate_only",
                "implementation_verified": False,
                "release_verified": False,
                "remote_verified": False,
            })

    for record in source_records:
        relative = record["path"].lower()
        text = record["content"]
        if any(term in relative for term in ("extension", "extensions", "plugin", "plugins", "addon", "add-on")) or re.search(r"(?i)\b(extension|plugin|add[- ]on)\b", text):
            extension_candidates.append(candidate_record(record, "extension_or_plugin", ["extension", "plugin", "add-on"]))
        if any(term in relative for term in ("logo", "icon", "symbol", "brand")) or re.search(r"(?i)\b(logo|icon|symbol|brand)\b", text):
            logo_candidates.append(candidate_record(record, "logo_or_brand", ["logo", "icon", "symbol", "brand"]))
        if any(term in relative for term in ("setting", "config", "configuration")) or re.search(r"(?i)\b(setting|config(?:uration)?|variant)\b", text):
            settings_candidates.append(candidate_record(record, "settings_or_configuration", ["setting", "config", "configuration", "variant"]))
        if any(term in relative for term in ("workflow", "automation", "autonomous", "monitor", "trigger", "hook", "webhook")) or re.search(r"(?i)\b(workflow|automation|autonomous|monitor|trigger|hook|webhook)\b", text):
            automation_candidates.append(candidate_record(record, "automation_or_operations", ["workflow", "automation", "autonomous", "monitor", "trigger", "hook", "webhook"]))
        if any(term in relative for term in ("release", "tag", "publish", "build", "install", "download", "deploy")) or re.search(r"(?i)\b(release|tag|publish|build|install|download|deploy)\b", text):
            release_candidates.append(candidate_record(record, "release_or_delivery", ["release", "tag", "publish", "build", "install", "download", "deploy"]))
            delivery_candidates.append(candidate_record(record, "delivery_lifecycle", ["release", "tag", "publish", "build", "install", "download", "deploy"]))
        if relative.endswith(".md") or any(term in relative for term in ("download", "research", "production", "variation")):
            documentation_candidates.append(candidate_record(record, "documentation_or_research", ["markdown", "download", "research", "production", "variation"]))

    source_records.sort(key=lambda item: item["path"])
    unique_variations = sorted({item["path"] for item in variations})
    manifest_payload = {
        "root": str(source_root),
        "source_scope": "materialized_repository_and_local_git_refs",
        "refs": refs,
        "branches": branches,
        "commit_hashes": commit_hashes,
        "files": [
            {"path": item["path"], "size": item["size"], "sha256": item["sha256"], "scope": item["scope"]}
            for item in source_records
        ],
        "skipped": sorted(skipped, key=lambda item: item["path"]),
        "variations": sorted(unique_variations),
        "variation_count": len(unique_variations),
        "extension_candidate_count": len(extension_candidates),
        "logo_candidate_count": len(logo_candidates),
        "settings_candidate_count": len(settings_candidates),
        "automation_candidate_count": len(automation_candidates),
        "release_candidate_count": len(release_candidates),
        "documentation_candidate_count": len(documentation_candidates),
    }
    source_manifest_sha256 = hashlib.sha256(
        json.dumps(manifest_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    blockers = [
        "No remote repository, ref, release, tag, artifact, deployment, or owner authorization was queried.",
        "Lion and extension path/content matches are candidates and do not prove implementation or production readiness.",
        "Local Git refs establish local object coverage only; remote freshness and every intermediate-tree SHA remain unverified.",
    ]
    if not source_records:
        blockers.append("No readable source files were discovered.")
    if skipped:
        blockers.append(f"{len(skipped)} paths were excluded, unreadable, or symlinked.")

    return {
        "status": "NEEDS_REVIEW",
        "source_root": str(source_root),
        "source_scope": "materialized_repository_and_local_git_refs",
        "remote_verification_complete": False,
        "metrics": {
            "source_manifest_sha256": source_manifest_sha256,
            "ref_count": len(refs),
            "ref_coverage_complete": False,
            "local_tree_verified": False,
            "remote_verification_complete": False,
            "variation_count": len(unique_variations),
            "extension_candidate_count": len(extension_candidates),
            "logo_candidate_count": len(logo_candidates),
            "settings_candidate_count": len(settings_candidates),
            "automation_candidate_count": len(automation_candidates),
            "release_candidate_count": len(release_candidates),
            "documentation_candidate_count": len(documentation_candidates),
            "delivery_candidate_count": len(delivery_candidates),
            "files_scanned": len(source_records),
            "directories_scanned": 0,
            "skipped_count": len(skipped),
            "duration_seconds": round(time.monotonic() - started, 6),
        },
        "variations": sorted(variations, key=lambda item: item["path"]),
        "extension_candidates": sorted(extension_candidates, key=lambda item: item["path"]),
        "logo_candidates": sorted(logo_candidates, key=lambda item: item["path"]),
        "settings_candidates": sorted(settings_candidates, key=lambda item: item["path"]),
        "automation_candidates": sorted(automation_candidates, key=lambda item: item["path"]),
        "release_candidates": sorted(release_candidates, key=lambda item: item["path"]),
        "delivery_candidates": sorted(delivery_candidates, key=lambda item: item["path"]),
        "documentation_candidates": sorted(documentation_candidates, key=lambda item: item["path"]),
        "refs": refs,
        "branches": branches,
        "commit_hashes": commit_hashes,
        "blockers": blockers,
        "artifacts": {
            "manifest_path": "ollamatracks/lion_universe.json",
            "source_manifest_sha256": source_manifest_sha256,
            "candidate_tree_path": "QMOItracks/lion_variation_candidate_tree.md",
        },
    }


def write_qaudit_artifacts(
    root: Path | str,
    product_registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Refresh the deterministic local QAUDITS universe and candidate tree atomically."""
    source_root = Path(root).resolve()
    universe = build_qaudit_universe(source_root, product_registry=product_registry)
    inventory_path = source_root / "ollamatracks" / "qaudit_universe.json"
    tree_path = source_root / "QMOItracks" / "style_universal_candidate_tree.md"
    inventory_path.parent.mkdir(parents=True, exist_ok=True)
    tree_path.parent.mkdir(parents=True, exist_ok=True)

    def atomic_write(path: Path, content: str) -> None:
        fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    tree = render_style_universal_candidate_tree(universe)
    tree_hash = hashlib.sha256(tree.encode("utf-8")).hexdigest()
    universe["correlation_id"] = str(uuid.uuid4())
    universe["generated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    universe["artifacts"] = {
        "universe_json": inventory_path.relative_to(source_root).as_posix(),
        "candidate_tree_markdown": tree_path.relative_to(source_root).as_posix(),
        "candidate_tree_sha256": tree_hash,
    }
    atomic_write(tree_path, tree)
    persisted_universe = {
        "schema_version": UNIVERSE_SCHEMA_VERSION,
        "root": universe["discovery"]["root"],
        "status": universe["status"],
        "generated_at": universe["generated_at"],
        "correlation_id": universe["correlation_id"],
        "discovery": universe["discovery"],
        "metrics": universe["metrics"],
        "inventory": {
            kind: [record["path"] for record in universe["inventory"][kind]]
            for kind in ("styles", "universals", "audit")
        },
        "classes": universe["classes"],
        "dependency_graph": {
            "edge_count": len(universe["dependency_graph"]["edges"]),
            "cycles": universe["dependency_graph"]["cycles"],
            "orphaned": universe["dependency_graph"]["orphaned"],
        },
        "accountability": universe["accountability"],
        "audit_queue": universe["audit_queue"],
        "evidence": universe["evidence"],
        "artifacts": universe["artifacts"],
        "representation": "normalized_path_records; derived inventory lists; dependency edges are counted and available from class dependency paths",
    }
    atomic_write(inventory_path, json.dumps(persisted_universe, indent=2, sort_keys=True) + "\n")
    return universe


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

    def analyze_record(record: dict[str, Any]) -> dict[str, Any]:
        relative = str(record.get("path", ""))
        if not relative:
            return {"path": ""}
        path = root / relative
        suffix = path.suffix.lower() or "[no_extension]"
        text = ""
        try:
            if (
                int(record.get("bytes", 0)) <= 1_000_000
                and record.get("content_scan_status") == "scanned"
            ):
                text = path.read_bytes().decode("utf-8", errors="replace")
        except OSError:
            return {"path": relative, "unavailable": True, "suffix": suffix}
        searchable = f"{relative}\n{text}"
        facets = sorted(_file_facets(relative))
        evidence = {
            "path": relative,
            "sha256": record.get("sha256"),
            "scope": _scope_for_path(relative),
            "facets": facets,
        }
        delivery_matches = [stage for stage, pattern in DELIVERY_AUDIT_STAGES.items() if pattern.search(searchable)]
        governance_matches = [domain for domain, pattern in GOVERNANCE_AUDIT_DOMAINS.items() if pattern.search(searchable)]
        lion_matches = re.findall(r"(?i)\blion(?:[._ -][a-z0-9][a-z0-9._-]*)?", path.name)
        lion_candidate = "lion" in relative.lower() or bool(lion_matches) or bool(re.search(r"(?i)\blion\b", text))
        extension_candidate = (
            any(term in relative.lower() for term in ("extension", "extensions", "plugin", "plugins", "addon", "add-on"))
            or bool(re.search(r"(?i)\b(?:extension|plugin|add-on)\b", text))
        )
        return {
            "path": relative,
            "suffix": suffix,
            "evidence": evidence,
            "delivery_matches": delivery_matches,
            "governance_matches": governance_matches,
            "lion_candidate": lion_candidate,
            "lion_variation_candidates": sorted({item.lower().replace("_", "-").replace(" ", "-") for item in lion_matches}),
            "extension_candidate": extension_candidate,
        }

    worker_count = min(16, max(1, os.cpu_count() or 1))
    batch_size = max(32, worker_count * 4)
    with ThreadPoolExecutor(max_workers=worker_count, thread_name_prefix="qaudit-domain") as executor:
        for offset in range(0, len(file_records), batch_size):
            batch = file_records[offset : offset + batch_size]
            analyses = executor.map(analyze_record, batch)
            for analysis in analyses:
                relative = analysis.get("path", "")
                if not relative:
                    continue
                suffix = analysis.get("suffix", "[no_extension]")
                type_record = extension_types[suffix]
                type_record["file_count"] += 1
                if suffix in CODE_SUFFIXES | PACKAGE_SUFFIXES:
                    type_record["candidate_paths"].append(relative)
                if analysis.get("unavailable"):
                    continue
                evidence = analysis["evidence"]
                for stage in analysis["delivery_matches"]:
                    stage_records[stage].append(evidence)
                for domain in analysis["governance_matches"]:
                    governance_records[domain].append(evidence)
                if analysis["lion_candidate"]:
                    lion_paths[relative] = {
                        **evidence,
                        "variation_candidates": analysis["lion_variation_candidates"],
                    }
                if analysis["extension_candidate"]:
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
    scan_started = time.monotonic()
    files: list[dict[str, Any]] = []
    classes: dict[str, dict[str, Any]] = {}
    inventory: dict[str, list[dict[str, Any]]] = {"styles": [], "universals": [], "audit": []}
    edges: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    directories: set[str] = set()
    candidate_paths: set[str] = set()
    candidates_by_first_segment: dict[str, list[str]] = defaultdict(list)
    scanned = 0
    total_bytes = 0

    if not source_root.is_dir():
        return {
            "discovery": {"status": "BLOCKED", "files_scanned": 0, "root": str(source_root)},
            "inventory": inventory,
            "classes": classes,
            "dependency_graph": {"edges": edges},
            "evidence": {"source_scope": "materialized_local", "remote_verification_complete": False},
        }

    source_paths: list[str] = []
    policy_excluded_files_present = sorted(
        path for path in EXCLUDED_FILES if (source_root / path).is_file()
    )
    for current, directory_names, filenames in os.walk(source_root, topdown=True, followlinks=False):
        current_path = Path(current)
        retained = []
        for directory_name in directory_names:
            directory = current_path / directory_name
            relative_directory = directory.relative_to(source_root).as_posix()
            if (
                directory_name in EXCLUDED_DIRECTORIES
                or directory_name.startswith((".venv", "venv"))
                or directory.is_symlink()
                or relative_directory in EXCLUDED_DIRECTORY_PATHS
            ):
                skipped.append({"path": relative_directory, "reason": "excluded_or_symlinked"})
                continue
            retained.append(directory_name)
            directories.add(relative_directory)
        directory_names[:] = sorted(retained)
        for filename in sorted(filenames):
            relative = _relative(current_path / filename, source_root)
            if relative in EXCLUDED_FILES or any(part in EXCLUDED_DIRECTORIES for part in Path(relative).parts):
                continue
            source_paths.append(relative)

    enumerated_file_count = len(source_paths)
    enumeration_finished = time.monotonic()
    candidate_paths = set(source_paths)
    candidates_by_first_segment = defaultdict(list)
    for candidate_path in source_paths:
        candidates_by_first_segment[candidate_path.split("/", 1)[0] + "/"].append(candidate_path)

    worker_count = min(16, max(1, os.cpu_count() or 1))
    batch_size = max(32, worker_count * 4)
    with ThreadPoolExecutor(max_workers=worker_count, thread_name_prefix="qaudit-scan") as executor:
        for offset in range(0, len(source_paths), batch_size):
            batch = source_paths[offset : offset + batch_size]
            scanned_sources = executor.map(lambda path: _scan_source_file(source_root, path), batch)
            for source in scanned_sources:
                relative = source["path"]
                if source["status"] == "SKIPPED":
                    skipped.append({"path": relative, "reason": source["reason"]})
                    continue
                if source["reason"]:
                    skipped.append({"path": relative, "reason": source["reason"]})
                size = source["bytes"]
                content = source["content"]
                scanned += 1
                total_bytes += size
                digest = source["sha256"]
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
                    "scope": _scope_for_path(relative),
                    "categories": _audit_categories(relative, content),
                    "content_scan_status": "scanned" if source["status"] == "SCANNED" else source["reason"],
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

                referenced = _reference_paths(
                    relative,
                    content,
                    source_root,
                    candidate_paths,
                    candidates_by_first_segment,
                )
                class_record["dependencies"] = referenced
                edges.extend(
                    {
                        "source": relative,
                        "edge_type": "references",
                        "target": dependency,
                        "status": "observed",
                    }
                    for dependency in referenced
                    if dependency in candidate_paths
                )

    consumers_by_target: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        consumers_by_target[edge["target"]].add(edge["source"])
    for entity in classes.values():
        entity["consumers"] = sorted(consumers_by_target[entity["path"]])

    def all_records(kind: str) -> list[dict[str, Any]]:
        return sorted(
            (record for record in files if record["kind"] == kind),
            key=lambda item: item["path"],
        )

    category_counts: dict[str, int] = defaultdict(int)
    extension_counts: dict[str, int] = defaultdict(int)
    for record in files:
        extension_counts[Path(record["path"]).suffix.lower() or "[no_extension]"] += 1
        for category in record["categories"]:
            category_counts[category] += 1
    source_manifest = [
        (
            record["path"],
            record["bytes"],
            record["sha256"],
            record["kind"],
            record["categories"],
            record["scope"],
        )
        for record in sorted(files, key=lambda item: item["path"])
    ]
    source_manifest_sha256 = hashlib.sha256(
        json.dumps(
            {
                "files": source_manifest,
                "skipped": sorted(skipped, key=lambda item: item["path"]),
                "excluded_directories": sorted(EXCLUDED_DIRECTORIES),
                "excluded_files": sorted(EXCLUDED_FILES),
                "excluded_files_present": policy_excluded_files_present,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    unavailable_count = sum(item["reason"] != "excluded_or_symlinked" for item in skipped)
    markdown_records = [
        record for record in files if Path(record["path"]).suffix.lower() == ".md"
    ]
    markdown_name_groups: dict[str, list[str]] = defaultdict(list)
    for record in markdown_records:
        normalized_name = re.sub(r"[^a-z0-9]+", "", Path(record["path"]).stem.lower())
        markdown_name_groups[normalized_name].append(record["path"])
    represented_directories: set[str] = set()
    for record in files:
        if record["kind"] not in {"style", "universal"} and not record["path"].lower().endswith(".md"):
            continue
        parent = Path(record["path"]).parent
        while str(parent) not in {"", "."}:
            represented_directories.add(parent.as_posix())
            parent = parent.parent
    scope_counts: dict[str, int] = defaultdict(int)
    for record in files:
        scope_counts[record["scope"]] += 1
    audit_queue = build_audit_priority_queue(files, source_manifest_sha256)
    accountability = build_system_accountability_audit(
        source_root,
        files,
        product_registry=product_registry,
        unavailable_sources=skipped,
    )
    completed_at = time.monotonic()
    return {
        "discovery": {
            "status": "NEEDS_REVIEW" if unavailable_count else "COMPLETE_MATERIALIZED_LOCAL",
            "root": str(source_root),
            "files_scanned": scanned,
            "directories_scanned": len(directories),
            "bytes_scanned": total_bytes,
            "skipped_count": len(skipped),
            "excluded_source_count": len(skipped) - unavailable_count,
            "unavailable_source_count": unavailable_count,
            "skipped": sorted(skipped, key=lambda item: item["path"]),
            "excluded_directories": sorted(EXCLUDED_DIRECTORIES),
            "excluded_files": policy_excluded_files_present,
            "excluded_file_policy": sorted(EXCLUDED_FILES),
        },
        "metrics": {
            "source_scope": "materialized_local_only",
            "scanner_version": SCANNER_VERSION,
            "source_manifest_sha256": source_manifest_sha256,
            "enumeration_duration_seconds": round(enumeration_finished - scan_started, 3),
            "post_enumeration_duration_seconds": round(completed_at - enumeration_finished, 3),
            "total_duration_seconds": round(completed_at - scan_started, 3),
            "enumerated_file_count": enumerated_file_count,
            "file_count": scanned,
            "files_with_parsed_content_count": sum(
                1 for record in files if record["content_scan_status"] == "scanned"
            ),
            "metadata_only_file_count": sum(
                1 for record in files if record["content_scan_status"] != "scanned"
            ),
            "directory_count": len(directories),
            "excluded_source_count": len(skipped) - unavailable_count,
            "excluded_directory_policy": sorted(
                EXCLUDED_DIRECTORIES | EXCLUDED_DIRECTORY_PATHS
            ),
            "excluded_file_count": len(policy_excluded_files_present),
            "excluded_file_paths": policy_excluded_files_present,
            "maximum_directory_depth": max(
                (len(Path(path).parts) for path in directories), default=0
            ),
            "directory_paths": sorted(directories),
            "bytes_scanned": total_bytes,
            "extension_counts": dict(sorted(extension_counts.items())),
            "candidate_counts_by_kind": {
                kind: sum(1 for record in files if record["kind"] == kind)
                for kind in ("style", "universal", "audit", "other")
            },
            "category_candidate_path_counts": dict(sorted(category_counts.items())),
            "scope_candidate_path_counts": dict(sorted(scope_counts.items())),
            "style_universal_candidate_directory_count": len(represented_directories),
            "markdown_crosswalk_entry_count": len(markdown_records),
            "markdown_normalized_basename_collision_group_count": sum(
                1 for paths in markdown_name_groups.values() if len(paths) > 1
            ),
            "markdown_normalized_basename_collision_file_count": sum(
                len(paths) for paths in markdown_name_groups.values() if len(paths) > 1
            ),
            "duplicate_path_count": scanned - len(classes),
            "dependency_edge_count": len(edges),
            "dependency_orphan_count": sum(
                1 for record in classes.values()
                if not record["dependencies"] and not record["consumers"]
            ),
            "test_mapped_candidate_count": 0,
            "hook_reviewed_candidate_count": 0,
            "remote_verified_candidate_count": 0,
            "audit_queue_candidate_count": audit_queue["candidate_count"],
            "audit_queue_pending_count": audit_queue["pending_count"],
            "audit_queue_sha256": audit_queue["queue_sha256"],
            "audit_queue_priority_counts": audit_queue["priority_counts"],
            "skipped_source_count": unavailable_count,
            "hash_error_count": sum(
                1 for item in skipped
                if item["reason"] in {"unreadable_hash", "changed_during_scan"}
            ),
            "content_parse_skipped_count": sum(
                1 for item in skipped
                if item["reason"] in {"oversized_content_not_parsed", "invalid_utf8_content"}
            ),
            "verification_state": "candidate_discovery_only",
            "worker_count": worker_count,
            "batch_size": batch_size,
            "maximum_content_parse_bytes": 1_000_000,
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
        "accountability": accountability,
        "audit_queue": audit_queue,
        "evidence": {
            "source_scope": "materialized_local",
            "source_manifest_sha256": source_manifest_sha256,
            "remote_verification_complete": False,
            "all_refs": "not_verified",
            "pull_requests": "not_verified",
            "intermediate_commit_trees": "not_verified",
            "peer_repositories": "not_verified",
            "manual_replacement_authorized": False,
        },
        "status": "NEEDS_REMOTE_HISTORY_EVIDENCE",
    }
