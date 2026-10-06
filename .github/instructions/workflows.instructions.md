# Workflow instructions

## Default model

Use GitHub Actions for heavy validation, artifact generation, and release workflows. Keep the local Codespace responsible for orchestration, inspection, and lightweight validation.

## Required safeguards

- Validate workflow YAML and triggers before dispatch.
- Check required permissions, reuse, and concurrency.
- Ensure every run is tied to an exact SHA.
- Require terminal workflow conclusions before treating runs as success.
- Record workflow IDs, jobs, and artifact hashes with the evidence ledger.

## Completion rule

A workflow run is not completion. A terminal result plus independently verified remote state is required.

The autonomous agent must bind every queued or dispatched job to the exact repository/ref/SHA, preserve the run ID and result, resume from checkpoints, and stop at authorization or unavailable-evidence blockers without retrying indefinitely.

## GitHub App workflow contract

- For cross-repository reads, prefer `actions/create-github-app-token@v3` with an owner and explicit repository list and only the minimum read permissions. Do not use Codespaces secrets in Actions; configure Actions variables/secrets separately and verify their setup via authorized metadata/read-only checks.
- Keep the `github.token` or user-token fallback explicit and mark the selected credential role in value-free evidence. No fallback converts `AUTH_BLOCKED` into success without identity and endpoint verification.
- App-key rotation must be confirmed before token minting if the former key was exposed. Never print, persist, or artifact the private key or generated token; allow short-lived tokens to expire/revoke with the job.
- Copilot Chat should request target-owned workflows or approved integrations, not collect credential values. Every workflow result remains bound to exact repo/ref/SHA and a terminal conclusion.
