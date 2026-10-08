---
title: "QMOI Start Guide"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI Start Guide

## 🚀 How to Start or Resume QMOI (QCity & Cloud)

To ensure QMOI is always running (even in the cloud or when your device is offline), use the following command:

```bash
python scripts/qmoi-start.py
```

- This script will:
  - Check if QMOI is already running (locally or in the cloud)
  - Show the status of the running system
  - If not running, it will start/resume all QMOI automation, error fixing, and cloud features (QCity, Colab, Dagshub, etc.)
  - Ensure all features are always-on and self-healing

## 📊 Status

- The script will display the current status and health of QMOI, including error fixing, cloud sync, and notifications.

## 🧪 Developer Quick Start

- Run dev server: `npm run dev` (local: http://localhost:3000)
- Check dev server health: `npm run dev:health` (returns non-zero exit code if unreachable)
- Run tests: `npx jest --config=jest.config.cjs -i --runInBand --colors --verbose`
- Build (CI style): `npm run ci:build`

Local QM OI helper server (for quick persona and memory tests):

- Start the local helper server (Python):

  ```bash
  python3 scripts/qmoi_local_server.py
  ```

- Example: send a chat in "master" persona (curl):

  ```bash
  curl -sS -X POST http://127.0.0.1:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"messages":[{"role":"system","content":"master"},{"role":"user","content":"How are you doing today?"}]}'
  ```

  Expected snippet of reply:

  ```text
  [Master Mode] At your command. You said: How are you doing today?
  I will respond according to master-level persona with direct, authoritative guidance.
  ```

- Inspect memory saved by helper server:

  ```bash
  curl -sS http://127.0.0.1:8080/memory | jq .
  ```

- Trigger a sync push (no backends configured by default):

  ```bash
  curl -sS -X POST http://127.0.0.1:8080/sync/push
  # Expected: {"ok": true, "details": ["no_backends_configured"] }
  ```

## 🚀 Production

- Build and start (simple):
  - `npm run ci:build`
  - `NODE_ENV=production npm start`
- Daemonize with systemd (example):
  - Copy the repo to the target host (e.g. `/opt/qmoi`)
  - Run `sudo ./scripts/install-systemd-service.sh /opt/qmoi` (this will create `/etc/systemd/system/qmoi.service`, enable and start it)
- PM2: `npm run start:prod:pm2` (uses `ecosystem.config.js`)
- Docker (multi-stage):
  - `docker build -t qmoi-enhanced:latest .`
  - `docker run -p3000:3000 qmoi-enhanced:latest`
- Docker Compose (production):
  - `docker compose -f deploy/docker-compose.prod.yml up -d`

**CI/CD & Deploy:**

- A GitHub Actions workflow `/.github/workflows/ci-cd.yml` now builds and (when configured) pushes a Docker image to GHCR and can optionally deploy it to a host via SSH.
- To enable automated deploys, set the repository secrets `DEPLOY_HOST`, `DEPLOY_USER`, and `DEPLOY_SSH_KEY`. For GHCR pushes ensure `packages: write` permission (GITHUB_TOKEN or a PAT).
- Use `scripts/host-provision.sh` on the host to copy systemd units, enable PM2 startup, or pull a new image and restart the PM2 process (see `docs/DEPLOY.md`).

### MSW & Testing Notes

- MSW is initialized at test-time via `src/setupTests.ts` and provides a global promise `globalThis.__MSW_READY__` that tests can await.
- If you see unhandled network requests during tests, set `SHOW_MSW_UNHANDLED=1` to see them; use `TEST_VERBOSE=1` for extra handler debug output.

- See `CONTRIBUTING.md` for more developer testing notes and troubleshooting steps (MSW handler shapes, env flags, and common fixes).

## 🛡️ Always-On

- QMOI is designed to keep running in the cloud, so you never miss an event or fix—even if your device is offline.

### 🔒 Model policy

- QMOI now enforces a canonical model name `qmoi` (the QMOI aggregator) across the system; runtime overrides are ignored for safety and determinism.
- The local helper server no longer accepts environment or query-based model overrides and reports its health with `model: "qmoi"`.
- The model backup worker's interval configuration had a path bug that has been fixed to respect `ai.model.backup_interval` with a safe default.
- QMOI now exposes an aggregator that combines local and (optionally) cloud model outputs into a single response; a backup is performed after aggregation events to persist metrics and state.

---

**QMOI: Always-on, self-healing, and fully automated.**

<!-- QMOI_VALIDATION_START -->

{
"file": "START.md",
"validated_at": "2025-10-26T20:51:22.641823Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI Start Guide"
},
{
"name": "links",
"ok": true,
"detail": []
}
],
"passed": true,
"summary": {
"total_checks": 2,
"passed": true
}
}

<!-- QMOI_VALIDATION_END -->


---

## Merged source: qmoi-enhanced-history-14/_archive_qmoi-enhanced/START.md

---
title: "QMOI Start Guide"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI Start Guide

## 🚀 How to Start or Resume QMOI (QCity & Cloud)

To ensure QMOI is always running (even in the cloud or when your device is offline), use the following command:

```bash
python scripts/qmoi-start.py
```

- This script will:
  - Check if QMOI is already running (locally or in the cloud)
  - Show the status of the running system
  - If not running, it will start/resume all QMOI automation, error fixing, and cloud features (QCity, Colab, Dagshub, etc.)
  - Ensure all features are always-on and self-healing

## 📊 Status

- The script will display the current status and health of QMOI, including error fixing, cloud sync, and notifications.

## 🛡️ Always-On

- QMOI is designed to keep running in the cloud, so you never miss an event or fix—even if your device is offline.

---

**QMOI: Always-on, self-healing, and fully automated.**

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/START.md",
"validated_at": "2025-10-26T20:51:24.841380Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI Start Guide"
},
{
"name": "links",
"ok": true,
"detail": []
}
],
"passed": true,
"summary": {
"total_checks": 2,
"passed": true
}
}

<!-- QMOI_VALIDATION_END -->

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
