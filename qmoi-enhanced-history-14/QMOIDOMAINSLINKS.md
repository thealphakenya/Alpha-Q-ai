---
title: "QMOIDOMAINSLINKS.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

## Enhanced System-Wide Link & Domain Automation

- QMOI now automatically searches for all links and domains in the entire system, updating this file in real time.
- All links and domains are autotested, auto-fixed, and instantly updated for every app, platform, and service.
- QMOI handles all DNS, hosting, tunnel, and fallback logic, ensuring permanent operation and instant recovery from any issue.
- QMOIDOMAINSLINKS.md is always up to date, with all changes logged and visible in the QCity dashboard.

# QMOIDOMAINSLINKS.md

This file contains all domains and links used in the QMOI system, including their details, usage, and real-time status. It is auto-updated by QMOI automation scripts to ensure all domains and links are valid and working.

## Automated DNS Self-Healing & Link Tracking

- QMOI now automatically detects DNS issues for any link or domain, attempts to fix them (ngrok fallback, auto-register/host new domain), and retests until resolved.
- All DNS health, link status, fallback, and auto-fix history are tracked in LINKSTRACKS.md, updated in real time.
- Central TRACKS_DICTIONARY.json is used for all tracks and link features, referenced by TRACKS.md and LINKSTRACKS.md.

## Domains & Links

| Domain             | Link                                                    | Status | Usage           | Last Checked | Platform | Notes                     |
| ------------------ | ------------------------------------------------------- | ------ | --------------- | ------------ | -------- | ------------------------- |
| qmoisystem.com     | https://qmoisystem.com                                  | ✅     | Main QMOI site  | 2025-10-11   | All      | Production, auto-hosted   |
| downloads.qmoi.app | https://github.com/thealphakenya/qmoi-enhanced/releases | ✅     | App downloads   | 2025-10-11   | All      | CDN, auto-updated         |
| qcity.qmoi.app     | https://qcity.qmoi.app                                  | ✅     | QCity dashboard | 2025-10-11   | Web      | Auto-hosted, always-on    |
| api.qmoi.app       | https://api.qmoi.app                                    | ✅     | QMOI API        | 2025-10-11   | All      | API, auto-tested          |
| ngrok.io           | https://ngrok.io                                        | ✅     | Tunnel fallback | 2025-10-11   | All      | Used if main domains fail |

## Features

- All domains and links are auto-checked and updated in real time by QMOI automation scripts.
- If any link fails, QMOI will immediately attempt to fix it using ngrok, alternate providers, or auto-register and host a new domain.
- QMOI can automatically register domains, set up hosting, and configure tunnels (ngrok, Cloudflare, etc.) for QCity and all apps, with no human intervention.
- All links are autotested for validity and usage; broken links are auto-fixed or replaced using fallback (ngrok, alternate providers).
- Usage and platform details are tracked for every domain, including last checked date and status.
- QMOI ensures all download links are valid and working for every app/platform, and auto-fixes any issues detected.
- QMOI runs periodic autotests to verify all links and domains, updating this file in real time with the latest working links and details.
- All enhancements are fully automated and self-healing, ensuring QMOI links and domains always work for all users and platforms.

- All domains and links are auto-checked and updated in real time by QMOI automation scripts.
- QMOI can register, host, and update domains automatically using any provider (Freenom, Namecheap, GoDaddy, etc.), with no human intervention required.
- All links are tested for validity and usage; broken links are auto-fixed or replaced using fallback (ngrok, alternate providers).
- Usage and platform details are tracked for every domain, including last checked date and status.
- This file is referenced in ALLMDFILESREFS.md and auto-updated in real time.
- QMOI ensures all download links are valid and working for every app/platform, and auto-fixes any issues detected.

<!-- QMOI_VALIDATION_START -->

{
"file": "QMOIDOMAINSLINKS.md",
"validated_at": "2025-10-26T20:51:22.498296Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOIDOMAINSLINKS.md"
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
