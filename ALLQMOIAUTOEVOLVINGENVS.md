# QMOI Auto-Evolving Environments

## Purpose and current execution path

This document describes the active checkout's evidence-led feature discovery
and evolution-planning path. The existing
[`scripts/ollama_autonomous_agent.py`](scripts/ollama_autonomous_agent.py)
invokes the feature audit during `audit-inventory`; the focused
`qaudit-all-features` command refreshes the feature artifacts without running
the broader inventory. Both are local QAUDITS operations, not autonomous
permission to modify applications, branches, releases, accounts, or external
services.

The operating sequence is:

1. Inventory the canonical platform/app feature registry and local source
   files.
2. Collect explicitly declared Markdown `Feature:`/`Capability:` entries and
   named entries in structured JSON memory feature collections.
3. Deduplicate candidates and retain source path, SHA-256, line or JSON
   pointer, source family, and active/historical/archive scope.
4. Publish the candidates as `DISCOVERED_REVIEW_REQUIRED`; keep implementation
   and remote verification false.
5. Require an owner, intended behavior, access boundary, focused positive and
   negative tests, security/privacy review, rollback plan, and required
   authorization before implementation or promotion.
6. Measure actual implementation, test, workflow, UI/monitor, and remote
   evidence separately. A plan, source mention, or local test is not a
   production or remote-completion result.

## Candidate sources and feature domains

The feature audit reads the materialized local tree. Markdown discovery uses
explicit declaration lines rather than treating every heading, sentence, or
research idea as a feature. JSON memory discovery is limited to structured
`features`, `capabilities`, `feature_memory`, and `feature_candidates`
collections; parsing is bounded to 1 MiB, depth 8, and 10,000 visited nodes.
Oversized, malformed, or bounded-out memory sources are warnings, not empty
or successful evidence. Surrounding Markdown prose and memory descriptions
are not copied into candidate artifacts.

Source-family metrics classify discoveries across memory/recovery, research,
skills, projects, finance, styles/universals, parallel/orchestration,
QMOIMasks, QVS, QCity/QVillage, evolution, creativity, and app/platform
documentation. Source-family and source-scope counts can overlap and are not
unique implementation totals. Historical and archived candidates remain
separately marked; they do not become active capabilities by being remembered.

The feature and documentation handoff is shared across:

- [QAUDITS.md](QAUDITS.md) and the generated
  [ALLFEATURES.md](ALLFEATURES.md) catalog.
- The active [ALLLANGUAGES.md](ALLLANGUAGES.md) language inventory and
  [QVILLAGE.md](QVILLAGE.md) research/evolution handoff.
- [Qvillageevolutions.md](Qvillageevolutions.md) for QVillage evolution plans
  and [QCITY.md](QCITY.md) for project/platform coordination.
- The deterministic
  [`scripts/qaudits_evolution_planner.py`](scripts/qaudits_evolution_planner.py)
  contract plan, which inventories these sources without declaring them
  complete.

The active checkout does not contain `QENGINEER.md`. The
[QVIRTUALLABS.md](QVIRTUALLABS.md) source-reconciliation gate remains blocked
until its authoritative requirements are supplied and mapped; historical
snapshots and ambiguous public lookup failures are not substitutes.

## Metrics and artifacts

The machine-readable
[`feature_manifest.json`](ollamatracks/qaudits_all_features/feature_manifest.json)
records the registry and candidate totals, evidence counts, source-family,
source-kind, and source-scope counts, and memory scan warnings. Its per-feature
records distinguish registered features from review-only candidates and keep
implementation and remote verification separate. The paired
[`feature_evidence.json`](ollamatracks/qaudits_all_features/feature_evidence.json)
retains local shard/path provenance, and `ALLFEATURES.md` renders the catalog
for review.

The `audit-inventory` result and checkpoint carry these feature counts and
local artifact hashes alongside the independent memory, finance, style and
universal, accessibility, test/hook, project, and repository-surface
inventories. Do not add overlapping category counts into a single denominator.
The current manifest is a local snapshot; its counts must be refreshed by the
documented command before being quoted as current.

Feature and source counts are not model-quality scores. Research measurements
must separately record source URL, retrieval time, content hash, collector,
freshness, and result status. The existing inventory plans external research
without fetching it by default; live scheduled research, model inference,
controlled experiments, comparative benchmarks, and verified evolution
cycles remain `NOT_MEASURED` until their execution evidence exists.

## Master access, UI, and financial boundaries

`ALLFEATURES.md`, the feature manifest, and
[`ALLTRACKS.md`](ALLTRACKS.md) provide local review and monitoring-mapping
artifacts. They are not an authenticated interactive master dashboard. No
master-only UI/API mapping or live per-feature monitoring is established by
these artifacts; UI ownership, authorization, design-token/universal
accessibility mapping, data freshness, and focused tests must be verified
before exposing a dashboard.

Finance-related feature candidates are inventory labels only. They do not
provision a bank, wallet, exchange, or provider account; verify balances;
initiate payments or transfers; or establish realtime financial monitoring.
Those capabilities require provider/owner authorization, least-privilege
integration, reconciliation, security and legal review, tests, and explicit
remote evidence.

## Safe operation

Run the focused local feature inventory with:

```text
python scripts/ollama_autonomous_agent.py qaudit-all-features
```

Run the broader paired QAUDITS inventory only through its documented
`audit-inventory` path. It refreshes additional generated catalogs and evidence
and must retain its own correlation ID, source scope, hashes, omissions,
blockers, and next action. Do not rewrite every related Markdown file or
historical snapshot to make candidate counts appear complete.

Every generated result remains local evidence with
`remote_verification_complete=false`. Remote workflows, protected branches,
releases, deployments, credential changes, and financial operations continue
to require their separate authority and exact-repository/ref/SHA evidence.
