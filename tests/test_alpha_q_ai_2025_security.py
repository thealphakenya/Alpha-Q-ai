import json
import subprocess
from pathlib import Path


def test_alpha_q_ai_2025_npm_audit_has_no_known_vulnerabilities():
    project_dir = Path(__file__).resolve().parents[1] / "Alpha-Q-ai-2025"
    result = subprocess.run(
        ["npm", "audit", "--json", "--omit=dev"],
        cwd=project_dir,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout.strip():
        payload = json.loads(result.stdout)
        total = payload.get("metadata", {}).get("vulnerabilities", {}).get("total", 0)
        assert total == 0, (
            f"npm audit reports vulnerabilities for Alpha-Q-ai-2025: {payload.get('metadata', {}).get('vulnerabilities')}"
        )
    else:
        assert result.returncode == 0, f"npm audit failed without output: {result.stderr}"
