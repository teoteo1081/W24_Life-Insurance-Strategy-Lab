"""Regression tests for fee tables re-checked against the source PDFs on 2026-11-27.

Each expected value is read directly from the cited page, not from the engine.
"""
from __future__ import annotations

import math
import unittest

from model.compensation.compensation_engine import (
    calc_aia_cql_12m,
    calc_chubb_al_12m,
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
            calc_chubb_al_12m([45.0] * 12, [5] * 12, k2_ntt=85.0, quarterly_ryc_ntt_y2_y5=[math.nan, 1.0, 1.0, 1.0])


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
