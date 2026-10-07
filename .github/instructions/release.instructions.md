# Release instructions

## Release policy

- A release requires a tag or release ID, source SHA, artifact hashes, and published metadata.
- Install and runtime verification must happen before publication claims.
- Keep failed artifacts and successful artifacts separate in evidence.
- Retain release provenance and do not delete evidence to hide a failed attempt.
- Autonomous release planning may run without supervision, but tag, publish, or deploy operations remain blocked until all release gates and explicit authority are verified.

## Required evidence

- release ID
- source SHA
- artifact names and hashes
- verification result
- environment or install test result
- remote retrieval evidence

## GitHub App and credential gate

- Confirm the authenticated actor, credential type, repository scope, and exact source SHA before release preparation or publication. Codespaces secret presence and user-reported App permissions are not authentication or authorization proof.
- Use only owner-confirmed rotated App keys and short-lived installation tokens. Keep Actions and Codespaces secret stores separate, and use the least permission needed by the target-owned workflow.
- Never pass a credential value through Copilot Chat, shell command text, release metadata, logs, or artifacts. Keep releases, deployments, and signing operations blocked when auth, rotation, required checks, or provenance is unresolved.

## QAUDITS release documentation

- Use QAUDITS to inventory release-related requirements, docs, workflow evidence, artifact hashes, install/runtime checks, and unresolved omissions. Candidate discovery and local validation are planning evidence, not release evidence.
- Update `RELEASES.md` and related app/build/download/tag/publish/QTeam documents only from observed release state; bind every claim to release/tag ID, source SHA, artifact hashes, verification, and remote retrieval evidence.
- QAUDITS must not publish, tag, sign, or deploy on its own. Require explicit authority and all release gates, then record terminal target-owned workflow results and independently verified remote state; otherwise retain the release as blocked in paired completion records.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10428`; directories: `1268`; Markdown: `2416`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2109, orchestration=2061, qteam_accountability=2049, release_tag_publish=2088, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2221`; needs review: `187`; metric candidate lines: `52705`; percentage occurrences: `22237`.
- Markdown word count: `3550281`; heuristic sentence count: `673664`; sentence records indexed: `673664`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29834` metric claims; `10658` completion claims; `29737` metric and `10529` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13328`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `39967` lines in `3666` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `286`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
