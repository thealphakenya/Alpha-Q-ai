# QMOI Language Inventory and Engineering Use

## Status and scope

`scripts/language_strategy.py` provides a deterministic, advisory language
catalog and task-fit selector. QAUDITS adds a language label to every scanned
path and reports per-language path counts under the same source-manifest hash.
The current catalog is a maintained set of 26 profiles, not a claim to contain
every language in existence. New or ambiguous extensions remain
`unclassified` until reviewed.

The inventory is local materialized-tree evidence only. It does not certify
that a language, toolchain, runtime, dependency, or release is installed,
supported, secure, performant, or remotely deployed. Release versions and
support lifecycles must be fetched from official project sources and recorded
with source URL, observation time, and content hash before use in a decision.

## Language profiles

| Language | Useful strengths | Tradeoffs and engineering safeguards |
| --- | --- | --- |
| C | Portable low-level control and embedded reach | Manual memory and bounds safety require sanitizers, static analysis, and review |
| C++ | Performance-sensitive native systems and extensive libraries | Complex language surface; enforce ownership rules, sanitizers, and dependency review |
| C# | Productive .NET services, desktop, and cross-platform applications | Runtime/framework choices affect footprint and portability |
| Dart | Flutter-based shared application UI | Native integrations and platform-specific behavior need separate tests |
| Elixir | Fault-tolerant concurrent services | Smaller ecosystem and maintainer pool than mainstream alternatives |
| Go | Network services, concurrency, and simple deployment | Garbage-collection tradeoffs and less expressive abstraction model |
| Haskell | Strong type system and functional modeling of invariants | Steeper learning curve and smaller production maintainer pool |
| Java | Mature JVM services and broad enterprise support | Runtime footprint and framework complexity need operational controls |
| JavaScript | Ubiquitous web runtime and broad ecosystem | Dynamic typing and dependency supply-chain exposure need runtime validation |
| Julia | Numerical and scientific computing | Smaller general-purpose deployment and library ecosystem |
| Kotlin | Android development and JVM interoperability | Build/runtime choices can affect startup and interoperability |
| Lua | Small embedded runtime and application scripting | Dynamic typing and narrower ecosystem need explicit contracts |
| Objective-C | Interoperability with established Apple code | Apple-specific scope and mixed-language boundaries add maintenance cost |
| PHP | Broad web hosting and mature web application ecosystem | Runtime/legacy diversity requires strict input and dependency controls |
| Perl | Text processing and established automation | Newer-system maintenance and dependency choices need scrutiny |
| PowerShell | Windows administration and cross-platform automation | Host/version differences require compatibility tests |
| Python | Automation, data/ML, and rapid service development | Profile performance; use typing, tests, and runtime input validation |
| R | Statistics, research workflows, and visualization | General-service deployment often needs supporting components |
| Ruby | Productive web development and scripting | Dynamic typing and runtime costs need tests and dependency controls |
| Rust | Memory-safe systems code without garbage collection | Learning/build complexity; memory safety does not prevent logic flaws |
| Scala | JVM interoperability and typed data/distributed processing | Language and framework complexity can increase build/onboarding cost |
| Shell | Small orchestration tasks close to the operating system | Quoting, portability, and injection risks make it unsuitable for large apps |
| SQL | Relational querying, constraints, and data transformation | Dialect, privileges, migrations, and query plans need database-specific tests |
| Swift | Native Apple development with static typing | Apple SDK and deployment-target availability constrain portability |
| TypeScript | Typed web and Node.js applications | Types are erased; runtime validation and dependency security remain necessary |
| Zig | Explicit systems control and compile-time capabilities | Younger ecosystem; pin toolchains and validate compatibility |

## Selection and composition

Use `recommend_languages(task_domains, available_languages=...)` for
deterministic candidate ranking. It returns the inputs, unknown domains, ranked
fit candidates, and an explicit `migration_recommended: false`. It is guidance,
not a build-system or authorization decision.

Prefer the smallest set of languages that meets the product boundary:

- Rust, C, C++, Go, or Zig may be evaluated for constrained systems components;
  choose based on measured safety, latency, deployment, and maintenance needs.
- Python is a strong fit for automation, data science, and many ML integrations.
- TypeScript/JavaScript suit web interfaces and Node.js services; validate
  untrusted inputs at runtime.
- Kotlin and Swift fit native Android and Apple interfaces respectively.
- Dart is an option when Flutter's shared UI and platform support meet
  requirements.
- SQL owns relational queries and constraints, with schema migrations reviewed
  as code.
- Shell and PowerShell are for bounded operational glue; complex application
  logic should use a typed, testable runtime.

An application may combine languages through documented APIs, subprocess
contracts, generated bindings, or reviewed FFI. Every boundary must define
input/output schemas, authentication, errors, timeouts, resource limits,
compatibility, and focused integration tests. Do not introduce another
language solely because a generalized profile ranks it higher.

## Twenty cross-language engineering checks

Every language-specific recommendation and implementation review should record
applicability and evidence for these twenty dimensions:

1. Security threat model and trust boundaries.
2. Memory and resource safety.
3. Authentication and authorization.
4. Input validation and output encoding.
5. Dependency provenance and vulnerability handling.
6. Secret-safe logs and telemetry.
7. Privacy, retention, and data minimization.
8. Performance baselines and measured bottlenecks.
9. Reliability, failure isolation, and bounded retries.
10. Health checks, observability, and freshness.
11. Concurrency and race-safety tests.
12. API/schema and cross-language compatibility.
13. Accessibility and localization for user-facing surfaces.
14. Portability across declared target platforms.
15. Build reproducibility and toolchain pinning.
16. Unit, integration, and negative-path test coverage.
17. Static analysis, formatting, and type-check outcomes.
18. Upgrade, deprecation, and rollback strategy.
19. Ownership, maintainability, and operational runbooks.
20. Exact-ref/SHA validation and separately recorded remote evidence.

These checks are acceptance dimensions, not twenty completed features or a
weighted score. Mark non-applicable items with a reason; unknown or missing
evidence stays unresolved.

## Measurement contract

QAUDITS reports the count of scanned paths by language, unclassified paths,
catalog size, source scope, scanner version, source-manifest SHA-256, and scan
duration. Counts are path counts (not lines, packages, or implementation
coverage); multi-language files are counted once by extension. Ambiguous
extensions and generated/vendor paths follow the scanner's explicit
classification/exclusion rules. The report does not claim all-world language
coverage or current release research.
