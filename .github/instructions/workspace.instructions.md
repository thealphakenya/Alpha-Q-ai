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
- For App work, preserve user-authored credentials notes and inspect `githubapppermissions.md` as a reported snapshot; record whether each fact is user-reported, locally observed, or remotely verified.
- Keep `or.md`, `oe2.txt`, `githubapp.md`, `github.md`, `CREDENTIAL_READINESS.md`, and `remotecompletion.md` aligned on current App variable presence, installation-ID availability, rotation state, secret-list access, and exact local/remote SHA.
- Do not claim Copilot Chat or Ollama can authenticate merely because a Codespaces secret is present. Use a value-free preflight, approved secret source, short-lived scoped token, and independent identity/API evidence; preserve `AUTH_BLOCKED` when any gate is unavailable.
- Never overwrite dirty user work or replace missing remote configuration with inferred credentials. QMOI may automate inventories and setup checklists, but provider-issued values require authorized owner/provider action.

## Required files

- `remotecompletion.md`
- `oe2.txt`
- `MERGE.md`
- `RELEASES.md`
- `ALLVALIDATIONS.md`
- `ALLMDFILESREFS.md`
