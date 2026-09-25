import json
from pathlib import Path

from scripts.runbook_audit import audit, write_report


def test_audit_covers_all_130_requirements(tmp_path: Path):
    source = Path(__file__).resolve().parents[1] / "remotecompletion.md"
    (tmp_path / "remotecompletion.md").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    result = audit(tmp_path)
    assert [item["number"] for item in result["requirements"]] == list(range(1, 131))
    assert result["completion"] == "BLOCKED_AUTH"


def test_audit_writes_machine_report(tmp_path: Path):
    source = Path(__file__).resolve().parents[1] / "remotecompletion.md"
    (tmp_path / "remotecompletion.md").write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    report_path = write_report(tmp_path)
    payload = json.loads(report_path.read_text(encoding="utf-8"))
    assert len(payload["requirements"]) == 130
    assert payload["next_action"]