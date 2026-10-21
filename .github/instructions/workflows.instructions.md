---
description: "Use when editing, validating, dispatching, or interpreting GitHub Actions workflows. Covers permissions, concurrency, exact-SHA binding, terminal results, and completion evidence."
---

Mission alignment: follow the canonical [latest mission](../../latest%20mission.md), synchronized byte-for-byte to [MISSION.md](../../MISSION.md) and its instruction-directory mirror. Mission phases are `PH01`-`PH18`; legacy requirement task buckets `M01`-`M16` remain distinct. This instruction set is subordinate to the mission and to the repository's remote-first evidence gate. Any merge, release, deployment, or protected action remains blocked until exact remote proof exists.

# Workflow instructions

For the shared mission checkpoint and PH01-PH18 metrics lifecycle, follow [Mission metrics and monitoring](mission-metrics.instructions.md); scheduled workflows are not proof of a running continuation.

## Default model

Use GitHub Actions for heavy validation, artifact generation, and release workflows. Keep the local Codespace responsible for orchestration, inspection, and lightweight validation.

## Required safeguards

- Validate workflow YAML and triggers before dispatch.
- Check required permissions, reuse, and concurrency.
- Ensure every run is tied to an exact SHA.
- Require terminal workflow conclusions before treating runs as success.
- Record workflow IDs, jobs, and artifact hashes with the evidence ledger.

- For M01, do not use workflow dispatch as a substitute for owner/admin-authorized branch-policy evidence. Any workflow that can write a protected ref, publish, or mutate either target requires separately verified M01 evidence for the exact repository/ref/SHA and explicit operation authority; missing or HTTP 403/404 evidence remains blocked.

## Completion rule

A workflow run is not completion. A terminal result plus independently verified remote state is required.

The autonomous agent must bind every queued or dispatched job to the exact repository/ref/SHA, preserve the run ID and result, resume from checkpoints, and stop at authorization or unavailable-evidence blockers without retrying indefinitely.

The conceptual Copilot -> local bridge -> Ollama loop may perform bounded local work, but it must remain distinct from a hosted workflow. Return the local diff and validation evidence to the requester; only the actual target-owned workflow's terminal result and independent exact-SHA verification count as remote evidence. Keep credentials within approved workflow/runtime boundaries.

## GitHub App workflow contract

- For cross-repository reads, prefer `actions/create-github-app-token@v3` with an owner and explicit repository list and only the minimum read permissions. Supported Actions names may include `APP_CLIENT_ID`/`APP_PRIVATE_KEY` or `QMOI_GITHUB_CLIENT_ID`/`QMOI_GITHUB_APP_ID`/`QMOI_GITHUB_PRIVATE_KEY`. Do not use Codespaces secrets in Actions; configure Actions variables/secrets separately and verify their setup via authorized metadata/read-only checks.
- Keep the `github.token` or user-token fallback explicit and mark the selected credential role in value-free evidence. No fallback converts `AUTH_BLOCKED` into success without identity and endpoint verification.
- App-key rotation must be confirmed before token minting if the former key was exposed. Never print, persist, or artifact the private key or generated token; allow short-lived tokens to expire/revoke with the job.
- Copilot Chat should request target-owned workflows or approved integrations, not collect credential values. Every workflow result remains bound to exact repo/ref/SHA and a terminal conclusion.
- For App preflight, secret presence must not select App auth by itself. Require the target repository's owner-managed `QMOI_APP_KEY_ROTATION_CONFIRMED=true` Actions variable after rotation; mint a short-lived installation token only when that gate and required credential references are present. Do not use PAT/`GITHUB_TOKEN` fallback for an App-authenticated preflight result, and report missing or denied conditions as `APP_AUTH_BLOCKED`.
- Report Codespace variable presence as local process evidence only; it does not confirm Actions configuration or permit a workflow to bypass the per-repository rotation gate.

## QAUDITS workflow automation

- Use QAUDITS for bounded workflow discovery, requirement-to-test mapping, and resumable evidence collection. Record workflow/run/job IDs, exact repository/ref/SHA, permissions/concurrency context, artifacts and hashes, measured status, and explicit skipped/unavailable inputs.
- Validate triggers, permissions, reuse, and concurrency before any authorized dispatch. Bind dispatches to the exact SHA, cap retries, preserve failed results, and never treat dispatch acceptance or a queued run as completion.
- Require terminal conclusions plus independent remote ref/tree and artifact verification. Update paired `oe2.txt`/`remotecompletion.md` and machine evidence with the correlation ID and evidence level; leave remote completion blocked when any required check is missing.
- Keep heavy validation on target-owned workflows where available; local QAUDITS is orchestration and evidence, not a substitute for remote worker results or human authorization.
- Prefer the repository's existing CodeQL default setup. QAUDITS may summarize CodeQL workflow-run metadata from the workflow-run response it already fetched, but must bind it to the exact remote SHA/ref, label missing or stale runs `NOT_OBSERVED`, and must not launch a duplicate scan or extra API request as part of the fast completion path. Record run ID and per-language job terminal state; in-progress jobs and unavailable alert APIs stay incomplete/unknown. CodeQL metadata alone neither proves clean findings nor satisfies the remote-completion gate; required checks, security findings, authorization, and independent remote verification remain authoritative.

## Two-hour mission monitoring

- On every mission continuation, refresh the complete PH01-PH18 dashboard and all feature metrics supported by current evidence in both `oe2.txt` and `remotecompletion.md` through the supported checkpoint writer; record unavailable metrics as `NOT_MEASURED` and correlate machine evidence. Refreshing metrics is not a phase transition, workflow result, authorization, or remote proof, and must not restart an expired clock.
- Track phases `PH01`-`PH18` and task durations with real UTC events and one correlation ID across the paired documents and machine evidence; preserve `M01`-`M16` as requirement-task IDs.
- Invoke the mission-ledger updater only from the verified target checkout; its checkpoint is local evidence unless a later authorized hosted run records terminal exact-SHA results.
- Distinguish a configured schedule, accepted dispatch, running workflow, terminal conclusion, and independently verified remote state. The two-hour target does not replace any workflow or SHA gate.
- A queued, running, skipped, or failed workflow remains non-terminal/incomplete as appropriate. Continue independent safe local/read-only work, retain a concrete next action for the blocked workflow, and never launch a duplicate dispatch to make progress appear continuous.
- Leave unfinished actions durable at the deadline. Mark continuation verified only after a distinct run demonstrably restores the checkpoint and executes the next eligible task.

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

- Follow the canonical [root mission](../../MISSION.md) and its instruction-directory mirror for workflow task mapping, bounded retries, and evidence collection. This file's exact-SHA, authorization, terminal-result, and independent-verification gates remain controlling.
