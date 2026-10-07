# Q Audits

## Styles/universals audit gate and transition awareness

The QAUDITS layer must perform a full step-level audit before any style, universal, release, or Q-version action advances. The required gate includes app/platform coverage, access-mode classification, UI styling and token coverage, universal capability mapping, test and hook coverage, release/build/install/download/deploy evidence, QAUDITS category membership from [ALLMDFILESREFS.md](ALLMDFILESREFS.md), and exact-SHA validation. A discovered candidate is never treated as implemented or replaced without a verified lineage record.

The transition plan is documented in [TRANSION.md](TRANSION.md). This plan includes the same naming crosswalk, directory/file inventory, source/destination lineage, and metrics model used by QAUDITS and the style/universal layer so that no file, directory, or category is silently omitted.

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `10413`; directories: `1267`; Markdown: `2413`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `553`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Markdown structural checks passed: `2186`; needs review: `219`; metric candidate lines: `46842`; percentage occurrences: `22236`.
- Formula/calculation candidate lines: `11373`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `QMOItracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `36455` lines in `3093` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `285`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
