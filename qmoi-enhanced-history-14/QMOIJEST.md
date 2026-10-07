---
title: "QMOIJEST"
qmoi_validation_frontmatter: true
---

# QMOIJEST

## QMOI Jest Guide

Purpose: provide a concise, practical Jest setup for this repository (TypeScript + mixed JS/TS UI code, multi-package layout). The doc contains a recommended root config, CI snippets, test patterns, and integration notes for the autodev/autotest pipeline.

### Quick contract

- Inputs: source files (TS/JS/TSX/JSX) across repo and package workspaces, tests following patterns: `**/*.test.*`, `**/*.spec.*`, `**/*.integration.test.*`.
- Outputs: test results (exit code), coverage reports (lcov and JSON), optional snapshot diffs.
- Error modes: failing tests (non-zero exit), missing snapshots flagged, coverage thresholds exceeded.

### What we found in this repo

- Multiple package.json files contain `jest` devDependency entries and test scripts. There are existing test files like `src/hooks/useQmoiKernel.test.ts` and integration tests under `src/components/...integration.test.tsx`.
- Some validation and generated folders (e.g. `.qmoi_validation/` or `node_modules/`) pollute scans — those should be excluded from run-sets.

### Recommended root Jest configuration

Create a root `jest.config.cjs` (example included in this repo) and adapt per-package configs for specific needs. The root config is intentionally conservative and works with TypeScript via `ts-jest`.

Rationale:

- Single source of truth for CI runs.
- Supports per-package overrides via `projects` or local `jest.config.*` files.

### Running tests locally

- From repo root (if you use npm/yarn workspaces): `npm test` or `npx jest --coverage`.
- Recommended flags for local dev: `--watch --watchAll=false --findRelatedTests`.

### CI recommendations (GitHub Actions snippet)

Use a job that checks out code, installs deps, runs jest with coverage and fails on coverage thresholds. Example snippet (adapt to your CI runner):

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install
        run: npm ci
      - name: Run tests
        run: npx jest --coverage --runInBand
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: ./coverage/lcov.info
```

Notes:

- `--runInBand` is safe on CI but slows execution; remove it on runners with multiple cores and allow Jest to parallelize.

### Performance & parallelization

- Use Jest caching (default) and `--maxWorkers` to control CPU usage (e.g., `--maxWorkers=50%`).
- For large monorepos, run tests per package in parallel using CI matrix or `projects` entries in Jest config.

### Snapshot & test data hygiene

- Keep snapshots in the same repo and review snapshot updates carefully.
- Add `--updateSnapshot` only when intentionally updating.

### Coverage and quality gates

- Set sensible coverage thresholds in `jest.config.cjs` (example has a moderate threshold). Keep coverage gating in CI to prevent regressions.

### Integration with autodev/autotest pipeline

- Add a Jest step to `tools/autotest_runner.py` to run `npx jest --coverage --silent --colors=false` and write results to `tools/jest_results.json` (or use `--json --outputFile=...`).
- Use test results to gate auto-promote or canary rollout in the autodev flow.

### Edge cases and notes

- Exclude generated and vendor directories from patterns: `.qmoi_validation/`, `node_modules/`, `dist/`, `build/`.
- If monorepo uses workspaces, prefer running tests per workspace for quicker incremental runs.

### Next steps (low-risk)

1. Add/confirm `jest.config.cjs` at the repo root (we added a conservative example alongside this doc).
2. Add a small `jest.setup.js` for common test setup (e.g., `@testing-library/jest-dom`).
3. Wire a Jest run step into `tools/autotest_runner.py` that produces JSON output for automation.
4. Triage `tools/link_report.md` and `matches.json` to exclude generated artifacts and reduce noise for test/scan jobs.

If you want, I can now:

- add a small `jest.setup.js` and wire the `tools/autotest_runner.py` to run jest and collect JSON results, then run it (may be slow depending on repo size).

-- QMOI Automation

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
