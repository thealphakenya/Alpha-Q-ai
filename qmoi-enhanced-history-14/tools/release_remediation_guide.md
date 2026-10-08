# Release Remediation Guide

This guide documents safe, production-ready steps to fix releases that contain [AUTOFIXED by Ollama at 2026-07-26T18:54:45.618177Z] or corrupt assets.

Steps for maintainers
1. Identify flagged releases: `tools/releases_audit.md` lists releases flagged by automated heuristics.
2. For each flagged release tag (e.g., `v1.2.5`):
   - Build or locate the correct binary/artifact per platform (Windows `.exe`, macOS `.dmg`/`.zip`, Linux `.deb`/`.AppImage`, Android `.apk`, iOS `.ipa`).
   - Ensure binaries are signed/reproducible where applicable.
   - Prepare checksums (SHA256) for each artifact.
   - Include proper icons for apps (favicon, platform-specific icons) and a `release_notes.md` describing changes.
3. Upload artifacts to the GitHub release via web UI or the `gh` CLI: `gh release upload <tag> <files...>`.
4. Attach autoupdate metadata where applicable:
   - AppImage: include `update.json` with `version` and `files` entries.
   - Sparkle (macOS): include `.zip` and Sparkle appcast metadata.
   - Windows: include NSIS or Squirrel/WinSparkle metadata if used.
5. Validate release by downloading assets and verifying checksums.
6. Update `tools/releases_audit.md` and close the corresponding issue once remediated.

Automation helpers included in this repo:
- `scripts/audit_releases.py` — flags problematic releases based on heuristics.
- `scripts/create_issues_from_audit.py` — creates GitHub issues (stdlib variant exists as `create_issues_from_audit.py`).

Templates and examples are in `tools/release_templates/`.

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
