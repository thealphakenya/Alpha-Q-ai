import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from scripts.qaudit_model_review import (
    AuditModelReviewError,
    MAX_SOURCE_BYTES,
    review_source,
    select_next_priority_candidate,
)


class _Response:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        self.headers: dict[str, str] = {}

    def raise_for_status(self) -> None:
        return None

    def iter_content(self, chunk_size: int):
        yield json.dumps(self.payload).encode("utf-8")

    def close(self) -> None:
        return None


class _Session:
    trust_env = True

    def __init__(self, model_output: dict[str, Any] | None = None) -> None:
        self.model_output = model_output or {"findings": []}
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> _Response:
        self.calls.append((method, url, kwargs))
        if url.endswith("/api/version"):
            return _Response({"version": "0.test"})
        if url.endswith("/api/tags"):
            return _Response({
                "models": [{
                    "name": "review-model:1b",
                    "digest": "sha256:" + "a" * 64,
                }],
            })
        if url.endswith("/api/generate"):
            return _Response({"response": json.dumps(self.model_output)})
        raise AssertionError(f"Unexpected local endpoint path: {url}")


def _repository(root: Path) -> Path:
    (root / "source.py").write_text("def example():\n    return True\n", encoding="utf-8")
    (root / "oe2.txt").write_text("", encoding="utf-8")
    (root / "remotecompletion.md").write_text("", encoding="utf-8")
    (root / "remote-evidence-ledger.jsonl").write_text("", encoding="utf-8")
    (root / "remote-completion.json").write_text(
        json.dumps({"schema_version": "1.0", "state": {}, "blockers": []}),
        encoding="utf-8",
    )
    return root


def test_local_model_review_is_loopback_only_bounded_and_candidate_only(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    session = _Session({
        "findings": [{
            "category": "testing",
            "severity": "low",
            "line": 2,
            "recommendation": "map_requirement_to_test",
        }],
    })

    result = review_source(
        root,
        "source.py",
        "review-model:1b",
        "http://127.0.0.1:11434",
        consent=True,
        session=session,
    )

    artifact = root / result["artifact_path"]
    payload = json.loads(artifact.read_text(encoding="utf-8"))
    assert result["status"] == "CANDIDATES_ONLY"
    assert result["remote_verified"] is False
    assert result["source_modified"] is False
    assert payload["findings"][0]["source_line_sha256"] == hashlib.sha256(
        b"    return True"
    ).hexdigest()
    assert payload["findings"][0]["verification_status"] == "unverified_model_candidate"
    assert payload["selection"]["method"] == "explicit_path"
    assert "def example" not in artifact.read_text(encoding="utf-8")
    assert session.trust_env is False
    assert len(session.calls) == 3
    assert session.calls[-1][2]["json"]["options"] == {
        "temperature": 0,
        "num_ctx": 4096,
        "num_predict": 512,
    }
    assert (root / "source.py").read_text(encoding="utf-8") == "def example():\n    return True\n"


@pytest.mark.parametrize(
    ("path", "endpoint", "consent", "expected_code"),
    [
        ("source.py", "https://127.0.0.1:11434", True, "local_endpoint_invalid"),
        ("source.py", "http://example.com:11434", True, "local_endpoint_not_literal_loopback"),
        ("source.py", "http://127.0.0.1:11434", False, "explicit_local_content_consent_required"),
        ("../outside.py", "http://127.0.0.1:11434", True, "source_path_invalid"),
    ],
)
def test_local_model_review_fails_closed_on_scope_and_consent(
    tmp_path: Path,
    path: str,
    endpoint: str,
    consent: bool,
    expected_code: str,
) -> None:
    root = _repository(tmp_path)

    with pytest.raises(AuditModelReviewError) as raised:
        review_source(root, path, "review-model:1b", endpoint, consent=consent, session=_Session())

    assert raised.value.code == expected_code


def test_local_model_review_blocks_secrets_and_oversized_sources(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    secret = root / "credentials.py"
    secret.write_text("print('not reviewed')\n", encoding="utf-8")
    with pytest.raises(AuditModelReviewError, match="blocked"):
        review_source(root, "credentials.py", "review-model:1b", "http://127.0.0.1:11434", consent=True)

    large = root / "large.py"
    large.write_bytes(b"x" * (MAX_SOURCE_BYTES + 1))
    with pytest.raises(AuditModelReviewError) as raised:
        review_source(root, "large.py", "review-model:1b", "http://127.0.0.1:11434", consent=True)
    assert raised.value.code == "source_size_limit_exceeded"


def test_local_model_review_rejects_uninstalled_models_and_free_text_output(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    missing_model = _Session()
    missing_model.request = lambda method, url, **kwargs: (
        _Response({"version": "0.test"}) if url.endswith("/api/version")
        else _Response({"models": []})
    )
    with pytest.raises(AuditModelReviewError) as raised:
        review_source(root, "source.py", "review-model:1b", "http://127.0.0.1:11434", consent=True, session=missing_model)
    assert raised.value.code == "local_model_not_installed"

    invalid_output = _Session({"findings": [{"summary": "quoted source content"}]})
    with pytest.raises(AuditModelReviewError) as raised:
        review_source(root, "source.py", "review-model:1b", "http://127.0.0.1:11434", consent=True, session=invalid_output)
    assert raised.value.code == "model_output_schema_rejected"


def test_priority_queue_selection_uses_fresh_hashes_and_skips_reviewed_sources(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = _repository(tmp_path)
    reviewed_path = root / "source.py"
    next_path = root / "next.py"
    next_path.write_text("def next_candidate():\n    return None\n", encoding="utf-8")
    reviewed_sha = hashlib.sha256(reviewed_path.read_bytes()).hexdigest()
    next_sha = hashlib.sha256(next_path.read_bytes()).hexdigest()
    report_dir = root / "ollamatracks" / "qaudit_model_reviews"
    report_dir.mkdir(parents=True)
    (report_dir / "prior.json").write_text(
        json.dumps({"source_path": "source.py", "source_sha256": reviewed_sha}),
        encoding="utf-8",
    )
    universe = {
        "audit_queue": {
            "queue_sha256": "queue-digest",
            "source_manifest_sha256": "manifest-digest",
            "items": [
                {"path": "source.py", "sha256": reviewed_sha, "priority": 120, "reasons": ["unavailable"]},
                {"path": "next.py", "sha256": next_sha, "priority": 100, "reasons": ["security"]},
            ],
        },
        "classes": {
            "source.py": {"sha256": reviewed_sha, "content_scan_status": "scanned"},
            "next.py": {"sha256": next_sha, "content_scan_status": "scanned"},
        },
    }
    monkeypatch.setattr(
        "scripts.qaudit_universe.build_qaudit_universe",
        lambda repository_root: universe,
    )

    selected = select_next_priority_candidate(root)

    assert selected == {
        "source": "next.py",
        "priority": 100,
        "reasons": ["security"],
        "priority_queue_sha256": "queue-digest",
        "source_manifest_sha256": "manifest-digest",
        "selection_method": "fresh_deterministic_priority_queue",
    }
