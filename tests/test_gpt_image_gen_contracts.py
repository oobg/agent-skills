import json
import os
import stat
import subprocess
import tempfile
import textwrap
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
SKILL_DIR = ROOT / "skills" / "gpt-image-gen"
SKILL = SKILL_DIR / "SKILL.md"
GENERATE = SKILL_DIR / "scripts" / "generate.sh"
OPENAI_YAML = SKILL_DIR / "agents" / "openai.yaml"


class GptImageGenContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")
        cls.script = GENERATE.read_text(encoding="utf-8")

    def test_generation_requires_an_explicit_user_invocation(self):
        self.assertIn("명시적 호출 전용", self.text)
        self.assertIn("`/gpt-image-gen <이미지 설명>`", self.text)
        self.assertIn("`$gpt-image-gen <이미지 설명>`", self.text)
        self.assertIn("호스트 UI의 스킬 선택 기능", self.text)
        self.assertIn("사용량이 실제로 차감된다", self.text)

    def test_empty_prompt_asks_instead_of_guessing(self):
        self.assertIn("임의로 추측해 생성하지 말고", self.text)

    def test_any_host_agent_uses_the_script_adapter(self):
        self.assertIn("호스트 에이전트와 관계없이", self.text)
        self.assertIn("`codex exec` 명령을 직접 조립하지 말고", self.text)
        self.assertIn("`scripts/generate.sh`의 절대경로", self.text)
        self.assertIn('bash "<gpt-image-gen 스킬 절대경로>/scripts/generate.sh"', self.text)

    def test_unavailable_local_adapter_never_claims_generation(self):
        self.assertIn("스킬 파일 경로를 확인할 수 없거나 로컬 스크립트를 실행할 수 없으면", self.text)
        self.assertIn("생성됐다고 주장하지 않는다", self.text)

    def test_script_is_executable_and_reports_a_single_saved_path(self):
        self.assertTrue(GENERATE.is_file())
        self.assertTrue(os.stat(GENERATE).st_mode & stat.S_IXUSR)
        self.assertIn("set -euo pipefail", self.script)
        self.assertIn("echo \"SAVED ${ABS_OUT}\"", self.script)

    def test_parallel_calls_stay_isolated(self):
        self.assertIn('UNIQ="$$-${RANDOM}"', self.script)
        self.assertIn("/tmp/gpt-image-gen-${UNIQ}.log", self.script)

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

    def test_parallel_report_uses_only_the_exact_output_path(self):
        self.assertIn("공유 디렉터리에서 추측해 고르지 않고", self.text)

    def test_multiple_images_are_independent_single_image_calls(self):
        self.assertIn("독립 이미지 N장이 필요하면", self.text)
        self.assertIn("사용자가 독립 이미지 N장을\n   명시하면", self.text)
        self.assertIn("다시 확인하지 않고 진행한다", self.text)

    def test_codex_adapter_disables_implicit_invocation(self):
        metadata = OPENAI_YAML.read_text(encoding="utf-8")
        self.assertIn("allow_implicit_invocation: false", metadata)

    def test_lifecycle_registers_the_skill(self):
        config = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))
        entry = config["skills"]["gpt-image-gen"]
        self.assertEqual(entry["status"], "active")
        self.assertEqual(entry["providers"], ["claude", "codex", "gemini", "grok"])


class GptImageGenExecutionTests(unittest.TestCase):
    def run_generate(self, mode):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            bin_dir = work / "bin"
            bin_dir.mkdir()
            fake = bin_dir / "codex"
            fake.write_text(textwrap.dedent("""\
                #!/usr/bin/env python3
                import os
                from pathlib import Path
                import re
                import sys

                if sys.argv[1:3] == ["login", "status"]:
                    raise SystemExit(0)
                if sys.argv[1:3] == ["features", "list"]:
                    print("image_generation stable true")
                    raise SystemExit(0)
                if sys.argv[1:2] != ["exec"]:
                    raise SystemExit(2)
                if os.environ["FAKE_MODE"] == "exec_failure":
                    print("rate limit reached", file=sys.stderr)
                    raise SystemExit(9)
                match = re.search(r"Save it to exactly: (.+?) \\. Print only", sys.argv[-1])
                assert match
                exact = Path(match.group(1))
                mode = os.environ["FAKE_MODE"]
                if mode == "exact":
                    exact.write_bytes(b"\\x89PNG\\r\\n\\x1a\\nfixture")
                elif mode == "invalid_exact":
                    exact.write_bytes(b"not a png")
                elif mode in {"wrong_single", "wrong_multiple"}:
                    (exact.parent / "other.png").write_bytes(b"\\x89PNG\\r\\n\\x1a\\nother")
                    if mode == "wrong_multiple":
                        (exact.parent / "another.png").write_bytes(b"\\x89PNG\\r\\n\\x1a\\nanother")
            """), encoding="utf-8")
            fake.chmod(0o755)
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:{env['PATH']}"
            env["FAKE_MODE"] = mode
            return subprocess.run(
                ["bash", str(GENERATE), "fixture prompt"],
                cwd=work,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

    def test_exact_valid_png_is_reported(self):
        result = self.run_generate("exact")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"^SAVED .+/generated-images/img-.+\.png\n$")

    def test_single_png_at_another_path_is_not_misattributed(self):
        result = self.run_generate("wrong_single")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("SAVED", result.stdout)
        self.assertIn("이번 호출의 결과로 확정하지 않습니다", result.stderr)
        self.assertIn("로그 확인:", result.stderr)

    def test_multiple_pngs_at_other_paths_are_not_misattributed(self):
        result = self.run_generate("wrong_multiple")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("SAVED", result.stdout)

    def test_missing_output_is_an_error(self):
        result = self.run_generate("missing")
        self.assertEqual(result.returncode, 1)
        self.assertIn("지정 경로", result.stderr)

    def test_invalid_exact_file_is_an_error(self):
        result = self.run_generate("invalid_exact")
        self.assertEqual(result.returncode, 1)
        self.assertIn("PNG 시그니처와 데이터가 없습니다", result.stderr)

    def test_codex_failure_remains_an_error(self):
        result = self.run_generate("exec_failure")
        self.assertEqual(result.returncode, 1)
        self.assertIn("codex 실행 실패", result.stderr)
        self.assertIn("사용량이나 호출 한도", result.stderr)


if __name__ == "__main__":
    unittest.main()
