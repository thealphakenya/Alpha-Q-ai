"""Fail-closed Q.0.0.N reservations, pair audits, and remote-gated metrics."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit


class QVersionManager:
    SCHEMA_VERSION = 1
    LIFECYCLE_STAGES = (
        "MERGE_START",
        "ALL_BRANCH_INVENTORY",
        "PRE_MERGE_INVENTORY",
        "INTERNAL_RESEARCH",
        "EXTERNAL_RESEARCH",
        "MERGE_PLAN",
        "MERGE_APPLY",
        "POST_MERGE_AUDIT",
        "POST_AGENT_MERGE_PLAN",
        "POST_AGENT_MERGE_APPLY",
        "POST_AGENT_MERGE_AUDIT",
        "PRODUCTION_SCAN",
        "PRODUCTION_REPLACEMENTS",
        "FULL_VALIDATION",
        "REMOTE_VERIFICATION",
        "Q_VERSION_FINALIZATION",
    )
    LIFECYCLE_STATUSES = {"PASS", "IN_PROGRESS", "NEEDS_REVIEW", "BLOCKED", "FAIL"}
    pattern = re.compile(r"^Q\.0\.0\.([1-9][0-9]*)(?:\.md)?$")
    artifact_pattern = pattern
    version_pattern = re.compile(r"^Q\.0\.0\.([1-9][0-9]*)$")
    sha_pattern = re.compile(r"^[0-9a-f]{40}$")
    digest_pattern = re.compile(r"^[0-9a-f]{64}$")

    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.reservations = self.root / "ollamatracks" / "q_versions.json"

    @classmethod
    def parse_version(cls, version: str) -> int:
        """Accept only canonical positive Q.0.0.N identifiers."""
        match = cls.version_pattern.fullmatch(str(version))
        if not match:
            raise ValueError(f"Invalid Q version: {version!r}")
        return int(match.group(1))

    @staticmethod
    def _roots(roots: list[Path] | None, default: Path) -> list[Path]:
        candidates = list(roots) if roots else [default]
        unique: dict[str, Path] = {}
        for candidate in candidates:
            resolved = Path(candidate).resolve()
            unique.setdefault(str(resolved), resolved)
        return list(unique.values())

    def _load_reservation(self) -> dict[str, Any]:
        if not self.reservations.exists():
            return {"reserved": 0, "version": "Q.0.0.0"}
        try:
            data = json.loads(self.reservations.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError("Q-version reservation state is unreadable; refusing to reuse a version") from exc
        if not isinstance(data, dict):
            raise RuntimeError("Q-version reservation state must be a JSON object")
        reserved = data.get("reserved")
        if isinstance(reserved, bool) or not isinstance(reserved, int) or reserved < 0:
            raise RuntimeError("Q-version reservation counter is invalid")
        expected_version = f"Q.0.0.{reserved}"
        if data.get("version", expected_version) != expected_version:
            raise RuntimeError("Q-version reservation identifier does not match its counter")
        if data.get("schema_version", self.SCHEMA_VERSION) != self.SCHEMA_VERSION:
            raise RuntimeError("Unsupported Q-version reservation schema")
        checksum = data.get("integrity_sha256")
        if checksum is not None:
            unsigned = {key: value for key, value in data.items() if key != "integrity_sha256"}
            actual = hashlib.sha256(_canonical_json(unsigned)).hexdigest()
            if not isinstance(checksum, str) or checksum != actual:
                raise RuntimeError("Q-version reservation integrity check failed")
        return data

    def discover(self, roots: list[Path] | None = None) -> int:
        maximum = 0
        for root in self._roots(roots, self.root):
            for path in root.iterdir() if root.is_dir() else ():
                match = self.artifact_pattern.fullmatch(path.name)
                if match:
                    maximum = max(maximum, int(match.group(1)))
        data = self._load_reservation()
        maximum = max(maximum, int(data["reserved"]))
        return maximum

    def latest_artifact(self, roots: list[Path] | None = None) -> str | None:
        """Return the latest materialized version, excluding reservations without artifacts."""
        maximum = 0
        for root in self._roots(roots, self.root):
            for path in root.iterdir() if root.is_dir() else ():
                match = self.artifact_pattern.fullmatch(path.name)
                if match:
                    maximum = max(maximum, int(match.group(1)))
        return f"Q.0.0.{maximum}" if maximum else None

    def reserve(self, roots: list[Path] | None = None) -> str:
        self.reservations.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.reservations.with_suffix(".lock")
        try:
            lock_fd = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise RuntimeError("Q-version reservation is busy; retry remotely") from None
        try:
            lock_data = json.dumps({"pid": os.getpid(), "created_at": _utc_now()}).encode("utf-8")
            os.write(lock_fd, lock_data)
            os.fsync(lock_fd)
            source_roots = self._roots(roots, self.root)
            previous = self._load_reservation()
            next_number = self.discover(source_roots) + 1
            payload = {
                "schema_version": self.SCHEMA_VERSION,
                "reserved": next_number,
                "version": f"Q.0.0.{next_number}",
                "reservation_id": uuid.uuid4().hex,
                "created_at": _utc_now(),
                "previous_reserved": int(previous["reserved"]),
                "source_roots": [str(path) for path in source_roots],
            }
            payload["integrity_sha256"] = hashlib.sha256(_canonical_json(payload)).hexdigest()
            fd, temporary_name = tempfile.mkstemp(
                prefix="q-version-", suffix=".tmp", dir=self.reservations.parent
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as stream:
                    json.dump(payload, stream, indent=2, sort_keys=True)
                    stream.write("\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary_name, self.reservations)
                try:
                    directory_fd = os.open(self.reservations.parent, os.O_RDONLY)
                    try:
                        os.fsync(directory_fd)
                    finally:
                        os.close(directory_fd)
                except OSError:
                    pass
            finally:
                if os.path.exists(temporary_name):
                    os.unlink(temporary_name)
            return payload["version"]
        finally:
            os.close(lock_fd)
            try:
                os.unlink(lock_path)
            except FileNotFoundError:
                pass

    @staticmethod
    def inventory_repository(root: Path | str, *, exclude: set[str] | None = None) -> dict[str, Any]:
        """Hash every filesystem file/directory except Git internals and explicit self-referential outputs."""
        repository = Path(root).resolve()
        if not repository.is_dir():
            return {"root": str(repository), "status": "BLOCKED", "error": "repository root is missing"}
        excluded = set(exclude or ())
        files: list[dict[str, Any]] = []
        directories: list[str] = []
        errors: list[dict[str, str]] = []
        total_bytes = 0
        for current, dirnames, filenames in os.walk(repository, followlinks=False):
            current_path = Path(current)
            retained_directories = []
            for name in dirnames:
                candidate = current_path / name
                relative = candidate.relative_to(repository).as_posix()
                if relative == ".git" or relative.startswith(".git/"):
                    continue
                if relative in excluded or any(item.startswith(relative + "/") for item in excluded):
                    continue
                retained_directories.append(name)
                directories.append(relative)
            dirnames[:] = sorted(retained_directories)
            for name in sorted(filenames):
                path = current_path / name
                relative = path.relative_to(repository).as_posix()
                if relative in excluded or ".git" in Path(relative).parts:
                    continue
                try:
                    if path.is_symlink():
                        target = os.readlink(path)
                        data = target.encode("utf-8", errors="surrogateescape")
                        record = {"path": relative, "kind": "symlink", "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                    else:
                        data = path.read_bytes()
                        record = {"path": relative, "kind": "file", "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                    files.append(record)
                    total_bytes += record["bytes"]
                except OSError as exc:
                    errors.append({"path": relative, "error": str(exc)})
        git_head = _git(repository, "rev-parse", "HEAD")
        git_status = _git(repository, "status", "--porcelain")
        return {
            "root": str(repository),
            "status": "READY" if not errors else "BLOCKED",
            "scope": "filesystem snapshot excluding .git and declared self-referential outputs",
            "file_count": len(files),
            "directory_count": len(directories),
            "total_bytes": total_bytes,
            "files": files,
            "directories": sorted(directories),
            "read_errors": errors,
            "git_head_sha": git_head,
            "worktree_clean": git_status == "" if git_status is not None else False,
        }

    @classmethod
    def branch_inventory_evidence_from_sync_report(
        cls,
        report: dict[str, Any],
        report_sha256: str,
    ) -> dict[str, Any]:
        """Normalize a cross-repository branch audit for the Q-version lifecycle."""
        if not isinstance(report, dict):
            raise ValueError("Branch audit report must be a JSON object")
        coverage = report.get("branch_inventory_coverage", {})
        if not isinstance(coverage, dict):
            raise RuntimeError("Branch report has invalid branch coverage metadata")
        if coverage.get("all_remote_heads_enumerated") is not True:
            raise RuntimeError("Branch report does not prove enumeration of all remote heads")
        workflow = report.get("workflow")
        if (
            not isinstance(workflow, dict)
            or not workflow.get("run_id")
            or not workflow.get("repository")
            or not workflow.get("ref")
            or not cls.sha_pattern.fullmatch(str(workflow.get("head_sha", "")))
        ):
            raise RuntimeError("Branch report lacks target-workflow run, repository, ref, or head SHA")
        if not cls.digest_pattern.fullmatch(str(report_sha256)):
            raise ValueError("Branch audit report requires a SHA-256 digest")
        repositories = report.get("repositories")
        if not isinstance(repositories, dict):
            raise RuntimeError("Branch report is missing repository inventories")
        normalized_repositories: dict[str, dict[str, Any]] = {}
        for name, repository in repositories.items():
            if not isinstance(repository, dict):
                raise RuntimeError(f"Branch report has invalid repository inventory for {name}")
            root_value = str(repository.get("root", ""))
            if not root_value:
                raise RuntimeError(f"Branch report has no repository root for {name}")
            root = str(Path(root_value).resolve())
            branches = repository.get("branches")
            if not isinstance(branches, list):
                raise RuntimeError(f"Branch report has an incomplete inventory for {name}")
            if any(not isinstance(branch, dict) for branch in branches):
                raise RuntimeError(f"Branch report has an invalid branch entry for {name}")
            normalized_repositories[root] = {
                "repository": str(name),
                "branch_count": len(branches),
                "branches": [
                    {
                        "name": str(branch.get("name", "")),
                        "commit_sha": str(branch.get("commit_sha", "")),
                        "tree_sha": str(branch.get("tree_sha", "")),
                        "role": str(branch.get("role", "")),
                        "naming_status": str(branch.get("naming_status", "")),
                        "merge_policy": str(branch.get("merge_policy", "")),
                    }
                    for branch in branches
                ],
            }
        branch_alignment = report.get("branch_alignment", {})
        alignment_entries = branch_alignment.get("branches") if isinstance(branch_alignment, dict) else None
        all_branch_names = {
            branch["name"]
            for repository in normalized_repositories.values()
            for branch in repository["branches"]
        }
        if not isinstance(alignment_entries, list):
            raise RuntimeError("Branch report is missing cross-repository branch dispositions")
        aligned_names = [str(item.get("name", "")) for item in alignment_entries if isinstance(item, dict)]
        if len(aligned_names) != len(alignment_entries) or len(set(aligned_names)) != len(aligned_names):
            raise RuntimeError("Branch report has invalid or duplicate alignment entries")
        if set(aligned_names) != all_branch_names:
            raise RuntimeError("Branch alignment does not cover the union of repository branch names")
        for entry in alignment_entries:
            name = str(entry.get("name", ""))
            expected_auto_publish = name in {"main", "autosync-backup"}
            if entry.get("automatic_publication_allowed") is not expected_auto_publish:
                raise RuntimeError(f"Branch publication policy is invalid for {name}")
            if not entry.get("status") or not entry.get("merge_policy"):
                raise RuntimeError(f"Branch disposition is incomplete for {name}")
        return {
            "remote_verified": True,
            "all_remote_heads_enumerated": True,
            "captured_at": str(report.get("captured_at", "")),
            "source_report_sha256": report_sha256,
            "workflow": {
                "run_id": str(workflow["run_id"]),
                "repository": str(workflow["repository"]),
                "head_sha": str(workflow["head_sha"]),
                "ref": str(workflow["ref"]),
            },
            "branch_alignment": alignment_entries,
            "branches_by_repository": normalized_repositories,
        }

    @classmethod
    def validate_branch_inventory_evidence(
        cls,
        evidence: dict[str, Any] | None,
        roots: list[Path],
    ) -> dict[str, Any]:
        """Check complete, exact branch rosters for all supplied repositories."""
        errors: list[str] = []
        if not isinstance(evidence, dict):
            return {"complete": False, "errors": ["branch inventory evidence is missing"]}
        if evidence.get("remote_verified") is not True:
            errors.append("remote branch inventory is not verified")
        if evidence.get("all_remote_heads_enumerated") is not True:
            errors.append("all remote heads were not enumerated")
        if not evidence.get("captured_at"):
            errors.append("branch inventory capture time is missing")
        if not cls.digest_pattern.fullmatch(str(evidence.get("source_report_sha256", ""))):
            errors.append("source branch report SHA-256 is missing or invalid")
        workflow = evidence.get("workflow")
        if (
            not isinstance(workflow, dict)
            or not workflow.get("run_id")
            or not workflow.get("repository")
            or not workflow.get("ref")
            or not cls.sha_pattern.fullmatch(str(workflow.get("head_sha", "")))
        ):
            errors.append("target workflow identity is missing or invalid")
        repositories = evidence.get("branches_by_repository")
        if not isinstance(repositories, dict):
            return {"complete": False, "errors": errors + ["per-repository branch rosters are missing"]}
        branch_alignment = evidence.get("branch_alignment")
        if not isinstance(branch_alignment, list):
            errors.append("cross-repository branch dispositions are missing")
            branch_alignment = []

        expected_roots = {str(Path(root).resolve()) for root in roots}
        if len(expected_roots) < 2 or set(repositories) != expected_roots:
            errors.append("branch rosters do not exactly cover every target repository")
        normalized_repositories: dict[str, dict[str, Any]] = {}
        for root in sorted(expected_roots & set(repositories)):
            repository = repositories[root]
            branches = repository.get("branches") if isinstance(repository, dict) else None
            if not isinstance(branches, list):
                errors.append(f"branch roster is missing for {root}")
                continue
            names = [str(branch.get("name", "")) for branch in branches if isinstance(branch, dict)]
            if len(names) != len(branches) or len(set(names)) != len(names):
                errors.append(f"branch roster has invalid or duplicate names for {root}")
            if not {"main", "autosync-backup"}.issubset(set(names)):
                errors.append(f"required main/backup branch missing for {root}")
            for branch in branches:
                if not isinstance(branch, dict):
                    continue
                if not cls.sha_pattern.fullmatch(str(branch.get("commit_sha", ""))):
                    errors.append(f"branch commit SHA missing for {root}:{branch.get('name', '')}")
                if not cls.sha_pattern.fullmatch(str(branch.get("tree_sha", ""))):
                    errors.append(f"branch tree SHA missing for {root}:{branch.get('name', '')}")
            if repository.get("branch_count") != len(branches):
                errors.append(f"branch count does not match roster for {root}")
            normalized_repositories[root] = {
                "repository": str(repository.get("repository", "")),
                "branch_count": len(branches),
                "branches": sorted(branches, key=lambda branch: str(branch.get("name", ""))),
            }

        all_branch_names = {
            branch["name"]
            for repository in normalized_repositories.values()
            for branch in repository["branches"]
        }
        aligned_names = [str(item.get("name", "")) for item in branch_alignment if isinstance(item, dict)]
        if len(aligned_names) != len(branch_alignment) or len(set(aligned_names)) != len(aligned_names):
            errors.append("branch dispositions contain invalid or duplicate names")
        if set(aligned_names) != all_branch_names:
            errors.append("branch dispositions do not cover the union of branch names")
        for item in branch_alignment:
            if not isinstance(item, dict):
                continue
            name = str(item.get("name", ""))
            expected_auto_publish = name in {"main", "autosync-backup"}
            if item.get("automatic_publication_allowed") is not expected_auto_publish:
                errors.append(f"automatic publication policy is invalid for {name}")
            if not item.get("status") or not item.get("merge_policy"):
                errors.append(f"branch disposition is incomplete for {name}")

        payload = {
            "captured_at": str(evidence.get("captured_at", "")),
            "source_report_sha256": str(evidence.get("source_report_sha256", "")),
            "workflow": workflow if isinstance(workflow, dict) else {},
            "branch_alignment": branch_alignment,
            "repositories": normalized_repositories,
        }
        complete = not errors
        return {
            "complete": complete,
            "errors": errors,
            "inventory_sha256": hashlib.sha256(_canonical_json(payload)).hexdigest() if complete else None,
            **payload,
        }

    def record_lifecycle_stage(
        self,
        execution_id: str,
        stage: str,
        roots: list[Path],
        *,
        status: str = "IN_PROGRESS",
        details: dict[str, Any] | None = None,
        research_sources: list[dict[str, Any]] | None = None,
        include_inventory: bool = True,
    ) -> dict[str, Any]:
        """Append one hash-chained lifecycle record with source-tree file metrics."""
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", execution_id):
            raise ValueError("Invalid Q-version execution identifier")
        stage_name = str(stage).upper()
        if stage_name not in self.LIFECYCLE_STAGES:
            raise ValueError(f"Unsupported Q-version lifecycle stage: {stage}")
        normalized_status = str(status).upper()
        if normalized_status not in self.LIFECYCLE_STATUSES:
            raise ValueError(f"Unsupported lifecycle status: {status}")

        source_roots = self._roots(roots, self.root)
        normalized_details = dict(details or {})
        if stage_name == "ALL_BRANCH_INVENTORY":
            branch_inventory = self.validate_branch_inventory_evidence(
                normalized_details.get("branch_inventory"), source_roots
            )
            normalized_details["branch_inventory_validation"] = branch_inventory
            if normalized_status == "PASS" and not branch_inventory["complete"]:
                raise RuntimeError("Cannot pass ALL_BRANCH_INVENTORY without complete remote branch evidence")

        execution_dir = self.root / "ollamatracks" / "q_versions" / execution_id
        execution_dir.mkdir(parents=True, exist_ok=True)
        ledger = execution_dir / "lifecycle.jsonl"
        lock_path = execution_dir / "lifecycle.lock"
        try:
            lock_fd = os.open(lock_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            raise RuntimeError("Q-version lifecycle ledger is busy; retry the stage") from None
        try:
            os.write(lock_fd, json.dumps({"pid": os.getpid(), "created_at": _utc_now()}).encode("utf-8"))
            os.fsync(lock_fd)
            existing_lines = ledger.read_text(encoding="utf-8").splitlines() if ledger.is_file() else []
            existing_records = [json.loads(line) for line in existing_lines if line.strip()]
            verification = self._verify_lifecycle_records(existing_records)
            if not verification["valid"]:
                raise RuntimeError("Q-version lifecycle ledger failed integrity verification")
            previous_stage_index = max(
                (self.LIFECYCLE_STAGES.index(record["stage"]) for record in existing_records),
                default=-1,
            )
            stage_index = self.LIFECYCLE_STAGES.index(stage_name)
            if existing_records and stage_index < previous_stage_index:
                raise RuntimeError("Q-version lifecycle stage is out of order")

            root_metrics = {}
            if include_inventory:
                excluded = {f"ollamatracks/q_versions/{execution_id}"}
                root_metrics = {
                    str(root): self.inventory_repository(root, exclude=excluded)
                    for root in source_roots
                }
            normalized_sources = []
            for item in research_sources or []:
                parsed = urlsplit(str(item.get("url", "")))
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    raise ValueError("Research source must be an actually visited HTTP(S) URL")
                normalized_sources.append({
                    "url": urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", "")),
                    "title": str(item.get("title", ""))[:300],
                    "purpose": str(item.get("purpose", ""))[:500],
                    "visited_at": str(item.get("visited_at") or _utc_now()),
                    "repository": str(item.get("repository", "")),
                    "source_sha": str(item.get("source_sha", "")),
                    "content_sha256": str(item.get("content_sha256", "")),
                    "findings": [str(value)[:500] for value in item.get("findings", [])],
                })
            previous_hash = existing_records[-1]["record_sha256"] if existing_records else "0" * 64
            record = {
                "schema_version": self.SCHEMA_VERSION,
                "execution_id": execution_id,
                "sequence": len(existing_records) + 1,
                "correlation_id": uuid.uuid4().hex,
                "timestamp": _utc_now(),
                "stage": stage_name,
                "stage_status": normalized_status,
                "root_metrics": root_metrics,
                "details": normalized_details,
                "external_research_status": "recorded" if normalized_sources else "not_performed_or_not_supplied",
                "external_research_sources": normalized_sources,
                "previous_record_sha256": previous_hash,
            }
            record["record_sha256"] = hashlib.sha256(_canonical_json(record)).hexdigest()
            new_lines = [*existing_lines, json.dumps(record, sort_keys=True, separators=(",", ":"))]
            fd, temporary_name = tempfile.mkstemp(prefix="q-lifecycle-", suffix=".tmp", dir=execution_dir)
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as stream:
                    stream.write("\n".join(new_lines) + "\n")
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary_name, ledger)
            finally:
                if os.path.exists(temporary_name):
                    os.unlink(temporary_name)
            return {**record, "ledger_path": str(ledger)}
        finally:
            os.close(lock_fd)
            try:
                os.unlink(lock_path)
            except FileNotFoundError:
                pass

    def audit_lifecycle(self, execution_id: str) -> dict[str, Any]:
        """Verify lifecycle hash chain, sequence, stage order, and completion coverage."""
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", execution_id):
            raise ValueError("Invalid Q-version execution identifier")
        ledger = self.root / "ollamatracks" / "q_versions" / execution_id / "lifecycle.jsonl"
        if not ledger.is_file():
            return {"execution_id": execution_id, "valid": False, "status": "missing", "records": 0, "missing_stages": list(self.LIFECYCLE_STAGES)}
        try:
            records = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines() if line.strip()]
        except (OSError, json.JSONDecodeError):
            return {"execution_id": execution_id, "valid": False, "status": "invalid_json", "records": 0}
        verification = self._verify_lifecycle_records(records)
        present = {record.get("stage") for record in records if record.get("stage_status") == "PASS"}
        required = set(self.LIFECYCLE_STAGES[:-1])
        missing = [stage for stage in self.LIFECYCLE_STAGES[:-1] if stage not in present]
        return {
            "execution_id": execution_id,
            "ledger_path": str(ledger),
            "valid": verification["valid"],
            "status": "complete" if verification["valid"] and not missing else "incomplete",
            "records": len(records),
            "stage_sequence": [record.get("stage") for record in records],
            "passed_stages": sorted(present, key=self.LIFECYCLE_STAGES.index),
            "missing_or_unpassed_stages": missing,
            "stage_records": [
                {
                    "stage": record.get("stage"),
                    "stage_status": record.get("stage_status"),
                    "details": record.get("details", {}),
                    "root_metrics": record.get("root_metrics", {}),
                    "external_research_status": record.get("external_research_status"),
                    "external_research_sources": record.get("external_research_sources", []),
                }
                for record in records
            ],
            "external_research_sources": [source for record in records for source in record.get("external_research_sources", [])],
            "root_metrics": [record.get("root_metrics", {}) for record in records],
        }

    def _source_tree_clean_except_lifecycle(self, root: Path, execution_id: str) -> bool:
        status = _git(root, "status", "--porcelain", "--untracked-files=all")
        if status is None:
            return False
        allowed_prefix = f"ollamatracks/q_versions/{execution_id}/"
        for line in status.splitlines():
            path = line[3:].strip().replace("\\", "/")
            if root.resolve() == self.root and path.startswith(allowed_prefix):
                continue
            return False
        return True

    @classmethod
    def _verify_lifecycle_records(cls, records: list[dict[str, Any]]) -> dict[str, Any]:
        previous_hash = "0" * 64
        previous_stage_index = -1
        for sequence, record in enumerate(records, start=1):
            if not isinstance(record, dict) or record.get("sequence") != sequence:
                return {"valid": False, "reason": "sequence"}
            stage = record.get("stage")
            if stage not in cls.LIFECYCLE_STAGES:
                return {"valid": False, "reason": "stage"}
            stage_index = cls.LIFECYCLE_STAGES.index(stage)
            if stage_index < previous_stage_index or record.get("previous_record_sha256") != previous_hash:
                return {"valid": False, "reason": "order_or_parent_hash"}
            unsigned = {key: value for key, value in record.items() if key != "record_sha256"}
            actual_hash = hashlib.sha256(_canonical_json(unsigned)).hexdigest()
            if record.get("record_sha256") != actual_hash:
                return {"valid": False, "reason": "record_hash"}
            previous_hash = actual_hash
            previous_stage_index = stage_index
        return {"valid": True, "record_sha256": previous_hash}

    def audit(self, roots: list[Path] | None = None) -> dict[str, Any]:
        """Report reservations, canonical names, pair state, and per-repository metrics."""
        source_roots = self._roots(roots, self.root)
        reservation = self._load_reservation()
        highest_known_number = self.discover(source_roots)
        selected = self.latest_artifact(source_roots)
        pair = self.verify_pair(selected, source_roots) if selected else None
        return {
            "generated_at": _utc_now(),
            "schema_version": self.SCHEMA_VERSION,
            "reserved_version": reservation.get("version") if reservation.get("reserved") else None,
            "latest_materialized_version": selected,
            "highest_known_number": highest_known_number,
            "source_roots": [str(path) for path in source_roots],
            "pair": pair,
            "reservation_file": str(self.reservations),
            "reservation_integrity_verified": bool(reservation.get("integrity_sha256")) or not self.reservations.exists(),
        }

    @staticmethod
    def verify_pair(version: str, roots: list[Path]) -> dict[str, Any]:
        """Verify canonical version artifacts and report each repository's tree metrics."""
        QVersionManager.parse_version(version)
        source_roots = [Path(root).resolve() for root in dict.fromkeys(Path(item).resolve() for item in roots)]
        repositories: dict[str, dict[str, Any]] = {}
        for root in source_roots:
            directory = root / version
            document = root / f"{version}.md"
            repositories[str(root)] = {
                "directory_exists": directory.is_dir(),
                "document_exists": document.is_file(),
                "directory_metrics": QVersionManager.inventory_repository(directory) if directory.is_dir() else None,
            }
        verified = bool(repositories) and all(
            item["directory_exists"] and item["document_exists"]
            for item in repositories.values()
        )
        return {"version": version, "repositories": repositories, "verified": verified}

    def write_final_metrics(
        self,
        version: str,
        roots: list[Path],
        final_evidence: dict[str, Any],
    ) -> dict[str, Any]:
        """Prepare per-repository manifests from a clean remotely validated source tree."""
        self.parse_version(version)
        source_roots = self._roots(roots, self.root)
        if len(source_roots) < 2:
            raise RuntimeError("Final dual-repository Q-version metrics require both target repositories")
        if final_evidence.get("status") != "SUCCESS" or final_evidence.get("remote_verified") is not True:
            raise RuntimeError("Q-version metrics require independently verified remote completion")
        if final_evidence.get("workflow_conclusion") != "success" or not final_evidence.get("workflow_run_id"):
            raise RuntimeError("Q-version metrics require a terminal successful target-owned workflow")
        execution_id = str(final_evidence.get("lifecycle_execution_id", ""))
        if not execution_id:
            raise RuntimeError("Q-version metrics require the complete merge-to-verification lifecycle ledger")
        lifecycle = self.audit_lifecycle(execution_id)
        if not lifecycle.get("valid") or lifecycle.get("status") != "complete":
            raise RuntimeError("Q-version metrics require all ordered lifecycle stages to pass")
        stage_records = {item["stage"]: item for item in lifecycle["stage_records"]}
        branch_inventory_stage = stage_records.get("ALL_BRANCH_INVENTORY", {})
        branch_inventory_details = branch_inventory_stage.get("details", {})
        branch_inventory = branch_inventory_details.get("branch_inventory_validation", {})
        if (
            branch_inventory_stage.get("stage_status") != "PASS"
            or branch_inventory.get("complete") is not True
            or final_evidence.get("branch_inventory_sha256") != branch_inventory.get("inventory_sha256")
        ):
            raise RuntimeError("Q-version metrics require complete final all-branch inventory evidence")
        required_decisions = stage_records.get("MERGE_APPLY", {}).get("details", {})
        if (
            required_decisions.get("decision_ledger_complete") is not True
            or required_decisions.get("conflicts_reviewed") is not True
            or required_decisions.get("unresolved_conflicts") != 0
        ):
            raise RuntimeError("Q-version metrics require complete merge-decision and conflict evidence")
        production = stage_records.get("PRODUCTION_SCAN", {}).get("details", {})
        replacements = stage_records.get("PRODUCTION_REPLACEMENTS", {}).get("details", {})
        if (
            production.get("production_md_present") is not True
            or production.get("productionenhanced_md_present") is not True
            or production.get("unresolved_findings") != 0
            or replacements.get("replacement_records_verified") is not True
            or replacements.get("unresolved_findings") != 0
        ):
            raise RuntimeError("Q-version metrics require production scan and verified replacement evidence")
        validation = stage_records.get("FULL_VALIDATION", {}).get("details", {})
        if (
            validation.get("all_required_tests_passed") is not True
            or validation.get("all_markdown_validated") is not True
            or validation.get("inventory_documents_current") is not True
        ):
            raise RuntimeError("Q-version metrics require complete final validation evidence")
        remote_stage = stage_records.get("REMOTE_VERIFICATION", {}).get("details", {})
        if remote_stage.get("terminal_conclusion") != "success" or remote_stage.get("remote_verified") is not True:
            raise RuntimeError("Lifecycle ledger lacks terminal remote-verification proof")
        correlation_id = str(final_evidence.get("correlation_id", ""))
        if not correlation_id:
            raise RuntimeError("Q-version metrics require a correlation ID")
        repository_evidence = final_evidence.get("repositories")
        if not isinstance(repository_evidence, dict):
            raise RuntimeError("Q-version metrics require exact evidence for every repository")

        validated: list[tuple[Path, dict[str, Any], str]] = []
        for root in source_roots:
            evidence = repository_evidence.get(str(root))
            if not isinstance(evidence, dict):
                raise RuntimeError(f"Missing final remote evidence for {root}")
            sha = str(evidence.get("final_sha", ""))
            if (
                evidence.get("terminal_conclusion") != "success"
                or evidence.get("checks_passed") is not True
                or evidence.get("remote_verified") is not True
                or not self.sha_pattern.fullmatch(sha)
            ):
                raise RuntimeError(f"Remote completion evidence is incomplete for {root}")
            branch_repository = branch_inventory["repositories"].get(str(root), {})
            branch_tips = {
                branch.get("name"): branch
                for branch in branch_repository.get("branches", [])
            }
            if branch_tips.get("main", {}).get("commit_sha") != sha:
                raise RuntimeError(f"Branch inventory main SHA is stale for {root}")
            if evidence.get("autosync_backup_sha") != branch_tips.get("autosync-backup", {}).get("commit_sha"):
                raise RuntimeError(f"Branch inventory backup SHA is stale for {root}")
            git_head = _git(root, "rev-parse", "HEAD")
            if git_head != sha or not self._source_tree_clean_except_lifecycle(root, execution_id):
                raise RuntimeError(f"Local tree does not match the clean verified remote SHA for {root}")
            validated.append((root, evidence, sha))

        results: dict[str, Any] = {}
        for root, evidence, sha in validated:
            version_directory = root / version
            version_document = root / f"{version}.md"
            if version_directory.exists() or version_document.exists():
                raise RuntimeError(f"Refusing to overwrite an existing Q-version artifact in {root}")
            version_directory.mkdir(parents=True, exist_ok=True)
            metrics_path = version_directory / "REPOSITORY_METRICS.json"
            inventory = self.inventory_repository(
                root,
                exclude={
                    f"{version}/{metrics_path.name}",
                    f"{version}.md",
                    f"ollamatracks/q_versions/{execution_id}" if root == self.root else "",
                } - {""},
            )
            if inventory["status"] != "READY" or inventory["git_head_sha"] != sha:
                raise RuntimeError(f"Repository metrics did not validate against the final SHA for {root}")
            payload = {
                "schema_version": self.SCHEMA_VERSION,
                "version": version,
                "publication_status": "PREPARED_PENDING_REMOTE_VERIFICATION",
                "generated_at": _utc_now(),
                "correlation_id": correlation_id,
                "repository": str(root),
                "source_sha": sha,
                "workflow_run_id": str(final_evidence["workflow_run_id"]),
                "workflow_conclusion": "success",
                "checks_passed": True,
                "lifecycle_execution_id": execution_id,
                "lifecycle_ledger": str(self.root / "ollamatracks" / "q_versions" / execution_id / "lifecycle.jsonl"),
                "lifecycle_ledger_sha256": hashlib.sha256(
                    (self.root / "ollamatracks" / "q_versions" / execution_id / "lifecycle.jsonl").read_bytes()
                ).hexdigest(),
                "source_worktree_clean_except_lifecycle_evidence": True,
                "merge_decisions": required_decisions,
                "branch_inventory": branch_inventory,
                "production_scan": production,
                "production_replacements": replacements,
                "validation_summary": validation,
                "external_research_sources": lifecycle["external_research_sources"],
                "metrics": inventory,
                "self_referential_outputs_excluded": [str(metrics_path.relative_to(root)), version_document.name],
            }
            metrics_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            lines = [
                f"# {version} repository completion metrics",
                "",
                "Status: PREPARED_PENDING_REMOTE_PUBLICATION; not a final completion claim.",
                f"Repository: `{root}`",
                f"Metrics source SHA: `{sha}`",
                f"Preparation workflow run: `{final_evidence['workflow_run_id']}` (success)",
                f"Correlation ID: `{correlation_id}`",
                f"Remote branches inventoried: {sum(item['branch_count'] for item in branch_inventory['repositories'].values())}",
                f"Branch inventory SHA-256: `{branch_inventory['inventory_sha256']}`",
                f"Files inventoried: {inventory['file_count']}",
                f"Directories inventoried: {inventory['directory_count']}",
                f"Total file bytes: {inventory['total_bytes']}",
                f"Per-file SHA-256 and path metrics: `{version}/{metrics_path.name}`",
                "The JSON manifest excludes itself and this companion document to avoid recursive self-hashing.",
                "",
            ]
            version_document.write_text("\n".join(lines), encoding="utf-8")
            results[str(root)] = {
                "metrics_file": str(metrics_path),
                "version_document": str(version_document),
                "file_count": inventory["file_count"],
                "directory_count": inventory["directory_count"],
                "final_sha": sha,
            }
        return {
            "version": version,
            "status": "PREPARED_PENDING_REMOTE_VERIFICATION",
            "repositories": results,
            "correlation_id": correlation_id,
            "next_action": "Commit/publish through an authorized target-owned workflow, then verify its terminal success and exact resulting SHA with verify_final_publication.",
        }

    def verify_final_publication(
        self,
        version: str,
        roots: list[Path],
        final_evidence: dict[str, Any],
    ) -> dict[str, Any]:
        """Verify already-published Q artifacts against terminal remote evidence without mutating them."""
        self.parse_version(version)
        source_roots = self._roots(roots, self.root)
        if final_evidence.get("status") != "SUCCESS" or final_evidence.get("remote_verified") is not True:
            raise RuntimeError("Published Q artifacts require independently verified remote success")
        if final_evidence.get("workflow_conclusion") != "success" or not final_evidence.get("workflow_run_id"):
            raise RuntimeError("Published Q artifacts require a terminal successful verification workflow")
        correlation_id = str(final_evidence.get("correlation_id", ""))
        if not correlation_id:
            raise RuntimeError("Published Q artifact verification requires a correlation ID")
        repositories = final_evidence.get("repositories")
        if not isinstance(repositories, dict):
            raise RuntimeError("Published Q artifact verification requires both repository records")

        verified: dict[str, Any] = {}
        for root in source_roots:
            item = repositories.get(str(root))
            if not isinstance(item, dict):
                raise RuntimeError(f"Missing published-state evidence for {root}")
            final_sha = str(item.get("final_sha", ""))
            if (
                item.get("terminal_conclusion") != "success"
                or item.get("remote_verified") is not True
                or item.get("checks_passed") is not True
                or not self.sha_pattern.fullmatch(final_sha)
            ):
                raise RuntimeError(f"Final remote evidence is incomplete for {root}")
            metrics_path = root / version / "REPOSITORY_METRICS.json"
            document_path = root / f"{version}.md"
            if not metrics_path.is_file() or not document_path.is_file():
                raise RuntimeError(f"Published Q-version pair is incomplete for {root}")
            metrics_hash = hashlib.sha256(metrics_path.read_bytes()).hexdigest()
            document_hash = hashlib.sha256(document_path.read_bytes()).hexdigest()
            if item.get("metrics_sha256") != metrics_hash or item.get("version_document_sha256") != document_hash:
                raise RuntimeError(f"Published Q-version artifact hashes do not match remote evidence for {root}")
            git_head = _git(root, "rev-parse", "HEAD")
            git_status = _git(root, "status", "--porcelain")
            if git_head != final_sha or git_status is None or git_status:
                raise RuntimeError(f"Local tree does not match the clean verified published SHA for {root}")
            payload = json.loads(metrics_path.read_text(encoding="utf-8"))
            if (
                payload.get("version") != version
                or payload.get("publication_status") != "PREPARED_PENDING_REMOTE_VERIFICATION"
                or payload.get("source_sha") != item.get("prepared_source_sha")
                or payload.get("branch_inventory", {}).get("inventory_sha256") != final_evidence.get("branch_inventory_sha256")
            ):
                raise RuntimeError(f"Published Q-version manifest provenance is inconsistent for {root}")
            branch_repository = payload["branch_inventory"]["repositories"].get(str(root), {})
            branch_tips = {branch.get("name"): branch for branch in branch_repository.get("branches", [])}
            if (
                item.get("prepared_source_sha") != branch_tips.get("main", {}).get("commit_sha")
                or item.get("autosync_backup_sha") != branch_tips.get("autosync-backup", {}).get("commit_sha")
            ):
                raise RuntimeError(f"Published branch evidence does not match the Q-version roster for {root}")
            verified[str(root)] = {
                "prepared_source_sha": payload["source_sha"],
                "published_final_sha": final_sha,
                "workflow_run_id": str(final_evidence["workflow_run_id"]),
                "metrics_sha256": metrics_hash,
                "version_document_sha256": document_hash,
            }
        return {
            "version": version,
            "status": "SUCCESS",
            "remote_verified": True,
            "workflow_run_id": str(final_evidence["workflow_run_id"]),
            "correlation_id": correlation_id,
            "repositories": verified,
        }


def _canonical_json(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _git(root: Path, *arguments: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip()
