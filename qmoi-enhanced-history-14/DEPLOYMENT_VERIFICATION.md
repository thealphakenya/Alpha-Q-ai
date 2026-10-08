# Deployment verification manifest

## Policy
- The Ollama autonomous agent must verify deployment configuration, environment variables, and official platform documentation before attempting fixes.
- Whenever a deployment fails, the agent should capture the exact error message, identify the likely root cause, and apply the smallest verified fix.
- For Vercel, GitHub Actions, and other host platforms, the agent should prefer the official platform docs and the repository's deployment workflow files over guesswork.

## Detected deployment surfaces
- GitHub Actions: .github/workflows/ci-cd.yml
- GitHub Actions: .github/workflows/deploy.yml
- GitHub Actions: .github/workflows/docker-build-push.yml
- GitHub Actions: .github/workflows/publish-q-alpha.yml
- GitHub Actions: .github/workflows/publish-releases-realtime.yml
- GitHub Actions: .github/workflows/vercel-autofix.yml
- Netlify: netlify.toml
- Vercel: vercel.json, .github/workflows/deploy.yml, .github/workflows/vercel-autofix.yml, app/api/deploy/route.ts

## Verification checklist
- Confirm build and install commands are valid for the current repository state.
- Verify required environment variables are present for the target platform before deployment.
- Check deployment logs and route health after a deploy or redeploy attempt.
- Re-run verification after each fix until deployment health is confirmed.

## Official references
- Vercel: https://vercel.com/docs (Use official Vercel documentation for deployments, redeployments, environment variables, and build settings.)
- GitHub Actions: https://docs.github.com/actions (Use GitHub Actions documentation for workflow reliability, secrets, and deployment automation.)
- Netlify: https://docs.netlify.com/ (Use Netlify docs for deployment configuration, environment handling, and redeploys.)
- Render: https://render.com/docs (Use Render docs for service deployments, health checks, and runtime environment configuration.)
- Railway: https://docs.railway.app/ (Use Railway docs for environment provisioning and staging deployment flows.)
- Fly.io: https://fly.io/docs/ (Use Fly.io docs for app deployment, scaling, and runtime health checks.)

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
