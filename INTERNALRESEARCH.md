# Internal Research Contract

## Purpose

Internal research establishes what the repositories and their histories already contain before proposing edits or merges. It is the first research stage after the merge-start and pre-merge snapshot, and it does not authorize copying, deleting, pushing, or claiming completeness.

## Ten required controls

1. Inventory every supplied live repo, materialized snapshot, archive, and worktree before planning.
2. Read applicable repo instructions, `oe.txt`, `oe.md`, `oe2.md`, `oe2.txt`, `MERGE.md`, `SYNC.md`, and validation contracts before proposing work.
3. Inventory code, tests, workflows, docs, manifests, APIs, endpoints, routes, ports, build/install/release assets, and generated state by exact path and file type.
4. Enumerate every locally available head, remote-tracking, tag, and fetched PR ref, recording that this is not proof of remote freshness or all PR coverage.
5. Capture per-source and per-file path, size, content hash/object ID, source/ref, timestamps when available, and read/parse errors.
6. Map each requirement to implementation files, symbols, tests, workflow hooks, docs, owning repository, and destination candidates.
7. Compare active, snapshot, and historical versions to identify identical copies, additive sections, conflicts, deletions, and behavior regressions.
8. Keep missing, inaccessible, ambiguous, unowned, or unreadable sources explicitly blocked; never fill gaps with guessed content.
9. Turn findings into falsifiable hypotheses, bounded plans, test cases, rollback notes, and measurable acceptance criteria.
10. Use findings as research inputs for later improvements while preserving source provenance, user-authored content, memory, Q seed ancestry, and security boundaries.

## Execution stages

`MERGE_START` records the repositories and execution ID. `PRE_MERGE_INVENTORY` records the initial file/directory/ref baseline. `INTERNAL_RESEARCH` records the measured roots, file types, counts, limitations, and research controls. `MERGE_PLAN` stores ownership, candidate routing, compatibility, and duplicate decisions before mutation. Initial and post-agent merge passes are separate. Any implementation change requires targeted tests and a post-merge audit.

## Decision policy

- Identical content: deduplicate only after hashes and provenance are retained.
- Same document identity with same introduction and nonconflicting additive sections: a deterministic section merge may be proposed and tested.
- Different titles, conflicting section bodies, unknown ownership, deletion, security-sensitive behavior, or irreversible changes: preserve all sources and mark `preserved_conflict` for review.
- Historical source documents are evidence and candidates, not automatic production truth.
- UI findings route through `STYLES.md`, `UNIVERSAL.md`, and `UNIVERSALS.md`; app behavior remains product-specific.

## Q seed and QVillage

Each Q seed finding records a stable seed ID, parent, repository/ref/SHA, content digest, requirement, implementation path, tests, status, and authorization reference. QSeed payload encryption is explicit per-file opt-in using standard authenticated encryption and an owner-managed external key; never infer encryption/decryption authority from an audit candidate or model recommendation. QVillage may display sanitized research questions, citations, source hashes, timestamps, confidence/limitations, and linked validation results. It must distinguish `planned`, `visited`, `validated`, `blocked`, and `stale`; it must not display secrets, private content, or unverified claims as facts.

## Scope limits

A local filesystem walk is not a full history audit. The agent's current ref scan reads Markdown blobs reachable from refs in its local Git database; all intermediate commit trees, all remote PRs, future commits, inaccessible repos, and external systems require separate target-owned or authorized evidence. No audit can inspect future content before it exists.

## Repository surface audit integration

Every merge/internal-research run writes `ollamatracks/repository_surface_audit.json` and links it to the Q lifecycle. The audit maps all accessible materialized paths to Markdown, API, endpoints, routes, ports, links, components, tree, automation/hooks, styles/universals, QVillage/QVS, comparison, Qtrade, production-gap, percentage, and memory categories. It records hashes and structural metrics without copying source prose. Sentence counts are heuristic and do not prove semantic understanding; requirements require source/test/workflow mapping.

`ALLMDFILESREFS.md` plus the audit artifact distinguish present paths from missing, unreadable, excluded, historical-only, or remote-unverified sources. Local refs and materialized snapshots do not prove all PRs or intermediate commit trees. The shared audit gate remains `NEEDS_REVIEW` until exact-SHA target-owned evidence covers both repositories.

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

<!-- BEGIN QMOI MANAGED: internal-surface-research -->
## Agent-managed internal reference research coverage

- Audit status: `NEEDS_REVIEW`; local paths only; source hashes are in `QMOItracks/repository_surface_audit.json`.
- Markdown files: `2421`; local directories: `1280`; percentage candidates: `22237`; comparison/Qtrade metric lines: `52756`.
- Formula/calculation candidates: `13376`; path-grouped descriptive percentage summaries: `734`.
- Instruction candidates: `40146`; production-gap candidates: `299`. These are unverified queues, not proof of fulfilled instructions or defects.
- Production-gap scan: `299` candidates across `3409` files; candidates are not confirmed defects and are never bulk-replaced.
- Every document receives a content hash, byte/line/word/sentence counts, structural checks, and local-link checks when within the configured parse bound. Sentence counts are heuristic; semantic meaning is not inferred.
- All API, endpoint, route, port, workflow, link, component, tree, style, universal, QVS/QVillage, comparison, Qtrade, and metrics surfaces are mapped by path in `QMOItracks/repository_surface_audit.json`.
- Unavailable roots, unreadable or oversized files, remote refs, PR trees, and intermediate commit trees remain visible blockers.
<!-- END QMOI MANAGED: internal-surface-research -->
