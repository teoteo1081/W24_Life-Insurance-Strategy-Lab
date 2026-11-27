"""W24 Chính sách Lai VN 2026 (Hybrid Scheme) — PROPOSAL, không phải chính sách đã ban hành.

Kế thừa bộ tham số "Song Hành" đã hiệu chỉnh (scripts/calibrate_song_hanh.py) và hàm đại lý của engine
(calc_proposal_agent_12m, proposal_k2_factor). KHÔNG sửa compensation_engine.py (đã qua kiểm toán).

Ba điểm mới (TJ yêu cầu 2026-11-27):
 1. Hai đường ray đại lý:
    - FULL_TIME (cam kết): thưởng tháng 100% bậc Song Hành + trợ cấp cam kết cố định mỗi tháng đạt quota FYP vùng,
      ≥ CC tối thiểu và K2 ≥ 80% (hoặc chưa có K2).
    - PART_TIME (thuần biến phí): thưởng tháng = PART_TIME_RATE_MULT × bậc Song Hành, không trợ cấp.
 2. Chốt chặn K2 ≥ 80%: trợ cấp cam kết chỉ trả khi K2 ≥ 80%; phần trả chậm (quản lý, lãnh đạo) nhận ĐỦ khi K2 ≥ 80%,
    50% khi 75–<80%, 0 khi <75% (bậc đệm giảm vách đá). Thưởng tháng theo hệ số K2 liên tục của Song Hành (sàn 60%).
    Override nhóm trực tiếp đủ tỷ lệ tới 60tr FYC/tháng (không giãn theo vùng), phần vượt 50% — chống bẫy giữ đội phẳng.
 3. Hệ số vùng 4 bậc theo lương tối thiểu vùng NĐ 293/2025 (PROPOSAL): giãn MỌI ngưỡng FYP/FYC (quota, bậc thưởng, cổng gián tiếp,
    chỉ tiêu lãnh đạo) theo hệ số vùng; GIỮ NGUYÊN yêu cầu CC và K2 ≥ 80%. Không đổi tỷ lệ %.
Ràng buộc chi phí: tổng chi / FYP ≤ COST_CAP_PCT_FYP ở kịch bản chuẩn (kiểm trong scripts/build_phase2.py).
"""
from __future__ import annotations

import math
from dataclasses import replace
from typing import Dict, Optional

from model.compensation.compensation_engine import ProposalParams, calc_proposal_agent_12m, proposal_k2_factor

# ---------------- Tham số đề xuất (PROPOSAL — TJ có thể chỉnh) ----------------
# Hệ số vùng neo theo LƯƠNG TỐI THIỂU VÙNG 2026 — NĐ 293/2025/NĐ-CP (`SOURCE_CLAIM`, wheel-check r2 câu 5):
# Vùng I 5,31 · II 4,73 · III 4,14 · IV 3,70 tr/tháng → 100% / 89,1% / 78,0% / 69,7% (làm tròn 100/89/78/70).
# Danh sách địa bàn mỗi vùng theo phụ lục NĐ 293/2025 (34 tỉnh/thành sau NQ 202/2025/QH15). Thay bộ tự đặt 100/82,5/67,5% (audit r1 AUD-10).
REGIONS = {
    "V1": {"name": "Vùng I theo NĐ 293/2025 (gồm nội thành Hà Nội, TP.HCM)", "coef": 1.00},
    "V2": {"name": "Vùng II theo NĐ 293/2025", "coef": 0.89},
    "V3": {"name": "Vùng III theo NĐ 293/2025", "coef": 0.78},
    "V4": {"name": "Vùng IV theo NĐ 293/2025", "coef": 0.70},
}
K2_GATE_PCT = 80.0                 # chốt chặn trợ cấp & trả chậm
COST_CAP_PCT_FYP = 75.0            # trần tổng chi / FYP
FT_QUOTA_FYP_MONTH = 30.0          # quota FYP/tháng của Full-time ở Vùng 1 (= Mốc 1)
FT_MIN_CC_MONTH = 2                # số hợp đồng tối thiểu/tháng — KHÔNG giãn theo vùng
FT_ALLOWANCE_MONTH = 3.0           # trợ cấp cam kết/tháng (triệu) ở Vùng 1; vùng khác × hệ số vùng — phần cố định duy nhất của đại lý
PART_TIME_RATE_MULT = 0.70         # thưởng tháng Part-time = 70% bậc Song Hành
LEADER_TARGET_FYP_MONTH = 1000.0   # chỉ tiêu FYP/tháng của lãnh đạo vùng ở Vùng 1
LEADER_OVERRIDE_FYC_RATE = 0.115   # override toàn khu vực của lãnh đạo (Song Hành: 8,05%) — nâng để thu nhập lãnh đạo Mốc 4 không thấp hơn
                                   # mức thấp nhất của 3 hãng (Manulife PSM/SM 105,1 tr/tháng); 70% vẫn trả chậm 3 năm theo K2 (DEC-17, PROPOSAL)
INDIRECT_GEN2_SHARE = 0.5          # gián tiếp đời 2 = ½ tỷ lệ đời 1 (như Chubb/Manulife), tối đa 2 đời
K2_RAMP_FROM_PCT = 75.0            # trả chậm: K2 ≥80% nhận 100%; 75–<80% nhận 50%; <75% = 0 (giảm vách đá đo được ở 02)
K2_RAMP_SHARE = 0.5
DIRECT_FULL_RATE_CAP_FYC = 60.0    # override đủ tỷ lệ tới 60tr FYC nhóm trực tiếp/tháng (cố định mọi vùng); phần vượt 50% — chống bẫy đội phẳng
DIRECT_EXCESS_RATE_SHARE = 0.5
# Chống vỡ trần khi cơ cấu nghiêng bảo vệ thuần (AUD-03, audit r1 2026-11-27 — TJ chọn "sửa cơ chế"):
#  (1) FYC chuẩn hóa: mọi khoản THƯỞNG và PHÍ QUẢN LÝ tính trên FYP × 30%, không phụ thuộc tỷ lệ hoa hồng của sản phẩm.
#      Hoa hồng vẫn trả đúng tỷ lệ của từng sản phẩm (trần Điều 51 TT 67/2023 — CONDITIONAL).
#  (2) Trần quỹ thu nhập cây đại lý: nếu tổng chi khu vực > COST_CAP_PCT_FYP, phần thưởng + phí quản lý biến đổi (không gồm
#      hoa hồng và phần cố định) giảm theo cùng một tỷ lệ cho vừa trần — giống cách Điều 52 khóa trần ở cấp công ty.
#      Trần 75% là trần QUỸ THU NHẬP CÂY ĐẠI LÝ, không phải tổng chi phí khai thác trên BCTC (wheel-check r2 câu 3).
NORMALIZED_FYC_RATE = 0.30


def song_hanh_params() -> ProposalParams:
    """Bộ tham số Song Hành đã hiệu chỉnh (cùng nguồn với trang HTML)."""
    from scripts.calibrate_song_hanh import main as calibrate   # tránh import vòng khi chỉ dùng hằng số
    raw = calibrate()["params"]
    return ProposalParams(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in raw.items()})


def _fin(x: float, name: str) -> float:
    if not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return float(x)


def _coef(region: str) -> float:
    if region not in REGIONS:
        raise ValueError(f"region must be one of {list(REGIONS)}")
    return REGIONS[region]["coef"]


def _k2_ok(k2: Optional[float]) -> bool:
    return k2 is None or k2 >= K2_GATE_PCT


def _deferred_vest(k2: Optional[float]) -> float:
    """Tỷ lệ được nhận phần trả chậm: 100% khi K2 ≥ 80% (hoặc chưa có K2), 50% khi 75–<80%, 0 khi <75%."""
    if _k2_ok(k2):
        return 1.0
    return K2_RAMP_SHARE if k2 >= K2_RAMP_FROM_PCT else 0.0


def regional_params(base: ProposalParams, region: str, track: str) -> ProposalParams:
    c = _coef(region)
    if track not in ("FULL_TIME", "PART_TIME"):
        raise ValueError("track must be FULL_TIME or PART_TIME")
    mult = 1.0 if track == "FULL_TIME" else PART_TIME_RATE_MULT
    return replace(base, name=f"Hybrid_{region}_{track}",
                   agent_m_tier_thresholds=tuple(round(t * c, 4) for t in base.agent_m_tier_thresholds),
                   agent_m_tier_rates=tuple(round(r * mult, 6) for r in base.agent_m_tier_rates),
                   mgr_indirect_gate_fyc=round(base.mgr_indirect_gate_fyc * c, 4),
                   # Codex P2 (9dea455): MỌI ngưỡng FYP/FYC của đại lý giãn theo vùng, kể cả nhất quán / MDRT / nhập môn
                   agent_q_consistency_min_fyc=round(base.agent_q_consistency_min_fyc * c, 4),
                   agent_mdrt_fyc_threshold=round(base.agent_mdrt_fyc_threshold * c, 4),
                   agent_onboarding_min_fyc=round(base.agent_onboarding_min_fyc * c, 4))


def hybrid_agent_12m(fyp_month: float, cc_month: int, k2: Optional[float], region: str, track: str,
                     base: ProposalParams, fyc_rate: float = 0.30, syc_month: float = 0.0) -> Dict[str, float]:
    fyp_month = _fin(fyp_month, "fyp_month")
    fyc_rate = _fin(fyc_rate, "fyc_rate")
    if not 0.0 < fyc_rate <= 1.0:
        raise ValueError("fyc_rate must be in (0, 1]")
    p = regional_params(base, region, track)
    # Thưởng tính trên FYC chuẩn hóa (FYP × 30%); hoa hồng thật = FYP × tỷ lệ của sản phẩm
    r = calc_proposal_agent_12m([fyp_month * NORMALIZED_FYC_RATE] * 12, [syc_month] * 12, k2_pct=k2, params=p)
    commission = fyp_month * fyc_rate * 12
    adj = commission - r["fyc_total"]
    quota = FT_QUOTA_FYP_MONTH * _coef(region)
    allow_months = 12 if (track == "FULL_TIME" and fyp_month >= quota and cc_month >= FT_MIN_CC_MONTH and _k2_ok(k2)) else 0
    allowance = FT_ALLOWANCE_MONTH * _coef(region) * allow_months   # trợ cấp tỷ lệ theo hệ số vùng (Codex P1 9dea455: V3 đạt quota vượt trần 75%)
    total = r["total_earned"] + adj + allowance
    return {"fyc_total": round(commission, 4), "bonuses": round(r["total_bonuses_earned"], 4), "allowance_fixed": round(allowance, 4),
            "total_earned": round(total, 4), "cash_paid_y1": round(r["cash_paid_y1"] + adj + allowance, 4),
            "paid_next_years": round(r["deferred_post_y1"] + r["accrued_t_plus_1_unpaid"], 4), "quota_fyp_month": round(quota, 4),
            "quota_met": allow_months > 0}


def pool_cap_scale(total: float, commission: float, fixed: float, fyp_y: float) -> float:
    """Hệ số co của phần thưởng + phí quản lý biến đổi để tổng chi ≤ COST_CAP_PCT_FYP × FYP (1.0 = không phải co).
    Nếu riêng hoa hồng + phần cố định đã vượt trần thì co phần biến đổi về 0 (trần không thể đạt bằng cơ chế này)."""
    for v, n in ((total, "total"), (commission, "commission"), (fixed, "fixed"), (fyp_y, "fyp_y")):
        _fin(v, n)
    if fyp_y <= 0:
        raise ValueError("fyp_y must be > 0")
    cap = COST_CAP_PCT_FYP / 100.0 * fyp_y
    variable = total - commission - fixed
    if total <= cap or variable <= 0:
        return 1.0
    return max(0.0, (cap - commission - fixed) / variable)


def hybrid_manager_12m(direct_fyc_month: float, sub_direct_fyc_months: tuple, grand_sub_direct_fyc_months: tuple,
                       k2: Optional[float], region: str, base: ProposalParams) -> Dict[str, float]:
    """Quản lý trực tiếp (UM/BM): override nhóm trực tiếp × hệ số K2 (trần), gián tiếp 2 đời có cổng FYC vùng, trả chậm khi K2 ≥ 80%."""
    c = _coef(region)
    k2f = proposal_k2_factor(k2, base.k2_hard_floor_pct, allow_new_no_k2=k2 is None)
    rate = min(base.mgr_direct_max_rate, base.mgr_direct_base_rate * k2f)
    cap = DIRECT_FULL_RATE_CAP_FYC          # không giãn theo vùng: trần nhắm vào quy mô đội phẳng, không phải năng suất
    d_fyc = _fin(direct_fyc_month, "direct_fyc_month")
    direct = (min(d_fyc, cap) + max(0.0, d_fyc - cap) * DIRECT_EXCESS_RATE_SHARE) * 12 * rate
    gate_ok = direct_fyc_month >= base.mgr_indirect_gate_fyc * c
    gen1 = sum(f * 12 * rate for f in sub_direct_fyc_months) * base.mgr_indirect_l1_rate if gate_ok else 0.0
    gen2 = sum(f * 12 * rate for f in grand_sub_direct_fyc_months) * base.mgr_indirect_l1_rate * INDIRECT_GEN2_SHARE if gate_ok else 0.0
    deferred = direct_fyc_month * 12 * base.mgr_deferred_3y_rate * _deferred_vest(k2)
    cash = direct + gen1 + gen2
    return {"direct_override": round(direct, 4), "indirect": round(gen1 + gen2, 4), "deferred_3y": round(deferred, 4),
            "fixed": 0.0, "cash_paid_y1": round(cash, 4), "paid_next_years": round(deferred, 4), "total_earned": round(cash + deferred, 4)}


def hybrid_leader_12m(org_fyp_month: float, org_fyc_month: float, k2: Optional[float], region: str, base: ProposalParams) -> Dict[str, float]:
    """Lãnh đạo vùng: phí cơ bản theo % đạt chỉ tiêu vùng (sàn 30%, trần 140%) + override toàn vùng × K2; phần trả chậm khi K2 ≥ 80%."""
    c = _coef(region)
    ach = _fin(org_fyp_month, "org_fyp_month") / (LEADER_TARGET_FYP_MONTH * c)
    base_fee = 0.0 if ach < 0.30 else base.rd_base_monthly * 12 * min(1.40, ach * 1.25)
    k2f = proposal_k2_factor(k2, base.k2_hard_floor_pct, allow_new_no_k2=k2 is None)
    var = _fin(org_fyc_month, "org_fyc_month") * 12 * LEADER_OVERRIDE_FYC_RATE * k2f
    deferred_pool = var * base.rd_deferred_3y_share
    deferred = deferred_pool * _deferred_vest(k2)
    cash = base_fee + var - deferred_pool
    return {"base_fixed": round(base_fee, 4), "override": round(var, 4), "deferred_3y": round(deferred, 4),
            "fixed": round(base_fee, 4), "cash_paid_y1": round(cash, 4), "paid_next_years": round(deferred, 4),
            "total_earned": round(cash + deferred, 4), "target_achievement": round(ach, 4)}
