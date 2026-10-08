# Component Consolidation Analysis

## Summary

- **Total duplicate files:** 154 across `components/` and `qmoi-enhanced/components/`
- **Status:** Most are NOT byte-identical (have diverged during development)
- **Recommendation:** Keep current structure but document as intentional for now; plan unification for future release

## Duplicate Files (154 total)

See DUPLICATE_COMPONENTS.txt for full list.

### Sample Duplicates Verified

- `GlobalMail.tsx` — byte-identical ✓ (can consolidate immediately)
- `EmergencyPanel.tsx` — different (likely recent patches were only applied to one)
- `QmoiMediaManager.tsx` — different (likely recent patches were only applied to one)

## Consolidation Strategy (Recommended)

### Option A: One-shot consolidation (recommended for current iteration)

1. Run diff check on all 154 files to categorize:
   - Identical → keep single copy, remove duplicate
   - Different → merge changes into one, remove other
   - Intentional forks → document exception

2. Update all imports across codebase to point to single location

3. Delete duplicate directory structure

### Option B: Gradual consolidation (lower risk, more time)

1. Document current state in this file
2. During refactoring, consolidate one component at a time
3. Update imports incrementally
4. Reduce code duplication over time

## Current Recommendation

**For this iteration:** Keep both directories as-is but document that they should be consolidated.

**For next iteration:** Run automated diff analysis to:

```bash
# For each duplicate, show diff
for file in $(cat DUPLICATE_COMPONENTS.txt); do
  echo "=== Comparing: $file ==="
  diff -u "./components/$file" "./qmoi-enhanced/components/$file" | head -20
done
```

Then decide per-file whether to:

- Keep in `components/` (source of truth)
- Keep in `qmoi-enhanced/` (special enhancements)
- Merge both versions

## Affected Files (By Status)

### Tier 1: High-value consolidation targets

- GlobalMail.tsx (byte-identical)
- GlobalFileTransfer.tsx
- PriceProductVerifier.tsx
- (other utilities that don't have UI-specific logic)

### Tier 2: Medium-effort consolidation

- EmergencyPanel.tsx
- QmoiMediaManager.tsx
- FloatingPreviewWindow.tsx
- (components with adapters that were recently updated)

### Tier 3: Low-priority

- QAvatar.tsx
- SettingsPanel.tsx
- BrowserInterface.tsx
- (large UI components that may have intentional forks)

## Notes

- The duplication is likely from a copy-paste scaffolding process during project setup
- Recent patches (adapter integration) may have been applied inconsistently; [AUTOFIXED by Ollama at 2026-07-26T00:54:34.517740Z]_PROD items were reviewed and marked for production follow-up where applicable
- Consolidating will reduce code maintenance overhead and prevent drift
- Both directories are currently active in imports (suggests coexistence is intentional)

## Next Actions

1. Verify build succeeds with current duplicate structure (see task 7)
2. If build succeeds, document duplication as acceptable technical debt
3. Create GitHub issue for future consolidation task
4. In next release, consolidate using Option A above

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
