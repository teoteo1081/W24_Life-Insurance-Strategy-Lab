# Comprehensive Competitor Benchmarking — 12 Phương pháp & Ma trận Tổng Thu nhập (v2.0 Post-Audit)

**Ngày lập:** 2026-11-26 (Kế thừa và nâng cấp từ `competitor-comparison-v1.0.md` sau Independent Audit)  
**Cơ sở Ground Truth:** 7 tài liệu chính sách chính thức (`116 trang`, `SHA-256` đã kiểm chứng), 112 quy tắc (`business-rules-catalog.csv`), 3 bảng lookup chuẩn hóa (`1,300` dòng PAF+, `113` dòng Hoa hồng Chubb, `10` khung tuổi HSBH), 36 chức danh (`role-organization-mapping.csv`), và 44 cấu phần (`total-rewards-inventory.csv`).  
**Nhãn phạm vi bắt buộc:** `BASED ON AVAILABLE POLICY DOCUMENTS` — Mọi nhận định về kết quả kinh doanh thực tế (Active Ratio thực, K2 thực, VNB margin thực) đều là `UNKNOWN` hoặc `HYPOTHESIS`, tuyệt đối không suy diễn từ thiết kế chính sách thành hiệu quả đã chứng minh.

---

## 0. Tóm tắt Bản đồ Phủ dữ liệu Trước khi So sánh

| Tầng Chức năng | AIA Alpha | Chubb Life Agency | Manulife Việt Nam | Mức độ Đủ dữ liệu |
|---|---|---|---|---|
| **Tầng 1 — Đại lý Cá nhân** | `SA` (rõ thưởng; thiếu biểu HH & `Exchange/Pro`) | `AR` + `Champion Hubb` (rõ full 113 dòng HH + thưởng; thiếu ngưỡng `1 EHC` & `K2`) | **`UNKNOWN`** *(thiếu toàn bộ)* | 2/3 hãng (so trực diện trên `% FYC`; quy đổi `% FYP` có ghi nhãn `ASSUMPTION`) |
| **Tầng 2 — Quản lý Trực tiếp / Cấp trung** | `UM/SUM/DM/SDM` (rõ 100% công thức thưởng) | `AL: UM/SM/DM` + `CH QL` (rõ công thức; thiếu `260009V`) | **`UNKNOWN`** *(thiếu toàn bộ)* | 2/3 hãng |
| **Tầng 3 — Lãnh đạo Khối / Vùng Cấp cao** | `PAF → SPVP` (rõ 10 bậc + 1,300 dòng chỉ tiêu 5 năm) | `RD` (rõ 6/8 khoản; thiếu policy `BD` cho mục II.7–8) | `PSM/SM/PSSM/SSM` & `HKD1–4` (rõ 4 khoản; thiếu bảng chỉ tiêu & `C.1` từ 02/2026) | **Đủ cả 3 hãng** *(có điều kiện về bảng chỉ tiêu & BD)* |

---

## 1. Thực thi Đầy đủ 12 Phương pháp Benchmarking (Section 15)

### Phương pháp 01 — Component Benchmarking (Đối chiếu Danh mục Cấu phần A–H)
- **Mục tiêu:** Nhận diện cấu phần nào đối thủ có/không có trên toàn dải Total Rewards (A–H), tránh "mù chi phí ẩn".
- **Dữ liệu cần:** `total-rewards-inventory.csv` (44 cấu phần × 33 trường metadata).
- **Phương pháp:** Ánh xạ từng cấu phần vào 8 nhóm A–H theo tầng chức năng.
- **Giới hạn:** Thiếu chính sách FA/UM Manulife, gói trợ cấp Exchange/Pro AIA, và chi phí DN cho 3 phúc lợi phi tiền mặt (`Unpriced_Non_Cash_Benefit`).
- **Kết quả (`VERIFIED FACT`):**
  - **AIA Alpha** có độ phủ cấu phần rộng nhất (21 cấu phần): nổi bật ở kích hoạt 1/72H, thưởng đồng hành tuyển dụng 40% (`Exchange Pro`), thưởng SYC cao (+50%), CQL trả chậm 3 năm (`TOT ≥85%`), phí cố định `PAF+` 10 bậc (20–130tr/M) kèm Dual Career, và 2 phúc lợi phi tiền mặt (Chuyến HL 3M + BHSK 1 năm).
  - **Chubb Life** có cấu trúc **biến đổi ngắn hạn dày nhất** ở Tầng 1–2 (18 cấu phần): thưởng HQKD tháng nhân chồng quý (+30% AR / +50% AL), Champion Hubb M1–24 có giữ lại M12 + chuyển sang RYC năm 2, và RD có 8 khoản phí nghiệm thu + thưởng tăng trưởng QoQ/YoY (27.5% FYC) + BHSK & Tai nạn RD.
  - **Manulife (`PSM+/HKD`)** có thiết kế **tinh gọn nhất ở Tầng 3** (chỉ 4 khoản phí dịch vụ trong 6 trang memo): Phí cơ bản 35/45tr gắn KPI FYP (sàn 30%, trần 150%), Năng suất tháng 6–8%, Hoạt động quý 1–5% (`1mAA_4mFYC`), và Hợp tác dài hạn 3 năm (`30/30/40%`).

---

### Phương pháp 02 — Metric & Definition Normalization (Chuẩn hóa Định nghĩa Nền tảng)
- **Mục tiêu:** Loại trừ sai lệch "táo so với cam" khi mỗi hãng định nghĩa `FYP`, `FYC`, `Active`, `Persistency`, `Direct Team` khác nhau.
- **Dữ liệu cần:** Điều khoản định nghĩa của 7 memo.
- **Giới hạn:** Thiếu memo `FYC Tín Chỉ` (AIA), `0016M03/2024` (TLDTHD Manulife), `CHH0DCEB260005V` (`EHC`, `K2/P13` Chubb).
- **Kết quả (`VERIFIED FACT`):**

| Chỉ số nền tảng | AIA Alpha | Manulife `PSM+/HKD` | Chubb Life Agency | Hệ quả điều chỉnh khi so sánh |
|---|---|---|---|---|
| **Phí đóng thêm (Top-up) vào FYP** | **0%** (loại trừ hoàn toàn) | **+6%** vào FYP (`p.6`) | **0%** (SP mới & tính tăng trưởng RD) | Manulife dễ đạt chỉ tiêu FYP hơn nếu danh mục có nhiều Top-up; cần rà soát trước TT 96/2026! |
| **Phí đóng 1 lần (Single Premium)** | **10%** vào FYP | **6%** vào FYP | **10%** vào tăng trưởng FYP RD; hoa hồng 7% | Khác biệt trọng số 6% vs 10%. |
| **Cơ sở thưởng cá nhân/quản lý** | `FYC Tín Chỉ` (chưa rõ hệ số quy đổi) | `FYC thực thu` | `FYC thực thu` (full 113 dòng: UL 20–30%, KHTC TL ko QL TV 27%, Cao niên 20%) | So sánh chính xác nhất là trên **`% FYC`**. Khi quy sang `% FYP`, phải gắn nhãn `ASSUMPTION` (ví dụ 30% UL chuẩn). |
| **Đại lý Phục vụ (`SE / SA`) trong `Active`** | **`SE` bị LOẠI** khỏi `1mAA`; Exchange/Pro tính **×2** cho PAF+ | **`SA` ĐƯỢC TÍNH** vào `1mAA_4mFYC` (`≥4tr FYC`) | `EHC` / `3MAA` *(ngưỡng tiền `UNKNOWN`)*; CH yêu cầu `1 CC ≥ 15tr FYP` | Không được coi 1 `1mAA` AIA = 1 `1mAA` Manulife = 1 `EHC` Chubb mà không ghi giả định chuẩn hóa! |
| **Doanh số bản thân Quản lý trong `FYC NTT`** | **BAO GỒM** bản thân CQL (`002 p.13`) | Khu vực trực tiếp (không có khái niệm bán lẻ) | **LOẠI TRỪ** bản thân AL (`002 p.5`) | Cùng 1 mức FYC nhóm, AL Chubb phải tự bán tách riêng (hưởng đỉnh 109.2%) và dẫn dắt đội bán riêng (hưởng đỉnh 108%)! |
| **Làm tròn Persistency** | `CONFLICTING_EVIDENCE` (`ERR-DOC-02`: 0 chữ số — RoundUp p.14 vs HalfUp p.21) | `UNKNOWN` (`0016M03/2024`) | **2 chữ số thập phân** (`0003V p.13`) | Phải chạy độ nhạy 2 chế độ làm tròn cho AIA ở vùng biên `69.1%–69.5%`. |

---

### Phương pháp 03 — Threshold, Tier & Cliff Analysis (Phân tích Ngưỡng, Bậc thang & Vách đá)
- **Mục tiêu:** Đánh giá độ dốc kích thích sản lượng, điểm nhảy bậc (cliff/step), và vùng chết (dead zone) của từng chính sách.
- **Kết quả (`VERIFIED FACT`):**
  - **Tầng 1 (Đại lý):** Chubb Life có **mốc vào rất thấp** (`5tr FYC/3M` tức ~1.67tr/tháng đã nhận 7.5%) và **chạm đỉnh sớm** (`≥60tr FYC/3M` tức 20tr/tháng đã chạm 55% tháng → 85.8% cả quý!). Ngược lại, AIA Alpha bắt đầu ở `16tr/quý` (4%) và chỉ chạm đỉnh `40% + 15%` tại `≥150tr FYC/quý` (gấp **2.5 lần** ngưỡng đỉnh của Chubb!) cộng thêm mốc Năm lên tới **`1,600tr FYC/năm` (20%)**.
  - **Tầng 2 (Quản lý):** Chubb Life dùng **ngưỡng thâm niên kép** (`<15M` bị ghìm ở 25%/35%, `≥15M` mở 50%/60%) và **vách đá cứng NTT <15tr → 0% toàn bộ gián tiếp L1–L3**. AIA Alpha chia 4 bậc mềm hơn (`<7 / 7 / 20 / ≥50tr`), không khóa gián tiếp bằng doanh số NTT mà bằng duy trì chức danh + hạn đồng cấp 12/18/24M.
  - **Tầng 3 (Lãnh đạo Cấp cao):**
    - AIA `PAF+` có vùng an toàn rộng cho Phí cố định (`55%–115% FYP` đều hưởng `100%` phí cố định; `<35%` mới về `0%`).
    - Manulife `PSM+/HKD` dùng công thức **tuyến tính có sàn–trần** (`%FYP × 130%`, sàn `30%`, trần `150%` đạt ở `115.4% FYP`) → ít bị "đứng hình" giữa bậc hơn AIA!
    - Chubb `RD` dựng **vách đá K2 nhị phân cực sắc (`0%` hoặc `100%`)** nâng từ `50%` (Q1–Q2) lên **`60%` (từ Q3/2026)** cho cả phí tháng 3MAA lẫn thưởng tăng trưởng quý 27.5%!

---

### Phương pháp 04 — Formula, Multiplier & Compounding Mechanics (Phân tích Cơ chế Nhân chồng & Bù trừ)
- **Mục tiêu:** Phát hiện các công thức nhân chồng (compounding) tạo hiệu ứng chi phí phi tuyến hoặc bẫy hành vi.
- **Kết quả (`VERIFIED FACT`):**
  1. **Nhân chồng 3 lớp ở Chubb Life (`AR & AL`):** `Thưởng Quý = Thưởng Tháng × (1 + 30% [AR] / +50% [AL])` mà Thưởng Tháng đã nhân `Hệ số K2 (tới 120%)`. Hệ quả toán học: tỷ lệ biến đổi đạt đỉnh **`85.8% FYC` (AR)**, **`109.2% FYC` (AL bán cá nhân)**, và **`108.0% FYC NTT` (AL quản lý trực tiếp)**!
  2. **Chuỗi Gián tiếp Vô hạn Tầng ở AIA `PAF+`:** `50% × 50% × 50%...` trên toàn cây nhánh. Theo chuỗi hình học `Σ(0.5^k) = 1.0`, tổng chi phí override gián tiếp trên một khối cơ sở có thể tiến tới **+100% của chính khoản phí trực tiếp đó** khi cây có 5–7 tầng PAF+ (đúng như ví dụ `AF8 → President` trang 4 của `2601-035`).
  3. **Bù trừ hai tầng thông minh của Chubb Champion Hubb (`0007V p.10`):** Không trả trùng với Thưởng ĐL mới; khấu trừ `NewAgentBonus` vào **tiền mặt tháng trước**, phần dư mới trừ vào **cục giữ lại M12** (`CH_Month_Net = MAX(0, CH_M*W1 - NewAgent)`, `CH_M12_Net = MAX(0, CH_M12*W1 - MAX(0, NewAgent - CH_M*W1))`).
  4. **Clawback đối xứng (Symmetric Negative FYC) ở Chubb AL (`0008V p.5`):** Khi `FYC NTT < 0` do hủy hợp đồng, vẫn nhân tỷ lệ theo trị tuyệt đối `|FYC NTT|` để ghi **phí dịch vụ âm** — cơ chế phòng thủ cực tốt ít hãng có.

---

### Phương pháp 05 — Pay Mix Benchmarking (Cơ cấu Cố định vs. Biến đổi Ngắn hạn vs. Dài hạn/Trả chậm)
- **Mục tiêu:** So sánh tỷ trọng rủi ro định phí (fixed burn) và khả năng giữ chân bằng trả chậm giữa các hãng.
- **Kết quả (Tổng hợp từ mô phỏng kịch bản chuẩn trên Engine W24 — `MODEL_OUTPUT`):**
  - **Tầng 1 (Đại lý phổ thông):** Cả AIA Alpha (`SA`) và Chubb (`AR`) đều **0% cố định thuần** (chỉ có thưởng kích hoạt M1–M3 hoặc CH gắn điều kiện CC/SOP). Chubb thiên nặng về **biến đổi tháng–quý (chi trả ngay trong Y1)**, còn AIA trải đều sang **thưởng năm & SYC năm 2** (chưa kể gói trợ cấp `Exchange/Pro` bị `UNKNOWN`).
  - **Tầng 2 (Quản lý trực tiếp):** Chubb `AL` gần như **100% biến đổi trả ngay** (chỉ khóa M7–12 của phí tuyển dụng 10%). AIA `CQL` tách một phần đáng kể (**5%–10% FYC năm**) sang **trả chậm 3 năm (2028–2030)** gắn `TOT ≥85%`.
  - **Tầng 3 (Lãnh đạo Cấp cao — So đủ 3 hãng):**
    - **AIA `PAF+`:** Tỷ trọng cố định/KPI rất lớn (`20–130tr/M`), cộng Dual Career + biến đổi tháng/quý + thưởng vượt chỉ tiêu M12 (clawback 12M).
    - **Manulife `PSM+/HKD`:** Cân bằng nhất — khoảng **40%–48% Phí cơ bản KPI (sàn 30%/trần 150%)**, **30%–35% Biến đổi tháng/quý**, và **20%–25% Trả chậm 3 năm (`30/30/40%`)**.
    - **Chubb `RD`:** Cố định nghiệm thu bị chặn trần **45tr/M** (thấp hơn Manulife 52.5–67.5tr và AIA 50–130tr), phần lớn bứt phá nằm ở **biến đổi tăng trưởng quý (đến 27.5% FYC)** và **RYC (đến 30%)** — nhưng từ 2026 **không còn khoản giữ lại 25% mới**!

---

### Phương pháp 06 — Quality, Persistency & Anti-Gaming Benchmarking (So sánh Kỷ luật Chất lượng)
- **Kết quả (`VERIFIED FACT`):**

| Khía cạnh Chất lượng | AIA Alpha | Manulife `PSM+/HKD` | Chubb Life Agency |
|---|---|---|---|
| **Đáy Persistency (Penalty Floor)** | **2026:** mềm (`%FY`); **2027:** **Vách đá `<70% → 0%`** (CVTV); PAF+ `<50% → 0%`. | **Từ 04/2026:** **`<50% → K2/2`** (chia đôi); `<70%` mất sạch dài hạn 3 năm! | **AR/AL:** mềm đáy (`<50%` vẫn nhận **25%**!); **CH M13–24:** `<50% → 0%`; **RD:** **Vách đá nhị phân `50% (Q1–2) → 60% (Q3+)`!** |
| **Thưởng Tái tục (SYC/RYC)** | **Rất mạnh:** `+30% / +50% SYC` (4S/5S) | Không tách thưởng RYC riêng trong `0048M01` | **Mạnh & đều 3 tầng:** AR/AL `10%–15% RYC (Y2–5)`, CH Y2 `20% RYC × W2 (tới 125%)`, **RD `10%–30% RYC`**. |
| **Chặn dòng tiền & Thu hồi (Clawback)** | Thu hồi toàn bộ HH/thưởng **6 tháng** kể cả đã nghỉ; PAF+ thâm niên **clawback 100% trong 12M**. | Clawback vi phạm kể cả sau chấm dứt HĐ (`C.11`); khóa trả chậm 3 năm bằng `K2 ≥70%`. | **Trả chậm sang T+1 cho K2 <60% / ĐL mới**; **phí âm đối xứng** cho AL; 9 diện tạm giữ RD. |
| **Chống trục lợi sản phẩm (Top-up/HSBH)** | Top-up = 0% FYP | **Điểm yếu cần lưu ý:** FYP vẫn tính **6% Top-up**! | **Xuất sắc:** Top-up = **0% HH** ở SP mới + *Tự Do An Phúc* phân tầng FYC theo **HSBH** (`20%–30%`). |

---

### Phương pháp 07 — Behavior, Governance & Compliance Benchmarking (Kiểm soát Hành vi & Quản trị)
- **Kết quả (`VERIFIED FACT`):**
  - **Chubb Life** dẫn đầu về **kiểm soát hành vi đầu vào có đo lường số hóa**: Champion Hubb ép kỷ luật `SOP 9h–11h (3 buổi/tuần)` + `20 FNA/tháng` trên Smart Agency + phạt bồi hoàn cả AL nếu AR gian lận FNA; `AL` thiếu khóa **MAP** bị giáng bậc ngay; `RD` buộc nộp **Biên bản nghiệm thu dịch vụ** & đứng lớp `≥4 lớp (≥4 HV)/tháng`.
  - **AIA Alpha** dùng **chấm công (`≥50%` CQL / `≥70%` PAF+)**, **ACK 15 ngày** (ngoại lệ T01/2026: 28/02/2026), **Vitality hạng Vàng** cho thăng cấp PAF+, và cơ chế **tạm giữ 100% thu nhập Dual Career** nếu PAF+ thiếu khóa học.
  - **Manulife** có lợi thế **quản trị pháp nhân & thuế (`PSM+ ↔ HKD`)**, nhưng tồn tại **rủi ro điều khoản mở `C.1`** (yêu cầu hoạt động dịch vụ từ 02/2026 chưa có văn bản kèm theo).

---

### Phương pháp 08 — Lifecycle, Career Path & Retention Lock-in Benchmarking (Vòng đời & Giữ chân)
- **Kết quả (`VERIFIED FACT`):**
  - **Giai đoạn Onboarding (M1–M12):** AIA dùng 2 cú hích nhanh (1/72H + Đồng hành 3M + Chuyến HL 3M) và đổ thưởng cực lớn cho CQL tuyển `Exchange Pro` (40% × 12M). Chubb dùng cơ chế **24 tháng có giữ lại M12** (Champion Hubb) hoặc M3/6/12 (cap 36tr) + **khóa cục M7–12 phí tuyển dụng vào điều kiện người giới thiệu phải lên UM**!
  - **Giai đoạn Phát triển Quản lý:** AIA trả **150% (cap 30tr/M)** khi nhân bản UM mới — lực đẩy thăng cấp cực mạnh. Chubb trả **+100% phí gián tiếp** (cap 15tr UM / 30tr SM) nhưng đòi AL mẹ phải duy trì `EHC NTT ≥ 2/3/4`.
  - **Giai đoạn Giữ chân Lãnh đạo (Year 2–5):** **Manulife (`PSM+/HKD`)** và **AIA (`CQL`)** sở hữu "còng tay vàng" tốt nhất thị trường nhờ **3-year deferred vesting** (`30/30/40%` ở Manulife với `K2 ≥70%`; `15/25/60%` ở AIA CQL với `TOT ≥85%`). Chubb Life từ 2026 đã bỏ giữ lại 25% mới của RD nên mức khóa giữ chân dài hạn ở tầng RD thấp hơn Manulife.

---

### Phương pháp 09 — Total Compensation Matrix by Role (Ma trận Quyền lợi & Ma trận Kịch bản 12 Tháng)

#### 9A. Ma trận Quyền lợi Lý thuyết (Entitlement Matrix — Đỉnh & Đáy theo Văn bản Gốc)

| Vai trò Chuẩn | AIA Alpha (2026 → 2027) | Chubb Life Agency (2026) | Manulife (`PSM+/HKD` Post-04/2026) |
|---|---|---|---|
| **Tầng 1: Đại lý Cá nhân** | Biến đổi: `0%` → **`90.0% FYC`** (40% Q + 15% 5S + 20% Y × 120% FY) + `50% SYC` + 1/72H + 3M + BHSK (`Unpriced`) + `Exchange/Pro` (`UNKNOWN`) | Biến đổi: `0%` → **`85.8% FYC`** (AR ≥13M: 55% × 120% × 1.3) \| **`109.2% FYC` (AL bán cá nhân!)** + `15% RYC` + ĐL mới 36tr / CH M1–24 (`MAX`) | **`UNKNOWN`** |
| **Tầng 2: Quản lý Trực tiếp** | Trực tiếp: `8%` → **`61.0% FYC NTT`** (24% M + 12% Act + 15% Q + **10% Y trả chậm 3Y**) + Đồng hành **40% Exch Pro** + UM mới **150%** (cap 30tr) + GT **50/25/12.5%** | Trực tiếp: `0%` → **`108.0% FYC NTT`** (AL ≥15M: 60% × 120% × 1.5) + Tuyển 10% (M7–12 khóa UM) + GT **0% (<15tr) / 30–50% L1** + UM/SM mới +100% + `15% RYC` | **`UNKNOWN`** |
| **Tầng 3: Lãnh đạo Cấp cao** | Cố định `20–130tr/M` (×0–120%) + TT `0–10.7% M` & `0–9.5% Q` + **Chuỗi GT 50% vô hạn** + Thâm niên `4–6% vượt FYP` (cap 12M, clawback 12M) + **Dual Career** | Cố định nghiệm thu `0–45tr/M` + TT `2–12% M` + **Tăng trưởng `2.5–27.5% Q`** (K2 Cliff `50%→60%`) + `10–30% RYC` + BD/RD con `12.5–50%` + BHSK (`Unpriced`) | Cơ bản `35/45tr` (`×0–150%` = `52.5/67.5tr`) + TT `6–8% M × K2` + `1–5% Q × K2` + GT `50%` + **Dài hạn 3Y `75% TT + 25% GT` (cap 420/540tr)** |

#### 9B. Ma trận Kịch bản Chi trả 12 Tháng (Scenario Payout Matrix — Chuẩn hóa cùng Sản lượng & Chất lượng)
*(Các con số dưới đây khớp 100% với Python Engine `model/compensation/compensation_engine.py` và Excel Reference Model `outputs/working/W24_Compensation_Reference_Model_v1.xlsx`; giả định chuẩn hóa sản phẩm UL 30% FYC khi quy đổi `% FYP` cho AIA được gắn nhãn `ASSUMPTION`; không bao gồm trợ cấp `Exchange/Pro` bị `UNKNOWN` và phúc lợi phi tiền mặt `Unpriced`).*

| Hồ sơ Kịch bản (12 Tháng — Cùng Sản lượng & Chất lượng) | AIA Alpha 2026 (`% FYC` / `% FYP*`) | AIA Alpha 2027 (`% FYC` / `% FYP*`) | Chubb Life 2026 (`% FYC` / `% FYP`) | Manulife `PSM+` 2026 | Nhận xét Chênh lệch Trực tiếp |
|---|---:|---:|---:|---:|---|
| **A01 — Đại lý Mới Khá** *(10tr FYC/M = 120tr/Y, 12M, 2 CC/M, K2/FY=80%, không CH)* | **124.0% FYC** *(37.2% FYP)* | **123.3% FYC** *(37.0% FYP)* | **173.3% FYC** *(52.0% FYP)* | `UNKNOWN` | Chubb cao hơn AIA **+49.3 điểm % FYC** nhờ bậc HQKD tháng sớm + ĐL mới 20% (cap 36tr). |
| **A03 — Đại lý Chuẩn Trung bình** *(≥13M, 15tr FYC/M = 180tr/Y, FY/K2=75%)* | **131.0% FYC** *(39.3% FYP)* | **131.0% FYC** *(39.3% FYP)* | **158.5% FYC** *(47.6% FYP)* | `UNKNOWN` | Ở mức 15tr FYC/M, Chubb vẫn vượt trội +27.5 điểm % FYC & trả ngay từng tháng. |
| **A04 — Đại lý Rủi ro Chất lượng Thấp** *(≥13M, 20tr FYC/M = 240tr/Y, **FY/K2=65%**)* | **128.8% FYC** *(38.6% FYP)* | **100.0% FYC (0% thưởng!)** | **153.6% FYC** *(46.1% FYP)* | `UNKNOWN` | **Tương phản cực mạnh:** AIA 2027 cắt sạch thưởng về 0% ở FY=65%, còn Chubb vẫn trả tới **+53.6% thưởng trên FYC**! |
| **A05 — Đại lý Siêu sao MDRT** *(≥13M, 60tr FYC/M = 720tr/Y, FY/K2=85%, 3 EHC)* | **178.0% FYC** *(53.4% FYP)* | **174.8% FYC** *(52.4% FYP)* | **185.8% FYC** *(55.7% FYP)* | `UNKNOWN` | Ở phân khúc MDRT, khoảng cách thu hẹp mạnh (chỉ còn 7.8–11.0 điểm % FYC); lên TOT (`≥1,600tr FYC`), **AIA Alpha vượt lên 190% FYC**, vượt Chubb AR (185.8%)! |
| **M02 — Quản lý Trực tiếp Kỳ cựu** *(≥15M, NTT 60tr FYC/M = 720tr/Y, 6 active, FY/K2=82%)* | **61.0% FYC NTT** *(gồm 10% trả chậm 3Y)* + 10–40% Đồng hành | **61.0% FYC NTT** *(gồm 10% trả chậm 3Y)* | **108.0% FYC NTT** *(100% trả ngay Y1!)* | `UNKNOWN` | **Điểm nóng chi phí lớn nhất:** Direct Override của Chubb AL kỳ cựu cao hơn gấp **1.77 lần** AIA CQL (và cao hơn gấp **2.12 lần** về tiền mặt chi ngay Năm 1: 108% vs 51%)! |
| **L01 — Lãnh đạo Khối/Vùng Chuẩn** *(Khối TT 300tr FYC/M = 1 tỷ FYP/M = 12 tỷ FYP/Y, 120% chỉ tiêu, K2/FY=80%, tăng trưởng +15% QoQ)* | **~1,554tr/Y** *(PAF/SAF cố định + biến đổi TT + thâm niên, chưa gồm Dual Career & chuỗi GT)* | Như 2026 | **~1,242tr/Y** *(RD nghiệm thu + 3MAA + Tăng trưởng Q + RYC; rơi mạnh nếu K2 <60%)* | **~1,436tr/Y Earned** *(nhưng chỉ chi **~1,091tr Cash Y1**, giữ **~345tr trả 3Y**!)* | **Manulife tối ưu dòng tiền năm 1 nhất** (~24% giữ lại trả chậm 3 năm gắn `K2 ≥70%`); Chubb RD biến động cực mạnh theo tăng trưởng quý & vách đá K2 `60%`. |

---

### Phương pháp 10 — Enterprise Total Distribution Cost Stacking (Chi phí Phân phối Toàn Hệ thống Không Trùng Lặp)
- **Mục tiêu:** Đo tổng số tiền doanh nghiệp thực sự phải chi trên **100 đồng FYP** khi xếp chồng đầy đủ tất cả các tầng (Đại lý → Quản lý trực tiếp → Quản lý gián tiếp → Lãnh đạo vùng), **chỉ tính doanh thu 1 lần** và kiểm tra **Trần Điều 52 (≤30% FYP cho Thưởng đại lý)**.
- **Phương pháp:** Thiết lập cấu trúc chuẩn gồm 1 Khối Vùng (`12 tỷ FYP/năm = 3.6 tỷ FYC/năm`, 1 Lãnh đạo Vùng → 2 Quản lý cấp trung → 4 Quản lý trực tiếp → 20 Đại lý hoạt động bình quân), phân bổ cố định đúng 1 lần theo tỷ trọng FYP của đơn vị, chạy ở 3 kịch bản chất lượng (`K2 = 82%`, `72%`, `62%`).
- **Kết quả (`MODEL_OUTPUT` — chi tiết công thức động tại Sheet `11_Hierarchy_Dist_Cost` của Excel Model):**
  - **Chubb Life (cấu trúc AL kỳ cựu ≥15M + AR ≥13M, K2 = 82%):** Tổng chi phí toàn cây (Hoa hồng 30% + Thưởng AR ~20–25% FYP + Override AL TT/GT ~28–34% FYP + RD ~11% FYP) có thể vọt lên **`89% – 100%+ FYP Năm 1`** (tức **297%–333% FYC**), trong đó riêng nhóm thưởng đại lý có rủi ro **chạm sát hoặc vượt trần 30% FYP Điều 52** nếu tỷ trọng đại lý top cao! Khi K2 rơi xuống `62%`, chi phí vẫn còn khá cao (~`70%–75% FYP`) do AR/AL vẫn nhận 75% K2 factor.
  - **AIA Alpha (2026/2027, chưa tính trợ cấp `Exchange/Pro`, K2/FY = 82%):** Tổng chi phí toàn cây ở mức **`76% – 86% FYP Năm 1`** (chưa tính chi phí cố định PAF+ nhiều tầng nếu chuỗi gián tiếp sâu >3 tầng và chưa tính trợ cấp Exchange/Pro). Ở **FY = 65% năm 2027**, tổng chi phí rơi rất mạnh về **`~54% – 60% FYP`** nhờ vách đá `0%` cắt sạch thưởng CVTV — bảo vệ biên lợi nhuận doanh nghiệp tốt hơn Chubb khi chất lượng suy giảm!
  - **Manulife:** Chỉ đo được chính xác lớp Tầng 3 (`~10.5%–11.5% FYP Earned`, nhưng **Cash Year 1 chỉ ~8.0%–8.6% FYP** nhờ trả chậm 3 năm); Tầng 1–2 là `UNKNOWN` nên tổng cây toàn doanh nghiệp của Manulife được ghi nhận `INCOMPLETE / UNKNOWN`.

---

### Phương pháp 11 — Market Suitability & Strategic Archetype Benchmarking (Đánh giá Phù hợp Thị trường VN 2026–2027)
- **Kết quả (`HYPOTHESIS` gắn bằng chứng IAV/MOF 2024–2026):**
  - **AIA Alpha** theo nguyên mẫu **Professional Full-Time Expansion & Franchise Buy-Build** — mạnh khi cần hút thủ lĩnh & xây đội ngũ MDRT/Exchange Pro, nhưng rủi ro cao về định phí PAF+ và sốc rời bỏ ở vách đá 70% năm 2027 trong bối cảnh thị trường VN đang giảm kích cỡ hợp đồng (`Average Case Size` thu hẹp).
  - **Chubb Life** theo nguyên mẫu **High-Powered Traditional Production + Behavioral Discipline (Champion Hubb)** — cực mạnh về giữ chân AR/AL kỳ cựu bán giỏi và ép bán bảo vệ thực chất (`HSBH` + `Top-up = 0%`), nhưng chịu áp lực lớn về **tổng chi phí phân phối** và **trần Điều 52 (30% FYP)** ở nhóm năng suất cao, đồng thời thiếu cơ chế trả chậm 3 năm giữ lãnh đạo.
  - **Manulife (`PSM+/HKD`)** theo nguyên mẫu **Corporate-Disciplined Regional Governance & Entity Flexibility** — gọn nhất, kiểm soát định phí bằng sàn 30%/trần 150%, tối ưu dòng tiền & giữ chân qua trả chậm 3 năm (`30/30/40%`, `K2 ≥70%`), nhưng cần loại bỏ `6% Top-up` khỏi định nghĩa FYP để đồng bộ hoàn toàn với TT 96/2026.

---

### Phương pháp 12 — Financial Return, Cash-Flow & Break-Even Benchmarking (Hiệu quả Tài chính & Điều kiện ROI)
- **Mục tiêu:** Tuyệt đối **KHÔNG nhầm `Total Comp / APE` với `ROI`**. Vì chưa có `VNB Margin` và chi phí vận hành thực tế của doanh nghiệp đích (`UNKNOWN`), dùng phương pháp **Break-Even Margin & Cash-Flow Payback Sensitivity**.
- **Phương pháp:** Với mỗi cấu trúc phân phối (AIA Alpha, Chubb Agency, và 3 Proposal), tính:
  1. `Year-1 Cash Distribution Cost (% FYP)` vs `Total Earned Cost (% FYP)` vs `Deferred Liability (% FYP)`.
  2. `Persistency-Adjusted Effective Cost per Persisted Year-2 Policy = Total Distribution Cost / K2_Rate` (đo chi phí thực tế để tạo ra 1 đồng phí còn sống đến năm thứ 2!).
  3. **Ngưỡng Hòa vốn (`Break-Even Gross Product Contribution Margin`)** cần thiết để đạt `ROI ≥ 0%` và `ROI ≥ 15%` dưới các giả định chi phí vận hành/quản lý chung (`Home Office OpEx`: 15% / 20% / 25% FYP — gắn nhãn `ASSUMPTION`).
- **Kết quả cốt lõi (`MODEL_OUTPUT`):**
  - Khi K2 tụt từ `80%` xuống `60%`, **chi phí trên mỗi đồng phí còn sống đến Năm 2 (`Cost / Persisted Y2 Premium`)** ở một chính sách mềm đáy như Chubb AR/AL tăng vọt thêm **+20% đến +28%**, làm sụp đổ ROI cho dù tỷ lệ chi trên FYP năm 1 trông có vẻ giảm!
  - Việc dịch chuyển **15%–25% thưởng quản lý & đại lý cao cấp sang trả chậm 2–3 năm gắn `K2 ≥ 75%`** (học từ Manulife `PSM+` & AIA `CQL`) đồng thời **giảm căng thẳng dòng tiền Năm 1 từ 8–12 điểm % FYP** và **tự động loại bỏ chi trả cho các hợp đồng hủy sớm**, hạ ngưỡng `Break-Even Margin` cần thiết xuống **6–9 điểm % FYP**!
