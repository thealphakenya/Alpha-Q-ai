# QMOI Lion Variations

## Purpose and evidence status

This is the active-root catalog for QMOI Lion product-variation requirements.
Names in this catalog are product/capability proposals until QAUDITS maps them
to maintained source, owners, tests, build artifacts, and exact-SHA release
evidence. Historical Lion documents under archived snapshots remain historical
inputs and are not rewritten by this catalog.

## Variation catalog

| Variation | Intended focus | Engineering and delivery evidence still required |
| --- | --- | --- |
| Lion Core | Shared orchestration and stable extension interfaces | Versioned APIs, threat model, core regression and compatibility tests |
| Lion Agent | Bounded task execution and resumable automation | Least privilege, checkpoints, failure recovery, duplicate-run prevention |
| Lion Cloud | Hosted orchestration and tenant isolation | Deployment, availability, security, privacy, cost, rollback evidence |
| Lion Desktop | Local developer and desktop workflows | Platform packages, update/signature, local data and permission tests |
| Lion Embedded | Constrained devices and hardware interfaces | Memory/resource budgets, supported targets, reproducible toolchains |
| Lion Enterprise | Organizational identity and governance | RBAC/SSO, auditability, tenant separation, support lifecycle |
| Lion Lite | Resource-bounded local development | Feature boundaries, reproducible install, performance/resource tests |
| Lion ML | Model integrations and evaluation workflows | Model/data provenance, evaluation, safety, privacy, resource and licensing review |
| Lion OS | Appliance/container operating environments | Image provenance, hardening, update, recovery, and platform support |
| Lion Plugin | Third-party or first-party extension boundary | Sandbox, permissions, signing, supply-chain review, compatibility tests |
| Lion SDK | Language-neutral integration and client tooling | Stable schema/API versions and tests across each supported language |
| QLion Programming Language | Proposed QMOI language/interoperability surface | Specification, actual compiler/runtime or bounded orchestration implementation, adapters, conformance/security tests, releases |

QLion is listed as a Lion variation candidate; this does not establish a
working compiler or a universal language runtime. See
[QLIONPROGRAMMINGLANGUAGE.md](./QLIONPROGRAMMINGLANGUAGE.md).

## Product-surface mapping

Each variation may be evaluated for apps, platforms, settings, site URLs,
logos/icons, extensions, developer tools, and delivery channels. A candidate
must map every applicable surface to source paths, product owner, stable
requirement ID, access mode, accessibility/security review, tests, version and
release artifacts, rollback, and measured support state. Preserve each
platform's branding and user settings unless an approved design explicitly
requires a shared element.

Financial management, revenue collection, marketplace payments, pricing,
trading, and account configuration are separately authority-gated. Variation
discovery never enables a financial integration or production transaction.
Record feasibility and required provider/legal/security review as blockers
until independently evidenced.

## QAUDITS and Q-version lifecycle

- QAUDITS records path, SHA-256, source scope, variation names, candidate
  feature facets, settings/brand/extension/automation/release mappings, and
  unreadable or omitted inputs.
- A variation count is candidate discovery, not implementation, support,
  release, revenue, or deployment success.
- QVersion stages `LION_AND_EXTENSION_VARIANTS`,
  `PRODUCT_PLATFORM_CATALOG`, `RELEASE_DELIVERY_LIFECYCLE`, and
  `QMOI_CAPABILITY_PARITY` require mapped tests, owners, rollback, authorization,
  and exact-SHA evidence.
- Never bulk-replace Ollama-related files while establishing Lion parity.
  Preserve model/runtime dependencies, historical archives, and external
  resources unless each migration is separately reviewed and authorized.

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
