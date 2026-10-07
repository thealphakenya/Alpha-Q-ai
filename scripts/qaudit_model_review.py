"""Optional, bounded local-Ollama candidate review for one explicitly selected file."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import stat
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlsplit

import requests

from scripts.qaudit_checkpoint import record_qaudit_checkpoint

PROMPT_POLICY_VERSION = "qaudit-local-review-v1"
MAX_SOURCE_BYTES = 32 * 1024
MAX_FINDINGS = 12
MAX_RESPONSE_BYTES = 64 * 1024
ALLOWED_SUFFIXES = {".md", ".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".yml", ".yaml"}
ALLOWED_CATEGORIES = {
    "security",
    "authorization",
    "correctness",
    "privacy",
    "finance",
    "reliability",
    "testing",
    "documentation",
    "performance",
    "resource_usage",
}
ALLOWED_SEVERITIES = {"low", "medium", "high", "critical"}
ALLOWED_RECOMMENDATIONS = {
    "map_requirement_to_test",
    "inspect_auth_boundary",
    "verify_error_handling",
    "measure_resource_budget",
    "verify_data_provenance",
    "human_semantic_review",
}
SENSITIVE_PATH_PARTS = {
    ".env",
    "credentials",
    "private",
    "secrets",
    "tokens",
    "passwords",
    "keys",
}
SENSITIVE_CONTENT_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(
        r"\b(?:api[_-]?key|access[_-]?token|password|client[_-]?secret|private[_-]?key)"
        r"\s*[:=]\s*['\"][^'\"]{8,}['\"]",
        re.IGNORECASE,
    ),
)
OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "enum": sorted(ALLOWED_CATEGORIES)},
                    "severity": {"type": "string", "enum": sorted(ALLOWED_SEVERITIES)},
                    "line": {"type": "integer", "minimum": 1},
                    "recommendation": {
                        "type": "string",
                        "enum": sorted(ALLOWED_RECOMMENDATIONS),
                    },
                },
                "required": ["category", "severity", "line", "recommendation"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["findings"],
    "additionalProperties": False,
}


class AuditModelReviewError(ValueError):
    """A bounded, value-free reason why local model review could not run."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _local_endpoint(raw: str) -> str:
    parsed = urlsplit(raw)
    if (
        parsed.scheme != "http"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        raise AuditModelReviewError(
            "local_endpoint_invalid",
            "Use an HTTP URL with a literal loopback IP, port, and no path or credentials.",
        )
    try:
        address = ipaddress.ip_address(parsed.hostname)
    except ValueError as exc:
        raise AuditModelReviewError(
            "local_endpoint_not_literal_loopback",
            "The inference host must be a literal loopback IP address.",
        ) from exc
    if not address.is_loopback:
        raise AuditModelReviewError(
            "local_endpoint_not_loopback",
            "External inference endpoints are not permitted by this command.",
        )
    try:
        port = parsed.port or 11434
    except ValueError as exc:
        raise AuditModelReviewError(
            "local_endpoint_invalid",
            "The local inference endpoint has an invalid port.",
        ) from exc
    return f"http://{parsed.hostname}:{port}"


def _selected_source(root: Path, relative_path: str) -> tuple[Path, str, bytes]:
    requested = Path(relative_path)
    if requested.is_absolute() or ".." in requested.parts:
        raise AuditModelReviewError(
            "source_path_invalid",
            "The selected source must use a repository-relative path without parent traversal.",
        )
    candidate = root / requested
    cursor = root
    for component in requested.parts:
        cursor /= component
        if cursor.is_symlink():
            raise AuditModelReviewError(
                "source_symlink_blocked",
                "Symlinked source paths are not eligible.",
            )
    try:
        source = candidate.resolve(strict=True)
        source.relative_to(root)
    except (OSError, ValueError) as exc:
        raise AuditModelReviewError(
            "source_path_invalid",
            "The selected source must be an existing file inside the repository root.",
        ) from exc
    if not source.is_file() or source.suffix.lower() not in ALLOWED_SUFFIXES:
        raise AuditModelReviewError(
            "source_type_unsupported",
            "Select one regular Markdown, source, JSON, or YAML file.",
        )
    if any(part.lower() in SENSITIVE_PATH_PARTS for part in source.relative_to(root).parts):
        raise AuditModelReviewError(
            "sensitive_source_path_blocked",
            "Files in credential, private-key, secret, token, password, or .env paths are blocked.",
        )
    try:
        descriptor = os.open(source, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        raise AuditModelReviewError(
            "source_open_failed",
            f"Unable to open selected source: {type(exc).__name__}.",
        ) from exc
    try:
        details = os.fstat(descriptor)
        if not stat.S_ISREG(details.st_mode):
            raise AuditModelReviewError("source_not_regular", "Selected source is not a regular file.")
        if details.st_size > MAX_SOURCE_BYTES:
            raise AuditModelReviewError(
                "source_size_limit_exceeded",
                f"Selected source exceeds the {MAX_SOURCE_BYTES}-byte review limit.",
            )
        chunks = bytearray()
        while chunk := os.read(descriptor, MAX_SOURCE_BYTES + 1 - len(chunks)):
            chunks.extend(chunk)
            if len(chunks) > MAX_SOURCE_BYTES:
                raise AuditModelReviewError(
                    "source_size_limit_exceeded",
                    f"Selected source exceeds the {MAX_SOURCE_BYTES}-byte review limit.",
                )
    finally:
        os.close(descriptor)
    try:
        text = bytes(chunks).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise AuditModelReviewError("source_not_utf8", "Selected source is not valid UTF-8.") from exc
    if any(pattern.search(text) for pattern in SENSITIVE_CONTENT_PATTERNS):
        raise AuditModelReviewError(
            "sensitive_source_content_blocked",
            "Selected source matched a credential or private-key safety pattern.",
        )
    return source, text, bytes(chunks)


def _request_json(
    session: Any,
    method: str,
    endpoint: str,
    path: str,
    *,
    timeout: tuple[float, float] = (3.0, 45.0),
    **kwargs: Any,
) -> dict[str, Any]:
    response = None
    try:
        response = session.request(
            method,
            f"{endpoint}{path}",
            timeout=timeout,
            stream=True,
            **kwargs,
        )
        response.raise_for_status()
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_RESPONSE_BYTES:
            raise AuditModelReviewError(
                "model_response_size_limit_exceeded",
                "Local inference response exceeded the review-size limit.",
            )
        content = bytearray()
        for chunk in response.iter_content(chunk_size=8192):
            content.extend(chunk)
            if len(content) > MAX_RESPONSE_BYTES:
                raise AuditModelReviewError(
                    "model_response_size_limit_exceeded",
                    "Local inference response exceeded the review-size limit.",
                )
        payload = json.loads(content)
    except AuditModelReviewError:
        raise
    except (requests.RequestException, ValueError, OSError) as exc:
        raise AuditModelReviewError(
            "local_inference_request_failed",
            f"Local inference request failed: {type(exc).__name__}.",
        ) from exc
    finally:
        if response is not None:
            response.close()
    if not isinstance(payload, dict):
        raise AuditModelReviewError("local_inference_response_invalid", "Inference returned an invalid object.")
    return payload


def _validate_findings(raw: Any, lines: list[str]) -> list[dict[str, Any]]:
    if not isinstance(raw, dict) or set(raw) != {"findings"} or not isinstance(raw["findings"], list):
        raise AuditModelReviewError("model_output_schema_rejected", "Model output did not match the review schema.")
    if len(raw["findings"]) > MAX_FINDINGS:
        raise AuditModelReviewError("model_output_limit_exceeded", "Model returned too many findings.")
    findings = []
    seen: set[tuple[Any, ...]] = set()
    for finding in raw["findings"]:
        if not isinstance(finding, dict) or set(finding) != {
            "category",
            "severity",
            "line",
            "recommendation",
        }:
            raise AuditModelReviewError("model_output_schema_rejected", "A model finding has an invalid shape.")
        category = finding["category"]
        severity = finding["severity"]
        recommendation = finding["recommendation"]
        line_number = finding["line"]
        if (
            not isinstance(category, str)
            or not isinstance(severity, str)
            or not isinstance(recommendation, str)
            or category not in ALLOWED_CATEGORIES
            or severity not in ALLOWED_SEVERITIES
            or recommendation not in ALLOWED_RECOMMENDATIONS
            or isinstance(line_number, bool)
            or not isinstance(line_number, int)
            or not 1 <= line_number <= len(lines)
        ):
            raise AuditModelReviewError("model_output_schema_rejected", "A model finding has invalid values.")
        identity = (category, severity, line_number, recommendation)
        if identity in seen:
            continue
        seen.add(identity)
        line_digest = hashlib.sha256(lines[line_number - 1].encode("utf-8")).hexdigest()
        findings.append({
            "category": category,
            "severity": severity,
            "line": line_number,
            "source_line_sha256": line_digest,
            "recommendation": recommendation,
            "verification_status": "unverified_model_candidate",
        })
    return findings


def _write_report(root: Path, correlation_id: str, report: dict[str, Any]) -> tuple[str, str, int]:
    relative = Path("ollamatracks") / "qaudit_model_reviews" / f"{correlation_id}.json"
    directory = root / relative.parent
    if (root / "ollamatracks").is_symlink() or directory.is_symlink():
        raise AuditModelReviewError("report_directory_symlink_blocked", "Review artifact directory is symlinked.")
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise AuditModelReviewError(
            "report_directory_create_failed",
            f"Unable to create review artifact directory: {type(exc).__name__}.",
        ) from exc
    if (root / "ollamatracks").is_symlink() or directory.is_symlink():
        raise AuditModelReviewError("report_directory_symlink_blocked", "Review artifact directory is symlinked.")
    destination = root / relative
    payload = json.dumps(report, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    try:
        descriptor = os.open(
            destination,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
    except FileExistsError as exc:
        raise AuditModelReviewError("report_path_collision", "Refusing to overwrite a review artifact.") from exc
    except OSError as exc:
        raise AuditModelReviewError(
            "report_write_failed",
            f"Unable to create review artifact: {type(exc).__name__}.",
        ) from exc
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("Short write while persisting the review artifact")
            view = view[written:]
        os.fsync(descriptor)
    except OSError as exc:
        destination.unlink(missing_ok=True)
        raise AuditModelReviewError(
            "report_write_failed",
            f"Unable to persist review artifact: {type(exc).__name__}.",
        ) from exc
    finally:
        os.close(descriptor)
    return (
        relative.as_posix(),
        hashlib.sha256(payload).hexdigest(),
        len(payload),
    )


def review_source(
    root: Path,
    relative_path: str,
    model: str,
    endpoint: str,
    *,
    consent: bool,
    session: Any | None = None,
    selection: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if not consent:
        raise AuditModelReviewError(
            "explicit_local_content_consent_required",
            "Pass --allow-local-content-inference to send the selected file to loopback Ollama.",
        )
    if not model.strip() or len(model) > 160:
        raise AuditModelReviewError("model_name_invalid", "Provide a bounded exact local model tag.")
    target = root.resolve(strict=True)
    local_endpoint = _local_endpoint(endpoint)
    source, text, raw_bytes = _selected_source(target, relative_path)
    source_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    request_session = session or requests.Session()
    if hasattr(request_session, "trust_env"):
        request_session.trust_env = False
    version_data = _request_json(request_session, "GET", local_endpoint, "/api/version")
    tags_data = _request_json(request_session, "GET", local_endpoint, "/api/tags")
    versions = [
        item for item in tags_data.get("models", [])
        if isinstance(item, dict) and item.get("name") == model
    ]
    if not versions:
        raise AuditModelReviewError(
            "local_model_not_installed",
            "The exact model tag is not present locally; this command will not pull or install models.",
        )
    model_digest = str(versions[0].get("digest", ""))
    if not re.fullmatch(r"sha256:[0-9a-fA-F]{64}", model_digest):
        raise AuditModelReviewError(
            "local_model_digest_unavailable",
            "The local model tag did not provide a valid digest.",
        )
    prompt = (
        "Review the selected source for potential correctness, security, privacy, reliability, "
        "test, finance, documentation, performance, and resource-use issues. Return JSON matching "
        "the supplied schema only. Findings must cite a 1-based source line and use only an "
        "allowed category, severity, and recommendation code. Do not quote source text. Do not "
        "claim a defect is verified, do not claim the source is safe, and do not propose edits. "
        f"Source path: {source.relative_to(target).as_posix()}\n"
        f"Source SHA-256: {source_sha256}\n"
        f"Source text follows:\n{text}"
    )
    generated = _request_json(
        request_session,
        "POST",
        local_endpoint,
        "/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": OUTPUT_SCHEMA,
            "options": {"temperature": 0, "num_ctx": 4096, "num_predict": 512},
        },
    )
    generated_text = generated.get("response")
    if not isinstance(generated_text, str):
        raise AuditModelReviewError("model_output_schema_rejected", "Model response was not text.")
    try:
        raw_findings = json.loads(generated_text)
    except json.JSONDecodeError as exc:
        raise AuditModelReviewError(
            "model_output_schema_rejected",
            "Model response was not valid JSON.",
        ) from exc
    findings = _validate_findings(raw_findings, text.splitlines())
    _, _, current_bytes = _selected_source(target, relative_path)
    if hashlib.sha256(current_bytes).hexdigest() != source_sha256:
        raise AuditModelReviewError(
            "source_changed_during_review",
            "Source changed while review was running; candidate results were discarded.",
        )
    correlation_id = str(uuid.uuid4())
    report = {
        "schema_version": 1,
        "correlation_id": correlation_id,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": "CANDIDATES_ONLY" if findings else "NO_CANDIDATES_REQUIRES_HUMAN_REVIEW",
        "source_path": source.relative_to(target).as_posix(),
        "source_sha256": source_sha256,
        "source_bytes": len(raw_bytes),
        "model": {
            "name": model,
            "digest": model_digest.lower(),
            "server_version": str(version_data.get("version", "unknown")),
        },
        "prompt_policy_version": PROMPT_POLICY_VERSION,
        "selection": {
            "method": str((selection or {}).get("method", "explicit_path")),
            "priority": (selection or {}).get("priority"),
            "priority_queue_sha256": (selection or {}).get("priority_queue_sha256"),
            "source_manifest_sha256": (selection or {}).get("source_manifest_sha256"),
        },
        "findings": findings,
        "remote_verified": False,
        "source_modified": False,
    }
    artifact_path, artifact_sha256, artifact_bytes = _write_report(
        target,
        correlation_id,
        report,
    )
    checkpoint = record_qaudit_checkpoint(
        target,
        "qaudit-local-model-review",
        {
            "status": report["status"],
            "artifact_path": artifact_path,
            "artifact_sha256": artifact_sha256,
            "artifact_bytes": artifact_bytes,
            "artifact_refs": {
                "qaudit_model_review": {
                    "path": artifact_path,
                    "sha256": artifact_sha256,
                    "bytes": artifact_bytes,
                },
            },
            "metrics": {
                "source_sha256": source_sha256,
                "source_bytes": len(raw_bytes),
                "model_name": model,
                "model_digest": model_digest.lower(),
                "ollama_server_version": str(version_data.get("version", "unknown")),
                "prompt_policy_version": PROMPT_POLICY_VERSION,
                "selection_method": report["selection"]["method"],
                "priority": report["selection"]["priority"],
                "priority_queue_sha256": report["selection"]["priority_queue_sha256"],
                "source_manifest_sha256": report["selection"]["source_manifest_sha256"],
                "finding_count": len(findings),
                "candidate_findings": True,
                "source_modified": False,
                "remote_verified": False,
            },
            "next_action": (
                "Review candidate findings against the exact source SHA and tests; "
                "model output cannot authorize edits or pass a QAUDITS gate."
            ),
        },
        correlation_id=correlation_id,
    )
    return {
        "status": report["status"],
        "correlation_id": correlation_id,
        "source_path": report["source_path"],
        "selection": report["selection"],
        "artifact_path": artifact_path,
        "artifact_sha256": artifact_sha256,
        "finding_count": len(findings),
        "source_sha256": source_sha256,
        "source_modified": False,
        "remote_verified": False,
        "checkpoint": checkpoint,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run an explicitly authorized, bounded local-Ollama QAUDITS candidate review."
    )
    parser.add_argument("--repository-root", default=".")
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--source", help="One repository-relative source path.")
    selection.add_argument(
        "--next-priority-candidate",
        action="store_true",
        help="Select one fresh, eligible source from the complete deterministic QAUDITS queue.",
    )
    parser.add_argument("--model", required=True, help="Exact model tag already installed locally.")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434")
    parser.add_argument(
        "--allow-local-content-inference",
        action="store_true",
        help="Explicitly consent to sending the selected source to the loopback Ollama process.",
    )
    return parser


def _reviewed_source_hashes(root: Path) -> set[tuple[str, str]]:
    tracking_dir = root / "ollamatracks"
    review_dir = root / "ollamatracks" / "qaudit_model_reviews"
    if tracking_dir.is_symlink():
        raise AuditModelReviewError(
            "review_history_unavailable",
            "The local audit-tracking path is symlinked.",
        )
    if not review_dir.exists():
        return set()
    if review_dir.is_symlink() or not review_dir.is_dir():
        raise AuditModelReviewError(
            "review_history_unavailable",
            "The local review history path is not a regular directory.",
        )
    reviewed: set[tuple[str, str]] = set()
    for artifact in sorted(review_dir.glob("*.json")):
        if artifact.is_symlink() or not artifact.is_file():
            raise AuditModelReviewError(
                "review_history_unavailable",
                "A local model-review history artifact is not a regular file.",
            )
        try:
            record = json.loads(artifact.read_text(encoding="utf-8"))
            source_path = record.get("source_path")
            source_sha256 = record.get("source_sha256")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AuditModelReviewError(
                "review_history_unavailable",
                f"Unable to read prior review metadata: {type(exc).__name__}.",
            ) from exc
        if isinstance(source_path, str) and isinstance(source_sha256, str):
            reviewed.add((source_path, source_sha256))
    return reviewed


def select_next_priority_candidate(root: Path) -> dict[str, Any]:
    from scripts.qaudit_universe import build_qaudit_universe

    target = root.resolve(strict=True)
    universe = build_qaudit_universe(target)
    queue = universe["audit_queue"]
    reviewed = _reviewed_source_hashes(target)
    for item in queue["items"]:
        relative_path = str(item.get("path", ""))
        record = universe["classes"].get(relative_path, {})
        source = target / relative_path
        if (
            not relative_path
            or source.suffix.lower() not in ALLOWED_SUFFIXES
            or record.get("content_scan_status") != "scanned"
            or (relative_path, str(item.get("sha256", ""))) in reviewed
        ):
            continue
        try:
            size = source.stat().st_size
        except OSError:
            continue
        if size > MAX_SOURCE_BYTES or item.get("sha256") != record.get("sha256"):
            continue
        return {
            "source": relative_path,
            "priority": item["priority"],
            "reasons": item["reasons"],
            "priority_queue_sha256": queue["queue_sha256"],
            "source_manifest_sha256": queue["source_manifest_sha256"],
            "selection_method": "fresh_deterministic_priority_queue",
        }
    raise AuditModelReviewError(
        "no_eligible_priority_candidate",
        "No unreviewed, size-bounded source is eligible in the current QAUDITS priority queue.",
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.repository_root).expanduser()
    correlation_id = str(uuid.uuid4())
    try:
        if not args.allow_local_content_inference:
            raise AuditModelReviewError(
                "explicit_local_content_consent_required",
                "Pass --allow-local-content-inference to send the selected file to loopback Ollama.",
            )
        selection_metadata: dict[str, Any] = {
            "method": "explicit_path",
            "priority": None,
            "priority_queue_sha256": None,
            "source_manifest_sha256": None,
        }
        source_path = args.source
        if args.next_priority_candidate:
            selected = select_next_priority_candidate(root)
            source_path = selected["source"]
            selection_metadata = {
                "method": selected["selection_method"],
                "priority": selected["priority"],
                "priority_queue_sha256": selected["priority_queue_sha256"],
                "source_manifest_sha256": selected["source_manifest_sha256"],
            }
        result = review_source(
            root,
            source_path,
            args.model,
            args.endpoint,
            consent=args.allow_local_content_inference,
            selection=selection_metadata,
        )
    except AuditModelReviewError as exc:
        checkpoint = record_qaudit_checkpoint(
            root,
            "qaudit-local-model-review",
            {
                "status": "BLOCKED",
                "metrics": {
                    "candidate_findings": False,
                    "source_modified": False,
                    "remote_verified": False,
                },
                "blockers": [exc.code],
                "next_action": str(exc),
            },
            correlation_id=correlation_id,
        )
        print(
            json.dumps(
                {
                    "status": "BLOCKED",
                    "blocker": exc.code,
                    "checkpoint": checkpoint,
                    "remote_verified": False,
                    "source_modified": False,
                },
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
