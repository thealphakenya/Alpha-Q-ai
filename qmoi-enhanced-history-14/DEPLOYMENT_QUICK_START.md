# Quick Deployment Guide - QMOI Enhanced

## Prerequisites

```bash
# Ensure Node.js 18+ installed
node --version

# Ensure npm/yarn available
npm --version

# Clone the repository
git clone <repository-url>
cd qmoi-enhanced
```

## 1. Configure Environment Variables

```bash
# Copy production template
cp .env.production .env.production.local

# Edit with your production secrets
nano .env.production.local
```

**Critical variables to set:**

- `DATABASE_URL` - PostgreSQL connection
- `JWT_SECRET` - 32+ character random string
- `APP_URL` - Your production domain
- `STRIPE_SECRET_KEY` - If using Stripe
- `SENDGRID_API_KEY` - Email delivery
- Any third-party API keys

## 2. Install Dependencies

```bash
npm install --production
```

## 3. Build Application

```bash
# Production build
npm run ci:build

# Build succeeded? Continue to deployment
```

## 4. Deployment Options

### Option A: Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod

# Add environment variables in Vercel dashboard
# Then redeploy with environment variables set
```

### Option B: Docker

```bash
# Build Docker image
docker build -t qmoi-enhanced:latest .

# Run container
docker run -e DATABASE_URL=postgresql://... \
           -e JWT_SECRET=... \
           -e APP_URL=https://your-domain.com \
           -p 3000:3000 \
           qmoi-enhanced:latest

# Test health endpoint
curl http://localhost:3000/api/health
```

### Option C: Traditional Server (Node.js)

```bash
# Install PM2 for process management
npm install -g pm2

# Create PM2 ecosystem config
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'qmoi-enhanced',
    script: '.next/standalone/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production'
    }
  }]
};
EOF

# Start application
pm2 start ecosystem.config.js

# Monitor
pm2 monit
```

## 5. Verify Deployment

```bash
# Test health endpoint
curl https://your-domain.com/api/health

# Test chat endpoint
curl -X POST https://your-domain.com/api/qmoi/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello"}]}'

# Check logs
tail -f /var/log/qmoi-enhanced.log
```

## 6. Configure Domain & SSL

### With Vercel

- Add custom domain in Vercel dashboard
- SSL certificate auto-configured

### With Traditional Server

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d your-domain.com

# Configure nginx to use certificate
sudo nano /etc/nginx/sites-available/qmoi-enhanced
```

## 7. Setup Monitoring

### Application Monitoring

- Configure error tracking: Sentry.io
- Configure metrics: Datadog/New Relic
- Setup uptime monitoring: UptimeRobot

### Log Aggregation

- CloudWatch (AWS)
- Datadog
- LogRocket
- Papertrail

## 8. Database Setup

```bash
# Run Prisma migrations
npx prisma migrate deploy

# Verify database connection
npx prisma studio  # Opens Prisma Studio for inspection
```

## 9. Backup Configuration

```bash
# Daily database backups (example with pg_dump)
0 2 * * * pg_dump -Fc -h localhost -U postgres qmoi_prod > /backups/qmoi-$(date +\%Y\%m\%d).dump

# Store backups in S3
aws s3 cp /backups/qmoi-*.dump s3://your-backup-bucket/
```

## 10. Performance Optimization

```bash
# Enable caching
# Configure Redis
export REDIS_URL=redis://your-redis-host:6379

# Enable CDN (optional)
# CloudFlare or AWS CloudFront
```

## Common Issues & Solutions

### Issue: Database Connection Refused

```bash
# Verify connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Check database host accessibility
nc -zv <db-host> 5432
```

### Issue: Out of Memory

```bash
# Increase Node.js memory limit
export NODE_OPTIONS="--max-old-space-size=2048"
npm start
```

### Issue: Slow API Responses

```bash
# Check database query performance
npx prisma studio
# Review slow queries in database logs

# Increase database pool size in .env
DATABASE_POOL_MAX=50
```

## Post-Deployment Checklist

- [ ] Application starts without errors
- [ ] Database connection working
- [ ] Health endpoint responding
- [ ] Chat endpoint processing requests
- [ ] Error tracking (Sentry) receiving events
- [ ] Monitoring dashboard showing data
- [ ] Backups running on schedule
- [ ] SSL certificate valid
- [ ] DNS resolving correctly
- [ ] CDN cache working (if applicable)

## Monitoring URLs

Once deployed, monitor these endpoints:

```
Health Check: https://your-domain.com/api/health
Master Panel: https://your-domain.com/master (if configured)
API Docs: https://your-domain.com/api/docs (if configured)
Monitoring: https://your-monitoring-service.com
```

## Rollback Procedure

### Vercel

```bash
vercel rollback
# or select previous deployment in dashboard
```

### Docker/Traditional

```bash
# Stop current version
pm2 stop qmoi-enhanced

# Revert to previous version (from git or docker image)
git checkout previous-commit
npm run ci:build
pm2 start ecosystem.config.js

# Or with Docker
docker stop qmoi-enhanced
docker run -d --name qmoi-enhanced-v2 previous-image:tag
```

## Getting Help

1. Check logs: `pm2 logs qmoi-enhanced`
2. Review error tracking: Sentry.io dashboard
3. Check monitoring: Datadog/New Relic
4. Review GitHub issues: Search known issues
5. Contact support: support@qmoi.app

---

**Production build completed successfully!**  
Ready for deployment with proper environment configuration.

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
