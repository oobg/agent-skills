#!/usr/bin/env python3
"""Compile, publish, show, and verify the subagent operation policy."""

import argparse
import fcntl
import hashlib
import os
from pathlib import Path
import re
import sys
import tempfile


POLICY_NAME = "subagent-operation"
SNAPSHOT_FORMAT = 1
START = "<!-- policy:rules:start -->"
END = "<!-- policy:rules:end -->"
RULE_START = re.compile(r"^- <!-- rule:([a-z0-9]+(?:-[a-z0-9]+)*) -->$")
HASH = re.compile(r"sha256:[0-9a-f]{64}\Z")
REQUIRED_IDS = {
    "main-orchestrator", "min-delegation", "parent-validation",
    "model-routing", "model-explicit", "max-depth", "redelegation-boundary",
    "minimal-context", "batching", "parallel-conflict-check", "mutation-boundary",
}
REPO = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO / "policies" / "subagent-operation.md"
DEFAULT_RUNTIME = Path("~/.ontology/policies/subagent-operation").expanduser()


class PolicyError(ValueError):
    pass


def sha256(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical_rules(source_bytes):
    try:
        text = source_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PolicyError("source is not valid UTF-8") from exc
    if text.count(START) != 1 or text.count(END) != 1:
        raise PolicyError("source must contain exactly one marker pair")
    start = text.index(START) + len(START)
    end = text.index(END)
    if start >= end:
        raise PolicyError("policy markers are out of order or empty")
    rules = text[start:end].replace("\r\n", "\n")
    if "\r" in rules:
        raise PolicyError("source contains unsupported bare CR line endings")
    if rules.startswith("\n"):
        rules = rules[1:]
    if rules.endswith("\n"):
        rules = rules[:-1]
    rules = "\n".join(line.rstrip(" \t") for line in rules.split("\n"))
    rules = rules.rstrip("\n") + "\n"
    encoded = rules.encode("utf-8")
    validate_rules(encoded)
    return encoded


def validate_rules_text(rules_text):
    if not rules_text.endswith("\n") or rules_text.endswith("\n\n"):
        raise PolicyError("rules must end with exactly one LF")
    if "\r" in rules_text:
        raise PolicyError("rules must use LF line endings")
    lines = rules_text[:-1].split("\n")
    starts = []
    for index, line in enumerate(lines):
        match = RULE_START.fullmatch(line)
        if match:
            starts.append((index, match.group(1)))
        elif line.startswith("- <!-- rule:"):
            raise PolicyError("invalid rule identifier or rule marker")
    if not starts or starts[0][0] != 0:
        raise PolicyError("rules must begin with a rule marker")
    ids = [item[1] for item in starts]
    if len(ids) != len(set(ids)):
        raise PolicyError("duplicate rule identifier")
    missing = REQUIRED_IDS.difference(ids)
    if missing:
        raise PolicyError("missing required rule identifiers: " + ", ".join(sorted(missing)))
    for position, (line_index, _rule_id) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        body = lines[line_index + 1:next_index]
        if not body or not any(line.strip() for line in body):
            raise PolicyError("rule body must not be empty")
        if any(line and not line.startswith("  ") for line in body):
            raise PolicyError("rule body lines must be indented by two spaces")
    return ids


def validate_rules(rules_bytes):
    try:
        rules_text = rules_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PolicyError("rules are not valid UTF-8") from exc
    return validate_rules_text(rules_text)


def snapshot_without_hash_line(policy_version, source_hash, rules):
    header = (
        "---\n"
        "snapshot_format: 1\n"
        "policy: subagent-operation\n"
        f"policy_version: {policy_version}\n"
        f"source_hash: {source_hash}\n"
        "---\n\n"
    ).encode("utf-8")
    return header + rules


def render_snapshot(policy_version, source_hash, rules):
    without = snapshot_without_hash_line(policy_version, source_hash, rules)
    digest = sha256(without)
    marker = f"source_hash: {source_hash}\n".encode("utf-8")
    return without.replace(marker, marker + f"snapshot_hash: {digest}\n".encode("utf-8"), 1)


def parse_snapshot(data):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PolicyError("snapshot is not valid UTF-8") from exc
    if "\r" in text:
        raise PolicyError("snapshot must use LF line endings")
    parts = data.split(b"\n", 8)
    if len(parts) != 9 or parts[0] != b"---" or parts[6] != b"---" or parts[7] != b"":
        raise PolicyError("invalid snapshot framing")
    header_lines = [part.decode("utf-8") for part in parts[1:6]]
    expected_prefixes = [
        "snapshot_format: ", "policy: ", "policy_version: ",
        "source_hash: ", "snapshot_hash: ",
    ]
    if any(not line.startswith(prefix) for line, prefix in zip(header_lines, expected_prefixes)):
        raise PolicyError("snapshot metadata order or keys are invalid")
    values = [line.split(": ", 1)[1] for line in header_lines]
    if values[0] != str(SNAPSHOT_FORMAT) or values[1] != POLICY_NAME:
        raise PolicyError("unsupported snapshot format or policy")
    if not re.fullmatch(r"[1-9][0-9]*", values[2]):
        raise PolicyError("invalid policy version")
    if not HASH.fullmatch(values[3]) or not HASH.fullmatch(values[4]):
        raise PolicyError("invalid hash format")
    rules = parts[8]
    validate_rules(rules)
    if any(line.rstrip(" \t") != line for line in rules.decode("utf-8").split("\n")):
        raise PolicyError("snapshot rules contain trailing whitespace")
    if sha256(rules) != values[3]:
        raise PolicyError("source hash does not match rules")
    without_hash = b"\n".join(parts[:5] + parts[6:])
    if sha256(without_hash) != values[4]:
        raise PolicyError("snapshot checksum mismatch")
    return {"policy_version": int(values[2]), "source_hash": values[3], "rules": rules}


def read_once(path):
    with path.open("rb") as handle:
        return handle.read()


def verify_path(path):
    return parse_snapshot(read_once(path))


def publish(source_path, runtime_dir, reviewed_source_hash):
    if not HASH.fullmatch(reviewed_source_hash):
        raise PolicyError("--reviewed-source-hash must be sha256:<64 lowercase hex>")
    runtime_dir.mkdir(parents=True, exist_ok=True)
    lock_path = runtime_dir / "publish.lock"
    snapshot_path = runtime_dir / "snapshot.md"
    temp_path = None
    with lock_path.open("a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        rules = canonical_rules(read_once(source_path))
        actual_source_hash = sha256(rules)
        if actual_source_hash != reviewed_source_hash:
            raise PolicyError(
                f"reviewed source hash {reviewed_source_hash} does not match current hash {actual_source_hash}"
            )
        if snapshot_path.exists():
            current = verify_path(snapshot_path)
            version = current["policy_version"]
            if current["source_hash"] != actual_source_hash:
                version += 1
        else:
            version = 1
        rendered = render_snapshot(version, actual_source_hash, rules)
        parse_snapshot(rendered)
        fd, name = tempfile.mkstemp(prefix=".snapshot.", suffix=".tmp", dir=str(runtime_dir))
        temp_path = Path(name)
        try:
            with os.fdopen(fd, "wb") as temp:
                temp.write(rendered)
                temp.flush()
                os.fsync(temp.fileno())
            verify_path(temp_path)
            os.replace(str(temp_path), str(snapshot_path))
            temp_path = None
            directory_fd = os.open(str(runtime_dir), os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink()
                except FileNotFoundError:
                    pass
    return rendered


def build_parser():
    parser = argparse.ArgumentParser(prog="ontology")
    commands = parser.add_subparsers(dest="command", required=True)
    policy = commands.add_parser("policy")
    actions = policy.add_subparsers(dest="action", required=True)
    for action in ("show", "verify", "publish"):
        sub = actions.add_parser(action)
        sub.add_argument("policy_name", nargs="?", default=POLICY_NAME, choices=[POLICY_NAME])
        sub.add_argument("--runtime-dir", type=Path, default=DEFAULT_RUNTIME)
        if action == "publish":
            sub.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
            sub.add_argument("--reviewed-source-hash", required=True)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    snapshot_path = args.runtime_dir.expanduser() / "snapshot.md"
    try:
        if args.action == "publish":
            rendered = publish(args.source.expanduser(), args.runtime_dir.expanduser(), args.reviewed_source_hash)
            sys.stdout.write(rendered.decode("utf-8"))
        elif args.action == "show":
            data = read_once(snapshot_path)
            parse_snapshot(data)
            sys.stdout.write(data.decode("utf-8"))
        else:
            verify_path(snapshot_path)
            sys.stdout.write("valid\n")
    except (OSError, PolicyError) as exc:
        sys.stderr.write(f"ontology policy {args.action}: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
