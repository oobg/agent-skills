import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "skills" / "feature-analysis" / "scripts" / "collect_inventory.py"
SPEC = importlib.util.spec_from_file_location("collect_inventory", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

FIXTURE = """<!doctype html>
<style>:root{--color-accent:#0059ee;--space-4:16px}</style>
<div data-view="list"><button data-action="reserve-cancel" onclick="noop()">취소</button></div>
<input id="q" oninput="filter()">
<script>
// 실제로는 LLM 호출 자리
const DB = [{id: 1, status: 'requested'}, {id: 2, status: 'confirmed'}];
function cancelReservation(id){ const r = DB.find(x => x.id === id); r.status = 'cancelled'; toast('취소'); }
document.addEventListener('click', e => { if (e.target.dataset.action === 'reserve-cancel') cancelReservation(1); });
localStorage.setItem('x', '1');
fetch('/api/reservations');
</script>
"""


class CollectInventoryTests(unittest.TestCase):
    def run_fixture(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        target = root / "proto.html"
        target.write_text(FIXTURE, encoding="utf-8")
        before = target.read_bytes()
        inv = MODULE.collect(target)
        self.assertEqual(before, target.read_bytes(), "target must not be modified")
        return tmp, inv

    def test_collects_each_category_with_file_line_evidence(self):
        tmp, inv = self.run_fixture()
        with tmp:
            matches = {k: [i["match"] for i in inv[k]] for k in ("routes", "events", "delegation_attrs", "state", "api", "side_effects", "stub_markers", "destructive_defs", "status_enums")}
            self.assertIn("list", matches["routes"])
            self.assertIn("click", matches["events"])
            self.assertIn("input", matches["events"])
            self.assertTrue(any(m.startswith("action") for m in matches["delegation_attrs"]))
            self.assertIn("DB", matches["state"])
            self.assertIn("fetch", matches["api"])
            self.assertIn("localStorage", matches["side_effects"])
            self.assertIn("toast", matches["side_effects"])
            self.assertIn("실제로는", matches["stub_markers"])
            self.assertIn("cancelReservation", matches["destructive_defs"])
            self.assertIn("status requested", matches["status_enums"])
            tokens = {t["token"]: t["first_value"] for t in inv["css_tokens"]}
            self.assertEqual(tokens["--color-accent"], "#0059ee")
            for key in ("routes", "events", "state", "api"):
                for item in inv[key]:
                    self.assertRegex(item["evidence"], r"^proto\.html:\d+$")

    def test_meta_records_kind_hash_time_and_inventory_disclaimer(self):
        tmp, inv = self.run_fixture()
        with tmp:
            meta = inv["meta"]
            self.assertEqual(meta["kind_guess"], "single-html")
            self.assertEqual(len(meta["sha256"]), 64)
            self.assertTrue(inv["run"]["generated_at"])
            self.assertEqual(meta["files_scanned"], 1)
            self.assertIn("inventory only", meta["note"])
            self.assertIn("inventory only", MODULE.summarize(inv))

    def test_inventory_is_deterministic_and_run_metadata_is_separate(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "proto.html"
            target.write_text(FIXTURE, encoding="utf-8")
            first = MODULE.collect(target)
            second = MODULE.collect(target)
            for inv in (first, second):
                self.assertIn("generated_at", inv["run"])
                self.assertNotIn("generated_at", inv["meta"])
                self.assertIn("zero_means", inv["meta"])
            first.pop("run")
            second.pop("run")
            self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_url_target_is_not_fetched(self):
        self.assertEqual(MODULE.main(["https://example.com"]), 2)

    def test_json_output_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.html").write_text(FIXTURE, encoding="utf-8")
            out = root / "inv.json"
            md = root / "inv.md"
            self.assertEqual(MODULE.main([str(root / "a.html"), "--json", str(out), "--md", str(md)]), 0)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertIn("meta", data)
            self.assertTrue(md.read_text(encoding="utf-8").startswith("# Inventory"))


if __name__ == "__main__":
    unittest.main()
