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

- Status: `NEEDS_REVIEW`; materialized files: `10435`; directories: `1269`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2110, orchestration=2061, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52722`; percentage occurrences: `22237`.
- Markdown word count: `3552546`; heuristic sentence count: `673863`; sentence records indexed: `673863`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29844` metric claims; `10662` completion claims; `29747` metric and `10533` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13340`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40017` lines in `3670` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `287`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
