# ALLAUTO.md

This document inventories the repository automation workflows and the agent responsibilities that keep them healthy.

## Automation inventory
- [.github/workflows/all-links.yml](.github/workflows/all-links.yml)
- [.github/workflows/alllinks-autoupdate.yml](.github/workflows/alllinks-autoupdate.yml)
- [.github/workflows/android-build.yml](.github/workflows/android-build.yml)
- [.github/workflows/apply-on-label.yml](.github/workflows/apply-on-label.yml)
- [.github/workflows/auto-merge-automated-pr.yml](.github/workflows/auto-merge-automated-pr.yml)
- [.github/workflows/auto_release_variations.yml](.github/workflows/auto_release_variations.yml)
- [.github/workflows/build-and-release.yml](.github/workflows/build-and-release.yml)
- [.github/workflows/build-android-replace.yml](.github/workflows/build-android-replace.yml)
- [.github/workflows/build-missing-platforms.yml](.github/workflows/build-missing-platforms.yml)
- [.github/workflows/build.yml](.github/workflows/build.yml)
- [.github/workflows/ci-build-upload.yml](.github/workflows/ci-build-upload.yml)
- [.github/workflows/ci-build.yml](.github/workflows/ci-build.yml)
- [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml)
- [.github/workflows/ci-debug.yml](.github/workflows/ci-debug.yml)
- [.github/workflows/ci-monitor.yml](.github/workflows/ci-monitor.yml)
- [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [.github/workflows/code-quality.yml](.github/workflows/code-quality.yml)
- [.github/workflows/deploy.yml](.github/workflows/deploy.yml)
- [.github/workflows/docker-build-push.yml](.github/workflows/docker-build-push.yml)
- [.github/workflows/docker-image.yml](.github/workflows/docker-image.yml)
- [.github/workflows/dry-run-tests.yml](.github/workflows/dry-run-tests.yml)
- [.github/workflows/enhancer-report.yml](.github/workflows/enhancer-report.yml)
- [.github/workflows/full-start-smoke.yml](.github/workflows/full-start-smoke.yml)
- [.github/workflows/github-actions-qmoi-build.yml](.github/workflows/github-actions-qmoi-build.yml)
- [.github/workflows/install-requirements.yml](.github/workflows/install-requirements.yml)
- [.github/workflows/jest-ci.yml](.github/workflows/jest-ci.yml)
- [.github/workflows/link-cache-maintenance.yml](.github/workflows/link-cache-maintenance.yml)
- [.github/workflows/link-check-schedule.yml](.github/workflows/link-check-schedule.yml)
- [.github/workflows/link-check.yml](.github/workflows/link-check.yml)
- [.github/workflows/link-validation.yml](.github/workflows/link-validation.yml)
- [.github/workflows/nightly.yml](.github/workflows/nightly.yml)
- [.github/workflows/npm.yml](.github/workflows/npm.yml)
- [.github/workflows/ollama-autonomous-agent.yml](.github/workflows/ollama-autonomous-agent.yml)
- [.github/workflows/ollamatrigger.yml](.github/workflows/ollamatrigger.yml)
- [.github/workflows/payed-validation.yml](.github/workflows/payed-validation.yml)
- [.github/workflows/publish-q-alpha.yml](.github/workflows/publish-q-alpha.yml)
- [.github/workflows/publish-releases-realtime.yml](.github/workflows/publish-releases-realtime.yml)
- [.github/workflows/q.yml](.github/workflows/q.yml)
- [.github/workflows/qmoi-app-build.yml](.github/workflows/qmoi-app-build.yml)
- [.github/workflows/qmoi-autodev.yml](.github/workflows/qmoi-autodev.yml)
- [.github/workflows/qmoi-ci.yml](.github/workflows/qmoi-ci.yml)
- [.github/workflows/qmoi-sync-memory.yml](.github/workflows/qmoi-sync-memory.yml)
- [.github/workflows/qmoi-tests.yml](.github/workflows/qmoi-tests.yml)
- [.github/workflows/qvillage-sync.yml](.github/workflows/qvillage-sync.yml)
- [.github/workflows/rebuild-deb-verify-release.yml](.github/workflows/rebuild-deb-verify-release.yml)
- [.github/workflows/release-compliance-check.yml](.github/workflows/release-compliance-check.yml)
- [.github/workflows/release.yml](.github/workflows/release.yml)
- [.github/workflows/run-startup.yml](.github/workflows/run-startup.yml)
- [.github/workflows/scheduled-link-check.yml](.github/workflows/scheduled-link-check.yml)
- [.github/workflows/security-checks.yml](.github/workflows/security-checks.yml)
- [.github/workflows/security.yml](.github/workflows/security.yml)
- [.github/workflows/sync-memory.yml](.github/workflows/sync-memory.yml)
- [.github/workflows/sync-notify.yml](.github/workflows/sync-notify.yml)
- [.github/workflows/sync-releases-from-manifest.yml](.github/workflows/sync-releases-from-manifest.yml)
- [.github/workflows/update-readme-cli.yml](.github/workflows/update-readme-cli.yml)
- [.github/workflows/validate-and-tag-md.yml](.github/workflows/validate-and-tag-md.yml)
- [.github/workflows/vercel-autofix.yml](.github/workflows/vercel-autofix.yml)
- [.github/workflows/verify-release-assets.yml](.github/workflows/verify-release-assets.yml)
- [.github/workflows/wallet-tests.yml](.github/workflows/wallet-tests.yml)

## Production expectations
- Ensure every workflow uses resilient token fallbacks and webhook notifications.
- Keep workflow automation aligned with resumefromhere.txt, ALLHOOKSWEBHOOKS.md, and the live Ollama activity feed.

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
