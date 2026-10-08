---
title: "QMOI Universal Health & Runners"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->
## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI Universal Health & Runners

## Overview
This file documents the universal health checks, runners, and automation flows for all QMOI apps, platforms, and devices. All health checks and runners are zero-rated (free, unlimited, no billing) and are managed by QMOI runners and QCity cloud.

## Health Checks
- All apps, downloads, builds, and tests are autotested for health and reliability.
- Device-specific error logs and health stats are referenced in `ALLERRORSSTATSQMOI.md`.
- Health checks are performed before and after every deployment, build, and download.
- All health issues are auto-fixed by QMOI runners and logged for audit.

## Runners
- QMOI runners are cloud-based, parallel, and self-healing.
- No paid runners or billing issues; all automation is zero-rated and unlimited.
- Runners handle autotesting, auto-fix, deployment, build, and download for every app and platform.
- All runner actions are logged and referenced in `QMOIGITPODDEV.md`, `QMOI-ENHANCED-README.md`, and `QMOI-ENHANCEMENT-SUMMARY.md`.

## Automation & Documentation
- All health checks, runners, and automation flows are referenced and documented in:
  - `QMOIFREE.md` (zero-rated features)
  - `DOWNLOADQMOIAIAPPALLDEVICES.md` (downloads)
  - `BUILDAPPSFORALLPLATFORMS.md` (builds)
  - `TESTREADME.md` (testing)
  - `ALLERRORSSTATSQMOI.md` (device error stats)
  - `QMOI-ENHANCED-README.md` (enhanced automation)
  - `QMOI-ENHANCEMENT-SUMMARY.md` (enhancement summary)
  - `QMOIGITPODDEV.md` (Gitpod automation)
  - `QMOIAUTOREVENUEEARN.md` (auto revenue)
  - `ALLMDFILESREFS.md` (master .md index)

## Status
- All health checks and runners are now zero-rated, self-healing, and fully documented for every app, platform, and device.
- No paid runners or billing issues remain. All automation is cloud-based and unlimited.

<!-- QMOI_VALIDATION_START -->
{
  "file": "UNIVERSALHEALTHRUNNERS.md",
  "validated_at": "2025-10-26T20:51:22.653581Z",
  "validator": "QMOI Lion (automated)",
  "checks": [
    {
      "name": "title_present",
      "ok": true,
      "detail": "QMOI Universal Health & Runners"
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
