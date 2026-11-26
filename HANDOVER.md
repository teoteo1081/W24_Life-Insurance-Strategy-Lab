# HANDOVER.md — Điểm Bàn giao & Checkpoint Dự án

**Cập nhật lần cuối:** 2026-11-26 (Checkpoint G1 — Hoàn tất tiếp nhận, trích xuất 53 Business Rules & So sánh Đối thủ v1.0 từ 7 tài liệu thực tế)  
**Người thực hiện:** AGY  
**Business Owner:** TJ  

---

## 1. Mục tiêu hiện tại
Hoàn thành bài tư vấn theo **Primary Business Anchor (`SRC-REQ-001` — Bước 1 của chị Nhi)** trong deadline 3 ngày: phân tích chính sách thu nhập giữa các công ty và đề xuất chính sách phù hợp tại thị trường VN (gia tăng doanh số, chất lượng kinh doanh, hiệu quả chi phí & ROI). Hiện đã hoàn tất **G1 (Phân tích tài liệu thực tế & So sánh đối thủ v1.0)** và sẵn sàng bước vào **G2 (Excel Reference Model + 3 hướng Compensation Scheme + Golden Test Cases)**.

## 2. Công việc đã hoàn thành (Từ đầu đến G1)
- **Kiểm kê & Tổ chức tài liệu thực tế (Nhiệm vụ 1–2):** Quét 8 file từ nguồn TJ cung cấp; xác minh 100% bằng CRC32 rằng file `Chính sách thu nhập.7z` là bản nén trùng khớp từng bit của 7 file PDF bên ngoài (không sao chép trùng). Đã sao chép 7 file PDF vào `private/sources/{AIA-Alpha,Manulife,Chubb-Life}/` (được `.gitignore` bảo vệ tuyệt đối) và xác minh nguyên vẹn 100% bằng SHA-256.
- **Đọc trọn vẹn 116/116 trang tài liệu gốc:** Đọc toàn văn + bảng của 6 PDF text và đọc trực quan 15/15 trang ảnh của file scan Chubb Life `CHH0DCEB260003V` (Giám đốc Vùng RD). Xác nhận 100% bằng chứng trực tiếp rằng **Kênh Alpha là kênh của AIA Việt Nam**.
- **Cập nhật Source Register (Nhiệm vụ 3):** `knowledge/sources/source-registry.csv` đủ 16 cột chuẩn quản trị nguồn, không chứa đường dẫn cá nhân ngoài repo.
- **Trích xuất Business Rules (Nhiệm vụ 4):** `knowledge/business-rules/business-rules-catalog.csv` gồm **53 quy tắc** (50 `VERIFIED_FACT` từ 7 PDF gốc + 3 trần pháp lý `SOURCE_CLAIM` từ TT 67/2023 & TT 96/2026), 100% truy vết đến `Source_ID`, phiên bản và số trang.
- **Competitor Comparison Matrix v1.0 (Nhiệm vụ 5):** `outputs/working/competitor-comparison-v1.0.md` so sánh chuẩn hóa đúng 3 tầng bậc (Tầng 1: AIA Alpha CVTV vs. Chubb AR/CH; Tầng 2: AIA Alpha CQL vs. Chubb AL; Tầng 3: AIA Alpha PAF+ vs. Manulife PSM+/HKD vs. Chubb RD), kèm minh họa định lượng tính bằng Python trên cùng bộ giả định chuẩn hóa và tách bạch 5 lớp bằng chứng.
- **Kiến trúc Dữ liệu Tái sử dụng (Nhiệm vụ 6):** `schemas/compensation-scheme.schema.json` và `docs/architecture/reusable-model-schema.md` cho phép nạp thêm PDF đối thủ/proposal mới mà không cần sửa công thức Excel hay HTML Simulator.
- **Kiểm soát chất lượng G1 (Nhiệm vụ 7):** `qa/g1-extraction-qa-audit.md` áp dụng Rubric A (`DRAFT`) + Risk-Adaptive Audit (L1/L2/L4), chỉ ra 4 nhóm lỗi/bất nhất có thật trong tài liệu gốc (điển hình: lỗi `W1=50%` tại `SOP=85%` trong ví dụ trang 10 Chubb `0007V` và mâu thuẫn làm tròn AIA FY trang 14 vs. 21).

## 3. File đã tạo hoặc sửa trong G1
- **Tạo mới (Git-tracked):**
  - `schemas/compensation-scheme.schema.json`
  - `docs/architecture/reusable-model-schema.md`
  - `outputs/working/competitor-comparison-v1.0.md`
  - `qa/g1-extraction-qa-audit.md`
- **Cập nhật (Git-tracked):**
  - `knowledge/sources/source-registry.csv`
  - `knowledge/business-rules/business-rules-catalog.csv`
  - `ANCHOR_SPEC.md`
  - `HANDOVER.md`
  - `CHANGELOG.md`
- **Bản sao nội bộ (KHÔNG track trong Git, bị `.gitignore` chặn):**
  - `private/sources/AIA-Alpha/` (3 PDF)
  - `private/sources/Manulife/` (1 PDF)
  - `private/sources/Chubb-Life/` (3 PDF)

## 4. Bằng chứng
- Xác minh toàn vẹn file copy: 7/7 SHA-256 khớp 100% nguồn; `.7z` khớp 7/7 CRC32.
- Xác minh bảo mật: `git check-ignore -v private/` và `git status --short` xác nhận 0 file `private/` trong Git.
- Xác minh cấu trúc CSV: script kiểm tra 53/53 `Rule_ID` duy nhất, đủ 22 cột, 100% có `Source_ID` & trang.
- Minh họa định lượng tầng Đại lý cá nhân được tính trực tiếp bằng Python trên công thức thật của AIA Alpha (`2604-069`) và Chubb Life (`0007V`).

## 5. Kết quả kiểm thử thực tế
- CSV integrity check (`build_rules_catalog.py`): **PASS** (53 rules, 0 duplicate, 0 missing source/page).
- Minh họa định lượng Python (AIA Alpha vs. Chubb Life AR ở 30tr & 90tr FYC/quý, K2 85% vs 65%): **PASS**.
- Golden Test Cases cho Excel Reference Model: `NOT RUN` (sẽ thực hiện ở G2 / Ngày 2).

## 6. Kết quả kiểm toán
- G1 Extraction QA & Risk-Adaptive Audit (`qa/g1-extraction-qa-audit.md`): `INSPECTED` (L1 Logic, L2 Evidence đối chiếu 116 trang gốc, L4 Adversarial phát hiện lỗi ví dụ & rủi ro trục lợi) — **lưu ý: tự kiểm tra bởi AGY, chưa phải audit độc lập**.
- L3 Reproducibility trên Excel: `NOT RUN`.

## 7. Những việc chưa kiểm chứng
- Toàn văn Thông tư 96/2026/TT-BTC và Thông tư 67/2023/TT-BTC (hiện dùng nguồn tóm tắt pháp lý công khai `SOURCE_CLAIM`).
- Các tài liệu tham chiếu ngoài bộ file (xem mục 8).
- Hiệu quả kinh doanh thực tế (Persistency K2 thực, Active Ratio thực, chi phí thực trả / APE, VNB margin) của AIA Alpha, Manulife và Chubb Life.

## 8. Blocker & Khoảng trống Dữ liệu (Không chặn bước G2)
Không có blocker cứng làm dừng dự án, nhưng có **3 nhóm tài liệu tham chiếu còn thiếu** cần lưu ý:
1. **Manulife (`SRC-GAP-002`):** Thiếu chính sách Đại lý cá nhân (FA), Quản lý cấp trung (UM/SUM/DM), Biểu hoa hồng sản phẩm, Công thức K2 (`0016M03/2024`) và Bảng chỉ tiêu FYP/1mAA của PSM+.
2. **AIA (`SRC-GAP-001`):** Thiếu Biểu hoa hồng sản phẩm, Memo quy đổi `FYC Tín Chỉ`, Chính sách hỗ trợ `Exchange / Exchange Pro` & `AFF`, Chính sách Kênh Truyền thống AIA.
3. **Chubb Life (`SRC-GAP-003`):** Thiếu văn bản định nghĩa chung (`CHH0DCEB260005V`, `260006V` — định nghĩa `EHC`, công thức `K2/P13`, clawback tổng quát), Chính sách `BD`, và `CHH0DCEB260009V` (hỗ trợ ĐVKD mới).

## 9. Quyết định cần TJ
1. TJ có bổ sung thêm tài liệu cho 3 nhóm thiếu trên (đặc biệt là **Manulife Đại lý/CQL** và **AIA Truyền thống/Exchange/Biểu hoa hồng**) trước khi AGY chốt Excel Reference Model không?
2. Xác nhận định dạng bàn giao **Gói A (Interview Delivery cho chị Nhi)**: Slide deck (5–7 slides) hay Executive Brief (Markdown/PDF/Word)?
3. Xác nhận cho AGY chạy ngay **G2 (Ngày 2):** xây **Excel Reference Model (tách Inputs/Scheme_Config/Formulas/Outputs + 7 hồ sơ đại lý chuẩn + MAPA xuôi/ngược + Sensitivity & Break-even ROI)** + **Thiết kế 3 phương án Compensation Scheme (A: Growth, B: Quality, C: Balanced/Hybrid)** + **Golden Test Cases kiểm chứng bằng Python**.

## 10. Trạng thái Git
- Nhánh `main` (local only, không remote, không push). Thư mục `private/` được `.gitignore` bỏ qua hoàn toàn.

## 11. Commit SHA
- Checkpoint trước: `f9aabdf`. Commit G1: xem `git log -n 1` ngay sau thao tác commit cuối lượt.

## 12. Các sản phẩm P0 còn thiếu
- [ ] Thiết kế chi tiết 3 phương án Compensation Scheme đề xuất (A: Growth, B: Quality, C: Balanced/Hybrid) phục vụ `REQ-02..REQ-05`.
- [ ] Excel Reference Model kiểm chứng được (tách Inputs/Config/Formulas/Outputs + 7 nhóm đại lý + Chi phí/Chất lượng/Độ nhạy/Điểm hòa vốn ROI) + Golden Test Cases (`tests/`).
- [ ] Bản trình bày lãnh đạo Gói A (5–7 trang/slide tại `outputs/interview/`).
- [ ] Đối soát cuối cùng & Audit Ngày 3 trước khi bàn giao.

## 13. Hành động tiếp theo (G2 — Ngày 2)
1. Thiết kế 3 phương án Compensation Scheme đề xuất (tuân thủ TT 96/2026 từ 01/01/2027, kế thừa điểm mạnh & vá lỗ hổng từ AIA Alpha, Manulife PSM+, Chubb Life).
2. Xây dựng **Excel Reference Model (`outputs/working/W24_Compensation_Reference_Model_v1.xlsx`)** cấu hình hoàn toàn theo `schemas/compensation-scheme.schema.json` với công thức Excel thật (không hard-code), mô phỏng 7 nhóm đại lý chuẩn + MAPA xuôi/ngược + Financial Sensitivity & Break-even ROI.
3. Viết và chạy **Golden Test Cases độc lập bằng Python (`tests/test_compensation_golden.py`)** kiểm chứng mọi công thức biên (0 doanh số, dưới/đúng/trên ngưỡng, K2 cliff, clawback 6M, cap, tính xuôi/ngược MAPA).

## 14. Tiến độ so với deadline
- **Ngày 1 / 3 — HOÀN THÀNH VƯỢT MỤC TIÊU NGÀY 1:** Đã đọc xong 100% 7 tài liệu gốc (116 trang), trích xuất 53 business rules có nguồn, hoàn thiện Competitor Comparison Matrix v1.0, thiết kế Reusable Schema và hoàn tất QA Audit G1. Đủ dư địa vững chắc cho Ngày 2 (Excel + 3 Scheme + Tests) và Ngày 3 (Audit + Gói A Interview Delivery).
