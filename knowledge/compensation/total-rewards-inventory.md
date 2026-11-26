# Total Rewards Inventory — Danh mục Đầy đủ Cấu phần Thu nhập & Phúc lợi (Nhóm A–H)

**Ngày lập:** 2026-11-26  
**Bảng dữ liệu đầy đủ (44 cấu phần × 33 trường metadata chuẩn Section 14):** [total-rewards-inventory.csv](file:///C:/Users/User/Desktop/TJ/Project/W24_Life-Insurance-Strategy-Lab/knowledge/compensation/total-rewards-inventory.csv)  
**Cơ sở bằng chứng:** 7 PDF chính sách gốc (`116 trang`) — `BASED ON AVAILABLE POLICY DOCUMENTS`.

> **Nguyên tắc Quản trị Chi phí & Phúc lợi (Section 14):**
> 1. **Tuyệt đối không bỏ sót cấu phần phi tiền mặt hoặc trả chậm:** Tách bạch rõ 3 lớp chi phí: **(i) Tiền mặt định lượng được bằng công thức**, **(ii) Tiền mặt có phụ thuộc ngoài/thiếu dữ liệu**, và **(iii) Phúc lợi phi tiền mặt chưa định giá chi phí DN (`Unpriced_Non_Cash_Benefit`)**.
> 2. **Tuyệt đối KHÔNG đoán chi phí doanh nghiệp** cho vé Chuyến huấn luyện đặc biệt, gói Bảo hiểm Sức khỏe tiêu chuẩn/cao cấp hay gói BHSK & Tai nạn RD; ghi rõ `Employer_Cost_Known = UNKNOWN_DO_NOT_GUESS`.
> 3. **Phân nhóm Rổ Pháp lý (`Regulatory_Bucket`):** Gắn nhãn từng cấu phần vào đúng rổ chi phí theo **Điều 51 (Hoa hồng)**, **Điều 52 (Trần 30% FYP Y1 / 7% RYP cho Thưởng & Hỗ trợ đại lý)** và **NĐ 97/2026 (Chi phí Dịch vụ Quản lý, Đào tạo & Tuyển dụng)**.

---

## 1. Tổng hợp Cấu trúc 8 Nhóm Cấu phần (`Category A–H`) Theo Công ty

| Nhóm Cấu phần (`Category`) | AIA Việt Nam — Kênh Alpha (21 cấu phần) | Manulife Việt Nam — `PSM+/HKD` (5 cấu phần) | Chubb Life Việt Nam — Kênh Đại lý (18 cấu phần) |
|---|---|---|---|
| **A. Direct Commission (Hoa hồng trực tiếp)** | `TR-AIA-01` (`MISSING_DEPENDENCY`: thiếu phụ lục % theo sản phẩm & memo `FYC Tín Chỉ`) | `TR-MNL-05` (`UNKNOWN`: thiếu chính sách FA & biểu hoa hồng) | `TR-CHB-01` (**`VERIFIED_FACT`**, 113 dòng sản phẩm + 10 khung tuổi HSBH; UL/ILP 20%–30%, Top-up 0% SP mới / 1.5–7% SP cũ) |
| **B. Fixed / Base / Allowance (Cố định & Trợ cấp)** | `TR-AIA-11` (`Exchange/Pro/AFF` — `UNKNOWN` số tiền); **`TR-AIA-19` (`PAF+` cố định 20–130tr/M × KPI FYP × Chuyên cần)** | **`TR-MNL-01` (`PSM+/HKD` cơ bản 35/45tr × %FYP × 130%, sàn 30%, trần 150% = 52.5/67.5tr)** | **`TR-CHB-13` (`RD` 3 khoản nghiệm thu Đào tạo/EHC/FYP — tổng trần 45tr/M)** |
| **C. Activation / Onboarding (Kích hoạt ĐL mới)** | `TR-AIA-02` (1/72H: 1.5tr), `TR-AIA-03` (Đồng hành 3M: 1.5–3tr/M, ACK 15d / T01: 28/02/2026) | `UNKNOWN` (thiếu policy FA) | `TR-CHB-04` (ĐL mới M3/6/12: 20% FYC, cap 36tr, thiếu khóa cắt 50%), **`TR-CHB-06` (Champion Hubb Cá nhân M1–24 có bù trừ & giữ lại M12)** |
| **D. Short-Term Production (Thưởng DS ngắn hạn)** | `TR-AIA-05` (DS Quý 4–40% × FY), `TR-AIA-06` (Ngoại hạng 3/4/5S: 5–15% × FY), `TR-AIA-08` (DS Năm 6–20% × FY) → Đỉnh **90% FYC** | `UNKNOWN` (thiếu policy FA) | `TR-CHB-02` (HQKD Tháng Rolling 3M × K2, giữ T+1 nếu K2<60%), `TR-CHB-03` (HQKD Quý nhân chồng +15%/+30%) → Đỉnh **85.8% (AR) / 109.2% (AL)** |
| **E. Quality / Persistency / Renewal (Chất lượng tái tục)** | **`TR-AIA-07` (+30%/+50% SYC Quý cho 4S/5S)** | Tích hợp qua hệ số K2 (04/2026) & cổng K2 ≥70% dài hạn | `TR-CHB-05` (AR +10%/15% RYC Y2–5), `TR-CHB-11` (AL +10%/15% RYC NTT), **`TR-CHB-15` (RD +10%–30% RYC Vùng)** |
| **F. Management / Override / Recruit / Dev (Quản lý & Tuyển dụng)** | `TR-AIA-10` (SA giới thiệu 5/10/20%), `TR-AIA-12..16`, `TR-AIA-18` (CQL Direct 24% + Activity 12% + Premier 15% + Gen 2–4 50/25/12.5% + UM mới 150% cap 30tr + **Đồng hành 10/20/40%**), **`TR-AIA-20` (PAF+ chuỗi vô hạn 50%)** | `TR-MNL-02` (Năng suất tháng 6–8% × K2 + 50% GT), `TR-MNL-03` (Hoạt động quý 1–5% 1mAA × K2 + 50% GT) | `TR-CHB-07` (Tuyển dụng 10% M1–6 + 10% khóa M12 lên UM), **`TR-CHB-08` (HT KTN đỉnh 108% FYC NTT + phí âm đối xứng)**, `TR-CHB-09` (GT L1–3 khóa 0% nếu NTT <15tr), `TR-CHB-10` (+100% UM/SM mới), `TR-CHB-12` (CH QL), **`TR-CHB-14` (RD Tăng trưởng Quý 2.5–27.5% × K2 Cliff 50%→60%)**, `TR-CHB-16` (RD trên BD/RD con) |
| **G. Long-Term Deferred / Retention (Trả chậm & Giữ chân)** | **`TR-AIA-17` (CQL Năm 5–10%, trả chậm 3 năm 15/25/60% 2028–2030, `TOT ≥85%`)**, `TR-AIA-21` (PAF+ Thâm niên 4–6% vượt chỉ tiêu, **Clawback 100% trong 12M**) | **`TR-MNL-04` (Hợp tác dài hạn 75% TT + 25% GT, cap 12× = 420/540tr, trả rải 3 năm 30/30/40% tháng 4, `K2 ≥70%`)** | `TR-CHB-17` (Chuyển tiếp giải ngân 25% giữ lại 2024–2025 tại T+15; 2026 không tạo holdback 25% mới) + cục M12 của CH & Tuyển dụng |
| **H. Non-Cash Benefits (`Unpriced_Non_Cash_Benefit`)** | **`TR-AIA-04` (Chuyến HL Đặc biệt 3M — 1 vé, không quy tiền, không thu hồi)**, **`TR-AIA-09` (Gói BHSK 1 năm Tiêu chuẩn / Cao cấp — không quy tiền, hủy ngay khi nghỉ việc)** | Không ghi nhận trong `0048M01` | **`TR-CHB-18` (Gói BHSK & Tai nạn cho RD — chi phí DN không công bố)** |

---

## 2. Phân tách 3 Lớp Chi phí & Phúc lợi Phi tiền mặt (Không trộn lẫn)

| Lớp Chi phí (`Cost_Classification`) | Số cấu phần | Ý nghĩa khi đưa vào Mô hình Tài chính & Excel |
|---|---:|---|
| **1. Tiền mặt định lượng được (`Known_Cash_Formula`)** | 34 | Đưa trực tiếp vào Engine Python & Excel Reference Model (bao gồm tách riêng Cash Paid Year 1 vs Deferred Post-Y1 vs Holdback/Clawback). Lưu ý 2 cấu phần có `CONFLICTING_EVIDENCE` (`TR-AIA-05` làm tròn FY; `TR-CHB-06` hệ số `W1` 80% vs 50%) được mở 2 toggle chọn kịch bản. |
| **2. Tiền mặt thiếu tài liệu nguồn (`Known_Cash_Conditional_Missing_Dep`)** | 7 | Gồm Hoa hồng AIA (`TR-AIA-01`), Trợ cấp `Exchange/Pro/AFF` (`TR-AIA-11`), Toàn bộ FA/UM Manulife (`TR-MNL-05`), và phần phụ thuộc `BD` trong `TR-CHB-16`. **Không được bịa số** — ghi rõ giả định chuẩn hóa hoặc để `UNKNOWN` trong báo cáo. |
| **3. Phúc lợi Phi tiền mặt chưa định giá (`Unpriced_Non_Cash_Benefit`)** | 3 | Gồm `TR-AIA-04` (Chuyến HL 3M), `TR-AIA-09` (Gói BHSK CVTV), `TR-CHB-18` (Gói BHSK & Tai nạn RD). Liệt kê đầy đủ điều kiện đạt trong Total Rewards Ledger nhưng **giữ ô chi phí DN = `UNKNOWN (Unpriced)`**, không gán 0đ ngầm hay bịa giá mua bảo hiểm/tour. |

---

## 3. Liên kết Phân bổ Rổ Pháp lý (`Regulatory_Bucket`) — Cảnh báo Rủi ro Trần Điều 52

- **Rổ 1 — Hoa hồng Đại lý (`Art51_Commission`):** Chịu trần từng hợp đồng (30% UL/ILP Y1; 40% Tử kỳ/Trọn đời; Top-up ≤ phí ban đầu từ 01/01/2027). Chubb Life đã thể hiện sự tuân thủ chủ động khi đưa Top-up SP mới về `0%` và phân tầng FYC *Tự Do An Phúc* theo HSBH (`20%–30%`).
- **Rổ 2 — Thưởng & Hỗ trợ Đại lý Khai thác mới (`Art52_NewBiz_Bonus_30pct`):** Chịu **trần tổng danh mục công ty ≤ 30% FYP Năm 1** (hiệu lực đầy đủ từ 01/01/2026 sau khi hết lộ trình chuyển tiếp 31/12/2025!). Trong danh mục trên, cả thưởng kích hoạt (1/72H, 3M, ĐL mới, Champion Hubb Cá nhân), thưởng DS tháng/quý/năm, lẫn gói trợ cấp Exchange/Pro (nếu hạch toán hỗ trợ đại lý) đều **cùng chia chung rổ trần 30% FYP này** — đây là nút thắt tài chính-pháp lý quan trọng nhất mà mọi thiết kế mới phải kiểm tra.
- **Rổ 3 — Thưởng Chăm sóc Tái tục (`Art52_Renewal_Bonus_7pct`):** Chịu trần **≤ 7% phí tái tục thực thu** (`TR-AIA-07` 30–50% SYC; `TR-CHB-05` 10–15% RYC).
- **Rổ 4 — Chi phí Quản lý, Đào tạo & Tuyển dụng (`ND97_Mgt_Training_Service`):** Tách biệt khỏi Điều 51/52 theo NĐ 97/2026/NĐ-CP nhưng **phải có dịch vụ thực tế và biên bản nghiệm thu** (như Chubb RD và Manulife PSM+/HKD).

Toàn bộ 33 trường metadata cho từng cấu phần xem tại [total-rewards-inventory.csv](file:///C:/Users/User/Desktop/TJ/Project/W24_Life-Insurance-Strategy-Lab/knowledge/compensation/total-rewards-inventory.csv).
