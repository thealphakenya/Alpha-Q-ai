# ALLHOOKSWEBHOOKS.md

<!-- BEGIN QMOI MANAGED: active-hooks-webhooks-coverage -->
## Agent-managed active workflow and webhook inventory

Scope: current checkout only. Inventory discovery is not proof that a hook is registered remotely, reachable, authenticated, or successfully delivered.

- Workflow files discovered: `17`.
- Source/config files mentioning webhook identifiers: `5`.
- Workflow parse errors: `0`.
- External registration and delivery state: `not_verified` unless a provider read and signed delivery/test evidence are recorded for the exact repository/ref.
- Styles/universals feature event coverage is tracked in `QMOItracks/feature_test_hook_coverage.json`; applicability reviews: `0/404`; event-hook tests must be mapped separately from static style tests.

### Workflow event hooks

| Workflow | Trigger events | Status |
| --- | --- | --- |
| `.github/workflows/auto-merge-automated-pr.yml` | `pull_request_target, workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/branch-sync.yml` | `push, schedule, workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/codeql.yml` | `pull_request, push, schedule` | `definition_discovered_execution_not_implied` |
| `.github/workflows/cross-repo-auth-preflight.yml` | `schedule, workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/cross-repo-autosync.yml` | `push, schedule, workflow_dispatch, workflow_run` | `definition_discovered_execution_not_implied` |
| `.github/workflows/cross-repository-sync.yml` | `workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/markdown-inventory-refresh.yml` | `pull_request, push, schedule, workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/QMOI-autonomous-agent-realtime-monitor.yml` | `schedule, workflow_dispatch, workflow_run` | `definition_discovered_execution_not_implied` |
| `.github/workflows/QMOI-autonomous-agent.yml` | `schedule, workflow_dispatch, workflow_run` | `definition_discovered_execution_not_implied` |
| `.github/workflows/QMOI-live-activity-stream.yml` | `schedule, workflow_dispatch, workflow_run` | `definition_discovered_execution_not_implied` |
| `.github/workflows/QMOI-master-orchestrator.yml` | `schedule, workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/QMOI-pr-validation.yml` | `pull_request, push, workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/pr-monitor.yml` | `workflow_dispatch, workflow_run` | `definition_discovered_execution_not_implied` |
| `.github/workflows/qmoi-live-activity-stream.yml` | `push, schedule, workflow_dispatch, workflow_run` | `definition_discovered_execution_not_implied` |
| `.github/workflows/security-autofix.yml` | `schedule, workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/security-merge-gates.yml` | `pull_request, push, workflow_dispatch` | `definition_discovered_execution_not_implied` |
| `.github/workflows/workflow-tracker.yml` | `schedule, workflow_dispatch, workflow_run` | `definition_discovered_execution_not_implied` |

### Webhook-related source references

| Source path | Handler/provider mapping | Status |
| --- | --- | --- |
| `scripts/autonomous_completion_engine.py` | `unmapped` | `reference_only_not_runtime_verified` |
| `scripts/QMOI_autonomous_agent.py` | `unmapped` | `reference_only_not_runtime_verified` |
| `scripts/QMOI_research.py` | `unmapped` | `reference_only_not_runtime_verified` |
| `scripts/qaudit_universe.py` | `unmapped` | `reference_only_not_runtime_verified` |
| `tests/test_QMOI_autonomous_agent.py` | `unmapped` | `reference_only_not_runtime_verified` |

### Required hook/webhook safety evidence

For each active integration, record producer/event, consumer route and owner, signature/authentication verification, least-privilege scope, replay protection, idempotency, retry/backoff and dead-letter behavior, secret reference (never secret value), audit event, positive/negative delivery tests, freshness, exact SHA, and provider-side registration/read evidence. Never auto-register a third-party webhook or expose an endpoint without authorization and a reviewed threat model.
<!-- END QMOI MANAGED: active-hooks-webhooks-coverage -->

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10435`; directories: `1269`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2110, orchestration=2061, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52722`; percentage occurrences: `22237`.
- Markdown word count: `3552546`; heuristic sentence count: `673863`; sentence records indexed: `673863`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29844` metric claims; `10662` completion claims; `29747` metric and `10533` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13340`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40017` lines in `3670` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `287`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
