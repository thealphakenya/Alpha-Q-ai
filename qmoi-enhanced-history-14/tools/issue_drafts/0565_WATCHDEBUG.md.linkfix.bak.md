---
title: "Issue draft for WATCHDEBUG.md.linkfix.bak"
generated: 2025-11-08T16:06:38.355150Z
---

# Review needed: WATCHDEBUG.md.linkfix.bak

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:41.785487Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:41.785487Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:41.785487Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
---
title: "WATCHDEBUG.md - QMOI Comprehensive Monitoring & Error Fixing System"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->
## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# WATCHDEBUG.md - QMOI Comprehensive Monitoring & Error Fixing System

## Overview
WATCHDEBUG.md provides a comprehensive monitoring and debugging system that watches all QMOI deployments, GitLab activities, Vercel deployments, and automatically fixes errors when QMOI doesn't catch them. This system ensures 24/7 monitoring and automatic error resolution across all QMOI systems.

## Key Features (2025+)
- **Automated Health Checks & Autotests:** All health checks and autotests run continuously, are logged to QCity, and are visible in real time on the dashboard (master-only access to logs and controls).
- **Self-Healing & Error-Free Downloads:** App downloads are only enabled if all health checks and autotests pass. Apps are always up to date, error-free, and auto-updating after install.
- **Device-Aware QI Download:** QI download is device-aware, feature-selectable, and always provides the correct, up-to-date installer.
- **Expanded Platform Stats:** Dashboard now shows status for GitLab, GitHub, Vercel, Gitpod, Netlify, HuggingFace, Quantum, Village, Azure, AWS, GCP, DigitalOcean, and more, each with icons and names.
- **Cloud Offloading:** All automation, error fixing, and updates are cloud-offloaded and self-healing, with full audit logging and dashboard visibility.
- **Master-Only Controls:** Advanced dashboard features, logs, and controls are only visible to master/master users.
- **All .md docs are always up to date and reflect the latest automation and monitoring enhancements.**

## Monitoring Components

### 1. GitLab Monitoring
- Pipeline status and progress
- Job execution and completion
- Error detection and logging
- Automatic error f
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
