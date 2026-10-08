---
title: "Issue draft for qmoi-enhanced/scripts/qmoi_git_wrapper.py"
generated: 2025-11-08T16:06:38.824709Z
---

# Review needed: qmoi-enhanced/scripts/qmoi_git_wrapper.py

Status: AUTOMATED_REMOVAL_FROM_DONEREFS

Suggested next steps:

- Inspect the file and its [AUTOFIXED by Ollama at 2026-07-26T18:54:42.064791Z] markers or [AUTOFIXED by Ollama at 2026-07-26T18:54:42.064791Z]s.
- If the file is safe for production, remove the [AUTOFIXED by Ollama at 2026-07-26T18:54:42.064791Z] and add tests / small PR.
- If the file is intentionally non-production (e.g. simulated or cache), consider moving it out of the repo or documenting its purpose.
- After changes, re-run `scripts/verify_and_finalize_done.py` to include the file back in `donerefs.txt`.

Excerpt (first 2KB):

```
#!/usr/bin/env python3
"""Lightweight git wrapper that ensures the encrypted GitHub token is used for https pushes.

Usage: replace calls to 'git' with 'python scripts/qmoi_git_wrapper.py git ...' or add an alias.
It intercepts push/pull/fetch commands and sets GIT_ASKPASS to a small helper that returns the token.
"""
import os
import sys
import subprocess
from pathlib import Path


def get_github_token():
    try:
        from scripts.qmoi_secret_manager import get_named_secret
    except Exception:
        return None
    return get_named_secret('github')


def write_askpass_helper(token: str) -> str:
    p = Path('.qmoi') / 'git-askpass-qmoi.sh'
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(f"#!/usr/bin/env bash\necho '{token}'\n")
    p.chmod(0o700)
    return str(p)


def main():
    if len(sys.argv) < 2:
        print('Usage: qmoi_git_wrapper.py git <git-args...>')
        sys.exit(1)

    # pass-through for non-network commands
    args = sys.argv[1:]
    needs_credentials = any(x in ('push', 'pull', 'fetch') for x in args)

    env = os.environ.copy()
    askpass = None
    if needs_credentials:
        token = get_github_token()
        if token:
            askpass = write_askpass_helper(token)
            env['GIT_ASKPASS'] = askpass
            # set username to x-access-token for GitHub
            env['GIT_USERNAME'] = 'x-access-token'

    # Run git command with env override
    cmd = ['git'] + args
    p = subprocess.Popen(cmd, env=env)
    p.wait()
    sys.exit(p.returncode)


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
