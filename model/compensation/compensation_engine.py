"""
W24 Life Insurance Strategy Lab — 12-Month Compensation, Total Distribution Cost,
Earned/Paid/Obligation Ledger, MAPA & Financial Break-Even Engine (v2.0 Post-Audit).

Design Principles:
- Zero hard-coded competitor logic hidden inside opaque paths; every threshold & rate
  comes from explicit policy parameter dictionaries or normalized CSV lookup tables.
- Conflict toggles for unresolved source conflicts (ERR-DOC-01 Chubb W1; ERR-DOC-02 AIA rounding).
- Full separation of Earned, Cash Paid Year 1 (T / T+1), Deferred Post-Y1, Holdback,
  Clawback/Recovery, and Forfeiture.
- Enterprise Hierarchy Total Distribution Cost counts FYP revenue ONCE (zero double counting)
  and validates TT 67/2023 Art. 52 (<=30% Y1 new-business bonus portfolio ceiling).
"""

from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[2]
LOOKUPS_DIR = REPO_ROOT / "knowledge" / "lookups"
_YM_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


# =============================================================================
# 0. STRICT NUMERIC & INPUT VALIDATION HELPERS (REJECT NaN / Inf / INVALID TYPES)
# =============================================================================

def _require_finite_float(val: Any, name: str) -> float:
    """Validate finite real number (rejects bool, None, strings, NaN, +Inf, -Inf)."""
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise ValueError(f"Invalid numeric type for {name}: {val!r}")
    f = float(val)
    if not math.isfinite(f):
        raise ValueError(f"Non-finite numeric value for {name}: {val!r}")
    return f


def _require_non_negative_float(val: Any, name: str) -> float:
    f = _require_finite_float(val, name)
    if f < 0.0:
        raise ValueError(f"{name} must be non-negative, got {f}")
    return f


def _require_positive_float(val: Any, name: str) -> float:
    f = _require_finite_float(val, name)
    if f <= 0.0:
        raise ValueError(f"{name} must be strictly positive, got {f}")
    return f


def _require_int(val: Any, name: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    if isinstance(val, bool) or not isinstance(val, int):
        raise ValueError(f"Invalid integer for {name}: {val!r}")
    if min_val is not None and val < min_val:
        raise ValueError(f"{name} must be >= {min_val}, got {val}")
    if max_val is not None and val > max_val:
        raise ValueError(f"{name} must be <= {max_val}, got {val}")
    return val


def _require_percentage(val: Any, name: str, max_pct: float = 100.0) -> float:
    f = _require_finite_float(val, name)
    if f < 0.0 or f > max_pct:
        raise ValueError(f"{name} must be within [0, {max_pct}], got {f}")
    return f


def _require_rate_0_to_1(val: Any, name: str, allow_zero: bool = True) -> float:
    f = _require_finite_float(val, name)
    if f < 0.0 or f > 1.0 or (not allow_zero and f == 0.0):
        raise ValueError(f"{name} must be in {'[0, 1]' if allow_zero else '(0, 1]'}, got {f}")
    return f


def _require_vector(vec: Sequence[Any], expected_len: int, name: str, allow_negative: bool = False) -> List[float]:
    if not isinstance(vec, (list, tuple)) or len(vec) != expected_len:
        raise ValueError(f"{name} must be a sequence of length {expected_len}")
    out = []
    for i, item in enumerate(vec):
        v = _require_finite_float(item, f"{name}[{i}]")
        if not allow_negative and v < 0.0:
            raise ValueError(f"{name}[{i}] must be non-negative, got {v}")
        out.append(v)
    return out


def _require_int_vector(vec: Sequence[Any], expected_len: int, name: str, min_val: int = 0) -> List[int]:
    if not isinstance(vec, (list, tuple)) or len(vec) != expected_len:
        raise ValueError(f"{name} must be a sequence of length {expected_len}")
    return [_require_int(item, f"{name}[{i}]", min_val=min_val) for i, item in enumerate(vec)]


def _require_ym_date(ym: Any, name: str) -> str:
    if not isinstance(ym, str) or not _YM_RE.match(ym):
        raise ValueError(f"{name} must match YYYY-MM (01..12), got {ym!r}")
    return ym


# =============================================================================
# 1. NORMALIZED LOOKUP LOADERS (PAF+ 1,300 rows & Chubb 113 rows + 10 HSBH)
# =============================================================================

def load_aia_paf_targets(path: Optional[Path] = None) -> Dict[Tuple[str, int, str], Tuple[float, float]]:
    """Return {(Rank, Year_No, Period): (FYP_Million_VND, 1mAA_Count)} with duplicate/missing key checks."""
    p = path or (LOOKUPS_DIR / "aia-paf-5y-targets.csv")
    out: Dict[Tuple[str, int, str], Tuple[float, float]] = {}
    seen_metric_keys = set()
    with open(p, encoding="utf-8") as f:
        for idx, r in enumerate(csv.DictReader(f), 2):
            rank = (r.get("Role_Code") or "").strip()
            ty = (r.get("Tenure_Year") or "").strip()
            pk = (r.get("Period_Key") or "").strip()
            metric = (r.get("Metric") or "").strip()
            if not rank or not ty.startswith("Year_") or not pk or metric not in ("FYP_Million_VND", "1mAA_Count"):
                raise ValueError(f"Malformed AIA PAF lookup row {idx}: {r}")
            yr = _require_int(int(ty.replace("Year_", "")), "Tenure_Year", 1, 5)
            period = "Annual" if pk == "ANNUAL_TOTAL" else pk
            mkey = (rank, yr, period, metric)
            if mkey in seen_metric_keys:
                raise ValueError(f"Duplicate AIA PAF lookup key at row {idx}: {mkey}")
            seen_metric_keys.add(mkey)
            val = _require_non_negative_float(float(r["Target_Value"]), f"Target_Value[{mkey}]")
            prev_fyp, prev_aa = out.get((rank, yr, period), (0.0, 0.0))
            if metric == "FYP_Million_VND":
                out[(rank, yr, period)] = (val, prev_aa)
            else:
                out[(rank, yr, period)] = (prev_fyp, val)
    if not out:
        raise ValueError(f"Empty AIA PAF lookup file: {p}")
    return out


def load_chubb_commissions(path: Optional[Path] = None) -> Dict[str, Dict[str, str]]:
    """Return {Product_Rule_ID: row_dict} from 113-row normalized schedule with duplicate-key check."""
    p = path or (LOOKUPS_DIR / "chubb-product-commission-schedule.csv")
    out: Dict[str, Dict[str, str]] = {}
    with open(p, encoding="utf-8") as f:
        for idx, r in enumerate(csv.DictReader(f), 2):
            pid = (r.get("Product_Rule_ID") or "").strip()
            if not pid:
                raise ValueError(f"Missing Product_Rule_ID at row {idx}")
            if pid in out:
                raise ValueError(f"Duplicate Product_Rule_ID at row {idx}: {pid}")
            out[pid] = r
    if not out:
        raise ValueError(f"Empty Chubb commission lookup file: {p}")
    return out


def load_chubb_hsbh(path: Optional[Path] = None) -> List[Dict[str, str]]:
    """Return 10 age-band rows for Chubb Tu Do An Phuc HSBH tiers with key/range checks."""
    p = path or (LOOKUPS_DIR / "chubb-hsbh-tiers.csv")
    rows: List[Dict[str, str]] = []
    seen_bands = set()
    with open(p, encoding="utf-8") as f:
        for idx, r in enumerate(csv.DictReader(f), 2):
            band = (r.get("Age_Band") or "").strip()
            if not band or band in seen_bands:
                raise ValueError(f"Invalid or duplicate HSBH Age_Band at row {idx}: {band!r}")
            seen_bands.add(band)
            rows.append(r)
    if not rows:
        raise ValueError(f"Empty Chubb HSBH lookup file: {p}")
    return rows


def lookup_chubb_tudo_anphuc_y1_rate(age: int, gender: str, hsbh: float, hsbh_rows: Optional[List[Dict[str, str]]] = None) -> float:
    """
    Exact Chubb Tu Do An Phuc Y1 FYC rate from SRC-POL-CHB-001 p.16 & p.19.
    Age < 18: Tier0 (<T1)=20%, Tier1 (T1-<T2)=22%, Tier2 (>=T2)=25%.
    Age >= 18: Tier0 (<T1)=25%, Tier1 (T1-<T2)=27%, Tier2 (>=T2)=30%.
    """
    age_i = _require_int(age, "age", 0, 65)
    hsbh_f = _require_non_negative_float(hsbh, "hsbh")
    if not isinstance(gender, str):
        raise ValueError(f"Invalid gender: {gender!r}")
    g = gender.strip().upper()
    if g in ("M", "MALE", "NAM"):
        t1_col, t2_col = "Male_Tier1_HSBH", "Male_Tier2_HSBH"
    elif g in ("F", "FEMALE", "NU", "NỮ"):
        t1_col, t2_col = "Female_Tier1_HSBH", "Female_Tier2_HSBH"
    else:
        raise ValueError(f"Unsupported gender for HSBH lookup: {gender!r}")
    rows = hsbh_rows if hsbh_rows is not None else load_chubb_hsbh()
    t1 = t2 = None
    for r in rows:
        lo, hi = int(r["Min_Age"]), int(r["Max_Age"])
        if lo <= age_i <= hi:
            t1 = _require_non_negative_float(float(r[t1_col]), t1_col)
            t2 = _require_non_negative_float(float(r[t2_col]), t2_col)
            break
    if t1 is None or t2 is None:
        raise ValueError(f"Age {age_i} out of Chubb HSBH range 0-65")
    if age_i < 18:
        if hsbh_f >= t2:
            return 0.25
        return 0.22 if hsbh_f >= t1 else 0.20
    else:
        if hsbh_f >= t2:
            return 0.30
        return 0.27 if hsbh_f >= t1 else 0.25


# =============================================================================
# 2. ROUNDING & CONFLICT-SAFE HELPERS
# =============================================================================

def round_aia_fy(fy_pct: float, mode: str = "HalfUp") -> int:
    """
    ERR-DOC-02 Conflict Toggle:
    - 'HalfUp': Standard half-up rounding (>=0.5 up) per AIA CQL p.21 & PAF+ p.18
      (74.49 -> 74, 74.50 -> 75).
    - 'RoundUp': Ceiling rounding per AIA CVTV p.14 wording ('lam tron len den 0 so thap phan')
      (74.01 -> 75, 74.00 -> 74).
    """
    fy_val = _require_percentage(fy_pct, "fy_pct", max_pct=100.0)
    if mode == "HalfUp":
        return int(math.floor(fy_val + 0.5))
    elif mode == "RoundUp":
        return int(math.ceil(fy_val - 1e-12))
    raise ValueError(f"Unknown AIA rounding mode: {mode}")


def apply_aia_70pct_cap(
    target_req: float,
    direct_val: float,
    sub_branch_vals: List[float],
    level: str = "CQL",
) -> float:
    """
    Codex Finding #6 fix:
    - CQL (2601-034 p.9-10): When sub_branch_vals is non-empty, BOTH direct_val AND each
      sub-UM+ branch are capped at 70% of target_req!
    - PAF+ (2601-035 p.6-7): Direct block counts 100% (uncapped); ONLY each direct sub-PAF+
      branch is capped at 70% of target_req!
    """
    tgt = _require_non_negative_float(target_req, "target_req")
    dval = _require_non_negative_float(direct_val, "direct_val")
    subs = [_require_non_negative_float(v, f"sub_branch_vals[{i}]") for i, v in enumerate(sub_branch_vals)]
    cap = 0.70 * tgt
    if level == "CQL":
        if not subs:
            return dval
        return min(dval, cap) + sum(min(v, cap) for v in subs)
    elif level == "PAF+":
        return dval + sum(min(v, cap) for v in subs)
    raise ValueError(f"Unknown level for 70% cap: {level}")


# =============================================================================
# 3. AIA ALPHA ENGINE (CVTV 2026/2027, CQL, PAF+)
# =============================================================================

def aia_cvtv_fy_factor(fy_pct_raw: float, policy_year: int = 2026, rounding_mode: str = "HalfUp") -> float:
    if policy_year not in (2026, 2027):
        raise ValueError(f"Unsupported AIA CVTV policy_year: {policy_year!r} (expected 2026 or 2027)")
    fy = round_aia_fy(fy_pct_raw, rounding_mode)
    if policy_year == 2026:
        if fy >= 85:
            return 1.20
        if fy >= 80:
            return 1.10
        if fy >= 75:
            return 1.00
        if fy >= 70:
            return 0.90
        if fy >= 65:
            return 0.80
        return fy / 100.0  # Soft floor in 2026
    else:  # 2027 hard cliff
        if fy >= 90:
            return 1.20
        if fy >= 85:
            return 1.15
        if fy >= 80:
            return 1.05
        if fy >= 75:
            return 1.00
        if fy >= 70:
            return 0.85
        return 0.0  # Hard cliff <70% -> 0%


def aia_cvtv_quarterly_rate(fyc_q_annualized: float) -> float:
    """8 tiers on quarterly FYC TC (Million VND) — SRC-POL-AIA-ALP-001 p.5."""
    val = _require_finite_float(fyc_q_annualized, "fyc_q_annualized")
    tiers = [
        (150.0, 0.40), (120.0, 0.35), (90.0, 0.30), (70.0, 0.25),
        (50.0, 0.20), (35.0, 0.15), (20.0, 0.10), (16.0, 0.04),
    ]
    for th, rate in tiers:
        if val >= th:
            return rate
    return 0.0


def aia_cvtv_premier_tier(
    fyc_q: float, active_months_in_q: int, fy_pct_raw: float,
    policy_year: int = 2026, rounding_mode: str = "HalfUp"
) -> Tuple[str, float, float]:
    """Return (TierLabel, PremierRate_on_FYC, SYC_Bonus_Rate)."""
    if policy_year not in (2026, 2027):
        raise ValueError(f"Unsupported AIA CVTV policy_year: {policy_year!r}")
    fq = _require_finite_float(fyc_q, "fyc_q")
    act = _require_int(active_months_in_q, "active_months_in_q", 0, 3)
    fy = round_aia_fy(fy_pct_raw, rounding_mode)
    gate_34 = 65 if policy_year == 2026 else 70
    gate_5 = 75 if policy_year == 2026 else 80
    if fq >= 70.0 and act >= 3 and fy >= gate_5:
        return ("5S", 0.15, 0.50)
    if fq >= 35.0 and act >= 3 and fy >= gate_34:
        return ("4S", 0.10, 0.30)
    if fq >= 20.0 and act >= 2 and fy >= gate_34:
        return ("3S", 0.05, 0.00)
    return ("None", 0.00, 0.00)


def aia_cvtv_annual_rate(fyc_annual: float) -> float:
    val = _require_finite_float(fyc_annual, "fyc_annual")
    for th, rate in [(1600.0, 0.20), (800.0, 0.14), (300.0, 0.10), (150.0, 0.06)]:
        if val >= th:
            return rate
    return 0.0


def aia_ack_eligible_for_3m_bonus(
    approval_date_ym: str, ack_days_from_approval: int, ack_received_on_or_before_feb28: bool = False
) -> bool:
    """
    Codex Finding #5 fix (SRC-POL-AIA-ALP-001 p.22):
    Normally ACK must be valid within 15 days of approval, EXCEPT policies approved in
    2026-01 have until 2026-02-28!
    """
    ym = _require_ym_date(approval_date_ym, "approval_date_ym")
    days = _require_int(ack_days_from_approval, "ack_days_from_approval", 0)
    if ym == "2026-01" and ack_received_on_or_before_feb28:
        return True
    return days <= 15


def calc_aia_cvtv_12m(
    monthly_fyc: List[float],
    monthly_syc: List[float],
    fy_pct: float,
    policy_year: int = 2026,
    is_new_sa: bool = False,
    fast_72h_qualified: bool = False,
    attendance_ok_m1_3: bool = True,
    ack_ok_m1_3: bool = True,
    freelook_ok_m1_3: bool = True,
    partial_q1_months: int = 3,
    disciplinary_final_warning: bool = False,
    clawback_6m_fyc: float = 0.0,
    rounding_mode: str = "HalfUp",
    assumed_fyc_to_fyp_rate: float = 0.30,
) -> Dict[str, float]:
    """Full 12-month AIA Alpha CVTV simulation (in Million VND)."""
    monthly_fyc = _require_vector(monthly_fyc, 12, "monthly_fyc", allow_negative=True)
    monthly_syc = _require_vector(monthly_syc, 12, "monthly_syc", allow_negative=True)
    _require_int(partial_q1_months, "partial_q1_months", 1, 3)
    clawback_6m_fyc = _require_non_negative_float(clawback_6m_fyc, "clawback_6m_fyc")
    assumed_fyc_to_fyp_rate = _require_rate_0_to_1(assumed_fyc_to_fyp_rate, "assumed_fyc_to_fyp_rate", allow_zero=False)
    fy_fac = aia_cvtv_fy_factor(fy_pct, policy_year, rounding_mode)
    disc_mult = 0.70 if disciplinary_final_warning else 1.00

    # Activation: 1/72H & Onboarding 3M (for new standard SA only)
    b_72h = 1.5 if (is_new_sa and fast_72h_qualified) else 0.0
    b_3m = 0.0
    if is_new_sa and attendance_ok_m1_3 and ack_ok_m1_3 and freelook_ok_m1_3:
        for m in range(3):
            # Exclude 4M minimum 1/72H policy from M1 if 1/72H paid
            eff_fyc = max(0.0, monthly_fyc[m] - (4.0 if (m == 0 and b_72h > 0) else 0.0))
            if eff_fyc >= 10.0:
                b_3m += 3.0
            elif eff_fyc >= 5.0:
                b_3m += 1.5

    q_prod_total = 0.0
    q_prem_total = 0.0
    q_syc_total = 0.0
    q_4s_count = 0
    q_5s_count = 0

    for q in range(4):
        sl = monthly_fyc[q * 3 : (q + 1) * 3]
        sl_syc = monthly_syc[q * 3 : (q + 1) * 3]
        q_fyc = sum(sl)
        q_syc = sum(sl_syc)
        act_m = sum(1 for x in sl if x >= 4.0)
        ann_fyc = q_fyc * (3.0 / partial_q1_months) if (q == 0 and partial_q1_months < 3) else q_fyc
        q_rate = aia_cvtv_quarterly_rate(ann_fyc)
        q_prod_total += q_fyc * q_rate * fy_fac

        tier, p_rate, syc_rate = aia_cvtv_premier_tier(q_fyc, act_m, fy_pct, policy_year, rounding_mode)
        if tier in ("4S", "5S"):
            q_4s_count += 1
        if tier == "5S":
            q_5s_count += 1
        q_prem_total += q_fyc * p_rate * fy_fac
        q_syc_total += q_syc * syc_rate

    fyc_total = sum(monthly_fyc)
    syc_total = sum(monthly_syc)
    ann_bonus = fyc_total * aia_cvtv_annual_rate(fyc_total) * fy_fac

    gross_bonuses = (b_72h + b_3m + q_prod_total + q_prem_total + q_syc_total + ann_bonus) * disc_mult
    # 6M clawback proportional recovery on canceled FYC
    clawback_ratio = min(1.0, clawback_6m_fyc / fyc_total) if fyc_total > 0 else 0.0
    clawback_amount = (fyc_total + gross_bonuses) * clawback_ratio

    earned_total = fyc_total + syc_total + gross_bonuses
    cash_paid_y1 = earned_total - clawback_amount
    implied_fyp = fyc_total / assumed_fyc_to_fyp_rate if assumed_fyc_to_fyp_rate > 0 else 0.0

    # Unpriced non-cash flags (NEVER guess cost!)
    non_cash_health_tier = 2 if (q_5s_count >= 3 and round_aia_fy(fy_pct, rounding_mode) >= 75) else (
        1 if (q_4s_count >= 3 and round_aia_fy(fy_pct, rounding_mode) >= 65) else 0
    )

    return {
        "fyc_total": round(fyc_total, 4),
        "syc_total": round(syc_total, 4),
        "implied_fyp": round(implied_fyp, 4),
        "bonus_72h": round(b_72h * disc_mult, 4),
        "bonus_3m": round(b_3m * disc_mult, 4),
        "bonus_quarterly_prod": round(q_prod_total * disc_mult, 4),
        "bonus_quarterly_premier": round(q_prem_total * disc_mult, 4),
        "bonus_syc": round(q_syc_total * disc_mult, 4),
        "bonus_annual": round(ann_bonus * disc_mult, 4),
        "total_bonuses_earned": round(gross_bonuses, 4),
        "total_earned": round(earned_total, 4),
        "cash_paid_y1": round(cash_paid_y1, 4),
        "deferred_post_y1": 0.0,
        "clawback_recovery": round(clawback_amount, 4),
        "pct_of_fyc": round((earned_total / fyc_total) * 100.0, 2) if fyc_total > 0 else 0.0,
        "bonus_pct_of_fyp": round((gross_bonuses / implied_fyp) * 100.0, 2) if implied_fyp > 0 else 0.0,
        "non_cash_health_tier_flag": float(non_cash_health_tier),
    }


def calc_aia_cql_12m(
    monthly_team_fyc: List[float],
    monthly_active_count: List[int],
    fy_pct: float,
    tot_pct: float = 86.0,
    attendance_ok: bool = True,
    quarterly_new_recruits: Optional[List[int]] = None,
    new_agent_fyc_12m: float = 0.0,
    new_agent_type: str = "SA",  # SA=10%, Exchange=20%, ExchangePro=40%
    indirect_gen2_base_12m: float = 0.0,
    new_um_base_monthly: float = 0.0,
    rounding_mode: str = "HalfUp",
    indirect_gen3_base_12m: float = 0.0,
    indirect_gen4_base_12m: float = 0.0,
) -> Dict[str, float]:
    """Full 12-month AIA Alpha CQL Manager calculation (Million VND).

    Indirect fee (2601-034 p.4, muc III): 50% / 25% / 12.5% of fee A of sub-CQL at
    level 2 / 3 / 4, where A = monthly direct "tuyen dung hieu qua" fee (+ JFW fee).
    The *_base_12m inputs are the 12-month sums of fee A per level.
    """
    indirect_gen3_base_12m = _require_finite_float(indirect_gen3_base_12m, "indirect_gen3_base_12m")
    indirect_gen4_base_12m = _require_finite_float(indirect_gen4_base_12m, "indirect_gen4_base_12m")
    monthly_team_fyc = _require_vector(monthly_team_fyc, 12, "monthly_team_fyc", allow_negative=True)
    monthly_active_count = _require_int_vector(monthly_active_count, 12, "monthly_active_count", min_val=0)
    tot_pct = _require_percentage(tot_pct, "tot_pct", 100.0)
    new_agent_fyc_12m = _require_non_negative_float(new_agent_fyc_12m, "new_agent_fyc_12m")
    indirect_gen2_base_12m = _require_finite_float(indirect_gen2_base_12m, "indirect_gen2_base_12m")
    new_um_base_monthly = _require_non_negative_float(new_um_base_monthly, "new_um_base_monthly")
    if new_agent_type not in ("SA", "Exchange", "ExchangePro"):
        raise ValueError(f"Unsupported AIA new_agent_type: {new_agent_type!r}")
    fy = round_aia_fy(fy_pct, rounding_mode)
    recruits = _require_int_vector(quarterly_new_recruits if quarterly_new_recruits is not None else [2, 2, 2, 2], 4, "quarterly_new_recruits", min_val=0)

    direct_m_total = 0.0
    activity_m_total = 0.0
    for m in range(12):
        f = monthly_team_fyc[m]
        a = monthly_active_count[m]
        if fy >= 80:
            rate = 0.24 if f >= 50 else (0.18 if f >= 20 else (0.15 if f >= 7 else 0.10))
        else:
            rate = 0.20 if f >= 50 else (0.15 if f >= 20 else (0.12 if f >= 7 else 0.08))
        direct_m_total += f * rate

        if attendance_ok:
            act_rate = 0.12 if a >= 6 else (0.08 if a >= 4 else (0.05 if a >= 2 else 0.0))
            fy_act_fac = 1.0 if fy >= 70 else (fy / 100.0)
            activity_m_total += f * act_rate * fy_act_fac

    premier_q_total = 0.0
    q_4s_plus = 0
    q_5s = 0
    for q in range(4):
        qf = sum(monthly_team_fyc[q * 3 : (q + 1) * 3])
        qa = sum(monthly_active_count[q * 3 : (q + 1) * 3])
        qr = recruits[q]
        req_r = 1 if q == 0 else 2
        if attendance_ok and fy >= 75:
            if qf >= 170 and qa >= 14 and qr >= req_r:
                premier_q_total += qf * 0.15
                q_4s_plus += 1
                q_5s += 1
            elif qf >= 80 and qa >= 9 and qr >= req_r:
                premier_q_total += qf * 0.08
                q_4s_plus += 1
            elif qf >= 50 and qa >= 6 and qr >= 1:
                premier_q_total += qf * 0.05

    team_fyc_y = sum(monthly_team_fyc)
    # Annual deferred 3Y (15% Y+2, 25% Y+3, 60% Y+4) requires FY>=75% & >=3Q; payout requires TOT>=85%
    ann_rate = 0.10 if (fy >= 75 and q_5s >= 3) else (0.05 if (fy >= 75 and q_4s_plus >= 3) else 0.0)
    deferred_3y_earned = team_fyc_y * ann_rate
    deferred_vested_if_tot_ok = deferred_3y_earned if tot_pct >= 85.0 else 0.0

    coach_rate = {"SA": 0.10, "Exchange": 0.20, "ExchangePro": 0.40}.get(new_agent_type, 0.10)
    coaching_fee = new_agent_fyc_12m * coach_rate
    indirect_fee = indirect_gen2_base_12m * 0.50 + indirect_gen3_base_12m * 0.25 + indirect_gen4_base_12m * 0.125
    new_um_promo_fee = min(30.0, new_um_base_monthly * 1.50) * 12.0 if (fy >= 75 and new_um_base_monthly > 0) else 0.0

    cash_y1 = direct_m_total + activity_m_total + premier_q_total + coaching_fee + indirect_fee + new_um_promo_fee
    total_earned = cash_y1 + deferred_3y_earned
    return {
        "team_fyc_12m": round(team_fyc_y, 4),
        "direct_monthly": round(direct_m_total, 4),
        "activity_monthly": round(activity_m_total, 4),
        "premier_quarterly": round(premier_q_total, 4),
        "annual_deferred_3y": round(deferred_3y_earned, 4),
        "deferred_vesting_y2_15pct": round(deferred_vested_if_tot_ok * 0.15, 4),
        "deferred_vesting_y3_25pct": round(deferred_vested_if_tot_ok * 0.25, 4),
        "deferred_vesting_y4_60pct": round(deferred_vested_if_tot_ok * 0.60, 4),
        "coaching_fee": round(coaching_fee, 4),
        "indirect_fee": round(indirect_fee, 4),
        "new_um_promo_fee": round(new_um_promo_fee, 4),
        "cash_paid_y1": round(cash_y1, 4),
        "total_earned": round(total_earned, 4),
        "direct_override_pct_fyc": round(((direct_m_total + activity_m_total + premier_q_total + deferred_3y_earned) / team_fyc_y) * 100.0, 2) if team_fyc_y > 0 else 0.0,
    }


PAF_BASE_FEES = {
    "PAF": 20.0, "AF": 35.0, "PSAF": 40.0, "SAF": 50.0, "DRF": 60.0,
    "RF": 70.0, "DSRF": 80.0, "SRF": 90.0, "PVP": 110.0, "SPVP": 130.0,
}


def calc_aia_paf_12m(
    rank: str,
    year_no: int,
    monthly_fyp: List[float],
    monthly_fyc: List[float],
    monthly_1maa: List[float],
    fy_pct: float,
    attendance_pct: float = 80.0,
    sub_paf_prof_fees_12m: float = 0.0,
    targets: Optional[Dict[Tuple[str, int, str], Tuple[float, float]]] = None,
    rounding_mode: str = "HalfUp",
) -> Dict[str, float]:
    """Full 12-month AIA Alpha PAF+ calculation reading normalized 1,300-row lookup."""
    if rank not in PAF_BASE_FEES:
        raise ValueError(f"Unsupported AIA PAF+ rank: {rank!r} (expected one of {sorted(PAF_BASE_FEES)})")
    _require_int(year_no, "year_no", 1, 5)
    monthly_fyp = _require_vector(monthly_fyp, 12, "monthly_fyp", allow_negative=True)
    monthly_fyc = _require_vector(monthly_fyc, 12, "monthly_fyc", allow_negative=True)
    monthly_1maa = _require_vector(monthly_1maa, 12, "monthly_1maa", allow_negative=False)
    attendance_pct = _require_percentage(attendance_pct, "attendance_pct", 100.0)
    sub_paf_prof_fees_12m = _require_finite_float(sub_paf_prof_fees_12m, "sub_paf_prof_fees_12m")
    t_map = targets if targets is not None else load_aia_paf_targets()
    for pk in [f"M{m:02d}" for m in range(1, 13)] + ["Annual"]:
        if (rank, year_no, pk) not in t_map:
            raise ValueError(f"Missing AIA PAF+ lookup key: {(rank, year_no, pk)}")
    base_m = PAF_BASE_FEES[rank]
    fy = round_aia_fy(fy_pct, rounding_mode)
    att_mult = 1.0 if attendance_pct >= 70.0 else 0.70

    # PAF+ FY factor (2601-035 p.4)
    if fy >= 75:
        fy_fac = 1.20
    elif fy >= 70:
        fy_fac = 1.10
    elif fy >= 65:
        fy_fac = 1.00
    elif fy >= 60:
        fy_fac = 0.80
    elif fy >= 50:
        fy_fac = 0.60
    else:
        fy_fac = 0.00

    base_total = 0.0
    prof_m_total = 0.0
    for m in range(12):
        tgt_fyp, tgt_aa = t_map[(rank, year_no, f"M{m+1:02d}")]
        ach_fyp = monthly_fyp[m] / tgt_fyp if tgt_fyp > 0 else 0.0
        ach_aa = monthly_1maa[m] / tgt_aa if tgt_aa > 0 else 0.0

        b_pct = 1.20 if ach_fyp >= 1.15 else (1.00 if ach_fyp >= 0.55 else (0.50 if ach_fyp >= 0.35 else 0.0))
        base_total += base_m * b_pct * att_mult

        r_fyp = 0.06 if ach_fyp >= 1.15 else (0.045 if ach_fyp >= 0.90 else (0.03 if ach_fyp >= 0.55 else 0.0))
        r_aa = 0.035 if ach_aa >= 1.15 else (0.025 if ach_aa >= 0.90 else (0.015 if ach_aa >= 0.55 else 0.0))
        prof_m_total += monthly_fyc[m] * (r_fyp * fy_fac + r_aa)

    prof_q_total = 0.0
    for q in range(4):
        q_fyp = sum(monthly_fyp[q * 3 : (q + 1) * 3])
        q_fyc = sum(monthly_fyc[q * 3 : (q + 1) * 3])
        q_aa = sum(monthly_1maa[q * 3 : (q + 1) * 3])
        q_tgt_fyp = sum(t_map[(rank, year_no, f"M{q*3+i+1:02d}")][0] for i in range(3))
        q_tgt_aa = sum(t_map[(rank, year_no, f"M{q*3+i+1:02d}")][1] for i in range(3))
        ach_qf = q_fyp / q_tgt_fyp if q_tgt_fyp > 0 else 0.0
        ach_qa = q_aa / q_tgt_aa if q_tgt_aa > 0 else 0.0

        rq_f = 0.05 if ach_qf >= 1.30 else (0.035 if ach_qf >= 1.15 else (0.02 if ach_qf >= 1.00 else (0.005 if ach_qf >= 0.90 else 0.0)))
        rq_a = 0.035 if ach_qa >= 1.30 else (0.025 if ach_qa >= 1.15 else (0.015 if ach_qa >= 1.00 else (0.005 if ach_qa >= 0.90 else 0.0)))
        prof_q_total += q_fyc * (rq_f * fy_fac + rq_a)

    ann_tgt_fyp = t_map[(rank, year_no, "Annual")][0]
    excess_fyp = max(0.0, sum(monthly_fyp) - ann_tgt_fyp)
    if year_no == 1:
        sen_rate = 0.05
    else:
        sen_rate = 0.06 if fy >= 70 else (0.05 if fy >= 65 else (0.04 if fy >= 55 else 0.0))
    seniority_fee = min(base_total, excess_fyp * sen_rate)
    indirect_50 = sub_paf_prof_fees_12m * 0.50

    total = base_total + prof_m_total + prof_q_total + seniority_fee + indirect_50
    return {
        "rank": rank,
        "annual_target_fyp": round(ann_tgt_fyp, 4),
        "actual_fyp": round(sum(monthly_fyp), 4),
        "base_fee_12m": round(base_total, 4),
        "prof_monthly_12m": round(prof_m_total, 4),
        "prof_quarterly_12m": round(prof_q_total, 4),
        "seniority_fee_clawback12m": round(seniority_fee, 4),
        "indirect_50pct": round(indirect_50, 4),
        "total_earned": round(total, 4),
        "cash_paid_y1": round(total, 4),
    }


# =============================================================================
# 4. CHUBB LIFE AGENCY ENGINE (AR, CHAMPION HUBB, AL, RD)
# =============================================================================

def chubb_k2_factor(k2_pct: Optional[float], allow_new_no_k2: bool = True) -> float:
    """
    Chubb AR & AL K2 factor (SRC-POL-CHB-001 p.5 & 002 p.5): <50% still gets 25%!
    Per memo p.5, new agents with no K2 history receive 100% ONLY when allow_new_no_k2=True;
    otherwise None / missing K2 raises ValueError instead of silently converting UNKNOWN to 1.0.
    """
    if k2_pct is None:
        if not allow_new_no_k2:
            raise ValueError("k2_pct is None/UNKNOWN and allow_new_no_k2=False")
        return 1.00
    val = _require_percentage(k2_pct, "k2_pct", 100.0)
    if val >= 80.0:
        return 1.20
    if val >= 70.0:
        return 1.00
    if val >= 60.0:
        return 0.75
    if val >= 50.0:
        return 0.50
    return 0.25


def chubb_ch_w1_factor(sop_pct: float, conflict_mode: str = "Table_80") -> float:
    """
    ERR-DOC-01 Conflict Toggle (SRC-POL-CHB-001 p.9 vs p.10):
    - 'Table_80': Per official table p.9 (80-<90% -> 80%, 70-<80% -> 50%).
    - 'Example_50': Per p.10 M11-M12 worked example (85% -> 50%).
    """
    if conflict_mode not in ("Table_80", "Example_50"):
        raise ValueError(f"Unsupported Chubb ERR-DOC-01 conflict_mode: {conflict_mode!r}")
    val = _require_percentage(sop_pct, "sop_pct", 100.0)
    if val >= 90.0:
        return 1.00
    if val >= 80.0:
        return 0.80 if conflict_mode == "Table_80" else 0.50
    if val >= 70.0:
        return 0.50
    return 0.00


def chubb_ch_w2_factor(k2_pct: float) -> float:
    val = _require_percentage(k2_pct, "k2_pct", 100.0)
    if val >= 85.0:
        return 1.25
    if val >= 75.0:
        return 1.00
    if val >= 65.0:
        return 0.50
    if val >= 50.0:
        return 0.30
    return 0.00


def calc_chubb_ch_m1_12_offset(
    month_idx: int,
    cc_count: int,
    sop_pct: float,
    kpi_pct: float,
    new_agent_bonus_paid_in_month: float = 0.0,
    conflict_mode: str = "Table_80",
) -> Dict[str, float]:
    """
    Codex Finding #7 exact fix (SRC-POL-CHB-001 p.9-10):
    Deducts NewAgentBonus from CH_Month cash first; any excess deducts from CH_M12 deferred tranche!
    Verified directly against p.10 M7 (5.0+2.4 vs 6.0 -> 0.0 month, 1.4 M12) & M12 (2.5+1.2 vs 1.5 -> 1.0 month, 1.2 M12).
    """
    month_idx = _require_int(month_idx, "month_idx", 1, 12)
    cc_count = _require_int(cc_count, "cc_count", 0)
    kpi_pct = _require_percentage(kpi_pct, "kpi_pct", 200.0)
    new_agent_bonus_paid_in_month = _require_non_negative_float(new_agent_bonus_paid_in_month, "new_agent_bonus_paid_in_month")
    w1 = chubb_ch_w1_factor(sop_pct, conflict_mode)
    if kpi_pct < 70.0 or cc_count < 1 or w1 == 0.0:
        return {"w1": w1, "ch_month_gross": 0.0, "ch_m12_gross": 0.0, "ch_month_net": 0.0, "ch_m12_net": 0.0}

    if 1 <= month_idx <= 6:
        gross_m = 7.0 if cc_count >= 3 else (5.0 if cc_count == 2 else 3.0)
        gross_m12 = 0.0
    else:  # M7-M12
        gross_m = 5.0 if cc_count >= 3 else (3.0 if cc_count == 2 else 2.0)
        gross_m12 = 2.4 if cc_count >= 2 else 1.2

    adj_m = gross_m * w1
    adj_m12 = gross_m12 * w1
    net_m = max(0.0, adj_m - new_agent_bonus_paid_in_month)
    excess_offset = max(0.0, new_agent_bonus_paid_in_month - adj_m)
    net_m12 = max(0.0, adj_m12 - excess_offset)
    return {
        "w1": w1,
        "ch_month_gross": round(adj_m, 4),
        "ch_m12_gross": round(adj_m12, 4),
        "ch_month_net": round(net_m, 4),
        "ch_m12_net": round(net_m12, 4),
    }


def calc_chubb_ar_12m(
    monthly_fyc: List[float],
    monthly_ryc: List[float],
    monthly_ehc: List[bool],
    k2_pct: Optional[float],
    tenure_months_start: int = 13,
    is_al_role: bool = False,
    new_agent_cc_m3_6_12: Tuple[int, int, int] = (0, 0, 0),
    new_agent_courses_ok: bool = True,
    join_ch: bool = False,
    monthly_cc_ch: Optional[List[int]] = None,
    sop_pct: float = 92.0,
    kpi_ch_pct: float = 80.0,
    remain_in_ch_at_m12: bool = True,
    conflict_mode: str = "Table_80",
    assumed_fyc_to_fyp_rate: float = 0.30,
) -> Dict[str, float]:
    """Full 12-month Chubb Life Individual Agent (AR or AL personal sales) calculation."""
    monthly_fyc = _require_vector(monthly_fyc, 12, "monthly_fyc", allow_negative=True)
    monthly_ryc = _require_vector(monthly_ryc, 12, "monthly_ryc", allow_negative=True)
    if not isinstance(monthly_ehc, (list, tuple)) or len(monthly_ehc) != 12 or not all(isinstance(x, bool) for x in monthly_ehc):
        raise ValueError("monthly_ehc must be a 12-element sequence of booleans")
    tenure_months_start = _require_int(tenure_months_start, "tenure_months_start", 1)
    assumed_fyc_to_fyp_rate = _require_rate_0_to_1(assumed_fyc_to_fyp_rate, "assumed_fyc_to_fyp_rate", allow_zero=False)
    k2_fac = chubb_k2_factor(k2_pct, allow_new_no_k2=(tenure_months_start < 13))
    hold_t_plus_1 = (k2_pct is None) or (k2_pct < 60.0)

    monthly_hqkd: List[float] = []
    # For seasoned agents (tenure>=13), prior 2 months assumed at steady-state M1 rate unless new agent
    pre_m = [monthly_fyc[0], monthly_fyc[0]] if tenure_months_start >= 13 else [0.0, 0.0]

    for m in range(12):
        tenure_m = tenure_months_start + m
        hist = pre_m + monthly_fyc[: m + 1]
        rolling_3m = sum(hist[-3:])
        capped = (tenure_m < 13) or (k2_pct is None)
        if not is_al_role:
            if rolling_3m >= 60.0:
                rate = 0.45 if capped else 0.55
            elif rolling_3m >= 40.0:
                rate = 0.45
            elif rolling_3m >= 20.0:
                rate = 0.35
            elif rolling_3m >= 10.0:
                rate = 0.25
            elif rolling_3m >= 5.0:
                rate = 0.075
            else:
                rate = 0.0
        else:
            if rolling_3m >= 60.0:
                rate = 0.60 if capped else 0.70
            elif rolling_3m >= 40.0:
                rate = 0.60
            elif rolling_3m >= 20.0:
                rate = 0.50
            elif rolling_3m >= 10.0:
                rate = 0.40
            elif rolling_3m >= 5.0:
                rate = 0.15
            else:
                rate = 0.0
        monthly_hqkd.append(monthly_fyc[m] * rate * k2_fac)

    q_mult_total = 0.0
    q_ryc_bonus = 0.0
    for q in range(4):
        ehc_q = sum(1 for x in monthly_ehc[q * 3 : (q + 1) * 3] if x)
        q_m_sum = sum(monthly_hqkd[q * 3 : (q + 1) * 3])
        q_mult = 0.30 if ehc_q >= 3 else (0.15 if ehc_q == 2 else 0.0)
        q_mult_total += q_m_sum * q_mult

        if (tenure_months_start + q * 3 + 2) >= 13 and (k2_pct is not None and k2_pct >= 65.0):
            ryc_rate = 0.15 if ehc_q >= 3 else (0.10 if ehc_q == 2 else 0.0)
            q_ryc_bonus += sum(monthly_ryc[q * 3 : (q + 1) * 3]) * ryc_rate

    # New Agent Bonus M3 / M6 / M12 (only for M1 starters)
    new_ag_by_month = [0.0] * 12
    if tenure_months_start == 1:
        cc3, cc6, cc12 = _require_int_vector(new_agent_cc_m3_6_12, 3, "new_agent_cc_m3_6_12")
        course_mult = 1.0 if new_agent_courses_ok else 0.50
        if cc3 >= 6:
            new_ag_by_month[2] = min(6.0, sum(monthly_fyc[0:3]) * 0.20)
        if cc6 >= 6:
            new_ag_by_month[5] = min(10.0, sum(monthly_fyc[3:6]) * 0.20) * course_mult
        if cc12 >= 12:
            new_ag_by_month[11] = min(20.0, sum(monthly_fyc[6:12]) * 0.20) * course_mult
    new_ag_total = sum(new_ag_by_month)

    # Champion Hubb M1-M12 add-on with exact offset
    ch_m_net_total = 0.0
    ch_m12_net_total = 0.0
    if join_ch and tenure_months_start == 1:
        ccs = _require_int_vector(monthly_cc_ch if monthly_cc_ch is not None else [2] * 12, 12, "monthly_cc_ch")
        for m in range(12):
            res = calc_chubb_ch_m1_12_offset(
                month_idx=m + 1, cc_count=ccs[m], sop_pct=sop_pct, kpi_pct=kpi_ch_pct,
                new_agent_bonus_paid_in_month=new_ag_by_month[m], conflict_mode=conflict_mode
            )
            ch_m_net_total += res["ch_month_net"]
            ch_m12_net_total += res["ch_m12_net"]
    ch_m12_vested = ch_m12_net_total if remain_in_ch_at_m12 else 0.0
    ch_m12_forfeited = ch_m12_net_total - ch_m12_vested

    fyc_total = sum(monthly_fyc)
    ryc_total = sum(monthly_ryc)
    hqkd_m_total = sum(monthly_hqkd)
    total_bonuses = hqkd_m_total + q_mult_total + q_ryc_bonus + new_ag_total + ch_m_net_total + ch_m12_vested
    total_earned = fyc_total + ryc_total + total_bonuses
    # If hold_t_plus_1 is True, M12 monthly bonus settles in Jan Y+1 (1 month lag)
    accrued_t_plus_1_m12 = monthly_hqkd[11] if hold_t_plus_1 else 0.0
    cash_paid_in_y1 = total_earned - accrued_t_plus_1_m12
    implied_fyp = fyc_total / assumed_fyc_to_fyp_rate if assumed_fyc_to_fyp_rate > 0 else 0.0

    return {
        "fyc_total": round(fyc_total, 4),
        "ryc_total": round(ryc_total, 4),
        "implied_fyp": round(implied_fyp, 4),
        "bonus_hqkd_monthly": round(hqkd_m_total, 4),
        "bonus_hqkd_quarterly": round(q_mult_total, 4),
        "bonus_ryc_quarterly": round(q_ryc_bonus, 4),
        "bonus_new_agent": round(new_ag_total, 4),
        "bonus_ch_month_addon": round(ch_m_net_total, 4),
        "bonus_ch_m12_vested": round(ch_m12_vested, 4),
        "bonus_ch_m12_forfeited": round(ch_m12_forfeited, 4),
        "total_bonuses_earned": round(total_bonuses, 4),
        "total_earned": round(total_earned, 4),
        "cash_paid_y1": round(cash_paid_in_y1, 4),
        "accrued_t_plus_1_unpaid": round(accrued_t_plus_1_m12, 4),
        "pct_of_fyc": round((total_earned / fyc_total) * 100.0, 2) if fyc_total > 0 else 0.0,
        "bonus_pct_of_fyp": round((total_bonuses / implied_fyp) * 100.0, 2) if implied_fyp > 0 else 0.0,
    }


K2_NO_K2_YET = "NO_K2_YET"
"""Explicit status: the direct team has no K2 yet (chưa phát sinh K2). Distinct from None, which means UNKNOWN."""


def _chubb_al_k2_status(k2_ntt: Any) -> Tuple[str, Optional[float]]:
    """Classify Chubb AL direct-team K2: ('NO_K2_YET', None) or ('OBSERVED', pct). None/UNKNOWN raises."""
    if isinstance(k2_ntt, str):
        if k2_ntt == K2_NO_K2_YET:
            return K2_NO_K2_YET, None
        raise ValueError(f"k2_ntt string must be {K2_NO_K2_YET!r}, got {k2_ntt!r}")
    if k2_ntt is None:
        raise ValueError(
            "k2_ntt is None (UNKNOWN). Pass the observed K2 % or K2_NO_K2_YET when the direct team has no K2 yet "
            "(0008V p.5, p.10); UNKNOWN is never converted to a factor."
        )
    return "OBSERVED", _require_percentage(k2_ntt, "k2_ntt", 100.0)


def calc_chubb_al_htktn_month(fyc_ntt: float, ehc_ntt: int, k2_ntt: Any, al_tenure_months: int = 15) -> float:
    """
    Chubb AL Monthly HT KTN (SRC-POL-CHB-002 p.5-6) INCLUDING symmetric negative FYC clawback!
    If fyc_ntt < 0 (valid cancellation/clawback adjustment), lookup tier on abs(fyc_ntt) and return negative fee!
    k2_ntt: observed K2 % of the direct team, or K2_NO_K2_YET ("chưa có phát sinh K2" -> 100%, p.5).
    None means UNKNOWN and raises ValueError.
    """
    fyc_ntt = _require_finite_float(fyc_ntt, "fyc_ntt")  # Negative allowed for valid symmetric clawback!
    ehc_ntt = _require_int(ehc_ntt, "ehc_ntt", 0)
    al_tenure_months = _require_int(al_tenure_months, "al_tenure_months", 1)
    abs_f = abs(fyc_ntt)
    high_ehc = ehc_ntt >= 4
    status, k2_val = _chubb_al_k2_status(k2_ntt)
    k2_fac = 1.00 if status == K2_NO_K2_YET else chubb_k2_factor(k2_val, allow_new_no_k2=False)
    if al_tenure_months >= 15:
        if abs_f >= 40.0:
            rate = 0.60 if high_ehc else 0.50
        elif abs_f >= 30.0:
            rate = 0.50 if high_ehc else 0.40
        elif abs_f >= 20.0:
            rate = 0.40 if high_ehc else 0.30
        elif abs_f >= 10.0:
            rate = 0.30 if high_ehc else 0.20
        elif abs_f >= 5.0:
            rate = 0.20 if high_ehc else 0.10
        else:
            rate = 0.0
    else:
        if abs_f >= 20.0:
            rate = 0.35 if high_ehc else 0.25
        elif abs_f >= 10.0:
            rate = 0.30 if high_ehc else 0.20
        elif abs_f >= 5.0:
            rate = 0.20 if high_ehc else 0.10
        else:
            rate = 0.0
    return fyc_ntt * rate * k2_fac


def calc_chubb_al_12m(
    monthly_fyc_ntt: List[float],
    monthly_ehc_ntt: List[int],
    k2_ntt: Any,  # observed K2 % or K2_NO_K2_YET; None = UNKNOWN -> ValueError
    al_tenure_start: int = 15,
    sub_l1_htktn_monthly: Optional[List[float]] = None,
    sub_l2_htktn_monthly: Optional[List[float]] = None,
    sub_l3_htktn_monthly: Optional[List[float]] = None,
    rank: str = "DM",
    new_ar_fyc_m1_6: float = 0.0,
    new_ar_fyc_m7_12: float = 0.0,
    still_um_al_at_m12: bool = True,
    new_um_indirect_monthly: float = 0.0,
    ch_mgt_gross_12m: float = 0.0,
    new_unit_fee_260009v_12m: float = 0.0,
    quarterly_ryc_ntt_y2_y5: Optional[List[float]] = None,
    quarterly_3maa_ntt: Optional[List[int]] = None,
) -> Dict[str, float]:
    """Full 12-month Chubb AL Manager calculation (excl. AL personal sales!).

    CHB-MG-008 (0008V p.9-10): quarterly persistency fee = RYC NTT (policy years 2-5) in quarter
    x 10% (3MAA NTT 2-4) / 15% (3MAA NTT >=5); requires AL tenure >=13 months and K2 NTT >=65%
    (K2_NO_K2_YET counts as met, p.10). Pass both inputs or neither: neither = fee not modeled;
    only one of them = MISSING_INPUT ValueError (a missing 3MAA is never treated as 0).
    """
    monthly_fyc_ntt = _require_vector(monthly_fyc_ntt, 12, "monthly_fyc_ntt", allow_negative=True)
    monthly_ehc_ntt = _require_int_vector(monthly_ehc_ntt, 12, "monthly_ehc_ntt", min_val=0)
    al_tenure_start = _require_int(al_tenure_start, "al_tenure_start", 1)
    if rank not in ("UM", "SM", "DM"):
        raise ValueError(f"Unsupported Chubb AL rank: {rank!r} (expected UM, SM, or DM)")
    new_ar_fyc_m1_6 = _require_non_negative_float(new_ar_fyc_m1_6, "new_ar_fyc_m1_6")
    new_ar_fyc_m7_12 = _require_non_negative_float(new_ar_fyc_m7_12, "new_ar_fyc_m7_12")
    new_um_indirect_monthly = _require_non_negative_float(new_um_indirect_monthly, "new_um_indirect_monthly")
    ch_mgt_gross_12m = _require_non_negative_float(ch_mgt_gross_12m, "ch_mgt_gross_12m")
    new_unit_fee_260009v_12m = _require_non_negative_float(new_unit_fee_260009v_12m, "new_unit_fee_260009v_12m")
    ht_m = [calc_chubb_al_htktn_month(monthly_fyc_ntt[m], monthly_ehc_ntt[m], k2_ntt, al_tenure_start + m) for m in range(12)]
    ht_q_total = 0.0
    for q in range(4):
        qf = sum(monthly_fyc_ntt[q * 3 : (q + 1) * 3])
        qm_fee = sum(ht_m[q * 3 : (q + 1) * 3])
        if qf >= 100.0:
            qr = 0.50
        elif qf >= 75.0:
            qr = 0.45
        elif qf >= 50.0:  # 0008V p.6: "Từ 50 đến dưới 75" -> 40%
            qr = 0.40
        elif qf >= 35.0:
            qr = 0.35
        elif qf >= 15.0:
            qr = 0.30
        else:
            qr = 0.0
        ht_q_total += qm_fee * qr

    l1_arr = _require_vector(
        sub_l1_htktn_monthly if sub_l1_htktn_monthly is not None else [0.0] * 12,
        12, "sub_l1_htktn_monthly", allow_negative=True,
    )
    l2_arr = _require_vector(
        sub_l2_htktn_monthly if sub_l2_htktn_monthly is not None else [0.0] * 12,
        12, "sub_l2_htktn_monthly", allow_negative=True,
    )
    l3_arr = _require_vector(
        sub_l3_htktn_monthly if sub_l3_htktn_monthly is not None else [0.0] * 12,
        12, "sub_l3_htktn_monthly", allow_negative=True,
    )
    ind_total = 0.0
    for m in range(12):
        f_ntt = monthly_fyc_ntt[m]
        if f_ntt < 15.0:
            r1 = r2 = r3 = 0.0
        elif f_ntt < 30.0:
            r1, r2, r3 = 0.30, 0.15, 0.075
        else:
            r1, r2, r3 = 0.50, 0.25, 0.125
        if rank == "UM":
            r2 = r3 = 0.0
        elif rank == "SM":
            r3 = 0.0
        ind_total += l1_arr[m] * r1 + l2_arr[m] * r2 + l3_arr[m] * r3

    recruit_m1_6 = new_ar_fyc_m1_6 * 0.10
    recruit_m7_12 = (new_ar_fyc_m7_12 * 0.10) if still_um_al_at_m12 else 0.0
    promo_dev_fee = min(15.0, new_um_indirect_monthly) * 12.0 if new_um_indirect_monthly > 0 else 0.0
    # CH Manager Add-On per 0008V p.12
    ch_mgt_addon = max(0.0, ch_mgt_gross_12m - (new_unit_fee_260009v_12m + promo_dev_fee))

    persistency_total = 0.0
    if (quarterly_ryc_ntt_y2_y5 is None) != (quarterly_3maa_ntt is None):
        raise ValueError(
            "MISSING_INPUT: CHB-MG-008 needs both quarterly_ryc_ntt_y2_y5 and quarterly_3maa_ntt "
            "(0008V p.9-10); a missing 3MAA is UNKNOWN, not 0."
        )
    if quarterly_ryc_ntt_y2_y5 is not None:
        ryc_q = _require_vector(quarterly_ryc_ntt_y2_y5, 4, "quarterly_ryc_ntt_y2_y5", allow_negative=True)
        maa_q = _require_int_vector(quarterly_3maa_ntt, 4, "quarterly_3maa_ntt")
        status, k2_val = _chubb_al_k2_status(k2_ntt)
        # 0008V p.10: "Trường hợp AL chưa phát sinh K2 NTT xem như đạt K2."
        k2_ok = status == K2_NO_K2_YET or k2_val >= 65.0
        for q in range(4):
            tenure_ok = (al_tenure_start + q * 3 + 2) >= 13
            rate = 0.15 if maa_q[q] >= 5 else (0.10 if maa_q[q] >= 2 else 0.0)
            if k2_ok and tenure_ok:
                persistency_total += ryc_q[q] * rate

    ht_m_sum = sum(ht_m)
    total_direct = ht_m_sum + ht_q_total
    total_all = total_direct + ind_total + recruit_m1_6 + recruit_m7_12 + promo_dev_fee + ch_mgt_addon + persistency_total
    ntt_sum = sum(monthly_fyc_ntt)
    return {
        "ntt_fyc_12m": round(ntt_sum, 4),
        "ht_ktn_monthly": round(ht_m_sum, 4),
        "ht_ktn_quarterly": round(ht_q_total, 4),
        "indirect_l1_l3": round(ind_total, 4),
        "recruit_m1_6": round(recruit_m1_6, 4),
        "recruit_m7_12_vested": round(recruit_m7_12, 4),
        "promo_dev_fee": round(promo_dev_fee, 4),
        "ch_mgt_addon": round(ch_mgt_addon, 4),
        "persistency_ryc_quarterly": round(persistency_total, 4),
        "total_earned": round(total_all, 4),
        "cash_paid_y1": round(total_all, 4),
        "direct_override_pct_fyc": round((total_direct / ntt_sum) * 100.0, 2) if ntt_sum > 0 else 0.0,
    }


def rd_growth_rate(q_fyp: float, prev_q_fyp: float) -> float:
    """
    Chubb RD Quarterly Business Growth payout rate (SRC-POL-CHB-003 p.8, scan), 12 levels:
    growth >=50%: 27.5% and -2.5 points per 5% step down to 0-<5%: 2.5%; growth <0%: 0%.
    Notes p.8: current-quarter FYP <360M and growth not negative -> 2.5%;
    FYP >=360M and comparison-quarter FYP <=0 or none -> 10%.
    """
    q_fyp = _require_finite_float(q_fyp, "q_fyp")
    prev_q_fyp = _require_finite_float(prev_q_fyp, "prev_q_fyp")
    if prev_q_fyp <= 0.0:
        return 0.10 if q_fyp >= 360.0 else 0.025
    g = (q_fyp - prev_q_fyp) / prev_q_fyp
    if g < 0.0:
        return 0.0
    if q_fyp < 360.0:
        return 0.025
    steps = min(10, int(math.floor(g / 0.05 + 1e-9)))  # 0-<5% -> 0 ... >=50% -> 10
    return 0.025 * (steps + 1)


def calc_chubb_rd_12m(
    monthly_direct_fyp: List[float],
    monthly_direct_fyc: List[float],
    monthly_direct_ehc: List[int],
    monthly_3maa: List[int],
    monthly_ryc: List[float],
    k2_pct: float,
    weighted_reported_fyp_monthly: float = 500.0,
    training_classes_monthly: int = 4,
    prior_year_q_fyp: Optional[List[float]] = None,
    legacy_holdback_2025: float = 0.0,
) -> Dict[str, float]:
    """Full 12-month Chubb RD calculation with Q1-Q2 (50%) vs Q3-Q4 (60%) K2 Binary Cliff!"""
    monthly_direct_fyp = _require_vector(monthly_direct_fyp, 12, "monthly_direct_fyp", allow_negative=True)
    monthly_direct_fyc = _require_vector(monthly_direct_fyc, 12, "monthly_direct_fyc", allow_negative=True)
    monthly_direct_ehc = _require_int_vector(monthly_direct_ehc, 12, "monthly_direct_ehc", min_val=0)
    monthly_3maa = _require_int_vector(monthly_3maa, 12, "monthly_3maa", min_val=0)
    monthly_ryc = _require_vector(monthly_ryc, 12, "monthly_ryc", allow_negative=True)
    k2_pct = _require_percentage(k2_pct, "k2_pct", 100.0)
    weighted_reported_fyp_monthly = _require_non_negative_float(weighted_reported_fyp_monthly, "weighted_reported_fyp_monthly")
    training_classes_monthly = _require_int(training_classes_monthly, "training_classes_monthly", 0)
    legacy_holdback_2025 = _require_non_negative_float(legacy_holdback_2025, "legacy_holdback_2025")
    base_q_fyp = _require_vector(prior_year_q_fyp, 4, "prior_year_q_fyp", allow_negative=True) if prior_year_q_fyp is not None else [sum(monthly_direct_fyp[0:3]) / 1.15] * 4
    train_total = act_total = biz_total = qual_m_total = 0.0

    for m in range(12):
        # II.1 Training
        t_base = 25.0 if weighted_reported_fyp_monthly >= 400.0 else 12.5
        t_mult = 1.0 if training_classes_monthly >= 4 else (0.75 if training_classes_monthly == 3 else (0.50 if training_classes_monthly == 2 else 0.0))
        train_total += t_base * t_mult

        # II.2 Activity (EHC) — 0003V p.6 (scan): 20+:8.0 | 16-19:6.5 | 12-15:5.0 | 9-11:3.5 | 6-8:2.5 | 4-5:1.5 | <4:0
        e = monthly_direct_ehc[m]
        act_total += (8.0 if e >= 20 else 6.5 if e >= 16 else 5.0 if e >= 12 else 3.5 if e >= 9
                      else 2.5 if e >= 6 else 1.5 if e >= 4 else 0.0)

        # II.3 Business (FYP) — 0003V p.6 (scan): 600+:12 | 480:9.5 | 360:7.0 | 270:5.0 | 180:3.5 | 120:2.5 | <120:0
        f = monthly_direct_fyp[m]
        biz_total += (12.0 if f >= 600 else 9.5 if f >= 480 else 7.0 if f >= 360 else 5.0 if f >= 270
                      else 3.5 if f >= 180 else 2.5 if f >= 120 else 0.0)

        # II.4 Quality 3MAA x K2 Binary Cliff (50% Q1-Q2 -> 60% Q3-Q4!)
        k2_gate = 1.0 if (k2_pct >= (50.0 if m < 6 else 60.0)) else 0.0
        a3 = monthly_3maa[m]
        r3 = 0.12 if a3 >= 12 else (0.10 if a3 >= 10 else (0.08 if a3 >= 8 else (0.06 if a3 >= 6 else (0.04 if a3 >= 4 else (0.02 if a3 >= 2 else 0.0)))))
        qual_m_total += monthly_direct_fyc[m] * r3 * k2_gate

    growth_q_total = 0.0
    ryc_q_total = 0.0
    for q in range(4):
        qf = sum(monthly_direct_fyp[q * 3 : (q + 1) * 3])
        qc = sum(monthly_direct_fyc[q * 3 : (q + 1) * 3])
        qr = sum(monthly_ryc[q * 3 : (q + 1) * 3])
        k2_gate = 1.0 if (k2_pct >= (50.0 if q < 2 else 60.0)) else 0.0

        prev_f = base_q_fyp[q]
        gr_rate = rd_growth_rate(qf, prev_f)
        growth_q_total += qc * gr_rate * k2_gate

        ryc_r = 0.30 if k2_pct >= 70 else (0.25 if k2_pct >= 60 else (0.20 if k2_pct >= 55 else (0.15 if k2_pct >= 50 else 0.10)))
        ryc_q_total += qr * ryc_r

    legacy_release = legacy_holdback_2025 * (1.0 if k2_pct >= 60 else (0.60 if k2_pct >= 50 else 0.0))
    total = train_total + act_total + biz_total + qual_m_total + growth_q_total + ryc_q_total
    return {
        "training_12m": round(train_total, 4),
        "activity_12m": round(act_total, 4),
        "business_12m": round(biz_total, 4),
        "quality_3maa_12m": round(qual_m_total, 4),
        "growth_quarterly_12m": round(growth_q_total, 4),
        "ryc_quarterly_12m": round(ryc_q_total, 4),
        "legacy_holdback_release": round(legacy_release, 4),
        "total_earned": round(total, 4),
        "cash_paid_y1": round(total + legacy_release, 4),
    }


# =============================================================================
# 5. MANULIFE PSM+ / HKD ENGINE (DUAL-PHASE APR 2026 + 3Y VESTING 30/30/40%)
# =============================================================================

def manulife_k2_factor(k2_pct: Optional[float], month_idx_1_to_12: int, allow_new_no_k2: bool = True) -> float:
    """Dual-phase K2 switch on 2026-04-01 (SRC-POL-MNL-001 p.2-3)."""
    month_idx_1_to_12 = _require_int(month_idx_1_to_12, "month_idx_1_to_12", 1, 12)
    if k2_pct is None:
        if not allow_new_no_k2:
            raise ValueError("k2_pct is None/UNKNOWN and allow_new_no_k2=False")
        return 1.00
    k2_val = _require_percentage(k2_pct, "k2_pct", 100.0)
    if month_idx_1_to_12 <= 3:  # Pre-Apr 2026
        if k2_val >= 75.0:
            return 1.15
        if k2_val >= 70.0:
            return 1.10
        if k2_val >= 65.0:
            return 1.05
        if k2_val >= 60.0:
            return 1.00
        if k2_val >= 55.0:
            return 0.90
        if k2_val >= 50.0:
            return 0.75
        return k2_val / 100.0
    else:  # Post-Apr 2026 (tightened!)
        if k2_val >= 80.0:
            return 1.10
        if k2_val >= 75.0:
            return 1.05
        if k2_val >= 70.0:
            return 1.00
        if k2_val >= 65.0:
            return 0.90
        if k2_val >= 60.0:
            return 0.70
        if k2_val >= 50.0:
            return 0.50
        return (k2_val / 100.0) / 2.0  # K2 / 2!


def calc_manulife_psm_12m(
    base_fee_monthly: float,  # 35.0 (PSM/SM/HKD1-2) or 45.0 (PSSM/SSM/HKD3-4)
    monthly_fyp_ach_pct: List[float],  # e.g. 1.15 = 115%
    monthly_direct_fyc: List[float],
    quarterly_1maa_ach_pct: List[float],
    k2_pct: float,
    indirect_prod_act_12m: float = 0.0,
    is_top15_national: bool = False,
) -> Dict[str, float]:
    """Full 12-month Manulife PSM+/HKD engine with Apr-2026 switch & 3Y 30/30/40% deferral."""
    base_fee_monthly = _require_positive_float(base_fee_monthly, "base_fee_monthly")
    monthly_fyp_ach_pct = _require_vector(monthly_fyp_ach_pct, 12, "monthly_fyp_ach_pct", allow_negative=False)
    monthly_direct_fyc = _require_vector(monthly_direct_fyc, 12, "monthly_direct_fyc", allow_negative=True)
    quarterly_1maa_ach_pct = _require_vector(quarterly_1maa_ach_pct, 4, "quarterly_1maa_ach_pct", allow_negative=False)
    k2_pct = _require_percentage(k2_pct, "k2_pct", 100.0)
    indirect_prod_act_12m = _require_finite_float(indirect_prod_act_12m, "indirect_prod_act_12m")
    base_total = 0.0
    prod_total = 0.0
    for m in range(12):
        ach = monthly_fyp_ach_pct[m]
        b = 0.0 if ach < 0.30 else min(base_fee_monthly * 1.50, base_fee_monthly * ach * 1.30)
        base_total += b

        rate = 0.08 if ach >= 1.15 else 0.06
        prod_total += monthly_direct_fyc[m] * rate * manulife_k2_factor(k2_pct, m + 1)

    act_q_total = 0.0
    for q in range(4):
        a_ach = quarterly_1maa_ach_pct[q]
        r_a = 0.05 if a_ach >= 1.20 else (0.035 if a_ach >= 1.10 else (0.025 if a_ach >= 1.00 else (0.01 if a_ach >= 0.90 else 0.0)))
        qfyc = sum(monthly_direct_fyc[q * 3 : (q + 1) * 3])
        k2_end_q = manulife_k2_factor(k2_pct, (q + 1) * 3)
        act_q_total += qfyc * r_a * k2_end_q

    ind_50 = indirect_prod_act_12m * 0.50
    avg_fyp_ach = sum(monthly_fyp_ach_pct) / 12.0
    qualifies_lt = (k2_pct >= 70.0) and (avg_fyp_ach >= 0.85 or is_top15_national)
    lt_raw = 0.75 * (prod_total + act_q_total) + 0.25 * ind_50
    lt_deferred = min(12.0 * base_fee_monthly, lt_raw) if qualifies_lt else 0.0

    cash_y1 = base_total + prod_total + act_q_total + ind_50
    total_earned = cash_y1 + lt_deferred
    return {
        "base_fee_12m": round(base_total, 4),
        "productivity_12m": round(prod_total, 4),
        "activity_quarterly_12m": round(act_q_total, 4),
        "indirect_50pct": round(ind_50, 4),
        "long_term_deferred_3y": round(lt_deferred, 4),
        "vest_y1_30pct": round(lt_deferred * 0.30, 4),
        "vest_y2_30pct": round(lt_deferred * 0.30, 4),
        "vest_y3_40pct": round(lt_deferred * 0.40, 4),
        "cash_paid_y1": round(cash_y1, 4),
        "total_earned": round(total_earned, 4),
    }


# =============================================================================
# 5b. MANULIFE AGENT (0046M01/2026/ASBD) & UM+ (0047M01/2026/ASBD)
# =============================================================================

def manulife_agent_k2_factor(k2: Any, month_idx_1_to_12: int) -> float:
    """0046M01 p.1 muc A.I: he so nhan TLDTHD cho THUONG dai ly (khac bang cua UM+/PSM+).
    Truoc 04/2026: <40% = TLDTHD thuc dat | 40-<55: 50% | 55-<65: 75% | >=65: 100%.
    Tu 04/2026:   <50% = TLDTHD/2 | 50-<60: 50% | 60-<65: 70% | 65-<70: 90% | >=70: 100%.
    "Chua co TLDTHD" = 100%: truyen K2_NO_K2_YET; None = UNKNOWN -> ValueError.
    """
    month_idx_1_to_12 = _require_int(month_idx_1_to_12, "month_idx_1_to_12", 1, 12)
    status, v = _chubb_al_k2_status(k2)
    if status == K2_NO_K2_YET:
        return 1.0
    if month_idx_1_to_12 <= 3:
        return v / 100.0 if v < 40 else (0.50 if v < 55 else (0.75 if v < 65 else 1.00))
    return (v / 100.0) / 2.0 if v < 50 else (0.50 if v < 60 else (0.70 if v < 65 else (0.90 if v < 70 else 1.00)))


def _manulife_um_k2_factor(k2: Any, month_idx_1_to_12: int) -> float:
    """0047M01 p.2 (= bang 0048M01 p.2): he so nhan TLDTHD cap bao cao truc tiep cua UM+."""
    status, v = _chubb_al_k2_status(k2)
    return 1.0 if status == K2_NO_K2_YET else manulife_k2_factor(v, month_idx_1_to_12, allow_new_no_k2=False)


MANULIFE_PRO_TITLES = (None, "Bac", "Vang", "BachKim")


def calc_manulife_agent_12m(
    monthly_fyc: List[float],
    monthly_fyp: List[float],
    monthly_cc: List[int],
    k2: Any,
    tenure_months_start: int = 13,
    pro_title: Optional[str] = None,
    clkd_factor: float = 1.0,
    monthly_ryc: Optional[List[float]] = None,
    monthly_new_recruit_productive: Optional[List[bool]] = None,
) -> Dict[str, Any]:
    """Manulife agent 12 thang theo 0046M01/2026/ASBD (trieu VND).

    Hoa hong co ban KHONG co trong 0046M01 (muc C.1 p.9 dan chieu thong bao theo san pham): FYC/RYC la dau vao.
    B.III thuong nang suat thang [p.4]; B.IV xuat sac thang (chi Manulife Pro) [p.4-5]; B.V nang suat quy [p.5-6];
    B.VI KDXS nam (chi Pro Vang/Bach Kim, tra cham 50/30/20) [p.6-7]; B.VII M-Star quy/nam [p.7-8];
    B.VIII KKPTKDHT [p.8]. B.I/B.II (dai ly moi) khong mo hinh o day (chi cho 2 thang dau).
    pro_title: None (khong co danh hieu — tieu chi 0011M04/2024 khong co trong nguon) | 'Bac' | 'Vang' | 'BachKim'.
    """
    fyc = _require_vector(monthly_fyc, 12, "monthly_fyc", allow_negative=True)
    fyp = _require_vector(monthly_fyp, 12, "monthly_fyp", allow_negative=True)
    cc = _require_int_vector(monthly_cc, 12, "monthly_cc", min_val=0)
    tenure_months_start = _require_int(tenure_months_start, "tenure_months_start", 1)
    clkd_factor = _require_rate_0_to_1(clkd_factor, "clkd_factor", allow_zero=True)
    if pro_title not in MANULIFE_PRO_TITLES:
        raise ValueError(f"pro_title must be one of {MANULIFE_PRO_TITLES}")
    ryc = _require_vector(monthly_ryc if monthly_ryc is not None else [0.0] * 12, 12, "monthly_ryc", allow_negative=True)
    recruit = monthly_new_recruit_productive if monthly_new_recruit_productive is not None else [False] * 12
    if len(recruit) != 12 or not all(isinstance(x, bool) for x in recruit):
        raise ValueError("monthly_new_recruit_productive must be 12 booleans")

    pre = [fyc[0], fyc[0]] if tenure_months_start >= 3 else [0.0, 0.0]
    monthly_bonus = [0.0] * 12
    excellence = [0.0] * 12
    kkpt = [0.0] * 12
    for m in range(12):
        tenure = tenure_months_start + m
        roll = sum((pre + fyc[: m + 1])[-3:])
        le6 = tenure <= 6
        tiers = [(100.0, 0.50), (80.0, 0.35), (60.0, 0.30), (45.0, 0.25), (30.0, 0.20), (15.0, 0.15), (10.0, 0.10), (5.0, 0.05)]
        rate = 0.0
        for thr, r in tiers:
            if (thr == 100.0 and le6) or (thr == 5.0 and not le6):
                continue
            if roll >= thr:
                rate = r
                break
        k2f = manulife_agent_k2_factor(k2, m + 1)
        if cc[m] >= 1:
            monthly_bonus[m] = rate * fyc[m] * k2f * clkd_factor
        if pro_title is not None:
            col = {"Bac": 0, "Vang": 1, "BachKim": 2}[pro_title]
            table = [(100.0, (None, None, 16.0)), (80.0, (None, None, 12.0)), (60.0, (None, 7.0, 10.0)), (45.0, (None, 5.0, 8.0)),
                     (30.0, (3.0, 3.0, 4.0)), (15.0, (1.5, 1.5, 2.0))]
            amt = 0.0
            for thr, amts in table:
                if fyp[m] >= thr and amts[col] is not None:
                    amt = amts[col]
                    break
            excellence[m] = amt * k2f * clkd_factor
        if recruit[m] and cc[m] >= 1 and fyc[m] >= 4.0:
            kkpt[m] = min(3.0, 0.20 * fyc[m]) * k2f * clkd_factor

    quarterly = [0.0] * 4
    mstar_q = [0.0] * 4
    mstar_targets = [160.0, 430.0, 750.0, 1073.6452]
    mstar_amts = [(5.0, 8.0), (8.0, 12.0), (10.0, 15.0), (0.0, 20.0)]
    for q in range(4):
        qf = sum(fyc[q * 3:(q + 1) * 3])
        tenure_end = tenure_months_start + q * 3 + 2
        excellent = all(monthly_bonus[q * 3 + i] > 0 for i in range(3)) or pro_title in ("Vang", "BachKim")
        qtiers = [(120.0, 0.10), (100.0, 0.08), (80.0, 0.06), (60.0, 0.05), (45.0, 0.04), (30.0, 0.03), (15.0, 0.02)]
        rate = 0.0
        for thr, r in qtiers:
            if thr == 15.0 and tenure_end > 6:
                continue
            if qf >= thr:
                rate = r
                break
        if excellent:
            rate *= 2.0
        k2q = manulife_agent_k2_factor(k2, (q + 1) * 3)
        quarterly[q] = rate * qf * k2q * clkd_factor
        cum = sum(fyp[: (q + 1) * 3])
        active_all = all(cc[q * 3 + i] >= 1 and fyc[q * 3 + i] >= 4.0 for i in range(3))
        ach = cum / mstar_targets[q]
        if active_all and ach >= 1.0:
            mstar_q[q] = mstar_amts[q][1] * k2q * clkd_factor
        elif active_all and ach >= 0.90:
            mstar_q[q] = mstar_amts[q][0] * k2q * clkd_factor
    fyp_y = sum(fyp)
    m_y = 100.0 if fyp_y >= 3000.0 else (75.0 if fyp_y >= 2000.0 else (55.0 if fyp_y >= 1073.6452 else 0.0))
    mstar_y = max(0.0, m_y * manulife_agent_k2_factor(k2, 12) * clkd_factor - sum(mstar_q))

    kdxs = 0.0
    status, k2v = _chubb_al_k2_status(k2)
    k2_ok_70 = status == K2_NO_K2_YET or k2v >= 70.0
    cc_y, fyc_y = sum(cc), sum(fyc)
    if pro_title == "BachKim" and cc_y >= 24 and fyp_y >= 600.0 and k2_ok_70:
        kdxs = min(100.0, 0.15 * fyc_y) * clkd_factor
    elif pro_title in ("Vang", "BachKim"):
        need_cc, need_fyp = (15, 360.0) if tenure_months_start > 12 else (10, 240.0)
        if cc_y >= need_cc and fyp_y >= need_fyp and k2_ok_70:
            kdxs = min(100.0, 0.10 * fyc_y) * clkd_factor

    earned_bonus = sum(monthly_bonus) + sum(excellence) + sum(quarterly) + sum(mstar_q) + mstar_y + sum(kkpt)
    total = fyc_y + sum(ryc) + earned_bonus + kdxs
    # Tiền thực trả năm hiện tại: KHÔNG gồm M-Star năm (trả kỳ thu nhập tháng 2 năm sau [0046M01_2026 : 8])
    # và KDXS năm (trả 50/30/20% trong 3 năm sau [0046M01_2026 : 7]).
    deferred_next_years = mstar_y + kdxs
    cash_bonus = earned_bonus
    return {
        "fyc_total": round(fyc_y, 4),
        "ryc_total": round(sum(ryc), 4),
        "bonus_monthly_productivity": round(sum(monthly_bonus), 4),
        "bonus_monthly_excellence_pro": round(sum(excellence), 4),
        "bonus_quarterly_productivity": round(sum(quarterly), 4),
        "bonus_mstar_quarterly": round(sum(mstar_q), 4),
        "bonus_mstar_annual": round(mstar_y, 4),
        "bonus_kkptkdht": round(sum(kkpt), 4),
        "bonus_annual_kdxs_deferred_50_30_20": round(kdxs, 4),
        "total_bonuses_earned": round(cash_bonus + kdxs, 4),
        "total_earned": round(total, 4),
        "cash_paid_y1": round(total - deferred_next_years, 4),
        "paid_next_years": round(deferred_next_years, 4),
        "monthly_bonus_by_month": [round(x, 6) for x in monthly_bonus],
        "quarterly_bonus_by_quarter": [round(x, 6) for x in quarterly],
    }


def calc_manulife_um_12m(
    monthly_level_fyc: List[Sequence[float]],
    monthly_direct_producing: List[int],
    monthly_direct_bonus_base: List[float],
    k2_direct: Any,
    mba_pro_title: Optional[str] = None,
    monthly_direct_new_agent_bonus: Optional[List[float]] = None,
    attendance_ok: bool = True,
) -> Dict[str, float]:
    """Manulife UM+ 12 thang theo 0047M01/2026/ASBD (trieu VND).

    monthly_level_fyc[m] = (FYC cap 1, cap 2, cap 3, cap 4) trong thang; cap 1 KHONG gom FYC cua chinh UM+ [p.1].
    A.I nang suat nhom [p.1]: cap 1 theo FYC cap 1: >=48: 20% | 24-<48: 16% | 7-<24: 14% | <7: 10%; cap 2-4 = 1/2 ty le cap lien tren.
    A.II hoat dong nhom [p.1-2]: ty le theo so DL/UM+ cap 1 co san xuat (>=4tr FYC & >=1 CC) x tong thuong nang suat
         thang + quy (0046M01 B.III, B.V) cua cap 1 nhan trong thang x he so TLDTHD [p.2].
         MBA Pro: >=6:125% | 4-5:100% | 2-3:75% | 1:30%; UM+ khac: 60/50/40/30%.
    A.III phat trien DL moi Manulife Pro [p.3-4]: MBA Pro 100% / khac 50% x thuong DL moi cua cap 1 x he so TLDTHD.
    A.V hop tac dai han [p.5-6]: chi MBA Pro (Bac 80 | Vang 100 | BachKim 125%) x tong (A.II + A.III) cua thang du dieu kien;
         tra cham 30/30/40%. Tieu chi MBA Pro (0050M01/2026) khong co trong nguon -> mba_pro_title=None la gia dinh.
    A.IV phat trien nhom moi (210%, tran 30tr) chi phat sinh khi co DL thang cap UM lan dau — khong mo hinh o day.
    attendance_ok: dieu kien "Doi ngu chuyen can" >=4 buoi/thang [p.3]; False -> khong nhan phi.
    """
    if len(monthly_level_fyc) != 12:
        raise ValueError("monthly_level_fyc must have 12 months")
    levels = [_require_vector(list(x), 4, f"monthly_level_fyc[{i}]", allow_negative=True) for i, x in enumerate(monthly_level_fyc)]
    prod = _require_int_vector(monthly_direct_producing, 12, "monthly_direct_producing", min_val=0)
    base = _require_vector(monthly_direct_bonus_base, 12, "monthly_direct_bonus_base", allow_negative=True)
    newb = _require_vector(monthly_direct_new_agent_bonus if monthly_direct_new_agent_bonus is not None else [0.0] * 12, 12,
                           "monthly_direct_new_agent_bonus", allow_negative=True)
    titles = {None: 0.0, "Bac": 0.80, "Vang": 1.00, "BachKim": 1.25}
    if mba_pro_title not in titles:
        raise ValueError(f"mba_pro_title must be one of {list(titles)}")
    if not isinstance(attendance_ok, bool):
        raise ValueError("attendance_ok must be bool")
    is_mba = mba_pro_title is not None
    a1 = a2 = a3 = lt_base = 0.0
    for m in range(12):
        if not attendance_ok:
            continue
        c1 = levels[m][0]
        r = 0.20 if c1 >= 48 else (0.16 if c1 >= 24 else (0.14 if c1 >= 7 else 0.10))
        fee1 = 0.0
        for lv in range(4):
            fee1 += levels[m][lv] * r / (2 ** lv)
        a1 += fee1
        n = prod[m]
        if is_mba:
            r2 = 1.25 if n >= 6 else (1.00 if n >= 4 else (0.75 if n >= 2 else (0.30 if n >= 1 else 0.0)))
        else:
            r2 = 0.60 if n >= 6 else (0.50 if n >= 4 else (0.40 if n >= 2 else (0.30 if n >= 1 else 0.0)))
        k2f = _manulife_um_k2_factor(k2_direct, m + 1)
        fee2 = r2 * base[m] * k2f
        fee3 = (1.00 if is_mba else 0.50) * newb[m] * k2f
        a2 += fee2
        a3 += fee3
        if n >= 2 and (fee2 + fee3) > 0:
            lt_base += fee2 + fee3
    lt = titles[mba_pro_title] * lt_base
    cash = a1 + a2 + a3
    return {
        "a1_team_productivity": round(a1, 4),
        "a2_team_activity": round(a2, 4),
        "a3_new_agent_development": round(a3, 4),
        "a5_long_term_deferred_30_30_40": round(lt, 4),
        "cash_paid_y1": round(cash, 4),
        "total_earned": round(cash + lt, 4),
    }


# =============================================================================
# 6. PROPOSED BALANCED / HYBRID SCHEME (PROPOSAL — SYNTHETIC ASSUMPTION)
# =============================================================================

@dataclass
class ProposalParams:
    """PO-configurable parameters for W24 Proposed Balanced/Hybrid Scheme."""
    name: str = "W24_Balanced_Hybrid_Primary"
    ul_y1_fyc_rate: float = 0.30           # Modeling input pending legal verification
    topup_commission_rate: float = 0.00    # Modeling input pending legal verification
    k2_hard_floor_pct: float = 60.0        # Below 60% -> 0% bonus (avoids Chubb soft 25% & AIA 70% cliff shock)
    k2_holdback_t1_threshold: float = 65.0 # Below 65% or New -> T+1 cash settlement
    agent_m_tier_rates: Tuple[float, float, float, float, float] = (0.08, 0.16, 0.24, 0.32, 0.38)
    agent_m_tier_thresholds: Tuple[float, float, float, float, float] = (5.0, 12.0, 22.0, 35.0, 55.0)
    agent_q_consistency_3m: float = 0.12   # +12% on monthly bonus when 3M active
    agent_annual_mdrt_rate: float = 0.10   # +10% on annual FYC >= 400M (MDRT tier)
    agent_ryc_bonus_rate: float = 0.25     # +25% on Y2 SYC/RYC when K2 >= 75%
    mgr_direct_base_rate: float = 0.30     # Direct override base rate before K2 multiplier
    mgr_direct_max_rate: float = 0.36      # Direct override max 36% FYC NTT (vs Chubb 108%!)
    mgr_indirect_gate_fyc: float = 15.0    # Learned from Chubb: 0% indirect if NTT < 15M/M
    mgr_indirect_l1_rate: float = 0.35     # Max 3 gens (35/17.5/8.75%), NO infinite chain
    mgr_deferred_3y_rate: float = 0.12     # 12% of direct FYC deferred 30/30/40% gated K2 >= 75%
    rd_base_monthly: float = 35.0          # KPI-linked 30% floor / 140% cap (learned from Manulife)
    rd_direct_fyc_rate: float = 0.07       # Monthly override x K2
    rd_deferred_3y_share: float = 0.60     # 60% of variable RD override deferred 30/30/40% (K2>=75%)


def _validate_proposal_params(p: ProposalParams) -> None:
    _require_rate_0_to_1(p.ul_y1_fyc_rate, "ProposalParams.ul_y1_fyc_rate", allow_zero=False)
    _require_rate_0_to_1(p.topup_commission_rate, "ProposalParams.topup_commission_rate", allow_zero=True)
    _require_percentage(p.k2_hard_floor_pct, "ProposalParams.k2_hard_floor_pct", 100.0)
    _require_percentage(p.k2_holdback_t1_threshold, "ProposalParams.k2_holdback_t1_threshold", 100.0)
    rates = _require_vector(p.agent_m_tier_rates, 5, "ProposalParams.agent_m_tier_rates")
    thresholds = _require_vector(p.agent_m_tier_thresholds, 5, "ProposalParams.agent_m_tier_thresholds")
    for i, r in enumerate(rates):
        _require_rate_0_to_1(r, f"ProposalParams.agent_m_tier_rates[{i}]")
    if any(lower >= upper for lower, upper in zip(thresholds, thresholds[1:])):
        raise ValueError("ProposalParams.agent_m_tier_thresholds must be strictly increasing")
    _require_rate_0_to_1(p.agent_q_consistency_3m, "ProposalParams.agent_q_consistency_3m")
    _require_rate_0_to_1(p.agent_annual_mdrt_rate, "ProposalParams.agent_annual_mdrt_rate")
    _require_rate_0_to_1(p.agent_ryc_bonus_rate, "ProposalParams.agent_ryc_bonus_rate")
    _require_rate_0_to_1(p.mgr_direct_base_rate, "ProposalParams.mgr_direct_base_rate")
    _require_rate_0_to_1(p.mgr_direct_max_rate, "ProposalParams.mgr_direct_max_rate")
    _require_non_negative_float(p.mgr_indirect_gate_fyc, "ProposalParams.mgr_indirect_gate_fyc")
    _require_rate_0_to_1(p.mgr_indirect_l1_rate, "ProposalParams.mgr_indirect_l1_rate")
    _require_rate_0_to_1(p.mgr_deferred_3y_rate, "ProposalParams.mgr_deferred_3y_rate")
    _require_non_negative_float(p.rd_base_monthly, "ProposalParams.rd_base_monthly")
    _require_rate_0_to_1(p.rd_direct_fyc_rate, "ProposalParams.rd_direct_fyc_rate")
    _require_rate_0_to_1(p.rd_deferred_3y_share, "ProposalParams.rd_deferred_3y_share")


def proposal_k2_factor(k2_pct: Optional[float], hard_floor: float = 60.0, allow_new_no_k2: bool = False) -> float:
    """
    Proposal K2 multiplier. Rejects None/UNKNOWN unless allow_new_no_k2=True (explicit new agent without K2 history).
    Prevents silent conversion of missing/UNKNOWN K2 into 1.00.
    """
    hf = _require_percentage(hard_floor, "hard_floor", 100.0)
    if k2_pct is None:
        if not allow_new_no_k2:
            raise ValueError("k2_pct is None/UNKNOWN; pass allow_new_no_k2=True only for explicit new agents without K2 history")
        return 1.00
    val = _require_percentage(k2_pct, "k2_pct", 100.0)
    if val >= 85.0:
        return 1.20
    if val >= 80.0:
        return 1.10
    if val >= 75.0:
        return 1.00
    if val >= 70.0:
        return 0.85
    if val >= hf:
        return 0.60
    return 0.00


def calc_proposal_agent_12m(
    monthly_fyc: List[float],
    monthly_syc: List[float],
    k2_pct: Optional[float],
    is_new_agent: bool = False,
    params: Optional[ProposalParams] = None,
) -> Dict[str, float]:
    p = params or ProposalParams()
    _validate_proposal_params(p)
    monthly_fyc = _require_vector(monthly_fyc, 12, "monthly_fyc", allow_negative=True)
    monthly_syc = _require_vector(monthly_syc, 12, "monthly_syc", allow_negative=True)
    k2_fac = proposal_k2_factor(k2_pct, p.k2_hard_floor_pct, allow_new_no_k2=is_new_agent)
    m_bonuses = []
    for m in range(12):
        f = monthly_fyc[m]
        rate = 0.0
        for th, r in zip(reversed(p.agent_m_tier_thresholds), reversed(p.agent_m_tier_rates)):
            if f >= th:
                rate = r
                break
        m_bonuses.append(f * rate * k2_fac)

    # Onboarding structured bonus M1-M6 (3M/M if >=8M FYC, 50% held to M12)
    onb_cash = 0.0
    onb_m12 = 0.0
    if is_new_agent:
        for m in range(6):
            if monthly_fyc[m] >= 8.0:
                onb_cash += 1.5
                onb_m12 += 1.5

    q_cons = 0.0
    for q in range(4):
        sl = monthly_fyc[q * 3 : (q + 1) * 3]
        if all(x >= 4.0 for x in sl):
            q_cons += sum(m_bonuses[q * 3 : (q + 1) * 3]) * p.agent_q_consistency_3m

    fyc_y = sum(monthly_fyc)
    syc_y = sum(monthly_syc)
    mdrt_b = (fyc_y * p.agent_annual_mdrt_rate * k2_fac) if fyc_y >= 400.0 else 0.0
    ryc_b = (syc_y * p.agent_ryc_bonus_rate) if (k2_pct is not None and k2_pct >= 75.0) else 0.0

    # Defer 30% of annual MDRT bonus into Y2 gated on K2 >= 75%
    deferred_post_y1 = mdrt_b * 0.30
    hold_t1 = (k2_pct is None) or (k2_pct < p.k2_holdback_t1_threshold)
    accrued_t1 = m_bonuses[11] if hold_t1 else 0.0

    total_bonuses = sum(m_bonuses) + onb_cash + onb_m12 + q_cons + mdrt_b + ryc_b
    total_earned = fyc_y + syc_y + total_bonuses
    cash_paid_y1 = total_earned - deferred_post_y1 - accrued_t1
    implied_fyp = fyc_y / p.ul_y1_fyc_rate

    return {
        "fyc_total": round(fyc_y, 4),
        "syc_total": round(syc_y, 4),
        "implied_fyp": round(implied_fyp, 4),
        "bonus_monthly": round(sum(m_bonuses), 4),
        "bonus_onboarding_cash": round(onb_cash, 4),
        "bonus_onboarding_m12": round(onb_m12, 4),
        "bonus_q_consistency": round(q_cons, 4),
        "bonus_annual_mdrt": round(mdrt_b, 4),
        "bonus_ryc": round(ryc_b, 4),
        "total_bonuses_earned": round(total_bonuses, 4),
        "total_earned": round(total_earned, 4),
        "cash_paid_y1": round(cash_paid_y1, 4),
        "deferred_post_y1": round(deferred_post_y1, 4),
        "accrued_t_plus_1_unpaid": round(accrued_t1, 4),
        "pct_of_fyc": round((total_earned / fyc_y) * 100.0, 2) if fyc_y > 0 else 0.0,
        "bonus_pct_of_fyp": round((total_bonuses / implied_fyp) * 100.0, 2) if implied_fyp > 0 else 0.0,
    }


# =============================================================================
# 7. ENTERPRISE TOTAL DISTRIBUTION COST (ZERO DOUBLE COUNTING + ART. 52 CHECK)
# =============================================================================

def calc_enterprise_hierarchy_cost(
    scheme: str,
    k2_pct: float = 82.0,
    ul_fyc_rate: float = 0.30,
    home_office_opex_pct_fyp: float = 0.20,
    params: Optional["ProposalParams"] = None,
) -> Dict[str, float]:
    """
    Standard Regional Hierarchy (1 Region = 12,000M FYP/year = 3,600M FYC/year):
    - Revenue counted ONCE: 12,000M FYP (1,000M/month)
    - Org: 1 Regional Leader -> 4 Direct Managers (each 75M FYC/M = 900M/Y)
           -> 20 Active Agents (5 per manager, each 15M FYC/M = 180M/Y, 3M active/Q)
    All payouts stacked across tiers without double-counting revenue!
    """
    k2_pct = _require_percentage(k2_pct, "k2_pct", 100.0)
    ul_fyc_rate = _require_rate_0_to_1(ul_fyc_rate, "ul_fyc_rate", allow_zero=False)
    home_office_opex_pct_fyp = _require_rate_0_to_1(home_office_opex_pct_fyp, "home_office_opex_pct_fyp", allow_zero=True)
    annual_fyp = 12000.0
    annual_fyc = annual_fyp * ul_fyc_rate  # 3,600M
    agent_m_fyc = [15.0] * 12  # 20 agents * 15M = 300M/M = 3,600M/Y
    agent_m_syc = [0.0] * 12   # Isolate Y1 new-business acquisition cost cleanly
    mgr_m_fyc = [75.0] * 12    # 4 managers * 75M = 300M/M

    if scheme == "AIA_Alpha_2026" or scheme == "AIA_Alpha_2027":
        yr = 2026 if scheme == "AIA_Alpha_2026" else 2027
        ag = calc_aia_cvtv_12m(agent_m_fyc, agent_m_syc, fy_pct=k2_pct, policy_year=yr, assumed_fyc_to_fyp_rate=ul_fyc_rate)
        ag_bonuses_all = ag["total_bonuses_earned"] * 20.0
        mg = calc_aia_cql_12m(mgr_m_fyc, [5] * 12, fy_pct=k2_pct, tot_pct=max(85.0, k2_pct))
        # 2 senior managers also get 50% Gen2 indirect on 2 peer/sub managers' direct monthly base
        mg_direct_all = (mg["direct_monthly"] + mg["activity_monthly"] + mg["premier_quarterly"]) * 4.0
        mg_deferred_all = mg["annual_deferred_3y"] * 4.0
        mg_indirect_all = (mg["direct_monthly"] * 0.50) * 2.0
        # 1 PAF+ leader (SAF rank, Year 1 target = 5,000M -> 12,000M exceeds target)
        paf = calc_aia_paf_12m("SAF", 1, [1000.0] * 12, [300.0] * 12, [20.0] * 12, fy_pct=k2_pct)
        rd_cash = paf["cash_paid_y1"]
        rd_deferred = 0.0
        art52_newbiz_bonuses = ag_bonuses_all

    elif scheme == "Chubb_Agency_2026":
        ag = calc_chubb_ar_12m(agent_m_fyc, agent_m_syc, [True] * 12, k2_pct=k2_pct, tenure_months_start=13, assumed_fyc_to_fyp_rate=ul_fyc_rate)
        ag_bonuses_all = ag["total_bonuses_earned"] * 20.0
        mg = calc_chubb_al_12m(mgr_m_fyc, [5] * 12, k2_ntt=k2_pct, al_tenure_start=15)
        mg_direct_all = (mg["ht_ktn_monthly"] + mg["ht_ktn_quarterly"]) * 4.0
        mg_deferred_all = 0.0
        mg_indirect_all = (mg["ht_ktn_monthly"] * 0.50) * 2.0
        rd = calc_chubb_rd_12m([1000.0] * 12, [300.0] * 12, [20] * 12, [20] * 12, [0.0] * 12, k2_pct=k2_pct)
        rd_cash = rd["total_earned"]
        rd_deferred = 0.0
        art52_newbiz_bonuses = ag_bonuses_all

    elif scheme == "W24_Proposed_Balanced":
        p = params or ProposalParams()
        ag = calc_proposal_agent_12m(agent_m_fyc, agent_m_syc, k2_pct=k2_pct, params=p)
        ag_bonuses_all = ag["total_bonuses_earned"] * 20.0
        k2_fac = proposal_k2_factor(k2_pct, p.k2_hard_floor_pct)
        mg_direct_all = annual_fyc * min(p.mgr_direct_max_rate, p.mgr_direct_base_rate * k2_fac)
        mg_indirect_all = (mg_direct_all * 0.50) * p.mgr_indirect_l1_rate  # 2 sub-managers
        mg_deferred_all = annual_fyc * p.mgr_deferred_3y_rate if k2_pct >= 75.0 else 0.0
        rd_base = p.rd_base_monthly * 12.0 * min(1.40, 1.05 * 1.25)  # 105% FYP ach -> 131.25%
        rd_var = annual_fyc * p.rd_direct_fyc_rate * k2_fac
        rd_deferred = rd_var * p.rd_deferred_3y_share if k2_pct >= 75.0 else 0.0
        rd_cash = rd_base + rd_var
        art52_newbiz_bonuses = ag_bonuses_all
    else:
        raise ValueError(f"Unsupported enterprise scheme: {scheme}")

    total_earned = annual_fyc + ag_bonuses_all + mg_direct_all + mg_indirect_all + mg_deferred_all + rd_cash + rd_deferred
    total_deferred = mg_deferred_all + rd_deferred
    total_cash_y1 = total_earned - total_deferred

    cost_pct_fyp = total_earned / annual_fyp
    cash_y1_pct_fyp = total_cash_y1 / annual_fyp
    art52_bonus_pct_fyp = art52_newbiz_bonuses / annual_fyp
    persisted_y2_fyp = annual_fyp * (k2_pct / 100.0)
    cost_per_persisted_y2_fyp = total_earned / persisted_y2_fyp if persisted_y2_fyp > 0 else 0.0
    breakeven_gross_margin_pct = (cost_pct_fyp + home_office_opex_pct_fyp) * 100.0

    return {
        "scheme": scheme,
        "k2_pct": k2_pct,
        "annual_fyp": annual_fyp,
        "layer_a_commission": round(annual_fyc, 2),
        "layer_b_agent_bonuses": round(ag_bonuses_all, 2),
        "layer_c_mgr_direct": round(mg_direct_all, 2),
        "layer_d_mgr_indirect": round(mg_indirect_all, 2),
        "layer_e_rd_cash": round(rd_cash, 2),
        "layer_f_deferred_3y": round(total_deferred, 2),
        "total_earned_vnd_m": round(total_earned, 2),
        "total_cash_y1_vnd_m": round(total_cash_y1, 2),
        "earned_pct_fyp": round(cost_pct_fyp * 100.0, 2),
        "cash_y1_pct_fyp": round(cash_y1_pct_fyp * 100.0, 2),
        "art52_bonus_pct_fyp": round(art52_bonus_pct_fyp * 100.0, 2),
        "art52_pass_30pct_cap": art52_bonus_pct_fyp <= 0.30,
        "cost_per_persisted_y2_pct": round(cost_per_persisted_y2_fyp * 100.0, 2),
        "breakeven_gross_margin_pct": round(breakeven_gross_margin_pct, 2),
        # Per-role income on the same standard tree (Earned incl. deferred; VND million / person / year).
        # Agent: 15M FYC/M (commission + bonuses). Direct manager: own override layer only (1 of 4).
        # Indirect: extra indirect override for each of the 2 senior managers. Leader: RD/PAF+ tier.
        "role_agent_earned": round((annual_fyc + ag_bonuses_all) / 20.0, 2),
        "role_mgr_direct_earned": round((mg_direct_all + mg_deferred_all) / 4.0, 2),
        "role_mgr_indirect_extra": round(mg_indirect_all / 2.0, 2),
        "role_leader_earned": round(rd_cash + rd_deferred, 2),
    }


# =============================================================================
# 8. MAPA FORWARD & REVERSE ENGINE
# =============================================================================

def mapa_forward(manpower: float, active_ratio: float, cases_per_active_per_month: float, avg_case_size_fyp: float, months: int = 12) -> Dict[str, float]:
    """FYP = Manpower * Active_Ratio * Productivity(Cases/M) * Avg_Case_Size * Months."""
    mp = _require_non_negative_float(manpower, "manpower")
    ar = _require_rate_0_to_1(active_ratio, "active_ratio", allow_zero=True)
    prod = _require_non_negative_float(cases_per_active_per_month, "cases_per_active_per_month")
    acs = _require_non_negative_float(avg_case_size_fyp, "avg_case_size_fyp")
    m = _require_int(months, "months", 1)
    active_agents = mp * ar
    total_cases = active_agents * prod * m
    total_fyp = total_cases * acs
    return {
        "active_agents_avg": round(active_agents, 2),
        "total_cases": round(total_cases, 2),
        "total_fyp_vnd_m": round(total_fyp, 2),
    }


def mapa_reverse_required_manpower(target_fyp_vnd_m: float, active_ratio: float, cases_per_active_per_month: float, avg_case_size_fyp: float, months: int = 12) -> float:
    tgt = _require_non_negative_float(target_fyp_vnd_m, "target_fyp_vnd_m")
    ar = _require_rate_0_to_1(active_ratio, "active_ratio", allow_zero=False)
    prod = _require_positive_float(cases_per_active_per_month, "cases_per_active_per_month")
    acs = _require_positive_float(avg_case_size_fyp, "avg_case_size_fyp")
    m = _require_int(months, "months", 1)
    denom = ar * prod * acs * m
    return round(tgt / denom, 2)


if __name__ == "__main__":
    print("=== W24 ENTERPRISE TOTAL DISTRIBUTION COST SNAPSHOT (12B FYP Region) ===")
    for k2 in (82.0, 72.0, 62.0):
        print(f"\n--- Persistency K2 / FY = {k2}% ---")
        for sc in ("AIA_Alpha_2026", "AIA_Alpha_2027", "Chubb_Agency_2026", "W24_Proposed_Balanced"):
            res = calc_enterprise_hierarchy_cost(sc, k2_pct=k2)
            print(
                f"  {sc:22s} | Earned: {res['earned_pct_fyp']:6.2f}% FYP | CashY1: {res['cash_y1_pct_fyp']:6.2f}% "
                f"| Art52: {res['art52_bonus_pct_fyp']:5.2f}% ({'PASS' if res['art52_pass_30pct_cap'] else 'FAIL'}) "
                f"| Cost/PersistedY2: {res['cost_per_persisted_y2_pct']:6.2f}% | BE Margin: {res['breakeven_gross_margin_pct']:6.2f}%"
            )
