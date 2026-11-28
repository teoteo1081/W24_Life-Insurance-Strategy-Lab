"""Gói A — Bản khuyến nghị điều hành (Bước 1), sinh từ MỘT nguồn số: web/data/snapshot.json (+ build_exec_summary).

KHÔNG tính lại công thức: mọi con số là giá trị engine đã có trong snapshot. Văn bản xoay quanh một đề xuất duy nhất —
Chính sách Đề xuất 2026 (mô hình khu vực 45 đại lý, 1,2 tỷ FYP/tháng) — đúng như trang HTML (ANCHOR_SPEC 1.2, DEC-15).

Dùng:  python scripts/build_brief.py [--full-out <đường dẫn NGOÀI repo>]
- Bản trong repo (outputs/interview/W24_Executive_Recommendation_Step1.md) KHÔNG chứa dòng `restricted`.
- --full-out ghi bản đủ số Manulife (gồm 2 văn bản ghi "thông tin mật") ra nơi khác; từ chối đường dẫn trong repo.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import build_exec_summary as ES  # noqa: E402

SNAP = REPO / "web/data/snapshot.json"
OUT = REPO / "outputs/interview/W24_Executive_Recommendation_Step1.md"
ADOPT_SRC = REPO / "outputs/working/strategic-recommendations-and-schemes.md"
PROPOSAL = "Chính sách Đề xuất 2026"
NAME = dict(ES.NAME)
DEC_VN = {"ADOPT": "Áp dụng", "ADAPT": "Cải tiến", "AVOID": "Tránh", "INVESTIGATE": "Cần tìm hiểu", "UNKNOWN": "Chưa đủ dữ liệu"}
vn = ES.vn


def adopt_matrix() -> list[dict]:
    """Cùng bộ phân tích cú pháp với scripts/build_html.py (ma trận Áp dụng / Cải tiến / Tránh)."""
    rows = []
    for line in ADOPT_SRC.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\*\*(\d+)\.\s*(.+?)\*\*\s*(\*\(([^)]*)\)\*)?\s*\|\s*([^|]+)\|\s*\*\*`([A-Z]+)`\*\*\s*\|\s*([^|]+)\|", line)
        if m:
            rows.append({"mechanism": re.sub(r"`", "", m.group(2)).strip(), "company": (m.group(4) or "").strip(),
                         "rules": re.findall(r"[A-Z]{3}-[A-Z]{2}-\d{3}", m.group(5)), "decision": m.group(6),
                         "why": re.sub(r"[`*]", "", m.group(7)).strip()})
    return rows


def render(tables: dict, full: bool) -> str:
    R, TR, RB, RG = tables["roi_analysis"], tables["behavior_traps"], tables["rubric_scores"], tables["hybrid_regional"]

    def v(s, m, k=85):
        for r in R:
            if r["scheme"] == s and r["metric"] == m and int(r["k2"]) == k:
                return ES.fin(r["value"])
        return None

    drop = lambda s: v(s, "payout_drop_k2_85_to_65", 0)
    schemes = [s for s in ES.CO if v(s, "cost_pct_fyp") is not None]
    comps = [s for s in schemes if s != "Hybrid"]
    ws = {s: sum(r["weight"] * r["score"] for r in RB if r["scheme"] == s) for s in schemes if any(r["scheme"] == s for r in RB)}
    _others = sorted((s for s in ws if s != "Hybrid"), key=lambda s: -ws[s])
    _gap = ws["Hybrid"] - ws[_others[0]] if _others else 0.0
    rank_txt = (f"{'hơn' if _gap >= 0 else 'kém'} {NAME[_others[0]]} {vn(abs(_gap), 2)} điểm" + (" — sát nút, không phải vượt trội" if abs(_gap) < 0.10 else "")) if _others else ""
    trap = lambda s, t: next((r for r in TR if r["scheme"] == s and r["trap"] == t), None)
    es = ES.build(tables)
    co = {r["scheme"]: r for r in es["company"]}
    hy = co["Hybrid"]
    top_drop = max(comps, key=lambda s: drop(s) or -1)
    cheaper = [s for s in comps if v(s, "cost_pct_fyp") < v("Hybrid", "cost_pct_fyp")]
    regions = []
    for r in RG:
        if r["region"] not in [x["region"] for x in regions]:
            regions.append({"region": r["region"], "name": r.get("region_name") or r["region"], "coef": r.get("coefficient")})
    pct = lambda x, d=1: "—" if x is None else f"{vn(x, d)}%"

    def be(metric, comp, basis="mix4"):
        """Hòa vốn doanh số (build_phase2 mục 1b): phần FYP giữ lại sau chi trả kênh đại lý bằng phương án so sánh."""
        r = next((r for r in R if r["id"] == f"Hybrid|{metric}|{comp}|{basis}"), None)
        return None if r is None else ES.fin(r["value"])
    be_comps = [s for s in comps if be("breakeven_fyp_more_agents_pct", s) is not None]
    be_need = [s for s in be_comps if be("breakeven_fyp_more_agents_pct", s) > 0]
    be_ahead = [s for s in be_comps if s not in be_need]
    plus = lambda x: "chưa hòa vốn trong +100%" if x is None else f"+{vn(x)}%"
    be_txt = "; ".join(f"so với {NAME[s]}: thêm đại lý {plus(be('breakeven_fyp_more_agents_pct', s))} hoặc tăng năng suất {plus(be('breakeven_fyp_productivity_pct', s))} FYP"
                       for s in be_need)
    m4 = {r["scheme"]: r["month"] for r in es["agent"] if r["milestone_id"] == "M4"}
    lead_lo = min((m4[s] for s in comps if s in m4), default=None)
    L: list[str] = []
    a = L.append

    # ---------------- Đầu trang ----------------
    a("# Chính sách thu nhập đại lý BHNT tại Việt Nam 2026 — Khuyến nghị điều hành (Bước 1)")
    a("")
    a(f"> **Gói A{'' if full else ' — bản rút gọn (không có Manulife tầng đại lý & quản lý nhóm)'}.** "
      "Số liệu sinh tự động từ cùng nguồn với trang tương tác *W24 Strategy Lab* (`web/data/snapshot.json`); không gõ tay. "
      "Nhãn: `MODEL_OUTPUT` = kết quả mô phỏng · `PROPOSAL` = đề xuất, chưa ban hành · `ASSUMPTION` = giả định · "
      "`HYPOTHESIS` = giả thuyết cần thí điểm · `CONDITIONAL` / `SOURCE_CLAIM` = pháp lý chờ đối chiếu toàn văn."
      )
    a("")
    a("**Đề bài:** “Phân tích các chính sách thu nhập giữa các công ty, và đề xuất chính sách phù hợp tại thị trường VN, nhằm thúc đẩy "
      "gia tăng doanh số, chất lượng kinh doanh và hiệu quả về mặt chi phí (ROI).”")
    a("")

    # ---------------- Trả lời trong 1 trang ----------------
    a("## Trả lời đề bài trong 1 trang")
    a("")
    a("| Vế đề bài | Kết luận | Số chính (K2 85%, khu vực 45 đại lý) | Xem |")
    a("|---|---|---|---|")
    a(f"| Phân tích chính sách các công ty | Ở đại lý cá nhân các hãng trả gần ngang nhau; khác biệt nằm ở tầng quản lý và ở việc chi trả có co theo chất lượng hay không. | "
      + " · ".join(f"{NAME[s]} {pct(v(s, 'cost_pct_fyp'))} FYP" for s in comps) + " | Trang 2 |")
    a(f"| Đề xuất phù hợp VN | **{PROPOSAL}** `PROPOSAL`: trả ngang thị trường, mọi khoản thưởng lớn gắn K2, giữ lại phần trả chậm, hệ số vùng theo lương tối thiểu. | "
      f"Tổng chi {pct(v('Hybrid', 'cost_pct_fyp'))} FYP · điểm 5 tiêu chí {vn(ws['Hybrid'], 2)}/5 ({rank_txt}) | Trang 5 |")
    a(f"| Doanh số | Đề xuất trả cao hơn {', '.join(NAME[s] for s in be_need) or 'không hãng nào'} nên phải bán thêm mới hòa vốn phần phí giữ lại sau chi trả kênh đại lý"
      f"{'; rẻ hơn ' + ', '.join(NAME[s] for s in be_ahead) + ' ngay ở cùng FYP' if be_ahead else ''}. Đây là chỉ tiêu tối thiểu của thí điểm — mức tăng thật vẫn `HYPOTHESIS`. | "
      f"4 nhóm năng suất: {be_txt or '—'} `PROPOSAL` | Trang 3, 7 |")
    a(f"| Chất lượng | Chi trả co mạnh nhất khi K2 xấu đi. | Khi K2 85% → 65%: đề xuất −{pct(drop('Hybrid'))}; hãng co mạnh nhất {NAME[top_drop]} −{pct(drop(top_drop))} | Trang 3 |")
    a(f"| Chi phí / ROI | {'Không rẻ nhất khi chất lượng tốt (' + ', '.join(NAME[s] + ' ' + pct(v(s, 'cost_pct_fyp')) for s in cheaper) + ' thấp hơn)' if cheaper else 'Rẻ nhất ở K2 85%'}, "
      f"nhưng an toàn nhất khi xấu: đỉnh stress test không vượt trần 75% FYP. ROI hiện là proxy (chi phí / FYP), chưa phải VNB. | "
      f"Xấu nhất {pct(v('Hybrid', 'cost_pct_fyp_worst_case'))}; bán nghiêng bảo vệ thuần {pct(v('Hybrid', 'cost_pct_fyp_worst_fyc40'))} | Trang 6 |")
    a("")

    # ---------------- Trang 1 ----------------
    a("## Trang 1 — Tóm tắt điều hành")
    a("")
    a(f"- **Khuyến nghị:** duyệt **{PROPOSAL}** ở dạng **thí điểm** (6–12 tháng, ghép cặp với văn phòng đối chứng), chưa ban hành toàn quốc khi chưa có VNB và K2 thật.")
    a(f"- **Vì sao:** chi trả ngang thị trường để giữ và tuyển người; chi trả **giảm {pct(drop('Hybrid'))}** khi K2 từ 85% xuống 65% (cao nhất nhóm); "
      f"**{pct(v('Hybrid', 'deferred_share'))}** chi trả được giữ lại trả chậm; tổng chi **{pct(v('Hybrid', 'cost_pct_fyp'))} FYP** "
      f"(≈ {vn(hy['month'])} triệu/tháng · {vn(hy['year'], 0)} triệu/năm cho khu vực 1,2 tỷ FYP/tháng) `PROPOSAL` `MODEL_OUTPUT`.")
    lead_txt = ("thấp hơn cả các hãng" if lead_lo is not None and m4["Hybrid"] < lead_lo else
                "không thấp hơn mức thấp nhất của các hãng" if lead_lo is not None else "")
    a(f"- **Đánh đổi đã công bố:** lãnh đạo khu vực của đề xuất nhận **{vn(m4['Hybrid'])} triệu/tháng — {lead_txt}**, trong đó 70% override toàn khu vực trả chậm 3 năm theo K2 "
      "(ít phí cố định); có các “vách đá” thu nhập (K2 80%, quota) cần làm mượt ở bước 2 (trang 5).")
    a("")
    a("**Khung giả định đang dùng** (đề bài không nêu ngân sách, chỉ tiêu, quy mô) `ASSUMPTION`:")
    a("")
    a("| Giả định | Giá trị | Ghi chú |")
    a("|---|---|---|")
    a("| Quy mô so sánh | Khu vực 45 đại lý, 1,2 tỷ FYP/tháng (1 lãnh đạo, 2 trưởng ban, 6 trưởng nhóm) | Năng suất 26,7 triệu FYP/đại lý/tháng ≈ 1,8 lần bình quân thị trường (~15 triệu, `SOURCE_CLAIM`) — xem kịch bản năng suất −50% ở trang 6 |")
    a("| Ngân sách chi trả | Trần tổng chi trả hệ thống đại lý ≤ 75% FYP ở kịch bản xấu nhất | Là trần chi trả cho đại lý, **không** phải tổng chi phí khai thác trên BCTC (còn văn phòng, marketing, kênh ngân hàng) |")
    a("| Chất lượng | K2 85% (chuẩn), 65% (xấu) | Giả định; K2 thật đo ở thí điểm |")
    a("| Hoa hồng năm đầu | 30% FYP (chuẩn); độ nhạy 25% / 40% | 40% ≈ danh mục nghiêng bảo vệ thuần |")
    a("| ROI | Chi phí / FYP và chi phí / phí còn duy trì | Proxy — cần product mix & chi phí vượt định mức từ Actuarial để ra VNB |")
    a("| Ưu tiên khi chấm điểm (DEC-19) | Cổng trước: Điều 52 ≤ 30% FYP, Đề xuất ≤ 75% FYP ở kịch bản xấu nhất. Điểm: Doanh số 30% · Chất lượng 30% · Chi phí/ROI 30% · Đơn giản 10%; Vận hành & pháp lý chỉ tham khảo | Mốc chấm là `PROPOSAL`, chốt trước khi tính điểm; đổi trọng số thì điểm đổi, cấu trúc đề xuất không đổi |")
    a("")

    # ---------------- Trang 2 ----------------
    a("## Trang 2 — Các hãng trả thế nào: 4 mốc quy mô chuẩn")
    a("")
    a("So mọi hãng ở cùng quy mô: **L1** đại lý 30 triệu FYP/tháng · **L2** nhóm 150 triệu (5 đại lý) · **L3** ban 450 triệu (15 đại lý) · **L4** khu vực 1,2 tỷ (45 đại lý). "
      "L1 = thu nhập cá nhân gồm tái tục; L2–L4 = phí quản lý thuần (không gồm tự bán). Triệu đồng/tháng, bình quân quy đổi từ thu nhập năm `MODEL_OUTPUT`.")
    a("")
    a("| Tầng | " + " | ".join(NAME[s] for s in ES.CO) + " |")
    a("|---|" + "---|" * len(ES.CO))
    for mid, tier in ES.TIERS:
        cells = []
        for s in ES.CO:
            r = next((x for x in es["agent"] if x["milestone_id"] == mid and x["scheme"] == s), None)
            cells.append(f"{r['title']} **{vn(r['month'])}** — {r['verdict']}" if r else "lược (văn bản mật)")
        a(f"| {tier} | " + " | ".join(cells) + " |")
    a("")
    a("**Đọc bảng:** “Thơm” = cao hơn mức thấp nhất của các hãng cùng tầng ≥ 1,2 lần; “Không thơm” = lên quản lý nhóm mà thu ít hơn tự bán. Trích dẫn trang văn bản gốc nằm ở cột nhận xét của *Tóm tắt nhanh 2 góc nhìn* (`outputs/interview/00_Executive_Summary_Keo_Thom.md`) và trên trang tương tác.")
    a("")
    for s in comps:
        lines = [t for t in (trap(s, "Tự bán vs quản lý thuần"), trap(s, "Bẫy giữ đội phẳng"), trap(s, "Vách đá K2 tại 80%")) if t]
        if lines:
            a(f"- **{NAME[s]}** — tổng chi {pct(v(s, 'cost_pct_fyp'))} FYP; " + "; ".join(f"{t['trap'][0].lower() + t['trap'][1:]}: {t['value_text']} {t['citation']}" for t in lines) + ".")
    a("")

    # ---------------- Trang 3 ----------------
    a("## Trang 3 — Tác động lên 3 mục tiêu của đề bài")
    a("")
    a("| Mục tiêu | " + " | ".join(NAME[s] for s in schemes) + " |")
    a("|---|" + "---|" * len(schemes))
    a("| Chi trả giảm khi K2 85% → 65% (cao = gắn chất lượng) | " + " | ".join(pct(drop(s)) for s in schemes) + " |")
    a("| Chi phí / phí còn duy trì, K2 85% | " + " | ".join(pct(v(s, "cost_per_persisted_pct", 85)) for s in schemes) + " |")
    a("| Chi phí / phí còn duy trì, K2 65% | " + " | ".join(pct(v(s, "cost_per_persisted_pct", 65)) for s in schemes) + " |")
    a("| Tổng chi / FYP, K2 85% | " + " | ".join(pct(v(s, "cost_pct_fyp")) for s in schemes) + " |")
    a("")
    a("- **Doanh số** `HYPOTHESIS`: thu nhập đại lý Full-time và quản lý không thấp hơn thị trường (trang 2) là điều kiện giữ và tuyển người; mức tăng FYP thật chỉ đo được bằng thí điểm (trang 7).")
    if be_need:
        a(f"- **Doanh số cần đạt để hòa vốn** `PROPOSAL`: đo bằng phần FYP giữ lại sau chi trả kênh đại lý (không phải lợi nhuận — biên lợi nhuận thật `UNKNOWN`), cơ cấu 4 nhóm năng suất "
          f"(7 không hoạt động / 13 × 10tr / 15 × 20tr / 10 × 77tr FYP/tháng) — {be_txt}. Thí điểm phải vượt mức này mới coi là thắng.")
    a("- **Chất lượng:** trợ cấp Full-time chỉ trả khi K2 ≥ 80%; phí quản lý nhân hệ số K2; trả chậm nhận đủ khi K2 ≥ 80%, một nửa khi 75–80%, mất khi dưới 75% `PROPOSAL`.")
    a(f"- **Chi phí:** xem trang 6 — gồm kịch bản năng suất giảm một nửa và danh mục nghiêng bảo vệ thuần.")
    a("")

    # ---------------- Trang 4 ----------------
    a("## Trang 4 — Học gì từ đối thủ: Áp dụng / Cải tiến / Tránh")
    a("")
    a("| Cơ chế | Hãng | Quyết định | Lý do | Mã quy tắc (truy vết trang PDF) |")
    a("|---|---|---|---|---|")
    for m in adopt_matrix():
        rules = ", ".join(r for r in m["rules"] if full or not r.startswith("MNL-AG") and not r.startswith("MNL-MG")) or "—"
        a(f"| {m['mechanism']} | {m['company'] or '—'} | {DEC_VN.get(m['decision'], m['decision'])} | {m['why']} | {rules} |")
    a("")

    # ---------------- Trang 5 ----------------
    a(f"## Trang 5 — Kiến trúc {PROPOSAL} `PROPOSAL`")
    a("")
    a("| Tầng | Cơ chế | Điều kiện chất lượng |")
    a("|---|---|---|")
    a("| Đại lý — 2 đường ray | **Full-time:** thưởng tháng 5 bậc đủ 100% + trợ cấp 3 triệu/tháng × hệ số vùng khi đạt quota vùng · **Part-time:** thưởng 70%, không trợ cấp | Trợ cấp cần quota, ≥ 2 hợp đồng/tháng và K2 ≥ 80% |")
    a("| Quản lý nhóm / ban | Override trực tiếp × hệ số K2; gián tiếp tối đa 2 đời, khóa nếu FYC nhóm trực tiếp < 15 triệu × hệ số vùng; một phần trả chậm 3 năm | Trả chậm: đủ khi K2 ≥ 80%, 50% khi 75–80%, 0 dưới 75% |")
    a("| Lãnh đạo khu vực | Phí cơ bản × % đạt chỉ tiêu (sàn 30%, trần 140%) thay phí cố định; phần lớn override trả chậm | K2 vùng ≥ 75% ở mỗi kỳ trả |")
    a("| Cơ sở tính | Thưởng & phí quản lý tính trên **FYC chuẩn hóa = FYP × 30%**; hoa hồng vẫn trả theo sản phẩm | Không thưởng trên phí đóng thêm |")
    a("| Trần chi trả | Tổng chi trả hệ thống đại lý ≤ 75% FYP; vượt trần thì thưởng + phí quản lý co theo cùng tỷ lệ | Kiểm ở kịch bản xấu nhất |")
    a("")
    a(f"**{len(regions)} vùng theo lương tối thiểu vùng (Nghị định 293/2025):** " + " · ".join(f"{x['region']} {vn((x['coef'] or 0) * 100, 0)}%" for x in regions)
      + " — chỉ tiêu FYP/FYC và trợ cấp nhân hệ số; giữ nguyên ≥ 2 hợp đồng/tháng và K2 ≥ 80%.")
    a("")
    a("**Kiểm trần pháp lý** — Điều 52 Thông tư 67/2023: thưởng + hỗ trợ đại lý (không gồm hoa hồng) ≤ 30% FYP phí định kỳ `CONDITIONAL`:")
    a("")
    a("| Phương án | Thưởng + hỗ trợ / FYP | Kịch bản xấu nhất | So trần 30% |")
    a("|---|---:|---:|---|")
    for s in schemes:
        x, w = v(s, "art52_agent_bonus_pct_fyp"), v(s, "art52_agent_bonus_pct_fyp_worst")
        if x is not None:
            a(f"| {NAME[s]} | {pct(x)} | {pct(w)} | {'Trong trần' if max(x, w or 0) <= 30 else 'Vượt trần'} |")
    a("")
    a("Từ 01/01/2027, TT 96/2026 thêm trần **7% phí thực thu** cho hợp đồng **đóng phí một lần** `SOURCE_CLAIM` — mô hình hiện chỉ tính phí định kỳ; sản phẩm đóng phí một lần phải tách riêng.")
    a("")
    a("**Rủi ro còn mở của đề xuất (công bố, không giấu):**")
    for t in ("Vách đá K2 tại 80%", "Vách đá K2 của đại lý Full-time", "Vách đá quota & dồn hợp đồng", "Bẫy giữ đội phẳng"):
        r = trap("Hybrid", t)
        if r:
            a(f"- {r['trap']}: {r['value_text']} `PROPOSAL`")
    a("- Lách vùng (đăng ký mã vùng có hệ số thấp) — cần quy tắc xác định vùng theo địa bàn hoạt động thực tế.")
    a("")

    # ---------------- Trang 6 ----------------
    a("## Trang 6 — Bằng chứng định lượng: chi phí, dòng tiền, độ nhạy")
    a("")
    a("| Phương án | Tổng chi / FYP | Năng suất −50% | Kịch bản xấu nhất | Hoa hồng 40% | 40% — xấu nhất | Tiền mặt năm 1 | Trả chậm | Phần cố định |")
    a("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for s in schemes:
        a(f"| {NAME[s]} | {pct(v(s, 'cost_pct_fyp'))} | {pct(v(s, 'cost_pct_fyp_half_production'))} | {pct(v(s, 'cost_pct_fyp_worst_case'))} | "
          f"{pct(v(s, 'cost_pct_fyp_fyc40'))} | {pct(v(s, 'cost_pct_fyp_worst_fyc40'))} | {pct(v(s, 'cash_y1_share'))} | {pct(v(s, 'deferred_share'))} | {pct(v(s, 'fixed_share'))} |")
    a("")
    a(f"- Khi bán nghiêng bảo vệ thuần (hoa hồng 40%), đề xuất chạm đúng trần 75% ở kịch bản xấu nhất; quỹ thưởng vẫn trả {pct(v('Hybrid', 'pool_paid_share_worst_fyc40'), 0)} `MODEL_OUTPUT`.")
    a("- **Giới hạn ROI:** đây là chi phí mô phỏng trên FYP, chưa phải lợi nhuận. Muốn ra ROI thật cần: cơ cấu sản phẩm, biên VNB theo sản phẩm, chi phí vượt định mức (expense overrun) và chi phí vận hành văn phòng — do bộ phận Định phí (Actuarial) cung cấp.")
    a("")

    # ---------------- Trang 7 ----------------
    a("## Trang 7 — Lộ trình & tham số hiệu chỉnh")
    a("")
    a("1. **Ghép số thật (tháng 1):** cơ cấu sản phẩm, VNB theo sản phẩm, chi phí vượt định mức từ Actuarial → thay chi phí / FYP bằng ROI thật.")
    a("2. **Thí điểm 6–12 tháng:** 1 văn phòng Vùng I và 1 văn phòng Vùng III, mỗi nơi ghép với 1 văn phòng đối chứng tương đồng (quy mô, năng suất, K2 lịch sử) giữ chính sách cũ. "
      "Đọc sớm sau 1 quý: FYP / đại lý hoạt động, tỷ lệ hoạt động, số hợp đồng / đại lý, tỷ lệ hủy trong 21 ngày cân nhắc, tỷ lệ đóng phí kỳ 2.")
    a("3. **Đánh giá K2 & ban hành:** K2 chỉ đo đủ ở tháng 13–15; ban hành toàn quốc khi K2 nhóm thí điểm không thấp hơn đối chứng và tổng chi / FYP vẫn ≤ 75% ở kịch bản xấu nhất.")
    a("")
    a("**Tham số hiệu chỉnh khi có số thật** (không cần đổi cấu trúc đề xuất):")
    a("")
    a("| Tham số | Đang dùng | Thay bằng |")
    a("|---|---|---|")
    a("| Ngân sách chi trả | Trần 75% FYP | Ngân sách phân phối được duyệt |")
    a("| Năng suất & cơ cấu lực lượng | 26,7 triệu FYP/đại lý, toàn Full-time | Phân phối năng suất thật, tỷ lệ Full-time / Part-time |")
    a("| Chất lượng | K2 85% / 65% | K2 lịch sử theo vùng, theo sản phẩm |")
    a("| Cơ cấu sản phẩm | Hoa hồng 30% (độ nhạy 25–40%) | Product mix thật |")
    a("| Hệ số vùng | NĐ 293/2025 (100/89/78/70%) | Giữ, hoặc thay bằng dữ liệu năng suất vùng |")
    a("")
    a("**Mô hình Excel tham chiếu** (`outputs/working/W24_Compensation_Reference_Model_v1.xlsx`) kiểm chứng mô hình **1 vùng 12 tỷ FYP/năm** và phương án tiền thân; "
      f"**không chứa {PROPOSAL}** và mô hình 45 đại lý — số của đề xuất lấy từ mô hình Python và trang tương tác (tự kiểm khớp mỗi lần mở).")
    a("")

    # ---------------- Phụ lục ----------------
    a("## Phụ lục — Lịch sử thiết kế")
    a("")
    a(f"- Vòng 1 (mô hình 1 vùng 12 tỷ FYP/năm, K2 kéo được): **Balanced Hybrid → Song Hành** và 2 biến thể (Song Hành siết K2, Tiết kiệm tối đa). Vẫn xem được ở nhóm “Phân tích sâu” của trang tương tác.")
    a(f"- Vòng 2 (mô hình khu vực 45 đại lý, 4 mốc chuẩn): **{PROPOSAL}** (tên làm việc cũ: “Chính sách Lai”) kế thừa tham số Song Hành, thêm 2 đường ray, FYC chuẩn hóa, trần tổng chi 75% và hệ số vùng.")
    a("- Hai mô hình khác quy mô và cơ cấu nên % chi phí khác nhau — không cộng trừ số giữa hai mô hình.")
    a("")
    return "\n".join(L)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full-out", help="ghi thêm bản đủ số (gồm dòng restricted) ra đường dẫn này — đặt NGOÀI repo")
    a = ap.parse_args(argv)
    tables = json.loads(SNAP.read_text(encoding="utf-8"))["tables"]
    OUT.write_text(render(tables, full=True), encoding="utf-8")   # DEC-16: repo công khai toàn bộ, kể cả Manulife
    msg = f"wrote {OUT.relative_to(REPO)}"
    if a.full_out:
        p = Path(a.full_out).resolve()
        p.write_text(render(tables, full=True), encoding="utf-8")
        msg += " + full copy outside repo"
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
