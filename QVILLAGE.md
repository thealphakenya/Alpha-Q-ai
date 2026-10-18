# QVILLAGE.md

QVillage is intended as the QMOI community, model, and knowledge coordination surface, with authenticated master-only controls where required. This document does not prove a live deployment, identity enforcement, or synchronization with GitHub, Hugging Face, or the autonomous agent.

QMOI should not seek, create, download, or monitor pornographic or disturbing content as a default behavior. A request to handle such material requires lawful, policy-compliant context and appropriate authorization; master identity is not an override for criminal facilitation, platform safeguards, or other safety requirements. Enforcement is not verified by this documentation alone.
## Active automation
- QVillage sync remains a first-class automation surface inside QCity and the autonomous agent.
- memory, model, and runtime state are synchronized across repo docs and platform references.
- the live state is refreshed automatically as the repository evolves.

## QVirtualLabs research and evolution

QVillage can curate source-backed engineering research, reviewed experiment proposals, and validated QVirtualLabs results. A discovery or Ollama-generated hypothesis is not a verified finding: retain source URL/hash/time, license and freshness, experiment configuration, baseline, result provenance, limitations, reviewer, and status.

The QVirtualLabs lifecycle and simulation/physical distinction are defined in [QVIRTUALLABS.md](./QVIRTUALLABS.md). Physical results require authorized human-operated tests and traceable instrument records; simulated outputs must never be presented as if a physical experiment occurred. QVillage must keep candidate, tested, accepted, and deployed evolution states separate and preserve rollback evidence.

Research retrieval, live Ollama inference, and physical instrumentation are not verified merely by this document or by local candidate metrics.

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

## Feature discovery and evolution handoff

QVillage research should produce provenance-backed candidates for the shared
QAUDITS feature ledger, then retain distinct `discovered`, `reviewed`,
`experimented`, `accepted`, and `deployed` states. Link each candidate to its
source scope/hash, affected QCity or application surface, language/toolchain,
owner, focused tests, design/accessibility requirements, monitoring evidence,
and rollback plan. The local feature catalog is
[ALLFEATURES.md](ALLFEATURES.md), and the run metrics are in
[`feature_manifest.json`](ollamatracks/qaudits_all_features/feature_manifest.json).

The local audit discovers declared Markdown and structured memory candidates;
it does not run scheduled internet research or live Ollama inference. Treat
Hugging Face, papers, repositories, model cards, memory summaries, and
generated hypotheses as untrusted input until sources are reviewed and
experiments are independently validated. See
[ALLLANGUAGES.md](ALLLANGUAGES.md),
[QCITY.md](QCITY.md), and
[ALLQMOIAUTOEVOLVINGENVS.md](ALLQMOIAUTOEVOLVINGENVS.md) for the linked
language, project-monitoring, and autonomous-evolution contracts.

The canonical `QENGINEER.md` requirements are not present in this active
checkout. Keep the [QVIRTUALLABS.md](QVIRTUALLABS.md) source-reconciliation
gate blocked rather than treating historical copies or a public 404 as
authoritative requirements.

## Model comparison and replacement gate

QVillage model comparisons must bind the incumbent and QMOI candidate to the
same versioned benchmark suite, dataset, environment, task protocol, and
canonical feature-registry hash. The QAUDITS plan counts active and historical
evolution/comparison documents separately and records explicit feature
declarations and comparison candidates; these counts are discovery evidence,
not evidence that QMOI is superior.

The comparison must cover every registered feature and the required quality,
reasoning, coding, factuality, safety, privacy, security, reliability,
throughput, latency, resource-cost, and offline-independence dimensions with
adequate samples and confidence bounds. Any missing dimension/feature, tie,
regression, safety/license failure, untested rollback, or absent independent
review blocks eligibility. `ELIGIBLE_FOR_INDEPENDENT_REVIEW` is not an
authorization or replacement. QMOI is not automatically substituted for a
QVillage incumbent; actual change requires separate approval, rollback
readiness, and independently verified terminal remote evidence for the exact
repository/ref/SHA.

See [QAUDITS.md](QAUDITS.md) and the generated
[`qaudits_evolution_plan.json`](ollamatracks/qaudits_evolution_plan.json) for
the measured local inventory. Benchmark or remote evidence not present in
those artifacts remains unknown, not a pass.


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

<!-- BEGIN QMOI MANAGED: qaudit-qvirtual-labs-coverage -->
## Agent-managed QVirtualLabs engineering coverage

Generated from the local QVirtualLabs source inventory; a full QAUDITS universe manifest is included only when supplied by that inventory refresh. These are candidate-plan metrics, not implementation, experiment, physical-lab, or remote-completion evidence.
- Status: `BLOCKED_SOURCE_RECONCILIATION`; correlation ID: `231b915c-d2b9-45e5-baaa-1a02ef7b2209`; source manifest SHA-256: `ac35b2d4e2cc91f1395e1dd85f01183b6adbc2cb40411ef2194f6ab0e69a20ba`.
- QAUDITS universe manifest SHA-256: `unavailable`; QVirtualLabs source-manifest scope: `qvirtual_labs_source_files`.
- Plan artifact: `ollamatracks/qvirtual_labs_plan.json`; plan SHA-256: `b01b3fe497df8a44e3bd5965ac9f34336042d092199d3fe16ce0537118122773`; scope: `materialized_local_only`.
- Starter engineering-domain candidates: `14`; cross-cutting gate candidates: `19`; total starter-plan requirements: `33`.
- Authoritative QENGINEER requirements: `UNKNOWN`; QENGINEER source status: `missing_or_unsafe`.
- Requirement-to-implementation / focused-test mappings: `0` / `0`.
- Verified simulations / benchmark validations: `0` / `0`; physical experiment records / calibration correlations: `0` / `0`.
- Convergence cases / uncertainty reports / accuracy claims verified: `0` / `0` / `0`; safety protocols reviewed: `0`.
- Official research sources checked / date-fresh observations / stale observations: `8` / `8` / `0`; exact retrieval times not captured: `8`; verified evolution cycles: `0`.
- Recommended architecture: `one bounded, auditable adapter contract with specialist solvers; no monolithic all-domain solver selected`; first pilot candidate: `ngspice circuit reference case`; Ollama inference: `NOT_MEASURED` by this inventory.
- Tool recommendation rationale: `domain fit from official documentation, implementation isolation, and a bounded first regression; not a comparative performance benchmark`; selected tool: `NONE`; tool candidates: `6`.
- Public QENGINEER probe: `UNKNOWN_NOT_FOUND_OR_PRIVATE`; a public 404 is ambiguous without authenticated repository read access.
- UI/accessibility mappings / project, auto-project, and preview integrations: `0` / `0`; remote verified: `False`.
- Simulation output is never counted as physical evidence. Physical correlation requires an authorized protocol, human operator, traceable instruments/calibration, and reviewed raw-data provenance.
- Historical reference: `qmoi-enhanced-history-14/QVIRTUALLABS.md`; scope `historical_snapshot_candidate`; not authoritative.
- The planner does not run a solver, retrieve external research, invoke hardware, or infer that an unlinked implementation is absent.
<!-- END QMOI MANAGED: qaudit-qvirtual-labs-coverage -->
