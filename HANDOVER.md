# HANDOVER.md — Điểm Bàn giao & Checkpoint Dự án

**Cập nhật lần cuối:** 2026-11-26 (Checkpoint Post-Audit Remediation + Full Benchmarking, 12M Engine, Excel 12.0 COM Verified Model & Package A Executive Delivery)  
**Người thực hiện:** AGY (Sole Execution Agent)  
**Business Owner:** TJ  
**Independent Auditor:** Codex (đã kiểm toán G1 tại `7bcf70e342a4baff34b50c215c010c6d5c544b70` — chờ kiểm toán độc lập đợt 2 cho gói Remediation & G2 này)

---

## 1. Mục tiêu & Phạm vi Hoàn tất
Hoàn tất toàn bộ **Execution Contract: Post-Audit Remediation, Comprehensive Compensation Benchmarking & Business Strategy** bám sát nguyên văn yêu cầu gốc của chị Nhi (`SRC-REQ-001`) tại `ANCHOR_SPEC.md`:
1. Khắc phục trọn vẹn **10 nhóm phát hiện của Independent Auditor (Codex)** + dọn sạch **Documentation Drift** trên toàn repo.
2. Chuẩn hóa 100% 3 bảng lookup lớn (`1,300` dòng AIA PAF+, `113` dòng Hoa hồng Chubb, `10` khung tuổi HSBH), bản đồ **36 chức danh** và **44 cấu phần Total Rewards** (33 metadata, tách bạch tiền mặt vs phi tiền mặt chưa định giá).
3. Hoàn thiện **12 Phương pháp Benchmarking**, **Khung Đánh giá & Rubric 15 tiêu chí** (tách Cổng Pháp lý bắt buộc + 6 Calibration Cases + Weight Sensitivity — `DRAFT`), **Phân tích Thị trường VN 2024–2027**, và **Đề xuất Chính sách `W24 Balanced Hybrid`** (+ 2 biến thể) cùng phân tích Break-Even Margin.
4. Xây dựng **Python 12M Compensation & Enterprise Distribution Cost Engine** (`40/40` Golden Tests `PASS`) và **Excel Reference Model 14 sheet tương thích Excel 2007** — **đã chạy tính toán lại thực tế qua Microsoft Excel 12.0 COM** (`0` lỗi công thức, `20/20` Live Excel Golden Tests `PASS`, `12/12` Enterprise Cost Parity khớp `0.00%` với Python!).
5. Bàn giao sạch **Gói A (`outputs/interview/W24_Executive_Recommendation_Step1.md` — 7 trang)** tách biệt hoàn toàn khỏi Gói B Working Papers.

---

## 2. Danh mục Sản phẩm Đã Tạo Mới & Cập Nhật (Checkpoint này)
- **Normalized Lookups & Data Inventories:**
  - `knowledge/lookups/aia-paf-5y-targets.csv` (1,300 dòng, 0 sai lệch tổng)
  - `knowledge/lookups/chubb-product-commission-schedule.csv` (113 dòng sản phẩm/phí trội/rider/nhóm)
  - `knowledge/lookups/chubb-hsbh-tiers.csv` (10 khung tuổi HSBH *Tự Do An Phúc*)
  - `knowledge/policies/role-organization-mapping.csv` (36 chức danh × 16 cột) & `.md`
  - `knowledge/compensation/total-rewards-inventory.csv` (44 cấu phần × 33 cột) & `.md`
  - `knowledge/sources/source-registry.csv` (16 nguồn × 17 cột, thêm `Revision_Class`, cập nhật Đ.51/52 `SOURCE_NOT_VERIFIED`)
  - `knowledge/business-rules/business-rules-catalog.csv` (112 quy tắc × 25 cột, 3 cột trạng thái chuẩn Section 32, 0 tham chiếu gãy)
- **Benchmarking, Rubric, Market & Strategy:**
  - `outputs/working/competitor-benchmarking-12-methods.md` (v2.0 — 12 phương pháp + Ma trận Quyền lợi & Kịch bản)
  - `docs/specifications/evaluation-framework-and-rubric.md` (15 tiêu chí + Mandatory Gate + 6 Calibration + Weight Sensitivity — `DRAFT`)
  - `docs/research/vietnam-market-suitability.md` (IAV/MOF 2024–2026 + khung pháp lý 2026–2027)
  - `outputs/working/strategic-recommendations-and-schemes.md` (`ADOPT/ADAPT/AVOID` + `W24 Balanced Hybrid` + Break-Even Sensitivity)
- **Engines, Excel Model & Independent-Style Verification:**
  - `model/compensation/compensation_engine.py` (12M calendar, dual-phase switches, conflict toggles, Enterprise Cost, MAPA, Break-Even)
  - `tests/test_compensation_golden.py` (`40/40 PASSED` bao phủ 23 nhóm biên Section 33)
  - `outputs/working/W24_Compensation_Reference_Model_v1.xlsx` (14 sheets, Excel 12.0 COM recalculated & saved!)
- **Executive Delivery (Package A) & Governance/QA:**
  - `outputs/interview/W24_Executive_Recommendation_Step1.md` (**Gói A — 7 trang sạch trình chị Nhi**)
  - `qa/post-audit-remediation-register.md` (Theo dõi cả 10 phát hiện Codex — `SELF_VERIFIED` / `OPEN`)
  - `qa/repository-maturity-assessment.md` (12+1 tiêu chuẩn trưởng thành)
  - `docs/decisions/decision-register.md` (7 quyết định mở `DEC-01..DEC-07`)
  - `docs/research/knowledge-backlog.md` (Khoảng trống nguồn & lộ trình P1/P2)
- **Documentation Drift Fixed:** `docs/research/wheel-check.md`, `docs/architecture/reusable-model-schema.md`, `knowledge/policies/aia-alpha-2026-deep-guide.md`, `knowledge/policies/chubb-life-agency-2026-deep-guide.md`, `qa/g1-coverage-audit-matrix.md`, `qa/g1-extraction-qa-audit.md` (banner lịch sử), `outputs/working/competitor-comparison-v1.0.md` (banner lịch sử), `ANCHOR_SPEC.md`, `HANDOVER.md`, `CHANGELOG.md`.

---

## 3. Bằng chứng Kiểm thử & Kiểm chứng (`SELF_VERIFIED` — CHƯA PHẢI `INDEPENDENTLY_VERIFIED`)
- **7 PDF bất biến trong `private/sources/`:** Xác minh `SHA-256` khớp 100% với `source-registry.csv` và thư mục Downloads (`ALL_7_PDFS_MATCH=True`). Không sửa bất kỳ file gốc nào.
- **Python Golden Test Suite:** `40/40 PASSED` (kỳ vọng tính độc lập bằng tay từ văn bản gốc).
- **Microsoft Excel 12.0 COM Recalculation (`CalculateFullRebuild`):**
  - `EXCEL_COM_VERSION = 12.0` | `EXCEL_RECALC_SAVE_OK = True`
  - Quét toàn bộ 14 sheet (`data_only=True`): **`0` ô lỗi công thức** (`#REF!`, `#NAME?`, `#VALUE!`, `#DIV/0!`, `#N/A`, `#NUM!`).
  - Sheet `14_QA_Golden_Tests`: **`20/20 PASS` (`0` Failures)**.
  - Sheet `11_Hierarchy_Dist_Cost`: **`12/12 PASS`** — khớp **`0.00%`** với Python trên mọi kịch bản K2 (`82%/72%/62%`) và mọi chính sách!
- **Phân bố Trạng thái trên 112 Rules (`business-rules-catalog.csv`):**
  - `Source_Verification`: `57 SOURCE_VERIFIED`, `46 MISSING_DEPENDENCY`, `7 SOURCE_NOT_VERIFIED`, `2 CONFLICTING_EVIDENCE`
  - `Implementation_Status`: `72 IMPLEMENTED`, `40 NOT_IMPLEMENTED`
  - `Calculation_Verification`: `37 TESTED_PASS (SELF)`, `35 CONDITIONAL`, `24 NOT_TESTED`, `16 BLOCKED`

---

## 4. Điểm Chưa Kiểm chứng / Hạn chế Trung thực
1. **Chưa có Independent Audit đợt 2:** Toàn bộ kết quả kiểm thử trên là `SELF_VERIFIED` do AGY tự thực hiện; cần Codex rà soát độc lập để cấp nhãn `INDEPENDENTLY_VERIFIED`.
2. **Rubric 15 tiêu chí còn ở trạng thái `DRAFT — NOT INDEPENDENTLY CALIBRATED`.**
3. **7 quy tắc pháp lý (`REG-*`) ở trạng thái `SOURCE_NOT_VERIFIED`** do chưa tải bản PDF toàn văn Công báo chính thức (`DEC-03`).
4. **2 xung đột nội tại nguồn gốc (`ERR-DOC-01` Chubb W1 `80% vs 50%`; `ERR-DOC-02` AIA làm tròn `RoundUp vs HalfUp`)** vẫn ở trạng thái `OPEN` (đã có toggle 2 chiều trên Excel & Python, không tự phán xử).
5. **Thiếu tài liệu đối thủ & nội bộ:** Manulife FA/UM/DM (`UNKNOWN`), AIA Exchange/Pro & Phụ lục HH, Chubb `260005V`/BD, và `VNB Margin` / `Home Office OpEx` thật của doanh nghiệp đích.

---

## 5. Trạng thái Git & Quyết định Cần TJ
- **Repository GitHub:** `https://github.com/teoteo1081/W24_Life-Insurance-Strategy-Lab` — Đã xác minh **`PRIVATE`** (`gh repo view`).
- **Baseline đã đồng bộ trên `origin/main`:** `5c2d13bbe060bee03e9dc4a9391b2df8c2e84cf9` (chứa 7 PDF nguồn `private/sources/` đã được TJ duyệt trước đó).
- **Trạng thái Local Commit mới:** AGY chỉ tạo **LOCAL commit trên nhánh `main`**, **TUYỆT ĐỐI KHÔNG tự ý push lên GitHub** theo đúng lệnh quản trị (`DEC-07`).
- **7 Quyết định Mở đang chờ TJ tại `docs/decisions/decision-register.md`:** `DEC-01` (`ERR-DOC-01`), `DEC-02` (`ERR-DOC-02`), `DEC-03` (Công báo pháp lý), `DEC-04` (Bổ sung PDF thiếu), `DEC-05` (Trọng số & Biến thể Đề xuất), `DEC-06` (Tham số VNB/OpEx nội bộ), và **`DEC-07` (Phê duyệt push local commit lên GitHub PRIVATE hoặc chạy Codex Independent Audit đợt 2 trước)**.
