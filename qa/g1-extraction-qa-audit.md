# Báo cáo Kiểm soát Chất lượng & Kiểm toán G1 (Historical G1 Snapshot — Superseded Post-Audit)

> **[HISTORICAL G1 SNAPSHOT — SUPERSEDED BY POST-AUDIT REMEDIATION]:** Đây là báo cáo tự kiểm G1 ban đầu khi catalog có 53 rules và trước khi Independent Auditor (Codex) kiểm toán checkpoint `7bcf70e` cũng như trước commit `5c2d13b` (theo dõi 7 PDF vào repo PRIVATE). Ba điểm trong bản G1 này đã được **hiệu chỉnh chính thức** tại [post-audit-remediation-register.md](file:///C:/Users/User/Desktop/TJ/Project/W24_Life-Insurance-Strategy-Lab/qa/post-audit-remediation-register.md):
> 1. **Chấm dứt tự phán xử mâu thuẫn (`ERR-DOC-01` & `ERR-DOC-02`):** Không còn áp đặt một cách hiểu duy nhất; cả 2 xung đột được gắn `CONFLICTING_EVIDENCE`, mô hình hóa 2 chế độ (toggle) và đưa vào [decision-register.md](file:///C:/Users/User/Desktop/TJ/Project/W24_Life-Insurance-Strategy-Lab/docs/decisions/decision-register.md).
> 2. **Trạng thái Git cho `private/sources/`:** Tại commit `5c2d13b` (theo phê duyệt của TJ), 7 PDF nguồn đã được track trong Git trên repo **PRIVATE** (thay vì bị `.gitignore` chặn như thời điểm G1).
> 3. **Quy mô Catalog & Lookup:** Đã mở rộng từ 53 rules lên 112 rules (3 cột trạng thái chuẩn Section 32) và chuẩn hóa 100% bảng PAF+ (1,300 dòng) & Hoa hồng Chubb (113 dòng + 10 dòng HSBH).
> Nội dung gốc bên dưới được giữ nguyên làm lịch sử G1.

**Ngày thực hiện (G1):** 2026-11-26  
**Phạm vi (G1):** 7 tài liệu chính sách gốc (`116 trang`) đã tiếp nhận trong G1, `knowledge/sources/source-registry.csv`, phiên bản G1 của `knowledge/business-rules/business-rules-catalog.csv` (53 rules), `schemas/compensation-scheme.schema.json`, và `outputs/working/competitor-comparison-v1.0.md`.  
**Người thực hiện:** AGY (tự kiểm tra chất lượng nội bộ — **KHÔNG** tuyên bố là kiểm toán độc lập vì cùng một agent trích xuất và kiểm tra).  
**Trạng thái tổng thể:** `INSPECTED` (L1 Logic, L2 Evidence, L4 Adversarial Design Review) | `NOT RUN` (L3 Independent Reproducibility trên Excel — sẽ chạy ở Ngày 2 bằng Golden Test Cases).

---

## 1. Đánh giá theo Rubric A — Chất lượng Trích xuất Chính sách `[STATUS: DRAFT — CHƯA CALIBRATION]`

| Tiêu chí Rubric A | Kết quả kiểm tra | Bằng chứng cụ thể | Điểm còn hạn chế |
|---|---|---|---|
| **Đúng nội dung nguồn & Đủ trang** | ĐẠT (7/7 file) | Đã đọc trọn 116/116 trang (6 PDF text trích xuất toàn văn + bảng; 1 PDF scan `CHH0DCEB260003V` render 15 ảnh PNG và đọc trực quan 15/15 trang). Kiểm chứng hash SHA-256 100% bản sao trong `private/sources/`; xác minh `.7z` trùng 100% bằng CRC32. | Không có OCR tự động cho bản scan (đã khắc phục bằng đọc trực quan toàn bộ 15 trang ảnh). |
| **Đầy đủ quy tắc & cấu phần thu nhập** | ĐẠT (50 rule thật + 3 trần pháp lý) | Bao phủ đầy đủ FYC/RYC (Chubb), Allowance, Activation (1/72H, 3M, New AR), Production/Performance Tháng–Quý–Năm, Quality/SYC/RYC Bonus, Direct & Indirect Override, Promotion Bonus, Deferred Retention 3 năm, Champion Hubb, Clawback, Cap, Payment Timing. | Một số cấu phần nằm ở văn bản tham chiếu ngoài bộ file (xem Mục 4). |
| **Đúng đối tượng, điều kiện & ngoại lệ** | ĐẠT | Tách bạch tuyệt đối 3 tầng (`Individual_Agent`, `Mid_Management`, `Senior_Executive_Leader`). Ghi rõ ngoại lệ (ví dụ: PAF+ không hưởng 1/72H & override gián tiếp CQL; AL Chubb không tính FYC bản thân vào FYC NTT; Manulife PSM+ tính 6% top-up vào FYP). | Cần lưu ý không gộp Manulife `PSM+` vào bảng so sánh Đại lý cá nhân. |
| **Truy vết Source ID, phiên bản & số trang** | ĐẠT (100%) | Chạy script kiểm chứng tự động `build_rules_catalog.py`: 53/53 dòng không trùng `Rule_ID`, đủ 22 cột, 100% có `Source_ID` và số trang cụ thể. | Chưa chạy đối chiếu chéo bởi người/agent thứ hai (chưa phải Independent Audit). |
| **Xử lý thông tin chưa rõ / mâu thuẫn** | ĐẠT | Không bịa bất kỳ con số nào cho các văn bản thiếu (`UNKNOWN`). Ghi nhận rõ mọi lỗi đánh máy & mâu thuẫn nội tại ngay trong văn bản gốc (xem Mục 2). | — |

---

## 2. Phân tách Rõ: Lỗi Đã Chứng minh trong Tài liệu Gốc vs. Nghi vấn vs. Dữ liệu Thiếu

### A. Lỗi / Mâu thuẫn nội tại ĐÃ CHỨNG MINH trực tiếp trong văn bản gốc (`VERIFIED FACT`)

| ID | Tài liệu & Trang | Nội dung lỗi / bất nhất phát hiện | Mức độ ảnh hưởng đến tính toán | Cách xử lý chuẩn trong W24 |
|---|---|---|---|---|
| **ERR-DOC-01** | `SRC-POL-CHB-001` (`CHH0DCEB260007V`, **trang 9 vs. trang 10**) | Bảng quy định Champion Hubb trang 9 ghi: `SOP từ 80% đến dưới 90% → W1 = 80%` (và `70% đến dưới 80% → W1 = 50%`). Nhưng **bảng ví dụ minh họa trang 10** ở tháng M11 & M12 ghi `SOP = 85%` nhưng lại áp **`W1 = 50%`** (lệch hẳn 30% mức thưởng trong ví dụ!). | **CAO** (nếu máy móc bắt chước ví dụ sẽ tính sai 30% thưởng Champion Hubb). | **Áp dụng đúng bảng quy định chính thức (trang 9: 80–90% → W1 = 80%)**, đồng thời ghi chú lỗi ví dụ để xác minh lại nếu triển khai thực tế. |
| **ERR-DOC-02** | `SRC-POL-AIA-ALP-001` (`AIAV/AD/2604-069`, **trang 14**) vs. `SRC-POL-AIA-ALP-002` (**trang 21**) | Trang 14 file CVTV ghi chữ "làm tròn **lên** đến 0 số thập phân" (ví dụ `90.666% → 91%`), trong khi file CQL (trang 21) & PAF+ (trang 18) ghi rõ là **làm tròn chuẩn** (`≥0.5` làm tròn lên: `74.50% → 75%`, `74.49% → 74%`). | **TRUNG BÌNH** (ảnh hưởng đại lý nằm sát ngưỡng 64.5%–69.5% FY). | Ghi nhận mâu thuẫn giữa câu chữ "làm tròn lên" (file CVTV) vs. "làm tròn gần nhất ≥0.5" (file CQL/PAF+); ưu tiên quy tắc chi tiết có 2 ví dụ biên (`74.49% vs 74.50%`) và đưa vào test case biên. |
| **ERR-DOC-03** | `SRC-POL-AIA-ALP-002` (`AIAV/AD/2601-034`, **trang 6 & 15**) vs. `SRC-POL-AIA-ALP-001` (`2604-069`) | File CQL ban hành 03/02/2026 tham chiếu bản CVTV cũ `AIAV/AD/2601-033 (Mục I.10)` và trang 15 dẫn chiếu nhầm "Mục C" (thực tế điều kiện duy trì là Mục D trang 10). File CVTV trong bộ dữ liệu là bản cập nhật `2604-069` (hiệu lực 01/04/2026), mục Phí giới thiệu là **Mục I.9** (trang 7). | **THẤP** (tỷ lệ thưởng 5%/10%/20% khớp nhau, chỉ lệch số hiệu mục & bản cũ/mới). | Áp dụng bản hiệu lực mới nhất `2604-069` (01/04/2026) và ghi chú quan hệ thay thế trong `source-registry.csv`. |
| **ERR-DOC-04** | `SRC-POL-AIA-ALP-001` (**trang 2 vs. trang 17**); `002/003` (**trang 1**); `003` (**trang 8**); `CHB-002` (**trang 12**) | Các lỗi biên tập hành chính: (i) CVTV Alpha trang 2 ghi `UM = Trưởng Nhóm, DM = Trưởng Phòng`, trang 17 định nghĩa `UM = Trưởng Phòng, DM = Giám Đốc Ban`; (ii) CQL & PAF+ Alpha trang 1 thư ngỏ ghi nhầm "năm 2025"; (iii) PAF+ trang 8 ghi "quý 2/202"; (iv) Chubb `0008V` trang 12 ghi thừa số 0 `9.000.0000`. | **RẤT THẤP** (không làm sai bản chất công thức, chỉ ảnh hưởng tên gọi). | Chuẩn hóa theo mã chức danh tiếng Anh (`UM/SUM/DM/SDM`, `PAF+`, `AR/AL/BD/RD`) trong toàn bộ mô hình. |

### B. Rủi ro Lợi dụng Chính sách & Thiết kế (L4 Adversarial Review)

1. **Rủi ro "bơm số ngắn hạn & vượt ngưỡng cộng dồn" ở Chubb Life (`AR/AL/RD`):**
   - Tầng Đại lý/Quản lý: K2 `<50%` vẫn nhận **25%** thưởng HQKD tháng & quý (chưa chặn về 0%), trong khi đỉnh thưởng AR lên tới **85.8% FYC** và AL lên tới **109.2% FYC** (cá nhân) / **108% FYC NTT** (quản lý) → nếu đại lý chất lượng thấp vẫn chạy khối lượng lớn hoặc dồn doanh số qua mã AL kỳ cựu (≥15M), chi phí phân phối bị đẩy lên rất cao.
   - Tầng RD: Thưởng tăng trưởng Quý lên tới **27.5% FYC** dựa trên tăng trưởng QoQ/YoY tạo động cơ **nén doanh số quý thấp để bứt phá quý sau (gaming/sandbagging)**, dù đã có điều kiện `FYP < 360tr` bị khóa ở `2.5%`.
2. **Rủi ro "chi phí cố định + phân tầng sâu + vách đá sốc 2027" ở AIA Alpha:**
   - Tầng PAF+: Phí cố định 20–130tr/tháng + Dual Career + chuỗi override gián tiếp 50% vô hạn tầng làm **định phí & tổng payout tỷ lệ thuận mạnh theo số tầng quản lý** nếu nhiều nhánh cùng đạt chỉ tiêu thấp/trung bình (chỉ cần đạt 55% FYP đã hưởng 100% phí cố định!).
   - Tầng CVTV: Vách đá cứng **FY < 70% → 0%** áp dụng từ 2027 tạo rủi ro rớt thu nhập đột ngột (cliff effect) ở mức 69% vs. 70% — một điểm cực nhạy dễ gây mất động lực hoặc tìm cách "cứu phí ảo" để giữ mốc 70%.
3. **Rủi ro "điều khoản mở" ở Manulife (`PSM+/HKD`):**
   - Điều khoản C.1 (`p.5`) ghi: *"Từ tháng 02/2026, PSM+/HKD+ sẽ cần hoàn thành Yêu cầu về hoạt động dịch vụ... quy định trong thông báo sau"* — chưa rõ chi tiết nên chưa thể đánh giá độ khó thực thi.
   - Định nghĩa FYP tại `p.6` vẫn tính **6% phí đóng thêm (Top-up)** — cần rà soát lại khi **TT 96/2026/TT-BTC** có hiệu lực 01/01/2027 siết hoa hồng phí đóng thêm.

### C. Dữ liệu còn thiếu (`UNKNOWN` — Chưa đủ để kết luận tuyệt đối)

| Nhóm dữ liệu thiếu | Tác động đến mô hình Ngày 2 | Phương án xử lý an toàn trong deadline 3 ngày |
|---|---|---|
| **Manulife:** Chính sách Đại lý cá nhân (FA), CQL cấp trung (UM/SUM/DM), Biểu hoa hồng, Bảng chỉ tiêu FYP/1mAA PSM+, Công thức K2 (`0016M03/2024`) | Không thể so sánh Manulife ở Tầng 1 & Tầng 2; chỉ so sánh Manulife ở Tầng 3 (`PSM+/HKD`) dựa trên `% hoàn thành chỉ tiêu`. | Giữ Manulife ở Tầng 3 trong bảng đối thủ; ghi nhãn `UNKNOWN` rõ ràng ở Tầng 1–2; thiết kế Excel mở sẵn cột `Manulife_Agent` để TJ điền vào bất kỳ lúc nào có file. |
| **AIA:** Biểu tỷ lệ hoa hồng (FYC/RYC), Memo `FYC Tín Chỉ`, Chính sách `Exchange / Exchange Pro` & `AFF`, Chính sách Kênh Truyền thống AIA | Khi so sánh AIA Alpha vs. Chubb Life theo `% FYP`, phải giả định chuẩn hóa `FYC Tín Chỉ = FYC thực thu (30% UL)` (ghi nhãn `ASSUMPTION`). Chưa lượng hóa được gói trợ cấp toàn thời gian Exchange/Pro. | So sánh trực tiếp theo `% trên FYC` (chính xác 100% không cần giả định hoa hồng!), và thêm lớp quy đổi sang `% FYP` dựa trên biểu hoa hồng thật của Chubb Life + giả định chuẩn 30% UL có ghi nhãn rõ. |
| **Chubb Life:** `CHH0DCEB260005V` & `260006V` (định nghĩa `EHC`, công thức `K2/P13`, clawback tổng quát), Chính sách `BD`, `260009V` | Chưa biết chính xác ngưỡng FYP/FYC để đạt `1 EHC` (giả định tương đương chuẩn thị trường `4tr FYC / 15tr FYP` để mô phỏng và ghi nhãn `ASSUMPTION`). | Cho phép PO chỉnh tham số `EHC threshold` trên sheet `Parameters` của Excel. |
| **Dữ liệu kinh doanh & tài chính nội bộ:** Active Ratio thực, K2 thực, VNB margin, định phí | Không thể tuyên bố ROI tuyệt đối hay khẳng định chính sách nào đang "thắng" trên thực tế. | Phân tích **Độ nhạy (Sensitivity Analysis)** và **Điểm hòa vốn (Break-even VNB Margin)** trên Excel để chứng minh chính sách đề xuất có ROI dương trong dải điều kiện cụ thể nào. |

---

## 3. Kiểm tra Bảo mật & Tuân thủ Quyền hạn

- [x] Không chỉnh sửa, đổi tên hay xóa bất kỳ file gốc nào trong thư mục nguồn Downloads.
- [x] Đã xác minh `.gitignore` chặn tuyệt đối `private/` (`git check-ignore -v` & `git status --short` xác nhận 0 file `private/` lọt vào Git).
- [x] Cả 7 tài liệu đã đọc đều là văn bản chính sách chung, **không phát hiện PII khách hàng hay bảng lương cá nhân**.
- [x] Không lưu đường dẫn cá nhân ngoài repo vào `source-registry.csv` hay các tài liệu chia sẻ.
- [x] Không dùng công cụ/dịch vụ upload PDF ra bên ngoài; 100% xử lý cục bộ bằng Python.
