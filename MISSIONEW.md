MISSION: COMPLETE AND ENHANCE QMOI REMOTE COMPLETION USING
OLLAMA-FIRST AUTONOMOUS DEVELOPMENT, A STRUCTURED COPILOT BRIDGE,
PRODUCTION-GRADE IMPLEMENTATIONS, AND EVIDENCE-VERIFIED AUTOMATION

============================================================
PRIMARY OBJECTIVE
============================================================

Upgrade the existing QMOI autonomous development system so Ollama
can independently plan, implement, integrate, test, repair, document,
secure, commit, push, and verify all authorized mission requirements
across the Alpha-Q-ai and qmoi-enhanced repositories.

Maximize completion speed without sacrificing correctness, security,
production quality, maintainability, accessibility, or completeness.

Preserve every mandatory requirement. Prevent forgotten tasks,
superficial implementations, duplicate execution, conflicting Git
operations, endless repair loops, and false completion claims.

Ollama must be the primary execution engine. GitHub Copilot Chat must
be optional for routine execution. When Copilot is available, provide
a structured, validated interface for communicating tasks to Ollama.

Integrate all enhancements into the existing autonomous agent and
master orchestrator wherever practical. Do not create competing
autonomous systems when existing components can be improved.

Execute the mission, not merely describe it. Inspect the actual
repository, implement changes, run tests, repair failures, verify
remote state, and record evidence.

============================================================
PHASE 1 — DISCOVER AND PRESERVE EVERYTHING
============================================================

Inspect the actual repository, active branch, Git status, recent
commits, existing source code, tests, workflows, scripts, configuration,
issues, dependencies, and relevant documentation before modifying
anything.

Read oe2.txt, remotecompletion.md, and all applicable mission
instructions and relevant Markdown files, including architecture,
styles, universals, accessibility, device support, testing, security,
deployment, APIs, endpoints, routes, model evolution, and
cross-repository requirements.

Verify actual paths, branch contents, and file histories. Do not
assume that previously mentioned files, features, permissions,
implementations, or tests currently exist.

Inventory:
- Fully implemented features.
- Partially implemented features.
- Missing requirements.
- Failing tests and builds.
- Broken workflows and integrations.
- Duplicate or conflicting automation.
- Security findings and vulnerable dependencies.
- Temporary workarounds, mocks, and placeholders.
- Unverified implementations and remote operations.
- Requirements blocked by missing access or external dependencies.

Create a baseline before changing anything.

Preserve valuable existing work, user modifications, uncommitted
changes, branch history, and working functionality.

Never discard changes merely to obtain a clean working tree.

============================================================
PHASE 2 — CREATE A PERSISTENT REQUIREMENTS LEDGER
============================================================

Create a durable, version-controlled requirements ledger with stable
identifiers, original source references, acceptance criteria,
dependencies, priorities, affected components, implementation status,
test evidence, blockers, commits, and remote verification status.

Track these states separately:
- Requirement discovered.
- Requirement understood.
- Implementation started.
- Implementation completed.
- Integration verified.
- Tests passed.
- Security review completed.
- Deployment readiness verified.
- Changes committed.
- Changes pushed.
- Remote checks passed.
- Cross-repository synchronization verified.
- Requirement fully completed.

Preserve overlapping requirements individually. Consolidate tracking
only when every original requirement and acceptance criterion remains
traceable.

Resolve conflicting instructions explicitly according to instruction
precedence and repository policy. Never silently discard or weaken a
mandatory requirement.

Record unresolved ambiguities and dependencies instead of inventing
requirements or making unsupported assumptions.

Reconcile the ledger against the original instructions and actual
repository state after every major phase and during the final audit.

Ensure mission state survives restarts, context limits, failed model
requests, Codespaces interruptions, and workflow timeouts.

Resume from the earliest unresolved dependency without blindly
repeating successful or irreversible operations.

============================================================
PHASE 3 — UNIFY THE EXISTING AUTONOMOUS ARCHITECTURE
============================================================

Inspect and enhance the existing components, verifying their paths:

- .github/workflows/ollama-autonomous-agent.yml
- .github/workflows/ollama-master-orchestrator.yml
- Existing Ollama autonomous-agent scripts.
- Existing master-orchestrator scripts.
- Existing automated tests.
- Existing checkpoints and recovery mechanisms.
- Existing CURRENT_STATUS and TRACKING_INDEX files.
- Existing telemetry.jsonl and live activity streams.
- Existing mission instructions and tracking documentation.

Reuse working components and preserve backward compatibility where
practical.

Establish ONE authoritative:
- Mission controller.
- Task scheduler.
- Requirements ledger.
- Checkpoint and recovery system.
- Model execution coordinator.
- Repository-writing coordinator.
- Completion and evidence auditor.

The master orchestrator owns mission scheduling, task dependencies,
execution leases, and task assignment.

The autonomous agent executes assigned tasks, validates results,
and reports evidence.

Prevent:
- Duplicate Ollama inference loops.
- Recursive workflow triggers.
- Multiple controllers running the same mission.
- Conflicting repository writers.
- Duplicate commits and pushes.
- Contradictory checkpoints.
- Stale execution leases.
- Repeated completed tasks.
- Unnecessary workflow runs.
- Conflicting mission states.

Use existing workflow triggers and concurrency controls where
appropriate. Avoid introducing a parallel autonomous workflow when
the existing architecture can be safely upgraded.

============================================================
PHASE 4 — MAKE OLLAMA THE PRIMARY EXECUTION ENGINE
============================================================

Use Ollama by default for:
- Mission analysis and task decomposition.
- Repository exploration.
- Dependency and implementation analysis.
- Planning and prioritization.
- Source-code implementation.
- Frontend and backend integration.
- Test-failure diagnosis and repair.
- Refactoring and regression analysis.
- Documentation updates.
- Security-finding triage.
- Checkpoint recovery.
- Task scheduling recommendations.
- Final evidence analysis and completion reporting.

Copilot must be optional for ordinary development work.

When Copilot is available, it may contribute plans, structured tasks,
alternative diagnoses, or independent reviews through the bridge
defined in PHASE 17.

When Copilot is unavailable, Ollama must continue executing authorized
tasks independently.

Use a structured task interface between the controller and Ollama.
Validate model outputs before any tool invocation.

Route file modifications, shell commands, Git operations, and network
access through restricted, auditable execution tools.

Never trust model-generated completion claims without independent
verification.

Never allow unvalidated model output to execute arbitrary commands,
modify unauthorized paths, expose secrets, or bypass security policy.

============================================================
PHASE 5 — MAXIMIZE SAFE COMPLETION SPEED
============================================================

Implement dependency-aware scheduling that prioritizes:

1. Critical blockers preventing other work.
2. Broken infrastructure and validation pipelines.
3. Missing foundations required by dependent features.
4. High-priority production functionality.
5. Integration and regression failures.
6. Remaining mandatory requirements.
7. Optional enhancements after mandatory work is secured.

Use the critical path to determine which work most directly advances
verified completion.

Parallelize genuinely independent tasks when resources permit.

Serialize tasks that modify overlapping files, shared configuration,
the same Git branch, or shared persistent state.

Start with one active model request and one repository writer.
Increase concurrency only after measuring resources and demonstrating
that additional concurrency improves throughput without introducing
conflicts, memory exhaustion, or excessive inference overhead.

Reuse test results only when the relevant code, dependencies,
configuration, and environment have not changed.

Invalidate stale evidence and rerun affected checks after modifications.

Avoid redundant model calls, unnecessary full-repository context,
repeated completed work, excessive logging, and unnecessary workflow
execution.

Track:
- Tasks completed per hour.
- Model calls per task.
- Copilot usage where measurable.
- Repair attempts per failure.
- Test and build duration.
- CPU and memory consumption.
- Human interventions.
- Failed and blocked tasks.
- Remaining critical-path work.
- Verification and deployment readiness.

Optimize for verified throughput rather than raw code volume.

============================================================
PHASE 6 — ENFORCE REAL PRODUCTION IMPLEMENTATIONS
============================================================

Implement actual working functionality, not merely plans, files,
interfaces, UI mockups, stubs, hardcoded responses, placeholder
implementations, or superficial success messages.

Before implementing a feature:
1. Inspect the existing implementation.
2. Identify the actual requirements and gaps.
3. Determine dependencies and affected components.
4. Design the smallest complete, maintainable solution.
5. Implement the feature.
6. Integrate it with the actual system.
7. Test successful and failure scenarios.
8. Inspect security and regression risks.
9. Document the actual behavior.
10. Record evidence before declaring completion.

Implement all applicable:
- Frontend and backend functionality.
- APIs and real service communication.
- Authentication and authorization.
- Database schemas, migrations, and persistence.
- Input validation and error handling.
- Configuration and secret management.
- Timeouts, bounded retries, and rate-limit handling.
- Logging, monitoring, and operational diagnostics.
- Accessibility and responsive layouts.
- Device and platform compatibility.
- Automated tests and failure recovery.
- Deployment and release configuration.
- Rollback and recovery procedures.
- Documentation and operational instructions.

Use real dependencies and services where available.

Do not substitute a mock, simulation, hardcoded response, disabled
integration, or placeholder for required production functionality.

Where credentials, hardware, external services, or permissions are
unavailable, complete safe work where possible and record precisely
what remains unverified.

Do not fabricate external service responses or claim integrations
work when they have not been exercised.

Avoid unnecessary rewrites or speculative feature expansion that
delays mandatory requirements.

Improve existing implementations wherever practical.

============================================================
PHASE 7 — IMPLEMENT BOUNDED AUTONOMOUS REPAIR
============================================================

For every failing test, build, or validation check:

1. Capture the command, exit code, logs, and environment.
2. Classify the failure.
3. Identify the likely root cause.
4. Inspect relevant code and dependencies.
5. Generate the smallest coherent repair.
6. Validate the proposed changes.
7. Apply the repair safely.
8. Rerun the failed check.
9. Run appropriate regression checks.
10. Record the result and supporting evidence.

Use a configurable default maximum of three repair attempts per
failure before escalation.

If unsuccessful, try a materially different diagnosis when appropriate.
Then preserve the blocker and escalate instead of looping indefinitely.

Do not repeatedly apply equivalent patches without new evidence.

Handle:
- Model unavailability.
- Resource exhaustion.
- Network failures.
- Missing credentials.
- Permission errors.
- Flaky tests.
- Dependency conflicts.
- External service outages.
- Invalid model responses.
- Build and deployment failures.

Preserve mission state when failures occur.

Automatically reopen previously completed tasks when fresh evidence
reveals regressions or when acceptance criteria are no longer met.

============================================================
PHASE 8 — IMPLEMENT DURABLE CHECKPOINTS AND RECOVERY
============================================================

Persist:
- Mission IDs.
- Task IDs and dependencies.
- Request identifiers.
- Execution attempts.
- Execution leases.
- Checkpoints.
- Changed files.
- Model and tool execution results.
- Git references and commit SHAs.
- Test results.
- Security findings.
- Blockers.
- Last verified operation.
- Outstanding remote operations.

Use atomic state updates, stale-lease recovery, and idempotent
operations where appropriate.

On restart:
1. Verify the repository and branch.
2. Inspect the working tree and user changes.
3. Restore the latest valid checkpoint.
4. Reconcile local and remote Git state.
5. Determine which operations actually succeeded.
6. Invalidate stale test evidence.
7. Reconcile the task ledger.
8. Resume the earliest unresolved dependency.

Never blindly repeat commits, pushes, merges, migrations, deployments,
or other potentially irreversible operations.

Use durable storage appropriate to the environment. Do not assume
that an ephemeral Codespace filesystem persists after deletion.

============================================================
PHASE 9 — ADD INDEPENDENT QUALITY AND SECURITY GATES
============================================================

Use deterministic verification tools rather than trusting Ollama's
self-assessment.

Run applicable:
- Unit tests.
- Integration and end-to-end tests.
- Regression tests.
- Type checks.
- Linting.
- Static analysis.
- Build and packaging checks.
- CodeQL code scanning.
- Dependency vulnerability scanning.
- Workflow YAML validation.
- Configuration validation.
- Secret detection.
- Sensitive-file checks.
- Diff and unintended-change inspection.
- API tests.
- Authentication and authorization tests.
- Accessibility checks.
- Device compatibility checks.
- Deployment and rollback checks.
- Remote GitHub Actions validation.

Inspect existing test coverage and add missing tests for:
- Mission scheduling.
- Invalid model output.
- Repair limits.
- Timeouts.
- Cancellation.
- Checkpoint recovery.
- Stale execution leases.
- Concurrent writers.
- Git failures.
- Duplicate workflow triggers.
- Permission failures.
- Bridge authorization.
- Idempotency.
- End-to-end mission completion.

Select checks appropriate to the actual technology stack.

Do not claim a check passed when it was skipped, blocked, unavailable,
or never executed.

Report skipped checks as SKIPPED and unavailable mandatory checks as
BLOCKED or UNVERIFIED, as appropriate.

Address security findings according to severity and actual applicability.
Do not automatically suppress or dismiss findings merely to obtain
a passing result.

============================================================
PHASE 10 — IMPLEMENT SAFE GIT AND REMOTE AUTOMATION
============================================================

Use authorized credentials and least-privilege permissions.

Preserve user changes, inspect every diff, and use a dedicated mission
branch where appropriate.

After implementation and required verification:

1. Commit coherent, verified changes.
2. Push to the authorized remote branch.
3. Confirm the remote branch contains the expected commit.
4. Open or update a pull request when authorized.
5. Wait for required remote checks.
6. Diagnose and repair failures within configured limits.
7. Merge only when authorized and all required branch protections,
   reviews, and checks are satisfied.
8. Verify the resulting remote state.

Never bypass branch protections, expose secrets, execute untrusted
pull-request code with write credentials, or fabricate GitHub results.

If credentials or permissions are missing, complete safe local work
and record the exact blocker.

A local commit or successful push is not proof that remote CI passed.

============================================================
PHASE 11 — VERIFY BOTH REPOSITORIES
============================================================

Treat the following repositories as related but independently
verifiable projects:

- thealphakenya/Alpha-Q-ai
- thealphakenya/qmoi-enhanced

Verify actual access, repository identity, branches, and current
remote state before operating on either repository.

Determine which requirements belong to each repository and identify
cross-repository dependencies.

Implement and test changes in the correct repository.

Verify:
- Branch relationships.
- Expected commits.
- Synchronization direction.
- Conflict handling.
- Required documentation.
- Remote CI results.
- Pull requests and merge status.
- Cross-repository compatibility.

Do not overwrite divergent histories or force-push without explicit
authorization.

Record the exact commit SHA, branch, changed files, validation results,
and synchronization status for each repository.

Never report both repositories complete merely because one repository
passed its checks.

============================================================
PHASE 12 — KEEP DOCUMENTATION SYNCHRONIZED
============================================================

Update relevant Markdown documentation whenever actual architecture,
behavior, interfaces, requirements, workflows, or operational
procedures change.

Inspect applicable:
- Architecture documentation.
- API, endpoint, and route documentation.
- Model evolution documentation.
- Styles and universals documentation.
- Accessibility documentation.
- Device and platform documentation.
- Testing documentation.
- Security documentation.
- Deployment and release documentation.
- Remote-completion instructions.
- Other mission-specific Markdown files.

Document actual implemented behavior, configuration, dependencies,
limitations, setup procedures, testing, recovery, and deployment.

Avoid duplicate or contradictory documentation.

Preserve mandatory requirements and distinguish planned capabilities
from implemented and verified functionality.

============================================================
PHASE 13 — MAINTAIN LIVE PROGRESS AND EVIDENCE
============================================================

Integrate with existing tracking systems where present and appropriate,
including:
- CURRENT_STATUS.
- TRACKING_INDEX.
- telemetry.jsonl.
- Checkpoint artifacts.
- Live activity streams.
- Existing mission dashboards.

Maintain an evidence ledger containing:
- Requirement ID and original source.
- Implementation and changed files.
- Test commands, exit codes, and results.
- Security and regression findings.
- Skipped checks and blockers.
- Commit SHA and remote branch.
- Pull request and required CI status.
- Cross-repository verification.
- Evidence timestamps and freshness.
- Actual completion status.

Make status updates atomic and consistent with the authoritative ledger.

Report meaningful progress without excessive repeated logging.

Never fabricate telemetry, test results, commit SHAs, remote states,
or completion claims.

============================================================
PHASE 14 — AUTOMATED FINAL COMPLETENESS AUDIT
============================================================

Before declaring completion, compare every mandatory requirement with
its implementation, acceptance criteria, test evidence, and required
remote state.

Detect:
- Missing or unassigned requirements.
- Partially implemented features.
- Unintegrated components.
- Remaining prohibited placeholders.
- Failing or skipped mandatory checks.
- Regressions and security findings.
- Stale verification evidence.
- Undocumented changes.
- Unpushed commits.
- Missing remote checks.
- Cross-repository inconsistencies.
- Unresolved blockers.
- Unauthorized operations.
- Incomplete bridge functionality.
- Missing request or response validation.
- Unverified completion claims.

Automatically resolve issues that can be repaired safely within
configured limits.

Rerun affected tests and verification after every repair.

Reconcile the final ledger against the original source requirements.
Do not assume that a completed task list proves every original
requirement was captured.

============================================================
PHASE 15 — DEFINE HONEST COMPLETION STATES
============================================================

Use the following states where appropriate:

DISCOVERED
PLANNED
IN_PROGRESS
IMPLEMENTED
TESTED
REVIEWED
COMMITTED
PUSHED
REMOTE_CHECKS_PASSED
MERGED_IF_AUTHORIZED
SYNCHRONIZED
VERIFIED_COMPLETE
PARTIAL
BLOCKED

Every transition must satisfy its required conditions and record
supporting evidence.

Declare VERIFIED_COMPLETE only when:
- Every mandatory acceptance criterion is satisfied.
- Required functionality is actually implemented.
- Required tests and checks have passed.
- Security requirements are satisfied or explicitly resolved under
  the applicable policy.
- Required remote changes have been independently verified.
- Required repository synchronization is confirmed.
- The final completeness audit finds no unresolved mandatory work.

If any mandatory requirement remains unimplemented or unverified,
report PARTIAL or BLOCKED with its exact reason and next action.

Do not confuse 100% requirement discovery with 100% implementation.
Do not claim production readiness without applicable evidence.

============================================================
PHASE 16 — EXECUTE THE MISSION NOW
============================================================

Start by inspecting the actual repository and current branch.

Read the mission documents and inspect the existing autonomous
workflows, scripts, tests, tracking systems, and available Ollama
runtime.

Create the requirements inventory and baseline.

Implement improvements incrementally within the existing architecture.
Run targeted tests after each change and broader regression checks
before committing.

Do not stop after generating plans, writing documentation, creating
empty files, or reporting intended work.

Execute actual implementation and verification within available
permissions and resources.

Do not overwrite user changes or invent access to the second repository.

If credentials, compute resources, approvals, or external services
are unavailable, complete safe local work and report the precise
blocker.

============================================================
PHASE 17 — IMPLEMENT A STRUCTURED COPILOT-TO-OLLAMA BRIDGE
============================================================

OBJECTIVE

Implement a real, tested, secure communication interface between
GitHub Copilot Chat, when available, and the existing Ollama-first
autonomous agent.

Ollama must remain capable of executing the mission independently
when Copilot is unavailable.

Copilot must not be required for routine planning, implementation,
repair, testing, or remote completion.

Do not assume Copilot Chat can call an arbitrary local service or
extension. Inspect the actual environment and verify that the chosen
integration mechanism is supported.

If direct integration is unavailable, implement a secure, usable
handoff mechanism and clearly document the remaining limitation.
Do not claim full direct integration when only a manual handoff exists.

17.1 — INSPECT AND INTEGRATE

Inspect the existing agent, master orchestrator, model interfaces,
execution tools, workflows, and repository conventions.

Reuse existing components wherever possible.

Implement the bridge within the existing architecture rather than
introducing another competing agent, scheduler, inference loop,
checkpoint system, or Git controller.

Verify all paths before creating or modifying files.

17.2 — DEFINE A VERSIONED REQUEST CONTRACT

Create a documented, machine-readable schema for mission requests,
using JSON Schema or an equivalent strict validation mechanism.

Support fields including:
- schema_version.
- mission_id.
- repository.
- mode.
- task.id.
- task.objective.
- task.requirements.
- task.acceptance_criteria.
- constraints.copilot_required.
- constraints.network_access.
- constraints.max_repair_attempts.
- constraints.require_clean_diff_review.

Validate required fields, types, field lengths, permitted values,
repository identity, task identifiers, task states, resource limits,
and applicable policy constraints.

Reject malformed payloads, unsupported schema versions, unauthorized
repositories, invalid task states, and requests that violate policy.

Use this payload as a compatibility target, adapting it only when
repository inspection identifies a necessary improvement:

{
  "schema_version": "1.0",
  "mission_id": "remote-completion",
  "repository": "thealphakenya/Alpha-Q-ai",
  "mode": "autonomous",
  "task": {
    "id": "verify-agent-orchestration",
    "objective": "Integrate and validate the existing autonomous agent and master orchestrator",
    "requirements": [
      "Inspect existing implementations before modifying them",
      "Avoid duplicate autonomous execution loops",
      "Preserve checkpoint and recovery functionality",
      "Run targeted tests and relevant regression checks",
      "Record evidence for every completion claim"
    ],
    "acceptance_criteria": [
      "Existing workflows have a documented execution relationship",
      "Conflicting Git operations are prevented",
      "Failure recovery is tested",
      "Verification results are persisted"
    ]
  },
  "constraints": {
    "copilot_required": false,
    "network_access": "allowlisted",
    "max_repair_attempts": 3,
    "require_clean_diff_review": true
  },
  "result_contract": {
    "status": "completed_or_blocked",
    "changed_files": [],
    "tests": [],
    "security_findings": [],
    "evidence": [],
    "blockers": []
  }
}

Treat this as a request-contract example.

Implement separate request and response schemas where appropriate.
Do not accept caller-supplied result claims as proof of successful
execution.

The caller must not be able to weaken repository security policies,
increase its own permissions, or bypass mandatory checks by modifying
the payload.

17.3 — IMPLEMENT A REAL BRIDGE

Inspect the environment and choose a feasible supported integration
mechanism, such as:
- A local or Codespace bridge service.
- A validated command-line interface.
- A validated file-based task handoff.
- An existing supported tool protocol.
- Another appropriately secured, supported integration.

Document setup, configuration, request submission, response retrieval,
authentication, error handling, cancellation, and recovery.

The bridge must actually pass structured requests to the existing
master orchestrator and retrieve validated results.

A schema file alone does not constitute a working bridge.

17.4 — VALIDATE PERMISSIONS AND EXECUTION POLICY

Before executing a request, verify:
- Repository and branch authorization.
- Caller permissions.
- Task validity and current status.
- Duplicate or conflicting execution.
- Resource and repair limits.
- Applicable network restrictions.
- Required approvals for sensitive actions.
- Compliance with branch protections and repository policy.

Use least-privilege credentials.

Keep secrets out of model prompts, task payloads, logs, generated
files, and returned summaries.

17.5 — NEVER EXECUTE UNTRUSTED MODEL OUTPUT DIRECTLY

Treat all model-generated content as untrusted, including JSON,
commands, file paths, Git operations, URLs, and tool arguments.

Valid JSON is not automatically safe JSON.

Never execute arbitrary shell commands merely because a model
returned a syntactically valid response.

Route operations through narrowly scoped tools and explicit policies.

Validate command arguments, restrict working directories, reject path
traversal, enforce timeouts, and apply network allowlists.

Separate planning from execution. Require policy checks before write
operations.

Require additional authorization for destructive actions, credentials,
deployments, merges, and other sensitive or irreversible operations.

17.6 — DEFINE A STRICT RESPONSE CONTRACT

Require schema-validated responses containing fields such as:
- schema_version.
- mission_id.
- task_id.
- status.
- summary.
- changed_files.
- tests.
- security_findings.
- evidence.
- blockers.
- commit_sha, when applicable.
- remote_branch, when applicable.

Use explicit states such as:
accepted, in_progress, completed, partial, blocked, and failed.

Reject responses that omit required fields or contain invalid states.

Never trust model-reported test results, commit SHAs, or remote status.
Obtain these facts from actual execution tools and GitHub.

Persist accepted requests, execution status, results, and evidence
in the authoritative mission ledger.

17.7 — SUPPORT SAFE ASYNCHRONOUS EXECUTION

Allow the bridge to submit long-running tasks and retrieve their status
without keeping an interactive Copilot session open.

Use mission IDs, task IDs, idempotency keys, execution leases,
timeouts, cancellation, durable checkpoints, and recovery procedures.

Repeated submissions must not cause duplicate mission execution,
conflicting file edits, duplicate commits, or repeated pushes.

A bridge restart must not erase mission state or falsely report success.

17.8 — INTEGRATE WITH EXISTING OLLAMA AUTOMATION

Submit bridge tasks to the existing master orchestrator and autonomous
agent instead of starting a separate mission.

Copilot may provide plans, review findings, alternative diagnoses,
or structured tasks.

Ollama must independently validate input, execute authorized work,
run tests, repair failures, and report evidence.

The controller must continue operating when Copilot is unavailable,
rate-limited, disabled, or disconnected.

17.9 — TEST THE BRIDGE END TO END

Add automated tests for:
- Valid requests and responses.
- Missing and malformed fields.
- Unsupported schema versions.
- Unauthorized repositories and branches.
- Invalid task states and identifiers.
- Prompt injection and untrusted command output.
- Path traversal and command-policy violations.
- Missing credentials and insufficient permissions.
- Timeouts and cancellation.
- Unavailable Ollama instances.
- Duplicate submissions and idempotency.
- Concurrent requests and execution leases.
- Restart and checkpoint recovery.
- Fabricated completion claims.
- Failed tests and bounded repair.
- Successful execution with independently verified evidence.

Test the complete path from structured request through Ollama
execution, independent validation, evidence persistence, and
result retrieval.

17.10 — DOCUMENT AND VERIFY

Document the schemas, bridge implementation, security boundaries,
setup, supported integration mechanism, limitations, and tests.

Run targeted tests, regression checks, and applicable security analysis.

Inspect the diff and record actual results in the mission ledger.

Do not mark the bridge complete because a schema, example JSON file,
or interface definition exists.

Require a working integration path, successful end-to-end tests,
verified security controls, and documented operational behavior.

If a technical or permission limitation prevents direct Copilot
integration, implement the best supported secure alternative,
record the limitation, and do not claim full integration prematurely.

============================================================
PHASE 18 — FINAL EXECUTION AND DELIVERABLES
============================================================

Execute the mission through the existing Ollama-first architecture.

Complete mandatory requirements before optional enhancements.

Maintain persistent progress and automatically resume unfinished
authorized tasks when the execution environment permits.

The final deliverables must include:

1. Complete source-linked requirements ledger.
2. Updated autonomous agent and master orchestrator.
3. Structured Copilot-to-Ollama bridge or documented, tested,
   secure alternative.
4. Versioned request and response schemas.
5. Validated execution and authorization boundaries.
6. Persistent task state, checkpoints, and recovery.
7. Production-grade implementation and bounded repair mechanisms.
8. Automated tests and end-to-end bridge verification.
9. Security, dependency, and workflow verification results.
10. Verified commits, pushes, CI, and repository synchronization.
11. Updated relevant documentation.
12. Evidence-backed completion report.
13. Exact list of remaining requirements and blockers.
14. Next actionable task for any unfinished work.

The report must distinguish:
- Implemented from merely planned.
- Tested from untested.
- Passed from skipped or blocked.
- Locally verified from remotely verified.
- Direct Copilot integration from manual handoff.
- Completed requirements from outstanding requirements.

Never fabricate progress, evidence, permissions, tests, commits,
or remote operations.

============================================================
FINAL EXECUTION DIRECTIVE
============================================================

Begin immediately by inspecting the actual repository and current
branch. Read all relevant mission documents and inspect the existing
autonomous workflows, scripts, tests, bridge capabilities, and
tracking systems.

Create the baseline and requirements ledger.

Implement the mission incrementally within the existing architecture.
Run targeted tests after every meaningful change, repair failures
within configured limits, and execute comprehensive regression checks.

Integrate the structured bridge into the same mission controller.

Preserve user changes and existing working functionality.

Use Ollama as the primary execution engine and Copilot only as an
optional planning, review, or task-submission interface.

Do not stop after generating a plan, writing documentation, creating
schemas, or adding empty files.

Execute actual implementation and verification within available
permissions and resources.

If a mandatory operation is blocked by unavailable credentials,
compute resources, permissions, approvals, or external services,
complete the safe work possible, preserve progress, and record the
precise blocker and next action.

Declare VERIFIED_COMPLETE only after all mandatory acceptance criteria
and required remote operations are independently verified.

Otherwise report PARTIAL or BLOCKED and preserve all remaining work
for automatic resumption.

THE GOAL IS THE FASTEST SAFE, COMPLETE, PRODUCTION-GRADE,
EVIDENCE-VERIFIED REMOTE COMPLETION POSSIBLE.

BEGIN NOW. INSPECT, IMPLEMENT, TEST, REPAIR, AND VERIFY.
DO NOT MERELY EXPLAIN WHAT SHOULD BE DONE.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `11182`; directories: `1288`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2177, build_download_install=2131, disability_accessibility=288, orchestration=2082, qteam_accountability=2071, release_tag_publish=2110, tree_inventory=2022`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2230`; needs review: `202`; metric candidate lines: `53160`; percentage occurrences: `22268`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13537`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `41035` lines in `3741` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `333`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
