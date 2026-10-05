# AUTODEV.md - Autonomous Development Framework

## Overview
This document formalizes how the QMOI automation stack should behave while operating autonomously across repositories and validation workflows.

## Autonomous Capabilities
- read and apply instructions from repo docs
- monitor workflow health
- repair broken scripts and YAML
- self-resume after interruption
- validate app and platform matrix
- maintain documentation inventory
- synchronize repo state across branches and repos

## Execution Model
1. Detect repository state
2. Validate core contracts
3. Repair missing or corrupted files
4. Run validation suite
5. Record checkpoints
6. Update docs and progress markers
7. Push or prepare PR state when appropriate

## Success Criteria
The autonomous development process is considered successful when:
- tests pass
- doc inventory is complete
- workflows are valid
- recovery logic remains active
- repo state remains accessible and consistent

<!-- BEGIN QMOI MANAGED: remote-continuity-and-failover -->
## Agent-managed remote continuity and failover contract

A target-owned workflow can run independently of a Codespace, but it is not independent of its workflow-host provider. Do not claim uninterrupted execution without a separately deployed, authorized worker and a verified failover test.

- Persist execution IDs, source refs/SHAs, idempotent requests, checkpoints, leases, and audit events outside the workspace; resume only after re-reading authoritative state.
- Heartbeat freshness, worker identity, queue age, lock ownership, and provider reachability are separate health signals. Missing/stale telemetry means `STALE` or `OFFLINE`, never `RUNNING`.
- Provider failover requires pre-authorized credentials, least-privilege access, tested data consistency, and a terminal failover exercise. Never silently switch trading venues or move funds when a provider is unavailable.
- On stale market/account data, lost authorization, provider outage, queue duplication, or ledger mismatch, stop new trading orders and preserve read-only monitoring where available.
- External-worker deployment, availability, and disaster recovery remain `not_verified` until exact-host evidence exists.
<!-- END QMOI MANAGED: remote-continuity-and-failover -->
