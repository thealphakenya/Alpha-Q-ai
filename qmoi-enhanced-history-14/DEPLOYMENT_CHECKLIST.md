# QMOI Enhanced - Deployment Checklist

## Pre-Deployment (On Your Machine)

### Environment Preparation

- [ ] Clone repository: `git clone https://github.com/thealphakenya/qmoi-enhanced.git`
- [ ] Copy environment template: `cp .env.production.updated .env.production`
- [ ] Create strong JWT_SECRET (32+ chars): `openssl rand -hex 16`
- [ ] Update DATABASE_URL with PostgreSQL credentials
- [ ] Update SLACK_WEBHOOK_URL (optional)
- [ ] Verify Node.js 18+: `node --version`
- [ ] Install PM2 globally: `npm install -g pm2`

### Local Testing

- [ ] Run environment validator: `node scripts/validate-production-env.js`
- [ ] Install dependencies: `npm install --production`
- [ ] Build application: `npm run ci:build`
- [ ] Test locally: `npm start` then `curl http://localhost:3000`

## Deployment (On Production Server)

### Phase 1: Initial Setup

- [ ] SSH to production server
- [ ] Create deployment user: `sudo useradd -m deploy`
- [ ] Create application directory: `sudo mkdir -p /var/www/qmoi-enhanced`
- [ ] Set permissions: `sudo chown deploy:deploy /var/www/qmoi-enhanced`
- [ ] Clone repository as deploy user
- [ ] Copy .env.production to server (securely via SCP)

### Phase 2: Application Deployment

- [ ] Run automated deployment: `bash scripts/deploy-production.sh`
- [ ] Verify processes: `pm2 list` (should show 3 running)
- [ ] Check logs: `pm2 logs` (should show no errors)
- [ ] Test health endpoint: `curl http://localhost:3000/api/health`

### Phase 3: Database Setup

- [ ] Ensure PostgreSQL is running
- [ ] Run database setup: `bash scripts/setup-database.sh`
- [ ] Verify migrations: Check database for tables

### Phase 4: SSL/TLS (Requires Domain + Root Access)

- [ ] Point domain DNS A record to server IP
- [ ] Wait for DNS propagation (~5 minutes): `nslookup qmoi.app`
- [ ] Run SSL setup (as root): `sudo bash scripts/setup-ssl-automated.sh qmoi.app master@qmoi.app`
- [ ] Verify certificate: `sudo certbot certificates`

### Phase 5: Nginx Setup

- [ ] Run Nginx setup (as root): `sudo bash scripts/setup-nginx-automated.sh qmoi.app 3000`
- [ ] Test Nginx config: `sudo nginx -t`
- [ ] Verify HTTPS: `curl https://qmoi.app` (should return 200)

### Phase 6: Monitoring & Backups

- [ ] Initialize monitoring: `node scripts/init-monitoring.js`
- [ ] Setup backups (as root): `sudo bash scripts/setup-backup-system.sh /var/backups/qmoi 30`
- [ ] Test backup: `sudo qmoi-backup /var/backups/qmoi 30`
- [ ] Start monitoring dashboard: `pm2 monit`

### Phase 7: Verification

- [ ] Run verification suite: `bash scripts/verify-deployment.sh`
- [ ] Check all endpoints: `curl https://qmoi.app/api/health`
- [ ] Monitor logs for errors: `pm2 logs qmoi-app --lines 50`
- [ ] Verify processes restart on failure: `kill -9 $(pm2 pid qmoi-app)`

## Post-Deployment

### Immediate (First Hour)

- [ ] Monitor logs for any errors
- [ ] Test key application features
- [ ] Verify database connectivity
- [ ] Check SSL certificate validity

### Short Term (First Day)

- [ ] Monitor performance metrics
- [ ] Review error logs
- [ ] Test backup system
- [ ] Document any issues

### Long Term (Ongoing)

- [ ] Daily: Check PM2 logs and health endpoint
- [ ] Weekly: Review performance metrics
- [ ] Monthly: Update SSL certificate status, security patches
- [ ] Quarterly: Full security audit, capacity planning

## Troubleshooting

### Application Won't Start

```bash
# Check PM2 logs
pm2 logs qmoi-app

# Check environment variables
cat .env.production

# Verify Node.js can start the app locally
node scripts/qmoi-production-init.js
```

### Database Connection Failed

```bash
# Verify DATABASE_URL
grep DATABASE_URL .env.production

# Test connection
psql $DATABASE_URL -c "SELECT 1"

# Check migrations status
npx prisma migrate status
```

### HTTPS Not Working

```bash
# Verify certificate
sudo certbot certificates

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Test Nginx config
sudo nginx -t
```

### PM2 Auto-startup Not Working

```bash
# Verify systemd service
sudo systemctl status pm2-node

# Re-enable auto-startup
pm2 startup systemd -u $USER --hp $HOME
pm2 save
```

## Rollback Procedure

If something goes wrong:

```bash
# 1. Stop all processes
pm2 stop all

# 2. Restore from backup
sudo tar -xzf /var/backups/qmoi-enhanced/app_backup_*.tar.gz -C /var/www

# 3. Restore database
sudo psql $DATABASE_URL < /var/backups/qmoi-enhanced/db_backup_*.sql

# 4. Start processes again
pm2 start pm2.config.cjs

# 5. Verify
pm2 logs
```

## Success Criteria

Your deployment is successful when:

- ✅ All 3 PM2 processes are running
- ✅ Health endpoint responds with 200 OK
- ✅ HTTPS connection works
- ✅ No errors in PM2 logs
- ✅ Database queries return results
- ✅ Application responds to requests in <500ms
- ✅ Auto-restart works (kill process, it restarts)
- ✅ Backups are being collected daily

---

**Need Help?**

- Check logs: `pm2 logs`
- View process status: `pm2 status`
- Monitor in real-time: `pm2 monit`
- Run verification: `bash scripts/verify-deployment.sh`

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
