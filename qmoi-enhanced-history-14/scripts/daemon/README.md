---
title: "Example systemd unit (place in /etc/systemd/system/qmoi-daemon.service):"
qmoi_validation_frontmatter: true
---

# QMOI daemon

This folder contains a lightweight daemon that orchestrates regular maintenance tasks used by QMOI. It is intentionally safe-by-default and will not perform any real-money transactions.

Tasks performed (dry-run):

- [AUTOFIXED by Ollama at 2026-07-20T02:07:46.805804Z: please review] scanner (`scripts/check_[AUTOFIXED by Ollama at 2026-07-20T02:07:46.805804Z: please review]s.py`)
- wallet quality verification (`scripts/wallets/check_wallets.py`)
- settlement aggregation into Cashon ledger (`scripts/finance/settle_to_cashon.py`) — dry-run only
- YAML/workflow validation (`scripts/validate_yml.py`)

## Running

One-shot dry-run (recommended for testing):

```bash
python3 scripts/daemon/qmoi_daemon.py --once
```

Continuous run (run under system supervisor like systemd or a process manager):

```bash
# Example systemd unit (place in /etc/systemd/system/qmoi-daemon.service):
[Unit]
Description=QMOI maintenance daemon (dry-run)
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/qmoi-enhanced
ExecStart=/usr/bin/python3 /path/to/qmoi-enhanced/scripts/daemon/qmoi_daemon.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

## Security & governance

- This daemon never passes production flags or environment variables that enable live transfers. Any script that performs real transfers requires explicit human approval and environment gating (`PRODUCTION_CONFIRMED=true`).
- For long-running, always-on operations you should deploy the daemon on a trusted VM or server (not a temporary codespace) and use a secret manager for credentials.


---
Automated update by Ollama agent at 2026-07-20T02:07:46.805804Z. Please review changes above.

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
