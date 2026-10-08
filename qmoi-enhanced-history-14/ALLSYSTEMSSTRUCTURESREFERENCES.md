---
title: "ALLSYSTEMSSTRUCTURESREFERENCES.md"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# ALLSYSTEMSSTRUCTURESREFERENCES.md

This document provides a comprehensive reference for all system structures, directories, and file responsibilities for QCity, QMOI-AI, and QMOI Space. It is designed for automation, self-development, and permanent operation of QMOI across all platforms.

## Directory & File Structure

- `/qcity-artifacts/` - Stores QCity build artifacts and resources
- `/QCITYREADME.md` - Main documentation for QCity features and activities
- `/QCITYMAINDEVICE.md` - Device management and orchestration
- `/QCITYDEVICEAUTOUPGRADE.md` - Auto-upgrade logic for QCity devices
- `/QCITYRUNNERSENGINE.md` - Runners and orchestration engine
- `/QCITYRESOURCES.md` - Resource management and allocation
- `/QCITYQMOIAUTOSTART.md` - Auto-start and initialization scripts

- `/qmoi_ai.py` - Main AI logic and orchestration
- `/qmoi_ai_launcher.py` - Launcher and entry point
- `/qmoi_ai_installer.iss` - Installer scripts
- `/qmoi_ai.spec` - Build specification
- `/QMOIAICORE.md` - Core AI documentation
- `/QMOI_MEMORY.md` - Memory management and usage
- `/QMOI-ENHANCED-AUTOTESTS.md` - Automated tests for AI features
- `/QMOI-ENHANCED-FEATURES.md` - List of enhanced AI features

- **QMOI Space**
  - `/qmoi-space/` - Main QMOI Space directory
  - `/QMOISPACEDEV.md` - Development and integration docs
  - `/QMOISPACEUI.md` - UI features and serving methods
  - `/QMOISPACE.md` - General space documentation
  - `/QMOIHUGGINGFACESPACES.md` - Hugging Face integration

### QCity Structure Diagram

```
QCity
├── qcity-artifacts/
├── QCITYREADME.md
├── QCITYMAINDEVICE.md
├── QCITYDEVICEAUTOUPGRADE.md
├── QCITYRUNNERSENGINE.md
├── QCITYRESOURCES.md
└── QCITYQMOIAUTOSTART.md
```

### QMOI-AI Structure Diagram

```
QMOI-AI
├── qmoi_ai.py
├── qmoi_ai_launcher.py
├── qmoi_ai_installer.iss
├── qmoi_ai.spec
├── QMOIAICORE.md
├── QMOI_MEMORY.md
├── QMOI-ENHANCED-AUTOTESTS.md
└── QMOI-ENHANCED-FEATURES.md
```

### QMOI Space Structure Diagram

```
QMOI Space
├── qmoi-space/
├── QMOISPACEDEV.md
├── QMOISPACEUI.md
├── QMOISPACE.md
└── QMOIHUGGINGFACESPACES.md
```

## Structure-Specific Documentation

- See `QMOIAICORE.md` for AI core logic and orchestration details
- See `QMOISPACEDEV.md` for QMOI Space development and integration
- See `QCITYREADME.md` for QCity features and activities
- See `QMOI_MEMORY.md` for memory/resource management
- See `QMOI-ENHANCED-AUTOTESTS.md` for automation and self-healing
- See `QMOI-ENHANCED-FEATURES.md` for enhanced AI features
- See `QMOISPACEUI.md` for UI features and serving logic
- See `QMOIHUGGINGFACESPACES.md` for Hugging Face integration

## File Responsibilities

- **Frontend Serving**
  - `/main.js`, `/qmoiexe_enhanced.py` (function: `open_frontend`) - Launches and serves frontend UI
  - `/QMOISPACEUI.md` - Documents all UI features and their serving logic

- **Backend Serving**
  - `/main.py`, `/qmoiexe_enhanced.py` (function: `run_backend`) - Serves backend API and logic
  - `/QMOI_MEMORY.md` - Details backend memory management

- **Automation & Self-Development**
  - `/QMOI-ENHANCED-AUTOTESTS.md` - Automated testing and self-healing
  - `/QMOIAUTODEV.md`, `/QMOIAUTOMAKENEW.md` - Auto-development and project creation
  - `/QMOIAUTOEVOLVE.md` - Auto-evolution logic
  - `/QMOI-ENHANCED-SUMMARY.md` - Summary of enhancements and automation

- **Permanent Operation & Resource Management**
  - `/QMOI_MEMORY.md`, `/QMOIENHANCEDAUTOEVOLVINGALLPYTHONENV.md` - Ensures unlimited memory, disk, and resource flexibility
  - `/QMOI-CLOUD.md`, `/QMOI-CLOUD-ENHANCED.md` - Cloud resource management
  - `/QMOIDATABASE.md` - Database management
  - `/QMOIVPNREADME.md` - VPN and network resource management

- **Auto Sign-Up, Registration, and Platform Independence**
  - `/QMOIAUTHBIOMETRICS.md` - Biometric authentication
  - `/QMOIAUTOGMAIL.md` - Gmail and email automation
  - `/QMOIINDEPENDENTQMOI.md` - Features for platform independence
  - `/QMOICLONEGITHUB.md`, `/QMOICLONEGITLAB.md`, `/QMOICLONEHUGGINGFACE.md` - Auto-cloning and platform integration

- **Revenue Generation & Income**
  - `/QMOIREVENUEGENERATION.md`, `/QMOI-REVENUE-README.md`, `/QMOIAUTOREVENUEEARN.md` - Revenue and income automation

## Reference Automation

See `ALLERRORS.md` for the latest automated error/issue logs and autofix status.

<!-- QMOI_VALIDATION_START -->

{
"file": "ALLSYSTEMSSTRUCTURESREFERENCES.md",
"validated_at": "2025-10-26T20:51:22.280220Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "ALLSYSTEMSSTRUCTURESREFERENCES.md"
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

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
