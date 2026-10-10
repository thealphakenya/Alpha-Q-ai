# ALLROUTES.md - Complete QMOI Route Inventory

## Scope
This document is the canonical route inventory for the QMOI automation stack, covering the main repository, historical snapshots, Alpha-Q-ai sync targets, GitHub Actions workflows, and repository-management operations.

## Route Groups

### Public Documentation Routes
- /README
- /BUILD
- /INSTALL
- /DOWNLOAD
- /MONITORING
- /SYNC
- /MERGE
- /API
- /ENDPOINTS
- /ROUTES
- /ALLPORTS
- /ALLMDFILESREFS
- /MODELEVOLUTIONO
- /WORKFLOWS
- /WORKFLOWSO

### Operational Application Routes
- /ai
- /space
- /files
- /ide
- /help/faq
- /status
- /health
- /ready
- /metrics
- /version

### Repository Management Routes
- /repo/status
- /repo/structure
- /repo/inventory
- /repo/history
- /repo/validate
- /repo/resume
- /repo/normalize
- /repo/checkpoint

### GitHub & Workflow Routes
- /github/token
- /github/branch-status
- /github/proof-contract
- /github/workflows
- /github/history
- /github/trigger-workflow
- /github/create-pr
- /github/dispatch
- /github/sync-branch

### Agent & Recovery Routes
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
- /agent/auto-heal

### File Inventory Routes
- /files/index
- /files/markdown
- /files/repo-tree
- /files/archive-scan
- /files/scan-all
- /files/normalize

### Historical / Snapshot Routes
- /history/all-repos
- /history/qmoi-enhanced
- /history/alpha-q-ai
- /history/qmoi-enhanced-history-14
- /history/branches
- /history/refs
- /history/clones
- /history/snapshots

### Sync and Merge Routes
- /sync/qmoi-enhanced
- /sync/alpha-q-ai
- /sync/backup
- /sync/reconcile
- /sync/reconcile-history
- /sync/merge
- /sync/monitor

## Historical Coverage
All route families above are expected to be reflected in the following canonical docs:
- API.md
- ENDPOINTS.md
- ROUTES.md
- ALLPORTS.md
- ALLMDFILESREFS.md
- MERGE.md
- SYNC.md
- WORKFLOWS.md
- MONITORING_INDEX.md
- QMOI_REALTIME_MEMORY_INDEX.md
- qmoi-enhanced-history-14 archived snapshots

## Implementation Notes
These routes are contract-level guideposts for the autonomous agent, repository synchronization, and GitHub-hosted validation stack. They must remain aligned with the live automation layer, workflow metadata, and historical inventory snapshots.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10603`; directories: `1280`; Markdown: `2421`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2157, build_download_install=2113, disability_accessibility=268, orchestration=2065, qteam_accountability=2053, release_tag_publish=2092, tree_inventory=2004`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2226`; needs review: `187`; metric candidate lines: `52756`; percentage occurrences: `22237`.
- Markdown word count: `3562982`; heuristic sentence count: `674722`; sentence records indexed: `674722`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29846` metric claims; `10693` completion claims; `29749` metric and `10564` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9053` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13376`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40146` lines in `3689` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `299`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
