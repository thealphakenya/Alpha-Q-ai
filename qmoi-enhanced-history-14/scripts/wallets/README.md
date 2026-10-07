---
title: "Wallets — security, testnet usage, and operational guidance"
qmoi_validation_frontmatter: true
---

# Wallets — security, testnet usage, and operational guidance

This document explains how the QMOI wallet tooling is intended to be used safely in development and production.

Key principles

- Safety-first: every adapter is mock-first. Real network calls require `PRODUCTION_CONFIRMED=true` and explicit `--real` flags.
- Secrets out of code: do NOT store API keys in the repo. Use environment variables or a secret manager (GitHub Secrets, Vault, AWS Secrets Manager).
- Audit trail: all wallet QV runs write validation artifacts under `.qmoi_validation/` and history under `.qmoi_validation/wallet_balance_history.json`.

Running checks

- Dry-run (safe, recommended):

```
python3 scripts/wallets/check_wallets.py --report ./.qmoi_validation/all_wallets_qvs.json
```

- Live mode (REQUIRES HUMAN REVIEW & SECRETS):

```
# export required env vars (example)
export CASHON_API_KEY=... CASHON_API_URL=...
export PRODUCTION_CONFIRMED=true
python3 scripts/wallets/check_wallets.py --report ./.qmoi_validation/all_wallets_qvs.json --real
```

Offline and testnet

- To avoid external rate queries, set `DISABLE_EXTERNAL_RATES=true` to use mocked conversion rates.
- Testnet adapters (e.g., `binance_testnet`, `mpesa_sandbox`, `leahwallet`) are available for dry-run and simulation.

Aliases & memory

- The small state store (`.qmoi_state/wallets.json`) maps aliases like `leah` to canonical wallet ids (e.g., `leahwallet`).
- Use `scripts/wallets/state_store.py` to bootstrap or inspect the state store.

API and dashboards

- A simple local API is provided at `scripts/wallets/wallets_api.py` (Flask). Run locally only and secure with `QMOI_API_TOKEN`.

Security checklist before enabling live operations

1. Ensure all adapters you intend to use have been code-reviewed.
2. Store credentials in a secrets manager; never commit them.
3. Run in a controlled environment (server/container) with monitored audit logs.
4. Require at least one human reviewer to approve `PRODUCTION_CONFIRMED=true` before running with `--real`.

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
