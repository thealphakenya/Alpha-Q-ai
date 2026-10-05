# Q Version Manager

## Purpose and authority

`scripts/q_version_manager.py` owns canonical `Q.0.0.N` parsing, collision-resistant reservations, pair verification, and final repository metrics. `scripts/autonomous_completion_engine.py` uses it for read-only latest-version discovery and audit. Evaluation and local validation never create a final Q artifact or claim remote completion.

A final version is written only by `write_final_metrics()` after the caller supplies terminal target-owned workflow success, independently verified exact SHAs for both target repositories, passed checks, clean local trees matching those SHAs, a workflow run ID, and a correlation ID. The manager checks those inputs and records them; it does not authenticate to GitHub or independently verify a caller-supplied claim. The target workflow remains responsible for producing trusted evidence.

## Canonical autonomous lifecycle

The Q-version lifecycle is the contract for the fully autonomous Ollama agent. These are the required stage names and the order they must be recorded in:

1. `MERGE_START`
2. `PRE_MERGE_INVENTORY`
3. `INSTRUCTION_INVENTORY`
4. `INTERNAL_RESEARCH`
5. `EXTERNAL_RESEARCH`
6. `REPOSITORY_SURFACE_AUDIT`
7. `OLLAMA_FULL_COVERAGE_AUDIT` (`OFCA`)
8. `MARKDOWN_SOURCE_INDEX`
9. `UI_TEST_HOOK_COVERAGE`
10. `MERGE_PLAN`
11. `MERGE_APPLY`
12. `POST_MERGE_AUDIT`
13. `POST_AGENT_MERGE_PLAN`
14. `POST_AGENT_MERGE_APPLY`
15. `POST_AGENT_MERGE_AUDIT`
16. `PRODUCTION_SCAN`
17. `PRODUCTION_REPLACEMENTS`
18. `PRODUCTION_READINESS`
19. `FULL_VALIDATION`
20. `REMOTE_VERIFICATION`
21. `QMOI_RESTORE_POINT`
22. `AUTO_CONTINUE_LOOP`
23. `AUTONOMOUS_COMPLETION`
24. `Q_VERSION_FINALIZATION`

This sequence covers the complete unattended control loop: branch-safe inventory, policy-instruction validation, research, Markdown coverage, repository surface audit, OFCA pre-merge safety, merge execution, production gap review, validation, UI/test-hook mapping, remote exact-SHA proof, bounded auto-continue execution, final autonomous completion, and only then Q.0.0.N finalization.

Every stage is a fail-closed gate. If a required stage is missing, blocked, or unsupported by exact remote evidence, the agent must record the blocker and continue only in read-only or resumable mode; it must never claim final completion without terminal target-owned workflow proof.

The live GitHub verifier and the Q-version lifecycle are designed to operate as a single remote completion contract. Every lifecycle stage above is evaluated as part of the same sequential evidence chain, and `QVersionManager.verify_remote_completion_gate()` blocks finalization unless the lifecycle is complete and the live verifier reports `READY` with verified auth, a matching local/remote SHA, branch-protection verification, and a successful workflow run for the exact remote SHA. This makes the stage chain and the remote proof mutually reinforcing rather than separately optional.

The merge pipeline records instruction inventory, repository surface audit, OFCA, Markdown indexing, and UI/test-hook coverage. The validation pipeline records production scan/replacement/readiness, full validation, remote verification, the `QMOI_RESTORE_POINT`, and the deterministic autonomous-completion verdict. The restore point is a separate `qmoi` branch in both repositories, created or fast-forwarded only after a target-owned workflow verifies both `main` and `autosync-backup` at the same exact SHA. It snapshots the last committed workspace tree before the next agent cycle; it never imports dirty or ignored files. `oe2.txt` and `remotecompletion.md` must be present at that SHA. Git does not store empty directories. The repository variable `QMOI_BRANCH_PUBLICATION_AUTHORIZED=true` is an explicit publication gate; absent authorization or evidence, the stage remains `NEEDS_REVIEW`. A local validation invocation is not itself an auto-continue run and has no terminal remote workflow proof, so those stages remain `NEEDS_REVIEW` until their owning execution paths supply evidence. The bounded continuation driver records its actual iteration count and retry limit; only a successful success-contract termination within that limit passes `AUTO_CONTINUE_LOOP`.

The agent's local success summary is an unversioned report at `ollamatracks/completion_reports/<execution-id>/COMPLETION.md`. It is not a Q artifact. Only the Q-version manager's evidence-gated finalization path may allocate `Q.0.0.N` directories and companion documents.

Finalization requires exactly two distinct repository roots and evidence keys matching those roots; publication verification also rejects missing, extra, or single-repository evidence. Lifecycle records are schema-checked in addition to hash-chain-checked. The latest stage attempt controls status, and the final `AUTONOMOUS_COMPLETION` record must match the supplied completion execution, gate map, and empty action queue. A passing `AUTO_CONTINUE_LOOP` record must show successful termination within its recorded retry bound. Instruction verification independently requires regular, non-symlinked `AGENTS.md`, `.github/copilot-instructions.md`, and `.github/instructions/` sources, valid nonempty UTF-8 content, and matching `applyTo` scope, byte count, and hash.

## Autonomous agent responsibilities covered by Q-version and OFCA gates

The agent is required to perform all of the following without human prompting:

- inventory the repository root, policy files, and instruction sources before protected work
- refresh and validate the Markdown source index across materialized files and refs
- complete the repository surface audit for Markdown, API, endpoints, routes, ports, automation, links, components, tree, style, universals, QVillage/QVS, comparison, Qtrade, percentages, production gaps, and memory
- run `OFCA` as the required pre-merge checkpoint immediately before merge activity
- verify merge decisions, conflict handling, and post-merge audit follow-up
- scan production gaps and replacements before final validation
- confirm production readiness with zero unresolved candidates and zero unreadable/oversized files
- validate all required tests and markdown coverage with exact repo state checks
- prove UI/style/universal coverage with stable IDs, hook applicability review, and event-driven test mapping
- keep the agent in a bounded `AUTO_CONTINUE_LOOP` until success or the retry limit is reached
- finish with `AUTONOMOUS_COMPLETION` only when every gate passes and the queue is empty
- preserve Q.0.0.N finalization as a repository artifact gated by exact remote SHA and workflow evidence, never as a local-only claim

For local, non-finalizing inventory refresh, run `python scripts/ollama_autonomous_agent.py audit-inventory --base-path <repository-root>`. This refreshes local research/surface, production, OFCA, feature-test-hook/style-universal, and instruction inventories, with external fetching disabled. It is diagnostic only: it does not merge, dispatch, publish, verify remote history, or promote `NEEDS_REVIEW` to `PASS`. Its JSON summary and generated manifests must be reviewed before planning any remediation; finalization still requires the complete lifecycle and terminal remote evidence above.

## Restore point automation safeguards

The target-owned autosync workflow may advance `main` and `autosync-backup` through its existing fast-forward-only contract, but it may publish `qmoi` only after a terminal successful Ollama agent run is independently checked. A push event, schedule, dispatch acceptance, nonempty secret, local test, or agent success file by itself is not a restore-point authorization.

The four branch roles are distinct: `main` is the default development/promotion ref; `autosync-backup` is the first fast-forward staging ref; `qmoi` is the post-success restore point; and `master` is a fast-forward-only mirror of the validated `main` tip used for parity/recovery checks. Git `master` is not an independent development branch and does not replace `main` as the default branch or `qmoi-enhanced` as the policy/master repository. Cross-repository audit evidence includes a machine-readable `master_branch_plan` with this operating policy.

The restore-point implementation enforces these safeguards:

1. Require exactly two distinct repository checkouts and a valid exact candidate SHA.
2. Require clean checkouts and candidate objects available in both repositories.
3. Require both repositories' `main`, `autosync-backup`, and `master` refs at the candidate SHA before restore publication.
4. Require candidate trees to match across repositories and refuse non-fast-forward `qmoi` or `master` updates.
5. Require `oe2.txt` and `remotecompletion.md` at the candidate SHA and record their SHA-256 values.
6. Require a completed Ollama workflow whose head repository is the trusted current repository and whose default-branch run has successful agent execution, repository tests, final validation, hosted-link validation, and final health gate.
7. Bind the completion evidence to the workflow run ID and source SHA; require that source SHA to be an ancestor of the candidate in both repositories.
8. Permit first-run bootstrap only when both `qmoi` and `master` refs are absent and all `main`/backup refs equal the hosted checkout; permit master migration only when `qmoi`, `main`, and backup already agree. Both require readable docs/tree and `QMOI_BRANCH_PUBLICATION_AUTHORIZED=true`.
9. Block one-sided, stale, divergent, or partially missing refs; bootstrap is never a repair path for mismatched branches.
10. Re-read `main`, backup, `qmoi`, and `master` immediately before publication to detect preflight-to-push ref drift.
11. Re-read and verify all four refs after each repository publication; record per-repository SHAs, tree, action, and verification result.
12. Preserve partial publication as `BLOCKED_PARTIAL`; never force-push or silently roll back a valid remote ref.
13. Keep ordinary push/scheduled sync independent from restore publication; without terminal agent evidence it records `SKIPPED_NO_VERIFIED_AGENT_SUCCESS` and does not create `qmoi`. Routine promotion still advances master from main when fast-forward-safe.
14. Record a correlation ID, UTC timestamp, workflow identifiers, authorization state, blockers, and resumable next action without recording token values.
15. Prefer the user-reported `MY_CUSTUOM_TOKEN` Actions secret and accept `MY_CUSTOM_TOKEN` as a compatibility alias; secret presence is not proof of validity, scope, or branch authorization.

These local contracts and workflow definitions do not prove that either remote currently has aligned refs or that a workflow actually passed. Q-version finalization still requires terminal artifacts and independent exact-SHA verification for both repositories.

## Required Q.0.0.N artifact contracts

Q.0.0.N is not a shortcut to completion; it is the final evidence archive for the autonomous system. A materialized version must include:

- `Q.0.0.N/REPOSITORY_METRICS.json`
- `Q.0.0.N.md` companion summary
- instruction inventory and hash proof for every applicable repository
- the source-manifest hash for repository and OFCA coverage
- production-readiness, UI-hook, and remote-verification results
- the autonomous completion gate map with zero pending actions
- terminal `qmoi` restore-point evidence showing both repositories' `qmoi`, `main`, and `autosync-backup` refs at their exact verified SHAs
- terminal `master` mirror evidence for both repositories at the same exact final SHA and tracked tree
- exact final SHAs and workflow IDs from target-owned success evidence

The companion files are generated only after the terminal workflow result is successful and the repository tree is clean and matched to that exact SHA. They must not overwrite an existing Q-version artifact or be used to mask missing remote evidence.

## Implemented enhancements

1. Canonical full-match parsing rejects malformed names, suffixes, leading-zero identifiers, and non-positive versions.
2. Artifact discovery is separate from reservation discovery, so an unmaterialized reservation is not reported as an existing completion.
3. Multi-root discovery deduplicates canonical paths and checks every explicitly supplied repository root.
4. Corrupt, unsupported, inconsistent, or checksum-mismatched reservation state fails closed instead of silently reusing a number.
5. Reservation records carry a schema version, UUID, UTC timestamp, prior counter, source roots, and integrity checksum.
6. Exclusive mode-`600` lock files serialize competing reservations; a pre-existing lock is preserved and reported as busy.
7. Reservation publication uses a same-directory temporary file, file `fsync`, atomic replacement, and best-effort directory `fsync`.
8. Pair verification reports directory and companion-document presence separately for each repository.
9. Filesystem metrics include every non-`.git` file and directory, per-file byte counts and SHA-256, symlink-target hashes, and read errors.
10. Git HEAD and worktree cleanliness are recorded alongside filesystem metrics; unavailable Git state never becomes a verified clean state.
11. Final metric writing requires a successful terminal workflow and matching clean local/remote SHA evidence for every supplied repository.
12. Existing Q-version directories or companion files are never overwritten during finalization.
13. Each repository receives `Q.0.0.N/REPOSITORY_METRICS.json` and `Q.0.0.N.md` with file, directory, byte, SHA, workflow, and correlation evidence.
14. Self-referential metric JSON and its companion Markdown are explicitly excluded from their own tree hash inventory; the manifest records that exclusion.
15. Audit output separates latest materialized version, highest reserved/discovered number, reservation integrity, pair status, and per-root source paths.
16. Instruction inventories hash applicable `AGENTS.md`, Copilot instructions, and every file under `.github/instructions` for each target; they record scope and read errors without persisting instruction source text.
17. Q-version finalization compares reported instruction paths, byte sizes, and hashes against both exact repository trees and rejects missing, unreadable, malformed, or tampered instruction evidence.
18. Autonomous completion evidence includes ranked next actions, current-state refresh, local evidence JSON/JSONL integrity results, and an explicit authorization state for every pending action.
19. Production-gap scanning is a scoped candidate inventory, not a blanket replacement engine: it records file hashes and marker line numbers, makes dependency/cache/history/build exclusions and unreadable/oversized coverage gaps explicit, and queues candidates as `discovered_unmapped` until owner, implementation, focused tests, security impact, rollback, and remote proof are supplied.
20. Final metrics require a `CLEAR` production inventory with complete scan coverage, zero candidates, zero unreadable files, and zero oversized files skipped; unresolved candidates keep production and Q-version gates blocked.
21. Every merge lifecycle runs the Ollama Full Coverage Audit (OFCA) after source inventory and immediately before merge activity. It records path/hash/line-number responsibility metrics from materialized files and local ref history, marks `prMergeIncluded`, and blocks completion when remote refs, PRs, or intermediate commit trees lack target-owned exact-SHA evidence.
22. Every internal-research lifecycle runs the repository-surface audit for Markdown, API, endpoint, route, port, automation, link, component, tree, styles, universals, QVillage/QVS, comparison, Qtrade, percentages, production gaps, and memory. It records per-file hashes, structural/content metrics, exact metric/percentage locations, local refs, research-topic coverage, and explicit exclusions; finalization requires terminal exact-SHA evidence for both repositories and all required domains.
23. Every styles/universals registry feature requires a stable ID, focused test mapping, and reviewed hook/webhook applicability; event-driven features require passing delivery/security/recovery tests before finalization.

## Unattended completion and instruction coverage

The autonomous agent must inventory and read the repository's root `AGENTS.md`, `.github/copilot-instructions.md`, and the `.github/instructions/` directory before it plans protected repository work. All three required sources must exist. Every regular instruction file is included; empty, unreadable, malformed, or symlinked instruction sources fail the gate. Each inventory record contains only the relative path, `applyTo` scope when present, byte count, and SHA-256. The inventory does not copy instruction text into logs or ledgers, and the finalizer compares every path, byte count, and hash against each exact repository tree.

Instruction inventory proves which policy files were read, not that every natural-language requirement was semantically implemented. The agent must map requirements to owning code, tests, workflows, documentation, and exact remote evidence. It may update generated status sections and evidence artifacts, but it must not rewrite, delete, weaken, or self-approve policy instructions as part of routine automation.

Production readiness follows the same evidence boundary. `production.md`, `productionenhanced.md`, and `ollamatracks/production_gap_inventory.json` must distinguish scanned candidates from reviewed defects, approved plans, implemented changes, tested replacements, and remotely verified production status. Marker matches in prose, tests, generated state, historical snapshots, virtual environments, or build outputs are not proof of non-production code. A blanket rewrite across every directory or branch is not an authorized operation; changes proceed in bounded file groups with ownership, compatibility, security, test, rollback, and exact-SHA evidence.

Each completion evaluation refreshes `ollamatracks/current_state.json`, validates available local JSON/JSONL evidence, and writes a priority-ordered resumable action queue for every non-passing gate. Safe local/read-only work can proceed automatically. Remote dispatch/publication, cross-repository promotion, releases, deployments, credential changes, financial activity, and Q-version finalization stay blocked until their explicit authorization and evidence requirements pass. Retries must be bounded and checkpointed; inaccessible or failed remote services are recorded as blockers rather than retried indefinitely or treated as success.

The agent must not claim equivalence to Copilot Chat or human judgment merely because it can inventory instructions or generate a queue. A final `Q.0.0.N` requires a terminal `SUCCESS` or `NO_CHANGES_REQUIRED` completion result, every required gate `PASS`, zero queued actions, valid instruction inventories for both repositories, a complete production scan with zero candidates, exact clean remote SHAs, and terminal target-owned workflow evidence.

The required `ollama_reference_audit` gate inventories Ollama-mentioned source and documentation files with paths, hashes, line numbers, and responsibility categories while excluding source text from evidence. Finalization additionally requires target-owned terminal evidence for both repositories covering every current ref, pull request, and intermediate commit tree at the exact final SHAs. A local scan of `qmoi-enhanced-history-14`, snapshots, or the current checkout cannot satisfy remote-history completeness by itself.

The `ui_test_hook_coverage` gate uses `ollamatracks/feature_test_hook_coverage.json` to track stable feature IDs, test paths, reviewed hook applicability, and event-driven hook tests. Static style features may record a reviewed not-applicable hook decision; event-driven features require tested authentication, denial, delivery, retry/idempotency, and recovery behavior. Unmapped rows block Q-version finalization.

## Q seed lineage

The seed feature is the initial Q capability set, not a claim that every feature is implemented. Each accepted seed revision should record:

- stable `seed_id`, parent seed/version, source repository and exact source SHA;
- a content SHA-256 for the seed manifest, never secret or credential values;
- feature identifiers, owning paths, dependencies, and their separate states: specified, implemented, tested, remotely verified, or blocked;
- tests and validation artifacts, migration/rollback notes, and compatibility constraints;
- a change reason and human/automation authorization reference.

Seed changes are additive by default. Removing or replacing a seed capability requires provenance, compatibility tests, and explicit review. A Q version may not turn a seed requirement into implementation evidence merely because the feature appears in a manifest.

## Repository metrics contract

The metrics JSON stores one record per included path with path, kind, byte length, and SHA-256, plus the complete directory list, aggregate counts, total bytes, exact repository SHA, clean-worktree state, workflow run ID, terminal conclusion, timestamp, and correlation ID. `.git` internals are excluded; no other filesystem path is silently filtered. Unreadable paths make the inventory blocked. Generated self-referential outputs are named in the exclusion list.

The companion Markdown reports per-repository counts and points to the complete path-level JSON. A final dual-repository version requires both trees and both companion documents. A local snapshot, a passing unit test, a dispatch response, or a reserved number cannot satisfy this gate.

## Markdown, history, and PR coverage relationship

The merge inventory scans every ref present in the local Git object database, including fetched `refs/pull/*` and tags, and batch-reads every distinct Markdown blob for UTF-8, heading, code-fence, unresolved-marker, and same-ref local Markdown-link checks. Per-ref records retain source/ref, path, bytes, lines, Git object ID, content SHA-256, validation checks, and outcome. Materialized Markdown uses the same validator. Any invalid or unreadable document remains `needs-review` or `content-unavailable`; inventory generation alone is not a pass.

The local ref scan does not enumerate every intermediate commit tree, remote ref freshness, every remote PR, private/inaccessible sources, or future content. Final completion requires the separate `markdown_inventory` gate to carry target-owned evidence for both repositories: all current refs, every PR and intermediate commit tree, all Markdown content validated, zero unavailable sources, terminal successful workflows, and exact final SHAs. These sources remain explicit blockers until that evidence exists.

“Future” means later commits and PRs as they become available; no audit can attest to not-yet-created content. Remote PR lists, changed-file manifests, refs, and terminal checks must be refreshed by authorized target-owned workflows for both repositories. `ALLMDFILESREFS.md` must distinguish current files, materialized snapshots, fetched refs, target-verified remote history, duplicates, and inaccessible sources rather than presenting a single unqualified total.

## Autonomous dual-repository publication flow

The Q-version manager is designed to support the autonomous update contract for both Alpha-Q-ai and qmoi-enhanced. The allowed flow is:

1. local validation and merge inventory pass on the current branch
2. backup branch publication and audit pass on `autosync-backup`
3. exact SHA verification and fast-forward safety check for both repos
4. Q.0.0.1 directory creation on each final branch only after the target-owned remote workflow concludes successfully
5. final main-branch promotion after backup/publication evidence is current and consistent
6. final SHA reconciliation, ledger write, and exact branch publication validation

A valid Q version is a repository artifact, not a substitute for branch authorization. The manager records the evidence but does not invent remote completion. It accepts a version only when the caller supplies terminal success, exact remote SHAs, clean local state, workflow run IDs, and correlated lifecycle evidence.

The same contract applies to additional repo instances that follow the autosync model: branch-level publication is performed on backup first, then main, with the same SHA check and ledger gate. The automation must never force-push, overwrite an existing Q-version artifact, or claim success without terminal workflow evidence.
The final metrics JSON also captures both repositories' instruction-inventory hashes and the terminal autonomous-completion gate map/action queue. The companion summary reports instruction-file counts and must state that the pending action count is zero; it may not summarize an unfinished queue as complete.

After a successful dual-repository main/backup update, the target-owned `cross-repo-autosync.yml` workflow creates or fast-forwards `qmoi` in both repositories to the same exact commit and tree. This is a restore point for the last completed workspace before the next agent cycle, not a working branch. It requires `QMOI_BRANCH_PUBLICATION_AUTHORIZED=true`; if unset, if either repository is not synchronized, if `oe2.txt` or `remotecompletion.md` is absent at the candidate SHA, or if an existing `qmoi` ref is not fast-forwardable, publication blocks without force-pushing. Git tracks files and nonempty directories only; ignored/uncommitted files and empty directories are not included.

## Q.0.0.1 creation and companion artifacts

The first materialized Q-version directory after the policy gate is `Q.0.0.1`. It must be created in the final branch state of each repository only after the evidence gate is satisfied. Preparation requires terminal `SUCCESS` or `NO_CHANGES_REQUIRED`, every required completion gate `PASS`, an empty pending-action queue, complete instruction inventories for both repositories, exact clean remote SHAs, and terminal target-owned workflow evidence. The directory should include:

- `Q.0.0.1/REPOSITORY_METRICS.json`
- `Q.0.0.1.md` companion summary
- any required lifecycle and sync records created by the branch publication flow
- per-repository instruction inventory and hash evidence embedded in `REPOSITORY_METRICS.json`
- complete dual-repository Ollama reference audit and source-manifest hash embedded in `REPOSITORY_METRICS.json`
- complete styles/universals test-hook coverage manifest with exact-SHA evidence embedded in `REPOSITORY_METRICS.json`
- the terminal autonomous-completion gate map and empty pending-action queue embedded in `REPOSITORY_METRICS.json`
- the complete production inventory summary with zero candidate files, unreadable files, and oversized skipped files
- instruction-file count in the companion Markdown summary; no instruction source text or secret values

This directory is a final artifact, not an everyday working directory. It is not an excuse to keep stale or fabricated research data around. The live repo content stays sanitized; the version artifact remains the archive of accepted evidence and completion state.

## Validation and current limitations

Focused tests cover strict parsing, cross-root discovery, reservation integrity and locking, pair metrics, per-file hashes, finalization blockers, exact-SHA finalization, and dirty/mismatched tree rejection. Local tests prove these deterministic contracts only.

Current remote completion remains blocked by unverified GitHub App key rotation, HTTP 403 branch-protection reads, failed earlier-SHA tracker/autosync runs, and local branch divergence. No final Q version was created by this continuation. Remote completion and final repository metrics remain pending independently verified target-owned evidence.

<!-- BEGIN QMOI MANAGED: ollama-reference-audit-gate -->
## QMOI reference audit and Q-version gate

This generated audit indexes paths, hashes, line numbers, and responsibility categories only; source text is never copied into the evidence artifact.

- Materialized files scanned: `10397`; QMOI-matching files: `4129`.
- Local scan status: `PASS`; historical source scopes are listed in `QMOItracks/QMOI_reference_audit.json`.
- Local tree and archived source scans do not cover every remote ref, pull request, or intermediate commit tree; Q-version completion stays blocked until both repositories have terminal exact-SHA audit evidence.
- Styles and universal UI requirements remain incomplete until each registered feature maps to focused tests and event-driven hook/webhook validation; registry discovery is not coverage proof.
<!-- END QMOI MANAGED: ollama-reference-audit-gate -->

## OFCA lifecycle evidence

`OLLAMA_FULL_COVERAGE_AUDIT` is a required lifecycle stage between source inventory/research and merge activity. It records local file/ref/commit counts, mention-bearing path counts, a source-manifest SHA-256, `prMergeIncluded`, and any remaining remote-history blocker. Local scans do not establish remote branch, PR, or intermediate-tree completeness. The stage remains `NEEDS_REVIEW` until target-owned evidence proves complete coverage at the exact repository SHA; merge application is blocked while OFCA or the Markdown source index is incomplete.

Style/universal migration candidates are tracked in `ollamatracks/style_universal_replacement_inventory.json` with path, hash, affected directory, source scope, and required test/hook review. This inventory is a plan only: it does not authorize bulk replacement or claim coverage from discovery.

## Repository surface audit gate

Internal and external research share `ollamatracks/repository_surface_audit.json`. The artifact records each accessible materialized path and hash, Markdown byte/line/word/heuristic-sentence counts, UTF-8/heading/fence/local-link checks, API/route/component/workflow/tree counts, QVillage/QVS scope, comparison and Qtrade metric candidate lines, and percentage tokens by path/line. It stores no source prose. Heuristic sentence counts are not semantic validation; each requirement still needs source/test ownership evidence. Remote refs, PRs, and intermediate trees require target-owned exact-SHA manifests for both repositories. Incomplete coverage remains a blocker and no candidate scan authorizes a bulk production replacement.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10413`; directories: `1267`; Markdown: `2413`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Markdown structural checks passed: `2186`; needs review: `219`; metric candidate lines: `46842`; percentage occurrences: `22236`.
- Formula/calculation candidate lines: `11373`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `36455` lines in `3093` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `285`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: project-autoproject-coverage -->
## Project and AutoProject coverage

The autonomous repo engine treats project and autoproject state as first-class operational evidence and keeps its registry, lifecycle, financial, and production surfaces synchronized with the current repository state.

- Master and sister roles may configure bank accounts, wallets, payment APIs, and project-linked payment destinations for autonomous project and autoproject execution.
- Public and authenticated users do not receive these administrative configuration controls without separate authorization and explicit policy approval.

- projectsandautoprojects.md: project automation contract
- projectsandautoprojectsenhanced.md: project automation contract
- QVERSIONMANAGER.md: Q Version Manager; Purpose and authority; Canonical autonomous lifecycle; Autonomous agent responsibilities covered by Q-version and OFCA gates; Required Q.0.0.N artifact contracts; Implemented enhancements
- production.md: production.md; Required replacement policy; Files flagged for production replacement; Agent-managed production inventory; Required replacement policy; Unmapped production candidates
- productionenhanced.md: productionenhanced.md; Production replacement policy; Enhancements; Files addressed; Agent-managed production inventory; Production replacement policy
- bankandbankaccounts.md: Agent Automation Status
- FINANCIALMANAGER.md: QMOI Financial Manager; Purpose; Operating principles; Core finance objectives; Wallet and account model; Financial layers
- QMOI_MODEL_CARD.md: QMOI Model Card; Overview; Applications; QMOIAIUI; QCity; QMOI Space
- QVILLAGE.md: QVILLAGE.md; Active automation
<!-- END QMOI MANAGED: project-autoproject-coverage -->
