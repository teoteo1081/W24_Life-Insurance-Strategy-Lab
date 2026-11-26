# CHANGELOG.md

Tất cả thay đổi quan trọng của dự án `W24_Life-Insurance-Strategy-Lab` được ghi nhận tại đây.

## [0.4.0] - 2026-11-26 (Post-Audit Remediation, 12-Method Benchmarking, Excel 12.0 COM Verified Model & Package A)

### Added
- **Normalized Lookup Tables (`knowledge/lookups/`):** `aia-paf-5y-targets.csv` (1,300 dòng, 0 sai lệch tổng), `chubb-product-commission-schedule.csv` (113 dòng), `chubb-hsbh-tiers.csv` (10 khung tuổi HSBH).
- **Complete Role Mapping & Total Rewards Inventory:** `knowledge/policies/role-organization-mapping.{csv,md}` (36 chức danh × 16 cột) và `knowledge/compensation/total-rewards-inventory.{csv,md}` (44 cấu phần × 33 metadata chuẩn Section 14, tách bạch tiền mặt vs phúc lợi phi tiền mặt chưa định giá).
- **Comprehensive Benchmarking & Evaluation Rubric:** `outputs/working/competitor-benchmarking-12-methods.md` (12 phương pháp Benchmarking + Entitlement & Scenario Payout Matrix) và `docs/specifications/evaluation-framework-and-rubric.md` (Mandatory Regulatory Gate G1–G3 + 15 tiêu chí + 6 Calibration Cases + 4 Weight Sensitivity Scenarios — `DRAFT`).
- **Market Suitability & Strategic Proposals:** `docs/research/vietnam-market-suitability.md` (IAV/MOF 2024–2026) và `outputs/working/strategic-recommendations-and-schemes.md` (`ADOPT/ADAPT/AVOID`, kiến trúc `W24 Balanced Hybrid` + 2 biến thể, Break-Even Margin Sensitivity).
- **12M Python Engine, Golden Tests & Excel 2007 Reference Model:** `model/compensation/compensation_engine.py`, `tests/test_compensation_golden.py` (`40/40 PASSED`), và `outputs/working/W24_Compensation_Reference_Model_v1.xlsx` (14 sheets, tính toán thực tế qua Microsoft Excel 12.0 COM: `0` lỗi công thức, `20/20` Live Excel Golden Tests `PASS`, `12/12` Enterprise Cost Parity khớp `0.00%` với Python).
- **Executive Delivery (Package A) & Governance Registers:** `outputs/interview/W24_Executive_Recommendation_Step1.md` (7 trang sạch), `qa/post-audit-remediation-register.md`, `qa/repository-maturity-assessment.md` (12+1 tiêu chuẩn), `docs/decisions/decision-register.md` (`DEC-01..07`), `docs/research/knowledge-backlog.md`.

### Changed
- Khắc phục toàn bộ 10 phát hiện sau Independent Audit của Codex (`7bcf70e`): bổ sung Điều 52 TT 67/2023 (trần thưởng 20%/30%/7%) & NĐ 97/2026 vào `wheel-check.md` và `business-rules-catalog.csv` (112 rules × 25 cột, tách 3 cột trạng thái Section 32, 0 tham chiếu gãy), thêm `Revision_Class` vào `source-registry.csv`, bổ sung ngoại lệ ACK T01/2026 (`28/02/2026`), tách biệt luật 70% cap CQL vs PAF+, lập trình công thức bù trừ Champion Hubb M7–M12 p.10, chấm dứt tự phán xử `ERR-DOC-01/02` (mở toggle + leo thang Decision Register), và dọn sạch documentation drift trên `reusable-model-schema.md`, `g1-coverage-audit-matrix.md`, `g1-extraction-qa-audit.md`, `competitor-comparison-v1.0.md`, `ANCHOR_SPEC.md`, `HANDOVER.md`.
- Chỉ tạo **local Git commit** trên nhánh `main` — chưa push lên `origin/main` (chờ phê duyệt của TJ tại `DEC-07`).

## [0.3.1] - 2026-11-26 (GitHub Private Sync)

### Changed
- Theo xác nhận tường minh của Business Owner (TJ): cập nhật `.gitignore` cho phép theo dõi riêng `private/sources/` (7 file PDF policy gốc) trong **PRIVATE** GitHub repository `teoteo1081/W24_Life-Insurance-Strategy-Lab`, vẫn chặn mọi file khác trong `private/` và credentials/secrets.
- Khởi tạo remote `origin` (PRIVATE) và đồng bộ toàn bộ nhánh `main` lên GitHub.

## [0.3.0] - 2026-11-26 (Checkpoint G1 Deep Policy Understanding & Coverage Audit)

### Added
- Policy Knowledge Base đầy đủ cho 3 công ty (`knowledge/policies/aia-alpha-2026-deep-guide.md`, `chubb-life-agency-2026-deep-guide.md`, `manulife-psm-hkd-2026-deep-guide.md`) kèm sơ đồ cấp bậc Mermaid và ví dụ tính toán thực tế.
- Cross-document Mapping (`knowledge/policies/cross-document-mapping.md`) truy vết trọn vẹn 25 mục tham chiếu chéo giữa các memo.
- Coverage Audit Matrix (`qa/g1-coverage-audit-matrix.md`) kiểm toán toàn văn 116/116 trang theo 6 trạng thái & 5 cấp độ trưởng thành hiểu biết.
- Phân tích chiến lược 12 khía cạnh từng công ty (`docs/research/competitor-strategy-analysis.md`), tách rõ chiến lược xác nhận trong văn bản vs. suy luận từ thiết kế.
- Đặc tả yêu cầu mô hình xuất phát từ thực tế memo (`docs/architecture/bottom-up-model-requirements.md`: 10 entities, tham số dùng chung vs. đặc thù, 14 năng lực Rule Engine).

### Changed
- Mở rộng `knowledge/business-rules/business-rules-catalog.csv` từ 53 lên **108 Atomic Business Rules** (`105 VERIFIED_FACT` + `3 SOURCE_CLAIM`).
- Mở rộng `knowledge/glossary/glossary.md` với toàn bộ thuật ngữ thực tế từ 7 memo và cảnh báo trùng mã viết tắt khác nghĩa giữa các công ty.
- Sửa chính xác SHA-256 của file nén trùng lặp `.7z` trong `knowledge/sources/source-registry.csv` sau khi kiểm kê lại thư mục nguồn & attachments.
- Cập nhật `ANCHOR_SPEC.md` (`REQ-01` -> `DONE_G1_DEEP`) và `HANDOVER.md`.

## [0.2.0] - 2026-11-26 (Checkpoint G1)

### Added
- Tiếp nhận, kiểm kê (CRC32 phát hiện `.7z` trùng lặp 100%) và tổ chức 7 tài liệu PDF chính sách gốc vào `private/sources/{AIA-Alpha,Manulife,Chubb-Life}/` (đã xác minh SHA-256 và chặn tuyệt đối khỏi Git qua `.gitignore`).
- Đọc trọn vẹn 116/116 trang (bao gồm đọc trực quan 15/15 trang scan PDF Chubb Life `CHH0DCEB260003V`) và trích xuất 50 quy tắc nghiệp vụ `VERIFIED_FACT` (+ 3 trần pháp lý `SOURCE_CLAIM`) vào `knowledge/business-rules/business-rules-catalog.csv`.
- Xây dựng Competitor Comparison Matrix v1.0 (`outputs/working/competitor-comparison-v1.0.md`) so sánh chuẩn hóa theo 3 tầng bậc (Đại lý, Quản lý trực tiếp, Quản lý cấp cao) bám sát 3 mục tiêu của chị Nhi.
- Thiết kế Schema cấu hình tái sử dụng (`schemas/compensation-scheme.schema.json` & `docs/architecture/reusable-model-schema.md`) cho Excel, MAPA, Marketing, Financial Model và HTML Simulator.
- Hoàn tất báo cáo kiểm soát chất lượng & kiểm toán G1 (`qa/g1-extraction-qa-audit.md`) phát hiện 4 nhóm lỗi/bất nhất trong tài liệu gốc và phân tích rủi ro trục lợi L4.

### Changed
- Nâng cấp `knowledge/sources/source-registry.csv` đủ 16 cột quản trị nguồn và cập nhật `ANCHOR_SPEC.md` (`REQ-01` -> `DONE_G1`) cùng `HANDOVER.md`.

## [0.1.1] - 2026-11-26

### Changed
- Lưu nguyên văn Yêu cầu Gốc Bước 1 của chị Nhi (`SRC-REQ-001`, `VERIFIED FACT`) vào `ANCHOR_SPEC.md` làm Primary Business Anchor có mức ưu tiên cao nhất.
- Phân tách rõ phạm vi Yêu cầu Gốc (P0) vs. Tầm nhìn Mở rộng của TJ (P1/P2: MAPA xuôi/ngược, Marketing tuyển Sales, Marketing tìm kiếm khách hàng, PO điều chỉnh tham số, HTML Simulator).
- Bổ sung Requirement Traceability Matrix (`REQ-01` → `REQ-05`) trong `ANCHOR_SPEC.md` để truy vết từ yêu cầu gốc đến nghiên cứu, mô hình, bằng chứng và khuyến nghị Gói A.
- Cập nhật trạng thái `SRC-REQ-001` sang `VERIFIED_FACT` trong `knowledge/sources/source-registry.csv`, `docs/discovery/domain-discovery.md` và `HANDOVER.md`.

## [0.1.0] - 2026-11-26

### Added
- Khởi tạo Git repository local (nhánh `main`) và nền móng tối thiểu: `.gitignore`, `README.md`, `AGENTS.md`, `ANCHOR_SPEC.md`, `EXECUTION_PLAN.md`, `HANDOVER.md`.
- Tài liệu `docs/discovery/domain-discovery.md` xác định bài toán, phân loại dữ kiện và danh mục tài liệu còn thiếu.
- Tài liệu `docs/research/wheel-check.md` tổng hợp giải pháp sẵn có (Nhóm A–E) và cập nhật khung pháp lý Việt Nam (Luật 08/2022/QH15, NĐ 46/2023 & NĐ 97/2026, TT 67/2023 & TT 96/2026).
- Bộ tri thức chuẩn hóa ban đầu: `knowledge/glossary/glossary.md`, `knowledge/sources/source-registry.csv`, `knowledge/business-rules/business-rules-catalog.csv`.
- Sản phẩm so sánh đối thủ đầu tiên `outputs/working/competitor-comparison-v0.1.md` (ghi rõ dữ kiện công khai, khoảng trống tài liệu gốc và khung so sánh 12 tiêu chí).
