# ALLAUTO.md - QMOI Automation Overview
abc
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

### Evidence-first QAUDITS and Q-version automation

- Run the local, non-finalizing inventory with `python scripts/ollama_autonomous_agent.py qaudit-universe --base-path <repository-root>`. It refreshes the QAUDITS universe and style/universal candidate tree without remote writes.
- Use [QAUDITS.md](QAUDITS.md) for denominators, categories, quality/security/finance/delivery metrics, evidence states, and fail-closed thresholds; use [QVERSIONMANAGER.md](QVERSIONMANAGER.md) for the ordered 28-stage lifecycle and remote finalization gates.
- Treat candidate discovery, test mapping, test pass, hook review, local verification, and remote exact-SHA verification as separate states. Do not infer success from totals or percentages.
- Parallelize only independent read-only shards with deterministic bounds and bounded memory; serialize checkpoint, lifecycle-ledger, merge, and publication writes. A missing/overlapping shard, timeout, stale cache, or unavailable source blocks the affected gate.
- Lifecycle checkpoint undo/redo is state-only and is governed by [undoredo.md](undoredo.md); it does not revert files, history, branches, deployments, or financial effects.

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

- Status: `NEEDS_REVIEW`; materialized files: `10446`; directories: `1270`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2156, build_download_install=2110, orchestration=2062, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2001`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52718`; percentage occurrences: `22237`.
- Markdown word count: `3554796`; heuristic sentence count: `674081`; sentence records indexed: `674081`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29838` metric claims; `10664` completion claims; `29741` metric and `10535` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9047` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13342`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40052` lines in `3673` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `290`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: restore-point-memory-sync -->
## Restore-point memory and branch continuity

- Evidence status: `BLOCKED_MISSING_EVIDENCE`; source status: `UNKNOWN`.
- Workspace SHA: `unknown`; tree SHA: `unknown`; master verified: `False`.
- Source evidence: `QMOItracks/qmoi_restore_point_preflight.json`; SHA-256: `unavailable`; workflow run: `unknown`.
- Ref roles: `main` is the default branch, `autosync-backup` is the staging ref, `master` is the validated-main parity mirror, and `qmoi` is the post-success restore point.
- These records are last-observed metadata, not proof that a remote worker is live; stale, missing, partial, or unverified refs remain visible as blocked/review-required.

- Current blocker: No restore-point preflight artifact is available in this checkout.
<!-- END QMOI MANAGED: restore-point-memory-sync -->
