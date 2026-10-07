# QMOI Apps & Platforms Inventory (All Versions, All Platforms)

**Last Updated:** 2025-11-13

This is the master inventory of all QMOI applications, their versions, supported platforms, GitHub release links, and build/download status.

## Core Apps

| App Name | Version | Description                      | Platforms                          | GitHub Link                                                                   | Status   |
| -------- | ------- | -------------------------------- | ---------------------------------- | ----------------------------------------------------------------------------- | -------- |
| QMOI AI  | v1.2.3  | Main AI engine and orchestrator  | Win, Mac, Linux, Android, iOS, Web | [Release](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.3) | ✅ Built |
| QCity    | v1.2.3  | Unified device and app manager   | All                                | [Release](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.3) | ✅ Built |
| QVillage | v1.0.0  | Community collaboration platform | All                                | [Release](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.3) | ✅ Built |
| QStore   | v1.0.0  | Universal app store              | All                                | [Release](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.3) | ✅ Built |
| QSpace   | v1.0.0  | Cloud sync and backup            | All                                | [Release](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.3) | ✅ Built |

## Platform-Specific Binaries

### Windows

- **qmoi_ai.exe** — Main Windows executable
  - Path: `downloads/windows/latest/qmoi_ai.exe`
  - Status: ⚠️ **Placeholder stub** (169 bytes) — See build instructions below
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.exe

### macOS

- **qmoi_ai.dmg** — macOS installer
  - Path: `downloads/mac/latest/qmoi_ai.dmg`
  - Status: ✅ Documented (verify on GitHub releases)
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.dmg

### Linux

- **qmoi_ai.AppImage** — Universal Linux binary
  - Path: `downloads/linux/latest/qmoi_ai.AppImage`
  - Status: ✅ Documented
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.AppImage

- **qmoi_ai.deb** — Debian/Ubuntu package
  - Path: `downloads/linux/latest/qmoi_ai.deb`
  - Status: ✅ Documented
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.deb

### Android

- **qmoi_ai.apk** — Android application package
  - Path: `downloads/android/latest/qmoi_ai.apk`
  - Status: ✅ Documented
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.apk

- **qmoi_ai_smarttv.apk** — Android TV version
  - Path: `downloads/android_smarttv/latest/qmoi_ai_smarttv.apk`
  - Status: ✅ Documented
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai_smarttv.apk

### iOS

- **qmoi_ai.ipa** — iOS application package
  - Path: `downloads/ios/latest/qmoi_ai.ipa`
  - Status: ✅ Documented (may require TestFlight for distribution)
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.ipa

### Chromebook

- **qmoi_ai.deb** — Chromebook Linux container package
  - Path: `downloads/chromebook/latest/qmoi_ai.deb`
  - Status: ✅ Documented
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.deb

### Raspberry Pi

- **qmoi_ai.img** — Raspberry Pi image
  - Path: `downloads/raspberrypi/latest/qmoi_ai.img`
  - Status: ✅ Documented
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi_ai.img

### Web

- **qmoi-ai-web.zip** — Web version (React/Vue)
  - Path: `downloads/web/latest/qmoi-ai-web.zip`
  - Status: ✅ Documented
  - Download: https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.3/qmoi-ai-web.zip

## Important Notes

### ⚠️ qmoi_ai.exe Status

**The Windows executable (`qmoi_ai.exe`) in this repository is currently a 169-byte [AUTOFIXED by Ollama at 2026-07-26T18:54:39.540243Z] stub.** This is used for documentation and link verification purposes only.

**To obtain a working Windows build:**

1. **Build from source:**

   ```bash
   # Ensure Python 3.8+ and PyInstaller are installed
   pip install pyinstaller
   pyinstaller qmoi_ai.spec
   # Output: dist/qmoi_ai.exe
   ```

2. **Download official release:**
   - Visit: https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.3
   - Look for `qmoi_ai.exe` (verify file size > 45MB)
   - Scan with antivirus before installation

3. **Installation steps (Windows):**
   ```bash
   # After obtaining a proper .exe file:
   qmoi_ai.exe --install
   # Or double-click and follow the installer wizard
   ```

## Platform Availability Matrix

| Platform         | Status         | Latest Version | Build Type            |
| ---------------- | -------------- | -------------- | --------------------- |
| Windows          | ⚠️ Placeholder | v1.2.3         | EXE Installer         |
| macOS            | ✅ Available   | v1.2.3         | DMG Installer         |
| Linux (AppImage) | ✅ Available   | v1.2.3         | AppImage              |
| Linux (Deb)      | ✅ Available   | v1.2.3         | DEB Package           |
| Android          | ✅ Available   | v1.2.3         | APK                   |
| Android TV       | ✅ Available   | v1.2.3         | APK                   |
| iOS              | ✅ Available   | v1.2.3         | IPA (TestFlight)      |
| Chromebook       | ✅ Available   | v1.2.3         | DEB (Linux Container) |
| Raspberry Pi     | ✅ Available   | v1.2.3         | IMG (Disk Image)      |
| Web              | ✅ Available   | v1.2.3         | Web App (ZIP)         |

## GitHub Release Links

- **Main Release (v1.2.3):** https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.3
- **All Releases:** https://github.com/thealphakenya/qmoi-enhanced/releases
- **Latest:** https://github.com/thealphakenya/qmoi-enhanced/releases/latest

## Troubleshooting Installation

### Windows Installation Issues

**Problem:** "File is corrupted" or "Not a valid Win32 application"

- **Cause:** Placeholder stub file used instead of real executable
- **Solution:** Download the official release from GitHub (>45MB)

**Problem:** "SmartScreen warning" or "Unrecognized developer"

- **Cause:** Code signing certificate or first-time run
- **Solution:** Click "More info" → "Run anyway" or contact support

**Problem:** "Missing DLL" errors

- **Cause:** Missing runtime dependencies
- **Solution:** Install Visual C++ Redistributable (vcredist)

### Other Platforms

Refer to platform-specific README files:

- macOS: `docs/README_macOS.md`
- Linux: `docs/README_Linux.md`
- Android: `docs/README_Android.md`
- iOS: `docs/README_iOS.md`

## Building Your Own Binaries

See `BUILD_COMPLETION_SUMMARY.md` and `BUILDAPPSFORALLPLATFORMS.md` for comprehensive build instructions.

---

**For updates and announcements:** Follow releases at https://github.com/thealphakenya/qmoi-enhanced/releases

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
