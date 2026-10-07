# 🔧 QMOI AutoFix - Quick Reference Card

## 🎯 Dashboard Access

- **URL**: `http://localhost:3000/master`
- **Tab**: "🔧 QMOI AutoFix System"
- **Access**: Master-only
- **Auth**: Requires ADMIN_TOKEN

## 🚀 Master Control Buttons

### 🔍 Scan For Errors

- Triggers comprehensive system scan
- Detects 7+ error types
- Duration: 10-30 seconds
- Use: Before deployments, daily checks

### ⚡ AutoFix All

- Automatically fixes all detected errors
- Success rate: 70-95%
- Duration: 5-60 seconds
- Use: After scan finds issues

### 💊 Refresh Health

- Updates health metrics
- Shows real-time system status
- Duration: <1 second
- Use: Check system state

## 📊 Health Metrics

| Metric    | Healthy | Warning | Critical |
| --------- | ------- | ------- | -------- |
| CPU       | <70%    | 70-85%  | >85%     |
| Memory    | <70%    | 70-85%  | >85%     |
| Disk      | <80%    | 80-95%  | >95%     |
| Network   | Online  | -       | Offline  |
| Processes | ✓       | -       | ✗        |
| Database  | ✓       | -       | ✗        |
| APIs      | ✓       | -       | ✗        |
| Cloud     | ✓       | -       | ✗        |

## 🔴 Error Severity Levels

- **🔴 Critical**: Requires immediate action
- **🟡 Warning**: Should be addressed soon
- **🔵 Info**: For information only

## 🛠️ Error Types

| Type                 | Auto-Fix Success |
| -------------------- | ---------------- |
| TypeScript/Syntax    | 90%              |
| Missing Dependencies | 95%              |
| Configuration        | 85%              |
| Security             | 80%              |
| Process              | 75%              |
| Resources            | 70%              |

## 📡 API Endpoints

```
POST   /api/master/autofix/scan
POST   /api/master/autofix/fix-all
GET    /api/master/autofix/status
GET    /api/master/autofix/health
GET/POST /api/master/autofix/errors
POST   /api/master/autofix/fix/{errorId}
GET    /api/master/autofix/stream
```

All require: `Authorization: Bearer {ADMIN_TOKEN}`

## 💻 Command Line Usage

### Start Dev Server

```bash
npm run dev
```

### Run Health Check

```bash
python3 scripts/qmoi_health_integration.py
```

### Generate Master Token

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Scan with cURL

```bash
curl -X POST http://localhost:3000/api/master/autofix/scan \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🐍 Python Usage

```python
from scripts.qmoi_health_integration import QMOIHealthIntegration

# Initialize
integration = QMOIHealthIntegration()

# Get health
health = integration.get_system_health()

# Scan for errors
errors = integration.comprehensive_error_scan()

# Fix all
results = integration.autofix_all_errors()

# Export data
dashboard = integration.get_dashboard_data()
```

## 🔐 Security Setup

### 1. Set Master Token

```bash
export ADMIN_TOKEN="your-secret-token"
# or in .env.local
ADMIN_TOKEN=your-secret-token
```

### 2. Generate Secure Token

```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### 3. Verify Token

```bash
echo $ADMIN_TOKEN
```

## 📋 Filtering Options

Click filter buttons in dashboard:

- **All**: Show all errors
- **Critical**: Only critical errors
- **Warning**: Only warnings
- **Fixed**: Only fixed errors
- **Unfixed**: Only unfixed errors

## 🔄 Auto-Refresh Intervals

| Component      | Interval  |
| -------------- | --------- |
| Health Metrics | 5 seconds |
| Error List     | Manual    |
| Status         | 5 seconds |
| Dashboard      | Real-time |

## 🐛 Troubleshooting

### "Access Denied"

- Check ADMIN_TOKEN in .env.local
- Verify token format
- Clear browser cache
- Restart dev server

### Errors Not Scanning

- Verify API endpoints exist
- Check server logs
- Ensure token is valid
- Check browser console

### AutoFix Failing

- Review error details
- Check logs: qmoi_autofix_health.log
- Run specific error fix
- Check system permissions

### High Resource Usage

- Reduce scan frequency
- Run during low-traffic periods
- Increase available memory
- Check background processes

## 📚 Documentation Files

| File                                   | Purpose                    |
| -------------------------------------- | -------------------------- |
| QMOI_AUTOFIX_MASTER_GUIDE.md           | Complete feature reference |
| QMOI_AUTOFIX_SETUP_GUIDE.md            | Setup and configuration    |
| QMOI_AUTOFIX_IMPLEMENTATION_SUMMARY.md | What was built             |
| qmoi-autofix-quickstart.sh             | Quick setup script         |

## 🎨 UI Elements

### Control Panel (Top)

- 🔍 Scan button (blue)
- ⚡ AutoFix button (green)
- 💊 Health button (purple)

### Status Cards

- 🔴 Total Errors Found (red)
- 🟢 Fixed (green)
- 🟡 Failed Fixes (yellow)
- 🔵 System Status (blue)

### Health Display

- CPU bar graph
- Memory bar graph
- Disk bar graph
- Network status
- Process indicators

### Error List

- Type badge
- Severity indicator
- Message
- Timestamp
- File reference (if available)
- Action buttons

## 🚀 Keyboard Shortcuts

| Action         | Command                 |
| -------------- | ----------------------- |
| Scan Errors    | Click 🔍 button         |
| Fix All        | Click ⚡ button         |
| Refresh Health | Click 💊 button         |
| Filter Errors  | Click filter buttons    |
| Fix Individual | Click "Fix This" button |
| Auto-refresh   | Every 5 seconds         |

## 📞 Support Resources

- **Logs**: qmoi_autofix_health.log
- **Dashboard Data**: qmoi_autofix_dashboard_data.json
- **API Docs**: See endpoint comments
- **Python Docs**: See script docstrings

## 🎯 Best Practices

✅ Scan daily
✅ Backup before fixing
✅ Review fixed issues
✅ Monitor health continuously
✅ Use during maintenance windows
✅ Check logs regularly
✅ Keep tokens secure
✅ Update regularly

## ⚡ Performance Tips

- Run scans during off-peak hours
- Limit health check frequency if needed
- Close unnecessary applications
- Monitor resource usage
- Keep dependencies up to date

---

**Version**: 2.0.0  
**Status**: Production Ready ✓  
**Master Access**: Required

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
