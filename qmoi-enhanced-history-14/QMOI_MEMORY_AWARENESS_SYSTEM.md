# QMOI_MEMORY_AWARENESS_SYSTEM.md

This document describes the memory-aware operational architecture of the QMOI agent and its credential-aware autonomous behavior.

## Purpose
- Track the repository’s active memory layers, credential stores, and automation awareness.
- Document how the Ollama autonomous agent discovers finance integrations, updates credential manifests, and preserves resume state.
- Serve as a canonical reference for secure account automation and master authorization gating.

## Autonomous execution surface
- Primary entrypoint: `python scripts/ollama_autonomous_agent.py`.
- GitHub workflow triggers: `.github/workflows/ollama-autonomous-agent.yml` and `.github/workflows/ollamatrigger.yml`.
- Default runtime behavior: `AUTO_CONTINUE=1`, `AUTO_PUSH=1`, `TARGET_BRANCH=autosync`.

## Credential and account automation
- The agent discovers finance and payment provider integrations by environment variable names and repository references only.
- It generates and maintains `FINANCE_CREDENTIALS.md` as the secure provisioning manifest for account automation.
- Live provisioning actions are gated by master authorization and are not executed without explicit approval.
- Secret values are never persisted by the agent; only env var names, sources, and secure guidance are recorded.

## Verification and persistence
- Persistent runtime state is stored in `.ollama_agent_state.json`.
- Execution progress and pending work are tracked in `resumefromhere.txt`.
- Live activity summaries are recorded in `OLLAMA_ACTIVITY_FEED.md`.
- The agent verifies required artifacts and documentation manifests before finalizing each run.

## Notes
- This document is part of the repository’s self-awareness inventory and is included in the agent’s documentation manifests.
- Keep this file synchronized with `ALLMDFILES.md`, `ALLLINKS.md`, `DOCS.md`, and `FINANCE_CREDENTIALS.md`.

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
