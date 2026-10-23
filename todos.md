# QMOI Mission TODO Plan

This is a resumable execution plan derived from the editor-provided mission
directive and reconciled against the current mission source and ledger. It
does not authorize protected or remote actions, change mission status, or
replace `ollamatracks/mission-task-ledger.json`.

## Plan state

| Field | Observed value |
|---|---|
| Repository | `thealphakenya/Alpha-Q-ai` |
| Branch | `codespace-sturdy-fishstick-69wxr9jjgw5pfrq65` |
| Local HEAD at latest checkpoint | `27012fd1c57d0291d279ae523f12bb0c59cc1a8a` |
| Mission run | `newmission-120-minute-2026-10-23-3d24ef13` |
| Correlation ID | `3d24ef13-b8e9-453a-80cd-41af8a129da4` |
| Latest observed checkpoint | `2026-10-23T01:05:44.775541Z` |
| Remote verification | `false` |
| Planner result | `BLOCKED_NO_SAFE_DEPENDENCY_READY_TASK` |
| Requirement-line review | 772 indexed; 0 reviewed; 772 not reviewed |
| Phase status | 5 partially complete; 13 pending |
| Legacy task status | 1 verified complete; 7 partially complete; 3 blocked; 5 pending |
| Ollama | Local service/model unavailable; authorized hosted inference not measured |
| Continuation result | Orchestrator returned `BLOCKED_NO_SAFE_DEPENDENCY_READY_TASK`; no task/phase transition; GitHub CLI unauthenticated |
| User-reported access | `USER_REPORTED`: GitHub username `simtwovictor` has push permission to both target repositories; not independently verified |
| Worktree | 13 pre-existing modified paths preserved; this plan is untracked |

These are a checkpoint snapshot, not live measurements. Refresh through the
supported ledger tools before a task transition. Do not infer progress from
this document.

## Execution rules

- Use the canonical `latest mission.md`, its byte-identical mirrors,
  `ollamatracks/mission-task-ledger.json`, and the applicable instructions as
  sources of truth. Preserve user work and history.
- Keep `M01`-`M16` distinct from `PH01`-`PH18`. Do not mark an item complete
  without its acceptance evidence; preserve `BLOCKED`, `UNKNOWN`,
  `NOT_MEASURED`, and `NOT_VERIFIED`.
- The ledger currently has no dependency-ready authorized task. Do not start
  blocked tasks, bypass the planner, or invent independent mission work.
- M01 requires owner/admin-authorized, provenance-bound, read-only
  branch-policy evidence for both `thealphakenya/Alpha-Q-ai` and
  `thealphakenya/qmoi-enhanced`. Until then, protected writes, dispatches,
  merge, release, deployment, and claims of remote completion remain blocked.
- User reports that GitHub username `simtwovictor` has push permission to both
  repositories. Record this as `USER_REPORTED` only: this Codespace currently
  has no authenticated GitHub CLI session, and the report does not establish
  identity, effective permissions, branch policy, or authority for a specific
  protected operation.
- Use the existing QEngineer/master-orchestrator architecture. Ollama
  implementation or inference is eligible only on an actually verified,
  authorized runtime. Do not create competing agents or claim a stopped
  session is persistent.
- After authorized work, record the exact command, result, duration where
  measured, repository/ref/SHA, correlation ID, evidence reference, blocker,
  and next action using supported writers. Run focused tests and security
  checks appropriate to the mapped change. Never treat dispatch or local
  success as remote completion.
- For each source requirement, preserve its source path and line locator and
  map it to owner, implementation/integration, test, security, documentation,
  and remote evidence, or explicitly record why each is pending, blocked, or
  not applicable.

## Legacy requirement TODOs

The IDs and dependency graph below mirror the canonical task ledger. Statuses
are the observed ledger statuses, not estimates. Acceptance criteria are
copied or condensed from the ledger; verification commands must be selected
for the actual mapped change and recorded with its evidence.

| ID | Status | Depends on | Action and acceptance criteria | Verification / evidence |
|---|---|---|---|---|
| M01 | BLOCKED | — | Verify repository/ref identity, exact local and remote SHAs, authentication, effective policy, and authority. User reports `simtwovictor` has push permission to both target repositories (`USER_REPORTED`, not verified). Obtain owner-authorized read-only branch-policy evidence for both; retain unavailable evidence as unknown. | Authorized read-only evidence with provenance, actor/credential category, response status, capture time, protected ref/full SHA, and redacted artifact hash. No dispatch or write until separately authorized. |
| M02 | PARTIALLY_COMPLETE | M01 | Reconcile every requirement in the mission, `oe2.txt`, `remotecompletion.md`, `AGENTS.md`, applicable instructions, and discovered sources to a stable task, acceptance evidence, and an explicit outcome. Finish reconciling the 85 named operations and indexed QMOI/Ollama topics against source, plans, workflows, tests, tracking artifacts, and history. | Requirement-source inventory and traceable mappings; record implementation/test/security/documentation/integration/remote evidence or explicit blocker per item. Never turn candidate counts into completion claims. |
| M03 | PARTIALLY_COMPLETE | M02 | Complete source-linked acceptance mapping for all 772 indexed authored mission requirement-line records; persist all 16 stable task IDs, criteria, dependencies, status, timestamps, elapsed time, retries, evidence, blockers, and next actions in the canonical ledger. | `python -m scripts.mission_task_ledger --root . status` and `... actions`; line-level mappings and evidence in supported ledger state. Current line review remains pending until actually performed. |
| M04 | VERIFIED_COMPLETE | — | Preserve bounded mission-clock history and record actual UTC task/phase timing; explicitly mark unavailable monotonic continuity. Reopen only if evidence contradicts this status. | `python -m scripts.mission_task_ledger --root . status`; retain the existing run/deadline and correlated checkpoint history. |
| M05 | PENDING | M02, M03 | Rank eligible tasks by mapped risk/value, dependencies, measured throughput, failure rate, and remaining time. Add weights only when supported by evidence. | Planner output and documented, evidence-based ranking; no transition merely because a task is ranked. |
| M06 | PENDING | M02, M05 | Select only a bounded, confirmed defect with mapped requirements. Document root cause, expected behavior, compatibility, regression coverage, rollback, and applicable security/reliability review; implement real behavior, not placeholders. | Focused regression test(s), applicable security checks, exact diff/command results, and evidence references. |
| M07 | PARTIALLY_COMPLETE | M01, M03, M04 | Keep schema-valid checkpoint, paired Markdown records, JSON state, and append-only JSONL event correlated to the run, repository/ref, exact local identity, timing, blockers, and next action. | Supported checkpoint writer; verify common correlation ID, artifact hashes, ledger digest, dashboard integrity, and explicit remote-verification state. |
| M08 | BLOCKED | M03, M07 | Design and test a non-mutating queue handoff in the existing orchestrator. A supported runner must validate the canonical ledger, select only dependency-ready tasks, bound execution, persist results, and avoid duplicate work without weakening ref/authorization policy. | Focused tests for ledger validation, dependency selection, idempotency, bounded recovery, and policy guards. Hosted resume remains unverified until independently observed. |
| M09 | PARTIALLY_COMPLETE | M01, M08 | Measure runner and model availability and a bounded inference, timeout, and recovery result only on the authorized hosted execution path. | Actual runner/model and inference result with timestamps, timeout/recovery outcome, and exact run/ref/SHA. Keep unavailable measurements `NOT_MEASURED`; do not bypass the hosted-runtime guard. |
| M10 | PARTIALLY_COMPLETE | M01, M08 | Validate target-owned workflow syntax/events, least privilege, concurrency, exact ref, bounded retries, checkpoint restoration, artifacts, and terminal run result. Do not dispatch before authority gates pass. | Workflow validation locally; if separately authorized, terminal run/job evidence bound to exact repository/ref/SHA plus independent remote ref/tree and artifact verification. |
| M11 | PARTIALLY_COMPLETE | M06, M07, M10 | Run bounded relevant validation, classify the interrupted broad-run failure or preserve a complete new failure report, repair confirmed causes, and keep local and remote results distinct. | Exact commands, start/end or elapsed time, exit status, test/check counts, SHA, failure details, repairs, and artifact references. Broaden coverage only after targeted results justify it. |
| M12 | PENDING | M02, M11 | Reconcile all requirements from `oe2.txt`, mission sources, instructions, `remotecompletion.md`, and discovered sources; assign each a traceable verified, partial, blocked, pending, or not-applicable outcome. | Cross-source coverage report with source locators, acceptance mappings, evidence references, and explicit omissions/unreadable inputs. |
| M13 | BLOCKED | M01, M11 | Preserve pre-existing edits. Publish only to a verified, authorized target after exact SHA, validated diff, required review, and checks are evidenced. | No publish while blocked. If gates later pass, record explicit authority, target/ref, exact SHA, review/check evidence, and terminal remote result. |
| M14 | PARTIALLY_COMPLETE | M04, M05, M11 | Recompute elapsed/remaining time, throughput, failure rate, test duration, blockers, and priorities at checkpoints. Measure repair count/human intervention only when observable. | Correlated checkpoint metrics; wall time distinct from process-active monotonic time; unavailable values explicitly `NOT_MEASURED`. |
| M15 | PENDING | M07, M08, M10, M11 | Demonstrate a distinct safe run restoring a saved checkpoint, selecting eligible work, avoiding duplicate completion, and persisting actual run evidence. | Independently observed restoration/resume result and exact run/checkpoint evidence. Until then, state the specific unverified step. |
| M16 | PENDING | M01, M02, M03, M04, M07, M11, M12, M13, M14, M15 | At the actual deadline, produce an evidence-based handover of repository/ref/SHAs, outcomes, tests, workflow/security/deployment state, checkpoint, continuation state, blockers, and next actions. | Supported ledger/checkpoint records; preserve original clock history. This handover is not the final remote-completion TODO below. |

## Canonical phase TODOs

Every canonical phase is represented separately below and maps to its
corresponding `PHxx` section in `latest mission.md`. Phase status mirrors the
latest observed ledger snapshot. The linked M-tasks are planning crosswalks,
not a replacement dependency graph; use the ledger for actual readiness.

| ID | Mission source section | Linked M-task crosswalk | Status | Acceptance outcome |
|---|---|---|---|---|
| PH01 | Phase 1 — Discover and Preserve Everything | M01, M02, M11 | PARTIALLY_COMPLETE | Repository, branch, worktree, requirements, code/tests/workflows, dependencies, gaps, security, and remote state are inventoried with uncertainty and pre-existing work preserved. |
| PH02 | Phase 2 — Create a Persistent Requirements Ledger | M02, M03, M12 | PARTIALLY_COMPLETE | Every source requirement has a stable traceable record, criteria, dependencies, owner, implementation/test/security/docs/integration/evidence status, and explicit unresolved state. |
| PH03 | Phase 3 — Unify the Existing Autonomous Architecture | M08, M10, M15 | PENDING | Existing controller, scheduler, ledger, executor, checkpoint/recovery, and auditor are coherently integrated; duplicate work/writers/triggers are prevented and focused tests pass. |
| PH04 | Phase 4 — Make Ollama the Primary Execution Engine | M08, M09 | PENDING | Ollama work is executed only through a verified authorized runtime with bounded inference/recovery and real recorded results; unavailable runtime stays blocked. |
| PH05 | Phase 5 — Maximize Safe Completion Speed | M05, M14 | PENDING | Dependency-aware prioritization, safe concurrency, evidence reuse, bounded retries, and measured resource/throughput behavior are demonstrated without skipping gates. |
| PH06 | Phase 6 — Enforce Real Production Implementations | M02, M06, M11 | PENDING | Mapped behavior is genuinely implemented and integrated, not represented by mocks/placeholders; compatibility, regression, and relevant security checks pass. |
| PH07 | Phase 7 — Implement Bounded Autonomous Repair | M06, M08, M11 | PENDING | Repairs are scoped, bounded, test-driven, recoverable, and stop on authorization/security limits; failures remain visible and no false-green fallback is possible. |
| PH08 | Phase 8 — Implement Durable Checkpoints and Recovery | M03, M07, M08, M15 | PENDING | Canonical state and correlated checkpoint artifacts survive interruption and safely resume without duplicate execution; independent restoration is evidenced. |
| PH09 | Phase 9 — Add Independent Quality and Security Gates | M06, M11, M12 | PARTIALLY_COMPLETE | Relevant tests, reviews, dependency/security checks, and required gates are mapped to changes; unresolved/unknown findings block protected completion. |
| PH10 | Phase 10 — Implement Safe Git and Remote Automation | M01, M10, M13 | PENDING | Git/remote actions are identity-, policy-, authorization-, ref-, and SHA-bound, with protected actions fail-closed and terminal evidence required. |
| PH11 | Phase 11 — Verify Both Repositories | M01, M10, M12, M13 | PENDING | Both target repositories are independently checked against intended refs/SHAs and required parity/evidence; denied or missing access remains unknown. |
| PH12 | Phase 12 — Keep Documentation Synchronized | M02, M07, M12 | PARTIALLY_COMPLETE | Required documentation and generated state are accurate, source-linked, correlated, and synchronized without rewriting policy or claiming unverified behavior. |
| PH13 | Phase 13 — Maintain Live Progress and Evidence | M03, M07, M14, M16 | PARTIALLY_COMPLETE | Actual events, metrics, timing, artifacts, blockers, and next actions are durable and correlated; unmeasured values and remote/local boundaries remain explicit. |
| PH14 | Phase 14 — Automated Final Completeness Audit | M02, M12, M16 | PENDING | Every original and discovered requirement is reconciled against implementation, tests, security, integration, docs, and evidence; skipped/unreadable scope is explicit. |
| PH15 | Phase 15 — Define Honest Completion States | M12, M16 | PENDING | Requirement, implementation, test, security, integration, deployment, commit, push, remote-check, and cross-repository states remain distinct and evidence-backed. |
| PH16 | Phase 16 — Execute the Mission Now | M02-M16 | PENDING | Eligible work is executed in dependency order with implementation, focused validation, repair, independent verification, and checkpoints; blocked work remains precisely queued. |
| PH17 | Phase 17 — Implement a Structured Copilot-to-Ollama Bridge | M08, M09, M10, M15 | PENDING | Existing approved bridge, if available, is verified and constrained with sanitized structured payloads, bounded execution, local/remote separation, and independently tested handoff; absence is reported, not bypassed. |
| PH18 | Phase 18 — Final Execution and Deliverables | M12, M16, FINAL_REMOTE_COMPLETION_CONFIRMATION | PENDING | Required deliverables and acceptance evidence are complete; final remote confirmation is attempted only after every prerequisite is independently verified. |

## Cross-cutting deliverables and gates

These are acceptance dimensions of the TODOs above, not permission to change
protected state:

- **Durable state:** canonical ledger and supported correlated checkpoint
  artifacts; append-only events; bounded recovery; no stale or fabricated
  success state.
- **Implementation and integration:** production behavior linked to source
  requirements, compatibility and rollback considered, focused tests passing,
  no placeholder success.
- **Quality and security:** applicable tests and security checks recorded;
  unresolved findings are not suppressed or self-approved; secret values are
  never recorded.
- **Documentation:** `oe2.txt`, `remotecompletion.md`, `QENGINEER.md`, the
  applicable instruction/documentation surfaces, and generated state are
  reconciled when actual work changes their content. Policy instructions are
  not rewritten during routine execution.
- **Remote completion:** exact target repository, intended ref, full SHA,
  authorized terminal workflow/check evidence, remote tree/artifact state,
  required parity, and applicable security/approval evidence must all be
  independently verified. A local pass, dispatch, PR, or elapsed time is not
  proof.

## Final TODO — must remain last

### FINAL_REMOTE_COMPLETION_CONFIRMATION

- **Status:** BLOCKED
- **Depends on:** every preceding TODO in this file, including every PH01-PH18
  acceptance criterion and all original requirement-line mappings.
- **Action:** Only after every prerequisite is complete and independently
  verified, inspect the actual remote repository and intended branch; required
  commits and exact remote HEAD SHA; authorized publication; local/remote tree
  parity; mandatory CI, tests, security checks, phase criteria, original
  requirements, discovered gaps, synchronized records, and terminal execution
  evidence. Confirm no required work remains pending, partial, skipped,
  inaccessible, or unverified.
- **Acceptance:** Timestamped, provenance-bound evidence records the exact
  verified repository/ref/SHA and all required terminal checks in
  `remotecompletion.md`, `oe2.txt`, and the canonical ledger. `remote_verified`
  becomes true only through the supported evidence-backed path.
- **Verification/evidence:** Independently read back the remote ref/tree and
  terminal target-owned workflow/check results at the exact SHA. Never infer
  success from a local commit or dispatch.
- **Blocker handling:** If any check fails, reopen/create the relevant TODO
  and return here only after it is verified. If authority or infrastructure
  blocks confirmation, keep this item BLOCKED with the precise owner action
  and evidence needed; do not claim remote completion.
