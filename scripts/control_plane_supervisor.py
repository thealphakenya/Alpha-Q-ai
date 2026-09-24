#!/usr/bin/env python3
"""Audit and bootstrap the deterministic QMOI remote control plane.

This supervisor manages control-plane readiness; it does not replace the
remote target runner and never turns missing implementation or remote evidence
into success. Runtime scaffolding is safe to create, while missing executable
components remain explicit blockers.
"""
from __future__ import annotations

import json
import os
import platform
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_COMPONENTS = {
    "completion_engine": "scripts/autonomous_completion_engine.py",
    "checkpoint_manager": "scripts/checkpoint_manager.py",
    "execution_lock": "scripts/execution_lock.py",
    "git_execution_manager": "scripts/git_execution_manager.py",
    "github_auth": "scripts/github_auth.py",
    "live_activity": "scripts/live_activity_events.py",
    "q_version_manager": "scripts/q_version_manager.py",
    "remote_lifecycle": "scripts/remote_lifecycle.py",
    "remote_state": "scripts/remote_state.py",
    "sync_contract": "scripts/sync_contract.py",
    "workspace_sync": "scripts/workspace_sync.py",
    "cli": "scripts/qmoictl.py",
}
RUNTIME_DIRECTORIES = (
    "ollamatracks/checkpoints",
    "ollamatracks/executions",
    "ollamatracks/requests",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class SupervisorReport:
    status: str
    generated: str
    remote_only: bool
    components: dict[str, dict[str, Any]]
    runtime_directories: dict[str, bool]
    blockers: list[str]
    next_actions: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "generated": self.generated,
            "remote_only": self.remote_only,
            "components": self.components,
            "runtime_directories": self.runtime_directories,
            "blockers": self.blockers,
            "next_actions": self.next_actions,
        }


class ControlPlaneSupervisor:
    """Keep control-plane readiness observable and safely resumable."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root).resolve()
        self.track_dir = self.root / "ollamatracks"

    def audit(self) -> SupervisorReport:
        components: dict[str, dict[str, Any]] = {}
        blockers: list[str] = []
        for name, relative in REQUIRED_COMPONENTS.items():
            path = self.root / relative
            present = path.is_file()
            item = {
                "path": relative,
                "present": present,
                "readable": present and os.access(path, os.R_OK),
            }
            components[name] = item
            if not present:
                blockers.append(f"missing control-plane component: {relative}")
        runtime = {relative: (self.root / relative).is_dir() for relative in RUNTIME_DIRECTORIES}
        blockers.extend(f"missing runtime directory: {relative}" for relative, present in runtime.items() if not present)
        if not (self.root / "QMOI_Ollama_Autonomous_Production_Completion_Master_Plan.md").is_file():
            blockers.append("master plan is unavailable")
        if not (self.root / "ollama_master_topic_index.txt").is_file():
            blockers.append("topic index is unavailable")
        return SupervisorReport(
            status="READY" if not blockers else "BLOCKED",
            generated=utc_now(),
            remote_only=True,
            components=components,
            runtime_directories=runtime,
            blockers=blockers,
            next_actions=(
                ["submit or resume the target-owned remote workflow", "observe remote run and verify final evidence"]
                if not blockers
                else ["install or restore missing control-plane components", "rerun control-plane-audit"]
            ),
        )

    def bootstrap_runtime(self) -> SupervisorReport:
        """Create only empty runtime directories, then re-audit everything."""
        for relative in RUNTIME_DIRECTORIES:
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        report = self.audit()
        payload = report.as_dict()
        payload["bootstrap"] = {
            "performed": True,
            "runner": "remote-target-workflow",
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        }
        self.track_dir.mkdir(parents=True, exist_ok=True)
        temporary = self.track_dir / "control_plane_state.json.tmp"
        temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(self.track_dir / "control_plane_state.json")
        return report


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("command", choices=("audit", "bootstrap"))
    args = parser.parse_args()
    supervisor = ControlPlaneSupervisor(args.root)
    report = supervisor.bootstrap_runtime() if args.command == "bootstrap" else supervisor.audit()
    print(json.dumps(report.as_dict(), indent=2, sort_keys=True))
    return 0 if report.status == "READY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
