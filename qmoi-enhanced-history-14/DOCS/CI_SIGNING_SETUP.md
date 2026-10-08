**CI Signing Setup**: Guidance for storing signing credentials in GitHub Actions secrets and using them in workflows.

Android (Keystore):

- Secrets to create in GitHub repo Settings → Secrets → Actions:
  - `ANDROID_KEYSTORE_BASE64` : Base64-encoded keystore file (run: `base64 -w0 my.keystore > my.keystore.b64`)
  - `ANDROID_KEYSTORE_PASSWORD` : keystore password
  - `ANDROID_KEY_ALIAS` : key alias
  - `ANDROID_KEY_PASSWORD` : key password

Example usage in workflow:

```
- name: Restore keystore
  run: echo "$ANDROID_KEYSTORE_BASE64" | base64 -d > $GITHUB_WORKSPACE/keystore.jks
  env:
    ANDROID_KEYSTORE_BASE64: ${{ secrets.ANDROID_KEYSTORE_BASE64 }}

- name: Build Android
  run: ./gradlew assembleRelease -Pkeystore=$GITHUB_WORKSPACE/keystore.jks -PkeyAlias=${{ secrets.ANDROID_KEY_ALIAS }} -PkeyPassword=${{ secrets.ANDROID_KEY_PASSWORD }}
```

iOS (Code signing):

- Secrets to create:
  - `IOS_CERT_BASE64` : Base64-encoded p12 certificate (exported from Keychain)
  - `IOS_CERT_PASSWORD` : p12 password
  - `IOS_PROVISIONING_PROFILE_BASE64` : Base64-encoded provisioning profile
  - `MATCH_PASSWORD` or relevant credentials if using fastlane match

Example usage (macOS runner):

```
- name: Restore iOS cert
  run: |
    echo "$IOS_CERT_BASE64" | base64 -d > cert.p12
    security create-keychain -p travis build.keychain
    security import cert.p12 -k build.keychain -P "$IOS_CERT_PASSWORD" -T /usr/bin/codesign

- name: Restore provisioning profile
  run: echo "$IOS_PROVISIONING_PROFILE_BASE64" | base64 -d > profile.mobileprovision

- name: Build iOS
  run: xcodebuild -workspace MyApp.xcworkspace -scheme MyScheme -configuration Release ...
```

General notes:

- Always store binary secrets as base64 strings to avoid line-ending issues.
- Limit repository collaborator access if secrets are present and rotate keys regularly.
- For production releases prefer a dedicated signing key with limited scope and rotate periodically.

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
