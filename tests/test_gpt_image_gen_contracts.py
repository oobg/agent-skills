import json
import os
import stat
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
SKILL_DIR = ROOT / "skills" / "gpt-image-gen"
SKILL = SKILL_DIR / "SKILL.md"
GENERATE = SKILL_DIR / "scripts" / "generate.sh"


class GptImageGenContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")
        cls.script = GENERATE.read_text(encoding="utf-8")

    def test_generation_requires_an_explicit_user_invocation(self):
        self.assertIn("명시적 호출 전용", self.text)
        self.assertIn("`/gpt-image-gen <이미지 설명>` 형태로 직접 호출한 경우", self.text)
        self.assertIn("사용량이 실제로 차감된다", self.text)

    def test_empty_prompt_asks_instead_of_guessing(self):
        self.assertIn("임의로 추측해 생성하지 말고", self.text)

    def test_model_must_not_assemble_the_codex_command_itself(self):
        self.assertIn("`codex exec` 명령을 본문에서 직접 조립하지 말고", self.text)
        self.assertIn("bash scripts/generate.sh", self.text)

    def test_script_is_executable_and_reports_a_single_saved_path(self):
        self.assertTrue(GENERATE.is_file())
        self.assertTrue(os.stat(GENERATE).st_mode & stat.S_IXUSR)
        self.assertIn("set -euo pipefail", self.script)
        self.assertIn("echo \"SAVED ${ABS_OUT}\"", self.script)

    def test_parallel_calls_stay_isolated(self):
        self.assertIn('UNIQ="$$-${RANDOM}"', self.script)
        self.assertIn("/tmp/gpt-image-gen-${UNIQ}.log", self.script)
        self.assertIn("이번 호출의 결과를 확정할 수 없습니다", self.script)

    def test_user_prompt_never_runs_under_a_full_access_sandbox(self):
        # The prompt is interpolated into the agent's instruction, so injected text
        # runs with whatever the sandbox grants. --add-dir is also meaningless under
        # danger-full-access, which is what the original call combined.
        self.assertIn("--sandbox workspace-write", self.script)
        self.assertNotIn("danger-full-access \\", self.script)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", self.script)
        self.assertIn('--add-dir "$ABS_OUT_DIR"', self.script)

    def test_missing_label_value_never_becomes_a_paid_call(self):
        # `shift 2 || true` swallowed the failure and sent "--label" as the prompt.
        self.assertNotIn("shift 2 || true", self.script)
        self.assertIn("--label 뒤에는 라벨 값과 프롬프트가 모두 필요합니다", self.script)

    def test_script_runs_on_the_default_macos_bash(self):
        # mapfile is bash 4+; /bin/bash on macOS is 3.2 and set -e would kill the
        # fallback at exit 127, breaking both the SAVED and the ERROR contract.
        self.assertNotIn("mapfile", self.script)

    def test_parallel_report_does_not_overclaim_the_fallback(self):
        self.assertIn("최선 추정이지 이번 호출의 결과라는 보장이 아니므로", self.text)

    def test_multiple_images_need_a_separate_confirmation(self):
        self.assertIn("2장 이상을 만들기 전에는 몇 장을 만들지 사용자에게 확인받는다", self.text)

    def test_lifecycle_registers_the_skill(self):
        config = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))
        entry = config["skills"]["gpt-image-gen"]
        self.assertEqual(entry["status"], "active")
        self.assertEqual(entry["providers"], ["claude"])


if __name__ == "__main__":
    unittest.main()
