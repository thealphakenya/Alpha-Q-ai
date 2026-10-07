---
title: "Issue draft for tools/qmoi_lint.py"
generated: 2025-11-08T16:06:39.011316Z
---

# Review needed: tools/qmoi_lint.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.170312Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.170312Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.170312Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""QMOI lint runner: runs Python linters (flake8/autoflake), attempts JS/TS eslint when Node present,
and emits machine-readable and human-readable reports.

This script is conservative: in local runs it prefers to emit patches or reports rather than apply large changes.
In CI (`--ci`) it can attempt safer autofix operations.
"""
from pathlib import Path
import subprocess
import json
import sys
import shlex

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / 'tools'
REPORT_JSON = TOOLS / 'qmoi_lint_report.json'
REPORT_MD = TOOLS / 'qmoi_lint_report.md'
PATCH_DIR = TOOLS / 'patches'

def run_cmd(cmd, cwd=ROOT):
    print('> ' + cmd)
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=str(cwd))
    return res.returncode, (res.stdout or '') + (res.stderr or '')

def run_python_linters(ci=False):
    results = {'flake8': None, 'autoflake': None}
    # flake8
    rc, out = run_cmd('flake8 --version')
    if rc == 0:
        rc, out = run_cmd('flake8 --exit-zero .')
        results['flake8'] = {'rc': rc, 'output': out}
    else:
        results['flake8'] = {'rc': None, 'output': 'flake8 not installed'}

    # autoflake for safe fixes (remove unused imports) - only in CI or when asked
    if ci:
        rc, out = run_cmd('autoflake --version')
        if rc == 0:
            # run autoflake in-place for safe fixes; conservative flags
            rc, out = run_cmd('autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .')
            results['autoflake'] = {'rc': rc, 'output': out}
        else:
            results['autoflake'] = {'rc': None, 'output': 'autoflake not installed'}
    else:
        results['autoflake'] = {'rc': None, 'output': 'skipped (local run)'}
    return results

def find_eslint_candidate():
    candidates = []
    local = ROOT / 'node_modules' / '.bin' / 'eslint'
    if local.exists():
        candidates.append(str(local))
    candidates.append('npm exec --no-install eslint')
    candidates.append('npx eslint')
    candi
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
