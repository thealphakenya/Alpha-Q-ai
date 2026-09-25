# GitHub API instructions

## Required approach

- Verify authenticated identity before any mutation.
- Inspect branch protection and rulesets before merge or dispatch.
- Classify HTTP 400/401/403/404/409/422/429/5xx separately.
- Treat 403 and 404 as ambiguous until verified against auth and repo state.
- Use repository dispatch or target-owned workflow triggers only when explicitly authorized.
- Never claim success from a dispatch acceptance alone.

## Evidence requirements

Record:

- repo owner/name,
- operation and endpoint class,
- ref and SHA,
- response status,
- run or PR identifiers,
- verification method,
- and whether the result was terminal or merely observed.
