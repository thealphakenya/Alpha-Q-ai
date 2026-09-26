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

## GitHub App credential handling

- Local App identifiers are stored outside the checkout in `$HOME/.config/alpha-q-ai/github-app/credentials.env` (directory mode `700`, file mode `600`).
- A replacement private key belongs at `$HOME/.config/alpha-q-ai/github-app/private-key.pem` with mode `600`; the previously tracked key is compromised and has been removed locally. Rotate it in GitHub App settings before further App authentication.
- Never print, quote, commit, or paste credential values into chat or logs. Load them only into the process that needs them, use short-lived tokens, and prefer read-only requests unless an explicitly authorized operation requires more.
