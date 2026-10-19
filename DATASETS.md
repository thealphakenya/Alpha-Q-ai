# QMOI Dataset Automation and Memory Recovery

This document defines the intended QMOI dataset and memory evidence contract. It is not proof of a live catalog, continuous synchronization, or validated training data.

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

The intended catalog covers the curated training, validation, test, benchmark, reference, and synthetic inputs used by QMOI. This document is a design contract, not proof of a live catalog or scheduled refresh. Keep materialized worktree, configured Hub scopes, historical snapshots, dependencies, and remote observations as separate populations.

Primary metadata sources:

- repository dataset manifests and evaluation folders
- model-training metadata under `models` and `datasets` surfaces
- benchmark logs and comparison files for model evolution
- separately scoped QMOI memory/recovery evidence; memory artifacts are not
  training/evaluation datasets unless explicitly classified and approved

## Autonomous dataset automation

The planned QMOI dataset automation path should:

- refresh dataset manifests automatically after repository changes
- preserve working memory and historical checkpoints before overwriting a dataset artifact
- validate dataset provenance, coverage, and integrity before publishing a dataset update
- keep the benchmark and model card aligned with the exact dataset version in use

## Canonical QMOI dataset registry

Assign QMOI-owned datasets a stable internal ID and version, for example
`qvillage/<domain>/<task>/<version>`. This convention does not assert that an
external Hugging Face namespace exists. Each manifest record should include:

Registry implementation and per-dataset QAUDITS metrics are
`NOT_VERIFIED` in this plan; no successful live refresh is inferred.

- immutable dataset ID, revision, schema version, file/manifest SHA-256, and
  source scope (`active`, `generated`, `archive`, `third_party`, or `remote`);
- owner, source URL/repository and original name, creator/attribution, license,
  allowed purpose, consent/rights evidence, privacy class, and retention rule;
- domain/task, canonical feature IDs, language, dataset role, split method and
  seed, collection/creation timestamp, freshness limit, and intended consumers;
- artifact count/bytes and safe sample/row/schema counts, parser/validator
  version, validation result, omissions, and the exact next action.

Do not treat a matching filename as a dataset record. Exclude dependency,
cache, generated build, and archive content from the active QMOI dataset
denominator while retaining separately scoped archival/source lineage where
needed. Never write raw private examples, prompts, credentials, or financial
values into manifests or QAUDITS reports.

## Dataset metrics and replacement lifecycle

QAUDITS should emit per-dataset and aggregate metrics with explicit scope,
source hash, timestamp, formula, numerator/denominator, state, and freshness:
discovered/read/parsed/validated/excluded/unavailable records; unique IDs and
revisions; bytes and safe sample counts; schema and feature coverage; split
sizes; missing/invalid/duplicate rates; applicable label balance;
contamination/leakage; provenance/license/privacy review; drift and staleness;
local/cache/provider availability; offline task results; and matched
benchmark quality, uncertainty, latency, throughput, and resource cost.
Unsupported or unobserved values are `NOT_MEASURED`/`UNKNOWN`, never zero or a
pass. The full metric, comparison, and document-refresh plan is in
[QAUDITS.md](QAUDITS.md), [ALLCOMPARETYPES.md](ALLCOMPARETYPES.md), and
[QVILLAGE.md](QVILLAGE.md).

Only create QMOI-owned data from owned, licensed, consented, or otherwise
authorized sources. For each third-party dataset, compare a candidate on the
same frozen tasks, splits, evaluator, model/runtime, and environment. Keep the
incumbent until a legal, privacy, compatibility, quality, offline, regression,
security, independent-review, explicit-approval, and rollback gate passes for
the specific consumer. Ties, regressions, unknown rights, stale evidence, and
missing coverage block substitution. Preserve third-party attribution and
never globally rename or erase source identity.

Offline independence means the approved local model/assets and locally
available QMOI data can support the declared core workloads from a clean
installation with network access to Hugging Face and other dataset providers
disabled. It must be demonstrated by repeatable cold-start, cache-miss,
network-denial, and recovery tests; it is `NOT_VERIFIED` until those tests and
their exact inputs/results are independently reviewed.

### Versioned comparison evidence and fail-closed substitution

The existing local evolution planner can read the optional
`ollamatracks/dataset_comparison_evidence.json` (schema version 1). It checks
that run/correlation IDs, repository/ref, full source SHA/tree SHA are
present; that the incumbent and candidate IDs differ, the candidate uses the internal
`qvillage/` namespace, both dataset artifact hashes and suite/evaluator/
environment hashes are valid, the protocol is matched, and at least three
replicated runs are reported. The namespace check is not ownership proof.

The required metrics are `task_quality`, `coverage`, `data_quality`,
`offline_independence`, and `resource_cost`, with declared higher/lower
directions, finite scores, at least 30 samples, and confidence intervals that
show strict candidate improvement. The record must also cover each unique
canonical feature ID with the expected direction, sufficient sample count,
and matching registry SHA-256. Hard gates must explicitly pass candidate
ownership/authorization, provenance, license/allowed use, privacy, schema
compatibility, split-leakage and benchmark-contamination checks, security,
regression, offline network-denial, rollback, and independent review.

Every absent, malformed, underpowered, tied, stale, or failing item remains a
blocker. The assessment is reported local evidence only:
`datasets_replaced_count` remains zero, automatic replacement remains
disabled, and `remote_verified` remains false. Eligibility allows independent
review only; actual consumer-specific migration still requires explicit owner
authorization, impact review, a reversible canary, and exact-SHA remote
evidence. This planner does not execute comparisons, switch datasets, rename
third-party assets, or refresh all documentation itself.

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
