# Merge manifest
# Merge operations
- Branch: 
- Auto-push: 1
- Auto-merge: 0
- Policy: keep docs, tests, routes, manifests, styles, universals, and merge state synchronized securely.
- Last sync: 2026-07-31T00:38:53.046673Z

## Documentation inventory
- @ALLMDFILESREFS.md
- ADVANCED_USER_IDENTIFICATION_SYSTEM.md
- ALLAUTO.md
- ALLBACKEND.md
- ALLCLONEDRELEASES.md
- ALLDEVICESSETTINGS.md
- ALLERRORS.md
- ALLERRORSSTATSQMOI.md
- ALLERRORSTYPESFILES.md
- ALLERRORTYPESANDHEALTHCHECKS.md
- ALLFRONTEND.md
- ALLHOOKSWEBHOOKS.md
- ALLLINKS.md
- ALLMDFILES.md
- ALLMDFILESREFS.md
- ALLPORTS.md
- ALLQMOIAIAPPSREALEASESVERSIONS.md
- ALLQMOIAUTOEVOLVINGENVS.md
- ALLSYSTEMSSTRUCTURESREFERENCES.md
- ALLTESTSAUOTOTESTS.md
- ALLUI.md
- ALLVERSIONS.md
- ALLWALLETSQVS.md
- ALPHAQMOIENGINE.md
- API.md
- API_ENDPOINTS_COMPLETE_AUDIT.md
- API_ENDPOINTS_REFERENCE.md
- API_INTEGRATION_GUIDE.md
- API_REFERENCE.md
- APPS_PLATFORMS_DOCUMENTATION_UPDATE.md
- APP_BUILD_MATRIX.md
- APP_FIX_ACTION_PLAN.md
- APP_FIX_CHECKLIST.md
- APP_FIX_COMPLETE.md
- AUTH_SYSTEM_IMPLEMENTATION.md
- AUTOCLONE_STANDALONE.md
- AUTODEV_SECRETS.md
- AUTODOWNLOAD.md
- AUTOGIT.md
- AUTOLINTREADME.md
- AUTOMATION-SUMMARY.md
- AUTOOPTIMIZEALPHAQMOIENGINE.md
- AUTO_RECOVERY_PROCEDURES.md
- AUTO_SETUP_COMPLETION_SUMMARY.md
- BACKEND_API_TEMPLATES.md
- BACKGROUND_AUTOMATION_COMPLETE.md
- BIOMETRIC_LOGIN_TEST_RESULTS.md
- BUILDAPPSFORALLPLATFORMS.md
- BUILD_COMPLETION_REPORT_v2.md
- BUILD_COMPLETION_SUMMARY.md
- BUILD_INSTRUCTIONS.md
- BUILD_INSTRUCTIONS_PRODUCTION.md
- BUILD_REAL_APPS.md
- BUILD_TRIGGER.md
- CACHING_GUIDE.md
- CAMPAIGN_COMPLETION_SUMMARY.md
- CASHON.md
- CASHONTRADINGREADME.md
- CHANGES.md
- CMDCOMMANDS.md
- COLAB_DAGSHUB_DEPLOY_CHECKLIST.md
- COMPLETE_SYSTEM_DOCUMENTATION_MASTER.md
- COMPLETION_INDEX.md
- COMPLETION_REPORT.md
- COMPLETION_REPORT_REAL_IMPLEMENTATIONS.md
- COMPONENTS.md
- COMPONENTS_MIGRATION_PLAN.md
- COMPREHENSIVE_TESTING_QA_STRATEGY.md
- CONSOLIDATION_ANALYSIS.md
- CONTINUOUS_IMPROVEMENT.md
- CONTRIBUTING.md
- CREDENTIAL_ROTATION_PLAYBOOK.md
- CRITICAL_APP_AUDIT_REPORT.md
- CURLCOMMANDS.md
- CURLQMOIMASTERSISTERUSER.md
- DASHBOARDTRACKS.md
- DEALS.md
- DELIVERABLES_CHECKLIST.md
- DELIVERABLES_FINAL_INVENTORY.md
- DEPLOYMENT-README.md
- ...and 586 more documentation files

## Official deployment references
- Vercel: https://vercel.com/docs (Use official Vercel documentation for deployments, redeployments, environment variables, and build settings.)
- GitHub Actions: https://docs.github.com/actions (Use GitHub Actions documentation for workflow reliability, secrets, and deployment automation.)
- Netlify: https://docs.netlify.com/ (Use Netlify docs for deployment configuration, environment handling, and redeploys.)
- Render: https://render.com/docs (Use Render docs for service deployments, health checks, and runtime environment configuration.)
- Railway: https://docs.railway.app/ (Use Railway docs for environment provisioning and staging deployment flows.)
- Fly.io: https://fly.io/docs/ (Use Fly.io docs for app deployment, scaling, and runtime health checks.)

## Production sync notes
- Ensure API.md, ENDPOINTS.md, ROUTES.md, and DOCS.md all reflect the current implementation.
- Ensure UNIVERSALS.md and STYLES.md remain aligned with the active UI and accessibility guidance.
- Ensure deployment and redeployment workflows reference the official documentation for each supported platform.

## DELS (all deleted after merge)
- tests/test_backup_monitor.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_backup_restore.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_backup_state.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_check_and_replace_placeholders.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_check_placeholders.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_create_release_placeholders.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_fix_removed_placeholders_batch.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_placeholder_fixer.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_placeholder_scanner.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_replace_placeholders.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_run_placeholder_scans.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_scan_placeholders.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_scan_replace_placeholders.py: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.
- tests/test_placeholder_scan.py.ollama.bak: Merged into MERGE.md; file was unused, legacy, or archive-only and removed after integration.

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
