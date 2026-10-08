# Deployment & Provisioning 🍱

This document explains how to build and deploy a production image and how to provision a host to run the app reliably (PM2 + systemd healthcheck timer).

## CI/CD (GitHub Actions)

- We added `.github/workflows/ci-cd.yml` which runs tests, builds the Next.js app and builds a Docker image. The workflow will push the image to GitHub Container Registry (GHCR) when not running in a pull-request.
- To enable the deploy job you must set these repository secrets:
  - `DEPLOY_HOST` — host IP or DNS
  - `DEPLOY_USER` — user to SSH as
  - `DEPLOY_SSH_KEY` — private key for SSH (PEM)

Optionally you can push images using a PAT with `packages:write` permissions for GHCR (GITHUB_TOKEN often suffices when enabled for packages).

## Host Provisioning (manual steps)

We included `scripts/host-provision.sh` to help automate the final host steps.

Common steps to run on the host (requires sudo):

1. Copy service files and enable timer:

   sudo ./scripts/host-provision.sh --install-systemd

2. Enable PM2 startup so the saved process is resumed on boot:

   sudo ./scripts/host-provision.sh --enable-pm2-startup

3. To deploy a new image from GHCR (pull and restart PM2):

   sudo ./scripts/host-provision.sh --deploy-image ghcr.io/<owner>/<repo>:<tag>

Note: The PM2 startup step tries to run the `pm2 startup` command and then `pm2 save`. If your environment requires a different invocation, follow the printed guidance.

## Local verification

- After running the host provisioning steps, verify HTTP health: `curl -fS http://localhost:3000/` and check `pm2 list`.

## Security & Secrets

- Keep the `DEPLOY_SSH_KEY` private and add it to GitHub secrets only for the repository or environment used for deployment.

## Operator checklist (required secrets & host steps)

1. Add repository secrets in GitHub:
   - `DEPLOY_HOST` - host IP/DNS
   - `DEPLOY_USER` - SSH user
   - `DEPLOY_SSH_KEY` - PEM private key text
   - (optional) `DEPLOY_PORT` - SSH port (default 22)
   - (optional) `GHCR_PAT` - personal access token if you prefer PAT for pushing to GHCR

2. On the target host (run as a privileged operator):
   - Ensure Docker and PM2 are installed and available for the deploy user.
   - From the repo root on the host, run:
     - `sudo ./scripts/host-provision.sh --install-systemd`
     - `sudo ./scripts/host-provision.sh --enable-pm2-startup`
   - Confirm the service and timer are active:
     - `systemctl status qmoi-healthcheck.timer`
     - `systemctl status qmoi.service`

3. To deploy a new image (manual alternative):
   - `sudo ./scripts/host-provision.sh --deploy-image ghcr.io/<owner>/<repo>:<tag>`

4. Verify health: `curl -fS http://localhost:3000/` or check `pm2 list`.

Add these notes to your operator runbook and restrict who has access to the `DEPLOY_SSH_KEY` secret.

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
