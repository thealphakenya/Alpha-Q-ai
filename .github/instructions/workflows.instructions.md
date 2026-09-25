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
