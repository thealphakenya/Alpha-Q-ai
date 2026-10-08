---
title: "SERVEQCITYQMOIAIQMOISPACE.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# SERVEQCITYQMOIAIQMOISPACE.md

This document describes how to serve QCity, QMOI AI, and QMOI Space for all apps, app types, and platforms, including automation and autofix features.

## QCity Serving

- Main entry: `QCITYREADME.md`, `QCITYMAINDEVICE.md`, and related scripts in `qcity-artifacts/`
- Serve via Python/Node.js web server (search for main server script or use FastAPI/Flask/Express)
- UI features: Referenced in `QCITYRESOURCES.md`, `QCITYRUNNERSENGINE.md`, and `QCITYQMOIAUTOSTART.md`
- All endpoints and UI features are autotested and autofixed by QMOI

## QMOI AI Serving

- Main entry: `qmoi_ai.py`, `qmoi_ai_launcher.py`, `main.py` (if present)
- Serve via Python backend (FastAPI/Flask)
- UI features: Referenced in `QMOI-ENHANCED-FEATURES.md`, `QMOI-ENHANCED-AUTOTESTS.md`, and `QMOI_MEMORY.md`
- All endpoints and UI features are autotested and autofixed by QMOI

## QMOI Space Serving

- Main entry: `qmoi-space/`, `QMOISPACEDEV.md`, `QMOISPACEUI.md`
- Serve via Python/Node.js backend or Gradio/Streamlit for AI features
- UI features: Referenced in `QMOISPACEUI.md`, `QMOISPACEDEV.md`, and `QMOIHUGGINGFACESPACES.md`
- All endpoints and UI features are autotested and autofixed by QMOI

## Automation & Enhancement

- QMOI runs background scripts to autotest, serve, and autofix all features for all apps and platforms
- Errors detected in any app or browser are autofixed automatically
- All serving and autofix features are referenced and documented for permanent operation

## Error Handling & Debugging

- All serving errors and issues are logged in SERVINGERRORSISSUES.md in real time
- Terminal output and debugging information are referenced for autofix and enhancement
- QMOI uses this log to locate, fix, and enhance all serving issues

<!-- QMOI_VALIDATION_START -->

{
"file": "SERVEQCITYQMOIAIQMOISPACE.md",
"validated_at": "2025-10-26T20:51:22.630809Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "SERVEQCITYQMOIAIQMOISPACE.md"
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
