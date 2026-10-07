---
title: "QMOI Orchestrator"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# QMOI Orchestrator

This document explains the orchestrator scaffold included in the repository.

Key features:

- `qmoi_orchestrator.py`: supervises `start_qmoi_ngrok.py`, periodic autotests, auto-fixers, backups and build driver.
- `qmoi_build_all.py`: basic driver that scans the repo for known build markers and reports/builds.
- `deploy/qmoi-orchestrator.service`: systemd template (place in `/etc/systemd/system/` and adjust `WorkingDirectory`/`User`).

Important safety notes:

- This is a conservative scaffold: many repo files still contain [AUTOFIXED by Ollama at 2026-07-26T18:54:39.614912Z]s and partial scripts. Review build steps before enabling `--apply` or deploying to production.
- Secrets must be provisioned securely to runners (use keyring, GitHub Secrets, or a cloud KMS). Do not store raw secrets in the repository.

Quick start (development):

```bash
# dry-run orchestrator
python qmoi-enhanced/qmoi-enhanced/qmoi_orchestrator.py --dry-run

# install as systemd service (example)
# copy repository to /opt/qmoi, edit deploy/qmoi-orchestrator.service to set User and WorkingDirectory
# sudo cp deploy/qmoi-orchestrator.service /etc/systemd/system/qmoi-orchestrator.service
# sudo systemctl daemon-reload
# sudo systemctl enable --now qmoi-orchestrator.service
```

Next steps to make this production-ready:

- Replace [AUTOFIXED by Ollama at 2026-07-26T18:54:39.614912Z] auto-fixer script references with concrete fixers.
- Integrate with managed secret stores and add transient token fetchers for CI/runners.
- Replace the passive build driver with per-platform build pipelines and signing workflows.

## QCity Deployment and Runners

This repository includes a pattern for deploying the Orchestrator into QCity (our runner fleet). QCity runners are treated as disposable, identity-managed execution nodes. The orchestrator should be deployed to each QCity runner with the following properties:

- Minimal local state: keep `.qmoi/` for encrypted artifacts and logs; push backups to external store (S3/GCS) regularly.
- Secure secrets: use repo/organization secrets for CI; for QCity runners use ephemeral credentials or node identity to fetch secrets from a central secrets manager.
- Self-healing service: configure a supervisor (systemd, Docker restart policy, or a process manager) to restart the orchestrator on failure.

Recommended flow for QCity deployment:

1. Provision runner base image with Python 3.11, virtualenv, and OS packages.
2. Use the included `deploy/qcity/deploy_orchestrator_qcity.sh` script to bootstrap the orchestrator and systemd unit.
3. Configure the runner to fetch `QMOI_MASTER_KEY` from a secure store (or use the OS keyring) on startup.
4. Configure the runner to register with the centrally-managed runner registry (if you use one) so workflows can target it.

## Runner sync strategy

To keep workflows and runners in sync:

- Use a central 'runner manifest' (e.g. `.qmoi/runner_manifest.json`) describing runner roles and available capabilities (build-mac, build-win, etc.). The orchestrator will read this manifest and only execute tasks that match the runner's capabilities.
- Update manifest centrally and propagate to runners via a secure channel (e.g., signed manifest or pull from S3/registry).
- Workflows should reference runner capabilities, and fallback to other runners if a capability is missing.

## Workflow resilience

Workflows should be designed to be idempotent and retry-friendly. The orchestrator provides a retry wrapper for critical tasks and logs results into `.qmoi/reports/` so that if a runner fails, another runner can pick up the task.

Example: When a build job runs, the orchestrator will:

1. Lock the build manifest entry locally.
2. Run the build script (dry-run first), then apply.
3. Publish artifacts to a remote registry and record the artifact checksum in `.qmoi/reports/builds.json`.
4. If push fails, the orchestrator will retry with exponential backoff and escalate if it exhausts retries.

See `deploy/qcity/qcity_runners.md` for detailed runner bootstrap steps and `deploy/qcity/deploy_orchestrator_qcity.sh` for a bootstrap script.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/QMOI_ORCHESTRATOR.md",
"validated_at": "2025-10-26T20:51:24.815314Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI Orchestrator"
},
{
"name": "links",
"ok": true,
"detail": []
}
],
"passed": true,
"summary": {
"total_checks": 2,
"passed": true
}
}

<!-- QMOI_VALIDATION_END -->

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
