"""Chính sách Lai VN 2026 (PROPOSAL) — model/compensation/hybrid_scheme.py và scripts/build_phase2.py."""
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from model.compensation import hybrid_scheme as H  # noqa: E402

BASE = H.song_hanh_params()


class TestHybridRules(unittest.TestCase):
    def test_region_coefficients_inside_tj_ranges(self) -> None:
        self.assertEqual(H.REGIONS["V1"]["coef"], 1.0)
        self.assertTrue(0.80 <= H.REGIONS["V2"]["coef"] <= 0.85)
        self.assertTrue(0.65 <= H.REGIONS["V3"]["coef"] <= 0.70)

    def test_full_time_allowance_gates(self) -> None:
        ok = H.hybrid_agent_12m(30, 2, 85.0, "V1", "FULL_TIME", BASE)
        self.assertEqual(ok["allowance_fixed"], H.FT_ALLOWANCE_MONTH * 12)
        self.assertEqual(H.hybrid_agent_12m(29.9, 2, 85.0, "V1", "FULL_TIME", BASE)["allowance_fixed"], 0)   # dưới quota
        self.assertEqual(H.hybrid_agent_12m(30, 1, 85.0, "V1", "FULL_TIME", BASE)["allowance_fixed"], 0)     # thiếu số HĐ
        self.assertEqual(H.hybrid_agent_12m(30, 2, 79.9, "V1", "FULL_TIME", BASE)["allowance_fixed"], 0)     # K2 < 80
        self.assertEqual(H.hybrid_agent_12m(30, 2, 85.0, "V1", "PART_TIME", BASE)["allowance_fixed"], 0)     # Part-time

    def test_regional_quota_keeps_cc_and_k2(self) -> None:
        v3 = H.hybrid_agent_12m(20.25, 2, 85.0, "V3", "FULL_TIME", BASE)
        self.assertTrue(v3["quota_met"])
        self.assertFalse(H.hybrid_agent_12m(20.25, 1, 85.0, "V3", "FULL_TIME", BASE)["quota_met"])
        self.assertFalse(H.hybrid_agent_12m(20.25, 2, 79.0, "V3", "FULL_TIME", BASE)["quota_met"])

    def test_part_time_earns_less_than_full_time(self) -> None:
        ft = H.hybrid_agent_12m(30, 2, 85.0, "V1", "FULL_TIME", BASE)
        pt = H.hybrid_agent_12m(30, 2, 85.0, "V1", "PART_TIME", BASE)
        self.assertLess(pt["bonuses"], ft["bonuses"])

    def test_deferred_vesting_ramp(self) -> None:
        f = lambda k2: H.hybrid_manager_12m(40, (), (), k2, "V1", BASE)["deferred_3y"]
        full = f(85.0)
        self.assertGreater(full, 0)
        self.assertEqual(f(80.0), full)                       # deferred không phụ thuộc K2 khi ≥80
        self.assertAlmostEqual(f(77.0), f(80.0) * 0.5, 4)                 # PROPOSAL: 75–<80% nhận 50%
        self.assertEqual(f(74.9), 0.0)

    def test_flat_team_cap(self) -> None:
        small = H.hybrid_manager_12m(60.0, (), (), 85.0, "V1", BASE)["direct_override"]
        big = H.hybrid_manager_12m(120.0, (), (), 85.0, "V1", BASE)["direct_override"]
        self.assertAlmostEqual(big, small * 1.5, 3)                         # PROPOSAL: phần vượt 60tr FYC nhận 50%

    def test_leader_deferred_forfeited_below_ramp(self) -> None:
        hi = H.hybrid_leader_12m(1200, 360, 85.0, "V1", BASE)
        lo = H.hybrid_leader_12m(1200, 360, 70.0, "V1", BASE)
        self.assertEqual(lo["deferred_3y"], 0.0)
        self.assertLess(lo["total_earned"], hi["total_earned"])
        self.assertEqual(H.hybrid_leader_12m(250, 75, 85.0, "V1", BASE)["base_fixed"], 0.0)   # < 30% chỉ tiêu

    def test_rejects_non_finite_and_bad_region(self) -> None:
        for bad in (float("nan"), float("inf"), -float("inf"), "30"):
            with self.subTest(bad=bad), self.assertRaises((ValueError, TypeError)):
                H.hybrid_agent_12m(bad, 2, 85.0, "V1", "FULL_TIME", BASE)
            with self.subTest(mgr=bad), self.assertRaises((ValueError, TypeError)):
                H.hybrid_manager_12m(bad, (), (), 85.0, "V1", BASE)
        with self.assertRaises(ValueError):
            H.hybrid_agent_12m(30, 2, 85.0, "V4", "FULL_TIME", BASE)
        with self.assertRaises(ValueError):
            H.hybrid_agent_12m(30, 2, 85.0, "V1", "SOMETIMES", BASE)


class TestPhase2Outputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        import build_phase2 as P2
        cls.P2 = P2
        cls.d = P2.compute()

    def test_cost_cap_75_pct(self) -> None:
        self.assertTrue(self.d["cost_cap_ok"])
        self.assertLessEqual(self.d["org"]["Hybrid"]["k85"]["cost_pct"], H.COST_CAP_PCT_FYP)

    def test_all_numbers_finite(self) -> None:
        for tbl in ("roi", "traps", "rubric", "regional"):
            for r in self.d[tbl]:
                for v in r.values():
                    if isinstance(v, float):
                        with self.subTest(tbl=tbl, id=r["id"]):
                            self.assertTrue(math.isfinite(v))

    def test_rubric_weights_and_range(self) -> None:
        for s in self.P2.SCHEMES:
            rows = [r for r in self.d["rubric"] if r["scheme"] == s]
            self.assertEqual(len(rows), 5)
            self.assertAlmostEqual(sum(r["weight"] for r in rows), 1.0)
            for r in rows:
                self.assertTrue(1 <= r["score"] <= 5)
        self.assertEqual([r["weight"] for r in self.d["rubric"] if r["scheme"] == "AIA"], [0.25, 0.25, 0.20, 0.15, 0.15])

    def test_k2_collapse_reduces_payout(self) -> None:
        for s in self.P2.SCHEMES:
            with self.subTest(s=s):
                self.assertLess(self.d["org"][s]["k65"]["total"], self.d["org"][s]["k85"]["total"])

    def test_dec14_manulife_rows_restricted_hybrid_labelled_proposal(self) -> None:
        for tbl in ("roi", "traps", "rubric"):
            for r in self.d[tbl]:
                if r["scheme"] == "Manulife":
                    self.assertEqual(r["confidentiality"], "restricted", r["id"])
                if r["scheme"] == "Hybrid":
                    self.assertEqual(r["label"], "PROPOSAL", r["id"])
        self.assertTrue(all(r["label"] == "PROPOSAL" for r in self.d["regional"]))

    def test_reports_written_and_pass_rubric(self) -> None:
        for p in (self.P2.OUT02, self.P2.OUT03):
            txt = p.read_text(encoding="utf-8")
            self.assertIn("**PASS** (ngưỡng 90)", txt)
            self.assertNotRegex(txt, r"\b(nan|inf)\b")
        self.assertIn("KHÔNG phải ROI thực tế", self.P2.OUT02.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
