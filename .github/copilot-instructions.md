# Copilot instructions

This repository follows the remote-first completion and evidence model described in `remotecompletion.md`.

## Law of the repository

- Local code changes do not prove remote success.
- Missing remote evidence is a blocker, not a pass.
- Protected branches, required checks, and existing GitHub policy must be respected.
- Do not fabricate progress, SHAs, approvals, releases, deployments, or parity claims.

## Safety rules

- Never expose credentials, tokens, or secrets.
- Never bypass rulesets, branch protections, or user approvals.
- Never force-push or rewrite shared history.
- Never infer remote completion from local commits.
- When a workflow or API returns 401/403/404, record it as diagnostic evidence and continue safely.

## Required artifacts

Keep these artifacts current and honest:

- `remotecompletion.md`
- `oe2.txt`
- `MERGE.md`
- `RELEASES.md`
- `ALLVALIDATIONS.md`
- `ALLMDFILESREFS.md`
- `remote-completion.json`
- `remote-evidence-ledger.jsonl`

## Evidence policy

Every operation should leave:

- a correlation ID;
- a repository and ref;
- status and result;
- relevant SHA(s);
- verification level; and
- an explicit blocker or next action when remote proof is unavailable.
