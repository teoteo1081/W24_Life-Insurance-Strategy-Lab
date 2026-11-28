# 02 — Phân tích hành vi, Trade-off & ROI 3 tầng (Giai đoạn 2)

> Số 3 hãng = `MODEL_OUTPUT`; số Chính sách Đề xuất 2026 = `PROPOSAL`. **"ROI" ở đây là chi phí / FYP và chi phí / phí còn duy trì — KHÔNG phải ROI thực tế** (VNB, biên lợi nhuận, OpEx thật = `UNKNOWN`). Số Manulife dựa trên 2 văn bản chính sách thu nhập 2026 của Manulife.

**Mô hình tổ chức dùng chung (`ASSUMPTION`):** khu vực Mốc 4 — 45 đại lý × 26,7tr FYP/tháng (1,2 tỷ), 1 lãnh đạo (5 ĐL trực tiếp) + 2 trưởng ban (5 ĐL + 2 trưởng nhóm) + 6 trưởng nhóm. Lãnh đạo: AIA PAF · Chubb RD · Manulife PSM/SM (đạt 100% chỉ tiêu) · Chính sách Đề xuất 2026: lãnh đạo vùng. Chi phí năm đầu = hoa hồng FYC + thưởng + phí quản lý; không gồm tái tục.

## 1. ROI 3 tầng

| Phương án | (1) Tổng chi / FYP — K2 85% | (1b) Khi năng suất −50% | (2) Chi phí / phí còn duy trì — K2 85% | (2) K2 65% | Chi trả giảm khi K2 sập | (3) Tiền mặt năm 1 | (3) Trả các năm sau | Phần cố định | Biểu phí nguồn | Nhãn |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| AIA Alpha | 58,4% | 54,3% | 68,7% | 78,4% | 12,7% | 97,4% | 2,6% | 3,4% | [AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7] | `MODEL_OUTPUT` |
| Chubb Life | 88,1% | 73,4% | 103,6% | 106,7% | 21,3% | 100,0% | 0,0% | 4,3% | [CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10] | `MODEL_OUTPUT` |
| Manulife | 50,8% | 44,9% | 59,8% | 73,0% | 6,7% | 95,8% | 4,2% | 7,5% | [0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5] | `MODEL_OUTPUT` |
| **Chính sách Đề xuất 2026** | 61,1% | 57,4% | 71,9% | 67,8% | 27,9% | 87,5% | 12,5% | 7,7% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |

**Kiểm trần theo kịch bản** (Mốc 4 chuẩn cho mỗi ĐL 26,7tr FYP — DƯỚI quota 30tr, nên trợ cấp Full-time không bật; vì vậy phải kiểm thêm kịch bản đạt quota):

| Phương án | Kịch bản | Tổng chi / FYP | Phần cố định | Nguồn | Nhãn |
|---|---|---:|---:|---|---|
| AIA Alpha | Mốc 4 chuẩn (26,7tr/ĐL) **(xấu nhất)** | 58,4% | 3,4% | [AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7] | `MODEL_OUTPUT` |
| AIA Alpha | Mọi ĐL đạt quota 30tr | 57,9% | 3,1% | [AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7] | `MODEL_OUTPUT` |
| Chubb Life | Mốc 4 chuẩn (26,7tr/ĐL) **(xấu nhất)** | 88,1% | 4,3% | [CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10] | `MODEL_OUTPUT` |
| Chubb Life | Mọi ĐL đạt quota 30tr | 87,7% | 3,8% | [CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10] | `MODEL_OUTPUT` |
| Manulife | Mốc 4 chuẩn (26,7tr/ĐL) | 50,8% | 7,5% | [0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5] | `MODEL_OUTPUT` |
| Manulife | Mọi ĐL đạt quota 30tr **(xấu nhất)** | 51,4% | 7,4% | [0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5] | `MODEL_OUTPUT` |
| **Chính sách Đề xuất 2026** | Mốc 4 chuẩn (26,7tr/ĐL) | 61,1% | 7,7% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | Mọi ĐL đạt quota 30tr | 70,6% | 20,1% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V2, năng suất ngang V1 | 61,1% | 7,7% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V3, năng suất ngang V1 | 69,9% | 19,3% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V4, năng suất ngang V1 | 69,0% | 18,2% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V1, mọi ĐL đạt đúng quota vùng (30,00tr) | 70,6% | 20,1% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V2, mọi ĐL đạt đúng quota vùng (26,70tr) | 71,1% | 20,6% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V3, mọi ĐL đạt đúng quota vùng (23,40tr) | 71,8% | 21,4% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V4, mọi ĐL đạt đúng quota vùng (21,00tr) | 72,4% | 22,0% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V1, điểm gãy cao nhất của lưới quét (183,33tr FYP/ĐL, K2 85%) | 73,4% | 3,2% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V2, điểm gãy cao nhất của lưới quét (163,17tr FYP/ĐL, K2 85%) | 73,6% | 3,3% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V3, điểm gãy cao nhất của lưới quét (143,00tr FYP/ĐL, K2 85%) | 73,9% | 3,4% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | V4, điểm gãy cao nhất của lưới quét (128,33tr FYP/ĐL, K2 85%) **(xấu nhất)** | 74,2% | 3,5% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |

Lưới quét điểm gãy Chính sách Đề xuất 2026: 261 điểm (4 vùng × năng suất quanh quota vùng, mọi bậc thưởng tháng, ngưỡng nhất quán, MDRT, năng suất V1 × K2 80/85/95%); 0 điểm vượt trần 75%. Bản nháp trước bỏ sót kịch bản V3 đạt đúng quota vùng (76,2% — VƯỢT); bản này đã nhân trợ cấp Full-time theo hệ số vùng và giãn mọi ngưỡng đại lý theo vùng.

**Độ nhạy cơ cấu sản phẩm — tỷ lệ hoa hồng năm đầu 25% / 30% / 40% FYP** (40% ≈ nghiêng bảo vệ thuần/tử kỳ, >50% HĐ mới 9T/2026 — `SOURCE_CLAIM`). Chính sách Đề xuất 2026 tính thưởng & phí quản lý trên **FYC chuẩn hóa = FYP × 30%** (hoa hồng vẫn theo sản phẩm) và có **trần quỹ thu nhập cây đại lý 75% FYP**: vượt trần thì thưởng & phí quản lý biến đổi co theo cùng tỷ lệ. 3 hãng trả trên FYC thật theo văn bản của họ. Trần 75% là trần quỹ thu nhập cây đại lý, KHÔNG phải tổng chi phí khai thác trên BCTC (gồm thêm văn phòng, marketing, bancassurance — wheel-check r2 câu 3).

| Phương án | Hoa hồng 25% — chuẩn | 25% — xấu nhất | Hoa hồng 30% — chuẩn | 30% — xấu nhất | Hoa hồng 40% — chuẩn | 40% — xấu nhất | Quỹ thưởng còn trả ở 40% xấu nhất | Nguồn | Nhãn |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| AIA Alpha | 49,3% | 49,3% | 58,4% | 58,4% | 79,4% | 88,6% | — | [AIAVAD 2601-034 : 3-6], [AIAVAD 2601-035 : 2-5], [AIAVAD 2604-069 : 3-7] | `MODEL_OUTPUT` |
| Chubb Life | 69,4% | 69,4% | 88,1% | 88,1% | 116,2% | 116,2% | — | [CHH0DCEB260007V : 4-7], [CHH0DCEB260008V : 5-10], [CHH0DCEB260003V : 5-10] | `MODEL_OUTPUT` |
| Manulife | 43,0% | 43,5% | 50,8% | 51,4% | 74,8% | 75,0% | — | [0046M01_2026 : 1-8], [0047M01_2026 : 1-3], [0048M01_2026 : 1-5] | `MODEL_OUTPUT` |
| **Chính sách Đề xuất 2026** | 56,1% | 69,2% | 61,1% | 74,2% | 71,1% | 75,0% | 85,8% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |

- **Tầng 1:** trần đề xuất 75% FYP, kiểm ở kịch bản xấu nhất. Chính sách Đề xuất 2026 74,2% (V4, điểm gãy cao nhất của lưới quét (128,33tr FYP/ĐL, K2 85%)) → **ĐẠT** trần, khoảng dư chỉ 0,8 điểm %. Rủi ro định phí thật của Chính sách Đề xuất 2026 là khi **nhiều** đại lý đạt quota, không phải khi năng suất giảm.
- **Điều 52 TT 67/2023** (thưởng + hỗ trợ đại lý, không gồm hoa hồng, ≤ 30% FYP phí định kỳ — `CONDITIONAL`): AIA Alpha 5,4% (xấu nhất 5,4%) · Chubb Life 16,4% (xấu nhất 16,4%) · Manulife 4,5% (xấu nhất 4,5%) · **Chính sách Đề xuất 2026** 4,1% (xấu nhất 24,8%) — tất cả **ĐẠT**. Phí quản lý tính là phí dịch vụ (NĐ 97/2026), cùng định nghĩa với mô hình enterprise. `MODEL_OUTPUT` / Chính sách Đề xuất 2026 `PROPOSAL`.
  - Vì sao Chính sách Đề xuất 2026 nhảy từ 4,1% lên 24,8%: kịch bản xấu nhất (V4, điểm gãy cao nhất của lưới quét (128,33tr FYP/ĐL, K2 85%)) là đại lý năng suất rất cao, chạm bậc thưởng tháng cao nhất và MDRT, nên phần thưởng (không gồm hoa hồng) tăng mạnh so với FYP; ở mốc chuẩn 26,7tr FYP/ĐL đa số đại lý chỉ ở bậc thưởng thấp. Mức xấu nhất vẫn dưới trần 30%, khoảng dư 5,2 điểm %.
- **Tầng 2:** chi phí trên mỗi đồng phí còn duy trì sang năm 2 = chi phí ÷ (FYP × K2). Khi K2 sập 85%→65%, phương án gắn thưởng với K2 tốt thì chi trả **giảm theo**; phương án yếu thì chi phí trên phí còn lại **tăng vọt**.
- **Tầng 3:** phần trả các năm sau (AIA thưởng năm 15/25/60% đến 2030; Manulife phí dài hạn 30/30/40%, M-Star năm trả tháng 2 năm sau; Chính sách Đề xuất 2026 trả chậm khi K2 ≥80%) giữ người và giảm áp lực tiền mặt năm 1.

## 1b. Vế doanh số — phải bán thêm bao nhiêu để hòa vốn (`PROPOSAL`)

**Cách đo (chỉ dùng số của mô hình, không giả định biên lợi nhuận — biên lợi nhuận thật = `UNKNOWN`):** phần phí giữ lại sau chi trả kênh đại lý = FYP × (1 − tổng chi/FYP). Hòa vốn = mức FYP mà phần giữ lại của Chính sách Đề xuất 2026 bằng phần giữ lại nếu công ty trả theo cơ chế của từng hãng ở mức FYP hiện tại (1,2 tỷ/tháng). Đây **không phải lợi nhuận**: chưa trừ chi phí văn phòng, marketing, dự phòng nghiệp vụ.

- **Thêm đại lý** (giữ cơ cấu năng suất): tỷ lệ chi phí gần như không đổi → FYP cần thêm = (1 − chi phí hãng) ÷ (1 − chi phí đề xuất) − 1.
- **Tăng năng suất mỗi đại lý**: thưởng lũy tiến làm tỷ lệ chi phí đổi theo — mô hình tính lại từng bước +0,5%; cột "bền" là mức mà từ đó trở lên luôn hòa vốn (qua được vách quota 30tr).

| Cơ cấu đại lý | So với | Chi phí hãng | Chi phí đề xuất | Chi thêm (tỷ/năm, cùng FYP) | Hòa vốn bằng thêm ĐL | Hòa vốn bằng năng suất | Năng suất (bền) | Nguồn | Nhãn |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| Bán đều 26,7tr/ĐL | AIA Alpha | 58,4% | 61,1% | 0,40 | +7,2% | +6,5% | +32,5% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| Bán đều 26,7tr/ĐL | Chubb Life | 88,1% | 61,1% | -3,88 | đã có lợi ở cùng FYP | đã có lợi ở cùng FYP | đã có lợi ở cùng FYP | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| Bán đều 26,7tr/ĐL | Manulife | 50,8% | 61,1% | 1,49 | +26,6% | +63,5% | +63,5% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| 4 nhóm năng suất | AIA Alpha | 61,6% | 68,5% | 0,99 | +21,8% | +18,0% | +18,0% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| 4 nhóm năng suất | Chubb Life | 91,5% | 68,5% | -3,32 | đã có lợi ở cùng FYP | đã có lợi ở cùng FYP | đã có lợi ở cùng FYP | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| 4 nhóm năng suất | Manulife | 57,2% | 68,5% | 1,62 | +35,8% | +29,5% | +58,0% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |

**Phân bổ năng suất 4 nhóm** (`ASSUMPTION`, cùng tổng 45 ĐL × 1,2 tỷ FYP/tháng): 7 ĐL «Không hoạt động» 0,0tr · 13 ĐL «Thấp» 10,0tr · 15 ĐL «Nòng cốt» 20,0tr · 10 ĐL «Top / MDRT» 77,0tr. Khi bán không đều, tổng chi/FYP tăng ở mọi phương án vì nhóm Top chạm bậc thưởng cao: AIA Alpha 58,4% → 61,6% · Chubb Life 88,1% → 91,5% · Manulife 50,8% → 57,2% · **Chính sách Đề xuất 2026** 61,1% → 68,5%. Chính sách Đề xuất 2026 vẫn dưới trần 75%; thu nhập đại lý theo nhóm (tr/tháng, năm đầu): 0,0tr → 0,0 · 10,0tr → 3,0 · 20,0tr → 6,8 · 77,0tr → 35,6.

**Chỉ tiêu đo cho thí điểm** (không cần giả định thêm): số đại lý có hợp đồng trong tháng, FYP/đại lý hoạt động, tỷ lệ đại lý đạt quota, K2 (≥ 85%), tỷ lệ đại lý mới còn hoạt động sau 13 tháng, và tổng chi/FYP so với trần 75% — đo hằng tháng ở văn phòng thí điểm và văn phòng đối chứng.

## 2. Bẫy hành vi (Gaming) & điểm gãy

| Hãng | Bẫy | Đo được | Trích dẫn | Nhãn |
|---|---|---|---|---|
| AIA Alpha | Tự bán vs quản lý thuần | Đại lý Mốc 1 18,1 tr/th; quản lý nhóm 5 người (phí thuần) 17,6 tr/th → quản lý thu ÍT hơn tự bán | [AIAVAD 2601-034 : 3-5] | `MODEL_OUTPUT` |
| AIA Alpha | Bẫy giữ đội phẳng | Ban 15 ĐL: để phẳng (15 trực tiếp) 82,4 vs có 2 quản lý con 25,7 tr/th → tỷ lệ 3,21× | [AIAVAD 2601-034 : 3-5] | `MODEL_OUTPUT` |
| AIA Alpha | Vách đá K2 tại 80% | Quản lý nhóm: K2 80% → 79% làm phí năm giảm 7,7% | [AIAVAD 2601-034 : 3-5] | `MODEL_OUTPUT` |
| Chubb Life | Tự bán vs quản lý thuần | Đại lý Mốc 1 22,5 tr/th; quản lý nhóm 5 người (phí thuần) 48,6 tr/th → quản lý thu nhiều hơn tự bán (chưa gồm khoản Duy trì chất lượng HĐ tính trên RYC — vì vậy thấp hơn cột Tổng của Chubb UM ở bảng 01) | [CHH0DCEB260008V : 5-7] | `MODEL_OUTPUT` |
| Chubb Life | Bẫy giữ đội phẳng | Ban 15 ĐL: để phẳng (15 trực tiếp) 145,8 vs có 2 quản lý con 81,0 tr/th → tỷ lệ 1,80× | [CHH0DCEB260008V : 5-7] | `MODEL_OUTPUT` |
| Chubb Life | Vách đá K2 tại 80% | Quản lý nhóm: K2 80% → 79% làm phí năm giảm 16,7% | [CHH0DCEB260008V : 5-7] | `MODEL_OUTPUT` |
| Manulife | Tự bán vs quản lý thuần | Đại lý Mốc 1 17,8 tr/th; quản lý nhóm 5 người (phí thuần) 11,0 tr/th → quản lý thu ÍT hơn tự bán | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| Manulife | Bẫy giữ đội phẳng | Ban 15 ĐL: để phẳng (15 trực tiếp) 40,5 vs có 2 quản lý con 18,2 tr/th → tỷ lệ 2,23× | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| Manulife | Vách đá K2 tại 80% | Quản lý nhóm: K2 80% → 79% làm phí năm giảm 1,2% | [0047M01_2026 : 1-2] | `MODEL_OUTPUT` |
| **Chính sách Đề xuất 2026** | Tự bán vs quản lý thuần | Đại lý Mốc 1 23,2 tr/th; quản lý nhóm 5 người (phí thuần) 27,3 tr/th → quản lý thu nhiều hơn tự bán | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | Bẫy giữ đội phẳng | Ban 15 ĐL: để phẳng (15 trực tiếp) 65,9 vs có 2 quản lý con 40,8 tr/th → tỷ lệ 1,61× | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | Vách đá K2 tại 80% | Quản lý nhóm: K2 80% → 79% làm phí năm giảm 21,9% | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| AIA Alpha | Rủi ro định phí | Phần cố định 3,4% chi trả; năng suất giảm 50% → chi phí 54,3% FYP (từ 58,4%) | [AIAVAD 2601-035 : 3] | `MODEL_OUTPUT` |
| Chubb Life | Rủi ro định phí | Phần cố định 4,3% chi trả; năng suất giảm 50% → chi phí 73,4% FYP (từ 88,1%) | [CHH0DCEB260003V : 5-6] | `MODEL_OUTPUT` |
| Manulife | Rủi ro định phí | Phần cố định 7,5% chi trả; năng suất giảm 50% → chi phí 44,9% FYP (từ 50,8%) | [0048M01_2026 : 1] | `MODEL_OUTPUT` |
| **Chính sách Đề xuất 2026** | Rủi ro định phí | Phần cố định 7,7% chi trả; năng suất giảm 50% → chi phí 57,4% FYP (từ 61,1%) | PROPOSAL | `PROPOSAL` |
| Manulife | Độ nhạy danh hiệu MBA Pro (Vàng) | UM+ Mốc 2: không danh hiệu 11,0 → MBA Pro Vàng 22,2 tr/th (phí hoạt động 50%→100% + phí dài hạn 100%) | [0047M01_2026 : 2], [0047M01_2026 : 5] | `HYPOTHESIS` |
| **Chính sách Đề xuất 2026** | Vách đá K2 của đại lý Full-time | Đại lý Full-time 30tr FYP: K2 80% → 79% làm thu nhập năm giảm 23,6% (13,1 → 10,0 tr/th) vì mất trọn trợ cấp — số này không gồm tái tục; con số Mốc 1 ở bảng 01 gồm tái tục (A7) và tính ở K2 85% nên cao hơn | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| **Chính sách Đề xuất 2026** | Vách đá quota & dồn hợp đồng | FYP 30 → 29,9tr/tháng: thu nhập 13,2 → 10,2 tr/th — động cơ dồn/chuyển hợp đồng giữa các tháng để chạm quota (HYPOTHESIS về hành vi) | PROPOSAL (hybrid_scheme.py) | `PROPOSAL` |
| AIA Alpha | Cổng tuyển mới | Quản lý nhóm AIA: có tuyển (1/2/2/2 người mới/quý) 17,6 vs không tuyển 11,7 tr/th | [AIAVAD 2601-034 : 4-5] | `MODEL_OUTPUT` |

Đọc nhanh: (a) **tự bán vs quản lý** — ở AIA và Manulife, lên quản lý nhóm 5 người mà bỏ bán thì thu nhập giảm; (b) **đội phẳng** — tỷ lệ >1 nghĩa là giữ mọi người trực tiếp có lợi hơn phát triển quản lý con; (c) **vách đá K2** — giảm 1 điểm K2 quanh 80% làm mất một bậc hệ số; (d) **định phí** — phí cố định không co khi năng suất giảm.

## 3. Rubric 5 trụ cột (Compensation Designer) — bản DEC-19

**Cổng đạt/trượt (xét trước điểm, không bù trừ):**

| Phương án | Cổng | Giá trị | Giới hạn | Kết quả |
|---|---|---:|---:|---|
| AIA Alpha | Điều 52 TT 67/2023: thưởng + hỗ trợ đại lý ≤ 30% FYP ở kịch bản xấu nhất (CONDITIONAL) | 5,4% | 30,0% | ĐẠT |
| Chubb Life | Điều 52 TT 67/2023: thưởng + hỗ trợ đại lý ≤ 30% FYP ở kịch bản xấu nhất (CONDITIONAL) | 16,4% | 30,0% | ĐẠT |
| Manulife | Điều 52 TT 67/2023: thưởng + hỗ trợ đại lý ≤ 30% FYP ở kịch bản xấu nhất (CONDITIONAL) | 4,5% | 30,0% | ĐẠT |
| **Chính sách Đề xuất 2026** | Điều 52 TT 67/2023: thưởng + hỗ trợ đại lý ≤ 30% FYP ở kịch bản xấu nhất (CONDITIONAL) | 24,9% | 30,0% | ĐẠT |
| **Chính sách Đề xuất 2026** | Cam kết thiết kế của Đề xuất: tổng chi trả kênh đại lý ≤ 75% FYP ở kịch bản xấu nhất (PROPOSAL) | 74,2% | 75,0% | ĐẠT |

**Điểm (chỉ xét phương án đạt mọi cổng):** trọng số 30/30/30 cho 3 vế đề bài (doanh số · chất lượng · chi phí) + 10 cho độ đơn giản. Mọi mốc chấm là `PROPOSAL` (chốt trước khi tính điểm, không có nguồn ngoài).

| Trụ cột (trọng số) | AIA Alpha | Chubb Life | Manulife | **Chính sách Đề xuất 2026** |
|---|---:|---:|---:|---:|
| Thúc đẩy doanh số (30%) | 4,08 | 4,08 | 3,37 | 3,27 |
| Chất lượng kinh doanh (hành vi) (30%) | 2,75 | 3,46 | 3,14 | 3,60 |
| Hiệu quả chi phí / ROI (30%) | 4,72 | 2,72 | 4,97 | 4,16 |
| Độ đơn giản & dễ tính (10%) | 2,20 | 1,40 | 3,00 | 4,60 |
| Vận hành & Pháp lý (không tính vào tổng) (0%) | 3,00 | 2,50 | 3,50 | 3,50 |
| **Điểm có trọng số (1–5)** | **3,69** | **3,22** | **3,74** | **3,77** |

Căn cứ từng điểm:

- **AIA Alpha:** *Thúc đẩy doanh số* — Động lực bán thêm: bán gấp 1,5 → thu nhập ×1,73 (hệ số 1,46; 1,0 = tăng đúng tỷ lệ = 1 điểm, ≥1,5 = 5 điểm) · Sức hút thu nhập so với hãng trả cao nhất trong 3 hãng: M1 80% · M2 36% · M3 32% · M4 100% (`MODEL_OUTPUT`); *Chất lượng kinh doanh (hành vi)* — Chi trả giảm 12,7% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc 3,21× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% 7,7% (≤5% = 5, ≥30% = 1) (`MODEL_OUTPUT`); *Hiệu quả chi phí / ROI* — Chi phí chuẩn 58,4% FYP (≤50% = 5, ≥90% = 1); kịch bản xấu nhất (Mốc 4 chuẩn (26,7tr/ĐL)) 58,4% (≤60% = 5, ≥100% = 1); năng suất −50% → 54,3% (≤70% = 5, ≥130% = 1) (`MODEL_OUTPUT`); *Độ đơn giản & dễ tính* — 11 khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): 2601-034 mục A.I–A.VI + B (7) [AIAVAD 2601-034 : 3-6]; 2601-035 mục A.1–A.4 (4) [AIAVAD 2601-035 : 3-5] (`MODEL_OUTPUT`); *Vận hành & Pháp lý (không tính vào tổng)* — Chấm công ≥50% (CQL) / ≥70% (PAF+), khóa học bắt buộc, trả chậm tới 2030 cần TOT ≥85% — nhiều cổng hành chính [AIAVAD 2601-034 : 3-5] (`JUDGEMENT`)
- **Chubb Life:** *Thúc đẩy doanh số* — Động lực bán thêm: bán gấp 1,5 → thu nhập ×1,65 (hệ số 1,30; 1,0 = tăng đúng tỷ lệ = 1 điểm, ≥1,5 = 5 điểm) · Sức hút thu nhập so với hãng trả cao nhất trong 3 hãng: M1 100% · M2 100% · M3 100% · M4 71% (`MODEL_OUTPUT`); *Chất lượng kinh doanh (hành vi)* — Chi trả giảm 21,3% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc 1,80× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% 16,7% (≤5% = 5, ≥30% = 1) (`MODEL_OUTPUT`); *Hiệu quả chi phí / ROI* — Chi phí chuẩn 88,1% FYP (≤50% = 5, ≥90% = 1); kịch bản xấu nhất (Mốc 4 chuẩn (26,7tr/ĐL)) 88,1% (≤60% = 5, ≥100% = 1); năng suất −50% → 73,4% (≤70% = 5, ≥130% = 1) (`MODEL_OUTPUT`); *Độ đơn giản & dễ tính* — 13 khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): 0008V mục II.1–II.5 (5) [CHH0DCEB260008V : 3]; 0003V mục II.1–II.8 (8) [CHH0DCEB260003V : 4] (`MODEL_OUTPUT`); *Vận hành & Pháp lý (không tính vào tổng)* — RD phải có biên bản nghiệm thu dịch vụ hàng tháng; 9 trường hợp tạm giữ phí; 3 văn bản quy định chung không có trong nguồn (260005V/006V/009V) [CHH0DCEB260003V : 12-15] (`JUDGEMENT`)
- **Manulife:** *Thúc đẩy doanh số* — Động lực bán thêm: bán gấp 1,5 → thu nhập ×1,67 (hệ số 1,34; 1,0 = tăng đúng tỷ lệ = 1 điểm, ≥1,5 = 5 điểm) · Sức hút thu nhập so với hãng trả cao nhất trong 3 hãng: M1 79% · M2 23% · M3 22% · M4 77% (`MODEL_OUTPUT`); *Chất lượng kinh doanh (hành vi)* — Chi trả giảm 6,7% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc 2,23× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% 1,2% (≤5% = 5, ≥30% = 1) (`MODEL_OUTPUT`); *Hiệu quả chi phí / ROI* — Chi phí chuẩn 50,8% FYP (≤50% = 5, ≥90% = 1); kịch bản xấu nhất (Mọi ĐL đạt quota 30tr) 51,4% (≤60% = 5, ≥100% = 1); năng suất −50% → 44,9% (≤70% = 5, ≥130% = 1) (`MODEL_OUTPUT`); *Độ đơn giản & dễ tính* — 9 khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): 0047M01 A.I–A.V (5) [0047M01_2026 : 1-5]; 0048M01 A.I–A.IV (4) [0048M01_2026 : 1-3] (`MODEL_OUTPUT`); *Vận hành & Pháp lý (không tính vào tổng)* — Hai hình thức hợp đồng PSM+/HKD cùng biểu phí, chuyển đổi bảo lưu kết quả; HKD tự xuất hóa đơn — tách rủi ro thuế [0048M01_2026 : 5-6]; điều kiện 'Đội ngũ chuyên cần' 4 buổi/tháng [0047M01_2026 : 3] (`JUDGEMENT`)
- ****Chính sách Đề xuất 2026**:** *Thúc đẩy doanh số* — Động lực bán thêm: bán gấp 1,5 → thu nhập ×1,61 (hệ số 1,21; 1,0 = tăng đúng tỷ lệ = 1 điểm, ≥1,5 = 5 điểm) · Sức hút thu nhập so với hãng trả cao nhất trong 3 hãng: M1 103% · M2 56% · M3 50% · M4 78% (`PROPOSAL`); *Chất lượng kinh doanh (hành vi)* — Chi trả giảm 27,9% khi K2 85%→65% (≥30% = 5 điểm); tỷ lệ đội phẳng/có cấu trúc 1,61× (≤1 = 5, ≥3 = 1); vách đá K2 80→79% 21,9% (≤5% = 5, ≥30% = 1) (`PROPOSAL`); *Hiệu quả chi phí / ROI* — Chi phí chuẩn 61,1% FYP (≤50% = 5, ≥90% = 1); kịch bản xấu nhất (V4, điểm gãy cao nhất của lưới quét (128,33tr FYP/ĐL, K2 85%)) 74,2% (≤60% = 5, ≥100% = 1); năng suất −50% → 57,4% (≤70% = 5, ≥130% = 1) (`PROPOSAL`); *Độ đơn giản & dễ tính* — 5 khoản phí tuyến quản lý (≤4 = 5, ≥14 = 1): cùng đơn vị đếm với 3 hãng — 1 khoản = 1 mục chi trả có công thức riêng (các đời gián tiếp cùng công thức gộp 1 như [AIAVAD 2601-034 : 4]; phần giữ lại của cùng khoản không tính riêng): override trực tiếp; phí gián tiếp (đời 1–2); thưởng trả chậm quản lý (quỹ riêng 12% FYC); phí cơ bản lãnh đạo; override lãnh đạo (gồm phần trả chậm giữ lại) (hybrid_scheme.py) (`PROPOSAL`); *Vận hành & Pháp lý (không tính vào tổng)* — Ít khoản, một cổng K2 ≥80% thống nhất; CHƯA đối chiếu pháp lý (TT 67/2023, NĐ 97/2026 — CONDITIONAL); trợ cấp Full-time cần quy trình xác nhận quota/CC (`PROPOSAL`)

> **Lưu ý thiên lệch:** bậc đệm K2 75–80% và trần đội phẳng của Chính sách Đề xuất 2026 được thêm SAU khi đo bằng rubric bản trước — thiết kế đã được hiệu chỉnh theo thước đo cũ, nên rubric không phải phép thử khách quan cho Chính sách Đề xuất 2026. DEC-19 (2026-11-28) sửa 4 điểm của bản trước: (1) ROI thêm chi phí ở kịch bản chuẩn, bỏ "tỷ lệ trả chậm" (đặc điểm thiết kế, không phải kết quả); (2) thêm trụ cột Thúc đẩy doanh số = động lực bán thêm + sức hút thu nhập so với 3 hãng (không so với chính đề xuất); (3) Vận hành & Pháp lý vẫn hiển thị nhưng không cộng vào tổng (đánh giá chủ quan, đề xuất tự chấm, pháp lý `CONDITIONAL`); (4) Điều 52 và trần 75% thành cổng đạt/trượt.

> 4 trụ cột tính điểm đều bằng công thức công khai ở trên; *Độ đơn giản* đếm khoản phí theo mục lục văn bản; *Vận hành & Pháp lý* là đánh giá có dẫn chứng (`JUDGEMENT`), chỉ để tham khảo. Điểm Chính sách Đề xuất 2026 là **tự chấm của bên thiết kế** — cần một bên độc lập chấm lại trước khi dùng làm kết luận.

## 4. Ghi chú độ nhạy Manulife MBA Pro (`HYPOTHESIS`)

UM+ Mốc 2: không danh hiệu 11,0 → MBA Pro Vàng 22,2 tr/th (phí hoạt động 50%→100% + phí dài hạn 100%) `[0047M01_2026 : 2]`, `[0047M01_2026 : 5]`. Tiêu chí danh hiệu (0050M01/2026) không có trong nguồn — chưa đưa vào base case.

## 5. Pháp lý tham chiếu

Rổ thưởng + hỗ trợ đại lý / FYP trên mô hình khu vực 45 ĐL (ngưỡng 30% Điều 52, `CONDITIONAL / SOURCE_NOT_VERIFIED`): AIA 5,4% (xấu nhất 5,4%), Chubb 16,4% (xấu nhất 16,4%), Manulife 4,5% (xấu nhất 4,5%), Hybrid 4,1% (xấu nhất 24,8%). Từ 01/01/2027, Điều 17 TT 96/2026 thêm trần 7% cho phí nộp 1 lần (`SOURCE_CLAIM`). Cần Pháp chế đối chiếu ảnh trang Điều 51–52 trong 44/2026/VBHN-TT-BTC trước khi ban hành.

## 6. Negative Proof — kết luận "không có trong nguồn" của báo cáo này

| Kết luận | Đã quét | Là 1 trong 9 file nguồn? | Trang có nhắc tới (chỉ dẫn chiếu, không phải nội dung) |
|---|---|---|---|
| Tiêu chí danh hiệu MBA Pro / Manulife Pro (0050M01/2026) | 9/9 file (tên file + toàn văn từng trang) | KHÔNG | 0046M01_2026: `Manulife Pro` [3, 4, 5, 6, 10]; 0047M01_2026: `0050M01` [2, 3], `MBA Pro` [2, 3, 5], `Manulife Pro` [3, 5] |
| Quy định chung Chubb 260005V / 260006V / 260009V | 9/9 file (tên file + toàn văn từng trang) | KHÔNG | CHH0DCEB260007V: `260005V` [3, 4]; CHH0DCEB260008V: `260005V` [3], `260006V` [3], `260009V` [12] |

## 7. Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)

| # | Tiêu chí (`qa/data-ingestion-rubric.md`) | Điểm | Tối đa | Căn cứ đo được |
|---|---|---:|---:|---|
| 1 | Độ phủ nguồn 9/9 file | 25.0 | 25 | 9/9 file mở được và khớp SHA-256; bản scan soát 15/15 trang |
| 2 | Chức danh gốc & tuyến | 25.0 | 25 | 3/3 chức danh có tên nguyên văn khớp trang trích (hoặc đối chiếu bằng mắt với bản scan) và có `track_type` |
| 3 | Trích dẫn `[File : Trang]` cho từng con số | 19.3 | 20 | 52/54 dòng có số mang trích dẫn đúng mẫu |
| 4 | Negative Proof | 15.0 | 15 | 2/2 kết luận "không có trong tài liệu" kèm nhật ký tìm kiếm |
| 5 | Tách Fact / Assumption | 14.7 | 15 | 53/54 dòng có nhãn phân loại |
| | **Tổng** | **99.0** | **100** | **PASS** (ngưỡng 90) — máy đếm trên chính các bảng, đo độ phủ trích dẫn & nhãn, không phải điểm chất lượng phân tích |

Tiêu chí 1 theo kiểm kê `00_Role_Mapping_Audit.md` (9/9 file khớp SHA-256, 15/15 trang scan). Tiêu chí 2: 3 chức danh lãnh đạo Mốc 4 (AIA PAF, Chubb RD, Manulife PSM/SM) lấy từ ma trận `00_Role_And_Benefit_Matrix.md`. Tiêu chí 3/5 đếm tự động mọi dòng bảng có số ở mục 1–2 (dòng Chính sách Đề xuất 2026 trích `PROPOSAL (hybrid_scheme.py)` vì không có trong PDF).
