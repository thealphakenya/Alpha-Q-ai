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
