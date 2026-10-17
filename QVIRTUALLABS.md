# QVirtualLabs

QVirtualLabs is a proposed, evidence-led engineering simulation and experiment-planning capability. This document defines a candidate roadmap; it does not claim a working simulator, live research service, physical laboratory connection, validated result, or production integration.

The singular [QVIRTUALLAB.md](./QVIRTUALLAB.md) is an index to this canonical plural document. The prior [QVIRTUALLABS.md snapshot](./qmoi-enhanced-history-14/QVIRTUALLABS.md) is historical reference material only. The requested authoritative `QENGINEER.md` source is not present in this checkout, so completeness against QMOI's engineering requirements cannot yet be established.

## Candidate engineering-domain inventory

The following 14 domains are starter candidates taken from the historical QVirtualLabs description. They are not a complete or verified QENGINEER feature list.

<!-- BEGIN QMOI MANAGED: qvirtual-lab-domain-inventory -->
1. **Computer-aided engineering** — engineering models and system-level design analysis.
2. **Finite-element analysis** — structural response, deformation, stress, and fatigue.
3. **Computational fluid dynamics** — flow, pressure, heat transfer, and turbulence.
4. **Electrical circuits** — circuit behavior, waveforms, power, and component limits.
5. **Electromagnetic fields** — fields, flux, induction, motors, and antenna behavior.
6. **Mechanical motion** — mechanisms, linkages, gears, and multibody dynamics.
7. **Chemical processes** — reaction, separation, heat exchange, and process behavior.
8. **Aerospace systems** — aerodynamic, stability, propulsion, and flight-model analysis.
9. **Automotive systems** — vehicle, powertrain, braking, suspension, and energy models.
10. **Robotics** — kinematics, sensors, navigation, and control models.
11. **Electronic boards** — PCB, signal-integrity, power-delivery, and EMI analysis.
12. **Power systems** — grids, faults, converters, storage, and renewable integration.
13. **System and control modeling** — control loops, algorithms, and coupled system models.
14. **Multiphysics** — coupled physical domains with explicit solver and interface assumptions.
<!-- END QMOI MANAGED: qvirtual-lab-domain-inventory -->

## Research, experiment, and evolution lifecycle

QMOI should use one auditable lifecycle rather than treating a model-generated answer as an experiment:

1. Discover a requirement or research claim from an allowlisted official source; retain its URL, retrieval time, source hash, license/availability, collector version, and freshness.
2. Map the claim to a stable feature requirement, owner, affected project, acceptance criteria, risk class, and baseline.
3. Prepare an isolated experiment with reviewed inputs, explicit units, solver/model versions, environment, resource limits, deterministic seeds where applicable, and a rollback path.
4. Validate inputs and model applicability; reject invalid units, unsupported assumptions, unsafe configurations, and unbounded resource requests.
5. Run the approved simulation or benchmark, recording configuration, output hashes, warnings, convergence, sensitivity, uncertainty, and failures.
6. Compare against an independent reference case and prior baseline. Keep candidate suggestions separate from measured results.
7. Require engineering review for safety-relevant or consequential claims and human authorization before physical actuation, external services, promotion, or release.
8. Correlate against traceable physical measurements when available, then record discrepancy, uncertainty, calibration, and model limitations.
9. Promote only through focused regression tests, security/privacy checks, accessibility review, staged rollout, and a tested rollback.
10. Feed reviewed results back into QVillage research and project/auto-project proposals without converting proposals into completed work.

Internal research can inventory local code and documents. External research must be bounded, read-only, source-attributed, license-aware, and treated as untrusted input. Ollama may propose hypotheses and analyze evidence, but it must not autonomously bypass review, modify protected sources, or claim successful inference when the Ollama runtime is unavailable.

### Official-tool research and recommended starting point

Official documentation was retrieved and content-hashed on the UTC date `2026-10-16`; exact retrieval time was not captured, so these observations are date-bound and expire for planning on `2026-10-30`. They establish advertised scope, not comparative performance, fitness certification, or QMOI compatibility.

| Domain | Tool candidate | Official documentation observation | Recommendation |
| --- | --- | --- | --- |
| Circuits | [ngspice](https://ngspice.sourceforge.io/) | Project identifies itself as an open-source SPICE circuit simulator. | First bounded adapter pilot candidate; first prove one deterministic reference circuit and output parser. |
| Structural FEA | [CalculiX](https://www.calculix.de/) | Project documents linear/nonlinear, static, dynamic, and thermal finite-element analyses; GPL terms apply. | Specialist adapter candidate after a verified pilot and license review. |
| CFD | [OpenFOAM](https://cfd.direct/openfoam/features/) | Official feature page describes a broad CFD set (including RAS/LES, multiphase, reacting flow, dynamic meshes, and parallel processing). | Specialist candidate; defer until resource-limited worker execution, mesh convergence, and reference cases exist. |
| Robotics | [Gazebo Sim](https://gazebosim.org/docs/latest/getstarted/) | Official guide documents 3D robotics simulation, SDF worlds, and server-only/headless operation. | Specialist candidate for robotics; keep simulation distinct from real robot control. |
| Chemical process | [DWSIM](https://dwsim.org/) | Official site describes the standard process-simulator release as free and open source and distinguishes separately offered editions. | Specialist candidate; verify edition, automation API, and license for the selected deployment. |
| CAD and geometry authoring | [FreeCAD](https://www.freecad.org/) | Official project presents FreeCAD as an open-source CAD design application. | Optional geometry-authoring adapter, not a physics solver. |
| Model orchestration | [Ollama API](https://docs.ollama.com/api/introduction) and [structured outputs](https://docs.ollama.com/capabilities/structured-outputs) | Local API runs at a local server; cloud API requires an API key. JSON-schema outputs can constrain and validate model responses; cloud structured outputs are currently unsupported. | Use local Ollama, when available, only to propose structured plans and analyze results; independently validate every response and never let it assert solver or physical execution. |

**Recommendation:** build one QVirtualLabs adapter contract and register narrow, domain-specific solvers behind isolated, bounded workers; do not choose a monolithic solver. Use ngspice as the first pilot candidate because circuits provide a bounded scope for validating job input, deterministic fixtures, output parsing, provenance, cancellation, and failure handling before adding heavier FEA/CFD or robotics workers. This is an engineering judgment from the retrieved scope descriptions, not a benchmark result. Confirm the choice against the missing QENGINEER requirements before implementation.

Suggested adapter boundary: versioned problem schema → validated units/inputs → solver identity/version and resource policy → isolated job → raw output plus parsed result schema → hashes, logs, warnings, uncertainty, and reference-case comparison. Ollama may help draft the schema or explain anomalies, but it cannot authorize solver execution, certify correctness, or upgrade evidence status. Hardware actuation, cloud Ollama, and paid/commercial solvers stay disabled unless their separate owner, security, privacy, cost, and authorization gates pass.

The public lookup of `thealphakenya/qmoi-enhanced` at `main/QENGINEER.md` returned HTTP 404, while `gh` could not authenticate. This is `UNKNOWN_NOT_FOUND_OR_PRIVATE`, not proof the source does not exist. The local `QENGINEER.md` requirement count remains unknown.

## Simulation versus physical research

A simulation is not a physical experiment. QMOI must label results as `SIMULATED`, `MEASURED`, `INFERRED`, or `UNKNOWN`, and must never present simulated results as though hardware was operated. A model can approach physical observations only for a stated domain and operating envelope after validation against suitable evidence; no general “physically accurate” guarantee is justified.

Physical correlation requires, at minimum, an approved protocol and risk review, responsible human operator, device and instrument identifiers, instrument calibration records, UTC timestamps, controlled test conditions, units, raw-data integrity hashes, chain-of-custody, expected uncertainty, and independent review. Hardware control remains disabled unless the specific equipment, authority, interlocks, emergency stop, and safety procedure are verified. The agent may organize and analyze authorized data; it cannot claim to have physically tested anything without those records.

For every modeled result, expose assumptions, input provenance, solver version, convergence status, reference dataset, uncertainty interval, sensitivity, validation date, known limitations, and the decision threshold. If calibration or validation data is missing, report `UNVALIDATED`/`UNKNOWN`, not an accuracy score.

## UI, transitions, and project integration

The eventual shared interface should use the existing QMOI design-system tokens and universal components rather than inventing a separate visual system. It must support responsive layouts, keyboard and assistive-technology use, readable units, reduced motion, accessible charts, and explicit permission states.

Required workflow states include `DRAFT`, `NEEDS_REVIEW`, `READY`, `QUEUED`, `RUNNING`, `CANCELLED`, `FAILED`, `STALE`, `RESULTS_AVAILABLE`, `PHYSICAL_REVIEW_REQUIRED`, and `BLOCKED`. Every state transition needs a reason, actor, timestamp, and evidence reference; cancellation, timeout, partial output, retry, and recovery must be visible.

Project and auto-project cards and the preview window may show a read-only design, experiment plan, and labeled result summary. They must not expose restricted invention details, start physical work, or grant capabilities based on UI state alone. QVillage can curate reviewed research and evolution proposals; it must preserve source provenance and distinguish proposals from accepted changes.

## QAUDITS metrics and acceptance gates

The following values describe the starter plan only. `0` means no verifiable mapping or execution evidence is recorded in this plan; it does not prove that no related code exists elsewhere. Counts are local and must remain separate from historical, remote, and physical-lab evidence.

| Metric | Current evidence status |
| --- | --- |
| Starter engineering-domain candidates | 14, sourced from the historical description |
| Cross-cutting acceptance-gate candidates | 19, defined by the local planner |
| Authoritative QENGINEER requirements | Unknown; `QENGINEER.md` is missing |
| Requirements mapped to implementation / focused tests | 0 / 0 verified mappings |
| Simulation runs / benchmark validations | 0 / 0 recorded by this plan |
| Solver convergence / uncertainty reports / accuracy claims verified | 0 / 0 / 0 |
| Safety protocols reviewed | 0 |
| Physical experiment records / calibration correlations | 0 / 0 verified |
| Official simulator/Ollama documentation observations / verified evolution cycles | 8 observed by UTC date within freshness window / 0 verified |
| Official source retrieval time | Exact times not captured; UTC retrieval date recorded as `2026-10-16` |
| UI/accessibility and project/preview integrations | 0 / 0 verified |
| Remote verification | `False` |

`scripts/ollama_autonomous_agent.py` refreshes the machine-readable plan at `ollamatracks/qvirtual_labs_plan.json` and the managed metrics sections in the related QVillage, QAUDITS, and transition documents. The plan records its source manifest and SHA-256; it does not run a solver, fetch research, invoke a physical device, or substitute for tests and human engineering review.

### Next acceptance sequence

1. Restore or identify the canonical QENGINEER requirements and reconcile every requirement without dropping overlaps.
2. Map each requirement to an owner, implementation/source path, focused test, UI/platform surface, research evidence, and authorization/safety boundary.
3. Add isolated deterministic simulator adapters only for explicitly supported domains, with reference fixtures and numerical regression tests.
4. Add output provenance, uncertainty, calibration, and physical-correlation evidence before publishing accuracy claims.
5. Integrate read-only previews and reviewed project/QVillage flows with existing universal UI and access controls.
6. Validate the exact local tree and focused tests; keep hosted workflow and remote exact-SHA gates separate.

Until those gates pass, QVirtualLabs remains a planned capability with incomplete source reconciliation, not an implemented or physically validated laboratory.

<!-- BEGIN QMOI MANAGED: qaudit-qvirtual-labs-coverage -->
## Agent-managed QVirtualLabs engineering coverage

Generated from the local QVirtualLabs source inventory; a full QAUDITS universe manifest is included only when supplied by that inventory refresh. These are candidate-plan metrics, not implementation, experiment, physical-lab, or remote-completion evidence.
- Status: `BLOCKED_SOURCE_RECONCILIATION`; correlation ID: `231b915c-d2b9-45e5-baaa-1a02ef7b2209`; source manifest SHA-256: `ac35b2d4e2cc91f1395e1dd85f01183b6adbc2cb40411ef2194f6ab0e69a20ba`.
- QAUDITS universe manifest SHA-256: `unavailable`; QVirtualLabs source-manifest scope: `qvirtual_labs_source_files`.
- Plan artifact: `ollamatracks/qvirtual_labs_plan.json`; plan SHA-256: `b01b3fe497df8a44e3bd5965ac9f34336042d092199d3fe16ce0537118122773`; scope: `materialized_local_only`.
- Starter engineering-domain candidates: `14`; cross-cutting gate candidates: `19`; total starter-plan requirements: `33`.
- Authoritative QENGINEER requirements: `UNKNOWN`; QENGINEER source status: `missing_or_unsafe`.
- Requirement-to-implementation / focused-test mappings: `0` / `0`.
- Verified simulations / benchmark validations: `0` / `0`; physical experiment records / calibration correlations: `0` / `0`.
- Convergence cases / uncertainty reports / accuracy claims verified: `0` / `0` / `0`; safety protocols reviewed: `0`.
- Official research sources checked / date-fresh observations / stale observations: `8` / `8` / `0`; exact retrieval times not captured: `8`; verified evolution cycles: `0`.
- Recommended architecture: `one bounded, auditable adapter contract with specialist solvers; no monolithic all-domain solver selected`; first pilot candidate: `ngspice circuit reference case`; Ollama inference: `NOT_MEASURED` by this inventory.
- Tool recommendation rationale: `domain fit from official documentation, implementation isolation, and a bounded first regression; not a comparative performance benchmark`; selected tool: `NONE`; tool candidates: `6`.
- Public QENGINEER probe: `UNKNOWN_NOT_FOUND_OR_PRIVATE`; a public 404 is ambiguous without authenticated repository read access.
- UI/accessibility mappings / project, auto-project, and preview integrations: `0` / `0`; remote verified: `False`.
- Simulation output is never counted as physical evidence. Physical correlation requires an authorized protocol, human operator, traceable instruments/calibration, and reviewed raw-data provenance.
- Historical reference: `qmoi-enhanced-history-14/QVIRTUALLABS.md`; scope `historical_snapshot_candidate`; not authoritative.
- The planner does not run a solver, retrieve external research, invoke hardware, or infer that an unlinked implementation is absent.
<!-- END QMOI MANAGED: qaudit-qvirtual-labs-coverage -->
