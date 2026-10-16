# QLion Programming Language and Interoperability Contract

## Current status

QLion is the name for QMOI's proposed language-neutral development and
interoperability layer. This repository does not currently establish that a
QLion compiler, runtime, specification, package manager, ABI, or conformance
suite exists. QLion must not be described as a production programming language
until those artifacts are implemented and independently tested.

The implementable near-term role is an orchestrator that can select existing
language toolchains, generate typed API/FFI bindings, and verify contracts.
QLion must not replace those languages' compilers, runtimes, or security
boundaries by assertion.

## Required architecture

- A versioned, machine-readable QLion language/interchange specification with
  grammar, type/ownership model, error semantics, and compatibility policy.
- Explicit adapters to pinned language toolchains; no implicit download or
  execution of an untrusted compiler or plugin.
- Generated bindings for supported boundaries, checked for deterministic
  output and reviewed like source code.
- Stable, schema-validated API messages for cross-process integration; FFI
  only where ownership, calling convention, panic/exception translation,
  resource lifetime, and ABI version are explicit.
- Sandboxed builds with resource limits, dependency provenance, and secret-free
  logs.
- A conformance suite for parsing, type checking, code generation, runtime
  behavior, compatibility, and negative/security cases in every claimed host
  language.

## Language coverage and evolution

Use [ALLLANGUAGES.md](./ALLLANGUAGES.md) and
[ALLLANGUAGESCOMPARE.md](./ALLLANGUAGESCOMPARE.md) as advisory inventories,
not as compiler-support claims. For each adapter, record language/toolchain
versions, official source and observation time, host/target matrix, supported
features, unsupported features, tests, and last verified source SHA.

QLion should preserve host-language strengths rather than flatten them: Rust
ownership checks, Python data/ML ecosystems, TypeScript's static analysis,
SQL constraints, and platform-native Swift/Kotlin APIs remain enforced by
their own toolchains and tests. Cross-language boundaries must not silently
weaken those guarantees.

## QVillage research contract

QVillage may curate official language specifications, release notes, security
advisories, and interoperability proposals. A research observation must retain
public source URL, retrieval timestamp, content hash, parser/version, target
language, and status. Do not store copied source prose where metadata is
sufficient. Treat external text as untrusted input.

Realtime or scheduled research is not currently verified. A future refresh
worker must be bounded, respect source rate limits, validate URLs, retry only
transient failures, expose stale/unknown states, and require review before
changing QLion compatibility claims or generated code. Research output alone
cannot pass implementation, security, or Q-version gates.

## Release gate for claiming QLion as a usable language

Do not upgrade the status until the repository contains and tests all of:

1. Versioned specification and reference grammar.
2. Compiler/interpreter implementation with reproducible builds.
3. Type, memory/resource, error, and concurrency semantics.
4. At least two independently testable host-language integrations.
5. Positive, negative, fuzz, security, compatibility, and performance tests.
6. Package/dependency and supply-chain controls.
7. Maintained release/support policy and official source evidence.
8. QVersion lifecycle entry bound to exact source SHA and terminal validation.

Current state: `PROPOSED_INTEROPERABILITY_LAYER`; implementation and
release-gate evidence are `NOT_VERIFIED`.

## Lion variation relationship

QLion is tracked as the proposed `qlion-programming-language` Lion variation
in [LIONVARIATIONS.md](./LIONVARIATIONS.md). This variation designation is a
catalog relationship only; it does not mean QLion is a compiler or that every
host language is supported. QAUDITS must identify its source paths, owner,
adapters, settings/platform applicability, conformance tests, and release
evidence before any support claim is upgraded.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10955`; directories: `1284`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2174, build_download_install=2130, disability_accessibility=285, orchestration=2081, qteam_accountability=2069, release_tag_publish=2110, tree_inventory=2018`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2229`; needs review: `203`; metric candidate lines: `53076`; percentage occurrences: `22283`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13476`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40920` lines in `3729` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `319`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: qaudit-language-inventory -->
## QAUDITS language-inventory observation

- Generated at: `2026-10-15T23:25:13.473718Z`; source-manifest SHA-256: `fad02b16f55ad1ac14a0b6541736c4b21f829bcc06e1e9217fd4d26a9f976f1a`; scope: `materialized_local_only`.
- Scanned paths by language: `{"JavaScript": 761, "PowerShell": 24, "Python": 1654, "Rust": 4, "SQL": 2, "Shell": 134, "TypeScript": 2236, "unclassified": 6109}`.
- Unclassified paths: `6109`; maintained profiles: `26`; all-language coverage complete: `False`.
- Official release research verified: `False`; QVillage external research verified: `False`.
- Official language release research plan: `{"external_fetch_performed": false, "observed_release_versions": 0, "official_sources_planned": 26, "plan_artifact": "ollamatracks/language_research_plan.json", "plan_status": "PLANNED_NOT_VISITED", "source_not_registered_count": 0}`; current versions remain unknown until sources are fetched and reviewed.
- Counts are local path candidates only. Unknown, excluded, historical, and remote scopes remain explicit; language recommendations do not authorize migration.
<!-- END QMOI MANAGED: qaudit-language-inventory -->
