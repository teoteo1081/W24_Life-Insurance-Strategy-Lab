# EXECUTION_PLAN.md — Kế hoạch Thực thi & Theo dõi Tiến độ

> **Single Source of Truth Note:** File này theo dõi các mốc kế hoạch dự án (3 ngày P0 + Sprint củng cố Level 2). Trạng thái vận hành mới nhất, kết quả kiểm thử hiện hành và hành động tiếp theo luôn xem tại [HANDOVER.md](HANDOVER.md).

---

## Giai đoạn 1 — Nền móng, Pháp lý & Hiểu sâu Chính sách (G0 → G1 Deep)

- [x] Khởi tạo Git repository local an toàn (`main`) và cấu trúc nền móng (`ANCHOR_SPEC.md`, `AGENTS.md`, `HANDOVER.md`, `CHANGELOG.md`).
- [x] Tiếp nhận nguyên văn Yêu cầu Gốc Bước 1 của chị Nhi (`SRC-REQ-001`) lưu tại `ANCHOR_SPEC.md`.
- [x] Tiếp nhận, kiểm kê Hash SHA-256 và đọc trọn vẹn **7 PDF chính sách (116/116 trang)**: AIA Alpha (3), Manulife PSM+/HKD (1), Chubb Life Agency (3).
- [x] Xây dựng Policy Knowledge Base (3 Deep Guides + Cross-Document Mapping 25 tham chiếu + Coverage Audit Matrix 116p + 12-dimension Strategy Analysis + Bottom-up Model Spec) — Checkpoint `7bcf70e` (Codex Independent Audit lần 1).

## Giai đoạn 2 — Post-Audit Remediation, Benchmarking 12 Phương pháp, Excel Model & Gói A (`852ca87`)

- [x] Khắc phục 10 phát hiện từ Independent Audit lần 1 (`qa/post-audit-remediation-register.md`): mở rộng catalog lên 112 quy tắc (3 cột trạng thái chuẩn Section 32), bổ sung Điều 52 TT 67/2023 & NĐ 97/2026 (`SOURCE_NOT_VERIFIED`), sửa tham chiếu `Rule_ID`, dừng tự phán xử `ERR-DOC-01/02`.
- [x] Chuẩn hóa 100% 3 bảng lookup lớn (`aia-paf-5y-targets.csv` 1,300 dòng; `chubb-product-commission-schedule.csv` 113 dòng; `chubb-hsbh-tiers.csv` 10 dòng), bản đồ 36 chức danh và 44 cấu phần Total Rewards.
- [x] Hoàn thiện Benchmarking 12 phương pháp (`outputs/working/competitor-benchmarking-12-methods.md`), Khung đánh giá 15 tiêu chí (`DRAFT`), Phân tích thị trường VN 2024–2027, và Kiến trúc đề xuất `W24 Balanced Hybrid` (`PROPOSAL`).
- [x] Xây dựng Python 12M Engine (`model/compensation/compensation_engine.py`), Excel Reference Model 14 sheets (`outputs/working/W24_Compensation_Reference_Model_v1.xlsx`) và Gói A 7 trang (`outputs/interview/W24_Executive_Recommendation_Step1.md`).

## Giai đoạn 3 — Post-Independent-Audit Hardening & Level 2 Maturity Sprint (Sau Codex Audit `5cb7a21`)

- [x] **P0 Confidentiality & Document Rights Review:** Quét bảo mật toàn repo/lịch sử Git (lưu báo cáo chi tiết ngoài repo PUBLIC), bổ sung cột `Redistribution_Rights_Status` vào `source-registry.csv`, ban hành `docs/governance/confidentiality-and-rights-policy.md`, xóa sạch 10 liên kết đường dẫn cục bộ không khả chuyển (`file://` ổ đĩa máy cá nhân).
- [x] **P0 Business, ROI & Legal Precision:** Cập nhật metadata chính thức `44/2026/VBHN-TT-BTC` & `TT 96/2026` (`02/07/2026`), tách bạch tuyệt đối `Modeled Break-Even` với `Actual ROI (UNKNOWN)`, đưa cổng pháp lý về `CONDITIONAL` cho đến khi đối chiếu toàn văn (`DEC-03`).
- [x] **P0/P1 Test Discovery, NaN Safety & Input Validation:** Chuẩn hóa `unittest discover`, sửa `assert_close` chặn `NaN/±Inf/bool`, bổ sung validation đầu vào & phân biệt âm hợp lệ (clawback) vs âm lỗi + không chuyển ngầm `UNKNOWN` thành `1.0`, bổ sung regression tests & độc lập hóa `GT-16`.
- [x] **P1 Reproducible Workbook, Quality Gates, Docs & Clean-Clone Proof:** Đưa `scripts/build_workbook.py`, `scripts/verify_workbook_excel.py`, `scripts/validate_repo.py`, `scripts/run_checks.py` và `requirements.txt` vào repo; chạy Excel COM recalculation + live input perturbation; chạy kiểm chứng trên bản `git clone` sạch; lập `docs/architecture/level3-level4-architecture-advisory.md` và cập nhật Single Source of Truth (`README.md`, `HANDOVER.md`, `AGENTS.md`).

## Giai đoạn Mở rộng Sau Checkpoint (P2 — Chưa triển khai trong Sprint Level 2)

- [ ] **Independent Audit Đợt 3 (Codex):** Xác nhận độc lập các năng lực Level 2 và rà soát `DEC-01..08`.
- [ ] **Level 3 Vertical Slice:** Cấu hình hóa 1 nhóm thưởng bằng JSON có `effective_date` chạy trực tiếp qua operator chuẩn không sửa công thức.
- [ ] **Level 4/P3 (Khi TJ duyệt):** Company Adapters + Cross-engine Golden Vectors + HTML Interactive Simulator + Phễu Marketing Tuyển Sales & Khách hàng + Nạp VNB/OpEx thực tế.
