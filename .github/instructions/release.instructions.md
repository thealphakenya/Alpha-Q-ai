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
