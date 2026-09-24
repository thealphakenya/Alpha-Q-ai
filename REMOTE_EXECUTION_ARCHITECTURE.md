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
