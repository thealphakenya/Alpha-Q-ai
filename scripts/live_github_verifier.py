#!/usr/bin/env python3
"""Advanced GitHub state verification for the remote-first completion gate."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_gh(args: list[str]) -> tuple[str | None, str | None, int]:
    """Run a GitHub CLI command and return stdout/stderr and exit code."""
    try:
        result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc), 1
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def parse_repo_view(repo: str) -> dict[str, Any]:
    stdout, stderr, code = run_gh(["repo", "view", repo, "--json", "nameWithOwner,defaultBranchRef,visibility"])
    if code != 0:
        return {"status": "unavailable", "error": stderr or "gh repo view failed", "repo": repo}
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return {"status": "unavailable", "error": "invalid repo metadata response", "repo": repo}
    return {
        "repo": payload.get("nameWithOwner") or repo,
        "default_branch": (payload.get("defaultBranchRef") or {}).get("name") if isinstance(payload.get("defaultBranchRef"), dict) else payload.get("defaultBranchRef"),
        "visibility": payload.get("visibility"),
        "status": "verified" if payload.get("nameWithOwner") else "unavailable",
    }


def parse_auth_status() -> dict[str, Any]:
    stdout, stderr, code = run_gh(["auth", "status"])
    if code != 0:
        return {"status": "unauthenticated", "error": stderr or "gh auth status failed", "verified": False}
    logged_in = "Logged in to github.com" in (stdout or "") or "Active account" in (stdout or "")
    return {
        "status": "verified" if logged_in else "unauthenticated",
        "verified": logged_in,
        "details": stdout or "",
    }


def parse_workflows(repo: str) -> list[dict[str, Any]]:
    stdout, stderr, code = run_gh(["workflow", "list", "--repo", repo, "--json", "name,state,id"])
    if code != 0:
        return [{"name": "workflow-list", "state": "unavailable", "error": stderr or "workflow list failed"}]
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return [{"name": "workflow-list", "state": "unavailable", "error": "invalid workflow response"}]
    return payload if isinstance(payload, list) else []


def parse_workflow_runs(
    repo: str,
    remote_sha: str | None = None,
    limit: int = 50,
    branch: str | None = None,
) -> list[dict[str, Any]]:
    stdout, stderr, code = run_gh([
        "run",
        "list",
        "--repo",
        repo,
        "--limit",
        str(limit),
        "--json",
        "databaseId,name,headSha,headBranch,conclusion,status,workflowName,createdAt,updatedAt,url,number",
    ])
    if code != 0:
        return [{"name": "workflow-runs", "headSha": remote_sha, "conclusion": "unavailable", "status": "unavailable", "error": stderr or "workflow run list failed"}]
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        return [{"name": "workflow-runs", "headSha": remote_sha, "conclusion": "unavailable", "status": "unavailable", "error": "invalid workflow run response"}]
    runs = payload if isinstance(payload, list) else []
    if remote_sha:
        runs = [run for run in runs if str(run.get("headSha") or "") == str(remote_sha)]
    if branch:
        runs = [run for run in runs if str(run.get("headBranch") or "") == branch]
    return runs


def parse_branch_protection(repo: str, branch: str) -> str:
    stdout, stderr, code = run_gh(["api", f"repos/{repo}/branches/{branch}/protection", "--silent"])
    if code == 0:
        return "verified"
    if code in (401, 403):
        return "unknown"
    return "unavailable"


def parse_remote_main_sha(repo: str, branch: str) -> str | None:
    stdout, stderr, code = run_gh(["api", f"repos/{repo}/commits/{branch}", "--jq", ".sha"])
    if code != 0:
        return None
    sha = (stdout or "").strip()
    return sha if sha else None


def parse_remote_tree_sha(repo: str, commit_sha: str | None) -> str | None:
    if not commit_sha:
        return None
    stdout, stderr, code = run_gh([
        "api",
        f"repos/{repo}/git/commits/{commit_sha}",
        "--jq",
        ".tree.sha",
    ])
    if code != 0:
        return None
    tree_sha = (stdout or "").strip()
    return tree_sha if tree_sha else None


def summarize_codeql_evidence(
    workflows: list[dict[str, Any]],
    workflow_runs: list[dict[str, Any]],
    remote_sha: str | None,
    branch: str,
) -> dict[str, Any]:
    codeql_workflows = sorted({
        str(workflow.get("name") or "")
        for workflow in workflows
        if isinstance(workflow, dict) and "codeql" in str(workflow.get("name") or "").casefold()
    })
    codeql_runs = [
        run for run in workflow_runs
        if isinstance(run, dict)
        and "codeql" in str(run.get("workflowName") or run.get("name") or "").casefold()
    ]
    exact_runs = [
        run for run in codeql_runs
        if remote_sha
        and str(run.get("headSha") or "") == remote_sha
        and str(run.get("headBranch") or "") == branch
    ]
    latest_run = max(
        exact_runs,
        key=lambda run: str(run.get("updatedAt") or run.get("createdAt") or ""),
        default=None,
    )
    status = "NOT_OBSERVED"
    if latest_run:
        run_status = str(latest_run.get("status") or "").casefold()
        conclusion = str(latest_run.get("conclusion") or "").casefold()
        if run_status != "completed":
            status = "IN_PROGRESS"
        elif conclusion == "success":
            status = "SUCCESS"
        elif conclusion == "skipped":
            status = "SKIPPED"
        else:
            status = "NON_SUCCESSFUL"

    latest_evidence = None
    if latest_run:
        latest_evidence = {
            "workflow_run_id": latest_run.get("databaseId"),
            "workflow_name": latest_run.get("workflowName") or latest_run.get("name"),
            "head_sha": latest_run.get("headSha"),
            "head_branch": latest_run.get("headBranch"),
            "status": latest_run.get("status"),
            "conclusion": latest_run.get("conclusion"),
            "updated_at": latest_run.get("updatedAt") or latest_run.get("createdAt"),
            "url": latest_run.get("url"),
        }
    return {
        "status": status,
        "verification_level": "same_response_exact_sha_workflow_metadata_only",
        "remote_sha": remote_sha,
        "branch": branch,
        "workflow_names": codeql_workflows,
        "exact_sha_run_count": len(exact_runs),
        "latest_exact_sha_run": latest_evidence,
        "analysis_triggered_by_verifier": False,
    }


def build_completion_status(
    repo: str,
    local_head: str,
    remote_main_sha: str | None,
    auth_verified: bool,
    branch_protection_status: str,
    workflows: list[dict[str, Any]] | None = None,
    workflow_runs: list[dict[str, Any]] | None = None,
    remote_tree_sha: str | None = None,
    default_branch: str = "main",
    repository_identity_verified: bool = False,
) -> dict[str, Any]:
    workflows = workflows or []
    workflow_runs = workflow_runs or []
    remote_matches_local = bool(remote_main_sha and remote_main_sha == local_head)
    matching_workflow_runs = [
        run for run in workflow_runs
        if isinstance(run, dict)
        and "codeql" not in str(run.get("workflowName") or run.get("name") or "").casefold()
        and str(run.get("headSha") or "") == str(remote_main_sha or "")
        and str(run.get("headBranch") or "") == default_branch
        and str(run.get("status") or "").lower() == "completed"
        and str(run.get("conclusion") or "").lower() == "success"
        and isinstance(run.get("databaseId"), int)
        and not isinstance(run.get("databaseId"), bool)
        and run["databaseId"] > 0
    ]
    exact_sha_successful_workflow = bool(matching_workflow_runs and repository_identity_verified)
    blockers: list[str] = []
    next_actions: list[str] = []

    if not auth_verified:
        blockers.append("GitHub authentication is not verified; a live remote completion claim requires an authenticated terminal identity.")
        next_actions.append("Authenticate the target GitHub identity and verify the terminal session before any remote completion claim.")

    if not repository_identity_verified:
        blockers.append("The authenticated GitHub repository identity does not independently match the requested owner/repository.")
        next_actions.append("Verify the exact owner/repository identity before accepting refs or workflow evidence.")

    if not remote_main_sha:
        blockers.append("The remote main SHA is unavailable; exact remote completion proof is missing.")
        next_actions.append("Query the live GitHub main SHA with the authenticated CLI and confirm the exact remote ref before continuing.")
    elif not re.fullmatch(r"[0-9a-f]{40}", str(remote_main_sha)):
        blockers.append("The remote ref response is not a valid full commit SHA.")
        next_actions.append("Re-read the exact target ref and validate its complete commit SHA.")
    elif not remote_matches_local:
        blockers.append("remote main SHA does not match the local HEAD; local validation does not equal remote completion.")
        next_actions.append("Verify the exact remote SHA from a target-owned workflow and ensure the local checkout is aligned before claiming completion.")

    if not re.fullmatch(r"[0-9a-f]{40}", str(remote_tree_sha or "")):
        blockers.append("The exact remote commit tree SHA was not independently read back.")
        next_actions.append("Read the remote commit's tree SHA and bind it to the terminal workflow and final ref evidence.")

    if not re.fullmatch(r"[0-9a-f]{40}", str(local_head)):
        blockers.append("The local HEAD is not a valid full commit SHA.")
        next_actions.append("Read the local checkout's full HEAD SHA before comparing it with the remote ref.")

    if branch_protection_status != "verified":
        blockers.append("Branch protection and protected-write authority are not verified; mutation safety remains unproven.")
        next_actions.append("Check the branch protection rules and confirm write authority through an authorized GitHub-side workflow before any push or merge.")

    if not workflows:
        blockers.append("No workflow inventory was observed from the live GitHub repo; workflow evidence is incomplete.")
        next_actions.append("List the active target-owned workflows and confirm the exact run and job evidence for the remote SHA.")

    if remote_main_sha and not exact_sha_successful_workflow:
        blockers.append("No successful target-owned workflow was recorded for the exact remote SHA; remote completion requires workflow proof on that exact commit.")
        next_actions.append("Trigger or confirm a target-owned workflow for the exact remote SHA and verify a successful conclusion before claiming completion.")

    completion_status = "READY" if not blockers else "BLOCKED"
    return {
        "repo": repo,
        "remote_ref": f"refs/heads/{default_branch}",
        "local_head": local_head,
        "remote_main_sha": remote_main_sha,
        "remote_tree_sha": remote_tree_sha,
        "remote_matches_local": remote_matches_local,
        "auth_verified": auth_verified,
        "branch_protection_status": branch_protection_status,
        "workflows": workflows,
        "workflow_runs": workflow_runs,
        "codeql_evidence": summarize_codeql_evidence(
            workflows,
            workflow_runs,
            remote_main_sha,
            default_branch,
        ),
        "exact_sha_successful_workflow": exact_sha_successful_workflow,
        "exact_sha_workflow_runs": [
            {
                "workflow_run_id": run["databaseId"],
                "workflow_name": run.get("workflowName") or run.get("name"),
                "head_sha": run.get("headSha"),
                "head_branch": run.get("headBranch"),
                "tree_sha": remote_tree_sha,
                "status": run.get("status"),
                "conclusion": run.get("conclusion"),
                "url": run.get("url"),
            }
            for run in matching_workflow_runs
        ] if repository_identity_verified else [],
        "repository_identity_verified": repository_identity_verified,
        "completion_status": completion_status,
        "blockers": blockers,
        "next_actions": next_actions,
        "checked_at": utc_now(),
    }


def verify_live_github_state(repo: str, local_head: str, default_branch: str = "main") -> dict[str, Any]:
    repo_meta = parse_repo_view(repo)
    auth = parse_auth_status()
    workflows = parse_workflows(repo)
    remote_main_sha = parse_remote_main_sha(repo, default_branch)
    remote_tree_sha = parse_remote_tree_sha(repo, remote_main_sha)
    workflow_runs = parse_workflow_runs(repo, remote_main_sha, branch=default_branch)
    branch_protection_status = parse_branch_protection(repo, default_branch)
    result = build_completion_status(
        repo=repo,
        local_head=local_head,
        remote_main_sha=remote_main_sha,
        auth_verified=bool(auth.get("verified")),
        branch_protection_status=branch_protection_status,
        workflows=workflows,
        workflow_runs=workflow_runs,
        remote_tree_sha=remote_tree_sha,
        default_branch=default_branch,
        repository_identity_verified=(
            repo_meta.get("status") == "verified"
            and str(repo_meta.get("repo", "")).casefold() == repo.casefold()
        ),
    )
    result["repo_metadata"] = repo_meta
    result["auth_status"] = auth
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the live GitHub state against the local checkout for the remote-first completion gate.")
    parser.add_argument("--repo", default="thealphakenya/Alpha-Q-ai")
    parser.add_argument("--local-head", default=os.environ.get("LOCAL_HEAD") or "")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--write-json", default="")
    args = parser.parse_args()

    if not args.local_head:
        try:
            args.local_head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Failed to read local HEAD: {exc}", file=sys.stderr)
            return 2

    result = verify_live_github_state(args.repo, args.local_head, args.branch)
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.write_json:
        try:
            with open(args.write_json, "w", encoding="utf-8") as handle:
                json.dump(result, handle, indent=2, sort_keys=True)
                handle.write("\n")
        except OSError as exc:
            print(f"Failed to write JSON report: {exc}", file=sys.stderr)
            return 2
    return 0 if result["completion_status"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
