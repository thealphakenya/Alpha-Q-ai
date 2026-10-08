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

### Disability and assistive-technology access

Audit each app/platform feature for keyboard-only operation, visible focus, screen-reader semantics, low-vision zoom/reflow and contrast, captions/transcripts, motor and alternative-input support, cognitive/reading needs, seizure/reduced-motion needs, and other applicable access modes. This checklist is not exhaustive; applicability and fallback behavior must be tested per feature and platform.

Users may explicitly select accessibility preferences. Do not infer, label, or persist disability status. Preferences do not create permissions, and the same identity, privacy, and safety boundaries apply to chat, voice, dashboards, and other interfaces. Missing implementation or test evidence remains `unmapped`.

Voice and hands-free actions require device permission, an equivalent non-voice path, and explicit confirmation before protected or destructive operations. Unclear input, stale health, or missing permission must stop the action.
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

- Status: `NEEDS_REVIEW`; materialized files: `10446`; directories: `1270`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2156, build_download_install=2110, orchestration=2062, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2001`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52718`; percentage occurrences: `22237`.
- Markdown word count: `3554796`; heuristic sentence count: `674081`; sentence records indexed: `674081`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29838` metric claims; `10664` completion claims; `29741` metric and `10535` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9047` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13342`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40052` lines in `3673` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `290`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
