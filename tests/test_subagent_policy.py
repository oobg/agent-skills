import hashlib
import importlib.util
import fcntl
import io
import multiprocessing
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "ontology.py"
SOURCE = ROOT / "policies" / "subagent-operation.md"
SPEC = importlib.util.spec_from_file_location("ontology_policy", SCRIPT)
POLICY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(POLICY)


def publish_worker(source, runtime, reviewed_hash, queue):
    try:
        POLICY.publish(Path(source), Path(runtime), reviewed_hash)
        queue.put(None)
    except Exception as exc:  # pragma: no cover - only returned to parent
        queue.put(repr(exc))


class SubagentPolicyTests(unittest.TestCase):
    def reviewed_hash(self, source=SOURCE):
        return POLICY.sha256(POLICY.canonical_rules(source.read_bytes()))

    def publish(self, runtime, source=SOURCE, reviewed_hash=None):
        return POLICY.publish(
            source,
            Path(runtime),
            reviewed_hash or self.reviewed_hash(source),
        )

    def run_cli(self, action, runtime, *extra):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "policy", action,
             "--runtime-dir", str(runtime), *extra],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_source_has_required_rule_ids_and_all_rules_are_preserved(self):
        rules = POLICY.canonical_rules(SOURCE.read_bytes())
        ids = POLICY.validate_rules(rules)
        required = {
            "main-orchestrator", "min-delegation", "parent-validation",
            "model-routing", "model-explicit", "max-depth",
            "redelegation-boundary", "minimal-context", "batching",
            "parallel-conflict-check", "mutation-boundary",
        }
        self.assertTrue(required.issubset(ids))
        snapshot = POLICY.render_snapshot(1, POLICY.sha256(rules), rules)
        self.assertEqual(POLICY.parse_snapshot(snapshot)["rules"], rules)

    def test_marker_and_rule_contracts_are_strict(self):
        base = SOURCE.read_text(encoding="utf-8")
        invalid = [
            b"no markers",
            (POLICY.START + "\n- <!-- rule:ok -->\n  body\n").encode(),
            base.replace("rule:main-orchestrator", "rule:Bad").encode(),
            base.replace(
                "<!-- rule:min-delegation -->",
                "<!-- rule:main-orchestrator -->",
            ).encode(),
            base.replace(
                "- <!-- rule:min-delegation -->\n  필요한 최소 깊이와 최소 수의 에이전트를 사용합니다. 독립 작업은 공유 상태와 통합 경계를 확인한 뒤 병렬화합니다.\n",
                "- <!-- rule:min-delegation -->\n",
            ).encode(),
            base.replace(
                "- <!-- rule:model-explicit -->\n  서브에이전트를 호출할 때 배정 모델을 명시합니다.\n",
                "",
            ).encode(),
        ]
        for source in invalid:
            with self.subTest(source=source[:30]):
                with self.assertRaises(POLICY.PolicyError):
                    POLICY.canonical_rules(source)

    def test_source_hash_normalization_has_exact_boundaries(self):
        expected = POLICY.canonical_rules(SOURCE.read_bytes())
        source = SOURCE.read_text(encoding="utf-8")
        source = "\r\n".join(
            line if line in {POLICY.START, POLICY.END} else line + "  "
            for line in source.split("\n")
        )
        normalized = POLICY.canonical_rules(source.encode("utf-8"))
        self.assertEqual(normalized, expected)
        self.assertEqual(POLICY.sha256(expected), "sha256:" + hashlib.sha256(expected).hexdigest())

    def test_snapshot_rejects_metadata_rules_and_checksum_damage(self):
        rules = POLICY.canonical_rules(SOURCE.read_bytes())
        snapshot = POLICY.render_snapshot(1, POLICY.sha256(rules), rules)
        damaged = [
            snapshot.replace(b"snapshot_format: 1", b"snapshot_format: 2"),
            snapshot.replace(b"policy: subagent-operation\n", b"unknown: value\npolicy: subagent-operation\n"),
            snapshot.replace(b"policy_version: 1", b"policy_version: 0"),
            snapshot.replace(b"source_hash: sha256:", b"source_hash: sha256:f", 1),
            snapshot.replace(b"main-orchestrator", b"main-orchestratoX", 1),
        ]
        for data in damaged:
            with self.subTest(data=data[:100]):
                with self.assertRaises(POLICY.PolicyError):
                    POLICY.parse_snapshot(data)

    def test_strict_metadata_and_canonical_rules_fail_even_when_resigned(self):
        rules = POLICY.canonical_rules(SOURCE.read_bytes())

        def resign(data):
            lines = data.decode().splitlines(keepends=True)
            without = "".join(lines[:5] + lines[6:]).encode()
            lines[5] = f"snapshot_hash: {POLICY.sha256(without)}\n"
            return "".join(lines).encode()

        valid = POLICY.render_snapshot(1, POLICY.sha256(rules), rules)
        reordered = valid.replace(
            b"snapshot_format: 1\npolicy: subagent-operation\n",
            b"policy: subagent-operation\nsnapshot_format: 1\n",
        )
        duplicate = valid.replace(
            b"policy: subagent-operation\n",
            b"policy: subagent-operation\npolicy: subagent-operation\n",
        )
        bad_rules = rules.replace(b"\n  ", b"  \n  ", 1)
        trailing = POLICY.render_snapshot(1, POLICY.sha256(bad_rules), bad_rules)
        for data in (resign(reordered), resign(duplicate), trailing):
            with self.assertRaises(POLICY.PolicyError):
                POLICY.parse_snapshot(data)

        unicode_separator = valid.replace(
            b"snapshot_format: 1\npolicy: subagent-operation\n",
            "snapshot_format: 1\u2028policy: subagent-operation\n".encode(),
        )
        with self.assertRaises(POLICY.PolicyError):
            POLICY.parse_snapshot(resign(unicode_separator))

    def test_publish_versions_and_rejects_source_changed_after_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "runtime"
            source = Path(tmp) / "source.md"
            source.write_bytes(SOURCE.read_bytes())
            first = POLICY.parse_snapshot(self.publish(runtime, source))
            second = POLICY.parse_snapshot(self.publish(runtime, source))
            self.assertEqual((first["policy_version"], second["policy_version"]), (1, 1))
            reviewed = self.reviewed_hash(source)
            source.write_text(
                source.read_text() .replace("필요한 최소 깊이", "필요한 최소 계층"),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(POLICY.PolicyError, "does not match current hash"):
                self.publish(runtime, source, reviewed)
            changed = POLICY.parse_snapshot(self.publish(runtime, source))
            self.assertEqual(changed["policy_version"], 2)

    def test_publish_reextracts_source_only_after_acquiring_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "runtime"
            runtime.mkdir()
            source = Path(tmp) / "source.md"
            source.write_bytes(SOURCE.read_bytes())
            reviewed = self.reviewed_hash(source)
            lock = (runtime / "publish.lock").open("a+b")
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            errors = []

            def worker():
                try:
                    POLICY.publish(source, runtime, reviewed)
                except Exception as exc:
                    errors.append(exc)

            thread = threading.Thread(target=worker)
            thread.start()
            source.write_text(source.read_text().replace("최소 깊이", "최소 계층"), encoding="utf-8")
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
            lock.close()
            thread.join(5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(len(errors), 1)
            self.assertIn("does not match current hash", str(errors[0]))

    def test_publish_refuses_to_replace_corrupt_existing_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            self.publish(runtime)
            snapshot = runtime / "snapshot.md"
            snapshot.write_bytes(snapshot.read_bytes() + b"damage")
            damaged = snapshot.read_bytes()
            with self.assertRaises(POLICY.PolicyError):
                self.publish(runtime)
            self.assertEqual(snapshot.read_bytes(), damaged)

    def test_concurrent_publish_is_serialized_and_lock_file_is_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "runtime"
            sources = []
            for index in range(4):
                source = Path(tmp) / f"source-{index}.md"
                source.write_text(
                    SOURCE.read_text(encoding="utf-8").replace(
                        "필요한 최소 깊이와 최소 수", f"필요한 최소 깊이와 최소 수 {index}"
                    ),
                    encoding="utf-8",
                )
                sources.append(source)
            context = multiprocessing.get_context("spawn")
            queue = context.Queue()
            workers = [context.Process(
                target=publish_worker,
                args=(str(source), str(runtime), self.reviewed_hash(source), queue),
            ) for source in sources]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join(15)
                self.assertEqual(worker.exitcode, 0)
            self.assertEqual([queue.get(timeout=2) for _ in workers], [None] * 4)
            parsed = POLICY.verify_path(runtime / "snapshot.md")
            self.assertEqual(parsed["policy_version"], 4)
            lock_inode = (runtime / "publish.lock").stat().st_ino
            final_source = next(source for source in sources if self.reviewed_hash(source) == parsed["source_hash"])
            self.publish(runtime, final_source)
            self.assertEqual((runtime / "publish.lock").stat().st_ino, lock_inode)

    def test_show_during_publish_returns_only_a_whole_valid_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "runtime"
            old = self.publish(runtime)
            source = Path(tmp) / "changed.md"
            source.write_text(SOURCE.read_text().replace("최소 깊이", "최소 계층"), encoding="utf-8")
            entered = threading.Event()
            release = threading.Event()
            original_replace = POLICY.os.replace
            errors = []

            def paused_replace(src, dst):
                entered.set()
                release.wait(5)
                original_replace(src, dst)

            def worker():
                try:
                    self.publish(runtime, source)
                except Exception as exc:
                    errors.append(exc)

            with mock.patch.object(POLICY.os, "replace", side_effect=paused_replace):
                thread = threading.Thread(target=worker)
                thread.start()
                self.assertTrue(entered.wait(5))
                during = self.run_cli("show", runtime)
                release.set()
                thread.join(5)
            after = self.run_cli("show", runtime)
            self.assertFalse(errors)
            self.assertEqual(during.stdout, old)
            self.assertNotEqual(after.stdout, old)
            POLICY.parse_snapshot(during.stdout)
            POLICY.parse_snapshot(after.stdout)

    def test_show_emits_no_body_when_snapshot_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp)
            (runtime / "snapshot.md").write_bytes(b"private-looking body")
            result = self.run_cli("show", runtime)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, b"")
            self.assertTrue(result.stderr)

    def test_show_reads_once_and_missing_snapshot_creates_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = Path(tmp) / "runtime"
            missing = self.run_cli("show", runtime)
            self.assertNotEqual(missing.returncode, 0)
            self.assertEqual(missing.stdout, b"")
            self.assertFalse(runtime.exists())
            runtime.mkdir()
            data = self.publish(runtime)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with mock.patch.object(POLICY, "read_once", return_value=data) as read:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    result = POLICY.main(["policy", "show", "subagent-operation", "--runtime-dir", str(runtime)])
            self.assertEqual(result, 0)
            self.assertEqual(read.call_count, 1)
            self.assertEqual(stderr.getvalue(), "")

    def test_cli_publish_show_verify_end_to_end_in_tmp(self):
        with tempfile.TemporaryDirectory() as tmp:
            publish = self.run_cli(
                "publish", tmp,
                "--source", str(SOURCE),
                "--reviewed-source-hash", self.reviewed_hash(),
            )
            self.assertEqual(publish.returncode, 0, publish.stderr)
            shown = self.run_cli("show", tmp)
            self.assertEqual(shown.returncode, 0, shown.stderr)
            self.assertEqual(shown.stdout, publish.stdout)
            verified = self.run_cli("verify", tmp)
            self.assertEqual((verified.returncode, verified.stdout), (0, b"valid\n"))


if __name__ == "__main__":
    unittest.main()
