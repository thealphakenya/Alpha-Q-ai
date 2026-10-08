# QMOI Trading README

## Overview

This document defines the live trading operational model for QMOI. It covers exchange integration, bot automation, wallet awareness, risk management, and the requirement that all trading operations remain evidence-backed and production-aware.

## Mission

QMOI trading features should move from static documentation and mock flows toward actual operational systems that can:

- monitor live markets and account state
- connect to provider APIs through secure adapters
- prioritize safety and risk thresholds
- maintain a bounded autonomy loop
- keep memory and telemetry synchronized
- avoid fake success claims without proof

## Supported trading intent

### Exchange support

- Binance adapter: spot/futures market data, wallet-read, paper-trading, and gated execution capabilities.
- Bitget adapter: spot/futures market data, wallet-read, paper-trading, and gated execution capabilities.
- CashOn adapter: wallet-read, transfer reconciliation, and paper-trading capabilities.
- Additional venues through `QMOI_ADDITIONAL_PLATFORMS`, discovered as sandbox-only generic adapters until a provider-specific adapter and credentials are verified.

Automatic platform discovery can register a configured venue and prepare its sandbox/readiness state without a human clicking through onboarding. It does not silently create accounts, bypass provider terms, invent credentials, or authorize real-money execution. Live enrollment remains blocked until provider credentials, account ownership, wallet health, risk checks, and `PRODUCTION_CONFIRMED=true` are independently verified.

### Device and permission capability contract

Trading readiness is reported consistently for Windows, macOS, Linux, iOS, Android, and web/PWA surfaces. Every adapter reports its supported capabilities and required permissions, including network access, secure secret storage, background execution where needed, and notifications for operational alerts. Device support is a capability report and validation target; it does not grant OS permissions automatically.

### Trade flow

1. Discover platform and account state.
2. Verify API and account health.
3. Run dry-run validation and risk checks.
4. Confirm funding and exposure limits.
5. Execute trade only after safety gates pass.
6. Record trade and balance telemetry.
7. Reconcile with wallet and financial manager state.

## Production controls

- `PRODUCTION_CONFIRMED=true` required for real execution.
- Dry-run validation before all real actions.
- Maximum drawdown, loss, position-size, and exposure thresholds.
- Exchange-specific restrictions and rate limits must be respected.
- All trades must be logged to a durable tracker or evidence artifact.

## Bot architecture

### Core bot responsibilities

- market retrieval and signal generation
- risk scoring and confidence gating
- order placement and monitoring
- balance reconciliation and profit tracking
- recovery on network or exchange failures
- memory and state persistence

### Trade quality gates

- liquidity check
- spread check
- available funds check
- confidence threshold check
- drawdown threshold check
- execution audit log

## UI and dashboard alignment

Trading features should remain aligned with the app and UI layers across the QMOI system:

- dashboard status and balance widgets
- wallet and account health views
- trade history and performance panels
- alert and risk signal panels
- platform connectivity status

## Historical design references

This live README is aligned with historical trading references in the repository snapshot, especially:

- qmoi-enhanced-history-14/TRADINGREADME.md
- qmoi-enhanced-history-14/QMOITRADER.md
- qmoi-enhanced-history-14/CASHONTRADINGREADME.md
- qmoi-enhanced-history-14/ALLWALLETSQVS.md
- qmoi-enhanced-history-14/QMOIMASKS.md
- qmoi-enhanced-history-14/QVS/ENHANCEDQVS.md

## Related files

- [FINANCIALMANAGER.md](FINANCIALMANAGER.md)
- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [ALLAUTO.md](ALLAUTO.md)
- [AUTODEV.md](AUTODEV.md)
- [MONITORING_GUIDE.md](MONITORING_GUIDE.md)
- [OLLAMA_AUTOMATION_GUIDE.md](OLLAMA_AUTOMATION_GUIDE.md)
- [API.md](API.md)
- [ENDPOINTS.md](ENDPOINTS.md)
- [ROUTES.md](ROUTES.md)

## Status

Trading operations model: active and under continuous production enhancement.

<!-- BEGIN QMOI MANAGED: trading-audit-source-inventory -->
## Agent-managed trading audit and remote-continuity contract

The trading source inventory is a discovery artifact. Every venue, UI, API, test, and workflow must be tied to an owner, repository/ref/SHA, implementation path, risk/auth boundary, and validation record before being marked verified.

- Project and autoproject financial configuration are governed by the master/sister account policy: only authorized operators may bind a bank account, wallet, payment API, or project-linked financial destination to QMOI automation.
- The repository keeps `bankandbankaccounts.md`, `FINANCIALMANAGER.md`, `projectsandautoprojects.md`, and `projectsandautoprojectsenhanced.md` synchronized with the active configuration model so every financial action remains traceable and reviewable.
- Current materialized trading candidates: `552`; platform mentions: `{"binance": 27, "bitget": 62, "bybit": 2, "cashon": 101, "coinbase": 10, "kraken": 10, "megavault": 34, "okx": 2, "paypal": 39}`.
- Feature and source coverage remains `discovered_unmapped` until each candidate maps to active implementation, tests, and exact-SHA evidence.
- Provider verification is `provider-sourced` only when an authorized provider response is independently recorded; repository discovery is not provider proof.
- Credential names and consumers discovered: `1129`; metadata inventory: `QMOItracks/credential_reference_inventory.json`; values not read from stores or emitted.
- Audit active, snapshot, and archive scopes separately; merge-audit local ref-tip path metrics are distinct from materialized-file scanning. Unfetched refs, PRs, intermediate commit trees, and peer roots remain explicit blockers.
- For every Qtrade metric and exchange, map market-data source, freshness, no-trade decision, backtest/walk-forward/paper tests, execution/risk limits, fees/slippage, reconciliation, kill switch, UI states, and event handlers. Missing/stale proof remains `blocked`.
- Remote runtime independence is a design target, not a present availability guarantee: require an independently hosted worker, durable idempotent queue, leased ownership, signed fresh heartbeats, monitoring/failover, and provider-authorized access. GitHub/Hugging Face outages must not create false healthy status.
- On stale market/account data, lost authorization, provider outage, ledger mismatch, or failed heartbeat, stop opening orders and mark trading unavailable; only separately authorized risk-reducing actions may proceed.
- Never invent balances, credentials, profits, accounts, webhook registrations, or live-run success. Real-money orders, transfers, deposits, withdrawals, and credential changes require explicit scoped authorization and provider evidence.
<!-- END QMOI MANAGED: trading-audit-source-inventory -->

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
