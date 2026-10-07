---
title: "Issue draft for WORKSPACE_LIGHT_MODE.md"
generated: 2025-11-08T16:06:38.358103Z
---

# Review needed: WORKSPACE_LIGHT_MODE.md

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:41.786757Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:41.786757Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:41.786757Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

````
---
title: "Workspace Light Mode (Low-data / Codespaces Optimizations)"
qmoi_validation_frontmatter: true
---

# Workspace Light Mode (Low-data / Codespaces Optimizations)

Purpose: reduce data and CPU usage when opening and using this workspace in a browser-based editor (Codespaces, GitHub.dev, VS Code Web). These are non-invasive, reversible changes and only add helpers and documentation — nothing will be auto-executed.

Principles
- Avoid downloading large folders (node_modules, .qmoi_validation, build outputs).
- Prefer sparse-checkout and shallow clones for git operations.
- Run heavy scans or installs in CI or on demand (server-side).
- Serve files on-demand and compress responses.

Quick actions (commands you can run locally or in Codespace terminal)

- Sparse checkout (git 2.25+):

  ```bash
  git clone --no-checkout <repo> repo-light
  cd repo-light
  git sparse-checkout init --cone
  git sparse-checkout set src app docs
  git checkout
````

- Shallow clone (reduce history):

  ```bash
  git clone --depth 1 <repo>
  ```

- Avoid installing dependencies in the browser workspace; run `npm ci` in CI or a remote builder. Use the CI workflow added to run tests and heavy tasks.

Files and tools added here

- `tools/build_light_index.py` — creates `tools/light_index.json` with top large files and suggestions to exclude them locally.
- `tools/start_light_server.py` — simple on-demand HTTP server that serves files under a size limit or from a whitelist in the light index.
- `.vscode/settings.json` — hides large folders from Explorer (non-destructive editor setting).

Best practices

- Use Codespaces for editing and run heavy commands in CI.
- Use the `tools/light_index.json` to know which files to avoid opening in the browser.
- If you must open large files, consider opening them via the server preview (the light server) which streams and compresses content.

Safety note

- These helpers do not modify source files. They only generate indexes and provide lightweight servers.
- If you want me to create a branch that

```

Notes:

- This draft was generated automatically to help triage files removed from `donerefs.txt`.
- Backups and previous runs may exist under `.qmoi_validation`.
```

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
