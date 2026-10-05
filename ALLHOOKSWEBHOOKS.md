# ALLHOOKSWEBHOOKS.md

<!-- BEGIN QMOI MANAGED: active-hooks-webhooks-coverage -->
## Agent-managed active workflow and webhook inventory

Scope: current checkout only. Inventory discovery is not proof that a hook is registered remotely, reachable, authenticated, or successfully delivered.

- Workflow files discovered: `17`.
- Source/config files mentioning webhook identifiers: `3`.
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
| `.github/workflows/cross-repo-autosync.yml` | `push, schedule, workflow_dispatch` | `definition_discovered_execution_not_implied` |
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
| `tests/test_QMOI_autonomous_agent.py` | `unmapped` | `reference_only_not_runtime_verified` |

### Required hook/webhook safety evidence

For each active integration, record producer/event, consumer route and owner, signature/authentication verification, least-privilege scope, replay protection, idempotency, retry/backoff and dead-letter behavior, secret reference (never secret value), audit event, positive/negative delivery tests, freshness, exact SHA, and provider-side registration/read evidence. Never auto-register a third-party webhook or expose an endpoint without authorization and a reviewed threat model.
<!-- END QMOI MANAGED: active-hooks-webhooks-coverage -->
