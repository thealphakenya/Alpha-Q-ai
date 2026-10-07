---
title: "WhatsApp Qmoi Bot"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->
## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# WhatsApp Qmoi Bot

## Overview
A WhatsApp automation bot powered by Qmoi AI, using Baileys for WhatsApp Web integration. Supports messaging, media, group management, broadcasting, and advanced AI features.

## Features
- Persistent WhatsApp session (auth.json)
- Master/sister onboarding via QR code
- AI-powered replies, media, and group actions
- Broadcast and scheduled campaigns
- Secure, encrypted data handling
- Runs 24/7 in Colab, Docker, or cloud

## Setup
1. Install dependencies: `npm install @whiskeysockets/baileys @hapi/boom axios`
2. Run `node index.js` to start the bot and scan the QR code with your WhatsApp (Linked Devices)
3. The bot will stay online and use Qmoi for all intelligence

## Folder Structure
- `index.js` - Main bot logic
- `handlers/` - Text, media, group handlers
- `services/` - Qmoi AI connector
- `utils/` - Delay, broadcast, and helper utilities

## Security
- All sensitive data is encrypted
- No real data is exposed in exports or unzipped builds

## Extending
- Add new handlers for calls, video, or custom features
- Integrate with Qmoi for animation/game generation, subtitles, and more

## 2025-06-13: WhatsApp Qmoi Bot Handlers & Security
- Handlers for calls, video, voice, vision, subtitles, downloads, notifications, marketing, projects, app download, secure data, scheduling, and animation/game generation.
- All handlers use Qmoi for intelligence and are fully integrated with the WhatsApp bot.
- Data encryption for all sensitive information.

## 2025-06-13: Wallet, Child-Friendly, and Robust AI Features
- WhatsApp Qmoi Bot now supports wallet automation, child-friendly features (music, stories, conversations), and robust, thorough, and fast AI task handling.

---

<!-- QMOI_VALIDATION_START -->
{
  "file": "whatsapp-qmoi-bot/README.md",
  "validated_at": "2025-10-26T20:51:24.878537Z",
  "validator": "QMOI Lion (automated)",
  "checks": [
    {
      "name": "title_present",
      "ok": true,
      "detail": "WhatsApp Qmoi Bot"
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
