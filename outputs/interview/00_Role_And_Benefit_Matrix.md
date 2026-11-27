# 00 — Ma trận chức danh & quyền lợi ngang hàng (4 mốc × 3 hãng × 6 dòng)

> Nguồn: 9/9 PDF trong `private/sources/` (3 AIA + 3 Chubb + 3 Manulife), kiểm kê và Negative Proof ở `00_Role_Mapping_Audit.md`. Số tiền = **tr/tháng** (`MODEL_OUTPUT`, cùng engine và giả định với `01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md`); điều kiện = `VERIFIED FACT`. Mọi trích dẫn có token được script kiểm trên text trang. Mục lục 9 PDF: `knowledge/sources/pdf-bookmarks.json`.

> **Mốc 2–4 là PHÍ QUẢN LÝ THUẦN — KHÔNG gồm hoa hồng/thưởng tự bán của quản lý** (giả định A3). Vì vậy tổng Mốc 2 của AIA và Manulife có thể **thấp hơn** Mốc 1 (đại lý tự bán 30tr FYP/tháng). Nếu quản lý vẫn tự bán như Mốc 1, cộng thêm thu nhập cá nhân Mốc 1: AIA 18,1, Chubb 22,5, Manulife 17,8 tr/tháng (xấp xỉ: Chubb AL hưởng bảng thưởng cá nhân cao hơn AR `[CHH0DCEB260007V : 4]`; AIA tính FYC bản thân CQL vào nhóm trực tiếp `[AIAVAD 2601-034 : 3]`).

## Mốc 1 — Cá nhân — 1 đại lý, 30,0tr FYP/tháng (thu nhập cá nhân)

| Dòng | AIA Alpha · **SA** | Chubb Life · **AR** | Manulife · **Đại Lý** |
|---|---|---|---|
| (1) Hoa hồng trực tiếp | 16,4 (FYC + tái tục, A1/A7) [AIAVAD 2604-069 : 18] `ASSUMPTION` | 16,4 (FYC + RYC, A1/A7) [CHH0DCEB260007V : 13-19] `ASSUMPTION` | 16,4 (FYC + tái tục, A1/A7) [0046M01_2026 : 9] `ASSUMPTION` |
| (2) Phí quản lý F1 (nhóm trực tiếp) | — không quản lý [AIAVAD 2601-034 : 8] `VERIFIED FACT` | — không quản lý [CHH0DCEB260008V : 3] `VERIFIED FACT` | — không quản lý [0047M01_2026 : 1] `VERIFIED FACT` |
| (3) Phí quản lý gián tiếp F2–F4 | — không quản lý [AIAVAD 2601-034 : 4] `VERIFIED FACT` | — không quản lý [CHH0DCEB260008V : 7] `VERIFIED FACT` | — không quản lý [0047M01_2026 : 1] `VERIFIED FACT` |
| (4) Thưởng quý / năm / tăng trưởng | 1,6 [AIAVAD 2604-069 : 5-7] `MODEL_OUTPUT` | 4,9 (HQKD tháng + quý) [CHH0DCEB260007V : 4-6] `MODEL_OUTPUT` | 1,3 (năng suất tháng/quý + M-Star) [0046M01_2026 : 4-8] `MODEL_OUTPUT` |
| (5) Duy trì tái tục (RYC) | 0,0 (thưởng SYC) [AIAVAD 2604-069 : 6] `MODEL_OUTPUT` | 1,1 [CHH0DCEB260007V : 6-7] `MODEL_OUTPUT` | — không có khoản riêng [0046M01_2026 : 2-8] `VERIFIED FACT` |
| (6) Điều kiện chặn K2 / tuyển mới | Thưởng × hệ số FY 2026; lên UM cần ≥2 người tuyển/6 tháng [AIAVAD 2604-069 : 3], [AIAVAD 2601-034 : 8] `VERIFIED FACT` | Thưởng × K2 cá nhân (≥80%: 120% … <50%: 25%); RYC cần K2 ≥65%; lên UM cần 2 đại lý giới thiệu đạt 3MAA [CHH0DCEB260007V : 4], [CHH0DCEB260007V : 7] `VERIFIED FACT` | Mọi thưởng × hệ số TLDTHD (từ 04/2026: ≥70% 100%, <50% TLDTHD/2) × CLKD; điều kiện lên UM+ ở 0013M04/2024 (không có) [0046M01_2026 : 1], [0047M01_2026 : 6] `VERIFIED FACT` |
| **Tổng tr/tháng** | **18,1** | **22,5** | **17,8** |

## Mốc 2 — Nhóm 6 người — 5 đại lý, 150,0tr FYP/tháng (phí quản lý thuần, không gồm tự bán)

| Dòng | AIA Alpha · **SUM** | Chubb Life · **UM** | Manulife · **UM+** |
|---|---|---|---|
| (1) Hoa hồng trực tiếp | — quản lý không tự bán (A3)  `ASSUMPTION` | — quản lý không tự bán (A3)  `ASSUMPTION` | — quản lý không tự bán (A3)  `ASSUMPTION` |
| (2) Phí quản lý F1 (nhóm trực tiếp) | 11,7 [AIAVAD 2601-034 : 3] `MODEL_OUTPUT` | 32,4 [CHH0DCEB260008V : 5] `MODEL_OUTPUT` | 7,2 (A.I cấp 1) + 3,8 (A.II) [0047M01_2026 : 1-2] `MODEL_OUTPUT` |
| (3) Phí quản lý gián tiếp F2–F4 | — không có quản lý con [AIAVAD 2601-034 : 4] `ASSUMPTION` | — không có AL con [CHH0DCEB260008V : 7] `ASSUMPTION` | — không có cấp 2 [0047M01_2026 : 1] `ASSUMPTION` |
| (4) Thưởng quý / năm / tăng trưởng | 5,9 (quý 4 sao + năm trả chậm) [AIAVAD 2601-034 : 4-5] `MODEL_OUTPUT` | 16,2 (HT KTN quý) [CHH0DCEB260008V : 6] `MODEL_OUTPUT` | 0 (phí dài hạn chỉ cho MBA Pro) [0047M01_2026 : 5] `ASSUMPTION` |
| (5) Duy trì tái tục (RYC) | — không có khoản này [AIAVAD 2601-034 : 3-7] `VERIFIED FACT` | 5,6 [CHH0DCEB260008V : 9-10] `MODEL_OUTPUT` | — không có khoản này [0047M01_2026 : 1-6] `VERIFIED FACT` |
| (6) Điều kiện chặn K2 / tuyển mới | FY nhóm <80% → bậc phí thấp hơn; FY <70% → phí hoạt động × FY thực đạt; quý cần FY ≥75%; người mới/quý: 3 sao ≥1, 4–5 sao ≥2 (từ Q2) [AIAVAD 2601-034 : 3-5] `VERIFIED FACT` | Phí tháng × K2 NTT (≥80%: 120% … <50%: 25%); phí RYC cần K2 NTT ≥65%; gián tiếp = 0 nếu FYC NTT <15tr [CHH0DCEB260008V : 5-10] `VERIFIED FACT` | Phí hoạt động × TLDTHD cấp 1 (từ 04/2026: ≥80% 110% … <50% TLDTHD/2); phải "Đội ngũ chuyên cần" ≥4 buổi/tháng; phí dài hạn cần TLDTHD ≥70% [0047M01_2026 : 2-3], [0047M01_2026 : 6] `VERIFIED FACT` |
| **Tổng tr/tháng** | **17,6** | **54,2** | **11,0** |

## Mốc 3 — Ban 15 người — 15 đại lý, 450,0tr FYP/tháng (phí quản lý thuần, không gồm tự bán)

| Dòng | AIA Alpha · **SDM** | Chubb Life · **DM** | Manulife · **UM+** |
|---|---|---|---|
| (1) Hoa hồng trực tiếp | — quản lý không tự bán (A3)  `ASSUMPTION` | — quản lý không tự bán (A3)  `ASSUMPTION` | — quản lý không tự bán (A3)  `ASSUMPTION` |
| (2) Phí quản lý F1 (nhóm trực tiếp) | 11,7 [AIAVAD 2601-034 : 3] `MODEL_OUTPUT` | 32,4 [CHH0DCEB260008V : 5] `MODEL_OUTPUT` | 7,2 (A.I cấp 1) + 3,8 (A.II) [0047M01_2026 : 1-2] `MODEL_OUTPUT` |
| (3) Phí quản lý gián tiếp F2–F4 | 8,1 [AIAVAD 2601-034 : 4] `MODEL_OUTPUT` | 32,4 [CHH0DCEB260008V : 7] `MODEL_OUTPUT` | 7,2 (cấp 2 × ½ tỷ lệ) [0047M01_2026 : 1] `MODEL_OUTPUT` |
| (4) Thưởng quý / năm / tăng trưởng | 5,9 (quý 4 sao + năm trả chậm) [AIAVAD 2601-034 : 4-5] `MODEL_OUTPUT` | 16,2 (HT KTN quý) [CHH0DCEB260008V : 6] `MODEL_OUTPUT` | 0 (phí dài hạn chỉ cho MBA Pro) [0047M01_2026 : 5] `ASSUMPTION` |
| (5) Duy trì tái tục (RYC) | — không có khoản này [AIAVAD 2601-034 : 3-7] `VERIFIED FACT` | 5,6 [CHH0DCEB260008V : 9-10] `MODEL_OUTPUT` | — không có khoản này [0047M01_2026 : 1-6] `VERIFIED FACT` |
| (6) Điều kiện chặn K2 / tuyển mới | FY nhóm <80% → bậc phí thấp hơn; FY <70% → phí hoạt động × FY thực đạt; quý cần FY ≥75%; người mới/quý: 3 sao ≥1, 4–5 sao ≥2 (từ Q2) [AIAVAD 2601-034 : 3-5] `VERIFIED FACT` | Phí tháng × K2 NTT (≥80%: 120% … <50%: 25%); phí RYC cần K2 NTT ≥65%; gián tiếp = 0 nếu FYC NTT <15tr [CHH0DCEB260008V : 5-10] `VERIFIED FACT` | Phí hoạt động × TLDTHD cấp 1 (từ 04/2026: ≥80% 110% … <50% TLDTHD/2); phải "Đội ngũ chuyên cần" ≥4 buổi/tháng; phí dài hạn cần TLDTHD ≥70% [0047M01_2026 : 2-3], [0047M01_2026 : 6] `VERIFIED FACT` |
| **Tổng tr/tháng** | **25,7** | **86,6** | **18,2** |

## Mốc 4 — Khu vực 45 người — 45 đại lý, 1.200,0tr FYP/tháng (phí quản lý thuần, không gồm tự bán)

**Bảng chính — tuyến lãnh đạo vùng.** Chubb: chức danh đạt bằng chỉ tiêu là **BD** `[CHH0DCEB260007V : 7]` nhưng biểu phí BD không có trong nguồn; RD và PSM/SM là chức danh bổ nhiệm theo hợp đồng dịch vụ.

| Dòng | AIA Alpha · **PAF** | Chubb Life · **RD (bổ nhiệm)** | Manulife · **PSM/SM (bổ nhiệm)** |
|---|---|---|---|
| (1) Hoa hồng trực tiếp | — quản lý không tự bán (A3)  `ASSUMPTION` | — RD không tự bán (A3)  `ASSUMPTION` | — PSM+ không tự bán (A3)  `ASSUMPTION` |
| (2) Phí quản lý F1 (nhóm trực tiếp) | 24,0 (phí cơ bản PAF) + 38,5 (chuyên môn tháng) + 10,4 (CQL trực tiếp) [AIAVAD 2601-035 : 3-4], [AIAVAD 2601-035 : 2] `MODEL_OUTPUT` | 45,0 (đào tạo 25 + hoạt động 8 + kinh doanh 12) + 43,2 (chất lượng 12% FYC) [CHH0DCEB260003V : 5-7] `MODEL_OUTPUT` | 45,5 (phí cơ bản 35tr × 100% × 130%) + 24,0 (năng suất 6% FYC × TLDTHD) [0048M01_2026 : 1-2] `MODEL_OUTPUT` |
| (3) Phí quản lý gián tiếp F2–F4 | 0 — PAF+ không nhận gián tiếp cấp 2-3-4 [AIAVAD 2601-035 : 2] `VERIFIED FACT` | 0 — không có BD/RD con trong cấu trúc mốc (phí II.7–II.8 = 25–50% / 12,5–25% phí của BD/RD con) [CHH0DCEB260003V : 10-11] `ASSUMPTION` | 0 — không có PSM+ báo cáo trực tiếp (gián tiếp = 50% phí của cấp báo cáo) [0048M01_2026 : 2] `ASSUMPTION` |
| (4) Thưởng quý / năm / tăng trưởng | 34,2 (chuyên môn quý) + 24,0 (vượt chỉ tiêu) + 5,2 (CQL quý/năm) [AIAVAD 2601-035 : 4-5] `MODEL_OUTPUT` | 9,0 (tăng trưởng quý 2,5% — FYP đi ngang) [CHH0DCEB260003V : 8-9] `MODEL_OUTPUT` | 10,0 (hoạt động quý 2,5%) + 25,5 (hợp tác dài hạn, trả chậm 30/30/40) [0048M01_2026 : 2-5] `MODEL_OUTPUT` |
| (5) Duy trì tái tục (RYC) | — không có khoản này [AIAVAD 2601-035 : 3-5] `VERIFIED FACT` | 89,4 (30% RYC năm 2–5, K2 ≥70%; RYC theo A7) [CHH0DCEB260003V : 9-10] `MODEL_OUTPUT` | — không có khoản này [0048M01_2026 : 1-5] `VERIFIED FACT` |
| (6) Điều kiện chặn K2 / tuyển mới | Hệ số FY cho phí chuyên môn: ≥75% 120% … <50% 0%; phí cơ bản theo % đạt chỉ tiêu FYP (<35% = 0) [AIAVAD 2601-035 : 3-4] `VERIFIED FACT` | Phí chất lượng & tăng trưởng = 0 nếu K2 <60% (từ Q3/2026); duy trì: nhánh trực tiếp 750tr FYP + 25 EHC / 6 tháng; chức danh RD do bổ nhiệm theo hợp đồng [CHH0DCEB260003V : 7], [CHH0DCEB260003V : 13], [CHH0DCEB260003V : 3] `VERIFIED FACT` | Phí cơ bản = 0 nếu đạt <30% chỉ tiêu FYP; phí năng suất/quý × TLDTHD (từ 04/2026: <50% → TLDTHD/2); phí dài hạn cần ≥85% chỉ tiêu và TLDTHD ≥70%; chức danh PSM+ do bổ nhiệm (0013M04/2024 không có) [0048M01_2026 : 1-4] `VERIFIED FACT` |
| **Tổng tr/tháng** | **136,3** | **186,6** | **105,1** |

### Mốc 4 — bảng phụ: tuyến quản lý truyền thống (phí quản lý thuần)

| Dòng | Chubb Life · **DM (AL)** — nếu chưa lên BD | Manulife · **UM+** |
|---|---|---|
| (1) Hoa hồng trực tiếp | — quản lý không tự bán (A3)  `ASSUMPTION` | — quản lý không tự bán (A3)  `ASSUMPTION` |
| (2) Phí quản lý F1 (nhóm trực tiếp) | 28,8 [CHH0DCEB260008V : 5] `MODEL_OUTPUT` | 6,4 (A.I cấp 1) + 3,3 (A.II) [0047M01_2026 : 1-2] `MODEL_OUTPUT` |
| (3) Phí quản lý gián tiếp F2–F4 | 86,4 (L1 50% × 4 AL con + L2 25% × 4 UM) [CHH0DCEB260008V : 7] `MODEL_OUTPUT` | 19,2 (cấp 2 × 8% + cấp 3 × 4%) [0047M01_2026 : 1] `MODEL_OUTPUT` |
| (4) Thưởng quý / năm / tăng trưởng | 14,4 (HT KTN quý) [CHH0DCEB260008V : 6] `MODEL_OUTPUT` | 0 (phí dài hạn chỉ cho MBA Pro) [0047M01_2026 : 5] `ASSUMPTION` |
| (5) Duy trì tái tục (RYC) | 5,0 [CHH0DCEB260008V : 9-10] `MODEL_OUTPUT` | — không có khoản này [0047M01_2026 : 1-6] `VERIFIED FACT` |
| (6) Điều kiện chặn K2 / tuyển mới | Phí tháng × K2 NTT (≥80%: 120% … <50%: 25%); phí RYC cần K2 NTT ≥65%; gián tiếp = 0 nếu FYC NTT <15tr; đủ điều kiện lên BD nhưng biểu phí BD không có trong nguồn (Negative Proof: `00_Role_Mapping_Audit.md` mục 4.3) [CHH0DCEB260008V : 5-10], [CHH0DCEB260007V : 7] `VERIFIED FACT` | Phí hoạt động × TLDTHD cấp 1 (từ 04/2026: ≥80% 110% … <50% TLDTHD/2); phải "Đội ngũ chuyên cần" ≥4 buổi/tháng; phí dài hạn cần TLDTHD ≥70% [0047M01_2026 : 2-3] `VERIFIED FACT` |
| **Tổng tr/tháng** | **134,6** | **28,9** |

### Ghi chú độ nhạy — Manulife có danh hiệu MBA Pro (để chạy ở Giai đoạn 2)

Base case = **không có danh hiệu** (tiêu chí MBA Pro ở 0050M01/2026, không có trong 9 PDF). Nếu UM+ có danh hiệu MBA Pro: phí hoạt động nhóm tăng từ 50% lên **100%** (4–5 người sản xuất) hoặc 125% (≥6) `[0047M01_2026 : 2]`; phí phát triển đại lý mới tăng từ 50% lên 100% `[0047M01_2026 : 3]`; có thêm **phí hợp tác dài hạn** 80% (Bạc) / 100% (Vàng) / 125% (Bạch Kim) × (A.II + A.III), trả chậm 30/30/40% `[0047M01_2026 : 5-6]`. Với đại lý: danh hiệu Manulife Pro mở thêm thưởng xuất sắc tháng và thưởng KDXS năm `[0046M01_2026 : 4-7]`. Nhãn: `HYPOTHESIS` — chưa đưa vào số base case.

## Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)

| # | Tiêu chí (`qa/data-ingestion-rubric.md`) | Điểm | Tối đa | Căn cứ đo được |
|---|---|---:|---:|---|
| 1 | Độ phủ nguồn 9/9 file | 25.0 | 25 | 9/9 file mở được và khớp SHA-256; bản scan soát 15/15 trang |
| 2 | Chức danh gốc & tuyến | 25.0 | 25 | 12/12 chức danh có tên nguyên văn khớp trang trích (hoặc đối chiếu bằng mắt với bản scan) và có `track_type` |
| 3 | Trích dẫn `[File : Trang]` cho từng con số | 20.0 | 20 | 57/57 dòng có số mang trích dẫn đúng mẫu |
| 4 | Negative Proof | 15.0 | 15 | 0/0 kết luận "không có trong tài liệu" kèm nhật ký tìm kiếm |
| 5 | Tách Fact / Assumption | 15.0 | 15 | 84/84 dòng có nhãn phân loại |
| | **Tổng** | **100.0** | **100** | **PASS** (ngưỡng 90) — máy đếm trên chính các bảng, đo độ phủ trích dẫn & nhãn, không phải điểm chất lượng phân tích |

Script đã kiểm token trên trang cho 82 trích dẫn (bản scan 0003V: đối chiếu bằng mắt).
