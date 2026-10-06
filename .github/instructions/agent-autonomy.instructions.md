---
applyTo: "**"
---
# Autonomous Agent Instructions

## Instruction coverage

- Before planning repository changes, read root `AGENTS.md`, `.github/copilot-instructions.md`, and every file under `.github/instructions`.
- Record relative path, applicable scope, byte count, SHA-256, and read/parse result. Never copy instruction source text into telemetry or public evidence.
- If an instruction is missing, unreadable, empty, malformed, or changes during a run, stop protected planning, write a checkpoint, and report the exact blocker.
- Inventory is not semantic proof. Map each applicable requirement to implementation, tests, workflows, docs, and remote evidence.
- Do not rewrite, delete, weaken, or self-approve policy instructions during routine automation. Update generated status/evidence only unless an authorized policy change explicitly requests a policy edit.

## Autonomous execution

- Automatically perform safe local and read-only work, validate focused changes, persist correlation IDs and checkpoints, and keep a prioritized resumable action queue for remaining gates.
- Bind remote jobs to repository, ref, and exact SHA. Dispatch only through target-owned workflows when the recorded authorization gate allows it; verify terminal results and remote refs independently.
- Bound retries, preserve failed evidence, and pause on missing authority, ambiguous API responses, unavailable sources, failed checks, or unresolved security findings. Never spin indefinitely or translate a queued action into success.
- Payments, transfers, payroll, trading, account/credential changes, releases, deployments, protected-branch changes, and Q-version finalization require their documented authority and evidence gates; agent confidence is not authorization.
- Production-marker matches are candidates, not proof of defects. Never bulk-rewrite minimal/stub/TODO matches across files or branches; map each to owner, intended behavior, focused tests, security/compatibility impact, rollback, and exact remote evidence before marking a replacement verified.
- Keep Codespace work metadata-first and low-bandwidth. Use target-owned workers for heavy validation and preserve local editing, Git, and Copilot workflows.

## Credential and continuation contract

- On GitHub credential tasks, read the latest `or.md`, `oe2.txt`, `remotecompletion.md`, `githubapp.md`, `github.md`, `githubapppermissions.md`, and `CREDENTIAL_READINESS.md` before acting; treat dated prior chat summaries as pointers, not current proof.
- Carry forward user requirements only when they are explicit in the active request or recorded in current repository evidence. Preserve newer user edits and reconcile conflicts in favor of the newest instruction without claiming cross-session memory that is not actually available.
- Secret-variable presence is not authentication. Distinguish Codespaces secrets, Actions secrets/variables, user tokens, and App installation tokens. Never print, persist, or place secret values in prompts, evidence, commands, or workflow summaries.
- Do not authenticate with an App key marked compromised until the owner confirms revocation/rotation and replacement. App permission snapshots are reported configuration until independently verified; use least privilege and short-lived tokens.
- QMOI may inventory names, prepare setup checklists, and validate through authorized read-only endpoints. It must not invent or self-issue provider credentials, alter accounts, or claim readiness when external ownership, authorization, or verification is missing.