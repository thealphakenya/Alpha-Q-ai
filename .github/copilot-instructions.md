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
- Before planning protected work, inventory and read root `AGENTS.md`, this file, and all files under `.github/instructions`; report relative paths, scopes, hashes, and unreadable files without storing instruction text in telemetry.
- The autonomous agent may refresh generated evidence and run safe local/read-only tasks, but must not rewrite or weaken policy instructions, self-authorize protected actions, or convert a queued action into completion without terminal evidence.

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

The Ollama completion engine maintains a resumable, priority-ordered queue for non-passing gates. Retries are bounded and checkpointed. It pauses at explicit authorization or remote-evidence blockers instead of spinning, bypassing policy, or claiming it can replace Copilot Chat or human judgment.

## GitHub App credential handling

- Local App identifiers are stored outside the checkout in `$HOME/.config/alpha-q-ai/github-app/credentials.env` (directory mode `700`, file mode `600`).
- A replacement private key belongs at `$HOME/.config/alpha-q-ai/github-app/private-key.pem` with mode `600`; the previously tracked key is compromised and has been removed locally. Rotate it in GitHub App settings before further App authentication.
- Never print, quote, commit, or paste credential values into chat or logs. Load them only into the process that needs them, use short-lived tokens, and prefer read-only requests unless an explicitly authorized operation requires more.
