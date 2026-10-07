p# Remote Execution Architecture

This repository uses a remote-first control plane for autonomous production work.
A Codespace or local checkout is a submission and observation surface only. It
must not be treated as the authoritative executor of GitHub mutations.

## Authority boundaries

| Operation | Workspace | Target repository runner |
| --- | --- | --- |
| Inspect local intent and source SHA | allowed | rechecked remotely |
| Submit an execution request | allowed | receives authenticated request |
| Push, branch sync, PR, merge | forbidden | owns through GitHub Actions/API |
| Security, tests, build and runtime gates | advisory only | authoritative |
| Q-version and evidence publication | observe only | authoritative |
| Final success verdict | forbidden | deterministic completion engine |

The target workflow must use its own `GITHUB_TOKEN` or an explicitly
preflighted GitHub App installation. A source repository token is never used
to write the target repository. HTTP 403 is an authorization blocker, not a
retryable success state.

## Request lifecycle

1. The workspace creates a unique `sync_id` and sends a `workflow_dispatch` request.
2. The target repository records the request and acquires its repository lock.
3. The target runner re-fetches the immutable source SHA and validates branch,
   authorization, source ownership, protected-branch policy and change scope.
4. The target runner executes tests, security checks, build/runtime checks,
   PR/check/merge policy and cross-repository verification.
5. The target runner publishes JSONL events, current state, checkpoint and
   Q-version evidence as GitHub artifacts and repository-tracked evidence.
6. A reconnecting workspace observes the remote run and never replaces its
   state with local assumptions.

## Remote observability

Every event contains an execution identity, correlation identity, repository,
branch, SHA, workflow/run URL, stage, status, sequence, timestamp and heartbeat.
`RUNNING` is valid only while the latest heartbeat is within the configured
freshness threshold. Otherwise the monitor reports `STALE`, `OFFLINE`, or
`FAILED`.

## Local commands

```text
python scripts/qmoictl.py remote-submit --target-repository OWNER/REPO \
  --direction alpha-to-qmoi --source-repository OWNER/SOURCE \
  --source-sha SHA --mode dry-run
python scripts/qmoictl.py remote-observe --target-repository OWNER/REPO --run-id RUN_ID
python scripts/qmoictl.py status
```

`remote-submit` only dispatches a target-owned workflow. `remote-observe` is
read-only. `autonomous_complete` and `verify` remain fail-closed when remote
main, backup, security, cross-repository, Q-version, live-activity or final
verification evidence is absent.

## Codespace independence

The authoritative request and checkpoint must survive Codespace shutdown. A
reopened workspace queries remote workflow state, artifacts and the target
repository’s current state. It must preserve local modifications and must not
perform destructive checkout, force-push, direct protected-branch writes or
blind branch replacement.

<!-- BEGIN QMOI MANAGED: remote-continuity-and-failover -->
## Agent-managed remote continuity and failover contract

A target-owned workflow can run independently of a Codespace, but it is not independent of its workflow-host provider. Do not claim uninterrupted execution without a separately deployed, authorized worker and a verified failover test.

- Persist execution IDs, source refs/SHAs, idempotent requests, checkpoints, leases, and audit events outside the workspace; resume only after re-reading authoritative state.
- Heartbeat freshness, worker identity, queue age, lock ownership, and provider reachability are separate health signals. Missing/stale telemetry means `STALE` or `OFFLINE`, never `RUNNING`.
- Provider failover requires pre-authorized credentials, least-privilege access, tested data consistency, and a terminal failover exercise. Never silently switch trading venues or move funds when a provider is unavailable.
- On stale market/account data, lost authorization, provider outage, queue duplication, or ledger mismatch, stop new trading orders and preserve read-only monitoring where available.
- External-worker deployment, availability, and disaster recovery remain `not_verified` until exact-host evidence exists.
<!-- END QMOI MANAGED: remote-continuity-and-failover -->

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
