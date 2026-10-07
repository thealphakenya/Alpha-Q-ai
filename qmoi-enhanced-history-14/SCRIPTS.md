---
title: "SCRIPTS.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# SCRIPTS.md

This file documents all scripts in the `scripts/` directory, their usage, and integration for QCity, QMOI AI, and QMOI Space. All scripts are checked to ensure they are used and served as expected. Unused or duplicate scripts are marked for removal.

## Directory Structure

```
scripts/
├── api/
│   └── automation_api.py  # FastAPI endpoints for AI automation, serving QCity, QMOI AI, QMOI Space
├── ai_automation.py       # Core AI automation, orchestration, and optimization
├── search_and_serve_components.py  # Logs unused components/UI features for integration
├── auto_updater.py        # Automates documentation updates and system checks
├── ensure_build_files.py  # Ensures all build files are present and up-to-date
├── doit.py                # Task automation and orchestration
├── ... (many more scripts for deployment, error handling, device management, etc.)
```

## Usage & Integration

- **api/automation_api.py**: Provides REST API endpoints for automation, used by QCity, QMOI AI, and QMOI Space for orchestration and health checks.
- **ai_automation.py**: Main automation engine, runs all AI-powered tasks, error fixing, and optimization for all platforms.
- **search_and_serve_components.py**: Scans all component/UI directories, logs unused features, and ensures all are integrated and served.
- **auto_updater.py**: Keeps documentation and system files up-to-date, triggers auto-fix and health checks.
- **ensure_build_files.py**: Verifies build files for all apps/platforms, triggers rebuilds if needed.
- **doit.py**: Orchestrates tasks and automation flows for all QMOI systems.
- **Other scripts**: Cover deployment, device management, error handling, financial integration, and more. All are referenced in automation flows and serve QCity, QMOI AI, and QMOI Space.

## UI Features & Coverage

- All scripts related to UI features (e.g., enhanced_preview.py, enhanced_qmoi_implementation.py) are checked for usage in QCity, QMOI AI, and QMOI Space.
- Unused/duplicate scripts are marked for removal in SERVINGERRORSISSUES.md and will be deleted in the next cleanup.

## Automation & Health

- All scripts are referenced in `ALLMDFILESREFS.md` and are planned for further enhancement and integration.
- Automation ensures every script is used, and unused ones are logged for removal.

**Status:** All scripts are now checked for usage and integration. No unused/duplicate scripts will remain after next cleanup. All UI features and automation flows are covered for QCity, QMOI AI, and QMOI Space.

<!-- QMOI_VALIDATION_START -->

{
"file": "SCRIPTS.md",
"validated_at": "2025-10-26T20:51:22.623340Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "SCRIPTS.md"
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

## Autonomous workflow integration

- This directory document is maintained by the Ollama autonomous agent and synchronized with the GitHub workflow triggers.
- It tracks WiFi/captive-portal automation, component gallery migration, universal styles, and self-healing run expectations.
- Keep this file aligned with API.md, ENDPOINTS.md, ROUTES.md, ALLPORTS.md, STYLES.md, UNIVERSALS.md, and WORKFLOWS.md.
- Ensure every run records resume state in resumefromhere.txt and preserves processed work between local and workflow executions.

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
