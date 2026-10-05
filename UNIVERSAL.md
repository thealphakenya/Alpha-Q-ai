# UNIVERSAL.md

<!-- BEGIN QMOI MANAGED: universal-ui-access-contract -->
## Universal UI access modes and per-user feature creation

All apps and cloned-platform consoles use the same public, authenticated-user, and master-operator access model. App-specific screens may add capabilities but may not weaken these checks.

### public_guest
- Public catalog, public documentation, public previews, and safe anonymous browsing.
- No user-specific data, private workspace, account action, or protected mutation.

### authenticated_user
- Verified identity, consent, session state, personal settings, and user-owned workspace.
- Account, wallet, purchase, upload, private media, and write actions require server-side authorization.

### master_operator
- Explicit master role, MFA or equivalent step-up verification, current capability, and audit context.
- Administrative mutations require backend authorization and human confirmation where impact is high; master and sister may configure bank accounts, wallets, payment APIs, and project-linked payment destinations.

### Per-user UI generation

- Generate or configure account-specific UI only after verified identity, consent, tenant/user scope, and server-provided capabilities are available.
- Keep guest/public browsing useful without exposing private data; upgrade to account features only through explicit sign-in and consent.
- Personalization may adjust preferences and layout but cannot create permissions, reveal another user's data, suppress risk warnings, or trigger financial/hosting/quantum actions.
- Account creation, MFA, consent, payments, OS permission grants, production deployment, and quantum spend remain human-confirmed actions when required by policy.
- Record access-mode transitions and denial reasons without writing credentials, tokens, or private user content to docs or logs.
<!-- END QMOI MANAGED: universal-ui-access-contract -->

<!-- BEGIN QMOI MANAGED: feature-test-event-accountability -->
## Agent-managed feature, test, and event accountability contract

Automation may inventory and test preauthorized repository changes without a person present, but may not bypass repository policy, branch protection, user consent, provider permissions, or required human approvals for high-impact actions.

- A feature is complete only when its implementation, UI/API access boundary, tests, docs, and event integrations agree for an exact repository/ref/SHA.
- Every file mutation records path, owner, prior/new hashes, reason, validation, and authorization context; failed or skipped work remains visible.
- Hooks/webhooks require authentication/signatures, replay and idempotency controls, bounded retries, secret-reference-only handling, audit logging, and tested failure paths.
- A feature without a mapped test or verified event integration remains `unmapped` or `blocked`; total automation claims cannot exceed inspected scope.
- Current styles/universals mapping state: `NEEDS_FEATURE_TEST_HOOK_MAPPING`; tests mapped: `0/404`; hook applicability reviewed: `0/404`.
- Candidate migration inventory: `QMOItracks/style_universal_replacement_inventory.json`; each candidate remains review-required and is not treated as a completed replacement.
- Trading automation remains paused on stale market/account data, invalid authorization, provider outage, risk-limit breach, or ledger mismatch; runtime independence requires separately verified hosts and fresh heartbeat evidence.
<!-- END QMOI MANAGED: feature-test-event-accountability -->

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10408`; directories: `1267`; Markdown: `2412`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Markdown structural checks passed: `2186`; needs review: `218`; metric candidate lines: `46823`; percentage occurrences: `22236`.
- Formula/calculation candidate lines: `11364`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `36263` lines in `3090` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `285`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
