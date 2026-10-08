---
title: "Issue draft for scripts/update_ngrok_links.py"
generated: 2025-11-08T16:06:38.994468Z
---

# Review needed: scripts/update_ngrok_links.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.148693Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.148693Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.148693Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""
scripts/update_ngrok_links.py

Idempotent utility to scan the repository for occurrences of known ngrok/tunnel URLs and optionally rewrite them
to a new URL supplied via --new-url or taken from live_qmoi_ngrok_url.txt. Designed to be safe: supports --dry-run and
--apply modes, creates .bak timestamped backups for files it will modify.

Usage examples:
  python3 scripts/update_ngrok_links.py --dry-run --source live_qmoi_ngrok_url.txt
  python3 scripts/update_ngrok_links.py --apply --new-url https://3cf7294944e8.ngrok-free.app

This script intentionally avoids network calls and git pushes; a thin wrapper in the orchestrator can commit/push
if allowed.
"""
from __future__ import annotations

import argparse
import re
import sys
import os
import time
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
NGROK_PATTERN = re.compile(r"https?://[0-9a-zA-Z\-]+\.ngrok(?:-free)?\.app")


def find_candidate_files(root: Path) -> List[Path]:
    exts = {'.md', '.txt', '.py', '.js', '.json', '.html', '.webmanifest'}
    candidates: List[Path] = []
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in exts:
            candidates.append(p)
    return candidates


def scan_file_for_ngrok(path: Path) -> List[Tuple[int, str]]:
    matches: List[Tuple[int, str]] = []
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return matches
    for i, line in enumerate(text.splitlines(), start=1):
        if NGROK_PATTERN.search(line):
            matches.append((i, line.strip()))
    return matches


def replace_in_file(path: Path, old: str, new: str) -> bool:
    text = path.read_text(encoding='utf-8')
    if old not in text:
        return False
    # backup
    ts = time.strftime('%Y%m%dT%H%M%S')
    bak = path.with_suffix(path.suffix + f'.bak.{ts}')
    bak.write_text(text, encoding='utf-8')
    new_text = text.replace(old, new)
    path.write_text(new_text, encoding='utf-8')
    return True


def load
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
