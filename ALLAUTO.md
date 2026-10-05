# ALLAUTO.md - QMOI Automation Overview

## Purpose
This file lists the automation capabilities that keep the QMOI repositories self-maintaining, self-validating, and resilient.

## Automation Domains

### Repository Automation
- branch sync
- backup sync
- repository health checks
- validation on PR
- workflow monitoring
- issue and PR trigger management

### Agent Automation
- full validation suite
- platform validation
- feature validation
- auto-healing
- missing-file reconstruction
- syntax repair for Python and YAML
- checkpoint resume
- refresh QStore app catalog and cross-platform UI requirements
- preserve and refresh the managed QStream integration contract
- maintain source-repository app links in APP_LINKS.md and VERCELLINKS.md
- report catalog coverage separately from code validation of external app repositories

### Recovery Automation
- missing file detection
- corruption detection
- YAML repair
- Python repair
- graceful degradation
- degraded-mode execution

## Governance
All automation is expected to remain self-hosted, GitHub-driven, and resilient to partial file-loss or syntax issues without requiring manual intervention.

## Complete Repository And History Coverage

Every merge or synchronization run must inventory both
`thealphakenya/qmoi-enhanced` and `thealphakenya/Alpha-Q-ai`, every reachable
local and remote branch, and the complete tracked tree. The historical ref
`origin/codespace-potential-space-happiness-wrv69x5j6qjq2g7wp` is mandatory
input, not an optional backup. Its contents are also materialized in
`qmoi-enhanced-history-14/` and must be considered for missing files,
directories, implementations, and documentation.

The agent must classify every path as `QE`, `AQ`, `BOTH`, `HISTORICAL`, or
`CONFLICT`, including unused paths and every `.md` file. Missing paths are
reconciled only after dependency, ownership, security, and feature-degradation
checks. A conflict or uncertain ownership blocks automatic mutation and creates
a review record; it must never be silently discarded.

The required sequence is: discover repositories and refs, snapshot commits and
trees, inventory markdown and non-markdown paths, classify ownership, build a
merge plan, create a recoverable checkpoint, apply only authorized changes,
validate syntax/tests/links, compare the complete post-merge tree, update
`MERGE.md` and `ALLMDFILESREFS.md`, and publish telemetry. Merge success requires
evidence for both repositories and the historical source; a partial-file result
is insufficient.

<!-- BEGIN QMOI MANAGED: remote-continuity-and-failover -->
## Agent-managed remote continuity and failover contract

A target-owned workflow can run independently of a Codespace, but it is not independent of its workflow-host provider. Do not claim uninterrupted execution without a separately deployed, authorized worker and a verified failover test.

- Persist execution IDs, source refs/SHAs, idempotent requests, checkpoints, leases, and audit events outside the workspace; resume only after re-reading authoritative state.
- Heartbeat freshness, worker identity, queue age, lock ownership, and provider reachability are separate health signals. Missing/stale telemetry means `STALE` or `OFFLINE`, never `RUNNING`.
- Provider failover requires pre-authorized credentials, least-privilege access, tested data consistency, and a terminal failover exercise. Never silently switch trading venues or move funds when a provider is unavailable.
- On stale market/account data, lost authorization, provider outage, queue duplication, or ledger mismatch, stop new trading orders and preserve read-only monitoring where available.
- External-worker deployment, availability, and disaster recovery remain `not_verified` until exact-host evidence exists.
<!-- END QMOI MANAGED: remote-continuity-and-failover -->

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10408`; directories: `1267`; Markdown: `2412`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Markdown structural checks passed: `2186`; needs review: `218`; metric candidate lines: `46823`; percentage occurrences: `22236`.
- Formula/calculation candidate lines: `11364`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `36263` lines in `3090` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `285`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
