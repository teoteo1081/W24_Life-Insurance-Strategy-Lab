# AGENTS.md — Quy tắc làm việc cho AI Agent

Áp dụng cho mọi AI agent làm việc trong repository `W24_Life-Insurance-Strategy-Lab`.

## 1. Vai trò & Giới hạn quyền hạn

- **AGY** là tác nhân thực thi duy nhất trong phiên làm việc hiện tại. **Không tự ý khởi chạy hoặc giao việc cho AI agent khác.**
- **TJ** là Business Owner của dự án nghiên cứu. Các quyết định về thay đổi phạm vi, phát sinh chi phí, chia sẻ dữ liệu ra ngoài, thay đổi quy tắc nghiệp vụ chính thức hoặc thao tác không thể phục hồi phải xin xác nhận của TJ.
- Không sửa đổi bất kỳ repository nào khác ngoài `W24_Life-Insurance-Strategy-Lab`.
- Không tự ý thêm remote, push GitHub, chạy lệnh Git phá hủy, upload tài liệu nội bộ lên dịch vụ bên ngoài, hay dùng API trả phí.

## 2. Nguyên tắc Bằng chứng & Ground Truth

Mọi thông tin phải được gắn nhãn phân loại rõ ràng:
- `VERIFIED FACT` — Dữ kiện đã kiểm chứng trực tiếp từ tài liệu gốc/văn bản pháp luật.
- `SOURCE CLAIM` — Thông tin do một nguồn công khai/báo chí/tài liệu công bố nhưng chưa kiểm chứng bản gốc nội bộ.
- `ASSUMPTION` — Giả định mô phỏng có ghi rõ phạm vi.
- `HYPOTHESIS` — Giả thuyết cần kiểm chứng.
- `PROPOSAL` — Đề xuất thiết kế, không phải chính sách đã duyệt.
- `UNKNOWN` — Chưa có dữ liệu. Không tự điền 0 hoặc bịa số.
- `CONFLICTING EVIDENCE` — Có mâu thuẫn giữa các nguồn, cần ghi nhận để người có thẩm quyền phân xử.

## 3. Nguyên tắc Nghiệp vụ & Kỹ thuật

- Không đánh đồng `APE`, `FYP`, `FYC`, `RYP`, `RYC`, phí thực thu, thu nhập được hưởng và thu nhập thực trả.
- Không mặc định mỗi công ty chỉ có một chính sách; luôn tách rõ: Công ty → Kênh → Scheme → Đối tượng/Cấp bậc → Phiên bản → Hiệu lực.
- Không biến thông tin truyền miệng (đặc biệt về kênh Alpha) thành kết luận.
- Không nhầm tỷ lệ chi phí trên APE với ROI.
- Không tuyên bố đã kiểm thử hoặc đã audit độc lập nếu chưa thực hiện hoặc tự viết tự kiểm.
- Ưu tiên tuyệt đối **P0** trong deadline 3 ngày; không hy sinh P0 cho P1/P2.

## 4. Giao tiếp với TJ

- Dùng tiếng Việt, giữ thuật ngữ tiếng Anh chuyên ngành cần thiết.
- Giải thích ngắn gọn bản chất khi ra quyết định quan trọng: Vấn đề → Vì sao → Lựa chọn → Lý do chọn → Bằng chứng → Rủi ro → Điểm TJ cần quyết định.
- Cập nhật `HANDOVER.md` tại mỗi mốc checkpoint quan trọng.
