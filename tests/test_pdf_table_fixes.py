"""Regression tests for fee tables re-checked against the source PDFs on 2026-11-27.

Each expected value is read directly from the cited page, not from the engine.
"""
from __future__ import annotations

import math
import unittest

from model.compensation.compensation_engine import (
    K2_NO_K2_YET,
    calc_aia_cql_12m,
    calc_chubb_al_12m,
    calc_chubb_al_htktn_month,
    calc_chubb_rd_12m,
    rd_growth_rate,
)


def _rd(ehc: int = 0, fyp: float = 0.0, **kw):
    """Chubb RD with one constant month repeated 12 times; FYC 0 isolates the fixed-amount fees."""
    return calc_chubb_rd_12m([fyp] * 12, [0.0] * 12, [ehc] * 12, [0] * 12, [0.0] * 12, k2_pct=80.0, **kw)


class TestChubbRdFixedTables(unittest.TestCase):
    """CHH0DCEB260003V p.6 (scan): activity fee by EHC, business fee by monthly FYP."""

    def test_activity_fee_by_ehc(self) -> None:
        # (EHC, fee per month, million VND)
        for ehc, fee in [(25, 8.0), (20, 8.0), (19, 6.5), (16, 6.5), (15, 5.0), (12, 5.0),
                         (11, 3.5), (9, 3.5), (8, 2.5), (6, 2.5), (5, 1.5), (4, 1.5), (3, 0.0), (0, 0.0)]:
            with self.subTest(ehc=ehc):
                self.assertAlmostEqual(_rd(ehc=ehc)["activity_12m"], fee * 12, places=6)

    def test_business_fee_by_fyp(self) -> None:
        for fyp, fee in [(700, 12.0), (600, 12.0), (599, 9.5), (480, 9.5), (479, 7.0), (360, 7.0),
                         (359, 5.0), (270, 5.0), (269, 3.5), (180, 3.5), (179, 2.5), (120, 2.5), (119, 0.0)]:
            with self.subTest(fyp=fyp):
                self.assertAlmostEqual(_rd(fyp=fyp)["business_12m"], fee * 12, places=6)


class TestChubbRdGrowthRate(unittest.TestCase):
    """CHH0DCEB260003V p.8 (scan): 12-level growth table and the two notes under it."""

    def test_growth_levels(self) -> None:
        prev = 1000.0
        for growth, rate in [(0.60, 0.275), (0.50, 0.275), (0.47, 0.25), (0.45, 0.25), (0.42, 0.225),
                             (0.37, 0.20), (0.32, 0.175), (0.27, 0.15), (0.22, 0.125), (0.17, 0.10),
                             (0.15, 0.10), (0.12, 0.075), (0.07, 0.05), (0.05, 0.05), (0.02, 0.025),
                             (0.0, 0.025), (-0.01, 0.0), (-0.30, 0.0)]:
            with self.subTest(growth=growth):
                self.assertAlmostEqual(rd_growth_rate(prev * (1 + growth), prev), rate, places=9)

    def test_notes(self) -> None:
        self.assertEqual(rd_growth_rate(300.0, 100.0), 0.025)   # <360M, positive growth -> 2.5%
        self.assertEqual(rd_growth_rate(300.0, 400.0), 0.0)     # <360M but negative growth -> table (0%)
        self.assertEqual(rd_growth_rate(400.0, 0.0), 0.10)      # >=360M, no comparison quarter -> 10%
        self.assertEqual(rd_growth_rate(400.0, -5.0), 0.10)

    def test_rejects_non_finite(self) -> None:
        for bad in (math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError):
                rd_growth_rate(bad, 100.0)


class TestChubbAlQuarterlyBand(unittest.TestCase):
    """CHH0DCEB260008V p.6: quarterly HT KTN rate 'Từ 50 đến dưới 75' = 40%."""

    def test_q_fyc_50_to_55_gets_40pct(self) -> None:
        fyc_m = 52.0 / 3.0  # quarterly NTT FYC = 52
        r = calc_chubb_al_12m([fyc_m] * 12, [4] * 12, k2_ntt=75.0)
        self.assertAlmostEqual(r["ht_ktn_quarterly"], r["ht_ktn_monthly"] * 0.40, places=3)


class TestChubbAlPersistencyFee(unittest.TestCase):
    """CHH0DCEB260008V p.9-10 (CHB-MG-008): RYC NTT x 10% (3MAA 2-4) / 15% (>=5), K2 NTT >=65%, tenure >=13M."""

    def test_rates_and_gates(self) -> None:
        base = dict(monthly_fyc_ntt=[45.0] * 12, monthly_ehc_ntt=[5] * 12, al_tenure_start=15)
        ryc = [30.0] * 4
        self.assertAlmostEqual(calc_chubb_al_12m(**base, k2_ntt=85.0, quarterly_ryc_ntt_y2_y5=ryc,
                                                 quarterly_3maa_ntt=[5] * 4)["persistency_ryc_quarterly"], 18.0)
        self.assertAlmostEqual(calc_chubb_al_12m(**base, k2_ntt=85.0, quarterly_ryc_ntt_y2_y5=ryc,
                                                 quarterly_3maa_ntt=[3] * 4)["persistency_ryc_quarterly"], 12.0)
        self.assertAlmostEqual(calc_chubb_al_12m(**base, k2_ntt=85.0, quarterly_ryc_ntt_y2_y5=ryc,
                                                 quarterly_3maa_ntt=[1] * 4)["persistency_ryc_quarterly"], 0.0)
        self.assertAlmostEqual(calc_chubb_al_12m(**base, k2_ntt=64.9, quarterly_ryc_ntt_y2_y5=ryc,
                                                 quarterly_3maa_ntt=[5] * 4)["persistency_ryc_quarterly"], 0.0)

    def test_default_unchanged(self) -> None:
        r = calc_chubb_al_12m([45.0] * 12, [5] * 12, k2_ntt=85.0)
        self.assertEqual(r["persistency_ryc_quarterly"], 0.0)

    def test_rejects_non_finite_ryc(self) -> None:
        with self.assertRaises(ValueError):
            calc_chubb_al_12m([45.0] * 12, [5] * 12, k2_ntt=85.0, quarterly_ryc_ntt_y2_y5=[math.nan, 1.0, 1.0, 1.0],
                              quarterly_3maa_ntt=[5] * 4)

    def test_missing_3maa_is_missing_input_not_zero(self) -> None:
        # Audit P2 #1: RYC without 3MAA used to return 0 fee silently.
        with self.assertRaisesRegex(ValueError, "MISSING_INPUT"):
            calc_chubb_al_12m([45.0] * 12, [5] * 12, k2_ntt=85.0, quarterly_ryc_ntt_y2_y5=[30.0] * 4)
        with self.assertRaisesRegex(ValueError, "MISSING_INPUT"):
            calc_chubb_al_12m([45.0] * 12, [5] * 12, k2_ntt=85.0, quarterly_3maa_ntt=[5] * 4)


class TestChubbAlK2Status(unittest.TestCase):
    """Audit P2 #2: NO_K2_YET (0008V p.5: factor 100%; p.10: counts as met) vs None = UNKNOWN."""

    BASE = dict(monthly_fyc_ntt=[45.0] * 12, monthly_ehc_ntt=[5] * 12, al_tenure_start=15)

    def test_no_k2_yet_runs_end_to_end_for_15_month_manager(self) -> None:
        r = calc_chubb_al_12m(**self.BASE, k2_ntt=K2_NO_K2_YET,
                              quarterly_ryc_ntt_y2_y5=[30.0] * 4, quarterly_3maa_ntt=[5] * 4)
        # Monthly: 45 x 60% (>=40M, EHC>=4, >=15M tenure, p.5) x 100% (no K2 yet, p.5) = 27.0 / month
        self.assertAlmostEqual(r["ht_ktn_monthly"], 27.0 * 12, places=6)
        # Persistency: no K2 yet counts as met (p.10): 30 x 15% x 4 quarters = 18.0
        self.assertAlmostEqual(r["persistency_ryc_quarterly"], 18.0, places=6)

    def test_no_k2_yet_differs_from_observed_k2(self) -> None:
        r_obs = calc_chubb_al_12m(**self.BASE, k2_ntt=85.0)
        self.assertAlmostEqual(r_obs["ht_ktn_monthly"], 45.0 * 0.60 * 1.20 * 12, places=6)

    def test_none_is_unknown_and_raises(self) -> None:
        for tenure in (5, 15):
            with self.subTest(tenure=tenure), self.assertRaisesRegex(ValueError, "UNKNOWN"):
                calc_chubb_al_12m([45.0] * 12, [5] * 12, k2_ntt=None, al_tenure_start=tenure)
        with self.assertRaisesRegex(ValueError, "UNKNOWN"):
            calc_chubb_al_htktn_month(45.0, 5, None, 15)

    def test_unknown_status_string_rejected(self) -> None:
        with self.assertRaises(ValueError):
            calc_chubb_al_12m(**self.BASE, k2_ntt="N/A")


class TestAiaCqlIndirectLevels(unittest.TestCase):
    """AIAV/AD/2601-034 p.4 (muc III): indirect 50% / 25% / 12.5% for sub-CQL level 2 / 3 / 4."""

    def test_gen3_gen4(self) -> None:
        kw = dict(monthly_team_fyc=[0.0] * 12, monthly_active_count=[0] * 12, fy_pct=85.0)
        r = calc_aia_cql_12m(**kw, indirect_gen2_base_12m=100.0, indirect_gen3_base_12m=100.0, indirect_gen4_base_12m=100.0)
        self.assertAlmostEqual(r["indirect_fee"], 50.0 + 25.0 + 12.5)

    def test_rejects_non_finite(self) -> None:
        with self.assertRaises(ValueError):
            calc_aia_cql_12m([0.0] * 12, [0] * 12, 85.0, indirect_gen3_base_12m=math.inf)


if __name__ == "__main__":
    unittest.main()


class TestAiaStarRecruitBoundaries(unittest.TestCase):
    """Codex P2 (2543e02): ranh giới người mới cho danh hiệu CQL Ngoại hạng quý [AIAVAD 2601-034 : 4-5].

    3 sao: >=1 người mới mọi quý. 4–5 sao: >=1 ở Q1/2026, >=2 từ Q2/2026. Tỷ lệ 5/8/15% FYC quý nhóm trực tiếp.
    Không đạt bậc cao vì thiếu người mới thì rơi xuống bậc thấp hơn nếu đủ điều kiện bậc đó.
    """

    def q(self, fyc_month: float, active_month: int, recruits):
        r = calc_aia_cql_12m([fyc_month] * 12, [active_month] * 12, fy_pct=85.0, tot_pct=85.0, quarterly_new_recruits=recruits)
        return r["premier_quarterly"]

    def test_three_star_needs_one_new_agent_every_quarter(self) -> None:
        # FYC quý 60 (>=50), lượt hoạt động 6 (>=6) -> 3 sao 5% = 3.0 mỗi quý
        self.assertAlmostEqual(self.q(20.0, 2, [1, 1, 1, 1]), 3.0 * 4, places=6)
        self.assertAlmostEqual(self.q(20.0, 2, [0, 0, 0, 0]), 0.0, places=6)
        self.assertAlmostEqual(self.q(20.0, 2, [1, 0, 1, 0]), 3.0 * 2, places=6)

    def test_four_star_needs_one_in_q1_two_from_q2(self) -> None:
        # FYC quý 90 (>=80), lượt 9 (>=9): Q1 với 1 người -> 4 sao 8% = 7.2; Q2–Q4 với 1 người -> rơi xuống 3 sao 5% = 4.5
        self.assertAlmostEqual(self.q(30.0, 3, [1, 1, 1, 1]), 7.2 + 4.5 * 3, places=6)
        self.assertAlmostEqual(self.q(30.0, 3, [1, 2, 2, 2]), 7.2 * 4, places=6)

    def test_five_star_needs_one_in_q1_two_from_q2(self) -> None:
        # FYC quý 180 (>=170), lượt 15 (>=14): Q1 với 1 người -> 5 sao 15% = 27; Q2–Q4 với 1 người -> 3 sao 5% = 9
        self.assertAlmostEqual(self.q(60.0, 5, [1, 1, 1, 1]), 27.0 + 9.0 * 3, places=6)
        self.assertAlmostEqual(self.q(60.0, 5, [1, 2, 2, 2]), 27.0 * 4, places=6)


class TestManulifeCashTiming(unittest.TestCase):
    """Codex P2 (2543e02): M-Star năm trả kỳ thu nhập tháng 2 năm sau [0046M01_2026 : 8] — không thuộc tiền thực trả năm hiện tại."""

    def test_mstar_annual_excluded_from_cash_paid_y1(self) -> None:
        from model.compensation.compensation_engine import calc_manulife_agent_12m
        # FYP 200/tháng: M-Star quý 8+12+15+20 = 55; năm FYP 2.400 >= 2 tỷ -> 75 - 55 = 20 (trả tháng 2 năm sau)
        r = calc_manulife_agent_12m([60.0] * 12, [200.0] * 12, [1] * 12, k2=85.0)
        self.assertAlmostEqual(r["bonus_mstar_quarterly"], 55.0)
        self.assertAlmostEqual(r["bonus_mstar_annual"], 20.0)
        self.assertAlmostEqual(r["paid_next_years"], 20.0)
        self.assertAlmostEqual(r["total_earned"] - r["cash_paid_y1"], 20.0, places=4)

    def test_kdxs_and_mstar_both_deferred(self) -> None:
        from model.compensation.compensation_engine import calc_manulife_agent_12m
        r = calc_manulife_agent_12m([60.0] * 12, [200.0] * 12, [2] * 12, k2=85.0, pro_title="Vang")
        self.assertAlmostEqual(r["paid_next_years"], r["bonus_mstar_annual"] + r["bonus_annual_kdxs_deferred_50_30_20"], places=4)
        self.assertAlmostEqual(r["total_earned"] - r["cash_paid_y1"], r["paid_next_years"], places=4)
