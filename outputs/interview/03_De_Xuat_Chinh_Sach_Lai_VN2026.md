# 03 — Chính sách Đề xuất 2026 & Phân vùng

> `PROPOSAL` — không phải chính sách đã ban hành. Sinh bởi `scripts/build_phase2.py`; tham số ở `model/compensation/hybrid_scheme.py`. Kế thừa bộ tham số **Song Hành** đã hiệu chỉnh (hiệu chỉnh để không tầng nào thấp nhất thị trường ở K2 82%; trong K2 75–90% có điểm thấp hơn tối đa ~2%).

## 1. Khung chính sách

| Thành phần | Thiết kế | Lý do (bài học từ 3 hãng) |
|---|---|---|
| Đường ray **Full-time** (cam kết) | Thưởng tháng 100% bậc Song Hành + trợ cấp cam kết 3,0tr/tháng (Vùng 1; vùng khác × hệ số vùng) khi FYP ≥ quota vùng, ≥2 HĐ/tháng và K2 ≥80% | Nuôi quân có điều kiện như AIA Exchange nhưng có cổng chất lượng; phần cố định nhỏ |
| Đường ray **Part-time** (thuần biến phí) | Thưởng tháng 70% bậc Song Hành, không trợ cấp | Không phát sinh định phí cho người bán không đều |
| **Chốt chặn K2 ≥ 80%** | Trợ cấp Full-time chỉ khi K2 ≥80%; phần trả chậm nhận ĐỦ khi K2 ≥80%, 50% khi 75–<80%, 0 khi <75%; thưởng tháng theo hệ số K2 liên tục (sàn 60%) | Bản thử đầu (cắt hết dưới 80%) tạo vách đá −37,5% ở quản lý nhóm — lớn nhất trong 4 phương án; bậc đệm 75–80% giảm vách đá mà vẫn khóa phần thưởng lớn vào chất lượng |
| Giảm (chưa xóa) bẫy đội phẳng | Override nhóm trực tiếp đủ tỷ lệ tới 60tr FYC/tháng (không giãn theo vùng), phần vượt 50% | Cả 3 hãng trả cho đội phẳng nhiều hơn đội có quản lý con (mục 2 của 02); với Chính sách Đề xuất 2026 tỷ lệ vẫn > 1 — chỉ giảm, chưa xóa |
| Quản lý | Override 35,7% × hệ số K2 (trần 42,8%) FYC nhóm; gián tiếp 2 đời (35,0% / ½), cổng FYC nhóm ≥ 15,0tr × hệ số vùng; trả chậm 17,8% FYC nhóm | Học cổng 15tr của Chubb, bỏ chuỗi gián tiếp vô hạn |
| Lãnh đạo vùng | Phí cơ bản 40,2tr × % đạt chỉ tiêu (sàn 30%, trần 140%) + override 8,05% FYC vùng × K2; 70% override trả chậm | Học Manulife: phí cơ bản gắn chỉ tiêu, không cố định cứng |
| Trần chi phí | Tổng chi / FYP ≤ 75% ở kịch bản XẤU NHẤT | Kiểm tự động: chuẩn 61,1%; xấu nhất (V4, điểm gãy cao nhất của lưới quét (128,33tr FYP/ĐL, K2 85%)) 74,2% → ĐẠT, dư 0,8 điểm % |

## 2. Bảng hệ số vùng (Regional Tiering) — `PROPOSAL`

| Vùng | Hệ số quota FYP | Quota Full-time (tr FYP/tháng) | Trợ cấp Full-time (tr/tháng) | Chỉ tiêu lãnh đạo (tr FYP/tháng) | Giữ nguyên |
|---|---:|---:|---:|---:|---|
| Vùng I theo NĐ 293/2025 (gồm nội thành Hà Nội, TP.HCM) | 100,0% | 30,0 | 3,00 | 1.000 | ≥2 HĐ/tháng; K2 ≥80% — PROPOSAL (hybrid_scheme.py) `PROPOSAL` |
| Vùng II theo NĐ 293/2025 | 89,0% | 26,7 | 2,67 | 890 | ≥2 HĐ/tháng; K2 ≥80% — PROPOSAL (hybrid_scheme.py) `PROPOSAL` |
| Vùng III theo NĐ 293/2025 | 78,0% | 23,4 | 2,34 | 780 | ≥2 HĐ/tháng; K2 ≥80% — PROPOSAL (hybrid_scheme.py) `PROPOSAL` |
| Vùng IV theo NĐ 293/2025 | 70,0% | 21,0 | 2,10 | 700 | ≥2 HĐ/tháng; K2 ≥80% — PROPOSAL (hybrid_scheme.py) `PROPOSAL` |

Hệ số giãn **mọi ngưỡng FYP/FYC** của Chính sách Đề xuất 2026: quota, bậc thưởng tháng, ngưỡng thưởng nhất quán (4tr FYC/tháng), MDRT (400tr FYC/năm), thưởng nhập môn (8tr), cổng gián tiếp, chỉ tiêu lãnh đạo; và **trợ cấp Full-time** (3tr × hệ số). **Không giãn:** tỷ lệ %, số hợp đồng, K2, và trần override đội phẳng 60tr FYC (nhắm vào quy mô đội, không phải năng suất). Hệ số = lương tối thiểu vùng 2026 theo NĐ 293/2025/NĐ-CP (5,31 / 4,73 / 4,14 / 3,70 tr/tháng → 100 / 89 / 78 / 70%) — `SOURCE_CLAIM` (wheel-check r2 câu 5); thay bộ tự đặt 100 / 82,5 / 67,5% trước đây. Đối chiếu thu nhập bình quân đầu người VHLSS 2025: thành phố lớn 84–87% Hà Nội/TP.HCM, cả nước 73%, miền núi 31–50% → Vùng IV 70% vẫn cao so với tỉnh miền núi nghèo nhất (`HYPOTHESIS`: có thể cần bậc thứ 5).

## 3. Thu nhập theo vùng (tr/tháng)

Hai cách đọc: **cùng FYP** (cùng năng suất ở mọi vùng) và **FYP vùng** (năng suất điển hình = FYP mốc × hệ số vùng). Đại lý = thu nhập cá nhân gồm tái tục (A7, cùng cơ sở bảng 01); quản lý = phí quản lý thuần.

| Vai trò | V1 cùng FYP | V1 FYP vùng | V2 cùng FYP | V2 FYP vùng | V3 cùng FYP | V3 FYP vùng | V4 cùng FYP | V4 FYP vùng | Nguồn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| M1 · Đại lý Full-time | 23,2 | 23,2 | 22,9 | 20,7 | 22,6 | 18,1 | 23,6 | 16,3 | PROPOSAL (hybrid_scheme.py) `PROPOSAL` |
| M1 · Đại lý Part-time | 19,9 | 19,9 | 19,9 | 17,7 | 19,9 | 15,5 | 20,7 | 13,9 | PROPOSAL (hybrid_scheme.py) `PROPOSAL` |
| M2 · Trưởng nhóm (phí thuần) | 27,3 | 27,3 | 27,3 | 24,3 | 27,3 | 21,3 | 27,3 | 19,1 | PROPOSAL (hybrid_scheme.py) `PROPOSAL` |
| M3 · Trưởng ban (phí thuần) | 40,8 | 40,8 | 40,8 | 36,3 | 40,8 | 31,8 | 40,8 | 28,6 | PROPOSAL (hybrid_scheme.py) `PROPOSAL` |
| M4 · Lãnh đạo khu vực (phí thuần) | 106,0 | 106,0 | 106,0 | 100,6 | 106,0 | 95,1 | 106,0 | 91,1 | PROPOSAL (hybrid_scheme.py) `PROPOSAL` |

## 4. Đáp ứng khác biệt vùng miền (`HYPOTHESIS` — repo không có dữ liệu hành vi theo vùng)

| Miền | Giả thuyết hành vi | Cơ chế trong Chính sách Đề xuất 2026 |
|---|---|---|
| Bắc | Trọng hệ thống, danh hiệu, lộ trình thăng tiến | Lộ trình quản lý 2 đời rõ ràng; trả chậm gắn K2 như "danh hiệu bền"; quota vùng 1 cho Hà Nội |
| Trung | K2 cao, hợp đồng nhỏ, năng suất thấp hơn | Hệ số vùng 2/3 hạ quota nhưng **giữ CC và K2**; thưởng tháng theo hệ số K2 liên tục thưởng chất lượng |
| Nam | Ưu tiên dòng tiền, tự chủ; quen mô hình HKD | Part-time thuần biến phí trả hàng tháng; lãnh đạo có thể chọn hình thức hợp đồng hộ kinh doanh như Manulife (cùng biểu phí — lợi ích thuế cần Pháp chế xác nhận) |

## 5. Chấm điểm so với 3 hãng (cùng Rubric 5 trụ cột, bản DEC-19)

| Phương án | Điểm có trọng số (1–5) |
|---|---:|
| **Chính sách Đề xuất 2026** | 3,77 — PROPOSAL (hybrid_scheme.py) `PROPOSAL` |
| Manulife | 3,74 — [0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5] `MODEL_OUTPUT` |
| AIA Alpha | 3,69 — [AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7] `MODEL_OUTPUT` |
| Chubb Life | 3,22 — [CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10] `MODEL_OUTPUT` |

Chi tiết trụ cột và công thức: `02_Phan_Tich_MAPA_TradeOff_Va_ROI.md` mục 3. **Lưu ý:** điểm Chính sách Đề xuất 2026 do bên thiết kế tự chấm; trụ cột Vận hành & Pháp lý là đánh giá, không cộng vào tổng; pháp lý `CONDITIONAL`; cổng Điều 52 và trần 75% xét trước điểm.

## 6. Rủi ro & việc TJ cần quyết

1. Hệ số vùng đã neo lương tối thiểu vùng NĐ 293/2025; vẫn cần dữ liệu năng suất bán hàng thật theo tỉnh của công ty để hiệu chỉnh (`PROPOSAL`).
2. Trợ cấp Full-time 3,0tr/tháng và quota — phần cố định duy nhất; nếu tỷ lệ đạt quota thấp, chi phí thấp hơn mô hình.
3. Pháp lý: tỷ lệ thưởng/FYP và hợp đồng hộ kinh doanh cần Pháp chế đối chiếu toàn văn trước khi ban hành.
4. **Rủi ro lách vùng (chưa có kiểm soát — cần chọn 1 trong 3 cách dưới đây trước khi thí điểm):** cùng năng suất, đại lý vùng thấp nhất (V4) nhận 23,6 so với V1 23,2 tr/tháng và chi phí tổ chức tăng lên mức kịch bản xấu nhất ở 02 — tạo động cơ đăng ký mã vùng thấp hơn nơi bán thật. Lựa chọn: (a) gắn vùng theo địa chỉ bên mua bảo hiểm của từng hợp đồng; (b) gắn theo văn phòng quản lý, kiểm tra chéo tỷ lệ hợp đồng ngoài vùng; (c) trần: đại lý vượt 120% quota vùng 3 tháng liên tiếp chuyển sang ngưỡng vùng trên.
5. Vách đá cấp đại lý còn lại (mục 2 của 02): mất K2 80% hoặc thiếu 0,1tr quota làm mất trọn trợ cấp. Giữ nguyên có chủ đích vì đây là chốt chặn chất lượng hồ sơ; phương án mềm hơn (trợ cấp giảm dần thay vì mất trọn) để ngỏ cho giai đoạn thí điểm.

## 7. Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)

Báo cáo này là `PROPOSAL`: mọi tham số lấy từ `hybrid_scheme.py` / bộ Song Hành, không từ PDF; các con số đối chiếu 3 hãng nằm ở 02 (đã trích). Tiêu chí 3 đếm dòng bảng có số mang nguồn (PDF hoặc `PROPOSAL`); tiêu chí 5 đếm dòng có nhãn.

| # | Tiêu chí (`qa/data-ingestion-rubric.md`) | Điểm | Tối đa | Căn cứ đo được |
|---|---|---:|---:|---|
| 1 | Độ phủ nguồn 9/9 file | 25.0 | 25 | 9/9 file mở được và khớp SHA-256; bản scan soát 15/15 trang |
| 2 | Chức danh gốc & tuyến | 25.0 | 25 | 3/3 chức danh có tên nguyên văn khớp trang trích (hoặc đối chiếu bằng mắt với bản scan) và có `track_type` |
| 3 | Trích dẫn `[File : Trang]` cho từng con số | 18.6 | 20 | 13/14 dòng có số mang trích dẫn đúng mẫu |
| 4 | Negative Proof | 15.0 | 15 | 0/0 kết luận "không có trong tài liệu" kèm nhật ký tìm kiếm |
| 5 | Tách Fact / Assumption | 13.9 | 15 | 13/14 dòng có nhãn phân loại |
| | **Tổng** | **97.5** | **100** | **PASS** (ngưỡng 90) — máy đếm trên chính các bảng, đo độ phủ trích dẫn & nhãn, không phải điểm chất lượng phân tích |
