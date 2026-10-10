# TRANSION.md

## Purpose and scope

This document defines the transition plan for the active QMOI styles and universals migration. It is a governance and planning artifact, not proof of completion. Every entry below distinguishes discovered candidates, planned replacements, verified replacements, and remote-verified results. The agent must continue only when each step has a matching QAUDITS pass, exact-path record, test/hook mapping, and remote evidence or a written blocker.

The correctly spelled entry point is [TRANSITION.md](TRANSITION.md). This established file remains the detailed plan to avoid maintaining two competing migration bodies.

## Canonical style/universal replacement catalog

The style and universal layer is the shared contract for the active repository, historical sources, cloned platforms, and cross-repo product surfaces. Planned and candidate coverage includes the primary documents and directories below.

### Canonical documents treated as style and universal authority

- [STYLES.md](STYLES.md)
- [UNIVERSAL.md](UNIVERSAL.md)
- [UNIVERSALS.md](UNIVERSALS.md)
- [QAUDITS.md](QAUDITS.md)
- [QVERSIONMANAGER.md](QVERSIONMANAGER.md)
- [ALLAUTO.md](ALLAUTO.md)
- [AUTODEV.md](AUTODEV.md)
- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [OFCA.md](OFCA.md)
- [ALLTESTSAUTOTESTS.md](ALLTESTSAUTOTESTS.md)
- [ALLHOOKSWEBHOOKS.md](ALLHOOKSWEBHOOKS.md)
- [COMPONENTS.md](COMPONENTS.md)
- [TREE.md](TREE.md)
- [APP_LINKS.md](APP_LINKS.md)
- [VERCELLINKS.md](VERCELLINKS.md)
- [API.md](API.md)
- [ENDPOINTS.md](ENDPOINTS.md)
- [ROUTES.md](ROUTES.md)
- [ALLPORTS.md](ALLPORTS.md)
- [INTERNALRESEARCH.md](INTERNALRESEARCH.md)
- [EXTERNALRESEARCH.md](EXTERNALRESEARCH.md)

### Directories and registry paths participating in the transition

- `.github/instructions/`
- `scripts/`
- `tests/`
- `ollamatracks/`
- `QMOItracks/`
- `qmoi-enhanced-history-14/`
- `Alpha-Q-ai-2025/`
- `QMOI/`-like generated registry surfaces and category-driven indexes

### Replacement lineage status model

- `candidate`: discovered by file naming, path structure, hash, or content pattern; not assumed to be implemented
- `planned_replacement`: approved for review, test mapping, and rollback planning
- `verified_replacement`: has path, source/destination map, tests, hook applicability review, owner, and exact SHA evidence
- `remote_verified`: verified by target-owned workflow evidence for the exact repository and ref
- `blocked`: missing review, missing tests, missing remote verification, or conflicting ownership

### Metrics baseline and counts

The exact counts below are local discovery baselines and must be regenerated and revalidated before any production replacement claim is made.

- Candidate file entries: `pending regeneration from materialized scan`.
- Candidate directory entries: `pending regeneration from materialized scan`.
- Verified replacements: `0` (local evidence must create a verified file/directory lineage before this count changes).
- Pending replacement records: `pending`.
- Skipped/unreadable/oversized sources: `pending`.
- Feature IDs requiring test mapping: `pending`.
- Hook/webhook reviews required: `pending`.
- Remote-verified release/deploy/install evidence: `pending`.
- Audit shard count, missing/overlapping shard count, scan duration, bytes hashed, metadata-only large-file count, read/hash failures, and retry count: reported per refresh, never inferred from percentages.

## Required transition enhancements

1. Create a canonical style/universal registry with one source-of-truth path for app, platform, clone, and access-mode coverage.
2. Add deterministic naming crosswalks for Markdown, generated docs, and historical snapshots so basename collisions are visible and must be reviewed rather than silently replaced.
3. Add a step-by-step QAUDITS gate before every automation stage: inspect requirements, source paths, tests, hooks, policies, and exact evidence before continuing.
4. Synchronize `ALLMDFILESREFS.md` category assignments with the QAUDITS inventory so style, universal, test, hook, finance, monitoring, and Q-version entries are tracked together rather than in isolated files.
5. Enforce a verified replacement ledger in which every replacement record includes source path, destination path, prior SHA-256, new SHA-256, owner, reason, tests, rollback, authorization, repo/ref/SHA, and remote evidence.
6. Add per-step metrics for candidate files, directories, style counts, universal counts, extension counts, and unmapped features so no coverage is omitted.
7. Add a lifecycle gate in `QVERSIONMANAGER.md` requiring `PRODUCT_PLATFORM_CATALOG`, `LION_AND_EXTENSION_VARIANTS`, `RELEASE_DELIVERY_LIFECYCLE`, and `QTEAM_ACCOUNTABILITY` to pass before any finalization.
8. Add QAUDITS-specific policy that every claim is tagged as `candidate`, `mapped`, `verified`, `review_required`, or `remote_verified` and that local-only discovery never upgrades to remote completion.
9. Extend the agent to generate and refresh the full style/universal candidate tree without self-referential hash drift and without counting the generated report as replacement proof.
10. Extend the canonical docs to mention every new style/universal file and directory and every discovered candidate in a reviewable inventory section.
11. Add release/build/install/download/deploy lifecycle checks so QAUDITS verifies not just code presence but production readiness and distribution evidence.
12. Add human and automation accountability tracking for QTeam/friendship/master ownership, role boundaries, and protected actions so no universal or style change bypasses authorization.
13. Add an explicit orphan and duplicate rule: name-only matches must be listed as unresolved until the path and lineage are checked against the item’s canonical owner and target scope.
14. Add continuity metrics for success/failure record counts, skipped sources, and unresolved features so the agent can safely resume without losing evidence.
15. Use deterministic sorted path manifests, streamed SHA-256, bounded parallel batches, stable worker versions, and atomic artifact publication for large repositories; cap workers and in-flight batch memory.
16. Preserve large-file path/size/hash metadata while explicitly marking content parsing unavailable; do not treat an unparsed large file as semantically audited.
17. Partition remote refs, PRs, and intermediate commit trees into immutable, exactly bounded shards; verify shard completeness, overlap, source SHA, and merged manifest before gate advancement.
18. Separate traversal, hash, structural Markdown, semantic mapping, test execution, hook review, and remote-verification durations/counts so one fast phase cannot disguise a missing phase.
19. Add checkpointed bounded retry/timeout budgets, resumable work queues, cancellation-safe incomplete states, and risk-prioritized scheduling for high-impact/security gates.
20. Apply content-addressed cache entries only when repo/ref/source SHA, schema/tool version, policy version, and expiry match; stale or ambiguous cache data triggers refresh.
21. Expand finance/Qtrade audit mapping to require fresh source timestamps, units/currency, account/venue scope, costs, risk measures, no-trade decision quality, reconciliation, and explicit blocked states for unavailable values.
22. Add audit determinism, large-file, symlink, unreadable-path, worker-failure, missing/duplicate-shard, cache-expiry, and resume-after-interruption regression cases.

## Transition execution plan

1. Regenerate the style/universal candidate inventory and its directory tree from materialized paths only.
2. Normalize the `.md` naming crosswalk and classify each match by category, source scope, and status.
3. Reconcile `STYLES.md`, `UNIVERSAL.md`, `UNIVERSALS.md`, `QAUDITS.md`, and `QVERSIONMANAGER.md` against the inventory and categorization model.
4. Add `TRANSION.md` to the canonical documentation set and reference it from every relevant managed section.
5. Require a QAUDITS pass before every additional step and record the missing items as blockers rather than treating them as resolved.
6. Validate generated path trees, hashes, and cross-refs before any replacement is approved.
7. Generate the verified replacement ledger only when tests, rollback, authorization, and remote evidence are present.
8. Run the target suite and record the exact result before marking a step complete.
9. Re-read the branch- and repo-level evidence and update the local evidence artifacts after each step.
10. Stop finalization unless the exact remote SHA, workflow evidence, and branch authorization are all recorded and independently verified.
11. For large trees, shard only immutable inputs, persist shard checkpoints, validate every expected range, and merge sorted records into a root manifest; rescan changed prefixes only for local diagnostics, then regenerate the full final digest before any gate.
12. Schedule independent read-only work concurrently, but serialize checkpoint cursor updates, lifecycle-ledger appends, protected writes, merge operations, and publication.
13. Stop boundedly on exhausted retries, resource limits, inaccessible inputs, ambiguous HTTP responses, or human-authorization gates; retain partial outputs and a ranked resumable queue.
14. Inventory chat, conversational, voice, and hands-free interfaces by actual source path; map access, consent, privacy, style, platform permissions, disability access modes, and tests. Keep absent implementations unmapped.
15. Map checkpoint undo/redo and restore decisions to freshness signals and validation gates; heartbeat loss alone never authorizes restore, and checkpoint navigation is not file rollback.
16. Audit health, heartbeat, dashboard, and oxygen-style metrics by source, unit, freshness, and missing-data behavior; unknown values remain unknown rather than becoming zero or healthy.

## Required documentation references

This transition plan must remain consistent with:

- [QAUDITS.md](QAUDITS.md)
- [STYLES.md](STYLES.md)
- [UNIVERSAL.md](UNIVERSAL.md)
- [UNIVERSALS.md](UNIVERSALS.md)
- [ALLAUTO.md](ALLAUTO.md)
- [AUTODEV.md](AUTODEV.md)
- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [QVERSIONMANAGER.md](QVERSIONMANAGER.md)
- [OFCA.md](OFCA.md)
- [ALLTESTSAUTOTESTS.md](ALLTESTSAUTOTESTS.md)
- [ALLHOOKSWEBHOOKS.md](ALLHOOKSWEBHOOKS.md)
- [INTERNALRESEARCH.md](INTERNALRESEARCH.md)
- [EXTERNALRESEARCH.md](EXTERNALRESEARCH.md)
- [MERGE.md](MERGE.md)
- [production.md](production.md)
- [productionenhanced.md](productionenhanced.md)
- [undoredo.md](undoredo.md)

## Final governance note

This plan intentionally keeps replacement discovery fail-closed: the system can count, review, and document candidates, but it must not convert them into replacements without verified metadata, test coverage, policy alignment, and exact-SHA evidence. Local generation and historical scan results remain advisory until a target-owned workflow proves the exact remote state.

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

<!-- BEGIN QMOI MANAGED: qaudit-style-universal-accessibility-coverage -->
## Agent-managed QAUDITS style, universal, accessibility, and recovery coverage

This section is refreshed from the same local QAUDITS universe on every invocation of `refresh_QMOI_reference_audit()` (pre-merge and full `audit-inventory` paths). It is not a timer or remote verification.
- Generated at: `2026-10-10T02:54:49.639306Z`; correlation ID: `80504776-40b9-44ed-a424-40611c22cc87`.
- Source manifest SHA-256: `f604caed4cca2e044439cdcaeabb9d44d0b394a7a836adf5c50c57ec67d8ed2d`; scope: `materialized_local_only`.
- Style candidates: `22`; universal candidates: `40`; all remain candidate-only.
- QStats: `13` planned domains; `20` observed contract files; `1` missing/unavailable; remote verified: `False`.
- QLion: `820` variation candidates; `8` registered extensions; implementation and remote validation remain unverified.
- Chat/voice/hands-free candidates: `944`; checkpoint/undo/redo/restore candidates: `776`; heartbeat/health/oxygen candidates: `1434`.
- Disability/accessibility Markdown candidates: `266`; complete path/category/hash records are in `QMOItracks/qaudit_universe.json` and `ALLMDFILESREFS.md` under Category D1.
- Disability/accessibility category path count: `407`; mapped tests: `0`; reviewed hook applicability: `0`.
- Audit status: `NEEDS_REVIEW` until owners, implementations, user-selected access preferences, privacy boundaries, applicable tests, and exact-SHA evidence are mapped. No disability is inferred or stored as a user profile.
- Missing, stale, or provider-unverified health/oxygen values remain `UNKNOWN`; dashboard balances and account values require authorized provider evidence and are not inferred from prose.
- Updating this managed section never rewrites historical/archive documents, policy instructions, or Q-version artifacts.
<!-- END QMOI MANAGED: qaudit-style-universal-accessibility-coverage -->
