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

## Restore point and branch coverage

OFCA evidence for restore operations must bind the audit SHA to both repositories' `main`, `autosync-backup`, `qmoi`, and `master` refs, the corresponding tree SHA, required completion-document hashes, and the terminal Ollama workflow run that authorized restore publication. `master` is a fast-forward mirror of validated `main`, not an independent development branch. The pre-agent check may report `BOOTSTRAP_READY` only when both `qmoi` and `master` refs are absent and both `main`/backup pairs exactly match the trusted checkout under the explicit `QMOI_BRANCH_PUBLICATION_AUTHORIZED` gate. It may report `MASTER_BOOTSTRAP_READY` only when `qmoi`, `main`, and backup already agree and `master` is absent in both repositories. Any one-sided or stale ref remains blocked.

Push and scheduled autosync can maintain fast-forward-only main/backup synchronization, but they do not publish `qmoi` unless the completed default-branch agent workflow and its agent, tests, final validation, hosted-link, and health steps are verified successful. The publisher rechecks all relevant refs before and after publication and records partial outcomes without force-updating or hiding them. User-reported Actions secret name `MY_CUSTUOM_TOKEN` is supported with `MY_CUSTOM_TOKEN` as a compatibility alias; values are never recorded, and secret presence does not establish authorization.

<!-- BEGIN QMOI MANAGED: ollama-full-coverage-audit-status -->
## Agent-managed OFCA status

- Audit name: `OFCA`; local scan status: `INCOMPLETE`.
- Materialized files scanned: `10411`; mention-bearing files: `4148`.
- Local refs: `40`; local commits: `2627`; mention-change commits: `2006`.
- Source manifest SHA-256: `b780d118e7dff7bebb1fa4d11cf8ec895e9e64c21d9c51a5b828926065a70cb0`; full remote-history coverage: `False`.
- QVillage/QVS materialized references: `369` files, `212` Markdown files; remote/history completeness: `not_verified`.
- `prMergeIncluded` is required before merge activity. Unverified remote refs, pull requests, peer roots, and intermediate commit trees remain blockers.
- Next action: Run an authorized target-owned audit for both repositories covering all refs, PRs, and intermediate commit trees; attach terminal exact-SHA evidence before Q-version finalization.
<!-- END QMOI MANAGED: ollama-full-coverage-audit-status -->

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
