"""Trang 'Hai góc nhìn' (scripts/build_two_lens.py): khung chuẩn, số khớp mô hình, thuế tính 2 cách, bản công khai không lộ số mật."""
import json
import math
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "scripts")]

import build_two_lens as TL  # noqa: E402


class TestTwoLens(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.d = TL.compute()

    def test_same_questions_for_every_scheme(self) -> None:
        self.assertEqual(len(self.d["six_questions"]), 6)
        for s, x in self.d["schemes"].items():
            self.assertEqual(len(x["six"]), 6, s)
            self.assertEqual([r["group"] for r in x["income"]], ["Thấp", "Nòng cốt", "Top / MDRT"], s)

    def test_insurer_answers_cite_pages(self) -> None:
        cite = re.compile(r"\[[^\]:]+ : \d+(?:-\d+)?\]")
        for s in ("AIA", "Chubb", "Manulife"):
            for i, cell in enumerate(self.d["schemes"][s]["six"]):
                with self.subTest(s=s, q=i + 1):
                    self.assertRegex(cell, cite)
        for cell in self.d["schemes"]["Hybrid"]["six"]:
            self.assertTrue("PROPOSAL" in cell or "ASSUMPTION" in cell, cell)   # đề xuất: mọi ô phải gắn nhãn, không giả làm sự thật

    def test_tax_both_readings(self) -> None:
        self.assertEqual(TL.tax_year(900.0), {"excess_reading": 0.0, "full_reading": 0.0})
        t = TL.tax_year(1200.0)
        self.assertAlmostEqual(t["excess_reading"], 10.0)      # 5% × 200
        self.assertAlmostEqual(t["full_reading"], 60.0)        # 5% × 1.200
        for x in self.d["schemes"].values():
            for r in x["income"]:
                lo, hi = r["after_tax_month"]
                self.assertLessEqual(lo, hi)
                self.assertTrue(math.isfinite(lo) and math.isfinite(hi))

    def test_numbers_match_phase2_and_bench_has_sources(self) -> None:
        import build_phase2 as P
        import model.compensation.hybrid_scheme as H
        base = H.song_hanh_params()
        for s, x in self.d["schemes"].items():
            r = x["income"][1]
            self.assertAlmostEqual(r["year"], round(P.agent(s, r["fyp_month"], 85.0, base)["total"], 2))
            self.assertAlmostEqual(sum(it["year"] for it in x["items"]), x["items_total"], delta=0.05)
        for k in ("min_wage", "avg_income", "tax"):
            self.assertEqual(self.d["bench"][k]["label"], "SOURCE_CLAIM")
            self.assertTrue(self.d["bench"][k]["source"])

    def test_public_view_drops_confidential(self) -> None:
        self.assertIn("Manulife", TL.public_view(self.d)["schemes"])          # DEC-21: 9 PDF như nhau
        x = json.loads(json.dumps(self.d))
        x["schemes"]["Chubb"]["confidentiality"] = "restricted"              # cơ chế lọc vẫn hoạt động nếu sau này có tài liệu mật
        self.assertNotIn("Chubb", TL.public_view(x)["schemes"])


if __name__ == "__main__":
    unittest.main()
