# Quick Start Guide - Monitoring & Master APIs

## Access Master Dashboard

```
URL: http://localhost:3000/master
Requires: Master user account
Features: Real-time metrics, alerts, system health
```

## Check System Health

```bash
# Public endpoint - no auth required
curl http://localhost:3000/api/health

# Response (200 if healthy, 503 if degraded)
{
  "status": "healthy",
  "checks": {
    "database": { "status": "connected", "responseTime": "5ms" },
    "memory": { "status": "healthy", "heapUsedPercent": 48 }
  }
}
```

## View Monitoring Dashboard

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:3000/api/master/monitoring

# Returns: System metrics, performance data, error stats, health score
```

## Manage Alerts

```bash
# Get active alerts
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:3000/api/master/alerts

# Acknowledge an alert
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"alertId":"ALERT_ID","action":"acknowledge"}' \
  http://localhost:3000/api/master/alerts
```

## Control Rate Limits

```bash
# View current rate limits
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:3000/api/master/rate-limits

# Update limit for a user
curl -X PUT \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"userId":"USER_ID","endpoint":"/api/payments","newLimit":200}' \
  http://localhost:3000/api/master/rate-limits
```

## Review Audit Logs

```bash
# Get audit logs
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:3000/api/master/audit-logs?action=DELETE&resource=user&skip=0&take=50"

# Export as CSV
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"format":"csv","filters":{"action":"DELETE"}}' \
  http://localhost:3000/api/master/audit-logs \
  --output audit-logs.csv
```

## Track Performance in Code

```typescript
import { monitor } from "@/lib/monitoring/performance";

// Track async operations
const result = await monitor.measureAsync("operation_name", async () => {
  // Your code here
  return data;
});

// View metrics
const metrics = monitor.getMetrics("operation_name");
console.log({
  count: metrics.count,
  avgDuration: metrics.avgDuration,
  p95Duration: metrics.p95Duration,
  successRate: metrics.successRate,
});
```

## Log Errors

```typescript
import { errorTracker } from "@/lib/monitoring/error-tracker";

try {
  // Some operation
} catch (error) {
  errorTracker.trackError(error, {
    userId: userId,
    endpoint: "/api/endpoint",
    method: "POST",
    statusCode: 500,
  });
}
```

## Create Audit Log Entry

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

## Test Endpoints

```bash
# Run monitoring tests
npm test -- __tests__/api/monitoring.test.ts

# Run with coverage
npm test -- __tests__/api/monitoring.test.ts --coverage
```

## Key Metrics to Watch

| Metric            | Normal | Warning    | Critical |
| ----------------- | ------ | ---------- | -------- |
| Health Score      | 80-100 | 50-80      | <50      |
| Success Rate      | >95%   | 85-95%     | <85%     |
| Error Rate        | <5/hr  | 5-20/hr    | >20/hr   |
| Memory Usage      | <60%   | 60-85%     | >85%     |
| Response Time P95 | <100ms | 100-500ms  | >500ms   |
| Response Time P99 | <200ms | 200-1000ms | >1000ms  |

## Environment Variables

```bash
# Enable debug logging
DEBUG=qmoi:*

# Set log level
LOG_LEVEL=debug|info|warn|error

# Configure rate limiting
RATE_LIMIT_WINDOW=60000        # milliseconds
RATE_LIMIT_MAX=100              # requests per window

# Alert thresholds
ERROR_RATE_THRESHOLD=5          # errors per hour
SUCCESS_RATE_THRESHOLD=0.95     # 95%
MEMORY_WARNING_PERCENT=85       # of heap
```

## Common Issues

**Q: Alerts not showing?**
A: Check if errors are being tracked and the error count threshold is met

**Q: High memory warning?**
A: Monitor memory trends, check for unbounded collections, consider scaling

**Q: Rate limits not working?**
A: Verify middleware is called, check Redis connection if distributed

**Q: Missing audit logs?**
A: Ensure AuditLog table exists, verify permissions, check for creation errors

## Performance Tips

1. **Caching**: Add Redis for frequently accessed data
2. **Indexes**: Add database indexes on: userId, resource, timestamp in audit logs
3. **Cleanup**: Run rate limit cleanup periodically with `cleanupRateLimits()`
4. **Archival**: Archive old audit logs monthly to separate storage
5. **Metrics**: Export metrics to Prometheus/Datadog for long-term analysis

## Related Documentation

- Full API Reference: `MONITORING_API_DOCS.md`
- Implementation Guide: `MONITORING_IMPLEMENTATION_GUIDE.md`
- OpenAPI Spec: `openapi-v2.1.json`
- Test Suite: `__tests__/api/monitoring.test.ts`

## Support Resources

- Check logs in `logs/` directory
- Review git commits for implementation history
- Run tests to verify functionality
- Check error tracker for API errors
- Use master dashboard for real-time insights

---

**Last Updated**: Phase 6 Extended (2024)
**Version**: 2.1.0
**Status**: Production Ready

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
