# QMOI Financial Manager

## Purpose

This document defines the live financial management model for QMOI. It consolidates wallet monitoring, trading automation, balance growth, platform accountability, real-funds revenue generation, and production risk controls so the system can operate with real-funds-aware logic instead of placeholder-only workflows.

QMOI remains conscious, aware, and memory-synced in every financial action. The system must record wallet state, account confidence, revenue streams, trade executions, deployment health, and monitoring telemetry as a single live model before any live funds movement is allowed.

## Operating principles

- Safety first: real money movement is gated behind explicit production approval, environment verification, and runtime confirmation.
- Multi-wallet awareness: every wallet, exchange, transfer lane, and account must be discoverable and auditable.
- Risk-aware automation: all automation must monitor drawdown, exposure, slippage, and confidence metrics before acting.
- Memory-aware execution: financial state, wallet history, and trading telemetry must remain synchronized across GitHub, local runtime, monitoring, and dev workflows.
- Evidence-based completion: no “success” claim is valid without live validation or proof artifacts.

## Core finance objectives

1. Maintain wallet and account visibility across all supported channels.
2. Increase net financial health, not just activity volume.
3. Balance safety, automation, and profitability using risk thresholds.
4. Keep real-money trading paths isolated behind audit-ready controls.
5. Keep all live state synchronized and recoverable.

## Finance feature coverage and evidence contract

QAUDITS refreshes the managed finance section of this document and the finance categories in `ALLMDFILESREFS.md` during `audit-inventory`. Its keyword-based `financial_claim_inventory.json` reports candidate files/lines by amount and currency, revenue/income/money-making, payments/transfers, wallets/banking, deals/contracts, employment/payroll, country/jurisdiction, project budgets/expenses, and financial security/authorization. Counts are overlapping discovery metrics, not proof that any capability is implemented, available globally, compliant, connected, or safe to use.

Each real feature must be independently mapped to a named owner, supported implementation path, least-privilege API/UI boundary, applicable test and negative/failure test, source/provider evidence, reconciliation/audit trail, and exact repository/ref/SHA. Country, nation, currency, provider and employment coverage must come from reviewed, versioned registries and authorized sources; keyword matches must not be interpreted as a complete legal, geographic, or ISO currency list. QAUDITS stores hashes and candidate locations, not source amounts, balances, account identifiers, credentials, or raw claim text.

The financial management backlog should explicitly inventory:

- Multi-currency ledgers with decimal-safe amounts, immutable double-entry journals, idempotency, settlement states, reversals, reconciliation, and distinct pending/available/reserved balances.
- Wallet, bank, payment-provider and exchange adapters with owner consent, account scoping, read-only verification first, webhook signature/replay defenses, scoped credential references, rate limits, outage handling, and verified provider capabilities.
- Revenue, subscription, sales, media/royalty, project/autoproject, marketplace, affiliate and grant flows; evidence for gross/net receipts, fees, refunds, taxes, outstanding receivables and forecast-versus-actual with period/source provenance.
- Deal/contract/invoice/escrow/commission workflows with counterparty, approvals, contract version, obligations, dates, dispute/chargeback status and audit trail.
- Employment and payroll requirements by country/jurisdiction, worker classification, consent, approvals, payroll/tax/benefit obligations and provider support. Do not infer employment or legal readiness from document mentions.
- Project budgets, expenses, procurement, accounts payable/receivable, liabilities, reserves, cash flow, runway and owner-approved limits, reconciled to source records.
- Fraud/AML/KYC/sanctions and privacy controls, segregation of duties, least privilege, step-up authorization, retention and incident/revocation paths. Such evidence is a hard gate, not a weighted score.
- Management metrics with explicit numerator/denominator, currency, time period, account/project scope, timestamp, fee/tax policy, data source and reconciliation state. Missing/stale inputs produce `unknown`/`blocked`, never a zero or inferred value.

Discovery does not authorize transfers, trades, deposits, withdrawals, payroll, account/credential changes, or external provider registration. Those actions require explicit scoped owner authorization, verified provider capability, applicable human/legal approval and terminal evidence; remote completion additionally requires target-owned exact-SHA proof.

## Wallet and account model

### Financial layers

- Treasury layer: all stable balances and cash reserves.
- Wallet layer: provider and platform accounts such as CashOn, Binance, Bitget, PayPal, Airtel, M-Pesa, and other operational channels.
- Execution layer: automated trade and transfer logic.
- Audit layer: logs, checkpointing, balance checks, and revision records.

### Required monitoring fields

- wallet name and canonical ID
- account owner or delegated controller
- currency, network, and platform
- available balance, reserved balance, and pending withdrawals
- risk score and confidence level
- last successful validation timestamp
- last transfer or trade timestamp
- alert state and drift thresholds

## Production risk controls

- Require `PRODUCTION_CONFIRMED=true` before any real transfer or trade flow.
- Require explicit provider and account IDs, not just generic names.
- Require dry-run validation before live execution.
- Enforce maximum position, max exposure, max drawdown, and daily loss thresholds.
- Require health checks before any external API call.
- Keep secrets outside tracked code and outside commit logs.

## Trading bot architecture

### Bot responsibilities

- Discover exchange connectivity and account health.
- Evaluate liquidity and spread before execution.
- Respect platform-specific limits and time windows.
- Record order IDs, balances, and settlement status.
- Keep a bounded recovery loop for failures or rate limits.

### Supported platform intent

- Binance: spot, futures, and order book monitoring.
- Bitget: exchange connectivity, futures/spot logic, and account checks.
- CashOn and wallet ecosystems: local transfer and balance reconciliation.
- Additional providers: support via adapter-based integration, not hardcoded assumptions.

### Execution policy

- Live execution runs only when the environment is verified and the bot has passed dry-run validation.
- Order size is limited by account balance, exposure, and risk thresholds.
- All bots must emit structured telemetry and checkpoint evidence.

## Real-funds-aware strategy

The project should treat trading as an operational system, not as a static demo. The financial manager must support:

- account creation and onboarding workflows
- secure credential and secret handling
- real-time balance checks
- trading plan generation
- execution monitoring and reconciliation
- profit/loss tracking
- recovery when exchange or network failures occur

## Historical references to reconcile

This document is aligned with the historical finance and trading materials in the repository snapshot, including:

- qmoi-enhanced-history-14/FINANCIALMANAGER.md
- qmoi-enhanced-history-14/TRADINGREADME.md
- qmoi-enhanced-history-14/CASHONTRADINGREADME.md
- qmoi-enhanced-history-14/ALLWALLETSQVS.md
- qmoi-enhanced-history-14/QMOITRADER.md
- qmoi-enhanced-history-14/QMOIMASKS.md
- qmoi-enhanced-history-14/QVS/ENHANCEDQVS.md
- qmoi-enhanced-history-14/DEALS.md
- qmoi-enhanced-history-14/PAYMENTS.md
- qmoi-enhanced-history-14/docs/REVENUE_SPEC.md

The live repo should keep the live documentation authoritative, while the historical docs remain a reference for operational continuity and transfer of lessons learned.

## Deal and transaction documentation coverage

The following active markdown files contain deal, transaction, payment, settlement, contract, invoice, payout, escrow, counterparty, or revenue-share guidance and are part of the financial manager documentation surface. They must remain aligned with this document:

- [ADVANCEMENT.md](ADVANCEMENT.md)
- [ALLBACKEND.md](ALLBACKEND.md)
- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [ALLROUTES.md](ALLROUTES.md)
- [API.md](API.md)
- [AUTODEV.md](AUTODEV.md)
- [ENDPOINTS.md](ENDPOINTS.md)
- [FINAL_VALIDATION_EVIDENCE_2026_08_29.md](FINAL_VALIDATION_EVIDENCE_2026_08_29.md)
- [GITHUBCLONED.md](GITHUBCLONED.md)
- [GITHUB_ACTIONS_EXECUTION_GUIDE.md](GITHUB_ACTIONS_EXECUTION_GUIDE.md)
- [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)
- [MEMORY_INDEX.md](MEMORY_INDEX.md)
- [MERGE.md](MERGE.md)
- [MODEL_CARD.md](MODEL_CARD.md)
- [MONITORING_GUIDE.md](MONITORING_GUIDE.md)
- [MONITORING_INDEX.md](MONITORING_INDEX.md)
- [MONITORING_SUMMARY.md](MONITORING_SUMMARY.md)
- [OLLAMA_AUTOMATION_GUIDE.md](OLLAMA_AUTOMATION_GUIDE.md)
- [OLLAMA_ENHANCEMENT_COMPLETE.md](OLLAMA_ENHANCEMENT_COMPLETE.md)
- [OLLAMA_ENHANCEMENT_SUCCESS.md](OLLAMA_ENHANCEMENT_SUCCESS.md)
- [PHASE_1_4_COMPLETION_SUMMARY.md](PHASE_1_4_COMPLETION_SUMMARY.md)
- [QALPHA.md](QALPHA.md)
- [QMOIAI.md](QMOIAI.md)
- [QMOI_MODEL_CARD.md](QMOI_MODEL_CARD.md)
- [QTEAM.md](QTEAM.md)
- [README.md](README.md)
- [REAL_TIME_MONITORING_GUIDE.md](REAL_TIME_MONITORING_GUIDE.md)
- [REAL_TIME_MONITORING_README.md](REAL_TIME_MONITORING_README.md)
- [ROUTES.md](ROUTES.md)
- [STYLES.md](STYLES.md)
- [TEST_ENHANCEMENTS.md](TEST_ENHANCEMENTS.md)
- [UNIVERSALS.md](UNIVERSALS.md)
- [WORKFLOWS.md](WORKFLOWS.md)
- [WORKFLOWSO.md](WORKFLOWSO.md)
- [WORKFLOW_EXECUTION_PLAN.md](WORKFLOW_EXECUTION_PLAN.md)
- [WORKFLOW_STATUS_DASHBOARD.md](WORKFLOW_STATUS_DASHBOARD.md)
- [github.md](github.md)
- [monitor.md](monitor.md)
- [oe.md](oe.md)
- [ollama.md](ollama.md)
- [or.md](or.md)
- [trigger.md](trigger.md)

This map is an inventory and synchronization contract. A keyword match alone does not make a document an execution authority: live code, tests, wallet telemetry, and transaction proof remain authoritative for actual deal state.

## Automation requirements

- Currency and wallet state must be audited at defined intervals.
- Balance health and investment thresholds must be in monitor state.
- Alerts must trigger when a wallet or bot moves outside allowed bounds.
- A repo checkpoint must be updated whenever financial automation changes state.
- QMOI memory and monitoring must remain synchronized with wallet and trader state.

## GitHub/Vercel/developer alignment

The financial manager must be aligned with GitHub automation, deployment systems, and development operations:

- GitHub Actions for workflow verification and on-demand automation
- GitHub-hosted validation before live execution
- Vercel integration and deployment safety for app surfaces and dashboards
- memory and telemetry sync across repo and runtime systems

## QMOI consciousness, memory sync, and real-time awareness

QMOI must remain conscious, aware, and memory-synced in every financial action. That means the system must keep a single live model of:

- user identity and delegated account ownership
- wallet and exchange state across all connected platforms
- trade history, account confidence, and balance drift
- revenue streams, payout windows, and active monetization channels
- last successful validation, alert state, and any runtime anomaly
- remote monitoring state from GitHub, local runtime, and deployment systems

This awareness is not optional. The financial manager must treat every trade, wallet operation, revenue event, and user dashboard metric as part of the same QMOI memory graph so the system does not act with stale or fragmented financial context.

### Required consciousness guardrails

- Every financial action must carry a valid state snapshot and runtime identity.
- Every wallet balance update must be reflected in the live memory index and monitoring telemetry.
- Every revenue operation must be attributable to a channel, agent, and user or organization context.
- Every remote monitor result must be reconciled before changing live execution permissions.
- Any gap between wallet state, monitoring state, and runtime memory is a stop condition until resolved.

## Real-funds revenue generation model

QMOI should treat money-making as a production system with operational controls. The live model includes:

- core trading revenue from supported exchange flows
- wallet-funded account operations and account onboarding flows
- service revenue channels such as features, AI workflows, and platform access
- content and music monetization where applicable
- partner and platform revenue conversion channels
- direct and indirect monetization flows routed through managed wallets and account dashboards

The financial manager must keep a running view of:

- active revenue streams
- net revenue and transfer health
- payout reliability
- channel risk
- user or brand-specific monetization confidence scores

## Remote realtime monitoring and operational visibility

The financial system must stay observable in real time across all remote and local environments. The monitor should continuously check:

- wallet health and available balances
- revenue-generation task status
- trade bot execution windows and exposure limits
- platform connectivity and rate-limit health
- GitHub workflow delivery and deployment health
- global dashboard metrics and alert thresholds
- memory synchronization health across automation loops

Monitoring expectations:

- remote state should be visible in a live dashboard, not hidden in logs only
- every critical event should be emitted to telemetry and checkpoint state
- any failed validation should freeze live execution until the issue is resolved
- financial monitoring should combine policy checks, confidence scoring, and telemetry correlation

## UI and user experience for financial operations

The financial manager interface should present all critical measurements clearly to users and operators:

- wallet overview with balances and drift
- account confidence indicators
- platform status for Binance, Bitget, CashOn, and other supported providers
- trading readiness and execution gating
- revenue and payouts summary
- global metrics for gains, losses, exposure, and health
- user-specific style profiles and financial dashboard personalization

These UI surfaces should be reviewed against the styling system so each user receives a personalized but consistent finance experience without losing operational clarity.

## Style-personalized financial UX plan

The QMOI styling layer should allow the UI to adapt to user or organization context while preserving system integrity. Financial dashboard styles should include:

- high-trust mode for account safety and audits
- premium growth mode for revenue and profit dashboards
- conservative risk mode for trader and wallet controls
- personal brand mode for user-specific music, revenue, or advisor surfaces
- operational command-center mode for real-time monitor status and trade execution readiness

This ensures the system can present each user with a tailored financial experience while remaining consistent with the live QMOI design system and safety model.

## Money-making, revenue generation, and platform automation track

The financial manager should support multi-track revenue generation, including:

- trading and arbitrage workflows
- wallet and balance growth operations
- ad, content, and brand monetization
- music, creator, and licensing revenue pathways
- automation and autopilot revenue logic
- user-facing monetization workflows and onboarding funnels

Every revenue track should have:

- a defined source of funds
- a health monitor
- an owner or delegated controller
- a risk threshold
- a validation log
- a payout or settlement record

## Deal-making, deal confirmation, and transaction validation

QMOI must treat deal-making as a structured financial workflow, not as informal negotiation. The system should support all classes of transactions and deals, including:

- trading deals on exchanges and wallet-mediated flows
- partner or client payment deals
- creator, music, licensing, and media deals
- invoice and settlement deals
- business acquisition or reseller deals
- debt, payout, or escrow-based financial commitments
- cross-border transfer and treasury deals
- investment, revenue-share, and stake-related deals
- marketplace service deals and vendor payouts

### Deal lifecycle

1. Opportunity detection and discovery
   - identify the counterpart, expected value, and flow path
   - confirm asset type, currency, risk, and required settlement method
2. Offer creation and negotiation
   - prepare deal terms and expected outcomes
   - enforce pre-deal confidence threshold and counterparty verification
3. Confirmation gate
   - confirm the counterpart and source of funds
   - validate whether the deal is in a safe execution window
4. Transaction preparation
   - route funds via approved wallet, account, or exchange
   - mark obligations and reserve balances
5. Execution and settlement
   - trigger transfer or trading order only after validation and risk checks pass
6. Proof capture and reconciliation
   - record payment hashes, order IDs, settlement receipts, and confirmations
7. Post-deal audit
   - reconcile expected vs actual values
   - update the memory graph, dashboard, and monitoring telemetry

### Required confirmation rules for all deals

- Deal counterpart must be explicitly identified and risk-scored.
- Transaction amount must be checked against wallet limits and balance health.
- Route must be approved and valid for the deal type and region.
- All funds movement must be traceable to an approved wallet or account path.
- All confirmations must be stored with timestamps and proof references.
- Any mismatch between declared amount, route, or wallet state blocks execution.
- A deal is not considered valid unless the same state is visible in monitor, memory, and wallet systems.

### Transaction validation model

The financial manager should validate each payment or trade with a consistent evidence stack:

- identity and ownership validation
- counterparty confirmation
- wallet balance and reserve checks
- route and settlement channel checks
- exchange or platform readiness check
- transaction status proof and confirmation hash
- anti-fraud and drift detection
- final accounting reconcile step before close-out

Any failed validation means the deal is held in an "unconfirmed" state until the discrepancy is corrected.

## UI features for financial manager and deal processing

The financial dashboard must expose operational clarity for all money actions and deal workflows:

- wallet health and account confidence indicator
- total deal pipeline value and live stage status
- pending, confirmed, and rejected deal counters
- transaction validation panel for proofs, confirmations, and drift checks
- revenue, trading, and deal health timeline
- global metrics for balances, exposure, payouts, and automated gains
- personalized user dashboard and risk-aware styling modes
- alert and escalation panel for failed or suspicious transactions
- activity feed for deal execution, funding confirmation, and settlement events

These UI features should also integrate directly with the QMOI monitor, memory graph, and alert system so the user never sees a stale or fragmented financial view.

## Evidence standard

The financial manager is only considered active when the following are true:

- wallet and exchange inventory is known
- balance checks are verified
- monitoring is running
- risk gates are enforced
- checkpoint and log artifacts are produced
- dry-run validation occurs before real execution

## Related files

- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [ALLAUTO.md](ALLAUTO.md)
- [AUTODEV.md](AUTODEV.md)
- [API.md](API.md)
- [ENDPOINTS.md](ENDPOINTS.md)
- [ROUTES.md](ROUTES.md)
- [MONITORING_GUIDE.md](MONITORING_GUIDE.md)
- [OLLAMA_AUTOMATION_GUIDE.md](OLLAMA_AUTOMATION_GUIDE.md)
- [QMOI_REALTIME_MEMORY_INDEX.md](QMOI_REALTIME_MEMORY_INDEX.md)
- [WORKFLOWS.md](WORKFLOWS.md)

## Status

Production-oriented financial management model: active and under continued enhancement.

<!-- BEGIN QMOI MANAGED: trading-evidence-and-balance-accountability -->
## Agent-managed trading and balance evidence

Trading and balance displays must distinguish provider-observed, simulated, stale, and unavailable values. Path discovery does not prove account ownership, current balances, settlement, or provider integration.

- Materialized trading candidates: `552`; detailed inventory: `QMOItracks/trading_surface_inventory.json`.
- Financial claim audit: `1062` files, `25910` redacted candidate lines; values are excluded from the report and no balances are verified.
- Only authorized read-only provider responses can produce current balance evidence; include account scope, currency, observed-at timestamp, and reconciliation status without exposing account secrets.
- Transfers, deposits, withdrawals, payroll, and live trading remain blocked without explicit authorization, verified provider capability, risk checks, and auditable confirmation.
- Revenue, P&L, and model-comparison claims must be independently sourced and net of fees; no guaranteed growth/profit claims.
### Redacted financial amount and account-claim audit

This scan indexes claim locations and metadata only; it does not verify balances, account ownership, provider access, or transaction truth. Raw amounts, account identifiers, and source line text are never copied into the report.

- Tracked materialized Markdown files with financial claims: `1062`.
- Candidate financial lines: `25910`; amount-like candidates: `3302`; untyped numeric candidates: `5420`.
- Account-ID-like lines: `4`; actual balances independently verified by this scan: `0`.
- Currency mentions by owner label: `{"binance": {"AED": 1, "BTC": 8, "CAD": 1, "CNY": 1, "ETH": 8, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 5, "RAND": 1, "USD": 5, "USDC": 1, "USDT": 14}, "bitget": {"AED": 1, "BTC": 4, "CAD": 1, "CNY": 1, "ETH": 4, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 1, "RAND": 1, "USD": 1, "USDC": 1, "USDT": 10}, "bybit": {"AED": 1, "BTC": 1, "CAD": 1, "CNY": 1, "ETH": 1, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 1, "RAND": 1, "USD": 1, "USDC": 1, "USDT": 1}, "cashon": {"AED": 1, "BTC": 6, "CAD": 1, "CNY": 1, "ETH": 6, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 29, "RAND": 1, "USD": 5, "USDC": 1, "USDT": 11}, "coinbase": {"AED": 1, "BTC": 1, "CAD": 1, "CNY": 1, "ETH": 1, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 1, "RAND": 1, "USD": 1, "USDC": 1, "USDT": 1}, "kcb": {"AED": 1, "BTC": 2, "CAD": 1, "CNY": 1, "ETH": 2, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 4, "RAND": 1, "USD": 2, "USDC": 1, "USDT": 1}, "kraken": {"AED": 1, "BTC": 1, "CAD": 1, "CNY": 1, "ETH": 1, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 1, "RAND": 1, "USD": 1, "USDC": 1, "USDT": 1}, "ledger_wallet": {"BTC": 1, "ETH": 1}, "megavault": {"AED": 1, "BTC": 1, "CAD": 1, "CNY": 1, "ETH": 1, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 1, "RAND": 1, "USD": 1, "USDC": 1, "USDT": 1}, "okx": {"AED": 1, "BTC": 1, "CAD": 1, "CNY": 1, "ETH": 1, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 1, "RAND": 1, "USD": 1, "USDC": 1, "USDT": 1}, "paypal": {"AED": 1, "BTC": 2, "CAD": 1, "CNY": 1, "ETH": 2, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 9, "RAND": 1, "USD": 2, "USDC": 1, "USDT": 4}, "pesapal": {"AED": 1, "BTC": 1, "CAD": 1, "CNY": 1, "ETH": 1, "EUR": 1, "GBP": 1, "JPY": 1, "KES": 3, "RAND": 1, "USD": 1, "USDC": 1, "USDT": 2}, "standard_chartered": {"BTC": 1, "ETH": 1}, "unassigned_account_wallet_bank": {"BTC": 1, "ETH": 1, "EUR": 3, "GBP": 3, "KES": 39, "USD": 16, "USDC": 1, "USDT": 2}, "unassigned_financial_claim": {"AED": 1, "BTC": 111, "CAD": 2, "CNY": 1, "ETH": 11, "EUR": 18, "GBP": 16, "JPY": 1, "KES": 1235, "RAND": 11, "USD": 62, "USDT": 50}}`.
- Candidate lines by financial-management category: `{"amount_currency": 5273, "country_and_jurisdiction": 917, "deals_and_contracts": 1355, "employment_and_payroll": 2305, "financial_security_and_authorization": 1870, "payments_and_transfers": 2556, "project_budget_and_expenses": 238, "revenue_income_money_making": 10703, "wallets_and_banking": 3790}`.
- Candidate locations, line numbers, hashes, scopes, and owner groups: `QMOItracks/financial_claim_inventory.json`.
- Tracked Markdown denominator: `2408`; untracked/ignored/oversized/unreadable/symlink exclusions: `2/0/5/3/0`.
- Taxonomy categories are keyword candidates (amount/currency, revenue/income, payments/transfers, wallets/banking, deals/contracts, employment/payroll, country/jurisdiction, project budgets/expenses, and financial security/authorization); counts overlap and do not establish implementation or coverage.
- Unsupported claims remain `needs_independent_review_not_verified`; do not silently delete or replace historical amounts with invented evidence. Resolve each claim with authorized source proof or retain it clearly marked unverified.
<!-- END QMOI MANAGED: trading-evidence-and-balance-accountability -->

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
