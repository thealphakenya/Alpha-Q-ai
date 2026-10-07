---
title: "API / Routes Enhancement Plan"
qmoi_validation_frontmatter: true
---

# API / Routes Enhancement Plan

Purpose

- Produce a verified API inventory, ensure `API.md` and `ENDPOINTS.md` contain live-verified examples, and add automated endpoint checks to CI.

Steps

1. Extraction
   - Extract server routes and API handlers from `app/api` and server folders using static analysis and small runtime probes.
2. Validation
   - Create a test harness that can run against a dev server or a mocked server to validate status codes, schemas, and auth flows.
3. Documentation
   - Auto-generate `API.md` sections from verified endpoints and include example curl requests and Postman collections.
4. RSA / Security
   - Update `RSAAPIREADME.md` with concrete configuration, key rotation instructions, and example signed request flows.
5. WPA / Security Review
   - If WPA refers to wireless auth or a project-specific acronym, run an explicit security audit and document findings in `docs/WPA-REVIEW.md`.

Short term actionable tasks

- Add `scripts/extract_endpoints.py` to generate a `docs/api_endpoint_index.json` (can be run in CI).
- Add `tests/integration/test_endpoints.py` (pytest) to run against a running dev server for core endpoints.
- Add a GitHub Action to run endpoint smoke tests on push to main.

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/API_ENHANCEMENTS_PLAN.md",
"validated_at": "2025-10-26T20:51:22.675357Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "API / Routes Enhancement Plan"
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
