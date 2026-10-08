# Build & Test Instructions

## Build Environment Status

### Current Container / CI

- **Node.js:** Recommended 18.x or 20.x (CI uses Node 18 by default)
- **npm:** 9.x or later recommended
- **Python:** ✓ Available (used for local testing of dashboards)

> Note: Local Codespaces may have limited memory; heavy Next.js production builds are more reliable on a CI runner (see the included GitHub Actions workflow). If you have trouble building locally, use CI or a larger machine.

## Build Steps (Run on machine with Node.js 18+)

### Static preview (safe while production build fails locally)

If local Next.js production builds are unstable due to memory limits, you can run the lightweight static preview server:

```bash
npm run serve:static
# Open: http://localhost:3005
```

This serves `public/index.html` as a minimal preview while full build is performed in CI.

### 1. Install Dependencies

```bash
npm install
```

### 2. TypeScript Type Check (Optional but Recommended)

```bash
npx tsc --noEmit
```

### 3. Build Next.js Production Bundle

```bash
npm run build
```

**Expected output:**

```
✓ Compiled successfully
✓ Linting and type checking...
✓ Collecting page data...
✓ Generating static pages...
✓ Finalizing page optimization...

Route (kind)                    Size     First Load JS
┌ ○ /                          ...      ...
├ ○ /qcity                      ...      ...
├ ○ /chatbot                    ...      ...
└ ...
```

### 4. Verify Build Artifacts

```bash
# Check output directory exists
ls -la .next/

# Output should contain:
# - cache/
# - server/
# - static/
```

### 5. Test Production Bundle (Optional)

```bash
npm start
# Then open: http://localhost:3000
```

## Test Suite (if configured)

```bash
# Run Jest tests (if jest.config.js exists)
npm test

# Run Playwright E2E tests (if playwright.config.ts exists)
npm run test:e2e
```

## Lint & Format Check

```bash
# ESLint check
npm run lint

# Fix lint issues
npm run lint:fix

# Format code with Prettier (if configured)
npm run format
```

## Troubleshooting Build Issues

### Common Error 1: Missing TypeScript

```
error: Cannot find module 'typescript'
```

**Solution:**

```bash
npm install --save-dev typescript
npm run build
```

### Common Error 2: Module Not Found

```
error: Module not found: 'src/config/api'
```

**Solution:**

```bash
# Verify file exists
ls -la src/config/api.ts

# Verify tsconfig.json has correct paths
cat tsconfig.json | grep -A 2 '"paths"'
```

### Common Error 3: Next.js Image Optimization

```
error: Image optimization service unavailable
```

**Solution:**

```bash
# Use unoptimized images in dev/build
export NEXT_SKIP_VALIDATION=1
npm run build
```

## Post-Build Validation

### 1. Check Component Compilation

- All .tsx files in `components/` and `qmoi-enhanced/components/` should compile
- API adapters (`src/adapters/clientAdapters.ts`) should resolve correctly
- Config file (`src/config/api.ts`) should be accessible

### 2. Verify No Dead Imports

```bash
# Run build with verbose mode
npm run build -- --verbose 2>&1 | grep -i "error\|warning" | head -20
```

### 3. Check Bundle Size

```bash
npm run build
# Look for warnings about large chunks
```

## Environment Variables for Build

Create `.env.local` before building (see `.env.example`):

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENV=development
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build & Test
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
      - run: npm install
      - run: npm run build
      - run: npm run lint
      - run: npm test (if applicable)
```

## Summary

- **Build time:** ~2-5 minutes (depends on machine specs)
- **Node.js requirement:** 18.x or 20.x LTS
- **npm requirement:** 9.x or later
- **Disk space:** ~500MB for node_modules + .next build
- **Memory:** ~1GB for build process

**Next:** Once build succeeds locally, commit `.env.local` to `.gitignore` and push to repo.

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
