# QVILLAGE.md

QVillage is the live QMOI community, model, and knowledge coordination surface. It is treated as the master-only QMOI community layer that stays synchronized with GitHub, Hugging Face, and the live autonomous agent.

## Active automation
- QVillage sync remains a first-class automation surface inside QCity and the autonomous agent.
- memory, model, and runtime state are synchronized across repo docs and platform references.
- the live state is refreshed automatically as the repository evolves.

## Language and QLion research

`ALLLANGUAGES.md`, `ALLLANGUAGESCOMPARE.md`, and
`QLIONPROGRAMMINGLANGUAGE.md` define the local language inventory, decision
criteria, and QLion implementation status. A local candidate inventory is not
live external research or proof that a compiler/toolchain is supported.

### Research evidence contract

For each language or QLion compatibility observation, retain the official
source URL, subject, retrieval timestamp (UTC), observed release/support value,
content hash, parser/collector version, freshness deadline, and result status.
Prefer official language specifications, release notes, security advisories,
and toolchain documentation. External text is untrusted input; store
source metadata and concise reviewed findings rather than copying source
prose. Rate limits, timeouts, stale records, and unavailable sources must be
reported explicitly.

The requested realtime/scheduled language research and automatic QVillage
refresh are `NOT_IMPLEMENTED` and `NOT_VERIFIED` in this checkout. No current
language release version or supported-QLion claim is inferred. A future
worker must run with read-only least privilege, bounded requests and retries,
and explicit evidence freshness; it must not change compatibility claims,
generate executable bindings, or publish without validation and review.
Monitor candidate-source count, fresh/stale/unknown observations, retrieval
success/failure, latency, retries, content-hash changes, and downstream
validation outcomes separately. These are monitoring requirements, not
measured live service metrics.


<!-- BEGIN QMOI MANAGED: restore-point-memory-sync -->
## Restore-point memory and branch continuity

- Evidence status: `BLOCKED_MISSING_EVIDENCE`; source status: `UNKNOWN`.
- Workspace SHA: `unknown`; tree SHA: `unknown`; master verified: `False`.
- Source evidence: `QMOItracks/qmoi_restore_point_preflight.json`; SHA-256: `unavailable`; workflow run: `unknown`.
- Ref roles: `main` is the default branch, `autosync-backup` is the staging ref, `master` is the validated-main parity mirror, and `qmoi` is the post-success restore point.
- These records are last-observed metadata, not proof that a remote worker is live; stale, missing, partial, or unverified refs remain visible as blocked/review-required.

- Current blocker: No restore-point preflight artifact is available in this checkout.
<!-- END QMOI MANAGED: restore-point-memory-sync -->
