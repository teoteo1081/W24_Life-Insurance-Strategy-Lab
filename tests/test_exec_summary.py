"""Tóm tắt nhanh 2 góc nhìn (scripts/build_exec_summary.py): chỉ tổng hợp số engine, không tính lại; bản công khai không có dòng mật."""
from __future__ import annotations

import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import build_exec_summary as ES  # noqa: E402

TABLES = json.loads((REPO / "web/data/snapshot.json").read_text(encoding="utf-8"))["tables"]
PUBLIC = {k: [r for r in v if r.get("confidentiality") != "restricted"] for k, v in TABLES.items()}


class TestExecSummary(unittest.TestCase):
    def setUp(self) -> None:
        self.full, self.pub = ES.build(TABLES), ES.build(PUBLIC)

    def test_public_has_no_restricted_rows(self) -> None:
        for part in ("agent", "company"):
            self.assertEqual([r for r in self.pub[part] if r["confidentiality"] == "restricted"], [], part)
        self.assertEqual({r["scheme"] for r in self.pub["company"]}, {"AIA", "Chubb", "Hybrid"})
        self.assertTrue(any(r["scheme"] == "Manulife" and r["milestone_id"] == "M4" for r in self.pub["agent"]))   # PSM/SM 0048M01 vẫn công khai
        md = ES.to_markdown(self.pub, full=False)
        for token in ("0046M01", "0047M01", "UM+"):
            self.assertNotIn(token, md)

    def test_full_has_four_tiers_by_four_schemes(self) -> None:
        self.assertEqual(len(self.full["agent"]), 16)
        self.assertEqual([r["scheme"] for r in self.full["company"]], ["AIA", "Chubb", "Manulife", "Hybrid"])

    def test_numbers_are_aggregates_of_engine_values(self) -> None:
        roi = {(r["scheme"], r["metric"], int(r["k2"])): r["value"] for r in TABLES["roi_analysis"]}
        for r in self.full["company"]:
            with self.subTest(s=r["scheme"]):
                self.assertAlmostEqual(r["cost_pct"], roi[(r["scheme"], "cost_pct_fyp", 85)])
                self.assertAlmostEqual(r["year"], round(r["cost_pct"] / 100 * ES.ORG_FYP_Y, 1), places=1)
                self.assertGreaterEqual(r["peak_pct"], r["cost_pct"])
        bench = {(b["milestone_id"], b["company"]): b["income_vnd_m_month"] for b in TABLES["benchmark_results"] if b["comparison"] == "primary"}
        for r in self.full["agent"]:
            with self.subTest(t=r["tier"], s=r["scheme"]):
                self.assertTrue(all(math.isfinite(r[k]) for k in ("month", "quarter", "year")))
                self.assertAlmostEqual(r["year"], round(r["month"] * 12, 1), delta=0.7)   # làm tròn 1 chữ số
                if r["scheme"] != "Hybrid":
                    self.assertAlmostEqual(r["month"], round(bench[(r["milestone_id"], r["scheme"])], 1))

    def test_verdict_rule(self) -> None:
        v = {(r["milestone_id"], r["scheme"]): r["verdict"] for r in self.full["agent"]}
        self.assertTrue(v[("M2", "AIA")].startswith("Không thơm"))        # quản lý thu ít hơn tự bán (behavior_traps)
        self.assertEqual(v[("M2", "Chubb")], "Thơm")
        self.assertEqual(v[("M4", "Hybrid")], "Thấp hơn cả các hãng")       # lãnh đạo Lai thấp hơn mọi hãng — công bố, không giấu

    def test_full_copy_must_be_outside_repo(self) -> None:
        with self.assertRaises(SystemExit):
            ES.main(["--full-out", str(REPO / "outputs" / "x.md")])
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(ES.main(["--full-out", str(Path(d) / "full.md")]), 0)
            self.assertIn("Manulife · UM+", (Path(d) / "full.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
