---
title: "Issue draft for scripts/qmoi-integrity-guardian.py"
generated: 2025-11-08T16:06:38.980188Z
---

# Review needed: scripts/qmoi-integrity-guardian.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.133517Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.133517Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.133517Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
def report_test_status():
    # Run QMoiKernelPanel tests and report status to GitHub
    result = run("npm test -- src/components/q-city/QMoiKernelPanel.test.tsx")
    if "FAIL" in result or "Error" in result:
        send_github_status(f"QMoiKernelPanel test failed: {result}")
    else:
        send_github_status(f"QMoiKernelPanel test passed: {result}")
#!/usr/bin/env python3
"""
qmoi-integrity-guardian.py
Automated script for continuous git integrity checks, workflow/hook validation, and scheduled backups.
"""
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

BACKUP_PATH = "/workspaces/qmoi-enhanced-backup-latest.tar.gz"
WORKFLOW_DIR = ".github/workflows"
HUSKY_DIR = ".husky"
CHECK_INTERVAL = 900  # seconds (15 min, adjustable)
CLOUD_BACKUP_PATH = "/workspaces/qmoi-cloud-backup-latest.tar.gz"
ALPHA_Q_AI_REMOTE = "alpha-q-ai"

WORKFLOW_TEMPLATES = {
    "build.yml": "# Recreated build workflow\nname: Build\non:\n  push:\n    branches:\n      - main\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v3\n      - name: Set up Python\n        uses: actions/setup-python@v4\n        with:\n          python-version: 3.12\n      - name: Install dependencies\n        run: pip install -r requirements.txt\n      - name: Run tests\n        run: pytest\n",
    # ...add other workflow templates as needed...
}
HUSKY_TEMPLATES = {
    "pre-commit": "#!/bin/sh\n# Recreated pre-commit hook\necho \"pre-commit hook triggered\"\n",
    "pre-push": "#!/bin/sh\n# Recreated pre-push hook\necho \"pre-push hook triggered\"\n",
    "post-checkout": "#!/bin/sh\n# Recreated post-checkout hook\necho \"post-checkout hook triggered\"\n",
    "post-commit": "#!/bin/sh\n# Recreated post-commit hook\necho \"post-commit hook triggered\"\n",
    "post-merge": "#!/bin/sh\n# Recreated post-merge hook\necho \"post-merge hook triggered\"\n",
}

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdou
```

Notes:

- This draft was generated automatically to help triage files removed from `donerefs.txt`.
- Backups and previous runs may exist under `.qmoi_validation`.

<!-- AUTOMATED-CHECK: 2025-11-11 11:36:36 UTC -->

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
