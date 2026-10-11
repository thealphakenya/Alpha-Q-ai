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