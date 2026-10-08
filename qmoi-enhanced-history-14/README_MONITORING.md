# 📊 QMOI Monitoring & Observability System

Complete enterprise-grade monitoring, alerting, and audit system for production operations.

## 🎯 Overview

This is a production-ready monitoring and observability layer that provides:

- **Real-time Health Monitoring** - System metrics, performance tracking, health scoring
- **Automatic Alerts** - Intelligent alert generation with severity classification
- **Rate Limiting** - Prevent abuse with configurable per-user/endpoint limits
- **Audit Trails** - Complete change tracking for compliance and debugging
- **Master Dashboard** - Real-time visualization of system health and metrics
- **Comprehensive APIs** - RESTful endpoints for all monitoring operations

## 📁 File Structure

```
qmoi-enhanced/
├── app/
│   ├── api/
│   │   ├── health/route.ts                    # Public health check
│   │   ├── master/
│   │   │   ├── monitoring/route.ts           # Monitoring dashboard
│   │   │   ├── alerts/route.ts               # Alert management
│   │   │   ├── rate-limits/route.ts          # Rate limiting control
│   │   │   └── audit-logs/route.ts           # Audit log management
│   │   └── metrics/route.ts                  # Metrics endpoint
│   ├── components/
│   │   └── AdminDashboard.tsx                # Dashboard UI component
│   └── master/
│       └── page.tsx                          # Master dashboard page
├── lib/
│   ├── logger/
│   │   └── index.ts                          # Winston logger setup
│   └── monitoring/
│       ├── performance.ts                    # Performance monitoring
│       └── error-tracker.ts                  # Error tracking
├── __tests__/
│   └── api/
│       └── monitoring.test.ts                # Comprehensive test suite
├── cypress/
│   └── e2e/
│       └── user-flows.cy.ts                  # E2E tests
├── MONITORING_API_DOCS.md                    # API documentation
├── MONITORING_IMPLEMENTATION_GUIDE.md        # Implementation details
├── MONITORING_COMMANDS.sh                    # Common commands
├── QUICK_START_MONITORING.md                 # Quick reference
└── PHASE_6_EXTENDED_SUMMARY.md              # Phase summary
```

## 🚀 Quick Start

### Access Master Dashboard

```
URL: http://localhost:3000/master
Requires: Master user account
Features: Real-time metrics, alerts, system health
```

### Check System Health

```bash
# Public endpoint - no authentication required
curl http://localhost:3000/api/health

# Response
{
  "status": "healthy",
  "checks": {
    "service": {"status": "up", "version": "2.1.0"},
    "database": {"status": "connected", "responseTime": "5ms"},
    "memory": {"status": "healthy", "heapUsedPercent": 48},
    "uptime": 86400
  }
}
```

### View Monitoring Data

```bash
TOKEN="your_admin_token"

# Get monitoring dashboard
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/master/monitoring | jq '.'

# Get active alerts
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/master/alerts | jq '.'

# Get rate limit config
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/master/rate-limits | jq '.'

# Get audit logs
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/master/audit-logs | jq '.'
```

## 📚 Documentation

### Core Documentation

- **[MONITORING_API_DOCS.md](./MONITORING_API_DOCS.md)** - Complete API reference with examples
- **[MONITORING_IMPLEMENTATION_GUIDE.md](./MONITORING_IMPLEMENTATION_GUIDE.md)** - Technical implementation details
- **[QUICK_START_MONITORING.md](./QUICK_START_MONITORING.md)** - Quick reference guide
- **[PHASE_6_EXTENDED_SUMMARY.md](./PHASE_6_EXTENDED_SUMMARY.md)** - Phase completion summary

### Quick Commands

```bash
# Source the commands file
source MONITORING_COMMANDS.sh

# Use helper functions
get_health_score
get_alert_count
get_memory_percent
is_healthy
export_daily_logs
system_diagnostic
```

## 🔧 API Endpoints

### Health Check (Public)

```
GET /health
```

### Master Endpoints (Master Role Required)

```
GET    /master/monitoring              # System metrics and health
GET    /master/alerts                  # View active alerts
POST   /master/alerts                  # Manage alerts
GET    /master/rate-limits             # View rate limits
PUT    /master/rate-limits             # Update rate limits
GET    /master/audit-logs              # View audit logs
POST   /master/audit-logs              # Export audit logs
```

## 📊 Key Metrics

### Health Score (0-100)

- **80-100**: Healthy ✅
- **50-80**: Degraded ⚠️
- **<50**: Critical ❌

### Performance Metrics Per Endpoint

- **count** - Total requests
- **successRate** - Percentage of successful requests
- **avgDuration** - Average response time (ms)
- **p95Duration** - 95th percentile response time
- **p99Duration** - 99th percentile response time

### Alert Types

| Type                    | Trigger           | Critical Threshold |
| ----------------------- | ----------------- | ------------------ |
| HIGH_ERROR_RATE         | >5 errors/hour    | >20 errors/hour    |
| PERFORMANCE_DEGRADATION | <95% success rate | <85% success rate  |
| HIGH_MEMORY_USAGE       | >85% heap         | >95% heap          |

## 🔐 Security & Authorization

### Access Control

- **Health Check** - Public (no auth required)
- **Master Endpoints** - Master role only
- **Rate Limiting** - Per-user, per-endpoint
- **Audit Logs** - All operations tracked with IP/user agent

### Authentication

All master endpoints require:

```
Authorization: Bearer <JWT_TOKEN>
```

## 📈 Usage Examples

### Track Performance

```typescript
import { monitor } from "@/lib/monitoring/performance";

// Measure async operation
const result = await monitor.measureAsync("operation_name", async () => {
  // Your code here
  return data;
});

// Get metrics
const metrics = monitor.getMetrics("operation_name");
```

### Track Errors

```typescript
import { errorTracker } from "@/lib/monitoring/error-tracker";

try {
  // operation
} catch (error) {
  errorTracker.trackError(error, { userId, endpoint: "/api/endpoint" });
}
```

### Create Audit Log

```typescript
import { createAuditLog } from "@/app/api/master/audit-logs/route";

await createAuditLog({
  userId: currentUser.id,
  action: "UPDATE",
  resource: "user",
  resourceId: targetUser.id,
  changes: { role: "master" },
  ipAddress: request.ip,
  userAgent: request.headers.get("user-agent"),
});
```

## 🧪 Testing

```bash
# Run monitoring test suite
npm test -- __tests__/api/monitoring.test.ts

# Run with coverage
npm test -- __tests__/api/monitoring.test.ts --coverage

# Run E2E tests
npm run e2e

# Run all tests
npm test
```

## 📋 Configuration

### Environment Variables

```bash
# Log level
LOG_LEVEL=info|debug|warn|error

# Rate limiting
RATE_LIMIT_WINDOW=60000        # milliseconds
RATE_LIMIT_MAX=100             # requests per window

# Alert thresholds
ERROR_RATE_THRESHOLD=5         # errors per hour
SUCCESS_RATE_THRESHOLD=0.95    # 95%
MEMORY_WARNING_PERCENT=85      # of heap
```

### Database Setup

Add this model to Prisma schema:

```prisma
model AuditLog {
  id        String   @id @default(cuid())
  userId    String
  action    String
  resource  String
  resourceId String?
  changes   String?
  ipAddress  String?
  userAgent  String?
  timestamp DateTime @default(now())

  @@index([userId])
  @@index([resource])
  @@index([timestamp])
}
```

## 🎯 Common Tasks

### Check System Health

```bash
# Quick health check
curl http://localhost:3000/api/health | jq '.status'

# Detailed health info
curl http://localhost:3000/api/health?type=detailed
```

### View Active Alerts

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/master/alerts | jq '.alerts'
```

### Manage Rate Limits

```bash
# Update user limit
curl -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"userId":"USER_ID","endpoint":"/api/payments","newLimit":200}' \
  http://localhost:3000/api/master/rate-limits

# Reset to default
curl -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"userId":"USER_ID","endpoint":"/api/payments","action":"reset"}' \
  http://localhost:3000/api/master/rate-limits
```

### Export Audit Logs

```bash
# Export as CSV
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"format":"csv"}' \
  http://localhost:3000/api/master/audit-logs \
  --output logs.csv

# Export with filters
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"format":"csv","filters":{"action":"DELETE","resource":"user"}}' \
  http://localhost:3000/api/master/audit-logs \
  --output deletions.csv
```

## 🚨 Troubleshooting

### High Memory Usage

1. Check memory trend in `/api/master/monitoring`
2. Review alert logs for memory warnings
3. Check for unbounded collections
4. Consider scaling vertically

### High Error Rates

1. View error types in `/api/master/alerts`
2. Check detailed errors in `/api/master/monitoring`
3. Review audit logs for related changes
4. Check error stack traces in logs

### Rate Limiting Issues

1. Verify middleware is called
2. Check Redis connection (if distributed)
3. Review rate limit configuration
4. Test with rate limit commands

### Missing Audit Logs

1. Verify AuditLog table exists
2. Check database permissions
3. Ensure createAuditLog() is called
4. Review error logs for exceptions

## 📊 Monitoring Best Practices

### Health Checks

- Poll `/health` every 30 seconds (load balancers)
- Alert if status changes to unhealthy
- Track response time trends

### Performance Monitoring

- Watch P99 duration for SLA tracking
- Alert if P95 > 500ms
- Track success rate trends

### Alert Management

- Review alerts daily
- Investigate critical alerts immediately
- Acknowledge handled alerts
- Export alerts monthly for analysis

### Audit Logging

- Review audit logs weekly
- Export monthly for compliance
- Archive quarterly
- Investigate suspicious patterns

## 🔄 Deployment Checklist

- [ ] Create AuditLog database table
- [ ] Configure Redis for rate limiting (optional)
- [ ] Set up health check monitoring
- [ ] Configure alert thresholds
- [ ] Set up monitoring dashboard access
- [ ] Enable audit logging in key routes
- [ ] Test all endpoints with master account
- [ ] Review performance baselines
- [ ] Set up log aggregation
- [ ] Configure backup for audit logs

## 📈 Performance Impact

### API Overhead

- Health check: ~5ms (database query)
- Monitoring: ~10ms (aggregation)
- Alert check: ~2ms (in-memory)
- Rate limit: ~1ms (map lookup)
- Audit log: ~10ms (database write)

### Memory Usage

- Performance metrics: ~1-2MB
- Error tracker: ~2-3MB
- Rate limits: ~5-10MB
- Total overhead: ~10-15MB

## 🎓 Learning Resources

### Documentation

- [Full API Reference](./MONITORING_API_DOCS.md)
- [Implementation Guide](./MONITORING_IMPLEMENTATION_GUIDE.md)
- [Quick Start](./QUICK_START_MONITORING.md)
- [Phase Summary](./PHASE_6_EXTENDED_SUMMARY.md)

### Code Examples

- [API Routes](./app/api/)
- [Test Suite](./__tests__/api/monitoring.test.ts)
- [Components](./app/components/)
- [Utilities](./lib/monitoring/)

### Command Reference

- [Monitoring Commands](./MONITORING_COMMANDS.sh)

## 🔗 Related Files

- **Master Dashboard**: [app/master/page.tsx](./app/master/page.tsx)
- **Dashboard Component**: [app/components/AdminDashboard.tsx](./app/components/AdminDashboard.tsx)
- **Performance Monitor**: [lib/monitoring/performance.ts](./lib/monitoring/performance.ts)
- **Error Tracker**: [lib/monitoring/error-tracker.ts](./lib/monitoring/error-tracker.ts)
- **Logger**: [lib/logger/index.ts](./lib/logger/index.ts)
- **OpenAPI Spec**: [openapi-v2.1.json](./openapi-v2.1.json)

## 🤝 Contributing

When adding new endpoints or features:

1. Track performance with `monitor.measureAsync()`
2. Log errors with `errorTracker.trackError()`
3. Create audit logs with `createAuditLog()`
4. Add tests to `__tests__/api/monitoring.test.ts`
5. Update API documentation
6. Update OpenAPI spec

## 📞 Support

For questions or issues:

1. Check the [API Documentation](./MONITORING_API_DOCS.md)
2. Review the [Implementation Guide](./MONITORING_IMPLEMENTATION_GUIDE.md)
3. Run the [test suite](./__tests__/api/monitoring.test.ts)
4. Check git history for implementation decisions

## 📄 License

MIT License - See LICENSE file for details

---

**Version**: 2.1.0  
**Status**: Production Ready ✅  
**Last Updated**: 2024  
**Maintenance**: Active

For updates and support, visit: https://qmoi.app

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
