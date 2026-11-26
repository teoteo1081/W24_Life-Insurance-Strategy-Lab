# Role & Organization Mapping — Bản đồ Chức danh, Cấp bậc & Tương đương Chức năng

**Ngày lập:** 2026-11-26  
**Dữ liệu chuẩn hóa (36 chức danh × 16 thuộc tính):** [role-organization-mapping.csv](./role-organization-mapping.csv)  
**Cơ sở bằng chứng:** Toàn văn 7 PDF chính sách gốc (`116 trang`) — `BASED ON AVAILABLE POLICY DOCUMENTS`.

> **Nguyên tắc chống so sánh lệch tầng (No False Equivalence):** Không bao giờ đặt một chức danh Quản lý Cấp cao/Hộ Kinh Doanh (như Manulife `PSM+/HKD`) ngang hàng với Đại lý cá nhân (`AIA SA` hay `Chubb AR`) hoặc Quản lý cấp trung (`UM/SM/DM`). Mọi phép so sánh phải quy chiếu về **7 nhóm Tương đương Chức năng (Functional Tiers)** bên dưới.

---

## 1. Bảng Tương đương Chức năng Giữa 3 Công ty (Apples-to-Apples Mapping)

| Tầng Chức năng (`Functional_Tier`) | AIA Việt Nam — Kênh Alpha | Chubb Life Việt Nam — Kênh Đại lý | Manulife Việt Nam | Khả năng So sánh Trực diện |
|---|---|---|---|---|
| **1A. Đại lý Cá nhân Chuẩn** (`Tier_1_Individual`) | `SA` (Chuyên viên Tư vấn) | `AR` (Đại diện Kinh doanh) | **`FA` — `UNKNOWN`** *(thiếu tài liệu)* | **2 hãng** (AIA vs Chubb) |
| **1B. Đại lý Chuyên nghiệp / Toàn thời gian** (`Tier_1_FullTime_Special`) | `Exchange` / `Exchange Pro` *(chính sách trợ cấp riêng `MISSING_DEPENDENCY`; biết thưởng đồng hành 20%/40% & ×2 lượt `1mAA`)* | `AR Champion Hubb` (M1–M24, kỷ luật SOP 3 buổi/tuần + 20 FNA/tháng) | **`UNKNOWN`** | **Một phần** (Chubb rõ công thức; AIA thiếu gói trợ cấp) |
| **1C. Đại lý Phục vụ / Dự bị** (`Tier_1_Servicing_Reserve`) | `SE` (tối đa 12M, 0% thưởng, **loại trừ khỏi `1mAA`**) | `AR Dự bị` (tối đa 18M khi rớt duy trì 6M) | `SA` (Đại lý phục vụ — **được tính vào `1mAA_4mFYC`**, thiếu `01M02/2024/AO`) | **Định tính** (khác biệt lớn ở việc tính `1mAA`) |
| **2. Quản lý Kinh doanh Trực tiếp & Cấp trung** (`Tier_2_Direct_Mid_Manager`) | `UM → SUM → DM → SDM` (gồm luồng tuyển thẳng `AFF`; FYC NTT **bao gồm** bán cá nhân; gián tiếp Gen 2–4: 50/25/12.5%) | `AL: UM → SM → DM` + `AL Champion Hubb` (FYC NTT **không gồm** bán cá nhân; gián tiếp L1–L3 khóa `0%` nếu NTT `<15tr`) | **`UM / SUM / DM` — `UNKNOWN`** *(thiếu tài liệu)* | **2 hãng** (AIA vs Chubb) |
| **3A. Lãnh đạo Khối / Vùng Cấp cao (Cá nhân)** (`Tier_3_Senior_Leader`) | 10 bậc có biểu phí: `PAF → AF → PSAF → SAF → DRF → RF → DSRF → SRF → PVP → SPVP` + 4 bậc cao hơn (`VP / EVP / SVP / President` — thiếu biểu phí). **Dual Career** (vừa bán cá nhân + CQL TT + PAF+). | `AMD: BD` *(thiếu policy phí 2026)* → **`RD`** (Giám đốc Vùng Điều hành & PTKD, HĐDV có biên bản nghiệm thu, 8 khoản phí). | **`PSM / SM`** (35tr cơ bản) & **`PSSM / SSM`** (45tr cơ bản), HĐDV Quản lý Cấp cao (khấu trừ TNCN). | **ĐỦ CẢ 3 HÃNG!** *(Điểm benchmark toàn diện nhất hiện có)* |
| **3B. Pháp nhân Đối tác / Hộ Kinh Doanh** (`Tier_3_Entity_HKD`) | Không xuất hiện trong 3 memo Alpha (`UNKNOWN`) | Không xuất hiện trong 3 memo Chubb (`UNKNOWN`) | **`HKD1/2`** (35tr) & **`HKD3/4`** (45tr) — xuất hóa đơn, tự kê khai thuế, bảo lưu 100% khi chuyển đổi từ `PSM+`. | **Đặc thù Manulife** |

---

## 2. Khác biệt Tổ chức & Quy tắc Quản trị Chức danh Cốt lõi (`VERIFIED FACT`)

1. **Cách tính Doanh số Nhóm Trực tiếp (`Direct Team Scope`):**
   - **AIA Alpha (`CQL`):** `FYC Tín Chỉ` nhóm trực tiếp **BAO GỒM** cả doanh số bán cá nhân của chính CQL (`2601-034 p.13`).
   - **Chubb Life (`AL`):** `FYC` nhóm trực tiếp (NTT) **KHÔNG BAO GỒM** doanh số bán cá nhân của AL (`0008V p.5`) — buộc AL phải vừa quản lý đội ngũ vừa tự bán nếu muốn hưởng mức thưởng cá nhân `109.2% FYC`!
2. **Quy tắc Chống Lệch Cân bằng / Ăn bám Hệ thống (`Concentration & Direct Accountability`):**
   - **AIA Alpha (`CQL` vs `PAF+`):** Dùng **70% Concentration Cap** (trong CQL áp dụng cho **cả nhóm trực tiếp lẫn nhánh UM+ con**, tối đa 70% **chỉ tiêu yêu cầu**; trong PAF+ chỉ áp cho nhánh PAF+ con, khối trực tiếp tính 100%).
   - **Chubb Life (`AL`):** Dùng **Direct-Team Floor Gate** rất sắc: nếu `FYC NTT < 15tr/tháng`, toàn bộ Override Gián tiếp L1–L3 rơi về **`0%`** (`15–30tr` chỉ nhận `30/15/7.5%`, từ `≥30tr` mới mở khóa `50/25/12.5%`).
   - **Manulife (`PSM+/HKD`):** Phân bổ Phí Hợp tác Dài hạn theo tỷ trọng **75% Khu vực Trực tiếp vs. 25% Khu vực Gián tiếp** để giữ lãnh đạo cấp cao bám sát thực địa.
3. **Báo cáo Đồng cấp & Vượt cấp (`Peer & Leapfrog Rules`):**
   - **AIA Alpha:** CQL đồng cấp bảo lưu `12M (UM) / 18M (SUM) / 24M (DM)` và **miễn tách nhánh cho `SDM–SDM`**. PAF+ đồng cấp bảo lưu `12/18/24M`, nhưng **từ Q2/2026 vượt cấp (con cao hơn mẹ) tách nhánh ngay lập tức** (`2601-035 p.8`).
   - **Chubb Life:** `AL` áp dụng quy tắc `Team Null`; `RD–RD` đồng cấp bảo lưu tối đa **24 tháng** (`0003V p.12`).
4. **Cơ cấu Pháp lý & Thuế (`Contract & Tax Structure` — Liên kết NĐ 97/2026/NĐ-CP):**
   - Cả 3 hãng đều tách **Hợp đồng Đại lý** (hoa hồng Điều 51 + thưởng Điều 52) khỏi **Hợp đồng Dịch vụ Quản lý / Đào tạo / HKD** (có yêu cầu nghiệm thu dịch vụ rõ nhất ở Chubb RD và linh hoạt hóa pháp nhân rõ nhất ở Manulife HKD).

---

## 3. Danh sách Đầy đủ 36 Chức danh (Truy vết 100% về File CSV)

Toàn bộ 16 thuộc tính chi tiết (Role_ID, Company, Channel, Scheme, Role_Code, Role_Title, Functional_Tier, Contract_Type, Tax_Status, Entry/Promotion, Maintenance/Demotion, Dual Career, Managed Scope, Peer Rule, Mandatory Training/Compliance, Source & Status) được lưu trữ chuẩn hóa tại [role-organization-mapping.csv](./role-organization-mapping.csv).
