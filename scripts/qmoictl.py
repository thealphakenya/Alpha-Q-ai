#!/usr/bin/env python3
"""Safe local control-plane CLI for autonomous completion and synchronization."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from autonomous_completion_engine import AutonomousCompletionEngine, REQUIRED_GATES
from control_plane_supervisor import ControlPlaneSupervisor
from github_auth import preflight_auth
from q_version_manager import QVersionManager
from remote_state import read_workflow_run
from workspace_sync import submit_remote_workflow, write_request


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("autonomous_complete", "status", "verify", "preflight-auth", "reserve-q", "remote-submit", "remote-observe", "control-plane-audit", "control-plane-bootstrap"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--execution-id", default=None)
    parser.add_argument("--target-repository", default=None)
    parser.add_argument("--workflow", default="cross-repository-sync.yml")
    parser.add_argument("--direction", choices=("alpha-to-qmoi", "qmoi-to-alpha"), default=None)
    parser.add_argument("--source-repository", default=None)
    parser.add_argument("--source-sha", default=None)
    parser.add_argument("--mode", choices=("dry-run", "apply"), default="dry-run")
    parser.add_argument("--sync-id", default=None)
    parser.add_argument("--run-id", default=None)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.command in {"control-plane-audit", "control-plane-bootstrap"}:
        supervisor = ControlPlaneSupervisor(root)
        report = supervisor.bootstrap_runtime() if args.command == "control-plane-bootstrap" else supervisor.audit()
        print(json.dumps(report.as_dict(), indent=2, sort_keys=True))
        return 0 if report.status == "READY" else 2
    if args.command == "remote-submit":
        required = {
            "--target-repository": args.target_repository,
            "--direction": args.direction,
            "--source-repository": args.source_repository,
            "--source-sha": args.source_sha,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            parser.error(f"remote-submit requires {', '.join(missing)}")
        request = submit_remote_workflow(
            args.target_repository,
            args.workflow,
            direction=args.direction,
            source_repository=args.source_repository,
            source_sha=args.source_sha,
            mode=args.mode,
            sync_id=args.sync_id,
        )
        request_path = write_request(root, request)
        request["request_path"] = str(request_path)
        print(json.dumps(request, indent=2, sort_keys=True))
        return 0 if request["status"] == "QUEUED" else 2
    if args.command == "remote-observe":
        if not args.target_repository or not args.run_id:
            parser.error("remote-observe requires --target-repository and --run-id")
        result = read_workflow_run(args.target_repository, args.run_id)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result.get("status") == "REMOTE_VERIFIED" else 2
    if args.command == "status":
        state = root / "ollamatracks" / "current_state.json"
        print(state.read_text(encoding="utf-8") if state.is_file() else json.dumps({"status": "UNKNOWN"}))
        return 0
    if args.command == "preflight-auth":
        result = preflight_auth(("thealphakenya/Alpha-Q-ai", "thealphakenya/qmoi-enhanced"), ("contents", "pull-requests", "actions"))
        print(json.dumps(result.as_dict(), indent=2))
        return 0 if result.status == "AUTH_READY" else 2
    if args.command == "reserve-q":
        print(QVersionManager(root).reserve())
        return 0
    if args.command == "verify":
        # Verification reads the persisted evidence; it must never manufacture
        # passing gates merely because the command was requested.
        result = AutonomousCompletionEngine(root, args.execution_id).evaluate()
        print(json.dumps(result.as_dict(), indent=2))
        return 0 if result.status in {"SUCCESS", "NO_CHANGES_REQUIRED"} else 2
    result = AutonomousCompletionEngine(root, args.execution_id).evaluate()
    print(json.dumps(result.as_dict(), indent=2))
    return 0 if result.status in {"SUCCESS", "NO_CHANGES_REQUIRED"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
