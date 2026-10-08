---
title: "Issue draft for scripts/generate_revenue_spec.py"
generated: 2025-11-08T16:06:38.968063Z
---

# Review needed: scripts/generate_revenue_spec.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.117025Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.117025Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.117025Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""Enhanced revenue specification generator for QMOI.

This script scans repository Markdown files for revenue-related information and generates
a structured revenue specification document. Features:

- Identifies monetary amounts, revenue mentions, and payment systems
- Conservative by default (generates .generated.md in dry-run mode)
- Provides both human-readable Markdown and machine-readable JSON output
- Supports environment-based configuration via tools/lion.env

Usage:
  python3 scripts/generate_revenue_spec.py --out docs/REVENUE_SPEC.md --root .
  LION_APPLY=1 python3 scripts/generate_revenue_spec.py  # applies changes
"""
import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

# Comprehensive revenue-related keywords
KEYWORDS = {
    'revenue_terms': [
        'revenue', 'profit', 'income', 'earnings', 'monetization',
        'daily target', 'daily profit', 'projection', 'forecast'
    ],
    'payment_systems': [
        'wallet', 'cashon', 'mpesa', 'paypal', 'payment', 'transfer',
        'trading', 'payout', 'subscription', 'sale'
    ],
    'currencies': [
        'KSH', 'KES', 'USD', 'EUR', '$', 'master'
    ]
}

# Regex for monetary amounts with currency
AMOUNT_RE = re.compile(
    r'((?:KSH|KES|USD|EUR|\$)\s*\d[\d,]*|\d[\d,]*\s*(?:KSH|KES|USD|EUR))',
    re.IGNORECASE
)
def load_dotenv(root: Path) -> Dict[str, str]:
    """Load environment variables from tools/lion.env or .env files.

    Environment variables in the OS take precedence over file-based configuration.
    Returns a merged dictionary of environment variables.
    """
    candidates = [root / 'tools' / 'lion.env', root / '.env']
    env = {}

    # Load from first existing env file
    for p in candidates:
        if p.exists():
            for line in p.read_text(encoding='utf8').splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:

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
