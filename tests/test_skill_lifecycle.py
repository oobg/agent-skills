import importlib.util
import io
import json
import os
import sqlite3
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "skill_lifecycle.py"
SPEC = importlib.util.spec_from_file_location("skill_lifecycle", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LifecycleTests(unittest.TestCase):
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

    def test_queries_concept_candidates(self):
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
            self.assertEqual(
                MODULE.concept_candidates(config),
                [{"name": "반복 지식", "recent_sessions": 2}],
            )

    def test_unmeasured_skill_is_not_parking_candidate(self):
        config = {
            "thresholds": {"park_max_recent_uses": 0},
            "skills": {"quiet-skill": {"status": "active"}},
        }
        original_usage = MODULE.skill_usage
        original_candidates = MODULE.concept_candidates
        original_sync = MODULE.sync
        try:
            MODULE.skill_usage = lambda _: {}
            MODULE.concept_candidates = lambda _: []
            MODULE.sync = lambda *_args, **_kwargs: 0
            output = io.StringIO()
            with redirect_stdout(output):
                MODULE.report(config)
            self.assertIn("unmeasured; never auto-park", output.getvalue())
            self.assertNotIn("review-for-parking", output.getvalue())
        finally:
            MODULE.skill_usage = original_usage
            MODULE.concept_candidates = original_candidates
            MODULE.sync = original_sync


if __name__ == "__main__":
    unittest.main()
