# Q Version Manager

## Purpose and authority

`scripts/q_version_manager.py` owns canonical `Q.0.0.N` parsing, collision-resistant reservations, pair verification, and final repository metrics. `scripts/autonomous_completion_engine.py` uses it for read-only latest-version discovery and audit. Evaluation and local validation never create a final Q artifact or claim remote completion.

A final version is written only by `write_final_metrics()` after the caller supplies terminal target-owned workflow success, independently verified exact SHAs for both target repositories, passed checks, clean local trees matching those SHAs, a workflow run ID, and a correlation ID. The manager checks those inputs and records them; it does not authenticate to GitHub or independently verify a caller-supplied claim. The target workflow remains responsible for producing trusted evidence.

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

- Materialized files scanned: `10384`; QMOI-matching files: `4125`.
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

- Status: `NEEDS_REVIEW`; materialized files: `10408`; directories: `1267`; Markdown: `2412`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Markdown structural checks passed: `2186`; needs review: `218`; metric candidate lines: `46823`; percentage occurrences: `22236`.
- Formula/calculation candidate lines: `11364`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `36263` lines in `3090` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `285`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
