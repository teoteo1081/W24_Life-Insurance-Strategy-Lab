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

    def test_allowance_scales_with_region(self) -> None:
        self.assertAlmostEqual(H.hybrid_agent_12m(20.25, 2, 85.0, "V3", "FULL_TIME", BASE)["allowance_fixed"], 3.0 * 0.675 * 12, 6)
        self.assertAlmostEqual(H.hybrid_agent_12m(24.75, 2, 85.0, "V2", "FULL_TIME", BASE)["allowance_fixed"], 3.0 * 0.825 * 12, 6)

    def test_all_agent_thresholds_scale_with_region(self) -> None:
        # Codex P2 (9dea455): V3 FYC năm 360tr ≥ MDRT vùng 270tr → phải có thưởng MDRT; ở V1 (ngưỡng 400) thì không
        from model.compensation.compensation_engine import ProposalParams, calc_proposal_agent_12m
        d = ProposalParams()
        self.assertEqual((d.agent_q_consistency_min_fyc, d.agent_mdrt_fyc_threshold, d.agent_onboarding_min_fyc), (4.0, 400.0, 8.0))   # mặc định = hành vi cũ
        v3 = H.regional_params(BASE, "V3", "FULL_TIME")
        self.assertAlmostEqual(v3.agent_mdrt_fyc_threshold, 270.0)
        self.assertAlmostEqual(v3.agent_q_consistency_min_fyc, 2.7)
        self.assertAlmostEqual(v3.agent_onboarding_min_fyc, 5.4)
        fyp = 360 / 12 / 0.30
        r3 = H.hybrid_agent_12m(fyp, 2, 85.0, "V3", "FULL_TIME", BASE)
        r1 = H.hybrid_agent_12m(fyp, 2, 85.0, "V1", "FULL_TIME", BASE)
        self.assertGreater(r3["paid_next_years"], 0.0)          # 30% MDRT trả chậm → có MDRT
        self.assertEqual(r1["paid_next_years"], 0.0)
        # ngưỡng nhất quán: FYC 3,5tr/tháng ở V3 (≥ bậc 1 vùng 3,375) nhận thưởng nhất quán khi ngưỡng giãn còn 2,7; ngưỡng 4,0 cố định thì không
        from dataclasses import replace
        scaled = calc_proposal_agent_12m([3.5] * 12, [0.0] * 12, k2_pct=85.0, params=v3)
        fixed = calc_proposal_agent_12m([3.5] * 12, [0.0] * 12, k2_pct=85.0, params=replace(v3, agent_q_consistency_min_fyc=4.0))
        self.assertGreater(scaled["total_bonuses_earned"], fixed["total_bonuses_earned"])

    def test_bonus_base_independent_of_product_commission_rate(self) -> None:
        a30 = H.hybrid_agent_12m(30, 2, 85.0, "V1", "FULL_TIME", BASE, fyc_rate=0.30)
        a40 = H.hybrid_agent_12m(30, 2, 85.0, "V1", "FULL_TIME", BASE, fyc_rate=0.40)
        self.assertEqual(a30["bonuses"], a40["bonuses"])                                   # thưởng trên FYC chuẩn hóa
        self.assertAlmostEqual(a40["total_earned"] - a30["total_earned"], 30 * 0.10 * 12, places=3)   # chỉ hoa hồng đổi
        self.assertAlmostEqual(a40["fyc_total"], 30 * 0.40 * 12, places=3)
        for bad in (float("nan"), float("inf"), 0.0, -0.3, 1.5):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                H.hybrid_agent_12m(30, 2, 85.0, "V1", "FULL_TIME", BASE, fyc_rate=bad)

    def test_pool_cap_scale(self) -> None:
        self.assertEqual(H.pool_cap_scale(70.0, 30.0, 5.0, 100.0), 1.0)                     # dưới trần: không co
        self.assertAlmostEqual(H.pool_cap_scale(85.0, 30.0, 5.0, 100.0), (75 - 35) / 50)   # co đúng phần biến đổi
        self.assertEqual(H.pool_cap_scale(120.0, 70.0, 10.0, 100.0), 0.0)                  # hoa hồng + cố định đã vượt
        for bad in ((float("nan"), 1, 1, 100), (80, 1, 1, 0), (80, float("inf"), 1, 100)):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                H.pool_cap_scale(*bad)

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
        # trần phải giữ ở kịch bản XẤU NHẤT (tự kiểm toán 41bec2d: kịch bản chuẩn không bật trợ cấp Full-time)
        worst = self.d["org"]["Hybrid"]["worst"]["cost_pct"]
        self.assertLessEqual(worst, 75.0)
        self.assertGreaterEqual(worst, max(sc["cost_pct"] for sc in self.d["org"]["Hybrid"]["scenarios"].values()))
        self.assertIn("V2, năng suất ngang V1", self.d["org"]["Hybrid"]["scenarios"])
        self.assertGreater(self.d["org"]["Hybrid"]["quota"]["fixed_share"], self.d["org"]["Hybrid"]["k85"]["fixed_share"])   # trợ cấp bật khi đạt quota

    def test_cost_cap_holds_at_every_region_quota_and_breakpoint(self) -> None:
        # Codex P1 (9dea455): V3, 45 ĐL đúng quota 20,25tr từng vượt 76,2%
        for reg, meta in H.REGIONS.items():
            o = self.P2.org_cost("Hybrid", 85.0, BASE, prod=H.FT_QUOTA_FYP_MONTH * meta["coef"] / (1200 / 45), region=reg)
            with self.subTest(reg=reg):
                self.assertLessEqual(o["cost_pct"], 75.0)
        self.assertEqual([x for x in self.d["sweep"] if x["cost_pct"] > 75.0], [])
        # quét dày ngoài lưới: FYP 5–600tr/ĐL bước 2,5 × K2 80/85/90/95 × 3 vùng
        worst = max(self.P2.org_cost("Hybrid", k2, BASE, prod=(5 + 2.5 * i) / (1200 / 45), region=reg)["cost_pct"]
                    for reg in H.REGIONS for k2 in (80.0, 85.0, 90.0, 95.0) for i in range(239))
        self.assertLessEqual(worst, 75.0)
        self.assertLessEqual(worst, self.d["org"]["Hybrid"]["worst"]["cost_pct"] + 0.5)   # lưới không bỏ sót đỉnh đáng kể

    def test_cap_holds_when_mix_is_pure_protection(self) -> None:
        # AUD-03 (audit r1): hoa hồng 40% (bảo vệ thuần) từng đẩy Chính sách Lai lên 78–93% FYP
        rows = {(r["scheme"], r["rate"]): r for r in self.d["fyc_sensitivity"]}
        self.assertEqual({r for _, r in rows}, {0.25, 0.30, 0.40})
        h40 = rows[("Hybrid", 0.40)]
        self.assertLessEqual(h40["worst"], H.COST_CAP_PCT_FYP + 1e-6)
        self.assertLess(h40["pool_scale_worst"], 1.0)                 # trần thật sự chặn — và được công bố, không giấu
        self.assertEqual(rows[("Hybrid", 0.30)]["pool_scale_worst"], 1.0)   # kịch bản chuẩn không bị cắt
        self.assertAlmostEqual(rows[("Hybrid", 0.30)]["std"], self.d["org"]["Hybrid"]["k85"]["cost_pct"], places=6)
        self.assertGreater(rows[("Chubb", 0.40)]["std"], rows[("Chubb", 0.30)]["std"])   # đối thủ trả trên FYC thật
        for r in self.d["fyc_sensitivity"]:
            self.assertTrue(all(math.isfinite(r[k]) for k in ("std", "worst", "pool_scale_std", "pool_scale_worst")))

    def test_agent_cliffs_disclosed_and_simplicity_counted_uniformly(self) -> None:
        keys = {t["id"] for t in self.d["traps"]}
        self.assertIn("Hybrid|agent_k2_cliff", keys)
        self.assertIn("Hybrid|quota_cliff", keys)
        p4 = next(r for r in self.d["rubric"] if r["scheme"] == "Hybrid" and r["pillar"].startswith("Độ đơn giản"))
        self.assertTrue(p4["evidence"].startswith("5 khoản"), p4["evidence"])          # cùng đơn vị đếm với 3 hãng (Codex P2 9dea455)
        self.assertIn("gộp 1", p4["evidence"])

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
