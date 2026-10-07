# v1.2.5 Release Publish Report

Status: PUBLISHED ✅

Release: https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5
Release ID: 262642597
Published at: 2025-11-15T07:52:09Z

Uploaded assets (10):

- SHA256SUMS.txt
- master.zip
- app-release.apk
- deals.zip
- q-alpha.zip
- qmoi-ai.zip
- qmoi-release.exe
- qmoi-release.ipa
- qmoi-space.zip
- qmoi.zip

Verification:

- Downloaded `SHA256SUMS.txt` from the release and matched it against the local `v1.2.5_release/SHA256SUMS.txt` (no differences found).

Local artifact directory: `/workspaces/qmoi-enhanced/v1.2.5_release/`

Next recommended actions:

1. (Optional) Add Android keystore secrets to GitHub Secrets for fully automated signed builds in CI:
   - `ANDROID_KEYSTORE_BASE64`
   - `ANDROID_KEYSTORE_PASSWORD`
   - `ANDROID_KEY_ALIAS`
   - `ANDROID_KEY_PASSWORD`
2. (Optional) Add iOS signing credentials to enable automated iOS builds in CI (requires macOS runners).
3. Manually test-install `app-release.apk` and `qmoi-release.ipa` on devices/emulators.
4. Test PWAs by serving one of the created zips locally and checking install/offline behavior.

Audit notes:

- All uploaded artifacts have `state: uploaded` and `digest` SHA-256 values in the release metadata.
- Android APK content type: `application/vnd.android.package-archive`.

Done by automation: uploaded artifacts, created release, verified checksums.

Report generated: `/workspaces/qmoi-enhanced/RELEASE_v1.2.5_PUBLISH_REPORT.md`

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
