---
title: "QMOIDOMAINS"
qmoi_validation_frontmatter: true
---

# QMOIDOMAINS

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

QMOIDOMAINS.md
QMOI Domains Management & Automation
This file documents how QMOI manages domains for downloads, cloud services, platform automation, and fallback recovery. QMOI dynamically integrates domain providers like Freenom, GoDaddy, Namecheap, Cloudflare, and auto-generates fallback tunnels using Ngrok.

🌐 Current Domain Inventory
Type Domains
✅ Primary Download Domain downloads.qmoi.app
🚨 Fallback Domain fallback.qmoi.app
🌍 Freenom Domains downloads-qmoi.tk, downloads-qmoi.ml, downloads-qmoi.ga, downloads-qmoi.cf, downloads-qmoi.gq
⚡ Ngrok Tunnels Auto-generated, live, and updated in QMOINGROK.md
🔧 Self-Registered Domains Dynamically created and managed by QMOI
📱 App/Platform-specific Links Auto-generated for: WhatsApp, Telegram, QCity bots, Android installs, Colab notebooks

🤖 Automation & Management
Capability Description
🛠 Domain Creation Uses browser automation (Selenium) and/or APIs (Freenom, Namecheap, etc.)
🔁 Auto-Rotation If any domain or tunnel fails, QMOI rotates to the next available
🧠 Smart Prioritization Always uses the most stable, fastest, and lowest-latency link
🖥️ UI Management QCity dashboard allows authorized users to manage domains/tunnels
📋 Activity Logging All domain changes are timestamped and logged
🧩 Integration Fully integrates with QMOINGROK.md, QMOIDNS.md, and QMOIAUTODEV.md

🧪 Health Monitoring
QMOI runs periodic checks on all domain/tunnel endpoints:

If DNS is misconfigured → triggers fix or fallback

If HTTP ping fails → retries, logs, then rotates

If rate limits hit → auto-waits, or switches to mirror/tunnel

All health checks are logged with:

json
Copy
Edit
{
"domain": "downloads-qmoi.ga",
"status": "degraded",
"timestamp": "2025-07-23T21:55:01Z",
"recovery_action": "Switched to ngrok fallback"
}
🧪 Example: Freenom Automation
QMOI can:

Register a .tk or .ml domain (via browser automation or pre-authenticated API)

Set DNS records automatically

Map to a current ngrok or backend IP

Log the new domain and notify QCity dashboard

🔐 Domain Security Notes
Domain ownership credentials are stored securely (via .env, GCP Vault, AWS Secrets Manager, etc.)

Subdomain generation is automated, and cleanup occurs on every rotation

QMOI avoids exposing private/public keys directly in code or UI

🧩 API & UI Management
📡 QCity Domain API:
Endpoint Description
GET /api/qcity/domains Returns a list of current working domains and tunnels
POST /api/qcity/domains/add Adds a new custom domain
DELETE /api/qcity/domains/remove Removes a domain (master-only)

🔐 Requires master-level authentication

🧭 QCity Dashboard:
Visual domain health

Add/edit/remove domains

Audit logs

Tunnel status (see QMOINGROK.md)

📦 Domain Source Types
Source Managed By
🧪 Ngrok QMOI
🌍 Freenom QMOI
🏢 Namecheap Manual + QMOI
🧠 Self-hosted DNS QMOI
📦 Cloudflare API QMOI (if token provided)

✅ Summary
Feature Description
🌐 Domain Automation Auto-register + map domains to tunnels
🔁 Rotation Instant switch when domains fail
📊 Dashboard Control QCity panel for domain visibility
🔐 Secure Storage All keys/tokens managed securely
🛡️ Resilient Fallbacks Multi-layered: primary → Freenom → ngrok
📜 Audit Trail All changes are timestamped + logged

📄 This document is maintained by the QMOI master orchestrator. Refer to QMOINGROK.md for tunnel logic and QMOIDNS.md for DNS settings.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/QMOIDOMAINS.md",
"validated_at": "2025-10-26T20:51:24.763011Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": false,
"detail": "No H1 title found"
},
{
"name": "links",
"ok": true,
"detail": []
}
],
"passed": false,
"summary": {
"total_checks": 2,
"passed": false
}
}

<!-- QMOI_VALIDATION_END -->

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
