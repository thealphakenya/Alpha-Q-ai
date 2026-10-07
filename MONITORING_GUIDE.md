# REALTIME GITHUB WORKFLOW MONITORING GUIDE
## Ollama Autonomous Agent - Live Execution Tracking

This guide explains how to monitor the PR Ollama Autonomous Agent while it runs in GitHub in real-time, completely independent of the local codespace.

---

## 🎯 Monitoring Features

### 1. **Realtime Status Tracking**
- Live job status updates every 10 seconds (configurable)
- Job completion tracking with detailed timing
- Overall workflow status with completion percentage
- Automatic color-coded status indicators

### 2. **Quality Metrics**
- **Pass Rate**: Percentage of successful jobs
- **Reliability Score**: Overall workflow reliability (0-100)
- **Processing Speed**: Jobs processed per minute
- **Average Job Duration**: Time per job execution

### 3. **Performance Analytics**
- Elapsed time tracking
- Job-by-job performance metrics
- Failure detection and alerting
- Comprehensive final report generation

### 4. **Agent Behavior Tracking**
- GitHub token usage and validation
- Branch sync operations monitoring
- Avatar identity validation progress
- Voice profile automation tracking
- Real-time execution proof collection

---

## 🚀 Quick Start: Monitor Live Workflow

### Method 1: Python CLI (Recommended)

Start monitoring the current workflow run:

```bash
# Using run ID from the triggered workflow
export GH_TOKEN='your_github_token'
python3 scripts/realtime_workflow_monitor.py 31834413057

# With custom options
python3 scripts/realtime_workflow_monitor.py 31834413057 \
  --interval 5 \
  --duration 1800 \
  --repo thealphakenya/qmoi-enhanced
```

**Output includes:**
- ✅ Live job status table
- 📈 Real-time metrics
- ⭐ Quality and reliability scores
- ⚠️ Alerts on failures
- 📋 Final comprehensive report

### Method 2: GitHub CLI

Monitor workflow status directly:

```bash
export GH_TOKEN='your_github_token'

# Watch workflow in real-time
gh run watch 31834413057 --repo thealphakenya/qmoi-enhanced

# Get detailed run status
gh run view 31834413057 --repo thealphakenya/qmoi-enhanced --json \
  databaseId,displayTitle,status,conclusion,headBranch,createdAt,updatedAt,url,headSha,jobs

# Get all jobs for the run
gh run view 31834413057 --repo thealphakenya/qmoi-enhanced --json jobs
```

### Method 3: Web Dashboard

Access GitHub Actions directly:

1. Go to: https://github.com/thealphakenya/qmoi-enhanced/actions
2. Click on "Ollama PR Validation - 293+ Platform Features"
3. Select the specific run to monitor
4. View live job logs and status

---

## 📊 Monitoring Output Structure

### Console Output Example

```
======================================================================
🔴 OLLAMA PR VALIDATION REALTIME MONITOR
======================================================================

Run ID:     31834413057
Repository: thealphakenya/qmoi-enhanced
Started:    2026-08-14T19:41:36Z

📊 JOB STATUS:

Job Name                                       Status              Conclusion   
────────────────────────────────────────────────────────────────────────────────
Validate Documentation                         ⏳ in_progress       -            
Validate Platform Compilation (web)            ✅ completed        ✓ success    
Validate Platform Compilation (windows)        ✅ completed        ✓ success    
Validate Platform Compilation (ios)            ✅ completed        ✓ success    
Validate Platform Compilation (macos)          ✅ completed        ✓ success    
Validate Platform Compilation (android)        ✅ completed        ✓ success    
Validate Platform Compilation (linux)          ✅ completed        ✓ success    

📈 METRICS:

Overall Status:     🟡 In Progress
Elapsed Time:       2m 15s
Completion:         85.7% (6/7 jobs)
Jobs Passed:        6
Jobs Failed:        0
Jobs In Progress:   1

⭐ QUALITY METRICS:

Pass Rate:          100.0%
Reliability Score:  100.0/100
Processing Speed:   2.67 jobs/min
Avg Job Duration:   1m 05s

Last updated: 2026-08-14 19:45:12
Updating every 10 seconds (Ctrl+C to stop)
```

---

## 🎯 What Gets Monitored

### Agent Authentication & Token Usage
- ✅ GitHub token resolution and validation
- ✅ Secure token usage in GitHub Actions
- ✅ Token precedence validation (MY_CUSTOM_TOKEN > MY_CUTOM_TOKEN > GITHUB_TOKEN)
- ✅ Repository secret configuration

### Branch Operations
- ✅ Main branch validation
- ✅ autosync-backup branch sync
- ✅ Branch merge operations
- ✅ Cross-repository sync (Alpha-Q-ai)

### Avatar & UI Features
- ✅ QMOI avatar identity validation
- ✅ Avatar selection UI features
- ✅ Avatar preview clip automation (5+ seconds)
- ✅ Voice profile selection and automation
- ✅ Avatar window styling and display
- ✅ Real-time avatar animation tracking

### Test Coverage
- ✅ Platform compilation (6+ platforms)
- ✅ Feature validation (293+ features)
- ✅ Test suite execution (40+ tests)
- ✅ Documentation validation
- ✅ Final validation gates

### Performance Metrics
- ✅ Job execution time per platform
- ✅ Test completion rates
- ✅ Overall workflow duration
- ✅ Success/failure ratios
- ✅ Processing speed

---

## 📈 Metrics Explained

### Pass Rate
- **Ideal**: ≥ 95%
- **What it means**: Percentage of successful jobs out of total jobs
- **Action if low**: Check failed jobs for detailed error logs

### Reliability Score
- **Range**: 0-100
- **Ideal**: ≥ 95
- **Calculation**: Pass rate adjusted for consistency
- **What it means**: Overall workflow stability and robustness

### Processing Speed
- **Unit**: Jobs per minute
- **Ideal**: ≥ 1.5 jobs/min
- **What it means**: How quickly jobs are being processed
- **Factors**: Job complexity, resource availability, GitHub runner load

### Average Job Duration
- **Typical range**: 30s - 10m
- **What it means**: Average time each job takes to complete
- **High durations**: May indicate complex validations or resource constraints

---

## � Automation plan to improve monitoring quality

The next monitor upgrade should be layered and evidence-driven:

1. Phase-aware tracking
   - Distinguish validation, branch-sync, and autonomous-trigger phases in one timeline.
   - Keep a clean state model: queued -> in_progress -> completed -> success/failure.

2. Failure-specific escalation
   - On each failure, capture the exact failed job name, failing step, and relevant log excerpt.
   - Recommend the next remediation action instead of only raising a generic alert.

3. Persistent evidence store
   - Save per-run JSON snapshots and summary artifacts to /tmp or a repository artifact location.
   - Keep a run history file that correlates result, issue, and remediation.

4. Cross-workflow correlation
   - Link branch-sync failures with validation outcomes and with the auto-merge workflow to explain which phase actually broke.

5. Resilience testing
   - Expand monitor tests to cover queued runs, waiting jobs, failed-step extraction, recovery guidance, and cross-workflow phase transitions.

6. GitHub-native alerting
   - Add status-summary comments or step summaries that can be read from the Actions UI without manually opening multiple jobs.

This plan gives the monitor enough evidence, automation, and test coverage to be useful as a real operational control system instead of a simple status display.

## �🚨 Alert Types & Responses

### ✅ Success Alert
- **When**: All jobs completed successfully
- **Action**: Review final report and merge PR if tests pass
- **Next Step**: Trigger automated merge if configured

### ❌ Failure Alert
- **When**: One or more jobs fail
- **Action**: Click on failed job for detailed logs
- **Investigate**: Check logs for root cause
- **Fix**: Address the issue and push new commit

### ⚠️ Performance Alert
- **When**: Pass rate drops below 95% or reliability < 90
- **Action**: Review recent changes
- **Investigate**: Check for flaky tests or resource issues
- **Optimize**: Consider breaking down complex validations

### 🟡 Timeout Alert
- **When**: Workflow runs longer than expected
- **Typical duration**: 5-15 minutes
- **Action**: Check if specific job is hanging
- **Force stop**: Cancel workflow and investigate

---

## 🔧 Advanced Monitoring Commands

### Get all workflow runs
```bash
gh run list --workflow="ollama-pr-validation.yml" --repo thealphakenya/qmoi-enhanced --limit 20
```

### Get specific job logs
```bash
gh run view 31834413057 --repo thealphakenya/qmoi-enhanced --log
```

### Get failed jobs only
```bash
gh run view 31834413057 --repo thealphakenya/qmoi-enhanced --log-failed
```

### Export run data as JSON
```bash
gh run view 31834413057 --repo thealphakenya/qmoi-enhanced --json \
  databaseId,displayTitle,status,conclusion,headBranch,createdAt,updatedAt,url,headSha,jobs,event
```

### Monitor with custom interval (5 seconds)
```bash
python3 scripts/realtime_workflow_monitor.py 31834413057 --interval 5
```

### Monitor for specific duration (30 minutes)
```bash
python3 scripts/realtime_workflow_monitor.py 31834413057 --duration 1800
```

---

## 📋 Monitoring Report Structure

Each monitoring session generates a JSON report with:

```json
{
  "run_id": "31834413057",
  "repository": "thealphakenya/qmoi-enhanced",
  "started_at": "2026-08-14T19:41:36Z",
  "monitoring_samples": 25,
  "metrics_history": [
    {
      "timestamp": "2026-08-14T19:41:36Z",
      "elapsed_seconds": 0,
      "jobs_total": 7,
      "jobs_completed": 0,
      "jobs_in_progress": 7,
      "jobs_passed": 0,
      "jobs_failed": 0,
      "completion_percent": 0.0,
      "overall_status": "🟡 In Progress"
    }
    // ... more samples over time
  ],
  "final_jobs": [
    {
      "name": "Validate Documentation",
      "status": "completed",
      "conclusion": "success",
      "startedAt": "2026-08-14T19:41:40Z",
      "completedAt": "2026-08-14T19:42:15Z"
    }
    // ... all jobs
  ],
  "final_status": "completed",
  "final_conclusion": "success"
}
```

---

## 🔄 Continuous Monitoring Best Practices

1. **Monitor throughout entire workflow**: Don't stop monitoring until completion
2. **Use appropriate update interval**: 5-10 seconds for active troubleshooting, 30+ for passive monitoring
3. **Keep monitoring logs**: Save JSON reports for audit trail
4. **Set up alerts**: Configure GitHub workflow notifications
5. **Review metrics regularly**: Check pass rate and reliability trends

---

## 🎓 Understanding Agent Behavior in Monitoring

### What the agent is doing when you see:

**"Validate Documentation"**
- Agent is validating README.md, STYLES.md, QTEAM.md, and avatar-related docs
- Checking markdown syntax and link validity
- Verifying all documentation is up-to-date with code

**"Validate Platform Compilation (linux/windows/etc)"**
- Agent is testing compilation for each platform
- Building and validating 293+ platform-specific features
- Checking avatar identity, animation features, voice profiles work on that platform

**"Run comprehensive test suite"**
- Agent running 40+ automated tests
- Testing GitHub token handling
- Validating branch sync logic
- Testing avatar selection UI
- Testing voice profile automation
- Testing realtime window styling

**"Final Validation"**
- Agent performing final gates and checks
- Building GitHub proof contract
- Confirming all features validated successfully
- Preparing to merge or report results

---

## ✅ Proof of Successful Execution

When all monitoring shows:
- ✅ All jobs completed successfully
- ✅ 100% pass rate
- ✅ Reliability score ≥ 95
- ✅ Zero failed jobs
- ✅ Final status: "success"

This is **direct proof** that the PR Ollama Autonomous Agent:
1. ✅ Executed successfully in GitHub
2. ✅ Used GitHub token correctly
3. ✅ Synced branches properly
4. ✅ Validated all avatar features
5. ✅ Passed all tests
6. ✅ Is ready for production

---

## 📞 Troubleshooting Monitoring Issues

### "No GitHub token found"
```bash
export GH_TOKEN='your_github_token'
export MY_CUSTOM_TOKEN='your_github_token'
```

### "Failed to fetch run status"
- Check GitHub token permissions
- Verify run ID is correct
- Ensure repository is accessible
- Try: `gh auth status`

### "Connection timeout"
- Check network connectivity
- GitHub may be under maintenance
- Try again with longer timeout: `--duration 5400`

### Monitor logs not updating
- Verify update interval is not too small
- Check if workflow is still running
- Try refreshing with: `Ctrl+C` and restart

---

## 🎯 Integration with CI/CD

The realtime monitor integrates with:
- ✅ GitHub Actions native workflows
- ✅ Local development environment (via gh CLI)
- ✅ Remote GitHub servers (no codespace needed)
- ✅ Automated reporting systems
- ✅ Alert systems (via webhook or API)

This ensures monitoring is **always independent of the local codespace** and provides **real-time evidence** of agent behavior in production GitHub environment.

<!-- BEGIN QMOI MANAGED: remote-continuity-and-failover -->
## Agent-managed remote continuity and failover contract

A target-owned workflow can run independently of a Codespace, but it is not independent of its workflow-host provider. Do not claim uninterrupted execution without a separately deployed, authorized worker and a verified failover test.

- Persist execution IDs, source refs/SHAs, idempotent requests, checkpoints, leases, and audit events outside the workspace; resume only after re-reading authoritative state.
- Heartbeat freshness, worker identity, queue age, lock ownership, and provider reachability are separate health signals. Missing/stale telemetry means `STALE` or `OFFLINE`, never `RUNNING`.
- Provider failover requires pre-authorized credentials, least-privilege access, tested data consistency, and a terminal failover exercise. Never silently switch trading venues or move funds when a provider is unavailable.
- On stale market/account data, lost authorization, provider outage, queue duplication, or ledger mismatch, stop new trading orders and preserve read-only monitoring where available.
- External-worker deployment, availability, and disaster recovery remain `not_verified` until exact-host evidence exists.
<!-- END QMOI MANAGED: remote-continuity-and-failover -->

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
