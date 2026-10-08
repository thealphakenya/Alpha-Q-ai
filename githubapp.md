# QMOI Dual Repository Agent

## Current safety status (2026-09-28T02:45:47Z)

- Correlation ID: `3f5e3904-b367-405d-bb0e-fc4d7ef2882d`.
- The authenticated CLI identity is GitHub user `themegakenya`, not verified App authentication. The current App key remains rotation-unverified and is not used.
- Read-only SHA observations: Alpha-Q-ai `main` `68de1f1962a52a9c16d722a905f818ddf73e2949`; qmoi-enhanced `main` `28a87cc43cbf9dce8f7ecb53518d5d845de586fe`.
- Alpha-Q-ai `Push on main` run `36370328749` is still in progress on the observed Alpha SHA; JavaScript/TypeScript analysis is pending. Branch-protection GET returned HTTP 403 `Resource not accessible by integration`.
- No App JWT/token, dispatch, or remote mutation was attempted. Remote completion and cross-repository/backup parity are not proven.

## Current safety status (2026-09-27T22:19:12Z)

- Correlation ID: `c7668de2-4209-4bf7-9f83-d15490bf33b9`.
- GitHub CLI user `qmoialpha-star` can read current repository refs and workflow metadata, but is not App authentication. Both `main` branch-protection reads returned HTTP 403; no dispatch or mutation authority is inferred.
- Current remote `main` SHAs are Alpha-Q-ai `1a7eb987f18358b1508ea868feecde89fa18959a` and qmoi-enhanced `df3f34fb4733ed5cd4d25107b9d056de9697fcbe`. Push workflows succeeded at those SHAs, but Alpha's latest observed PR tracker failed at an older SHA and qmoi-enhanced cross-repository autosync failed at an older SHA.
- App-key rotation is not independently confirmed. Treat the historical key as compromised; do not use present local key material, create a JWT/token, or call App APIs until the App owner confirms rotation and the replacement is securely installed.
- Remote completion remains blocked by protection authorization, failed/stale automation evidence, unproven cross-repository/backup parity, and local divergence. See [remotecompletion.md](remotecompletion.md) and [oe2.txt](oe2.txt).

## Current safety status (2026-09-27T20:33:40Z)

- Correlation ID: `e0809d88-9e0a-42fa-9c5c-adaa18d554d2`.
- App use remains blocked: protected credential-file presence/modes do not establish key rotation, and the historical key remains classified as compromised. No App JWT, installation token, or App API request was made in this checkpoint.
- The separate GitHub CLI user is `qmoialpha-star`; current target branch-protection reads previously returned HTTP 403. No dispatch, mutation, or protected-branch authority is claimed.
- Latest Alpha-Q-ai `main` SHA observed: `95f24dce8877c95138c54e654ce4ed2dda3644dc`; its push workflow was still in progress. See [github.md](github.md) and [remotecompletion.md](remotecompletion.md) for the read-only checkpoint.

## Current App authentication status (2026-09-27)

- Correlation ID: `c46ede71-59c1-4210-93b4-1c93c9bc4569`.
- Local metadata only: `credentials.env` and `private-key.pem` are present under `$HOME/.config/alpha-q-ai/github-app/`, with directory mode `700` and file modes `600`.
- Rotation state: the files' metadata does not prove that the private key is newly rotated. Repository policy records the historical key as compromised; the present key must not be used for App authentication until the App owner confirms revocation/rotation and securely installs a verified replacement.
- No GitHub App JWT or installation token was created in this session. No App API request, dispatch, or mutation was attempted.
- `gh auth status` identified the Codespace's separate user session as `qmoialpha-star`; it is not GitHub App authentication.
- Read-only user-session evidence at `2026-09-27T20:09:16Z`: Alpha-Q-ai `main` SHA `a51b1f36bb3ca249cf5cab3fa00616065ae0f8f0`; qmoi-enhanced `main` SHA `76306f983d19127dea9a446e0aa22d42006f9d9f`. Both main-branch protection reads returned HTTP 403 `Resource not accessible by integration`.
- Result: `APP_AUTH_BLOCKED_ROTATION_UNVERIFIED`. Do not authenticate, dispatch, mutate, or claim App authorization until the replacement key is independently confirmed.

## Credential migration and authentication verification (2026-09-25T22:02:13Z)

- Correlation ID: `026ff4e5-97d8-451f-88fe-cfedc67f6c7e`.
- Repository/ref/SHA: `thealphakenya/Alpha-Q-ai`, `main`, `a33e627c3ac123bd47b3aafbdb30b8a973256670`.
- Read-only authentication: `GET /app` returned HTTP 200 for `qmoi-dual-repository-agent`; `GET /repos/thealphakenya/Alpha-Q-ai/installation` returned HTTP 200 for account `thealphakenya` with selected-repository installation.
- A five-minute App JWT existed only in process memory. No installation access token was created or saved.
- App and Client IDs are stored outside the checkout in `$HOME/.config/alpha-q-ai/github-app/credentials.env` (directory mode `700`, file mode `600`). The replacement-key path is `$HOME/.config/alpha-q-ai/github-app/private-key.pem`.
- Blocker: the old PEM is present in `origin/main` history. It was removed from the working tree and local credential store, but history still contains it. Rotate/delete that key in GitHub App settings and install a replacement at the path above before any further App authentication; rotation is not yet verified.

## Verified GitHub App authentication (2026-09-25T02:45:05Z)

- Correlation ID: `remote-completion-alpha-q-ai-2026-09-25-024505`.
- The uploaded private key was validated locally with mode `600`; its value was never printed or persisted to evidence.
- GitHub App JWT identity probe: HTTP 200.
- App installation discovery: HTTP 200; installation matched `thealphakenya`.
- Short-lived installation token mint: HTTP 201; token remained in memory only.
- Read-only repository probes returned HTTP 200 for `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`.
- Actions permission probes returned HTTP 200 with Actions enabled for both repositories.
- `main` branch-protection probes returned HTTP 404 for both repositories. This is ambiguous remote evidence, not proof that protection is absent or that mutation is authorized.
- Result: `APP_AUTHENTICATED_READ_ONLY`. No dispatch, branch mutation, merge, release, or deployment was attempted.

## Installation record
Retired private-key fingerprint omitted; the former key appears in remote history and must not be reused.

This document records the GitHub App installation reported by the repository owner
on 2026-09-25. It is an operational record, not independent proof that every
permission is usable by the current Codespaces token.

| Field | Value |
| --- | --- |
| App | QMOI Dual Repository Agent |
| Developer | thealphakenya |
| Developer profile | https://github.com/thealphakenya |
| Purpose | Autonomous development, repository management, CI/CD, workflow orchestration, monitoring, cross-repository synchronization, and QMOI automation |
| Installation scope | All repositories is available; the installation currently selects 2 repositories |
| Selected repositories | `thealphakenya/Alpha-Q-ai`, `thealphakenya/qmoi-enhanced` |
| Public repositories | Read-only access may include public repositories |
| Installation time | Reported as 2026-09-25; verify from GitHub when auditing the installation |

## Permission contract

The installation reports read access to Codespaces metadata and repository
metadata. It reports read/write access to the following capability families:


The exact effective permission set must be re-read from GitHub for each target
repository. An app installation permission is not the same thing as a workflow's
`GITHUB_TOKEN` permission, a user token scope, an environment approval, a ruleset
exception, or an organization policy decision.

## Event subscriptions are separate from permissions

| Permissions | What is QMOI allowed to access or change? | Read/write code, manage PRs, manage Actions, manage issues, security, deployments, and secrets |
| Event subscriptions | What should GitHub tell QMOI about? | Push, pull request, workflow run, workflow job, check run, security alerts, deployment, and repository dispatch |

The app should subscribe to the events needed by the monitoring and orchestration
side, while still checking the matching permission before taking action:

| Event | Use in QMOI monitoring/orchestration | Action gate |
| --- | --- | --- |
| `push` | Refresh the source SHA, documentation inventories, and synchronization plan | Contents access and target policy |
| `pull_request` | Validate, review, update, and observe PR lifecycle state | Pull requests and Contents access |
| `workflow_run` | Track workflow dispatch, conclusion, ref, SHA, and artifacts | Actions access; delivery alone is not completion |
| `workflow_job` | Monitor individual jobs, logs metadata, runners, and failures | Actions access and permitted log/artifact access |
| `check_run` | Evaluate required checks and report terminal conclusions | Checks access |
| `security_advisory` and security-alert events | Surface Dependabot, code-scanning, and secret-scanning changes | The applicable security-event and alert permissions |
| `deployment` and `deployment_status` | Track deployment creation, status, URL, and source SHA | Deployments, environments, Pages, or provider access as applicable |
| `repository_dispatch` | Receive an explicitly authorized cross-repository orchestration request | Dispatch reception plus target mutation permissions |

The important monitoring set for this installation is `workflow_run`,
`workflow_job`, `check_run`, `push`, `pull_request`, and `repository_dispatch`,
with security and deployment events included for their respective gates. A
delivered event is only an observation. Before responding, QMOI must verify the
installation, repository, ref/SHA, event authenticity, current permissions,
branch/ruleset state, and idempotency key. If the required permission is missing,
the event is recorded as `AUTH_BLOCKED` and no mutation is attempted.

## How the app is used

### 1. Authentication and preflight

Before an operation, the controller should identify the app installation and
repository, request a short-lived installation token through the authorized
GitHub App flow, and run read-only checks for identity, repository access,
Actions access, workflow existence, target ref, rulesets, environments, and
required checks. Tokens and private keys must never be written to this file,
logs, artifacts, prompts, or evidence records.

Every preflight record includes:

- correlation ID, source repository, target repository, actor/app identity, and ref;
- requested endpoint class and required permission;
- sanitized HTTP status and failure class;
- source and target SHA when available; and
- the next action when access is denied or evidence is incomplete.

A `403` is `AUTH_BLOCKED`, not success. A `404` remains ambiguous until identity,
installation, repository, endpoint, method, ref, and authorization have been
checked.

### 2. Repository and cross-repository work

For `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`, the app may
coordinate read, inventory, validation, PR, workflow, artifact, deployment, and
synchronization operations when the installation and target policy authorize
them. Cross-repository work must explicitly name both source and target; access
to one repository is never inferred for the other.

The merge controller uses the app to compare current trees and the available
`Alpha-Q-ai-2025` and `qmoi-enhanced-history-14` projections, detect duplicate and
variant paths, and prepare a plan. It must not silently overwrite product
identity, app-specific features, icons, history, memory, or platform behavior.
Variant conflicts require provenance, feature review, validation, and an
approved target-owned mutation path.

### 3. API, endpoint, route, and port inventories

The app-backed remote workflows should refresh and validate `API.md`,
`ENDPOINTS.md`, `ROUTES.md`, and `ALLPORTS.md` from both repositories and their
approved history projections. Each generated record should retain source path,
repository, ref/SHA, timestamp, and hash or other provenance. Missing source
trees are reported as unavailable; they are never replaced with guessed data.

The same inventory contract applies to apps, platforms, components, `.ts`,
`.tsx`, `.py`, build, install, download, deployment, Vercel, and memory surfaces.
`ALLMDFILESREFS.md` remains the index of the resulting documentation and must be
refreshed after a new canonical Markdown file is added.

### 4. Actions, CI/CD, and monitoring

The app can support target-owned workflow dispatch, workflow inspection, checks,
statuses, artifacts, deployment records, Pages, and live monitoring when the
installation token and repository policy permit each operation. Heavy validation
and repository mutation stay in target-owned workflows. The Codespace may
submit, observe, and verify; it must not convert dispatch acceptance into a
completion claim.

A workflow operation is complete only after all of the following are recorded:

1. target workflow and exact ref/SHA;
2. run ID and job conclusions;
3. required checks and security gates;
4. resulting PR, merge, artifact, release, or deployment identifiers;
5. independently observed target state and final SHA; and
6. evidence in `remote-evidence-ledger.jsonl`, `remote-completion.json`, and the
   applicable runbook files.

### 5. Merge, backup, release, and deployment

The app may coordinate PRs, merge queues, protected-branch workflows, backup
synchronization, releases, packages, deployments, and Vercel redeployments only
through the policy-compatible target-owned path. Required reviews, rulesets,
environment approvals, security findings, and required checks remain gates.

`autosync-backup` is synchronized only when a target-owned run proves the backup
SHA equals the verified target SHA. A release requires its source SHA, release
ID, artifact hashes, installation/runtime checks, and remote retrieval evidence.
A deployment requires its target URL or deployment ID, source SHA, terminal
result, and independent availability verification.

## Ensuring required access without bypassing controls

The app cannot grant itself new permissions or override GitHub policy. The
installation administrator must keep both repositories selected and must approve
permission changes, organization policies, environments, secrets, rulesets, and
branch protection as needed. The controller should continuously surface missing
capabilities through a preflight matrix rather than retrying blindly.

The minimum capability groups for the remote-completion lifecycle are:

| Lifecycle action | Minimum capability to verify |
| --- | --- |
| Read source and history | Metadata and Contents read |
| Inspect and dispatch Actions | Actions read/write and workflow access |
| Create/update branches and PRs | Contents write and Pull requests write |
| Read required checks | Checks and commit statuses read |
| Merge protected branches | Repository write plus ruleset-compatible authority, reviews, and checks |
| Synchronize backup branches | Contents write plus branch-policy compatibility |
| Manage releases and artifacts | Contents/releases, Actions/artifact, packages as applicable |
| Deploy and verify | Deployments, environments, Pages or provider-specific access as applicable |
| Audit security blockers | Security-events and relevant alert read/write permissions |
| Cross-repository operation | The same verified capability on each target repository |

If a capability is absent, stale, denied, or only locally inferred, the operation
stops with a named blocker and remediation. It does not downgrade to an unsafe
credential, print a secret, bypass a ruleset, force-push, or claim completion.

## Current evidence and blockers

The user-reported installation details above are the current installation record.
Existing repository evidence separately records that the Codespaces integration
received `HTTP 403: Resource not accessible by integration` for Actions and
branch-protection checks on 2026-09-24. Therefore this document does not claim
that remote completion is currently unblocked.

Remote completion remains blocked until an authorized app installation token or
user-owned credential independently proves, for both repositories:

- identity and installation access;
- Actions/workflow dispatch and observation;
- contents, PR, checks, merge-queue, ruleset, and protected-branch compatibility;
- backup and cross-repository parity;
- security-gate status; and
- terminal target-owned workflow results with exact final SHAs.

Reference contracts: [CROSS_REPO_PERMISSION_MATRIX.md](CROSS_REPO_PERMISSION_MATRIX.md),
[remotecompletion.md](remotecompletion.md), [remote-completion.json](remote-completion.json),
[QMOIGITHUBAPP.md](QMOIGITHUBAPP.md), and [oe2.txt](oe2.txt).

## App Authentication Probe (2026-09-25T01:34:39Z)

- Correlation ID: `remote-completion-alpha-q-ai-2026-09-25-013439`.
- The Codespace exposes only generic GitHub/Codespaces token variables; no GitHub App ID, private key, or installation token credential is configured.
- GitHub API `/app` returned HTTP 401 `A JSON web token could not be decoded` with the current credential. `/user/installations` returned no installations.
- Both target repositories remain readable, but Actions permission and protected-branch probes still return HTTP 403 `Resource not accessible by integration`.
- Result: `APP_AUTH_UNAVAILABLE`; this environment cannot switch to the reported App installation without administrator-provided App credentials or a target-owned workflow that mints the short-lived installation token.
- Required remediation: configure the App ID/private key and installation ID only in GitHub-managed secrets or an authorized external runner, mint a short-lived installation token for both repositories, rerun identity/permissions/protection preflight, and record terminal workflow evidence before any completion claim.

## Fresh two-repository probe (2026-09-25T02:10:57Z)

- Correlation ID: `remote-completion-alpha-q-ai-2026-09-25-021057`.
- Both target repositories remain readable as `qmoialpha-star` with repository `push=true`, but Actions permissions and `main` branch-protection endpoints return `HTTP 403 Resource not accessible by integration` for each target.
- A bounded dispatch of `ollama-autonomous-agent.yml` in `thealphakenya/qmoi-enhanced` also returned `HTTP 403`; no workflow run or downstream evidence exists for this attempt.
- The active Codespace still has no usable App JWT or installation token. This confirms the reported installation record is documentation, not proof of effective App authentication.
- Result: `APP_AUTH_UNAVAILABLE` and `REMOTE_COMPLETION_BLOCKED`; no secret was printed, copied, persisted, or requested.
- Required next action: an administrator must expose the App through a target-owned token-minting workflow or provide an authorized user-owned credential through GitHub-managed secret/configuration, then rerun both-repository identity, permission, protection, dispatch, terminal-run, and SHA verification gates.








Yes—but only if you want code running inside the Codespace itself to authenticate as the GitHub App.
Since you have already installed QMOI Dual Repository Agent on both Alpha-Q-ai and qmoi-enhanced, the installation is done. The remaining issue is authentication.
Your setup should be
                 QMOI Dual Repository Agent
                                             │
                                                              Installed on @thealphakenya
                                                                                          │
                                                                                                        ┌─────────────┴─────────────┐
                                                                                                                      │                           │
                                                                                                                              Alpha-Q-ai                  qmoi-enhanced
                                                                                                                                            │                           │
                                                                                                                                                          └─────────────┬─────────────┘
                                                                                                                                                                                      │
                                                                                                                                                                                                        GitHub App credentials
                                                                                                                                                                                                                                    │
                                                                                                                                                                                                                                                     Installation token
                                                                                                                                                                                                                                                                                 │
                                                                                                                                                                                                                                                                                                  ┌──────────┴──────────┐
                                                                                                                                                                                                                                                                                                                   │                     │
                                                                                                                                                                                                                                                                                                                              GitHub Actions          Codespace
                                                                                                                                                                                                                                                                                                                              The installation alone does not give your Codespace the App's private key. A private key is required when software needs to authenticate as the App and generate an installation access token. �
                                                                                                                                                                                                                                                                                                                              GitHub Docs +1
                                                                                                                                                                                                                                                                                                                              What I recommend for your QMOI architecture
                                                                                                                                                                                                                                                                                                                              If QMOI primarily runs through GitHub Actions
                                                                                                                                                                                                                                                                                                                              Do NOT put the private key in the Codespace.
                                                                                                                                                                                                                                                                                                                              Put it in Actions Secrets in both repositories:
                                                                                                                                                                                                                                                                                                                              APP_PRIVATE_KEY
                                                                                                                                                                                                                                                                                                                              and put your App's Client ID in Actions Variables:
                                                                                                                                                                                                                                                                                                                              APP_CLIENT_ID
                                                                                                                                                                                                                                                                                                                              Then your workflow generates a short-lived installation token:
                                                                                                                                                                                                                                                                                                                              - name: Create QMOI GitHub App token
                                                                                                                                                                                                                                                                                                                                id: app-token
                                                                                                                                                                                                                                                                                                                                  uses: actions/create-github-app-token@v3
                                                                                                                                                                                                                                                                                                                                    with:
                                                                                                                                                                                                                                                                                                                                        client-id: ${{ vars.APP_CLIENT_ID }}
                                                                                                                                                                                                                                                                                                                                            private-key: ${{ secrets.APP_PRIVATE_KEY }}
                                                                                                                                                                                                                                                                                                                                            GitHub specifically documents this architecture for GitHub Apps accessing resources beyond the workflow's own repository. �
                                                                                                                                                                                                                                                                                                                                            GitHub Docs
                                                                                                                                                                                                                                                                                                                                            The resulting token can then be used by your QMOI agent to access both repositories, because your App installation has access to both.
                                                                                                                                                                                                                                                                                                                                            If you want QMOI running directly inside a Codespace
                                                                                                                                                                                                                                                                                                                                            Then yes, the Codespace needs access to the private key.
                                                                                                                                                                                                                                                                                                                                            But don't put:
                                                                                                                                                                                                                                                                                                                                            qmoi-app.pem
                                                                                                                                                                                                                                                                                                                                            in Git.
                                                                                                                                                                                                                                                                                                                                            Instead, use a Codespaces secret.
                                                                                                                                                                                                                                                                                                                                            Go to:
                                                                                                                                                                                                                                                                                                                                            GitHub → Settings → Codespaces → Codespaces secrets → New secret
                                                                                                                                                                                                                                                                                                                                            Create:
                                                                                                                                                                                                                                                                                                                                            QMOI_APP_PRIVATE_KEY
                                                                                                                                                                                                                                                                                                                                            Paste the complete PEM private key as the value.
                                                                                                                                                                                                                                                                                                                                            GitHub allows account-level Codespaces secrets to be restricted to specific repositories, so you can give the secret access to both:
                                                                                                                                                                                                                                                                                                                                            Alpha-Q-ai
                                                                                                                                                                                                                                                                                                                                            qmoi-enhanced
                                                                                                                                                                                                                                                                                                                                            �
                                                                                                                                                                                                                                                                                                                                            GitHub Docs +1
                                                                                                                                                                                                                                                                                                                                            You can also create a second Codespaces secret:
                                                                                                                                                                                                                                                                                                                                            QMOI_APP_CLIENT_ID
                                                                                                                                                                                                                                                                                                                                            Then your Codespace can access them as environment variables.
                                                                                                                                                                                                                                                                                                                                            GitHub explicitly recommends development-environment secrets for sensitive credentials used inside Codespaces. �
                                                                                                                                                                                                                                                                                                                                            GitHub Docs
                                                                                                                                                                                                                                                                                                                                            Important: Codespaces secrets ≠ Actions secrets
                                                                                                                                                                                                                                                                                                                                            This distinction matters for your setup.
                                                                                                                                                                                                                                                                                                                                            Credential
                                                                                                                                                                                                                                                                                                                                            Where
                                                                                                                                                                                                                                                                                                                                            Used by
                                                                                                                                                                                                                                                                                                                                            QMOI_APP_PRIVATE_KEY
                                                                                                                                                                                                                                                                                                                                            Codespaces secret
                                                                                                                                                                                                                                                                                                                                            Code running inside Codespace
                                                                                                                                                                                                                                                                                                                                            APP_PRIVATE_KEY
                                                                                                                                                                                                                                                                                                                                            Actions repository secret
                                                                                                                                                                                                                                                                                                                                            GitHub Actions
                                                                                                                                                                                                                                                                                                                                            QMOI_APP_CLIENT_ID
                                                                                                                                                                                                                                                                                                                                            Codespaces secret/variable
                                                                                                                                                                                                                                                                                                                                            Codespace
                                                                                                                                                                                                                                                                                                                                            APP_CLIENT_ID
                                                                                                                                                                                                                                                                                                                                            Actions variable
                                                                                                                                                                                                                                                                                                                                            GitHub Actions
                                                                                                                                                                                                                                                                                                                                            Installation token
                                                                                                                                                                                                                                                                                                                                            Generated at runtime
                                                                                                                                                                                                                                                                                                                                            QMOI/GitHub API
                                                                                                                                                                                                                                                                                                                                            GitHub Actions cannot access Codespaces secrets. �
                                                                                                                                                                                                                                                                                                                                            GitHub Docs
                                                                                                                                                                                                                                                                                                                                            So if your autonomous agent is GitHub-hosted through Actions, give Actions its own protected secret. If you're running the agent interactively inside Codespaces, give the Codespace its own secret.
                                                                                                                                                                                                                                                                                                                                            For your particular QMOI setup
                                                                                                                                                                                                                                                                                                                                            Because you want both repositories to be able to control/update each other, I'd configure both execution environments:
                                                                                                                                                                                                                                                                                                                                            Alpha-Q-ai
                                                                                                                                                                                                                                                                                                                                            Actions:
                                                                                                                                                                                                                                                                                                                                            APP_CLIENT_ID
                                                                                                                                                                                                                                                                                                                                            APP_PRIVATE_KEY
                                                                                                                                                                                                                                                                                                                                            Codespaces:
                                                                                                                                                                                                                                                                                                                                            QMOI_APP_CLIENT_ID
                                                                                                                                                                                                                                                                                                                                            QMOI_APP_PRIVATE_KEY
                                                                                                                                                                                                                                                                                                                                            qmoi-enhanced
                                                                                                                                                                                                                                                                                                                                            Actions:
                                                                                                                                                                                                                                                                                                                                            APP_CLIENT_ID
                                                                                                                                                                                                                                                                                                                                            APP_PRIVATE_KEY
                                                                                                                                                                                                                                                                                                                                            Codespaces:
                                                                                                                                                                                                                                                                                                                                            QMOI_APP_CLIENT_ID
                                                                                                                                                                                                                                                                                                                                            QMOI_APP_PRIVATE_KEY
                                                                                                                                                                                                                                                                                                                                            You don't need a different GitHub App or private key for each repository. The same App installation can authorize access to both repositories.
                                                                                                                                                                                                                                                                                                                                            Then test it before integrating everything
                                                                                                                                                                                                                                                                                                                                            From a Codespace, your QMOI authentication layer should effectively do:
                                                                                                                                                                                                                                                                                                                                            Private key
                                                                                                                                                                                                                                                                                                                                                 ↓
                                                                                                                                                                                                                                                                                                                                                 GitHub App JWT
                                                                                                                                                                                                                                                                                                                                                      ↓
                                                                                                                                                                                                                                                                                                                                                      App installation
                                                                                                                                                                                                                                                                                                                                                           ↓
                                                                                                                                                                                                                                                                                                                                                           Installation access token
                                                                                                                                                                                                                                                                                                                                                                ↓
                                                                                                                                                                                                                                                                                                                                                                GitHub API
                                                                                                                                                                                                                                                                                                                                                                     ↓
                                                                                                                                                                                                                                                                                                                                                                     Alpha-Q-ai
                                                                                                                                                                                                                                                                                                                                                                          +
                                                                                                                                                                                                                                                                                                                                                                          qmoi-enhanced
                                                                                                                                                                                                                                                                                                                                                                          GitHub's App authentication model is specifically designed around this App → installation → installation-token flow. �
                                                                                                                                                                                                                                                                                                                                                                          GitHub Docs
                                                                                                                                                                                                                                                                                                                                                                          And the installation token is temporary, rather than a permanent credential. That is preferable to putting a long-lived PAT into the Codespace.
                                                                                                                                                                                                                                                                                                                                                                          One security rule I'd strongly keep
                                                                                                                                                                                                                                                                                                                                                                          Never commit the .pem file, private key, JWT, or installation token to either repository.
                                                                                                                                                                                                                                                                                                                                                                          GitHub describes the App private key as the App's most valuable secret and recommends keeping it securely stored. �
                                                                                                                                                                                                                                                                                                                                                                          GitHub Docs +1
                                                                                                                                                                                                                                                                                                                                                                          So your current situation is:
                                                                                                                                                                                                                                                                                                                                                                          App installed on both repos → ✅ done
                                                                                                                                                                                                                                                                                                                                                                          App permissions → ✅ done
                                                                                                                                                                                                                                                                                                                                                                          Repository access → ✅ done
                                                                                                                                                                                                                                                                                                                                                                          Private key securely stored → next step
                                                                                                                                                                                                                                                                                                                                                                          Generate installation token → next step
                                                                                                                                                                                                                                                                                                                                                                          Test access to both repos → next step
                                                                                                                                                                                              Credential cleanup record: the copied App ID, Client ID, and private-key fingerprint were removed from this tracked document. No private key or installation token was present to relocate. Store the App private key only in GitHub-managed Actions/Codespaces secrets and retrieve short-lived installation tokens at runtime; never place credential values in repository files, chat, logs, or evidence.

                                                                                                                                                                 Client secrets
                                                                                                                                                                 You need a client secret to authenticate as the application to the API.

                                                                                                                                                                 Basic information
                                                                                                                                                                 GitHub App name
                                                                                                                                                                 QMOI Dual Repository Agent
                                                                                                                                                                 The name of your GitHub App.

                                                                                                                                                                 Write
                                                                                                                                                                 Preview
                                                                                                                                                                 Autonomous development, repository management, CI/CD, workflow orchestration, monitoring, cross-repository synchronization, and automation for QMOI projects.
                                                                                                                                                                 Homepage URL
                                                                                                                                                                 https://github.com/thealphakenya
                                                                                                                                                                 The full URL to your GitHub App’s website.

                                                                                                                                                                 Identifying and authorizing users
                                                                                                                                                                 The URIs to redirect to after a user authorizes your application. You may add up to 10 redirect URIs. Wildcard matching allows tokens to be sent to all subdomains and additional paths of the redirect URI. Only enable this if you are sure you have control over all possible matches. Learn more about secure use of redirect URIs.
                                                                                                                                                                 Redirect URI
                                                                                                                                                                 e.g. https://example.com/auth
                                                                                                                                                                  Allow wildcard matching
                                                                                                                                                                   Request user authorization (OAuth) during installation
                                                                                                                                                                   Requests that the installing user grants access to their identity during installation of your App.

                                                                                                                                                                    Enable Device Flow
                                                                                                                                                                    Allow this GitHub App to authorize users via the device flow.

                                                                                                                                                                    Post installation
                                                                                                                                                                    Setup URL (optional)
                                                                                                                                                                    Users will be redirected to this URL after installing your GitHub App to complete additional setup.

                                                                                                                                                                     Redirect on update
                                                                                                                                                                     Redirect users to the 'Setup URL' after installations are updated (E.g. repositories added/removed).

                                                                                                                                                                     Webhook

                                                                                                                                                                     Active
                                                                                                                                                                     We will deliver event details when this hook is triggered.
                                                                                                                                                                     Webhook URL
                                                                                                                                                                     Events will POST to this URL with a webhook.

                                                                                                                                                                     Secret
                                                                                                                                                                     Set a secret to secure your webhooks.


                                                                                                                                                                      Display information
                                                                                                                                                                      Drag & drop

                                                                                                                                                                      You can also drag and drop a picture from your computer.


                                                                                                                                                                      Private keys
                                                                                                                                                                      Generate a private key
                                                                                                                                                                      You need a private key to sign access token requests.

                                                                                                                                                                      Learn more about private keys.

                                                                                                                                                                      IP allow list
                                                                                                                                                                      Enter the IP addresses of your GitHub App to allow organizations with IP allow lists to selectively inherit the App's IP allow list when installed. Learn more about App IP allow lists.

                                                                                                                                                                      There are no IP addresses on the allow list yet.
                                                                                                                                                                      IP address or CIDR range
                                                                                                                                                                      Short description
                                                                                                                                                                      Check IP address
                                                                                                                                                                      Enter an IP address to check whether it is permitted by enabled entries on the IP allow list.

                                                                                                                                                                      Footer
                                                                                                                                                                      © 2026 GitHub, Inc.
                                                                                                                                                                      Footer navigation
                                                                                                                                                                      Terms
                                                                                                                                                                      Privacy
                                                                                                                                                                      Security
                                                                                                                                                                      Status
                                                                                                                                                                      Community
                                                                                                                                                                      Docs
                                                                                                                                                                      Contact
                                                                                                                                                                      Manage cookies
                                                                                                                                                                      Do not share my personal information                                                                                                                                                                                                         If your goal is for QMOI to work automatically both from GitHub-hosted Actions and from either repository's Codespace, I would set up both the Actions secret and the Codespaces secret, rather than putting the PEM directly into either repository.

                                                                                                                                                                      Skip to content
                                                                                                                                                                      Developer Settings
                                                                                                                                                                      Registration successful. You must generate a private key in order to install your GitHub App.
                                                                                                                                                                      Settings Developer settings GitHub Apps QMOI Dual Repository Agent
                                                                                                                                                                      About
                                                                                                                                                                      Owned by: @thealphakenya

                                                                                                                                                                      App ID: [redacted; store in GitHub-managed configuration]

                                                                                                                                                                      Using your App ID to get installation tokens? You can now use your Client ID instead.

                                                                                                                                                                      Client ID: [redacted; store in GitHub-managed configuration]

                                                                                                                                                                      GitHub Apps can use OAuth credentials to identify users. Learn more about identifying users by reading our integration developer documentation.

                                                                                                                                                                      Client secrets
                                                                                                                                                                      You need a client secret to authenticate as the application to the API.

                                                                                                                                                                      Basic information
                                                                                                                                                                      GitHub App name
                                                                                                                                                                      QMOI Dual Repository Agent
                                                                                                                                                                      The name of your GitHub App.

                                                                                                                                                                      Write
                                                                                                                                                                      Preview
                                                                                                                                                                      Autonomous development, repository management, CI/CD, workflow orchestration, monitoring, cross-repository synchronization, and automation for QMOI projects.
                                                                                                                                                                      Homepage URL
                                                                                                                                                                      https://github.com/thealphakenya
                                                                                                                                                                      The full URL to your GitHub App’s website.

                                                                                                                                                                      Identifying and authorizing users
                                                                                                                                                                      The URIs to redirect to after a user authorizes your application. You may add up to 10 redirect URIs. Wildcard matching allows tokens to be sent to all subdomains and additional paths of the redirect URI. Only enable this if you are sure you have control over all possible matches. Learn more about secure use of redirect URIs.
                                                                                                                                                                      Redirect URI
                                                                                                                                                                      e.g. https://example.com/auth
                                                                                                                                                                       Allow wildcard matching
                                                                                                                                                                        Request user authorization (OAuth) during installation
                                                                                                                                                                        Requests that the installing user grants access to their identity during installation of your App.

                                                                                                                                                                         Enable Device Flow
                                                                                                                                                                         Allow this GitHub App to authorize users via the device flow.

                                                                                                                                                                         Post installation
                                                                                                                                                                         Setup URL (optional)
                                                                                                                                                                         Users will be redirected to this URL after installing your GitHub App to complete additional setup.

                                                                                                                                                                          Redirect on update
                                                                                                                                                                          Redirect users to the 'Setup URL' after installations are updated (E.g. repositories added/removed).

                                                                                                                                                                          Webhook

                                                                                                                                                                          Active
                                                                                                                                                                          We will deliver event details when this hook is triggered.
                                                                                                                                                                          Webhook URL
                                                                                                                                                                          Events will POST to this URL with a webhook.

                                                                                                                                                                          Secret
                                                                                                                                                                          Set a secret to secure your webhooks.


                                                                                                                                                                           Display information
                                                                                                                                                                           Drag & drop

                                                                                                                                                                           You can also drag and drop a picture from your computer.


                                                                                                                                                                           Private keys
                                                                                                                                                                           Generate a private key
                                                                                                                                                                           You need a private key to sign access token requests.

                                                                                                                                                                           Learn more about private keys.

                                                                                                                                                                           IP allow list
                                                                                                                                                                           Enter the IP addresses of your GitHub App to allow organizations with IP allow lists to selectively inherit the App's IP allow list when installed. Learn more about App IP allow lists.

                                                                                                                                                                           There are no IP addresses on the allow list yet.
                                                                                                                                                                           IP address or CIDR range
                                                                                                                                                                           Short description
                                                                                                                                                                           Check IP address
                                                                                                                                                                           Enter an IP address to check whether it is permitted by enabled entries on the IP allow list.

                                                                                                                                                                           Footer
                                                                                                                                                                           © 2026 GitHub, Inc.
                                                                                                                                                                           Footer navigation
                                                                                                                                                                           Terms
                                                                                                                                                                           Privacy
                                                                                                                                                                           Security
                                                                                                                                                                           Status
                                                                                                                                                                           Community
                                                                                                                                                                           Docs
                                                                                                                                                                           Contact
                                                                                                                                                                           Manage cookies
                                                                                                                                                                           Do not share my personal information

                                                                                                                                                                          Retired private-key fingerprint omitted because the key is exposed in remote history.

## Current 2026-10-06 App installation checkpoint — 2026-10-06T02:04:20.680597Z

- Installation record: QMOI Dual Repository Agent is reported as installed on both `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`. This is a user-reported installation record and does not by itself prove that the current Codespace can authenticate as the App.
- At this checkpoint the local App credential directory and files were absent. This historical observation is superseded by the later 2026-10-06 name-only environment check, which found the three QMOI App variable names present but did not validate their values.
- Current GitHub CLI state: `gh auth status` reports the active token as invalid. `gh api user` returned HTTP 401 `Bad credentials`, so no valid GitHub identity or repository access was proven from the current token.
- The two selected repositories therefore remain separate authorization domains. An installation on both repositories does not grant the current Codespace App identity without a verified private key, App ID, installation ID, and short-lived installation token.
- App authentication proof required before any mutation: a target-owned workflow or authorized external runner must mint a short-lived installation token, then successfully call GitHub identity, installation, repository, Actions, branch-protection, and ruleset endpoints for both repositories.
- Safe operation rule: never place the private key in the Codespace, terminal history, Markdown, JSON, or environment command strings. Use a GitHub Actions secret or an authorized secret manager, scope token lifetime to the minimum, and never log or persist the token.
- Current result: `APP_AUTHENTICATION_BLOCKED`; installation documentation is retained, but current effective App identity and permission are not verified. No dispatch, merge, release, or deployment was attempted.

## GitHub App setup and credential inventory — 2026-10-06

### Installation and feature scope

- The owner reports that `QMOI Dual Repository Agent` is installed for both `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`. This records the installation claim only; this Codespace could not verify the installation through GitHub because its available CLI token returned HTTP 401.
- The intended App feature set is read-only repository/workflow/check observation and, only when separately authorized by repository policy, target-owned workflow dispatch, pull-request orchestration, and cross-repository coordination. Installation scope does not itself authorize protected-branch changes, bypass review, merge, release, or deployment.
- Before enabling a feature, verify the App's minimum required repository permissions and event subscriptions in GitHub App settings, verify both repositories are selected in the installation, and independently verify each repository's rulesets and workflow permissions. Do not grant broad permissions merely because a feature is listed here.

### Permission snapshot supplied by the owner

`githubapppermissions.md` contains a user-provided settings-page snapshot. The following is recorded as **reported configuration**, not as live API-verified effective permissions:

- Read access: Codespaces metadata and repository metadata.
- Read/write access: Dependabot alerts; license-compliance alerts; Actions and Actions variables; administration; agent secrets, tasks, and variables; artifact metadata; attestations API; checks; code; code quality; Codespaces and Codespaces lifecycle administration; commit statuses; Copilot agent settings; repository custom properties; Dependabot secrets; deployments; discussions; environments; issues; merge queues; packages; Pages; pull requests; repository advisories, hooks, and projects; secret-scanning alert dismissal requests and alerts; secret-scanning push-protection bypass requests; repository secrets; security events; and workflows.
- Reported installation scope: two selected repositories, `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`.

This is a broad, high-impact permission set. Administration, repository secrets, agent/Codespaces secrets, workflow writes, alert dismissal, and push-protection bypass-request permissions must not be used merely because they are available. Review the live App configuration and remove every permission not required by an approved workflow; prefer read-only access for inventory and authentication preflight. A permission grant is not authorization to bypass review or a repository ruleset.

### Recommended Actions setup

1. Rotate the historically exposed App private key in GitHub App settings. Do not use the former key or any local copy until the App owner confirms the old key is revoked and the replacement is installed.
2. For GitHub Actions, configure the App Client ID as `APP_CLIENT_ID` (Actions variable) or `QMOI_GITHUB_CLIENT_ID` (Actions secret), and the replacement PEM as `APP_PRIVATE_KEY` or `QMOI_GITHUB_PRIVATE_KEY` (Actions secret). The optional `QMOI_GITHUB_APP_ID` secret is also accepted. Use the repository's **Settings -> Secrets and variables -> Actions** page. Codespaces secrets do not flow into Actions. Never place the PEM in this repository, a Codespace file, a command argument, logs, workflow artifacts, or documentation.
3. The local target-owned `cross-repo-auth-preflight.yml` workflow supports those names through `actions/create-github-app-token@v3`, pins the owner and both repository names, and requests read-only Actions, checks, contents, pull-request, and status scopes. It is uncommitted and has not run remotely. Keep the generated installation token in memory for that job and do not persist or print it.
4. For interactive Codespaces use, configure separate Codespaces secrets restricted to the two repositories; Actions secrets are not automatically available to Codespaces and Codespaces secrets are not available to Actions. Prefer the target-owned workflow path so the private key does not enter the Codespace.
5. Validate identity and installation access with read-only API calls for both repositories before enabling any operation. Then verify Actions, checks, branch protection, and rulesets. A valid identity is not mutation authority.

### Other GitHub Actions credentials

The following are **workflow references found in available source**, not a verified list of configured GitHub secrets. Secret values were not requested. Alpha-Q-ai's current local workflow files reference `MY_CUSTOM_TOKEN`, legacy typo `MY_CUSTUOM_TOKEN`, GitHub-provided `GITHUB_TOKEN`, the Actions variable `APP_CLIENT_ID`, and the Actions secrets `APP_PRIVATE_KEY`, `QMOI_GITHUB_CLIENT_ID`, `QMOI_GITHUB_APP_ID`, and `QMOI_GITHUB_PRIVATE_KEY` in `.github/workflows/cross-repo-auth-preflight.yml`. That local workflow change adds an optional read-only App-token preflight and retains the existing token fallbacks; it has not been dispatched or remotely verified. The separate repository secret inventory could not be read: `gh secret list` returned HTTP 401 for both repositories.

The available `qmoi-enhanced-history-14` workflow snapshot references additional secret names in these categories:

- GitHub and publishing: `GH_PAT`, `GH_TOKEN`, `MY_CUSTOM_TOKEN`, `GITHUB_TOKEN`, `PYPI_API_TOKEN`.
- Build and deployment: `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEYSTORE_ALIAS`, `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `STAGING_HOST`, `STAGING_USER`, `PROD_HOST`, `PROD_USER`, `DEPLOY_HOST`, `DEPLOY_PORT`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`, `VERCEL_TOKEN`, `QCITY_DEPLOY_WEBHOOK`.
- QMOI integrations and sync: `QMOI_EMAIL_USER`, `QMOI_EMAIL_PASS`, `QMOI_EMAIL_RECIPIENT`, `QMOI_SLACK_WEBHOOK`, `QMOI_TWILIO_SID`, `QMOI_TWILIO_TOKEN`, `QMOI_TWILIO_WHATSAPP`, `QMOI_TELEGRAM_TOKEN`, `QMOI_TELEGRAM_CHAT`, `QMOI_DISCORD_WEBHOOK`, `QMOI_SYNC_BACKENDS`, `QMOI_GIST_ID`, `QMOI_GH_TOKEN`, `QMOI_HF_REPO`, `QMOI_HF_TOKEN`, `QMOI_MEMORY_URL`, `QMOI_SYNC_API_KEY`, `QVILLAGE_INTERNAL_URL`, `HF_API_TOKEN`, `SLACK_WEBHOOK_URL`.
- Security and CI: `CODECOV_TOKEN`, `SNYK_TOKEN`, `SONAR_TOKEN`.

The qmoi-enhanced names above come from a historical local snapshot, not a live qmoi-enhanced checkout or current GitHub settings. Their presence in YAML does not prove a secret exists, is current, is valid, or is needed by the active workflow. Reconcile each reference against the current workflow and least-privilege purpose before configuring it; never copy credential values between repositories by hand.

### Current authorization and exposure status

- Secret-name inventory attempts on 2026-10-06 returned HTTP 401 for `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`. Configured repository/org secret names and values are therefore unknown.
- The token previously pasted into a terminal export command is exposed in terminal/session context. Revoke or rotate it promptly through GitHub settings, then remove any saved shell-history entry using the shell's supported history controls. Do not reuse it for App authentication or remote checks.
- Current state remains `APP_AUTHENTICATION_BLOCKED` and `SECRET_INVENTORY_UNKNOWN`; the new local preflight has not run, no App token was minted, and no repository mutation was attempted.

## Codespace App variable availability — 2026-10-06T22:00:04Z

- Name-only environment checks found `QMOI_GITHUB_APP_ID`, `QMOI_GITHUB_CLIENT_ID`, and `QMOI_GITHUB_PRIVATE_KEY` present in the current Codespace process. Their values were not printed, copied, or tested cryptographically.
- `QMOI_GITHUB_INSTALLATION_ID` is absent from the current process and has not been independently discovered. Do not invent or copy an installation ID from a different App or repository. `actions/create-github-app-token@v3` can discover the installation from the owner and explicit repository list, so this ID is not required by the target-owned preflight workflow.
- Presence of a Codespaces secret does not make it available to GitHub Actions. The local optional workflow path separately requires its Actions variable/secret configuration; that configuration and its run are unverified.
- The historical private key is still documented as compromised and rotation is not confirmed. The available environment value must not be used to mint a JWT or call App APIs until the owner confirms that the old key was revoked and this is the replacement.
- GitHub CLI authentication remains invalid (`GH_TOKEN`, HTTP 401). No App JWT, installation token, or authenticated App identity was proven.
- Result: `APP_CREDENTIALS_PRESENT_ROTATION_UNVERIFIED_INSTALLATION_ID_ABSENT_AUTH_BLOCKED`.

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
