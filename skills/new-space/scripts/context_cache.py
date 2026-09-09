#!/usr/bin/env python3
"""Persist user-approved new-space preferences and validated Orca guidance off-repo."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional


SCHEMA_VERSION = 1


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_digest(value: object) -> str:
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def state_root() -> Path:
    return Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")) / "new-space"


def cache_root() -> Path:
    return Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "new-space"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
    ).stdout.strip()


def file_records(paths: List[Path]) -> List[Dict[str, object]]:
    records = []
    for path in paths:
        resolved = path.resolve()
        records.append({"path": str(resolved), "sha256": digest(resolved.read_bytes())})
    return records


def atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def repo_identity(repo: Path) -> Dict[str, str]:
    common = Path(git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")).resolve()
    origin = subprocess.run(
        ["git", "-C", str(repo), "remote", "get-url", "origin"], check=False, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
    ).stdout.strip()
    return {"git_common_dir": str(common), "origin": origin}


def project_path(identity: Dict[str, str]) -> Path:
    return state_root() / "projects" / f"{json_digest(identity)}.json"


def validate_preferences(preferences: object) -> Dict[str, str]:
    forbidden = {"approval_policy", "sandbox_mode", "worktree_id", "terminal_handle"}
    if not isinstance(preferences, dict) or not preferences:
        raise ValueError("preferences must be a non-empty JSON object")
    rejected = forbidden.intersection(preferences)
    if rejected:
        raise ValueError("runtime authority or ephemeral Orca identifiers cannot be stored")
    allowed = {"base_policy", "branch_convention", "handoff_preference", "model_preference"}
    if set(preferences) - allowed:
        raise ValueError("preferences contain unsupported fields")
    if not all(isinstance(value, str) and value for value in preferences.values()):
        raise ValueError("preference values must be non-empty strings")
    return preferences


def policy_records(repo: Path, supplied: List[str]) -> List[Dict[str, object]]:
    sources = list(dict.fromkeys(["AGENTS.md", *supplied]))
    records = []
    for source in sources:
        candidate = Path(source)
        path = candidate if candidate.is_absolute() else repo / candidate
        record: Dict[str, object] = {"source": source, "exists": path.exists()}
        if path.exists():
            record["sha256"] = digest(path.read_bytes())
        records.append(record)
    return records


def project_get(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    identity = repo_identity(repo)
    path = project_path(identity)
    if not path.exists():
        print(json.dumps({"ok": False, "status": "missing", "memory_path": str(path)}))
        return 2
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        print(json.dumps({"ok": False, "status": "invalid", "memory_path": str(path)}))
        return 4
    if not isinstance(payload, dict):
        print(json.dumps({"ok": False, "status": "invalid", "memory_path": str(path)}))
        return 4
    current = policy_records(repo, args.policy_file)
    if payload.get("schema_version") != SCHEMA_VERSION or payload.get("policy_sources") != current:
        print(json.dumps({"ok": False, "status": "stale", "memory_path": str(path)}))
        return 3
    try:
        preferences = validate_preferences(payload.get("preferences"))
    except ValueError:
        print(json.dumps({"ok": False, "status": "invalid", "memory_path": str(path)}))
        return 4
    print(json.dumps({"ok": True, "status": "hit", "preferences": preferences,
                      "memory_path": str(path)}, ensure_ascii=False, indent=2))
    return 0


def project_set(args: argparse.Namespace) -> int:
    preferences = validate_preferences(json.loads(args.preferences_json))
    repo = Path(args.repo).resolve()
    identity = repo_identity(repo)
    path = project_path(identity)
    payload = {"schema_version": SCHEMA_VERSION, "repo_identity": identity,
               "policy_sources": policy_records(repo, args.policy_file),
               "preferences": preferences}
    atomic_json(path, payload)
    print(json.dumps({"ok": True, "status": "stored", "memory_path": str(path)}))
    return 0


def executable_record(executable: str) -> Dict[str, object]:
    selected = shutil.which(executable) if not Path(executable).is_absolute() else executable
    if not selected:
        raise OSError(f"selected Orca executable was not found: {executable}")
    resolved = Path(selected).resolve()
    stat = resolved.stat()
    version = subprocess.run(
        [str(resolved), "--version"], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
    ).stdout.strip()
    return {"path": str(resolved), "version": version, "size": stat.st_size,
            "mtime_ns": stat.st_mtime_ns}


def orca_key(executable: Dict[str, object]) -> str:
    return json_digest({"path": executable["path"]})


def guide_fingerprint(args: argparse.Namespace, executable: Dict[str, object]) -> Dict[str, object]:
    return {"schema_version": SCHEMA_VERSION, "executable": executable,
            "stub": file_records([Path(args.stub_file)])[0],
            "contracts": file_records([Path(item) for item in args.contract_file])}


def orca_guide(args: argparse.Namespace) -> int:
    executable = executable_record(args.orca_executable)
    fingerprint = guide_fingerprint(args, executable)
    path = cache_root() / "orca" / f"{orca_key(executable)}.json"
    cached: Optional[Dict[str, object]] = None
    if path.exists():
        try:
            cached = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            cached = None
    if (not args.refresh and isinstance(cached, dict) and not cached.get("invalidated")
            and cached.get("fingerprint") == fingerprint
            and isinstance(cached.get("guide_source"), str)
            and cached.get("guide_sha256") == digest(cached["guide_source"].encode())):
        if isinstance(cached.get("recipe"), str) and cached["recipe"].strip():
            print(json.dumps({"ok": True, "status": "hit", "recipe": cached["recipe"],
                              "guide_sha256": cached["guide_sha256"], "cache_path": str(path)}, indent=2))
            return 0
        print(json.dumps({"ok": True, "status": "needs-review", "guide_source": cached["guide_source"],
                          "guide_sha256": cached["guide_sha256"], "cache_path": str(path)}, indent=2))
        return 2
    if args.refresh and isinstance(cached, dict):
        cached["recipe"] = None
        cached["invalidated"] = True
        atomic_json(path, cached)
    result = subprocess.run(
        [str(executable["path"]), "skills", "get", "orca-cli", "--full", "--json"],
        check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
    )
    try:
        envelope = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("Orca returned a non-JSON orca-cli guide") from exc
    if (not isinstance(envelope, dict) or envelope.get("name") != "orca-cli"
            or not isinstance(envelope.get("markdown"), str) or not envelope["markdown"].strip()):
        raise ValueError("Orca did not return a successful orca-cli guide")
    payload = {"fingerprint": fingerprint, "guide_sha256": digest(result.stdout.encode()),
               "guide_source": result.stdout, "recipe": None}
    atomic_json(path, payload)
    print(json.dumps({"ok": True, "status": "needs-review", "guide_source": result.stdout,
                      "guide_sha256": payload["guide_sha256"], "cache_path": str(path)}, indent=2))
    return 2


def orca_remember(args: argparse.Namespace) -> int:
    executable = executable_record(args.orca_executable)
    path = cache_root() / "orca" / f"{orca_key(executable)}.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("no valid fetched guide is available to remember") from exc
    if not isinstance(payload, dict):
        raise ValueError("no valid fetched guide is available to remember")
    if payload.get("invalidated"):
        raise ValueError("cached guide was invalidated; fetch and review the current guide")
    if payload.get("fingerprint") != guide_fingerprint(args, executable):
        raise ValueError("Orca or cache contract changed; fetch and review the current guide")
    if (payload.get("guide_sha256") != args.guide_sha256
            or not isinstance(payload.get("guide_source"), str)
            or digest(payload["guide_source"].encode()) != args.guide_sha256):
        raise ValueError("guide hash changed; review the current source before remembering a recipe")
    recipe = Path(args.recipe_file).read_text(encoding="utf-8").strip()
    if not recipe:
        raise ValueError("recipe file is empty")
    payload["recipe"] = recipe
    atomic_json(path, payload)
    print(json.dumps({"ok": True, "status": "ready", "cache_path": str(path)}))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    get = sub.add_parser("project-get")
    get.add_argument("--repo", required=True)
    get.add_argument("--policy-file", action="append", default=[])
    get.set_defaults(run=project_get)
    save = sub.add_parser("project-set")
    save.add_argument("--repo", required=True)
    save.add_argument("--policy-file", action="append", default=[])
    save.add_argument("--preferences-json", required=True)
    save.set_defaults(run=project_set)
    guide = sub.add_parser("orca-guide")
    guide.add_argument("--orca-executable", required=True)
    guide.add_argument("--stub-file", required=True)
    guide.add_argument("--contract-file", action="append", required=True)
    guide.add_argument("--refresh", action="store_true")
    guide.set_defaults(run=orca_guide)
    remember = sub.add_parser("orca-remember")
    remember.add_argument("--orca-executable", required=True)
    remember.add_argument("--stub-file", required=True)
    remember.add_argument("--contract-file", action="append", required=True)
    remember.add_argument("--guide-sha256", required=True)
    remember.add_argument("--recipe-file", required=True)
    remember.set_defaults(run=orca_remember)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.run(args)
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
