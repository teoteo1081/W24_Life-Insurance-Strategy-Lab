# Glossary — Từ điển Thuật ngữ Nghiệp vụ Chuẩn

Tài liệu này định nghĩa thống nhất các thuật ngữ sử dụng xuyên suốt mô hình Excel, bảng so sánh đối thủ và bài trình bày. **Tuyệt đối không đánh đồng các chỉ tiêu khác nhau.**

---

## 1. Chỉ tiêu Doanh số & Phí bảo hiểm

| Thuật ngữ | Tên tiếng Anh | Định nghĩa chuẩn | Lưu ý tránh nhầm lẫn |
|---|---|---|---|
| **APE** | Annualized Premium Equivalent | Phí bảo hiểm quy năm tương đương. Thường tính = `100% Phí định kỳ năm + 10% Phí đóng một lần (Single Premium)` (tùy quy định từng công ty về phần Top-up). | **Không đánh đồng với FYP.** Một hợp đồng đóng phí theo quý 5 triệu/quý có APE = 20 triệu, nhưng tại thời điểm phát hành phí thực thu mới là 5 triệu. |
| **FYP** | First Year Premium | Tổng phí bảo hiểm năm thứ nhất của hợp đồng. Cần phân biệt rõ giữa **FYP quy năm (Annualized FYP)** và **FYP thực thu (Collected FYP)** theo từng kỳ đóng phí. | Pháp luật VN quy định hoa hồng tính trên **phí bảo hiểm thực tế thu được**. |
| **RYP** | Renewal Year Premium | Phí bảo hiểm tái tục từ năm hợp đồng thứ 2 trở đi. | Gắn chặt với chỉ số Persistency (K2, K3...). |
| **Top-up** | Top-up / Additional Premium | Phí bảo hiểm đóng thêm ngoài phí bảo hiểm cơ bản (trong sản phẩm UL/ILP). | Theo TT 96/2026/TT-BTC (hiệu lực 01/01/2027), hoa hồng phí đóng thêm bị siết không vượt quá tỷ lệ phí ban đầu của phần đóng thêm. |

---

## 2. Chỉ tiêu Thu nhập Đại lý & Quản lý

| Thuật ngữ | Tên tiếng Anh | Định nghĩa chuẩn | Lưu ý tránh nhầm lẫn |
|---|---|---|---|
| **FYC** | First Year Commission | Hoa hồng năm thứ nhất trả cho đại lý, tính bằng `% FYC × Phí năm nhất thực thu` (tuân thủ trần Bộ Tài chính). | **Không bằng tổng thu nhập đại lý.** Chưa gồm thưởng quý, trợ cấp, contest. |
| **RYC** | Renewal Year Commission | Hoa hồng tái tục từ năm hợp đồng thứ 2 trở đi. | Quan trọng cho giữ chân đại lý (Retention) và chất lượng duy trì hợp đồng. |
| **Allowance** | Fixed / Conditional Allowance | Trợ cấp cố định hoặc trợ cấp có điều kiện KPI (thường áp dụng cho đại lý toàn thời gian / đại lý mới). | Là chi phí rủi ro cao nếu không gắn điều kiện sản lượng & chất lượng (dễ bị trục lợi). |
| **Activation Bonus** | Activation Bonus | Thưởng kích hoạt cho đại lý mới phát sinh hợp đồng đầu tiên / đạt mốc năng suất sớm trong 30–90 ngày đầu. | Tác động trực tiếp đến `Active Ratio` của cohort mới. |
| **Production / Quarterly Bonus** | Production / Performance Bonus | Thưởng năng suất theo tháng/quý/năm, thường tính lũy tiến theo bậc thang trên `FYC` hoặc `APE/FYP`. | Cần phân biệt rõ: **Lũy tiến từng phần (Marginal tier)** vs. **Áp dụng ngược toàn phần (Retroactive / Cliff tier)**. |
| **Override** | Management Override | Thu nhập cấp quản lý (UM/SUM/DM/BM...) tính theo % trên FYC/FYP của đội ngũ trực thuộc hoặc gián tiếp. | Phải tách biệt với thu nhập bán cá nhân của quản lý. |
| **Clawback / Recovery** | Clawback / Chargeback | Cơ chế thu hồi hoa hồng/thưởng đã chi trả khi khách hàng hủy hợp đồng trong thời gian cân nhắc (21 ngày) hoặc mất hiệu lực sớm. | Cần phân biệt: **Thu nhập được hưởng (Earned)** vs. **Thu nhập đã thực trả (Paid)** vs. **Thu nhập ròng sau thu hồi (Net Paid)**. |

---

## 3. Chỉ tiêu Chất lượng & Lập kế hoạch (MAPA)

| Thuật ngữ | Tên tiếng Anh | Định nghĩa chuẩn | Công thức / Ý nghĩa |
|---|---|---|---|
| **MAPA** | Manpower × Active × Productivity × Average Case Size | Mô hình phân rã động lực doanh số kênh đại lý. | `Doanh số (APE) = Manpower × Active Ratio × Productivity (Cases/Active) × Average Case Size (APE/Case)` |
| **Active Ratio** | Active Agent Ratio | Tỷ lệ đại lý có phát sinh ít nhất 1 hợp đồng hợp lệ (hoặc đạt ngưỡng hoạt động quy định) trong kỳ. | `Active Agents / Total Manpower` (luôn nằm trong `[0%, 100%]`). |
| **Persistency (K2 / 13M)** | 13-Month Persistency Rate | Tỷ lệ hợp đồng/phí bảo hiểm duy trì đóng phí sang năm thứ 2 (tháng thứ 13). | Thước đo vàng của **Chất lượng kinh doanh (Business Quality)**. |
| **Total Comp / APE** | Compensation Cost Ratio | Tỷ lệ tổng chi phí thu nhập đại lý & quản lý trên tổng APE mang về. | **Không phải ROI.** Đây chỉ là tỷ lệ chi phí phân phối trên doanh số. |
| **ROI** | Return on Investment | Tỷ suất sinh lời trên khoản đầu tư tăng thêm của chính sách. | `(Lợi ích đóng góp tăng thêm − Chi phí tăng thêm) / Chi phí tăng thêm`. Chỉ tính khi có định nghĩa biên đóng góp (`Contribution` / `VNB`) rõ ràng. |
