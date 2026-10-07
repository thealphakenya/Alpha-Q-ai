# MSW Testing Setup

This project uses MSW (Mock Service Worker) in tests with a runtime-friendly setup to avoid ESM/CommonJS loader issues when running tests under Next.js and Jest.

## Key concepts

- Handlers are exposed as an async factory: `export async function getHandlers() { /* ... */ }` so tests and `src/setupTests.ts` can dynamically import MSW at runtime and choose the right helpers (e.g., `rest` vs `http`).

- Tests wait for MSW readiness using the global readiness promise: `globalThis.__MSW_READY__`. `src/setupTests.ts` installs a `mswInitPromise` and sets `globalThis.__MSW_READY__ = mswInitPromise`.

- To avoid race conditions, `setupTests.ts` also wraps `global.fetch` so any test-initiated fetch will await MSW initialization automatically.

## Handler shape compatibility

Handlers are written defensively to support both `rest` (typical MSW API) and `http` helpers from `msw`:

- Prefer `res(ctx.status(...), ctx.json(...))` when `ctx` helpers are available.
- When not available (some `http` helper cases), handlers can return a real `Response` object (with `Headers`) so `fetch`/Xhr consumers can read headers, clone, etc.

## Env flags

- `TEST_VERBOSE=1` enables extra debug logging for handlers and fetch wrappers (helpful when diagnosing handler selection or request shapes).
- `SHOW_MSW_UNHANDLED=1` will allow MSW's `onUnhandledRequest` logging to be visible (off by default to reduce noisy logs in CI). Use it to track leaking real network calls.

## Troubleshooting

- If you see `UNHANDLED REQUEST` for `http://localhost/...`, ensure handlers also register absolute URLs in addition to path-only routes (e.g., both `/api/qmoi/status` and `http://localhost/api/qmoi/status`).
- If tests fail with `response.headers.get is not a function` or `response.clone is not a function`, handlers may be returning plain objects instead of real `Response` objects. Use the Response fallback or `res(ctx.*)`.

## Example

```js
// src/mocks/handlers.ts
export async function getHandlers() {
  const msw = await import("msw");
  const helpers = msw.rest || msw.http;

  return [
    helpers.get("/api/qmoi/status", (req, res, ctx) => {
      return res(ctx.status(200), ctx.json({ ok: true }));
    }),
    // absolute url variant
    helpers.get(
      "http://localhost/api/qmoi/status",
      (req) =>
        new Response(JSON.stringify({ ok: true }), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
    ),
  ];
}
```

---

If you'd like, I can add a short troubleshooting checklist to `CONTRIBUTING.md` or `START.md` as well.

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
