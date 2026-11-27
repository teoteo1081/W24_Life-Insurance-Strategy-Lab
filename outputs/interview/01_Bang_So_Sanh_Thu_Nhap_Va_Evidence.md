# 01 — Bảng soi tiền 3 cấp quản lý & Evidence

> **Trạng thái:** `MODEL_OUTPUT` trên kịch bản chuẩn (`ASSUMPTION`) — chờ TJ duyệt (Giai đoạn 1).
> Không phải thu nhập thực tế đã quan sát, không phải ROI thực tế.
> Sinh tự động bởi `scripts/build_interview_income_table.py` từ `model/compensation/compensation_engine.py`; không gõ tay số.
> Đơn vị: **triệu VNĐ / tháng** = thu nhập được hưởng cả năm (Earned, gồm phần trả chậm) ÷ 12, **trước thuế TNCN**.

## 1. Kết luận nhanh

| Cấp (kịch bản) | AIA Alpha | Chubb Life | Manulife | Chi phí quản lý / FYP tổ chức (AIA · Chubb) |
|---|---:|---:|---:|---|
| Cấp 1 — Trưởng nhóm (UM): 5 ĐL, 150tr FYP/th | **17,6** | **54,2** | ❓ chưa có tài liệu | 11,7% · 36,1% |
| Cấp 2 — Trưởng ban (BM): 15 ĐL, 450tr FYP/th | **25,7** | **86,6** | ❓ chưa có tài liệu | 5,7% · 19,2% |
| Cấp 3 — Trưởng khu vực (DM): 45 ĐL, 1,2 tỷ FYP/th | **37,2** | **134,6** | ❓ chưa có tài liệu | 3,1% · 11,2% |
| Cấp 3B — cùng khu vực, nếu xếp vào tuyến **lãnh đạo vùng** (AIA PAF+ DSRF · Chubb RD · Manulife PSM) | **144,8** | **186,6** | **105,1** | 12,1% · 15,5% · MNL 8,8% |

**Đọc nhanh (`MODEL_OUTPUT`):**
- Ở tuyến quản lý trung gian (UM/BM/DM), **Chubb trả gấp khoảng 3,1–3,6 lần AIA** với cùng đội ngũ và doanh số. Lý do: Chubb tính phí trực tiếp 60% FYC nhóm × hệ số K2 120% và cộng thêm 50% phí tháng mỗi quý; AIA trả 8–24% FYC nhóm.
- **AIA đặt 2 cửa khóa:** thưởng quý (3–5 sao) đòi tuyển mới **≥2 CVTV có hoạt động mỗi quý** (Q1 ≥1); thưởng năm trả chậm 15/25/60% vào 2028–2030 và đòi FY nhóm ≥75%, TOT ≥85%.
- **Manulife:** 7 PDF chỉ có biểu phí **PSM+/HKD** (tuyến lãnh đạo vùng). Biểu phí UM/SUM/DM của Manulife **không có trong tài liệu** (`SRC-GAP-002`) nên cấp 1–3 là `UNKNOWN`, không điền 0.
- **HKD không rẻ hơn cho công ty theo văn bản:** PSM+ và HKD dùng **cùng một biểu phí** (0048M01 mục A). Khác biệt chỉ ở hợp đồng và thuế (mục C.9–C.10): PSM+ được công ty khấu trừ TNCN; HKD tự xuất hóa đơn và tự nộp thuế. Lợi ích thuế của HKD là `UNKNOWN` cho đến khi Pháp chế/Thuế đối chiếu.

## 2. Giả định chuẩn dùng cho mọi hãng (`ASSUMPTION`)

| # | Giả định | Giá trị | Vì sao / ảnh hưởng |
|---|---|---|---|
| A1 | FYC / FYP | 30% | Giả định chung của repo. Thiếu biểu hoa hồng AIA và memo FYC tín chỉ (`SRC-GAP-001`); cơ cấu sản phẩm thật chưa có. AIA tính trên **FYC tín chỉ**, ở đây coi = FYC. |
| A2 | Tỷ lệ duy trì | K2 = 85% cho cả 3 hãng | AIA dùng **FY** (14 tháng) và **TOT**; Manulife dùng **TLDTHD**; Chubb dùng **K2 NTT**. Coi cả ba = 85%. Công thức gốc của từng hãng nằm ở văn bản chưa có (260005V, 0016M03/2024). |
| A3 | Quản lý không tự bán | 0 doanh số cá nhân | So sánh thuần thu nhập quản lý. Lưu ý: FYC nhóm trực tiếp của AIA **có** gồm bán cá nhân của CQL, của Chubb thì **không**. |
| A4 | Đại lý hoạt động | Cả đội hoạt động mọi tháng; mỗi đại lý ≥1 HĐ và ≥4tr FYC | FYC mỗi đại lý: 9tr (cấp 1–2), 8tr (cấp 3). Chubb: coi mọi đại lý đạt **EHC** và **3MAA**; định nghĩa EHC nằm ở 260005V (chưa có). |
| A5 | Cấu trúc tổ chức | Cấp 1: 1 nhóm 5 người. Cấp 2: nhóm trực tiếp 5 + 2 UM con × 5. Cấp 3: nhóm trực tiếp 5 + 2 BM con (mỗi BM như cấp 2) + 2 UM con = 45 | Thu nhập phụ thuộc mạnh vào cấu trúc; xem độ nhạy ở mục 5. |
| A6 | Tuyển dụng (AIA) | CVTV mới có hoạt động/quý ở nhóm trực tiếp: [1, 2, 2, 2] | Cần để đạt danh hiệu 3–5 sao quý. Không cộng FYC và phí đồng hành của người mới (giữ quy mô 5 người). |
| A7 | Thâm niên | Quản lý ≥15 tháng, ổn định cả năm 2026 | Chubb AL ≥15 tháng được bảng phí cao hơn; phí RYC cần ≥13 tháng. |
| A8 | RYC (chỉ Chubb dùng) | RYC/năm = FYP năm × K2 × 20% + FYP năm × K2 × 0.92 × 10% | Giả định tái tục chung của repo (`scripts/agent_income_multiyear.py`); chỉ tính HĐ năm 2–3 nên thấp hơn thực tế. |
| A10 | Cấp 3B | AIA PAF+ bậc DSRF năm 1 (chỉ tiêu 12.000tr FYP/năm); Manulife PSM/SM phí cơ bản 35tr, đạt 100% chỉ tiêu FYP và 1mAA; Chubb RD FYP đi ngang so với cùng kỳ | Chọn bậc PAF+ có chỉ tiêu gần nhất mà không vượt 14.400tr/năm. Bảng chỉ tiêu Manulife và quy định cấp bậc (0013M04/2024) không có. |
| A9 | Thời điểm | Cả năm 2026; hệ số K2 Manulife đổi từ 04/2026 | Manulife: tháng 1–3 hệ số 115%, từ tháng 4 hệ số 110% ở K2 85%. |

## 3. Quy đổi chức danh ngang hàng

| Cấp trong bài | AIA Alpha | Chubb Life | Manulife | Nguồn |
|---|---|---|---|---|
| Cấp 1 — Trưởng nhóm | UM (CQL) | AL — UM | UM — ❓ không có tài liệu | 2601-034 tr.2; 0008V tr.3 |
| Cấp 2 — Trưởng ban | SUM (CQL) | AL — SM | SUM — ❓ | như trên |
| Cấp 3 — Trưởng khu vực | DM (CQL) | AL — DM | DM — ❓ | như trên |
| Cấp 3B — Lãnh đạo vùng | PAF+ (DSRF) | RD | PSM/SM hoặc HKD1/2 | 2601-035; 0003V; 0048M01 |

Biểu phí CQL của AIA **không phân biệt UM/SUM/DM**: cấp bậc chỉ ảnh hưởng điều kiện thăng/giữ cấp và việc được hưởng gián tiếp. Chubb phân biệt theo cấp ở phí gián tiếp: UM chỉ có L1, SM có L1–L2, DM có L1–L3 (0008V tr.7).

## 4.1. Cấp 1 — Trưởng nhóm (UM): 5 ĐL, 150tr FYP/th

FYC tổ chức = 45,0tr/tháng. FYC nhóm trực tiếp của người quản lý = 45,0tr/tháng.

| Khoản (tr/tháng) | AIA Alpha | Chubb Life | Manulife |
|---|---:|---:|---:|
| (1) Phí dịch vụ trực tiếp hàng tháng | 11,7 | 32,4 | ❓ |
| (2) Trợ cấp / phí cố định | — *(không có khoản này)* | — *(không có khoản này)* | ❓ |
| (3) Override gián tiếp (trên quản lý con) | — | — | ❓ |
| (4) Thưởng quý quy đổi tháng | 3,6 | 16,2 | ❓ |
| (5) Thưởng năm quy đổi tháng (**trả chậm**) | 2,2 | — *(không có khoản này)* | ❓ |
| (6) Phí duy trì HĐ theo RYC | — *(không có khoản này)* | 5,6 | ❓ |
| **Tổng được hưởng / tháng** | **17,6** | **54,2** | ❓ |
| Trong đó tiền mặt năm 2026 | 15,3 | 54,2 | ❓ |
| % FYP tổ chức | 11,7% | 36,1% | ❓ |

**Evidence từng con số:**

| Hãng · khoản | tr/tháng | File PDF · mục · trang | Công thức với số của kịch bản |
|---|---:|---|---|
| AIA · (1a) tuyển dụng hiệu quả | 8,1 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.I · tr.3 | FYC nhóm 45,0 × 18% (bậc ≥20tr, FY ≥80%) |
| AIA · (1b) tuyển dụng chất lượng | 3,6 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.II · tr.3 | FYC nhóm 45,0 × 8% (≥4 lượt CVTV hoạt động) × hệ số FY 100% (FY ≥70%) |
| AIA · (4) quý | 3,6 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.V.1–2 · tr.4–5 | FYC quý 135,0 × 8% (4 sao: FYC quý, lượt hoạt động quý, CVTV mới ≥1 Q1 / ≥2 Q2+, FY ≥75%) |
| AIA · (5) năm, trả chậm | 2,2 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.VI · tr.5 | FYC năm 540,0 × 5% (4 sao toàn năm = ≥3 quý). Trả 15% (01/2028), 25% (01/2029), 60% (01/2030) nếu còn là CQL và TOT ≥85% |
| Chubb · (1) HT KTN tháng | 32,4 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.2.1 · tr.5 | FYC NTT 45,0 × 60% (≥40tr, EHC ≥4, ≥15 tháng QL) × 120% (K2 NTT ≥80%) |
| Chubb · (4) HT KTN quý | 16,2 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.2.2 · tr.6 | Tổng phí HT KTN tháng trong quý × 50% (FYC NTT quý 135,0 ≥100tr) |
| Chubb · (6) duy trì chất lượng HĐ | 5,6 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.5 · tr.9–10 | RYC NTT quý 111,7 (A8) × 15% (3MAA NTT ≥5), K2 NTT ≥65%, ≥13 tháng |
| AIA · (2) / Chubb · (2) trợ cấp cố định | — | 2601-034 mục A–B; 0008V tr.3 bảng tóm tắt | Văn bản không có khoản trợ cấp cố định cho CQL/AL (`VERIFIED FACT`: đã đọc đủ mục lục) |
| Manulife · mọi khoản | ❓ | — | Biểu phí UM/SUM/DM của Manulife không có trong 7 PDF (`SRC-GAP-002`) → `UNKNOWN` |

## 4.2. Cấp 2 — Trưởng ban (BM): 15 ĐL, 450tr FYP/th

FYC tổ chức = 135,0tr/tháng. FYC nhóm trực tiếp của người quản lý = 45,0tr/tháng.

| Khoản (tr/tháng) | AIA Alpha | Chubb Life | Manulife |
|---|---:|---:|---:|
| (1) Phí dịch vụ trực tiếp hàng tháng | 11,7 | 32,4 | ❓ |
| (2) Trợ cấp / phí cố định | — *(không có khoản này)* | — *(không có khoản này)* | ❓ |
| (3) Override gián tiếp (trên quản lý con) | 8,1 | 32,4 | ❓ |
| (4) Thưởng quý quy đổi tháng | 3,6 | 16,2 | ❓ |
| (5) Thưởng năm quy đổi tháng (**trả chậm**) | 2,2 | — *(không có khoản này)* | ❓ |
| (6) Phí duy trì HĐ theo RYC | — *(không có khoản này)* | 5,6 | ❓ |
| **Tổng được hưởng / tháng** | **25,7** | **86,6** | ❓ |
| Trong đó tiền mặt năm 2026 | 23,4 | 86,6 | ❓ |
| % FYP tổ chức | 5,7% | 19,2% | ❓ |

**Evidence từng con số:**

| Hãng · khoản | tr/tháng | File PDF · mục · trang | Công thức với số của kịch bản |
|---|---:|---|---|
| AIA · (1a) tuyển dụng hiệu quả | 8,1 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.I · tr.3 | FYC nhóm 45,0 × 18% (bậc ≥20tr, FY ≥80%) |
| AIA · (1b) tuyển dụng chất lượng | 3,6 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.II · tr.3 | FYC nhóm 45,0 × 8% (≥4 lượt CVTV hoạt động) × hệ số FY 100% (FY ≥70%) |
| AIA · (3) gián tiếp | 8,1 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.III · tr.4 | 50% × phí A của 2 CQL con (8,1/tháng mỗi người); A = phí tuyển dụng hiệu quả tháng của CQL con |
| AIA · (4) quý | 3,6 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.V.1–2 · tr.4–5 | FYC quý 135,0 × 8% (4 sao: FYC quý, lượt hoạt động quý, CVTV mới ≥1 Q1 / ≥2 Q2+, FY ≥75%) |
| AIA · (5) năm, trả chậm | 2,2 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.VI · tr.5 | FYC năm 540,0 × 5% (4 sao toàn năm = ≥3 quý). Trả 15% (01/2028), 25% (01/2029), 60% (01/2030) nếu còn là CQL và TOT ≥85% |
| Chubb · (1) HT KTN tháng | 32,4 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.2.1 · tr.5 | FYC NTT 45,0 × 60% (≥40tr, EHC ≥4, ≥15 tháng QL) × 120% (K2 NTT ≥80%) |
| Chubb · (3) quản lý nhóm | 32,4 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.3 · tr.7 | L1 50% × HT KTN tháng của 2 AL con (32,4/tháng mỗi người); tỷ lệ L theo FYC NTT của chính AL (45,0 ≥30tr) |
| Chubb · (4) HT KTN quý | 16,2 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.2.2 · tr.6 | Tổng phí HT KTN tháng trong quý × 50% (FYC NTT quý 135,0 ≥100tr) |
| Chubb · (6) duy trì chất lượng HĐ | 5,6 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.5 · tr.9–10 | RYC NTT quý 111,7 (A8) × 15% (3MAA NTT ≥5), K2 NTT ≥65%, ≥13 tháng |
| AIA · (2) / Chubb · (2) trợ cấp cố định | — | 2601-034 mục A–B; 0008V tr.3 bảng tóm tắt | Văn bản không có khoản trợ cấp cố định cho CQL/AL (`VERIFIED FACT`: đã đọc đủ mục lục) |
| Manulife · mọi khoản | ❓ | — | Biểu phí UM/SUM/DM của Manulife không có trong 7 PDF (`SRC-GAP-002`) → `UNKNOWN` |

## 4.3. Cấp 3 — Trưởng khu vực (DM): 45 ĐL, 1,2 tỷ FYP/th

FYC tổ chức = 360,0tr/tháng. FYC nhóm trực tiếp của người quản lý = 40,0tr/tháng.

| Khoản (tr/tháng) | AIA Alpha | Chubb Life | Manulife |
|---|---:|---:|---:|
| (1) Phí dịch vụ trực tiếp hàng tháng | 10,4 | 28,8 | ❓ |
| (2) Trợ cấp / phí cố định | — *(không có khoản này)* | — *(không có khoản này)* | ❓ |
| (3) Override gián tiếp (trên quản lý con) | 21,6 | 86,4 | ❓ |
| (4) Thưởng quý quy đổi tháng | 3,2 | 14,4 | ❓ |
| (5) Thưởng năm quy đổi tháng (**trả chậm**) | 2,0 | — *(không có khoản này)* | ❓ |
| (6) Phí duy trì HĐ theo RYC | — *(không có khoản này)* | 5,0 | ❓ |
| **Tổng được hưởng / tháng** | **37,2** | **134,6** | ❓ |
| Trong đó tiền mặt năm 2026 | 35,2 | 134,6 | ❓ |
| % FYP tổ chức | 3,1% | 11,2% | ❓ |

**Evidence từng con số:**

| Hãng · khoản | tr/tháng | File PDF · mục · trang | Công thức với số của kịch bản |
|---|---:|---|---|
| AIA · (1a) tuyển dụng hiệu quả | 7,2 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.I · tr.3 | FYC nhóm 40,0 × 18% (bậc ≥20tr, FY ≥80%) |
| AIA · (1b) tuyển dụng chất lượng | 3,2 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.II · tr.3 | FYC nhóm 40,0 × 8% (≥4 lượt CVTV hoạt động) × hệ số FY 100% (FY ≥70%) |
| AIA · (3) gián tiếp | 21,6 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.III · tr.4 | 50% × phí A của 4 CQL con (7,2/tháng mỗi người) + 25% × phí A của 4 UM cấp dưới nữa; A = phí tuyển dụng hiệu quả tháng của CQL con |
| AIA · (4) quý | 3,2 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.V.1–2 · tr.4–5 | FYC quý 120,0 × 8% (4 sao: FYC quý, lượt hoạt động quý, CVTV mới ≥1 Q1 / ≥2 Q2+, FY ≥75%) |
| AIA · (5) năm, trả chậm | 2,0 | AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha · A.VI · tr.5 | FYC năm 480,0 × 5% (4 sao toàn năm = ≥3 quý). Trả 15% (01/2028), 25% (01/2029), 60% (01/2030) nếu còn là CQL và TOT ≥85% |
| Chubb · (1) HT KTN tháng | 28,8 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.2.1 · tr.5 | FYC NTT 40,0 × 60% (≥40tr, EHC ≥4, ≥15 tháng QL) × 120% (K2 NTT ≥80%) |
| Chubb · (3) quản lý nhóm | 86,4 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.3 · tr.7 | L1 50% × HT KTN tháng của 4 AL con (28,8/tháng mỗi người) + L2 25% × HT KTN tháng của 4 UM báo cáo cấp 1; tỷ lệ L theo FYC NTT của chính AL (40,0 ≥30tr) |
| Chubb · (4) HT KTN quý | 14,4 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.2.2 · tr.6 | Tổng phí HT KTN tháng trong quý × 50% (FYC NTT quý 120,0 ≥100tr) |
| Chubb · (6) duy trì chất lượng HĐ | 5,0 | CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL) · II.5 · tr.9–10 | RYC NTT quý 99,3 (A8) × 15% (3MAA NTT ≥5), K2 NTT ≥65%, ≥13 tháng |
| AIA · (2) / Chubb · (2) trợ cấp cố định | — | 2601-034 mục A–B; 0008V tr.3 bảng tóm tắt | Văn bản không có khoản trợ cấp cố định cho CQL/AL (`VERIFIED FACT`: đã đọc đủ mục lục) |
| Manulife · mọi khoản | ❓ | — | Biểu phí UM/SUM/DM của Manulife không có trong 7 PDF (`SRC-GAP-002`) → `UNKNOWN` |

## 4.4. Cấp 3B — cùng khu vực 45 ĐL / 1,2 tỷ FYP/tháng, xếp vào tuyến lãnh đạo vùng

Đây là **tầng duy nhất có tài liệu của cả 3 hãng**. Khác cấp 3 ở trên: người quản lý ký hợp đồng dịch vụ quản lý cấp cao, có phí cơ bản/cố định và hưởng trên toàn tổ chức.

| Khoản (tr/tháng) | AIA PAF+ DSRF | Chubb RD | Manulife PSM (35tr) |
|---|---:|---:|---:|
| (2) Phí cơ bản / cố định | 86,7 | 45,0 | 45,5 |
| (1) Phí theo năng suất / chất lượng tháng | 30,9 | 43,2 | 24,0 |
| (4) Phí quý | 17,2 | 9,0 | 10,0 |
| (5) Năm / dài hạn | 10,0 *(thưởng vượt chỉ tiêu)* | — | 25,5 *(trả chậm 30/30/40)* |
| (6) Theo RYC | — | 89,4 | — |
| **Tổng / tháng** | **144,8** | **186,6** | **105,1** |
| % FYP | 12,1% | 15,5% | 8,8% |

**Evidence:**

| Hãng · khoản | File · mục · trang | Công thức / giả định riêng |
|---|---|---|
| AIA PAF+ | AIAV/AD/2601-035 — CS thu nhập 2026 cho PAF+ Alpha · tr.4–6 (phí), tr.9–10 (chỉ tiêu) | Bậc DSRF năm 1: phí cơ bản 80tr × 120% ở tháng đạt ≥115% chỉ tiêu FYP tháng, × 100% ở tháng đạt 55–115% (chỉ tiêu tháng có hệ số mùa vụ, bảng tr.9–10); phí chuyên môn tháng/quý theo % FYC × hệ số FY 120% (FY ≥75%); phí vượt chỉ tiêu = (FYP năm − 12.000) × 5%, tối đa bằng phí cơ bản năm. **Chưa cộng** phần Dual Career (PAF+ đồng thời nhận phí CQL, `AIA-PF-001` chưa mô hình). |
| Chubb RD | CHH0DCEB260003V — Phí dịch vụ Giám đốc vùng (RD), bản scan · II.1–II.6 · tr.5–10 | Đào tạo 25tr (FYP theo cấp báo cáo ≥400tr, ≥4 lớp); hoạt động 8tr (EHC ≥20); kinh doanh 12tr (FYP ≥600tr); chất lượng 12% FYC (3MAA ≥12) × 100% (K2 ≥60%); tăng trưởng quý **2,5%** (tăng trưởng 0% — giả định FYP đi ngang); RYC × 30% (K2 ≥70%, RYC theo A8). **Chưa cộng** phí trên BD (II.7–II.8) vì thiếu chính sách BD. |
| Manulife PSM | 0048M01/2026/ASBD — Biểu phí dịch vụ PSM+ & HKD · A.I–A.IV · tr.1–5 | Phí cơ bản 35tr × **100% đạt chỉ tiêu FYP** × 130%; năng suất 6% FYC (<115%) × hệ số TLDTHD (115% tháng 1–3, 110% từ tháng 4); hoạt động quý 2,5% (đạt 100% chỉ tiêu 1mAA); dài hạn 75% × (năng suất + hoạt động), trần 12 × 35tr, trả 30/30/40% trong 3 năm. **Bảng chỉ tiêu FYP/1mAA không có** → % đạt là `ASSUMPTION`. |

## 5. Độ nhạy — những giả định làm đổi kết luận

| Thay đổi | AIA | Chubb | Ý nghĩa |
|---|---:|---:|---|
| Cấp 1, **không tuyển mới** trong năm | 11,7 (từ 17,6) | 54,2 (không đổi) | AIA khóa thưởng quý & năm vào tuyển dụng; Chubb không. |
| Cấp 2, cả 15 ĐL **trực tiếp** (không có UM con) | 82,4 (từ 25,7) | 162,6 (từ 86,6) | Cả hai hãng trả **nhiều hơn** khi quản lý giữ đội phẳng → động cơ không phát triển quản lý con. |

## 6. Đã kiểm chứng gì & đã sửa gì so với bản cũ

Đối chiếu với **7 PDF gốc** (SHA-256 khớp `knowledge/sources/source-registry.csv`). Bản Chubb RD là bản scan nên được đọc bằng ảnh trang.

| # | Phát hiện | Bằng chứng | Xử lý |
|---|---|---|---|
| F1 | Chubb AL — phí HT KTN quý: engine và workbook dùng ngưỡng **55tr**, PDF ghi **50tr** cho bậc 40% | 0008V tr.6 "Từ 50 đến dưới 75 → 40%"; catalog `CHB-MG-004` ghi đúng | Đã sửa engine + workbook; test `tests/test_pdf_table_fixes.py` |
| F2 | Chubb RD — phí quản lý hoạt động theo EHC: engine sai mức tiền và ngưỡng (6,0/4,5/3,0 tại 16/12/8) | 0003V tr.6: 8,0 / 6,5 / 5,0 / 3,5 / 2,5 / 1,5 tại 20/16/12/9/6/4; catalog `CHB-RD-003` ghi đúng | Đã sửa engine + workbook; test |
| F3 | Chubb RD — phí quản lý kinh doanh theo FYP: engine có bậc 240→4,5 không tồn tại, thiếu 270→5,0 và 180→3,5 | 0003V tr.6; catalog `CHB-RD-004` ghi đúng | Đã sửa engine + workbook; test |
| F4 | Chubb RD — phí tăng trưởng quý: engine 7 bậc; 0–5% trả 5% (PDF 2,5%), tăng trưởng âm trả 2,5% (PDF 0%) | 0003V tr.8: 12 bậc, bước 2,5% mỗi 5% tăng trưởng | Đã sửa engine (`rd_growth_rate`); golden GT-16a: Chubb 99,21% → **99,96%** FYP ở K2 82% |
| F5 | Chubb AL — **thiếu** phí duy trì chất lượng HĐ (10–15% RYC NTT) dù catalog ghi `IMPLEMENTED` | 0008V tr.9–10, `CHB-MG-008` | Đã thêm tham số tùy chọn (mặc định không phát sinh → kết quả cũ giữ nguyên) |
| F6 | AIA CQL — engine chỉ có gián tiếp cấp 2 (50%), **thiếu cấp 3 (25%) và cấp 4 (12,5%)** | 2601-034 tr.4 mục III | Đã thêm tham số tùy chọn |
| F7 | Bộ 7 PDF **không có** biểu phí Manulife cấp UM/SUM/DM | `SRC-GAP-002` | Giữ `UNKNOWN`, không điền 0 |
| F8 | "HKD tối ưu thuế & chi phí" chưa có căn cứ trong tài liệu | 0048M01: cùng biểu phí cho PSM+ và HKD; mục C.9–C.10 chỉ khác cách khấu trừ thuế | Ghi `HYPOTHESIS` — cần Pháp chế/Thuế |

Đã kiểm khớp, không sửa: AIA CQL (A.I–A.VI, B), Chubb AL tháng / L1–L3 / hệ số K2, Chubb RD đào tạo và chất lượng 3MAA, Manulife A.I–A.IV.

## 7. TJ cần quyết trước Giai đoạn 2

1. **Cấu trúc A5** (cấp 2 = 5 trực tiếp + 2 UM con; cấp 3 = 5 + 2 BM + 2 UM) có đúng ý TJ không? Nếu TJ muốn "phẳng" thì số đổi mạnh (mục 5).
2. **Cấp 3 so ở tuyến nào:** quản lý trung gian (AIA DM · Chubb DM · Manulife ❓) hay lãnh đạo vùng (PAF+ · RD · PSM — đủ 3 hãng)?
3. **FYC/FYP = 30%** cho cả 3 hãng, hay TJ có cơ cấu sản phẩm thật để quy đổi?

