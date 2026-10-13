"""Evidence-first language inventory and task-fit recommendations for QAUDITS."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Iterable


LANGUAGE_PROFILES: dict[str, dict[str, object]] = {
    "C": {
        "extensions": (".c",),
        "strengths": "Portable low-level control, predictable layout, broad embedded support.",
        "tradeoffs": "Manual memory and bounds discipline; safety depends heavily on tooling and review.",
        "domains": ("embedded", "systems"),
    },
    "C++": {
        "extensions": (".cc", ".cpp", ".cxx", ".hh", ".hpp", ".hxx"),
        "strengths": "High-performance systems, mature native libraries, and fine-grained control.",
        "tradeoffs": "Large language surface and memory/concurrency hazards require strict tooling.",
        "domains": ("performance", "systems", "embedded"),
    },
    "C#": {
        "extensions": (".cs",),
        "strengths": "Productive .NET services, desktop applications, and mature tooling.",
        "tradeoffs": "Runtime and framework choices affect deployment size and portability.",
        "domains": ("backend", "desktop", "cross_platform"),
    },
    "Dart": {
        "extensions": (".dart",),
        "strengths": "Flutter enables a shared mobile, desktop, and web UI codebase.",
        "tradeoffs": "Native integrations and platform-specific behavior still need separate validation.",
        "domains": ("mobile", "cross_platform", "frontend"),
    },
    "Elixir": {
        "extensions": (".ex", ".exs"),
        "strengths": "Fault-tolerant concurrent services and resilient distributed applications.",
        "tradeoffs": "Smaller hiring pool and ecosystem than mainstream general-purpose languages.",
        "domains": ("distributed", "backend"),
    },
    "Go": {
        "extensions": (".go",),
        "strengths": "Simple deployment, strong concurrency primitives, and efficient network services.",
        "tradeoffs": "Garbage collection and a deliberately smaller abstraction ecosystem.",
        "domains": ("backend", "distributed", "performance", "security"),
    },
    "Haskell": {
        "extensions": (".hs", ".lhs"),
        "strengths": "Strong types and functional abstractions help express complex invariants.",
        "tradeoffs": "Steeper learning curve and a smaller pool of production maintainers.",
        "domains": ("correctness", "data"),
    },
    "Java": {
        "extensions": (".java",),
        "strengths": "Mature JVM ecosystem, static typing, and broad enterprise support.",
        "tradeoffs": "Runtime footprint and framework complexity need operational planning.",
        "domains": ("backend", "distributed", "android"),
    },
    "JavaScript": {
        "extensions": (".js", ".jsx", ".mjs", ".cjs"),
        "strengths": "Ubiquitous web runtime and broad frontend/backend package ecosystems.",
        "tradeoffs": "Dynamic typing and dependency supply-chain risks require added controls.",
        "domains": ("frontend", "backend", "cross_platform"),
    },
    "Julia": {
        "extensions": (".jl",),
        "strengths": "Numerical and scientific computing with a high-level workflow.",
        "tradeoffs": "Smaller general-purpose deployment and library ecosystem.",
        "domains": ("data", "performance"),
    },
    "Kotlin": {
        "extensions": (".kt", ".kts"),
        "strengths": "Concise JVM development and first-class Android support.",
        "tradeoffs": "Platform and build-tool choices can affect startup and interoperability.",
        "domains": ("android", "backend", "cross_platform"),
    },
    "Lua": {
        "extensions": (".lua",),
        "strengths": "Small embeddable runtime and convenient application scripting.",
        "tradeoffs": "Dynamic typing and a narrower standard ecosystem require explicit contracts.",
        "domains": ("embedded", "automation"),
    },
    "Objective-C": {
        "extensions": (".m", ".mm"),
        "strengths": "Interoperability with established Apple platform code.",
        "tradeoffs": "New Apple development generally favors Swift; mixed-language boundaries add cost.",
        "domains": ("apple", "mobile"),
    },
    "PHP": {
        "extensions": (".php", ".phtml"),
        "strengths": "Mature web hosting ecosystem and broad application deployment support.",
        "tradeoffs": "Legacy/runtime diversity and dynamic behavior require strict dependency and input controls.",
        "domains": ("backend", "web"),
    },
    "Perl": {
        "extensions": (".pl", ".pm"),
        "strengths": "Established text processing and system automation capabilities.",
        "tradeoffs": "Maintenance and dependency choices can be difficult in newer systems.",
        "domains": ("automation", "data"),
    },
    "PowerShell": {
        "extensions": (".ps1", ".psm1", ".psd1"),
        "strengths": "Structured administration across Windows and supported cross-platform hosts.",
        "tradeoffs": "Shell version and platform differences need explicit compatibility tests.",
        "domains": ("automation", "windows"),
    },
    "Python": {
        "extensions": (".py", ".pyi"),
        "strengths": "Automation, data/ML ecosystems, and rapid service and tooling development.",
        "tradeoffs": "Runtime performance and dynamic typing need profiling and static/test safeguards.",
        "domains": ("automation", "data", "ml", "backend"),
    },
    "R": {
        "extensions": (".r", ".R"),
        "strengths": "Statistical analysis, research workflows, and visualization.",
        "tradeoffs": "General service deployment and concurrency often need supporting components.",
        "domains": ("data", "statistics"),
    },
    "Ruby": {
        "extensions": (".rb", ".rake"),
        "strengths": "Expressive web development and productive scripting.",
        "tradeoffs": "Dynamic typing and runtime costs require tests and dependency controls.",
        "domains": ("web", "automation", "backend"),
    },
    "Rust": {
        "extensions": (".rs",),
        "strengths": "Memory safety without a garbage collector and strong systems-level control.",
        "tradeoffs": "Steeper learning curve and compile-time complexity; safe memory does not prevent logic flaws.",
        "domains": ("security", "systems", "performance", "embedded"),
    },
    "Scala": {
        "extensions": (".scala", ".sc"),
        "strengths": "JVM interoperability and expressive typed data/distributed processing.",
        "tradeoffs": "Language and framework complexity can increase onboarding and build costs.",
        "domains": ("data", "distributed", "backend"),
    },
    "Shell": {
        "extensions": (".sh", ".bash", ".zsh"),
        "strengths": "Portable orchestration and small glue tasks close to the operating system.",
        "tradeoffs": "Quoting, error handling, portability, and injection risks make it unsuitable for large applications.",
        "domains": ("automation",),
    },
    "SQL": {
        "extensions": (".sql",),
        "strengths": "Declarative relational queries, constraints, and data transformations.",
        "tradeoffs": "Dialect, migration, privilege, and query-plan differences need database-specific tests.",
        "domains": ("database", "data"),
    },
    "Swift": {
        "extensions": (".swift",),
        "strengths": "Modern native Apple application development with static typing.",
        "tradeoffs": "Apple platform focus and SDK availability constrain deployment targets.",
        "domains": ("apple", "mobile"),
    },
    "TypeScript": {
        "extensions": (".ts", ".tsx", ".mts", ".cts"),
        "strengths": "Typed web/client and Node.js development with broad ecosystem support.",
        "tradeoffs": "Types are erased at runtime; runtime validation and dependency security remain necessary.",
        "domains": ("frontend", "backend", "cross_platform"),
    },
    "Zig": {
        "extensions": (".zig",),
        "strengths": "Explicit low-level control and compile-time capabilities for systems work.",
        "tradeoffs": "Younger ecosystem and evolving tooling require version pinning and careful review.",
        "domains": ("systems", "performance", "embedded"),
    },
}

_EXTENSION_TO_LANGUAGE: dict[str, str] = {}
for _language_name, _profile in LANGUAGE_PROFILES.items():
    _extensions = _profile["extensions"]
    if isinstance(_extensions, tuple):
        for _extension in _extensions:
            _EXTENSION_TO_LANGUAGE[_extension.lower()] = _language_name
_EXTENSION_TO_LANGUAGE[".h"] = "C/C++"

_DOMAIN_PREFERENCES: dict[str, tuple[str, ...]] = {
    "android": ("Kotlin", "Java"),
    "apple": ("Swift", "Objective-C"),
    "automation": ("Python", "PowerShell", "Shell", "Go"),
    "backend": ("Go", "Python", "TypeScript", "Java", "C#"),
    "cross_platform": ("TypeScript", "Dart", "Kotlin", "C#"),
    "data": ("Python", "SQL", "R", "Julia", "Scala"),
    "database": ("SQL",),
    "distributed": ("Go", "Elixir", "Java", "Scala", "Rust"),
    "embedded": ("Rust", "C", "C++", "Zig"),
    "frontend": ("TypeScript", "JavaScript", "Dart"),
    "ml": ("Python",),
    "performance": ("Rust", "C++", "Go", "Julia", "Zig"),
    "security": ("Rust", "Go", "Python"),
    "statistics": ("R", "Python", "Julia"),
    "systems": ("Rust", "C", "C++", "Go", "Zig"),
    "web": ("TypeScript", "JavaScript", "PHP", "Ruby", "Python"),
    "windows": ("PowerShell", "C#"),
    "correctness": ("Haskell", "Rust", "Kotlin"),
}


def classify_language(path: str | Path) -> str:
    """Return a conservative language label, retaining unknown extensions as unknown."""
    return _EXTENSION_TO_LANGUAGE.get(Path(path).suffix.lower(), "unclassified")


def aggregate_language_counts(paths: Iterable[str | Path]) -> dict[str, int]:
    """Count every supplied source path exactly once by detected language."""
    return dict(sorted(Counter(classify_language(path) for path in paths).items()))


def recommend_languages(
    task_domains: Iterable[str],
    *,
    available_languages: Iterable[str] = (),
) -> dict[str, object]:
    """Rank task-fit candidates; existing-language preference never authorizes migration."""
    domains = sorted({domain.strip().lower() for domain in task_domains if domain.strip()})
    available = {language.strip() for language in available_languages if language.strip()}
    scores: Counter[str] = Counter()
    matched_domains: dict[str, list[str]] = {}
    unknown_domains = []

    for domain in domains:
        preferences = _DOMAIN_PREFERENCES.get(domain)
        if preferences is None:
            unknown_domains.append(domain)
            continue
        for rank, language in enumerate(preferences):
            scores[language] += max(1, len(preferences) - rank)
            matched_domains.setdefault(language, []).append(domain)

    ranked = sorted(
        scores,
        key=lambda language: (-scores[language], language not in available, language),
    )
    recommendations = [
        {
            "language": language,
            "fit_score": scores[language],
            "matched_domains": sorted(set(matched_domains[language])),
            "already_present": language in available,
        }
        for language in ranked
    ]
    return {
        "task_domains": domains,
        "unknown_task_domains": unknown_domains,
        "recommendations": recommendations,
        "migration_recommended": False,
        "decision_basis": "deterministic_task_fit_advisory",
        "remote_research_verified": False,
        "release_versions_verified": False,
    }


def language_inventory(paths: Iterable[str | Path]) -> dict[str, object]:
    """Build count-only inventory metadata without reading or retaining source text."""
    materialized = [Path(path).as_posix() for path in paths]
    counts = aggregate_language_counts(materialized)
    return {
        "status": "CANDIDATE_DISCOVERY_ONLY",
        "scope": "caller_supplied_materialized_paths",
        "file_count": len(materialized),
        "language_counts": counts,
        "unclassified_file_count": counts.get("unclassified", 0),
        "catalog_language_count": len(LANGUAGE_PROFILES),
        "catalog_coverage_complete_for_all_languages": False,
        "remote_research_verified": False,
        "release_versions_verified": False,
    }
