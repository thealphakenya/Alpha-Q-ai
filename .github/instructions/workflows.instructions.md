# Workflow instructions

## Default model

Use GitHub Actions for heavy validation, artifact generation, and release workflows. Keep the local Codespace responsible for orchestration, inspection, and lightweight validation.

## Required safeguards

- Validate workflow YAML and triggers before dispatch.
- Check required permissions, reuse, and concurrency.
- Ensure every run is tied to an exact SHA.
- Require terminal workflow conclusions before treating runs as success.
- Record workflow IDs, jobs, and artifact hashes with the evidence ledger.

## Completion rule

A workflow run is not completion. A terminal result plus independently verified remote state is required.

The autonomous agent must bind every queued or dispatched job to the exact repository/ref/SHA, preserve the run ID and result, resume from checkpoints, and stop at authorization or unavailable-evidence blockers without retrying indefinitely.

## GitHub App workflow contract

- For cross-repository reads, prefer `actions/create-github-app-token@v3` with an owner and explicit repository list and only the minimum read permissions. Supported Actions names may include `APP_CLIENT_ID`/`APP_PRIVATE_KEY` or `QMOI_GITHUB_CLIENT_ID`/`QMOI_GITHUB_APP_ID`/`QMOI_GITHUB_PRIVATE_KEY`. Do not use Codespaces secrets in Actions; configure Actions variables/secrets separately and verify their setup via authorized metadata/read-only checks.
- Keep the `github.token` or user-token fallback explicit and mark the selected credential role in value-free evidence. No fallback converts `AUTH_BLOCKED` into success without identity and endpoint verification.
- App-key rotation must be confirmed before token minting if the former key was exposed. Never print, persist, or artifact the private key or generated token; allow short-lived tokens to expire/revoke with the job.
- Copilot Chat should request target-owned workflows or approved integrations, not collect credential values. Every workflow result remains bound to exact repo/ref/SHA and a terminal conclusion.

## QAUDITS workflow automation

- Use QAUDITS for bounded workflow discovery, requirement-to-test mapping, and resumable evidence collection. Record workflow/run/job IDs, exact repository/ref/SHA, permissions/concurrency context, artifacts and hashes, measured status, and explicit skipped/unavailable inputs.
- Validate triggers, permissions, reuse, and concurrency before any authorized dispatch. Bind dispatches to the exact SHA, cap retries, preserve failed results, and never treat dispatch acceptance or a queued run as completion.
- Require terminal conclusions plus independent remote ref/tree and artifact verification. Update paired `oe2.txt`/`remotecompletion.md` and machine evidence with the correlation ID and evidence level; leave remote completion blocked when any required check is missing.
- Keep heavy validation on target-owned workflows where available; local QAUDITS is orchestration and evidence, not a substitute for remote worker results or human authorization.

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
