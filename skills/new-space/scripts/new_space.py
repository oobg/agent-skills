#!/usr/bin/env python3
"""Read-only preflight and verification for the new-space skill."""

import argparse
import fnmatch
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )


def resolve_commit(repo: Path, ref: str) -> str:
    result = git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")
    return result.stdout.strip()


def branch_available(repo: Path, branch: str) -> bool:
    valid = git(repo, "check-ref-format", "--branch", branch, check=False)
    if valid.returncode != 0:
        raise ValueError("invalid branch name")
    exists = git(repo, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}", check=False)
    if exists.returncode == 0:
        return False
    if exists.returncode == 1:
        return True
    raise RuntimeError("could not inspect existing branches")


def remote_branches(repo: Path) -> List[str]:
    result = git(
        repo,
        "for-each-ref",
        "--format=%(refname:short)",
        "refs/remotes/",
    )
    return [line for line in result.stdout.splitlines() if line and not line.endswith("/HEAD")]


def active_releases(repo: Path, main_ref: str, release_glob: str) -> List[str]:
    resolve_commit(repo, main_ref)
    releases = sorted(ref for ref in remote_branches(repo) if fnmatch.fnmatchcase(ref, release_glob))
    active = []
    for ref in releases:
        merged = git(repo, "merge-base", "--is-ancestor", ref, main_ref, check=False)
        if merged.returncode == 1:
            active.append(ref)
        elif merged.returncode != 0:
            raise RuntimeError(f"could not compare release ref: {ref}")
    return active


def preflight(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    if not branch_available(repo, args.branch):
        raise ValueError("branch already exists")

    active: List[str] = []
    selected: Optional[str] = args.base
    decision = "explicit"
    if args.main_ref:
        if not args.release_glob:
            raise ValueError("--release-glob is required with --main-ref")
        active = active_releases(repo, args.main_ref, args.release_glob)
        if len(active) > 1:
            selected = None
            decision = "ambiguous-release"
        elif len(active) == 1:
            selected = active[0]
            decision = "active-release"
        else:
            selected = args.main_ref
            decision = "main-ref"

    payload: Dict[str, object] = {
        "ok": selected is not None,
        "branch_available": True,
        "decision": decision,
        "active_release_refs": active,
    }
    if selected is not None:
        payload["base_ref"] = selected
        payload["base_sha"] = resolve_commit(repo, selected)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if selected is not None else 2


def verify(args: argparse.Namespace) -> int:
    repo = Path(args.worktree).resolve()
    top = Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if top != repo:
        raise ValueError("worktree path is not its Git top level")
    branch = git(repo, "branch", "--show-current").stdout.strip()
    head = resolve_commit(repo, "HEAD")
    ahead = int(git(repo, "rev-list", "--count", f"{args.base_sha}..HEAD").stdout.strip())
    behind = int(git(repo, "rev-list", "--count", f"HEAD..{args.base_sha}").stdout.strip())
    branch_matches = branch == args.expected_branch
    base_matches = head == args.base_sha and ahead == 0 and behind == 0
    print(
        json.dumps(
            {
                "ok": branch_matches and base_matches,
                "actual_branch": branch,
                "expected_branch": args.expected_branch,
                "branch_rewritten": not branch_matches,
                "head": head,
                "base_sha": args.base_sha,
                "ahead": ahead,
                "behind": behind,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if branch_matches and base_matches else 3


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    before = sub.add_parser("preflight", help="resolve base SHA and check branch availability")
    before.add_argument("--repo", required=True)
    before.add_argument("--branch", required=True)
    choice = before.add_mutually_exclusive_group(required=True)
    choice.add_argument("--base")
    choice.add_argument("--main-ref")
    before.add_argument("--release-glob")
    before.set_defaults(run=preflight)

    after = sub.add_parser("verify", help="compare a created worktree with the recorded base")
    after.add_argument("--worktree", required=True)
    after.add_argument("--expected-branch", required=True)
    after.add_argument("--base-sha", required=True)
    after.set_defaults(run=verify)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.run(args)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
