---
title: "Issue draft for qmoi-enhanced/scripts/enhanced-build.py"
generated: 2025-11-08T16:06:38.814141Z
---

# Review needed: qmoi-enhanced/scripts/enhanced-build.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.054866Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.054866Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.054866Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""
Enhanced QMOI Build Script with Cloud Integration and Error Fixing
Fixes all build issues including permission errors and vulnerabilities
"""

import os
import sys
import subprocess
import shutil
import time
import json
import requests
import tempfile
import zipfile
from pathlib import Path

class QMOIEnhancedBuilder:
    """Enhanced builder with cloud integration and error fixing"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.temp_dir = tempfile.mkdtemp()

    def clean_build_directories(self):
        """Clean build directories to fix permission issues"""
        print("üßπ Cleaning build directories...")

        # Kill any running processes that might lock files
        try:
            subprocess.run(["taskkill", "/F", "/IM", "qmoiexe.exe"],
                         capture_output=True, check=False)
        except:
            pass

        # Wait a moment for processes to terminate
        time.sleep(2)

        # Remove directories with retry logic
        for directory in [self.dist_dir, self.build_dir]:
            if directory.exists():
                for attempt in range(3):
                    try:
                        shutil.rmtree(directory)
                        print(f"‚úÖ Cleaned {directory}")
                        break
                    except PermissionError:
                        print(f"‚ö†Ô∏è Permission error on attempt {attempt + 1}, retrying...")
                        time.sleep(1)
                        if attempt == 2:
                            # Force remove with master privileges
                            try:
                                subprocess.run(["rmdir", "/S", "/Q", str(directory)],
                                             shell=True, check=True)
                                print(f"‚úÖ Force cleaned {directory}")

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
