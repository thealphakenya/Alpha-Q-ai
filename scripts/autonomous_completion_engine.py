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
                item.get("terminal_conclusion") != "success"
                or item.get("remote_verified") is not True
                or not re.fullmatch(r"[0-9a-f]{40}", str(item.get("final_sha", "")))
                or not item.get("workflow_run_id")
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
