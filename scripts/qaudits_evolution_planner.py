"""Build a deterministic, local-only QAUDITS evolution plan."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTRACTS = (
    ("autodev", ("AUTODEV.md",)),
    ("model_evolution", ("MODELEVOLUTIONO.md", "MODELEVUTIONO.md")),
    ("qvillage_evolution", ("Qvillageevolutions.md",)),
    ("qvirtual_labs", ("QVIRTUALLABS.md", "QENGINEER.md", "Qvillageevolutions.md")),
    ("internal_research", ("INTERNALRESEARCH.md",)),
    ("external_research", ("EXTERNALRESEARCH.md", "EXTERIORRESEARCH.md")),
    ("q_seed", ("QSEED.md",)),
    ("q_version", ("QVERSIONMANAGER.md",)),
    ("instruction_inventory", ("AGENTS.md", ".github/copilot-instructions.md")),
    ("repository_surface_audit", ("scripts/qaudit_universe.py", "scripts/ollama_research.py")),
    (
        "markdown_refresh",
        (
            "ALLMDFILESREFS.md",
            "TRANSION.md",
            "TRANSIONQ.md",
            "TRANSITION.md",
            "QVIRTUALLAB.md",
            "QVIRTUALLABS.md",
        ),
    ),
    ("production_gate", ("production.md", "productionenhanced.md")),
    ("validation", ("ALLVALIDATIONS.md",)),
    ("remote_verification", ("remotecompletion.md", "remote-completion.json")),
    ("evolutiono_pre_retirement", ("MODELEVOLUTIONO.md", "scripts/q_version_manager.py", "AUTODEV.md")),
    ("qmoi_capability_parity", ("AUTODEV.md", "ALLFEATURES.md", "ALLTESTSAUTOTESTS.md")),
    ("qreplaceo_archive", ("SYNC.md", "MODELEVOLUTIONO.md")),
    ("evolutiono_clean_branch_audit", ("SYNC.md", "scripts/qaudit_universe.py", "scripts/qaudits_evolution_planner.py")),
    ("evolutiono_ofca_metrics", ("MODELEVOLUTIONO.md", "scripts/qaudits_evolution_planner.py", "scripts/q_version_manager.py")),
)

EVOLUTIONO_TRANSITION_DOMAINS = (
    "evolutiono_pre_retirement",
    "qmoi_capability_parity",
    "qreplaceo_archive",
    "evolutiono_clean_branch_audit",
    "evolutiono_ofca_metrics",
)
PLAN_TARGETS = {
    "repository_surface_audit": ("QAUDITS.md", "OFCA.md"),
    "qvirtual_labs": (
        "QVIRTUALLAB.md",
        "QVIRTUALLABS.md",
        "QAUDITS.md",
        "TRANSION.md",
        "TRANSIONQ.md",
        "TRANSITION.md",
        "QVILLAGE.md",
        "Qvillageevolutions.md",
    ),
    "evolutiono_ofca_metrics": ("OFCA.md",),
}

QVIRTUAL_LAB_DOMAIN_MARKERS = (
    "<!-- BEGIN QMOI MANAGED: qvirtual-lab-domain-inventory -->",
    "<!-- END QMOI MANAGED: qvirtual-lab-domain-inventory -->",
)
QVIRTUAL_LAB_METRIC_MARKERS = (
    "<!-- BEGIN QMOI MANAGED: qaudit-qvirtual-labs-coverage -->",
    "<!-- END QMOI MANAGED: qaudit-qvirtual-labs-coverage -->",
)
QVIRTUAL_LAB_METRIC_DOCUMENTS = frozenset({
    "QVIRTUALLAB.md",
    "QVIRTUALLABS.md",
    "QAUDITS.md",
    "TRANSION.md",
    "TRANSIONQ.md",
    "TRANSITION.md",
    "QVILLAGE.md",
    "Qvillageevolutions.md",
})

QVIRTUAL_LAB_CROSSCUTTING_REQUIREMENTS = (
    ("ownership_traceability", "Requirement, owner, implementation, test, and source lineage"),
    ("access_and_privacy", "Role boundaries, consent, privacy, and protected invention access"),
    ("input_validation", "Geometry, materials, boundary conditions, units, and dimensional validation"),
    ("solver_selection", "Solver and model selection with documented applicability limits"),
    ("convergence", "Numerical stability, mesh or resolution convergence, and repeatability"),
    ("provenance", "Versioned inputs, solver/model versions, seeds, environment, and result hashes"),
    ("uncertainty", "Sensitivity analysis, uncertainty bounds, and assumptions"),
    ("reference_benchmarks", "Independent reference cases and regression baselines"),
    ("physical_calibration", "Calibration and correlation to traceable physical measurements"),
    ("physical_safety", "Human-reviewed risk assessment and approved physical test protocol"),
    ("instrument_provenance", "Instrument identity, calibration status, operator, time, and raw-data hash"),
    ("result_classification", "Unambiguous simulated, measured, inferred, and unknown result labels"),
    ("execution_isolation", "Sandboxing, resource limits, bounded jobs, and network restrictions"),
    ("failure_recovery", "Cancellation, timeout, retry, partial-result, and recovery behavior"),
    ("interaction_transitions", "Accessible progress, empty, running, success, failure, stale, and cancelled states"),
    ("universal_ui", "Shared design tokens, responsive layouts, keyboard access, and assistive technology"),
    ("project_preview_integration", "Project, auto-project, and preview-window integrations with permission checks"),
    ("qvillage_research", "Source-backed QVillage discovery, review, experiments, and evolution history"),
    ("gated_promotion", "Independent regression review, rollback plan, and authorized promotion"),
)

QVIRTUAL_LAB_RESEARCH_CAPTURED_DATE_UTC = "2026-10-16"
QVIRTUAL_LAB_RESEARCH_FRESH_UNTIL = "2026-10-30"
QVIRTUAL_LAB_RESEARCH_COLLECTOR = "manual-official-document-review/1"
QVIRTUAL_LAB_RESEARCH_SOURCES = (
    {
        "source_url": "https://www.calculix.de/",
        "subject": "CalculiX finite-element analysis",
        "observed_fact": "Official project describes linear/nonlinear static, dynamic, and thermal finite-element analyses.",
        "http_status": 200,
        "retrieved_bytes": 9839,
        "source_sha256": "771c31efba047f9a70685d9232398c3c39390cac3bcea681747395b8f072d6dd",
    },
    {
        "source_url": "https://ngspice.sourceforge.io/",
        "subject": "ngspice circuit simulation",
        "observed_fact": "Official project identifies ngspice as an open-source SPICE circuit simulator.",
        "http_status": 200,
        "retrieved_bytes": 7948,
        "source_sha256": "ec33b25455c0267bebf487f13be7ff64b8aa1aae2923d3f8a7942b360013d3a5",
    },
    {
        "source_url": "https://cfd.direct/openfoam/features/",
        "subject": "OpenFOAM computational fluid dynamics",
        "observed_fact": "Official feature page lists CFD models including RAS, LES, multiphase, reacting flow, dynamic meshes, and parallel processing.",
        "http_status": 200,
        "retrieved_bytes": 98952,
        "source_sha256": "8c7f75b9e56e333d666d87eac7ed51963b1c1fd05ae1b80f6441046a2b742461",
    },
    {
        "source_url": "https://gazebosim.org/docs/latest/getstarted/",
        "subject": "Gazebo robotics simulation",
        "observed_fact": "Official guide documents Gazebo Sim as a 3D robotics simulator with server-only headless mode, SDF worlds, and separate user/developer workflows.",
        "http_status": 200,
        "retrieved_bytes": 41843,
        "source_sha256": "7f21d9fa5aaacd2b849351a93a647f6e712b07b452a4c4a1b74cd88c5e268cad",
    },
    {
        "source_url": "https://dwsim.org/",
        "subject": "DWSIM chemical process simulation",
        "observed_fact": "Official project describes the standard process-simulator release as free and open source; separately offered editions may have different capabilities.",
        "http_status": 200,
        "retrieved_bytes": 245468,
        "source_sha256": "c33f1edcd3f0191978e958a9642f4210182455a5a06c215e141d6c0a1c6c8fe0",
    },
    {
        "source_url": "https://www.freecad.org/",
        "subject": "FreeCAD geometry authoring",
        "observed_fact": "Official project presents FreeCAD as an open-source CAD design application; CAD authoring does not itself validate a physics solver.",
        "http_status": 200,
        "retrieved_bytes": 45200,
        "source_sha256": "3825726c8e40c316f9680edbd85e8ab435e728e65b8c87bcdeff34c345561346",
    },
    {
        "source_url": "https://docs.ollama.com/api/introduction",
        "subject": "Ollama runtime/API boundary",
        "observed_fact": "Official API documentation distinguishes local-server inference from cloud API requests that require an API key.",
        "http_status": 200,
        "retrieved_bytes": 270032,
        "source_sha256": "4cdff4e784bf13edeeeccdcf5a04d811311ea9d35800d421f8c028737c5f6428",
    },
    {
        "source_url": "https://docs.ollama.com/capabilities/structured-outputs",
        "subject": "Ollama structured outputs",
        "observed_fact": "Official docs describe schema-constrained JSON responses and validating them against an application schema; cloud structured outputs are currently unsupported.",
        "http_status": 200,
        "retrieved_bytes": 366050,
        "source_sha256": "5c8d318dba75d40cf7d1ee0bc8c1a6a13413b2418feab1822ec46c131158b3b3",
    },
)
QVIRTUAL_LAB_TOOL_RECOMMENDATIONS = (
    {
        "domain": "electrical circuits",
        "tool": "ngspice",
        "fit": "Dedicated SPICE circuit simulation; best first bounded adapter pilot, subject to a local reference-case test.",
        "decision": "PILOT_CANDIDATE",
    },
    {
        "domain": "finite-element analysis",
        "tool": "CalculiX",
        "fit": "Dedicated structural FEA with documented static, dynamic, thermal, and nonlinear capabilities.",
        "decision": "DOMAIN_ADAPTER_CANDIDATE",
    },
    {
        "domain": "computational fluid dynamics",
        "tool": "OpenFOAM",
        "fit": "Broad CFD capability; defer until isolated resource-bounded worker and solver validation exist.",
        "decision": "DOMAIN_ADAPTER_CANDIDATE",
    },
    {
        "domain": "robotics",
        "tool": "Gazebo Sim",
        "fit": "3D robotics simulation with headless server operation and SDF-described worlds.",
        "decision": "DOMAIN_ADAPTER_CANDIDATE",
    },
    {
        "domain": "chemical processes",
        "tool": "DWSIM",
        "fit": "Open-source process-simulation option; verify the exact edition, automation interface, and license before integration.",
        "decision": "DOMAIN_ADAPTER_CANDIDATE",
    },
    {
        "domain": "CAD and geometry authoring",
        "tool": "FreeCAD",
        "fit": "Open-source CAD/design surface; treat as geometry authoring, not as a universal physics solver.",
        "decision": "OPTIONAL_GEOMETRY_ADAPTER_CANDIDATE",
    },
)


def _candidate_virtual_lab_domains(root: Path) -> list[dict[str, str]]:
    source = root / "QVIRTUALLABS.md"
    if not source.is_file() or source.is_symlink():
        return []
    try:
        content = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    start_marker, end_marker = QVIRTUAL_LAB_DOMAIN_MARKERS
    start = content.find(start_marker)
    end = content.find(end_marker)
    if start < 0 or end <= start:
        return []

    domains: list[dict[str, str]] = []
    for line in content[start + len(start_marker):end].splitlines():
        match = re.match(r"^\s*\d+\.\s+\*\*(.+?)\*\*", line)
        if match:
            name = match.group(1).strip()
            domains.append({
                "id": f"QVLAB-DOM-{len(domains) + 1:02d}",
                "name": name,
                "status": "candidate_unmapped",
            })
    return domains


def build_qvirtual_labs_plan(
    root: Path | str,
    *,
    source_manifest_sha256: str | None = None,
) -> dict[str, Any]:
    """Build local-only QVirtualLabs coverage metrics without claiming execution."""
    source_root = Path(root).resolve()
    active_sources = [
        _file_evidence(source_root, "QVIRTUALLABS.md"),
        _file_evidence(source_root, "QENGINEER.md"),
    ]
    historical_source = _file_evidence(
        source_root,
        "qmoi-enhanced-history-14/QVIRTUALLABS.md",
    )
    research_is_fresh = (
        datetime.now(timezone.utc).date().isoformat()
        <= QVIRTUAL_LAB_RESEARCH_FRESH_UNTIL
    )
    research_observations = [
        {
            **source,
            "retrieved_date_utc": QVIRTUAL_LAB_RESEARCH_CAPTURED_DATE_UTC,
            "retrieved_at_utc": None,
            "retrieval_time_status": "NOT_CAPTURED",
            "freshness_deadline": QVIRTUAL_LAB_RESEARCH_FRESH_UNTIL,
            "collector_version": QVIRTUAL_LAB_RESEARCH_COLLECTOR,
            "result_status": "OBSERVED_DATE_ONLY" if research_is_fresh else "STALE",
        }
        for source in QVIRTUAL_LAB_RESEARCH_SOURCES
    ]
    domains = _candidate_virtual_lab_domains(source_root)
    requirements = [
        {
            "id": domain["id"],
            "name": domain["name"],
            "category": "engineering_domain_candidate",
            "status": domain["status"],
            "implementation_evidence": "NOT_MAPPED",
            "test_evidence": "NOT_MAPPED",
            "simulation_evidence": "NOT_RUN",
            "physical_evidence": "NOT_VERIFIED",
        }
        for domain in domains
    ]
    requirements.extend(
        {
            "id": f"QVLAB-CORE-{index:02d}",
            "name": name,
            "category": "cross_cutting_gate",
            "status": "candidate_unmapped",
            "implementation_evidence": "NOT_MAPPED",
            "test_evidence": "NOT_MAPPED",
            "simulation_evidence": "NOT_RUN",
            "physical_evidence": "NOT_VERIFIED",
        }
        for index, (_, name) in enumerate(QVIRTUAL_LAB_CROSSCUTTING_REQUIREMENTS, start=1)
    )
    missing_authoritative = [
        item["path"]
        for item in active_sources
        if item["path"] == "QENGINEER.md" and item["status"] != "observed_local"
    ]
    manifest_subjects = {
        "active_source_files": active_sources,
        "historical_reference": historical_source,
    }
    scoped_manifest_sha256 = hashlib.sha256(
        json.dumps(manifest_subjects, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    blockers = []
    if missing_authoritative:
        blockers.append("Authoritative QENGINEER.md feature source is missing or unreadable.")
    if not domains:
        blockers.append("Canonical QVIRTUALLABS.md domain inventory is missing or malformed.")
    blockers.extend([
        "No requirement-to-implementation, owner, or focused-test mappings are recorded by this plan.",
        "No simulation, benchmark, calibration, or physical experiment was run by this plan.",
        "Ollama inference, QVillage external research, and UI/project integration are not measured by this plan.",
        "Remote verification is unavailable to this local planner.",
    ])
    metrics = {
        "source_manifest_sha256": source_manifest_sha256 or scoped_manifest_sha256,
        "source_manifest_scope": (
            "qaudit_universe" if source_manifest_sha256 else "qvirtual_labs_source_files"
        ),
        "source_requirement_count": None,
        "starter_domain_candidate_count": len(domains),
        "cross_cutting_gate_candidate_count": len(QVIRTUAL_LAB_CROSSCUTTING_REQUIREMENTS),
        "starter_plan_requirement_count": len(requirements),
        "requirements_mapped_to_implementation_count": 0,
        "requirements_mapped_to_tests_count": 0,
        "simulation_runs_verified_count": 0,
        "benchmark_validations_verified_count": 0,
        "solver_convergence_cases_verified_count": 0,
        "uncertainty_reports_verified_count": 0,
        "accuracy_claims_verified_count": 0,
        "safety_protocols_reviewed_count": 0,
        "physical_experiment_records_verified_count": 0,
        "physical_calibration_correlations_verified_count": 0,
        "fresh_external_research_observations_count": (
            len(research_observations) if research_is_fresh else 0
        ),
        "stale_external_research_observations_count": (
            0 if research_is_fresh else len(research_observations)
        ),
        "official_research_source_count": len(research_observations),
        "official_research_retrieval_time_not_captured_count": len(research_observations),
        "autonomous_evolution_cycles_verified_count": 0,
        "ui_accessibility_mappings_verified_count": 0,
        "project_autoproject_preview_integrations_verified_count": 0,
        "remote_verified": False,
        "interpretation": "plan_and_candidate_inventory_only_not_implementation_or_execution_evidence",
    }
    plan: dict[str, Any] = {
        "schema_version": 1,
        "status": (
            "BLOCKED_SOURCE_RECONCILIATION"
            if missing_authoritative or not domains
            else "NEEDS_REVIEW"
        ),
        "source_scope": "materialized_local_only",
        "active_source_files": active_sources,
        "research": {
            "status": "OBSERVED_DATE_ONLY" if research_is_fresh else "STALE",
            "retrieved_date_utc": QVIRTUAL_LAB_RESEARCH_CAPTURED_DATE_UTC,
            "retrieved_at_utc": None,
            "retrieval_time_status": "NOT_CAPTURED",
            "freshness_deadline": QVIRTUAL_LAB_RESEARCH_FRESH_UNTIL,
            "collector_version": QVIRTUAL_LAB_RESEARCH_COLLECTOR,
            "observations": research_observations,
            "interpretation": "official capability documentation review_not_independent_benchmark_or_performance_validation",
        },
        "recommended_adapter_stack": {
            "architecture": "one bounded, auditable adapter contract with specialist solvers; no monolithic all-domain solver selected",
            "initial_pilot": "ngspice circuit reference case",
            "tool_candidates": list(QVIRTUAL_LAB_TOOL_RECOMMENDATIONS),
            "decision_basis": "domain fit from official documentation, implementation isolation, and a bounded first regression; not a comparative performance benchmark",
            "requirements_dependent": True,
        },
        "historical_reference": {
            **historical_source,
            "scope": "historical_snapshot_candidate",
            "not_authoritative": True,
        },
        "domains": domains,
        "requirements": requirements,
        "metrics": metrics,
        "blockers": blockers,
        "public_qengineer_probe": {
            "source_url": "https://raw.githubusercontent.com/thealphakenya/qmoi-enhanced/main/QENGINEER.md",
            "observed_http_status": 404,
            "status": "UNKNOWN_NOT_FOUND_OR_PRIVATE",
            "interpretation": "A public raw URL returning 404 without authenticated repository access cannot distinguish a missing path from a private repo, ref mismatch, or inaccessible source.",
            "retrieved_date_utc": QVIRTUAL_LAB_RESEARCH_CAPTURED_DATE_UTC,
            "retrieved_at_utc": None,
            "retrieval_time_status": "NOT_CAPTURED",
        },
        "next_action": (
            "Restore or identify the authoritative QENGINEER.md, reconcile every source requirement, "
            "then map owners, implementations, focused tests, simulation evidence, and physical-validation gates."
        ),
    }
    canonical = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode("utf-8")
    plan["plan_sha256"] = hashlib.sha256(canonical).hexdigest()
    return plan


def _file_evidence(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    if not path.is_file() or path.is_symlink():
        return {"path": relative, "status": "missing_or_unsafe", "bytes": None, "sha256": None}
    try:
        content = path.read_bytes()
        text = content.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return {
            "path": relative,
            "status": f"unavailable:{type(exc).__name__}",
            "bytes": None,
            "sha256": None,
        }
    if relative in QVIRTUAL_LAB_METRIC_DOCUMENTS:
        start_marker, end_marker = QVIRTUAL_LAB_METRIC_MARKERS
        start_count, end_count = text.count(start_marker), text.count(end_marker)
        if (start_count, end_count) not in {(0, 0), (1, 1)}:
            return {
                "path": relative,
                "status": "unavailable:invalid_qvirtual_managed_section",
                "bytes": None,
                "sha256": None,
            }
        if start_count:
            start = text.index(start_marker)
            end = text.index(end_marker, start) + len(end_marker)
            text = (text[:start] + text[end:]).rstrip() + "\n"
        content = text.encode("utf-8")
    return {
        "path": relative,
        "status": "observed_local",
        "bytes": len(content),
        "sha256": hashlib.sha256(content).hexdigest(),
        "hash_scope": (
            "authored_content_excluding_qvirtual_metrics"
            if relative in QVIRTUAL_LAB_METRIC_DOCUMENTS
            else "full_file"
        ),
    }


def build_evolution_plan(
    root: Path | str,
    *,
    source_manifest_sha256: str | None = None,
) -> dict[str, Any]:
    """Map existing governance contracts to planned gates without passing them."""
    source_root = Path(root).resolve()
    stages = []
    for sequence, (domain, paths) in enumerate(CONTRACTS, start=1):
        sources = [_file_evidence(source_root, relative) for relative in paths]
        stage_manifest = hashlib.sha256(
            json.dumps(sources, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        stages.append({
            "sequence": sequence,
            "domain": domain,
            "state": "PLANNED",
            "status": "PLANNED",
            "target_documents": list(PLAN_TARGETS.get(domain, ())),
            "source_files": sources,
            "source_sha256": stage_manifest,
            "metrics": {
                "source_manifest_sha256": source_manifest_sha256 or stage_manifest,
                "source_file_count": len(sources),
                "available_source_file_count": sum(item["status"] == "observed_local" for item in sources),
                "missing_or_unavailable_source_file_count": sum(item["status"] != "observed_local" for item in sources),
                "remote_verified": False,
            },
            "blockers": [
                "planned_only; implementation, tests, and semantic review are not inferred",
                "remote exact-SHA evidence is unavailable to this local planner",
            ],
        })

    serialized_stages = json.dumps(stages, sort_keys=True, separators=(",", ":")).encode("utf-8")
    plan_sha256 = hashlib.sha256(serialized_stages).hexdigest()
    manifest_for_plan = source_manifest_sha256 or plan_sha256
    qstats = {
        "stage_count": len(stages),
        "planned_stage_count": len(stages),
        "evolutiono_transition_stage_count": len(EVOLUTIONO_TRANSITION_DOMAINS),
        "evolutiono_transition_completed_stage_count": 0,
        "available_contract_file_count": sum(stage["metrics"]["available_source_file_count"] for stage in stages),
        "missing_or_unavailable_contract_file_count": sum(stage["metrics"]["missing_or_unavailable_source_file_count"] for stage in stages),
        "remote_verified_stage_count": 0,
        "source_manifest_sha256": manifest_for_plan,
        "interpretation": "derived_local_inventory_counts_not_completion_or_remote_proof",
    }
    evolutiono_transition = {
        "status": "PLANNED",
        "stage_domains": list(EVOLUTIONO_TRANSITION_DOMAINS),
        "planned_stage_count": len(EVOLUTIONO_TRANSITION_DOMAINS),
        "completed_stage_count": 0,
        "archive_branch": "qmoi",
        "archive_path_prefix": "qreplaceo/",
        "archive_optional_for_core_runtime": True,
        "automatic_mutation_enabled": False,
        "remote_verified": False,
        "ofca_target_document": "OFCA.md",
        "plan_sha256": plan_sha256,
    }
    return {
        "status": "PLANNED",
        "source_root": str(source_root),
        "source_manifest_sha256": manifest_for_plan,
        "source_scope": "materialized_local_only",
        "remote_verification_complete": False,
        "stages": stages,
        "qstats": qstats,
        "qvirtual_labs": build_qvirtual_labs_plan(
            source_root,
        ),
        "evolutiono_transition": evolutiono_transition,
        "plan_sha256": plan_sha256,
        "blockers": [
            "Plan entries are not execution results or production implementations.",
            "Remote completion requires authorized target-owned terminal exact-SHA and tree evidence.",
        ],
    }