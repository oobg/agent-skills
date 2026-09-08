#!/usr/bin/env python3
"""Collect read-only Git facts needed before a staging deployment."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if check and result.returncode:
        message = result.stderr.strip().splitlines()
        raise RuntimeError(message[-1] if message else "git command failed")
    return result.stdout.rstrip("\n") if result.returncode == 0 else ""


def count_nul(value: str) -> int:
    return len([item for item in value.split("\0") if item])


def resolve_ref(repo: Path, ref: str) -> str | None:
    value = git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}", check=False)
    return value or None


def worktrees(repo: Path) -> list[dict[str, str | bool]]:
    records: list[dict[str, str | bool]] = []
    current: dict[str, str | bool] = {}
    fields = git(repo, "worktree", "list", "--porcelain", "-z").split("\0")
    for field in fields:
        if not field:
            if current:
                records.append(current)
                current = {}
            continue
        key, _, value = field.partition(" ")
        if key == "worktree":
            current["path"] = value
        elif key == "branch":
            prefix = "refs/heads/"
            current["branch"] = value[len(prefix):] if value.startswith(prefix) else value
        elif key == "HEAD":
            current["sha"] = value
        elif key == "detached":
            current["detached"] = True
    return records


def collect(repo: Path, target_branch: str | None, remote: str) -> dict:
    root = Path(git(repo, "rev-parse", "--show-toplevel")).resolve()
    branch = git(root, "symbolic-ref", "--quiet", "--short", "HEAD", check=False)
    remotes = git(root, "remote").splitlines()
    trees = worktrees(root)
    result = {
        "repository": str(root),
        "current": {
            "branch": branch or None,
            "detached": not bool(branch),
            "sha": git(root, "rev-parse", "HEAD"),
        },
        "changes": {
            "staged": count_nul(git(root, "diff", "--cached", "--name-only", "-z")),
            "unstaged": count_nul(git(root, "diff", "--name-only", "-z")),
            "untracked": count_nul(
                git(root, "ls-files", "--others", "--exclude-standard", "-z")
            ),
        },
        "remote": {"name": remote, "configured": remote in remotes},
        "worktrees": trees,
    }
    result["changes"]["clean"] = not any(
        result["changes"][key] for key in ("staged", "unstaged", "untracked")
    )
    if target_branch:
        occupied = [
            tree for tree in trees if tree.get("branch") == target_branch
        ]
        result["target"] = {
            "branch": target_branch,
            "local_sha": resolve_ref(root, f"refs/heads/{target_branch}"),
            "remote_tracking_sha": resolve_ref(
                root, f"refs/remotes/{remote}/{target_branch}"
            ),
            "occupied_worktrees": occupied,
        }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Report read-only Git preflight facts as JSON."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--target-branch")
    parser.add_argument("--remote", required=True)
    args = parser.parse_args(argv)
    try:
        print(json.dumps(collect(args.repo, args.target_branch, args.remote), ensure_ascii=False, indent=2))
    except (OSError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
