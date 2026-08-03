import json
from pathlib import Path
import unittest


ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills" / "conventional-commits" / "SKILL.md"


class ConventionalCommitsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8")

    def test_message_request_does_not_authorize_git_mutation(self):
        self.assertIn("메시지 작성 요청만으로 git commit·push를 실행하지 않는다", self.text)
        self.assertIn("별도 명시가 있을 때만 실행한다", self.text)
        self.assertIn("사용자가 현재 요청에서 명시적으로 커밋을 지시한 경우에만", self.text)

    def test_language_rules_preserve_identifiers_and_footers(self):
        self.assertIn("코드 식별자, 제품명, 파일 경로", self.text)
        self.assertIn("사람 이름과 이메일", self.text)
        self.assertIn("Co-Authored-By", self.text)

    def test_commit_execution_has_shared_worktree_guards(self):
        self.assertIn("공유 워킹트리에서 다른 에이전트가 작업 중이거나", self.text)
        self.assertIn("pathspec 오류의 stderr를 숨기지 않는다", self.text)
        self.assertIn("git show --stat --oneline HEAD", self.text)

    def test_lifecycle_registers_all_providers(self):
        config = json.loads((ROOT / "lifecycle.json").read_text(encoding="utf-8"))
        entry = config["skills"]["conventional-commits"]
        self.assertEqual(entry["status"], "active")
        self.assertEqual(entry["providers"], ["claude", "codex", "gemini", "grok"])


if __name__ == "__main__":
    unittest.main()
