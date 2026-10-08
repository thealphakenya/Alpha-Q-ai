**Release Maintenance**

- **Purpose**: Keep GitHub release assets in sync with `release_assets_manifest.json`.

- **Workflows** (`.github/workflows/sync-releases-from-manifest.yml`):
  - **sync-draft** (always runs): Regenerates manifest and syncs to a draft release (safe mode).
    - On tag pushes: uses the tag name as the release tag.
    - On schedule/dispatch: uses commit hash as the draft release tag.
    - Draft releases stay unpublished until manually published on GitHub or via `--publish` flag.
  - **sync-all-releases** (on-demand via dispatch): Syncs assets to all existing published releases (one-time/maintenance).

- **Local commands**:
  - Regenerate manifest: `python3 scripts/generate_release_manifest.py`
  - Dry-check releases: `python3 scripts/check_github_releases.py`
  - Sync to draft release (safe): `python3 scripts/sync_to_draft_release.py [--tag TAG] [--publish]`
  - Sync to all published releases (one-time): `GITHUB_TOKEN="ghp_..." python3 scripts/sync_all_releases.py`
  - Backup before uploads: `gh release download <tag> --repo owner/repo --dir reports/releases_backup/<tag>`

- **Safety & Flow**:
  - Default: assets are synced to **draft** releases (unpublished) for review.
  - Approve and publish via GitHub UI or pass `--publish` flag to script.
  - Existing backups are saved in `reports/releases_backup/<tag>/` before any replacements.

- **Token**: GitHub PAT maintained in `CREDENTIAL_ROTATION_PLAYBOOK.md`. Workflows use `GITHUB_TOKEN` secret.

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
