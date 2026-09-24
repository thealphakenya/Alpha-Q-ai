# QMOI + Ollama Autonomous Production Completion & Live Activity Stream Master Plan

**Repositories:** `thealphakenya/qmoi-enhanced` and
`thealphakenya/Alpha-Q-ai`\
**Primary branch:** `main`\
**Coordination branch:** `autosync-backup`\
**Completion marker:** `Q.0.0.N`

**Canonical Alpha source policy:** `Alpha-Q-ai-2025` is the only accepted
name for the materialized Alpha source tree. All merge planners, audits,
inventories, documentation, evidence, automation, and generated path lists
must use that name; no legacy Alpha-history identifier may be reintroduced.
Before any merge, Alpha-Q-ai's existing tree and every file and
directory in `Alpha-Q-ai-2025` are jointly treated as its base. Likewise,
qmoi-enhanced's existing tree and every file and directory in
`qmoi-enhanced-history-14` are jointly treated as its base. The pre-merge
qmoi-enhanced contents are the research and implementation reference for
Alpha-Q-ai changes, while ownership, conflict, authorization, and validation
gates remain mandatory.

> **Implementation contract:** This document is for GitHub Copilot
> Chat/Agent or another repository automation operator. Inspect the
> actual repositories before modifying them. Do not treat existing
> documentation as proof that a feature works. Implement, test, repair,
> and independently verify every applicable requirement. Never report
> success merely because Ollama ran or a workflow was green.

## 1. Complete autonomous lifecycle

The complete lifecycle in both repositories must be:

``` text
DISCOVER
→ INSPECT BOTH REPOSITORIES
→ INVENTORY
→ DETERMINE REQUIRED CHANGES
→ PLAN
→ MODIFY FILES
→ SELF-REVIEW
→ TEST
→ LINT / TYPE / STATIC VALIDATION
→ SECURITY / SECRET / DEPENDENCY VALIDATION
→ BUILD / RUNTIME VALIDATION
→ PRODUCTION CONTRACT VALIDATION
→ RE-INSPECT GIT DIFF
→ COMMIT
→ PUSH
→ VERIFY REMOTE SHA
→ DISCOVER BRANCHES
→ DISCOVER PRs
→ CREATE / UPDATE PR
→ WAIT FOR REQUIRED CHECKS
→ DIAGNOSE FAILURES
→ SELF-REPAIR
→ REVALIDATE
→ MERGE WHEN CONTRACT IS SATISFIED
→ VERIFY MERGE
→ VERIFY main
→ SYNCHRONIZE autosync-backup
→ VERIFY autosync-backup
→ SYNCHRONIZE THE OTHER REPOSITORY
→ VERIFY CROSS-REPOSITORY STATE
→ UPDATE DOCUMENTATION
→ GENERATE Q.0.0.N
→ VERIFY Q.0.0.N
→ UPDATE LIVE ACTIVITY
→ WRITE FINAL EVIDENCE
→ FINAL REMOTE INSPECTION
→ FINAL SECURITY/PRODUCTION CHECK
→ ONLY THEN SUCCESS
```

Every stage requires an execution ID, timestamp, status, evidence,
errors, retry information, and repository/branch/SHA context. Silent
skipping is prohibited; a non-required stage must be recorded as
`NOT_APPLICABLE` with a reason.

## 2. Q.0.0.(numbering) should become part of the completion protocol

Every completed autonomous production cycle must receive a deterministic
`Q.0.0.N` number.

The agent must discover existing Q versions in **both** repositories,
select the next valid number, prevent collisions, use the same logical
number for the coordinated cycle, and create the Q-version artifacts in
both repositories.

The complete topic inventory for this master plan has been verified at
exactly 208 headings. The canonical execution ledger is stored in
`ollama_master_topic_index.txt` and must remain synchronized with this
plan. Every topic is treated as a production task with the same
standard evidence envelope: inspect, implement, validate, self-heal,
verify remote state, and publish final evidence. No topic is considered
complete without live repository evidence.

The continuation contract for each numbered topic is:

``` text
inspect → implement → validate → repair if needed → verify evidence → record status → continue
```

The live continuity tasks remaining from `oe2.txt` are also tracked as
obligations that must be reconciled with this 208-topic plan before any
final success claim is made.

The live ledger records mutually exclusive topic metrics. Until individual
evidence envelopes prove every required gate for a topic, that topic remains
`IN PROGRESS`; aggregate tests or documentation do not count as full
completion. The current snapshot records 208 discovered topics, 0 fully
proven topics, and 208 active topics, with remote merge, authorization, and
security conditions tracked as separate blockers. The autonomous merge-audit
path computes plan/index parity, evidence coverage, unproven-topic lists, and
status-count integrity, and writes the machine-readable result to
`ollamatracks/topic_metrics.json`.

The model responsibility extension is part of the same gate: Ollama and QMOI
must inspect current and materialized historical sources before changing model
behavior, discover and run applicable model tests, refresh both
`MODEL_CARD.md` and `QMOI_MODEL_CARD.md`, and synchronize the same evidence to
the QVillage model UI. Model-card or QVillage updates must expose timestamps,
execution identity, test status, source/merge evidence, and blocked or stale
states; they must never manufacture production health from missing evidence.

QMOI awareness and memory synchronization is likewise a cross-surface
responsibility. The Master Orchestrator must inventory both repositories,
materialized history, platform adapters, applications, model inference/tests,
automation, workflows, live activity, security, finance, deployment, and
runtime state; refresh the memory and awareness artifacts with correlated
execution IDs, branches, SHAs, and timestamps; and plan additive improvements
across existing features before promotion. Missing, stale, blocked, or
unavailable sources remain explicit failures and cannot be reported as
synchronized consciousness or healthy automation.

Recommended structure:

``` text
Q.0.0.N/
├── README.md
├── COMPLETION.md
├── CHANGES.md
├── VALIDATION.md
├── SECURITY.md
├── TESTS.md
├── MERGE.md
├── SYNCHRONIZATION.md
├── LIVE_ACTIVITY.md
└── evidence/
    ├── execution.json
    ├── repository-state.json
    ├── commits.json
    ├── checks.json
    └── verification.json

Q.0.0.N.md
```

The number must be reserved safely and verified after the final push. A
Q-version must never claim completion before final verification.Automate and enhance further so that in future qmoi could be also be able to do everything ollama autonomous agent does and also automatically create the Q.0.0.N directory and .md files if instructed by master or when it automatically wants too noting the evolution, autoresearch, auto evolution and all other qmoi autimations best

## 3. The Q.0.0.N document should explicitly prove completion

`Q.0.0.N.md` and `Q.0.0.N/COMPLETION.md` must be evidence records, not
marketing text.

They must record:

-   execution and parent execution IDs;
-   start and completion timestamps;
-   agent/orchestrator versions;
-   repository and branch;
-   before SHA, commit SHA, after SHA and verified remote SHA;
-   files inspected/added/changed/deleted;
-   tests, lint, type/static validation, security, dependency checks,
    build and runtime validation;
-   commit/push result;
-   PR number/head SHA;
-   required checks;
-   merge method and merge SHA;
-   verified `main` SHA;
-   `autosync-backup` SHA and verification;
-   other-repository synchronization result;
-   QMOI, Ollama and Master Orchestrator live activity evidence;
-   production-readiness result;
-   final status.

Evidence must be generated from actual execution state. Fake SHAs, URLs,
test results or heartbeat data are forbidden. 

## 4. Self-healing is essential

Implement a bounded repair loop:

``` text
FAILURE
→ CLASSIFY
→ DETERMINE SAFE/AUTOMATABLE REPAIR
→ REPAIR
→ VALIDATE
→ RETRY FAILED STAGE
→ PASS: CONTINUE
→ FAIL: NEXT REPAIR STRATEGY
```

Record every failure and repair attempt. Cover recoverable
workflow/configuration errors, dependency installation problems,
deterministic test failures, malformed generated documentation, Git
index/worktree problems, stale branch metadata, recoverable API/network
errors, stale tracker data and live-stream failures.

Never bypass security, branch protection or authorization to obtain
success. Never repeatedly execute the same failed operation and label it
self-healing.

## 5. The Master Orchestrator should supervise failures

The Master Orchestrator is the supervisory control plane. It must:

-   discover state;
-   dispatch/resume the autonomous agent;
-   monitor heartbeats;
-   monitor stage transitions;
-   detect stale executions;
-   recover from checkpoints;
-   detect failures;
-   initiate bounded recovery;
-   revalidate after recovery;
-   verify final remote state;
-   publish final evidence.

Required states include:

``` text
RUNNING
WAITING
RETRYING
SELF_HEALING
STALE
RECOVERING
BLOCKED
FAILED
COMPLETED
SUCCESS
NO_CHANGES_REQUIRED
```

A successful workflow dispatch is **not** successful repository
completion.

## 6. Human intervention should be unnecessary for ordinary operations

The normal path must autonomously handle inspection, modification,
testing, linting, security checks, commits, pushes, PR creation/update,
check monitoring, safe repairs, authorized merges, branch
synchronization, cross-repository synchronization, Q-version generation,
documentation, telemetry and final verification.

Human intervention should be reserved for genuine external constraints
such as unavailable credentials, GitHub permissions that cannot be
granted, mandatory human review, protected high-risk actions, unresolved
ambiguity or unavailable external infrastructure.

When blocked, publish the exact blocker and a resumable checkpoint.
Never manufacture success.

## 7. Production readiness must be a gate, not a statement

Before final success, independently verify:

**Code:** tests, lint, type/static checks where applicable,
syntax/import checks, build, runtime smoke tests and configuration.

**Security:** secret scanning, dependency vulnerabilities, workflow
security, token scope, untrusted PR hazards and dangerous shell/Git
operations.

**Git:** worktree state, commit, remote, remote SHA, branch, PR, checks,
merge, `main` and `autosync-backup`.

**Operations:** checkpoint/resume, stale detection, telemetry, live
activity, failure-state publication and evidence retention.

**Cross-repository:** both repositories independently valid and their
shared contract verified.

Only then:

``` text
PRODUCTION_READY=true
FINAL_STATUS=SUCCESS
```

## 8. Most importantly: eliminate "green wrapper" success

Never report success merely because:

``` text
Ollama started
Model available
Inference successful
Tests passed
Checkpoint created
```

A successful completion must prove the complete applicable chain:

``` text
DISCOVERY PASS
INSPECTION PASS
PLAN PASS
MODIFICATION PASS/N-A
VALIDATION PASS
DIFF VERIFICATION PASS
COMMIT PASS/N-A
PUSH PASS/N-A
REMOTE SHA PASS
PR PASS/N-A
CHECKS PASS/N-A
MERGE PASS/N-A
MERGE VERIFICATION PASS/N-A
MAIN VERIFICATION PASS
AUTOSYNC VERIFICATION PASS
CROSS-REPO VERIFICATION PASS
Q-VERSION PASS
LIVE ACTIVITY PASS
EVIDENCE PASS
SECURITY PASS
PRODUCTION READINESS PASS
FINAL REMOTE VERIFICATION PASS
```

Failure must become `FAILED_AT_<STAGE>`. A legitimate no-change run
becomes `NO_CHANGES_REQUIRED`.

## 9. The ultimate invariant

> The Ollama Autonomous Agent is not successful because it ran
> successfully. It is successful only when it has demonstrably brought
> every applicable repository, Git state, merge state, synchronization
> state, documentation state, Q.0.0.N evidence state, security state,
> validation state, production-readiness state and live-observability
> state to the required condition and independently verified that final
> state.

Formally:

``` text
SUCCESS =
ALL_REQUIRED_STAGES_PASS
AND REMOTE_STATE_VERIFIED
AND FINAL_PRODUCTION_CHECK_PASS
AND Q_VERSION_VERIFIED
AND LIVE_ACTIVITY_VERIFIED
```

## 10. Repository architecture

Use a layered design rather than putting all responsibility into one LLM
script. Reuse existing modules where sound.

Recommended responsibilities:

``` text
ollama_autonomous_agent.py       # reasoning/execution coordinator
ollama_autonomous_agent_enhanced.py
autonomous_completion_engine.py  # authoritative completion state machine
repository_inspector.py
repository_mutator.py
git_execution_manager.py
github_pr_manager.py
github_merge_manager.py
cross_repository_sync.py
q_version_manager.py
production_readiness.py
security_gate.py
evidence_manager.py
execution_state.py
checkpoint_manager.py
live_activity_stream.py
live_activity_server.py
orchestrator_health.py
```

The LLM reasons about what should happen; deterministic components
perform and verify Git/GitHub operations. Only one authoritative
completion engine may produce the final verdict.

## 11. Thorough Ollama-agent inspection

Before changing anything, inspect all relevant files in both
repositories:

-   Ollama autonomous-agent scripts;
-   enhanced agent implementations;
-   Master Orchestrator;
-   autonomous-agent workflows;
-   PR validation and monitoring workflows;
-   merge/sync workflows;
-   `ollamatracks`;
-   tests;
-   state/checkpoint files;
-   telemetry;
-   live activity scripts/workflows;
-   merge/sync documentation;
-   monitoring documentation;
-   resilience/auto-healing documentation;
-   GitHub setup/permissions documentation.

Build a machine-readable inventory:

``` text
component
location
purpose
entry point
caller
workflow
inputs
outputs
permissions
side effects
tests
known gaps
```

Classify every requirement as:

``` text
IMPLEMENTED
PARTIALLY_IMPLEMENTED
DOCUMENTED_ONLY
MISSING
BROKEN
DUPLICATED
CONFLICTING
```

Create `AUTONOMOUS_COMPLETION_GAP_MATRIX.md`.

## 12. Autonomous Agent execution contract

Create one authoritative operation conceptually equivalent to:

``` text
autonomous_complete
```

It must load/resume state, create an execution ID, inspect both
repositories, plan, modify, validate, self-heal, perform the GitHub
lifecycle, synchronize, generate Q-version evidence, publish live
activity, write evidence, perform final verification and return a
structured result.

All successful paths must converge on the same final completion gate.

## 13. Git commit and push must be first-class verified operations

Implement explicit operations:

``` text
prepare_commit()
create_commit()
verify_commit()
push_branch()
verify_remote_branch()
```

Record:

``` text
before_sha
commit_sha
remote_sha
branch
remote
changed_files
```

After push, independently compare local and remote references. A push
without remote verification is incomplete.

## 14. PR lifecycle must be autonomous

The agent must list PRs, correlate an existing PR to the execution,
create/update one when needed, wait for checks, inspect failures, repair
where safe, re-run checks, verify the PR head SHA, and merge when policy
permits.

Prevent duplicate PRs.

## 15. Merge operations must be real merge operations

Use explicit states:

``` text
PR_CREATED
PR_UPDATED
CHECKS_PENDING
CHECKS_FAILED
CHECKS_PASSED
MERGE_READY
MERGE_EXECUTED
MERGE_VERIFIED
```

After merge verify that the PR is actually merged, the merge SHA exists,
and remote `main` contains the expected result.

Never treat a successful command return alone as proof.

## 16. autosync-backup must be synchronized and verified

After `main` is finalized:

``` text
main → autosync-backup
```

Inspect divergence, select a deterministic safe strategy, update, push,
verify remote SHA and record the relationship between the branches.

Do not overwrite unrelated work automatically.

## 17. Cross-repository synchronization

Coordinate:

``` text
thealphakenya/qmoi-enhanced
thealphakenya/Alpha-Q-ai
```

without blindly mirroring their entire trees.

Define shared synchronization classes:

``` text
SHARED_AUTOMATION
SHARED_TRACKING
SHARED_DOCUMENTATION
SHARED_Q_VERSION
REPOSITORY_SPECIFIC
```

Synchronize only contractually shared paths. Verify expected files,
shared versions, workflow contracts and Q-version consistency.

## 18. QMOI live activity stream

The QMOI stream must expose real QMOI activity rather than merely
workflow existence.

Minimum event fields(you can also add more event fields to ebsure it contains all event fields it should have):

``` json
{
  "timestamp": "...",
  "execution_id": "...",
  "source": "QMOI",
  "component": "...",
  "event": "...",
  "status": "RUNNING",
  "message": "...",
  "repository": "...",
  "workflow": "...",
  "run_id": "...",
  "url": "...",
  "stage": "...",
  "sequence": 123,
  "heartbeat": true
}
```

Include startup, heartbeat, task start/end, model, memory, repository,
validation, recovery, synchronization and completion events.

## 19. Ollama Autonomous Agent live activity stream

The Ollama stream must independently expose:

``` text
AGENT_STARTED
DISCOVERY
INSPECTION
PLANNING
MODIFICATION
VALIDATION
SELF_REPAIR
COMMIT
PUSH
REMOTE_VERIFY
PR_DISCOVERY
PR_UPDATE
CHECKS
MERGE
MERGE_VERIFY
BACKUP_SYNC
CROSS_REPO_SYNC
Q_VERSION
FINAL_VERIFY
SUCCESS
FAILURE
```

Every event needs an exact timestamp and execution ID.

Do not infer activity merely because a workflow exists.

## 20. Fix the live activity stream architecture in both repositories

The existing `liveactivitystream.md` files describe source-labelled QMOI
and Ollama streams, and the repositories already contain live activity
generation/workflow infrastructure. Upgrade this into a verifiable
observability system:

``` text
AGENT EVENTS
→ JSONL EVENT STORE
→ LIVE STREAM GENERATOR
→ CURRENT-STATE JSON
→ GITHUB ARTIFACT
→ OPTIONAL HTTP/SSE/WEBSOCKET VIEW
→ QMOI MONITOR/UI
```

Use append-only JSONL for history and a compact current-state JSON for
fast display. GitHub artifacts must not be the only current-state
source.

## 21. Live activity must be genuinely observable

Expose:

-   current execution;
-   current stage;
-   last event;
-   last event timestamp;
-   heartbeat;
-   agent status;
-   orchestrator status;
-   repository status;
-   current/target SHA;
-   PR;
-   checks;
-   merge;
-   Q-version;
-   errors;
-   retry count.

Define:

``` text
HEALTHY
STALE
OFFLINE
FAILED
```

and ensure the UI cannot display `RUNNING` forever after heartbeat
expiry.

## 22. Live activity must work in both repositories

Both repositories must expose the same logical streams:

``` text
QMOI LIVE ACTIVITY
OLLAMA AUTONOMOUS AGENT LIVE ACTIVITY
MASTER ORCHESTRATOR ACTIVITY
```

Each must support local, remote and cross-repository events, workflow
URLs, execution IDs, stage, status and freshness.

## 23. Live stream freshness verification

Test:

-   event creation;
-   serialization;
-   ordering;
-   duplicate handling;
-   heartbeat;
-   stale detection;
-   failure;
-   recovery;
-   remote lookup;
-   missing remote data;
-   artifact generation;
-   current-state generation;
-   rendering;
-   cross-repository events.

A test must fail if the stream reports live activity beyond the
configured freshness threshold.

## 24. Master Orchestrator heartbeat/watchdog

Implement agent, orchestrator, stage and repository heartbeats.

Detect:

``` text
no heartbeat
workflow unexpectedly ended
agent disappeared
state stopped advancing
GitHub run stopped
PR checks stale
```

Resume from checkpoints rather than blindly restarting.

## 25. Checkpoint and resume

Persist:

``` text
execution_id
parent_execution_id
current_stage
completed_stages
failed_stages
retry_counts
repository SHAs
PR numbers
Q-version
last successful operation
next operation
```

Make checkpoints atomic and resumable. Do not repeat destructive
operations merely because state is incomplete.

## 26. Idempotency

Make operations idempotent wherever practical:

-   PR create/update;
-   branch sync;
-   Q-version generation;
-   event publication;
-   evidence writing;
-   workflow repair.

Use execution/operation IDs. Re-running an operation must not create
duplicate PRs, duplicate versions or corrupted tracker state.

## 27. Concurrency control

Prevent simultaneous runs from modifying the same repository state.

Use GitHub Actions concurrency, repository-aware execution locks,
Q-version collision protection and stale-lock recovery.

## 28. GitHub permissions and security

Use least privilege. Review `contents`, `pull-requests`, `actions`,
`checks` and `issues` permissions according to actual operations.

Never store credentials in code, `.env.example`, logs, artifacts,
Q-version evidence or live messages. Use GitHub-provided authentication
where possible. Treat historically committed credentials as compromised
and rotate them.

Never execute untrusted fork PR code with privileged credentials.

## 29. Pull-request safety

Separate trusted main-branch automation from untrusted PR validation.
Untrusted changes should be validated without privileged mutation
credentials. Only trusted automation may push/merge.

## 30. Workflow architecture

Consolidate into clearly defined responsibilities, adapting existing
workflow names rather than creating duplicates:

``` text
ollama-master-orchestrator.yml
ollama-autonomous-agent.yml
ollama-live-activity-stream.yml
qmoi-live-activity-stream.yml
ollama-pr-validation.yml
autonomous-production-verification.yml
cross-repository-sync.yml
```

GitHub Actions should orchestrate jobs, permissions, environment,
artifacts, dependencies and dispatch; complex business logic should live
in tested code.

## 31. Master Orchestrator responsibilities

The orchestrator should:

``` text
schedule
dispatch
monitor
resume
retry
recover
coordinate
verify
publish
```

It should supervise rather than duplicate the agent's reasoning.

## 32. Autonomous Agent responsibilities

The agent should:

``` text
inspect
reason
plan
modify
validate
repair
request deterministic Git/GitHub operations
interpret failures
produce evidence
```

GitHub/Git and deterministic verification remain the source of truth.

## 33. Deterministic completion engine

Implement one authoritative completion engine with a structured result
containing:

``` text
status
stage
execution_id
repository_results
cross_repository_result
q_version
live_activity
evidence
errors
```

Only this engine may produce the final completion verdict.

## 34. No-change completion

If no change is required, the agent must still inspect, validate, verify
remote state, verify synchronization and create evidence. Report:

``` text
NO_CHANGES_REQUIRED
```

Do not manufacture commits merely to create activity.

## 35. Change detection

After modifications run:

``` text
git status
git diff --stat
git diff --name-status
git diff --check
```

Compare actual changes with the plan. Missing intended changes are a
failure unless the plan was legitimately revised and recorded.

## 36. File integrity

Detect malformed YAML/JSON/Markdown, duplicate workflow keys, missing
generated files, unexpected deletion, broken references and stale
documentation.

## 37. Documentation synchronization

Inspect and update relevant existing documentation, especially:

``` text
README.md
OLLAMA_AUTOMATION_GUIDE.md
MONITORING_GUIDE.md
MONITORING_INDEX.md
REAL_TIME_MONITORING_GUIDE.md
REAL_TIME_MONITORING_README.md
RESILIENCE_AUTO_HEALING.md
MERGE.md
SYNC.md
WORKFLOWS.md
WORKFLOW_EXECUTION_PLAN.md
WORKFLOW_STATUS_DASHBOARD.md
liveactivitystream.md
```

Also inspect the corresponding Alpha-Q-ai documents. Do not rewrite
accurate documentation unnecessarily.

## 38. Test architecture

Add tests for:

-   state transitions;
-   idempotency;
-   retries;
-   Q-version numbering;
-   Git SHA verification;
-   PR discovery;
-   merge verification;
-   cross-repository synchronization;
-   evidence generation;
-   stale detection;
-   live activity;
-   heartbeat;
-   checkpoint/resume.

Add integration/end-to-end tests where safe.

## 39. Failure injection

Test controlled failures for:

``` text
Ollama unavailable
model unavailable
test failure
lint failure
security failure
commit failure
push failure
remote mismatch
PR failure
check failure
merge failure
backup sync failure
cross-repo failure
Q-version failure
live-stream failure
stale heartbeat
```

Verify correct failure states and recovery.

## 40. Fail-closed required gates

If a required security, remote verification or live-activity check
cannot run, use `UNKNOWN`/failure, not pass.

Examples:

``` text
SECURITY_UNKNOWN ≠ SECURITY_PASS
REMOTE_VERIFY_UNKNOWN ≠ SUCCESS
LIVE_ACTIVITY_UNKNOWN ≠ SUCCESS
```

## 41. Evidence architecture

Use `ollamatracks` as a machine-readable execution ledger:

``` text
ollamatracks/
├── CURRENT_STATUS
├── TRACKING_INDEX
├── telemetry.jsonl
├── current_state.json
├── executions/
│   └── <execution_id>/
│       ├── execution.json
│       ├── stages.json
│       ├── repository-state.json
│       ├── git.json
│       ├── pull-requests.json
│       ├── merge.json
│       ├── synchronization.json
│       ├── validation.json
│       ├── security.json
│       ├── live-activity.json
│       └── final-verification.json
└── checkpoints/
```

## 42. Telemetry schema

Every event should contain:

``` text
timestamp
execution_id
sequence
repository
source
component
stage
event
status
message
run_id
commit_sha
branch
pr_number
q_version
duration_ms
retry
error
```

Machine decisions must use structured fields, not free-form logs.

## 43. Current status file

`CURRENT_STATUS` must show:

``` text
Execution
Agent
Orchestrator
Repository
Stage
Status
Started
Last heartbeat
Current SHA
Target SHA
PR
Checks
Merge
Q-version
Last error
Next action
Final status
```

Generate it from structured state.

## 44. Live stream UI contract

The operational monitor should show:

**Overview:** agent, QMOI and orchestrator status, heartbeat, execution.

**Timeline:** ordered events, source, status, duration, links.

**Repository:** branch, SHA, target SHA, diff, PR, checks, merge, sync.

**Recovery:** failures, retries and repairs.

**Completion:** Q-version, production readiness and evidence.

## 45. Define "live" precisely

If transport is polling/GitHub Actions, document the actual refresh
interval and freshness threshold. If using SSE/WebSocket, implement true
push.

``` text
LIVE =
freshness <= threshold
AND heartbeat current
AND state source reachable
```

Never show stale snapshots as live.

## 46. Remote workflow observability

Where available show:

``` text
workflow name
run ID
run URL
status
conclusion
created
started
updated
completed
branch
SHA
```

If remote state is unavailable, publish `REMOTE_STATUS_UNAVAILABLE`.

## 47. Cross-repository live activity

Use:

``` text
execution_id
parent_execution_id
correlation_id
```

to correlate activity from `qmoi-enhanced`, `Alpha-Q-ai`, QMOI and the
orchestrator.

## 48. QMOI and Ollama event separation

Use source labels:

``` text
QMOI
OLLAMA_AGENT
MASTER_ORCHESTRATOR
GITHUB
VALIDATION
SECURITY
SYNC
```

Also distinguish QMOI process/model/memory/task events from Ollama
process/model/inference/agent events.

## 49. Monitoring correctness tests

Prove:

``` text
agent running → RUNNING
agent progresses → stage changes
agent fails → FAILED
agent repairs → SELF_HEALING
agent resumes → RECOVERING
agent completes → SUCCESS
heartbeat expires → STALE/OFFLINE
```

Automate these tests.

## 50. Orchestrator/live-stream integration

Publish:

``` text
ORCHESTRATOR_STARTED
AGENT_DISPATCHED
AGENT_HEARTBEAT
AGENT_STAGE_CHANGED
AGENT_STALLED
RECOVERY_STARTED
RECOVERY_COMPLETED
FINAL_VERIFICATION_STARTED
FINAL_VERIFICATION_COMPLETED
```

## 51. Q-version directory synchronization

Both repositories must contain the same logical `Q.0.0.N` completion
cycle. Include execution ID, Q-version, repository-specific SHA
information and cross-repository references.

## 52. Q-version collision protection

Two simultaneous runs must never create the same Q number. Use atomic
reservation/locking and re-check before final commit. Automatically
recover from a collision by selecting the next unused number.

## 53. Final remote verification

After all mutations:

``` text
git fetch --all --prune
```

Then verify:

``` text
origin/main
origin/autosync-backup
```

and verify Q-version files are actually present remotely. Generate final
evidence from final remote state.

## 54. Final repository inspection

Inspect remote `main` for both repositories, both `autosync-backup`
branches, Q-version artifacts, relevant workflows and current
live-activity state.

Only after this can the completion engine declare success.

## 55. Production-ready invariant

For each repository:

``` text
REMOTE_MAIN_VERIFIED
AND REMOTE_BACKUP_VERIFIED
AND REQUIRED_CHECKS_VERIFIED
AND SECURITY_VERIFIED
AND Q_VERSION_VERIFIED
AND LIVE_ACTIVITY_VERIFIED
AND DOCUMENTATION_VERIFIED
```

## 56. Cross-repository invariant

For the pair:

``` text
EXECUTION_ID_MATCHES
AND Q_VERSION_MATCHES
AND SHARED_AUTOMATION_CONTRACT_MATCHES
AND EXPECTED_SHARED_FILES_MATCH
AND EACH_REPOSITORY_IS_INDEPENDENTLY_VALID
```

## 57. No hidden incomplete stages

Every execution must terminate as exactly one of:

``` text
SUCCESS
NO_CHANGES_REQUIRED
BLOCKED_REQUIRES_HUMAN
FAILED_AT_<STAGE>
```

Invalid states include `SUCCESS_BUT_NOT_PUSHED`,
`SUCCESS_BUT_NOT_MERGED`, `SUCCESS_BUT_NOT_VERIFIED`, or any other
success-with-unknown-state variant.

## 58. Copilot Chat execution mode

When this document is provided to Copilot Chat/Agent, it must act as an
implementation agent:

1.  Read the entire document.
2.  Inspect both repositories completely enough to map every relevant
    implementation.
3.  Inspect all Ollama
    agent/orchestrator/live-stream/merge/sync/tracking files.
4.  Do not assume documentation equals runtime behavior.
5.  Build the gap matrix.
6.  Implement the completion architecture.
7.  Preserve working functionality.
8.  Consolidate duplicates/conflicts.
9.  Add regression tests.
10. Run tests/lint/security/static validation.
11. Verify workflow syntax and permissions.
12. Verify Git lifecycle.
13. Verify Q-version generation.
14. Verify live activity.
15. Verify cross-repository behavior.
16. Repair failures autonomously.
17. Repeat until all applicable gates pass.
18. Produce final evidence.
19. Independently verify final remote state.
20. Do not claim completion without evidence.

## 59. Copilot must inspect before modifying

Before edits inspect:

``` text
git status
git branch -a
git log
all relevant workflows
all Ollama files
live activity files
tracking files
Q-version files
merge/sync files
tests
```

Then classify the implementation using the gap matrix.

## 60. Do not rewrite working systems unnecessarily

For sound existing components:

``` text
KEEP → HARDEN → TEST → INTEGRATE
```

For conflicts:

``` text
SELECT AUTHORITATIVE IMPLEMENTATION
→ MIGRATE DEPENDENCIES
→ REMOVE DUPLICATE PATH
→ ADD REGRESSION TEST
```

## 61. Keep workflows thin

Avoid giant monolithic YAML. Keep stateful logic in tested code; Actions
should provide checkout, environment, permissions, job dependencies,
dispatch, retries and artifact handling.

## 62. Permissions must match operations

Review required GitHub permissions for push, PR, checks, Actions and
merge operations. Prefer job-level least privilege.

## 63. Merge policy integration

Before autonomous merge inspect branch protection/rules, required
checks, approvals, merge method and current token authority.

If autonomous merge is permitted, perform it and verify it. Otherwise
report `BLOCKED_REQUIRES_HUMAN` with the exact policy blocker.

Never bypass protection.

## 64. GitHub API failure handling

Retry transient failures with bounded exponential/backoff. Distinguish
authentication/authorization, not-found/conflict/validation and
server/transient failures. Refresh state after conflicts. Never retry
authorization failures indefinitely.

## 65. Artifact retention

Retain final evidence, execution state, Q-version artifacts,
live-activity snapshots, test reports and security reports without
secrets. Canonical completion evidence belongs in the repository.

## 66. Operator documentation

Create/update concise documentation explaining:

``` text
Master Orchestrator
Autonomous Agent
Completion Engine
Git lifecycle
PR/merge lifecycle
Q.0.0.N
Live activity
Failure recovery
Resume
Success verification
```

Link it from README.

## 67. Monitoring dashboard

Provide a single operational index for:

``` text
Master Orchestrator
Ollama Agent
QMOI
qmoi-enhanced
Alpha-Q-ai
main
autosync-backup
PRs
checks
merge
Q-version
live activity
security
production readiness
```

## 68. Alerts

Alert on:

``` text
agent stale
orchestrator stale
repeated self-healing
security failure
permission failure
push failure
merge failure
cross-repo divergence
live-stream stale
Q-version collision
production-gate failure
```

## 69. Resource and timeout controls

Every stage needs a timeout, retry limit, heartbeat and cancellation
handling. Hung operations must not consume Actions indefinitely.

## 70. Graceful interruption

On cancellation:

1.  write checkpoint;
2.  publish cancellation event;
3.  record current stage;
4.  preserve evidence;
5.  leave repository in a safe known state;
6.  permit resume.

Never report success.

## 71. Git conflict recovery

For safe conflicts:

``` text
fetch
→ inspect divergence
→ determine safe strategy
→ resolve deterministically
→ validate
→ commit
→ push
→ verify
```

Ambiguous conflicts become `BLOCKED_REQUIRES_HUMAN`.

## 72. Failed-check recovery

On required-check failure:

``` text
fetch check details
→ classify
→ map to files
→ repair
→ commit
→ push
→ wait for new checks
```

Never merge with required checks failed/pending.

## 73. Failed-merge recovery

Refresh PR and branch state, determine the cause, repair if safe,
revalidate and retry. Never assume the PR remained unchanged.

## 74. Cross-repository divergence recovery

If unexpected divergence appears:

``` text
STOP CROSS_REPO_MUTATION
→ INSPECT BOTH
→ CLASSIFY DIFFERENCE
→ SYNC ONLY CONTRACTUAL PATHS
→ VALIDATE
```

Never overwrite unknown work automatically.

## 75. Live-stream failure behavior

Live activity is an observability subsystem, but if it is configured as
a required production gate, failure must block success until repaired
and verified.

Never corrupt repository state merely to make the stream green.

## 76. QMOI versus GitHub activity

A GitHub workflow heartbeat proves the workflow is running; it does not
prove QMOI model activity. Publish separate QMOI
process/model/memory/task events.

## 77. Ollama versus QMOI activity

Likewise distinguish:

``` text
OLLAMA_PROCESS
OLLAMA_MODEL
OLLAMA_INFERENCE
OLLAMA_AGENT
```

from QMOI events.

## 78. Event correlation

Use execution, parent-execution and correlation IDs so the complete
lifecycle can be reconstructed across both repositories and all streams.

## 79. Final end-to-end test

Create a controlled test proving:

``` text
start
→ discover
→ inspect
→ controlled modification
→ test
→ commit
→ push
→ remote SHA
→ PR
→ checks
→ merge
→ main verification
→ backup sync
→ second repository sync
→ Q.0.0.N
→ live streams
→ final evidence
→ SUCCESS
```

Also create no-change and failure/recovery scenarios.

## 80. Final acceptance test

An independent verifier must be able to answer YES to:

``` text
Can the agent inspect both repositories?
Can it determine required work?
Can it modify files?
Can it validate?
Can it self-heal?
Can it commit?
Can it push?
Can it verify the remote SHA?
Can it discover/update PRs?
Can it wait for checks?
Can it repair failed checks?
Can it merge when authorized?
Can it verify merge/main?
Can it synchronize autosync-backup?
Can it synchronize the other repository?
Can it verify both repositories?
Can it create Q.0.0.N?
Can Q.0.0.N prove completion?
Can it publish QMOI live activity?
Can it publish Ollama live activity?
Can it publish orchestrator activity?
Can it detect stale activity?
Can it resume?
Can it produce complete evidence?
Can it prove production readiness?
Can it avoid false success?
```

## 81. Final success contract

Use exactly:

``` text
SUCCESS
NO_CHANGES_REQUIRED
BLOCKED_REQUIRES_HUMAN
FAILED_AT_<STAGE>
```

## 82. Final evidence chain

The evidence chain must be:

``` text
local intended state
→ local validated state
→ local commit SHA
→ remote branch SHA
→ PR head SHA
→ merged SHA
→ remote main SHA
→ autosync-backup SHA
→ cross-repository state
→ Q.0.0.N
→ live activity evidence
→ final verification
→ SUCCESS
```

## 83. Repository-specific principle

The repositories share one autonomous completion contract, event schema,
Q-version semantics and verification model, but must retain
repository-specific code and documentation.

## 84. Preserve existing functionality

The repositories contain extensive platform validation, QMOI
functionality, Ollama automation, monitoring, tracking and
documentation. Do not remove these merely to simplify the architecture.
Discover, classify, integrate, consolidate, test and harden them.

## 85. Upgrade existing liveactivitystream.md

Treat the existing `liveactivitystream.md` files as canonical
user-facing specifications, but update them to match actual runtime
behavior. Document QMOI, Ollama and Master Orchestrator streams, event
schema, freshness, heartbeat, current state, workflows, artifacts,
endpoints, stale handling, troubleshooting and verification.

## 86. Live-stream proof requirement

Every production completion must record:

``` text
last_event_timestamp
last_heartbeat_timestamp
current_execution_id
current_stage
final_execution_status
```

with evidence references.

## 87. Q-version live-activity record

`Q.0.0.N/LIVE_ACTIVITY.md` must summarize QMOI, Ollama and Master
Orchestrator streams, event counts, first/last events, heartbeat, final
status and evidence locations.

## 88. Production verification independent of the LLM

The LLM may recommend readiness, but the deterministic completion engine
must independently verify readiness from GitHub/Git/test/security state.

## 89. No mock production evidence

Never generate fake SHAs, fake PRs, fake merges, fake heartbeat data,
fake URLs or fake test results. Missing evidence is unknown/failure.

## 90. No stale success artifacts

Every final status must be tied to the current execution ID, commit SHA,
Q-version and timestamp. A previous successful execution cannot make a
new run appear successful.

## 91. CURRENT_STATUS freshness

Current status must be updated atomically and generated from structured
state. A new run must replace the previous authoritative state.

## 92. Master Orchestrator final responsibility

The Master Orchestrator must remain responsible through:

``` text
dispatch
→ monitor
→ recover
→ verify
→ finalize
```

It must not exit merely after dispatching the agent.

## 93. Immutable terminal state

A completed execution should have a terminal record containing execution
ID, final status, Q-version and final main SHAs.

## 94. Rerunnable verification

Provide a read-only verifier conceptually equivalent to:

``` text
python scripts/autonomous_completion_engine.py verify --execution-id <id>
```

and suitable sub-verifiers for remote, live, Q-version and
cross-repository state.

## 95. Dry-run

Provide a non-mutating planning mode such as:

``` text
autonomous_complete --dry-run
```

It must never report production `SUCCESS`.

## 96. Audit mode

Provide a read-only audit mode such as:

``` text
autonomous_complete --audit
```

## 97. Repair mode

Provide a safe deterministic repair mode such as:

``` text
autonomous_complete --repair
```

## 98. Resume mode

Provide:

``` text
autonomous_complete --resume <execution-id>
```

## 99. Implementation sequence

Implement in this order:

``` text
A. Inventory and gap analysis
B. State machine and execution IDs
C. Checkpoint/resume
D. Deterministic Git/GitHub completion engine
E. PR/check/merge verification
F. Cross-repository synchronization
G. Q.0.0.N manager
H. Evidence/telemetry
I. QMOI/Ollama/orchestrator live streams
J. Security/production gates
K. Master Orchestrator integration
L. End-to-end tests
M. Failure injection
N. Documentation
O. Final remote verification
```

## 100. Required implementation checklist

``` text
[ ] Both repositories inspected
[ ] All Ollama files inspected
[ ] Master Orchestrator inspected
[ ] Merge/sync inspected
[ ] Live activity inspected
[ ] Tracking inspected
[ ] Tests inspected
[ ] Gap matrix created
[ ] Completion engine implemented
[ ] State machine implemented
[ ] Checkpoint/resume implemented
[ ] Self-healing implemented
[ ] Commit verification implemented
[ ] Push verification implemented
[ ] Remote SHA verification implemented
[ ] PR lifecycle implemented
[ ] Check monitoring implemented
[ ] Merge lifecycle implemented
[ ] Merge verification implemented
[ ] main verification implemented
[ ] autosync-backup verification implemented
[ ] Cross-repository synchronization implemented
[ ] Q.0.0.N manager implemented
[ ] Q.0.0.N evidence implemented
[ ] QMOI live stream fixed
[ ] Ollama live stream fixed
[ ] Master Orchestrator stream implemented
[ ] Heartbeats implemented
[ ] Stale detection implemented
[ ] Current-state implementation implemented
[ ] Event schema implemented
[ ] Security gates implemented
[ ] Production gates implemented
[ ] Green-wrapper success eliminated
[ ] Failure-injection tests implemented
[ ] End-to-end tests implemented
[ ] Documentation updated
[ ] Workflow permissions reviewed
[ ] Final remote verification implemented
[ ] Both repositories verified
```

## 101. Final success ceremony

Only after every applicable gate passes:

``` text
1. Generate final evidence.
2. Generate Q.0.0.N.
3. Commit Q-version evidence.
4. Push.
5. Verify remote SHA.
6. Verify main.
7. Verify autosync-backup.
8. Verify both repositories.
9. Verify live activity.
10. Verify production readiness.
11. Write immutable terminal execution state.
12. Publish SUCCESS.
```

The final success declaration must be the last operation, not an early
workflow step.

## 102. Expected successful lifecycle

``` text
MASTER ORCHESTRATOR
→ DISCOVER
→ INSPECT
→ PLAN
→ OLLAMA AGENT
→ MODIFY
→ TEST
→ SECURITY
→ SELF-HEAL IF NEEDED
→ COMMIT
→ PUSH
→ REMOTE VERIFY
→ PR
→ CHECKS
→ MERGE
→ MERGE VERIFY
→ MAIN VERIFY
→ AUTOSYNC-BACKUP
→ CROSS-REPOSITORY SYNC
→ Q.0.0.N
→ QMOI LIVE STREAM
→ OLLAMA LIVE STREAM
→ MASTER ORCHESTRATOR STREAM
→ FINAL PRODUCTION VERIFICATION
→ FINAL REMOTE VERIFICATION
→ EVIDENCE
→ SUCCESS
```

## 103. Definition of done

This initiative is complete only when:

-   both repositories contain the autonomous completion architecture;
-   the Master Orchestrator supervises the entire lifecycle;
-   ordinary repository work can complete without manual intervention;
-   commits and pushes are real and verified;
-   PR/check/merge operations are real and verified;
-   `main` and `autosync-backup` are verified;
-   cross-repository synchronization is verified;
-   `Q.0.0.N` exists in both repositories;
-   Q.0.0.N proves completion;
-   self-healing and stale recovery are operational;
-   production readiness is a hard gate;
-   green-wrapper success is eliminated;
-   QMOI live activity works;
-   Ollama autonomous-agent live activity works;
-   Master Orchestrator activity is visible;
-   heartbeats/freshness/stale detection work;
-   all final evidence is tied to the current execution;
-   end-to-end and failure-injection tests pass;
-   security validation passes;
-   final remote repository state is independently verified.

Only then:

``` text
Q.0.0.N
FINAL_STATUS=SUCCESS
PRODUCTION_READY=true
```

## 104. Final instruction to Copilot Chat/Agent

**Do not treat this document as a request for another plan. Treat it as
the implementation contract.**

Inspect the actual current state of both repositories first. Implement
every applicable requirement. Reuse and harden working components. Do
not silently omit anything because a Markdown file claims it already
works.

If a feature is documented but not implemented, implement it. If
implemented but not wired into the autonomous path, wire it in. If
partially implemented, complete it. If duplicated/conflicting,
consolidate it and add regression tests.

Continue through validation and autonomous repair until all safe work is
complete.

Finally, independently verify both remote repositories, their branches,
PR/merge state, Q.0.0.N artifacts, live QMOI/Ollama/orchestrator
activity and production-readiness gates.

**The objective is not a green workflow. The objective is a demonstrably
updated, synchronized, production-ready `qmoi-enhanced` and
`Alpha-Q-ai`, with a verified `Q.0.0.N` completion record and genuinely
working QMOI + Ollama + Master Orchestrator live activity streams.**


## 105. Bidirectional workspace/repository architecture

The two repositories must become **symmetrical development peers**:

```text
Alpha-Q-ai Codespace
      │
      ├── local work
      │
      └── QMOI Workspace Sync Broker
               │
               ├── qmoi-enhanced target
               └── Alpha-Q-ai source

qmoi-enhanced Codespace
      │
      ├── local work
      │
      └── QMOI Workspace Sync Broker
               │
               ├── Alpha-Q-ai target
               └── qmoi-enhanced source
```

The user must be able to work primarily inside either repository's Codespace without manually running `git pull`, `git fetch`, `git push`, branch synchronization, remote PR or merge commands.

The automation must make the **repository being edited and the repository being updated explicit**, never infer the destination from the current directory alone.

## 106. Workspace should be a control surface, not the Git transport

The Codespace should not be responsible for manually executing the complete GitHub lifecycle.

Instead:

```text
Codespace edit
→ workspace agent detects change
→ sync request
→ GitHub automation
→ target-repository workflow
→ target branch/PR
→ checks
→ merge when authorized
→ remote verification
→ workspace state refresh
```

The workspace can use Git internally for detecting local modifications, but the user should not need to type Git lifecycle commands.

## 107. Two-way repository bridge

Create a shared cross-repository bridge with equivalent configuration in both repositories:

```text
scripts/
├── workspace_sync.py
├── cross_repo_sync.py
├── remote_state.py
└── sync_contract.py

.github/workflows/
├── workspace-sync.yml
├── cross-repository-sync.yml
└── remote-update.yml
```

Both repositories must understand:

```text
SOURCE_REPOSITORY
TARGET_REPOSITORY
SOURCE_WORKSPACE
SOURCE_REF
SOURCE_COMMIT
TARGET_REF
SYNC_ID
EXECUTION_ID
REQUESTED_FILES
REQUEST_TYPE
```

## 108. Alpha-Q-ai Codespace → qmoi-enhanced

A user working inside `Alpha-Q-ai` must be able to request:

```text
Update qmoi-enhanced with my intended changes.
```

The automation must:

1. inspect the Alpha working state;
2. identify the intended change set;
3. create a sync request;
4. authenticate against GitHub;
5. transfer the change set securely;
6. create/update a target branch in `qmoi-enhanced`;
7. run target validation;
8. create/update the target PR;
9. wait for required checks;
10. self-heal safe failures;
11. merge when policy allows;
12. verify `qmoi-enhanced/main`;
13. synchronize `autosync-backup`;
14. report the final SHA back to Alpha;
15. refresh local remote metadata automatically.

The user must not need to manually push Alpha or pull qmoi-enhanced.

## 109. qmoi-enhanced Codespace → Alpha-Q-ai

The inverse path must work identically:

```text
qmoi-enhanced Codespace
→ workspace sync broker
→ Alpha-Q-ai target workflow
→ target branch
→ validation
→ PR
→ checks
→ merge
→ Alpha-Q-ai/main verification
→ autosync-backup
→ result returned
```

No asymmetric "Alpha can update QMOI but QMOI cannot update Alpha" implementation is acceptable.

## 110. Automatic source publication

A fundamental problem must be solved explicitly:

A GitHub-hosted workflow cannot see arbitrary uncommitted files that exist only inside a Codespace.

Therefore the workspace bridge must have a deterministic **source publication mechanism**.

Supported modes:

```text
MODE A: automatic source commit
MODE B: automatic patch bundle
MODE C: automatic changed-file upload
```

The default should be `MODE A` where safe.

The user edits files normally; the bridge detects the change and publishes the source state through GitHub APIs or an authenticated temporary branch without requiring the user to manually execute `git push`.

## 111. Automatic source commit

When the user requests a cross-repository update:

```text
workspace changes
→ validation
→ generated source commit
→ remote source branch
→ target synchronization
```

The generated commit must identify:

```text
workspace_sync_id
execution_id
source_repo
source_branch
source_sha
target_repo
target_branch
```

Do not silently commit unrelated user work.

## 112. Automatic patch mode

If automatic source commits are disabled, generate a signed/validated patch bundle containing:

```text
changed paths
file modes
renames
deletions
binary-file handling
base SHA
source SHA
checksums
manifest
```

The target workflow must reject patches whose base SHA does not match the expected source state.

## 113. Workspace intent boundaries

The automation must never assume that every local modification should be synchronized.

Use:

```text
SYNC_INCLUDE
SYNC_EXCLUDE
SYNC_REPOSITORY
SYNC_SCOPE
```

with safe defaults excluding:

```text
secrets
.env
credentials
tokens
private keys
local caches
virtual environments
generated temporary files
large unrelated artifacts
```

## 114. Automatic local synchronization

After the remote target has been updated, the workspace should automatically refresh its view through the development environment integration.

The user experience should be:

```text
"Changes synchronized."
"qmoi-enhanced main: <verified SHA>"
"Alpha-Q-ai main: <verified SHA>"
```

rather than requiring manual `pull`.

If local uncommitted work would be overwritten, the system must preserve it and stop the destructive refresh.

## 115. Never use blind force-push

Cross-repository automation must never use:

```text
git push --force
git reset --hard
git clean -fd
```

against a user's active workspace or protected production branch merely to resolve synchronization.

Conflicts must be classified and handled through a safe branch/PR workflow.

## 116. Cross-repository synchronization contract

Define one machine-readable contract:

```yaml
sync_id: ...
execution_id: ...
source:
  repository: thealphakenya/Alpha-Q-ai
  ref: ...
  sha: ...
target:
  repository: thealphakenya/qmoi-enhanced
  ref: ...
  base_sha: ...
scope:
  paths: []
policy:
  create_pr: true
  auto_merge: true
  require_checks: true
  require_remote_verification: true
```

The inverse configuration must be equally valid.

## 117. GitHub Actions authentication architecture

Do **not** attempt to solve cross-repository 403 errors by blindly increasing `GITHUB_TOKEN` permissions.

GitHub documents that `GITHUB_TOKEN` permissions are repository/workflow-scoped and that unspecified permissions become `none` when permissions are explicitly configured. citeturn0search0

Therefore implement two distinct authentication paths:

```text
CURRENT-REPOSITORY OPERATIONS
→ repository GITHUB_TOKEN

CROSS-REPOSITORY OPERATIONS
→ dedicated GitHub App installation token
   OR appropriately scoped fine-grained credential
```

Record the current identity and capability boundary as evidence: the
`thealphakenya` account owns both coordinated repositories, while the current
Codespace session is `thevictorkenya` with repository push access. A Codespaces
`GITHUB_TOKEN` with repository push access is not proof of Actions dispatch or
protected-branch administration. The preflight must test the exact operation
and preserve `AUTH_BLOCKED` on a 403.

## 118. Prefer GitHub App authentication for cross-repository automation

Create a dedicated GitHub App/service identity for the two repositories where practical.

Grant only the permissions actually required for:

```text
contents
pull requests
actions/checks
metadata
```

and any additional permission proven necessary.

The App installation must be authorized for **both**:

```text
thealphakenya/Alpha-Q-ai
thealphakenya/qmoi-enhanced
```

The resulting installation token should be short-lived and generated only when required.

This is preferable to embedding a long-lived personal credential throughout both workspaces.

## 119. Fine-grained credential fallback

If a GitHub App is not practical, use a fine-grained token restricted to:

```text
Owner: thealphakenya
Repositories:
  Alpha-Q-ai
  qmoi-enhanced
```

Grant only the required repository permissions.

GitHub's current documentation confirms that fine-grained tokens support repository-specific permissions and that `write` includes `read` for a permission. citeturn0search10

Never use a broad token merely because it makes setup easier.

## 120. Separate credential roles

Do not use one credential for everything.

Define:

```text
LOCAL_WORKSPACE_SYNC_CREDENTIAL
CROSS_REPO_DISPATCH_CREDENTIAL
TARGET_REPOSITORY_WORKFLOW_CREDENTIAL
ADMINISTRATION_CREDENTIAL
```

The ordinary target workflow should use its own `GITHUB_TOKEN` for operations inside that target repository whenever possible.

## 121. Cross-repository dispatch

Use GitHub `repository_dispatch` or an equivalent authenticated API mechanism to notify the target repository.

GitHub's API documentation confirms that workflow dispatch can require Actions write permission, while cross-repository dispatch requires appropriate authorization on the target repository. citeturn0search2

The implementation must test the exact API path being used rather than assuming one permission model applies to every operation.

For same-repository workflow chaining, use the repository-managed
`MY_CUSTOM_TOKEN` first and `github.token` only as a validated fallback. The
dispatching workflow must record the target run ID, target SHA, endpoint,
credential role without the secret, and terminal conclusion. A successful API
response that never yields a successful target run is not completion.

## 122. Do not rely on the source repository's GITHUB_TOKEN for target writes

A source workflow's ordinary `GITHUB_TOKEN` should not be assumed to have write authority over the other repository.

The target workflow should perform target-repository writes using its own repository-scoped token where possible, after receiving a validated dispatch/request.

This prevents the common architecture:

```text
Alpha GITHUB_TOKEN
→ attempt qmoi-enhanced push
→ 403
```

and replaces it with:

```text
Alpha
→ authenticated request
→ qmoi-enhanced workflow
→ qmoi-enhanced GITHUB_TOKEN
→ qmoi-enhanced branch/PR
```

## 123. 403 prevention preflight

Before attempting any cross-repository mutation, run a deterministic authorization preflight:

```text
credential available?
credential valid?
source repository accessible?
target repository accessible?
target contents write?
target Actions permission?
PR permission?
required workflow permission?
branch protection compatible?
```

Return:

```text
AUTH_READY
AUTH_BLOCKED
```

The preflight must run separately for both repositories and cover identity,
repository access, workflow visibility, workflow dispatch, Actions permission,
contents write, pull-request write, checks read, branch-rule compatibility,
and artifact access. The known secret name is `MY_CUSTOM_TOKEN`; only GitHub
Actions may resolve its value. Codespace tooling must never attempt to read or
echo that secret.

before beginning mutation.

A known 403 must never be discovered only after a destructive workflow has started.

## 124. 403 diagnostics

Every authorization failure must record:

```text
HTTP status
GitHub endpoint
operation
source repository
target repository
credential role
required permission
actual operation
remediation
```

Never expose token values.

## 125. 403 self-healing boundary

Self-healing may:

- refresh an expired App installation token;
- retry transient GitHub API failures;
- refresh repository state;
- select the correct authenticated endpoint;
- retry after a permission propagation delay.

Self-healing must **not**:

- invent credentials;
- print secrets;
- escalate permissions automatically;
- bypass branch protection;
- disable security controls.

A genuine missing permission becomes:

```text
BLOCKED_REQUIRES_HUMAN
```

with an exact remediation.

## 126. Repository Actions permission gate

Both repositories must have workflow permissions explicitly reviewed.

Where a workflow needs repository writes, specify the minimum required permissions, for example:

```yaml
permissions:
  contents: write
  pull-requests: write
```

Additional permissions must be justified by an actual operation.

GitHub states that repository/organization defaults can restrict `GITHUB_TOKEN`, while a workflow can request appropriate permissions in its YAML. citeturn0search0turn0search7

## 127. Cross-repository permission matrix

Create:

```text
CROSS_REPO_PERMISSION_MATRIX.md
```

with rows for:

```text
operation
source
target
credential
required permission
workflow
expected HTTP result
verification
```

At minimum cover:

```text
dispatch
branch creation
contents write
PR creation
PR update
checks read
merge
branch synchronization
workflow dispatch
artifact access
```

The matrix must include both directions (`Alpha-Q-ai -> qmoi-enhanced` and
`qmoi-enhanced -> Alpha-Q-ai`) and distinguish repository push access from
Actions dispatch and protected-branch administration. Repository push alone
must remain insufficient for `AUTH_READY`.

## 128. Automated permission verification

Add a safe diagnostic workflow:

```text
cross-repo-auth-preflight.yml
```

It must test authorization without modifying production branches.

It should produce:

```text
Alpha → QMOI: PASS/BLOCKED
QMOI → Alpha: PASS/BLOCKED
```

## 129. Workspace bootstrap

Both repositories' Codespaces should install the same lightweight synchronization interface.

For example:

```text
qmoictl sync alpha
qmoictl sync qmoi
qmoictl sync both
qmoictl status
qmoictl verify
qmoictl resume
```

The commands are convenience interfaces; the user should not need to know the underlying Git/API mechanics.

## 130. Automatic background synchronization

Where Codespace lifecycle permits, provide an opt-in background watcher:

```text
file change
→ debounce
→ determine scope
→ validate
→ synchronize
```

Use conservative debounce intervals and do not commit every keystroke.

Default behavior should batch changes.

## 131. Explicit synchronization modes

Support:

```text
manual-request
auto-on-save
auto-on-checkpoint
auto-on-agent-completion
scheduled
```

Production synchronization should default to `auto-on-agent-completion` rather than every keystroke.

## 132. Workspace status dashboard

Both Codespaces should expose:

```text
Current repository
Current branch
Local modification state
Remote SHA
Target repository
Target SHA
Sync state
Execution ID
PR
Checks
Merge
Q-version
Live activity
403/auth state
```

## 133. Remote-first development model

The authoritative state after synchronization must be GitHub remote state.

The workspace is a development surface.

Therefore:

```text
workspace ≠ source of truth
remote repository = source of truth
completion evidence = proof of truth
```

## 134. Bidirectional synchronization graph

Represent the relationship as:

```text
Alpha-Q-ai/main
       ↕
cross-repo contract
       ↕
qmoi-enhanced/main

Alpha-Q-ai/autosync-backup
       ↕
backup synchronization contract
       ↕
qmoi-enhanced/autosync-backup
```

Do not assume the repositories should always have identical full trees. Synchronize according to ownership and declared shared paths.

## 135. Shared-path ownership

Create:

```text
CROSS_REPO_OWNERSHIP.yml
```

classifying paths as:

```text
ALPHA_ONLY
QMOI_ONLY
SHARED
GENERATED
SYNCED_EVIDENCE
SYNCED_AUTOMATION
```

Only `SHARED`, `SYNCED_EVIDENCE` and explicitly approved `SYNCED_AUTOMATION` paths are eligible for automatic cross-repository replication.

## 136. Avoid repository contamination

Do not automatically copy repository-specific:

```text
application code
deployment secrets
environment configuration
local paths
repository-specific generated state
```

unless ownership rules explicitly allow it.

This is especially important because Alpha-Q-ai currently documents extensive historical/materialized merge inputs and cross-repository planning. citeturn2view0turn2view1

## 137. Preserve the existing merge inventory contract

The existing Alpha merge contract already requires complete inventory, source ownership, conflict classification, validation and explicit evidence. The new cross-repository bridge must call into that machinery rather than bypassing it. citeturn2view1

## 138. Codespace light/full/audit modes

Preserve the existing Codespaces model in Alpha-Q-ai:

```text
light
full
audit
```

The cross-repository automation must automatically switch to an appropriate full/audit materialization when a synchronization operation genuinely requires complete source coverage.

The user should not have to manually prepare the Codespace.

## 139. Automatic sibling-repository materialization

If the user is in:

```text
/workspaces/Alpha-Q-ai
```

the automation may automatically materialize:

```text
/workspaces/qmoi-enhanced
```

when required.

If the user is in:

```text
/workspaces/qmoi-enhanced
```

it may automatically materialize:

```text
/workspaces/Alpha-Q-ai
```

when required.

Do not duplicate enormous histories unnecessarily; use sparse/blobless/full-history modes appropriate to the operation.

## 140. One workspace, two repository control plane

Provide an optional shared control directory outside either repository, conceptually:

```text
/workspaces/.qmoicontrol/
```

containing:

```text
config
execution state
sync queue
credentials metadata
locks
temporary patches
```

Never store raw secrets there.

## 141. Avoid nested Git repository mistakes

If sibling repositories are materialized:

```text
/workspaces/Alpha-Q-ai
/workspaces/qmoi-enhanced
```

keep them as independent repositories.

Never accidentally initialize one as a Git submodule or place one repository inside the tracked tree of the other.

## 142. Automatic remote tracking

The workspace helper should maintain remote metadata:

```text
origin
source remote
target remote
main
autosync-backup
current verified SHA
last synchronization ID
```

It should repair stale metadata without changing repository content.

## 143. Automatic branch synchronization

Implement:

```text
sync_main
sync_autosync_backup
sync_feature_branch
sync_cross_repository
```

with the same state-machine/evidence contract used by the autonomous agent.

## 144. Branch sync must be direction-aware

Never blindly synchronize:

```text
A → B
```

without identifying:

```text
source SHA
target SHA
common ancestor
ahead/behind
divergence
protected status
```

## 145. Branch divergence gate

If:

```text
A ahead, B behind
```

the system may synchronize safely.

If:

```text
A and B diverged
```

it must inspect the divergence before selecting merge/rebase/cherry-pick strategy.

## 146. Autosync-backup relationship

`autosync-backup` must remain a recoverable backup/synchronization branch, not a second uncontrolled development main.

Record:

```text
main_sha
backup_sha
relationship
last_sync_execution
```

## 147. Automatic backup synchronization

After verified `main` completion:

```text
main
→ autosync-backup
→ remote verification
```

If backup synchronization fails, final production success must remain blocked when backup sync is a required contract.

## 148. Cross-repository backup synchronization

The pair must maintain:

```text
Alpha main
Alpha autosync-backup
QMOI main
QMOI autosync-backup
```

and record all four SHAs in final evidence.

## 149. Automatic PR origin tracking

Every cross-repository PR must contain machine-readable metadata:

```text
sync_id
execution_id
source_repo
source_sha
target_repo
target_base_sha
q_version
```

The PR body should link to the completion evidence.

## 150. PR deduplication

Before creating a PR:

```text
search existing PR
→ compare source SHA
→ compare target
→ compare sync ID
```

Update an existing compatible PR instead of creating duplicates.

## 151. Merge queue/race protection

If another automation run modifies the target branch:

```text
refresh
→ compare expected SHA
→ recalculate
→ continue only if safe
```

Never merge based on stale SHA assumptions.

## 152. Source/target SHA proof

A cross-repository synchronization record must prove:

```text
source working state
→ source published SHA
→ target received source SHA
→ target branch SHA
→ merged SHA
→ target main SHA
```

## 153. Automatic workspace result callback

After target completion, publish a structured result back to the originating repository:

```json
{
  "sync_id": "...",
  "source_repository": "...",
  "target_repository": "...",
  "source_sha": "...",
  "target_sha": "...",
  "pr_number": 0,
  "merge_sha": "...",
  "q_version": "...",
  "status": "SUCCESS"
}
```

The originating workspace monitor consumes this event automatically.

## 154. Cross-repository event stream

Extend live activity with:

```text
CROSS_REPO_SYNC_REQUESTED
SOURCE_PUBLISHED
TARGET_DISPATCHED
TARGET_RECEIVED
TARGET_VALIDATION
TARGET_PR
TARGET_CHECKS
TARGET_MERGE
TARGET_VERIFIED
CALLBACK_PUBLISHED
WORKSPACE_REFRESHED
```

## 155. 403 visibility in live activity

When an authorization problem occurs, show:

```text
AUTH_FAILURE
operation
source
target
required permission
credential role
recovery state
```

Never show token contents.

## 156. Cross-repository health endpoint/state

Expose machine-readable health:

```text
alpha_to_qmoi
qmoi_to_alpha
auth
dispatch
target_workflow
target_write
pr
merge
verification
```

## 157. Cross-repository health gate

Production readiness requires:

```text
Alpha → QMOI path verified
AND
QMOI → Alpha path verified
```

unless a documented deployment mode intentionally disables one direction.

## 158. End-to-end Alpha → QMOI test

Create a disposable test branch and prove:

```text
Alpha workspace change
→ automatic source publication
→ QMOI synchronization
→ QMOI PR
→ checks
→ merge
→ QMOI main SHA
→ callback
→ Alpha evidence
```

No manual push/pull command should be required.

## 159. End-to-end QMOI → Alpha test

Perform the exact inverse test.

The test must prove the architecture is truly bidirectional.

## 160. No-manual-Git acceptance criterion

The feature is not complete if the documented procedure still requires the user to manually type:

```text
git add
git commit
git pull
git fetch
git push
git checkout
git merge
```

for ordinary cross-repository synchronization.

The automation may execute Git operations internally in controlled workflows; the requirement is that the user does not have to manually perform the lifecycle.

## 161. User safety gate

Before automatic publication, detect:

```text
uncommitted unrelated changes
unstaged deletions
conflicting local branch state
untracked sensitive files
```

Pause safely when necessary.

## 162. Secret-safe synchronization

The cross-repository bridge must scan all outbound changes for:

```text
GitHub tokens
PATs
private keys
cloud credentials
API keys
database credentials
`.env` values
```

and block publication.

## 163. Existing `.env.example` and historical-secret audit

Because both repositories contain extensive automation and configuration documentation, perform a dedicated historical secret scan before enabling unattended cross-repository publication.

A historical credential leak cannot be considered fixed merely because the current tree no longer contains the value.

## 164. Token rotation proof

If a historical token is found:

```text
detect
→ revoke/rotate
→ remove
→ rewrite affected files
→ scan history
→ verify current state
```

Do not print the secret.

## 165. GitHub App token lifecycle

For an App-based implementation:

```text
request installation token
→ validate installation
→ use token
→ discard token
```

Do not persist the short-lived token in repository files.

## 166. Credential fallback order

Recommended:

```text
1. GitHub App installation token
2. GitHub Actions GITHUB_TOKEN for same-repository operations
3. Fine-grained PAT as controlled fallback
4. No anonymous mutation
```

Never silently fall back to a credential with broader privileges.

## 167. Permission configuration documentation

Add:

```text
CROSS_REPO_AUTH_SETUP.md
CROSS_REPO_PERMISSION_MATRIX.md
CODESPACE_SYNC.md
```

to both repositories.

These documents must explain exact setup, required GitHub settings, credential locations and verification commands/UI paths without exposing secrets.

## 168. GitHub Actions settings verification

Verify repository Actions settings allow the required workflow behavior.

GitHub provides repository-level controls for default workflow permissions and Actions policy, and changing these settings itself requires repository administration authority. citeturn0search7

The automation must detect insufficient administration authority rather than claiming it fixed the setting.

## 169. Protected branch compatibility

Cross-repository automation must respect branch protection/rulesets.

If `main` requires PRs/checks/reviews, automation must create the PR and satisfy those rules rather than trying to push directly.

## 170. Direct push only where permitted

Direct push may be used only for explicitly permitted automation branches such as an agent feature branch or designated backup branch.

`main` must follow repository policy.

## 171. Remote workflow dispatch fallback

If direct cross-repository API dispatch fails but a safe GitHub-native trigger is available, the orchestrator may use the documented fallback.

Every fallback must still use authenticated authorization and must be recorded.

## 172. No 403 masking

A 403 must never be converted into:

```text
SUCCESS
WAITING
NO_CHANGES_REQUIRED
```

It must remain:

```text
AUTH_BLOCKED
```

until the required authorization is actually available.

## 173. Permission propagation handling

If GitHub configuration was just changed, use a bounded retry window for propagation.

After the window expires:

```text
BLOCKED_REQUIRES_HUMAN
```

with exact state.

## 174. Cross-repository operation lock

Use a distributed operation identity:

```text
sync_id
```

and prevent two runs from simultaneously updating the same target branch.

## 175. Idempotent cross-repository request

If the same `sync_id` is received twice:

```text
do not duplicate
→ retrieve existing result
→ return existing status
```

## 176. Cross-repository queue

When a target is busy:

```text
QUEUED
→ WAITING
→ RUNNING
```

rather than launching competing mutations.

## 177. Cross-repository cancellation

Support safe cancellation:

```text
REQUESTED
→ CANCELLING
→ CHECKPOINTED
→ CANCELLED
```

Never leave an ambiguous half-completed synchronization marked successful.

## 178. Automatic recovery from Codespace shutdown

The cross-repository operation must survive Codespace termination after the request has been published.

The authoritative execution must continue in GitHub Actions.

## 179. Workspace-independent completion

After the request is accepted by GitHub, the Codespace may disappear. The remote orchestrator must still be capable of completing:

```text
validation
PR
checks
merge
sync
Q-version
evidence
```

## 180. Reconnect behavior

When the user opens either repository again, the workspace bootstrap should discover unfinished remote executions and display:

```text
execution
stage
target
status
last heartbeat
next action
```

without requiring manual Git recovery.

## 181. Automatic remote-state refresh

On Codespace startup:

```text
query remote state
→ compare local state
→ preserve local modifications
→ refresh safe metadata
→ expose synchronization status
```

## 182. No automatic destructive checkout

The workspace must never automatically change branches or discard changes simply because remote `main` advanced.

## 183. Conflict UX

When local and remote changes conflict, expose:

```text
LOCAL_ONLY
REMOTE_ONLY
BOTH_CHANGED
CONFLICT
```

and let the deterministic merge system create a safe branch/PR rather than destroying local work.

## 184. Cross-repository dry run

Provide:

```text
qmoictl sync --source Alpha-Q-ai --target qmoi-enhanced --dry-run
```

showing:

```text
source changes
target base
planned files
permissions
PR plan
checks
merge policy
```

No mutation.

## 185. Cross-repository audit

Provide:

```text
qmoictl sync audit
```

showing current:

```text
SHAs
branches
permissions
PRs
divergence
autosync
Q-version
live activity
```

## 186. Cross-repository verification

Provide:

```text
qmoictl sync verify
```

which independently verifies both directions.

## 187. Synchronization evidence

Each sync must generate:

```text
SYNC.md
sync.json
source-state.json
target-state.json
authorization.json
verification.json
```

under the corresponding execution/Q-version evidence.

## 188. Cross-repository Q-version

A successful bidirectional synchronization must be incorporated into the same `Q.0.0.N` completion record.

The Q-version must explicitly state:

```text
Alpha-Q-ai source state
qmoi-enhanced source state
Alpha-Q-ai target state
qmoi-enhanced target state
cross-repo direction
sync ID
```

## 189. Cross-repository live stream

The live stream must show both directions:

```text
Alpha → QMOI
QMOI → Alpha
```

with no ambiguity about source and destination.

## 190. Workspace UI completion indicator

The Codespace monitor should show:

```text
SYNC: HEALTHY
AUTH: READY
ALPHA → QMOI: READY
QMOI → ALPHA: READY
LAST SYNC: ...
LAST VERIFIED SHA: ...
```

## 191. Permission test matrix

Automate tests for:

```text
valid App token
expired App token
wrong repository
missing contents write
missing PR write
missing Actions permission
protected main
stale branch
duplicate request
```

Every test must produce the expected state.

## 192. 403 regression test

Add a regression test specifically proving that the previous cross-repository 403 failure mode is detected during preflight rather than after partial execution.

## 193. Remote-write regression test

Prove that a target repository can receive a legitimate update through its own authorized workflow and produce a verifiable remote SHA.

## 194. Bidirectional regression test

Prove:

```text
Alpha → QMOI
```

and:

```text
QMOI → Alpha
```

using disposable branches.

## 195. Autosync regression test

Prove that after target `main` verification:

```text
target main
→ target autosync-backup
→ remote backup SHA verified
```

## 196. Cross-repository branch-sync regression test

Prove that branch synchronization handles:

```text
ahead
behind
diverged
identical
missing
protected
```

without destructive behavior.

## 197. Merge regression test

Prove that the cross-repository system cannot mark success when:

```text
PR open
checks pending
checks failed
merge failed
main unchanged
```

## 198. Final bidirectional invariant

The ultimate cross-repository invariant is:

```text
A workspace can initiate a verified update to B
AND
B workspace can initiate a verified update to A
AND
neither operation requires the user to manually perform Git lifecycle commands
AND
both operations respect GitHub authorization and branch protection
AND
both operations produce independently verifiable remote evidence.
```

## 199. Final cross-repository success contract

For Alpha → QMOI:

```text
AUTH_READY
AND SOURCE_STATE_PUBLISHED
AND TARGET_RECEIVED
AND TARGET_VALIDATED
AND PR_VERIFIED
AND CHECKS_VERIFIED
AND MERGE_VERIFIED
AND TARGET_MAIN_VERIFIED
AND TARGET_BACKUP_VERIFIED
AND CALLBACK_VERIFIED
```

For QMOI → Alpha, use the exact inverse.

## 200. Final architecture objective

The finished system should make these two workflows operationally equivalent:

```text
┌──────────────────────┐
│ Alpha-Q-ai Codespace │
└──────────┬───────────┘
           │ edit
           ↓
   Workspace Sync Broker
           │
           ↓
   GitHub Authenticated API
           │
           ↓
 ┌───────────────────────┐
 │ qmoi-enhanced Actions │
 └──────────┬────────────┘
            ↓
      validate → PR → checks
            ↓
          merge
            ↓
      verify main/back-up
            ↓
      Q.0.0.N + live stream
```

and:

```text
┌────────────────────────┐
│ qmoi-enhanced Codespace│
└───────────┬────────────┘
            │ edit
            ↓
    Workspace Sync Broker
            │
            ↓
    GitHub Authenticated API
            │
            ↓
 ┌─────────────────────────┐
 │ Alpha-Q-ai Actions      │
 └───────────┬─────────────┘
             ↓
       validate → PR → checks
             ↓
           merge
             ↓
       verify main/back-up
             ↓
       Q.0.0.N + live stream
```

The user-facing experience should therefore be **repository-independent**: work from whichever Codespace is convenient, request/allow synchronization, and let the remote autonomous system perform the authenticated GitHub lifecycle.

## 201. Additional required files

Add or update these in **both** repositories where appropriate:

```text
CROSS_REPO_AUTH_SETUP.md
CROSS_REPO_PERMISSION_MATRIX.md
CROSS_REPO_SYNC.md
CODESPACE_SYNC.md
WORKSPACE_AUTOSYNC.md
BRANCH_SYNC.md
AUTONOMOUS_GIT_LIFECYCLE.md
```

Do not create redundant documents if an existing canonical document can be extended.

## 202. Additional required implementation components

Where existing equivalents do not already exist, implement:

```text
scripts/workspace_sync.py
scripts/cross_repo_sync.py
scripts/sync_contract.py
scripts/remote_state.py
scripts/auth_preflight.py
scripts/qmoictl.py

.github/workflows/workspace-sync.yml
.github/workflows/cross-repository-sync.yml
.github/workflows/cross-repo-auth-preflight.yml
```

Integrate with existing architecture rather than duplicating existing functionality.

## 203. Final Copilot instruction for this extension

When implementing topics 105–202:

1. Inspect the actual current implementation first.
2. Locate existing autosync, branch-sync, merge and Codespace scripts.
3. Locate existing Alpha/QMOI merge inventory mechanisms.
4. Locate current authentication and GitHub API code.
5. Identify exactly where the historical HTTP 403 occurs.
6. Replace the fragile cross-repository write path with the authenticated target-workflow architecture.
7. Preserve the existing merge/audit evidence contract.
8. Implement bidirectional operation.
9. Test Alpha → QMOI.
10. Test QMOI → Alpha.
11. Test autosync in both directions.
12. Test branch synchronization.
13. Test authorization preflight.
14. Test deliberate 403 scenarios.
15. Test protected-branch behavior.
16. Test Codespace shutdown/resume.
17. Test live activity.
18. Test Q.0.0.N evidence.
19. Run the complete production gate.
20. Verify the final remote SHAs.
21. Do not claim success until both directions have real evidence.

## 204. Final no-manual-command invariant

The completed system must allow the user to remain in either repository's Codespace and work normally while the automation handles the remote lifecycle.

The user should **not have to manually execute**:

```text
pull
fetch
push
branch synchronization
PR creation
PR merge
autosync
cross-repository synchronization
```

for ordinary supported operations.

The system may execute these operations internally through controlled GitHub Actions/API mechanisms; the important invariant is that the user does not have to manually perform them.

## 205. Final authorization invariant

A successful cross-repository update must never depend on a token that merely happens to work in one repository.

The credential architecture must explicitly prove:

```text
who
→ can access
→ which repository
→ for which operation
→ with which permission
→ for how long
```

and preflight it before mutation.

## 206. Final 403 invariant

The target repository must perform its own authorized repository writes wherever possible.

Therefore the intended architecture is:

```text
source workspace
→ authenticated request
→ target repository workflow
→ target GITHUB_TOKEN
→ target branch/PR
→ target checks
→ target merge
```

rather than:

```text
source workspace
→ source GITHUB_TOKEN
→ target repository push
→ HTTP 403
```

This is the key architectural correction for the cross-repository permission problem.

## 207. Final two-repository production invariant

The complete QMOI platform is production-ready only when all of the following are true:

```text
Alpha-Q-ai autonomous lifecycle PASS
qmoi-enhanced autonomous lifecycle PASS

Alpha → QMOI synchronization PASS
QMOI → Alpha synchronization PASS

Alpha main verified
Alpha autosync-backup verified

QMOI main verified
QMOI autosync-backup verified

Cross-repository authorization PASS
Branch synchronization PASS
PR/merge lifecycle PASS
Q.0.0.N PASS

QMOI live stream PASS
Ollama live stream PASS
Master Orchestrator live stream PASS

Self-healing PASS
Checkpoint/resume PASS
Security PASS
Production readiness PASS
Final remote verification PASS
```

Only then may the final execution transition to:

```text
FINAL_STATUS=SUCCESS
PRODUCTION_READY=true
```

and never merely because the individual workflows themselves are green.

### Remote-first execution addendum

All autonomous production mutations must run independently on an authenticated
target-repository runner. A Codespace or local checkout is a submission,
inspection, and read-only observation surface; it is not the authority for
push, pull-request creation, merge, branch synchronization, Q-version
publication, or the final verdict. The target repository workflow must acquire
its own repository-scoped `GITHUB_TOKEN` or preflighted GitHub App identity,
re-fetch immutable source SHAs, enforce protected-branch policy, persist
checkpoints, and publish evidence and live activity remotely.

The local control plane must expose only these remote-safe operations:

``` text
remote-submit  -> target workflow dispatch -> queued remote execution
remote-observe -> remote workflow/run/artifact lookup
status         -> current remote/local evidence without mutation
verify        -> deterministic fail-closed evidence evaluation
```

The target runner owns tests, security, build/runtime validation, PR/check/
merge policy, backup synchronization, cross-repository verification, Q-version
generation, and final production readiness. A missing token, unavailable
remote state, HTTP 403, stale heartbeat, or absent artifact remains
`AUTH_BLOCKED`, `REMOTE_STATUS_UNAVAILABLE`, `STALE`, or
`BLOCKED_REQUIRES_HUMAN`; it must never be converted into `SUCCESS`,
`WAITING`, or `NO_CHANGES_REQUIRED`. See
`REMOTE_EXECUTION_ARCHITECTURE.md` and the target-owned
`.github/workflows/cross-repository-sync.yml` contract.

The executable target-runner contract is implemented by
`scripts/remote_lifecycle.py`. It must acquire the repository-scoped
execution lock, emit correlated JSONL events through
`scripts/live_activity_events.py`, checkpoint every stage through
`scripts/checkpoint_manager.py`, run deterministic validation and security
checks, verify `main` and `autosync-backup` from remote state, and invoke the
single completion engine. The runner must return a non-success terminal state
when cross-repository, authorization, security, Q-version, live-activity, or
remote-SHA evidence is missing. Its JSON result, checkpoint, event stream,
current state, topic metrics, and execution evidence are uploaded by the
target-owned workflow for remote observation after Codespace shutdown.

Remote execution is therefore independently resumable and observable: local
commands may submit, inspect, and verify evidence, but may not substitute
local test results or local Git state for the target runner's authoritative
result. A green dispatch, a passing local suite, or a generated checkpoint is
never sufficient for `PRODUCTION_READY=true`.


## 208. Thoroughly ensure that Alpha-Q-ai repo should have all the contents it already has plus all the directories and files in Alpha-Q-ai-2025 and all these together used as base of all files and directories in Alpha-Q-ai repo before merging. qmoi-enhanced repo should also have all the files it currently has plus all the files and directories in qmoi-enhanced-history-14 and all these used as base contents of everything in qmoi-enhanced repo before merging begins.Also remember to update MERGE.md , ollama master orchestrator and all other files and features based on all these. Ollama autonomous agent should also enhanced and automated further how it sets up all automations in all repos and ensuring qmoi is incharge of all automations and should always ensure a automations are always successful. 