---
title: "Issue draft for docs/LIONVARIATIONS.md"
generated: 2025-11-08T16:06:38.368731Z
---

# Review needed: docs/LIONVARIATIONS.md

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:41.800030Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:41.800030Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:41.800030Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
---
title: "LION Variations — Overview"
qmoi_validation_frontmatter: true
---

# LION Variations — Overview

This document catalogs the official LION (LION = Large Intelligent Orchestration Network) variations used across QMOI. Each variation is a focused distribution or product built from the same core orchestrator/agents, optimized for different platforms and use-cases. Variations are treated as first-class artifacts and follow an automated build/release workflow.

Core goals for variations
- Consistent naming and metadata
- Automated builds, releases and platform packaging
- Lightweight per-variation docs describing features, platforms and revenue models
- Auto-updates and continuous development (CI-driven)

Variations included in this repository (each has a dedicated spec under `docs/lion_variations/`):

1. lion-core — The canonical orchestrator and core libraries (Python). Suitable for servers and development.
2. lion-agent — Lightweight agent runtime for edge devices (Python/Node builds).
3. lion-os — A minimal operating-system-style appliance image (Docker/OCI) for deployment as a VM/container.
4. lion-plugin — Plugin SDK and curated plugin distribution (node/npm and python packages).
5. lion-extension — Browser/IDE extensions that integrate LION proposals and insights into developer tools.
6. lio (mobile) — Mobile-focused variant (Android/iOS packaging guidance, AAB/IPA artifacts) for on-device agents.
7. lion-cloud — Cloud-native orchestrator distribution with Kubernetes manifests, autoscaling and monitoring presets.

New variations can be added by creating a spec file in `docs/lion_variations/` and declaring the variation name in `scripts/release_helper.py`.

Releases and automation
- Variations are packaged and published automatically when a tag `variation/<name>/vX.Y.Z` or `variation-<name>-vX.Y.Z` is pushed.
- GitHub Actions workflow `.github/workflows/auto_release.yml` handles building artifacts, creating a GitHub Release, and uploading assets.

How variations are used in QMOI
- Each variation maps
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
