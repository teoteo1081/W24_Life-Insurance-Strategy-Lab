# EXECUTION_PLAN.md — Kế hoạch Thực thi 3 Ngày

**Mục tiêu tối thượng:** Hoàn thành trọn vẹn **P0** trong 3 ngày với bằng chứng kiểm chứng được, đồng thời xây nền tảng repo bền vững cho tương lai.

---

## Ngày 1 — Nền móng, Pháp lý & Nghiên cứu Đối thủ

- [x] Kiểm tra workspace & khởi tạo Git repository local an toàn (`main`).
- [x] Tạo nền móng repository tối thiểu (`.gitignore`, `README.md`, `AGENTS.md`, `ANCHOR_SPEC.md`, `EXECUTION_PLAN.md`, `CHANGELOG.md`).
- [x] Domain Discovery: xác định bài toán, phân loại dữ kiện, lập danh sách câu hỏi & tài liệu còn thiếu (`docs/discovery/domain-discovery.md`).
- [x] Wheel Check giới hạn thời gian cho 5 nhóm A–E, đặc biệt cập nhật khung pháp lý VN 2023–2026 (`docs/research/wheel-check.md`).
- [x] Thiết lập sổ kiểm kê nguồn (`knowledge/sources/source-registry.csv`), từ điển thuật ngữ (`knowledge/glossary/glossary.md`) và danh mục quy tắc nghiệp vụ (`knowledge/business-rules/business-rules-catalog.csv`).
- [x] Tạo bảng so sánh đối thủ v0.1 (`outputs/working/competitor-comparison-v0.1.md`) phân rõ nguồn công khai vs. phần thiếu tài liệu gốc.
- [ ] **Đang chờ từ TJ:** Đề bài gốc của chị Nhi + tài liệu policy (PDF/Excel/ảnh) của AIA, Manulife, Chubb Life, Kênh Alpha (nếu có).
- [ ] Ngay khi nhận tài liệu: Trích xuất Business Rules có số trang nguồn → nâng cấp bảng so sánh lên v1.0.

## Ngày 2 — Mô hình Excel MVP, Thiết kế Scheme & MAPA

- [ ] Xây Excel Reference Model (`model/compensation/` & `outputs/working/`) tách rõ Inputs / Formulas / Outputs.
- [ ] Mô phỏng 7 nhóm đại lý chuẩn (Mới, Năng suất thấp/TB/cao, Quản lý, Đội ngũ mới thu hút, Đội ngũ ổn định).
- [ ] Thiết kế 3 phương án Compensation Scheme (A: Growth, B: Quality, C: Balanced/Hybrid) và phân tích rủi ro gian lận / tuân thủ pháp lý (TT 67/2023 & TT 96/2026).
- [ ] Tích hợp MAPA tính xuôi & tính ngược + phân tích độ nhạy chi phí / điểm hòa vốn / ROI.
- [ ] Viết Golden Test Cases kiểm thử công thức độc lập (`tests/`).
- [ ] *(P1 nếu dư thời gian)* Bổ sung khung tuyển dụng sales & marketing tìm kiếm khách hàng; HTML MVP.

## Ngày 3 — Audit, Đối soát & Đóng gói Bàn giao

- [ ] Risk-Adaptive Audit (L1 Logic, L2 Evidence đối chiếu tài liệu gốc, L3 Reproducibility, L4 Adversarial test các trường hợp lợi dụng chính sách).
- [ ] Hoàn thiện Gói A — Executive Presentation 5–7 trang/slide (`outputs/interview/`).
- [ ] Tách bạch Gói A (Interview Delivery) và Gói B (Working Papers).
- [ ] Cập nhật `HANDOVER.md`, `CHANGELOG.md`, lập Knowledge Backlog & Roadmap sau deadline.
- [ ] Khóa checkpoint Git local sạch sẽ.
