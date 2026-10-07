<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOIAUTODEVDOCTESTS.MD

## QMOI Automated Developer & Fixing System: Test Plan & Documentation

### Overview

This document describes the automated and manual testing strategy for the QMOI self-healing, always-on fixing system. It ensures that all critical fixing subsystems are tested, including those requiring manual intervention or advanced reasoning.

---

## 1. Test Types

- **Automated Error Simulation:**
  - Syntax errors
  - Runtime errors
  - Missing/corrupted files
  - Permission issues
  - Logic/semantic errors
  - Network/API failures
- **Manual/Reasoning-Based Fixes:**
  - Complex logic bugs
  - Ambiguous or context-dependent errors
  - Errors requiring user input or decision

## 2. Test Automation

- All critical fixing subsystems are covered by automated tests.
- Tests are run before any fix is attempted ("pre-fix health check").
- Failures in the fixing system itself trigger notifications and self-repair attempts.

## 3. Manual Intervention & Reasoning

- For errors that cannot be auto-fixed, QMOI prompts for manual input or advanced reasoning.
- These cases are logged and tracked for accountability.

## 4. Reporting & Accountability

- All test results are logged and synced to the cloud.
- Fixes, attempted fixes, and notifications are tracked and queryable from all interfaces.
- Test results are visible in the dashboard, chat interfaces, and GitHub Actions.

## 5. Extensibility

- New error types and fixing strategies can be added by extending the test suite and documentation.
- Contributions and improvements are encouraged.

## 6. Enhanced Resilience & Automation (2025-06-11)

- **Fallback:** If the Node.js doc verifier fails, the Python verifier is run automatically.
- **Error Resilience:** Simulates permission errors, corrupted files, and missing directories to ensure the verifier never fails for doc issues.
- **Persistent Logging:** All actions, errors, and auto-fixes are logged in JSON and synced to the cloud.
- **Notification Triggers:** If verification or fixes fail, notifications are sent via email, Slack, or WhatsApp.
- **.md File Update Automation:** All .md files are updated with verification/fix metadata and checked for up-to-date status after every run.
- **CI/CD Integration:** Both verifiers are run in CI, and logs/reports are uploaded as artifacts. The workflow never fails for doc issues, only for true system errors.

---

### See also: QMOIAVATAR.md, QMOI-ENHANCED-README.md, AUTOGIT.md, MONITORING.md

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/QMOIAUTODEVDOCTESTS.MD",
"validated_at": "2025-10-26T20:51:24.731291Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOIAUTODEVDOCTESTS.MD"
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
