#!/usr/bin/env python3
"""Run the target-owned remote lifecycle with fail-closed evidence.

This command is intended for a GitHub Actions runner. A workspace may submit
it, but only the target repository runner may execute the authoritative stages.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any

from autonomous_completion_engine import AutonomousCompletionEngine, REQUIRED_GATES
from checkpoint_manager import CheckpointManager
from execution_lock import ExecutionLock
from live_activity_events import LiveActivity
from remote_state import read_branch


def command_available(command: str) -> bool:
    return subprocess.run(["sh", "-c", f"command -v {command}"], capture_output=True, check=False).returncode == 0


def run_check(command: list[str], root: Path) -> dict[str, Any]:
    try:
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False, timeout=900)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"status": "UNKNOWN", "command": command, "error": str(exc)}
    return {
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout[-4000:],
        "stderr": result.stderr[-4000:],
    }


def run_lifecycle(root: Path, *, execution_id: str, sync_id: str, mode: str, direction: str, source_repository: str, source_sha: str) -> dict[str, Any]:
    activity = LiveActivity(root, execution_id, source="MASTER_ORCHESTRATOR")
    checkpoint = CheckpointManager(root)
    lock = ExecutionLock(root, sync_id)
    gates: dict[str, str | bool | None] = {name: None for name in REQUIRED_GATES}
    details: dict[str, Any] = {"mode": mode, "direction": direction, "source_repository": source_repository, "source_sha": source_sha, "stages": {}}
    try:
        lock.acquire(execution_id)
    except RuntimeError as exc:
        activity.publish("EXECUTION_BLOCKED", "BLOCKED", "DISCOVERY", str(exc), sync_id=sync_id)
        return {"status": "BLOCKED_REQUIRES_HUMAN", "execution_id": execution_id, "error": str(exc)}

    try:
        activity.publish("AGENT_STARTED", "RUNNING", "DISCOVERY", "Target-owned remote lifecycle started", sync_id=sync_id)
        gates["discovery"] = True
        checkpoint.record_stage(execution_id, "DISCOVERY", "PASS", next_operation="INSPECTION", sync_id=sync_id)

        activity.publish("INSPECTION", "RUNNING", "INSPECTION", "Inspecting target checkout and immutable request")
        request_valid = bool(direction and source_repository and source_sha and len(source_sha) >= 7)
        gates["inspection"] = request_valid
        details["stages"]["inspection"] = {"request_valid": request_valid}
        checkpoint.record_stage(execution_id, "INSPECTION", "PASS" if request_valid else "BLOCKED", next_operation="VALIDATION")

        activity.publish("VALIDATION", "RUNNING", "VALIDATION", "Running deterministic syntax and repository checks")
        syntax = run_check(["python", "-m", "py_compile", "scripts/autonomous_completion_engine.py", "scripts/remote_lifecycle.py", "scripts/qmoictl.py"], root)
        tests = run_check(["python", "-m", "pytest", "tests", "-q"], root)
        gates["validation"] = syntax["status"] == "PASS" and tests["status"] == "PASS"
        details["stages"]["validation"] = {"syntax": syntax, "tests": tests}
        checkpoint.record_stage(execution_id, "VALIDATION", "PASS" if gates["validation"] else "FAIL", next_operation="SECURITY")

        activity.publish("SECURITY", "RUNNING", "SECURITY", "Running dependency security gate")
        security_command = ["python", "-m", "pip_audit", "-r", "requirements.txt"]
        security = run_check(security_command, root) if command_available("python") else {"status": "UNKNOWN", "command": security_command}
        gates["security"] = security["status"] == "PASS"
        details["stages"]["security"] = security
        checkpoint.record_stage(execution_id, "SECURITY", "PASS" if gates["security"] else "BLOCKED", next_operation="REMOTE_MAIN")

        activity.publish("REMOTE_VERIFY", "RUNNING", "REMOTE_MAIN", "Verifying target repository remote state")
        repository = os.environ.get("GITHUB_REPOSITORY")
        remote_main = read_branch(repository, "main") if repository else None
        gates["remote_main"] = bool(remote_main and remote_main.reachable and remote_main.sha)
        details["stages"]["remote_main"] = remote_main.as_dict() if remote_main else {"status": "REMOTE_STATUS_UNAVAILABLE"}
        checkpoint.record_stage(execution_id, "REMOTE_MAIN", "PASS" if gates["remote_main"] else "BLOCKED", next_operation="REMOTE_BACKUP")

        remote_backup = read_branch(repository, "autosync-backup") if repository else None
        gates["remote_backup"] = bool(remote_backup and remote_backup.reachable and remote_backup.sha)
        details["stages"]["remote_backup"] = remote_backup.as_dict() if remote_backup else {"status": "REMOTE_STATUS_UNAVAILABLE"}
        checkpoint.record_stage(execution_id, "REMOTE_BACKUP", "PASS" if gates["remote_backup"] else "BLOCKED", next_operation="Q_VERSION")

        activity.publish("Q_VERSION", "RUNNING", "Q_VERSION", "Checking synchronized Q-version evidence")
        q_version_files = list(root.glob("Q.0.0.*"))
        gates["q_version"] = bool(q_version_files and any(path.is_dir() and (path / "COMPLETION.md").is_file() for path in q_version_files))
        details["stages"]["q_version"] = {"paths": [str(path.relative_to(root)) for path in q_version_files], "verified": gates["q_version"]}
        checkpoint.record_stage(execution_id, "Q_VERSION", "PASS" if gates["q_version"] else "BLOCKED", next_operation="LIVE_ACTIVITY")

        activity.heartbeat("LIVE_ACTIVITY")
        gates["live_activity"] = activity.freshness()["fresh"]
        details["stages"]["live_activity"] = activity.freshness()
        checkpoint.record_stage(execution_id, "LIVE_ACTIVITY", "PASS" if gates["live_activity"] else "BLOCKED", next_operation="CROSS_REPOSITORY")

        gates["cross_repository"] = False
        details["stages"]["cross_repository"] = {"status": "UNKNOWN", "reason": "independent target and source remote evidence not supplied"}
        checkpoint.record_stage(execution_id, "CROSS_REPOSITORY", "BLOCKED", next_operation="FINAL_VERIFICATION")

        result = AutonomousCompletionEngine(root, execution_id).evaluate(
            gates=gates,
            repository_results={"target": {"mode": mode, "direction": direction}},
            errors=["cross-repository verification evidence is unavailable"] if not gates["cross_repository"] else [],
        )
        details["final"] = result.as_dict()
        checkpoint.record_stage(execution_id, "FINAL_VERIFICATION", "PASS" if result.status in {"SUCCESS", "NO_CHANGES_REQUIRED"} else "BLOCKED", final_status=result.status)
        activity.publish("SUCCESS" if result.status in {"SUCCESS", "NO_CHANGES_REQUIRED"} else "FAILURE", "SUCCESS" if result.status in {"SUCCESS", "NO_CHANGES_REQUIRED"} else "BLOCKED", "FINAL_VERIFICATION", f"Remote lifecycle finished with {result.status}", final_status=result.status)
        return result.as_dict()
    finally:
        lock.release(execution_id)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--execution-id", required=True)
    parser.add_argument("--sync-id", required=True)
    parser.add_argument("--direction", required=True)
    parser.add_argument("--source-repository", required=True)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--mode", choices=("dry-run", "apply"), default="dry-run")
    args = parser.parse_args()
    result = run_lifecycle(args.root.resolve(), execution_id=args.execution_id, sync_id=args.sync_id, mode=args.mode, direction=args.direction, source_repository=args.source_repository, source_sha=args.source_sha)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("status") in {"SUCCESS", "NO_CHANGES_REQUIRED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
