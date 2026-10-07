# WORKFLOWS.md

This document records the repository's GitHub Actions workflow inventory and canonical workflow file state.

## Workflow inventory
- .github/workflows/all-links.yml — Regenerate ALLLINKS
- .github/workflows/alllinks-autoupdate.yml — ALLLINKS Autoupdate
- .github/workflows/android-build.yml — Android CI (QMOI)
- .github/workflows/apply-on-label.yml — Apply ALLLINKS on label
- .github/workflows/auto-merge-automated-pr.yml — Auto-merge automated proposals
- .github/workflows/auto_release_variations.yml — Auto Release LION Variations
- .github/workflows/build-and-release.yml — Build and Release
- .github/workflows/build-android-replace.yml — Build Android & SmartTV and Replace Release Asset
- .github/workflows/build-missing-platforms.yml — Build Missing Platforms
- .github/workflows/build.yml — Build QMOI AI
- .github/workflows/ci-build-upload.yml — CI Build & Release
- .github/workflows/ci-build.yml — CI Build & Smoke
- .github/workflows/ci-cd.yml — CI/CD Pipeline
- .github/workflows/ci-debug.yml — CI Debug (test logs)
- .github/workflows/ci-monitor.yml — CI Monitor
- .github/workflows/ci.yml — CI Build & Test
- .github/workflows/code-quality.yml — Code Quality
- .github/workflows/deploy.yml — Production Deployment
- .github/workflows/docker-build-push.yml — Build and Push Docker image (GHCR)
- .github/workflows/docker-image.yml — Docker Build & Container Smoke
- .github/workflows/dry-run-tests.yml — CI - Dry-run Tests
- .github/workflows/enhancer-report.yml — Enhancement Report
- .github/workflows/full-start-smoke.yml — Full Start Smoke Test
- .github/workflows/github-actions-qmoi-build.yml — QMOI Multi-Platform Build & Publish
- .github/workflows/install-requirements.yml — Install and verify Python dependencies
- .github/workflows/jest-ci.yml — CI - Autotest & Jest
- .github/workflows/link-cache-maintenance.yml — Link Cache Maintenance
- .github/workflows/link-check-schedule.yml — Link & DNS checker (daily)
- .github/workflows/link-check.yml — Link & DNS check
- .github/workflows/link-validation.yml — Link Validation (dry-run)
- .github/workflows/nightly.yml — Nightly
- .github/workflows/npm.yml — CI
- .github/workflows/ollama-autonomous-agent.yml — Ollama autonomous agent
- .github/workflows/ollamatrigger.yml — Ollama trigger workflow
- .github/workflows/payed-validation.yml — Payed Validation
- .github/workflows/publish-q-alpha.yml — Publish Q Alpha PWA
- .github/workflows/publish-releases-realtime.yml — 🚀 QMOI Real-time Multi-Platform Release Publisher
- .github/workflows/q.yml — QMOI Enhanced CI/CD
- .github/workflows/qmoi-app-build.yml — QMOI App Build
- .github/workflows/qmoi-autodev.yml — QMOI Autodev Pipeline
- .github/workflows/qmoi-ci.yml — QMOI AI Build & Release
- .github/workflows/qmoi-sync-memory.yml — qmoi-memory-sync
- .github/workflows/qmoi-tests.yml — QMOI Tests
- .github/workflows/qvillage-sync.yml — QVillage Sync - QMOI Memory ↔ HF Spaces
- .github/workflows/rebuild-deb-verify-release.yml — Rebuild and Replace corrupted .deb
- .github/workflows/release-compliance-check.yml — Release Compliance Check
- .github/workflows/release.yml — LION Variations Release
- .github/workflows/run-startup.yml — Run Startup & Verification (CI)
- .github/workflows/scheduled-link-check.yml — Scheduled Link Check
- .github/workflows/security-checks.yml — Security Checks (Pre-Merge)
- .github/workflows/security.yml — Security Audit
- .github/workflows/sync-memory.yml — QM OI Memory Sync
- .github/workflows/sync-notify.yml — Sync Notify
- .github/workflows/sync-releases-from-manifest.yml — Sync Releases From Manifest
- .github/workflows/update-readme-cli.yml — Update README CLI Usage
- .github/workflows/validate-and-tag-md.yml — Validate and Tag Markdown
- .github/workflows/vercel-autofix.yml — Vercel build + autofix
- .github/workflows/verify-release-assets.yml — Verify Release Assets
- .github/workflows/wallet-tests.yml — Wallet unit tests

## Notes
- Keep WORKFLOWS.md synchronized with .github/workflows and ALLAUTO.md.
- Merge or remove redundant workflow definitions before applying workflow fixes.

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
