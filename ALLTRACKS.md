# ALLTRACKS.md

## Current local continuation status

This document remains a local, non-production evidence artifact. Monitoring, tracker, and feature mappings are still `NEEDS_REVIEW`; no live metric samples, provider connections, or remote completion proof were verified. The current mission is expired in local wall time, and exact remote SHA proof remains unavailable. This file should be used as a local review ledger, not as evidence of runtime success or production completion.

<!-- BEGIN QMOI MANAGED: alltracks-monitoring-inventory -->
## Agent-managed tracking, monitoring, and live-metric coverage

This report is a generated local inventory and implementation plan. Path discovery and source hashes do not prove that a monitor executes, that a metric is live/fresh, or that a feature is implemented.

- Status: `NEEDS_REVIEW`; scope: `materialized_nonignored_local_checkout`.
- Repository/ref/local HEAD: `Alpha-Q-ai` / `codespace-sturdy-fishstick-69wxr9jjgw5pfrq65` / `3c8479d87dfb5e35d665c8a7d88b4faa2dae1400`.
- Correlation ID: `7a77e4f3-448c-4801-ad77-b65306c958ab`; generated: `2026-10-16T19:46:23.956432Z`.
- Source-manifest SHA-256: `e0a00cfcb5d632986ece2627752a83e06a8d372114585efbc491a0c4c913e175`.
- Complete path-level references and hashes: `ollamatracks/alltracks_monitoring_inventory.json`.

### Calculated QAUDITS metrics

| Metric | Value | Formula / interpretation |
| --- | ---: | --- |
| Indexed materialized paths | 11575 | Enumerated local non-ignored scope only |
| Registered feature requirements | 404 | Registry denominator; not implementation count |
| Master UI requirements | 12 | Master dashboard/control requirements |
| Planned/unverified requirements | 138 | Future or not-yet-verified product requirements |
| UIS requirements | 41 | Requirements referenced by ID/line/hash, without copying source prose |
| Monitoring requirements | 595 | Registered, master UI, planned, and UIS requirements |
| Monitoring source candidates | 39 | Path candidates; execution not verified |
| Metric artifact references | 37 | Hashed file references; values were not read |
| Tracking document references | 18 | Local Markdown path candidates |
| Tracking artifacts referenced | 884 | Local JSON/JSONL/CSV files under tracker roots; metric values are never read and hashing is bounded |
| Tracker-directory file path references | 2576 | Materialized non-ignored input files plus managed output paths; self-referential output contents are excluded |
| Ollama tracker file paths / metric artifacts | 2573 / 37 | Input path/metadata inventory; input hashes are bounded to 1000000 bytes; metric values are not read |
| QMOI tracker file paths / metric artifacts | 3 / 0 | Input path/metadata inventory; input hashes are bounded to 1000000 bytes; metric values are not read |
| Verified per-requirement monitor mappings | 0 | Evidence-linked feature mappings only |
| Pending monitoring review actions | 595 | One durable review action per requirement; no runtime mutation authorized |
| Monitor-mapping rate | 0.0% | Verified mappings / all requirements; zero currently verified |
| Source hash coverage | 98.82% | Hashed candidates / discovered source candidates; local integrity only |
| Unhashed, unavailable, or changed sources | 31 | Check `unavailable_sources` for per-path reasons, including the 1 MB hashing bound |
| Live metric samples observed | 0 | No runtime endpoint was read |
| Verified live provider connections | 0 | No provider connection was made |

The machine inventory defines each calculation, numerator, denominator, unit, and interpretation. A percentage never means global, remote, semantic, or production coverage.

### Access, styles, and universals contract

- `public_guest`: public-only views; no user-specific or protected state.
- `authenticated_user`: only verified user-owned scope, enforced by server-side authorization.
- `master_operator`: all supported monitoring surfaces only after role verification, with least privilege, consent, and audit controls.
- Product-feature access classifications remain `review_required`; this report does not infer role access from feature names.
- Apply [STYLES.md](STYLES.md), [UNIVERSAL.md](UNIVERSAL.md), and [UNIVERSALS.md](UNIVERSALS.md) consistently during UI transitions without sharing private data across users.
- Master monitoring UI requirements are individually listed in the machine inventory; backend authorization and actual UI implementation remain unverified.

### Registered product features and monitoring assessment

| Feature ID | Platform | App | Access classification | Monitoring | Shared style/universal transition |
| --- | --- | --- | --- | --- | --- |
| `ui.android.qalpha.001.code-editing` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.002.syntax-highlighting` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.003.code-completion` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.004.debugger` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.005.terminal-integration` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.006.git-integration` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.007.file-explorer` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.008.theme-support` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.009.keyboard-shortcuts` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.010.extensions` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.011.realtime-sync` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.012.offline-mode` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.013.gradle-build-system` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qalpha.014.android-emulator` | `android` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.001.folder-tree-navigation` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.002.view-modes` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.003.search-functionality` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.004.batch-operations` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.005.duplicate-finder` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.006.smart-tags` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.007.auto-organization` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.008.cloud-storage-integration` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.009.github-repo-automation` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.010.gitpod-workspace-automation` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.011.vercel-deployment-automation` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.012.huggingface-space-automation` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.013.qvillage-sync-automation` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.014.voice-commands` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.015.gesture-controls` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.016.file-preview` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.017.realtime-sync` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.018.storage-access-framework` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qcity.019.foldable-support` | `android` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.001.playback-controls` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.002.volume-control` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.003.quality-selection` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.004.subtitle-switching` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.005.audio-track-switching` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.006.playlist-management` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.007.picture-in-picture` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.008.media-library` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.009.voice-control` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.010.gesture-control` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.011.keyboard-shortcuts` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.012.eye-tracking` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.013.mediaplayer-exoplayer` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoi-space.014.spatial-audio-android` | `android` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.001.conversation-creation` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.002.message-history` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.003.model-selector` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.004.parameter-tuning` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.005.export-functionality` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.006.voice-input` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.007.voice-output` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.008.memory-persistence` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.009.accessibility-features` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.010.platform-specific-styling` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.011.offline-mode` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.012.realtime-sync` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.013.content-provider` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.014.documents-provider` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.015.documentsrovider` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.android.qmoiaiui.016.material-you-theming` | `android` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.001.code-editing` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.002.syntax-highlighting` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.003.code-completion` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.004.debugger` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.005.terminal-integration` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.006.git-integration` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.007.file-explorer` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.008.theme-support` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.009.keyboard-shortcuts` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.010.extensions` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.011.realtime-sync` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.012.offline-mode` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.013.swift-playgrounds` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.014.xcode-previews` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.015.swift-compiler` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qalpha.016.swift-package-manager-ios` | `ios` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.001.folder-tree-navigation` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.002.view-modes` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.003.search-functionality` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.004.batch-operations` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.005.duplicate-finder` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.006.smart-tags` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.007.auto-organization` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.008.cloud-storage-integration` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.009.github-repo-automation` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.010.gitpod-workspace-automation` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.011.vercel-deployment-automation` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.012.huggingface-space-automation` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.013.qvillage-sync-automation` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.014.voice-commands` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.015.gesture-controls` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.016.file-preview` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.017.realtime-sync` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.018.files-app-integration` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.019.icloud-drive-ios` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.020.document-picker-ios` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qcity.021.fileprovider-extension-ios` | `ios` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.001.playback-controls` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.002.volume-control` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.003.quality-selection` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.004.subtitle-switching` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.005.audio-track-switching` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.006.playlist-management` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.007.picture-in-picture` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.008.media-library` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.009.voice-control` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.010.gesture-control` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.011.keyboard-shortcuts` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.012.eye-tracking` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.013.avplayer-framework` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.014.airplay-ios` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.015.avfoundation-ios` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoi-space.016.core-audio-ios` | `ios` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.001.conversation-creation` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.002.message-history` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.003.model-selector` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.004.parameter-tuning` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.005.export-functionality` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.006.voice-input` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.007.voice-output` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.008.memory-persistence` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.009.accessibility-features` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.010.platform-specific-styling` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.011.offline-mode` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.012.realtime-sync` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.013.fileprovider-integration` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.014.handoff-ios` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.015.siri-shortcuts` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.ios.qmoiaiui.016.swiftui-interface` | `ios` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.001.code-editing` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.002.syntax-highlighting` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.003.code-completion` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.004.debugger` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.005.terminal-integration` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.006.git-integration` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.007.file-explorer` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.008.theme-support` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.009.keyboard-shortcuts` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.010.extensions` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.011.realtime-sync` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.012.offline-mode` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.013.gcc-clang-toolchain` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qalpha.014.docker-integration` | `linux` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.001.folder-tree-navigation` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.002.view-modes` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.003.search-functionality` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.004.batch-operations` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.005.duplicate-finder` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.006.smart-tags` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.007.auto-organization` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.008.cloud-storage-integration` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.009.github-repo-automation` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.010.gitpod-workspace-automation` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.011.vercel-deployment-automation` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.012.huggingface-space-automation` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.013.qvillage-sync-automation` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.014.voice-commands` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.015.gesture-controls` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.016.file-preview` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.017.realtime-sync` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.018.nautilus-dolphin-integration` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qcity.019.freedesktop-mime-types` | `linux` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.001.playback-controls` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.002.volume-control` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.003.quality-selection` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.004.subtitle-switching` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.005.audio-track-switching` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.006.playlist-management` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.007.picture-in-picture` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.008.media-library` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.009.voice-control` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.010.gesture-control` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.011.keyboard-shortcuts` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.012.eye-tracking` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.013.pulseaudio-integration` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoi-space.014.pipewire-support` | `linux` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.001.conversation-creation` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.002.message-history` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.003.model-selector` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.004.parameter-tuning` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.005.export-functionality` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.006.voice-input` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.007.voice-output` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.008.memory-persistence` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.009.accessibility-features` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.010.platform-specific-styling` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.011.offline-mode` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.012.realtime-sync` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.013.dbus-integration` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.014.desktop-entry-file` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.015.appstream-metadata` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.linux.qmoiaiui.016.freedesktop-notifications` | `linux` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.001.code-editing` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.002.syntax-highlighting` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.003.code-completion` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.004.debugger` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.005.terminal-integration` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.006.git-integration` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.007.file-explorer` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.008.theme-support` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.009.keyboard-shortcuts` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.010.extensions` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.011.realtime-sync` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.012.offline-mode` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.013.xcode-integration` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qalpha.014.lldb-debugger` | `macos` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.001.folder-tree-navigation` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.002.view-modes` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.003.search-functionality` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.004.batch-operations` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.005.duplicate-finder` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.006.smart-tags` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.007.auto-organization` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.008.cloud-storage-integration` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.009.github-repo-automation` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.010.gitpod-workspace-automation` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.011.vercel-deployment-automation` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.012.huggingface-space-automation` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.013.qvillage-sync-automation` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.014.voice-commands` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.015.gesture-controls` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.016.file-preview` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.017.realtime-sync` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.018.finder-integration` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.019.quick-look-plugin` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qcity.020.airdrop-files` | `macos` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.001.playback-controls` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.002.volume-control` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.003.quality-selection` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.004.subtitle-switching` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.005.audio-track-switching` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.006.playlist-management` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.007.picture-in-picture` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.008.media-library` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.009.voice-control` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.010.gesture-control` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.011.keyboard-shortcuts` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.012.eye-tracking` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.013.avfoundation-framework` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoi-space.014.airplay-streaming` | `macos` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.001.conversation-creation` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.002.message-history` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.003.model-selector` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.004.parameter-tuning` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.005.export-functionality` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.006.voice-input` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.007.voice-output` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.008.memory-persistence` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.009.accessibility-features` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.010.platform-specific-styling` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.011.offline-mode` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.012.realtime-sync` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.013.notification-center` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.014.spotlight-search` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.015.handoff-continuity` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.016.icloud-sync` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.macos.qmoiaiui.017.metal-gpu-acceleration` | `macos` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.001.code-editing` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.002.syntax-highlighting` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.003.code-completion` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.004.debugger` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.005.terminal-integration` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.006.git-integration` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.007.file-explorer` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.008.theme-support` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.009.keyboard-shortcuts` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.010.extensions` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.011.realtime-sync` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.012.offline-mode` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.013.javascript-debugging` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qalpha.014.jest-testing` | `web` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.001.folder-tree-navigation` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.002.view-modes` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.003.search-functionality` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.004.batch-operations` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.005.duplicate-finder` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.006.smart-tags` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.007.auto-organization` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.008.cloud-storage-integration` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.009.github-repo-automation` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.010.gitpod-workspace-automation` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.011.vercel-deployment-automation` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.012.huggingface-space-automation` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.013.qvillage-sync-automation` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.014.voice-commands` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.015.gesture-controls` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.016.file-preview` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.017.realtime-sync` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.018.drag-drop-files` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qcity.019.file-input-api` | `web` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.001.playback-controls` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.002.volume-control` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.003.quality-selection` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.004.subtitle-switching` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.005.audio-track-switching` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.006.playlist-management` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.007.picture-in-picture` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.008.media-library` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.009.voice-control` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.010.gesture-control` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.011.keyboard-shortcuts` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.012.eye-tracking` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.013.html5-audio-video` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoi-space.014.mediasource-api` | `web` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.001.conversation-creation` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.002.message-history` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.003.model-selector` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.004.parameter-tuning` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.005.export-functionality` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.006.voice-input` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.007.voice-output` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.008.memory-persistence` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.009.accessibility-features` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.010.platform-specific-styling` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.011.offline-mode` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.012.realtime-sync` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.013.service-worker-web` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.web.qmoiaiui.014.indexeddb-persistence` | `web` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.001.code-editing` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.002.syntax-highlighting` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.003.code-completion` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.004.debugger` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.005.terminal-integration` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.006.git-integration` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.007.file-explorer` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.008.theme-support` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.009.keyboard-shortcuts` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.010.extensions` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.011.realtime-sync` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.012.offline-mode` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.013.powershell-integration` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.014.windows-api` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qalpha.015.msvc-toolchain` | `windows` | `qalpha` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.001.folder-tree-navigation` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.002.view-modes` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.003.search-functionality` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.004.batch-operations` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.005.duplicate-finder` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.006.smart-tags` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.007.auto-organization` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.008.cloud-storage-integration` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.009.github-repo-automation` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.010.gitpod-workspace-automation` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.011.vercel-deployment-automation` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.012.huggingface-space-automation` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.013.qvillage-sync-automation` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.014.voice-commands` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.015.gesture-controls` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.016.file-preview` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.017.realtime-sync` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.018.windows-shell-integration` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.019.ntfs-attributes` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.020.alternate-data-streams` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.021.file-metadata-windows` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.022.quick-access` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.023.file-preview-pane` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.024.compressed-folder-support` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.025.unc-paths` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.026.onedrive-integration` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.027.windows-search` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.028.file-ownership-permissions` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qcity.029.thumbnail-cache` | `windows` | `qcity` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.001.playback-controls` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.002.volume-control` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.003.quality-selection` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.004.subtitle-switching` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.005.audio-track-switching` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.006.playlist-management` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.007.picture-in-picture` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.008.media-library` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.009.voice-control` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.010.gesture-control` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.011.keyboard-shortcuts` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.012.eye-tracking` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.013.media-keys` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.014.taskbar-buttons` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoi-space.015.windows-codecs` | `windows` | `qmoi-space` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.001.conversation-creation` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.002.message-history` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.003.model-selector` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.004.parameter-tuning` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.005.export-functionality` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.006.voice-input` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.007.voice-output` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.008.memory-persistence` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.009.accessibility-features` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.010.platform-specific-styling` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.011.offline-mode` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.012.realtime-sync` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.013.windows-notifications-api` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.014.media-keys-integration` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.015.taskbar-integration` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.016.windows-hello-biometric` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.017.fluent-design-styling` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.018.cortana-integration` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.019.clipboard-history` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.020.virtual-desktop-support` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.021.registry-persistence` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.022.game-bar-integration` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.023.winget-auto-update` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |
| `ui.windows.qmoiaiui.024.file-explorer-context-menu` | `windows` | `qmoiaiui` | `review_required` | `unmapped` | `required_mapping_not_verified` |

### Planned and not-yet-verified feature requirements

| Feature ID | Source category | Access classification | Availability | Monitoring |
| --- | --- | --- | --- | --- |
| `planned.access_transitions.001.public-guest-public-catalog-public-documentation-public-previews-and-saf` | `access_transitions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.access_transitions.002.public-guest-no-user-specific-data-private-workspace-account-action-or-p` | `access_transitions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.access_transitions.003.authenticated-user-verified-identity-consent-session-state-personal-sett` | `access_transitions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.access_transitions.004.authenticated-user-account-wallet-purchase-upload-private-media-and-writ` | `access_transitions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.access_transitions.005.master-operator-explicit-master-role-mfa-or-equivalent-step-up-verificat` | `access_transitions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.access_transitions.006.master-operator-expose-every-supported-enabled-qmoi-feature-to-the-verif` | `access_transitions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.access_transitions.007.master-operator-administrative-mutations-require-backend-authorization-a` | `access_transitions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.authenticated_ui.001.user-profile-workspace-preferences-and-personalization` | `authenticated_ui` | `authenticated_user_contract` | `planned_or_unverified` | `unmapped` |
| `planned.authenticated_ui.002.wallet-billing-and-account-linked-financial-actions` | `authenticated_ui` | `authenticated_user_contract` | `planned_or_unverified` | `unmapped` |
| `planned.authenticated_ui.003.private-files-deployment-previews-and-protected-project-state` | `authenticated_ui` | `authenticated_user_contract` | `planned_or_unverified` | `unmapped` |
| `planned.authenticated_ui.004.role-managed-admin-panels-audit-logs-and-approval-flows` | `authenticated_ui` | `authenticated_user_contract` | `planned_or_unverified` | `unmapped` |
| `planned.authenticated_ui.005.per-user-media-library-private-history-or-account-bound-content` | `authenticated_ui` | `authenticated_user_contract` | `planned_or_unverified` | `unmapped` |
| `planned.brand_customization.001.qmoi-logo-variants-and-avatar-branding` | `brand_customization` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.brand_customization.002.app-specific-icon-sets-for-each-platform-and-app-surface` | `brand_customization` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.brand_customization.003.font-families-and-typography-scales-per-platform-and-user-mode` | `brand_customization` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.brand_customization.004.theme-tokens-for-light-dark-high-contrast-and-accessibility-modes` | `brand_customization` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.brand_customization.005.custom-ui-polish-for-qcity-qstore-qstream-quantum-and-every-cloned-platf` | `brand_customization` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.001.github-repository-and-branch-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.002.github-workflow-check-status` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.003.github-pr-release-security-summaries` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.004.github-permission-and-audit-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.005.github-qmoi-branded-repo-and-release-card-customization` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.006.gitlab-project-and-merge-request-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.007.gitlab-pipeline-runner-status` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.008.gitlab-registry-artifact-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.009.gitlab-permission-and-audit-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.010.gitlab-qmoi-clone-polish-for-project-headers-and-milestone-views` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.011.gitpod-workspace-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.012.gitpod-environment-and-startup-status` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.013.gitpod-workspace-launch-stop-controls` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.014.gitpod-secret-readiness-without-values` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.015.gitpod-custom-workspace-branding-and-startup-states` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.016.netlify-site-build-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.017.netlify-preview-and-production-deploys` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.018.netlify-forms-redirects-edge-function-status` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.019.netlify-domain-and-logs-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.020.netlify-custom-site-branding-icons-and-fonts` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.021.vercel-project-deployment-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.022.vercel-preview-promote-rollback-controls` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.023.vercel-domains-functions-edge-status` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.024.vercel-logs-analytics-usage-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.025.vercel-custom-deployment-ui-and-qmoi-badge-polish` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.026.quantum-hosting-project-deployment-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.027.quantum-compute-backend-and-queue-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.028.quantum-hybrid-job-controls` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.029.quantum-quota-cost-provenance-and-audit-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.030.quantum-qmoi-compute-ui-tokens-and-custom-job-branding` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.031.huggingface-model-space-dataset-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.032.huggingface-inference-and-runtime-status` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.033.huggingface-build-log-artifact-views` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.034.huggingface-permissions-and-access-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.035.huggingface-brand-safe-hf-surfaces-and-custom-qmoi-identity` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.036.qvillage-community-content-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.037.qvillage-device-and-sync-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.038.qvillage-moderation-notification-controls` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.039.qvillage-member-privacy-and-access-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.040.qvillage-custom-community-visual-language-and-shared-iconography` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.041.dagshub-repository-dataset-inventory` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.042.dagshub-experiment-and-ml-workflow-status` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.043.dagshub-artifact-metric-comparisons` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.044.dagshub-permission-and-provenance-state` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.clone_platform_ui.045.dagshub-custom-dataset-and-experiment-ui-branding` | `clone_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.001.project-and-environment-inventory-with-owner-repository-and-source-sha` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.002.build-configuration-dependency-cache-and-artifact-status` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.003.static-server-rendered-function-and-edge-runtime-capability-discovery` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.004.preview-staging-production-promote-rollback-and-cancel-workflows` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.005.domain-dns-tls-redirect-and-deployment-alias-management` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.006.logs-metrics-traces-health-checks-alerts-and-incident-history` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.007.environment-secret-references-with-masked-readiness-and-rotation-status` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.008.regions-traffic-controls-quotas-resource-usage-and-cost-visibility` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.009.storage-databases-queues-scheduled-jobs-and-integration-status` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.hosting.010.access-policy-approvals-audit-events-and-recovery-controls` | `hosting` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.001.page-identity` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.002.documented-feature-list` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.003.access-mode` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.004.state-handling` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.005.visual-branding-parity` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.006.source-implementation-or-contract-evidence` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.007.ui-affordance-presence` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.008.permission-boundary` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.009.error-loading-offline-state` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.010.final-validation-result` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.011.public` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.012.authenticated` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.013.mixed-access` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.014.missing` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.015.stale` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.016.blocked` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.017.validate-each-link-against-its-documented-ui-contract-before-marking-it-` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.018.compare-reported-ui-features-behavior-access-mode-and-state-handling-wit` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.019.flag-missing-stale-account-only-or-public-only-features-as-explicit-gaps` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.020.require-a-documented-source-or-implementation-proof-before-a-platform-li` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.link_validation.021.keep-public-authenticated-and-mixed-access-states-separate-in-validation` | `link_validation` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.mixed_access_ui.001.shared-public-preview-with-account-required-publish-or-save-flow` | `mixed_access_ui` | `mixed_access_contract` | `planned_or_unverified` | `unmapped` |
| `planned.mixed_access_ui.002.public-project-listing-with-authenticated-edit-controls` | `mixed_access_ui` | `mixed_access_contract` | `planned_or_unverified` | `unmapped` |
| `planned.mixed_access_ui.003.public-dashboard-cards-that-reveal-identity-bound-totals-only-after-sess` | `mixed_access_ui` | `mixed_access_contract` | `planned_or_unverified` | `unmapped` |
| `planned.mixed_access_ui.004.public-feed-with-private-comments-follows-or-saved-items-behind-auth` | `mixed_access_ui` | `mixed_access_contract` | `planned_or_unverified` | `unmapped` |
| `planned.public_ui.001.public-catalog-pages-and-documentation` | `public_ui` | `public_guest_contract` | `planned_or_unverified` | `unmapped` |
| `planned.public_ui.002.public-preview-pages-and-public-product-details` | `public_ui` | `public_guest_contract` | `planned_or_unverified` | `unmapped` |
| `planned.public_ui.003.public-search-browse-and-compare-flows` | `public_ui` | `public_guest_contract` | `planned_or_unverified` | `unmapped` |
| `planned.public_ui.004.public-landing-pages-pricing-summaries-and-release-notes` | `public_ui` | `public_guest_contract` | `planned_or_unverified` | `unmapped` |
| `planned.public_ui.005.public-status-and-health-pages-that-reveal-no-personal-data` | `public_ui` | `public_guest_contract` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.001.windows-windows-package-and-architecture-compatibility` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.002.windows-keyboard-navigation-and-native-install-update-handoff` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.003.macos-macos-package-and-architecture-compatibility` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.004.macos-signing-notarization-state-when-independently-verified` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.005.linux-linux-package-format-and-distribution-compatibility` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.006.linux-package-manager-handoff-and-dependency-status` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.007.ios-ios-device-compatibility-and-official-store-handoff` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.008.ios-voiceover-and-system-permission-disclosure` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.009.android-android-device-compatibility-and-official-store-handoff` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.010.android-talkback-and-runtime-permission-disclosure` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.011.web-responsive-web-catalog-and-installable-pwa-state` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.qstore_platform_ui.012.web-offline-catalog-state-and-browser-compatible-install-handoff` | `qstore_platform_ui` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.quantum_extensions.001.capability-discovery-for-simulator-hybrid-runtime-and-provider-backed-qp` | `quantum_extensions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.quantum_extensions.002.provider-adapters-with-explicit-availability-region-queue-and-maintenanc` | `quantum_extensions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.quantum_extensions.003.circuit-job-submission-validation-cancellation-retry-and-result-retrieva` | `quantum_extensions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.quantum_extensions.004.qubit-shots-compiler-backend-fidelity-and-execution-metadata-when-suppli` | `quantum_extensions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.quantum_extensions.005.hybrid-classical-quantum-workflow-orchestration-and-reproducible-job-man` | `quantum_extensions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.quantum_extensions.006.queue-time-runtime-quota-cost-estimate-and-spend-confirmation-before-exe` | `quantum_extensions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.quantum_extensions.007.result-provenance-artifact-integrity-simulator-versus-hardware-labeling-` | `quantum_extensions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.quantum_extensions.008.provider-outage-unsupported-operation-quota-and-job-failure-recovery-sta` | `quantum_extensions` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.style_coverage.001.shared-design-tokens-plus-app-specific-and-platform-specific-tokens` | `style_coverage` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.style_coverage.002.public-guest-authenticated-user-and-master-operator-access-states` | `style_coverage` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.style_coverage.003.loading-empty-offline-stale-blocked-degraded-success-and-error-states` | `style_coverage` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.style_coverage.004.responsive-navigation-keyboard-focus-screen-readers-contrast-and-text-sc` | `style_coverage` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.style_coverage.005.risk-security-validation-overlays-that-cannot-be-hidden-by-themes-or-per` | `style_coverage` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.style_coverage.006.consistent-hosting-deployment-quantum-job-and-cloned-platform-controls` | `style_coverage` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.001.qmoiaiui-public-guest-interaction` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.002.qmoiaiui-authenticated-profile-and-private-conversation-controls` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.003.qcity-public-file-management-information` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.004.qcity-authenticated-private-files-and-workspace-controls` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.005.qmoi-space-public-media-discovery` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.006.qmoi-space-authenticated-library-history-and-account-controls` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.007.qalpha-public-product-documentation-views` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.008.qalpha-authenticated-private-projects-and-collaboration` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.009.qstream-public-catalog-and-permitted-previews` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `planned.user_access_requirements.010.qstream-authenticated-profiles-library-creator-and-subscription-controls` | `user_access_requirements` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-00-r01` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-00-r02` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-00-r03` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-00-r04` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-01-r01` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r01` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r02` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r03` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r04` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r05` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r06` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r07` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r08` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r09` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-02-r10` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-03-r01` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-03-r02` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-04-r01` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-05-r01` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-06-r01` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r01` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r02` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r03` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r04` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r05` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r06` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r07` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r08` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r09` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r10` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r11` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r12` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r13` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r14` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r15` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r16` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r17` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r18` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r19` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r20` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |
| `uis.uis-07-r21` | `universal_intelligence` | `review_required` | `planned_or_unverified` | `unmapped` |

### Master monitoring and control requirements

| Feature ID | Requirement | Access | Monitoring status |
| --- | --- | --- | --- |
| `master.monitoring.001` | System overview with source timestamp, health, and stale/degraded indicators. | `master_operator_contract` | `unmapped` |
| `master.monitoring.002` | Repository, application, hosting, and deployment inventory with exact source SHAs. | `master_operator_contract` | `unmapped` |
| `master.monitoring.003` | User, role, session, consent, and access review with least-privilege controls. | `master_operator_contract` | `unmapped` |
| `master.monitoring.004` | Quantum compute/provider control with capability and billing gates. | `master_operator_contract` | `unmapped` |
| `master.monitoring.005` | Deployment preview, approval, promotion, rollback, and audit trail. | `master_operator_contract` | `unmapped` |
| `master.monitoring.006` | Domain, DNS, TLS, and ownership management with confirmation before changes. | `master_operator_contract` | `unmapped` |
| `master.monitoring.007` | Documentation, styles, app-catalog, and validation report management. | `master_operator_contract` | `unmapped` |
| `master.monitoring.008` | Master and sister account configuration for bank accounts, wallets, payment APIs, and project-linked financial destinations. | `master_operator_contract` | `unmapped` |
| `master.monitoring.009` | Revenue, wallet, and financial dashboards with read/write permissions separated. | `master_operator_contract` | `unmapped` |
| `master.monitoring.010` | Monitoring, notifications, incidents, recovery, and automation controls. | `master_operator_contract` | `unmapped` |
| `master.monitoring.011` | Security events, audit history, export, retention, and access-revocation controls. | `master_operator_contract` | `unmapped` |
| `master.monitoring.012` | Brand customization with QMOI logo, icon, font, motion, and identity tokens without hiding risk state. | `master_operator_contract` | `unmapped` |

### Ollama and QMOI runtime monitoring targets

- Track model/provider availability and inference failures, duration, timeouts, and bounded retries without logging prompts or credentials.
- Track agent cycle status, task queue depth/age, checkpoint freshness, source-manifest deltas, skipped/unreadable inputs, test outcomes, and recovery results.
- Track QMOI feature-service health and data freshness separately from discovery counts; missing or stale telemetry must report `UNKNOWN`, `STALE`, or `OFFLINE`, never healthy by default.
- Record source, observation time, units, thresholds, owner, and evidence hash for every runtime sample; keep personal data tenant-scoped and collect only approved aggregates.

### Bounded implementation plan

1. **inventory_and_contracts** — All current feature, monitoring, metric-artifact, and tracking candidates retain local scope and source hashes. Status: `implemented_candidate_inventory`.
2. **planned_and_unavailable_features** — Every planned, unavailable, or newly registered feature receives a stable monitoring-review row and durable action before any implementation is claimed. Status: `implemented_candidate_queue`.
3. **metric_schema_and_ownership** — Each approved signal has an owner, unit, source, scope, sampling/freshness rule, and data-minimization policy. Status: `planned`.
4. **per_feature_monitor_mapping** — Every feature has reviewed applicability, signals, thresholds, alerts/runbook, and positive/negative tests or a justified not-applicable result. Status: `planned`.
5. **style_universal_and_access_transitions** — Public, authenticated, and master surfaces share styles while data and actions remain role-scoped and server-authorized. Status: `planned`.
6. **ollama_and_qmoi_runtime** — Authorized runtime health, queue age, checkpoint freshness, failures, and model/provider availability have freshness-bound evidence and recovery tests. Status: `planned`.
7. **dashboard_and_alert_delivery** — Master controls expose all supported monitoring features; user views remain tenant-scoped; alerts are tested, auditable, and revocable. Status: `planned`.
8. **remote_validation** — Target-owned terminal exact-SHA checks and independently verified remote artifacts are recorded before completion claims. Status: `blocked_remote_evidence_required`.

### Current blockers and next action

- No live metric endpoint or runtime sample was read by this inventory.
- Per-feature monitoring signals and access assignments have not been independently mapped or verified.
- Static source timestamps are not evidence of metric freshness or service health.
- Materialized local paths do not establish ignored, historical-ref, peer-repository, or remote coverage.
- Next action: Review the machine-readable source and feature inventory, then map monitor applicability, owner, signal, freshness, access scope, thresholds, alerts, tests, and recovery before adding runtime instrumentation or dashboards.
- Do not automatically instrument a feature until ownership, applicability, authorized data scope, privacy/security impact, thresholds, test plan, rollback, and required human approval are explicit.
- No production UI, telemetry endpoint, external monitor, or remote workflow was added or activated by this inventory.
<!-- END QMOI MANAGED: alltracks-monitoring-inventory -->

<!-- BEGIN QMOI MANAGED: repository-surface-audit -->
## Agent-managed repository surface audit

- Status: `NEEDS_REVIEW`; materialized files: `11301`; directories: `1291`; Markdown: `2440`.
- API/endpoint candidates: `962`; route candidates: `737`; components: `1384`; automation/event candidates: `554`.
- Managed-document family candidates: `app_platform=2177, build_download_install=2131, disability_accessibility=288, orchestration=2082, qteam_accountability=2071, release_tag_publish=2110, tree_inventory=2022`.
- Project/autoproject registry documents discovered: `4`; coverage refreshes these docs and model-card headings, but discovery is not implementation or completion proof.
- Active-root Markdown refresh targets combine stable core names, `ALL*` names, and content/path family matches for app/platform, build/download/install, release/tag/publish, QTeam/accountability, orchestration, and repository-tree documentation. Historical/archive candidates are audited but never rewritten as active docs.
- `TREE.md` is the canonical full indexed path tree: directories, every indexed file path and scope/status, plus skipped/unavailable path reasons. It is local materialized scope only; ignored roots, inaccessible paths, Git-history trees, and remote refs remain explicit limitations.
- Markdown structural checks passed: `2230`; needs review: `202`; metric candidate lines: `53187`; percentage occurrences: `22274`.
- Markdown word count: `2485`; heuristic sentence count: `395`; sentence records indexed: `395`; sentence records beyond the bound: `0`.
- Sentence review candidates: `8` metric claims; `15` completion claims; `8` metric and `14` completion claims lack an inline reference marker. Reference markers are candidates, not proof.
- Word-integrity candidates: `4` adjacent-repeat candidates; sentence and normalized word-sequence hashes are stored without source prose. Grammar and semantic truth remain unverified.
- Formula/calculation candidate lines: `13561`; percentage aggregates are grouped per source file and explicitly unclassified, not model-comparison proof.
- Surface manifest and source hashes: `ollamatracks/repository_surface_audit.json`; the generated report is excluded from its own digest.
- Instruction candidates: `41058` lines in `3748` files; each requires semantic requirement-to-code/test/workflow mapping.
- Production-gap candidates: `340`; status `NEEDS_REVIEW`; automatic replacement authorized: `False`.
- Checks cover encoding, headings, fences, unresolved markers, local links, hashes, paths, and metric locations. They do not prove sentence semantics, feature truth, benchmark superiority, or production readiness.
- Local roots/refs are not proof of all remote repositories, PRs, or intermediate commit trees. Production candidates remain review items; no bulk replacement is authorized.
<!-- END QMOI MANAGED: repository-surface-audit -->
