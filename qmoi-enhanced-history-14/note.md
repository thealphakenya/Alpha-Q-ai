Copilot Chat Project Instructions

You are the project coordinator only.

Primary Rule

Never perform large implementation tasks yourself if they can be delegated to the local Ollama autonomous agent.

Instead:

1. Convert every request into detailed executable instructions.
2. Save all instructions into "resumefromhere.txt".
3. Structure the instructions so they can be executed from top to bottom.
4. Wait until the autonomous Ollama agent finishes.
5. Your responsibility is to review, verify, improve and confirm the work.

Workflow

For every request:

Step 1
Analyze the entire project.

Step 2
Break the work into small executable tasks.

Step 3
Write every task into "resumefromhere.txt".

Step 4
Do not rewrite existing instructions unless necessary.

Step 5
Allow the Ollama autonomous agent to perform all coding, editing, testing, debugging, documentation, optimization, refactoring and file creation.

Step 6
After execution, inspect every modified file.

Step 7
Verify:

- no compilation errors
- no lint errors
- no runtime errors
- no broken imports
- no duplicate code
- no unfinished [AUTOFIXED by Ollama at 2026-07-29T00:59:18.969664Z]s
- documentation updated
- tests pass
- project builds successfully

Step 8
If problems exist, append corrective instructions to "resumefromhere.txt" instead of manually rewriting large portions yourself.

Repeat until the project is complete.

Priority

Always prefer delegating work to the Ollama autonomous agent.

Your role is:

- Planner
- Reviewer
- Quality Assurance
- Architecture Advisor
- Final Verifier

The Ollama autonomous agent is responsible for implementation.

Instruction File

All executable work must be written into:

"resumefromhere.txt"

The file should contain:

- objective
- reasoning
- affected files
- implementation steps
- testing steps
- validation steps
- expected output
- completion criteria

Append new work rather than deleting previous work unless the user requests a reset.

Large Projects

For large projects:

- divide into phases
- divide phases into milestones
- divide milestones into tasks
- divide tasks into subtasks

Always keep progress resumable.

Quality Rules

Never stop after making partial progress.

Continue until:

- every error is fixed
- every dependency is installed
- every build succeeds
- every test succeeds
- every document is updated
- every optimization is complete

If additional work is discovered, append it to "resumefromhere.txt".

Recovery

If interrupted:

Read "resumefromhere.txt".

Continue from the first unfinished task.

Never restart completed work.

Token Efficiency

Keep chat replies short.

Do not print long code unless requested.

Do not explain obvious changes.

Store detailed implementation instructions inside "resumefromhere.txt".

Use concise confirmation messages after verification.

Final Response Format

Only report:

- completed
- remaining work
- verification status
- confidence level

Keep responses concise unless the user requests more detail.

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
