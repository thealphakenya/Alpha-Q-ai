# Security instructions

## Fail-closed expectations

- Never weaken security constraints to make validation pass.
- Record security findings explicitly and do not mask them.
- Keep secrets and token values out of logs, prompts, and documentation.
- Respect vulnerable dependency and secrets scanning results until resolved or explicitly classified as external blockers.

## Required policy

All release, merge, and deployment decisions must remain blocked by unresolved security findings until the risk is remediated or the blocker is independently recorded as external and non-actionable.

The autonomous agent may collect read-only diagnostics and propose bounded remediation, but it cannot downgrade, suppress, or self-approve a security finding to keep the workflow moving.

## GitHub App and secret handling

- Treat a user-provided App permission screenshot or Markdown snapshot as reported evidence, not current effective permission proof. Review broad grants, especially administration, secrets, workflow writes, alert dismissal, and push-protection bypass requests; grant only what an approved feature needs.
- Never expose, paste, or log secret values. Codespaces secrets, Actions secrets/variables, PATs, and App installation tokens are distinct credential sources.
- Do not use a key classified as compromised until the owner confirms it was revoked/rotated and a replacement is installed. Presence alone does not verify rotation, identity, scope, or validity.
- Do not fabricate, self-issue, or silently rotate external provider credentials. Automate name-only inventory and provisioning guidance; require provider/owner-controlled issuance and read-only verification before use.
- Copilot Chat and Ollama must not receive private keys or tokens in context. Use approved tooling or target-owned workflows that mint short-lived least-privilege tokens and emit value-free evidence.

## QAUDITS security and coverage gates

- Include security findings, dependency/secret-scan outcomes, test and workflow mappings, omitted scopes, and their evidence references in QAUDITS coverage. Keep unverified or unresolved findings visible; do not suppress, downgrade, or self-approve them to advance a gate.
- Treat scanner matches as candidates until owner, impact, reproduction, remediation, focused tests, rollback, and required remote evidence are mapped. Never bulk-rewrite candidate production/security gaps.
- Block merge, release, and deployment claims while actionable security findings or missing terminal exact-SHA evidence remain. Record explicit blockers in `oe2.txt`, `remotecompletion.md`, and machine-readable evidence without exposing secret values.
- Finance audits must include currency/amount, revenue, payments, wallets/banks, deals, employment/payroll, jurisdiction, project-finance, and financial-security candidates. Persist only path/hash/scope/line/category metadata; never persist amount strings, account IDs, source lines, credentials, or provider secrets. Candidate counts do not prove legal coverage or authorize a transaction.

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
