# 01 — Bảng soi tiền theo 4 mốc quy mô & Evidence

> **Trạng thái:** `MODEL_OUTPUT` trên kịch bản chuẩn (`ASSUMPTION`) — chờ TJ duyệt Giai đoạn 1. Không phải thu nhập thực tế, không phải ROI thực tế.
> Sinh bởi `scripts/build_interview_income_table.py` từ engine; chức danh từng mốc suy từ điều kiện thăng cấp (`scripts/w24_milestones.py`). Kiểm kê nguồn & Negative Proof: `outputs/interview/00_Role_Mapping_Audit.md`.
> Đơn vị: **triệu VNĐ / tháng** = thu nhập được hưởng cả năm (gồm phần trả chậm) ÷ 12, **trước thuế TNCN**.

## 1. Kết luận nhanh — mỗi ô ghi chức danh, thu nhập, nguồn điều kiện thăng cấp, nguồn biểu phí

| Mốc | Hãng | Chức danh · tr/tháng (Mốc 1: thu nhập cá nhân; Mốc 2–4: phí quản lý thuần) | Nguồn điều kiện thăng cấp | Nguồn biểu phí tính tiền | Ghi chú / lý do ❓ | Nhãn |
|---|---|---|---|---|---|---|
| Mốc 1 — Cá nhân | AIA | **SA** · 18,1 | [AIAVAD 2601-034 : 8] (SA→UM chưa đạt: cần ≥2 người tuyển trong 6 tháng) | [AIAVAD 2604-069 : 3-7] | Hoa hồng FYC/tái tục theo giả định A1, A7 (biểu hoa hồng AIA không có trong nguồn) | `MODEL_OUTPUT` |
| Mốc 1 — Cá nhân | Chubb | **AR** · 22,5 | [CHH0DCEB260007V : 7] (AR→UM chưa đạt: cần 2 đại lý giới thiệu đạt 3MAA) | [CHH0DCEB260007V : 4-7], hoa hồng [CHH0DCEB260007V : 13-19] | Tỷ lệ hoa hồng theo sản phẩm có trong Phụ đính II; cơ cấu sản phẩm theo A1 | `MODEL_OUTPUT` |
| Mốc 1 — Cá nhân | Manulife | **Đại Lý** · 17,8 | — điều kiện lên UM+ ở 0013M04/2024 (không có trong nguồn) [0047M01_2026 : 6] | [0046M01_2026 : 1-8] | Hoa hồng cơ bản theo thông báo sản phẩm [0046M01_2026 : 9] → giả định A1, A7 | `MODEL_OUTPUT` |
| Mốc 2 — Nhóm 6 người | AIA | **SUM** · 17,6 | [AIAVAD 2601-034 : 8] (đạt SUM; DM cần ≥1 UM+ trực tiếp) | [AIAVAD 2601-034 : 3-5] | Phí CQL không phân biệt UM/SUM | `MODEL_OUTPUT` |
| Mốc 2 — Nhóm 6 người | Chubb | **UM** · 54,2 | [CHH0DCEB260007V : 7] (SM cần ≥1 AL trực tiếp) | [CHH0DCEB260008V : 5-10] | — | `MODEL_OUTPUT` |
| Mốc 2 — Nhóm 6 người | Manulife | **UM+** · 11,0 | — bậc trong UM+ theo 0013M04/2024 (không có) [0047M01_2026 : 6] | [0047M01_2026 : 1-3] | Không có danh hiệu MBA Pro (tiêu chí 0050M01/2026 không có) → không có phí dài hạn A.V | `MODEL_OUTPUT` |
| Mốc 3 — Ban 15 người | AIA | **SDM** · 25,7 | [AIAVAD 2601-034 : 8] (PAF cần ≥3 UM+ trực tiếp) | [AIAVAD 2601-034 : 3-5] | — | `MODEL_OUTPUT` |
| Mốc 3 — Ban 15 người | Chubb | **DM** · 86,6 | [CHH0DCEB260007V : 7] (BD cần 3MAA ≥20, ≥4 AL trực tiếp) | [CHH0DCEB260008V : 5-10] | — | `MODEL_OUTPUT` |
| Mốc 3 — Ban 15 người | Manulife | **UM+** · 18,2 | — như Mốc 2 [0047M01_2026 : 6] | [0047M01_2026 : 1-3] | Cấp 2 = ½ tỷ lệ cấp 1 | `MODEL_OUTPUT` |
| Mốc 4 — Khu vực 45 người | AIA | **PAF** · 136,3 | [AIAVAD 2601-034 : 8] (SDM→PAF đạt); [AIAVAD 2601-035 : 6] (AF cần ≥5 UM+) | [AIAVAD 2601-035 : 2-5] + phí CQL trực tiếp [AIAVAD 2601-034 : 3-5] | Không còn phí gián tiếp cấp 2–4 [AIAVAD 2601-035 : 2] | `MODEL_OUTPUT` |
| Mốc 4 — Khu vực 45 người | Chubb | **RD** (bổ nhiệm) · 186,6 — *so sánh chính* | RD bổ nhiệm theo hợp đồng [CHH0DCEB260003V : 3]; chức danh đạt bằng chỉ tiêu là BD [CHH0DCEB260007V : 7] | [CHH0DCEB260003V : 5-10] | Phụ (tuyến quản lý truyền thống): DM 134,6 [CHH0DCEB260008V : 5-10]. BD: biểu phí không có trong nguồn — Negative Proof `00_Role_Mapping_Audit.md` mục 4.3 | `MODEL_OUTPUT` |
| Mốc 4 — Khu vực 45 người | Manulife | **PSM/SM** (bổ nhiệm) · 105,1 — *so sánh chính* | PSM+ bổ nhiệm; điều kiện bậc ở 0013M04/2024 (không có) [0048M01_2026 : 5] | [0048M01_2026 : 1-5] | Đạt 100% chỉ tiêu là giả định A8. Phụ: UM+ 28,9 [0047M01_2026 : 1-3] | `MODEL_OUTPUT` |

> **Mốc 2–4 là PHÍ QUẢN LÝ THUẦN, KHÔNG gồm hoa hồng/thưởng tự bán của quản lý** (giả định A3). Vì vậy Mốc 2 của AIA (17,6) và Manulife (11,0) thấp hơn Mốc 1 (đại lý tự bán 30tr FYP). Nếu quản lý vẫn tự bán như Mốc 1, cộng thêm khoảng: AIA 18,1, Chubb 22,5, Manulife 17,8 tr/tháng. Mốc 4 so sánh chính theo tuyến lãnh đạo vùng (AIA PAF · Chubb RD · Manulife PSM/SM); số tuyến quản lý truyền thống (Chubb DM · Manulife UM+) ở cột ghi chú.

### 1.1. Giải trình các ô ❓ và số tham chiếu

**Manulife.** Đã có đủ 3 văn bản: `0046M01_2026` (Đại Lý), `0047M01_2026` (UM+), `0048M01_2026` (PSM+/HKD). Còn 3 chỗ phải giả định, có ghi trong bảng: (a) hoa hồng cơ bản theo từng sản phẩm không có trong 0046M01 `[0046M01_2026 : 9]`; (b) bậc cụ thể trong UM+ và điều kiện lên PSM+ nằm ở 0013M04/2024 `[0047M01_2026 : 6]`; (c) danh hiệu Manulife Pro / MBA Pro (0011M04/2024, 0050M01/2026) — mặc định **không có danh hiệu** nên không có thưởng KDXS năm, thưởng xuất sắc tháng, phí dài hạn A.V. Nhật ký tìm kiếm: `00_Role_Mapping_Audit.md` mục 4.3.

**Chubb BD Mốc 4.** Khu vực 45 người đạt điều kiện DM → BD `[CHH0DCEB260007V : 7]`. BD thuộc Ban Điều hành và Phát triển Kinh doanh (AMD) `[CHH0DCEB260003V : 3]`, không còn là AL nên không hưởng biểu phí AL (bảng tóm tắt 0008V chỉ có AR/UM/SM/DM `[CHH0DCEB260008V : 3]`). Biểu phí của chính BD không nằm trong file nào: 0003V áp dụng cho RD `[CHH0DCEB260003V : 3]` và chỉ nhắc tên 6 khoản phí của BD để làm căn cứ tính phí cho RD quản lý `[CHH0DCEB260003V : 10-11]`. Hai số DM (134,6) và RD (186,6) là **tham chiếu**: DM là nếu người đó chưa nhận thăng cấp, RD là chức danh do công ty bổ nhiệm theo hợp đồng, không phải chức danh đạt được bằng chỉ tiêu.

**Đọc nhanh:**
- Cùng quy mô, **chức danh đạt được khác nhau**: nhóm 5 đại lý đủ điều kiện **SUM** ở AIA nhưng chỉ **UM** ở Chubb; ban 15 đại lý là **SDM** (AIA) và **DM** (Chubb); khu vực 45 đại lý lên **PAF** (AIA) và **BD** (Chubb).
- Ở tuyến quản lý (Mốc 2–3), **Chubb trả khoảng 3,1–3,4 lần AIA** cho cùng đội ngũ: Chubb trả 60% FYC nhóm × 120% (K2 ≥80%) + 50% mỗi quý; AIA trả 8–24% FYC nhóm.
- Ở Mốc 4, AIA chuyển sang tuyến **PAF+** có phí cố định và vẫn giữ phí CQL trên nhóm trực tiếp ("con đường sự nghiệp kép"), nhưng **mất phí gián tiếp cấp 2–4** `[AIAVAD 2601-035 : 2]`.
- **AIA thưởng quý cần người mới có hoạt động:** **3 sao cần ≥1 người/quý**; **4–5 sao cần ≥1 ở Q1/2026 và ≥2 từ Q2/2026** `[AIAVAD 2601-034 : 4]`.
- **Manulife UM+ trả thấp nhất ở tuyến quản lý**: 11,0 / 18,2 / 28,9 tr/tháng ở Mốc 2/3/4 — chỉ 10–20% FYC cấp 1 (`[0047M01_2026 : 1]`) và phí hoạt động tính trên **thưởng** của đại lý chứ không trên FYC (`[0047M01_2026 : 1-2]`). Không có danh hiệu MBA Pro thì mất phí dài hạn.

### 1.2. Ghi chú độ nhạy — Manulife có danh hiệu MBA Pro / Manulife Pro (chạy ở Giai đoạn 2, `HYPOTHESIS`)

Base case = **không có danh hiệu** (tiêu chí ở 0050M01/2026 và 0011M04/2024, không có trong 9 PDF). Nếu có MBA Pro: phí hoạt động nhóm UM+ tăng từ 50% lên 100% (4–5 người sản xuất) hoặc 125% (≥6) `[0047M01_2026 : 2]`, phí phát triển đại lý mới từ 50% lên 100% `[0047M01_2026 : 3]`, thêm phí hợp tác dài hạn 80/100/125% × (A.II + A.III), trả chậm 30/30/40% `[0047M01_2026 : 5-6]`. Đại lý có Manulife Pro: thêm thưởng xuất sắc tháng và thưởng KDXS năm `[0046M01_2026 : 4-7]`.

## 2. Giả định chung (`ASSUMPTION`)

| # | Giả định | Giá trị | Ghi chú |
|---|---|---|---|
| A1 | FYC / FYP | 30% | Thiếu biểu hoa hồng AIA và memo FYC tín chỉ (00 mục 4). AIA tính trên **FYC tín chỉ**, coi = FYC. |
| A2 | Tỷ lệ duy trì | K2 = FY = TLDTHD = 85% | Công thức gốc từng hãng nằm ở văn bản không có trong nguồn (260005V, 0016M03/2024). |
| A3 | Quản lý tự bán | 2 HĐ / 6 tháng (để giữ điều kiện AIA), FYC không đáng kể | So sánh thuần thu nhập quản lý ở Mốc 2–4. |
| A4 | Hoạt động | Mọi đại lý hoạt động mỗi tháng, ≥1 HĐ và ≥4tr FYC; Chubb: mọi đại lý đạt EHC/3MAA | Định nghĩa EHC ở 260005V (không có trong nguồn). |
| A5 | Cấu trúc | Theo `knowledge/policies/scale-milestones.json` | Mốc 2: 1 QL + 5 ĐL; Mốc 3: + 2 quản lý con × 5; Mốc 4: 5 trực tiếp + 2 ban con + 2 nhóm con. |
| A6 | Tuyển mới | CVTV mới có hoạt động/quý: [1, 2, 2, 2] | Đủ cho 4–5 sao AIA và 3MAA mới của Chubb. |
| A7 | Tái tục | RYC/năm = FYP × K2 × 20% + FYP × K2 × 0.92 × 10% | Giả định chung của repo; chỉ HĐ năm 2–3. |
| A8 | Mốc 4 | AIA PAF năm 1; Manulife PSM/SM phí cơ bản 35tr, đạt 100% chỉ tiêu; Chubb RD FYP đi ngang | Bảng chỉ tiêu Manulife không có trong nguồn. |

## 3. Chi tiết từng mốc — mỗi con số kèm trích dẫn

### Mốc 1 — Cá nhân — 1 đại lý, 30,0tr FYP/tháng (FYC 9,0tr)

| Hãng · chức danh | Khoản | tr/tháng | Công thức với số của kịch bản | Trích dẫn | Nhãn |
|---|---|---:|---|---|---|
| AIA · SA | Hoa hồng trực tiếp (FYC) | 9,0 | FYC 9,0/tháng (A1) | — | `ASSUMPTION` |
| AIA · SA | Hoa hồng tái tục năm 2–3 | 7,4 | A7 | — | `ASSUMPTION` |
| AIA · SA | Trợ cấp cố định | — | Không có cho SA (trợ cấp Exchange/Pro nằm ở văn bản riêng, không có trong nguồn) | [AIAVAD 2604-069 : 3] | `VERIFIED FACT` |
| AIA · SA | Thưởng sản xuất quý | 1,1 | % theo FYC tín chỉ quý × hệ số FY | [AIAVAD 2604-069 : 5] | `MODEL_OUTPUT` |
| AIA · SA | Thưởng Chuyên viên Ngoại hạng quý | 0,5 | Theo danh hiệu sao quý | [AIAVAD 2604-069 : 6] | `MODEL_OUTPUT` |
| AIA · SA | Thưởng chất lượng phục vụ (SYC) quý | 0,0 | % SYC quý | [AIAVAD 2604-069 : 6] | `MODEL_OUTPUT` |
| AIA · SA | Thưởng sản xuất năm | 0,0 | % FYC năm × hệ số FY | [AIAVAD 2604-069 : 7] | `MODEL_OUTPUT` |
| **AIA · SA** | **Tổng** | **18,1** | FYC + SYC + thưởng + tái tục năm 3 | [AIAVAD 2604-069 : 5-7] | `MODEL_OUTPUT` |
| Chubb · AR | Hoa hồng trực tiếp (FYC) | 9,0 | FYC 9,0/tháng (A1); tỷ lệ theo sản phẩm ở Phụ đính II | [CHH0DCEB260007V : 13-19] | `ASSUMPTION` |
| Chubb · AR | Hoa hồng tái tục (RYC) | 7,4 | A7 | — | `ASSUMPTION` |
| Chubb · AR | Trợ cấp cố định | — | Không có trong bảng tóm tắt 5 khoản thu nhập | [CHH0DCEB260007V : 3] | `VERIFIED FACT` |
| Chubb · AR | Thưởng HQKD tháng | 3,8 | FYC × 35% (FYC 3 tháng 27,0tr: bậc 20–<40) × 120% (K2 ≥80%) | [CHH0DCEB260007V : 4] | `MODEL_OUTPUT` |
| Chubb · AR | Thưởng HQKD quý | 1,1 | 30% tổng thưởng tháng trong quý (3 tháng đạt EHC) | [CHH0DCEB260007V : 5-6] | `MODEL_OUTPUT` |
| Chubb · AR | Thưởng duy trì HĐ quý (RYC) | 1,1 | 15% RYC năm 2–5 (3 lượt EHC/quý, K2 ≥65%) | [CHH0DCEB260007V : 6-7] | `MODEL_OUTPUT` |
| **Chubb · AR** | **Tổng** | **22,5** | FYC + RYC + thưởng | [CHH0DCEB260007V : 4-7] | `MODEL_OUTPUT` |
| Manulife · Đại Lý | Hoa hồng trực tiếp (FYC) | 9,0 | FYC 9,0/tháng (A1); bảng hoa hồng theo thông báo sản phẩm (không có) | [0046M01_2026 : 9] | `ASSUMPTION` |
| Manulife · Đại Lý | Hoa hồng tái tục | 7,4 | A7 | — | `ASSUMPTION` |
| Manulife · Đại Lý | Trợ cấp cố định | — | Không có trong 8 khoản thưởng B.I–B.VIII | [0046M01_2026 : 2-8] | `VERIFIED FACT` |
| Manulife · Đại Lý | Thưởng năng suất tháng | 1,3 | FYC × 15% (FYC 3 tháng 27,0tr ≥15) × hệ số TLDTHD 100% | [0046M01_2026 : 4] | `MODEL_OUTPUT` |
| Manulife · Đại Lý | Thưởng năng suất quý | 0,0 | FYC quý 27,0tr < 30tr (mức 2, >6 tháng) → 0 | [0046M01_2026 : 5] | `MODEL_OUTPUT` |
| Manulife · Đại Lý | M-Star quý/năm | 0,0 | FYP lũy kế quý 1 = 90,0tr < 90% × 160tr → 0 | [0046M01_2026 : 7-8] | `MODEL_OUTPUT` |
| **Manulife · Đại Lý** | **Tổng** | **17,8** | FYC + tái tục + thưởng; không danh hiệu Manulife Pro | [0046M01_2026 : 4-8] | `MODEL_OUTPUT` |

### Mốc 2 — Nhóm 6 người — 5 đại lý, 150,0tr FYP/tháng; FYC nhóm trực tiếp 45,0tr

| Hãng · chức danh | Khoản | tr/tháng | Công thức với số của kịch bản | Trích dẫn | Nhãn |
|---|---|---:|---|---|---|
| AIA · SUM | Hoa hồng trực tiếp | — | Quản lý không tự bán đáng kể (A3) | — | `ASSUMPTION` |
| AIA · SUM | Trợ cấp cố định | — | Không có trong chính sách CQL | [AIAVAD 2601-034 : 3-7] | `VERIFIED FACT` |
| AIA · SUM | Phí tuyển dụng hiệu quả tháng | 8,1 | FYC nhóm 45,0 × 18% (≥20tr, FY ≥80%) | [AIAVAD 2601-034 : 3] | `MODEL_OUTPUT` |
| AIA · SUM | Phí tuyển dụng chất lượng tháng | 3,6 | FYC nhóm × 8% (≥4 lượt hoạt động) × 100% (FY ≥70%) | [AIAVAD 2601-034 : 3] | `MODEL_OUTPUT` |
| AIA · SUM | Phí quý (4 sao) | 3,6 | FYC quý 135,0 × 8% (≥80tr, ≥9 lượt, người mới theo A6) | [AIAVAD 2601-034 : 4-5] | `MODEL_OUTPUT` |
| AIA · SUM | Phí năm (trả chậm 15/25/60%) | 2,2 | FYC năm 540,0 × 5% (≥3 quý 4 sao); trả 2028–2030 nếu TOT ≥85% | [AIAVAD 2601-034 : 5] | `MODEL_OUTPUT` |
| **AIA · SUM** | **Tổng** | **17,6** | tiền mặt 2026: 15,3 | [AIAVAD 2601-034 : 3-5] | `MODEL_OUTPUT` |
| Chubb · UM | Hoa hồng trực tiếp | — | Quản lý không tự bán đáng kể (A3) | — | `ASSUMPTION` |
| Chubb · UM | Trợ cấp cố định | — | Không có trong bảng tóm tắt 5 khoản của AL | [CHH0DCEB260008V : 3] | `VERIFIED FACT` |
| Chubb · UM | HT KTN tháng | 32,4 | FYC NTT 45,0 × 60% (≥40tr, EHC ≥4, ≥15 tháng) × 120% (K2 ≥80%) | [CHH0DCEB260008V : 5] | `MODEL_OUTPUT` |
| Chubb · UM | HT KTN quý | 16,2 | Phí tháng trong quý × 50% (FYC NTT quý 135,0 ≥100tr) | [CHH0DCEB260008V : 6] | `MODEL_OUTPUT` |
| Chubb · UM | Duy trì chất lượng HĐ (RYC) | 5,6 | RYC NTT quý 111,7 (A7) × 15% (3MAA ≥5, K2 ≥65%) | [CHH0DCEB260008V : 9-10] | `MODEL_OUTPUT` |
| **Chubb · UM** | **Tổng** | **54,2** | trả tiền mặt trong năm | [CHH0DCEB260008V : 5-10] | `MODEL_OUTPUT` |
| Manulife · UM+ | Hoa hồng trực tiếp | — | Quản lý không tự bán đáng kể (A3) | — | `ASSUMPTION` |
| Manulife · UM+ | Trợ cấp cố định | — | Không có trong biểu phí UM+ (5 khoản A.I–A.V) | [0047M01_2026 : 1-6] | `VERIFIED FACT` |
| Manulife · UM+ | Phí năng suất nhóm (cấp 1–4) | 7,2 | Cấp 1 FYC 45,0 × 16% (24–<48) + cấp 2 0,0 × 8% + cấp 3 0,0 × 4% | [0047M01_2026 : 1] | `MODEL_OUTPUT` |
| Manulife · UM+ | Phí hoạt động nhóm | 3,8 | 50% (5 người sản xuất) × thưởng năng suất của cấp 1 × TLDTHD 115% (T1–3) / 110% | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| Manulife · UM+ | Phí hợp tác dài hạn | 0,0 | Chỉ cho MBA Pro (tiêu chí 0050M01/2026 không có) → 0 | [0047M01_2026 : 5] | `ASSUMPTION` |
| **Manulife · UM+** | **Tổng** | **11,0** | trả tiền mặt trong năm | [0047M01_2026 : 1-3] | `MODEL_OUTPUT` |

### Mốc 3 — Ban 15 người — 15 đại lý, 450,0tr FYP/tháng; FYC nhóm trực tiếp 45,0tr

| Hãng · chức danh | Khoản | tr/tháng | Công thức với số của kịch bản | Trích dẫn | Nhãn |
|---|---|---:|---|---|---|
| AIA · SDM | Hoa hồng trực tiếp | — | Quản lý không tự bán đáng kể (A3) | — | `ASSUMPTION` |
| AIA · SDM | Trợ cấp cố định | — | Không có trong chính sách CQL | [AIAVAD 2601-034 : 3-7] | `VERIFIED FACT` |
| AIA · SDM | Phí tuyển dụng hiệu quả tháng | 8,1 | FYC nhóm 45,0 × 18% (≥20tr, FY ≥80%) | [AIAVAD 2601-034 : 3] | `MODEL_OUTPUT` |
| AIA · SDM | Phí tuyển dụng chất lượng tháng | 3,6 | FYC nhóm × 8% (≥4 lượt hoạt động) × 100% (FY ≥70%) | [AIAVAD 2601-034 : 3] | `MODEL_OUTPUT` |
| AIA · SDM | Phí gián tiếp (CQL con) | 8,1 | 50% × phí A của 2 CQL con (8,1/tháng mỗi người) | [AIAVAD 2601-034 : 4] | `MODEL_OUTPUT` |
| AIA · SDM | Phí quý (4 sao) | 3,6 | FYC quý 135,0 × 8% (≥80tr, ≥9 lượt, người mới theo A6) | [AIAVAD 2601-034 : 4-5] | `MODEL_OUTPUT` |
| AIA · SDM | Phí năm (trả chậm 15/25/60%) | 2,2 | FYC năm 540,0 × 5% (≥3 quý 4 sao); trả 2028–2030 nếu TOT ≥85% | [AIAVAD 2601-034 : 5] | `MODEL_OUTPUT` |
| **AIA · SDM** | **Tổng** | **25,7** | tiền mặt 2026: 23,4 | [AIAVAD 2601-034 : 3-5] | `MODEL_OUTPUT` |
| Chubb · DM | Hoa hồng trực tiếp | — | Quản lý không tự bán đáng kể (A3) | — | `ASSUMPTION` |
| Chubb · DM | Trợ cấp cố định | — | Không có trong bảng tóm tắt 5 khoản của AL | [CHH0DCEB260008V : 3] | `VERIFIED FACT` |
| Chubb · DM | HT KTN tháng | 32,4 | FYC NTT 45,0 × 60% (≥40tr, EHC ≥4, ≥15 tháng) × 120% (K2 ≥80%) | [CHH0DCEB260008V : 5] | `MODEL_OUTPUT` |
| Chubb · DM | Quản lý nhóm L1 | 32,4 | 50% × HT KTN tháng của 2 AL con (32,4/tháng mỗi người) | [CHH0DCEB260008V : 7] | `MODEL_OUTPUT` |
| Chubb · DM | HT KTN quý | 16,2 | Phí tháng trong quý × 50% (FYC NTT quý 135,0 ≥100tr) | [CHH0DCEB260008V : 6] | `MODEL_OUTPUT` |
| Chubb · DM | Duy trì chất lượng HĐ (RYC) | 5,6 | RYC NTT quý 111,7 (A7) × 15% (3MAA ≥5, K2 ≥65%) | [CHH0DCEB260008V : 9-10] | `MODEL_OUTPUT` |
| **Chubb · DM** | **Tổng** | **86,6** | trả tiền mặt trong năm | [CHH0DCEB260008V : 5-10] | `MODEL_OUTPUT` |
| Manulife · UM+ | Hoa hồng trực tiếp | — | Quản lý không tự bán đáng kể (A3) | — | `ASSUMPTION` |
| Manulife · UM+ | Trợ cấp cố định | — | Không có trong biểu phí UM+ (5 khoản A.I–A.V) | [0047M01_2026 : 1-6] | `VERIFIED FACT` |
| Manulife · UM+ | Phí năng suất nhóm (cấp 1–4) | 14,4 | Cấp 1 FYC 45,0 × 16% (24–<48) + cấp 2 90,0 × 8% + cấp 3 0,0 × 4% | [0047M01_2026 : 1] | `MODEL_OUTPUT` |
| Manulife · UM+ | Phí hoạt động nhóm | 3,8 | 50% (5 người sản xuất) × thưởng năng suất của cấp 1 × TLDTHD 115% (T1–3) / 110% | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| Manulife · UM+ | Phí hợp tác dài hạn | 0,0 | Chỉ cho MBA Pro (tiêu chí 0050M01/2026 không có) → 0 | [0047M01_2026 : 5] | `ASSUMPTION` |
| **Manulife · UM+** | **Tổng** | **18,2** | trả tiền mặt trong năm | [0047M01_2026 : 1-3] | `MODEL_OUTPUT` |

### Mốc 4 — Khu vực 45 người — 45 đại lý, 1.200,0tr FYP/tháng (FYC 360,0tr)

| Hãng · chức danh | Khoản | tr/tháng | Công thức với số của kịch bản | Trích dẫn | Nhãn |
|---|---|---:|---|---|---|
| AIA · PAF | Phí cơ bản (cố định theo chức danh) | 24,0 | 20tr × 120% (đạt ≥115% chỉ tiêu FYP tháng) × hệ số chuyên cần 100% | [AIAVAD 2601-035 : 3] | `MODEL_OUTPUT` |
| AIA · PAF | Phí chuyên môn tháng | 38,5 | FYC × (6% × hệ số FY 120% + 3,5% theo 1mAA) | [AIAVAD 2601-035 : 4] | `MODEL_OUTPUT` |
| AIA · PAF | Phí chuyên môn quý | 34,2 | FYC quý × (5% × 120% + 3,5%) khi đạt ≥130% chỉ tiêu | [AIAVAD 2601-035 : 4-5] | `MODEL_OUTPUT` |
| AIA · PAF | Phí vượt chỉ tiêu | 24,0 | (FYP năm − 1.800) × 5%, tối đa = phí cơ bản năm | [AIAVAD 2601-035 : 5] | `MODEL_OUTPUT` |
| AIA · PAF | Phí CQL trên nhóm trực tiếp (Dual Career) | 15,6 | Như CQL: FYC nhóm 40,0 × 18% + 8% + quý 4 sao + năm 5%; KHÔNG có gián tiếp cấp 2–4 | [AIAVAD 2601-035 : 2] | `MODEL_OUTPUT` |
| **AIA · PAF** | **Tổng** | **136,3** | PAF+ + CQL trực tiếp | [AIAVAD 2601-035 : 2-5] | `MODEL_OUTPUT` |
| Chubb · BD | Mọi khoản | ❓ | Biểu phí dành cho BD (0003V chỉ dẫn chiếu "Chính sách 2026 dành cho BD") | Không có trong nguồn — Negative Proof: `00_Role_Mapping_Audit.md` mục 4.3 | `UNKNOWN` |
| Chubb · tham chiếu: nếu vẫn là DM (AL) | Tổng | 134,6 | HT KTN tháng + quý + L1 (4 AL con) + L2 (4 UM) + RYC | [CHH0DCEB260008V : 5-10] | `MODEL_OUTPUT` |
| Chubb · tham chiếu: RD (bổ nhiệm theo hợp đồng) | Tổng | 186,6 | Đào tạo 25 + hoạt động 8 + kinh doanh 12 + 12% FYC + tăng trưởng 2,5% (đi ngang) + 30% RYC; riêng RYC 89,4 | [CHH0DCEB260003V : 5-10] | `MODEL_OUTPUT` |
| Manulife · UM+ | Phí năng suất nhóm (cấp 1–4) | 25,6 | Cấp 1 FYC 40,0 × 16% + cấp 2 160,0 × 8% + cấp 3 160,0 × 4% | [0047M01_2026 : 1] | `MODEL_OUTPUT` |
| Manulife · UM+ | Phí hoạt động nhóm | 3,3 | 50% (5 người sản xuất) × thưởng năng suất của cấp 1 × hệ số TLDTHD | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| **Manulife · UM+** | **Tổng** | **28,9** | Bậc trong UM+ / điều kiện lên PSM+ ở 0013M04/2024 (không có trong nguồn) | [0047M01_2026 : 1-3] | `MODEL_OUTPUT` |
| Manulife · tham chiếu nếu được bổ nhiệm PSM/SM | Phí cơ bản | 45,5 | 35tr × 100% đạt chỉ tiêu × 130% (A8) | [0048M01_2026 : 1] | `ASSUMPTION` |
| Manulife · PSM/SM | Phí năng suất tháng | 24,0 | FYC × 6% (<115% chỉ tiêu) × TLDTHD 115% (T1–3) / 110% (từ T4) | [0048M01_2026 : 1-2] | `MODEL_OUTPUT` |
| Manulife · PSM/SM | Phí hoạt động quý | 10,0 | FYC quý × 2,5% (đạt 100% 1mAA) × hệ số TLDTHD | [0048M01_2026 : 2-3] | `MODEL_OUTPUT` |
| Manulife · PSM/SM | Phí hợp tác dài hạn (trả chậm 30/30/40%) | 25,5 | 75% × (năng suất + hoạt động), trần 12 × 35tr | [0048M01_2026 : 3-5] | `MODEL_OUTPUT` |
| **Manulife · PSM/SM** | **Tổng** | **105,1** | HKD cùng biểu phí; khác cách nộp thuế | [0048M01_2026 : 1-6] | `MODEL_OUTPUT` |

## 4. Đã kiểm chứng & đã sửa

| # | Nội dung | Trích dẫn | Nhãn |
|---|---|---|---|
| F1–F4 | Chubb AL quý 50tr; Chubb RD bảng EHC, bảng FYP, tăng trưởng 12 bậc — đã sửa engine + workbook (ca3304c) | [CHH0DCEB260008V : 6], [CHH0DCEB260003V : 6-8] | `VERIFIED FACT` |
| F5–F6 | Thêm phí RYC của AL (CHB-MG-008) và gián tiếp AIA cấp 3–4 (ca3304c) | [CHH0DCEB260008V : 9-10], [AIAVAD 2601-034 : 4] | `VERIFIED FACT` |
| P2 #1 | Có RYC mà thiếu 3MAA → báo `MISSING_INPUT`, không coi là 0 (có test) | [CHH0DCEB260008V : 10] | `VERIFIED FACT` |
| P2 #2 | `K2_NO_K2_YET` (chưa phát sinh → hệ số 100%, coi như đạt) tách khỏi `None` = UNKNOWN (báo lỗi); test xuyên suốt hàm cho AL 15 tháng | [CHH0DCEB260008V : 5], [CHH0DCEB260008V : 10] | `VERIFIED FACT` |
| P2 #3 | Điều kiện người mới AIA: 3 sao ≥1; 4–5 sao ≥1 ở Q1, ≥2 từ Q2 | [AIAVAD 2601-034 : 4] | `VERIFIED FACT` |
| G1 | PAF+ Dual Career: cộng phí CQL trực tiếp, bỏ gián tiếp cấp 2–4; chức danh Mốc 4 suy từ điều kiện (PAF) thay vì chọn tay | [AIAVAD 2601-035 : 2], [AIAVAD 2601-034 : 8] | `VERIFIED FACT` |
| G2 | Mâu thuẫn tên tiếng Việt UM/SUM/DM giữa các trang AIA — giữ mã làm khóa | [AIAVAD 2604-069 : 17] | `VERIFIED FACT` |
| G3 | Nạp 0046M01 (Đại Lý) và 0047M01 (UM+) — engine `calc_manulife_agent_12m`, `calc_manulife_um_12m`, test riêng | [0046M01_2026 : 1-9], [0047M01_2026 : 1-6] | `VERIFIED FACT` |

## 5. Quyết định của TJ (2026-11-27, DEC-14)

1. Chấp nhận phạm vi 9/9 PDF; giữ đánh dấu thiếu tài liệu cho Chubb BD và các memo ngoài phạm vi. Mốc 2–4 ghi rõ là **phí quản lý thuần**.
2. Manulife: base case **không có MBA Pro / Manulife Pro**; kịch bản có danh hiệu là ghi chú độ nhạy, chạy ở Giai đoạn 2.
3. Mốc 4: so sánh chính **AIA PAF · Chubb RD · Manulife PSM/SM**; số phụ **Chubb DM · Manulife UM+**.
4. Bảo mật: chỉ commit local, **không push** (0046M01 D.3 và 0047M01 B.4 ghi thông tin mật).

## 6. Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)

| # | Tiêu chí (`qa/data-ingestion-rubric.md`) | Điểm | Tối đa | Căn cứ đo được |
|---|---|---:|---:|---|
| 1 | Độ phủ nguồn 9/9 file | 25.0 | 25 | 9/9 file mở được và khớp SHA-256; bản scan soát 15/15 trang |
| 2 | Chức danh gốc & tuyến | 25.0 | 25 | 12/12 chức danh có tên nguyên văn khớp trang trích (hoặc đối chiếu bằng mắt với bản scan) và có `track_type` |
| 3 | Trích dẫn `[File : Trang]` cho từng con số | 18.9 | 20 | 71/75 dòng có số mang trích dẫn đúng mẫu |
| 4 | Negative Proof | 15.0 | 15 | 1/1 kết luận "không có trong tài liệu" kèm nhật ký tìm kiếm |
| 5 | Tách Fact / Assumption | 15.0 | 15 | 99/99 dòng có nhãn phân loại |
| | **Tổng** | **98.9** | **100** | **PASS** (ngưỡng 90) — máy đếm trên chính các bảng, đo độ phủ trích dẫn & nhãn, không phải điểm chất lượng phân tích |

Tiêu chí 1–2 dựa trên kiểm kê của `00_Role_Mapping_Audit.md` (9/9 file khớp hash, 15/15 trang scan; chức danh mỗi mốc suy từ điều kiện có trích dẫn). Tiêu chí 3 đếm các dòng có số ở mục 3; dòng giả định thuần (hoa hồng theo A1, tái tục theo A7) không có trang nguồn nên bị trừ điểm.
