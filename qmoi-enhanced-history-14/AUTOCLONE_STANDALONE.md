## CI/CD Workflow Status

![Docker Build & Push](https://github.com/thealphakenya/qmoi-enhanced/actions/workflows/docker-build-push.yml/badge.svg)

## Troubleshooting & Validation

1. Check the health endpoint:

```bash
curl http://localhost:8080/health
# Should return: OK
```

2. Check GitHub Actions workflow status:

- Go to the Actions tab in your GitHub repo and confirm all jobs are green.

3. If the container fails to start, check logs:

```bash
docker logs <container_id>
```

4. For QCity auto-update, confirm systemd timer and service are enabled and running:

```bash
systemctl status qvillage-update.timer
systemctl status qvillage-update.service
```

## Health Check Endpoint

The standalone runner exposes a health check endpoint at `http://localhost:8080/health` (configurable via `HEALTH_PORT` env var).

Example:

```bash
curl http://localhost:8080/health
# Returns: OK
```

## Usage: Docker

```bash
docker build -f Dockerfile.qvillage -t qvillage-standalone:latest .
docker run -d --restart=always -e HF_API_TOKEN=... -e SLACK_WEBHOOK_URL=... -e HEALTH_PORT=8080 qvillage-standalone:latest
```

## Usage: Docker

```bash
docker build -f Dockerfile.qvillage -t qvillage-standalone:latest .
docker run -d --restart=always -e HF_API_TOKEN=... -e SLACK_WEBHOOK_URL=... -e HEALTH_PORT=8080 qvillage-standalone:latest
```

# Autoclone & Standalone Mode — QMOI / QVillage

This short guide explains the autoclone + standalone runner mode so QMOI/QVillage can run independently of any external hosting platform.

Files added to repo (ready-to-use):

- `tools/autoclone_and_run.sh` — entrypoint that clones/updates the repository into `REPO_DIR` (default: `/opt/qvillage`), installs optional requirements, then launches the standalone runner.
- `tools/standalone_runner.py` — attempts to import `QVillageSyncEngine` from `tools/qvillage_memory_sync.py` and run its `run_full_sync()` loop; falls back to executing the script as a subprocess.
- `Dockerfile.qvillage` — container image optimized to run the autoclone entrypoint and runner.

Principles:

- Platform-agnostic: works with Docker, systemd, Kubernetes, or bare metal.
- Safe defaults: `RUN_INTERVAL_SECONDS=3600` (hourly), set `RUN_INTERVAL_SECONDS=0` to run once and exit.
- Configurable: pass `REPO_URL`, `REPO_BRANCH`, `REPO_DIR`, `HF_API_TOKEN`, and other env vars at runtime.
- Skips: set `SKIP_AUTOCLONE=1` to avoid cloning (useful when mounting your repo into container), `SKIP_DEP_INSTALL=1` to skip pip installs at startup.

Quick Docker run (now):

```bash
# Build the image
docker build -f Dockerfile.qvillage -t qvillage-standalone:latest .

# Run container (auto-clones the repo into /opt/qvillage inside the container)
docker run -d --restart=always \
  -e REPO_URL=https://github.com/thealphakenya/qmoi-enhanced.git \
  -e REPO_BRANCH=main \
  -e REPO_DIR=/opt/qvillage \
  -e RUN_INTERVAL_SECONDS=3600 \
  -e HF_API_TOKEN=$HF_API_TOKEN \
  -e SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL \
  qvillage-standalone:latest
```

One-shot run (no loop):

```bash
docker run --rm \
  -e RUN_INTERVAL_SECONDS=0 \
  -e SKIP_DEP_INSTALL=1 \
  qvillage-standalone:latest
```

systemd example (if you don't use Docker):

```ini
[Unit]
Description=QVillage Autoclone + Sync
After=network-online.target

[Service]
Type=simple
User=qvillage
ExecStart=/usr/bin/env bash /opt/qvillage/tools/autoclone_and_run.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Notes & recommended env vars:

- `REPO_URL` — URL of this repository (default: `https://github.com/thealphakenya/qmoi-enhanced.git`)
- `REPO_BRANCH` — branch to clone (default: `main`)
- `REPO_DIR` — destination directory (default: `/opt/qvillage`)
- `RUN_INTERVAL_SECONDS` — loop interval; `0` runs once and exits; default is `3600` (1 hour)
- `HF_API_TOKEN` — hugging face token used by the sync engine (optional if running with local fallbacks)
- `SLACK_WEBHOOK_URL` — optional for notifications

Security:

- Keep secrets out of the image — pass them at runtime as environment variables or use your cloud provider's secret manager.
- If you mount the repo into `REPO_DIR`, set `SKIP_AUTOCLONE=1` to avoid accidental overwrites.

Support:

If you see errors during autoclone or execution, check container logs (`docker logs <container>`), then inspect `/opt/qvillage/tools/` for the cloned source and run `python tools/standalone_runner.py --dry-run` locally to reproduce errors.

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
