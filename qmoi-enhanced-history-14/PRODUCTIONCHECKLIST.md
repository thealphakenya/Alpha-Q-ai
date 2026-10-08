---
title: "PRODUCTION CHECKLIST"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

# PRODUCTION CHECKLIST

This checklist is a practical, ordered set of steps and validations to make QMOI production-ready. Treat it as a living doc and re-run checks after any change.

1. Code & Repo
   - [ ] All linting issues fixed for all languages used (Python, JS/TS, Shell, etc.).
   - [ ] Tests: unit & integration tests pass locally and in CI for core services.
   - [ ] Vulnerability scan (dependabot/Snyk) run and critical issues resolved.
   - [ ] All secrets moved to repository secrets or an external secrets store (Vault/KMS).

2. CI/CD & Releases
   - [ ] Workflows are defined and use least-privilege service accounts or `QMOI_TOKEN` secret.
   - [ ] Release automation validated (tag -> build -> publish to artifacts storage).
   - [ ] Canary and rollback strategies are implemented for deploys.

3. Infrastructure & Orchestrator
   - [ ] Orchestrator control-plane deployed to highly-available Linux hosts.
   - [ ] Agents deployed on every runner/host with auto-update enabled.
   - [ ] Persistent storage (Postgres/etcd) with cross-region replication configured.
   - [ ] Autoscaling policies verified (CPU, memory, disk, GPU pools).

4. Observability & Monitoring
   - [ ] Metrics pipelines (Prometheus, Grafana) in place for apps, orchestrator, and runners.
   - [ ] Log aggregation configured (ELK/Fluentd/Cloud Logging).
   - [ ] Alerts for service degradation and automated remediation playbooks exist.

5. Security & Access
   - [ ] Branch protection rules applied to main branches.
   - [ ] Secrets injected at runtime via repo secrets or cloud KMS.
   - [ ] GitHub App and webhooks validated; signature verification implemented.

6. Models & AI
   - [ ] Model storage and versioning verified (artifacts bucket + manifest).
   - [ ] Model inference cluster healthchecks passing and autoscaling verified.
   - [ ] Training pipelines guarded with resource quotas and monitoring.

7. Final Smoke Tests
   - [ ] Deploy a canary release and run end-to-end smoke tests.
   - [ ] Validate webhook delivery and QMOI responses.
   - [ ] Confirm automated rollback on failures.

Notes

- Use `POSTPRODUCTIONCHECKLIST.md` for daily/weekly checks after production.
- Use `ALLERRORSTYPESFILES.md` to map observed errors to fixes and tests.

<!-- QMOI_VALIDATION_START -->

{
"file": "PRODUCTIONCHECKLIST.md",
"validated_at": "2025-10-26T20:51:22.334388Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "PRODUCTION CHECKLIST"
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

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
