---
title: "Workspace / Codespace / QCity — Minimize Device Data Bundles (Enhanced)"
qmoi_validation_frontmatter: true
---

# Workspace / Codespace / QCity — Minimize Device Data Bundles (Enhanced)

This document describes practical strategies and architecture patterns to make the workspace and its apps use minimal on-device data (mobile/limited-bundle devices) while leveraging cloud/qcity resources for performance and features.

Principles
- Offline-first, delta-synced: keep a small local cache and sync only diffs. Use ETags, range requests, and compressed deltas.
- Compute-offload: prefer remote inference / heavy compute on qcity/cloud nodes and stream results.
- Compact formats: use binary/compact serialization (msgpack, protobuf) for sync payloads, gzip or brotli for transfers.
- Prioritize metadata: synchronize lightweight metadata first (indices, manifest) and lazy-load heavy assets on-demand.
- Throttling & scheduling: allow background sync over Wi‑Fi or when device is idle/plugged in; provide user-configurable low-data mode.

Recommended components
- qcity-edge-proxy: small agent that negotiates bandwidth-efficient sync with central qcity servers.
- delta-storage: store content-addressed deltas and reconstruct locally when needed.
- smart-cache: LRU cache with size/age policies adapting to device/bundle settings.

Usage guidelines
- Default to minimal datasets for on-device operations; larger datasets are fetched on-demand.
- Keep model sizes small for on-device models; prefer offloading to qcity with cached quantized weights.
- Use resumable downloads and prioritized queues to avoid re-transfers.

Implementation notes (next steps)
1. Add an agent that negotiates low-data sync settings and exposes a config file in `qc/` or `config/`.
2. Add server-side support in qcity to return compact deltas and pre-computed artifacts for low-bandwidth clients.
3. Integrate with the existing `QMOI` sync infrastructure and document the policy in `QCITYRESOURCES.md` and `QMOI-CLOUD-ENHANCED.md`.

See also: `docs/OFFLINE_FIRST_ARCHITECTURE.md`, `QCITYRESOURCES.md`, `QMOI-CLOUD-ENHANCED.md`.

Generated: tools/find_[AUTOFIXED by Ollama at 2026-07-26T18:54:39.576470Z]s.py scan run

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
