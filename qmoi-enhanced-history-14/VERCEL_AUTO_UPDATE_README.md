# Vercel Links Auto-Update System

Comprehensive guide for automatically managing and verifying Vercel deployment links in the QMOI Enhanced project.

## 📋 Overview

The Auto-Update System automatically:

- **Verifies** all Vercel deployment links every 5 minutes
- **Updates** VERCELLINKS.md with current deployment status
- **Detects** when deployment goes live (changes from 404 to 200)
- **Integrates** seamlessly with Git hooks and npm scripts
- **Monitors** health check endpoints
- **Reports** detailed deployment status

## 🔗 Key Files

| File                                                         | Purpose                             | Status       |
| ------------------------------------------------------------ | ----------------------------------- | ------------ |
| [VERCELLINKS.md](./VERCELLINKS.md)                           | Master list of all deployment links | ✓ Active     |
| [update_vercel_links.sh](./update_vercel_links.sh)           | Bash script for link verification   | ✓ Executable |
| [scripts/check-deployment.js](./scripts/check-deployment.js) | Node.js deployment checker          | ✓ Executable |
| [setup-git-hooks.sh](./setup-git-hooks.sh)                   | Git hook setup utility              | ✓ Ready      |

## 📍 Deployment Links

### Primary Application

- **URL**: https://qmoi-enhanced.vercel.app
- **Status**: Currently pending deployment
- **Expected**: Goes live in 5-6 minutes

### Vercel Dashboard

- **URL**: https://vercel.com/thealphakenya/qmoi-enhanced
- **Status**: ✓ Live and accessible
- **View**: Deployment logs, environment variables, settings

### GitHub Repository

- **URL**: https://github.com/thealphakenya/qmoi-enhanced
- **Status**: ✓ Live and accessible
- **View**: Source code, commits, pull requests

## 🚀 Usage

### Run Manual Verification

```bash
# Simple update (non-verbose)
npm run update-links

# Verbose output with detailed logs
npm run update-links:verbose

# Force update and commit
npm run update-links:force
```

Or use the bash script directly:

```bash
# Execute bash script
./update_vercel_links.sh

# With verbose logging
./update_vercel_links.sh --verbose

# Force update
./update_vercel_links.sh --force
```

### Check Deployment Status

```bash
# Run Node.js deployment checker
npm run check-deployment

# Or run directly
node scripts/check-deployment.js

# Verify full deployment
npm run verify-vercel
```

## 🔄 Automatic Updates

### npm Scripts

Add these scripts to your workflow:

```json
{
  "scripts": {
    "update-links": "./update_vercel_links.sh",
    "update-links:verbose": "./update_vercel_links.sh --verbose",
    "update-links:force": "./update_vercel_links.sh --force",
    "check-deployment": "node scripts/check-deployment.js",
    "verify-vercel": "npm run update-links && npm run check-deployment"
  }
}
```

### Git Hooks

Setup automatic updates on git events:

```bash
# Initialize git hooks
./setup-git-hooks.sh
```

This creates:

- **post-push hook**: Automatically checks deployment after `git push`
- **pre-commit hook**: Updates VERCELLINKS.md before committing

### Scheduled Cron Jobs

Add to your crontab for periodic checks:

```bash
# Check every 5 minutes
*/5 * * * * cd /workspaces/qmoi-enhanced && ./update_vercel_links.sh >> /tmp/qmoi-links.log 2>&1

# Check every hour
0 * * * * cd /workspaces/qmoi-enhanced && npm run verify-vercel >> /tmp/qmoi-deploy.log 2>&1
```

## 📊 Link Verification Process

The auto-update system:

1. **Tests** each link with HTTP HEAD request
2. **Records** response status code
3. **Compares** with previous status
4. **Updates** VERCELLINKS.md with latest results
5. **Timestamps** each check for tracking
6. **Logs** all activities to `/tmp/qmoi-links.log`

### Status Codes Explained

| Code  | Meaning                          | Action               |
| ----- | -------------------------------- | -------------------- |
| 200   | Link is live and working         | ✓ Success            |
| 404   | Deployment in progress           | ⏳ Wait 5-6 minutes  |
| 000   | Connection timeout or error      | ✗ Check connectivity |
| Other | Server error or misconfiguration | ⚠️ Investigate       |

## 🎯 What Gets Monitored

### Application Links

- **https://qmoi-enhanced.vercel.app** - Main application
- **https://qmoi-enhanced.vercel.app/api** - API base endpoint
- **https://qmoi-enhanced.vercel.app/api/health** - Health check endpoint

### Management Links

- **https://vercel.com/thealphakenya/qmoi-enhanced** - Vercel dashboard
- **https://github.com/thealphakenya/qmoi-enhanced** - GitHub repository

## 📝 VERCELLINKS.md Structure

The main documentation file includes:

```
# QMOI Enhanced - Vercel Deployment Links
├── Last Updated: [timestamp]
├── Status: Ready/Live/In Progress
├── Auto-Update: Enabled/Disabled
├── 🌐 Primary Application Links
├── 📊 Vercel Dashboard & Monitoring
├── 🔧 Repository & Code
├── 🎯 Testing Endpoints
├── 📋 Link Status Summary (auto-updated)
├── 🔄 Auto-Update Configuration
├── 📊 Deployment Verification Checklist
└── 🚀 Quick Actions
```

## 🔍 Example Output

```
═══════════════════════════════════════
    QMOI VERCEL LINKS AUTO-UPDATE REPORT
═══════════════════════════════════════

  ⏳ [404] Primary App
  ⏳ [404] API Base
  ⏳ [404] Health Check
  ✓ [200] Vercel Dashboard
  ✓ [200] GitHub Repository

⏳ Deployment in progress (checking every 5 minutes)

📊 LINK STATUS SUMMARY
────────────────────────────────────────
  [404] Primary App
  [404] API Base
  [404] Health Check
  [200] Vercel Dashboard
  [200] GitHub Repository

✓ Auto-update completed
```

## 🔒 Security Considerations

- **No credentials** stored in VERCELLINKS.md
- **No API keys** logged in output
- **HTTPS only** for all links
- **Read-only** link checking (no POST/PUT requests)
- **Timeout protection** (5-second default)
- **Error isolation** (one failing link doesn't affect others)

## 🐛 Troubleshooting

### Links Keep Showing 404

**Cause**: Deployment still in progress  
**Solution**: Wait 5-6 minutes after push, then refresh  
**Check**: https://vercel.com/thealphakenya/qmoi-enhanced for status

### Script Permission Denied

**Cause**: Script not executable  
**Solution**: Run `chmod +x update_vercel_links.sh`  
**Verify**: `ls -lh update_vercel_links.sh` should show `x` in permissions

### Auto-Update Not Triggering

**Cause**: Git hooks not initialized  
**Solution**: Run `./setup-git-hooks.sh`  
**Verify**: Check `.git/hooks/` directory for hook files

### npm Scripts Not Working

**Cause**: package.json scripts not configured  
**Solution**: Verify `package.json` has the link update scripts  
**Check**: Run `npm run | grep update`

## 📞 Support

For deployment issues:

1. Check [VERCELLINKS.md](./VERCELLINKS.md) for current status
2. Visit [Vercel Dashboard](https://vercel.com/thealphakenya/qmoi-enhanced)
3. Review logs in `/tmp/qmoi-links.log`
4. Check GitHub integration status

## 🎓 Learning Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Git Hooks Guide](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)
- [Bash Scripting](https://www.gnu.org/software/bash/manual/)

---

**Last Updated**: January 18, 2026  
**Version**: 1.0.0  
**Status**: Production Ready

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
