# Production Changes Applied Automatically

This file summarizes the automated production-ready fixes and enhancements applied by the assistant.

- Stabilized `updateQMOIMemory` in `components/MasterContext.tsx`:
  - Now uses `useCallback` and accepts functional updaters to prevent infinite render loops.

- Fixed Chatbot memory syncing:
  - `components/Chatbot.tsx` and `src/components/Chatbot.tsx` now best-effort POST to `/api/qmoi/memory` when conversations change to keep server memory synchronized.

- Enhanced avatar preview UI:
  - `src/components/q-city/AvatarSelector.tsx` now shows a live `iframe` preview when `previewUrl` or `demoUrl` is provided by the avatar configuration, with a clear fallback UI.

- Removed duplicate Next.js page file `app/qcity/page.js` to resolve duplicate-route warnings.

- Started and verified Next dev server and ran a production build; build completed successfully (see `build.log`).

- Updated `API_ENDPOINTS_REFERENCE.md` with production readiness notes.

What I recommend next (can implement automatically):

- Run full test suite (`npm run test:all`) and fix failing tests.
- Run `npm run lint:fix` and address remaining lint warnings.
- Audit and consolidate duplicate components (e.g., multiple `Chatbot` implementations) to a single canonical location.
- Update user-facing docs for `QVillage` to mark web-only where appropriate (several docs already reference this).
- Configure CI to run `npm run build && npm run test:all` on pull requests.

If you want, I will now run tests and lint, then consolidate duplicate components and update docs accordingly.


---
Checked by Ollama agent at 2026-07-21T22:49:04.514683Z. No immediate [AUTOFIXED by Ollama at 2026-07-26T00:54:34.627123Z]s found.

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
