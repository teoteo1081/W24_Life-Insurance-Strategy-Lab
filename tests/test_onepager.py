"""Bản tóm tắt 2 trang (scripts/build_onepager.py): số đọc từ snapshot, không gõ tay; không lộ đường dẫn máy."""
import json
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "scripts")]

import build_onepager as OP  # noqa: E402


class TestOnePager(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tables = json.loads(OP.SNAPSHOT.read_text(encoding="utf-8"))["tables"]
        cls.html = OP.render(cls.tables)

    def v(self, s, m, k=85):
        return next(float(r["value"]) for r in self.tables["roi_analysis"] if r["scheme"] == s and r["metric"] == m and int(r["k2"]) == k)

    def test_numbers_come_from_snapshot(self) -> None:
        for s in ("AIA", "Chubb", "Manulife", "Hybrid"):
            self.assertIn(OP.vn(self.v(s, "cost_pct_fyp")) + "%", self.html)
        self.assertIn(OP.vn(self.v("Hybrid", "cost_pct_fyp_worst_case")) + "%", self.html)
        be = next(float(r["value"]) for r in self.tables["roi_analysis"] if r["id"] == "Hybrid|breakeven_fyp_productivity_pct|AIA|mix4")
        self.assertIn("+" + OP.vn(be) + "%", self.html)

    def test_two_pages_and_clean(self) -> None:
        self.assertEqual(self.html.count('class=pb'), 1)                         # đúng 1 ngắt trang → 2 trang
        self.assertNotRegex(self.html, r"(?i)file://|[A-Z]:\\\\Users|nan%|inf%")
        self.assertNotIn("Chính sách Lai", self.html)
        self.assertFalse(re.search(r"\bTJ\b", self.html))


if __name__ == "__main__":
    unittest.main()
