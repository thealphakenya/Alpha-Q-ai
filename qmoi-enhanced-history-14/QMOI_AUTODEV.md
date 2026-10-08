---
title: "QMOI Autodev & UI Auto-update (Design + Implementation Notes)"
qmoi_validation_frontmatter: true
---

# QMOI Autodev & UI Auto-update (Design + Implementation Notes)

This document describes a safe, auditable autodev/autoupdate flow for QMOI that
enables automated UI updates and platform changes after automated testing and
validation steps.

Goals

- Allow QMOI to propose UI updates (new components, color/theme changes,
  layout tweaks) and automatically roll them out to monitored environments once
  they pass automated verification.
- Keep the master user in control: UI preview and release rollouts should be
  gated by 'master' approvals and automated safety checks.
- Minimize device data usage by delivering updates as small deltas and
  deferring heavy assets to qcity/cloud resources.

Core components

- Autotest pipeline — runs unit/integration/ui tests (automated): existing
  `tools/autotest_runner.py` can orchestrate initial checks.
- Validation layer — linting, accessibility checks, snapshot tests.
- Delta packager — create small patch bundles (CSS/JS/JSON) and signature.
- Canary & rollout controller — deploy to a small group (qcity edge nodes or
  device testers) before global rollout.
- Audit & rollback — keep change logs, perform automated rollback on errors.

UI Auto-update flow (safe, short)

1. QMOI generates a proposed change (UI component, theme, text) and stores it
   as a draft artifact in the repository or artifact store (e.g. `releases/`).
2. Autotest pipeline runs: unit tests, accessibility, visual diff snapshots.
3. If all checks pass, the delta packager produces a signed patch.
4. Canary rollout to designated qcity edge servers and a small number of
   devices with automatic monitoring.
5. After a successful canary window, the master UI dashboard shows a one-click
   promote option for full rollout; if configured, QMOI can auto-promote.

Security & Safety

- All patches are signed; devices verify signature before applying.
- Rollout uses feature flags so changes can be toggled per region/device.
- Master-only privileged endpoints exist for full rollout and master preview.

Integration points

- `ALLVERSIONS.md` — list UI versions and artifacts for download.
- `tools/autotest_runner.py` — integrate test results into release decisions.
- `tools/check_links.py` — validate docs links during the pipeline.

Next steps (implementation tasks)

- Add delta packager and signature verification helper.
- Wire autotest runner to produce a machine-readable status for CI.
- Implement canary rollout controller (prototype as scripts) and add audit logs.

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
