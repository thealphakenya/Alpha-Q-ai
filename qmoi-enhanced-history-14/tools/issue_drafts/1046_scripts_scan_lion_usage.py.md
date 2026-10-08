---
title: "Issue draft for scripts/scan_lion_usage.py"
generated: 2025-11-08T16:06:38.987330Z
---

# Review needed: scripts/scan_lion_usage.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.144060Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.144060Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.144060Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""Scan the repository for LION usage and related artifacts.

Produces `docs/lion_usage_report.json` with occurrences for quick triage.

This is conservative: read-only and safe to run in CI or locally.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'lion_usage_report.json'

PATTERNS = [
    r'\bLION\b',
    r'\blion\b',
    r'lionctl',
    r'lionlaunch',
    r'LIONOPERAT',
    r'LionOperating',
]

def scan_root(root: Path):
    report = {'root': str(root), 'checked_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z', 'matches': {}}
    for p in PATTERNS:
        report['matches'][p] = []

    for path in root.rglob('*'):
        if path.is_file():
            try:
                text = path.read_text(encoding='utf8', errors='ignore')
            except Exception:
                continue
            for pat in PATTERNS:
                if re.search(pat, text):
                    report['matches'][pat].append({'path': str(path), 'snippet': _grab_snippet(text, pat)})
    return report

def _grab_snippet(text, pat, max_len=160):
    m = re.search(pat, text)
    if not m:
        return ''
    start = max(0, m.start() - 40)
    end = min(len(text), m.end() + 40)
    return text[start:end].replace('\n', ' ')[:max_len]

def main():
    report = scan_root(ROOT)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding='utf8')
    print('Wrote', OUT)

if __name__ == '__main__':
    main()

```

Notes:

- This draft was generated automatically to help triage files removed from `donerefs.txt`.
- Backups and previous runs may exist under `.qmoi_validation`.

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
