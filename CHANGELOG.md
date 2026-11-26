# CHANGELOG.md

Tất cả thay đổi quan trọng của dự án `W24_Life-Insurance-Strategy-Lab` được ghi nhận tại đây.

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
