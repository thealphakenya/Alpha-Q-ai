# QMOI Enhanced System: Automated Environment & Credential Management

## Features
- Automatic creation and updating of `.env` and `.env.example` files
- Auto-population of platform credentials for Vercel, AWS, GCP, Azure, and GitHub
- Easy script execution via `npm run env-setup`
- Extendable for additional platforms and secrets

## Usage
Run the following command to auto-setup all environment variables and credentials:

```bash
npm run env-setup
```

This will ensure all required variables are present in `.env` and `.env.example`.

## Customization
Edit `scripts/qmoi-env-setup.js` to add or modify platform variables as needed.

## Last updated: November 24, 2025
# WORKSPACEGENERAL

- Audit timestamp: 2025-11-11T00:00:00Z
- Total files scanned: 18921
- Files considered done (no original [AUTOFIXED by Ollama at 2026-07-26T18:54:39.577070Z]s): 14596
- Files with [AUTOFIXED by Ollama at 2026-07-26T18:54:39.577070Z]s detected: 0

## Files referenced
- resumetodos.txt
- donerefs.txt
- allrefs.txt
- allrefs.md

## Automation

Workflows and scripts live under `.github/workflows` and `tools/`.

New automation added (auto-managed):
- `tools/check_links_clean.py` — link/DNS checker (generates reports in `tools/`).
- `tools/apply_link_fixes.py` — conservative http->https auto-fixer (dry-run default).
- `tools/auto_fix_build.py` — conservative build autofixer for missing deps (Node/Python).
- Scheduled link-check workflow: `.github/workflows/scheduled-link-check.yml` (daily).
- Vercel autofix workflow: `.github/workflows/vercel-autofix.yml` (runs on push/PR and will attempt safe fixes and open PRs).
 - Scheduled memory-sync workflow: `.github/workflows/sync-memory.yml` (every 15 minutes; requires `QMOI_GH_TOKEN`/`QMOI_GIST_ID` or `QMOI_HF_TOKEN`/`QMOI_HF_REPO` to be configured in repo secrets).

New Vercel helper scripts added (2025-11-24):
- `scripts/vercel_deploy.sh` — deploy the PWA/web app to Vercel using the `vercel` CLI or guidance via the Vercel API when tokens are available.
- `scripts/vercel_monitor_and_fix.sh` — poll the Vercel API for recent deployments, fetch logs, and run `tools/auto_fix_build.py` (if present) to propose safe fixes; writes logs to `logs/`.

Automation policy: automated changes create PRs (or branches) for review. Low-risk fixes (http->https) are applied automatically per policy; dependency fixes are attempted conservatively and offered as PRs.

Keep this file updated when automation changes.
# Recent workspace updates (summary):

- Added a local QM OI dev server: `scripts/qmoi_local_server.py` with OpenAI-style `/v1/chat/completions` and persistent memory in `qmoi_memory.json`.
- Memory sync: `/sync/push`, `/sync/pull`, and `/sync/config` endpoints added to the local server. A standalone sync helper `scripts/sync_memory.py` supports pushing to GitHub Gist, Hugging Face repo, or SCP targets using env vars.
- PWA: `pwa_apps/qmoi-space` updated/verified (manifest + service worker present).
- Documentation: `docs/LOCAL_QMOI_DEVELOPMENT.md`, `CURLQMOIMASTERSISTERUSER.md`, and `HOOKS.md` updated to reference the local server and memory sync.

- Deployment helpers: `deploy/qvillage/run_qmoi.sh` and `deploy/qvillage/qmoi.service` added to keep `qmoi` running in qvillage (systemd example + supervisor loop). See `deploy/README.md` for instructions.
- CI: `.github/workflows/qmoi-sync-memory.yml` added to run `scripts/sync_memory.py` on a schedule (every 15 minutes) and on branch push — requires secrets `QMOI_GH_TOKEN`, `QMOI_HF_TOKEN`, `QMOI_GIST_ID` to be configured.

Next suggested steps:
- Configure `QMOI_GH_TOKEN` and/or `QMOI_HF_TOKEN` in CI or environment secrets to enable automated memory sync.
- Add authentication in front of `/sync/*` endpoints before exposing to any network.
- Run `python3 scripts/sync_memory.py` manually for initial sync, or add a CI job that runs it on a schedule.
# Quick Vercel checklist
- Set `VERCEL_TOKEN` and `VERCEL_PROJECT_ID` as repository-level secrets (or in your deployment environment) to enable automated deploys and monitoring.
- To deploy locally: install `vercel` CLI (`npm i -g vercel`) and run `./scripts/vercel_deploy.sh pwa_apps/qmoi-ai`.
- To monitor and attempt safe fixes: run `VERCEL_TOKEN=... VERCEL_PROJECT_ID=... ./scripts/vercel_monitor_and_fix.sh` and review generated logs/PRs.
# WORKSPACEGENERAL

- Audit timestamp: 2025-11-08T15:29:10.283537Z
- Total files scanned: 18921
- Files considered done (no original [AUTOFIXED by Ollama at 2026-07-26T18:54:39.577070Z]s): 14596
- Files with [AUTOFIXED by Ollama at 2026-07-26T18:54:39.577070Z]s detected: 0

## Files referenced
- resumetodos.txt
- donerefs.txt
- allrefs.txt
- allrefs.md

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
