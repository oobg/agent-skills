import importlib.util
import io
import json
import os
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "skill_lifecycle.py"
SPEC = importlib.util.spec_from_file_location("skill_lifecycle", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LifecycleTests(unittest.TestCase):
    def test_provider_mode_defaults_to_managed_for_string_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            provider = Path(tmp) / "provider"
            source = root / "skills" / "active"
            source.mkdir(parents=True)
            config = {
                "providers": {"sample": str(provider)},
                "skills": {
                    "active": {"status": "active", "providers": ["sample"]}
                },
            }

            with mock.patch.object(MODULE, "ROOT", root):
                self.assertEqual(MODULE.provider_mode(config, "sample"), "managed")
                self.assertEqual(
                    MODULE.expected_links(config),
                    [("sample", provider / "active", source.resolve())],
                )

    def test_external_provider_is_neither_planned_nor_unlinked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            provider = Path(tmp) / "provider"
            active_source = root / "skills" / "active"
            dormant_source = root / "skills" / "dormant"
            active_source.mkdir(parents=True)
            dormant_source.mkdir(parents=True)
            provider.mkdir()
            (active_source / "SKILL.md").write_text("# active\n")
            (dormant_source / "SKILL.md").write_text("# dormant\n")
            dormant_link = provider / "dormant"
            dormant_link.symlink_to(dormant_source, target_is_directory=True)
            config = {
                "providers": {"sample": str(provider)},
                "provider_modes": {"sample": "external"},
                "skills": {
                    "active": {"status": "active", "providers": ["sample"]},
                    "dormant": {"status": "retired", "providers": ["sample"]},
                },
            }

            output = io.StringIO()
            with mock.patch.object(MODULE, "ROOT", root), redirect_stdout(output):
                self.assertEqual(MODULE.expected_links(config), [])
                self.assertEqual(MODULE.sync(config, apply=True), 0)

            self.assertFalse(os.path.lexists(provider / "active"))
            self.assertTrue(dormant_link.is_symlink())
            self.assertEqual(dormant_link.resolve(), dormant_source.resolve())
            self.assertIn("external", output.getvalue())
            self.assertIn("unverified; skipped", output.getvalue())
            self.assertNotIn("would-link", output.getvalue())
            self.assertNotIn("unlink", output.getvalue())

    def test_external_provider_status_is_visible_in_report_and_doctor(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            provider = Path(tmp) / "provider"
            db = Path(tmp) / "ontology.db"
            provider.mkdir()
            db.touch()
            config = {
                "ontology_db": str(db),
                "providers": {"sample": str(provider)},
                "provider_modes": {"sample": "external"},
                "thresholds": {"park_max_recent_uses": 0},
                "skills": {},
            }

            report_output = io.StringIO()
            with (
                mock.patch.object(MODULE, "ROOT", root),
                mock.patch.object(MODULE, "skill_usage", return_value={}),
                mock.patch.object(MODULE, "concept_candidates", return_value=[]),
                mock.patch.object(MODULE, "repeated_concepts", return_value=[]),
                redirect_stdout(report_output),
            ):
                MODULE.report(config)

            doctor_output = io.StringIO()
            with mock.patch.object(MODULE, "ROOT", root), redirect_stdout(doctor_output):
                self.assertEqual(MODULE.doctor(config), 0)

            for output in (report_output.getvalue(), doctor_output.getvalue()):
                self.assertIn("external", output)
                self.assertIn("unverified; skipped", output)

    def test_sync_preserves_unregistered_link_to_canonical_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            provider = Path(tmp) / "provider"
            source = root / "skills" / "unregistered"
            source.mkdir(parents=True)
            provider.mkdir()
            (source / "SKILL.md").write_text("# unregistered\n")
            link = provider / "unregistered"
            link.symlink_to(source, target_is_directory=True)
            config = {
                "providers": {"sample": str(provider)},
                "skills": {},
            }

            output = io.StringIO()
            with mock.patch.object(MODULE, "ROOT", root), redirect_stdout(output):
                self.assertEqual(MODULE.sync(config, apply=True), 0)

            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), source.resolve())
            self.assertNotIn("unlink", output.getvalue())

    def test_sync_preserves_active_link_to_a_different_canonical_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            provider = Path(tmp) / "provider"
            active_source = root / "skills" / "active"
            other_source = root / "skills" / "other"
            active_source.mkdir(parents=True)
            other_source.mkdir(parents=True)
            provider.mkdir()
            (active_source / "SKILL.md").write_text("# active\n")
            (other_source / "SKILL.md").write_text("# other\n")
            link = provider / "active"
            link.symlink_to(other_source, target_is_directory=True)
            config = {
                "providers": {"sample": str(provider)},
                "skills": {
                    "active": {"status": "active", "providers": ["sample"]}
                },
            }

            output = io.StringIO()
            errors = io.StringIO()
            with (
                mock.patch.object(MODULE, "ROOT", root),
                redirect_stdout(output),
                redirect_stderr(errors),
            ):
                self.assertEqual(MODULE.sync(config, apply=True), 1)

            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), other_source.resolve())
            self.assertIn("unmanaged target exists", errors.getvalue())
            self.assertNotIn("unlink", output.getvalue())

    def test_sync_preserves_inactive_link_to_a_different_canonical_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            provider = Path(tmp) / "provider"
            dormant_source = root / "skills" / "dormant"
            other_source = root / "skills" / "other"
            dormant_source.mkdir(parents=True)
            other_source.mkdir(parents=True)
            provider.mkdir()
            (dormant_source / "SKILL.md").write_text("# dormant\n")
            (other_source / "SKILL.md").write_text("# other\n")
            link = provider / "dormant"
            link.symlink_to(other_source, target_is_directory=True)
            config = {
                "providers": {"sample": str(provider)},
                "skills": {
                    "dormant": {"status": "retired", "providers": ["sample"]}
                },
            }

            output = io.StringIO()
            with mock.patch.object(MODULE, "ROOT", root), redirect_stdout(output):
                self.assertEqual(MODULE.sync(config, apply=True), 0)

            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), other_source.resolve())
            self.assertNotIn("unlink", output.getvalue())

    def test_sync_reports_and_removes_declared_inactive_links(self):
        for status in ("candidate", "parked", "retired"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "repo"
                provider = Path(tmp) / "provider"
                source = root / "skills" / "dormant"
                source.mkdir(parents=True)
                provider.mkdir()
                (source / "SKILL.md").write_text("# dormant\n")
                link = provider / "dormant"
                link.symlink_to(source, target_is_directory=True)
                config = {
                    "providers": {"sample": str(provider)},
                    "skills": {
                        "dormant": {
                            "status": status,
                            "providers": ["sample"],
                        }
                    },
                }

                dry_run = io.StringIO()
                with mock.patch.object(MODULE, "ROOT", root), redirect_stdout(dry_run):
                    self.assertEqual(MODULE.sync(config, apply=False), 0)
                self.assertTrue(link.is_symlink())
                self.assertIn("would-unlink", dry_run.getvalue())

                applied = io.StringIO()
                with mock.patch.object(MODULE, "ROOT", root), redirect_stdout(applied):
                    self.assertEqual(MODULE.sync(config, apply=True), 0)
                self.assertFalse(os.path.lexists(link))
                self.assertIn("unlink", applied.getvalue())

    def test_ontology_db_expands_home_directory(self):
        original_query_rows = MODULE.query_rows
        try:
            seen = []
            MODULE.query_rows = lambda path, *_args: seen.append(path) or []
            MODULE.skill_usage(
                {
                    "ontology_db": "~/.ontology/ontology.db",
                    "thresholds": {"park_after_days": 90},
                }
            )
            self.assertEqual(
                seen,
                [Path(os.path.expanduser("~/.ontology/ontology.db"))],
            )
        finally:
            MODULE.query_rows = original_query_rows

    def test_invalid_status_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(
                json.dumps({"version": 1, "skills": {"x": {"status": "unknown"}}})
            )
            with self.assertRaises(ValueError):
                MODULE.load_config(path)

    def test_unknown_provider_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({
                "version": 1,
                "providers": {"sample": "~/sample-skills"},
                "skills": {"x": {"status": "active", "providers": ["typo"]}},
            }))
            with self.assertRaisesRegex(ValueError, "unknown providers"):
                MODULE.load_config(path)

    def test_provider_modes_must_be_a_map(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({
                "version": 1,
                "providers": {"sample": "~/sample-skills"},
                "provider_modes": ["external"],
            }))
            with self.assertRaisesRegex(ValueError, "provider_modes must be a map"):
                MODULE.load_config(path)

    def test_provider_modes_reject_unknown_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({
                "version": 1,
                "providers": {"sample": "~/sample-skills"},
                "provider_modes": {"typo": "external"},
            }))
            with self.assertRaisesRegex(ValueError, "references unknown providers"):
                MODULE.load_config(path)

    def test_provider_modes_reject_unknown_mode(self):
        for mode in ("delegated", ["external"]):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "config.json"
                path.write_text(json.dumps({
                    "version": 1,
                    "providers": {"sample": "~/sample-skills"},
                    "provider_modes": {"sample": mode},
                }))
                with self.assertRaisesRegex(ValueError, "invalid provider modes"):
                    MODULE.load_config(path)

    def test_registered_active_skills_target_every_declared_provider(self):
        config = MODULE.load_config(Path(__file__).parents[1] / "lifecycle.json")
        expected = set(config["providers"])
        for name, meta in config["skills"].items():
            if meta["status"] in {"active", "pinned"}:
                with self.subTest(skill=name):
                    self.assertEqual(expected, set(meta["providers"]))

    def test_candidate_classification_requires_human_rationale(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({
                "version": 1,
                "candidate_classifications": {
                    "계층적 검증": {"kind": "procedure", "reusable": True}
                },
            }))
            with self.assertRaisesRegex(ValueError, "must include a rationale"):
                MODULE.load_config(path)

    def test_frequency_alone_is_not_a_skill_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "ontology.db"
            with sqlite3.connect(db) as conn:
                conn.executescript(
                    """
                    CREATE TABLE concepts(id INTEGER PRIMARY KEY, name TEXT);
                    CREATE TABLE sessions(session_id TEXT PRIMARY KEY, last_ts TEXT);
                    CREATE TABLE session_concepts(session_id TEXT, concept_id INTEGER);
                    INSERT INTO concepts(id, name) VALUES (1, '반복 지식');
                    INSERT INTO sessions(session_id, last_ts)
                    VALUES ('s1', '2999-01-01'), ('s2', '2999-01-02');
                    INSERT INTO session_concepts(session_id, concept_id)
                    VALUES ('s1', 1), ('s2', 1);
                    """
                )
            config = {
                "ontology_db": str(db),
                "thresholds": {
                    "candidate_min_sessions": 2,
                    "candidate_window_days": 90
                },
                "skills": {},
                "candidate_exclusions": []
            }
            self.assertEqual(MODULE.concept_candidates(config), [])
            self.assertEqual(
                MODULE.repeated_concepts(config),
                [{"name": "반복 지식", "recent_sessions": 2}],
            )

    def test_explicit_reusable_procedure_is_a_skill_candidate(self):
        original_repeated = MODULE.repeated_concepts
        try:
            MODULE.repeated_concepts = lambda _: [
                {"name": "계층적 검증", "recent_sessions": 12}
            ]
            config = {
                "candidate_classifications": {
                    "계층적 검증": {
                        "kind": "procedure",
                        "reusable": True,
                        "rationale": "입력-검사-종료 절차가 여러 프로젝트에서 반복됨",
                    }
                }
            }
            self.assertEqual(
                MODULE.concept_candidates(config),
                [
                    {
                        "name": "계층적 검증",
                        "recent_sessions": 12,
                        "rationale": "입력-검사-종료 절차가 여러 프로젝트에서 반복됨",
                    }
                ],
            )
        finally:
            MODULE.repeated_concepts = original_repeated

    def test_domain_concept_classification_does_not_promote(self):
        original_repeated = MODULE.repeated_concepts
        try:
            MODULE.repeated_concepts = lambda _: [
                {"name": "점주앱", "recent_sessions": 30}
            ]
            config = {
                "candidate_classifications": {
                    "점주앱": {"kind": "domain", "reusable": True}
                }
            }
            self.assertEqual(MODULE.concept_candidates(config), [])
        finally:
            MODULE.repeated_concepts = original_repeated

    def test_unmeasured_skill_is_not_parking_candidate(self):
        config = {
            "thresholds": {"park_max_recent_uses": 0},
            "skills": {"quiet-skill": {"status": "active"}},
        }
        original_usage = MODULE.skill_usage
        original_candidates = MODULE.concept_candidates
        original_repeated = MODULE.repeated_concepts
        original_sync = MODULE.sync
        try:
            MODULE.skill_usage = lambda _: {}
            MODULE.concept_candidates = lambda _: []
            MODULE.repeated_concepts = lambda _: []
            MODULE.sync = lambda *_args, **_kwargs: 0
            output = io.StringIO()
            with redirect_stdout(output):
                MODULE.report(config)
            self.assertIn("unmeasured; never auto-park", output.getvalue())
            self.assertNotIn("review-for-parking", output.getvalue())
        finally:
            MODULE.skill_usage = original_usage
            MODULE.concept_candidates = original_candidates
            MODULE.repeated_concepts = original_repeated
            MODULE.sync = original_sync


if __name__ == "__main__":
    unittest.main()
