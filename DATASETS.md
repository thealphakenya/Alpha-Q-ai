# QMOI Dataset Automation and Memory Recovery

This dataset ledger is the operational inventory that keeps the QMOI model, repository, and autonomous agent aligned across all models, apps, clone surfaces, and memory checkpoints.

## Memory provenance and recovery

QMOI must always preserve and restore all previously known memory artifacts before making a new autonomous update. This includes repository memory, historical logs, checkpoints, and the explicit memory seeds that were previously recorded in:

- `qmoi-enhanced-history-14/abc.txt`
- `qmoi-enhanced-history-14/abctesting.txt`
- `MEMORY_INDEX.md`
- `memory_index.json`
- `QMOI_REALTIME_MEMORY_INDEX.md`

Recovery rules:

- recover the latest valid memory before any model change
- preserve historical context even when later artifacts diverge
- keep irreversible deletions visible rather than silent
- record the memory source, timestamp, provenance, and validation state

## Dataset inventory

The autonomous agent must keep a live dataset inventory that includes the curated training, evaluation, benchmark, and dataset manifest inputs used by QMOI.

Primary metadata sources:

- repository dataset manifests and evaluation folders
- model-training metadata under `models` and `datasets` surfaces
- benchmark logs and comparison files for model evolution
- QMOI memory snapshots and training validation evidence

## Autonomous dataset automation

The QMOI dataset automation path should:

- refresh dataset manifests automatically after repository changes
- preserve working memory and historical checkpoints before overwriting a dataset artifact
- validate dataset provenance, coverage, and integrity before publishing a dataset update
- keep the benchmark and model card aligned with the exact dataset version in use

## Vulnerability automation contract

QMOI auto-remediation must extend beyond a single repo and fix known dependency risks across every discovered requirement file and repo surface without requiring repeated human intervention.

Recommendations:

- scan all discovered requirement manifests and dependency files
- patch known vulnerable floor versions automatically
- record all changed files and validation output
- re-run validation after the automated remediation cycle
- preserve a full audit trail and do not hide unresolved findings

## Best-model evidence gate

The claim that QMOI is the best model must only be added to the model card after independent benchmark validation proves it. Until that proof exists, the model card should continue to display the benchmark gate as pending rather than as a fact.

## Model-card UI integration

The model card UI must show:

- memory provenance and recovery readiness
- dataset inventory and validation state
- benchmark comparison section
- security remediation status
- best-model claim gate with explicit validation status

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
