---
title: "QMOI Friendship Integration Runbook"
qmoi_validation_frontmatter: true
---

# QMOI Friendship Integration Runbook

This runbook documents how the `qmoi-friendship-integration.js` module operates, how to run it safely, and where it writes proposals and artifacts.

Key principles

- Safe-by-default: destructive actions are never executed unless explicitly enabled.
- Proposal-first: any change (installing deps, syntax fixes, git operations, or configuration updates) is written as a proposal under `.qmoi_validation/` for human review.
- Explicit production gating: to allow destructive actions you must set the environment variable `PRODUCTION_CONFIRMED=true` and pass `--real` on the command line.

Files & artifacts

- Main module: `qmoi-friendship-integration.js`
- Dry-run test: `tests/test_qmoi_friendship.js`
- Proposals (aggregated): `.qmoi_validation/error_fix_proposals.json`
- Per-proposal files: `.qmoi_validation/proposals/<timestamp>-<type>.json`

Environment variables

- `VERCEL_TOKEN` - Vercel API token (optional). If missing, Vercel deploys are dry-run and proposals are created.
- `GITLAB_TOKEN` - GitLab API token (optional). If missing, GitLab deploys will fail or be dry-run depending on code paths.
- `PRODUCTION_CONFIRMED` - When set to `true` and combined with `--real`, the module may perform destructive actions like writing files, installing deps, or pushing commits.

How to run

Dry-run (recommended for testing):

```bash
# run the simple dry-run test (safe)
node tests/test_qmoi_friendship.js
```

Review proposals

1. After running the dry-run, open `.qmoi_validation/error_fix_proposals.json` to see aggregated proposals.
2. For quick review, check `.qmoi_validation/proposals/` for individual proposal files.
3. Each proposal contains `type`, `detail`, and `timestamp` fields. Follow your team's review process to approve proposals.

Applying proposals (manual process)

1. Inspect the proposal file and verify the suggested change.
2. If the change is safe, you can either:
   - Manually apply the fix (edit files, run `npm install`, commit and push), or
   - Run the module in production mode to attempt automated application (only allowed when you trust the code):

```bash
# ONLY run when you have performed a human review and are sure
PRODUCTION_CONFIRMED=true node -e "const Q=require('./qmoi-friendship-integration.js'); (async()=>{ const i=new Q(); /* call methods that apply changes, e.g., detectAndFixErrors */ })()" --real
```

Notes and cautions

- Never run the `--real` mode on an environment you don't control.
- For dependency installation, prefer using containerized or isolated environments.
- The module writes small notes to `.env` when applying configuration changes; use a secret manager instead in production.

Next steps

- Add CI that runs `tests/test_qmoi_friendship.js` in CI (dry-run) and uploads `.qmoi_validation` artifacts to a secure location for human review.
- Integrate proposal files with an internal ticketing/review process (e.g., create a PR or open an issue automatically with the proposal contents for traceability).

Contact & ownership

- Maintainers: check repository CONTRIBUTORS or OWNERS files for the appropriate reviewer.

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
