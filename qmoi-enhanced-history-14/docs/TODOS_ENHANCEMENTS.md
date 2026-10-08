---
title: "QMOI To-dos Enhancements (20+ improvements)"
qmoi_validation_frontmatter: true
---

# QMOI To-dos Enhancements (20+ improvements)

This file lists concrete improvements to the QMOI to-dos system (used by `scripts/qmoi_todos.py`) that will make planning, execution, validation, and LION integration more robust.

1. Persistent task metadata with versioning and provenance
2. Task dependency graph (DAG) support
3. Retry/backoff strategies and failure categorization
4. LION-executable action hooks for automated remediation
5. QVS attachment support (store artifacts and logs per task)
6. Role-based assignments and access metadata
7. Task templating and parametrization
8. Scheduled runs and cron-like triggers
9. Audit trail for runs (who/when/what changed)
10. Checkpointing and resumable task runs
11. Integration with `validate_md.py` to auto-create validation tasks
12. Auto-generation of tasks from validation reports (missing/extra refs)
13. Export/import in multiple formats (JSON/CSV/markdown)
14. CLI and REST API endpoints for orchestrators
15. Webhook notifications on task state changes
16. Pluggable executors (local, container, remote agent)
17. Performance profiling and cost estimation for tasks
18. Test harness integration to auto-validate results
19. Security checks and secret scanning as pre-run gates
20. Metrics and dashboards for task throughput and success rates
21. Automatic ticket creation for failures (integration with issue trackers)
22. Prioritization and SLA enforcement
23. Tagging and search across tasks and run outputs
24. Machine-readable LION tags for each completed task (for memory and audit)

Next steps: implement items incrementally; begin by wiring (11) and (12) so that validation reports auto-create remediation tasks.

<!-- QMOI_VALIDATION_START -->

{
"file": "docs/[AUTOFIXED by Ollama at 2026-07-20T01:19:39.211930Z: please review]S_ENHANCEMENTS.md",
"validated_at": "2025-10-26T20:51:24.577849Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": true,
"detail": "QMOI To-dos Enhancements (20+ improvements)"
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


---
Automated update by Ollama agent at 2026-07-20T01:19:39.211930Z. Please review changes above.

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
