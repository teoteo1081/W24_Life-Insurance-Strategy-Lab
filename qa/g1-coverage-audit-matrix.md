# Coverage Audit Matrix — Kiểm toán Độ bao phủ Toàn văn 7 Memo (116 Trang — Cập nhật Post-Audit)

**Ngày cập nhật:** 2026-11-26 (Post-Audit Remediation sau kiểm toán Codex tại `7bcf70e`)  
**Phạm vi:** 100% các trang, mục, phụ lục, bảng biểu và ví dụ trong 7 tài liệu chính sách gốc (`116 trang`).  
**Người thực hiện:** AGY (`SELF_VERIFIED` — tự kiểm toán nội bộ sau khi khắc phục các phát hiện của Codex; **KHÔNG** tuyên bố `INDEPENDENTLY_VERIFIED`).

---

## 1. Phân tách 7 Tầng Sẵn sàng Kiểm chứng & Tính toán (Không đánh đồng!)

> **Nguyên tắc Section 32:** Không bao giờ gộp `Đọc hết trang` = `Sẵn sàng tính toán`. Mọi tài liệu & quy tắc được tách bạch qua 7 tầng: **(1) READ → (2) UNDERSTOOD → (3) EXTRACTED → (4) NORMALIZED (Lookup) → (5) SOURCE_VERIFIED → (6) IMPLEMENTED (Python/Excel) → (7) TESTED (Golden + Excel COM Parity)**.

| Tài liệu (`Source_ID`) | (1) READ | (2) UNDERSTOOD | (3) EXTRACTED | (4) NORMALIZED | (5) SOURCE_VERIFIED | (6) IMPLEMENTED | (7) TESTED | Nguyên nhân chặn / Phụ thuộc còn lại |
|---|---|---|---|---|---|---|---|---|
| **AIA Alpha CVTV** (`2604-069`, 23p) | **ĐẠT (23/23)** | **ĐẠT** *(trừ VB ngoài)* | **ĐẠT (26 rules)** | **ĐẠT** *(không có bảng lớn ẩn)* | **MỘT PHẦN** *(1 xung đột `ERR-DOC-02` + 12 rule thiếu VB ngoài)* | **MỘT PHẦN** *(14/26 rule lõi)* | **CONDITIONAL / PASS** *(xem Catalog)* | Thiếu Phụ lục Hoa hồng, Memo `FYC Tín Chỉ`, `2501-017`, chính sách `Exchange/Pro`; `ERR-DOC-02` mở 2 toggle (`RoundUp` vs `HalfUp`). |
| **AIA Alpha CQL** (`2601-034`, 21p) | **ĐẠT (21/21)** | **ĐẠT** | **ĐẠT (16 rules)** | **ĐẠT** *(gồm luật 70% cap CQL)* | **MỘT PHẦN** *(8 rule phụ thuộc VB ngoài)* | **MỘT PHẦN** *(10/16 rule lõi)* | **CONDITIONAL / PASS** | Thiếu Memo `FYC Tín Chỉ`, `2601-023`, `2401-029`, quy định chấm công chi tiết. |
| **AIA Alpha PAF+** (`2601-035`, 18p) | **ĐẠT (18/18)** | **ĐẠT** | **ĐẠT (12 rules)** | **ĐẠT 100%** (`aia-paf-5y-targets.csv`: **1,300 dòng**, 0 sai số cộng!) | **MỘT PHẦN** *(4 rule phụ thuộc VB ngoài)* | **MỘT PHẦN** *(6/12 rule lõi)* | **CONDITIONAL / PASS** | Thiếu quy định Vitality hạng Vàng, quy định chấm công PAF+, `2511-169` (Q1/2026). |
| **Manulife PSM+/HKD** (`0048M01`, 6p) | **ĐẠT (6/6)** | **ĐẠT** | **ĐẠT (13 rules)** | **ĐẠT** | **MỘT PHẦN** *(6 rule phụ thuộc VB ngoài)* | **MỘT PHẦN** *(9/13 rule lõi)* | **CONDITIONAL / PASS** | Thiếu bảng chỉ tiêu FYP/1mAA, `0016M03/2024` (TLDTHD), TB mở C.1 (02/2026); thiếu toàn bộ tầng Đại lý FA & UM/DM. |
| **Chubb Life Đại lý** (`260007V`, 19p) | **ĐẠT (19/19)** | **ĐẠT** | **ĐẠT (16 rules)** | **ĐẠT 100%** (`chubb-product-commission-schedule.csv`: **113 dòng** + `chubb-hsbh-tiers.csv`: **10 khung tuổi**) | **MỘT PHẦN** *(1 xung đột `ERR-DOC-01` + 6 rule thiếu `260005V`)* | **MỘT PHẦN** *(11/16 rule lõi)* | **CONDITIONAL / PASS** | Thiếu `CHH0DCEB260005V` (ngưỡng `1 EHC`, công thức `K2/P13`, clawback tổng quát); `ERR-DOC-01` mở 2 toggle (`Table 80%` vs `Example 50%`). |
| **Chubb Life Quản lý AL** (`260008V`, 14p) | **ĐẠT (14/14)** | **ĐẠT** | **ĐẠT (10 rules)** | **ĐẠT** | **MỘT PHẦN** *(4 rule phụ thuộc `260005V/006V/009V`)* | **CAO** *(9/10 rule lõi)* | **CONDITIONAL / PASS** | Thiếu `260005V` (`EHC/K2`), `260006V` và `260009V` (Phí XD ĐVKD mới). |
| **Chubb Life GĐ Vùng RD** (`260003V`, 15p scan) | **ĐẠT (15/15 ảnh)** | **ĐẠT** | **ĐẠT (12 rules)** | **ĐẠT** | **MỘT PHẦN** *(6 rule phụ thuộc `260005V/006V` & chính sách `BD`)* | **CAO** *(9/12 rule lõi)* | **CONDITIONAL / PASS** | Thiếu `260005V/006V` và **Chính sách 2026 cho cấp `BD`** (đầu vào cho Mục II.7 & II.8 của RD). |

---

## 2. Ma trận Kiểm toán Độ bao phủ Theo Từng Tài liệu — Từng Trang — Từng Mục

**6 Nhãn phân loại chuẩn:**
- `[FULL]` — Đã hiểu và trích xuất đầy đủ thành Business Rule.
- `[UNDERSTOOD_NO_RULE]` — Đã hiểu nhưng chưa chuyển thành rule tính toán chi tiết (sẽ nạp bảng chi tiết khi xây mô hình).
- `[REF_ONLY]` — Nội dung tham khảo hành chính/truyền thông, không cần tính toán *(có giải thích căn cứ)*.
- `[UNCLEAR]` — Chưa hiểu rõ / Điều khoản mở chưa định nghĩa.
- `[CONFLICT]` — Có mâu thuẫn / lỗi nội tại trong chính tài liệu gốc.
- `[DEP_EXTERNAL]` — Phụ thuộc tài liệu khác chưa có trong thư mục nguồn.

### 2.1. `SRC-POL-AIA-ALP-001` — AIA Alpha CVTV (`AIAV/AD/2604-069`, 23 trang)

| Trang | Mục / Điều khoản | Phân loại | Rule ID / Tham chiếu | Căn cứ & Ghi chú kiểm toán |
|---|---|---|---|---|
| p.1 | Thư ngỏ định hướng chiến lược & chữ ký PTGĐ | `[REF_ONLY]` | — | **Căn cứ:** Thông điệp định hướng quản trị (chất lượng, văn hóa thăng tiến), không chứa công thức hay điều kiện trả tiền; dùng cho phân tích Chiến lược xác nhận. |
| p.2 | Hiệu lực 01/04/2026 & Sơ đồ lộ trình SA → SDM | `[FULL]` + `[CONFLICT]` | `AIA-CV-014` | **Mâu thuẫn nhẹ (`ERR-DOC-04`):** Sơ đồ p.2 ghi `UM = Trưởng Nhóm, DM = Trưởng Phòng`, khác với mục định nghĩa p.17 (`UM = Trưởng Phòng, DM = GĐ Ban`). |
| p.3 | Căn cứ NĐ 46/2023; Phân hạng Ngoại hạng Quý; Bảng Hệ số FY 2026 vs 2027 | `[FULL]` | `AIA-CV-001`, `002`, `003` | Đã tách rõ 2 bảng 2026 (phạt mềm) vs 2027 (vách đá `<70% → 0%`). |
| p.4–5 | Mục I.2 Thưởng 1/72H & Mục I.3 Chuyến HL đặc biệt 3M | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-CV-004`, `005`, `006` | Phụ thuộc `2506-074` (chỉ cho cohort gia nhập `<01/01/2026`) và danh sách chi tiết khóa `SB1–SB6`. |
| p.5–6 | Mục I.4 Thưởng DS Quý (8 bậc + quy đổi Q1 vs Q2+), I.5 Ngoại hạng Quý, I.6 Chất lượng SYC | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-CV-007..010` | Công thức rõ ràng 100%, nhưng đầu vào `FYC Tín Chỉ` & `SYC` phụ thuộc Memo cách tính doanh số & Phụ lục Hoa hồng. |
| p.7–8 | Mục I.7 Thưởng DS Năm, I.8 Gói BHSK, I.9 Phí Giới thiệu CVTV mới (5/10/20%) | `[FULL]` | `AIA-CV-011`, `012`, `013` | Đã tách cả tạm khấu trừ 10% TNCN, gộp M0→M1, chuyển đổi sang CQL (tham chiếu cũ `2512-192` nay là `2601-034`). |
| p.8–9 | Mục II Thăng tiến SA → UM & Mục III Duy trì HĐ | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-CV-014`, `015` | Phụ thuộc `AIAV/AD/2601-023` về danh sách khóa học bắt buộc. |
| p.10–11 | Mục IV Chuyển đổi/Duy trì/Khôi phục SE & Mục V Gia hạn 1–24 | `[FULL]` | `AIA-CV-016`, `017` | Trích xuất đủ 2 đợt xét, xóa nhóm khi UM+ → SE, giới hạn 12M. |
| p.11–13 | Mục VI Quy định tính doanh số, Thai sản, Bán cho NV AIA, 2 kỳ trả, Xét trả & Thu hồi 6M | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-CV-018..021` | Phụ thuộc `2401-029` (HĐ thay thế), `2501-016` (lịch trả V2), **`2501-017` (3 tiêu chí CL ĐLBH — ảnh hưởng cao)**. |
| p.13–14 | Mục VI.8 Kỷ luật hoạt động (70% / 0%) | `[FULL]` | `AIA-CV-022` | Áp dụng cho mọi thưởng/hỗ trợ/danh hiệu/Exchange. |
| p.14–17 | Mục VII Công thức AIA FY 14M, Quy định chuyển giao & 3 Ví dụ minh họa | `[FULL]` + `[CONFLICT]` | `AIA-CV-023` | **Mâu thuẫn (`ERR-DOC-02`):** p.14 ghi "làm tròn lên đến 0 số thập phân", khác với p.21 file CQL ("làm tròn gần nhất ≥0.5"). |
| p.17–20 | Mục VIII Định nghĩa, Thuật ngữ, Tháng chuẩn 1–15/16+, Thuế TNCN | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-CV-024` | Phụ thuộc Phụ lục Hoa hồng & Memo FYC Tín Chỉ. |
| p.21 | Phụ lục 2: Phí dịch vụ hoạt động JFW hàng tháng (CQL) | `[FULL]` | `AIA-CV-025` | Đã tách riêng thành rule cho CQL, hiệu lực 01/2026. |
| p.22–23 | Phụ lục 3: Đồng hành CVTV mới 3M đầu (T1–T6/2026) & Điều kiện ACK 15 ngày (**Ngoại lệ T01/2026: 28/02/2026**) / 21 ngày | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-CV-026` | **Đã bổ sung Post-Audit:** Ngoại lệ HĐ duyệt trong tháng 01/2026 có hạn nhận ACK hợp lệ đến hết `28/02/2026` (p.22). Phụ thuộc Quy định chấm công, `2501-017`, `2506-074`. |

### 2.2. `SRC-POL-AIA-ALP-002` — AIA Alpha CQL (`AIAV/AD/2601-034`, 21 trang)

| Trang | Mục / Điều khoản | Phân loại | Rule ID / Tham chiếu | Căn cứ & Ghi chú kiểm toán |
|---|---|---|---|---|
| p.1–2 | Thư ngỏ, Hiệu lực & Sơ đồ thăng tiến UM → SDM | `[REF_ONLY]` + `[CONFLICT]` | — | **Căn cứ `[REF_ONLY]`:** Nội dung giới thiệu chung. **Lỗi biên tập (`ERR-DOC-04`):** Thư ngỏ p.1 ghi nhầm "năm 2025". |
| p.3 | Mục A.I Phí TD hiệu quả tháng (Non-JFW) & A.II Phí TD chất lượng tháng (Activity + chấm công 50%) | `[FULL]` | `AIA-MG-001`, `002` | Đầy đủ bảng bậc thang FYC, active, FY & chấm công. |
| p.4–5 | Mục A.III Đào tạo gián tiếp (50/25/12.5%), A.IV UM thăng tiến (150%, cap 30tr), A.V Ngoại hạng Quý (3/4/5S), A.VI Kỹ năng Năm (trả chậm 15/25/60% 2028–2030, TOT ≥85%) | `[FULL]` | `AIA-MG-003..007` | Đã trích xuất đủ cả sự dịch chuyển Q1→Q2+ về số tuyển mới & quy đổi Exchange Pro = 2 mới. |
| p.6–7 | Mục B Đồng hành CVTV mới (10/20/40% trực tiếp; 5/10/20% qua SA) + 3 Ví dụ minh họa | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-MG-008`, `009` | Tham chiếu `2601-033` (nay đã thay bởi `2604-069`); cohort 2025 phụ thuộc `2501-110`. |
| p.8–9 | Mục C Thăng tiến UM→SDM, SDM→PAF & Luật 70% Concentration Cap + Ví dụ | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-MG-010`, `011`, `012` | Phụ thuộc khóa học `2601-023`. |
| p.10–11 | Mục D Duy trì chức danh CQL & Mục E Báo cáo đồng cấp (12/18/24M + miễn SDM) | `[FULL]` | `AIA-MG-013`, `014` | Đã tách rõ định kỳ Quý (UM/SUM) vs 6M (DM/SDM) và miễn cho AFF ≤2M. |
| p.12–16 | Mục F Sơ đồ cây 4 cấp, Thuật ngữ, Doanh số mới vs thuần, Xét trả & Thu hồi 6M, Nghỉ thai sản | `[FULL]` + `[CONFLICT]` + `[DEP_EXTERNAL]` | `AIA-MG-015` | **Lỗi dẫn chiếu (`ERR-DOC-03`):** p.15 ghi "Mục C" thay vì "Mục D". Phụ thuộc `2401-029` (HĐ thay thế), quy định chấm công & danh sách khóa học. |
| p.17–21 | Phụ lục 2: Công thức AIA FY & AIA TOT, 5 Ví dụ & Quy định làm tròn chuẩn (`≥0.5`) | `[FULL]` | `AIA-MG-016` | Là nguồn chuẩn để kiểm chứng ví dụ biên `74.49% vs 74.50%`. |

### 2.3. `SRC-POL-AIA-ALP-003` — AIA Alpha PAF+ (`AIAV/AD/2601-035`, 18 trang)

| Trang | Mục / Điều khoản | Phân loại | Rule ID / Tham chiếu | Căn cứ & Ghi chú kiểm toán |
|---|---|---|---|---|
| p.1–2 | Thư ngỏ & Tổng quan Con đường sự nghiệp kép (Dual Career) + 5 khoản loại trừ | `[FULL]` + `[CONFLICT]` | `AIA-PF-001` | **Lỗi biên tập:** p.1 ghi nhầm "năm 2025". Đã trích đủ quyền lợi kép & danh sách loại trừ + tạm giữ thu nhập khi thiếu khóa học. |
| p.3–5 | Danh sách 14 chức danh; A.1 Phí cố định (10 bậc 20–130tr), A.2 Đào tạo CN Tháng (50% chuỗi vô hạn), A.3 Quý, A.4 Thâm niên (cap 12M, clawback 100% 12M) | `[FULL]` | `AIA-PF-002..006` | Đã hiểu và trích xuất toàn bộ công thức + ví dụ 7 tầng (AF8 → President). |
| p.6–7 | Mục B Thăng tiến 10 bậc (AF → VP) + 70% cap + Vitality Vàng + CAO duyệt | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-PF-007` | Phụ thuộc quy định hạng Vàng Vitality & danh sách khóa học phòng Huấn luyện. |
| p.7–9 | Mục C Duy trì & Giáng cấp (AF+ vs PAF) & Mục D Báo cáo đồng cấp / vượt cấp (từ Q2/2026) | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-PF-008..010` | Q1/2026 phụ thuộc chuyển tiếp `AIAVAD 2511-169`. Lỗi đánh máy p.8: "quý 2/202". |
| p.9–13 | Mục E.1 Bảng phí cố định, E.2–E.3 Bảng chỉ tiêu 5 năm & 12 tháng lịch cho 10 chức danh + 2 ví dụ phân bổ tháng | `[FULL]` + `[NORMALIZED]` | `AIA-PF-011` | **Đã chuẩn hóa 100% Post-Audit:** Trích xuất trọn bộ 1,300 dòng (`100` dòng năm + `1,200` dòng tháng cho 10 chức danh × 5 năm × 2 chỉ tiêu FYP/1mAA, 0 sai lệch tổng) vào `knowledge/lookups/aia-paf-5y-targets.csv`. |
| p.13–14 | Mục E.4 Định nghĩa, Lịch trả 08–10, Làm tròn 0 chữ số, Ngừng trả khi có đơn thôi việc | `[FULL]` + `[DEP_EXTERNAL]` | `AIA-PF-012` | Phụ thuộc Memo `FYC Tín Chỉ` & quy định hoạt động/khóa học PAF+. |
| p.15–18 | Phụ lục 2: AIA FY & AIA TOT + 5 Ví dụ + Làm tròn | `[FULL]` | `AIA-MG-016` | Khớp 100% với Phụ lục 2 của `2601-034`. |

### 2.4. `SRC-POL-MNL-001` — Manulife PSM+ & HKD (`0048M01/2026/ASBD`, 6 trang)

| Trang | Mục / Điều khoản | Phân loại | Rule ID / Tham chiếu | Căn cứ & Ghi chú kiểm toán |
|---|---|---|---|---|
| p.1 | Phạm vi, Hiệu lực 01/01/2026; A.I Phí cơ bản (35/45tr × %FYP × 130%, sàn 30%, trần 150%); A.II Phí năng suất tháng | `[FULL]` + `[DEP_EXTERNAL]` | `MNL-PM-001`, `002` | Phụ thuộc bảng chỉ tiêu FYP giao cho từng PSM+/HKD (không có trong file). |
| p.2–3 | Bảng % năng suất (6%/8%), 2 giai đoạn Hệ số TLDTHD (trước & từ 04/2026), Phí gián tiếp 50%, A.III Phí hoạt động Quý (`1mAA_4mFYC`) | `[FULL]` + `[DEP_EXTERNAL]` | `MNL-PM-003..007` | Phụ thuộc bảng chỉ tiêu `1mAA_4mFYC` & công thức TLDTHD (`0016M03/2024`). |
| p.3–5 | A.IV Phí hợp tác dài hạn (ĐK1 ≥85% FYP vs ĐK2 Top 15 + tie-breaker; 75% TT + 25% GT; cap 12×; trả 30/30/40% Y1–Y3 tháng 4, K2 ≥70%, áp dụng cả 2024–2025) | `[FULL]` | `MNL-PM-008`, `009` | Đầy đủ, rõ ràng 100%, không mâu thuẫn. |
| p.5–6 | Mục C Quy định chung (C.1 Điều khoản mở từ 02/2026; C.5–C.8 Chuyển đổi PSM+↔HKD; C.9–C.10 Thuế/HĐ; C.11 Clawback sau chấm dứt) | `[FULL]` + `[UNCLEAR]` + `[DEP_EXTERNAL]` | `MNL-PM-010..012` | **`[UNCLEAR]` tại Mục C.1:** Chưa có thông báo chi tiết "Yêu cầu hoạt động dịch vụ từ tháng 02/2026". Phụ thuộc `0013M04/2024/ASBD`. |
| p.6 | Mục D Định nghĩa (FYP gồm 6% đóng 1 lần + 6% Top-up, FYC, `1mAA_4mFYC`, SA, hủy 21 ngày, TLDTHD) | `[FULL]` + `[DEP_EXTERNAL]` | `MNL-PM-013` | Phụ thuộc `01M02/2024/AO` (SA) & `0016M03/2024/ASBD` (TLDTHD). |

### 2.5. `SRC-POL-CHB-001` — Chubb Life Đại lý & Champion Hubb (`CHH0DCEB260007V`, 19 trang)

| Trang | Mục / Điều khoản | Phân loại | Rule ID / Tham chiếu | Căn cứ & Ghi chú kiểm toán |
|---|---|---|---|---|
| p.1–3 | Bìa, Mục lục, Mục I Quy định chung & Hiệu lực 01/01/2026 | `[REF_ONLY]` + `[DEP_EXTERNAL]` | — | **Căn cứ `[REF_ONLY]`:** Bìa/mục lục/mục đích hành chính. **Phụ thuộc:** `CHH0DCEB260005V` (định nghĩa chuẩn). |
| p.4–6 | Mục II.1 Hoa hồng, II.2 Thưởng HQKD Tháng (AR vs AL, chặn <13M, K2 25–120%, trả T vs T+1), II.3 Thưởng HQKD Quý (0/15/30% EHC) | `[FULL]` + `[DEP_EXTERNAL]` | `CHB-AG-005..008` | Phụ thuộc `260005V` về ngưỡng số tiền của `1 EHC` & công thức `K2`. |
| p.6–7 | Mục II.4 Thưởng HĐ Đại lý mới (M3/6/12, cap 6/10/20tr, phạt 50% thiếu khóa học) & II.5 Thưởng Duy trì CL HĐBH Quý (RYC Y2–Y5) | `[FULL]` | `CHB-AG-009`, `010` | Rõ ràng, trích xuất đầy đủ. |
| p.7–8 | Mục III Điều kiện thăng cấp (AR→BD) & Duy trì vị trí (AR dự bị 18M; AL khóa MAP) | `[FULL]` + `[DEP_EXTERNAL]` | `CHB-AG-011`, `012` | Phụ thuộc `260005V` (`3MAA`, `K2`, `P13`). |
| p.9–12 | Phụ đính I: Champion Hubb Cá nhân (KPI 4 trụ, M1–6, M7–12 trả ngay + M12 + **cơ chế bù trừ `NewAgentBonus` vào cục tháng trước rồi cục M12**, M13–24 RYC×W1×W2, SOP 9–11h, FNA 6M, chống gian lận) | `[FULL]` + `[CONFLICT]` | `CHB-CH-001..004` | **Mâu thuẫn (`ERR-DOC-01` — `CONFLICTING_EVIDENCE`):** Bảng p.9 ghi `SOP 80–<90% → W1=80%`, nhưng ví dụ p.10 (M11 & M12) ghi `SOP=85%` lại nhân `W1=50%`. Không tự phán xử — mở 2 toggle trong mô hình & leo thang Decision Register. Đã mô hình hóa chính xác công thức bù trừ M7–M12 ở ví dụ p.10. |
| p.13–19 | Phụ đính II: Full Biểu tỷ lệ Hoa hồng sản phẩm (từ 01/01/2025) & Bảng Hệ số bảo hiểm (HSBH) | `[FULL]` + `[NORMALIZED]` + `[DEP_EXTERNAL]` | `CHB-AG-001..004` | **Đã chuẩn hóa 100% Post-Audit:** Toàn bộ 113 dòng sản phẩm/phí trội/rider/nhóm đã nạp vào `knowledge/lookups/chubb-product-commission-schedule.csv` và 10 khung tuổi HSBH vào `knowledge/lookups/chubb-hsbh-tiers.csv`. Ghi nhận UL/ILP không đồng nhất 30% (KHTC Tương lai không QL tử vong người giám hộ = 27%, Cao niên = 20%, Hoạch định TC ≤20t = 25%, SP cũ còn Top-up 1.5–7%). HĐ `<01/01/2025` phụ thuộc `240048V`. |

### 2.6. `SRC-POL-CHB-002` — Chubb Life Quản lý AL & CH Quản lý (`CHH0DCEB260008V`, 14 trang)

| Trang | Mục / Điều khoản | Phân loại | Rule ID / Tham chiếu | Căn cứ & Ghi chú kiểm toán |
|---|---|---|---|---|
| p.1–3 | Bìa, Mục lục, Quy định chung, Hiệu lực 01/01/2026 & Bảng tóm tắt | `[REF_ONLY]` + `[DEP_EXTERNAL]` | — | **Căn cứ `[REF_ONLY]`:** Hành chính & bảng tóm tắt. Phụ thuộc `260005V` & `260006V`. |
| p.4 | Mục II.1 Phí Hỗ trợ tuyển dụng ĐDKD mới (10% M1–6 + 10% M7–12 khóa UM/AL) | `[FULL]` | `CHB-MG-001` | Đã ghi rõ phạm vi hoạt động hỗ trợ (tham khảo nghiệp vụ) và quy tắc khóa M12. |
| p.5–7 | Mục II.2 Phí HT KTN Tháng (≥15M vs <15M, EHC, K2, FYC âm tính phí âm) & Quý (30–50%) | `[FULL]` | `CHB-MG-002..004` | Trích xuất trọn vẹn cả ngoại lệ FYC âm & quy đổi không tròn quý. |
| p.7 | Mục II.3 Phí Quản lý nhóm Tháng (L1/L2/L3 khóa 0% khi FYC NTT <15tr, Team Null) | `[FULL]` | `CHB-MG-005` | Trích xuất đủ 3 bậc UM/SM/DM & Team Null. |
| p.8–10 | Mục II.4 Phí Đào tạo nâng cao CL QL (UM mới cap 15tr, SM mới cap 30tr, EHC NTT ≥2/3/4) & II.5 Duy trì CL HĐBH (RYC Y2–Y5) | `[FULL]` | `CHB-MG-006..008` | Đầy đủ 100%, rõ ràng. |
| p.11–14 | Phụ đính III: Champion Hubb Quản lý (chọn 1 vai trò, KPI nhóm ≥60%, mức 3–9tr / 1.5–4.5tr × W1, MAX vs `260009V` + Đào tạo QL, duy trì & SOP) | `[FULL]` + `[DEP_EXTERNAL]` | `CHB-MG-009`, `010` | Phụ thuộc `CHH0DCEB260009V` (Phí XD ĐVKD mới). Lỗi đánh máy p.12: `9.000.0000`. |

### 2.7. `SRC-POL-CHB-003` — Chubb Life Giám đốc Vùng RD (`CHH0DCEB260003V`, 15 trang scan)

| Trang | Mục / Điều khoản | Phân loại | Rule ID / Tham chiếu | Căn cứ & Ghi chú kiểm toán |
|---|---|---|---|---|
| p.1–4 | Bìa, Mục lục, Mục I (Mục đích, Cấp bậc AMD = BD/RD, Phạm vi, Hiệu lực 01/01/2026, 5 mối quan hệ báo cáo, Bảng 8 khoản phí) | `[FULL]` + `[DEP_EXTERNAL]` | `CHB-RD-001` | Đọc trực quan ảnh 150dpi rõ 100%. Phụ thuộc `260005V` & `260006V`. |
| p.5 | Mục II.1 Phí Đào tạo tiêu chuẩn Tháng (12.5/25tr theo FYP trọng số 100/50/25/12.5% × lớp ≥4 HV) | `[FULL]` | `CHB-RD-002` | Phạm vi mô tả đầu việc đào tạo là `[REF_ONLY]` cho nghiệm thu dịch vụ. |
| p.6–7 | Mục II.2 Quản lý HĐ (EHC), II.3 Quản lý KD (FYP), II.4 CL Hoạt động ĐLBH (3MAA × K2 Binary Cliff 50%→60% Q3+) | `[FULL]` | `CHB-RD-003..005` | Đầy đủ mọi bậc thang và mốc chuyển ngưỡng Q3/2026. |
| p.8–10 | Mục II.5 Quản lý & PTKD Quý (Tăng trưởng FYP QoQ/YoY 2.5–27.5% × K2 Cliff + ngoại lệ 360tr/0) & II.6 CL Phục vụ KH Quý (RYC 10–30%) | `[FULL]` | `CHB-RD-006`, `007` | Đã bóc đủ 12 bậc tăng trưởng & quy tắc đóng phí 1 lần 10%, loại trừ Top-up. |
| p.10–12 | Mục II.7 Đào tạo BD mới (25/50% 12M) & II.8 Quản lý BD/RD con (12.5/25%, đồng cấp 24M) | `[FULL]` + `[DEP_EXTERNAL]` | `CHB-RD-008`, `009` | **Phụ thuộc Chính sách 2026 của `BD`** để tính ra tổng 6 khoản phí quản lý của BD! |
| p.12–13 | Mục III Nghiệm thu dịch vụ; Mục IV Thăng cấp (9 tỷ FYP, 300 EHC, 2 DM, 4 BD/RD) & Duy trì (TT vs Toàn nhánh) | `[FULL]` | `CHB-RD-010` | Đầy đủ 100%. |
| p.13–15 | Mục V Quy định khác (ngày 15/16, BHSK, làm tròn 2 thập phân, giải ngân 25% holdback 2024–2025 tại T+15, 4 TH không trả, chuyển khoản 7 ngày, 9 TH tạm giữ & hoàn trả) | `[FULL]` | `CHB-RD-011`, `012` | Đầy đủ đến chữ ký PTGĐ Nguyễn Trọng Nghĩa trang 15/15. |
