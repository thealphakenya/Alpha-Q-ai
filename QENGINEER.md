# QEngineer

QEngineer is the local engineering-control contract for the Alpha-Q-ai mission. It is a source-of-truth for the repository's safe automation, evidence, and review gates. It does not claim remote completion, branch-policy approval, hosted execution, or production deployment.

## Mission execution contract

The QEngineer contract is intentionally local and fail-closed. The autonomous agent may run bounded local validation and research orchestration only when the repository remains in a safe state and the evidence trail is preserved. No requirement below is satisfied by a local dashboard, a plan artifact, or a doc-only mention without implementation, tests, and review evidence.

1. Preserve project state and user work before any automated edit or checkpoint refresh.
2. Keep the mission ledger, phase metrics, and checkpoint evidence correlated through the current run and branch state.
3. Refresh `immediate.md`, `oe2.txt`, `remotecompletion.md`, and the mission ledger together using one correlation ID.
4. Keep `M01`-`M16` and `PH01`-`PH18` separate; never infer mission completion from dashboard counts alone.
5. Treat remote verification as blocked until exact repository/ref/SHA evidence is independently observed and terminal workflow conclusions are available.
6. Preserve explicit `BLOCKED`, `UNKNOWN`, `NOT_MEASURED`, and `NOT_VERIFIED` states instead of converting them into pass states.
7. Continue with the next safe local task while external authorization gates remain unresolved.
8. Resolve the actual blocker before claiming the next stage complete; do not bypass permissions, branch protection, or release gates.

## QVillage and QVirtualLabs requirements

9. Use `QVILLAGE.md` as the QMOI research and evolution handoff contract between local discovery and higher-level project execution.
10. Use `QVIRTUALLABS.md` as the planned engineering-simulation and experiment-planning contract; treat it as a bounded local plan until source reconciliation, tests, and calibration evidence exist.
11. Keep `Qvillageevolutions.md` and `ALLQMOIAUTOEVOLVINGENVS.md` as local evolution-plan and environment-contract references, not proof of execution.
12. Keep QVillage research candidates, benchmark records, model comparisons, and dataset comparisons provenance-bound and review-only until owner approval and independent evidence exist.
13. Ensure QVirtualLabs adapters are built behind isolated bounded workers and a narrow pilot domain selection rather than as a monolithic all-domain solver.
14. Require source reconciliation for the authoritative engineering requirements before a QVirtualLabs domain is treated as implemented or valid.
15. Maintain the distinction between simulated results and physical experiment results; never present one as the other.

## Automation and evidence rules

16. The autonomous agent must update the immediate checkpoint, mission ledger, and related evidence in the same pass when mission state changes.
17. Local QAUDITS and model-comparison inventories are evidence of candidate discovery only; they are not completion or replacement proof.
18. `ollama_autonomous_agent.py` and `qaudits_evolution_planner.py` must keep QEngineer requirements visible in the generated QVirtualLabs and QVillage artifacts without claiming execution or remote success.
19. The system must reflect all relevant source files, metrics, blockers, and next actions in the mission checkpoint and not silently drop unresolved items.
20. Any workflow, branch, release, deployment, secrets change, or financial action remains blocked until explicit authorization and exact-SHA evidence exist.

## Files that QEngineer must keep aligned

The QEngineer workflow keeps the following files synchronized with the mission state and safe operational boundaries:

- `AGENTS.md`
- `.github/copilot-instructions.md`
- `.github/instructions/**`
- `immediate.md`
- `oe2.txt`
- `remotecompletion.md`
- `ollamatracks/mission-task-ledger.json`
- `QVILLAGE.md`
- `QVIRTUALLABS.md`
- `Qvillageevolutions.md`
- `ALLQMOIAUTOEVOLVINGENVS.md`
- `scripts/ollama_autonomous_agent.py`
- `scripts/qaudits_evolution_planner.py`
- `scripts/qaudit_checkpoint.py`

This file is a local contract for progress and evidence integrity. It should be read and refreshed whenever the mission state, QVillage research contract, or QVirtualLabs plan changes. It does not grant permission to branch, deploy, or claim remote completion.
