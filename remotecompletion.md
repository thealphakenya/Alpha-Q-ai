# Remote Completion Runbook — Advanced Dual-Repository Autonomous Low-Bandwidth Edition

## Purpose

This is the authoritative operational source for completing, synchronizing, validating,
monitoring and operating:

- `thealphakenya/Alpha-Q-ai`
- `thealphakenya/qmoi-enhanced`

It is designed for browser-based GitHub Codespaces, including mobile/low-bandwidth
usage, while keeping heavy computation remote and preserving independent repository
ownership, history, protection and evidence.

## Operating Objective

Maximize safe autonomous remote execution while minimizing data transferred to the
user's browser/device.

The system must:

1. keep both repositories independently healthy;
2. allow either repository's Codespace to work on both repositories when authorized;
3. allow each Codespace to update its own repository and the peer repository;
4. prefer remote Actions for heavy compute;
5. use metadata/hashes/deltas before large payloads;
6. tolerate browser/network disconnection;
7. protect human edits from autonomous mutation;
8. recover deterministic failures automatically;
9. preserve evidence and remote telemetry;
10. never claim completion without independently verified remote evidence.

## Core Architecture

```text
Phone/Browser
     |
     v
Codespace (human workspace)
     |
     +---- Alpha-Q-ai working tree
     |
     +---- qmoi-enhanced working tree
     |
     +---- lightweight controller
     |
     v
GitHub remote state
     |
     +---- target-owned Actions
     +---- PRs/rulesets/merge queues
     +---- artifacts/releases
     +---- deployments
     +---- evidence bus
     |
     v
Autonomous watchdog / completion controller
```

The Codespace is the development workstation. GitHub Actions and target-owned
workflows are the autonomous execution layer.

## Authoritative Machine Files

Maintain, as applicable:

- `remote-completion.json`
- `remote-evidence-ledger.jsonl`
- `remotecompletion.md`
- `oe2.txt`
- `ALLMDFILESREFS.md`
- `ALLVALIDATIONS.md`
- `RELEASES.md`
- `MERGE.md`

## Completion Rule

No local observation can upgrade a remote claim to VERIFIED.

Every final claim requires a remote identifier and exact SHA/hash where applicable.

## Evidence Rule

`UNKNOWN` and `STALE` are not `PASS`.

## Safety Rule

The system may automate everything it is authorized and technically able to perform,
but must isolate authorization boundaries, protected-branch requirements and genuine
human decisions instead of bypassing them.

---

## 1. Purpose

Define the authoritative operational contract for completing and continuously operating `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`. Completion is evidence-driven: local success, dispatch acceptance, authentication, or push permission never alone proves remote completion.

## 2. Scope

Cover both repositories, their active trees, requested historical projections, branches, tags, PR trees, Markdown inventories, APIs, endpoints, routes, ports, builds, tests, workflows, artifacts, releases, deployments, backups, ledgers, security state, and final remote SHA verification.

## 3. Non-Negotiable Principles

Never fabricate success, never infer remote state from local state, never force-push as an autonomous recovery mechanism, never bypass rulesets/protection, never expose credentials, and never destroy remote telemetry to make a workflow green.

## 4. Completion Definition

A repository is complete only when target-owned remote evidence proves synchronization, validation, required checks, merge/publication, backup parity, deployment where applicable, documentation/ledger freshness, and exact final remote SHA state.

## 5. Current Evidence Baseline

The baseline recorded by the existing runbook is dated 2026-09-24. Treat its recorded SHAs, permissions, divergence and 403 result as historical evidence that must be refreshed before new claims.

## 6. Target Repositories

Primary targets are `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`. Every operation must identify its source and target repository explicitly.

## 7. Identity Verification

Verify authenticated GitHub identity and repository ownership/visibility before mutation. Never infer identity from a configured Git remote alone.

## 8. Permission Verification

Independently verify contents, Actions, PR, checks/statuses, releases, packages/artifacts, deployments, rulesets and merge capabilities. `push=true` does not imply protected-branch or Actions authority.

## 9. Authorization Alternatives

Support user-owned authorized credentials, narrowly scoped GitHub App installation tokens, target-owned PR/merge-queue workflows, authorized repository dispatch, and offline signed handoff. Prefer short-lived, least-privilege authorization.

## 10. Secret Safety

Never place tokens, passwords, private keys or secret values in prompts, source, logs, artifacts, Markdown inventories, evidence ledgers or workflow output. Record only credential class and capability evidence.

## 11. 404 Diagnostic Contract

Treat 404 as ambiguous until HTTP method, host, API version, URL, owner, repository, authentication, permissions, App installation, workflow existence, trigger, ref, encoding and resource identity have been checked.

## 12. 404-A Authentication Concealment

A private or protected resource may appear as 404 when the caller cannot access it. Verify identity and repository authorization before declaring absence.

## 13. 404-B Wrong Repository

Compare requested owner/repository against authenticated identity, remote origin and authoritative API responses. Never silently normalize names.

## 14. 404-C Wrong Endpoint

Verify HTTP method, endpoint path, API host/version, URL encoding and trailing/path syntax. A malformed or unsupported request can surface as 404.

## 15. 404-D Wrong Workflow

Verify workflow file, workflow identifier, enabled state, `workflow_dispatch` or other required trigger, and target ref before classifying a dispatch failure as missing.

## 16. 404-E Wrong Ref

Verify `refs/heads/*`, `refs/tags/*`, PR refs and target branch existence remotely. Local branch names are insufficient evidence.

## 17. 404-F Cross-Repository Token Boundary

Never assume a workflow token from repository A can mutate repository B. Cross-repository mutation requires explicitly authorized access or a target-owned workflow.

## 18. 404-G Genuine Absence

Only classify a resource as genuinely absent after independent identity, authorization, endpoint, method and resource checks succeed.

## 19. HTTP Failure Matrix

Classify 400, 401, 403, 404, 409, 422, 429 and 5xx separately. Retry transient failures with bounded backoff; diagnose permanent authorization or validation failures instead of looping.

## 20. 403 Diagnostic Contract

Distinguish permission denial, rate limit, secondary rate limit, repository policy, ruleset, environment protection, token policy, App policy and organization policy. Inspect response body and relevant headers.

## 21. 429 and 5xx Recovery

Honor `Retry-After` and rate-limit reset information where provided. Use exponential backoff with jitter and bounded attempts. Do not hammer GitHub.

## 22. Repository Dispatch

Use correlation IDs and target-owned workflows for cross-repository operations. A dispatch request is an instruction, not proof that the target operation completed.

## 23. Workflow Dispatch

Verify workflow identity and ref, dispatch only when authorized, then poll the resulting run and required jobs to terminal state.

## 24. Workflow Terminality

Queued, requested, in-progress, skipped or accepted states are not completion. Completion requires the appropriate terminal conclusion and independent remote verification.

## 25. Concurrency

Use repository/operation-specific concurrency groups to prevent competing synchronization, release, deployment and merge operations. Do not cancel critical publication operations merely to reduce noise.

## 26. Watchdog

Continuously identify failed, stale, queued, waiting, cancelled or orphaned workflows and route them through diagnosis, safe remediation, validation and re-verification.

## 27. State Machine

Use states INIT, PREFLIGHT, AUTHORIZED, DISCOVERING, RECONCILING, VALIDATING, AWAITING_CHECKS, READY_TO_MERGE, MERGING, RELEASING, DEPLOYING, VERIFYING, COMPLETE, BLOCKED_AUTH, BLOCKED_RULESET, BLOCKED_VALIDATION, BLOCKED_DIVERGENCE, BLOCKED_EXTERNAL and FAILED.

## 28. Retry State

Every retry records attempt number, failure signature, previous result, new action, backoff, expected result and actual result. Repeated identical failures terminate that repair path.

## 29. Git Safety

Fetch and snapshot before reconciliation. Never autonomously use `push --force`, destructive reset, remote deletion or history rewriting to make parity appear successful.

## 30. Divergence Classification

Calculate remote-only, local-only, common and divergent commits/paths before changes. Preserve remote work and select rebase, merge, PR or deferred resolution according to repository policy.

## 31. Remote Tree Authority

The current remote tree is authoritative for remote-state claims. Git history projections are not substitutes for inspecting the current peer repository.

## 32. Cross-Repository Inventory

Inventory both repositories independently, then compare manifests by path, size, hash/object ID, last commit, category and validation status.

## 33. Bidirectional Sync Plan

For every path classify missing, identical, variant, repository-specific, generated, shared, intentionally divergent, obsolete or requiring review. Never perform blind directory mirroring.

## 34. Ownership Map

Maintain explicit ownership for shared contracts and repository-specific files. Synchronization must follow ownership and policy, not file similarity alone.

## 35. Markdown Inventory

Maintain `ALLMDFILESREFS.md` with unlimited category membership and per-file source, bytes, lines, SHA/object ID, last commit, validation and review status.

## 36. Markdown Review Closure

Every `needs-review` record must receive a terminal classification such as VALIDATED, REPAIRED, DUPLICATE, OBSOLETE, INTENTIONAL_VARIANT, REQUIRES_EXTERNAL_AUTH, REQUIRES_HUMAN_DECISION or NOT_REPRODUCIBLE with evidence.

## 37. API Contract Validation

Validate documented API names, methods, schemas, authentication requirements, request/response contracts, error behavior and implementation alignment.

## 38. Endpoint Validation

Verify every documented endpoint against routing code, tests and deployed/target configuration. Flag undocumented and documented-but-missing endpoints.

## 39. Route Validation

Compare route inventories with application registration, reverse proxy configuration and tests. Never infer route availability from documentation alone.

## 40. Port Validation

Record expected ports, actual listeners, health checks, container mappings and deployment configuration. Detect conflicts without terminating user processes automatically.

## 41. Build Validation

Run deterministic builds in remote CI where practical. Record build ID, source SHA, toolchain, result, duration and artifact hashes.

## 42. Dependency Validation

Validate lockfiles, declared floors, transitive vulnerabilities, reproducibility and compatibility. Do not weaken security constraints simply to make builds pass.

## 43. Security Validation

Run secret scanning, dependency/security checks and repository policy validation. Security failures block release/merge until resolved or explicitly classified as external blockers.

## 44. Focused Tests

Run targeted tests for changed components first to provide fast feedback and reduce compute/bandwidth cost.

## 45. Full Tests

Run full test suites remotely before final completion. Record exact source SHA, test count, failures and terminal workflow/job identifiers.

## 46. Installation Tests

For releasable artifacts, test clean installation in supported environments and record artifact hash and environment details.

## 47. Runtime Tests

Exercise startup, health, core runtime behavior and shutdown/recovery. Record source/artifact SHA and environment.

## 48. Workflow Validation

Lint/parse workflow YAML and validate referenced actions, permissions, triggers, concurrency, artifacts, environments and expected outputs.

## 49. Pull Request Lifecycle

Create/update PRs through target repositories, wait for required checks, respect review/ruleset requirements and verify merge results from remote state.

## 50. Required Checks

Associate every check with its exact head SHA. A green check from an older commit cannot prove the current commit is valid.

## 51. Ruleset Verification

Read applicable branch protection/rulesets before merge. Never bypass required reviews, checks, signed commits, queues, deployments or other configured protections.

## 52. Merge Queue

If a merge queue is active, enter through the queue and verify the resulting merge commit SHA. Do not direct-push around the queue.

## 53. Release Contract

A release requires a tag/release ID, source SHA, artifacts, artifact hashes, publication state and independent download/verification evidence.

## 54. Artifact Contract

Every artifact records name, size, SHA-256, source SHA, build ID, workflow ID, platform and validation results.

## 55. Deployment Contract

Record deployment ID, environment, source SHA, status, environment URL and workflow/run identifiers. Environment protection must be honored.

## 56. Backup Contract

Verify `autosync-backup` or other designated backups against the validated main SHA and intended parity policy. Never claim parity from a local branch.

## 57. Ledger Synchronization

Keep `RELEASES.md`, `ALLVALIDATIONS.md`, `ALLMDFILESREFS.md`, `MERGE.md`, `oe2.txt` and machine-readable ledgers synchronized with fresh remote evidence.

## 58. Evidence Levels

Use NONE, LOCAL, REMOTE_OBSERVED, REMOTE_TERMINAL and REMOTE_INDEPENDENTLY_VERIFIED. Mandatory completion claims require independent remote verification.

## 59. Evidence Event

Every mutation or material observation records event ID, correlation ID, timestamp, repository, operation, request, response, result, diagnosis, verification and evidence references.

## 60. Machine Completion Contract

Maintain `remote-completion.json` containing schema version, correlation ID, timestamps, state, repository results, authorization, synchronization, validation, checks, PRs, merges, releases, artifacts, deployments, backups, blockers and evidence.

## 61. JSONL Evidence Ledger

Maintain `remote-evidence-ledger.jsonl` as append-oriented machine-readable evidence. Do not rewrite history merely to make the latest result look clean.

## 62. Failure Signature

Normalize errors into stable signatures based on operation, HTTP class, endpoint class, repository, ref and meaningful error code/message so repeated failures can be recognized.

## 63. Safe Autonomous Repair

Repair deterministic workflow, documentation, generated-ledger, stale-ref, test and synchronization defects when authorized. Revalidate after every repair.

## 64. Authorization Boundary

When authorization is missing, isolate the blocked operation, record the exact capability required, and continue all independent read-only work.

## 65. Human Decision Boundary

Some operations may require a deliberate human decision, such as ambiguous destructive reconciliation or policy exceptions. Record the decision requirement rather than inventing one.

## 66. No False Completion

Only the final verifier may transition to COMPLETE, and only when every mandatory gate has independently verified evidence.

## 67. Correlation IDs

Every cross-repository request, workflow chain, repair, release and deployment gets a unique correlation ID carried through all child operations.

## 68. Idempotency

Operations must be safe to rerun. Before creating branches, PRs, releases or artifacts, search for an existing correlation ID or deterministic operation key.

## 69. Stale Operation Detection

Detect operations whose remote state has changed since the operation began. Re-read state before applying mutations and abandon stale plans safely.

## 70. Lease/Ownership

Long-running autonomous tasks acquire a short-lived logical lease and renew it. Expired leases are recoverable; they must not permanently block work.

## 71. Resource Budget

Define CPU, memory, disk, API-call, workflow-minute and artifact-size budgets. Prefer remote CI for heavy operations and lightweight metadata checks for routine health.

## 72. Bandwidth Budget

Treat mobile bandwidth as scarce. Default to metadata, hashes, summaries and changed paths; retrieve full logs, diffs and artifacts only on demand.

## 73. Data Minimization

Do not automatically stream large logs, download release artifacts or clone unnecessary history into the phone-facing workspace.

## 74. Caching

Cache immutable dependencies, toolchains and repository metadata where supported. Invalidate caches deterministically when lockfiles or toolchain versions change.

## 75. Generated Output Separation

Keep large generated artifacts in Actions artifacts/releases or appropriate storage rather than constantly tracking them in working trees.

## 76. Remote-First Tests

Prefer GitHub-hosted or other authorized remote compute for full tests, builds, scans and releases. The Codespace should orchestrate rather than duplicate heavy compute.

## 77. Local Fast Feedback

Run only lightweight targeted checks locally unless a local environment is specifically needed. Provide commands to escalate heavy checks to remote Actions.

## 78. User Safety

Detect uncommitted or actively edited files and suspend conflicting autonomous mutations. Never checkout, reset, rebase or overwrite a user worktree during active edits.

## 79. Locking

Use repository and operation locks for sync, release, deployment, merge and backup. Locks must have owners, timestamps, TTLs and recovery behavior.

## 80. Transaction Model

Cross-repository synchronization follows PLAN → SNAPSHOT → VALIDATE → APPLY → TEST → VERIFY. Partial application remains INCOMPLETE until reconciled.

## 81. Rollback Model

Prefer additive branches/PRs and reversible changes. Roll back only through a defined, evidence-preserving procedure; never delete evidence to hide a failed attempt.

## 82. Health Model

Expose repository health, workspace health, Actions health, cross-repo access, backup state, validation state and evidence freshness separately.

## 83. Staleness Model

Every health result has a timestamp and freshness threshold. Stale evidence is UNKNOWN, not PASS.

## 84. Monitoring

Monitor workflows, PRs, checks, releases, artifacts, deployments, branches, divergence, security findings and evidence freshness without continuously downloading large payloads.

## 85. Alerts

Alert only on actionable state changes: new blocker, failed required check, permission loss, divergence, backup mismatch, release failure, deployment failure or security regression.

## 86. Notification Deduplication

Deduplicate repeated failures by failure signature and correlation ID. Send a compact state change rather than repeated identical logs.

## 87. Recovery Queue

Maintain a durable queue of pending repairs with priority, reason, attempt count, lease, dependency and next eligible execution time.

## 88. Dead-Letter Queue

After bounded failed attempts, move unresolved operations to a dead-letter state with complete evidence and continue unrelated work.

## 89. Dependency Graph

Represent workflows, tests, artifacts, releases, deployments and ledgers as dependencies so downstream tasks cannot run from stale upstream state.

## 90. Change Impact Analysis

For each commit determine affected paths, tests, workflows, documentation, releases and deployments. Run the smallest sufficient validation first, then escalate.

## 91. Policy-as-Code

Encode synchronization, release, security, branch and evidence requirements in machine-readable policy so agents cannot reinterpret them inconsistently.

## 92. Schema Versioning

Version all machine-readable manifests, evidence events and completion contracts. Support migration rather than silently changing field meaning.

## 93. Observability

Emit structured events with timestamps, correlation IDs, repository, SHA, operation, duration, result and evidence references. Keep verbose logs remotely stored.

## 94. Remote Evidence Bus

Use workflow artifacts, job summaries, JSONL ledgers and repository files as complementary evidence channels. The final verifier must cross-check them rather than trusting one source.

## 95. Artifact Retention

Retain critical completion evidence long enough to support audit/recovery. Do not retain secrets or unnecessary sensitive data.

## 96. Release/Deployment Independence

Release and deployment controllers must remain independently restartable and must not require a user's Codespace to remain online.

## 97. Codespace Independence

The Codespace is a human development workspace, not the permanent host for autonomous production workflows.

## 98. Remote Completion Watchdog

A scheduled/triggered watchdog periodically rechecks incomplete operations, stale evidence and failed lifecycle stages and safely resumes them.

## 99. Final Verification

Read remote state again after all mutations. Verify exact main SHA, backup SHA, PR/merge IDs, checks, releases, artifacts, deployments and ledger commits.

## 100. Completion Report

Write `remotecompletion.md` and `oe2.txt` with timestamps, correlation IDs, exact SHAs, terminal outcomes, evidence references and remaining blockers.

## 101. Two-Repository Completion

Both repositories must independently satisfy all mandatory gates. One repository being complete cannot imply the other is complete.

## 102. Pre-Existing Blocker Handling

The documented prior 403 and divergence are historical blockers until freshly tested. Never carry an old PASS forward without refreshing its evidence.

## 103. Dual-Codespace Architecture

Either repository's Codespace must be able to host both repositories as independent working trees: `/workspaces/Alpha-Q-ai` and `/workspaces/qmoi-enhanced`. The Codespace origin is a workspace context, not repository ownership.

## 104. Cross-Repository Workspace Protocol

On startup, detect primary repository and peer repository, establish independent Git remotes, verify access, record both SHAs, and expose both working trees. Never create a nested `.git` relationship or treat one repository as a subdirectory mirror of the other.

## 105. Bidirectional Repository Capability

From an Alpha-Q-ai Codespace, permit authorized work on both Alpha-Q-ai and qmoi-enhanced; from a qmoi-enhanced Codespace, permit authorized work on both. Each commit and push must explicitly identify its repository and branch.

## 106. Low-Bandwidth Mobile Mode

Default browser-facing operation to metadata-first behavior: compact status, hashes, deltas, summaries and on-demand logs. Do not auto-download large artifacts, full diffs, dependency caches or complete workflow logs.

## 107. Remote-First Execution

Delegate full tests, builds, scans, release creation, artifact production and deployment to remote workflows. Use the Codespace for editing, orchestration and lightweight validation.

## 108. Codespace Lifecycle Controller

Detect active, idle, stopped, unhealthy and deleted states. Preserve work through commits/pushes and let autonomous Actions continue independently when the Codespace is stopped.

## 109. Cross-Repository Authentication

Use Codespaces additional-repository permissions where supported and explicitly authorized. For existing Codespaces whose permissions cannot be changed in place, use the documented authorized credential path or recreate the Codespace with the required permissions. Never assume access.

## 110. Workspace Lock Protocol

Maintain `.alpha.lock`, `.qmoi.lock` and `.crossrepo.lock` logically or through a safe lock service/file protocol. Include owner, operation, timestamp, TTL and recovery state. Never steal a live lock.

## 111. Autonomous Conflict Prevention

Before modifying a repository, inspect dirty state, active editor changes, branches, pending merges and remote movement. If a user is editing affected files, defer conflicting automation rather than overwriting work.

## 112. Transactional Synchronization

Cross-repo changes use PLAN → SNAPSHOT → CLASSIFY → APPLY ON BRANCH → VALIDATE → PR → CHECKS → MERGE → VERIFY. Direct bulk copying between working trees is not the default synchronization mechanism.

## 113. Lightweight Status Protocol

Provide compact status records containing repository, branch, local SHA, remote SHA, divergence count, workflow state, blocker count and evidence freshness. Full details are fetched only when requested.

## 114. Mobile Command Interface

Provide compact commands such as `q status`, `q status both`, `q sync both`, `q validate both`, `q workflows`, `q health`, `q evidence`, `q repair` and `q logs RUN_ID`. Commands should return summaries first.

## 115. Codespace Recovery

Provide safe repair for stale Git credentials, remotes, peer checkout, locks, processes, ports, caches and environment drift. Never perform destructive worktree reset automatically.

## 116. Autonomous Watchdog

Run scheduled/event-driven health checks for both repositories, workflows, PRs, checks, backups, releases, deployments, evidence freshness and cross-repo synchronization. Resume safe incomplete operations.

## 117. Remote Evidence Bus

Publish compact machine-readable completion events remotely and keep verbose diagnostics in workflow logs/artifacts. The phone-facing interface retrieves summaries by correlation ID.

## 118. Cross-Repository SHA Reconciliation

Continuously compare expected source/target relationships and record exact local, remote, PR, merge, release and backup SHAs. Never infer parity from matching filenames or history paths.

## 119. Artifact-on-Demand Policy

Do not download artifacts into the Codespace or browser unless requested or required for a local test. Prefer remote hash verification and metadata inspection.

## 120. Network Failure Tolerance

Classify DNS, transport, timeout, connection reset, HTTP and Git failures separately. Queue idempotent operations, back off and resume from recorded checkpoints after connectivity returns.

## 121. Offline/Disconnected Operation

A browser disconnect must not cancel safe remote workflows. Codespace and Actions state must be recoverable through correlation IDs after reconnection. Local uncommitted work remains protected.

## 122. Resource-Aware Execution

Monitor Codespace CPU, memory, disk and process health. Avoid starting competing heavy jobs. Prefer remote Actions for compute-heavy operations and stop unnecessary local services.

## 123. Prebuild Optimization

Use Codespaces prebuilds where appropriate, keep devcontainer setup deterministic, and avoid rebuilding expensive environments for every source-only change. Prebuild configuration must itself be tested and kept lightweight.

## 124. Dependency Cache Strategy

Use package-manager and Actions caches for immutable dependency inputs. Key caches by lockfile/toolchain identity and invalidate when dependency definitions change.

## 125. Remote Test Delegation

Expose one-command remote test dispatch for focused, full, installation, runtime, security and release validation. Return only compact results by default and retain full output remotely.

## 126. Automatic Environment Health Checks

At Codespace startup and periodically, verify Git, GitHub authentication, both repository access paths, remotes, disk, memory, required tools, ports, locks and controller health.

## 127. Safe User/Agent Concurrency

Separate human editing from autonomous mutation. Agents may observe freely but must acquire operation locks before mutation. User work always wins over conflicting automation.

## 128. Cross-Repository PR Automation

When synchronization changes the peer repository, automatically create/update a target-owned branch and PR, attach correlation/evidence, wait for required checks, respect reviews/queues, and verify the resulting merge SHA.

## 129. Release/Deployment Independence

Releases and deployments must run from repository-owned workflows and survive Codespace disconnection. The Codespace may request, observe and verify them but must not be their single point of execution.

## 130. Final Remote Completion Controller

The final controller evaluates every mandatory gate across both repositories. It may emit `REMOTE COMPLETION VERIFIED` only after independent remote evidence proves all required gates; otherwise it emits `REMOTE COMPLETION BLOCKED — EVIDENCE ATTACHED` with exact blockers and capabilities needed.

---

# Preflight Checklist

Before any mutation:

- [ ] authenticated identity verified
- [ ] both repository identities verified
- [ ] default branches verified remotely
- [ ] current remote SHAs captured
- [ ] local/remote divergence classified
- [ ] peer repository access verified
- [ ] Codespace cross-repository permissions verified
- [ ] Actions read/dispatch capability verified
- [ ] PR/check/release/artifact capability verified
- [ ] rulesets/protection inspected
- [ ] workflow files and triggers verified
- [ ] correlation ID created
- [ ] active user edits detected
- [ ] locks checked
- [ ] bandwidth mode selected
- [ ] resource budget checked
- [ ] current evidence freshness checked

Before synchronization:

- [ ] both trees independently inventoried
- [ ] ownership map loaded
- [ ] changed paths identified
- [ ] destructive changes excluded
- [ ] synchronization plan recorded
- [ ] snapshot recorded
- [ ] target branch policy identified

Before merge:

- [ ] PR exists in target repository
- [ ] PR head SHA recorded
- [ ] required checks correspond to current SHA
- [ ] required reviews satisfied
- [ ] merge queue/ruleset requirements satisfied
- [ ] no unresolved merge conflict
- [ ] no stale-plan condition

Before release:

- [ ] merge SHA verified
- [ ] build succeeded from intended SHA
- [ ] artifact hashes recorded
- [ ] installation test passed
- [ ] runtime test passed
- [ ] release publication verified
- [ ] release assets independently retrievable

Before deployment:

- [ ] deployment source SHA verified
- [ ] environment requirements satisfied
- [ ] deployment terminal state verified
- [ ] health endpoint/runtime evidence verified

Before completion:

- [ ] Alpha-Q-ai main SHA verified
- [ ] qmoi-enhanced main SHA verified
- [ ] backup parity verified
- [ ] Markdown inventory fresh
- [ ] validation ledger fresh
- [ ] release ledger fresh
- [ ] merge ledger fresh
- [ ] evidence ledger complete
- [ ] no mandatory gate is UNKNOWN/STALE
- [ ] all blockers are resolved or explicitly terminal
- [ ] final verifier independently reread remote state

---

# Evidence Ledger Schema

File: `remote-evidence-ledger.jsonl`

One immutable event per line:

```json
{
  "schema_version": "1.0",
  "event_id": "uuid",
  "correlation_id": "uuid",
  "timestamp": "ISO-8601",
  "repository": "owner/repo",
  "operation": "string",
  "stage": "string",
  "actor_type": "human|workflow|agent|app|codespace",
  "actor_id": "non-secret identifier",
  "request": {
    "method": "GET|POST|PATCH|PUT|DELETE|GIT",
    "endpoint_class": "string",
    "ref": "string",
    "source_sha": "string",
    "target_sha": "string"
  },
  "response": {
    "http_status": 0,
    "message_class": "string",
    "run_id": "string",
    "job_id": "string",
    "pr_number": "string",
    "release_id": "string",
    "deployment_id": "string"
  },
  "result": {
    "status": "PASS|FAIL|PENDING|BLOCKED|UNKNOWN",
    "conclusion": "string",
    "remote_sha": "string",
    "artifact_sha256": "string"
  },
  "diagnosis": {
    "failure_class": "string",
    "failure_signature": "string",
    "retryable": false,
    "repairable": false,
    "authorization_related": false
  },
  "verification": {
    "level": "NONE|LOCAL|REMOTE_OBSERVED|REMOTE_TERMINAL|REMOTE_INDEPENDENTLY_VERIFIED",
    "verified": false,
    "verified_at": "ISO-8601",
    "method": "string"
  },
  "evidence_refs": [],
  "next_action": "string"
}
```

## Final Completion Contract

The only successful terminal result is:

```text
REMOTE COMPLETION VERIFIED
```

when every mandatory gate has level-4 remote independent verification.

Otherwise:

```text
REMOTE COMPLETION BLOCKED — EVIDENCE ATTACHED
```

with exact blockers, affected repository/operation, current state, last known
remote SHA and required capability/action.

## Low-Bandwidth Defaults

Default browser profile:

```text
MODE=MOBILE
LOGS=SUMMARY
DIFFS=ON_DEMAND
ARTIFACTS=ON_DEMAND
FULL_TESTS=REMOTE
BUILDS=REMOTE
SECURITY_SCANS=REMOTE
POLLING=EVENT_OR_SLOW
METADATA_FIRST=true
AUTO_DOWNLOAD=false
```

## Suggested Workspace Commands

```bash
q status
q status alpha
q status qmoi
q status both

q health
q sync alpha
q sync qmoi
q sync both

q validate alpha
q validate qmoi
q validate both

q workflows
q evidence
q repair
q logs <run-id>
q release <repo>
q deploy <repo>
```

These commands should be thin clients to remote operations and should return compact
summaries by default.

## Copilot / Agent Operating Contract

Create in both repositories:

- `.github/copilot-instructions.md`
- `AGENTS.md`
- `.github/instructions/workspace.instructions.md`
- `.github/instructions/github-api.instructions.md`
- `.github/instructions/workflows.instructions.md`
- `.github/instructions/release.instructions.md`
- `.github/instructions/security.instructions.md`

Copilot/agents must obey:

1. inspect before modifying;
2. preserve user work;
3. never force-push;
4. never bypass protection;
5. never expose credentials;
6. never infer remote state;
7. treat 404 as diagnostically ambiguous;
8. treat 403 as diagnostically ambiguous;
9. distinguish dispatch from completion;
10. distinguish merge from release;
11. distinguish release from deployment;
12. use exact SHAs;
13. use correlation IDs;
14. use bounded retries;
15. repair deterministic failures;
16. revalidate every repair;
17. isolate authorization blockers;
18. continue independent read-only work;
19. keep evidence synchronized;
20. never say COMPLETE without final remote verification.

## Final Design Principle

The platform should behave as:

```text
OBSERVE
  -> CLASSIFY
  -> PLAN
  -> LOCK
  -> APPLY
  -> VALIDATE
  -> REMOTE EXECUTE
  -> WATCH
  -> RECOVER
  -> VERIFY
  -> PUBLISH
  -> VERIFY AGAIN
  -> COMPLETE
```

while the human-facing channel behaves as:

```text
SMALL REQUEST
  -> SMALL STATUS
  -> REMOTE COMPUTE
  -> SMALL RESULT
```

This is the intended low-bandwidth operating model.
