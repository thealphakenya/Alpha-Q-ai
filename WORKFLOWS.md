# QMOI Workflow Contract

This file is the canonical workflow map for `qmoi-enhanced`. GitHub Actions are the independent execution environment; a codespace is never required.

## Execution Order

1. `ollama-pr-validation.yml` validates source, tests, documentation, and workflow structure.
2. `ollama-master-orchestrator.yml` coordinates validated main-branch work and dispatches the agent once.
3. `ollama-autonomous-agent.yml` checks out trusted `main`, installs dependencies, bootstraps Ollama, verifies `qwen2.5-coder:3b` with real inference, runs a bounded LLM repair loop, validates, checkpoints, uploads evidence, and enforces `OLLAMA_SUCCESS.json`.
4. `ollama-autonomous-agent-realtime-monitor.yml`, `workflow-tracker.yml`, and `pr-monitor.yml` observe runs and must report `SUCCESS` only from a passed contract.
5. `branch-sync.yml` maintains `main` and `autosync-backup`; cross-repository sync is explicit and must create auditable changes.

## Success Contract

The message `Autonomous agent executed successfully.` is valid only when `ollamatracks/OLLAMA_SUCCESS.json` has `final_status: SUCCESS` and all of these are true: Ollama healthy, model available, inference verified, LLM coding started, post-agent validation passed, and checkpoint created. A Python-only validation pass is not agent success.

## Bounds And Safety

`MAX_ITERATIONS`, `MAX_TASKS_PER_ITERATION`, and `MAX_RECOVERY_ATTEMPTS` bound work. Repeated failures, repeated model responses, invalid plans, protected paths, credentials, workflow edits, traversal, and untrusted checkpoints fail closed. Secrets are supplied through GitHub Actions secrets and are never sent in model prompts or tracking artifacts.

## Manual Execution

```bash
OLLAMA_MODEL=qwen2.5-coder:3b python scripts/ollama_autonomous_agent.py health
OLLAMA_APPLY_REPAIRS=false python scripts/ollama_autonomous_agent.py autonomous
```

Set `OLLAMA_APPLY_REPAIRS=true` only in a trusted, explicitly authorized run. Scheduled runs are bounded and use the same contract as manual runs; workflow recursion is prevented by trusted-branch and concurrency conditions.

## Evidence

Diagnostics live under `ollamatracks/`, including `OLLAMA_HEALTH.json`, `OLLAMA_SUCCESS.json`, telemetry, logs, and resume state. Failed or blocked runs upload diagnostics and do not emit success.
`checkpoint.json` records the commit, workflow run, iteration, model, Ollama
health, task, inspected/changed files, tests, repair state, and failure
fingerprint needed for trusted resume.

## Sister Repository

`Alpha-Q-ai` uses the same contract when its setup instructions in `zx.txt` are installed. Shared documentation and sync changes are classified, audited, validated, and proposed through a PR rather than copied blindly.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10955`; directories: `1284`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2174, build_download_install=2130, disability_accessibility=285, orchestration=2081, qteam_accountability=2069, release_tag_publish=2110, tree_inventory=2018`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2229`; needs review: `203`; metric candidate lines: `53076`; percentage occurrences: `22283`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13476`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40920` lines in `3729` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `319`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
