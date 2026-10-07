# QSTORE.md

<!-- BEGIN QMOI MANAGED: qstore-catalog -->
## Catalog ownership

- The app catalog is generated from the active autonomous development agent's `QSTORE_CATALOG_APPS` registry.
- QStore includes every core QMOI app plus QStream; QStream's source repository is `thealphakenya/qstream`.
- Repository links identify source repositories only. They do not prove a build, download, public app URL, or deployment is available.
- The legacy four-app platform validator remains a separate compatibility contract. Catalog membership does not mean an external app implementation was checked out or tested.

## Managed app catalog

| App | Category | Source repository | Documentation | Implementation status |
| --- | --- | --- | --- | --- |
| `qmoiaiui` (QMOIAIUI) | ai | [repository](https://github.com/thealphakenya/qmoi-enhanced) | [QMOIAI.md](QMOIAI.md) | Implementation not verified by this workspace |
| `qcity` (QCity) | file-management | [repository](https://github.com/thealphakenya/qmoi-enhanced) | [QCITY.md](QCITY.md) | Implementation not verified by this workspace |
| `qmoi-space` (QMOI Space) | media | [repository](https://github.com/thealphakenya/qmoi-enhanced) | [QMOISPACE.md](QMOISPACE.md) | Implementation not verified by this workspace |
| `qalpha` (QALPHA) | development | [repository](https://github.com/thealphakenya/qmoi-enhanced) | [QALPHA.md](QALPHA.md) | Implementation not verified by this workspace |
| `qstream` (QStream) | entertainment | [repository](https://github.com/thealphakenya/qstream) | [QSTREAM.md](QSTREAM.md) | Implementation not verified by this workspace |
| `qvillage` (QVillage) | community | [repository](https://github.com/thealphakenya/qvillage) | [QVILLAGE.md](QVILLAGE.md) | Implementation not verified by this workspace |
| `quantum` (Quantum) | hosting | [repository](https://github.com/thealphakenya/Alpha-Q-ai) | [QUANTUM.md](QUANTUM.md) | Implementation not verified by this workspace |

## QStore UI feature coverage by platform

The agent refreshes this requirement matrix on every validation pipeline. Requirements are not implementation evidence; code-level UI tests are required before any platform is marked verified.

### windows

- [ ] Search and filter by app name, category, platform, and availability.
- [ ] Accessible app cards and detail views with version, publisher, and source.
- [ ] Platform compatibility and minimum-requirement indicators.
- [ ] Release history, changelog, and update-availability states.
- [ ] Install, update, cancel, retry, and rollback controls with progress and errors.
- [ ] Permission, privacy, license, and content-availability details before install.
- [ ] Package source and integrity metadata; do not imply verification without evidence.
- [ ] Keyboard, screen-reader, focus, contrast, and scalable-text support.
- [ ] QMOI recommendations that disclose their basis and respect user settings.
- [ ] Loading, empty, offline, restricted, and failed states with recoverable actions.
- [ ] Windows package and architecture compatibility.
- [ ] Keyboard navigation and native install/update handoff.

### macos

- [ ] Search and filter by app name, category, platform, and availability.
- [ ] Accessible app cards and detail views with version, publisher, and source.
- [ ] Platform compatibility and minimum-requirement indicators.
- [ ] Release history, changelog, and update-availability states.
- [ ] Install, update, cancel, retry, and rollback controls with progress and errors.
- [ ] Permission, privacy, license, and content-availability details before install.
- [ ] Package source and integrity metadata; do not imply verification without evidence.
- [ ] Keyboard, screen-reader, focus, contrast, and scalable-text support.
- [ ] QMOI recommendations that disclose their basis and respect user settings.
- [ ] Loading, empty, offline, restricted, and failed states with recoverable actions.
- [ ] macOS package and architecture compatibility.
- [ ] Signing/notarization state when independently verified.

### linux

- [ ] Search and filter by app name, category, platform, and availability.
- [ ] Accessible app cards and detail views with version, publisher, and source.
- [ ] Platform compatibility and minimum-requirement indicators.
- [ ] Release history, changelog, and update-availability states.
- [ ] Install, update, cancel, retry, and rollback controls with progress and errors.
- [ ] Permission, privacy, license, and content-availability details before install.
- [ ] Package source and integrity metadata; do not imply verification without evidence.
- [ ] Keyboard, screen-reader, focus, contrast, and scalable-text support.
- [ ] QMOI recommendations that disclose their basis and respect user settings.
- [ ] Loading, empty, offline, restricted, and failed states with recoverable actions.
- [ ] Linux package format and distribution compatibility.
- [ ] Package-manager handoff and dependency status.

### ios

- [ ] Search and filter by app name, category, platform, and availability.
- [ ] Accessible app cards and detail views with version, publisher, and source.
- [ ] Platform compatibility and minimum-requirement indicators.
- [ ] Release history, changelog, and update-availability states.
- [ ] Install, update, cancel, retry, and rollback controls with progress and errors.
- [ ] Permission, privacy, license, and content-availability details before install.
- [ ] Package source and integrity metadata; do not imply verification without evidence.
- [ ] Keyboard, screen-reader, focus, contrast, and scalable-text support.
- [ ] QMOI recommendations that disclose their basis and respect user settings.
- [ ] Loading, empty, offline, restricted, and failed states with recoverable actions.
- [ ] iOS device compatibility and official-store handoff.
- [ ] VoiceOver and system-permission disclosure.

### android

- [ ] Search and filter by app name, category, platform, and availability.
- [ ] Accessible app cards and detail views with version, publisher, and source.
- [ ] Platform compatibility and minimum-requirement indicators.
- [ ] Release history, changelog, and update-availability states.
- [ ] Install, update, cancel, retry, and rollback controls with progress and errors.
- [ ] Permission, privacy, license, and content-availability details before install.
- [ ] Package source and integrity metadata; do not imply verification without evidence.
- [ ] Keyboard, screen-reader, focus, contrast, and scalable-text support.
- [ ] QMOI recommendations that disclose their basis and respect user settings.
- [ ] Loading, empty, offline, restricted, and failed states with recoverable actions.
- [ ] Android device compatibility and official-store handoff.
- [ ] TalkBack and runtime-permission disclosure.

### web

- [ ] Search and filter by app name, category, platform, and availability.
- [ ] Accessible app cards and detail views with version, publisher, and source.
- [ ] Platform compatibility and minimum-requirement indicators.
- [ ] Release history, changelog, and update-availability states.
- [ ] Install, update, cancel, retry, and rollback controls with progress and errors.
- [ ] Permission, privacy, license, and content-availability details before install.
- [ ] Package source and integrity metadata; do not imply verification without evidence.
- [ ] Keyboard, screen-reader, focus, contrast, and scalable-text support.
- [ ] QMOI recommendations that disclose their basis and respect user settings.
- [ ] Loading, empty, offline, restricted, and failed states with recoverable actions.
- [ ] Responsive web catalog and installable-PWA state.
- [ ] Offline catalog state and browser-compatible install handoff.

## Per-app user access modes

These are access-state requirements for app UI generation, not claims that account systems or screens are implemented.

### qmoiaiui
- [ ] public guest interaction
- [ ] authenticated profile and private conversation controls
- [ ] Resolve the current server-verified identity, consent, and capability before rendering protected controls.
- Implementation status: not verified by this workspace.

### qcity
- [ ] public file-management information
- [ ] authenticated private files and workspace controls
- [ ] Resolve the current server-verified identity, consent, and capability before rendering protected controls.
- Implementation status: not verified by this workspace.

### qmoi-space
- [ ] public media discovery
- [ ] authenticated library, history, and account controls
- [ ] Resolve the current server-verified identity, consent, and capability before rendering protected controls.
- Implementation status: not verified by this workspace.

### qalpha
- [ ] public product/documentation views
- [ ] authenticated private projects and collaboration
- [ ] Resolve the current server-verified identity, consent, and capability before rendering protected controls.
- Implementation status: not verified by this workspace.

### qstream
- [ ] public catalog and permitted previews
- [ ] authenticated profiles, library, creator, and subscription controls
- [ ] Resolve the current server-verified identity, consent, and capability before rendering protected controls.
- Implementation status: not verified by this workspace.

## QStream entry

QStream is listed in this catalog and linked to [thealphakenya/qstream](https://github.com/thealphakenya/qstream). Its product specification remains in [QSTREAM.md](QSTREAM.md). No runtime or download URL is asserted until independently verified.

## Agent update contract

On each validation run, the autonomous agent refreshes this managed section, the QStream integration section, and `APP_LINKS.md`. It inventories every app above across all six declared platforms and reports implementation validation as unverified unless the corresponding source checkout and tests are available.
<!-- END QMOI MANAGED: qstore-catalog -->

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
