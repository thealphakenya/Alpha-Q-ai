# QSeed

## Purpose and status

QSeed is an optional, provenance-bound format for explicitly selected local
payloads. It complements Q-version lineage and memory/restore-point metadata; it
does not replace Git history, autosync backups, undo/redo journals, or a tested
restore point. Seed presence is not implementation, validation, authorization,
or remote-completion evidence.

The current local utility is
[`scripts/qseed_vault.py`](scripts/qseed_vault.py), callable through
`python scripts/ollama_autonomous_agent.py qseed ...`. It uses the
`cryptography` package's Fernet authenticated encryption. QSeed does not use a
home-grown or “QMOI-only” cipher, and this implementation makes no quantum-safe
claim.

## Key and payload safety

- Key creation and use are explicit CLI actions. Keys are owner-only files
  outside the repository; key material is never returned in output, stored in
  the repository, or copied into audit logs.
- Encryption accepts one explicitly named regular file per operation, has a
  16 MiB payload limit, authenticates the metadata and bytes together, and
  defaults to `~/.local/share/qmoi/qseeds/`.
- Decryption is an explicit action requiring an explicit output path outside
  the repository. Existing output files, symlink paths, invalid keys, and
  failed authentication are rejected.
- The repository stores this specification and utility, not key files or
  plaintext payloads. Ciphertext may contain sensitive data and should be
  backed up only under the owner's storage policy.
- The encrypted payload carries its source path, source SHA/ref when locally
  available, seed lineage, content digest, label, and timestamp. This metadata
  is encrypted with the payload. The public checkpoint records only operation
  status, encrypted-artifact integrity where relevant, and a correlation ID.

Example:

```text
python scripts/ollama_autonomous_agent.py qseed --repository-root . generate-key --key-file ~/.config/qmoi/qseed.key
python scripts/ollama_autonomous_agent.py qseed --repository-root . encrypt --input MEMORY_INDEX.md --key-file ~/.config/qmoi/qseed.key --kind memory
python scripts/ollama_autonomous_agent.py qseed --repository-root . audit
python scripts/ollama_autonomous_agent.py qseed --repository-root . decrypt --input ~/.local/share/qmoi/qseeds/<seed-id>.qseed --key-file ~/.config/qmoi/qseed.key --output ~/qseed-recovery/MEMORY_INDEX.md
```

Protect and independently back up the key before relying on a QSeed artifact.
Loss of the key makes the encrypted payload unrecoverable. Do not put key
values, decrypted content, source prose, or credential material in tickets,
checkpoints, or logs.

## Audit, research, and automation contract

QAUDITS inventories all indexed paths and creates a deterministic risk-priority
follow-up queue. It ranks unreadable/metadata-only, security/authorization,
financial, delivery/workflow, test-mapping, and memory/recovery/seed surfaces
ahead of baseline review, while preserving every indexed path in the queue.
Prioritization never removes lower-ranked work or produces a pass.

Deep-learning or local-model assistance may suggest review questions and
candidate mappings, but suggestions must be tied to exact input hashes, model
identity/version, prompt/policy version, and measured execution status. Model
output is untrusted candidate evidence; it cannot decide semantic truth,
decryption, authorization, replacement, or remote completion. Repository
content must not be sent to an external model without a separate explicit
authorization and data review. No automatic model-based pass is claimed by the
current deterministic queue.

The optional `qaudit-model-review` command can produce unverified suggestions
for one explicitly selected source through a literal loopback IP and an exact
model tag already installed on the local Ollama service. It requires an
explicit local-content consent flag, caps UTF-8 input at 32 KiB, caps findings
and response size, records model/version/digest and source hashes, and stores
only constrained category/severity/line-hash/recommendation data. It never
pulls a model, contacts external endpoints, edits source, or converts a
suggestion into a pass. See the optional review and low-data session controls
in [QAUDITS.md](QAUDITS.md).

Internal and external research remain separately sourced and timestamped.
External research is limited to the configured official-source allowlist and
bounded read-only requests; citations and research do not establish local
implementation or remote verification.

QSeed, restore-point, autosync, undo/redo, and evolution operations require
separate integrity checks and recovery tests. The Ollama autonomous agent may
perform safe local inventory and evidence refreshes, but it must stop at
missing keys, security findings, user authorization, inaccessible repositories,
or missing terminal exact-SHA evidence. Its checkpoint writer keeps
[`oe2.txt`](oe2.txt), [`remotecompletion.md`](remotecompletion.md),
`remote-completion.json`, and the append-only ledger correlated. Local evidence
does not prove remote completion.

## Repository scope

This checkout is `thealphakenya/Alpha-Q-ai`. `qmoi-enhanced-history-14/` is a
materialized historical snapshot, not a verified live second repository. This
file therefore does not claim that QSeed has been installed or verified in a
live `qmoi-enhanced` checkout. That repository's owner/workflow must apply and
validate its own QSeed documentation and implementation against its exact
remote SHA.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10446`; directories: `1270`; Markdown: `2418`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Managed-document family candidates: `app_platform=2156, build_download_install=2110, orchestration=2062, qteam_accountability=2050, release_tag_publish=2089, tree_inventory=2001`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2223`; needs review: `187`; metric candidate lines: `52718`; percentage occurrences: `22237`.
- Markdown word count: `3554796`; heuristic sentence count: `674081`; sentence records indexed: `674081`; sentence records beyond the bound: `0`.
- Sentence review candidates: `29838` metric claims; `10664` completion claims; `29741` metric and `10535` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `9047` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13342`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `40052` lines in `3673` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `290`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
