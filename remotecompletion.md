# Remote Completion Runbook

## Purpose

This document is the operational source for understanding why cross-repository
completion, Markdown synchronization, release publication, and protected-branch
completion may remain blocked. It records verified facts and required evidence;
it never converts a failed or unavailable remote operation into success.

## Scope

The completion target is both repositories:

- `thealphakenya/Alpha-Q-ai`
- `thealphakenya/qmoi-enhanced`

The completion scope includes active trees, `Alpha-Q-ai-2025`,
`qmoi-enhanced-history-14`, all available branches/tags/PR trees, Markdown
inventories, APIs/endpoints/routes/ports, release and validation ledgers, build
artifacts, tests, workflow checks, deployment state, and final remote SHA
verification.

## Current Evidence: 2026-09-24

| Evidence | Current result | Meaning |
| --- | --- | --- |
| Authenticated CLI account | `thevictorkenya` | A login exists; this does not prove every GitHub capability. |
| Repository permissions | `pull=true`, `push=true`, `triage=true` for both repositories; `admin=false`, `maintain=false` | Repository write access is present, but protected rules and Actions capabilities still require separate proof. |
| Alpha-Q-ai remote | `https://github.com/thealphakenya/Alpha-Q-ai` | Current local checkout target. |
| Local branch/SHA | `main` / `a5d5dc0fb05d8e84d262abc63d0d653835da6697` | Local work is not the remote completion result. |
| Remote `Alpha-Q-ai/main` | `60d329124102a03ab9cc40a20b7dc0c5919e8754` | Remote is ahead of this checkout. |
| Remote `autosync-backup` | `6d925c33f0093035755772137d863618b3818ab0` | Backup parity is not proven. |
| Divergence | remote ahead `16`, local ahead `2` | A normal fetch/rebase/validation/push cycle is required; force-push is prohibited. |
| Workflow visibility | Alpha-Q-ai `18`, qmoi-enhanced `97` workflows readable | Visibility is not dispatch or protected-branch authorization. |
| Previous Codespaces integration result | HTTP `403 Resource not accessible by integration` for target-owned dispatch/protected operations | The integration credential could not complete the remote lifecycle. |
| Local peer checkout | Only `/workspaces/Alpha-Q-ai/.git` is materialized | Cross-repository content parity cannot be independently proven locally. |
| Markdown evidence | `37,418` Category ALL records, including Git-ref history paths and per-file metrics | This is local/ref evidence, not proof that both remote repositories contain every file. |

No token, secret, or credential value belongs in this document, logs, commits,
workflow output, or prompts.

## What Remains Blocked

1. **Target-owned mutation:** The remote workflow must create/update branches,
   PRs, releases, artifacts, and documentation in the correct target repository.
2. **Cross-repository synchronization:** Both repository trees must be
   materialized or compared by an authorized target workflow. Local history
   paths are not a substitute for the second repository.
3. **Protected completion:** Required checks, reviews, rulesets, and merge
   authority must produce a remote PR/check/merge SHA.
4. **Backup parity:** `autosync-backup` must be synchronized and independently
   verified against the validated remote `main` SHA.
5. **Release publication:** Every artifact must have build, hash, install,
   runtime, platform, release-asset, and publication evidence.
6. **Validation closure:** The 102 local Markdown records marked `needs-review`
   must be classified or remediated; all remote validation jobs must be current.
7. **Ledger synchronization:** `RELEASES.md`, `ALLVALIDATIONS.md`,
   `ALLMDFILESREFS.md`, `MERGE.md`, and `oe2.txt` must reflect fresh remote
   evidence in both repositories.

## Authorization Alternatives

### Option A: User-owned CLI credential

Authenticate `gh` directly in the host terminal with an authorized credential,
then configure Git transport from that login. Required capabilities must be
verified for both repositories before any mutation:

- Contents read/write
- Actions read and workflow dispatch/write
- Pull requests read/write
- Checks and statuses read
- Releases read/write
- Protected-branch or ruleset-compatible merge authority
- Backup branch update authority

The credential must be entered by the user directly. It must never be sent to
or stored by the agent.

### Option B: GitHub App

Install a narrowly scoped GitHub App on both repositories. Grant only the
permissions required for the lifecycle above, issue short-lived installation
tokens in the target workflow, and verify each operation with repository, run,
PR, artifact, and SHA evidence. This is the preferred unattended option when a
long-lived personal token is unsuitable.

### Option C: Target-owned PR or merge queue

Use a source workflow to open or update a PR in the target repository. Let the
target repository run required checks and its own merge queue. The source must
wait for terminal conclusions and verify the merge commit SHA. This avoids
assuming that a source workflow can bypass target rules.

### Option D: Repository dispatch from an authorized workflow

Have an already-authorized workflow in one repository dispatch a correlation-ID
request to the other. The target workflow performs all mutation and publishes a
machine-readable result containing run ID, source SHA, target SHA, checks,
artifacts, and failure reason.

### Option E: Offline signed handoff

When network authorization is unavailable, produce a deterministic signed
bundle containing Markdown manifests, hashes, validation reports, release
plans, and the exact source SHA. A target-owned workflow later imports the
bundle, revalidates it, applies changes, and publishes the final evidence. This
is a plan/draft state, not completion.

## Required Remote Completion Sequence

1. Obtain authorization through one of the alternatives above.
2. Verify both repository identities, default branches, permissions, workflow
   visibility, dispatch capability, rulesets, and release access.
3. Fetch remote refs and classify divergence. Rebase local work safely; never
   force-push or discard remote telemetry.
4. Materialize or remotely inventory both repositories, all requested history
   projections, branches, tags, PR trees, and Markdown paths.
5. Refresh `ALLMDFILESREFS.md` in both repositories. Preserve unlimited category
   membership and record source, bytes, lines, hash/object ID, and validation
   status for every file.
6. Build a bidirectional sync plan. Classify missing paths, identical paths,
   variants, ownership, replacement decisions, and files requiring review.
7. Validate every category and every aggregate contract: APIs, endpoints,
   routes, ports, builds, installs, downloads, releases, platforms, security,
   memory, deployment, and documentation.
8. Run focused tests, full tests, workflow validation, dependency/security
   checks, artifact checks, and installation/runtime checks in both targets.
9. Submit the target-owned PR or workflow. Wait for terminal required-check
   conclusions; do not infer success from dispatch acceptance.
10. Merge or publish only through the authorized target lifecycle.
11. Verify final remote `main`, backup, PR, release, artifact, and deployment
    SHAs. Confirm both repositories contain the expected ledgers and inventories.
12. Update `remotecompletion.md` and `oe2.txt` with timestamps, IDs, SHAs,
    outcomes, and any remaining blockers.

## Failure Interpretation

- HTTP `401` or `403`: authorization or token capability failure; stop mutation.
- HTTP `404`: inaccessible resource or wrong repository/ref; verify identity.
- `non-fast-forward`: remote divergence; fetch, rebase, validate, retry normally.
- Pending or missing run: no completion evidence exists yet.
- Failed required check: repair the reported slice and rerun the same check.
- Missing peer tree: parity is unproven; do not copy or delete by assumption.
- Stale artifact/report: regenerate it before making a release or merge claim.

## Completion Definition

Remote completion is proven only when both repositories have fresh target-owned
evidence for synchronization, validation, required checks, merge/publication,
backup parity, and exact final SHAs. Local tests, Git-ref inventories, login
presence, repository push permission, or a successful dispatch request alone do
not satisfy this definition.
