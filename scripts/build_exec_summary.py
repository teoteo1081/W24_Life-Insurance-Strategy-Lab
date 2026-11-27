"""Tóm tắt nhanh — 2 góc nhìn (Đại lý/Quản lý · Công ty). CHỈ tổng hợp số engine đã có trong web/data/snapshot.json —
KHÔNG tính lại công thức nào. Một nguồn cho cả file Markdown và khối trên trang web (scripts/build_html.py gọi build()).

Quy ước số:
- Góc nhìn đại lý: thu nhập NĂM từ engine (đã gồm thưởng quý, thưởng năm, M-Star, MDRT nếu chính sách có); Tháng = Năm / 12,
  Quý = Năm / 4 (bình quân quy đổi, không phải dòng tiền từng tháng). Mốc 1 = thu nhập cá nhân gồm tái tục (giả định A7);
  Mốc 2–4 = phí quản lý thuần (không gồm tự bán) — cùng cơ sở Trang 1. Chính sách Lai: Vùng I, đại lý Full-time.
- Góc nhìn công ty: khu vực Mốc 4 (45 đại lý, 1,2 tỷ FYP/tháng = 14,4 tỷ/năm), K2 85%. Tổng chi = tổng chi/FYP × FYP năm.

Dùng:  python scripts/build_exec_summary.py [--full-out <đường dẫn ngoài repo>]
File trong repo KHÔNG chứa dòng `restricted` (DEC-14); --full-out ghi bản đủ số Manulife ra nơi khác.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs" / "interview" / "00_Executive_Summary_Keo_Thom.md"
SNAP = REPO / "web" / "data" / "snapshot.json"
ORG_FYP_Y = 1200.0 * 12          # Mốc 4: 1,2 tỷ FYP/tháng (knowledge/policies/scale-milestones.json)
TIERS = [("M1", "L1 · Cá nhân 30tr FYP/tháng"), ("M2", "L2 · Nhóm 150tr (5 ĐL)"), ("M3", "L3 · Ban 450tr (15 ĐL)"), ("M4", "L4 · Khu vực 1,2 tỷ (45 ĐL)")]
CO = ["AIA", "Chubb", "Manulife", "Hybrid"]
NAME = {"AIA": "AIA Alpha", "Chubb": "Chubb Life", "Manulife": "Manulife", "Hybrid": "Chính sách Lai (đề xuất)"}
HYB_ROW = {"M1": ("FULL_TIME", "Đại lý Full-time"), "M2": ("MANAGER", "Trưởng nhóm"), "M3": ("MANAGER", "Trưởng ban"), "M4": ("LEADER", "Lãnh đạo khu vực")}

# Nhận xét cơ chế (JUDGEMENT) cho các văn bản KHÔNG mật; Manulife tầng 1–3 lấy câu từ dòng dữ liệu mật (behavior_traps) nên tự lọc ở bản công khai.
MECH = {
    ("M1", "AIA"): ("Ăn tiền nhất: thưởng quý/5 Sao/năm và +50% thưởng tái tục [AIAVAD 2604-069 : 3-7]",
                    "Dễ bị cắt: hệ số FY — dưới 70% về 0 từ 2027 (vách đá)"),
    ("M1", "Chubb"): ("Ăn tiền nhất: thưởng tháng–quý vào sớm, đỉnh ~86% FYC [CHH0DCEB260007V : 4-7]",
                      "Dễ bị cắt: giữ T+1 khi mới / K2 thấp; phí âm khi hợp đồng bị hủy"),
    ("M1", "Hybrid"): ("Ăn tiền nhất: trợ cấp 3tr/tháng khi đạt quota 30tr + thưởng tháng 5 bậc (PROPOSAL)",
                       "Dễ bị cắt: K2 80→79% hoặc thiếu 0,1tr quota là mất trọn trợ cấp"),
    ("M2", "AIA"): ("Ăn tiền nhất: thưởng tuyển mới & nhân bản UM [AIAVAD 2601-034 : 4-5]", "Dễ bị cắt: không tuyển người mới"),
    ("M2", "Chubb"): ("Ăn tiền nhất: override trực tiếp cao, trả ngay [CHH0DCEB260008V : 5-7]",
                      "Dễ bị cắt: phí gián tiếp về 0 nếu nhóm trực tiếp <15tr FYC; phí âm khi hủy HĐ"),
    ("M2", "Hybrid"): ("Ăn tiền nhất: override 35,7% × K2 (trần 42,8%) trên FYC nhóm (PROPOSAL)", "Dễ bị cắt: vách đá K2 80→79%"),
    ("M3", "AIA"): ("Ăn tiền nhất: để đội phẳng (mọi người báo cáo trực tiếp)", "Dễ bị cắt: phát triển quản lý con làm thu nhập giảm"),
    ("M3", "Chubb"): ("Ăn tiền nhất: override trực tiếp + gián tiếp L1–L3", "Dễ bị cắt: cổng 15tr FYC của nhóm trực tiếp"),
    ("M3", "Hybrid"): ("Ăn tiền nhất: override trực tiếp + gián tiếp 2 đời (PROPOSAL)", "Dễ bị cắt: cổng FYC nhóm ≥15tr × hệ số vùng; K2 <75% mất trả chậm"),
    ("M4", "AIA"): ("Ăn tiền nhất: phí cố định 20–130tr/tháng + chuỗi gián tiếp nhiều tầng [AIAVAD 2601-035 : 2-5]", "Dễ bị cắt: chỉ tiêu 5 năm"),
    ("M4", "Chubb"): ("Ăn tiền nhất: tăng trưởng quý 2,5–27,5% FYC + tái tục [CHH0DCEB260003V : 5-10]",
                      "Dễ bị cắt: vách đá K2 50→60% (Q3/2026); bắt buộc biên bản nghiệm thu"),
    ("M4", "Manulife"): ("Ăn tiền nhất: phí cơ bản 35tr × % đạt chỉ tiêu (sàn 30%, trần 150%) [0048M01_2026 : 1]",
                         "Dễ bị cắt: phần trả chậm 3 năm cần K2 ≥70%"),
    ("M4", "Hybrid"): ("Ăn tiền nhất: phí cơ bản × % đạt chỉ tiêu (sàn 30%, trần 140%) + override vùng (PROPOSAL)",
                       "Dễ bị cắt: 70% override trả chậm, mất nếu K2 <75%"),
}
COMPANY = {
    "AIA": "Rẻ ở K2 tốt nhưng CHƯA gồm gói Exchange/Pro (UNKNOWN); bán nghiêng bảo vệ thuần thì vọt lên nhiều nhất.",
    "Chubb": "Đắt nhất, trả ngay gần như toàn bộ, không giữ lại trả chậm — rủi ro dòng tiền khi chất lượng xấu.",
    "Manulife": "Rẻ nhất ở K2 tốt nhưng chi phí gần như không co khi chất lượng xấu; quản lý nhận ít hơn tự bán.",
    "Hybrid": "Ngang thị trường ở K2 tốt, co mạnh nhất khi K2 xấu, giữ lại nhiều trả chậm nhất; đỉnh bị trần quỹ 75% chặn.",
}


def fin(x):
    if not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"non-finite {x!r}")
    return float(x)


def vn(x, d=1):
    return f"{fin(x):,.{d}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def build(tables: dict) -> dict:
    """Trả {"agent": [...], "company": [...]}; mỗi dòng mang `confidentiality` để bản công khai lọc được."""
    B, RG, R, TR = (tables.get(k, []) for k in ("benchmark_results", "hybrid_regional", "roi_analysis", "behavior_traps"))
    roi = {(r["scheme"], r["metric"], int(r["k2"])): r for r in R}
    trap = {(t["scheme"], t["trap"]): t for t in TR}
    agent = []
    for mid, tier in TIERS:
        for co in CO:
            if co == "Hybrid":
                track, role = HYB_ROW[mid]
                r = next((x for x in RG if x["region"] == "V1" and x["track"] == track and x["milestone_id"] == mid and x["basis"] == "national_fyp"), None)
                title, conf, label = role, "public", "PROPOSAL"
            else:
                r = next((x for x in B if x["milestone_id"] == mid and x["company"] == co and x["comparison"] == "primary"), None)
                title, conf, label = (r or {}).get("title", ""), (r or {}).get("confidentiality", "public"), (r or {}).get("label", "MODEL_OUTPUT")
            if r is None or r.get("income_vnd_m_month") is None:
                continue                                    # dòng mật đã bị lọc, hoặc UNKNOWN — không ép về 0
            m = fin(r["income_vnd_m_month"])
            good, bad = MECH.get((mid, co), ("", ""))
            if co == "Manulife" and mid != "M4":            # chỉ có ở bản đủ (dòng restricted)
                t = trap.get(("Manulife", "Tự bán vs quản lý thuần")) if mid == "M2" else trap.get(("Manulife", "Bẫy giữ đội phẳng")) if mid == "M3" else None
                good = "Ăn tiền nhất: thưởng tháng theo FYC 3 tháng + thưởng quý, M-Star" if mid == "M1" else (t["value_text"] if t else "")
                bad = "Dễ bị cắt: mọi thưởng × hệ số duy trì HĐ (dưới 50% chia đôi) × hệ số kỷ luật"
            if mid == "M2" and co in ("AIA", "Chubb", "Hybrid") and (co, "Tự bán vs quản lý thuần") in trap:
                good = good + " · " + trap[(co, "Tự bán vs quản lý thuần")]["value_text"].split("→")[-1].strip()
            if mid == "M3" and co in ("AIA", "Chubb", "Hybrid") and (co, "Bẫy giữ đội phẳng") in trap:
                bad = bad + f" (đội phẳng trả gấp {vn(trap[(co, 'Bẫy giữ đội phẳng')]['metric_value'], 2)}× đội có quản lý con)"
            # Quy tắc nhận định (công bố ở đầu bảng): so với mức THẤP NHẤT của các hãng cùng tầng có trong dữ liệu
            lo = min(fin(x["income_vnd_m_month"]) for x in B if x["milestone_id"] == mid and x.get("income_vnd_m_month") is not None and x["comparison"] == "primary")
            verdict = "Thơm" if m >= 1.2 * lo else ("Thấp hơn cả các hãng" if m < lo else "Trung bình")
            st = trap.get((co, "Tự bán vs quản lý thuần"))
            if mid == "M2" and st and fin(st["metric_value"]) < 0:   # lên quản lý nhóm thu ít hơn tự bán
                verdict = "Không thơm (quản lý thu ít hơn tự bán)"
            agent.append({"tier": tier, "milestone_id": mid, "scheme": co, "name": NAME[co], "title": title, "month": round(m, 1),
                          "quarter": round(m * 3, 1), "year": round(m * 12, 1), "verdict": verdict,
                          "comment": f"{good}. {bad}.".replace("..", "."), "label": label, "confidentiality": conf})
    company = []
    for co in CO:
        c85 = roi.get((co, "cost_pct_fyp", 85))
        if c85 is None:
            continue                                        # Manulife bị lọc ở bản công khai
        wc, w40, drop, dfr = (roi.get((co, k, kk)) for k, kk in (("cost_pct_fyp_worst_case", 85), ("cost_pct_fyp_worst_fyc40", 85),
                                                                  ("payout_drop_k2_85_to_65", 0), ("deferred_share", 85)))
        y = fin(c85["value"]) / 100 * ORG_FYP_Y
        peak = max((x for x in (wc, w40) if x), key=lambda x: x["value"])
        company.append({"scheme": co, "name": NAME[co], "month": round(y / 12, 1), "quarter": round(y / 4, 1), "year": round(y, 1),
                        "cost_pct": fin(c85["value"]), "worst_pct": fin(wc["value"]) if wc else None, "worst_fyc40_pct": fin(w40["value"]) if w40 else None,
                        "peak_pct": fin(peak["value"]), "peak_note": peak.get("note", ""), "drop_pct": fin(drop["value"]) if drop else None,
                        "deferred_pct": fin(dfr["value"]) if dfr else None, "comment": COMPANY[co], "label": c85["label"],
                        "confidentiality": c85.get("confidentiality", "public")})
    return {"agent": agent, "company": company}


def to_markdown(es: dict, full: bool) -> str:
    L = ["# Tóm tắt nhanh — 2 góc nhìn (Executive Summary · “Kèo thơm hay không?”)", ""]
    L.append("> Tổng hợp số engine hiện có (`web/data/snapshot.json`), **không tính lại công thức**. Số 3 hãng = `MODEL_OUTPUT`, Chính sách Lai = `PROPOSAL`; "
             "nhận xét = `JUDGEMENT`. Mô hình: K2 85%, hoa hồng năm đầu 30% FYP, trước thuế, triệu đồng."
             + ("" if full else " **Bản này đã lược Manulife tầng 1–3** (2 văn bản ghi \"thông tin mật\", DEC-14)."))
    L += ["", "## Bảng 1 — Góc nhìn Đại lý / Quản lý", "",
          "Tháng = thu nhập năm / 12, Quý = năm / 4 (bình quân quy đổi, **đã gồm** thưởng quý, thưởng năm, M-Star, MDRT nếu có — không phải dòng tiền từng tháng). "
          "L1 = thu nhập cá nhân gồm tái tục; L2–L4 = phí quản lý thuần (không gồm tự bán). Chính sách Lai: Vùng I, đại lý Full-time. "
          "**Kèo thơm?** = so với mức thấp nhất của các hãng cùng tầng: ≥ 1,2 lần → *Thơm*; thấp hơn → *Thấp hơn cả các hãng*; còn lại *Trung bình*; "
          "ở L2, nếu lên quản lý nhóm mà thu ít hơn tự bán → *Không thơm*.", "",
          "| Tầng | Hãng · chức danh | Tháng | Quý | Năm | Kèo thơm? | Nhận xét |", "|---|---|---:|---:|---:|---|---|"]
    for r in es["agent"]:
        L.append(f"| {r['tier']} | {r['name']} · {r['title']} | {vn(r['month'])} | {vn(r['quarter'])} | {vn(r['year'], 0)} | {r['verdict']} | {r['comment']} |")
    L += ["", "## Bảng 2 — Góc nhìn Công ty (khu vực Mốc 4: 45 đại lý, 1,2 tỷ FYP/tháng)", "",
          "| Chính sách | Tổng chi / tháng | / quý | / năm | Tổng chi / FYP | Đỉnh stress test | Chi trả giảm khi K2 85%→65% | Trả chậm | Nhận xét cho Ban Giám đốc |",
          "|---|---:|---:|---:|---:|---|---:|---:|---|"]
    for r in es["company"]:
        L.append(f"| {r['name']} | {vn(r['month'])} | {vn(r['quarter'])} | {vn(r['year'], 0)} | {vn(r['cost_pct'])}% | {vn(r['peak_pct'])}% — {r['peak_note']} | "
                 f"{vn(r['drop_pct'])}% | {vn(r['deferred_pct'])}% | {r['comment']} |")
    L += ["", "**Đọc nhanh:** “đỉnh stress test” là chi phí cao nhất trong các kịch bản đã chạy (mọi đại lý đạt quota, lưới điểm gãy, hoặc bán nghiêng bảo vệ thuần — hoa hồng 40%). "
          "Tổng chi / FYP là chi phí mô phỏng của quỹ thu nhập cây đại lý, **không phải ROI thực tế** (thiếu biên lợi nhuận VNB, chi phí vận hành của công ty).", ""]
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full-out", help="ghi thêm bản đủ số (gồm dòng restricted) ra đường dẫn này — đặt NGOÀI repo")
    a = ap.parse_args(argv)
    tables = json.loads(SNAP.read_text(encoding="utf-8"))["tables"]
    public = {k: [r for r in v if r.get("confidentiality") != "restricted"] for k, v in tables.items()}
    OUT.write_text(to_markdown(build(public), full=False), encoding="utf-8")
    msg = f"wrote {OUT.relative_to(REPO)}"
    if a.full_out:
        p = Path(a.full_out).resolve()
        if REPO in p.parents:
            raise SystemExit("--full-out phải nằm NGOÀI repo (bản đủ có số mật — DEC-14)")
        p.write_text(to_markdown(build(tables), full=True), encoding="utf-8")
        msg += " + full copy outside repo"
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
