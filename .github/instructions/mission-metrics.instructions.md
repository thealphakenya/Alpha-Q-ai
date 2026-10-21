---
description: "Use when continuing the Alpha-Q-ai mission, refreshing PH01-PH18 metrics, recording checkpoints, or monitoring task progress. Defines the shared dashboard lifecycle and local-versus-remote evidence rules."
---

# Mission metrics and monitoring

The canonical mission mirror is [MISSION.md](../../MISSION.md); phase metrics must stay subordinate to its requirements.

## Authoritative state

- Use `latest mission.md` as the canonical phase source and `ollamatracks/mission-task-ledger.json` as the task, phase, deadline, and checkpoint state.
- Keep canonical phases `PH01`-`PH18` separate from legacy requirement tasks `M01`-`M16`.
- Before a continuation or transition, read the current ledger, deadline, branch, worktree, latest checkpoint, and append-only evidence. Verify mission mirrors before source-related transitions.
- M01 status is controlled by evidence, not dashboard counts: keep it blocked until the owner/admin-authorized, provenance-checked, read-only branch-policy and effective-permission evidence is bound to both target repositories, their protected refs, and full SHAs. A 403/404 or missing field remains unknown; never infer M01 completion or unblock dependents from a refreshed metric.

## Refresh lifecycle

- Run `python -m scripts.mission_task_ledger --root . refresh-metrics` at continuation start and after material mission changes when an Ollama cycle has not already refreshed the metrics.
- The Ollama `continue`, `autonomous`, and audit-first paths refresh metrics after each agent cycle, including failed cycles. A refresh failure is a failed invocation, not a successful handoff.
- Use the mission-ledger helper for task and phase transitions; its checkpoint writer keeps `oe2.txt`, `remotecompletion.md`, `remote-completion.json`, and `remote-evidence-ledger.jsonl` correlated. Do not manually edit generated metric regions or create a second checkpoint writer.
- A metrics refresh updates the phase catalog and paired evidence; it does not change phase/task status, authorize work, restart a clock, or prove completion.

## Evidence and monitoring limits

- Report all 18 phase statuses, supported current metrics, deadline state, correlation ID, blockers, and next action from the latest observed checkpoint. Use `NOT_MEASURED` for unavailable measurements and preserve `remote_verified: false` without independently verified terminal evidence for the exact repository, ref, SHA, and tree.
- A scheduled workflow or configured trigger is not proof it ran, loaded the canonical ledger, resumed a task, or reached a terminal result. Treat monitoring as active only during an observed local or hosted execution; do not imply that Copilot Chat runs indefinitely or that a daemon exists unless verified.
- Continue only through authorized, bounded cycles. At an expiry, authorization gate, unavailable runtime, or exhausted safe queue, preserve the blocker and resume action instead of spinning, restarting time, or marking phases complete.
- Ollama may be the primary executor only when its approved runtime is verified. If unavailable, record the limitation and do not claim inference, execution, or Ollama usage. A proposed Copilot-billing percentage is not a measured guarantee or reason to weaken validation.
- Passing all phase dashboards alone is not mission completion. Require each acceptance criterion, implementation, tests, security review, and separately gated remote evidence required by the mission.
