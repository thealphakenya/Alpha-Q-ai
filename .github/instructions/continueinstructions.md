# Continue Mission

Follow [Mission metrics and monitoring](mission-metrics.instructions.md) for the paired PH01-PH18 dashboard, machine evidence, and limits on automatic continuation.

This file is a human-readable continuation prompt. The workspace instruction that Copilot Chat can discover on a `continue` or `resume` request is [continue.instructions.md](continue.instructions.md).

Use this request to resume the Alpha-Q-ai mission in this workspace:

> Continue from the freshest verified checkpoint. Read the current ledger for actual clock state, remaining time, dependencies, and blockers; do not trust fixed status text or historical summaries. Select bounded, highest-priority safe work, avoid idle pauses while independent safe work remains, and do not skip acceptance checks or exceed bounded retry limits for speed. Avoid sleep/busy-poll loops and duplicate work; when a long tool is running, use completion notifications and only do independent work without shared writers. On every continuation, refresh the complete PH01-PH18 dashboard and all feature metrics supported by current evidence in both `oe2.txt` and `remotecompletion.md`; mark unavailable metrics `NOT_MEASURED` and update paired machine evidence under one correlation ID. If the user explicitly authorizes continuation after expiry, start a distinct run through the supported `new-run` command, preserving the prior clock and statuses. If the safe queue is exhausted or an authority/remote gate blocks all remaining tasks, record the precise blocker and next action and yield promptly. Do not restart an expired clock without that explicit authorization, alter task/phase status to force progress, or claim remote completion without exact independently verified repo/ref/SHA evidence.

If this repository is not open in the current workspace, Copilot cannot inspect its local mission state; open the repository or provide the correct workspace rather than assuming prior-session context is available.