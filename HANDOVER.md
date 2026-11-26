# HANDOVER.md — Điểm Bàn giao & Checkpoint Dự án

**Cập nhật lần cuối:** 2026-11-26 (Checkpoint 1 — Ngày 1)  
**Người thực hiện:** AGY  
**Business Owner:** TJ  

---

## 1. Mục tiêu hiện tại
Hoàn thành nền móng Ngày 1 (repo Level 1, Domain Discovery, Wheel Check, khung pháp lý VN, cấu trúc Ground Truth & bảng so sánh đối thủ v0.1) để sẵn sàng nạp tài liệu policy gốc và chuyển sang xây Excel Reference Model + Thiết kế Scheme + MAPA ở Ngày 2.

## 2. Công việc đã hoàn thành
- Kiểm tra workspace sạch (không có repo cha, không tạo repo lồng) và khởi tạo Git local (`main`).
- Kiểm tra môi trường máy cục bộ: Python 3.12.10 đã có sẵn `openpyxl 3.1.5`, `pymupdf`, `pdfplumber` (đủ để đọc PDF policy và sinh Excel Reference Model có công thức thật mà không cần cài thêm công cụ).
- Tạo nền móng repository tối thiểu: `.gitignore`, `README.md`, `AGENTS.md`, `ANCHOR_SPEC.md`, `EXECUTION_PLAN.md`, `CHANGELOG.md`.
- Hoàn thành Domain Discovery (`docs/discovery/domain-discovery.md`) với bảng phân loại bằng chứng và 5 câu hỏi xếp theo mức độ ảnh hưởng cho TJ.
- Hoàn thành Wheel Check giới hạn thời gian cho 5 nhóm A–E (`docs/research/wheel-check.md`), đặc biệt cập nhật khung pháp lý VN: Luật KDBH 08/2022/QH15, NĐ 46/2023 & NĐ 97/2026, TT 67/2023 & **TT 96/2026/TT-BTC** (áp dụng trần hoa hồng mới và siết hoa hồng phí đóng thêm từ 01/01/2027).
- Tạo bộ tri thức chuẩn hóa: `knowledge/glossary/glossary.md`, `knowledge/sources/source-registry.csv`, `knowledge/business-rules/business-rules-catalog.csv`.
- Tạo sản phẩm so sánh đối thủ đầu tiên: `outputs/working/competitor-comparison-v0.1.md` (khung 12 tiêu chí, phân rõ `SOURCE CLAIM` vs. `UNKNOWN`, có minh họa cấu trúc tính toán `[SYNTHETIC_EXAMPLE]`).

## 3. File đã tạo hoặc sửa
- `.gitignore`
- `README.md`
- `AGENTS.md`
- `ANCHOR_SPEC.md`
- `EXECUTION_PLAN.md`
- `CHANGELOG.md`
- `HANDOVER.md`
- `docs/discovery/domain-discovery.md`
- `docs/research/wheel-check.md`
- `knowledge/glossary/glossary.md`
- `knowledge/sources/source-registry.csv`
- `knowledge/business-rules/business-rules-catalog.csv`
- `outputs/working/competitor-comparison-v0.1.md`

## 4. Bằng chứng
- Môi trường cục bộ: đã chạy lệnh kiểm tra `git`, `python 3.12.10`, `openpyxl 3.1.5`, `pymupdf`, `pdfplumber`.
- Nguồn công khai: tổng hợp khung pháp lý từ `chinhphu.vn`, `thuvienphapluat.vn`, `luatvietnam.vn`, `thoibaotaichinhvietnam.vn` và thông tin tổng quan AIA/Alpha/Manulife/Chubb Life từ báo chí công khai (`laodong.vn`, `vneconomy.vn`, `cafef.vn`, `dantri.com.vn`, `tinnhanhchungkhoan.vn`). Toàn bộ đều gắn nhãn `SOURCE_CLAIM`.

## 5. Kết quả kiểm thử thực tế
- `NOT RUN` — Chưa xây dựng công thức Excel/Python tính toán (sẽ thực hiện và viết Golden Test Cases ở Ngày 2).

## 6. Kết quả kiểm toán
- `INSPECTED` (tự kiểm tra nội bộ cấu trúc repo & nhãn bằng chứng — **không** tuyên bố audit độc lập).
- `NOT RUN` cho L2 Evidence đối chiếu PDF gốc (vì chưa có PDF gốc) và L3 Reproducibility.

## 7. Những việc chưa kiểm chứng
- Toàn văn chính thức của Thông tư 96/2026/TT-BTC và Thông tư 67/2023/TT-BTC (hiện mới ở mức tóm tắt từ nguồn pháp lý công khai).
- Chính sách thu nhập nội bộ (biểu FYC thực tế, bậc thưởng quý/năm, trợ cấp, override, persistency gate, clawback) của AIA, Kênh Alpha, Manulife, Chubb Life.
- Đề bài gốc chính xác của chị Nhi.

## 8. Blocker
- **BLOCKER P0 (Thiếu dữ liệu đầu vào gốc):** Workspace hiện chưa có:
  1. Đề bài gốc của chị Nhi (`SRC-REQ-001`).
  2. Tài liệu policy gốc (PDF/Excel/ảnh) của AIA, Kênh Alpha, Manulife, Chubb Life (`SRC-POL-AIA-001`, `SRC-POL-ALP-001`, `SRC-POL-MNL-001`, `SRC-POL-CHB-001`).
- *Lưu ý:* Dự án **không bị dừng** vì blocker này — AGY vẫn có thể chuyển sang xây Excel Reference Model tham số hóa + 3 hướng Compensation Scheme + MAPA xuôi/ngược trên dữ liệu giả lập có nhãn rõ ràng nếu TJ chưa kịp cung cấp tài liệu.

## 9. Quyết định cần TJ
1. Cung cấp **đề bài gốc của chị Nhi** và **tài liệu policy đối thủ** (nếu có — đề xuất đặt vào thư mục `private/`, đã có trong `.gitignore`).
2. Xác nhận **bối cảnh doanh nghiệp đích** (công ty cụ thể hay giả định công ty tầm trung/lớn; ưu tiên kênh truyền thống hay kênh toàn thời gian) và **định dạng Gói A** (Slide deck 5–7 slides hay tài liệu Markdown/Word/PDF).
3. Nếu chưa có tài liệu policy gốc ngay hôm nay, xác nhận cho AGY tiến hành xây luôn **Excel Reference Model MVP + 3 hướng Scheme + MAPA xuôi/ngược** bằng tham số cấu hình (có nhãn `[SYNTHETIC_ASSUMPTION]`) để sẵn sàng lắp số thật khi có tài liệu.

## 10. Trạng thái Git
- Local repository khởi tạo mới tại `C:\Users\User\Desktop\TJ\Project\W24_Life-Insurance-Strategy-Lab`, nhánh `main`.
- Không có remote, chưa push GitHub.

## 11. Commit SHA
- Đang chuẩn bị tạo commit khởi tạo đầu tiên (`chore: initialize W24 foundation, discovery, wheel check, and comparison v0.1`). Xem `git log -n 1` sau checkpoint.

## 12. Các sản phẩm P0 còn thiếu
- [ ] Danh mục Business Rules đã trích xuất từ policy gốc (có số trang nguồn).
- [ ] Bảng so sánh đối thủ v1.0 (có số liệu thực tế trên 7 nhóm đại lý).
- [ ] 3 phương án Compensation Scheme (A: Growth, B: Quality, C: Balanced/Hybrid).
- [ ] Excel Reference Model (tách Inputs/Formulas/Outputs + Golden Test Cases).
- [ ] Phân tích doanh số, chất lượng, chi phí, độ nhạy & ROI.
- [ ] Bản trình bày lãnh đạo Gói A (5–7 trang/slide tại `outputs/interview/`).

## 13. Hành động tiếp theo
- **Nếu TJ gửi tài liệu policy & đề bài gốc:** Đọc PDF bằng `pymupdf`/`pdfplumber` → cập nhật `source-registry.csv` & `business-rules-catalog.csv` → nâng cấp bảng so sánh lên v1.0 → xây Excel Reference Model.
- **Nếu chưa có tài liệu ngay:** Xây ngay Excel Reference Model MVP (tham số hóa hoàn toàn) + MAPA xuôi/ngược + 3 phương án Compensation Scheme + Golden Test Cases bằng Python để chứng minh repo đạt Level 2 (tái tạo kết quả).

## 14. Tiến độ so với deadline
- **Ngày 1 / 3:** Đã hoàn thành toàn bộ nền móng repo, Domain Discovery, Wheel Check pháp lý & kỹ thuật, cấu trúc Ground Truth và bảng so sánh v0.1. Đúng tiến độ Ngày 1; điểm nghẽn duy nhất cần mở khóa là tài liệu policy gốc & đề bài gốc.
