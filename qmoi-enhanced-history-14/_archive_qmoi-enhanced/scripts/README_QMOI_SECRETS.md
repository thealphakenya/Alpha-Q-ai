---
title: "or if keyring not available:"
qmoi_validation_frontmatter: true
---

<!-- LION_VALIDATION_START -->

## 🦁 L — Validated by QMOI Lion

- validated: yes
- validator: QMOI Lion
- timestamp: 2025-10-25T00:32:32.231969Z
- note: Auto-inserted by `scripts/autotag_md_with_lion.py` (creates .bak backup)
<!-- LION_VALIDATION_END -->

QMOI Secrets & Link tools

This folder contains small helper scripts that enable encrypted secret storage for QMOI and
updating repository links using the live ngrok tunnel.

Files:

- qmoi_secret_manager.py - helper to generate/lookup master key, encrypt/decrypt secrets using Fernet
- qmoi_bootstrap_secrets.py - CLI to generate a master key and encrypt an ngrok token to `.qmoi/ngrok_token.enc`
- update_links_with_ngrok.py - replaces any ngrok links in files listed in `ALLMDFILESREFS.md` with the live ngrok URL found in `.qmoi/ngrok_tunnel.json` or `ngrok_tunnel.txt`.

Requirements (recommended):

- python3.10+
- Install dependencies for secrets tooling:

```bash
pip install -r scripts/requirements-secrets.txt
```

Bootstrap example (local machine):

```bash
python3 scripts/qmoi_bootstrap_secrets.py --token "<NEW_NGROK_TOKEN>" --store-keyring
# or if keyring not available:
python3 scripts/qmoi_bootstrap_secrets.py --token "<NEW_NGROK_TOKEN>"
# copy the printed export to your environment or CI secrets
```

After ngrok is running and `start_qmoi_ngrok.py` has written `.qmoi/ngrok_tunnel.json`:

Dry-run link update:

```bash
python3 scripts/update_links_with_ngrok.py --dry-run
```

Apply changes:

```bash
python3 scripts/update_links_with_ngrok.py --apply
```

Notes:

- For production use, integrate the master key into a cloud secret manager and modify `qmoi_secret_manager.py` to fetch from that service.
- Rotate the ngrok token if it had been accidentally committed.

<!-- QMOI_VALIDATION_START -->

{
"file": "qmoi-enhanced/scripts/README_QMOI_SECRETS.md",
"validated_at": "2025-10-26T20:51:24.871159Z",
"validator": "QMOI Lion (automated)",
"checks": [
{
"name": "title_present",
"ok": false,
"detail": "No H1 title found"
},
{
"name": "links",
"ok": true,
"detail": []
}
],
"passed": false,
"summary": {
"total_checks": 2,
"passed": false
}
}

<!-- QMOI_VALIDATION_END -->

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
