---
applyTo: "**"
---
Mission alignment: follow the canonical [latest mission](../../latest%20mission.md), synchronized byte-for-byte to [MISSION.md](../../MISSION.md) and its instruction-directory mirror. Mission phases are `PH01`-`PH18`; legacy requirement task buckets `M01`-`M16` remain distinct. This instruction set is subordinate to the mission and to the repository's remote-first evidence gate. Any merge, release, deployment, or protected action remains blocked until exact remote proof exists.

# Autonomous Agent Instructions

## Instruction coverage

- Before planning repository changes, read root `AGENTS.md`, `.github/copilot-instructions.md`, and every file under `.github/instructions`.
- Record relative path, applicable scope, byte count, SHA-256, and read/parse result. Never copy instruction source text into telemetry or public evidence.
- If an instruction is missing, unreadable, empty, malformed, or changes during a run, stop protected planning, write a checkpoint, and report the exact blocker.
- Inventory is not semantic proof. Map each applicable requirement to implementation, tests, workflows, docs, and remote evidence.
- Do not rewrite, delete, weaken, or self-approve policy instructions during routine automation. Update generated status/evidence only unless an authorized policy change explicitly requests a policy edit.

## Autonomous execution

- Automatically perform safe local and read-only work, validate focused changes, persist correlation IDs and checkpoints, and keep a prioritized resumable action queue for remaining gates.
- Bind remote jobs to repository, ref, and exact SHA. Dispatch only through target-owned workflows when the recorded authorization gate allows it; verify terminal results and remote refs independently.
- Bound retries, preserve failed evidence, and pause on missing authority, ambiguous API responses, unavailable sources, failed checks, or unresolved security findings. Never spin indefinitely or translate a queued action into success.
- Payments, transfers, payroll, trading, account/credential changes, releases, deployments, protected-branch changes, and Q-version finalization require their documented authority and evidence gates; agent confidence is not authorization.
- Production-marker matches are candidates, not proof of defects. Never bulk-rewrite minimal/stub/TODO matches across files or branches; map each to owner, intended behavior, focused tests, security/compatibility impact, rollback, and exact remote evidence before marking a replacement verified.
- Keep Codespace work metadata-first and low-bandwidth. Use target-owned workers for heavy validation and preserve local editing, Git, and Copilot workflows.
- Continue automatically across every remaining safe local mission task until the queue is exhausted or an external authority gate blocks a remote/protected action. Treat a blocked remote action as a recorded blocker, not as a reason to ignore the remaining work or silently mark the mission complete.
- Never skip, forget, or silently defer an in-scope mission item; each remaining requirement must be mapped to an owner, a concrete next action, and an evidence or blocker status in the mission ledger and checkpoints.

## Conceptual execution loop

- Route eligible work as a structured goal, constraints, dependencies, acceptance checks, and bounded resource/time budget through the verified local agent bridge to Ollama; preserve a human/Copilot reviewable diff.
- Keep planning, local execution, validation/repair, and result handoff as distinct evidence stages. Return the diff, actual tests, repair count, limitations, and next action to Copilot/developer; do not treat a proposed payload or an Ollama response as completion.
- If bridge/model availability, permissions, or resource limits are unknown, mark that step `NOT_MEASURED` or blocked and use only a safe, verified alternate path. Do not bypass existing authorization or remote verification gates.
- Measure payload completeness, local execution counts, repair iterations, validation outcomes, handoff completeness, and regressions per phase when instrumentation exists. Treat the concept note's quota/work-volume numbers as unverified claims, never as targets or progress.

## Credential and continuation contract

- On GitHub credential tasks, read the latest `or.md`, `oe2.txt`, `remotecompletion.md`, `githubapp.md`, `github.md`, `githubapppermissions.md`, and `CREDENTIAL_READINESS.md` before acting; treat dated prior chat summaries as pointers, not current proof.
- Carry forward user requirements only when they are explicit in the active request or recorded in current repository evidence. Preserve newer user edits and reconcile conflicts in favor of the newest instruction without claiming cross-session memory that is not actually available.
- Secret-variable presence is not authentication. Distinguish Codespaces secrets, Actions secrets/variables, user tokens, and App installation tokens. Never print, persist, or place secret values in prompts, evidence, commands, or workflow summaries.
- Do not authentictate with an App key marked compromised until the owner confirms revocation/rotation and replacement. App permission snapshots are reported configuration until independently verified; use least privilege and short-lived tokens.
- QMOI may inventory names, prepare setup checklists, and validate through authorized read-only endpoints. It must not invent or self-issue provider credentials, alter accounts, or claim readiness when external ownership, authorization, or verification is missing.

## QAUDITS-driven execution

- Use QAUDITS as a resumable evidence coordinator, not an unrestricted autonomous executor. Each work item must retain its owner/scope, prerequisites, correlation ID, repository/ref/SHA, status, measured duration, artifact references, coverage counts, omissions, blockers, and next action.
- Keep the current phase budget and live time accounting synchronized in `oe2.txt` and `remotecompletion.md`; if a mission checkpoint changes date or phase scope, update the recorded time and status in the same pass.
- Prioritize bounded shards by risk and dependencies; parallelize only independent work with isolated outputs and deterministic aggregation. Preserve failed shards and checkpoints, cap retries, and report the exact uncovered remainder.
- Refresh the supported paired `oe2.txt`/`remotecompletion.md` checkpoint and JSON/JSONL evidence after audit operations. Keep local validation distinct from remote validation and do not claim complete coverage for unreadable, skipped, ignored, or out-of-bound inputs.
- Continue automatically only for safe local or read-only tasks. Remote mutations, releases, deployments, protected changes, and finalization remain authority-gated; remote completion requires a terminal target-owned result and independently verified exact repository/ref/SHA/tree evidence.
- QAUDITS metrics and sentence checks are candidate/integrity signals. They cannot certify semantic truth, production readiness, or that months/years of work were completed in minutes; preserve human review and explicit blockers.
- Every `audit-inventory` run refreshes the complete materialized Markdown category index, finance catalog, `FINANCIALMANAGER.md` managed evidence section, and finance candidate inventory. Include currencies/amounts, revenue, payment/transfer, wallets/banking, deals, employment/payroll, country/jurisdiction, project budgets, and financial security; store no raw amounts, account identifiers, credentials, or source prose.
- Treat all finance category hits as overlapping keyword candidates. Missing currency/country lists, unreadable/oversized/untracked paths, provider evidence, owner mappings, tests, legal review, or exact-SHA results stay explicit blockers. Never initiate or imply authorization for financial actions.
- Write a paired `IN_PROGRESS` checkpoint before long inventory work and finalize it under the same correlation ID; an interrupted run must remain explicitly in progress, not inherit a prior passing status.
- Measure each long audit phase and avoid duplicate full-tree passes when a deterministic per-run result can be reused. If a local scan makes no measurable progress, stop it gracefully, preserve its checkpoint as incomplete, and resume in a fresh bounded run; never report the interrupted run as complete.
- Reuse CodeQL metadata from an already-fetched exact-SHA workflow response only. Do not dispatch duplicate analysis, and do not treat CodeQL success or unavailable alert data as overall completion or a clean security result.

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

## Mission roadmap

- Follow the canonical [root mission](../../MISSION.md) and its instruction-directory mirror. The mission defines task mapping, bounded resumable execution, measured evidence, and completion gates; it does not override this policy or authorize remote/protected operations.

## Two-hour mission monitoring

- Use stable phase IDs `PH01`-`PH18` for the canonical mission and retain `M01`-`M16` only for the existing requirement-task ledger. Track phase status, actual UTC start/finish, elapsed seconds, retries, acceptance evidence, blockers, dependencies, and next action in the latest machine checkpoint.
- Record phase/task transitions using the same correlation ID in `oe2.txt`, `remotecompletion.md`, `remote-completion.json`, and `remote-evidence-ledger.jsonl` via the supported checkpoint writer. Use monotonic timing only while the process is live; mark continuity unavailable after restarts.
- Use `python -m scripts.mission_task_ledger phase-start PHASE_ID`, `phase-finish PHASE_ID`, `start Mxx`, and `finish Mxx` for task/phase transitions; the helper enforces ledger schema, branch matching, dependency readiness, bounded locks, and evidence-backed completion.
- Keep implementation, test, remote-CI, and production verification metrics distinct. Do not infer completion from time budgets, counts, or attempted work.
- At the 120-minute boundary, preserve unfinished work and concrete resume actions. Claim autonomous continuation only after a separate run has actually loaded and resumed the saved checkpoint.
