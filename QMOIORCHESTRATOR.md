# QMOI Orchestrator

## Purpose

QMOI needs a single central orchestration service that continuously inspects every orchestration surface in the repository, prioritizes runtime health, and generates a live improvement backlog for each orchestrator it finds. This central service should act as the executive layer above workflow orchestrators, runner orchestrators, release orchestrators, AI agent orchestrators, network orchestrators, security orchestrators, and styling orchestration components.

## Central service responsibilities

The system must:

- discover every orchestrator-like surface across the repo and archives
- classify orchestrators by domain: network, security, build, release, automation, agent, style, mask, PR, sync, and monitoring
- evaluate health, drift, stale rules, and missing capabilities
- generate an improvement plan for each orchestrator automatically
- prioritize changes by operational risk, revenue impact, security, and runtime stability
- apply safe patching and validation gates before merge
- keep runtime state, memory, and tracker data synchronized
- continuously refresh documentation, reports, and monitoring surfaces
- ensure Ollama autonomous agent tasks are also coordinated via central orchestration logic

## Enhancement backlog: 25 improvement targets

1. Central orchestrator registry
   - Index every orchestrator file, service, workflow, and script in the repo and archive.
   - Keep a registry with last-seen status, owner, domain, and runtime readiness.

2. Automated capability detection
   - Infer capabilities from orchestrator code instead of relying on manual config.
   - Map capabilities to runner requirements and workflow gates.

3. Cross-repo orchestration awareness
   - Include historical repos, active repo, and branch/sync surfaces in the same live dependency map.

4. Source-of-truth runtime authority
   - Declare the GitHub-hosted runner path as the default production authority when local state conflicts with remote state.

5. Unified health model
   - Merge CI health, workflow health, security health, network health, and agent health into one decision model.

6. Autonomous action planner
   - Convert discovered issues into ranked action queues with risk grouping and rollback plans.

7. Batch patch intelligence
   - Group related issues by domain and patch them together to minimize churn and maintain coherence.

8. Dynamic fallback routing
   - Run tasks on alternative runners or fallback workflows when the preferred path fails.

9. Runtime resume continuity
   - Ensure every orchestrator can resume from the last valid checkpoint without losing workflow state.

10. Security-first orchestration
    - Treat security and data leakage as first-class orchestration constraints rather than post-processing checks.

11. Multiplatform orchestration
    - Support Linux, Windows, macOS, Android, iOS, Vercel, GitHub Actions, and web deployment surfaces.

12. Network-aware orchestration
    - Route orchestration actions through known-good network paths, VPN, firewall, and security layers.

13. Mask-aware orchestration
    - Ensure privacy and obfuscation layers remain active when orchestrator tasks involve external traffic, identity-bound data, or agent activity.

14. VPN and tunnel orchestration
    - Integrate VPN state, tunnel health, and route selection into the orchestrator decision loop.

15. QVS integration
    - Connect mask, security, and visibility layers to the QVS decision engine so trust and network actions are aligned.

16. Global send orchestration
    - Add routing logic for push, sync, deploy, and broadcast events across repos, branches, and related platforms.

17. Style-aware orchestration
    - Respect user-specific theme, accessibility, and personalization rules when orchestrators emit UI or platform output.

18. Universal policy enforcement
    - Every orchestrator should validate against UNIVERSALS.md and core safety gates before doing production actions.

19. Drift detection and reconciliation
    - Detect stale config, duplicate workflows, outdated docs, and divergent implementations between live and archived copies.

20. Merge-aware orchestration
    - Include active PR, branch, and merge decision readiness as part of the orchestration health model.

21. Documentation synchronization engine
    - Ensure docs such as QMOINETWORK.md, QMOIMASKS.md, STYLES.md, UNIVERSALS.md, and related docs are refreshed automatically by the orchestrator.

22. Agent expansion loop
    - Let the Ollama autonomous agent discover missing tasks automatically and add them to the orchestrator plan if not already represented.

23. Autonomous self-healing cycle
    - The orchestrator should patch broken workflows, stale YAML, incomplete configs, and invalid release logic without waiting for manual intervention.

24. Evidence and audit trail
    - Every orchestration action must log intent, results, and validation output to a machine-readable artifact.

25. Continuous improvement backlog
    - Generate a rolling backlog of the next 20 actions for each orchestrator and then automatically re-rank it as runtime conditions change.

## Orchestrator domains to cover

The central orchestrator should own and coordinate the following domains:

- workflow orchestration
- build and release orchestration
- CI and validation orchestration
- security scanning orchestration
- network routing and connectivity orchestration
- VPN and tunnel orchestration
- QVS and mask orchestration
- UI and styling orchestration
- financial and ledger orchestration
- repo sync and merge orchestration
- GitHub automation orchestration
- living memory and tracker orchestration
- autonomous agent orchestration

## Required runtime contract

Every orchestrator should expose the same minimum contract:

- name
- domain
- capability list
- trigger sources
- health state
- dependency list
- last validation result
- automatic remediation plan
- merge readiness
- docs sync status

## Improvement loop

The central orchestrator should run in a continuous loop:

1. Discover all orchestrators.
2. Score them for health, risk, and drift.
3. Gather evidence from logs, workflows, and docs.
4. Generate a ranked improvement list.
5. Patch the highest-priority issues with validation gates.
6. Re-scan the repo and update docs and state.
7. Push the revised state when validation is accepted.

## Recommended architecture

- Registry: orchestrator registry file with metadata and state
- Planner: improvement backlog generator for each orchestrator
- Executor: safe patcher and workflow runner
- Validator: test, lint, security, and merge acceptance checks
- Reporter: live stream and monitoring artifact updates
- Memory: live runtime and tracker state for continuity

## Merge integration requirement

Any PR or merge operation must consider the central orchestrator plan. If a PR touches orchestrator, network, VPN, mask, security, or style logic, it must also pass the orchestrator readiness checklist before being considered complete.

## Final objective

The repo should evolve from isolated automation scripts into a single orchestrator-aware operating system: one central decision layer that understands every workflow, network boundary, security gate, style rule, and autonomous loop, and automatically produces the next best improvement set for each orchestrator it finds.

<!-- BEGIN QMOI MANAGED: ollama-full-coverage-audit-status -->
## Agent-managed OFCA status

- Audit name: `OFCA`; local scan status: `INCOMPLETE`.
- Materialized files scanned: `10411`; mention-bearing files: `4148`.
- Local refs: `40`; local commits: `2627`; mention-change commits: `2006`.
- Source manifest SHA-256: `b780d118e7dff7bebb1fa4d11cf8ec895e9e64c21d9c51a5b828926065a70cb0`; full remote-history coverage: `False`.
- QVillage/QVS materialized references: `369` files, `212` Markdown files; remote/history completeness: `not_verified`.
- `prMergeIncluded` is required before merge activity. Unverified remote refs, pull requests, peer roots, and intermediate commit trees remain blockers.
- Next action: Run an authorized target-owned audit for both repositories covering all refs, PRs, and intermediate commit trees; attach terminal exact-SHA evidence before Q-version finalization.
<!-- END QMOI MANAGED: ollama-full-coverage-audit-status -->

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10428`; directories: `1268`; Markdown: `2416`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2109, orchestration=2061, qteam_accountability=2049, release_tag_publish=2088, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2221`; needs review: `187`; metric candidate lines: `52705`; percentage occurrences: `22237`.
- Markdown word count: `3550281`; heuristic sentence count: `673664`; sentence records indexed: `673664`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29834` metric claims; `10658` completion claims; `29737` metric and `10529` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13328`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `39967` lines in `3666` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `286`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
