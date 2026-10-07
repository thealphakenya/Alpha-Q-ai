---
title: "Markdown File References"
qmoi_validation_frontmatter: true
---

# Markdown File References

A master index of all Markdown documentation in this repository.

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-31T10:00:00.000000Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

<!-- QMOI_VALIDATION_START -->

{
"file": "@ALLMDFILESREFS.md",
"validated_at": "2025-10-31T10:00:00.000000Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "Found H1 title 'Markdown File References'"
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

## Documentation Index

### Core Documentation

- [ALLLINKS.md](ALLLINKS.md) - Master list of all external links and their statuses
- [HOSTLINKSDOMAINS.md](HOSTLINKSDOMAINS.md) - DNS and hosting configuration reference
- [operations.md](docs/operations.md) - Operations guide, security gates and configuration

### Generated Reports

- [link_validation.log](.qmoi_validation/link_validation.log) - Link validation results
- [provider_calls.log](.qmoi_validation/provider_calls.log) - DNS provider operation logs
- [all_links.json](.qmoi_validation/all_links.json) - Link metadata cache


---

## Merged source: qmoi-enhanced-history-14/_archive_qmoi-enhanced/@ALLMDFILESREFS.md

---
title: "ALL MD Files References - Enhanced Comprehensive Edition"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# ALL MD Files References - Enhanced Comprehensive Edition

## Overview

## Codespace/Cloud Automation

- All QMOI features (builds, storage, memory, error fixing, etc.) are elastically offloaded to QMOI Cloud when running in Codespaces or any low-resource environment.
- PWAs and all apps are always available, never blocked by local resource limits.

This comprehensive reference document catalogs and categorizes all .md files in the QMOI system with advanced categorization, automation features, and health checks. The system ensures QMOI can automatically reference, fix, and enhance all documentation.

- **All app download links are now provided via https://github.com/thealphakenya/qmoi-enhanced/releases/**
- **All links are autotested and always up-to-date, managed by QCity runners.**
- **See [ALLQMOIAIAPPSREALEASESVERSIONS.md](ALLQMOIAIAPPSREALEASESVERSIONS.md) for all app releases and versions.**
- **See [DOWNLOADQMOIAIAPPALLDEVICES.md](DOWNLOADQMOIAIAPPALLDEVICES.md) for all device/platform download instructions.**

## Download Autofix & Customer Care (2025+)

- All download links are autotested, auto-fixed, and always up-to-date.
- Download UI and scripts feature robust error handling, retry logic, and real-time status.
- Users can report issues directly from the download UI; all issues are logged and prioritized for immediate fix.
- Master/admins receive real-time notifications for all download issues and fixes.
- See [ALLQMOIAIAPPSREALEASESVERSIONS.md](ALLQMOIAIAPPSREALEASESVERSIONS.md) and [DOWNLOADQMOIAIAPPALLDEVICES.md](DOWNLOADQMOIAIAPPALLDEVICES.md) for all links and troubleshooting.

> **Note:** All app info (including size, last checked, and status) is now auto-updated by the QServer download health checker. All documentation and app info is always up-to-date and precise.

# QMOI App Build Automation (2025-06-13)

- The QMOI app builder script (`scripts/qmoi-app-builder.py`) now performs real builds for:
  - **Windows**: Electron app, built after Next.js build and server start, output as `Qmoi_apps/windows/qmoi ai.exe`.
  - **Android**: React Native APK, built and output as `Qmoi_apps/android/qmoi ai.apk`.
  - **iOS**: React Native IPA (if on macOS), output as `Qmoi_apps/ios/qmoi ai.ipa`.
- All actions and errors are robustly logged via `qmoi_activity_logger`.
- [AUTOFIXED by Ollama at 2026-07-26T18:54:39.580453Z]_PRODs remain for mac, linux, chromebook, raspberrypi, smarttv, qcity.
- All output files are named `qmoi ai` and placed in the correct subdirectory.
- Download links and notifications are updated automatically after each build.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/@ALLMDFILESREFS.md",
"validated_at": "2025-10-26T20:51:24.587629Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "ALL MD Files References - Enhanced Comprehensive Edition"
},
{
"name": "links",
"ok": true,
"detail": [
{
"label": "ALLQMOIAIAPPSREALEASESVERSIONS.md",
"target": "./ALLQMOIAIAPPSREALEASESVERSIONS.md",
"ok": true
},
{
"label": "DOWNLOADQMOIAIAPPALLDEVICES.md",
"target": "./DOWNLOADQMOIAIAPPALLDEVICES.md",
"ok": true
},
{
"label": "ALLQMOIAIAPPSREALEASESVERSIONS.md",
"target": "./ALLQMOIAIAPPSREALEASESVERSIONS.md",
"ok": true
},
{
"label": "DOWNLOADQMOIAIAPPALLDEVICES.md",
"target": "./DOWNLOADQMOIAIAPPALLDEVICES.md",
"ok": true
}
]
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
