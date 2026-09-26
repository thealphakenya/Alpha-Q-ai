# QMOI Dual Repository Agent

## Current App authentication status (2026-09-26T01:20:00Z)

- Correlation ID: `2026-09-26-github-app-authorization-gate`.
- Historical PEM recovery: the uploaded GitHub App key was located in the reachable Git history as `qmoi-dual-repository-agent.2026-09-24.private-key (1).pem` and restored to the protected App key path at `$HOME/.config/alpha-q-ai/github-app/private-key.pem`.
- Verified metadata: `$HOME/.config/alpha-q-ai/github-app/credentials.env` is present with mode `600` and contains the App identifiers (`APP_ID`, `CLIENT_ID`) and the configured private-key path.
- Verified state: the restored PEM is present at the protected key path, the file has mode `600`, and a direct GitHub App JWT verification against the `/app` endpoint returned HTTP 200.
- Result: the current workspace now has a valid installed PEM for the GitHub App identity check, and the App identity is confirmed as `QMOI Dual Repository Agent` under owner `thealphakenya`.
- Remaining gate: complete the installation-based repository authorization checks and then continue only with read-only or target-authorized workflow validation before any remote mutation or dispatch.

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