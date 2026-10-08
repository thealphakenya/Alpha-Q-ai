# QMOI Background Automation - Quick Reference

## 🚀 Quick Start (30 seconds)

```bash
# 1. Setup environment
bash scripts/qmoi-background-setup.sh

# 2. Start app
npm run dev

# 3. Visit dashboard
# http://localhost:3000/master
```

## 🔑 Key Concepts

| Concept            | What It Does                           |
| ------------------ | -------------------------------------- |
| **Auto-Scan**      | Periodically detects errors (7+ types) |
| **Health Monitor** | Continuously checks CPU/Memory/Disk    |
| **Auto-Fix**       | Automatically fixes detected errors    |
| **Alerts**         | Notifies of threshold breaches         |
| **Recovery**       | Auto-fixes critical health issues      |

## 📋 Configuration

### Via Environment

```bash
# Timing (in milliseconds)
QMOI_AUTO_SCAN_INTERVAL=300000           # 5 min (default)
QMOI_HEALTH_MONITOR_INTERVAL=30000       # 30 sec (default)

# Thresholds (0-100%)
QMOI_CPU_WARNING=70
QMOI_CPU_CRITICAL=90
QMOI_MEMORY_WARNING=75
QMOI_MEMORY_CRITICAL=95
QMOI_DISK_WARNING=80
QMOI_DISK_CRITICAL=95

# Flags
QMOI_AUTO_FIX_ON_ERRORS=true
QMOI_AUTO_FIX_ON_HEALTH_ISSUES=true
```

### Via API

```bash
# Get config
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/config

# Update config
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"autoScanInterval": 600000}' \
  http://localhost:3000/api/master/autofix/config

# Reset to defaults
curl -X DELETE -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/config
```

## 🎛️ Control Commands

```bash
# Get status
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/background-automation

# Start automation
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "start"}' \
  http://localhost:3000/api/master/autofix/background-automation

# Stop automation
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "stop"}' \
  http://localhost:3000/api/master/autofix/background-automation

# Restart automation
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"action": "restart"}' \
  http://localhost:3000/api/master/autofix/background-automation
```

## 📊 Status Endpoints

```bash
# Auto-scan status
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/autoscan

# Health monitor status
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/healthmonitor

# Bootstrap logs
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/bootstrap
```

## 📁 Log Files

```
.logs/
├── qmoi-bootstrap.log          # App startup logs
├── qmoi-autoscan.log           # Error scanning logs
└── qmoi-health-monitor.log     # Health checking logs
```

**View logs:**

```bash
tail -f .logs/qmoi-autoscan.log
tail -f .logs/qmoi-health-monitor.log
tail -50 .logs/qmoi-bootstrap.log
```

## 🔐 Authentication

All APIs require Bearer token:

```bash
Authorization: Bearer YOUR_ADMIN_TOKEN
```

Set `ADMIN_TOKEN` in `.env.local`:

```bash
ADMIN_TOKEN=your-secure-token-here
```

## 💡 Common Tasks

### Check if automation is running

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/background-automation | jq '.status'
```

### Get latest statistics

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/autoscan | jq '.statistics'
```

### View last 20 logs

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/autoscan | jq '.logs[-20:]'
```

### Increase scan interval (10 minutes)

```bash
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"autoScanInterval": 600000}' \
  http://localhost:3000/api/master/autofix/config
```

### Adjust CPU threshold (80%)

```bash
curl -X POST -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cpuThresholdWarning": 80}' \
  http://localhost:3000/api/master/autofix/config
```

### View recent alerts

```bash
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:3000/api/master/autofix/healthmonitor | jq '.alerts[-10:]'
```

## 🆘 Quick Troubleshooting

| Problem               | Solution                                         |
| --------------------- | ------------------------------------------------ |
| Services not starting | Check `.logs/qmoi-bootstrap.log`                 |
| No errors detected    | Run manual scan, check `.logs/qmoi-autoscan.log` |
| High CPU usage        | Increase `QMOI_AUTO_SCAN_INTERVAL`               |
| No health alerts      | Verify thresholds aren't too high                |
| API returns 403       | Check `ADMIN_TOKEN` is correct                   |

## ⚙️ Performance Tuning

### For Production (Less Frequent)

```bash
QMOI_AUTO_SCAN_INTERVAL=600000         # 10 min
QMOI_HEALTH_MONITOR_INTERVAL=60000     # 1 min
```

### For Development (More Frequent)

```bash
QMOI_AUTO_SCAN_INTERVAL=60000          # 1 min
QMOI_HEALTH_MONITOR_INTERVAL=10000     # 10 sec
```

## 🔍 Default Thresholds

| Metric | Warning | Critical |
| ------ | ------- | -------- |
| CPU    | 70%     | 90%      |
| Memory | 75%     | 95%      |
| Disk   | 80%     | 95%      |

## 📚 File Locations

| Purpose           | Location                                    |
| ----------------- | ------------------------------------------- |
| Configuration     | `lib/qmoi-automation-config.ts`             |
| Bootstrap         | `lib/qmoi-bootstrap.ts`                     |
| Auto-Scan Service | `lib/qmoi-background-autoscan.ts`           |
| Health Monitor    | `lib/qmoi-health-monitor.ts`                |
| Manager           | `lib/qmoi-automation-manager.ts`            |
| Middleware        | `middleware.ts`                             |
| APIs              | `app/api/master/autofix/*/route.ts`          |
| Setup Script      | `scripts/qmoi-background-setup.sh`          |
| Quick Start       | `docs/QMOI_BACKGROUND_AUTOMATION_README.md` |
| Full Guide        | `docs/QMOI_BACKGROUND_AUTOMATION_GUIDE.md`  |
| Summary           | `docs/IMPLEMENTATION_SUMMARY.md`            |

## 🎯 Endpoint Summary

| Method | Endpoint                                   | Purpose                      |
| ------ | ------------------------------------------ | ---------------------------- |
| GET    | `/api/master/autofix/background-automation` | Get status                   |
| POST   | `/api/master/autofix/background-automation` | Control (start/stop/restart) |
| GET    | `/api/master/autofix/autoscan`              | Auto-scan status             |
| GET    | `/api/master/autofix/healthmonitor`         | Health monitor status        |
| GET    | `/api/master/autofix/config`                | Get configuration            |
| POST   | `/api/master/autofix/config`                | Update configuration         |
| PUT    | `/api/master/autofix/config`                | Update configuration         |
| DELETE | `/api/master/autofix/config`                | Reset to defaults            |
| GET    | `/api/master/autofix/bootstrap`             | Get bootstrap logs           |
| DELETE | `/api/master/autofix/bootstrap`             | Clear bootstrap logs         |

## ✅ Verification Checklist

- [ ] Environment variables configured
- [ ] App starts without errors
- [ ] Dashboard shows "Running" status
- [ ] Auto-scan logs in `.logs/qmoi-autoscan.log`
- [ ] Health monitor logs in `.logs/qmoi-health-monitor.log`
- [ ] API endpoints respond (200 status)
- [ ] Statistics updating in real-time
- [ ] No authorization errors (403)

## 🚀 Next Steps

1. Setup: `bash scripts/qmoi-background-setup.sh`
2. Start: `npm run dev`
3. Dashboard: `http://localhost:3000/master`
4. Monitor: Check `.logs/` directory
5. Configure: Adjust intervals and thresholds
6. Deploy: Move to production when ready

---

**Quick Reference v1.0 | QMOI Background Automation System**

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
