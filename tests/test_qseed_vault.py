import json
import subprocess
from pathlib import Path

import pytest

from scripts.qseed_vault import (
    QSeedError,
    audit_vault,
    decrypt_file,
    encrypt_file,
    generate_key,
    main,
)


def _git_repo(root: Path) -> Path:
    root.mkdir()
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "qseed@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "QSeed Test"], check=True)
    (root / "README.md").write_text("# QSeed test\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)
    subprocess.run(
        ["git", "-C", str(root), "commit", "-m", "initialize QSeed test"],
        check=True,
        capture_output=True,
    )
    return root


def test_qseed_encrypt_decrypt_authenticates_payload_without_repo_ciphertext(tmp_path: Path) -> None:
    root = _git_repo(tmp_path / "repo")
    source = root / "memory.txt"
    source.write_text("private qseed test payload\n", encoding="utf-8")
    key_path = tmp_path / "private" / "qseed.key"
    encrypted_path = tmp_path / "vault" / "seed.qseed"
    decrypted_path = tmp_path / "restored" / "memory.txt"
    key_record = generate_key(key_path, root)

    result = encrypt_file(
        source,
        key_path,
        root,
        output_path=encrypted_path,
        kind="memory",
        label="memory fixture",
    )

    assert key_record["status"] == "KEY_CREATED"
    assert key_path.stat().st_mode & 0o777 == 0o600
    assert result["status"] == "ENCRYPTED"
    assert result["plaintext_persisted"] is False
    assert b"private qseed test payload" not in encrypted_path.read_bytes()
    assert not (root / "qseeds").exists()

    restored = decrypt_file(encrypted_path, key_path, decrypted_path, root)

    assert restored["status"] == "DECRYPTED"
    assert restored["plaintext_sha256_verified"] is True
    assert decrypted_path.read_text(encoding="utf-8") == source.read_text(encoding="utf-8")
    assert decrypted_path.stat().st_mode & 0o777 == 0o600


def test_qseed_refuses_wrong_key_overwrite_and_repository_outputs(tmp_path: Path) -> None:
    root = _git_repo(tmp_path / "repo")
    source = root / "payload.txt"
    source.write_text("payload\n", encoding="utf-8")
    key_path = tmp_path / "keys" / "first.key"
    other_key = tmp_path / "keys" / "other.key"
    encrypted_path = tmp_path / "vault" / "seed.qseed"
    generate_key(key_path, root)
    generate_key(other_key, root)
    encrypt_file(source, key_path, root, output_path=encrypted_path)

    with pytest.raises(QSeedError, match="authentication"):
        decrypt_file(encrypted_path, other_key, tmp_path / "restore" / "output.txt", root)
    with pytest.raises(QSeedError, match="outside the repository"):
        encrypt_file(source, key_path, root, output_path=root / "unsafe.qseed")
    with pytest.raises(QSeedError, match="overwrite"):
        encrypt_file(source, key_path, root, output_path=encrypted_path)
    with pytest.raises(QSeedError, match="outside the repository"):
        generate_key(root / "in-repository.key", root)


def test_qseed_refuses_symlinked_paths_and_hard_linked_key(tmp_path: Path) -> None:
    root = _git_repo(tmp_path / "repo")
    source = root / "payload.txt"
    source.write_text("payload\n", encoding="utf-8")
    key_path = tmp_path / "keys" / "qseed.key"
    generate_key(key_path, root)
    hard_link = tmp_path / "keys" / "qseed-copy.key"
    hard_link.hardlink_to(key_path)

    with pytest.raises(QSeedError, match="single hard link"):
        encrypt_file(source, hard_link, root, output_path=tmp_path / "vault" / "seed.qseed")

    symlinked_source = root / "symlinked.txt"
    symlinked_source.symlink_to(source)
    with pytest.raises(QSeedError, match="symlinked"):
        encrypt_file(symlinked_source, key_path, root, output_path=tmp_path / "vault" / "seed.qseed")

    symlinked_parent = tmp_path / "linked-vault"
    symlinked_parent.symlink_to(tmp_path / "vault", target_is_directory=True)
    with pytest.raises(QSeedError, match="symlinked"):
        encrypt_file(source, key_path, root, output_path=symlinked_parent / "seed.qseed")


def test_qseed_rejects_tampered_envelope_without_writing_plaintext(tmp_path: Path) -> None:
    root = _git_repo(tmp_path / "repo")
    source = root / "payload.txt"
    source.write_text("authenticated payload\n", encoding="utf-8")
    key_path = tmp_path / "keys" / "qseed.key"
    encrypted_path = tmp_path / "vault" / "seed.qseed"
    output_path = tmp_path / "restore" / "payload.txt"
    generate_key(key_path, root)
    encrypt_file(source, key_path, root, output_path=encrypted_path)

    envelope = json.loads(encrypted_path.read_text(encoding="utf-8"))
    token = envelope["ciphertext"]
    envelope["ciphertext"] = ("A" if token[0] != "A" else "B") + token[1:]
    encrypted_path.write_text(json.dumps(envelope), encoding="utf-8")

    with pytest.raises(QSeedError, match="authentication"):
        decrypt_file(encrypted_path, key_path, output_path, root)
    assert not output_path.exists()


def test_qseed_audit_reports_ciphertext_hashes_without_decryption(tmp_path: Path) -> None:
    root = _git_repo(tmp_path / "repo")
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "one.qseed").write_bytes(b"ciphertext only")
    (vault / "ignored.txt").write_text("not a seed", encoding="utf-8")

    inventory = audit_vault(vault, root)

    assert inventory["status"] == "INVENTORIED"
    assert inventory["seed_count"] == 1
    assert inventory["plaintext_read"] is False
    assert inventory["seeds"][0]["encrypted_bytes"] == len(b"ciphertext only")


def test_qseed_cli_records_operation_in_paired_completion_evidence(tmp_path: Path, capsys) -> None:
    root = _git_repo(tmp_path / "repo")
    (root / "oe2.txt").write_text("", encoding="utf-8")
    (root / "remotecompletion.md").write_text("", encoding="utf-8")
    (root / "remote-evidence-ledger.jsonl").write_text("", encoding="utf-8")
    (root / "remote-completion.json").write_text(
        json.dumps({"schema_version": "1.0", "state": {}, "blockers": []}),
        encoding="utf-8",
    )
    key_path = tmp_path / "keys" / "qseed.key"

    assert main([
        "--repository-root",
        str(root),
        "generate-key",
        "--key-file",
        str(key_path),
    ]) == 0

    output = json.loads(capsys.readouterr().out)
    checkpoint = output["checkpoint"]
    ledger = [
        json.loads(line)
        for line in (root / "remote-evidence-ledger.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert output["status"] == "KEY_CREATED"
    assert checkpoint["operation"] == "qseed-generate-key"
    assert checkpoint["correlation_id"] == ledger[0]["correlation_id"]
    assert "key_file" not in output
    assert key_path.read_bytes().decode("ascii").strip() not in (root / "oe2.txt").read_text()
