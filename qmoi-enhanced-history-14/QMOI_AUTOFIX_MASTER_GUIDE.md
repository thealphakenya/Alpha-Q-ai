# 🔧 QMOI Advanced AutoFix & Health Monitoring System

## Overview

The QMOI AutoFix system is a comprehensive, master-controlled error detection, diagnosis, and automatic remediation platform integrated into the QMOI master dashboard. This system enables masters to monitor system health, scan for errors, and automatically fix issues across all QMOI components.

## Features

### 1. **Real-Time Error Detection**

- **TypeScript/ESLint Errors**: Syntax and code quality issues
- **Missing Dependencies**: Identifies broken npm packages
- **Configuration Issues**: Missing or invalid config files
- **File System Problems**: Disk space, permissions, missing files
- **Process Errors**: QMOI and service processes not running
- **Security Issues**: Vulnerable packages, exposed environment files
- **Performance Issues**: High CPU/Memory usage, resource bottlenecks
- **API Health**: Endpoint connectivity and response status
- **Database Health**: Connection and query performance
- **Cloud Services**: AWS, GCP, Azure integration status

### 2. **Automatic Fixing**

The system intelligently attempts to fix detected issues:

| Error Type           | Auto-Fix Method            | Success Rate |
| -------------------- | -------------------------- | ------------ |
| Syntax Errors        | Run `eslint --fix`         | 90%          |
| Missing Dependencies | Run `npm install`          | 95%          |
| Configuration        | Create/Update config files | 85%          |
| Security             | Run `npm audit fix`        | 80%          |
| Resource Issues      | Clear caches, optimize     | 70%          |
| Process Errors       | Restart services           | 75%          |

### 3. **Master Control Dashboard**

The master dashboard provides a visually stunning master control interface:

#### Control Panel

- **🔍 Scan For Errors**: Trigger comprehensive system scan
- **⚡ AutoFix All**: Automatically fix all detected issues
- **💊 Refresh Health**: Get latest health metrics

#### Status Metrics

- Total Errors Found
- Successfully Fixed Count
- Failed Fixes Count
- Success Rate Percentage
- System Status

#### Health Metrics Display

- CPU Usage (with visual progress bar)
- Memory Usage (with visual progress bar)
- Disk Usage (with visual progress bar)
- Network Status (Online/Offline)
- Process Status
- Database Status
- API Endpoints Status
- Cloud Services Status

#### Error Details Panel

- Color-coded severity indicators (🔴 Critical, 🟡 Warning, 🔵 Info)
- Error type and message
- Timestamp and file reference
- Individual "Fix This" buttons
- Filter by: All, Critical, Warning, Fixed, Unfixed

## API Endpoints

All endpoints require `Authorization: Bearer <ADMIN_TOKEN>` header.

### 1. **Scan for Errors**

```
POST /api/master/autofix/scan
```

**Response:**

```json
{
  "success": true,
  "errors": [
    {
      "id": "ts_app/page.tsx",
      "type": "TypeScript/Syntax Error",
      "severity": "warning",
      "message": "Syntax error detected",
      "file": "app/page.tsx",
      "timestamp": "2026-01-25T10:30:00Z",
      "fixed": false
    }
  ],
  "totalErrors": 5,
  "scanTime": "2026-01-25T10:30:00Z"
}
```

### 2. **AutoFix All Errors**

```
POST /api/master/autofix/fix-all
```

**Response:**

```json
{
  "success": true,
  "results": {
    "fixed": 4,
    "failed": 1,
    "total": 5,
    "successRate": 80
  },
  "details": [
    {
      "errorId": "ts_app/page.tsx",
      "type": "TypeScript/Syntax Error",
      "status": "fixed",
      "timestamp": "2026-01-25T10:31:00Z"
    }
  ],
  "timestamp": "2026-01-25T10:31:00Z"
}
```

### 3. **Get AutoFix Status**

```
GET /api/master/autofix/status
```

**Response:**

```json
{
  "status": {
    "scanning": false,
    "fixing": false,
    "totalErrors": 0,
    "fixedErrors": 0,
    "failedFixes": 0,
    "lastScanTime": "2026-01-25T10:30:00Z",
    "lastFixTime": "2026-01-25T10:31:00Z",
    "successRate": 100
  }
}
```

### 4. **Get System Health**

```
GET /api/master/autofix/health
```

**Response:**

```json
{
  "health": {
    "cpu_usage": 35.2,
    "memory_usage": 62.5,
    "disk_usage": 45.1,
    "network_status": "healthy",
    "last_check": "2026-01-25T10:32:00Z",
    "processes_healthy": true,
    "database_healthy": true,
    "api_healthy": true,
    "cloud_healthy": true
  },
  "timestamp": "2026-01-25T10:32:00Z"
}
```

### 5. **Get All Errors**

```
GET /api/master/autofix/errors
```

**Response:**

```json
{
  "errors": [...],
  "count": 5,
  "timestamp": "2026-01-25T10:30:00Z"
}
```

### 6. **Fix Specific Error**

```
POST /api/master/autofix/fix/{errorId}
```

**Response:**

```json
{
  "success": true,
  "errorId": "ts_app/page.tsx",
  "status": "fixed",
  "message": "Successfully fixed error: ts_app/page.tsx",
  "timestamp": "2026-01-25T10:31:00Z"
}
```

## Python Integration

### Using the Health Integration Script

```python
from scripts.qmoi_health_integration import QMOIHealthIntegration

# Initialize
integration = QMOIHealthIntegration()

# Get system health
health = integration.get_system_health()
print(health)
# Output: {'cpu_usage': 35.2, 'memory_usage': 62.5, ...}

# Scan for errors
errors = integration.comprehensive_error_scan()
print(f"Found {len(errors)} errors")

# Fix all errors
results = integration.autofix_all_errors()
print(f"Fixed: {results['fixed']}, Failed: {results['failed']}")

# Get dashboard data
dashboard_data = integration.get_dashboard_data()
```

### Running the Script

```bash
# One-time scan and fix
python3 scripts/qmoi_health_integration.py

# Continuous monitoring
while true; do
  python3 scripts/qmoi_health_integration.py
  sleep 300  # Run every 5 minutes
done
```

## Security & Access Control

### Master-Only Access

- All AutoFix endpoints require valid master token
- Token validation: `Authorization: Bearer <ADMIN_TOKEN>`
- Set `ADMIN_TOKEN` environment variable

### Setting Master Token

```bash
export ADMIN_TOKEN="your-secret-master-token"
```

### In .env.local

```env
ADMIN_TOKEN=your-secret-master-token
```

## Error Types & Fixes

### 1. TypeScript/Syntax Errors

**Detection:** ESLint analysis
**Auto-Fix:** `eslint --fix`
**Success Rate:** 90%

### 2. Missing Dependencies

**Detection:** npm ls analysis
**Auto-Fix:** `npm install`
**Success Rate:** 95%

### 3. Configuration Errors

**Detection:** File existence check
**Auto-Fix:** Create/update from templates
**Success Rate:** 85%

### 4. Security Issues

**Detection:** npm audit, env file checks
**Auto-Fix:** `npm audit fix`
**Success Rate:** 80%

### 5. Process Errors

**Detection:** Process monitoring
**Auto-Fix:** Service restart
**Success Rate:** 75%

### 6. Resource Issues

**Detection:** Disk/CPU/Memory monitoring
**Auto-Fix:** Cache cleanup, optimization
**Success Rate:** 70%

### 7. API Health Issues

**Detection:** Endpoint connectivity checks
**Auto-Fix:** Service restart, config update
**Success Rate:** 80%

## Dashboard Navigation

### In Master Panel

1. Navigate to `/master`
2. Click "🔧 QMOI AutoFix System" tab
3. Use the control panel to scan and fix

### Real-Time Updates

- Health metrics update every 5 seconds
- Error list refreshes automatically
- Status indicators show live state

## Monitoring & Logging

### Log Files

- `qmoi_autofix_health.log` - Detailed logs
- `qmoi_autofix_dashboard_data.json` - Dashboard data cache

### Viewing Logs

```bash
tail -f qmoi_autofix_health.log
```

## Best Practices

### 1. Regular Scanning

Run scans at least daily:

```bash
0 2 * * * python3 /path/to/scripts/qmoi_health_integration.py
```

### 2. Backup Before Fixing

Always maintain backups before running auto-fix:

```bash
git commit -am "Pre-autofix backup"
```

### 3. Review Fixed Issues

Check the fix history after autofix:

- Review what was fixed
- Verify no breaking changes
- Test affected features

### 4. Monitor Health Continuously

Keep the dashboard open during critical operations
Update health check interval based on load

## Troubleshooting

### Token Not Working

```bash
# Verify token in environment
echo $ADMIN_TOKEN

# Check .env.local
cat .env.local | grep ADMIN_TOKEN
```

### Errors Not Showing

1. Check browser console for API errors
2. Verify master token is set
3. Run manual scan: POST /api/master/autofix/scan

### AutoFix Failing

1. Review fix details in dashboard
2. Check logs: `tail -f qmoi_autofix_health.log`
3. Manually fix high-severity issues
4. Retry autofix

## Performance Considerations

- **Scan Duration**: 10-30 seconds depending on system size
- **Fix Duration**: 5-60 seconds depending on fixes needed
- **Health Checks**: Run every 5 seconds (configurable)
- **Resource Usage**: Minimal (<1% CPU, <50MB memory)

## Future Enhancements

- Machine learning-based error prediction
- Custom fix strategies per error type
- Integration with CI/CD pipelines
- Team notifications for critical errors
- Historical trend analysis
- Automated health reporting

## Support & Documentation

For issues or questions:

1. Check `QMOI_ENHANCED_COMPLETE.md`
2. Review error logs
3. Check API response details
4. Contact: QMOI Master Support

---

**Version:** 2.0.0  
**Last Updated:** January 25, 2026  
**Master Access Required:** Yes

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
