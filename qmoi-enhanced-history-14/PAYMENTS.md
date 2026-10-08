---
title: "PAYMENTS"
qmoi_validation_frontmatter: true
---

# PAYMENTS

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

PAYMENTS.md

This file documents the payment integration plan for QMOI.

## Overview

QMOI currently uses a local SQLite-backed `wallets` table to simulate balances
(`balance_cents` stored as integers). Deals purchase flow debits the user's
wallet and credits the `cashon` system wallet. To handle "real actual cash"
we must integrate with one or more payment providers and implement webhooks,
settlements, and reconciliation.

## Recommended next steps

1. Provider selection
   - For card-based payments and global support: Stripe (recommended)
   - For mobile-money in East Africa: M-Pesa (Safaricom) or local provider
   - For bank transfers: integrate a local bank API or a payments aggregator

2. Credentials & secrets
   - Store provider keys in environment variables (e.g., STRIPE_API_KEY)
   - Ensure production uses a secrets manager and TLS for webhooks

3. Adapter pattern
   - Implement a payments adapter per provider (see `payments/provider_stub.py`)
   - Adapters must implement create_charge(username, amount_cents, currency)
   - Add webhook endpoints to receive provider events and mark transactions
     settled/failed

4. Ledger & reconciliation
   - Add a `transactions` table (done) to track provider status and refs
   - Implement periodic reconciliation job to re-query provider for unsettled
     transactions

5. Production durability
   - Move from SQLite to PostgreSQL for transactional integrity under load
   - Add idempotency keys for charge creation
   - Add audit logging and receipts

## Testing

- `scripts/test_payments.py` demonstrates a simulated charge using the
  provider stub and verifies a transaction is created and marked settled.

## Security

- Do not commit provider secrets. Use environment variables and a secrets
  manager. Verify webhook signatures before accepting events.

## Notes

The current implementation auto-settles transactions when no external provider
is configured (useful for offline/testing)."}

<!-- QMOI_VALIDATION_START -->

{
"file": "PAYMENTS.md",
"validated_at": "2025-10-26T20:51:22.331115Z",
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
