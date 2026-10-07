# QMOI Java Integration and Production Readiness

## Overview

This document describes how Java and JVM-based technologies are integrated into the QMOI ecosystem, including build tools, server/cloud support, and validation systems. It also provides best practices for Java environment setup and usage across QMOI, QCity, and all related platforms.

---

## Java Environment Setup

- QMOI requires Java (JDK 11 or 17+) for Android builds, JVM-based microservices, and cross-platform automation.
- All QMOI servers, clouds, and CI/CD runners should have Java installed and `JAVA_HOME` set.
- Use OpenJDK for compatibility and security.

### Installation (Linux/Alpine example)

```sh
# As root or with sudo:
apk add openjdk-17-jdk
export JAVA_HOME="/usr/lib/jvm/java-17-openjdk"
export PATH="$JAVA_HOME/bin:$PATH"
```

---

## QMOI Java Build Tools

- QMOI includes Gradle and Maven wrappers for Java builds.
- Android builds use Gradle and React Native integration.
- Java validation scripts are provided for APK, JAR, and WAR verification.
- QMOI CI/CD pipelines auto-detect and use Java for Android and JVM builds.

---

## Java in QCity and QMOI Servers/Clouds

- QCity supports Java-based microservices and can deploy JVM apps as containers or native services.
- QMOI cloud can run Java apps, validate JVM builds, and orchestrate Java-based workflows.
- Java-based health checks and validation are integrated into QMOI's automation and monitoring.

---

## Java Validation System

- QMOI validation system uses Java tools to:
  - Verify APK/JAR/WAR signatures and manifest integrity
  - Check Android APK installability on real/virtual devices
  - Run JVM-based unit and integration tests
  - Report results in `qmoi_validation_report.json`
- Java validation hooks are available for QCity, QMOI cloud, and local dev.

---

## Best Practices

- Always use LTS Java versions (11 or 17+)
- Set `JAVA_HOME` and update `PATH` for all build agents and servers
- Use QMOI's Gradle/Maven wrappers for reproducible builds
- Validate all Java artifacts before release
- Monitor Java app health with QMOI's built-in checks

---

## References

- [QMOI System README](../README.md)
- [QMOI Mobile App](../mobile/README.md)
- [QCity Documentation](../qcity/README.md)
- [ALL_APPS Registry](../ALL_APPS/README.md)
- [QMOI Validation Report](../docs/qmoi_validation_report.json)

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
