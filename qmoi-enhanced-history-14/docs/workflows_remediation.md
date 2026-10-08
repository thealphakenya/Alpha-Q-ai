---
title: "Workflows remediation report"
qmoi_validation_frontmatter: true
---

# Workflows remediation report

_scanned at 2025-10-28T23:42:26.289223Z_

## .github/workflows/auto_release_variations.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Secrets used: GITHUB_TOKEN, PYPI_API_TOKEN, json
- Env vars: GITHUB_TOKEN
- Owner/repo references: actions/checkout, actions/setup-python, docker/build-push-action, docker/setup-buildx-action, softprops/action-gh-release

## .github/workflows/build.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Env vars: NODE_VERSION, QMOI_AUTODEV_ENABLED
- Owner/repo references: actions/checkout, actions/setup-node, actions/setup-python

## .github/workflows/ci.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Secrets used: GITHUB_TOKEN
- Owner/repo references: actions/checkout, actions/setup-node, actions/setup-python

## .github/workflows/github-actions-qmoi-build.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Secrets used: GITHUB_TOKEN
- Env vars: GH_TOKEN, NODE_VERSION, QMOI_AUTODEV_ENABLED, matrix, platform, strategy
- Owner/repo references: actions/checkout, actions/setup-node, actions/setup-python

## .github/workflows/nightly.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Env vars: NODE_VERSION, QMOI_AUTODEV_ENABLED
- Owner/repo references: ./.github, workflows/build-and-publish.yml

## .github/workflows/npm.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Env vars: NODE_VERSION, QMOI_AUTODEV_ENABLED
- Owner/repo references: actions/cache, actions/checkout, actions/setup-node

## .github/workflows/publish-q-alpha.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Secrets used: GITHUB_TOKEN
- Owner/repo references: actions/checkout, actions/setup-node, peaceiris/actions-gh-pages

## .github/workflows/q.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Env vars: NODE_VERSION, QMOI_AUTODEV_ENABLED
- Owner/repo references: actions/checkout, actions/setup-node

## .github/workflows/qmoi-app-build.yml

- Secrets used: QMOI_DISCORD_WEBHOOK, QMOI_EMAIL_PASS, QMOI_EMAIL_RECIPIENT, QMOI_EMAIL_USER, QMOI_SLACK_WEBHOOK, QMOI_TELEGRAM_CHAT, QMOI_TELEGRAM_TOKEN, QMOI_TWILIO_SID, QMOI_TWILIO_TOKEN, QMOI_TWILIO_WHATSAPP
- Env vars: GIT_DEPTH, GIT_SUBMODULE_STRATEGY, NODE_ENV, NODE_VERSION, PYTHONUNBUFFERED, QMOI_AUTODEV_ENABLED, QMOI_CODESPACES, QMOI_DISCORD_WEBHOOK, QMOI_EMAIL_PASS, QMOI_EMAIL_RECIPIENT, QMOI_EMAIL_USER, QMOI_SLACK_WEBHOOK, QMOI_TELEGRAM_CHAT, QMOI_TELEGRAM_TOKEN, QMOI_TWILIO_SID, QMOI_TWILIO_TOKEN, QMOI_TWILIO_WHATSAPP, steps

## .github/workflows/qmoi-autodev.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Issue: no secrets or envs detected (ok)
- Owner/repo references: actions/checkout, actions/setup-python

## .github/workflows/qmoi-ci.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Env vars: NODE_VERSION, QMOI_AUTODEV_ENABLED
- Owner/repo references: actions/checkout, actions/setup-node, actions/setup-python, actions/upload-artifact

## .github/workflows/release.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Secrets used: GH_TOKEN, GITHUB_TOKEN
- Env vars: GH_TOKEN, GITHUB_TOKEN, NODE_VERSION, QMOI_AUTODEV_ENABLED, steps, timeout_minutes
- Owner/repo references: actions/cache, actions/checkout, actions/setup-node, actions/setup-python, actions/upload-artifact, docker/setup-buildx-action, softprops/action-gh-release

## .github/workflows/sync-notify.yml

- Env vars: NODE_VERSION, QMOI_AUTODEV_ENABLED

## .github/workflows/update-readme-cli.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Env vars: NODE_VERSION, QMOI_AUTODEV_ENABLED
- Owner/repo references: actions/checkout, actions/setup-python

## .github/workflows/validate-and-tag-md.yml

- Issue: owner/repo references found; ensure they are templated or use inputs
- Issue: no secrets or envs detected (ok)
- Owner/repo references: actions/checkout, actions/setup-python, actions/upload-artifact

## Suggested remediation steps

1. Move any secrets or API keys to repository secrets or a vault and reference them via `secrets.NAME`.
2. Avoid hard-coding tokens in workflow YAML; use inputs or secrets instead.
3. Template owner/repo references when workflows must run from forks or other users; prefer using inputs or `github.repository`.
4. For workflows that need to run in other users' codespaces, provide a README or `workflows_remediation.md` listing required secrets and how to set them (use `gh secret set`).

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
