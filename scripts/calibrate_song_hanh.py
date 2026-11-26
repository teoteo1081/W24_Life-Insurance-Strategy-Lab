"""Hiệu chỉnh biến thể "Song Hành": không trả thấp nhất thị trường ở bất kỳ tầng nào.

Mục tiêu mỗi tầng = mức của đối thủ TRẢ THẤP NHẤT có tài liệu ở tầng đó (cây tổ chức chuẩn, K2 = 82%):
- Đại lý: tổng thu nhập 3 năm ở FYC 5 / 15 / 35 tr/tháng >= min(AIA, Chubb)   (Manulife UNKNOWN)
- Quản lý trực tiếp, thu nhập gián tiếp thêm: >= min(AIA, Chubb)              (Manulife UNKNOWN)
- Lãnh đạo vùng: >= min(AIA PAF+, Chubb RD, Manulife PSM+)
Cách làm: nhân các nhóm tham số của phương án cân bằng với hệ số nhỏ nhất (bước 1%) đủ đạt mục tiêu.
Kết quả: PROPOSAL / MODEL_OUTPUT, không phải ROI thực tế.
"""
from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
for p in (REPO, REPO / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from model.compensation.compensation_engine import (  # noqa: E402
    ProposalParams,
    calc_enterprise_hierarchy_cost,
    calc_manulife_psm_12m,
)
from agent_income_multiyear import agent_income_3y  # noqa: E402

K2 = 82.0
BASE = ProposalParams()


def agent_params(a: float) -> ProposalParams:
    return replace(BASE, name="Song_Hanh",
                   agent_m_tier_rates=tuple(min(1.0, r * a) for r in BASE.agent_m_tier_rates),
                   agent_ryc_bonus_rate=min(1.0, BASE.agent_ryc_bonus_rate * a))


def find_min(fn, lo=1.0, hi=4.0, step=0.01):
    x = lo
    while x <= hi + 1e-9:
        if fn(x):
            return round(x, 2)
        x += step
    raise SystemExit("không tìm được hệ số trong khoảng cho phép")


def main() -> dict:
    # Tầng đại lý
    def agent_ok(a):
        p = agent_params(a)
        for fyc in (5.0, 15.0, 35.0):
            r = agent_income_3y(fyc, K2, p)
            if r["PROPOSAL"]["total_3y"] < min(r["AIA"]["total_3y"], r["CHUBB"]["total_3y"]):
                return False
        return True
    a = find_min(agent_ok)

    comp = {s: calc_enterprise_hierarchy_cost(s, K2) for s in ("AIA_Alpha_2026", "Chubb_Agency_2026")}
    mnl = calc_manulife_psm_12m(35.0, [1.05] * 12, [300.0] * 12, [1.0] * 4, K2)["total_earned"]
    tgt_dir = min(c["role_mgr_direct_earned"] for c in comp.values())
    tgt_ind = min(c["role_mgr_indirect_extra"] for c in comp.values())
    tgt_lead = min(min(c["role_leader_earned"] for c in comp.values()), mnl)

    def ent(p):
        return calc_enterprise_hierarchy_cost("W24_Proposed_Balanced", K2, params=p)

    p = agent_params(a)
    b = find_min(lambda x: ent(replace(p, mgr_direct_base_rate=BASE.mgr_direct_base_rate * x,
                                       mgr_direct_max_rate=min(1.0, BASE.mgr_direct_max_rate * x),
                                       mgr_deferred_3y_rate=BASE.mgr_deferred_3y_rate * x))["role_mgr_direct_earned"] >= tgt_dir)
    p = replace(p, mgr_direct_base_rate=BASE.mgr_direct_base_rate * b,
                mgr_direct_max_rate=min(1.0, BASE.mgr_direct_max_rate * b),
                mgr_deferred_3y_rate=BASE.mgr_deferred_3y_rate * b)
    c = find_min(lambda x: ent(replace(p, mgr_indirect_l1_rate=min(1.0, BASE.mgr_indirect_l1_rate * x)))["role_mgr_indirect_extra"] >= tgt_ind)
    p = replace(p, mgr_indirect_l1_rate=min(1.0, BASE.mgr_indirect_l1_rate * c))
    d = find_min(lambda x: ent(replace(p, rd_base_monthly=BASE.rd_base_monthly * x,
                                       rd_direct_fyc_rate=BASE.rd_direct_fyc_rate * x))["role_leader_earned"] >= tgt_lead)
    p = replace(p, rd_base_monthly=BASE.rd_base_monthly * d, rd_direct_fyc_rate=BASE.rd_direct_fyc_rate * d)

    out = {"multipliers": {"agent": a, "mgr_direct": b, "mgr_indirect": c, "leader": d},
           "targets_k2_82": {"mgr_direct": tgt_dir, "mgr_indirect": tgt_ind, "leader": tgt_lead, "manulife_leader": round(mnl, 2)},
           "params": {k: (list(v) if isinstance(v, tuple) else v) for k, v in p.__dict__.items()},
           "cost": {}}
    for k2 in (82.0, 72.0, 62.0):
        bal = calc_enterprise_hierarchy_cost("W24_Proposed_Balanced", k2)
        sh = calc_enterprise_hierarchy_cost("W24_Proposed_Balanced", k2, params=p)
        aia = calc_enterprise_hierarchy_cost("AIA_Alpha_2026", k2)
        chb = calc_enterprise_hierarchy_cost("Chubb_Agency_2026", k2)
        out["cost"][f"{k2:.0f}"] = {n: {"earned_pct_fyp": r["earned_pct_fyp"], "cash_y1_pct_fyp": r["cash_y1_pct_fyp"],
                                        "cost_per_persisted_y2_pct": r["cost_per_persisted_y2_pct"],
                                        "agent": r["role_agent_earned"], "mgr_direct": r["role_mgr_direct_earned"],
                                        "mgr_indirect": r["role_mgr_indirect_extra"], "leader": r["role_leader_earned"]}
                                    for n, r in (("balanced", bal), ("song_hanh", sh), ("aia", aia), ("chubb", chb))}
    out["agent_3y_k2_82"] = {f"{f:.0f}": agent_income_3y(f, K2, p) for f in (5.0, 15.0, 35.0)}
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=1, ensure_ascii=False))
