---
description: "Use when the user says continue or resume, or asks to carry on the Alpha-Q-ai mission. Resume from verified local mission evidence and update paired checkpoints without bypassing authorization or remote-proof gates."
---

# Mission Continuation

Follow [Mission metrics and monitoring](mission-metrics.instructions.md) for the paired PH01-PH18 dashboard, machine evidence, and limits on automatic continuation.

The canonical mission mirror is [MISSION.md](../../MISSION.md); this continuation instruction does not supersede it.

When the user says `continue`, resume safe work in this repository. A continuation request authorizes local, read-only, and otherwise policy-permitted work; it does not authorize credentials, remote mutations, protected operations, releases, deployments, or financial actions.

## Resume

- Determine continuation status and remaining time from the current mission ledger and latest checkpoint on every run. Do not rely on a fixed clock claim in this instruction or historical notes. Remote completion and protected actions remain blocked until their exact evidence and authority gates pass.
- Confirm the repository root, current branch, worktree status, and any active process. Preserve all existing user changes and generated artifacts unless the task explicitly authorizes their replacement.
- Read `AGENTS.md`, `.github/copilot-instructions.md`, and every file under `.github/instructions`. Record each instruction's relative path, applicable scope, byte count, SHA-256, and read/parse result in supported evidence; never copy instruction source text into telemetry.
- Read `latest mission.md`, `oe2.txt`, `remotecompletion.md`, and the current `ollamatracks/mission-task-ledger.json`. Check the latest paired checkpoint and append-only evidence events. Treat historical notes as pointers, not current proof.
- Validate mission mirrors and source hashes. If they differ, do not perform phase/task transitions; use `python -m scripts.mission_task_ledger --root . sync-mission` only when adopting the current canonical source is explicitly authorized.
- Check the actual mission deadline before transitions. Do not restart or extend an expired clock, infer process-active time from wall time, or convert stale `IN_PROGRESS` entries into success.
- When the user explicitly authorizes continuation after expiry, establish a distinct run with `python -m scripts.mission_task_ledger --root . new-run --authorization-ref <short-non-secret-reference>`. The helper must archive the expired run with its correlation ID and original clock, preserve all task/phase statuses, create a fresh correlation ID and 120-minute clock, and keep remote/protected actions independently gated. Never reset the old clock in place.

## M01 Branch-Policy Gate

- Keep M01 `BLOCKED` until current, owner/admin-authorized, read-only evidence covers both `thealphakenya/Alpha-Q-ai` and `thealphakenya/qmoi-enhanced`.
- For each repository, bind evidence to the exact repository name, protected branch/ref and full SHA; capture the effective branch protection and organization rulesets, authenticated actor and credential category, effective permissions relevant to the requested action, read-only method/endpoint and response status, capture time, provenance, and evidence artifact hash.
- An HTTP 403/404, token presence, user assertion, stale screenshot, workflow dispatch, or local test is not proof of policy or permission. Treat unavailable or ambiguous fields as `UNKNOWN`; do not transition M01 or start dependent tasks on that basis.
- Record only redacted, value-free evidence references through the mission ledger. Never store tokens, private keys, or secret values. If owner/admin evidence is unavailable, checkpoint the exact blocker and continue only independent safe tasks; yield if the safe queue is empty.

## GitHub App Credential Gate

- Treat reported Actions-secret presence as `USER_REPORTED`; the current user `GITHUB_TOKEN` is not App authentication. Never inspect or print secret values.
- Do not use the historically exposed App key until the owner confirms revocation/rotation and installation of its replacement. Before App-token minting, the target-owned preflight also requires `QMOI_APP_KEY_ROTATION_CONFIRMED=true` in that repository's Actions variables. This variable is an owner attestation, not independent proof of key rotation.
- Use only the target-owned preflight's short-lived, least-privilege installation token for read-only identity/repository/workflow checks. No PAT or `GITHUB_TOKEN` fallback is allowed for an App-authenticated result. Missing confirmation, failed token mint, or 401/403/404 remains `APP_AUTH_BLOCKED`/`UNKNOWN`; keep M01 and dependent tasks blocked.

## Execute

- Select the earliest dependency-ready, highest-priority safe local task. State one falsifiable local hypothesis and one focused validation check before a code edit.
- Inspect the owning implementation, nearby tests, and applicable docs. Make the smallest coherent change, then run the focused test immediately; broaden validation only when the result and risk justify it.
- If the highest-priority task is blocked by an external authority or remote-evidence gate, keep that task blocked and continue with the next independent safe local/read-only task. Stop only when the safe queue is exhausted or all remaining tasks require the unresolved gate; never change status or authorization to force progress.
- Be time-aware without becoming success-driven: read the ledger's actual `remaining_seconds`, prioritize bounded critical-path work, and checkpoint measured progress. Do not idle while independent safe work remains, but do not skip acceptance checks to fit a time budget. Avoid sleep/busy-poll loops; use tool completion notifications, and perform concurrent work only when it cannot contend for shared files, locks, or evidence writers. If the safe queue is exhausted or the clock closes, persist the blocker and next action, then yield without restarting the clock.
- For long inventories, use bounded resumable shards. Persist `IN_PROGRESS` before work, finalize under the same correlation ID, preserve omissions, and stop gracefully if measurable progress stalls. Do not run competing writers against shared audit artifacts.
- Treat indexes, keyword matches, path/hash scans, feature names, and archive matches as candidates, not semantic proof. Do not bulk-rewrite candidate files or create placeholder docs to make an inventory pass.
- Keep Ollama availability, model inference, tests, local checks, remote CI, and production verification as distinct measured states. Mark unavailable measurements `NOT_MEASURED` or `BLOCKED`.

## Evidence And Handoff

- The Ollama `autonomous`, `audit-first`, and `continue` CLI paths refresh the canonical PH01-PH18 metrics after each agent cycle through `scripts.mission_task_ledger`; a refresh failure fails the invocation rather than being reported as success. This refresh does not mark phases complete, restart an expired mission clock, or prove remote completion.
- Before resuming, `continue` records a read-only plan of all 18 phases, all M01-M16 dependency states, and every indexed mission line, including lines not assigned to a phase. The plan may rank a candidate but never authorizes execution or changes status; an expired clock pauses task transitions until a separately authorized mission run is established.
- On every continuation, refresh the complete PH01-PH18 dashboard and all feature metrics supported by current evidence in both `oe2.txt` and `remotecompletion.md` using `python -m scripts.mission_task_ledger --root . refresh-metrics` and the supported QAUDITS/checkpoint writer. Record unavailable feature metrics as `NOT_MEASURED`; keep one correlation ID across `oe2.txt`, `remotecompletion.md`, `remote-completion.json`, and `remote-evidence-ledger.jsonl`. This refresh does not change phase status, authorize transitions, restart an expired clock, or prove completion.
- Record actual commands, pass/fail/skip counts, durations, artifact paths and hashes, scope, exclusions, blockers, deadline state, and next action. Keep `remote_verified` false until target-owned terminal evidence independently proves the exact repository, ref, SHA, and tree.
- Treat time remaining as scheduling information, never as authorization or proof. Mark unavailable time estimates or process-active durations `NOT_MEASURED`; do not promise every phase will finish within an arbitrary short window.
- Before changing an instruction or mission source, inspect its current worktree diff and preserve authored/user content. Instruction policy changes require an explicit user request; generated status updates do not justify weakening policy.
- End each continuation with tested changes, unverified scope, blockers, and the next concrete action. Do not say the mission is complete while mandatory requirements or remote gates remain unresolved.
- If the repository is not present in the current workspace, state that its local mission state cannot be inspected; do not invent cross-session memory or claim automatic continuation in an unopened workspace.