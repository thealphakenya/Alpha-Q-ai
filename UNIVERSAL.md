# UNIVERSAL.md

## Styles/universals transition and replacement lineage

The universal layer must remain aligned with [STYLES.md](STYLES.md), [UNIVERSALS.md](UNIVERSALS.md), [QAUDITS.md](QAUDITS.md), [QVERSIONMANAGER.md](QVERSIONMANAGER.md), [ALLMDFILESREFS.md](ALLMDFILESREFS.md), and [TRANSION.md](TRANSION.md). Every style or universal file/directory candidate, including those that match the same basename as a legacy or generated doc, must be tracked as `candidate`, `review_required`, `verified_replacement`, or `remote_verified` instead of silently counted as replaced.

This document intentionally names the canonical policy and registry family that the transition covers: `STYLES.md`, `UNIVERSAL.md`, `UNIVERSALS.md`, `QAUDITS.md`, `QVERSIONMANAGER.md`, `ALLMDFILESREFS.md`, `ALLAUTO.md`, `AUTODEV.md`, `OFCA.md`, `ALLTESTSAUTOTESTS.md`, `ALLHOOKSWEBHOOKS.md`, and the app/platform/link registries. The transition plan documents how these files and directories are reviewed, counted, and advanced without ignoring any category or source path.

The generated local style/universal candidate path/hash crosswalk is [QMOItracks/style_universal_candidate_tree.md](QMOItracks/style_universal_candidate_tree.md); it does not assert implementation or replacement. Lifecycle checkpoint undo/redo is covered by [undoredo.md](undoredo.md) and does not grant repository or external-system rollback authority.

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

- Status: `NEEDS_REVIEW`; materialized files: `10603`; directories: `1280`; Markdown: `2421`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2157, build_download_install=2113, disability_accessibility=268, orchestration=2065, qteam_accountability=2053, release_tag_publish=2092, tree_inventory=2004`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2226`; needs review: `187`; metric candidate lines: `52756`; percentage occurrences: `22237`.
- Markdown word count: `3562982`; heuristic sentence count: `674722`; sentence records indexed: `674722`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29846` metric claims; `10693` completion claims; `29749` metric and `10564` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9053` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13376`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40146` lines in `3689` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `299`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: qaudit-style-universal-accessibility-coverage -->
## Agent-managed QAUDITS style, universal, accessibility, and recovery coverage

This section is refreshed from the same local QAUDITS universe on every invocation of `refresh_QMOI_reference_audit()` (pre-merge and full `audit-inventory` paths). It is not a timer or remote verification.
- Generated at: `2026-10-10T02:54:49.639306Z`; correlation ID: `80504776-40b9-44ed-a424-40611c22cc87`.
- Source manifest SHA-256: `f604caed4cca2e044439cdcaeabb9d44d0b394a7a836adf5c50c57ec67d8ed2d`; scope: `materialized_local_only`.
- Style candidates: `22`; universal candidates: `40`; all remain candidate-only.
- QStats: `13` planned domains; `20` observed contract files; `1` missing/unavailable; remote verified: `False`.
- QLion: `820` variation candidates; `8` registered extensions; implementation and remote validation remain unverified.
- Chat/voice/hands-free candidates: `944`; checkpoint/undo/redo/restore candidates: `776`; heartbeat/health/oxygen candidates: `1434`.
- Disability/accessibility Markdown candidates: `266`; complete path/category/hash records are in `QMOItracks/qaudit_universe.json` and `ALLMDFILESREFS.md` under Category D1.
- Disability/accessibility category path count: `407`; mapped tests: `0`; reviewed hook applicability: `0`.
- Audit status: `NEEDS_REVIEW` until owners, implementations, user-selected access preferences, privacy boundaries, applicable tests, and exact-SHA evidence are mapped. No disability is inferred or stored as a user profile.
- Missing, stale, or provider-unverified health/oxygen values remain `UNKNOWN`; dashboard balances and account values require authorized provider evidence and are not inferred from prose.
- Updating this managed section never rewrites historical/archive documents, policy instructions, or Q-version artifacts.
<!-- END QMOI MANAGED: qaudit-style-universal-accessibility-coverage -->
