"""Evidence-first internal and external research controls for the QMOI agent."""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import uuid
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
    "hash and structurally validate every accessible Markdown document while keeping semantic review and remote-history proof separate",
    "inventory API, endpoint, route, port, automation, link, component, tree, style, universal, clone, QVS, QVillage, compare, and Qtrade surfaces by exact path",
    "extract metric and percentage candidate locations with source hashes, preserving values only for explicit percentage tokens and never treating claims as benchmark proof",
    "turn production-gap matches into prioritized owner/test/security/rollback tasks; never bulk-rewrite candidates from search results",
    "refresh awareness, memory, QVillage, and resumable action evidence from the same correlated audit without self-authorizing protected actions",
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
    "select official research topics from discovered repository surfaces and maintain a per-domain visited/not-visited matrix",
    "evaluate model comparisons with reproducible benchmark methodology and distinguish source claims from measured results",
    "review license, code/model availability, resource cost, bandwidth, reliability, security, and rollback before proposing adoption",
    "map external findings to exact implementation paths, tests, hooks, docs, and limitations; external research alone never authorizes changes",
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
    "www.itl.nist.gov",
    "cftc.gov",
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
    {"url": "https://huggingface.co/docs/evaluate/index", "topic": "model-evaluation", "purpose": "reproducible metric definitions and evaluation workflows"},
    {"url": "https://huggingface.co/docs/hub/index", "topic": "huggingface-research", "purpose": "official model, dataset, Space, license, and Hub capability research"},
    {"url": "https://www.itl.nist.gov/div898/handbook/", "topic": "statistical-methods", "purpose": "measurement, uncertainty, sampling, and statistical comparison methodology"},
    {"url": "https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/index.htm", "topic": "financial-controls", "purpose": "official risk and consumer-protection guidance for financial/trading workflow audits"},
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
    "metrics_and_comparisons": ("model-evaluation", "statistical-methods", "python-testing"),
    "qtrade_and_financial_metrics": ("financial-controls", "statistical-methods", "application-security"),
    "qvillage_qvs_and_research_adoption": ("huggingface-research", "model-hosting", "application-security"),
    "tree_components_and_repo_inventory": ("github-rest-api", "python-testing"),
    "styles_universals_hooks_and_webhooks": ("accessibility", "application-security", "github-actions-auth"),
    "memory_awareness_and_q_versions": ("python-testing", "github-rest-api"),
    "projects_and_autoprojects": ("github-rest-api", "application-security", "python-testing"),
}

MAX_RESOURCE_BYTES = 256 * 1024
ALLOWED_CONTENT_TYPES = ("text/html", "text/plain", "text/markdown", "application/json", "application/xhtml+xml")
SURFACE_DOCUMENTS = {
    "markdown_index": ("ALLMDFILESREFS.md",),
    "api": ("API.md",),
    "endpoints": ("ENDPOINTS.md",),
    "routes": ("ROUTES.md", "ALLROUTES.md"),
    "ports": ("ALLPORTS.md",),
    "automation": ("ALLAUTO.md",),
    "links": ("ALLLINKS.md",),
    "components": ("COMPONENTS.md",),
    "tree": ("TREE.md", "TREE_FULL_STRUCTURE.md"),
    "comparison": ("compare.md", "QMOI_MODEL_CARD.md", "QMOI_BEST_MODEL_PROOF.md"),
    "trading": ("Qtrade.md", "TRADINGREADME.md"),
    "styles": ("STYLES.md",),
    "universals": ("UNIVERSALS.md", "UNIVERSAL.md"),
    "qvillage_qvs": ("QVILLAGE.md", "Qvillageevolutions.md", "QVS.md", "ENHANCEDQVS.md"),
    "internal_research": ("INTERNALRESEARCH.md", "INTERNALREFSEARCH.md"),
    "external_research": ("EXTERIORRESEARCH.md", "EXTERNALRESEARCH.md"),
    "instructions": ("AGENTS.md", "copilot-instructions.md"),
    "production_metrics": ("production.md", "productionenhanced.md", "FEATURES_AND_PERCENTAGES.md", "compare.md", "Qtrade.md"),
    "projects_autoprojects": ("projectsandautoprojects.md", "projectsandautoprojectsenhanced.md", "projectsndautoprojects.md", "projectandautoprojects.md"),
}
MARKDOWN_DOCUMENT_FAMILY_PATTERNS = {
    "app_platform": re.compile(r"\b(?:apps?|applications?|platforms?|mobile|desktop)\b", re.IGNORECASE),
    "build_download_install": re.compile(r"\b(?:builds?|compile|install(?:ation)?s?|packages?|downloads?|artifacts?)\b", re.IGNORECASE),
    "release_tag_publish": re.compile(r"\b(?:releases?|tags?|publish(?:ed|ing)?|versions?|artifacts?)\b", re.IGNORECASE),
    "qteam_accountability": re.compile(r"\b(?:qteam|accountability|ownership|owners?|approvals?|governance)\b", re.IGNORECASE),
    "orchestration": re.compile(r"\b(?:orchestras?|orchestration|orchestrators?|coordination|pipelines?)\b", re.IGNORECASE),
    "tree_inventory": re.compile(r"\b(?:trees?|directory structure|folder structure|file inventory|repository structure|filesystem)\b", re.IGNORECASE),
    "disability_accessibility": re.compile(r"\b(?:disabilit\w*|accessibility|a11y|blind|low vision|deaf|hard of hearing|captions?|screen readers?|assistive technology|dyslex\w*|neurodiverg\w*|motor impairment|cognitive access|epilepsy|reduced motion|switch control)\b", re.IGNORECASE),
}
HISTORICAL_PATH_COMPONENT_PATTERN = re.compile(
    r"(?:^|[-_.])(?:19|20)\d{2}(?:[-_.]|$)",
    re.IGNORECASE,
)
AUDIT_IGNORED_DIRECTORIES = frozenset({
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".next", ".turbo", "dist", "build", "target", "coverage",
})
AUDIT_MAX_FILE_BYTES = 100_000_000
AUDIT_MAX_TEXT_BYTES = 5_000_000
MAX_MARKDOWN_SENTENCE_RECORDS = 100_000
MARKDOWN_SENTENCE_AUDIT_JSONL = "ollamatracks/qaudit_markdown_sentence_audit.jsonl.gz"
MARKDOWN_SENTENCE_AUDIT_MANIFEST = "ollamatracks/qaudit_markdown_sentence_audit.json"
AUDIT_SELF_REFERENTIAL_REPORTS = {
    "ollamatracks/repository_surface_audit.json",
    MARKDOWN_SENTENCE_AUDIT_JSONL,
    MARKDOWN_SENTENCE_AUDIT_MANIFEST,
    "ollamatracks/qaudit_universe.json",
    "ollamatracks/ollama_reference_audit.json",
    "ollamatracks/feature_test_hook_coverage.json",
    "ollamatracks/system_accountability_audit.json",
    "ollamatracks/qaudits_evolution_plan.json",
    "ollamatracks/style_universal_replacement_inventory.json",
    "ollamatracks/legacy_sync_artifact_inventory.json",
    "ollamatracks/restore_point_memory.json",
    "ollamatracks/production_gap_inventory.json",
    "ollamatracks/telemetry.jsonl",
    "oe2.txt",
    "remotecompletion.md",
    "remote-completion.json",
    "remote-evidence-ledger.jsonl",
    "QMOItracks/style_universal_candidate_tree.md",
}
METRIC_TERM_PATTERN = re.compile(
    r"\b(?:accuracy|precision|recall|f1|latency|throughput|speed|ram|memory|gpu|bandwidth|cost|reliability|benchmark|confidence|percentage|percent|ratio|sharpe|drawdown|win rate|profit|loss|slippage|roi)\b",
    re.IGNORECASE,
)
INSTRUCTION_CANDIDATE_PATTERN = re.compile(
    r"\b(?:must|shall|required|should|always|never|ensure|do not|cannot|can only|blocked unless)\b",
    re.IGNORECASE,
)
INSTRUCTION_TEXT_SUFFIXES = frozenset({".md", ".txt", ".rst", ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".sh"})
PERCENT_PATTERN = re.compile(r"(?<![\w.])\d+(?:\.\d+)?\s*%")
CALCULATION_PATTERN = re.compile(r"(?:=|\+|\*|/|\b(?:formula|calculate|calculated|calculation|average|mean|median|sum|ratio|rate)\b)", re.IGNORECASE)
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
COMPONENT_SUFFIXES = frozenset({".tsx", ".jsx", ".ts", ".js", ".vue", ".svelte", ".css", ".scss"})
AUDIT_METRIC_SUFFIXES = frozenset({".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".css", ".scss", ".json", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".txt", ".sh"})


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _source_scope(relative_path: str) -> str:
    historical_components = {"archive", "archives", "history", "historical", "backups", "snapshots"}
    for component in Path(relative_path).parts:
        lowered = component.lower()
        component_tokens = set(re.split(r"[-_.]+", lowered))
        if (
            component_tokens & historical_components
            or HISTORICAL_PATH_COMPONENT_PATTERN.search(lowered)
        ):
            return "historical_or_archive_candidate"
    return "materialized_repository"


def _markdown_document_families(relative_path: str, text: str) -> list[str]:
    searchable = f"{relative_path}\n{text}"
    return sorted(
        family
        for family, pattern in MARKDOWN_DOCUMENT_FAMILY_PATTERNS.items()
        if pattern.search(searchable)
    )


def _markdown_sentence_evidence(text: str) -> dict[str, Any]:
    """Index bounded sentence and word-sequence evidence without persisting source prose."""
    boundaries = [
        match.end()
        for match in re.finditer(r"[.!?]+(?=\s|$)|\n+", text)
    ]
    if not boundaries or boundaries[-1] < len(text):
        boundaries.append(len(text))

    records: list[dict[str, Any]] = []
    omitted = 0
    total_word_count = 0
    duplicate_adjacent_word_candidate_count = 0
    metric_claim_candidate_count = 0
    completion_claim_candidate_count = 0
    unreferenced_metric_claim_candidate_count = 0
    unreferenced_completion_claim_candidate_count = 0
    line_number = 1
    start = 0
    for end in boundaries:
        fragment = text[start:end]
        normalized = fragment.strip()
        start = end
        line_start = line_number + fragment[: len(fragment) - len(fragment.lstrip())].count("\n")
        line_number += fragment.count("\n")
        if not normalized:
            continue
        words = re.findall(r"\b[\w'-]+\b", normalized, re.UNICODE)
        total_word_count += len(words)
        duplicate_adjacent_word = any(
            left.casefold() == right.casefold()
            for left, right in zip(words, words[1:])
        )
        has_metric_claim = bool(
            METRIC_TERM_PATTERN.search(normalized) or PERCENT_PATTERN.search(normalized)
        )
        has_completion_claim = bool(
            re.search(
                r"\b(?:complete(?:d)?|success(?:ful)?|passed|merged|published|released|deployed|production[- ]ready)\b",
                normalized,
                re.IGNORECASE,
            )
        )
        has_reference_marker = bool(
            MARKDOWN_LINK_PATTERN.search(normalized)
            or re.search(r"https?://|(?:\[[0-9]+\])", normalized, re.IGNORECASE)
        )
        duplicate_adjacent_word_candidate_count += duplicate_adjacent_word
        metric_claim_candidate_count += has_metric_claim
        completion_claim_candidate_count += has_completion_claim
        unreferenced_metric_claim_candidate_count += has_metric_claim and not has_reference_marker
        unreferenced_completion_claim_candidate_count += (
            has_completion_claim and not has_reference_marker
        )
        if len(records) >= MAX_MARKDOWN_SENTENCE_RECORDS:
            omitted += 1
            continue
        word_sequence = "\x1f".join(word.casefold() for word in words)
        records.append({
            "sentence_index": len(records) + 1,
            "line_start": line_start,
            "line_end": line_number,
            "word_count": len(words),
            "sentence_sha256": hashlib.sha256(normalized.encode("utf-8")).hexdigest(),
            "word_sequence_sha256": hashlib.sha256(word_sequence.encode("utf-8")).hexdigest(),
            "duplicate_adjacent_word_candidate": duplicate_adjacent_word,
            "metric_claim_candidate": has_metric_claim,
            "completion_claim_candidate": has_completion_claim,
            "reference_marker_present": has_reference_marker,
            "semantic_status": "unverified_requires_source_and_owner_mapping",
        })

    return {
        "sentence_count_heuristic": len(records) + omitted,
        "sentence_records": records,
        "sentence_records_omitted_by_bound": omitted,
        "word_count": total_word_count,
        "duplicate_adjacent_word_candidate_count": duplicate_adjacent_word_candidate_count,
        "metric_claim_candidate_count": metric_claim_candidate_count,
        "completion_claim_candidate_count": completion_claim_candidate_count,
        "unreferenced_metric_claim_candidate_count": unreferenced_metric_claim_candidate_count,
        "unreferenced_completion_claim_candidate_count": unreferenced_completion_claim_candidate_count,
        "semantic_validation": "sentence_and_word_sequence_hashes_are_integrity_metadata_only",
        "source_text_recorded": False,
    }


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


def audit_repository_surfaces(roots: Iterable[Path | str]) -> dict[str, Any]:
    """Inventory repository surfaces and document metrics without exporting source text."""
    audit_started = time.monotonic()
    root_reports: list[dict[str, Any]] = []
    all_file_records: list[dict[str, Any]] = []
    all_directories: list[dict[str, Any]] = []
    unavailable_roots: list[str] = []
    audit_domains = set(VALIDATION_RESEARCH_MAP)
    audit_topics = {topic for topics in VALIDATION_RESEARCH_MAP.values() for topic in topics}

    for value in roots:
        root_started = time.monotonic()
        root = Path(value).resolve()
        if not root.is_dir():
            unavailable_roots.append(str(root))
            root_reports.append({
                "root": str(root),
                "exists": False,
                "status": "BLOCKED",
                "file_count": 0,
                "directory_count": 0,
                "files": [],
                "directories": [],
                "source_contents_recorded": False,
                "scan_duration_seconds": round(time.monotonic() - root_started, 3),
            })
            continue

        file_records: list[dict[str, Any]] = []
        markdown_records: list[dict[str, Any]] = []
        directories: list[dict[str, Any]] = []
        unreadable: list[dict[str, str]] = []
        skipped: list[dict[str, Any]] = []
        links: list[dict[str, Any]] = []
        metric_candidates: list[dict[str, Any]] = []
        percentage_candidates: list[dict[str, Any]] = []
        calculation_candidates: list[dict[str, Any]] = []
        instruction_candidates: list[dict[str, Any]] = []
        instruction_candidate_line_count = 0
        all_metric_candidate_count = 0
        directory_counts: dict[str, int] = {}
        suffix_counts: dict[str, int] = {}
        surface_files: dict[str, list[str]] = {name: [] for name in SURFACE_DOCUMENTS}
        surface_paths: dict[str, list[str]] = {name: [] for name in SURFACE_DOCUMENTS}
        file_count = 0
        byte_count = 0
        markdown_count = 0
        component_count = 0
        api_source_count = 0
        endpoint_source_count = 0
        route_source_count = 0
        automation_source_count = 0
        content_digest = hashlib.sha256()
        self_referential_exclusions: list[str] = []

        for current, dirnames, filenames in os.walk(root, followlinks=False):
            current_path = Path(current)
            retained = []
            for dirname in sorted(dirnames):
                child = current_path / dirname
                relative_dir = child.relative_to(root).as_posix()
                if dirname in AUDIT_IGNORED_DIRECTORIES:
                    skipped.append({"path": relative_dir, "reason": "excluded_generated_or_dependency_directory"})
                elif child.is_symlink():
                    skipped.append({"path": relative_dir, "reason": "symlink_directory_not_followed"})
                else:
                    retained.append(dirname)
                    directories.append(relative_dir)
            dirnames[:] = retained

            for filename in sorted(filenames):
                path = current_path / filename
                relative = path.relative_to(root).as_posix()
                if path.is_symlink():
                    skipped.append({"path": relative, "reason": "symlink_file_not_followed"})
                    continue
                try:
                    size = path.stat(follow_symlinks=False).st_size
                except OSError as exc:
                    unreadable.append({"path": relative, "error_type": type(exc).__name__})
                    continue
                file_count += 1
                byte_count += size
                parent = Path(relative).parent
                while str(parent) not in {"", "."}:
                    key = parent.as_posix()
                    directory_counts[key] = directory_counts.get(key, 0) + 1
                    parent = parent.parent

                suffix = path.suffix.lower()
                name = path.name.lower()
                lowered = relative.lower()
                suffix_counts[suffix or "[no extension]"] = suffix_counts.get(suffix or "[no extension]", 0) + 1
                roles = []
                for surface, names in SURFACE_DOCUMENTS.items():
                    if name in {item.lower() for item in names}:
                        surface_files[surface].append(relative)
                        roles.append(surface)
                path_parts_lower = {part.lower() for part in Path(relative).parts}
                if "qvillage" in lowered or "qvs" in path_parts_lower or "qve" in path_parts_lower or "qvs" in Path(relative).stem.lower():
                    surface_paths["qvillage_qvs"].append(relative)
                    roles.append("qvillage_qvs")
                if ".github/instructions/" in lowered or name.endswith(".instructions.md"):
                    roles.append("instruction_policy")
                if suffix == ".md":
                    roles.append("markdown")
                if suffix in COMPONENT_SUFFIXES and any(token in lowered for token in ("component", "src/", "app/", "ui/", "frontend/")):
                    roles.append("component_source")
                    component_count += 1
                if any(token in lowered for token in ("/api/", "/apis/", "api_", "endpoint")):
                    roles.append("api_or_endpoint_source")
                    api_source_count += 1
                    if "endpoint" in lowered:
                        endpoint_source_count += 1
                if any(token in lowered for token in ("/route", "routes/", "_route.", "route_")):
                    roles.append("route_source")
                    route_source_count += 1
                if ".github/workflows/" in lowered or any(token in lowered for token in ("automation", "autodev", "workflow", "hook", "webhook")):
                    roles.append("automation_or_event_source")
                    automation_source_count += 1

                record: dict[str, Any] = {
                    "path": relative,
                    "scope": _source_scope(relative),
                    "suffix": suffix or "[no extension]",
                    "bytes": size,
                    "roles": sorted(set(roles)) or ["general_source"],
                    "sha256": None,
                    "status": "indexed",
                }
                if relative in AUDIT_SELF_REFERENTIAL_REPORTS:
                    record["bytes"] = None
                    record["status"] = "self_referential_excluded"
                    record["exclusion_reason"] = "audit_report_is_generated_from_this_inventory"
                    self_referential_exclusions.append(relative)
                    file_records.append(record)
                    all_file_records.append({"root": str(root), **record})
                    continue
                if suffix == ".md":
                    markdown_count += 1
                if size > AUDIT_MAX_FILE_BYTES:
                    record["status"] = "oversized_not_hashed"
                    skipped.append({"path": relative, "reason": "oversized_file_not_hashed", "bytes": size})
                    file_records.append(record)
                    all_file_records.append({"root": str(root), **record})
                    continue

                digest = hashlib.sha256()
                try:
                    with path.open("rb") as stream:
                        while chunk := stream.read(1024 * 1024):
                            digest.update(chunk)
                    record["sha256"] = digest.hexdigest()
                    content_digest.update(relative.encode("utf-8", errors="replace"))
                    content_digest.update(b"\0")
                    content_digest.update(record["sha256"].encode("ascii"))
                    content_digest.update(b"\n")
                except OSError as exc:
                    record["status"] = "unreadable"
                    unreadable.append({"path": relative, "error_type": type(exc).__name__})
                    file_records.append(record)
                    all_file_records.append({"root": str(root), **record})
                    continue

                if suffix == ".md":
                    if size > AUDIT_MAX_TEXT_BYTES:
                        record["markdown_validation"] = "oversized_content_not_parsed"
                        skipped.append({"path": relative, "reason": "oversized_markdown_not_parsed", "bytes": size})
                    else:
                        try:
                            text = path.read_text(encoding="utf-8")
                        except (OSError, UnicodeDecodeError) as exc:
                            record["markdown_validation"] = "unreadable_or_invalid_utf8"
                            unreadable.append({"path": relative, "error_type": type(exc).__name__})
                        else:
                            lines = text.splitlines()
                            words = re.findall(r"\b[\w'-]+\b", text, re.UNICODE)
                            document_families = _markdown_document_families(relative, text)
                            record["document_families"] = document_families
                            sentence_evidence = _markdown_sentence_evidence(text)
                            headings = sum(line.lstrip().startswith("#") for line in lines)
                            fence_count = sum(line.lstrip().startswith(("```", "~~~")) for line in lines)
                            unresolved = sorted(set(re.findall(r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b", text, re.IGNORECASE)))
                            missing_links = []
                            for line_number, line in enumerate(lines, 1):
                                for match in MARKDOWN_LINK_PATTERN.finditer(line):
                                    raw_target = match.group(1).strip().split(maxsplit=1)[0].strip("<>")
                                    parsed = urlsplit(raw_target)
                                    if parsed.scheme or parsed.netloc or not parsed.path:
                                        continue
                                    link_path = Path(parsed.path.split("?", 1)[0].split("#", 1)[0])
                                    resolved = (path.parent / link_path).resolve()
                                    if root not in resolved.parents and resolved != root:
                                        missing_links.append({"line": line_number, "target_sha256": hashlib.sha256(raw_target.encode("utf-8")).hexdigest(), "reason": "link_escapes_repository"})
                                        continue
                                    exists = resolved.is_file()
                                    if not exists:
                                        missing_links.append({"line": line_number, "target_sha256": hashlib.sha256(raw_target.encode("utf-8")).hexdigest(), "reason": "local_target_missing"})
                                    parsed_target = urlsplit(raw_target)
                                    if parsed_target.scheme.lower() in {"http", "https"} and parsed_target.hostname:
                                        safe_target = urlunsplit((parsed_target.scheme.lower(), parsed_target.hostname.lower(), parsed_target.path, "", ""))
                                    else:
                                        safe_target = parsed_target.path
                                    links.append({
                                        "source_path": relative,
                                        "line": line_number,
                                        "target": safe_target,
                                        "target_sha256": hashlib.sha256(raw_target.encode("utf-8")).hexdigest(),
                                        "target_kind": "external" if parsed_target.scheme else "local",
                                        "local_target_exists": exists if not parsed_target.scheme else None,
                                    })
                            metric_lines = []
                            instruction_lines = []
                            for line_number, line in enumerate(lines, 1):
                                if INSTRUCTION_CANDIDATE_PATTERN.search(line):
                                    instruction_lines.append(line_number)
                                terms = sorted(set(match.group(0).lower() for match in METRIC_TERM_PATTERN.finditer(line)))
                                percentages = [match.group(0).replace(" ", "") for match in PERCENT_PATTERN.finditer(line)]
                                if terms or percentages:
                                    metric_lines.append({"line": line_number, "metric_terms": terms, "percentages": percentages})
                                    if percentages:
                                        percentage_candidates.extend({"root": str(root), "path": relative, "line": line_number, "value": value} for value in percentages)
                                    if terms and CALCULATION_PATTERN.search(line):
                                        calculation_candidates.append({
                                            "root": str(root), "path": relative, "line": line_number,
                                            "metric_terms": terms,
                                            "operator_count": len(re.findall(r"=|\+|\*|/", line)),
                                            "sha256": record["sha256"],
                                            "source_text_recorded": False,
                                        })
                            all_metric_candidate_count += len(metric_lines)
                            if instruction_lines:
                                instruction_candidate_line_count += len(instruction_lines)
                                instruction_candidates.append({
                                    "root": str(root), "path": relative, "sha256": record["sha256"],
                                    "candidate_line_count": len(instruction_lines),
                                    "line_numbers": instruction_lines[:500],
                                    "line_numbers_truncated": len(instruction_lines) > 500,
                                    "status": "instruction_candidate_needs_semantic_mapping",
                                    "source_text_recorded": False,
                                })
                            comparison_rows = sum(line.lstrip().startswith("|") for line in lines)
                            review_reasons = []
                            if not text.strip():
                                review_reasons.append("empty_document")
                            if headings == 0:
                                review_reasons.append("missing_heading")
                            if fence_count % 2:
                                review_reasons.append("unbalanced_code_fences")
                            if unresolved:
                                review_reasons.append("unresolved_markers")
                            if missing_links:
                                review_reasons.append("invalid_or_missing_local_links")
                            markdown_record = {
                                "path": relative,
                                "scope": record["scope"],
                                "document_families": document_families,
                                "bytes": size,
                                "sha256": record["sha256"],
                                "line_count": len(lines),
                                "word_count": len(words),
                                "sentence_count_heuristic": sentence_evidence["sentence_count_heuristic"],
                                "sentence_records": sentence_evidence["sentence_records"],
                                "sentence_records_omitted_by_bound": sentence_evidence["sentence_records_omitted_by_bound"],
                                "duplicate_adjacent_word_candidate_count": sentence_evidence["duplicate_adjacent_word_candidate_count"],
                                "metric_claim_candidate_count": sentence_evidence["metric_claim_candidate_count"],
                                "completion_claim_candidate_count": sentence_evidence["completion_claim_candidate_count"],
                                "unreferenced_metric_claim_candidate_count": sentence_evidence["unreferenced_metric_claim_candidate_count"],
                                "unreferenced_completion_claim_candidate_count": sentence_evidence["unreferenced_completion_claim_candidate_count"],
                                "semantic_validation": "integrity_is_hash_checked; each sentence still requires source_and_owner_review",
                                "heading_count": headings,
                                "code_fence_count": fence_count,
                                "balanced_code_fences": fence_count % 2 == 0,
                                "unresolved_markers": unresolved,
                                "local_link_error_count": len(missing_links),
                                "local_link_errors": missing_links,
                                "comparison_table_row_count": comparison_rows if "compare" in name or "model_card" in name else 0,
                                "metric_candidate_line_count": len(metric_lines),
                                "metric_candidate_lines": metric_lines,
                                "status": "needs_review" if review_reasons else "structurally_validated",
                                "review_reasons": review_reasons,
                                "source_text_recorded": False,
                            }
                            markdown_records.append(markdown_record)
                            record["markdown_validation"] = markdown_record["status"]
                            record["line_count"] = len(lines)
                            record["word_count"] = len(words)
                            if name in {"compare.md", "qtrade.md", "tradingreadme.md"} or "model_card" in name:
                                metric_candidates.extend({"path": relative, **item} for item in metric_lines)
                elif suffix in AUDIT_METRIC_SUFFIXES:
                    if size > AUDIT_MAX_TEXT_BYTES:
                        skipped.append({"path": relative, "reason": "oversized_metric_source_not_parsed", "bytes": size})
                    else:
                        try:
                            text = path.read_text(encoding="utf-8")
                        except (OSError, UnicodeDecodeError) as exc:
                            unreadable.append({"path": relative, "error_type": type(exc).__name__})
                        else:
                            code_metric_lines = []
                            instruction_lines = []
                            for line_number, line in enumerate(text.splitlines(), 1):
                                if INSTRUCTION_CANDIDATE_PATTERN.search(line):
                                    instruction_lines.append(line_number)
                                terms = sorted(set(match.group(0).lower() for match in METRIC_TERM_PATTERN.finditer(line)))
                                percentages = [match.group(0).replace(" ", "") for match in PERCENT_PATTERN.finditer(line)]
                                if terms or percentages:
                                    code_metric_lines.append({"line": line_number, "metric_terms": terms, "percentages": percentages})
                                    if percentages:
                                        percentage_candidates.extend({"root": str(root), "path": relative, "line": line_number, "value": item} for item in percentages)
                                    if terms and CALCULATION_PATTERN.search(line):
                                        calculation_candidates.append({
                                            "root": str(root), "path": relative, "line": line_number,
                                            "metric_terms": terms,
                                            "operator_count": len(re.findall(r"=|\+|\*|/", line)),
                                            "sha256": record["sha256"],
                                            "source_text_recorded": False,
                                        })
                            record["metric_candidate_line_count"] = len(code_metric_lines)
                            all_metric_candidate_count += len(code_metric_lines)
                            if instruction_lines:
                                instruction_candidate_line_count += len(instruction_lines)
                                instruction_candidates.append({
                                    "root": str(root), "path": relative, "sha256": record["sha256"],
                                    "candidate_line_count": len(instruction_lines),
                                    "line_numbers": instruction_lines[:500],
                                    "line_numbers_truncated": len(instruction_lines) > 500,
                                    "status": "instruction_candidate_needs_semantic_mapping",
                                    "source_text_recorded": False,
                                })
                            if code_metric_lines and any(token in lowered for token in ("compare", "qtrade", "trading", "benchmark", "metric")):
                                metric_candidates.extend({"path": relative, **item} for item in code_metric_lines)

                file_records.append(record)
                all_file_records.append({"root": str(root), **record})

        for directory in sorted(directories):
            all_directories.append({"root": str(root), "path": directory, "file_count_in_subtree": directory_counts.get(directory, 0)})

        required_documents = {
            name: {
                "expected_basenames": list(basenames),
                "found_paths": sorted(
                    record["path"]
                    for record in file_records
                    if Path(record["path"]).name.lower() in {item.lower() for item in basenames}
                ),
                "status": "present" if any(
                    Path(item["path"]).name.lower() in {name.lower() for name in basenames}
                    for item in file_records
                ) else "missing",
            }
            for name, basenames in SURFACE_DOCUMENTS.items()
        }
        try:
            refs = subprocess.run(
                ["git", "-C", str(root), "for-each-ref", "--format=%(refname)"],
                capture_output=True,
                text=True,
                check=True,
                timeout=20,
            ).stdout.splitlines()
            commit_count = int(subprocess.run(
                ["git", "-C", str(root), "rev-list", "--all", "--count"],
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            ).stdout.strip())
            local_head_sha = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True,
                timeout=20,
            ).stdout.strip()
            local_tree_sha = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD^{tree}"],
                capture_output=True,
                text=True,
                check=True,
                timeout=20,
            ).stdout.strip()
            local_branch_result = subprocess.run(
                ["git", "-C", str(root), "symbolic-ref", "--quiet", "--short", "HEAD"],
                capture_output=True,
                text=True,
                check=False,
                timeout=20,
            )
            local_branch = local_branch_result.stdout.strip() if local_branch_result.returncode == 0 else None
            git_status = "enumerated_local_refs_and_commits"
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired, ValueError):
            refs = []
            commit_count = None
            local_head_sha = None
            local_tree_sha = None
            local_branch = None
            git_status = "unavailable"

        root_report = {
            "root": str(root),
            "exists": True,
            "file_count": file_count,
            "directory_count": len(directories),
            "total_bytes": byte_count,
            "markdown_file_count": markdown_count,
            "component_source_count": component_count,
            "api_or_endpoint_source_count": api_source_count,
            "endpoint_named_source_count": endpoint_source_count,
            "route_source_count": route_source_count,
            "automation_or_event_source_count": automation_source_count,
            "file_type_counts": dict(sorted(suffix_counts.items())),
            "surface_documents": required_documents,
            "surface_paths": {name: sorted(set(paths)) for name, paths in surface_paths.items() if paths},
            "document_family_paths": {
                family: sorted(
                    item["path"]
                    for item in markdown_records
                    if family in item.get("document_families", [])
                )
                for family in MARKDOWN_DOCUMENT_FAMILY_PATTERNS
            },
            "markdown_records": markdown_records,
            "directories": sorted(directories),
            "git_history": {
                "status": git_status,
                "ref_count": len(refs),
                "refs": sorted(refs),
                "commit_count": commit_count,
                "local_ref": f"refs/heads/{local_branch}" if local_branch else "HEAD",
                "local_branch": local_branch,
                "local_head_sha": local_head_sha,
                "local_tree_sha": local_tree_sha,
                "intermediate_commit_trees_scanned": False,
                "remote_completeness": "not_verified",
            },
            "unreadable": unreadable,
            "skipped": skipped,
            "self_referential_exclusions": self_referential_exclusions,
            "self_referential_exclusion_policy": sorted(AUDIT_SELF_REFERENTIAL_REPORTS),
            "content_digest": content_digest.hexdigest(),
            "source_contents_recorded": False,
            "semantic_requirements_understood": False,
            "scan_duration_seconds": round(time.monotonic() - root_started, 3),
        }
        root_reports.append(root_report)

    manifest = json.dumps(
        {
            "files": all_file_records,
            "directories": all_directories,
            "self_referential_exclusion_policy": sorted(AUDIT_SELF_REFERENTIAL_REPORTS),
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    invalid_markdown = sum(
        item["status"] != "structurally_validated"
        for report in root_reports
        for item in report.get("markdown_records", [])
    )
    markdown_records = [
        item
        for report in root_reports
        for item in report.get("markdown_records", [])
    ]
    unreadable_count = sum(len(report.get("unreadable", [])) for report in root_reports)
    skipped_count = sum(len(report.get("skipped", [])) for report in root_reports)
    surface_counts: dict[str, int] = {}
    for name in SURFACE_DOCUMENTS:
        surface_counts[name] = sum(
            len(report.get("surface_documents", {}).get(name, {}).get("found_paths", []))
            for report in root_reports
        )
    surface_counts["qvillage_qvs"] = sum(
        len(report.get("surface_paths", {}).get("qvillage_qvs", []))
        for report in root_reports
    )
    document_family_paths = {
        family: sorted({
            path
            for report in root_reports
            for path in report.get("document_family_paths", {}).get(family, [])
        })
        for family in MARKDOWN_DOCUMENT_FAMILY_PATTERNS
    }
    percentage_values_by_path: dict[tuple[str, str], list[float]] = {}
    for item in percentage_candidates:
        try:
            value = float(item["value"].replace("%", ""))
        except (TypeError, ValueError):
            continue
        percentage_values_by_path.setdefault((item["root"], item["path"]), []).append(value)
    percentage_summary_by_path = [
        {
            "root": root,
            "path": path,
            "count": len(values),
            "minimum": min(values),
            "maximum": max(values),
            "mean": round(sum(values) / len(values), 4),
            "interpretation": "descriptive_unclassified_percentages_not_comparable_performance_proof",
        }
        for (root, path), values in sorted(percentage_values_by_path.items())
    ]
    return {
        "schema_version": 4,
        "generated_at": utc_now(),
        "scan_duration_seconds": round(time.monotonic() - audit_started, 3),
        "status": "NEEDS_REVIEW" if unavailable_roots or invalid_markdown or unreadable_count or skipped_count else "MATERIALIZED_AUDIT_COMPLETE_REMOTE_HISTORY_INCOMPLETE",
        "scope": "materialized repository roots and local refs only",
        "roots": root_reports,
        "file_count": len(all_file_records),
        "directory_count": len(all_directories),
        "markdown_file_count": sum(report.get("markdown_file_count", 0) for report in root_reports),
        "surface_document_counts": surface_counts,
        "document_family_counts": {
            family: len(paths) for family, paths in document_family_paths.items()
        },
        "document_family_paths": document_family_paths,
        "component_source_count": sum(report.get("component_source_count", 0) for report in root_reports),
        "api_or_endpoint_source_count": sum(report.get("api_or_endpoint_source_count", 0) for report in root_reports),
        "route_source_count": sum(report.get("route_source_count", 0) for report in root_reports),
        "automation_or_event_source_count": sum(report.get("automation_or_event_source_count", 0) for report in root_reports),
        "markdown_structurally_validated_count": sum(item["status"] == "structurally_validated" for report in root_reports for item in report.get("markdown_records", [])),
        "markdown_needs_review_count": invalid_markdown,
        "markdown_word_count": sum(item.get("word_count", 0) for item in markdown_records),
        "markdown_sentence_count_heuristic": sum(item.get("sentence_count_heuristic", 0) for item in markdown_records),
        "markdown_sentence_records_indexed": sum(len(item.get("sentence_records", [])) for item in markdown_records),
        "markdown_sentence_records_omitted_by_bound": sum(item.get("sentence_records_omitted_by_bound", 0) for item in markdown_records),
        "markdown_duplicate_adjacent_word_candidate_count": sum(item.get("duplicate_adjacent_word_candidate_count", 0) for item in markdown_records),
        "markdown_metric_claim_candidate_count": sum(item.get("metric_claim_candidate_count", 0) for item in markdown_records),
        "markdown_completion_claim_candidate_count": sum(item.get("completion_claim_candidate_count", 0) for item in markdown_records),
        "markdown_unreferenced_metric_claim_candidate_count": sum(item.get("unreferenced_metric_claim_candidate_count", 0) for item in markdown_records),
        "markdown_unreferenced_completion_claim_candidate_count": sum(item.get("unreferenced_completion_claim_candidate_count", 0) for item in markdown_records),
        "metric_candidate_line_count": all_metric_candidate_count,
        "instruction_candidate_line_count": instruction_candidate_line_count,
        "instruction_candidate_file_count": len(instruction_candidates),
        "instruction_candidates": instruction_candidates,
        "percentage_occurrence_count": len(percentage_candidates),
        "percentage_candidates": percentage_candidates,
        "percentage_summary_by_path": percentage_summary_by_path,
        "calculation_candidate_line_count": len(calculation_candidates),
        "calculation_candidates": calculation_candidates,
        "comparison_and_qtrade_metric_candidates": metric_candidates,
        "link_reference_count": len(links),
        "links": links,
        "all_file_records": all_file_records,
        "all_directory_records": all_directories,
        "unavailable_roots": unavailable_roots,
        "self_referential_exclusions": sorted({path for report in root_reports for path in report.get("self_referential_exclusions", [])}),
        "unreadable_file_count": unreadable_count,
        "skipped_source_count": skipped_count,
        "source_manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "remote_refs_prs_and_intermediate_trees_verified": False,
        "semantic_validation": "structure, UTF-8, local links, metrics, and hashes are machine-checked; semantic correctness of each sentence requires mapped source/tests and is not inferred",
        "production_replacement_policy": "candidate discovery only; implementation, owner, security, focused tests, rollback, and remote evidence are required before replacement",
        "source_text_recorded": False,
        "self_referential_exclusion_policy": sorted(AUDIT_SELF_REFERENTIAL_REPORTS),
        "research_domains": sorted(audit_domains),
        "research_topics": sorted(audit_topics),
        "next_actions": [
            "resolve missing, unreadable, oversized, or structurally invalid materialized sources",
            "map each requirement to implementation, tests, workflow hooks, owning docs, and exact SHA",
            "obtain target-owned all-ref, PR, and intermediate-tree manifests for both repositories",
            "review production candidates individually before implementation or replacement",
        ],
    }


def write_markdown_sentence_audit(
    root: Path | str,
    report: dict[str, Any],
    *,
    correlation_id: str | None = None,
) -> dict[str, Any]:
    """Persist bounded sentence/word integrity metadata without copying Markdown prose."""
    target = Path(root).resolve()
    artifact_path = target / MARKDOWN_SENTENCE_AUDIT_JSONL
    manifest_path = target / MARKDOWN_SENTENCE_AUDIT_MANIFEST
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    run_id = correlation_id or str(uuid.uuid4())
    markdown_records = [
        (str(root_report.get("root", "")), item)
        for root_report in report.get("roots", [])
        for item in root_report.get("markdown_records", [])
    ]
    local_git_context = [
        {
            "root": str(root_report.get("root", "")),
            "repository": Path(str(root_report.get("root", target))).name,
            "ref": root_report.get("git_history", {}).get("local_ref", "UNKNOWN"),
            "head_sha": root_report.get("git_history", {}).get("local_head_sha"),
            "tree_sha": root_report.get("git_history", {}).get("local_tree_sha"),
            "verification_level": "local_git_observation_only",
            "remote_verified": False,
        }
        for root_report in report.get("roots", [])
    ]
    totals = {
        "scan_duration_seconds": float(report.get("scan_duration_seconds", 0.0)),
        "markdown_file_count": len(markdown_records),
        "sentence_count_heuristic": sum(
            int(item.get("sentence_count_heuristic", 0)) for _, item in markdown_records
        ),
        "sentence_records_indexed": sum(
            len(item.get("sentence_records", [])) for _, item in markdown_records
        ),
        "sentence_records_omitted_by_bound": sum(
            int(item.get("sentence_records_omitted_by_bound", 0))
            for _, item in markdown_records
        ),
        "word_count": sum(int(item.get("word_count", 0)) for _, item in markdown_records),
        "metric_claim_candidate_count": sum(
            int(item.get("metric_claim_candidate_count", 0))
            for _, item in markdown_records
        ),
        "completion_claim_candidate_count": sum(
            int(item.get("completion_claim_candidate_count", 0))
            for _, item in markdown_records
        ),
        "unreferenced_metric_claim_candidate_count": sum(
            int(item.get("unreferenced_metric_claim_candidate_count", 0))
            for _, item in markdown_records
        ),
        "unreferenced_completion_claim_candidate_count": sum(
            int(item.get("unreferenced_completion_claim_candidate_count", 0))
            for _, item in markdown_records
        ),
    }

    def write_jsonl_record(stream: gzip.GzipFile, value: dict[str, Any]) -> None:
        stream.write(
            json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
            + b"\n"
        )

    fd, temporary_name = tempfile.mkstemp(
        prefix=".qaudit-markdown-sentences-",
        suffix=".jsonl.gz.tmp",
        dir=artifact_path.parent,
    )
    try:
        with os.fdopen(fd, "wb") as raw_stream:
            with gzip.GzipFile(fileobj=raw_stream, mode="wb", mtime=0) as compressed:
                write_jsonl_record(compressed, {
                    "record_type": "manifest",
                    "schema_version": 4,
                    "generated_at": report.get("generated_at"),
                    "scan_duration_seconds": report.get("scan_duration_seconds"),
                    "correlation_id": run_id,
                    "repository": target.name,
                    "scope": report.get("scope", "materialized_repository"),
                    "status": report.get("status", "UNKNOWN"),
                    "source_manifest_sha256": report.get("source_manifest_sha256"),
                    "self_referential_exclusion_policy": report.get(
                        "self_referential_exclusion_policy",
                        sorted(AUDIT_SELF_REFERENTIAL_REPORTS),
                    ),
                    "source_text_recorded": False,
                    "local_git_context": local_git_context,
                    "remote_verified": False,
                    **totals,
                })
                for source_root, item in sorted(
                    markdown_records,
                    key=lambda entry: (entry[0], str(entry[1].get("path", ""))),
                ):
                    path = str(item.get("path", ""))
                    write_jsonl_record(compressed, {
                        "record_type": "document",
                        "root": source_root,
                        "path": path,
                        "scope": item.get("scope"),
                        "document_families": item.get("document_families", []),
                        "bytes": item.get("bytes"),
                        "sha256": item.get("sha256"),
                        "line_count": item.get("line_count"),
                        "word_count": item.get("word_count"),
                        "sentence_count_heuristic": item.get("sentence_count_heuristic"),
                        "sentence_records_omitted_by_bound": item.get("sentence_records_omitted_by_bound"),
                        "status": item.get("status"),
                        "review_reasons": item.get("review_reasons", []),
                        "local_link_error_count": item.get("local_link_error_count", 0),
                        "semantic_validation": item.get("semantic_validation"),
                        "source_text_recorded": False,
                    })
                    for sentence in item.get("sentence_records", []):
                        write_jsonl_record(compressed, {
                            "record_type": "sentence",
                            "root": source_root,
                            "path": path,
                            **{
                                field: sentence[field]
                                for field in (
                                    "sentence_index",
                                    "line_start",
                                    "line_end",
                                    "word_count",
                                    "sentence_sha256",
                                    "word_sequence_sha256",
                                    "duplicate_adjacent_word_candidate",
                                    "metric_claim_candidate",
                                    "completion_claim_candidate",
                                    "reference_marker_present",
                                    "semantic_status",
                                )
                                if field in sentence
                            },
                            "source_text_recorded": False,
                        })
            raw_stream.flush()
            os.fsync(raw_stream.fileno())
        digest = hashlib.sha256()
        compressed_bytes = 0
        with Path(temporary_name).open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
                compressed_bytes += len(chunk)
        os.replace(temporary_name, artifact_path)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)

    blockers = []
    if report.get("status") != "MATERIALIZED_AUDIT_COMPLETE_REMOTE_HISTORY_INCOMPLETE":
        blockers.append(f"surface_audit_status:{report.get('status', 'UNKNOWN')}")
    if report.get("unreadable_file_count", 0):
        blockers.append(f"unreadable_files:{report['unreadable_file_count']}")
    if report.get("skipped_source_count", 0):
        blockers.append(f"skipped_sources:{report['skipped_source_count']}")
    if totals["sentence_records_omitted_by_bound"]:
        blockers.append(
            f"sentence_records_omitted_by_bound:{totals['sentence_records_omitted_by_bound']}"
        )
    blockers.append("remote_refs_prs_intermediate_trees_and_release_state_not_verified")
    metadata = {
        "schema_version": 4,
        "correlation_id": run_id,
        "generated_at": report.get("generated_at"),
        "repository": target.name,
        "source_scope": report.get("scope", "materialized_repository"),
        "status": report.get("status", "UNKNOWN"),
        "source_manifest_sha256": report.get("source_manifest_sha256"),
        "self_referential_exclusions": report.get("self_referential_exclusions", []),
        "self_referential_exclusion_policy": report.get(
            "self_referential_exclusion_policy",
            sorted(AUDIT_SELF_REFERENTIAL_REPORTS),
        ),
        "local_git_context": local_git_context,
        "artifact_path": artifact_path.relative_to(target).as_posix(),
        "artifact_sha256": digest.hexdigest(),
        "artifact_bytes": compressed_bytes,
        "record_format": "gzip-compressed-jsonl; manifest, document, then sentence records",
        "source_text_recorded": False,
        "remote_verified": False,
        "totals": totals,
        "unreadable_file_count": report.get("unreadable_file_count", 0),
        "skipped_source_count": report.get("skipped_source_count", 0),
        "blockers": blockers,
    }
    fd, metadata_temporary = tempfile.mkstemp(
        prefix=".qaudit-markdown-manifest-",
        suffix=".json.tmp",
        dir=manifest_path.parent,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(metadata, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(metadata_temporary, manifest_path)
    finally:
        if os.path.exists(metadata_temporary):
            os.unlink(metadata_temporary)
    return metadata


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
