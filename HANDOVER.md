# HANDOVER.md — Điểm Bàn giao & Checkpoint Dự án

**Cập nhật lần cuối:** 2026-11-26 (Checkpoint G1 Deep — Hoàn tất Deep Policy Understanding, 108 Atomic Rules, Cross-Doc Map, Coverage Audit Matrix 116p, 12-Dimension Strategy Analysis & Bottom-up Model Spec)  
**Người thực hiện:** AGY  
**Business Owner:** TJ  

---

## 1. Mục tiêu hiện tại
Hoàn tất tuyệt đối nền tảng hiểu sâu chính sách thực tế (**G1 Deep Policy Understanding & Coverage Audit**) cho 3 công ty (7 memo, 116 trang) phục vụ **Primary Business Anchor (`SRC-REQ-001` — Bước 1 của chị Nhi)** trước khi chuyển sang **G2 (Thiết kế 3 Scheme đề xuất & Excel Reference Model xuất phát từ thực tế memo)**.

## 2. Công việc đã hoàn thành (G1 Deep)
- **Kiểm kê lại 100% nguồn & attachments:** Quét lại thư mục gốc Downloads (0 thư mục con, 8 file: 7 PDF + 1 `.7z` trùng 100% CRC32), kiểm tra 0 embedded files / 0 annotations trong 7 PDF (44 links chỉ là mục lục nội bộ Chubb & watermark CamScanner). Đã sửa chính xác 100% SHA-256 của file `.7z` trong `source-registry.csv`.
- **Xây dựng Policy Knowledge Base (3 cẩm nang chuyên sâu tiếng Việt, có sơ đồ Mermaid & ví dụ tính toán thực tế):**
  - `knowledge/policies/aia-alpha-2026-deep-guide.md`
  - `knowledge/policies/chubb-life-agency-2026-deep-guide.md`
  - `knowledge/policies/manulife-psm-hkd-2026-deep-guide.md`
- **Cross-Document Mapping đầy đủ 25 mục tham chiếu chéo:** `knowledge/policies/cross-document-mapping.md` (sơ đồ Mermaid + bảng phân loại Đã có / Đã bị thay thế / Thực sự thiếu + ảnh hưởng nghiệp vụ).
- **Mở rộng Glossary thực tế:** `knowledge/glossary/glossary.md` bao phủ mọi thuật ngữ từ 7 memo và cảnh báo trùng mã viết tắt khác nghĩa (`SA` AIA vs. `SA` Manulife, `SM` Chubb vs. `SM` Manulife, `DM` AIA vs. `DM` Chubb).
- **Mở rộng Business Rules lên 108 Atomic Rules:** `knowledge/business-rules/business-rules-catalog.csv` gồm **105 rules `VERIFIED_FACT`** từ 7 memo gốc + **3 trần pháp lý `SOURCE_CLAIM`** (tăng từ 53 lên 108 rules, tách nguyên tử từng điều khoản thưởng, chuyển tiếp, làm tròn, ngoại lệ, clawback, tạm giữ).
- **Coverage Audit Matrix trọn vẹn 116/116 trang:** `qa/g1-coverage-audit-matrix.md` phân tách 5 cấp độ hiểu biết (Đọc → Hiểu → Trích xuất → Kiểm chứng → Tính toán chính xác) và kiểm toán từng trang/mục theo 6 nhãn trạng thái.
- **Phân tích Chiến lược 12 khía cạnh từng công ty:** `docs/research/competitor-strategy-analysis.md` tách rõ chiến lược xác nhận trong văn bản vs. chiến lược suy luận từ thiết kế chính sách.
- **Bottom-up Model Requirements:** `docs/architecture/bottom-up-model-requirements.md` xác định 10 Business Entities, phân loại tham số dùng chung vs. đặc thù từng scheme và 14 năng lực bắt buộc của Rule Engine xuất phát từ 108 rules thực tế.

## 3. File đã tạo hoặc sửa trong G1 Deep
- **Tạo mới (Git-tracked):**
  - `knowledge/policies/aia-alpha-2026-deep-guide.md`
  - `knowledge/policies/chubb-life-agency-2026-deep-guide.md`
  - `knowledge/policies/manulife-psm-hkd-2026-deep-guide.md`
  - `knowledge/policies/cross-document-mapping.md`
  - `qa/g1-coverage-audit-matrix.md`
  - `docs/research/competitor-strategy-analysis.md`
  - `docs/architecture/bottom-up-model-requirements.md`
- **Cập nhật (Git-tracked):**
  - `knowledge/sources/source-registry.csv` (sửa SHA-256 chính xác của `.7z`)
  - `knowledge/glossary/glossary.md` (mở rộng đầy đủ thuật ngữ 7 memo)
  - `knowledge/business-rules/business-rules-catalog.csv` (nâng từ 53 → 108 atomic rules)
  - `ANCHOR_SPEC.md` (`REQ-01` → `DONE_G1_DEEP`)
  - `HANDOVER.md`, `CHANGELOG.md`
- **Bản sao nội bộ (không track Git, `.gitignore` chặn 100%):** `private/sources/{AIA-Alpha,Manulife,Chubb-Life}/` (7 PDF).

## 4. Bằng chứng
- Quét toàn văn 6 PDF text bằng regex + kiểm tra trực quan 15/15 ảnh scan `CHH0DCEB260003V` để xác nhận 100% tham chiếu chéo & điều khoản.
- Kiểm tra cấu trúc CSV & JSON Schema tự động bằng Python (`source-registry.csv`: 16×16; `business-rules-catalog.csv`: 108×22, 0 trùng `Rule_ID`, 100% có `Source_ID` & trang).

## 5. Kết quả kiểm thử thực tế
- CSV & JSON Schema validation: **PASS** (108 atomic rules + 16 sources).
- Golden Test Cases trên Excel Reference Model: `NOT RUN` (chưa sang G2 theo đúng yêu cầu TJ).

## 6. Kết quả kiểm toán
- Coverage Audit Matrix (`qa/g1-coverage-audit-matrix.md`) & Extraction QA (`qa/g1-extraction-qa-audit.md`): `INSPECTED` (tự kiểm tra nội bộ bởi AGY, **chưa phải kiểm toán độc lập**).
- Ghi nhận rõ các điểm mâu thuẫn nội tại (`ERR-DOC-01`: lỗi ví dụ `W1=50%` ở `SOP=85%` p.10 Chubb `0007V`; `ERR-DOC-02`: làm tròn lên vs. chuẩn AIA FY p.14 vs. p.21; `ERR-DOC-03/04`: lỗi biên tập/dẫn chiếu) và điều khoản mở (`MNL-PM-010`: yêu cầu hoạt động dịch vụ từ 02/2026).

## 7. Những việc chưa kiểm chứng
- Khả năng tính toán chính xác 100% từ FYP thô cho AIA Alpha (do thiếu Phụ lục Hoa hồng & Memo `FYC Tín Chỉ`) và tính `EHC/K2` gốc cho Chubb Life (`CHH0DCEB260005V`) & Manulife (`0016M03/2024`).
- Hiệu quả kinh doanh thực tế (Active Ratio, Persistency K2 thực, Total Comp/APE thực, VNB margin) của cả 3 hãng.

## 8. Tài liệu thực sự còn thiếu (Ảnh hưởng cao nhất đến G2)
1. **AIA Alpha:** Phụ lục Hoa hồng sản phẩm, Memo `FYC Tín Chỉ`, Chính sách `Exchange / Exchange Pro` & `AFF`, `AIAV/AD/2501-017` (3 tiêu chí chất lượng), `AIAV/AD/2601-023` (khóa học), `AIAV/AD/2401-029` (HĐ thay thế).
2. **Manulife:** Toàn bộ chính sách Đại lý cá nhân (FA), Quản lý cấp trung (UM/SUM/DM), Biểu hoa hồng, `0016M03/2024/ASBD` (công thức TLDTHD), Bảng chỉ tiêu FYP/1mAA, Thông báo mở Mục C.1 (từ 02/2026).
3. **Chubb Life:** `CHH0DCEB260005V` & `260006V` (định nghĩa `EHC`, công thức `K2/P13`, clawback chung), Chính sách 2026 cho cấp `BD`, `CHH0DCEB260009V` (Phí XD ĐVKD mới).

## 9. Quyết định cần TJ
1. TJ rà soát Policy Knowledge Base & Coverage Audit Matrix: có bổ sung thêm văn bản nào trong danh sách thiếu ở Mục 8 không (đặc biệt Manulife FA/CQL, AIA Hoa hồng/Exchange, Chubb `260005V`)?
2. Khi TJ hài lòng với mức độ hiểu sâu G1, xác nhận để AGY chuyển sang **G2** (Thiết kế 3 Scheme đề xuất + xây **Excel Reference Model** theo đúng Bottom-up Model Spec + **Golden Test Cases**) và xác nhận định dạng **Gói A** (Slide deck 5–7 slides hay Executive Brief).

## 10. Trạng thái Git
- Nhánh `main`, remote `origin` trỏ tới **PRIVATE repository** `https://github.com/teoteo1081/W24_Life-Insurance-Strategy-Lab` (tài khoản `teoteo1081`).
- Theo xác nhận tường minh của Business Owner (TJ) ngày 2026-11-26, 7 file PDF nguồn trong `private/sources/` đã được commit & push lên repo **PRIVATE** này. **Cảnh báo bảo mật:** tuyệt đối giữ repo ở chế độ `PRIVATE`, không chuyển sang Public và không chia sẻ ra bên ngoài.

## 11. Commit SHA
- Checkpoint G1 Deep: `7bcf70e`. Commit bật tracking `private/sources/` & đồng bộ GitHub Private: xem `git log -n 1`.

## 12. Các sản phẩm P0 còn thiếu (G2 & G3)
- [ ] Thiết kế 3 phương án Compensation Scheme đề xuất (A: Growth, B: Quality, C: Balanced/Hybrid) tuân thủ TT 96/2026.
- [ ] Excel Reference Model (cấu hình theo Bottom-up Model Spec, 7 hồ sơ đại lý + 3 tầng lãnh đạo + MAPA + Sensitivity & Break-even ROI) + Golden Test Cases (`tests/`).
- [ ] Bản trình bày lãnh đạo Gói A (5–7 trang/slide tại `outputs/interview/`).
- [ ] Audit & đối soát cuối Ngày 3.

## 13. Hành động tiếp theo
Chờ TJ nghiệm thu gói **G1 Deep Policy Understanding & Coverage Audit** (và cung cấp thêm tài liệu bổ sung nếu có), sau đó khởi chạy G2 đúng theo `docs/architecture/bottom-up-model-requirements.md`.

## 14. Tiến độ so với deadline
- **Cuối Ngày 1 / 3:** Nền tảng hiểu sâu chính sách đã đạt mức rất vững (116/116 trang kiểm toán, 108 atomic rules, 3 Deep Guides, 25 cross-doc references, 12-dimension strategy, Bottom-up Model Spec). Sẵn sàng tăng tốc G2 (Ngày 2) và G3 (Ngày 3) ngay khi TJ bật đèn xanh.
