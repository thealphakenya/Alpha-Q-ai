# QMOI checkpoint undo and redo

## Purpose and boundaries

Undo/redo gives the autonomous agent a controlled way to revisit its resumable lifecycle state. It complements restore points, but it does not replace Git history, a backup branch, or the `qmoi` restore-point branch.

`CheckpointManager.undo()` and `CheckpointManager.redo()` move the cursor over a bounded history of up to 50 distinct state snapshots for one execution ID. Writes are atomic; a new state after undo discards the redo branch. Unreadable or malformed checkpoint/history data raises an error instead of silently resetting state. The state history is stored in the checkpoint JSON and `load()` returns the current public checkpoint state without exposing manager metadata.

**These APIs only change orchestration/checkpoint JSON. They do not revert or reapply project files, Git commits, branches, Q versions, credentials, database records, financial transactions, releases, or deployments.** A checkpoint transition must never be described as a project rollback.

## Safe usage

```python
from pathlib import Path

from scripts.checkpoint_manager import CheckpointManager

manager = CheckpointManager(Path("."))
current = manager.load("execution-id")
history = manager.history_status("execution-id")

if history["undo_available"]:
    manager.undo("execution-id")

# Inspect the restored state and rerun its required local validation before continuing.
restored = manager.resume_state("execution-id")
history = manager.history_status("execution-id")

if history["redo_available"]:
    manager.redo("execution-id")
```

Use the same stable execution ID to inspect and continue one run. Review the checkpoint and its evidence before undo or redo; rerun any gate whose source SHA, manifest hash, dependencies, or environment has changed. Never place tokens, private keys, account secrets, or sensitive user data in checkpoint fields. Treat the JSON as operational state, not an authorization grant.

## Project recovery tiers

1. **Lifecycle-state undo/redo:** move the checkpoint cursor to a previously recorded agent state. Validate the restored state against current source and policy before continuing.
2. **Local project-file recovery:** inspect `git status`, diff, file hashes, and the last verified checkpoint. Recover changes with a deliberate, reviewable patch or new commit. Do not run `git reset`, force-push, or overwrite uncommitted user work as an automatic undo.
3. **Repository restore point:** use the target-owned, authorized restore-point workflow. It must verify exact source SHA and tree, both repositories, branch policy, clean state, required evidence documents, and terminal successful workflow evidence. It is fast-forward-only; divergence is a blocker, not a reason to overwrite history.
4. **External side effects:** database changes, user/account settings, credentials, payments, trades, releases, or deployments require their own compensating operation and explicit authority. A Git revert or checkpoint undo cannot reverse those effects.

## Autonomous agent integration

Before an agent resumes a project or advances a Q-version stage, it should:

- record the execution ID, repository/ref/SHA, correlation ID, manifest hash, current stage, action queue, retry budget, and gate outcomes;
- use checkpoint undo/redo only to select lifecycle state, then re-check instructions, source manifests, current files, and blockers;
- take a new verified restore point before a separately authorized change when the owning workflow requires it;
- perform changes in bounded, reviewable units, preserving user changes and recording before/after hashes and tests;
- redo only when the next recorded state is still valid for the current source and policy; otherwise start a new checkpoint branch/state rather than replaying stale actions;
- retain failures and partial outcomes; do not turn a queued action, local pass, restore-point name, or dispatch acceptance into completion; and
- pause for human/provider authorization on protected branches, credentials, finance/trading, releases, deployments, or other high-impact actions.

For projects, QMOI should checkpoint discovery and plan state before implementation, record test and audit results after each bounded change, and use an independently verified restore point for repository-level recovery. Undo a bad plan/state and reassess; do not mechanically undo user-authored changes. For financial or trading projects, checkpoints may retain only value-free IDs, source timestamps, and hashes; reconciliation and provider-authorized compensating actions are required for real account-side effects.

## Automatic recovery decisions and interface requirements

The agent may automatically move the checkpoint cursor only for local lifecycle-state navigation, with the cause recorded:

- **Undo:** return to a prior checkpoint after failed local validation or invalid resumable state only when history is readable and current source/policy fingerprints are recorded. Re-run affected validation before continuing. This does not revert files or erase failure evidence.
- **Redo:** replay a recorded state only when repository/ref, source manifest, instruction hashes, and prerequisite gates still match. If an identity is stale or unavailable, do not replay; create a new checkpoint state and re-plan.
- **Restore point:** a stale heartbeat alone never triggers restore. Consider restore only after repository loss or corruption is confirmed, then require the authorized target-owned workflow, clean exact-SHA/tree evidence for both repositories, fast-forward safety, and required approvals. Divergence remains blocked.
- **External effects:** never automatically undo/redo payments, trades, credentials, account settings, deployments, releases, or user data. Provider-owned compensating actions require explicit authority.

Every recovery decision records its reason, execution/correlation IDs, before/after checkpoint fingerprints, source SHA/manifest, validation result, and next action. Missing, stale, malformed, or conflicting signals yield `UNKNOWN` or `BLOCKED`, not a guessed recovery. Evidence ledgers remain append-only.

Any future chat UI must bind undo/redo controls only to `CheckpointManager.history_status()` and the selected execution ID. Controls need accessible names, tooltips, disabled states, and a clear notice that checkpoint navigation changes lifecycle state only. No active chat UI exists in this checkout, so those controls remain `unmapped`, not shipped.

Hands-free/voice input may navigate, read status, or prepare a draft within granted permissions. It must not bypass identity, consent, explicit confirmation, or protected-action gates. Ambiguous speech, low confidence, missing permissions, or stale health stops the action for clarification or human review.

## Retention, integrity, and recovery checks

- At most 50 distinct checkpoint snapshots are retained per execution ID; when the cap is reached, the oldest snapshots age out. This is not an archive or disaster-recovery guarantee.
- Corrupt, missing, malformed, or out-of-range history is an explicit blocker. Preserve the file for diagnosis and recover from a separately verified source; do not silently initialize a replacement history.
- Undo/redo availability is reported by `history_status()` with retained/max snapshot counts; it does not imply that the corresponding source files still exist or that their hashes match.
- Test undo, redo, new-write-after-undo branching, retention, malformed JSON handling, and filesystem recovery behavior. Record test outcomes and the exact source manifest in QAUDITS.
- Never undo audit/evidence history to conceal a failure. Evidence ledgers remain append-only; checkpoint navigation changes only the current resumable state.

## Relationship to audit and Q versions

[QAUDITS.md](QAUDITS.md) measures checkpoint freshness, integrity, retained depth, restore-test status, and recovery scope. [QVERSIONMANAGER.md](QVERSIONMANAGER.md) requires exact source/remote evidence for finalization; an undo/redo action or checkpoint snapshot cannot satisfy a Q-version gate. The `qmoi` ref is a restore point only under its authorized target-workflow contract, not a branch on which the agent may independently rewrite history.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10446`; directories: `1270`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2156, build_download_install=2110, orchestration=2062, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2001`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52718`; percentage occurrences: `22237`.
- Markdown word count: `3554796`; heuristic sentence count: `674081`; sentence records indexed: `674081`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29838` metric claims; `10664` completion claims; `29741` metric and `10535` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9047` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13342`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40052` lines in `3673` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `290`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
