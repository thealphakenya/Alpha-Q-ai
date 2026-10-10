# Mission

**Status:** IN_PROGRESS. This document is an execution contract and prioritized roadmap, not evidence that its planned work is implemented or complete.

## Source And Scope

The repository-root `MISSION.md` is canonical. `.github/instructions/MISSION.md` must remain byte-for-byte identical; `tests/test_control_plane.py` enforces this and verifies that every `*.instructions.md` file links back here. Update the canonical file first, copy the complete content to the mirror, then run that focused check.

This mission applies with `AGENTS.md`, `.github/copilot-instructions.md`, and every file under `.github/instructions/`. Those policies remain controlling. This roadmap supplements them and never authorizes a protected change, credential use, financial action, release, deployment, branch update, or remote mutation by itself.

## Policy Traceability

The execution contract and roadmap incorporate these mandatory requirements; consult each linked policy for its complete controls:

| Governing file | Requirements carried into this mission |
| --- | --- |
| `AGENTS.md` and `.github/copilot-instructions.md` | Inspect before editing; preserve dirty work; keep local and remote proof distinct; retain required paired and machine evidence; never bypass branch protection or claim remote completion without exact-SHA terminal proof. |
| `.github/instructions/agent-autonomy.instructions.md` | Bounded resumable execution; explicit owner, prerequisites, correlation ID, repo/ref/SHA, measured duration, artifacts, coverage, omissions, blockers, and next action; no self-authorization or bulk replacement of candidates. |
| `.github/instructions/github-api.instructions.md` | Verify identity and authority; inspect protection before mutation; classify HTTP 400/401/403/404/409/422/429/5xx separately; bind observations to owner/repository/ref/full SHA and endpoint; never equate dispatch acceptance with terminal success. |
| `.github/instructions/release.instructions.md` | Require release ID, source SHA, artifact names/hashes, install/runtime verification, provenance, remote retrieval evidence, and explicit authority; retain failed evidence and do not publish from a plan. |
| `.github/instructions/security.instructions.md` | Keep secrets value-free; require owner-confirmed credential rotation and least privilege; retain unresolved findings; map remediation, tests, rollback, and evidence; audit finance categories without storing source amounts, account IDs, or credentials. |
| `.github/instructions/workflows.instructions.md` | Keep heavy validation on target-owned workflows; validate YAML, triggers, permissions, reuse, and concurrency before authorized dispatch; bind runs/jobs/artifacts to exact SHA and require terminal plus independent remote verification. |
| `.github/instructions/workspace.instructions.md` | Prefer metadata/deltas; respect locks and user edits; validate narrowly first; separate planned from verified; checkpoint long inventories; refresh required Markdown/finance catalogs; report ignored, excluded, unreadable, and bounded inputs. |

For a full `audit-inventory` refresh, regenerate the applicable Markdown category index, finance catalog, and managed finance evidence in `FINANCIALMANAGER.md` from the same checkpoint. Finance and production-gap matches remain candidates requiring review, not proof or authorization. Keep the repository's canonical `TREE.md` scope limits explicit; do not infer coverage of ignored paths, Git history, or remote refs.

## Outcome

Deliver the requested engineering and audit work as real, maintainable implementations with traceable requirements, tests, operational evidence, and safe recovery. Preserve user work. Work quickly by prioritizing risk and dependencies and parallelizing only independent tasks with isolated outputs; do not promise a completion time, convert queued work into success, or trade evidence and correctness for speed.

An implementation is production-ready only when its owner and intended behavior are known, inputs and failure states are handled, authorization and data boundaries are explicit, retries are bounded, observability and rollback are defined where relevant, and focused tests plus required workflow evidence pass. Stubs, candidate counts, documentation plans, and local test results are not production or remote-completion proof.

## Execution Contract

1. **Preserve and identify.** Record repository, ref, exact local commit and tree, dirty-worktree state, correlation ID, and existing locks/checkpoints. Never overwrite user changes or silently resume from an unverified checkpoint.
2. **Inventory instructions.** Read root and applicable instructions before protected work. Record relative path, scope, byte count, SHA-256, and read/parse outcome in supported machine evidence. Distinguish parsed from merely read; missing, empty, unreadable, malformed, or changed instructions block protected planning.
3. **Map before changing.** Give each requirement a stable ID, owner/scope, prerequisite, acceptance check, test/evidence reference, risk, rollback or recovery note, and status. Keep discovery candidates separate from confirmed defects and implementation results.
4. **Execute bounded work.** Order tasks by risk and dependency. Use independent deterministic shards only where outputs are isolated; cap retries, checkpoint before long scans, resume only from verified state, preserve failures, and report skipped/unreadable/out-of-bound scope.
5. **Validate progressively.** Run the narrowest relevant test or check after each change, then required integration and repository gates. Record command, result, duration, commit/tree identity, artifact hashes, omissions, and blockers. Never suppress unrelated failures or call an unavailable check a pass.
6. **Synchronize safely.** Keep the mission mirror byte-identical and test it. For repository synchronization, use the authorized target-owned workflow, explicit source/target/ref/SHA, non-force fast-forward policy, preflight drift checks, and independent post-run ref/tree verification. A local mirror check is not cross-repository parity.
7. **Close only on evidence.** Local completion and remote completion are distinct. Remote completion requires the exact repository/ref/SHA, terminal successful target-owned workflow, independently verified remote ref/tree and required artifacts/checks, plus applicable authorization, security, and branch-protection evidence. Otherwise retain `IN_PROGRESS`, `NEEDS_REVIEW`, or `BLOCKED`, with a concrete next action.

## Autonomous Remote Completion Loop

This is the resumable coordinator contract for finishing the mission. It may automatically perform local, read-only, and already-authorized low-risk work; it cannot authorize itself, bypass branch rules, or promise completion before external gates pass.

| State | Automatic action | Transition condition |
| --- | --- | --- |
| `SNAPSHOT` | Record canonical repositories, requested refs, local HEAD/tree/dirty state, correlation ID, policy hashes, and current queue/checkpoint. | Proceed only when required inputs are readable and the checkpoint is internally consistent; otherwise `BLOCKED_INPUT`. |
| `PREFLIGHT` | Read identity, repository identity, exact remote SHAs/trees, required checks, workflow inventory, protection/rulesets, and permitted alert visibility for every target. | Any missing/ambiguous identity, 401/403/404, denied protection, or unavailable required source is recorded as `BLOCKED_AUTH` or `UNKNOWN`; no mutation is attempted. |
| `ANALYZE` | Reuse already-fetched workflow/check results, including CodeQL run/job metadata, bound to the exact repository/ref/SHA. Read findings only through an authorized endpoint. | Stale/missing analysis is `NOT_OBSERVED`; in-progress jobs are `WAITING_CHECKS`; denied alert access is `UNKNOWN`, never zero findings. Do not launch duplicate CodeQL analysis in the fast path. |
| `PLAN_REMEDIATION` | Convert each failed check or uncovered requirement into an owned task with prerequisite, acceptance test, risk, rollback, authority, and evidence reference. Automatically proceed with safe local fixes and focused validation. | Protected, credential, release, deployment, financial, or provider operations stay queued until their documented authority and gates are independently verified. |
| `EXECUTE_AUTHORIZED` | Submit eligible work only through the target-owned workflow, keyed idempotently by repository/ref/SHA/workflow and bounded attempt. Preserve each run/job result. | A queued/accepted dispatch is `WAITING_WORKFLOW`, not success. Failed attempts retain artifacts and blockers; retries are bounded, never infinite. |
| `VERIFY` | Re-read the target ref/tree, terminal workflow conclusions, required statuses, artifact hashes, security/CodeQL findings, and relevant protection state. | If the ref advanced, invalidate prior SHA-bound evidence and return to `PREFLIGHT` for the new SHA. If any check is missing, failed, skipped when required, or unavailable, return to the queue with its exact blocker. |
| `FINALIZE` | Write one paired terminal checkpoint to `oe2.txt`, `remotecompletion.md`, `remote-completion.json`, and the append-only ledger, preserving one correlation ID and exact evidence references. | Set `COMPLETED` only when all mission requirements and required remote gates are independently verified for the same exact SHA/tree. Otherwise retain `NEEDS_REVIEW` or `BLOCKED`. |

### Resume And Stop Rules

- Prefer target-owned `workflow_run`, `workflow_job`, `check_run`, and `push` events to wake a continuation. Use an existing authorized scheduled workflow only as a fallback; do not create duplicate pollers or dispatches.
- When events are unavailable, use bounded read-only polling with capped backoff and a small maximum attempt count. On exhaustion, persist `WAITING_EXTERNAL` with the next event or owner action and exit; do not hold a CPU-bound loop open.
- A new commit/ref invalidates evidence tied to an older SHA. Re-plan only the affected SHA-bound work and reuse other evidence only when its contract allows it.
- Resume only from a verified checkpoint with matching repository/ref/SHA and intact artifact hashes. Preserve interrupted work as `IN_PROGRESS`; never promote it based on elapsed time or partial files.
- Stop automatic execution immediately at missing authority, denied protected access, unresolved actionable security findings, failed required checks, or an external provider/owner decision. The queue remains resumable, but the agent cannot claim it will eventually pass without that prerequisite.

### Terminal Completion Gate

Remote completion requires, for every target repository and required ref in scope: verified repository identity; a full current SHA and tree; the intended changes present in that tree; terminal success for all required target-owned checks on that SHA; required CodeQL analysis terminal on that SHA with alert access and findings status understood; failed Vercel/deployment checks resolved when required; branch/ruleset authority verified; no unresolved required security or human-approval gate; and independently verified artifacts/statuses. All matching claims must be present in the paired ledgers under the same correlation ID. Missing or denied evidence remains a blocker. A successful CodeQL job, clean local tests, or local/remote main parity alone never passes this gate.

## Prioritized Automation Roadmap

The items below are planned unless independently verified by code, focused tests, and evidence. Do not mark an item complete from this list alone.

| Priority | Workstream | Production acceptance |
| --- | --- | --- |
| P0 | Mission and instruction integrity | Canonical/mirror byte parity; every instruction links to this mission; focused regression fails on drift. |
| P1 | Structured instruction inventory | Enumerate all applicable instruction files; validate UTF-8, emptiness, supported frontmatter/scope, and parse outcome; hash inputs; detect changes between inventory and use; fail closed on incomplete inventory. |
| P1 | Resumable task orchestration | Persist a dependency-aware queue with owner, stable task/correlation IDs, bounded attempts, checkpoint schema/version, measured duration, artifact references, and explicit recovery/blocker states. Resume idempotently from verified checkpoints only. |
| P1 | Deterministic audit shards | Partition by stable path/manifest identity; use isolated outputs and deterministic aggregation; bind every shard to repository/ref/commit/tree and manifest hash; retain failed shards and state exact omissions. |
| P1 | Requirement-to-implementation coverage | Map features, routes, components, hooks, APIs, docs, security controls, and workflows to owners, source, tests, and evidence. Review candidates before remediation; never bulk-rewrite gaps based on keyword matches. |
| P1 | Evidence and metric integrity | Generate paired human/machine checkpoints with one correlation ID, append-only events, source/artifact hashes, status, duration, denominator, coverage limits, and next action. Separate observed, locally verified, terminal, and independently remote-verified evidence. |
| P2 | Workflow and remote verification | Validate workflow syntax, triggers, permissions, concurrency, and exact-SHA binding before any authorized dispatch; record run/job/artifact identities; require terminal conclusions and independent remote ref/tree checks. Reuse already-fetched CodeQL run metadata only; never add a duplicate scan or API call to the fast path. |
| P2 | Synchronization and drift detection | Test local document mirrors; inventory both repositories before sync; detect conflicts and stale/divergent refs; require explicit authority and target-owned workflows; never force-push or infer parity from matching filenames or dispatch acceptance. |
| P2 | Security and sensitive-domain gates | Keep secrets value-free; verify identity, scope, rotation, least privilege, and endpoint evidence; map dependency/security findings to owner, impact, remediation, tests, rollback, and remote proof. Treat CodeQL run metadata as advisory unless the target's required-check policy says otherwise; stale or absent analysis is never a clean result. Finance/trading/payroll/payment actions remain separately authorized and blocked without provider, owner, legal, and security evidence. |
| P3 | Operational assurance | Expose status, queue age, shard progress, retries, duration, failures, omissions, and stale-checkpoint alerts without claiming continuous worker availability. Define service objectives only after owners and measurement sources approve them. |

## Required Measures

Every audit or execution report should include, where applicable: requirements total/mapped/implemented/tested/blocked; input files discovered/read/parsed/skipped/unreadable; shard planned/started/passed/failed/retried; elapsed time; source and artifact hashes; ignored/excluded scope; security findings; local versus remote verification level; exact blockers and next action. State each denominator and scope. Counts and percentages are integrity signals, not semantic proof, production readiness, or remote completion.

## Completion Checklist

- All active requirements and instructions are inventoried, mapped, and reviewed; no missing or unreadable input is hidden.
- Each claimed implementation has a focused passing test and required integration/workflow evidence; failures and omissions remain visible.
- The working tree and local/remote refs are reported accurately; no user work is lost and no unapproved mutation occurred.
- The mission mirror check passes and paired checkpoint artifacts agree on correlation ID and status.
- Protected or remote work is complete only with the exact-SHA authority and terminal evidence described above. If any gate is unavailable, report the mission as blocked or in progress and preserve its resumable queue.

## Current Continuation

- Finish or safely resume the existing local QAUDITS inventory; do not start a competing full scan while one is active.
- Validate mission mirror parity and the focused regression, then record the result through the supported checkpoint path without overwriting newer user evidence.
- Continue the remaining prioritized local audit and implementation checks from verified checkpoints; preserve exact omissions, failures, and durations.
- Keep remote completion blocked until authenticated, authorized target-owned terminal exact-SHA and remote-tree evidence is independently available.

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
