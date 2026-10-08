---
title: "Issue draft for qmoi-enhanced/app/api/qmoi/auto-fix/start/route.ts"
generated: 2025-11-08T16:06:38.784607Z
---

# Review needed: qmoi-enhanced/app/api/qmoi/auto-fix/start/route.ts

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.022427Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.022427Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.022427Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { writeFileSync } from 'fs';
import os from 'os';

function requireApiKey(request: NextRequest) {
  const key = request.headers.get('x-qmoi-api-key') || '';
  const expected = process.env.QMOI_API_KEY || '';
  if (!expected) return true;
  return key === expected;
}

async function writeProposal(proposal: any) {
  try {
    const dir = '.qmoi_validation';
    if (!fs.existsSync(dir)) fs.mkdirSync(dir);
    const file = path.join(dir, 'auto_fix_proposals.json');
    let agg: any[] = [];
    if (fs.existsSync(file)) {
      try { agg = JSON.parse(fs.readFileSync(file, 'utf8') || '[]'); } catch (e) { agg = []; }
    }
    agg.push(proposal);
    fs.writeFileSync(file, JSON.stringify(agg, null, 2), 'utf8');
  } catch (err) {
    console.error('Failed to write auto-fix proposal:', err && (err as any).message ? (err as any).message : err);
  }
}

export async function POST(request: NextRequest) {
  try {
    if (!requireApiKey(request)) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

    const scriptPath = path.join(process.cwd(), 'scripts', 'qmoi_auto_fix_enhanced.py');

    if (!fs.existsSync(scriptPath)) {
      return NextResponse.json({ error: 'Auto-fix script not found' }, { status: 404 });
    }

    const canRun = process.env.PRODUCTION_CONFIRMED === 'true' && process.argv.indexOf('--real') !== -1;
    const proposal = { type: 'start_auto_fix', script: scriptPath, requestedAt: new Date().toISOString(), willRun: !!canRun };
    if (!canRun) {
      await writeProposal(proposal);
      return NextResponse.json({ status: 'proposed', message: 'Auto-fix start proposed (dry-run)' });
    }

    // Start the auto-fix process (careful: server environments may not allow spawn)
    const child = spawn('python', [scriptPath], { cwd: process.cwd(), stdio: ['ignore', 'pipe', 'pipe'] });

    child.stdout.on('data', (d) => console.log('[auto-fix]', d.toStr
```

Notes:

- This draft was generated automatically to help triage files removed from `donerefs.txt`.
- Backups and previous runs may exist under `.qmoi_validation`.

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
