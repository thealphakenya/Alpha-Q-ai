---
title: "QMOI Monitoring & Analytics Guide"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI Monitoring & Analytics Guide

## Dashboard

- **URL:** http://localhost:4000/
- **Login:** Username/password or Google OAuth
- **Features:**
  - View error/fix analytics (auto + manual)
  - Progress bar for percent fixed
  - List of manual errors with instructions
  - Table of recent error/fix runs
  - Trigger auto-fix manually
  - Send test notifications
  - See live GitHub Actions status
  - API endpoints for logs and analytics

## Endpoints

- `/` - Main dashboard
- `/api/error-fix-log` - Error/fix log (JSON)
- `/api/logs` - Orchestrator logs
- `/api/trigger-fix` - Trigger a fix run
- `/health` - Health check

## GitHub Actions Integration

- Progress bar and manual error reporting in workflow summary
- Auto-triggers local fix if remote workflow fails

## Manual Error Handling

- Manual errors are detected and logged with instructions
- View and address manual errors in dashboard and GitHub Actions
- Progress reflects both auto and manual fixes

## Troubleshooting

- If manual errors persist, follow instructions in dashboard or logs
- Use `/api/trigger-fix` to retry fixes
- Check orchestrator logs for details

## Usage

- Start dashboard: `node scripts/qmoi_dashboard.js` or with PM2
- Start orchestrator: `node scripts/qmoi_media_orchestrator.js` or with PM2

---

## Hugging Face Automation Monitoring

- **Deployment & Model Sync:**
  - All Hugging Face Space deployments and model syncs are logged and visible in GitLab CI/CD.
- **UI Feature Test:**
  - Automated UI tests run after each deployment, with results logged and uploaded as artifacts.
- **Log Access:**
  - Review `logs/hf_model_sync.log`, `logs/huggingface_spaces.log`, and `logs/test_hf_space_ui.log` in the GitLab CI/CD artifacts.
- **Health & Status:**
  - QMOI health and status are always visible in the Hugging Face Space dashboard and model card.

---

## Always Fix All Automation Monitoring

- All runs of `npm run qmoi:always-fix-all` are logged to `logs/qmoi-always-fix-all-attempts.json`
- Success and failure notifications are sent via the QMOI notification system
- Persistent failures are highlighted in the dashboard and require manual intervention
- See [QMOIAUTOFIXREADME.md](QMOIAUTOFIXREADME.md) for details

---

## AI Error Prediction & Notification Monitoring

- Error predictions are available at `/api/predictions` (port 4100)
- Notification preferences and history are available at `/api/notification-prefs` and `/api/notification-history` (port 4200)
- Dashboard displays predictions, notification preferences, and history

---

For a full list of documentation, see [REFERENCES.md](REFERENCES.md)

For questions or issues, contact the QMOI master team.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/MONITORING.md",
"validated_at": "2025-10-26T20:51:24.643093Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI Monitoring & Analytics Guide"
},
{
"name": "links",
"ok": true,
"detail": [
{
"label": "QMOIAUTOFIXREADME.md",
"target": "./QMOIAUTOFIXREADME.md",
"ok": true
},
{
"label": "REFERENCES.md",
"target": "./REFERENCES.md",
"ok": true
}
]
}
],
"passed": true,
"summary": {
"total_checks": 2,
"passed": true
}
}

<!-- QMOI_VALIDATION_END -->

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
