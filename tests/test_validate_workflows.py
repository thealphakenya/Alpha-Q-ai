from datetime import datetime, timezone
from pathlib import Path

import pytest

import scripts.validate_workflows as workflow_validator


def test_main_fails_when_any_workflow_yaml_is_invalid(monkeypatch, capsys):
    monkeypatch.setattr(
        workflow_validator,
        "validate_workflow_yaml",
        lambda: ({"valid.yml": {}}, ["invalid.yml failed to parse"]),
    )

    assert workflow_validator.main() == 1
    output = capsys.readouterr().out
    assert "Workflow YAML validation failed" in output
    assert "Local workflow checks passed" not in output


def test_main_fails_when_false_success_prevention_check_fails(monkeypatch, capsys):
    monkeypatch.setattr(
        workflow_validator,
        "validate_workflow_yaml",
        lambda: ({"agent.yml": {}}, []),
    )
    monkeypatch.setattr(workflow_validator, "validate_success_prevention", lambda *_: False)

    assert workflow_validator.main() == 1
    output = capsys.readouterr().out
    assert "False-success prevention validation failed" in output
    assert "Local workflow checks passed" not in output


@pytest.mark.parametrize("failed_gate", ["critical", "agent_cli"])
def test_main_fails_when_critical_or_cli_gate_fails(monkeypatch, capsys, failed_gate):
    monkeypatch.setattr(
        workflow_validator,
        "validate_workflow_yaml",
        lambda: ({"valid.yml": {}}, []),
    )
    monkeypatch.setattr(workflow_validator, "validate_success_prevention", lambda *_: True)
    monkeypatch.setattr(workflow_validator, "check_critical_workflows", lambda: failed_gate != "critical")
    monkeypatch.setattr(workflow_validator, "validate_success_contract_schema", lambda: None)
    monkeypatch.setattr(workflow_validator, "validate_agent_cli", lambda: failed_gate != "agent_cli")

    assert workflow_validator.main() == 1
    output = capsys.readouterr().out
    assert "Local workflow validation failed" in output
    assert "Local workflow checks passed" not in output


def test_main_reports_local_context_without_claiming_remote_readiness(monkeypatch, capsys):
    monkeypatch.setattr(
        workflow_validator,
        "validate_workflow_yaml",
        lambda: ({"valid.yml": {}}, []),
    )
    monkeypatch.setattr(workflow_validator, "validate_success_prevention", lambda *_: True)
    monkeypatch.setattr(workflow_validator, "check_critical_workflows", lambda: True)
    monkeypatch.setattr(workflow_validator, "validate_agent_cli", lambda: True)

    assert workflow_validator.main() == 0
    output = capsys.readouterr().out
    assert f"Repository directory: {Path(__file__).resolve().parents[1].name}" in output
    assert f"Date (UTC): {datetime.now(timezone.utc).date().isoformat()}" in output
    assert "Local workflow checks passed; remote execution and deployment are not verified." in output
    assert "Documented success contract requirements listed" in output
    assert "SUCCESS CONTRACT REQUIREMENTS (NOT DYNAMICALLY VALIDATED)" in output
    assert "ready for GitHub Actions execution" not in output


def test_cross_repository_app_preflight_requires_rotation_confirmation():
    workflow_path = Path(__file__).resolve().parents[1] / ".github/workflows/cross-repo-auth-preflight.yml"
    workflow = workflow_validator.load_workflow(workflow_path)
    steps = workflow["jobs"]["authorization-preflight"]["steps"]
    app_config = next(step for step in steps if step.get("id") == "app-config")
    token_step = next(step for step in steps if step.get("id") == "app-token")
    probe = next(step for step in steps if step.get("name") == "Probe repository and workflow access")

    assert app_config["env"]["APP_KEY_ROTATION_CONFIRMED"] == "${{ vars.QMOI_APP_KEY_ROTATION_CONFIRMED }}"
    assert '"${APP_KEY_ROTATION_CONFIRMED:-}" == "true"' in app_config["run"]
    assert token_step["if"] == "${{ steps.app-config.outputs.use_app == 'true' }}"
    assert "MY_CUSTUOM_TOKEN" not in probe["env"]["CREDENTIAL_ROLE"]
    assert "MY_CUSTOM_TOKEN" not in probe["env"]["CREDENTIAL_ROLE"]
    assert probe["env"]["APP_TOKEN_AVAILABLE"] == "${{ steps.app-token.outputs.token != '' }}"
    assert 'process.env.APP_TOKEN_AVAILABLE !== "true"' in probe["with"]["script"]
    assert 'status: "APP_AUTH_BLOCKED_ROTATION_UNCONFIRMED"' in probe["with"]["script"]
    assert "AUTH_BLOCKED" in probe["with"]["script"]


def test_security_merge_gate_does_not_suppress_npm_audit_failures():
    workflow_path = Path(__file__).resolve().parents[1] / ".github/workflows/security-merge-gates.yml"
    workflow = workflow_validator.load_workflow(workflow_path)

    assert isinstance(workflow, dict)
    audit_steps = [
        step
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
        if "npm audit" in step.get("run", "")
    ]

    assert len(audit_steps) == 1
    assert audit_steps[0]["run"].strip() == "npm audit --omit=dev --audit-level=high"
    assert audit_steps[0].get("continue-on-error") is not True


def test_realtime_monitor_reports_tracking_persistence_failures():
    workflow_path = (
        Path(__file__).resolve().parents[1]
        / ".github/workflows/ollama-autonomous-agent-realtime-monitor.yml"
    )
    workflow = workflow_validator.load_workflow(workflow_path)

    assert isinstance(workflow, dict)
    persistence_steps = [
        step
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
        if step.get("name") == "Persist tracking state"
    ]

    assert len(persistence_steps) == 1
    script = persistence_steps[0]["run"]
    conflict_path = script.split('if ! git rebase "origin/${target_branch}"; then', 1)[1].split(
        "\n            fi", 1
    )[0]
    assert "git rebase --abort || true" in conflict_path
    assert "exit 1" in conflict_path
    assert script.rstrip().endswith("exit 1")


def test_master_orchestrator_report_does_not_invent_validation_results():
    workflow_path = (
        Path(__file__).resolve().parents[1]
        / ".github/workflows/ollama-master-orchestrator.yml"
    )
    workflow = workflow_validator.load_workflow(workflow_path)

    assert isinstance(workflow, dict)
    steps = {
        step.get("name"): step
        for step in workflow["jobs"]["final-status-report"]["steps"]
    }
    status_script = steps["Determine final validation status"]["run"]
    report_script = steps["Compile comprehensive report"]["run"]
    summary_script = steps["Post final summary"]["run"]
    final_gate = steps["Enforce final validation result"]["run"]

    assert "Comprehensive Validation Matrix (aggregate)" in report_script
    assert "Platform Validation | ${{ needs.comprehensive-validation.result }}" not in report_script
    assert "Feature Validation | ${{ needs.comprehensive-validation.result }}" not in report_script
    assert "NOT_REPORTED" in report_script
    assert "| Final Validation | ${{ steps.final_status.outputs.final_status }} |" in report_script
    assert "Comprehensive Validation Matrix (aggregate)" in summary_script
    assert "Platform Validation | ${{ needs.comprehensive-validation.result }}" not in summary_script
    assert "Feature Validation | ${{ needs.comprehensive-validation.result }}" not in summary_script
    assert "| Final Validation | ${{ steps.final_status.outputs.final_status }} |" in summary_script
    for script in (report_script, summary_script):
        assert 'TEST_COUNT="${{ needs.enhanced-test-execution.outputs.test_count }}"' in script
        assert 'TEST_COUNT="NOT_REPORTED"' in script

    for condition in (
        '[ "${TESTS_STATUS}" = "true" ]',
        '[ "${PREFLIGHT_RESULT}" = "success" ]',
        '[ "${MATRIX_RESULT}" = "success" ]',
        '[ "${ENHANCED_TEST_RESULT}" = "success" ]',
        '[ "${AGENT_TRIGGER_RESULT}" = "success" ]',
    ):
        assert condition in status_script

    for condition in (
        '[ "${TESTS_STATUS}" != "true" ]',
        '[ "${PREFLIGHT_RESULT}" != "success" ]',
        '[ "${MATRIX_RESULT}" != "success" ]',
        '[ "${ENHANCED_TEST_RESULT}" != "success" ]',
        '[ "${AGENT_TRIGGER_RESULT}" != "success" ]',
    ):
        assert condition in final_gate
