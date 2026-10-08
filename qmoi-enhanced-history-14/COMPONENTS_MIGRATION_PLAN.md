# COMPONENTS_MIGRATION_PLAN.md

- OWNER: Ollama autonomous agent
- GENERATED: Please do not manually remove; agent will own execution and updates.

## Migration Tasks

TASK: Move all contents from `components/` into `src/components/` preserving subdirectories and file timestamps.
TASK: Update import paths across the repo to reference `src/components/` instead of `components/` (TS/JS/TSX/JSX imports and absolute paths).
TASK: Update `COMPONENTS.md`, `UNIVERSALS.md`, `STYLES.md`, and `TREE.md` to reference the new `src/components/` locations.
TASK: Append detailed migration actions and completion checkpoints to `resumefromhere.txt` as JOURNEY MAP TRACKS entries; the Ollama agent will own these entries.
TASK: Refresh `API.md`, `ENDPOINTS.md`, `ROUTES.md`, and `ALLPORTS.md` to reflect any changes caused by component moves.
TASK: Produce per-directory merge reports under `MERGE_REPORTS/` for backend, frontend, scripts, and components after merging archives.
TASK: Ensure `ALLBACKEND.md` and `ALLFRONTEND.md` are rebuilt and committed after migration.
TASK: Merge implementations from backup/archive directories into canonical files where appropriate and record decisions in `MERGE_REPORTS/`.
TASK: Run repository verification and collect results; if failures occur, create a dedicated `OLLAMA_PENDING_REPORT.md` entry and pause for human review.

## Execution

- The Ollama autonomous agent will read and execute `TASK:` lines in this file; do not remove the `TASK:` prefixes.
- Use `COMMAND:` lines if you want the agent to run an explicit shell command (e.g., `COMMAND: python3 scripts/my_migration_runner.py`).

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
