---
title: "Security Automation & Vulnerability Remediation"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# Security Automation & Vulnerability Remediation

## Overview

This document describes the automated security vulnerability remediation system for QMOI.

## Features

- **GitHub Security Alerts Integration**: Automatically fetches vulnerability alerts from GitHub.
- **Automated Remediation**:
  - Runs `npm audit fix` to auto-fix vulnerabilities.
  - Runs `snyk wizard` for advanced remediation.
  - Optionally creates PRs or issues for unresolved vulnerabilities.
- **Continuous Monitoring**: Integrated into the master automation system for regular checks.
- **Reporting**: Generates security reports and logs actions taken.

## How It Works

1. **Fetch Alerts**: Uses GitHub API to fetch open security alerts.
2. **Run Fixes**: Executes `npm audit fix` and `snyk wizard`.
3. **Create PRs/Issues**: If vulnerabilities remain, creates a pull request or GitHub issue for manual review.
4. **Log & Report**: All actions are logged and summarized in `reports/security_automation_report.json`.

## Usage

- The master automation system runs security checks automatically.
- You can trigger manually:
  ```bash
  python scripts/qmoi_security_automation.py --auto-fix --report
  ```

## Configuration

- See `config/security_automation.json` for settings (e.g., GitHub token, schedule).

### GitHub token handling (QMOI secret manager)

QMOI can securely store and use a GitHub personal access token for automation tasks (creating PRs, pushing fixes, fetching alerts). The repository includes a minimal secret manager that:

- Encrypts secrets using a master key stored in the OS keyring or provided as `QMOI_MASTER_KEY` (base64 urlsafe).
- Stores encrypted secrets under `.qmoi/` (e.g. `.qmoi/github_token.enc`, `.qmoi/ngrok_token.enc`).
- Provides CLI helpers: `scripts/qmoi_bootstrap_secrets.py` to generate a master key and encrypt tokens, and `scripts/qmoi_git_wrapper.py` to run git commands using the decrypted token.

Important notes and warnings:

- Do NOT commit unencrypted tokens to the repository. If you previously committed the token, rotate it immediately.
- The scripts included are minimal helpers for convenience. For production, integrate with a managed secrets store (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) and implement proper key rotation and audit logging.

Example bootstrap (creates encrypted GH token and optional git helper):

```bash
pip install -r scripts/requirements-secrets.txt
python scripts/qmoi_bootstrap_secrets.py --github-token "<YOUR_GH_TOKEN>" --store-keyring --create-git-helper
```

This creates `.qmoi/github_token.enc` and a helper `.qmoi/git-credential-qmoi.sh` which can be configured as a git credential helper.

## Best Practices

- Review security reports regularly.
- Keep dependencies up to date.
- Address high/critical vulnerabilities promptly.

## Related

- See `TROUBLESHOOTING.md` for common issues.
- See `README.md` for automation commands.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/SECURITY_AUTOMATION.md",
"validated_at": "2025-10-26T20:51:24.838556Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "Security Automation & Vulnerability Remediation"
},
{
"name": "links",
"ok": true,
"detail": []
}
],
"passed": true,
"summary": {
"total_checks": 2,
"passed": true
}
}

<!-- QMOI_VALIDATION_END -->

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
