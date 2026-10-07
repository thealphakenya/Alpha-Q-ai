---
title: "COMPONENTS.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# COMPONENTS.md

## Usage

Most components are used in the main application page (`app/page.tsx`) and are integrated into the sidebar, main content, or preview sections. Some are used in specialized panels, dashboards, or as context providers. For details, see the import statements and JSX usage in `app/page.tsx` and related files.

### Example Usage

```tsx
import { Chatbot } from "../src/components/Chatbot";
<Chatbot />;
```

Props and usage details are documented in each component's file.

---

## Automation & Enhancement

- All components are designed to be lightweight, fast, and reliable.
- QMOI memory is integrated via `QmoiMemoryPanel` and is used everywhere: in all chats, apps, and platforms. It is automated for speed, appearance, reliability, and power.
- For production, ensure all components are styled, optimized, and tested for performance and reliability.
- Automation features include real-time logging, auto-sync, and persistent memory across all platforms and apps.

---

## For More Details

- See each component's `.tsx` file for implementation and usage examples.
- Refer to DEVCOMMANDS.md for development commands.
- See TRACKS.md, SYNCREPOS.md, and ALLMDFILESREFS.md for automation, memory, and sync features.
- FEATURESREADME.md and ENHANCED_AUTOMATION_SUMMARY.md provide details on advanced features and automation.
- FarmBusinessManager.tsx: Farm business management
- FileCategorizer.tsx: File categorization UI
- FileExplorer.tsx: File explorer panel
- FinancialManager.tsx: Financial management features
- FloatingPreviewWindow.tsx: Floating preview UI
- GitStatus.tsx: Git status panel
- GlobalCall.tsx: Global call features
- GlobalFileTransfer.tsx: File transfer UI
- GlobalMail.tsx: Global mail features
- GlobalVideoCall.tsx: Video call features
- HelpGuide.tsx: Help and guide UI
- LcSpaces.tsx: LC spaces panel
- LeahWallet.tsx: Wallet features
- LeahWalletPanel.tsx: Wallet panel UI
- MapLocationPanel.tsx: Location mapping
- MasterContext.tsx: Master context provider
- MediaPreviewWindow.tsx: Media preview UI
- NotificationCenter.tsx: Notification center
- NotificationPanel.tsx: Recent notifications panel
- PreviewWindow.tsx: Main preview UI
- PriceProductVerifier.tsx: Product verification
- QAvatar.tsx: Avatar UI
- QCityErrorManager.tsx: Error management for QCity
- QCityThemeProvider.tsx: Theme provider for QCity
- QConverse.tsx: Conversation UI
- QFileManager.tsx: File manager
- QI.tsx: QI main panel
- QIStateWindow.tsx: QI state display
- QMOIAutoFixDashboard.tsx: Auto-fix dashboard
- QMOIOwnDevice.tsx: Own device management
- QiSpaces.tsx: Qi spaces panel
- QmoiAccessibility.tsx: Accessibility features
- QmoiAutoDistribution.tsx: Auto distribution UI
- QmoiBrowser.tsx: QMOI browser features
- QmoiDialer.tsx: Dialer UI
- QmoiEnhancedSystem.tsx: Enhanced system UI
- QmoiKeyboard.tsx: Keyboard panel
- QmoiMediaManager.tsx: Media management
- QmoiMemoryPanel.tsx: QMOI memory panel
- QmoiRevenueDashboard.tsx: Revenue dashboard
- SettingsPanel.tsx: Settings management
- SisterProjects.tsx: Sister projects panel
- SystemHealthDashboard.tsx: System health UI
- TeamRoleManager.tsx: Team role management
- TradingPanel.tsx: Trading panel
- VoiceSelectionPanel.tsx: Voice selection UI
- WhatsAppBusinessPanel.tsx: WhatsApp business features
- WifiAutoConnectPanel.tsx: WiFi auto-connect
- WifiPanel.tsx: WiFi management

---

## src/components Directory

### UI & Functional Components

- AITradingRules.tsx: AI trading rules panel
- AssetOverview.tsx: Asset overview UI
- Chatbot.tsx: Main chatbot UI
- DownloadQCity.tsx: QCity download panel
- FileExplorer.tsx: File explorer panel
- FloatingAQ.tsx: Floating AQ panel
- GitStatus.tsx: Git status panel
- LcSpaces.tsx: LC spaces panel
- PreviewWindow.tsx: Main preview UI
- QI.tsx: QI main panel
- QIStateWindow.tsx: QI state display
- QiSpaces.tsx: Qi spaces panel
- TradingHistory.tsx: Trading history panel
- TradingStatus.tsx: Trading status panel
- alpha-q-ai-system.tsx: Alpha Q AI system panel
- release-notes.tsx: Release notes UI
- theme-provider.tsx: Theme provider
- vercel-analytics-next.ts: Vercel analytics integration

---

## Usage

Most components are used in the main application page (`app/page.tsx`) and are integrated into the sidebar, main content, or preview sections. Some are used in specialized panels, dashboards, or as context providers. For details, see the import statements and JSX usage in `app/page.tsx` and related files.

---

## How to Use

- Import the component from its directory (e.g., `import { Chatbot } from '../src/components/Chatbot'`)
- Add the component to your JSX: `<Chatbot />`
- Pass props as needed (see each component's file for details)

---

## Automation & Enhancement

- All components are designed to be lightweight, fast, and reliable.
- QMOI memory is integrated via `QmoiMemoryPanel` and can be further enhanced for use in all chats, apps, and platforms.
- For production, ensure all components are styled, optimized, and tested for performance and reliability.

---

## For More Details

- See each component's `.tsx` file for implementation and usage examples.
- Refer to DEVCOMMANDS.md for development commands.
- See TRACKS.md, SYNCREPOS.md, and ALLMDFILESREFS.md for automation, memory, and sync features.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/COMPONENTS.md",
"validated_at": "2025-10-26T20:51:24.604102Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "COMPONENTS.md"
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
