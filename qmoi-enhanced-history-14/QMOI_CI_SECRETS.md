# QMOI CI Secrets and Keystore Setup

This document explains which GitHub Actions secrets are required for the Android CI workflow and how to add them in your repository settings.

Required secrets (Repository -> Settings -> Secrets -> Actions):

- `KEYSTORE_BASE64` : Base64-encoded keystore file (JKS). Encode locally with:

```bash
base64 -w0 my-release-keystore.jks > keystore.b64
# then copy the content and paste into GitHub secret KEYSTORE_BASE64
```

- `KEYSTORE_PASSWORD` : Keystore password (string)
- `KEYSTORE_ALIAS` : Key alias within the keystore (string)
- `KEY_PASSWORD` : (optional) key password if different from keystore password

Optional secrets:

- `FIREBASE_TOKEN` : for distribution to Firebase App Distribution
- `PLAY_STORE_JSON` : Service account JSON for Google Play uploads (store in Secrets and mount as file in workflow)

How the workflow uses the secrets:

- `KEYSTORE_BASE64` is decoded in the workflow into `mobile/android/app/keystore.jks`
- `keystore.properties` is created dynamically in the repo for Gradle signing using the provided passwords and alias
- Do NOT commit the keystore or passwords to the repo; always use secrets

Security notes:

- Rotate keystore passwords and service account credentials regularly
- Limit repository master access to trusted users
- Use organization-level secrets for multi-repo workflows if needed

_Last updated: 2025-11-24_

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
