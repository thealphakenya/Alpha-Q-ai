# ALLPORTS.md - Port and Service Map

## Purpose
This file documents the expected port and service layout for the QMOI project and its supporting automation environment.

## Standard Port Map
- 8000: primary local service port
- 8080: monitoring / status service
- 3000: frontend or dashboard layer
- 5000: API or local automation service
- 5432: PostgreSQL or local DB service (if present)
- 6379: cache / queue service (if present)
- 11434: Ollama local runtime API/default host
- 8081: alternate health/telemetry service
- 9000: local automation or self-healing gateway
- 9090: metrics or observability endpoint

## Ollama autonomous agent runtime port and merge usage

The Ollama autonomous agent must include the active repo, the historical archive, and the markdown inventory in its operational checks, and it must confirm that no merge step conflicts with the expected runtime ports. The agent should treat the active port map as a contract, validate route and endpoint alignment, and compare the live repo with the historical archive before migrating any recovered feature into the active repo.

## QMOI Runtime Port Usage
- Local dev and validation flows: 8000, 8080, 5000
- Ollama runtime: 11434
- GitHub-hosted automation: dynamic ephemeral runner ports, not permanent repo ports
- Historical repo snapshots: use repo-local config, not fixed service ports

## Notes
Ports are documented as operational defaults and may vary by environment, but the names and roles remain stable across the repo stack, the autonomous runtime, and the historical archive inventory.

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
