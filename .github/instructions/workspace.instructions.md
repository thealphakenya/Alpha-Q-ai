# Workspace instructions

## Purpose

Keep the workspace safe, deterministic, and consistent with the repository’s remote-first policy.

## Required behavior

- Prefers metadata, hashes, and deltas over large downloads.
- Respect user edits and active locks.
- Use narrow validation before broad validation.
- Track local and remote divergence explicitly.
- Separate “planned” status from “verified” status.
- Inventory and read all repository instructions before protected work; record path, scope, hash, and read outcome without copying policy text into telemetry.
- Preserve human-authored instructions; automation may update generated status and evidence only unless an authorized policy change explicitly says otherwise.
- Keep autonomous retries bounded and checkpointed; retain authorization blockers instead of spinning or self-approving.
- For App work, preserve user-authored credentials notes and inspect `githubapppermissions.md` as a reported snapshot; record whether each fact is user-reported, locally observed, or remotely verified.
- Keep `or.md`, `oe2.txt`, `githubapp.md`, `github.md`, `CREDENTIAL_READINESS.md`, and `remotecompletion.md` aligned on current App variable presence, installation-ID availability, rotation state, secret-list access, and exact local/remote SHA.
- Do not claim Copilot Chat or Ollama can authenticate merely because a Codespaces secret is present. Use a value-free preflight, approved secret source, short-lived scoped token, and independent identity/API evidence; preserve `AUTH_BLOCKED` when any gate is unavailable.
- Never overwrite dirty user work or replace missing remote configuration with inferred credentials. QMOI may automate inventories and setup checklists, but provider-issued values require authorized owner/provider action.

## Required files

- `remotecompletion.md`
- `oe2.txt`
- `MERGE.md`
- `RELEASES.md`
- `ALLVALIDATIONS.md`
- `ALLMDFILESREFS.md`

## QAUDITS workspace evidence

- Run QAUDITS before and after broad documentation/runtime work to capture baseline and resulting local tree, path coverage, hashes, structural findings, duration, and explicit ignored/unreadable/skipped/bounded inputs.
- Keep generated artifacts and mutable self-referential evidence out of their own source digests through declared path-only exclusions; record artifact and paired-ledger hashes separately. Never count excluded data as scanned.
- Refresh `oe2.txt`, `remotecompletion.md`, `remote-completion.json`, `remote-evidence-ledger.jsonl`, and related generated inventory docs from the same operation/correlation. Preserve pre-existing user edits and report partial-write failures explicitly.
- Use deterministic bounded shards and resume from verified checkpoints. Do not infer complete coverage from speed, caches, local tree state, or a count of discovered files.
- On every full `audit-inventory` refresh, regenerate `ALLMDFILESREFS.md` category assignments from materialized Markdown paths/content and refresh the financial-document catalog plus the managed finance evidence section in `FINANCIALMANAGER.md`. Bind financial candidate artifacts to the same checkpoint; report incomplete or excluded sources rather than implying full country/currency coverage.
- Long inventory commands must write a paired `IN_PROGRESS` checkpoint before scanning and finalize under that correlation ID; if interrupted, retain the unfinished checkpoint as the current state.
- Remote completion remains blocked until exact repository/ref/SHA, terminal target-owned workflow result, remote tree/artifact verification, and required authority/security gates are independently evidenced.
- For long QAUDITS runs, record phase timing and the active correlation ID in paired evidence; avoid concurrent duplicate full-tree scans and use deterministic, bounded work where available. Keep user-edited mission content intact, preserve the mission mirror byte-for-byte, and retain interrupted scans as `IN_PROGRESS` until a fresh run reaches a terminal checkpoint.
- CodeQL fast-path integration is read-only: reuse exact-SHA workflow metadata already fetched, never launch a duplicate analysis, and keep alert API 403/404 or stale/missing runs explicitly unknown/incomplete.

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

## Mission roadmap

- Follow the canonical [root mission](../../MISSION.md) and keep `.github/instructions/MISSION.md` byte-identical to it; the focused regression enforces both mirror parity and instruction links. This file's workspace preservation, checkpoint, and remote-first rules remain controlling.
