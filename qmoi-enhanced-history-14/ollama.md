# ollama.md

This document describes the Ollama autonomous agent capabilities, production expectations, and current orchestration behavior.

## Purpose
- Document the autonomous Ollama agent's feature set and the exact repository automation it performs.
- Record how the agent resumes work, merges archives, updates docs, and validates the repository.
- Serve as both a user-facing agent spec and a machine-generated verification artifact.

## Core capabilities
- Resume execution from the last run using .ollama_agent_state.json and processed item history.
- Detect changes to resumefromhere.txt and refresh the execution plan automatically.
- Maintain resumefromhere.txt as the authoritative source of truth for pending work, progress, and journey map tracks.
- Scan archive/backup directories for missing or unmerged files and merge them into the working tree.
- Scan download/app/build/release documentation for referenced .py scripts and ensure those scripts are present, updated, or noted.
- Generate and synchronize manifest files for APIs, endpoints, routes, merge operations, documentation inventory, production readiness, and error tracking.
- Create or refresh tests for discovered Python modules and update ALLTESTSAUOTOTESTS.md accordingly.
- Create or refresh hooks/webhooks documentation and record workflow token gaps in ALLHOOKSWEBHOOKS.md.
- Normalize local development ports to production port equivalents in repository files.
- Start a local helper server and optional production helper server for verification endpoints.
- Run safe repository verification with pytest and Python compile checks when requested.
- Persist audit logs, live notifications, and completion reports for every autonomous run.

## Execution behavior
- On each run, the agent loads state, checks resumefromhere.txt, merges archives, gathers pending work, and updates the plan.
- It writes JOURNEY MAP TRACKS at the top of resumefromhere.txt with counters for pending_before, pending_after, merged_archives, and verification status.
- It updates resumefromhere.txt with progress counts, a progress ledger, repository inventory, and explicit agent instructions.
- If AUTO_CONTINUE=1 is enabled, the agent loops until no pending items remain or iteration limits are reached.
- If RUN_FULL_TESTS=1 is set, the agent starts a production helper server and performs verification even if pending work remains.
- It avoids infinite loops by tracking processed items and stopping when no new progress is made.

## Required artifacts
- API.md, ENDPOINTS.md, ROUTES.md, MERGE.md, DOCS.md, production.md, productionenhanced.md, ALLERRORS.md, ALLBACKEND.md, ALLFRONTEND.md, ALLUI.md, ALLPORTS.md, UNIVERSALS.md, STYLES.md, resumefromhere.txt, OLLAMA_ACTIVITY_FEED.md.
- These artifacts are verified as present and non-empty on each run.

## Reporting
- OLLAMA_ACTIVITY_FEED.md is updated with the latest status and branch metadata.
- OLLAMA_PENDING_REPORT.md and OLLAMA_COMPLETION_REPORT.md are generated for pending work and completion summaries.
- The agent writes .ollama_agent_audit.jsonl and .ollama_agent_state.json for runtime traceability.

## Change control
- The agent creates backups for files it modifies when feasible, using .ollama.bak and audit markers.
- It refrains from destructive replacements and preserves audit trails for every automated change.

## Notes
- This file is regenerated automatically by the agent on each run.
- Treat this document as the current capabilities contract for the Ollama autonomous agent.

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
