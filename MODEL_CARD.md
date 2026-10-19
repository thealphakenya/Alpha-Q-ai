# QMOI Model Card

**Generated:** 2026-09-27T23:00:52.206730Z
**Status:** Evidence-tracked; production status requires the final completion gate.

## Overview

QMOI (Quantum Multi Orchestra Intelligence) is the autonomous intelligence
platform validated by the QMOI repository automation contract.

## Applications

### QMOIAIUI

Conversational AI interface.

### QCity

File Manager.

### QMOI Space

Media Player.

### QALPHA

IDE.

## Memory Recovery and Provenance

QMOI must recover memory as a first-class capability. The autonomous agent treats memory as permanent operational state across repo updates, model changes, and dataset refresh cycles.

- Memory recovery sources: abc.txt, abctesting.txt, MEMORY_INDEX.md, memory_index.json, QMOI_REALTIME_MEMORY_INDEX.md
- Historical memory checkpoints referenced: abc.txt, abctesting.txt, MEMORY_INDEX.md, memory_index.json, QMOI_REALTIME_MEMORY_INDEX.md
- Recovery policy: validate integrity, restore serialized memory artifacts, reconcile timestamps, and rehydrate the latest working state before any autonomous update is considered safe.
- Missing or stale memory is a visible operational blocker; it must never be silently discarded or overwritten without evidence.

## QSeed lineage and protected payloads

- QSeed is an explicit local opt-in for encrypting a specifically selected payload using standard Fernet authenticated encryption and a user-managed key stored outside the repository.
- The QSeed vault writes ciphertext to a private external directory by default; decryption requires an explicit external destination and verifies integrity before writing.
- QSeed does not use a proprietary or QMOI-only cipher, make a quantum-safe claim, or automatically encrypt every repository file.
- Its lineage and encrypted-artifact hashes supplement but do not replace source-control history, autosync backups, undo/redo, restore-point validation, or terminal remote exact-SHA evidence.
- QAUDITS inventories ciphertext metadata without decrypting it. Deterministic risk prioritization includes every indexed path; model-generated audit suggestions are unverified and cannot authorize changes or mark gates passed.
- The local utility and specification are present in this checkout; a live second-repository installation and remote parity are not verified.

## Dataset automation and training corpus

This card reports path-only dataset candidates from configured data directories. It does not validate dataset contents, prove that a training job ran, or claim a live refresh service.

- Dataset candidate paths: Alpha-Q-ai-2025/datasets/trading/trading-dataset-sample.csv
- Dataset path-candidate count: 1; registered/validated dataset count: NOT_MEASURED
- Per-dataset quality, license, privacy, split/leakage, and benchmark metrics: NOT_MEASURED
- Dataset comparison evidence: NOT_PRESENT; assessment: NOT_ELIGIBLE; measured metrics: 0/5; blockers: 38
- Dataset replacements: 0; automatic replacement: disabled; remote verification: false
- Offline independence from remote dataset providers: NOT_VERIFIED
- Planned catalog and replacement gates: [DATASETS.md](DATASETS.md), [QAUDITS.md](QAUDITS.md), and [ALLCOMPARETYPES.md](ALLCOMPARETYPES.md)
- Dataset provenance and versioning must bind to immutable revisions and hashes. External source names and ownership must remain attributable.

## Model and Merge Evidence

- Master-plan topics discovered: 208
- Active repository files inventoried: 56078
- Alpha source tree available: True
- QMOI history source available: True
- Model-test paths: Alpha-Q-ai-2025/models/latest/qmoi_enhanced_advanced_model.py, Alpha-Q-ai-2025/models/latest/qmoi_enhanced_model.py, qmoi-enhanced-history-14/QMOIMODELTESTS.md, qmoi-enhanced-history-14/__tests__/chatbot.model.test.tsx, qmoi-enhanced-history-14/__tests__/ci.no-model-selector.test.ts, qmoi-enhanced-history-14/__tests__/qmoi-model.route.test.ts, qmoi-enhanced-history-14/_archive_qmoi-enhanced/models/latest/qmoi_enhanced_advanced_model.py, qmoi-enhanced-history-14/_archive_qmoi-enhanced/models/latest/qmoi_enhanced_model.py, qmoi-enhanced-history-14/models/latest/qmoi_enhanced_advanced_model.py, qmoi-enhanced-history-14/models/latest/qmoi_enhanced_model.py, qmoi-enhanced-history-14/tests/test_hf_model_sync.py, qmoi-enhanced-history-14/tests/test_qmoi_model_enhancer.py, qmoi-enhanced-history-14/tests/test_update_model_card.py, qmoi-enhanced-history-14/tools/issue_drafts/0604_models_latest_README.md.md, qmoi-enhanced-history-14/tools/issue_drafts/0936_qmoi-enhanced_models_latest_README.md.md
- Model updates must compare current code with all materialized history and
    merge inventories before changing behavior.

## Model comparison against leading frontier models

The table is a comparison roster, not a ranking. No superiority claim is made without a fresh, matched, independently reviewed benchmark and a schema-validated evidence record.

| Comparison target | Independently validated result |
| --- | --- |
| GPT-5 | NOT_MEASURED |
| Claude 4 Opus | NOT_MEASURED |
| Gemini 2.5 Pro | NOT_MEASURED |
| Llama 4 Maverick | NOT_MEASURED |
| DeepSeek V3 | NOT_MEASURED |

## Best-model validation gate

Best-model claim is pending independent benchmark validation; no proven top-rank claim is yet inserted into the model card.

## QVillage UI and Card Synchronization

- QVillage documentation present: True
- Awareness contract artifact present: False
- Memory artifacts present: MEMORY_INDEX.md, memory_index.json, QMOI_REALTIME_MEMORY_INDEX.md
- QVillage must expose model version, health, test status, source evidence,
    last update timestamp, and blocked or stale states.
- Model-card refreshes must update the repository card and publish the same
    evidence fields to the QVillage model surface only after validation passes.
- Missing credentials, remote failures, or incomplete tests remain visible as
    blocked evidence; they must never be represented as healthy completion.

## Model-card UI and evolution plan

- preserve the QMOI identity shell, status cards, memory history, and benchmark evidence in the UI
- ensure public and authenticated states remain separate and validated
- show memory recovery, dataset lineage, and security automation visibly rather than burying them behind hidden metadata
- list the benchmark gate, validation status, and the strongest known QMOI advantages in a single view

## Validation Contract

The autonomous validation contract covers:

- Windows
- macOS
- Linux
- iOS
- Android
- Web
- Platform-specific features
- File-handler registration
- GitHub automation
- Cross-repository synchronization
- Realtime telemetry
- Auto-healing
- Resume checkpoints
- Memory index generation
- Model-card generation
- GitHub proof contracts
- Security automation and vulnerability remediation
- Dataset recovery and benchmark validation

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
