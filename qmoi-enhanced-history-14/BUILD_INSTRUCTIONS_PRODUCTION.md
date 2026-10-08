# Production Build & Deployment

This document explains how to build and validate a production-ready artifact for the QMOI Enhanced app.

Prerequisites:

- Node 18 or later
- npm 8 or later
- Docker (for container builds)
- Sufficient RAM (recommended >= 8GB) for building Next.js production artifacts

Quick steps (recommended for CI):

1. npm ci
2. NODE_OPTIONS=--max-old-space-size=8192 npm run build
3. npm run test:coverage --if-present
4. npm run ci:smoke (starts a temporary `next start` and checks key endpoints)

Useful scripts:

- `npm run ci:build` — Build using higher memory limits
- `npm run ci:smoke` — Start a production server and verify a small set of pages and APIs
- `npm run docker:build` — Build a production Docker image using the provided `Dockerfile`
- `npm run serve:static` — Lightweight static server for previewing a minimal page locally

Notes:

- The Next.js build can be memory-intensive and may fail on machines with limited RAM; we run CI on `ubuntu-latest` with increased NODE_OPTIONS to mitigate this.
- If the build worker is SIGTERM'ed locally, run the CI workflow on a hosted runner or a larger machine and review failures in the job logs.

CI:

- A GitHub Actions workflow named `.github/workflows/ci-build.yml` is added to run the build, tests, and smoke checks on push and pull requests.

Docker image & CI publishing 🔧

- A new workflow `.github/workflows/docker-image.yml` builds the production Docker image using Buildx, runs container-based smoke tests, and publishes to GitHub Container Registry (GHCR) when commits are pushed to `main`.
- Image tags published: `ghcr.io/<owner>/<repo>:latest` and `ghcr.io/<owner>/<repo>:<sha>`. The workflow uses the `GITHUB_TOKEN` for authentication and is configured to `push` only when running on `main`.
- To preview locally after CI publishes an image:
  1. docker pull ghcr.io/<owner>/<repo>:latest
  2. docker run -p 3000:3000 --rm ghcr.io/<owner>/<repo>:latest
  3. Visit http://localhost:3000 in your browser.

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
