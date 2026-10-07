---
title: "ALL WALLETS QVS (Quick Verification Summary)"
qmoi_validation_frontmatter: true
---

# ALL WALLETS QVS (Quick Verification Summary)

This file documents discovered wallet-related documentation and provides instructions to run the automated wallet Quick Verification (QV) script.

Purpose

- Provide a single place listing wallet docs and guidance for running automated checks.
- Ensure wallet checks are dry-run by default and require explicit gating to run live transfers.

Discovered wallet docs (non-exhaustive)

- `CASHON.md` — Cashon system wallet and operational notes.
- `LEAHWALLET.md` — Leah/Sister wallet guide and UI notes.
- `QMOI-REVENUE-README.md`, `QMOIREVENUEGENERATION.md`, `QMOIAUTOREVENUEEARN.md` — revenue/autorevenue docs referencing Cashon and wallet flows.
- `CASHONTRADINGREADME.md`, `TRADINGREADME.md` — trading + wallet integration notes.
- Various README files reference wallets and payment providers (Mpesa, PayPal, Binance, Bitget, CashApp). Use the repository-wide [AUTOFIXED by Ollama at 2026-07-26T00:54:34.484662Z] scanner to find more references.

Location of automated checks

- Script: `scripts/wallets/check_wallets.py`
- Validation output: `.qmoi_validation/all_wallets_qvs.json`

How the checks work

- Default mode: mock/dry-run. No real network transfers or money movement are performed.
- To run live operations (NOT RECOMMENDED without human review + secret manager), you must set:
  - `PRODUCTION_CONFIRMED=true` in the environment, and
  - pass the `--real` flag to the script.
- Live transfer code paths are intentionally gated and require human approval and secret provisioning.

Run (dry-run) — local dev

```bash
python3 scripts/wallets/check_wallets.py
```

Run (explicit live, only after human review)

```bash
# Only run after manual code review and secrets provisioned
export PRODUCTION_CONFIRMED=true
python3 scripts/wallets/check_wallets.py --real
```

Next steps

- Expand `scripts/wallets/` with adapters for testnets and exchanges (Binance, Bitget, PayPal). Start with testnet-only adapters and automated unit tests.
- Add a scheduled job (daemon) to persist balance history to `.qmoi_validation/wallet_balance_history.json`.
- Prioritize adding secure secret manager integration (GH Secrets / Vault / AWS Secrets Manager) and never commit keys.

Contact / Audit

- All wallet changes must be code-reviewed and approved by the project owner. See `CASHON.md` and `MASTERREADME.md` for master-approval flows.

Generated: automatic inventory created by automation on request.

# ALL WALLETS QVS

This file lists all known wallets in the repository and provides a quick verification (QVS) plan.

IMPORTANT: All test scripts in `scripts/wallets/` run in dry-run/mock mode by default. Any operation that performs real transactions requires BOTH:

- the environment variable `PRODUCTION_CONFIRMED=true`
- the CLI flag `--real`

This is a deliberate safety gate to prevent accidental real-fund activity.

Wallet inventory (discovered):

- `MEGAVAULT.md` — QMOI Megavault System (file: `MEGAVAULT.md`)
- `CASHON.md` — Cashon wallet (file: `CASHON.md`)
- `CASHONTRADINGREADME.md` — Cashon trading system docs (file: `CASHONTRADINGREADME.md`)
- `LEAHWALLET.md` — Leah wallet (file: `LEAHWALLET.md`) — (created/updated)

Additional wallets may exist; run the check script to refresh the QV report.

How to run (dry-run / safe):

1. Dry-run (no network calls, mocked balances):

```bash
python3 scripts/wallets/check_wallets.py --report all_wallets_qvs.json
```

2. Live check (REAL calls) — MUST set `PRODUCTION_CONFIRMED=true` and understand this will attempt network calls and may use real funds where adapters support transactions/balances:

```bash
export PRODUCTION_CONFIRMED=true
python3 scripts/wallets/check_wallets.py --real --report all_wallets_qvs.json
```

Report output format (JSON):

{
"wallet": {
"balance": "<amount>|mock",
"currency": "<currency>",
"last_checked": "2025-10-28T22:00:00Z",
"source_file": "MEGAVAULT.md",
"status": "ok|missing_credentials|error"
}
}

Next steps (recommended):

- Review `LEAHWALLET.md` and follow the non-dev setup guide.
- Provide credentials via secure secrets manager or environment variables — do NOT commit them to git.
- Run the dry-run first to verify adapters and configuration, then run live checks only when ready.

Generated/Updated: 2025-10-28T22:30:00Z

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
