---
title: "Release Automation — QMOI"
qmoi_validation_frontmatter: true
---

# Release Automation — QMOI

This document explains the release automation system in this repository and how QMOI and LION coordinate to produce safe, auditable releases.

Overview

- `scripts/release_automation.py` — produces release proposals from validated build artifacts and can publish to GitHub when credentials are available.
- `scripts/validate_builds.py` — validates artifact presence for discovered apps.
- `.qmoi_validation/releases_proposals/` — stores generated proposals for review.
- `.qmoi_validation/auto_env.json` — default non-sensitive config; may be overridden by `.env` files or environment variables.

Design principles

- Non-destructive by default: scripts write proposals and patches to `.qmoi_validation/` for human or CI review rather than pushing changes automatically.
- Multi-source configuration: credentials and settings are discovered from (in order): environment variables, `.env` at repo root, `.qmoi_validation/.env`, and `.qmoi_validation/auto_env.json`.
- Safe publishing: publishing requires a valid `GITHUB_TOKEN` and `GITHUB_REPO`. To avoid accidental billing or storage use, uploading large binary assets is gated and opt-in.
- LION orchestration: validators and fixers emit LION task stubs under `.qmoi_validation/lion_tasks/`. `scripts/lion_orchestrator.py` will process those tasks and create PR proposals and todo items.

Quick run

1. Run validations and create proposals locally:

```bash
python3 scripts/generate_allmdrefs.py --write
python3 scripts/validate_md.py
python3 scripts/validate_builds.py
python3 scripts/release_automation.py
```

2. Review `.qmoi_validation/releases_proposals/` and `.qmoi_validation/pr_proposals/`.

3. To publish programmatically (CI), provide `GITHUB_TOKEN` and `GITHUB_REPO` (owner/repo) as CI secrets. Set `AUTO_PUBLISH=true` only in a guarded workflow and on protected branches.

CI workflow

- The repository includes `.github/workflows/qmoi-autodev.yml` which runs discovery, validations and LION orchestration on push to the protected autosync branch and via manual dispatch. It generates proposals and does not publish releases automatically.

Extensibility

- To enable automatic uploads and publishing in CI, extend `scripts/release_automation.py` to implement the upload flow using the `upload_url` returned by the Releases API. Always gate uploads behind `MAX_UPLOAD_MB` limits and explicit `--upload` flags.

Security

- Never commit valid tokens into the repo. Use GitHub Actions secrets or an encrypted store. The `auto_env.json` file is intentionally seeded with empty tokens.

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
