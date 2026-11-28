"""Sinh knowledge/sources/glossary.json — nguồn DUY NHẤT cho từ điển thuật ngữ và tooltip trên trang HTML.

Mỗi mục có 6 trường bắt buộc (abbr, english, vietnamese, company_and_memo, market_equivalent, note) + trường phụ
(group, companies, english_status, citations). Trang "xuất hiện đầu tiên" trong từng văn bản do script TỰ TÌM trên text
PDF (luật 2 & 4 AGENTS.md); bản scan CHH0DCEB260003V dùng trang đã đối chiếu bằng mắt (ghi method = visual).
Tên tiếng Anh không có trong văn bản được đánh dấu english_status = "Diễn giải" (không trình bày như nguyên văn).
Chạy:  python scripts/build_glossary.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import pymupdf  # noqa: E402

from w24_milestones import FILE_IDS  # noqa: E402

OUT = REPO / "knowledge" / "sources" / "glossary.json"
SCAN_ID = "CHH0DCEB260003V"
COMPANY_FILES = {
    "AIA": ["AIAVAD 2604-069", "AIAVAD 2601-034", "AIAVAD 2601-035"],
    "Chubb": ["CHH0DCEB260007V", "CHH0DCEB260008V", "CHH0DCEB260003V"],
    "Manulife": ["0046M01_2026", "0047M01_2026", "0048M01_2026"],
}
SRC = "Nguyên văn văn bản"
INT = "Diễn giải (văn bản không ghi tiếng Anh)"

# (abbr, english, english_status, vietnamese, group, companies, search_regex, visual_scan_pages, market_equivalent, note)
#   companies: list các hãng; "Chung" = chung toàn ngành / thuật ngữ dự án (không tìm trong PDF)
E = [
    # ---------------- Chỉ số ----------------
    ("FYP", "First Year Premium", INT, "Phí bảo hiểm thực thu năm thứ nhất", "Chỉ số", ["AIA", "Chubb", "Manulife"], r"\bFYP\b", [5, 6, 12, 13],
     "APE (phí quy năm) — tương đương khi quy đổi kỳ đóng phí", "Manulife: gồm phí cơ bản + bổ trợ + 6% phí đóng một lần, trừ HĐ bị hủy trong 21 ngày [0048M01_2026 : 6]"),
    ("FYC", "First Year Commission", INT, "Hoa hồng thực thu năm thứ nhất", "Chỉ số", ["AIA", "Chubb", "Manulife"], r"\bFYC\b", [7, 8],
     "First-year commission — thước đo năng suất đại lý", "Repo giả định FYC ≈ 30% FYP (A1) vì thiếu biểu hoa hồng theo sản phẩm"),
    ("FYC tín chỉ", "Credited First Year Commission", INT, "FYC dùng để xét thưởng / chỉ tiêu ở AIA", "Chỉ số", ["AIA"], r"FYC\s+[Tt]ín\s+[Cc]hỉ", [],
     "Weighted / credited FYC", "Cách quy đổi nằm ở memo riêng của AIA, không có trong 9 PDF; repo coi = FYC"),
    ("SYC", "Second Year Commission", INT, "Hoa hồng năm thứ hai (phí tái tục năm 2)", "Chỉ số", ["AIA"], r"\bSYC\b", [],
     "Renewal commission Y2", "AIA trả thưởng chất lượng phục vụ theo % SYC quý"),
    ("RYC", "Renewal Year Commission", INT, "Hoa hồng tái tục (từ năm hợp đồng thứ 2)", "Chỉ số", ["Chubb"], r"\bRYC\b", [9, 10],
     "Renewal commission", "Chubb tính phí/thưởng duy trì trên RYC năm 2–5"),
    ("K2", "Year-2 Persistency Ratio", INT, "Tỷ lệ duy trì hợp đồng năm thứ 2", "Chỉ số", ["Chubb"], r"\bK2\b", [7, 9, 10, 12, 13],
     "13/25-month persistency (canonical: K2)", "Công thức K2 của Chubb nằm ở 260005V (không có trong 9 PDF)"),
    ("TLDTHD", "Year-2 Policy Persistency Ratio", INT, "Tỷ lệ duy trì hợp đồng năm 2 (Manulife)", "Chỉ số", ["Manulife"], r"TLDTHD", [],
     "K2", "Công thức ở 0016M03/2024 (không có trong 9 PDF); hệ số nhân đổi bảng từ 04/2026"),
    ("FY", "AIA FY Persistency Ratio", INT, "Tỷ lệ duy trì phí AIA FY (14 tháng)", "Chỉ số", ["AIA"], r"\bFY\b", [],
     "K2 / 13-month persistency", "Ví dụ tính FY: phí thực thu ÷ phí phải thu (2604-069 mục VII)"),
    ("TOT", "AIA TOT Persistency Ratio", INT, "Tỷ lệ duy trì tổng phí AIA TOT", "Chỉ số", ["AIA"], r"\bTOT\b", [],
     "Total-premium persistency", "Phí năm CQL trả chậm cần TOT ≥85% tại thời điểm chi trả"),
    ("P13", "13th-month Persistency", INT, "Tỷ lệ duy trì tháng 13", "Chỉ số", ["Chubb"], r"\bP13\b", [],
     "13-month persistency", "Chubb dùng K2 hoặc trung bình P13 3 tháng để xét thăng/giữ cấp"),
    ("EHC", "— (định nghĩa ở 260005V, không có trong 9 PDF)", INT, "Lượt/đại lý đạt chuẩn hoạt động trong tháng (Chubb)", "Chỉ số", ["Chubb"], r"\bEHC\b", [6, 12, 13],
     "Active agent (monthly)", "Định nghĩa chi tiết ở CHH0DCEB260005V — không có trong nguồn"),
    ("3MAA", "3-Month Active Agent", INT, "Đại lý chính thức còn làm việc và đạt EHC ít nhất 1 lần trong 3 tháng gần nhất", "Chỉ số", ["Chubb"], r"\b3MAA\b", [7, 14],
     "Active agents (3-month window)", "Định nghĩa nguyên văn ở [CHH0DCEB260003V : 14] (mục V.10). KHÔNG phải \"bình quân 3 tháng\""),
    ("1mAA", "1-Month Active Agent", INT, "Số lượt đại lý có hoạt động trong tháng", "Chỉ số", ["AIA", "Manulife"], r"\b1mAA", [],
     "Monthly active agents", "Manulife 1mAA_4mFYC: đại lý ≥1 HĐ thực cấp và ≥4tr FYC trong tháng [0048M01_2026 : 6]"),
    ("CC", "Case Count", INT, "Số hợp đồng thực cấp (đã trừ hủy / từ chối)", "Chỉ số", ["Manulife"], r"\bCC\b", [],
     "Net issued cases", "Định nghĩa ở [0046M01_2026 : 10]"),
    ("NTT", "Direct Team", INT, "Nhóm trực tiếp (Chubb)", "Chỉ số", ["Chubb"], r"\bNTT\b", [],
     "Direct team / F1", "FYC NTT của AL không gồm FYC của chính AL"),
    ("FNA", "Financial Needs Analysis", INT, "Gặp khách hàng có phân tích nhu cầu tài chính", "Chỉ số", ["Chubb"], r"\bFNA\b", [],
     "Needs-based selling activity", "Chỉ tiêu Champion Hubb: 20 FNA/tháng"),
    ("SOP", "Standard Operating Procedure (hoạt động chuẩn)", INT, "Tỷ lệ tham dự hoạt động chuẩn (Champion Hubb)", "Chỉ số", ["Chubb"], r"\bSOP\b", [],
     "Activity discipline", "Hệ số W1 theo % tham dự SOP; có mâu thuẫn bảng vs ví dụ (ERR-DOC-01)"),
    ("MDRT", "Million Dollar Round Table", INT, "Danh hiệu quốc tế cho tư vấn viên doanh số cao", "Chỉ số", ["AIA", "Manulife"], r"\bMDRT\b", [],
     "MDRT", "Manulife dùng MDRT cho mức thưởng xuất sắc ≥120tr FYP"),
    ("APE", "Annualised Premium Equivalent", INT, "Phí bảo hiểm quy năm", "Chỉ số", ["Chung"], None, [],
     "APE", "Thuật ngữ chung toàn ngành; tìm thấy trong 9 PDF chỉ ở dạng liệt kê chỉ số (nếu có)"),
    ("VNB", "Value of New Business", INT, "Giá trị hợp đồng mới (lợi nhuận kỳ vọng của hợp đồng mới)", "Chỉ số", ["Chung"], None, [],
     "VNB margin", "Không có trong 9 PDF; dùng ở Giai đoạn 2 (ROI) — số VNB thật là UNKNOWN"),
    ("ROI", "Return on Investment", INT, "Hiệu quả trên chi phí bỏ ra", "Chỉ số", ["Chung"], None, [],
     "ROI", "Đề bài yêu cầu; repo chỉ có chi phí mô phỏng, không phải ROI thực tế"),
    ("MAPA", "Manpower × Active × Productivity × Average case size", INT, "Công thức doanh số: nhân lực × tỷ lệ hoạt động × năng suất × quy mô hợp đồng", "Chỉ số", ["Chung"], None, [],
     "Agency sales driver tree", "Thuật ngữ nội bộ của bài phân tích (cây động lực doanh số)"),
    ("OpEx", "Operating Expenses", INT, "Chi phí vận hành văn phòng của công ty", "Chỉ số", ["Chung"], None, [],
     "OpEx", "Không có trong 9 PDF; repo giả định 15–25% FYP"),
    # ---------------- Khoản thu nhập ----------------
    ("HT KTN", "Team Production Support Fee", INT, "Phí dịch vụ hỗ trợ khai thác nhóm (Chubb AL)", "Khoản thu nhập", ["Chubb"], r"HT\s*KTN", [],
     "Direct override (F1)", "Tháng: FYC NTT × 10–60% × hệ số K2; quý: thêm 30–50%"),
    ("HQKD", "Personal Business Performance Bonus", INT, "Thưởng hiệu quả kinh doanh cá nhân (Chubb)", "Khoản thu nhập", ["Chubb"], r"HQKD", [],
     "Production bonus", "Tháng theo FYC 3 tháng × K2; quý ×15–30% theo EHC"),
    ("CLKD", "Business Quality Multiplier", INT, "Hệ số nhân chất lượng kinh doanh (kỷ luật) — Manulife", "Khoản thu nhập", ["Manulife"], r"CLKD", [],
     "Compliance multiplier", "Thư nhắc nhở 50%; cảnh cáo / chấm dứt = 0"),
    ("KDXS", "Annual Business Excellence Bonus", INT, "Thưởng kinh doanh xuất sắc năm (Manulife)", "Khoản thu nhập", ["Manulife"], r"K[DS]X?S|KDSX", [],
     "Annual bonus (deferred)", "Chỉ cho Manulife Pro Vàng trở lên; trả 50/30/20% trong 3 năm"),
    ("M-Star", "M-Star", SRC, "Thưởng theo tiến độ FYP lũy kế (Manulife)", "Khoản thu nhập", ["Manulife"], r"M-?[Ss]tar", [],
     "Sales contest bonus", "Quý: ≥160/430/750/1.073,6tr FYP lũy kế"),
    ("JFW", "Join-field-work", SRC, "Doanh số làm việc kèm thực địa (AIA)", "Khoản thu nhập", ["AIA"], r"\bJFW\b", [],
     "Joint field work credit", "Phí dịch vụ JFW tính riêng với phí tuyển dụng hiệu quả"),
    ("Override", "Override", INT, "Phí quản lý tính theo % doanh số / phí của nhóm do mình quản lý", "Khoản thu nhập", ["Chung"], None, [],
     "Management override", "Thuật ngữ chung; mỗi hãng gọi khác: phí dịch vụ tuyển dụng (AIA), HT KTN (Chubb), phí năng suất nhóm (Manulife)"),
    # ---------------- Chức danh ----------------
    ("CVTV", "— (AIA dùng \"SA\")", INT, "Chuyên viên Tư vấn (AIA)", "Chức danh", ["AIA"], r"\bCVTV\b", [],
     "Tầng 1 — Đại lý cá nhân", "\"SA\" là Chuyên viên Tư vấn (viết tắt CVTV) [AIAVAD 2604-069 : 17]"),
    ("SA (AIA)", "— (văn bản không ghi tiếng Anh)", INT, "Chuyên viên Tư vấn — đại lý cá nhân AIA Alpha", "Chức danh", ["AIA"], r"\bSA\b", [],
     "Tầng 1 — Đại lý cá nhân", "Lên UM cần ≥2 người tuyển/6 tháng, FYC toàn nhánh 6T ≥50tr"),
    ("SA (Manulife)", "Servicing Agent", INT, "Đại lý phục vụ (Manulife)", "Chức danh", ["Manulife"], r"\bSA\b", [],
     "Tầng 1C — Đại lý phục vụ", "Quy định ở 01M02/2024/AO (không có trong 9 PDF); được tính vào 1mAA_4mFYC"),
    ("SE", "— (văn bản không ghi tiếng Anh)", INT, "Chuyên viên Tư vấn Hỗ trợ phục vụ (AIA)", "Chức danh", ["AIA"], r"\bSE\b", [],
     "Tầng 1C — Đại lý phục vụ", "SA/UM+ không đạt duy trì → SE nếu phục vụ ≥3 HĐ, phí quy năm ≥20tr"),
    ("Exchange", "Exchange", SRC, "Chuyên viên Hoạch định Tài chính (AIA)", "Tuyến hợp đồng", ["AIA"], r"\bExchange\b", [],
     "Tầng 1B — Đại lý toàn thời gian", "Gói trợ cấp riêng không có trong 9 PDF"),
    ("Exchange Pro", "Exchange Pro", SRC, "Chuyên viên Hoạch định Tài chính Cấp cao (AIA)", "Tuyến hợp đồng", ["AIA"], r"Exchange\s+Pro", [],
     "Tầng 1B — Đại lý toàn thời gian", "Tính 2 lượt hoạt động; phí đồng hành cho CQL 40%"),
    ("CQL", "— (văn bản không ghi tiếng Anh)", INT, "Cấp Quản Lý (AIA): UM, SUM, DM, SDM", "Chức danh", ["AIA"], r"\bCQL\b", [],
     "Tầng 2 — Quản lý trực tiếp", "Ký Hợp đồng Đại lý + Hợp đồng Dịch vụ Quản lý Đại lý"),
    ("UM+", "— (văn bản không ghi tiếng Anh)", INT, "Nhóm cấp quản lý: AIA = UM/SUM/DM/SDM; Manulife = Quản Lý Đại Lý", "Chức danh", ["AIA", "Manulife"], r"UM\+", [],
     "Tầng 2 — Quản lý trực tiếp", "Manulife: biểu phí 0047M01, ký HĐDV QLĐL"),
    ("UM", "Unit Manager", INT, "Trưởng nhóm kinh doanh (AIA: có chỗ gọi Trưởng Phòng Kinh Doanh — mâu thuẫn tên)", "Chức danh", ["AIA", "Chubb", "Manulife"], r"\bUM\b(?!\+)", [],
     "Tầng 2 — Quản lý cấp 1", "AIA: CONFLICTING EVIDENCE về tên tiếng Việt (2601-034 tr.2 vs 2604-069 tr.17)"),
    ("SUM", "Senior Unit Manager", INT, "Trưởng nhóm kinh doanh cấp cao (AIA)", "Chức danh", ["AIA"], r"\bSUM\b", [],
     "Tầng 2 — Quản lý cấp 1", "Lên SUM: 9 lượt hoạt động 3T, FYC toàn nhánh 6T ≥100tr"),
    ("SM (Chubb)", "Sales Manager", INT, "Trưởng Ban Kinh doanh (Chubb AL)", "Chức danh", ["Chubb"], r"\bSM\b", [],
     "Tầng 2 — Quản lý cấp 2", "Lên SM cần ≥1 AL báo cáo trực tiếp"),
    ("DM", "District Manager", INT, "AIA: Trưởng Phòng Kinh Doanh (có chỗ gọi Giám Đốc Ban); Chubb: cấp AL cao nhất", "Chức danh", ["AIA", "Chubb"], r"\bDM\b", [],
     "Tầng 2 — Quản lý cấp 2/3", "Chubb DM nhận L1–L3; AIA DM cần ≥1 UM+ trực tiếp"),
    ("SDM", "Senior District Manager", INT, "Trưởng Phòng Kinh Doanh Cấp cao (AIA)", "Chức danh", ["AIA"], r"\bSDM\b", [],
     "Tầng 2 — Quản lý cấp cao nhất tuyến CQL", "Lên PAF cần ≥3 UM+ trực tiếp, FYP toàn nhánh 6T ≥1.200tr"),
    ("BM", "Branch Manager", INT, "Trưởng ban (thuật ngữ của bài toán)", "Chức danh", ["Chung"], None, [],
     "Tầng 2 — Quản lý cấp 2", "KHÔNG xuất hiện trong 9 PDF; tương ứng AIA SUM/SDM, Chubb SM/DM theo quy mô (xem 4 mốc)"),
    ("AR", "Agency Representative", INT, "Đại diện Kinh doanh (Chubb)", "Chức danh", ["Chubb"], r"\bAR\b", [],
     "Tầng 1 — Đại lý cá nhân", "\"Đại diện Kinh doanh (ĐDKD hay AR)\""),
    ("AL", "Agency Leader", INT, "Quản lý Kinh doanh (Chubb): UM, SM, DM", "Chức danh", ["Chubb"], r"\bAL\b", [],
     "Tầng 2 — Quản lý trực tiếp", "\"Quản lý Kinh doanh (QLKD hay AL)\""),
    ("AMD", "Agency Management and Development", SRC, "Ban Điều hành và Phát triển Kinh doanh (Chubb): BD, RD", "Chức danh", ["Chubb"], r"\bAMD\b", [3],
     "Tầng 3 — Lãnh đạo vùng", "Ký hợp đồng dịch vụ, có báo cáo nghiệm thu"),
    ("BD", "Business Director, Agency Development", SRC, "Giám đốc, Phát triển Kinh doanh (Chubb)", "Chức danh", ["Chubb"], r"\bBD\b", [3, 10, 11],
     "Tầng 3 — Lãnh đạo vùng (bậc 1)", "Lên BD từ DM có điều kiện; biểu phí BD KHÔNG có trong 9 PDF"),
    ("RD", "Regional Director, Agency Management and Development", SRC, "Giám đốc Vùng, Điều hành và Phát triển Kinh doanh (Chubb)", "Chức danh", ["Chubb"], r"\bRD\b", [3, 4, 5],
     "Tầng 3 — Lãnh đạo vùng", "Bổ nhiệm theo hợp đồng; 8 khoản phí dịch vụ"),
    ("PAF+", "— (văn bản không ghi tiếng Anh)", INT, "Nhóm Nhà Sáng lập (AIA): PAF → … → President", "Chức danh", ["AIA"], r"PAF\+", [],
     "Tầng 3 — Lãnh đạo vùng", "\"Con đường sự nghiệp kép\": vẫn nhận phí CQL trực tiếp, không nhận gián tiếp cấp 2–4"),
    ("PAF", "Pre-Agency Founder", INT, "Quyền Sáng lập khối (AIA) — bậc đầu tuyến PAF+", "Chức danh", ["AIA"], r"\bPAF\b(?!\+)", [],
     "Tầng 3 — Lãnh đạo vùng (bậc 1)", "KHÔNG phải \"Premier Agency Force\": văn bản gọi là Quyền Sáng lập khối [AIAVAD 2601-035 : 3]; phí cố định 20tr/tháng"),
    ("AF", "Agency Founder", INT, "Nhà Sáng lập khối (AIA)", "Chức danh", ["AIA"], r"\bAF\b", [],
     "Tầng 3 — Lãnh đạo vùng", "Lên AF: FYP 6T 2.500tr, 5 UM+ trực tiếp"),
    ("RF", "Regional Founder", INT, "Nhà Sáng lập vùng (AIA)", "Chức danh", ["AIA"], r"\bRF\b", [],
     "Tầng 3 — Lãnh đạo vùng", "Chỉ tiêu năm 1: 10.000tr FYP"),
    ("AFF", "— (văn bản không ghi tiếng Anh)", INT, "Chương trình tuyển dụng Cấp quản lý trực tiếp (AIA)", "Tuyến hợp đồng", ["AIA"], r"\bAFF\b", [],
     "Direct manager recruitment", "Chi tiết chương trình không có trong 9 PDF"),
    ("PSM+", "— (văn bản không ghi tiếng Anh)", INT, "Quản Lý Cấp Cao (Manulife): PSM/SM, PSSM/SSM", "Chức danh", ["Manulife"], r"PSM\+", [],
     "Tầng 3 — Lãnh đạo vùng", "Ký HĐDV QLCC; phí cơ bản 35tr / 45tr"),
    ("PSM / SM (Manulife)", "— (văn bản không ghi tiếng Anh)", INT, "Quản lý cấp cao bậc 1 (Manulife), phí cơ bản 35tr", "Chức danh", ["Manulife"], r"\bPSM/SM\b", [],
     "Tầng 3 — Lãnh đạo vùng", "Điều kiện bậc ở 0013M04/2024 (không có trong 9 PDF)"),
    ("PSSM / SSM", "— (văn bản không ghi tiếng Anh)", INT, "Quản lý cấp cao bậc 2 (Manulife), phí cơ bản 45tr", "Chức danh", ["Manulife"], r"PSSM/SSM", [],
     "Tầng 3 — Lãnh đạo vùng", "Cùng biểu phí với HKD3/4"),
    ("MBA Pro", "MBA Pro", SRC, "Danh hiệu của Quản Lý Đại Lý UM+ (Manulife): Bạc / Vàng / Bạch Kim", "Chức danh", ["Manulife"], r"MBA\s+Pro", [],
     "Manager quality title", "Tiêu chí ở 0050M01/2026 (không có); base case không có danh hiệu"),
    ("Manulife Pro", "Manulife Pro", SRC, "Danh hiệu đại lý Manulife: Bạc / Vàng / Bạch Kim", "Chức danh", ["Manulife"], r"Manulife\s+Pro", [],
     "Agent quality title", "Tiêu chí ở 0011M04/2024 (không có)"),
    # ---------------- Đề xuất W24 (Giai đoạn 2) — PROPOSAL, không có trong 9 PDF ----------------
    ("Hybrid", "Hybrid Scheme", INT, "Chính sách Lai VN 2026 (đề xuất W24): 2 đường ray Full-time / Part-time, chốt K2 ≥80%, trần tổng chi 75% FYP", "Đề xuất W24", ["Chung"], None, [],
     "Hybrid compensation design", "PROPOSAL — tham số ở model/compensation/hybrid_scheme.py; báo cáo 03_De_Xuat_Chinh_Sach_Lai_VN2026.md"),
    ("Regional Tiering", "Regional Tiering", INT, "Phân vùng hệ số quota: Vùng 1 100%, Vùng 2 82,5%, Vùng 3 67,5%; giữ nguyên số hợp đồng và K2", "Đề xuất W24", ["Chung"], None, [],
     "Geographic quota adjustment", "PROPOSAL của TJ; hệ số giãn mọi ngưỡng FYP/FYC, không đổi tỷ lệ %"),
    ("Full-time", "Full-time committed track", INT, "Đường ray đại lý cam kết: trợ cấp 3tr/tháng khi đạt quota vùng, ≥2 HĐ/tháng và K2 ≥80%", "Đề xuất W24", ["Chung"], None, [],
     "Tầng 1B — Đại lý toàn thời gian", "Phần cố định duy nhất của đại lý trong Chính sách Lai"),
    ("Part-time", "Part-time variable track", INT, "Đường ray thuần biến phí: thưởng tháng 70% bậc Song Hành, không trợ cấp", "Đề xuất W24", ["Chung"], None, [],
     "Tầng 1 — Đại lý cá nhân", "Không phát sinh định phí cho người bán không đều"),
    ("Quota", "Sales quota", INT, "Chỉ tiêu FYP tối thiểu mỗi tháng (Vùng 1: 30tr) để nhận trợ cấp Full-time", "Đề xuất W24", ["Chung"], None, [],
     "Sales target", "Nhân hệ số vùng: Vùng 2 24,8tr; Vùng 3 20,2tr"),
    ("Rubric", "Scoring rubric", INT, "Thang chấm 5 trụ cột (DEC-19): doanh số 30%, chất lượng 30%, chi phí/ROI 30%, đơn giản 10%; vận hành & pháp lý chỉ tham khảo (0%); cổng Điều 52 và trần 75% xét trước", "Đề xuất W24", ["Chung"], None, [],
     "Compensation design scorecard", "4 trụ cột tính bằng công thức; Vận hành & Pháp lý là đánh giá, không cộng vào tổng; điểm Chính sách Đề xuất 2026 là tự chấm"),
    # ---------------- Tuyến hợp đồng ----------------
    ("HKD", "— (văn bản không ghi tiếng Anh)", INT, "Hộ Kinh Doanh (Manulife) — lãnh đạo ký hợp đồng như một đơn vị kinh doanh", "Tuyến hợp đồng", ["Manulife"], r"\bHKD\b", [],
     "Tầng 3B — Pháp nhân đối tác", "Cùng biểu phí với PSM+; tự xuất hóa đơn, tự chịu thuế [0048M01_2026 : 5-6]"),
    ("HĐDV QLĐL", "— (văn bản không ghi tiếng Anh)", INT, "Hợp đồng Dịch vụ Quản Lý Đại Lý (Manulife UM+)", "Tuyến hợp đồng", ["Manulife"], r"HĐDV\s+QLĐL", [],
     "Manager service contract", "Công ty tạm khấu trừ TNCN"),
    ("HĐDV QLCC", "— (văn bản không ghi tiếng Anh)", INT, "Hợp đồng Dịch vụ Quản lý Đại lý dành cho Quản Lý Cấp Cao (Manulife PSM+)", "Tuyến hợp đồng", ["Manulife"], r"HĐDV\s+QLCC", [],
     "Senior manager service contract", "Có thể chuyển đổi qua lại với HĐDV HKD, bảo lưu kết quả"),
    ("Champion Hubb", "Champion Hubb", SRC, "Chương trình đại lý/quản lý chuyên nghiệp có kỷ luật hoạt động (Chubb)", "Tuyến hợp đồng", ["Chubb"], r"Champion\s+Hubb", [],
     "Tầng 1B / 2 — chương trình toàn thời gian", "AL chỉ chọn 1 trong 2 vai trò: Cá nhân hoặc Quản lý"),
    ("GTF", "— (văn bản không ghi tiếng Anh)", INT, "Chương trình Phát Triển Quản Lý Đại Lý (Manulife UM+ GTF)", "Tuyến hợp đồng", ["Manulife"], r"\bGTF\b", [],
     "Manager development program", "Không tính phí phát triển nhóm mới trên UM+ GTF; quy định ở 0004M04/2024 (không có)"),
]


def load_pages():
    reg = {r["Source_ID"]: r for r in csv.DictReader(open(REPO / "knowledge/sources/source-registry.csv", encoding="utf-8"))}
    return {fid: {"sid": sid, "pages": [p.get_text() for p in pymupdf.open(REPO / reg[sid]["Local_Relative_Path"])]}
            for fid, sid in FILE_IDS.items()}


def build():
    pages = load_pages()
    out = []
    for abbr, en, en_st, vi, group, comps, rx, scan_pages, mkt, note in E:
        cites = []
        if rx:
            pat = re.compile(rx)
            for co in comps:
                for fid in COMPANY_FILES.get(co, []):
                    if fid == SCAN_ID:
                        if scan_pages:
                            cites.append({"company": co, "file_id": fid, "source_id": pages[fid]["sid"], "page": scan_pages[0], "method": "visual_scan"})
                        continue
                    hit = next((i + 1 for i, t in enumerate(pages[fid]["pages"]) if pat.search(t)), None)
                    if hit:
                        cites.append({"company": co, "file_id": fid, "source_id": pages[fid]["sid"], "page": hit, "method": "text_search"})
            if not cites:
                raise SystemExit(f"glossary: '{abbr}' not found in any declared file — fix regex or mark as Chung")
        if comps == ["Chung"]:
            cam = "Chung toàn ngành / thuật ngữ dự án (không có trong 9 PDF)"
        else:
            parts = []
            for co in comps:
                cs = [c for c in cites if c["company"] == co]
                if cs:
                    first = cs[0]
                    parts.append(f"{co} [{first['file_id']} : {first['page']}]")
            cam = " · ".join(parts)
        item = {"abbr": abbr, "english": en, "vietnamese": vi, "company_and_memo": cam, "market_equivalent": mkt, "note": note,
                "group": group, "companies": comps, "english_status": en_st, "citations": cites}
        for k in ("abbr", "english", "vietnamese", "company_and_memo", "market_equivalent", "note"):
            if not str(item[k]).strip():
                raise SystemExit(f"glossary: empty field {k} for {abbr}")
        out.append(item)
    return {"$comment": "Nguồn duy nhất cho từ điển & tooltip trên trang HTML. Sinh bởi scripts/build_glossary.py; trang trích dẫn tự tìm trên text 9 PDF "
                        "(bản scan CHH0DCEB260003V: đối chiếu bằng mắt). english_status = 'Diễn giải' khi văn bản không ghi tên tiếng Anh.",
            "required_fields": ["abbr", "english", "vietnamese", "company_and_memo", "market_equivalent", "note"],
            "entries": out}


def main() -> None:
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(data['entries'])} entries)")


if __name__ == "__main__":
    main()
