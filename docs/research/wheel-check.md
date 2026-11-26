# Wheel Check — Nghiên cứu Giải pháp Sẵn có & Khung Pháp lý (Time-boxed)

**Ngày thực hiện:** 2026-11-26  
**Mục đích:** Kiểm tra các phương pháp, công cụ và quy định pháp lý hiện hành trước khi tự xây, nhằm tránh phát minh lại bánh xe và đảm bảo tuân thủ deadline 3 ngày.

---

## 1. Tổng hợp Quyết định Wheel Check (Nhóm A – E)

| Nhóm | Vấn đề cần giải quyết | Công cụ / Phương pháp hiện có | Nguồn / Phiên bản | Phù hợp P0 (3 ngày) | Chi phí / Offline | Độ phức tạp bảo trì | Giới hạn | Quyết định |
|---|---|---|---|---|---|---|---|---|
| **A. Nghiệp vụ BHNT** | Chuẩn hóa cấu trúc chính sách thu nhập đại lý (FYC, RYC, Bonus, Override, Clawback, Persistency) | Khung phân tích Agency Compensation chuẩn ngành (LIMRA / MDRT benchmarks + cơ cấu FYC/Thưởng quý/Persistency gate) | Kiến thức ngành chuẩn hóa | Rất cao | 0đ / Offline | Thấp | Cần tài liệu policy gốc từng công ty để điền số liệu thật | **ADAPT** |
| **A. Nghiệp vụ BHNT** | Chiến lược phát triển đội ngũ (Build / Buy / Hybrid) | Mô hình vòng đời đại lý (Recruit → Activate → Productive → Retain) | Chuẩn quản trị Agency | Cao (P0/P1) | 0đ / Offline | Thấp | Thiếu số liệu tỷ lệ rơi rụng thực tế của doanh nghiệp đích | **ADAPT** |
| **B. Lập kế hoạch KD** | Lập kế hoạch doanh số & năng lực đội ngũ | **MAPA** (Manpower × Active Ratio × Productivity × Average Case Size) — xuôi & ngược + What-if / Sensitivity Analysis / Goal Seek | Chuẩn ngành BHNT & Financial Modeling | Rất cao | 0đ / Offline | Thấp | MAPA là mô hình trung bình kỳ; cần tách cohort (đại lý mới vs. cũ) để tránh sai lệch | **REUSE** |
| **B. Lập kế hoạch KD** | Tối ưu hóa có ràng buộc (Operations Research / Linear Programming) | Excel Solver / Python `scipy.optimize` | Công cụ tiêu chuẩn | Thấp cho 3 ngày (P2) | 0đ / Offline | Trung bình–Cao | Quá phức tạp cho giai đoạn thiếu dữ liệu biên lợi nhuận thật | **DEFER** |
| **C. Marketing** | Mô phỏng phễu tuyển dụng sales & tìm kiếm khách hàng | Hai phễu chuyển đổi độc lập có liên kết (Recruitment Funnel → Manpower/Active; Customer Funnel → Productivity/Case Size), tách Attribution vs. Incrementality | Chuẩn Performance Marketing | Trung bình (P1) | 0đ / Offline | Trung bình | Chưa có CPL & conversion rate thực tế; phải dùng giả định + độ nhạy | **ADAPT** (làm ở P1) |
| **D. Công nghệ** | Đọc PDF policy & trích xuất bảng biểu | Python `pymupdf` + `pdfplumber` (đã cài sẵn trên máy, Python 3.12.10) | Local installed | Rất cao | 0đ / Offline 100% | Thấp | PDF scan ảnh cần kiểm tra thủ công / OCR; không tự động hoàn toàn trong 3 ngày | **REUSE** |
| **D. Công nghệ** | Xây dựng mô hình tham chiếu & kiểm thử độc lập | Microsoft Excel + Python `openpyxl 3.1.5` (đã cài sẵn trên máy) để sinh file Excel có công thức thật & chạy Golden Test Cases bằng Python | Local installed | Rất cao | 0đ / Offline 100% | Thấp | Cần kiểm tra công thức khi mở bằng Excel để xác nhận tính toán không lỗi | **REUSE** |
| **D. Công nghệ** | Biểu diễn quy tắc nghiệp vụ chính sách | **Decision Tables** (dạng CSV/Excel có chuẩn cột theo DMN-lite) | Chuẩn DMN / Tabular Rules | Rất cao | 0đ / Offline | Thấp | Chưa cần full DMN engine trong 3 ngày | **ADAPT** |
| **D. Công nghệ** | Giao diện tương tác cho PO | Static HTML/CSS/Vanilla JS (không server, không API trả phí) | Trình duyệt local | Trung bình (P1) | 0đ / Offline | Trung bình | Chỉ xây sau khi Excel Reference Model đạt chuẩn và có Parity Test | **DEFER → P1** |
| **E. Pháp lý VN** | Ràng buộc trần hoa hồng & chi trả đại lý BHNT | Luật KDBH 08/2022/QH15; NĐ 46/2023/NĐ-CP & NĐ 97/2026/NĐ-CP; **TT 67/2023/TT-BTC** & **TT 96/2026/TT-BTC** | Bộ Tài chính / Chính phủ VN | **Bắt buộc (P0)** | 0đ / Công khai | Thấp | Cần đối chiếu điều khoản văn bản gốc chính thức cho từng sản phẩm cụ thể trước khi ban hành chính sách thật | **REUSE (Ràng buộc cứng)** |

---

## 2. Tổng hợp Khung Pháp lý Việt Nam về Hoa hồng Đại lý BHNT (Nhóm E — Trọng tâm P0)

> **Lưu ý kiểm chứng:** Thông tin dưới đây tổng hợp từ nguồn công khai (`SOURCE CLAIM` từ chinhphu.vn, thuvienphapluat.vn, luatvietnam.vn, thoibaotaichinhvietnam.vn tra cứu ngày 26/11/2026). Cần đối chiếu trực tiếp toàn văn văn bản pháp luật khi trình phê duyệt chính thức.

### 2.1. Các văn bản nền tảng & cập nhật mới nhất (2023–2026)
1. **Luật Kinh doanh bảo hiểm số 08/2022/QH15** (hiệu lực từ 01/01/2023): Nguyên tắc chi trả hoa hồng minh bạch, gắn với hiệu quả, không vượt quá mức tối đa do Bộ trưởng Bộ Tài chính quy định.
2. **Nghị định 46/2023/NĐ-CP** (ngày 01/07/2023) & **Nghị định 97/2026/NĐ-CP** (năm 2026): Quy định chi tiết thi hành Luật KDBH (NĐ 97/2026 tập trung cập nhật tiêu chuẩn nhân sự cấp cao, chuyên gia tính toán, chi nhánh/VPĐD và dịch vụ phụ trợ).
3. **Thông tư 67/2023/TT-BTC** (ban hành 02/11/2023): Quy định trần tỷ lệ hoa hồng đại lý bảo hiểm nhân thọ tối đa tính trên **phí bảo hiểm thực tế thu được của từng hợp đồng**.
4. **Thông tư 96/2026/TT-BTC** (ban hành 02/07/2026, quy định hoa hồng mới áp dụng cho hợp đồng phát hành từ **01/01/2027**):
   - Tiếp tục chuẩn hóa khung trần hoa hồng đại lý BHNT cá nhân.
   - **Điểm siết mới rất quan trọng:** Hoa hồng đại lý đối với **phí bảo hiểm đóng thêm (Top-up)** của hợp đồng liên kết chung (UL) / liên kết đơn vị (ILP) **không được vượt quá tỷ lệ phí ban đầu** đối với phần phí đóng thêm đó (nhằm chặn hành vi đẩy top-up trục lợi hoa hồng năm đầu).
   - Các khoản chi hỗ trợ, thù lao ngoài hoa hồng phải tuân thủ quy chế nội bộ, khung pháp luật và gắn với **chất lượng duy trì hợp đồng (persistency)**.

### 2.2. Bảng Trần Tỷ lệ Hoa hồng Tối đa (Nộp phí định kỳ — Hợp đồng cá nhân)

*(Theo nguồn công khai về TT 67/2023/TT-BTC và TT 96/2026/TT-BTC áp dụng từ 01/01/2027)*

| Nghiệp vụ bảo hiểm nhân thọ cá nhân | Nộp phí 1 lần | Năm thứ 1 (FYC tối đa) | Năm thứ 2 (RYC tối đa) | Năm thứ 3+ (RYC tối đa) |
|---|---|---|---|---|
| **Hợp đồng ≤ 1 năm / tái tục hàng năm** | — | 20% | — | — |
| **Bảo hiểm tử kỳ, trọn đời** | 15% | **40%** | **20%** | **15%** |
| **Sinh kỳ, trả tiền định kỳ, hỗn hợp (≤ 10 năm)** | 5% | **25%** | **7%** | **5%** |
| **Sinh kỳ, trả tiền định kỳ, hỗn hợp (> 10 năm)** | 3% | **30%** | **20%** | **10%** (Năm 3) / **3%–7%** (Năm 4+) |
| **Liên kết chung (UL), Liên kết đơn vị (ILP)** *(trên phí cơ bản)* | — | **30%** | **20%** | **10%** (Năm 3) / **7%** (Năm 4+) |

### 2.3. Hàm ý Chiến lược cho Bài tư vấn W24
- **Trần FYC cho sản phẩm chủ lực (UL/ILP) là 30% trên phí cơ bản thực thu** — điều này có nghĩa là **không doanh nghiệp nào có thể cạnh tranh bằng cách đẩy tỷ lệ FYC thuần vượt trần 30%**.
- Cuộc đua chính sách thu nhập giữa AIA, Manulife, Chubb Life và các mô hình toàn thời gian (AIA Exchange, AIA Alpha...) thực chất nằm ở:
  1. **Cấu trúc thưởng hiệu suất (Thưởng tháng/quý/năm, thưởng kích hoạt, thưởng MDRT)** và điều kiện mở khóa (Persistency gate).
  2. **Trợ cấp cố định / gói hỗ trợ chuyển đổi (Allowance / Transition package)** cho đại lý toàn thời gian hoặc thu hút đội ngũ.
  3. **Cơ chế Override & thưởng phát triển cấp quản lý** gắn với chất lượng duy trì (K2/13M) thay vì chỉ gắn với doanh số năm 1.
  4. **Cơ chế thu hồi (Clawback)** và thời điểm chi trả (trả ngay vs. trả chậm theo kỳ đóng phí năm 2) để kiểm soát rủi ro hủy hợp đồng sớm và dòng tiền.
- Với thời điểm hiện tại (cuối 11/2026), việc đề xuất chính sách phải **tính sẵn hiệu lực của Thông tư 96/2026/TT-BTC từ 01/01/2027** — đây sẽ là một điểm cộng rất lớn về tính thời sự và tuân thủ khi trình bày với chị Nhi.
