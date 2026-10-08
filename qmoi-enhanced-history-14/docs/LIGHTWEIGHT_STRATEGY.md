---
title: "QMOI Lightweight Application Strategy"
qmoi_validation_frontmatter: true
---

# QMOI Lightweight Application Strategy

Goal: Keep QMOI applications and artifacts as small and efficient as possible while retaining full functionality and graceful fallbacks when cloud features or external providers are unavailable.

Principles

- Local-first: prefer local models, local artifact store (`.qvs`) and low-dependency runtimes.
- Optional cloud: cloud integrations are optional; default to simulated/local implementations if cloud is unavailable.
- Lazy loading: load heavy modules only when needed.
- Minimal runtime: prefer pure-Python or small WASM bindings for inference, avoid large native dependencies in client apps.
- Quantized models: use quantized, small footprint checkpoints for offline inference.
- Offload large assets: move large datasets, checkpoints, and media into `QVS` or optional cloud buckets; keep repo lightweight.
- Strip assets: provide utilities to locate and optionally compress or move large files out of the application tree.

Techniques and Implementation

1. QVS (QMOI Virtual Store)

- Store large files under `.qvs/` outside the code path and index them; QVS is already implemented in `lib/qvs.py`.
- Use `put()` to store large model checkpoints and mark them as optional for clients.

2. Lazy module loading

- For features that require heavy libraries (Torch, TensorFlow), wrap imports in factory functions and load only when the feature is invoked.

3. Simulation/fallback

- Device integrations include lightweight simulated implementations so apps can run without hardware or cloud keys.
- Environment flags to force local-only behavior: `QMOI_DISABLE_CLOUD=1`, `QMOI_DISABLE_HW=1`.

4. Model size reduction

- Prefer quantized model formats and compact runtimes (ONNX, TFLite, or WASM-based inference).
- Provide small distilled models for typical client tasks and optional larger models for server deployments.

5. Asset stripping tool

- Scripts are provided to scan for large files (by size) and either compress them or move them to `.qvs/`.

6. Packaging

- Keep client npm packages minimal: avoid bundling heavy ML libs in browser/edge SDKs.
- Use feature flags to only include heavy modules in server-side builds.

Operational Guidance

- During CI, run `scripts/strip_large_files.py --threshold 10MB --report large_files.json` to find large assets.
- Review `large_files.json` and offload eligible files using `lib/qvs.put()` or move to artifacts storage.
- Monitor repository size and prune old model checkpoints.

Security & Privacy

- Sensitive credentials should never be stored in `.qvs/` or repo; use secrets management.
- Access to optional cloud stores must be controlled by the deployment environment and defaults must be local-first.

Notes

- The lightweight strategy emphasizes safe defaults: the system works (in simulated mode) even when external cloud models or APIs are unavailable.
- LION orchestrator should manage fallbacks, automatic offloading, and resource-aware scheduling when heavy operations are requested.

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/LIGHTWEIGHT_STRATEGY.md",
"validated_at": "2025-10-26T20:51:22.689199Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI Lightweight Application Strategy"
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
