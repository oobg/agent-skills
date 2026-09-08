#!/usr/bin/env python3
"""Preflight and safely finalize a worktree created by the new-space skill."""

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


def current_branch(repo: Path) -> str:
    branch = git(repo, "branch", "--show-current").stdout.strip()
    if not branch:
        raise ValueError("detached HEAD is not supported")
    return branch


def compare_base(repo: Path, base_sha: str) -> Dict[str, object]:
    head = resolve_commit(repo, "HEAD")
    ahead = int(git(repo, "rev-list", "--count", f"{base_sha}..HEAD").stdout.strip())
    behind = int(git(repo, "rev-list", "--count", f"HEAD..{base_sha}").stdout.strip())
    return {
        "head": head,
        "base_sha": base_sha,
        "ahead": ahead,
        "behind": behind,
        "base_matches": head == base_sha and ahead == 0 and behind == 0,
    }


def ensure_worktree(repo: Path) -> None:
    top = Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    if top != repo:
        raise ValueError("worktree path is not its Git top level")
    listed = git(repo, "worktree", "list", "--porcelain", "-z").stdout.split("\0")
    paths = [Path(field[9:]).resolve() for field in listed if field.startswith("worktree ")]
    if paths.count(repo) != 1:
        raise ValueError("worktree path is not uniquely registered")


def ensure_linked_worktree(repo: Path) -> None:
    git_dir = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-dir").stdout.strip()).resolve()
    common_dir = Path(
        git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir").stdout.strip()
    ).resolve()
    if git_dir == common_dir:
        raise ValueError("refusing to finalize the primary checkout")


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
    ensure_worktree(repo)
    branch = current_branch(repo)
    base = compare_base(repo, args.base_sha)
    branch_matches = branch == args.expected_branch
    base_matches = bool(base["base_matches"])
    print(
        json.dumps(
            {
                "ok": branch_matches and base_matches,
                "actual_branch": branch,
                "expected_branch": args.expected_branch,
                "branch_rewritten": not branch_matches,
                **base,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if branch_matches and base_matches else 3


def orca_state(executable: str, worktree_id: str, repo: Path) -> Dict[str, str]:
    result = subprocess.run(
        [executable, "worktree", "show", "--worktree", f"id:{worktree_id}", "--json"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    payload = json.loads(result.stdout)
    if not isinstance(payload, dict) or payload.get("ok") is not True:
        raise ValueError("Orca worktree lookup did not succeed")
    result_payload = payload.get("result")
    if not isinstance(result_payload, dict) or not isinstance(result_payload.get("worktree"), dict):
        raise ValueError("Orca response did not contain result.worktree")
    worktree = result_payload["worktree"]
    if worktree.get("id") != worktree_id:
        raise ValueError("Orca returned a different worktree id")
    path = worktree.get("path")
    if not isinstance(path, str) or Path(path).resolve() != repo:
        raise ValueError("Orca returned a different worktree path")
    nested = worktree.get("git")
    if not isinstance(nested, dict):
        raise ValueError("Orca response did not contain worktree.git")
    candidates = [worktree.get("branch"), nested.get("branch")]
    if not all(isinstance(value, str) and value for value in candidates):
        raise ValueError("Orca response did not contain both branch fields")
    prefix = "refs/heads/"
    normalized = [branch[len(prefix):] if branch.startswith(prefix) else branch for branch in candidates]
    if len(set(normalized)) != 1:
        raise ValueError("Orca branch fields disagree")
    heads = [worktree.get("head"), nested.get("head")]
    if not all(isinstance(value, str) and value for value in heads) or len(set(heads)) != 1:
        raise ValueError("Orca head fields are missing or disagree")
    return {"branch": normalized[0], "head": heads[0]}


def finalize(args: argparse.Namespace) -> int:
    repo = Path(args.worktree).resolve()
    ensure_worktree(repo)
    ensure_linked_worktree(repo)
    if "::" not in args.worktree_id:
        raise ValueError("worktree id must be the full <repo-id>::<path> value")
    id_path = Path(args.worktree_id.split("::", 1)[1]).resolve()
    if id_path != repo:
        raise ValueError("worktree id path does not match --worktree")

    actual = current_branch(repo)
    if actual != args.created_branch:
        raise ValueError("actual branch does not match --created-branch")
    base = compare_base(repo, args.base_sha)
    if not base["base_matches"]:
        raise ValueError("HEAD does not exactly match the recorded base SHA")
    if git(repo, "status", "--porcelain=v1").stdout:
        raise ValueError("created worktree is dirty")

    branch_matches = actual == args.expected_branch
    if branch_matches:
        observed = orca_state(args.orca_executable, args.worktree_id, repo)
        ok = observed["branch"] == args.expected_branch and observed["head"] == args.base_sha
        print(json.dumps({"ok": ok, "branch_repaired": False, "actual_branch": actual,
                          "orca_branch": observed["branch"], "orca_head": observed["head"], **base},
                         ensure_ascii=False, indent=2))
        return 0 if ok else 3

    if not branch_available(repo, args.expected_branch):
        raise ValueError("expected branch already exists")
    if not args.apply:
        print(json.dumps({"ok": False, "repair_required": True, "actual_branch": actual,
                          "expected_branch": args.expected_branch, **base}, ensure_ascii=False, indent=2))
        return 4

    git(repo, "branch", "-m", args.expected_branch)
    repaired = current_branch(repo)
    after = compare_base(repo, args.base_sha)
    try:
        observed = orca_state(args.orca_executable, args.worktree_id, repo)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "branch_repaired": True, "actual_branch": repaired,
                          "error": str(exc), **after}, ensure_ascii=False, indent=2))
        return 3
    if (repaired != args.expected_branch or not after["base_matches"]
            or observed["branch"] != args.expected_branch or observed["head"] != args.base_sha):
        print(json.dumps({"ok": False, "branch_repaired": True, "actual_branch": repaired,
                          "orca_branch": observed["branch"], "orca_head": observed["head"],
                          "error": "Git or Orca post-repair verification failed", **after},
                         ensure_ascii=False, indent=2))
        return 3

    print(json.dumps({"ok": True, "branch_repaired": True, "actual_branch": repaired,
                      "orca_branch": observed["branch"], "orca_head": observed["head"], **after},
                     ensure_ascii=False, indent=2))
    return 0


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

    finish = sub.add_parser("finalize", help="repair an Orca-created branch and verify all postconditions")
    finish.add_argument("--worktree", required=True)
    finish.add_argument("--worktree-id", required=True)
    finish.add_argument("--created-branch", required=True)
    finish.add_argument("--expected-branch", required=True)
    finish.add_argument("--base-sha", required=True)
    finish.add_argument("--orca-executable", required=True)
    finish.add_argument("--apply", action="store_true")
    finish.set_defaults(run=finalize)
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
