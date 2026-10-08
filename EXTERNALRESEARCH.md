# External Research

<!-- BEGIN QMOI MANAGED: external-surface-research -->
## Agent-managed external research coverage

- Research status: `PLANNED_NOT_VISITED`; planned resources: `18`; successful visits: `0`.
- The surface audit manifest and source hashes are in `QMOItracks/repository_surface_audit.json`; the report is excluded from its own digest.
- Resources are fetched only when explicitly enabled in an authorized GitHub-hosted run; plans are never visit evidence.
- Adoption remains gated by license, code/model availability, reproducible benchmarks, accuracy/speed/RAM/GPU/bandwidth/cost/reliability measurements, security, focused regression tests, rollback, and exact-SHA review.

| Topic | Official source | Visit status | Content SHA-256 |
| --- | --- | --- | --- |
| `github-actions-auth` | `https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication` | `PLANNED_NOT_VISITED` | `` |
| `github-rest-api` | `https://docs.github.com/en/rest` | `PLANNED_NOT_VISITED` | `` |
| `python-testing` | `https://docs.pytest.org/en/stable/` | `PLANNED_NOT_VISITED` | `` |
| `QMOI-runtime` | `https://docs.QMOI.com/` | `PLANNED_NOT_VISITED` | `` |
| `application-security` | `https://cheatsheetseries.owasp.org/` | `PLANNED_NOT_VISITED` | `` |
| `python-packaging` | `https://packaging.python.org/en/latest/` | `PLANNED_NOT_VISITED` | `` |
| `container-builds` | `https://docs.docker.com/` | `PLANNED_NOT_VISITED` | `` |
| `javascript-packages` | `https://docs.npmjs.com/` | `PLANNED_NOT_VISITED` | `` |
| `vercel-deployment` | `https://vercel.com/docs` | `PLANNED_NOT_VISITED` | `` |
| `netlify-deployment` | `https://docs.netlify.com/` | `PLANNED_NOT_VISITED` | `` |
| `accessibility` | `https://www.w3.org/TR/WCAG22/` | `PLANNED_NOT_VISITED` | `` |
| `http-semantics` | `https://www.rfc-editor.org/rfc/rfc9110` | `PLANNED_NOT_VISITED` | `` |
| `gitlab-ci` | `https://docs.gitlab.com/ee/` | `PLANNED_NOT_VISITED` | `` |
| `model-hosting` | `https://huggingface.co/docs` | `PLANNED_NOT_VISITED` | `` |
| `model-evaluation` | `https://huggingface.co/docs/evaluate/index` | `PLANNED_NOT_VISITED` | `` |
| `huggingface-research` | `https://huggingface.co/docs/hub/index` | `PLANNED_NOT_VISITED` | `` |
| `statistical-methods` | `https://www.itl.nist.gov/div898/handbook/` | `PLANNED_NOT_VISITED` | `` |
| `financial-controls` | `https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/index.htm` | `PLANNED_NOT_VISITED` | `` |
<!-- END QMOI MANAGED: external-surface-research -->

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
