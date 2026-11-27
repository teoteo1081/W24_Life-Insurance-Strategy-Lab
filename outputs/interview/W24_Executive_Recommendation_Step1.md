# ĐỀ XUẤT CHIẾN LƯỢC CHÍNH SÁCH THU NHẬP ĐẠI LÝ BẢO HIỂM NHÂN THỌ TẠI VIỆT NAM (2026–2027)
## Gói Bàn giao Điều hành — Bước 1 (`Executive Advisory Deck — 7 Trang`)

> **Đề bài gốc (Chị Nhi):** *"Bước 1: Phân tích các chính sách thu nhập giữa các công ty, và đề xuất chính sách phù hợp tại thị trường VN, nhằm thúc đẩy gia tăng doanh số, chất lượng kinh doanh và hiệu quả về mặt chi phí (ROI)."*  
> **Cơ sở bằng chứng:** **9 văn bản chính sách hiệu lực 2026 (135 trang)** của **AIA Việt Nam (Kênh Alpha)**, **Chubb Life Việt Nam (Kênh Đại lý)** và **Manulife Việt Nam**. Bản khuyến nghị này được phân tích trên **7 văn bản đầu (116 trang)**, trong đó Manulife chỉ có tầng Quản lý Cấp cao `PSM+/HKD`; **2 văn bản Manulife bổ sung sau** (chính sách Đại lý cá nhân và biểu phí Quản lý cấp trung `UM+`, ghi "thông tin mật" — chỉ lưu local, DEC-14) đã được đưa vào bảng so sánh 4 mốc & ma trận quyền lợi trên trang web (trang 1–2) nhưng **chưa được phản ánh vào các kết luận và bảng dưới đây**. Ngoài ra: bối cảnh thị trường IAV/MOF 2024–2026 (`SOURCE_CLAIM`), và tham chiếu khung pháp lý Việt Nam (TT 67/2023/TT-BTC, NĐ 97/2026/NĐ-CP, TT 96/2026/TT-BTC, Văn bản hợp nhất `44/2026/VBHN-TT-BTC` — `SOURCE_NOT_VERIFIED` ở mức toàn văn từng điều khoản).  
> **Ranh giới Kết luận & Minh bạch Phạm vi (`BASED ON AVAILABLE POLICY DOCUMENTS`):**
> - Bộ tài liệu chỉ đại diện cho **thiết kế chính sách (Policy Design)** của các tầng có văn bản (chưa có gói trợ cấp Exchange/Pro & biểu HH AIA, hay quy định chung `260005V`/BD Chubb). Đại lý cá nhân & Quản lý cấp trung Manulife đã có văn bản nhưng chưa được đưa vào phần phân tích của tài liệu này — xem trang web (trang 1–2).
> - Toàn bộ con số tài chính trong tài liệu là **Chi phí & Điểm hòa vốn mô phỏng theo kịch bản chuẩn (`Modeled Payout / Modeled Distribution Cost / Modeled Break-Even Gross Margin`)**, **KHÔNG phải ROI thực tế đã chứng minh** hay bằng chứng tăng trưởng doanh số/chất lượng thực tế (`Observed Performance & Actual ROI = UNKNOWN` do chưa có `VNB Margin`, `OpEx` và dữ liệu cohort của doanh nghiệp đích).
> - Đề xuất là **kiến trúc tư vấn minh họa (`PROPOSAL / SYNTHETIC ASSUMPTION`)**, chỉ có giá trị định hướng thảo luận; mọi điều kiện tuân thủ pháp lý ở trạng thái **`CONDITIONAL`** cho đến khi Pháp chế & Kế toán đối chiếu toàn văn `44/2026/VBHN-TT-BTC`.
>
> **Giả định thay cho thông tin đề bài chưa nêu** (đề bài không cho ngân sách, chỉ tiêu, quy mô kênh hay thứ tự ưu tiên):
> - **Ngân sách chi phí phân phối:** trần tự đặt **tổng chi ≤ 75% FYP ở kịch bản xấu nhất**, cộng trần pháp lý Điều 52 TT 67/2023 cho thưởng & hỗ trợ (`CONDITIONAL`).
> - **Quy mô:** 1 Vùng chuẩn 12 tỷ FYP/năm (trang 1–6 của tài liệu này); trang web dùng thêm mô hình 1 khu vực 45 đại lý, 1,2 tỷ FYP/tháng. Không cộng trừ số giữa hai mô hình.
> - **Chất lượng:** K2 82% kịch bản chuẩn, 62% kịch bản xấu.
> - **ROI:** chưa có biên lợi nhuận (VNB) và chi phí vận hành của doanh nghiệp → đo bằng chi phí / FYP, chi phí / phí còn duy trì và ngưỡng hòa vốn mô phỏng.
> - **Ưu tiên:** trọng số 30% Doanh số / 25% Chất lượng / 25% Tài chính / 10% Con người / 10% Triển khai (đổi được, xem độ nhạy trang 6).
> - Có số thật thì thay vào mô hình là tính lại; cấu trúc đề xuất không đổi.
> - **Công cụ tính:** mô hình Excel tham chiếu (14 sheet, công thức mở) phủ 7 văn bản đầu và mô hình Vùng 12 tỷ; phần Chính sách Lai và mô hình khu vực 45 đại lý trên trang web tính bằng Python engine có bộ kiểm thử, chưa đưa vào Excel.

---

## TRẢ LỜI ĐỀ BÀI TRONG 1 TRANG

| Đề bài hỏi | Trả lời ngắn | Con số dẫn chứng (`MODEL_OUTPUT`, 1 Vùng 12 tỷ FYP/năm) | Vì sao hợp Việt Nam | Chi tiết |
|---|---|---|---|---|
| **1. Các công ty trả thu nhập thế nào?** | Ở đại lý cá nhân các hãng trả gần ngang nhau; khác biệt lớn nằm ở **tầng quản lý** — nơi quyết định chi phí và động cơ của cả hệ thống. | Tổng chi toàn cây ở K2 82%: Chubb `99.21%`, AIA `73.44%` FYP; Chubb trả quản lý trực tiếp tới `108% FYC`, AIA có phí cố định lãnh đạo `20–130tr/tháng`. | 3 hãng đều trong top 10 thị phần phí khai thác mới 2024 (Manulife #4, AIA #6, Chubb #10 — `SOURCE_CLAIM`). | Trang 2 |
| **2. Chính sách nào hợp thị trường VN?** | **Balanced Hybrid:** thu nhập đại lý ngang thị trường, nhưng mọi khoản thưởng lớn gắn với K2 và một phần trả chậm 3 năm; cắt chuỗi gián tiếp vô hạn tầng và phí cố định cao. | Override trực tiếp đỉnh `30–36% FYC` (Chubb `108%`); gián tiếp tối đa 3 tầng, khóa nếu nhóm `<15tr FYC/tháng`; trả chậm `30/30/40%` gắn `K2 ≥75%`. | (1) Hợp đồng mới nhỏ đi, >50% là bảo vệ thuần → ngưỡng thưởng thấp, `Top-up = 0%`; (2) Điều 52 TT 67/2023 khóa trần thưởng 20–30% FYP → phải cạnh tranh bằng cấu trúc, không bằng tiền; (3) NĐ 97/2026 yêu cầu nghiệm thu dịch vụ → phí lãnh đạo gắn KPI. | Trang 4–5 |
| **3. Tác động lên doanh số, chất lượng, chi phí?** | **Chất lượng & chi phí đã đo được; doanh số chưa** — cần thí điểm. | Chi phí co giãn theo chất lượng: K2 82% → 62% làm tổng chi giảm từ `59.44%` xuống `45.42% FYP`; chi phí trên mỗi đồng phí còn sống giữ ổn định `72.48% → 73.27%` (Chubb tăng lên `124.42%`). | Thị trường đang trong khủng hoảng niềm tin & K2 → chính sách phải tự “phạt” bán ẩu thay vì trả theo khối lượng. | Trang 3, 6 |

**Doanh số (`HYPOTHESIS`):** mô hình chưa đo được doanh số tăng thêm. Cơ chế kỳ vọng: gói kích hoạt M1–M6 ngưỡng thấp, thưởng tháng 5 bậc mượt, thưởng đều đặn quý. **Cách đo:** thí điểm 3 tháng ở một vùng, so với vùng đối chứng giữ chính sách cũ — FYP trên mỗi đại lý hoạt động, tỷ lệ đại lý hoạt động, K2.

---

## TRANG 1 — TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

### Bối cảnh 2026–2027: Kỷ nguyên "Đốt Quỹ Thưởng Mua Thị Phần" Đã Chấm Dứt
1. **Chuyển dịch thị trường VN (`SOURCE_CLAIM` — IAV/MOF 2024–2026):** Sau giai đoạn giảm sâu (`-13.0%` NBP năm 2024), số lượng hợp đồng mới 8–9T/2026 đã phục hồi (`+2.9% đến +4.3%`), **nhưng tổng phí khai thác mới vẫn giảm (`-10.6% đến -11.7%`)** do kích cỡ hợp đồng (`Case Size`) thu hẹp và **>50% hợp đồng mới dịch chuyển sang Bảo vệ thuần / Tử kỳ**.
2. **Hai gọng kìm pháp lý mới:**
   - **Điều 52 TT 67/2023/TT-BTC (hết lộ trình chuyển tiếp 31/12/2025 → hiệu lực đầy đủ 2026):** Khóa trần tổng chi thưởng & hỗ trợ đại lý khai thác mới ở mức **`≤ 20%` (HĐ ≤1 năm) + `≤ 30%` FYP Năm 1 (HĐ >1 năm)** và **`≤ 7%` phí tái tục** ở cấp toàn danh mục công ty.
   - **Thông tư 96/2026/TT-BTC — `SOURCE CLAIM`:** Bản tóm tắt nêu tỷ lệ hoa hồng Top-up không vượt tỷ lệ phí ban đầu. Phạm vi và mốc áp dụng chờ đối chiếu toàn văn hợp nhất.

### Khuyến nghị Trung tâm: Kiến trúc `Balanced Hybrid` (Cân bằng Doanh số — Chất lượng — Dòng tiền)
- **Định vị:** Kết hợp các cơ chế chứng minh xuất sắc nhất từ cả 3 hãng (Bảo vệ thực chất + Chặn T+1 + Khóa gián tiếp từ Chubb; Kỷ luật tái tục & SYC cao từ AIA; Trả chậm 3 năm `30/30/40%` + Sàn/Trần định phí + Chuyển đổi HKD từ Manulife), đồng thời **loại bỏ 3 nguồn gây vỡ chi phí lớn nhất thị trường** (Direct Override >100% FYC, Phí cố định quá cao kèm chuỗi gián tiếp vô hạn tầng, và thưởng tăng trưởng thuần QoQ).
- **Tác động mô phỏng trên kịch bản 1 Vùng chuẩn (`12 tỷ FYP/năm`, `K2 = 82%`, `MODEL_OUTPUT — KHÔNG PHẢI ROI THỰC TẾ`):** Hạ tổng chi phí phân phối toàn hệ thống mô phỏng xuống **`59.44% FYP`** (chi tiền mặt Năm 1 mô phỏng `54.45% FYP`, thấp hơn `15.99` điểm % so với kịch bản AIA Alpha chưa gồm Exchange/Pro và `44.76` điểm % so với kịch bản Chubb Life trong cùng giả định sản lượng). Rổ thưởng đại lý mô phỏng đạt `5.91% FYP` ở kịch bản năng suất trung bình (`15tr FYC/M`, và dưới `~19% FYP` ở nhóm năng suất cao), giữ biên đệm rộng dưới ngưỡng tham chiếu `30%` của Điều 52 *(cần Pháp chế & Kế toán kiểm chứng phạm vi tính rổ pháp định theo toàn văn `44/2026/VBHN-TT-BTC`)*.
- **Đọc đúng lợi thế chi phí:** so sánh chi phí trong tài liệu này gồm AIA và Chubb; Manulife chỉ công bố được tầng `PSM+/HKD`, nên tài liệu **không kết luận "rẻ nhất thị trường"**. Lợi thế bền của đề xuất là **chi phí co giãn theo chất lượng**: khi K2 rơi từ 82% xuống 62%, tổng chi tự giảm từ `59.44%` xuống `45.42% FYP`, trong khi chi phí trên mỗi đồng phí còn sống đến Năm 2 gần như đứng yên (`72.48%` → `73.27%`) — trang 6.

---

## TRANG 2 — BẢN ĐỒ CHIẾN LƯỢC 3 ĐỐI THỦ (SO SÁNH ĐÚNG TẦNG BẬC)

| Tầng Lực lượng | AIA Việt Nam — Kênh Alpha | Chubb Life — Kênh Đại lý | Manulife Việt Nam (`PSM+/HKD`) |
|---|---|---|---|
| **Triết lý Chiến lược** | **Mở rộng Lực lượng Toàn thời gian & Doanh chủ (`Dual Career`)** — Dồn ngân sách vào tuyển `Exchange Pro` (40%), nhân bản UM (150%), và siết vách đá `FY <70% → 0%` từ 2027. | **Năng suất Biến đổi Cao & Kỷ luật Hành vi (`Champion Hubb`)** — Trả thưởng cực hậu cho AR/AL kỳ cựu bán giỏi, kiểm soát rủi ro bằng T+1 hold, `Top-up = 0%` và `HSBH`. | **Quản trị Vùng Tinh gọn & Giữ chân Dài hạn (`HKD`)** — Văn bản 6 trang cực rõ, định phí có sàn 30%/trần 150%, siết K2 từ 04/2026 và khóa giữ chân bằng trả chậm 3 năm. |
| **Tầng 1: Đại lý Cá nhân** | Đỉnh biến đổi **90% FYC** (Quý 40% + 5S 15% + Năm 20% × FY 120%) + **50% SYC** + 1/72H + 3M + BHSK. *(Thiếu gói trợ cấp Exchange/Pro & biểu HH)*. | Đỉnh **85.8% FYC (AR)** / **109.2% FYC (AL tự bán)** ngay theo tháng–quý + 15% RYC + ĐL mới (36tr) / CH M1–24 (`SOP + 20 FNA`). **Đáy K2 mềm (`<50%` vẫn nhận 25%)!** | *Chưa có tài liệu (`UNKNOWN`)* |
| **Tầng 2: Quản lý Trực tiếp** | Direct Override nền **~51% + 10% trả chậm 3 năm (`TOT ≥85%`)** + Đồng hành **40% Exch Pro** + UM mới **150%** (cap 30tr) + 70% Cap. | Direct Override chạm đỉnh **108% FYC NTT** (100% trả ngay Y1!) + **Phí âm đối xứng khi hủy HĐ** + **Khóa Indirect L1–L3 về 0% nếu NTT `<15tr`**! | *Chưa có tài liệu (`UNKNOWN`)* |
| **Tầng 3: Lãnh đạo Cấp cao** | **Phí cố định 20–130tr/M** (10 bậc, chỉ tiêu 5 năm) + **Dual Career** + **Chuỗi gián tiếp 50% vô hạn tầng** + Thâm niên clawback 12M. | **Nghiệm thu dịch vụ** (trần cố định 45tr/M) + **Tăng trưởng Quý 2.5–27.5% FYC** × **Vách đá K2 `50%→60%` (Q3/2026)** + 10–30% RYC. Bỏ giữ lại 25% mới từ 2026. | **Cơ bản 35/45tr** (`×0–150%`) + Năng suất 6–8% + 1mAA Quý 1–5% + **Trả chậm 3 năm `30/30/40%` (`K2 ≥70%`, cap 420/540tr)** + Chuyển đổi `PSM+ ↔ HKD`. |

---

## TRANG 3 — PHÂN TÍCH ĐÁNH ĐỔI TRÊN 3 TRỤC MỤC TIÊU CỦA CHỊ NHI

### 1. Gia tăng Doanh số (`Growth & Production`)
- **Chubb Life dẫn đầu về lực đẩy ngắn hạn:** Mốc thưởng vào sớm (`5tr FYC/3M`) và chạm đỉnh nhanh (`60tr/3M`), khiến ở mức 15tr FYC/tháng (`K2=75%`), đại lý Chubb nhận **158.5% FYC** so với **131.0% FYC** của AIA Alpha (+27.5 điểm %). Tuy nhiên, thưởng tăng trưởng thuần QoQ tới `27.5%` của RD dễ tạo rủi ro **nén số giữa các quý**.
- **AIA Alpha mạnh về mở rộng hệ thống & MDRT/TOT:** Đổ thưởng cực lớn cho tuyển dụng toàn thời gian (`40% Exchange Pro`), nhân bản UM (`150%`) và đẩy đỉnh thưởng năm lên tới **190% FYC** ở nhóm TOT (`≥1,600tr FYC/năm`).

### 2. Chất lượng Kinh doanh (`Business Quality & Persistency`)
- **Điểm sáng xuất sắc nhất thị trường:**
  1. **Sản phẩm bảo vệ (Chubb Life):** Cắt `Top-up = 0%` ở dòng SP mới và gắn FYC *Tự Do An Phúc* theo **Hệ số Bảo vệ (HSBH)** (`20%–30%`), đi trước TT 96/2026 một bước.
  2. **Phòng thủ dòng tiền & Hành vi (Chubb Life):** Giữ thanh toán sang **T+1** cho đại lý mới / `K2 <60%`, tính **phí âm đối xứng** cho AL khi hủy HĐ, và đo `SOP + 20 FNA` qua ứng dụng Smart Agency.
  3. **Kỷ luật tái tục & Thưởng SYC (AIA Alpha + Manulife):** AIA thưởng **+50% SYC** (5 Sao) và khóa trả chậm CQL bằng `TOT ≥85%`; Manulife siết mạnh hệ số K2 từ 04/2026 (`<50% → K2/2`) và khóa trả chậm 3 năm bằng `K2 ≥70%`.
- **Hai rủi ro chất lượng cần tránh:** Đáy K2 mềm `25%` ở Chubb AR/AL (tạo động cơ chạy khối lượng dù K2 dưới 50%) và cú sốc vách đá đột ngột `<70% → 0%` của AIA 2027 dễ gây gãy lực lượng đại lý trung bình.

### 3. Hiệu quả Chi phí & Dòng tiền (`Enterprise Cost & ROI`)
- **Phát hiện định lượng quan trọng nhất:** Khi xếp chồng đầy đủ tất cả các tầng (Đại lý + Quản lý TT/GT + Vùng) trên cùng 1 Vùng chuẩn **`12 tỷ FYP/năm`** (doanh thu chỉ tính 1 lần):
  - **Chubb Life (`K2=82%`):** Tổng chi phí toàn cây lên tới **`99.2% FYP`** (chi tiền mặt Năm 1 = `99.2%`), và khi K2 tụt xuống `62%`, chi phí trên mỗi đồng phí còn sống đến Năm 2 **tăng vọt lên `124.4%`**!
  - **AIA Alpha (`K2=82%`, chưa tính trợ cấp `Exchange/Pro`):** Tổng chi phí toàn cây **`73.4% FYP`** (`70.4%` tiền mặt Y1); ở `K2=62%` năm 2027 giảm mạnh còn **`52.0% FYP`** nhờ vách đá cắt thưởng.
  - **Manulife (`PSM+` Tầng 3):** Nhờ cơ chế trả chậm 3 năm (`30/30/40%`), giữ lại **~24% dòng tiền ra của tầng lãnh đạo vùng** sang các năm sau và tự động hủy trả nếu K2 tụt dưới 70%!

---

## TRANG 4 — MA TRẬN QUYẾT ĐỊNH CHỌN LỌC (`ADOPT / ADAPT / AVOID`)

| Quyết định | Cơ chế Chính sách Cụ thể | Tác động Trực tiếp |
|---|---|---|
| **`ADOPT` (Áp dụng ngay)** | • `Top-up = 0%` & phân tầng FYC theo **Hệ số Bảo vệ (HSBH)** *(Chubb)*<br>• Trả chậm **T+1** cho ĐL mới / `K2 <65%` & **Phí âm đối xứng** *(Chubb)*<br>• Khóa **Indirect Override = 0%** nếu Nhóm trực tiếp `<15tr/M` *(Chubb)*<br>• **Trả chậm 3 năm (`30/30/40%`)** gắn `K2 ≥75%` + Định phí **Sàn 30% / Trần 140%** + Chuyển đổi **HKD** *(Manulife)*<br>• **Biên bản nghiệm thu dịch vụ** & điều kiện đào tạo bắt buộc *(Chubb RD / NĐ 97/2026)*<br>• Thưởng tái tục **SYC/RYC cao (+15%–30%)** đồng bộ cả 3 tầng *(AIA & Chubb RD)* | Hỗ trợ kiểm soát theo khung pháp lý tham chiếu (`CONDITIONAL`); giảm mạnh áp lực tiền mặt Năm 1 và khóa chặt chất lượng tái tục. |
| **`ADAPT` (Cải tiến cho VN 2026)** | • **Cổng Persistency sàn cứng tại `K2 <60% → 0%`** (thay vì 25% quá mềm của Chubb hay 70% quá sốc của AIA 2027), có lộ trình nâng lên 65% ở Năm 2.<br>• Gói kích hoạt M1–M6 mức vào dễ thở (`≥5–8tr FYC/M` phù hợp Case Size nhỏ), giữ lại **50% trả tại M12** + quy định bù trừ `MAX()` rõ ràng (loại bỏ mâu thuẫn).<br>• Áp thống nhất **Luật 70% Concentration Cap** cho mọi cấp quản lý. | Kích hoạt nhanh đại lý bảo vệ thuần, giảm tỷ lệ sốc rơi rụng năm 1 và ngăn phụ thuộc 1 nhánh lớn. |
| **`AVOID` (Loại bỏ triệt để)** | • Đỉnh Direct Override `108% FYC` & Cá nhân `109.2% FYC` *(Chubb)* → phá vỡ ROI & đe dọa trần Điều 52.<br>• Phí cố định `20–130tr/M` + Dual Career + **Chuỗi gián tiếp 50% vô hạn tầng** *(AIA PAF+)* → phình định phí không kiểm soát.<br>• Thưởng tăng trưởng thuần **QoQ tới 27.5%** *(Chubb RD)* → tạo bẫy nén số giữa các quý.<br>• Tính **6% Top-up** vào chỉ tiêu FYP *(Manulife)* → ngược xu hướng TT 96/2026. | Bảo vệ biên lợi nhuận VNB, giảm rủi ro pháp lý cần thẩm định và tránh rủi ro vận hành/trục lợi. |

---

## TRANG 5 — KIẾN TRÚC CHÍNH SÁCH ĐỀ XUẤT (`W24 BALANCED HYBRID — PROPOSAL`)

### Thiết kế 3 Tầng Đồng bộ (100% Tham số hóa — Định hướng Thiết kế Theo Khung TT 67/2023, NĐ 97/2026 & `44/2026/VBHN-TT-BTC` — `CONDITIONAL` Chờ Đối chiếu Toàn văn Pháp lý)

| Tầng | Cơ chế Thu nhập Đề xuất (`PROPOSAL / SYNTHETIC ASSUMPTION`) | Rổ Pháp lý Tham chiếu & Điểm Kiểm soát |
|---|---|---|
| **Tầng 1: Đại lý Cá nhân** | • **Hoa hồng:** UL/ILP **25%–30%** theo HSBH (Y2: **20%**, Y3+: **10%**); **Top-up = 0%**; Tử kỳ/Riders bảo vệ trả cạnh tranh.<br>• **Kích hoạt M1–M6:** `1.5tr` tiền mặt + `1.5tr` **giữ đến M12** khi đạt `≥8tr FYC/M`, ACK ≤15d & qua 21 ngày (tối đa 18tr).<br>• **Thưởng Tháng mượt (5 bậc):** `5/12/22/35/≥55tr FYC` → **`8% / 16% / 24% / 32% / 38%`** × **`K2`** (`<60%: 0%` → `≥85%: 120%`).<br>• **Đều đặn Quý:** `+12%` thưởng tháng khi đạt `3/3` tháng hoạt động (`≥4tr FYC/M`).<br>• **Thưởng MDRT Năm (`≥400tr FYC`):** `+10% FYC` (**30% trả chậm sang Năm 2** khi `K2 ≥75%`).<br>• **Thưởng Tái tục:** **`+25% SYC`** khi `K2 ≥75%`. **Giữ T+1** nếu mới / `K2 <65%`; **Clawback 6M**. | **Tham chiếu Điều 51 & Điều 52 (`CONDITIONAL`):** Rổ thưởng đại lý mô phỏng giữ trong vùng `~5.9%–19% FYP`, tạo biên đệm rộng so với mốc `30%` Điều 52; cần xác nhận phân loại kế toán pháp định trước khi ban hành. |
| **Tầng 2: Quản lý Trực tiếp** | • **Direct Override:** Đỉnh **`30%–36% FYC NTT`** × `K2` + **Phí âm đối xứng khi hủy HĐ**.<br>• **Indirect Override (Tối đa 3 tầng: `35% / 17.5% / 8.75%`):** **Khóa `0%` nếu `FYC NTT < 15tr/M`** + **70% Cap**.<br>• **Tuyển dụng & Nhân bản UM:** `10% FYC` người mới (50% trả tại M12) + `+100%` UM mới 12M (cap 15tr/M, `K2 ≥75%`).<br>• **Thưởng Giữ chân 3 Năm (Deferred):** **`12% FYC NTT/năm`**, trả rải **`30% (Y+1) – 30% (Y+2) – 40% (Y+3)`** gắn `K2 ≥75%`.<br>• **Thưởng RYC Nhóm:** `+15% RYC NTT` (`K2 ≥70%`). | **NĐ 97/2026:** HĐDV Quản lý có nghiệm thu KPI; chặn quản lý ăn bám và khóa giữ chân 3 năm. |
| **Tầng 3: Lãnh đạo Vùng / HKD** | • **Cơ bản KPI Nghiệm thu:** `35tr / 45tr` × `%FYP` × `125%` (**Sàn 30% / Trần 140%**) + nghiệm thu `≥3 lớp đào tạo/M`.<br>• **Override Vùng:** `7% FYC` trực tiếp × `K2` + `40%` gián tiếp (tối đa 2 tầng) + `15%–30% RYC`.<br>• **Hợp tác Dài hạn 3 Năm:** `60%` Override Vùng biến đổi (cap 12×), trả **`30/30/40%`** gắn `K2 ≥75%` + **Linh hoạt chuyển đổi `Cá nhân ↔ HKD`**. | **NĐ 97/2026:** Chi tiền mặt Năm 1 thấp, không phình định phí, tối ưu pháp nhân thuế. |

*(Hai biến thể điều chỉnh nhanh trên cùng mô hình Excel: **Growth-Tilted** cho DN cần mở rộng thị phần nhanh; **Quality & Cash-First** cho DN ưu tiên cải thiện K2 & vốn).*

---

## TRANG 6 — BẰNG CHỨNG ĐỊNH LƯỢNG: CHI PHÍ TOÀN HỆ THỐNG, DÒNG TIỀN & ĐIỂM HÒA VỐN VNB

*(Kết quả mô phỏng đồng nhất trên Python & Excel Reference Model cho 1 Vùng chuẩn = **12 tỷ FYP/năm = 3.6 tỷ FYC**, 20 Đại lý × 15tr FYC/M, 4 Quản lý trực tiếp, 1 Lãnh đạo Vùng — Doanh thu chỉ tính 1 lần, không tính trùng).*

| Chính sách *(1 Vùng 12 tỷ FYP)* | Persistency (`K2 / FY`) | Tổng Chi phí Toàn cây (`% FYP`) | Chi tiền mặt Năm 1 (`% FYP`) | Quỹ Thưởng ĐL (`Trần Đ.52 ≤30%`) | Chi phí / 1đ Phí sống Năm 2 (`%`) | **Break-Even Gross Margin** *(OpEx giả định 20%)* |
|---|---:|---:|---:|---:|---:|---:|
| **Chubb Life Agency 2026** | **82%** | `99.21%` | `99.21%` | `21.06%` *(ĐL top sát trần!)* | `120.99%` | `119.21%` |
| **AIA Alpha 2026** *(chưa gồm Exch/Pro)* | **82%** | `73.44%` | `70.44%` | `10.23%` | `89.57%` | `93.44%` |
| **W24 Proposed Balanced (`PROPOSAL`)** | **82%** | **`59.44%`** | **`54.45%`** | **`5.91%` (dưới ngưỡng mô phỏng)** | **`72.48%`** | **`79.44%`** |
| **Chubb Life Agency 2026** | **62%** | `77.14%` | `77.14%` | `13.16%` | **`124.42%`** *(tệ hơn 82%!)* | `97.14%` |
| **AIA Alpha 2027 (Vách đá `<70%`)** | **62%** | `51.98%` | `51.98%` | `0.00%` | `83.84%` | `71.98%` |
| **W24 Proposed Balanced (`PROPOSAL`)** | **62%** | **`45.42%`** | **`45.42%`** | **`3.23%` (dưới ngưỡng mô phỏng)** | **`73.27%`** *(siêu ổn định!)* | **`65.42%`** |

### 3 Kết luận Tài chính Mô phỏng & Giới hạn ROI cho Ban Lãnh đạo
1. **Phân biệt rạch ròi `Modeled Distribution Cost / Break-Even` với `Actual ROI (UNKNOWN)`:** Mô hình hiện chứng minh **ngưỡng hòa vốn biên gộp cần thiết (`Modeled Break-Even Gross Margin`)** và **chi phí trên mỗi đồng phí còn sống đến Năm 2** trên kịch bản chuẩn, **chưa phải ROI thực tế đã chứng minh** (vì chưa có `VNB Margin`, `OpEx` và tỷ lệ thực tế của doanh nghiệp đích). Khi `K2` tụt từ 82% xuống 62%, chi phí mô phỏng trên mỗi đồng phí còn sống đến Năm 2 ở mô hình đáy mềm (Chubb) tăng lên `124.42%`, trong khi **W24 Proposed Balanced** giữ ổn định trong dải hẹp `69.36% – 73.27%`.
2. **Tác động Dòng tiền Năm 1 mô phỏng:** Nhờ cơ chế trả chậm 3 năm (`30/30/40%`), chi tiền mặt Năm 1 mô phỏng giảm xuống **`54.45% FYP`** (thấp hơn `15.99` điểm % so với kịch bản AIA và `44.76` điểm % so với kịch bản Chubb ở cùng giả định), giúp giảm áp lực vốn lưu động đầu kỳ.
3. **Điểm đánh giá thiết kế đa tiêu chí (15 tiêu chí, bộ trọng số 30/25/25/10/10 — `DRAFT, NOT INDEPENDENTLY CALIBRATED`):** **W24 Proposed Balanced đạt `4.41 / 5.0`** (cổng pháp lý `CONDITIONAL` chờ đối chiếu toàn văn `44/2026/VBHN-TT-BTC`) so với AIA Alpha (`3.54 / 5.0`) và Chubb Life (`3.39 / 5.0`), dẫn đầu ổn định trên cả 4 kịch bản độ nhạy trọng số.

---

## TRANG 7 — LỘ TRÌNH TRIỂN KHAI 90 NGÀY & ĐIỂM CẦN BAN LÃNH ĐẠO QUYẾT ĐỊNH

### Lộ trình Triển khai & Kiểm chứng An toàn (3 Giai đoạn — 90 Ngày)
1. **Ngày 1–30 (Hiệu chuẩn Pháp lý & Tài chính Nội bộ):**
   - Đối chiếu bản toàn văn Công báo của TT 67/2023 (Điều 51, 52), NĐ 97/2026 & TT 96/2026 với bộ phận Pháp chế & Actuarial.
   - Nạp dữ liệu thực tế của doanh nghiệp (`VNB Margin`, `Home Office OpEx`, phân bổ năng suất đại lý & đường cong K2 lịch sử) vào Excel Reference Model để chốt tham số cuối cùng (chọn giữa `Balanced`, `Growth-Tilted`, hoặc `Quality-First`).
2. **Ngày 31–60 (Mô phỏng Hồi tố — Back-testing & Pilot):**
   - Chạy **Back-testing** trên dữ liệu 12 tháng gần nhất của toàn bộ lực lượng đại lý hiện hữu để đo chính xác nhóm "tăng thu nhập" vs "giảm thu nhập" (kiểm soát rủi ro rời bỏ ở nhóm `K2 60%–69%`).
   - Thiết kế hệ thống nghiệm thu dịch vụ số hóa (NĐ 97/2026) và quy trình chuyển đổi `HKD`.
3. **Ngày 61–90 (Truyền thông, Đào tạo & Chuyển tiếp Không sốc):**
   - Ban hành tài liệu chính sách tinh gọn (**≤ 15 trang**, không mâu thuẫn nội tại, công cụ giả lập thu nhập cho đại lý).
   - Áp dụng **lộ trình chuyển tiếp 6 tháng** trước khi khóa sàn cứng `K2 = 60%` và chốt lịch triển khai sau khi xác minh điều khoản chuyển tiếp.

### 4 Quyết định Cần Ban Lãnh đạo / Chị Nhi Xác nhận cho Bước 2
1. **Ưu tiên chiến lược (Trọng số):** Xác nhận bộ trọng số ưu tiên (`30% Doanh số / 25% Chất lượng / 25% Tài chính / 10% Con người / 10% Triển khai`) hay muốn nghiêng mạnh hơn về Growth hoặc Quality?
2. **Mức độ chấp nhận định phí & Khẩu vị đầu tư Toàn thời gian:** Có triển khai nhánh đại lý toàn thời gian (gói hỗ trợ gắn `SOP + FNA` giữ lại M12) song song với nhánh truyền thống hay tập trung một khung chuẩn?
3. **Cung cấp đầu vào Tài chính & Đối thủ bổ sung:** Chia sẻ giả định biên sản phẩm (`VNB Margin` / `OpEx`) của doanh nghiệp và bổ sung chính sách AIA Exchange (chính sách Đại lý Manulife đã có, đang so sánh trên trang web; nếu cần tinh chỉnh cạnh tranh tuyển dụng trực tiếp).
4. **Phê duyệt chuyển sang Bước 2:** Mở rộng sang **MAPA chi tiết theo cohort, Kế hoạch Marketing Tuyển dụng & Tìm kiếm Khách hàng, và HTML Interactive Simulator** cho PO tự tinh chỉnh tham số.
