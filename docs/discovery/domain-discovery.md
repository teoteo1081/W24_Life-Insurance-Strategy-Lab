# Domain Discovery — Khám phá Bài toán Nghiệp vụ

**Trạng thái:** v0.1 (Ngày 1 — Đang chờ đề bài gốc và tài liệu policy nội bộ)  
**Người thực hiện:** AGY  
**Business Owner:** TJ  

---

## 1. Khung Bài toán Kinh doanh

| Hạng mục | Nội dung | Phân loại |
|---|---|---|
| **Mục tiêu kinh doanh** | Phân tích chính sách thu nhập đại lý BHNT giữa các đối thủ và đề xuất compensation scheme phù hợp tại thị trường Việt Nam nhằm thúc đẩy: (1) Gia tăng doanh số, (2) Chất lượng kinh doanh, (3) Hiệu quả chi phí & ROI. | `SOURCE CLAIM` (theo tóm tắt của TJ, cần đối chiếu đề bài gốc của chị Nhi) |
| **Vấn đề cần giải quyết** | Chính sách thu nhập đại lý thường đối mặt xung đột 3 chiều: trả cao để kéo doanh số/tuyển dụng dễ gây đội chi phí và trục lợi/hủy hợp đồng sớm; siết chặt để giữ chất lượng dễ làm giảm sức hút tuyển dụng & activation. | `VERIFIED FACT` (đặc thù ngành BHNT) |
| **Stakeholders** | - Chị Nhi (người đặt đề bài / đánh giá bài tư vấn)<br>- TJ (Business Owner dự án)<br>- Ban lãnh đạo doanh nghiệp / Bộ phận Agency Strategy, Finance, Actuarial, Legal & Compliance (người ra quyết định thực tế nếu triển khai). | `SOURCE CLAIM` / `ASSUMPTION` |
| **Đối tượng nghiên cứu** | AIA (truyền thống / AIA Exchange), Kênh Alpha (thuộc AIA VN theo nguồn công khai), Manulife, Chubb Life, và các scheme bổ sung sau này. | `SOURCE CLAIM` |
| **Phạm vi trong 3 ngày (P0)** | So sánh chính sách thu nhập trên cùng cơ sở chuẩn hóa; danh mục business rules có nguồn; đề xuất 3 hướng scheme (Growth / Quality / Balanced-Hybrid); mô hình Excel kiểm chứng được; phân tích doanh số–chất lượng–chi phí/ROI; bài trình bày 5–7 trang/slide. | `VERIFIED FACT` (Master Execution Contract) |
| **Ngoài phạm vi 3 ngày** | Tự động hóa đọc PDF hàng loạt, tối ưu hóa nâng cao (OR), tích hợp CRM/Chatbot, hệ thống tính hoa hồng production, chạy quảng cáo thật. | `VERIFIED FACT` |
| **KPI đánh giá thành công** | Doanh số (`APE`/`FYP`), Tỷ lệ hoạt động (`Active Ratio`), Năng suất (`Cases/Active Agent`), Chất lượng (`Persistency K2/13M`, tỷ lệ hủy trong 21 ngày cân nhắc), Chi phí (`Total Comp / APE`, `Cost per Productive Agent`), `Contribution` & `ROI` (khi đủ dữ liệu định biên). | `PROPOSAL` (cần xác nhận ưu tiên từ đề bài gốc) |
| **Ràng buộc pháp lý** | Tuân thủ Luật Kinh doanh bảo hiểm 08/2022/QH15, NĐ 46/2023/NĐ-CP (sửa đổi bởi NĐ 97/2026/NĐ-CP), TT 67/2023/TT-BTC và **TT 96/2026/TT-BTC** (trần hoa hồng mới áp dụng từ 01/01/2027, siết hoa hồng phí đóng thêm). | `SOURCE CLAIM` (tổng hợp từ nguồn pháp lý công khai — cần đối chiếu văn bản gốc khi đi sâu điều khoản) |
| **Ràng buộc thời gian** | 3 ngày hoàn thành Gói A (Interview Delivery) + Excel Reference Model kiểm chứng được. | `VERIFIED FACT` |
| **Ràng buộc ngân sách / dữ liệu tài chính nội bộ** | Chưa có số liệu ngân sách tối đa, biên lợi nhuận (`VNB margin`), định phí vận hành hay baseline thực tế của doanh nghiệp đích. | `UNKNOWN` |

---

## 2. Kiểm kê Dữ liệu Hiện có vs. Còn thiếu

### Đang có
- Master Execution Contract v1.0 (từ TJ).
- Thông tin pháp lý công khai tại Việt Nam (Luật 08/2022/QH15, TT 67/2023/TT-BTC, TT 96/2026/TT-BTC, NĐ 97/2026/NĐ-CP) ở mức tóm tắt công khai.
- Thông tin báo chí/công khai cấp tổng quan về AIA / AIA Exchange / AIA Alpha, Manulife, Chubb Life.

### Đang thiếu (Cần TJ cung cấp để đạt Ground Truth)
1. **[ƯU TIÊN CAO NHẤT — P0]** Đề bài gốc của chị Nhi (email/brief/slide yêu cầu cụ thể về định dạng, đối tượng doanh nghiệp mục tiêu, tiêu chí chấm điểm).
2. **[ƯU TIÊN CAO NHẤT — P0]** Tài liệu chính sách thu nhập gốc (PDF/Excel/ảnh chụp) của từng công ty/kênh:
   - AIA (phân rõ kênh truyền thống / AIA Exchange / Kênh Alpha, phiên bản & ngày hiệu lực).
   - Manulife (phân rõ kênh truyền thống / MPro / các chương trình đại lý mới, quản lý).
   - Chubb Life (chính sách đại lý & quản lý, phiên bản & ngày hiệu lực).
3. **[ƯU TIÊN TRUNG BÌNH — P0/P1]** Thông tin bối cảnh doanh nghiệp đích (quy mô manpower hiện tại, tỷ lệ active, persistency K2 hiện tại, sản phẩm chủ lực UL/ILP hay truyền thống, ngân sách thưởng/marketing dự kiến) — nếu đề bài không cung cấp, ta sẽ dùng bộ giả định minh bạch và phân tích độ nhạy (Sensitivity Analysis).

---

## 3. Danh sách Câu hỏi cho TJ (Xếp theo mức độ ảnh hưởng đến quyết định)

| Mức độ ảnh hưởng | ID | Câu hỏi | Tác động nếu chưa có câu trả lời |
|---|---|---|---|
| **Rất cao (P0)** | Q1 | TJ đã có **đề bài gốc của chị Nhi** và **bộ tài liệu policy (PDF/Excel/ảnh)** của AIA, Manulife, Chubb Life, Kênh Alpha chưa? Nếu có, TJ có thể đặt vào thư mục `private/` (đã được `.gitignore` bảo vệ) để AGY đọc trực tiếp không? | Chưa thể trích xuất Business Rules thật có số trang nguồn; bảng so sánh đối thủ phải giữ ở mức khung + nguồn công khai, không được kết luận xếp hạng tuyệt đối. |
| **Cao (P0)** | Q2 | Doanh nghiệp đích trong bài tư vấn là một **công ty bảo hiểm cụ thể** (hay giả định một công ty tầm trung/lớn tại VN)? Đang thiên về kênh đại lý truyền thống (Part-time + Full-time) hay muốn xây kênh Full-time chuyên nghiệp (như Exchange/Alpha)? | Ảnh hưởng trực tiếp đến việc ưu tiên Scheme A (Growth), Scheme B (Quality) hay Scheme C (Balanced/Hybrid). |
| **Trung bình (P0)** | Q3 | Đề bài yêu cầu đầu ra Gói A là **Slide deck (5–7 slides)** hay **tài liệu Word/PDF/Markdown executive brief**? | Quyết định định dạng xuất bản ở Ngày 3. |
| **Trung bình (P1)** | Q4 | Có dữ liệu baseline nào về **MAPA hiện tại** (Manpower, Active Ratio, Productivity, Average Case Size) hoặc **ngân sách thưởng/marketing** được phép dùng không? | Nếu không có, AGY sẽ xây mô hình Excel tham số hóa hoàn toàn (PO có thể tự nhập số) và chạy kịch bản giả lập có nhãn `[SYNTHETIC_ASSUMPTION]` kèm phân tích độ nhạy. |
| **Thấp (P1/P2)** | Q5 | Thông tin về **Kênh Alpha** mà TJ nghe được gồm những điểm cụ thể nào cần kiểm chứng? | Giúp tách rõ phần nào là `HYPOTHESIS` cần kiểm chứng và phần nào là `SOURCE CLAIM` từ báo chí công khai (mô hình Alpha của AIA VN ra mắt cuối 2023). |

---

## 4. Hướng xử lý trong khi chờ tài liệu

Theo nguyên tắc không dừng dự án khi thiếu một phần dữ liệu:
1. Hoàn thiện ngay khung chuẩn hóa dữ liệu (`source-registry.csv`, `business-rules-catalog.csv`, `glossary.md`).
2. Hoàn thiện bảng so sánh đối thủ v0.1 dựa trên khung pháp lý VN hiện hành và nguồn công khai (đánh dấu rõ `UNKNOWN` ở các chỉ số nội bộ).
3. Sẵn sàng chuyển sang Ngày 2: xây Excel Reference Model tham số hóa hoàn toàn + 3 hướng Compensation Scheme + MAPA xuôi/ngược, để ngay khi TJ nạp tài liệu policy gốc vào `private/`, chỉ cần trích xuất rule vào bảng và chạy lại toàn bộ mô hình.
