# SYNC.md - Repository Synchronization Guide

## Overview
This document details the synchronization mechanisms between the **qmoi-enhanced** repository and the **Alpha-Q-ai** repository. Both repositories are designed to work in full autonomy while maintaining bidirectional synchronization of critical files, features, and configurations.

## Repository Information

### qmoi-enhanced
- **Owner**: thealphakenya
- **URL**: https://github.com/thealphakenya/qmoi-enhanced
- **Required Protected Branches**: main, autosync-backup
- **Other Branches**: inventoried from live remote refs on every sync audit; do not assume the required branches are the complete branch set
- **Purpose**: QMOI AI applications UI, core features, and user-facing components
- **Contains**: Applications (qmoiaiui, qmoi-space, qcity, qalpha), styles, UI features

### Alpha-Q-ai
- **Owner**: thealphakenya
- **URL**: https://github.com/thealphakenya/Alpha-Q-ai
- **Required Protected Branches**: main, autosync-backup
- **Other Branches**: inventoried from live remote refs on every sync audit; do not assume the required branches are the complete branch set
- **Purpose**: Backend infrastructure, APIs, core algorithms, and cross-cutting concerns
- **Contains**: API implementations, endpoints, routes, backend services

## Synchronization Strategy

The remote historical branch `codespace-potential-space-happiness-wrv69x5j6qjq2g7wp`
is an auditable source snapshot. Before importing anything, automation must
enumerate its reachable files and commits, compare checksums against both
repositories, classify each path as QE-only, AQ-only, shared, or obsolete, and
create a reviewable sync PR. It must never overwrite current `main` implicitly.
Missing files are included through the PR when classification and validation
agree; conflicts remain blocked for review.

### Bidirectional Sync Model
Both repositories maintain:
1. **Main Branch**: Production-ready code with validated features
2. **Autosync-Backup Branch**: Automated backup and staging branch

### All-Branch Inventory and Naming Policy

Every audit fetches all remote branch refs from both repositories and reports
each branch name, tip commit SHA, tree SHA, recognized role, naming status,
same-name counterpart, and merge eligibility in the
`branch_alignment.branches` report array. That generated report is the current
complete roster for the audited refs; the short stable summary here must not be
treated as an exhaustive or permanent list. Record the report's repository,
ref, capture time, SHA, target Actions run ID, head SHA, and exact branch refs
when publishing it as a workflow artifact. Missing,
unfetched, permission-denied, or stale refs are coverage gaps, never an empty
branch set.

#### Observed branch-name snapshot — 2026-10-02T02:05:57Z

This is a human-readable snapshot of the live `refs/heads` names observed at
the timestamp above. The generated sync report is authoritative for exact tip
SHAs and later changes. These names are inventoried; they are not all merge or
publication targets.

<details>
<summary>Alpha-Q-ai — 25 observed branches</summary>

| Branch | Role |
| --- | --- |
| `autosync-backup` | protected_backup |
| `chore/security-autofix` | chore |
| `codespace-ominous-space-spork-wrqg5956x445hggv7` | ephemeral_codespace |
| `codespace-super-umbrella-wrq596r754wwfvgwg` | ephemeral_codespace |
| `dependabot/github_actions/actions/checkout-7` | dependency_update |
| `dependabot/github_actions/actions/download-artifact-8` | dependency_update |
| `dependabot/github_actions/actions/github-script-9` | dependency_update |
| `dependabot/github_actions/actions/setup-python-7` | dependency_update |
| `dependabot/github_actions/actions/upload-artifact-7` | dependency_update |
| `dependabot/github_actions/peter-evans/create-pull-request-8` | dependency_update |
| `dependabot/npm_and_yarn/Alpha-Q-ai-2025/npm_and_yarn-c3809050de` | dependency_update |
| `dependabot/npm_and_yarn/qmoi-enhanced-history-14/npm_and_yarn-36f0a19845` | dependency_update |
| `dependabot/pip/boto3-gte-1.43.101` | dependency_update |
| `dependabot/pip/coverage-gte-7.16.1` | dependency_update |
| `dependabot/pip/fido2-gte-2.2.1` | dependency_update |
| `dependabot/pip/flake8-gte-7.4.1` | dependency_update |
| `dependabot/pip/flask-cors-gte-6.0.5` | dependency_update |
| `dependabot/pip/gitpython-gte-3.1.62` | dependency_update |
| `dependabot/pip/pyjwt-gte-2.15.0` | dependency_update |
| `dependabot/pip/pytest-cov-gte-7.1.0` | dependency_update |
| `dependabot/pip/requests-gte-2.34.2` | dependency_update |
| `fix-dependabot-ws` | legacy_or_unclassified |
| `main` | production |
| `resolved-dependabot-ws` | legacy_or_unclassified |
| `security/dependency-remediation-20261002` | security |

</details>

<details>
<summary>qmoi-enhanced — 151 observed branches</summary>

| Branch | Role |
| --- | --- |
| `auto-merge/imported-theofalphakenya-20251122T090610Z` | legacy_or_unclassified |
| `auto-merge/imported-theofalphakenya-20251122T090632Z` | legacy_or_unclassified |
| `auto-merge/imported-theofalphakenya-20251122T092741Z` | legacy_or_unclassified |
| `auto/dns-fixes-proposals-20251120122343` | legacy_or_unclassified |
| `auto/http-to-https-20251110` | legacy_or_unclassified |
| `auto/placeholder-proposals-20251120-01` | legacy_or_unclassified |
| `auto/placeholder-stubs` | legacy_or_unclassified |
| `auto/placeholder-stubs-clean` | legacy_or_unclassified |
| `auto/placeholders-fixes` | legacy_or_unclassified |
| `auto/placeholders-fixes-backup-20251028002407` | legacy_or_unclassified |
| `auto/placeholders/auto-apply-dryrun` | legacy_or_unclassified |
| `auto/placeholders/auto-apply-final` | legacy_or_unclassified |
| `auto/placeholders/code-fix-docs_link-validation-report.json` | legacy_or_unclassified |
| `auto/placeholders/code-fix-qmoi-enhanced_components` | legacy_or_unclassified |
| `auto/placeholders/code-fix-qmoi-enhanced_scripts` | legacy_or_unclassified |
| `auto/placeholders/code-fix-qmoi-enhanced_src` | legacy_or_unclassified |
| `auto/placeholders/code-fix-reports_placeholders.json` | legacy_or_unclassified |
| `auto/placeholders/code-fix-reports_suggestions.json` | legacy_or_unclassified |
| `auto/placeholders/code-fix-src_components` | legacy_or_unclassified |
| `auto/placeholders/docs-fix-3` | legacy_or_unclassified |
| `auto/placeholders/p0-epic` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-50b8f7d4acdba845f989c2f8552ba482453936ac` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-6f861e97978f7658419a96db195621a1370c35b2` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-730e13874a1c207ea2a3a2ca71d1a929ea46dd6a` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-74ddf5a1585e1c97907f5e3b70c046a8f629ad2e` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-7a60e32686716c20c7de7384b2470585a2be6067` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-8a71717e5525d8ca42c511e6bc97d14b3aed1e70` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-950017e1ca3e2c4421bfebba5eebc7585d7f9a98` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-ac68e484dc37c4b6600eb8ef553888b664c04a86` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-d21bd6a5f3e1c05f2cd6589732542942d8c16d29` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_1` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_10` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_11` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_12` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_13` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_14` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_15` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_2` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_3` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_4` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_5` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_6` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_7` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_8` | legacy_or_unclassified |
| `auto/placeholders/pr-patch-pass_fixes_batch_9` | legacy_or_unclassified |
| `auto/redact-credentials-20251113` | legacy_or_unclassified |
| `auto/release-inventory-20251113160839` | legacy_or_unclassified |
| `auto/update-mds-1762860999` | legacy_or_unclassified |
| `auto/vercel-fix-1762862377` | legacy_or_unclassified |
| `auto/vercel-fix-1762885773` | legacy_or_unclassified |
| `auto/vercel-fixes` | legacy_or_unclassified |
| `automated/requests-security-fix` | legacy_or_unclassified |
| `automation/continue-setup` | legacy_or_unclassified |
| `autosync-artifacts-20251107` | legacy_or_unclassified |
| `autosync-backup` | protected_backup |
| `autosync-backup-20250926-232440` | legacy_or_unclassified |
| `autosync-backup-20250927-004803` | legacy_or_unclassified |
| `autosync-backup-20250927-005413` | legacy_or_unclassified |
| `autosync-backup-20250927-010622` | legacy_or_unclassified |
| `autosync-backup-20250927-013228` | legacy_or_unclassified |
| `autosync-backup-20250928-202506` | legacy_or_unclassified |
| `autosync-backup-20250929-044647` | legacy_or_unclassified |
| `autosync-backup-20250929-051243` | legacy_or_unclassified |
| `autosync-backup-20250929-052822` | legacy_or_unclassified |
| `autosync-backup-20250929-055200` | legacy_or_unclassified |
| `autosync-largefiles-20250927-004803` | legacy_or_unclassified |
| `autosync-largefiles-20250927-005413` | legacy_or_unclassified |
| `autosync-largefiles-20250927-010622` | legacy_or_unclassified |
| `autosync-largefiles-20250927-013228` | legacy_or_unclassified |
| `autosync-largefiles-20250928-202506` | legacy_or_unclassified |
| `autosync-largefiles-20250929-044647` | legacy_or_unclassified |
| `autosync-largefiles-20250929-051243` | legacy_or_unclassified |
| `autosync-largefiles-20250929-052822` | legacy_or_unclassified |
| `autosync-largefiles-20250929-055200` | legacy_or_unclassified |
| `autosync-links-20251107` | legacy_or_unclassified |
| `autosync-md-fixes-20251107` | legacy_or_unclassified |
| `autosync-placeholder-fix-20251125073732` | legacy_or_unclassified |
| `autosync-resolved-1700261406` | legacy_or_unclassified |
| `autosync/enhancements` | legacy_or_unclassified |
| `autosync/env-manager-ci-fixes-20251027` | legacy_or_unclassified |
| `autosync/verification-20251107-clean` | legacy_or_unclassified |
| `autosync/verification-20251107-pr` | legacy_or_unclassified |
| `autoupdate/alllinks-25781049099` | legacy_or_unclassified |
| `autoupdate/alllinks-28078916358` | legacy_or_unclassified |
| `backup/before-auto-merge-20251122T092741Z` | legacy_or_unclassified |
| `backup/before-replacer-${TS}` | legacy_or_unclassified |
| `chore/cleanup-tests-and-lint` | chore |
| `chore/copilot-setup-smoke-20251122T103756Z` | legacy_or_unclassified |
| `chore/copilot-setup-smoke-20251122T103820Z` | legacy_or_unclassified |
| `chore/local-chat-integration-20251122T104109Z` | legacy_or_unclassified |
| `chore/local-chat-integration-20251122T104216Z` | legacy_or_unclassified |
| `chore/prepare-production-20251123T140000Z` | legacy_or_unclassified |
| `chore/update-master-docs-20251122T135155Z` | legacy_or_unclassified |
| `ci-debug-output-manual-1766306758` | legacy_or_unclassified |
| `ci/docker-run-tests` | legacy_or_unclassified |
| `codespace-didactic-halibut-pj95gjxxr5v736w64` | ephemeral_codespace |
| `codespace-potential-space-happiness-wrv69x5j6qjq2g7wp` | ephemeral_codespace |
| `codespace-potential-tribble-g46v54ggq6rv2w4v5` | ephemeral_codespace |
| `codespace-special-guacamole-4jpvwg9rj4x4f5xx5` | ephemeral_codespace |
| `codespace-super-enigma-wrqx6xg9ggvg356v4` | ephemeral_codespace |
| `codespace-ubiquitous-space-waddle-r7r7rjjp7rvhpq77` | ephemeral_codespace |
| `codespace-zany-capybara-x5xg95jjw7x5hgwg` | ephemeral_codespace |
| `copilot/hosted-step-manager` | legacy_or_unclassified |
| `dependabot/github_actions/actions/checkout-7` | dependency_update |
| `dependabot/github_actions/actions/download-artifact-8` | dependency_update |
| `dependabot/github_actions/actions/github-script-9` | dependency_update |
| `dependabot/github_actions/actions/setup-python-7` | dependency_update |
| `dependabot/github_actions/actions/upload-artifact-7` | dependency_update |
| `dependabot/github_actions/peter-evans/create-pull-request-8` | dependency_update |
| `dependabot/npm_and_yarn/qmoi-enhanced-history-14/npm_and_yarn-9239f84e19` | dependency_update |
| `dependabot/pip/bandit-gte-1.9.4` | dependency_update |
| `dependabot/pip/coverage-gte-7.16.1` | dependency_update |
| `dependabot/pip/msgpack-gte-1.2.2` | dependency_update |
| `dependabot/pip/mypy-gte-2.3.1` | dependency_update |
| `dependabot/pip/pyjwt-gte-2.14.0` | dependency_update |
| `dependabot/pip/pylint-gte-4.0.8` | dependency_update |
| `dependabot/pip/python-dotenv-gte-1.2.3` | dependency_update |
| `dependabot/pip/requests-gte-2.34.2` | dependency_update |
| `dependabot/pip/stripe-gte-15.6.1` | dependency_update |
| `dependabot/pip/werkzeug-gte-3.1.8` | dependency_update |
| `enhancement/readme-pr-demo` | legacy_or_unclassified |
| `feat/mpesa-adapter-wireup` | legacy_or_unclassified |
| `feature/auth-prod-1780061287` | feature |
| `feature/ci-verify-and-release` | feature |
| `feature/session4-complete` | feature |
| `fix/harden-ollama-agent` | fix |
| `fix/placeholders-automated-20251122T092214Z` | legacy_or_unclassified |
| `fix/placeholders-prod-review-20251220-clean` | fix |
| `fix/security-redactions-20251027` | fix |
| `gh-pages` | legacy_or_unclassified |
| `imported-snapshot/theofalphakenya-20251122T085133Z` | legacy_or_unclassified |
| `imported/theofalphakenya/HEAD` | legacy_or_unclassified |
| `imported/theofalphakenya/main` | legacy_or_unclassified |
| `integration/all-repositories-20260919` | legacy_or_unclassified |
| `link-update/pr-clean` | legacy_or_unclassified |
| `main` | production |
| `mark-unverified-20251113` | legacy_or_unclassified |
| `merge/complete-copy-gate-qe-20260919` | legacy_or_unclassified |
| `merge/materialized-inputs-clean-20260919` | legacy_or_unclassified |
| `ollama/iteration-11` | legacy_or_unclassified |
| `ollama/iteration-8` | legacy_or_unclassified |
| `ollama/iteration-9` | legacy_or_unclassified |
| `prod-enablement-20251113090017` | legacy_or_unclassified |
| `prod/cleanup-20260516` | legacy_or_unclassified |
| `qe/complete-autonomous-audit-20260920` | legacy_or_unclassified |
| `revert-88-autosync-artifacts-20251107` | legacy_or_unclassified |
| `review/imported-theofalphakenya-main` | legacy_or_unclassified |
| `save/current-work-20251122T093850Z` | legacy_or_unclassified |
| `sync-notify` | legacy_or_unclassified |
| `todo-prod-sweep-20251221` | legacy_or_unclassified |
| `upgrade/next-15` | legacy_or_unclassified |

</details>

The only protected shared lifecycle branches are `main` and
`autosync-backup`. New human work branches use lowercase names in the form
`<type>/<issue-id>-<kebab-slug>`, for example `feature/123-add-search` or
`security/456-fix-token-validation`. Allowed types are `feature`, `fix`,
`hotfix`, `security`, `chore`, `docs`, and `experiment`. Release branches use
`release/v<major>.<minor>.<patch>[-<label>]`. Dependabot and Codespaces names
are provider-managed exceptions; the agent inventories but does not rename
them. Unknown legacy names remain visible as `legacy_review` and are never
silently deleted or synchronized.

Branch creation is tied to a reviewed issue, release plan, or provider
automation. The agent must not invent branches just to increase branch count.
It records the purpose, owning repository, base SHA, expected checks, creator,
and cleanup/retention rule before proposing a new branch. Existing branch names
are never reused for unrelated work.

Feature, fix, security, docs, experiment, release, Dependabot, Codespaces, and
unclassified branches are inventory and merge-planning inputs, not automatic
cross-repository promotion targets. They remain in their owning repository
unless an explicit review PR requests a same-name counterpart or a change into
`main`. Required checks and human review apply before merge. Codespaces branches
are never cross-repository synchronized. Unknown/conflicting branches stop for
review. Branch inventory inclusion means every branch is considered by merge
planning; it does not mean every branch is blindly merged or copied.

### Autonomous update and publication contract
The Ollama autonomous agent may update both repositories only after the local validation, merge inventory, and lifecycle gates pass. The authorized sequence is:

1. validate the local repo and merge inventory
2. publish or validate the backup branch (`autosync-backup`) for both repos
3. verify exact SHA and fast-forward safety on both repos
4. create the Q.0.0.1 directory and companion manifest on the final branch state
5. promote main only after backup publication and final workflow proof agree
6. record exact final SHAs and remote workflow evidence in the ledger and the branch status files

This contract applies to Alpha-Q-ai, qmoi-enhanced, and any additional repository following the same cross-repo autosync pattern. No force-push or history rewrite is allowed. If branch protection or target-owned workflow evidence is missing, the automation stops and marks the state as blocked rather than claiming success.

### Per-branch completion gate
Each branch is considered successful only after the branch-specific publication evidence is valid:

- `main` branch: validated production branch and exact SHA proof
- `autosync-backup` branch: backup publication and audit pass before main promotion
- Q-version artifact: `Q.0.0.1` directory and companion document added only after the final successful branch state is proven

For all other branches, completion means inventory coverage plus an explicit
branch disposition (`review_pr_required`, `provider_managed`, `ephemeral`, or
`legacy_review`). Automatic branch publication is disabled unless the branch
is one of the protected lifecycle branches and its exact-SHA, fast-forward,
backup-first, and required-check gates all pass. An absent counterpart is
reported as `only_in_<repository>` and is not created automatically.

All branches and final artifacts must remain consistent with the same evidence ledger. The branch sync remains operationally complete only when both repos and both branches are in a verified state, not merely when a local script reports success.

### Master File Sync
The following critical files are synced bidirectionally:

#### API & Endpoints
- **API.md**: All APIs from both repositories
- **ENDPOINTS.md**: All endpoints from both repositories
- **ROUTES.md**: All routes from both repositories
- **MODELEVOLUTIONO.md**: The model evolution and countdown tracking file used by both repos

#### Architecture & Structure
- **ALLMDFILESREFS.md**: Reference of all .md files in both repos
- **TREE_FULL_STRUCTURE.md**: Complete directory structure
- **ALLPLATFORMSDEVICE.md**: Cross-platform device support

#### Features & Specifications
- **STYLES.md**: Unified UI styles with user-specific customization
- **UNIVERSALS.md**: Features available across all platforms
- **ALLAUTO.md**: All automation features
- **AUTODEV.md**: Auto-development capabilities

#### Applications
- **QMOIAI.md**: QMOI AI app specifications
- **QCITY.md**: File manager specifications
- **QMOI-SPACE.md**: Media player specifications
- **QALPHA.md**: IDE specifications

#### Accountability & Governance
- **ACCOUNTABILITY.md**: Master accountability tracking
- **QMOI_MODEL_CARD.md**: Model information card
- **QMOI_REALTIME_MEMORY_INDEX.md**: Real-time memory index

## Synchronization Workflows

### GitHub Actions Workflows in Both Repos
1. **branch-sync.yml**: Keeps main and autosync-backup branches in sync
2. **auto-merge-automated-pr.yml**: Automatically merges validated PRs
3. **ollama-autonomous-agent.yml**: Runs agent for autonomous validation
4. **ollama-pr-validation.yml**: Validates PRs against specifications

### Automatic Sync Triggers
- **On Push to Main**: Auto-sync critical files to sister repo
- **On PR Merge**: Validate and sync features between repos
- **Scheduled Daily**: Full sync check and reconciliation
- **On File Update**: Real-time sync for critical documentation files

### Bidirectional Autosync Workflow

Both repositories include `.github/workflows/cross-repo-autosync.yml`. It runs
on pushes to `main`, every 15 minutes, and manual dispatch. The workflow checks
out the current repository and its counterpart, runs
`scripts/cross_repo_sync.py`, publishes `autosync-backup` first, and promotes
to `main` only when the target tip is a verified fast-forward. QMOI remains the
policy master, but a push from Alpha-Q-ai selects the reverse direction so
either repository can initiate a synchronization attempt.

The workflow never force-pushes. Diverged or unrelated histories stop with a
reviewable failure and an uploaded JSON audit report. This is intentional:
automatic synchronization must not erase work from either repository. The
existing `branch-sync.yml` legacy force-mirroring job is disabled; the guarded
workflow is the only automatic branch synchronizer.

Fast-forward eligibility also requires the source commit object to exist in
the target checkout; equal-looking SHA strings or source-repository ancestry
alone are insufficient. Before `--promote` applies anything, the sync tool
preflights both `autosync-backup` and `main`. Missing objects or refs produce a
blocked JSON report and no push attempt. A remote push failure is recorded with
completed and failed branch names so partial publication is never reported as
full synchronization.

The workflow uses `MY_CUSTOM_TOKEN` for write access to both repositories. That
secret must already exist in each repository's Actions settings; no code-only
change can grant GitHub write permission. Local Codespaces can use the same
runner in either checkout:

```bash
python scripts/cross_repo_sync.py \
	--qmoi /path/to/qmoi-enhanced \
	--alpha /path/to/Alpha-Q-ai \
	--direction audit \
	--report /tmp/cross-repo-sync-report.json
```

Use `qmoi-to-alpha` or `alpha-to-qmoi` with `--apply --promote` only after the
audit reports `fast_forward_possible: true`. A false value requires a reviewed
merge or rebase before promotion.

All sync jobs use a single-writer rule per repository, `autosync-backup` as the
first publication target, `[sync]` commit markers, and `[skip ci]` only for the
resulting synchronization commit. This prevents push-trigger recursion and
competing Ollama servers. The agent records branch, file inventory, checksums,
authors, timestamps, and conflict decisions in `MERGE.md` and
`ollamatracks/SYNC_STATUS.txt`.

## File Distribution Strategy

### Files in qmoi-enhanced Only
- Application UI implementations (React, TypeScript, etc.)
- User interface styles and themes
- Desktop/Mobile app packages
- Client-side libraries
- User documentation

### Files in Alpha-Q-ai Only
- Backend API implementations
- Database schemas and migrations
- Server-side algorithms
- Microservices configurations
- Cloud infrastructure as code

### Files in BOTH Repositories
- API specifications (API.md, ENDPOINTS.md, ROUTES.md)
- Cross-cutting concerns
- Shared protocols and interfaces
- Model cards and specifications
- Accountability and governance documents

## Sync Process Flow

### Step 1: Change Detection
Agent detects changes in either repository:
- File modifications
- New files
- Deleted files
- Configuration changes
- All remote branches, including branches not changed in the current push

### Step 2: Classification
Agent classifies changes:
- **Repo-Specific**: Stays in source repo
- **Shared**: Needs replication to other repo
- **Critical**: Requires immediate sync
- **Scheduled**: Queued for next sync cycle
- **Branch-Only**: Preserved in its owning repo and routed through a review PR unless it is a protected lifecycle branch

### Step 3: Validation
Before sync:
- Syntax validation
- Conflict detection
- Integrity checks
- Security scanning

### Step 4: Merge
Apply changes to target repository:
- Create a reviewable sync branch or PR for non-protected branch changes
- Update `autosync-backup` before any permitted `main` promotion
- Never auto-resolve conflicts or directly merge feature/release/provider branches
- Record unresolved conflicts and the required human decision

### Step 5: Commit & Push
Finalize sync:
- Commit with "[sync]" label
- Push to autosync-backup first
- Validate in backup branch
- Merge to main on success

## Token Policy
- **Primary Token**: MY_CUSTOM_TOKEN (GitHub Personal Access Token)
- **Fallback**: GitHub token via `gh auth token`
- **Scope**: Full repo access for both repositories
- **Security**: Token never logged or exposed in output

## Conflict Resolution

### Strategy
1. **File-level conflicts**: Keep both versions, mark for manual review
2. **Merge conflicts**: Use intelligent merge considering both repo contexts
3. **Feature conflicts**: Parent feature wins, child feature marked for review
4. **API conflicts**: Version-aware merge with backward compatibility

### Manual Review
Critical conflicts flagged in:
- Pull request with detailed explanation
- Sync status file
- Agent logs

## Monitoring & Verification

### Sync Health Checks
- Verify file checksum after sync
- Validate JSON/YAML syntax
- Check markdown link validity
- Ensure no broken references

### Status Tracking
Sync status stored in:
- `/ollamatracks/SYNC_STATUS.txt`
- GitHub commit messages (with [sync] tag)
- GitHub Actions logs

## Master Awareness
QMOI Ollama Agent maintains awareness of:
- Master decisions and commands
- Sync preferences and priorities
- Special handling requirements
- Manual intervention needs

## Autonomous Merge Completion Contract

The current workspace contains `qmoi-enhanced` and the materialized historical
snapshot, but it does not contain a local `Alpha-Q-ai` checkout. The agent must
therefore treat cross-repository completion as blocked until it can authenticate
and inventory the actual Alpha-Q-ai repository. Documentation or a remote URL is
not evidence that the second repository was merged.

Before claiming a complete merge, the agent must:

1. Inventory every reachable branch, commit, tracked path, symlink, dependency
	manifest, workflow, and historical snapshot in both repositories.
2. Record path ownership as `QE`, `AQ`, `BOTH`, `HISTORICAL`, or `CONFLICT` and
	stop automatic mutation for unknown ownership or unresolved conflicts.
3. Scan active code and workflows for placeholders, TODO/FIXME/TBD markers,
	simulated success, stubbed handlers, unsafe fallback behavior, and disabled
	production paths. Each finding must be replaced by a tested implementation or
	recorded as an explicit, non-production historical exception.
4. Run dependency audits for every discovered manifest, syntax and workflow
	validation, targeted tests, full tests, and post-merge tree comparison.
5. Publish only from a reviewable sync branch after both repositories pass the
	same evidence contract. Never force-update a production branch as a shortcut.

The agent records sanitized command metadata in checkpoint evidence and
`ollamatracks/TERMINAL_COMMANDS.log`. Secrets, tokens, passwords, private keys,
and authenticated URLs are always redacted. A missing Alpha-Q-ai checkout,
inaccessible Dependabot alerts, or an upstream advisory without a fix remains a
visible blocker; it must never be reported as successful completion.

## Emergency Procedures

### If Sync Fails
1. Log detailed error to SYNC_STATUS.txt
2. Flag as critical in pull request
3. Stop automatic merges
4. Wait for manual intervention
5. Retry after manual fix

### If Files Diverge
1. Detect divergence automatically
2. Create comparison report
3. Flag in agent logs
4. Suggest merge strategy
5. Wait for confirmation

## Related Documentation
- [MERGE.md](MERGE.md) - Detailed merge procedures by file type
- [or.md](or.md) - Operations reference and progress tracking
- [zx.txt](zx.txt) - Alpha-Q-ai specific workflow setup instructions

## Notes
This document is automatically maintained and updated by QMOI Ollama Autonomous Agent.
Last Updated: 2026-09-17T00:30:00Z
