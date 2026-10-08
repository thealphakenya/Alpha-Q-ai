# Q Master Exams

## Purpose

Q Master Exams is a dedicated, secure online examination platform modeled on Smowl-style assessment workflows, but designed strictly for exam use cases. It is not a general-purpose app, chatbot, trading environment, marketplace, or open-ended productivity platform.

This product exists to support institutionally managed testing, certification, compliance assessments, and supervised remote exam delivery in a controlled, lawful, and auditable environment.

## Scope and non-scope

### In scope

- Remote exam administration
- Candidate authentication and session enrollment
- Secure timed assessments
- Proctoring and monitoring where authorized by exam policy
- Audit logs and review workflows
- Admin dashboards for session creation and incident handling
- Candidate support tied to exam access and status

### Out of scope

- General-purpose conversational AI usage
- Trading or financial automation
- Wallet, coupon, revenue, or business-account operations
- Social media, marketplace, or open browsing features
- Any activity that is not directly related to an authorized exam session
- Any use intended to evade exam security, monitoring, or policy enforcement

## Exam-only rule

Q Master Exams must be used only in the context of exams and exam administration. It must not be employed for general productivity, commerce, unapproved research workflows, financial management, or unrelated automation.

The platform must enforce a strict exam-only access model:

- Only exam roles and exam-approved sessions may access the experience.
- Non-exam modules must be isolated or blocked.
- General-purpose capabilities must not be presented as features of the exam product.
- The product must actively reject off-scope use cases during design, integration, and operation.

## Security and integrity model

Q Master Exams should be designed with security-first testing controls similar to the standards commonly used by remote proctoring tools, with a focus on lawful, transparent, and institution-approved monitoring.

### Required controls

- Session identity and authorization checks
- Environment validation to reject unsupported or unsafe setups
- Integrity checks for monitoring and capture components
- Secure storage and retention of exam evidence
- Audit trails for candidate action review
- Explicit incident escalation paths for suspected policy violations
- Safe failure behavior when verification cannot be completed

### Evasion and anti-abuse policy

The platform must not include or encourage methods to evade monitoring, detection, or exam rules.

This includes:

- Virtual machine-based bypasses
- Remote desktop or capture-card circumvention
- Process injection or hook tampering
- Hidden secondary-device or sandbox evasion
- Unauthorized manipulation of detection telemetry or system integrity checks

If the environment cannot be validated, the exam should not proceed unless a designated exam administrator makes a documented policy decision.

## Architecture intent

Q Master Exams should be implemented as a dedicated product surface, separated from the general QMOI platform stack where practical.

### Core architectural layers

1. Access and identity layer
   - Candidate and admin authentication
   - Role management
   - Session authorization

2. Exam orchestration layer
   - Exam scheduling
   - Rules and restrictions
   - Timer and navigation controls
   - Candidate state transitions

3. Monitoring and integrity layer
   - Device checks
   - Browser or system environment validation
   - Recording and evidence capture
   - Incident detection and escalation

4. Review and reporting layer
   - Candidate status
   - Incident logs
   - Admin reporting
   - Appeal and evidence review workflows

5. Privacy and retention layer
   - Data access controls
   - Retention policy enforcement
   - Redaction and secure handling of evidence

## Governance and compliance principles

- Use only for authorized exam delivery, assessment, and institutional testing.
- Respect legal, ethical, and privacy requirements for student and candidate data.
- Keep monitoring transparent, limited to approved case requirements, and aligned with institutional policy.
- Maintain secure auditability for all exam sessions and review decisions.
- Keep this platform isolated from unrelated operational workflows and business automation.

## Operational rule for QMOI

QMOI may support Q Master Exams only as a secure exam platform implementation and may not use the platform for cross-domain tasks outside exam management. All documentation, code, and product decisions must clearly state that Q Master Exams is exam-only and not a general-purpose environment.

## Summary

Q Master Exams is a dedicated secure exam platform with Smowl-inspired assessment safeguards, but it exists solely for exam administration and controlled assessment scenarios. It must remain tightly bounded to that purpose, must reject off-scope usage, and must be documented and operated as an exam-only product in every repository record and implementation reference.

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
