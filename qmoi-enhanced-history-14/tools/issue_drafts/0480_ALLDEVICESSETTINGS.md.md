---
title: "Issue draft for ALLDEVICESSETTINGS.md"
generated: 2025-11-08T16:06:38.258694Z
---

# Review needed: ALLDEVICESSETTINGS.md

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:41.706781Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:41.706781Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:41.706781Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
---
title: "QMOI All Devices Settings & Features Reference"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->
## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI All Devices Settings & Features Reference

This file documents the features, settings, and UI capabilities for each QMOI app/device type. It ensures every app is fully set up for its target device, with device-specific enhancements and access to all UI/app features.

## Android
- App: `Qmoi_apps/android/qmoi ai.apk`
- Features: Touch UI, notifications, background tasks, device sensors, file access, Google Play integration, offline install, USB transfer.

## Windows
- App: `Qmoi_apps/windows/qmoi ai.exe`
- Features: Mouse and pointer support, keyboard shortcuts, system tray, notifications, file explorer integration, offline install, USB transfer.

## Mac (Apple Laptop)
- App: `Qmoi_apps/mac/qmoi ai.dmg`
- Features: Mouse and pointer support, trackpad gestures, keyboard shortcuts, dock integration, notifications, file access, offline install, USB transfer.

## Linux
- App: `Qmoi_apps/linux/qmoi ai.appimage` / `Qmoi_apps/linux/qmoi ai.deb`
- Features: Mouse and pointer support, keyboard shortcuts, notifications, file manager integration, offline install, USB transfer.

## iOS
- App: `Qmoi_apps/ios/qmoi ai.ipa`
- Features: Touch UI, notifications, device sensors, offline install, USB transfer, App Store integration.

## Smart TV
- App: `Qmoi_apps/smarttv/qmoi ai.apk`
- Features: Remote control support, large screen UI, notifications, offline install, USB transfer.

## Raspberry Pi
- App: `Qmoi_apps/raspberrypi/qmoi ai.img`
- Features: GPIO integration, mouse/pointer, keyboard, notifications, offline install, USB transfer.

## Chromebook
- App: `Qmoi_apps/chromebook/qmoi ai.zip`
- Features: Touch UI, keyboard, notifications, file manager integration, offline inst
```

Notes:

- This draft was generated automatically to help triage files removed from `donerefs.txt`.
- Backups and previous runs may exist under `.qmoi_validation`.

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
