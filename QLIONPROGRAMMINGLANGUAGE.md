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
