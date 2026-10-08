# QMOI WhatsApp Browser Login Page

This page describes how to log QMOI into WhatsApp using the official WhatsApp Web login, including all intended UI features and usage instructions.

---

## How to Log QMOI into WhatsApp

1. **Open the QMOI WhatsApp Login Page**
   - The page opens WhatsApp Web in a new window/tab: [https://web.whatsapp.com/](https://web.whatsapp.com/)
2. **Scan the QR Code**
   - Use your WhatsApp mobile app to scan the QR code displayed on the page.
   - Go to WhatsApp > Menu > Linked Devices > Link a Device.
3. **Successful Login**
   - Once scanned, QMOI will be logged in and can use the WhatsApp account for all intended automation and messaging features.

---

## Intended UI Features

- **QR Code Section:**
  - Prominently displays the WhatsApp QR code for easy scanning.
- **Status Indicator:**
  - Shows connection status ("Waiting for scan", "Connected", "Disconnected").
- **Instructions Panel:**
  - Step-by-step guide for linking the device.
- **Session Management:**
  - Option to log out, refresh QR, or switch accounts.
- **Security Notice:**
  - Reminds users to only scan with trusted devices.
- **QMOI Integration Panel:**
  - Shows QMOI's WhatsApp automation status (active, idle, error).
- **Help/Support Link:**
  - Quick access to troubleshooting and support resources.

---

## Features QMOI Can Use After Login

- Send and receive WhatsApp messages
- Join and manage groups
- Send media, files, and documents
- Automate responses and workflows
- Monitor chats and trigger QMOI actions
- Log out or switch WhatsApp accounts

---

## Troubleshooting

- If the QR code does not load, refresh the page.
- If login fails, ensure your phone has internet and try again.
- For persistent issues, consult the QMOI WhatsApp integration documentation or support.

---

_Last updated: 2025-11-23_

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
