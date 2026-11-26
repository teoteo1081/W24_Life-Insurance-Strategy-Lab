# ANCHOR_SPEC.md — Mục tiêu và Phạm vi Chuẩn

**Dự án:** W24 — Life Insurance Strategy Lab  
**Phiên bản:** 1.0  
**Business Owner:** TJ  

---

## 1. Bài toán kinh doanh cốt lõi

Theo thông tin TJ cung cấp (cần đối chiếu lại với đề bài gốc của chị Nhi khi nhận được):

> Phân tích các chính sách thu nhập đại lý giữa các công ty bảo hiểm nhân thọ và đề xuất chính sách phù hợp tại thị trường Việt Nam nhằm thúc đẩy:
> 1. Gia tăng doanh số (APE / FYP).
> 2. Chất lượng kinh doanh (Persistency, chất lượng tư vấn, giảm hủy hợp đồng sớm).
> 3. Hiệu quả về mặt chi phí và ROI.

**Đối tượng nghiên cứu dự kiến:**
- AIA (bao gồm các kênh như truyền thống, AIA Exchange, v.v.)
- Manulife
- Chubb Life
- Kênh Alpha (thuộc AIA Việt Nam theo nguồn công khai — chưa có tài liệu policy nội bộ xác minh)
- Các chính sách / đề xuất bổ sung sau này.

---

## 2. Phân cấp Ưu tiên (Deadline 3 ngày)

### P0 — Bắt buộc (Không được hy sinh)
1. Phân tích chính sách đối thủ (có phân tách công ty / kênh / đối tượng / phiên bản).
2. Bảng so sánh chính sách thu nhập trên cùng một cơ sở chuẩn hóa.
3. Danh mục quy tắc nghiệp vụ (`business-rules-catalog`) có truy vết nguồn.
4. Đề xuất compensation scheme phù hợp (tối thiểu 3 hướng chiến lược: Growth / Quality / Balanced-Hybrid).
5. Phân tích tác động đến doanh số, chất lượng kinh doanh và chi phí / ROI (có phân tích độ nhạy & điểm hòa vốn).
6. Mô hình Excel tham chiếu có thể kiểm chứng độc lập (tách Inputs / Formulas / Outputs + Golden Test Cases).
7. Bản trình bày lãnh đạo (Gói A — Interview Delivery, 5–7 trang/slide).

### P1 — Giá trị bổ sung quan trọng (Làm khi P0 vững)
- Mô hình MAPA tính xuôi & tính ngược.
- Khung chiến lược tuyển dụng sales (Build / Buy / Hybrid) & marketing tuyển dụng.
- Khung chiến lược tìm kiếm khách hàng & phân bổ ngân sách marketing.
- HTML Interactive Simulator phiên bản MVP (chỉ làm khi Excel đã kiểm chứng và có Parity Test).

### P2 — Phát triển sau deadline
- Tự động hóa đọc PDF, tối ưu hóa nâng cao (Operations Research), tích hợp CRM/Chatbot, hệ thống tính hoa hồng production, kết nối nền tảng quảng cáo.

---

## 3. Tiêu chuẩn Trưởng thành Repository

- **Mục tiêu 3 ngày:** Đạt **Level 1 (Có tổ chức)** toàn repo và chứng minh **Level 2 (Có thể tái tạo kết quả)** trên các luồng tính toán trọng yếu (Compensation, MAPA, Cost/ROI sensitivity).
- Không tự nhận đạt cấp độ cao hơn khi chưa có bằng chứng kiểm thử thực tế.

---

## 4. Ranh giới Bảo mật & Chia sẻ

- **Gói A (`outputs/interview/`):** Gói trình bày cho chị Nhi. Chỉ chứa kết luận có bằng chứng, bảng so sánh, đề xuất, trade-offs và lộ trình pilot.
- **Gói B (Working Papers):** Giữ nội bộ trong repo của TJ.
- Tài liệu gốc nội bộ của doanh nghiệp/đối thủ (PDF policy, dữ liệu nhạy cảm) đặt trong `private/` (đã nằm trong `.gitignore`), không commit vào lịch sử Git nếu chưa được cấp quyền.
