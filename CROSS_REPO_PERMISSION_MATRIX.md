# Cross-Repository Permission Matrix

This matrix is an evidence contract for `thealphakenya/Alpha-Q-ai` and
`thealphakenya/qmoi-enhanced`. It records capability requirements without
storing credential values.

| Operation | Source | Target | Credential role | Required permission | Expected result | Verification |
| --- | --- | --- | --- | --- | --- | --- |
| Repository read | Either repo | Either repo | `MY_CUSTOM_TOKEN` or target `GITHUB_TOKEN` | Contents: read | HTTP 200 | Repository metadata and SHA |
| Workflow visibility | Either repo | Target repo | `MY_CUSTOM_TOKEN` or target `GITHUB_TOKEN` | Actions: read | HTTP 200 | Workflow is active and addressable |
| Same-repo workflow dispatch | Target workflow | Same target repo | `MY_CUSTOM_TOKEN`, then `github.token` fallback | Actions: write | HTTP 204 | Target run ID, ref, SHA, terminal result |
| Cross-repo dispatch | Source workflow | Target workflow | GitHub App installation token or `MY_CUSTOM_TOKEN` | Actions: write on target | HTTP 204 | Target run ID and correlation ID |
| Branch creation | Target workflow | Target repo | Target workflow credential | Contents: write | HTTP 201 | Branch ref and source SHA |
| PR creation/update | Target workflow | Target repo | Target workflow credential | Pull requests: write, Contents: write | HTTP 201/200 | PR number, base/head SHA |
| Checks/status read | Observer | Target repo | Read credential | Checks: read, Commit statuses: read | HTTP 200 | Required-check conclusions |
| Protected-branch merge | Target workflow | Target repo | Authorized repository/App identity | Ruleset-compatible merge authority | Policy-dependent | Merge SHA and required reviews/checks |
| Backup synchronization | Target workflow | `autosync-backup` | Target workflow credential | Contents: write, branch policy compatible | Policy-dependent | Backup SHA equals verified main SHA |
| Artifact access | Observer | Target workflow | Actions: read | HTTP 200 | Artifact manifest and checksum |

## Authorization rules

- `thealphakenya` is the coordinated GitHub owner/account for both repositories.
- The current Codespace identity is `thevictorkenya`; repository push access is
  not equivalent to Actions dispatch or protected-branch administration.
- `MY_CUSTOM_TOKEN` is a GitHub-managed secret expected in both repositories.
  Only Actions may resolve it; its value must never be printed, copied, or
  persisted by Codespace tooling.
- A failed permission probe is `AUTH_BLOCKED`, never `SUCCESS` or
  `NO_CHANGES_REQUIRED`.
- Every successful mutation requires target run/PR/SHA evidence and a terminal
  remote conclusion.
- The matrix must be evaluated in both directions before cross-repository
  parity is claimed.

## Evidence fields

Each preflight or lifecycle record must include the operation, source, target,
credential role (never its value), endpoint, HTTP result, required permission,
run or PR identifier, source SHA, target SHA, timestamp, and remediation for a
failure.

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
