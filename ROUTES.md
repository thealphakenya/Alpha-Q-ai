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

- Status: `NEEDS_REVIEW`; materialized files: `11301`; directories: `1291`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2177, build_download_install=2131, disability_accessibility=288, orchestration=2082, qteam_accountability=2071, release_tag_publish=2110, tree_inventory=2022`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2230`; needs review: `202`; metric candidate lines: `53187`; percentage occurrences: `22274`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13561`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `41058` lines in `3748` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `340`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
