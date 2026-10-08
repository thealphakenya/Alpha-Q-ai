---
title: "QMOIDNS"
qmoi_validation_frontmatter: true
---

# QMOIDNS

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

QMOIDNS.md
QMOI DNS & Tunnel Management Automation System
The QMOI DNS system manages and automates the full lifecycle of DNS and ngrok tunnel configurations to ensure high availability, instant failover, and secure delivery of all QMOI downloads and services.

🌐 Core Features
Feature Description
🔁 Automated DNS & Tunnel Checks QMOI continuously monitors all critical DNS records and ngrok tunnel endpoints.
🛠 Auto-Setup & Repair Automatically sets or repairs A, CNAME, TXT, and other records when missing/misconfigured.
🚨 Auto-Fix Routine On failure, QMOI triggers a self-healing routine and logs all diagnostics.
🌍 Fallback Switching Seamless failover to zero-rated CDN or ngrok (see ZERORATEDQMOI.md & QMOINGROK.md) when primary DNS fails.
📊 Dashboard Integration Master/admins can view real-time DNS/tunnel health, trigger manual repairs, and view logs via the QCity dashboard.
🤖 Fully Automated No manual steps required — all checks, repairs, updates, and fallbacks are hands-free.
🪵 Audit Logging Every DNS/tunnel event (check, fix, failover) is logged for traceability.

🔌 API & UI Integration
Endpoint Purpose
GET /api/qcity/dns-health Returns DNS status for all configured domains
GET /api/qcity/ngrok-health Returns ngrok tunnel status
POST /api/qcity/dns-fix Manually triggers DNS reconfiguration (master-only)
POST /api/qcity/ngrok-fix Manually restarts ngrok tunnels (master-only)

✅ All endpoints require API key authentication.

📍 QCity Panel includes a visual dashboard for:

Real-time health metrics

Manual override buttons

Activity & diagnostic logs

🔄 GitLab/CI Integration
DNS/tunnel checks and auto-fixes are run before deployments or builds in .gitlab-ci.yml or CI runners:

yaml
Copy
Edit
before_script:

- python scripts/check_dns_and_ngrok.py
  If a failure is detected:

Tunnel is restarted

DNS is re-provisioned

Links are updated before continuing

⚡ Ngrok Tunnel Automation
Feature Description
🟢 Auto-Start QMOI starts tunnels as needed for any service
🔁 Auto-Rotation If a tunnel fails, a new one is spun up and all links are updated
🔄 Download Link Injection UI, API, Markdown, and config files get updated dynamically
🧪 Health Monitoring Tunnel health is checked every minute
📢 Notification Admins are notified of changes/failovers
🪵 Logging All tunnel lifecycle events are fully logged

🔁 Tunnel Failover Flow
text
Copy
Edit

1. Detect tunnel or domain failure
2. Restart ngrok tunnel or fix DNS via API
3. Update all affected links (UI, .md, JSON)
4. Notify admins via QCity dashboard
5. Monitor tunnel every 60 seconds
   🔗 Integration Points
   This DNS and tunnel automation system integrates with:

QMOIBROWSER.md

QCITYRUNNERSENGINE.md

QMOIQCITYAUTOMATIC.md

QMOINGROK.md

ZERORATEDQMOI.md

🌍 Multi-Provider & Self-Hosted Domain Support
QMOI supports automated DNS across:

Provider Method
🆓 Freenom Browser automation
🌐 Cloudflare API
🏢 Namecheap API or Selenium
☁️ AWS Route 53 Boto3-based automation
🔐 Self-Hosted BIND CLI + Python wrapper
🔄 Ngrok pyngrok integration
🧠 QMOI Internal Domains Dynamically generated and self-managed

All actions are:

Logged in dns-tunnel-activity.log

Viewable in QCity dashboard

Recoverable (automated backup of records)

✅ Summary
Feature Description
🌐 DNS Automation Auto-check, auto-fix for A/CNAME/TXT records
⚙ Tunnel Management Start/stop/reconnect ngrok tunnels dynamically
🔁 Fallback Switching Seamless switch to working domain or tunnel
📊 CI Integration Ensures working DNS before deployment
📋 UI Controls Admins manage everything from QCity
🪵 Full Audit Logging Every step logged with timestamp & status
🔐 Multi-Provider Support Freenom, Cloudflare, AWS, GoDaddy, etc.
☁️ Zero-downtime Updates Real-time link rewriting and propagation

📄 This file is maintained by QMOI Orchestrator Engine and reflects the current DNS and tunnel management state of all QMOI services. For more info, see QMOIDOMAINS.md and QMOINGROK.md.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/QMOIDNS.md",
"validated_at": "2025-10-26T20:51:24.762052Z",
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
