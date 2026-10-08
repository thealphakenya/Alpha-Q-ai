import json
import subprocess
from pathlib import Path

from scripts.qaudit_universe import build_lion_universe


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def test_lion_universe_covers_variations_extensions_and_delivery_surfaces(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "qaudits@example.invalid")
    _git(repo, "config", "user.name", "QAudits Test")

    paths = {
        "docs/lion_variations/lion-cloud.md": "# Lion Cloud\n",
        "docs/lion_variations/lion-ai.md": "# Lion AI\n",
        "scripts/lion_plugins/lion_cloud.py": "LION_VARIATION = 'cloud'\n",
        "assets/lion-logo.svg": "<svg/>\n",
        "config/lion_settings.json": '{"variant": "cloud"}\n',
        ".github/workflows/lion-release.yml": "name: release\n",
        "download/LION.md": "# Download\n",
        "production.md": "# production\n",
        "productionenhanced.md": "# enhanced production\n",
        "qmoi-enhanced-history-14/docs/lion_variations/lion-enterprise.md": "# Lion Enterprise\n",
    }
    for relative, content in paths.items():
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "add lion evidence")
    _git(repo, "branch", "lion-variation-audit")

    universe = build_lion_universe(repo)

    assert universe["status"] == "NEEDS_REVIEW"
    assert universe["remote_verification_complete"] is False
    assert universe["metrics"]["variation_count"] == 3
    assert universe["metrics"]["extension_candidate_count"] >= 1
    assert universe["metrics"]["logo_candidate_count"] >= 1
    assert universe["metrics"]["settings_candidate_count"] >= 1
    assert universe["metrics"]["automation_candidate_count"] >= 1
    assert universe["metrics"]["release_candidate_count"] >= 1
    assert universe["metrics"]["documentation_candidate_count"] >= 4
    assert universe["metrics"]["ref_count"] >= 1
    assert universe["metrics"]["ref_coverage_complete"] is False
    assert any(item["path"] == "docs/lion_variations/lion-cloud.md" for item in universe["variations"])
    assert any(item["path"] == "qmoi-enhanced-history-14/docs/lion_variations/lion-enterprise.md" for item in universe["variations"])
    assert any(item["path"] == "scripts/lion_plugins/lion_cloud.py" for item in universe["extension_candidates"])
    assert any(item["path"] == ".github/workflows/lion-release.yml" for item in universe["delivery_candidates"])
    assert universe["artifacts"]["manifest_path"].endswith("lion_universe.json")
    assert universe["metrics"]["source_manifest_sha256"]


def test_lion_universe_keeps_all_refs_and_rejects_false_completion(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "qaudits@example.invalid")
    _git(repo, "config", "user.name", "QAudits Test")
    (repo / "docs").mkdir()
    (repo / "docs" / "lion-core.md").write_text("# core\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "base")
    _git(repo, "branch", "feature/lion-audit")

    universe = build_lion_universe(repo)

    assert universe["metrics"]["ref_count"] >= 2
    assert universe["metrics"]["ref_coverage_complete"] is False
    assert universe["metrics"]["local_tree_verified"] is False
    assert universe["metrics"]["remote_verification_complete"] is False
    assert universe["blockers"]
    assert "source_manifest_sha256" in json.dumps(universe)
