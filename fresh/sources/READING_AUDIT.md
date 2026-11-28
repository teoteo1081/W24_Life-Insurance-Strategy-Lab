# Kiểm tra đọc nguồn — 9 PDF, 2 lượt đọc độc lập, đối chiếu ngược với bản `main`

Ngày: 2026-11-28 · Nhánh `claude/fresh-approach` · Không sửa gì trên `main`.

## 1. Cách đọc

- 9 văn bản, 135 trang. Mỗi văn bản giao cho 2 người đọc độc lập (agent phụ), không ai xem bài của người kia:
  - **A**: đọc chữ đã tách theo trang, rồi mở ảnh từng trang có bảng để xác nhận từng ô.
  - **B**: đọc ảnh từng trang làm nguồn chính, chỉ dùng chữ để chép đúng câu chữ. Bản scan Chubb `CHH0DCEB260003V` (15 trang, không có lớp chữ) chỉ đọc bằng ảnh 200 dpi; B đọc ngược từ trang cuối.
- Hướng dẫn chung: [READER_BRIEF.md](READER_BRIEF.md). Bản đọc gốc: [reads/](reads/).
- So 2 bản bằng máy ([compare_reads.py](compare_reads.py), [table_order.py](table_order.py)):
  1. Tập hợp mọi con số theo trang và toàn văn bản.
  2. Thứ tự từng ô trong từng bảng.
  3. **Điều kiện biên** (bổ sung sau review): mỗi con số mang theo dấu đứng trước nó (≥ > ≤ <, hoặc "từ / trên / dưới / tối thiểu / tối đa / ít nhất…"; cả dạng hậu tố "55% ≤ FY"). **Cụm đứng sau số quyết định chiều**: "từ 12 tháng trở xuống" là ≤ 12 dù có chữ "từ"; "từ hoặc dưới 6" là ≤ 6. Ghép từng quy tắc và từng bảng của A với B theo **cả hai chiều**, rồi so dấu ở mỗi vị trí cùng số (căn theo thứ tự) và tập dấu của mỗi số (không phụ thuộc hàng/cột). Hai lớp 1–2 không bắt được "≥50%" → ">50%"; lớp 3 bắt được.
  4. **Đối chiếu với lớp chữ gốc của PDF** ([check_bounds_vs_text.py](check_bounds_vs_text.py)): mỗi cặp (dấu, số) trong bộ đã chốt phải xuất hiện với cùng dấu trên trang được trích (±1). Lớp này bắt cả trường hợp A và B **cùng** đọc sai một dấu. Thiếu thư mục, thiếu file, hoặc lớp chữ rỗng ở văn bản không phải scan → script báo lỗi đầu vào và dừng (mã thoát 2); chỉ bản scan đã biết `CHB-003` được bỏ qua.
- Mọi chỗ lệch được Claude mở ảnh trang gốc để chốt.

## 2. Kết quả đọc

| Văn bản | Trang | Quy tắc | A so với B (số + dấu biên) | Ghi chú chốt |
|---|---:|---:|---|---|
| AIA 2604-069 (CVTV) | 23 | 22 | Khớp | Claude xem ảnh tr.3–4: bảng tỷ lệ chi trả theo FY |
| AIA 2601-034 (CQL) | 21 | 18 | Khớp | — |
| AIA 2601-035 (PAF+) | 18 | 23 | Khớp | 1.300 chỉ tiêu tháng/năm cộng khớp tổng |
| Chubb 260007V (Đại lý) | 19 | 23 | Khớp | Ô gộp 45%/60% (tr.4) |
| Chubb 260008V (Quản lý) | 14 | 13 | Khớp | Ô gộp 25%/35% (tr.5) |
| Chubb 260003V (RD, **scan**) | 15 | 16 | Khớp | Không có chữ số mờ |
| Manulife 0046M01 (Đại lý) | 11 | 21 | **Lệch 1 bảng** | Tr.4 Manulife Pro: ô gộp Bạc 3tr từ ≥30tr, Vàng 7tr từ ≥60tr đến hết bảng — **chốt theo B** sau khi xem ảnh; ghi chú quy tắc đã viết lại cho khớp bảng |
| Manulife 0047M01 (UM+) | 8 | 11 | Khớp | — |
| Manulife 0048M01 (PSM+) | 6 | 11 | Khớp | — |
| **Tổng** | **135** | **158** | | Bộ đã chốt: [rules_verified.json](rules_verified.json) |

### Kiểm điều kiện biên (bổ sung sau review)

| Lớp kiểm | Kết quả |
|---|---|
| A so với B, theo quy tắc và theo bảng | 8 cờ, đều vô hại: một bên ghi thêm vế bù ("TOT < 85% → không trả" cạnh "≥ 85%") hoặc hai bên chia quy tắc khác nhau. Từng cờ và lý do: [boundary_review.json](boundary_review.json). **0 chỗ cùng số khác dấu thật.** |
| Bộ đã chốt so với lớp chữ PDF (8 văn bản có lớp chữ) | 418 cặp (dấu, số) khớp cùng dấu; 2 cặp "khác dấu" chính là 2 vế bù nêu trên (suy trực tiếp từ điều kiện ≥ của văn bản); 1 cặp trích chéo trang (tr.5 dẫn quy định thai sản tr.16). Kết quả: [bounds_vs_text.json](bounds_vs_text.json) |
| Thử cấy lỗi trên bản đọc thật | Dấu: ≥→> 205/205 · >→≥ 13/13 · <→≤ 87/87 · ≤→< 16/16 · ≥→< 203/205. Cụm chữ (cả bản A và B): "trở lên"→"trở xuống" 109/109 · "trở xuống"→"trở lên" 4/4 · "từ hoặc dưới"→"từ hoặc trên" 2/2 bị phát hiện |

**Giới hạn còn lại:**
- Đổi ≥ thành < trong một quy tắc vốn đã ghi cả "<X" lẫn "≥X" cho cùng số X (2/205 ca thử) không bị lớp A–B bắt. Lớp chữ PDF vẫn bắt nếu văn bản không có cụm "<X" ở trang đó.
- Bản scan Chubb `CHH0DCEB260003V` không có lớp chữ, nên chỉ có lớp A–B (2 lượt đọc ảnh độc lập).
- Ngưỡng không có dấu trong văn bản (ví dụ cột "FYC của quý" chỉ ghi "120 triệu đồng") được giữ nguyên là số trần và ghi chú "không ghi dấu"; công cụ không tự suy ra dấu.
- Chưa có ai đọc lại toàn bộ 135 trang lần thứ ba. Xác nhận hiện có gồm hai lượt đọc độc lập, các lớp máy ở trên, và Claude xem ảnh tại mọi chỗ bị cờ.

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
