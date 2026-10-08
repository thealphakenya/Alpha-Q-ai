# QMOI GitHub Releases - Master Index

**Complete documentation for all QMOI apps available on GitHub Releases**

> **📌 Central Reference:** See [`QMOI_APPS_AND_PLATFORMS_INVENTORY_CORRECTED.md`](./QMOI_APPS_AND_PLATFORMS_INVENTORY_CORRECTED.md) for the authoritative inventory of all apps, versions, platforms, and download links.

## 🎯 Latest Release: v1.2.3 (November 12, 2025)

✅ **Status**: DEPLOYED  
📍 **Link**: https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.3  
📋 **Details**: [DEPLOYMENT_STATUS_V1_2_3.md](./DEPLOYMENT_STATUS_V1_2_3.md)

### What's Included

- ✅ All 6 QMOI Apps (QMOI AI, QCity, QShare, Yap, QStore, QVillage)
- ✅ 12+ Platforms (Windows, macOS, Linux, Android, iOS, Raspberry Pi, Chromebook, PWA, Smart TV, Wear OS, Docker, and more)
- ✅ 72+ Total Builds
- ✅ SHA256 Checksums for all downloads
- ✅ Comprehensive release notes

---

## 📚 Documentation Files

### 1. **GITHUB_RELEASES_COMPLETE_GUIDE.md** (15 KB)

Comprehensive installation guide for all QMOI apps on all platforms.

- Overview of 6 QMOI apps
- Complete platform support (12+ platforms)
- Download options comparison
- Detailed step-by-step installation guides
- Direct download links
- Verification and security
- Troubleshooting section

**Use when:** You need detailed installation instructions.

---

### 2. **GITHUB_RELEASES_QUICK_REFERENCE.md** (3.8 KB)

Quick lookup card for downloads and links.

- All 6 apps summary
- Download speed guide
- Platform file types
- Direct download URLs
- Support resources

**Use when:** You need quick reference information.

---

### 3. **GITHUB_RELEASES_GUIDE.md** (4.4 KB)

Overview of all apps and platforms.

- App and platform inventory
- Installation quick start
- Release information
- Direct download links

**Use when:** You want an overview.

---

### 4. **GITHUB_RELEASES_CONFIG.json** (2.4 KB)

Machine-readable configuration for automation.

- Apps metadata
- Platforms supported
- Repository information
- Version information

**Use when:** Building automation or integrations.

---

## 🛠️ Real-Time Release Tools

### ⚡ Automated GitHub Actions Workflow

**File:** `.github/workflows/publish-releases-realtime.yml`

Fully automated multi-platform release publishing triggered by git tags:

```bash
# Just tag a release - GitHub Actions does everything else!
git tag v1.2.3
git push origin v1.2.3

# Automatically:
# 1. ✅ Discovers all platform builds
# 2. ✅ Generates SHA256 checksums
# 3. ✅ Creates GitHub Release
# 4. ✅ Uploads all assets
# 5. ✅ Publishes release notes
```

**Features:**

- Auto-discovery of Windows, macOS, Linux, Android, iOS, Raspberry Pi, Chromebook, PWA builds
- Platform classification & organization
- SHA256 checksum generation
- Retry logic (3 attempts per asset)
- Real-time progress logging
- Zero-touch operation

**Time:** ~5-10 minutes from tag to live release

---

### 🚀 publish-releases-realtime.sh

Enhanced bash script for manual/automated release publishing.

```bash
# Publish production release
./publish-releases-realtime.sh --version v1.2.3

# Create draft for testing
./publish-releases-realtime.sh --version v1.3.0-beta --draft

# With verbose logging
./publish-releases-realtime.sh --version v1.2.3 --verbose
```

**Features:**

- Asset discovery across multiple directories
- Platform classification (8+ types)
- Parallel checksum generation
- Retry logic with exponential backoff
- Comprehensive logging
- Success/failure statistics

---

### 🐍 publish-releases-realtime.py

Python version with advanced features:

```bash
# Publish release
python publish-releases-realtime.py --version v1.2.3

# Draft release
python publish-releases-realtime.py --version v1.3.0-beta --draft

# Verbose mode
python publish-releases-realtime.py --version v1.2.3 --verbose
```

**Features:**

- Parallel asset processing
- Structured logging
- Comprehensive error handling
- JSON configuration support
- Audit trail generation

---

### 📚 GITHUB_RELEASES_REALTIME_GUIDE.md

Complete documentation for the real-time release system:

- Quick start guide
- Detailed usage instructions
- Architecture overview
- GitHub Actions workflow documentation
- Manual publishing guide
- Troubleshooting
- Best practices

**Use when:** You need comprehensive release automation documentation

---

### Advanced Automation

- ✅ GitHub Actions triggers on git tags (automatic)
- ✅ Manual publishing via shell or Python scripts
- ✅ CI/CD integration (GitLab CI, Jenkins, etc.)
- ✅ Real-time asset discovery & validation
- ✅ Parallel upload with retry logic
- ✅ Full audit logging
- ✅ Zero-touch operation

See detailed guide: `GITHUB_RELEASES_REALTIME_GUIDE.md`

---

## 📱 All 6 QMOI Apps

| App      | Version | Platforms                                                                    |
| -------- | ------- | ---------------------------------------------------------------------------- |
| QMOI AI  | v1.2.3  | Windows, macOS, Linux, Android, iOS, Smart TV, Raspberry Pi, Chromebook, Web |
| QCity    | v2.0.1  | Windows, macOS, Linux, Android, iOS, Web                                     |
| QShare   | v1.0.0  | Universal (all platforms)                                                    |
| Yap      | v1.1.0  | Universal (all platforms)                                                    |
| QStore   | v1.0.0  | Universal (all platforms)                                                    |
| QVillage | v1.0.0  | Universal (all platforms)                                                    |

---

## 🖥️ All 12+ Platforms Supported

**Desktop:**

- ✅ Windows (x64, ARM64)
- ✅ macOS (Intel, Apple Silicon)
- ✅ Linux (DEB, AppImage)

**Mobile:**

- ✅ Android (Phone, Tablet, TV)
- ✅ iOS (iPhone, iPad)

**IoT & Specialized:**

- ✅ Raspberry Pi
- ✅ Chromebook
- ✅ Web/PWA

---

## 📥 Download Methods

1. **GitHub Releases** (Recommended)
   https://github.com/thealphakenya/qmoi-enhanced/releases

2. **Official Portal**
   https://github.com/thealphakenya/qmoi-enhanced/releases

3. **App Stores**
   - Google Play Store
   - Apple App Store
   - Windows Store (coming)
   - Mac App Store (coming)

4. **Web/PWA**
   - https://qmoi.qmoi.app
   - https://qcity.qmoi.app
   - https://qvillage.qmoi.app
   - And more...

---

## 🚀 Quick Start

**Download QMOI AI for Windows:**

1. Visit: https://github.com/thealphakenya/qmoi-enhanced/releases
2. Download: qmoi-ai.exe
3. Run installer
4. Follow prompts

**See detailed guide in:** GITHUB_RELEASES_COMPLETE_GUIDE.md

---

## 📞 Support

- **Releases:** https://github.com/thealphakenya/qmoi-enhanced/releases
- **Issues:** https://github.com/thealphakenya/qmoi-enhanced/issues
- **Email:** support@qmoi.app
- **Community:** https://qvillage.qmoi.app

---

**All QMOI apps available on GitHub with downloads for every platform.**

Status: ✅ Production Ready | Version: v1.2.3 | Date: 2025-11-12

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
