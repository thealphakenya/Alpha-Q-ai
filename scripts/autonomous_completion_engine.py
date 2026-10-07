#!/usr/bin/env python3
"""Deterministic, fail-closed completion gate for the QMOI/Ollama lifecycle.

The LLM agent may propose work, but this module alone evaluates whether the
required production evidence exists. Unknown gates never become successful.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

try:
    from .checkpoint_manager import CheckpointManager
    from .live_activity_events import LiveActivity
    from .q_version_manager import QVersionManager
except ImportError:  # pragma: no cover - direct script execution
    from checkpoint_manager import CheckpointManager
    from live_activity_events import LiveActivity
    from q_version_manager import QVersionManager

REQUIRED_GATES = (
    "discovery",
    "inspection",
    "repository_surface_audit",
    "ollama_reference_audit",
    "ui_test_hook_coverage",
    "qmoi_restore_point",
    "instruction_inventory",
    "production_readiness",
    "markdown_inventory",
    "validation",
    "security",
    "remote_main",
    "remote_backup",
    "q_version",
    "live_activity",
    "cross_repository",
    "final_verification",
)
TERMINAL_STATUSES = {
    "SUCCESS",
    "NO_CHANGES_REQUIRED",
    "BLOCKED_REQUIRES_HUMAN",
}
GATE_ACTIONS = {
    "discovery": ("Refresh refs, source roots, and repository identity", "READ_ONLY_AUTOMATIC", False),
    "inspection": ("Map requirements to source, tests, workflows, and documentation", "READ_ONLY_AUTOMATIC", False),
    "repository_surface_audit": ("Verify file, Markdown, API, route, link, component, tree, metrics, and percentage coverage at exact SHAs", "TARGET_WORKFLOW_REQUIRED", True),
    "ollama_reference_audit": ("Inventory Ollama responsibilities across materialized and remote histories", "TARGET_WORKFLOW_REQUIRED", True),
    "ui_test_hook_coverage": ("Map every styles/universals feature to tests and reviewed hook/webhook applicability", "TARGET_WORKFLOW_REQUIRED", True),
    "qmoi_restore_point": ("Verify the qmoi restore branch matches both repositories' main and autosync-backup SHAs", "TARGET_WORKFLOW_REQUIRED", True),
    "instruction_inventory": ("Read and hash all applicable repository instructions without rewriting policy", "READ_ONLY_AUTOMATIC", False),
    "production_readiness": ("Map production candidates to owners, requirements, focused tests, and safe replacement plans", "LOCAL_ANALYSIS_AND_FOCUSED_TESTS", False),
    "markdown_inventory": ("Run complete target-owned Markdown/ref/PR inventory", "TARGET_WORKFLOW_REQUIRED", True),
    "validation": ("Run focused local checks, then configured target-owned validation", "LOCAL_THEN_TARGET_WORKFLOW", False),
    "security": ("Run available read-only security checks and record inaccessible findings", "READ_ONLY_AUTOMATIC", False),
    "remote_main": ("Verify exact main SHA and use only an authorized normal publication path", "REMOTE_AUTHORIZATION_REQUIRED", True),
    "remote_backup": ("Verify backup SHA and guarded fast-forward eligibility", "REMOTE_AUTHORIZATION_REQUIRED", True),
    "q_version": ("Finalize a sequential Q version only after every required gate passes", "CONDITIONAL_FINALIZATION", True),
    "live_activity": ("Publish sanitized lifecycle status and verify the exact-SHA event", "LOCAL_OR_TARGET_WORKFLOW", False),
    "cross_repository": ("Verify both source objects and run guarded target-owned sync", "TARGET_WORKFLOW_REQUIRED", True),
    "final_verification": ("Re-read terminal checks, refs, ledgers, and clean exact-SHA evidence", "READ_ONLY_AUTOMATIC", False),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _json_write(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(dict(payload), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()


def repository_state(root: Path) -> dict[str, Any]:
    """Return local state, keeping unavailable Git data explicit."""
    return {
        "path": str(root),
        "branch": _git(root, "branch", "--show-current"),
        "sha": _git(root, "rev-parse", "HEAD"),
        "status": _git(root, "status", "--short"),
        "remote_main": _git(root, "rev-parse", "refs/remotes/origin/main"),
        "remote_backup": _git(root, "rev-parse", "refs/remotes/origin/autosync-backup"),
    }


def audit_instruction_files(root: Path | str) -> dict[str, Any]:
    """Read every active instruction file and emit scope/hash metadata, never source contents."""
    target = Path(root).resolve()
    candidates: set[Path] = set()
    errors = []
    for relative in ("AGENTS.md", ".github/copilot-instructions.md"):
        path = target / relative
        if path.is_symlink():
            errors.append({"path": relative, "error_type": "SymlinkInstruction"})
        elif path.is_file():
            candidates.add(path)
        else:
            errors.append({"path": relative, "error_type": "MissingRequiredInstruction"})
    instruction_root = target / ".github" / "instructions"
    if instruction_root.is_symlink():
        errors.append({"path": ".github/instructions", "error_type": "SymlinkInstructionDirectory"})
    elif instruction_root.is_dir():
        for path in instruction_root.rglob("*"):
            if path.is_symlink():
                errors.append({"path": path.relative_to(target).as_posix(), "error_type": "SymlinkInstruction"})
            elif path.is_file():
                candidates.add(path)
    else:
        errors.append({"path": ".github/instructions", "error_type": "MissingInstructionDirectory"})

    inventory = []
    for path in sorted(candidates, key=lambda item: item.relative_to(target).as_posix()):
        relative_path = path.relative_to(target).as_posix()
        try:
            content = path.read_bytes()
            text = content.decode("utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append({"path": relative_path, "error_type": type(exc).__name__})
            continue
        stripped = text.lstrip()
        frontmatter = None
        if stripped.startswith("---"):
            parts = stripped.split("---", 2)
            if len(parts) != 3:
                errors.append({"path": relative_path, "error_type": "MalformedFrontmatter"})
                continue
            match = re.search(r"(?m)^applyTo:\s*(.*?)\s*$", parts[1])
            frontmatter = match.group(1).strip("\"'") if match else "repository-wide"
        else:
            frontmatter = "repository-wide"
        if not text.strip():
            errors.append({"path": relative_path, "error_type": "EmptyInstruction"})
            continue
        inventory.append({
            "path": relative_path,
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "apply_to": frontmatter,
            "nonempty": True,
        })
    return {
        "status": "PASS" if inventory and not errors else "FAIL",
        "files_discovered": len(candidates),
        "files_read": len(inventory),
        "unreadable_or_invalid": errors,
        "files": inventory,
        "source_contents_recorded": False,
    }


def audit_ollama_reference_files(root: Path | str) -> dict[str, Any]:
    """Inventory Ollama mentions without copying source lines into evidence."""
    target = Path(root).resolve()
    excluded_directory_names = {
        ".git", "node_modules", ".venv", "venv", "__pycache__",
        ".pytest_cache", "dist", "build", "coverage",
    }
    max_file_bytes = 100_000_000
    skipped: list[dict[str, str]] = []
    excluded_directories: dict[str, int] = {}
    matched_files: list[dict[str, Any]] = []
    qvillage_qvs_files: list[dict[str, Any]] = []
    category_counts: dict[str, int] = {}
    scope_counts: dict[str, int] = {}
    self_excluded_files = 0
    scanned_files = 0
    scanned_bytes = 0
    tree_digest = hashlib.sha256()

    category_patterns = {
        "runtime_and_models": re.compile(r"runtime|model|inference|server", re.IGNORECASE),
        "workflows_and_remote_git": re.compile(r"workflow|github|remote|sync|push|pull request|branch", re.IGNORECASE),
        "history_and_merges": re.compile(r"history|archive|backup|merge|reconcile", re.IGNORECASE),
        "validation_and_security": re.compile(r"test|validation|lint|security|production|feature", re.IGNORECASE),
        "memory_and_research": re.compile(r"memory|research|awareness|dataset|qvillage", re.IGNORECASE),
        "q_version_lifecycle": re.compile(r"q\.0\.0|q_version|q-version|finaliz|reservation", re.IGNORECASE),
        "activity_and_evidence": re.compile(r"activity|telemetry|heartbeat|checkpoint|evidence|completion", re.IGNORECASE),
        "styles_hooks_and_universals": re.compile(r"styles|universal|hook|webhook|accessibility|ui feature", re.IGNORECASE),
        "financial_surfaces": re.compile(r"bank|wallet|payment|trading|finance|account", re.IGNORECASE),
    }

    if not target.is_dir():
        return {
            "schema_version": 1,
            "status": "BLOCKED",
            "coverage_complete": False,
            "root": str(target),
            "reason": "repository root is missing",
            "source_contents_recorded": False,
        }

    for current, directory_names, filenames in os.walk(target, topdown=True, followlinks=False):
        current_path = Path(current)
        retained_directories = []
        for name in directory_names:
            directory = current_path / name
            relative = directory.relative_to(target).as_posix()
            if name in excluded_directory_names or name.startswith((".venv", "venv")):
                excluded_directories[relative] = excluded_directories.get(relative, 0) + 1
            elif directory.is_symlink():
                skipped.append({"path": relative, "reason": "symlink_directory_not_followed"})
            else:
                retained_directories.append(name)
        directory_names[:] = retained_directories

        for filename in filenames:
            path = current_path / filename
            relative = path.relative_to(target).as_posix()
            if relative == "ollamatracks/ollama_reference_audit.json":
                self_excluded_files += 1
                continue
            if path.is_symlink():
                skipped.append({"path": relative, "reason": "symlink_file_not_followed"})
                continue
            try:
                size = path.stat().st_size
                if size > max_file_bytes:
                    skipped.append({"path": relative, "reason": "oversized_file_not_read"})
                    continue
                content = path.read_bytes()
            except OSError as exc:
                skipped.append({"path": relative, "reason": type(exc).__name__})
                continue

            content_sha256 = hashlib.sha256(content).hexdigest()
            tree_digest.update(relative.encode("utf-8", errors="replace"))
            tree_digest.update(b"\0")
            tree_digest.update(content_sha256.encode("ascii"))
            tree_digest.update(b"\n")
            scanned_files += 1
            scanned_bytes += size

            path_parts_lower = {part.lower() for part in Path(relative).parts}
            lowered_relative = relative.lower()
            decoded_content = content.decode("utf-8", errors="replace")
            qvillage_mentions = len(re.findall(r"\bqvillage\b", decoded_content, re.IGNORECASE))
            qvs_mentions = len(re.findall(r"\bqvs\b", decoded_content, re.IGNORECASE))
            qve_mentions = len(re.findall(r"\bqve\b", decoded_content, re.IGNORECASE))
            if (
                "qvillage" in lowered_relative
                or "qvs" in path_parts_lower
                or "qve" in path_parts_lower
                or "qvs" in Path(relative).stem.lower()
                or qvillage_mentions
                or qvs_mentions
                or qve_mentions
            ):
                if "qmoi-enhanced-history-14" in path_parts_lower or "_archive_qmoi-enhanced" in path_parts_lower:
                    source_scope = "qmoi_enhanced_history"
                elif "alpha-q-ai-2025" in path_parts_lower:
                    source_scope = "alpha_source_snapshot"
                else:
                    source_scope = "active_repository"
                qvillage_qvs_files.append({
                    "path": relative,
                    "scope": source_scope,
                    "bytes": size,
                    "sha256": content_sha256,
                    "kind": "markdown" if path.suffix.lower() == ".md" else "source_or_data",
                    "qvillage_mention_count": qvillage_mentions,
                    "qvs_mention_count": qvs_mentions,
                    "qve_mention_count": qve_mentions,
                })

            path_match = "ollama" in relative.lower()
            lines = content.decode("utf-8", errors="replace").splitlines()
            matching_line_numbers = [
                index for index, line in enumerate(lines, 1)
                if "ollama" in line.lower()
            ]
            if not path_match and not matching_line_numbers:
                continue

            scope = "active_repository"
            path_parts = Path(relative).parts
            if "qmoi-enhanced-history-14" in path_parts or "_archive_qmoi-enhanced" in path_parts:
                scope = "qmoi_enhanced_history"
            elif "Alpha-Q-ai-2025" in path_parts:
                scope = "alpha_source_snapshot"
            matched_lines = [lines[index - 1] for index in matching_line_numbers]
            searchable_text = relative + "\n" + "\n".join(matched_lines)
            categories = sorted(
                name for name, pattern in category_patterns.items()
                if pattern.search(searchable_text)
            ) or ["other"]
            record = {
                "path": relative,
                "scope": scope,
                "bytes": size,
                "sha256": content_sha256,
                "path_match": path_match,
                "matching_line_count": len(matching_line_numbers),
                "mention_count": sum(line.lower().count("ollama") for line in matched_lines),
                "matching_line_numbers": matching_line_numbers[:100],
                "line_numbers_truncated": len(matching_line_numbers) > 100,
                "categories": categories,
            }
            matched_files.append(record)
            scope_counts[scope] = scope_counts.get(scope, 0) + 1
            for category in categories:
                category_counts[category] = category_counts.get(category, 0) + 1

    local_complete = not skipped
    try:
        refs = subprocess.run(
            ["git", "-C", str(target), "for-each-ref", "--format=%(refname)"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        commit_count = int(subprocess.run(
            ["git", "-C", str(target), "rev-list", "--all", "--count"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip())
        git_history_status = "enumerated_local_refs_and_commit_count"
    except (OSError, subprocess.CalledProcessError, ValueError):
        refs = []
        commit_count = None
        git_history_status = "unavailable"

    history_diff_paths: dict[str, set[str]] = {}
    history_diff_status = "unavailable"
    history_diff_commit_count = 0
    try:
        history_diff = subprocess.run(
            [
                "git", "-C", str(target), "-c", "core.quotePath=false", "log",
                "--all", "--regexp-ignore-case", "-Gollama", "--format=%H", "--name-only",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        current_commit = None
        commit_ids: set[str] = set()
        for line in history_diff.stdout.splitlines():
            if re.fullmatch(r"[0-9a-f]{40}", line):
                current_commit = line
                commit_ids.add(line)
            elif line.strip() and current_commit:
                history_diff_paths.setdefault(line.strip(), set()).add(current_commit)
        history_diff_commit_count = len(commit_ids)
        history_diff_status = "all_local_ref_diffs_scanned"
    except (OSError, subprocess.CalledProcessError):
        pass

    historical_paths = [
        {
            "path": path,
            "matching_change_commit_count": len(commit_ids),
            "matching_change_commits": sorted(commit_ids),
        }
        for path, commit_ids in sorted(history_diff_paths.items())
    ]
    manifest = json.dumps(
        {"materialized_matches": matched_files, "local_history_diffs": historical_paths},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema_version": 1,
        "status": "NEEDS_REMOTE_HISTORY_EVIDENCE" if local_complete else "INCOMPLETE_LOCAL_SCAN",
        "generated_at": utc_now(),
        "repository": target.name,
        "head_sha": _git(target, "rev-parse", "HEAD"),
        "scope": "all materialized files excluding explicitly listed dependency, build, cache, and Git roots",
        "local_scan": {
            "status": "PASS" if local_complete else "INCOMPLETE",
            "complete": local_complete,
            "files_scanned": scanned_files,
            "bytes_scanned": scanned_bytes,
            "matched_file_count": len(matched_files),
            "matched_files_by_scope": dict(sorted(scope_counts.items())),
            "matched_files_by_category": dict(sorted(category_counts.items())),
            "tree_sha256": tree_digest.hexdigest(),
            "excluded_directories": dict(sorted(excluded_directories.items())),
            "self_referential_files_excluded": self_excluded_files,
            "skipped_sources": skipped,
            "source_contents_recorded": False,
        },
        "matched_files": sorted(matched_files, key=lambda item: item["path"]),
        "qvillage_qvs_inventory": {
            "status": "MATERIALIZED_PATHS_ONLY",
            "coverage_complete": False,
            "file_count": len(qvillage_qvs_files),
            "markdown_file_count": sum(item["kind"] == "markdown" for item in qvillage_qvs_files),
            "files": sorted(qvillage_qvs_files, key=lambda item: item["path"]),
            "source_contents_recorded": False,
            "remote_refs_prs_and_intermediate_trees_verified": False,
        },
        "source_manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "local_git_history": {
            "status": git_history_status,
            "ref_count": len(refs),
            "refs": sorted(refs),
            "commit_count": commit_count,
            "ollama_mention_diff_status": history_diff_status,
            "ollama_mention_diff_commit_count": history_diff_commit_count,
            "ollama_mention_diff_path_count": len(historical_paths),
            "ollama_mention_diff_paths": historical_paths,
            "intermediate_commit_trees_scanned": False,
        },
        "remote_history": {
            "verified": False,
            "all_refs_enumerated": False,
            "all_pull_requests_included": False,
            "all_intermediate_commit_trees_scanned": False,
        },
        "coverage_complete": False,
        "unavailable_sources": [item["path"] for item in skipped],
        "next_action": "Run an authorized target-owned audit for both repositories covering all refs, PRs, and intermediate commit trees; attach terminal exact-SHA evidence before Q-version finalization.",
    }


def discover_q_version(root: Path) -> str | None:
    return QVersionManager(root).latest_artifact()


def topic_metrics(root: Path) -> dict[str, Any]:
    """Compute plan/index parity and evidence-backed topic counts."""
    plan = root / "QMOI_Ollama_Autonomous_Production_Completion_Master_Plan.md"
    index = root / "ollama_master_topic_index.txt"
    heading_pattern = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")
    topics = {
        int(match.group(1)): match.group(2)
        for line in plan.read_text(encoding="utf-8").splitlines()
        if plan.is_file() and (match := heading_pattern.match(line))
    } if plan.is_file() else {}
    indexed = [
        int(match.group(1))
        for line in index.read_text(encoding="utf-8").splitlines()
        if index.is_file() and (match := re.match(r"^(\d+)\.\s+", line))
    ] if index.is_file() else []
    records: dict[int, dict[str, Any]] = {}
    evidence = root / "Q.0.0.N" / "evidence" / "topics"
    for path in sorted(evidence.glob("topic-*.json")) if evidence.is_dir() else ():
        match = re.match(r"topic-(\d+)\.json$", path.name)
        if not match:
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        number = int(match.group(1))
        if number in topics and isinstance(record, dict):
            records[number] = record
    complete = sum(
        str(item.get("status", "")).upper() in {"SUCCESS", "FULLY_COMPLETED"}
        and bool(item.get("evidence_complete"))
        for item in records.values()
    )
    blocked = sum(str(item.get("status", "")).upper() in {"BLOCKED", "FAILED"} for item in records.values())
    not_started = sum(str(item.get("status", "")).upper() == "NOT_STARTED" for item in records.values())
    active = max(len(topics) - complete - blocked - not_started, 0)
    return {
        "generated": utc_now(),
        "master_plan_topics": len(topics),
        "topic_index_entries": len(indexed),
        "topic_index_matches_plan": sorted(topics) == indexed,
        "missing_index_numbers": sorted(set(topics) - set(indexed)),
        "duplicate_index_numbers": sorted(number for number in set(indexed) if indexed.count(number) > 1),
        "evidence_records": len(records),
        "fully_completed": complete,
        "blocked": blocked,
        "not_started": not_started,
        "in_progress": active,
        "status_sum_matches_inventory": complete + blocked + not_started + active == len(topics),
    }


@dataclass
class CompletionResult:
    execution_id: str
    status: str
    stage: str
    gates: dict[str, str]
    errors: list[str] = field(default_factory=list)
    repository_results: dict[str, Any] = field(default_factory=dict)
    evidence: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)

    def as_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "status": self.status,
            "stage": self.stage,
            "gates": self.gates,
            "errors": self.errors,
            "repository_results": self.repository_results,
            "evidence": self.evidence,
            "created_at": self.created_at,
        }


class AutonomousCompletionEngine:
    """Own the final verdict; all required evidence must be explicit."""

    def __init__(self, root: Path | str, execution_id: str | None = None) -> None:
        self.root = Path(root).resolve()
        self.execution_id = execution_id or f"exec-{uuid.uuid4().hex}"
        self.checkpoints = CheckpointManager(self.root)
        self.activity = LiveActivity(self.root, self.execution_id)

    def evaluate(
        self,
        gates: Mapping[str, str | bool | None] | None = None,
        *,
        repository_results: Mapping[str, Any] | None = None,
        errors: list[str] | None = None,
    ) -> CompletionResult:
        self.activity.publish("AGENT_STARTED", "RUNNING", "DISCOVERY", "Completion evaluation started")
        self.checkpoints.write(self.execution_id, {
            "current_stage": "DISCOVERY",
            "completed_stages": [],
            "failed_stages": [],
            "retry_counts": {},
            "next_operation": "evaluate required gates",
        })
        normalized = {
            name: self._normalize_gate((gates or {}).get(name))
            for name in REQUIRED_GATES
        }
        instruction_inventory = audit_instruction_files(self.root)
        if instruction_inventory["status"] != "PASS":
            normalized["instruction_inventory"] = "FAIL"
        surface_audit_evidence = (repository_results or {}).get("repository_surface_audit")
        surface_audit_complete = self._repository_surface_audit_evidence_complete(surface_audit_evidence)
        if normalized["repository_surface_audit"] == "UNKNOWN" and surface_audit_complete:
            normalized["repository_surface_audit"] = "PASS"
        elif normalized["repository_surface_audit"] == "PASS" and not surface_audit_complete:
            normalized["repository_surface_audit"] = "UNKNOWN"
        ollama_audit_evidence = (repository_results or {}).get("ollama_reference_audit")
        ollama_audit_complete = self._ollama_reference_audit_evidence_complete(ollama_audit_evidence)
        if normalized["ollama_reference_audit"] == "UNKNOWN" and ollama_audit_complete:
            normalized["ollama_reference_audit"] = "PASS"
        elif normalized["ollama_reference_audit"] == "PASS" and not ollama_audit_complete:
            normalized["ollama_reference_audit"] = "UNKNOWN"
        ui_coverage_evidence = (repository_results or {}).get("ui_test_hook_coverage")
        ui_coverage_complete = self._ui_test_hook_coverage_evidence_complete(ui_coverage_evidence)
        if normalized["ui_test_hook_coverage"] == "UNKNOWN" and ui_coverage_complete:
            normalized["ui_test_hook_coverage"] = "PASS"
        elif normalized["ui_test_hook_coverage"] == "PASS" and not ui_coverage_complete:
            normalized["ui_test_hook_coverage"] = "UNKNOWN"
        restore_point_evidence = (repository_results or {}).get("qmoi_restore_point")
        restore_point_complete = self._qmoi_restore_point_evidence_complete(restore_point_evidence)
        if normalized["qmoi_restore_point"] == "UNKNOWN" and restore_point_complete:
            normalized["qmoi_restore_point"] = "PASS"
        elif normalized["qmoi_restore_point"] == "PASS" and not restore_point_complete:
            normalized["qmoi_restore_point"] = "UNKNOWN"
        local_evidence_checks = self._validate_local_evidence_files()
        if local_evidence_checks["status"] != "PASS":
            normalized["final_verification"] = "FAIL"
        if normalized["markdown_inventory"] == "PASS" and not self._markdown_inventory_evidence_complete(
            (repository_results or {}).get("markdown_inventory")
        ):
            normalized["markdown_inventory"] = "UNKNOWN"
        for name, status in normalized.items():
            self.activity.publish(name, "RUNNING" if status == "PASS" else "BLOCKED", name.upper(), f"Gate {name}: {status}")
            self.checkpoints.record_stage(self.execution_id, name.upper(), status, gate=status)
        failures = list(errors or [])
        failures.extend(f"{name}={value}" for name, value in normalized.items() if value != "PASS")
        next_actions = self._build_next_actions(normalized)
        all_pass = not failures and all(value == "PASS" for value in normalized.values())
        no_changes = all_pass and not any(
            (repository_results or {}).get(key, {}).get("changed_files")
            for key in ("primary", "secondary")
            if isinstance((repository_results or {}).get(key), Mapping)
        )
        status = "NO_CHANGES_REQUIRED" if no_changes else "SUCCESS" if all_pass else "BLOCKED_REQUIRES_HUMAN"
        result = CompletionResult(
            execution_id=self.execution_id,
            status=status,
            stage="FINAL_VERIFICATION" if all_pass else self._first_failed_stage(normalized),
            gates=normalized,
            errors=failures,
            repository_results=dict(repository_results or {}),
            evidence={
                "q_version": discover_q_version(self.root),
                "q_version_audit": QVersionManager(self.root).audit(),
                "topic_metrics": topic_metrics(self.root),
                "repository_surface_audit": {
                    "status": normalized["repository_surface_audit"],
                    "evidence_supplied": isinstance(surface_audit_evidence, Mapping),
                    "coverage_complete": surface_audit_complete,
                },
                "ollama_reference_audit": {
                    "status": normalized["ollama_reference_audit"],
                    "evidence_supplied": isinstance(ollama_audit_evidence, Mapping),
                    "coverage_complete": ollama_audit_complete,
                },
                "ui_test_hook_coverage": {
                    "status": normalized["ui_test_hook_coverage"],
                    "evidence_supplied": isinstance(ui_coverage_evidence, Mapping),
                    "coverage_complete": ui_coverage_complete,
                },
                "qmoi_restore_point": {
                    "status": normalized["qmoi_restore_point"],
                    "evidence_supplied": isinstance(restore_point_evidence, Mapping),
                    "coverage_complete": restore_point_complete,
                },
                "instruction_inventory": instruction_inventory,
                "local_evidence_checks": local_evidence_checks,
                "next_actions": next_actions,
                "production_ready": all_pass,
            },
        )
        self.activity.publish(
            "SUCCESS" if all_pass else "FAILURE",
            "SUCCESS" if all_pass else "BLOCKED",
            result.stage,
            f"Completion evaluation ended with {status}",
            final_status=status,
        )
        self.checkpoints.write(self.execution_id, {
            "current_stage": result.stage,
            "completed_stages": [name.upper() for name, value in normalized.items() if value == "PASS"],
            "failed_stages": [name.upper() for name, value in normalized.items() if value != "PASS"],
            "retry_counts": {},
            "next_operation": next_actions[0]["operation"] if next_actions else None,
            "pending_actions": next_actions,
            "local_evidence_checks": local_evidence_checks,
            "instruction_inventory": instruction_inventory,
            "final_status": status,
        })
        self._write_evidence(result)
        return result

    @staticmethod
    def _has_terminal_exact_sha_binding(
        repository: str,
        item: Mapping[str, Any],
        *,
        required_ref: str | None = None,
    ) -> bool:
        final_sha = str(item.get("final_sha", ""))
        remote_tree_sha = str(item.get("remote_tree_sha", ""))
        workflow_tree_sha = str(item.get("workflow_tree_sha", ""))
        remote_ref = str(item.get("remote_ref", ""))
        run_id = item.get("workflow_run_id")
        return (
            item.get("repository") == repository
            and item.get("repository_identity_verified") is True
            and item.get("remote_verified") is True
            and item.get("terminal_conclusion") == "success"
            and item.get("run_status") == "completed"
            and bool(run_id)
            and not isinstance(run_id, bool)
            and re.fullmatch(r"[0-9a-f]{40}", final_sha) is not None
            and item.get("remote_ref_sha") == final_sha
            and item.get("workflow_head_sha") == final_sha
            and re.fullmatch(r"refs/heads/[^\s]+", remote_ref) is not None
            and (required_ref is None or remote_ref == required_ref)
            and re.fullmatch(r"[0-9a-f]{40}", remote_tree_sha) is not None
            and workflow_tree_sha == remote_tree_sha
        )

    @classmethod
    def _markdown_inventory_evidence_complete(cls, evidence: Any) -> bool:
        """Require terminal, exact-SHA proof for complete Markdown audits of both targets."""
        if not isinstance(evidence, Mapping):
            return False
        if any(evidence.get(name) is not True for name in (
            "remote_verified",
            "all_document_content_validated",
            "all_remote_refs_enumerated",
            "all_pull_requests_included",
            "all_intermediate_commit_trees_validated",
        )):
            return False
        if evidence.get("unavailable_sources") != []:
            return False
        repositories = evidence.get("repositories")
        required_repositories = {
            "thealphakenya/Alpha-Q-ai",
            "thealphakenya/qmoi-enhanced",
        }
        if not isinstance(repositories, Mapping) or not required_repositories.issubset(repositories):
            return False
        for repository in required_repositories:
            item = repositories.get(repository)
            if not isinstance(item, Mapping):
                return False
            total = item.get("markdown_total")
            validated = item.get("markdown_validated")
            if (
                not cls._has_terminal_exact_sha_binding(repository, item)
                or isinstance(total, bool)
                or not isinstance(total, int)
                or total < 1
                or validated != total
                or item.get("failed_documents") != 0
                or item.get("unfetched_refs") != 0
                or item.get("unfetched_pull_requests") != 0
                or item.get("unvalidated_intermediate_trees") != 0
            ):
                return False
        return True

    @classmethod
    def _ollama_reference_audit_evidence_complete(cls, evidence: Any) -> bool:
        """Require complete, dual-repository remote evidence for Ollama-history coverage."""
        if not isinstance(evidence, Mapping):
            return False
        if (
            evidence.get("status") != "PASS"
            or evidence.get("coverage_complete") is not True
            or evidence.get("materialized_scope_complete") is not True
            or not re.fullmatch(r"[0-9a-f]{64}", str(evidence.get("source_manifest_sha256", "")))
            or evidence.get("unavailable_sources") != []
        ):
            return False
        repositories = evidence.get("repositories")
        required_repositories = {
            "thealphakenya/Alpha-Q-ai",
            "thealphakenya/qmoi-enhanced",
        }
        if not isinstance(repositories, Mapping) or set(repositories) != required_repositories:
            return False
        for repository in required_repositories:
            item = repositories.get(repository)
            if not isinstance(item, Mapping):
                return False
            if (
                not cls._has_terminal_exact_sha_binding(repository, item)
                or item.get("all_refs_enumerated") is not True
                or item.get("all_pull_requests_included") is not True
                or item.get("all_intermediate_commit_trees_scanned") is not True
                or item.get("unavailable_sources") != []
            ):
                return False
        return True

    @classmethod
    def _repository_surface_audit_evidence_complete(cls, evidence: Any) -> bool:
        """Require complete, exact-SHA dual-repository evidence for all registered audit surfaces."""
        if not isinstance(evidence, Mapping):
            return False
        if (
            evidence.get("status") != "PASS"
            or evidence.get("coverage_complete") is not True
            or evidence.get("remote_verified") is not True
            or evidence.get("semantic_review_complete") is not True
            or evidence.get("all_required_surfaces_inventoried") is not True
            or evidence.get("all_metrics_mapped") is not True
            or not re.fullmatch(r"[0-9a-f]{64}", str(evidence.get("source_manifest_sha256", "")))
            or evidence.get("unavailable_sources") != []
        ):
            return False
        repositories = evidence.get("repositories")
        required_repositories = {
            "thealphakenya/Alpha-Q-ai",
            "thealphakenya/qmoi-enhanced",
        }
        if not isinstance(repositories, Mapping) or set(repositories) != required_repositories:
            return False
        required_surfaces = {
            "markdown", "api", "endpoints", "routes", "ports", "automation",
            "links", "components", "tree", "styles", "universals", "qvillage_qvs",
            "comparison", "qtrade_metrics", "percentages", "production_gaps", "memory",
        }
        for repository in required_repositories:
            item = repositories.get(repository)
            if not isinstance(item, Mapping):
                return False
            surfaces = item.get("validated_surfaces")
            if (
                not cls._has_terminal_exact_sha_binding(repository, item)
                or not isinstance(surfaces, list)
                or not required_surfaces.issubset(set(surfaces))
                or item.get("all_markdown_structurally_validated") is not True
                or item.get("all_percentages_mapped") is not True
                or item.get("all_metric_candidates_mapped") is not True
                or item.get("unavailable_sources") != []
            ):
                return False
        return True

    @classmethod
    def _ui_test_hook_coverage_evidence_complete(cls, evidence: Any) -> bool:
        """Require feature-level tests and reviewed hook applicability at an exact remote SHA."""
        if not isinstance(evidence, Mapping):
            return False
        if (
            evidence.get("status") != "PASS"
            or evidence.get("coverage_verified") is not True
            or not re.fullmatch(r"[0-9a-f]{64}", str(evidence.get("source_manifest_sha256", "")))
            or evidence.get("unavailable_sources") != []
        ):
            return False
        repositories = evidence.get("repositories")
        required_repositories = {
            "thealphakenya/Alpha-Q-ai",
            "thealphakenya/qmoi-enhanced",
        }
        if not isinstance(repositories, Mapping) or set(repositories) != required_repositories:
            return False
        for repository in required_repositories:
            item = repositories.get(repository)
            if not isinstance(item, Mapping):
                return False
            feature_count = item.get("feature_count")
            if (
                not cls._has_terminal_exact_sha_binding(repository, item)
                or isinstance(feature_count, bool)
                or not isinstance(feature_count, int)
                or feature_count < 1
                or item.get("test_mapped_feature_count") != feature_count
                or item.get("hook_applicability_reviewed_count") != feature_count
                or item.get("unmapped_feature_count") != 0
                or item.get("unreviewed_hook_applicability_count") != 0
                or item.get("unmapped_event_hook_count") != 0
                or item.get("all_feature_tests_passed") is not True
                or item.get("all_event_hook_tests_passed") is not True
                or item.get("unavailable_sources") != []
            ):
                return False
        return True

    @staticmethod
    def _qmoi_restore_point_evidence_complete(evidence: Any) -> bool:
        """Require both repositories' main/backup/qmoi/master refs to prove one committed tree."""
        if not isinstance(evidence, Mapping):
            return False
        workspace_sha = str(evidence.get("workspace_sha", ""))
        tree_sha = str(evidence.get("tree_sha", ""))
        if (
            evidence.get("status") not in {"PASS", "SUCCESS"}
            or evidence.get("branch") != "qmoi"
            or evidence.get("remote_verified") is not True
            or evidence.get("coverage_complete") is not True
            or evidence.get("master_verified") is not True
            or not evidence.get("workflow_run_id")
            or not re.fullmatch(r"[0-9a-f]{40}", workspace_sha)
            or not re.fullmatch(r"[0-9a-f]{40}", tree_sha)
        ):
            return False
        repositories = evidence.get("repositories")
        required_repositories = {
            "thealphakenya/Alpha-Q-ai",
            "thealphakenya/qmoi-enhanced",
        }
        if not isinstance(repositories, Mapping) or set(repositories) != required_repositories:
            return False
        for repository in required_repositories:
            item = repositories.get(repository)
            if not isinstance(item, Mapping):
                return False
            if (
                item.get("repository") != repository
                or item.get("repository_identity_verified") is not True
                or item.get("branch") != "qmoi"
                or item.get("terminal_conclusion") != "success"
                or item.get("remote_verified") is not True
                or item.get("run_status") != "completed"
                or item.get("workflow_run_id") != evidence.get("workflow_run_id")
                or item.get("workflow_head_sha") != workspace_sha
                or item.get("qmoi_sha") != workspace_sha
                or item.get("main_sha") != workspace_sha
                or item.get("backup_sha") != workspace_sha
                or item.get("master_sha") != workspace_sha
                or item.get("branch_tree_sha") != tree_sha
                or item.get("remote_tree_sha") != tree_sha
                or item.get("workflow_tree_sha") != tree_sha
                or item.get("remote_ref_sha") != workspace_sha
                or item.get("remote_ref") not in {
                    "refs/heads/main",
                    "refs/heads/autosync-backup",
                    "refs/heads/master",
                    "refs/heads/qmoi",
                }
                or item.get("required_docs_present") is not True
            ):
                return False
        return True

    @staticmethod
    def _normalize_gate(value: str | bool | None) -> str:
        if value is True or str(value).upper() == "PASS":
            return "PASS"
        if value is False:
            return "FAIL"
        return "UNKNOWN"

    @staticmethod
    def _first_failed_stage(gates: Mapping[str, str]) -> str:
        for name in REQUIRED_GATES:
            if gates[name] != "PASS":
                return name.upper()
        return "FINAL_VERIFICATION"

    @staticmethod
    def _build_next_actions(gates: Mapping[str, str]) -> list[dict[str, Any]]:
        """Turn every non-passing gate into a ranked, resumable action without granting authority."""
        actions = []
        for priority, gate in enumerate(REQUIRED_GATES, start=1):
            gate_status = gates.get(gate, "UNKNOWN")
            if gate_status == "PASS":
                continue
            operation, execution_mode, authorization_required = GATE_ACTIONS[gate]
            actions.append({
                "action_id": f"{gate}:{gate_status.lower()}",
                "priority": priority,
                "gate": gate,
                "gate_status": gate_status,
                "operation": operation,
                "execution_mode": execution_mode,
                "status": "BLOCKED_REQUIRES_AUTHORIZATION" if authorization_required else "QUEUED_SAFE_AUTOMATION",
                "authorization_required": authorization_required,
                "evidence_required": ["execution_id", "repository", "exact_sha", "result", "verification_method"],
            })
        return actions

    def _validate_local_evidence_files(self) -> dict[str, Any]:
        """Check local evidence syntax without copying sensitive values into the report."""
        checks: dict[str, Any] = {}
        json_files = (
            "remote-completion.json",
            "ollamatracks/bank_automation_status.json",
        )
        for relative_path in json_files:
            path = self.root / relative_path
            if not path.exists():
                checks[relative_path] = {"status": "NOT_PRESENT"}
                continue
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
                checks[relative_path] = {
                    "status": "PASS" if isinstance(value, dict) else "INVALID_ROOT_TYPE",
                    "root_type": type(value).__name__,
                }
            except (OSError, json.JSONDecodeError) as exc:
                checks[relative_path] = {"status": "FAIL", "error_type": type(exc).__name__}

        jsonl_files = (
            "remote-evidence-ledger.jsonl",
            "ollamatracks/telemetry.jsonl",
        )
        for relative_path in jsonl_files:
            path = self.root / relative_path
            if not path.exists():
                checks[relative_path] = {"status": "NOT_PRESENT", "records": 0}
                continue
            records = 0
            failure = None
            try:
                for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                    if not line.strip():
                        continue
                    record = json.loads(line)
                    if not isinstance(record, dict):
                        failure = {"status": "INVALID_ROOT_TYPE", "line": line_number}
                        break
                    records += 1
            except (OSError, json.JSONDecodeError) as exc:
                failure = {"status": "FAIL", "error_type": type(exc).__name__}
            checks[relative_path] = failure or {"status": "PASS", "records": records}

        failures = [name for name, result in checks.items() if result.get("status") in {"FAIL", "INVALID_ROOT_TYPE"}]
        return {
            "status": "FAIL" if failures else "PASS",
            "checks": checks,
            "failed_paths": failures,
            "values_recorded": False,
        }

    def _write_evidence(self, result: CompletionResult) -> None:
        track = self.root / "ollamatracks"
        payload = result.as_dict()
        payload["repository_state"] = repository_state(self.root)
        payload["topic_metrics"] = payload["evidence"]["topic_metrics"]
        _json_write(track / "instruction_inventory.json", payload["evidence"]["instruction_inventory"])
        _json_write(track / "executions" / self.execution_id / "execution.json", payload)
        current_state = track / "current_state.json"
        _json_write(current_state, {
            "execution_id": self.execution_id,
            "status": result.status,
            "stage": result.stage,
            "timestamp": utc_now(),
            "heartbeat": result.status not in TERMINAL_STATUSES,
            "pending_actions": result.evidence.get("next_actions", []),
            "local_evidence_checks": result.evidence.get("local_evidence_checks", {}),
        })
        _json_write(track / "topic_metrics.json", payload["topic_metrics"])
        checksum = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        (track / "executions" / self.execution_id / "evidence.sha256").write_text(checksum + "\n", encoding="utf-8")


__all__ = ["AutonomousCompletionEngine", "CompletionResult", "REQUIRED_GATES", "audit_instruction_files", "topic_metrics"]
