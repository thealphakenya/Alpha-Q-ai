---
title: "ALLTESTSAUTOTESTS.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# ALLTESTSAUTOTESTS.md

Purpose

- A single reference file listing all tests and autotests, their purposes, how to run them locally and in CI, and how they integrate with self-heal and autodev.

Structure

- Unit tests
  - folder: `packages/*/test` or `__tests__`
  - runner: jest (see `jest.config.js`) or `pytest` for Python
  - purpose: fast checks of core functions
- Integration tests
  - runner: play scripts or integration suite
  - purpose: test interaction between modules (API, DB, runners)
- End-to-end tests
  - tools: Playwright / Cypress / puppeteer or custom harness
  - purpose: full-user flows, eg: extension start, chat UI open, to-do automation flow
- Self-heal tests
  - purpose: simulate failures and assert self-heal reactions (restart, fallback)
  - example: bring down a service and assert auto-restart via orchestration scripts
- Autodev tests
  - purpose: validate autodev pipelines (builds, cross-platform artifacts)
  - example: run build scripts for linux/mac/win in isolated containers

How to run

- Local quick-run (unit): `npm test` (or `pnpm test`) in service/package
- CI: GitHub Actions workflows will run the matrix across OS/Node versions

Integration with self-heal & autodev

- Tests should be labeled with metadata tags so the autotest runner can pick them (eg: `[self-heal]`, `[autodev]`).
- The autotest runner collects results and decides remediation: re-run, add to todo, create incident.

Files & CI refs

- Add CI workflow: `.github/workflows/autotests.yml` that runs the full test matrix and uploads artifacts.

Next steps

- Generate test list automatically using `scripts/generate_test_index.py` (todo)
- Add descriptions for tests listed in `teststoadd.txt` and map them to CI jobs

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/ALLTESTSAUTOTESTS.md",
"validated_at": "2025-10-26T20:51:22.673313Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "ALLTESTSAUTOTESTS.md"
},
{
"name": "links",
"ok": true,
"detail": []
}
],
"passed": true,
"summary": {
"total_checks": 2,
"passed": true
}
}

<!-- QMOI_VALIDATION_END -->

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
