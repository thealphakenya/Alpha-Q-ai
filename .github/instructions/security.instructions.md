# Security instructions

## Fail-closed expectations

- Never weaken security constraints to make validation pass.
- Record security findings explicitly and do not mask them.
- Keep secrets and token values out of logs, prompts, and documentation.
- Respect vulnerable dependency and secrets scanning results until resolved or explicitly classified as external blockers.

## Required policy

All release, merge, and deployment decisions must remain blocked by unresolved security findings until the risk is remediated or the blocker is independently recorded as external and non-actionable.

The autonomous agent may collect read-only diagnostics and propose bounded remediation, but it cannot downgrade, suppress, or self-approve a security finding to keep the workflow moving.

## GitHub App and secret handling

- Treat a user-provided App permission screenshot or Markdown snapshot as reported evidence, not current effective permission proof. Review broad grants, especially administration, secrets, workflow writes, alert dismissal, and push-protection bypass requests; grant only what an approved feature needs.
- Never expose, paste, or log secret values. Codespaces secrets, Actions secrets/variables, PATs, and App installation tokens are distinct credential sources.
- Do not use a key classified as compromised until the owner confirms it was revoked/rotated and a replacement is installed. Presence alone does not verify rotation, identity, scope, or validity.
- Do not fabricate, self-issue, or silently rotate external provider credentials. Automate name-only inventory and provisioning guidance; require provider/owner-controlled issuance and read-only verification before use.
- Copilot Chat and Ollama must not receive private keys or tokens in context. Use approved tooling or target-owned workflows that mint short-lived least-privilege tokens and emit value-free evidence.
