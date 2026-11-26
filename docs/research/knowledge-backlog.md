# Knowledge Backlog & Roadmap Mở rộng (Section 37)

**Ngày cập nhật:** 2026-11-26  
**Mục đích:** Theo dõi tập trung mọi khoảng trống tri thức, văn bản còn thiếu cần thu thập, yêu cầu kiểm chứng pháp lý, và tầm nhìn mở rộng P1/P2 (không để lẫn vào phạm vi P0 của chị Nhi).

---

## 1. Tài liệu Chính sách Đối thủ Cần Thu thập Bổ sung (Ưu tiên Cao → Thấp)

| Ưu tiên | Công ty | Tài liệu / Mã văn bản thiếu | Ảnh hưởng Nghiệp vụ | Trạng thái |
|---|---|---|---|---|
| **P1 (Rất cao)** | **Manulife** | Chính sách Đại lý Cá nhân (`FA`), Quản lý cấp trung (`UM/SUM/DM`), Biểu Hoa hồng sản phẩm | Hiện Manulife hoàn toàn `UNKNOWN` ở Tầng 1 & Tầng 2; bổ sung sẽ hoàn thiện bảng so sánh 3 hãng trọn vẹn cả 3 tầng. | `BACKLOG` |
| **P1 (Rất cao)** | **AIA Alpha** | Chính sách trợ cấp `Exchange`, `Exchange Pro`, `AFF`; Phụ lục Hoa hồng; Memo `FYC Tín Chỉ` | Hiện chưa lượng hóa được gói trợ cấp toàn thời gian `Exchange/Pro` và phải giả định 30% UL khi quy đổi từ `FYP` sang `FYC`. | `BACKLOG` |
| **P1 (Cao)** | **Chubb Life** | `CHH0DCEB260005V` (định nghĩa `EHC`, `K2/P13`, clawback tổng quát) & Chính sách `BD` 2026 | Xác định chính xác ngưỡng tiền của `1 EHC` và cơ sở tính mục II.7–II.8 của RD. | `BACKLOG` |
| **P2 (Trung bình)** | **Manulife** | `0016M03/2024/ASBD` (công thức `TLDTHD`), Bảng chỉ tiêu `FYP/1mAA`, Thông báo hoạt động dịch vụ C.1 từ 02/2026, `0013M04/2024`, `01M02/2024` | Hoàn thiện 100% tính toán tuyệt đối từ doanh số thô cho tầng `PSM+/HKD`. | `BACKLOG` |
| **P2 (Trung bình)** | **AIA Alpha** | `AIAV/AD/2501-017` (3 tiêu chí CL ĐLBH), `2601-023` (khóa học), `2401-029` (HĐ thay thế), quy định chấm công & Vitality Vàng, Kênh Truyền thống AIA | Khép kín các cổng điều kiện phụ (attendance, training, replacement policy) và so sánh Alpha vs Truyền thống. | `BACKLOG` |
| **P2 (Trung bình)** | **Chubb Life** | `CHH0DCEB260006V`, `CHH0DCEB260009V` (Phí XD ĐVKD mới), `240048V` (HĐ <2025) | Hoàn thiện phép so sánh `MAX()` cho Champion Hubb Quản lý. | `BACKLOG` |
| **P3 (Mở rộng)** | **Đối thủ khác** | Prudential, Dai-ichi Life, Bảo Việt Nhân Thọ, FWD, Generali (Top thị phần VN) | Mở rộng benchmark thị trường bằng chính kiến trúc cấu hình module đã xây sẵn. | `BACKLOG` |

---

## 2. Kiểm chứng Pháp lý & Dữ liệu Nội bộ Cần Nạp cho Bước 2

| Hạng mục | Chi tiết Cần Xác minh / Thu thập | Nguồn Phụ trách |
|---|---|---|
| **Toàn văn Công báo Pháp luật** | Tải bản PDF chính thức (từ Cổng TTĐT Chính phủ / Bộ Tài chính) của: **Luật KDBH 08/2022/QH15**, **NĐ 46/2023 & NĐ 97/2026/NĐ-CP**, **TT 67/2023/TT-BTC (Điều 51 & 52)**, **TT 96/2026/TT-BTC** để nâng trạng thái 7 quy tắc `REG-*` từ `SOURCE_NOT_VERIFIED` lên `SOURCE_VERIFIED`. | Legal / TJ |
| **Dữ liệu Tài chính & Actuarial DN đích** | `VNB Margin` theo dòng sản phẩm (UL/ILP, Tử kỳ, Riders), `Home Office OpEx`, chi phí phát hành/thẩm định, và tỷ suất chiết khấu (`WACC / Hurdle Rate`) để chuyển từ Break-Even Margin sang tính **ROI & NPV thực tế**. | Finance / Actuarial |
| **Dữ liệu Cohort Lực lượng Bán** | Phân bổ thực tế theo thâm niên (M1–M3, M4–M12, >13M), tỷ lệ rơi rụng theo tháng, phân bổ `K2` thực tế, và `Average Case Size` thực tế để chạy **Back-testing** trên mô hình. | Agency Operations |

---

## 3. Tầm nhìn Mở rộng của TJ (P1 / P2 — Ngoài Phạm vi P0 Bước 1)

1. **HTML Interactive Simulator & PO Parameter Control (P1):** Chuyển đổi `compensation_engine.py` và cấu hình JSON/CSV sang giao diện Web tĩnh offline (HTML/CSS/Vanilla JS, 0đ, chạy cục bộ) có thanh trượt cho PO chỉnh tham số Proposal và chạy **Parity Test 100%** khớp với Excel & Python.
2. **Recruitment Marketing Funnel (P1):** Liên kết `CPL → Lead → Interview → Licensing → Active M1–M3` vào `Manpower` & `Active Ratio` của MAPA để tính **Total Acquisition Cost per Productive Agent**.
3. **Customer Marketing Funnel & Incrementality (P1–P2):** Mô phỏng phễu tạo lead khách hàng gắn với `Productivity` & `Case Size` của MAPA, tách bạch **Attribution vs. Incrementality** (tránh cộng trùng doanh số hữu cơ).
4. **Independent Calibration & Audit Đợt 2 (P1):** Mời Independent Auditor (Codex) kiểm toán lại toàn bộ gói Post-Audit Remediation, 112 rules, 3 lookup tables, Python Engine và Excel 14-sheet Model để cấp chứng nhận `INDEPENDENTLY_VERIFIED`.
