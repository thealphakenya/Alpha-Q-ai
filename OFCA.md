# Ollama Full Coverage Audit (OFCA)

OFCA is a required pre-merge audit stage. The agent runs it after source inventory and before merge planning or file-merge activity, records it as `OLLAMA_FULL_COVERAGE_AUDIT` in the Q-version lifecycle, and sets `prMergeIncluded` in merge evidence.

Merge planning and read-only inventory may continue when the audit is incomplete, but merge application is blocked unless OFCA and the Markdown source index are complete. The blocked lifecycle stage retains its reasons and resumable next action.

The metadata-only report in `ollamatracks/ollama_reference_audit.json` records mention-bearing paths, hashes, line numbers, responsibility categories, local ref and commit counts, and a source-manifest hash. It never copies source lines into evidence. `ollamatracks/style_universal_replacement_inventory.json` tracks candidate files and directories, hashes, source scope, and required test/hook review for migration to `STYLES.md`, `UNIVERSALS.md`, and `UNIVERSAL.md`.

## Coverage boundaries

- A materialized-tree scan is local scope, not all-history proof.
- Local refs and commit-diff scans do not prove remote-ref freshness, every pull request, every intermediate commit tree, or coverage in an unavailable peer repository.
- Missing, unreadable, oversized, or unenumerated sources remain explicit blockers; local audit status cannot be promoted to complete by inference.
- A match is a candidate responsibility record, not proof of a defect or a reason to rewrite a file.
- Style/universal candidates require ownership, compatibility, accessibility/security, focused tests, hook/webhook applicability, rollback, and authorization review before changes.
- Test and hook discovery is not coverage. A feature remains unmapped until implementation, positive/negative tests, event behavior, and exact-SHA validation are linked.
- Merge, release, deployment, credential, financial, and protected-branch actions remain subject to their existing authorization and evidence gates.

## Q version gate

Q version lifecycle gate 21 requires OFCA on each merge execution. Finalization additionally requires terminal target-owned audit evidence for both repositories covering current refs, pull requests, and intermediate commit trees at exact final SHAs. Until that evidence exists, the audit stays `NEEDS_REVIEW` and Q-version finalization stays blocked.

<!-- BEGIN QMOI MANAGED: ollama-full-coverage-audit-status -->
## Agent-managed OFCA status

- Audit name: `OFCA`; local scan status: `PASS`.
- Materialized files scanned: `10384`; mention-bearing files: `4125`.
- Local refs: `37`; local commits: `2578`; mention-change commits: `1962`.
- Source manifest SHA-256: `3d1fc49a37f28083b89c2634bc247ef2111c64df1a2a1142205fe778b1c8547c`; full remote-history coverage: `False`.
- QVillage/QVS materialized references: `356` files, `205` Markdown files; remote/history completeness: `not_verified`.
- `prMergeIncluded` is required before merge activity. Unverified remote refs, pull requests, peer roots, and intermediate commit trees remain blockers.
- Next action: Run an authorized target-owned audit for both repositories covering all refs, PRs, and intermediate commit trees; attach terminal exact-SHA evidence before Q-version finalization.
<!-- END QMOI MANAGED: ollama-full-coverage-audit-status -->
