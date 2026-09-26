# ALLFRONTEND.md - Frontend Feature Map

## Purpose
This file captures the platform and UI features expected across the frontend-facing QMOI applications.

## Frontend Feature Areas
- user interface consistency
- platform-native styling
- responsive layouts
- avatar and live-state presentation
- monitoring and dashboard views
- operator and workflow controls

## QStore and QStream Coverage
- QStore's catalog UI requirements are tracked in `QSTORE.md` for Windows, macOS, Linux, iOS, Android, and Web.
- QStream's product/UI specification remains in `QSTREAM.md`; only its marked QMOI integration section is agent-maintained.
- `APP_LINKS.md` is the generated source-repository link registry. Repository links do not establish live download or deployment URLs.
- The autonomous agent refreshes these docs on validation runs but does not mark external app UI implementation verified without the source checkout and platform tests.

## Automation sync contract

The frontend inventory is not a static list. It is refreshed automatically as the
site, clone, and product catalog evolves. When the style layer updates, the
frontend contract must also refresh the relevant app surfaces, link labels,
feature expectations, and platform-specific UI state coverage. The active agent
must keep `STYLES.md`, `UNIVERSALS.md`, `APP_LINKS.md`, `QSTORE.md`, `QSTREAM.md`,
`QVILLAGE.md`, `QUANTUM.md`, and the platform docs synchronized with the same
feature inventory. This keeps all clone and hosted surfaces aligned with the
current QMOI identity and prevents missing or stale UI states.

## Priority
Frontend features must remain aligned with the live repository design and must not be lost during sync or merge operations.
