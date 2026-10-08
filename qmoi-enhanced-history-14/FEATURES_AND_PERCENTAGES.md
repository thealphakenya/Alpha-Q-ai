# Features and percentages manifest

## Policy
- The Ollama autonomous agent should keep feature and percentage guidance synchronized with the code and docs so that global behavior and thresholds remain consistent.
- When a new feature, confidence threshold, or percentage-based rule is introduced, it should be documented here and in the relevant runtime manifest.

## Inventory
- percentage: 20 files mention related feature or global guidance
  - .env.example: # QMOI Enhanced - Environment Configuration Template
# Copy this file to .env.local for local development
# For production, use .env.production with actual values

# ==============
  - .eslint_report_parsing_files.txt: _archive_qmoi-enhanced/_app_archived/api/qmoi/voice-preview/route.ts
_archive_qmoi-enhanced/_app_archived/layout.js
_archive_qmoi-enhanced/components/DownloadQApp.tsx
_archive_qmoi
  - .eslintrc.json: {
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "ignorePatterns": [
    "_archive_qmoi-enhanced",
    "d",
    "app",
    "components",
    "dashboard
  - .github/PULL_REQUEST_TEMPLATE/automated_fix.md: <!-- Automated PR Template -->

## Summary

This PR was created automatically by the QMOI CI helper to propose a fix for a common Android build or release issue.

## What changed


  - .github/PULL_REQUEST_TEMPLATE.md: <!-- Describe the purpose of this PR in one sentence -->

## Summary

This PR contains production-enablement changes for the local `qmoi` development server and supporting automati
  - .github/workflows/build-and-release.yml: name: Build and Release

on:
  workflow_dispatch:
  push:
    tags:
      - "v*"

jobs:
  build-android:
    name: Build Android APK
    runs-on: ubuntu-latest
    steps:
      - u
  - .github/workflows/ci-cd.yml: name: CI/CD Pipeline

on:
  push:
    branches: [main, develop, autosync-backup-20250926-232440]
    tags:
      - "v*"
  pull_request:
    branches: [main, develop]
  workflow_dis
  - .github/workflows/ci-monitor.yml: name: CI Monitor

on:
  workflow_run:
    workflows: ["CI Build & Smoke", "Docker Build & Container Smoke"]
    types:
      - completed

permissions:
  issues: write
  pull-reques
- feature: 20 files mention related feature or global guidance
  - .cspell.json: {
  "version": "0.2",
  "language": "en",
  "words": [
    "Colab",
    "alphaq",
    "Qmoi",
    "qmoi",
    "Creds",
    "creds",
    "longname",
    "Platformer",
    "Habari",

  - .devcontainer/devcontainer.json: {
  "name": "QMOI AI - Node.js + Python Dev Environment",
  "image": "mcr.microsoft.com/devcontainers/javascript-node:18-bullseye",
  "features": {
    "ghcr.io/devcontainers/featu
  - .env.example: # QMOI Enhanced - Environment Configuration Template
# Copy this file to .env.local for local development
# For production, use .env.production with actual values

# ==============
  - .eslint_report_parsing_files.txt: _archive_qmoi-enhanced/_app_archived/api/qmoi/voice-preview/route.ts
_archive_qmoi-enhanced/_app_archived/layout.js
_archive_qmoi-enhanced/components/DownloadQApp.tsx
_archive_qmoi
  - .eslintrc.cjs: module.exports = {
  // Temporary global env settings to reduce `no-undef` noise during triage.
  env: {
    node: true,
    browser: true,
    jest: true,
  },
  rules: {
    // T
  - .eslintrc.json: {
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "ignorePatterns": [
    "_archive_qmoi-enhanced",
    "d",
    "app",
    "components",
    "dashboard
  - .github/workflows/build.yml: name: Build QMOI AI
"on":
  push:
    branches:
      - main
  schedule:
    - cron: 0 3 * * *
  workflow_dispatch: null
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      
  - .github/workflows/ci-debug.yml: name: CI Debug (test logs)

on:
  workflow_dispatch:
  pull_request:

permissions:
  contents: write
  issues: write
  actions: write

jobs:
  ci-debug:
    name: CI Debug
    runs
- percentages: 20 files contain percentage values
  - .ollama_agent_audit.jsonl: 100%
  - .qmoi_state/health_memory.json: 35%, 86.27%
  - ADVANCED_USER_IDENTIFICATION_SYSTEM.md: 100%, 40%, 70%, 75%, 85%, 90%, 95%, 98%, 99%
  - API_ENDPOINTS_COMPLETE_AUDIT.md: 99.9%, 99.99%
  - API_INTEGRATION_GUIDE.md: 100%, 5%
  - APP_BUILD_MATRIX.md: 100%, 73%, 75%, 88%, 91%
  - AUTH_SYSTEM_IMPLEMENTATION.md: 85%
  - AUTO_RECOVERY_PROCEDURES.md: 5%, 99%

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
