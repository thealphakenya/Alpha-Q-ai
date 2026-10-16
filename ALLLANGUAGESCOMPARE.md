# Programming Language Comparison for QMOI

## Interpretation

This is a qualitative engineering comparison, not a benchmark or security
ranking. Use project-specific threat models, test results, maintainer capacity,
deployment constraints, and measured performance before selecting a language.
Read the profile details and QAUDITS scope in [ALLLANGUAGES.md](./ALLLANGUAGES.md).

| Language | Strong fits | Main costs or risks | Official release-source topic |
| --- | --- | --- | --- |
| C | Embedded, native systems | Manual memory and bounds safety | `language-c-release` |
| C++ | Native performance, systems | Complexity, memory/concurrency hazards | `language-cpp-release` |
| C# | .NET services, desktop | Runtime and framework footprint | `language-csharp-release` |
| Dart | Flutter applications | Native integration and platform variance | `language-dart-release` |
| Elixir | Fault-tolerant concurrency | Smaller ecosystem and hiring pool | `language-elixir-release` |
| Go | APIs, distributed services | Garbage collection, smaller abstraction surface | `language-go-release` |
| Haskell | Invariant-heavy functional systems | Learning curve and maintainer availability | `language-haskell-release` |
| Java | JVM services, enterprise | Runtime footprint and framework complexity | `language-java-release` |
| JavaScript | Web and Node.js | Dynamic types and package supply chain | `language-javascript-release` |
| Julia | Scientific/numerical computing | General-purpose deployment ecosystem | `language-julia-release` |
| Kotlin | Android, JVM | Build/runtime complexity | `language-kotlin-release` |
| Lua | Embedded scripting | Dynamic contracts and narrower ecosystem | `language-lua-release` |
| Objective-C | Existing Apple code | Apple scope and mixed-language maintenance | `language-objective-c-release` |
| PHP | Web hosting and applications | Runtime/legacy variability | `language-php-release` |
| Perl | Text processing, automation | New-system maintenance ecosystem | `language-perl-release` |
| PowerShell | Windows administration | Host and version differences | `language-powershell-release` |
| Python | Automation, data, ML | Runtime performance and dynamic typing | `language-python-release` |
| R | Statistical analysis | General-service operations | `language-r-release` |
| Ruby | Web applications and scripts | Runtime costs and dynamic typing | `language-ruby-release` |
| Rust | Systems and memory-safety-sensitive components | Learning/build complexity; logic bugs remain possible | `language-rust-release` |
| Scala | JVM data/distributed workloads | Language and framework complexity | `language-scala-release` |
| Shell | Small orchestration tasks | Quoting, portability, injection exposure | `language-shell-release` |
| SQL | Relational data operations | Dialect, privilege, migration, and query-plan risks | `language-sql-release` |
| Swift | Native Apple applications | Apple SDK and platform scope | `language-swift-release` |
| TypeScript | Web UI and Node.js services | Runtime types are not enforced after compilation | `language-typescript-release` |
| Zig | Low-level systems | Younger ecosystem and evolving tooling | `language-zig-release` |

## Decision method

1. Define task domains and constraints: security, latency, memory, platform,
   integration, deployment, maintenance, and team skills.
2. Generate candidate languages with
   `scripts.language_strategy.recommend_languages`; unknown domains are
   reported rather than guessed.
3. Prefer a suitable language already in the codebase unless measured
   requirements demonstrate a material benefit from change.
4. Prototype only the bounded critical path and compare identical workloads.
   Record environment, source revision, input, warm-up, repeats, variance,
   correctness, resource use, and test outcomes.
5. Review dependency lifecycle, threat model, operability, and rollback before
   adopting the result.
6. Store external release/support observations with official source URL,
   retrieval time, observed version, and content hash in QVillage research
   evidence. Expired or inaccessible observations are `UNKNOWN`, not current.

Rust's ownership and type system can reduce classes of memory-safety defects;
it is not proof of application security. No language is universally safest or
fastest. Benchmark results are only comparable when workloads and environments
match.

The topic IDs resolve to allowlisted official-source candidates through
`scripts.ollama_research.build_language_research_plan()`. That function
creates a plan only: current versions, support status, and retrieval time are
intentionally blank until an authorized, bounded fetch is actually performed.
For SQL, the registered source is a database dialect's release page, not the
SQL standard itself.

## Automation state

- Local selection engine: `IMPLEMENTED` as deterministic advisory logic.
- QAUDITS language counts: `IMPLEMENTED` for recognized extensions in the
  materialized path inventory; unknown extensions remain visible.
- Official release-version refresh and continuous QVillage research:
  `NOT_IMPLEMENTED`; no current release claims are made here.
- Automatic language migration or file renaming: `DISABLED`; recommendations
  do not authorize code changes.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `11182`; directories: `1288`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2177, build_download_install=2131, disability_accessibility=288, orchestration=2082, qteam_accountability=2071, release_tag_publish=2110, tree_inventory=2022`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2230`; needs review: `202`; metric candidate lines: `53160`; percentage occurrences: `22268`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13537`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `41035` lines in `3741` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `333`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: qaudit-language-inventory -->
## QAUDITS language-inventory observation

- Generated at: `2026-10-16T17:21:35.554481Z`; source-manifest SHA-256: `05d646de7978656bb04da692ae36a07478506edc8126c8259d0f182daa46f685`; scope: `materialized_local_only`.
- Scanned paths by language: `{"JavaScript": 761, "PowerShell": 24, "Python": 1654, "Rust": 4, "SQL": 2, "Shell": 134, "TypeScript": 2236, "unclassified": 6336}`.
- Unclassified paths: `6336`; maintained profiles: `26`; all-language coverage complete: `False`.
- Official release research verified: `False`; QVillage external research verified: `False`.
- Official language release research plan: `{"external_fetch_performed": false, "observed_release_versions": 0, "official_sources_planned": 26, "plan_artifact": "ollamatracks/language_research_plan.json", "plan_status": "PLANNED_NOT_VISITED", "source_not_registered_count": 0}`; current versions remain unknown until sources are fetched and reviewed.
- Counts are local path candidates only. Unknown, excluded, historical, and remote scopes remain explicit; language recommendations do not authorize migration.
<!-- END QMOI MANAGED: qaudit-language-inventory -->
