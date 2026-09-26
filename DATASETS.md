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
