# W24 — Life Insurance Strategy Lab

**Agency Business Planning & Strategy Decision Support System**

Dự án tư vấn chiến lược thu nhập đại lý bảo hiểm nhân thọ tại thị trường Việt Nam, đồng thời xây dựng nền tảng phương pháp luận, mô hình tài chính và kho tri thức tái sử dụng lâu dài.

- **Business Owner:** TJ
- **Primary Execution Agent:** AGY (Google Antigravity)
- **Trạng thái hiện tại:** Ngày 1 — Khởi tạo nền móng Level 1, Domain Discovery, Wheel Check và Khung so sánh đối thủ v0.1 (đang chờ tài liệu policy gốc & đề bài gốc).

---

## 1. Hai mục tiêu song song

1. **Mục tiêu ngắn hạn (3 ngày — P0):** Hoàn thành bài tư vấn chiến lược chính sách thu nhập đại lý bảo hiểm nhân thọ (so sánh AIA, Manulife, Chubb Life, kênh Alpha; đề xuất compensation scheme thúc đẩy doanh số, chất lượng kinh doanh, hiệu quả chi phí & ROI; mô hình Excel kiểm chứng được; bài trình bày lãnh đạo 5–7 trang/slide).
2. **Mục tiêu dài hạn (MVP → DSS):** Phát triển hệ thống hỗ trợ ra quyết định chiến lược kinh doanh đại lý (MAPA xuôi/ngược, mô phỏng tuyển dụng & marketing, phân tích kịch bản, HTML simulator, quản trị bằng chứng & kiểm toán).

---

## 2. Cấu trúc Repository hiện tại

```text
W24_Life-Insurance-Strategy-Lab/
├── README.md                                   # Tài liệu giới thiệu & hướng dẫn sử dụng
├── AGENTS.md                                   # Quy tắc làm việc cho AI agent
├── ANCHOR_SPEC.md                              # Mục tiêu, phạm vi P0/P1/P2 và nguyên tắc bất biến
├── EXECUTION_PLAN.md                           # Lộ trình thực thi 3 ngày
├── HANDOVER.md                                 # Điểm bàn giao & checkpoint hiện tại
├── CHANGELOG.md                                # Lịch sử thay đổi
├── .gitignore                                  # Bảo vệ dữ liệu nhạy cảm & file tạm
├── docs/
│   ├── discovery/domain-discovery.md           # Khám phá nghiệp vụ, dữ kiện & câu hỏi trọng yếu
│   └── research/wheel-check.md                 # Nghiên cứu giải pháp sẵn có & khung pháp lý VN
├── knowledge/
│   ├── glossary/glossary.md                    # Từ điển thuật ngữ chuẩn (APE/FYP/FYC/MAPA...)
│   ├── sources/source-registry.csv             # Sổ kiểm kê nguồn Ground Truth
│   └── business-rules/business-rules-catalog.csv # Danh mục quy tắc nghiệp vụ có nguồn
└── outputs/
    └── working/competitor-comparison-v0.1.md   # Bảng so sánh đối thủ bản v0.1 (working)
```

*(Các thư mục `model/`, `tests/`, `qa/`, `outputs/interview/`, `apps/simulator/`, `private/` sẽ chỉ được tạo khi có tài liệu/code thực tế phát sinh.)*

---

## 3. Phân gói sản phẩm & Bảo mật

- **Gói A (`outputs/interview/`):** Tài liệu trình bày cho chị Nhi (5–7 trang/slide, gọn gàng, bảo vệ được bằng bằng chứng, không chứa dữ liệu nhạy cảm hay toàn bộ working papers).
- **Gói B (Toàn bộ repo working papers):** Nghiên cứu chi tiết, business rules, mô hình Excel, kiểm thử, audit, kiến trúc.
- **Thư mục `private/` (được gitignore):** Lưu tài liệu nội bộ/hạn chế chia sẻ (PDF policy gốc, đề bài gốc nếu chứa thông tin nhạy cảm). Không bao giờ commit hay push ra ngoài.

---

## 4. Cách bắt đầu tiếp quản

1. Đọc [HANDOVER.md](HANDOVER.md) để nắm trạng thái mới nhất, blocker và hành động tiếp theo.
2. Đọc [ANCHOR_SPEC.md](ANCHOR_SPEC.md) để nắm rõ ranh giới P0/P1/P2 và chuẩn bằng chứng.
3. Đọc [EXECUTION_PLAN.md](EXECUTION_PLAN.md) để bám sát tiến độ 3 ngày.
