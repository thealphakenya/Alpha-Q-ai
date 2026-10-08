---
title: "QMOI GitLab Self-Healing CI/CD Automation"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI GitLab Self-Healing CI/CD Automation

## Overview

QMOI now includes a self-healing automation script for GitLab CI/CD. This script automatically detects and fixes common errors in `.gitlab-ci.yml` (such as typos in script paths), commits the fix, pushes it, and triggers a new pipeline. All actions are logged for audit and debugging.

## How It Works

- On pipeline failure, the script fetches the latest failed job log using the GitLab API.
- It scans for common errors (e.g., `No such file or directory`, `command not found`).
- If a typo in a file path is detected, it uses fuzzy matching to suggest and apply the correct path.
- The script patches `.gitlab-ci.yml`, commits, pushes, and triggers a new pipeline.
- All actions are logged to `logs/ci-self-heal.log`.

## Requirements

- Node.js environment in CI/CD
- Environment variables:
  - `GITLAB_TOKEN`: Personal access token with API access
  - `GITLAB_PROJECT_ID`: Numeric project ID
  - `GITLAB_TRIGGER_TOKEN`: (optional) Pipeline trigger token

## Integration Steps

1. Add `scripts/ci-self-heal.js` to your repository.
2. Ensure `node-fetch` and `js-yaml` are available (see `requirements/ai_automation.txt`).
3. Add a job to `.gitlab-ci.yml` to run the script on failure (see below).
4. Set the required environment variables in your GitLab CI/CD settings.

## Example `.gitlab-ci.yml` Addition

```yaml
ci_self_heal:
  stage: fix
  image: node:18
  script:
    - node scripts/ci-self-heal.js
  only:
    - main
  when: on_failure
```

## Logs

- All actions and fixes are logged in `logs/ci-self-heal.log` for review.

## Persistent Failure Notifications

If the same error persists for multiple runs (default: 2), QMOI will send notifications to Slack and/or email if configured.

### Slack

- Set `SLACK_WEBHOOK_URL` as a CI/CD variable or in your `.env` file.

### Email

- Set the following env vars:
  - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `EMAIL_TO`, `EMAIL_FROM`
- QMOI will send an email when persistent failures are detected.

You can adjust the notification threshold with `PERSISTENT_FAIL_THRESHOLD` (default: 2).

All notifications are logged in `logs/ci-self-heal.log`.

## Gmail Notification Integration

- All progress and result notifications for GitLab CI self-healing and autotest are sent to rovicviccy@gmail.com via Gmail.
- Environment variables are managed by scripts/qmoi-environment-setup.js.
- See scripts/ci-self-heal.js and scripts/autotest/advanced_autotest_system.py for implementation details.

## Security

- Tokens are loaded from environment variables and never logged or committed.

## Cross-Platform Support

QMOI self-healing automation is designed to work with GitLab, GitHub Actions, and Vercel. Platform detection is automatic based on environment variables, or you can set `QMOI_CI_PLATFORM` to `gitlab`, `github`, or `vercel` to force a platform.

- **GitLab:** Full support (API, auto-fix, notifications)
- **GitHub Actions:** Coming soon (API integration in progress)
- **Vercel:** Coming soon (API integration in progress)

See the script for details and future updates.

## See Also

- [REFERENCES.md](REFERENCES.md)

> **Note:** QMOI now supports GitHub Actions self-healing automation. See [QMOIGITHUBDEV.md](QMOIGITHUBDEV.md) for details.

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/QMOIGITLABDEV.md",
"validated_at": "2025-10-26T20:51:22.713327Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI GitLab Self-Healing CI/CD Automation"
},
{
"name": "links",
"ok": true,
"detail": [
{
"label": "REFERENCES.md",
"target": "./REFERENCES.md",
"ok": true
},
{
"label": "QMOIGITHUBDEV.md",
"target": "./QMOIGITHUBDEV.md",
"ok": true
}
]
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
