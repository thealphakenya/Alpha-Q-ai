---
title: "lion-plugin"
qmoi_validation_frontmatter: true
---

# lion-plugin

Description

- A developer-focused distribution that provides plugin SDKs and scaffolding for writing LION handlers.

Key features

- Plugin templates, linters, and test harnesses
- Local dev server for quick iteration

Release & packaging

- Distributed as a Python package and a ZIP containing templates. Published to GitHub releases and PyPI.

# LION-Plugin (Extensibility SDK)

Purpose

- A plugin/SDK distribution enabling third-parties to write plugins and handlers that run inside the LION orchestrator.

Key features

- Stable plugin API, versioned SDK, examples, templates, secure sandboxing recommendations.

Target platforms

- Python packages for plugin authors; optionally npm bindings for UI plugins.

Packaging

- Python package `lion-plugin-sdk` with typed stubs and examples; templates to scaffold new handlers.

Release artifacts

- `lion-plugin-sdk-vX.Y.Z.tar.gz` and PyPI package.

Auto-update strategy

- Plugin authors publish to PyPI/npm; LION-Cloud/LION-OS can fetch and validate plugin signatures.

Monetization

- Marketplace for paid plugins, revenue share with plugin authors.

Integration with QMOI

- Plugins gain access to QVS read-only APIs and core orchestrator hooks through an explicit capability grant.

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
