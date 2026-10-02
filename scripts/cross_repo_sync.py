#!/usr/bin/env python3
"""Audit and synchronize the Alpha-Q-ai and qmoi-enhanced repositories.

The default operation is read-only. Apply mode updates the target autosync branch
first and only promotes to main when --promote is explicitly supplied. The
script never force-pushes and treats qmoi-enhanced as the policy/master source
for the default direction.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

QMOI_NAME = "qmoi-enhanced"
ALPHA_NAME = "Alpha-Q-ai"
DEFAULT_BACKUP_BRANCH = "autosync-backup"
MANAGED_BRANCH_TYPES = {"feature", "fix", "hotfix", "security", "chore", "docs", "experiment"}
MANAGED_BRANCH_PATTERN = re.compile(
    r"^(?:feature|fix|hotfix|security|chore|docs|experiment)/[a-z0-9]+-[a-z0-9]+(?:-[a-z0-9]+)*$"
)
RELEASE_BRANCH_PATTERN = re.compile(r"^release/v[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.]+)?$")
DEPENDABOT_BRANCH_PATTERN = re.compile(
    r"^dependabot/(?:github_actions|npm_and_yarn|pip)/[a-z0-9][a-z0-9._/-]*$",
    re.IGNORECASE,
)
ALL_REMOTE_HEADS_REFSPEC = "+refs/heads/*:refs/remotes/origin/*"


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


def classify_branch_name(name: str) -> dict[str, Any]:
    """Describe a branch's role and safe automatic merge policy."""
    if name == "main":
        return {"role": "production", "naming_status": "reserved", "merge_policy": "protected_review_and_checks"}
    if name == DEFAULT_BACKUP_BRANCH:
        return {"role": "protected_backup", "naming_status": "reserved", "merge_policy": "fast_forward_before_main"}
    if DEPENDABOT_BRANCH_PATTERN.fullmatch(name):
        return {"role": "dependency_update", "naming_status": "provider_managed", "merge_policy": "pull_request_and_security_checks"}
    if name.startswith("codespace-"):
        return {"role": "ephemeral_codespace", "naming_status": "provider_managed", "merge_policy": "never_cross_repo_sync"}
    if RELEASE_BRANCH_PATTERN.fullmatch(name):
        return {"role": "release", "naming_status": "valid", "merge_policy": "pull_request_and_release_gates"}
    if MANAGED_BRANCH_PATTERN.fullmatch(name):
        return {
            "role": name.split("/", 1)[0],
            "naming_status": "valid",
            "merge_policy": "pull_request_and_required_checks",
        }
    return {"role": "legacy_or_unclassified", "naming_status": "legacy_review", "merge_policy": "review_only"}


def validate_new_branch_name(name: str) -> bool:
    """Accept documented human work/release names, not reserved or provider branches."""
    return bool(MANAGED_BRANCH_PATTERN.fullmatch(name) or RELEASE_BRANCH_PATTERN.fullmatch(name))


def remote_branch_inventory(repo: Path) -> list[dict[str, Any]]:
    """Inventory every branch fetched from origin, without promoting any branch."""
    refs = run_git(
        repo,
        "for-each-ref",
        "--format=%(refname:strip=3)%09%(objectname)",
        "refs/remotes/origin",
    )
    inventory = []
    for line in refs.splitlines():
        name, separator, commit_sha = line.partition("\t")
        if not separator or not name or name == "HEAD":
            continue
        tree_sha = run_git(repo, "rev-parse", f"{commit_sha}^{{tree}}", check=False) or None
        inventory.append(
            {
                "name": name,
                "commit_sha": commit_sha,
                "tree_sha": tree_sha,
                "automatic_publication_allowed": name in {"main", DEFAULT_BACKUP_BRANCH},
                **classify_branch_name(name),
            }
        )
    return sorted(inventory, key=lambda branch: branch["name"])


def fetch_all_remote_branches(repo: Path) -> None:
    """Refresh every branch visible from origin, independent of clone refspecs."""
    run_git(repo, "fetch", "--prune", "origin", ALL_REMOTE_HEADS_REFSPEC)


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


def compare_branch_inventories(
    qmoi: Path,
    alpha: Path,
    qmoi_branches: list[dict[str, Any]],
    alpha_branches: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compare same-name remote branches while leaving feature merges review-only."""
    qmoi_by_name = {branch["name"]: branch for branch in qmoi_branches}
    alpha_by_name = {branch["name"]: branch for branch in alpha_branches}
    comparisons = []
    for name in sorted(qmoi_by_name.keys() | alpha_by_name.keys()):
        qmoi_branch = qmoi_by_name.get(name)
        alpha_branch = alpha_by_name.get(name)
        policy = classify_branch_name(name)
        if qmoi_branch and alpha_branch:
            qmoi_to_alpha = cross_repo_ancestry(qmoi, name, alpha, name)
            alpha_to_qmoi = cross_repo_ancestry(alpha, name, qmoi, name)
            if qmoi_branch["commit_sha"] == alpha_branch["commit_sha"]:
                status = "identical_tip"
            elif qmoi_to_alpha["fast_forward_possible"]:
                status = "qmoi_fast_forward_candidate"
            elif alpha_to_qmoi["fast_forward_possible"]:
                status = "alpha_fast_forward_candidate"
            else:
                status = "diverged_or_objects_unavailable"
            comparisons.append(
                {
                    "name": name,
                    "status": status,
                    "qmoi_sha": qmoi_branch["commit_sha"],
                    "alpha_sha": alpha_branch["commit_sha"],
                    "qmoi_to_alpha": qmoi_to_alpha,
                    "alpha_to_qmoi": alpha_to_qmoi,
                    "automatic_publication_allowed": name in {"main", DEFAULT_BACKUP_BRANCH},
                    "merge_policy": policy["merge_policy"],
                }
            )
        else:
            source = "qmoi" if qmoi_branch else "alpha"
            branch = qmoi_branch or alpha_branch
            comparisons.append(
                {
                    "name": name,
                    "status": f"only_in_{source}",
                    "qmoi_sha": qmoi_branch["commit_sha"] if qmoi_branch else None,
                    "alpha_sha": alpha_branch["commit_sha"] if alpha_branch else None,
                    "automatic_publication_allowed": False,
                    "merge_policy": policy["merge_policy"],
                    "review_required": True,
                    "source_role": branch["role"],
                }
            )
    return {
        "branch_name_policy": {
            "protected": ["main", DEFAULT_BACKUP_BRANCH],
            "managed_types": sorted(MANAGED_BRANCH_TYPES),
            "managed_name_format": "<type>/<issue-id>-<lowercase-kebab-slug>",
            "release_name_format": "release/v<major>.<minor>.<patch>[-<label>]",
            "provider_managed": ["dependabot/*", "codespace-*"],
            "new_branch_default": "pull_request_required_no_direct_promotion",
        },
        "qmoi_branch_count": len(qmoi_branches),
        "alpha_branch_count": len(alpha_branches),
        "same_name_count": sum(1 for item in comparisons if item["status"] not in {"only_in_qmoi", "only_in_alpha"}),
        "qmoi_only_count": sum(1 for item in comparisons if item["status"] == "only_in_qmoi"),
        "alpha_only_count": sum(1 for item in comparisons if item["status"] == "only_in_alpha"),
        "branches": comparisons,
    }


def audit(qmoi: Path, alpha: Path, backup_branch: str) -> dict[str, Any]:
    for repo in (qmoi, alpha):
        fetch_all_remote_branches(repo)
    qmoi_branches = remote_branch_inventory(qmoi)
    alpha_branches = remote_branch_inventory(alpha)
    return {
        "captured_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "workflow": {
            "run_id": os.environ.get("GITHUB_RUN_ID", ""),
            "repository": os.environ.get("GITHUB_REPOSITORY", ""),
            "head_sha": os.environ.get("GITHUB_SHA", ""),
            "ref": os.environ.get("GITHUB_REF", ""),
        },
        "master": QMOI_NAME,
        "repositories": {
            QMOI_NAME: {
                "root": str(qmoi),
                "main": repo_metrics(qmoi, "main"),
                "backup": repo_metrics(qmoi, backup_branch),
                "branches": qmoi_branches,
            },
            ALPHA_NAME: {
                "root": str(alpha),
                "main": repo_metrics(alpha, "main"),
                "backup": repo_metrics(alpha, backup_branch),
                "branches": alpha_branches,
            },
        },
        "directions": {
            "qmoi-to-alpha": cross_repo_ancestry(qmoi, "main", alpha, "main"),
            "alpha-to-qmoi": cross_repo_ancestry(alpha, "main", qmoi, "main"),
        },
        "branch_alignment": compare_branch_inventories(qmoi, alpha, qmoi_branches, alpha_branches),
        "branch_inventory_coverage": {
            "fetch_refspec": ALL_REMOTE_HEADS_REFSPEC,
            "all_remote_heads_enumerated": True,
            "qmoi_fetched_branch_count": len(qmoi_branches),
            "alpha_fetched_branch_count": len(alpha_branches),
            "scope": "all refs/heads advertised by each origin during fetch",
            "pull_request_refs_included": False,
            "intermediate_commit_trees_enumerated": False,
            "coverage_limitations": [
                "Branches created or moved after fetch are not included until the next audit.",
                "Pull request refs and intermediate commit trees require a separate audit.",
            ],
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
        branches = [args.backup_branch, "main"] if args.promote else [args.backup_branch]
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

    payload = json.dumps(report, indent=2, sort_keys=True)
    write_report(args.report, report)
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
