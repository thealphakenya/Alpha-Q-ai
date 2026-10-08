TESTS.md

## Overview

This document lists the automated tests in this repository, the features they exercise, and how to run them. It also documents expected behaviour for production-ready features referenced by tests (session/memory, accessibility settings, TTS/SSML, sync backends).

## Run tests

- JavaScript / Next.js tests (Jest):
  - Install: `npm install`
  - Run: `npm run test` or `npm run ci:full` for full build+tests

- Python tests (pytest):
  - Ensure dev requirements installed: `pip install -r requirements-dev.txt`
  - Run: `python -m pytest` or `python -m pytest tests/<specific>`

## High-level test areas and related features

1. API / HTTP

- Files: `tests/api/*`, `__tests__/qmoi-chat-api.test.ts`
- Features tested:
  - `/api/qmoi/chat` proxy returns OpenAI-like chat completion objects.
  - `/api/qmoi/memory` and `/api/qmoi/voice-preview` endpoints respond and honor model name `qmoi`.
- Production considerations:
  - Enforce `QMOI_API_BASE` and request timeouts.
  - Validate and sanitize incoming messages before forwarding to models.

2. Persona & helper server integration

- Files: `__tests__/*persona.integration*`, `scripts/qmoi_local_server.py` (helper)
- Features tested:
  - Persona detection (master/sister/user) and fallback behaviour.
  - Persistent local memory file (`qmoi_memory.json`) and optional SQLite backend.
  - Sync push/pull endpoints for backends (gist, hf, scp) using `QMOI_SYNC_BACKENDS` env var.
- Production considerations:
  - Protect sync endpoints with `QMOI_SYNC_API_KEY`.
  - Use atomic writes for memory persistence and optional Redis for scaling.

3. Memory & sync

- Files: `scripts/tests/test_memory_sync.py`, `tests/test_qmoi_memory.py`
- Features tested:
  - `push_memory_to_backends` and `pull_memory_from_backends` behaviour.
  - Merge strategy for remote memory (idempotent by timestamp keys).
- Production considerations:
  - Prefer Redis or managed DB for production memory with periodic durable backups.
  - Ensure credentials (GH token, HF token) come from env and are validated.

4. UI components & accessibility

- Files: `src/components/*`, integration UI tests
- Features tested:
  - `UISettings` persists user preferences (font size, colors, high contrast, reduce motion).
  - Keyboard shortcuts and global events (`qmoi:open-settings`, `qmoi:toggle-high-contrast`, `qmoi:toggle-reduce-motion`).
  - `FloatingAQ` floating ask widget and `ThemeProvider` behaviour.
- Production considerations:
  - `UISettings` is client-only and mounted dynamically to avoid SSR problems (done via `app/layout.tsx`).
  - Expose CSS custom properties for theming and accessibility.

5. Payments, webhooks and integrations

- Files: `payments/*`, `scripts/test_*` that exercise payments
- Features tested:
  - Stripe adapter error handling and webhook verification.
  - Provider stubs used in tests when third-party keys are absent.
- Production considerations:
  - Use real Stripe keys only in secure environments; tests should use stubs or test keys.
  - Validate and mask sensitive values in logs.

6. End-to-end and smoke tests

- Files: `tests/e2e/*`, `scripts/*comprehensive*`
- Features tested:
  - App build, static generation, and core UI routes.
  - Quick smoke checks using helper servers.
- Production considerations:
  - CI should run `npm run build` and server-side smoke tests in a reproducible environment.

## Notes on running tests reliably

- Pytest environment:
  - Some tests expect local directories (e.g., `logs/`) and environment variables. Ensure `logs/` exists and sensible env vars are set (`QMOI_BASE`, `QMOI_SYNC_BACKENDS`, tokens if testing sync`).
  - Use the provided `requirements-dev.txt`.
- Jest / Node:
  - The Next `app` layout dynamically imports client-only components; ensure `next build` succeeds before running some integration tests.

## Actionable checklist to reach green CI (recommended)

- Ensure `requirements-dev.txt` contains all Python test deps and install in CI image.
- Create the `logs/` directory before running pytest.
- Add a lightweight, well-tested `qmoi_local_server.py` helper that uses atomic writes and optional Redis.
- Protect sync endpoints with `QMOI_SYNC_API_KEY` and make tests use a test key.
- Keep client-only UI components dynamically imported (already wired in `app/layout.tsx`).

If you want, I can:

- Add a minimal, robust copy of `scripts/qmoi_local_server.py` (safe default helper) to reduce flaky integration failures.
- Run `npm run ci:full` and `pytest` in CI-like sequence and fix remaining issues until green.

---

Generated on: 2025-12-23

## Autonomous workflow integration

- This directory document is maintained by the Ollama autonomous agent and synchronized with the GitHub workflow triggers.
- It tracks WiFi/captive-portal automation, component gallery migration, universal styles, and self-healing run expectations.
- Keep this file aligned with API.md, ENDPOINTS.md, ROUTES.md, ALLPORTS.md, STYLES.md, UNIVERSALS.md, and WORKFLOWS.md.
- Ensure every run records resume state in resumefromhere.txt and preserves processed work between local and workflow executions.

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
