"""Giai đoạn 2 — phân tích hành vi / ROI 3 tầng / Rubric 5 trụ cột + Chính sách Đề xuất 2026 & phân vùng.

Sinh:
  outputs/interview/02_Phan_Tich_MAPA_TradeOff_Va_ROI.md
  outputs/interview/03_De_Xuat_Chinh_Sach_Lai_VN2026.md
compute() cũng là nguồn cho scripts/sync_to_supabase.py (bảng roi_analysis, rubric_scores, behavior_traps, hybrid_regional).

Nhãn: số tính từ engine = MODEL_OUTPUT; tham số Chính sách Đề xuất 2026 & hệ số vùng = PROPOSAL; khác biệt hành vi vùng miền = HYPOTHESIS;
"ROI" ở đây là chi phí / FYP và chi phí / phí còn duy trì — KHÔNG phải ROI thực tế (VNB, biên lợi nhuận, OpEx thật = UNKNOWN).
Chạy:  python scripts/build_phase2.py
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from model.compensation import hybrid_scheme as H  # noqa: E402
from model.compensation.compensation_engine import (  # noqa: E402
    calc_aia_cql_12m, calc_aia_cvtv_12m, calc_aia_paf_12m, calc_chubb_al_12m, calc_chubb_al_htktn_month,
    calc_chubb_ar_12m, calc_chubb_rd_12m, calc_manulife_agent_12m, calc_manulife_psm_12m, calc_manulife_um_12m,
    calc_enterprise_hierarchy_cost,
)
from w24_milestones import load_milestones, rubric_table, FILE_IDS  # noqa: E402

OUT02 = REPO / "outputs" / "interview" / "02_Phan_Tich_MAPA_TradeOff_Va_ROI.md"
OUT03 = REPO / "outputs" / "interview" / "03_De_Xuat_Chinh_Sach_Lai_VN2026.md"
FYC_RATE = 0.30
SCHEMES = ("AIA", "Chubb", "Manulife", "Hybrid")
RECRUITS = [1, 2, 2, 2]
# Phân bổ năng suất 4 nhóm (ASSUMPTION — khung Inactive / Low 10tr / Core 15–20tr / Top-MDRT 50–100tr của docs/research/wheel-check-r2.md câu 4);
# giữ nguyên tổng 45 ĐL và 1,2 tỷ FYP/tháng của Mốc 4 để chỉ đo tác động của việc bán KHÔNG đều.
PRODUCTIVITY_MIX = [("Không hoạt động", 7, 0.0), ("Thấp", 13, 10.0), ("Nòng cốt", 15, 20.0), ("Top / MDRT", 10, 77.0)]
MIX = [(n, f) for _, n, f in PRODUCTIVITY_MIX]
CONF = {"Manulife"}   # số Manulife dựa trên 0046M01/0047M01 → restricted (DEC-14)


def fin(x):
    if not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"non-finite {x!r}")
    return float(x)


def vn(x, d=1):
    return f"{fin(x):,.{d}f}".replace(",", "_").replace(".", ",").replace("_", ".")


# =============================================================================
# Thu nhập theo từng vai trò — K2 là tham số (không dùng hằng số module)
# =============================================================================
def renewal(fyp_m, k2):
    """Hoa hồng tái tục ổn định/năm (giả định A7 của bảng 01): HĐ năm 2 (20%) + năm 3 (10%)."""
    from agent_income_multiyear import K3_RATIO, RENEWAL_COMM_Y2, RENEWAL_COMM_Y3
    y, k = fyp_m * 12, k2 / 100
    return y * k * RENEWAL_COMM_Y2, y * k * K3_RATIO * RENEWAL_COMM_Y3


def agent(scheme, fyp_m, k2, base, region="V1", track="FULL_TIME", with_renewal=False, fyc_rate=FYC_RATE):
    """with_renewal=False: chi phí năm đầu (ROI tầng 1). True: cùng cơ sở thu nhập Mốc 1 của bảng 01 (gồm tái tục A7).
    fyc_rate: tỷ lệ hoa hồng năm đầu của cơ cấu sản phẩm (độ nhạy 25/30/40% — AUD-03)."""
    fyc = fyp_m * fyc_rate
    y2, y3 = renewal(fyp_m, k2) if with_renewal else (0.0, 0.0)
    if scheme == "AIA":
        r = calc_aia_cvtv_12m([fyc] * 12, [y2 / 12] * 12, fy_pct=k2)
        return {"total": r["total_earned"] + y3, "cash": r["cash_paid_y1"] + y3, "fixed": 0.0}
    if scheme == "Chubb":
        r = calc_chubb_ar_12m([fyc] * 12, [(y2 + y3) / 12] * 12, [True] * 12, k2_pct=k2, tenure_months_start=13)
        return {"total": r["total_earned"], "cash": r["cash_paid_y1"], "fixed": 0.0}
    if scheme == "Manulife":
        r = calc_manulife_agent_12m([fyc] * 12, [fyp_m] * 12, [1] * 12, k2=k2, monthly_ryc=[(y2 + y3) / 12] * 12)
        return {"total": r["total_earned"], "cash": r["cash_paid_y1"], "fixed": 0.0}
    r = H.hybrid_agent_12m(fyp_m, H.FT_MIN_CC_MONTH, k2, region, track, base, fyc_rate=fyc_rate, syc_month=y2 / 12)
    return {"total": r["total_earned"] + y3, "cash": r["cash_paid_y1"] + y3, "fixed": r["allowance_fixed"], "commission": r["fyc_total"]}


def manager(scheme, fpa_fyp, k2, base, n_sub=0, n_grand=0, region="V1", direct=5, rank="UM", fyc_rate=FYC_RATE):
    """Quản lý có `direct` đại lý trực tiếp, n_sub quản lý con (mỗi người 5 ĐL), n_grand quản lý cháu.
    Chính sách Đề xuất 2026 tính phí quản lý trên FYC chuẩn hóa (FYP × 30%); 3 hãng tính trên FYC thật theo văn bản của họ."""
    fpa = fpa_fyp * (H.NORMALIZED_FYC_RATE if scheme == "Hybrid" else fyc_rate)
    team = fpa * direct
    sub_team = fpa * 5
    if scheme == "AIA":
        sub_a = calc_aia_cql_12m([sub_team] * 12, [5] * 12, fy_pct=k2, tot_pct=k2, quarterly_new_recruits=RECRUITS)["direct_monthly"]
        r = calc_aia_cql_12m([team] * 12, [direct] * 12, fy_pct=k2, tot_pct=k2, quarterly_new_recruits=RECRUITS,
                             indirect_gen2_base_12m=n_sub * sub_a, indirect_gen3_base_12m=n_grand * sub_a)
        return {"total": r["total_earned"], "cash": r["cash_paid_y1"], "fixed": 0.0}
    if scheme == "Chubb":
        sub_ht = calc_chubb_al_htktn_month(sub_team, 5, k2, 15)
        r = calc_chubb_al_12m([team] * 12, [direct] * 12, k2_ntt=k2, al_tenure_start=15, rank=rank,
                              sub_l1_htktn_monthly=[n_sub * sub_ht] * 12, sub_l2_htktn_monthly=[n_grand * sub_ht] * 12)
        return {"total": r["total_earned"], "cash": r["cash_paid_y1"], "fixed": 0.0}
    if scheme == "Manulife":
        ag = calc_manulife_agent_12m([fpa] * 12, [fpa_fyp] * 12, [1] * 12, k2=k2)
        per = [ag["monthly_bonus_by_month"][m] + (ag["quarterly_bonus_by_quarter"][m // 3] if m % 3 == 2 else 0.0) for m in range(12)]
        r = calc_manulife_um_12m([(team, sub_team * n_sub, sub_team * n_grand, 0.0)] * 12, [direct] * 12, [direct * x for x in per], k2)
        return {"total": r["total_earned"], "cash": r["cash_paid_y1"], "fixed": 0.0}
    r = H.hybrid_manager_12m(team, (sub_team,) * n_sub, (sub_team,) * n_grand, k2, region, base)
    return {"total": r["total_earned"], "cash": r["cash_paid_y1"], "fixed": 0.0}


def leader(scheme, org_fyp_m, org_agents, k2, base, region="V1", psm_ach=1.0, fyc_rate=FYC_RATE):
    fyc = org_fyp_m * (H.NORMALIZED_FYC_RATE if scheme == "Hybrid" else fyc_rate)
    team5 = fyc / org_agents * 5
    if scheme == "AIA":
        paf = calc_aia_paf_12m("PAF", 1, [org_fyp_m] * 12, [fyc] * 12, [float(org_agents)] * 12, fy_pct=k2, attendance_pct=80.0)
        cql = calc_aia_cql_12m([team5] * 12, [5] * 12, fy_pct=k2, tot_pct=k2, quarterly_new_recruits=RECRUITS)
        return {"total": paf["total_earned"] + cql["total_earned"], "cash": paf["cash_paid_y1"] + cql["cash_paid_y1"], "fixed": paf["base_fee_12m"]}
    if scheme == "Chubb":
        rd = calc_chubb_rd_12m([org_fyp_m] * 12, [fyc] * 12, [org_agents] * 12, [org_agents] * 12, [0.0] * 12, k2_pct=k2,
                               weighted_reported_fyp_monthly=org_fyp_m, training_classes_monthly=4, prior_year_q_fyp=[org_fyp_m * 3] * 4)
        return {"total": rd["total_earned"], "cash": rd["cash_paid_y1"], "fixed": rd["training_12m"] + rd["activity_12m"] + rd["business_12m"]}
    if scheme == "Manulife":
        r = calc_manulife_psm_12m(35.0, [psm_ach] * 12, [fyc] * 12, [psm_ach] * 4, k2)
        return {"total": r["total_earned"], "cash": r["cash_paid_y1"], "fixed": r["base_fee_12m"]}
    r = H.hybrid_leader_12m(org_fyp_m, fyc, k2, region, base)
    return {"total": r["total_earned"], "cash": r["cash_paid_y1"], "fixed": r["fixed"]}


def org_cost(scheme, k2, base, prod=1.0, region="V1", fyc_rate=FYC_RATE, mix=None):
    """Khu vực Mốc 4: 45 ĐL × FYP/ĐL; lãnh đạo (5 trực tiếp) + 2 trưởng ban (5 + 2 UM) + 2 UM trực tiếp + 4 UM dưới ban.
    Chi phí NĂM ĐẦU: hoa hồng FYC + thưởng + phí quản lý; KHÔNG gồm hoa hồng/thưởng tái tục (cùng quy ước enterprise model).
    mix: [(số ĐL, FYP/tháng)] — phân bổ năng suất không đều (tổng 45 ĐL); None = mọi ĐL bán đều FYP Mốc 4. prod nhân mọi nhóm.
    Quản lý & lãnh đạo tính trên FYP nhóm/khu vực (mỗi nhóm trộn đủ các mức năng suất), nên chỉ phần đại lý thay đổi theo mix."""
    m4 = load_milestones()[3]
    groups = [(m4.agents, m4.fyp_per_agent)] if mix is None else [(int(n), float(f)) for n, f in mix]
    if sum(n for n, _ in groups) != m4.agents or any(n < 0 or f < 0 for n, f in groups):
        raise ValueError("mix must cover exactly the 45 agents with non-negative FYP")
    groups = [(n, fin(f * prod)) for n, f in groups]
    org_fyp = sum(n * f for n, f in groups)
    fpa = org_fyp / m4.agents
    ag = [(("45 đại lý" if mix is None else f"{n} đại lý × {vn(f)}tr"), agent(scheme, f, k2, base, region, fyc_rate=fyc_rate), n) for n, f in groups if n]
    parts = ag + [("6 trưởng nhóm", manager(scheme, fpa, k2, base, region=region, rank="UM", fyc_rate=fyc_rate), 6),
                  ("2 trưởng ban", manager(scheme, fpa, k2, base, n_sub=2, region=region, rank="DM", fyc_rate=fyc_rate), 2),
                  ("lãnh đạo khu vực", leader(scheme, org_fyp, m4.agents, k2, base, region, psm_ach=prod, fyc_rate=fyc_rate), 1)]
    tot = sum(r["total"] * n for _, r, n in parts)
    cash = sum(r["cash"] * n for _, r, n in parts)
    fixed = sum(r["fixed"] * n for _, r, n in parts)
    fyp_y = org_fyp * 12
    scale = 1.0
    if scheme == "Hybrid":   # trần quỹ thu nhập cây đại lý: co thưởng + phí quản lý biến đổi theo cùng tỷ lệ (AUD-03)
        comm = sum(r["commission"] * n for _, r, n in ag)
        scale = H.pool_cap_scale(tot, comm, fixed, fyp_y)
        if scale < 1.0:
            var_tot, var_cash = tot - comm - fixed, cash - comm - fixed
            parts = [(nm, {**r, "total": r["total"] * (comm + fixed + var_tot * scale) / tot}, n) for nm, r, n in parts]
            tot, cash = comm + fixed + var_tot * scale, comm + fixed + var_cash * scale
    agent_tot = sum(r["total"] * n for _, r, n in parts[:len(ag)])
    return {"total": tot, "cash": cash, "fixed": fixed, "fyp_y": fyp_y, "cost_pct": tot / fyp_y * 100, "cash_share": cash / tot * 100,
            "deferred_share": (tot - cash) / tot * 100, "fixed_share": fixed / tot * 100,
            "cost_per_persisted_pct": tot / (fyp_y * k2 / 100) * 100,
            "parts": {name: r["total"] * n for name, r, n in parts}, "pool_scale": scale,
            # Rổ Điều 52 TT 67/2023 (cùng định nghĩa engine enterprise): thưởng + hỗ trợ của ĐẠI LÝ, không gồm hoa hồng; phí quản lý là phí dịch vụ (NĐ 97/2026)
            "art52_pct": (agent_tot - org_fyp * fyc_rate * 12) / fyp_y * 100,
            "agent_income_m": {f: r["total"] / 12 for (_, r, _n), (_n2, f) in zip(parts[:len(ag)], [g for g in groups if g[0]])}}


SCHEME_SRC = {"AIA": "[AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7]",
              "Chubb": "[CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10]",
              "Manulife": "[0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5]",
              "Hybrid": "PROPOSAL (hybrid_scheme.py)"}
CITE_RE = re.compile(r"\[[^\]]+ : [\d\-–]+\]|PROPOSAL \(")
NEG_PROOF = [("Tiêu chí danh hiệu MBA Pro / Manulife Pro (0050M01/2026)", [r"0050M01", r"MBA Pro", r"Manulife Pro"]),
             ("Quy định chung Chubb 260005V / 260006V / 260009V", [r"260005V", r"260006V", r"260009V"])]


def negative_proof() -> list:
    """Nhật ký tìm kiếm thật trên 9 PDF (tên file + nội dung từng trang) — AGENTS.md luật 3."""
    import csv
    import pymupdf
    reg = [r for r in csv.DictReader(open(REPO / "knowledge/sources/source-registry.csv", encoding="utf-8")) if r["Local_Relative_Path"].lower().endswith(".pdf")]
    assert len(reg) == len(FILE_IDS), len(reg)
    out = []
    for claim, kws in NEG_PROOF:
        log = []
        for r in reg:
            path = REPO / r["Local_Relative_Path"]
            name_hit = [k for k in kws if re.search(k, path.name, re.I)]
            pages = {k: [] for k in kws}
            with pymupdf.open(path) as doc:
                for i, pg in enumerate(doc):
                    t = re.sub(r"\s+", " ", pg.get_text())
                    for k in kws:
                        if re.search(k, t, re.I):
                            pages[k].append(i + 1)
            fid = next((f for f in FILE_IDS if f in path.name), path.stem)
            log.append((fid, name_hit, pages))
        is_file = any(nh for _, nh, _ in log)
        out.append({"claim": claim, "files_scanned": len(log), "is_a_source_file": is_file, "log": log})
    return out


def sweep_hybrid(base, fyc_rate=FYC_RATE) -> list:
    """Lưới quét điểm gãy Chính sách Đề xuất 2026: mỗi vùng × năng suất/ĐL (quanh quota vùng, các bậc thưởng tháng,
    ngưỡng nhất quán, MDRT, năng suất V1) × K2 {80, 85, 95}. Trả mọi điểm để kiểm trần ở điểm CAO NHẤT."""
    fpa0 = load_milestones()[3].fyp_per_agent
    pts = []
    for reg, meta in H.REGIONS.items():
        c = meta["coef"]
        q = H.FT_QUOTA_FYP_MONTH * c
        fyps = {q * k for k in (0.5, 0.75, 0.999, 1.0, 1.001, 1.25, 1.5, 2.0)} | {fpa0, 30.0}
        for t in base.agent_m_tier_thresholds:                        # bậc thưởng tháng (FYC) → FYP
            fyps |= {t * c / FYC_RATE, t * c / FYC_RATE * 1.001}
        fyps |= {base.agent_q_consistency_min_fyc * c / FYC_RATE, base.agent_mdrt_fyc_threshold * c / 12 / FYC_RATE}
        for f in sorted(fyps):
            for k2 in (80.0, 85.0, 95.0):
                o = org_cost("Hybrid", k2, base, prod=f / fpa0, region=reg, fyc_rate=fyc_rate)
                pts.append({"region": reg, "fpa": f, "k2": k2, "cost_pct": o["cost_pct"], "org": o})
    return pts


def lin(x, x_good, x_bad):
    """Điểm 1–5 tuyến tính: x_good → 5, x_bad → 1 (kẹp)."""
    if x_good == x_bad:
        return 3.0
    t = (x - x_bad) / (x_good - x_bad)
    return round(1 + 4 * max(0.0, min(1.0, t)), 2)


# =============================================================================
def compute() -> dict:
    base = H.song_hanh_params()
    ms = {m.mid: m for m in load_milestones()}
    out = {"roi": [], "traps": [], "rubric": [], "regional": [], "org": {}}

    # ---------- ROI 3 tầng ----------
    for s in SCHEMES:
        o85, o65, half = org_cost(s, 85.0, base), org_cost(s, 65.0, base), org_cost(s, 85.0, base, prod=0.5)
        quota = org_cost(s, 85.0, base, prod=H.FT_QUOTA_FYP_MONTH / load_milestones()[3].fyp_per_agent)   # mọi ĐL đạt quota 30tr
        scen = {"Mốc 4 chuẩn (26,7tr/ĐL)": o85, "Mọi ĐL đạt quota 30tr": quota}
        if s == "Hybrid":
            fpa0 = load_milestones()[3].fyp_per_agent
            for reg in [r for r in H.REGIONS if r != "V1"]:   # cùng năng suất V1 nhưng ngưỡng vùng thấp hơn → trợ cấp & bậc thưởng bật sớm hơn
                scen[f"{reg}, năng suất ngang V1"] = org_cost(s, 85.0, base, region=reg)
            for reg, meta in H.REGIONS.items():   # Codex P1 (9dea455): mọi ĐL đạt ĐÚNG quota của vùng mình
                scen[f"{reg}, mọi ĐL đạt đúng quota vùng ({vn(H.FT_QUOTA_FYP_MONTH * meta['coef'], 2)}tr)"] = \
                    org_cost(s, 85.0, base, prod=H.FT_QUOTA_FYP_MONTH * meta["coef"] / fpa0, region=reg)
            sw = sweep_hybrid(base)
            out["sweep"] = sw
            for reg in H.REGIONS:
                top = max((x for x in sw if x["region"] == reg), key=lambda x: x["cost_pct"])
                scen[f"{reg}, điểm gãy cao nhất của lưới quét ({vn(top['fpa'], 2)}tr FYP/ĐL, K2 {top['k2']:.0f}%)"] = top["org"]
        wname = max(scen, key=lambda k: scen[k]["cost_pct"])
        out["org"][s] = {"k85": o85, "k65": o65, "half": half, "quota": quota, "scenarios": scen, "worst": scen[wname], "worst_name": wname}
        conf = "restricted" if s in CONF else "public"
        lab = "PROPOSAL" if s == "Hybrid" else "MODEL_OUTPUT"
        for k2, o in ((85, o85), (65, o65)):
            for metric, unit, v in (("cost_pct_fyp", "% FYP", o["cost_pct"]), ("cost_per_persisted_pct", "% phí còn duy trì", o["cost_per_persisted_pct"]),
                                    ("cash_y1_share", "% chi trả", o["cash_share"]), ("deferred_share", "% chi trả", o["deferred_share"]),
                                    ("fixed_share", "% chi trả", o["fixed_share"])):
                out["roi"].append({"id": f"{s}|{metric}|{k2}", "scheme": s, "metric": metric, "k2": k2, "value": round(fin(v), 2), "unit": unit,
                                   "label": lab, "note": "", "confidentiality": conf})
        for metric, v, note in (("cost_pct_fyp_quota_productivity", quota["cost_pct"], "Mọi đại lý đạt quota 30tr FYP/tháng"),
                                ("cost_pct_fyp_worst_case", scen[wname]["cost_pct"], f"Kịch bản chi phí cao nhất: {wname}")):
            out["roi"].append({"id": f"{s}|{metric}|85", "scheme": s, "metric": metric, "k2": 85, "value": round(fin(v), 2), "unit": "% FYP",
                               "label": lab, "note": note, "confidentiality": conf})
        for metric, v, note in (("art52_agent_bonus_pct_fyp", o85["art52_pct"], "Rổ Điều 52: thưởng + hỗ trợ đại lý (không gồm hoa hồng) / FYP — trần 30% FYP phí định kỳ (CONDITIONAL)"),
                                ("art52_agent_bonus_pct_fyp_worst", scen[wname]["art52_pct"], f"Rổ Điều 52 ở kịch bản chi phí cao nhất: {wname}")):
            out["roi"].append({"id": f"{s}|{metric}|85", "scheme": s, "metric": metric, "k2": 85, "value": round(fin(v), 2), "unit": "% FYP",
                               "label": lab, "note": note, "confidentiality": conf})
        out["roi"].append({"id": f"{s}|cost_pct_fyp_half_production|85", "scheme": s, "metric": "cost_pct_fyp_half_production", "k2": 85,
                           "value": round(half["cost_pct"], 2), "unit": "% FYP", "label": lab, "note": "Năng suất giảm 50% (kiểm rủi ro định phí)", "confidentiality": conf})
        elastic = (o85["total"] - o65["total"]) / o85["total"] * 100
        out["roi"].append({"id": f"{s}|payout_drop_k2_85_to_65|0", "scheme": s, "metric": "payout_drop_k2_85_to_65", "k2": 0, "value": round(elastic, 2),
                           "unit": "% giảm chi trả", "label": lab, "note": "Chi trả giảm bao nhiêu khi K2 sập 85%→65% (cao = gắn chất lượng)", "confidentiality": conf})

    # ---------- Độ nhạy cơ cấu sản phẩm: tỷ lệ hoa hồng năm đầu 25% / 30% / 40% (AUD-03) ----------
    # 40% ≈ cơ cấu nghiêng bảo vệ thuần/tử kỳ (>50% HĐ mới 9T/2026 — SOURCE_CLAIM). Chính sách Đề xuất 2026: thưởng/phí quản lý trên FYC chuẩn hóa
    # + trần quỹ 75% (pool_scale = phần thưởng & phí quản lý biến đổi còn được trả). Kịch bản xấu nhất của Lai = lưới quét + mọi ĐL đạt quota.
    fpa0 = load_milestones()[3].fyp_per_agent
    out["fyc_sensitivity"] = []
    for rate in (0.25, 0.30, 0.40):
        for s in SCHEMES:
            std = org_cost(s, 85.0, base, fyc_rate=rate)
            cands = [std, org_cost(s, 85.0, base, prod=H.FT_QUOTA_FYP_MONTH / fpa0, fyc_rate=rate)]
            if s == "Hybrid":
                cands += [x["org"] for x in sweep_hybrid(base, fyc_rate=rate)]
            worst = max(cands, key=lambda o: o["cost_pct"])
            tag = f"fyc{int(round(rate * 100))}"
            row = {"scheme": s, "rate": rate, "std": std["cost_pct"], "worst": worst["cost_pct"],
                   "pool_scale_std": std["pool_scale"], "pool_scale_worst": worst["pool_scale"]}
            out["fyc_sensitivity"].append(row)
            conf = "restricted" if s in CONF else "public"
            lab = "PROPOSAL" if s == "Hybrid" else "MODEL_OUTPUT"
            for metric, v, note in ((f"cost_pct_fyp_{tag}", std["cost_pct"], f"Hoa hồng năm đầu {int(rate * 100)}% FYP, K2 85%, năng suất Mốc 4"),
                                    (f"cost_pct_fyp_worst_{tag}", worst["cost_pct"], f"Hoa hồng {int(rate * 100)}% FYP — kịch bản chi phí cao nhất")):
                out["roi"].append({"id": f"{s}|{metric}|85", "scheme": s, "metric": metric, "k2": 85, "value": round(fin(v), 2), "unit": "% FYP",
                                   "label": lab, "note": note, "confidentiality": conf})
            if s == "Hybrid":
                for metric, v in ((f"pool_paid_share_{tag}", std["pool_scale"]), (f"pool_paid_share_worst_{tag}", worst["pool_scale"])):
                    out["roi"].append({"id": f"{s}|{metric}|85", "scheme": s, "metric": metric, "k2": 85, "value": round(fin(v) * 100, 2),
                                       "unit": "% thưởng & phí quản lý được trả", "label": lab,
                                       "note": "100% = trần 75% không phải cắt; <100% = quỹ thưởng tự co để giữ trần", "confidentiality": conf})

    # ---------- Phân bổ năng suất 4 nhóm & hòa vốn doanh số ----------
    out["mix"] = {s: org_cost(s, 85.0, base, mix=MIX) for s in SCHEMES}
    for s in SCHEMES:
        conf = "restricted" if s in CONF else "public"
        lab = "PROPOSAL" if s == "Hybrid" else "MODEL_OUTPUT"
        for metric, v, note in (("cost_pct_fyp_mix4", out["mix"][s]["cost_pct"], "Phân bổ năng suất 4 nhóm (7 không hoạt động / 13 × 10tr / 15 × 20tr / 10 × 77tr), cùng tổng 1,2 tỷ FYP"),
                                ("art52_agent_bonus_pct_fyp_mix4", out["mix"][s]["art52_pct"], "Rổ Điều 52 ở phân bổ năng suất 4 nhóm")):
            out["roi"].append({"id": f"{s}|{metric}|85", "scheme": s, "metric": metric, "k2": 85, "value": round(fin(v), 2), "unit": "% FYP",
                               "label": lab, "note": note, "confidentiality": conf})
    out["breakeven"] = []
    grid = [1 + 0.005 * i for i in range(201)]                  # tăng năng suất 0 → +100%
    for basis, mix in (("uniform", None), ("mix4", MIX)):
        keep = [(g, g * (1 - org_cost("Hybrid", 85.0, base, prod=g, mix=mix)["cost_pct"] / 100)) for g in grid]
        c_new = 1 - keep[0][1]
        fyp_y = org_cost("Hybrid", 85.0, base, mix=mix)["fyp_y"]
        for comp in ("AIA", "Chubb", "Manulife"):
            c_old = org_cost(comp, 85.0, base, mix=mix)["cost_pct"] / 100
            target = 1 - c_old
            agents_pct = (target / (1 - c_new) - 1) * 100       # thêm ĐL cùng cơ cấu → tỷ lệ chi phí gần như giữ nguyên
            if target <= keep[0][1]:
                prod_pct = stable_pct = 0.0
            else:
                prod_pct = next(((g - 1) * 100 for g, v in keep if v >= target), None)
                stable_pct = next(((g - 1) * 100 for i, (g, _) in enumerate(keep) if all(v >= target for _, v in keep[i:])), None)
            row = {"basis": basis, "vs": comp, "cost_new_pct": c_new * 100, "cost_old_pct": c_old * 100,
                   "extra_cost_bn_year": (c_new - c_old) * fyp_y / 1000, "agents_pct": agents_pct,
                   "prod_pct": prod_pct, "prod_stable_pct": stable_pct}
            out["breakeven"].append(row)
            conf = "restricted" if comp in CONF else "public"
            for metric, v, unit in (("breakeven_fyp_more_agents_pct", agents_pct, "% FYP thêm"),
                                    ("breakeven_fyp_productivity_pct", prod_pct, "% FYP thêm"),
                                    ("breakeven_extra_cost_bn_year", row["extra_cost_bn_year"], "tỷ/năm")):
                if v is None:
                    continue   # không hòa vốn trong lưới +100% → không ghi số (không biến UNKNOWN thành 0)
                out["roi"].append({"id": f"Hybrid|{metric}|{comp}|{basis}", "scheme": "Hybrid", "metric": metric, "k2": 85, "value": round(fin(v), 2),
                                   "unit": unit, "label": "PROPOSAL", "confidentiality": conf,
                                   "note": f"So với {comp} — {'mọi ĐL bán đều 26,7tr' if basis == 'uniform' else 'phân bổ năng suất 4 nhóm'}; "
                                           "hòa vốn = phần FYP còn lại sau chi trả kênh đại lý bằng phương án so sánh (không phải lợi nhuận)"})

    # ---------- Bẫy hành vi ----------
    def trap(s, key, title, value, text, cite, label="MODEL_OUTPUT"):
        out["traps"].append({"id": f"{s}|{key}", "scheme": s, "trap": title, "metric_value": None if value is None else round(fin(value), 2),
                             "value_text": text, "citation": cite, "label": label, "confidentiality": "restricted" if s in CONF else "public"})

    m1, m2, m3 = ms["M1"], ms["M2"], ms["M3"]
    flat, cliff = {}, {}
    for s in SCHEMES:
        a1 = agent(s, m1.fyp_month, 85.0, base, with_renewal=True)["total"] / 12
        mg2 = manager(s, m2.fyp_per_agent, 85.0, base, rank="UM")["total"] / 12
        st3 = manager(s, m3.fyp_per_agent, 85.0, base, n_sub=2, rank="DM")["total"] / 12
        fl3 = manager(s, m3.fyp_per_agent, 85.0, base, direct=15, rank="UM")["total"] / 12
        flat[s] = fl3 / st3
        c80 = manager(s, m2.fyp_per_agent, 80.0, base)["total"]
        c79 = manager(s, m2.fyp_per_agent, 79.0, base)["total"]
        cliff[s] = (c80 - c79) / c80 * 100 if c80 else 0.0
        cite = {"AIA": "[AIAVAD 2601-034 : 3-5]", "Chubb": "[CHH0DCEB260008V : 5-7]", "Manulife": "[0047M01_2026 : 1-2]", "Hybrid": "PROPOSAL (hybrid_scheme.py)"}[s]
        trap(s, "self_vs_manage", "Tự bán vs quản lý thuần", mg2 - a1,
             f"Đại lý Mốc 1 {vn(a1)} tr/th; quản lý nhóm 5 người (phí thuần) {vn(mg2)} tr/th → {'quản lý thu ÍT hơn tự bán' if mg2 < a1 else 'quản lý thu nhiều hơn tự bán'}"
             + (" (chưa gồm khoản Duy trì chất lượng HĐ tính trên RYC — vì vậy thấp hơn cột Tổng của Chubb UM ở bảng 01)" if s == "Chubb" else ""), cite,
             "PROPOSAL" if s == "Hybrid" else "MODEL_OUTPUT")
        trap(s, "flat_team", "Bẫy giữ đội phẳng", fl3 / st3,
             f"Ban 15 ĐL: để phẳng (15 trực tiếp) {vn(fl3)} vs có 2 quản lý con {vn(st3)} tr/th → tỷ lệ {vn(fl3 / st3, 2)}×", cite,
             "PROPOSAL" if s == "Hybrid" else "MODEL_OUTPUT")
        trap(s, "k2_cliff_80", "Vách đá K2 tại 80%", (c80 - c79) / c80 * 100 if c80 else 0.0,
             f"Quản lý nhóm: K2 80% → 79% làm phí năm giảm {vn((c80 - c79) / c80 * 100 if c80 else 0, 1)}%", cite, "PROPOSAL" if s == "Hybrid" else "MODEL_OUTPUT")
    o = out["org"]
    for s in SCHEMES:
        trap(s, "fixed_cost", "Rủi ro định phí", o[s]["k85"]["fixed_share"],
             f"Phần cố định {vn(o[s]['k85']['fixed_share'])}% chi trả; năng suất giảm 50% → chi phí {vn(o[s]['half']['cost_pct'])}% FYP (từ {vn(o[s]['k85']['cost_pct'])}%)",
             {"AIA": "[AIAVAD 2601-035 : 3]", "Chubb": "[CHH0DCEB260003V : 5-6]", "Manulife": "[0048M01_2026 : 1]", "Hybrid": "PROPOSAL"}[s],
             "PROPOSAL" if s == "Hybrid" else "MODEL_OUTPUT")
    # Manulife MBA Pro — HYPOTHESIS
    ag = calc_manulife_agent_12m([m2.fyp_per_agent * FYC_RATE] * 12, [m2.fyp_per_agent] * 12, [1] * 12, k2=85.0)
    per = [ag["monthly_bonus_by_month"][mm] + (ag["quarterly_bonus_by_quarter"][mm // 3] if mm % 3 == 2 else 0.0) for mm in range(12)]
    fy5 = m2.fyp_per_agent * FYC_RATE * 5
    no = calc_manulife_um_12m([(fy5, 0, 0, 0)] * 12, [5] * 12, [5 * x for x in per], 85.0)
    yes = calc_manulife_um_12m([(fy5, 0, 0, 0)] * 12, [5] * 12, [5 * x for x in per], 85.0, mba_pro_title="Vang")
    trap("Manulife", "mba_pro_sensitivity", "Độ nhạy danh hiệu MBA Pro (Vàng)", (yes["total_earned"] - no["total_earned"]) / 12,
         f"UM+ Mốc 2: không danh hiệu {vn(no['total_earned'] / 12)} → MBA Pro Vàng {vn(yes['total_earned'] / 12)} tr/th (phí hoạt động 50%→100% + phí dài hạn 100%)",
         "[0047M01_2026 : 2], [0047M01_2026 : 5]", "HYPOTHESIS")
    a80 = H.hybrid_agent_12m(30, 2, 80.0, "V1", "FULL_TIME", base)["total_earned"]
    a79 = H.hybrid_agent_12m(30, 2, 79.0, "V1", "FULL_TIME", base)["total_earned"]
    trap("Hybrid", "agent_k2_cliff", "Vách đá K2 của đại lý Full-time", (a80 - a79) / a80 * 100,
         f"Đại lý Full-time 30tr FYP: K2 80% → 79% làm thu nhập năm giảm {vn((a80 - a79) / a80 * 100)}% ({vn(a80 / 12)} → {vn(a79 / 12)} tr/th) vì mất trọn trợ cấp — số này không gồm tái tục; con số Mốc 1 ở bảng 01 gồm tái tục (A7) và tính ở K2 85% nên cao hơn",
         "PROPOSAL (hybrid_scheme.py)", "PROPOSAL")
    q1 = H.hybrid_agent_12m(30, 2, 85.0, "V1", "FULL_TIME", base)["total_earned"]
    q0 = H.hybrid_agent_12m(29.9, 2, 85.0, "V1", "FULL_TIME", base)["total_earned"]
    trap("Hybrid", "quota_cliff", "Vách đá quota & dồn hợp đồng", (q1 - q0) / 12,
         f"FYP 30 → 29,9tr/tháng: thu nhập {vn(q1 / 12)} → {vn(q0 / 12)} tr/th — động cơ dồn/chuyển hợp đồng giữa các tháng để chạm quota (HYPOTHESIS về hành vi)",
         "PROPOSAL (hybrid_scheme.py)", "PROPOSAL")
    aia_norec = calc_aia_cql_12m([fy5] * 12, [5] * 12, fy_pct=85.0, tot_pct=85.0, quarterly_new_recruits=[0, 0, 0, 0])["total_earned"]
    aia_rec = manager("AIA", m2.fyp_per_agent, 85.0, base)["total"]
    trap("AIA", "recruit_gate", "Cổng tuyển mới", (aia_rec - aia_norec) / 12,
         f"Quản lý nhóm AIA: có tuyển (1/2/2/2 người mới/quý) {vn(aia_rec / 12)} vs không tuyển {vn(aia_norec / 12)} tr/th", "[AIAVAD 2601-034 : 4-5]")

    # ---------- Rubric 5 trụ cột ----------
    inc = {}
    for s in SCHEMES:
        inc[s] = [agent(s, m1.fyp_month, 85.0, base, with_renewal=True)["total"], manager(s, m2.fyp_per_agent, 85.0, base)["total"],
                  manager(s, m3.fyp_per_agent, 85.0, base, n_sub=2, rank="DM")["total"],
                  leader(s, ms["M4"].fyp_month, ms["M4"].agents, 85.0, base)["total"]]
    mx = [max(inc[s][i] for s in SCHEMES) for i in range(4)]
    components = {"AIA": (11, "2601-034 mục A.I–A.VI + B (7) [AIAVAD 2601-034 : 3-6]; 2601-035 mục A.1–A.4 (4) [AIAVAD 2601-035 : 3-5]"),
                  "Chubb": (13, "0008V mục II.1–II.5 (5) [CHH0DCEB260008V : 3]; 0003V mục II.1–II.8 (8) [CHH0DCEB260003V : 4]"),
                  "Manulife": (9, "0047M01 A.I–A.V (5) [0047M01_2026 : 1-5]; 0048M01 A.I–A.IV (4) [0048M01_2026 : 1-3]"),
                  "Hybrid": (5, "cùng đơn vị đếm với 3 hãng — 1 khoản = 1 mục chi trả có công thức riêng (các đời gián tiếp cùng công thức gộp 1 như [AIAVAD 2601-034 : 4]; phần giữ lại của cùng khoản không tính riêng): "
                                "override trực tiếp; phí gián tiếp (đời 1–2); thưởng trả chậm quản lý (quỹ riêng 12% FYC); phí cơ bản lãnh đạo; override lãnh đạo (gồm phần trả chậm giữ lại) (hybrid_scheme.py)")}
    ops = {"AIA": (3.0, "Chấm công ≥50% (CQL) / ≥70% (PAF+), khóa học bắt buộc, trả chậm tới 2030 cần TOT ≥85% — nhiều cổng hành chính [AIAVAD 2601-034 : 3-5]"),
           "Chubb": (2.5, "RD phải có biên bản nghiệm thu dịch vụ hàng tháng; 9 trường hợp tạm giữ phí; 3 văn bản quy định chung không có trong nguồn (260005V/006V/009V) [CHH0DCEB260003V : 12-15]"),
           "Manulife": (3.5, "Hai hình thức hợp đồng PSM+/HKD cùng biểu phí, chuyển đổi bảo lưu kết quả; HKD tự xuất hóa đơn — tách rủi ro thuế [0048M01_2026 : 5-6]; điều kiện 'Đội ngũ chuyên cần' 4 buổi/tháng [0047M01_2026 : 3]"),
           "Hybrid": (3.5, "Ít khoản, một cổng K2 ≥80% thống nhất; CHƯA đối chiếu pháp lý (TT 67/2023, NĐ 97/2026 — CONDITIONAL); trợ cấp Full-time cần quy trình xác nhận quota/CC")}
    for s in SCHEMES:
        o85, o65, half = o[s]["k85"], o[s]["k65"], o[s]["half"]
        drop = (o85["total"] - o65["total"]) / o85["total"] * 100
        p1 = round((lin(drop, 30.0, 0.0) + lin(flat[s], 1.0, 3.0) + lin(cliff[s], 5.0, 30.0)) / 3, 2)
        wc = o[s]["worst"]
        p2 = round((lin(wc["cost_pct"], 60.0, 100.0) + lin(half["cost_pct"], 70.0, 130.0) + lin(o85["deferred_share"], 15.0, 0.0)) / 3, 2)
        p3 = round(1 + 4 * sum(inc[s][i] / mx[i] for i in range(4)) / 4, 2)
        p4 = lin(components[s][0], 4, 14)
        p5 = ops[s][0]
        rows = [("Định hướng hành vi", 0.25, p1, "computed",
                 f"Chi trả giảm {vn(drop)}% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc {vn(flat[s], 2)}× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% {vn(cliff[s])}% (≤5% = 5, ≥30% = 1)"),
                ("An toàn tài chính / ROI", 0.25, p2, "computed",
                 f"Chi phí kịch bản xấu nhất ({o[s]['worst_name']}) {vn(wc['cost_pct'])}% FYP (≤60% = 5, ≥100% = 1); năng suất −50% → {vn(half['cost_pct'])}% (≤70% = 5, ≥130% = 1); trả chậm {vn(o85['deferred_share'])}% (≥15% = 5)"),
                ("Sức cạnh tranh thu nhập", 0.20, p3, "computed",
                 "Trung bình thu nhập 4 mốc / mức cao nhất trong 4 phương án: " + " · ".join(f"M{i + 1} {vn(inc[s][i] / mx[i] * 100, 0)}%" for i in range(4))),
                ("Độ đơn giản & dễ tính", 0.15, p4, "computed", f"{components[s][0]} khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): {components[s][1]}"),
                ("Vận hành & Pháp lý", 0.15, p5, "judgement", ops[s][1])]
        for pillar, wgt, sc, method, ev in rows:
            out["rubric"].append({"id": f"{s}|{pillar}", "scheme": s, "pillar": pillar, "weight": wgt, "score": sc, "method": method,
                                  "evidence": ev, "label": "PROPOSAL" if s == "Hybrid" else ("MODEL_OUTPUT" if method == "computed" else "JUDGEMENT"),
                                  "confidentiality": "restricted" if s in CONF else "public"})
    out["weighted"] = {s: round(sum(r["weight"] * r["score"] for r in out["rubric"] if r["scheme"] == s), 2) for s in SCHEMES}

    # ---------- Chính sách Đề xuất 2026 theo vùng ----------
    for reg, meta in H.REGIONS.items():
        c = meta["coef"]
        for basis, mult in (("national_fyp", 1.0), ("regional_fyp", c)):
            rows = [("M1", "FULL_TIME", "Đại lý Full-time", lambda b=mult: agent("Hybrid", ms["M1"].fyp_month * b, 85.0, base, reg, "FULL_TIME", with_renewal=True), ms["M1"].fyp_month * mult),
                    ("M1", "PART_TIME", "Đại lý Part-time", lambda b=mult: agent("Hybrid", ms["M1"].fyp_month * b, 85.0, base, reg, "PART_TIME", with_renewal=True), ms["M1"].fyp_month * mult),
                    ("M2", "MANAGER", "Trưởng nhóm (phí thuần)", lambda b=mult: manager("Hybrid", ms["M2"].fyp_per_agent * b, 85.0, base, region=reg), ms["M2"].fyp_month * mult),
                    ("M3", "MANAGER", "Trưởng ban (phí thuần)", lambda b=mult: manager("Hybrid", ms["M3"].fyp_per_agent * b, 85.0, base, n_sub=2, region=reg), ms["M3"].fyp_month * mult),
                    ("M4", "LEADER", "Lãnh đạo khu vực (phí thuần)", lambda b=mult: leader("Hybrid", ms["M4"].fyp_month * b, ms["M4"].agents, 85.0, base, reg), ms["M4"].fyp_month * mult)]
            for mid, track, role, fn, fyp in rows:
                r = fn()
                quota = H.FT_QUOTA_FYP_MONTH * c if track in ("FULL_TIME", "PART_TIME") else (H.LEADER_TARGET_FYP_MONTH * c if track == "LEADER" else None)
                out["regional"].append({"id": f"{reg}|{track}|{mid}|{basis}", "region": reg, "region_name": meta["name"], "coefficient": c,
                                        "track": track, "milestone_id": mid, "role": role, "basis": basis, "fyp_month": round(fyp, 2),
                                        "quota_fyp_month": None if quota is None else round(quota, 2),
                                        "income_vnd_m_month": round(r["total"] / 12, 2), "cash_y1_vnd_m_month": round(r["cash"] / 12, 2),
                                        "label": "PROPOSAL", "confidentiality": "public"})
    out["cost_cap_ok"] = o["Hybrid"]["worst"]["cost_pct"] <= H.COST_CAP_PCT_FYP
    out["cost_cap_headroom"] = round(H.COST_CAP_PCT_FYP - o["Hybrid"]["worst"]["cost_pct"], 2)
    out["params"] = {"k2_gate": H.K2_GATE_PCT, "cost_cap": H.COST_CAP_PCT_FYP, "ft_quota": H.FT_QUOTA_FYP_MONTH, "ft_cc": H.FT_MIN_CC_MONTH,
                     "ft_allowance": H.FT_ALLOWANCE_MONTH, "pt_mult": H.PART_TIME_RATE_MULT, "leader_target": H.LEADER_TARGET_FYP_MONTH,
                     "song_hanh": {k: (list(v) if isinstance(v, tuple) else v) for k, v in base.__dict__.items()}}
    out["enterprise_art52"] = {s: calc_enterprise_hierarchy_cost(s, 85.0)["art52_bonus_pct_fyp"] for s in ("AIA_Alpha_2026", "Chubb_Agency_2026")}
    return out


# =============================================================================
def write_reports(d: dict) -> None:
    o, W = d["org"], d["weighted"]
    names = {"AIA": "AIA Alpha", "Chubb": "Chubb Life", "Manulife": "Manulife", "Hybrid": "**Chính sách Đề xuất 2026**"}
    L = []
    w = L.append
    w("# 02 — Phân tích hành vi, Trade-off & ROI 3 tầng (Giai đoạn 2)")
    w("")
    w("> Số 3 hãng = `MODEL_OUTPUT`; số Chính sách Đề xuất 2026 = `PROPOSAL`. "
      "**\"ROI\" ở đây là chi phí / FYP và chi phí / phí còn duy trì — KHÔNG phải ROI thực tế** (VNB, biên lợi nhuận, OpEx thật = `UNKNOWN`). "
      "Số Manulife dựa trên 2 văn bản chính sách thu nhập 2026 của Manulife.")
    w("")
    w("**Mô hình tổ chức dùng chung (`ASSUMPTION`):** khu vực Mốc 4 — 45 đại lý × 26,7tr FYP/tháng (1,2 tỷ), 1 lãnh đạo (5 ĐL trực tiếp) + 2 trưởng ban (5 ĐL + 2 trưởng nhóm) + 6 trưởng nhóm. "
      "Lãnh đạo: AIA PAF · Chubb RD · Manulife PSM/SM (đạt 100% chỉ tiêu) · Chính sách Đề xuất 2026: lãnh đạo vùng. Chi phí năm đầu = hoa hồng FYC + thưởng + phí quản lý; không gồm tái tục.")
    w("")
    w("## 1. ROI 3 tầng")
    w("")
    w("| Phương án | (1) Tổng chi / FYP — K2 85% | (1b) Khi năng suất −50% | (2) Chi phí / phí còn duy trì — K2 85% | (2) K2 65% | Chi trả giảm khi K2 sập | (3) Tiền mặt năm 1 | (3) Trả các năm sau | Phần cố định | Biểu phí nguồn | Nhãn |")
    w("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|")
    for s in SCHEMES:
        a, b, h = o[s]["k85"], o[s]["k65"], o[s]["half"]
        drop = (a["total"] - b["total"]) / a["total"] * 100
        w(f"| {names[s]} | {vn(a['cost_pct'])}% | {vn(h['cost_pct'])}% | {vn(a['cost_per_persisted_pct'])}% | {vn(b['cost_per_persisted_pct'])}% | {vn(drop)}% | {vn(a['cash_share'])}% | {vn(a['deferred_share'])}% | {vn(a['fixed_share'])}% | {SCHEME_SRC[s]} | `{'PROPOSAL' if s == 'Hybrid' else 'MODEL_OUTPUT'}` |")
    w("")
    w("**Kiểm trần theo kịch bản** (Mốc 4 chuẩn cho mỗi ĐL 26,7tr FYP — DƯỚI quota 30tr, nên trợ cấp Full-time không bật; vì vậy phải kiểm thêm kịch bản đạt quota):")
    w("")
    w("| Phương án | Kịch bản | Tổng chi / FYP | Phần cố định | Nguồn | Nhãn |")
    w("|---|---|---:|---:|---|---|")
    for s in SCHEMES:
        for nm, sc in o[s]["scenarios"].items():
            w(f"| {names[s]} | {nm}{' **(xấu nhất)**' if nm == o[s]['worst_name'] else ''} | {vn(sc['cost_pct'])}% | {vn(sc['fixed_share'])}% | {SCHEME_SRC[s]} | `{'PROPOSAL' if s == 'Hybrid' else 'MODEL_OUTPUT'}` |")
    w("")
    if d.get("sweep"):
        sw = d["sweep"]
        w(f"Lưới quét điểm gãy Chính sách Đề xuất 2026: {len(sw)} điểm ({len(H.REGIONS)} vùng × năng suất quanh quota vùng, mọi bậc thưởng tháng, ngưỡng nhất quán, MDRT, năng suất V1 × K2 80/85/95%); "
          f"{sum(1 for x in sw if x['cost_pct'] > H.COST_CAP_PCT_FYP)} điểm vượt trần {int(H.COST_CAP_PCT_FYP)}%. "
          "Bản nháp trước bỏ sót kịch bản V3 đạt đúng quota vùng (76,2% — VƯỢT); bản này đã nhân trợ cấp Full-time theo hệ số vùng và giãn mọi ngưỡng đại lý theo vùng.")
        w("")
    if d.get("fyc_sensitivity"):
        fs = {(r["scheme"], r["rate"]): r for r in d["fyc_sensitivity"]}
        w("**Độ nhạy cơ cấu sản phẩm — tỷ lệ hoa hồng năm đầu 25% / 30% / 40% FYP** (40% ≈ nghiêng bảo vệ thuần/tử kỳ, >50% HĐ mới 9T/2026 — `SOURCE_CLAIM`). "
          "Chính sách Đề xuất 2026 tính thưởng & phí quản lý trên **FYC chuẩn hóa = FYP × 30%** (hoa hồng vẫn theo sản phẩm) và có **trần quỹ thu nhập cây đại lý 75% FYP**: "
          "vượt trần thì thưởng & phí quản lý biến đổi co theo cùng tỷ lệ. 3 hãng trả trên FYC thật theo văn bản của họ. "
          "Trần 75% là trần quỹ thu nhập cây đại lý, KHÔNG phải tổng chi phí khai thác trên BCTC (gồm thêm văn phòng, marketing, bancassurance — wheel-check r2 câu 3).")
        w("")
        w("| Phương án | Hoa hồng 25% — chuẩn | 25% — xấu nhất | Hoa hồng 30% — chuẩn | 30% — xấu nhất | Hoa hồng 40% — chuẩn | 40% — xấu nhất | Quỹ thưởng còn trả ở 40% xấu nhất | Nguồn | Nhãn |")
        w("|---|---:|---:|---:|---:|---:|---:|---:|---|---|")
        for s in SCHEMES:
            r25, r30, r40 = fs[(s, 0.25)], fs[(s, 0.30)], fs[(s, 0.40)]
            pool = f"{vn(r40['pool_scale_worst'] * 100)}%" if s == "Hybrid" else "—"
            w(f"| {names[s]} | {vn(r25['std'])}% | {vn(r25['worst'])}% | {vn(r30['std'])}% | {vn(r30['worst'])}% | {vn(r40['std'])}% | {vn(r40['worst'])}% | {pool} | {SCHEME_SRC[s]} | `{'PROPOSAL' if s == 'Hybrid' else 'MODEL_OUTPUT'}` |")
        w("")
    w(f"- **Tầng 1:** trần đề xuất 75% FYP, kiểm ở kịch bản xấu nhất. Chính sách Đề xuất 2026 {vn(o['Hybrid']['worst']['cost_pct'])}% ({o['Hybrid']['worst_name']}) → {'**ĐẠT**' if d['cost_cap_ok'] else '**VƯỢT**'} trần, khoảng dư chỉ {vn(d['cost_cap_headroom'])} điểm %. Rủi ro định phí thật của Chính sách Đề xuất 2026 là khi **nhiều** đại lý đạt quota, không phải khi năng suất giảm.")
    w("- **Điều 52 TT 67/2023** (thưởng + hỗ trợ đại lý, không gồm hoa hồng, ≤ 30% FYP phí định kỳ — `CONDITIONAL`): "
      + " · ".join(f"{names[s]} {vn(o[s]['k85']['art52_pct'])}% (xấu nhất {vn(o[s]['worst']['art52_pct'])}%)" for s in SCHEMES)
      + f" — {'tất cả **ĐẠT**' if all(o[s]['worst']['art52_pct'] <= 30 for s in SCHEMES) else '**CÓ PHƯƠNG ÁN VƯỢT**'}. Phí quản lý tính là phí dịch vụ (NĐ 97/2026), cùng định nghĩa với mô hình enterprise. `MODEL_OUTPUT` / Chính sách Đề xuất 2026 `PROPOSAL`.")
    w(f"  - Vì sao Chính sách Đề xuất 2026 nhảy từ {vn(o['Hybrid']['k85']['art52_pct'])}% lên {vn(o['Hybrid']['worst']['art52_pct'])}%: kịch bản xấu nhất ({o['Hybrid']['worst_name']}) là đại lý năng suất rất cao, chạm bậc thưởng tháng cao nhất và MDRT, nên phần thưởng (không gồm hoa hồng) tăng mạnh so với FYP; ở mốc chuẩn 26,7tr FYP/ĐL đa số đại lý chỉ ở bậc thưởng thấp. Mức xấu nhất vẫn dưới trần 30%, khoảng dư {vn(30 - o['Hybrid']['worst']['art52_pct'])} điểm %.")
    w("- **Tầng 2:** chi phí trên mỗi đồng phí còn duy trì sang năm 2 = chi phí ÷ (FYP × K2). Khi K2 sập 85%→65%, phương án gắn thưởng với K2 tốt thì chi trả **giảm theo**; phương án yếu thì chi phí trên phí còn lại **tăng vọt**.")
    w("- **Tầng 3:** phần trả các năm sau (AIA thưởng năm 15/25/60% đến 2030; Manulife phí dài hạn 30/30/40%, M-Star năm trả tháng 2 năm sau; Chính sách Đề xuất 2026 trả chậm khi K2 ≥80%) giữ người và giảm áp lực tiền mặt năm 1.")
    w("")
    w("## 1b. Vế doanh số — phải bán thêm bao nhiêu để hòa vốn (`PROPOSAL`)")
    w("")
    w("**Cách đo (chỉ dùng số của mô hình, không giả định biên lợi nhuận — biên lợi nhuận thật = `UNKNOWN`):** phần phí giữ lại sau chi trả kênh đại lý = FYP × (1 − tổng chi/FYP). "
      "Hòa vốn = mức FYP mà phần giữ lại của Chính sách Đề xuất 2026 bằng phần giữ lại nếu công ty trả theo cơ chế của từng hãng ở mức FYP hiện tại (1,2 tỷ/tháng). "
      "Đây **không phải lợi nhuận**: chưa trừ chi phí văn phòng, marketing, dự phòng nghiệp vụ.")
    w("")
    w("- **Thêm đại lý** (giữ cơ cấu năng suất): tỷ lệ chi phí gần như không đổi → FYP cần thêm = (1 − chi phí hãng) ÷ (1 − chi phí đề xuất) − 1.")
    w("- **Tăng năng suất mỗi đại lý**: thưởng lũy tiến làm tỷ lệ chi phí đổi theo — mô hình tính lại từng bước +0,5%; cột \"bền\" là mức mà từ đó trở lên luôn hòa vốn (qua được vách quota 30tr).")
    w("")
    w("| Cơ cấu đại lý | So với | Chi phí hãng | Chi phí đề xuất | Chi thêm (tỷ/năm, cùng FYP) | Hòa vốn bằng thêm ĐL | Hòa vốn bằng năng suất | Năng suất (bền) | Nguồn | Nhãn |")
    w("|---|---|---:|---:|---:|---:|---:|---:|---|---|")
    pc = lambda x: "chưa hòa vốn trong +100%" if x is None else ("đã có lợi ở cùng FYP" if x <= 0 else f"+{vn(x)}%")
    for r in d.get("breakeven", []):
        w(f"| {'Bán đều 26,7tr/ĐL' if r['basis'] == 'uniform' else '4 nhóm năng suất'} | {names[r['vs']]} | {vn(r['cost_old_pct'])}% | {vn(r['cost_new_pct'])}% | "
          f"{vn(r['extra_cost_bn_year'], 2)} | {pc(r['agents_pct'])} | {pc(r['prod_pct'])} | {pc(r['prod_stable_pct'])} | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |")
    w("")
    if d.get("mix"):
        mx = d["mix"]
        w("**Phân bổ năng suất 4 nhóm** (`ASSUMPTION`, cùng tổng 45 ĐL × 1,2 tỷ FYP/tháng): " + " · ".join(f"{n} ĐL «{nm}» {vn(f)}tr" for nm, n, f in PRODUCTIVITY_MIX) +
          ". Khi bán không đều, tổng chi/FYP tăng ở mọi phương án vì nhóm Top chạm bậc thưởng cao: " +
          " · ".join(f"{names[s]} {vn(d['org'][s]['k85']['cost_pct'])}% → {vn(mx[s]['cost_pct'])}%" for s in SCHEMES) +
          f". Chính sách Đề xuất 2026 vẫn dưới trần {int(H.COST_CAP_PCT_FYP)}%; thu nhập đại lý theo nhóm (tr/tháng, năm đầu): " +
          " · ".join(f"{vn(f)}tr → {vn(v)}" for f, v in mx["Hybrid"]["agent_income_m"].items()) + ".")
        w("")
    w("**Chỉ tiêu đo cho thí điểm** (không cần giả định thêm): số đại lý có hợp đồng trong tháng, FYP/đại lý hoạt động, tỷ lệ đại lý đạt quota, K2 (≥ 85%), "
      "tỷ lệ đại lý mới còn hoạt động sau 13 tháng, và tổng chi/FYP so với trần 75% — đo hằng tháng ở văn phòng thí điểm và văn phòng đối chứng.")
    w("")
    w("## 2. Bẫy hành vi (Gaming) & điểm gãy")
    w("")
    w("| Hãng | Bẫy | Đo được | Trích dẫn | Nhãn |")
    w("|---|---|---|---|---|")
    for t in d["traps"]:
        w(f"| {names[t['scheme']]} | {t['trap']} | {t['value_text']} | {t['citation']} | `{t['label']}` |")
    w("")
    w("Đọc nhanh: (a) **tự bán vs quản lý** — ở AIA và Manulife, lên quản lý nhóm 5 người mà bỏ bán thì thu nhập giảm; (b) **đội phẳng** — tỷ lệ >1 nghĩa là giữ mọi người trực tiếp có lợi hơn phát triển quản lý con; "
      "(c) **vách đá K2** — giảm 1 điểm K2 quanh 80% làm mất một bậc hệ số; (d) **định phí** — phí cố định không co khi năng suất giảm.")
    w("")
    w("## 3. Rubric 5 trụ cột (Compensation Designer)")
    w("")
    w("| Trụ cột (trọng số) | " + " | ".join(names[s] for s in SCHEMES) + " |")
    w("|---|" + "---:|" * len(SCHEMES))
    pillars = [r["pillar"] for r in d["rubric"] if r["scheme"] == "AIA"]
    for p in pillars:
        wt = next(r["weight"] for r in d["rubric"] if r["pillar"] == p)
        w(f"| {p} ({int(wt * 100)}%) | " + " | ".join(vn(next(r["score"] for r in d["rubric"] if r["scheme"] == s and r["pillar"] == p), 2) for s in SCHEMES) + " |")
    w("| **Điểm có trọng số (1–5)** | " + " | ".join(f"**{vn(W[s], 2)}**" for s in SCHEMES) + " |")
    w("")
    w("Căn cứ từng điểm:")
    w("")
    for s in SCHEMES:
        w(f"- **{names[s]}:** " + "; ".join(f"*{r['pillar']}* — {r['evidence']} (`{r['label']}`)" for r in d["rubric"] if r["scheme"] == s))
    w("")
    w("> **Lưu ý thiên lệch:** bậc đệm K2 75–80% và trần đội phẳng của Chính sách Đề xuất 2026 được thêm SAU khi đo bằng chính rubric này — thiết kế đã được hiệu chỉnh theo thước đo, nên rubric không phải phép thử khách quan cho Chính sách Đề xuất 2026. "
      "Độ nhạy: chấm Vận hành & Pháp lý của Chính sách Đề xuất 2026 ở 2,0 (chưa đối chiếu pháp lý) thì điểm giảm 0,225.")
    w("")
    w("> 3 trụ cột đầu tính bằng công thức công khai ở trên; *Độ đơn giản* đếm khoản phí theo mục lục văn bản; *Vận hành & Pháp lý* là đánh giá có dẫn chứng (`JUDGEMENT`). "
      "Điểm Chính sách Đề xuất 2026 là **tự chấm của bên thiết kế** — cần một bên độc lập chấm lại trước khi dùng làm kết luận.")
    w("")
    w("## 4. Ghi chú độ nhạy Manulife MBA Pro (`HYPOTHESIS`)")
    w("")
    w(next(t["value_text"] for t in d["traps"] if t["id"] == "Manulife|mba_pro_sensitivity") + " `[0047M01_2026 : 2]`, `[0047M01_2026 : 5]`. Tiêu chí danh hiệu (0050M01/2026) không có trong nguồn — chưa đưa vào base case.")
    w("")
    w("## 5. Pháp lý tham chiếu")
    w("")
    o = d["org"]   # AUD D6 (audit r1): dùng CÙNG mô hình khu vực 45 ĐL của báo cáo này, không kéo số từ mô hình 1 vùng 12 tỷ
    w("Rổ thưởng + hỗ trợ đại lý / FYP trên mô hình khu vực 45 ĐL (ngưỡng 30% Điều 52, `CONDITIONAL / SOURCE_NOT_VERIFIED`): " +
      ", ".join(f"{s} {vn(o[s]['k85']['art52_pct'])}% (xấu nhất {vn(o[s]['worst']['art52_pct'])}%)" for s in SCHEMES) +
      ". Từ 01/01/2027, Điều 17 TT 96/2026 thêm trần 7% cho phí nộp 1 lần (`SOURCE_CLAIM`). Cần Pháp chế đối chiếu ảnh trang Điều 51–52 trong 44/2026/VBHN-TT-BTC trước khi ban hành.")
    w("")
    w("## 6. Negative Proof — kết luận \"không có trong nguồn\" của báo cáo này")
    w("")
    w("| Kết luận | Đã quét | Là 1 trong 9 file nguồn? | Trang có nhắc tới (chỉ dẫn chiếu, không phải nội dung) |")
    w("|---|---|---|---|")
    for np_ in d["negative_proof"]:
        hits = "; ".join(f"{fid}: " + ", ".join(f"`{k}` {pp}" for k, pp in pages.items() if pp) for fid, _, pages in np_["log"] if any(pages.values())) or "0 trang"
        w(f"| {np_['claim']} | {np_['files_scanned']}/9 file (tên file + toàn văn từng trang) | {'CÓ' if np_['is_a_source_file'] else 'KHÔNG'} | {hits} |")
    w("")
    w("## 7. Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)")
    w("")
    tbl, tot = rubric_table(len(FILE_IDS), 15, 15, 3, 3, d["ev02"]["cited"], d["ev02"]["numeric"],
                            sum(1 for x in d["negative_proof"] if not x["is_a_source_file"]), len(d["negative_proof"]), d["ev02"]["labelled"], d["ev02"]["numeric"])
    w(tbl)
    w("")
    w("Tiêu chí 1 theo kiểm kê `00_Role_Mapping_Audit.md` (9/9 file khớp SHA-256, 15/15 trang scan). Tiêu chí 2: 3 chức danh lãnh đạo Mốc 4 (AIA PAF, Chubb RD, Manulife PSM/SM) lấy từ ma trận `00_Role_And_Benefit_Matrix.md`. "
      "Tiêu chí 3/5 đếm tự động mọi dòng bảng có số ở mục 1–2 (dòng Chính sách Đề xuất 2026 trích `PROPOSAL (hybrid_scheme.py)` vì không có trong PDF).")
    d["rubric02"] = tot
    OUT02.write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---------------- 03 ----------------
    P = d["params"]
    L = []
    w = L.append
    w("# 03 — Chính sách Đề xuất 2026 & Phân vùng")
    w("")
    w("> `PROPOSAL` — không phải chính sách đã ban hành. Sinh bởi `scripts/build_phase2.py`; tham số ở `model/compensation/hybrid_scheme.py`. "
      "Kế thừa bộ tham số **Song Hành** đã hiệu chỉnh (không thấp nhất thị trường ở mọi tầng, K2 ~75–90%).")
    w("")
    w("## 1. Khung chính sách")
    w("")
    w("| Thành phần | Thiết kế | Lý do (bài học từ 3 hãng) |")
    w("|---|---|---|")
    w(f"| Đường ray **Full-time** (cam kết) | Thưởng tháng 100% bậc Song Hành + trợ cấp cam kết {vn(P['ft_allowance'])}tr/tháng (Vùng 1; vùng khác × hệ số vùng) khi FYP ≥ quota vùng, ≥{P['ft_cc']} HĐ/tháng và K2 ≥{int(P['k2_gate'])}% | Nuôi quân có điều kiện như AIA Exchange nhưng có cổng chất lượng; phần cố định nhỏ |")
    w(f"| Đường ray **Part-time** (thuần biến phí) | Thưởng tháng {int(P['pt_mult'] * 100)}% bậc Song Hành, không trợ cấp | Không phát sinh định phí cho người bán không đều |")
    w(f"| **Chốt chặn K2 ≥ {int(P['k2_gate'])}%** | Trợ cấp Full-time chỉ khi K2 ≥{int(P['k2_gate'])}%; phần trả chậm nhận ĐỦ khi K2 ≥{int(P['k2_gate'])}%, 50% khi 75–<80%, 0 khi <75%; thưởng tháng theo hệ số K2 liên tục (sàn {vn(P['song_hanh']['k2_hard_floor_pct'], 0)}%) | Bản thử đầu (cắt hết dưới 80%) tạo vách đá −37,5% ở quản lý nhóm — lớn nhất trong 4 phương án; bậc đệm 75–80% giảm vách đá mà vẫn khóa phần thưởng lớn vào chất lượng |")
    w(f"| Giảm (chưa xóa) bẫy đội phẳng | Override nhóm trực tiếp đủ tỷ lệ tới {vn(H.DIRECT_FULL_RATE_CAP_FYC, 0)}tr FYC/tháng (không giãn theo vùng), phần vượt {int(H.DIRECT_EXCESS_RATE_SHARE * 100)}% | Cả 3 hãng trả cho đội phẳng nhiều hơn đội có quản lý con (mục 2 của 02); với Chính sách Đề xuất 2026 tỷ lệ vẫn > 1 — chỉ giảm, chưa xóa |")
    w(f"| Quản lý | Override {vn(P['song_hanh']['mgr_direct_base_rate'] * 100)}% × hệ số K2 (trần {vn(P['song_hanh']['mgr_direct_max_rate'] * 100)}%) FYC nhóm; gián tiếp 2 đời ({vn(P['song_hanh']['mgr_indirect_l1_rate'] * 100)}% / ½), cổng FYC nhóm ≥ {vn(P['song_hanh']['mgr_indirect_gate_fyc'])}tr × hệ số vùng; trả chậm {vn(P['song_hanh']['mgr_deferred_3y_rate'] * 100)}% FYC nhóm | Học cổng 15tr của Chubb, bỏ chuỗi gián tiếp vô hạn |")
    w(f"| Lãnh đạo vùng | Phí cơ bản {vn(P['song_hanh']['rd_base_monthly'])}tr × % đạt chỉ tiêu (sàn 30%, trần 140%) + override {vn(P['song_hanh']['rd_direct_fyc_rate'] * 100, 2)}% FYC vùng × K2; {vn(P['song_hanh']['rd_deferred_3y_share'] * 100, 0)}% override trả chậm | Học Manulife: phí cơ bản gắn chỉ tiêu, không cố định cứng |")
    w(f"| Trần chi phí | Tổng chi / FYP ≤ {int(P['cost_cap'])}% ở kịch bản XẤU NHẤT | Kiểm tự động: chuẩn {vn(o['Hybrid']['k85']['cost_pct'])}%; xấu nhất ({o['Hybrid']['worst_name']}) {vn(o['Hybrid']['worst']['cost_pct'])}% → {'ĐẠT' if d['cost_cap_ok'] else 'VƯỢT'}, dư {vn(d['cost_cap_headroom'])} điểm % |")
    w("")
    w("## 2. Bảng hệ số vùng (Regional Tiering) — `PROPOSAL`")
    w("")
    w("| Vùng | Hệ số quota FYP | Quota Full-time (tr FYP/tháng) | Trợ cấp Full-time (tr/tháng) | Chỉ tiêu lãnh đạo (tr FYP/tháng) | Giữ nguyên |")
    w("|---|---:|---:|---:|---:|---|")
    for reg, meta in H.REGIONS.items():
        w(f"| {meta['name']} | {vn(meta['coef'] * 100, 1)}% | {vn(P['ft_quota'] * meta['coef'])} | {vn(P['ft_allowance'] * meta['coef'], 2)} | {vn(P['leader_target'] * meta['coef'], 0)} | ≥{P['ft_cc']} HĐ/tháng; K2 ≥{int(P['k2_gate'])}% — PROPOSAL (hybrid_scheme.py) `PROPOSAL` |")
    w("")
    w("Hệ số giãn **mọi ngưỡng FYP/FYC** của Chính sách Đề xuất 2026: quota, bậc thưởng tháng, ngưỡng thưởng nhất quán (4tr FYC/tháng), MDRT (400tr FYC/năm), thưởng nhập môn (8tr), cổng gián tiếp, chỉ tiêu lãnh đạo; và **trợ cấp Full-time** (3tr × hệ số). "
      "**Không giãn:** tỷ lệ %, số hợp đồng, K2, và trần override đội phẳng 60tr FYC (nhắm vào quy mô đội, không phải năng suất). "
      "Hệ số = lương tối thiểu vùng 2026 theo NĐ 293/2025/NĐ-CP (5,31 / 4,73 / 4,14 / 3,70 tr/tháng → 100 / 89 / 78 / 70%) — `SOURCE_CLAIM` (wheel-check r2 câu 5); thay bộ tự đặt 100 / 82,5 / 67,5% trước đây. "
      "Đối chiếu thu nhập bình quân đầu người VHLSS 2025: thành phố lớn 84–87% Hà Nội/TP.HCM, cả nước 73%, miền núi 31–50% → Vùng IV 70% vẫn cao so với tỉnh miền núi nghèo nhất (`HYPOTHESIS`: có thể cần bậc thứ 5).")
    w("")
    w("## 3. Thu nhập theo vùng (tr/tháng)")
    w("")
    w("Hai cách đọc: **cùng FYP** (cùng năng suất ở mọi vùng) và **FYP vùng** (năng suất điển hình = FYP mốc × hệ số vùng). Đại lý = thu nhập cá nhân gồm tái tục (A7, cùng cơ sở bảng 01); quản lý = phí quản lý thuần.")
    w("")
    w("| Vai trò | " + " | ".join(f"{reg} cùng FYP | {reg} FYP vùng" for reg in H.REGIONS) + " | Nguồn |")
    w("|---|" + "---:|" * (2 * len(H.REGIONS)) + "---|")
    roles = []
    for r in d["regional"]:
        if (r["milestone_id"], r["track"], r["role"]) not in roles:
            roles.append((r["milestone_id"], r["track"], r["role"]))
    for mid, tr, role in roles:
        cells = []
        for reg in H.REGIONS:
            for basis in ("national_fyp", "regional_fyp"):
                x = next(r for r in d["regional"] if r["region"] == reg and r["track"] == tr and r["milestone_id"] == mid and r["basis"] == basis)
                cells.append(vn(x["income_vnd_m_month"]))
        w(f"| {mid} · {role} | " + " | ".join(cells) + " | PROPOSAL (hybrid_scheme.py) `PROPOSAL` |")
    w("")
    w("## 4. Đáp ứng khác biệt vùng miền (`HYPOTHESIS` — repo không có dữ liệu hành vi theo vùng)")
    w("")
    w("| Miền | Giả thuyết hành vi | Cơ chế trong Chính sách Đề xuất 2026 |")
    w("|---|---|---|")
    w("| Bắc | Trọng hệ thống, danh hiệu, lộ trình thăng tiến | Lộ trình quản lý 2 đời rõ ràng; trả chậm gắn K2 như \"danh hiệu bền\"; quota vùng 1 cho Hà Nội |")
    w("| Trung | K2 cao, hợp đồng nhỏ, năng suất thấp hơn | Hệ số vùng 2/3 hạ quota nhưng **giữ CC và K2**; thưởng tháng theo hệ số K2 liên tục thưởng chất lượng |")
    w("| Nam | Ưu tiên dòng tiền, tự chủ; quen mô hình HKD | Part-time thuần biến phí trả hàng tháng; lãnh đạo có thể chọn hình thức hợp đồng hộ kinh doanh như Manulife (cùng biểu phí — lợi ích thuế cần Pháp chế xác nhận) |")
    w("")
    w("## 5. Chấm điểm so với 3 hãng (cùng Rubric 5 trụ cột)")
    w("")
    w("| Phương án | Điểm có trọng số (1–5) |")
    w("|---|---:|")
    for s in sorted(SCHEMES, key=lambda x: -W[x]):
        w(f"| {names[s]} | {vn(W[s], 2)} — {SCHEME_SRC[s]} `{'PROPOSAL' if s == 'Hybrid' else 'MODEL_OUTPUT'}` |")
    w("")
    w("Chi tiết trụ cột và công thức: `02_Phan_Tich_MAPA_TradeOff_Va_ROI.md` mục 3. **Lưu ý:** điểm Chính sách Đề xuất 2026 do bên thiết kế tự chấm; trụ cột Vận hành & Pháp lý là đánh giá; pháp lý `CONDITIONAL`.")
    w("")
    w("## 6. Rủi ro & việc TJ cần quyết")
    w("")
    w("1. Hệ số vùng đã neo lương tối thiểu vùng NĐ 293/2025; vẫn cần dữ liệu năng suất bán hàng thật theo tỉnh của công ty để hiệu chỉnh (`PROPOSAL`).")
    w(f"2. Trợ cấp Full-time {vn(P['ft_allowance'])}tr/tháng và quota — phần cố định duy nhất; nếu tỷ lệ đạt quota thấp, chi phí thấp hơn mô hình.")
    w("3. Pháp lý: tỷ lệ thưởng/FYP và hợp đồng hộ kinh doanh cần Pháp chế đối chiếu toàn văn trước khi ban hành.")
    vr = {reg: next(r for r in d["regional"] if r["region"] == reg and r["track"] == "FULL_TIME" and r["milestone_id"] == "M1" and r["basis"] == "national_fyp")["income_vnd_m_month"] for reg in H.REGIONS}
    w(f"4. **Rủi ro lách vùng (chưa có kiểm soát — cần chọn 1 trong 3 cách dưới đây trước khi thí điểm):** cùng năng suất, đại lý vùng thấp nhất ({list(H.REGIONS)[-1]}) nhận {vn(vr[list(H.REGIONS)[-1]])} so với V1 {vn(vr['V1'])} tr/tháng và chi phí tổ chức tăng lên mức kịch bản xấu nhất ở 02 — tạo động cơ đăng ký mã vùng thấp hơn nơi bán thật. "
      "Lựa chọn: (a) gắn vùng theo địa chỉ bên mua bảo hiểm của từng hợp đồng; (b) gắn theo văn phòng quản lý, kiểm tra chéo tỷ lệ hợp đồng ngoài vùng; (c) trần: đại lý vượt 120% quota vùng 3 tháng liên tiếp chuyển sang ngưỡng vùng trên.")
    w("5. Vách đá cấp đại lý còn lại (mục 2 của 02): mất K2 80% hoặc thiếu 0,1tr quota làm mất trọn trợ cấp. Giữ nguyên có chủ đích vì đây là chốt chặn chất lượng hồ sơ; phương án mềm hơn (trợ cấp giảm dần thay vì mất trọn) để ngỏ cho giai đoạn thí điểm.")
    w("")
    w("## 7. Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)")
    w("")
    w("Báo cáo này là `PROPOSAL`: mọi tham số lấy từ `hybrid_scheme.py` / bộ Song Hành, không từ PDF; các con số đối chiếu 3 hãng nằm ở 02 (đã trích). "
      "Tiêu chí 3 đếm dòng bảng có số mang nguồn (PDF hoặc `PROPOSAL`); tiêu chí 5 đếm dòng có nhãn.")
    w("")
    tbl, tot = rubric_table(len(FILE_IDS), 15, 15, 3, 3, d["ev03"]["cited"], d["ev03"]["numeric"], 0, 0, d["ev03"]["labelled"], d["ev03"]["numeric"])
    w(tbl)
    d["rubric03"] = tot
    OUT03.write_text("\n".join(L) + "\n", encoding="utf-8")


def measure(path: Path, sections=None) -> dict:
    """Đếm dòng bảng có số (bỏ mã A1…, mã văn bản, số trang trích dẫn) → có trích dẫn? có nhãn?"""
    txt = path.read_text(encoding="utf-8")
    if sections:
        txt = "\n".join(re.split(r"^## ", txt, flags=re.M)[i] for i in sections)
    ev = {"numeric": 0, "cited": 0, "labelled": 0}
    for ln in txt.splitlines():
        if not ln.startswith("|") or re.match(r"^\|[-:| ]+\|$", ln) or ln.startswith("| Phương án | (1)") or ln.startswith("| Hãng |") or ln.startswith("| Vai trò |") or ln.startswith("| Vùng |"):
            continue
        bare = CITE_RE.sub("", ln)
        bare = re.sub(r"\b(A\d+|M\d|V\d|K2|0\d{3}M\d+_?\d*|2\d{3}-\d{3})\b", "", bare)
        if not re.search(r"\d", bare):
            continue
        ev["numeric"] += 1
        ev["cited"] += bool(CITE_RE.search(ln))
        ev["labelled"] += bool(re.search(r"`(MODEL_OUTPUT|PROPOSAL|HYPOTHESIS|VERIFIED FACT|ASSUMPTION|JUDGEMENT)`", ln))
    return ev


def main() -> int:
    d = compute()
    d["negative_proof"] = negative_proof()
    d["ev02"] = d["ev03"] = {"numeric": 1, "cited": 0, "labelled": 0}
    write_reports(d)                       # lượt 1: sinh bảng
    d["ev02"], d["ev03"] = measure(OUT02, sections=[1, 2, 3]), measure(OUT03, sections=[2, 3, 5])
    write_reports(d)                       # lượt 2: rubric đo trên chính bảng đã sinh
    if min(d["rubric02"], d["rubric03"]) < 90:
        raise SystemExit(f"rubric FAIL 02={d['rubric02']} 03={d['rubric03']}")
    txt = OUT02.read_text(encoding="utf-8") + OUT03.read_text(encoding="utf-8")
    if re.search(r"\b(nan|inf)\b", txt, re.I):
        raise SystemExit("non-finite in reports")
    print(f"wrote {OUT02.relative_to(REPO)} and {OUT03.relative_to(REPO)} · weighted {d['weighted']} · cost cap ok {d['cost_cap_ok']} · rubric 02={d['rubric02']} 03={d['rubric03']} · ev02={d['ev02']} ev03={d['ev03']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
