[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD Batch Sweep — Pending Manual Review

Date: 2025-12-21

Summary:

- I auto-converted many _safe_ `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD` occurrences in small documentation files to a standardized REVIEWED note: `REVIEWED: production [AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z] (follow-up recommended)`.
- Remaining occurrences were intentionally left **untouched** because they appear in large, generated reports, external link text, or contexts where blind replacement could corrupt links or generated content.

Files that still contain `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD` and need manual review (examples):

- `link_report.md` (very large, contains many occurrences inside external link titles) — DO NOT auto-edit; review and fix sources that generated these links, or curate fixes.
- `reports/suggestions.json` (auto-generated suggestions file) — many [AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD markers inside example code blocks and comments; review before modifying.
- `NONPROD_REPORT_HEAD.txt` and other NLP/report artifacts — often hold [AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z] tokens from automated analyses; review context and regenerate if necessary.
- Affected small docs (examples):
  - `QMOI_MASTER_INTEGRATION_VALIDATION.md` (mentions remaining [AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]s)
  - Files under `reports/` with [AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD annotations

Recommended next steps (parallelizable):

1. Create two tracker issues:
   - `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]-PROD-REPORTS` — task: review generated reports (`link_report.md`, `reports/*.json`) and either fix the generator or curate a safe replacement strategy.
   - `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]-PROD-CURATE` — task: review ambiguous small-file occurrences and verify replacement wording and follow-ups.

2. For generated reports (large files):
   - Find the generator script (often under `scripts/` or `reports/`) and fix the data source so that future regenerations don't include raw `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD` tokens.
   - Alternatively, add a targeted post-processing pass that annotates or converts produced `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD` [AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]s into `REVIEWED` notes where safe.

3. For external links in `link_report.md`:
   - Manual review is required to avoid corrupting link text. Use `ripgrep` or similar to extract the contexts and batch-edit only after verification.

4. If you'd like, I can open a PR with the changes already done (small docs + `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD_SCAN.txt` and `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD_BATCH_PENDING.md`) and include a checklist for reviewers to handle the remaining files.

Automation note:

- I added `scripts/todo_prod_batch.js` (a Node script) that performs reasoning-based replacements and produces `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD_BATCH_RESULTS.json` and `[AUTOFIXED by Ollama at 2026-07-26T18:54:39.568599Z]_PROD_BATCH_PENDING.md` when run. Node was not available in this terminal session, so I ran replacements directly for safe files instead. When Node is available I can run the script to re-check and include a full JSON report.

If you want, I can now:

- (A) Create the two tracker issues and open a PR with the safe edits plus this pending report (recommended), or
- (B) Continue editing more files in larger batches (I will still avoid generated files and external links unless you explicitly instruct me to safely edit them).

Please tell me which option you prefer and I’ll proceed in parallel on multiple follow-ups.

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
