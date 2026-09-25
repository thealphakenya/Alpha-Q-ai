# Security instructions

## Fail-closed expectations

- Never weaken security constraints to make validation pass.
- Record security findings explicitly and do not mask them.
- Keep secrets and token values out of logs, prompts, and documentation.
- Respect vulnerable dependency and secrets scanning results until resolved or explicitly classified as external blockers.

## Required policy

All release, merge, and deployment decisions must remain blocked by unresolved security findings until the risk is remediated or the blocker is independently recorded as external and non-actionable.
