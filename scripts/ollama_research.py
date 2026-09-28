"""Evidence-first internal and external research controls for the QMOI agent."""
from __future__ import annotations

import hashlib
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit

INTERNAL_RESEARCH_CONTROLS = (
    "inventory every supplied repository, snapshot, and history root before planning changes",
    "read governing instructions, merge policy, validation contracts, and prior execution ledgers first",
    "inventory source, tests, workflows, docs, build manifests, APIs, endpoints, routes, and ports by path",
    "enumerate locally available branches, tags, PR refs, commits, and tree identities without claiming unfetched coverage",
    "retain per-source and per-file path, size, content hash, timestamp, and provenance when accessible",
    "map requirements to implementation symbols, tests, workflows, documentation, and owning repositories",
    "compare candidate changes with current and historical behavior to identify additions, duplicates, and regressions",
    "record unresolved ownership, missing sources, unreadable files, and conflicting evidence as blockers",
    "turn each accepted research finding into a testable change hypothesis and focused validation",
    "refresh memory, merge, Markdown, validation, and Q-version evidence from measured results rather than estimates",
)

EXTERNAL_RESEARCH_CONTROLS = (
    "fetch only HTTPS resources on an explicit official-domain allowlist",
    "reject user-info, credentials, tokens, local hosts, private addresses, and unapproved domains",
    "use bounded timeouts, response sizes, content types, and redirect refusal",
    "record the actual visit time, canonical URL, title, research question, and repository/ref/SHA context",
    "hash fetched content and store only metadata, findings, and bounded text needed for research",
    "prefer primary vendor, language, platform, security-advisory, and standards documentation",
    "cross-check security-critical claims against independent primary sources where feasible",
    "discover links as candidates but require domain-policy review before visiting unknown hosts",
    "mark inaccessible, stale, contradictory, or rate-limited resources as blocked instead of inferring facts",
    "retain citations and limitations in the research ledger and connect each finding to a validation case",
)

OFFICIAL_RESEARCH_DOMAINS = frozenset({
    "docs.github.com",
    "github.blog",
    "docs.python.org",
    "docs.pytest.org",
    "docs.ollama.com",
    "ollama.com",
    "owasp.org",
    "cheatsheetseries.owasp.org",
    "docs.docker.com",
    "docs.npmjs.com",
    "pip.pypa.io",
    "packaging.python.org",
    "docs.pydantic.dev",
    "vercel.com",
    "docs.netlify.com",
    "docs.gitlab.com",
    "docs.gitpod.io",
    "huggingface.co",
    "docs.qdrant.tech",
    "w3.org",
    "www.rfc-editor.org",
})

OFFICIAL_RESOURCE_CATALOG = (
    {"url": "https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication", "topic": "github-actions-auth", "purpose": "least-privilege workflow token and repository permission validation"},
    {"url": "https://docs.github.com/en/rest", "topic": "github-rest-api", "purpose": "remote repository, pull request, workflow, and evidence API behavior"},
    {"url": "https://docs.python.org/3/library/urllib.request.html", "topic": "python-http-client", "purpose": "bounded standards-compliant HTTPS research access"},
    {"url": "https://docs.pytest.org/en/stable/", "topic": "python-testing", "purpose": "deterministic test collection and validation strategy"},
    {"url": "https://docs.ollama.com/", "topic": "ollama-runtime", "purpose": "official Ollama API and runtime behavior"},
    {"url": "https://cheatsheetseries.owasp.org/", "topic": "application-security", "purpose": "security validation and remediation guidance"},
    {"url": "https://packaging.python.org/en/latest/", "topic": "python-packaging", "purpose": "build, install, and release validation"},
    {"url": "https://docs.docker.com/", "topic": "container-builds", "purpose": "reproducible container and environment validation"},
    {"url": "https://docs.npmjs.com/", "topic": "javascript-packages", "purpose": "dependency and package lifecycle validation"},
    {"url": "https://vercel.com/docs", "topic": "vercel-deployment", "purpose": "deployment, build, and hosted runtime validation"},
    {"url": "https://docs.netlify.com/", "topic": "netlify-deployment", "purpose": "deployment configuration and runtime validation"},
    {"url": "https://www.w3.org/TR/WCAG22/", "topic": "accessibility", "purpose": "accessibility acceptance criteria and UI validation"},
    {"url": "https://www.rfc-editor.org/rfc/rfc9110", "topic": "http-semantics", "purpose": "HTTP protocol behavior for APIs and endpoint validation"},
    {"url": "https://docs.gitlab.com/ee/", "topic": "gitlab-ci", "purpose": "cross-platform repository and pipeline integration research"},
    {"url": "https://huggingface.co/docs", "topic": "model-hosting", "purpose": "model, dataset, and hosted inference integration research"},
)

VALIDATION_RESEARCH_MAP = {
    "markdown": ("python-testing", "github-rest-api"),
    "links": ("github-rest-api", "http-semantics"),
    "apps_and_ui": ("accessibility", "python-testing"),
    "platforms_and_devices": ("accessibility", "container-builds"),
    "api_endpoints_routes_ports": ("http-semantics", "github-rest-api"),
    "build_install_download": ("python-packaging", "javascript-packages", "container-builds"),
    "dependencies_and_security": ("application-security", "github-actions-auth", "javascript-packages"),
    "workflows_and_hooks": ("github-actions-auth", "github-rest-api"),
    "ollama_runtime_and_models": ("ollama-runtime", "model-hosting"),
    "hosting_and_deployment": ("vercel-deployment", "netlify-deployment", "gitlab-ci"),
    "memory_and_q_seed": ("python-testing",),
    "production_and_release": ("python-packaging", "github-rest-api", "application-security"),
}

MAX_RESOURCE_BYTES = 256 * 1024
ALLOWED_CONTENT_TYPES = ("text/html", "text/plain", "text/markdown", "application/json", "application/xhtml+xml")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canonical_url(url: str) -> tuple[str, str]:
    parsed = urlsplit(str(url).strip())
    if parsed.scheme.lower() != "https" or not parsed.hostname:
        raise ValueError("External research requires an HTTPS URL")
    if parsed.username or parsed.password:
        raise ValueError("External research URLs must not contain user-info or credentials")
    hostname = parsed.hostname.rstrip(".").lower()
    if hostname in {"localhost", "localhost.localdomain"} or hostname.endswith((".local", ".internal", ".localhost")):
        raise ValueError("Local and private-network hosts are not valid research sources")
    if not any(hostname == domain or hostname.endswith("." + domain) for domain in OFFICIAL_RESEARCH_DOMAINS):
        raise ValueError("External research domain is not allowlisted")
    port = parsed.port
    if port not in (None, 443):
        raise ValueError("External research permits only the standard HTTPS port")
    canonical = urlunsplit(("https", hostname, parsed.path or "/", "", ""))
    return canonical, hostname


def build_internal_research_plan(roots: Iterable[Path | str]) -> dict[str, Any]:
    """Describe complete local research scope without reading or exporting file contents."""
    reports = []
    for value in roots:
        root = Path(value).resolve()
        files = 0
        directories = 0
        bytes_total = 0
        unreadable = 0
        suffix_counts: dict[str, int] = {}
        if root.is_dir():
            for current, dirnames, filenames in os.walk(root, followlinks=False):
                dirnames[:] = sorted(name for name in dirnames if name != ".git")
                current_path = Path(current)
                directories += len(dirnames)
                for filename in filenames:
                    path = current_path / filename
                    files += 1
                    suffix = path.suffix.lower() or "[no extension]"
                    suffix_counts[suffix] = suffix_counts.get(suffix, 0) + 1
                    try:
                        bytes_total += path.stat(follow_symlinks=False).st_size
                    except OSError:
                        unreadable += 1
        reports.append({
            "root": str(root),
            "exists": root.is_dir(),
            "file_count": files,
            "directory_count": directories,
            "total_bytes": bytes_total,
            "unreadable_metadata_count": unreadable,
            "file_types": dict(sorted(suffix_counts.items())),
            "scope": "materialized filesystem excluding .git internals; Git refs and commit trees require separate inventory",
        })
    return {
        "generated_at": utc_now(),
        "controls": list(INTERNAL_RESEARCH_CONTROLS),
        "source_roots": reports,
        "automatic_merge_authorized": False,
        "limitations": [
            "future commits and PRs do not exist yet and cannot be pre-audited",
            "unfetched refs, inaccessible repositories, and intermediate commit trees require target-owned remote enumeration",
            "inventory metadata is not proof that every file's semantic requirements were understood",
        ],
    }


def build_external_research_plan(topics: Iterable[str] | None = None) -> dict[str, Any]:
    """Select official resources relevant to current topics without fetching them."""
    requested = {str(topic).strip().lower() for topic in (topics or ()) if str(topic).strip()}
    resources = [
        dict(item)
        for item in OFFICIAL_RESOURCE_CATALOG
        if not requested or item["topic"] in requested
    ]
    return {
        "generated_at": utc_now(),
        "controls": list(EXTERNAL_RESEARCH_CONTROLS),
        "requested_topics": sorted(requested),
        "selected_resources": resources,
        "resource_count": len(resources),
        "fetch_policy": {
            "https_only": True,
            "official_domain_allowlist": sorted(OFFICIAL_RESEARCH_DOMAINS),
            "redirects": "refused",
            "maximum_response_bytes": MAX_RESOURCE_BYTES,
            "maximum_timeout_seconds": 15,
            "unknown_domains": "candidate_only_until_policy_review",
        },
        "visited_sources": [],
        "status": "PLANNED_NOT_VISITED",
    }


def build_validation_research_matrix(
    visited_sources: Iterable[dict[str, Any]] = (),
) -> dict[str, Any]:
    """Connect each validation class to relevant official resources without inferring a pass."""
    visited_by_topic: dict[str, list[dict[str, Any]]] = {}
    for source in visited_sources:
        topic = str(source.get("topic", ""))
        if topic:
            visited_by_topic.setdefault(topic, []).append({
                "url": str(source.get("url", "")),
                "visited_at": str(source.get("visited_at", "")),
                "content_sha256": str(source.get("content_sha256", "")),
            })
    matrix = {}
    for validation_kind, topics in VALIDATION_RESEARCH_MAP.items():
        matrix[validation_kind] = {
            "required_research_topics": list(topics),
            "visited_sources": {
                topic: visited_by_topic.get(topic, [])
                for topic in topics
            },
            "research_status": (
                "VISITED"
                if all(visited_by_topic.get(topic) for topic in topics)
                else "PLANNED_OR_NOT_VISITED"
            ),
            "validation_status": "NOT_EVALUATED_BY_RESEARCH",
            "required_validation_evidence": [
                "implementation or target evidence",
                "deterministic tests/validation result",
                "exact repository/ref/SHA and timestamp",
                "limitations and unavailable sources",
            ],
        }
    return {
        "generated_at": utc_now(),
        "validation_domains": matrix,
        "research_does_not_pass_validation": True,
    }


def discover_resource_candidates(source_url: str, links: Iterable[str]) -> list[dict[str, str]]:
    """Classify observed links; never turn newly discovered hosts into auto-fetch authority."""
    source, _ = _canonical_url(source_url)
    candidates = []
    for link in links:
        try:
            canonical, hostname = _canonical_url(link)
            status = "allowlisted_candidate"
            reason = "host is already in the official-resource allowlist; fetch is still per-request and bounded"
        except ValueError as exc:
            canonical = str(link).split("?", 1)[0].split("#", 1)[0][:500]
            try:
                hostname = urlsplit(str(link)).hostname or ""
            except ValueError:
                hostname = ""
            status = "review_required"
            reason = str(exc)
        candidates.append({
            "source_url": source,
            "candidate_url": canonical,
            "hostname": hostname.lower(),
            "status": status,
            "reason": reason,
        })
    return candidates


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, response, code, message, headers, new_url):
        raise urllib.error.HTTPError(request.full_url, code, "redirect refused by research policy", headers, None)


def fetch_official_resource(url: str, *, timeout_seconds: float = 8.0, max_bytes: int = MAX_RESOURCE_BYTES) -> dict[str, Any]:
    """Fetch one allowlisted source with strict bounds; callers decide whether to persist the returned text."""
    canonical, hostname = _canonical_url(url)
    if not 0 < timeout_seconds <= 15 or not 0 < max_bytes <= MAX_RESOURCE_BYTES:
        raise ValueError("External research timeout or response size exceeds policy")
    request = urllib.request.Request(canonical, headers={"User-Agent": "QMOI-Research/1.0", "Accept": ", ".join(ALLOWED_CONTENT_TYPES)})
    opener = urllib.request.build_opener(_NoRedirect())
    try:
        with opener.open(request, timeout=timeout_seconds) as response:
            content_type = response.headers.get_content_type().lower()
            if not any(content_type == item or content_type.startswith(item + ";") for item in ALLOWED_CONTENT_TYPES):
                raise ValueError(f"Research response content type is not permitted: {content_type}")
            body = response.read(max_bytes + 1)
            if len(body) > max_bytes:
                raise ValueError("Research response exceeded the configured byte limit")
            try:
                text = body.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise ValueError("Research response is not valid UTF-8") from exc
            return {
                "status": "FETCHED",
                "url": canonical,
                "hostname": hostname,
                "visited_at": utc_now(),
                "content_type": content_type,
                "http_status": int(response.status),
                "bytes": len(body),
                "content_sha256": hashlib.sha256(body).hexdigest(),
                "text": text,
                "credential_values_recorded": False,
            }
    except (OSError, urllib.error.URLError, TimeoutError) as exc:
        return {
            "status": "BLOCKED",
            "url": canonical,
            "hostname": hostname,
            "visited_at": utc_now(),
            "error_class": type(exc).__name__,
            "error": str(exc)[:300],
            "credential_values_recorded": False,
        }


def record_research_visit(
    *,
    url: str,
    title: str,
    question: str,
    purpose: str,
    content: bytes,
    findings: Iterable[str],
    limitations: Iterable[str],
    repository: str,
    ref: str,
    source_sha: str,
) -> dict[str, Any]:
    """Create a secret-free, content-hashed visit record tied to code and validation work."""
    canonical, hostname = _canonical_url(url)
    if not question.strip() or not purpose.strip() or not repository.strip() or not ref.strip():
        raise ValueError("Research question, purpose, repository, and ref are required")
    if not re.fullmatch(r"[0-9a-f]{40}", source_sha):
        raise ValueError("Research visit requires an exact source SHA")
    return {
        "url": canonical,
        "hostname": hostname,
        "title": title.strip()[:300],
        "question": question.strip()[:500],
        "purpose": purpose.strip()[:500],
        "visited_at": utc_now(),
        "content_sha256": hashlib.sha256(content).hexdigest(),
        "content_bytes": len(content),
        "findings": [str(item)[:500] for item in findings],
        "limitations": [str(item)[:500] for item in limitations],
        "repository": repository,
        "ref": ref,
        "source_sha": source_sha,
        "validation_case_ids": [],
        "credential_values_recorded": False,
    }
