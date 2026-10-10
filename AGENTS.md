# AGENTS.md

This repository is governed by the remote-first completion contract in `remotecompletion.md`.

## Required operating rules

1. Inspect before modifying.
2. Preserve user work and never overwrite uncommitted edits.
3. Prefer local observation and remote validation over local mutation claims.
4. Never force-push, rewrite history, or bypass branch protections.
5. Never print, persist, or expose credentials or tokens.
6. Treat 401/403/404 as ambiguous until proven otherwise.
7. Distinguish dispatch from completion, merge from release, and release from deployment.
8. Record exact SHAs, correlation IDs, and evidence references for every operation.
9. Keep machine-readable evidence current and fail closed when data is missing.
10. Do not declare remote completion without independently verified remote evidence.
11. Before planning protected work, inventory and read root `AGENTS.md`, `.github/copilot-instructions.md`, and all files under `.github/instructions`; store only paths, scopes, hashes, and outcomes in machine evidence.
12. Preserve instruction files as policy. Automation may refresh generated status/evidence but must not silently rewrite or weaken instructions.
13. Resume only from verified checkpoints; keep safe work automatic and leave authorization-gated remote, release, deployment, credential, and financial operations blocked until their evidence and authority gates pass.

## Repository responsibilities

- Maintain safe runtime scaffolding only.
- Prefer target-owned GitHub workflows for heavy or production actions.
- Use local work only for inspection, planning, and lightweight validation.
- Validate with targeted tests first, then full validation when required.
- Keep `remotecompletion.md`, `oe2.txt`, `MERGE.md`, `RELEASES.md`, `ALLVALIDATIONS.md`, and `ALLMDFILESREFS.md` aligned to current evidence.

## Completion gate

Remote completion is only valid when the target-owned workflow and exact remote SHA prove the result. Local success alone is never enough.

## QAUDITS execution and evidence

- Use the documented QAUDITS commands for repository-surface, Markdown-integrity, and coverage refreshes. Bind each run to its repository, ref, local commit/tree, correlation ID, measured duration, status, metrics, omissions, unreadable/skipped paths, and next action.
- Long `audit-inventory` runs write a paired `IN_PROGRESS` checkpoint before scanning and finish under the same correlation ID; interruption must leave a visible unfinished state.
- Treat indexes, hashes, claim candidates, and structural checks as local evidence only. Heuristic scans do not establish semantic correctness, feature completion, or exhaustive coverage when any scope is omitted or unreadable.
- Keep `oe2.txt`, `remotecompletion.md`, `remote-completion.json`, and `remote-evidence-ledger.jsonl` aligned using the supported checkpoint writer; preserve matching correlation IDs and record explicit local-versus-remote verification levels.
- The `audit-inventory` financial pass discovers amount/currency, revenue, payment, wallet/banking, deals, employment/payroll, jurisdiction, project-budget, and security candidates without persisting source values. Treat results as overlapping keyword candidates; financial operations require separate provider, owner, legal, security, and exact-SHA evidence.
- Remote completion requires independently verified target-owned terminal workflow evidence bound to the exact repository/ref/SHA, plus remote tree and required artifact/check evidence. Dispatch acceptance, local tests, a clean worktree, or a locally generated report alone never passes this gate.
- Prefer bounded, resumable, risk-prioritized work and measured parallelism. Do not trade correctness for an elapsed-time target or claim that work spanning months/years is completed in minutes; retain unresolved work as prioritized blockers.
- Reuse target-owned CodeQL run metadata already collected for the exact repository/ref/SHA; do not launch a duplicate analysis for speed. A passing CodeQL run is security evidence, not remote-completion proof, and denied/missing alert access remains unknown rather than zero findings.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10435`; directories: `1269`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2155, build_download_install=2110, orchestration=2061, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2000`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52722`; percentage occurrences: `22237`.
- Markdown word count: `3552546`; heuristic sentence count: `673863`; sentence records indexed: `673863`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29844` metric claims; `10662` completion claims; `29747` metric and `10533` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9046` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13340`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40017` lines in `3670` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `287`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
