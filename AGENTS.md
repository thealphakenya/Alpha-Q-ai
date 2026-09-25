# AGENTS.md

This repository is governed by the remote-first completion contract in `remotecompletion.md`.

## Required operating rules

1. Inspect before modifying.
2. Preserve user work and never overwrite uncommitted edits.
3. Prefer local observation and remote validation over local mutation claims.
4. Never force-push, rewrite history, or bypass branch protections.
5. Never print, persist, or expose credentials or tokens.
6. Treat 401/403/404 as ambiguous until proven otherwise.
7. Distinguish dispatch from completion, merge from release, and release from deployment.
8. Record exact SHAs, correlation IDs, and evidence references for every operation.
9. Keep machine-readable evidence current and fail closed when data is missing.
10. Do not declare remote completion without independently verified remote evidence.

## Repository responsibilities

- Maintain safe runtime scaffolding only.
- Prefer target-owned GitHub workflows for heavy or production actions.
- Use local work only for inspection, planning, and lightweight validation.
- Validate with targeted tests first, then full validation when required.
- Keep `remotecompletion.md`, `oe2.txt`, `MERGE.md`, `RELEASES.md`, `ALLVALIDATIONS.md`, and `ALLMDFILESREFS.md` aligned to current evidence.

## Completion gate

Remote completion is only valid when the target-owned workflow and exact remote SHA prove the result. Local success alone is never enough.
