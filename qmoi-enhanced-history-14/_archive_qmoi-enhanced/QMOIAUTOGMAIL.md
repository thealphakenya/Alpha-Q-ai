---
title: "QMOI Automated Gmail Notification System"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI Automated Gmail Notification System

## Overview

QMOI provides a fully automated Gmail notification system for all automation, error fixing, deployments, and platform events. Notifications are sent in real time to all configured recipients, even when running in the cloud (Colab, Dagshub, QCity, etc.).

## Features

- **Automated Email Alerts:** Receive notifications for doc fixing, deployments, errors, and more.
- **Multiple Recipients:** Supports comma-separated recipient list (e.g., rovicviccy@gmail.com,qmoi@gmail.com).
- **Secure Credential Management:** QMOI auto-manages Gmail credentials using environment variables. Never expose secrets in public repos.
- **Cloud-Ready:** Works in Colab, Dagshub, and other cloud environments for always-on notifications.
- **Parallel Integration:** Tightly integrated with QMOI's parallel engine for real-time, platform-specific alerts.
- **Lightweight:** Designed to be resource-efficient and not slow down or hang devices.

## Setup

1. **Set Environment Variables:**
   - `GMAIL_USER`: Your Gmail address (e.g., rovicviccy@gmail.com)
   - `GMAIL_PASS`: Gmail App Password (never your main password)
   - `GMAIL_RECIPIENT`: Comma-separated list of recipients
2. **Security:**
   - Use Gmail App Passwords for automation.
   - Never commit secrets to public repositories.
   - For production/cloud, use a secrets manager or environment variable injection.
3. **Cloud/Always-On:**
   - QMOI can run in Colab, Dagshub, or any always-on environment for 24/7 notifications.
   - Notifications are sent even if your local device is offline or powered off.

## Best Practices

- Rotate app passwords regularly.
- Use a secrets manager for production.
- Monitor notification logs for delivery status.
- Add/Remove recipients as needed in the `GMAIL_RECIPIENT` variable.

## Integration with QMOI Parallel Engine

- All parallel jobs (error fixing, deployments, etc.) trigger notifications independently.
- Platform-specific alerts are sent for GitLab, GitHub, Vercel, HuggingFace, and more.
- Notifications are categorized by event type and platform for clarity.

## 📊 Dashboard Integration for Notifications

- The QMOI dashboard (`python scripts/qmoi-dashboard.py`) now displays Gmail and multi-channel notification status, delivery logs, and allows master users to trigger test notifications.
- All notification events (success, failure, delivery, etc.) are visualized and logged in real time in the dashboard.
- Notification analytics and history are available alongside automation logs and reports.
- This integration is always-on, cloud-offloaded, and works in Colab, Dagshub, and all cloud environments.

---

**QMOI Automated Gmail Notification System**

- Always-on, secure, and fully integrated with QMOI's automation and parallel processing.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/QMOIAUTOGMAIL.md",
"validated_at": "2025-10-26T20:51:24.738150Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI Automated Gmail Notification System"
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
