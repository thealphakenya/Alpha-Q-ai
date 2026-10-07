---
title: "QMOIBROWSER.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOIBROWSER.md

## QMOI Browser: Automated Testing & Error-Fixing Engine

QMOI Browser is a fully automated, AI-powered browser used by QMOI to autotest, validate, and fix all links, downloads, and web-based features across all platforms and devices. It is deeply integrated into all QMOI automation, deployment, and monitoring systems.

### Features

- **Automated Link Testing:** QMOI Browser continuously tests all download links, websites, and APIs for availability, correctness, and performance.
- **Error Detection & Auto-Fix:** Any broken or slow link is automatically fixed, re-uploaded, or replaced. QMOI logs and notifies all issues and fixes.
- **Parallel Testing:** All links and web features are tested in parallel for maximum speed and coverage.
- **Integration:** QMOI Browser is used in all automation cycles (AutoDev, AutoEvolve, Clone, WatchDebug, etc.) to ensure all web features are always working.
- **Cloud/Colab/Dagshub Offloading:** All browser-based testing is offloaded to QCity/cloud for speed and reliability.
- **Master-Only Controls:** Master can view browser test logs, trigger manual tests, and review fixes in QCity dashboard.
- **Audit Logging:** All browser actions are logged for compliance and transparency.

### DNS & Link Auto-Resolution Enhancements

- **DNS Auto-Check & Fix:** QMOI Browser now automatically checks DNS for all download links (e.g., downloads.qmoi.app). If DNS is misconfigured or fails, QMOI triggers an auto-fix routine to set up or repair DNS records, notifies master/master, and logs all actions.
- **Zero-Rated & Fallback Links:** If DNS cannot be fixed immediately, QMOI Browser auto-switches to zero-rated or fallback CDN links (see ZERORATEDQMOI.md) to ensure downloads always work, even in restricted or offline environments.
- **Freenom Fallback:** If DNS cannot be fixed, QMOI Browser auto-registers a free fallback domain via Freenom, updates all download links, and ensures downloads remain available. All actions are logged and master/master is notified.
- **Master/Master Controls:** Master can view DNS/link health, trigger manual DNS checks, and review logs in the QCity dashboard.
- **Full Automation:** All DNS and link health checks, fixes, and fallback logic are fully automated and require no manual intervention.

### Usage

- QMOI Browser runs automatically in every automation cycle.
- Master can trigger manual browser tests from QCity UI (master-only panel).
- All issues are auto-fixed and logged, with notifications sent to master/master.

### API & UI

- `/api/qcity/browser-test` endpoint for triggering and monitoring browser tests (master-only, API key required).
- QCity dashboard panel for viewing browser test results, logs, and fixes.

### Integration Points

- QMOIAUTODEV.md: Browser is used in every automation/fix cycle.
- QMOIAUTOEVOLVE.md: Auto-evolution uses browser to validate new features.
- QMOICLONE.md: All cloned sites/devices are autotested with browser.
- WATCHDEBUG.md: Browser logs and fixes are visible in WatchDebug panel.

---

_This file is managed by QMOI and documents all browser automation and autotesting logic._

<!-- QMOI_VALIDATION_START -->

{
"file": "QMOIBROWSER.md",
"validated_at": "2025-10-26T20:51:22.471220Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOIBROWSER.md"
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


---

## Merged source: qmoi-enhanced-history-14/_archive_qmoi-enhanced/QMOIBROWSER.md

---
title: "QMOIBROWSER.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOIBROWSER.md

## QMOI Browser: Automated Testing & Error-Fixing Engine

QMOI Browser is a fully automated, AI-powered browser used by QMOI to autotest, validate, and fix all links, downloads, and web-based features across all platforms and devices. It is deeply integrated into all QMOI automation, deployment, and monitoring systems.

### Features

- **Automated Link Testing:** QMOI Browser continuously tests all download links, websites, and APIs for availability, correctness, and performance.
- **Error Detection & Auto-Fix:** Any broken or slow link is automatically fixed, re-uploaded, or replaced. QMOI logs and notifies all issues and fixes.
- **Parallel Testing:** All links and web features are tested in parallel for maximum speed and coverage.
- **Integration:** QMOI Browser is used in all automation cycles (AutoDev, AutoEvolve, Clone, WatchDebug, etc.) to ensure all web features are always working.
- **Cloud/Colab/Dagshub Offloading:** All browser-based testing is offloaded to QCity/cloud for speed and reliability.
- **Master-Only Controls:** Master can view browser test logs, trigger manual tests, and review fixes in QCity dashboard.
- **Audit Logging:** All browser actions are logged for compliance and transparency.

### DNS & Link Auto-Resolution Enhancements

- **DNS Auto-Check & Fix:** QMOI Browser now automatically checks DNS for all download links (e.g., downloads.qmoi.app). If DNS is misconfigured or fails, QMOI triggers an auto-fix routine to set up or repair DNS records, notifies master/master, and logs all actions.
- **Zero-Rated & Fallback Links:** If DNS cannot be fixed immediately, QMOI Browser auto-switches to zero-rated or fallback CDN links (see ZERORATEDQMOI.md) to ensure downloads always work, even in restricted or offline environments.
- **Freenom Fallback:** If DNS cannot be fixed, QMOI Browser auto-registers a free fallback domain via Freenom, updates all download links, and ensures downloads remain available. All actions are logged and master/master is notified.
- **Master/Master Controls:** Master can view DNS/link health, trigger manual DNS checks, and review logs in the QCity dashboard.
- **Full Automation:** All DNS and link health checks, fixes, and fallback logic are fully automated and require no manual intervention.

### Usage

- QMOI Browser runs automatically in every automation cycle.
- Master can trigger manual browser tests from QCity UI (master-only panel).
- All issues are auto-fixed and logged, with notifications sent to master/master.

### API & UI

- `/api/qcity/browser-test` endpoint for triggering and monitoring browser tests (master-only, API key required).
- QCity dashboard panel for viewing browser test results, logs, and fixes.

### Integration Points

- QMOIAUTODEV.md: Browser is used in every automation/fix cycle.
- QMOIAUTOEVOLVE.md: Auto-evolution uses browser to validate new features.
- QMOICLONE.md: All cloned sites/devices are autotested with browser.
- WATCHDEBUG.md: Browser logs and fixes are visible in WatchDebug panel.

---

_This file is managed by QMOI and documents all browser automation and autotesting logic._

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/QMOIBROWSER.md",
"validated_at": "2025-10-26T20:51:24.751562Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOIBROWSER.md"
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
