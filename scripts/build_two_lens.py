"""Trang "2 góc nhìn": cùng một bộ câu hỏi cho mọi phương án (khung chuẩn — thêm scheme thì thêm cột, không thêm dòng).

Phần 1 · Chính sách NÓI GÌ — 6 câu hỏi cho tầng đại lý (trích từ bộ quy tắc đã kiểm 2 lượt, qa/source-reading).
Phần 2 · Người bán NHẬN GÌ — khoản nhận, thấp / giữa / cao / bình quân, năm–quý–tháng, sau thuế, có sống được không, rủi ro.
Phần 3 · Doanh nghiệp ĐƯỢC GÌ — doanh số, chất lượng, chi phí/ROI, pháp lý, vận hành (đọc từ build_phase2, không tính lại khác).

Số ngoài (thuế, lương) chỉ dùng khi có nguồn; nguồn chưa đối chiếu toàn văn gắn `SOURCE_CLAIM`; cách hiểu luật chưa chắc
thì tính CẢ HAI cách và trình bày dạng khoảng — không chọn một cách rồi coi là đúng.
Chạy: python scripts/build_two_lens.py  → outputs/interview/04_Hai_Goc_Nhin_Nguoi_Ban_Va_Doanh_Nghiep.md + web/data/two_lens.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
for p in (REPO, REPO / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import build_phase2 as P  # noqa: E402
import model.compensation.hybrid_scheme as H  # noqa: E402

OUT_MD = REPO / "outputs/interview/04_Hai_Goc_Nhin_Nguoi_Ban_Va_Doanh_Nghiep.md"
OUT_JSON = REPO / "web/data/two_lens.json"
K2 = 85.0
NAMES = {"AIA": "AIA Alpha", "Chubb": "Chubb Life", "Manulife": "Manulife", "Hybrid": "Chính sách Đề xuất 2026"}

# ---------------- Mốc so sánh bên ngoài (có nguồn) ----------------
BENCH = {
    "min_wage": {"values": {"Vùng I": 5.31, "Vùng II": 4.73, "Vùng III": 4.14, "Vùng IV": 3.70}, "unit": "triệu đồng/tháng",
                 "source": "Lương tối thiểu vùng 2026 — Nghị định 293/2025/NĐ-CP (đã dùng trong repo, wheel-check r2 câu 5)", "label": "SOURCE_CLAIM"},
    "avg_income": {"values": {"Bình quân lao động cả nước": 9.2, "Lao động khu vực dịch vụ": 10.9}, "unit": "triệu đồng/tháng",
                   "source": "Cục Thống kê (Bộ Tài chính), thu nhập bình quân tháng quý III/2026 — đọc qua báo chí dẫn số liệu; "
                             "chưa mở được trang nso.gov.vn để đối chiếu bảng gốc",
                   "urls": ["https://www.vietnamplus.vn/thu-nhap-nguoi-lao-dong-tang-99-thi-truong-viec-lam-9-thang-tiep-tuc-phuc-hoi-post1139842.vnp",
                            "https://daibieunhandan.vn/thu-nhap-cua-lao-dong-tiep-tuc-tang-trong-quy-iii-10433108.html"],
                   "label": "SOURCE_CLAIM"},
    "tax": {"rate": 0.05, "threshold_year": 1000.0,
            "source": "Thuế TNCN đại lý bảo hiểm 5% trên doanh thu — Luật Thuế TNCN 2025 số 109/2025/QH15, Điều 7 khoản 3 (đọc qua bản tóm tắt); "
                      "ngưỡng không phải nộp 1 tỷ đồng/năm — Nghị định 68/2026/NĐ-CP sửa bởi Nghị định 141/2026/NĐ-CP (đọc qua báo chí). "
                      "Văn bản công ty: thu nhập trả là TRƯỚC thuế, công ty khấu trừ thuế trước khi trả [0048M01_2026 : 5]; người nhận chịu mọi nghĩa vụ thuế [CHH0DCEB260003V : 12]; "
                      "AIA tạm khấu trừ 10% trên phí giới thiệu [AIAVAD 2604-069 : 7-8]",
            "urls": ["https://luatvietnam.vn/thue/luat-thue-thu-nhap-ca-nhan-2025-so-109-2025-qh15-422733-d1.html",
                     "https://plo.vn/chinh-thuc-nang-nguong-doanh-thu-chiu-thue-voi-ca-nhan-ho-kinh-doanh-len-1-ti-dongnam-post906478.html"],
            "label": "SOURCE_CLAIM",
            "open_question": "Chưa đối chiếu toàn văn: 5% tính trên PHẦN VƯỢT 1 tỷ (đa số nguồn) hay trên TOÀN BỘ doanh thu khi vượt 1 tỷ → tính cả 2 cách"},
}

# ---------------- Phần 1: 6 câu hỏi cho tầng đại lý ----------------
SIX_Q = ["1. Ai được trả", "2. Trả trên cơ sở gì", "3. Tỷ lệ / bậc thang", "4. Điều kiện chất lượng", "5. Khi nào trả", "6. Khi nào mất / bị thu hồi"]
SIX = {
    "AIA": [
        "Chuyên viên (SA, UM+ và PAF+ tham gia bán cá nhân) [AIAVAD 2604-069 : 3]",
        "Hoa hồng theo biểu phí sản phẩm — KHÔNG có trong 9 văn bản (mô hình giả định 30% FYP, `ASSUMPTION`); thưởng tính trên FYC Tín chỉ quý / năm [AIAVAD 2604-069 : 5-7]",
        "Thưởng doanh số quý 8 bậc 4%–40% (FYC quý ≥16 … ≥150 tr) [AIAVAD 2604-069 : 5-6]; Ngoại hạng quý 5/10/15% [AIAVAD 2604-069 : 6]; thưởng năm 6/10/14/20% (≥150/300/800/1.600 tr) [AIAVAD 2604-069 : 7]",
        "Mọi thưởng × Tỷ lệ chi trả theo FY: 2026 ≥85% → 120% · ≥75% → 110% · ≥65% → 100% · <65% → %FY; 2027 <70% → 0% [AIAVAD 2604-069 : 3]; xét duy trì hợp đồng hằng quý [AIAVAD 2604-069 : 9-10]",
        "Sau khi hết tháng/quý/năm, trả Kỳ 1 (ngày 10–12) hoặc Kỳ 2 (28–30); thưởng năm vào kỳ 1 năm sau [AIAVAD 2604-069 : 12-13]",
        "Hợp đồng hủy trong 6 tháng: thu hồi toàn bộ hoa hồng, thưởng, phí liên quan; tính lại bậc và thu phần chênh [AIAVAD 2604-069 : 13]; chấm dứt hợp đồng do kỷ luật: không trả thưởng [AIAVAD 2604-069 : 12-14]",
    ],
    "Chubb": [
        "Đại lý kênh Đại lý (AR, AL, AMD) [CHH0DCEB260007V : 4]",
        "Hoa hồng % phí bảo hiểm theo sản phẩm và năm hợp đồng [CHH0DCEB260007V : 13-19]; thưởng tháng trên FYC tháng [CHH0DCEB260007V : 4-5]",
        "Thưởng HQKD tháng = FYC × tỷ lệ theo FYC 3 tháng (AR: 7,5% / 25% / 35% / 45% / 55% từ 5 / 10 / 20 / 40 / 60 tr) × tỷ lệ điều chỉnh [CHH0DCEB260007V : 4-5]; thưởng quý 0/15/30% theo số lượt EHC [CHH0DCEB260007V : 5-6]",
        "Tỷ lệ điều chỉnh theo K2 cá nhân: ≥80% → 120% · 70–<80% → 100% · 60–<70% → 75% · 50–<60% → 50% · <50% → 25%; chưa có K2 → 100% [CHH0DCEB260007V : 4]",
        "K2 ≥60%: tạm ứng trong kỳ trả của tháng/quý xét thưởng [CHH0DCEB260007V : 4-6]",
        "Hợp đồng phát hành trong kỳ mà bị hủy: tính lại và thu hồi thưởng [CHH0DCEB260007V : 5-6]",
    ],
    "Manulife": [
        "Đại Lý [0046M01_2026 : 1]",
        "Hoa hồng theo thông báo riêng từng sản phẩm (không có trong văn bản) [0046M01_2026 : 9]; thưởng năng suất trên FYC tháng / quý [0046M01_2026 : 4-6]",
        "Thưởng năng suất tháng 5%–50% theo FYC 3 tháng (5 … 100 tr), mỗi tháng phải có ≥1 hợp đồng thực cấp [0046M01_2026 : 4]; thưởng quý 2%–10% (gấp đôi cho Đại lý xuất sắc) [0046M01_2026 : 5-6]",
        "× Hệ số TLDTHD năm 2 (từ 04/2026): ≥70% → 100% · 65–<70% → 90% · 60–<65% → 70% · 50–<60% → 50% · <50% → TLDTHD/2 [0046M01_2026 : 1]",
        "Thưởng năm trả 50/30/20% trong 3 năm sau, mỗi lần cần TLDTHD ≥70% [0046M01_2026 : 7]; ký quỹ 5% thu nhập/tháng tới khi đủ 2 tr [0046M01_2026 : 9]",
        "Hợp đồng mất hiệu lực: thu hồi 100% hoa hồng; hủy/từ chối: thu hồi thu nhập tương ứng [0046M01_2026 : 9-10]",
    ],
    "Hybrid": [
        "Đại lý 2 đường ray: Full-time (cam kết) / Part-time (thuần biến phí) — `PROPOSAL` (hybrid_scheme.py)",
        "Hoa hồng 30% FYP năm đầu (`ASSUMPTION`, như 3 hãng trong mô hình); thưởng tháng trên FYC tháng",
        "Thưởng tháng 5 bậc 10,24% → 48,64% FYC (ngưỡng FYC 5 / 12 / 22 / 35 / 55 tr); Full-time thêm trợ cấp 3 tr/tháng (Vùng I) khi đạt quota 30 tr FYP và ≥2 hợp đồng — `PROPOSAL`",
        "Thưởng × hệ số K2 liên tục (sàn 60%); trợ cấp chỉ khi K2 ≥80%; ngưỡng giãn theo vùng (100/89/78/70%) — `PROPOSAL`",
        "Hằng tháng; phần trả chậm chỉ ở tầng quản lý và lãnh đạo — `PROPOSAL`",
        "K2 <80% mất trợ cấp tháng đó; thu hồi theo quy định chung khi hợp đồng hủy (chưa thiết kế chi tiết) — `PROPOSAL`",
    ],
}

# Tên khoản theo khóa engine → (tên hiển thị, trích dẫn)
ITEM_NAMES = {
    "AIA": {"fyc_total": ("Hoa hồng năm đầu", "ASSUMPTION 30% FYP"), "bonus_quarterly_prod": ("Thưởng doanh số quý", "[AIAVAD 2604-069 : 5-6]"),
            "bonus_quarterly_premier": ("Thưởng Ngoại hạng quý", "[AIAVAD 2604-069 : 6]"), "bonus_syc": ("Thưởng chất lượng dịch vụ quý", "[AIAVAD 2604-069 : 6]"),
            "bonus_annual": ("Thưởng doanh số năm (trả năm sau)", "[AIAVAD 2604-069 : 7]")},
    "Chubb": {"fyc_total": ("Hoa hồng năm đầu", "ASSUMPTION 30% FYP"), "bonus_hqkd_monthly": ("Thưởng HQKD tháng", "[CHH0DCEB260007V : 4-5]"),
              "bonus_hqkd_quarterly": ("Thưởng HQKD quý", "[CHH0DCEB260007V : 5-6]"), "bonus_ryc_quarterly": ("Thưởng duy trì quý (RYC)", "[CHH0DCEB260007V : 6-7]")},
    "Manulife": {"fyc_total": ("Hoa hồng năm đầu", "ASSUMPTION 30% FYP"), "bonus_monthly_productivity": ("Thưởng năng suất tháng", "[0046M01_2026 : 4]"),
                 "bonus_monthly_excellence_pro": ("Thưởng xuất sắc tháng (Manulife Pro)", "[0046M01_2026 : 4-5]"),
                 "bonus_quarterly_productivity": ("Thưởng năng suất quý", "[0046M01_2026 : 5-6]"), "bonus_mstar_quarterly": ("Thưởng M-Star quý", "[0046M01_2026 : 7-8]"),
                 "bonus_mstar_annual": ("Thưởng M-Star năm", "[0046M01_2026 : 8]"), "bonus_annual_kdxs_deferred_50_30_20": ("Thưởng KDXS năm (trả 3 năm)", "[0046M01_2026 : 6-7]")},
    "Hybrid": {"fyc_total": ("Hoa hồng năm đầu", "ASSUMPTION 30% FYP"), "bonuses": ("Thưởng tháng theo bậc × hệ số K2", "PROPOSAL"),
               "allowance_fixed": ("Trợ cấp Full-time (đạt quota)", "PROPOSAL")},
}


def agent_detail(s: str, fyp: float, base) -> dict:
    """Thu nhập năm 1 (chưa gồm tái tục) + từng khoản, cùng hàm/tham số với build_phase2.agent()."""
    from model.compensation.compensation_engine import calc_aia_cvtv_12m, calc_chubb_ar_12m, calc_manulife_agent_12m
    fyc = fyp * P.FYC_RATE
    if s == "AIA":
        r = calc_aia_cvtv_12m([fyc] * 12, [0.0] * 12, fy_pct=K2)
    elif s == "Chubb":
        r = calc_chubb_ar_12m([fyc] * 12, [0.0] * 12, [True] * 12, k2_pct=K2, tenure_months_start=13)
    elif s == "Manulife":
        r = calc_manulife_agent_12m([fyc] * 12, [fyp] * 12, [1] * 12, k2=K2)
    else:
        r = H.hybrid_agent_12m(fyp, H.FT_MIN_CC_MONTH, K2, "V1", "FULL_TIME", base)
    total = float(r["total_earned"])
    assert abs(total - P.agent(s, fyp, K2, base)["total"]) < 1e-6        # cùng số với báo cáo 02
    items = [{"name": nm, "cite": c, "year": round(float(r.get(k, 0.0)), 2)} for k, (nm, c) in ITEM_NAMES[s].items() if float(r.get(k, 0.0) or 0.0) > 0]
    return {"total": total, "cash_y1": float(r["cash_paid_y1"]), "items": items}


def tax_year(revenue: float) -> dict:
    t = BENCH["tax"]
    excess = t["rate"] * max(0.0, revenue - t["threshold_year"])                         # cách hiểu 1: chỉ phần vượt
    full = t["rate"] * revenue if revenue > t["threshold_year"] else 0.0                  # cách hiểu 2: toàn bộ khi vượt
    return {"excess_reading": round(excess, 2), "full_reading": round(full, 2)}


def compute() -> dict:
    base = H.song_hanh_params()
    d2 = P.compute()
    groups = [(nm, n, f) for nm, n, f in P.PRODUCTIVITY_MIX if f > 0]
    mw1 = BENCH["min_wage"]["values"]["Vùng I"]
    avg_all = BENCH["avg_income"]["values"]["Bình quân lao động cả nước"]
    out = {"k2": K2, "bench": BENCH, "six_questions": SIX_Q, "groups": [{"name": nm, "agents": n, "fyp_month": f} for nm, n, f in P.PRODUCTIVITY_MIX],
           "schemes": {}}
    for s in P.SCHEMES:
        det = {nm: agent_detail(s, f, base) for nm, _, f in groups}
        n_act = sum(n for _, n, _ in groups)
        mean_year = sum(n * det[nm]["total"] for nm, n, _ in groups) / n_act
        rows = []
        for nm, n, f in groups:
            y = det[nm]["total"]
            tx = tax_year(y)
            after_lo = (y - tx["full_reading"]) / 12           # sau thuế, cách hiểu bất lợi hơn
            after_hi = (y - tx["excess_reading"]) / 12
            rows.append({"group": nm, "agents": n, "fyp_month": f, "year": round(y, 2), "quarter": round(y / 4, 2), "month": round(y / 12, 2),
                         "cash_y1_share": round(det[nm]["cash_y1"] / y * 100, 1) if y else 0.0,
                         "tax_year": tx, "after_tax_month": [round(after_lo, 2), round(after_hi, 2)],
                         "vs_min_wage_v1": round(after_lo / mw1, 2), "vs_avg_income": round(after_lo / avg_all, 2)})
        median_group = "Nòng cốt"                                     # 13 / 15 / 10 người → người thứ 19–20 thuộc nhóm Nòng cốt
        traps = [t for t in d2["traps"] if t["scheme"] == s]
        roi = {(r["metric"], r["k2"]): r["value"] for r in d2["roi"] if r["scheme"] == s}
        rub = {r["pillar"]: r for r in d2["rubric"] if r["scheme"] == s}
        out["schemes"][s] = {
            "name": NAMES[s], "six": SIX[s],
            "items_group": "Nòng cốt", "items": det["Nòng cốt"]["items"], "items_total": round(det["Nòng cốt"]["total"], 2),
            "income": rows, "mean_month_active": round(mean_year / 12, 2), "median_group": median_group,
            "risks": [{"trap": t["trap"], "text": t["value_text"], "cite": t["citation"], "label": t["label"]} for t in traps],
            "company": {
                "score": d2["weighted"][s],
                "sales": rub["Thúc đẩy doanh số"]["evidence"], "sales_score": rub["Thúc đẩy doanh số"]["score"],
                "quality": rub["Chất lượng kinh doanh (hành vi)"]["evidence"], "quality_score": rub["Chất lượng kinh doanh (hành vi)"]["score"],
                "cost": rub["Hiệu quả chi phí / ROI"]["evidence"], "cost_score": rub["Hiệu quả chi phí / ROI"]["score"],
                "cost_pct_fyp": roi.get(("cost_pct_fyp", 85)), "cost_per_persisted_k65": roi.get(("cost_per_persisted_pct", 65)),
                "fixed_share": roi.get(("fixed_share", 85)),
                "legal": [g["rule"] + f": {P.vn(g['value'])}% / giới hạn {P.vn(g['limit'])}% — {'ĐẠT' if g['pass'] else 'TRƯỢT'}" for g in d2["gates"][s].values()],
                "ops": rub["Độ đơn giản & dễ tính"]["evidence"],
            },
            "label": "PROPOSAL" if s == "Hybrid" else "MODEL_OUTPUT",
            "confidentiality": "restricted" if s in P.CONF else "public",
        }
    return out


def verdict(row: dict) -> str:
    lo = row["after_tax_month"][0]
    mw = BENCH["min_wage"]["values"]
    if lo < mw["Vùng IV"]:
        return "dưới lương tối thiểu cả 4 vùng"
    if lo < mw["Vùng I"]:
        return "dưới lương tối thiểu Vùng I"
    if lo < BENCH["avg_income"]["values"]["Bình quân lao động cả nước"]:
        return "trên lương tối thiểu, dưới thu nhập bình quân lao động"
    return "trên thu nhập bình quân lao động"


def write_md(d: dict) -> str:
    vn = P.vn
    S = P.SCHEMES
    L = []
    w = L.append
    w("# Hai góc nhìn: Người bán nhận gì · Doanh nghiệp được gì")
    w("")
    w(f"Cùng một bộ câu hỏi cho mọi phương án — thêm phương án thì thêm cột, không thêm dòng. Kịch bản chuẩn: K2 {vn(d['k2'], 0)}%, năm đầu (chưa gồm tái tục), "
      f"hoa hồng 30% FYP (`ASSUMPTION`), đại lý theo 4 nhóm năng suất (`ASSUMPTION`, DEC-17): " +
      " · ".join(f"{g['agents']} ĐL «{g['name']}» {vn(g['fyp_month'], 0)} tr FYP/tháng" for g in d["groups"]) + ".")
    w("")
    w("## Phần 1 · Chính sách nói gì — 6 câu hỏi (tầng đại lý)")
    w("")
    w("| Câu hỏi | " + " | ".join(NAMES[s] for s in S) + " |")
    w("|---|" + "---|" * len(S))
    for i, q in enumerate(SIX_Q):
        w(f"| {q} | " + " | ".join(d["schemes"][s]["six"][i] for s in S) + " |")
    w("")
    w("Nguồn: bộ quy tắc đọc 2 lượt độc lập và đối chiếu ảnh trang (`qa/source-reading/rules_verified.json`).")
    w("")
    w("## Phần 2 · Người bán nhận gì")
    w("")
    w(f"### 2.1 Một năm nhận những khoản gì (đại lý «Nòng cốt», 20 tr FYP/tháng)")
    w("")
    for s in S:
        x = d["schemes"][s]
        w(f"- **{NAMES[s]}** — tổng {vn(x['items_total'])} tr/năm: " + "; ".join(f"{it['name']} {vn(it['year'])} tr ({it['cite']})" for it in x["items"]))
    w("")
    w("### 2.2 Thấp / giữa / cao — năm, quý, tháng, sau thuế")
    w("")
    w("| Phương án | Nhóm | FYP/tháng | Năm | Quý | Tháng | Sau thuế/tháng | So lương tối thiểu Vùng I | So thu nhập bình quân lao động | Kết luận |")
    w("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for s in S:
        for r in d["schemes"][s]["income"]:
            lo, hi = r["after_tax_month"]
            at = vn(lo) if abs(hi - lo) < 0.005 else f"{vn(lo)}–{vn(hi)}"
            w(f"| {NAMES[s]} | {r['group']} | {vn(r['fyp_month'], 0)} | {vn(r['year'])} | {vn(r['quarter'])} | {vn(r['month'])} | {at} | "
              f"{vn(r['vs_min_wage_v1'], 2)}× | {vn(r['vs_avg_income'], 2)}× | {verdict(r)} |")
    w("")
    w("Bình quân đại lý có hoạt động (bị nhóm Top kéo lên): " + " · ".join(f"{NAMES[s]} {vn(d['schemes'][s]['mean_month_active'])} tr/tháng" for s in S) +
      ". Người ở **giữa** (trung vị) thuộc nhóm «Nòng cốt» — đọc dòng đó để biết \"đa số nhận bao nhiêu\".")
    w("")
    t = d["bench"]["tax"]
    w(f"**Thuế** (`SOURCE_CLAIM`): {t['source']}. {t['open_question']}. Không nhóm nào vượt 1 tỷ/năm nên **cả 2 cách đều ra thuế 0** — kết luận không phụ thuộc chỗ chưa chắc. "
      "Lưu ý dòng tiền: công ty có thể **tạm khấu trừ** hằng tháng rồi hoàn khi quyết toán.")
    w("")
    w(f"**Mốc so sánh** (`SOURCE_CLAIM`): {d['bench']['min_wage']['source']}: " + " · ".join(f"{k} {vn(v, 2)}" for k, v in d["bench"]["min_wage"]["values"].items()) +
      f" tr/tháng. {d['bench']['avg_income']['source']}: " + " · ".join(f"{k} {vn(v)}" for k, v in d['bench']['avg_income']['values'].items()) + " tr/tháng.")
    w("")
    w("**Chưa biết (`UNKNOWN`, không tự điền):** chi phí tự chi của đại lý (đi lại, điện thoại, chăm khách); bảo hiểm xã hội của đại lý; số tháng thấp nhất trong năm (cần dữ liệu hằng tháng thật).")
    w("")
    w("### 2.3 Rủi ro mất tiền")
    w("")
    for s in S:
        rs = d["schemes"][s]["risks"]
        if rs:
            w(f"- **{NAMES[s]}:** " + "; ".join(f"{r['trap']} — {r['text']}" for r in rs))
    w("")
    w("## Phần 3 · Doanh nghiệp được gì")
    w("")
    w("| Câu hỏi | " + " | ".join(NAMES[s] for s in S) + " |")
    w("|---|" + "---|" * len(S))
    C = {s: d["schemes"][s]["company"] for s in S}
    w("| Điểm tổng (rubric DEC-19) | " + " | ".join(f"**{vn(C[s]['score'], 2)}**" for s in S) + " |")
    w("| Doanh số (điểm) | " + " | ".join(f"{vn(C[s]['sales_score'], 2)} — {C[s]['sales']}" for s in S) + " |")
    w("| Chất lượng (điểm) | " + " | ".join(f"{vn(C[s]['quality_score'], 2)} — {C[s]['quality']}" for s in S) + " |")
    w("| Chi phí / ROI (điểm) | " + " | ".join(f"{vn(C[s]['cost_score'], 2)} — {C[s]['cost']}" for s in S) + " |")
    w("| Chi phí / phí còn duy trì khi K2 65% | " + " | ".join(f"{vn(C[s]['cost_per_persisted_k65'])}%" for s in S) + " |")
    w("| Tỷ trọng cố định | " + " | ".join(f"{vn(C[s]['fixed_share'])}%" for s in S) + " |")
    w("| Pháp lý (cổng) | " + " | ".join("<br>".join(C[s]["legal"]) for s in S) + " |")
    w("| Vận hành | " + " | ".join(C[s]["ops"] for s in S) + " |")
    w("")
    w("ROI ở đây là chỉ số thay thế (chi phí / FYP, chi phí / phí còn duy trì) — ROI thật cần biên lợi nhuận sản phẩm (VNB) từ Actuarial (`UNKNOWN`).")
    w("")
    w("## Đọc nhanh")
    w("")
    low = [s for s in S if verdict(d["schemes"][s]["income"][0]).startswith("dưới lương tối thiểu")]
    mid_under = [s for s in S if d["schemes"][s]["income"][1]["after_tax_month"][0] < BENCH["avg_income"]["values"]["Bình quân lao động cả nước"]]
    w(f"- Đại lý năng suất thấp (10 tr FYP/tháng) nhận **dưới lương tối thiểu Vùng I** ở {len(low)}/4 phương án — không phương án nào giải được bài toán này bằng hoa hồng; "
      "đây là lý do tỷ lệ rời bỏ đại lý mới cao và cũng là lý do Đề xuất có trợ cấp Full-time gắn quota.")
    w(f"- Đại lý «Nòng cốt» (giữa) nhận dưới thu nhập bình quân lao động ở {len(mid_under)}/4 phương án.")
    w("- Doanh nghiệp: xem Phần 3 — Đề xuất mạnh ở chất lượng và độ đơn giản, yếu nhất ở động lực bán thêm, chi phí cao hơn Manulife và AIA.")
    w("")
    w("Nhãn: `VERIFIED FACT` (văn bản gốc có trang) · `MODEL_OUTPUT` (tính từ quy tắc + giả định) · `ASSUMPTION` · `PROPOSAL` · `SOURCE_CLAIM` (nguồn ngoài chưa đối chiếu toàn văn) · `UNKNOWN`.")
    return "\n".join(L) + "\n"


def public_view(d: dict) -> dict:
    """Bản công khai: bỏ Manulife (số đại lý tính từ 0046M01 — văn bản ghi 'thông tin mật', DEC-14)."""
    x = json.loads(json.dumps(d))
    x["schemes"] = {s: v for s, v in x["schemes"].items() if v["confidentiality"] == "public"}
    return x


def main() -> int:
    d = compute()
    OUT_MD.write_text(write_md(d), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT_MD.relative_to(REPO)} and {OUT_JSON.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
