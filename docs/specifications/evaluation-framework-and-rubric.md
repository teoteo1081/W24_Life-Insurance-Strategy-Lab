# Evaluation Framework & Scoring Rubric — Khung Đánh giá & Chấm điểm Chính sách Thu nhập

**Ngày lập:** 2026-11-26  
**Trạng thái Calibration:** **`DRAFT — NOT INDEPENDENTLY CALIBRATED`** *(xây dựng nội bộ bởi AGY, cần Business Owner TJ và/hoặc Independent Auditor rà soát, phê duyệt trọng số và chấm mù đối chiếu trước khi chốt điểm chính thức)*.  
**Truy vết Yêu cầu Gốc (`SRC-REQ-001` — Chị Nhi):** Đánh giá khách quan các chính sách đối thủ và đề xuất mới trên 3 trục cốt lõi: **Gia tăng Doanh số**, **Chất lượng Kinh doanh**, và **Hiệu quả Chi phí (ROI)**, kèm trục Con người và Khả năng Triển khai.

---

## 1. Kiến trúc 2 Tầng: Cổng Pháp lý Bắt buộc (Mandatory Gate) + 15 Tiêu chí Chấm điểm

> **Nguyên tắc Rubric Engineering:** Tuân thủ pháp luật (Regulatory Compliance) **KHÔNG được tính điểm bù trừ (compensatory weight)**! Một chính sách dù thúc đẩy doanh số đạt 5/5 nhưng vi phạm trần Điều 51 (hoa hồng), Điều 52 (thưởng đại lý ≤ 30% FYP Y1 / ≤ 7% RYP) hoặc TT 96/2026 (Top-up) phải bị gắn cờ **`FAIL_GATE — KHÔNG ĐƯỢC BAN HÀNH`** cho đến khi sửa đạt chuẩn.

### Tầng 0 — Mandatory Regulatory & Compliance Gate (`PASS / CONDITIONAL / FAIL`)
| Cổng kiểm tra | Yêu cầu bắt buộc | Trạng thái hiện tại trên đối thủ & đề xuất |
|---|---|---|
| **G1. Trần Hoa hồng (Điều 51 TT 67/2023 & TT 96/2026 / `44/2026/VBHN-TT-BTC`)** | UL/ILP PCB Y1 ≤ 30%, Y2 ≤ 20%; Tử kỳ/Trọn đời Y1 ≤ 40%; Nhóm ≤ 50% cá nhân; Hưu trí ≤ 3%; Top-up ≤ phí ban đầu. | Chubb SP mới: `CONDITIONAL` *(Top-up 0% nhưng điều khoản luật `SOURCE_NOT_VERIFIED`)*; AIA/Manulife: `CONDITIONAL` *(thiếu biểu HH; Manulife còn 6% Top-up vào FYP)*; Proposal W24: **`CONDITIONAL`** *(thiết kế nhắm tuân thủ, chờ đối chiếu toàn văn `44/2026/VBHN-TT-BTC` — `DEC-03`)*. |
| **G2. Trần Thưởng & Hỗ trợ Đại lý (Điều 52 TT 67/2023)** | Tổng thưởng/hỗ trợ ĐL khai thác mới ≤ 20% phí ≤1Y + ≤ 30% FYP (>1Y); tái tục ≤ 7% RYP ở cấp toàn danh mục DN. | Chubb: **`CONDITIONAL / HIGH RISK`** (đỉnh cá nhân 25.7%–32.8% FYP); AIA: `CONDITIONAL` (thiếu số tiền Exchange/Pro); Proposal W24: **`CONDITIONAL`** *(rổ thưởng mô phỏng `5.91%–19% FYP` < 30%, nhưng phân loại kế toán & mẫu số pháp định cần Pháp chế/Tài chính xác nhận trên toàn văn `44/2026/VBHN-TT-BTC`)*. |
| **G3. Phân tách Phí Quản lý/Đào tạo (NĐ 97/2026/NĐ-CP)** | Mọi khoản phí quản lý/đào tạo/tuyển dụng phải gắn dịch vụ thực tế, có hợp đồng & biên bản nghiệm thu, không ngụy trang thưởng bán cá nhân. | Chubb RD, Manulife PSM+/HKD & Proposal W24: **`CONDITIONAL`** *(có cấu trúc nghiệm thu dịch vụ; chờ đối chiếu toàn văn NĐ 97/2026 ngày 31/03/2026)*. |

---

## 2. 15 Tiêu chí Đánh giá & Bộ Trọng số Tham chiếu (PO Reference Weights)

| Trụ cột (Pillar) | Trọng số PO Tham chiếu | Mã Tiêu chí | Tên Tiêu chí Đánh giá | Trọng số Con |
|---|---:|---|---|---:|
| **I. Gia tăng Doanh số (Growth & Production)** | **30%** | `C01` | Kích hoạt Đại lý Mới & Tốc độ tạo doanh số đầu tiên (`Activation`) | 8% |
| | | `C02` | Động lực Tăng Năng suất & Tần suất Đều đặn (`Productivity & Active Ratio`) | 9% |
| | | `C03` | Mở rộng Quy mô Đội ngũ & Nhân bản Quản lý (`Recruitment & Manager Build`) | 7% |
| | | `C04` | Định hướng Sản phẩm Giá trị cao & Bảo vệ Thực chất (`Product Mix / Case Size`) | 6% |
| **II. Chất lượng Kinh doanh (Business Quality)** | **25%** | `C05` | Kỷ luật Tỷ lệ Duy trì Hợp đồng (`Persistency K2 / FY / TOT Gates`) | 10% |
| | | `C06` | Động lực Chăm sóc Tái tục Năm 2+ (`SYC / RYC Servicing Incentives`) | 7% |
| | | `C07` | Chống Trục lợi, Chống Hủy sớm & Kiểm soát Hành vi (`Clawback / Anti-Gaming / SOP`) | 8% |
| **III. Hiệu quả Chi phí & ROI (Financial & Cost)** | **25%** | `C08` | Kiểm soát Tổng Chi phí Phân phối Toàn Hệ thống (`Enterprise Cost / FYP`) | 8% |
| | | `C09` | Kiểm soát Rủi ro Định phí & Biến thiên Chi phí theo Chu kỳ (`Fixed Burn & Cap`) | 6% |
| | | `C10` | Hiệu quả Dòng tiền Năm 1 & Cơ chế Trả chậm (`Cash Flow & Deferral`) | 6% |
| | | `C11` | Khả năng Chịu đựng Độ nhạy & Điểm Hòa vốn VNB (`Break-Even & Downside Resilience`) | 5% |
| **IV. Con người & Giữ chân (People & Retention)** | **10%** | `C12` | Lộ trình Thăng tiến Rõ ràng & Công bằng giữa các Tầng (`Career Path & Fairness`) | 5% |
| | | `C13` | Khóa Giữ chân Đại lý Giỏi & Lãnh đạo Cốt cán (`Long-Term Retention Lock-in`) | 5% |
| **V. Khả năng Triển khai (Implementation)** | **10%** | `C14` | Độ Đơn giản, Dễ Truyền thông & Minh bạch cho Đội ngũ (`Simplicity & Explainability`) | 5% |
| | | `C15` | Khả năng Vận hành Hệ thống, Kiểm toán & Tính Rõ ràng Văn bản (`Operability & Auditability`) | 5% |
| **TỔNG CỘNG** | **100%** | **15 Tiêu chí** | *(Độc lập với Cổng Pháp lý Bắt buộc G1–G3)* | **100%** |

---

## 3. Thang Chấm điểm Cụ thể Theo Từng Tiêu chí (Criterion-Specific 1–5 Anchors)

> **Quy tắc chống chấm cảm tính & chống gán 0 khi thiếu dữ liệu:** Nếu một chính sách thiếu bằng chứng cho tiêu chí nào (ví dụ Manulife thiếu toàn bộ Tầng 1–2 cho `C01`, `C02`, `C04`), tuyệt đối **KHÔNG chấm 1/5 hay 0/5**, mà ghi rõ **`N/A (INSUFFICIENT_EVIDENCE)`** và loại tiêu chí đó khỏi mẫu số hoặc báo cáo điểm kèm **`Coverage %`** (tỷ lệ trọng số có đủ bằng chứng).

| Mã | Mức 1 (Yếu / Rủi ro cao) | Mức 2 (Dưới chuẩn) | Mức 3 (Đạt chuẩn thị trường) | Mức 4 (Tốt / Cân bằng) | Mức 5 (Xuất sắc / Best-in-Class) |
|---|---|---|---|---|---|
| **`C01`** | Không có kích hoạt M1–M3 hoặc trả cứng không điều kiện HĐ. | Có thưởng ĐL mới nhưng mốc quá cao (>15tr FYC/M) hoặc không gắn freelook. | Có gói M1–M3 rõ ràng gắn HĐ thực cấp & qua 21 ngày. | Kết hợp thưởng kích hoạt nhanh (tuần/tháng) + mốc M3–M6–M12 + kiểm soát đào tạo/ACK. | Gói kích hoạt phân tầng (phổ thông vs toàn thời gian), có bù trừ `MAX()`, giữ lại một phần đến M12 và chuyển mượt sang năm 2. |
| **`C02`** | Tỷ lệ thưởng phẳng, không phân biệt người bán đều vs bán dồn. | Bậc thang quá ít hoặc quá dốc gây bỏ cuộc giữa chừng. | Có bậc thang tháng/quý gắn tối thiểu `1mAA/EHC`. | Bậc thang mượt khuyến khích bán đều hàng tháng (EHC/active) + thưởng vượt chuẩn cho top MDRT. | Tối ưu đồng thời 3 phân khúc (lõi đại trà, năng suất khá, siêu sao MDRT/TOT) không tạo bẫy dồn số giữa các quý. |
| **`C03`** | Không có thưởng tuyển dụng/nhân bản quản lý hoặc trả không gắn hoạt động. | Trả thưởng theo đầu người (headcount) dễ tuyển ảo. | Trả override theo FYC người mới trong 6–12 tháng. | Thưởng tuyển gắn doanh số thực của người mới + khóa điều kiện lên cấp/duy trì + chặn "ăn bám" hệ thống dưới. | Kết hợp thưởng đồng hành theo chất lượng ứng viên + thưởng nhân bản quản lý có cap hợp lý + luật chống phụ thuộc 1 nhánh (`≤70%`) + điều kiện NTT tối thiểu. |
| **`C04`** | Vẫn trả hoa hồng/FYP cao cho Top-up hoặc sản phẩm tiết kiệm thuần biên thấp. | Hoa hồng phẳng mọi sản phẩm, không phân biệt mức độ bảo vệ. | Cắt Top-up khỏi FYP thưởng; tách rider riêng. | Cắt Top-up = 0% cả HH lẫn FYP + thưởng thêm cho sản phẩm bảo vệ/rider sức khỏe. | Tích hợp trực tiếp **Hệ số Bảo vệ (HSBH)** vào biểu hoa hồng & cơ sở thưởng (kiểu *Tự Do An Phúc* Chubb) + không thưởng Top-up, khớp 100% TT 96/2026. |
| **`C05`** | Không có hệ số K2/FY hoặc đáy mềm <50% vẫn hưởng ≥50% thưởng. | Có hệ số K2 nhưng đáy mềm (`<50%` vẫn nhận 25%) khiến chất lượng thấp vẫn sinh lời. | Có hệ số K2 bậc thang cắt mạnh dưới 60% và thưởng trên 80%. | Ngưỡng cứng hợp lý (`<60%` về 0% hoặc `K2/2` có lộ trình), tránh sốc vách đá nhưng chặn triệt để doanh số rác. | Hệ số Persistency mượt kết hợp ngưỡng sàn cứng bảo vệ DN (`<60%→0%` có lộ trình), áp xuyên suốt từ Đại lý đến Lãnh đạo Vùng & cả khoản trả chậm. |
| **`C06`** | Không có thưởng tái tục (`SYC/RYC`). | Thưởng RYC thấp (<5%) hoặc điều kiện quá dễ. | Có thưởng RYC 10%–15% khi đạt K2 ≥ 65%. | Thưởng SYC/RYC hấp dẫn (15%–30%+) gắn điều kiện hoạt động đều & K2 cao (≥70%–75%). | Hệ thống thưởng tái tục đồng bộ cả 3 tầng (Đại lý 20–50% SYC/RYC, Quản lý 15%, Vùng 25–30%) + năm 2 chuyển hẳn trọng tâm sang RYC. |
| **`C07`** | Trả ngay 100% trong tháng T, không clawback hoặc dễ trục lợi FNA/nén số. | Có clawback nhưng chỉ trừ trong lúc còn làm, nghỉ việc là mất dấu. | Có clawback 6M và trừ hủy 21 ngày. | Kết hợp **trả chậm T+1 cho K2 <60%/mới**, clawback cả sau khi nghỉ việc, và kiểm soát hành vi đầu vào (SOP/FNA/ACK). | Phòng thủ 4 lớp: (1) T+1 hold cho K2 thấp/mới, (2) phí âm đối xứng khi hủy, (3) clawback kể cả hậu nghỉ việc, (4) chống nén số QoQ & chống gian lận FNA. |
| **`C08`** | Tổng chi phí toàn cây vượt >95% FYP năm 1 hoặc chạm/vượt trần Điều 52. | Tổng chi phí 85%–95% FYP năm 1, biên an toàn rất mỏng. | Tổng chi phí 75%–85% FYP năm 1, nằm trong biên kiểm soát. | Tổng chi phí toàn cây 65%–75% FYP năm 1; quỹ thưởng đại lý ≤ 24% FYP (cách xa trần 30% Điều 52). | Tổng chi phí toàn cây tối ưu ≤ 65%–70% FYP ở kịch bản chuẩn, có trần rõ ở mọi lớp override gián tiếp (không chuỗi vô hạn tầng). |
| **`C09`** | Định phí cao không gắn sàn KPI hoặc trả cố định kể cả khi doanh số rất thấp. | Định phí cao có sàn thấp (35%–55% đã hưởng 100%) kèm Dual Career chồng lớp. | Định phí vừa phải có sàn và trần rõ ràng. | Định phí bị khóa chặt bằng **sàn ≥30%–40%, trần ≤120%–150%** hoặc gắn nghiệm thu đầu việc cụ thể. | Định phí thấp nhất có thể, tự động co giãn tuyến tính theo KPI thực đạt + nghiệm thu đầu việc đào tạo/hoạt động và có trần tổng danh mục. |
| **`C10`** | Chi 100% tiền mặt ngay trong Năm 1, không có deferral/holdback. | Chỉ giữ lại cục nhỏ (<5% tổng thu nhập) đến M12. | Có giữ lại 10%–15% thưởng năm hoặc M12. | Dịch chuyển 15%–20% tổng thu nhập quản lý/top agent sang trả chậm 2–3 năm gắn K2. | Cấu trúc trả chậm 2–3 năm (kiểu `30/30/40%` Manulife / `15/25/60%` AIA CQL) giúp giảm 8–12 điểm % Cash Outflow Năm 1 và tự động hủy trả nếu K2 tụt. |
| **`C11`** | Khi K2 giảm xuống 60%, chi phí/phí còn sống tăng vọt >+25%, nhanh chóng lỗ nặng. | Chi phí giảm chậm hơn mức sụt giảm chất lượng. | Chi phí giảm tương ứng với K2 ở mức trung bình. | Khi K2 giảm xuống 60–65%, thưởng tự động co mạnh giúp ổn định điểm hòa vốn VNB. | Cơ chế tự ổn định (automatic stabilizer): chi phí phân phối co giãn nhanh theo cả sản lượng lẫn K2, giữ Break-Even VNB Margin thấp ổn định qua mọi kịch bản xấu. |
| **`C12`** | Lộ trình rối rắm, nhiều lỗi bất nhất tên gọi hoặc thiếu minh bạch thăng/giáng cấp. | Có lộ trình nhưng quá nhiều bậc phụ (>12 bậc) hoặc điều kiện giáng cấp quá khắc nghiệt/mơ hồ. | Lộ trình 3 tầng rõ ràng với tiêu chuẩn định lượng. | Lộ trình rõ ràng, công bằng giữa người mới & cựu binh, tách rạch ròi vai trò bán hàng vs quản lý. | Lộ trình 3 tầng sạch, có cơ chế chuyển đổi linh hoạt (cá nhân ↔ pháp nhân HKD, nhánh Chuyên gia MDRT song song nhánh Quản lý). |
| **`C13`** | Không có cơ chế giữ chân dài hạn; đại lý/lãnh đạo dễ bị đối thủ mua đứt không tổn thất. | Chỉ giữ chân bằng danh hiệu/phúc lợi nhỏ. | Có thưởng năm hoặc phí thâm niên clawback 12M. | Có thưởng trả chậm 2–3 năm gắn tái tục cho tầng Quản lý & Lãnh đạo. | Khóa giữ chân đa tầng: M12 cho người mới, 2–3 năm trả chậm gắn K2 cho Quản lý & Vùng, và bảo lưu quyền lợi khi nâng cấp mô hình HKD. |
| **`C14`** | Chính sách dài >50 trang nhiều phụ lục rời rạc, đại lý không tự nhẩm được thu nhập. | Công thức quá nhiều hệ số chồng chéo (3–4 lớp điều kiện). | Đại lý hiểu được khoản chính sau đào tạo. | Văn bản súc tích (≤15–20 trang), bảng tra trực quan, ít ngoại lệ rối rắm. | Cực kỳ tinh gọn (kiểu 6 trang của Manulife PSM+), công thức minh bạch, đại lý tự tính được thu nhập trong 2 phút. |
| **`C15`** | Nhiều mâu thuẫn nội tại (`ERR-DOC`), thiếu văn bản định nghĩa gốc, điều khoản mở chưa ban hành. | Có một số lỗi ví dụ hoặc tham chiếu văn bản cũ chưa đồng bộ. | Công thức tính được bằng hệ thống nhưng còn vài ngoại lệ thủ công. | Không mâu thuẫn nội tại, toàn bộ định nghĩa/lookup tự chứa, dễ lập trình & kiểm toán. | 100% tự chứa (self-contained), zero conflict, tách rõ phiên bản hiệu lực, số hóa hoàn toàn nghiệm thu & kiểm thử tự động trên Excel/Core system. |

---

## 4. 6 Ca Hiệu chuẩn Rubric (Calibration Test Cases — Kiểm tra Độ nhạy & Tính Nhất quán của Thang điểm)

| Mã Ca | Loại Ca Kiểm thử | Kịch bản Thử nghiệm | Kết quả Mong đợi từ Rubric | Trạng thái Kiểm tra |
|---|---|---|---|---|
| **CAL-01** | `Known-Good` (Mẫu chuẩn tốt) | Chính sách cân bằng: tuân thủ 100% TT 67/96 (`G1–G3 PASS`), Top-up 0%, HSBH theo bảo vệ, K2 sàn cứng `<60%→0%` + T+1 hold, trả chậm 3 năm `30/30/40%` cho quản lý, tổng chi phí toàn cây `68% FYP`, văn bản gọn sạch. | `Gate = PASS`; Tổng điểm trọng số **`≥ 4.2 / 5.0`**, không tiêu chí nào `< 3.5`. | **ĐẠT (`4.46 / 5.0`)** |
| **CAL-02** | `Known-Bad` (Mẫu lỗi nguy hiểm) | Chính sách đốt tiền: FYC UL 35% (vượt trần 30%!), thưởng cá nhân 120% FYC kể cả K2 = 40%, cố định 100tr không sàn KPI, không clawback, chi 100% tiền mặt tháng T. | **`Gate = FAIL (G1 & G2)`** — Chặn ngay bất kể điểm Growth; Tổng điểm **`≤ 2.0 / 5.0`**. | **ĐẠT (`FAIL_GATE`, `1.65 / 5.0`)** |
| **CAL-03** | `Borderline` (Mẫu ranh giới đánh đổi) | Chính sách giống Chubb Agency 2026: Growth & Hành vi (CH) rất mạnh (4.2–4.5), HSBH/Top-up tốt, nhưng chi phí toàn cây cao (`~90% FYP`), đáy K2 AR/AL mềm 25%, rủi ro sát trần Điều 52. | `Gate = CONDITIONAL (G2 Risk)`; Điểm Growth cao (~4.3) bị kéo cân bằng bởi Financial thấp (~2.2–2.5) → Tổng điểm ở vùng trung bình–khá **`3.1 – 3.5 / 5.0`**, không thể lọt vào nhóm xuất sắc `>4.0`. | **ĐẠT (`3.38 / 5.0`)** |
| **CAL-04** | `Missing Evidence` (Thiếu dữ liệu — Manulife) | Đánh giá Manulife chỉ từ 1 memo `PSM+/HKD` (thiếu 100% Tầng 1–2). | **Tuyệt đối không gán 0/1 điểm cho `C01–C04`, `C08` toàn cây**; chấm riêng Tầng 3 với nhãn `Coverage = 55%` và ghi rõ `INCOMPLETE_FOR_FULL_RANKING`. | **ĐẠT (Tầng 3: `3.82/5.0`, Full Coverage: `55%`)** |
| **CAL-05** | `Conflicting Evidence` (Xung đột nguồn) | Đánh giá AIA Alpha (`ERR-DOC-02` làm tròn) và Chubb (`ERR-DOC-01` bảng vs ví dụ `W1`). | Tiêu chí `C15` (Operability & Auditability) bị trừ điểm rõ ràng (từ 4 xuống ≤ 2.5–3.0) và gắn cờ xung đột chưa giải quyết. | **ĐẠT (`C15`: AIA `2.5`, Chubb `2.5`)** |
| **CAL-06** | `Minimal Pairs` (Cặp tối thiểu chỉ đổi 1 cơ chế) | So 2 phiên bản giống hệt nhau của Proposal W24, chỉ thay đổi duy nhất **bỏ trả chậm 3 năm (trả ngay 100% Y1)**. | Chỉ duy nhất `C10` (Cash Flow & Deferral) và `C13` (Retention Lock-in) giảm mạnh (-1.5 đến -2.0 điểm), kéo tổng điểm giảm ~0.20 điểm; 13 tiêu chí còn lại giữ nguyên 100%. | **ĐẠT (Delta `-0.19`, đúng 2 tiêu chí)** |

---

## 5. Kết quả Chấm điểm Sơ bộ & Kiểm tra Độ nhạy Trọng số (Weight Sensitivity Analysis)

> **Cảnh báo:** Bảng điểm dưới đây là **`DRAFT — NOT INDEPENDENTLY CALIBRATED`** và **`BASED ON AVAILABLE POLICY DOCUMENTS`**. Điểm của Manulife chỉ phản ánh **Tầng 3 (`PSM+/HKD`, Coverage 55%)**, không dùng để xếp hạng chung toàn kênh với AIA và Chubb!

| Trụ cột / Chỉ tiêu | Trọng số PO (Base) | AIA Alpha *(Tầng 1–3, thiếu Exch/HH)* | Chubb Life *(Tầng 1–3, thiếu BD/EHC)* | Manulife *(CHỈ Tầng 3 `PSM+/HKD`)* | **Proposal Primary (Balanced Hybrid)** |
|---|---:|---:|---:|---:|---:|
| **Mandatory Gate (G1–G3)** | **Gate** | `CONDITIONAL` *(thiếu HH & Exch; luật `SOURCE_NOT_VERIFIED`)* | `CONDITIONAL` *(rủi ro trần Đ.52; luật `SOURCE_NOT_VERIFIED`)* | `CONDITIONAL` *(6% Top-up + thiếu FA)* | **`CONDITIONAL`** *(thiết kế nhắm tuân thủ, chờ toàn văn `44/2026/VBHN-TT-BTC`)* |
| **I. Gia tăng Doanh số (`C01–C04`)** | **30%** | 3.77 | **4.27** | `N/A (T3: 3.60)` | **4.20** |
| **II. Chất lượng Kinh doanh (`C05–C07`)** | **25%** | **3.92** | 3.60 | `3.95` *(T3)* | **4.60** |
| **III. Hiệu quả Chi phí & ROI (`C08–C11`)** | **25%** | 3.24 | 2.48 | **`4.20`** *(T3)* | **4.52** |
| **IV. Con người & Giữ chân (`C12–C13`)** | **10%** | 3.90 | 3.10 | `4.10` *(T3)* | **4.40** |
| **V. Khả năng Triển khai (`C14–C15`)** | **10%** | 2.25 | 2.75 | **`3.75`** *(T3)* | **4.30** |
| **ĐIỂM TỔNG — Bộ Trọng số PO (30/25/25/10/10)** | **100%** | **3.54 / 5.0** | **3.39 / 5.0** | `3.92* (T3 only, 55% cov)` | **4.41 / 5.0** |

### Kiểm tra Độ nhạy Trọng số (Weight Sensitivity — 4 Kịch bản Ưu tiên của PO)
| Kịch bản Trọng số (`Growth / Quality / Financial / People / Impl`) | AIA Alpha | Chubb Life | **Proposal Primary** | Thay đổi thứ hạng Đối thủ? |
|---|---:|---:|---:|---|
| **1. PO Reference (`30 / 25 / 25 / 10 / 10`)** | **3.54** | 3.39 | **4.41** | AIA nhỉnh hơn Chubb (+0.15) nhờ kỷ luật FY 2027 & CQL trả chậm 3 năm. |
| **2. Growth-First (`45 / 15 / 15 / 15 / 10`)** | 3.58 | **3.62** | **4.36** | **ĐẢO NGƯỢC:** Chubb vượt AIA (+0.04) khi ưu tiên tối đa doanh số ngắn hạn! |
| **3. Quality-First (`20 / 40 / 20 / 10 / 10`)** | **3.59** | 3.37 | **4.46** | AIA nới rộng cách biệt (+0.22) nhờ vách đá FY 2027 & 50% SYC. |
| **4. Financial-ROI-First (`20 / 20 / 40 / 10 / 10`)** | **3.48** | 3.16 | **4.45** | Chubb tụt mạnh nhất (-0.32 so với AIA) do áp lực tổng chi phí toàn cây & không có deferral. |

**Kết luận Hiệu chuẩn:** Thứ hạng giữa AIA Alpha và Chubb Life **nhạy cảm rõ rệt với chiến lược ưu tiên của Ban Lãnh đạo** (Growth-First chọn cơ chế Chubb; Quality/ROI-First chọn kỷ luật AIA + Manulife), chứng tỏ Rubric phản ánh trung thực sự đánh đổi nghiệp vụ chứ không thiên vị cứng. Trong cả 4 bộ trọng số, **Proposal Primary (Balanced Hybrid)** đạt điểm thiết kế cao nhất (`4.36 – 4.46 / 5.0`), với điều kiện Cổng Pháp lý `G1–G3` vẫn giữ trạng thái **`CONDITIONAL`** cho đến khi đối chiếu toàn văn `44/2026/VBHN-TT-BTC` & `NĐ 97/2026/NĐ-CP` (`DEC-03`).
