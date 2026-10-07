# QMOI Agent Instructions (Master / Sister / User)

This file provides clear, actionable agent-style instructions and examples for interacting with `qmoi` over curl. Use the `X-QMOI-ROLE` header or include a `system` message to set persona and privileges.

1. Greeting + Agent Action (Master)

Example: master issues a repo write (create file)

```bash
curl -s -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-QMOI-ROLE: master" \
  -d '{
    "model": "qmoi",
    "messages": [
      {"role":"system","content":"You are Master. Execute allowed repo actions and report results clearly."},
      {"role":"user","content":"Hello qmoi — please create a file at /abctesting.txt with the single line: 'Agent: created abctesting.txt' and then reply with the path and first line."}
    ]
  }'
```

2. Verification steps (what to expect in reply)

- A success confirmation message: e.g., "Created `/abctesting.txt` — first line: 'Agent: created abctesting.txt'"
- An entry appended to persistent memory (e.g., `qmoi_memory.json`) describing the performed action.

3. Security and policy

- Only deploy file-write agent handlers behind strong authentication and allow a limited set of master tokens or service accounts.
- Validate and sanitize requested file paths to avoid directory traversal.

4. Troubleshooting

- If the server returns a reply but the file is not present, ensure the server process has filesystem write permissions and that the action handler is implemented.
- Consult server logs under `logs/` for any action errors.

5. Example agent greeting sequence (Master then follow-up)

1) Master: "GREETINGS. Create file X and confirm."
2) QM0I -> creates file and replies with success.
3) Master: "Please run quick verification head -n 1 X"
4) QM0I -> replies with the file preview and stores the action in memory.

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
