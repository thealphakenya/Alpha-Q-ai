# QVILLAGE.md

QVillage is the live QMOI community, model, and knowledge coordination surface. It is treated as the master-only QMOI community layer that stays synchronized with GitHub, Hugging Face, and the live autonomous agent.

## Active automation
- QVillage sync remains a first-class automation surface inside QCity and the autonomous agent.
- memory, model, and runtime state are synchronized across repo docs and platform references.
- the live state is refreshed automatically as the repository evolves.

## Language and QLion research

`ALLLANGUAGES.md`, `ALLLANGUAGESCOMPARE.md`, and
`QLIONPROGRAMMINGLANGUAGE.md` define the local language inventory, decision
criteria, and QLion implementation status. A local candidate inventory is not
live external research or proof that a compiler/toolchain is supported.

### Research evidence contract

For each language or QLion compatibility observation, retain the official
source URL, subject, retrieval timestamp (UTC), observed release/support value,
content hash, parser/collector version, freshness deadline, and result status.
Prefer official language specifications, release notes, security advisories,
and toolchain documentation. External text is untrusted input; store
source metadata and concise reviewed findings rather than copying source
prose. Rate limits, timeouts, stale records, and unavailable sources must be
reported explicitly.

The requested realtime/scheduled language research and automatic QVillage
refresh are `NOT_IMPLEMENTED` and `NOT_VERIFIED` in this checkout. No current
language release version or supported-QLion claim is inferred. A future
worker must run with read-only least privilege, bounded requests and retries,
and explicit evidence freshness; it must not change compatibility claims,
generate executable bindings, or publish without validation and review.
Monitor candidate-source count, fresh/stale/unknown observations, retrieval
success/failure, latency, retries, content-hash changes, and downstream
validation outcomes separately. These are monitoring requirements, not
measured live service metrics.


<!-- BEGIN QMOI MANAGED: restore-point-memory-sync -->
## Restore-point memory and branch continuity

- Evidence status: `BLOCKED_MISSING_EVIDENCE`; source status: `UNKNOWN`.
- Workspace SHA: `unknown`; tree SHA: `unknown`; master verified: `False`.
- Source evidence: `ollamatracks/qmoi_restore_point_preflight.json`; SHA-256: `unavailable`; workflow run: `unknown`.
- Ref roles: `main` is the default branch, `autosync-backup` is the staging ref, `master` is the validated-main parity mirror, and `qmoi` is the post-success restore point.
- These records are last-observed metadata, not proof that a remote worker is live; stale, missing, partial, or unverified refs remain visible as blocked/review-required.

- Current blocker: No restore-point preflight artifact is available in this checkout.
<!-- END QMOI MANAGED: restore-point-memory-sync -->

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `11182`; directories: `1288`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2177, build_download_install=2131, disability_accessibility=288, orchestration=2082, qteam_accountability=2071, release_tag_publish=2110, tree_inventory=2022`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2230`; needs review: `202`; metric candidate lines: `53160`; percentage occurrences: `22268`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13537`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `41035` lines in `3741` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `333`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: qaudit-language-inventory -->
## QAUDITS language-inventory observation

- Generated at: `2026-10-16T17:21:35.554481Z`; source-manifest SHA-256: `05d646de7978656bb04da692ae36a07478506edc8126c8259d0f182daa46f685`; scope: `materialized_local_only`.
- Scanned paths by language: `{"JavaScript": 761, "PowerShell": 24, "Python": 1654, "Rust": 4, "SQL": 2, "Shell": 134, "TypeScript": 2236, "unclassified": 6336}`.
- Unclassified paths: `6336`; maintained profiles: `26`; all-language coverage complete: `False`.
- Official release research verified: `False`; QVillage external research verified: `False`.
- Official language release research plan: `{"external_fetch_performed": false, "observed_release_versions": 0, "official_sources_planned": 26, "plan_artifact": "ollamatracks/language_research_plan.json", "plan_status": "PLANNED_NOT_VISITED", "source_not_registered_count": 0}`; current versions remain unknown until sources are fetched and reviewed.
- Counts are local path candidates only. Unknown, excluded, historical, and remote scopes remain explicit; language recommendations do not authorize migration.
<!-- END QMOI MANAGED: qaudit-language-inventory -->

<!-- BEGIN QMOI MANAGED: ollama-full-coverage-audit-status -->
## Agent-managed OFCA status

- Audit name: `OFCA`; local scan status: `INCOMPLETE`.
- Materialized files scanned: `11164`; mention-bearing files: `4960`.
- Ollam path/content candidates: `4960` paths and `48` named directories; scan duration: `160.215` seconds; start `2026-10-16T17:21:36.754913Z`, finish `2026-10-16T17:24:16.970273Z`.
- Phase preflight `audit_inventory_preflight`: 2 OFCA full scans plus 1 QAUDITS-universe scan; every-phase/task wiring: `NOT_VERIFIED`.
- Local refs: `39`; local commits: `2865`; mention-change commits: `2229`.
- Source manifest SHA-256: `5727eb29cf3bbafab867e7336c5008f0d08bef6c48c43a3c73814e77f5194a29`; full remote-history coverage: `False`.
- EvolutionO phases: `0/5` planned phases complete; plan SHA-256 `d1eb35569693ffac7ded5925d4485a03e6f148af1da2d26b5df1bb21b99b9746`; metrics SHA-256 `7b1820030d032f3d9cfa02cf9371783ff32cc96dbfe564a77c2b8e6de2b39097`; remote verified: `False`.
- Retirement remains blocked until pre-retirement agent success, QMOI capability parity, qmoi/qreplaceo archival, all-branch clean-tree evidence, and terminal OFCA metrics are independently verified.
- QVillage/QVS materialized references: `477` files, `222` Markdown files; remote/history completeness: `not_verified`.
- `prMergeIncluded` is required before merge activity. Unverified remote refs, pull requests, peer roots, and intermediate commit trees remain blockers.
- Next action: Run an authorized target-owned audit for both repositories covering all refs, PRs, and intermediate commit trees; attach terminal exact-SHA evidence before Q-version finalization.
<!-- END QMOI MANAGED: ollama-full-coverage-audit-status -->
