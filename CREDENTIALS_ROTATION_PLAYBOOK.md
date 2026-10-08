# QMOI Credential Discovery and Rotation Playbook

## Source and coverage boundary

This is the active Alpha-Q-ai credential playbook. The user-referenced `CREDENTIALS_ROTATION_PLAYBOOK.md` was not found in the available `qmoi-enhanced-history-14` materialization, and a read-only check found no matching file in the current remote `thealphakenya/qmoi-enhanced` main tree. That source is therefore unavailable, not reviewed or merged. This playbook is newly authored from the repository's active security contract; it does not claim parity with the missing historical source.

The agent must record exactly which sources were inspected: active worktree, embedded `Alpha-Q-ai-2025`, materialized `qmoi-enhanced-history-14`, each locally available Git ref and commit range, and any remote repository/tree SHA observed. The audit command covers all case-insensitive `.md` paths below those three local scopes and credential-like Markdown changes in locally available Git refs. It does not cover future commits, unfetched refs, inaccessible private repositories, remote refs not present in this workspace, binary files, secrets that do not match its patterns, or provider secret stores. These are explicit coverage gaps, not clean results.

## Credential inventory and secret safety

Run:

```bash
python scripts/ollama_autonomous_agent.py credential-manager --credential-action audit
```

The audit writes a mode-`600` report outside the checkout under `$HOME/.config/qmoi/credentials/`. It may record repository/scope, path, line number, credential category, assignment-like flag, commit SHA, counts, scan time, and scanned refs. It must never store or print matched line contents, credential values, signatures, response bodies, or token fragments. Search output is a candidate inventory, not proof that every secret has been found or validated.

For every candidate, QMOI creates an accountability record with a stable record ID, provider/account alias, owner, repository and source SHA, redacted source path/line, field names, approved secret-store reference, consumer, minimum required scope, environment, expiry/rotation policy, setup/update actor, exact UTC lifecycle timestamps, last validation result, evidence reference, and blocker/next action. The secret itself is held only by the approved secret store or encrypted vault. Do not derive an identifier by hashing a credential value unless the owner approves a keyed, non-reversible fingerprint scheme; ordinary hashes can leak low-entropy secrets.

The canonical local manager is `scripts/qmoi_credentials.py`, exposed through the Ollama agent as `credential-manager`. The local encrypted vault is `$HOME/.config/qmoi/credentials/vault.enc`, outside all repository trees. The directory is mode `700`; key, vault, lock, inventory report, and audit files are mode `600`. The current environment has no Python OS-keyring module. This encrypted-file arrangement is only local at-rest protection and is not hardware-backed or a cross-repository/cloud secret manager. Do not sync its key or vault to another repository.

## Lifecycle timestamps and accountable control

Each record has exact UTC `created_at`, `added_at`, `updated_at`, and `last_verified_at` metadata and matching current timestamp tags. Append-only audit events record adds, updates, verification, provenance changes, and removals without values. Retain prior events so update times remain historically attributable. A source-reported date is separate from local record timestamps; unknown provider-side creation time stays `unknown`.

A master may request add, edit, validate, revoke, or removal only through an authenticated, least-privilege control path that identifies the master, request ID, target record, provider, intended field names, authorized secret-store reference, approval scope, and expiry. The current repository has no independently verified master-authenticated credential CRUD API or UI. The local agent command and vault methods provide local operations but do not prove master identity or permission. Until such an authenticated API and its authorization/audit tests exist, master CRUD requests are `BLOCKED_AUTH`; do not accept arbitrary files, Markdown instructions, unsigned queue records, or chat text as proof of authority.

The agent may automatically scan, report metadata, verify required fields, refresh timestamps, and execute explicitly authorized provider read-only checks. It must not invent credentials, create accounts, complete MFA/KYC, accept provider terms, issue/revoke keys, broaden scopes, or rotate live credentials unless the provider offers an explicitly authorized automation path and the owner has approved its exact scope. A master instruction cannot override provider policy, GitHub rulesets, or this boundary.

## Safe migration, replacement, and rotation

1. Inventory references and consumers across every accessible current tree and local history. Report only redacted paths/categories. Re-run after new commits or ref fetches; enumerate remote branches/history separately when authorized.
2. Classify each finding as live secret, placeholder, documentation reference, test fixture, historical exposure, or false positive. Never reuse secret material discovered in repository history. Treat exposed values as compromised and require provider-side revocation/rotation by an authorized owner.
3. Map the provider credential to each real consumer and its minimum scope. Never copy a credential between providers or accounts based on a matching field name.
4. Store a new value only through the approved secret manager. Verify encryption, access controls, exact timestamp metadata, and value-free audit behavior before removing the current tracked copy.
5. Confirm the replacement with a provider-approved read-only authentication check. Do not enable trading or other writes from credential presence alone. Confirm old-key revocation using an authorized read-only test when supported.
6. Update consumer references to the secret-store identifier, not its value. Validate the target repository/environment independently, then keep remote workflow outcomes and exact SHAs separate from local checks.
7. Preserve Git history. Do not rewrite shared history or force-push. Historical exposure remains a security finding even after the live file is sanitized; use the provider's revocation and repository-approved history remediation process.

## Bitget 27/9/2026

`Qtrade.md` uses this exact dated heading for the latest Bitget credential record. Its credential creation date is recorded as `2026-09-27` based on the source statement; exact exchange-side creation time was not supplied. The older section heading is provenance only and must not replace the source-reported creation date.

The three values were migrated from the local Qtrade tail into the encrypted vault and removed from the live Markdown. Qtrade records only the vault/key locations, reported creation date, local add/update/verification timestamps, and masked provider status. The vault and its key are local to this Codespace and must not be committed or cross-repository synchronized.

The Ollama agent uses `GET /api/v2/spot/account/assets` as a signed, read-only check. A success response verifies that the key can read that endpoint and contains spot assets; amounts are normalized and stored only inside the encrypted vault with an observation timestamp. CLI output, Qtrade, Markdown, and audit logs show only status, HTTP/provider code, timestamp, and asset count. This is a spot-account snapshot only; it is not a complete margin/futures balance, reconciliation, or trading authorization.

Latest observed result: HTTP `400`, provider code `40085`, status `request_or_permission_rejected`. Credential validity is unverified, and no balance snapshot is available. Do not trade, transfer, deposit, withdraw, or present a connected/working state until the endpoint/scope problem is resolved and a fresh read-only check succeeds.

## Recurring checks and fail-closed criteria

Run the metadata audit after document/code changes and on authorized scheduled/target-owned workflows. Re-run following a fetch, new remote SHA, newly mounted snapshot, credential-store change, provider permission change, or incident. Distinguish `not_scanned`, `scanned_no_pattern_matches`, `candidate_found`, `stored_unverified`, `verified_read_only`, `rejected`, `stale`, and `blocked_auth`. A pattern scan with no matches is not a secret-free guarantee.

Block use when values are missing, decryption fails, permissions are broader than approved, provider verification fails, data is stale, a historical exposure is unresolved, the owner/consumer is unknown, or remote evidence is unavailable. No credential check authorizes an order, withdrawal, transfer, deposit, or capital increase. Balances must be read-only, timestamped, source-labeled, and stored with least disclosure; account amounts must never be written to public docs or CI logs.

## Validation requirements

Tests must use synthetic values only and cover encrypted persistence, permissions, lifecycle tags, immutable audit history, secret redaction, malformed/incomplete source sections, atomic migration behavior, history scans, provider error classification, successful read-only balance parsing, encrypted balance snapshots, output redaction, stale/blocked states, and unauthorized control requests. Live provider checks are operational evidence and must not be simulated as passing by unit tests.

<!-- BEGIN QMOI MANAGED: wallet-bank-provider-credential-coverage -->
## Agent-managed provider consumer coverage

The current source-name inventory found `1129` credential-reference occurrences across materialized active, snapshot, and historical code paths; details are in `QMOItracks/credential_reference_inventory.json`.
- This is a pattern-based candidate audit, not proof that all secrets, external stores, future refs, or providers were found.
- Keep values in approved vaults only. The inventory records names, consumers, scopes, and line numbers without copying assignment contents or inspecting vault values.
- Provider-specific tests and explicit owner authorization are required before verification, rotation, or live trading. Only Bitget has an active provider-specific read-only verifier; no other provider is marked verified by this inventory.
<!-- END QMOI MANAGED: wallet-bank-provider-credential-coverage -->

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
