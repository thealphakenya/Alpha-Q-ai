#!/usr/bin/env python3
"""Audit and synchronize the Alpha-Q-ai and qmoi-enhanced repositories.

The default operation is read-only. Apply mode updates the target autosync branch
first and only promotes to main when --promote is explicitly supplied. The
script never force-pushes and treats qmoi-enhanced as the policy/master source
for the default direction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
import uuid

QMOI_NAME = "qmoi-enhanced"
ALPHA_NAME = "Alpha-Q-ai"
DEFAULT_BACKUP_BRANCH = "autosync-backup"
DEFAULT_MASTER_BRANCH = "master"


def run_git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
    )
    if not check and result.returncode != 0:
        return ""
    if check:
        return result.stdout.strip()
    return result.stdout.strip()


def branch_sha(repo: Path, branch: str) -> str | None:
    value = run_git(repo, "rev-parse", f"refs/remotes/origin/{branch}", check=False)
    return value or None


def repo_metrics(repo: Path, branch: str) -> dict[str, Any]:
    sha = run_git(repo, "rev-parse", f"origin/{branch}", check=False) or None
    files = run_git(repo, "ls-tree", "-r", "--name-only", f"origin/{branch}", check=False)
    paths = [line for line in files.splitlines() if line]
    directories = {str(Path(path).parent) for path in paths if Path(path).parent != Path(".")}
    return {"branch": branch, "sha": sha, "files": len(paths), "directories": len(directories)}


def commit_exists(repo: Path, sha: str) -> bool:
    if not sha:
        return False
    result = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{sha}^{{commit}}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def cross_repo_ancestry(
    source_repo: Path,
    source_branch: str,
    target_repo: Path,
    target_branch: str,
) -> dict[str, Any]:
    source = branch_sha(source_repo, source_branch)
    target = branch_sha(target_repo, target_branch)
    if not source or not target:
        return {"source": source, "target": target, "ahead": None, "behind": None, "same_commit": False, "fast_forward_possible": False}
    if source == target:
        return {
            "source": source,
            "target": target,
            "ahead": 0,
            "behind": 0,
            "same_commit": True,
            "source_object_available_in_target": True,
            "target_object_available_in_source": True,
            "fast_forward_possible": True,
        }
    target_in_source = commit_exists(source_repo, target)
    source_in_target = commit_exists(target_repo, source)
    is_ancestor = target_in_source and subprocess.run(
        ["git", "-C", str(source_repo), "merge-base", "--is-ancestor", target, source],
        check=False,
    ).returncode == 0
    return {
        "source": source,
        "target": target,
        "ahead": None,
        "behind": None,
        "same_commit": False,
        "source_object_available_in_target": source_in_target,
        "target_object_available_in_source": target_in_source,
        "fast_forward_possible": source_in_target and is_ancestor,
    }


def audit(qmoi: Path, alpha: Path, backup_branch: str) -> dict[str, Any]:
    for repo in (qmoi, alpha):
        run_git(repo, "fetch", "origin", "--prune")
    return {
        "captured_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "master": QMOI_NAME,
        "repositories": {
            QMOI_NAME: {
                "root": str(qmoi),
                "main": repo_metrics(qmoi, "main"),
                "backup": repo_metrics(qmoi, backup_branch),
                "master": repo_metrics(qmoi, DEFAULT_MASTER_BRANCH),
            },
            ALPHA_NAME: {
                "root": str(alpha),
                "main": repo_metrics(alpha, "main"),
                "backup": repo_metrics(alpha, backup_branch),
                "master": repo_metrics(alpha, DEFAULT_MASTER_BRANCH),
            },
        },
        "directions": {
            "qmoi-to-alpha": cross_repo_ancestry(qmoi, "main", alpha, "main"),
            "alpha-to-qmoi": cross_repo_ancestry(alpha, "main", qmoi, "main"),
        },
        "master_branch_plan": {
            "purpose": "Fast-forward-only mirror of each validated main tip for a stable cross-repository recovery and parity reference.",
            "authority": "main remains the default development branch; qmoi-enhanced remains the policy/master repository.",
            "update_policy": "Update master from main after backup and main promotion; never accept independent or non-fast-forward master commits.",
            "required_parity": "Both repositories' master refs must equal the candidate main SHA and tracked tree before Q-version finalization.",
        },
    }


def preflight_fast_forward(
    target: Path,
    source: Path,
    target_branch: str,
    source_branch: str,
) -> dict[str, Any]:
    source_sha = run_git(source, "rev-parse", f"origin/{source_branch}")
    target_ref = f"refs/remotes/origin/{target_branch}"
    target_sha = run_git(target, "rev-parse", target_ref, check=False)
    if not commit_exists(target, source_sha):
        raise RuntimeError(
            f"Refusing cross-repository update: source commit {source_sha} is not available in target checkout"
        )
    if target_sha and target_sha != source_sha:
        target_in_source = commit_exists(source, target_sha)
        is_ancestor = target_in_source and subprocess.run(
            ["git", "-C", str(source), "merge-base", "--is-ancestor", target_sha, source_sha],
            check=False,
        ).returncode == 0
        if not is_ancestor:
            raise RuntimeError(f"Refusing non-fast-forward update of {target_branch}: review conflict first")
    return {
        "source_branch": source_branch,
        "source_sha": source_sha,
        "target_branch": target_branch,
        "target_sha": target_sha or None,
        "status": "unchanged" if target_sha == source_sha else "ready",
    }


def push_fast_forward(target: Path, source: Path, target_branch: str, source_branch: str) -> None:
    plan = preflight_fast_forward(target, source, target_branch, source_branch)
    if plan["status"] == "unchanged":
        return
    source_sha = plan["source_sha"]
    run_git(target, "push", "origin", f"{source_sha}:refs/heads/{target_branch}")


def _remote_branch_shas(repo: Path, branches: list[str]) -> dict[str, str]:
    refs = [f"refs/heads/{branch}" for branch in branches]
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-remote", "--heads", "origin", *refs],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Unable to inspect origin branch refs for {repo} (exit {result.returncode})")
    found = {}
    for line in result.stdout.splitlines():
        sha, ref = line.split("\t", 1)
        found[ref.removeprefix("refs/heads/")] = sha
    return found


def evaluate_qmoi_restore_preflight(
    *,
    current_main: str,
    current_backup: str,
    current_qmoi: str,
    current_master: str,
    peer_main: str,
    peer_backup: str,
    peer_qmoi: str,
    peer_master: str,
    checkout_sha: str,
    tree_sha: str,
    required_docs_present: bool,
    bootstrap_authorized: bool,
) -> dict[str, Any]:
    """Classify a verified restore point or a narrowly authorized first-run baseline."""
    if not all((current_main, current_backup, peer_main, peer_backup, checkout_sha, tree_sha)):
        return {"status": "BLOCKED", "blocker": "Both repositories must expose readable main and autosync-backup refs and the checkout tree."}
    if not required_docs_present:
        return {"status": "BLOCKED", "blocker": "The synchronized baseline is missing oe2.txt or remotecompletion.md."}

    refs = (current_main, current_backup, current_qmoi, current_master, peer_main, peer_backup, peer_qmoi, peer_master)
    if all(ref == checkout_sha for ref in refs):
        return {"status": "PASS", "blocker": None, "bootstrap_allowed": False}

    if not current_qmoi and not peer_qmoi and not current_master and not peer_master:
        baseline_refs = (current_main, current_backup, peer_main, peer_backup)
        if all(ref == checkout_sha for ref in baseline_refs):
            if bootstrap_authorized:
                return {
                    "status": "BOOTSTRAP_READY",
                    "blocker": "No qmoi restore point exists yet; aligned main/backup refs permit the first authorized agent cycle.",
                    "bootstrap_allowed": True,
                }
            return {
                "status": "BLOCKED_REQUIRES_AUTHORIZATION",
                "blocker": "Initial restore-point bootstrap requires QMOI_BRANCH_PUBLICATION_AUTHORIZED=true.",
                "bootstrap_allowed": False,
            }

    if not current_master and not peer_master and current_qmoi == checkout_sha and peer_qmoi == checkout_sha:
        baseline_refs = (current_main, current_backup, peer_main, peer_backup, current_qmoi, peer_qmoi)
        if all(ref == checkout_sha for ref in baseline_refs):
            if bootstrap_authorized:
                return {
                    "status": "MASTER_BOOTSTRAP_READY",
                    "blocker": "The qmoi restore point is aligned, but master is absent in both repositories; authorized master initialization is required.",
                    "bootstrap_allowed": True,
                }
            return {
                "status": "BLOCKED_REQUIRES_AUTHORIZATION",
                "blocker": "Initial master-branch publication requires QMOI_BRANCH_PUBLICATION_AUTHORIZED=true.",
                "bootstrap_allowed": False,
            }

    return {
        "status": "BLOCKED",
        "blocker": "Both repositories must have main, autosync-backup, qmoi, and master at one identical exact SHA, or both restore refs must be absent for an authorized first-run bootstrap.",
        "bootstrap_allowed": False,
    }


def _agent_success_blocker(evidence: Mapping[str, Any] | None) -> str | None:
    if not isinstance(evidence, Mapping):
        return "A verified successful Ollama agent workflow run is required before qmoi publication."
    if evidence.get("verified") is not True or evidence.get("conclusion") != "success":
        return "The Ollama agent workflow has no verified terminal success evidence."
    if not str(evidence.get("workflow_run_id", "")).strip():
        return "The successful Ollama agent workflow run ID is missing."
    source_sha = evidence.get("source_sha")
    if not isinstance(source_sha, str) or len(source_sha) != 40 or any(char not in "0123456789abcdef" for char in source_sha):
        return "The successful Ollama agent workflow must be bound to an exact source SHA."
    return None


def preflight_qmoi_branch(
    repositories: list[Path],
    workspace_sha: str,
    *,
    agent_success_evidence: Mapping[str, Any],
    backup_branch: str = DEFAULT_BACKUP_BRANCH,
) -> dict[str, Any]:
    """Verify both clean checkouts and remotes agree before creating `qmoi`."""
    roots = list(dict.fromkeys(Path(repo).resolve() for repo in repositories))
    if len(roots) != 2:
        raise RuntimeError("QMOI branch publication requires exactly two distinct repositories")
    if not isinstance(workspace_sha, str) or len(workspace_sha) != 40 or any(char not in "0123456789abcdef" for char in workspace_sha):
        raise RuntimeError("QMOI branch publication requires an exact lowercase commit SHA")
    if not backup_branch or backup_branch in {"main", "qmoi", DEFAULT_MASTER_BRANCH}:
        raise RuntimeError("QMOI branch publication requires a distinct backup branch name")
    blocker = _agent_success_blocker(agent_success_evidence)
    if blocker:
        raise RuntimeError(blocker)

    repository_plans = {}
    shared_tree = None
    shared_required_docs: dict[str, str] | None = None
    for root in roots:
        status = run_git(root, "status", "--porcelain", "--untracked-files=all", check=False)
        if status:
            raise RuntimeError(f"Refusing QMOI branch creation from a dirty checkout: {root}")
        if not commit_exists(root, workspace_sha):
            raise RuntimeError(f"Workspace SHA is unavailable in repository object database: {root}")

        required_doc_hashes = {}
        for required_path in ("oe2.txt", "remotecompletion.md"):
            result = subprocess.run(
                ["git", "-C", str(root), "show", f"{workspace_sha}:{required_path}"],
                check=False,
                capture_output=True,
            )
            if result.returncode != 0:
                raise RuntimeError(f"Required completion evidence file is missing at workspace SHA: {required_path}")
            required_doc_hashes[required_path] = hashlib.sha256(result.stdout).hexdigest()
        if shared_required_docs is not None and required_doc_hashes != shared_required_docs:
            raise RuntimeError("Completion evidence files differ between repository trees")
        shared_required_docs = required_doc_hashes

        tree_sha = run_git(root, "rev-parse", f"{workspace_sha}^{{tree}}")
        if shared_tree is not None and tree_sha != shared_tree:
            raise RuntimeError("The two repositories do not contain the same tracked workspace tree")
        shared_tree = tree_sha

        remote = _remote_branch_shas(root, ["main", backup_branch, "qmoi", DEFAULT_MASTER_BRANCH])
        if any(remote.get(branch) != workspace_sha for branch in ("main", backup_branch, DEFAULT_MASTER_BRANCH)):
            raise RuntimeError(f"Remote main, {backup_branch}, and master must all equal the workspace SHA for {root}")
        if not commit_exists(root, str(agent_success_evidence["source_sha"])):
            raise RuntimeError(f"Successful agent source SHA is unavailable in repository: {root}")
        if subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", str(agent_success_evidence["source_sha"]), workspace_sha],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode != 0:
            raise RuntimeError(f"Successful agent source SHA is not an ancestor of the restore-point SHA for {root}")
        existing_qmoi_sha = remote.get("qmoi")
        if existing_qmoi_sha and existing_qmoi_sha != workspace_sha:
            fetch = subprocess.run(
                ["git", "-C", str(root), "fetch", "--no-tags", "origin", "refs/heads/qmoi"],
                check=False,
                capture_output=True,
                text=True,
            )
            is_fast_forward = (
                fetch.returncode == 0
                and commit_exists(root, existing_qmoi_sha)
                and subprocess.run(
                    ["git", "-C", str(root), "merge-base", "--is-ancestor", existing_qmoi_sha, workspace_sha],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                ).returncode == 0
            )
            if not is_fast_forward:
                raise RuntimeError(f"Refusing to replace a non-fast-forward existing qmoi branch in {root}")
        repository_plans[str(root)] = {
            "workspace_sha": workspace_sha,
            "tree_sha": tree_sha,
            "branch_tree_sha": tree_sha,
            "main_sha": remote["main"],
            "backup_sha": remote[backup_branch],
            "master_sha": remote[DEFAULT_MASTER_BRANCH],
            "qmoi_sha": existing_qmoi_sha,
            "required_doc_sha256": required_doc_hashes,
            "agent_success_run_id": str(agent_success_evidence["workflow_run_id"]),
            "agent_success_source_sha": str(agent_success_evidence["source_sha"]),
            "action": "already_current" if existing_qmoi_sha == workspace_sha else "fast_forward" if existing_qmoi_sha else "create",
            "required_docs_present": True,
        }

    return {
        "status": "READY",
        "workspace_sha": workspace_sha,
        "tree_sha": shared_tree,
        "master_verified": True,
        "required_doc_sha256": shared_required_docs,
        "agent_success_evidence": {
            "workflow_run_id": str(agent_success_evidence["workflow_run_id"]),
            "source_sha": str(agent_success_evidence["source_sha"]),
            "source_repository": agent_success_evidence.get("source_repository"),
            "conclusion": "success",
        },
        "repositories": repository_plans,
    }


def publish_qmoi_branch(
    repositories: list[Path],
    workspace_sha: str,
    *,
    authorized: bool = False,
    agent_success_evidence: Mapping[str, Any] | None = None,
    backup_branch: str = DEFAULT_BACKUP_BRANCH,
) -> dict[str, Any]:
    """Create (never force-update) `qmoi` after dual-repository synchronization."""
    metadata = {
        "correlation_id": str(uuid.uuid4()),
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "workflow_run_id": os.getenv("GITHUB_RUN_ID"),
        "workflow_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
        "workflow_repository": os.getenv("GITHUB_REPOSITORY"),
        "workflow_sha": os.getenv("GITHUB_SHA"),
        "publication_authorized": authorized is True,
        "authorization_gate": "QMOI_BRANCH_PUBLICATION_AUTHORIZED",
    }
    try:
        plan = preflight_qmoi_branch(
            repositories,
            workspace_sha,
            agent_success_evidence=agent_success_evidence or {},
            backup_branch=backup_branch,
        )
    except RuntimeError as exc:
        return {**metadata, "status": "BLOCKED", "workspace_sha": workspace_sha, "blocker": str(exc), "repositories": {}}
    if not authorized:
        return {
            **metadata,
            **plan,
            "status": "BLOCKED_REQUIRES_AUTHORIZATION",
            "blocker": "Set the target-owned QMOI branch publication authorization gate after policy review.",
            "published_repositories": [],
        }

    published_repositories = []
    verified_repositories = []
    for root_string, item in plan["repositories"].items():
        pre_publish_refs = _remote_branch_shas(Path(root_string), ["main", backup_branch, "qmoi", DEFAULT_MASTER_BRANCH])
        if any(pre_publish_refs.get(branch) != workspace_sha for branch in ("main", backup_branch, DEFAULT_MASTER_BRANCH)) or pre_publish_refs.get("qmoi") != item["qmoi_sha"]:
            return {
                **metadata,
                **plan,
                "status": "BLOCKED_PARTIAL" if published_repositories else "BLOCKED",
                "blocker": f"Remote main, backup, or qmoi ref drifted after preflight for {root_string}.",
                "failed_repository": root_string,
                "published_repositories": published_repositories,
                "verified_repositories": verified_repositories,
            }
        if item["action"] != "already_current":
            result = subprocess.run(
                ["git", "-C", root_string, "push", "origin", f"{workspace_sha}:refs/heads/qmoi"],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                return {
                    **metadata,
                    **plan,
                    "status": "BLOCKED_PARTIAL" if published_repositories else "BLOCKED",
                    "blocker": "Remote qmoi ref publication failed; no force update was attempted.",
                    "failed_repository": root_string,
                    "push_exit_code": result.returncode,
                    "published_repositories": published_repositories,
                    "verified_repositories": verified_repositories,
                }
            published_repositories.append(root_string)
        try:
            final_refs = _remote_branch_shas(Path(root_string), ["main", backup_branch, "qmoi", DEFAULT_MASTER_BRANCH])
        except RuntimeError as exc:
            return {
                **metadata,
                **plan,
                "status": "BLOCKED_PARTIAL",
                "blocker": str(exc),
                "published_repositories": published_repositories,
                "verified_repositories": verified_repositories,
            }
        if any(final_refs.get(branch) != workspace_sha for branch in ("main", backup_branch, "qmoi", DEFAULT_MASTER_BRANCH)):
            return {
                **metadata,
                **plan,
                "status": "BLOCKED_PARTIAL",
                "blocker": f"Remote main, backup, and qmoi refs did not all verify at the requested SHA for {root_string}",
                "failed_repository": root_string,
                "observed_refs": final_refs,
                "published_repositories": published_repositories,
                "verified_repositories": verified_repositories,
            }
        item["qmoi_sha"] = final_refs["qmoi"]
        item["remote_verification"] = {
            "main_sha": final_refs["main"],
            "backup_sha": final_refs[backup_branch],
            "qmoi_sha": final_refs["qmoi"],
            "master_sha": final_refs[DEFAULT_MASTER_BRANCH],
            "tree_sha": item["tree_sha"],
            "verified": True,
        }
        verified_repositories.append(root_string)
        if item["action"] == "create":
            item["action"] = "created"
        elif item["action"] == "fast_forward":
            item["action"] = "fast_forwarded"

    return {
        **metadata,
        **plan,
        "status": "SUCCESS",
        "master_verified": len(verified_repositories) == len(plan["repositories"]),
        "verified_branches": ["main", backup_branch, "qmoi", DEFAULT_MASTER_BRANCH],
        "published_repositories": published_repositories,
        "verified_repositories": verified_repositories,
        "verification": "both repositories' main, backup, qmoi, and master refs equal the workspace SHA and tree",
    }


def write_report(path: Path | None, report: dict[str, Any]) -> None:
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qmoi", type=Path, required=True, help="Local qmoi-enhanced checkout")
    parser.add_argument("--alpha", type=Path, required=True, help="Local Alpha-Q-ai checkout")
    parser.add_argument("--direction", choices=("audit", "qmoi-to-alpha", "alpha-to-qmoi"), default="audit")
    parser.add_argument("--backup-branch", default=DEFAULT_BACKUP_BRANCH)
    parser.add_argument("--apply", action="store_true", help="Push the source main commit to the target backup branch")
    parser.add_argument("--promote", action="store_true", help="After backup sync, also promote to target main")
    parser.add_argument("--report", type=Path, help="Write the audit JSON report")
    args = parser.parse_args()

    qmoi = args.qmoi.resolve()
    alpha = args.alpha.resolve()
    report = audit(qmoi, alpha, args.backup_branch)
    report["requested_direction"] = args.direction
    report["apply"] = args.apply
    report["promote"] = args.promote

    if args.apply and args.direction == "audit":
        parser.error("--apply requires --direction qmoi-to-alpha or alpha-to-qmoi")
    if args.promote and not args.apply:
        parser.error("--promote requires --apply")

    if args.apply:
        source, target = (qmoi, alpha) if args.direction == "qmoi-to-alpha" else (alpha, qmoi)
        branches = [args.backup_branch, "main", DEFAULT_MASTER_BRANCH] if args.promote else [args.backup_branch]
        try:
            preflight = [
                preflight_fast_forward(target, source, branch, "main")
                for branch in branches
            ]
        except RuntimeError as exc:
            report["status"] = "blocked"
            report["apply_preflight"] = {"status": "blocked", "error": str(exc)}
            report["applied"] = False
            payload = json.dumps(report, indent=2, sort_keys=True)
            write_report(args.report, report)
            print(payload)
            return 2

        report["apply_preflight"] = {"status": "ready", "branches": preflight}
        applied_branches = []
        for branch in branches:
            try:
                push_fast_forward(target, source, branch, "main")
                applied_branches.append(branch)
            except subprocess.CalledProcessError as exc:
                report["status"] = "blocked"
                report["applied"] = {
                    "source": str(source),
                    "target": str(target),
                    "completed_branches": applied_branches,
                    "failed_branch": branch,
                    "promoted": False,
                }
                report["apply_error"] = {
                    "type": "push_failed",
                    "returncode": exc.returncode,
                }
                payload = json.dumps(report, indent=2, sort_keys=True)
                write_report(args.report, report)
                print(payload)
                return 2
        report["applied"] = {
            "source": str(source),
            "target": str(target),
            "completed_branches": applied_branches,
            "backup_branch": args.backup_branch,
            "promoted": args.promote,
        }

        if args.promote:
            try:
                for repo in (qmoi, alpha):
                    run_git(repo, "fetch", "origin", "--prune")
                    push_fast_forward(repo, repo, args.backup_branch, "main")
                    push_fast_forward(repo, repo, "master", "main")
                    run_git(repo, "fetch", "origin", "--prune")
                workspace_sha = branch_sha(source, "main")
                authorization = os.environ.get("QMOI_BRANCH_PUBLICATION_AUTHORIZED", "").strip().lower() in {"1", "true", "yes"}
                agent_success_evidence = {
                    "verified": os.environ.get("QMOI_AGENT_SUCCESS_VERIFIED", "").strip().lower() == "true",
                    "conclusion": os.environ.get("QMOI_AGENT_SUCCESS_CONCLUSION", ""),
                    "workflow_run_id": os.environ.get("QMOI_AGENT_SUCCESS_RUN_ID", ""),
                    "source_sha": os.environ.get("QMOI_AGENT_SUCCESS_SOURCE_SHA", ""),
                    "source_repository": os.environ.get("QMOI_AGENT_SUCCESS_REPOSITORY", ""),
                }
                if agent_success_evidence["verified"] is not True:
                    report["qmoi_restore_point"] = {
                        "status": "SKIPPED_NO_VERIFIED_AGENT_SUCCESS",
                        "blocker": "Main/backup synchronization completed, but no terminal successful Ollama agent run was verified; qmoi publication was not attempted.",
                        "publication_authorized": authorization,
                        "published_repositories": [],
                    }
                    report["status"] = "success_restore_point_deferred"
                    report["next_action"] = "Wait for terminal agent success with passing final validation and link checks; then rerun the target-owned autosync workflow."
                    write_report(args.report, report)
                    print(json.dumps(report, indent=2, sort_keys=True))
                    return 0
                restore_point = publish_qmoi_branch(
                    [qmoi, alpha],
                    workspace_sha or "",
                    authorized=authorization,
                    agent_success_evidence=agent_success_evidence,
                    backup_branch=args.backup_branch,
                )
            except (RuntimeError, subprocess.CalledProcessError) as exc:
                restore_point = {
                    "status": "BLOCKED",
                    "blocker": str(exc),
                    "workspace_sha": None,
                    "repositories": {},
                }
            report["qmoi_restore_point"] = restore_point
            if restore_point.get("status") != "SUCCESS":
                report["status"] = restore_point.get("status", "BLOCKED")
                report["next_action"] = "Resolve QMOI branch authorization or synchronization blocker; rerun only through an authorized target-owned workflow."
                write_report(args.report, report)
                print(json.dumps(report, indent=2, sort_keys=True))
                return 2
            report["qmoi_restore_point"]["workflow_run_id"] = os.getenv("GITHUB_RUN_ID")
            report["qmoi_restore_point"]["verification_level"] = "remote_refs_verified; workflow_terminal_result_pending"
            report["status"] = "success"

    payload = json.dumps(report, indent=2, sort_keys=True)
    write_report(args.report, report)
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
