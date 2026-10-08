# Finance and credential provisioning manifest

## Secure provisioning policy
- Discover credentials by variable name and repository source only; never print or persist secret values.
- Provisioning steps must use a secure vault or environment injection and remain gated by master authorization when live accounts are involved.
- Keep this manifest in sync with runtime integrations and documentation so automation can safely plan account provisioning.

## Inventory
- Binance: env vars [BINANCE_API_KEY, BINANCE_SECRET_KEY, BINANCE_WITHDRAWAL_ADDRESS] | sources [.eslint_report_parsing_files.txt, .github/workflows/wallet-tests.yml, .ollama_agent_state.json, .qmoi_state/wallets.json, ALLAUTO.md, ALLERRORS.md, ALLERRORS.txt, ALLHOOKSWEBHOOKS.md] | provisioning: standard environment injection
- Bitget: env vars [BITGET_API_KEY, BITGET_API_PASSPHRASE, BITGET_API_SECRET, BITGET_API_URL, BITGET_PASSPHRASE, BITGET_SECRET_KEY] | sources [.cspell.json, .env.example, .eslint_report_parsing_files.txt, .ollama_agent_state.json, ALLBACKEND.md, ALLERRORS.md, ALLLINKS.md, ALLMDFILES.md] | provisioning: master authorization required
- CashOn: env vars [CASHON_MPESA_NUMBER, CASHON_WALLET] | sources [.ollama_agent_state.json, ALLERRORS.md, ALLERRORS.txt, ALLLINKS.md, ALLMDFILES.md, ALLMDFILESREFS.md, ALLUI.md, ALLVERSIONS.md] | provisioning: master authorization required
- Master/QMOI: env vars [QMOI_MASTER_API_KEY, QMOI_MASTER_TOKEN] | sources [.eslint_report_parsing_files.txt, .ollama_agent_state.json, ALLBACKEND.md, ALLERRORS.md, ALLERRORS.txt, ALLLINKS.md, ALLMDFILES.md, ALLMDFILESREFS.md] | provisioning: master authorization required
- PayPal: env vars [PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET, PAYPAL_MODE] | sources [.env.example, .env.production, ALLERRORS.md, ALLWALLETSQVS.md, API_REFERENCE.md, CASHON.md, CASHONTRADINGREADME.md, COMPLETION_INDEX.md] | provisioning: master authorization required
- Stripe: env vars [STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET] | sources [.env.example, .env.production, .ollama_agent_state.json, ALLERRORS.md, ALLMDFILESREFS.md, API_INTEGRATION_GUIDE.md, API_REFERENCE.md, COMPLETION_INDEX.md] | provisioning: master authorization required

## Secure provisioning plan
- Validate each provider's environment variables in the runtime environment or secure vault before any provisioning action.
- Record approvals, account states, and provisioning outcomes in this manifest and the workflow activity feed.
- Keep live provisioning actions disabled unless the master/system authorization context is present.

## Notes
- Master authorization is required for live account provisioning.
- The autonomous agent should only create or update this manifest; it should not attempt live credential submission or external account creation without explicit master approval.

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
