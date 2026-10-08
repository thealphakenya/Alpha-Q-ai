# TECHNICAL REFERENCE — Next Steps Commands

**Quick copy-paste commands for Phase 1-4 execution**

---

## Phase 1: Workflow Validation

### Create & Push Test Release Tag

```bash
cd /workspaces/qmoi-enhanced

# Create test tag
git tag test-v1.2.5 -m "Test release for workflow validation"

# Push tag (triggers sync-draft workflow automatically)
git push origin test-v1.2.5

# Monitor workflow in real-time
# Visit: https://github.com/thealphakenya/qmoi-enhanced/actions
```

### Check Draft Release Status

```bash
# List release assets (requires gh CLI installed)
gh release view test-v1.2.5 --repo thealphakenya/qmoi-enhanced \
  --json assets --jq '.assets | length'
# Expected: 16

# Get detailed asset info
gh release view test-v1.2.5 --repo thealphakenya/qmoi-enhanced \
  --json assets --jq '.assets[] | {name, size}'

# Check if release is draft (not published)
gh release view test-v1.2.5 --repo thealphakenya/qmoi-enhanced \
  --json isDraft --jq '.isDraft'
# Expected: true
```

### Download & Verify a Single Asset

```bash
# Download AppImage
curl -L -o /tmp/qmoi_ai.AppImage \
  https://github.com/thealphakenya/qmoi-enhanced/releases/download/test-v1.2.5/qmoi_ai.AppImage

# Get expected SHA256 from manifest
EXPECTED_SHA=$(jq -r '.assets[] | select(.name == "qmoi_ai.AppImage") | .sha256' \
  /workspaces/qmoi-enhanced/release_assets_manifest.json)

# Calculate actual SHA256
ACTUAL_SHA=$(sha256sum /tmp/qmoi_ai.AppImage | awk '{print $1}')

# Compare
echo "Expected: $EXPECTED_SHA"
echo "Actual:   $ACTUAL_SHA"
echo "Match: $([ "$EXPECTED_SHA" = "$ACTUAL_SHA" ] && echo 'YES ✓' || echo 'NO ✗')"
```

### Publish Draft Release

```bash
# Option A: Using Python script
python3 /workspaces/qmoi-enhanced/scripts/sync_to_draft_release.py \
  --tag test-v1.2.5 \
  --publish

# Option B: Using gh CLI
gh release edit test-v1.2.5 \
  --repo thealphakenya/qmoi-enhanced \
  --draft=false

# Verify it's now published
gh release view test-v1.2.5 --repo thealphakenya/qmoi-enhanced --json isDraft
```

### Full Asset Verification Batch

```bash
# Download all assets and verify all SHA256s
cd /tmp
mkdir -p qmoi_test && cd qmoi_test

# Get all asset names from manifest
jq -r '.assets[].name' /workspaces/qmoi-enhanced/release_assets_manifest.json | \
while read -r asset; do
  echo "Downloading: $asset"
  curl -L -o "$asset" \
    "https://github.com/thealphakenya/qmoi-enhanced/releases/download/test-v1.2.5/$asset"
done

# Verify all checksums
echo "=== VERIFICATION RESULTS ==="
jq -r '.assets[] | "\(.name):\(.sha256)"' \
  /workspaces/qmoi-enhanced/release_assets_manifest.json | \
while IFS=: read -r name sha; do
  actual=$(sha256sum "$name" 2>/dev/null | awk '{print $1}' || echo "MISSING")
  match=$([ "$actual" = "$sha" ] && echo "✓" || echo "✗")
  echo "$match $name"
done
```

---

## Phase 2: Compliance Validation

### Generate Compliance Report Locally

```bash
cd /workspaces/qmoi-enhanced

# Run compliance check
python3 scripts/generate_release_compliance_report.py

# View report
cat reports/release_compliance_report.json | jq '.'

# Check status
cat reports/release_compliance_report.json | jq '.status'
# Expected: "OK"

# Count alerts (should be 0 if compliant)
cat reports/release_compliance_report.json | jq '.alerts | length'
```

### Simulate Non-Compliance (Testing)

```bash
cd /workspaces/qmoi-enhanced

# Backup a critical asset
mv Qmoi_downloaded_apps/qcity_package.zip Qmoi_downloaded_apps/qcity_package.zip.bak

# Run compliance (should detect missing asset)
python3 scripts/generate_release_compliance_report.py

# Check report (status should be non-OK, alerts > 0)
cat reports/release_compliance_report.json | jq '{status: .status, alerts: (.alerts | length)}'

# Restore asset
mv Qmoi_downloaded_apps/qcity_package.zip.bak Qmoi_downloaded_apps/qcity_package.zip

# Re-run compliance (should be OK again)
python3 scripts/generate_release_compliance_report.py
cat reports/release_compliance_report.json | jq '.status'
```

### Manual Trigger of Compliance Workflow (if GitHub CLI available)

```bash
# Dispatch workflow manually
gh workflow run release-compliance-check.yml \
  --repo thealphakenya/qmoi-enhanced \
  --ref autosync-backup-20250926-232440

# Check recent runs
gh run list --workflow=release-compliance-check.yml \
  --repo thealphakenya/qmoi-enhanced \
  --limit 3 \
  --json name,status,conclusion

# View latest run logs (replace with actual run ID)
gh run view <RUN_ID> --log --repo thealphakenya/qmoi-enhanced
```

---

## Phase 3: Documentation Updates

### Fetch Real Release Data

```bash
# Get v1.2.3 release info (JSON)
gh release view v1.2.3 --repo thealphakenya/qmoi-enhanced --json \
  name,body,createdAt,publishedAt,assets | jq '.'

# Extract asset names & sizes
gh release view v1.2.3 --repo thealphakenya/qmoi-enhanced --json assets \
  --jq '.assets[] | "\(.name) (\(.size | tonumber / 1048576 | round / 1) MB)"'
```

### Update Files with Real Data

```bash
# For GITHUB_RELEASES_RECENT.md:
# 1. Get release info:
gh release view v1.2.3 --repo thealphakenya/qmoi-enhanced --json \
  name,body,publishedAt | jq -r '.publishedAt, .body'

# 2. Manually edit GITHUB_RELEASES_RECENT.md with real dates & content

# For README.md:
# 1. Verify all download links work
curl -I https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.exe \
  | grep -E "HTTP|Location"
# Expected: 200 OK or 302 redirect

# 2. Test all platform links in quick batch
for platform in "exe" "dmg" "AppImage" "deb" "apk" "ipa"; do
  echo -n "Testing .$platform: "
  curl -s -I "https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/*.$platform" \
    2>/dev/null | head -1 | grep -q "200\|302" && echo "✓" || echo "✗"
done
```

### Validate All Documentation Links

```bash
# Extract all URLs from markdown files
grep -r "https://" /workspaces/qmoi-enhanced/README.md \
  /workspaces/qmoi-enhanced/RELEASE_MAINTENANCE.md \
  /workspaces/qmoi-enhanced/GITHUB_RELEASES_RECENT.md \
  /workspaces/qmoi-enhanced/DOWNLOADS.md 2>/dev/null | \
grep -oP 'https?://[^\s)]+' | sort -u | \
while read url; do
  status=$(curl -s -I -L "$url" 2>/dev/null | head -1 | awk '{print $2}')
  echo "$status $url"
done | sort
```

---

## Phase 4: Security & Cleanup

### Review Dependabot Alerts

```bash
# List all security alerts
gh secret list --repo thealphakenya/qmoi-enhanced 2>/dev/null || \
  echo "Note: Run from repo directory with 'gh auth login' first"

# Get Dependabot status (via API)
curl -s -H "Authorization: token $(gh auth token)" \
  https://api.github.com/repos/thealphakenya/qmoi-enhanced/vulnerability-alerts \
  | jq '.[] | {repository, vulnerability}'
```

### Check Dependency Versions

```bash
cd /workspaces/qmoi-enhanced

# Python dependencies
if [ -f requirements.txt ]; then
  echo "=== Python Dependencies ==="
  cat requirements.txt
fi

# Node.js dependencies
if [ -f package.json ]; then
  echo "=== Node.js Dependencies ==="
  jq '.dependencies' package.json
fi

# Docker base images
if find . -name "Dockerfile*" -type f | head -1 >/dev/null; then
  echo "=== Docker Base Images ==="
  grep -h "^FROM" Dockerfile* | sort -u
fi
```

### Commit Documentation & Fixes

```bash
cd /workspaces/qmoi-enhanced

# Add all changes
git add -A

# Review changes before commit
git diff --cached --stat

# Commit with descriptive message
git commit -m "docs: update release docs and fix verification links

- Updated GITHUB_RELEASES_RECENT.md with v1.2.3 & v1.2.4 real data
- Created RELEASES_USER_GUIDE.md for user quick-start
- Verified all SHA256 links and download URLs
- Fixed deprecated links in platform-specific docs"

# Push to remote
git push origin autosync-backup-20250926-232440
```

---

## Useful Utilities

### Watch Workflow Progress

```bash
# Keep checking workflow status (updates every 5 sec)
watch -n 5 'gh run list --workflow=sync-releases-from-manifest.yml \
  --repo thealphakenya/qmoi-enhanced \
  --limit 1 \
  --json status,conclusion'
```

### Compare Manifest vs Actual Files

```bash
cd /workspaces/qmoi-enhanced

echo "=== Assets in Manifest ==="
jq -r '.assets[].name' release_assets_manifest.json | sort

echo ""
echo "=== Files in Qmoi_downloaded_apps/ ==="
find Qmoi_downloaded_apps -type f ! -path '*/.*' -name '*' | \
  sed 's#.*/##' | sort

echo ""
echo "=== Files in downloads/ ==="
find downloads -type f ! -path '*/.*' -name '*' | \
  sed 's#.*/##' | sort
```

### Generate Fresh SHA256 Checksums

```bash
cd /workspaces/qmoi-enhanced

echo "Regenerating manifest with fresh checksums..."
python3 scripts/generate_release_manifest.py

echo "Comparing with previous version..."
git diff release_assets_manifest.json | head -50
```

### Test GitHub API Authentication

```bash
# Verify PAT works
curl -s -H "Authorization: token $(gh auth token)" \
  https://api.github.com/user | jq '.login, .name'

# Check token scopes
curl -s -H "Authorization: token $(gh auth token)" \
  https://api.github.com/user | jq '.scopes // "NO SCOPES INFO"'

# Check repo access
curl -s -H "Authorization: token $(gh auth token)" \
  https://api.github.com/repos/thealphakenya/qmoi-enhanced | \
  jq '.name, .private, .permissions'
```

---

## Troubleshooting Commands

### If Workflow Fails

```bash
# Get latest workflow run
RUN_ID=$(gh run list --workflow=sync-releases-from-manifest.yml \
  --repo thealphakenya/qmoi-enhanced --limit 1 --json databaseId \
  --jq '.[0].databaseId')

# View full logs
gh run view $RUN_ID --log --repo thealphakenya/qmoi-enhanced

# Re-run failed workflow
gh run rerun $RUN_ID --repo thealphakenya/qmoi-enhanced
```

### If Assets Are Missing

```bash
cd /workspaces/qmoi-enhanced

# Check what's in the release
gh release view v1.2.3 --repo thealphakenya/qmoi-enhanced \
  --json assets --jq '.assets | length'

# Compare with manifest
echo "Expected: $(jq '.assets | length' release_assets_manifest.json)"

# Re-sync missing assets
python3 scripts/sync_all_releases.py
# (This will back up and re-upload all assets)
```

### Restore from Backup

```bash
cd /workspaces/qmoi-enhanced

# List available backups
ls -la reports/releases_backup/

# Restore a backup
# (Manual step: copy files back from reports/releases_backup/<TAG>/)
cp reports/releases_backup/v1.2.3/* Qmoi_downloaded_apps/
```

---

## Checklist for Execution

Print this and check off as you go:

```
Phase 1: Workflow Validation
[ ] git tag test-v1.2.5 && git push origin test-v1.2.5
[ ] gh release view test-v1.2.5 shows 16 assets
[ ] Download & verify SHA256 of 1 asset
[ ] Publish draft: sync_to_draft_release.py --tag test-v1.2.5 --publish
[ ] Verify published on GitHub

Phase 2: Compliance
[ ] python3 scripts/generate_release_compliance_report.py
[ ] cat reports/release_compliance_report.json | jq '.status' → "OK"
[ ] Simulate non-compliance (rename asset)
[ ] Run compliance again (should fail)
[ ] Restore asset & verify compliant again

Phase 3: Documentation
[ ] Update GITHUB_RELEASES_RECENT.md with real data
[ ] Create RELEASES_USER_GUIDE.md
[ ] Test all download links: curl -I <URL>
[ ] git add -A && git commit
[ ] git push

Phase 4: Security
[ ] Review Dependabot vulnerabilities
[ ] Merge or create fix PRs
[ ] Verify no critical issues remain
[ ] Final commit & push
```

---

**Last Updated**: November 14, 2025  
**Commands Tested On**: Alpine Linux v3.22 (bash)

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
