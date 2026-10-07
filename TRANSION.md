# TRANSION.md

## Purpose and scope

This document defines the transition plan for the active QMOI styles and universals migration. It is a governance and planning artifact, not proof of completion. Every entry below distinguishes discovered candidates, planned replacements, verified replacements, and remote-verified results. The agent must continue only when each step has a matching QAUDITS pass, exact-path record, test/hook mapping, and remote evidence or a written blocker.

## Canonical style/universal replacement catalog

The style and universal layer is the shared contract for the active repository, historical sources, cloned platforms, and cross-repo product surfaces. Planned and candidate coverage includes the primary documents and directories below.

### Canonical documents treated as style and universal authority

- [STYLES.md](STYLES.md)
- [UNIVERSAL.md](UNIVERSAL.md)
- [UNIVERSALS.md](UNIVERSALS.md)
- [QAUDITS.md](QAUDITS.md)
- [QVERSIONMANAGER.md](QVERSIONMANAGER.md)
- [ALLAUTO.md](ALLAUTO.md)
- [AUTODEV.md](AUTODEV.md)
- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [OFCA.md](OFCA.md)
- [ALLTESTSAUTOTESTS.md](ALLTESTSAUTOTESTS.md)
- [ALLHOOKSWEBHOOKS.md](ALLHOOKSWEBHOOKS.md)
- [COMPONENTS.md](COMPONENTS.md)
- [TREE.md](TREE.md)
- [APP_LINKS.md](APP_LINKS.md)
- [VERCELLINKS.md](VERCELLINKS.md)
- [API.md](API.md)
- [ENDPOINTS.md](ENDPOINTS.md)
- [ROUTES.md](ROUTES.md)
- [ALLPORTS.md](ALLPORTS.md)
- [INTERNALRESEARCH.md](INTERNALRESEARCH.md)
- [EXTERNALRESEARCH.md](EXTERNALRESEARCH.md)

### Directories and registry paths participating in the transition

- `.github/instructions/`
- `scripts/`
- `tests/`
- `ollamatracks/`
- `QMOItracks/`
- `qmoi-enhanced-history-14/`
- `Alpha-Q-ai-2025/`
- `QMOI/`-like generated registry surfaces and category-driven indexes

### Replacement lineage status model

- `candidate`: discovered by file naming, path structure, hash, or content pattern; not assumed to be implemented
- `planned_replacement`: approved for review, test mapping, and rollback planning
- `verified_replacement`: has path, source/destination map, tests, hook applicability review, owner, and exact SHA evidence
- `remote_verified`: verified by target-owned workflow evidence for the exact repository and ref
- `blocked`: missing review, missing tests, missing remote verification, or conflicting ownership

### Metrics baseline and counts

The exact counts below are local discovery baselines and must be regenerated and revalidated before any production replacement claim is made.

- Candidate file entries: `pending regeneration from materialized scan`.
- Candidate directory entries: `pending regeneration from materialized scan`.
- Verified replacements: `0` (local evidence must create a verified file/directory lineage before this count changes).
- Pending replacement records: `pending`.
- Skipped/unreadable/oversized sources: `pending`.
- Feature IDs requiring test mapping: `pending`.
- Hook/webhook reviews required: `pending`.
- Remote-verified release/deploy/install evidence: `pending`.

## Required transition enhancements

1. Create a canonical style/universal registry with one source-of-truth path for app, platform, clone, and access-mode coverage.
2. Add deterministic naming crosswalks for Markdown, generated docs, and historical snapshots so basename collisions are visible and must be reviewed rather than silently replaced.
3. Add a step-by-step QAUDITS gate before every automation stage: inspect requirements, source paths, tests, hooks, policies, and exact evidence before continuing.
4. Synchronize `ALLMDFILESREFS.md` category assignments with the QAUDITS inventory so style, universal, test, hook, finance, monitoring, and Q-version entries are tracked together rather than in isolated files.
5. Enforce a verified replacement ledger in which every replacement record includes source path, destination path, prior SHA-256, new SHA-256, owner, reason, tests, rollback, authorization, repo/ref/SHA, and remote evidence.
6. Add per-step metrics for candidate files, directories, style counts, universal counts, extension counts, and unmapped features so no coverage is omitted.
7. Add a lifecycle gate in `QVERSIONMANAGER.md` requiring `PRODUCT_PLATFORM_CATALOG`, `LION_AND_EXTENSION_VARIANTS`, `RELEASE_DELIVERY_LIFECYCLE`, and `QTEAM_ACCOUNTABILITY` to pass before any finalization.
8. Add QAUDITS-specific policy that every claim is tagged as `candidate`, `mapped`, `verified`, `review_required`, or `remote_verified` and that local-only discovery never upgrades to remote completion.
9. Extend the agent to generate and refresh the full style/universal candidate tree without self-referential hash drift and without counting the generated report as replacement proof.
10. Extend the canonical docs to mention every new style/universal file and directory and every discovered candidate in a reviewable inventory section.
11. Add release/build/install/download/deploy lifecycle checks so QAUDITS verifies not just code presence but production readiness and distribution evidence.
12. Add human and automation accountability tracking for QTeam/friendship/master ownership, role boundaries, and protected actions so no universal or style change bypasses authorization.
13. Add an explicit orphan and duplicate rule: name-only matches must be listed as unresolved until the path and lineage are checked against the item’s canonical owner and target scope.
14. Add continuity metrics for success/failure record counts, skipped sources, and unresolved features so the agent can safely resume without losing evidence.

## Transition execution plan

1. Regenerate the style/universal candidate inventory and its directory tree from materialized paths only.
2. Normalize the `.md` naming crosswalk and classify each match by category, source scope, and status.
3. Reconcile `STYLES.md`, `UNIVERSAL.md`, `UNIVERSALS.md`, `QAUDITS.md`, and `QVERSIONMANAGER.md` against the inventory and categorization model.
4. Add `TRANSION.md` to the canonical documentation set and reference it from every relevant managed section.
5. Require a QAUDITS pass before every additional step and record the missing items as blockers rather than treating them as resolved.
6. Validate generated path trees, hashes, and cross-refs before any replacement is approved.
7. Generate the verified replacement ledger only when tests, rollback, authorization, and remote evidence are present.
8. Run the target suite and record the exact result before marking a step complete.
9. Re-read the branch- and repo-level evidence and update the local evidence artifacts after each step.
10. Stop finalization unless the exact remote SHA, workflow evidence, and branch authorization are all recorded and independently verified.

## Required documentation references

This transition plan must remain consistent with:

- [QAUDITS.md](QAUDITS.md)
- [STYLES.md](STYLES.md)
- [UNIVERSAL.md](UNIVERSAL.md)
- [UNIVERSALS.md](UNIVERSALS.md)
- [ALLAUTO.md](ALLAUTO.md)
- [AUTODEV.md](AUTODEV.md)
- [ALLMDFILESREFS.md](ALLMDFILESREFS.md)
- [QVERSIONMANAGER.md](QVERSIONMANAGER.md)
- [OFCA.md](OFCA.md)
- [ALLTESTSAUTOTESTS.md](ALLTESTSAUTOTESTS.md)
- [ALLHOOKSWEBHOOKS.md](ALLHOOKSWEBHOOKS.md)
- [INTERNALRESEARCH.md](INTERNALRESEARCH.md)
- [EXTERNALRESEARCH.md](EXTERNALRESEARCH.md)
- [MERGE.md](MERGE.md)
- [production.md](production.md)
- [productionenhanced.md](productionenhanced.md)

## Final governance note

This plan intentionally keeps replacement discovery fail-closed: the system can count, review, and document candidates, but it must not convert them into replacements without verified metadata, test coverage, policy alignment, and exact-SHA evidence. Local generation and historical scan results remain advisory until a target-owned workflow proves the exact remote state.
