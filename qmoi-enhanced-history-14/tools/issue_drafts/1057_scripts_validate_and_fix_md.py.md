---
title: "Issue draft for scripts/validate_and_fix_md.py"
generated: 2025-11-08T16:06:38.996663Z
---

# Review needed: scripts/validate_and_fix_md.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.151922Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.151922Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.151922Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""
scripts/validate_and_fix_md.py

Conservative validator and autofixer for Markdown files.

Features:
- Scans markdown files listed in docs/md_index.json (or finds .md files)
- Finds HTTP URLs and tests whether the HTTPS equivalent responds with HEAD
- Produces docs/link_report.json with findings and suggested safe fixes
- If --apply is passed, creates .bak backups and applies HTTPS upgrades where safe

Usage:
  python3 scripts/validate_and_fix_md.py --out docs/link_report.json [--apply] [--root .] [--timeout 5]

This script is intentionally conservative: it only auto-fixes http->https when
the https HEAD request returns <400. It never rewrites anchors or file paths.
"""
import argparse
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import urlparse

ROOT_DEFAULT = Path(__file__).resolve().parents[1]
OUT_DEFAULT = ROOT_DEFAULT / 'docs' / 'link_report.json'

URL_RE = re.compile(r"https?://[^)\s'\"]+")


def find_md_files(root: Path):
    idx = root / 'docs' / 'md_index.json'
    if idx.exists():
        try:
            j = json.loads(idx.read_text(encoding='utf8'))
            return [root / f['path'] for f in j.get('files', [])]
        except Exception:
            pass
    # fallback: glob
    return sorted(root.rglob('*.md'))


def check_https_equiv(url: str, timeout: int = 5) -> bool:
    if not url.startswith('http://'):
        return False
    https = 'https://' + url[len('http://'):]
    try:
        import urllib.request
        req = urllib.request.Request(https, method='HEAD')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status < 400
    except Exception:
        return False


def scan_and_fix(root: Path, out_path: Path, apply: bool = False, timeout: int = 5):
    files = find_md_files(root)
    findings = {'generated': None, 'files': []}
    for p in files:
        try:
            text = p.read_text(encoding='utf8')
        except Exception:
            continue
        urls = list(set(UR
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
