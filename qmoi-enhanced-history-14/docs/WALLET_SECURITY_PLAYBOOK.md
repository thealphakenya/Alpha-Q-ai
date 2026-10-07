---
title: "Wallet Security Playbook"
qmoi_validation_frontmatter: true
---

# Wallet Security Playbook

This document summarizes the recommended operational and engineering controls for QMOI wallets and payment flows.

Key principles

- Never store private keys in source control.
- Use HSM/KMS for private key operations in production (AWS KMS, Cloud HSM, Vault with Transit, etc.).
- Require sandbox mode by default. Live funds require explicit master approval and documented KYC/AML.
- Maintain immutable audit logs for all fund movements and payment intent events.

Operational guardrails

- Multi-sig thresholds: require at least 2 approvals for withdrawals above set thresholds.
- Daily limits and per-account velocity checks.
- KYC/AML checks integrated at onboarding and when thresholds are exceeded.
- Emergency freeze: operator action to disable outgoing payments while preserving read-only access to logs for forensics.

Engineering controls

- Secrets: store API keys and private keys in a secret manager. Provide a LocalSecretStore only for development.
- Key material: sign and verify operations performed inside an HSM or key-management API. Do not export raw private keys.
- Audit logging: append-only, tamper-evident store (e.g., write-ahead log stored in S3 with object lock, or WORM-enabled DB). Local `data/wallets/audit.log` is for sandbox only.
- Idempotency: all payment/webhook handlers must be idempotent. Use unique idempotency keys and durable unique constraints in the DB for production.

Incident response

1. Freeze funds (disable settlement workers).
2. Capture live memory/process snapshots and write to secure storage.
3. Rotate compromised keys (via KMS), revoke old keys, update adapter credentials.
4. Notify legal and compliance teams, start forensic timeline.
5. Notify affected customers and regulators per jurisdictional requirements.

Monitoring and alerts

- Alerts for large transfers, unusual velocity, repeated failed settlement attempts, new unrecognized payout destinations.
- Health checks for settlement workers and payment adapter connectivity.

Testing and drills

- Run periodic simulation drills that exercise the emergency freeze and key rotation.
- Maintain a sandbox environment with synthetic funds to run end-to-end tests.

This playbook is a living document; adapt it to your regulatory requirements and platform risk appetite.

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/WALLET_SECURITY_PLAYBOOK.md",
"validated_at": "2025-10-26T20:51:24.581046Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "Wallet Security Playbook"
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
