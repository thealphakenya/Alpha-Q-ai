---
title: "Placeholder Scan Summary"
qmoi_validation_frontmatter: true
---

# Placeholder Scan Summary

Created by running `tools/find_[AUTOFIXED by Ollama at 2026-07-20T01:19:41.424624Z: please review]s.py`.

- Total matches found: 27736
- Files with matches: 1264

Top sample files with high counts (first entries from `allrefs.txt`):

1. .qmoi_validation/[AUTOFIXED by Ollama at 2026-07-20T01:19:41.424624Z: please review]_suggestions.json — 8593 matches
2. .qmoi_validation/[AUTOFIXED by Ollama at 2026-07-20T01:19:41.424624Z: please review]s.json — 3166 matches
3. .qmoi_validation/[AUTOFIXED by Ollama at 2026-07-20T01:19:41.424624Z: please review]_report.json — 408 matches
4. .qmoi_validation/links_report.json — 98 matches
5. .qmoi_validation/link_update_plan.json — 54 matches
6. qmoi-enhanced/app/api/qmoi-model.ts — 36 matches
7. docs/\* and many `qmoi` docs — multiple matches across many files

Notes & next actions

- Run `tools/auto_fix_[AUTOFIXED by Ollama at 2026-07-20T01:19:41.424624Z: please review]s.py` (dry-run) to generate `[AUTOFIXED by Ollama at 2026-07-20T01:19:41.424624Z: please review]_fixes.patch` for conservative fixes.
- Review high-volume generated JSON validation files in `.qmoi_validation/` — many matches are probably auto-generated and need targeted filtering (these files may be validation artifacts rather than source code).
- Use `tools/update_all_md_refs.py` to regenerate `ALLMDFILESREFS.md` after new .md files are added.

Location of detail outputs:

- `matches.json` — per-match detailed records
- `allrefs.txt` — list of file paths and counts

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->


---
Automated update by Ollama agent at 2026-07-20T01:19:41.424624Z. Please review changes above.

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
