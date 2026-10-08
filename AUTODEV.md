# AUTODEV.md - Autonomous Development Framework

## Overview
This document formalizes how the QMOI automation stack should behave while operating autonomously across repositories and validation workflows.

## Autonomous Capabilities
- read and apply instructions from repo docs
- monitor workflow health
- repair broken scripts and YAML
- self-resume after interruption
- validate app and platform matrix
- maintain documentation inventory
- synchronize repo state across branches and repos

## Execution Model
1. Detect repository state
2. Validate core contracts
3. Repair missing or corrupted files
4. Run validation suite
5. Record checkpoints
6. Update docs and progress markers
7. Push or prepare PR state when appropriate

## Success Criteria
The autonomous development process is considered successful when:
- tests pass
- doc inventory is complete
- workflows are valid
- recovery logic remains active
- repo state remains accessible and consistent

## QAUDITS and lifecycle gates

Before a stage advances, retain its exact source/ref/hash scope, QAUDITS metric snapshot, test/hook evidence, skipped-source list, blockers, and resumable next action. The local `qaudit-universe` command is read-only with respect to remote state and cannot satisfy remote lifecycle gates. Large scans should use deterministic, bounded parallel batches for independent reads; publish only complete atomic artifacts, and serialize lifecycle/checkpoint mutations. See [QAUDITS.md](QAUDITS.md), [QVERSIONMANAGER.md](QVERSIONMANAGER.md), and [TRANSION.md](TRANSION.md) for the full metric and stage contract.

Checkpoint undo/redo selects a prior orchestration state only. It does not undo project files or remote side effects; use the scoped recovery tiers in [undoredo.md](undoredo.md).

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
