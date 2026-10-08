---
title: "QMOIICONS"
qmoi_validation_frontmatter: true
---

# QMOIICONS

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

QMOIICONS.md

QMOI Icons, locations, and auto-update process

Overview
QMOI uses a consistent icon set across platforms (desktop, mobile, web, TV) to ensure a unified UX. Icons are stored in the repository, installed with each platform build, and can be auto-updated by QMOI's automation engine.

Repository locations (convention)

- /assets/icons/ : master icon set (SVG, PNG, ICO)
- /mobile/assets/icons/ : mobile-specific sizes and adaptive icons
- /desktop/installer/icons/ : installer and shortcut icons
- /qmoi-space/public/icons/ : web icons and favicons

Naming conventions

- qmoi-{name}-{platform}.{ext}
  - Examples: qmoi-logo.svg, qmoi-notification-windows.ico, qmoi-shortcut-linux.png

Auto-update & distribution
QMOI provides a small icon manager that:

- checks a central icon manifest (.qmoi/icons.json)
- downloads any updated icons from the QMOI CDN or mirror
- replaces local icons atomically and regenerates favicons and platform-specific variants
- notifies platform services to reload icons (desktop tray, mobile assets cache)

Basic icon manifest format (.qmoi/icons.json)
{
"icons": [
{"name": "qmoi-logo", "versions": "1.2.0", "paths": {"svg": "assets/icons/qmoi-logo.svg"}},
{"name": "qmoi-notification", "versions": "1.0.1", "paths": {"ico": "desktop/installer/icons/qmoi-notification.ico"}}
],
"timestamp": 0
}

Auto-creation of shortcuts & system integration

- Desktop installers will create shortcuts during installation using platform-native installers (NSIS for Windows, .desktop for Linux, dmg pkg scripts for macOS).
- QMOI automation includes small helper scripts to register notification icons and tray menu entries.

Security & signing

- Icons that are downloaded during auto-update are checksummed (sha256) and signed by QMOI signing key. The icon manager verifies checksum before replacing local files.

Where icons are used

- App launcher and installer
- Notification/Tray icons
- Website favicons and PWA manifests
- Mobile adaptive icons and home screen shortcuts

How QMOI updates icons

1. Automation agent checks remote manifest
2. Downloads new icons to a staging area
3. Verifies signature and checksum
4. Atomically swaps files and updates platform caches
5. Logs the update and alerts master if any step fails

See also

- ALLDEVICESSETTINGS.md (device-specific icon settings)
- BUILDAPPSFORALLPLATFORMS.md (integration into build pipelines)
- QMOINGROK.md (icon downloads via tunnel/CDN if needed)

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/QMOIICONS.md",
"validated_at": "2025-10-26T20:51:24.783458Z",
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
