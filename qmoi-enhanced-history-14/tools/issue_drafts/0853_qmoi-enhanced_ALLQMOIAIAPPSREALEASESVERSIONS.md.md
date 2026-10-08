---
title: "Issue draft for qmoi-enhanced/ALLQMOIAIAPPSREALEASESVERSIONS.md"
generated: 2025-11-08T16:06:38.724178Z
---

# Review needed: qmoi-enhanced/ALLQMOIAIAPPSREALEASESVERSIONS.md

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:41.981041Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:41.981041Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:41.981041Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
---
title: "QMOI AI Apps - All Releases & Versions"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->
## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI AI Apps - All Releases & Versions

## PWA (Progressive Web App) Status
| App Name   | Platform      | Version   | PWA Link                                         | Status   |
|------------|--------------|-----------|--------------------------------------------------|----------|
| QCity      | Web (PWA)    | v2.0.1    | https://qcity.qmoi.app/                          | ✅        |
| QMOI Space | Web (PWA)    | v1.2.3    | https://space.qmoi.app/                          | ✅        |

> PWAs for QCity and QMOI Space are always up-to-date, autotested, and cloud-offloaded for unlimited usage, even in Codespaces or low-resource environments.

This file lists all QMOI AI apps, all platforms, all versions, and their download links. It is auto-updated by QCity runners. All links are autotested and always up-to-date.

> **Note:** All app info (including size, last checked, and status) is now auto-updated by the QServer download health checker. The table below is always up-to-date and precise.

| App Name   | Platform      | Version   | Download Link                                      | Status   |
|-----------|---------------|-----------|----------------------------------------------------|----------|
| QMOI AI   | Windows       | v1.2.3    | https://github.com/thealphakenya/qmoi-enhanced/releases/qmoi/windows.exe        | ✅       |
| QMOI AI   | Mac           | v1.2.3    | https://github.com/thealphakenya/qmoi-enhanced/releases/qmoi/mac.dmg            | ✅       |
| QMOI AI   | Linux (DEB)   | v1.2.3    | https://github.com/thealphakenya/qmoi-enhanced/releases/qmoi/linux.deb          | ✅       |
| QMOI AI   | Linux (AppImage) | v1.2.3 | https://github.com/thealphakenya/qmoi-enhanced/releases/qmoi/linux.appimage     | ✅       |
| QMOI AI   | Android       | v1.2.3    | https://downloads.
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
