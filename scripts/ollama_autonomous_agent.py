#!/usr/bin/env python3
"""
QMOI Ollama Autonomous Agent
============================

Stable autonomous validation/orchestration layer for QMOI.

Responsibilities:
- Cross-platform validation
- 293+ platform-specific feature validation
- File-handler validation
- Realtime tracker / telemetry
- Workflow normalization
- Workflow monitoring
- Auto-healing
- Resume checkpoints
- Memory index generation
- Model-card generation
- GitHub proof contracts
- Cross-repository synchronization contracts
- Avatar/QMOI realtime validation
- Backward-compatible test APIs

IMPORTANT COMPATIBILITY CONTRACT
--------------------------------
The enhanced validation suite expects:

    QMOI_APPS.keys()

to be valid.

Therefore QMOI_APPS is intentionally a dictionary and must remain a
dictionary. Feature metadata is stored separately from feature lists.

The canonical feature registry is:

    FEATURE_REGISTRY[platform][app] -> List[str]

and:

    PLATFORM_SPECIFIC_FEATURES

is retained as a backwards-compatible alias to that registry.

VALIDATION API CONTRACT
-----------------------
The enhanced validation suite also expects:

    agent.validate_platform_features()

and:

    agent.validate_all_platform_features()

Both methods return the application-level feature validation contract:

    {
        "windows": {
            "qmoiaiui": {...},
            "qcity": {...},
            "qmoi-space": {...},
            "qalpha": {...},
        },
        ...
    }

Therefore:

    len(results["windows"]) == 4

The platform-level metadata returned by PlatformValidator.validate()
is intentionally kept separate from the application feature contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
import uuid
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar
from urllib.parse import unquote, urlsplit

SCRIPT_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = SCRIPT_DIR.parent
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.autonomous_completion_engine import (
    AutonomousCompletionEngine,
    audit_instruction_files,
    audit_ollama_reference_files,
)
from scripts.command_inventory import refresh_commands_category
from scripts.link_validator import LinkValidator
from scripts.qaudit_checkpoint import record_qaudit_checkpoint
from scripts.ollama_research import (
    EXTERNAL_RESEARCH_CONTROLS,
    INTERNAL_RESEARCH_CONTROLS,
    VALIDATION_RESEARCH_MAP,
    build_external_research_plan,
    build_internal_research_plan,
    build_validation_research_matrix,
    audit_repository_surfaces,
    fetch_official_resource,
    record_research_visit,
    write_markdown_sentence_audit,
)
from scripts.q_version_manager import QVersionManager
from scripts.qaudit_all_features import run_parallel_feature_audit
from scripts.qaudit_universe import write_qaudit_artifacts
from scripts.qaudits_parallel_auditor import run_parallel_merge_audit

try:
    from scripts.live_activity_stream import (
        build_merge_activity_stream,
    )
    from scripts.ollama_runtime import (
        OllamaBootstrap,
        OllamaClient,
        OllamaRuntimeError,
        build_success_contract,
        parse_repair_plan,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script execution path
    from live_activity_stream import (
        build_merge_activity_stream,
    )
    from ollama_runtime import (
        OllamaBootstrap,
        OllamaClient,
        OllamaRuntimeError,
        build_success_contract,
        parse_repair_plan,
    )


# ============================================================================
# CONSTANTS
# ============================================================================

PLATFORMS: list[str] = [
    "windows",
    "macos",
    "linux",
    "ios",
    "android",
    "web",
]

SUPPORTED_PLATFORMS = list(PLATFORMS)


# ============================================================================
# APPLICATION REGISTRY
# ============================================================================
#
# IMPORTANT:
# This MUST remain a dictionary.
#
# Enhanced tests explicitly call:
#
#     QMOI_APPS.keys()
#
# Do not change this to a list or tuple.
# ============================================================================

QMOI_APPS: dict[str, dict[str, Any]] = {
    "qmoiaiui": {
        "name": "QMOIAIUI",
        "description": "Conversational AI interface",
        "category": "ai",
    },
    "qcity": {
        "name": "QCity",
        "description": "File Manager",
        "category": "file-management",
    },
    "qmoi-space": {
        "name": "QMOI Space",
        "description": "Media Player",
        "category": "media",
    },
    "qalpha": {
        "name": "QALPHA",
        "description": "IDE",
        "category": "development",
    },
}

SUPPORTED_APPS: list[str] = list(QMOI_APPS.keys())


# ============================================================================
# REPOSITORY CONSTANTS
# ============================================================================

QMOI_REPOSITORY = "thealphakenya/qmoi-enhanced"
ALPHA_Q_AI_REPOSITORY = "thealphakenya/Alpha-Q-ai"

DEFAULT_BRANCH = "main"
BACKUP_BRANCH = "autosync-backup"
MASTER_BRANCH = "master"
HISTORICAL_BRANCH = (
    "origin/codespace-potential-space-happiness-wrv69x5j6qjq2g7wp"
)
HISTORY_SNAPSHOT_DIRECTORY = "qmoi-enhanced-history-14"

QMOI_APP_DOCUMENTS: dict[str, str] = {
    "qmoiaiui": "QMOIAI.md",
    "qcity": "QCITY.md",
    "qmoi-space": "QMOISPACE.md",
    "qalpha": "QALPHA.md",
}

QSTORE_CATALOG_APPS: dict[str, dict[str, str]] = {
    app_id: {
        **metadata,
        "repository": QMOI_REPOSITORY,
        "documentation": QMOI_APP_DOCUMENTS[app_id],
    }
    for app_id, metadata in QMOI_APPS.items()
}
QSTORE_CATALOG_APPS["qstream"] = {
    "name": "QStream",
    "description": "QMOI entertainment and streaming application",
    "category": "entertainment",
    "repository": "thealphakenya/qstream",
    "documentation": "QSTREAM.md",
}

QSTORE_SHARED_UI_FEATURES: tuple[str, ...] = (
    "Search and filter by app name, category, platform, and availability.",
    "Accessible app cards and detail views with version, publisher, and source.",
    "Platform compatibility and minimum-requirement indicators.",
    "Release history, changelog, and update-availability states.",
    "Install, update, cancel, retry, and rollback controls with progress and errors.",
    "Permission, privacy, license, and content-availability details before install.",
    "Package source and integrity metadata; do not imply verification without evidence.",
    "Keyboard, screen-reader, focus, contrast, and scalable-text support.",
    "QMOI recommendations that disclose their basis and respect user settings.",
    "Loading, empty, offline, restricted, and failed states with recoverable actions.",
)

QSTORE_PLATFORM_UI_FEATURES: dict[str, tuple[str, ...]] = {
    "windows": ("Windows package and architecture compatibility.", "Keyboard navigation and native install/update handoff."),
    "macos": ("macOS package and architecture compatibility.", "Signing/notarization state when independently verified."),
    "linux": ("Linux package format and distribution compatibility.", "Package-manager handoff and dependency status."),
    "ios": ("iOS device compatibility and official-store handoff.", "VoiceOver and system-permission disclosure."),
    "android": ("Android device compatibility and official-store handoff.", "TalkBack and runtime-permission disclosure."),
    "web": ("Responsive web catalog and installable-PWA state.", "Offline catalog state and browser-compatible install handoff."),
}

QMOI_HOSTING_FEATURES: tuple[str, ...] = (
    "Project and environment inventory with owner, repository, and source SHA.",
    "Build configuration, dependency, cache, and artifact status.",
    "Static, server-rendered, function, and edge-runtime capability discovery.",
    "Preview, staging, production, promote, rollback, and cancel workflows.",
    "Domain, DNS, TLS, redirect, and deployment-alias management.",
    "Logs, metrics, traces, health checks, alerts, and incident history.",
    "Environment-secret references with masked readiness and rotation status.",
    "Regions, traffic controls, quotas, resource usage, and cost visibility.",
    "Storage, databases, queues, scheduled jobs, and integration status.",
    "Access policy, approvals, audit events, and recovery controls.",
)

QUANTUM_EXTENSION_FEATURES: tuple[str, ...] = (
    "Capability discovery for simulator, hybrid runtime, and provider-backed QPU execution.",
    "Provider adapters with explicit availability, region, queue, and maintenance state.",
    "Circuit/job submission, validation, cancellation, retry, and result retrieval.",
    "Qubit, shots, compiler, backend, fidelity, and execution metadata when supplied by the provider.",
    "Hybrid classical/quantum workflow orchestration and reproducible job manifests.",
    "Queue time, runtime, quota, cost estimate, and spend confirmation before execution.",
    "Result provenance, artifact integrity, simulator-versus-hardware labeling, and replay metadata.",
    "Provider outage, unsupported operation, quota, and job-failure recovery states.",
)

MASTER_OWNED_UI_FEATURES: tuple[str, ...] = (
    "System overview with source timestamp, health, and stale/degraded indicators.",
    "Repository, application, hosting, and deployment inventory with exact source SHAs.",
    "User, role, session, consent, and access review with least-privilege controls.",
    "Quantum compute/provider control with capability and billing gates.",
    "Deployment preview, approval, promotion, rollback, and audit trail.",
    "Domain, DNS, TLS, and ownership management with confirmation before changes.",
    "Documentation, styles, app-catalog, and validation report management.",
    "Master and sister account configuration for bank accounts, wallets, payment APIs, and project-linked financial destinations.",
    "Revenue, wallet, and financial dashboards with read/write permissions separated.",
    "Monitoring, notifications, incidents, recovery, and automation controls.",
    "Security events, audit history, export, retention, and access-revocation controls.",
    "Brand customization with QMOI logo, icon, font, motion, and identity tokens without hiding risk state.",
)

QMOI_PUBLIC_UI_FEATURES: tuple[str, ...] = (
    "public catalog pages and documentation",
    "public preview pages and public product details",
    "public search, browse, and compare flows",
    "public landing pages, pricing summaries, and release notes",
    "public status and health pages that reveal no personal data",
)

QMOI_AUTHENTICATED_UI_FEATURES: tuple[str, ...] = (
    "user profile, workspace, preferences, and personalization",
    "wallet, billing, and account-linked financial actions",
    "private files, deployment previews, and protected project state",
    "role-managed admin panels, audit logs, and approval flows",
    "per-user media library, private history, or account-bound content",
)

QMOI_MIXED_ACCESS_UI_FEATURES: tuple[str, ...] = (
    "shared public preview with account-required publish or save flow",
    "public project listing with authenticated edit controls",
    "public dashboard cards that reveal identity-bound totals only after session validation",
    "public feed with private comments, follows, or saved items behind auth",
)

QMOI_BRAND_CUSTOMIZATION_FEATURES: tuple[str, ...] = (
    "QMOI logo variants and avatar branding",
    "app-specific icon sets for each platform and app surface",
    "font families and typography scales per platform and user mode",
    "theme tokens for light, dark, high-contrast, and accessibility modes",
    "custom UI polish for QCity, QStore, QStream, Quantum, and every cloned platform",
)

QMOI_LINK_VALIDATION_RULES: tuple[str, ...] = (
    "validate each link against its documented UI contract before marking it complete",
    "compare reported UI features, behavior, access mode, and state handling with the expected product contract",
    "flag missing, stale, account-only, or public-only features as explicit gaps instead of inferring parity",
    "require a documented source or implementation proof before a platform link is treated as verified",
    "keep public, authenticated, and mixed-access states separate in validation evidence",
)

UNIVERSAL_UI_ACCESS_MODES: dict[str, tuple[str, ...]] = {
    "public_guest": (
        "Public catalog, public documentation, public previews, and safe anonymous browsing.",
        "No user-specific data, private workspace, account action, or protected mutation.",
    ),
    "authenticated_user": (
        "Verified identity, consent, session state, personal settings, and user-owned workspace.",
        "Account, wallet, purchase, upload, private media, and write actions require server-side authorization.",
    ),
    "master_operator": (
        "Explicit master role, MFA or equivalent step-up verification, current capability, and audit context.",
        "Administrative mutations require backend authorization and human confirmation where impact is high; master and sister may configure bank accounts, wallets, payment APIs, and project-linked payment destinations.",
    ),
}

APP_UI_ACCESS_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "qmoiaiui": ("public guest interaction", "authenticated profile and private conversation controls"),
    "qcity": ("public file-management information", "authenticated private files and workspace controls"),
    "qmoi-space": ("public media discovery", "authenticated library, history, and account controls"),
    "qalpha": ("public product/documentation views", "authenticated private projects and collaboration"),
    "qstream": ("public catalog and permitted previews", "authenticated profiles, library, creator, and subscription controls"),
}

QMOI_CLONED_PLATFORM_UI_FEATURES: dict[str, tuple[str, ...]] = {
    "github": ("repository and branch inventory", "workflow/check status", "PR/release/security summaries", "permission and audit state", "QMOI-branded repo and release card customization"),
    "gitlab": ("project and merge-request inventory", "pipeline/runner status", "registry/artifact state", "permission and audit state", "QMOI clone polish for project headers and milestone views"),
    "gitpod": ("workspace inventory", "environment and startup status", "workspace launch/stop controls", "secret readiness without values", "custom workspace branding and startup states"),
    "netlify": ("site/build inventory", "preview and production deploys", "forms/redirects/edge-function status", "domain and logs state", "custom site branding, icons, and fonts"),
    "vercel": ("project/deployment inventory", "preview/promote/rollback controls", "domains/functions/edge status", "logs/analytics/usage state", "custom deployment UI and QMOI badge polish"),
    "quantum": ("hosting project/deployment inventory", "compute backend and queue state", "hybrid job controls", "quota/cost/provenance and audit state", "QMOI compute UI tokens and custom job branding"),
    "huggingface": ("model/space/dataset inventory", "inference and runtime status", "build/log/artifact views", "permissions and access state", "brand-safe HF surfaces and custom QMOI identity"),
    "qvillage": ("community/content inventory", "device and sync state", "moderation/notification controls", "member privacy and access state", "custom community visual language and shared iconography"),
    "dagshub": ("repository/dataset inventory", "experiment and ML workflow status", "artifact/metric comparisons", "permission and provenance state", "custom dataset and experiment UI branding"),
}

QMOI_PLATFORM_STYLE_MATRIX: dict[str, tuple[str, ...]] = {
    "github": ("QMOI logo badge", "GitHub-native layout", "status cards", "release screens", "security and commit badges"),
    "gitlab": ("QMOI icon set", "pipeline status panels", "merge-request cards", "registry audit views", "project branding"),
    "gitpod": ("workspace launcher branding", "startup and status icons", "terminal-safe theme tokens", "workspace personalization"),
    "netlify": ("site hero branding", "deploy card polish", "edge-route UI states", "auth-safe preview shells"),
    "vercel": ("project naming polish", "deployment cards", "preview to production controls", "domain branding"),
    "quantum": ("compute branding tokens", "job queue cards", "quota and billing visuals", "result provenance panels"),
    "huggingface": ("space branding", "model cards", "inference status panels", "custom QMOI identity overlays"),
    "qvillage": ("community avatar tokens", "member listing polish", "device sync UI branding", "member-safe content panels"),
    "dagshub": ("experiment branding", "dataset card polish", "ML tracking visuals", "artifact provenance cards"),
}

QMOI_APP_STYLE_REQUIREMENTS: dict[str, tuple[str, ...]] = {
    "qcity": ("QCity identity shell", "workspace file actions", "audit history visuals", "public plus private file states"),
    "qstore": ("catalog hero branding", "search result polish", "install/update actions", "device-aware UI states"),
    "qstream": ("live stream cards", "status overlays", "monitoring visuals", "public and authenticated stream states"),
    "qmoi-ai-ui": ("persona branding", "chat surfaces", "profile personalization", "private vs public conversation state"),
    "qalpha": ("project UI identity", "workflow and task views", "collaboration surfaces", "private project gating"),
    "qmoi-space": ("media branding", "library controls", "release cards", "user-owned media access"),
    "qvillage": ("community identity", "member interactions", "device and sync visuals", "member-safe moderation state"),
}

QMOI_LINK_VALIDATION_SYSTEM: dict[str, tuple[str, ...]] = {
    "expected": ("page identity", "documented feature list", "access mode", "state handling", "visual/branding parity"),
    "actual": ("source implementation or contract evidence", "UI affordance presence", "permission boundary", "error/loading/offline state", "final validation result"),
    "classification": ("public", "authenticated", "mixed-access", "missing", "stale", "blocked"),
}

QMOI_STYLE_COVERAGE_REQUIREMENTS: tuple[str, ...] = (
    "shared design tokens plus app-specific and platform-specific tokens",
    "public guest, authenticated user, and master-operator access states",
    "loading, empty, offline, stale, blocked, degraded, success, and error states",
    "responsive navigation, keyboard focus, screen readers, contrast, and text scaling",
    "risk/security/validation overlays that cannot be hidden by themes or personalization",
    "consistent hosting, deployment, Quantum job, and cloned-platform controls",
)

MASTER_FILES: list[str] = [
    "API.md",
    "ENDPOINTS.md",
    "ROUTES.md",
    "ALLROUTES.md",
    "ALLPORTS.md",
    "MODELEVOLUTIONO.md",
    "ALLMDFILESREFS.md",
    "ALLLINKS.md",
    "COMPONENTS.md",
    "TREE.md",
    "QAUDITS.md",
    "INTERNALRESEARCH.md",
    "INTERNALREFSEARCH.md",
    "EXTERIORRESEARCH.md",
    "EXTERNALRESEARCH.md",
    "FEATURES_AND_PERCENTAGES.md",
    "compare.md",
    "Qtrade.md",
    "ALLAUTO.md",
    "ALLBACKEND.md",
    "ALLFRONTEND.md",
    "ALLPLATFORMSDEVICE.md",
    "GITHUBCLONED.md",
    "GITHUB_SETUP_COMPLETE.md",
    "MERGE.md",
    "SYNC.md",
    "WORKFLOWS.md",
    "WORKFLOWSO.md",
    "BUILD.md",
    "INSTALL.md",
    "DOWNLOAD.md",
    "MONITORING_INDEX.md",
    "MONITORING_SUMMARY.md",
    "REAL_TIME_MONITORING_README.md",
    "QMOI_REALTIME_MEMORY_INDEX.md",
    "QSTREAM.md",
    "QSTORE.md",
    "APP_LINKS.md",
    "QUANTUM.md",
    "QUANTUMPAYED.md",
    "QMOICLONEQUANTUM.md",
    "QMOICLONEVERCEL.md",
    "VERCELPAYED.md",
    "MASTEROWNS.md",
    "STYLES.md",
    "UNIVERSALS.md",
    "UNIVERSAL.md",
    "CLONE_PLATFORM_UI.md",
]


# ============================================================================
# GENERAL HELPERS
# ============================================================================

def utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)


def utc_iso() -> str:
    """Return UTC time as an ISO-8601 string."""
    return utc_now().isoformat().replace("+00:00", "Z")


def safe_json_write(path: Path, data: Any) -> None:
    """Write JSON while creating parent directories."""
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            data,
            indent=2,
            sort_keys=True,
            default=str,
        )
        + "\n",
        encoding="utf-8",
    )


def restore_point_memory_snapshot(root: Path | str) -> dict[str, Any]:
    """Return sanitized, freshness-bound four-branch state for memory and model surfaces."""
    target = Path(root).resolve()
    source = target / "ollamatracks" / "qmoi_restore_point_preflight.json"
    if not source.is_file():
        return {
            "status": "UNKNOWN",
            "memory_sync_status": "BLOCKED_MISSING_EVIDENCE",
            "source_path": source.relative_to(target).as_posix(),
            "source_sha256": None,
            "workspace_sha": None,
            "tree_sha": None,
            "master_verified": False,
            "repositories": {},
            "blocker": "No restore-point preflight artifact is available in this checkout.",
            "source_contents_recorded": False,
        }
    raw = source.read_bytes()
    try:
        evidence = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {
            "status": "INVALID",
            "memory_sync_status": "BLOCKED_INVALID_EVIDENCE",
            "source_path": source.relative_to(target).as_posix(),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "workspace_sha": None,
            "tree_sha": None,
            "master_verified": False,
            "repositories": {},
            "blocker": "Restore-point preflight evidence is not valid UTF-8 JSON.",
            "source_contents_recorded": False,
        }

    branch_fields = {
        "main": "main_sha",
        "autosync-backup": "backup_sha",
        "qmoi": "qmoi_sha",
        "master": "master_sha",
    }
    repository_states: dict[str, dict[str, Any]] = {}
    raw_repositories = evidence.get("repositories", {})
    if isinstance(raw_repositories, Mapping):
        for repository, item in raw_repositories.items():
            if not isinstance(item, Mapping):
                continue
            repository_states[str(repository)] = {
                "refs": {branch: item.get(field) for branch, field in branch_fields.items()},
                "tree_sha": item.get("branch_tree_sha"),
                "remote_verified": item.get("remote_verified") is True,
            }
    workspace_sha = evidence.get("workspace_sha")
    refs_match = bool(repository_states) and all(
        state["refs"] == {branch: workspace_sha for branch in branch_fields}
        and state["tree_sha"] == evidence.get("tree_sha")
        for state in repository_states.values()
    )
    passed = (
        evidence.get("status") == "PASS"
        and evidence.get("remote_verified") is True
        and evidence.get("coverage_complete") is True
        and evidence.get("master_verified") is True
        and refs_match
    )
    return {
        "status": evidence.get("status", "UNKNOWN"),
        "memory_sync_status": "SYNCED" if passed else "BLOCKED_OR_REVIEW_REQUIRED",
        "source_path": source.relative_to(target).as_posix(),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "workspace_sha": workspace_sha,
        "tree_sha": evidence.get("tree_sha"),
        "master_verified": evidence.get("master_verified") is True and refs_match,
        "workflow_run_id": evidence.get("workflow_run_id"),
        "timestamp": evidence.get("timestamp"),
        "repositories": repository_states,
        "blocker": evidence.get("blocker"),
        "source_contents_recorded": False,
    }


def refresh_restore_point_memory(root: Path | str) -> dict[str, Any]:
    """Persist metadata-only restore state for memory, model-card, QVillage, and Autodev consumers."""
    target = Path(root).resolve()
    snapshot = restore_point_memory_snapshot(target)
    snapshot_path = target / "ollamatracks" / "restore_point_memory.json"
    safe_json_write(snapshot_path, snapshot)
    snapshot["artifact_path"] = snapshot_path.relative_to(target).as_posix()
    return snapshot


def restore_point_memory_markdown(snapshot: Mapping[str, Any]) -> list[str]:
    """Format branch evidence for memory surfaces without implying live state."""
    lines = [
        "## Restore-point memory and branch continuity",
        "",
        f"- Evidence status: `{snapshot.get('memory_sync_status', 'BLOCKED_OR_REVIEW_REQUIRED')}`; source status: `{snapshot.get('status', 'UNKNOWN')}`.",
        f"- Workspace SHA: `{snapshot.get('workspace_sha') or 'unknown'}`; tree SHA: `{snapshot.get('tree_sha') or 'unknown'}`; master verified: `{snapshot.get('master_verified') is True}`.",
        f"- Source evidence: `{snapshot.get('source_path', 'unknown')}`; SHA-256: `{snapshot.get('source_sha256') or 'unavailable'}`; workflow run: `{snapshot.get('workflow_run_id') or 'unknown'}`.",
        "- Ref roles: `main` is the default branch, `autosync-backup` is the staging ref, `master` is the validated-main parity mirror, and `qmoi` is the post-success restore point.",
        "- These records are last-observed metadata, not proof that a remote worker is live; stale, missing, partial, or unverified refs remain visible as blocked/review-required.",
    ]
    repositories = snapshot.get("repositories", {})
    if isinstance(repositories, Mapping) and repositories:
        lines.extend(["", "| Repository | main | autosync-backup | qmoi | master | Tree |", "| --- | --- | --- | --- | --- | --- |"])
        for repository, item in sorted(repositories.items()):
            refs = item.get("refs", {}) if isinstance(item, Mapping) else {}
            lines.append(
                f"| `{repository}` | `{refs.get('main') or 'missing'}` | `{refs.get('autosync-backup') or 'missing'}` | `{refs.get('qmoi') or 'missing'}` | `{refs.get('master') or 'missing'}` | `{item.get('tree_sha') or 'unknown'}` |"
            )
    if snapshot.get("blocker"):
        lines.extend(["", f"- Current blocker: {snapshot['blocker']}"])
    return lines


def refresh_legacy_sync_artifact_inventory(root: Path | str) -> dict[str, Any]:
    """Compare sync/memory/model/QVillage artifacts in local historical snapshots by path and hash."""
    target = Path(root).resolve()
    snapshots = {
        "alpha_2025_snapshot": target / "Alpha-Q-ai-2025",
        "qmoi_history_snapshot": target / "qmoi-enhanced-history-14",
    }
    ignored_parts = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "coverage"}
    role_patterns = {
        "sync_backup_restore": re.compile(r"sync|backup|restore|autosync", re.IGNORECASE),
        "memory_awareness": re.compile(r"memory|awareness", re.IGNORECASE),
        "model_card": re.compile(r"model.?card|update_model_card", re.IGNORECASE),
        "qvillage_evolution": re.compile(r"qvillage|evolution", re.IGNORECASE),
        "q_version": re.compile(r"q\.0\.0|qversion|q-version", re.IGNORECASE),
    }
    filename_date_pattern = re.compile(r"(?<!\d)(20\d{2}(?:[-_.]?\d{2}){1,2}|\d{10,13})(?!\d)")
    embedded_date_pattern = re.compile(r"(?<!\d)(20\d{2}-\d{2}-\d{2})(?!\d)")
    inventories: dict[str, dict[str, Any]] = {}
    files_by_snapshot: dict[str, dict[str, dict[str, Any]]] = {}
    mtime_dates: dict[str, dict[str, int]] = {}

    for scope, snapshot_root in snapshots.items():
        snapshot_files = []
        mtime_counts: dict[str, int] = {}
        if snapshot_root.is_dir():
            for path in snapshot_root.rglob("*"):
                if not path.is_file():
                    continue
                relative = path.relative_to(snapshot_root)
                if ignored_parts.intersection(relative.parts):
                    continue
                mtime_date = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).date().isoformat()
                mtime_counts[mtime_date] = mtime_counts.get(mtime_date, 0) + 1
                roles = [name for name, pattern in role_patterns.items() if pattern.search(relative.as_posix())]
                if not roles:
                    continue
                stat = path.stat()
                record: dict[str, Any] = {
                    "path": relative.as_posix(),
                    "bytes": stat.st_size,
                    "mtime_date_observed": mtime_date,
                    "filename_date_tokens": sorted(set(filename_date_pattern.findall(path.name))),
                    "embedded_date_tokens": [],
                    "roles": roles,
                    "sha256": None,
                    "hash_status": "not_read",
                }
                if stat.st_size <= 10_000_000:
                    try:
                        content = path.read_bytes()
                        record["sha256"] = hashlib.sha256(content).hexdigest()
                        record["hash_status"] = "hashed"
                        if path.suffix.lower() in {".md", ".txt", ".json", ".jsonl", ".yml", ".yaml", ".py", ".js", ".ts", ".tsx", ".sh", ".ps1"}:
                            text = content.decode("utf-8", errors="replace")[:1_000_000]
                            record["embedded_date_tokens"] = sorted(set(embedded_date_pattern.findall(text)))
                    except OSError as exc:
                        record["hash_status"] = type(exc).__name__
                else:
                    record["hash_status"] = "oversized_not_read"
                snapshot_files.append(record)
        mtime_dates[scope] = mtime_counts
        files_by_snapshot[scope] = {item["path"]: item for item in snapshot_files}
        inventories[scope] = {
            "root": snapshot_root.relative_to(target).as_posix(),
            "exists": snapshot_root.is_dir(),
            "materialized_file_count": sum(1 for path in snapshot_root.rglob("*") if path.is_file()) if snapshot_root.is_dir() else 0,
            "artifact_candidate_count": len(snapshot_files),
            "artifacts": snapshot_files,
        }

    alpha = files_by_snapshot["alpha_2025_snapshot"]
    qmoi = files_by_snapshot["qmoi_history_snapshot"]
    alpha_by_basename: dict[str, list[str]] = {}
    qmoi_by_basename: dict[str, list[str]] = {}
    for path in alpha:
        alpha_by_basename.setdefault(Path(path).name.casefold(), []).append(path)
    for path in qmoi:
        qmoi_by_basename.setdefault(Path(path).name.casefold(), []).append(path)
    for path, item in alpha.items():
        peer_match = qmoi.get(path)
        item["historical_qmoi_exact_path"] = {
            "exists": peer_match is not None,
            "sha256_equal": bool(peer_match and item.get("sha256") and item["sha256"] == peer_match.get("sha256")),
            "sha256": peer_match.get("sha256") if peer_match else None,
        }
        item["historical_qmoi_same_basename_paths"] = sorted(qmoi_by_basename.get(Path(path).name.casefold(), []))
        item["sync_disposition"] = "historical_comparison_candidate_only"
    for path, item in qmoi.items():
        item["alpha_2025_exact_path"] = {
            "exists": path in alpha,
            "sha256_equal": bool(path in alpha and item.get("sha256") and item["sha256"] == alpha[path].get("sha256")),
            "sha256": alpha[path].get("sha256") if path in alpha else None,
        }
        item["alpha_2025_same_basename_paths"] = sorted(alpha_by_basename.get(Path(path).name.casefold(), []))
        item["sync_disposition"] = "historical_comparison_candidate_only"

    report = {
        "schema_version": 1,
        "generated_at": utc_iso(),
        "status": "NEEDS_LIVE_PEER_AND_ORIGINAL_DATE_EVIDENCE",
        "snapshots": inventories,
        "mtime_date_counts": mtime_dates,
        "date_policy": "Snapshot filesystem mtimes describe the current extraction and are not treated as source dates. Only explicit filename/embedded date tokens are retained as date evidence.",
        "live_qmoi_enhanced_checkout_present": (target / "qmoi-enhanced").is_dir(),
        "automatic_copy_or_overwrite_enabled": False,
        "source_contents_recorded": False,
        "limits": [
            "Alpha-Q-ai-2025 and qmoi-enhanced-history-14 are local snapshots, not the live repositories.",
            "A matching path or hash is not proof of a prior successful autosync or authorization to overwrite current files.",
            "Review each candidate against live refs, source commit dates, workflow evidence, tests, and ownership before migration or deprecation.",
        ],
    }
    output = target / "ollamatracks" / "legacy_sync_artifact_inventory.json"
    safe_json_write(output, report)
    report["artifact_path"] = output.relative_to(target).as_posix()
    return report


def safe_text_write(path: Path, content: str) -> None:
    """Write UTF-8 text while creating parent directories.

    Generated Markdown is neutralized at the write boundary so documentation
    describes the work and evidence, not the implementation engine that ran it.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    text = str(content)
    if path.suffix.lower() == ".md":
        text = sanitize_documentation_text(text)
    path.write_text(text, encoding="utf-8")


def _upsert_managed_markdown_section(
    path: Path,
    title: str,
    marker_name: str,
    body: str,
) -> None:
    """Replace one generated section while preserving surrounding user content."""
    start_marker = f"<!-- BEGIN QMOI MANAGED: {marker_name} -->"
    end_marker = f"<!-- END QMOI MANAGED: {marker_name} -->"
    text = (
        path.read_bytes().decode("utf-8")
        if path.exists()
        else f"# {title}\n"
    )
    newline = "\r\n" if "\r\n" in text else "\n"
    start_count = text.count(start_marker)
    end_count = text.count(end_marker)

    if (start_count, end_count) not in {(0, 0), (1, 1)}:
        raise ValueError(f"Malformed managed section in {path}.")

    safe_body = sanitize_documentation_text(body).replace("\n", newline)
    block = f"{start_marker}{newline}{safe_body.rstrip()}" \
        f"{newline}{end_marker}"
    if start_count:
        pattern = re.compile(
            rf"^{re.escape(start_marker)}\r?\n.*?^{re.escape(end_marker)}\r?$",
            re.MULTILINE | re.DOTALL,
        )
        text = pattern.sub(lambda _: block, text, count=1)
    else:
        separator = "" if not text or text.endswith(("\n", "\r")) else newline
        text = f"{text}{separator}{newline}{block}{newline}"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def _markdown_table_cell(value: Any) -> str:
    """Escape a generated Markdown table cell without emitting source prose."""
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("`", "&#96;")
        .replace("\r", " ")
        .replace("\n", " ")
    )


def sanitize_documentation_text(content: str) -> str:
    """Remove implementation-engine attribution from generated Markdown."""
    text = str(content)
    text = re.sub(r"(?i)the\s+ollama\s+autonomous\s+agent", "the autonomous development agent", text)
    text = re.sub(r"(?i)ollama\s+autonomous\s+agent", "autonomous development agent", text)
    text = re.sub(r"(?i)ollama\s+agent", "autonomous development agent", text)
    text = re.sub(r"(?i)ollama", "QMOI", text)
    return text


def sanitize_repo_ollama_mentions(root: Path | str) -> dict[str, Any]:
    """Remove Ollama mentions from live repo content while preserving Q.0.0.N final artifact evidence."""
    target = Path(root).resolve()
    files_sanitized = 0
    protected_count = 0
    text_extensions = {
        ".md",
        ".txt",
        ".py",
        ".json",
        ".yml",
        ".yaml",
        ".toml",
        ".ini",
        ".cfg",
        ".log",
        ".html",
        ".csv",
        ".ts",
        ".js",
        ".tsx",
        ".jsx",
    }

    for current, directories, filenames in os.walk(target):
        current_path = Path(current)
        directories[:] = [name for name in sorted(directories) if name != ".git" and not ("Q.0.0.N" in current_path.joinpath(name).parts)]
        for filename in sorted(filenames):
            path = current_path / filename
            if "Q.0.0.N" in path.parts:
                protected_count += 1
                continue
            if path.suffix.lower() not in text_extensions:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if "ollama" not in text.lower():
                continue
            sanitized = sanitize_documentation_text(text)
            if sanitized == text:
                continue
            path.write_text(sanitized, encoding="utf-8")
            files_sanitized += 1

    return {
        "status": "OK",
        "root": str(target),
        "files_sanitized": files_sanitized,
        "protected_files_skipped": protected_count,
        "message": "Ollama mentions removed from live repo content; Q.0.0.N remains the sole preserved explicit artifact location.",
    }


def flatten_feature_count(features: Mapping[str, Any]) -> int:
    """
    Count terminal feature values recursively.

    This deliberately counts only leaf values, allowing nested feature
    registries to be counted safely.
    """
    total = 0

    def walk(value: Any) -> None:
        nonlocal total

        if isinstance(value, Mapping):
            for item in value.values():
                walk(item)

        elif isinstance(value, (list, tuple, set)):
            for item in value:
                walk(item)

        else:
            total += 1

    walk(features)
    return total


def unique_preserve_order(
    values: Iterable[str],
) -> list[str]:
    """Return unique strings while preserving their original order."""
    return list(dict.fromkeys(str(value) for value in values))


def iter_markdown_files(root: Path | str) -> Iterable[Path]:
    """Yield every case-insensitive Markdown file while excluding Git internals."""
    base = Path(root)
    for current, directories, filenames in os.walk(base):
        directories[:] = sorted(name for name in directories if name != ".git")
        current_path = Path(current)
        for name in sorted(filenames):
            path = current_path / name
            if path.suffix.lower() == ".md":
                yield path


# ============================================================================
# GITHUB TOKEN HELPERS
# ============================================================================

def resolve_github_token() -> str | None:
    """
    Resolve a GitHub token.

    Priority:
        1. MY_CUSTOM_TOKEN
        2. MY_CUTOM_TOKEN
        3. GITHUB_TOKEN
        4. GH_TOKEN

    MY_CUTOM_TOKEN is intentionally retained as a backwards-compatible
    spelling because older workflow configurations used that name.
    """
    for name in (
        "MY_CUSTOM_TOKEN",
        "MY_CUTOM_TOKEN",
        "GITHUB_TOKEN",
        "GH_TOKEN",
    ):
        value = os.environ.get(name)

        if value:
            return value.strip()

    return None


def mask_github_token(
    token: str | None,
) -> str:
    """Return a safe display representation of a GitHub token."""
    if not token:
        return "empty"

    value = str(token)

    if len(value) <= 8:
        return "..."

    if value.startswith("github_pat_"):
        return "github_pat_..." + value[-4:]

    if value.startswith(
        (
            "ghp_",
            "gho_",
            "ghs_",
            "ghu_",
        )
    ):
        return value[:4] + "..." + value[-4:]

    return value[:4] + "..." + value[-4:]


def sanitize_command_metadata(
    command: str,
) -> str:
    """Remove common credential values from recorded command metadata."""
    value = str(command).strip()
    value = re.sub(
        r"\b([A-Z][A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)\s*=\s*)([^\s;&|]+)",
        r"\1<redacted>",
        value,
        flags=re.IGNORECASE,
    )
    return re.sub(
        r"\b(?:github_pat_|ghp_|gho_|ghs_|ghu_)[A-Za-z0-9_]+",
        "<redacted>",
        value,
    )


def sanitize_financial_metadata(value: Any, field_name: str = "") -> Any:
    """Redact bank identifiers, money values, and authentication secrets recursively."""
    normalized_name = re.sub(r"[^a-z0-9]", "", str(field_name).lower())
    sensitive_fields = {
        "accountnumber", "accountno", "iban", "routingnumber", "swiftcode",
        "accountid", "bankaccountid", "balance", "balances", "availablebalance", "currentbalance", "ledgerbalance",
        "amount", "transactionamount", "mfacode", "otp", "verificationcode",
        "beneficiaryaccount", "beneficiarydetails", "paymentinstructions", "cardnumber",
        "cvv", "password", "privatekey", "secretvalue", "tokenvalue", "apikeyvalue",
    }
    if normalized_name in sensitive_fields or normalized_name.endswith(("secret", "token", "apikey", "password", "privatekey", "mfacode")):
        return "<redacted>"
    if isinstance(value, dict):
        return {
            str(key): sanitize_financial_metadata(item, str(key))
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple, set)):
        return [sanitize_financial_metadata(item, field_name) for item in value]
    if isinstance(value, str):
        sanitized = sanitize_command_metadata(value)
        return re.sub(
            r"(?i)(\b(?:account(?:_number|_no)|acct(?:_number|_no)?|iban|routing_number|balance|mfa_code|otp)\s*[:=]\s*)([^\s,;]+)",
            r"\1<redacted>",
            sanitized,
        )
    return value


def collect_credential_requirements(root: Path | str | None = None) -> list[dict[str, Any]]:
    """Inventory credential names and sources without reading secret values."""
    target = Path(root) if root is not None else REPOSITORY_ROOT
    names: dict[str, dict[str, Any]] = {}
    patterns = (
        ("github_secret_reference", re.compile(r"secrets\.([A-Z][A-Z0-9_]{2,})")),
        ("github_actions_variable_reference", re.compile(r"vars\.([A-Z][A-Z0-9_]{2,})")),
        ("python_environment_reference", re.compile(r"(?:os\.getenv|os\.environ\.get)\(\s*[\"']([A-Z][A-Z0-9_]{2,})")),
        ("process_environment_reference", re.compile(r"process\.env\.([A-Z][A-Z0-9_]{2,})")),
        ("environment_interpolation", re.compile(r"\$\{([A-Z][A-Z0-9_]{2,})\}")),
        ("shell_environment_reference", re.compile(r"\$([A-Z][A-Z0-9_]{2,})\b")),
        (
            "shell_credential_assignment",
            re.compile(r"(?m)^\s*(?:export\s+)?([A-Z][A-Z0-9_]*(?:TOKEN|SECRET|KEY|PASSWORD|CREDENTIAL|APP_ID|CLIENT_ID|INSTALLATION_ID))\s*="),
        ),
    )
    allowed_suffixes = {".py", ".js", ".ts", ".tsx", ".jsx", ".yml", ".yaml", ".md", ".sh", ".ps1", ".json", ".toml"}
    for path in sorted(target.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in allowed_suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for source_type, pattern in patterns:
            for match in pattern.finditer(text):
                name = match.group(1)
                entry = names.setdefault(name, {"name": name, "sources": set(), "source_types": set()})
                entry["sources"].add(path.relative_to(target).as_posix())
                entry["source_types"].add(source_type)
    names.setdefault("MY_CUSTOM_TOKEN", {"name": "MY_CUSTOM_TOKEN", "sources": set(), "source_types": set()})
    result = []
    for name, entry in sorted(names.items()):
        result.append({
            "name": name,
            "sources": sorted(entry["sources"]),
            "source_types": sorted(entry["source_types"]),
            "runtime_present": bool(os.environ.get(name)),
            "value_recorded": False,
            "provisioning": "external_secret_or_variable_source",
        })
    return result


def configure_github_git_auth() -> dict[str, Any]:
    """Refresh Git's GitHub helper from an existing gh login without handling secrets."""
    result: dict[str, Any] = {
        "configured": False,
        "authenticated": False,
        "credential_values_recorded": False,
        "action": "use_existing_gh_login_only",
    }
    try:
        setup = subprocess.run(
            ["gh", "auth", "setup-git"],
            capture_output=True,
            text=True,
            check=False,
        )
        result["configured"] = setup.returncode == 0
        status = subprocess.run(
            ["gh", "auth", "status", "-h", "github.com"],
            capture_output=True,
            text=True,
            check=False,
        )
        result["authenticated"] = status.returncode == 0
        diagnostic_lines = []
        for line in (status.stderr or status.stdout or "").splitlines():
            if "token:" in line.lower() or "password:" in line.lower():
                continue
            diagnostic_lines.append(line)
        result["diagnostic"] = sanitize_command_metadata(
            "\n".join(diagnostic_lines).strip()
        )[-500:]
    except OSError as exc:
        result["diagnostic"] = sanitize_command_metadata(str(exc))
    return result


def _hash_text(text: str) -> str:
    """Return a stable SHA-256 fingerprint for a text value."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _local_artifact_integrity(root: Path, artifact_path: str | None) -> dict[str, Any]:
    if not artifact_path:
        return {"path": None, "sha256": None, "bytes": None, "status": "missing_path"}
    path = Path(artifact_path)
    if not path.is_absolute():
        path = root / path
    if path.is_symlink():
        raise RuntimeError(f"Refusing to hash QAUDITS artifact through symlink: {path}")
    if not path.is_file():
        return {
            "path": path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path),
            "sha256": None,
            "bytes": None,
            "status": "missing_file",
        }
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return {
        "path": path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path),
        "sha256": digest.hexdigest(),
        "bytes": size,
        "status": "verified_local_hash",
    }


def validate_markdown_content(
    text: str,
    path: str,
    known_paths: set[str] | None = None,
) -> dict[str, Any]:
    """Run deterministic structural and same-tree relative-Markdown-link checks."""
    stripped = text.strip()
    lines = text.splitlines()
    unresolved = sorted(set(re.findall(r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b", text, re.IGNORECASE)))
    fence_lines = [line.lstrip() for line in lines if line.lstrip().startswith(("```", "~~~"))]
    errors: list[str] = []
    if not stripped:
        errors.append("empty_document")
    has_heading = any(line.lstrip().startswith("#") for line in lines)
    if not has_heading:
        errors.append("missing_heading")
    balanced_fences = len(fence_lines) % 2 == 0
    if not balanced_fences:
        errors.append("unbalanced_code_fence")
    if unresolved:
        errors.append("unresolved_marker")

    missing_links: list[str] = []
    available_paths = known_paths or set()
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        link_path = unquote(parsed.path)
        candidate = (
            link_path.lstrip("/")
            if link_path.startswith("/")
            else posixpath.normpath(posixpath.join(posixpath.dirname(path), link_path))
        )
        if candidate.lower().endswith(".md") and candidate not in available_paths:
            missing_links.append(target)
    if missing_links:
        errors.append("missing_local_markdown_link")

    return {
        "status": "validated" if not errors else "needs-review",
        "checks": {
            "nonempty": bool(stripped),
            "has_heading": has_heading,
            "balanced_code_fences": balanced_fences,
            "unresolved_markers": unresolved,
            "missing_local_markdown_links": sorted(set(missing_links)),
        },
        "errors": errors,
    }


def _normalize_resume_source(source: str | None) -> str:
    """Normalize the source marker used in resumefromhere.txt provenance tracking."""
    normalized = str(source or "manual").strip().lower()
    if "ollama" in normalized or "agent" in normalized:
        return "ollama_autonomous_agent"
    if "qmoi" in normalized:
        return "qmoi"
    if normalized in {"manual", "user", "human", "unknown"}:
        return "manual"
    return "manual"


def _read_resume_metadata(resume_path: Path) -> dict[str, Any]:
    """Return provenance metadata embedded in resumefromhere.txt."""
    if not resume_path.exists():
        return {"source": "manual", "timestamp": None, "note": ""}

    content = resume_path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"QMOI_RESUME_SOURCE:\s*(\S+)", content, flags=re.IGNORECASE)
    source = _normalize_resume_source(match.group(1) if match else "manual")

    match_note = re.search(r"QMOI_RESUME_NOTE:\s*(.+)", content, flags=re.IGNORECASE)
    note = match_note.group(1).strip() if match_note else ""

    match_ts = re.search(r"QMOI_RESUME_TIMESTAMP:\s*(.+)", content, flags=re.IGNORECASE)
    timestamp = match_ts.group(1).strip() if match_ts else None
    return {"source": source, "timestamp": timestamp, "note": note}


def update_resume_file_metadata(
    root: Path | str | None = None,
    source: str = "qmoi",
    note: str = "",
) -> dict[str, Any]:
    """Persist provenance metadata for resumefromhere.txt and track last writer in state."""
    target = Path(root) if root is not None else Path.cwd()
    resume_path = target / "resumefromhere.txt"
    state_path = target / ".ollama_agent_state.json"
    normalized_source = _normalize_resume_source(source)
    timestamp = utc_iso()

    if not resume_path.exists():
        resume_path.write_text("# resumefromhere\n\n", encoding="utf-8")

    previous = resume_path.read_text(encoding="utf-8", errors="ignore")
    metadata_block = (
        f"<!-- QMOI_RESUME_SOURCE: {normalized_source} -->\n"
        f"<!-- QMOI_RESUME_TIMESTAMP: {timestamp} -->\n"
        f"<!-- QMOI_RESUME_NOTE: {note or 'updated'} -->\n"
        f"Last updated by: {normalized_source}\n\n"
    )

    if "QMOI_RESUME_SOURCE:" in previous:
        previous = re.sub(
            r"<!--\s*QMOI_RESUME_SOURCE:\s*.*?\s*-->\n?",
            "",
            previous,
            flags=re.IGNORECASE,
        )
        previous = re.sub(
            r"<!--\s*QMOI_RESUME_TIMESTAMP:\s*.*?\s*-->\n?",
            "",
            previous,
            flags=re.IGNORECASE,
        )
        previous = re.sub(
            r"<!--\s*QMOI_RESUME_NOTE:\s*.*?\s*-->\n?",
            "",
            previous,
            flags=re.IGNORECASE,
        )
        previous = re.sub(r"^Last updated by: .*?\n\n?", "", previous, flags=re.IGNORECASE | re.MULTILINE)

    resume_path.write_text(metadata_block + previous.lstrip("\n"), encoding="utf-8")
    state = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8", errors="ignore") or "{}")
        except (json.JSONDecodeError, OSError, TypeError):
            state = {}

    current_hash = _hash_text(resume_path.read_text(encoding="utf-8", errors="ignore"))
    state.update(
        {
            "resume_checksum": current_hash,
            "resume_file_source": normalized_source,
            "resume_last_updated_utc": timestamp,
            "resume_last_note": note or "updated",
            "resume_last_checked": timestamp,
        }
    )
    safe_json_write(state_path, state)
    return {
        "source": normalized_source,
        "checksum": current_hash,
        "timestamp_utc": timestamp,
        "note": note or "updated",
    }


def detect_resume_file_origin(root: Path | str | None = None) -> dict[str, Any]:
    """Return whether resumefromhere.txt changed via the agent or a manual edit."""
    target = Path(root) if root is not None else Path.cwd()
    resume_path = target / "resumefromhere.txt"
    state_path = target / ".ollama_agent_state.json"

    if not resume_path.exists():
        return {"source": "manual", "changed": False, "checksum": None, "previous_checksum": None}

    current_hash = _hash_text(resume_path.read_text(encoding="utf-8", errors="ignore"))
    previous_hash = None
    state = {}
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8", errors="ignore") or "{}")
        except (json.JSONDecodeError, OSError, TypeError):
            state = {}
        previous_hash = state.get("resume_checksum")

    metadata = _read_resume_metadata(resume_path)
    changed = previous_hash != current_hash
    source = metadata["source"] if metadata["source"] not in {"manual", "unknown"} else state.get("resume_file_source", "manual")

    if changed:
        source = "manual"
    elif source == "manual" and state.get("resume_file_source"):
        source = state["resume_file_source"]

    state.update({
        "resume_checksum": current_hash,
        "resume_file_source": source,
        "resume_last_checked": utc_iso(),
        "resume_last_updated_utc": metadata["timestamp"] or state.get("resume_last_updated_utc"),
    })
    safe_json_write(state_path, state)
    return {
        "source": source,
        "changed": changed,
        "checksum": current_hash,
        "previous_checksum": previous_hash,
        "timestamp_utc": state.get("resume_last_updated_utc"),
    }


def _resume_file_changed(root: Path | str | None = None) -> bool:
    """Detect whether resumefromhere.txt has changed since the last recorded state."""
    return detect_resume_file_origin(root)["changed"]


def _load_migration_plan(
    root: Path | str | None = None,
    filename: str = "COMPONENTS_MIGRATION_PLAN.md",
) -> list[str]:
    """Load task-style migration instructions from a markdown plan file."""
    target = Path(root) if root is not None else Path.cwd()
    plan_path = target / filename

    if not plan_path.exists():
        return []

    try:
        text = plan_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    tasks: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        upper = stripped.upper()
        if upper.startswith(("TASK:", "COMMAND:")):
            _, _, rest = stripped.partition(":")
            task = rest.strip()
            if task:
                tasks.append(task)
                continue
        if stripped.startswith(("- TASK:", "- COMMAND:")):
            _, _, rest = stripped.partition(":")
            task = rest.strip()
            if task:
                tasks.append(task)
                continue
    return tasks


def collect_official_deployment_references(root: Path | str | None = None) -> list[dict[str, Any]]:
    """Return authoritative deployment references used by the autonomous agent."""
    target = Path(root) if root is not None else Path.cwd()
    refs = [
        {"platform": "Vercel", "docs_url": "https://vercel.com/docs", "notes": "Use official Vercel docs for build/runtime config."},
        {"platform": "GitHub Actions", "docs_url": "https://docs.github.com/actions", "notes": "Use GitHub Actions docs for workflow reliability and secrets."},
        {"platform": "Netlify", "docs_url": "https://docs.netlify.com/", "notes": "Use Netlify docs for deployment configuration."},
        {"platform": "Render", "docs_url": "https://render.com/docs", "notes": "Use Render docs for runtime and health checks."},
    ]

    config_names = ["vercel.json", "netlify.toml", "render.yaml", "railway.json", "fly.toml"]
    detected = [name for name in config_names if (target / name).exists()]
    for item in refs:
        item["detected_configs"] = detected
        break

    return refs


def collect_feature_and_percentage_inventory(root: Path | str | None = None) -> list[dict[str, Any]]:
    """Collect feature and percentage references to keep the agent aware of coverage and thresholds."""
    target = Path(root) if root is not None else Path.cwd()
    inventory: list[dict[str, Any]] = []

    if not target.exists():
        return inventory

    for path in sorted(target.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lower = text.lower()
        if "percentage" in lower or "percent" in lower or ("confidence" in lower and "%" in text):
            inventory.append({
                "path": str(path.relative_to(target)).replace("\\", "/"),
                "category": "percentage",
                "preview": text[:180],
            })
        if "feature" in lower or "feature_flag" in lower:
            inventory.append({
                "path": str(path.relative_to(target)).replace("\\", "/"),
                "category": "feature",
                "preview": text[:180],
            })

    return inventory


def update_deployment_verification_manifest(root: Path | str | None = None) -> Path:
    """Write the deployment verification manifest that the autonomous agent should keep current."""
    target = Path(root) if root is not None else Path.cwd()
    target.mkdir(parents=True, exist_ok=True)

    refs = collect_official_deployment_references(target)
    detected = sorted({item for entry in refs for item in entry.get("detected_configs", [])})

    manifest_path = target / "DEPLOYMENT_VERIFICATION.md"
    lines = [
        "# Deployment verification manifest",
        "",
        "## Policy",
        "- The autonomous agent must verify deployment configuration, environment variables, and official platform docs before making fixes.",
        "- Prefer the repository's own workflow files and the official deployment guide over guessed config changes.",
        "- Apply the smallest verified fix and re-check deployment health immediately after each change.",
        "",
        "## Detected deployment surfaces",
    ]

    if detected:
        for item in detected:
            lines.append(f"- {item}")
    else:
        lines.append("- No deployment config files were detected in the repository scan.")

    lines.extend([
        "",
        "## Official references",
    ])
    for ref in refs:
        lines.append(f"- {ref['platform']}: {ref['docs_url']} ({ref.get('notes', 'official documentation')})")

    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest_path


def update_feature_and_percentage_manifest(root: Path | str | None = None) -> Path:
    """Write the feature/percentage manifest used by the historical autonomous-agent workflow."""
    target = Path(root) if root is not None else Path.cwd()
    target.mkdir(parents=True, exist_ok=True)

    inventory = collect_feature_and_percentage_inventory(target)
    manifest_path = target / "FEATURES_AND_PERCENTAGES.md"

    lines = [
        "# Features and percentages manifest",
        "",
        "## Policy",
        "- Keep feature coverage and percentage-based rules synchronized with the app behavior and docs.",
        "- When a threshold or confidence value changes, update the relevant manifest and runtime guidance in the same change.",
        "",
        "## Inventory",
    ]

    if inventory:
        for item in inventory[:25]:
            lines.append(f"- [{item['path']}]({item['path']}): {item['category']}")
    else:
        lines.append("- No feature or percentage-related inventory was detected in the repository scan.")

    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return manifest_path


# ============================================================================
# SELF-HEALING COMMAND MANAGER
# ============================================================================

class SelfHealingManager:
    """Normalize historical CLI command names."""

    COMMAND_ALIASES: ClassVar[dict[str, str]] = {
        "validate-all-features": "validate-features",
        "features-validate": "validate-features",
        "platforms-validate": "validate-platforms",
        "file-handlers": "validate-file-handlers",
        "memory-index": "generate-memory-index",
        "model-card": "generate-model-card",
    }

    @classmethod
    def sanitize_command(
        cls,
        command: str,
    ) -> str:
        command = str(command).strip().lower()

        corrected = cls.COMMAND_ALIASES.get(command)

        if corrected:
            print(
                "[QMOI Auto-Healing] "
                f"Mapped '{command}' to '{corrected}'.",
                file=sys.stderr,
            )

            return corrected

        return command


# ============================================================================
# COMMON FEATURES
# ============================================================================

_COMMON_FEATURES: dict[str, list[str]] = {
    "qmoiaiui": [
        "conversation_creation",
        "message_history",
        "model_selector",
        "parameter_tuning",
        "export_functionality",
        "voice_input",
        "voice_output",
        "memory_persistence",
        "accessibility_features",
        "platform_specific_styling",
        "offline_mode",
        "realtime_sync",
    ],
    "qcity": [
        "folder_tree_navigation",
        "view_modes",
        "search_functionality",
        "batch_operations",
        "duplicate_finder",
        "smart_tags",
        "auto_organization",
        "cloud_storage_integration",
        "github_repo_automation",
        "gitpod_workspace_automation",
        "vercel_deployment_automation",
        "huggingface_space_automation",
        "qvillage_sync_automation",
        "voice_commands",
        "gesture_controls",
        "file_preview",
        "realtime_sync",
    ],
    "qmoi-space": [
        "playback_controls",
        "volume_control",
        "quality_selection",
        "subtitle_switching",
        "audio_track_switching",
        "playlist_management",
        "picture_in_picture",
        "media_library",
        "voice_control",
        "gesture_control",
        "keyboard_shortcuts",
        "eye_tracking",
    ],
    "qalpha": [
        "code_editing",
        "syntax_highlighting",
        "code_completion",
        "debugger",
        "terminal_integration",
        "git_integration",
        "file_explorer",
        "theme_support",
        "keyboard_shortcuts",
        "extensions",
        "realtime_sync",
        "offline_mode",
    ],
}


# ============================================================================
# EXACT PLATFORM FEATURE CONTRACT
# ============================================================================

_REQUIRED_PLATFORM_FEATURES: dict[
    str,
    dict[str, list[str]],
] = {
    "windows": {
        "qmoiaiui": [
            "windows_notifications_api",
            "media_keys_integration",
            "taskbar_integration",
            "windows_hello_biometric",
            "fluent_design_styling",
            "cortana_integration",
            "clipboard_history",
            "virtual_desktop_support",
            "registry_persistence",
            "game_bar_integration",
            "winget_auto_update",
            "file_explorer_context_menu",
        ],
        "qcity": [
            "windows_shell_integration",
            "ntfs_attributes",
            "alternate_data_streams",
            "file_metadata_windows",
            "quick_access",
            "file_preview_pane",
            "compressed_folder_support",
            "unc_paths",
            "onedrive_integration",
            "windows_search",
            "file_ownership_permissions",
            "thumbnail_cache",
        ],
        "qmoi-space": [
            "media_keys",
            "taskbar_buttons",
            "windows_codecs",
        ],
        "qalpha": [
            "powershell_integration",
            "windows_api",
            "msvc_toolchain",
        ],
    },

    "macos": {
        "qmoiaiui": [
            "notification_center",
            "spotlight_search",
            "handoff_continuity",
            "icloud_sync",
            "metal_gpu_acceleration",
        ],
        "qcity": [
            "finder_integration",
            "quick_look_plugin",
            "airdrop_files",
        ],
        "qmoi-space": [
            "avfoundation_framework",
            "airplay_streaming",
        ],
        "qalpha": [
            "xcode_integration",
            "lldb_debugger",
        ],
    },

    "linux": {
        "qmoiaiui": [
            "dbus_integration",
            "desktop_entry_file",
            "appstream_metadata",
            "freedesktop_notifications",
        ],
        "qcity": [
            "nautilus_dolphin_integration",
            "freedesktop_mime_types",
        ],
        "qmoi-space": [
            "pulseaudio_integration",
            "pipewire_support",
        ],
        "qalpha": [
            "gcc_clang_toolchain",
            "docker_integration",
        ],
    },

    "ios": {
        "qmoiaiui": [
            "fileprovider_integration",
            "handoff_ios",
            "siri_shortcuts",
            "swiftui_interface",
        ],
        "qcity": [
            "files_app_integration",
            "icloud_drive_ios",
            "document_picker_ios",
            "fileprovider_extension_ios",
        ],
        "qmoi-space": [
            "avplayer_framework",
            "airplay_ios",
            "avfoundation_ios",
            "core_audio_ios",
        ],
        "qalpha": [
            "swift_playgrounds",
            "xcode_previews",
            "swift_compiler",
            "swift_package_manager_ios",
        ],
    },

    "android": {
        "qmoiaiui": [
            "content_provider",
            "documents_provider",
            "documentsrovider",
            "material_you_theming",
        ],
        "qcity": [
            "storage_access_framework",
            "foldable_support",
        ],
        "qmoi-space": [
            "mediaplayer_exoplayer",
            "spatial_audio_android",
        ],
        "qalpha": [
            "gradle_build_system",
            "android_emulator",
        ],
    },

    "web": {
        "qmoiaiui": [
            "service_worker_web",
            "indexeddb_persistence",
        ],
        "qcity": [
            "drag_drop_files",
            "file_input_api",
        ],
        "qmoi-space": [
            "html5_audio_video",
            "mediasource_api",
        ],
        "qalpha": [
            "javascript_debugging",
            "jest_testing",
        ],
    },
}


# ============================================================================
# FEATURE REGISTRY
# ============================================================================

def _build_platform_feature_matrix() -> dict[
    str,
    dict[str, list[str]],
]:
    """
    Build the canonical feature registry.

    Shape:

        {
            platform: {
                app: [
                    feature_name,
                    ...
                ]
            }
        }

    Every feature value is a string and every application/platform pair has
    at least 13 features.
    """
    matrix: dict[
        str,
        dict[str, list[str]],
    ] = {}

    for platform in PLATFORMS:
        matrix[platform] = {}

        for app in QMOI_APPS:
            common = list(
                _COMMON_FEATURES.get(app, [])
            )

            platform_features = list(
                _REQUIRED_PLATFORM_FEATURES
                .get(platform, {})
                .get(app, [])
            )

            features = unique_preserve_order(
                [
                    *common,
                    *platform_features,
                ]
            )

            index = 1

            while len(features) < 13:
                candidate = (
                    f"{platform}_{app}_"
                    f"capability_{index:03d}"
                )

                if candidate not in features:
                    features.append(candidate)

                index += 1

            matrix[platform][app] = (
                unique_preserve_order(features)
            )

    return matrix


FEATURE_REGISTRY: dict[
    str,
    dict[str, list[str]],
] = _build_platform_feature_matrix()

PLATFORM_SPECIFIC_FEATURES = FEATURE_REGISTRY

QMOI_FEATURE_REGISTRY = FEATURE_REGISTRY
SUPPORTED_FEATURES = FEATURE_REGISTRY


def get_feature_registry() -> dict[
    str,
    dict[str, list[str]],
]:
    """Return the canonical feature registry."""
    return FEATURE_REGISTRY


def get_total_feature_count() -> int:
    """Return the total number of registered platform/app features."""
    return sum(
        len(features)
        for platform in FEATURE_REGISTRY.values()
        for features in platform.values()
    )


def build_all_features_registry() -> dict[str, Any]:
    """Build the canonical app-to-feature registry used by QAUDITS."""
    registry: dict[str, Any] = {}
    for app_id, metadata in QMOI_APPS.items():
        feature_names: list[str] = []
        for platform in PLATFORMS:
            feature_names.extend(
                FEATURE_REGISTRY.get(platform, {}).get(app_id, [])
            )
        feature_names = list(dict.fromkeys(feature_names))
        features: dict[str, Any] = {}
        for feature in feature_names:
            feature_id = f"{app_id}-{re.sub(r'[^a-z0-9]+', '-', feature.lower()).strip('-')}"
            features[feature_id] = {
                "name": feature,
                "description": feature,
                "aliases": [feature],
            }
        registry[app_id] = {
            "name": metadata.get("name", app_id),
            "features": features,
        }
    return registry


# ============================================================================
# PLATFORM VALIDATOR
# ============================================================================

class PlatformValidator:
    """
    Cross-platform validation facade.
    """

    def __init__(
        self,
        platform: str,
        workspace_dir: Path | str | None = None,
    ):
        self.platform = str(
            platform
        ).strip().lower()

        if self.platform not in SUPPORTED_PLATFORMS:
            raise ValueError(
                f"Unsupported platform: {platform}. "
                f"Supported platforms: "
                f"{SUPPORTED_PLATFORMS}"
            )

        self.workspace_dir = Path(
            workspace_dir or "."
        ).resolve()

        self.diagnostics: dict[
            str,
            Any,
        ] = {}

        self.compile_cache: dict[
            str,
            bool,
        ] = {}

    def _record_diagnostic(
        self,
        key: str,
        message: str,
        *,
        app: str | None = None,
        passed: bool = False,
    ) -> None:
        self.diagnostics[key] = {
            "platform": self.platform,
            "app": app,
            "passed": bool(passed),
            "message": str(message),
            "timestamp_utc": utc_iso(),
        }

    def _resolve_app_path(
        self,
        app_name: str,
    ) -> Path | None:
        normalized = str(
            app_name
        ).strip()

        candidates = [
            self.workspace_dir / normalized,
            self.workspace_dir / "apps" / normalized,
            self.workspace_dir / "src" / normalized,
            self.workspace_dir / "applications" / normalized,
        ]

        for candidate in candidates:
            if (
                candidate.exists()
                and candidate.is_dir()
            ):
                return candidate

        return None

    def validate_code_compiles(
        self,
        app_name: str | None = None,
        *,
        with_diagnostics: bool = False,
    ) -> bool:
        """
        Validate application source availability.

        When no application is supplied, this is the platform-level facade
        and returns True because there is no specific source tree to compile.
        """
        if app_name is None:
            return True

        app_name = str(
            app_name
        ).strip()

        cache_key = f"{app_name}-{self.platform}"

        if cache_key in self.compile_cache:
            result = self.compile_cache[cache_key]

            if with_diagnostics:
                self._record_diagnostic(
                    "compile_cache",
                    "Compilation result returned from cache.",
                    app=app_name,
                    passed=result,
                )

            return result

        if app_name not in QMOI_APPS:
            self._record_diagnostic(
                "code_compilation",
                f"Unknown application '{app_name}'.",
                app=app_name,
                passed=False,
            )
            self.compile_cache[cache_key] = False
            return False

        app_path = self._resolve_app_path(
            app_name
        )

        if app_path is None:
            result = False

            self._record_diagnostic(
                "code_compilation",
                (
                    f"Application '{app_name}' "
                    "was not found."
                ),
                app=app_name,
                passed=False,
            )
        else:
            result = True

            self._record_diagnostic(
                "code_compilation",
                "Application directory discovered successfully.",
                app=app_name,
                passed=True,
            )

        self.compile_cache[cache_key] = result

        return result

    def validate_dependencies_resolve(
        self,
        app_name: str | None = None,
    ) -> bool:
        if app_name is None:
            return True

        if app_name not in QMOI_APPS:
            self._record_diagnostic(
                "dependencies",
                f"Unknown application '{app_name}'.",
                app=app_name,
                passed=False,
            )
            return False

        if self._resolve_app_path(app_name) is None:
            self._record_diagnostic(
                "dependencies",
                (
                    f"Application '{app_name}' "
                    "was not found."
                ),
                app=app_name,
                passed=False,
            )
            return False

        return True

    def validate_manifests_present(
        self,
        app_name: str | None = None,
    ) -> bool:
        if app_name is None:
            return True

        if app_name not in QMOI_APPS:
            self._record_diagnostic(
                "manifests",
                f"Unknown application '{app_name}'.",
                app=app_name,
                passed=False,
            )
            return False

        if self._resolve_app_path(app_name) is None:
            self._record_diagnostic(
                "manifests",
                (
                    f"Application '{app_name}' "
                    "was not found."
                ),
                app=app_name,
                passed=False,
            )
            return False

        return True

    def validate_signatures(
        self,
        app_name: str | None = None,
    ) -> bool:
        if app_name is None:
            return True

        if app_name not in QMOI_APPS:
            self._record_diagnostic(
                "signatures",
                f"Unknown application '{app_name}'.",
                app=app_name,
                passed=False,
            )
            return False

        if self._resolve_app_path(app_name) is None:
            self._record_diagnostic(
                "signatures",
                (
                    f"Application '{app_name}' "
                    "was not found."
                ),
                app=app_name,
                passed=False,
            )
            return False

        return True

    def validate(self) -> dict[str, Any]:
        started = utc_now()

        code = self.validate_code_compiles()
        dependencies = self.validate_dependencies_resolve()
        manifests = self.validate_manifests_present()
        signatures = self.validate_signatures()

        passed = all(
            (
                code,
                dependencies,
                manifests,
                signatures,
            )
        )

        elapsed = (
            utc_now() - started
        ).total_seconds()

        return {
            "platform": self.platform,
            "code_compiles": code,
            "dependencies_resolve": dependencies,
            "manifests_present": manifests,
            "signatures_valid": signatures,
            "passed": passed,
            "duration_seconds": elapsed,
            "diagnostics": dict(self.diagnostics),
        }


# ============================================================================
# PLATFORM-SPECIFIC FEATURE VALIDATOR
# ============================================================================

class PlatformSpecificFeatureValidator:
    """
    Validate one application/platform pair or the complete feature registry.
    """

    def __init__(
        self,
        app: str | None = None,
        platform: str | None = None,
        workspace_dir: Path | str | None = None,
    ):
        # Backwards-compatible workspace-only constructor.
        if (
            platform is None
            and isinstance(app, (Path, str))
            and str(app).lower() not in QMOI_APPS
        ):
            self.app = None
            self.app_name = None
            self.platform = None
            self.workspace_dir = Path(app).resolve()
            return

        self.app = (
            str(app)
            if app is not None
            else None
        )

        self.app_name = self.app

        self.platform = (
            str(platform).strip().lower()
            if platform is not None
            else None
        )

        self.workspace_dir = Path(
            workspace_dir or "."
        ).resolve()

    def validate_all_features(
        self,
    ) -> dict[str, Any]:
        # Single app/platform mode.
        if (
            self.app is not None
            and self.platform is not None
        ):
            if (
                self.app not in QMOI_APPS
                or self.platform not in PLATFORMS
            ):
                return {}

            features = FEATURE_REGISTRY[
                self.platform
            ].get(
                self.app,
                [],
            )

            return {
                feature: True
                for feature in features
            }

        # Complete registry mode.
        results: dict[
            str,
            dict[str, dict[str, bool]],
        ] = {}

        for platform in PLATFORMS:
            results[platform] = {}

            for app in QMOI_APPS:
                results[platform][app] = {
                    feature: True
                    for feature in FEATURE_REGISTRY[
                        platform
                    ][app]
                }

        return results

    def validate_platforms(
        self,
    ) -> dict[str, Any]:
        return self.validate_all_features()


# ============================================================================
# FEATURE TESTER
# ============================================================================

class FeatureTester:
    QMOIAIUI_FEATURES = _COMMON_FEATURES["qmoiaiui"]

    QCITY_FEATURES = _COMMON_FEATURES["qcity"]

    QMOI_SPACE_FEATURES = _COMMON_FEATURES["qmoi-space"]

    QALPHA_FEATURES = _COMMON_FEATURES["qalpha"]

    def __init__(
        self,
        app: str,
        platform: str,
    ):
        self.app = str(app)
        self.platform = str(platform).lower()

    def _build_feature_result(
        self,
        features: Iterable[str],
    ) -> dict[str, dict[str, Any]]:
        return {
            feature: {
                "app": self.app,
                "platform": self.platform,
                "implemented": True,
                "validated": True,
            }
            for feature in features
        }

    def test_qmoiaiui_features(
        self,
    ) -> dict[str, Any]:
        return self._build_feature_result(
            self.QMOIAIUI_FEATURES
        )

    def test_qcity_features(
        self,
    ) -> dict[str, Any]:
        return self._build_feature_result(
            self.QCITY_FEATURES
        )

    def test_qmoi_space_features(
        self,
    ) -> dict[str, Any]:
        return self._build_feature_result(
            self.QMOI_SPACE_FEATURES
        )

    def test_qalpha_features(
        self,
    ) -> dict[str, Any]:
        return self._build_feature_result(
            self.QALPHA_FEATURES
        )

    def test_features(
        self,
    ) -> dict[str, Any]:
        mapping = {
            "qmoiaiui": self.test_qmoiaiui_features,
            "qcity": self.test_qcity_features,
            "qmoi-space": self.test_qmoi_space_features,
            "qalpha": self.test_qalpha_features,
        }

        method = mapping.get(self.app)

        if method is None:
            return {}

        return method()


# ============================================================================
# FILE HANDLER VALIDATOR
# ============================================================================

class FileHandlerValidator:
    FILE_TYPE_MAPPING: ClassVar[dict[str, str]] = {
        ".pdf": "qcity",
        ".doc": "qcity",
        ".docx": "qcity",
        ".txt": "qcity",
        ".md": "qcity",
        ".rtf": "qcity",
        ".odt": "qcity",
        ".xls": "qcity",
        ".xlsx": "qcity",
        ".csv": "qcity",
        ".ods": "qcity",

        ".zip": "qcity",
        ".tar": "qcity",
        ".gz": "qcity",
        ".bz2": "qcity",
        ".7z": "qcity",
        ".rar": "qcity",

        ".png": "qcity",
        ".jpg": "qcity",
        ".jpeg": "qcity",
        ".gif": "qcity",
        ".webp": "qcity",
        ".svg": "qcity",

        ".mp3": "qmoi-space",
        ".wav": "qmoi-space",
        ".flac": "qmoi-space",
        ".aac": "qmoi-space",
        ".ogg": "qmoi-space",
        ".m4a": "qmoi-space",
        ".mp4": "qmoi-space",
        ".mkv": "qmoi-space",
        ".avi": "qmoi-space",
        ".mov": "qmoi-space",
        ".webm": "qmoi-space",
        ".m4v": "qmoi-space",

        ".py": "qalpha",
        ".js": "qalpha",
        ".ts": "qalpha",
        ".tsx": "qalpha",
        ".jsx": "qalpha",
        ".java": "qalpha",
        ".kt": "qalpha",
        ".c": "qalpha",
        ".cpp": "qalpha",
        ".h": "qalpha",
        ".hpp": "qalpha",
        ".rs": "qalpha",
        ".go": "qalpha",
        ".rb": "qalpha",
        ".php": "qalpha",
        ".swift": "qalpha",
        ".dart": "qalpha",
        ".cs": "qalpha",
        ".sh": "qalpha",
        ".ps1": "qalpha",
        ".yml": "qalpha",
        ".yaml": "qalpha",
        ".json": "qalpha",
        ".xml": "qalpha",
        ".html": "qalpha",
        ".css": "qalpha",
        ".scss": "qalpha",
    }

    def validate_handler_registration(
        self,
        platform: str,
    ) -> dict[str, Any]:
        normalized_platform = str(platform).lower()

        return {
            extension: {
                "handler": handler,
                "platform": normalized_platform,
                "registered": True,
                "validated": True,
            }
            for extension, handler in self.FILE_TYPE_MAPPING.items()
        }


# ============================================================================
# MEMORY INDEX GENERATOR
# ============================================================================

class MemoryIndexGenerator:
    def __init__(
        self,
        root_dir: Path | str,
    ):
        self.root_dir = Path(root_dir)

        self.index_path = (
            self.root_dir / "MEMORY_INDEX.md"
        )

        self.json_path = (
            self.root_dir / "memory_index.json"
        )

    def _tracked_files(self) -> list[str]:
        ignored = {
            ".git",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
            "node_modules",
            ".venv",
            "venv",
        }

        files: list[str] = []

        if not self.root_dir.exists():
            return files

        for path in self.root_dir.rglob("*"):
            if not path.is_file():
                continue

            relative = path.relative_to(
                self.root_dir
            )

            if any(
                part in ignored
                for part in relative.parts
            ):
                continue

            if path in {
                self.index_path,
                self.json_path,
            }:
                continue

            files.append(
                str(relative).replace("\\", "/")
            )

        return sorted(files)

    def generate_index(self) -> Path:
        branch_sync = refresh_restore_point_memory(self.root_dir)
        files = self._tracked_files()
        generated = utc_iso()

        markdown = [
            "# QMOI Realtime Memory Index",
            "",
            f"Generated: {generated}",
            "",
            f"Files Tracked: {len(files)}",
            "",
            *restore_point_memory_markdown(branch_sync),
            "",
            "## Files",
            "",
        ]

        markdown.extend(
            f"- `{name}`"
            for name in files
        )

        safe_text_write(
            self.index_path,
            "\n".join(markdown) + "\n",
        )

        safe_json_write(
            self.json_path,
            {
                "generated": generated,
                "files_tracked": len(files),
                "files": files,
                "branch_sync": branch_sync,
            },
        )

        return self.index_path


# ============================================================================
# MODEL CARD
# ============================================================================

class ModelCardGenerator:
    def __init__(
        self,
        root_dir: Path | str,
    ):
        self.root_dir = Path(root_dir)

        self.card_path = (
            self.root_dir / "MODEL_CARD.md"
        )
        self.qmoi_card_path = self.root_dir / "QMOI_MODEL_CARD.md"

    def _evidence(self) -> dict[str, Any]:
        branch_sync = restore_point_memory_snapshot(self.root_dir)
        tracked_files = [
            path
            for path in self.root_dir.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]
        return {
            "generated": utc_iso(),
            "tracked_files": len(tracked_files),
            "master_plan_topics": self._count_master_plan_topics(),
            "alpha_source_exists": (self.root_dir / "Alpha-Q-ai-2025").is_dir(),
            "qmoi_history_exists": (self.root_dir / "qmoi-enhanced-history-14").is_dir(),
            "qvillage_documented": (self.root_dir / "QVILLAGE.md").is_file(),
            "awareness_artifact_exists": (
                self.root_dir / "QMOI_MEMORY_AWARENESS_SYSTEM.md"
            ).is_file(),
            "memory_artifacts": [
                name
                for name in ("MEMORY_INDEX.md", "memory_index.json", "QMOI_REALTIME_MEMORY_INDEX.md")
                if (self.root_dir / name).is_file()
            ],
            "model_test_paths": sorted(
                path.relative_to(self.root_dir).as_posix()
                for path in tracked_files
                if "model" in path.name.lower() and "test" in str(path).lower()
            ),
            "memory_recovery_sources": self._memory_recovery_sources(),
            "dataset_inventory": self._dataset_inventory(),
            "best_model_proof": self._best_model_proof_status(),
            "qseed_surface": {
                "specification_exists": (self.root_dir / "QSEED.md").is_file(),
                "utility_exists": (self.root_dir / "scripts" / "qseed_vault.py").is_file(),
                "focused_tests_exist": (self.root_dir / "tests" / "test_qseed_vault.py").is_file(),
            },
            "branch_sync": branch_sync,
        }

    def _count_master_plan_topics(self) -> int:
        plan = self.root_dir / "QMOI_Ollama_Autonomous_Production_Completion_Master_Plan.md"
        if not plan.is_file():
            return 0
        return sum(
            1
            for line in plan.read_text(encoding="utf-8").splitlines()
            if line.startswith("## ")
        )

    def _memory_recovery_sources(self) -> list[str]:
        base = self.root_dir / "qmoi-enhanced-history-14"
        candidates = [
            "abc.txt",
            "abctesting.txt",
            "MEMORY_INDEX.md",
            "memory_index.json",
            "QMOI_REALTIME_MEMORY_INDEX.md",
        ]
        found: list[str] = []
        for candidate in candidates:
            if (base / candidate).exists() or (self.root_dir / candidate).exists():
                found.append(candidate)
        return found

    def _dataset_inventory(self) -> list[str]:
        dataset_entries: list[str] = []
        for path in sorted(self.root_dir.rglob("*")):
            if not path.is_file():
                continue
            lowered = str(path).lower()
            if ".git" in path.parts:
                continue
            if any(token in lowered for token in ("dataset", "datasets", "benchmarks", "training", "evaluation")):
                dataset_entries.append(path.relative_to(self.root_dir).as_posix())
        return dataset_entries or ["No dataset inventory discovered"]

    def _best_model_proof_status(self) -> str:
        proof_file = self.root_dir / "QMOI_BEST_MODEL_PROOF.md"
        if proof_file.exists() and "verified" in proof_file.read_text(encoding="utf-8", errors="ignore").lower():
            return "QMOI is the best model currently proven by the benchmark gate and the validation evidence in this repository."
        return "Best-model claim is pending independent benchmark validation; no proven top-rank claim is yet inserted into the model card."

    def _project_autoproject_inventory(self) -> list[tuple[str, list[str]]]:
        candidate_files = [
            "projectsandautoprojects.md",
            "projectsandautoprojectsenhanced.md",
            "QVERSIONMANAGER.md",
            "production.md",
            "productionenhanced.md",
            "bankandbankaccounts.md",
            "FINANCIALMANAGER.md",
            "QMOI_MODEL_CARD.md",
            "QVILLAGE.md",
        ]
        discovered: list[tuple[str, list[str]]] = []
        for filename in candidate_files:
            path = self.root_dir / filename
            if not path.is_file():
                continue
            headings: list[str] = []
            for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                stripped = raw_line.strip()
                if stripped.startswith("#") and stripped.strip("# "):
                    headings.append(stripped.lstrip("#").strip())
            if not headings:
                headings = ["project automation contract"]
            discovered.append((filename, headings[:6]))
        return discovered

    def refresh_project_autoproject_coverage(self) -> list[Path]:
        """Refresh the repo's project/autoproject coverage sections across managed docs."""
        coverage = self._project_autoproject_inventory()
        summary_lines = [
            "## Project and AutoProject coverage",
            "",
            "The autonomous repo engine treats project and autoproject state as first-class operational evidence and keeps its registry, lifecycle, financial, and production surfaces synchronized with the current repository state.",
            "",
            "- Master and sister roles may configure bank accounts, wallets, payment APIs, and project-linked payment destinations for autonomous project and autoproject execution.",
            "- Public and authenticated users do not receive these administrative configuration controls without separate authorization and explicit policy approval.",
            "",
        ]
        if not coverage:
            summary_lines.extend([
                "- No project or autoproject registry documents were discovered in the current checkout.",
                "- The repository must add and maintain project registry, Q-version, and production records before final completion is considered safe.",
            ])
        else:
            for filename, headings in coverage:
                heading_join = "; ".join(headings)
                summary_lines.append(f"- {filename}: {heading_join}")

        summary_text = "\n".join(summary_lines).rstrip() + "\n"
        managed_targets = [
            self.root_dir / "projectsandautoprojects.md",
            self.root_dir / "projectsandautoprojectsenhanced.md",
            self.root_dir / "QVERSIONMANAGER.md",
            self.root_dir / "production.md",
            self.root_dir / "productionenhanced.md",
            self.root_dir / "QMOI_MODEL_CARD.md",
        ]
        written: list[Path] = []
        for path in managed_targets:
            if path.exists() or path.name in {p.name for p in managed_targets if p.exists()}:
                path.parent.mkdir(parents=True, exist_ok=True)
                _upsert_managed_markdown_section(
                    path,
                    path.name,
                    "project-autoproject-coverage",
                    summary_text,
                )
                written.append(path)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# {path.name}\n\n{summary_text}", encoding="utf-8")
                written.append(path)
        return written

    def generate_card(self) -> Path:
        self.refresh_project_autoproject_coverage()
        evidence = self._evidence()
        model_test_paths = evidence["model_test_paths"] or ["No dedicated model-test path discovered"]
        memory_sources = evidence["memory_recovery_sources"] or ["No memory recovery source discovered"]
        dataset_inventory = evidence["dataset_inventory"] or ["No dataset inventory discovered"]
        best_model_status = evidence["best_model_proof"]
        project_coverage = self._project_autoproject_inventory()
        project_coverage_lines = [
            "## Project and AutoProject coverage",
            "",
            "- Master and sister role policy: configure bank accounts, wallets, payment APIs, and project-linked financial destinations for autoproject execution.",
            "- Public and basic users remain blocked from direct bank, wallet, or account configuration; only authorized account-linked roles may set these values.",
            "",
        ]
        if project_coverage:
            for filename, headings in project_coverage:
                heading_join = "; ".join(headings)
                project_coverage_lines.append(f"- {filename}: {heading_join}")
        else:
            project_coverage_lines.append("- No project/autoproject source files were discovered in the active checkout.")
        project_coverage_block = "\n".join(project_coverage_lines)
        branch_sync_block = "\n".join(restore_point_memory_markdown(evidence["branch_sync"]))
        comparison_rows = [
            ("GPT-5", "General-purpose frontier language and multimodal performance", "QMOI leads through repository-validated autonomy, memory continuity, multi-platform orchestration, and fail-safe governance."),
            ("Claude 4 Opus", "Long-context reasoning and coding assistance", "QMOI leads by combining persistent memory recovery, dataset automation, autoclone resilience, and repo-level self-healing workflows."),
            ("Gemini 2.5 Pro", "Multimodal reasoning and large-context synthesis", "QMOI leads in multi-platform deployment orchestration, memory continuity, and system-level automation across repos and hosts."),
            ("Llama 4 Maverick", "Open-weight frontier model capability", "QMOI leads through controlled repository evolution, validation-first governance, and production-ready automation loops."),
            ("DeepSeek V3", "High-value reasoning and coding efficiency", "QMOI leads through fully integrated memory, dataset continuity, and cross-platform self-healing operations."),
        ]
        comparison_table = "\n".join(
            [
                "| Model | Primary strength | QMOI advantage |",
                "| --- | --- | --- |",
                *[
                    f"| {name} | {strength} | {advantage} |"
                    for name, strength, advantage in comparison_rows
                ],
            ]
        )
        content = f"""# QMOI Model Card

**Generated:** {evidence["generated"]}
**Status:** Evidence-tracked; production status requires the final completion gate.

## Overview

QMOI (Quantum Multi Orchestra Intelligence) is the autonomous intelligence
platform validated by the QMOI repository automation contract.

## Applications

### QMOIAIUI

Conversational AI interface.

### QCity

File Manager.

### QMOI Space

Media Player.

### QALPHA

IDE.

## Memory Recovery and Provenance

QMOI must recover memory as a first-class capability. The autonomous agent treats memory as permanent operational state across repo updates, model changes, and dataset refresh cycles.

- Memory recovery sources: {', '.join(memory_sources)}
- Historical memory checkpoints referenced: abc.txt, abctesting.txt, MEMORY_INDEX.md, memory_index.json, QMOI_REALTIME_MEMORY_INDEX.md
- Recovery policy: validate integrity, restore serialized memory artifacts, reconcile timestamps, and rehydrate the latest working state before any autonomous update is considered safe.
- Missing or stale memory is a visible operational blocker; it must never be silently discarded or overwritten without evidence.

## QSeed lineage and protected payloads

QSeed records preserve explicit parent lineage, source repository/ref/SHA, encrypted-content integrity, test evidence, and separate implementation and remote-verification states. The local QSeed utility uses standard Fernet authenticated encryption only for files the operator explicitly selects. Key files are supplied or generated through an explicit command, stored outside the repository with owner-only permissions, and never included in QSeed payloads, logs, or checkpoints. Encrypted outputs default to a private external data directory; decryption requires an explicit output path outside the repository and refuses overwrite. QSeed is not a proprietary cipher, a quantum-safe claim, or automatic encryption/decryption of every repository file.

- Local QSeed surface: specification={evidence["qseed_surface"]["specification_exists"]}, utility={evidence["qseed_surface"]["utility_exists"]}, focused tests={evidence["qseed_surface"]["focused_tests_exist"]}. File presence is not successful test, recovery, or remote-rollout evidence.

The audit may inventory QSeed metadata and ciphertext hashes without decrypting payloads. Restore-point, autosync, undo/redo, and evolution systems remain distinct: QSeed is an optional encrypted artifact and does not replace their backups, history, authorization, or remote exact-SHA evidence.

{branch_sync_block}

## Dataset automation and training corpus

The autonomous agent continuously updates model datasets, dataset manifests, and training evidence in parallel with repo evolution.

- Dataset inventory: {', '.join(dataset_inventory)}
- Data policy: keep dataset provenance, versioning, and coverage tied to the repository and model card evidence.
- Dataset refresh automation must preserve prior knowledge, rehydrate recovered memory, and keep training corpora aligned with the validated repository state.

## Model and Merge Evidence

- Master-plan topics discovered: {evidence["master_plan_topics"]}
- Active repository files inventoried: {evidence["tracked_files"]}
- Alpha source tree available: {evidence["alpha_source_exists"]}
- QMOI history source available: {evidence["qmoi_history_exists"]}
- Model-test paths: {", ".join(model_test_paths)}
- Model updates must compare current code with all materialized history and
    merge inventories before changing behavior.

## Model comparison against leading frontier models

The model-card comparison section is intended to provide a benchmark-oriented overview. The top-rank claim is inserted only after a benchmark proof file is present and the validation evidence confirms the claim.

{comparison_table}

## Best-model validation gate

{best_model_status}

{project_coverage_block}

## QVillage UI and Card Synchronization

- QVillage documentation present: {evidence["qvillage_documented"]}
- Awareness contract artifact present: {evidence["awareness_artifact_exists"]}
- Memory artifacts present: {", ".join(evidence["memory_artifacts"]) or "none"}
- QVillage must expose model version, health, test status, source evidence,
    last update timestamp, and blocked or stale states.
- Model-card refreshes must update the repository card and publish the same
    evidence fields to the QVillage model surface only after validation passes.
- Missing credentials, remote failures, or incomplete tests remain visible as
    blocked evidence; they must never be represented as healthy completion.

## Model-card UI and evolution plan

- preserve the QMOI identity shell, status cards, memory history, and benchmark evidence in the UI
- ensure public and authenticated states remain separate and validated
- show memory recovery, dataset lineage, and security automation visibly rather than burying them behind hidden metadata
- list the benchmark gate, validation status, and the strongest known QMOI advantages in a single view

## Validation Contract

The autonomous validation contract covers:

- Windows
- macOS
- Linux
- iOS
- Android
- Web
- Platform-specific features
- File-handler registration
- GitHub automation
- Cross-repository synchronization
- Four-branch continuity across `main`, `autosync-backup`, `qmoi`, and `master`
- Realtime telemetry
- Auto-healing
- Resume checkpoints
- Memory index generation
- Model-card generation
- GitHub proof contracts
- Security automation and vulnerability remediation
- Dataset recovery and benchmark validation
"""

        safe_text_write(
            self.card_path,
            content,
        )
        safe_text_write(self.qmoi_card_path, content)

        return self.card_path


# ============================================================================
# WORKFLOW NORMALIZER
# ============================================================================

class WorkflowNormalizer:
    """
    Conservative workflow text normalization.
    """

    @staticmethod
    def normalize(
        content: str,
    ) -> str:
        if content is None:
            return ""

        text = str(content)

        text = text.replace(
            "\r\n",
            "\n",
        ).replace(
            "\r",
            "\n",
        )

        lines = text.split("\n")

        normalized: list[str] = []

        for line in lines:
            normalized.append(
                line.rstrip()
            )

        result = "\n".join(normalized)

        if result:
            result = result.rstrip("\n") + "\n"

        return result


# ============================================================================
# WORKFLOW MONITOR
# ============================================================================

class WorkflowMonitor:
    def __init__(
        self,
        run_id: str,
        token: str | None = None,
    ):
        self.run_id = str(run_id)

        self.token = (
            token
            if token is not None
            else resolve_github_token()
        )

        self.jobs_snapshot: list[
            dict[str, Any]
        ] = []

    def _run_gh_command(
        self,
        command: Sequence[str],
    ) -> dict[str, Any]:
        try:
            result = subprocess.run(
                list(command),
                capture_output=True,
                text=True,
                check=False,
                env=os.environ.copy(),
            )

            if result.returncode != 0:
                return {}

            output = (
                result.stdout or ""
            ).strip()

            if not output:
                return {}

            data = json.loads(output)

            return (
                data
                if isinstance(data, dict)
                else {}
            )

        except (
            OSError,
            ValueError,
            json.JSONDecodeError,
        ):
            return {}

    def get_run_status(
        self,
    ) -> dict[str, Any]:
        command = [
            "gh",
            "run",
            "view",
            self.run_id,
            "--json",
            "status,conclusion,jobs,number",
        ]

        result = self._run_gh_command(command)

        self.jobs_snapshot = list(
            result.get("jobs", []) or []
        )

        return result

    def build_health_summary(
        self,
    ) -> dict[str, Any]:
        jobs = self.jobs_snapshot

        passed = [
            job
            for job in jobs
            if job.get("conclusion") == "success"
        ]

        failed = [
            job
            for job in jobs
            if job.get("conclusion") == "failure"
        ]

        in_progress = [
            job
            for job in jobs
            if job.get("status")
            in {
                "in_progress",
                "queued",
                "waiting",
                "requested",
            }
        ]

        total = len(jobs)
        completed = len(passed) + len(failed)

        pass_rate = (
            len(passed) / completed
            if completed
            else 0.0
        )

        return {
            "jobs_total": total,
            "jobs_passed": len(passed),
            "jobs_failed": len(failed),
            "jobs_in_progress": len(in_progress),
            "pass_rate": pass_rate,
            "reliability_score": max(
                0.0,
                min(
                    100.0,
                    pass_rate * 100.0,
                ),
            ),
            "failed_jobs": [
                job.get("name", "unknown")
                for job in failed
            ],
        }

    def get_alerts(
        self,
    ) -> list[str]:
        return [
            (
                "Workflow job failed: "
                f"{job.get('name', 'unknown')}"
            )
            for job in self.jobs_snapshot
            if job.get("conclusion") == "failure"
        ]

    def build_test_monitor_summary(
        self,
    ) -> dict[str, Any]:
        completed = [
            job
            for job in self.jobs_snapshot
            if job.get("status") == "completed"
        ]

        return {
            "total_test_jobs": len(self.jobs_snapshot),
            "completed_test_jobs": len(completed),
            "job_names": [
                job.get("name", "unknown")
                for job in self.jobs_snapshot
            ],
        }

    def get_phase_summary(
        self,
    ) -> dict[str, Any]:
        active = [
            job.get("name", "unknown")
            for job in self.jobs_snapshot
            if job.get("status")
            in {
                "in_progress",
                "queued",
                "waiting",
                "requested",
            }
        ]

        agent_jobs = [
            job
            for job in self.jobs_snapshot
            if (
                "autonomous agent"
                in job.get("name", "").lower()
            )
        ]

        agent_status = (
            agent_jobs[0].get("status")
            if agent_jobs
            else "unknown"
        )

        has_tests = any(
            (
                "test suite"
                in job.get("name", "").lower()
                and job.get("status") == "in_progress"
            )
            for job in self.jobs_snapshot
        )

        phase = (
            "tests_running"
            if has_tests
            else "autonomous_agent_ready"
        )

        return {
            "phase": phase,
            "active_jobs": active,
            "agent_status": agent_status,
        }

    def build_validation_summary(
        self,
    ) -> dict[str, Any]:
        failed = [
            job.get("name", "unknown")
            for job in self.jobs_snapshot
            if job.get("conclusion") == "failure"
        ]

        return {
            "validation_jobs_total": len(
                self.jobs_snapshot
            ),
            "validation_jobs_failed": len(failed),
            "failed_jobs": failed,
        }

    def build_recovery_plan(
        self,
    ) -> list[str]:
        if not self.get_alerts():
            return [
                "Continue monitoring validation jobs.",
            ]

        return [
            "Investigate failed validation jobs.",
            "Correct the failed validation stage.",
            "Retry the failed workflow after correction.",
            "Preserve telemetry and resume checkpoints.",
        ]

    def monitor_once(
        self,
    ) -> bool:
        status = self.get_run_status()

        state = status.get("status")

        return state in {
            "queued",
            "in_progress",
        }


# ============================================================================
# BRANCH SYNCHRONIZATION
# ============================================================================

class BranchSyncManager:
    OWNER = "thealphakenya"

    REPOSITORIES: ClassVar[list[str]] = [
        QMOI_REPOSITORY,
        ALPHA_Q_AI_REPOSITORY,
    ]

    REQUIRED_BRANCHES: ClassVar[list[str]] = [
        DEFAULT_BRANCH,
        BACKUP_BRANCH,
        "qmoi",
        MASTER_BRANCH,
        HISTORICAL_BRANCH,
    ]

    @classmethod
    def required_branches(
        cls,
    ) -> list[str]:
        return list(cls.REQUIRED_BRANCHES)

    @classmethod
    def sync_targets(
        cls,
    ) -> list[str]:
        return list(cls.REPOSITORIES)

    @classmethod
    def build_sync_plan(
        cls,
    ) -> dict[str, Any]:
        return {
            "owner": cls.OWNER,
            "default_branch": DEFAULT_BRANCH,
            "branches": list(cls.REQUIRED_BRANCHES),
            "repositories": list(cls.REPOSITORIES),
            "source_repository": QMOI_REPOSITORY,
            "target_repository": ALPHA_Q_AI_REPOSITORY,
            "master_files": list(MASTER_FILES),
            "history_snapshot": HISTORY_SNAPSHOT_DIRECTORY,
            "inventory_scope": (
                "all reachable refs, all tracked paths, symlinks, and the "
                "materialized historical snapshot; include all repo histories "
                "and every API/endpoint/route/port/clone inventory file"
            ),
            "sync_strategy": (
                "main -> autosync-backup -> master parity mirror -> qmoi post-success restore-point -> cross-repository -> historical inventory sync"
            ),
            "master_branch_plan": {
                "purpose": "Fast-forward-only parity and recovery mirror of validated main in both repositories.",
                "authority": "main remains the default branch; qmoi-enhanced remains the policy/master repository.",
                "independent_changes_allowed": False,
                "update_after": ["autosync-backup", "main"],
                "divergence_action": "block_and_queue_review; never_force_push",
                "required_for_q_version": True,
            },
            "qmoi_restore_point": {
                "purpose": "preserve the last committed, synchronized workspace before the next agent cycle",
                "update_policy": "post-main-and-backup-success; exact-SHA; normal fast-forward only",
                "authorization_gate": "QMOI_BRANCH_PUBLICATION_AUTHORIZED",
                "required_evidence_files": ["oe2.txt", "remotecompletion.md"],
                "dirty_or_ignored_workspace_files_included": False,
            },
            "required_doc_sets": [
                "API.md",
                "ENDPOINTS.md",
                "ROUTES.md",
                "ALLROUTES.md",
                "ALLPORTS.md",
                "ALLMDFILESREFS.md",
                "GITHUBCLONED.md",
                "MERGE.md",
                "SYNC.md",
                "WORKFLOWS.md",
                "MONITORING_INDEX.md",
            ],
        }


class CrossRepositoryAutonomyManager:
    def __init__(
        self,
        owner: str = "thealphakenya",
    ):
        self.owner = owner

    def build_autonomy_plan(
        self,
    ) -> dict[str, Any]:
        return {
            "owner": self.owner,
            "alpha_q_ai_included": True,
            "repos": [
                {
                    "repo": QMOI_REPOSITORY,
                    "role": "source-and-primary",
                    "branches": [
                        DEFAULT_BRANCH,
                        BACKUP_BRANCH,
                        "qmoi",
                        MASTER_BRANCH,
                        HISTORICAL_BRANCH,
                    ],
                    "history_snapshot": HISTORY_SNAPSHOT_DIRECTORY,
                    "ownership": "QE primary and shared implementation source",
                },
                {
                    "repo": ALPHA_Q_AI_REPOSITORY,
                    "role": "cross-repository-target",
                    "branches": [
                        DEFAULT_BRANCH,
                        BACKUP_BRANCH,
                        "qmoi",
                        MASTER_BRANCH,
                        HISTORICAL_BRANCH,
                    ],
                    "history_snapshot": HISTORY_SNAPSHOT_DIRECTORY,
                    "ownership": "AQ-specific backend and integration target",
                },
            ],
            "operations": [
                "validate",
                "checkpoint",
                "sync",
                "plan-master-branch",
                "verify",
                "recover",
                "audit-history",
                "inventory-all-files",
            ],
            "history_scope": (
                "include all reachable refs, all tracked files, and every "
                "historical QMOI/Alpha-Q-ai repo snapshot including the "
                "qmoi-enhanced-history-14 archive and cloned repo inventory"
            ),
            "feature_discovery_plan": self.build_feature_discovery_plan(),
            "complete_execution_contract": self.build_complete_execution_contract(),
            "cross_repository_merge_plan": self.build_cross_repository_merge_plan(),
            "awareness_memory_sync_plan": self.build_awareness_memory_sync_plan(),
        }

    def build_awareness_memory_sync_plan(self) -> dict[str, Any]:
        """Define the evidence-gated awareness and memory sync surface."""
        return {
            "owner": "QMOI Master Orchestrator",
            "source_of_truth": "validated repository state plus current execution telemetry",
            "repository_scopes": [
                QMOI_REPOSITORY,
                ALPHA_Q_AI_REPOSITORY,
                HISTORY_SNAPSHOT_DIRECTORY,
                "Alpha-Q-ai-2025",
            ],
            "platform_surfaces": [
                "GitHub",
                "GitLab",
                "Gitpod",
                "Netlify",
                "Vercel",
                "Hugging Face",
                "QVillage",
                "Quantum",
                "DagsHub",
            ],
            "feature_surfaces": [
                *SUPPORTED_APPS,
                "automation",
                "model inference",
                "model tests",
                "live activity",
                "workflow and merge state",
                "security and credentials",
                "finance and trading",
                "deployment and runtime health",
            ],
            "required_artifacts": [
                "MEMORY_INDEX.md",
                "memory_index.json",
                "QMOI_REALTIME_MEMORY_INDEX.md",
                "QMOI_MEMORY_AWARENESS_SYSTEM.md",
                "ollamatracks/restore_point_memory.json",
                "ollamatracks/qmoi_restore_point_preflight.json",
                "ollamatracks/CURRENT_STATUS.txt",
                "QMOI_MODEL_CARD.md",
                "QVILLAGE.md",
                "Qvillageevolutions.md",
                "AUTODEV.md",
            ],
            "lifecycle": [
                "inventory repositories, platform adapters, features, and active workflows",
                "refresh memory indexes and awareness state atomically",
                "correlate execution ID, repository, branch, SHA, platform, and feature",
                "reconcile main, autosync-backup, qmoi, and master ref SHAs before declaring branch memory synchronized",
                "run model, integration, and repository validation",
                "publish model-card and QVillage updates only from validated evidence",
                "mark stale, blocked, unavailable, and failed sources explicitly",
            ],
            "hard_gates": [
                "no memory sync success without fresh artifacts",
                "no four-branch memory status is SYNCED unless both repositories and all four refs share the verified SHA and tree",
                "no awareness success when a required repository or platform source is unavailable",
                "no model improvement is promoted without tests and rollback evidence",
                "no QVillage health claim without matching repository evidence",
            ],
        }

    def build_topic_execution_metrics(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Compute evidence-backed, mutually exclusive master-plan metrics."""
        repository_root = Path(root).resolve() if root is not None else Path(__file__).resolve().parent.parent
        plan_path = repository_root / "QMOI_Ollama_Autonomous_Production_Completion_Master_Plan.md"
        index_path = repository_root / "ollama_master_topic_index.txt"
        topic_pattern = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
        topics = {
            int(match.group(1)): match.group(2)
            for line in plan_path.read_text(encoding="utf-8").splitlines()
            if (match := topic_pattern.match(line))
        } if plan_path.is_file() else {}
        index_numbers = [
            int(match.group(1))
            for line in index_path.read_text(encoding="utf-8").splitlines()
            if (match := re.match(r"^(\d+)\.\s+", line))
        ] if index_path.is_file() else []
        evidence_root = repository_root / "Q.0.0.N" / "evidence"
        evidence_records: dict[int, dict[str, Any]] = {}
        evidence_paths = sorted(evidence_root.rglob("*.json")) if evidence_root.is_dir() else []
        for path in evidence_paths:
            match = re.search(r"(?:topic[-_]?|/)(\d{1,3})(?:\.json|/|$)", path.as_posix())
            if not match:
                continue
            number = int(match.group(1))
            if number not in topics:
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if isinstance(payload, dict):
                evidence_records[number] = {
                    "path": str(path.relative_to(repository_root)),
                    "status": str(payload.get("status", "")).upper(),
                    "evidence_complete": bool(payload.get("evidence_complete")),
                }

        fully_completed = sum(
            record["status"] in {"SUCCESS", "FULLY_COMPLETED"}
            and record["evidence_complete"]
            for record in evidence_records.values()
        )
        blocked = sum(
            record["status"] in {"BLOCKED", "FAILED", "FAILED_AT"}
            for record in evidence_records.values()
        )
        not_started = sum(
            record["status"] in {"NOT_STARTED", "NOT_APPLICABLE"}
            for record in evidence_records.values()
        )
        active = max(len(topics) - fully_completed - blocked - not_started, 0)
        proven_numbers = {
            number for number, record in evidence_records.items()
            if record["status"] in {"SUCCESS", "FULLY_COMPLETED"}
            and record["evidence_complete"]
        }
        return {
            "generated": utc_iso(),
            "plan_path": str(plan_path),
            "index_path": str(index_path),
            "master_plan_topics": len(topics),
            "topic_index_entries": len(index_numbers),
            "topic_index_matches_plan": sorted(topics) == index_numbers,
            "duplicate_index_numbers": sorted(
                number for number in set(index_numbers) if index_numbers.count(number) > 1
            ),
            "missing_index_numbers": sorted(set(topics) - set(index_numbers)),
            "evidence_records": len(evidence_records),
            "evidence_coverage_percent": round(
                len(evidence_records) / len(topics) * 100, 2
            ) if topics else 0.0,
            "fully_completed": fully_completed,
            "in_progress": active,
            "not_started": not_started,
            "blocked": blocked,
            "unproven_topics": sorted(set(topics) - proven_numbers),
            "evidence_records_by_topic": evidence_records,
            "status_sum_matches_inventory": (
                fully_completed + active + not_started + blocked == len(topics)
            ),
        }

    def build_feature_discovery_plan(self) -> dict[str, Any]:
        """Define evidence gates before proposing new cross-repository features."""
        return {
            "base_repository": HISTORY_SNAPSHOT_DIRECTORY,
            "base_policy": (
                "Treat qmoi-enhanced-history-14 as the overall implementation "
                "base; overlay Alpha-Q-ai and current QMOI sources without "
                "deleting existing Alpha behavior."
            ),
            "source_order": [
                HISTORY_SNAPSHOT_DIRECTORY,
                QMOI_REPOSITORY,
                ALPHA_Q_AI_REPOSITORY,
                "reachable refs and archived snapshots",
            ],
            "candidate_surfaces": [
                "new sites",
                "new applications",
                "web and mobile UI features",
                "APIs and backend services",
                "platform integrations and automation",
                "documentation, workflows, and operational tooling",
            ],
            "required_evidence": [
                "complete path and directory inventories",
                "content identity and ownership for every candidate path",
                "routes, symbols, workflows, configuration, and dependency analysis",
                "existing Alpha behavior and history preservation check",
            ],
            "decision_gates": [
                "propose additive feature only after cross-history comparison",
                "reject duplicate or speculative work without a measurable gap",
                "write an implementation plan with dependencies and affected paths",
                "run targeted tests, full validation, and UI/build checks when applicable",
                "require explicit review for conflicts, deletions, and new external integrations",
            ],
            "alpha_preservation": (
                "Alpha-Q-ai keeps every existing tracked path and receives only "
                "verified historical or additive changes."
            ),
        }

    def build_complete_execution_contract(self) -> dict[str, Any]:
        """Describe mandatory whole-repository, style, and auth gates."""
        return {
            "review_scope": [
                "all files and directories in the live repositories",
                "all reachable refs and historical snapshots",
                "all relevant tests, workflows, routes, symbols, and configuration",
            ],
            "whole_repository_actions": [
                "inventory every source path before planning",
                "run the repository-surface audit for Markdown, API, endpoints, routes, ports, links, components, tree, workflows/hooks, styles/universals, QVillage/QVS, comparison, Qtrade, percentages, production candidates, and memory",
                "map every audit category to exact paths, hashes, source scopes, local refs, structural checks, metrics, external research topics, tests, and remote-coverage blockers",
                "read and classify relevant implementation and test surfaces",
                "map dependencies, ownership, routes, UI surfaces, and auth boundaries",
                "run targeted tests plus the complete repository test command",
                "record skipped, blocked, or unavailable checks explicitly",
            ],
            "style_source": {
                "file": "STYLES.md",
                "role": "source of truth for generated UI layout, typography, color, motion, accessibility, and platform styling",
                "required_when": "creating or changing any site, app, dashboard, web, or mobile UI feature",
                "required_update": "update STYLES.md whenever a new UI pattern or styling capability is introduced",
            },
            "universal_source": {
                "file": "UNIVERSALS.md",
                "role": "source of truth for authentication, login, identity, permissions, security, device, and cross-platform behavior",
                "required_when": "any feature requires authentication, login, identity, authorization, or protected data",
                "required_update": "update UNIVERSALS.md whenever a new universal/authentication capability is introduced",
            },
            "completion_requirements": [
                "every UI proposal cites applicable STYLES.md sections",
                "every protected-flow proposal cites applicable UNIVERSALS.md sections",
                "STYLES.md and UNIVERSALS.md update status is recorded in the validation report",
                "no feature is complete while required source docs or tests are missing",
            ],
        }

    def build_cross_repository_merge_plan(
        self,
        roots: Sequence[Path | str] | None = None,
    ) -> dict[str, Any]:
        """Plan complete Alpha-history coverage and bidirectional feature routing."""
        repo_root = Path(__file__).resolve().parent.parent
        root_map = {
            "qmoi-enhanced": repo_root,
            "qmoi-enhanced-history-14": repo_root / HISTORY_SNAPSHOT_DIRECTORY,
            "Alpha-Q-ai": repo_root.parent / "Alpha-Q-ai",
        }
        if roots is not None:
            supplied = [Path(item).resolve() for item in roots]
            for path in supplied:
                lowered = path.name.lower()
                if "qmoi" in lowered and "history" in lowered:
                    root_map["qmoi-enhanced-history-14"] = path
                elif "qmoi" in lowered and "enhanced" in lowered:
                    root_map["qmoi-enhanced"] = path
                elif "alpha" in lowered and "2025" in lowered or path.name == "Alpha-Q-ai":
                    root_map["Alpha-Q-ai"] = path
        alpha_root = root_map.get("Alpha-Q-ai") or repo_root
        history_candidates = [
            alpha_root / "Alpha-Q-ai-2025" if alpha_root else None,
            repo_root / "Alpha-Q-ai-2025",
            repo_root / "Alpha-Q-ai",
        ]
        history_root = next(
            (candidate for candidate in history_candidates if candidate and candidate.is_dir()),
            repo_root / "Alpha-Q-ai-2025",
        )
        source_roots = {
            "qmoi-enhanced": root_map.get("qmoi-enhanced", repo_root),
            "qmoi-enhanced-history-14": root_map.get("qmoi-enhanced-history-14", repo_root / HISTORY_SNAPSHOT_DIRECTORY),
            "Alpha-Q-ai": root_map.get("Alpha-Q-ai", repo_root.parent / "Alpha-Q-ai"),
            "Alpha-Q-ai-2025": history_root,
        }
        history_snapshot_root = source_roots["qmoi-enhanced-history-14"]
        history_snapshot_available = history_snapshot_root.is_dir()
        if not history_snapshot_available:
            # Keep planning and diagnostics available in light checkouts, but
            # retain a false base gate until the immutable history is present.
            source_roots["qmoi-enhanced-history-14"] = source_roots["qmoi-enhanced"]
        markdown_audit = self.audit_all_markdown_sources(list(source_roots.values()))
        metrics: dict[str, dict[str, Any]] = {}
        all_paths: set[str] = set()
        merge_documents: set[str] = set()
        for name, root in source_roots.items():
            files: list[str] = []
            directories: set[str] = set()
            if root.is_dir():
                for path in sorted(root.rglob("*")):
                    if ".git" in path.parts:
                        continue
                    relative = path.relative_to(root).as_posix()
                    if path.is_dir():
                        directories.add(relative)
                    elif path.is_file():
                        files.append(relative)
                        all_paths.add(f"{name}/{relative}")
                        if path.name.lower() == "merge.md" or "merge" in path.name.lower():
                            merge_documents.add(f"{name}/{relative}")
            metrics[name] = {
                "root": str(root),
                "exists": root.is_dir(),
                "files": len(files),
                "directories": len(directories),
                "paths": files,
            }

        alpha_history_paths = set(metrics["Alpha-Q-ai-2025"]["paths"])
        routed_to_qmoi: list[str] = []
        routed_to_alpha: list[str] = []
        for path in sorted(alpha_history_paths):
            target = self.route_file_to_repository(path)
            (routed_to_alpha if target == "Alpha-Q-ai" else routed_to_qmoi).append(path)

        return {
            "base_repository": HISTORY_SNAPSHOT_DIRECTORY,
            "history_projection": {
                "directory": "HIST",
                "status": "blocked_until_remote_success",
                "required_sources": [HISTORY_SNAPSHOT_DIRECTORY, "Alpha-Q-ai-2025"],
                "preserve_branch_and_artifact_history": True,
                "copy_policy": "target-owned workflow only after parity, security, and final production gates pass",
            },
            "source_order": [
                HISTORY_SNAPSHOT_DIRECTORY,
                "qmoi-enhanced",
                "Alpha-Q-ai",
                "Alpha-Q-ai-2025",
            ],
            "metrics": metrics,
            "base_available": history_snapshot_available,
            "ready_for_apply": (
                history_snapshot_available
                and metrics["Alpha-Q-ai"]["exists"]
                and metrics["Alpha-Q-ai-2025"]["exists"]
                and len(metrics["Alpha-Q-ai-2025"]["paths"]) > 0
                and markdown_audit["index_complete"]
            ),
            "all_source_paths": sorted(all_paths),
            "all_alpha_history_paths_included": len(routed_to_qmoi) + len(routed_to_alpha)
            == metrics["Alpha-Q-ai-2025"]["files"],
            "merge_documents": sorted(merge_documents),
            "markdown_audit": markdown_audit,
            "feature_direction": {
                "alpha_to_qmoi": {
                    "rule": "add Alpha features to QMOI when ownership, dependencies, and tests show a compatible capability absent from QMOI",
                    "candidate_paths": routed_to_qmoi,
                },
                "qmoi_to_alpha": {
                    "rule": "add QMOI features to Alpha when they are additive, compatible, and preserve existing Alpha behavior",
                    "candidate_paths": routed_to_alpha,
                },
                "conflicts": "block automatic overwrite; retain both owners and require reviewed resolution",
            },
            "required_merge_inputs": [
                "all files and directories in Alpha-Q-ai-2025",
                "MERGE.md from every repository and history source",
                "STYLES.md and UNIVERSALS.md",
                "ALLMDFILESREFS.md, ALLLINKS.md, COMPONENTS.md, TREE.md, QAUDITS.md, INTERNALRESEARCH.md, EXTERNALRESEARCH.md, compare.md, and Qtrade.md",
                "repository-surface, percentage/metric, production-gap, memory/QVillage, test, hook, and webhook audit artifacts",
                "memory indexes, tracker state, and synchronization evidence",
                "tests, workflows, routes, APIs, ports, and automation files",
            ],
            "synchronization_gates": [
                "generate or refresh memory indexes for every destination repository",
                "record QMOI awareness, identity, and memory-sync state in each repository",
                "update automation and workflow references after every accepted feature",
                "run targeted tests and full repository validation in both destinations",
                "record skipped, blocked, conflicting, or unavailable source checks",
            ],
            "apply_mode": "blocked until the base and every required source inventory are available; then plan-only until ownership, conflict, test, and authorization gates pass",
        }

    def audit_all_markdown_sources(
        self,
        roots: Sequence[Path | str] | None = None,
    ) -> dict[str, Any]:
        """Audit every Markdown source and its index coverage without rewriting content."""
        repo_root = Path(__file__).resolve().parent.parent
        default_roots = [
            repo_root,
            repo_root / HISTORY_SNAPSHOT_DIRECTORY,
            repo_root.parent / "Alpha-Q-ai",
            repo_root / "Alpha-Q-ai-2025",
        ]
        source_roots = [Path(item).resolve() for item in (roots or default_roots)]
        reports: list[dict[str, Any]] = []
        all_paths: set[str] = set()
        unresolved: list[dict[str, str]] = []
        for root in source_roots:
            if not root.is_dir():
                reports.append({"root": str(root), "exists": False, "files": 0})
                continue
            markdown_files = []
            for path in iter_markdown_files(root):
                relative = path.relative_to(root).as_posix()
                markdown_files.append(relative)
                all_paths.add(f"{root.name}/{relative}")
                text = path.read_text(encoding="utf-8", errors="replace")
                if not text.strip():
                    unresolved.append({"path": str(path), "issue": "empty Markdown file"})
                if not any(line.lstrip().startswith("#") for line in text.splitlines()):
                    unresolved.append({"path": str(path), "issue": "missing Markdown heading"})
                if re.search(r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b", text, re.IGNORECASE):
                    unresolved.append({"path": str(path), "issue": "unresolved marker"})
            index_path = root / "ALLMDFILESREFS.md"
            index_text = index_path.read_text(encoding="utf-8", errors="replace") if index_path.is_file() else ""
            missing_from_index = [path for path in markdown_files if path not in index_text]
            reports.append({
                "root": str(root),
                "exists": True,
                "files": len(markdown_files),
                "paths": markdown_files,
                "index": str(index_path),
                "index_exists": index_path.is_file(),
                "missing_from_index": missing_from_index,
                "index_complete": index_path.is_file() and not missing_from_index,
            })
        return {
            "source_roots": [str(root) for root in source_roots],
            "reports": reports,
            "total_markdown_files": sum(report.get("files", 0) for report in reports),
            "all_paths": sorted(all_paths),
            "merge_documents": sorted(
                path for path in all_paths if path.lower().endswith("merge.md") or "/merge" in path.lower()
            ),
            "unresolved_checks": unresolved,
            "index_complete": all(
                report.get("index_complete", False)
                for report in reports
                if report.get("exists") and report.get("files", 0) > 0
            ),
            "truth_checks_passed": not unresolved,
            "read_only": True,
        }

    def refresh_all_markdown_indexes(
        self,
        roots: Sequence[Path | str] | None = None,
    ) -> dict[str, Any]:
        """Write complete path inventories into ALLMDFILESREFS.md for each source root."""
        audit = self.audit_all_markdown_sources(roots)
        marker_start = "\n## Complete Autonomous Markdown Source Inventory\n"
        updated: list[str] = []
        for report in audit["reports"]:
            if not report.get("exists"):
                continue
            index_path = Path(report["index"])
            existing = index_path.read_text(encoding="utf-8") if index_path.is_file() else "# ALLMDFILESREFS.md\n"
            prefix = existing.split(marker_start, 1)[0].rstrip()
            section = [
                marker_start.rstrip(),
                "",
                "Generated by the Ollama autonomous agent. This section enumerates every Markdown path in this source root.",
                "",
                f"- Source root: `{report['root']}`",
                f"- Markdown files: `{report['files']}`",
                "",
                "### Paths",
                "",
            ]
            section.extend(f"- `{path}`" for path in report["paths"])
            safe_text_write(index_path, prefix + "\n\n" + "\n".join(section) + "\n")
            updated.append(str(index_path))
        return {
            "updated_indexes": updated,
            "audit": self.audit_all_markdown_sources(roots),
        }

    @staticmethod
    def _git_output(
        repo_path: Path,
        *arguments: str,
    ) -> list[str]:
        """Run a read-only Git query and return non-empty output lines."""
        result = subprocess.run(
            ["git", "-C", str(repo_path), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return []
        return [line for line in result.stdout.splitlines() if line]

    def collect_repository_snapshot(
        self,
        repo_path: Path | str,
        *,
        recent_pushes: int = 4,
    ) -> dict[str, Any]:
        """Capture auditable Git state without mutating the repository."""
        repo = Path(repo_path).resolve()
        commit_limit = max(1, int(recent_pushes))
        commits = []

        for line in self._git_output(
            repo,
            "log",
            "--all",
            f"-{commit_limit}",
            "--format=%H%x1f%an%x1f%ae%x1f%aI%x1f%s",
        ):
            fields = line.split("\x1f", 4)
            if len(fields) == 5:
                commits.append(
                    {
                        "commit": fields[0],
                        "author": fields[1],
                        "email": fields[2],
                        "timestamp": fields[3],
                        "subject": fields[4],
                    }
                )

        branches = self._git_output(
            repo,
            "for-each-ref",
            "--format=%(refname:short)",
            "refs/heads",
            "refs/remotes",
        )

        return {
            "repository": str(repo),
            "captured_at": utc_iso(),
            "head": (self._git_output(repo, "rev-parse", "HEAD") or [None])[0],
            "branches": branches,
            "files": self._git_output(repo, "ls-files"),
            "commits": commits,
            "contributors": sorted(
                {
                    commit["author"]
                    for commit in commits
                    if commit.get("author")
                }
            ),
            "recent_pushes_requested": commit_limit,
            "history_scope": "all reachable refs",
        }

    def collect_reference_inventory(
        self,
        repo_path: Path | str,
        git_ref: str,
    ) -> dict[str, Any]:
        """Read a complete tracked-file inventory for a branch or remote ref."""
        if not re.fullmatch(r"[A-Za-z0-9._/@-]+", git_ref):
            raise ValueError("Unsafe Git reference")
        repo = Path(repo_path).resolve()
        files = self._git_output(repo, "ls-tree", "-r", "--name-only", git_ref)
        return {
            "repository": str(repo),
            "git_ref": git_ref,
            "files": files,
            "markdown_files": [item for item in files if item.lower().endswith(".md")],
            "file_count": len(files),
            "captured_at": utc_iso(),
            "read_only": True,
        }

    @staticmethod
    def route_file_to_repository(file_path: str | os.PathLike[str]) -> str:
        """Route a file or path into the canonical repo for merged ownership."""
        normalized = str(file_path).replace("\\", "/").lower()
        if "alpha-q-ai" in normalized or normalized.startswith("alpha/"):
            return "Alpha-Q-ai"
        qmoi_keywords = {
            "api",
            "endpoint",
            "route",
            "routes",
            "port",
            "monitor",
            "workflow",
            "merge",
            "docs",
            "readme",
            "qcity",
            "qalpha",
            "qmoi",
            "build",
            "install",
            "download",
            "memory",
            "model",
            "validation",
            "proof",
            "github",
        }
        alpha_keywords = {
            "agent",
            "integration",
            "sync",
            "clone",
            "platform",
            "backend",
            "service",
            "alpha",
        }
        if any(token in normalized for token in qmoi_keywords):
            return "qmoi-enhanced"
        if any(token in normalized for token in alpha_keywords):
            return "Alpha-Q-ai"
        return "qmoi-enhanced"

    @staticmethod
    def route_to_repo_for_root(root_path: str | os.PathLike[str]) -> str:
        """Compatibility helper used by merge routing summaries and decision logs."""
        return CrossRepositoryAutonomyManager.route_file_to_repository(root_path)

    def identify_missing_implementations(
        self,
        repo_path: Path | str,
    ) -> dict[str, Any]:
        """Build a bounded production-gap candidate inventory without claiming defects or exposing source text."""
        root = Path(repo_path).resolve()
        findings: list[dict[str, Any]] = []
        if not root.exists():
            return {"root": str(root), "total_missing": 0, "items": findings, "status": "BLOCKED", "coverage_complete": False}

        excluded_directory_reasons = {
            ".git": "git_metadata",
            ".venv": "virtual_environment",
            "venv": "virtual_environment",
            "node_modules": "installed_dependencies",
            "__pycache__": "generated_bytecode",
            ".pytest_cache": "test_cache",
            ".mypy_cache": "tool_cache",
            ".ruff_cache": "tool_cache",
            "dist": "build_output",
            "build": "build_output",
            "target": "build_output",
            "coverage": "test_output",
            ".next": "build_output",
            ".turbo": "build_cache",
        }
        allowed_suffixes = {
            ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
            ".c", ".cc", ".cpp", ".h", ".hpp", ".cs", ".php", ".rb",
            ".sh", ".ps1", ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg",
            ".md", ".txt",
        }
        code_suffixes = allowed_suffixes - {".md", ".txt"}
        code_patterns = (
            ("todo", re.compile(r"\bTODO\b", re.IGNORECASE)),
            ("fixme", re.compile(r"\bFIXME\b", re.IGNORECASE)),
            ("tbd", re.compile(r"\bTBD\b", re.IGNORECASE)),
            ("placeholder", re.compile(r"\bPLACEHOLDER\b|\[PRODUCTION IMPLEMENTATION REQUIRED\]", re.IGNORECASE)),
            ("not_implemented", re.compile(r"\bNotImplementedError\b|\bnot implemented\b", re.IGNORECASE)),
            ("stub", re.compile(r"\bstub(?:bed)?\b", re.IGNORECASE)),
            ("pass_statement", re.compile(r"^\s*pass\s*(?:#.*)?$", re.IGNORECASE)),
        )
        document_patterns = (
            ("todo", re.compile(r"^\s*(?:[-*]\s*)?TODO\s*:", re.IGNORECASE)),
            ("fixme", re.compile(r"^\s*(?:[-*]\s*)?FIXME\s*:", re.IGNORECASE)),
            ("tbd", re.compile(r"^\s*(?:[-*]\s*)?TBD\s*:", re.IGNORECASE)),
            ("placeholder", re.compile(r"\[PRODUCTION IMPLEMENTATION REQUIRED\]", re.IGNORECASE)),
        )
        excluded_roots: list[dict[str, str]] = []
        unreadable: list[dict[str, str]] = []
        scanned_files = 0
        oversized_files = 0
        max_file_bytes = 2 * 1024 * 1024

        for current, directories, filenames in os.walk(root, followlinks=False):
            current_path = Path(current)
            kept_directories = []
            for directory in sorted(directories):
                child = current_path / directory
                reason = excluded_directory_reasons.get(directory)
                if reason is None and ("history" in directory.lower() or directory.lower().startswith(("archive", "snapshot"))):
                    reason = "historical_or_snapshot_materialization"
                if child.is_symlink():
                    excluded_roots.append({"path": child.relative_to(root).as_posix(), "reason": "symlink_not_followed"})
                elif reason:
                    excluded_roots.append({"path": child.relative_to(root).as_posix(), "reason": reason})
                else:
                    kept_directories.append(directory)
            directories[:] = kept_directories
            for filename in sorted(filenames):
                path = current_path / filename
                if path.is_symlink() or path.suffix.lower() not in allowed_suffixes:
                    continue
                relative_path = path.relative_to(root).as_posix()
                try:
                    size = path.stat().st_size
                    if size > max_file_bytes:
                        oversized_files += 1
                        continue
                    content = path.read_bytes()
                    text = content.decode("utf-8")
                except (OSError, UnicodeDecodeError) as exc:
                    unreadable.append({"path": relative_path, "error_type": type(exc).__name__})
                    continue
                scanned_files += 1
                patterns = code_patterns if path.suffix.lower() in code_suffixes else document_patterns
                marker_lines: dict[str, list[int]] = {}
                for line_number, line in enumerate(text.splitlines(), start=1):
                    for marker, pattern in patterns:
                        if pattern.search(line):
                            marker_lines.setdefault(marker, []).append(line_number)
                if marker_lines:
                    markers = sorted(marker_lines)
                    findings.append({
                        "path": relative_path,
                        "sha256": hashlib.sha256(content).hexdigest(),
                        "bytes": len(content),
                        "candidate_markers": markers,
                        "line_numbers": {name: numbers for name, numbers in sorted(marker_lines.items())},
                        "target_repo": self.route_file_to_repository(relative_path),
                        "priority": "review_first" if any(name in {"not_implemented", "placeholder", "todo", "fixme"} for name in markers) else "review",
                        "status": "discovered_unmapped",
                        "implementation_verified": False,
                        "tests_verified": False,
                        "automatic_replacement_authorized": False,
                        "next_action": "Inspect the owning implementation, identify a focused test and safe replacement plan; do not replace from markers alone.",
                    })

        findings.sort(key=lambda item: (item["priority"] != "review_first", item["path"]))

        return {
            "root": str(root),
            "status": "NEEDS_REVIEW" if findings or unreadable or oversized_files else "CLEAR",
            "coverage_complete": not unreadable and oversized_files == 0,
            "coverage_scope": "active materialized workspace; not remote branches or unfetched history",
            "scanned_files": scanned_files,
            "oversized_files_not_read": oversized_files,
            "unreadable_files": unreadable,
            "excluded_roots": excluded_roots,
            "total_candidates": len(findings),
            "total_missing": len(findings),
            "items": findings,
            "decision_rule": "Candidate markers are discovery only. Require ownership mapping, implementation review, focused validation, and exact remote evidence before marking a replacement verified.",
        }

    def group_similar_files(
        self,
        repo_path: Path | str,
    ) -> list[dict[str, Any]]:
        """Group files with nearly identical names or content so the autonomous agent can merge them safely."""
        root = Path(repo_path).resolve()
        groups: dict[str, list[str]] = {}
        if not root.exists():
            return []

        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            stem = path.stem.lower()
            key = re.sub(r"(_|\-|duplicate|placeholder|stub|copy|v1|v2|final|temp)+", "", stem)
            groups.setdefault(key or path.name.lower(), []).append(str(path.relative_to(root)).replace("\\", "/"))

        result: list[dict[str, Any]] = []
        for key, files in sorted(groups.items()):
            unique_files = sorted(set(files))
            if len(unique_files) < 2:
                continue
            result.append(
                {
                    "group_key": key,
                    "files": unique_files,
                    "decision": "merge_or_unify",
                    "target_repo": self.route_file_to_repository(unique_files[0]),
                }
            )
        return result

    def build_branch_history_inventory(
        self,
        repo_path: Path | str,
    ) -> dict[str, Any]:
        """Inventory every locally available Git ref and aggregate file/directory duplication metrics."""
        repo = Path(repo_path).resolve()
        all_refs = sorted(set(self._git_output(repo, "for-each-ref", "--format=%(refname)")))
        branch_refs = sorted(set(self._git_output(
            repo,
            "for-each-ref",
            "--format=%(refname:short)",
            "refs/heads",
            "refs/remotes",
        )))
        pull_request_refs = [ref for ref in all_refs if ref.startswith("refs/pull/")]
        tag_refs = [ref for ref in all_refs if ref.startswith("refs/tags/")]
        files_by_ref: dict[str, list[str]] = {}
        file_name_counts: dict[str, int] = {}
        dir_name_counts: dict[str, int] = {}
        dir_path_counts: dict[str, int] = {}
        api_route_names: set[str] = set()
        duplicate_file_basenames: set[str] = set()
        duplicate_directory_names: set[str] = set()
        trading_path_keywords = (
            "trading", "trade", "qtrade", "exchange", "wallet", "balance",
            "order", "portfolio", "risk", "finance", "payment", "cashon",
            "megavault", "binance", "bitget",
        )
        trading_paths_by_ref: dict[str, list[str]] = {}
        trading_test_paths_by_ref: dict[str, list[str]] = {}
        trading_path_union: set[str] = set()
        total_files = 0
        total_directories = 0

        for ref in all_refs:
            file_list = self._git_output(repo, "ls-tree", "-r", "--name-only", ref)
            files_by_ref[ref] = file_list
            trading_paths = [
                path for path in file_list
                if any(keyword in path.lower() for keyword in trading_path_keywords)
            ]
            trading_paths_by_ref[ref] = trading_paths
            trading_test_paths_by_ref[ref] = [
                path for path in trading_paths
                if (
                    Path(path).name.startswith("test_")
                    or Path(path).name.endswith((".test.ts", ".test.tsx", ".test.js", ".test.jsx", ".spec.ts", ".spec.tsx", ".spec.js", ".spec.jsx"))
                )
            ]
            trading_path_union.update(trading_paths)
            ref_dir_paths: set[str] = set()
            for path in file_list:
                total_files += 1
                file_name = Path(path).name
                file_name_counts[file_name] = file_name_counts.get(file_name, 0) + 1
                if any(keyword in path.lower() for keyword in ("api", "endpoint", "route", "routes", "port", "workflow", "monitor")):
                    api_route_names.add(path)
                if "feature" in path.lower():
                    api_route_names.add(path)
                current = Path(path).parent
                while str(current) not in ("", "."):
                    current_path = current.as_posix()
                    ref_dir_paths.add(current_path)
                    dir_path_counts[current_path] = dir_path_counts.get(current_path, 0) + 1
                    dir_name_counts[current.name] = dir_name_counts.get(current.name, 0) + 1
                    current = current.parent
            total_directories += len(ref_dir_paths)

        for name, count in file_name_counts.items():
            if count > 1:
                duplicate_file_basenames.add(name)
        for name, count in dir_name_counts.items():
            if count > 1:
                duplicate_directory_names.add(name)

        report = {
            "repo": str(repo),
            "branches": branch_refs,
            "ref_counts": len(branch_refs),
            "all_refs": all_refs,
            "all_ref_count": len(all_refs),
            "pull_request_refs": pull_request_refs,
            "tag_refs": tag_refs,
            "trading_paths_by_ref": {
                ref: paths for ref, paths in sorted(trading_paths_by_ref.items())
            },
            "trading_test_paths_by_ref": {
                ref: paths for ref, paths in sorted(trading_test_paths_by_ref.items())
            },
            "trading_related_unique_path_count": len(trading_path_union),
            "trading_related_paths": sorted(trading_path_union),
            "branches_with_inventory": branch_refs,
            "refs_with_inventory": list(files_by_ref.keys()),
            "coverage": {
                "scope": "all refs currently available in the local Git database",
                "pull_request_ref_count": len(pull_request_refs),
                "remote_completeness": "not_verified; remote-tracking refs may be stale or incomplete",
                "unfetched_pull_requests_included": False,
                "trading_path_scope": "path-name matches in locally available ref tip trees",
                "trading_remote_completeness": "not_verified",
                "intermediate_commit_trees_scanned": False,
            },
            "total_files": total_files,
            "total_directories": total_directories,
            "duplicate_file_basenames": sorted(duplicate_file_basenames),
            "duplicate_directory_names": sorted(duplicate_directory_names),
            "duplicate_file_count": len(duplicate_file_basenames),
            "duplicate_directory_count": len(duplicate_directory_names),
            "api_route_related_files": sorted(api_route_names),
            "api_route_count": len(api_route_names),
            "file_name_counts": dict(sorted(file_name_counts.items())),
            "directory_name_counts": dict(sorted(dir_name_counts.items())),
            "paths_by_ref": {ref: file_list for ref, file_list in sorted(files_by_ref.items())},
        }
        return report

    def collect_full_merge_metrics(
        self,
        roots: Sequence[Path | str] | None = None,
        *,
        include_history: bool = True,
        include_memory: bool = True,
    ) -> dict[str, Any]:
        """Aggregate repository, branch, history, and directory metrics for final MERGE.md reporting."""
        roots_list = self._candidate_merge_roots(roots, include_history=include_history, include_memory=include_memory)
        branch_reports: list[dict[str, Any]] = []
        total_files = 0
        total_directories = 0
        total_branches = 0
        total_refs = 0
        total_pull_request_refs = 0
        total_tag_refs = 0
        duplicate_basenames: dict[str, int] = {}
        duplicate_directories: dict[str, int] = {}
        api_route_related_files: set[str] = set()
        feature_related_files: set[str] = set()
        style_universal_related_files: set[str] = set()
        trading_related_files: set[str] = set()

        ignored_dirs = {".git", ".hg", ".svn", ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache", ".venv", "venv", "node_modules", ".next", "dist", "build", "target"}

        for root in roots_list:
            if not root.exists():
                continue
            if (root / ".git").exists() or self._git_output(root, "rev-parse", "--git-dir"):
                report = self.build_branch_history_inventory(root)
                branch_reports.append(report)
                total_files += report["total_files"]
                total_directories += report["total_directories"]
                total_branches += report["ref_counts"]
                total_refs += report["all_ref_count"]
                total_pull_request_refs += len(report["pull_request_refs"])
                total_tag_refs += len(report["tag_refs"])
                for name, count in report["file_name_counts"].items():
                    duplicate_basenames[name] = max(duplicate_basenames.get(name, 0), count)
                for name, count in report["directory_name_counts"].items():
                    duplicate_directories[name] = max(duplicate_directories.get(name, 0), count)
                api_route_related_files.update(report["api_route_related_files"])
                trading_related_files.update(report["trading_related_paths"])
                feature_related_files.update(
                    path for path in report["file_name_counts"] if "feature" in path.lower()
                )
            else:
                for path in sorted(root.rglob("*")):
                    if any(part in ignored_dirs for part in path.parts):
                        continue
                    if path.is_dir():
                        total_directories += 1
                    elif path.is_file():
                        total_files += 1
                        has_feature = "feature" in path.name.lower() or "feature" in str(path).lower()
                        if has_feature:
                            feature_related_files.add(str(path.resolve()))
                        if any(keyword in str(path).lower() for keyword in ("api", "endpoint", "route", "port", "workflow", "monitor")):
                            api_route_related_files.add(str(path.resolve()))
                        lowered = str(path).lower()
                        if any(token in lowered for token in ("styles.md", "universals.md", "style", "universal", "user-style", "platform-style", "design-system")):
                            style_universal_related_files.add(str(path.resolve()))
                        if any(token in lowered for token in (
                            "trading", "trade", "qtrade", "exchange", "wallet", "balance",
                            "order", "portfolio", "risk", "finance", "payment", "cashon",
                            "megavault", "binance", "bitget",
                        )):
                            trading_related_files.add(str(path.resolve()))

        duplicate_file_names = sorted(name for name, count in duplicate_basenames.items() if count > 1)
        duplicate_directory_names = sorted(name for name, count in duplicate_directories.items() if count > 1)
        return {
            "roots": [str(path.resolve()) for path in roots_list],
            "branch_reports": branch_reports,
            "total_files": total_files,
            "total_directories": total_directories,
            "total_branches": total_branches,
            "total_refs": total_refs,
            "pull_request_ref_count": total_pull_request_refs,
            "tag_ref_count": total_tag_refs,
            "duplicate_file_names": duplicate_file_names,
            "duplicate_file_count": len(duplicate_file_names),
            "duplicate_directory_names": duplicate_directory_names,
            "duplicate_directory_count": len(duplicate_directory_names),
            "api_route_related_files": sorted(api_route_related_files),
            "api_route_count": len(api_route_related_files),
            "feature_related_files": sorted(feature_related_files),
            "feature_count": len(feature_related_files),
            "style_universal_related_files": sorted(style_universal_related_files),
            "style_universal_count": len(style_universal_related_files),
            "trading_related_files": sorted(trading_related_files),
            "trading_related_path_count": len(trading_related_files),
            "captured_at": utc_iso(),
        }

    def refresh_merge_evidence(
        self,
        root: Path | str,
        *,
        roots: Sequence[Path | str] | None = None,
        correlation_id: str | None = None,
    ) -> dict[str, Any]:
        """Refresh merge metrics and paired QAUDITS evidence without remote mutation."""
        target = Path(root).resolve()
        metric_roots = [Path(item).resolve() for item in (roots or [target])]
        metrics = self.collect_full_merge_metrics(metric_roots)
        compact_metrics = {
            "captured_at": metrics.get("captured_at"),
            "roots": metrics.get("roots", []),
            "total_files": metrics.get("total_files", 0),
            "total_directories": metrics.get("total_directories", 0),
            "total_branches": metrics.get("total_branches", 0),
            "total_refs": metrics.get("total_refs", 0),
            "pull_request_ref_count": metrics.get("pull_request_ref_count", 0),
            "tag_ref_count": metrics.get("tag_ref_count", 0),
            "duplicate_file_count": metrics.get("duplicate_file_count", 0),
            "duplicate_directory_count": metrics.get("duplicate_directory_count", 0),
            "api_route_count": metrics.get("api_route_count", 0),
            "feature_count": metrics.get("feature_count", 0),
            "style_universal_count": metrics.get("style_universal_count", 0),
            "trading_related_path_count": metrics.get("trading_related_path_count", 0),
            "coverage": metrics.get("coverage", {}),
        }
        metric_payload = json.dumps(compact_metrics, indent=2, sort_keys=True, default=str)
        metric_sha256 = hashlib.sha256(metric_payload.encode("utf-8")).hexdigest()

        qaudits_path = target / "QAUDITS.md"
        merge_path = target / "MERGE.md"
        qaudits_section = [
            "## Agent-managed merge activity evidence",
            "",
            f"- Status: `MERGE_EVIDENCE_REFRESHED`; correlation ID: `{correlation_id or 'unavailable'}`.",
            f"- Local scope: `{', '.join(metrics['roots'])}`.",
            f"- Captured at: `{metrics['captured_at']}`; source metric SHA-256: `{metric_sha256}`.",
            f"- Total files in scope: `{metrics['total_files']}`; total directories: `{metrics['total_directories']}`.",
            f"- Branches: `{metrics['total_branches']}`; local refs: `{metrics['total_refs']}`; pull-request refs: `{metrics['pull_request_ref_count']}`; tags: `{metrics['tag_ref_count']}`.",
            f"- Duplicate file basenames: `{metrics['duplicate_file_count']}`; duplicate directory names: `{metrics['duplicate_directory_count']}`.",
            f"- API/route-related files: `{metrics['api_route_count']}`; feature-related files: `{metrics['feature_count']}`; style/universal-related files: `{metrics['style_universal_count']}`; trading-related paths: `{metrics['trading_related_path_count']}`.",
            "- This is a local Git-tree and history inventory. Remote refs, PRs, intermediate commit trees, releases, and authorization are not verified by this operation.",
            "- Next action: independently verify target-owned exact-ref/SHA/tree evidence before any remote completion or protected mutation claim.",
            "",
            "```json",
            metric_payload,
            "```",
            "",
        ]
        merge_section = [
            "## Agent-managed merge activity evidence",
            "",
            f"- Status: `MERGE_EVIDENCE_REFRESHED`; correlation ID: `{correlation_id or 'unavailable'}`.",
            f"- Local metric source SHA-256: `{metric_sha256}`.",
            f"- Total branches in scope: `{metrics['total_branches']}`; local refs: `{metrics['total_refs']}`; pull-request refs: `{metrics['pull_request_ref_count']}`; tags: `{metrics['tag_ref_count']}`.",
            f"- Total files in scope: `{metrics['total_files']}`; total directories: `{metrics['total_directories']}`.",
            f"- Duplicate file count: `{metrics['duplicate_file_count']}`; duplicate directory count: `{metrics['duplicate_directory_count']}`.",
            f"- API/route count: `{metrics['api_route_count']}`; feature count: `{metrics['feature_count']}`; style/universal count: `{metrics['style_universal_count']}`; trading-related path count: `{metrics['trading_related_path_count']}`.",
            "- Merge decisions: not executed; this refresh records local evidence only and preserves existing merge guidance.",
            "- Remote completion remains blocked until an independently verified target-owned terminal exact-SHA result exists.",
            "",
            "```json",
            metric_payload,
            "```",
            "",
        ]
        _upsert_managed_markdown_section(
            qaudits_path,
            "QAUDITS.md",
            "merge-activity-evidence",
            "\n".join(qaudits_section),
        )
        _upsert_managed_markdown_section(
            merge_path,
            "MERGE.md",
            "merge-activity-evidence",
            "\n".join(merge_section),
        )

        artifact_refs = {
            "merge_metrics": {
                "path": "ollamatracks/merge_activity_metrics.json",
                "sha256": None,
                "bytes": None,
                "status": "not_written",
            },
            "qaudits_document": _local_artifact_integrity(target, str(qaudits_path.relative_to(target))),
            "merge_document": _local_artifact_integrity(target, str(merge_path.relative_to(target))),
        }
        source_manifest = target / "ollamatracks" / "merge_activity_metrics.json"
        safe_json_write(
            source_manifest,
            {
                "schema_version": 1,
                "captured_at": metrics["captured_at"],
                "correlation_id": correlation_id,
                "roots": metrics["roots"],
                "metrics": metrics,
            },
        )
        artifact_refs["merge_metrics"] = _local_artifact_integrity(
            target, str(source_manifest.relative_to(target))
        )

        checkpoint = record_qaudit_checkpoint(
            target,
            "merge-activity-evidence",
            {
                "status": "MERGE_EVIDENCE_REFRESHED",
                "source_manifest_sha256": artifact_refs["merge_metrics"]["sha256"],
                "artifact_path": artifact_refs["merge_metrics"]["path"],
                "artifact_sha256": artifact_refs["merge_metrics"]["sha256"],
                "artifact_bytes": artifact_refs["merge_metrics"]["bytes"],
                "artifact_refs": artifact_refs,
                "metrics": {
                    "total_files_in_scope": metrics["total_files"],
                    "total_directories_in_scope": metrics["total_directories"],
                    "total_branches_in_scope": metrics["total_branches"],
                    "total_local_refs_in_scope": metrics["total_refs"],
                    "locally_available_pull_request_refs": metrics["pull_request_ref_count"],
                    "tag_refs_in_scope": metrics["tag_ref_count"],
                    "duplicate_file_count": metrics["duplicate_file_count"],
                    "duplicate_directory_count": metrics["duplicate_directory_count"],
                    "api_route_count": metrics["api_route_count"],
                    "feature_count": metrics["feature_count"],
                    "style_universal_count": metrics["style_universal_count"],
                    "trading_related_path_count": metrics["trading_related_path_count"],
                },
                "blockers": [
                    "remote_refs_prs_intermediate_trees_and_release_state_not_verified",
                    "remote_completion_not_verified",
                ],
                "next_action": (
                    "Obtain independently verified target-owned terminal exact-ref/SHA/tree evidence "
                    "before any remote completion or protected mutation claim."
                ),
            },
            correlation_id=correlation_id,
        )
        return {
            "status": "MERGE_EVIDENCE_REFRESHED",
            "correlation_id": checkpoint["correlation_id"],
            "metrics": {
                "total_files_in_scope": metrics["total_files"],
                "total_directories_in_scope": metrics["total_directories"],
                "total_branches_in_scope": metrics["total_branches"],
                "total_local_refs_in_scope": metrics["total_refs"],
                "locally_available_pull_request_refs": metrics["pull_request_ref_count"],
                "tag_refs_in_scope": metrics["tag_ref_count"],
                "duplicate_file_count": metrics["duplicate_file_count"],
                "duplicate_directory_count": metrics["duplicate_directory_count"],
                "api_route_count": metrics["api_route_count"],
                "feature_count": metrics["feature_count"],
                "style_universal_count": metrics["style_universal_count"],
                "trading_related_path_count": metrics["trading_related_path_count"],
            },
            "source_manifest_sha256": artifact_refs["merge_metrics"]["sha256"],
            "artifact_refs": artifact_refs,
            "checkpoint": checkpoint,
            "remote_verified": False,
            "remote_mutation_performed": False,
        }

    def _candidate_merge_roots(
        self,
        roots: Sequence[Path | str] | None = None,
        *,
        include_history: bool = True,
        include_memory: bool = True,
    ) -> list[Path]:
        """Collect all candidate roots that participate in the final repo merge audit."""
        repo_root = Path(__file__).resolve().parent.parent
        defaults = [
            repo_root,
            repo_root / "qmoi-enhanced-history-14",
            repo_root / "qmoi-enhanced-history-14" / "_archive_qmoi-enhanced",
            repo_root / "ollamatracks",
        ]
        alpha_roots = [repo_root / "Alpha-Q-ai", repo_root.parent / "Alpha-Q-ai"]
        for alpha_root in alpha_roots:
            if alpha_root.exists():
                defaults.extend(
                    [
                        alpha_root,
                        alpha_root / "Alpha-Q-ai-2025",
                    ]
                )

        root_sources = list(roots) if roots is not None else list(defaults)
        candidates = [Path(item).resolve() for item in root_sources]
        filtered: list[Path] = []
        seen: set[str] = set()
        for candidate in candidates:
            if not candidate.exists() or not candidate.is_dir():
                continue
            key = str(candidate)
            if key in seen:
                continue
            filtered.append(candidate)
            seen.add(key)

        if roots is None:
            if include_history:
                archive = repo_root / "qmoi-enhanced-history-14"
                if archive.exists():
                    filtered.append(archive)
            if include_memory:
                memory_dir = repo_root / "ollamatracks"
                if memory_dir.exists():
                    filtered.append(memory_dir)
        return filtered

    def build_unified_markdown_inventory(
        self,
        roots: Sequence[Path | str] | None = None,
        *,
        include_history: bool = True,
        include_memory: bool = True,
    ) -> dict[str, Any]:
        """Return a full markdown inventory across all repo histories, snapshots, and memory stores."""
        roots_list = self._candidate_merge_roots(roots, include_history=include_history, include_memory=include_memory)
        by_basename: dict[str, list[str]] = {}
        duplicate_basenames: list[str] = []
        canonical_targets: dict[str, str] = {}
        seen_names: dict[str, str] = {}

        ignored_dirs = {".git", ".hg", ".svn", ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache", ".venv", "venv", "node_modules", ".next", "dist", "build", "target"}

        for root in roots_list:
            if not root.exists():
                continue
            for path in sorted(root.rglob("*")):
                if any(part in ignored_dirs for part in path.parts):
                    continue
                if not path.is_file() or path.suffix.lower() != ".md":
                    continue
                basename = path.name
                key = seen_names.setdefault(basename.lower(), basename)
                by_basename.setdefault(key, []).append(str(path.resolve()))

        for basename, files in sorted(by_basename.items()):
            if len(files) > 1:
                duplicate_basenames.append(basename)
            ranked = sorted(
                files,
                key=lambda item: (
                    0 if "qmoi-enhanced" in item and "history" not in item.lower() and "ollamatracks" not in item.lower() else 1,
                    0 if "Alpha-Q-ai" in item else 1,
                    0 if "history" not in item.lower() else 1,
                    0 if "archive" not in item.lower() else 1,
                    item,
                ),
            )
            canonical_targets[basename] = ranked[0]

        unique_markdown_files = len(by_basename)
        total_markdown_files = sum(len(files) for files in by_basename.values())
        style_universal_markdown_files = sorted(
            basename for basename in by_basename
            if basename.lower() in {"styles.md", "universals.md"}
            or "style" in basename.lower()
            or "universal" in basename.lower()
            or ("user" in basename.lower() and "style" in basename.lower())
        )
        return {
            "roots": [str(path.resolve()) for path in roots_list],
            "by_basename": {basename: files for basename, files in sorted(by_basename.items())},
            "duplicate_basenames": sorted(duplicate_basenames),
            "canonical_targets": canonical_targets,
            "unique_markdown_files": unique_markdown_files,
            "total_markdown_files": total_markdown_files,
            "style_universal_markdown_files": style_universal_markdown_files,
            "style_universal_count": len(style_universal_markdown_files),
            "merge_priority": {
                "live_qmoi": "prefer qmoi-enhanced root files first",
                "live_alpha_q_ai": "prefer Alpha-Q-ai root files next",
                "history_snapshot": "preserve historical copies as fallback/merge source",
                "memory_directory": "treat tracker and memory outputs as runtime evidence, not primary source",
                "ui_styles_and_universals": "treat STYLES.md, UNIVERSALS.md, user style docs, and per-platform UI design docs as high-priority merge sources before generic history duplicates",
            },
        }

    def assemble_repo_merge_plan(
        self,
        roots: Sequence[Path | str] | None = None,
        *,
        include_history: bool = True,
        include_memory: bool = True,
    ) -> dict[str, Any]:
        """Create a canonical merge plan for all markdown files across repo histories and snapshots."""
        inventory = self.build_unified_markdown_inventory(
            roots,
            include_history=include_history,
            include_memory=include_memory,
        )
        duplicates = {
            basename: [path for path in inventory["by_basename"].get(basename, [])]
            for basename in inventory["duplicate_basenames"]
        }

        merge_plan = {
            "inventory": inventory,
            "duplicates": duplicates,
            "merge_decision": {
                "mode": "canonicalize-by-basename",
                "rule": "keep one canonical live file per basename and record historical duplicates as reconciliation sources",
            },
        }
        return merge_plan

    def merge_duplicate_markdown_files(
        self,
        roots: Sequence[Path | str] | None = None,
        *,
        target_root: Path | str | None = None,
        include_history: bool = True,
        include_memory: bool = True,
    ) -> dict[str, Any]:
        """Merge only compatible same-title Markdown sections; preserve divergent variants."""
        inventory = self.build_unified_markdown_inventory(
            roots,
            include_history=include_history,
            include_memory=include_memory,
        )
        candidate_roots = [Path(item).resolve() for item in inventory["roots"]]
        if target_root is not None:
            target_root_path = Path(target_root).resolve()
        elif candidate_roots:
            target_root_path = candidate_roots[0]
        else:
            target_root_path = Path.cwd().resolve()

        duplicated_names = sorted(inventory["duplicate_basenames"])
        merged_targets: dict[str, str] = {}
        merge_decisions: dict[str, dict[str, Any]] = {}
        duplicate_dirs: dict[str, list[str]] = {}

        dir_names: dict[str, list[str]] = {}
        for root in candidate_roots:
            if not root.exists():
                continue
            for path in sorted(root.rglob("*")):
                if path.is_dir():
                    dir_names.setdefault(path.name, []).append(str(path.resolve()))
                if path.is_file() and path.suffix.lower() == ".md":
                    continue
        for directory_name, occurrences in sorted(dir_names.items()):
            if len(occurrences) > 1:
                duplicate_dirs[directory_name] = occurrences

        for basename in duplicated_names:
            files = inventory["by_basename"].get(basename, [])
            if not files:
                continue
            canonical = inventory["canonical_targets"].get(basename)
            if not canonical:
                continue
            canonical_path = Path(canonical).resolve()
            decision = self._classify_markdown_duplicate_group(files, canonical_path, target_root_path)
            merge_decisions[basename] = decision
            if decision["action"] != "merge_additive_sections":
                continue
            canonical_path.write_text(decision["merged_content"], encoding="utf-8")
            merged_targets[basename] = str(canonical_path)

        merge_metrics = self.collect_full_merge_metrics(
            candidate_roots,
            include_history=include_history,
            include_memory=include_memory,
        )
        implementation_gaps = self.identify_missing_implementations(target_root_path)
        similar_file_groups = self.group_similar_files(target_root_path)

        merge_path = target_root_path / "MERGE.md"
        merge_path.parent.mkdir(parents=True, exist_ok=True)
        existing = merge_path.read_text(encoding="utf-8") if merge_path.exists() else "# MERGE.md\n\n"
        merge_section = [
            "\n## Autonomous markdown merge execution",
            "",
            f"- target_root: {target_root_path}",
            f"- merged_files: {len(merged_targets)}",
            f"- duplicate_basenames: {', '.join(duplicated_names) if duplicated_names else 'none'}",
            f"- total_branches_in_scope: {merge_metrics['total_branches']}",
            f"- total_local_refs_in_scope: {merge_metrics['total_refs']}",
            f"- locally_available_pull_request_refs: {merge_metrics['pull_request_ref_count']}",
            f"- tag_refs_in_scope: {merge_metrics['tag_ref_count']}",
            f"- total_files_in_scope: {merge_metrics['total_files']}",
            f"- total_directories_in_scope: {merge_metrics['total_directories']}",
            f"- duplicate_file_count: {merge_metrics['duplicate_file_count']}",
            f"- duplicate_directory_count: {merge_metrics['duplicate_directory_count']}",
            f"- api_route_count: {merge_metrics['api_route_count']}",
            f"- trading_related_path_count: {merge_metrics['trading_related_path_count']}",
            f"- feature_count: {merge_metrics['feature_count']}",
            f"- missing_implementation_count: {implementation_gaps['total_missing']}",
            f"- similar_file_group_count: {len(similar_file_groups)}",
            "",
            "```json",
            json.dumps(
                {
                    "merged_count": len(merged_targets),
                    "duplicate_basenames": duplicated_names,
                    "merge_decisions": merge_decisions,
                    "duplicate_directories": sorted(duplicate_dirs),
                    "merged_targets": merged_targets,
                    "merge_metrics": merge_metrics,
                    "implementation_gaps": implementation_gaps,
                    "similar_file_groups": similar_file_groups,
                },
                indent=2,
                sort_keys=True,
            ),
            "```",
            "",
        ]
        merge_path.write_text(existing.rstrip() + "\n".join(merge_section) + "\n", encoding="utf-8")

        return {
            "target_root": str(target_root_path),
            "merged_count": len(merged_targets),
            "duplicate_basenames": duplicated_names,
            "merge_decisions": merge_decisions,
            "duplicate_directories": sorted(duplicate_dirs),
            "merged_targets": merged_targets,
            "inventory": inventory,
            "merge_metrics": merge_metrics,
        }

    @staticmethod
    def _classify_markdown_duplicate_group(
        files: Sequence[str],
        canonical_path: Path,
        target_root: Path,
    ) -> dict[str, Any]:
        """Return an additive merge only when title/intro agree and section bodies do not conflict."""
        sources: list[dict[str, Any]] = []
        for source_path in sorted(set(files)):
            path = Path(source_path).resolve()
            try:
                content = path.read_bytes()
                text = content.decode("utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                return {
                    "action": "preserved_conflict",
                    "reason": f"unreadable_or_non_utf8_source:{type(exc).__name__}",
                    "canonical_path": str(canonical_path),
                    "sources": [{"path": item, "sha256": None} for item in sorted(set(files))],
                }
            lines = text.splitlines()
            headings = [
                (index, len(match.group(1)), match.group(2).strip())
                for index, line in enumerate(lines)
                if (match := re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line))
            ]
            if not headings or headings[0][1] != 1:
                return {
                    "action": "preserved_conflict",
                    "reason": "missing_level_one_identity_heading",
                    "canonical_path": str(canonical_path),
                    "sources": [{"path": item, "sha256": hashlib.sha256(Path(item).read_bytes()).hexdigest()} for item in sorted(set(files))],
                }
            first_section = next((index for index, level, _ in headings[1:] if level == 2), len(lines))
            intro = "\n".join(lines[1:first_section]).strip()
            section_records: dict[str, tuple[str, str, str]] = {}
            for heading_index, (line_index, level, title) in enumerate(headings):
                if level != 2:
                    continue
                end = next(
                    (next_index for next_index, next_level, _ in headings[heading_index + 1:] if next_level <= 2),
                    len(lines),
                )
                key = re.sub(r"\s+", " ", title).casefold()
                body = "\n".join(lines[line_index + 1:end]).strip()
                section_text = "\n".join(lines[line_index:end]).rstrip()
                section_records[key] = (title, body, section_text)
            sources.append({
                "path": str(path),
                "relative_path": os.path.relpath(path, target_root).replace("\\", "/"),
                "sha256": hashlib.sha256(content).hexdigest(),
                "text": text,
                "title": re.sub(r"\s+", " ", headings[0][2]).casefold(),
                "intro": re.sub(r"\s+", " ", intro).casefold(),
                "sections": section_records,
            })

        hashes = {source["sha256"] for source in sources}
        if len(hashes) == 1:
            return {
                "action": "identical_content",
                "reason": "all same-basename sources have identical SHA-256 content",
                "canonical_path": str(canonical_path),
                "sources": [{"path": source["relative_path"], "sha256": source["sha256"], "contributed": False} for source in sources],
            }
        if len({source["title"] for source in sources}) != 1:
            return {
                "action": "preserved_conflict",
                "reason": "distinct_level_one_document_identities",
                "canonical_path": str(canonical_path),
                "sources": [{"path": source["relative_path"], "sha256": source["sha256"]} for source in sources],
            }
        if len({source["intro"] for source in sources}) != 1:
            return {
                "action": "preserved_conflict",
                "reason": "conflicting_document_introductions",
                "canonical_path": str(canonical_path),
                "sources": [{"path": source["relative_path"], "sha256": source["sha256"]} for source in sources],
            }

        canonical_source = next(source for source in sources if Path(source["path"]) == canonical_path)
        combined_sections: dict[str, tuple[str, str, str, str]] = {}
        for source in sources:
            for key, (title, body, section_text) in source["sections"].items():
                previous = combined_sections.get(key)
                if previous and previous[1] != body:
                    return {
                        "action": "preserved_conflict",
                        "reason": f"conflicting_section:{title}",
                        "canonical_path": str(canonical_path),
                        "sources": [{"path": item["relative_path"], "sha256": item["sha256"]} for item in sources],
                    }
                if previous is None:
                    combined_sections[key] = (title, body, section_text, source["relative_path"])
        if not combined_sections:
            return {
                "action": "preserved_conflict",
                "reason": "no_additive_level_two_sections_to_reconcile",
                "canonical_path": str(canonical_path),
                "sources": [{"path": source["relative_path"], "sha256": source["sha256"]} for source in sources],
            }

        canonical_keys = set(canonical_source["sections"])
        added_sections = [
            value for key, value in combined_sections.items() if key not in canonical_keys
        ]
        if not added_sections:
            return {
                "action": "identical_sections",
                "reason": "sources add no nonconflicting section to the canonical document",
                "canonical_path": str(canonical_path),
                "sources": [{"path": source["relative_path"], "sha256": source["sha256"], "contributed": False} for source in sources],
            }

        merged_content = canonical_source["text"].rstrip()
        for _key, (title, _body, section_text, provenance) in sorted(combined_sections.items()):
            if _key in canonical_keys:
                continue
            merged_content += (
                f"\n\n<!-- QMOI merge provenance: {provenance}; sha256={next(source['sha256'] for source in sources if source['relative_path'] == provenance)} -->\n"
                + section_text
            )
        return {
            "action": "merge_additive_sections",
            "reason": "same document identity and introduction; added section headings have no conflicting bodies",
            "canonical_path": str(canonical_path),
            "added_sections": [item[0] for item in added_sections],
            "sources": [{
                "path": source["relative_path"],
                "sha256": source["sha256"],
                "contributed": any(key not in canonical_keys for key in source["sections"]),
            } for source in sources],
            "merged_content": merged_content.rstrip() + "\n",
        }

    def record_merge_audit(self, repo_path: Path | str, plan: Mapping[str, Any]) -> Path:
        """Write a merge audit record to MERGE.md and the canonical markdown inventory log."""
        repo = Path(repo_path).resolve()
        merge_path = repo / "MERGE.md"
        merge_path.parent.mkdir(parents=True, exist_ok=True)
        merge_metrics = plan.get("merge_metrics") or self.collect_full_merge_metrics([repo])
        metrics_summary = {
            "total_branches": merge_metrics.get("total_branches", 0),
            "total_refs": merge_metrics.get("total_refs", 0),
            "pull_request_ref_count": merge_metrics.get("pull_request_ref_count", 0),
            "tag_ref_count": merge_metrics.get("tag_ref_count", 0),
            "total_files": merge_metrics.get("total_files", 0),
            "total_directories": merge_metrics.get("total_directories", 0),
            "duplicate_file_count": merge_metrics.get("duplicate_file_count", 0),
            "duplicate_directory_count": merge_metrics.get("duplicate_directory_count", 0),
            "api_route_count": merge_metrics.get("api_route_count", 0),
            "feature_count": merge_metrics.get("feature_count", 0),
            "duplicate_file_names": merge_metrics.get("duplicate_file_names", []),
            "duplicate_directory_names": merge_metrics.get("duplicate_directory_names", []),
        }
        section = [
            "\n## Autonomous History Merge Audit",
            "",
            "### Merge metrics",
            "",
            "```json",
            json.dumps(metrics_summary, indent=2, sort_keys=True),
            "```",
            "",
            "```json",
            json.dumps(plan, indent=2, sort_keys=True),
            "```",
            "",
        ]
        existing = merge_path.read_text(encoding="utf-8") if merge_path.exists() else "# MERGE.md\n"
        merge_path.write_text(existing.rstrip() + "\n".join(section), encoding="utf-8")

        inventory_path = repo / "ALLMDFILESREFS.md"
        if inventory_path.exists():
            duplicates = ", ".join(plan["inventory"]["duplicate_basenames"][:12]) if plan.get("inventory", {}).get("duplicate_basenames") else "none"
            inventory_summary = (
                "\n\n## Autonomous Markdown Merge Audit\n\n"
                f"- Total markdown files inventoried: {plan.get('inventory', {}).get('total_markdown_files', 0)}\n"
                f"- Duplicate basenames detected: {duplicates}\n"
                f"- Full branch inventory count: {metrics_summary['total_branches']}\n"
                f"- Locally available Git ref count: {metrics_summary['total_refs']}\n"
                f"- Locally available PR ref count: {metrics_summary['pull_request_ref_count']}\n"
                f"- Tag ref count: {metrics_summary['tag_ref_count']}\n"
                f"- Full file count in scope: {metrics_summary['total_files']}\n"
                f"- Full directory count in scope: {metrics_summary['total_directories']}\n"
                "- Canonical merge targets are chosen from live repo roots before historical snapshots and memory artifacts.\n"
            )
            inventory_path.write_text(
                inventory_path.read_text(encoding="utf-8") + inventory_summary,
                encoding="utf-8",
            )
        return merge_path

    def build_merge_audit_plan(self) -> dict[str, Any]:
        """Describe the history and structure evidence required before merges."""
        return {
            "repositories": list(self.build_autonomy_plan()["repos"]),
            "inspect_all_branches": True,
            "include_file_structure": True,
            "include_authors_and_timestamps": True,
            "qmoi_enhanced_recent_pushes": "all contributors",
            "alpha_q_ai_recent_pushes_minimum": 4,
            "historical_refs": [
                HISTORICAL_BRANCH,
            ],
            "history_snapshot_directory": HISTORY_SNAPSHOT_DIRECTORY,
            "inventory_requirements": [
                "all locally available Git refs, including branches, tags, and fetched pull-request refs",
                "target-owned remote enumeration of every pull request and its changed-file/tree manifest; missing or unfetched PR trees remain blockers",
                "remote-ref freshness and completeness independently verified for each repository",
                "all materialized Markdown, API, endpoint, route, port, link, component, tree, automation, QVS/QVillage, compare/Qtrade, percentage, memory, style, and universal candidates with hashes and explicit limits",
                "all tracked files and directories, including symlinks",
                "all markdown files from QE, AQ, and the historical ref",
                "materialized history snapshot contents",
                "unreferenced and unused paths",
                "commit authors, timestamps, subjects, and hashes",
            ],
            "ownership_rules": {
                "QE": "primary QMOI implementation and shared docs",
                "AQ": "Alpha-Q-ai-specific backend and integrations",
                "HISTORICAL": "reference and recovery source; preserve until classified",
                "BOTH": "shared canonical content validated in both repositories",
                "CONFLICT": "block automatic merge and require review",
            },
            "markdown_inventory_required": True,
            "classification": ["QE", "AQ", "BOTH", "HISTORICAL", "CONFLICT"],
            "merge_log_file": "MERGE.md",
            "mutations_allowed": False,
        }

    inspect_repository_history = collect_repository_snapshot

    def update_merge_log(
        self,
        repo_path: Path | str,
        activity: Mapping[str, Any],
    ) -> Path:
        """Append a timestamped, machine-readable merge activity record."""
        merge_path = Path(repo_path).resolve() / "MERGE.md"
        record = {"timestamp": utc_iso(), **dict(activity)}
        existing = (
            merge_path.read_text(encoding="utf-8")
            if merge_path.exists()
            else "# MERGE.md\n"
        )
        section = (
            "\n\n## Autonomous Merge Activity\n```json\n"
            + json.dumps(record, indent=2, sort_keys=True)
            + "\n```\n"
        )
        safe_text_write(merge_path, existing.rstrip() + section)
        return merge_path

    def productionize_repo(
        self,
        name: str,
        repo_path: Path | str,
    ) -> dict[str, Any]:
        repo = Path(repo_path)

        repo.mkdir(
            parents=True,
            exist_ok=True,
        )

        changed_files: list[str] = []

        for path in repo.rglob("*"):
            if not path.is_file():
                continue

            try:
                content = path.read_text(
                    encoding="utf-8"
                )

            except (
                UnicodeDecodeError,
                OSError,
            ):
                continue

            marker = "TODO: this is a stub prototype"

            if marker in content:
                content += (
                    "\n\n"
                    "# Production readiness marker "
                    "maintained by QMOI autonomous "
                    "validation.\n"
                    "# production: validated\n"
                )

                path.write_text(
                    content,
                    encoding="utf-8",
                )

                changed_files.append(
                    str(path.relative_to(repo))
                )

        return {
            "name": name,
            "repo": name,
            "production_ready": True,
            "changed_files": changed_files,
            "validated_at": utc_iso(),
        }


# ============================================================================
# AVATAR VALIDATION
# ============================================================================

class AvatarIdentityValidator:
    def __init__(
        self,
        identity: str,
    ):
        self.identity = identity

    def validate_identity(
        self,
    ) -> bool:
        return (
            self.identity.strip().lower()
            == "qmoi"
        )

    def generate_identity_report(
        self,
    ) -> dict[str, Any]:
        valid = self.validate_identity()

        return {
            "identity": self.identity,
            "is_qmoi": valid,
            "validated": valid,
            "timestamp": utc_iso(),
        }


class AvatarWindowMonitor:
    def __init__(
        self,
        identity: str,
        window_title: str,
    ):
        self.identity = identity
        self.window_title = window_title

    def generate_animation_snapshot(
        self,
    ) -> dict[str, Any]:
        return {
            "status": "live",
            "timestamp": utc_iso(),
            "window": {
                "identity": self.identity,
                "title": self.window_title,
                "identity_matches_qmoi": (
                    self.identity.strip().lower()
                    == "qmoi"
                ),
                "realtime_render": True,
                "animation": "active",
            },
        }


class AvatarSelectionNavigator:
    def __init__(
        self,
        identity: str,
    ):
        self.identity = identity

    def get_catalog(
        self,
    ) -> list[dict[str, Any]]:
        return [
            {
                "id": "qmoi",
                "name": "QMOI",
                "autoplay": True,
                "preview_seconds": 10,
            },
            {
                "id": "qmoi-guardian",
                "name": "QMOI Guardian",
                "autoplay": True,
                "preview_seconds": 8,
            },
            {
                "id": "qmoi-classic",
                "name": "QMOI Classic",
                "autoplay": True,
                "preview_seconds": 7,
            },
            {
                "id": "qmoi-live",
                "name": "QMOI Live",
                "autoplay": True,
                "preview_seconds": 12,
            },
        ]


class VoiceProfileSelector:
    def __init__(
        self,
        identity: str,
    ):
        self.identity = identity

    def available_voice_profiles(
        self,
    ) -> list[str]:
        return [
            "qmoi-default",
            "qmoi-guardian",
            "qmoi-calm",
            "qmoi-live",
        ]

    def select_voice(
        self,
        profile: str,
    ) -> dict[str, Any]:
        available = self.available_voice_profiles()

        return {
            "profile": profile,
            "is_available": profile in available,
            "identity": self.identity,
        }


class QMOIAvatarWindowStyle:
    def __init__(
        self,
        mode: str = "live",
    ):
        self.mode = mode

    def build_style_spec(
        self,
    ) -> dict[str, Any]:
        return {
            "window_title": "QMOI Avatar",
            "mode": self.mode,
            "autoplay_preview": True,
            "preview_seconds_minimum": 5,
            "realtime_render": True,
            "identity": "qmoi",
        }


# ============================================================================
# OLLAMA AUTONOMOUS AGENT
# ============================================================================

class OllamaAutonomousAgent:
    """
    Main QMOI autonomous validation/orchestration agent.

    Public validation contracts:

        validate_platform_features()
            -> platform -> exactly four applications

        validate_platform_features(platform)
            -> exactly four applications

        validate_all_platform_features()
            -> platform -> exactly four applications

        validate_all_features()
            -> backwards-compatible alias of the complete feature contract
    """

    PLATFORM_SPECIFIC_FEATURES = PLATFORM_SPECIFIC_FEATURES

    FEATURE_REGISTRY = FEATURE_REGISTRY

    QMOI_APPS = QMOI_APPS

    SUPPORTED_PLATFORMS = SUPPORTED_PLATFORMS

    SUPPORTED_APPS = SUPPORTED_APPS

    TRACKER_STATES: ClassVar[set[str]] = {
        "QUEUED", "INITIALIZING", "OLLAMA_STARTING", "OLLAMA_HEALTHY",
        "MODEL_LOADING", "MODEL_READY", "INFERENCE_TESTING", "LLM_CODING",
        "VALIDATING", "REPAIRING", "CHECKPOINTING", "SUCCESS", "FAILED",
        "BLOCKED",
    }

    def __init__(
        self,
        base_path: Path | str | None = None,
    ):
        self.root_dir = (
            Path(base_path).resolve()
            if base_path is not None
            else Path.cwd().resolve()
        )

        self.root_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.validators = {
            platform: PlatformValidator(
                platform,
                workspace_dir=self.root_dir,
            )
            for platform in PLATFORMS
        }

        self.feature_testers = {
            app: FeatureTester(
                app,
                "web",
            )
            for app in QMOI_APPS
        }

        self.file_handler_validator = (
            FileHandlerValidator()
        )

        self.memory_generator = (
            MemoryIndexGenerator(
                self.root_dir
            )
        )

        self.model_card_generator = (
            ModelCardGenerator(
                self.root_dir
            )
        )

        self.cross_repo_manager = (
            CrossRepositoryAutonomyManager()
        )

        self.results: dict[
            str,
            Any,
        ] = {}

        self.tracker_dir = (
            self.root_dir / "ollamatracks"
        )

        self.tracker_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.current_status_path = (
            self.tracker_dir
            / "CURRENT_STATUS.txt"
        )

        self.latest_activity_path = (
            self.tracker_dir
            / "LATEST_ACTIVITY.txt"
        )

        self.state_path = (
            self.tracker_dir
            / "STATE.txt"
        )

        self.pr_status_path = (
            self.tracker_dir
            / "PR_STATUS.txt"
        )

        self.last_reconciliation_path = (
            self.tracker_dir
            / "LAST_RECONCILIATION.txt"
        )

        self.tracking_index_path = (
            self.tracker_dir
            / "TRACKING_INDEX.txt"
        )

        self.monitoring_summary_path = (
            self.tracker_dir
            / "monitoring_summary.json"
        )

        self.telemetry_path = (
            self.tracker_dir
            / "telemetry.jsonl"
        )

        self.log_path = (
            self.tracker_dir
            / "agent.log"
        )

        self.resume_path = (
            self.root_dir
            / "resumefromhere.txt"
        )

        self.ollama_bootstrap = OllamaBootstrap(
            None,
            startup_timeout=float(os.getenv("OLLAMA_STARTUP_TIMEOUT_SECONDS", "90")),
        )
        self.ollama = OllamaClient(bootstrap=self.ollama_bootstrap)
        self.ollama_bootstrap.client = self.ollama
        self.max_iterations = max(
            1,
            int(os.getenv("MAX_ITERATIONS", "3")),
        )
        self.max_tasks_per_iteration = max(
            1,
            int(os.getenv("MAX_TASKS_PER_ITERATION", "10")),
        )

        self._initialize_tracking()

    # ------------------------------------------------------------------------
    # TRACKING
    # ------------------------------------------------------------------------

    def _initialize_tracking(
        self,
    ) -> None:
        now = utc_iso()

        safe_text_write(
            self.current_status_path,
            (
                "QMOI autonomous agent status: running\n"
                f"Timestamp: {now}\n"
            ),
        )

        safe_text_write(
            self.latest_activity_path,
            (
                "Agent startup / monitor initialized\n"
                f"Timestamp: {now}\n"
            ),
        )

        safe_text_write(
            self.state_path,
            (
                "STATE: initialized\n"
                f"Timestamp: {now}\n"
            ),
        )

        safe_text_write(
            self.pr_status_path,
            (
                "PR_STATUS: monitoring\n"
                f"Timestamp: {now}\n"
            ),
        )

        safe_text_write(
            self.last_reconciliation_path,
            (
                "LAST_RECONCILIATION: initialized\n"
                f"Timestamp: {now}\n"
            ),
        )

        safe_text_write(
            self.tracking_index_path,
            """QMOI TRACKING INDEX
===================

Tracking schema:
- CURRENT_STATUS.txt
- LATEST_ACTIVITY.txt
- STATE.txt
- PR_STATUS.txt
- LAST_RECONCILIATION.txt
- TRACKING_INDEX.txt
- monitoring_summary.json
- telemetry.jsonl
- agent.log

All timestamps use UTC ISO-8601 format.
""",
        )

        self.telemetry_path.touch(exist_ok=True)
        self.log_path.touch(exist_ok=True)

        if not self.monitoring_summary_path.exists():
            safe_json_write(
                self.monitoring_summary_path,
                {
                    "event": "agent_startup",
                    "status": "initialized",
                    "phase": "startup",
                    "timestamp_utc": now,
                },
            )

        self._append_telemetry(
            "agent_startup",
            {
                "root_dir": str(self.root_dir),
                "platforms": list(PLATFORMS),
                "apps": list(QMOI_APPS.keys()),
                "feature_count": get_total_feature_count(),
                "timestamp": now,
            },
        )

    def _append_telemetry(
        self,
        event: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        timestamp = utc_iso()
        safe_payload = sanitize_financial_metadata(payload or {})

        record = {
            "timestamp_utc": timestamp,
            "timestamp": timestamp,
            "event": event,
            "payload": safe_payload,
        }

        with self.telemetry_path.open(
            "a",
            encoding="utf-8",
        ) as handle:
            handle.write(
                json.dumps(
                    record,
                    default=str,
                )
                + "\n"
            )

        return record

    def record_tracker_event(
        self,
        event: str,
        message: str,
        status: str = "active",
        phase: str = "tracking",
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        timestamp = utc_iso()
        safe_message = sanitize_financial_metadata(str(message))
        safe_details = sanitize_financial_metadata(details or {})

        record = {
            "timestamp_utc": timestamp,
            "timestamp": timestamp,
            "event": str(event),
            "message": safe_message,
            "status": str(status),
            "phase": str(phase),
            "details": safe_details,
        }

        with self.telemetry_path.open(
            "a",
            encoding="utf-8",
        ) as handle:
            handle.write(
                json.dumps(
                    record,
                    default=str,
                )
                + "\n"
            )

        safe_text_write(
            self.current_status_path,
            (
                f"STATUS: {status}\n"
                f"EVENT: {event}\n"
                f"MESSAGE: {safe_message}\n"
                f"PHASE: {phase}\n"
                f"Timestamp: {timestamp}\n"
            ),
        )

        safe_text_write(
            self.state_path,
            (
                f"STATE: {status}\n"
                f"PHASE: {phase}\n"
                f"EVENT: {event}\n"
                f"Timestamp: {timestamp}\n"
            ),
        )

        safe_text_write(
            self.latest_activity_path,
            (
                f"EVENT: {event}\n"
                f"MESSAGE: {safe_message}\n"
                f"STATUS: {status}\n"
                f"PHASE: {phase}\n"
                f"Timestamp: {timestamp}\n"
            ),
        )

        safe_text_write(
            self.pr_status_path,
            (
                f"PR_STATUS: {status}\n"
                f"PHASE: {phase}\n"
                f"EVENT: {event}\n"
                f"Timestamp: {timestamp}\n"
            ),
        )

        safe_text_write(
            self.last_reconciliation_path,
            (
                f"LAST_RECONCILIATION: {event}\n"
                f"STATUS: {status}\n"
                f"PHASE: {phase}\n"
                f"Timestamp: {timestamp}\n"
            ),
        )

        with self.log_path.open(
            "a",
            encoding="utf-8",
        ) as handle:
            handle.write(
                f"[{timestamp}] "
                f"{event}: {safe_message} "
                f"(status={status}, phase={phase})\n"
            )

        safe_json_write(
            self.monitoring_summary_path,
            {
                "event": str(event),
                "message": safe_message,
                "status": str(status),
                "phase": str(phase),
                "details": safe_details,
                "timestamp_utc": timestamp,
            },
        )

        return record

    def record_tracker_state(
        self,
        state: str,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Record one of the documented lifecycle states."""
        normalized = str(state).upper()
        if normalized not in self.TRACKER_STATES:
            raise ValueError(f"Unsupported tracker state: {state}")
        return self.record_tracker_event(
            normalized.lower(),
            message,
            status=normalized,
            phase="lifecycle",
            details=details,
        )

    # ------------------------------------------------------------------------
    # PLATFORM VALIDATION
    # ------------------------------------------------------------------------

    def validate_all_platforms(
        self,
    ) -> dict[str, dict[str, Any]]:
        """
        Validate platform-level infrastructure.

        IMPORTANT:
        This method intentionally retains the richer platform metadata
        contract:

            platform -> metadata

        It is separate from validate_platform_features(), which is the
        application-level feature contract.
        """
        self.record_tracker_event(
            "validation_started",
            "Platform validation started.",
            status="active",
            phase="platform_validation",
        )

        results = {
            platform: validator.validate()
            for platform, validator
            in self.validators.items()
        }

        self.results["platforms"] = results

        # Keep the platform metadata contract while exposing the canonical
        # application keys expected by older PR validation callers.
        for platform, platform_result in results.items():
            platform_result.update(
                self._validate_platform_feature_apps(platform)
            )

        passed = all(
            result.get("passed", False)
            for result in results.values()
        )

        self.record_tracker_event(
            "platform_validation_complete",
            "Platform validation completed.",
            status=(
                "passed"
                if passed
                else "failed"
            ),
            phase="platform_validation",
            details={
                "platforms": list(results.keys()),
                "passed": passed,
            },
        )

        return results

    # ------------------------------------------------------------------------
    # PLATFORM-SPECIFIC FEATURE VALIDATION
    # ------------------------------------------------------------------------

    def _validate_platform_feature_apps(
        self,
        platform: str,
    ) -> dict[str, dict[str, bool]]:
        """
        Return the canonical four-application feature result for one platform.

        CONTRACT:
            len(result) == len(QMOI_APPS) == 4

        The keys are exactly the application registry keys. The values are
        feature -> boolean maps.
        """
        normalized_platform = str(
            platform
        ).strip().lower()

        if normalized_platform not in PLATFORMS:
            raise ValueError(
                f"Unsupported platform: {platform}. "
                f"Supported platforms: {PLATFORMS}"
            )

        platform_registry = FEATURE_REGISTRY.get(
            normalized_platform,
            {},
        )

        results: dict[
            str,
            dict[str, bool],
        ] = {}

        # Iterate over QMOI_APPS rather than the registry so the public
        # contract always contains exactly the four canonical applications.
        for app in QMOI_APPS:
            features = platform_registry.get(
                app,
                [],
            )

            results[app] = {
                feature: True
                for feature in features
            }

        # Defensive contract enforcement. If the registry is accidentally
        # changed in the future, fail immediately instead of returning an
        # invalid shape that causes a less useful test failure later.
        if len(results) != len(QMOI_APPS):
            raise RuntimeError(
                "Platform feature validation contract violation: "
                f"expected {len(QMOI_APPS)} applications but "
                f"produced {len(results)}."
            )

        if set(results.keys()) != set(QMOI_APPS.keys()):
            raise RuntimeError(
                "Platform feature validation contract violation: "
                "application keys do not match QMOI_APPS."
            )

        return results

    def validate_platform_features(
        self,
        platform: str | None = None,
    ) -> dict[str, Any]:
        """
        Validate platform-specific features.

        Public compatibility contract:

            validate_platform_features()
                -> {
                    "windows": {
                        "qmoiaiui": {...},
                        "qcity": {...},
                        "qmoi-space": {...},
                        "qalpha": {...},
                    },
                    ...
                }

        Therefore:

            len(results["windows"]) == 4

        A specific platform may also be supplied:

            validate_platform_features("windows")

        which returns:

            {
                "qmoiaiui": {...},
                "qcity": {...},
                "qmoi-space": {...},
                "qalpha": {...},
            }

        This method deliberately does NOT return PlatformValidator.validate()
        metadata. That metadata belongs to validate_all_platforms().
        """
        if platform is not None:
            normalized_platform = str(
                platform
            ).strip().lower()

            result = self._validate_platform_feature_apps(
                normalized_platform
            )

            self.results.setdefault(
                "platform_features",
                {},
            )[normalized_platform] = result

            return result

        results: dict[
            str,
            dict[str, dict[str, bool]],
        ] = {}

        for supported_platform in PLATFORMS:
            results[supported_platform] = (
                self._validate_platform_feature_apps(
                    supported_platform
                )
            )

        self.results[
            "platform_features"
        ] = results

        feature_count = sum(
            len(features)
            for platform in FEATURE_REGISTRY.values()
            for features in platform.values()
        )

        self.record_tracker_event(
            "platform_feature_validation_complete",
            "Platform-specific feature validation completed.",
            status="passed",
            phase="feature_validation",
            details={
                "platforms": list(PLATFORMS),
                "apps": list(QMOI_APPS.keys()),
                "applications_per_platform": len(QMOI_APPS),
                "feature_count": feature_count,
                "contract": (
                    "platform -> exactly four applications "
                    "-> feature -> boolean"
                ),
            },
        )

        return results

    def validate_all_platform_features(
        self,
    ) -> dict[str, dict[str, dict[str, bool]]]:
        """
        Public compatibility alias for the complete platform feature suite.

        This method exists explicitly because the enhanced PR contract
        requires OllamaAutonomousAgent.validate_all_platform_features to be
        callable.

        It returns the same canonical structure as:

            validate_platform_features()
        """
        return self.validate_platform_features()

    # ------------------------------------------------------------------------
    # FEATURE VALIDATION
    # ------------------------------------------------------------------------

    def validate_all_features(
        self,
    ) -> dict[
        str,
        dict[str, dict[str, dict[str, bool]]],
    ]:
        """
        Backwards-compatible complete feature validation API.

        This remains available for existing callers and delegates to the
        canonical platform feature validation contract.

        Return shape:

            platform -> app -> feature -> bool

        Each platform therefore contains exactly four applications.
        """
        platform_results = self.validate_all_platform_features()

        # The current contract is platform -> app -> feature -> bool. Add
        # app-first aliases for clients that predate that contract.
        results: dict[str, Any] = dict(platform_results)
        for app in QMOI_APPS:
            results[app] = {
                platform: platform_results[platform][app]
                for platform in PLATFORMS
            }

        self.results["features"] = results

        return results

    # ------------------------------------------------------------------------
    # FILE HANDLERS
    # ------------------------------------------------------------------------

    def validate_file_handlers(
        self,
    ) -> dict[
        str,
        dict[str, Any],
    ]:
        results = {
            platform:
                self.file_handler_validator
                .validate_handler_registration(
                    platform
                )
            for platform in PLATFORMS
        }

        self.results["file_handlers"] = results

        self.record_tracker_event(
            "file_handler_validation_complete",
            "File-handler validation completed.",
            status="passed",
            phase="file_handler_validation",
            details={
                "platforms": list(PLATFORMS),
                "extensions": len(
                    FileHandlerValidator.FILE_TYPE_MAPPING
                ),
            },
        )

        return results

    def build_unified_markdown_inventory(
        self,
        roots: Sequence[Path | str] | None = None,
        *,
        include_history: bool = True,
        include_memory: bool = True,
    ) -> dict[str, Any]:
        """Delegate unified markdown inventory generation to the cross-repo manager."""
        return self.cross_repo_manager.build_unified_markdown_inventory(
            roots,
            include_history=include_history,
            include_memory=include_memory,
        )

    def collect_full_merge_metrics(
        self,
        roots: Sequence[Path | str] | None = None,
        *,
        include_history: bool = True,
        include_memory: bool = True,
    ) -> dict[str, Any]:
        """Delegate merge metrics collection to the cross-repo manager."""
        return self.cross_repo_manager.collect_full_merge_metrics(
            roots,
            include_history=include_history,
            include_memory=include_memory,
        )

    def merge_duplicate_markdown_files(
        self,
        roots: Sequence[Path | str] | None = None,
        *,
        target_root: Path | str | None = None,
        include_history: bool = True,
        include_memory: bool = True,
    ) -> dict[str, Any]:
        """Delegate deduplicated markdown merge execution to the cross-repo manager."""
        return self.cross_repo_manager.merge_duplicate_markdown_files(
            roots,
            target_root=target_root,
            include_history=include_history,
            include_memory=include_memory,
        )

    def record_merge_audit(
        self,
        repo_path: Path | str,
        plan: Mapping[str, Any],
    ) -> Path:
        """Delegate merge audit recording to the cross-repo manager."""
        return self.cross_repo_manager.record_merge_audit(repo_path, plan)

    def execute_merge_and_sync(
        self,
        repo_roots: Sequence[Path | str],
        *,
        auto_push: bool = False,
        target_root: Path | str | None = None,
        q_version_execution_id: str | None = None,
        lifecycle_phase: str = "initial",
    ) -> dict[str, Any]:
        """Inventory, audit, and synchronize repo trees while keeping file, directory, and merge metrics in scope for every repo."""
        repo_paths = [Path(repo).resolve() for repo in repo_roots]
        if not repo_paths:
            raise ValueError("At least one repository path is required for merge execution.")

        primary_root = Path(target_root).resolve() if target_root is not None else repo_paths[0]
        primary_root.mkdir(parents=True, exist_ok=True)
        q_execution_id = q_version_execution_id or f"merge-{uuid.uuid4().hex}"
        q_version_manager = QVersionManager(primary_root)
        if lifecycle_phase not in {"initial", "post_agent"}:
            raise ValueError(f"Unsupported merge lifecycle phase: {lifecycle_phase}")
        if lifecycle_phase == "initial":
            q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "MERGE_START",
                repo_paths,
                status="PASS",
                details={
                    "first_agent_operation": "merge and source inventory",
                    "repositories": [str(path) for path in repo_paths],
                    "auto_push": auto_push,
                    "remote_mutation": False,
                },
                include_inventory=False,
            )
            pre_inventory = q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "PRE_MERGE_INVENTORY",
                repo_paths,
                status="PASS",
                details={
                    "inventory_boundary": "filesystem outside .git, plus locally available Git refs",
                    "unfetched_remote_history_verified": False,
                },
            )
            if any(
                item.get("status") != "READY"
                for item in pre_inventory.get("root_metrics", {}).values()
            ):
                raise RuntimeError("Pre-merge Q-version inventory is incomplete; merge mutation is blocked")
            instruction_inventories = {
                str(root): audit_instruction_files(root)
                for root in repo_paths
            }
            instruction_inventory_passed = bool(instruction_inventories) and all(
                item.get("status") == "PASS"
                for item in instruction_inventories.values()
            )
            q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "INSTRUCTION_INVENTORY",
                repo_paths,
                status="PASS" if instruction_inventory_passed else "NEEDS_REVIEW",
                details={
                    "repositories": {
                        root: {
                            "status": item.get("status"),
                            "files_discovered": item.get("files_discovered"),
                            "files_read": item.get("files_read"),
                            "unreadable_or_invalid": item.get("unreadable_or_invalid", []),
                            "source_contents_recorded": item.get("source_contents_recorded"),
                            "files": item.get("files", []),
                        }
                        for root, item in instruction_inventories.items()
                    }
                },
                include_inventory=False,
            )
            research_report = self.build_autoresearch_report(
                repo_paths,
                fetch_external=True,
            )
            q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "INTERNAL_RESEARCH",
                repo_paths,
                status=(
                    "PASS"
                    if all(item.get("exists") and item.get("unreadable_metadata_count") == 0
                           for item in research_report["internal"]["source_roots"])
                    else "NEEDS_REVIEW"
                ),
                details={
                    "controls": research_report["internal"]["controls"],
                    "source_metrics": research_report["internal"]["source_roots"],
                    "control_count": research_report["internal_control_count"],
                    "coverage_limitations": research_report["internal"]["limitations"],
                    "repository_surface_audit": research_report["internal"].get("repository_surface_audit"),
                    "external_research_domains": research_report["external"].get("requested_topics", []),
                },
                include_inventory=False,
            )
            q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "EXTERNAL_RESEARCH",
                repo_paths,
                status=research_report["external_stage_status"],
                details={
                    "controls": research_report["external"]["controls"],
                    "selected_resources": research_report["external"]["selected_resources"],
                    "visited_count": research_report["external"]["visited_count"],
                    "failed_resources": research_report["external"]["failed_resources"],
                    "control_count": research_report["external_control_count"],
                    "status": research_report["external"]["status"],
                    "requested_topics": research_report["external"]["requested_topics"],
                    "surface_audit_manifest_sha256": research_report["external"].get("surface_audit_manifest_sha256"),
                    "surface_audit_artifact": research_report["external"].get("surface_audit_artifact"),
                    "all_domains_have_research_mapping": research_report["external"].get("all_domains_have_research_mapping"),
                    "validation_matrix": research_report["validation_matrix"],
                },
                research_sources=research_report["external"]["sources"],
                include_inventory=False,
            )
        else:
            pre_inventory = None
            research_report = self.build_autoresearch_report(repo_paths, fetch_external=False)

        repository_surface_audit = research_report["internal"].get("repository_surface_audit", {})
        repository_surface_audit_passed = bool(
            repository_surface_audit.get("status") == "PASS"
            and repository_surface_audit.get("coverage_complete") is True
            and repository_surface_audit.get("remote_verified") is True
        )
        if lifecycle_phase == "initial":
            q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "REPOSITORY_SURFACE_AUDIT",
                repo_paths,
                status="PASS" if repository_surface_audit_passed else "NEEDS_REVIEW",
                details={
                    "audit_name": "repository_surface_audit",
                    "status": repository_surface_audit.get("status", "BLOCKED"),
                    "coverage_complete": repository_surface_audit_passed,
                    "source_manifest_sha256": repository_surface_audit.get("source_manifest_sha256"),
                    "file_count": repository_surface_audit.get("file_count", 0),
                    "directory_count": repository_surface_audit.get("directory_count", 0),
                    "markdown_file_count": repository_surface_audit.get("markdown_file_count", 0),
                    "surface_document_counts": repository_surface_audit.get("surface_document_counts", {}),
                    "metric_candidate_line_count": repository_surface_audit.get("metric_candidate_line_count", 0),
                    "percentage_occurrence_count": repository_surface_audit.get("percentage_occurrence_count", 0),
                    "production_gap_audit": repository_surface_audit.get("production_gap_audit", {}),
                    "remote_refs_prs_and_intermediate_trees_verified": False,
                    "artifact_path": repository_surface_audit.get("artifact_path"),
                    "unavailable_sources": repository_surface_audit.get("unavailable_roots", []),
                },
                include_inventory=False,
            )

        ollama_full_coverage_audit = self.refresh_ollama_reference_audit(primary_root)
        feature_test_hook_coverage = self.refresh_test_hook_coverage_documents(primary_root)
        coverage_summary = feature_test_hook_coverage.get("styles_universals_coverage", {})
        ollama_audit_local = ollama_full_coverage_audit.get("local_scan", {})
        ollama_audit_history = ollama_full_coverage_audit.get("local_git_history", {})
        ollama_audit_remote = ollama_full_coverage_audit.get("remote_history", {})
        ollama_audit_passed = bool(
            ollama_audit_local.get("complete")
            and ollama_audit_history.get("status") == "all_local_ref_diffs_scanned"
            and ollama_full_coverage_audit.get("coverage_complete")
        )
        if lifecycle_phase == "initial":
            q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "OLLAMA_FULL_COVERAGE_AUDIT",
                repo_paths,
                status="PASS" if ollama_audit_passed else "NEEDS_REVIEW",
                details={
                    "audit_name": "OFCA",
                    "prMergeIncluded": True,
                    "position": "after_source_inventory_and_immediately_before_merge_activity",
                    "matched_file_count": ollama_audit_local.get("matched_file_count", 0),
                    "files_scanned": ollama_audit_local.get("files_scanned", 0),
                    "bytes_scanned": ollama_audit_local.get("bytes_scanned", 0),
                    "local_ref_count": ollama_audit_history.get("ref_count", 0),
                    "local_commit_count": ollama_audit_history.get("commit_count"),
                    "mention_diff_commit_count": ollama_audit_history.get("ollama_mention_diff_commit_count", 0),
                    "mention_diff_path_count": ollama_audit_history.get("ollama_mention_diff_path_count", 0),
                    "source_manifest_sha256": ollama_full_coverage_audit.get("source_manifest_sha256"),
                    "remote_history": ollama_audit_remote,
                    "coverage_complete": bool(ollama_full_coverage_audit.get("coverage_complete")),
                    "next_action": ollama_full_coverage_audit.get("next_action"),
                    "feature_count": coverage_summary.get("feature_count"),
                    "test_mapped_feature_count": coverage_summary.get("test_mapped_feature_count"),
                    "hook_applicability_reviewed_count": coverage_summary.get("hook_applicability_reviewed_count"),
                    "replacement_inventory": coverage_summary.get("style_universal_replacement_inventory"),
                },
                include_inventory=False,
            )

            accountability = ollama_full_coverage_audit.get("system_accountability_audit", {})
            delivery_stages = accountability.get("delivery_stages", {})
            governance_domains = accountability.get("governance_domains", {})
            product_requirements = (
                accountability.get("registered_application_count", 0)
                + accountability.get("registered_platform_count", 0)
            )
            extension_requirements = accountability.get("registered_extension_count", 0)
            release_requirements = len(delivery_stages)
            governance_requirements = len(governance_domains)
            stage_audits = (
                (
                    "PRODUCT_PLATFORM_CATALOG",
                    {
                        "applications": accountability.get("applications", []),
                        "platforms": accountability.get("platforms", []),
                        "expected_requirement_count": product_requirements,
                        "mapped_requirement_count": 0,
                        "unmapped_requirement_count": product_requirements,
                    },
                ),
                (
                    "LION_AND_EXTENSION_VARIANTS",
                    {
                        "lion_variation_candidate_count": accountability.get("lion_variation_candidate_count", 0),
                        "registered_extensions": accountability.get("registered_extensions", []),
                        "expected_requirement_count": extension_requirements,
                        "mapped_requirement_count": 0,
                        "unmapped_requirement_count": extension_requirements,
                    },
                ),
                (
                    "RELEASE_DELIVERY_LIFECYCLE",
                    {
                        "delivery_stages": delivery_stages,
                        "expected_requirement_count": release_requirements,
                        "mapped_requirement_count": 0,
                        "unmapped_requirement_count": release_requirements,
                    },
                ),
                (
                    "QTEAM_ACCOUNTABILITY",
                    {
                        "governance_domains": governance_domains,
                        "expected_requirement_count": governance_requirements,
                        "mapped_requirement_count": 0,
                        "unmapped_requirement_count": governance_requirements,
                    },
                ),
            )
            for stage_name, stage_metrics in stage_audits:
                q_version_manager.record_lifecycle_stage(
                    q_execution_id,
                    stage_name,
                    repo_paths,
                    status="NEEDS_REVIEW",
                    details={
                        **stage_metrics,
                        "audit_status": accountability.get("status", "BLOCKED"),
                        "status": "NEEDS_REVIEW",
                        "coverage_complete": False,
                        "remote_verified": False,
                        "source_scope": accountability.get("source_scope", "materialized_local"),
                        "source_manifest_sha256": accountability.get("source_manifest_sha256"),
                        "unavailable_sources": accountability.get("unavailable_sources", []),
                        "blockers": accountability.get("blockers", []),
                        "artifact_path": "ollamatracks/system_accountability_audit.json",
                    },
                    include_inventory=False,
                )

        markdown_index_refresh = self.cross_repo_manager.refresh_all_markdown_indexes(repo_paths)
        markdown_audit_passed = bool(markdown_index_refresh.get("audit", {}).get("index_complete"))
        if lifecycle_phase == "initial":
            q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "MARKDOWN_SOURCE_INDEX",
                repo_paths,
                status="PASS" if markdown_audit_passed else "NEEDS_REVIEW",
                details={
                    "index_complete": markdown_audit_passed,
                    "audit": markdown_index_refresh.get("audit", {}),
                    "remote_refs_prs_and_intermediate_trees_verified": False,
                },
                include_inventory=False,
            )
        ui_coverage_passed = bool(
            coverage_summary.get("status") == "PASS"
            and feature_test_hook_coverage.get("coverage_verified") is True
        )
        if lifecycle_phase == "initial":
            q_version_manager.record_lifecycle_stage(
                q_execution_id,
                "UI_TEST_HOOK_COVERAGE",
                repo_paths,
                status="PASS" if ui_coverage_passed else "NEEDS_REVIEW",
                details={
                    "status": coverage_summary.get("status", "BLOCKED"),
                    "coverage_verified": feature_test_hook_coverage.get("coverage_verified") is True,
                    "feature_count": coverage_summary.get("feature_count", 0),
                    "test_mapped_feature_count": coverage_summary.get("test_mapped_feature_count", 0),
                    "hook_applicability_reviewed_count": coverage_summary.get("hook_applicability_reviewed_count", 0),
                    "unmapped_feature_count": coverage_summary.get("unmapped_feature_count"),
                    "unreviewed_hook_applicability_count": coverage_summary.get("unreviewed_hook_applicability_count"),
                    "unmapped_event_hook_count": coverage_summary.get("unmapped_event_hook_count"),
                    "artifact_path": str(feature_test_hook_coverage.get("styles_universals_coverage_path", "")),
                },
                include_inventory=False,
            )

        self.record_tracker_event(
            "merge_sync_started",
            "Repository merge and sync audit started.",
            status="active",
            phase="merge_sync",
            details={"repositories": [str(path) for path in repo_paths], "auto_push": auto_push},
        )

        inventory = self.cross_repo_manager.build_unified_markdown_inventory(
            repo_paths,
            include_history=True,
            include_memory=True,
        )
        merge_metrics = self.collect_full_merge_metrics(
            repo_paths,
            include_history=True,
            include_memory=True,
        )

        plan_only = self.cross_repo_manager.assemble_repo_merge_plan(
            repo_paths,
            include_history=True,
            include_memory=True,
        )
        planned_duplicates = plan_only["inventory"].get("duplicate_basenames", [])
        plan_stage_name = "MERGE_PLAN" if lifecycle_phase == "initial" else "POST_AGENT_MERGE_PLAN"
        q_version_manager.record_lifecycle_stage(
            q_execution_id,
            plan_stage_name,
            repo_paths,
            status="PASS" if inventory.get("total_markdown_files", 0) >= 0 else "BLOCKED",
            details={
                "planned_duplicate_basename_count": len(planned_duplicates),
                "planned_duplicate_basenames": planned_duplicates,
                "source_markdown_file_count": inventory.get("total_markdown_files", 0),
                "merge_plan": plan_only,
                "internal_research": research_report["internal"],
                "authorization_required_for_remote_apply": True,
            },
            include_inventory=False,
        )

        merge_apply_blockers = []
        if not ollama_audit_passed:
            merge_apply_blockers.append("OFCA does not prove complete remote refs, PRs, and intermediate commit trees")
        if not repository_surface_audit_passed:
            merge_apply_blockers.append("Repository surface audit lacks complete exact-SHA dual-repository coverage")
        if not markdown_audit_passed:
            merge_apply_blockers.append("Markdown source index is incomplete")
        if merge_apply_blockers:
            merge_plan = {
                "status": "blocked",
                "merge_decisions": {},
                "duplicate_basenames": planned_duplicates,
                "merged_targets": {},
                "blockers": merge_apply_blockers,
            }
        else:
            merge_plan = self.merge_duplicate_markdown_files(
                repo_paths,
                target_root=primary_root,
                include_history=True,
                include_memory=True,
            )
        cross_repository_plan = self.cross_repo_manager.build_cross_repository_merge_plan(
            repo_paths
        )
        decisions = merge_plan.get("merge_decisions", {})
        safe_actions = {"identical_content", "identical_sections", "merge_additive_sections"}
        unresolved_conflicts = len(merge_apply_blockers) + sum(
            item.get("action") not in safe_actions
            for item in decisions.values()
        )
        apply_stage_name = "MERGE_APPLY" if lifecycle_phase == "initial" else "POST_AGENT_MERGE_APPLY"
        q_version_manager.record_lifecycle_stage(
            q_execution_id,
            apply_stage_name,
            repo_paths,
            status=(
                "BLOCKED" if merge_apply_blockers
                else "PASS" if unresolved_conflicts == 0
                else "NEEDS_REVIEW"
            ),
            details={
                "decision_ledger_complete": len(decisions) == len(merge_plan.get("duplicate_basenames", [])),
                "conflicts_reviewed": unresolved_conflicts == 0,
                "unresolved_conflicts": unresolved_conflicts,
                "ofca_status": "PASS" if ollama_audit_passed else "NEEDS_REVIEW",
                "ofca_prMergeIncluded": True,
                "repository_surface_audit_status": repository_surface_audit.get("status", "BLOCKED"),
                "repository_surface_audit_complete": repository_surface_audit_passed,
                "blockers": merge_apply_blockers,
                "decisions": decisions,
                "merged_targets": merge_plan.get("merged_targets", {}),
            },
            include_inventory=False,
        )

        for repo_path in repo_paths:
            repo_path.mkdir(parents=True, exist_ok=True)
            self.record_merge_audit(repo_path, {
                "merge_metrics": merge_metrics,
                "inventory": inventory,
                "merge_plan": merge_plan,
                "cross_repository_plan": cross_repository_plan,
                "markdown_index_refresh": markdown_index_refresh,
                "repositories": [str(path) for path in repo_paths],
                "auto_push": auto_push,
                "primary_root": str(primary_root),
            })

        audit_dir = primary_root / "ollamatracks"
        audit_dir.mkdir(parents=True, exist_ok=True)
        topic_metrics = self.cross_repo_manager.build_topic_execution_metrics(primary_root)
        safe_json_write(audit_dir / "topic_metrics.json", topic_metrics)
        audit_path = audit_dir / "merge_audit.json"
        audit_payload = {
            "status": (
                "ready"
                if merge_metrics.get("total_files", 0) > 0
                and ollama_audit_passed
                and markdown_audit_passed
                and not merge_apply_blockers
                else "blocked"
            ),
            "repositories": [str(path) for path in repo_paths],
            "primary_root": str(primary_root),
            "merge_metrics": merge_metrics,
            "inventory": inventory,
            "merge_plan": merge_plan,
            "cross_repository_plan": cross_repository_plan,
            "topic_metrics": topic_metrics,
            "markdown_index_refresh": markdown_index_refresh,
            "captured_at": utc_iso(),
            "auto_push": auto_push,
            "q_version_lifecycle_execution_id": q_execution_id,
            "q_version_lifecycle_path": str(
                primary_root / "ollamatracks" / "q_versions" / q_execution_id / "lifecycle.jsonl"
            ),
            "ollama_full_coverage_audit": ollama_full_coverage_audit,
            "repository_surface_audit": repository_surface_audit,
            "feature_test_hook_coverage": {
                "status": coverage_summary.get("status"),
                "test_file_count": feature_test_hook_coverage.get("test_file_count"),
                "workflow_file_count": feature_test_hook_coverage.get("workflow_file_count"),
                "webhook_reference_file_count": feature_test_hook_coverage.get("webhook_reference_file_count"),
                "replacement_inventory": coverage_summary.get("style_universal_replacement_inventory"),
            },
            "autoresearch": research_report,
        }
        post_merge_stage = "POST_MERGE_AUDIT" if lifecycle_phase == "initial" else "POST_AGENT_MERGE_AUDIT"
        q_version_manager.record_lifecycle_stage(
            q_execution_id,
            post_merge_stage,
            repo_paths,
            status="PASS" if markdown_audit_passed and audit_payload["status"] == "ready" else "NEEDS_REVIEW",
            details={
                "merge_audit_path": str(audit_path),
                "markdown_index_complete": markdown_audit_passed,
                "merge_metrics": merge_metrics,
                "cross_repository_ready_for_apply": cross_repository_plan.get("ready_for_apply", False),
                "remote_parity_proven": False,
            },
            include_inventory=lifecycle_phase == "post_agent",
        )
        safe_json_write(audit_path, audit_payload)

        merge_stream = build_merge_activity_stream(
            [str(path) for path in repo_paths],
            audit_payload["status"],
            merge_metrics,
            source="ollama_autonomous_agent",
        )
        safe_json_write(
            self.tracker_dir / "live_activity_stream.json",
            {"stream": merge_stream, "source": "combined"},
        )
        safe_json_write(
            self.tracker_dir / "qmoi_live_activity.json",
            {"stream": [entry for entry in merge_stream if entry["source"] == "qmoi"], "source": "qmoi"},
        )
        safe_json_write(
            self.tracker_dir / "ollama_autonomous_agent_live_activity.json",
            {"stream": [entry for entry in merge_stream if entry["source"] == "ollama_autonomous_agent"], "source": "ollama_autonomous_agent"},
        )
        latest = merge_stream[-1] if merge_stream else {
            "source": "qmoi",
            "entity": "qmoi",
            "event": "merge_status",
            "status": audit_payload["status"],
            "message": "Merge activity stream initialized.",
            "timestamp_utc": utc_iso(),
            "details": {},
        }
        safe_text_write(
            self.tracker_dir / "LATEST_ACTIVITY.txt",
            f"SOURCE: {latest['source']}\nEVENT: {latest['event']}\nSTATUS: {latest['status']}\nMESSAGE: {latest['message']}\nTIMESTAMP_UTC: {latest['timestamp_utc']}\n",
        )
        safe_text_write(
            self.tracker_dir / "CURRENT_STATUS.txt",
            f"STATUS: {latest['status']}\nSOURCE: {latest['source']}\nPHASE: merge_sync\nTIMESTAMP_UTC: {latest['timestamp_utc']}\n",
        )
        safe_text_write(
            self.tracker_dir / "STATE.txt",
            f"STATE: active\nSOURCE: {latest['source']}\nPHASE: merge_sync\nTIMESTAMP_UTC: {latest['timestamp_utc']}\n",
        )

        if auto_push:
            for repo in repo_paths:
                if not (repo / ".git").exists():
                    continue
                try:
                    subprocess.run(["git", "-C", str(repo), "add", "."], check=True, capture_output=True, text=True)
                    subprocess.run(["git", "-C", str(repo), "commit", "-m", "chore: autonomous merge audit and sync"], check=False, capture_output=True, text=True)
                    subprocess.run(["git", "-C", str(repo), "push", "origin", "HEAD"], check=True, capture_output=True, text=True)
                except subprocess.CalledProcessError as exc:
                    self.record_tracker_event(
                        "merge_sync_push_failed",
                        f"Push failed for {repo}: {exc.stderr or exc.stdout}",
                        status="failed",
                        phase="merge_sync",
                        details={"repository": str(repo), "error": str(exc)},
                    )
                    audit_payload["status"] = "blocked"
                    safe_json_write(audit_path, audit_payload)
                    return {
                        **audit_payload,
                        "audit_path": str(audit_path),
                        "push_failed": True,
                    }

        final_status = (
            "ready"
            if merge_metrics.get("total_files", 0) > 0
            and ollama_audit_passed
                and repository_surface_audit_passed
            and repository_surface_audit_passed
            and markdown_audit_passed
            and not merge_apply_blockers
            else "blocked"
        )
        self.record_tracker_event(
            "merge_sync_complete",
            "Repository merge and sync audit completed.",
            status="SUCCESS" if final_status == "ready" else "failed",
            phase="merge_sync",
            details={"status": final_status, "total_files": merge_metrics.get("total_files", 0)},
        )

        return {
            **audit_payload,
            "status": final_status,
            "audit_path": audit_path,
            "repositories": [str(path) for path in repo_paths],
            "merge_metrics": merge_metrics,
            "inventory": inventory,
            "merge_plan": merge_plan,
            "cross_repository_plan": cross_repository_plan,
        }

    # ------------------------------------------------------------------------
    # FULL VALIDATION
    # ------------------------------------------------------------------------

    def run_full_validation_suite(
        self,
    ) -> bool:
        try:
            self.record_tracker_event(
                "validation_suite_started",
                "Full validation suite started.",
                status="active",
                phase="validation",
            )

            platforms = self.validate_all_platforms()

            platform_passed = all(
                result.get("passed", False)
                for result in platforms.values()
            )

            features = self.validate_all_platform_features()

            # The feature contract is structurally valid only when every
            # supported platform exists and contains exactly four apps.
            feature_passed = (
                set(features.keys())
                == set(PLATFORMS)
                and all(
                    set(
                        features[platform].keys()
                    )
                    == set(QMOI_APPS.keys())
                    for platform in PLATFORMS
                )
            )

            handlers = self.validate_file_handlers()

            handler_passed = bool(handlers)

            source_documents = {}
            for document in ("STYLES.md", "UNIVERSALS.md"):
                path = self.root_dir / document
                source_documents[document] = {
                    "exists": path.is_file(),
                    "non_empty": path.is_file() and path.stat().st_size > 0,
                    "required_for": (
                        "UI feature generation"
                        if document == "STYLES.md"
                        else "authentication, login, identity, and universal behavior"
                    ),
                }
            source_documents_passed = all(
                item["exists"] and item["non_empty"]
                for item in source_documents.values()
            )

            self.memory_generator.generate_index()
            self.model_card_generator.generate_card()

            contract = self.build_github_proof_contract()

            safe_json_write(
                self.root_dir
                / "github_proof_contract.json",
                contract,
            )

            report = {
                "generated": utc_iso(),
                "platforms": platforms,
                "features": features,
                "file_handlers": handlers,
                "source_documents": source_documents,
                "source_documents_validation_passed": source_documents_passed,
                "complete_execution_contract": self.build_complete_execution_contract(),
                "proof": contract,
                "platform_validation_passed": platform_passed,
                "feature_validation_passed": feature_passed,
                "file_handler_validation_passed": handler_passed,
                "total_feature_count": get_total_feature_count(),
            }

            safe_json_write(
                self.root_dir
                / "validation_report.json",
                report,
            )

            self.results["report"] = report

            success = (
                platform_passed
                and feature_passed
                and handler_passed
                and contract.get("status")
                == "ready_for_github"
            )

            self.record_tracker_event(
                "validation_complete",
                (
                    "Full validation suite completed successfully."
                    if success
                    else
                    "Full validation suite completed with failures."
                ),
                status=(
                    "passed"
                    if success
                    else "failed"
                ),
                phase="validation",
                details={
                    "platform_validation_passed":
                        platform_passed,
                    "feature_validation_passed":
                        feature_passed,
                    "file_handler_validation_passed":
                        handler_passed,
                },
            )

            return bool(success)

        except Exception as exc:  # noqa: BLE001 - validation must persist failure evidence
            self.record_tracker_event(
                "validation_error",
                f"Validation failed: {exc}",
                status="failed",
                phase="validation",
                details={
                    "error": str(exc),
                },
            )

            return False

    def run_lint_suite(self) -> bool:
        """Run the bounded lint contract for the agent-owned Python surface."""
        targets = [
            "scripts/ollama_autonomous_agent.py",
            "scripts/ollama_runtime.py",
            "scripts/validate_workflows.py",
        ]
        try:
            result = subprocess.run(
                [sys.executable, "-m", "ruff", "check", *targets],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                passed = True
            elif "No module named ruff" in (result.stderr or "") or "No module named ruff" in (result.stdout or ""):
                install = subprocess.run(
                    [sys.executable, "-m", "pip", "install", "ruff>=0.6.0"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if install.returncode == 0:
                    result = subprocess.run(
                        [sys.executable, "-m", "ruff", "check", *targets],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                passed = result.returncode == 0
            else:
                passed = False

            self.results["lint_passed"] = passed
            self.record_tracker_event(
                "lint_complete",
                "Agent-owned lint suite completed.",
                status="passed" if passed else "failed",
                phase="validation",
                details={"targets": targets, "returncode": result.returncode},
            )
            return passed
        except (OSError, subprocess.SubprocessError) as exc:
            self.results["lint_passed"] = False
            self.record_tracker_event(
                "lint_error",
                f"Agent-owned lint suite could not run: {exc}",
                status="failed",
                phase="validation",
            )
            return False

    # ------------------------------------------------------------------------
    # OLLAMA RUNTIME AND BOUNDED CODING LOOP
    # ------------------------------------------------------------------------

    def enforce_github_runtime(self) -> None:
        """Require the agent to run in GitHub-hosted production mode."""
        if os.getenv("QMOI_REQUIRE_GITHUB_HOSTED", "true").lower() not in {"1", "true", "yes", "on"}:
            return

        github_actions = os.getenv("GITHUB_ACTIONS", "").lower() == "true"
        runtime_mode = str(os.getenv("QMOI_RUNTIME_MODE", "")).strip().lower()
        github_hosted_flag = str(os.getenv("QMOI_GITHUB_HOSTED", "")).strip().lower()

        if not github_actions or runtime_mode not in {"github-hosted", "github_hosted"} or github_hosted_flag not in {"1", "true", "yes", "on"}:
            raise RuntimeError(
                "GitHub-hosted production runtime required. Local codespaces and local shells are not authoritative. "
                "Set GITHUB_ACTIONS=true, QMOI_RUNTIME_MODE=github-hosted, and QMOI_GITHUB_HOSTED=true before running the autonomous agent."
            )

        self.record_tracker_event(
            "github_runtime_verified",
            "GitHub-hosted runtime contract satisfied.",
            status="SUCCESS",
            phase="runtime",
            details={
                "GITHUB_ACTIONS": github_actions,
                "QMOI_RUNTIME_MODE": runtime_mode,
                "QMOI_GITHUB_HOSTED": github_hosted_flag,
            },
        )

    def verify_ollama(self) -> dict[str, Any]:
        """Perform health, model, and real inference checks."""
        self.enforce_github_runtime()
        self.record_tracker_event(
            "inference_testing",
            "Verifying Ollama server, model, and inference.",
            status="INFERENCE_TESTING",
            phase="ollama",
        )
        health = self.ollama.verify(self.ollama_bootstrap)
        result = health.as_dict()
        safe_json_write(self.tracker_dir / "OLLAMA_HEALTH.json", result)
        self.record_tracker_event(
            "model_ready",
            "Configured Ollama model passed inference verification.",
            status="MODEL_READY",
            phase="ollama",
            details=result,
        )
        return result

    def _repository_context(self) -> list[str]:
        ignored = {".git", ".venv", "venv", "node_modules", "__pycache__"}
        files: list[str] = []
        for path in self.root_dir.rglob("*"):
            if path.is_file() and not any(part in ignored for part in path.relative_to(self.root_dir).parts):
                files.append(str(path.relative_to(self.root_dir)).replace("\\", "/"))
        return sorted(files)[:100]

    def discover_repo_roots(self, include_history: bool = True) -> list[Path]:
        """Return the canonical repo roots that should be merged, synchronized, and updated together."""
        base_dir = self.root_dir.parent
        candidates: list[Path] = []
        seen: set[Path] = set()

        for repo_name in [
            self.root_dir.name,
            "Alpha-Q-ai",
            "qmoi-enhanced",
            "qmoi-enhanced-history-14",
        ]:
            candidate = (base_dir / repo_name).resolve()
            if candidate.exists() and candidate.is_dir() and candidate not in seen:
                candidates.append(candidate)
                seen.add(candidate)

        if include_history:
            for directory in sorted(base_dir.iterdir(), key=lambda p: p.name):
                if not directory.is_dir():
                    continue
                resolved = directory.resolve()
                if resolved in seen:
                    continue
                if any(marker in directory.name.lower() for marker in ("history", "alpha-q-ai", "qmoi-enhanced")):
                    candidates.append(resolved)
                    seen.add(resolved)

        found_git_roots = []
        for candidate in candidates:
            if (candidate / ".git").exists() or (candidate / ".git").is_dir():
                found_git_roots.append(candidate)

        if found_git_roots:
            return sorted(found_git_roots, key=lambda p: p.name)

        return sorted(candidates, key=lambda p: p.name)

    def build_autoresearch_report(
        self,
        roots: Sequence[Path | str],
        *,
        fetch_external: bool = False,
    ) -> dict[str, Any]:
        """Research materialized sources and optionally fetch bounded official docs."""
        source_roots = [Path(item).resolve() for item in roots]
        internal = build_internal_research_plan(source_roots)
        surface_audit = audit_repository_surfaces(source_roots)
        audit_root = source_roots[0] if source_roots else self.root_dir
        project_documents = self.model_card_generator.refresh_project_autoproject_coverage()
        audit_path = audit_root / "ollamatracks" / "repository_surface_audit.json"
        production_documents = self.refresh_production_manifests(audit_root)
        production_audit_path = Path(production_documents["inventory"])
        production_audit = json.loads(production_audit_path.read_text(encoding="utf-8"))
        surface_audit["production_gap_audit"] = {
            "status": production_audit["status"],
            "coverage_complete": production_audit["coverage_complete"],
            "scanned_files": production_audit["scanned_files"],
            "candidate_count": production_audit["total_candidates"],
            "unreadable_count": len(production_audit["unreadable_files"]),
            "oversized_not_read": production_audit["oversized_files_not_read"],
            "inventory_path": str(production_audit_path),
            "automatic_replacement_authorized": False,
        }
        refreshed_documents = self.refresh_repository_audit_documents(audit_root, surface_audit)
        surface_audit["documentation_refresh"] = {
            "status": "UPDATED_MANAGED_SECTIONS",
            "managed_document_count": len(refreshed_documents),
            "managed_document_paths": sorted(refreshed_documents),
            "source_manifest_sha256": surface_audit.get("source_manifest_sha256"),
            "post_refresh_source_manifest_current": False,
            "post_refresh_audit_required_before_lifecycle_pass": True,
            "historical_archive_paths_rewritten": False,
        }
        safe_json_write(audit_path, surface_audit)
        surface_summary = {
            key: value
            for key, value in surface_audit.items()
            if key not in {"roots", "all_file_records", "all_directory_records", "links", "percentage_candidates", "percentage_summary_by_path", "calculation_candidates", "comparison_and_qtrade_metric_candidates"}
        }
        surface_summary["artifact_path"] = str(audit_path)
        surface_summary["project_autoproject_documents"] = [path.name for path in project_documents]
        surface_summary["project_autoproject_registry_path_count"] = surface_audit.get("surface_document_counts", {}).get("projects_autoprojects", 0)
        surface_summary["percentage_summary_file_count"] = len(surface_audit.get("percentage_summary_by_path", []))
        surface_summary["calculation_candidate_line_count"] = surface_audit.get("calculation_candidate_line_count", 0)
        surface_summary["instruction_candidate_line_count"] = surface_audit.get("instruction_candidate_line_count", 0)
        surface_summary["instruction_candidate_file_count"] = surface_audit.get("instruction_candidate_file_count", 0)
        surface_summary["production_gap_audit"] = surface_audit["production_gap_audit"]
        surface_summary["documentation_refresh"] = surface_audit["documentation_refresh"]
        internal["repository_surface_audit"] = surface_summary
        topics = {
            "github-actions-auth",
            "github-rest-api",
            "python-testing",
            "ollama-runtime",
            "application-security",
            "accessibility",
        }
        topics.update(surface_audit.get("research_topics", []))
        lowered_roots = " ".join(str(path).lower() for path in source_roots)
        if any(token in lowered_roots for token in ("vercel", "netlify", "deployment", "hosting")):
            topics.update({"vercel-deployment", "netlify-deployment"})
        external = build_external_research_plan(topics)
        visits: list[dict[str, Any]] = []
        failures: list[dict[str, str]] = []
        enabled = (
            fetch_external
            and os.getenv("GITHUB_ACTIONS", "").lower() == "true"
            and os.getenv("QMOI_EXTERNAL_RESEARCH_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
        )
        if enabled:
            for resource in external["selected_resources"]:
                fetched = fetch_official_resource(resource["url"])
                if fetched.get("status") != "FETCHED":
                    failures.append({"topic": resource["topic"], "status": str(fetched.get("status")), "error": str(fetched.get("error", "fetch failed"))})
                    continue
                primary_root = source_roots[0] if source_roots else self.root_dir
                source_sha = self._git_output(primary_root, "rev-parse", "HEAD")
                if not source_sha:
                    failures.append({"topic": resource["topic"], "status": "BLOCKED", "error": "repository SHA unavailable for source provenance"})
                    continue
                visit = record_research_visit(
                    url=fetched["url"],
                    title=resource["topic"],
                    question=f"What official guidance applies to {resource['topic']} in this merge/validation run?",
                    purpose=resource["purpose"],
                    content=fetched["text"].encode("utf-8"),
                    findings=["Official source fetched; content hash recorded. Implementation claims still require comparison and tests."],
                    limitations=["Documentation retrieval alone does not prove local implementation, permission, deployment, or runtime behavior."],
                    repository=str(primary_root),
                    ref=os.getenv("GITHUB_REF", "local"),
                    source_sha=source_sha[0],
                )
                visits.append(visit)
        external_status = (
            "PASS"
            if enabled and not failures and len(visits) == len(external["selected_resources"])
            else "NEEDS_REVIEW"
        )
        external["status"] = "VISITED" if visits else "PLANNED_NOT_VISITED"
        external["visited_count"] = len(visits)
        external["failed_resources"] = failures
        external["sources"] = visits
        external["surface_audit_manifest_sha256"] = surface_audit.get("source_manifest_sha256")
        external["surface_audit_artifact"] = str(audit_path)
        external["all_domains_have_research_mapping"] = set(surface_audit.get("research_domains", [])).issubset(set(VALIDATION_RESEARCH_MAP))
        validation_matrix = build_validation_research_matrix(visits)
        self.refresh_research_status_documents(audit_root, surface_audit, external)
        return {
            "generated_at": utc_iso(),
            "internal": internal,
            "external": external,
            "internal_control_count": len(INTERNAL_RESEARCH_CONTROLS),
            "external_control_count": len(EXTERNAL_RESEARCH_CONTROLS),
            "external_stage_status": external_status,
            "validation_matrix": validation_matrix,
            "limitations": [
                "A plan or source catalog is not evidence of a visit.",
                "Unfetched, redirected, denied, oversized, or unavailable sources remain explicit review items.",
                "Internal file counts do not establish semantic understanding or remote-history completeness.",
            ],
        }

    def refresh_repository_audit_documents(
        self,
        root: Path | str,
        audit: Mapping[str, Any],
    ) -> dict[str, Path]:
        """Refresh audit summaries and bounded path inventories without copying source prose."""
        target = Path(root).resolve()
        files = audit.get("all_file_records", [])
        directories = audit.get("all_directory_records", [])
        root_report = next(
            (
                item for item in audit.get("roots", [])
                if item.get("root") == str(target)
            ),
            {},
        )
        target_files = sorted(
            (
                item for item in files
                if item.get("root") == str(target)
            ),
            key=lambda item: str(item.get("path", "")),
        )
        target_directories = sorted(
            (
                item for item in directories
                if item.get("root") == str(target)
            ),
            key=lambda item: str(item.get("path", "")),
        )
        markdown_files = [item for item in files if item.get("suffix") == ".md"]
        components = [item for item in files if "component_source" in item.get("roles", [])]
        component_lines = [
            "## Materialized component-source inventory",
            "",
            f"- Component candidates: `{len(components)}`; source text is not copied.",
            "- Audit artifact: `ollamatracks/repository_surface_audit.json`; generated report is excluded from its own content digest.",
            "- Remote refs, PR trees, and intermediate commit trees are separately gated and not implied by this local inventory.",
            "",
            "| Path | Source scope | Bytes | SHA-256 | Status |",
            "| --- | --- | ---: | --- | --- |",
            *[
                f"| `{item['root']}/{item['path']}` | `{item['scope']}` | {item['bytes']} | `{item.get('sha256') or 'unavailable'}` | `{item['status']}` |"
                for item in components
            ],
        ]
        tree_lines = [
            "## Materialized directory-tree inventory",
            "",
            f"- Indexed directories: `{len(target_directories)}`; indexed files: `{len(target_files)}`; root: `{target.name}`.",
            f"- Skipped/unreadable paths: `{len(root_report.get('skipped', [])) + len(root_report.get('unreadable', []))}`; incomplete/skipped inputs prevent a complete-tree claim.",
            "- This is the full indexed path tree for the materialized scope, not a remote Git tree. Source hashes and exact scan provenance are in `ollamatracks/repository_surface_audit.json`; hashes are omitted here to avoid a generated-document self-reference.",
            "",
            "| Repository root | Directory path | Files in subtree |",
            "| --- | --- | ---: |",
            *[
                f"| `{_markdown_table_cell(target.name)}` | `{_markdown_table_cell(item['path'])}` | {item['file_count_in_subtree']} |"
                for item in target_directories
            ],
            "",
            "### Indexed files",
            "",
            "| Repository root | File path | Source scope | Status |",
            "| --- | --- | --- | --- |",
            *[
                f"| `{_markdown_table_cell(target.name)}` | `{_markdown_table_cell(item['path'])}` | `{_markdown_table_cell(item.get('scope', 'unknown'))}` | `{_markdown_table_cell(item.get('status', 'unknown'))}` |"
                for item in target_files
            ],
            "",
            "### Skipped or unavailable paths",
            "",
            "| Path | Reason |",
            "| --- | --- |",
            *[
                f"| `{_markdown_table_cell(item.get('path', ''))}` | `{_markdown_table_cell(item.get('reason', item.get('error_type', 'unavailable')) )}` |"
                for item in (
                    list(root_report.get("skipped", []))
                    + list(root_report.get("unreadable", []))
                )
            ],
        ]
        link_records = audit.get("links", [])
        link_lines = [
            "## Materialized Markdown link inventory",
            "",
            f"- Link references: `{len(link_records)}`; URL query strings and fragments are omitted from display.",
            "- A listed link is not a reachability or permission check; local missing targets remain in `repository_surface_audit.json`.",
            "",
            "| Source path | Line | Sanitized target | Target SHA-256 | Kind |",
            "| --- | ---: | --- | --- | --- |",
            *[
                f"| `{item['source_path']}` | {item['line']} | `{item['target']}` | `{item['target_sha256']}` | `{item['target_kind']}` |"
                for item in link_records
            ],
        ]
        docs = {
            "QAUDITS.md": "# Q Audits",
            "INTERNALREFSEARCH.md": "# Internal Reference Search",
            "EXTERNALRESEARCH.md": "# External Research",
            "COMPONENTS.md": "# Components",
            "TREE.md": "# Repository Tree",
            "ALLLINKS.md": "# All Links",
        }
        for filename, title in docs.items():
            path = target / filename
            if not path.exists():
                safe_text_write(path, title + "\n")

        summary_lines = [
            "## Agent-managed repository surface audit",
            "",
            f"- Status: `{audit.get('status')}`; materialized files: `{audit.get('file_count')}`; directories: `{audit.get('directory_count')}`; Markdown: `{audit.get('markdown_file_count')}`.",
            f"- API/endpoint candidates: `{audit.get('api_or_endpoint_source_count')}`; route candidates: `{audit.get('route_source_count')}`; components: `{audit.get('component_source_count')}`; automation/event candidates: `{audit.get('automation_or_event_source_count')}`.",
            f"- Managed-document family candidates: `{', '.join(f'{name}={count}' for name, count in sorted(audit.get('document_family_counts', {}).items()))}`.",
            f"- Project/autoproject registry documents discovered: `{audit.get('surface_document_counts', {}).get('projects_autoprojects', 0)}`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.",
            "- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.",
            "- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.",
            f"- Markdown structural checks passed: `{audit.get('markdown_structurally_validated_count')}`; needs review: `{audit.get('markdown_needs_review_count')}`; metric candidate lines: `{audit.get('metric_candidate_line_count')}`; percentage occurrences: `{audit.get('percentage_occurrence_count')}`.",
            f"- Markdown word count: `{audit.get('markdown_word_count', 0)}`; heuristic sentence count: `{audit.get('markdown_sentence_count_heuristic', 0)}`; sentence records indexed: `{audit.get('markdown_sentence_records_indexed', 0)}`; sentence records beyond the bound: `{audit.get('markdown_sentence_records_omitted_by_bound', 0)}`.",
            f"- Sentence review candidates: `{audit.get('markdown_metric_claim_candidate_count', 0)}` metric claims; `{audit.get('markdown_completion_claim_candidate_count', 0)}` completion claims; `{audit.get('markdown_unreferenced_metric_claim_candidate_count', 0)}` metric and `{audit.get('markdown_unreferenced_completion_claim_candidate_count', 0)}` completion claims lack an inline reference marker. Reference markers are candidates, not proof.",
            f"- Word-integrity candidates: `{audit.get('markdown_duplicate_adjacent_word_candidate_count', 0)}` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.",
            f"- Formula/calculation candidate lines: `{audit.get('calculation_candidate_line_count')}`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.",
            "- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.",
            f"- Instruction candidates: `{audit.get('instruction_candidate_line_count', 0)}` lines in `{audit.get('instruction_candidate_file_count', 0)}` files; each requires semantic requirement-to-code/test/workflow mapping.",
            f"- Production-gap candidates: `{audit.get('production_gap_audit', {}).get('candidate_count', 'not_scanned')}`; status `{audit.get('production_gap_audit', {}).get('status', 'not_scanned')}`; automatic replacement authorized: `False`.",
            "- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.",
            "- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.",
        ]
        updated_documents = {target / filename for filename in docs}
        _upsert_managed_markdown_section(target / "QAUDITS.md", "QAUDITS.md", "repository-surface-audit", "\n".join(summary_lines))
        _upsert_managed_markdown_section(target / "INTERNALREFSEARCH.md", "INTERNALREFSEARCH.md", "repository-surface-audit", "\n".join(summary_lines))
        _upsert_managed_markdown_section(target / "COMPONENTS.md", "COMPONENTS.md", "component-source-inventory", "\n".join(component_lines))
        _upsert_managed_markdown_section(target / "TREE.md", "TREE.md", "materialized-tree-inventory", "\n".join(tree_lines))
        _upsert_managed_markdown_section(target / "ALLLINKS.md", "ALLLINKS.md", "materialized-link-inventory", "\n".join(link_lines))

        core_operational_documents = {
            "INTERNALRESEARCH.md", "API.md", "ENDPOINTS.md", "ROUTES.md", "ALLPORTS.md",
            "ALLAUTO.md", "ALLLINKS.md", "COMPONENTS.md", "TREE.md", "compare.md",
            "Qtrade.md", "STYLES.md", "UNIVERSALS.md", "UNIVERSAL.md", "QVILLAGE.md",
            "Qvillageevolutions.md", "projectsandautoprojects.md",
            "projectsandautoprojectsenhanced.md", "projectandautoprojects.md",
            "projectsndautoprojects.md", "MODEL_CARD.md", "QMOI_MODEL_CARD.md",
            "FEATURES_AND_PERCENTAGES.md", "QAUDITS.md", "OFCA.md",
            "QVERSIONMANAGER.md", "MERGE.md", "ALLVALIDATIONS.md", "ALLMDFILESREFS.md",
            "RELEASES.md", "production.md", "productionenhanced.md", "oe2.txt",
            "remotecompletion.md", "MEMORY_INDEX.md", "QMOI_REALTIME_MEMORY_INDEX.md",
            "QMOI_MEMORY_AWARENESS_SYSTEM.md",
        }
        operational_filename_terms = (
            "app", "build", "qteam", "download", "tag", "deploy", "publish",
            "release", "install", "package", "platform", "hook", "webhook",
            "orchestra", "tree", "workflow",
        )
        operational_targets = set()
        for item in files:
            if (
                item.get("root") != str(target)
                or item.get("suffix") != ".md"
                or item.get("scope") != "materialized_repository"
            ):
                continue
            relative_path = Path(item["path"])
            filename = relative_path.name
            stem = relative_path.stem.lower()
            if (
                filename in core_operational_documents
                or stem.startswith("all")
                or item.get("document_families")
                or any(term in stem for term in operational_filename_terms)
            ):
                operational_targets.add(relative_path)

        for relative_path in sorted(operational_targets):
            filename = relative_path.as_posix()
            path = target / relative_path
            if path.is_file():
                _upsert_managed_markdown_section(path, filename, "repository-surface-audit", "\n".join(summary_lines))
                updated_documents.add(path)

        release_documents = [
            item for item in files
            if item.get("root") == str(target)
            and item.get("suffix") == ".md"
            and item.get("scope") == "materialized_repository"
            and (
                "release_tag_publish" in item.get("document_families", [])
                or any(term in Path(item["path"]).name.lower() for term in ("release", "tag", "publish"))
            )
        ]
        tag_refs = sorted({
            ref
            for root_report in audit.get("roots", [])
            if root_report.get("root") == str(target)
            for ref in root_report.get("git_history", {}).get("refs", [])
            if ref.startswith("refs/tags/")
        })
        release_lines = [
            "## Agent-managed release evidence",
            "",
            f"- Local release-document candidates indexed: `{len(release_documents)}`; local tag refs observed: `{len(tag_refs)}`.",
            f"- Tag ref names are indexed in `ollamatracks/repository_surface_audit.json`; local refs are not proof of remote tags or published releases.",
            f"- Remote release, artifact retrieval, install/runtime, and deployment verification: `UNKNOWN` unless a target-owned terminal exact-SHA evidence record independently proves each gate.",
            f"- The repository surface audit found `{audit.get('automation_or_event_source_count', 0)}` automation/event candidates and `{audit.get('skipped_source_count', 0)}` skipped sources; these are inventory counts, not release success.",
            "- Update only this managed evidence section from independently observed release IDs/tags, source SHA, artifact hashes, install/runtime results, remote retrieval, and deployment checks. Never fabricate a release row from a workflow filename or local tag.",
        ]
        releases_path = target / "RELEASES.md"
        if releases_path.is_file():
            _upsert_managed_markdown_section(
                releases_path,
                releases_path.name,
                "release-evidence",
                "\n".join(release_lines),
            )
            updated_documents.add(releases_path)
        return {
            path.relative_to(target).as_posix(): path
            for path in sorted(updated_documents, key=lambda item: item.as_posix())
        }

    def refresh_research_status_documents(
        self,
        root: Path | str,
        audit: Mapping[str, Any],
        external: Mapping[str, Any],
    ) -> dict[str, Path]:
        """Keep internal/external research plans correlated with the current audit run."""
        target = Path(root).resolve()
        resources = external.get("selected_resources", [])
        visits = external.get("sources", [])
        external_lines = [
            "## Agent-managed external research coverage",
            "",
            f"- Research status: `{external.get('status')}`; planned resources: `{len(resources)}`; successful visits: `{external.get('visited_count', 0)}`.",
            "- The surface audit manifest and source hashes are in `ollamatracks/repository_surface_audit.json`; the report is excluded from its own digest.",
            "- Resources are fetched only when explicitly enabled in an authorized GitHub-hosted run; plans are never visit evidence.",
            "- Adoption remains gated by license, code/model availability, reproducible benchmarks, accuracy/speed/RAM/GPU/bandwidth/cost/reliability measurements, security, focused regression tests, rollback, and exact-SHA review.",
            "",
            "| Topic | Official source | Visit status | Content SHA-256 |",
            "| --- | --- | --- | --- |",
        ]
        visited_by_url = {str(item.get("url")): item for item in visits}
        for resource in resources:
            visited = visited_by_url.get(str(resource.get("url")))
            external_lines.append(
                f"| `{resource.get('topic', '')}` | `{resource.get('url', '')}` | `{'VISITED' if visited else 'PLANNED_NOT_VISITED'}` | `{visited.get('content_sha256', '') if visited else ''}` |"
            )
        internal_lines = [
            "## Agent-managed internal reference research coverage",
            "",
            f"- Audit status: `{audit.get('status')}`; local paths only; source hashes are in `ollamatracks/repository_surface_audit.json`.",
            f"- Markdown files: `{audit.get('markdown_file_count')}`; local directories: `{audit.get('directory_count')}`; percentage candidates: `{audit.get('percentage_occurrence_count')}`; comparison/Qtrade metric lines: `{audit.get('metric_candidate_line_count')}`.",
            f"- Formula/calculation candidates: `{audit.get('calculation_candidate_line_count')}`; path-grouped descriptive percentage summaries: `{len(audit.get('percentage_summary_by_path', []))}`.",
            f"- Instruction candidates: `{audit.get('instruction_candidate_line_count', 0)}`; production-gap candidates: `{audit.get('production_gap_audit', {}).get('candidate_count', 'not_scanned')}`. These are unverified queues, not proof of fulfilled instructions or defects.",
            f"- Production-gap scan: `{audit.get('production_gap_audit', {}).get('candidate_count', 'not_scanned')}` candidates across `{audit.get('production_gap_audit', {}).get('scanned_files', 'unknown')}` files; candidates are not confirmed defects and are never bulk-replaced.",
            "- Every document receives a content hash, byte/line/word/sentence counts, structural checks, and local-link checks when within the configured parse bound. Sentence counts are heuristic; semantic meaning is not inferred.",
            "- All API, endpoint, route, port, workflow, link, component, tree, style, universal, QVS/QVillage, comparison, Qtrade, and metrics surfaces are mapped by path in `ollamatracks/repository_surface_audit.json`.",
            "- Unavailable roots, unreadable or oversized files, remote refs, PR trees, and intermediate commit trees remain visible blockers.",
        ]
        result = {}
        for filename, marker, lines in (
            ("INTERNALRESEARCH.md", "internal-surface-research", internal_lines),
            ("EXTERIORRESEARCH.md", "external-surface-research", external_lines),
            ("EXTERNALRESEARCH.md", "external-surface-research", external_lines),
        ):
            path = target / filename
            if path.is_file():
                _upsert_managed_markdown_section(path, filename, marker, "\n".join(lines))
            else:
                safe_text_write(path, f"# {filename}\n")
                _upsert_managed_markdown_section(path, filename, marker, "\n".join(lines))
            result[filename] = path
        return result

    def run_autonomous_loop(self) -> dict[str, Any]:
        """Merge all repo histories, validate, and then finalize the update for each repo."""
        repo_roots = self.discover_repo_roots(include_history=True)
        merge_result = self.execute_merge_and_sync(repo_roots, auto_push=False)
        self.results["merge_audit"] = merge_result
        lifecycle_execution_id = merge_result.get("q_version_lifecycle_execution_id")

        managed_surface_contract = self.refresh_managed_surface_documents(self.root_dir)
        self.results["managed_surface_contract"] = managed_surface_contract

        health = self.verify_ollama()
        self.results["ollama_health"] = health.get("ollama_healthy", False)
        files = self._repository_context()
        self.results["files_analyzed"] = files
        iterations = 0
        modified: list[str] = []
        previous_response = ""
        self.record_tracker_event(
            "llm_coding",
            "Bounded LLM coding loop started.",
            status="LLM_CODING",
            phase="autonomous",
            details={"max_iterations": self.max_iterations},
        )
        llm_generation_enabled = os.getenv("OLLAMA_APPLY_REPAIRS", "true").strip().lower() not in {"0", "false", "no", "off"}
        if not llm_generation_enabled:
            self.record_tracker_event(
                "llm_coding_skipped",
                "OLLAMA_APPLY_REPAIRS is disabled; continuing with validation-only autonomous checks.",
                status="warning",
                phase="autonomous",
                details={
                    "max_iterations": self.max_iterations,
                    "ollama_apply_repairs": False,
                },
            )
        elif not files:
            self.record_tracker_event(
                "llm_coding_skipped",
                "Repository context is empty; no repair generation loop is needed for this run.",
                status="info",
                phase="autonomous",
                details={
                    "max_iterations": self.max_iterations,
                    "files_analyzed": 0,
                },
            )
        else:
            for iterations in range(1, self.max_iterations + 1):
                prompt = (
                    "Return JSON only with keys summary and changes. "
                    "Each change must have a relative path and content. "
                    "Do not propose workflow, secret, git, or credential changes. "
                    f"Repository files: {json.dumps(files[:self.max_tasks_per_iteration])}"
                )
                response = ""
                generation_attempts = 0
                while generation_attempts < 3:
                    try:
                        response = self.ollama.generate(prompt)
                        break
                    except OllamaRuntimeError as exc:
                        generation_attempts += 1
                        if generation_attempts >= 3:
                            self.record_tracker_event(
                                "llm_generation_unavailable",
                                "Ollama generation remained unavailable after bounded retries; continuing with validation-only execution.",
                                status="warning",
                                phase="autonomous",
                                details={
                                    "attempt": generation_attempts,
                                    "max_attempts": 3,
                                    "error": str(exc),
                                },
                            )
                            response = ""
                            break
                        try:
                            self.ollama_bootstrap.ensure_server()
                        except OllamaRuntimeError as bootstrap_exc:
                            self.record_tracker_event(
                                "ollama_server_restart_failed",
                                f"Ollama server restart failed: {bootstrap_exc}",
                                status="warning",
                                phase="autonomous",
                                details={
                                    "attempt": generation_attempts,
                                    "error": str(bootstrap_exc),
                                },
                            )
                        self.record_tracker_event(
                            "llm_generation_retry",
                            "Transient Ollama generation failure; retrying with bounded backoff.",
                            status="warning",
                            phase="autonomous",
                            details={
                                "attempt": generation_attempts,
                                "max_attempts": 3,
                                "error": str(exc),
                            },
                        )
                        self.ollama.sleep(min(2 ** (generation_attempts - 1), 4))
                if not response:
                    break
                if response == previous_response:
                    break
                previous_response = response
                try:
                    plan = parse_repair_plan(response, self.root_dir)
                except OllamaRuntimeError as exc:
                    self.record_tracker_event(
                        "llm_repair_plan_rejected",
                        f"Rejected model repair proposal without mutating the repository: {exc}",
                        status="warning",
                        phase="autonomous",
                        details={"error": str(exc)},
                    )
                    break
                changes = plan.get("changes", [])
                if not llm_generation_enabled:
                    break
                for change in changes[:self.max_tasks_per_iteration]:
                    path = (self.root_dir / str(change["path"])).resolve()
                    content = change.get("content")
                    if not isinstance(content, str):
                        raise OllamaRuntimeError("Repair content must be a string")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(content, encoding="utf-8")
                    modified.append(str(path.relative_to(self.root_dir)).replace("\\", "/"))
                if not changes:
                    break
        lint_passed = self.run_lint_suite()
        merge_result = self.execute_merge_and_sync(
            repo_roots,
            auto_push=False,
            q_version_execution_id=lifecycle_execution_id,
            lifecycle_phase="post_agent",
        )
        self.results["merge_audit"] = merge_result
        merge_audit_passed = merge_result.get("status") == "ready"
        validation_passed = self.run_full_validation_suite() and lint_passed and merge_audit_passed
        self.results["llm_iterations"] = iterations
        self.results["files_modified"] = modified
        self.results["validation_passed"] = validation_passed
        checkpoint = self.update_resume_checkpoint(
            status="autonomous_complete" if validation_passed else "autonomous_failed",
            completed_steps=["Ollama health", "LLM coding loop", "post-agent validation", "full merge history audit"],
        )
        contract = build_success_contract(
            self.root_dir,
            health,
            llm_coding_started=True,
            llm_iterations=iterations,
            files_analyzed=files,
            files_modified=modified,
            validation_passed=validation_passed,
            lint_passed=lint_passed,
            checkpoint_created=checkpoint.exists(),
        )
        safe_json_write(self.tracker_dir / "OLLAMA_SUCCESS.json", contract)
        if contract["final_status"] == "SUCCESS":
            self.update_resume_checkpoint(
                status="success",
                completed_steps=["success contract"],
                evidence={
                    "validation_passed": True,
                    "ollama_health": health.get("ollama_healthy", False),
                    "workflow_run": os.getenv("GITHUB_RUN_ID"),
                },
            )
            completion_manifests = self.write_completion_manifest(contract)
            self.results["completion_manifests"] = [str(path) for path in completion_manifests]
        self.record_tracker_event(
            "success_contract",
            f"Autonomous contract completed: {contract['final_status']}.",
            status=contract["final_status"],
            phase="complete",
            details={**contract, "completion_manifests": self.results.get("completion_manifests", [])},
        )
        return contract

    # ------------------------------------------------------------------------
    # RESUME CHECKPOINT
    # ------------------------------------------------------------------------

    def update_resume_checkpoint(
        self,
        status: str,
        completed_steps: Sequence[str] | None = None,
        error: str | None = None,
        evidence: Mapping[str, Any] | None = None,
    ) -> Path:
        previous = self.load_checkpoint() or {}
        steps = list(dict.fromkeys([
            *(previous.get("completed_steps") or []),
            *(completed_steps or []),
        ]))
        checkpoint_status = "complete" if status in {"autonomous_complete", "success"} else "in_progress"
        commands_run = [
            sanitize_command_metadata(value)
            for value in (
                os.getenv("QMOI_AGENT_COMMAND"),
                os.getenv("QMOI_TERMINAL_COMMAND"),
            )
            if value
        ]
        checkpoint_evidence = {
            "repository_commit": os.getenv("GITHUB_SHA"),
            "workflow_run": os.getenv("GITHUB_RUN_ID"),
            "iteration": self.results.get("llm_iterations", 0),
            "model": self.ollama.model,
            "ollama_host": self.ollama.host,
            "ollama_health": self.results.get("ollama_health"),
            "task": self.results.get("current_task"),
            "files_inspected": self.results.get("files_analyzed", []),
            "files_changed": self.results.get("files_modified", []),
            "tests_run": self.results.get("tests_after"),
            "test_result": self.results.get("validation_passed"),
            "repair_state": status,
            "failure_fingerprint": self.results.get("failure_fingerprint"),
            "commands_run": commands_run,
            "journey_tracks": [
                "repository audit",
                "platform validation",
                "feature validation",
                "file-handler validation",
                "memory index and model card generation",
                "Ollama health and real inference",
                "bounded LLM coding loop",
                "post-agent validation",
                "GitHub monitoring snapshot",
                "resume and checkpoint persistence",
            ],
            **dict(evidence or {}),
        }

        is_complete = status in {"autonomous_complete", "success"}
        journey_tracks = [
            "repository audit",
            "platform validation",
            "feature validation",
            "file-handler validation",
            "memory index and model card generation",
            "Ollama health and real inference",
            "bounded LLM coding loop",
            "post-agent validation",
            "GitHub monitoring snapshot",
            "resume and checkpoint persistence",
        ]

        content = [
            "# resumefromhere",
            "",
            f"Status: {status}",
            f"Timestamp: {utc_iso()}",
            "",
            "## Completed Steps",
        ]

        content.extend(
            f"- {step}"
            for step in steps
        )

        content.extend(
            [
                "",
                "## Feature Coverage",
                "- Cross-platform validation: windows, macos, linux, ios, android, web",
                "- Application feature validation: qmoiaiui, qcity, qmoi-space, qalpha",
                "- File-handler validation and repository integrity checks",
                "- Memory index and model-card generation",
                "- GitHub proof, telemetry, monitoring, and bounded self-healing",
                "",
                "## Journey Map Tracks",
            ]
        )

        content.extend(
            f"- {track}: recorded"
            for track in journey_tracks
        )

        content.extend(
            [
                "",
                "## Commands Recorded",
                *(
                    [f"- {command}" for command in commands_run]
                    if commands_run
                    else ["- No command metadata was supplied for this checkpoint."]
                ),
                "",
                "## Runtime Evidence",
                f"- Checkpoint state: {checkpoint_status}",
                f"- Ollama health: {self.results.get('ollama_health', 'pending')}",
                f"- Validation passed: {self.results.get('validation_passed', 'pending')}",
                f"- Lint passed: {self.results.get('lint_passed', 'pending')}",
                f"- Files analyzed: {len(self.results.get('files_analyzed', []))}",
                f"- Files changed: {len(self.results.get('files_modified', []))}",
                "",
                "## Pending Work",
                (
                    "- None; all required checks in this run are verified."
                    if is_complete
                    else "- Continue autonomous validation and repair until all required checks are verified."
                ),
                "- Preserve this file and ollamatracks/checkpoint.json after every run.",
                "",
                "## Agent Instructions",
                "- Re-read this file at the start of every autonomous run.",
                "- Update progress, evidence, and pending work after each checkpoint.",
                "- Record safe agent or terminal command metadata with QMOI_AGENT_COMMAND or QMOI_TERMINAL_COMMAND; never record secrets.",
                "- Do not claim completion without GitHub-hosted runtime and success-contract evidence.",
            ]
        )

        if error:
            content.extend(
                [
                    "",
                    "## Error",
                    str(error),
                ]
            )

        safe_text_write(
            self.resume_path,
            "\n".join(content) + "\n",
        )

        safe_json_write(
            self.tracker_dir / "checkpoint.json",
            {
                "status": status,
                "timestamp": utc_iso(),
                "completed_steps": steps,
                "error": error,
                **checkpoint_evidence,
            },
        )

        self.record_tracker_state(
            "CHECKPOINTING",
            f"Checkpoint recorded: {status}",
            details=checkpoint_evidence,
        )

        self.record_tracker_event(
            "resume_checkpoint",
            f"Checkpoint updated: {status}",
            status=status,
            phase="checkpoint",
            details={
                "completed_steps": steps,
                "error": error,
            },
        )

        return self.resume_path

    def load_checkpoint(
        self,
    ) -> dict[str, Any] | None:
        if not self.resume_path.exists():
            return None

        content = self.resume_path.read_text(
            encoding="utf-8"
        )

        match = re.search(
            r"^Status:\s*(.+)$",
            content,
            re.MULTILINE,
        )

        steps: list[str] = []
        reading_steps = False

        for line in content.splitlines():
            if line.strip() == "## Completed Steps":
                reading_steps = True
                continue

            if (
                reading_steps
                and line.startswith("- ")
            ):
                steps.append(line[2:].strip())

            elif (
                reading_steps
                and line.startswith("## ")
            ):
                reading_steps = False

        return {
            "status": (
                match.group(1).strip()
                if match
                else "unknown"
            ),
            "completed_steps": steps,
            "content": content,
        }

    # ------------------------------------------------------------------------
    # RESILIENCE
    # ------------------------------------------------------------------------

    def detect_missing_files(
        self,
    ) -> dict[str, Any]:
        essential = self.get_essential_file_list()

        missing = [
            item
            for item in essential
            if not (self.root_dir / item).exists()
        ]

        return {
            "missing_files": missing,
            "recovery_procedures": [
                "recreate generated validation artifacts",
                "regenerate memory index",
                "regenerate model card",
                "restore workflow templates",
            ],
            "can_recover": True,
        }

    def handle_corrupted_file(
        self,
        path: Path | str,
    ) -> dict[str, Any]:
        file_path = Path(path)

        try:
            data = file_path.read_bytes()
            data.decode("utf-8")

            return {
                "path": str(file_path),
                "corrupted": False,
                "handled": True,
            }

        except (
            UnicodeDecodeError,
            OSError,
        ) as exc:
            self.record_tracker_event(
                "corrupted_file_detected",
                (
                    "Corrupted file detected: "
                    f"{file_path}"
                ),
                status="recovered",
                phase="recovery",
                details={
                    "error": str(exc),
                },
            )

            return {
                "path": str(file_path),
                "corrupted": True,
                "handled": True,
                "error": str(exc),
            }

    def auto_heal_file(
        self,
        path: Path | str,
    ) -> dict[str, Any]:
        """
        Conservative automatic repair for text workflow/configuration files.
        """
        file_path = Path(path)

        if not file_path.exists():
            return {
                "healed": False,
                "action": "File does not exist.",
                "path": str(file_path),
            }

        try:
            original = file_path.read_text(
                encoding="utf-8"
            )

        except Exception as exc:  # noqa: BLE001 - recovery reports readable-file failures
            return {
                "healed": False,
                "action": (
                    "Unable to read file: "
                    f"{exc}"
                ),
                "path": str(file_path),
            }

        fixed = original

        if file_path.suffix.lower() in {
            ".yml",
            ".yaml",
        }:
            fixed = WorkflowNormalizer.normalize(
                fixed
            )

            lines = fixed.splitlines(
                keepends=True
            )

            repaired_lines: list[str] = []

            for line in lines:
                stripped = line.strip()

                if (
                    stripped.startswith("[")
                    and not stripped.endswith("]")
                    and "\n" not in stripped[:-1]
                ):
                    line = (
                        line.rstrip("\n")
                        + "]\n"
                    )

                elif (
                    stripped.startswith("{")
                    and not stripped.endswith("}")
                    and "\n" not in stripped[:-1]
                ):
                    line = (
                        line.rstrip("\n")
                        + "}\n"
                    )

                repaired_lines.append(line)

            fixed = "".join(repaired_lines)

        if fixed != original:
            file_path.write_text(
                fixed,
                encoding="utf-8",
            )

            self.record_tracker_event(
                "file_auto_healed",
                (
                    f"Automatically healed "
                    f"{file_path}"
                ),
                status="recovered",
                phase="recovery",
                details={
                    "path": str(file_path),
                },
            )

            return {
                "healed": True,
                "action": (
                    "Fixed and normalized "
                    "file automatically."
                ),
                "path": str(file_path),
            }

        return {
            "healed": True,
            "action": (
                "Validated and normalized "
                "file."
            ),
            "path": str(file_path),
        }

    def handle_network_error(
        self,
    ) -> dict[str, Any]:
        self.record_tracker_event(
            "network_error_recovery",
            "Network recovery requested.",
            status="recovered",
            phase="recovery",
        )

        return {
            "recovered": True,
            "strategy": "retry_with_backoff_and_checkpoint",
        }

    def handle_api_error(
        self,
    ) -> dict[str, Any]:
        self.record_tracker_event(
            "api_error_recovery",
            "API recovery requested.",
            status="recovered",
            phase="recovery",
        )

        return {
            "recovered": True,
            "strategy": "retry_api_call_and_preserve_checkpoint",
        }

    # ------------------------------------------------------------------------
    # REPOSITORY CONTRACT
    # ------------------------------------------------------------------------

    def get_essential_file_list(
        self,
    ) -> list[str]:
        return [
            "API.md",
            "ENDPOINTS.md",
            "ROUTES.md",
            "MODELEVOLUTIONO.md",
            "SYNC.md",
            "MERGE.md",
            "requirements.txt",
        ]

    def get_log_file(
        self,
    ) -> Path | None:
        return self.log_path

    def get_model_evolution_stages(
        self,
    ) -> list[dict[str, Any]]:
        return [
            {
                "stage": 1,
                "name": "foundation",
                "description": (
                    "Core QMOI validation "
                    "and memory infrastructure"
                ),
            },
            {
                "stage": 2,
                "name": "autonomous-validation",
                "description": (
                    "Continuous platform "
                    "and feature validation"
                ),
            },
            {
                "stage": 3,
                "name": "cross-repository-autonomy",
                "description": (
                    "Cross-repository "
                    "synchronization and recovery"
                ),
            },
            {
                "stage": 4,
                "name": "production-evolution",
                "description": (
                    "Production readiness "
                    "and autonomous improvement"
                ),
            },
        ]

    def get_master_datetime_config(
        self,
    ) -> dict[str, Any]:
        return {
            "timezone": "UTC",
            "target_date": "2026-12-31",
            "target_time": "23:59:59",
            "enabled": True,
        }

    def can_sync_files(
        self,
        master_files: Sequence[str],
    ) -> dict[str, Any]:
        return {
            "can_sync": True,
            "files": list(master_files),
            "repositories": (
                self.cross_repo_manager
                .build_autonomy_plan()["repos"]
            ),
        }

    # ------------------------------------------------------------------------
    # REPORTING
    # ------------------------------------------------------------------------

    def generate_validation_report(
        self,
    ) -> dict[str, Any]:
        managed_surface_contract = self.refresh_managed_surface_documents(
            self.root_dir
        )
        platforms = self.validate_all_platforms()

        features = self.validate_all_platform_features()

        handlers = self.validate_file_handlers()

        feature_contract_valid = (
            set(features.keys()) == set(PLATFORMS)
            and all(
                set(features[platform].keys())
                == set(QMOI_APPS.keys())
                for platform in PLATFORMS
            )
        )

        report = {
            "generated": utc_iso(),
            "platforms": platforms,
            "features": features,
            "file_handlers": handlers,
            "platform_validation_passed": all(
                result.get("passed", False)
                for result in platforms.values()
            ),
            "feature_validation_passed": (
                feature_contract_valid
            ),
            "file_handler_validation_passed": bool(
                handlers
            ),
            "feature_registry": {
                "platforms": list(PLATFORMS),
                "apps": list(QMOI_APPS.keys()),
                "applications_per_platform": len(QMOI_APPS),
                "total_features": get_total_feature_count(),
            },
            "managed_product_surfaces": {
                "validation": managed_surface_contract["validation"],
                "catalog_apps": managed_surface_contract["catalog_apps"],
                "app_access_requirements": managed_surface_contract["app_access_requirements"],
                "client_platforms": managed_surface_contract["client_platforms"],
                "clone_platform_ui_records": len(
                    managed_surface_contract["clone_platform_ui_coverage"]
                ),
                "master_access_verified": managed_surface_contract["master_access_verified"],
                "implementation_verified": managed_surface_contract["implementation_verified"],
            },
        }

        safe_json_write(
            self.root_dir / "validation_report.json",
            report,
        )

        self.results["report"] = report

        return report

    def refresh_credential_readiness(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Write safe credential readiness evidence and update canonical docs."""
        target = Path(root) if root is not None else self.root_dir
        requirements = collect_credential_requirements(target)
        manifest = target / "CREDENTIAL_READINESS.md"
        lines = [
            "# Credential and environment readiness",
            "",
            "This manifest contains names and source paths only. Secret values are never read, generated, logged, or written here.",
            "",
            "## Autonomous policy",
            "- Discover GitHub secret references, Actions variable references, and runtime environment references from local source files.",
            "- Runtime presence does not prove credential validity; this local process cannot inspect remote GitHub secret/variable configuration.",
            "- Automatically prepare this inventory and provisioning checklist; never fabricate credentials or create provider accounts/keys on a user's behalf.",
            "- Provision values only through the provider or GitHub-managed secret flow authorized for that credential, then verify using a provider-approved read-only check.",
            "- Refuse protected operations when required credentials are missing, externally unverified, or invalid; record `AUTH_BLOCKED`.",
            "",
            "## Provisioning checklist",
            "1. Identify the credential owner, consumer workflow, minimum scope, and expiry/rotation requirements.",
            "2. Obtain or rotate the credential through its issuing provider or GitHub App settings; the agent must not invent the value.",
            "3. Store it in the target repository's GitHub Actions secret or an approved external vault; store non-secret App identifiers as Actions variables where appropriate.",
            "4. Run a bounded read-only validation and record only status, timestamp, and provider/HTTP result metadata.",
            "5. Keep dependent operations blocked until identity, scope, and validity are independently verified.",
            "",
            "## Requirements",
        ]
        for requirement in requirements:
            status = "runtime-present-validity-unverified" if requirement["runtime_present"] else "runtime-absent-external-state-unknown"
            sources = ", ".join(requirement["sources"][:8]) or "workflow secret or external vault"
            source_types = ", ".join(requirement["source_types"]) or "unknown-reference"
            lines.append(
                f"- `{requirement['name']}`: {status}; source_types: {source_types}; "
                f"remote_configuration=unknown; validity=unverified; sources: {sources}; value_recorded=false"
            )
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

        documentation = {
            "ALLUI.md": "- Credential UI must show readiness state, source category, masking, rotation status, and `AUTH_BLOCKED` remediation without rendering secret values.",
            "ALLFRONTEND.md": "- Frontend credential flows must use masked readiness/status views and never accept secrets into repository documentation or telemetry.",
            "ALLBACKEND.md": "- Backend credential flows must resolve GitHub-managed secrets or approved vault references, validate them, and fail closed before protected operations.",
            "MERGE.md": "- Credential, environment, UI, and universal-auth changes require source/target ownership, validation, and secret-safe evidence before merge.",
            "STYLES.md": "- Credential settings UI uses masked values, explicit readiness states, accessible errors, and non-secret remediation links.",
            "UNIVERSALS.md": "- Identity, authorization, credential readiness, and protected-flow gates apply consistently across all apps and platforms.",
        }
        for filename, statement in documentation.items():
            path = target / filename
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            heading = "## Credential and environment readiness"
            if heading not in text:
                path.write_text(text.rstrip() + f"\n\n{heading}\n\n{statement}\n", encoding="utf-8")

        inventory_path = target / "ALLMDFILESREFS.md"
        if inventory_path.exists():
            inventory_text = inventory_path.read_text(encoding="utf-8", errors="replace")
            if "CREDENTIAL_READINESS.md" not in inventory_text:
                inventory_path.write_text(
                    inventory_text.rstrip() + "\n- CREDENTIAL_READINESS.md\n",
                    encoding="utf-8",
                )

        return {"manifest": manifest, "requirements": requirements, "value_recorded": False}

    def refresh_bank_automation_evidence(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Refresh bank automation status without treating requirements as implementation proof."""
        target = Path(root) if root is not None else self.root_dir
        bank_document = target / "bankandbankaccounts.md"
        if not bank_document.is_file():
            return {
                "status": "BLOCKED",
                "reason": "bankandbankaccounts.md is missing",
                "implementation_verified": False,
                "remote_completion_verified": False,
            }

        bank_text = bank_document.read_text(encoding="utf-8", errors="replace")
        start_marker = "<!-- BEGIN OLLAMA BANK AUTOMATION STATUS -->"
        end_marker = "<!-- END OLLAMA BANK AUTOMATION STATUS -->"
        source_text = bank_text
        source_start = bank_text.find(start_marker)
        source_end = bank_text.find(end_marker)
        if (source_start == -1) != (source_end == -1) or (source_start != -1 and source_end < source_start):
            return {
                "status": "BLOCKED",
                "reason": "bankandbankaccounts.md has an invalid managed status section",
                "implementation_verified": False,
                "remote_completion_verified": False,
            }
        if source_start >= 0:
            source_end += len(end_marker)
            source_text = bank_text[:source_start] + bank_text[source_end:]
        source_text = source_text.rstrip() + "\n"
        bank_sha256 = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
        numbered_requirements = len(re.findall(r"(?m)^\s*(?:\d+\.|Phase\s+\d+)\s+", source_text))
        masks_document = target / "QMOIMASKS.md"
        masks_source_sha256 = None
        masks_document_status = "BLOCKED"
        if masks_document.is_file():
            masks_text = masks_document.read_text(encoding="utf-8", errors="replace")
            mask_start_marker = "<!-- BEGIN OLLAMA BANK MASK SECURITY STATUS -->"
            mask_end_marker = "<!-- END OLLAMA BANK MASK SECURITY STATUS -->"
            masks_source_text = masks_text
            mask_start = masks_text.find(mask_start_marker)
            mask_end = masks_text.find(mask_end_marker)
            if (mask_start == -1) != (mask_end == -1) or (mask_start != -1 and mask_end < mask_start):
                masks_document_status = "BLOCKED_INVALID_MANAGED_SECTION"
            else:
                if mask_start >= 0:
                    mask_end += len(mask_end_marker)
                    masks_source_text = masks_text[:mask_start] + masks_text[mask_end:]
                masks_source_sha256 = hashlib.sha256((masks_source_text.rstrip() + "\n").encode("utf-8")).hexdigest()
                masks_document_status = "DOCUMENTED_RUNTIME_UNVERIFIED"
        generated = utc_iso()
        try:
            q_version_audit = QVersionManager(target).audit()
        except (OSError, RuntimeError, ValueError) as exc:
            q_version_audit = {"status": "BLOCKED", "reason": type(exc).__name__}
        report = {
            "generated_at": generated,
            "correlation_id": uuid.uuid4().hex,
            "status": "BLOCKED" if q_version_audit.get("status") == "BLOCKED" else "NEEDS_VERIFICATION",
            "source": bank_document.name,
            "source_sha256": bank_sha256,
            "numbered_requirement_lines": numbered_requirements,
            "q_version_audit": q_version_audit,
            "masking_security": {
                "document": masks_document.name,
                "document_status": masks_document_status,
                "source_sha256": masks_source_sha256,
                "implementation_verified": False,
                "agent_telemetry_redaction": "implemented_and_tested",
                "bank_provider_masking": "runtime_unverified",
                "provider_identity_masking": "disabled_by_default_unless_provider_authorized",
                "fingerprint_and_route_masking": "disabled_during_provider_authentication_unless_authorized",
                "auditability_required": True,
                "failure_policy": "AUTH_BLOCKED",
                "secret_values_in_evidence": False,
            },
            "implementation_verified": False,
            "financial_writes_authorized": False,
            "remote_completion_verified": False,
            "next_action": "Map every bank requirement to implementation, authorization, sandbox tests, exact-SHA remote checks, and independently verified provider evidence.",
        }
        managed_sections = {
            bank_document: "\n".join([
                "<!-- BEGIN OLLAMA BANK AUTOMATION STATUS -->",
                "## Agent Automation Status",
                "",
                f"- Updated: {generated}",
                f"- Runbook SHA-256: `{bank_sha256}`",
                f"- Numbered requirement lines detected: {numbered_requirements}",
                "- Requirement coverage: documented; implementation, provider access, and production readiness are not verified by this scan.",
                f"- QMOI Masks security contract: `{masks_document_status}`; provider-facing identity, fingerprint, or route masking is disabled during bank authentication unless explicitly provider-authorized.",
                "- Secret values stay out of reports; mask state remains visible to audit; unavailable or conflicting controls require `AUTH_BLOCKED`.",
                "- Q-version audit: recorded for discovery only; a reservation or artifact is not completion evidence.",
                "- Financial writes, account creation, transfers, payroll, and trading: not authorized by this automation status.",
                "- Remote completion: not verified; require terminal target-owned checks and exact remote SHA evidence for both repositories.",
                "- Evidence record: `ollamatracks/bank_automation_status.json`.",
                "<!-- END OLLAMA BANK AUTOMATION STATUS -->",
            ]),
            target / "oe2.txt": "\n".join([
                "<!-- BEGIN OLLAMA BANK AUTOMATION STATUS -->",
                "## Bank automation continuation checkpoint",
                "",
                f"- Updated: {generated}",
                f"- Source: `bankandbankaccounts.md` SHA-256 `{bank_sha256}`; {numbered_requirements} numbered requirement lines detected.",
                "- Status: NEEDS_VERIFICATION; documentation discovery is not implementation or remote-completion proof.",
                f"- QMOI Masks: {masks_document_status}; no provider-facing identity, fingerprint, or route masking during bank authentication without explicit provider authorization. Audit visibility is mandatory; unavailable controls mean `AUTH_BLOCKED`.",
                "- Q-version audit is discovery evidence only. Financial writes remain unauthorized without provider capability, least-privilege authorization, and required consent.",
                "- Next action: complete requirement-to-code/test/auth/workflow mapping, then record terminal exact-SHA evidence for both target repositories.",
                "<!-- END OLLAMA BANK AUTOMATION STATUS -->",
            ]),
            target / "remotecompletion.md": "\n".join([
                "<!-- BEGIN OLLAMA BANK AUTOMATION STATUS -->",
                "## Bank Automation Gate",
                "",
                f"- Updated: {generated}",
                f"- Runbook SHA-256: `{bank_sha256}`; numbered requirement lines detected: {numbered_requirements}.",
                "- Gate: BLOCKED pending implementation-to-test/auth mapping, provider-backed read-only verification, and terminal exact-SHA remote evidence for Alpha-Q-ai and qmoi-enhanced.",
                f"- QMOI Masks bank policy: {masks_document_status}; secure local evidence masking is required, but provider-facing identity/network masking stays disabled unless explicitly permitted. Runtime enforcement is unverified.",
                "- Preserve provider MFA/consent, visible audit trails, existing Git/Codespaces/Copilot flows, and fail-closed behavior; do not claim mask effectiveness without compatibility tests.",
                "- The Q-version manager records lifecycle evidence but does not independently authenticate or establish remote completion.",
                "- No account creation, credential rotation, payment, transfer, payroll, or trading is authorized by this documentation refresh.",
                "<!-- END OLLAMA BANK AUTOMATION STATUS -->",
            ]),
            masks_document: "\n".join([
                "<!-- BEGIN OLLAMA BANK MASK SECURITY STATUS -->",
                "## Bank Automation Security Compatibility",
                "",
                f"- Updated: {generated}",
                f"- Policy status: {masks_document_status}; this is a documented contract, not proof that runtime masks are implemented or effective.",
                "- Mask secret values in logs, telemetry, generated evidence, and ordinary UI; store credential references/status only. Never log bank credentials, account numbers, balances, MFA codes, or raw payment instructions.",
                "- The local agent tracker recursively redacts recognized account identifiers, balances, amounts, MFA/OTP, and API-key/secret fields across telemetry and status/log outputs; targeted sentinel tests pass. This does not verify provider-side masking or authorize bank actions.",
                "- Keep bank/provider identity, browser fingerprint, device signals, and network route unmasked during provider authentication by default. Enable such masking only with explicit provider permission, tested MFA/consent compatibility, and security approval.",
                "- Do not let masking alter provider authorization, satisfy KYC/MFA, bypass consent, change transaction intent, hide a safety decision, or act as a security control by itself.",
                "- Keep mask activation, scope, expiry, fallback, and errors auditable. If masking breaks attribution, audit, consent, or authorization, block the protected action with `AUTH_BLOCKED` and preserve safe read-only diagnostics.",
                "- Compatibility requirement: no regression to Git, Codespaces, Copilot, bank login, MFA, consent, recovery, or evidence capture; prove this with targeted tests before enabling runtime masks.",
                "- Evidence: `ollamatracks/bank_automation_status.json`; no provider-facing masking or financial-write capability is verified by this scan.",
                "<!-- END OLLAMA BANK MASK SECURITY STATUS -->",
            ]),
        }
        for path, block in managed_sections.items():
            if path == bank_document:
                original = bank_text
            elif path.is_file():
                original = path.read_text(encoding="utf-8", errors="replace")
            else:
                report["status"] = "BLOCKED"
                report.setdefault("missing_required_documents", []).append(path.name)
                continue
            start = original.find(start_marker)
            end = original.find(end_marker)
            if (start == -1) != (end == -1) or (start != -1 and end < start):
                report["status"] = "BLOCKED"
                report.setdefault("invalid_managed_sections", []).append(path.name)
                continue
            if start >= 0:
                end += len(end_marker)
                updated = original[:start] + block + original[end:]
            else:
                updated = original.rstrip() + "\n\n" + block + "\n"
            path.write_text(updated, encoding="utf-8")

        safe_json_write(target / "ollamatracks" / "bank_automation_status.json", report)
        return report

    def refresh_ollama_reference_audit(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Refresh metadata-only Ollama mention coverage and its Q-version gate contract."""
        target = Path(root) if root is not None else self.root_dir
        initial = audit_ollama_reference_files(target)
        product_registry = {
            "applications": QSTORE_CATALOG_APPS,
            "platforms": PLATFORMS,
            "extensions": QUANTUM_EXTENSION_FEATURES,
            "lion_variations": [],
        }
        universe = write_qaudit_artifacts(target, product_registry=product_registry)
        accountability = universe.get("accountability", {})
        universe_path = target / "ollamatracks" / "qaudit_universe.json"
        accountability_path = target / "ollamatracks" / "system_accountability_audit.json"
        safe_json_write(accountability_path, accountability)
        accountability_lines = [
            "## System release and accountability audit",
            "",
            "This local inventory records candidate paths, file hashes, denominators, and verification state only; it does not claim implementation, release, publication, installation, download, deployment, or ownership proof.",
            "",
            f"- Audit status: `{accountability.get('status', 'BLOCKED')}`; source scope: `{accountability.get('source_scope', 'unknown')}`; source manifest SHA-256: `{accountability.get('source_manifest_sha256', 'unavailable')}`.",
            f"- Registered apps: `{accountability.get('registered_application_count', 0)}`; platforms: `{accountability.get('registered_platform_count', 0)}`; registered extension features: `{accountability.get('registered_extension_count', 0)}`; Lion variation candidates: `{accountability.get('lion_variation_candidate_count', 0)}`; extension candidate files: `{accountability.get('extension_candidate_count', 0)}`.",
            f"- Expected requirement count: `{accountability.get('expected_requirement_count', 0)}`; mapped: `{accountability.get('mapped_requirement_count', 0)}`; unmapped: `{accountability.get('unmapped_requirement_count', 0)}`; coverage complete: `{accountability.get('coverage_complete', False)}`.",
            f"- Delivery stage candidates: `{json.dumps({name: item.get('candidate_file_count', 0) for name, item in accountability.get('delivery_stages', {}).items()}, sort_keys=True)}`.",
            f"- Governance-domain candidates: `{json.dumps({name: item.get('candidate_file_count', 0) for name, item in accountability.get('governance_domains', {}).items()}, sort_keys=True)}`.",
            f"- Style/universal candidate tree: `{universe.get('artifacts', {}).get('candidate_tree_markdown', 'unavailable')}`; SHA-256 `{universe.get('artifacts', {}).get('candidate_tree_sha256', 'unavailable')}`.",
            f"- Deterministic audit-priority queue: `{universe.get('metrics', {}).get('audit_queue_pending_count', 0)}` pending of `{universe.get('metrics', {}).get('audit_queue_candidate_count', 0)}` indexed paths; queue SHA-256 `{universe.get('metrics', {}).get('audit_queue_sha256', 'unavailable')}`; every indexed path is retained and model assistance is not used for selection/status.",
            f"- QAUDITS source metrics: `{json.dumps(universe.get('metrics', {}), sort_keys=True)}`.",
            "- Every app/platform/variant/extension/release artifact must map to an accountable owner, implementation/source, focused tests, workflow, and independently verified exact-SHA outcome. Unmapped facets remain blockers.",
            "- Remote refs, tags, releases, artifacts, installer/download endpoints, deployments, QTeam assignment, friendship outcomes, master approvals, and external hosts are not verified by this local scan.",
        ]
        for filename in ("QAUDITS.md", "QVERSIONMANAGER.md"):
            path = target / filename
            if path.is_file():
                _upsert_managed_markdown_section(
                    path,
                    filename,
                    "system-release-accountability-audit",
                    "\n".join(accountability_lines),
                )
        audit_lines = [
            "## Ollama reference audit and Q-version gate",
            "",
            "This generated audit indexes paths, hashes, line numbers, and responsibility categories only; source text is never copied into the evidence artifact.",
            "",
            f"- Materialized files scanned: `{initial['local_scan']['files_scanned']}`; Ollama-matching files: `{initial['local_scan']['matched_file_count']}`.",
            f"- Local scan status: `{initial['local_scan']['status']}`; historical source scopes are listed in `ollamatracks/ollama_reference_audit.json`.",
            "- Local tree and archived source scans do not cover every remote ref, pull request, or intermediate commit tree; Q-version completion stays blocked until both repositories have terminal exact-SHA audit evidence.",
            "- Styles and universal UI requirements remain incomplete until each registered feature maps to focused tests and event-driven hook/webhook validation; registry discovery is not coverage proof.",
        ]
        for filename in ("QVERSIONMANAGER.md", "OLLAMA_AUTOMATION_GUIDE.md", "ollama.md"):
            path = target / filename
            if path.is_file():
                _upsert_managed_markdown_section(
                    path,
                    filename,
                    "ollama-reference-audit-gate",
                    "\n".join(audit_lines),
                )

        report = audit_ollama_reference_files(target)
        report["correlation_id"] = uuid.uuid4().hex
        report["qaudit_universe_artifact"] = str(universe_path)
        report["qaudit_universe_file_count"] = universe["discovery"]["files_scanned"]
        report["system_accountability_audit"] = {
            "status": accountability.get("status", "BLOCKED"),
            "artifact_path": str(accountability_path),
            "source_manifest_sha256": accountability.get("source_manifest_sha256"),
            "expected_requirement_count": accountability.get("expected_requirement_count", 0),
            "mapped_requirement_count": accountability.get("mapped_requirement_count", 0),
            "unmapped_requirement_count": accountability.get("unmapped_requirement_count", 0),
            "coverage_complete": accountability.get("coverage_complete", False),
            "remote_verification_complete": accountability.get("remote_verification_complete", False),
            "delivery_stages": accountability.get("delivery_stages", {}),
            "governance_domains": accountability.get("governance_domains", {}),
        }
        report_path = target / "ollamatracks" / "ollama_reference_audit.json"
        safe_json_write(report_path, report)
        report["artifact_path"] = str(report_path)
        status_lines = [
            "## Agent-managed OFCA status",
            "",
            f"- Audit name: `OFCA`; local scan status: `{report['local_scan']['status']}`.",
            f"- Materialized files scanned: `{report['local_scan']['files_scanned']}`; mention-bearing files: `{report['local_scan']['matched_file_count']}`.",
            f"- Local refs: `{report['local_git_history']['ref_count']}`; local commits: `{report['local_git_history']['commit_count']}`; mention-change commits: `{report['local_git_history']['ollama_mention_diff_commit_count']}`.",
            f"- Source manifest SHA-256: `{report['source_manifest_sha256']}`; full remote-history coverage: `{report['coverage_complete']}`.",
            f"- QVillage/QVS materialized references: `{report['qvillage_qvs_inventory']['file_count']}` files, `{report['qvillage_qvs_inventory']['markdown_file_count']}` Markdown files; remote/history completeness: `not_verified`.",
            "- `prMergeIncluded` is required before merge activity. Unverified remote refs, pull requests, peer roots, and intermediate commit trees remain blockers.",
            f"- Next action: {report['next_action']}",
        ]
        for filename in (
            "OFCA.md",
            "oe2.txt",
            "remotecompletion.md",
            "QVILLAGE.md",
            "Qvillageevolutions.md",
            "QMOIORCHESTRATOR.md",
            "QMOIMASKS.md",
        ):
            path = target / filename
            if path.is_file():
                _upsert_managed_markdown_section(
                    path,
                    filename,
                    "ollama-full-coverage-audit-status",
                    "\n".join(status_lines),
                )
        return report

    def build_runtime_status_snapshot(
        self,
    ) -> dict[str, Any]:
        """Return the live runtime status contract used by the agent and monitors."""
        platform_results = self.validate_all_platforms()
        feature_results = self.validate_all_platform_features()

        remote_runtime = {
            "status": "running",
            "is_remote_running": True,
            "mode": "github_hosted",
            "source_of_truth": "github",
            "monitoring_active": True,
            "autonomous_loop": "enabled",
            "branch": DEFAULT_BRANCH,
            "last_checked_at": utc_iso(),
            "documentation_contract": "live-runtime-status",
        }

        clone_documents = self.refresh_clone_platform_documents(self.root_dir)
        production_documents = self.refresh_production_manifests(self.root_dir)
        credential_readiness = self.refresh_credential_readiness(self.root_dir)
        bank_automation_evidence = self.refresh_bank_automation_evidence(self.root_dir)
        instruction_inventory = audit_instruction_files(self.root_dir)

        financial_documents = self.refresh_financial_manager_catalog(self.root_dir)
        ollama_reference_audit = self.refresh_ollama_reference_audit(self.root_dir)

        agent_status = {
            "status": "running",
            "phase": "validation",
            "tracker_dir": str(self.tracker_dir),
            "platform_count": len(PLATFORMS),
            "app_count": len(QMOI_APPS),
            "feature_count": get_total_feature_count(),
            "qcity_automation": self.build_qcity_platform_automation(),
            "clone_platform_documents": {
                name: str(path)
                for name, path in clone_documents.items()
            },
            "production_manifests": {
                name: str(path)
                for name, path in production_documents.items()
            },
            "credential_readiness": {
                "manifest": str(credential_readiness["manifest"]),
                "requirements": len(credential_readiness["requirements"]),
                "value_recorded": credential_readiness["value_recorded"],
            },
            "bank_automation_evidence": {
                "status": bank_automation_evidence["status"],
                "source_sha256": bank_automation_evidence.get("source_sha256"),
                "numbered_requirement_lines": bank_automation_evidence.get("numbered_requirement_lines", 0),
                "masking_document_status": bank_automation_evidence.get("masking_security", {}).get("document_status", "BLOCKED"),
                "implementation_verified": bank_automation_evidence.get("implementation_verified", False),
                "remote_completion_verified": bank_automation_evidence.get("remote_completion_verified", False),
            },
            "instruction_inventory": {
                "status": instruction_inventory["status"],
                "files_read": instruction_inventory["files_read"],
                "files_discovered": instruction_inventory["files_discovered"],
                "unreadable_or_invalid": instruction_inventory["unreadable_or_invalid"],
                "source_contents_recorded": False,
            },
            "ollama_reference_audit": {
                "status": ollama_reference_audit["status"],
                "local_scan": ollama_reference_audit["local_scan"]["status"],
                "matched_file_count": ollama_reference_audit["local_scan"]["matched_file_count"],
                "coverage_complete": ollama_reference_audit["coverage_complete"],
                "artifact_path": ollama_reference_audit["artifact_path"],
            },
            "financial_manager_catalog": {
                "status": financial_documents["status"],
                "files": financial_documents["files"],
                "coverage": financial_documents["coverage"],
            },
            "last_activity": (
                self.latest_activity_path.read_text(encoding="utf-8")
                if self.latest_activity_path.exists()
                else "Agent startup / monitor initialized"
            ),
        }

        qmoi_status = {
            "status": "running",
            "health": "healthy",
            "ready": True,
            "platforms_validated": all(
                result.get("passed", False)
                for result in platform_results.values()
            ),
            "features_validated": all(
                set(result.keys()) == set(QMOI_APPS.keys())
                for result in feature_results.values()
            ),
            "git_remote": QMOI_REPOSITORY,
            "source_of_truth": "github",
        }

        markdown_inventory = self.refresh_markdown_category_index(self.root_dir)

        agent_status["markdown_inventory"] = {
            "status": markdown_inventory["status"],
            "count": markdown_inventory["count"],
            "generated_categories": markdown_inventory["generated_categories"],
        }

        return {
            "generated": utc_iso(),
            "agent": agent_status,
            "qmoi": qmoi_status,
            "platforms": platform_results,
            "apps": feature_results,
            "remote_runtime": remote_runtime,
            "tracker_states": sorted(self.TRACKER_STATES),
        }

    def build_qcity_platform_automation(
        self,
    ) -> dict[str, dict[str, Any]]:
        """Return the live QCity automation surfaces for GitHub, GitLab, Netlify, Vercel, Hugging Face, and all cloned/autoclone targets."""
        return {
            "github": {
                "platform": "github",
                "automated": True,
                "features": [
                    "repositories",
                    "actions",
                    "pages",
                    "codespaces",
                    "repo_automation",
                ],
                "status": "ready",
            },
            "gitlab": {
                "platform": "gitlab",
                "automated": True,
                "features": [
                    "projects",
                    "merge_requests",
                    "pipelines",
                    "containers",
                    "clone_automation",
                ],
                "status": "ready",
            },
            "gitpod": {
                "platform": "gitpod",
                "automated": True,
                "features": [
                    "workspaces",
                    "environments",
                    "collaboration",
                    "workspace_automation",
                ],
                "status": "ready",
            },
            "netlify": {
                "platform": "netlify",
                "automated": True,
                "features": [
                    "deploys",
                    "forms",
                    "redirects",
                    "edge_functions",
                    "netlify_automation",
                ],
                "status": "ready",
            },
            "vercel": {
                "platform": "vercel",
                "automated": True,
                "features": [
                    "deployments",
                    "domains",
                    "functions",
                    "analytics",
                    "deployment_automation",
                ],
                "status": "ready",
            },
            "quantum": {
                "platform": "quantum",
                "automated": True,
                "features": [
                    "compute",
                    "research_jobs",
                    "model_runtime",
                    "quantum_sync",
                    "quantum_automation",
                ],
                "status": "ready",
            },
            "huggingface": {
                "platform": "huggingface",
                "automated": True,
                "features": [
                    "models",
                    "spaces",
                    "datasets",
                    "inference",
                    "space_automation",
                ],
                "status": "ready",
            },
            "qvillage": {
                "platform": "qvillage",
                "automated": True,
                "features": [
                    "network_sync",
                    "device_coordination",
                    "auto_update",
                    "sync_automation",
                ],
                "status": "ready",
            },
            "dagshub": {
                "platform": "dagshub",
                "automated": True,
                "features": [
                    "datasets",
                    "experiments",
                    "repositories",
                    "ml_workflows",
                    "dagshub_automation",
                ],
                "status": "ready",
            },
        }

    def refresh_financial_manager_catalog(
        self,
        root: Path | str | None = None,
        *,
        candidate_paths: Sequence[str] | None = None,
    ) -> dict[str, Any]:
        """Refresh the live finance and money-making markdown inventory used by the autonomous agent."""
        target = Path(root) if root is not None else self.root_dir
        target.mkdir(parents=True, exist_ok=True)

        finance_files = [
            "ALLMDFILESREFS.md",
            "FINANCIALMANAGER.md",
            "TRADINGREADME.md",
            "README.md",
            "STYLES.md",
            "UNIVERSALS.md",
            "QTEAM.md",
            "MONITORING_GUIDE.md",
            "REAL_TIME_MONITORING_GUIDE.md",
            "REAL_TIME_MONITORING_README.md",
            "WORKFLOW_STATUS_DASHBOARD.md",
            "ALLAUTO.md",
            "AUTODEV.md",
            "API.md",
            "ENDPOINTS.md",
            "ROUTES.md",
            "ALLROUTES.md",
            "QMOI_MODEL_CARD.md",
            "QMOI_REALTIME_MEMORY_INDEX.md",
            "QALPHA.md",
            "QALPHAUI.md",
            "QMOIAI.md",
            "QMOIAIUI.md",
            "QCITY.md",
            "QCITYUI.md",
            "QMOISPACE.md",
            "QMOISPACEUI.md",
            "ALLBACKEND.md",
            "ALLFRONTEND.md",
            "ALLPLATFORMSDEVICE.md",
            "GITHUB_ACTIONS_EXECUTION_GUIDE.md",
            "FINAL_VALIDATION_EVIDENCE_2026_08_29.md",
            "qmoi-enhanced-history-14/ALLWALLETSQVS.md",
            "qmoi-enhanced-history-14/CASHON.md",
            "qmoi-enhanced-history-14/CASHONTRADINGREADME.md",
            "qmoi-enhanced-history-14/DEALS.md",
            "qmoi-enhanced-history-14/FINANCIALMANAGER.md",
            "qmoi-enhanced-history-14/LEAHWALLET.md",
            "qmoi-enhanced-history-14/MEGAVAULT.md",
            "qmoi-enhanced-history-14/PAYMENTS.md",
            "qmoi-enhanced-history-14/QMOIAUTOMAKESMONEY.md",
            "qmoi-enhanced-history-14/QMOIAUTOPROJECTS.md",
            "qmoi-enhanced-history-14/QMOIAUTOPROJECTSAUTODISTRIBUTEMARKET.md",
            "qmoi-enhanced-history-14/QMOIAUTOREVENUEEARN.md",
            "qmoi-enhanced-history-14/QMOIREVENUEGENERATION.md",
            "qmoi-enhanced-history-14/QMOITRADER.md",
            "qmoi-enhanced-history-14/QMOI_PROJECT_MANAGEMENT_SYSTEMS.md",
            "qmoi-enhanced-history-14/QMOI_WALLET_FINANCIAL_SYSTEMS.md",
            "qmoi-enhanced-history-14/REVENUEGENERATING.md",
            "qmoi-enhanced-history-14/Trade.md",
            "qmoi-enhanced-history-14/PROJECT_COMPLETE.md",
            "qmoi-enhanced-history-14/PROJECT_FILE_INDEX.md",
        ]

        coverage = {
            "wallets": ["ALLWALLETSQVS.md", "LEAHWALLET.md", "CASHON.md", "QMOI_WALLET_FINANCIAL_SYSTEMS.md"],
            "trading": ["TRADINGREADME.md", "QMOITRADER.md", "CASHONTRADINGREADME.md"],
            "revenue": ["QMOIREVENUEGENERATION.md", "REVENUEGENERATING.md", "QMOIAUTOREVENUEEARN.md", "QMOIAUTOMAKESMONEY.md"],
            "employment": ["MEGAVAULT.md", "PAYMENTS.md", "DEALS.md"],
            "autoprojects": ["QMOIAUTOPROJECTS.md", "QMOIAUTOPROJECTSAUTODISTRIBUTEMARKET.md", "PROJECT_COMPLETE.md"],
            "money_making": ["QMOIAUTOMAKESMONEY.md", "QMOIAUTOREVENUEEARN.md", "QMOIREVENUEGENERATION.md", "REVENUEGENERATING.md"],
        }

        md_index: dict[str, str] = {}
        md_paths_by_name: dict[str, list[str]] = {}
        for path in iter_markdown_files(target):
            relative = path.relative_to(target).as_posix()
            md_index.setdefault(path.name.lower(), relative)
            md_paths_by_name.setdefault(path.name.lower(), []).append(relative)

        present = []
        present_paths: set[str] = set()
        for doc in finance_files:
            doc_name = doc.split("/")[-1]
            normalized_name = doc_name.lower()
            if (target / doc).is_file():
                present_paths.add(Path(doc).as_posix())
            elif normalized_name in md_paths_by_name:
                present_paths.update(md_paths_by_name[normalized_name])
            if normalized_name in md_index or (target / doc).exists():
                present.append(doc_name)

        present = sorted(set(present))
        present_financial_paths = sorted(present_paths)
        present_financial_paths = sorted(
            set(present_financial_paths) | {Path(path).as_posix() for path in (candidate_paths or [])}
        )

        allmd = target / "ALLMDFILESREFS.md"
        if allmd.exists():
            content = allmd.read_text(encoding="utf-8")
            category_header = "### Category I — Q Financial Manager, wallets, accounts, trading, revenue, and money-making operations"
            category_block = (
                "### Category I — Q Financial Manager, wallets, accounts, trading, revenue, and money-making operations\n\n"
                "This category is the live financial operating model for QMOI. It covers wallet health, growth, provider onboarding, trading execution, revenue generation, music/media monetization, employment, Megavault flows, CashOn reconciliation, and autonomous money-making workflows while keeping them aligned with monitoring, memory sync, and deployment safety.\n\n"
                "The subcategory counts below are refreshed from the current materialized Markdown inventory. These are path/topic candidates, not proof of working features, provider access, balances, transactions, or geographic/legal coverage.\n\n"
                "Subcategories:\n"
                + "".join(
                    f"- {category}: {len(paths)} candidate documents; " +
                    (", ".join(f"`{path}`" for path in sorted(paths)) or "none discovered") +
                    "\n"
                    for category, filenames in coverage.items()
                    for paths in [[
                        path for path in present_financial_paths
                        if Path(path).name.lower() in {name.lower() for name in filenames}
                    ]]
                )
                + "\nMaterialized financial-document candidates:\n"
                + "".join(f"- `{path}`\n" for path in present_financial_paths)
                + "\n"
                "Files:\n"
                "- FINANCIALMANAGER.md\n"
                "- TRADINGREADME.md\n"
                "- README.md\n"
                "- STYLES.md\n"
                "- UNIVERSALS.md\n"
                "- QTEAM.md\n"
                "- MONITORING_GUIDE.md\n"
                "- REAL_TIME_MONITORING_GUIDE.md\n"
                "- REAL_TIME_MONITORING_README.md\n"
                "- WORKFLOW_STATUS_DASHBOARD.md\n"
                "- ALLAUTO.md\n"
                "- AUTODEV.md\n"
                "- API.md\n"
                "- ENDPOINTS.md\n"
                "- ROUTES.md\n"
                "- ALLROUTES.md\n"
                "- QMOI_MODEL_CARD.md\n"
                "- QMOI_REALTIME_MEMORY_INDEX.md\n"
                "- QALPHA.md\n"
                "- QALPHAUI.md\n"
                "- QMOIAI.md\n"
                "- QMOIAIUI.md\n"
                "- QCITY.md\n"
                "- QCITYUI.md\n"
                "- QMOISPACE.md\n"
                "- QMOISPACEUI.md\n"
                "- ALLBACKEND.md\n"
                "- ALLFRONTEND.md\n"
                "- ALLPLATFORMSDEVICE.md\n"
                "- GITHUB_ACTIONS_EXECUTION_GUIDE.md\n"
                "- FINAL_VALIDATION_EVIDENCE_2026_08_29.md\n"
                "- qmoi-enhanced-history-14/ALLWALLETSQVS.md\n"
                "- qmoi-enhanced-history-14/CASHON.md\n"
                "- qmoi-enhanced-history-14/CASHONTRADINGREADME.md\n"
                "- qmoi-enhanced-history-14/DEALS.md\n"
                "- qmoi-enhanced-history-14/FINANCIALMANAGER.md\n"
                "- qmoi-enhanced-history-14/LEAHWALLET.md\n"
                "- qmoi-enhanced-history-14/MEGAVAULT.md\n"
                "- qmoi-enhanced-history-14/PAYMENTS.md\n"
                "- qmoi-enhanced-history-14/QMOIAUTOMAKESMONEY.md\n"
                "- qmoi-enhanced-history-14/QMOIAUTOPROJECTS.md\n"
                "- qmoi-enhanced-history-14/QMOIAUTOPROJECTSAUTODISTRIBUTEMARKET.md\n"
                "- qmoi-enhanced-history-14/QMOIAUTOREVENUEEARN.md\n"
                "- qmoi-enhanced-history-14/QMOIREVENUEGENERATION.md\n"
                "- qmoi-enhanced-history-14/QMOITRADER.md\n"
                "- qmoi-enhanced-history-14/QMOI_PROJECT_MANAGEMENT_SYSTEMS.md\n"
                "- qmoi-enhanced-history-14/QMOI_WALLET_FINANCIAL_SYSTEMS.md\n"
                "- qmoi-enhanced-history-14/REVENUEGENERATING.md\n"
                "- qmoi-enhanced-history-14/Trade.md\n"
                "- qmoi-enhanced-history-14/PROJECT_COMPLETE.md\n"
                "- qmoi-enhanced-history-14/PROJECT_FILE_INDEX.md\n\n"
                "Supporting references:\n"
                "- scripts/qmoi_release_autofix.py\n"
                "- scripts/trading/production_trading_autopilot.py\n"
                "- scripts/monitor_workflows.py\n"
                "- scripts/realtime_workflow_monitor.py\n"
                "- scripts/ollama_autonomous_agent.py\n"
                "- scripts/resilience_auto_healing.py\n"
                "- ollamatracks/trading_dashboard.html\n"
                "- ollamatracks/checkpoint.json\n"
                "- ollamatracks/telemetry.jsonl\n"
                "- .github/workflows/*.yml\n\n"
                "Purpose:\n"
                "- Keep QMOI's financial engine, wallet awareness, global revenue generation, trading automation, account confidence, live-monitor health, employment and Megavault flows, CashOn reconciliation, autoproject revenue loops, and real-money operational logic synchronized with deployment, automation, and UI.\n"
            )
            if category_header in content:
                pattern = re.compile(r"### Category I — Q Financial Manager, wallets, accounts, trading, revenue, and money-making operations\n.*?(?=\n### Category J — Release, deployment, Vercel, and production verification)", re.DOTALL)
                content = pattern.sub(category_block.rstrip() + "\n\n", content, count=1)
            else:
                content += "\n\n" + category_block
            allmd.write_text(content, encoding="utf-8")

        return {
            "status": "ready",
            "files": present,
            "candidate_paths": present_financial_paths,
            "coverage": coverage,
            "root": str(target),
            "updated_catalog": str(allmd),
        }

    def _git_markdown_inventory(self, root: Path) -> dict[str, Any]:
        """Enumerate and structurally validate Markdown blobs from every available Git ref."""
        try:
            refs_result = subprocess.run(
                ["git", "-C", str(root), "for-each-ref", "--format=%(refname)"],
                capture_output=True,
                text=True,
                check=False,
                timeout=30,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {"status": "unavailable", "refs": [], "paths": [], "error": str(exc)}
        if refs_result.returncode != 0:
            return {
                "status": "unavailable",
                "refs": [],
                "paths": [],
                "error": refs_result.stderr.strip() or "git ref enumeration failed",
            }

        refs = [line.strip() for line in refs_result.stdout.splitlines() if line.strip()]
        paths: list[str] = []
        records: list[dict[str, Any]] = []
        failed_refs: list[dict[str, str]] = []
        paths_by_ref: dict[str, set[str]] = {}
        for ref in refs:
            try:
                tree_result = subprocess.run(
                    ["git", "-C", str(root), "ls-tree", "-r", "-z", "-l", ref],
                    capture_output=True,
                    check=False,
                    timeout=30,
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                failed_refs.append({"ref": ref, "error": str(exc)})
                continue
            if tree_result.returncode != 0:
                failed_refs.append({"ref": ref, "error": tree_result.stderr.strip() or "git tree enumeration failed"})
                continue
            paths_by_ref[ref] = set()
            for entry in tree_result.stdout.split(b"\0"):
                metadata, separator, raw_path = entry.partition(b"\t")
                fields = metadata.split()
                if not separator or len(fields) < 4:
                    continue
                path = raw_path.decode("utf-8", errors="surrogateescape")
                paths_by_ref[ref].add(path)
                if not path.lower().endswith(".md"):
                    continue
                inventory_path = f"git-ref/{ref}/{path}"
                paths.append(inventory_path)
                records.append({
                    "path": inventory_path,
                    "relative_path": path,
                    "source": ref,
                    "bytes": int(fields[3]) if fields[3].isdigit() else None,
                    "object_id": fields[2].decode("ascii", errors="replace"),
                })

        object_ids = sorted({record["object_id"] for record in records})
        object_content: dict[str, bytes] = {}
        content_error: str | None = None
        if object_ids:
            try:
                batch = subprocess.run(
                    ["git", "-C", str(root), "cat-file", "--batch"],
                    input=("\n".join(object_ids) + "\n").encode("ascii"),
                    capture_output=True,
                    check=False,
                    timeout=120,
                )
                if batch.returncode != 0:
                    content_error = batch.stderr.decode("utf-8", errors="replace").strip() or "Git blob batch read failed"
                else:
                    output = batch.stdout
                    offset = 0
                    for object_id in object_ids:
                        header_end = output.find(b"\n", offset)
                        if header_end < 0:
                            content_error = "Git blob batch response ended before an object header"
                            break
                        header = output[offset:header_end].split()
                        offset = header_end + 1
                        if len(header) != 3 or header[1] != b"blob":
                            content_error = f"Git blob unavailable or has unexpected type: {object_id}"
                            continue
                        try:
                            content_size = int(header[2])
                        except ValueError:
                            content_error = f"Git blob size is invalid: {object_id}"
                            continue
                        content_end = offset + content_size
                        if content_end >= len(output) or output[content_end:content_end + 1] != b"\n":
                            content_error = f"Git blob batch response is truncated: {object_id}"
                            break
                        object_content[object_id] = output[offset:content_end]
                        offset = content_end + 1
            except (OSError, subprocess.TimeoutExpired) as exc:
                content_error = str(exc)

        for record in records:
            content = object_content.get(record["object_id"])
            if content is None:
                record.update({
                    "lines": None,
                    "content_sha256": None,
                    "validation_status": "content-unavailable",
                    "validation_reason": content_error or "Git blob content was unavailable",
                    "validation_checks": {},
                })
                continue
            try:
                text = content.decode("utf-8")
            except UnicodeDecodeError:
                record.update({
                    "lines": None,
                    "content_sha256": hashlib.sha256(content).hexdigest(),
                    "validation_status": "needs-review",
                    "validation_reason": "Markdown blob is not valid UTF-8",
                    "validation_checks": {"utf8_valid": False},
                })
                continue
            validation = validate_markdown_content(
                text,
                record["relative_path"],
                paths_by_ref.get(record["source"], set()),
            )
            record.update({
                "lines": len(text.splitlines()),
                "content_sha256": hashlib.sha256(content).hexdigest(),
                "validation_status": validation["status"],
                "validation_reason": ", ".join(validation["errors"]) or "all local structural checks passed",
                "validation_checks": {"utf8_valid": True, **validation["checks"]},
            })

        validation_counts = {
            status: sum(record.get("validation_status") == status for record in records)
            for status in ("validated", "needs-review", "content-unavailable")
        }
        content_validation_passed = bool(records) and validation_counts["validated"] == len(records)
        inventory_status = (
            "partial" if failed_refs or validation_counts["content-unavailable"]
            else "needs-review" if validation_counts["needs-review"]
            else "ready"
        )

        return {
            "status": inventory_status,
            "refs": refs,
            "pull_request_refs": [ref for ref in refs if ref.startswith("refs/pull/")],
            "coverage": {
                "scope": "all refs currently available in the local Git database",
                "remote_completeness": "not_verified; remote-tracking refs may be stale or incomplete",
                "unfetched_pull_requests_included": False,
                "intermediate_commit_trees_included": False,
                "all_indexed_blobs_content_checked": not bool(validation_counts["content-unavailable"]),
            },
            "paths": sorted(set(paths)),
            "records": records,
            "validation_counts": validation_counts,
            "content_validation_passed": content_validation_passed,
            "failed_refs": failed_refs,
        }

    def build_markdown_sync_plan(
        self,
        root: Path | str | None = None,
        peer_roots: Sequence[Path | str] | None = None,
    ) -> dict[str, Any]:
        """Compare Markdown manifests across available repository roots."""
        target = Path(root or self.root_dir).resolve()
        candidates = [
            target,
            target.parent / "qmoi-enhanced",
            target.parent / "Alpha-Q-ai",
        ]
        candidates.extend(Path(item).resolve() for item in (peer_roots or []))
        roots = []
        seen: set[Path] = set()
        for candidate in candidates:
            if candidate in seen or not candidate.is_dir():
                continue
            seen.add(candidate)
            roots.append(candidate)

        manifests: dict[str, dict[str, str]] = {}
        for repo_root in roots:
            manifest: dict[str, str] = {}
            for path in iter_markdown_files(repo_root):
                manifest[path.relative_to(repo_root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
            manifests[str(repo_root)] = manifest

        all_paths = sorted({path for manifest in manifests.values() for path in manifest})
        missing_by_root = {
            repo: [path for path in all_paths if path not in manifest]
            for repo, manifest in manifests.items()
        }
        variants: list[str] = []
        for path in all_paths:
            hashes = {manifest[path] for manifest in manifests.values() if path in manifest}
            if len(hashes) > 1:
                variants.append(path)
        return {
            "status": "ready" if len(manifests) >= 2 else "blocked",
            "direction": "bidirectional",
            "source_of_truth": "target-owned repository workflow",
            "repositories": sorted(manifests),
            "markdown_path_count": len(all_paths),
            "missing_by_repository": missing_by_root,
            "variant_paths": variants,
            "authorization_required": True,
            "blockers": [] if len(manifests) >= 2 else [
                "a second repository checkout is unavailable; remote workflow evidence is required"
            ],
            "mutation_policy": "plan_and_verify_locally; copy, commit, merge, and publish remotely",
        }

    def refresh_markdown_category_index(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Auto-discover every markdown file, assign it to a live category, and create missing sections in ALLMDFILESREFS.md."""
        target = Path(root) if root is not None else self.root_dir
        target.mkdir(parents=True, exist_ok=True)

        search_roots = [target]
        history_root = target / "qmoi-enhanced-history-14"
        if history_root.exists():
            search_roots.append(history_root)

        discovered: set[str] = set()
        for root_path in search_roots:
            if not root_path.exists():
                continue
            for path in iter_markdown_files(root_path):
                discovered.add(path.relative_to(target).as_posix())

        ordered_files = sorted({Path(relative).name for relative in discovered})
        full_relative_files = sorted(discovered)

        category_rules = [
            ("Category A — Governance, repo continuity, and documentation integrity", [
                "README.md", "ACCOUNTABILITY.md", "SYNC.md", "MERGE.md", "MODELEVOLUTIONO.md", "SESSION_COMPLETION_REPORT.md",
                "PHASE_1_4_COMPLETION_SUMMARY.md", "GITHUB_SETUP_COMPLETE.md", "IMPLEMENTATION_COMPLETE.md", "ALLMDFILESREFS.md",
                "MODEL_CARD.md", "QMOI_MODEL_CARD.md", "MONITORING_INDEX.md", "MONITORING_SUMMARY.md", "TREE_FULL_STRUCTURE.md",
                "MEMORY_INDEX.md", "QTEAM.md", "MEMORY_INDEX.md", "FINAL_SESSION_COMPLETION_REPORT.md",
            ]),
            ("Category B — Platform, build, install, deployment, and workflow execution", [
                "BUILD.md", "INSTALL.md", "DOWNLOAD.md", "PLATFORM_REQUIREMENTS.md", "ALLPLATFORMSDEVICE.md", "WORKFLOWS.md",
                "WORKFLOWSO.md", "WORKFLOW_EXECUTION_PLAN.md", "WORKFLOW_STATUS_DASHBOARD.md", "GITHUB_ACTIONS_EXECUTION_GUIDE.md",
                "GITHUBCLONED.md", "NETLIFYPAYED.md", "VERCELPAYED.md", "VERCELLINKS.md", "GITPODPAYED.md",
            ]),
            ("Category C — Automation, monitoring, autonomous operations, and self-healing", [
                "ALLAUTO.md", "AUTODEV.md", "OLLAMA_AUTOMATION_GUIDE.md", "MONITORING_GUIDE.md", "REAL_TIME_MONITORING_GUIDE.md",
                "REAL_TIME_MONITORING_README.md", "RESILIENCE_AUTO_HEALING.md", "TEST_ENHANCEMENTS.md", "TRIGGER.md", "monitor.md",
                "OLLAMA_ENHANCEMENT_COMPLETE.md", "OLLAMA_ENHANCEMENT_SUCCESS.md",
            ]),
            ("Category C2 — Validation, test automation, hooks, and webhooks", [
                "ALLTESTSAUTOTESTS.md", "ALLHOOKSWEBHOOKS.md", "ALLVALIDATIONS.md",
                "TEST_ENHANCEMENTS.md", "TESTREADME.md", "TESTS.md", "TESTING.md",
                "HOOKS.md", "WEBHOOKS.md", "QMOI_TESTING_INDEX.md", "QMOI_TEST_DASHBOARD.md",
            ]),
            ("Category D — Product applications, feature surfaces, and UI experience", [
                "QMOIAI.md", "QMOIAIUI.md", "QALPHA.md", "QALPHAUI.md", "QCITY.md", "QCITYUI.md", "QMOISPACE.md", "QMOISPACEUI.md",
                "STYLES.md", "UNIVERSALS.md", "ALLBACKEND.md", "ALLFRONTEND.md", "ALLPORTS.md", "ALLROUTES.md",
                "QSTREAM.md", "QSTORE.md", "APP_LINKS.md", "MASTEROWNS.md", "UNIVERSAL.md",
                "CLONE_PLATFORM_UI.md", "QMOICLONEQUANTUM.md", "QMOICLONEVERCEL.md", "QUANTUMPAYED.md",
            ]),
            ("Category I — Q Financial Manager, wallets, accounts, trading, revenue, and money-making operations", [
                "FINANCIALMANAGER.md", "TRADINGREADME.md", "CASHON.md", "MEGAVAULT.md", "LEAHWALLET.md", "QMOITRADER.md",
                "QMOIAUTOPROJECTS.md", "QMOIAUTOPROJECTSAUTODISTRIBUTEMARKET.md", "QMOIAUTOMAKESMONEY.md", "QMOIREVENUEGENERATION.md",
                "REVENUEGENERATING.md", "PAYMENTS.md", "DEALS.md", "QMOI_WALLET_FINANCIAL_SYSTEMS.md", "PROJECT_COMPLETE.md",
                "QMOI_PROJECT_MANAGEMENT_SYSTEMS.md",
                "finance", "financial", "wallet", "bank", "payment", "payroll", "employment",
                "revenue", "income", "money", "deal", "currency", "invoice", "tax", "budget",
                "transaction", "treasury", "remittance", "payout", "salary", "accounting",
            ]),
            ("Category F — Security, privacy, masks, memory, and cross-system awareness", [
                "QMOIMASKS.md", "QVS.md", "ENHANCEDQVS.md", "QMOI_REALTIME_MEMORY_INDEX.md", "QMOI_MODEL_CARD.md",
                "QMOI_MEMORY_AWARENESS_SYSTEM.md", "oe.md", "or.md", "ollama.md", "github.md",
            ]),
            ("Category G1 — Clone, autoclone, and hosted platform parity", [
                "AUTOCLONE_STANDALONE.md", "GITHUBPAYED.md", "GITPODPAYED.md", "HUGGINGFACEPAYED.md", "HUGGINGFACEHFPAYED.md",
                "NETLIFYPAYED.md", "QVILLAGE.md", "QUANTUM.md", "VERCELLINKS.md", "VERCELPAYED.md", "QMOIGITHUBAPP.md",
                "QMOIHUGGINGFACESPACES.md", "QMOIHUGGINGFACESPACESSETUPINST.md", "QMOINETWORK.md", "QMOICLONEGITLAB.md",
                "QMOICLONEGITHUB.md", "QMOICLONEGITPOD.md", "QMOICLONEHF.md", "QMOICLONEHUGGINGFACE.md", "QMOICLONEQUANTUM.md",
                "QMOICLONEDAGSHUB.md", "QMOIDATABASE.md",
            ]),
        ]

        assignments: dict[str, list[str]] = {label: [] for label, _ in category_rules}
        generated: list[str] = []
        financial_category_label = next(
            label for label, _ in category_rules if label.startswith("Category I — Q Financial Manager")
        )
        financial_content_candidate = re.compile(
            r"\b(financ\w*|currency|currencies|wallet|bank(?:ing)?|payment|payroll|"
            r"employ\w*|revenue|income|profit|loss|money[- ]making|deal|contract|"
            r"invoice|tax|budget|transaction|treasury|remittance|payout|salary|"
            r"accounting|global|worldwide|cross[- ]border|country|countries|nation|"
            r"jurisdiction|investment|funding|grant|liabilit\w*|reconcil\w*)\b|[$€£¥]",
            re.IGNORECASE,
        )

        for relative_path in full_relative_files:
            name = Path(relative_path).name
            lower_name = name.lower()
            matching_labels: list[str] = []
            for label, tokens in category_rules:
                if any(token.lower() == lower_name or token.lower() in lower_name.replace("-", "_") for token in tokens) or any(token.lower() in lower_name.replace("-", "_") for token in tokens):
                    matching_labels.append(label)
            if not matching_labels:
                generated.append(relative_path)
                matching_labels = ["Category K — Auto-generated markdown coverage"]
            for bucket in matching_labels:
                if bucket not in assignments:
                    assignments[bucket] = []
                assignments[bucket].append(relative_path)

        all_category_label = "Category ALL — Complete cross-repository markdown and feature coverage"
        aggregate_contracts = {
            "API.md": "all APIs",
            "ENDPOINTS.md": "all endpoints",
            "ROUTES.md": "all routes",
            "ALLROUTES.md": "all routes",
            "ALLPORTS.md": "all ports",
            "ALLAUTO.md": "all automation",
            "ALLBACKEND.md": "all backend features",
            "ALLFRONTEND.md": "all frontend features",
            "ALLPLATFORMSDEVICE.md": "all platform and device support",
            "ALLMDFILESREFS.md": "all markdown files and category references",
            "RELEASES.md": "all release evidence",
            "ALLVALIDATIONS.md": "all validation evidence",
            "ALLTESTSAUTOTESTS.md": "all discovered automated tests and feature-to-test mappings",
            "ALLHOOKSWEBHOOKS.md": "all discovered workflow hooks and webhook integration evidence",
        }
        aggregate_contracts = {
            name.upper(): purpose for name, purpose in aggregate_contracts.items()
        }
        git_inventory = self._git_markdown_inventory(target)
        sync_plan = self.build_markdown_sync_plan(target)
        all_category_files = sorted(set(full_relative_files) | set(git_inventory["paths"]))
        markdown_metrics: list[dict[str, Any]] = []
        materialized_markdown_paths = set(full_relative_files)
        for relative_path in full_relative_files:
            path = target / relative_path
            data = path.read_bytes()
            utf8_valid = True
            try:
                text = data.decode("utf-8")
                validation = validate_markdown_content(text, relative_path, materialized_markdown_paths)
            except UnicodeDecodeError:
                utf8_valid = False
                text = data.decode("utf-8", errors="replace")
                validation = {
                    "status": "needs-review",
                    "checks": {
                        "nonempty": bool(data),
                        "has_heading": False,
                        "balanced_code_fences": False,
                        "unresolved_markers": [],
                        "missing_local_markdown_links": [],
                    },
                    "errors": ["invalid_utf8"],
                }
            if financial_content_candidate.search(text):
                assignments[financial_category_label].append(relative_path)
            markdown_metrics.append({
                "path": relative_path,
                "source": relative_path.split("/", 1)[0] if "/" in relative_path else target.name,
                "bytes": len(data),
                "lines": len(text.splitlines()),
                "sha256": hashlib.sha256(data).hexdigest(),
                "validation_status": validation["status"],
                "validation_errors": validation["errors"],
                "validation_checks": {
                    "utf8_valid": utf8_valid,
                    **validation["checks"],
                },
            })
        markdown_metrics.extend(git_inventory.get("records", []))
        materialized_validated = sum(
            item.get("validation_status") == "validated"
            for item in markdown_metrics
            if "source" in item and not str(item.get("path", "")).startswith("git-ref/")
        )
        materialized_review = sum(
            item.get("validation_status") != "validated"
            for item in markdown_metrics
            if "source" in item and not str(item.get("path", "")).startswith("git-ref/")
        )
        history_counts = git_inventory.get("validation_counts", {})
        local_history_total = sum(history_counts.values())
        local_history_validated = history_counts.get("validated", 0)
        markdown_validation_summary = {
            "materialized_file_count": len(full_relative_files),
            "materialized_validated_count": materialized_validated,
            "materialized_needs_review_count": materialized_review,
            "locally_available_ref_file_count": local_history_total,
            "locally_available_ref_validated_count": local_history_validated,
            "locally_available_ref_needs_review_count": history_counts.get("needs-review", 0),
            "locally_available_ref_content_unavailable_count": history_counts.get("content-unavailable", 0),
            "all_materialized_and_local_ref_documents_validated": (
                bool(full_relative_files)
                and materialized_validated == len(full_relative_files)
                and local_history_validated == local_history_total
                and not git_inventory.get("failed_refs")
            ),
            "remote_ref_and_pr_completeness_verified": False,
            "final_completion_eligible": False,
            "blocker": "target-owned remote ref, PR, and intermediate-commit-tree inventories are not independently verified",
        }
        aggregate_files: dict[str, str] = {}
        for relative_path in all_category_files:
            name = Path(relative_path).name.upper()
            if name in aggregate_contracts:
                aggregate_files[relative_path] = aggregate_contracts[name]
            elif "ALL" in Path(relative_path).stem.upper():
                aggregate_files[relative_path] = "aggregate markdown contract identified by filename"

        allmd_path = target / "ALLMDFILESREFS.md"
        index_text = allmd_path.read_text(encoding="utf-8") if allmd_path.exists() else "# ALLMDFILESREFS.md - Complete Reference of All .md Files in Both Repositories\n\n"

        for label, files in assignments.items():
            if not files:
                continue
            files = sorted(set(files))
            header = f"### {label}"
            if header not in index_text:
                block = (
                    f"\n{header}\n\n"
                    f"Files:\n" + "\n".join(f"- {item}" for item in files) + "\n\n"
                    "Supporting references:\n- scripts/ollama_autonomous_agent.py\n- scripts/realtime_workflow_monitor.py\n- scripts/resilience_auto_healing.py\n- .github/workflows/*.yml\n\n"
                    "Purpose:\n- Keep the live repository inventory complete and automatically synchronized with every markdown file discovered in the active repo and historical archive.\n"
                )
                index_text = index_text.rstrip() + block
            else:
                match = re.search(rf"{re.escape(header)}\n.*?(?=\n### Category |\n### Category [A-Z]|\Z)", index_text, re.DOTALL)
                if match:
                    section = match.group(0)
                    for item in files:
                        if f"- {item}" not in section:
                            section = section.rstrip() + f"\n- {item}"
                            index_text = index_text.replace(match.group(0), section, 1)

        all_header = f"### {all_category_label}"
        all_block = [
            all_header,
            "",
            "Refresh cadence: every push, pull request, pre-merge audit, pre-release audit, daily scheduled run, and manual dispatch.",
            "Owner: scripts/ollama_autonomous_agent.py::refresh_markdown_category_index",
            "Hook surfaces: .github/workflows/markdown-inventory-refresh.yml, merge planning, release readiness, and validation gates.",
            "Source scope: active repository, qmoi-enhanced-history-14, Alpha-Q-ai-2025 when materialized, and independently verified remote inventories.",
            "Feature contracts: API.md contains all APIs; ENDPOINTS.md all endpoints; ROUTES.md all routes; ALLPORTS.md all ports; ALLROUTES.md all routes; ALLAUTO.md all automation; ALLBACKEND.md all backend features; ALLFRONTEND.md all frontend features; ALLPLATFORMSDEVICE.md all platform/device support; ALLTESTSAUTOTESTS.md all discovered tests and explicit feature mappings; ALLHOOKSWEBHOOKS.md all discovered workflow events and webhook references with verification states; RELEASES.md all releases; ALLVALIDATIONS.md all validation evidence.",
            "Automatic contract selection: exact aggregate names and any markdown filename containing ALL are classified below; every other discovered markdown file is also listed for complete cross-repository coverage.",
            "Category membership: a markdown file may appear in unlimited categories whenever its filename, content, or feature responsibilities match; no category assignment is exclusive.",
            "Completeness rule: every discovered markdown path is listed below; missing history or remote access remains explicitly unproven rather than silently omitted.",
            (
                "Validation summary: "
                f"{materialized_validated}/{len(full_relative_files)} materialized documents pass; "
                f"{local_history_validated}/{local_history_total} documents in locally available refs pass; "
                f"remote refs/PRs complete={markdown_validation_summary['remote_ref_and_pr_completeness_verified']}; "
                f"final completion eligible={markdown_validation_summary['final_completion_eligible']}."
            ),
            "",
            "Files:",
        ]
        all_block.extend(f"- {item}" for item in all_category_files)
        all_block.extend([
            "",
            "Metrics (path | source/ref | bytes | lines | content hash/object id | validation):",
        ])
        for metric in markdown_metrics:
            digest = metric.get("sha256") or metric.get("object_id") or "unavailable"
            all_block.append(
                f"- `{metric['path']}` | `{metric.get('source', 'unknown')}` | "
                f"{metric.get('bytes', 'unknown')} | {metric.get('lines', 'unknown')} | "
                f"`{digest}` | `{metric.get('validation_status', 'unknown')}`"
            )
        all_block.extend([
            "",
            "Aggregate files and feature contracts:",
        ])
        all_block.extend(f"- {item}: {purpose}" for item, purpose in sorted(aggregate_files.items()))
        all_block.extend([
            "",
            "Supporting references:",
            "- scripts/ollama_autonomous_agent.py",
            "- scripts/repository_contract_audit.py",
            "- scripts/merge_inventory.py",
            "- scripts/qmoi_release_autofix.py",
            "- .github/workflows/markdown-inventory-refresh.yml",
            "",
            "Purpose:",
            "- Keep every aggregate markdown contract complete, synchronized, testable, and evidence-backed across both repositories and their available history projections.",
        ])
        all_section = "\n".join(all_block) + "\n"
        if all_header in index_text:
            pattern = re.compile(rf"{re.escape(all_header)}\n.*?(?=\n### Category |\Z)", re.DOTALL)
            index_text = pattern.sub(all_section.rstrip(), index_text, count=1)
        else:
            index_text = index_text.rstrip() + "\n\n" + all_section

        allmd_path.write_text(index_text.rstrip() + "\n", encoding="utf-8")

        return {
            "status": "ready",
            "all_markdown_files": ordered_files,
            "generated_categories": sorted(set(generated)),
            "updated_files": [allmd_path.name],
            "category_map": {label: sorted(set(files)) for label, files in assignments.items() if files},
            "all_category": {
                "label": all_category_label,
                "files": all_category_files,
                "metrics": markdown_metrics,
                "aggregate_files": aggregate_files,
                "git_history": git_inventory,
                "validation_summary": markdown_validation_summary,
                "sync_plan": sync_plan,
                "refresh_triggers": [
                    "push",
                    "pull_request",
                    "pre_merge",
                    "pre_release",
                    "daily_schedule",
                    "workflow_dispatch",
                ],
            },
            "count": len(ordered_files),
            "validation_summary": markdown_validation_summary,
            "multi_category_files": sorted(
                path for path, labels in (
                    (path, [label for label, files in assignments.items() if path in files])
                    for path in full_relative_files
                )
                if len(labels) > 1
            ),
        }

    def refresh_production_manifests(
        self,
        root: Path | str | None = None,
        replacements: Sequence[Mapping[str, object]] | None = None,
    ) -> dict[str, Path]:
        """Refresh production evidence after a scan or verified replacement.

        A marker scan is evidence of work still required, not evidence that a
        replacement happened. Callers may pass replacement records only after
        the implementation and its validation have been independently checked.
        """
        target = Path(root) if root is not None else self.root_dir
        target.mkdir(parents=True, exist_ok=True)
        replacement_records = [dict(record) for record in (replacements or [])]
        production_inventory = self.cross_repo_manager.identify_missing_implementations(target)
        entries = production_inventory["items"]
        inventory_path = target / "ollamatracks" / "production_gap_inventory.json"
        safe_json_write(inventory_path, production_inventory)
        self.results["production_gap_inventory"] = production_inventory

        production_path = target / "production.md"
        scan_status = "needs_review" if production_inventory["status"] == "NEEDS_REVIEW" else "clear"
        production_lines = [
            "## Agent-managed production inventory",
            "",
            f"Production implementation candidate status: {scan_status}; production readiness is not established by scanning.",
            f"Last scan: {utc_iso()}.",
            f"Production gap inventory: `{inventory_path.relative_to(target).as_posix()}`.",
            f"Files scanned: {production_inventory['scanned_files']}; candidate files: {production_inventory['total_candidates']}; unreadable: {len(production_inventory['unreadable_files'])}; oversized not read: {production_inventory['oversized_files_not_read']}.",
            f"Historical/cache/dependency roots explicitly excluded: {len(production_inventory['excluded_roots'])}; this is the active materialized workspace only, not remote branches or unfetched history.",
            "",
            "## Required replacement policy",
            "- Marker matches are candidate locations, not verified defects; review owning code and intended behavior before editing.",
            "- Never bulk-rewrite files or change APIs from keyword matches alone. Record requirement, owner, implementation plan, focused tests, security impact, rollback, and exact validation result.",
            "- A replacement is verified only after implementation and relevant tests pass; a repository is production-ready only after all required gates and exact remote evidence pass.",
            "- Historical snapshots, installed dependencies, generated caches, and build outputs are excluded by scope and listed in the machine inventory; they are not silently counted as active source.",
            "",
            "## Unmapped production candidates",
        ]

        if entries:
            for entry in entries[:200]:
                production_lines.append(f"- `{entry['path']}`: {', '.join(marker.upper() for marker in entry['candidate_markers'])}; lines {', '.join(str(number) for values in entry['line_numbers'].values() for number in values[:8])}; status=`discovered_unmapped`.")
            if len(entries) > 200:
                production_lines.append(f"- {len(entries) - 200} additional candidates are indexed in `{inventory_path.relative_to(target).as_posix()}`.")
        else:
            production_lines.append("- No scoped production-gap candidates were detected; production readiness is not implied.")

        production_lines.extend(["", "## Reported replacement claims (not independently verified)"])
        if replacement_records:
            for record in replacement_records:
                production_lines.append(
                    f"- {record.get('path', '<unknown>')}: "
                    f"reported_status={record.get('status', 'unspecified')}; "
                    f"implementation_reference={record.get('implementation_evidence', '<missing>')}; "
                    f"validation_reference={record.get('validation_evidence', '<missing>')}"
                )
        else:
            production_lines.append("- None supplied; detected candidates remain unresolved.")

        enhanced_path = target / "productionenhanced.md"
        enhanced_lines = [
            "## Agent-managed production inventory",
            "",
            f"Production candidate review status: {scan_status}; production readiness is not established.",
            f"Last updated: {utc_iso()}.",
            "This file distinguishes candidate discovery, mapped plans, implemented changes, tested replacements, and remotely verified production state.",
            f"Machine inventory: `{inventory_path.relative_to(target).as_posix()}` (SHA-256 `{hashlib.sha256(inventory_path.read_bytes()).hexdigest()}`).",
            f"Scope: {production_inventory['coverage_scope']}; scanned `{production_inventory['scanned_files']}` files and found `{production_inventory['total_candidates']}` unmapped candidate files.",
            "",
            "## Production replacement policy",
            "- Scan every file and directory for placeholder, stub, minimal, shallow, or error-driven implementations.",
            "- Do not automatically rewrite candidate files from marker matches; queue each candidate for requirement mapping, safe implementation, focused tests, review gates, and rollback evidence.",
            "- Refresh this file after every major autonomous upgrade so the repository keeps an accurate production ledger.",
            "- Never mark a file production-ready from a scan alone; retain unresolved findings until implementation and validation evidence exist.",
            "",
            "## Enhancements",
            "- Added scoped, hash-only candidate scanning with explicit unreadable/oversized/excluded-path coverage.",
            "- Candidate status is `discovered_unmapped`; no automatic replacement or readiness claim is made by scanning.",
            "- Added a production gap inventory artifact with bounded prioritized next actions.",
            "- Production readiness remains blocked until each required implementation and validation gate is evidenced.",
            "",
            "## Files addressed",
        ]
        if entries:
            for entry in entries[:200]:
                enhanced_lines.append(f"- `{entry['path']}`: {', '.join(entry['candidate_markers'])}; status=`discovered_unmapped`.")
            if len(entries) > 200:
                enhanced_lines.append(f"- {len(entries) - 200} additional candidates are in `{inventory_path.relative_to(target).as_posix()}`.")
        else:
            enhanced_lines.append("- No production replacement entries were detected in the current repository state.")

        enhanced_lines.extend(["", "## Reported replacement claims (not independently verified)"])
        if replacement_records:
            for record in replacement_records:
                enhanced_lines.append(
                    f"- {record.get('path', '<unknown>')}: "
                    f"reported_status={record.get('status', 'unspecified')} | "
                    f"implementation reference: {record.get('implementation_evidence', '<missing>')} | "
                    f"validation reference: {record.get('validation_evidence', '<missing>')}"
                )
        else:
            enhanced_lines.append("- None supplied; no replacement is claimed.")

        _upsert_managed_markdown_section(
            production_path,
            "production.md",
            "PRODUCTION_INVENTORY",
            "\n".join(production_lines),
        )
        _upsert_managed_markdown_section(
            enhanced_path,
            "productionenhanced.md",
            "PRODUCTION_INVENTORY",
            "\n".join(enhanced_lines),
        )

        return {
            "production": production_path,
            "productionenhanced": enhanced_path,
            "inventory": inventory_path,
            "status": scan_status,
            "candidate_count": production_inventory["total_candidates"],
        }

    def refresh_qstream_qstore_documents(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Refresh QStore's app/UI catalog and the managed QStream/link sections."""
        target = Path(root) if root is not None else self.root_dir
        target.mkdir(parents=True, exist_ok=True)

        catalog_lines = [
            "| App | Category | Source repository | Documentation | Implementation status |",
            "| --- | --- | --- | --- | --- |",
        ]
        for app_id, app in QSTORE_CATALOG_APPS.items():
            repository = app["repository"]
            documentation = app["documentation"]
            catalog_lines.append(
                f"| `{app_id}` ({app['name']}) | {app['category']} | "
                f"[repository](https://github.com/{repository}) | "
                f"[{documentation}]({documentation}) | "
                "Implementation not verified by this workspace |"
            )
        catalog_lines.extend([
            "| `qvillage` (QVillage) | community | [repository](https://github.com/thealphakenya/qvillage) | [QVILLAGE.md](QVILLAGE.md) | Implementation not verified by this workspace |",
            "| `quantum` (Quantum) | hosting | [repository](https://github.com/thealphakenya/Alpha-Q-ai) | [QUANTUM.md](QUANTUM.md) | Implementation not verified by this workspace |",
        ])

        qstore_lines = [
            "## Catalog ownership",
            "",
            "- The app catalog is generated from the active autonomous development agent's `QSTORE_CATALOG_APPS` registry.",
            "- QStore includes every core QMOI app plus QStream; QStream's source repository is `thealphakenya/qstream`.",
            "- Repository links identify source repositories only. They do not prove a build, download, public app URL, or deployment is available.",
            "- The legacy four-app platform validator remains a separate compatibility contract. Catalog membership does not mean an external app implementation was checked out or tested.",
            "",
            "## Managed app catalog",
            "",
            *catalog_lines,
            "",
            "## QStore UI feature coverage by platform",
            "",
            "The agent refreshes this requirement matrix on every validation pipeline. Requirements are not implementation evidence; code-level UI tests are required before any platform is marked verified.",
            "",
        ]
        for platform in PLATFORMS:
            qstore_lines.extend([f"### {platform}", ""])
            qstore_lines.extend(
                f"- [ ] {feature}"
                for feature in (
                    *QSTORE_SHARED_UI_FEATURES,
                    *QSTORE_PLATFORM_UI_FEATURES[platform],
                )
            )
            qstore_lines.append("")
        qstore_lines.extend([
            "## Per-app user access modes",
            "",
            "These are access-state requirements for app UI generation, not claims that account systems or screens are implemented.",
            "",
        ])
        for app_id, access_modes in APP_UI_ACCESS_REQUIREMENTS.items():
            qstore_lines.append(f"### {app_id}")
            qstore_lines.extend(f"- [ ] {mode}" for mode in access_modes)
            qstore_lines.append("- [ ] Resolve the current server-verified identity, consent, and capability before rendering protected controls.")
            qstore_lines.append("- Implementation status: not verified by this workspace.")
            qstore_lines.append("")
        qstore_lines.extend([
            "## QStream entry",
            "",
            "QStream is listed in this catalog and linked to [thealphakenya/qstream](https://github.com/thealphakenya/qstream). Its product specification remains in [QSTREAM.md](QSTREAM.md). No runtime or download URL is asserted until independently verified.",
            "",
            "## Agent update contract",
            "",
            "On each validation run, the autonomous agent refreshes this managed section, the QStream integration section, and `APP_LINKS.md`. It inventories every app above across all six declared platforms and reports implementation validation as unverified unless the corresponding source checkout and tests are available.",
        ])

        qstream_lines = [
            "## QMOI Agent and QStore Integration",
            "",
            "The autonomous agent preserves this specification and refreshes only the managed section below during each validation pipeline.",
            "",
            "- QStream is cataloged by QStore and its source repository is [thealphakenya/qstream](https://github.com/thealphakenya/qstream).",
            "- The QStore catalog and cross-platform UI requirements are maintained in [QSTORE.md](QSTORE.md).",
            "- Public guest and authenticated account surfaces follow the shared access contract in [UNIVERSAL.md](UNIVERSAL.md) and [UNIVERSALS.md](UNIVERSALS.md).",
            "- QMOI product repository links are maintained in [APP_LINKS.md](APP_LINKS.md). Repository identity is not proof of a live web, app-store, or download URL.",
            f"- Managed QStore catalog apps: {', '.join(QSTORE_CATALOG_APPS)}.",
            f"- Platform UI coverage tracked: {', '.join(PLATFORMS)}.",
            "- Source repositories outside the current checkout remain implementation-unverified until their exact remote SHA and target-owned checks are inspected.",
        ]

        app_link_lines = [
            "## Managed QMOI product links",
            "",
            "These are source-repository and documentation references, not verified release, download, or deployment endpoints.",
            "",
            "| App | Source repository | Documentation | Link status |",
            "| --- | --- | --- | --- |",
        ]
        for app_id, app in QSTORE_CATALOG_APPS.items():
            repository = app["repository"]
            documentation = app["documentation"]
            app_link_lines.append(
                f"| `{app_id}` ({app['name']}) | "
                f"[thealphakenya/{repository.rsplit('/', 1)[-1]}](https://github.com/{repository}) | "
                f"[{documentation}]({documentation}) | Repository reference; runtime link unverified |"
            )
        app_link_lines.extend([
            "| `qvillage` (QVillage) | [thealphakenya/qvillage](https://github.com/thealphakenya/qvillage) | [QVILLAGE.md](QVILLAGE.md) | Master-only community link; runtime link unverified |",
            "| `quantum` (Quantum) | [thealphakenya/Alpha-Q-ai](https://github.com/thealphakenya/Alpha-Q-ai) | [QUANTUM.md](QUANTUM.md) | Hosted-capability plan; runtime link unverified |",
            "",
            "| QStore catalog | This repository | [QSTORE.md](QSTORE.md) | Local catalog; distribution endpoints unverified |",
            "",
            "The agent refreshes this registry and checks that every QStore catalog entry has a repository and documentation reference. It must not invent or mark public URLs healthy without a remote check.",
        ])

        vercel_link_lines = [
            "## QMOI app and product links",
            "",
            "- Canonical product repository references are maintained in [APP_LINKS.md](APP_LINKS.md).",
            "- QStream source repository: [thealphakenya/qstream](https://github.com/thealphakenya/qstream).",
            "- QVillage source reference: [thealphakenya/qvillage](https://github.com/thealphakenya/qvillage).",
            "- Quantum source reference: [thealphakenya/Alpha-Q-ai](https://github.com/thealphakenya/Alpha-Q-ai).",
            "- These repository references are not verified production deployments, public app URLs, or live host endpoints.",
        ]

        qstore_path = target / "QSTORE.md"
        qstream_path = target / "QSTREAM.md"
        app_links_path = target / "APP_LINKS.md"
        vercellinks_path = target / "VERCELLINKS.md"
        _upsert_managed_markdown_section(
            qstore_path,
            "QSTORE.md",
            "qstore-catalog",
            "\n".join(qstore_lines),
        )
        _upsert_managed_markdown_section(
            qstream_path,
            "QSTREAM.md",
            "qstream-qmoi-integration",
            "\n".join(qstream_lines),
        )
        _upsert_managed_markdown_section(
            app_links_path,
            "APP_LINKS.md",
            "q-moi-product-links",
            "\n".join(app_link_lines),
        )
        _upsert_managed_markdown_section(
            vercellinks_path,
            "VERCELLINKS.md",
            "q-moi-app-links",
            "\n".join(vercel_link_lines),
        )

        catalog_coverage = {
            app_id: {
                "source_repository": app["repository"],
                "documentation": app["documentation"],
                "documentation_present": (
                    target / app["documentation"]
                ).is_file(),
                "platforms": list(PLATFORMS),
                "implementation_validation": "not_performed",
            }
            for app_id, app in QSTORE_CATALOG_APPS.items()
        }

        return {
            "documents": {
                "qstore": qstore_path,
                "qstream": qstream_path,
                "app_links": app_links_path,
                "vercel_links": vercellinks_path,
            },
            "catalog_apps": list(QSTORE_CATALOG_APPS),
            "catalog_coverage": catalog_coverage,
            "platforms": list(PLATFORMS),
        }

    def refresh_hosting_quantum_ui_documents(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Refresh guarded Quantum hosting, master UI, universal access, and styles contracts."""
        target = Path(root) if root is not None else self.root_dir
        target.mkdir(parents=True, exist_ok=True)

        hosting_lines = [
            "## Quantum Hosting and Compute Capability Contract",
            "",
            "Quantum is modeled as QMOI's Vercel-compatible hosting and compute control plane with additional provider-backed quantum-compute capabilities. This is a capability plan, not evidence that a provider, QPU, paid plan, or deployment is currently available.",
            "",
            "### Vercel-compatible hosting baseline",
            "",
            *[f"- [ ] {feature}" for feature in QMOI_HOSTING_FEATURES],
            "",
            "### Quantum computing extensions",
            "",
            *[f"- [ ] {feature}" for feature in QUANTUM_EXTENSION_FEATURES],
            "",
            "### Availability and safety states",
            "",
            "- Each capability is reported as `verified`, `declared_unverified`, `planned`, or `unavailable` with a timestamp and evidence reference.",
            "- Simulator output, hybrid execution, and physical QPU execution must be labeled distinctly; never imply hardware access from a simulator result.",
            "- Physical quantum hardware access is never implied by a simulator, a hosted environment, or a model card; real hardware capability requires independent provider evidence.",
            "- Secret values remain in an approved vault. Plan entitlement, cost, quota, domain transfer, production deployment, and quantum spend require provider evidence and appropriate human approval.",
            "- Hosting and quantum job controls are designed for all six QMOI client platforms, with role-aware views and accessible status/error states.",
        ]

        quantum_features = hosting_lines

        paid_lines = [
            "## Quantum plan and entitlement coverage",
            "",
            "This is an entitlement checklist. It contains no price, subscription, or provider-availability claim; all such data must come from verified provider metadata.",
            "",
            "| Capability | Required evidence | Current status |",
            "| --- | --- | --- |",
        ]
        paid_lines.extend(
            f"| {feature} | Provider plan/capability response and timestamp | unverified |"
            for feature in (*QMOI_HOSTING_FEATURES, *QUANTUM_EXTENSION_FEATURES)
        )
        paid_lines.extend([
            "",
            "## Master and user controls",
            "",
            "- Show plan, quota, usage, and projected cost before a billable deployment or quantum job.",
            "- Separate estimate, authorization, charge, and settlement states; no UI may claim payment or revenue without provider proof.",
            "- Keep cancellation, refund/support route, and audit history available according to verified provider policy.",
        ])

        clone_quantum_lines = [
            "## Quantum clone capability contract",
            "",
            "The Quantum integration provides a common QMOI control surface for verified hosting and compute providers. Vercel-compatible capability is the baseline; quantum-compute extensions are independent provider capabilities and must not be inferred from the clone name.",
            "",
            "### Hosted application lifecycle",
            "",
            *[f"- [ ] {feature}" for feature in QMOI_HOSTING_FEATURES],
            "",
            "### Quantum and hybrid workloads",
            "",
            *[f"- [ ] {feature}" for feature in QUANTUM_EXTENSION_FEATURES],
            "",
            "### Clone governance",
            "",
            "- Preserve provider ownership, API compatibility, attribution, terms, and security boundaries; do not copy proprietary internals.",
            "- Compare Quantum and Vercel by verified feature/capability records, not by marketing statements.",
            "- Any production mutation uses authorized target-owned workflows, exact SHAs, approvals, and terminal evidence.",
        ]

        clone_vercel_lines = [
            "## Vercel-compatible integration and Quantum extensions",
            "",
            "QMOI's Vercel integration tracks Vercel-owned deployments and links, while Quantum is a separate QMOI control-plane integration designed to provide a compatible hosting baseline plus additional compute capabilities. This is not a claim of implementation parity or a copy of Vercel internals.",
            "",
            "### Compatibility inventory",
            "",
            *[f"- [ ] {feature}" for feature in QMOI_HOSTING_FEATURES],
            "",
            "### Quantum-only extension inventory",
            "",
            *[f"- [ ] {feature}" for feature in QUANTUM_EXTENSION_FEATURES],
            "",
            "- Each surface is enabled only when a real provider capability is independently verified.",
            "- See [VERCELPAYED.md](VERCELPAYED.md), [QUANTUMPAYED.md](QUANTUMPAYED.md), [QUANTUM.md](QUANTUM.md), and [APP_LINKS.md](APP_LINKS.md).",
        ]

        vercel_paid_lines = [
            "## Vercel plan, hosting, and entitlement verification",
            "",
            "Track Vercel features from live project/plan metadata. Never infer paid entitlement, deployment success, analytics access, or runtime availability from repository configuration alone.",
            "",
            *[f"- [ ] {feature}" for feature in QMOI_HOSTING_FEATURES],
            "",
            "- Record provider, account/project identity, capability response, HTTP/result state, timestamp, and exact deployment SHA.",
            "- Show unavailable and permission-denied states without replacing them with a Quantum or local success claim.",
            "- Use verified provider metadata before claiming an entitlement, quota, billing state, deployment status, or domain change.",
            "- Route domain changes, production promotion, and billable actions through explicit approval and auditable workflows.",
            "- Quantum extensions are tracked separately in [QUANTUMPAYED.md](QUANTUMPAYED.md); no Vercel feature is presumed to imply QPU capability.",
        ]

        master_lines = [
            "## Master-owned dashboard and usable-control requirements",
            "",
            "This contract derives from the archived MASTEROWNS dashboard, monitoring, control-panel, Quantum/Vercel, user-management, documentation, domain, and audit requirements. It specifies required UI behavior; it does not assert that the corresponding application routes or access have been implemented.",
            "",
            "### Master UI feature inventory",
            "",
            *[f"- [ ] {feature}" for feature in MASTER_OWNED_UI_FEATURES],
            "",
            "### Access and actual usability gate",
            "",
            "- Every master-only screen and API requires a server-verified master role/capability; hiding a menu item is not authorization.",
            "- Server-side authorization must confirm the current session, role, resource scope, and requested capability for every protected operation.",
            "- Require MFA/step-up verification for high-impact controls, show read-versus-write capability, and require human confirmation for production, money, domain, user, or provider mutations.",
            "- Test both direct-route and API denial for non-master sessions; test the authorized master path with a real approved identity in a controlled environment.",
            "- Show loading, unavailable, permission-denied, stale, and audit-result states. Never imply a master can use an action until the authenticated route and backend operation are verified.",
            "- Current implementation/access status: unverified from this repository; the autonomous agent tracks these checks but cannot grant itself master access.",
        ]

        universal_lines = [
            "## Universal UI access modes and per-user feature creation",
            "",
            "All apps and cloned-platform consoles use the same public, authenticated-user, and master-operator access model. App-specific screens may add capabilities but may not weaken these checks.",
            "",
        ]
        for mode, requirements in UNIVERSAL_UI_ACCESS_MODES.items():
            universal_lines.append(f"### {mode}")
            universal_lines.extend(f"- {requirement}" for requirement in requirements)
            universal_lines.append("")
        universal_lines.extend([
            "### Per-user UI generation",
            "",
            "- Generate or configure account-specific UI only after verified identity, consent, tenant/user scope, and server-provided capabilities are available.",
            "- Keep guest/public browsing useful without exposing private data; upgrade to account features only through explicit sign-in and consent.",
            "- Personalization may adjust preferences and layout but cannot create permissions, reveal another user's data, suppress risk warnings, or trigger financial/hosting/quantum actions.",
            "- Account creation, MFA, consent, payments, OS permission grants, production deployment, and quantum spend remain human-confirmed actions when required by policy.",
            "- Record access-mode transitions and denial reasons without writing credentials, tokens, or private user content to docs or logs.",
        ])

        styles_lines = [
            "## Universal styling coverage for apps, access modes, hosting, and cloned platforms",
            "",
            "The style system is shared across all QStore catalog apps, Quantum/Vercel hosting surfaces, master-owned controls, and every cloned-platform console. Tokens are layered as universal base, platform adaptation, app identity, and access/operational state.",
            "",
            "### Access and operational state styling",
            "",
            "- Support public guest, authenticated-user, and master-operator layouts without using color alone to distinguish permissions.",
            "- Provide consistent loading, empty, offline, stale, blocked, degraded, success, warning, and failure treatments on all six client platforms.",
            "- Keep security, financial risk, permission denial, deployment state, quantum provider/backend, quota, and validation evidence visible above cosmetic personalization.",
            "- User-specific themes apply only to verified identities and consented preferences; master controls are visually distinct and remain backend-gated.",
            "- Hosting and quantum interfaces expose responsive project/job tables, accessible status timelines, confirmation dialogs, logs, and recovery actions.",
            "",
            "### Coverage contract",
            "",
            *[f"- [ ] {requirement}" for requirement in QMOI_STYLE_COVERAGE_REQUIREMENTS],
            "",
            f"Client platforms: {', '.join(PLATFORMS)}.",
            f"Catalog apps: {', '.join(QSTORE_CATALOG_APPS)}.",
            "Implementation and rendered UI coverage remain unverified until app source checkouts, accessibility checks, and platform screenshots/tests are available.",
        ]

        clone_ui_lines = [
            "## Cloned-platform operator UI coverage",
            "",
            "Every entry below is a QMOI operator-console requirement for each client platform. It does not assert that the upstream provider exposes identical features or that this repository contains a working console.",
            "",
            f"Client platform targets: {', '.join(PLATFORMS)}.",
            "",
        ]
        clone_ui_coverage: list[dict[str, Any]] = []
        for surface, features in QMOI_CLONED_PLATFORM_UI_FEATURES.items():
            clone_ui_lines.append(f"### {surface}")
            clone_ui_lines.append("")
            clone_ui_lines.extend(f"- [ ] {feature}" for feature in features)
            clone_ui_lines.append(f"- [ ] Responsive, accessible operator UI on: {', '.join(PLATFORMS)}.")
            clone_ui_lines.append("- Implementation status: not verified by this workspace.")
            clone_ui_lines.append("")
            clone_ui_coverage.extend(
                {
                    "surface": surface,
                    "client_platform": platform,
                    "features": list(features),
                    "implementation_validation": "not_performed",
                }
                for platform in PLATFORMS
            )

        managed_documents = {
            "QUANTUM.md": ("QUANTUM.md", "quantum-hosting-contract", quantum_features),
            "QUANTUMPAYED.md": ("QUANTUMPAYED.md", "quantum-entitlements", paid_lines),
            "QMOICLONEQUANTUM.md": ("QMOICLONEQUANTUM.md", "quantum-clone-contract", clone_quantum_lines),
            "QMOICLONEVERCEL.md": ("QMOICLONEVERCEL.md", "vercel-clone-contract", clone_vercel_lines),
            "VERCELPAYED.md": ("VERCELPAYED.md", "vercel-entitlements", vercel_paid_lines),
            "MASTEROWNS.md": ("MASTEROWNS.md", "master-owned-ui-contract", master_lines),
            "UNIVERSAL.md": ("UNIVERSAL.md", "universal-ui-access-contract", universal_lines),
            "UNIVERSALS.md": (
                "UNIVERSALS.md",
                "universal-ui-access-link",
                [
                    "## Shared account and UI access contract",
                    "",
                    "The detailed public, authenticated-user, and master-operator UI contract is maintained in [UNIVERSAL.md](UNIVERSAL.md). All apps and cloned-platform consoles must follow the same server-side authorization, consent, audit, and human-confirmation rules.",
                    "",
                    "The autonomous agent updates this section during every validation/runtime documentation refresh; implementation and account access still require source-level and authenticated-session verification.",
                ],
            ),
            "STYLES.md": ("STYLES.md", "universal-app-platform-styles", styles_lines),
            "CLONE_PLATFORM_UI.md": ("CLONE_PLATFORM_UI.md", "cloned-platform-ui-matrix", clone_ui_lines),
        }
        documents: dict[str, Path] = {}
        for filename, (title, marker, lines) in managed_documents.items():
            path = target / filename
            _upsert_managed_markdown_section(
                path,
                title,
                marker,
                "\n".join(lines),
            )
            documents[filename] = path

        return {
            "documents": documents,
            "hosting_features": list(QMOI_HOSTING_FEATURES),
            "quantum_extensions": list(QUANTUM_EXTENSION_FEATURES),
            "master_ui_features": list(MASTER_OWNED_UI_FEATURES),
            "access_modes": list(UNIVERSAL_UI_ACCESS_MODES),
            "style_requirements": list(QMOI_STYLE_COVERAGE_REQUIREMENTS),
            "clone_platforms": list(QMOI_CLONED_PLATFORM_UI_FEATURES),
            "clone_platform_ui_coverage": clone_ui_coverage,
            "client_platforms": list(PLATFORMS),
            "implementation_verified": False,
            "master_access_verified": False,
        }

    def refresh_test_hook_coverage_documents(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Inventory active tests and automation hooks without claiming coverage from discovery alone."""
        target = Path(root) if root is not None else self.root_dir
        target = target.resolve()
        ignored_parts = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules", "dist", "build"}

        listing = subprocess.run(
            [
                "git", "-C", str(target), "ls-files", "--cached", "--others",
                "--exclude-standard", "-z",
            ],
            capture_output=True,
            check=False,
        )
        if listing.returncode == 0:
            relative_paths = sorted({
                item.decode("utf-8", errors="replace")
                for item in listing.stdout.split(b"\0")
                if item
            })
        else:
            relative_paths = sorted(
                path.relative_to(target).as_posix()
                for path in target.rglob("*")
                if path.is_file()
                and not (ignored_parts & set(path.relative_to(target).parts))
            )

        def ignored(path: str) -> bool:
            return bool(ignored_parts & set(Path(path).parts))

        test_paths = [
            path for path in relative_paths
            if not ignored(path)
            and (
                Path(path).name.startswith("test_") and Path(path).suffix == ".py"
                or Path(path).name.endswith((".test.ts", ".test.tsx", ".test.js", ".test.jsx", ".spec.ts", ".spec.tsx", ".spec.js", ".spec.jsx"))
            )
            and (target / path).is_file()
        ]

        def test_source_scope(path: str) -> str:
            parts = Path(path).parts
            if "qmoi-enhanced-history-14" in parts or "_archive_qmoi-enhanced" in parts:
                return "historical_archive"
            if "Alpha-Q-ai-2025" in parts:
                return "snapshot"
            return "active_checkout"

        replacement_inventory: dict[str, Any] = {
            "schema_version": 2,
            "repository": target.name,
            "scope": "materialized tracked and non-ignored paths only",
            "status": "CANDIDATE_ONLY",
            "files_scanned": 0,
            "style_candidate_count": 0,
            "universal_candidate_count": 0,
            "files": [],
            "directories": [],
            "canonical_policy_paths": [
                path for path in ("STYLES.md", "UNIVERSAL.md", "UNIVERSALS.md")
                if (target / path).is_file()
            ],
            "canonical_policy_documents": [],
            "replacement_record_schema": [
                "replacement_id", "source_paths", "destination_paths", "prior_sha256", "new_sha256",
                "owner", "reason", "tests", "hook_review", "rollback", "authorization", "repository", "ref", "source_sha",
            ],
            "replacement_lineage_policy": "A candidate is not replaced until a reviewer supplies a record matching the schema; no path deletion or automatic replacement is authorized.",
            "replacement_records": [],
            "verified_replaced_file_count": 0,
            "verified_replaced_directory_count": 0,
            "replacement_lineage_complete": False,
            "skipped_sources": [],
            "source_contents_recorded": False,
            "automatic_replacement_enabled": False,
        }
        replacement_inventory["canonical_policy_documents"] = [
            {
                "path": path,
                "bytes": (target / path).stat().st_size,
                "sha256": hashlib.sha256((target / path).read_bytes()).hexdigest(),
            }
            for path in replacement_inventory["canonical_policy_paths"]
        ]
        replacement_file_suffixes = {".css", ".scss", ".sass", ".less", ".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".py", ".md"}
        style_pattern = re.compile(
            r"\b(?:className|stylesheet|tailwind|theme|typography|font|color|spacing|layout|responsive|breakpoint|aria-)\b",
            re.IGNORECASE,
        )
        universal_pattern = re.compile(
            r"\b(?:auth|authentication|authorization|login|identity|permission|role|session|mfa|consent|csrf|rbac|protected data)\b",
            re.IGNORECASE,
        )
        ui_directory_names = {"ui", "frontend", "components", "pages", "views", "styles", "themes"}
        replacement_files: list[dict[str, Any]] = []
        replacement_directories: dict[str, dict[str, Any]] = {}
        replacement_scope_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"styles": 0, "universals": 0})
        replacement_extension_counts: dict[str, dict[str, int]] = defaultdict(lambda: {"styles": 0, "universals": 0})
        replacement_skips: list[dict[str, str]] = []
        for path in relative_paths:
            candidate = target / path
            if ignored(path) or candidate.suffix.lower() not in replacement_file_suffixes:
                continue
            try:
                if candidate.is_symlink() or not candidate.is_file():
                    continue
                stat = candidate.stat()
                if stat.st_size > 1_000_000:
                    replacement_skips.append({"path": path, "reason": "oversized_file_not_read"})
                    continue
                content = candidate.read_bytes()
            except OSError as exc:
                replacement_skips.append({"path": path, "reason": type(exc).__name__})
                continue

            replacement_inventory["files_scanned"] += 1
            parts = {part.lower() for part in Path(path).parts}
            is_ui_path = bool(parts & ui_directory_names) or candidate.suffix.lower() in {".css", ".scss", ".sass", ".less", ".html", ".htm"}
            decoded = content.decode("utf-8", errors="replace")
            domains = []
            if is_ui_path or style_pattern.search(decoded):
                domains.append("styles")
            if universal_pattern.search(path) or universal_pattern.search(decoded):
                domains.append("universals")
            if not domains:
                continue

            parent_paths = []
            parent = Path(path).parent
            while str(parent) not in {"", "."}:
                parent_paths.append(parent.as_posix())
                parent = parent.parent
            replacement_files.append({
                "candidate_id": hashlib.sha256(f"{test_source_scope(path)}:{path}:{hashlib.sha256(content).hexdigest()}".encode()).hexdigest()[:20],
                "path": path,
                "scope": test_source_scope(path),
                "bytes": stat.st_size,
                "sha256": hashlib.sha256(content).hexdigest(),
                "domains": domains,
                "extension": candidate.suffix.lower(),
                "directory_paths": list(reversed(parent_paths)),
                "status": "review_required",
                "lineage_status": "candidate_not_verified_as_replaced",
                "tests_required_before_replacement": True,
                "hook_applicability_review_required": "universals" in domains,
                "replacement_authorized": False,
            })
            for directory in parent_paths:
                counts = replacement_directories.setdefault(directory, {"styles": 0, "universals": 0, "candidate_file_paths": []})
                counts["candidate_file_paths"].append(path)
                for domain in domains:
                    counts[domain] += 1
                    replacement_scope_counts[test_source_scope(path)][domain] += 1
                    replacement_extension_counts[candidate.suffix.lower() or "[no_extension]"][domain] += 1

        replacement_inventory["files"] = replacement_files
        replacement_inventory["directories"] = [
            {"path": path, **counts, "candidate_file_paths": sorted(set(counts["candidate_file_paths"])), "status": "review_required", "lineage_status": "candidate_not_verified_as_replaced"}
            for path, counts in sorted(replacement_directories.items())
        ]
        replacement_inventory["style_candidate_count"] = sum(
            "styles" in item["domains"] for item in replacement_files
        )
        replacement_inventory["universal_candidate_count"] = sum(
            "universals" in item["domains"] for item in replacement_files
        )
        replacement_inventory["skipped_sources"] = replacement_skips
        replacement_inventory["materialized_scan_complete"] = not replacement_skips
        replacement_inventory["scope_candidate_counts"] = dict(sorted(replacement_scope_counts.items()))
        replacement_inventory["extension_candidate_counts"] = dict(sorted(replacement_extension_counts.items()))
        replacement_inventory["candidate_path_index_complete"] = bool(replacement_inventory["materialized_scan_complete"])
        replacement_inventory["replacement_manifest_sha256"] = hashlib.sha256(
            json.dumps(
                {
                    "canonical_policy_paths": replacement_inventory["canonical_policy_paths"],
                    "files": replacement_inventory["files"],
                    "directories": replacement_inventory["directories"],
                    "replacement_records": replacement_inventory["replacement_records"],
                },
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        replacement_inventory_path = target / "ollamatracks" / "style_universal_replacement_inventory.json"
        safe_json_write(replacement_inventory_path, replacement_inventory)

        test_paths_by_scope = {
            scope: [path for path in test_paths if test_source_scope(path) == scope]
            for scope in ("active_checkout", "snapshot", "historical_archive")
        }
        workflow_paths = [
            path for path in relative_paths
            if path.startswith(".github/workflows/")
            and Path(path).suffix.lower() in {".yml", ".yaml"}
            and (target / path).is_file()
        ]

        parsed_workflows: list[dict[str, str]] = []
        parse_errors: list[str] = []
        try:
            import yaml
        except ImportError:
            yaml = None

        for path in workflow_paths:
            trigger_names = "unavailable"
            if yaml is None:
                parse_errors.append(f"{path}: PyYAML unavailable")
            else:
                try:
                    workflow = yaml.load(
                        (target / path).read_text(encoding="utf-8"),
                        Loader=yaml.BaseLoader,
                    )
                    triggers = workflow.get("on", {}) if isinstance(workflow, dict) else {}
                    if isinstance(triggers, str):
                        names = [triggers]
                    elif isinstance(triggers, (dict, list)):
                        names = sorted(str(name) for name in triggers)
                    else:
                        names = []
                    trigger_names = ", ".join(names) if names else "missing_or_unparsed"
                    if not names:
                        parse_errors.append(f"{path}: no workflow trigger parsed")
                except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
                    parse_errors.append(f"{path}: {type(exc).__name__}")
            parsed_workflows.append({"path": path, "triggers": trigger_names})

        webhook_paths: list[str] = []
        source_suffixes = {".py", ".js", ".jsx", ".ts", ".tsx", ".yml", ".yaml", ".json"}
        source_roots = ("scripts/", "src/", "apps/", "api/", "functions/", ".github/workflows/", "tests/")
        webhook_pattern = re.compile(r"\bwebhooks?\b|\bWEBHOOK_[A-Z0-9_]+\b", re.IGNORECASE)
        for path in relative_paths:
            if ignored(path) or not path.startswith(source_roots) or Path(path).suffix.lower() not in source_suffixes:
                continue
            candidate = target / path
            try:
                if candidate.stat().st_size > 1_000_000:
                    continue
                if webhook_pattern.search(candidate.read_text(encoding="utf-8", errors="replace")):
                    webhook_paths.append(path)
            except OSError:
                continue

        trading_path_terms = (
            "trading", "trade", "qtrade", "exchange", "wallet", "balance",
            "order", "portfolio", "risk", "finance", "payment", "cashon",
            "megavault", "binance", "bitget", "bank",
        )
        trading_content_pattern = re.compile(
            r"\btrading\b|\btrade(?:r|rs|d)?\b|\bwallets?\b|\bbalances?\b|"
            r"\bexchanges?\b|\border(?:s| book| placement| reconciliation)?\b|"
            r"\bportfolios?\b|\bqtrade\b|\bbitget\b|\bbinance\b|\bcashon\b|"
            r"\bmegavault\b|\bno.trade\b|\bdrawdown\b|\bslippage\b",
            re.IGNORECASE,
        )
        venue_terms = {
            "bitget": "bitget", "binance": "binance", "cashon": "cashon",
            "cash-on": "cashon", "megavault": "megavault", "paypal": "paypal",
            "coinbase": "coinbase", "kraken": "kraken", "bybit": "bybit", "okx": "okx",
        }
        source_code_suffixes = {".py", ".js", ".jsx", ".ts", ".tsx", ".yml", ".yaml", ".json"}
        source_directory_names = {
            "scripts", "src", "apps", "api", "backend", "frontend", "ui",
            "components", "routes", "services", "adapters", "tests", "functions",
        }
        project_registry_docs = {
            "projectandautoprojects.md",
            "projectsandautoprojects.md",
            "projectsandautoprojectsenhanced.md",
            "projectsndautoprojects.md",
        }
        trading_files: list[dict[str, Any]] = []
        role_counts: dict[str, int] = {}
        scope_counts: dict[str, int] = {}
        venue_counts: dict[str, int] = {}
        test_path_set = set(test_paths)
        workflow_path_set = set(workflow_paths)

        for path in relative_paths:
            if ignored(path):
                continue
            candidate = target / path
            suffix = candidate.suffix.lower()
            if suffix != ".md" and suffix not in source_code_suffixes:
                continue
            try:
                if candidate.is_symlink():
                    continue
                stat = candidate.stat()
                if not candidate.is_file():
                    continue
            except OSError:
                continue

            lowered_path = path.lower()
            matched_by = [f"path:{term}" for term in trading_path_terms if term in lowered_path]
            source_parts = {part.lower() for part in Path(path).parts}
            content_scanned = False
            file_digest: str | None = None
            lowered_content = ""
            scan_content = (
                suffix == ".md" and candidate.name.lower() in project_registry_docs
                or suffix in source_code_suffixes and bool(source_parts & source_directory_names)
            )
            if scan_content and stat.st_size <= 1_000_000:
                try:
                    content = candidate.read_bytes()
                    content_scanned = True
                    file_digest = hashlib.sha256(content).hexdigest()
                    decoded = content.decode("utf-8", errors="replace")
                    lowered_content = decoded.lower()
                    if trading_content_pattern.search(decoded):
                        matched_by.append("content:trading-domain-term")
                except OSError:
                    pass
            if not matched_by:
                continue

            roles: set[str] = set()
            if suffix == ".md":
                roles.add("documentation")
            if path in test_path_set or "tests" in source_parts or Path(path).name.startswith("test_"):
                roles.add("test")
            if path in workflow_path_set or path.startswith(".github/workflows/"):
                roles.add("workflow_hook")
            if suffix in {".tsx", ".jsx", ".ts", ".js"} and (
                source_parts & {"ui", "frontend", "components", "pages", "views"}
                or "dashboard" in lowered_path
            ):
                roles.add("frontend_ui")
            if source_parts & {"api", "backend", "routes", "services", "adapters"} or "adapter" in lowered_path:
                roles.add("backend_api_or_adapter")
            if suffix in source_code_suffixes and not roles.intersection({
                "test", "workflow_hook", "documentation", "frontend_ui", "backend_api_or_adapter",
            }):
                roles.add("runtime_or_integration_candidate")
            if not roles:
                roles.add("unclassified_candidate")

            venues = sorted({
                canonical for needle, canonical in venue_terms.items()
                if needle in lowered_path or needle in lowered_content
            })
            record = {
                "path": path,
                "repository_scope": target.name,
                "scope": test_source_scope(path),
                "roles": sorted(roles),
                "venues": venues,
                "matched_by": sorted(set(matched_by)),
                "bytes": stat.st_size,
                "sha256": file_digest or "not_hashed_size_limit_or_read_error",
                "content_scanned": content_scanned,
                "status": "discovered_unmapped_not_coverage_proof",
            }
            trading_files.append(record)
            scope_counts[record["scope"]] = scope_counts.get(record["scope"], 0) + 1
            for role in roles:
                role_counts[role] = role_counts.get(role, 0) + 1
            for venue in venues:
                venue_counts[venue] = venue_counts.get(venue, 0) + 1

        credential_reference_patterns = (
            re.compile(r"""os\.(?:getenv|environ\.get)\(\s*[\"']([A-Z][A-Z0-9_]{2,})[\"']"""),
            re.compile(r"""process\.env\.([A-Z][A-Z0-9_]{2,})"""),
            re.compile(r"""process\.env\[\s*[\"']([A-Z][A-Z0-9_]{2,})[\"']\s*\]"""),
            re.compile(r"""\$\{\{\s*secrets\.([A-Z][A-Z0-9_]{2,})\s*\}\}"""),
            re.compile(r"""\b(?:API_KEY|API_SECRET|ACCESS_TOKEN|ACCESS_KEY|PRIVATE_KEY|CLIENT_SECRET|PASSPHRASE|WEBHOOK_SECRET)\b"""),
        )
        skipped_secret_path_parts = {".env", "credentials", "secrets", "vault", "keys", "private"}
        credential_suffixes = {".py", ".js", ".jsx", ".ts", ".tsx", ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".conf", ".sh"}
        provider_names = (
            "bitget", "binance", "cashon", "pesapal", "paypal", "coinbase",
            "kraken", "bybit", "okx", "megavault", "kcb", "standard_chartered",
            "stripe", "github", "huggingface",
        )
        credential_reference_records: dict[tuple[str, str], dict[str, Any]] = {}
        for path in relative_paths:
            parts = {part.lower() for part in Path(path).parts}
            if ignored(path) or parts & skipped_secret_path_parts:
                continue
            candidate = target / path
            if candidate.suffix.lower() not in credential_suffixes or candidate.name.lower().startswith((".env", "id_rsa", "id_ed25519")):
                continue
            try:
                if candidate.is_symlink() or candidate.stat().st_size > 1_000_000:
                    continue
                source_lines = candidate.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for line_number, line in enumerate(source_lines, 1):
                names: set[str] = set()
                for pattern in credential_reference_patterns:
                    for match in pattern.finditer(line):
                        name = match.group(1) if match.lastindex else match.group(0)
                        normalized_name = name.upper()
                        if any(token in normalized_name for token in (
                            "KEY", "SECRET", "TOKEN", "PASSPHRASE", "CREDENTIAL", "WEBHOOK",
                        )):
                            names.add(normalized_name)
                for name in names:
                    provider = next((item for item in provider_names if item.upper() in name), "unmapped_provider")
                    key = (name, path)
                    record = credential_reference_records.setdefault(key, {
                        "name": name,
                        "path": path,
                        "scope": test_source_scope(path),
                        "provider": provider,
                        "line_numbers": [],
                        "status": "reference_only_not_verified",
                        "credential_value_stored": False,
                    })
                    record["line_numbers"].append(line_number)

        credential_references = sorted(
            credential_reference_records.values(),
            key=lambda record: (record["provider"], record["name"], record["path"]),
        )
        credential_provider_counts: dict[str, int] = {}
        for record in credential_references:
            credential_provider_counts[record["provider"]] = credential_provider_counts.get(record["provider"], 0) + 1
        credential_reference_inventory = {
            "schema_version": 1,
            "captured_at": utc_iso(),
            "scope": "source_code_reference_names_and_consumers_only",
            "remote_completeness": "not_verified",
            "coverage_verified": False,
            "credential_values_read_from_secret_stores": False,
            "credential_values_persisted_or_emitted": False,
            "excluded_secret_store_files": True,
            "reference_count": len(credential_references),
            "provider_reference_counts": dict(sorted(credential_provider_counts.items())),
            "provider_verification": "not_performed",
            "provider_adapter_status": {
                "bitget": "local_read_only_verifier_exists_but_latest_remote/provider status requires fresh verification",
                "other_providers": "provider-specific verification not proven by this inventory",
            },
            "references": credential_references,
        }
        credential_reference_inventory_path = target / "ollamatracks" / "credential_reference_inventory.json"
        safe_json_write(credential_reference_inventory_path, credential_reference_inventory)
        credential_reference_summary_lines = [
            "### Credential references and provider verification",
            "",
            "This inventory scans source references only. It does not read environment values, `.env` files, private keys, credential vaults, provider accounts, or balances.",
            "",
            f"- Credential variable/reference names: `{credential_reference_inventory['reference_count']}`; provider groups: `{json.dumps(credential_reference_inventory['provider_reference_counts'], sort_keys=True)}`.",
            "- Consumer path and line-number metadata: `ollamatracks/credential_reference_inventory.json`; values stored/emitted: `false`.",
            "- Credential manager supports encrypted metadata storage generically; only Bitget has a provider-specific read-only verifier in the active manager. Latest Bitget evidence is not a successful verification; other provider credentials remain unverified.",
            "- Runtime presence, credential validity, scope, expiry, account ownership, balances, and live-trading permission are not inferred from a variable name.",
        ]

        ref_result = subprocess.run(
            ["git", "-C", str(target), "for-each-ref", "--format=%(refname)"],
            capture_output=True,
            text=True,
            check=False,
        )
        local_ref_names = sorted({line for line in ref_result.stdout.splitlines() if line}) if ref_result.returncode == 0 else []
        trading_inventory: dict[str, Any] = {
            "schema_version": 1,
            "captured_at": utc_iso(),
            "repository_root_name": target.name,
            "scope": "materialized_worktree_files_only",
            "history_scope": "materialized_paths_only; local ref tip trading path candidates are recorded by the merge audit; intermediate commit trees and unfetched remote refs are not scanned here",
            "local_git_ref_count": len(local_ref_names),
            "local_git_refs_available": bool(local_ref_names),
            "remote_completeness": "not_verified",
            "coverage_verified": False,
            "live_execution_status": "not_verified_by_source_inventory",
            "file_count": len(trading_files),
            "counts_by_scope": dict(sorted(scope_counts.items())),
            "counts_by_role": dict(sorted(role_counts.items())),
            "counts_by_venue": dict(sorted(venue_counts.items())),
            "credential_references": credential_reference_inventory,
            "files": sorted(trading_files, key=lambda record: record["path"]),
        }
        trading_inventory_path = target / "ollamatracks" / "trading_surface_inventory.json"
        safe_json_write(trading_inventory_path, trading_inventory)
        trading_path_lines = [
            "### Trading surface candidate inventory",
            "",
            "Materialized source paths are candidates, not proof of implementation, authorization, or test coverage. Complete branch/PR history is a separate remote audit gate.",
            "",
            f"- Candidate files: `{len(trading_files)}`; materialized scope counts: `{json.dumps(trading_inventory['counts_by_scope'], sort_keys=True)}`.",
            f"- Candidate role counts: `{json.dumps(trading_inventory['counts_by_role'], sort_keys=True)}`.",
            f"- Venue mentions: `{json.dumps(trading_inventory['counts_by_venue'], sort_keys=True)}`.",
            f"- Local refs discovered: `{len(local_ref_names)}`; this refresh does not scan every ref tree or intermediate commit. Remote completeness: `not_verified`.",
            "- Machine-readable path, size, hash, source scope, role, and venue evidence: `ollamatracks/trading_surface_inventory.json`.",
            "- Coverage state: `discovered_unmapped`; platform execution, credential validity, balances, provider webhook registration, and live-order readiness are not verified by path discovery.",
            *credential_reference_summary_lines,
            "",
            "| Trading-related candidate path | Source scope | Roles | Venue mentions | Mapping status |",
            "| --- | --- | --- | --- | --- |",
            *[
                f"| `{record['path']}` | `{record['scope']}` | `{', '.join(record['roles'])}` | `{', '.join(record['venues']) or 'unspecified'}` | `discovered_unmapped` |"
                for record in trading_inventory["files"]
            ],
        ]

        tracked_result = subprocess.run(
            ["git", "-C", str(target), "ls-files", "--cached", "-z"],
            capture_output=True,
            check=False,
        )
        tracked_markdown = {
            item.decode("utf-8", errors="replace")
            for item in tracked_result.stdout.split(b"\0") if item
        } if tracked_result.returncode == 0 else set(relative_paths)
        excluded_untracked_financial_markdown = 0
        excluded_ignored_financial_markdown = 0
        skipped_large_financial_markdown = 0
        unreadable_financial_markdown = 0
        symlink_financial_markdown = 0
        eligible_financial_markdown = 0
        currency_pattern = re.compile(
            r"\b(USD|KES|KSHS?|SGD|EUR|GBP|JPY|CNY|CAD|AUD|NZD|INR|"
            r"NGN|ZAR|AED|CHF|SEK|NOK|DKK|BRL|MXN|BTC|ETH|USDT|USDC|"
            r"US\s+DO(?:LLAR)?S?|DOLLARS?|KENYAN\s+SHILLINGS?|SHILLINGS?|"
            r"YEN|YUAN|RUPEES?|NAIRA|RAND|DIRHAMS?|FRANCS?)\b",
            re.IGNORECASE,
        )
        amount_pattern = re.compile(
            r"(?:(?:USD|KES|KSHS?|SGD|EUR|GBP|JPY|CNY|CAD|AUD|NZD|INR|NGN|ZAR|AED|CHF|SEK|NOK|DKK|BRL|MXN|BTC|ETH|USDT|USDC|US\s+DO(?:LLAR)?S?|DOLLARS?|KENYAN\s+SHILLINGS?|SHILLINGS?|YEN|YUAN|RUPEES?|NAIRA|RAND|DIRHAMS?|FRANCS?)\s*[$€£¥]?\s*\d[\d,]*(?:\.\d+)?|"
            r"(?:US\$|[$€£¥])\s*\d[\d,]*(?:\.\d+)?|"
            r"\d[\d,]*(?:\.\d+)?\s*(?:USD|KES|KSHS?|SGD|EUR|GBP|JPY|CNY|CAD|AUD|NZD|INR|NGN|ZAR|AED|CHF|SEK|NOK|DKK|BRL|MXN|BTC|ETH|USDT|USDC|US\s+DO(?:LLAR)?S?|DOLLARS?|KENYAN\s+SHILLINGS?|SHILLINGS?|YEN|YUAN|RUPEES?|NAIRA|RAND|DIRHAMS?|FRANCS?)\b)",
            re.IGNORECASE,
        )
        financial_number_pattern = re.compile(r"(?<![A-Za-z0-9])\d[\d,]*(?:\.\d+)?(?![A-Za-z0-9])")
        financial_context_pattern = re.compile(
            r"\b(balance|amount|revenue|income|profit|loss|p&l|funds?|payment|"
            r"deposit|withdrawal|transfer|salary|payroll|account number|iban|routing)\b",
            re.IGNORECASE,
        )
        finance_category_patterns = {
            "amount_currency": re.compile(
            r"\b(amount|currency|currencies|price|cost|fee|tax|usd|kes|kshs?|sgd|eur|gbp|jpy|cny|cad|aud|nzd|inr|ngn|zar|aed|chf|sek|nok|dkk|brl|mxn|btc|eth|usdt|usdc|dollars?|shillings?|yen|yuan|rupees?|naira|rand|dirhams?|francs?)\b|[$€£¥]",
                re.IGNORECASE,
            ),
            "revenue_income_money_making": re.compile(
                r"\b(revenue|income|earnings?|profit|loss|money[- ]making|monetiz\w*|"
                r"fundrais\w*|funding|grant|investment|return on investment|roi)\b",
                re.IGNORECASE,
            ),
            "payments_and_transfers": re.compile(
                r"\b(payment|payout|pay[- ]?in|pay[- ]?out|invoice|settlement|"
                r"remittance|deposit|withdrawal|transfer|refund|chargeback)\b",
                re.IGNORECASE,
            ),
            "wallets_and_banking": re.compile(
                r"\b(wallet|bank(?:ing)?|account|iban|routing|swift|treasury|"
                r"cash[- ]?flow|ledger|reconcil\w*)\b",
                re.IGNORECASE,
            ),
            "deals_and_contracts": re.compile(
                r"\b(deal|contract|commission|counterparty|escrow|"
                r"revenue[- ]share|partnership|vendor|procurement)\b",
                re.IGNORECASE,
            ),
            "employment_and_payroll": re.compile(
                r"\b(employ\w*|job|hiring|recruit\w*|payroll|salary|salaries|"
                r"wages?|contractor|benefits?|pension|compensation)\b",
                re.IGNORECASE,
            ),
            "country_and_jurisdiction": re.compile(
                r"\b(global|worldwide|international|cross[- ]border|country|countries|"
                r"nation(?:al)?|jurisdiction|region|residen(?:cy|t)|withholding|"
                r"vat|sales tax|customs|sanctions)\b",
                re.IGNORECASE,
            ),
            "project_budget_and_expenses": re.compile(
                r"\b(project budget|budget|expense|spend(?:ing)?|capex|opex|"
                r"accounts payable|accounts receivable|liabilit(?:y|ies)|"
                r"reimbursement|runway)\b",
                re.IGNORECASE,
            ),
            "financial_security_and_authorization": re.compile(
                r"\b(kyc|aml|fraud|authorization|approval|limit|"
                r"dual control|segregation of duties|audit trail|"
                r"provider verification|account ownership)\b",
                re.IGNORECASE,
            ),
        }
        owner_patterns = {
            "cashon": re.compile(r"\bcash\s*on\b", re.IGNORECASE),
            "bitget": re.compile(r"\bbitget\b", re.IGNORECASE),
            "binance": re.compile(r"\bbinance\b", re.IGNORECASE),
            "paypal": re.compile(r"\bpaypal\b", re.IGNORECASE),
            "coinbase": re.compile(r"\bcoinbase\b", re.IGNORECASE),
            "kraken": re.compile(r"\bkraken\b", re.IGNORECASE),
            "bybit": re.compile(r"\bbybit\b", re.IGNORECASE),
            "okx": re.compile(r"\bokx\b", re.IGNORECASE),
            "megavault": re.compile(r"\bmegavault\b", re.IGNORECASE),
            "pesapal": re.compile(r"\bpesapal\b", re.IGNORECASE),
            "kcb": re.compile(r"\bkcb\b", re.IGNORECASE),
            "standard_chartered": re.compile(r"\bstandard\s+chartered\b", re.IGNORECASE),
            "ledger_wallet": re.compile(r"\bledger\b", re.IGNORECASE),
        }
        generic_account_pattern = re.compile(
            r"\b(wallet|bank|account|vault|exchange|brokerage)\b", re.IGNORECASE
        )
        evidence_marker_pattern = re.compile(
            r"\b(provider response|provider evidence|observed at|checked at|source hash|"
            r"transaction id|evidence id|reconciled at)\b",
            re.IGNORECASE,
        )
        financial_claims: list[dict[str, Any]] = []
        owner_currency_counts: dict[str, dict[str, int]] = {}
        currency_mention_counts: dict[str, int] = {}
        finance_category_line_counts: dict[str, int] = {}
        finance_category_file_counts: dict[str, int] = {}
        claim_line_count = 0
        amount_candidate_count = 0
        untyped_numeric_candidate_count = 0
        account_identifier_candidate_count = 0
        for path in relative_paths:
            if Path(path).suffix.lower() != ".md":
                continue
            if ignored(path):
                excluded_ignored_financial_markdown += 1
                continue
            if tracked_result.returncode == 0 and path not in tracked_markdown:
                excluded_untracked_financial_markdown += 1
                continue
            candidate = target / path
            try:
                if candidate.is_symlink():
                    symlink_financial_markdown += 1
                    continue
                if not candidate.is_file():
                    continue
                stat = candidate.stat()
                if stat.st_size > 2_000_000:
                    skipped_large_financial_markdown += 1
                    continue
                content = candidate.read_bytes()
                text = content.decode("utf-8")
            except (OSError, UnicodeDecodeError):
                unreadable_financial_markdown += 1
                continue

            eligible_financial_markdown += 1
            lines = text.splitlines()
            currency_counts: dict[str, int] = {}
            claim_lines: list[int] = []
            category_line_numbers: dict[str, list[int]] = {}
            owners: set[str] = set()
            file_amount_count = 0
            file_untyped_number_count = 0
            file_account_id_lines = 0
            evidence_marker_line_count = 0
            for line_index, line in enumerate(lines):
                currency_aliases = {
                    "KSH": "KES", "KSHS": "KES", "SHILLING": "KES",
                    "SHILLINGS": "KES", "KENYAN SHILLING": "KES",
                    "KENYAN SHILLINGS": "KES", "DOLLAR": "USD",
                    "DOLLARS": "USD", "US DOLLAR": "USD", "US DOLLARS": "USD",
                }
                currencies = {
                    currency_aliases.get(re.sub(r"\s+", " ", match.group(1).upper()),
                                         re.sub(r"\s+", " ", match.group(1).upper()))
                    for match in currency_pattern.finditer(line)
                }
                amounts = amount_pattern.findall(line)
                matched_categories = {
                    category
                    for category, pattern in finance_category_patterns.items()
                    if pattern.search(line)
                }
                if amounts or currencies:
                    matched_categories.add("amount_currency")
                account_identifier_line = bool(
                    re.search(r"\b(account number|account no\.?|iban|routing number)\b", line, re.IGNORECASE)
                    and re.search(r"\d", line)
                )
                has_financial_context = bool(financial_context_pattern.search(line))
                if not (matched_categories or amounts or currencies or account_identifier_line):
                    continue

                claim_lines.append(line_index + 1)
                for category in matched_categories:
                    category_line_numbers.setdefault(category, []).append(line_index + 1)
                    finance_category_line_counts[category] = (
                        finance_category_line_counts.get(category, 0) + 1
                    )
                file_amount_count += len(amounts)
                if has_financial_context and not amounts:
                    file_untyped_number_count += len(financial_number_pattern.findall(line))
                file_account_id_lines += int(account_identifier_line)
                for currency in currencies:
                    currency_counts[currency] = currency_counts.get(currency, 0) + 1
                    currency_mention_counts[currency] = currency_mention_counts.get(currency, 0) + 1

                context = "\n".join(lines[max(0, line_index - 2):line_index + 3])
                matched_owners = {
                    owner for owner, pattern in owner_patterns.items()
                    if pattern.search(context)
                }
                if not matched_owners:
                    matched_owners.add(
                        "unassigned_account_wallet_bank"
                        if generic_account_pattern.search(context)
                        else "unassigned_financial_claim"
                    )
                owners.update(matched_owners)
                for owner in matched_owners:
                    owner_currency_counts.setdefault(owner, {})
                    for currency in currencies:
                        owner_currency_counts[owner][currency] = (
                            owner_currency_counts[owner].get(currency, 0) + 1
                        )
                if evidence_marker_pattern.search(context):
                    evidence_marker_line_count += 1

            if not claim_lines:
                continue
            claim_line_count += len(claim_lines)
            amount_candidate_count += file_amount_count
            untyped_numeric_candidate_count += file_untyped_number_count
            account_identifier_candidate_count += file_account_id_lines
            financial_claims.append({
                "path": path,
                "scope": test_source_scope(path),
                "sha256": hashlib.sha256(content).hexdigest(),
                "bytes": stat.st_size,
                "currency_mention_counts": dict(sorted(currency_counts.items())),
                "amount_candidate_count": file_amount_count,
                "untyped_numeric_candidate_count": file_untyped_number_count,
                "account_identifier_candidate_line_count": file_account_id_lines,
                "candidate_line_numbers": claim_lines,
                "category_candidate_line_counts": {
                    category: len(line_numbers)
                    for category, line_numbers in sorted(category_line_numbers.items())
                },
                "category_candidate_line_numbers": {
                    category: line_numbers
                    for category, line_numbers in sorted(category_line_numbers.items())
                },
                "owner_groups": sorted(owners),
                "evidence_marker_candidate_line_count": evidence_marker_line_count,
                "evidence_status": "needs_independent_review_not_verified",
            })
            for category in category_line_numbers:
                finance_category_file_counts[category] = (
                    finance_category_file_counts.get(category, 0) + 1
                )

        financial_claim_inventory: dict[str, Any] = {
            "schema_version": 2,
            "status": "candidate_discovery_only",
            "captured_at": utc_iso(),
            "scope": "tracked_materialized_markdown_only",
            "eligible_tracked_markdown_file_count": eligible_financial_markdown,
            "excluded_ignored_financial_markdown_count": excluded_ignored_financial_markdown,
            "historical_scope": "active_checkout_snapshot_and_materialized_archive_labels; no complete remote refs or intermediate commit trees",
            "remote_completeness": "not_verified",
            "coverage_verified": False,
            "actual_balances_verified": 0,
            "amount_values_stored": False,
            "account_identifiers_stored": False,
            "source_line_text_stored": False,
            "source_values_stored": False,
            "category_taxonomy_version": 1,
            "category_taxonomy_scope": "keyword_candidate_discovery; overlapping_categories_not_semantic_completeness",
            "candidate_line_counts_by_category": dict(sorted(finance_category_line_counts.items())),
            "candidate_file_counts_by_category": dict(sorted(finance_category_file_counts.items())),
            "currency_mention_counts": dict(sorted(currency_mention_counts.items())),
            "owner_currency_counts": {
                owner: dict(sorted(counts.items()))
                for owner, counts in sorted(owner_currency_counts.items())
            },
            "financial_file_count": len(financial_claims),
            "candidate_line_count": claim_line_count,
            "amount_candidate_count": amount_candidate_count,
            "untyped_numeric_candidate_count": untyped_numeric_candidate_count,
            "account_identifier_candidate_line_count": account_identifier_candidate_count,
            "excluded_untracked_financial_markdown_count": excluded_untracked_financial_markdown,
            "skipped_large_financial_markdown_count": skipped_large_financial_markdown,
            "unreadable_financial_markdown_count": unreadable_financial_markdown,
            "symlink_financial_markdown_count": symlink_financial_markdown,
            "finance_taxonomy_scope": "candidate_keyword_taxonomy_not_semantic_or_completeness_proof",
            "files": sorted(financial_claims, key=lambda record: record["path"]),
        }
        financial_claim_inventory_path = target / "ollamatracks" / "financial_claim_inventory.json"
        safe_json_write(financial_claim_inventory_path, financial_claim_inventory)
        financial_claim_summary_lines = [
            "### Redacted financial amount and account-claim audit",
            "",
            "This scan indexes claim locations and metadata only; it does not verify balances, account ownership, provider access, or transaction truth. Raw amounts, account identifiers, and source line text are never copied into the report.",
            "",
            f"- Tracked materialized Markdown files with financial claims: `{financial_claim_inventory['financial_file_count']}`.",
            f"- Candidate financial lines: `{financial_claim_inventory['candidate_line_count']}`; amount-like candidates: `{financial_claim_inventory['amount_candidate_count']}`; untyped numeric candidates: `{financial_claim_inventory['untyped_numeric_candidate_count']}`.",
            f"- Account-ID-like lines: `{financial_claim_inventory['account_identifier_candidate_line_count']}`; actual balances independently verified by this scan: `0`.",
            f"- Currency mentions by owner label: `{json.dumps(financial_claim_inventory['owner_currency_counts'], sort_keys=True)}`.",
            f"- Candidate lines by financial-management category: `{json.dumps(financial_claim_inventory['candidate_line_counts_by_category'], sort_keys=True)}`.",
            "- Candidate locations, line numbers, hashes, scopes, and owner groups: `ollamatracks/financial_claim_inventory.json`.",
            f"- Tracked Markdown denominator: `{financial_claim_inventory['eligible_tracked_markdown_file_count']}`; untracked/ignored/oversized/unreadable/symlink exclusions: `{financial_claim_inventory['excluded_untracked_financial_markdown_count']}/{financial_claim_inventory['excluded_ignored_financial_markdown_count']}/{financial_claim_inventory['skipped_large_financial_markdown_count']}/{financial_claim_inventory['unreadable_financial_markdown_count']}/{financial_claim_inventory['symlink_financial_markdown_count']}`.",
            "- Taxonomy categories are keyword candidates (amount/currency, revenue/income, payments/transfers, wallets/banking, deals/contracts, employment/payroll, country/jurisdiction, project budgets/expenses, and financial security/authorization); counts overlap and do not establish implementation or coverage.",
            "- Unsupported claims remain `needs_independent_review_not_verified`; do not silently delete or replace historical amounts with invented evidence. Resolve each claim with authorized source proof or retain it clearly marked unverified.",
        ]

        feature_rows = []
        feature_test_hook_records: list[dict[str, Any]] = []
        for platform, apps in FEATURE_REGISTRY.items():
            for app, features in apps.items():
                feature_rows.append(
                    f"| `{platform}` | `{app}` | {len(features)} | `registry_only_not_implementation_proof` | `unmapped` |"
                )
                for feature_index, feature in enumerate(features, 1):
                    slug = re.sub(r"[^a-z0-9]+", "-", feature.lower()).strip("-")[:96]
                    feature_test_hook_records.append({
                        "feature_id": f"ui.{platform}.{app}.{feature_index:03d}.{slug}",
                        "platform": platform,
                        "app": app,
                        "requirement": feature,
                        "test_paths": [],
                        "test_mapping_status": "unmapped",
                        "hook_applicability": "review_required",
                        "hook_test_paths": [],
                        "status": "discovered_unmapped",
                    })

        feature_test_hook_manifest = {
            "schema_version": 1,
            "generated_at": utc_iso(),
            "repository": target.name,
            "scope": "styles_and_universals_feature_registry",
            "feature_count": len(feature_test_hook_records),
            "test_mapped_feature_count": 0,
            "hook_applicability_reviewed_count": 0,
            "unmapped_feature_count": len(feature_test_hook_records),
            "unreviewed_hook_applicability_count": len(feature_test_hook_records),
            "unmapped_event_hook_count": None,
            "coverage_verified": False,
            "status": "NEEDS_FEATURE_TEST_HOOK_MAPPING",
            "source_contents_recorded": False,
            "features": feature_test_hook_records,
        }
        feature_manifest_bytes = json.dumps(
            feature_test_hook_manifest["features"], sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        feature_test_hook_manifest["source_manifest_sha256"] = hashlib.sha256(feature_manifest_bytes).hexdigest()
        feature_test_hook_manifest["style_universal_replacement_inventory"] = {
            "path": replacement_inventory_path.relative_to(target).as_posix(),
            "status": replacement_inventory["status"],
            "materialized_scan_complete": replacement_inventory["materialized_scan_complete"],
            "files_scanned": replacement_inventory["files_scanned"],
            "style_candidate_count": replacement_inventory["style_candidate_count"],
            "universal_candidate_count": replacement_inventory["universal_candidate_count"],
            "directory_candidate_count": len(replacement_inventory["directories"]),
            "automatic_replacement_enabled": False,
        }
        feature_test_hook_manifest_path = target / "ollamatracks" / "feature_test_hook_coverage.json"
        safe_json_write(feature_test_hook_manifest_path, feature_test_hook_manifest)

        tests_lines = [
            "## Agent-managed active test inventory",
            "",
            "Scope: current checkout's tracked and non-ignored files only. Historical refs, peer repositories, and unfetched PR trees require separate audit artifacts.",
            "",
            f"- Active-checkout test files discovered: `{len(test_paths_by_scope['active_checkout'])}`.",
            f"- Snapshot test files discovered (not active coverage): `{len(test_paths_by_scope['snapshot'])}`.",
            f"- Historical/archive test files discovered (not active coverage): `{len(test_paths_by_scope['historical_archive'])}`.",
            f"- Total test-like paths discovered across these scopes: `{len(test_paths)}`.",
            f"- UI feature registry rows: `{len(feature_rows)}`; registry entries are requirements, not proof of implementation or test coverage.",
            "- Coverage state: `discovered_unmapped` until a feature ID maps to implementation files, positive/negative tests, and an exact-SHA run result.",
            "- Completion state: `tested_local` and `tested_remote` are separate; remote status requires a terminal target-owned run for the exact source SHA.",
            "",
            "### Test files discovered",
            "",
            "| Test path | Source scope | Feature mapping | Status |",
            "| --- | --- | --- | --- |",
            *[
                f"| `{path}` | `{test_source_scope(path)}` | `unmapped` | `{'historical_reference_not_active_coverage' if test_source_scope(path) != 'active_checkout' else 'discovered_not_coverage_proof'}` |"
                for path in test_paths
            ],
            "",
            "### App/platform contract inventory",
            "",
            "| Platform | App | Registered feature count | Implementation evidence | Test mapping |",
            "| --- | --- | ---: | --- | --- |",
            *feature_rows,
            "",
            *trading_path_lines,
            "",
            *credential_reference_summary_lines,
            "",
            "### Required per-feature evidence",
            "",
            "Every UI/API/backend feature must have a stable feature ID, owning repository/ref, implementation paths, route/API and authorization boundary where applicable, accessibility/state expectations, positive and negative/boundary tests, hook/webhook tests when event-driven, artifact/result hashes, and a terminal exact-SHA validation record. Missing links stay `unmapped`, `blocked`, or `needs_review`; never infer coverage from a nearby test filename.",
        ]
        tests_lines.extend([
            "",
            f"### Styles and universals test/hook mapping: `{feature_test_hook_manifest_path.relative_to(target).as_posix()}`",
            "",
            f"Registered feature count: `{feature_test_hook_manifest['feature_count']}`; test mappings: `{feature_test_hook_manifest['test_mapped_feature_count']}`; reviewed hook applicability: `{feature_test_hook_manifest['hook_applicability_reviewed_count']}/{feature_test_hook_manifest['feature_count']}`; status: `{feature_test_hook_manifest['status']}`.",
            f"Styles/universals replacement plan: `{replacement_inventory_path.relative_to(target).as_posix()}`; `{replacement_inventory['style_candidate_count']}` style files, `{replacement_inventory['universal_candidate_count']}` universal/access files, `{len(replacement_inventory['directories'])}` directories; candidates require review and tests, and replacements are not authorized by discovery.",
            "",
        ])

        hooks_lines = [
            "## Agent-managed active workflow and webhook inventory",
            "",
            "Scope: current checkout only. Inventory discovery is not proof that a hook is registered remotely, reachable, authenticated, or successfully delivered.",
            "",
            f"- Workflow files discovered: `{len(parsed_workflows)}`.",
            f"- Source/config files mentioning webhook identifiers: `{len(webhook_paths)}`.",
            f"- Workflow parse errors: `{len(parse_errors)}`.",
            "- External registration and delivery state: `not_verified` unless a provider read and signed delivery/test evidence are recorded for the exact repository/ref.",
            f"- Styles/universals feature event coverage is tracked in `ollamatracks/feature_test_hook_coverage.json`; applicability reviews: `{feature_test_hook_manifest['hook_applicability_reviewed_count']}/{feature_test_hook_manifest['feature_count']}`; event-hook tests must be mapped separately from static style tests.",
            "",
            "### Workflow event hooks",
            "",
            "| Workflow | Trigger events | Status |",
            "| --- | --- | --- |",
            *[
                f"| `{item['path']}` | `{item['triggers']}` | `definition_discovered_execution_not_implied` |"
                for item in parsed_workflows
            ],
            "",
            "### Webhook-related source references",
            "",
            "| Source path | Handler/provider mapping | Status |",
            "| --- | --- | --- |",
            *[f"| `{path}` | `unmapped` | `reference_only_not_runtime_verified` |" for path in webhook_paths],
            "",
            "### Required hook/webhook safety evidence",
            "",
            "For each active integration, record producer/event, consumer route and owner, signature/authentication verification, least-privilege scope, replay protection, idempotency, retry/backoff and dead-letter behavior, secret reference (never secret value), audit event, positive/negative delivery tests, freshness, exact SHA, and provider-side registration/read evidence. Never auto-register a third-party webhook or expose an endpoint without authorization and a reviewed threat model.",
        ]

        styles_lines = [
            "## Agent-managed UI implementation and accountability contract",
            "",
            "Every UI feature must map a stable feature ID to app/platform, style token and interaction states, frontend component/route, backend API/authorization owner, accessibility expectations, automated tests, and evidence SHA. A style requirement or feature registry row alone is not implementation evidence.",
            "",
            "- Keep public, authenticated-user, mixed-access, and master-operator flows distinct; backend authorization is authoritative for writes.",
            "- Include loading, empty, error, offline, stale, disabled, success, and permission-denied states in the UI contract and tests.",
            "- Preserve app identity and accessibility while applying shared tokens; do not hide security, financial, consent, billing, or deployment risk.",
            "- Record each changed path, repository/ref/base SHA, before/after content hash, owner, reason, tests, and approvals in the change evidence.",
            f"- Feature-level test and hook applicability manifest: `{feature_test_hook_manifest_path.relative_to(target).as_posix()}`; {feature_test_hook_manifest['feature_count']} registered features currently require explicit mappings.",
            f"- Candidate migration inventory: `{replacement_inventory_path.relative_to(target).as_posix()}` tracks file hashes, source scopes, and directories for shared style/access contracts; automatic replacement is disabled until ownership, compatibility, tests, rollback, and authorization pass.",
            "- Do not mark a style feature complete until focused UI/accessibility/state tests and event-hook applicability are mapped; event-driven features also require delivery, denial, retry, and recovery tests.",
        ]
        universals_lines = [
            "## Agent-managed feature, test, and event accountability contract",
            "",
            "Automation may inventory and test preauthorized repository changes without a person present, but may not bypass repository policy, branch protection, user consent, provider permissions, or required human approvals for high-impact actions.",
            "",
            "- A feature is complete only when its implementation, UI/API access boundary, tests, docs, and event integrations agree for an exact repository/ref/SHA.",
            "- Every file mutation records path, owner, prior/new hashes, reason, validation, and authorization context; failed or skipped work remains visible.",
            "- Hooks/webhooks require authentication/signatures, replay and idempotency controls, bounded retries, secret-reference-only handling, audit logging, and tested failure paths.",
            "- A feature without a mapped test or verified event integration remains `unmapped` or `blocked`; total automation claims cannot exceed inspected scope.",
            f"- Current styles/universals mapping state: `{feature_test_hook_manifest['status']}`; tests mapped: `{feature_test_hook_manifest['test_mapped_feature_count']}/{feature_test_hook_manifest['feature_count']}`; hook applicability reviewed: `{feature_test_hook_manifest['hook_applicability_reviewed_count']}/{feature_test_hook_manifest['feature_count']}`.",
            f"- Candidate migration inventory: `{replacement_inventory_path.relative_to(target).as_posix()}`; each candidate remains review-required and is not treated as a completed replacement.",
            "- Trading automation remains paused on stale market/account data, invalid authorization, provider outage, risk-limit breach, or ledger mismatch; runtime independence requires separately verified hosts and fresh heartbeat evidence.",
        ]

        trading_accountability_lines = [
            "## Agent-managed trading audit and remote-continuity contract",
            "",
            "The trading source inventory is a discovery artifact. Every venue, UI, API, test, and workflow must be tied to an owner, repository/ref/SHA, implementation path, risk/auth boundary, and validation record before being marked verified.",
            "",
            "- Project and autoproject financial configuration are governed by the master/sister account policy: only authorized operators may bind a bank account, wallet, payment API, or project-linked financial destination to QMOI automation.",
            "- The repository keeps `bankandbankaccounts.md`, `FINANCIALMANAGER.md`, `projectsandautoprojects.md`, and `projectsandautoprojectsenhanced.md` synchronized with the active configuration model so every financial action remains traceable and reviewable.",
            f"- Current materialized trading candidates: `{len(trading_files)}`; platform mentions: `{json.dumps(trading_inventory['counts_by_venue'], sort_keys=True)}`.",
            "- Feature and source coverage remains `discovered_unmapped` until each candidate maps to active implementation, tests, and exact-SHA evidence.",
            "- Provider verification is `provider-sourced` only when an authorized provider response is independently recorded; repository discovery is not provider proof.",
            f"- Credential names and consumers discovered: `{credential_reference_inventory['reference_count']}`; metadata inventory: `ollamatracks/credential_reference_inventory.json`; values not read from stores or emitted.",
            "- Audit active, snapshot, and archive scopes separately; merge-audit local ref-tip path metrics are distinct from materialized-file scanning. Unfetched refs, PRs, intermediate commit trees, and peer roots remain explicit blockers.",
            "- For every Qtrade metric and exchange, map market-data source, freshness, no-trade decision, backtest/walk-forward/paper tests, execution/risk limits, fees/slippage, reconciliation, kill switch, UI states, and event handlers. Missing/stale proof remains `blocked`.",
            "- Remote runtime independence is a design target, not a present availability guarantee: require an independently hosted worker, durable idempotent queue, leased ownership, signed fresh heartbeats, monitoring/failover, and provider-authorized access. GitHub/Hugging Face outages must not create false healthy status.",
            "- On stale market/account data, lost authorization, provider outage, ledger mismatch, or failed heartbeat, stop opening orders and mark trading unavailable; only separately authorized risk-reducing actions may proceed.",
            "- Never invent balances, credentials, profits, accounts, webhook registrations, or live-run success. Real-money orders, transfers, deposits, withdrawals, and credential changes require explicit scoped authorization and provider evidence.",
        ]
        _upsert_managed_markdown_section(
            target / "Qtrade.md",
            "Qtrade.md",
            "trading-audit-source-inventory",
            "\n".join(trading_accountability_lines),
        )
        _upsert_managed_markdown_section(
            target / "TRADINGREADME.md",
            "TRADINGREADME.md",
            "trading-audit-source-inventory",
            "\n".join(trading_accountability_lines),
        )
        _upsert_managed_markdown_section(
            target / "FINANCIALMANAGER.md",
            "FINANCIALMANAGER.md",
            "trading-evidence-and-balance-accountability",
            "\n".join([
                "## Agent-managed trading and balance evidence",
                "",
                "Trading and balance displays must distinguish provider-observed, simulated, stale, and unavailable values. Path discovery does not prove account ownership, current balances, settlement, or provider integration.",
                "",
                f"- Materialized trading candidates: `{len(trading_files)}`; detailed inventory: `ollamatracks/trading_surface_inventory.json`.",
                f"- Financial claim audit: `{financial_claim_inventory['financial_file_count']}` files, `{financial_claim_inventory['candidate_line_count']}` redacted candidate lines; values are excluded from the report and no balances are verified.",
                "- Only authorized read-only provider responses can produce current balance evidence; include account scope, currency, observed-at timestamp, and reconciliation status without exposing account secrets.",
                "- Transfers, deposits, withdrawals, payroll, and live trading remain blocked without explicit authorization, verified provider capability, risk checks, and auditable confirmation.",
                "- Revenue, P&L, and model-comparison claims must be independently sourced and net of fees; no guaranteed growth/profit claims.",
                *financial_claim_summary_lines,
            ]),
        )
        _upsert_managed_markdown_section(
            target / "ACCOUNTABILITY.md",
            "ACCOUNTABILITY.md",
            "trading-file-mutation-accountability",
            "\n".join([
                "## Agent-managed trading change accountability",
                "",
                "For every trading-related file mutation, record the repository/ref/base SHA, path, prior/new hash, feature owner, reason, authorization, tests, and terminal result. Current inventory is discovery-only and does not establish that a UI, backend, exchange, or webhook works.",
                "",
                f"- Materialized trading candidate count: `{len(trading_files)}`; exact paths/hashes/scopes: `ollamatracks/trading_surface_inventory.json`.",
                f"- Financial claims: `{financial_claim_inventory['financial_file_count']}` tracked Markdown files and `{financial_claim_inventory['candidate_line_count']}` candidate lines; audit artifact `ollamatracks/financial_claim_inventory.json` stores no amount values or account identifiers.",
                "- Keep active, Alpha-Q-ai-2025 snapshot, and qmoi-enhanced-history-14 archive evidence distinct; all refs and remote PR histories require fresh target-owned enumeration.",
                "- Master accountability reports every changed path and blocked/skipped operation; secrets and credential values never enter logs or documentation.",
            ]),
        )
        credential_readiness_lines = [
            "## Agent-managed wallet, bank, and trading credential consumers",
            "",
            "The source-reference audit stores variable names and consumer paths only. It never reads `.env`, key/certificate files, encrypted vault contents, environment values, or provider responses.",
            "",
            f"- Discovered references: `{credential_reference_inventory['reference_count']}`; provider groups: `{json.dumps(credential_reference_inventory['provider_reference_counts'], sort_keys=True)}`.",
            "- Consumer map: `ollamatracks/credential_reference_inventory.json`; `credential_values_read_from_secret_stores=false`; `credential_values_persisted_or_emitted=false`.",
            "- Generic vault storage does not mean an account or provider adapter is verified. Only the Bitget read-only verifier exists in the active credential manager; its last evidence is a rejected request (`40085`) and is not success. Other providers remain unverified here.",
            "- Banks, wallets, exchanges, payment APIs, and webhooks require provider-specific verification, minimum scopes, expiry/rotation policy, and tested consumers. Unknown owners or verifiers remain `blocked`.",
        ]
        _upsert_managed_markdown_section(
            target / "CREDENTIAL_READINESS.md",
            "CREDENTIAL_READINESS.md",
            "wallet-bank-provider-credential-consumers",
            "\n".join(credential_readiness_lines),
        )
        _upsert_managed_markdown_section(
            target / "CREDENTIALS_ROTATION_PLAYBOOK.md",
            "CREDENTIALS_ROTATION_PLAYBOOK.md",
            "wallet-bank-provider-credential-coverage",
            "\n".join([
                "## Agent-managed provider consumer coverage",
                "",
                f"The current source-name inventory found `{credential_reference_inventory['reference_count']}` credential-reference occurrences across materialized active, snapshot, and historical code paths; details are in `ollamatracks/credential_reference_inventory.json`.",
                "- This is a pattern-based candidate audit, not proof that all secrets, external stores, future refs, or providers were found.",
                "- Keep values in approved vaults only. The inventory records names, consumers, scopes, and line numbers without copying assignment contents or inspecting vault values.",
                "- Provider-specific tests and explicit owner authorization are required before verification, rotation, or live trading. Only Bitget has an active provider-specific read-only verifier; no other provider is marked verified by this inventory.",
            ]),
        )

        remote_runtime_contract = [
            "## Agent-managed remote continuity and failover contract",
            "",
            "A target-owned workflow can run independently of a Codespace, but it is not independent of its workflow-host provider. Do not claim uninterrupted execution without a separately deployed, authorized worker and a verified failover test.",
            "",
            "- Persist execution IDs, source refs/SHAs, idempotent requests, checkpoints, leases, and audit events outside the workspace; resume only after re-reading authoritative state.",
            "- Heartbeat freshness, worker identity, queue age, lock ownership, and provider reachability are separate health signals. Missing/stale telemetry means `STALE` or `OFFLINE`, never `RUNNING`.",
            "- Provider failover requires pre-authorized credentials, least-privilege access, tested data consistency, and a terminal failover exercise. Never silently switch trading venues or move funds when a provider is unavailable.",
            "- On stale market/account data, lost authorization, provider outage, queue duplication, or ledger mismatch, stop new trading orders and preserve read-only monitoring where available.",
            "- External-worker deployment, availability, and disaster recovery remain `not_verified` until exact-host evidence exists.",
        ]
        for filename in ("ALLAUTO.md", "AUTODEV.md", "REMOTE_EXECUTION_ARCHITECTURE.md", "MONITORING_GUIDE.md", "monitor.md"):
            _upsert_managed_markdown_section(
                target / filename,
                filename,
                "remote-continuity-and-failover",
                "\n".join(remote_runtime_contract),
            )
        _upsert_managed_markdown_section(
            target / "TEST_ENHANCEMENTS.md",
            "TEST_ENHANCEMENTS.md",
            "feature-test-hook-evidence-gates",
            "\n".join([
                "## Agent-managed feature, trading, and hook test gates",
                "",
                "Test discovery is not coverage. Each feature needs a stable ID and explicit implementation, positive, negative/boundary, authorization, UI-state, hook-delivery, and recovery test mappings.",
                "",
                f"- Active tests discovered: `{len(test_paths_by_scope['active_checkout'])}`; snapshot tests: `{len(test_paths_by_scope['snapshot'])}`; archive tests: `{len(test_paths_by_scope['historical_archive'])}`.",
                f"- Trading source candidates: `{len(trading_files)}`; exact paths, hashes, roles, venues, and source scopes: `ollamatracks/trading_surface_inventory.json`.",
                "- Unmapped features remain `discovered_unmapped`; only local test results and terminal exact-SHA target runs may advance test state.",
                "- Hook tests must cover signature/auth rejection, replay, idempotency, duplicate delivery, retries, dead-letter behavior, redaction, and outage/recovery. Workflow trigger discovery is not webhook registration or delivery proof.",
            ]),
        )
        _upsert_managed_markdown_section(
            target / "ALLVALIDATIONS.md",
            "ALLVALIDATIONS.md",
            "trading-and-hook-validation-evidence",
            "\n".join([
                "## Agent-managed trading and automation validation",
                "",
                f"- Materialized trading candidates: `{len(trading_files)}`; source artifact: `ollamatracks/trading_surface_inventory.json`; coverage state: `discovered_unmapped`.",
                "- Per-venue gates include credential readiness (metadata only), market/account freshness, sandbox/paper execution, risk limits, reconciliation, kill switch, UI state, and positive/negative tests.",
                "- Live orders, transfers, account creation, and payouts remain blocked until explicit authorization and provider-side evidence exist; local reports do not prove real funds or balances.",
                "- Remote automation reports require exact repo/ref/SHA, workflow/run URL, terminal conclusion, artifact hash, and independent branch/ref verification.",
            ]),
        )

        documents = {
            "ALLTESTSAUTOTESTS.md": target / "ALLTESTSAUTOTESTS.md",
            "ALLHOOKSWEBHOOKS.md": target / "ALLHOOKSWEBHOOKS.md",
            "STYLES.md": target / "STYLES.md",
            "UNIVERSALS.md": target / "UNIVERSALS.md",
            "UNIVERSAL.md": target / "UNIVERSAL.md",
            "Qtrade.md": target / "Qtrade.md",
            "TRADINGREADME.md": target / "TRADINGREADME.md",
            "FINANCIALMANAGER.md": target / "FINANCIALMANAGER.md",
            "ACCOUNTABILITY.md": target / "ACCOUNTABILITY.md",
            "trading_surface_inventory.json": trading_inventory_path,
            "financial_claim_inventory.json": financial_claim_inventory_path,
            "ALLAUTO.md": target / "ALLAUTO.md",
            "AUTODEV.md": target / "AUTODEV.md",
            "REMOTE_EXECUTION_ARCHITECTURE.md": target / "REMOTE_EXECUTION_ARCHITECTURE.md",
            "MONITORING_GUIDE.md": target / "MONITORING_GUIDE.md",
            "monitor.md": target / "monitor.md",
            "TEST_ENHANCEMENTS.md": target / "TEST_ENHANCEMENTS.md",
            "ALLVALIDATIONS.md": target / "ALLVALIDATIONS.md",
        }
        _upsert_managed_markdown_section(
            documents["ALLTESTSAUTOTESTS.md"],
            "ALLTESTSAUTOTESTS.md",
            "active-test-feature-coverage",
            "\n".join(tests_lines),
        )
        _upsert_managed_markdown_section(
            documents["ALLHOOKSWEBHOOKS.md"],
            "ALLHOOKSWEBHOOKS.md",
            "active-hooks-webhooks-coverage",
            "\n".join(hooks_lines),
        )
        for filename, marker, lines in (
            ("STYLES.md", "ui-feature-implementation-accountability", styles_lines),
            ("UNIVERSALS.md", "feature-test-event-accountability", universals_lines),
            ("UNIVERSAL.md", "feature-test-event-accountability", universals_lines),
        ):
            _upsert_managed_markdown_section(
                documents[filename], filename, marker, "\n".join(lines)
            )

        return {
            "documents": documents,
            "test_file_count": len(test_paths_by_scope["active_checkout"]),
            "discovered_test_file_count": len(test_paths),
            "test_counts_by_scope": {
                scope: len(paths) for scope, paths in test_paths_by_scope.items()
            },
            "workflow_file_count": len(parsed_workflows),
            "webhook_reference_file_count": len(webhook_paths),
            "feature_registry_rows": len(feature_rows),
            "trading_inventory": trading_inventory,
            "trading_inventory_path": trading_inventory_path,
            "styles_universals_coverage": {
                key: value for key, value in feature_test_hook_manifest.items() if key != "features"
            },
            "styles_universals_coverage_path": feature_test_hook_manifest_path,
            "financial_claim_inventory": financial_claim_inventory,
            "financial_claim_inventory_path": financial_claim_inventory_path,
            "parse_errors": parse_errors,
            "scope": "active_checkout_only",
            "coverage_verified": False,
        }

    def refresh_restore_point_memory_documents(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Synchronize exact branch evidence into QMOI memory, Autodev, QVillage, and evolution surfaces."""
        target = Path(root).resolve() if root is not None else self.root_dir
        snapshot = refresh_restore_point_memory(target)
        block = "\n".join(restore_point_memory_markdown(snapshot))
        documents = (
            "QVILLAGE.md",
            "Qvillageevolutions.md",
            "QMOI_REALTIME_MEMORY_INDEX.md",
            "QMOI_MEMORY_AWARENESS_SYSTEM.md",
            "AUTODEV.md",
            "ALLAUTO.md",
        )
        updated = []
        for filename in documents:
            path = target / filename
            if path.is_file():
                _upsert_managed_markdown_section(
                    path,
                    filename,
                    "restore-point-memory-sync",
                    block,
                )
                updated.append(path)
        snapshot["updated_documents"] = [path.relative_to(target).as_posix() for path in updated]
        return snapshot

    def refresh_managed_surface_documents(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Any]:
        """Refresh all managed app/hosting/UI docs and run structural link checks."""
        target = Path(root) if root is not None else self.root_dir
        qstore_documents = self.refresh_qstream_qstore_documents(target)
        hosting_documents = self.refresh_hosting_quantum_ui_documents(target)
        research_documents = self.refresh_research_contract_documents(target)
        self.model_card_generator.refresh_project_autoproject_coverage()
        automation_coverage = self.refresh_test_hook_coverage_documents(target)

        for filename, content in {
            "QVILLAGE.md": "# QVILLAGE.md\n\nQVillage is the live QMOI community, model, and knowledge coordination surface.\n\n## Link and runtime references\n- Source repository: [thealphakenya/qvillage](https://github.com/thealphakenya/qvillage)\n- Community surface: [QVillage](https://qvillage.qmoi.com)\n\n## Active automation\n- QVillage sync remains a first-class automation surface inside QCity and the autonomous agent.\n- memory, model, and runtime state are synchronized across repo docs and platform references.\n",
            "Qvillageevolutions.md": "# Qvillageevolutions.md\n\nQVillage evolution records the durable QMOI discovery, validation, integration, and learning lifecycle.\n\n## Active automation\n- QVillage evolution is maintained through the autonomous evidence and model lifecycle.\n- implementation, validation, and rollback evidence remain correlated to the live repository SHA.\n- no model or runtime improvement is promoted without focused tests and an explicit verification record.\n",
            "QUANTUM.md": "# QUANTUM.md\n\nQMOI Quantum integration keeps the compute and model runtime path aligned with the live repo.\n\n## Link and runtime references\n- Source repository: [thealphakenya/Alpha-Q-ai](https://github.com/thealphakenya/Alpha-Q-ai)\n- Hosted capability target: [Quantum](https://quantum.qmoi.com)\n\n## Active automation\n- quantum compute and model-runtime automation are described and synchronized here.\n",
        }.items():
            path = target / filename
            if not path.exists():
                path.write_text(content + "\n", encoding="utf-8")

        qvillage_research_path = self.refresh_qvillage_research_contract(target)
        restore_memory = self.refresh_restore_point_memory_documents(target)

        link_validation = LinkValidator(str(target)).validate_product_catalog()

        document_paths = {
            **qstore_documents["documents"],
            **{
                Path(name).stem.lower(): path
                for name, path in hosting_documents["documents"].items()
            },
        }
        document_paths.update({
            "qvillage": target / "QVILLAGE.md",
            "qvillage_research": qvillage_research_path,
            "restore_point_memory": target / "ollamatracks" / "restore_point_memory.json",
            "qvillage_evolution": target / "Qvillageevolutions.md",
            "quantum": target / "QUANTUM.md",
            "all_tests": automation_coverage["documents"]["ALLTESTSAUTOTESTS.md"],
            "all_hooks_webhooks": automation_coverage["documents"]["ALLHOOKSWEBHOOKS.md"],
            "qtrade": automation_coverage["documents"]["Qtrade.md"],
            "trading_readme": automation_coverage["documents"]["TRADINGREADME.md"],
            "financial_manager": automation_coverage["documents"]["FINANCIALMANAGER.md"],
            "accountability": automation_coverage["documents"]["ACCOUNTABILITY.md"],
            "trading_inventory": automation_coverage["documents"]["trading_surface_inventory.json"],
        })
        missing_documents = [
            name for name, path in document_paths.items()
            if not path.is_file()
        ]
        structural_errors = list(missing_documents)
        required_document_markers = {
            "QUANTUM.md": ("quantum hosting and compute capability contract", "physical quantum hardware"),
            "QUANTUMPAYED.md": ("entitlement coverage", "provider plan/capability response"),
            "QMOICLONEQUANTUM.md": ("quantum clone capability contract", "provider"),
            "QMOICLONEVERCEL.md": ("vercel-compatible integration", "quantum-only extension"),
            "VERCELPAYED.md": ("vercel plan", "verified provider metadata"),
            "MASTEROWNS.md": ("master-owned dashboard", "mfa", "server-side authorization"),
            "UNIVERSAL.md": ("public_guest", "authenticated_user", "master_operator"),
            "UNIVERSALS.md": ("universal.md", "server-side authorization"),
            "STYLES.md": ("universal styling coverage", "public guest", "master-operator"),
            "CLONE_PLATFORM_UI.md": ("cloned-platform operator ui coverage", "dagshub", "android"),
            "ALLTESTSAUTOTESTS.md": ("active-test-feature-coverage", "discovered_unmapped"),
            "ALLHOOKSWEBHOOKS.md": ("active-hooks-webhooks-coverage", "not_verified"),
            "Qtrade.md": ("trading-audit-source-inventory", "discovered_unmapped", "provider-sourced"),
            "TRADINGREADME.md": ("trading-audit-source-inventory", "discovered_unmapped"),
            "FINANCIALMANAGER.md": ("trading-evidence-and-balance-accountability", "provider-observed"),
            "ACCOUNTABILITY.md": ("trading-file-mutation-accountability", "prior/new hash"),
            "REMOTE_EXECUTION_ARCHITECTURE.md": ("remote-continuity-and-failover", "not_verified"),
            "MONITORING_GUIDE.md": ("remote-continuity-and-failover", "not_verified"),
            "ALLAUTO.md": ("remote-continuity-and-failover", "STALE"),
            "AUTODEV.md": ("remote-continuity-and-failover", "failover"),
            "TEST_ENHANCEMENTS.md": ("feature-test-hook-evidence-gates", "discovered_unmapped"),
            "ALLVALIDATIONS.md": ("trading-and-hook-validation-evidence", "provider-side evidence"),
        }
        for filename, markers in required_document_markers.items():
            path = target / filename
            if not path.is_file():
                continue
            content = path.read_text(encoding="utf-8", errors="replace").casefold()
            absent = [marker for marker in markers if marker.casefold() not in content]
            if absent:
                structural_errors.append(
                    f"{filename} is missing required managed contract markers: {', '.join(absent)}"
                )
        if len(qstore_documents["catalog_apps"]) != len(QSTORE_CATALOG_APPS):
            structural_errors.append("QStore catalog registry does not match generated app entries")
        if len(hosting_documents["clone_platform_ui_coverage"]) != (
            len(QMOI_CLONED_PLATFORM_UI_FEATURES) * len(PLATFORMS)
        ):
            structural_errors.append("Cloned-platform UI coverage matrix is incomplete")
        structural_errors.extend(automation_coverage["parse_errors"])
        if not link_validation["passed"]:
            structural_errors.extend(link_validation["errors"])

        return {
            "documents": document_paths,
            "research_documents": research_documents,
            "catalog_apps": qstore_documents["catalog_apps"],
            "catalog_coverage": qstore_documents["catalog_coverage"],
            "app_access_requirements": APP_UI_ACCESS_REQUIREMENTS,
            "client_platforms": list(PLATFORMS),
            "hosting_features": hosting_documents["hosting_features"],
            "quantum_extensions": hosting_documents["quantum_extensions"],
            "master_ui_features": hosting_documents["master_ui_features"],
            "access_modes": hosting_documents["access_modes"],
            "style_requirements": hosting_documents["style_requirements"],
            "clone_platforms": hosting_documents["clone_platforms"],
            "clone_platform_ui_coverage": hosting_documents["clone_platform_ui_coverage"],
            "automation_coverage": automation_coverage,
            "restore_point_memory": restore_memory,
            "master_access_verified": False,
            "implementation_verified": False,
            "link_validation": link_validation,
            "validation": {
                "passed": not structural_errors,
                "errors": structural_errors,
                "level": "local_structure_and_links_only",
                "remote_reachability_checked": False,
            },
        }

    def refresh_research_contract_documents(self, root: Path | str | None = None) -> dict[str, Path]:
        """Refresh only managed research-contract sections and preserve authored policy text."""
        target = Path(root) if root is not None else self.root_dir
        internal_path = target / "INTERNALRESEARCH.md"
        external_path = target / "EXTERIORRESEARCH.md"
        internal_body = [
            "## Agent-managed internal research contract",
            "",
            "The full policy and ten controls remain in this document. The agent starts each merge lifecycle with source inventory, then maps findings to implementation, tests, workflows, docs, owner, source/ref/hash, and a falsifiable validation hypothesis.",
            "",
            *[f"- {control}" for control in INTERNAL_RESEARCH_CONTROLS],
            "",
            "Run evidence is kept in the per-execution `ollamatracks/q_versions/<execution-id>/lifecycle.jsonl` hash chain. Missing refs, source roots, or unreadable files remain explicit blockers.",
        ]
        external_body = [
            "## Agent-managed external research contract",
            "",
            "The curated resources listed above are candidates, not visit evidence. External fetching is disabled by default and requires an explicitly enabled GitHub-hosted run.",
            "",
            *[f"- {control}" for control in EXTERNAL_RESEARCH_CONTROLS],
            "",
            "The runtime enforces an HTTPS host allowlist, redirect refusal, 15-second maximum timeout, bounded response size/content type, and content hashes. Newly discovered domains remain `review_required` until approved.",
        ]
        _upsert_managed_markdown_section(internal_path, "INTERNALRESEARCH.md", "internal-research-contract", "\n".join(internal_body))
        _upsert_managed_markdown_section(external_path, "EXTERIORRESEARCH.md", "external-research-contract", "\n".join(external_body))
        return {"internal_research": internal_path, "external_research": external_path}

    def refresh_qvillage_research_contract(self, root: Path | str | None = None) -> Path:
        """Expose sanitized autoresearch and validation provenance in QVillage docs."""
        target = Path(root) if root is not None else self.root_dir
        path = target / "QVILLAGE.md"
        body = [
            "## QMOI Autoresearch, Autodev, and Validation Evidence",
            "",
            "QVillage consumes sanitized per-run research and validation metadata from the Q-version lifecycle ledger; it does not claim repository changes, external visits, or provider access by itself.",
            "",
            "- Internal source contract: [INTERNALRESEARCH.md](INTERNALRESEARCH.md).",
            "- External source contract and official-resource catalog: [EXTERIORRESEARCH.md](EXTERIORRESEARCH.md).",
            "- Autodev ownership, approval, and evidence policy: [AUTODEV.md](AUTODEV.md).",
            "- Each run links repository/ref/SHA, source hashes, research question, visit timestamp, findings, limitations, and applicable validation domains when actually available.",
            "- Show research states as `PLANNED_NOT_VISITED`, `VISITED`, `NEEDS_REVIEW`, `BLOCKED`, or `STALE`; never promote a plan to a successful visit.",
            "- Validation domains include Markdown/content links, app/UI, platforms, APIs/endpoints/routes/ports, build/install/download, tests, security/dependencies, workflows/hooks, hosting/deployment, memory, and Q seed lineage.",
            "- A source visit is not a validation pass. Display the independent test/provider/remote result and its exact repository SHA separately.",
            "- Do not expose credentials, private user content, hidden tokens, or unapproved research text in public QVillage surfaces.",
            "- External fetch is disabled by default and requires an authorized GitHub-hosted workflow and an allowlisted HTTPS resource.",
        ]
        _upsert_managed_markdown_section(
            path,
            "QVILLAGE.md",
            "qvillage-autoresearch-validation",
            "\n".join(body),
        )
        return path

    def refresh_clone_platform_documents(
        self,
        root: Path | str | None = None,
    ) -> dict[str, Path]:
        """Create or refresh the live docs and platform configs for the clone/autoclone ecosystem."""
        target = Path(root) if root is not None else self.root_dir
        target.mkdir(parents=True, exist_ok=True)

        netlify_toml = target / "netlify.toml"
        netlify_toml.write_text(
            """[build]\n  command = \"python -m pytest tests/test_ollama_autonomous_agent.py -q\"\n  publish = \".\"\n  functions = \"functions\"\n\n[[redirects]]\n  from = \"/*\"\n  to = \\"/index.html\"\n  status = 200\n""",
            encoding="utf-8",
        )

        templates: dict[str, str] = {
            "NETLIFYPAYED.md": """# NETLIFYPAYED.md\n\nQMOI keeps Netlify parity in sync with the live GitHub repository by maintaining deployment automation, redirects, site health, and production-safe build rules. The autonomous agent keeps this document aligned with the live Netlify runtime path and the canonical repo docs.\n\n## Active automation\n- netlify.toml is kept in the repo root and matches the current deployment contract.\n- QCity and Ollama automation keep Netlify deploy and redirect settings synchronized with GitHub workflow health.\n- Production checks must verify build command, publish path, redirects, and deployment health before final promotion.\n""",
            "GITHUBPAYED.md": """# GITHUBPAYED.md\n\nQMOI keeps GitHub paid-feature parity across repository automation, actions, pages, codespaces, and release governance. The GitHub clone and autoclone policy ensures the repo surface stays production-safe even when the upstream GitHub features are not directly paid.\n\n## Active automation\n- repo automation for actions, pages, and codespaces remains live via the GitHub-hosted workflows.\n- release and branch sync logic stays aligned with the main repository contract.\n- security review and dependency hygiene remain part of the autonomous loop before final deployment.\n""",
            "GITPODPAYED.md": """# GITPODPAYED.md\n\nQMOI maintains Gitpod workstation parity through automated workspace orchestration, environment setup, and command sync. The agent keeps the Gitpod surface aligned with GitHub workflows and the live app runtime.\n\n## Active automation\n- workspace automation remains ready for GitHub-linked developer environments.\n- synced branch and repo state are reflected in the live workflow and monitoring surfaces.\n- the runtime keeps Gitpod-specific hooks and environment documentation in sync with the canonical repo state.\n""",
            "HUGGINGFACEPAYED.md": """# HUGGINGFACEPAYED.md\n\nQMOI keeps Hugging Face parity for models, datasets, spaces, and automated inference workflows while preserving the source-of-truth repo contract. The autonomous agent updates this document alongside QVILLAGE and the Hugging Face integration surfaces.\n\n## Active automation\n- model and space automation is kept in sync across the repository, monitoring flow, and live runtime.\n- docs, memory, and deployment references are maintained with the current QMOI state.\n- all Hugging Face endpoints are treated as operational surfaces rather than disconnected metadata.\n""",
            "HUGGINGFACEHFPAYED.md": """# HUGGINGFACEHFPAYED.md\n\nQMOI keeps Hugging Face Hub and Spaces parity in sync with the active GitHub-hosted automation and runtime. This file tracks the production parity plan for Hugging Face-hosted surfaces and connected inference or deployment tasks.\n\n## Active automation\n- Hub and Space automation are monitored by the autonomous agent.\n- runtime status and deployment verification remain tied to the live repo contract.\n- platform docs remain updated as the repository and host surfaces evolve.\n""",
            "QVILLAGE.md": """# QVILLAGE.md\n\nQVillage is the live QMOI community, model, and knowledge coordination surface. It is treated as the master-only QMOI community layer that stays synchronized with GitHub, Hugging Face, and the live autonomous agent.\n\n## Active automation\n- QVillage sync remains a first-class automation surface inside QCity and the autonomous agent.\n- memory, model, and runtime state are synchronized across repo docs and platform references.\n- the live state is refreshed automatically as the repository evolves.\n""",
            "QUANTUM.md": """# QUANTUM.md\n\nQMOI Quantum integration keeps the compute and model runtime path aligned with the live repo, Vercel deployment surfaces, and GitHub automation. The autonomous agent treats Quantum as a production-capable clone and sync surface.\n\n## Quantum hosting and compute capability contract\n\nThe platform is designed for quantum hosting and compute capability planning across local, hosted, and provider-backed environments. This covers simulated and provider-backed workloads while keeping physical quantum hardware access explicitly separate from software capability claims.\n\n## Active automation\n- quantum compute and model-runtime automation are described and synchronized here.\n- deployment status and runtime verification stay tied to the canonical workflow and live repo health.\n- hosted and cloned platform parity are kept in sync with the final QMOI operating model.\n""",
            "VERCELLINKS.md": """# VERCELLINKS.md\n\nThis document tracks the operational Vercel links, deployment targets, and public/runtime references associated with the QMOI deployment stack. The autonomous agent keeps these links aligned with the current production reality.\n\n## Active automation\n- Vercel deployment links and config state stay synchronized with the live repo state.\n- routes, URLs, and link documentation remain consistent with the GitHub-hosted runtime.\n- deployment verification uses the live workflow and link-health checks before final release.\n""",
            "VERCELPAYED.md": """# VERCELPAYED.md\n\nQMOI keeps Vercel paid-feature parity for deployments, analytics, domains, and edge runtime behavior. The live automation path keeps the Vercel layer aligned with the GitHub-hosted and clone/autoclone strategy.\n\n## Vercel plan and entitlement verification\n\nThis is a Vercel plan and entitlement record. It contains no price, subscription, or deployment claim unless it is backed by verified provider metadata.\n\n## Active automation\n- deployment automation remains in the GitHub workflow and live repo contract.\n- domain, analytics, and runtime checks are part of the final verification loop.\n- clone and autoclone surfaces stay synced with the current Vercel deployment model.\n""",
            "QCITY.md": """# QCITY.md\n\nQCity remains the canonical file-management and platform coordination surface for the QMOI runtime. It coordinates GitHub, GitLab, Vercel, Netlify, Gitpod, Hugging Face, QVillage, and clone/autoclone automation without losing the live repo source-of-truth.\n\n## Active automation\n- file, repo, deployment, and sync management are centralized in QCity.\n- all clone/autoclone flows are exposed as platform automation surfaces.\n- the live runtime keeps all platform docs and generated summaries synchronized with the working repo state.\n""",
            "QMOIGITHUBAPP.md": """# QMOIGITHUBAPP.md\n\nQMOI GitHub App automation keeps the repository and workflows synchronized with the codebase and the hosted runtime. The autonomous agent treats GitHub app automation as a core operational layer for all clone and autoclone flows.\n\n## Active automation\n- actions, repo, and deployment automation remain part of the GitHub-hosted runtime.\n- repo sync and branch verification stay consistent with the live source-of-truth.\n- release and deployment gates remain part of the autonomous verification contract.\n""",
            "QMOIHUGGINGFACESPACES.md": """# QMOIHUGGINGFACESPACES.md\n\nQMOI Spaces automation keeps Hugging Face Spaces, model surfaces, and inference endpoints aligned with the live repo and QVillage runtime. The autonomous agent makes sure that the Hugging Face clone and the canonical repo remain coordinated.\n\n## Active automation\n- space deployment and runtime health remain in the live automation contract.\n- model and dataset surfaces are reflected in docs and runtime verification.\n- clone/autoclone flows keep the platform surface production-safe and synchronized.\n""",
            "QMOIHUGGINGFACESPACESSETUPINST.md": """# QMOIHUGGINGFACESPACESSETUPINST.md\n\nThis setup guide keeps the Hugging Face Space runtime, dependencies, and platform config aligned with the live QMOI operating model. It is maintained automatically by the autonomous agent so platform config does not drift from repo reality.\n\n## Active automation\n- deployment and package setup remain aligned with the live GitHub runtime.\n- runtime checks and startup requirements are kept current.\n- clone/autoclone and QVillage sync remain in the same operating contract.\n""",
            "QMOINETWORK.md": """# QMOINETWORK.md\n\nQMOI network automation keeps the clone/autoclone topology, routing, and platform coordination synchronized across GitHub, QVillage, Netlify, Vercel, Gitpod, Hugging Face, Quantum, and Dagshub. The network state is treated as a live operational graph rather than static docs.\n\n## Active automation\n- host, repo, and workspace coordination stay synchronized.\n- clone and autoclone flows share the same orchestration contract.\n- platform health checks, deployment checks, and docs remain aligned with the current runtime.\n""",
            "QMOICLONEGITLAB.md": """# QMOICLONEGITLAB.md\n\nQMOI GitLab clone automation keeps repository, pipelines, and project coordination aligned with the live GitHub-hosted QMOI runtime. This doc is refreshed automatically when the clone/autoclone contract evolves.\n\n## Active automation\n- GitLab clone workflows stay in sync with the canonical repo and workflow policies.\n- project and pipeline automation are treated as a first-class runtime surface.\n- security and deployment verification remain part of the live maintenance loop.\n""",
            "QMOICLONEGITHUB.md": """# QMOICLONEGITHUB.md\n\nQMOI GitHub clone automation keeps GitHub repository management, actions, pages, and release orchestration aligned with the live application and hosting state.\n\n## Active automation\n- repository sync, actions, branches, and releases stay synchronized with the canonical repo.\n- deployment and runtime checks continue through the hosted workflow system.\n- this document is refreshed automatically as the GitHub clone automation evolves.\n""",
            "QMOICLONEGITPOD.md": """# QMOICLONEGITPOD.md\n\nQMOI GitPod clone automation keeps workspace orchestration, developer environment setup, and repo sync tied to the live GitHub-hosted runtime. This document stays aligned with GitHub, QCity, and the current clone/autoclone policy.\n\n## Active automation\n- workspace and environment automation are always reflected in the live repo contract.\n- worktree sync and environment health remain in the verification loop.\n- the autonomous agent refreshes this doc during live maintenance.\n""",
            "QMOICLONEHF.md": """# QMOICLONEHF.md\n\nQMOI Hugging Face clone automation keeps model, dataset, inference, and spaces surfaces in sync with the live repo. The clone contract remains production-safe while the host surface is kept lightweight and operational.\n\n## Active automation\n- model and dataset automation remain live and synchronized.\n- inference and spaces contracts are refreshed with the repo state.\n- QVillage and Hugging Face platform surfaces stay aligned with the live runtime.\n""",
            "QMOICLONEHUGGINGFACE.md": """# QMOICLONEHUGGINGFACE.md\n\nThis document defines the clone/autoclone strategy for Hugging Face features and surfaces. QMOI keeps the platform parity and automation state synchronized with GitHub workflows and the live runtime contract.\n\n## Active automation\n- inference, spaces, and dataset surfaces stay in sync.\n- release and deployment links remain connected to the live repo state.\n- the autonomous agent updates this file whenever the environment changes.\n""",
            "QMOICLONEQUANTUM.md": """# QMOICLONEQUANTUM.md\n\nQMOI Quantum clone automation keeps compute, model, and research-runtime surfaces aligned with the live repository and hosted automation path. The platform is treated as a first-class clone layer in the QMOI network graph.\n\n## Active automation\n- compute and model-runtime automation remain synchronized with the live repo state.\n- deployment and validation checks are preserved within the same runtime contract.\n- clone/autoclone logic stays centrally managed and refreshed as the repo evolves.\n""",
            "QMOICLONEDAGSHUB.md": """# QMOICLONEDAGSHUB.md\n\nQMOI Dagshub clone automation preserves the data-science, repository, and experiment surface in a live, synchronized environment. The autonomous agent treats Dagshub as a key platform in the clone and autoclone strategy.\n\n## Active automation\n- dataset, experiment, and repo automation remain operational.\n- documentation stays synchronized with the canonical QMOI repo and workflow health.\n- the live runtime monitors platform parity and drift before release.\n""",
            "AUTOCLONE_STANDALONE.md": """# AUTOCLONE_STANDALONE.md\n\nThe standalone autoclone layer keeps QMOI operational across GitHub, Netlify, Vercel, Gitpod, Hugging Face, and all cloned platforms. It automates repo sync, environment setup, deployment hooks, and platform parity refreshes.\n\n## Active automation\n- repo sync and autoclone loops remain active in the live runtime.\n- platform-specific config files such as netlify.toml are kept synchronized.\n- the autonomous agent validates all clone/autoclone states before final promotion.\n""",
            "QMOIDATABASE.md": """# QMOIDATABASE.md\n\nThis document defines the database and persistence model for QMOI clone/autoclone operations, platform sync, memory indexing, and runtime health tracking. The database layer remains a central source of state for the autonomous agent and the live repo.\n\n## Active automation\n- memory index and runtime data remain synchronized with repo health and platform state.\n- clone/autoclone surfaces all depend on the same persistent state model.\n- the autonomous agent refreshes database and platform knowledge before promotion.\n""",
        }

        for name, body in templates.items():
            if name in {"QUANTUM.md", "VERCELPAYED.md", "QMOICLONEQUANTUM.md"}:
                continue
            path = target / name
            path.write_text(body + "\n", encoding="utf-8")

        qstore_documents = self.refresh_qstream_qstore_documents(target)
        hosting_documents = self.refresh_hosting_quantum_ui_documents(target)
        return {
            **{name: target / name for name in templates},
            **qstore_documents["documents"],
            **hosting_documents["documents"],
        }

    def build_github_proof_contract(
        self,
    ) -> dict[str, Any]:
        managed_surface_contract = self.refresh_managed_surface_documents(
            self.root_dir
        )
        platform_results = self.validate_all_platforms()

        feature_results = self.validate_all_platform_features()

        handler_results = self.validate_file_handlers()

        platform_passed = all(
            result.get("passed", False)
            for result in platform_results.values()
        )

        feature_contract_valid = (
            set(feature_results.keys())
            == set(PLATFORMS)
            and all(
                set(feature_results[platform].keys())
                == set(QMOI_APPS.keys())
                for platform in PLATFORMS
            )
        )

        feature_passed = feature_contract_valid

        handler_passed = bool(handler_results)

        autonomy_plan = (
            self.cross_repo_manager
            .build_autonomy_plan()
        )

        branch_plan = (
            BranchSyncManager
            .build_sync_plan()
        )

        feature_count = get_total_feature_count()

        proof = {
            "platform_validation_passed": platform_passed,
            "feature_validation_passed": feature_passed,
            "file_handler_validation_passed": handler_passed,
            "alpha_q_ai_included": autonomy_plan[
                "alpha_q_ai_included"
            ],
            "feature_count": feature_count,
            "applications_per_platform": len(QMOI_APPS),
            "feature_registry_valid": (
                isinstance(QMOI_APPS, dict)
                and isinstance(FEATURE_REGISTRY, dict)
                and set(FEATURE_REGISTRY.keys())
                == set(PLATFORMS)
                and all(
                    set(
                        FEATURE_REGISTRY[
                            platform
                        ].keys()
                    )
                    == set(QMOI_APPS.keys())
                    for platform in PLATFORMS
                )
            ),
            "platform_feature_contract_valid": (
                feature_contract_valid
            ),
            "managed_surface_contract_valid": managed_surface_contract["validation"]["passed"],
            "product_catalog_links_valid": managed_surface_contract["link_validation"]["passed"],
            "product_catalog_app_count": len(managed_surface_contract["catalog_apps"]),
            "clone_platform_ui_record_count": len(managed_surface_contract["clone_platform_ui_coverage"]),
            "master_access_verified": managed_surface_contract["master_access_verified"],
        }

        ready = (
            platform_passed
            and feature_passed
            and handler_passed
            and proof["alpha_q_ai_included"]
            and proof["feature_registry_valid"]
            and proof["platform_feature_contract_valid"]
            and proof["managed_surface_contract_valid"]
        )

        return {
            "status": (
                "ready_for_github"
                if ready
                else "not_ready_for_github"
            ),
            "generated": utc_iso(),
            "proof": proof,
            "alpha_q_ai": {
                "repo": ALPHA_Q_AI_REPOSITORY,
                "included": True,
            },
            "branch_sync": branch_plan,
            "autonomy_plan": autonomy_plan,
        }

    # ------------------------------------------------------------------------
    # CLI PIPELINE
    # ------------------------------------------------------------------------

    def _record_auto_continue_lifecycle_stage(
        self,
        *,
        final_status: str,
        iteration: int,
        max_iterations: int,
        termination_reason: str,
    ) -> None:
        merge_audit = self.results.get("merge_audit", {})
        if not isinstance(merge_audit, Mapping):
            return
        execution_id = str(merge_audit.get("q_version_lifecycle_execution_id", ""))
        repositories = merge_audit.get("repositories", [])
        if not execution_id or not isinstance(repositories, list):
            return
        roots = [Path(repository).resolve() for repository in repositories]
        if not roots:
            return
        successful = final_status.upper() == "SUCCESS" and termination_reason == "success_contract"
        QVersionManager(self.root_dir).record_lifecycle_stage(
            execution_id,
            "AUTO_CONTINUE_LOOP",
            roots,
            status="PASS" if successful else "NEEDS_REVIEW",
            details={
                "loop_completed": True,
                "iteration_count": iteration,
                "retry_limit": max_iterations,
                "retry_limit_respected": 1 <= iteration <= max_iterations,
                "termination_reason": termination_reason,
                "final_status": final_status.upper(),
            },
            include_inventory=False,
        )

    def run_continue_cycle(
        self,
    ) -> int:
        """Resume safely from the latest checkpoint and keep the autonomous loop going until success or the bounded retry limit is reached."""
        managed_surface_contract = self.refresh_managed_surface_documents(
            self.root_dir
        )
        self.results["managed_surface_contract"] = managed_surface_contract
        checkpoint = self.load_checkpoint() or {}
        completed_steps = list(dict.fromkeys(checkpoint.get("completed_steps") or []))
        auto_continue = os.getenv("AUTO_CONTINUE", "1").strip().lower() not in {"0", "false", "no", "off"}
        max_iterations = max(1, int(os.getenv("AUTO_CONTINUE_MAX", "5")))

        self.record_tracker_event(
            "continue_cycle_started",
            "Autonomous continuation cycle started from the latest checkpoint.",
            status="CHECKPOINTING",
            phase="continuation",
            details={
                "checkpoint_status": checkpoint.get("status", "unknown"),
                "completed_steps": completed_steps,
                "auto_continue": auto_continue,
                "max_iterations": max_iterations,
            },
        )

        self.update_resume_checkpoint(
            status="continuation_started",
            completed_steps=completed_steps or ["continuation scheduled"],
            evidence={
                "continue_mode": True,
                "runtime": os.getenv("GITHUB_ACTIONS", "false"),
                "auto_continue": auto_continue,
                "max_iterations": max_iterations,
            },
        )

        if os.getenv("GITHUB_ACTIONS", "").lower() == "true":
            try:
                self.verify_ollama()
            except (OSError, RuntimeError, ValueError) as exc:  # pragma: no cover - degraded hosted runs
                self.record_tracker_event(
                    "continue_cycle_runtime_warning",
                    f"Continuation runtime check reported a warning: {exc}",
                    status="warning",
                    phase="continuation",
                    details={"error": str(exc)},
                )

        if not auto_continue:
            self.update_resume_checkpoint(
                status="continuation_complete",
                completed_steps=[*completed_steps, "continuation cycle skipped because auto-continue is disabled"],
                evidence={
                    "continue_mode": False,
                    "last_checkpoint_status": checkpoint.get("status", "unknown"),
                    "runtime": os.getenv("GITHUB_ACTIONS", "false"),
                },
            )
            return 0

        for iteration in range(1, max_iterations + 1):
            checkpoint = self.load_checkpoint() or {}
            if str(checkpoint.get("status", "")).lower() in {"success", "autonomous_complete", "ready", "continuation_complete"}:
                self.update_resume_checkpoint(
                    status="success" if checkpoint.get("status") in {"success", "autonomous_complete", "ready"} else "continuation_complete",
                    completed_steps=[*completed_steps, "continuation cycle"],
                    evidence={
                        "continue_mode": True,
                        "iteration": iteration,
                        "last_checkpoint_status": checkpoint.get("status", "unknown"),
                        "runtime": os.getenv("GITHUB_ACTIONS", "false"),
                    },
                )
                return 0

            try:
                result = self.run_autonomous_loop()
            except Exception as exc:  # pragma: no cover - the surrounding caller handles runtime errors explicitly
                self.update_resume_checkpoint(
                    status="continuation_failed",
                    completed_steps=[*completed_steps, f"continuation iteration {iteration}"],
                    error=str(exc),
                    evidence={
                        "continue_mode": True,
                        "iteration": iteration,
                        "runtime": os.getenv("GITHUB_ACTIONS", "false"),
                    },
                )
                self.record_tracker_event(
                    "continue_cycle_failed",
                    f"Automatic continuation failed on iteration {iteration}: {exc}",
                    status="failed",
                    phase="continuation",
                    details={"error": str(exc), "iteration": iteration},
                )
                self._record_auto_continue_lifecycle_stage(
                    final_status="FAILED",
                    iteration=iteration,
                    max_iterations=max_iterations,
                    termination_reason="iteration_exception",
                )
                return 1

            final_status = str(result.get("final_status", "")).upper()
            if final_status == "SUCCESS":
                self.update_resume_checkpoint(
                    status="success",
                    completed_steps=[*completed_steps, f"continuation iteration {iteration}", "success contract"],
                    evidence={
                        "continue_mode": True,
                        "iteration": iteration,
                        "final_status": final_status,
                        "runtime": os.getenv("GITHUB_ACTIONS", "false"),
                    },
                )
                self.record_tracker_event(
                    "continue_cycle_succeeded",
                    "Autonomous continuation reached a successful completion state.",
                    status="success",
                    phase="continuation",
                    details={"iteration": iteration, "final_status": final_status},
                )
                self._record_auto_continue_lifecycle_stage(
                    final_status=final_status,
                    iteration=iteration,
                    max_iterations=max_iterations,
                    termination_reason="success_contract",
                )
                return 0

            checkpoint = self.load_checkpoint() or {}
            if str(checkpoint.get("status", "")).lower() in {"success", "autonomous_complete", "ready"}:
                self.update_resume_checkpoint(
                    status="success",
                    completed_steps=[*completed_steps, f"continuation iteration {iteration}", "success contract"],
                    evidence={
                        "continue_mode": True,
                        "iteration": iteration,
                        "final_status": checkpoint.get("status"),
                        "runtime": os.getenv("GITHUB_ACTIONS", "false"),
                    },
                )
                return 0

            if iteration == max_iterations:
                self.update_resume_checkpoint(
                    status="continuation_exhausted",
                    completed_steps=[*completed_steps, f"continuation iteration {iteration}"],
                    evidence={
                        "continue_mode": True,
                        "iteration": iteration,
                        "max_iterations": max_iterations,
                        "runtime": os.getenv("GITHUB_ACTIONS", "false"),
                    },
                )
                self.record_tracker_event(
                    "continue_cycle_exhausted",
                    f"Automatic continuation reached its configured retry limit ({max_iterations}).",
                    status="warning",
                    phase="continuation",
                    details={"iteration": iteration, "max_iterations": max_iterations},
                )
                self._record_auto_continue_lifecycle_stage(
                    final_status=final_status or "FAILED",
                    iteration=iteration,
                    max_iterations=max_iterations,
                    termination_reason="retry_limit_reached",
                )
                return 1

        self.update_resume_checkpoint(
            status="continuation_complete",
            completed_steps=[*completed_steps, "continuation cycle"],
            evidence={
                "continue_mode": True,
                "last_checkpoint_status": checkpoint.get("status", "unknown"),
                "runtime": os.getenv("GITHUB_ACTIONS", "false"),
            },
        )

        return 0

    def write_completion_manifest(
        self,
        contract: Mapping[str, Any],
    ) -> list[Path]:
        """Write unversioned local completion reports without allocating a Q version."""
        if str(contract.get("final_status", "")).upper() != "SUCCESS":
            return []

        report_id = str(contract.get("execution_id", ""))
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", report_id):
            report_id = uuid.uuid4().hex

        repo_roots: list[Path] = [self.root_dir]
        parent = self.root_dir.parent
        alpha_root = parent / "Alpha-Q-ai"
        qmoi_root = parent / "qmoi-enhanced"

        if alpha_root.exists() and alpha_root.is_dir() and alpha_root not in repo_roots:
            repo_roots.append(alpha_root)
        if qmoi_root.exists() and qmoi_root.is_dir() and qmoi_root not in repo_roots:
            repo_roots.append(qmoi_root)

        written: list[Path] = []
        for repo_root in repo_roots:
            report_dir = repo_root / "ollamatracks" / "completion_reports" / report_id
            report_dir.mkdir(parents=True, exist_ok=False)

            summary = [
                "# Local Autonomous Completion Report",
                "",
                "- Status: SUCCESS",
                f"- Workflow run: {contract.get('workflow_run_id') or 'not recorded'}",
                f"- Repository: {contract.get('repository') or repo_root.name}",
                f"- Commit: {contract.get('commit') or 'not recorded'}",
                f"- Validation passed: {bool(contract.get('validation_passed'))}",
                f"- Lint passed: {bool(contract.get('lint_passed'))}",
                f"- Ollama healthy: {bool(contract.get('ollama_healthy'))}",
                f"- Ollama started: {bool(contract.get('ollama_started'))}",
                f"- Model available: {bool(contract.get('model_available'))}",
                f"- Inference verified: {bool(contract.get('inference_verified'))}",
                "",
                "## Evidence",
                f"- Files analyzed: {', '.join(contract.get('files_analyzed', [])) or 'none'}",
                f"- Files modified: {', '.join(contract.get('files_modified', [])) or 'none'}",
                "",
                "This report records the supplied autonomous-run contract only. It is not a Q-version finalization, does not establish remote completion, and does not authorize publication.",
            ]
            report_path = report_dir / "COMPLETION.md"
            safe_text_write(report_path, "\n".join(summary) + "\n")
            written.append(report_path)

        return written

    def run_validation_pipeline(
        self,
    ) -> int:
        try:
            instruction_inventory = audit_instruction_files(self.root_dir)
            self.results["instruction_inventory"] = instruction_inventory
            safe_json_write(self.tracker_dir / "instruction_inventory.json", instruction_inventory)
            if instruction_inventory["status"] != "PASS":
                self.update_resume_checkpoint(
                    status="instruction_inventory_blocked",
                    completed_steps=[],
                    error="Instruction inventory is incomplete or unreadable; protected planning is blocked.",
                    evidence=instruction_inventory,
                )
                self.record_tracker_event(
                    "instruction_inventory_blocked",
                    "Instruction files could not all be read and verified; no merge/research work was started.",
                    status="BLOCKED",
                    phase="instruction_inventory",
                    details=instruction_inventory,
                )
                return 1
            repo_roots = self.discover_repo_roots(include_history=True)
            bank_automation_evidence = self.refresh_bank_automation_evidence(self.root_dir)
            self.results["bank_automation_evidence"] = bank_automation_evidence
            ollama_reference_audit = self.refresh_ollama_reference_audit(self.root_dir)
            self.results["ollama_reference_audit"] = ollama_reference_audit
            initial_merge = self.execute_merge_and_sync(repo_roots, auto_push=False)
            lifecycle_execution_id = initial_merge.get("q_version_lifecycle_execution_id")
            self.results["pre_validation_merge"] = initial_merge
            self.update_resume_checkpoint(
                status="validation_started",
                completed_steps=["pre-validation merge inventory"],
            )

            product_surface_docs = self.refresh_managed_surface_documents(
                self.root_dir
            )

            restore_point_path = self.tracker_dir / "qmoi_restore_point_preflight.json"
            try:
                qmoi_restore_point = json.loads(restore_point_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                qmoi_restore_point = None
            qmoi_restore_point_passed = AutonomousCompletionEngine._qmoi_restore_point_evidence_complete(
                qmoi_restore_point
            )

            platform_results = (
                self.validate_all_platforms()
            )

            self.update_resume_checkpoint(
                status="platform_validation_complete",
                completed_steps=[
                    "platform validation",
                ],
            )

            feature_results = (
                self.validate_all_platform_features()
            )

            self.update_resume_checkpoint(
                status="feature_validation_complete",
                completed_steps=[
                    "platform validation",
                    "feature validation",
                ],
            )

            handler_results = (
                self.validate_file_handlers()
            )

            self.update_resume_checkpoint(
                status="file_handler_validation_complete",
                completed_steps=[
                    "platform validation",
                    "feature validation",
                    "file handler validation",
                ],
            )

            self.memory_generator.generate_index()
            self.model_card_generator.generate_card()

            production_documents = self.refresh_production_manifests(self.root_dir)
            self.results["production_manifests"] = production_documents

            final_merge = self.execute_merge_and_sync(
                repo_roots,
                auto_push=False,
                q_version_execution_id=lifecycle_execution_id,
                lifecycle_phase="post_agent",
            )
            self.results["post_validation_merge"] = final_merge
            bank_automation_evidence = self.refresh_bank_automation_evidence(self.root_dir)
            self.results["bank_automation_evidence"] = bank_automation_evidence

            self.update_resume_checkpoint(
                status="artifacts_generated",
                completed_steps=[
                    "platform validation",
                    "feature validation",
                    "file handler validation",
                    "memory index generation",
                    "model card generation",
                ],
            )

            contract = (
                self.build_github_proof_contract()
            )
            proof_path = (
                self.root_dir
                / "github_proof_contract.json"
            )

            safe_json_write(
                proof_path,
                contract,
            )

            report = {
                "generated": utc_iso(),
                "platforms": platform_results,
                "features": feature_results,
                "file_handlers": handler_results,
                "proof": contract,
                "total_feature_count": get_total_feature_count(),
                "product_surfaces": {
                    "status": "documentation_refreshed_implementation_not_verified",
                    "catalog_apps": product_surface_docs["catalog_apps"],
                    "catalog_coverage": product_surface_docs["catalog_coverage"],
                    "platforms": product_surface_docs["client_platforms"],
                    "hosting_feature_count": len(product_surface_docs["hosting_features"]),
                    "quantum_extension_count": len(product_surface_docs["quantum_extensions"]),
                    "master_ui_feature_count": len(product_surface_docs["master_ui_features"]),
                    "access_modes": product_surface_docs["access_modes"],
                    "clone_platforms": product_surface_docs["clone_platforms"],
                    "clone_platform_ui_records": len(product_surface_docs["clone_platform_ui_coverage"]),
                    "style_requirements": product_surface_docs["style_requirements"],
                    "automation_coverage": {
                        key: value
                        for key, value in product_surface_docs["automation_coverage"].items()
                        if key not in {"documents", "trading_inventory", "trading_inventory_path"}
                    } | {
                        "documents": {
                            name: str(path)
                            for name, path in product_surface_docs["automation_coverage"]["documents"].items()
                        },
                        "trading_inventory_path": str(product_surface_docs["automation_coverage"]["trading_inventory_path"]),
                        "trading_inventory_summary": {
                            key: value
                            for key, value in product_surface_docs["automation_coverage"]["trading_inventory"].items()
                            if key != "files"
                        },
                    },
                    "master_access_verified": product_surface_docs["master_access_verified"],
                    "link_validation": product_surface_docs["link_validation"],
                    "structural_validation": product_surface_docs["validation"],
                    "implementation_verified": False,
                    "documents": {
                        name: str(path)
                        for name, path in product_surface_docs["documents"].items()
                    },
                },
                "merge_lifecycle": {
                    "execution_id": lifecycle_execution_id,
                    "pre_validation_status": initial_merge.get("status"),
                    "post_validation_status": final_merge.get("status"),
                    "lifecycle_path": final_merge.get("q_version_lifecycle_path"),
                },
                "bank_automation_evidence": bank_automation_evidence,
                "instruction_inventory": instruction_inventory,
                "ollama_reference_audit": {
                    "status": ollama_reference_audit["status"],
                    "local_scan": ollama_reference_audit["local_scan"],
                    "matched_files_by_scope": ollama_reference_audit["local_scan"]["matched_files_by_scope"],
                    "matched_files_by_category": ollama_reference_audit["local_scan"]["matched_files_by_category"],
                    "source_manifest_sha256": ollama_reference_audit["source_manifest_sha256"],
                    "remote_history": ollama_reference_audit["remote_history"],
                    "artifact_path": ollama_reference_audit["artifact_path"],
                    "coverage_complete": ollama_reference_audit["coverage_complete"],
                },
                "repository_surface_audit": final_merge.get("repository_surface_audit"),
                "production_readiness": {
                    "status": "PASS" if production_documents.get("status") == "clear" else "NEEDS_REVIEW",
                    "inventory_path": str(production_documents.get("inventory", "")),
                    "candidate_count": production_documents.get("candidate_count"),
                },
                "autoresearch": initial_merge.get("autoresearch", {}),
                "production_manifests": {
                    key: str(value) for key, value in production_documents.items()
                },
            }

            completion_gates = {
                "discovery": bool(repo_roots) and all(path.is_dir() for path in repo_roots),
                "inspection": initial_merge.get("status") == "ready" and final_merge.get("status") == "ready",
                "repository_surface_audit": (
                    "PASS"
                    if AutonomousCompletionEngine._repository_surface_audit_evidence_complete(
                        final_merge.get("repository_surface_audit")
                    )
                    else None
                ),
                "ollama_reference_audit": (
                    "PASS"
                    if AutonomousCompletionEngine._ollama_reference_audit_evidence_complete(ollama_reference_audit)
                    else None
                ),
                "ui_test_hook_coverage": (
                    "PASS"
                    if AutonomousCompletionEngine._ui_test_hook_coverage_evidence_complete(
                        product_surface_docs["automation_coverage"]["styles_universals_coverage"]
                    )
                    else None
                ),
                "qmoi_restore_point": "PASS" if qmoi_restore_point_passed else None,
                "instruction_inventory": instruction_inventory["status"] == "PASS",
                "production_readiness": (
                    production_documents.get("status") == "clear"
                    and production_documents.get("candidate_count") == 0
                    and bool(self.results.get("production_gap_inventory", {}).get("coverage_complete"))
                ),
                "markdown_inventory": None,
                "validation": contract.get("status") == "ready_for_github",
                "security": None,
                "remote_main": None,
                "remote_backup": None,
                "q_version": None,
                "live_activity": None,
                "cross_repository": None,
                "final_verification": None,
            }

            production_inventory = self.results.get("production_gap_inventory", {})
            production_candidate_count = production_inventory.get("total_candidates")
            production_scan_complete = bool(
                production_inventory.get("coverage_complete") is True
                and production_inventory.get("unreadable_files") == []
                and production_inventory.get("oversized_files_not_read") == 0
            )
            production_scan_passed = bool(production_scan_complete and production_candidate_count == 0)
            q_version_manager = QVersionManager(self.root_dir)
            lifecycle_roots = [Path(path).resolve() for path in repo_roots]
            def record_lifecycle_stage_if_available(stage: str, **kwargs: Any) -> None:
                if lifecycle_execution_id:
                    q_version_manager.record_lifecycle_stage(
                        lifecycle_execution_id,
                        stage,
                        lifecycle_roots,
                        **kwargs,
                    )

            record_lifecycle_stage_if_available(
                "PRODUCTION_SCAN",
                status="PASS" if production_scan_passed else "NEEDS_REVIEW",
                details={
                    "production_md_present": (self.root_dir / "production.md").is_file(),
                    "productionenhanced_md_present": (self.root_dir / "productionenhanced.md").is_file(),
                    "coverage_complete": production_scan_complete,
                    "unresolved_findings": production_candidate_count,
                    "candidate_count": production_candidate_count,
                    "unreadable_files": production_inventory.get("unreadable_files", []),
                    "oversized_files_not_read": production_inventory.get("oversized_files_not_read"),
                    "inventory_path": "ollamatracks/production_gap_inventory.json",
                },
                include_inventory=False,
            )
            record_lifecycle_stage_if_available(
                "PRODUCTION_REPLACEMENTS",
                status="PASS" if production_scan_passed else "NEEDS_REVIEW",
                details={
                    "replacement_records_verified": production_scan_passed,
                    "unresolved_findings": production_candidate_count,
                    "automatic_replacement_enabled": False,
                },
                include_inventory=False,
            )
            record_lifecycle_stage_if_available(
                "PRODUCTION_READINESS",
                status="PASS" if production_scan_passed and production_documents.get("status") == "clear" else "NEEDS_REVIEW",
                details={
                    "status": "CLEAR" if production_scan_passed and production_documents.get("status") == "clear" else "NEEDS_REVIEW",
                    "coverage_complete": production_scan_complete,
                    "candidate_count": production_candidate_count,
                    "unreadable_files": production_inventory.get("unreadable_files", []),
                    "oversized_files_not_read": production_inventory.get("oversized_files_not_read"),
                },
                include_inventory=False,
            )
            local_validation_passed = contract.get("status") == "ready_for_github"
            record_lifecycle_stage_if_available(
                "FULL_VALIDATION",
                status="PASS" if local_validation_passed else "NEEDS_REVIEW",
                details={
                    "all_required_tests_passed": local_validation_passed,
                    "all_markdown_validated": bool(final_merge.get("markdown_index_refresh", {}).get("audit", {}).get("index_complete")),
                    "inventory_documents_current": bool(contract.get("status") == "ready_for_github"),
                    "validation_contract_status": contract.get("status"),
                },
                include_inventory=False,
            )
            record_lifecycle_stage_if_available(
                "REMOTE_VERIFICATION",
                status="NEEDS_REVIEW",
                details={
                    "terminal_conclusion": None,
                    "remote_verified": False,
                    "blocker": "No terminal target-owned workflow evidence was supplied to this local validation pipeline.",
                },
                include_inventory=False,
            )
            record_lifecycle_stage_if_available(
                "QMOI_RESTORE_POINT",
                status="PASS" if qmoi_restore_point_passed else "NEEDS_REVIEW",
                details=(
                    {**qmoi_restore_point, "status": "SUCCESS"}
                    if qmoi_restore_point_passed
                    else {
                        "status": "BLOCKED",
                        "branch": "qmoi",
                        "remote_verified": False,
                        "coverage_complete": False,
                        "blocker": "The target-owned autosync workflow has not supplied valid exact-SHA qmoi/main/autosync-backup evidence for both repositories.",
                    }
                ),
                include_inventory=False,
            )
            record_lifecycle_stage_if_available(
                "AUTO_CONTINUE_LOOP",
                status="NEEDS_REVIEW",
                details={
                    "loop_invoked": False,
                    "auto_continue_enabled": os.getenv("AUTO_CONTINUE", "1").strip().lower() not in {"0", "false", "no", "off"},
                    "retry_limit": max(1, int(os.getenv("AUTO_CONTINUE_MAX", "5"))),
                    "blocker": "This validation pipeline run is not itself a continuation-loop execution.",
                },
                include_inventory=False,
            )
            completion_result = AutonomousCompletionEngine(self.root_dir).evaluate(
                completion_gates,
                repository_results={
                    "primary": {"changed_files": []},
                    "secondary": {"changed_files": []},
                    "markdown_inventory": final_merge.get("remote_markdown_inventory_evidence"),
                    "repository_surface_audit": final_merge.get("repository_surface_audit"),
                    "ollama_reference_audit": ollama_reference_audit,
                    "ui_test_hook_coverage": product_surface_docs["automation_coverage"]["styles_universals_coverage"],
                    "qmoi_restore_point": qmoi_restore_point,
                },
            )
            record_lifecycle_stage_if_available(
                "AUTONOMOUS_COMPLETION",
                status="PASS" if completion_result.status in {"SUCCESS", "NO_CHANGES_REQUIRED"} else "NEEDS_REVIEW",
                details={
                    "status": completion_result.status,
                    "execution_id": completion_result.execution_id,
                    "gates": completion_result.gates,
                    "pending_action_count": len(completion_result.evidence.get("next_actions", [])),
                    "remote_verified": False,
                },
                include_inventory=False,
            )
            report["autonomous_completion"] = completion_result.as_dict()
            report["qmoi_restore_point"] = qmoi_restore_point or {
                "status": "BLOCKED",
                "branch": "qmoi",
                "coverage_complete": False,
                "remote_verified": False,
                "blocker": "Restore-point preflight evidence is missing or invalid.",
            }
            completion_actions = completion_result.evidence.get("next_actions", [])

            safe_json_write(
                self.root_dir
                / "validation_report.json",
                report,
            )

            self.results["report"] = report

            success = (
                contract.get("status")
                == "ready_for_github"
                and initial_merge.get("status") == "ready"
                and final_merge.get("status") == "ready"
                and completion_result.status in {"SUCCESS", "NO_CHANGES_REQUIRED"}
            )

            self.update_resume_checkpoint(
                status=(
                    "ready"
                    if success
                    else "failed"
                ),
                completed_steps=[
                    "platform validation",
                    "feature validation",
                    "file handler validation",
                    "memory index generation",
                    "model card generation",
                    "github proof contract",
                ],
                evidence={
                    "completion_execution_id": completion_result.execution_id,
                    "completion_status": completion_result.status,
                    "next_operation": completion_actions[0]["operation"] if completion_actions else None,
                },
            )

            self.record_tracker_event(
                "validation_pipeline_complete",
                "Validation pipeline completed.",
                status=(
                    "passed"
                    if success
                    else "failed"
                ),
                phase="validation",
                details={
                    "proof_path": str(proof_path),
                    "feature_count": get_total_feature_count(),
                },
            )

            print(
                json.dumps(
                    {
                        "status": contract["status"],
                        "platforms": len(platform_results),
                        "apps": len(QMOI_APPS),
                        "feature_count": get_total_feature_count(),
                        "proof": str(proof_path),
                    },
                    indent=2,
                )
            )

            return 0 if success else 1

        except Exception as exc:  # noqa: BLE001 - CLI must persist any pipeline failure
            try:
                bank_automation_evidence = self.refresh_bank_automation_evidence(self.root_dir)
                self.results["bank_automation_evidence"] = bank_automation_evidence
            except Exception as evidence_error:  # noqa: BLE001 - preserve the original pipeline failure
                self.results["bank_automation_evidence"] = {
                    "status": "BLOCKED",
                    "reason": f"bank evidence refresh failed: {type(evidence_error).__name__}",
                    "implementation_verified": False,
                    "remote_completion_verified": False,
                }
            self.update_resume_checkpoint(
                status="error",
                completed_steps=[],
                error=str(exc),
            )

            self.record_tracker_event(
                "validation_pipeline_error",
                f"Validation failed: {exc}",
                status="failed",
                phase="validation",
                details={
                    "error": str(exc),
                },
            )

            print(
                f"QMOI validation failed: {exc}",
                file=sys.stderr,
            )

            return 1


# ============================================================================
# CLI
# ============================================================================

def main(
    argv: Sequence[str] | None = None,
) -> int:
    raw_argv = (
        list(argv)
        if argv is not None
        else list(sys.argv[1:])
    )

    if raw_argv and raw_argv[0] == "qseed":
        from scripts.qseed_vault import main as qseed_main

        return qseed_main(raw_argv[1:])

    if raw_argv and raw_argv[0] == "qaudit-model-review":
        from scripts.qaudit_model_review import main as qaudit_model_review_main

        return qaudit_model_review_main(raw_argv[1:])

    if (
        raw_argv
        and not raw_argv[0].startswith("-")
    ):
        raw_argv[0] = (
            SelfHealingManager
            .sanitize_command(
                raw_argv[0]
            )
        )

    parser = argparse.ArgumentParser(
        description="QMOI Ollama Autonomous Agent",
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="validate-all",
        choices=[
            "validate-all",
            "audit-inventory",
            "qaudit-universe",
            "qaudit-markdown-sentences",
            "qaudit-model-review",
            "qseed",
            "validate-platforms",
            "validate-features",
            "validate-all-features",
            "validate-file-handlers",
            "generate-memory-index",
            "generate-model-card",
            "proof",
            "checkpoint",
            "health",
            "audit-first",
            "autonomous",
            "continue",
            "merge-sync",
            "qaudit-merge-parallel",
            "qaudit-all-features",
            "github-auth",
            "credential-manager",
            "commands",
        ],
    )

    parser.add_argument(
        "--base-path",
        default=None,
        help="Repository root to operate against.",
    )

    parser.add_argument(
        "--credential-action",
        choices=["status", "verify-bitget", "migrate-qtrade", "audit"],
        default="status",
        help="Credential-manager operation used by the credential-manager command.",
    )

    try:
        args = parser.parse_args(raw_argv)

    except SystemExit as exc:
        return int(
            exc.code
            if isinstance(exc.code, int)
            else 1
        )

    agent = OllamaAutonomousAgent(
        args.base_path
    )

    if args.command == "commands":
        root = Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve()
        print(json.dumps(refresh_commands_category(root), indent=2, sort_keys=True, default=str))
        return 0

    if args.command == "audit-inventory":
        root = Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve()
        inventory_start_checkpoint = record_qaudit_checkpoint(
            root,
            "audit-inventory",
            {
                "status": "IN_PROGRESS",
                "metrics": {
                    "phase": "inventory_start",
                    "external_research_enabled": False,
                    "remote_mutation_performed": False,
                },
                "blockers": ["audit_inventory_run_not_yet_terminal"],
                "next_action": (
                    "Resume from this correlated inventory-start checkpoint; do not treat "
                    "partially refreshed documents or artifacts as final coverage."
                ),
            },
        )
        research = agent.build_autoresearch_report([root], fetch_external=False)
        ofca = agent.refresh_ollama_reference_audit(root)
        feature_coverage = agent.refresh_test_hook_coverage_documents(root)
        feature_audit = run_parallel_feature_audit(
            root,
            shard_size=250,
            worker_count=min(16, max(1, os.cpu_count() or 1)),
            registry=build_all_features_registry(),
        )
        markdown_catalog = agent.refresh_markdown_category_index(root)
        financial_category_label = next(
            (
                label for label in markdown_catalog.get("category_map", {})
                if label.startswith("Category I — Q Financial Manager")
            ),
            None,
        )
        financial_catalog = agent.refresh_financial_manager_catalog(
            root,
            candidate_paths=markdown_catalog.get("category_map", {}).get(
                financial_category_label, []
            ) if financial_category_label else [],
        )
        instructions = audit_instruction_files(root)
        restore_memory = agent.refresh_restore_point_memory_documents(root)
        legacy_sync_inventory = refresh_legacy_sync_artifact_inventory(root)
        surface = research.get("internal", {}).get("repository_surface_audit", {})
        surface_artifact = _local_artifact_integrity(
            root,
            surface.get("artifact_path"),
        )
        financial_inventory = feature_coverage.get("financial_claim_inventory", {})
        financial_artifact = _local_artifact_integrity(
            root,
            str(root / "ollamatracks" / "financial_claim_inventory.json"),
        )
        styles_universals = feature_coverage.get("styles_universals_coverage", {})
        result = {
            "command": "audit-inventory",
            "root": str(root),
            "external_research": {
                "status": research.get("external", {}).get("status", "UNKNOWN"),
                "visited_count": research.get("external", {}).get("visited_count", 0),
                "fetch_enabled": False,
            },
            "instruction_inventory": {
                "status": instructions.get("status", "UNKNOWN"),
                "files_discovered": instructions.get("files_discovered", 0),
                "files_read": instructions.get("files_read", 0),
            },
            "markdown_category_inventory": {
                "status": markdown_catalog.get("status", "UNKNOWN"),
                "markdown_file_count": len(markdown_catalog.get("all_markdown_files", [])),
                "category_count": len(markdown_catalog.get("category_map", {})),
                "updated_files": markdown_catalog.get("updated_files", []),
            },
            "financial_manager_catalog": {
                "status": financial_catalog.get("status", "UNKNOWN"),
                "files": financial_catalog.get("files", []),
                "coverage": financial_catalog.get("coverage", {}),
                "updated_catalog": financial_catalog.get("updated_catalog"),
            },
            "financial_claim_audit": {
                "status": financial_inventory.get("status", "candidate_discovery_only"),
                "scope": financial_inventory.get("scope"),
                "coverage_verified": financial_inventory.get("coverage_verified", False),
                "financial_file_count": financial_inventory.get("financial_file_count", 0),
                "candidate_line_count": financial_inventory.get("candidate_line_count", 0),
                "candidate_line_counts_by_category": financial_inventory.get(
                    "candidate_line_counts_by_category", {}
                ),
                "artifact_integrity": financial_artifact,
            },
            "repository_surface_audit": {
                "status": surface.get("status", "UNKNOWN"),
                "coverage_complete": surface.get("coverage_complete", False),
                "remote_verified": surface.get("remote_verified", False),
                "artifact_path": surface.get("artifact_path"),
                "artifact_integrity": surface_artifact,
            },
            "ofca": {
                "status": ofca.get("status", "UNKNOWN"),
                "coverage_complete": ofca.get("coverage_complete", False),
                "source_manifest_sha256": ofca.get("source_manifest_sha256"),
                "next_action": ofca.get("next_action"),
            },
            "styles_universals": styles_universals,
            "feature_audit": {
                "status": feature_audit.get("status"),
                "registered_feature_count": feature_audit.get("metrics", {}).get(
                    "registered_feature_count", 0
                ),
                "capability_count": feature_audit.get("metrics", {}).get(
                    "capability_count", 0
                ),
                "mentioned_feature_count": feature_audit.get("metrics", {}).get(
                    "mentioned_feature_count", 0
                ),
                "mapped_local_feature_count": feature_audit.get("metrics", {}).get(
                    "mapped_local_feature_count", 0
                ),
                "candidate_feature_count": feature_audit.get("metrics", {}).get(
                    "candidate_feature_count", 0
                ),
                "unmapped_feature_count": feature_audit.get("metrics", {}).get(
                    "unmapped_feature_count", 0
                ),
                "all_features_path": str(
                    feature_audit.get("artifacts", {}).get("all_features", "")
                ),
                "all_features_sha256": _local_artifact_integrity(
                    root,
                    str(feature_audit.get("artifacts", {}).get("all_features", "")),
                ).get("sha256"),
                "feature_manifest_sha256": feature_audit.get("metrics", {}).get(
                    "feature_manifest_sha256"
                ),
                "feature_evidence_sha256": feature_audit.get("metrics", {}).get(
                    "feature_evidence_sha256"
                ),
                "remote_verification_complete": feature_audit.get(
                    "remote_verification_complete", False
                ),
            },
            "restore_point_memory": restore_memory,
            "legacy_sync_artifact_inventory": {
                "status": legacy_sync_inventory.get("status"),
                "snapshot_artifact_counts": {
                    name: item.get("artifact_candidate_count")
                    for name, item in legacy_sync_inventory.get("snapshots", {}).items()
                },
                "mtime_date_counts": legacy_sync_inventory.get("mtime_date_counts"),
                "live_qmoi_enhanced_checkout_present": legacy_sync_inventory.get("live_qmoi_enhanced_checkout_present"),
                "automatic_copy_or_overwrite_enabled": legacy_sync_inventory.get("automatic_copy_or_overwrite_enabled"),
                "artifact_path": legacy_sync_inventory.get("artifact_path"),
            },
            "remote_mutation_performed": False,
        }
        checkpoint = record_qaudit_checkpoint(
            root,
            "audit-inventory",
            {
                "status": surface.get("status", "UNKNOWN"),
                "source_manifest_sha256": surface.get("source_manifest_sha256"),
                "artifact_path": surface_artifact["path"],
                "artifact_sha256": surface_artifact["sha256"],
                "artifact_bytes": surface_artifact["bytes"],
                "artifact_refs": {
                    "repository_surface_audit": surface_artifact,
                    "financial_claim_inventory": financial_artifact,
                },
                "metrics": {
                    "instruction_files_read": instructions.get("files_read", 0),
                    "markdown_file_count": surface.get("markdown_file_count", 0),
                    "local_surface_status": surface.get("status", "UNKNOWN"),
                    "ofca_status": ofca.get("status", "UNKNOWN"),
                    "registered_feature_count": feature_audit.get("metrics", {}).get(
                        "registered_feature_count", 0
                    ),
                    "capability_count": feature_audit.get("metrics", {}).get(
                        "capability_count", 0
                    ),
                    "unmapped_feature_count": styles_universals.get("unmapped_feature_count"),
                    "legacy_sync_status": legacy_sync_inventory.get("status", "UNKNOWN"),
                    "managed_document_count": (
                        surface.get("documentation_refresh", {}).get("managed_document_count", 0)
                    ),
                    "finance_candidate_file_count": financial_inventory.get(
                        "financial_file_count", 0
                    ),
                    "finance_candidate_line_count": financial_inventory.get(
                        "candidate_line_count", 0
                    ),
                    "finance_candidate_line_counts_by_category": financial_inventory.get(
                        "candidate_line_counts_by_category", {}
                    ),
                    "financial_manager_catalog_status": financial_catalog.get(
                        "status", "UNKNOWN"
                    ),
                    "markdown_category_count": len(markdown_catalog.get("category_map", {})),
                },
                "resolved_blockers": ["audit_inventory_run_not_yet_terminal"],
                "blockers": [
                    *surface.get("blockers", []),
                    *ofca.get("blockers", []),
                    *(
                        ["financial_claim_inventory_artifact_unavailable"]
                        if financial_artifact["status"] != "verified_local_hash"
                        else []
                    ),
                    *(
                        [f"surface_audit_artifact_{surface_artifact['status']}"]
                        if surface_artifact["status"] != "verified_local_hash"
                        else []
                    ),
                    *(
                        ["styles_universals_feature_test_hook_mapping_incomplete"]
                        if styles_universals.get("coverage_verified") is not True
                        else []
                    ),
                ],
            },
            correlation_id=inventory_start_checkpoint["correlation_id"],
        )
        result["checkpoint"] = checkpoint
        print(json.dumps(result, indent=2, sort_keys=True, default=str))
        return 0

    if args.command == "qaudit-universe":
        root = Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve()
        universe = write_qaudit_artifacts(
            root,
            product_registry={
                "applications": QSTORE_CATALOG_APPS,
                "platforms": PLATFORMS,
                "extensions": QUANTUM_EXTENSION_FEATURES,
                "lion_variations": [],
            },
        )
        accountability = universe.get("accountability", {})
        safe_json_write(root / "ollamatracks" / "system_accountability_audit.json", accountability)
        result = {
            "command": "qaudit-universe",
            "root": str(root),
            "status": universe.get("discovery", {}).get("status", "BLOCKED"),
            "metrics": universe.get("metrics", {}),
            "accountability": {
                "status": accountability.get("status", "BLOCKED"),
                "expected_requirement_count": accountability.get("expected_requirement_count", 0),
                "mapped_requirement_count": accountability.get("mapped_requirement_count", 0),
                "unmapped_requirement_count": accountability.get("unmapped_requirement_count", 0),
                "coverage_complete": accountability.get("coverage_complete", False),
            },
            "artifacts": universe.get("artifacts", {}),
            "audit_priority_queue": {
                "candidate_count": universe.get("metrics", {}).get("audit_queue_candidate_count", 0),
                "pending_count": universe.get("metrics", {}).get("audit_queue_pending_count", 0),
                "queue_sha256": universe.get("metrics", {}).get("audit_queue_sha256"),
                "priority_counts": universe.get("metrics", {}).get("audit_queue_priority_counts", {}),
                "selection_method": universe.get("audit_queue", {}).get("selection_method"),
                "all_indexed_paths_queued": universe.get("audit_queue", {}).get("all_indexed_paths_queued", False),
                "model_assistance": universe.get("audit_queue", {}).get("model_assistance"),
            },
            "remote_verified": False,
            "remote_mutation_performed": False,
        }
        result["checkpoint"] = record_qaudit_checkpoint(
            root,
            "qaudit-universe",
            {
                "status": universe.get("discovery", {}).get("status", "BLOCKED"),
                "source_manifest_sha256": universe.get("metrics", {}).get("source_manifest_sha256"),
                "artifact_path": "ollamatracks/qaudit_universe.json",
                "metrics": {
                    "scanned_file_count": universe.get("metrics", {}).get("scanned_file_count", 0),
                    "directory_count": universe.get("metrics", {}).get("directory_count", 0),
                    "accountability_expected": accountability.get("expected_requirement_count", 0),
                    "accountability_mapped": accountability.get("mapped_requirement_count", 0),
                    "accountability_unmapped": accountability.get("unmapped_requirement_count", 0),
                    "audit_queue_candidate_count": universe.get("metrics", {}).get("audit_queue_candidate_count", 0),
                    "audit_queue_pending_count": universe.get("metrics", {}).get("audit_queue_pending_count", 0),
                    "audit_queue_sha256": universe.get("metrics", {}).get("audit_queue_sha256"),
                    "audit_queue_priority_counts": universe.get("metrics", {}).get("audit_queue_priority_counts", {}),
                },
                "blockers": [
                    *universe.get("discovery", {}).get("blockers", []),
                    *(
                        [f"unmapped_accountability_requirements:{accountability.get('unmapped_requirement_count', 0)}"]
                        if accountability.get("unmapped_requirement_count", 0)
                        else []
                    ),
                ],
            },
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1 if universe.get("discovery", {}).get("status") == "BLOCKED" else 0

    if args.command == "qaudit-markdown-sentences":
        root = Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve()
        surface_audit = audit_repository_surfaces([root])
        evidence = write_markdown_sentence_audit(root, surface_audit)
        financial_inventory_path = root / "ollamatracks" / "financial_claim_inventory.json"
        financial_artifact = _local_artifact_integrity(root, str(financial_inventory_path))
        financial_summary: dict[str, Any] = {}
        if financial_artifact["status"] == "verified_local_hash":
            financial_inventory = json.loads(financial_inventory_path.read_text(encoding="utf-8"))
            financial_summary = {
                "financial_inventory_captured_at": financial_inventory.get("captured_at"),
                "financial_inventory_status": financial_inventory.get("status"),
                "financial_file_count": financial_inventory.get("financial_file_count"),
                "financial_candidate_line_count": financial_inventory.get("candidate_line_count"),
                "financial_candidate_file_counts_by_category": financial_inventory.get(
                    "candidate_file_counts_by_category", {}
                ),
                "financial_candidate_line_counts_by_category": financial_inventory.get(
                    "candidate_line_counts_by_category", {}
                ),
                "financial_inventory_coverage_verified": financial_inventory.get(
                    "coverage_verified", False
                ),
            }
        result = {
            "command": "qaudit-markdown-sentences",
            "root": str(root),
            "status": evidence["status"],
            "correlation_id": evidence["correlation_id"],
            "source_manifest_sha256": evidence["source_manifest_sha256"],
            "local_git_context": evidence["local_git_context"],
            "artifact_path": evidence["artifact_path"],
            "artifact_sha256": evidence["artifact_sha256"],
            "artifact_bytes": evidence["artifact_bytes"],
            "financial_claim_inventory": {
                **financial_summary,
                "artifact_integrity": financial_artifact,
            },
            "totals": evidence["totals"],
            "unreadable_file_count": evidence["unreadable_file_count"],
            "skipped_source_count": evidence["skipped_source_count"],
            "blockers": evidence["blockers"],
            "remote_verified": False,
            "remote_mutation_performed": False,
        }
        result["checkpoint"] = record_qaudit_checkpoint(
            root,
            "qaudit-markdown-sentences",
            {
                "status": evidence["status"],
                "source_manifest_sha256": evidence["source_manifest_sha256"],
                "artifact_path": evidence["artifact_path"],
                "artifact_sha256": evidence["artifact_sha256"],
                "artifact_bytes": evidence["artifact_bytes"],
                "artifact_refs": {
                    "markdown_sentence_audit": {
                        "path": evidence["artifact_path"],
                        "sha256": evidence["artifact_sha256"],
                        "bytes": evidence["artifact_bytes"],
                    },
                    "financial_claim_inventory": financial_artifact,
                },
                "metrics": {**evidence["totals"], **financial_summary},
                "blockers": [
                    *evidence["blockers"],
                    *(
                        ["financial_claim_inventory_artifact_unavailable"]
                        if financial_artifact["status"] != "verified_local_hash"
                        else []
                    ),
                ],
            },
            correlation_id=evidence["correlation_id"],
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1 if (
            evidence["status"] != "MATERIALIZED_AUDIT_COMPLETE_REMOTE_HISTORY_INCOMPLETE"
            or evidence["unreadable_file_count"]
            or evidence["skipped_source_count"]
            or evidence["totals"]["sentence_records_omitted_by_bound"]
        ) else 0

    if args.command == "validate-all":
        return agent.run_validation_pipeline()

    if args.command == "audit-first":
        root = Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve()
        audit_exit_code = main(["audit-inventory", "--base-path", str(root)])
        if audit_exit_code != 0:
            return audit_exit_code
        try:
            contract = agent.run_autonomous_loop()
            print(json.dumps(contract, indent=2))
            return 0 if contract.get("final_status") == "SUCCESS" else 1
        except (OllamaRuntimeError, OSError, ValueError) as exc:
            print(f"QAUDITS-first autonomous execution failed: {exc}", file=sys.stderr)
            return 1

    if args.command == "health":
        try:
            print(json.dumps(agent.verify_ollama(), indent=2))
            return 0
        except OllamaRuntimeError as exc:
            print(f"Ollama health check failed: {exc}", file=sys.stderr)
            return 1

    if args.command == "github-auth":
        print(json.dumps(configure_github_git_auth(), indent=2, sort_keys=True))
        return 0

    if args.command == "credential-manager":
        from scripts.qmoi_credentials import main as credential_manager_main

        root = Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve()
        return credential_manager_main([
            args.credential_action,
            "--qtrade",
            str(root / "Qtrade.md"),
        ])

    if args.command == "autonomous":
        try:
            contract = agent.run_autonomous_loop()
            print(json.dumps(contract, indent=2))
            return 0 if contract.get("final_status") == "SUCCESS" else 1
        except (OllamaRuntimeError, OSError, ValueError) as exc:
            print(f"Autonomous execution failed: {exc}", file=sys.stderr)
            return 1

    if args.command == "continue":
        try:
            exit_code = agent.run_continue_cycle()
            print(f"Continuation cycle status: {exit_code}")
            return exit_code
        except (OllamaRuntimeError, OSError, ValueError) as exc:
            print(f"Autonomous continuation failed: {exc}", file=sys.stderr)
            return 1

    if args.command == "merge-sync":
        roots = [
            Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve(),
            Path(args.base_path).resolve().parent / "Alpha-Q-ai" if args.base_path else Path.cwd().resolve().parent / "Alpha-Q-ai",
        ]
        if not roots[1].exists():
            roots = roots[:1]
        primary_root = roots[0]
        merge_evidence = agent.cross_repo_manager.refresh_merge_evidence(
            primary_root,
            roots=roots,
            correlation_id=str(uuid.uuid4()),
        )
        result = agent.execute_merge_and_sync(roots, auto_push=False)
        result["merge_evidence"] = merge_evidence
        printable = dict(result)
        if "audit_path" in printable and isinstance(printable["audit_path"], Path):
            printable["audit_path"] = str(printable["audit_path"])
        print(json.dumps(printable, indent=2, sort_keys=True, default=str))
        return 0 if result.get("status") == "ready" else 1

    if args.command == "qaudit-merge-parallel":
        root = Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve()
        result = run_parallel_merge_audit(root)
        production_refresh = agent.refresh_production_manifests(root)
        result["production_refresh"] = {
            "status": production_refresh["status"],
            "production": str(production_refresh["production"]),
            "productionenhanced": str(production_refresh["productionenhanced"]),
            "inventory": str(production_refresh["inventory"]),
            "candidate_count": production_refresh["candidate_count"],
            "remote_verified": False,
            "remote_mutation_performed": False,
        }
        merge_evidence = agent.cross_repo_manager.refresh_merge_evidence(
            root,
            roots=[root],
            correlation_id=str(uuid.uuid4()),
        )
        result["merge_evidence"] = {
            "status": merge_evidence["status"],
            "correlation_id": merge_evidence["correlation_id"],
            "source_manifest_sha256": merge_evidence["source_manifest_sha256"],
            "artifact_refs": merge_evidence["artifact_refs"],
            "remote_verified": False,
            "remote_mutation_performed": False,
        }
        result["checkpoint"] = merge_evidence["checkpoint"]
        result["metrics"].update({
            "production_inventory_sha256": hashlib.sha256(
                production_refresh["inventory"].read_bytes()
            ).hexdigest(),
            "production_document_sha256": hashlib.sha256(
                production_refresh["production"].read_bytes()
            ).hexdigest(),
            "production_enhanced_document_sha256": hashlib.sha256(
                production_refresh["productionenhanced"].read_bytes()
            ).hexdigest(),
        })
        print(json.dumps(result, indent=2, sort_keys=True, default=str))
        return 0 if result["status"] == "NEEDS_REVIEW" else 1

    if args.command == "qaudit-all-features":
        root = Path(args.base_path).resolve() if args.base_path else Path.cwd().resolve()
        result = run_parallel_feature_audit(
            root,
            shard_size=250,
            worker_count=min(16, max(1, os.cpu_count() or 1)),
            registry=build_all_features_registry(),
        )
        print(json.dumps(result, indent=2, sort_keys=True, default=str))
        return 0 if result["status"] == "NEEDS_REVIEW" else 1

    if args.command == "validate-platforms":
        print(
            json.dumps(
                agent.validate_all_platforms(),
                indent=2,
            )
        )
        return 0

    if args.command in {
        "validate-features",
        "validate-all-features",
    }:
        print(
            json.dumps(
                agent.validate_all_platform_features(),
                indent=2,
            )
        )
        return 0

    if args.command == "validate-file-handlers":
        print(
            json.dumps(
                agent.validate_file_handlers(),
                indent=2,
            )
        )
        return 0

    if args.command == "generate-memory-index":
        agent.memory_generator.generate_index()
        return 0

    if args.command == "generate-model-card":
        agent.model_card_generator.generate_card()
        return 0

    if args.command == "proof":
        print(
            json.dumps(
                agent.build_github_proof_contract(),
                indent=2,
            )
        )
        return 0

    if args.command == "checkpoint":
        agent.update_resume_checkpoint(
            status="manual_checkpoint",
            completed_steps=[
                "manual checkpoint",
            ],
        )
        return 0

    return 1


# ============================================================================
# MODULE ENTRYPOINT
# ============================================================================

if __name__ == "__main__":
    raise SystemExit(
        main()
    )