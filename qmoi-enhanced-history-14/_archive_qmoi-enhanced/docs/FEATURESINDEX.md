---
title: "QMOI Features Master Index"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI Features Master Index

| Feature/Integration     | Description                                      | Documentation File         |
| ----------------------- | ------------------------------------------------ | -------------------------- |
| Handsfree All Devices   | Control any device handsfree, accessibility      | QMOIALLDEVICESHANDSFREE.md |
| Enhanced QVS Security   | Device/network sandboxing, masking, VPN          | ENHANCEDQVS.md             |
| VPN                     | Always-on, privacy, Colab/Dagshub support        | QVPNREADME.md              |
| Network Masking         | [AUTOFIXED by Ollama at 2026-07-26T18:54:39.696555Z]_PROD/unreal IPs, privacy-first              | QMOIMASKS.md               |
| Network Optimization    | Secure, optimized, auto-connect                  | QMOINETWORK.md             |
| Alpha QMOI Engine       | All integrations/platforms auto-handled          | ALPHAQMOIENGINE.md         |
| Accounts & Platforms    | Auto-create/register accounts, track credentials | QMOIACCOUNTSPLATFORMS.md   |
| Qcity Device            | Lightweight, handsfree, log/data management      | QCITYREADME.md             |
| Accessibility Settings  | High-contrast, large text, voice/gesture, etc.   | (see UI panel)             |
| Device Integrations     | TV, car, smart home, WhatsApp, Colab, Dagshub    | DeviceIntegrationStubs.ts  |
| Auto-update/Auto-evolve | Self-updating, self-enhancing, auto-fixing       | (core system, see docs)    |

## See also

- [README.md](qmoi-enhanced/README.md)
- [QMOI-ENHANCED-README.md](qmoi-enhanced/QMOI-ENHANCED-README.md)
- [QMOI-FEATURE-INDEX.md](qmoi-enhanced/QMOI-FEATURE-INDEX.md)
- [QMOIALLDEVICESHANDSFREE.md](qmoi-enhanced/QMOIALLDEVICESHANDSFREE.md)
- [ENHANCEDQVS.md](qmoi-enhanced/ENHANCEDQVS.md)
- [QVPNREADME.md](qmoi-enhanced/QVPNREADME.md)
- [QMOIMASKS.md](qmoi-enhanced/QMOIMASKS.md)
- [QMOINETWORK.md](qmoi-enhanced/QMOINETWORK.md)
- [ALPHAQMOIENGINE.md](qmoi-enhanced/ALPHAQMOIENGINE.md)
- [QMOIACCOUNTSPLATFORMS.md](qmoi-enhanced/QMOIACCOUNTSPLATFORMS.md)
- [QCITYREADME.md](qmoi-enhanced/QCITYREADME.md)

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/docs/FEATURESINDEX.md",
"validated_at": "2025-10-26T20:51:24.857443Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI Features Master Index"
},
{
"name": "links",
"ok": true,
"detail": [
{
"label": "README.md",
"target": "../README.md",
"ok": true
},
{
"label": "QMOI-ENHANCED-README.md",
"target": "../QMOI-ENHANCED-README.md",
"ok": true
},
{
"label": "QMOI-FEATURE-INDEX.md",
"target": "../QMOI-FEATURE-INDEX.md",
"ok": true
},
{
"label": "QMOIALLDEVICESHANDSFREE.md",
"target": "../QMOIALLDEVICESHANDSFREE.md",
"ok": true
},
{
"label": "ENHANCEDQVS.md",
"target": "../ENHANCEDQVS.md",
"ok": true
},
{
"label": "QVPNREADME.md",
"target": "../QVPNREADME.md",
"ok": true
},
{
"label": "QMOIMASKS.md",
"target": "../QMOIMASKS.md",
"ok": true
},
{
"label": "QMOINETWORK.md",
"target": "../QMOINETWORK.md",
"ok": true
},
{
"label": "ALPHAQMOIENGINE.md",
"target": "../ALPHAQMOIENGINE.md",
"ok": true
},
{
"label": "QMOIACCOUNTSPLATFORMS.md",
"target": "../QMOIACCOUNTSPLATFORMS.md",
"ok": true
},
{
"label": "QCITYREADME.md",
"target": "../QCITYREADME.md",
"ok": true
}
]
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
