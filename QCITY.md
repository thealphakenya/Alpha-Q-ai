# QCITY.md

QCity remains the canonical file-management and platform coordination surface for the QMOI runtime. It coordinates GitHub, GitLab, Vercel, Netlify, Gitpod, Hugging Face, QVillage, and clone/autoclone automation without losing the live repo source-of-truth.

## Active automation
- file, repo, deployment, and sync management are centralized in QCity.
- all clone/autoclone flows are exposed as platform automation surfaces.
- the live runtime keeps all platform docs and generated summaries synchronized with the working repo state.

## Feature inventory and master review

Use the local [ALLFEATURES.md](ALLFEATURES.md) catalog and
[`feature_manifest.json`](ollamatracks/qaudits_all_features/feature_manifest.json)
as read-only QAUDITS inputs for QCity feature discovery. Map project and
platform candidates to an owner, implementation, tests, access mode, style and
universal UI requirements, and a monitoring source before describing them as
available to master. [ALLTRACKS.md](ALLTRACKS.md) and its machine inventory
remain the monitoring-mapping evidence; a candidate or metric reference is
not proof of a live monitor or interactive master dashboard.

QCity may list finance-related feature requirements, but it must not create
wallets, bank/provider accounts, move funds, or claim balances or realtime
financial data without separately authorized integrations and verified
provider evidence. Local inventories do not verify external synchronization,
deployment, or remote repository state.


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
