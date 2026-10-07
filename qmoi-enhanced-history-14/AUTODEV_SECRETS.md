---
title: "QMOI — Required Secrets and Local .env Guidance"
qmoi_validation_frontmatter: true
---

# QMOI — Required Secrets and Local .env Guidance

This file documents the secret names expected by QMOI and how to provide them
for CI and local development. The canonical manifest is `required_secrets.json`.

Required secrets

- `GITHUB_TOKEN` — GitHub token used by CI and release automation (required)
- `GITHUB_REPO` — Owner/repo for release automation (required), e.g. `thealphakenya/qmoi-enhanced`
- `QMOIN_NOTIFY_HMAC_SECRET` — HMAC secret used to sign outbound notifications (required)

Optional secrets (examples)

- `PYPI_API_TOKEN` — PyPI API token for publishing wheels
- `DOCKERHUB_USERNAME` / `DOCKERHUB_PASSWORD` — DockerHub credentials for image pushes
- `NPM_TOKEN` — npm token for publishing JS SDKs
- `MAVEN_USERNAME` / `MAVEN_PASSWORD` — Maven repo credentials
- `QMOI_DB_ENCRYPTION_KEY` — Optional DB encryption key for production DBs

Where to set these

- GitHub Actions: add repository secrets under Settings → Secrets and variables → Actions.
  Use the exact names above (e.g. `GITHUB_TOKEN`, `QMOIN_NOTIFY_HMAC_SECRET`).
- Locally (development): create a `.env` file in the project root with KEY=value pairs.
  The repository includes a generated `.env.example` you can copy and fill.

Quick local setup

1. Copy the example file:

```bash
cp .env.example .env
# Edit .env and fill required values (especially QMOIN_NOTIFY_HMAC_SECRET and GITHUB_TOKEN/GITHUB_REPO)
```

2. Make `.env` readable only by you (optional but recommended):

```bash
chmod 600 .env
```

CI enforcement

- The release workflow (`.github/workflows/release.yml`) runs the env check step:

```yaml
- name: Validate required secrets
  run: python scripts/env_manager.py --check
```

This step ensures required secrets are present and fails the job with a clear message
if they are missing.

Advanced: automated secret injection

- For production-grade setups, consider using your cloud provider's secret manager
  (AWS Secrets Manager, Azure Key Vault, or HashiCorp Vault). The env manager is
  manifest-driven and could be extended to fetch secrets from those providers.

Questions or next steps

- Want me to add the same check to more CI workflows? I can add a small job-step
  to other workflows such as `ci.yml` or `build.yml` on request.

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
