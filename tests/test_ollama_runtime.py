import json
import os
from pathlib import Path

import pytest

from scripts.ollama_runtime import (
    HEALTH_SENTINEL,
    OllamaBootstrap,
    OllamaClient,
    OllamaRuntimeError,
    build_success_contract,
    parse_repair_plan,
    validate_repair_paths,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return FakeResponse(response)


def test_verify_proves_model_and_inference():
    session = FakeSession([
        {"models": [{"name": "qwen2.5-coder:3b"}]},
        {"version": "0.1.0"},
        {"models": [{"name": "qwen2.5-coder:3b"}]},
        {"response": HEALTH_SENTINEL},
    ])
    health = OllamaClient(session=session, retries=1).verify()
    assert health.ollama_started is True
    assert health.ollama_healthy is True
    assert health.model_available is True
    assert health.inference_verified is True
    assert health.ollama_version == "0.1.0"


def test_bootstrap_reuses_healthy_server():
    session = FakeSession([{"models": []}])
    client = OllamaClient(session=session, retries=1)
    assert OllamaBootstrap(client).ensure_server() is True


def test_bootstrap_reports_missing_binary(monkeypatch):
    session = FakeSession([ConnectionError("offline")])
    client = OllamaClient(session=session, retries=1)
    monkeypatch.setattr(OllamaBootstrap, "_find_binary", staticmethod(lambda: None))
    with pytest.raises(OllamaRuntimeError, match="not installed"):
        OllamaBootstrap(client).ensure_server()


def test_bootstrap_installs_missing_binary(monkeypatch):
    session = FakeSession([ConnectionError("offline"), {"models": []}])
    client = OllamaClient(session=session, retries=1)

    class StubProcess:
        stderr = None

        def poll(self):
            return None

    monkeypatch.setattr(OllamaBootstrap, "_find_binary", staticmethod(lambda: None))
    monkeypatch.setattr(OllamaBootstrap, "_install_binary", staticmethod(lambda: "/usr/local/bin/ollama"))
    monkeypatch.setattr("scripts.ollama_runtime.subprocess.Popen", lambda *args, **kwargs: StubProcess())

    assert OllamaBootstrap(client).ensure_server() is True


def test_verify_fails_when_server_is_unavailable():
    session = FakeSession([OllamaRuntimeError("offline")])
    with pytest.raises(OllamaRuntimeError):
        OllamaClient(session=session, retries=1).verify()


def test_verify_pulls_missing_model_then_infers():
    session = FakeSession([
        {"models": []},
        {"version": "0.1.0"},
        {"models": []},
        {"status": "success"},
        {"models": [{"name": "qwen2.5-coder:3b"}]},
        {"response": HEALTH_SENTINEL},
    ])
    health = OllamaClient(session=session, retries=1).verify()
    assert health.model_available is True
    assert any(call[0] == "POST" and call[1].endswith("/api/pull") for call in session.calls)


def test_repair_plan_rejects_malformed_and_unsafe_content(tmp_path: Path):
    with pytest.raises(OllamaRuntimeError):
        parse_repair_plan("not-json", tmp_path)
    with pytest.raises(OllamaRuntimeError):
        parse_repair_plan(json.dumps({"changes": [{"path": "../secret", "content": "x"}]}), tmp_path)
    with pytest.raises(OllamaRuntimeError):
        parse_repair_plan(json.dumps({"changes": [{"path": "safe.py", "content": "GITHUB_TOKEN"}]}), tmp_path)


def test_validate_repair_paths_rejects_protected_paths(tmp_path: Path):
    with pytest.raises(OllamaRuntimeError):
        validate_repair_paths(tmp_path, [".github/workflows/job.yml"])
    with pytest.raises(OllamaRuntimeError):
        validate_repair_paths(tmp_path, ["/etc/passwd"])


def test_success_contract_cannot_report_success_without_validation(tmp_path: Path):
    session = FakeSession([
        {"models": [{"name": "qwen2.5-coder:3b"}]},
        {"version": "0.1.0"},
        {"models": [{"name": "qwen2.5-coder:3b"}]},
        {"response": HEALTH_SENTINEL},
    ])
    health = OllamaClient(session=session, retries=1).verify()
    contract = build_success_contract(
        tmp_path,
        health,
        llm_coding_started=True,
        validation_passed=False,
        checkpoint_created=True,
    )
    assert contract["final_status"] == "FAILED"


def test_success_contract_accepts_agent_health_mapping(tmp_path: Path):
    health = {
        "ollama_started": True,
        "ollama_healthy": True,
        "model_available": True,
        "inference_verified": True,
    }
    contract = build_success_contract(
        tmp_path,
        health,
        llm_coding_started=True,
        validation_passed=True,
        checkpoint_created=True,
    )
    assert contract["final_status"] == "SUCCESS"


def test_run_autonomous_loop_recovers_from_transient_model_500(monkeypatch, tmp_path: Path):
    from scripts.ollama_autonomous_agent import OllamaAutonomousAgent

    agent = OllamaAutonomousAgent(tmp_path)
    attempts = {"count": 0}

    monkeypatch.setattr(
        agent,
        "verify_ollama",
        lambda: {
            "ollama_host": "http://127.0.0.1:11434",
            "model": "qwen2.5-coder:3b",
            "ollama_started": True,
            "ollama_healthy": True,
            "ollama_version": "0.34.2",
            "model_available": True,
            "inference_verified": True,
            "inference_latency": 0.1,
            "health_timestamp": "2026-09-18T00:00:00Z",
            "error": None,
        },
    )
    monkeypatch.setattr(agent, "_repository_context", lambda: ["README.md"])
    monkeypatch.setattr(agent, "run_lint_suite", lambda: True)
    monkeypatch.setattr(agent, "run_full_validation_suite", lambda: True)
    monkeypatch.setattr(agent, "record_tracker_event", lambda *args, **kwargs: None)

    def fake_checkpoint(*args, **kwargs):
        checkpoint_path = tmp_path / "checkpoint.json"
        checkpoint_path.write_text("{}", encoding="utf-8")
        return checkpoint_path

    monkeypatch.setattr(agent, "update_resume_checkpoint", fake_checkpoint)

    def fake_generate(prompt):
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise OllamaRuntimeError("Ollama request failed: 500 Server Error")
        return json.dumps({"summary": "ok", "changes": []})

    monkeypatch.setattr(agent.ollama, "generate", fake_generate)

    result = agent.run_autonomous_loop()
    assert result["final_status"] == "SUCCESS"
    assert attempts["count"] >= 2


def test_agent_rejects_non_github_hosted_runtime(monkeypatch, tmp_path):
    monkeypatch.setenv("QMOI_RUNTIME_MODE", "github-hosted")
    monkeypatch.setenv("QMOI_GITHUB_HOSTED", "true")
    monkeypatch.setenv("QMOI_REQUIRE_GITHUB_HOSTED", "true")
    monkeypatch.setenv("GITHUB_ACTIONS", "false")

    from scripts.ollama_autonomous_agent import OllamaAutonomousAgent

    agent = OllamaAutonomousAgent(tmp_path)
    with pytest.raises(RuntimeError, match="GitHub-hosted"):
        agent.enforce_github_runtime()


def test_validate_release_assets_handles_full_release_list(monkeypatch):
    captured = []

    def fake_run(*args, **kwargs):
        return type("Result", (), {"stdout": '{"tag_name":"v1.2.5","assets":["https://example.com/app.zip"]}', "returncode": 0})()

    monkeypatch.setattr("scripts.link_validator.subprocess.run", fake_run)
    monkeypatch.setattr(
        "scripts.link_validator.LinkValidator.add_checked",
        lambda self, url, source, link_type: captured.append((url, source, link_type)),
    )

    LinkValidator = __import__("scripts.link_validator", fromlist=["LinkValidator"]).LinkValidator
    validator = LinkValidator()
    validator.validate_release_assets()

    assert captured == [("https://example.com/app.zip", "release:v1.2.5", "release_asset")]


def test_validate_rendered_page_detects_expected_markers(monkeypatch):
    LinkValidator = __import__("scripts.link_validator", fromlist=["LinkValidator"]).LinkValidator
    validator = LinkValidator()

    monkeypatch.setattr(validator, "check_url", lambda url: (True, 200, None))
    monkeypatch.setattr(
        validator,
        "fetch_rendered_html",
        lambda url: "<html><head><title>QMOI AI</title></head><body><h1>QMOI AI</h1></body></html>",
    )

    result = validator.validate_rendered_page("https://qmoi.com", ("QMOI", "AI"))

    assert result.accessible is True
    assert result.status_code == 200
    assert result.rendered_ok is True


def test_validate_rendered_page_flags_missing_content(monkeypatch):
    LinkValidator = __import__("scripts.link_validator", fromlist=["LinkValidator"]).LinkValidator
    validator = LinkValidator()

    monkeypatch.setattr(validator, "check_url", lambda url: (True, 200, None))
    monkeypatch.setattr(
        validator,
        "fetch_rendered_html",
        lambda url: "<html><body><h1>Something else</h1></body></html>",
    )

    result = validator.validate_rendered_page("https://qmoi.com", ("QMOI", "AI"))

    assert result.accessible is True
    assert result.rendered_ok is False
    assert "QMOI" in (result.error or "")


def test_validate_product_catalog_covers_apps_docs_and_platforms(tmp_path):
    from scripts.link_validator import LinkValidator

    required_docs = (
        "QSTREAM.md", "QMOIAI.md", "QCITY.md", "QMOISPACE.md", "QALPHA.md",
        "QUANTUM.md", "QMOICLONEQUANTUM.md", "QMOICLONEVERCEL.md",
        "QUANTUMPAYED.md", "VERCELPAYED.md", "MASTEROWNS.md", "STYLES.md",
        "UNIVERSALS.md", "UNIVERSAL.md", "CLONE_PLATFORM_UI.md",
        "VERCELLINKS.md",
    )
    for name in required_docs:
        (tmp_path / name).write_text("# Document\n", encoding="utf-8")

    app_ids = ("qmoiaiui", "qcity", "qmoi-space", "qalpha", "qstream")
    qstore_rows = []
    link_rows = []
    for app_id in app_ids:
        repo = "thealphakenya/qstream" if app_id == "qstream" else "thealphakenya/qmoi-enhanced"
        doc = {
            "qmoiaiui": "QMOIAI.md",
            "qcity": "QCITY.md",
            "qmoi-space": "QMOISPACE.md",
            "qalpha": "QALPHA.md",
            "qstream": "QSTREAM.md",
        }[app_id]
        name = app_id
        qstore_rows.append(
            f"| `{app_id}` ({name}) | app | [repository](https://github.com/{repo}) | [{doc}]({doc}) | unverified |"
        )
        link_rows.append(
            f"| `{app_id}` ({name}) | [repository](https://github.com/{repo}) | [{doc}]({doc}) | unverified |"
        )

    platforms = "\n".join(f"### {platform}" for platform in (
        "windows", "macos", "linux", "ios", "android", "web"
    ))
    (tmp_path / "QSTORE.md").write_text("\n".join(qstore_rows) + "\n" + platforms, encoding="utf-8")
    (tmp_path / "APP_LINKS.md").write_text("\n".join(link_rows), encoding="utf-8")

    report = LinkValidator(str(tmp_path)).validate_product_catalog()

    assert report["passed"] is True
    assert report["app_count"] == 5
    assert len(report["platforms"]) == 6
    assert report["remote_reachability_checked"] is False


def test_validate_product_catalog_fails_closed_when_local_app_doc_is_missing(tmp_path):
    from scripts.link_validator import LinkValidator

    for name in (
        "QSTREAM.md", "QMOIAI.md", "QCITY.md", "QMOISPACE.md", "QALPHA.md",
        "QUANTUM.md", "QMOICLONEQUANTUM.md", "QMOICLONEVERCEL.md",
        "QUANTUMPAYED.md", "VERCELPAYED.md", "MASTEROWNS.md", "STYLES.md",
        "UNIVERSALS.md", "UNIVERSAL.md", "CLONE_PLATFORM_UI.md", "VERCELLINKS.md",
    ):
        (tmp_path / name).write_text("# Document\n", encoding="utf-8")
    (tmp_path / "QSTORE.md").write_text(
        "| `qstream` (QStream) | media | [repository](https://github.com/thealphakenya/qstream) | [QSTREAM.md](QSTREAM.md) | unverified |\n"
        "\n".join(f"### {platform}" for platform in ("windows", "macos", "linux", "ios", "android", "web")),
        encoding="utf-8",
    )
    (tmp_path / "APP_LINKS.md").write_text(
        "| `qstream` (QStream) | [repository](https://github.com/thealphakenya/qstream) | [QSTREAM.md](QSTREAM.md) | unverified |",
        encoding="utf-8",
    )
    (tmp_path / "QSTREAM.md").unlink()

    report = LinkValidator(str(tmp_path)).validate_product_catalog()

    assert report["passed"] is False
    assert any("QSTREAM.md" in error for error in report["errors"])


def test_validate_clone_platform_links_covers_qvillage_and_quantum(tmp_path):
    from scripts.link_validator import LinkValidator

    required_files = {
        "QSTORE.md": "| `qstream` (QStream) | [repository](https://github.com/thealphakenya/qstream) | [QSTREAM.md](QSTREAM.md) | unverified |\n\n### windows\n### macos\n### linux\n### ios\n### android\n### web\n",
        "APP_LINKS.md": "| `qstream` (QStream) | [repository](https://github.com/thealphakenya/qstream) | [QSTREAM.md](QSTREAM.md) | unverified |\n| `qvillage` (QVillage) | [repository](https://github.com/thealphakenya/qvillage) | [QVILLAGE.md](QVILLAGE.md) | Source reference |\n| `quantum` (Quantum) | [repository](https://github.com/thealphakenya/Alpha-Q-ai) | [QUANTUM.md](QUANTUM.md) | Hosted capability plan |",
        "VERCELLINKS.md": "- Vercel: https://vercel.com\n- QVillage: https://github.com/thealphakenya/qvillage\n- Quantum: https://github.com/thealphakenya/Alpha-Q-ai\n",
        "QVILLAGE.md": "# QVillage\n\nQVillage is linked at https://github.com/thealphakenya/qvillage and https://qvillage.qmoi.com.\n",
        "QUANTUM.md": "# Quantum\n\nQuantum is linked at https://github.com/thealphakenya/Alpha-Q-ai and https://quantum.qmoi.com.\n",
        "QSTREAM.md": "# QStream\n\nQStream source: https://github.com/thealphakenya/qstream\n",
        "QMOICLONEVERCEL.md": "# Clone Vercel\n\nVercel clone: https://vercel.com\n",
        "QMOICLONEQUANTUM.md": "# Clone Quantum\n\nQuantum clone: https://github.com/thealphakenya/Alpha-Q-ai\n",
    }
    for name, content in required_files.items():
        (tmp_path / name).write_text(content, encoding="utf-8")

    report = LinkValidator(str(tmp_path)).validate_clone_platform_links()

    assert report["passed"] is True
    assert "qvillage" in report["required_platforms"]
    assert "quantum" in report["required_platforms"]
    assert report["missing_links"] == []
