---
description: "Use when the user says continue or resume, or asks to carry on the Alpha-Q-ai mission. Resume from verified local mission evidence and update paired checkpoints without bypassing authorization or remote-proof gates."
---

# Mission Continuation

When the user says `continue`, resume safe work in this repository. A continuation request authorizes local, read-only, and otherwise policy-permitted work; it does not authorize credentials, remote mutations, protected operations, releases, deployments, or financial actions.

## Resume

- Confirm the repository root, current branch, worktree status, and any active process. Preserve all existing user changes and generated artifacts unless the task explicitly authorizes their replacement.
- Read `AGENTS.md`, `.github/copilot-instructions.md`, and every file under `.github/instructions`. Record each instruction's relative path, applicable scope, byte count, SHA-256, and read/parse result in supported evidence; never copy instruction source text into telemetry.
- Read `latest mission.md`, `oe2.txt`, `remotecompletion.md`, and the current `ollamatracks/mission-task-ledger.json`. Check the latest paired checkpoint and append-only evidence events. Treat historical notes as pointers, not current proof.
- Validate mission mirrors and source hashes. If they differ, do not perform phase/task transitions; use `python -m scripts.mission_task_ledger --root . sync-mission` only when adopting the current canonical source is explicitly authorized.
- Check the actual mission deadline before transitions. Do not restart or extend an expired clock, infer process-active time from wall time, or convert stale `IN_PROGRESS` entries into success.

## Execute

- Select the earliest dependency-ready, highest-priority safe local task. State one falsifiable local hypothesis and one focused validation check before a code edit.
- Inspect the owning implementation, nearby tests, and applicable docs. Make the smallest coherent change, then run the focused test immediately; broaden validation only when the result and risk justify it.
- For long inventories, use bounded resumable shards. Persist `IN_PROGRESS` before work, finalize under the same correlation ID, preserve omissions, and stop gracefully if measurable progress stalls. Do not run competing writers against shared audit artifacts.
- Treat indexes, keyword matches, path/hash scans, feature names, and archive matches as candidates, not semantic proof. Do not bulk-rewrite candidate files or create placeholder docs to make an inventory pass.
- Keep Ollama availability, model inference, tests, local checks, remote CI, and production verification as distinct measured states. Mark unavailable measurements `NOT_MEASURED` or `BLOCKED`.

## Evidence And Handoff

- The Ollama `autonomous`, `audit-first`, and `continue` CLI paths refresh the canonical PH01-PH18 metrics after each agent cycle through `scripts.mission_task_ledger`; a refresh failure fails the invocation rather than being reported as success. This refresh does not mark phases complete, restart an expired mission clock, or prove remote completion.
- Before resuming, `continue` records a read-only plan of all 18 phases, all M01-M16 dependency states, and every indexed mission line, including lines not assigned to a phase. The plan may rank a candidate but never authorizes execution or changes status; an expired clock pauses task transitions until a separately authorized mission run is established.
- Refresh the phase dashboard with `python -m scripts.mission_task_ledger --root . refresh-metrics` after mission-catalog changes. Record operations through the supported QAUDITS/checkpoint writer so `oe2.txt`, `remotecompletion.md`, `remote-completion.json`, and `remote-evidence-ledger.jsonl` stay correlated.
- Record actual commands, pass/fail/skip counts, durations, artifact paths and hashes, scope, exclusions, blockers, deadline state, and next action. Keep `remote_verified` false until target-owned terminal evidence independently proves the exact repository, ref, SHA, and tree.
- Before changing an instruction or mission source, inspect its current worktree diff and preserve authored/user content. Instruction policy changes require an explicit user request; generated status updates do not justify weakening policy.
- End each continuation with tested changes, unverified scope, blockers, and the next concrete action. Do not say the mission is complete while mandatory requirements or remote gates remain unresolved.
- If the repository is not present in the current workspace, state that its local mission state cannot be inspected; do not invent cross-session memory or claim automatic continuation in an unopened workspace.