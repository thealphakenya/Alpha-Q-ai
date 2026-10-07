---
title: "QMOI Cloud Features"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI Cloud Features

## Overview

QCity and QMOI now support advanced, automated cloud integration for offloading, artifact sync, multi-device, and failover. All mobile builds, tests, and error-fixing can be offloaded to the cloud for maximum reliability and minimal device resource usage.

_Last updated: 2024-06-09_

## Key Cloud Features

- **Cloud Offloading:** All installs, builds, tests, and error-fixing (including mobile) can be run in the cloud/Colab, with results/artifacts synced back to your device.
- **Cloud Storage:** node_modules, build files, and caches are stored in cloud storage (S3, GCS, etc.) for fast recovery and multi-device use.
- **Multi-Device/Failover:** Multiple QCity cloud devices can work together, with automatic failover and load balancing.
- **Cloud-First Mode:** Option to run everything in the cloud, syncing only UI and results to your device.
- **Cloud Artifact Sync:** Syncs all important files between local and cloud for reliability and speed.
- **Mobile Cloud Builds:** Mobile app builds and tests are offloaded to the cloud when local resources are low, ensuring lightweight operation on all devices.
- **Continuous Self-Healing:** All errors (including in mobile, cloud, and CI/CD) are auto-fixed in the cloud, with master-only access to error/fix logs and controls.
- **Automated Last-Updated Dates:** Documentation and system UIs always show the real last update date.

## How to Use

- Configure cloud options in `config/qcity-device-config.json` and `config/qmoi_cloud_config.json`.
- Use dashboard to monitor cloud status, trigger offloading/sync, and view master-only error/fix logs.
- See `API.md` for cloud endpoints.
- Mobile automation: Use `node scripts/qmoi-mobile-auto-selfheal.js` to ensure mobile is always running, self-healing, and offloading to the cloud as needed.

## Automation Autotest

A new autotest script is available to verify that all QMOI automation scripts run successfully:

```sh
npm run qmoi:automation:autotest
```

- This will run all automation scripts in sequence and report any errors.
- If you see a missing script error, ensure you are running from the project root, not a subdirectory.

---

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/QMOI-CLOUD.md",
"validated_at": "2025-10-26T20:51:24.670834Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI Cloud Features"
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
