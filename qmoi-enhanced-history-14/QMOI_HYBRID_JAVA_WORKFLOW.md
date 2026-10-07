# QMOI Hybrid Java/Android Build & Validation Workflow

This guide explains how to develop in your codespace while offloading all Java/Android build and validation tasks to QMOI/QCity servers, CI/CD, or Docker. This is a robust, production-ready approach when local Java is unavailable.

---

## 1. Develop Locally in Codespace

- Write and edit code as usual in your codespace (no local Java required).
- Commit and push changes to your remote repository (GitHub, GitLab, etc.).

## 2. Offload Java/Android Tasks Remotely

- Use one or more of the following:
  - **QMOI/QCity Server:**
    - Set up a server with Java, Android SDK, and build tools.
    - Use SSH, rsync, or cloud sync to transfer code/artifacts.
    - Trigger builds/validation via SSH or QMOI/QCity API.
  - **CI/CD Pipeline:**
    - Configure GitHub Actions, GitLab CI, or similar with Java/Android runners.
    - Automate builds, tests, and APK validation on every push or PR.
    - Download artifacts from CI after successful builds.
  - **Dockerized Build Environment:**
    - Use a Docker image with Java and Android tools (e.g., `openjdk:17`, custom Android images).
    - Run builds/validation inside the container, mounting your code as a volume.

## 3. Retrieve and Use Artifacts

- Download built APKs/JARs from the remote server, CI/CD, or Docker container.
- Deploy or distribute as needed.

## 4. Integrate with QMOI/QCity Automation

- Add scripts to automate code sync, build triggers, and artifact retrieval.
- Use QMOI/QCity APIs for remote build/validation orchestration.
- Monitor build/validation status in QMOI dashboards.

---

## Example: Remote Build Script (SSH)

```sh
# Sync code to remote QMOI build server
rsync -avz ./mobile/ user@qmoibuild.example.com:/srv/qmoi/mobile/

# Trigger build remotely
ssh user@qmoibuild.example.com 'cd /srv/qmoi/mobile/android && ./gradlew assembleRelease'

# Retrieve APK
scp user@qmoibuild.example.com:/srv/qmoi/mobile/android/app/build/outputs/apk/release/app-release.apk ./artifacts/
```

---

## Best Practices

- Always validate artifacts before release.
- Use secure channels (SSH, HTTPS) for all transfers.
- Automate as much as possible for reliability and auditability.
- Document your workflow in your project for team clarity.

---

_Last updated: 2025-11-23_

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
