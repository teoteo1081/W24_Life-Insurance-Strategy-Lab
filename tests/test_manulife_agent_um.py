"""Manulife agent (0046M01/2026/ASBD) and UM+ (0047M01/2026/ASBD) — expected values hand-computed from the cited pages."""
from __future__ import annotations

import math
import unittest

from model.compensation.compensation_engine import (
    K2_NO_K2_YET,
    calc_manulife_agent_12m,
    calc_manulife_um_12m,
    manulife_agent_k2_factor,
)


class TestManulifeAgentK2(unittest.TestCase):
    """0046M01 p.1 muc A.I."""

    def test_two_phases(self) -> None:
        for k2, before, after in [(85, 1.00, 1.00), (68, 1.00, 0.90), (62, 0.75, 0.70), (56, 0.75, 0.50), (45, 0.50, 0.225), (30, 0.30, 0.15)]:
            with self.subTest(k2=k2):
                self.assertAlmostEqual(manulife_agent_k2_factor(k2, 3), before)
                self.assertAlmostEqual(manulife_agent_k2_factor(k2, 4), after)
        self.assertEqual(manulife_agent_k2_factor(K2_NO_K2_YET, 6), 1.0)
        with self.assertRaises(ValueError):
            manulife_agent_k2_factor(None, 6)


class TestManulifeAgent(unittest.TestCase):
    def test_monthly_tier_p4(self) -> None:
        # FYC 9/thang, 3 thang = 27 -> Muc 3 (>=15tr) 15%; >6 thang lam viec -> 9 x 15% x 1.0 = 1.35/thang
        r = calc_manulife_agent_12m([9.0] * 12, [30.0] * 12, [1] * 12, k2=85.0)
        self.assertAlmostEqual(r["bonus_monthly_productivity"], 1.35 * 12, places=6)
        # Quy: FYC quy 27 < 30 (Muc 1 chi cho <=6 thang) -> 0 [p.5]
        self.assertAlmostEqual(r["bonus_quarterly_productivity"], 0.0)
        # M-Star: FYP luy ke Q1 = 90 < 90% x 160 -> 0 [p.7]
        self.assertAlmostEqual(r["bonus_mstar_quarterly"] + r["bonus_mstar_annual"], 0.0)

    def test_no_contract_no_monthly_bonus(self) -> None:
        r = calc_manulife_agent_12m([9.0] * 12, [30.0] * 12, [0] * 12, k2=85.0)
        self.assertAlmostEqual(r["bonus_monthly_productivity"], 0.0)

    def test_quarterly_excellent_doubles_p5_p6(self) -> None:
        # FYC 20/thang: 3T = 60 -> Muc 6 30%; quy 60 -> Muc 4 5%, dai ly xuat sac (thuong thang 3 thang lien) -> 10%
        r = calc_manulife_agent_12m([20.0] * 12, [60.0] * 12, [1] * 12, k2=85.0)
        self.assertAlmostEqual(r["bonus_monthly_productivity"], 20 * 0.30 * 12, places=6)
        self.assertAlmostEqual(r["bonus_quarterly_productivity"], 60 * 0.10 * 4, places=6)

    def test_mstar_p7_p8(self) -> None:
        # FYP 100/thang: Q1 300 >= 160 -> 8; Q2 600 >= 430 -> 12; Q3 900 >= 750 -> 15; Q4 1200 >= 1073.6 -> 20; nam 55 - 55 = 0
        r = calc_manulife_agent_12m([30.0] * 12, [100.0] * 12, [1] * 12, k2=85.0)
        self.assertAlmostEqual(r["bonus_mstar_quarterly"], 55.0)
        self.assertAlmostEqual(r["bonus_mstar_annual"], 0.0)

    def test_kdxs_only_for_pro_titles_p6(self) -> None:
        none = calc_manulife_agent_12m([30.0] * 12, [100.0] * 12, [2] * 12, k2=85.0)
        gold = calc_manulife_agent_12m([30.0] * 12, [100.0] * 12, [2] * 12, k2=85.0, pro_title="Vang")
        self.assertEqual(none["bonus_annual_kdxs_deferred_50_30_20"], 0.0)
        self.assertAlmostEqual(gold["bonus_annual_kdxs_deferred_50_30_20"], 36.0)   # 10% x 360 FYC

    def test_rejects_bad_inputs(self) -> None:
        with self.assertRaises(ValueError):
            calc_manulife_agent_12m([math.nan] + [9.0] * 11, [30.0] * 12, [1] * 12, k2=85.0)
        with self.assertRaises(ValueError):
            calc_manulife_agent_12m([9.0] * 12, [30.0] * 12, [1] * 12, k2=85.0, pro_title="Gold")


class TestManulifeUM(unittest.TestCase):
    def test_a1_levels_p1(self) -> None:
        # Cap 1 = 45 FYC -> 16%; cap 2 = 90 -> 8%; cap 3 = 160 -> 4%  => 7.2 + 7.2 + 6.4 = 20.8/thang
        r = calc_manulife_um_12m([(45.0, 90.0, 160.0, 0.0)] * 12, [5] * 12, [0.0] * 12, 85.0)
        self.assertAlmostEqual(r["a1_team_productivity"], 20.8 * 12, places=6)

    def test_a2_activity_p2(self) -> None:
        # 5 DL san xuat -> 50% (UM+ khac); thuong co so 6.75; he so TLDTHD 85%: 115% (T1-3), 110% (T4-12)
        r = calc_manulife_um_12m([(45.0, 0, 0, 0)] * 12, [5] * 12, [6.75] * 12, 85.0)
        self.assertAlmostEqual(r["a2_team_activity"], 0.5 * 6.75 * (1.15 * 3 + 1.10 * 9), places=3)  # engine rounds to 4 dp
        self.assertEqual(r["a5_long_term_deferred_30_30_40"], 0.0)   # khong co danh hieu MBA Pro

    def test_mba_pro_and_long_term_p5(self) -> None:
        r = calc_manulife_um_12m([(45.0, 0, 0, 0)] * 12, [6] * 12, [10.0] * 12, K2_NO_K2_YET, mba_pro_title="Vang")
        self.assertAlmostEqual(r["a2_team_activity"], 1.25 * 10.0 * 12, places=6)
        self.assertAlmostEqual(r["a5_long_term_deferred_30_30_40"], 1.00 * 1.25 * 10.0 * 12, places=6)

    def test_attendance_gate_p3(self) -> None:
        r = calc_manulife_um_12m([(45.0, 0, 0, 0)] * 12, [5] * 12, [6.75] * 12, 85.0, attendance_ok=False)
        self.assertEqual(r["total_earned"], 0.0)

    def test_unknown_k2_raises(self) -> None:
        with self.assertRaises(ValueError):
            calc_manulife_um_12m([(45.0, 0, 0, 0)] * 12, [5] * 12, [6.75] * 12, None)


if __name__ == "__main__":
    unittest.main()
