# API.md - QMOI Unified API Reference

## Overview
This document is the canonical API index for the QMOI ecosystem across the qmoi-enhanced and Alpha-Q-ai repositories. It consolidates the operational interfaces, automation hooks, and repository synchronization contracts used by the autonomous agent.

## API Categories

### 1. Repository Management APIs
- GET /repo/status
- GET /repo/structure
- GET /repo/inventory
- GET /repo/history
- POST /repo/sync
- POST /repo/validate
- POST /repo/resume
- POST /repo/normalize

### 2. GitHub Integration APIs
- GET /github/token
- GET /github/branch-status
- GET /github/proof-contract
- GET /github/workflows
- GET /github/history
- POST /github/trigger-workflow
- POST /github/create-pr
- POST /github/dispatch
- POST /github/sync-branch

### 3. Agent Runtime APIs
- POST /agent/validate-all
- POST /agent/validate-platforms
- POST /agent/validate-features
- POST /agent/auto-heal
- POST /agent/checkpoint
- POST /agent/recover
- GET /agent/health
- GET /agent/summary

### 4. Sync & Recovery APIs
- POST /sync/alpha-q-ai
- POST /sync/backups
- POST /sync/merge
- POST /sync/reconcile-docs
- POST /sync/reconcile-history
- POST /recover/files
- POST /recover/yaml
- POST /recover/python
- POST /recover/history

### 5. File Inventory APIs
- GET /files/index
- GET /files/markdown
- GET /files/repo-tree
- GET /files/archives
- POST /files/scan-all
- POST /files/normalize

### 6. Historical & Clone Coverage APIs
- GET /history/qmoi-enhanced
- GET /history/alpha-q-ai
- GET /history/all-repos
- GET /history/branches
- GET /history/refs
- GET /history/clones

## Ollama autonomous agent merge and documentation contract

The Ollama autonomous agent must reconcile the following files before it marks a merge or automation pass as complete:

- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [STYLES.md](STYLES.md)
- [UNIVERSALS.md](UNIVERSALS.md)
- [ENDPOINTS.md](ENDPOINTS.md)
- [ROUTES.md](ROUTES.md)
- [ALLPORTS.md](ALLPORTS.md)
- [qmoi-enhanced-history-14/ALLMDFILESREFS.md](qmoi-enhanced-history-14/ALLMDFILESREFS.md)
- [qmoi-enhanced-history-14/STYLES.md](qmoi-enhanced-history-14/STYLES.md)
- [qmoi-enhanced-history-14/UNIVERSALS.md](qmoi-enhanced-history-14/UNIVERSALS.md)

The agent must use the processed API inventory, endpoint registry, route map, and port map to ensure that every automation, workflow, and merge operation matches the real system behavior. When the archive contains a missing feature or a recovered pattern, the agent merges it into the live repo only after validating the source-of-truth and preserving security, identity, and UI consistency.

## Core Contracts

### PR Validation Contract
The agent exposes a GitHub proof contract that validates:
- platform build checks
- feature validation matrix
- file-handler validation
- branch sync readiness
- markdown and inventory coverage
- history snapshot coverage
- memory-index generation

### Auto-Healing Contract
The resilience coordinator can repair:
- missing files
- corrupted files
- invalid YAML
- invalid Python syntax
- degraded runtime states
- missing API, route, and port inventory entries
- stale historical references

### Repository Inventory Contract
This system must maintain authoritative inventory records for:
- QMOI main repo
- Alpha-Q-ai repo
- qmoi-enhanced-history-14 archive
- all reachable refs and branches
- all Markdown, API, route, endpoint, and port docs
- all clone and backup histories

## Notes
This file is intentionally kept as the canonical interface and inventory index for the automation, sync layers, and historical repository audit process.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10428`; directories: `1268`; Markdown: `2416`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2109, orchestration=2061, qteam_accountability=2049, release_tag_publish=2088, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2221`; needs review: `187`; metric candidate lines: `52705`; percentage occurrences: `22237`.
- Markdown word count: `3550281`; heuristic sentence count: `673664`; sentence records indexed: `673664`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29834` metric claims; `10658` completion claims; `29737` metric and `10529` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13328`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `39967` lines in `3666` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `286`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
