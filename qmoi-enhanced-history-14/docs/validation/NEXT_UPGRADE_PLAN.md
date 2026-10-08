# Next.js Upgrade Plan

Goal: Upgrade `next` from ^13.5.0 to the minimal secure version that resolves reported advisories (recommendation: 15.5.8+), verify app compatibility, and remediate related vulnerabilities.

Steps:

1. Create branch: `upgrade/nextjs-major`.
2. Run `npm outdated` and `npm audit` to list current advisories.
3. Update `next` to target version (15.5.8) in `package.json` and run `npm install`.
4. Run the full test suite and `CI=true npm run build`.
5. Fix compile/runtime breakages (likely in middleware, image optimization, or server actions). Refer to Next.js migration guide for 14→15 breaking changes.
6. Update or pin transitive dependencies (some advisories may be indirect and require other updates or replacements).
7. Run `npm audit fix --force` only after manual verification; prefer incremental fixes.
8. Add a CI job to run `npm audit --audit-level=moderate` nightly and create PRs for upgrades via conventional tools (Dependabot or Renovate).

Rollback plan:

- If build or tests fail, revert to pre-upgrade commit and open a PR with the migration changes and a detailed compatibility matrix.

Testing strategy:

- Run existing unit/smoke tests (auth, linting, build). Add specific tests for image optimization paths and middleware behavior where applicable.
- Use a staging environment to perform end-to-end verification before merging to main.

Notes:

- Upgrading Next may be semver-major; schedule maintenance window and coordinate with stakeholders.

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
