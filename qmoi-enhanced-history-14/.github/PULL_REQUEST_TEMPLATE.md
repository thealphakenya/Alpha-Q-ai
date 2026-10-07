<!-- Describe the purpose of this PR in one sentence -->

## Summary

This PR contains production-enablement changes for the local `qmoi` development server and supporting automation: model enforcement, optional SQLite memory, sync authentication, supervisor/service artifacts, scheduled memory-sync workflow, docs, and release helpers.

## What changed

- Enforce `qmoi` as default model (allow override via `QMOI_ALLOW_MODEL_OVERRIDE=1`).
- Optional SQLite memory backend (enable `QMOI_USE_SQLITE=1`) with migration from `qmoi_memory.json`.
- `/sync/*` endpoints protected by optional `QMOI_SYNC_API_KEY`.
- Supervisor + systemd example for qvillage under `deploy/qvillage/`.
- Scheduled sync workflow `.github/workflows/qmoi-sync-memory.yml` (requires repo secrets).
- Release helper and master scripts for installing the service and uploading release assets.

## Notes for reviewers

- This PR removes large downloaded app artifacts from the repository and adds `.gitignore` rules; release artifacts should be published to GitHub Releases or object storage instead of committing to git.
- CI workflow will be a no-op until secrets are configured (see `SECRET_SETUP.md`).

## Security considerations

- Do not merge until repo secrets are provisioned by a repo master if you want scheduled sync to run.
- Review `QMOI_SYNC_API_KEY` usage: it's a simple bearer token check for development; for production, integrate with your auth system.

## How to test

1. Start the server locally: `python3 scripts/qmoi_local_server.py &`
2. Run curl examples from `CURLQMOIMASTERSISTERUSER.md`.
3. (Optional) Enable SQLite mode: `export QMOI_USE_SQLITE=1` and restart server — verify `qmoi_memory.db` contains conversations.

## Checklist

- [ ] Secrets provisioned (GH/HF tokens)
- [ ] Release artifacts moved to Releases or object storage
- [ ] Service install tested on staging host

## General PR checklist

- [ ] Tests pass locally (`npx jest --config=jest.config.cjs -i --runInBand --colors --verbose`)
- [ ] CI build passes (`npm run ci:build`)
- [ ] Coverage report generated and attached as an artifact
- [ ] Changes documented in `CONTRIBUTING.md` / `START.md` if relevant
- [ ] MSW-related test changes include notes about `__MSW_READY__` and absolute URL handlers (if applicable)

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
