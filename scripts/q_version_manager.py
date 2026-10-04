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

            source_roots = self._roots(roots, self.root)
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
                "details": dict(details or {}),
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

    @staticmethod
    def verify_instruction_inventory(root: Path | str, instruction_inventory: Any) -> dict[str, Any]:
        """Verify instruction inventory coverage and hashes against the current repository tree."""
        target = Path(root).resolve()
        expected_paths = set()
        for relative in ("AGENTS.md", ".github/copilot-instructions.md"):
            candidate = target / relative
            if candidate.is_file() and not candidate.is_symlink():
                expected_paths.add(relative)
        instruction_root = target / ".github" / "instructions"
        if instruction_root.is_dir():
            expected_paths.update(
                candidate.relative_to(target).as_posix()
                for candidate in instruction_root.rglob("*")
                if candidate.is_file() and not candidate.is_symlink()
            )
        if not isinstance(instruction_inventory, dict):
            raise RuntimeError(f"Instruction inventory is incomplete or unsafe for {target}")
        files = instruction_inventory.get("files")
        if (
            instruction_inventory.get("status") != "PASS"
            or instruction_inventory.get("files_discovered") != len(expected_paths)
            or instruction_inventory.get("files_read") != len(expected_paths)
            or instruction_inventory.get("unreadable_or_invalid") != []
            or instruction_inventory.get("source_contents_recorded") is not False
            or not isinstance(files, list)
        ):
            raise RuntimeError(f"Instruction inventory is incomplete or unsafe for {target}")
        reported_paths = set()
        try:
            for item in files:
                if not isinstance(item, dict):
                    raise ValueError("invalid record")
                if set(item) != {"path", "bytes", "sha256", "apply_to", "nonempty"}:
                    raise ValueError("unexpected instruction evidence field")
                relative_path = str(item.get("path", ""))
                path = Path(relative_path)
                source = target / path
                if (
                    path.is_absolute()
                    or ".." in path.parts
                    or relative_path not in expected_paths
                    or relative_path in reported_paths
                    or not source.is_file()
                    or source.is_symlink()
                    or item.get("bytes") != source.stat().st_size
                    or item.get("sha256") != hashlib.sha256(source.read_bytes()).hexdigest()
                    or not isinstance(item.get("apply_to"), str)
                    or item.get("nonempty") is not True
                ):
                    raise ValueError("record mismatch")
                reported_paths.add(relative_path)
        except (OSError, ValueError):
            raise RuntimeError(f"Instruction inventory is incomplete or unsafe for {target}") from None
        if reported_paths != expected_paths:
            raise RuntimeError(f"Instruction inventory is incomplete or unsafe for {target}")
        return instruction_inventory

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
        instruction_inventories = final_evidence.get("instruction_inventories")
        if not isinstance(instruction_inventories, dict):
            raise RuntimeError("Q-version metrics require instruction inventories for both repositories")
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
        for root in source_roots:
            self.verify_instruction_inventory(root, instruction_inventories.get(str(root)))
        autonomous_completion = final_evidence.get("autonomous_completion")
        if (
            not isinstance(autonomous_completion, dict)
            or autonomous_completion.get("status") not in {"SUCCESS", "NO_CHANGES_REQUIRED"}
            or not autonomous_completion.get("execution_id")
            or not isinstance(autonomous_completion.get("gates"), dict)
            or not autonomous_completion["gates"]
            or any(value != "PASS" for value in autonomous_completion["gates"].values())
            or autonomous_completion["gates"].get("instruction_inventory") != "PASS"
            or autonomous_completion["gates"].get("final_verification") != "PASS"
            or autonomous_completion.get("next_actions") != []
        ):
            raise RuntimeError("Q-version metrics require terminal autonomous completion with no pending actions")
        production_readiness = final_evidence.get("production_readiness")
        if (
            not isinstance(production_readiness, dict)
            or production_readiness.get("status") != "CLEAR"
            or production_readiness.get("coverage_complete") is not True
            or production_readiness.get("candidate_count") != 0
            or production_readiness.get("unreadable_files") != []
            or production_readiness.get("oversized_files_not_read") != 0
        ):
            raise RuntimeError("Q-version metrics require complete production readiness evidence with zero candidates")

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
                "production_scan": production,
                "production_replacements": replacements,
                "validation_summary": validation,
                "instruction_inventory": instruction_inventories[str(root)],
                "autonomous_completion": {
                    "execution_id": autonomous_completion.get("execution_id"),
                    "status": autonomous_completion["status"],
                    "gates": autonomous_completion["gates"],
                    "next_actions": [],
                },
                                "production_readiness": production_readiness,
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
                f"Files inventoried: {inventory['file_count']}",
                f"Directories inventoried: {inventory['directory_count']}",
                f"Total file bytes: {inventory['total_bytes']}",
                f"Instruction files inventoried: {instruction_inventories[str(root)]['files_read']}",
                "Autonomous completion gates: all PASS; pending actions: 0.",
                                "Production readiness: complete inventory; zero unresolved candidates.",
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
            ):
                raise RuntimeError(f"Published Q-version manifest provenance is inconsistent for {root}")
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
