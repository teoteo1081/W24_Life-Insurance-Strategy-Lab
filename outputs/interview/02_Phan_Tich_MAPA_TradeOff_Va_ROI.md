# 02 — Phân tích hành vi, Trade-off & ROI 3 tầng (Giai đoạn 2)

> Sinh bởi `scripts/build_phase2.py` từ engine (baseline `90e7d10`, Codex PASS). Số 3 hãng = `MODEL_OUTPUT`; số Chính sách Lai = `PROPOSAL`. **"ROI" ở đây là chi phí / FYP và chi phí / phí còn duy trì — KHÔNG phải ROI thực tế** (VNB, biên lợi nhuận, OpEx thật = `UNKNOWN`). Số Manulife dựa trên 0046M01/0047M01 (`restricted`, DEC-14).

**Mô hình tổ chức dùng chung (`ASSUMPTION`):** khu vực Mốc 4 — 45 đại lý × 26,7tr FYP/tháng (1,2 tỷ), 1 lãnh đạo (5 ĐL trực tiếp) + 2 trưởng ban (5 ĐL + 2 trưởng nhóm) + 6 trưởng nhóm. Lãnh đạo: AIA PAF · Chubb RD · Manulife PSM/SM (đạt 100% chỉ tiêu) · Lai: lãnh đạo vùng. Chi phí năm đầu = hoa hồng FYC + thưởng + phí quản lý; không gồm tái tục.

## 1. ROI 3 tầng

| Phương án | (1) Tổng chi / FYP — K2 85% | (1b) Khi năng suất −50% | (2) Chi phí / phí còn duy trì — K2 85% | (2) K2 65% | Chi trả giảm khi K2 sập | (3) Tiền mặt năm 1 | (3) Trả các năm sau | Phần cố định | Biểu phí nguồn | Nhãn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| AIA Alpha | 58,4% | 54,3% | 68,7% | 77,0% | 14,2% | 97,4% | 2,6% | 3,4% | [AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7] | `MODEL_OUTPUT` |
| Chubb Life | 88,1% | 73,4% | 103,6% | 106,7% | 21,3% | 100,0% | 0,0% | 4,3% | [CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10] | `MODEL_OUTPUT` |
| Manulife | 50,8% | 44,9% | 59,8% | 73,0% | 6,7% | 95,8% | 4,2% | 7,5% | [0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5] | `MODEL_OUTPUT` |
| **Chính sách Lai (đề xuất)** | 59,9% | 56,1% | 70,5% | 67,5% | 26,7% | 88,7% | 11,3% | 7,8% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |

**Kiểm trần theo kịch bản** (Mốc 4 chuẩn cho mỗi ĐL 26,7tr FYP — DƯỚI quota 30tr, nên trợ cấp Full-time không bật; vì vậy phải kiểm thêm kịch bản đạt quota):

| Phương án | Kịch bản | Tổng chi / FYP | Phần cố định | Nguồn | Nhãn |
|---|---|---:|---:|---|---|
| AIA Alpha | Mốc 4 chuẩn (26,7tr/ĐL) **(xấu nhất)** | 58,4% | 3,4% | [AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7] | `MODEL_OUTPUT` |
| AIA Alpha | Mọi ĐL đạt quota 30tr | 57,9% | 3,1% | [AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7] | `MODEL_OUTPUT` |
| Chubb Life | Mốc 4 chuẩn (26,7tr/ĐL) **(xấu nhất)** | 88,1% | 4,3% | [CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10] | `MODEL_OUTPUT` |
| Chubb Life | Mọi ĐL đạt quota 30tr | 87,7% | 3,8% | [CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10] | `MODEL_OUTPUT` |
| Manulife | Mốc 4 chuẩn (26,7tr/ĐL) | 50,8% | 7,5% | [0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5] | `MODEL_OUTPUT` |
| Manulife | Mọi ĐL đạt quota 30tr **(xấu nhất)** | 51,4% | 7,4% | [0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5] | `MODEL_OUTPUT` |
| **Chính sách Lai (đề xuất)** | Mốc 4 chuẩn (26,7tr/ĐL) | 59,9% | 7,8% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Lai (đề xuất)** | Mọi ĐL đạt quota 30tr | 69,4% | 20,4% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Lai (đề xuất)** | V2, năng suất ngang V1 **(xấu nhất)** | 71,2% | 22,4% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Lai (đề xuất)** | V3, năng suất ngang V1 | 71,2% | 22,4% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |

- **Tầng 1:** trần đề xuất 75% FYP, kiểm ở kịch bản xấu nhất. Chính sách Lai 71,2% (V2, năng suất ngang V1) → **ĐẠT** trần, khoảng dư chỉ 3,8 điểm %. Rủi ro định phí thật của Chính sách Lai là khi **nhiều** đại lý đạt quota, không phải khi năng suất giảm.
- **Tầng 2:** chi phí trên mỗi đồng phí còn duy trì sang năm 2 = chi phí ÷ (FYP × K2). Khi K2 sập 85%→65%, phương án gắn thưởng với K2 tốt thì chi trả **giảm theo**; phương án yếu thì chi phí trên phí còn lại **tăng vọt**.
- **Tầng 3:** phần trả các năm sau (AIA thưởng năm 15/25/60% đến 2030; Manulife phí dài hạn 30/30/40%, M-Star năm trả tháng 2 năm sau; Lai trả chậm khi K2 ≥80%) giữ người và giảm áp lực tiền mặt năm 1.

## 2. Bẫy hành vi (Gaming) & điểm gãy

| Hãng | Bẫy | Đo được | Trích dẫn | Nhãn |
|---|---|---|---|---|
| AIA Alpha | Tự bán vs quản lý thuần | Đại lý Mốc 1 18,1 tr/th; quản lý nhóm 5 người (phí thuần) 17,6 tr/th → quản lý thu ÍT hơn tự bán | [AIAVAD 2601-034 : 3-5] | `MODEL_OUTPUT` |
| AIA Alpha | Bẫy giữ đội phẳng | Ban 15 ĐL: để phẳng (15 trực tiếp) 82,4 vs có 2 quản lý con 25,7 tr/th → tỷ lệ 3,21× | [AIAVAD 2601-034 : 3-5] | `MODEL_OUTPUT` |
| AIA Alpha | Vách đá K2 tại 80% | Quản lý nhóm: K2 80% → 79% làm phí năm giảm 7,7% | [AIAVAD 2601-034 : 3-5] | `MODEL_OUTPUT` |
| Chubb Life | Tự bán vs quản lý thuần | Đại lý Mốc 1 22,5 tr/th; quản lý nhóm 5 người (phí thuần) 48,6 tr/th → quản lý thu nhiều hơn tự bán | [CHH0DCEB260008V : 5-7] | `MODEL_OUTPUT` |
| Chubb Life | Bẫy giữ đội phẳng | Ban 15 ĐL: để phẳng (15 trực tiếp) 145,8 vs có 2 quản lý con 81,0 tr/th → tỷ lệ 1,80× | [CHH0DCEB260008V : 5-7] | `MODEL_OUTPUT` |
| Chubb Life | Vách đá K2 tại 80% | Quản lý nhóm: K2 80% → 79% làm phí năm giảm 16,7% | [CHH0DCEB260008V : 5-7] | `MODEL_OUTPUT` |
| Manulife | Tự bán vs quản lý thuần | Đại lý Mốc 1 17,8 tr/th; quản lý nhóm 5 người (phí thuần) 11,0 tr/th → quản lý thu ÍT hơn tự bán | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| Manulife | Bẫy giữ đội phẳng | Ban 15 ĐL: để phẳng (15 trực tiếp) 40,5 vs có 2 quản lý con 18,2 tr/th → tỷ lệ 2,23× | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| Manulife | Vách đá K2 tại 80% | Quản lý nhóm: K2 80% → 79% làm phí năm giảm 1,2% | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| **Chính sách Lai (đề xuất)** | Tự bán vs quản lý thuần | Đại lý Mốc 1 23,2 tr/th; quản lý nhóm 5 người (phí thuần) 27,3 tr/th → quản lý thu nhiều hơn tự bán | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Lai (đề xuất)** | Bẫy giữ đội phẳng | Ban 15 ĐL: để phẳng (15 trực tiếp) 65,9 vs có 2 quản lý con 40,8 tr/th → tỷ lệ 1,61× | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Lai (đề xuất)** | Vách đá K2 tại 80% | Quản lý nhóm: K2 80% → 79% làm phí năm giảm 21,9% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| AIA Alpha | Rủi ro định phí | Phần cố định 3,4% chi trả; năng suất giảm 50% → chi phí 54,3% FYP (từ 58,4%) | [AIAVAD 2601-035 : 3] | `MODEL_OUTPUT` |
| Chubb Life | Rủi ro định phí | Phần cố định 4,3% chi trả; năng suất giảm 50% → chi phí 73,4% FYP (từ 88,1%) | [CHH0DCEB260003V : 5-6] | `MODEL_OUTPUT` |
| Manulife | Rủi ro định phí | Phần cố định 7,5% chi trả; năng suất giảm 50% → chi phí 44,9% FYP (từ 50,8%) | [0048M01_2026 : 1] | `MODEL_OUTPUT` |
| **Chính sách Lai (đề xuất)** | Rủi ro định phí | Phần cố định 7,8% chi trả; năng suất giảm 50% → chi phí 56,1% FYP (từ 59,9%) | PROPOSAL | `PROPOSAL` |
| Manulife | Độ nhạy danh hiệu MBA Pro (Vàng) | UM+ Mốc 2: không danh hiệu 11,0 → MBA Pro Vàng 22,2 tr/th (phí hoạt động 50%→100% + phí dài hạn 100%) | [0047M01_2026 : 2], [0047M01_2026 : 5] | `HYPOTHESIS` |
| **Chính sách Lai (đề xuất)** | Vách đá K2 của đại lý Full-time | Đại lý Full-time 30tr FYP: K2 80% → 79% làm thu nhập năm giảm 23,6% (13,1 → 10,0 tr/th) vì mất trọn trợ cấp | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Lai (đề xuất)** | Vách đá quota & dồn hợp đồng | FYP 30 → 29,9tr/tháng: thu nhập 13,2 → 10,2 tr/th — động cơ dồn/chuyển hợp đồng giữa các tháng để chạm quota (HYPOTHESIS về hành vi) | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| AIA Alpha | Cổng tuyển mới | Quản lý nhóm AIA: có tuyển (1/2/2/2 người mới/quý) 17,6 vs không tuyển 11,7 tr/th | [AIAVAD 2601-034 : 4-5] | `MODEL_OUTPUT` |

Đọc nhanh: (a) **tự bán vs quản lý** — ở AIA và Manulife, lên quản lý nhóm 5 người mà bỏ bán thì thu nhập giảm; (b) **đội phẳng** — tỷ lệ >1 nghĩa là giữ mọi người trực tiếp có lợi hơn phát triển quản lý con; (c) **vách đá K2** — giảm 1 điểm K2 quanh 80% làm mất một bậc hệ số; (d) **định phí** — phí cố định không co khi năng suất giảm.

## 3. Rubric 5 trụ cột (Compensation Designer)

| Trụ cột (trọng số) | AIA Alpha | Chubb Life | Manulife | **Chính sách Lai (đề xuất)** |
|---|---:|---:|---:|---:|
| Định hướng hành vi (25%) | 2,82 | 3,46 | 3,14 | 3,54 |
| An toàn tài chính / ROI (25%) | 3,90 | 2,65 | 4,04 | 4,30 |
| Sức cạnh tranh thu nhập (20%) | 3,46 | 4,68 | 2,99 | 3,73 |
| Độ đơn giản & dễ tính (15%) | 2,20 | 1,40 | 3,00 | 3,80 |
| Vận hành & Pháp lý (15%) | 3,00 | 2,50 | 3,50 | 3,50 |
| **Điểm có trọng số (1–5)** | **3,15** | **3,05** | **3,37** | **3,80** |

Căn cứ từng điểm:

- **AIA Alpha:** *Định hướng hành vi* — Chi trả giảm 14,2% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc 3,21× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% 7,7% (≤5% = 5, ≥30% = 1) (`MODEL_OUTPUT`); *An toàn tài chính / ROI* — Chi phí kịch bản xấu nhất (Mốc 4 chuẩn (26,7tr/ĐL)) 58,4% FYP (≤60% = 5, ≥100% = 1); năng suất −50% → 54,3% (≤70% = 5, ≥130% = 1); trả chậm 2,6% (≥15% = 5) (`MODEL_OUTPUT`); *Sức cạnh tranh thu nhập* — Trung bình thu nhập 4 mốc / mức cao nhất trong 4 phương án: M1 78% · M2 36% · M3 32% · M4 100% (`MODEL_OUTPUT`); *Độ đơn giản & dễ tính* — 11 khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): 2601-034 mục A.I–A.VI + B (7) [AIAVAD 2601-034 : 3-6]; 2601-035 mục A.1–A.4 (4) [AIAVAD 2601-035 : 3-5] (`MODEL_OUTPUT`); *Vận hành & Pháp lý* — Chấm công ≥50% (CQL) / ≥70% (PAF+), khóa học bắt buộc, trả chậm tới 2030 cần TOT ≥85% — nhiều cổng hành chính [AIAVAD 2601-034 : 3-5] (`JUDGEMENT`)
- **Chubb Life:** *Định hướng hành vi* — Chi trả giảm 21,3% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc 1,80× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% 16,7% (≤5% = 5, ≥30% = 1) (`MODEL_OUTPUT`); *An toàn tài chính / ROI* — Chi phí kịch bản xấu nhất (Mốc 4 chuẩn (26,7tr/ĐL)) 88,1% FYP (≤60% = 5, ≥100% = 1); năng suất −50% → 73,4% (≤70% = 5, ≥130% = 1); trả chậm 0,0% (≥15% = 5) (`MODEL_OUTPUT`); *Sức cạnh tranh thu nhập* — Trung bình thu nhập 4 mốc / mức cao nhất trong 4 phương án: M1 97% · M2 100% · M3 100% · M4 71% (`MODEL_OUTPUT`); *Độ đơn giản & dễ tính* — 13 khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): 0008V mục II.1–II.5 (5) [CHH0DCEB260008V : 3]; 0003V mục II.1–II.8 (8) [CHH0DCEB260003V : 4] (`MODEL_OUTPUT`); *Vận hành & Pháp lý* — RD phải có biên bản nghiệm thu dịch vụ hàng tháng; 9 trường hợp tạm giữ phí; 3 văn bản quy định chung không có trong nguồn (260005V/006V/009V) [CHH0DCEB260003V : 12-15] (`JUDGEMENT`)
- **Manulife:** *Định hướng hành vi* — Chi trả giảm 6,7% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc 2,23× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% 1,2% (≤5% = 5, ≥30% = 1) (`MODEL_OUTPUT`); *An toàn tài chính / ROI* — Chi phí kịch bản xấu nhất (Mọi ĐL đạt quota 30tr) 51,4% FYP (≤60% = 5, ≥100% = 1); năng suất −50% → 44,9% (≤70% = 5, ≥130% = 1); trả chậm 4,2% (≥15% = 5) (`MODEL_OUTPUT`); *Sức cạnh tranh thu nhập* — Trung bình thu nhập 4 mốc / mức cao nhất trong 4 phương án: M1 77% · M2 23% · M3 22% · M4 77% (`MODEL_OUTPUT`); *Độ đơn giản & dễ tính* — 9 khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): 0047M01 A.I–A.V (5) [0047M01_2026 : 1-5]; 0048M01 A.I–A.IV (4) [0048M01_2026 : 1-3] (`MODEL_OUTPUT`); *Vận hành & Pháp lý* — Hai hình thức hợp đồng PSM+/HKD cùng biểu phí, chuyển đổi bảo lưu kết quả; HKD tự xuất hóa đơn — tách rủi ro thuế [0048M01_2026 : 5-6]; điều kiện 'Đội ngũ chuyên cần' 4 buổi/tháng [0047M01_2026 : 3] (`JUDGEMENT`)
- ****Chính sách Lai (đề xuất)**:** *Định hướng hành vi* — Chi trả giảm 26,7% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc 1,61× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% 21,9% (≤5% = 5, ≥30% = 1) (`PROPOSAL`); *An toàn tài chính / ROI* — Chi phí kịch bản xấu nhất (V2, năng suất ngang V1) 71,2% FYP (≤60% = 5, ≥100% = 1); năng suất −50% → 56,1% (≤70% = 5, ≥130% = 1); trả chậm 11,3% (≥15% = 5) (`PROPOSAL`); *Sức cạnh tranh thu nhập* — Trung bình thu nhập 4 mốc / mức cao nhất trong 4 phương án: M1 100% · M2 56% · M3 50% · M4 67% (`PROPOSAL`); *Độ đơn giản & dễ tính* — 7 khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): cùng quy tắc đếm khoản phí tuyến quản lý trong code: override trực tiếp, gián tiếp đời 1, gián tiếp đời 2, trả chậm quản lý, phí cơ bản lãnh đạo, override lãnh đạo, trả chậm lãnh đạo (hybrid_scheme.py) (`PROPOSAL`); *Vận hành & Pháp lý* — Ít khoản, một cổng K2 ≥80% thống nhất; CHƯA đối chiếu pháp lý (TT 67/2023, NĐ 97/2026 — CONDITIONAL); trợ cấp Full-time cần quy trình xác nhận quota/CC (`PROPOSAL`)

> **Lưu ý thiên lệch:** bậc đệm K2 75–80% và trần đội phẳng của Chính sách Lai được thêm SAU khi đo bằng chính rubric này — thiết kế đã được hiệu chỉnh theo thước đo, nên rubric không phải phép thử khách quan cho Chính sách Lai. Độ nhạy (tự kiểm toán): chấm Vận hành & Pháp lý của Lai ở 2,0 (chưa đối chiếu pháp lý) thì điểm giảm 0,225.

> 3 trụ cột đầu tính bằng công thức công khai ở trên; *Độ đơn giản* đếm khoản phí theo mục lục văn bản; *Vận hành & Pháp lý* là đánh giá có dẫn chứng (`JUDGEMENT`). Điểm Chính sách Lai là **tự chấm của bên thiết kế** — cần kiểm toán độc lập (Codex) trước khi dùng làm kết luận.

## 4. Ghi chú độ nhạy Manulife MBA Pro (`HYPOTHESIS`)

UM+ Mốc 2: không danh hiệu 11,0 → MBA Pro Vàng 22,2 tr/th (phí hoạt động 50%→100% + phí dài hạn 100%) `[0047M01_2026 : 2]`, `[0047M01_2026 : 5]`. Tiêu chí danh hiệu (0050M01/2026) không có trong nguồn — chưa đưa vào base case.

## 5. Pháp lý tham chiếu

Tỷ lệ thưởng/FYP theo enterprise model (ngưỡng 30% Điều 52, `CONDITIONAL / SOURCE_NOT_VERIFIED`): AIA_Alpha_2026 11,2%, Chubb_Agency_2026 21,1%. Cần Pháp chế đối chiếu 44/2026/VBHN-TT-BTC trước khi ban hành.

## 6. Negative Proof — kết luận "không có trong nguồn" của báo cáo này

| Kết luận | Đã quét | Là 1 trong 9 file nguồn? | Trang có nhắc tới (chỉ dẫn chiếu, không phải nội dung) |
|---|---|---|---|
| Tiêu chí danh hiệu MBA Pro / Manulife Pro (0050M01/2026) | 9/9 file (tên file + toàn văn từng trang) | KHÔNG | 0046M01_2026: `Manulife Pro` [3, 4, 5, 6, 10]; 0047M01_2026: `0050M01` [2, 3], `MBA Pro` [2, 3, 5], `Manulife Pro` [3, 5] |
| Quy định chung Chubb 260005V / 260006V / 260009V | 9/9 file (tên file + toàn văn từng trang) | KHÔNG | CHH0DCEB260007V: `260005V` [3, 4]; CHH0DCEB260008V: `260005V` [3], `260006V` [3], `260009V` [12] |

## 7. Tự chấm rubric 100 điểm (`qa/data-ingestion-rubric.md`)

| # | Tiêu chí (`qa/data-ingestion-rubric.md`) | Điểm | Tối đa | Căn cứ đo được |
|---|---|---:|---:|---|
| 1 | Độ phủ nguồn 9/9 file | 25.0 | 25 | 9/9 file mở được và khớp SHA-256; bản scan soát 15/15 trang |
| 2 | Chức danh gốc & tuyến | 25.0 | 25 | 3/3 chức danh có tên nguyên văn khớp trang trích (hoặc đối chiếu bằng mắt với bản scan) và có `track_type` |
| 3 | Trích dẫn `[File : Trang]` cho từng con số | 19.4 | 20 | 33/34 dòng có số mang trích dẫn đúng mẫu |
| 4 | Negative Proof | 15.0 | 15 | 2/2 kết luận "không có trong tài liệu" kèm nhật ký tìm kiếm |
| 5 | Tách Fact / Assumption | 15.0 | 15 | 34/34 dòng có nhãn phân loại |
| | **Tổng** | **99.4** | **100** | **PASS** (ngưỡng 90) — `SELF_VERIFIED`, chưa phải kiểm toán độc lập |

Tiêu chí 1 theo kiểm kê `00_Role_Mapping_Audit.md` (9/9 file khớp SHA-256, 15/15 trang scan). Tiêu chí 2: 3 chức danh lãnh đạo Mốc 4 (AIA PAF, Chubb RD, Manulife PSM/SM) lấy từ ma trận `00_Role_And_Benefit_Matrix.md`. Tiêu chí 3/5 đếm tự động mọi dòng bảng có số ở mục 1–2 (dòng Chính sách Lai trích `PROPOSAL (hybrid_scheme.py)` vì không có trong PDF).
