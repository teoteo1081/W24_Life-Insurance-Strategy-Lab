"""Sinh bản có dấu tiếng Việt cho kho 44 cấu phần thu nhập để hiển thị trên trang HTML.

Không sửa file gốc `knowledge/compensation/total-rewards-inventory.csv` (nguyên văn trích xuất, là bằng chứng).
Đầu ra: `knowledge/compensation/total-rewards-inventory-vi.csv` (Component_ID + các trường hiển thị).
Cách làm: thay cụm từ dài trước, rồi từ đơn, giữ hoa/thường; sau đó áp OVERRIDES theo từng ô đã rà tay.
Dùng:  py -3 scripts/vietnamize_rewards.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "knowledge/compensation/total-rewards-inventory.csv"
OUT = REPO / "knowledge/compensation/total-rewards-inventory-vi.csv"
FIELDS = ("Component_Name_VN", "Rate_Or_Amount_Summary", "Eligibility_Conditions", "Threshold_Minimum", "Cap_Maximum",
          "Quality_Persistency_Gate", "Activity_Attendance_Gate", "Training_Compliance_Gate", "Measurement_Period",
          "Payment_Timing", "Vesting_Schedule", "Clawback_Recovery_Rule")

PHRASES = {
    # cụm nhiều từ (ưu tiên)
    "hoa hong": "hoa hồng", "khai thac": "khai thác", "phu luc": "phụ lục", "gia dinh": "giả định", "mo phong": "mô phỏng",
    "dai ly": "đại lý", "hieu luc": "hiệu lực", "phi thuc thu": "phí thực thu", "thuc thu": "thực thu", "khong chan xet tra": "không chặn xét trả",
    "chung chi": "chứng chỉ", "thu hoi": "thu hồi", "huy trong": "hủy trong", "6 thang dau": "6 tháng đầu", "ke ca": "kể cả",
    "da nghi viec": "đã nghỉ việc", "kich hoat": "kích hoạt", "sieu toc": "siêu tốc", "ngay lam viec": "ngày làm việc",
    "cap ma": "cấp mã", "khong tu mua": "không tự mua", "tu cap ma": "từ cấp mã", "dong hanh": "đồng hành", "thang dau": "tháng đầu",
    "can nhac": "cân nhắc", "ngoai le": "ngoại lệ", "cham cong": "chấm công", "tieu chi": "tiêu chí", "chuyen huan luyen": "chuyến huấn luyện",
    "huan luyen": "huấn luyện", "dac biet": "đặc biệt", "quy doi": "quy đổi", "chi phi": "chi phí", "hoan thanh": "hoàn thành",
    "khoa hoc": "khóa học", "doanh so": "doanh số", "ca nhan": "cá nhân", "he so": "hệ số", "khong tron quy": "không tròn quý",
    "tron quy": "tròn quý", "theo ngay": "theo ngày", "so thang": "số tháng", "lam tron": "làm tròn", "ky luat": "kỷ luật",
    "ky chi tra": "kỳ chi trả", "chi tra": "chi trả", "cuoi quy": "cuối quý", "chuyen vien": "chuyên viên", "ngoai hang": "ngoại hạng",
    "toi thieu": "tối thiểu", "chat luong": "chất lượng", "dich vu": "dịch vụ", "danh hieu": "danh hiệu", "theo quy dinh": "theo quy định",
    "quy dinh": "quy định", "tai chinh": "tài chính", "sau chot nam": "sau chốt năm", "chot nam": "chốt năm", "bao hiem": "bảo hiểm",
    "suc khoe": "sức khỏe", "tieu chuan": "tiêu chuẩn", "cao cap": "cao cấp", "trong nam": "trong năm", "con hieu luc": "còn hiệu lực",
    "cap goi": "cấp gói", "1 nam": "1 năm", "cham dut": "chấm dứt", "nhung": "nhưng", "gioi thieu": "giới thiệu", "nguoi gioi thieu": "người giới thiệu",
    "tam khau tru": "tạm khấu trừ", "khau tru": "khấu trừ", "hang thang": "hàng tháng", "hang quy": "hàng quý", "hang nam": "hàng năm",
    "nguoi moi": "người mới", "tro cap": "trợ cấp", "toan thoi gian": "toàn thời gian", "khong duoc bia so": "không được bịa số",
    "tuyen dung": "tuyển dụng", "hieu qua": "hiệu quả", "duy tri": "duy trì", "chuc danh": "chức danh", "khai bao": "khai báo",
    "trung thuc": "trung thực", "nhay len": "nhảy lên", "khung": "khung", "mien thang bo nhiem": "miễn tháng bổ nhiệm",
    "bo nhiem": "bổ nhiệm", "thai san": "thai sản", "dao tao": "đào tạo", "gian tiep": "gián tiếp", "truc tiep": "trực tiếp",
    "tuan thu": "tuân thủ", "han dong cap": "hạn đồng cấp", "dong cap": "đồng cấp", "cql con": "CQL con", "cql me": "CQL mẹ",
    "thang tien": "thăng tiến", "lan dau": "lần đầu", "ca me va con": "cả mẹ và con", "giu chuc danh": "giữ chức danh",
    "nang cao": "nâng cao", "ky nang": "kỹ năng", "tra cham": "trả chậm", "3 nam": "3 năm", "co ban": "cơ bản", "co dinh": "cố định",
    "chuyen nghiep": "chuyên nghiệp", "tham nien": "thâm niên", "nang suat": "năng suất", "hoat dong": "hoạt động", "hop tac": "hợp tác",
    "dai han": "dài hạn", "san pham": "sản phẩm", "phi troi": "phí trội", "hieu qua kinh doanh": "hiệu quả kinh doanh", "kinh doanh": "kinh doanh",
    "nhan": "nhận", "dai ly moi": "đại lý mới", "ho tro": "hỗ trợ", "khai thac nhom": "khai thác nhóm", "quan ly": "quản lý", "nhom": "nhóm",
    "phat trien": "phát triển", "giai ngan": "giải ngân", "giu lai": "giữ lại", "tai nan": "tai nạn", "phuc vu": "phục vụ", "khach hang": "khách hàng",
    "tang truong": "tăng trưởng", "tich luy": "tích lũy", "nghiem thu": "nghiệm thu", "bat buoc": "bắt buộc", "tai tuc": "tái tục",
    "phi am": "phí âm", "doi xung": "đối xứng", "chuong trinh": "chương trình", "quyen loi": "quyền lợi", "thoi han": "thời hạn",
    "trach nhiem": "trách nhiệm", "dien": "diện", "tro len": "trở lên", "duoi": "dưới", "tren": "trên", "vuot": "vượt", "tong": "tổng",
    "khong": "không", "chua": "chưa", "den": "đến", "theo": "theo", "trong": "trong", "hoac": "hoặc", "trong thang": "trong tháng",
    "nop": "nộp", "duyet": "duyệt", "lop": "lớp", "buoi": "buổi", "lan": "lần", "luot": "lượt", "vong": "vòng", "nguong": "ngưỡng",
    "muc": "mức", "bac": "bậc", "giang cap": "giáng cấp", "xet": "xét", "dat": "đạt", "cong": "cổng", "ung": "ứng", "gom": "gồm",
    "tu": "từ", "voi": "với", "va": "và", "cua": "của", "neu": "nếu", "sau": "sau", "truoc": "trước", "khi": "khi", "da": "đã",
    "con": "con", "la": "là", "tai": "tại", "tiep": "tiếp", "de": "để", "tam": "tạm", "thoi viec": "thôi việc", "chia doi": "chia đôi", "ngay khi": "ngay khi", "dong 1 lan": "đóng 1 lần", "no cap": "không trần", "quy doi": "quy đổi", "trung thuc": "trung thực", "phi dich vu": "phí dịch vụ", "thieu": "thiếu", "moi": "mới", "nguoi": "người", "thang": "tháng", "quy": "quý", "nam": "năm", "ngay": "ngày", "tuan": "tuần",
    "thuong": "thưởng", "phi": "phí", "tra": "trả", "huy": "hủy", "cap": "cấp", "tien": "tiền", "ve": "vé", "goi": "gói",
    "thuan": "thuần", "lai": "lại", "dau": "đầu", "cuoi": "cuối", "ky": "kỳ", "so": "số", "co": "có", "ca": "cả", "ma": "mã",
    "chi": "chỉ", "tieu": "tiêu", "dong": "đồng", "hd": "HĐ", "hdbh": "HĐBH", "doanh": "doanh", "thu": "thu", "thieu": "thiếu",
    "hien": "hiện", "dung": "đúng", "tinh": "tính", "can": "cần", "duoc": "được", "bi": "bị", "ko": "không", "nhanh": "nhánh",
    "chuoi": "chuỗi", "phan": "phần", "tran": "trần", "mat": "mất", "gan": "gắn", "vao": "vào", "khu vuc": "khu vực", "suat": "suất",
    "quoc": "quốc", "luu": "lưu", "nguon": "nguồn", "tuy": "tùy", "tuong": "tương", "cu": "cũ", "do": "do", "tuoi": "tuổi",
    "tiet": "tiết", "nghia": "nghĩa", "chon": "chọn", "vai": "vài", "nhat": "nhất", "thong": "thông", "chiu": "chịu", "thuoc": "thuộc",
    "chan": "chặn", "toi": "tối", "du": "đủ", "luat": "luật", "yeu cau": "yêu cầu", "van": "vẫn", "diem": "điểm", "chia": "chia",
    "ngung": "ngừng", "don": "đơn", "nghiep": "nghiệp", "phai": "phải", "xung": "xứng", "map": "map", "bam": "bám", "sach": "sách",
    "dang": "đang", "ty": "tỷ", "doan": "đoạn", "trien": "triển", "dut": "dứt", "bo": "bộ", "me": "mẹ", "tham": "thâm", "nien": "niên",
    "tru": "trừ", "giu": "giữ", "chot": "chốt", "thoi": "thời", "nhiem": "nhiệm", "san": "sàn", "hanh": "hành", "trung": "trùng",
    "han": "hạn", "dot": "đợt", "tung": "từng", "cat": "cắt", "pham": "phạm", "phat": "phát", "an": "an", "phuc": "phúc",
    "soat": "soát", "chong": "chống", "ho": "hộ", "nan": "nạn", "mo": "mô", "phong": "phỏng", "mua": "mua", "le": "lệ",
    "dac": "đặc", "biet": "biệt", "loi": "lợi", "luc": "lực", "ban": "bản", "hoc": "học", "doi": "đối", "khoa": "khóa", "lam": "làm",
    "dich": "dịch", "cao": "cao", "tri": "trì", "toan": "toàn", "bien": "biến", "truong": "trưởng", "tao": "tạo", "nang": "năng",
    "hop": "hợp", "ngoai": "ngoại", "len": "lên", "chuc": "chức", "dinh": "định", "duyet": "duyệt", "tron": "tròn", "chinh": "chính",
    "dieu kien": "điều kiện", "ke": "kể", "thanh": "thành", "nhap": "nhập", "tuc": "tục", "tac": "tác", "lieu": "liệu", "troi": "trội",
    "tich": "tích", "luy": "lũy", "cuc": "cực", "am": "âm", "giang": "giáng", "thoi gian": "thời gian", "loai tru": "loại trừ",
    "dien bien": "diễn biến", "binh quan": "bình quân", "nhac": "nhắc", "trach": "trách", "vien": "viên", "sao": "sao", "hiem": "hiểm",
    "suc": "sức", "khoe": "khỏe", "chuan": "chuẩn", "khung": "khung", "tuyen": "tuyển", "quan": "quản", "hieu": "hiệu", "nghi": "nghỉ",
    "viec": "việc", "hoan": "hoàn", "cham": "chậm", "giai": "giải", "ngan": "ngân", "dao": "đào", "gioi": "giới", }
# None / N/A / Immediate được GIỮ NGUYÊN: template dùng chúng để ẩn ô rỗng (audit 64b9a5a, P2).
ENGLISH = {"monthly": "Hàng tháng", "quarterly": "Hàng quý", "annual": "Hàng năm",
           "unknown": "Chưa có tài liệu", "per policy": "Theo hợp đồng", "no cap": "Không trần"}
STATUS_KEEP = {"none", "n/a", "immediate", "0"}
KEEP = {"tr", "fyc", "fyp", "fy", "syc", "ryc", "ntt", "ehc", "um", "al", "rd", "cql", "paf", "ar", "sa", "ul", "tt", "kpi",
        "jfw", "ack", "fna", "sop", "tc", "cl", "bd", "sm", "dm", "vnd", "aia", "hkd", "psm", "amd", "ilp", "hsbh", "tncn", "btc", "aff"}


def _case(src: str, dst: str) -> str:
    if src.isupper() and len(src) > 1:
        return dst.upper()
    if src[:1].isupper():
        return dst[:1].upper() + dst[1:]
    return dst


def vietnamize(text: str) -> str:
    if not text:
        return text
    t = text.strip()
    if t.lower() in STATUS_KEEP:
        return t
    if t.lower() in ENGLISH:
        return ENGLISH[t.lower()]
    # "cap" tiếng Anh = trần khi đi kèm "=" hoặc con số tính bằng tr/% (cap 6tr, Cap = 12x, cap 45%); còn lại là "cấp" (audit 64b9a5a, P1).
    t = re.sub(r"\b(cap)\b(?=\s*(?:=|\d+(?:[.,]\d+)?\s*(?:tr|%)))", lambda m: "Trần" if m.group(1)[0].isupper() else "trần", t, flags=re.I)
    t = re.sub(r"(?<=\d)d\b", "đ", t)                    # "0d" -> "0đ"
    keys = sorted((k for k in PHRASES if k.strip().lower() not in KEEP), key=len, reverse=True)
    pat = re.compile(r"(?<![A-Za-zÀ-ỹ])(" + "|".join(re.escape(k.strip()) for k in keys) + r")(?![A-Za-zÀ-ỹ])", re.I)
    lut = {k.strip().lower(): v.strip() for k, v in PHRASES.items()}
    t = pat.sub(lambda m: _case(m.group(0), lut[m.group(0).lower()]), t)   # một lượt, không thay chồng
    t = re.sub(r"\bUNKNOWN\b", "chưa có tài liệu", t)
    for a, b in FIXUPS:
        t = t.replace(a, b)
    return t


# Sửa các từ đa nghĩa sau khi rà tay toàn bộ 44 dòng.
FIXUPS = [("None (", "Không ("), ("pending C.1 from 02/2026", "chờ quy định C.1 từ 02/2026"), ("pending C.1", "chờ quy định C.1"),
          ("deferred prevents payout", "trả chậm, chưa chi"), ("1,300 đồng", "1.300 dòng"), ("113 đồng", "113 dòng"), ("CQL còn", "CQL con"), ("hiệu lực ngày khi", "hiệu lực ngay khi"),
          ("cấp trùng", "cấp trung"), ("trưởng hợp", "trường hợp"), ("Biến bản", "Biên bản"), ("gian lần", "gian lận"),
          ("Boi hoàn", "Bồi hoàn"), ("boi hoàn", "bồi hoàn"), ("chỉ tiết", "chi tiết"), ("Tương lại", "Tương lai"),
          ("Từ Do An Phúc", "Tự Do An Phúc"), ("từ vòng", "tử vong"), ("bao cao", "báo cáo"), ("bao lưu", "bảo lưu"),
          ("chống!)", "chồng!)"), ("Nhận chống", "Nhận chồng"), ("o T+1", "ở T+1"), ("vé 0%", "về 0%"), ("phần FYP vé", "phần FYP về"),
          ("KPI 4 trừ", "KPI 4 trụ"), ("đối con thâm gia", "đối với người còn tham gia"), ("an bám he thông dưới", "ăn bám hệ thống dưới"),
          ("Để nhận cực", "Để nhận cục"), ("Chọn 1 vài tro duy nhất", "Chọn 1 vai trò duy nhất"), ("Chuyen khoan", "Chuyển khoản"),
          ("TANG LÊN", "TĂNG LÊN"), ("PHU THUỘC", "PHỤ THUỘC"), ("Chuyen tiếp", "Chuyển tiếp"), ("cổng tỷ", "công ty"),
          ("KHÔNG ĐƯỢC ĐOẠN", "KHÔNG ĐƯỢC ĐOÁN"), ("TẠI LIỆU", "TÀI LIỆU"), ]


OVERRIDES: dict[tuple[str, str], str] = {
    # Đối chiếu SRC-POL-MNL-001 tr.5: TLDTHD (K2) >= 70% xét riêng cho từng năm chi trả Y1/Y2/Y3,
    # xác định tại cuối tháng 12 năm liền trước năm chi trả (audit 64b9a5a, P3).
    ("TR-MNL-04", "Quality_Persistency_Gate"):
        "K2 (TLDTHD) >= 70%, xét lại cho từng năm chi trả Y1–Y3, đo tại cuối tháng 12 năm liền trước năm chi trả",
}


def main() -> int:
    with SRC.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=("Component_ID",) + FIELDS)
        w.writeheader()
        for r in rows:
            out = {"Component_ID": r["Component_ID"]}
            for k in FIELDS:
                out[k] = OVERRIDES.get((r["Component_ID"], k), vietnamize(r[k]))
            w.writerow(out)
    print(f"wrote {OUT.relative_to(REPO)} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
