---
title: "QMOI Validation Tools"
qmoi_validation_frontmatter: true
---

# QMOI Validation Tools

This document explains the lightweight validation tools included in the repository and how to use them.

Key tools

- `scripts/generate_allmdrefs.py` — discovers repository `.md` files (excluding vendor dirs) and writes `.qmoi_validation/md_files_found.json`. Use `--write` to update `ALLMDFILESREFS.md`.
- `scripts/validate_md.py` — validates markdown files for title, frontmatter, and links. Writes per-file reports to `.qmoi_validation/validation_reports/`. Use `--apply` to insert/update validation metadata blocks.
- `scripts/validate_md.py` — validates markdown files for title, frontmatter, and links. Writes per-file reports to `.qmoi_validation/validation_reports/`. Use `--apply` to insert/update validation metadata blocks. The validator now captures QVS provenance (when `.qmoi_validation/qvs_context.json` exists) and records minimal run provenance (Codespace, GITHUB_RUN_ID, host, user) into each report for auditability.
- `scripts/qmoi_todos.py` — lightweight to-dos manager used by validation automation and orchestrators (LION hooks can be added where noted).

Quick start

1. Dry-run discovery:

   python3 scripts/generate_allmdrefs.py

2. Write refs (if review OK):

   python3 scripts/generate_allmdrefs.py --write

3. Dry-run validation (no file modification):

   python3 scripts/validate_md.py

4. Apply validation blocks into files:

   python3 scripts/validate_md.py --apply

Integration points

- LION: validation tools produce JSON outputs in `.qmoi_validation/` which LION can consume to coordinate further remediation, backups to QVS, or to create validation tasks in the QMOI to-dos system.
- QVS: validation reports and marked files can be snapshot to QVS for audit/history.
- QVS: validation reports and marked files can be snapshot to QVS for audit/history. Validation reports now include `qvs` or `qvs_provenance` keys with structured provenance information. See `.qmoi_validation/validation_reports/` and `.qmoi_validation/runs.log` for recorded run events.

Applications & builds

- App discovery and artifact registry: `scripts/collect_build_scripts.py` and `scripts/register_app_build.py` scan the repo for build scripts and build outputs and write results to `.qmoi_validation/` (see `.qmoi_validation/build_scripts_found.json` and `.qmoi_validation/apps_found.json`). Use `register_app_build.py --copy` to move artifacts into `ALL_APPS/` (dry-run first).
- Validation tools can be extended to validate build outputs (e.g., check build manifests, sizes, checksums, and that a build completed successfully). See `scripts/register_app_build.py` for a starting point.

Notes

- All tools are lightweight and dependency-free (pure Python standard library). They are safe to run locally and in CI; they avoid vendor directories by default.

## QMOI Validation Tools

This document explains the validation tooling added to the repository and how they are intended to be used.

- `scripts/generate_allmdrefs.py` — scans the repo for `.md` files (excludes vendor dirs) and can update `ALLMDFILESREFS.md` with the discovered list.
- `scripts/validate_md.py` — validates markdown files and inserts/updates a QMOI validation block inside each file; writes per-file JSON reports to `.qmoi_validation/`.
- `scripts/qmoi_todos.py` — a lightweight to-dos manager that persists tasks to `.qmoi_validation/todos.json` and can export plans for validators.

Quick usage:

1. Scan for .md files (dry-run):

   python3 scripts/generate_allmdrefs.py

2. Write to `ALLMDFILESREFS.md`:

   python3 scripts/generate_allmdrefs.py --write

3. Validate markdown files (dry-run doesn't write validation blocks):

   python3 scripts/validate_md.py --dry-run

4. Run validator and tag files:

   python3 scripts/validate_md.py

5. Manage QMOI to-dos:

   python3 scripts/qmoi_todos.py add "Finish validation" --note "run validate_md" --priority 3
   python3 scripts/qmoi_todos.py list
   python3 scripts/qmoi_todos.py done 1

All outputs and reports are stored in `.qmoi_validation/` so CI or other tools can pick them up.

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/VALIDATION_TOOLS.md",
"validator": "qmoi-validator-v3",
"checked_at": "2025-11-07T13:03:53.260806+00:00",
"checks": {
"readable": {
"ok": true
},
"title_present": {
"ok": true,
"detail": "QMOI Validation Tools"
},
"frontmatter_present": {
"ok": false
},
"links": {
"ok": true,
"detail": []
},
"build_info": {
"build": "not_found"
}
},
"ok": false,
"lion_task": {
"id": "735061c5-43c8-4213-80e6-5635724eda4a",
"task": "remediate_markdown_issues",
"created_at": "2025-11-07T13:03:53.260806+00:00",
"notes": "Auto-generated remediation suggestion (title/frontmatter/links)",
"priority": "medium",
"recommended_actions": [
"add H1 title",
"add frontmatter",
"fix broken links"
],
"qcity_hints": {
"preferred_cluster": "qcity-default",
"storage_bucket": "qcity-artifacts"
}
},
"qvs_provenance": {
"codespace": "silver-journey-r4596xxpxg99cw594",
"github_run_id": null,
"user": "vscode",
"host": "codespaces-08409b"
}
}

<!-- QMOI_VALIDATION_END -->

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
