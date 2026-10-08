---
title: "PLATFORM AUTOMATION"
qmoi_validation_frontmatter: true
---

# PLATFORM AUTOMATION

Platform Automation & Safety Guidelines

This document explains how QMOI should interact with external platforms in production.

Summary

- QMOI may prepare and suggest account creation steps, but automatic creation of accounts
  on external platforms MUST be implemented per-platform with legal review, human approval,
  and secure API adapters.
- Handling real funds requires industry-standard safeguards: KYC/AML, PCI-DSS for card processing,
  use of approved payment processors (Stripe Connect, PayPal, Adyen), escrow for marketplace
  transactions, and comprehensive auditing.

Account lifecycle (recommended)

1. Prepare: QMOI prepares an account creation plan using `services/platformManager.prepareAccountCreation`.
2. Review: A human master reviews plan and approves (manual or automated workflow in the platform adapter).
3. Create: PlatformAdapter (per-platform implementation) performs creation using official APIs.
4. Verify: Perform email/phone verification and KYC where applicable.
5. Store: Securely store credentials in a secrets manager (Vault, AWS KMS/SecretsManager). NEVER store secrets in plaintext in repo.
6. Audit: All actions logged and signed; master must be able to revoke access.

Payments & Real Funds

- Default: All modules operate in "dry-run/simulated" mode unless an explicit `--enable-live-funds` flag AND master approval are provided.
- Use PCI-compliant payment processors. Do not implement direct card handling unless certified.
- Keep strict limits and require multi-party approval for transfers above configurable thresholds.
- Add an escrow layer for marketplace/deals where QMOI acts as an agent.

Legal & TOS

- Automatic account creation may violate platform Terms of Service. Implementers must obtain legal review and platform-specific API agreements before enabling automation.

Security Checklist (minimum)

- Secrets: Move all secrets to an external secrets manager.
- Audit logs: Immutable, retained for minimum 365 days.
- Limits: Per-platform rate limits with exponential backoff and circuit breakers.
- Master controls: Human-in-the-loop approvals for account creation, payments, and high-risk operations.

Notes

- The included `services/platformManager.ts` is a safe scaffolding and DOES NOT contact external APIs.
- For production, implement PlatformAdapters in `services/adapters/<platform>.ts` with rate-limiting, retries, error handling and master approval flows.

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/PLATFORM_AUTOMATION.md",
"validated_at": "2025-10-26T20:51:22.705060Z",
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
