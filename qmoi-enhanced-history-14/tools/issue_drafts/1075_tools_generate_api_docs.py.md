---
title: "Issue draft for tools/generate_api_docs.py"
generated: 2025-11-08T16:06:39.011025Z
---

# Review needed: tools/generate_api_docs.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.169636Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.169636Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.169636Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""Generate a simple API endpoints markdown by scanning repository files for common route patterns.

This is heuristic and conservative: it looks for common patterns used by Flask, FastAPI, Express, and simple 'METHOD /path' lines.
It outputs a Markdown string to stdout.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

ROUTE_PATTERNS = [
    # Flask/Django style decorators and app.route
    re.compile(r"@.*route\(['\"](?P<path>/[^'\"]*)['\"](?:,\s*methods=\[(?P<methods>[^\]]*)\])?\)", re.IGNORECASE),
    re.compile(r"app\.route\(['\"](?P<path>/[^'\"]*)['\"](?:,\s*methods=\[(?P<methods>[^\]]*)\])?\)", re.IGNORECASE),
    # FastAPI/APIRouter decorators
    re.compile(r"@(router|app)\.(?P<method>get|post|put|delete|patch|options|head)\(['\"](?P<path>/[^'\"]*)['\"]", re.IGNORECASE),
    # Express style: app.get('/path', ...)
    re.compile(r"app\.(?P<method>get|post|put|delete|patch)\(['\"](?P<path>/[^'\"]*)['\"]", re.IGNORECASE),
    # Generic METHOD /path in comments or docs
    re.compile(r"\b(?P<method>GET|POST|PUT|DELETE|PATCH|OPTIONS|HEAD)\s+(?P<path>/[\w\-/{}:.]*)", re.IGNORECASE),
]

def scan_files():
    entries = []
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix in ('.py', '.js', '.ts', '.rst', '.md', '.yaml', '.yml'):
            try:
                txt = p.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                continue
            for pat in ROUTE_PATTERNS:
                for m in pat.finditer(txt):
                    method = m.groupdict().get('method') or ''
                    path = m.groupdict().get('path') or ''
                    methods = m.groupdict().get('methods') or ''
                    if methods:
                        # methods may be like '"GET", "POST"' or 'GET,POST'
                        methods = re.sub(r"[^A-Z,]", '', methods.upper())
                    entry = {'file': str(p.relative_to(ROOT)), 'method': (method or methods).upper(), 'path': path}

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
