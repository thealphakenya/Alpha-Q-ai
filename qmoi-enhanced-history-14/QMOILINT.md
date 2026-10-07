---
title: "QMOI Linting & AutoDev Guidelines"
qmoi_validation_frontmatter: true
---

# QMOI Linting & AutoDev Guidelines

This document describes the linting and autofix strategy used by the QMOI project.

Goals

- Maintain a consistent code style across languages (Python, TypeScript/JavaScript).
- Provide safe automatic fixes where possible (docs, trivial code stubs) while requiring manual review for risky changes.
- Integrate linting into the Autotest / Validation pipeline so lint checks and autofixes run automatically in CI and on developer machines.

Principles

- Conservative: automatic fixes are applied only when the change is unambiguous (for example, formatting fixes, reorder imports, replacing 'pass' with explicit NotImplementedError when associated with a [AUTOFIXED by Ollama at 2026-07-26T18:54:39.534997Z] comment).
- Auditable: all automated fixes are emitted as draft patches under `tools/patches/` and as commits on a review branch when approved.
- Low-bandwidth aware: linters and autofix runners avoid downloading heavy dependencies locally. CI is used to run full JS/TS linters when Node is not available locally.

Local tooling strategy

- Python linting: use `flake8` and `autoflake` if installed in the Python environment. The `tools/qmoi_lint.py` helper will detect these and run them. It will write `tools/qmoi_lint_report.json` and a human-readable `tools/qmoi_lint_report.md`.
- JS/TS linting: the repository provides an ESLint configuration `.eslintrc.cjs` and `package.json` scripts can be added. Locally the lint runner will attempt `npm exec --no-install eslint` or `npx eslint`; if Node is missing the runner will skip JS/TS linting and instruct CI to run it.

CI integration

- The CI workflow (GitHub Actions) will run `python3 tools/qmoi_lint.py --ci` which will install or use the environment and run full autofix where safe and report results. The CI job will upload `tools/qmoi_lint_report.*` artifacts for review.

Autofix policy

- `--fix` is only run on code paths that are low-risk: formatting, import ordering, small doc replacements.
- For higher-risk files, the lint runner will create draft patches instead of applying fixes.

Extensibility

- Add new language linters by updating `tools/qmoi_lint.py` and adding language-specific config files and CI steps.

See also: `tools/qmoi_lint.py`, `tools/process_allrefs.py`, `tools/autotest_runner.py` and `tools/validate_system.py`.

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
