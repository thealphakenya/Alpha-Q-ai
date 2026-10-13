"""Build privacy-safe, evidence-bound tracking and monitoring inventories."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


TRACKING_TERMS = re.compile(
    r"monitor|metric|telemetry|health|observability|heartbeat|track|dashboard|"
    r"coverage|audit|status|state|activity|evidence|validation|manifest|inventory|"
    r"ledger|plan|workflow|test|ollama|qmo",
    re.IGNORECASE,
)
METRIC_ARTIFACT_SUFFIXES = {".json", ".jsonl", ".csv"}
MONITOR_SOURCE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".yml", ".yaml"}
MAX_SOURCE_HASH_BYTES = 1_000_000
EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
}
HISTORICAL_PARTS = {
    "qmoi-enhanced-history-14",
    "_archive_qmoi-enhanced",
    "archive",
    "archives",
    "legacy",
}
SNAPSHOT_PARTS = {"alpha-q-ai-2025"}
OUTPUT_PATHS = {
    "ALLTRACKS.md",
    "QMOITACKS.md",
    "QMOITRACKS.md",
    "ollamatracks/ALLTRACKS.md",
    "QMOItracks/QMOITRACKS.md",
    "ollamatracks/alltracks_monitoring_inventory.json",
    "QMOItracks/qmoitracks_monitoring_inventory.json",
}
TRACKING_SYSTEM_OUTPUTS = {
    "ollamatracks": (
        "ollamatracks/ALLTRACKS.md",
        "ollamatracks/alltracks_monitoring_inventory.json",
    ),
    "qmoitracks": (
        "QMOItracks/QMOITRACKS.md",
        "QMOItracks/qmoitracks_monitoring_inventory.json",
    ),
}
MONITORING_REQUIREMENT = (
    "Define owner, signal, unit, source, freshness, thresholds, alert/runbook, "
    "privacy scope, and positive/negative tests before treating monitoring as implemented."
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _scope(path: str) -> str:
    parts = {part.lower() for part in Path(path).parts}
    if parts & HISTORICAL_PARTS:
        return "historical_archive"
    if parts & SNAPSHOT_PARTS:
        return "snapshot"
    return "active_checkout"


def _git_value(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            check=False,
            text=True,
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 and result.stdout.strip() else None


def _candidate_paths(root: Path, supplied_paths: Sequence[str] | None) -> tuple[list[str], str]:
    if supplied_paths is not None:
        paths = list(supplied_paths)
        scope = "materialized_nonignored_local_checkout"
    else:
        try:
            result = subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "ls-files",
                    "--cached",
                    "--others",
                    "--exclude-standard",
                    "-z",
                ],
                capture_output=True,
                check=False,
            )
        except OSError:
            result = None
        if result is not None and result.returncode == 0:
            paths = [
                item.decode("utf-8", errors="replace")
                for item in result.stdout.split(b"\0")
                if item
            ]
            scope = "materialized_nonignored_local_checkout"
        else:
            paths = []
            for current, directories, filenames in os.walk(root, followlinks=False):
                current_path = Path(current)
                directories[:] = sorted(
                    name
                    for name in directories
                    if name not in EXCLUDED_PARTS
                    and not (current_path / name).is_symlink()
                )
                for name in filenames:
                    path = current_path / name
                    if path.is_symlink():
                        continue
                    paths.append(path.relative_to(root).as_posix())
            scope = "materialized_nonignored_local_checkout_fallback"

    normalized = sorted(
        {
            Path(path).as_posix()
            for path in paths
            if path
            and Path(path).as_posix() not in OUTPUT_PATHS
            and not (EXCLUDED_PARTS & set(Path(path).parts))
        }
    )
    return normalized, scope


def _is_metric_artifact(path: str) -> bool:
    candidate = Path(path)
    in_tracker = candidate.parts and candidate.parts[0].lower() in {
        "ollamatracks",
        "qmoitracks",
    }
    return (
        bool(in_tracker)
        and candidate.suffix.lower() in METRIC_ARTIFACT_SUFFIXES
        and bool(TRACKING_TERMS.search(candidate.name))
    )


def _is_tracking_artifact(path: str) -> bool:
    candidate = Path(path)
    return (
        candidate.parts
        and candidate.parts[0].lower() in {"ollamatracks", "qmoitracks"}
        and candidate.suffix.lower() in METRIC_ARTIFACT_SUFFIXES
    )


def _is_monitor_source(path: str) -> bool:
    candidate = Path(path)
    lower_parts = [part.lower() for part in candidate.parts]
    active_source_root = bool(
        lower_parts
        and lower_parts[0] in {"scripts", "src", "apps", "api", "functions", ".github"}
    )
    return (
        active_source_root
        and candidate.suffix.lower() in MONITOR_SOURCE_SUFFIXES
        and (
            bool(TRACKING_TERMS.search(candidate.name))
            or "ollama_autonomous_agent.py" == candidate.name.lower()
        )
    )


def _source_record(root: Path, path: str, roles: list[str]) -> dict[str, Any]:
    source = root / path
    try:
        if source.is_symlink() or not source.is_file():
            raise OSError("not_a_regular_file")
        before = source.stat()
        if before.st_size > MAX_SOURCE_HASH_BYTES:
            return {
                "path": path,
                "scope": _scope(path),
                "roles": roles,
                "bytes": before.st_size,
                "sha256": None,
                "status": "oversized_not_hashed",
                "max_hash_bytes": MAX_SOURCE_HASH_BYTES,
                "metric_values_read": False,
            }
        digest = hashlib.sha256()
        bytes_read = 0
        with source.open("rb") as stream:
            for chunk in iter(lambda: stream.read(64 * 1024), b""):
                bytes_read += len(chunk)
                if bytes_read > MAX_SOURCE_HASH_BYTES:
                    return {
                        "path": path,
                        "scope": _scope(path),
                        "roles": roles,
                        "bytes": before.st_size,
                        "sha256": None,
                        "status": "grew_beyond_hash_bound",
                        "max_hash_bytes": MAX_SOURCE_HASH_BYTES,
                        "metric_values_read": False,
                    }
                digest.update(chunk)
        after = source.stat()
        modified = datetime.fromtimestamp(after.st_mtime, timezone.utc).isoformat().replace(
            "+00:00", "Z"
        )
        return {
            "path": path,
            "scope": _scope(path),
            "roles": roles,
            "bytes": after.st_size,
            "sha256": digest.hexdigest(),
            "file_modified_at_utc": modified,
            "status": (
                "SCANNED"
                if (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns)
                else "changed_during_scan"
            ),
            "mtime_is_metric_freshness": False,
            "metric_values_read": False,
        }
    except OSError as exc:
        return {
            "path": path,
            "scope": _scope(path),
            "roles": roles,
            "status": f"unavailable:{type(exc).__name__}",
            "sha256": None,
            "metric_values_read": False,
        }


def _feature_id(platform: str, app: str, index: int, name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:96]
    return f"ui.{platform}.{app}.{index:03d}.{slug}"


def _percent(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return round((numerator / denominator) * 100, 2)


def build_tracking_inventory(
    root: Path | str,
    *,
    feature_registry: Mapping[str, Mapping[str, Sequence[str]]],
    master_ui_features: Sequence[str],
    access_modes: Mapping[str, Sequence[str]],
    source_paths: Sequence[str] | None = None,
    planned_feature_requirements: Mapping[str, Sequence[str]] | None = None,
    uis_plan: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Inventory monitoring references without reading metric values or claiming coverage."""
    source_root = Path(root).resolve()
    indexed_paths, source_scope = _candidate_paths(source_root, source_paths)

    monitor_paths = {
        path for path in indexed_paths if _is_monitor_source(path) and _scope(path) == "active_checkout"
    }
    metric_paths = {path for path in indexed_paths if _is_metric_artifact(path)}
    track_docs = {
        path
        for path in indexed_paths
        if Path(path).suffix.lower() == ".md"
        and "track" in Path(path).name.lower()
        and _scope(path) != "active_checkout"
    } | {
        path
        for path in indexed_paths
        if Path(path).suffix.lower() == ".md"
        and "track" in Path(path).name.lower()
        and _scope(path) == "active_checkout"
    }

    roles_by_path: dict[str, set[str]] = {}
    for path in monitor_paths:
        roles_by_path.setdefault(path, set()).add("monitoring_source_candidate")
    for path in metric_paths:
        roles_by_path.setdefault(path, set()).add("metric_artifact_reference")
    for path in indexed_paths:
        if _is_tracking_artifact(path):
            roles_by_path.setdefault(path, set()).add("tracking_artifact_reference")
    for path in track_docs:
        roles_by_path.setdefault(path, set()).add("tracking_document_reference")
    for path in indexed_paths:
        if Path(path).parts and Path(path).parts[0].lower() in {
            "ollamatracks",
            "qmoitracks",
        }:
            roles_by_path.setdefault(path, set()).add(
                "tracking_system_source_reference"
            )
    source_records = [
        _source_record(source_root, path, sorted(roles))
        for path, roles in sorted(roles_by_path.items())
    ]
    readable_sources = sum(item.get("status") == "SCANNED" for item in source_records)
    unavailable_sources = [
        item for item in source_records if item.get("status") != "SCANNED"
    ]

    feature_records: list[dict[str, Any]] = []
    for platform, applications in sorted(feature_registry.items()):
        for app, names in sorted(applications.items()):
            normalized_names = [names] if isinstance(names, str) else list(names)
            for index, name in enumerate(normalized_names, start=1):
                feature_records.append({
                    "feature_id": _feature_id(platform, app, index, str(name)),
                    "platform": platform,
                    "application": app,
                    "requirement": str(name),
                    "access_classification": "review_required",
                    "availability_status": "not_verified",
                    "style_universal_transition": "required_mapping_not_verified",
                    "monitoring_status": "unmapped",
                    "monitoring_source_paths": [],
                    "implementation_verified": False,
                })

    planned_records: list[dict[str, Any]] = []
    for category, requirements in sorted((planned_feature_requirements or {}).items()):
        names = [requirements] if isinstance(requirements, str) else requirements
        for index, requirement in enumerate(names, start=1):
            name = str(requirement)
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:72]
            access_classification = {
                "public_ui": "public_guest_contract",
                "authenticated_ui": "authenticated_user_contract",
                "mixed_access_ui": "mixed_access_contract",
                "master_ui": "master_operator_contract",
            }.get(category, "review_required")
            planned_records.append({
                "feature_id": f"planned.{category}.{index:03d}.{slug}",
                "source_category": category,
                "requirement": name,
                "access_classification": access_classification,
                "availability_status": "planned_or_unverified",
                "style_universal_transition": "required_mapping_not_verified",
                "monitoring_status": "unmapped",
                "monitoring_source_paths": [],
                "implementation_verified": False,
            })

    uis_records: list[dict[str, Any]] = []
    for section in (uis_plan or {}).get("sections", []):
        if not isinstance(section, Mapping):
            continue
        for requirement in section.get("requirements", []):
            if not isinstance(requirement, Mapping):
                continue
            requirement_id = str(requirement.get("id") or "unknown")
            description = str(requirement.get("description") or "")
            description_sha = hashlib.sha256(description.encode("utf-8")).hexdigest()
            uis_records.append({
                "feature_id": f"uis.{requirement_id.lower()}",
                "source_category": "universal_intelligence",
                "source_path": str((uis_plan or {}).get("source_path") or "QMOIUNIVERSALINTELLIGENCESYSTEM.md"),
                "source_line": requirement.get("source_line"),
                "source_sha256": (uis_plan or {}).get("source_sha256"),
                "requirement_sha256": description_sha,
                "access_classification": "review_required",
                "availability_status": "planned_or_unverified",
                "style_universal_transition": "required_mapping_not_verified",
                "monitoring_status": "unmapped",
                "monitoring_source_paths": [],
                "implementation_verified": False,
            })

    master_records = [
        {
            "feature_id": f"master.monitoring.{index:03d}",
            "requirement": str(name),
            "access_classification": "master_operator_contract",
            "availability_status": "not_verified",
            "backend_authorization_verified": False,
            "monitoring_status": "unmapped",
            "monitoring_source_paths": [],
            "implementation_verified": False,
        }
        for index, name in enumerate(master_ui_features, start=1)
    ]
    monitoring_requirements = [*feature_records, *master_records, *planned_records, *uis_records]
    all_requirements = len(monitoring_requirements)
    action_queue = [
        {
            "action_id": f"monitor-{hashlib.sha256(item['feature_id'].encode()).hexdigest()[:16]}",
            "feature_id": item["feature_id"],
            "scope": item.get("source_category", item.get("platform", "master_ui")),
            "status": "PENDING_REVIEW",
            "next_action": MONITORING_REQUIREMENT,
            "automatic_runtime_mutation_authorized": False,
        }
        for item in monitoring_requirements
    ]
    monitoring_source_count = sum(
        "monitoring_source_candidate" in item["roles"] for item in source_records
    )
    metric_reference_count = sum(
        "metric_artifact_reference" in item["roles"] for item in source_records
    )
    tracking_doc_count = sum(
        "tracking_document_reference" in item["roles"] for item in source_records
    )
    tracking_artifact_count = sum(
        "tracking_artifact_reference" in item["roles"] for item in source_records
    )
    tracking_artifacts_by_system = {
        system: {
            "source_file_reference_count": sum(
                item["path"].split("/", 1)[0].lower() == system
                and "tracking_system_source_reference" in item["roles"]
                for item in source_records
            ),
            "generated_output_reference_count": len(
                TRACKING_SYSTEM_OUTPUTS[system]
            ),
            "generated_inventory_output_count": sum(
                path.endswith("_monitoring_inventory.json")
                for path in TRACKING_SYSTEM_OUTPUTS[system]
            ),
            "file_reference_count": sum(
                item["path"].split("/", 1)[0].lower() == system
                and "tracking_system_source_reference" in item["roles"]
                for item in source_records
            ) + len(TRACKING_SYSTEM_OUTPUTS[system]),
            "artifact_reference_count": sum(
                item["path"].split("/", 1)[0].lower() == system
                and "tracking_artifact_reference" in item["roles"]
                for item in source_records
            ),
            "metric_artifact_reference_count": sum(
                item["path"].split("/", 1)[0].lower() == system
                and "metric_artifact_reference" in item["roles"]
                for item in source_records
            ),
            "monitor_source_candidate_count": sum(
                item["path"].split("/", 1)[0].lower() == system
                and "monitoring_source_candidate" in item["roles"]
                for item in source_records
            ),
        }
        for system in ("ollamatracks", "qmoitracks")
    }
    tracking_system_output_references = [
        {
            "path": path,
            "scope": "active_checkout",
            "status": "managed_output_path_excluded_from_source_hash",
            "content_read": False,
        }
        for paths in TRACKING_SYSTEM_OUTPUTS.values()
        for path in paths
    ]

    metric_definitions = {
        "feature_monitoring_mapping_rate_percent": {
            "unit": "percent",
            "numerator": "feature requirements with explicitly verified monitor-to-feature evidence",
            "denominator": "registered, master UI, planned, and Universal Intelligence requirements",
            "formula": "100 * numerator / denominator; null when denominator is zero",
            "interpretation": "implementation evidence coverage, not source-candidate discovery",
        },
        "source_hash_coverage_percent": {
            "unit": "percent",
            "numerator": "all discovered monitor, metric-artifact, tracking-document, and tracker-directory sources hashed successfully",
            "denominator": "unique source candidates discovered in the materialized local scope",
            "formula": "100 * numerator / denominator; null when denominator is zero",
            "interpretation": "local source integrity only; not freshness or runtime availability",
        },
    }
    hashed = hashlib.sha256(
        json.dumps(
            {
                "source_records": [
                    {key: item.get(key) for key in ("path", "scope", "roles", "bytes", "sha256")}
                    for item in source_records
                ],
                "feature_records": feature_records,
                "master_records": master_records,
                "planned_records": planned_records,
                "uis_records": uis_records,
                "action_queue": action_queue,
                "tracking_system_output_references": tracking_system_output_references,
                "access_mode_names": sorted(access_modes),
                "source_scope": source_scope,
                "policy_version": 1,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "schema_version": 1,
        "correlation_id": str(uuid.uuid4()),
        "generated_at": _utc_now(),
        "repository": source_root.name,
        "ref": _git_value(source_root, "symbolic-ref", "--short", "HEAD"),
        "local_head_sha": _git_value(source_root, "rev-parse", "HEAD"),
        "source_scope": source_scope,
        "status": "NEEDS_REVIEW",
        "source_manifest_sha256": hashed,
        "coverage_verified": False,
        "remote_verified": False,
        "live_metric_values_observed": False,
        "live_metric_provider_connections_verified": 0,
        "feature_requirements": feature_records,
        "master_ui_requirements": master_records,
        "planned_feature_requirements": planned_records,
        "universal_intelligence_requirements": uis_records,
        "monitoring_action_queue": action_queue,
        "universal_intelligence_plan_status": (uis_plan or {}).get("status", "not_available"),
        "access_mode_names": sorted(access_modes),
        "access_policy": {
            "public_guest": "public-only; do not expose user-specific or protected state",
            "authenticated_user": "verified user-owned scope only, enforced server-side",
            "master_operator": "all supported monitoring surfaces subject to verified role, least privilege, consent, and audit",
            "feature_access_assignments_verified": 0,
            "master_backend_authorization_verified": False,
            "source": "UNIVERSAL.md and MASTEROWNS.md",
        },
        "monitor_source_candidates": [
            item for item in source_records if "monitoring_source_candidate" in item["roles"]
        ],
        "metric_artifact_references": [
            item for item in source_records if "metric_artifact_reference" in item["roles"]
        ],
        "tracking_document_references": [
            item for item in source_records if "tracking_document_reference" in item["roles"]
        ],
        "tracking_artifact_references": [
            item for item in source_records if "tracking_artifact_reference" in item["roles"]
        ],
        "tracking_system_source_references": [
            item for item in source_records if "tracking_system_source_reference" in item["roles"]
        ],
        "tracking_system_output_references": tracking_system_output_references,
        "tracking_artifacts_by_system": tracking_artifacts_by_system,
        "metrics": {
            "indexed_materialized_path_count": len(indexed_paths),
            "feature_requirement_count": len(feature_records),
            "master_ui_requirement_count": len(master_records),
            "planned_feature_requirement_count": len(planned_records),
            "universal_intelligence_requirement_count": len(uis_records),
            "monitoring_requirement_count": all_requirements,
            "monitoring_source_candidate_count": monitoring_source_count,
            "metric_artifact_reference_count": metric_reference_count,
            "tracking_document_reference_count": tracking_doc_count,
            "tracking_artifact_reference_count": tracking_artifact_count,
            "tracking_system_file_reference_count": sum(
                "tracking_system_source_reference" in item["roles"]
                for item in source_records
            ) + len(tracking_system_output_references),
            "monitoring_mappings_verified_count": 0,
            "monitoring_unmapped_requirement_count": all_requirements,
            "monitoring_action_queue_count": len(action_queue),
            "feature_monitoring_mapping_rate_percent": _percent(0, all_requirements),
            "source_candidate_count": len(source_records),
            "source_candidates_hashed_count": readable_sources,
            "source_hash_coverage_percent": _percent(readable_sources, len(source_records)),
            "source_hash_failure_count": len(unavailable_sources),
            "live_metric_values_observed_count": 0,
            "live_metric_provider_connections_verified_count": 0,
            "formula_count": len(metric_definitions),
            "interpretation": "local_inventory_and_mapping_gaps_not_runtime_health_or_feature_completion",
        },
        "metric_definitions": metric_definitions,
        "plan": [
            {
                "stage": "inventory_and_contracts",
                "acceptance": "All current feature, monitoring, metric-artifact, and tracking candidates retain local scope and source hashes.",
                "status": "implemented_candidate_inventory",
            },
            {
                "stage": "planned_and_unavailable_features",
                "acceptance": "Every planned, unavailable, or newly registered feature receives a stable monitoring-review row and durable action before any implementation is claimed.",
                "status": "implemented_candidate_queue",
            },
            {
                "stage": "metric_schema_and_ownership",
                "acceptance": "Each approved signal has an owner, unit, source, scope, sampling/freshness rule, and data-minimization policy.",
                "status": "planned",
            },
            {
                "stage": "per_feature_monitor_mapping",
                "acceptance": "Every feature has reviewed applicability, signals, thresholds, alerts/runbook, and positive/negative tests or a justified not-applicable result.",
                "status": "planned",
            },
            {
                "stage": "style_universal_and_access_transitions",
                "acceptance": "Public, authenticated, and master surfaces share styles while data and actions remain role-scoped and server-authorized.",
                "status": "planned",
            },
            {
                "stage": "ollama_and_qmoi_runtime",
                "acceptance": "Authorized runtime health, queue age, checkpoint freshness, failures, and model/provider availability have freshness-bound evidence and recovery tests.",
                "status": "planned",
            },
            {
                "stage": "dashboard_and_alert_delivery",
                "acceptance": "Master controls expose all supported monitoring features; user views remain tenant-scoped; alerts are tested, auditable, and revocable.",
                "status": "planned",
            },
            {
                "stage": "remote_validation",
                "acceptance": "Target-owned terminal exact-SHA checks and independently verified remote artifacts are recorded before completion claims.",
                "status": "blocked_remote_evidence_required",
            },
        ],
        "unavailable_sources": unavailable_sources,
        "blockers": [
            "No live metric endpoint or runtime sample was read by this inventory.",
            "Per-feature monitoring signals and access assignments have not been independently mapped or verified.",
            "Static source timestamps are not evidence of metric freshness or service health.",
            "Materialized local paths do not establish ignored, historical-ref, peer-repository, or remote coverage.",
        ] + (
            ["Universal Intelligence source plan is unavailable or blocked."]
            if (uis_plan or {}).get("status") == "BLOCKED"
            else []
        ),
        "next_action": (
            "Review the machine-readable source and feature inventory, then map monitor applicability, "
            "owner, signal, freshness, access scope, thresholds, alerts, tests, and recovery before "
            "adding runtime instrumentation or dashboards."
        ),
    }


def render_tracking_markdown(inventory: Mapping[str, Any]) -> str:
    metrics = inventory["metrics"]
    lines = [
        "## Agent-managed tracking, monitoring, and live-metric coverage",
        "",
        "This report is a generated local inventory and implementation plan. Path discovery and source hashes do not prove that a monitor executes, that a metric is live/fresh, or that a feature is implemented.",
        "",
        f"- Status: `{inventory['status']}`; scope: `{inventory['source_scope']}`.",
        f"- Repository/ref/local HEAD: `{inventory['repository']}` / `{inventory.get('ref') or 'unavailable'}` / `{inventory.get('local_head_sha') or 'unavailable'}`.",
        f"- Correlation ID: `{inventory['correlation_id']}`; generated: `{inventory['generated_at']}`.",
        f"- Source-manifest SHA-256: `{inventory['source_manifest_sha256']}`.",
        f"- Complete path-level references and hashes: `ollamatracks/alltracks_monitoring_inventory.json`.",
        "",
        "### Calculated QAUDITS metrics",
        "",
        "| Metric | Value | Formula / interpretation |",
        "| --- | ---: | --- |",
        f"| Indexed materialized paths | {metrics['indexed_materialized_path_count']} | Enumerated local non-ignored scope only |",
        f"| Registered feature requirements | {metrics['feature_requirement_count']} | Registry denominator; not implementation count |",
        f"| Master UI requirements | {metrics['master_ui_requirement_count']} | Master dashboard/control requirements |",
        f"| Planned/unverified requirements | {metrics['planned_feature_requirement_count']} | Future or not-yet-verified product requirements |",
        f"| UIS requirements | {metrics['universal_intelligence_requirement_count']} | Requirements referenced by ID/line/hash, without copying source prose |",
        f"| Monitoring requirements | {metrics['monitoring_requirement_count']} | Registered, master UI, planned, and UIS requirements |",
        f"| Monitoring source candidates | {metrics['monitoring_source_candidate_count']} | Path candidates; execution not verified |",
        f"| Metric artifact references | {metrics['metric_artifact_reference_count']} | Hashed file references; values were not read |",
        f"| Tracking document references | {metrics['tracking_document_reference_count']} | Local Markdown path candidates |",
        f"| Tracking artifacts referenced | {metrics['tracking_artifact_reference_count']} | Local JSON/JSONL/CSV files under tracker roots; metric values are never read and hashing is bounded |",
        f"| Tracker-directory file path references | {metrics['tracking_system_file_reference_count']} | Materialized non-ignored input files plus managed output paths; self-referential output contents are excluded |",
        f"| Ollama tracker file paths / metric artifacts | {inventory['tracking_artifacts_by_system']['ollamatracks']['file_reference_count']} / {inventory['tracking_artifacts_by_system']['ollamatracks']['metric_artifact_reference_count']} | Input path/metadata inventory; input hashes are bounded to {MAX_SOURCE_HASH_BYTES} bytes; metric values are not read |",
        f"| QMOI tracker file paths / metric artifacts | {inventory['tracking_artifacts_by_system']['qmoitracks']['file_reference_count']} / {inventory['tracking_artifacts_by_system']['qmoitracks']['metric_artifact_reference_count']} | Input path/metadata inventory; input hashes are bounded to {MAX_SOURCE_HASH_BYTES} bytes; metric values are not read |",
        f"| Verified per-requirement monitor mappings | {metrics['monitoring_mappings_verified_count']} | Evidence-linked feature mappings only |",
        f"| Pending monitoring review actions | {metrics['monitoring_action_queue_count']} | One durable review action per requirement; no runtime mutation authorized |",
        f"| Monitor-mapping rate | {metrics['feature_monitoring_mapping_rate_percent']}% | Verified mappings / all requirements; zero currently verified |",
        f"| Source hash coverage | {metrics['source_hash_coverage_percent']}% | Hashed candidates / discovered source candidates; local integrity only |",
        f"| Unhashed, unavailable, or changed sources | {metrics['source_hash_failure_count']} | Check `unavailable_sources` for per-path reasons, including the 1 MB hashing bound |",
        f"| Live metric samples observed | {metrics['live_metric_values_observed_count']} | No runtime endpoint was read |",
        f"| Verified live provider connections | {metrics['live_metric_provider_connections_verified_count']} | No provider connection was made |",
        "",
        "The machine inventory defines each calculation, numerator, denominator, unit, and interpretation. A percentage never means global, remote, semantic, or production coverage.",
        "",
        "### Access, styles, and universals contract",
        "",
        "- `public_guest`: public-only views; no user-specific or protected state.",
        "- `authenticated_user`: only verified user-owned scope, enforced by server-side authorization.",
        "- `master_operator`: all supported monitoring surfaces only after role verification, with least privilege, consent, and audit controls.",
        "- Product-feature access classifications remain `review_required`; this report does not infer role access from feature names.",
        "- Apply [STYLES.md](STYLES.md), [UNIVERSAL.md](UNIVERSAL.md), and [UNIVERSALS.md](UNIVERSALS.md) consistently during UI transitions without sharing private data across users.",
        "- Master monitoring UI requirements are individually listed in the machine inventory; backend authorization and actual UI implementation remain unverified.",
        "",
        "### Registered product features and monitoring assessment",
        "",
        "| Feature ID | Platform | App | Access classification | Monitoring | Shared style/universal transition |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| `{item['feature_id']}` | `{item['platform']}` | `{item['application']}` | `{item['access_classification']}` | `{item['monitoring_status']}` | `{item['style_universal_transition']}` |"
        for item in inventory["feature_requirements"]
    )
    lines.extend([
        "",
        "### Planned and not-yet-verified feature requirements",
        "",
        "| Feature ID | Source category | Access classification | Availability | Monitoring |",
        "| --- | --- | --- | --- | --- |",
    ])
    lines.extend(
        f"| `{item['feature_id']}` | `{item['source_category']}` | `{item['access_classification']}` | `{item['availability_status']}` | `{item['monitoring_status']}` |"
        for item in inventory["planned_feature_requirements"]
    )
    lines.extend(
        f"| `{item['feature_id']}` | `{item['source_category']}` | `{item['access_classification']}` | `{item['availability_status']}` | `{item['monitoring_status']}` |"
        for item in inventory["universal_intelligence_requirements"]
    )
    lines.extend([
        "",
        "### Master monitoring and control requirements",
        "",
        "| Feature ID | Requirement | Access | Monitoring status |",
        "| --- | --- | --- | --- |",
    ])
    lines.extend(
        f"| `{item['feature_id']}` | {item['requirement']} | `{item['access_classification']}` | `{item['monitoring_status']}` |"
        for item in inventory["master_ui_requirements"]
    )
    lines.extend([
        "",
        "### Ollama and QMOI runtime monitoring targets",
        "",
        "- Track model/provider availability and inference failures, duration, timeouts, and bounded retries without logging prompts or credentials.",
        "- Track agent cycle status, task queue depth/age, checkpoint freshness, source-manifest deltas, skipped/unreadable inputs, test outcomes, and recovery results.",
        "- Track QMOI feature-service health and data freshness separately from discovery counts; missing or stale telemetry must report `UNKNOWN`, `STALE`, or `OFFLINE`, never healthy by default.",
        "- Record source, observation time, units, thresholds, owner, and evidence hash for every runtime sample; keep personal data tenant-scoped and collect only approved aggregates.",
        "",
        "### Bounded implementation plan",
        "",
    ])
    lines.extend(
        f"{index}. **{stage['stage']}** — {stage['acceptance']} Status: `{stage['status']}`."
        for index, stage in enumerate(inventory["plan"], start=1)
    )
    lines.extend([
        "",
        "### Current blockers and next action",
        "",
        *[f"- {blocker}" for blocker in inventory["blockers"]],
        f"- Next action: {inventory['next_action']}",
        "- Do not automatically instrument a feature until ownership, applicability, authorized data scope, privacy/security impact, thresholds, test plan, rollback, and required human approval are explicit.",
        "- No production UI, telemetry endpoint, external monitor, or remote workflow was added or activated by this inventory.",
    ])
    return "\n".join(lines)


def render_qmoi_tracks_markdown(inventory: Mapping[str, Any]) -> str:
    metrics = inventory["metrics"]
    lines = [
        "## Agent-managed QMOI feature and monitoring tracker",
        "",
        "This generated QMOI tracker includes currently registered and planned/unverified feature requirements. It creates review work automatically; it does not claim feature availability or silently install runtime telemetry.",
        "",
        f"- Status: `{inventory['status']}`; correlation: `{inventory['correlation_id']}`.",
        f"- Source manifest: `{inventory['source_manifest_sha256']}`; local source SHA: `{inventory.get('local_head_sha') or 'unavailable'}`.",
        f"- Registered features: `{metrics['feature_requirement_count']}`; planned/UIS requirements: `{metrics['planned_feature_requirement_count'] + metrics['universal_intelligence_requirement_count']}`.",
        f"- Local Ollama tracker file paths: `{inventory['tracking_artifacts_by_system']['ollamatracks']['file_reference_count']}`; QMOI tracker file paths: `{inventory['tracking_artifacts_by_system']['qmoitracks']['file_reference_count']}`. Managed output paths are path-listed but excluded from self-hashing.",
        f"- All requirements with a generated monitoring-review action: `{metrics['monitoring_action_queue_count']}/{metrics['monitoring_requirement_count']}`.",
        f"- Verified monitor mappings: `{metrics['monitoring_mappings_verified_count']}/{metrics['monitoring_requirement_count']}`; coverage verified: `{inventory['coverage_verified']}`.",
        "",
        "### QMOI product/platform features",
        "",
        "| Feature ID | Platform | App | Availability | Access review | Monitoring |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(
        f"| `{item['feature_id']}` | `{item['platform']}` | `{item['application']}` | `{item['availability_status']}` | `{item['access_classification']}` | `{item['monitoring_status']}` |"
        for item in inventory["feature_requirements"]
    )
    lines.extend([
        "",
        "### Planned and Universal Intelligence requirements",
        "",
        "| Requirement ID | Source reference | Access review | Availability | Monitoring |",
        "| --- | --- | --- | --- | --- |",
    ])
    lines.extend(
        f"| `{item['feature_id']}` | `{item.get('source_path', item.get('source_category'))}`"
        f"{':' + str(item['source_line']) if item.get('source_line') else ''} | "
        f"`{item['access_classification']}` | `{item['availability_status']}` | `{item['monitoring_status']}` |"
        for item in [*inventory["planned_feature_requirements"], *inventory["universal_intelligence_requirements"]]
    )
    lines.extend([
        "",
        "### Master monitoring access",
        "",
        "- Expose every supported monitoring control to a server-verified master role only; backend authorization, consent, audit, and required approval remain authoritative.",
        "- Keep authenticated users limited to their own authorized data, and public surfaces limited to approved non-personal status. Do not infer access from a name or UI presence.",
        "- Use [STYLES.md](STYLES.md), [UNIVERSAL.md](UNIVERSAL.md), and [UNIVERSALS.md](UNIVERSALS.md) for consistent styling and public/authenticated/master transitions.",
        "",
        "| Master requirement ID | Requirement | Authorization | Monitoring |",
        "| --- | --- | --- | --- |",
    ])
    lines.extend(
        f"| `{item['feature_id']}` | {item['requirement']} | `{item['access_classification']}` "
        f"(backend verification: `{item['backend_authorization_verified']}`) | `{item['monitoring_status']}` |"
        for item in inventory["master_ui_requirements"]
    )
    lines.extend([
        "",
        "- Each feature is automatically queued for owner, signals, units, source/freshness, alert/runbook, privacy review, tests, and recovery mapping. Production instrumentation still requires reviewed code and authorization.",
        "",
        "### Ollama and QMOI monitoring work",
        "",
        "- Track model/provider availability, failures, durations, timeouts, bounded retries, task queue age, checkpoints, source-manifest deltas, skipped inputs, and recovery outcomes.",
        "- Mark missing/stale samples `UNKNOWN`, `STALE`, or `OFFLINE`; include source timestamp, unit, scope, and evidence hash before reporting live health.",
        "- Full metric artifact references and generated review actions are in `ollamatracks/alltracks_monitoring_inventory.json`; raw metric values and user content are not copied into this tracker.",
        "- This tracker is updated by the Ollama QAUDITS coverage refresh. No remote completion or runtime-health claim is implied.",
    ])
    return "\n".join(lines)


__all__ = [
    "build_tracking_inventory",
    "render_qmoi_tracks_markdown",
    "render_tracking_markdown",
]
