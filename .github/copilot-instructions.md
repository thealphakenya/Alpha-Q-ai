# Copilot instructions

This repository follows the remote-first completion and evidence model described in `remotecompletion.md`.

## Law of the repository

- Local code changes do not prove remote success.
- Missing remote evidence is a blocker, not a pass.
- Protected branches, required checks, and existing GitHub policy must be respected.
- Do not fabricate progress, SHAs, approvals, releases, deployments, or parity claims.

## Safety rules

- Never expose credentials, tokens, or secrets.
- Never bypass rulesets, branch protections, or user approvals.
- Never force-push or rewrite shared history.
- Never infer remote completion from local commits.
- When a workflow or API returns 401/403/404, record it as diagnostic evidence and continue safely.
- Before planning protected work, inventory and read root `AGENTS.md`, this file, and all files under `.github/instructions`; report relative paths, scopes, hashes, and unreadable files without storing instruction text in telemetry.
- The autonomous agent may refresh generated evidence and run safe local/read-only tasks, but must not rewrite or weaken policy instructions, self-authorize protected actions, or convert a queued action into completion without terminal evidence.

## Required artifacts

Keep these artifacts current and honest:

- `remotecompletion.md`
- `oe2.txt`
- `MERGE.md`
- `RELEASES.md`
- `ALLVALIDATIONS.md`
- `ALLMDFILESREFS.md`
- `remote-completion.json`
- `remote-evidence-ledger.jsonl`

## Evidence policy

Every operation should leave:

- a correlation ID;
- a repository and ref;
- status and result;
- relevant SHA(s);
- verification level; and
- an explicit blocker or next action when remote proof is unavailable.

The Ollama completion engine maintains a resumable, priority-ordered queue for non-passing gates. Retries are bounded and checkpointed. It pauses at explicit authorization or remote-evidence blockers instead of spinning, bypassing policy, or claiming it can replace Copilot Chat or human judgment.

## GitHub App credential handling

- Local App identifiers are stored outside the checkout in `$HOME/.config/alpha-q-ai/github-app/credentials.env` (directory mode `700`, file mode `600`).
- A replacement private key belongs at `$HOME/.config/alpha-q-ai/github-app/private-key.pem` with mode `600`; the previously tracked key is compromised and has been removed locally. Rotate it in GitHub App settings before further App authentication.
- Never print, quote, commit, or paste credential values into chat or logs. Load them only into the process that needs them, use short-lived tokens, and prefer read-only requests unless an explicitly authorized operation requires more.

## QAUDITS and remote-completion workflow

- Run the documented QAUDITS inventory and Markdown-integrity commands before claiming audit coverage. Record repository/ref, local commit/tree, correlation ID, measured duration, artifact hashes, status, counts, omissions, unreadable/skipped inputs, blockers, and next action.
- Treat sentence/word hashes, candidate detection, and structural validation as local integrity signals, not semantic review or proof of implementation. Report scope limits and heuristic status; never fill missing evidence with assumed success.
- Update the paired `oe2.txt` and `remotecompletion.md` checkpoints and machine-readable evidence through the supported checkpoint writer. Keep one correlation ID across the pair, state JSON, and append-only event; explicitly preserve remote verification as false until proven.
- Start long `audit-inventory` runs with a paired `IN_PROGRESS` record and finalize with the same correlation ID so interruption cannot leave stale success-looking evidence.
- Remote completion must be independently verified against the exact repository, ref, and SHA using terminal target-owned workflow evidence and the corresponding remote tree/artifact/check evidence. A workflow dispatch, local scan/test, PR existence, or elapsed-time target is not completion proof.
- Use bounded resumable shards and safe parallel work; stop on authorization, security, unavailable-source, or terminal-evidence blockers rather than retrying indefinitely or implying the agent can replace human judgment.
- The full inventory also refreshes finance-document categories and redacted amount/currency, revenue, payment, wallet/banking, deal, employment/payroll, jurisdiction, project-budget, and financial-security candidates. These counts are neither semantic/coverage proof nor authorization; never store raw amounts, account identifiers, credentials, or source lines.
- Reuse existing target-owned CodeQL run metadata only when bound to the exact repository/ref/SHA; never launch a duplicate scan in the fast QAUDITS path. A CodeQL success cannot satisfy the completion gate, and denied alert access is `UNKNOWN`, not a clean result.

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
