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
16. The ordered lifecycle begins `MERGE_START` -> `ALL_BRANCH_INVENTORY` -> `PRE_MERGE_INVENTORY`; a missing or incomplete branch roster is `NEEDS_REVIEW` and cannot produce final Q metrics.
17. Final Q manifests preserve the exact branch names, tip commit/tree SHAs, roles, roster capture time, source report SHA-256, and normalized branch-inventory SHA-256 for both repositories.

## Branch inventory and Q-version lifecycle

The Ollama agent records `ALL_BRANCH_INVENTORY` immediately after `MERGE_START`
and before pre-merge planning. A valid target-generated cross-repository report
must state that every remote `refs/heads/*` was fetched and provide a unique
name, commit SHA, and tree SHA for every branch in both repositories, plus one
alignment/disposition entry per branch name. The report must carry the target
Actions run ID, repository, ref, and exact head SHA. Each repository roster must
include `main` and `autosync-backup`; the report is bound to its capture time
and SHA-256. The agent accepts that report through
`--branch-inventory-report <path>` and records the normalized roster and
validation result in the hash-chained lifecycle ledger.

When no target-generated report is supplied, the agent records locally
available refs as discovery evidence and marks `ALL_BRANCH_INVENTORY`
`NEEDS_REVIEW`. Local branch names or stale remote-tracking refs never satisfy
the remote inventory gate. Feature, fix, security, release, Dependabot,
Codespaces, and legacy branch names are preserved in the roster; only the
protected backup-first/main-after-gates lane can publish automatically. Other
branches remain PR/review-only and are not implicitly copied or merged.

`write_final_metrics()` refuses Q.0.0.N output unless the complete branch stage
passed and the caller supplies the same normalized inventory SHA-256 alongside
terminal workflow evidence. For each repository, the `main` report tip must
match the prepared source SHA and the `autosync-backup` report tip must match
the separately supplied verified backup SHA. Each `REPOSITORY_METRICS.json`
contains the full per-repository branch roster and dispositions, while the
companion document gives the total count and digest. Q-version finalization
therefore records the exact branch population that was considered before merge
and publication; it does not imply that every branch was merged or that
undiscovered future refs were audited.

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

1. start merge activity, enumerate every current branch in both repositories, and record exact tips before other planning
2. pass local validation and the merge inventory for the current branch set
3. publish or validate `autosync-backup` first, using only exact-SHA fast-forward checks
4. verify required checks and branch coverage against exact SHAs for both repos
5. promote `main` only after backup/publication evidence is current and consistent
6. create the next reserved Q.0.0.N artifact on each final branch only after terminal target-owned success
7. reconcile final SHAs, append the lifecycle ledger, and independently verify the published Q artifacts and branch-inventory digest

A valid Q version is a repository artifact, not a substitute for branch authorization. The manager records the evidence but does not invent remote completion. It accepts a version only when the caller supplies terminal success, exact remote SHAs, clean local state, workflow run IDs, and correlated lifecycle evidence.

The same contract applies to additional repo instances that follow the autosync model: branch-level publication is performed on backup first, then main, with the same SHA check and ledger gate. The automation must never force-push, overwrite an existing Q-version artifact, or claim success without terminal workflow evidence.

## Q.0.0.1 creation and companion artifacts

The first materialized Q-version directory after the policy gate is `Q.0.0.1`. It must be created in the final branch state of each repository only after the evidence gate is satisfied. The directory should include:

- `Q.0.0.1/REPOSITORY_METRICS.json`
- `Q.0.0.1.md` companion summary
- any required lifecycle and sync records created by the branch publication flow

This directory is a final artifact, not an everyday working directory. It is not an excuse to keep stale or fabricated research data around. The live repo content stays sanitized; the version artifact remains the archive of accepted evidence and completion state.

## Validation and current limitations

Focused tests cover strict parsing, cross-root discovery, reservation integrity and locking, pair metrics, per-file hashes, finalization blockers, exact-SHA finalization, and dirty/mismatched tree rejection. Local tests prove these deterministic contracts only.

Current remote completion remains blocked by unverified GitHub App key rotation, HTTP 403 branch-protection reads, failed earlier-SHA tracker/autosync runs, and local branch divergence. No final Q version was created by this continuation. Remote completion and final repository metrics remain pending independently verified target-owned evidence.
