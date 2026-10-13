Mission alignment: follow the canonical mission in [NEWMISSION.md](../../NEWMISSION.md), [MISSIONNEWEST.md](../../MISSIONNEWEST.md), [MISSIONNEW.md](../../MISSIONNEW.md), and [MISSION.md](../../MISSION.md). This instruction set is subordinate to the mission and to the repository's remote-first evidence gate. Any merge, release, deployment, or protected action remains blocked until exact remote proof exists.

# GitHub API instructions

## Required approach

- Verify authenticated identity before any mutation.
- Inspect branch protection and rulesets before merge or dispatch.
- Classify HTTP 400/401/403/404/409/422/429/5xx separately.
- Treat 403 and 404 as ambiguous until verified against auth and repo state.
- Use repository dispatch or target-owned workflow triggers only when explicitly authorized.
- Never claim success from a dispatch acceptance alone.
- The autonomous agent must apply these identity, protection, authorization, and terminal-evidence checks to each remote operation; an access preflight is not mutation authority or parity evidence.
- The Copilot-to-local-bridge-to-Ollama loop is a local execution path, not a GitHub credential path. Keep tokens and private keys out of structured payloads, model context, diffs, and return summaries; request remote work only through authorized least-privilege integrations and report its exact terminal evidence separately.

## Evidence requirements

Record:

- repo owner/name,
- operation and endpoint class,
- ref and SHA,
- response status,
- run or PR identifiers,
- verification method,
- and whether the result was terminal or merely observed.

## GitHub App preflight

- Prefer a target-owned workflow using a short-lived installation token scoped to explicit repositories and minimum permissions. Discover installation context from owner/repository inputs when supported; never fabricate an installation ID.
- Codespaces secrets are not Actions secrets. Do not infer that a value configured in one store is available in the other; validate each path independently.
- Before App API use, require owner-confirmed rotation of any historically exposed key, then verify App identity and installation/repository access with read-only calls. A secret-presence check is not proof of authentication.
- For GitHub App access by Copilot Chat or the Ollama agent, route through an approved tool or target-owned workflow that reads secrets in-process. Never place a private key/token in chat context. Fail closed on 401/403, unknown scopes, or missing endpoint evidence.

## QAUDITS remote-evidence binding

- QAUDITS must bind every remote observation to the canonical owner/repository, requested ref, full commit SHA, endpoint/verification method, response status, and correlation ID; preserve 400/401/403/404/409/422/429/5xx as distinct diagnostics.
- A run or dispatch ID is not terminal success. Require a terminal successful conclusion on the exact SHA, then independently verify the remote ref/tree and required artifact/check state before marking any gate passed.
- Refresh `oe2.txt`, `remotecompletion.md`, `remote-completion.json`, and `remote-evidence-ledger.jsonl` through the supported checkpoint path. Record whether evidence is observed, terminal, or independently verified; leave remote verification false when any binding or authority gate is absent.
- QAUDITS can queue and prioritize authorized work but cannot self-authorize a mutation, infer identity from secret presence, bypass branch protection, or convert local completion into remote completion.
- CodeQL workflow and code-scanning observations must be bound to the canonical repository, exact ref/full SHA, run/check ID, and terminal status. Reuse an existing workflow-run response where possible; an HTTP 403/404 alert response, absent run, stale SHA, or in-progress job is `UNKNOWN`/incomplete, never zero findings or success.

## Two-hour mission monitoring

- Track mission sections `M01`–`M16` with actual UTC phase/task times, status, retries, evidence, blockers, and next actions. Correlate the paired Markdown checkpoint, machine state, and append-only event through the supported writer.
- Keep the mission deadline separate from remote verification. Record identity, exact ref/SHA, endpoint response, and terminal evidence as observed; missing authentication or remote evidence remains blocked and must not be inferred from local elapsed-time metrics.
- Use the mission-ledger updater for local task/phase timing and retain its correlated remote-verification=false result until authenticated exact-SHA evidence is independently available.
- Preserve unfinished work at the deadline. A scheduled trigger or dispatch is not proof that continuation executed or resumed.

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

## Mission roadmap

- Follow the canonical [root mission](../../MISSION.md) and its instruction-directory mirror for requirement mapping and evidence status. This file's identity, authorization, exact-SHA, and terminal-verification rules remain controlling.
