# Continue Mission

This file is a human-readable continuation prompt. The workspace instruction that Copilot Chat can discover on a `continue` or `resume` request is [continue.instructions.md](continue.instructions.md).

Use this request to resume the Alpha-Q-ai mission in this workspace:

> Continue the mission from its current verified checkpoint. Read every applicable repository instruction and the canonical mission, inspect `oe2.txt`, `remotecompletion.md`, the mission ledger, and the latest evidence before selecting the next safe, dependency-ready task. On every continuation, refresh the complete PH01-PH18 dashboard and all feature metrics supported by current evidence in both `oe2.txt` and `remotecompletion.md`; record unavailable metrics as `NOT_MEASURED`, and update paired machine checkpoints under the same correlation ID. If the user explicitly authorizes continuation after expiry, establish a distinct run through the supported `new-run` command, preserving the prior clock and all task/phase statuses. Continue safe local work until the queue is exhausted or blocked; remote/protected actions retain their independent authorization gates. Preserve user changes and every unverified requirement, omission, and blocker. Do not claim remote completion without independently verified exact-repository/ref/SHA evidence.

If this repository is not open in the current workspace, Copilot cannot inspect its local mission state; open the repository or provide the correct workspace rather than assuming prior-session context is available.