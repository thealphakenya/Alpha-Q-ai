# GitHub Actions Secrets Setup

To enable production-grade signed builds in CI, configure these secrets in your GitHub repository:

**Location**: Settings → Secrets and variables → Actions → New repository secret

## Android Signing Secrets

1. **ANDROID_KEYSTORE_BASE64** (Required for signed APK)
   - Base64-encoded Android keystore file (.jks or .keystore)
   - How to generate:
     ```bash
     base64 -w0 /path/to/keystore.jks > keystore.b64
     # Copy the entire output to clipboard, paste into secret value
     ```

2. **ANDROID_KEYSTORE_PASSWORD**
   - Password for the keystore file

3. **ANDROID_KEY_ALIAS**
   - Alias of the key inside the keystore (e.g., "qmoi-release-key")
   - List aliases: `keytool -list -v -keystore keystore.jks`

4. **ANDROID_KEY_PASSWORD**
   - Password for the specific key alias

## iOS Signing Secrets

1. **IOS_CERT_BASE64** (Required for signed IPA)
   - Base64-encoded PKCS#12 certificate (.p12 file exported from Keychain)
   - How to generate:
     ```bash
     base64 -w0 cert.p12 > cert.b64
     # Copy output and paste into secret value
     ```

2. **IOS_CERT_PASSWORD**
   - Password used when exporting the p12 file from Keychain

3. **IOS_PROVISIONING_PROFILE_BASE64** (Required for signed IPA)
   - Base64-encoded provisioning profile (.mobileprovision)
   - Download from Apple Developer Portal
   - How to encode:
     ```bash
     base64 -w0 qmoi.mobileprovision > profile.b64
     # Copy output and paste into secret value
     ```

## Setup Steps

1. Go to: https://github.com/thealphakenya/qmoi-enhanced/settings/secrets/actions
2. For each secret above:
   - Click "New repository secret"
   - Paste the exact name (e.g., ANDROID_KEYSTORE_BASE64)
   - Paste the secret value (base64 string or password)
   - Click "Add secret"
3. Repeat for all 7 secrets (4 Android + 3 iOS)

Once secrets are added, the CI workflow will:

- Detect the secrets and use them for signing
- Build signed APKs (Android) and IPAs (iOS) on tag pushes
- Upload signed artifacts to the GitHub Release

If secrets are not present, the workflow will still build but produce unsigned/debug artifacts.

## Testing

After adding secrets, trigger the workflow via:

```bash
# Using the helper script
GITHUB_PAT=<your-pat> bash scripts/dispatch_workflow_with_pat_clean.sh \
  --workflow .github/workflows/build-and-release.yml \
  --ref v1.2.4 \
  --run

# Or push a new tag
git tag -a v1.2.5 -m "test signed build"
git push origin v1.2.5
```

## Security Notes

- Never commit keystore files, certificates, or provisioning profiles to the repo.
- Secrets are masked in logs but visible to anyone with repo access.
- Rotate signing keys regularly for production releases.
- Consider using a dedicated signing identity separate from development keys.
- For sensitive projects, use self-hosted runners with additional isolation.

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
