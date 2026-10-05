# ENDPOINTS.md - Consolidated Endpoint Map

## Purpose
This document lists the endpoint families used by the QMOI system and the repository automation stack.

## Endpoint Inventory

The Ollama autonomous agent must treat the following operational endpoints as part of the merge and automation contract:

- /agent/merge-history
- /agent/reconcile-markdown
- /agent/scan-archive
- /agent/validate-ui-styles
- /agent/validate-user-auth
- /agent/sync-documentation
- /agent/validate-routes
- /agent/validate-ports
- /agent/validate-history

These endpoints ensure that merge activity, markdown inventory validation, UI styling checks, route and port validation, and historical archive reconciliation are all part of the same operational process. The agent should always verify against the active repo first and then compare against [qmoi-enhanced-history-14](qmoi-enhanced-history-14) for missing or recovered implementation logic.

### Core System
- /health
- /status
- /ready
- /metrics
- /version
- /repo/inventory
- /repo/history
- /repo/structure

### GitHub / PR
- /github/pull-requests
- /github/workflows
- /github/branches
- /github/trigger
- /github/validate
- /github/proof-contract
- /github/dispatch
- /github/trigger-workflow

### Sync & Repo Ops
- /sync/branches
- /sync/main
- /sync/backup
- /sync/reconcile
- /sync/monitor
- /sync/reconcile-history
- /sync/qmoi-enhanced
- /sync/alpha-q-ai
- /sync/merge

### Agent & Automation
- /agent/run
- /agent/validate
- /agent/validate-all
- /agent/validate-platforms
- /agent/validate-features
- /agent/repair
- /agent/recover
- /agent/checkpoint
- /agent/health
- /agent/summary

### Model & Evolution
- /model/evolution
- /model/stages
- /model/countdown
- /model/status
- /model/files
- /model/memory

### File and History Inventory
- /files/index
- /files/markdown
- /files/repo-tree
- /files/archive-scan
- /history/all-repos
- /history/branches
- /history/refs
- /history/clones

### Historical / Clone Coverage
- /history/qmoi-enhanced
- /history/alpha-q-ai
- /history/qmoi-enhanced-history-14
- /history/archives
- /history/snapshots

## Notes
This document is the canonical operational endpoint registry for the repository and its historical snapshots, and it must remain aligned with the live automation, GitHub dispatchers, and cross-repo agent implementation.

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
