# AGENTS.md — Quy tắc Làm việc & Phân định Thẩm quyền cho AI Agent

## STRICT DATA INGESTION & MAPPING PROTOCOL (MANDATORY)
1. **NO PREMATURE CALCULATION:** Never write calculation code or summary tables before completing a 100% Source & Entity Inventory of ALL input files.
2. **EXACT TITLE & SCOPE EXTRACTION:** Extract exact verbatim titles/roles and eligibility rules with `[FileName : PageNumber]` citations before normalizing across entities.
3. **NEGATIVE PROOF RULE:** You are strictly forbidden from claiming "missing data/document" unless you provide a search log proving all input files and filenames were scanned for related keywords.
4. **EVIDENCE-BOUND NUMBERS:** Every threshold, tier, or percentage in code/tables must cite its exact PDF source and page number.

Áp dụng cho mọi AI agent làm việc trong repository `W24_Life-Insurance-Strategy-Lab`.

## 1. Phân định Vai trò & Giới hạn Thẩm quyền

- **Business Owner (`TJ`):** Chủ sở hữu dự án. Mọi quyết định về thay đổi phạm vi, phát sinh chi phí, quyền công bố/tái phân phối tài liệu bên thứ ba, chuyển chế độ hiển thị repository, thay đổi quy tắc nghiệp vụ chính thức, push GitHub, hoặc thao tác không thể phục hồi đều phải có xác nhận tường minh của TJ (lưu tại `docs/decisions/decision-register.md`).
- **Implementation Agent (`AGY`):** Tác nhân thực thi kỹ thuật trong phiên triển khai; không tự ý khởi chạy hay ủy quyền cho AI agent khác, không tự cấp nhãn `INDEPENDENTLY_VERIFIED` cho công việc mình thực hiện.
- **Independent Auditor (`Codex`):** Tác nhân kiểm toán độc lập tách biệt, chỉ đọc và đánh giá bằng chứng thực tế; báo cáo kiểm toán chứa thông tin hạn chế chia sẻ được lưu ngoài repository PUBLIC.
- Không sửa đổi bất kỳ repository nào khác ngoài `W24_Life-Insurance-Strategy-Lab`.
- Không tự ý sửa PDF nguồn gốc, thêm remote, push GitHub, đổi visibility, chạy lệnh Git phá hủy (reset/force-push/clean/rewrite history), cài phần mềm chưa duyệt, hay dùng API trả phí.

## 2. Nguyên tắc Bảo mật, Bản quyền & Đóng gói Công khai

Tuân thủ nghiêm túc [docs/governance/confidentiality-and-rights-policy.md](docs/governance/confidentiality-and-rights-policy.md):
- Không nhầm lẫn giữa **chế độ PUBLIC của repository** với **quyền tái phân phối hợp pháp tài liệu bên thứ ba**.
- Tuyệt đối không đưa vào repository PUBLIC: skill gốc hoặc tài liệu phương pháp độc quyền của bên thứ ba, prompt chia sẻ riêng, nội dung trao đổi cá nhân, khóa bí mật/token, PII khách hàng, hay đường dẫn cục bộ máy cá nhân (`file://` trỏ ổ đĩa cục bộ / thư mục user hệ điều hành).
- Luôn chạy `python scripts/run_checks.py` để kiểm tra quality gates và staging hygiene trước mỗi commit.

## 3. Nguyên tắc Bằng chứng & Ground Truth

Mọi thông tin phải gắn nhãn phân loại rõ ràng:
- `VERIFIED FACT` — Quan sát trực tiếp trong tài liệu gốc, runtime hoặc metadata công bố chính thức.
- `SOURCE CLAIM` — Thông tin từ nguồn công khai/tóm tắt nhưng chưa đối chiếu toàn văn bản gốc.
- `ASSUMPTION` — Giả định mô phỏng có ghi rõ phạm vi và mẫu số.
- `HYPOTHESIS` — Giả thuyết cần kiểm chứng thực nghiệm.
- `PROPOSAL` — Đề xuất thiết kế minh họa, không phải chính sách đã phê duyệt.
- `UNKNOWN` — Chưa có dữ liệu. **Tuyệt đối không tự chuyển `UNKNOWN` thành `0` hoặc hệ số mặc định `1.0` nếu không có điều khoản chính sách minh bạch.**
- `CONFLICTING EVIDENCE` — Mâu thuẫn nội tại giữa các nguồn; không tự phán xử mà leo thang vào `docs/decisions/decision-register.md`.

## 4. Nguyên tắc Nghiệp vụ, Tài chính & Kiểm thử

- Không đánh đồng `APE`, `FYP`, `FYC`, `RYP`, `RYC`, phí thực thu, thu nhập được hưởng (`Earned`), thu nhập thực trả (`Cash Paid Y1`), trả chậm (`Deferred`) và thu hồi (`Clawback`).
- Không đánh đồng **chi phí mô phỏng / ngưỡng hòa vốn biên gộp (`Modeled Break-Even Gross Margin`)** với **ROI thực tế đã chứng minh (`Actual ROI`)** hay kết quả kinh doanh thực tế.
- Không suy diễn ngày hiệu lực từng điều khoản pháp lý chỉ từ metadata ngày ban hành văn bản; giữ `SOURCE_NOT_VERIFIED` / `CONDITIONAL` cho đến khi đối chiếu toàn văn hợp nhất (`44/2026/VBHN-TT-BTC`).
- Mọi kiểm thử số phải chặn `NaN`, `±Inf` và sai kiểu; không báo `PASS` khi 0 test chạy.

## 5. Single Source of Truth & Giao tiếp với TJ

- Dùng tiếng Việt, giữ thuật ngữ tiếng Anh chuyên ngành cần thiết.
- Giải thích ngắn gọn khi trình quyết định: Vấn đề → Vì sao → Lựa chọn → Lý do chọn → Bằng chứng → Rủi ro → Điểm TJ cần quyết định.
- Trạng thái hiện hành duy nhất được cập nhật tại `HANDOVER.md`; không tạo thêm nhiều file theo dõi trùng lặp cùng một trạng thái.
