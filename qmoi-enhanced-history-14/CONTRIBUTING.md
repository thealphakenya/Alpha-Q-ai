# Contributing & Developer Notes

Thanks for contributing to QMOI! This file contains quick tips for running the dev environment and tests, and troubleshooting MSW-related test issues.

## Quick dev & test commands

- Dev server: `npm run dev` (local: http://localhost:3000)
- Dev health check: `npm run dev:health`
- Run tests: `npx jest --config=jest.config.cjs -i --runInBand --colors --verbose`
- CI-style build: `npm run ci:build`

## MSW & testing guidance

- MSW is initialized at test time via `src/setupTests.ts` and exposes a readiness promise at `globalThis.__MSW_READY__`.
- Tests should await `__MSW_READY__` or install handlers deterministically per test to avoid races.
- If you encounter unhandled requests during tests, enable `SHOW_MSW_UNHANDLED=1` to surface the origin.
- Use `TEST_VERBOSE=1` for additional handler/request debug output when diagnosing request shape mismatches (path-only vs absolute URL), or to inspect whether handlers are being selected properly.

## Troubleshooting

- `UNHANDLED REQUEST: GET http://localhost/api/...` usually means handlers are registered only as path-only (`/api/...`) while the test runtime produced an absolute URL; add both path and absolute variants when necessary.
- If you see `response.headers.get is not a function`, ensure handlers return a real `Response` when not using `ctx` helpers, or use `res(ctx.status(...), ctx.json(...))` when `ctx` is available.

## Making PRs

- Open a branch, push, and create a PR targeting the default branch (`autosync-backup-20250926-232440`) or `upgrade/next-15` for this migration work.
- The `CI Build and Tests` workflow (`.github/workflows/ci.yml`) will run the build and test suite on push/PR.

### PR checklist

- Ensure tests pass locally (`npx jest --config=jest.config.cjs -i --runInBand --colors --verbose`).
- Ensure the CI build passes (`npm run ci:build`) before merging.
- The CI workflow now generates a coverage report and uploads it as an artifact; check the workflow run for `coverage-report` artifacts.
- Use the PR template to include a summary and verify the checklist is completed.

Thank you — and welcome to the project! If you'd like me to add a short automation for generating a PR checklist or a PR template, I can add that next.

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
