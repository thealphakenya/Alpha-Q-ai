# QVILLAGE.md

QVillage is the live QMOI community, model, and knowledge coordination surface. It is treated as the master-only QMOI community layer that stays synchronized with GitHub, Hugging Face, and the live autonomous agent.

## Active automation
- QVillage sync remains a first-class automation surface inside QCity and the autonomous agent.
- memory, model, and runtime state are synchronized across repo docs and platform references.
- the live state is refreshed automatically as the repository evolves.


<!-- BEGIN QMOI MANAGED: ollama-full-coverage-audit-status -->
## Agent-managed OFCA status

- Audit name: `OFCA`; local scan status: `PASS`.
- Materialized files scanned: `10384`; mention-bearing files: `4125`.
- Local refs: `37`; local commits: `2578`; mention-change commits: `1962`.
- Source manifest SHA-256: `3d1fc49a37f28083b89c2634bc247ef2111c64df1a2a1142205fe778b1c8547c`; full remote-history coverage: `False`.
- QVillage/QVS materialized references: `356` files, `205` Markdown files; remote/history completeness: `not_verified`.
- `prMergeIncluded` is required before merge activity. Unverified remote refs, pull requests, peer roots, and intermediate commit trees remain blockers.
- Next action: Run an authorized target-owned audit for both repositories covering all refs, PRs, and intermediate commit trees; attach terminal exact-SHA evidence before Q-version finalization.
<!-- END QMOI MANAGED: ollama-full-coverage-audit-status -->

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10408`; directories: `1267`; Markdown: `2412`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Markdown structural checks passed: `2186`; needs review: `218`; metric candidate lines: `46823`; percentage occurrences: `22236`.
- Formula/calculation candidate lines: `11364`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `36263` lines in `3090` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `285`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
