# QMOI Apps: Download & Installation Guide

**Last Updated:** 2026-09-13  
**Status:** Multi-Platform Download Instructions  
**Supported Apps:** QMOIAIUI, QMOI Space, QCity, QALPHA

**Authoritative source:** [QMOI v1.2.5 published release](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5). The autonomous agent verifies every published release asset on GitHub-hosted runners. Store listings and custom `downloads.qmoi.com` URLs are not used until they have a real published listing.

---

## Quick Start: Download Your App

Choose your platform and app to get started immediately.

---

## Windows Desktop

### QMOIAIUI (Conversational AI)
- **Windows asset:** [Download v1.2.5 EXE](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qmoi_ai.exe)
- **Winget:** `winget install qmoiaiui`

### QMOI Space (Media Player)
- **Windows package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qmoi-space.zip)
- **Winget:** `winget install qmoi-space`

### QCity (File Manager)
- **Windows package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qcity_package.zip)
- **Winget:** `winget install qcity`

### QALPHA (IDE)
- **Windows package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/q-alpha.zip)
- **Winget:** `winget install qalpha`

**System Requirements:**
- Windows 10 (v1909+) or Windows 11
- 4GB RAM minimum, 8GB recommended
- 1GB free disk space per app
- Internet connection (optional for offline usage)

---

## macOS Desktop

### QMOIAIUI (Conversational AI)
- **DMG Installer:** [Download v1.2.5](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qmoi_ai.dmg)
- **Homebrew:** `brew install qmoiaiui`

### QMOI Space (Media Player)
- **macOS package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qmoi-space.zip)
- **Homebrew:** `brew install qmoi-space`

### QCity (File Manager)
- **macOS package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qcity_package.zip)
- **Homebrew:** `brew install qcity`

### QALPHA (IDE)
- **macOS package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/q-alpha.zip)
- **Homebrew:** `brew install qalpha`

**System Requirements:**
- macOS 12 Monterey or newer
- Intel Core i5 or Apple Silicon M1/M2/M3
- 4GB RAM minimum, 8GB recommended
- 1GB free disk space per app

**Note:** Notarized apps - no Gatekeeper warnings.

---

## Linux Desktop

### QMOIAIUI (Conversational AI)
- **AppImage:** [Download v1.2.5](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qmoi_ai.AppImage)
- **Snap:** `snap install qmoiaiui`
- **Flatpak:** `flatpak install flathub com.qmoi.aiapp`
- **Ubuntu PPA:** 
  ```bash
  sudo add-apt-repository ppa:qmoi/stable
  sudo apt-get update
  sudo apt-get install qmoiaiui
  ```
- **Fedora COPR:**
  ```bash
  sudo dnf copr enable qmoi/stable
  sudo dnf install qmoiaiui
  ```
- **Arch AUR:** `yay -S qmoiaiui`

### QMOI Space (Media Player)
- **Linux package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qmoi-space.zip)
- **Snap:** `snap install qmoi-space`
- **Flatpak:** `flatpak install flathub com.qmoi.space`
- **Ubuntu PPA:** `sudo apt-get install qmoi-space`
- **Fedora COPR:** `sudo dnf install qmoi-space`

### QCity (File Manager)
- **Linux package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qcity_package.zip)
- **Snap:** `snap install qcity`
- **Flatpak:** `flatpak install flathub com.qcity.filemanager`
- **Ubuntu PPA:** `sudo apt-get install qcity`
- **Fedora COPR:** `sudo dnf install qcity`

### QALPHA (IDE)
- **Linux package:** [Download v1.2.5 package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/q-alpha.zip)
- **Snap:** `snap install qalpha`
- **Flatpak:** `flatpak install flathub com.qalpha.ide`
- **Ubuntu PPA:** `sudo apt-get install qalpha`
- **Fedora COPR:** `sudo dnf install qalpha`

**System Requirements:**
- Ubuntu 22.04 LTS, Ubuntu 24.04 LTS
- Fedora 39+, Debian 12+, Arch Linux
- Intel Core i5 or ARM64
- 2GB RAM minimum, 4GB recommended
- 500MB free disk space per app

**Note:** All apps support both X11 and Wayland.

---

## iOS Mobile

### Download from App Store
All QMOI apps are available exclusively through the Apple App Store.

**QMOIAIUI:** [Download verified iOS package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qmoi_ai.ipa)
- Minimum: iOS 14+
- Size: ~38 MB (downloads on first launch)
- Requires: iPhone XS or newer, iPad (5th gen or newer)

**QMOI Space:** [View published packages](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5) (no native iOS asset published)
- Minimum: iOS 14+
- Size: ~52 MB
- Requires: iPhone XS or newer

**QCity:** [View published packages](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5) (no native iOS asset published)
- Minimum: iOS 14+
- Size: ~45 MB
- Requires: iPhone XS or newer

**QALPHA:** [View published packages](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5) (no native iOS asset published)
- Minimum: iOS 15+
- Size: ~160 MB (including IDE assets)
- Requires: iPad (6th gen or newer)

**Installation Steps:**
1. Open App Store on iPhone/iPad
2. Search for "QMOIAIUI" (or desired app name)
3. Tap "Get" → "Install"
4. Authenticate with Face ID, Touch ID, or Apple ID password
5. Wait for installation to complete
6. Tap "Open" to launch the app

**Alternative: TestFlight Beta**
- Join beta testing: no public TestFlight listing is currently published; use the [v1.2.5 release](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5)
- Test new features before release
- Provide feedback to improve the app

---

## Android Mobile

### Download from Google Play Store
All QMOI apps are available exclusively through Google Play.

**QMOIAIUI:** [Download verified Android package](https://github.com/thealphakenya/qmoi-enhanced/releases/download/v1.2.5/qmoi_ai.apk)
- Minimum: Android 11 (API 30+)
- Size: ~42 MB (downloads on first launch)
- Requires: ARM64 processor, 2GB RAM

**QMOI Space:** [View published packages](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5) (no native Android asset published)
- Minimum: Android 11 (API 30+)
- Size: ~58 MB
- Requires: ARM64 processor, 2GB RAM

**QCity:** [View published packages](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5) (no native Android asset published)
- Minimum: Android 11 (API 30+)
- Size: ~48 MB
- Requires: ARM64 processor, 2GB RAM

**QALPHA:** [View published packages](https://github.com/thealphakenya/qmoi-enhanced/releases/tag/v1.2.5) (no native Android asset published)
- Minimum: Android 12 (API 31+)
- Size: ~170 MB (including IDE assets)
- Requires: ARM64 processor, 3GB RAM

**Installation Steps:**
1. Open Google Play Store on Android device
2. Search for "QMOIAIUI" (or desired app name)
3. Tap "Install"
4. Authenticate with Google Account (if needed)
5. Wait for installation to complete
6. Tap "Open" to launch the app

**Alternative: Android Beta Program**
- Join Google Play beta: Open app → scroll down → "Join the beta"
- Test new features before full release
- Provide feedback via Play Store

---

## Web Browser (PWA)

### Access Online
Visit any of these URLs to access QMOI apps via your web browser:

**QMOIAIUI:** https://qmoi.com/ai
**QMOI Space:** https://qmoi.com/space
**QCity:** https://qmoi.com/files
**QALPHA:** https://qmoi.com/ide (read-only preview)

**Install as App:**
1. Open app URL in supported browser (Chrome, Firefox, Safari, Edge)
2. Click menu (⋮ or ⌘+A)
3. Select "Install app" or "Add to Home Screen"
4. Confirm installation
5. App appears on home screen / taskbar

**Supported Browsers:**
- Chrome 90+ (Desktop, Mobile)
- Firefox 88+ (Desktop, Mobile)
- Safari 15+ (macOS, iOS)
- Edge 90+ (Desktop)

**Offline Capability:**
- Works offline after first visit
- All data synced via Service Worker
- Automatic updates when online

---

## Version Information

### Current Stable Release
**QMOI Version 1.2.3** (Released: 2026-08-13)

**What's New:**
- Enhanced handsfree controls (voice, gestures, eye tracking)
- Improved file type handler system
- New accessibility profiles
- Better cross-platform synchronization
- Performance improvements

**Update History:**
- v1.2.3: Current (stable)
- v1.2.2: Previous (security patches available)
- v1.1.0: Legacy (no longer supported)

**Auto-Update:**
- Windows: Automatic via Windows Update / Microsoft Store
- macOS: Automatic via App Store
- Linux: Automatic via system package manager (apt, dnf, pacman)
- iOS: Automatic via App Store (if enabled)
- Android: Automatic via Google Play (if enabled)
- Web PWA: Automatic via Service Worker

---

## Troubleshooting Downloads

### "File not found" or "Download failed"
- Check your internet connection
- Try downloading from an alternative source (see options above)
- Try again in a few minutes (server may be temporarily unavailable)

### "Cannot install: Device not compatible"
- Verify your device meets minimum requirements
- Update your OS to latest version
- Contact support: support@qmoi.com

### "Antivirus/Security warning"
- The file is safe. Warnings appear because app is new.
- Add exception to your antivirus
- Download from official QMOI website or app store

### "Corrupt or incomplete download"
- Delete the partial file
- Clear browser cache
- Download again
- Try alternative download method

### "Installation failed silently"
- Restart your device
- Clear app cache (Settings → Apps → Clear Cache)
- Reinstall from scratch
- Check available storage space

---

## Need Help?

- **FAQ:** https://qmoi.com/help/faq
- **Support:** support@qmoi.com
- **Community Support:** https://github.com/thealphakenya/qmoi-enhanced/issues
- **Discord Server:** https://discord.gg/qmoi

---

## Digital Security & Integrity

All downloads are signed and verified:

- **Windows:** Authenticode certificate (Microsoft trusted)
- **macOS:** Developer ID certificate + notarization
- **Linux:** GPG-signed packages
- **iOS:** Apple App Store review
- **Android:** Google Play Protect scan
- **Web:** HTTPS/TLS encryption

**Verify Download Integrity:**
```bash
# All downloads include SHA256 checksums
sha256sum qmoiaiui-1.2.3.AppImage
# Expected: abc123def456...
```

---

**Last Updated:** 2026-08-13 by QMOI Development Team

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10603`; directories: `1280`; Markdown: `2421`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2157, build_download_install=2113, disability_accessibility=268, orchestration=2065, qteam_accountability=2053, release_tag_publish=2092, tree_inventory=2004`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2226`; needs review: `187`; metric candidate lines: `52756`; percentage occurrences: `22237`.
- Markdown word count: `3562982`; heuristic sentence count: `674722`; sentence records indexed: `674722`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29846` metric claims; `10693` completion claims; `29749` metric and `10564` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9053` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13376`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40146` lines in `3689` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `299`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
