# Kiểm tra đọc nguồn — 9 PDF, 2 lượt đọc độc lập, đối chiếu ngược với bản `main`

Ngày: 2026-11-28 · Nhánh `claude/fresh-approach` · Không sửa gì trên `main`.

## 1. Cách đọc

- 9 văn bản, 135 trang. Mỗi văn bản giao cho 2 người đọc độc lập (agent phụ), không ai xem bài của người kia:
  - **A**: đọc chữ đã tách theo trang, rồi mở ảnh từng trang có bảng để xác nhận từng ô.
  - **B**: đọc ảnh từng trang làm nguồn chính, chỉ dùng chữ để chép đúng câu chữ. Bản scan Chubb `CHH0DCEB260003V` (15 trang, không có lớp chữ) chỉ đọc bằng ảnh 200 dpi; B đọc ngược từ trang cuối.
- Hướng dẫn chung: [READER_BRIEF.md](READER_BRIEF.md). Bản đọc gốc: [reads/](reads/).
- So 2 bản bằng máy ([compare_reads.py](compare_reads.py), [table_order.py](table_order.py)): (1) tập hợp mọi con số theo trang và toàn văn bản; (2) thứ tự từng ô trong từng bảng. Mọi chỗ lệch được Claude mở ảnh trang gốc để chốt.

## 2. Kết quả đọc

| Văn bản | Trang | Quy tắc | A so với B | Ghi chú chốt |
|---|---:|---:|---|---|
| AIA 2604-069 (CVTV) | 23 | 22 | Khớp mọi số | Claude xem ảnh tr.3–4: bảng tỷ lệ chi trả theo FY |
| AIA 2601-034 (CQL) | 21 | 18 | Khớp mọi số | — |
| AIA 2601-035 (PAF+) | 18 | 23 | Khớp mọi số | 1.300 chỉ tiêu tháng/năm cộng khớp tổng |
| Chubb 260007V (Đại lý) | 19 | 23 | Khớp mọi số | Ô gộp 45%/60% (tr.4) |
| Chubb 260008V (Quản lý) | 14 | 13 | Khớp mọi số | Ô gộp 25%/35% (tr.5) |
| Chubb 260003V (RD, **scan**) | 15 | 16 | Khớp mọi số | Không có chữ số mờ |
| Manulife 0046M01 (Đại lý) | 11 | 21 | **Lệch 1 bảng** | Tr.4 Manulife Pro: ô gộp Bạc 3tr từ ≥30tr, Vàng 7tr từ ≥60tr — **chốt theo B** sau khi xem ảnh |
| Manulife 0047M01 (UM+) | 8 | 11 | Khớp mọi số | — |
| Manulife 0048M01 (PSM+) | 6 | 11 | Khớp mọi số | — |
| **Tổng** | **135** | **158** | | Bộ đã chốt: [rules_verified.json](rules_verified.json) |

Bản thân các văn bản có nhiều chỗ tự mâu thuẫn (ví dụ minh họa trái quy tắc, mục dẫn chiếu không tồn tại, thuật ngữ không định nghĩa) — đã ghi trong `inconsistencies` của từng văn bản.

## 3. Đối chiếu ngược: bản `main` đọc/tính sai ở đâu

3 agent kiểm toán so từng hằng số trong `model/compensation/compensation_engine.py` (và `scripts/`) với 158 quy tắc đã chốt. Chi tiết từng dòng: [audit_main/](audit_main/).

| Hãng | Khớp | Sai số | Thiếu trong code | Mơ hồ | Không có nguồn |
|---|---:|---:|---:|---:|---:|
| AIA | 22 | 6 | 8 | 3 | 3 |
| Chubb Life | 31 | 11 | 17 | 5 | 3 |
| Manulife | 23 | 1 | 12 | 6 | 3 |

**Lỗi mức cao (đã xác minh bằng ảnh trang với AIA):**

| Mã | Ở đâu trong `main` | Văn bản nói | `main` đang làm | Ảnh hưởng |
|---|---|---|---|---|
| MF-01 | `aia_cvtv_fy_factor` (dòng 259–287) | 2026: ≥85 → 120% · ≥75 → 110% · ≥65 hoặc chưa có FY → 100% · >0–<65 → %FY. 2027: ≥90 → 120% · ≥80 → 110% · ≥70 → 100% · <70 → 0% (AIA-069 tr.3) | Thêm bậc 90%/80% (2026) và 115%/105%/85% (2027) không có trong văn bản | Thu nhập đại lý AIA ở FY 65–80% bị tính thấp 10–20%; chỉ số "chi trả giảm khi K2 85→65%" của AIA sai |
| MF-03 | `calc_aia_paf` (dòng 606–607) | Phí chuyên nghiệp tháng: <50 / 50–<100 / 100–<115 / ≥115% (AIA-035 tr.4) | Ngưỡng 55 / 90 / 115% | 50–54% bị trả 0; 90–99% bị trả cao hơn 1,5 điểm % |
| MF-04 | `calc_aia_paf` (dòng 620–621) | Phí chuyên nghiệp quý: 90 / 100 / 110 / 120% (AIA-035 tr.4–5) | 90 / 100 / 115 / 130% | 110–114% và 120–129% bị trả thấp (~25tr/quý ở 125%) |
| CHB-05 | `calc_chubb_ar_12m` (dòng 776–781) | Đại lý <3 tháng: FYC 3 tháng = FYC thực × 3 / số tháng làm việc (CHB-007 tr.4) | Cộng 0 cho tháng thiếu | Đại lý mới bị xếp bậc thấp hơn (chỉ ảnh hưởng mô phỏng thâm niên <3 tháng) |
| CHB-46 | `calc_chubb_al_12m` | Phí phát triển SM: 100%, trần 30tr/tháng, 12 tháng (CHB-008 tr.8–9) | Không có | Thu nhập quản lý Chubb bị thiếu khi có thăng cấp |
| CHB-61/62 | `calc_chubb_rd_12m` | Phí II.7 (50/25%) và II.8 (25/12,5%) cho RD (CHB-003 tr.10–12) | Không có | Thu nhập lãnh đạo vùng Chubb bị thiếu |

**Không sai số nhưng đáng chú ý:**
- Manulife: không con số nào sai; thiếu mức Bạch Kim 20tr (FYP ≥120tr, điều kiện MDRT), phí phát triển nhóm mới UM+ (A.IV, tới 360tr/UM mới); `scripts/agent_income_multiyear.py` vẫn ghi "chưa có văn bản Manulife cấp đại lý" dù 0046M01 đã có.
- Thời điểm trả: nhiều khoản quý 4 / thưởng năm trả vào năm sau nhưng `main` tính vào tiền mặt năm 1 (AIA ~22tr/đại lý, Chubb AL ~43tr).
- Chubb RD: khi không có FYP năm trước, `main` tự giả định tăng trưởng 15% — ảnh hưởng ~360tr/năm trong kịch bản so sánh.

**Những gì `main` làm đúng:** mọi ô gộp quan trọng (Manulife Pro, Chubb 45/60%, Chubb 25/35%), cả 2 bảng hệ số K2 của Manulife, 1.300 chỉ tiêu PAF+, toàn bộ bảng RD Chubb từ bản scan.

## 4. Hệ quả cho nhánh này

Mô hình mới trên nhánh này đọc tham số trực tiếp từ `rules_verified.json`, kèm số trang; các lỗi trên không được mang sang. Quyết định có sửa `main` hay không là của TJ.
