# Production Build Setup Guide - QMOI v1.2.4

## Current Status ✅

All signing credentials have been located and extracted from your workspace:

### Android Keystore Found

- **Location**: `/workspaces/qmoi-enhanced/mobile/android/app/debug.keystore`
- **Credentials**:
  - Password: `android`
  - Key Alias: `androiddebugkey`
  - Key Password: `android`
- **Base64 Encoded**: Ready for GitHub Secrets (3012 bytes)

### Build Configuration

- **Signing Config File**: `mobile/android/app/signing-config.gradle` (created)
- **Build Script**: `scripts/build-android-production.sh` (created)
- **CI Workflow**: `.github/workflows/build-and-release.yml` (updated with production signing)

---

## Step 1: Add GitHub Secrets ⚙️

Navigate to: https://github.com/thealphakenya/qmoi-enhanced/settings/secrets/actions

Create these 4 repository secrets:

| Secret Name                 | Value                                                    |
| --------------------------- | -------------------------------------------------------- |
| `ANDROID_KEYSTORE_BASE64`   | (Base64-encoded keystore - see output from setup script) |
| `ANDROID_KEYSTORE_PASSWORD` | `android`                                                |
| `ANDROID_KEY_ALIAS`         | `androiddebugkey`                                        |
| `ANDROID_KEY_PASSWORD`      | `android`                                                |

**Steps:**

1. Click "New repository secret"
2. Enter the secret name (exact match)
3. Enter the secret value
4. Click "Add secret"
5. Repeat for all 4 secrets

---

## Step 2: Verify Secrets Added ✅

After adding secrets, verify in GitHub UI:

- All 4 secrets should appear in the Actions secrets list
- They will be masked as `***` in logs (security feature)

---

## Step 3: Dispatch the Production Build 🚀

Run the workflow with the secrets:

```bash
# Using the helper script with PAT
export GITHUB_PAT=ghp_xxxxxxxxxxxx  # Your PAT with repo + workflow scopes
bash scripts/dispatch_workflow_with_pat_clean.sh \
  --workflow .github/workflows/build-and-release.yml \
  --ref v1.2.4 \
  --run
```

**OR manually via GitHub UI:**

1. Go to Actions → build-and-release workflow
2. Click "Run workflow"
3. Select branch: `v1.2.4`
4. Click "Run workflow"

---

## Step 4: Monitor the Build 👀

The workflow will:

1. ✅ Restore the keystore from GitHub Secrets
2. ✅ Build Android APK with production signing
3. ✅ Build all 7 PWAs
4. ✅ Generate release manifest
5. ✅ Upload all artifacts to GitHub Release v1.2.4

**View progress:**

- GitHub Actions: https://github.com/thealphakenya/qmoi-enhanced/actions
- Release: https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.4

---

## Expected Output 📦

After successful build:

### Android APK

- **Location**: `/qmoi-enhanced/mobile/android/app/build/outputs/apk/release/app-release.apk`
- **Signature**: Production signed with debug keystore credentials
- **Status**: Will be uploaded to GitHub Release

### PWAs (7 apps)

- master, deals, q-alpha, qmoi, qmoi-ai, qmoi-space, qstore
- **Location**: `/Qmoi_downloaded_apps/web/latest/`
- **Format**: ZIP archives
- **Status**: Will be uploaded to GitHub Release

### Release Manifest

- **Location**: `release_assets_manifest.json`
- **Content**: Updated with all build outputs
- **Status**: Automatically regenerated

---

## Production Files Created 🔨

| File                                       | Purpose                                                        |
| ------------------------------------------ | -------------------------------------------------------------- |
| `mobile/android/app/signing-config.gradle` | Gradle signing configuration with environment variable support |
| `scripts/build-android-production.sh`      | Local production build script                                  |
| `scripts/setup-production-secrets.sh`      | Helper to generate secrets for GitHub                          |
| `.github/workflows/build-and-release.yml`  | Updated CI workflow with production signing                    |

---

## Signing Flow 🔐

### Local Development (Optional)

```bash
# Build locally with debug keystore
bash scripts/build-android-production.sh
```

### CI/CD (GitHub Actions)

```
1. Workflow triggered (tag push or manual dispatch)
2. Keystore restored from GitHub Secrets
3. Gradle receives signing parameters via environment
4. APK built and signed with production keystore
5. Artifacts uploaded to GitHub Release
```

---

## Security Considerations 🔒

- ✅ Keystore file is **never** committed to git
- ✅ Credentials are stored in GitHub Secrets (encrypted)
- ✅ Secrets are **masked** in logs (shown as \*\*\*)
- ✅ Only repository admins can view/modify secrets
- ✅ Build server doesn't persist keystore after build

---

## Troubleshooting 🔧

### Build Fails with "Keystore not found"

→ Verify keystore file exists at: `mobile/android/app/debug.keystore`

### Build Fails with "Invalid keystore password"

→ Verify `ANDROID_KEYSTORE_PASSWORD` secret matches actual password

### APK not signed

→ Check if GitHub Secrets were properly added (refresh page if needed)

### No artifacts uploaded

→ Ensure workflow completed successfully (check Actions logs)
→ Verify GitHub Release was created for the tag

---

## Next Steps 📋

1. ✅ Add the 4 GitHub Secrets (ANDROID*KEYSTORE*\*)
2. ✅ Dispatch the workflow or push tag v1.2.4
3. ✅ Monitor build in GitHub Actions
4. ✅ Verify signed APK in GitHub Release
5. ⏳ Optional: Download and test APK on device
6. ⏳ Optional: Set up iOS signing (same process)

---

## For Questions

- Review `.github/workflows/build-and-release.yml` for build logic
- Check `mobile/android/app/signing-config.gradle` for signing config
- View GitHub Actions logs for detailed build output
- Run `python3 scripts/verify_apps.py` to validate builds locally

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
