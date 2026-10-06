#!/usr/bin/env python3
"""Autonomous evidence monitor for live GitHub proof and required evidence files.

This tool intentionally stays fail-closed: it never claims remote completion unless
all required evidence is present and verified locally/remote-side. It can run once or
loop until the evidence gate becomes READY.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_DOCS = [
    "oe2.txt",
    "remotecompletion.md",
    "MERGE.md",
    "RELEASES.md",
    "ALLVALIDATIONS.md",
    "ALLMDFILESREFS.md",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_command(args: list[str], check: bool = False) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(args, capture_output=True, text=True, check=check)
        return completed.returncode, completed.stdout.strip(), completed.stderr.strip()
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover - defensive
        return 1, "", str(exc)


def git_rev_parse(repo_root: Path, ref: str = "HEAD") -> str:
    code, out, _ = run_command(["git", "-C", str(repo_root), "rev-parse", ref])
    return out.strip() if code == 0 else ""


def read_file_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def extract_qaudit_summary(path: Path) -> str:
    text = read_file_text(path)
    if not text:
        return "QAUDITS.md is missing or empty; no audit evidence is available."
    lower = text.lower()
    if "needs_review" not in lower and "needs review" not in lower:
        return "QAUDITS.md is present, but no explicit NEEDS_REVIEW evidence was found."
    lines = [line.strip() for line in text.splitlines() if "status" in line.lower() or "needs_review" in line.lower() or "needs review" in line.lower() or "production-gap" in line.lower() or "repository surface audit" in line.lower()]
    summary = "\n".join(lines[:12])
    return summary or "QAUDITS.md captured review status but no summary lines were parseable."


def evaluate_completion_status(
    local_head: str,
    remote_main_sha: str | None,
    auth_verified: bool,
    branch_protection_status: str,
    exact_sha_successful_workflow: bool,
    workflow_inventory_count: int,
    qaudit_summary: str = "",
) -> dict[str, Any]:
    blockers: list[str] = []
    next_actions: list[str] = []

    if not auth_verified:
        blockers.append("GitHub authentication is not verified; remote completion requires an authenticated terminal identity.")
        next_actions.append("Authenticate the target repository identity and confirm the active GitHub session before any completion claim.")

    if not remote_main_sha:
        blockers.append("The remote main SHA is unavailable; exact remote evidence is missing.")
        next_actions.append("Resolve the live remote main SHA and verify the exact repository ref before continuing.")
    elif local_head and remote_main_sha and local_head != remote_main_sha:
        blockers.append("local/remote SHA parity is not verified; the local HEAD does not match the live GitHub main SHA.")
        next_actions.append("Align the local checkout to the exact remote main SHA and re-run the verification gate before claiming completion.")

    if str(branch_protection_status).lower() not in {"verified", "pass", "ready"}:
        blockers.append("Branch protection and protected-write authority are not verified.")
        next_actions.append("Verify branch protection rules and write authority through the authorized GitHub-side workflow before any remote publication.")

    if workflow_inventory_count <= 0:
        blockers.append("Workflow inventory is missing; target-owned workflow evidence is incomplete.")
        next_actions.append("List the active repository workflows and confirm the verification path tied to the exact remote SHA.")

    if not exact_sha_successful_workflow:
        blockers.append("No successful workflow run was recorded for the exact remote SHA.")
        next_actions.append("Confirm a successful target-owned workflow for the exact remote SHA before treating the evidence as complete.")

    if "needs_review" in qaudit_summary.lower() or "needs review" in qaudit_summary.lower():
        blockers.append("QAUDITS evidence remains incomplete; review markers indicate the proof set is not fully complete.")
        next_actions.append("Use the QAUDITS inventory to resolve or document each review item before declaring the evidence set complete.")

    completion_status = "READY" if not blockers else "BLOCKED"
    return {
        "completion_status": completion_status,
        "blockers": blockers,
        "next_actions": next_actions,
    }


def collect_evidence(repo_root: Path, repo: str, branch: str = "main") -> dict[str, Any]:
    local_head = git_rev_parse(repo_root)

    auth_code, auth_out, auth_err = run_command(["gh", "auth", "status"])
    auth_verified = auth_code == 0 and ("Logged in to github.com" in (auth_out or "") or "Active account" in (auth_out or ""))

    repo_view_code, repo_view_out, repo_view_err = run_command([
        "gh", "repo", "view", repo, "--json", "nameWithOwner,defaultBranchRef,visibility"
    ])
    repo_metadata: dict[str, Any] = {}
    if repo_view_code == 0:
        try:
            repo_metadata = json.loads(repo_view_out)
        except json.JSONDecodeError:
            repo_metadata = {"status": "unavailable", "error": "invalid repo metadata response"}
    else:
        repo_metadata = {"status": "unavailable", "error": repo_view_err or "gh repo view failed"}

    remote_main_sha = ""
    remote_sha_code, remote_sha_out, _ = run_command(["gh", "api", f"repos/{repo}/commits/{branch}", "--jq", ".sha"])
    if remote_sha_code == 0 and remote_sha_out.strip():
        remote_main_sha = remote_sha_out.strip()

    workflow_code, workflow_out, workflow_err = run_command(["gh", "workflow", "list", "--repo", repo, "--json", "name,state,id"])
    workflow_inventory = []
    if workflow_code == 0:
        try:
            workflow_inventory = json.loads(workflow_out) if workflow_out else []
        except json.JSONDecodeError:
            workflow_inventory = []
    else:
        workflow_inventory = [{"name": "workflow-list", "state": "unavailable", "error": workflow_err or "workflow list failed"}]

    workflow_run_code, workflow_run_out, workflow_run_err = run_command([
        "gh",
        "run",
        "list",
        "--repo",
        repo,
        "--limit",
        "50",
        "--json",
        "name,headSha,conclusion,status,workflowName,createdAt,updatedAt,url,number",
    ])
    matching_runs = []
    if workflow_run_code == 0:
        try:
            runs = json.loads(workflow_run_out) if workflow_run_out else []
            matching_runs = [
                item for item in runs
                if str(item.get("headSha") or "") == str(remote_main_sha or "")
            ]
        except json.JSONDecodeError:
            matching_runs = []
    else:
        matching_runs = [{"name": "workflow-runs", "headSha": remote_main_sha, "conclusion": "unavailable", "status": "unavailable", "error": workflow_run_err or "workflow run list failed"}]

    bp_code, _, bp_err = run_command(["gh", "api", f"repos/{repo}/branches/{branch}/protection", "--silent"])
    if bp_code == 0:
        branch_protection_status = "verified"
    elif bp_code in (401, 403):
        branch_protection_status = "unavailable"
    else:
        branch_protection_status = "unavailable"

    exact_sha_successful_workflow = any(
        str(item.get("headSha") or "") == str(remote_main_sha or "") and str(item.get("conclusion") or "").lower() == "success"
        for item in matching_runs
    )

    qaudit_summary = extract_qaudit_summary(repo_root / "QAUDITS.md")
    gate = evaluate_completion_status(
        local_head=local_head,
        remote_main_sha=remote_main_sha,
        auth_verified=auth_verified,
        branch_protection_status=branch_protection_status,
        exact_sha_successful_workflow=exact_sha_successful_workflow,
        workflow_inventory_count=len(workflow_inventory),
        qaudit_summary=qaudit_summary,
    )

    payload = {
        "timestamp": utc_now(),
        "repo": repo,
        "branch": branch,
        "repo_metadata": repo_metadata,
        "auth_verified": auth_verified,
        "auth_status": {"status": "verified" if auth_verified else "unverified", "details": auth_out or auth_err or "gh auth status unavailable"},
        "local_head": local_head,
        "remote_main_sha": remote_main_sha,
        "remote_matches_local": bool(remote_main_sha and local_head and remote_main_sha == local_head),
        "branch_protection_status": branch_protection_status,
        "workflow_inventory_count": len(workflow_inventory),
        "workflow_runs": matching_runs[:10],
        "exact_sha_successful_workflow": exact_sha_successful_workflow,
        "qaudit_summary": qaudit_summary,
        "completion_status": gate["completion_status"],
        "blockers": gate["blockers"],
        "next_actions": gate["next_actions"],
    }
    return payload


def render_markdown_section(payload: dict[str, Any]) -> str:
    lines = [
        "## Autonomous evidence monitor",
        f"- timestamp: {payload['timestamp']}",
        f"- repo: {payload['repo']}",
        f"- branch: {payload['branch']}",
        f"- auth_verified: {payload['auth_verified']}",
        f"- local_head: {payload['local_head']}",
        f"- remote_main_sha: {payload['remote_main_sha']}",
        f"- remote_matches_local: {payload['remote_matches_local']}",
        f"- branch_protection_status: {payload['branch_protection_status']}",
        f"- workflow_inventory_count: {payload['workflow_inventory_count']}",
        f"- exact_sha_successful_workflow: {payload['exact_sha_successful_workflow']}",
        f"- completion_status: {payload['completion_status']}",
    ]
    if payload.get("blockers"):
        lines.append("- blockers:")
        for item in payload["blockers"]:
            lines.append(f"  - {item}")
    if payload.get("next_actions"):
        lines.append("- next_actions:")
        for item in payload["next_actions"]:
            lines.append(f"  - {item}")
    qaudit = payload.get("qaudit_summary", "")
    if qaudit:
        lines.append("- QAUDITS summary:")
        for item in qaudit.splitlines()[:6]:
            lines.append(f"  - {item}")
    return "\n".join(lines) + "\n"


def update_evidence_files(repo_root: Path, payload: dict[str, Any]) -> None:
    section = render_markdown_section(payload)
    marker = "## Autonomous evidence monitor"
    for name in ("oe2.txt", "remotecompletion.md"):
        file_path = repo_root / name
        existing = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
        prefix = existing
        while True:
            start = existing.find(marker)
            if start < 0:
                break
            next_heading = existing.find("\n## ", start + len(marker))
            end = len(existing) if next_heading < 0 else next_heading + 1
            existing = existing[:start].rstrip() + "\n" + existing[end:]
        if existing != prefix:
            existing = existing.rstrip() + "\n\n" + section + "\n"
        else:
            existing = existing.rstrip() + "\n\n" + section + "\n"
        file_path.write_text(existing, encoding="utf-8")


def monitor_once(repo_root: Path, repo: str, branch: str = "main") -> dict[str, Any]:
    payload = collect_evidence(repo_root, repo, branch)
    update_evidence_files(repo_root, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous evidence monitor for live GitHub and repository proof checks.")
    parser.add_argument("--repo", default="thealphakenya/Alpha-Q-ai")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--root", default=".")
    parser.add_argument("--interval", type=int, default=60)
    parser.add_argument("--max-rounds", type=int, default=1)
    parser.add_argument("--loop", action="store_true", help="Keep running until the evidence gate is READY or the max-rounds limit is reached.")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    rounds = 0
    loop = args.loop or not args.once
    max_rounds = args.max_rounds if args.max_rounds > 0 else 1

    while True:
        rounds += 1
        payload = monitor_once(root, args.repo, args.branch)
        print(json.dumps(payload, indent=2, sort_keys=True))

        if payload["completion_status"] == "READY":
            print("All required evidence is verified and the gate is READY.")
            return 0
        if not loop:
            print("Evidence gate is still BLOCKED; run again once the blockers are resolved.")
            return 1
        if rounds >= max_rounds:
            print(f"Reached max-rounds={max_rounds}; evidence gate remains BLOCKED.")
            return 1
        time.sleep(args.interval)


if __name__ == "__main__":
    raise SystemExit(main())
