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

## 2. Tổng hợp Khung Pháp lý Việt Nam về Hoa hồng, Thưởng & Chi phí Đại lý BHNT (Nhóm E — Trọng tâm P0 — Đã Khắc phục sau Kiểm toán)

> **Cảnh báo Kiểm chứng Pháp lý (`SOURCE_CLAIM` / `SOURCE_NOT_VERIFIED`):** Thông tin pháp lý dưới đây được tổng hợp từ nguồn tóm tắt công khai (chinhphu.vn, thuvienphapluat.vn, luatvietnam.vn, thoibaotaichinhvietnam.vn). Chưa tải/đối chiếu trực tiếp bản PDF toàn văn Công báo chính thức trong repository nên toàn bộ quy tắc pháp lý được gắn nhãn `SOURCE_NOT_VERIFIED` cho đến khi đối chiếu bản gốc Công báo trước khi ban hành chính sách thật.

### 2.1. Các văn bản nền tảng & 3 lớp trần chi phí riêng biệt (2023–2026)
1. **Luật Kinh doanh bảo hiểm số 08/2022/QH15** (hiệu lực 01/01/2023): Yêu cầu chi trả hoa hồng minh bạch, gắn với hiệu quả, không vượt trần của Bộ Tài chính.
2. **Nghị định 46/2023/NĐ-CP** & **Nghị định 97/2026/NĐ-CP (ban hành 31/03/2026):** Bên cạnh quy định quản trị, NĐ 97/2026 làm rõ nhóm **chi phí đào tạo ban đầu/nâng cao, tuyển dụng, quản lý đại lý cá nhân, kiểm tra giám sát chất lượng đại lý** là khoản chi nghiệp vụ/quản lý tách biệt với hoa hồng đại lý (Điều 51) và thưởng/hỗ trợ đại lý (Điều 52), nhưng phải có hợp đồng, biên bản nghiệm thu dịch vụ thực tế và tuân thủ quy định thuế/tài chính. *(Giải thích vì sao AIA, Manulife và Chubb Life đều cấu trúc thu nhập CQL/PSM+/AL/RD thành "Phí dịch vụ" kèm biên bản nghiệm thu).*
3. **Thông tư 67/2023/TT-BTC** (ban hành 02/11/2023): Quy định **HAI TRẦN RIÊNG BIỆT** bắt buộc phải tách bạch trong mọi mô hình chi phí:
   - **Lớp 1 — Điều 51 (Trần Hoa hồng Đại lý theo từng hợp đồng):** Có phân tách mốc chuyển tiếp **trước 01/07/2024** (UL >10 năm Y1 tối đa 40%, Y2 10%, Y3+ 7%; Hỗn hợp >10 năm Y1 40%) và **từ 01/07/2024** (UL/ILP & Hỗn hợp >10 năm hạ Y1 xuống **30%**, đẩy Y2 lên **20%** để tăng lực duy trì tái tục). Bao gồm cả **Bảo hiểm Nhóm (= 50% trần cá nhân, Khoản 3.2 Điều 51)** và **Bảo hiểm Hưu trí (= 3% tổng phí thu được)**.
   - **Lớp 2 — Điều 52 (Trần Thưởng, Hỗ trợ Đại lý & Quyền lợi khác ở mức danh mục công ty trong năm tài chính — BỔ SUNG SAU KIỂM TOÁN):**
     - **Khai thác mới (hết lộ trình chuyển tiếp vào 31/12/2025 → áp dụng đầy đủ năm 2026!):** Tổng chi thưởng, hỗ trợ đại lý và quyền lợi khác cho đại lý khai thác mới trong năm tài chính **≤ 20% phí bảo hiểm thực thu** (đối với hợp đồng ≤ 1 năm / tái tục hàng năm) **+ ≤ 30% phí bảo hiểm thực thu năm thứ nhất** (đối với hợp đồng > 1 năm).
     - **Chăm sóc tái tục:** Tổng chi thưởng, hỗ trợ cho đại lý chăm sóc hợp đồng tái tục (> 1 năm) **≤ 7% phí bảo hiểm tái tục thực thu** trong năm tài chính.
4. **Thông tư 96/2026/TT-BTC** (ban hành 02/07/2026, áp dụng khung hoa hồng mới cho hợp đồng phát hành từ **01/01/2027**):
   - Chuẩn hóa khung trần hoa hồng sửa đổi Điều 51 TT 67/2023.
   - **Siết chặt hoa hồng phí đóng thêm (Top-up):** Hoa hồng đại lý trên phí đóng thêm của hợp đồng UL/ILP/Hưu trí **không được vượt quá tỷ lệ phí ban đầu** áp dụng cho phần phí đóng thêm đó (đồng thời chịu trần phí ban đầu tối đa theo Điều 22 TT 67/2023 — lưu ý mức tham chiếu 1.5% cần đối chiếu toàn văn).

### 2.2. Bảng Trần Hoa hồng Tối đa (Điều 51 TT 67/2023 từ 01/07/2024 & TT 96/2026 từ 01/01/2027)

*(Trạng thái: `SOURCE_CLAIM` / `SOURCE_NOT_VERIFIED` — Cần đối chiếu toàn văn Công báo trước khi ban hành chính sách thật)*

| Nghiệp vụ bảo hiểm nhân thọ | Nộp phí 1 lần | Năm thứ 1 (FYC tối đa) | Năm thứ 2 (RYC tối đa) | Năm thứ 3+ (RYC tối đa) | Ghi chú kiểm chứng & Ngoại lệ |
|---|---|---|---|---|---|
| **Hợp đồng ≤ 1 năm / tái tục hàng năm** | — | **20%** | — | — | Áp dụng cho từng kỳ đóng phí thực thu. |
| **Bảo hiểm tử kỳ, trọn đời (cá nhân)** | **15%** | **40%** | **20%** | **15%** | Không bị hạ trần như UL/ILP. |
| **Sinh kỳ, trả tiền định kỳ, hỗn hợp (≤ 10 năm)** | **5%** | **25%** | **7%** | **5%** | — |
| **Sinh kỳ, trả tiền định kỳ, hỗn hợp (> 10 năm)** | **3%–7%** *(xem ghi chú)* | **30%** | **20%** | **10%** (Y3) / **7%–10%** (Y4+) | Trước 01/07/2024: Y1 40%/Y2 10%/Y3+ 10%. Các bản tóm tắt công khai có chênh lệch nhỏ ở phí 1 lần (3% vs 7%) & Y4+ — **cần kiểm tra Công báo**. |
| **Liên kết chung (UL), Liên kết đơn vị (ILP)** *(trên PCB)* | **≤ 7%** | **30%** | **20%** | **10%** (Y3) / **7%–10%** (Y4+) | Trước 01/07/2024: Y1 40%/Y2 10%/Y3+ 7%. **Phí đóng thêm (Top-up):** ≤ tỷ lệ phí ban đầu (TT 96/2026). Có chênh lệch bản tóm tắt về Y4+ (10% vs 7%) — **cần kiểm tra Công báo**. |
| **Bảo hiểm Hưu trí** | — | **≤ 3%** tổng phí thực thu | **≤ 3%** tổng phí thực thu | **≤ 3%** tổng phí thực thu | Phí đóng thêm hưu trí ≤ phí ban đầu (TT 96/2026). |
| **Bảo hiểm Nhân thọ Nhóm (Group Life)** | **50% trần cá nhân** | **50% trần cá nhân** | **50% trần cá nhân** | **50% trần cá nhân** | Khoản 3.2 Điều 51 TT 67/2023. |

### 2.3. Bảng Trần Thưởng & Hỗ trợ Đại lý Riêng biệt (Điều 52 TT 67/2023 — Hiệu lực đầy đủ từ 01/01/2026)

| Hạng mục chi phí ngoài Hoa hồng (Điều 52 TT 67/2023) | Cơ sở tính trần (Cấp toàn danh mục DN trong năm tài chính) | Trần tối đa bắt buộc | Ghi chú áp dụng vào mô hình W24 |
|---|---|---|---|
| **Thưởng, hỗ trợ & quyền lợi khác — Khai thác mới (≤ 1 năm)** | Phí bảo hiểm thực thu năm tài chính (HĐ ≤ 1 năm / tái tục năm) | **≤ 20%** | Kiểm tra bắt buộc ở tầng **Enterprise Distribution Cost** (không nhầm với trần 30% hoa hồng cá nhân). |
| **Thưởng, hỗ trợ & quyền lợi khác — Khai thác mới (> 1 năm)** | Phí bảo hiểm thực thu **Năm 1** trong năm tài chính (HĐ > 1 năm) | **≤ 30%** | **Rất quan trọng:** Nếu công ty có nhiều đại lý đạt thưởng 85%–109% FYC (tương đương 25%–33% FYP), tổng thưởng toàn công ty có nguy cơ tiệm cận hoặc chạm trần 30% FYP Điều 52 nếu không cân bằng bằng đại lý năng suất trung bình/cơ chế giữ lại! |
| **Thưởng, hỗ trợ — Chăm sóc hợp đồng tái tục (> 1 năm)** | Phí bảo hiểm **tái tục thực thu** trong năm tài chính | **≤ 7%** | Bao phủ các khoản thưởng SYC/RYC (như AIA 30–50% SYC, Chubb 10–15% RYC). |
| **Chi phí Quản lý, Đào tạo, Tuyển dụng & Giám sát Đại lý (NĐ 97/2026)** | Hợp đồng dịch vụ & chứng từ nghiệm thu hợp lệ | Theo quy chế tài chính & luật thuế *(không gom chung trần Điều 52 nếu có dịch vụ quản lý thực)* | Phải kiểm soát rủi ro thanh tra thuế/BTC: không được ngụy trang thưởng bán cá nhân thành phí dịch vụ quản lý. |

### 2.4. Hàm ý Chiến lược cho Bài tư vấn W24
- **Hai gọng kìm pháp lý năm 2026–2027:** Doanh nghiệp BHNT tại Việt Nam chịu đồng thời **(1) Trần Hoa hồng cá nhân theo hợp đồng (Điều 51: 30% FYC cho UL/ILP)** và **(2) Trần Tổng Thưởng & Hỗ trợ Đại lý khai thác mới theo danh mục công ty (Điều 52: 30% FYP năm 1, hết lộ trình chuyển tiếp từ 01/01/2026)**.
- **Hệ quả thiết kế trực tiếp:**
  1. Không doanh nghiệp nào có thể cạnh tranh bằng đẩy FYC UL/ILP vượt 30% hoặc trả hoa hồng cao cho phí đóng thêm (Top-up bị khóa theo TT 96/2026).
  2. Thiết kế thưởng cá nhân cực cao như Chubb Life (AR đỉnh 85.8% FYC ≈ 25.7% FYP; AL cá nhân đỉnh 109.2% FYC ≈ 32.8% FYP) **chỉ khả thi dưới trần 30% Điều 52 ở cấp toàn danh mục** khi phần lớn đại lý ở bậc thấp hơn hoặc một phần được hạch toán sang phí dịch vụ quản lý hợp lệ (theo NĐ 97/2026).
  3. Do đó, mọi đề xuất chính sách trong W24 phải tích hợp **Mandatory Regulatory Gate** kiểm tra cả **Điều 51 (Hoa hồng theo sản phẩm)**, **Điều 52 (Tổng thưởng đại lý ≤ 30% FYP Y1 / ≤ 7% RYP)** và **TT 96/2026 (Top-up)** ngay trong Excel Reference Model.
