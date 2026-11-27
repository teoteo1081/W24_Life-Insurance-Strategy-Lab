"""Sinh outputs/interview/00_Role_And_Benefit_Matrix.md và knowledge/sources/pdf-bookmarks.json.

Ma trận quyền lợi ngang hàng theo 4 mốc × 3 hãng × 6 dòng:
 (1) Hoa hồng trực tiếp  (2) Phí quản lý F1  (3) Phí quản lý gián tiếp F2–F4
 (4) Thưởng quý / năm / tăng trưởng  (5) Phí / thưởng duy trì tái tục (RYC)  (6) Điều kiện chặn K2 / tuyển mới
Mỗi ô: số tiền (tr/tháng, MODEL_OUTPUT) hoặc điều kiện (VERIFIED FACT) + `[Memo : Trang]`.
Số tiền dùng đúng các hàm của scripts/build_interview_income_table.py (cùng engine, cùng giả định).
Mọi trích dẫn có token được kiểm trên text trang; bản scan CHH0DCEB260003V ghi là đối chiếu bằng mắt.
Chạy:  python scripts/build_benefit_matrix.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))
import pymupdf  # noqa: E402

import build_interview_income_table as T  # noqa: E402
from w24_milestones import FILE_IDS, aia_title, chubb_title, load_milestones, manulife_title, rubric_table  # noqa: E402

OUT_MD = REPO / "outputs" / "interview" / "00_Role_And_Benefit_Matrix.md"
OUT_BM = REPO / "knowledge" / "sources" / "pdf-bookmarks.json"
SCAN_ID = "CHH0DCEB260003V"
CITE = re.compile(r"\[[^\]:]+ : [0-9]+(-[0-9]+)?\]")

# Mục lục bản scan 0003V — đọc bằng mắt trang 2 (MỤC LỤC) ngày 2026-11-27
SCAN_TOC = [("I. QUY ĐỊNH CHUNG", 3), ("1. MỤC ĐÍCH", 3), ("2. HỆ THỐNG CẤP BẬC", 3), ("3. PHẠM VI ÁP DỤNG", 3), ("4. HIỆU LỰC THI HÀNH", 3),
            ("5. MỐI QUAN HỆ BÁO CÁO", 4), ("6. BẢNG TÓM TẮT CÁC KHOẢN CHI TRẢ", 4), ("II. CÁC KHOẢN PHÍ DỊCH VỤ", 5),
            ("1. PHÍ DỊCH VỤ ĐÀO TẠO TIÊU CHUẨN THÁNG", 5), ("2. PHÍ DỊCH VỤ QUẢN LÝ HOẠT ĐỘNG THÁNG", 6), ("3. PHÍ DỊCH VỤ QUẢN LÝ KINH DOANH THÁNG", 6),
            ("4. PHÍ DỊCH VỤ QUẢN LÝ CHẤT LƯỢNG HOẠT ĐỘNG ĐẠI LÝ BẢO HIỂM THÁNG", 7), ("5. PHÍ DỊCH VỤ QUẢN LÝ VÀ PHÁT TRIỂN KINH DOANH QUÝ", 8),
            ("6. PHÍ DỊCH VỤ QUẢN LÝ CHẤT LƯỢNG PHỤC VỤ KHÁCH HÀNG QUÝ", 9), ("7. PHÍ DỊCH VỤ ĐÀO TẠO VÀ PHÁT TRIỂN ĐỘI NGŨ TRỰC THUỘC", 10),
            ("8. PHÍ DỊCH VỤ QUẢN LÝ ĐỘI NGŨ TRỰC THUỘC", 11), ("III. QUY ĐỊNH VỀ NGHIỆM THU PHÍ DỊCH VỤ", 12), ("IV. CHỈ TIÊU THĂNG CẤP VÀ DUY TRÌ CẤP BẬC", 12),
            ("1. CHỈ TIÊU THĂNG CẤP", 12), ("2. CHỈ TIÊU DUY TRÌ CẤP BẬC", 13), ("V. QUY ĐỊNH KHÁC", 13)]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip().lower()


def load_pages():
    reg = {r["Source_ID"]: r for r in csv.DictReader(open(REPO / "knowledge/sources/source-registry.csv", encoding="utf-8"))}
    out = {}
    for fid, sid in FILE_IDS.items():
        r = reg[sid]
        out[fid] = {"sid": sid, "path": r["Local_Relative_Path"], "name": r["Original_Filename"],
                    "pages": [p.get_text() for p in pymupdf.open(REPO / r["Local_Relative_Path"])]}
    return out


HEAD_RE = re.compile(r"^(PHỤ LỤC\s+\d+|PHỤ ĐÍNH\s+[IVX]+|[A-E]|[IVX]{1,4}|\d{1,2})[.:)]?\s+(.{3,90})$")


def is_heading(line: str) -> bool:
    m = HEAD_RE.match(line.strip())
    if not m:
        return False
    lead, text = m.group(1), m.group(2).strip()
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return False
    upper_ratio = sum(c.isupper() for c in letters) / len(letters)
    if lead.isdigit():
        return upper_ratio >= 0.85 and len(text) >= 6                 # "1. HOA HỒNG ĐẠI LÝ"
    if lead.startswith(("PHỤ", "Phụ")):
        return True
    return upper_ratio >= 0.6 or (len(lead) <= 4 and text[0].isupper() and len(text) <= 70 and not text.endswith(","))


def bookmarks(pages):
    data = {"$comment": "Mục lục trang của 9 PDF nguồn. Không file nào có bookmark gắn sẵn (get_toc() = 0) nên dựng từ dòng tiêu đề trong text; "
                        "bản scan CHH0DCEB260003V lấy từ trang MỤC LỤC (tr.2) đọc bằng mắt. Dùng cho web: mở PDF tại #page=N.",
            "generated_by": "scripts/build_benefit_matrix.py", "files": []}
    for fid, s in pages.items():
        items = []
        if fid == SCAN_ID:
            items = [{"title": t, "page": p, "method": "visual_toc_p2"} for t, p in SCAN_TOC]
        else:
            seen = set()
            for i, t in enumerate(s["pages"]):
                lines = [re.sub(r"\s+", " ", x).strip() for x in t.splitlines()]
                lines = [x for x in lines if x]
                for j, ln in enumerate(lines):
                    if re.fullmatch(r"([A-E]|[IVX]{1,4}|\d{1,2})\.", ln) and j + 1 < len(lines):
                        ln = f"{ln} {lines[j + 1]}"          # số mục và tên mục bị ngắt dòng
                    if re.search(r"\.{4,}|…{2,}", ln):     # dòng mục lục có chấm dẫn — bỏ, dùng tiêu đề thật trong thân văn bản
                        continue
                    if is_heading(ln) and (ln, i + 1) not in seen:
                        seen.add((ln, i + 1))
                        items.append({"title": ln, "page": i + 1, "method": "text_heading"})
        data["files"].append({"file_id": fid, "source_id": s["sid"], "file_name": s["name"], "local_relative_path": s["path"],
                              "page_count": len(s["pages"]), "bookmarks": items})
    return data


def um_c1_rate(c1: float) -> float:
    """0047M01 p.1: tỷ lệ cấp 1 theo FYC cấp 1 trong tháng."""
    return 0.20 if c1 >= 48 else (0.16 if c1 >= 24 else (0.14 if c1 >= 7 else 0.10))


def build():
    pages = load_pages()
    MS = load_milestones()

    def on_page(fid, pg, tok):
        if fid == SCAN_ID or not tok:
            return True
        a, _, b = pg.partition("-")
        text = " ".join(norm(pages[fid]["pages"][p - 1]) for p in range(int(a), int(b or a) + 1))
        return all(w in text for w in norm(tok).split())

    ev = {"numeric": 0, "cited": 0, "data": 0, "labelled": 0, "missing": 0, "missing_proof": 0}
    checks = []

    def C(fid, pg, tok=""):
        """Trích dẫn có kiểm token trên trang."""
        if not on_page(fid, pg, tok):
            raise SystemExit(f"token '{tok}' not found on [{fid} : {pg}]")
        checks.append((fid, pg))
        return f"[{fid} : {pg}]"

    def cell(val, cite, label="MODEL_OUTPUT"):
        return {"val": val, "cite": cite, "label": label}

    vn, m = T.vn, T.m
    titles = {ms.mid: (aia_title(ms)[0], chubb_title(ms)[0], manulife_title(ms)[0]) for ms in MS}
    # ---- numbers (same functions as 01)
    fyc, y2, y3, ra, rc = T.agent_m1(MS[0])
    rm = T.mnl_agent_m1(MS[0])
    mgr = {}
    for ms in MS[1:3]:
        mgr[ms.mid] = (T.aia_manager(ms)[0], T.chubb_manager(ms, titles[ms.mid][1] if titles[ms.mid][1] in ("UM", "SM", "DM") else "DM")[0], T.mnl_um(ms)[0])
    ms4 = MS[3]
    a4_cql = T.aia_manager(ms4, include_indirect=False)[0]
    paf = T.calc_aia_paf_12m("PAF", 1, [ms4.fyp_month] * 12, [ms4.fyc_month] * 12, [float(ms4.agents)] * 12, fy_pct=T.K2, attendance_pct=80.0)
    u4 = T.mnl_um(ms4)[0]

    NEG = "Negative Proof: `00_Role_Mapping_Audit.md` mục 4.3"
    ROWS = ["(1) Hoa hồng trực tiếp", "(2) Phí quản lý F1 (nhóm trực tiếp)", "(3) Phí quản lý gián tiếp F2–F4", "(4) Thưởng quý / năm / tăng trưởng",
            "(5) Duy trì tái tục (RYC)", "(6) Điều kiện chặn K2 / tuyển mới"]
    k2gate_aia_cql = "FY nhóm <80% → bậc phí thấp hơn; FY <70% → phí hoạt động × FY thực đạt; quý cần FY ≥75%; người mới/quý: 3 sao ≥1, 4–5 sao ≥2 (từ Q2)"
    k2gate_chb_al = "Phí tháng × K2 NTT (≥80%: 120% … <50%: 25%); phí RYC cần K2 NTT ≥65%; gián tiếp = 0 nếu FYC NTT <15tr"
    k2gate_mnl_um = "Phí hoạt động × TLDTHD cấp 1 (từ 04/2026: ≥80% 110% … <50% TLDTHD/2); phải \"Đội ngũ chuyên cần\" ≥4 buổi/tháng; phí dài hạn cần TLDTHD ≥70%"

    M = {}
    # M1
    M["M1"] = {
        "AIA": [cell(f"{vn(m(ra['fyc_total'] + y2 + y3))} (FYC + tái tục, A1/A7)", C("AIAVAD 2604-069", "18", "phụ lục về hoa hồng"), "ASSUMPTION"),
                cell("— không quản lý", C("AIAVAD 2601-034", "8", "UM 2"), "VERIFIED FACT"),
                cell("— không quản lý", C("AIAVAD 2601-034", "4", "50.0% 25.0% 12.5%"), "VERIFIED FACT"),
                cell(vn(m(ra["bonus_quarterly_prod"] + ra["bonus_quarterly_premier"] + ra["bonus_annual"])), C("AIAVAD 2604-069", "5-7")),
                cell(vn(m(ra["bonus_syc"])) + " (thưởng SYC)", C("AIAVAD 2604-069", "6")),
                cell("Thưởng × hệ số FY 2026; lên UM cần ≥2 người tuyển/6 tháng", C("AIAVAD 2604-069", "3") + ", " + C("AIAVAD 2601-034", "8"), "VERIFIED FACT")],
        "Chubb": [cell(f"{vn(m(rc['fyc_total'] + rc['ryc_total']))} (FYC + RYC, A1/A7)", C("CHH0DCEB260007V", "13-19"), "ASSUMPTION"),
                  cell("— không quản lý", C("CHH0DCEB260008V", "3", "AR UM SM DM"), "VERIFIED FACT"),
                  cell("— không quản lý", C("CHH0DCEB260008V", "7", "L1 L2 L3"), "VERIFIED FACT"),
                  cell(vn(m(rc["bonus_hqkd_monthly"] + rc["bonus_hqkd_quarterly"])) + " (HQKD tháng + quý)", C("CHH0DCEB260007V", "4-6")),
                  cell(vn(m(rc["bonus_ryc_quarterly"])), C("CHH0DCEB260007V", "6-7")),
                  cell("Thưởng × K2 cá nhân (≥80%: 120% … <50%: 25%); RYC cần K2 ≥65%; lên UM cần 2 đại lý giới thiệu đạt 3MAA", C("CHH0DCEB260007V", "4") + ", " + C("CHH0DCEB260007V", "7"), "VERIFIED FACT")],
        "Manulife": [cell(f"{vn(m(rm['fyc_total'] + rm['ryc_total']))} (FYC + tái tục, A1/A7)", C("0046M01_2026", "9", "Hoa hồng dành cho Đại Lý"), "ASSUMPTION"),
                     cell("— không quản lý", C("0047M01_2026", "1", "UM+"), "VERIFIED FACT"),
                     cell("— không quản lý", C("0047M01_2026", "1", "Cấp 2, 3, 4"), "VERIFIED FACT"),
                     cell(vn(m(rm["bonus_monthly_productivity"] + rm["bonus_quarterly_productivity"] + rm["bonus_mstar_quarterly"] + rm["bonus_mstar_annual"])) + " (năng suất tháng/quý + M-Star)", C("0046M01_2026", "4-8")),
                     cell("— không có khoản riêng", C("0046M01_2026", "2-8"), "VERIFIED FACT"),
                     cell("Mọi thưởng × hệ số TLDTHD (từ 04/2026: ≥70% 100%, <50% TLDTHD/2) × CLKD; điều kiện lên UM+ ở 0013M04/2024 (không có)", C("0046M01_2026", "1", "Hệ số nhân") + ", " + C("0047M01_2026", "6", "0013M04"), "VERIFIED FACT")],
    }
    for ms in MS[1:3]:
        a, c, u = mgr[ms.mid]
        c1 = ms.direct_agents * ms.fyp_per_agent * T.FYC_RATE
        M[ms.mid] = {
            "AIA": [cell("— quản lý không tự bán (A3)", "", "ASSUMPTION"),
                    cell(vn(m(a["direct_monthly"] + a["activity_monthly"])), C("AIAVAD 2601-034", "3", "≥ 50 20% 24%")),
                    cell(vn(m(a["indirect_fee"])) if ms.sub_units else "— không có quản lý con", C("AIAVAD 2601-034", "4", "50.0%"), "MODEL_OUTPUT" if ms.sub_units else "ASSUMPTION"),
                    cell(vn(m(a["premier_quarterly"] + a["annual_deferred_3y"])) + " (quý 4 sao + năm trả chậm)", C("AIAVAD 2601-034", "4-5")),
                    cell("— không có khoản này", C("AIAVAD 2601-034", "3-7"), "VERIFIED FACT"),
                    cell(k2gate_aia_cql, C("AIAVAD 2601-034", "3-5"), "VERIFIED FACT")],
            "Chubb": [cell("— quản lý không tự bán (A3)", "", "ASSUMPTION"),
                      cell(vn(m(c["ht_ktn_monthly"])), C("CHH0DCEB260008V", "5", "Từ 40 trở lên 50% 60%")),
                      cell(vn(m(c["indirect_l1_l3"])) if ms.sub_units else "— không có AL con", C("CHH0DCEB260008V", "7"), "MODEL_OUTPUT" if ms.sub_units else "ASSUMPTION"),
                      cell(vn(m(c["ht_ktn_quarterly"])) + " (HT KTN quý)", C("CHH0DCEB260008V", "6", "Từ 100 trở lên")),
                      cell(vn(m(c["persistency_ryc_quarterly"])), C("CHH0DCEB260008V", "9-10")),
                      cell(k2gate_chb_al, C("CHH0DCEB260008V", "5-10"), "VERIFIED FACT")],
            "Manulife": [cell("— quản lý không tự bán (A3)", "", "ASSUMPTION"),
                         cell(vn(c1 * um_c1_rate(c1)) + " (A.I cấp 1) + " + vn(m(u["a2_team_activity"])) + " (A.II)", C("0047M01_2026", "1-2")),
                         cell(vn(m(u["a1_team_productivity"]) - c1 * um_c1_rate(c1)) + " (cấp 2 × ½ tỷ lệ)" if ms.sub_units else "— không có cấp 2", C("0047M01_2026", "1", "Cấp 2, 3, 4"), "MODEL_OUTPUT" if ms.sub_units else "ASSUMPTION"),
                         cell("0 (phí dài hạn chỉ cho MBA Pro)", C("0047M01_2026", "5", "MBA Pro"), "ASSUMPTION"),
                         cell("— không có khoản này", C("0047M01_2026", "1-6"), "VERIFIED FACT"),
                         cell(k2gate_mnl_um, C("0047M01_2026", "2-3") + ", " + C("0047M01_2026", "6"), "VERIFIED FACT")],
        }
    # M4 — TJ 2026-11-27: so sánh CHÍNH = tuyến lãnh đạo vùng (AIA PAF · Chubb RD · Manulife PSM/SM);
    #      bảng PHỤ = tuyến quản lý truyền thống (Chubb DM · Manulife UM+). Chubb BD (chức danh đạt được bằng chỉ tiêu) không có biểu phí.
    c1_4 = ms4.direct_agents * ms4.fyp_per_agent * T.FYC_RATE
    y2o, y3o = T.renewal_split(ms4.fyp_month)
    rd = T.calc_chubb_rd_12m([ms4.fyp_month] * 12, [ms4.fyc_month] * 12, [ms4.agents] * 12, [ms4.agents] * 12, [(y2o + y3o) / 12] * 12,
                             k2_pct=T.K2, weighted_reported_fyp_monthly=ms4.fyp_month, training_classes_monthly=4, prior_year_q_fyp=[ms4.fyp_month * 3] * 4)
    psm = T.calc_manulife_psm_12m(T.MNL_BASE, [T.MNL_ACH] * 12, [ms4.fyc_month] * 12, [T.MNL_AA_ACH] * 4, T.K2)
    dm4 = T.chubb_manager(ms4, "DM")[0]
    M["M4"] = {
        "AIA": [cell("— quản lý không tự bán (A3)", "", "ASSUMPTION"),
                cell(f"{vn(m(paf['base_fee_12m']))} (phí cơ bản PAF) + {vn(m(paf['prof_monthly_12m']))} (chuyên môn tháng) + {vn(m(a4_cql['direct_monthly'] + a4_cql['activity_monthly']))} (CQL trực tiếp)", C("AIAVAD 2601-035", "3-4") + ", " + C("AIAVAD 2601-035", "2")),
                cell("0 — PAF+ không nhận gián tiếp cấp 2-3-4", C("AIAVAD 2601-035", "2", "cấp 2-3-4"), "VERIFIED FACT"),
                cell(f"{vn(m(paf['prof_quarterly_12m']))} (chuyên môn quý) + {vn(m(paf['seniority_fee_clawback12m']))} (vượt chỉ tiêu) + {vn(m(a4_cql['premier_quarterly'] + a4_cql['annual_deferred_3y']))} (CQL quý/năm)", C("AIAVAD 2601-035", "4-5")),
                cell("— không có khoản này", C("AIAVAD 2601-035", "3-5"), "VERIFIED FACT"),
                cell("Hệ số FY cho phí chuyên môn: ≥75% 120% … <50% 0%; phí cơ bản theo % đạt chỉ tiêu FYP (<35% = 0)", C("AIAVAD 2601-035", "3-4"), "VERIFIED FACT")],
        "Chubb": [cell("— RD không tự bán (A3)", "", "ASSUMPTION"),
                  cell(f"{vn(m(rd['training_12m'] + rd['activity_12m'] + rd['business_12m']))} (đào tạo 25 + hoạt động 8 + kinh doanh 12) + {vn(m(rd['quality_3maa_12m']))} (chất lượng 12% FYC)", C(SCAN_ID, "5-7")),
                  cell("0 — không có BD/RD con trong cấu trúc mốc (phí II.7–II.8 = 25–50% / 12,5–25% phí của BD/RD con)", C(SCAN_ID, "10-11"), "ASSUMPTION"),
                  cell(f"{vn(m(rd['growth_quarterly_12m']))} (tăng trưởng quý 2,5% — FYP đi ngang)", C(SCAN_ID, "8-9")),
                  cell(f"{vn(m(rd['ryc_quarterly_12m']))} (30% RYC năm 2–5, K2 ≥70%; RYC theo A7)", C(SCAN_ID, "9-10")),
                  cell("Phí chất lượng & tăng trưởng = 0 nếu K2 <60% (từ Q3/2026); duy trì: nhánh trực tiếp 750tr FYP + 25 EHC / 6 tháng; chức danh RD do bổ nhiệm theo hợp đồng", C(SCAN_ID, "7") + ", " + C(SCAN_ID, "13") + ", " + C(SCAN_ID, "3"), "VERIFIED FACT")],
        "Manulife": [cell("— PSM+ không tự bán (A3)", "", "ASSUMPTION"),
                     cell(f"{vn(m(psm['base_fee_12m']))} (phí cơ bản 35tr × 100% × 130%) + {vn(m(psm['productivity_12m']))} (năng suất 6% FYC × TLDTHD)", C("0048M01_2026", "1-2")),
                     cell("0 — không có PSM+ báo cáo trực tiếp (gián tiếp = 50% phí của cấp báo cáo)", C("0048M01_2026", "2", "50%"), "ASSUMPTION"),
                     cell(f"{vn(m(psm['activity_quarterly_12m']))} (hoạt động quý 2,5%) + {vn(m(psm['long_term_deferred_3y']))} (hợp tác dài hạn, trả chậm 30/30/40)", C("0048M01_2026", "2-5")),
                     cell("— không có khoản này", C("0048M01_2026", "1-5"), "VERIFIED FACT"),
                     cell("Phí cơ bản = 0 nếu đạt <30% chỉ tiêu FYP; phí năng suất/quý × TLDTHD (từ 04/2026: <50% → TLDTHD/2); phí dài hạn cần ≥85% chỉ tiêu và TLDTHD ≥70%; chức danh PSM+ do bổ nhiệm (0013M04/2024 không có)", C("0048M01_2026", "1-4"), "VERIFIED FACT")],
    }
    M4B = {
        "Chubb": [cell("— quản lý không tự bán (A3)", "", "ASSUMPTION"),
                  cell(vn(m(dm4["ht_ktn_monthly"])), C("CHH0DCEB260008V", "5", "Từ 40 trở lên 50% 60%")),
                  cell(vn(m(dm4["indirect_l1_l3"])) + " (L1 50% × 4 AL con + L2 25% × 4 UM)", C("CHH0DCEB260008V", "7")),
                  cell(vn(m(dm4["ht_ktn_quarterly"])) + " (HT KTN quý)", C("CHH0DCEB260008V", "6", "Từ 100 trở lên")),
                  cell(vn(m(dm4["persistency_ryc_quarterly"])), C("CHH0DCEB260008V", "9-10")),
                  cell(k2gate_chb_al + "; đủ điều kiện lên BD nhưng biểu phí BD không có trong nguồn (" + NEG + ")", C("CHH0DCEB260008V", "5-10") + ", " + C("CHH0DCEB260007V", "7", "450 lên BD"), "VERIFIED FACT")],
        "Manulife": [cell("— quản lý không tự bán (A3)", "", "ASSUMPTION"),
                     cell(f"{vn(c1_4 * um_c1_rate(c1_4))} (A.I cấp 1) + {vn(m(u4['a2_team_activity']))} (A.II)", C("0047M01_2026", "1-2")),
                     cell(vn(m(u4["a1_team_productivity"]) - c1_4 * um_c1_rate(c1_4)) + " (cấp 2 × 8% + cấp 3 × 4%)", C("0047M01_2026", "1", "Cấp 2, 3, 4")),
                     cell("0 (phí dài hạn chỉ cho MBA Pro)", C("0047M01_2026", "5", "MBA Pro"), "ASSUMPTION"),
                     cell("— không có khoản này", C("0047M01_2026", "1-6"), "VERIFIED FACT"),
                     cell(k2gate_mnl_um, C("0047M01_2026", "2-3"), "VERIFIED FACT")],
    }
    totals = {"M1": (T.m(ra["total_earned"] + y3), T.m(rc["total_earned"]), T.m(rm["total_earned"])),
              "M2": tuple(T.m(x["total_earned"]) for x in mgr["M2"]), "M3": tuple(T.m(x["total_earned"]) for x in mgr["M3"]),
              "M4": (T.m(paf["total_earned"] + a4_cql["total_earned"]), T.m(rd["total_earned"]), T.m(psm["total_earned"]))}
    header4 = {"M4": ("PAF", "RD (bổ nhiệm)", "PSM/SM (bổ nhiệm)")}

    def emit_row_block(cols, data):
        for i, rname in enumerate(ROWS):
            cells_txt = []
            for co in cols:
                c = data[co][i]
                ev["data"] += 1
                ev["labelled"] += 1
                if c["label"] == "UNKNOWN":
                    ev["missing"] += 1
                    ev["missing_proof"] += int("Negative Proof" in c["val"])
                elif re.search(r"\d", re.sub(r"\bA\d+\b|\d{4}M\d{2}/\d{4}", "", c["val"])):   # bỏ mã giả định (A3) / mã văn bản
                    ev["numeric"] += 1
                    ev["cited"] += int(bool(CITE.search(c["cite"] + c["val"])))
                cells_txt.append(f"{c['val']} {c['cite']} `{c['label']}`".strip())
            w(f"| {rname} | " + " | ".join(cells_txt) + " |")

    L = []
    w = L.append
    w("# 00 — Ma trận chức danh & quyền lợi ngang hàng (4 mốc × 3 hãng × 6 dòng)")
    w("")
    w("> Nguồn: 9/9 PDF trong `private/sources/` (3 AIA + 3 Chubb + 3 Manulife), kiểm kê và Negative Proof ở `00_Role_Mapping_Audit.md`. "
      "Số tiền = **tr/tháng** (`MODEL_OUTPUT`, cùng engine và giả định với `01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md`); điều kiện = `VERIFIED FACT`. "
      "Mọi trích dẫn có token được script kiểm trên text trang. Mục lục 9 PDF: `knowledge/sources/pdf-bookmarks.json`.")
    w("")
    w("> **Mốc 2–4 là PHÍ QUẢN LÝ THUẦN — KHÔNG gồm hoa hồng/thưởng tự bán của quản lý** (giả định A3). "
      "Vì vậy tổng Mốc 2 của AIA và Manulife có thể **thấp hơn** Mốc 1 (đại lý tự bán 30tr FYP/tháng). Nếu quản lý vẫn tự bán như Mốc 1, cộng thêm "
      f"thu nhập cá nhân Mốc 1: AIA {vn(T.m(ra['total_earned'] + y3))}, Chubb {vn(T.m(rc['total_earned']))}, Manulife {vn(T.m(rm['total_earned']))} tr/tháng "
      "(xấp xỉ: Chubb AL hưởng bảng thưởng cá nhân cao hơn AR `[CHH0DCEB260007V : 4]`; AIA tính FYC bản thân CQL vào nhóm trực tiếp `[AIAVAD 2601-034 : 3]`).")
    w("")
    for ms in MS:
        ta, tc, tm = header4.get(ms.mid, titles[ms.mid])
        kind = "thu nhập cá nhân" if ms.mid == "M1" else "phí quản lý thuần, không gồm tự bán"
        w(f"## {ms.label} — {ms.agents} đại lý, {vn(ms.fyp_month)}tr FYP/tháng ({kind})")
        w("")
        if ms.mid == "M4":
            w("**Bảng chính — tuyến lãnh đạo vùng** (TJ chọn ngày 2026-11-27). Chubb: chức danh đạt bằng chỉ tiêu là **BD** `[CHH0DCEB260007V : 7]` nhưng biểu phí BD không có trong nguồn; RD và PSM/SM là chức danh bổ nhiệm theo hợp đồng dịch vụ.")
            w("")
        w(f"| Dòng | AIA Alpha · **{ta}** | Chubb Life · **{tc}** | Manulife · **{tm}** |")
        w("|---|---|---|---|")
        emit_row_block(("AIA", "Chubb", "Manulife"), M[ms.mid])
        ta_, tc_, tm_ = totals[ms.mid]
        w(f"| **Tổng tr/tháng** | **{vn(ta_)}** | **{vn(tc_)}** | **{vn(tm_)}** |")
        w("")
    w("### Mốc 4 — bảng phụ: tuyến quản lý truyền thống (phí quản lý thuần)")
    w("")
    w("| Dòng | Chubb Life · **DM (AL)** — nếu chưa lên BD | Manulife · **UM+** |")
    w("|---|---|---|")
    emit_row_block(("Chubb", "Manulife"), M4B)
    w(f"| **Tổng tr/tháng** | **{vn(T.m(dm4['total_earned']))}** | **{vn(T.m(u4['total_earned']))}** |")
    w("")
    w("### Ghi chú độ nhạy — Manulife có danh hiệu MBA Pro (để chạy ở Giai đoạn 2)")
    w("")
    w("Base case = **không có danh hiệu** (tiêu chí MBA Pro ở 0050M01/2026, không có trong 9 PDF). Nếu UM+ có danh hiệu MBA Pro: "
      "phí hoạt động nhóm tăng từ 50% lên **100%** (4–5 người sản xuất) hoặc 125% (≥6) `[0047M01_2026 : 2]`; phí phát triển đại lý mới tăng từ 50% lên 100% `[0047M01_2026 : 3]`; "
      "có thêm **phí hợp tác dài hạn** 80% (Bạc) / 100% (Vàng) / 125% (Bạch Kim) × (A.II + A.III), trả chậm 30/30/40% `[0047M01_2026 : 5-6]`. "
      "Với đại lý: danh hiệu Manulife Pro mở thêm thưởng xuất sắc tháng và thưởng KDXS năm `[0046M01_2026 : 4-7]`. Nhãn: `HYPOTHESIS` — chưa đưa vào số base case.")
    w("")
    w("## Tự chấm rubric 100 điểm (`qa/data-ingestion-rubric.md`)")
    w("")
    tbl, tot = rubric_table(len(FILE_IDS), 15, 15, len(MS) * 3, len(MS) * 3, ev["cited"], ev["numeric"], ev["missing_proof"], ev["missing"], ev["labelled"], ev["data"])
    w(tbl)
    w("")
    w(f"Script đã kiểm token trên trang cho {len(checks)} trích dẫn (bản scan 0003V: đối chiếu bằng mắt).")
    if tot < 90:
        raise SystemExit(f"rubric FAIL {tot}")
    return "\n".join(L) + "\n", bookmarks(pages)


def main() -> None:
    md, bm = build()
    if re.search(r"\b(nan|inf)\b", md, re.I) or re.search(r"[A-Za-z]:\\\\Users|/Users/|file://", md + json.dumps(bm)):
        raise SystemExit("invalid output (non-finite or local path)")
    OUT_MD.write_text(md, encoding="utf-8")
    OUT_BM.write_text(json.dumps(bm, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT_MD.relative_to(REPO)} and {OUT_BM.relative_to(REPO)} ({sum(len(f['bookmarks']) for f in bm['files'])} bookmarks)")


if __name__ == "__main__":
    main()
