---
title: "QMOI Autodev & Release Automation (developer instructions)"
qmoi_validation_frontmatter: true
---

# QMOI Autodev & Release Automation (developer instructions)

Generated: 2025-10-26T

This file gathers recommended developer commands, test runners, build steps and the automated flows QMOI will use to maintain, validate and publish artifcats. It contains the minimal steps to let QMOI (the repo AI & LION orchestrator) autonomously validate, propose releases and — when authorised — publish them.

## Key scripts

- `scripts/generate_allmdrefs.py` — discover all `.md` files and update `ALLMDFILESREFS.md` (use `--write` to apply changes).
- `scripts/validate_md.py` — validate markdown files, produce per-file JSON reports in `.qmoi_validation/validation_reports/` and optionally insert validation blocks with `--apply`.
- `scripts/qmoi_todos.py` — lightweight todo manager used by validation and release scripts to create remediation tasks.
- `scripts/collect_build_scripts.py` — scan for build scripts and manifests.
- `scripts/register_app_build.py` — discover apps/artifacts and optionally copy artifacts into `ALL_APPS/` with `--copy`.
- `scripts/validate_builds.py` — checks discovered apps for expected artifacts and writes reports to `.qmoi_validation/build_validation_reports/`.
- `scripts/release_automation.py` — create release proposals from passed build validations and optionally publish to GitHub when `GITHUB_TOKEN` & `GITHUB_REPO` env vars are provided.

## Quick-run (recommended order)

1. Discover all MD files and update refs (safe):

```bash
python3 scripts/generate_allmdrefs.py --write
```

2. Run markdown validations (dry-run first):

```bash
python3 scripts/validate_md.py
# Inspect .qmoi_validation/validation_reports/
```

3. After review, insert validation metadata blocks (batch or per-file):

```bash
python3 scripts/validate_md.py --apply --create-todos --lion
```

4. Discover & register builds/apps (dry-run):

```bash
python3 scripts/collect_build_scripts.py
python3 scripts/register_app_build.py
```

5. Validate build artifacts:

```bash
python3 scripts/validate_builds.py
# Inspect .qmoi_validation/build_validation_reports/
```

6. Propose and optionally publish releases:

```bash
# Generates proposal JSON files under .qmoi_validation/releases_proposals/
python3 scripts/release_automation.py

# To publish (requires env vars):
export GITHUB_TOKEN=...  # scoped token with repo:release
export GITHUB_REPO=owner/repo
python3 scripts/release_automation.py --publish
```

## Autodev & LION integration notes

- QMOI (the AI) and LION (orchestrator) work together by writing machine-readable stubs into `.qmoi_validation/lion_tasks/` and `.qmoi_validation/` reports. When validations fail, `validate_md.py` and `validate_builds.py` can auto-create todos and LION task stubs to remediate.
- LION is used to schedule and route remediation tasks. QMOI uses past validation history (`.qmoi_validation/history/`) to decide remediation strategies (retry, create task, escalate).
- For full automation: authorize a dedicated bot account with a minimal `GITHUB_TOKEN` and set `GITHUB_REPO`. QMOI will only publish when `--publish` is given.

## Tests and CI

- Add unit tests for `scripts/validate_md.py` and `scripts/qmoi_todos.py` under `tests/` using pytest. Minimal tests to add:
  - validator reads file and returns checks structure for a small sample.
  - todo add/list/run flows operate on a temp `.qmoi_validation`.

- CI pipeline (GitHub Actions) should run discovery, validation (dry-run), build discovery and build validation. A manual approval step should gate `release_automation.py --publish`.

## Autodev best-practices (what QMOI will do automatically)

- Non-destructive first: QMOI runs discovery and validations in dry-run, creates proposals and todos, and waits for approval to apply changes or publish releases.
- When authorised, QMOI will:
  - insert validation metadata blocks into `.md` files in batches,
  - create remediation todos for missing artifacts,
  - propose GitHub Releases and publish after human or automated approval.
- QMOI will prefer lightweight artifacts (PWAs, wheels, wasm when possible) and tag releases with `pwa` or `apk` in release notes when those artifacts are present.

## Commands summary

All-in-one quick run (safe, review after each step):

```bash
python3 scripts/generate_allmdrefs.py --write
python3 scripts/validate_md.py
python3 scripts/validate_builds.py
python3 scripts/release_automation.py
```

## Where to extend

- To add automatic uploads of release artifacts, extend `scripts/release_automation.py` to collect artifacts and upload them to the GitHub release `upload_url`. Keep `--publish` gated behind env var checks.
- To enable fully autonomous publishing, configure a GitHub Actions workflow that runs the pipeline, and grant the run a minimal publish token only on a protected branch.

## Contact points in code

- `.qmoi_validation/` — validation artifacts, history, and LION task stubs.
- `scripts/qmoi_todos.py` — add/edit tasks used by validators.
- `scripts/register_app_build.py` — canonicalizes apps/artifacts for release.

---

End of autodev instructions.

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
