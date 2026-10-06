# GitHub API instructions

## Required approach

- Verify authenticated identity before any mutation.
- Inspect branch protection and rulesets before merge or dispatch.
- Classify HTTP 400/401/403/404/409/422/429/5xx separately.
- Treat 403 and 404 as ambiguous until verified against auth and repo state.
- Use repository dispatch or target-owned workflow triggers only when explicitly authorized.
- Never claim success from a dispatch acceptance alone.
- The autonomous agent must apply these identity, protection, authorization, and terminal-evidence checks to each remote operation; an access preflight is not mutation authority or parity evidence.

## Evidence requirements

Record:

- repo owner/name,
- operation and endpoint class,
- ref and SHA,
- response status,
- run or PR identifiers,
- verification method,
- and whether the result was terminal or merely observed.

## GitHub App preflight

- Prefer a target-owned workflow using a short-lived installation token scoped to explicit repositories and minimum permissions. Discover installation context from owner/repository inputs when supported; never fabricate an installation ID.
- Codespaces secrets are not Actions secrets. Do not infer that a value configured in one store is available in the other; validate each path independently.
- Before App API use, require owner-confirmed rotation of any historically exposed key, then verify App identity and installation/repository access with read-only calls. A secret-presence check is not proof of authentication.
- For GitHub App access by Copilot Chat or the Ollama agent, route through an approved tool or target-owned workflow that reads secrets in-process. Never place a private key/token in chat context. Fail closed on 401/403, unknown scopes, or missing endpoint evidence.
