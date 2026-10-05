# ALLTESTSAUTOTESTS.md

<!-- BEGIN QMOI MANAGED: active-test-feature-coverage -->
## Agent-managed active test inventory

Scope: current checkout's tracked and non-ignored files only. Historical refs, peer repositories, and unfetched PR trees require separate audit artifacts.

- Active-checkout test files discovered: `13`.
- Snapshot test files discovered (not active coverage): `25`.
- Historical/archive test files discovered (not active coverage): `525`.
- Total test-like paths discovered across these scopes: `563`.
- UI feature registry rows: `24`; registry entries are requirements, not proof of implementation or test coverage.
- Coverage state: `discovered_unmapped` until a feature ID maps to implementation files, positive/negative tests, and an exact-SHA run result.
- Completion state: `tested_local` and `tested_remote` are separate; remote status requires a terminal target-owned run for the exact source SHA.

### Test files discovered

| Test path | Source scope | Feature mapping | Status |
| --- | --- | --- | --- |
| `Alpha-Q-ai-2025/scripts/test_android_adb.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/scripts/test_error_fixing_suite.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/scripts/test_hf_space_ui.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/scripts/test_runner.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/src/App.test.js` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/src/components/q-city/QMoiKernelPanel.integration.test.tsx` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/src/components/q-city/QMoiKernelPanel.test.tsx` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/src/hooks/useQmoiKernel.test.ts` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/api/test_health.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/e2e/test_e2e_placeholder.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/integration/test_ai_integration.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/integration/test_error_fixing_integration.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/integration/test_financial_verification.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/integration/test_qcity_audit_log.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/integration/test_qcity_remote_command.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/integration/test_qcity_status.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/integration/test_session_integration.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/integration/test_whatsapp_verification.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/md/test_md_links.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/security/test_security_placeholder.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/ui/qmoi_ui_autotest.spec.js` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/unit/test_ai_component.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/unit/test_error_fixing.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/unit/test_multi_user_session.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `Alpha-Q-ai-2025/tests/unit/test_qi.py` | `snapshot` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/api.qmoi.chat.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/api.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/api/admin.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/api/auth.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/api/monitoring.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/api/payments.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/api/wallets.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/cache/cache.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/chatbot.chat.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/chatbot.model.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/ci.no-model-selector.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/integration/user-registration.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/memory-backup.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/persona.integration.test.js` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/persona.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/__tests__/qmoi-model.route.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/__tests__/wallet.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/test_android_adb.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/test_error_fixing_suite.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/test_hf_space_ui.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/test_runner.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/App.test.js` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/q-city/QMoiKernelPanel.integration.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/q-city/QMoiKernelPanel.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/hooks/useQmoiKernel.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/api/test_health.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/e2e/test_e2e_placeholder.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/integration/test_ai_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/integration/test_error_fixing_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/integration/test_financial_verification.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/integration/test_qcity_audit_log.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/integration/test_qcity_remote_command.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/integration/test_qcity_status.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/integration/test_session_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/integration/test_whatsapp_verification.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/md/test_md_links.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/security/test_security_placeholder.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/ui/qmoi_ui_autotest.spec.js` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/unit/test_ai_component.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/unit/test_error_fixing.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/unit/test_multi_user_session.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/tests/unit/test_qi.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/App.test.js` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/components/q-city/QMoiKernelPanel.integration.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/components/q-city/QMoiKernelPanel.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/hooks/useQmoiKernel.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/mocks/handlers.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_android_adb.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_attachments.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_control_server_endpoints.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_deals_and_sponsored.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_env_setup.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_error_fixing_suite.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_hf_space_ui.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_pay_flow.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_payments.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_runner.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_stripe_checkout.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_wallets.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/test_webhooks.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/scripts/tests/test_memory_sync.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/App.test.js` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/components/q-city/QMoiKernelPanel.integration.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/components/q-city/QMoiKernelPanel.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/hooks/useQmoiKernel.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/mocks/handlers.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src/App.test.js` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src/components/q-city/QMoiKernelPanel.integration.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src/components/q-city/QMoiKernelPanel.test.tsx` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src/hooks/useQmoiKernel.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/src/mocks/handlers.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/AutoResearcher.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/api/test_health.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/e2e/test_e2e_placeholder.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/handlers.integration.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/adapter-dryrun.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/test_ai_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/test_error_fixing_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/test_financial_verification.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/test_qcity_audit_log.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/test_qcity_remote_command.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/test_qcity_status.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/test_session_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/integration/test_whatsapp_verification.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/md/test_md_links.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/payments/test_adapters.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/qmoi-chat-api.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/scripts/auto_trading.test.js` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/security/test_security_placeholder.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test___init__.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_account_verification.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_adapter_base.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_advanced_architectures.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_advanced_autotest_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_advanced_optimization.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_advanced_training.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_ai_automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_all_cloned_releases.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_api_endpoints_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_app_validator.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_apply_all_enhancements.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_apply_dotslash_fixes.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_apply_safe_link_fixes.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_architectures.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_audit_releases.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_creds.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_deploy.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_enhance_pipeline.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_fix_md.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_fix_release_artifacts.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_fix_workflows.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_lint_fix.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_push_release.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_release_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_auto_update_allmdfilesrefs.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_automate_tasks.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_automation_api.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_automation_helpers.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_autotag_md_with_lion.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_autoupdate_releases.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_aws_route53.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_backup_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_backup_restore.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_backup_state.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_billing_guard.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_binance_adapter.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_biometrics_check.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_build_all_apps.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_captcha_solver.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_check_and_replace_placeholders.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_check_balances.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_check_github_releases.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_check_placeholders.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_check_release_assets.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_check_wallets.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_ci_production_orchestrator.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_cli_build_selector.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_cloud_deploy.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_cloud_deployment.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_cloud_resources_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_cloudflare.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_colab-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_colab_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_collect_build_scripts.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_continuous_testing.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_core_automation_&_evolution.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_create_dns_issues_using_pr.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_create_issues_from_audit.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_create_missing_assets_issues.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_create_pr_and_issues.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_create_release_placeholders.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_currency_convert.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_custom_error_handler.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_dagshub-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_db_migrations.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_deploy.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_device_ownership_detector.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_device_unlock_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_dns_plan_signer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_doc_verifier.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_domain_assigner.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_domain_registry.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_downloadqmoiai.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enable_claude_sonnet.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhance_ai.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced-build.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_automation_&_cloud_features_(2025_01_22).py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_browser.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_credential_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_earning_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_preview.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_qmoi_implementation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_test_runner.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_trading_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhanced_wallet_report.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_enhancers.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_env_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_error_fixer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_error_handler.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_error_tracker.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_error_tracking.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_expand_platform_todos.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_fast_git_commit.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_financial-integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_financial_verification.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_fix_broken_links.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_fix_deployment_issues.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_fix_icon.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_fix_removed_placeholders_batch.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_gen_real_apps.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_all_links.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_allmdrefs.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_app_metadata.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_apps_inventory.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_icon_all.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_issue_drafts_for_removed.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_md_inventory.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_payed_md.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_real_apps.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_release_compliance_report.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_release_manifest.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_revenue_spec.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_rsa_key.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_generate_test_index.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_get_public_ip.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_github_actions_auto_fix.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_github_actions_autofix.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_github_auto_push.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_github_release_sync.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_gmail_notify.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_hf_model_sync.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_hf_sync.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_host_health_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_integration_test_control_server.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_license_checker.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_link_apply_preview.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_link_autoupdater.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_link_cache.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_link_cache_maintenance.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_link_normalization_dryrun.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_link_systems.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_link_validator.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_lion_feature_enhancer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_lion_orchestrator.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_list_md_files.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_make_minimal_deb.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_master_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_merge_queue_metrics.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_metrics_server.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_migrate_memory_to_redis.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_migrate_sqlite_to_postgres.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_monitor_cloud_performance.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_monitor_performance.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_monitoring_dashboard.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_mpesa_adapter.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_netlify.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_network_connectivity_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_nonprod_scanner.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_notification_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_notification_service.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_notify_enhancement.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_notify_on_whatsapp.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_QMOI_autonomous_agent.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_one_command_automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_optimize_cloud_costs.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_optimize_cpu.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_optimize_memory.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_optimize_performance.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_optimize_storage.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_optimizer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_ota_updater.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_package_pwas.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_parallel_executor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_performance_monitoring.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_persist_history.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_placeholder_fixer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_placeholder_scan.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_placeholder_scanner.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_platform_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_production_helper_server.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_propose_workflow_fixes.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_provider_base.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_providers.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_q.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qcity_advanced_installer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qcity_device_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qcity_enhancer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qcity_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qcity_ui_enhancement.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qcity_unlimited_installer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-activity-logger.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-app-releaser.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-app-validator.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-auto-email-download.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-auto-evolution.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-cloud-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-comprehensive-parallel-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-dashboard-enhance.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-dashboard.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-dev-actions.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-download-link-tester.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-enhanced-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-enhanced-biometric-system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-enhanced-controller.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-enhanced-health-checker.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-enhanced-live-status.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-enhanced-master-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-enhanced-notifications.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-enhanced-platform-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-error-handler.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-git-auto.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-git-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-gitlab-ci-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-hands-free.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-hf-sync.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-hf-test.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-huggingface-space-enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-info.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-install-autotest.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-integrity-guardian.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-lint-integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-live-status.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-master-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-master-notifications.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-package-installer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-parallel-platform-enhancer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-parallel-processor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-performance-optimizer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-platform-manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-platform-optimizer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-qcity-automatic.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-qcity-enhanced-automatic.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-qcity-enhanced-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-quick-test.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-real-time-logger.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-real-time-monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-research-engine.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-space-backend.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-start-watch.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-start.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-system-controller.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-ultimate-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-unified-push-enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-unified-push-ultimate.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-unified-push.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-universal-error-fixer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-workflow-fix-count.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi-workflow-fix.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_activity_logger.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_advanced_analytics.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_advanced_automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_ai_api.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_ai_api_simple.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_ai_enhancement_engine.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_app_builder.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_app_installer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_app_delivery.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_app_validation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_docs.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_evolution.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_evolution_enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_evolution_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_fix_enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_setup.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_auto_startup.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_autodev.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_automated_betting_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_automated_device_controller.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_automation_autotest.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_build_api.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_build_ci.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_chat_server.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_cloud_integration_enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_cloud_setup.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_complete_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_comprehensive_test.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_contact_verifier.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_daemon.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_dashboard.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_data_optimization_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_device_agent.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_device_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_earning_daemon.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_earning_enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_employment_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_enhanced_ai.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_enhanced_auto_config.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_enhanced_automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_enhanced_startup.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_error_auto_fix.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_error_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_feature_suggester.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_git_automation.py.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_gitlab_automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_hands_free.py.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_health_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_health_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_health_reporting_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_hf_auto_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_huggingface_setup.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_huggingface_space_enhanced.py.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_integration_master.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_intelligent_scheduler.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_kernel.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_local_server.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_log_analyzer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_master_automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_master_automation_enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_master_wallet_cli.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_memory.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_model_enhancer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_notification_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_own_device_logger.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_parallel_error_fixer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_parallel_processor.py.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_performance_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_permission_fix.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_personality.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_revenue_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_security_automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_security_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_self_evolve.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_self_healing_enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_self_test.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_simple_autotest.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_todos.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_wallet_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_wallet_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qmoi_windows_service.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_qserver-download-tester.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_query_wallet.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_queue_worker.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_queue_worker_integration.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_quick_git_push.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_reconcile_payments.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_register_app_build.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_release_automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_release_helper.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_replace_all_release_assets.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_replace_placeholders.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_replace_release_asset.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_report_scheduler.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_resolve_dependabot_conflict.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_resolve_deployment_conflicts.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_restore_from_gdrive.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_restore_from_s3.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_restore_release_assets.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_revenue_enhancement_config.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_revenue_enhancer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_revenue_tracker.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_run_all_tests.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_run_enhancements.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_run_placeholder_scans.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_run_tests.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_run_unit_tests.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_run_validation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_run_validations.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_run_wallet_tests.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_scan_and_index.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_scan_lion_usage.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_scan_placeholders.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_scan_replace_placeholders.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_scan_workflows.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_search_and_serve_components.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_secret_store.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_security_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_server.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_settle_to_cashon.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_setup.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_setup_qmoi_environment.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_specialized_architectures.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_start_all_monitors.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_start_cloud_services.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_start_monitoring_system.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_start_qmoi_enhanced.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_state_store.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_strip_large_files.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_sync_all_releases.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_sync_cloud_data.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_sync_memory.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_sync_qmoi_downloads.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_sync_to_draft_release.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_system_status_monitor.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_task_queue.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_terms_enforcer.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_android_adb.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_attachments.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_control_server_endpoints.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_deals_and_sponsored.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_env_setup.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_error_fixing_suite.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_hf_space_ui.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_memory_sync.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_pay_flow.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_payments.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_runner.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_stripe_checkout.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_wallets.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_test_webhooks.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_trading_connection_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_universal_memory.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_update_autotest_status.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_update_md_from_state.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_update_md_refs.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_update_model_card.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_update_ngrok_links.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_update_readme.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_update_readme_cli_usage.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_update_readmes.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_upload_builds_to_drive.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_upload_release_assets.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_upload_to_github_release.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_all_credentials.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_and_fix_md.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_apps.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_builds.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_env.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_links_and_downloads.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_md.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_payed_platforms.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_ui_components.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_validate_yml.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_verify_and_finalize_done.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_verify_apps.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_wallet_balance_checker.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_wallet_credential_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_wallet_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_wallets_api.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_wallets_audit.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_watch_error_fixing.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_whatsapp-business-automation.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_whatsapp_verification.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_wifi_manager.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_workspace_audit.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/test_writing_assistant.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/testnet_adapter.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/ui/qmoi_ui_autotest.spec.js` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/unit/test_ai_component.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/unit/test_error_fixing.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/unit/test_multi_user_session.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/unit/test_qi.py` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `qmoi-enhanced-history-14/tests/wallet.test.ts` | `historical_archive` | `unmapped` | `historical_reference_not_active_coverage` |
| `tests/test_alpha_q_ai_2025_security.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_command_inventory.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_control_plane.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_cross_repo_sync.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_enhanced_tracking_and_workflows.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_merge_inventory.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_QMOI_autonomous_agent.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_QMOI_enhanced_features.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_QMOI_runtime.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_production_trading_autopilot.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_qmoi_credentials.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_qmoi_release_autofix.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |
| `tests/test_runbook_audit.py` | `active_checkout` | `unmapped` | `discovered_not_coverage_proof` |

### App/platform contract inventory

| Platform | App | Registered feature count | Implementation evidence | Test mapping |
| --- | --- | ---: | --- | --- |
| `windows` | `qmoiaiui` | 24 | `registry_only_not_implementation_proof` | `unmapped` |
| `windows` | `qcity` | 29 | `registry_only_not_implementation_proof` | `unmapped` |
| `windows` | `qmoi-space` | 15 | `registry_only_not_implementation_proof` | `unmapped` |
| `windows` | `qalpha` | 15 | `registry_only_not_implementation_proof` | `unmapped` |
| `macos` | `qmoiaiui` | 17 | `registry_only_not_implementation_proof` | `unmapped` |
| `macos` | `qcity` | 20 | `registry_only_not_implementation_proof` | `unmapped` |
| `macos` | `qmoi-space` | 14 | `registry_only_not_implementation_proof` | `unmapped` |
| `macos` | `qalpha` | 14 | `registry_only_not_implementation_proof` | `unmapped` |
| `linux` | `qmoiaiui` | 16 | `registry_only_not_implementation_proof` | `unmapped` |
| `linux` | `qcity` | 19 | `registry_only_not_implementation_proof` | `unmapped` |
| `linux` | `qmoi-space` | 14 | `registry_only_not_implementation_proof` | `unmapped` |
| `linux` | `qalpha` | 14 | `registry_only_not_implementation_proof` | `unmapped` |
| `ios` | `qmoiaiui` | 16 | `registry_only_not_implementation_proof` | `unmapped` |
| `ios` | `qcity` | 21 | `registry_only_not_implementation_proof` | `unmapped` |
| `ios` | `qmoi-space` | 16 | `registry_only_not_implementation_proof` | `unmapped` |
| `ios` | `qalpha` | 16 | `registry_only_not_implementation_proof` | `unmapped` |
| `android` | `qmoiaiui` | 16 | `registry_only_not_implementation_proof` | `unmapped` |
| `android` | `qcity` | 19 | `registry_only_not_implementation_proof` | `unmapped` |
| `android` | `qmoi-space` | 14 | `registry_only_not_implementation_proof` | `unmapped` |
| `android` | `qalpha` | 14 | `registry_only_not_implementation_proof` | `unmapped` |
| `web` | `qmoiaiui` | 14 | `registry_only_not_implementation_proof` | `unmapped` |
| `web` | `qcity` | 19 | `registry_only_not_implementation_proof` | `unmapped` |
| `web` | `qmoi-space` | 14 | `registry_only_not_implementation_proof` | `unmapped` |
| `web` | `qalpha` | 14 | `registry_only_not_implementation_proof` | `unmapped` |

### Trading surface candidate inventory

Materialized source paths are candidates, not proof of implementation, authorization, or test coverage. Complete branch/PR history is a separate remote audit gate.

- Candidate files: `549`; materialized scope counts: `{"active_checkout": 16, "historical_archive": 432, "snapshot": 101}`.
- Candidate role counts: `{"backend_api_or_adapter": 175, "documentation": 43, "frontend_ui": 81, "runtime_or_integration_candidate": 224, "test": 39}`.
- Venue mentions: `{"binance": 27, "bitget": 62, "bybit": 2, "cashon": 101, "coinbase": 10, "kraken": 10, "megavault": 34, "okx": 2, "paypal": 39}`.
- Local refs discovered: `37`; this refresh does not scan every ref tree or intermediate commit. Remote completeness: `not_verified`.
- Machine-readable path, size, hash, source scope, role, and venue evidence: `QMOItracks/trading_surface_inventory.json`.
- Coverage state: `discovered_unmapped`; platform execution, credential validity, balances, provider webhook registration, and live-order readiness are not verified by path discovery.
### Credential references and provider verification

This inventory scans source references only. It does not read environment values, `.env` files, private keys, credential vaults, provider accounts, or balances.

- Credential variable/reference names: `1130`; provider groups: `{"binance": 16, "bitget": 118, "cashon": 9, "github": 100, "huggingface": 10, "megavault": 11, "paypal": 22, "pesapal": 10, "stripe": 3, "unmapped_provider": 831}`.
- Consumer path and line-number metadata: `QMOItracks/credential_reference_inventory.json`; values stored/emitted: `false`.
- Credential manager supports encrypted metadata storage generically; only Bitget has a provider-specific read-only verifier in the active manager. Latest Bitget evidence is not a successful verification; other provider credentials remain unverified.
- Runtime presence, credential validity, scope, expiry, account ownership, balances, and live-trading permission are not inferred from a variable name.

| Trading-related candidate path | Source scope | Roles | Venue mentions | Mapping status |
| --- | --- | --- | --- | --- |
| `Alpha-Q-ai-2025/CASHON.md` | `snapshot` | `documentation` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/CASHONTRADINGREADME.md` | `snapshot` | `documentation` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/MEGAVAULT.md` | `snapshot` | `documentation` | `megavault` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/QMOITRADER.md` | `snapshot` | `documentation` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/TRADINGREADME.md` | `snapshot` | `documentation` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/ai-health/route.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/cashon/balance/route.ts` | `snapshot` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/cashon/deposit/route.ts` | `snapshot` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/cashon/route.ts` | `snapshot` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/cashon/signals/route.ts` | `snapshot` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/cashon/start-trading/route.ts` | `snapshot` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/cashon/stop-trading/route.ts` | `snapshot` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/cashon/trading-status/route.ts` | `snapshot` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/earning/route.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/employment/megavault/route.ts` | `snapshot` | `backend_api_or_adapter` | `megavault` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/employment/payment/route.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/qi-trading.ts` | `snapshot` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/qi-trading/route.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/qmoi-database/route.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/qmoi-model.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/trading/status/route.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/app/api/wallet.ts` | `snapshot` | `backend_api_or_adapter` | `binance, bitget, cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/backend/trading-engine.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/bitget-trader.py` | `snapshot` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/AppManager.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/CashonTradingPanel.tsx` | `snapshot` | `frontend_ui` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/DeviceSettingsPanel.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/HelpGuide.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/LeahWallet.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/LeahWalletPanel.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/QI.tsx` | `snapshot` | `frontend_ui` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/QiSpaces.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/QmoiRevenueDashboard.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/TradingPanel.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/auth/BiometricAuth.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/enhanced-system-dashboard.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/components/q-city/EmploymentDashboard.tsx` | `snapshot` | `frontend_ui` | `megavault` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/earnvault/ui/EnhancedTradingPanel.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/earnvault/ui/FloatingAQ.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/hooks/useBitgetTrader.ts` | `snapshot` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/hooks/useTrading.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/hooks/useTradingAutomation.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/lib/cashon-wallet.ts` | `snapshot` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/lib/ml-trading-strategy.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/lib/qmoi-trader.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/lib/trading-config.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/lib/trading-service.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/routes/api/qcity/trading/config.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/routes/api/qcity/trading/positions.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/auto-git-update.js` | `snapshot` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/auto_lint_fix.py` | `snapshot` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/auto_trading.js` | `snapshot` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/db_migrations.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/earning/enhanced_earning_system.py` | `snapshot` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/enhanced_test_runner.py` | `snapshot` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/monitoring/api_endpoints_monitor.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/monitoring/start_all_monitors.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/monitoring/system_status_monitor.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/network/network_connectivity_manager.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qcity_manager.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi-enhanced-auto-projects.js` | `snapshot` | `runtime_or_integration_candidate` | `cashon, paypal` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi-enhanced-biometric-system.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi-enhanced-controller.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi-environment-setup.js` | `snapshot` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi-revenue-enforcer.js` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_advanced_analytics.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_ai_enhancement_engine.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_auto_docs.py` | `snapshot` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_auto_evolution.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_auto_evolution_system.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_automated_betting_system.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_complete_system.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_data_optimization_system.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_enhanced_ai.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_hf_auto_manager.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_huggingface_setup.py` | `snapshot` | `runtime_or_integration_candidate` | `binance, coinbase, kraken` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_integration_master.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_intelligent_scheduler.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_own_device_logger.py` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/qmoi_payment_fix.js` | `snapshot` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/services/qcity_service.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/services/trading_service.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/setup_qmoi_environment.py` | `snapshot` | `runtime_or_integration_candidate` | `binance, coinbase, kraken` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/scripts/trading/enhanced_trading_system.py` | `snapshot` | `runtime_or_integration_candidate` | `binance, cashon` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/auth/AuthManager.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/components/AITradingRules.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/components/AssetOverview.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/components/TradingHistory.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/components/TradingStatus.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/components/q-city/QFileManager.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/components/q-city/WalletManager.tsx` | `snapshot` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/config/assets.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/config/bitget.ts` | `snapshot` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/config/trading.ts` | `snapshot` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/config/wallet.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/services/AIRequestRouter.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/services/AppManagementService.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/services/VoiceRecognitionService.ts` | `snapshot` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/services/WhatsAppService.ts` | `snapshot` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/src/types/trading.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Alpha-Q-ai-2025/types/trading.ts` | `snapshot` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `Qtrade.md` | `active_checkout` | `documentation` | `unspecified` | `discovered_unmapped` |
| `TRADINGREADME.md` | `active_checkout` | `documentation` | `unspecified` | `discovered_unmapped` |
| `bankandbankaccounts.md` | `active_checkout` | `documentation` | `unspecified` | `discovered_unmapped` |
| `QMOItracks/bank_automation_status.json` | `active_checkout` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `QMOItracks/trading_surface_inventory.json` | `active_checkout` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `projectsandautoprojects.md` | `active_checkout` | `documentation` | `unspecified` | `discovered_unmapped` |
| `projectsandautoprojectsenhanced.md` | `active_checkout` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/.github/workflows/wallet-tests.yml` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/.qmoi_state/wallets.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/ALLWALLETSQVS.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/CASHON.md` | `historical_archive` | `documentation` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/CASHONTRADINGREADME.md` | `historical_archive` | `documentation` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/FINANCE_CREDENTIALS.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/LEAHWALLET.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/MEGAVAULT.md` | `historical_archive` | `documentation` | `megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/PAYMENTS.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/QMOIFINANCEENGINES.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/QMOITRADER.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/QMOI_WALLET_FINANCIAL_SYSTEMS.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/TRADINGREADME.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/Trade.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/__tests__/api/admin.test.ts` | `historical_archive` | `backend_api_or_adapter, test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/__tests__/api/payments.test.ts` | `historical_archive` | `backend_api_or_adapter, test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/__tests__/api/wallets.test.ts` | `historical_archive` | `backend_api_or_adapter, test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/CASHON.md` | `historical_archive` | `documentation` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/CASHONTRADINGREADME.md` | `historical_archive` | `documentation` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/MEGAVAULT.md` | `historical_archive` | `documentation` | `megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/QMOITRADER.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/TRADINGREADME.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/__tests__/wallet.test.ts` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/ai-health/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/cashon/balance/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/cashon/deposit/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/cashon/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/cashon/signals/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/cashon/start-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/cashon/stop-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/cashon/trading-status/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/earning/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/employment/megavault/route.ts` | `historical_archive` | `backend_api_or_adapter` | `megavault, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/employment/payment/route.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/qi-trading.ts` | `historical_archive` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/qi-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/qmoi-database/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/qmoi-model.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/trading/status/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/_app_archived/api/wallet.ts` | `historical_archive` | `backend_api_or_adapter` | `binance, bitget, cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/backend/trading-engine.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/bitget-trader.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/AppManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/CashonTradingPanel.tsx` | `historical_archive` | `frontend_ui` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/DeviceSettingsPanel.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/HelpGuide.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/LeahWallet.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/LeahWalletPanel.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/QI.tsx` | `historical_archive` | `frontend_ui` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/QiSpaces.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/QmoiRevenueDashboard.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/TradingPanel.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/auth/BiometricAuth.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/enhanced-system-dashboard.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/q-city/EmploymentDashboard.tsx` | `historical_archive` | `frontend_ui` | `megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/components/q-city/index.ts` | `historical_archive` | `frontend_ui` | `megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/earnvault/ui/EnhancedTradingPanel.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/earnvault/ui/FloatingAQ.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/hooks/useBitgetTrader.ts` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/hooks/useTrading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/hooks/useTradingAutomation.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/routes/api/qcity/trading/config.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/routes/api/qcity/trading/positions.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/auto-git-update.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/auto_lint_fix.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/auto_trading.js` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/db_migrations.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/monitoring/api_endpoints_monitor.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/monitoring/start_all_monitors.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/monitoring/system_status_monitor.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/network/network_connectivity_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qcity_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi-enhanced-auto-projects.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi-enhanced-controller.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi-enhanced-doc-verifier.js` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi-environment-setup.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi-revenue-enforcer.js` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi-space-backend.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_advanced_analytics.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_auto_docs.py` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_auto_evolution.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_auto_evolution_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_automated_betting_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_complete_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_data_optimization_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_enhanced_ai.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_hf_auto_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_huggingface_setup.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, coinbase, kraken` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_integration_master.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_intelligent_scheduler.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_own_device_logger.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_payment_fix.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/qmoi_secret_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/services/qcity_service.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/services/trading_service.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/setup_qmoi_environment.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, coinbase, kraken` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/scripts/trading/enhanced_trading_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/auth/AuthManager.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/AITradingRules.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/AssetOverview.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/TradingHistory.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/TradingStatus.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/q-city/QFileManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/q-city/WalletManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/components/release-notes.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/config/assets.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/config/bitget.ts` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/config/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/config/wallet.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/services/AIRequestRouter.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/services/AppManagementService.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/services/VoiceRecognitionService.ts` | `historical_archive` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/services/WhatsAppService.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/src/types/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/_archive_qmoi-enhanced/types/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/admin/dashboard/route.ts` | `historical_archive` | `backend_api_or_adapter, frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/admin/users/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/ai-health/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/analytics/wallets/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/auth/register/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/cashon/balance/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/cashon/deposit/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/cashon/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/cashon/signals/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/cashon/start-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/cashon/stop-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/cashon/trading-status/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/earning/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/employment/megavault/route.ts` | `historical_archive` | `backend_api_or_adapter` | `megavault, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/employment/payment/route.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/metrics/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/mpesa/callback/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/payments/initiate/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/qi-trading.ts` | `historical_archive` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/qi-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/qmoi-model.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/trading/status/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/wallet.ts` | `historical_archive` | `backend_api_or_adapter` | `binance, bitget, cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/wallets/[walletId]/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/wallets/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/api/webhooks/payments/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app.backup.20260121144720/components/wallet/WalletList.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/admin/dashboard/route.ts` | `historical_archive` | `backend_api_or_adapter, frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/admin/financial/summary/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/admin/users/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/ai-health/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/analytics/wallets/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/auth/register/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/cashon/balance/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/cashon/deposit/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/cashon/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/cashon/signals/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/cashon/start-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/cashon/stop-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/cashon/trading-status/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/earning/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/employment/megavault/route.ts` | `historical_archive` | `backend_api_or_adapter` | `megavault, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/employment/payment/route.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/financial/transactions/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/metrics/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/payments/initiate/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/qi-trading.ts` | `historical_archive` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/qi-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/qmoi-earning-enhanced/route.ts` | `historical_archive` | `backend_api_or_adapter` | `bitget, coinbase, kraken` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/qmoi-model.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/qmoi/backup/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/qmoi/chat-enhanced/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/qmoi/memory/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/qmoi/research/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/trading/status/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/wallet.ts` | `historical_archive` | `backend_api_or_adapter` | `binance, bitget, cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/wallets/[walletId]/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/wallets/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/api/webhooks/payments/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/app/components/wallet/WalletList.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backend/trading-engine.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/admin/dashboard/route.ts` | `historical_archive` | `backend_api_or_adapter, frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/admin/users/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/ai-health/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/analytics/wallets/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/auth/register/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/cashon/balance/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/cashon/deposit/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/cashon/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/cashon/signals/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/cashon/start-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/cashon/stop-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/cashon/trading-status/route.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/earning/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/employment/megavault/route.ts` | `historical_archive` | `backend_api_or_adapter` | `megavault, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/employment/payment/route.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/metrics/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/mpesa/callback/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/payments/initiate/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/qi-trading.ts` | `historical_archive` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/qi-trading/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/qmoi-model.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/trading/status/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/wallet.ts` | `historical_archive` | `backend_api_or_adapter` | `binance, bitget, cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/wallets/[walletId]/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/wallets/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/api/webhooks/payments/route.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/app.backup.20260121144720/components/wallet/WalletList.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/components/AssetOverview.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/components/TradingHistory.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/components/TradingStatus.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/components/q-city/QFileManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/components/q-city/WalletManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/config/bitget.ts` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/config/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/config/wallet.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/services/AIRequestRouter.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/services/AppManagementService.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/services/VoiceRecognitionService.ts` | `historical_archive` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/services/WhatsAppService.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/types/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/backups/src.backup.20260121144720/wallet.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/bitget-trader.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/bitget.md` | `historical_archive` | `documentation` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/docs/WALLET_RUNBOOK.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/docs/WALLET_SECURITY_PLAYBOOK.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/docs/wallets_report.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/earnvault/ui/EnhancedTradingPanel.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/earnvault/ui/FloatingAQ.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/hooks/useBitgetTrader.ts` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/hooks/useTrading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/hooks/useTradingAutomation.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/payments/provider_stub.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/payments/reconciliation.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/payments/stripe_adapter.py` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/payments/webhook_processor.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/prisma/generated/prisma/models/Wallet.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/pwa_apps/deals/js/stripe-payment.js` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/routes/api/qcity/trading/config.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/routes/api/qcity/trading/positions.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/.wallet_balances.json` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/auto-git-update.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/auto_lint_fix.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/auto_trading.js` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/cashon_data/balances.json` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/check_balances.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/daemon/qmoi_daemon.py` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/db_migrations.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/domain_registry.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, coinbase, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/enhanced_credential_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, megavault, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/enhanced_wallet_report.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/finance/README.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/finance/settle_to_cashon.py` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/fix_removed_placeholders_batch.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/generate_issue_drafts_for_removed.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/generate_revenue_spec.py` | `historical_archive` | `runtime_or_integration_candidate` | `cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/link_cache.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/migrate_sqlite_to_postgres.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/monitoring/api_endpoints_monitor.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/monitoring/start_all_monitors.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/monitoring/system_status_monitor.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/network/network_connectivity_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/QMOI_autonomous_agent.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, bitget, cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/parallel_executor.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qcity_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi-enhanced-auto-projects.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi-enhanced-controller.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi-environment-setup.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi-revenue-enforcer.js` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi-space-backend.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_advanced_analytics.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_auto_docs.py` | `historical_archive` | `runtime_or_integration_candidate` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_auto_evolution.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_auto_evolution_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_automated_betting_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_chat_server.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_complete_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_data_optimization_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_enhanced_ai.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_enhanced_auto_config.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_hf_auto_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_huggingface_setup.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, coinbase, kraken` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_integration_master.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_intelligent_scheduler.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_master_wallet_cli.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_own_device_logger.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_payment_fix.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_wallet_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/qmoi_wallet_monitor.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/reconcile_payments.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/report_scheduler.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/revenue_enhancement_config.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, bitget, cashon, coinbase, kraken, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/revenue_enhancer.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/revenue_tracker.py` | `historical_archive` | `runtime_or_integration_candidate` | `megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/run-migrations.js` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/services/qcity_service.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/services/trading_service.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/setup_qmoi_environment.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, coinbase, kraken` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/task_queue.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/test_payments.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/test_stripe_checkout.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/test_wallets.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/trading/enhanced_trading_system.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/trading_connection_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/update_md_refs.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/validate-trading-env.js` | `historical_archive` | `runtime_or_integration_candidate` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/validate_all_credentials.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/validate_payment_credentials.js` | `historical_archive` | `runtime_or_integration_candidate` | `cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallet_balance_checker.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallet_credential_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallet_manager.py` | `historical_archive` | `runtime_or_integration_candidate` | `bitget, cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/PRODUCTION_RUNBOOK.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/README.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/adapter_base.py` | `historical_archive` | `backend_api_or_adapter` | `binance, cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/adapters/binance_adapter.py` | `historical_archive` | `backend_api_or_adapter` | `binance` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/adapters/mpesa_adapter.py` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/backup_state.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/check_wallets.py` | `historical_archive` | `runtime_or_integration_candidate` | `cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/currency_convert.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/persist_history.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/query_wallet.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/run_wallet_tests.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/state_store.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets/wallets_api.py` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/scripts/wallets_audit.py` | `historical_archive` | `runtime_or_integration_candidate` | `binance, cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/adapters/payments/PayPal.ts` | `historical_archive` | `backend_api_or_adapter` | `cashon, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/adapters/payments/stripe.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/adapters/payments/utils.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/adapters/payments/webhooks.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/data/payments_idempotency.json` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/payments/__init__.py` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/payments/sandbox_adapter.py` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/payments/stripe_adapter.py` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/services/walletManager.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/components/AssetOverview.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/components/TradingHistory.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/components/TradingStatus.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/components/q-city/QFileManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/components/q-city/WalletManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/config/bitget.ts` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/config/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/config/wallet.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/services/AIRequestRouter.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/services/AppManagementService.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/services/WhatsAppService.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/types/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src.backup.20260121144720/wallet.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/auth/AuthManager.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/AppManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/AssetOverview.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/CashonTradingPanel.tsx` | `historical_archive` | `frontend_ui` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/DeviceSettingsPanel.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/HelpGuide.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/LeahWallet.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/LeahWalletPanel.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/QMOIDashboard.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/QmoiRevenueDashboard.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/TradingHistory.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/TradingPanel.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/TradingStatus.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/_automerge/QI.tsx` | `historical_archive` | `frontend_ui` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/_automerge/QiSpaces.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/auth/BiometricAuth.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/enhanced-system-dashboard.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/q-city/EmploymentDashboard.tsx` | `historical_archive` | `frontend_ui` | `megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/q-city/QFileManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/components/q-city/WalletManager.tsx` | `historical_archive` | `frontend_ui` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/config/assets.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/config/bitget.ts` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/config/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/config/wallet.ts` | `historical_archive` | `runtime_or_integration_candidate` | `binance` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/hooks/useQMOIChat.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/mocks/server.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/services/AIRequestRouter.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/services/AppManagementService.ts` | `historical_archive` | `backend_api_or_adapter` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/services/VoiceRecognitionService.ts` | `historical_archive` | `backend_api_or_adapter` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/services/WhatsAppService.ts` | `historical_archive` | `backend_api_or_adapter` | `paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/types/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/src/wallet.ts` | `historical_archive` | `runtime_or_integration_candidate` | `cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/integration/adapter-dryrun.test.ts` | `historical_archive` | `backend_api_or_adapter, test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/payments/test_adapters.py` | `historical_archive` | `backend_api_or_adapter, test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/scripts/auto_trading.test.js` | `historical_archive` | `test` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_adapter_base.py` | `historical_archive` | `backend_api_or_adapter, test` | `cashon, megavault` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_binance_adapter.py` | `historical_archive` | `backend_api_or_adapter, test` | `binance` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_check_balances.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_check_wallets.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_currency_convert.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_enhanced_trading_system.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_enhanced_wallet_report.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_integration.py` | `historical_archive` | `test` | `bitget` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_QMOI_autonomous_agent.py` | `historical_archive` | `test` | `binance, bitget, paypal` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_qmoi_master_wallet_cli.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_qmoi_wallet_manager.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_qmoi_wallet_monitor.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_query_wallet.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_reconcile_payments.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_run_wallet_tests.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_settle_to_cashon.py` | `historical_archive` | `test` | `cashon` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_test_payments.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_test_wallets.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_trading_connection_manager.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_wallet_balance_checker.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_wallet_credential_manager.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_wallet_manager.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_wallets_api.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/test_wallets_audit.py` | `historical_archive` | `test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/testnet_adapter.test.ts` | `historical_archive` | `backend_api_or_adapter, test` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tests/wallet.test.ts` | `historical_archive` | `test` | `binance` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/0482_ALLWALLETSQVS.md.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/0596_hooks_useTrading.ts.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/0598_lib_trading-config.ts.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/0930_qmoi-enhanced_hooks_useTrading.ts.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/1058_scripts_validate_payment_credentials.js.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/1060_scripts_wallets_currency_convert.py.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/1061_scripts_wallets_audit.py.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/1063_services_adapters_payments_utils.ts.md` | `historical_archive` | `backend_api_or_adapter, documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/1064_services_payments_sandbox_adapter.py.md` | `historical_archive` | `backend_api_or_adapter, documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tools/issue_drafts/14_qmoi-enhanced_app_api_qi-trading_route_ts.md` | `historical_archive` | `documentation` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1766522820.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1766523878.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1766523929.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1766524081.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1766649218.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784844860.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784847619.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784847866.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784848069.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784849558.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784849639.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784850002.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784850083.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784850168.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1784850204.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1785024999.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1785025736.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/tracks/payments_1785025918.json` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `qmoi-enhanced-history-14/types/trading.ts` | `historical_archive` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `scripts/autonomous_completion_engine.py` | `active_checkout` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `scripts/QMOI_autonomous_agent.py` | `active_checkout` | `runtime_or_integration_candidate` | `binance, bitget, bybit, cashon, coinbase, kraken, megavault, okx, paypal` | `discovered_unmapped` |
| `scripts/q_version_manager.py` | `active_checkout` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `scripts/qmoi_credentials.py` | `active_checkout` | `runtime_or_integration_candidate` | `bitget` | `discovered_unmapped` |
| `scripts/realtime_workflow_monitor.py` | `active_checkout` | `runtime_or_integration_candidate` | `unspecified` | `discovered_unmapped` |
| `scripts/trading/production_trading_autopilot.py` | `active_checkout` | `runtime_or_integration_candidate` | `binance, bitget, cashon` | `discovered_unmapped` |
| `tests/test_QMOI_autonomous_agent.py` | `active_checkout` | `test` | `binance, bitget, cashon, megavault` | `discovered_unmapped` |
| `tests/test_production_trading_autopilot.py` | `active_checkout` | `test` | `binance, bitget, bybit, cashon, kraken, okx` | `discovered_unmapped` |
| `tests/test_qmoi_credentials.py` | `active_checkout` | `test` | `bitget` | `discovered_unmapped` |

### Credential references and provider verification

This inventory scans source references only. It does not read environment values, `.env` files, private keys, credential vaults, provider accounts, or balances.

- Credential variable/reference names: `1130`; provider groups: `{"binance": 16, "bitget": 118, "cashon": 9, "github": 100, "huggingface": 10, "megavault": 11, "paypal": 22, "pesapal": 10, "stripe": 3, "unmapped_provider": 831}`.
- Consumer path and line-number metadata: `QMOItracks/credential_reference_inventory.json`; values stored/emitted: `false`.
- Credential manager supports encrypted metadata storage generically; only Bitget has a provider-specific read-only verifier in the active manager. Latest Bitget evidence is not a successful verification; other provider credentials remain unverified.
- Runtime presence, credential validity, scope, expiry, account ownership, balances, and live-trading permission are not inferred from a variable name.

### Required per-feature evidence

Every UI/API/backend feature must have a stable feature ID, owning repository/ref, implementation paths, route/API and authorization boundary where applicable, accessibility/state expectations, positive and negative/boundary tests, hook/webhook tests when event-driven, artifact/result hashes, and a terminal exact-SHA validation record. Missing links stay `unmapped`, `blocked`, or `needs_review`; never infer coverage from a nearby test filename.

### Styles and universals test/hook mapping: `QMOItracks/feature_test_hook_coverage.json`

Registered feature count: `404`; test mappings: `0`; reviewed hook applicability: `0/404`; status: `NEEDS_FEATURE_TEST_HOOK_MAPPING`.
Styles/universals replacement plan: `QMOItracks/style_universal_replacement_inventory.json`; `1444` style files, `1170` universal/access files, `659` directories; candidates require review and tests, and replacements are not authorized by discovery.
<!-- END QMOI MANAGED: active-test-feature-coverage -->
