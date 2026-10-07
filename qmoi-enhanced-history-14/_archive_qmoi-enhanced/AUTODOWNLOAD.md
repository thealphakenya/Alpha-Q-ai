---
title: "AU[AUTOFIXED by Ollama at 2026-07-26T18:54:39.585427Z]WNLOAD.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# AU[AUTOFIXED by Ollama at 2026-07-26T18:54:39.585427Z]WNLOAD.md

## QMOI App Autodownload System

### Overview

This document describes the fully automated system for downloading and organizing all QMOI apps for every supported device and platform. The system ensures all apps are always available, up to date, and saved in their required directories, with no manual intervention required.

### Features

- **Autodownload All Apps:** Automatically downloads every app listed in QMOIAPPS.md and README.md for all platforms/devices.
- **Directory Structure:** All downloads are saved in `Qmoi_downloaded_apps/<platform>/latest/` and `Qmoi_downloaded_apps/<platform>/v<version>/`.
- **Device Coverage:** Supports Windows, Mac, Linux (DEB/AppImage), Android, iOS, Smart TV, Raspberry Pi, Chromebook, and more.
- **Billing-Safe:** No paid GitHub Actions, runners, or features are used. All automation runs on self-hosted/cloud runners (Colab, DagsHub, QCity, etc.) to avoid billing issues.
- **Auto-Update:** All download links are autotested and auto-updated (ngrok, fallback, etc.) before download. See QMOINGROK.md for details.
- **Error Handling:** If a download fails, the system retries, logs the error, and notifies master/master. All actions are auditable.
- **No Billing Issues:** All automation is designed to run on free or self-hosted infrastructure. No paid GitHub features are required or used.

### How It Works

1. **App List Extraction:** The automation reads QMOIAPPS.md and README.md to extract all app names and download links for every device/platform.
2. **Download Execution:** For each app and device, the system downloads the latest version using the provided link, saving it in the correct directory.
3. **Directory Organization:** All files are saved in `Qmoi_downloaded_apps/<platform>/latest/` and `Qmoi_downloaded_apps/<platform>/v<version>/`.
4. **Verification:** After download, the system verifies file size and integrity. If a file is missing or invalid, it retries or logs the error.
5. **Audit & Notification:** All actions are logged. Master/master is notified of any persistent issues.

### Example Directory Structure

```
Qmoi_downloaded_apps/
  windows/
    latest/
      qbrowser.exe
      qfilemanager.exe
      ...
    v1.2.0/
      qbrowser.exe
    v2.0.1/
      qfilemanager.exe
  mac/
    latest/
      qbrowser.dmg
      ...
  android/
    latest/
      qbrowser.apk
      ...
  ...
```

### Automation Script

- The main script is `downloadqmoiai.py`, which can be extended to loop over all apps and platforms.
- Platform-specific scripts (e.g., `downloadqmoiaiapk.py`, `downloadqmoiaiexe.py`) are also supported.

### Billing-Safe Design

- **No Paid GitHub Actions:** All automation is run on self-hosted or cloud runners (Colab, DagsHub, QCity, etc.).
- **No External Billing:** No step in the autodownload process requires a paid plan or incurs costs on GitHub.
- **Fallback Logic:** If a runner or service fails due to quota or billing, the system auto-switches to another free/cloud runner.

### See Also

- QMOIAPPS.md (app list and links)
- README.md (platforms and download structure)
- QMOINGROK.md (ngrok tunnel automation)
- QMOIQCITYAUTOMATIC.md (cloud automation)
- QCITYRUNNERSENGINE.md (self-hosted runners)

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/AU[AUTOFIXED by Ollama at 2026-07-26T18:54:39.585427Z]WNLOAD.md",
"validated_at": "2025-10-26T20:51:24.594875Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "AU[AUTOFIXED by Ollama at 2026-07-26T18:54:39.585427Z]WNLOAD.md"
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
