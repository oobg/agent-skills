import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).parents[1]


def load(name: str):
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT = load("trigger_misfire_audit")
EVAL = load("eval_trigger_cases")
REVISIONS = load("trigger_revisions")

SYNTHETIC_CASES = {
    "skill": "domain-ontology",
    "cases": [
        {
            "id": "recall-project-rule",
            "expect": "recall",
            "request": "이 저장소에서 정한 검토 규칙을 알려줘",
            "origin": "observed 2030-01-02 · sample-repo",
            "cwd": "~/sample-repo",
        },
        {
            "id": "skip-general-fact",
            "expect": "skip",
            "request": "파이썬 리스트 정렬 방법을 알려줘",
            "origin": "authored boundary case",
            "cwd": "~/sample-repo",
        },
    ],
}


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


class MisfireAuditTests(unittest.TestCase):
    def test_hand_started_recall_is_a_nudge(self):
        for text in ("온톨로지 기반으로 검토해줘", "온톨로지 읽어줘", "KB 조회해줘"):
            with self.subTest(text=text):
                self.assertEqual("nudge", AUDIT.classify(text)[0])

    def test_working_on_the_ontology_is_not_a_missed_trigger(self):
        # An explicit ingestion request was always in scope, so counting it as a
        # misfire would inflate the number the whole measurement rests on.
        for text in ("합성 문서를 온톨로지에 적재해줘", "docs.py를 실행해줘", "테넌트 설정을 확인해줘"):
            with self.subTest(text=text):
                self.assertEqual("ontology_work", AUDIT.classify(text)[0])

    def test_mere_mention_is_neither(self):
        self.assertEqual("mention_only", AUDIT.classify("온톨로지라는 개념이 뭐야?")[0])

    def test_non_timestamp_ts_is_not_bucketed_into_a_fake_month(self):
        self.assertEqual("2030-01", AUDIT.month_of("2030-01-02T03:04:05"))
        self.assertEqual("(시점 미상)", AUDIT.month_of("ordinal-value"))
        self.assertEqual("(시점 미상)", AUDIT.month_of(None))

    def test_eval_runs_are_excluded_from_the_measurement(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases_file = Path(tmp) / "cases.json"
            write_json(cases_file, SYNTHETIC_CASES)
            excluded = AUDIT.case_requests(cases_file)
            first = SYNTHETIC_CASES["cases"][0]["request"]
            self.assertIn(" ".join(first.split()), excluded)

    def test_missing_exclusion_file_requires_an_explicit_choice(self):
        with self.assertRaisesRegex(SystemExit, "--no-exclude"):
            AUDIT.case_requests(Path("missing-cases.json"))


class TriggerCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.cases_file = Path(cls.tmp.name) / "cases.json"
        write_json(cls.cases_file, SYNTHETIC_CASES)
        cls.payload = EVAL.load_cases(cls.cases_file)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_suite_loads_and_declares_both_expectations(self):
        expectations = {case["expect"] for case in self.payload["cases"]}
        self.assertEqual({"recall", "skip"}, expectations)

    def test_no_case_carries_the_nudge_it_is_testing_for(self):
        # The question is whether the skill fires without being told to. A case that
        # still says "온톨로지 기반으로" reproduces the workaround instead of testing it.
        for case in self.payload["cases"]:
            with self.subTest(case=case["id"]):
                for pattern in AUDIT.NUDGE_PATTERNS:
                    self.assertNotIn(pattern, case["request"].lower())

    def test_observed_cases_name_where_they_came_from(self):
        observed = [c for c in self.payload["cases"] if c["origin"].startswith("observed")]
        self.assertTrue(observed)
        for case in observed:
            with self.subTest(case=case["id"]):
                self.assertRegex(case["origin"], r"^observed \d{4}-\d{2}-\d{2} · .+")

    def test_grading_follows_the_evidence_line(self):
        recall = {"expect": "recall"}
        skip = {"expect": "skip"}
        self.assertTrue(EVAL.grade(recall, "근거: sample · synthetic-note")[0])
        self.assertFalse(EVAL.grade(recall, "그냥 일반론으로 답했다")[0])
        self.assertTrue(EVAL.grade(skip, "합성 테스트가 실패했다")[0])
        self.assertFalse(EVAL.grade(skip, "근거: sample · synthetic-note")[0])

    def test_non_object_case_is_rejected_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases_file = Path(tmp) / "cases.json"
            write_json(cases_file, {"cases": ["invalid"]})
            with self.assertRaisesRegex(SystemExit, r"case\[0\]: must be an object"):
                EVAL.load_cases(cases_file)

    def test_runner_uses_provider_neutral_argv_without_storing_output(self):
        captured = {}

        def fake_run(argv, **kwargs):
            captured["argv"] = argv
            captured["cwd"] = kwargs.get("cwd")

            class Completed:
                returncode = 0
                stdout = "근거: sample · synthetic-note"
                stderr = ""

            return Completed()

        original = EVAL.subprocess.run
        EVAL.subprocess.run = fake_run
        try:
            case = {"id": "x", "expect": "recall", "request": "질문", "origin": "authored"}
            template = ["sample-agent", "--ephemeral", "--prompt", "{request}"]
            result = EVAL.run_case(case, ROOT, template, 10)
        finally:
            EVAL.subprocess.run = original

        self.assertEqual(["sample-agent", "--ephemeral", "--prompt", "질문"], captured["argv"])
        self.assertTrue(result["passed"])
        self.assertNotIn("output_head", result)

    def test_nonzero_exit_without_stderr_fails(self):
        class Completed:
            returncode = 7
            stdout = "근거: sample · synthetic-note"
            stderr = ""

        original = EVAL.subprocess.run
        EVAL.subprocess.run = lambda *_args, **_kwargs: Completed()
        try:
            case = {"id": "x", "expect": "recall", "request": "질문", "origin": "authored"}
            result = EVAL.run_case(case, ROOT, ["sample-agent", "{request}"], 10)
        finally:
            EVAL.subprocess.run = original
        self.assertFalse(result["passed"])
        self.assertIn("exit code 7", result["reason"])

    def test_empty_or_whitespace_stdout_fails_for_both_expectations(self):
        for expect in ("skip", "recall"):
            for stdout in ("", " \n\t"):
                with self.subTest(expect=expect, stdout=repr(stdout)):
                    class Completed:
                        returncode = 0
                        stderr = ""

                    Completed.stdout = stdout
                    original = EVAL.subprocess.run
                    EVAL.subprocess.run = lambda *_args, **_kwargs: Completed()
                    try:
                        case = {"id": "x", "expect": expect, "request": "질문", "origin": "authored"}
                        result = EVAL.run_case(case, ROOT, ["sample-agent", "{request}"], 10)
                    finally:
                        EVAL.subprocess.run = original
                    self.assertFalse(result["passed"])
                    self.assertIn("응답 없음", result["reason"])

    def test_cli_empty_stdout_fails_and_writes_zero_pass_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            cases_file = Path(tmp) / "cases.json"
            report_file = Path(tmp) / "report.json"
            write_json(cases_file, {
                "skill": "sample-skill",
                "cases": [{
                    "id": "empty-response",
                    "expect": "skip",
                    "request": "합성 질문",
                    "origin": "authored synthetic case",
                }],
            })
            command = json.dumps([sys.executable, "-c", "pass", "{request}"])
            exit_code = EVAL.main([
                "--cases", str(cases_file),
                "--run",
                "--command-json", command,
                "--out", str(report_file),
            ])
            self.assertEqual(1, exit_code)
            report = json.loads(report_file.read_text(encoding="utf-8"))
            self.assertEqual(0, report["passed"])

    def test_failure_report_does_not_copy_stderr(self):
        class Completed:
            returncode = 2
            stdout = ""
            stderr = "synthetic-sensitive-command-argument"

        original = EVAL.subprocess.run
        EVAL.subprocess.run = lambda *_args, **_kwargs: Completed()
        try:
            case = {"id": "x", "expect": "skip", "request": "질문", "origin": "authored"}
            result = EVAL.run_case(case, ROOT, ["sample-agent", "{request}"], 10)
        finally:
            EVAL.subprocess.run = original
        self.assertNotIn("synthetic-sensitive-command-argument", str(result))

    def test_command_template_requires_one_request_placeholder(self):
        valid = EVAL.command_template('["sample-agent", "--prompt", "{request}"]')
        self.assertEqual(["sample-agent", "--prompt", "{request}"], valid)
        for raw in ('["sample-agent"]', '["{request}", "{request}"]', '["{request}"]', '"sample-agent"'):
            with self.subTest(raw=raw), self.assertRaises(SystemExit):
                EVAL.command_template(raw)

    def test_removed_agent_option_explains_the_migration(self):
        with self.assertRaises(SystemExit):
            EVAL.main(["--agent", "claude"])

    def test_every_case_declares_the_repository_it_was_observed_in(self):
        for case in self.payload["cases"]:
            with self.subTest(case=case["id"]):
                self.assertTrue(case.get("cwd"), "cwd 없이는 코드 저장소 안의 판단을 시험할 수 없다")

    def test_missing_directory_falls_back_and_is_reported(self):
        path, found = EVAL.case_cwd({"cwd": "/nonexistent/repo"}, ROOT)
        self.assertEqual(ROOT, path)
        self.assertFalse(found)

    def test_a_plain_run_does_not_spend_usage(self):
        # Every case costs one agent session, so the runner without --run must stay a
        # plan. This calls it with the agent replaced by a landmine.
        def landmine(*args, **kwargs):
            raise AssertionError("에이전트를 호출했다 — --run 없이는 호출하지 않아야 한다")

        original = EVAL.subprocess.run
        EVAL.subprocess.run = landmine
        try:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = EVAL.main(["--cases", str(self.cases_file)])
        finally:
            EVAL.subprocess.run = original

        self.assertEqual(0, exit_code)
        output = buffer.getvalue()
        self.assertIn("--run", output)
        self.assertIn("사용량이 차감된다", output)


class RevisionLogTests(unittest.TestCase):
    def test_log_is_valid_and_pins_a_blob_sha(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "revisions.json"
            write_json(
                log,
                {"revisions": [{"date": "2030-01-02", "skill": "sample-skill", "blob_sha": "a" * 40,
                                "reason": "합성 이유", "changed": ["합성 변경"]}]},
            )
            row = REVISIONS.load(log)["revisions"][0]
            self.assertRegex(row["blob_sha"], r"^[0-9a-f]{40}$")
            self.assertTrue(row["changed"])
            self.assertRegex(row["date"], r"^\d{4}-\d{2}-\d{2}$")

    def test_a_score_attaches_to_the_revision_it_measured(self):
        # A run is not a revision. Scores land on the row whose blob sha they were
        # measured against, so the same SKILL.md can be measured more than once.
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "revisions.json"
            sha = REVISIONS.blob_sha(ROOT / "skills" / "domain-ontology" / "SKILL.md")
            log.write_text(
                json.dumps(
                    {
                        "revisions": [
                            {
                                "date": "2030-01-02",
                                "skill": "domain-ontology",
                                "blob_sha": sha,
                                "reason": "r",
                                "changed": ["c"],
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = REVISIONS.main(
                    ["--log", str(log), "score", "--skill", "domain-ontology", "--score", "3/9"]
                )
            self.assertEqual(0, code)
            row = json.loads(log.read_text(encoding="utf-8"))["revisions"][0]
            self.assertEqual("3/9", row["trigger_score"])
            self.assertEqual(1, len(row["runs"]))

    def test_a_score_without_a_matching_revision_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "revisions.json"
            log.write_text(json.dumps({"revisions": []}), encoding="utf-8")
            code = REVISIONS.main(
                ["--log", str(log), "score", "--skill", "domain-ontology", "--score", "9/9"]
            )
            self.assertEqual(1, code)

    def test_required_fields_are_enforced(self):
        for field in REVISIONS.REQUIRED:
            self.assertIn(field, {"date", "skill", "blob_sha", "reason", "changed"})


if __name__ == "__main__":
    unittest.main()
