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
