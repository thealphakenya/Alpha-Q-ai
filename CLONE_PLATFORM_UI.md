# CLONE_PLATFORM_UI.md

<!-- BEGIN QMOI MANAGED: cloned-platform-ui-matrix -->
## Cloned-platform operator UI coverage

Every entry below is a QMOI operator-console requirement for each client platform. It does not assert that the upstream provider exposes identical features or that this repository contains a working console.

Client platform targets: windows, macos, linux, ios, android, web.

### github

- [ ] repository and branch inventory
- [ ] workflow/check status
- [ ] PR/release/security summaries
- [ ] permission and audit state
- [ ] QMOI-branded repo and release card customization
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.

### gitlab

- [ ] project and merge-request inventory
- [ ] pipeline/runner status
- [ ] registry/artifact state
- [ ] permission and audit state
- [ ] QMOI clone polish for project headers and milestone views
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.

### gitpod

- [ ] workspace inventory
- [ ] environment and startup status
- [ ] workspace launch/stop controls
- [ ] secret readiness without values
- [ ] custom workspace branding and startup states
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.

### netlify

- [ ] site/build inventory
- [ ] preview and production deploys
- [ ] forms/redirects/edge-function status
- [ ] domain and logs state
- [ ] custom site branding, icons, and fonts
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.

### vercel

- [ ] project/deployment inventory
- [ ] preview/promote/rollback controls
- [ ] domains/functions/edge status
- [ ] logs/analytics/usage state
- [ ] custom deployment UI and QMOI badge polish
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.

### quantum

- [ ] hosting project/deployment inventory
- [ ] compute backend and queue state
- [ ] hybrid job controls
- [ ] quota/cost/provenance and audit state
- [ ] QMOI compute UI tokens and custom job branding
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.

### huggingface

- [ ] model/space/dataset inventory
- [ ] inference and runtime status
- [ ] build/log/artifact views
- [ ] permissions and access state
- [ ] brand-safe HF surfaces and custom QMOI identity
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.

### qvillage

- [ ] community/content inventory
- [ ] device and sync state
- [ ] moderation/notification controls
- [ ] member privacy and access state
- [ ] custom community visual language and shared iconography
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.

### dagshub

- [ ] repository/dataset inventory
- [ ] experiment and ML workflow status
- [ ] artifact/metric comparisons
- [ ] permission and provenance state
- [ ] custom dataset and experiment UI branding
- [ ] Responsive, accessible operator UI on: windows, macos, linux, ios, android, web.
- Implementation status: not verified by this workspace.
<!-- END QMOI MANAGED: cloned-platform-ui-matrix -->

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
