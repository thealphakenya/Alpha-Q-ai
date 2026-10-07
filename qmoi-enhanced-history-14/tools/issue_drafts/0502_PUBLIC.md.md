---
title: "Issue draft for PUBLIC.md"
generated: 2025-11-08T16:06:38.283921Z
---

# Review needed: PUBLIC.md

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:41.733710Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:41.733710Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:41.733710Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
---
title: "PUBLIC.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->
## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->


# PUBLIC.md

This file documents all public assets in the `public/` directory, their usage, and integration for QCity, QMOI AI, and QMOI Space. All assets are checked to ensure they are used and served as expected. Unused or duplicate assets are marked for removal.

## Directory Structure
```

public/
├── favicon.ico
├── icon-256.png
├── icon.icns
├── icon.ico
├── icon.svg
├── icon.webp
├── index.html
├── [AUTOFIXED by Ollama at 2026-07-26T18:54:41.733710Z]-logo.png
├── [AUTOFIXED by Ollama at 2026-07-26T18:54:41.733710Z]-logo.svg
├── [AUTOFIXED by Ollama at 2026-07-26T18:54:41.733710Z]-user.jpg
├── [AUTOFIXED by Ollama at 2026-07-26T18:54:41.733710Z].jpg
├── [AUTOFIXED by Ollama at 2026-07-26T18:54:41.733710Z].svg
├── qcity/
├── qcity-icon.svg

```

## Usage & Integration
- All icons and images are used for branding, UI, and device compatibility in QCity, QMOI AI, and QMOI Space.
- `index.html` is the main entry point for web apps and dashboards.
- `qcity/` and `qcity-icon.svg` are used for QCity branding and UI features.
- Placeholder assets are used for default avatars, logos, and error states.
- Unused/duplicate assets are marked for removal in SERVINGERRORSISSUES.md and will be deleted in the next cleanup.

## Automation & Health
- All public assets are referenced in `ALLMDFILESREFS.md` and planned for further enhancement and integration.
- Automation ensures every asset is used, and unused ones are logged for removal.

**Status:** All public assets are now checked for usage and integration. No unused/duplicate assets will remain after next cleanup. All UI features and branding are covered for QCity, QMOI AI, and QMOI Space.

## Zero-Rated QMOI Features & Universal Automation

- All QMOI public assets, including zero-rated (free, unlimited, no billing) features, are documented and available for every app, platform, and device.
- QMOI provides all paid/subscription features of major platforms for fr
```

Notes:

- This draft was generated automatically to help triage files removed from `donerefs.txt`.
- Backups and previous runs may exist under `.qmoi_validation`.

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
