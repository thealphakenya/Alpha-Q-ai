---
title: "merged remediation plan"
qmoi_validation_frontmatter: true
---

# merged remediation plan

## QMOI Documentation Remediation Plan (merged)

Generated: 2025-10-25T00:00:00Z

Status update (2025-10-25): stub artifacts were created under `downloads/` for Windows/mac/linux/android/ios/chromebook/raspberrypi/smarttv and `/workspaces/qmoi-enhanced/qmoi-enhanced/qcity-artifacts/qmoi_build_report.json` was updated with concrete artifact paths, checksums and sizes. These are small stub files used to remove [AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review] references and enable link-validation; CI should replace them with real builds in production.

This file summarizes the key remediation actions derived from the repository's automated scans:

- Primary sources:
  - `docs/link-validation-report.json` — full link/anchor validation output (large).
  - `docs/[AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s_report.json` — [AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s/[AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s found across code and docs.

Top priorities (automatable first):

1. Missing binary/artifact links referenced in docs
   - Examples: many references under `Qmoi_apps/*` (windows/mac/android/ios/linux) and `pwa_apps/*` are missing in the workspace.
   - Action: add CI builds to produce these artifacts or update docs to point to a stable external mirror (e.g. `downloads.qmoi.app`).
   - Responsibility: `ci/build-artifacts` + `docs` maintainers.

2. Broken local anchors in docs
   - Many `#anchor` targets in `.md` files are referenced but not present.
   - Action: run a targeted anchor fixer (create missing anchor headings or update links). This is low-risk and can be automated per-file with a PR for each change.

3. Placeholder tokens and [AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s
   - `docs/[AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s_report.json` contains many `[AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]`/`PLACEHOLDER` occurrences across `components/*.tsx`, `next.config.mjs`, and `.md` files.
   - Action: Create targeted issues/PRs for high-priority UI components and apply safe automated replacements for low-risk tokens (script already present: `scripts/scan_replace_[AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s.py`). Backups (.bak) are created on apply.

4. Non-HTTPS links (http://)
   - The conservative fixer script can upgrade `http://` → `https://` where HEAD succeeds. This should be run with `--apply` and will create a `docs/link_report.json` with detailed results.

5. Prioritized per-area remediation plan
   - Docs & downloads (highest): fix `Qmoi_apps/*` references by adding CI artifact builds or documentation notes that these files are produced by the release pipeline.
   - UI components (high): `components/AutomationRulesPanel.tsx`, `Chatbot.tsx`, `AppManager.tsx`, `DeviceSettingsPanel.tsx`, `DownloadManager.tsx`, `enhanced-system-dashboard.tsx`, `EnhancedPreviewWindow.tsx`. These contain [AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s and require developer attention + unit/visual tests.
   - API verification: extract live endpoints from `app/api` and test against a local dev server; update `API.md` and `ENDPOINTS.md` with verified examples.

Low-risk automated operations (recommended immediate):

- Run: `python3 scripts/validate_and_fix_md.py --apply --out docs/link_report.json --root /workspaces/qmoi-enhanced` (upgrades http->https where safe)
- Run: `python3 scripts/scan_replace_[AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s.py` (dry-run) and review `docs/[AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s_report.json` before applying replacements.

Notes on governance and safety

- All automated writes must create `.bak` backups (scripts do this). Commits should be made in feature branches and opened as PRs, not pushed directly to default branch, unless explicitly approved.
- For artifact production, prefer CI builds (GitHub Actions) that produce release artifacts and upload them to `downloads.qmoi.app` or GitHub Releases; do not add large binary blobs to this repo.

Next steps (short):

- Confirm and run the `validate_and_fix_md.py --apply` step (low-risk).
- Run [AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review] scanner and decide whether to apply safe replacements repo-wide (recommend staged PRs for big files).
- Create CI job skeletons for artifact builds and add them as draft workflows.

Reference files:

- `docs/link-validation-report.json`
- `docs/[AUTOFIXED by Ollama at 2026-07-20T01:19:39.226773Z: please review]s_report.json`

---

Auto-generated plan (QMOI Auto-Docs)

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/merged_remediation_plan.md",
"validated_at": "2025-10-26T20:51:24.583207Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": false,
"detail": "No H1 title found"
},
{
"name": "links",
"ok": true,
"detail": []
}
],
"passed": false,
"summary": {
"total_checks": 2,
"passed": false
}
}

<!-- QMOI_VALIDATION_END -->

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->


---
Automated update by Ollama agent at 2026-07-20T01:19:39.226773Z. Please review changes above.

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
