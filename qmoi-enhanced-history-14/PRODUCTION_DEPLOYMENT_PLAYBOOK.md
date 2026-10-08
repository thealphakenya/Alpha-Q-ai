# QMOI Enhanced - Production Deployment Playbook

## Pre-Deployment Checklist

- [ ] Domain registered and DNS configured
- [ ] Server provisioned (2GB+ RAM, 2+ CPU cores)
- [ ] PostgreSQL database configured
- [ ] Nginx installed and configured
- [ ] SSL/TLS certificate obtained
- [ ] Monitoring service account created
- [ ] Backup system configured

## Deployment Steps

### Phase 1: Environment Setup

```bash
# 1. Clone repository
git clone https://github.com/thealphakenya/qmoi-enhanced.git
cd qmoi-enhanced

# 2. Configure environment
cp .env.production.updated .env.production

# 3. Update DATABASE_URL
export DATABASE_URL="postgresql://user:pass@host:5432/db"

# 4. Install dependencies
npm install --production
npm run ci:build
```

### Phase 2: Database Setup

```bash
# 1. Create database
createdb qmoi_production

# 2. Run migrations
npx prisma migrate deploy

# 3. Seed initial data (if needed)
npm run seed
```

### Phase 3: Process Management

```bash
# 1. Start with PM2
pm2 start pm2.config.cjs

# 2. Save PM2 configuration
pm2 save

# 3. Setup auto-startup
pm2 startup systemd -u node --hp /home/node
```

### Phase 4: Web Server Configuration

```bash
# 1. Setup Nginx
sudo cp nginx.conf.template /etc/nginx/sites-available/qmoi.app
sudo ln -s /etc/nginx/sites-available/qmoi.app /etc/nginx/sites-enabled/

# 2. Configure SSL
sudo certbot certonly --nginx -d qmoi.app

# 3. Test and restart
sudo nginx -t
sudo systemctl restart nginx
```

### Phase 5: Monitoring & Alerts

```bash
# 1. Configure alerts
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."
pm2 restart qmoi-health

# 2. Start monitoring
pm2 monit

# 3. Verify health endpoint
curl https://qmoi.app/api/health
```

## Post-Deployment Verification

```bash
# Check all processes running
pm2 status

# Verify HTTPS
curl -I https://qmoi.app

# Test API endpoints
curl https://qmoi.app/api/health
curl https://qmoi.app/api/status

# Monitor resources
pm2 monit

# View logs
pm2 logs
```

## Scaling (Horizontal)

### Add Additional Instances

```bash
# Switch to cluster mode
pm2 stop pm2.config.cjs
pm2 start pm2-cluster.config.cjs

# Verify load distribution
pm2 status
```

### Load Balancing

- Nginx distributes traffic across instances
- PM2 manages process restarts
- Health monitoring ensures uptime
- Automatic failover on process crash

## Maintenance Schedule

### Daily

- Check PM2 logs for errors
- Monitor CPU/Memory usage
- Verify health endpoint

### Weekly

- Review error patterns
- Check disk space
- Verify backup completion

### Monthly

- Update dependencies
- Review performance metrics
- Update SSL certificate (if needed)

### Quarterly

- Security audit
- Performance optimization
- Disaster recovery drill

## Troubleshooting

### App not responding

```bash
pm2 logs qmoi-app
pm2 restart qmoi-app
```

### High memory usage

```bash
pm2 monit
pm2 kill
pm2 start pm2.config.cjs
```

### SSL certificate issues

```bash
sudo certbot renew --force-renewal
sudo systemctl restart nginx
```

### Database connection failing

```bash
# Verify DATABASE_URL
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL
```

## Rollback Procedure

```bash
# If issues occur after deployment
git checkout previous-version
npm run ci:build
pm2 restart all
```

## Success Indicators

✅ All 3 PM2 processes online
✅ HTTPS working (no warnings)
✅ API health endpoint responding
✅ Zero request errors in monitoring
✅ CPU usage < 80%
✅ Memory usage < 80%
✅ Response time < 500ms

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
