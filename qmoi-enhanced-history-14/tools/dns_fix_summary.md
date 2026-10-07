# DNS Fix Summary

Generated: 2025-11-20 (automated)

This file is an automated summary produced from `tools/dns_links_report.json`.

Key points:

- Total links checked: see `tools/dns_links_report.json` (`total` field).
- Failures: entries with empty `resolved_ips` or non-2xx HTTP status; see the JSON for details.

Top recommended actions:

- Verify DNS/A/AAAA/CNAME records for hosts that do not resolve (empty `resolved_ips`).
- Replace [AUTOFIXED by Ollama at 2026-07-26T18:54:41.404932Z] domains (e.g., `qmoigateway.example.com`, `your-app.vercel.app`, `codespaces`) with correct production hostnames or remove them from public docs.
- For `http://` links, prefer `https://`; use `tools/apply_link_fixes.py` to run a conservative dry-run and proposals.
- After fixes, re-run `python3 tools/check_links_clean.py` to regenerate the reports and validate.

Files for review:

- `tools/dns_links_report.json` — full details per-URL.
- `tools/dns_links_report.md` — human-readable failures list.
- `tools/dns_docs_inventory.json` — inventory of docs and links found.

If you want, I can apply conservative fixes automatically (create branch + commit). Ask me to apply fixes and push or to open a PR.

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
