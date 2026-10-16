# Ollama Full Coverage Audit (OFCA)

OFCA is a required pre-merge audit stage. The agent runs it after source inventory and before merge planning or file-merge activity, records it as `OLLAMA_FULL_COVERAGE_AUDIT` in the Q-version lifecycle, and sets `prMergeIncluded` in merge evidence.

Merge planning and read-only inventory may continue when the audit is incomplete, but merge application is blocked unless OFCA and the Markdown source index are complete. The blocked lifecycle stage retains its reasons and resumable next action.

The metadata-only report in `ollamatracks/ollama_reference_audit.json` records mention-bearing paths, hashes, line numbers, responsibility categories, local ref and commit counts, and a source-manifest hash. It never copies source lines into evidence. The companion `ollamatracks/repository_surface_audit.json` is consumed by internal/external research and tracks all accessible file hashes, Markdown structure/word/sentence metrics, API/endpoint/route/port/link/component/tree/automation categories, comparison and Qtrade metrics, percentage locations, production candidates, and memory/QVillage/QVS surfaces. `ollamatracks/style_universal_replacement_inventory.json` tracks candidate files and directories, hashes, source scope, and required test/hook review for migration to `STYLES.md`, `UNIVERSALS.md`, and `UNIVERSAL.md`.

## Coverage boundaries

- A materialized-tree scan is local scope, not all-history proof.
- Local refs and commit-diff scans do not prove remote-ref freshness, every pull request, every intermediate commit tree, or coverage in an unavailable peer repository.
- Missing, unreadable, oversized, or unenumerated sources remain explicit blockers; local audit status cannot be promoted to complete by inference.
- A match is a candidate responsibility record, not proof of a defect or a reason to rewrite a file.
- Style/universal candidates require ownership, compatibility, accessibility/security, focused tests, hook/webhook applicability, rollback, and authorization review before changes.
- Test and hook discovery is not coverage. A feature remains unmapped until implementation, positive/negative tests, event behavior, and exact-SHA validation are linked.
- Markdown hashes and structural checks do not prove sentence meaning. Semantic requirement mapping must cite implementation, tests, workflows, documentation, owner, and exact-SHA evidence; unresolved items remain queued.
- Merge, release, deployment, credential, financial, and protected-branch actions remain subject to their existing authorization and evidence gates.

## Q version gate

Q version lifecycle gate 21 requires OFCA on each merge execution. Finalization additionally requires terminal target-owned audit evidence for both repositories covering current refs, pull requests, and intermediate commit trees at exact final SHAs. Until that evidence exists, the audit stays `NEEDS_REVIEW` and Q-version finalization stays blocked.

## Per-phase Ollama inventory and QMOI succession gate

At the start of every autonomous execution, lifecycle phase, and bounded task
batch, record an OFCA preflight event before doing work. The event must include
phase/task ID, UTC start/end and duration, repository/ref/HEAD, materialized
source-manifest SHA-256, files and bytes enumerated/read, Ollama/Ollam
path/content candidate counts, matched directory counts, skipped/unreadable/
oversized/symlink paths by reason, local refs/commits/PR evidence observed,
and the next action. Do not copy source lines into telemetry.

The preflight verifies the exact tree state, not just an `ollama` filename
search. Inventory both path names and file contents for Ollama/Ollam
responsibilities, including runtime/model use, workflows, policies,
telemetry, memory, history, dependencies, APIs, tests, and credentials
references (names/paths only). Keep materialized, historical, fetched-ref,
and remote-target coverage denominators separate. Record a changed-manifest
delta and rerun the full scan after any mutation. An unchanged manifest may
reuse an earlier full scan only when path set, hashes, exclusions, root/ref,
scanner version, and timestamp freshness all match; otherwise it is
`STALE`/`UNKNOWN`, not a pass. Never start merge, replacement, release, or
publication from a stale or incomplete preflight.

Ollama retirement is a gated handoff, not a string substitution. QMOI must
first demonstrate task-level capability parity, reliability, security,
performance, health, recovery, data compatibility, test coverage, and
operational ownership. Require a complete OFCA candidate inventory, reviewed
path-by-path dependency and ownership mapping, backwards-compatible adapter
or migration plan, focused regression tests, rollback, and terminal exact-SHA
validation. Only then may an authorized migration change eligible active
files/directories. Preserve third-party/runtime dependencies, historical
archives, user data, credentials/configuration, and externally managed
resources unless a separate explicit approval and compatibility plan covers
them. Never rewrite all matches in bulk or remove Ollama before QMOI parity is
independently proven.

Required succession counters are `preflight_runs`, `full_scans`,
`manifest_reuse_runs`, `stale_preflight_runs`, `candidate_paths`,
`candidate_directories`, `mapped_to_owner_or_feature`,
`unmapped_candidates`, `parity_gates_passed`, `eligible_migrations`,
`migrations_applied`, `focused_checks_passed`, `rollbacks`, and
`remote_sha_verified`. Publish numerator and denominator, scan scope, source
manifest, status, and blockers for each; local counts are not percentages of
global or remote coverage. QVersion's `QMOI_CAPABILITY_PARITY` and
`PRODUCTION_REPLACEMENTS` gates own acceptance. The existing automatic
replacement default remains disabled.

Implementation evidence must be reported, not implied by this contract: the
current OFCA helper performs a materialized-tree scan during explicit audit
entry points, and the existing agent refresh invokes it during inventory and
validation flows. This checkout has not yet demonstrated a separately
correlated preflight at every phase/task boundary, manifest-safe reuse,
candidate-directory counts, or automated QMOI parity evaluation. Those
capabilities remain `NOT_VERIFIED`; do not describe the above requirements as
already-running automation.

## Restore point and branch coverage

OFCA evidence for restore operations must bind the audit SHA to both repositories' `main`, `autosync-backup`, `qmoi`, and `master` refs, the corresponding tree SHA, required completion-document hashes, and the terminal Ollama workflow run that authorized restore publication. `master` is a fast-forward mirror of validated `main`, not an independent development branch. The pre-agent check may report `BOOTSTRAP_READY` only when both `qmoi` and `master` refs are absent and both `main`/backup pairs exactly match the trusted checkout under the explicit `QMOI_BRANCH_PUBLICATION_AUTHORIZED` gate. It may report `MASTER_BOOTSTRAP_READY` only when `qmoi`, `main`, and backup already agree and `master` is absent in both repositories. Any one-sided or stale ref remains blocked.

Push and scheduled autosync can maintain fast-forward-only main/backup synchronization, but they do not publish `qmoi` unless the completed default-branch agent workflow and its agent, tests, final validation, hosted-link, and health steps are verified successful. The publisher rechecks all relevant refs before and after publication and records partial outcomes without force-updating or hiding them. User-reported Actions secret name `MY_CUSTUOM_TOKEN` is supported with `MY_CUSTOM_TOKEN` as a compatibility alias; values are never recorded, and secret presence does not establish authorization.

<!-- BEGIN QMOI MANAGED: ollama-full-coverage-audit-status -->
## Agent-managed OFCA status

- Audit name: `OFCA`; local scan status: `INCOMPLETE`.
- Materialized files scanned: `11284`; mention-bearing files: `5080`.
- Ollam path/content candidates: `5080` paths and `51` named directories; scan duration: `166.113` seconds; start `2026-10-16T19:42:15.145668Z`, finish `2026-10-16T19:45:01.259147Z`.
- Phase preflight `audit_inventory_preflight`: 2 OFCA full scans plus 1 QAUDITS-universe scan; every-phase/task wiring: `NOT_VERIFIED`.
- Local refs: `39`; local commits: `2867`; mention-change commits: `2231`.
- Source manifest SHA-256: `c6cb8770188edc86682377011e495b7a3ef28927622c2c516e3423ed8c8e2e95`; full remote-history coverage: `False`.
- EvolutionO phases: `0/5` planned phases complete; plan SHA-256 `06271df029931a822e34bedda961c2f79bd9777520bb39f6560be05e282503ae`; metrics SHA-256 `b1b07beeb68639ec0c067c972b0e77852b1efb50080535d176f6cc4bafaf043c`; remote verified: `False`.
- Retirement remains blocked until pre-retirement agent success, QMOI capability parity, qmoi/qreplaceo archival, all-branch clean-tree evidence, and terminal OFCA metrics are independently verified.
- QVillage/QVS materialized references: `493` files, `223` Markdown files; remote/history completeness: `not_verified`.
- `prMergeIncluded` is required before merge activity. Unverified remote refs, pull requests, peer roots, and intermediate commit trees remain blockers.
- Next action: Run an authorized target-owned audit for both repositories covering all refs, PRs, and intermediate commit trees; attach terminal exact-SHA evidence before Q-version finalization.
<!-- END QMOI MANAGED: ollama-full-coverage-audit-status -->

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `11301`; directories: `1291`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2177, build_download_install=2131, disability_accessibility=288, orchestration=2082, qteam_accountability=2071, release_tag_publish=2110, tree_inventory=2022`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2230`; needs review: `202`; metric candidate lines: `53187`; percentage occurrences: `22274`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13561`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `41058` lines in `3748` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `340`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->

<!-- BEGIN QMOI MANAGED: qaudit-language-inventory -->
## QAUDITS language-inventory observation

- Generated at: `2026-10-16T19:42:13.889504Z`; source-manifest SHA-256: `2f2226c9b16ac7e88f811078ce1efe2cdeae4fbe797f2201d374a797b35cec76`; scope: `materialized_local_only`.
- Scanned paths by language: `{"JavaScript": 761, "PowerShell": 24, "Python": 1654, "Rust": 4, "SQL": 2, "Shell": 134, "TypeScript": 2236, "unclassified": 6455}`.
- Unclassified paths: `6455`; maintained profiles: `26`; all-language coverage complete: `False`.
- Official release research verified: `False`; QVillage external research verified: `False`.
- Official language release research plan: `{"external_fetch_performed": false, "observed_release_versions": 0, "official_sources_planned": 26, "plan_artifact": "ollamatracks/language_research_plan.json", "plan_status": "PLANNED_NOT_VISITED", "source_not_registered_count": 0}`; current versions remain unknown until sources are fetched and reviewed.
- Counts are local path candidates only. Unknown, excluded, historical, and remote scopes remain explicit; language recommendations do not authorize migration.
<!-- END QMOI MANAGED: qaudit-language-inventory -->
