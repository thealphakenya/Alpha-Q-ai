# Release instructions

## Release policy

- A release requires a tag or release ID, source SHA, artifact hashes, and published metadata.
- Install and runtime verification must happen before publication claims.
- Keep failed artifacts and successful artifacts separate in evidence.
- Retain release provenance and do not delete evidence to hide a failed attempt.
- Autonomous release planning may run without supervision, but tag, publish, or deploy operations remain blocked until all release gates and explicit authority are verified.

## Required evidence

- release ID
- source SHA
- artifact names and hashes
- verification result
- environment or install test result
- remote retrieval evidence

## GitHub App and credential gate

- Confirm the authenticated actor, credential type, repository scope, and exact source SHA before release preparation or publication. Codespaces secret presence and user-reported App permissions are not authentication or authorization proof.
- Use only owner-confirmed rotated App keys and short-lived installation tokens. Keep Actions and Codespaces secret stores separate, and use the least permission needed by the target-owned workflow.
- Never pass a credential value through Copilot Chat, shell command text, release metadata, logs, or artifacts. Keep releases, deployments, and signing operations blocked when auth, rotation, required checks, or provenance is unresolved.
