# NETLIFYPAYED.md

QMOI keeps Netlify parity in sync with the live GitHub repository by maintaining deployment automation, redirects, site health, and production-safe build rules. The autonomous agent keeps this document aligned with the live Netlify runtime path and the canonical repo docs.

## Active automation
- netlify.toml is kept in the repo root and matches the current deployment contract.
- QCity and Ollama automation keep Netlify deploy and redirect settings synchronized with GitHub workflow health.
- Production checks must verify build command, publish path, redirects, and deployment health before final promotion.

## Local deployment evidence — 2026-10-11
- PR #54 head `f0814054118b23c1cefea2addb01322d1b0fa3ef` has three failed Netlify checks for deployment `6acbd47760060400082ff4d0`; GitHub check summaries link to provider logs but do not include the failure details.
- The root `netlify.toml` configures a Python test command as the build, publishes `.`, redirects all paths to `/index.html`, and names `functions/` as the functions directory. The active root has no `index.html` or `functions/`, and `package.json` defines no frontend build command.
- The PR-head TOML redirect value was malformed and failed a local TOML parse. The redirect string is corrected locally and parses; this change is uncommitted and has not been redeployed.
- The intended app root, publish artifact, and serverless-function contract are not established by available active-repository evidence. Deployment remains `BLOCKED`; do not remove or replace the build, publish, redirect, or functions settings until the owner and provider logs confirm the intended architecture.

