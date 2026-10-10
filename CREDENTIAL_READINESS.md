# QMOI Credential Readiness

## Current evidence

- Canonical local manager: `scripts/qmoi_credentials.py`, exposed through the Ollama agent's `credential-manager` command.
- Bitget tag: `bitget 27/9/2026`.
- Secret values have been removed from the Qtrade tail and stored encrypted outside the repository at `$HOME/.config/qmoi/credentials/vault.enc`; its key is at `$HOME/.config/qmoi/credentials/master.key`.
- The vault directory is mode `700`; key, encrypted data, lock, and audit files are mode `600`. The audit log stores provider, tag, operation, status, and timestamps only.
- The Qtrade metadata section reports the user-provided creation date `2026-09-27`; exact exchange-side creation time is unknown. Vault record `created_at`, `added_at`, `updated_at`, and `last_verified_at` are separately timestamped in UTC.
- Last read-only Bitget account check: `2026-09-27T20:12:47Z`, HTTP `400`, provider code `40085`, status `request_or_permission_rejected`. Credential validity is **not verified** and trading must remain disabled until the request/permission cause is resolved and a read-only check returns success.
- GitHub App authentication is separately blocked until the historically exposed key is confirmed revoked/rotated. File presence and restrictive modes are not proof of rotation.
- The autonomous inventory discovers local references to GitHub secrets, Actions variables, and runtime environment variables without reading values. Runtime presence is not validity proof; remote GitHub secret/variable configuration remains unknown unless an authorized read-only GitHub API check succeeds.
- The credential manager automatically prepares a name-only readiness inventory and provisioning checklist. It cannot issue provider credentials or create user accounts; values must be issued/rotated by the provider or authorized GitHub App owner, stored in an approved secret store, and validated before use.
- `.github/workflows/cross-repo-auth-preflight.yml` has a local, unverified optional App-token path using `APP_CLIENT_ID`/`APP_PRIVATE_KEY` or `QMOI_GITHUB_CLIENT_ID`/`QMOI_GITHUB_APP_ID`/`QMOI_GITHUB_PRIVATE_KEY` in Actions configuration, restricted to read-only scopes. Codespaces secrets do not flow into Actions; no remote run has verified that configuration.
- Name-only Codespace checks found `QMOI_GITHUB_APP_ID`, `QMOI_GITHUB_CLIENT_ID`, and `QMOI_GITHUB_PRIVATE_KEY` present, but `QMOI_GITHUB_INSTALLATION_ID` absent. Values were not inspected. Codespaces secrets do not automatically populate GitHub Actions; Action-side configuration remains unknown.
- Do not use the present App private-key variable until the owner confirms the historically exposed key was revoked and this value is its replacement. The App permission snapshot is broad and user-reported, not live-verified; review it for least privilege before any App operation.
- Copilot Chat and Ollama must not receive secret values in prompt/context. They may use only an explicitly authorized tool/workflow that reads a secret in-process, mints a short-lived scoped token, verifies identity and endpoint access, and emits value-free status. Secret presence alone is never authentication proof.
- Full available local audit at `2026-09-27T20:38:31Z`: active tree `131`, `Alpha-Q-ai-2025` `2,456`, `qmoi-enhanced-history-14` `2,045`, total `4,632` Markdown files; 5,189 source/config files scanned (excluding generated dependency/build trees); 33,299 current credential-related reference records; 3,167 credential-like historical commit/path candidates across 2,364 locally available commits and 30 refs. The mode-`600` report is `$HOME/.config/qmoi/credentials/credential-inventory.json`.
- Coverage is limited to the current materialized trees and local refs. Future commits, unfetched/private refs, external credential stores, binary files, and non-matching credential formats are not covered. No scan result is a guarantee that all credentials were found.
- The requested rotation playbook was absent from the local history materialization; a read-only remote QMOI `main` tree query returned no matching path. The new active policy is [CREDENTIALS_ROTATION_PLAYBOOK.md](CREDENTIALS_ROTATION_PLAYBOOK.md); parity with the unavailable historical file is unverified.
- No master-authenticated credential CRUD API/UI is independently verified. The vault supports internal record storage/update and read-only verification, but master identity/authorization must remain blocked until a signed, least-privilege control path and its tests exist.
- Successful Bitget spot account reads will include normalized balance rows stored only inside the encrypted vault. Current provider result `40085` means no balance was received; none is claimed or displayed.

## Agent contract

- Use `python scripts/ollama_autonomous_agent.py credential-manager --credential-action status` for metadata-only status.
- Use `python scripts/ollama_autonomous_agent.py credential-manager --credential-action audit` to scan every current Markdown file in the three materialized scopes, source/config candidates outside generated trees, and credential-like edits on local Git refs. The report is redacted and remains outside the checkout; future/unfetched/private refs require a later authorized refresh.
- Use `python scripts/ollama_autonomous_agent.py credential-manager --credential-action verify-bitget` for the signed read-only Bitget check and automatic refresh of the `bitget 27/9/2026` Qtrade metadata section.
- Use `python scripts/ollama_autonomous_agent.py credential-manager --credential-action migrate-qtrade` only when all expected fields parse and encrypted storage succeeds. The plaintext source tail is replaced only after successful vault persistence.
- Never print, log, commit, transmit, or put values into Qtrade, Markdown, telemetry, test output, artifacts, or cross-repository evidence. Tests use synthetic credentials only.
- On provider/network/API errors, preserve the encrypted record, record status/code/time only, set readiness to blocked or unknown, and prohibit trading, withdrawals, or other writes.
- Automatic replacement or rotation requires an explicitly authorized mapping, provider-supported rotation permission, successful verification of the replacement, a timestamped value-free audit entry, and secure removal of the old value. Do not copy Bitget values into another provider's fields.
- Inventory credentials across repositories as secret references and redacted locations. Keep each repo's Actions credentials in that repo's authorized GitHub-managed secrets; the local vault is not synced across repositories or machines.
- The local environment has no Python OS-keyring module. The current encrypted-file fallback protects against accidental repository exposure but is not hardware-backed and does not protect against compromise of the same local account. Production/multi-machine credentials should use an approved managed secret store.

## Metadata lifecycle

Each provider record tracks provider name, tags, source, reported source-created date, record creation/add/update times, last verification time/status, and value-free audit events. An exact upstream credential creation time must remain unknown unless the provider supplies it. Verification status is separate from storage status and from authorization to use a credential.

<!-- BEGIN QMOI MANAGED: wallet-bank-provider-credential-consumers -->
## Agent-managed wallet, bank, and trading credential consumers

The source-reference audit stores variable names and consumer paths only. It never reads `.env`, key/certificate files, encrypted vault contents, environment values, or provider responses.

- Discovered references: `1129`; provider groups: `{"binance": 16, "bitget": 118, "cashon": 9, "github": 100, "huggingface": 10, "megavault": 11, "paypal": 22, "pesapal": 10, "stripe": 3, "unmapped_provider": 830}`.
- Consumer map: `QMOItracks/credential_reference_inventory.json`; `credential_values_read_from_secret_stores=false`; `credential_values_persisted_or_emitted=false`.
- Generic vault storage does not mean an account or provider adapter is verified. Only the Bitget read-only verifier exists in the active credential manager; its last evidence is a rejected request (`40085`) and is not success. Other providers remain unverified here.
- Banks, wallets, exchanges, payment APIs, and webhooks require provider-specific verification, minimum scopes, expiry/rotation policy, and tested consumers. Unknown owners or verifiers remain `blocked`.
<!-- END QMOI MANAGED: wallet-bank-provider-credential-consumers -->

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
