# TRANSION.md

## Purpose and scope

This document defines the transition plan for the active QMOI styles and universals migration. It is a governance and planning artifact, not proof of completion. Every entry below distinguishes discovered candidates, planned replacements, verified replacements, and remote-verified results. The agent must continue only when each step has a matching QAUDITS pass, exact-path record, test/hook mapping, and remote evidence or a written blocker.

The correctly spelled entry point is [TRANSITION.md](TRANSITION.md). This established file remains the detailed plan to avoid maintaining two competing migration bodies.

QVirtualLabs engineering coverage is tracked by [QVIRTUALLABS.md](QVIRTUALLABS.md) and indexed through [TRANSIONQ.md](TRANSIONQ.md). QENGINEER source reconciliation, simulation, physical evidence, UI, project integration, and QVillage research must remain separate transition gates.

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
- [QVIRTUALLABS.md](QVIRTUALLABS.md)
- [TRANSIONQ.md](TRANSIONQ.md)

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
23. Add a QVirtualLabs gate for canonical QENGINEER source reconciliation, stable engineering-domain IDs, implementation/test mappings, solver validation, uncertainty, physical calibration, research provenance, accessible UI transitions, and project/preview integration.
24. Keep simulation results distinct from measured physical results; require operator, instrument, calibration, protocol, safety, and raw-data provenance before counting a physical correlation.
25. Report candidate, mapped, tested, simulated, physically correlated, and remote-verified metrics separately in the shared QAUDITS plan and QVillage/transition documents.

## Transition execution plan

1. Regenerate the style/universal candidate inventory and its directory tree from materialized paths only.
2. Normalize the `.md` naming crosswalk and classify each match by category, source scope, and status.
3. Reconcile `STYLES.md`, `UNIVERSAL.md`, `UNIVERSALS.md`, `QAUDITS.md`, and `QVERSIONMANAGER.md` against the inventory and categorization model.
4. Add `TRANSION.md` to the canonical documentation set and reference it from every relevant managed section.
5. Require a QAUDITS pass before every additional step and record the missing items as blockers rather than treating them as resolved.
6. Validate generated path trees, hashes, and cross-refs before any replacement is approved.
7. Reconcile [QVIRTUALLABS.md](QVIRTUALLABS.md) with the canonical QENGINEER source before marking any engineering requirement understood or implemented.
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

- Status: `NEEDS_REVIEW`; materialized files: `11301`; directories: `1291`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2177, build_download_install=2131, disability_accessibility=288, orchestration=2082, qteam_accountability=2071, release_tag_publish=2110, tree_inventory=2022`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2230`; needs review: `202`; metric candidate lines: `53187`; percentage occurrences: `22274`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13561`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `41058` lines in `3748` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `340`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: qaudit-style-universal-accessibility-coverage -->
## Agent-managed QAUDITS style, universal, accessibility, and recovery coverage

This section is refreshed from the same local QAUDITS universe on every invocation of `refresh_ollama_reference_audit()` (pre-merge and full `audit-inventory` paths). It is not a timer or remote verification.
- Generated at: `2026-10-16T19:42:13.889504Z`; correlation ID: `e26c7a05-b66b-4740-93a2-c01b12b846ce`.
- Source manifest SHA-256: `2f2226c9b16ac7e88f811078ce1efe2cdeae4fbe797f2201d374a797b35cec76`; scope: `materialized_local_only`.
- Source language path counts: `{"JavaScript": 761, "PowerShell": 24, "Python": 1654, "Rust": 4, "SQL": 2, "Shell": 134, "TypeScript": 2236, "unclassified": 6455}`; unclassified: `6455`; all-world coverage: `False`.
- Style candidates: `22`; universal candidates: `42`; all remain candidate-only.
- QStats: `18` planned domains; `34` observed contract files; `1` missing/unavailable; remote verified: `False`.
- EvolutionO retirement plan: `0/5` phases complete; plan SHA-256 `06271df029931a822e34bedda961c2f79bd9777520bb39f6560be05e282503ae`; OFCA target `OFCA.md`; status remains `PLANNED` until terminal remote gates pass.
- QLion: `856` variation candidates; `8` registered extensions; implementation and remote validation remain unverified.
- Chat/voice/hands-free candidates: `1123`; checkpoint/undo/redo/restore candidates: `842`; heartbeat/health/oxygen candidates: `1557`.
- Disability/accessibility Markdown candidates: `284`; complete path/category/hash records are in `ollamatracks/qaudit_universe.json` and `ALLMDFILESREFS.md` under Category D1.
- Disability/accessibility category path count: `484`; mapped tests: `0`; reviewed hook applicability: `0`.
- Audit status: `NEEDS_REVIEW` until owners, implementations, user-selected access preferences, privacy boundaries, applicable tests, and exact-SHA evidence are mapped. No disability is inferred or stored as a user profile.
- Missing, stale, or provider-unverified health/oxygen values remain `UNKNOWN`; dashboard balances and account values require authorized provider evidence and are not inferred from prose.
- Updating this managed section never rewrites historical/archive documents, policy instructions, or Q-version artifacts.
<!-- END QMOI MANAGED: qaudit-style-universal-accessibility-coverage -->

<!-- BEGIN QMOI MANAGED: qaudit-qvirtual-labs-coverage -->
## Agent-managed QVirtualLabs engineering coverage

Generated from the local QVirtualLabs source inventory; a full QAUDITS universe manifest is included only when supplied by that inventory refresh. These are candidate-plan metrics, not implementation, experiment, physical-lab, or remote-completion evidence.
- Status: `BLOCKED_SOURCE_RECONCILIATION`; correlation ID: `231b915c-d2b9-45e5-baaa-1a02ef7b2209`; source manifest SHA-256: `ac35b2d4e2cc91f1395e1dd85f01183b6adbc2cb40411ef2194f6ab0e69a20ba`.
- QAUDITS universe manifest SHA-256: `unavailable`; QVirtualLabs source-manifest scope: `qvirtual_labs_source_files`.
- Plan artifact: `ollamatracks/qvirtual_labs_plan.json`; plan SHA-256: `b01b3fe497df8a44e3bd5965ac9f34336042d092199d3fe16ce0537118122773`; scope: `materialized_local_only`.
- Starter engineering-domain candidates: `14`; cross-cutting gate candidates: `19`; total starter-plan requirements: `33`.
- Authoritative QENGINEER requirements: `UNKNOWN`; QENGINEER source status: `missing_or_unsafe`.
- Requirement-to-implementation / focused-test mappings: `0` / `0`.
- Verified simulations / benchmark validations: `0` / `0`; physical experiment records / calibration correlations: `0` / `0`.
- Convergence cases / uncertainty reports / accuracy claims verified: `0` / `0` / `0`; safety protocols reviewed: `0`.
- Official research sources checked / date-fresh observations / stale observations: `8` / `8` / `0`; exact retrieval times not captured: `8`; verified evolution cycles: `0`.
- Recommended architecture: `one bounded, auditable adapter contract with specialist solvers; no monolithic all-domain solver selected`; first pilot candidate: `ngspice circuit reference case`; Ollama inference: `NOT_MEASURED` by this inventory.
- Tool recommendation rationale: `domain fit from official documentation, implementation isolation, and a bounded first regression; not a comparative performance benchmark`; selected tool: `NONE`; tool candidates: `6`.
- Public QENGINEER probe: `UNKNOWN_NOT_FOUND_OR_PRIVATE`; a public 404 is ambiguous without authenticated repository read access.
- UI/accessibility mappings / project, auto-project, and preview integrations: `0` / `0`; remote verified: `False`.
- Simulation output is never counted as physical evidence. Physical correlation requires an authorized protocol, human operator, traceable instruments/calibration, and reviewed raw-data provenance.
- Historical reference: `qmoi-enhanced-history-14/QVIRTUALLABS.md`; scope `historical_snapshot_candidate`; not authoritative.
- The planner does not run a solver, retrieve external research, invoke hardware, or infer that an unlinked implementation is absent.
<!-- END QMOI MANAGED: qaudit-qvirtual-labs-coverage -->
