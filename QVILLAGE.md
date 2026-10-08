# QVILLAGE.md

QVillage is the live QMOI community, model, and knowledge coordination surface. It is treated as the master-only QMOI community layer that stays synchronized with GitHub, Hugging Face, and the live autonomous agent.

## Active automation
- QVillage sync remains a first-class automation surface inside QCity and the autonomous agent.
- memory, model, and runtime state are synchronized across repo docs and platform references.
- the live state is refreshed automatically as the repository evolves.


<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10446`; directories: `1270`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2156, build_download_install=2110, orchestration=2062, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2001`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52718`; percentage occurrences: `22237`.
- Markdown word count: `3554796`; heuristic sentence count: `674081`; sentence records indexed: `674081`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29838` metric claims; `10664` completion claims; `29741` metric and `10535` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9047` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13342`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40052` lines in `3673` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `290`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: ollama-full-coverage-audit-status -->
## Agent-managed OFCA status

- Audit name: `OFCA`; local scan status: `INCOMPLETE`.
- Materialized files scanned: `10429`; mention-bearing files: `4158`.
- Local refs: `39`; local commits: `2653`; mention-change commits: `2029`.
- Source manifest SHA-256: `988b9f2630cb4cdb07acf8d51442048b72d239ea2d188b28318c0f57802cd783`; full remote-history coverage: `False`.
- QVillage/QVS materialized references: `373` files, `212` Markdown files; remote/history completeness: `not_verified`.
- `prMergeIncluded` is required before merge activity. Unverified remote refs, pull requests, peer roots, and intermediate commit trees remain blockers.
- Next action: Run an authorized target-owned audit for both repositories covering all refs, PRs, and intermediate commit trees; attach terminal exact-SHA evidence before Q-version finalization.
<!-- END QMOI MANAGED: ollama-full-coverage-audit-status -->
