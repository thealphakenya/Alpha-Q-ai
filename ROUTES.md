# ROUTES.md - Route Map for QMOI Automation

## Route Overview
This file defines the main route families that connect the repository automation, GitHub workflows, and autonomous validation layers.

## Route Families

### Ollama autonomous agent and merge routes
- /agent/merge-history
- /agent/reconcile-markdown
- /agent/scan-archive
- /agent/validate-ui-styles
- /agent/validate-user-auth
- /agent/sync-documentation
- /agent/validate-routes
- /agent/validate-ports
- /agent/validate-history

### Public Routes
- /README
- /BUILD
- /INSTALL
- /DOWNLOAD
- /MONITORING
- /SYNC
- /MERGE
- /MODELEVOLUTIONO
- /API
- /ENDPOINTS
- /ROUTES
- /ALLPORTS
- /ALLMDFILESREFS

### Operational Routes
- /agent/validate-all
- /agent/validate-platforms
- /agent/validate-features
- /agent/auto-heal
- /agent/checkpoint
- /agent/recover
- /agent/summary
- /repo/status
- /repo/structure
- /repo/inventory
- /repo/history

### Sync Routes
- /sync/qmoi-enhanced
- /sync/alpha-q-ai
- /sync/backup
- /sync/reconcile
- /sync/reconcile-history
- /sync/monitor
- /sync/merge

### PR & Workflow Routes
- /pr/contract
- /pr/validate
- /pr/summary
- /workflow/run
- /workflow/monitor
- /workflow/dispatch
- /workflow/verify

### File and History Routes
- /files/index
- /files/markdown
- /files/archive-scan
- /history/all-repos
- /history/qmoi-enhanced
- /history/alpha-q-ai
- /history/qmoi-enhanced-history-14
- /history/branches
- /history/refs

## Implementation Notes
Routes are represented as contract-level guideposts and should remain consistent with GitHub Action triggers, branch sync goals, repository inventory logic, historical repo snapshots, and the autonomous orchestration layer.

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
