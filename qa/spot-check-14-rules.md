# Kiểm mẫu độc lập 14 quy tắc ↔ trang PDF gốc

**Ngày:** 2026-11-26 · **Người kiểm:** Claude (phiên tư vấn TJ), không phải AGY, nên đây là lượt kiểm thứ hai độc lập với người trích xuất.
**Cách chọn mẫu:** 2 quy tắc/PDF, chọn ngẫu nhiên có seed cố định (`scripts/spot_check_sample.py`, seed 24) trong các quy tắc có số trang.
**Cách kiểm:** đọc lớp chữ của trang được trích dẫn bằng PyMuPDF. Với file scan Chubb 003, xem ảnh trang (80 dpi). Sau đó so ngưỡng, tỷ lệ, trần và cấu trúc của quy tắc với văn bản.
**Hai mục tiêu:**
1. Quy tắc có đúng với tài liệu không.
2. Số trang trong quy tắc có trùng chỉ số trang của file PDF không. Đây là điều kiện để link `…pdf#page=N` trên HTML mở đúng chỗ.

| # | Rule_ID | Trang | Kết quả | Bằng chứng trên trang |
|---|---|---|---|---|
| 1 | AIA-CV-023 | 001 p.14 | ✅ | Mục VII "Quy định về tỷ lệ duy trì phí năm đầu (AIA FY)", công thức T-14 |
| 2 | AIA-CV-013 | 001 p.7 | ✅ | Mục 9 "Phí dịch vụ giới thiệu Chuyên viên mới": SA 5% / Exchange 10% / Exchange Pro 20%, 12 tháng chuẩn |
| 3 | AIA-MG-006 | 002 p.5 | ✅ | Danh hiệu CQL 3/4/5 sao → 5% / 8% / 15% FYC tín chỉ nhóm quý, chấm công 50% |
| 4 | AIA-MG-004 | 002 p.4 | ✅ | Mục IV: 150% phí A, FY nhóm ≥ 75%, "tối đa 30 triệu/tháng/01 CQL mới" |
| 5 | AIA-PF-003 | 003 p.4 | ✅ | Tỷ lệ theo FYP 0 / 3 / 4.5 / 6%; 1mAA 0 / 1.5 / 2.5 / 3.5%; hệ số chất lượng 0–120% |
| 6 | AIA-PF-004 | 003 p.4 | ✅ | "50% Phí dịch vụ tháng thực nhận của báo cáo trực tiếp" (không nêu giới hạn tầng) |
| 7 | MNL-PM-003 | MNL p.2 | ✅ | "PSM+/HKD quản lý gián tiếp khu vực nhận 50% trên phí dịch vụ năng suất tháng…" |
| 8 | MNL-PM-011 | MNL p.5 | ✅ | Ghi chú 7–8: chuyển đổi PSM+ ↔ HKD giữ nguyên kết quả và quyền lợi đã phát sinh |
| 9 | CHB-AG-003 | CHB-001 p.13 | ✅ | Phụ đính II: tỷ lệ hoa hồng theo sản phẩm và năm hợp đồng |
| 10 | CHB-AG-012 | CHB-001 p.8 | ✅ | Điều kiện duy trì vị trí: K2/P13 50%, AR dự bị chấm dứt sau 18 tháng |
| 11 | CHB-MG-003 | CHB-002 p.5 | ✅ | Mục 2.1: phí dịch vụ HT KTN và bảng tỷ lệ điều chỉnh theo K2 (đã mở bằng link R2 `#page=5`) |
| 12 | CHB-MG-005 | CHB-002 p.7 | ✅ | Mục 3 "Phí dịch vụ quản lý nhóm theo tháng" L1/L2/L3 theo UM/SM/DM |
| 13 | CHB-RD-001 | CHB-003 p.3 (scan) | ✅ | Hệ thống cấp bậc AMD: BD và RD |
| 14 | CHB-RD-012 | CHB-003 p.13 (scan) | ✅ trang bắt đầu | Mục V "Quy định khác" bắt đầu ở p.13. Các trường hợp tạm giữ và kỳ chi trả nằm ở dải p.13–15 như quy tắc ghi |

**Kết luận (`VERIFIED FACT` trên mẫu):**
- 14/14 quy tắc khớp nội dung trang.
- 14/14 số trang trùng chỉ số trang PDF, nên `#page=N` dùng được trực tiếp, không cần bù lệch trang bìa.
- Mẫu nhỏ (14/112). Kết quả này **không** thay cho kiểm toán đầy đủ 112 quy tắc.

**Phát hiện thêm:** `SRC-POL-AIA-ALP-001` p.8 ghi công ty **tạm khấu trừ 10% thuế TNCN** trên phí dịch vụ giới thiệu Chuyên viên mới, và chuyên viên tự quyết toán thuế. Có thể dùng làm bằng chứng cho phần "thuế" trên HTML. Đây là quy định của một khoản thu nhập ở một hãng, không phải mức thuế chung cho mọi khoản.
