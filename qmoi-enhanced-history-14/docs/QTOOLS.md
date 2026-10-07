---
title: "QTOOLS"
qmoi_validation_frontmatter: true
---

# QTOOLS

## QMOI Tools & QTools — Overview

This document describes the enhanced toolchain (QTOOLS) used across the repository and how QMOI + LION orchestrate validation, builds, and releases.

Key improvements implemented:

- Auto env loading: tools now load non-sensitive defaults from `.qmoi_validation/auto_env.json` when environment variables are not provided. This allows the automation to propose, run and annotate flows even when CI secrets aren't set. Sensitive values (tokens) are intentionally left empty in the template and must be provided for publishing.
- Richer LION task stubs: validation and build tools now write LION task/event stubs with unique IDs, priority, recommended actions and `qcity_hints` to help orchestrators route remediation to QCity resources.
- Conservative publish: release automation will only create release proposals by default. Publishing requires `GITHUB_TOKEN` or an explicit configuration in `.qmoi_validation/auto_env.json` and remains opt-in.

Files of interest

- `scripts/validate_md.py` — markdown validation, history, LION stubs.
- `scripts/validate_builds.py` — artifact checks and remediation tasks.
- `scripts/release_automation.py` — proposal generation and optional publish.
- `.qmoi_validation/auto_env.json` — defaults and non-sensitive configuration.

Autodev behavior (how QMOI operates automatically)

- Discovery: runs `generate_allmdrefs.py` to keep `ALLMDFILESREFS.md` current.
- Validation: runs `validate_md.py` (dry-run), produces per-file reports and LION tasks for failures.
- Build checks: runs `validate_builds.py`, produces build reports and remediation tasks.
- Release: runs `release_automation.py` to create proposals; will only publish when authorized.

Safety and billing

- QMOI will not create cloud resources or enable billable services automatically. Any cloud-specific provisioning is recorded in `qcity_hints` and left for a human or a guarded CI workflow with explicit credentials.
- Uploading large binaries to third-party services is always gated behind explicit `--upload` flags and available credentials. This avoids accidental GitHub storage/bandwidth costs.

Extending QTOOLS

- To add a new validator, create a script under `scripts/` that follows the pattern: write JSON reports into `.qmoi_validation/`, and emit LION stubs into `.qmoi_validation/lion_tasks/`.
- Use `AUTO_ENV` values in scripts to pick reasonable defaults.

---

Add this file to `ALLMDFILESREFS.md` via generator.

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
