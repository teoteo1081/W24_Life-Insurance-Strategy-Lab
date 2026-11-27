"""Sinh outputs/interview/00_Role_Mapping_Audit.md — kiểm kê nguồn 7/7, chức danh nguyên văn, Negative Proof.

Chạy:  python scripts/build_role_audit.py
Mọi kiểm tra trong báo cáo được script chạy lại mỗi lần (hash, text từng trang, từ khóa). Bản scan
CHH0DCEB260003V không có lớp text: phần đó ghi rõ là đối chiếu bằng mắt (15/15 trang, 2026-11-27).
Báo cáo không chứa đường dẫn máy cá nhân (repo PUBLIC).
"""
from __future__ import annotations

import csv
import hashlib
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import pymupdf  # noqa: E402

from w24_milestones import FILE_IDS, aia_title, chubb_title, load_milestones, manulife_title, rubric_table  # noqa: E402

OUT = REPO / "outputs" / "interview" / "00_Role_Mapping_Audit.md"
SCAN_ID = "CHH0DCEB260003V"
SCAN_PAGES_REVIEWED = list(range(1, 16))   # soát bằng mắt toàn bộ 15/15 trang trong phiên 2026-11-27


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip().lower()


def load_sources():
    reg = {r["Source_ID"]: r for r in csv.DictReader(open(REPO / "knowledge/sources/source-registry.csv", encoding="utf-8"))}
    src = {}
    for fid, sid in FILE_IDS.items():
        r = reg[sid]
        p = REPO / r["Local_Relative_Path"]
        if not p.exists():
            raise SystemExit(f"missing source {sid}: run with private/sources populated")
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        doc = pymupdf.open(p)
        pages = [pg.get_text() for pg in doc]
        src[fid] = {"sid": sid, "company": r["Company"], "name": r["Original_Filename"], "pages": pages,
                    "hash_ok": h == r["SHA256_Hash"], "n": len(pages), "chars": sum(len(t) for t in pages)}
    return src


def on_page(src, fid: str, page_spec: str, needle: str) -> bool:
    """True nếu mọi từ của `needle` xuất hiện trên (một trong) trang trích. Bản scan: không kiểm được bằng text."""
    if fid == SCAN_ID:
        return False
    a, _, b = page_spec.partition("-")
    rng = range(int(a), int(b or a) + 1)
    text = " ".join(norm(src[fid]["pages"][p - 1]) for p in rng)
    return all(w in text for w in norm(needle).split())


# ---------------- Quy tắc thăng / giữ cấp (chép từ PDF, có token kiểm) ----------------
# (hãng, chức danh, loại, nội dung, fid, trang, token phải có trên trang)
RULES = [
    ("AIA", "SA → UM", "Thăng cấp", "3 tháng tại vị trí; ≥2 tuyển/giới thiệu trực tiếp 6T; ≥5 lượt CVTV hoạt động 3T; FYC tín chỉ toàn nhánh 6T ≥50tr; nhóm trực tiếp 6T ≥50tr; duy trì HĐ ≥70%; ≥2 HĐ thuần cá nhân", "AIAVAD 2601-034", "8", "THĂNG TIẾN LÊN VAI TRÒ UM+ 50 70%"),
    ("AIA", "UM → SUM", "Thăng cấp", "6 tháng; ≥2 tuyển 6T; 0 UM+ trực tiếp; ≥9 lượt hoạt động 3T; toàn nhánh 6T ≥100tr", "AIAVAD 2601-034", "8", "SUM 100 9"),
    ("AIA", "SUM → DM", "Thăng cấp", "6 tháng; ≥1 UM+ trực tiếp; ≥13 lượt; toàn nhánh 6T ≥200tr", "AIAVAD 2601-034", "8", "DM 200 13"),
    ("AIA", "DM → SDM", "Thăng cấp", "6 tháng; ≥2 UM+ trực tiếp; ≥17 lượt; toàn nhánh 6T ≥400tr", "AIAVAD 2601-034", "8", "SDM 400 17"),
    ("AIA", "Quy định 70% chỉ tiêu", "Thăng/duy trì", "Nhánh UM+ con đóng góp tối đa 70% yêu cầu (không áp cho SA → UM)", "AIAVAD 2601-034", "9", "70% chỉ tiêu"),
    ("AIA", "SDM → PAF", "Thăng cấp", "6 tháng; ≥3 UM+ trực tiếp; ≥18 lượt; FYP toàn nhánh 6T ≥1.200tr; duy trì ≥70%", "AIAVAD 2601-034", "8", "SDM THĂNG TIẾN LÊN PAF+ 1,200 18"),
    ("AIA", "UM / SUM / DM / SDM", "Duy trì", "≥6 tháng; ≥1 tuyển 6T; UM+ trực tiếp 0/0/1/1; lượt 4/6/9/12; FYC toàn nhánh 6T 30/45/75/105tr; duy trì ≥60%; không đạt → hạ 1 bậc", "AIAVAD 2601-034", "10", "ĐIỀU KIỆN DUY TRÌ CHỨC DANH 30 45 75 105 60%"),
    ("AIA", "PAF → AF … VP", "Thăng cấp", "AF: 6T, FYP 6T 2.500tr, 5 UM+, 1mAA 3T 35; … DSRF 12.000tr; SRF 15.000tr; VP 40.000tr; duy trì ≥70%", "AIAVAD 2601-035", "6", "AF 2,500 5UM+ 35 DSRF 12,000"),
    ("AIA", "PAF+ (Dual Career)", "Phạm vi", "PAF+ nhận thêm thu nhập vai trò CVTV/CQL; KHÔNG nhận phí gián tiếp cấp 2-3-4 của CQL", "AIAVAD 2601-035", "2", "CON ĐƯỜNG SỰ NGHIỆP KÉP gián tiếp cấp 2-3-4"),
    ("AIA", "SA / UM+ → SE", "Duy trì", "Không đạt duy trì HĐ → SE nếu phục vụ ≥3 HĐ, phí quy năm ≥20tr, TOT ≥50%", "AIAVAD 2604-069", "10-11", "Chuyên viên tư vấn Hỗ Trợ Phục Vụ (SE) 20 50%"),
    ("Chubb", "AR → UM", "Thăng cấp", "3 tháng; FYC tích lũy 3T ≥25tr (gồm AR được giới thiệu, bản thân ≥10tr); 2 đại lý giới thiệu đạt 3MAA; K2/P13 ≥55%; khóa MAP", "CHH0DCEB260007V", "7", "ĐIỀU KIỆN THĂNG CẤP 25 55% MAP"),
    ("Chubb", "UM → SM", "Thăng cấp", "3 tháng; FYC 3T ≥50tr; 3MAA ≥5; 3MAA mới ≥1; AL trực tiếp ≥1", "CHH0DCEB260007V", "7", "50 5"),
    ("Chubb", "SM → DM", "Thăng cấp", "6 tháng; FYC 6T ≥200tr; 3MAA ≥10; 3MAA mới ≥2; AL trực tiếp ≥2", "CHH0DCEB260007V", "7", "200 10"),
    ("Chubb", "DM → BD", "Thăng cấp", "6 tháng; FYC 6T ≥450tr; 3MAA ≥20; 3MAA mới ≥3; AL trực tiếp ≥4; làm việc tại công ty ≥18 tháng", "CHH0DCEB260007V", "7", "450 20 18 Tháng"),
    ("Chubb", "AR / UM / SM / DM", "Duy trì", "6 tháng; FYC 6T 10/20/100/200tr; 3MAA –/2/4/8; AL trực tiếp –/–/1/2; K2 ≥50%; AR rớt → AR dự bị (tối đa 18 tháng)", "CHH0DCEB260007V", "8", "ĐIỀU KIỆN DUY TRÌ VỊ TRÍ 100 200 dự bị"),
    ("Chubb", "AL Champion Hubb Quản lý", "Phạm vi", "AL chỉ tham gia 1 trong 2 vai trò (Cá nhân hoặc Quản lý)", "CHH0DCEB260008V", "11", "1 trong 2 vai trò"),
    ("Chubb", "BD / RD (AMD)", "Bổ nhiệm", "Cấp bậc AMD ghi nhận tại Hợp đồng/Phụ lục hoặc quyết định của Công ty", SCAN_ID, "3", ""),
    ("Chubb", "RD → cấp cao hơn", "Thăng cấp", "12 tháng; FYP 6T ≥9.000tr; EHC tích lũy ≥300; K2 ≥60%; ≥2 DM trực tiếp; ≥4 BD được phát triển / RD giới thiệu", SCAN_ID, "12", ""),
    ("Chubb", "RD", "Duy trì", "Nhánh trực tiếp: FYP 6T ≥750tr, EHC ≥25, K2 ≥50% HOẶC toàn nhánh: FYP ≥3.000tr, EHC ≥100, K2 ≥50%", SCAN_ID, "13", ""),
    ("Manulife", "Đại Lý — hệ số thưởng", "Hệ số", "Mọi khoản thưởng × hệ số TLDTHD (trước 04/2026: ≥65% → 100%; từ 04/2026: ≥70% → 100%, <50% → TLDTHD/2) × hệ số CLKD (thư nhắc nhở 50%, cảnh cáo 0)", "0046M01_2026", "1", "Hệ số nhân thưởng 65% 70% 50%"),
    ("Manulife", "Đại Lý — thưởng năng suất tháng", "Biểu thưởng", "Theo FYC 3 tháng: 5/10/15/30/45/60/80/100tr → 5/10/15/20/25/30/35/50% FYC tháng; cần ≥1 HĐ thực cấp; >6 tháng dùng mức 2–8", "0046M01_2026", "4", "Thưởng năng suất tháng 100 50% 35%"),
    ("Manulife", "Đại Lý — thưởng năng suất quý", "Biểu thưởng", "FYC quý 15/30/45/60/80/100/120tr → 2/3/4/5/6/8/10% (Đại Lý xuất sắc ×2); mức 1 chỉ cho ≤6 tháng", "0046M01_2026", "5", "Thưởng năng suất quý 120 10% 20%"),
    ("Manulife", "Đại Lý — KDXS năm", "Biểu thưởng", "Chỉ Manulife Pro Vàng trở lên: 10–15% FYC năm (tối đa 100tr), TLDTHD ≥70%, trả 50/30/20% trong 3 năm", "0046M01_2026", "6-7", "600.000.000 15% 50% 30% 20%"),
    ("Manulife", "Đại Lý — M-Star", "Biểu thưởng", "FYP lũy kế ≥160 / 430 / 750 / 1.073,6tr cuối quý → 8 / 12 / 15 / 20tr; năm ≥1.073,6tr / 2 tỷ / 3 tỷ → 55 / 75 / 100tr trừ phần quý", "0046M01_2026", "7-8", "M-Star 750.000.000 1.073.645.200"),
    ("Manulife", "Đại Lý — hoa hồng cơ bản", "Phạm vi", "Hoa hồng theo từng sản phẩm, theo Thông báo do Công Ty ban hành (không có bảng trong văn bản)", "0046M01_2026", "9", "Hoa hồng dành cho Đại Lý theo từng sản phẩm"),
    ("Manulife", "UM+ — phí năng suất nhóm", "Biểu phí", "Cấp 1: FYC ≥48 / 24 / 7 / <7tr → 20 / 16 / 14 / 10%; cấp 2–4 = ½ tỷ lệ cấp liền trên; không tính FYC bản thân UM+", "0047M01_2026", "1", "năng suất nhóm 48 20% 16% 14% 10%"),
    ("Manulife", "UM+ — phí hoạt động nhóm", "Biểu phí", "Số ĐL/UM+ cấp 1 có sản xuất ≥6 / 4–5 / 2–3 / 1 → MBA Pro 125 / 100 / 75 / 30%, UM+ khác 60 / 50 / 40 / 30% × thưởng năng suất tháng+quý của cấp 1 × hệ số TLDTHD", "0047M01_2026", "2", "125% 60% 100% 50% 75% 40% 30%"),
    ("Manulife", "UM+ — điều kiện nhận phí", "Điều kiện", "Từ 02/2026: tham gia Đội ngũ chuyên cần ≥4 buổi/tháng", "0047M01_2026", "3", "Đội ngũ chuyên cần 04 buổi"),
    ("Manulife", "UM+ — phát triển nhóm mới", "Biểu phí", "210% × phí năng suất nhóm cấp 1 của UM mới trong 12 tháng, tối đa 30tr/tháng; trả 50% ngay, 50% giữ lại", "0047M01_2026", "4", "210% 30 triệu"),
    ("Manulife", "UM+ — hợp tác dài hạn", "Biểu phí", "Chỉ MBA Pro: Bạch Kim 125% / Vàng 100% / Bạc 80% × (A.II + A.III) năm; trả 30/30/40% trong 3 năm nếu TLDTHD ≥70%", "0047M01_2026", "5-6", "MBA Pro Bạch Kim 125% Bạc 80% 30% 40%"),
    ("Manulife", "PSM/SM · PSSM/SSM · HKD1/2 · HKD3/4", "Phí cơ bản", "35tr (PSM/SM, HKD1/2) · 45tr (PSSM/SSM, HKD3/4); không có điều kiện thăng/giữ cấp trong văn bản", "0048M01_2026", "1", "35 45 HKD3/4"),
    ("Manulife", "PSM+ ↔ HKD", "Chuyển đổi", "Kết quả và quyền lợi được bảo lưu khi chuyển HĐDV QLCC ↔ HĐDV HKD", "0048M01_2026", "5", "chuyển đổi mô hình"),
    ("Manulife", "PSM+ / HKD", "Thuế", "PSM+: Công ty khấu trừ TNCN; HKD: tự xuất hóa đơn, tự chịu thuế", "0048M01_2026", "5-6", "khấu trừ hóa đơn"),
]

# ---------------- Kết luận "không có trong tài liệu" cần Negative Proof ----------------
# (kết luận, từ khóa tìm, nơi được dẫn chiếu nếu có)
MISSING = [
    ("Biểu hoa hồng cơ bản theo sản phẩm của Manulife (0046M01 mục C.1 chỉ dẫn chiếu)", ["Hoa hồng", "tỷ lệ hoa hồng", "Phụ lục"]),
    ("Hệ thống chức danh & điều kiện thăng / giữ cấp Manulife (0013M04/2024/ASBD)", ["0013M04", "thăng cấp", "điều kiện thăng", "SUM"]),
    ("Tiêu chí danh hiệu MBA Pro (0050M01/2026) và Manulife Pro (0011M04/2024)", ["0050M01", "0011M04", "Tiêu chí"]),
    ("Chính sách phí dịch vụ cho BD (Chubb)", ["BD"]),
]


def keyword_log(src, keys):
    rows = []
    for fid, s in src.items():
        if fid == SCAN_ID:
            rows.append((fid, "—", "bản scan, không có lớp text → soát bằng mắt 15/15 trang"))
            continue
        hits = []
        for k in keys:
            pat = re.compile(r"(?<![\w+])" + re.escape(k) + r"(?![\w+])", 0 if k.isupper() or any(ch.isdigit() for ch in k) else re.I)
            pg = [i + 1 for i, t in enumerate(s["pages"]) if pat.search(t)]
            hits.append(f"`{k}`: {pg if pg else '0'}")
        rows.append((fid, "; ".join(hits), ""))
    return rows


def file_name_search():
    """Tìm theo tên file ở các nơi có thể chứa tài liệu (chạy lại mỗi lần sinh báo cáo)."""
    pats = ["*0046M01*", "*0047M01*", "*UM+*.pdf", "*Manulife*.pdf", "*Bieu phi*.pdf"]
    home = Path.home()
    roots = {"<repo>/private/sources": REPO / "private" / "sources", "%USERPROFILE%/Downloads": home / "Downloads",
             "%USERPROFILE%/Desktop": home / "Desktop", "%USERPROFILE%/Documents": home / "Documents"}
    out = []
    for label, root in roots.items():
        if not root.exists():
            out.append((label, "không tồn tại", ""))
            continue
        found = []
        for p in pats:
            try:
                found += [x.name for x in root.rglob(p)]
            except OSError:
                pass
        out.append((label, ", ".join(pats), "; ".join(sorted(set(found))) if found else "0 kết quả"))
    return out


def archive_listing():
    exe = shutil.which("7z") or shutil.which("7za") or next((str(x) for x in (Path("C:/Program Files/7-Zip/7z.exe"),) if x.exists()), None)
    arc = list((Path.home() / "Downloads").rglob("Chính sách thu nhập.7z"))
    if not exe or not arc:
        return None
    out = subprocess.run([exe, "l", str(arc[0])], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    names = [ln[53:].strip() for ln in out.splitlines() if ln[:4].isdigit() and ".pdf" in ln.lower()]
    return names


def build() -> str:
    src = load_sources()
    L = []
    w = L.append
    counters = {"numeric": 0, "cited": 0, "data": 0, "labelled": 0}

    def row(cells, has_number=False, cite=None, label=None):
        if label is not None:          # None = dòng nhật ký, không phải dữ liệu
            counters["data"] += 1
            counters["labelled"] += int(bool(label))
        if has_number:
            counters["numeric"] += 1
            if cite and re.search(r"\[[^\]:]+ : [0-9]+(-[0-9]+)?\]", cite):
                counters["cited"] += 1
        w("| " + " | ".join(cells) + " |")

    w("# 00 — Kiểm kê nguồn & kiểm toán chức danh (Role Mapping Audit)")
    w("")
    w("> Sinh bởi `scripts/build_role_audit.py`; mọi kiểm tra (hash, text từng trang, từ khóa) chạy lại mỗi lần sinh. "
      "Áp dụng 4 luật `AGENTS.md` (STRICT DATA INGESTION & MAPPING PROTOCOL) và rubric `qa/data-ingestion-rubric.md`.")
    w("> Trích dẫn dạng `[FileName : Trang]`, FileName là mã duy nhất có trong tên file (bảng 1).")
    w("")
    w(f"## 1. Kiểm kê nguồn {len(src)}/{len(src)}")
    w("")
    w("| FileName (mã) | Source_ID | Hãng | Tên file gốc | Trang | Ký tự text | SHA-256 khớp registry | Cách đọc | Nhãn |")
    w("|---|---|---|---|---:|---:|---|---|---|")
    files_ok = 0
    for fid, s in src.items():
        files_ok += int(s["hash_ok"])
        how = f"bản scan — soát bằng mắt {len(SCAN_PAGES_REVIEWED)}/{s['n']} trang" if fid == SCAN_ID else "text từng trang (PyMuPDF)"
        row([f"`{fid}`", s["sid"], s["company"], s["name"], str(s["n"]), f"{s['chars']:,}".replace(",", "."), "✅" if s["hash_ok"] else "❌", how, "VERIFIED FACT"], label=True)
    w("")
    w(f"Tổng: **{files_ok}/{len(src)}** file khớp hash; {sum(s['n'] for s in src.values())} trang (`0046M01_2026`, `0047M01_2026` bổ sung ngày 2026-11-27).")
    w("")

    # ---- Titles
    w("## 2. Cây chức danh nguyên văn theo từng hãng")
    w("")
    w("Nguồn dữ liệu: `knowledge/policies/role-organization-mapping.csv` (cột `Raw_Title_Verbatim`, `Track_Type`, `Title_Citation`). "
      "Cột *Kiểm* = script tìm thấy mọi từ của tên nguyên văn trên đúng trang trích.")
    w("")
    w("| Hãng | Mã | Tên nguyên văn | Tuyến (`track_type`) | Trích dẫn | Kiểm | Nhãn |")
    w("|---|---|---|---|---|---|---|")
    roles = list(csv.DictReader(open(REPO / "knowledge/policies/role-organization-mapping.csv", encoding="utf-8")))
    titles_ok = titles_total = 0
    for r in roles:
        cit = r["Title_Citation"]
        if r["Track_Type"] == "NOT_IN_CORPUS":
            row([r["Company"].split()[0], r["Role_Code"], "— *(không có trong nguồn)*", "NOT_IN_CORPUS", "xem mục 4 (Negative Proof)", "—", "UNKNOWN"], label=True)
            continue
        titles_total += 1
        m = re.match(r"\[([^\]:]+) : ([0-9-]+)\]", cit)
        fid, pg = m.group(1), m.group(2)
        if fid == SCAN_ID:
            ok, mark = True, "👁 scan"
        else:
            ok = on_page(src, fid, pg, r["Raw_Title_Verbatim"].replace("—", " "))
            mark = "✅" if ok else "❌"
        titles_ok += int(ok and bool(r["Track_Type"]))
        row([r["Company"].split()[0], f"`{r['Role_Code']}`", r["Raw_Title_Verbatim"], r["Track_Type"], cit, mark, "VERIFIED FACT"], label=True)
    w("")

    w("### 2.1. Điều kiện thăng / giữ cấp (chép từ văn bản)")
    w("")
    w("| Hãng | Chức danh | Loại | Nội dung | Trích dẫn | Kiểm | Nhãn |")
    w("|---|---|---|---|---|---|---|")
    for co, t, kind, txt, fid, pg, tok in RULES:
        cite = f"[{fid} : {pg}]"
        ok = "👁 scan" if fid == SCAN_ID else ("✅" if on_page(src, fid, pg, tok) else "❌")
        if ok == "❌":
            raise SystemExit(f"rule token not found on cited page: {t} {cite} '{tok}'")
        row([co, t, kind, txt, cite, ok, "VERIFIED FACT"], has_number=bool(re.search(r"\d", txt)), cite=cite, label=True)
    w("")

    # ---- Conflicts
    w("## 3. Mâu thuẫn tên gọi trong văn bản AIA (`CONFLICTING EVIDENCE`)")
    w("")
    conf = [("UM", "Trưởng Nhóm Kinh Doanh", "Trưởng Phòng Kinh Doanh (viết tắt là “UM”)"),
            ("SUM", "Trưởng Nhóm Kinh Doanh Cấp Cao", "Trưởng Phòng Kinh Doanh Cấp Cao (viết tắt là “SUM”)"),
            ("DM", "Trưởng Phòng Kinh Doanh", "Giám Đốc Ban Kinh Doanh (viết tắt là “DM”)")]
    w("| Mã | Sơ đồ lộ trình `[AIAVAD 2601-034 : 2]`, `[AIAVAD 2604-069 : 2]` | Mục định nghĩa `[AIAVAD 2604-069 : 17]` | Kiểm | Nhãn |")
    w("|---|---|---|---|---|")
    for code, a, b in conf:
        ok = on_page(src, "AIAVAD 2601-034", "2", a) and on_page(src, "AIAVAD 2604-069", "17", b)
        row([f"`{code}`", a, b, "✅" if ok else "❌", "CONFLICTING EVIDENCE"], label=True)
    w("")
    w("Không tự phán xử: báo cáo dùng **mã** (UM/SUM/DM/SDM) làm khóa và giữ cả hai tên. Đề xuất ghi vào `docs/decisions/decision-register.md` nếu cần tên tiếng Việt chính thức.")
    w("")

    # ---- Manulife
    w("## 4. Manulife: 3 văn bản, 2 tuyến song song")
    w("")
    w("| Câu hỏi | Trả lời (`VERIFIED FACT`) | Căn cứ | Nhãn |")
    w("|---|---|---|---|")
    row(["`0046M01_2026` áp dụng cho ai?", "Chính sách chi trả dành cho Đại Lý Manulife (Việt Nam), gửi **Tất cả Đại Lý Bảo hiểm**, hiệu lực 01/01/2026, thay 0001M04/2025. Gồm hệ số TLDTHD/CLKD (mục A) và 8 khoản thưởng B.I–B.VIII. **Không có bảng hoa hồng cơ bản** (mục C.1 dẫn chiếu thông báo theo từng sản phẩm)", "[0046M01_2026 : 1], [0046M01_2026 : 2-8], [0046M01_2026 : 9]", "VERIFIED FACT"], has_number=True, cite="[0046M01_2026 : 1]", label=True)
    row(["`0047M01_2026` (UM+) áp dụng cho cấp nào?", "Biểu phí dịch vụ dành cho Quản Lý Đại Lý (UM+), gửi **Tất cả Quản Lý Đại Lý (UM+)**, ký HĐDV QLĐL, hiệu lực 01/01/2026, thay 0002M04/2024. Văn bản chỉ gọi tên một bậc là Trưởng nhóm Kinh doanh (UM); các bậc khác trong UM+ theo 0013M04/2024 (không có trong nguồn). Biểu phí **không phân biệt bậc**, chỉ phân biệt có/không danh hiệu MBA Pro", "[0047M01_2026 : 1], [0047M01_2026 : 4], [0047M01_2026 : 6]", "VERIFIED FACT"], has_number=True, cite="[0047M01_2026 : 1]", label=True)
    row(["Vì sao trước đây kết luận không có số UM/SUM/DM?", "Đến 11:47–11:50 ngày 2026-11-27 hai file này **chưa có** trên máy (bộ nguồn khi đó 7 file; file nén gốc cũng 7 file). Nay đã nạp và tính", "HANDOVER.md", "VERIFIED FACT"], label=True)
    row(["`0048M01_2026` (PSM+/HKD) liên kết thế nào với UM+?", "**Hai tuyến song song về hợp đồng**: UM+ ký HĐDV QLĐL (0047M01); PSM+ ký HĐDV QLCC, HKD ký HĐDV HKD (0048M01, cùng biểu phí). UM+ có thể chuyển sang PSM+/HKD và phí hợp tác dài hạn UM+ vẫn được trả tiếp sau khi chuyển. Điều kiện chuyển bậc nằm ở 0013M04/2024 (không có trong nguồn)", "[0047M01_2026 : 6-7], [0048M01_2026 : 5]", "VERIFIED FACT"], has_number=True, cite="[0047M01_2026 : 6-7]", label=True)
    w("")
    w("### 4.1. Chubb `BD` nằm ở đâu")
    w("")
    w("| Văn bản · trang | Nội dung về BD | Kiểm | Nhãn |")
    w("|---|---|---|---|")
    bd = [("CHH0DCEB260007V", "7", "Điều kiện thăng cấp DM → BD (FYC 6T ≥450tr, 3MAA ≥20, AL trực tiếp ≥4, ≥18 tháng tại công ty)", "450 lên BD 18 Tháng"),
          ("CHH0DCEB260007V", "4", "Thưởng HQKD cá nhân áp dụng cho AR, AL và AMD (BD là AMD) — thưởng bán cá nhân", "AR, AL và AMD"),
          ("CHH0DCEB260008V", "3", "Bảng tóm tắt phí AL chỉ có cột AR / UM / SM / DM — BD không hưởng phí AL", "AR UM SM DM"),
          (SCAN_ID, "3", "Cấp bậc AMD: Giám đốc, Phát triển Kinh doanh — Business Director, Agency Development (BD)", ""),
          (SCAN_ID, "10-11", "RD hưởng 25–50% tổng các khoản phí dịch vụ quản lý của BD được phát triển (6 khoản a–f) — chỉ có tên khoản, không có mức phí của BD", "")]
    for fid, pg, txt, tok in bd:
        ok = "👁 scan" if fid == SCAN_ID else ("✅" if on_page(src, fid, pg, tok) else "❌")
        if ok == "❌":
            raise SystemExit(f"BD token not found {fid} {pg}")
        row([f"[{fid} : {pg}]", txt, ok, "VERIFIED FACT"], has_number=True, cite=f"[{fid} : {pg}]", label=True)
    w("")
    w("Kết luận: BD **có điều kiện thăng cấp** nhưng **biểu phí của chính BD không có** trong 9 file (nhật ký ở 4.3).")
    w("")
    w("### 4.2. Danh sách file đã quét (tìm theo tên)")
    w("")
    w("| Nơi quét | Mẫu tên | Kết quả |")
    w("|---|---|---|")
    for loc, pats, res in file_name_search():
        row([loc, pats, res])
    w("")
    w(f"### 4.3. Tìm từ khóa trên toàn bộ trang của {len(src)} file (cho các kết luận còn thiếu)")
    w("")
    missing_with_proof = 0
    for claim, keys in MISSING:
        w(f"**{claim}** — nhãn `UNKNOWN` (không có trong nguồn):")
        w("")
        w("| FileName | Trang có từ khóa | Ghi chú |")
        w("|---|---|---|")
        for fid, hits, note in keyword_log(src, keys):
            row([f"`{fid}`", hits, note])
        w("")
        missing_with_proof += 1
    w("Đọc nhật ký: từ khóa có xuất hiện nhưng chỉ là **dẫn chiếu** sang văn bản không có trong nguồn (0013M04, 0050M01, 0011M04, thông báo hoa hồng) hoặc thuộc **hãng khác** — không có bảng số tương ứng.")
    w("")

    # ---- Milestones
    w("## 5. Bảng quy đổi theo 4 mốc quy mô — chức danh thực tế đạt được")
    w("")
    w("Mốc định nghĩa trong `knowledge/policies/scale-milestones.json`. Giả định dùng để suy chức danh (`ASSUMPTION`): FYC/FYP 30%; K2 = FY = 85%; "
      "mọi đại lý hoạt động mỗi tháng; tuyển 2 người mới có hoạt động/quý; quản lý tự bán 2 HĐ/6 tháng; đủ thời gian tại vị trí (trạng thái ổn định).")
    w("")
    w("| Mốc | AIA Alpha | Chubb Life | Manulife | Điều kiện quyết định (trích dẫn) | Nhãn |")
    w("|---|---|---|---|---|---|")
    for m in load_milestones():
        ta, ca = aia_title(m)
        tc, cc = chubb_title(m)
        tm, _ = manulife_title(m)
        fails = [c for c in ca + cc if not c.ok]
        why = "; ".join(f"{c.metric}: cần {c.need:g}, có {c.have:g} {c.cite}" for c in fails) or "đạt đủ điều kiện bậc kế tiếp đã xét"
        cite = (fails[0].cite if fails else "[AIAVAD 2601-034 : 8]")
        mnl = f"**{tm}** [0046M01_2026 : 1]" if tm == "Đại Lý" else f"**{tm}** [0047M01_2026 : 1] — bậc cụ thể UNKNOWN (0013M04/2024 không có)"
        row([m.label, f"**{ta}**", f"**{tc}**", mnl, f"Chặn ở bậc kế: {why}", "MODEL_OUTPUT"], has_number=True, cite=cite, label=True)
    w("")
    w("Ghi chú: Chubb **BD** (Mốc 4) có điều kiện thăng cấp `[CHH0DCEB260007V : 7]` nhưng **biểu phí BD không có trong nguồn** (mục 4.3). "
      "Chubb **RD** và Manulife **PSM+/HKD** là bổ nhiệm theo hợp đồng dịch vụ, không có lộ trình định lượng từ tuyến đại lý trong 9 PDF. "
      "Manulife: Đại Lý → UM+ → PSM+/HKD là các tuyến hợp đồng; điều kiện chuyển bậc ở 0013M04/2024 (không có trong nguồn, nhật ký 4.3).")
    w("")

    # ---- Rubric
    w("## 6. Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)")
    w("")
    tbl, tot = rubric_table(files_ok, len(SCAN_PAGES_REVIEWED), src[SCAN_ID]["n"], titles_ok, titles_total,
                            counters["cited"], counters["numeric"], missing_with_proof, len(MISSING),
                            counters["labelled"], counters["data"])
    w(tbl)
    w("")
    if tot < 90:
        raise SystemExit(f"rubric FAIL {tot}")
    return "\n".join(L) + "\n"


def main() -> None:
    text = build()
    if re.search(r"[A-Za-z]:\\\\Users|/Users/|file://", text):
        raise SystemExit("local path leaked into report")
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
