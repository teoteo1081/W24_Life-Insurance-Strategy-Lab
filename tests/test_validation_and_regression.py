"""
W24 Regression & Input-Validation Test Suite (Section 10 Hardening).

Proves that NaN, +Inf, -Inf, invalid numeric types, booleans, invalid dates,
out-of-range percentages, unsupported roles/schemes, missing/duplicate lookup keys,
UNKNOWN K2 without explicit new-agent flag, and invalid negative inputs are strictly
rejected — while valid negative business adjustments/clawbacks continue to work!
"""

from __future__ import annotations

import math
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from model.compensation.compensation_engine import (
    ProposalParams,
    aia_ack_eligible_for_3m_bonus,
    aia_cvtv_fy_factor,
    apply_aia_70pct_cap,
    calc_aia_cql_12m,
    calc_aia_cvtv_12m,
    calc_aia_paf_12m,
    calc_chubb_al_12m,
    calc_chubb_al_htktn_month,
    calc_chubb_ar_12m,
    calc_chubb_ch_m1_12_offset,
    calc_chubb_rd_12m,
    calc_enterprise_hierarchy_cost,
    calc_manulife_psm_12m,
    calc_proposal_agent_12m,
    chubb_ch_w1_factor,
    chubb_k2_factor,
    load_aia_paf_targets,
    load_chubb_commissions,
    load_chubb_hsbh,
    lookup_chubb_tudo_anphuc_y1_rate,
    manulife_k2_factor,
    mapa_forward,
    mapa_reverse_required_manpower,
    proposal_k2_factor,
    round_aia_fy,
)
from tests.test_compensation_golden import assert_close


class TestAssertCloseSafety(unittest.TestCase):
    """Regression proving NaN, Inf, -Inf, and bool can NEVER bypass assert_close."""

    def test_assert_close_rejects_nan_and_infinities(self) -> None:
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(AssertionError):
                assert_close(bad, 10.0, label="actual non-finite")
            with self.assertRaises(AssertionError):
                assert_close(10.0, bad, label="expected non-finite")
        with self.assertRaises(AssertionError):
            assert_close(float("nan"), float("nan"), label="both NaN must fail")

    def test_assert_close_rejects_bool_and_strings(self) -> None:
        with self.assertRaises(AssertionError):
            assert_close(True, 1.0, label="bool actual")  # type: ignore[arg-type]
        with self.assertRaises(AssertionError):
            assert_close("10.0", 10.0, label="string actual")  # type: ignore[arg-type]


class TestNaNInfAndTypeRejection(unittest.TestCase):
    """Proves NaN, +Inf, -Inf, booleans, and wrong types fail explicitly at engine entry."""

    def test_proposal_rejects_nan_inf_and_invalid_params(self) -> None:
        for bad in (float("nan"), float("inf"), float("-inf")):
            with self.assertRaises(ValueError):
                calc_proposal_agent_12m([bad] + [10.0] * 11, [0.0] * 12, k2_pct=80.0)
            with self.assertRaises(ValueError):
                calc_proposal_agent_12m([10.0] * 12, [0.0] * 12, k2_pct=bad)
            with self.assertRaises(ValueError):
                calc_proposal_agent_12m(
                    [10.0] * 12, [0.0] * 12, k2_pct=80.0,
                    params=ProposalParams(agent_q_consistency_3m=bad),
                )

    def test_competitor_engines_reject_nan_inf_and_booleans(self) -> None:
        with self.assertRaises(ValueError):
            round_aia_fy(float("nan"))
        with self.assertRaises(ValueError):
            aia_cvtv_fy_factor(float("inf"), 2026)
        with self.assertRaises(ValueError):
            calc_aia_cvtv_12m([10.0] * 11, [0.0] * 12, fy_pct=75.0)  # wrong length
        with self.assertRaises(ValueError):
            calc_chubb_ar_12m([10.0] * 12, [0.0] * 12, [True] * 12, k2_pct=float("nan"))
        with self.assertRaises(ValueError):
            calc_manulife_psm_12m(35.0, [1.0] * 12, [float("inf")] + [100.0] * 11, [1.0] * 4, k2_pct=80.0)
        with self.assertRaises(ValueError):
            calc_enterprise_hierarchy_cost("W24_Proposed_Balanced", k2_pct=float("nan"))
        with self.assertRaises(ValueError):
            mapa_forward(True, 0.35, 1.5, 20.0)  # type: ignore[arg-type]


class TestUnknownAndDomainValidation(unittest.TestCase):
    """Proves UNKNOWN is not silently converted to 0/1.0 and invalid domain inputs fail."""

    def test_unknown_k2_not_silently_converted_to_factor_1(self) -> None:
        with self.assertRaises(ValueError):
            proposal_k2_factor(None)
        with self.assertRaises(ValueError):
            calc_proposal_agent_12m([15.0] * 12, [0.0] * 12, k2_pct=None, is_new_agent=False)
        with self.assertRaises(ValueError):
            chubb_k2_factor(None, allow_new_no_k2=False)
        with self.assertRaises(ValueError):
            manulife_k2_factor(None, 4, allow_new_no_k2=False)
        with self.assertRaises(ValueError):
            proposal_k2_factor("UNKNOWN")  # type: ignore[arg-type]
        # Explicit policy-backed new agent without K2 history works cleanly:
        assert_close(proposal_k2_factor(None, allow_new_no_k2=True), 1.0, label="explicit new agent no K2")
        res_new = calc_proposal_agent_12m([10.0] * 12, [0.0] * 12, k2_pct=None, is_new_agent=True)
        self.assertGreater(res_new["accrued_t_plus_1_unpaid"], 0.0)

    def test_invalid_dates_percentages_roles_schemes_and_tenures(self) -> None:
        with self.assertRaises(ValueError):
            aia_ack_eligible_for_3m_bonus("2026-13", 10)
        with self.assertRaises(ValueError):
            aia_ack_eligible_for_3m_bonus("01/2026", 10)
        with self.assertRaises(ValueError):
            aia_cvtv_fy_factor(105.0, 2026)
        with self.assertRaises(ValueError):
            aia_cvtv_fy_factor(-5.0, 2026)
        with self.assertRaises(ValueError):
            aia_cvtv_fy_factor(75.0, 2025)  # unsupported policy_year
        with self.assertRaises(ValueError):
            round_aia_fy(75.0, mode="Floor")
        with self.assertRaises(ValueError):
            chubb_ch_w1_factor(85.0, conflict_mode="Arbitrary")
        with self.assertRaises(ValueError):
            calc_aia_paf_12m("UNKNOWN_RANK", 1, [100.0] * 12, [30.0] * 12, [5.0] * 12, 75.0)
        with self.assertRaises(ValueError):
            calc_aia_paf_12m("PAF", 6, [100.0] * 12, [30.0] * 12, [5.0] * 12, 75.0)  # Year > 5
        with self.assertRaises(ValueError):
            calc_chubb_al_12m([20.0] * 12, [4] * 12, 80.0, rank="VP")
        with self.assertRaises(ValueError):
            calc_chubb_ar_12m([20.0] * 12, [0.0] * 12, [True] * 12, 80.0, tenure_months_start=0)
        with self.assertRaises(ValueError):
            calc_enterprise_hierarchy_cost("Manulife_Full_Agency_UNKNOWN", k2_pct=80.0)
        with self.assertRaises(ValueError):
            lookup_chubb_tudo_anphuc_y1_rate(70, "Male", 50.0)  # age > 65
        with self.assertRaises(ValueError):
            lookup_chubb_tudo_anphuc_y1_rate(30, "Other", 50.0)  # invalid gender

    def test_valid_negative_clawback_allowed_vs_invalid_negative_rejected(self) -> None:
        # VALID negative adjustment: Chubb AL symmetric negative FYC clawback (0008V p.5)
        assert_close(calc_chubb_al_htktn_month(-25.0, ehc_ntt=4, k2_ntt=80.0, al_tenure_months=15), -12.0, label="valid negative clawback")
        # VALID negative monthly adjustment in 12m AL ledger
        al_neg = calc_chubb_al_12m([-25.0] + [30.0] * 11, [4] * 12, k2_ntt=80.0, al_tenure_start=15)
        self.assertTrue(math.isfinite(al_neg["total_earned"]))

        # INVALID negative inputs MUST fail:
        with self.assertRaises(ValueError):
            lookup_chubb_tudo_anphuc_y1_rate(30, "Male", -10.0)
        with self.assertRaises(ValueError):
            apply_aia_70pct_cap(-400.0, 100.0, [100.0], "CQL")
        with self.assertRaises(ValueError):
            calc_manulife_psm_12m(-35.0, [1.0] * 12, [100.0] * 12, [1.0] * 4, 80.0)
        with self.assertRaises(ValueError):
            calc_aia_cvtv_12m([10.0] * 12, [0.0] * 12, 75.0, clawback_6m_fyc=-5.0)
        with self.assertRaises(ValueError):
            mapa_forward(-10.0, 0.35, 1.5, 20.0)
        with self.assertRaises(ValueError):
            mapa_reverse_required_manpower(1000.0, 0.0, 1.5, 20.0)

    def test_duplicate_and_missing_lookup_keys_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "dup_chubb.csv"
            p.write_text(
                "Product_Rule_ID,Y1_Pct\nCHB-PRD-001,30.0\nCHB-PRD-001,25.0\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_chubb_commissions(p)

            p2 = Path(td) / "dup_paf.csv"
            p2.write_text(
                "Role_Code,Tenure_Year,Period_Key,Metric,Target_Value\n"
                "PAF,Year_1,M01,FYP_Million_VND,72\n"
                "PAF,Year_1,M01,FYP_Million_VND,72\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_aia_paf_targets(p2)

            p3 = Path(td) / "dup_hsbh.csv"
            p3.write_text(
                "Age_Band,Min_Age,Max_Age,Male_Tier1_HSBH,Male_Tier2_HSBH,Female_Tier1_HSBH,Female_Tier2_HSBH\n"
                "0-17,0,17,55,70,55,70\n0-17,0,17,55,70,55,70\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_chubb_hsbh(p3)

        # Missing key in custom targets dict passed to calc_aia_paf_12m
        with self.assertRaises(ValueError):
            calc_aia_paf_12m("PAF", 1, [100.0] * 12, [30.0] * 12, [5.0] * 12, 75.0, targets={})

    def test_parameter_perturbation_determinism(self) -> None:
        base = calc_proposal_agent_12m([15.0] * 12, [0.0] * 12, k2_pct=82.0)
        bumped = calc_proposal_agent_12m(
            [15.0] * 12, [0.0] * 12, k2_pct=82.0,
            params=ProposalParams(agent_m_tier_rates=(0.08, 0.20, 0.24, 0.32, 0.38)),
        )
        # 180 * 0.16 * 1.10 = 31.68 vs 180 * 0.20 * 1.10 = 39.60
        assert_close(base["bonus_monthly"], 31.68, label="base monthly bonus @ 16%")
        assert_close(bumped["bonus_monthly"], 39.60, label="perturbed monthly bonus @ 20%")


if __name__ == "__main__":
    unittest.main(verbosity=2)
