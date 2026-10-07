---
title: "LION Features (detailed)"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:00:00Z
- note: Starter feature doc for LION; expand as implementation progresses

<!-- LION_VALIDATION_END -->

# LION Features (detailed)

This document defines the features and responsibilities of the LION runtime (Lion OS / Lion agent) and how it enhances QMOI across platforms.

1. Purpose and scope
   - LION is a lightweight runtime abstraction that provides:
     - cross-platform installation and lifecycle management for QMOI components
     - an agent that can orchestrate autodev, self-heal, build, telemetry and documentation updates
     - a secure, auditable permission model for any actions that change system state

2. Core APIs
   - Filesystem: read/write with explicit scopes, sandboxing for untrusted operations.
   - Process control: start/stop services, controlled restart/rollback operations.
   - Networking: managed outbound connections, transparent tunneling (ngrok-like) with auditing.
   - Package & updates: fetch/verify packages (signed releases), atomic apply with rollback on failure.

3. Security model
   - Principle of least privilege: agent actions require explicit grants; every high-risk action is logged and requires an allow-list or operator-approved grant.
   - Signed releases: packages are validated by signature before apply.
   - Audit trail: immutable Append-Only logs of permission grants and actions, optionally pushed to a central telemetry collector.

4. Self-heal & autodev features
   - Health checks & recovery: heartbeat + watchdog; auto-restart services with exponential backoff.
   - Auto-PR generation: agent can open PRs for low-risk doc/typo fixes after human review is enabled.
   - Telemetry-driven fixes: parse telemetry, triage issues, and propose fixes; human-in-the-loop approval.

5. Cross-platform independence
   - Agent packaged per-platform (deb/rpm, msi/pkg, docker images, npm for edge) and built in CI.
   - Minimal runtime that allows QMOI services to run in a local sandbox even when remote services are unavailable (graceful degraded mode).
   - Local caches & artifact vault: maintain local copies of critical components to survive network outages.

6. Developer ergonomics
   - `lionctl` CLI to manage installs, builds, and diagnostics.
   - Developer-mode: allow simulated upgrades and test harnesses for patch validation.

7. Privacy & telemetry
   - Telemetry is opt-in: default collects only anonymized metrics for health and failure counts.
   - Explicit user consent required for personally-identifying telemetry or file-level audits.

8. Extensibility & plugins
   - Plugin API for Lion apps to extend UI, add device integrations, or provide custom install scripts.

9. Platform-cloned behavior
   - When the repo is cloned to other platforms or forks, Lion should provide consistent behavior via:
     - `lionctl bootstrap` to prepare the environment
     - `lionctl verify` to validate the local install and docs
     - `lionctl selfheal` to run local self-heal diagnostics

10. Next: implementation artifacts

- `tools/lionctl` (CLI) — scaffolded
- `docs/lion_installers.md` — installer build instructions
- CI workflows: `ci/build-lion-packages.yml` (draft)

This file is a living specification and will be expanded as we implement features.

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/lion_features.md",
"validated_at": "2025-10-26T20:51:24.582586Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "LION Features (detailed)"
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
