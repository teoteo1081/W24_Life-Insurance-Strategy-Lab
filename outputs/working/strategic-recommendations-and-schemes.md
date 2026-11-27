# Strategic Recommendations, Illustrative Compensation Schemes & Financial Sensitivity (Step 1 Advisory Backbone)

**Ngày lập:** 2026-11-26  
**Phân loại Bằng chứng:** Toàn bộ đề xuất chính sách trong tài liệu này được gắn nhãn **`PROPOSAL` / `SYNTHETIC ASSUMPTION`** — là **kiến trúc minh họa định hướng tư vấn** (không phải chính sách chính thức đã ban hành). Mọi số liệu chi phí phân phối được đối soát trực tiếp từ `model/compensation/compensation_engine.py` và `outputs/working/W24_Compensation_Reference_Model_v1.xlsx`.  
**Truy vết Yêu cầu Gốc (`SRC-REQ-001` — Chị Nhi):** Trả lời trực tiếp vế 2 của yêu cầu: *"đề xuất chính sách phù hợp tại thị trường VN, nhằm thúc đẩy gia tăng doanh số, chất lượng kinh doanh và hiệu quả về mặt chi phí (ROI)"*.

---

## 1. Ma trận Quyết định Cơ chế Đối thủ (`ADOPT / ADAPT / AVOID / INVESTIGATE / UNKNOWN`)

| Cơ chế Thực tế của Đối thủ | Nguồn Bằng chứng | Quyết định | Lý do Nghiệp vụ & Tài chính |
|---|---|---|---|
| **1. Top-up = 0% HH & Phân tầng FYC theo Hệ số Bảo vệ (HSBH)** *(Chubb Life)* | `CHB-AG-001/002` | **`ADOPT`** | Giả định thiết kế ưu tiên bảo vệ thuần. Áp dụng pháp lý ở trạng thái `CONDITIONAL` cho đến khi đối chiếu điều khoản Top-up. |
| **2. Trả chậm sang T+1 cho ĐL mới / K2 thấp & Phí âm đối xứng khi hủy HĐ** *(Chubb Life)* | `CHB-AG-005`, `CHB-MG-002` | **`ADOPT`** | Lớp phòng thủ dòng tiền cực rẻ mà cực hiệu quả, chặn thất thoát tiền mặt trước khi hợp đồng hủy sớm trong 21 ngày / 60 ngày. |
| **3. Khóa Override Gián tiếp về 0% nếu Nhóm Trực tiếp `<15tr/tháng`** *(Chubb Life)* | `CHB-MG-005` | **`ADOPT`** | Triệt tiêu căn bệnh "quản lý ngồi hưởng hệ thống dưới mà không dẫn dắt đội trực tiếp". |
| **4. Trả chậm 3 năm (`30/30/40%`) gắn `K2 ≥70–75%` + Phí cơ bản có Sàn 30%/Trần 150% + Chuyển đổi `PSM+ ↔ HKD`** *(Manulife)* | `MNL-PM-001/008/010` | **`ADOPT`** | Best-in-class về dòng tiền Năm 1, giữ chân lãnh đạo dài hạn, kiểm soát định phí và minh bạch pháp lý/thuế theo NĐ 97/2026. |
| **5. Nghiệm thu dịch vụ bắt buộc & Điều kiện đào tạo (MAP / khóa học)** *(Chubb RD/AL & AIA)* | `CHB-RD-002/011`, `CHB-AG-012` | **`ADOPT`** | Đảm bảo hợp lệ chi phí quản lý/đào tạo theo NĐ 97/2026/NĐ-CP và nâng chuẩn tư vấn thực chất. |
| **6. Thưởng SYC/RYC cao ở cả 3 tầng (`+25%–50%`)** *(AIA 50% SYC & Chubb RD 30% RYC)* | `AIA-CV-009`, `CHB-RD-007` | **`ADOPT`** | Động lực kinh tế mạnh nhất để đại lý & quản lý thực sự chăm sóc thu phí tái tục năm 2–5 (kiểm tra theo ngưỡng tham chiếu và phí thực thu cấp danh mục). |
| **7. Champion Hubb kỷ luật hành vi (`SOP + FNA`) + Bù trừ `MAX()` + Giữ lại M12** *(Chubb Life)* | `CHB-CH-002` | **`ADAPT`** | Rất tốt cho nhánh toàn thời gian, nhưng phải **sửa mâu thuẫn `ERR-DOC-01`** và kiểm soát chi phí vận hành kiểm tra FNA. |
| **8. Cổng Persistency Cứng (`<70%→0%` AIA 2027 vs `<50%→25%` Chubb)** | `AIA-CV-003`, `CHB-AG-005` | **`ADAPT`** | Tránh cả hai thái cực: không mềm đáy 25% như Chubb và không sốc đột ngột 70% như AIA → **đặt sàn cứng tại `K2 < 60% → 0%`** (lộ trình lên 65% năm sau) với đường cong mượt từ 60%–85%. |
| **9. Luật 70% Concentration Cap & Tuyển dụng khóa M12 lên UM** *(AIA CQL & Chubb AL)* | `AIA-MG-012`, `CHB-MG-001` | **`ADAPT`** | Áp thống nhất 70% cap cho mọi bậc quản lý (nêu rõ không nhầm CQL vs PAF+) và khóa 50% thưởng tuyển dụng vào mốc giữ chân M12. |
| **10. Direct Override AL chạm `108% FYC` & Cá nhân AL chạm `109.2% FYC`** *(Chubb Life)* | `CHB-AG-008`, `CHB-MG-003` | **`AVOID`** | Đẩy tổng chi phí phân phối toàn cây lên `89%–100%+ FYP`, làm tăng chi phí mô phỏng. Đánh giá Điều 52 cần đối chiếu các khoản thưởng thuộc phạm vi và phí thực thu cấp danh mục. |
| **11. Phí cố định quá cao (`20–130tr/M`) + Dual Career + Chuỗi gián tiếp 50% vô hạn tầng** *(AIA PAF+)* | `AIA-PF-001..004` | **`AVOID`** | Tạo phình định phí và hiệu ứng tầng cộng dồn không chặn trần (`Σ 0.5^k → +100%`), cực rủi ro khi thị trường tăng trưởng chậm. |
| **12. Thưởng Tăng trưởng thuần QoQ tới `27.5% FYC`** *(Chubb RD)* | `CHB-RD-006` | **`AVOID`** | Dễ kích thích hành vi "nén số/dồn số" (sandbagging) giữa các quý; thay bằng thưởng tăng trưởng trên nền **lũy kế năm (YTD) & vượt mục tiêu năm**. |
| **13. Tính `6% Top-up` vào chỉ tiêu FYP** *(Manulife PSM+)* | `MNL-PM-013` | **`AVOID`** | Đề xuất loại Top-up khỏi chỉ tiêu FYP. Đối chiếu riêng quy định hoa hồng Top-up và mốc áp dụng. |
| **14. Chính sách Trợ cấp `Exchange / Exchange Pro / AFF`** *(AIA)* | `SRC-GAP-001` | **`INVESTIGATE`** | Có ảnh hưởng rất lớn đến chi phí tuyển đại lý toàn thời gian — cần thu thập tài liệu gốc trước khi định giá cạnh tranh tuyển dụng. |
| **15. Chính sách Đại lý FA & UM/DM của Manulife + `BD` & `260005V` của Chubb** | `SRC-GAP-002/003` | **`UNKNOWN`** | Chưa đủ bằng chứng; giữ mở cấu trúc module để cập nhật ngay khi TJ thu thập thêm tài liệu. |

---

## 2. Kiến trúc Chính sách Đề xuất (`PROPOSAL`: 1 Phương án Chính + 2 Biến thể Chiến lược)

### 2.1. Phương án Khuyến nghị Chính — `W24 Balanced Hybrid ("Tăng trưởng Có Chất lượng & Tự Ổn định Chi phí")`
*(Mọi tham số đều cho phép PO điều chỉnh trực tiếp trên Sheet `04_Policy_Parameters` của Excel Reference Model — gắn cờ `po_editable = TRUE`)*

| Tầng Đối tượng | Cấu trúc Thu nhập Đề xuất (`PROPOSAL / SYNTHETIC ASSUMPTION`) | Mục tiêu Hành vi & Cơ chế Kiểm soát Chi phí / Pháp lý |
|---|---|---|
| **Tầng 1 — Đại lý Cá nhân** *(Tham chiếu Điều 51 và Điều 52 — `CONDITIONAL`)* | • **Hoa hồng (Điều 51):** UL/ILP PCB Y1 **30%** (phân tầng **25%–30%** theo HSBH bảo vệ), Y2 **20%**, Y3+ **10%**; **Top-up = 0%**; Tử kỳ/Riders bảo vệ trả sát trần hợp lý.<br>• **Kích hoạt ĐL mới (M1–M6):** `1.5tr/tháng` tiền mặt + `1.5tr/tháng` **giữ lại trả tại M12** khi đạt `≥8tr FYC/M`, qua 21 ngày, ACK ≤15 ngày & đủ khóa học (tối đa `18tr/Y1`).<br>• **Thưởng Năng suất Tháng (5 bậc mượt):** `5/12/22/35/≥55tr FYC` → **`8% / 16% / 24% / 32% / 38%`** × **`Hệ số K2`** (`<60%: 0%`, `60–70%: 60%`, `70–75%: 85%`, `75–80%: 100%`, `80–85%: 110%`, `≥85%: 120%`).<br>• **Thưởng Đều đặn Quý:** `+12%` trên tổng thưởng tháng khi đạt **3/3 tháng hoạt động (`≥4tr FYC/M`)**.<br>• **Thưởng Siêu sao Năm (MDRT):** `+10% FYC` (từ `≥400tr FYC/năm`, **giữ lại 30% sang năm 2** nếu `K2 ≥75%`).<br>• **Thưởng Tái tục (RYC/SYC):** **`+25%` trên SYC năm 2** khi `K2 ≥75%` (kiểm tra theo ngưỡng tham chiếu và phí thực thu cấp danh mục).<br>• **Dòng tiền & Clawback:** ĐL mới / `K2 <65%` nhận thưởng tại **T+1**; clawback **6 tháng** kể cả sau nghỉ việc. | • Đỉnh thưởng cá nhân ở K2=85% ≈ `51%–63% FYC` (~`15%–19% FYP`), dưới ngưỡng 30% trong phép so sánh đơn lẻ. Kết luận tuân thủ cần dữ liệu thưởng và phí thực thu cấp danh mục.<br>• Mốc khởi điểm `5tr FYC/M` phù hợp xu hướng **Case Size thu hẹp 2026**.<br>• Giữ động lực MDRT nhưng không tạo hố chi phí `85%–109%` như Chubb. |
| **Tầng 2 — Quản lý Trực tiếp & Cấp trung** *(HĐDV NĐ 97/2026)* | • **Direct Override Tháng + Quý (đỉnh `36% FYC NTT` × `K2`, không gồm bán cá nhân ở mức đỉnh vượt kiểm soát):** 4 bậc mượt + thưởng hoạt động nhóm + **phí âm đối xứng khi hủy HĐ**.<br>• **Indirect Override (Giới hạn 3 tầng: `35% / 17.5% / 8.75%`):** **Khóa về `0%` nếu `FYC NTT < 15tr/tháng`** (học Chubb Life) + **Luật 70% Concentration Cap** thống nhất.<br>• **Tuyển dụng & Nhân bản Quản lý:** `10% FYC` người mới (50% trả tháng M1–6, **50% trả tại M12 khi giữ hoạt động**) + `+100%` phí quản lý UM mới trong 12M (cap `15tr/M`, đòi `K2 ≥75%`).<br>• **Thưởng Giữ chân 3 Năm (Deferred):** **`12% FYC NTT năm`**, trả rải **`30% (Y+1) – 30% (Y+2) – 40% (Y+3)`** với điều kiện còn hợp đồng & **`K2 ≥75%`**.<br>• **Thưởng RYC Nhóm:** `+15% RYC NTT` khi `K2 ≥70%`. | • Cắt giảm **>50% chi phí nóng** so với đỉnh `108%` của Chubb AL, dồn sang **trả chậm 3 năm giữ chân**.<br>• Đảm bảo quản lý vừa trực tiếp bán/dẫn đội (`≥15tr NTT`) vừa nhân bản quản lý mới bền vững. |
| **Tầng 3 — Lãnh đạo Vùng / Đối tác HKD** *(HĐDV Nghiệm thu NĐ 97/2026)* | • **Phí Cơ bản KPI Nghiệm thu:** **`35tr / 45tr/tháng` × `%FYP` × `125%`** (Sàn **≥30%**, Trần **140%** = `49tr / 63tr/M`) + yêu cầu nghiệm thu `≥3 lớp đào tạo/tháng` (`≥4 HV/lớp`).<br>• **Override Vùng Biến đổi:** `7% FYC` trực tiếp × `K2` + `40%` gián tiếp (tối đa 2 tầng, **không chuỗi vô hạn**).<br>• **Phí Hợp tác Dài hạn 3 Năm:** `60%` tổng Override Vùng biến đổi (cap `12× cơ bản`), trả rải **`30/30/40%` gắn `K2 ≥75%`** + hỗ trợ chuyển đổi linh hoạt **`Cá nhân ↔ HKD`**.<br>• **Thưởng RYC Vùng:** `15%–30% RYC` theo `K2`. | • Kiểm soát chặt định phí, tối ưu dòng tiền Năm 1 (~20%–25% chi phí vùng trả chậm 3 năm).<br>• Không bị thao túng nén số QoQ như Chubb RD và không bị phình định phí 130tr + chuỗi vô hạn như AIA PAF+. |

### 2.2. Hai Biến thể Tùy chọn Theo Giai đoạn Chiến lược Doanh nghiệp
1. **Biến thể A — `Growth-Tilted Variant` (Dành cho DN cần mở rộng thị phần / tuyển thủ lĩnh nhanh):** Nâng gói kích hoạt toàn thời gian (kiểu Champion Hubb 12M gắn SOP + 20 FNA/M + giữ lại 40% đến M12), nâng mức thưởng nhân bản UM lên `125%` (cap 20tr/M), nhưng **giữ ngưỡng nội bộ đề xuất ≤ 26% FYP và sàn K2 60%**. Phù hợp khi ưu tiên tốc độ tăng Manpower trên MAPA.
2. **Biến thể B — `Quality & Cash-First Variant` (Dành cho DN tái cấu trúc / tối ưu VNB & vốn):** Nâng ngưỡng sàn cứng K2 lên `65%` ngay từ năm 1, tăng tỷ trọng trả chậm 3 năm lên `35%` tổng thu nhập quản lý, tăng thưởng SYC/RYC đại lý lên `35%`, hạ định phí vùng xuống `25–35tr/M`. Phù hợp khi biên vốn hẹp và K2 lịch sử đang yếu (`<70%`).

---

## 3. Phân tích Độ nhạy Tài chính & Điều kiện Hòa vốn (`Break-Even VNB Margin` — Không bịa Biên Lợi nhuận!)

> **Kỷ luật Tài chính (Section 25 & 30):** Do chưa có số liệu `VNB Margin` và chi phí vận hành trụ sở (`Home Office OpEx`) thực tế của doanh nghiệp mục tiêu (`UNKNOWN`), bảng dưới trình bày **Tổng Chi phí Phân phối Toàn Cây** (1 Vùng chuẩn = `12 tỷ FYP/năm`, tính doanh thu đúng 1 lần) và **Biên Gộp Sản phẩm Tối thiểu Cần đạt (`Break-Even Gross Margin`)** dưới giả định `Home Office OpEx = 20% FYP` (`ASSUMPTION`, có sensitivity 15%/20%/25% trên Excel Sheet `13_MAPA_&_Financial`).

| Chính sách / Kịch bản *(1 Vùng = 12 tỷ FYP/Y, 20 ĐL × 15tr FYC/M, 4 QL, 1 Vùng)* | Persistency (`K2 / FY`) | Tổng Chi phí Ghi nhận (`% FYP`) | Chi tiền mặt Năm 1 (`% FYP`) | Quỹ Thưởng ĐL (`Trần Đ.52 ≤30%`) | Chi phí / 1đ Phí còn sống Năm 2 (`%`) | **Break-Even Gross Margin** *(với OpEx 20%)* |
|---|---:|---:|---:|---:|---:|---:|
| **Chubb Life Agency 2026** | **82%** | **99.96%** | 99.96% | 21.06% *(riêng ĐL top chạm 26–33%!)* | 121.90% | **119.96%** *(cần lãi tái tục Y2+ bù!)* |
| **AIA Alpha 2026** *(chưa gồm `Exchange/Pro`!)* | **82%** | **73.44%** | 70.44% | 10.23% | 89.57% | **93.44%** |
| **AIA Alpha 2027** *(chưa gồm `Exchange/Pro`!)* | **82%** | **72.98%** | 69.98% | 9.77% | 89.00% | **92.98%** |
| **W24 Proposed Balanced (`PROPOSAL`)** | **82%** | **59.44%** | **54.45%** | **5.91% (dưới ngưỡng mô phỏng)** | **72.48%** | **79.44%** *(rẻ hơn Chubb **-39.8 điểm %**!)* |
| --- | --- | --- | --- | --- | --- | --- |
| **Chubb Life Agency 2026** | **72%** | **90.15%** | 90.15% | 17.55% | 125.21% | **110.15%** |
| **AIA Alpha 2026** | **72%** | **62.25%** | 62.25% | 8.37% | 86.46% | **82.25%** |
| **AIA Alpha 2027** | **72%** | **61.79%** | 61.79% | 7.90% | 85.82% | **81.79%** |
| **W24 Proposed Balanced (`PROPOSAL`)** | **72%** | **49.94%** | **49.94%** | **4.57% (dưới ngưỡng mô phỏng)** | **69.36%** | **69.94%** |
| --- | --- | --- | --- | --- | --- | --- |
| **Chubb Life Agency 2026** | **62%** | **77.89%** | 77.89% | 13.16% | **125.63%** *(tăng chi phí/phí sống!)* | **97.89%** |
| **AIA Alpha 2026** | **62%** | **55.89%** | 55.89% | 3.91% | 90.14% | **75.89%** |
| **AIA Alpha 2027 (Vách đá `<70%→0%`)** | **62%** | **51.98%** | 51.98% | **0.00%** | 83.84% | **71.98%** |
| **W24 Proposed Balanced (`PROPOSAL`)** | **62%** | **45.42%** | **45.42%** | **3.23% (dưới ngưỡng mô phỏng)** | **73.27%** | **65.42%** *(tự ổn định tốt nhất!)* |

*(Tất cả các con số trên khớp 100.00% đến 2 chữ số thập phân với đầu ra thực tế của Python Engine `model/compensation/compensation_engine.py` và sẽ được đối soát trực tiếp với Microsoft Excel COM trên Sheet `11_Hierarchy_Dist_Cost`!)*

### Kết luận Tài chính Mô phỏng & Ranh giới ROI (`Modeled Break-Even ≠ Actual ROI`)
1. **Tuyệt đối tách bạch Chi phí/Điểm hòa vốn Mô phỏng với ROI Thực tế (`UNKNOWN`):** Các con số trên đo **Modeled Distribution Cost (% FYP)**, **Modeled Cost per Persisted Year-2 FYP**, và **Modeled Break-Even Gross Margin** trên 1 kịch bản vùng chuẩn `12 tỷ FYP` với giả định `Home Office OpEx = 20%` (`ASSUMPTION`). Tài liệu này **KHÔNG chứng minh ROI thực tế** hay mức tăng doanh số/chất lượng thực tế cho đến khi nạp `VNB Margin`, `OpEx` thực và dữ liệu cohort của doanh nghiệp mục tiêu.
2. **Tính tự ổn định chi phí theo chất lượng (`Downside Cost Resilience`):** Khi K2 tụt từ `82%` xuống `62%`, `Cost / Persisted Y2 FYP` mô phỏng ở Chubb tăng lên `125.63%`, còn ở **W24 Proposed Balanced** giữ ổn định quanh `69.36% – 73.27%`.
3. **Hiệu quả Dòng tiền Năm 1 mô phỏng & Điều kiện Pháp lý (`CONDITIONAL`):** Nhờ trả chậm 3 năm (`30/30/40%` gắn `K2 ≥75%`), chi tiền mặt Năm 1 mô phỏng giảm còn `54.45% FYP` (thấp hơn `15.99` điểm % so với kịch bản AIA và `45.51` điểm % so với kịch bản Chubb). Cột `Art.52` chỉ kiểm tra tỷ lệ **rổ thưởng đại lý mô phỏng / FYP kịch bản**; cần Pháp chế & Kế toán xác nhận phân loại chi phí pháp định theo toàn văn **`44/2026/VBHN-TT-BTC`** (`DEC-03`).
