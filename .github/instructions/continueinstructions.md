# Continue Mission

This file is a human-readable continuation prompt. The workspace instruction that Copilot Chat can discover on a `continue` or `resume` request is [continue.instructions.md](continue.instructions.md).

Use this request to resume the Alpha-Q-ai mission in this workspace:

> Continue the mission from its current verified checkpoint. Read every applicable repository instruction and the canonical mission, inspect `oe2.txt`, `remotecompletion.md`, the mission ledger, and the latest evidence before selecting the next safe, dependency-ready task. Preserve user changes, update paired metrics and checkpoints through the supported helpers, and leave every unverified requirement, omission, and blocker explicit. Do not claim remote completion without independently verified exact-repository/ref/SHA evidence.

If this repository is not open in the current workspace, Copilot cannot inspect its local mission state; open the repository or provide the correct workspace rather than assuming prior-session context is available.