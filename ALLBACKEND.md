# ALLBACKEND.md - Backend Feature Map

## Purpose
This file captures the repository-level backend and orchestration capabilities used by the QMOI automation stack.

## Backend Feature Areas
- GitHub integration
- workflow orchestration
- validation and proof generation
- branch sync logic
- recovery and resilience coordination
- configuration and environment management

## Automation sync contract

The backend contract is automatically refreshed alongside the style, merge, and
link validation flow. It must cover repository orchestration, app feature
coverage, clone-platform status, link validation, and GitHub workflow evidence.
The backend layer is responsible for keeping the app catalog, inventory files,
style rules, and protected-flow checks synchronized, so every frontend update is
backed by an orchestration and validation path that reflects the actual runtime
and repository state.

## Priority
Backend features must remain consistent with the live automation scripts and the GitHub-hosted PR validation contract.
