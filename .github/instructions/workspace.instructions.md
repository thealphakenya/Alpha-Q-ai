# Workspace instructions

## Purpose

Keep the workspace safe, deterministic, and consistent with the repository’s remote-first policy.

## Required behavior

- Prefers metadata, hashes, and deltas over large downloads.
- Respect user edits and active locks.
- Use narrow validation before broad validation.
- Track local and remote divergence explicitly.
- Separate “planned” status from “verified” status.
- Inventory and read all repository instructions before protected work; record path, scope, hash, and read outcome without copying policy text into telemetry.
- Preserve human-authored instructions; automation may update generated status and evidence only unless an authorized policy change explicitly says otherwise.
- Keep autonomous retries bounded and checkpointed; retain authorization blockers instead of spinning or self-approving.

## Required files

- `remotecompletion.md`
- `oe2.txt`
- `MERGE.md`
- `RELEASES.md`
- `ALLVALIDATIONS.md`
- `ALLMDFILESREFS.md`
