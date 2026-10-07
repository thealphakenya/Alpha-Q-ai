---
title: "Issue draft for scripts/all_cloned_releases.py"
generated: 2025-11-08T16:06:38.959330Z
---

# Review needed: scripts/all_cloned_releases.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.104711Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.104711Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.104711Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""
Generate ALLCLONEDRELEASES.md from discovered markdown and platform data.

This is a safe, dry-run generator: it aggregates discovered platform PAYED
files, existing release notes and writes an audit JSON to
`.qmoi_validation/all_cloned_releases.json` and a markdown summary
`ALLCLONEDRELEASES.md` in repository root. It does not perform network calls.
"""
from pathlib import Path
import json
import re
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / '.qmoi_validation'
VALID.mkdir(parents=True, exist_ok=True)

OUT_MD = ROOT / 'ALLCLONEDRELEASES.md'
OUT_JSON = VALID / 'all_cloned_releases.json'

# We will consider any *PAYED.md and any CHANGELOG* or RELEASE* files as release sources
md_files = list(ROOT.glob('**/*PAYED.md'))
release_files = list(ROOT.glob('**/CHANGELOG*')) + list(ROOT.glob('**/RELEASE*'))

def short_info(path: Path):
    text = path.read_text(encoding='utf-8', errors='ignore')
    # find a short header or first bullet
    m = re.search(r"^#\s*(.+)$", text, re.M)
    first = m.group(1).strip() if m else text.splitlines()[0][:120]
    lines = len(text.splitlines())
    return {'path': str(path.relative_to(ROOT)), 'header': first, 'lines': lines}

data = {
    'generated_at': datetime.utcnow().isoformat() + 'Z',
    'payed_files': [short_info(p) for p in md_files],
    'release_files': [short_info(p) for p in release_files]
}

OUT_JSON.write_text(json.dumps(data, indent=2), encoding='utf-8')

lines = [f"# ALL CLONED RELEASES\n", f"Generated: {data['generated_at']}", '', '## PAYED files:']
for p in data['payed_files']:
    lines.append(f"- {p['path']} — {p['header']} ({p['lines']} lines)")

lines.append('')
lines.append('## Release / Changelog files:')
for r in data['release_files']:
    lines.append(f"- {r['path']} — {r['header']} ({r['lines']} lines)")

lines.append('')
lines.append('> NOTE: This file is generated in dry-run mode; run domain assigment and provisioning separately with explicit approval.')

OUT_MD.write_text('\n'.join(li
```

Notes:

- This draft was generated automatically to help triage files removed from `donerefs.txt`.
- Backups and previous runs may exist under `.qmoi_validation`.

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
