---
title: "ZERORATEDQMOI.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# ZERORATEDQMOI.md

## QMOI Zero-Rated Internet System

### Overview

QMOI Zero-Rated is a global, always-on internet fallback system that leverages zero-rated (free data) sites and services to ensure QMOI and QCity devices are always connected, regardless of location or network restrictions.

---

## 1. What is Zero-Rated QMOI?

- **Zero-Rated Sites:** Websites/services that are accessible without data charges (e.g., Wikipedia, Facebook Free Basics, WhatsApp, Google, select educational/government sites).
- **QMOI Zero-Rated Proxy:** QMOI can set up and manage a lightweight proxy/tunnel that routes essential traffic through zero-rated endpoints.
- **Global Fallback:** If all other connections fail, QMOI automatically switches to zero-rated mode to maintain connectivity.

---

## 2. How QMOI Sets Up and Uses Zero-Rated Internet

- **Auto-Detection:** QMOI continuously monitors connectivity and detects when only zero-rated access is available.
- **Proxy/Tunnel Setup:** QMOI can deploy a minimal web proxy or tunnel (e.g., using a cloud function, serverless, or a lightweight VPS) that mimics zero-rated traffic.
- **Dynamic Switching:** QMOI switches to zero-rated mode automatically and routes essential traffic (API, heartbeat, commands) through the proxy.
- **Global Coverage:** QMOI maintains a list of zero-rated endpoints for every region and can spin up new ones as needed.
- **Fallback Logic:** If a zero-rated site is blocked, QMOI tries the next available one, or sets up a new endpoint.

---

## 3. Technical Implementation

- **Zero-Rated Site List:** Maintained and updated regularly (Wikipedia, Facebook, WhatsApp, Google, YouTube, etc.).
- **Proxy Deployment:** QMOI can deploy a proxy on demand (e.g., using Heroku, Vercel, AWS Lambda, or a cheap VPS) to appear as a zero-rated service.
- **Traffic Shaping:** Only essential QMOI traffic is routed through the proxy to minimize detection and maximize reliability.
- **Auto-Testing:** QMOI tests all endpoints regularly and logs performance, switching as needed.
- **Security:** All traffic is encrypted and authenticated.

---

## 4. QCity UI Integration

- **Master Panel:**
  - Real-time status of zero-rated connectivity (active, fallback, last used, logs).
  - Controls to force zero-rated mode, test endpoints, and view logs.
  - Only visible to master users.
- **Settings (All Users):**
  - Option: "Always use QMOI Zero Rated for auto-connection" (toggle).
  - Description: "When enabled, QMOI will always attempt to use zero-rated internet for connectivity."
  - Status indicator: Shows if zero-rated mode is active.

---

## 5. Global Use Cases

- **Travel:** QMOI users can stay connected anywhere, even with no data plan.
- **Restricted Networks:** Bypass firewalls and data restrictions using zero-rated fallback.
- **Disaster Recovery:** Maintain connectivity during outages or emergencies.

---

## 6. Accountability & Reporting

- **Logs:** All zero-rated connections, switches, and failures are logged.
- **Reports:** Daily/weekly/monthly reports on zero-rated usage and performance.
- **Master Controls:** Only master users can view/export logs and force zero-rated mode.

---

## 7. Future Enhancements

- **AI Endpoint Selection:** Use AI to select the best zero-rated endpoint based on region and performance.
- **Community-Driven List:** Allow users to submit new zero-rated endpoints.
- **Integration with ISPs:** Work with ISPs to whitelist QMOI endpoints.

---

## DNS & Download Link Auto-Resolution

- **DNS Auto-Check & Fix:** QMOI Zero-Rated system now automatically checks and fixes DNS for all download links (downloads.qmoi.app). If DNS fails, it triggers an auto-fix routine, notifies master/master, and logs all actions.
- **Zero-Rated & Fallback Links:** If DNS cannot be fixed immediately, QMOI Zero-Rated system auto-switches to zero-rated or fallback CDN links to ensure downloads always work, even in restricted or offline environments.
- **Dashboard Integration:** Master can view DNS/link health and trigger manual checks from the dashboard.
- **Full Automation:** All DNS and link health checks, fixes, and fallback logic are fully automated and require no manual intervention.

---

_QMOI Zero-Rated: Always Connected, Anywhere, Anytime._

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/ZERORATEDQMOI.md",
"validated_at": "2025-10-26T20:51:24.851567Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "ZERORATEDQMOI.md"
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
