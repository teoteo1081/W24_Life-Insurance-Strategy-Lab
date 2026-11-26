# ANCHOR_SPEC.md — Mục tiêu, Business Anchor và Phạm vi Chuẩn

**Dự án:** W24 — Life Insurance Strategy Lab  
**Phiên bản:** 1.1 (Cập nhật Business Anchor nguyên văn ngày 2026-11-26)  
**Business Owner:** TJ  

---

## 1. Primary Business Anchor — Yêu cầu Nghiệp vụ Gốc (Ưu tiên Cao nhất)

**Nguồn:** `SRC-REQ-001` — Nguyên văn yêu cầu của chị Nhi (`VERIFIED FACT`, ghi nhận ngày 2026-11-26):

> **"Bước 1: Phân tích các chính sách thu nhập giữa các công ty, và đề xuất chính sách phù hợp tại thị trường VN, nhằm thúc đẩy gia tăng doanh số, chất lượng kinh doanh và hiệu quả về mặt chi phí (ROI)."**

Mọi hoạt động nghiên cứu, xây dựng mô hình và trình bày trong deadline 3 ngày phải phục vụ trực tiếp và truy vết ngược được về yêu cầu gốc này.

**Đối tượng nghiên cứu dự kiến:**
- AIA (bao gồm các kênh như truyền thống, AIA Exchange, v.v.)
- Manulife
- Chubb Life
- Kênh Alpha (thuộc AIA Việt Nam theo nguồn công khai — chưa có tài liệu policy nội bộ xác minh)
- Các chính sách / đề xuất bổ sung sau này.

---

## 2. Phân tách Ranh giới: Yêu cầu Gốc (Bước 1) vs. Tầm nhìn Mở rộng của TJ

### P0 — Phạm vi Bắt buộc phục vụ trực tiếp Yêu cầu Gốc của chị Nhi (Không được hy sinh)
1. **Phân tích chính sách thu nhập giữa các công ty** (tách rõ Công ty → Kênh → Scheme → Đối tượng → Phiên bản → Hiệu lực).
2. **Bảng so sánh chính sách thu nhập** trên cùng một cơ sở chuẩn hóa + **Danh mục quy tắc nghiệp vụ** (`business-rules-catalog.csv`) có truy vết nguồn.
3. **Đề xuất chính sách thu nhập phù hợp tại thị trường VN** (tối thiểu 3 hướng chiến lược: Growth / Quality / Balanced-Hybrid, tuân thủ khung pháp lý TT 67/2023 & TT 96/2026).
4. **Phân tích tác động lên 3 mục tiêu cốt lõi:** (a) Gia tăng doanh số, (b) Chất lượng kinh doanh, (c) Hiệu quả về mặt chi phí & ROI (có phân tích độ nhạy & điểm hòa vốn).
5. **Mô hình Excel tham chiếu có thể kiểm chứng độc lập** (tách Inputs / Formulas / Outputs + Golden Test Cases).
6. **Bản trình bày lãnh đạo** (Gói A — Interview Delivery, 5–7 trang/slide).

### P1 — Tầm nhìn Mở rộng của TJ (Chỉ triển khai khi P0 đã vững)
- **MAPA tính xuôi và tính ngược** (mở rộng lập kế hoạch lực lượng bán).
- **Marketing tuyển Sales** (phễu tuyển dụng đại lý).
- **Marketing tìm kiếm khách hàng** (phễu khách hàng & phân bổ ngân sách quảng cáo).
- **PO điều chỉnh tham số** (PO Decision Bridge cấu hình linh hoạt).
- **HTML Interactive Simulator** phiên bản đầu tiên (chỉ xây sau khi Excel đã kiểm chứng và có Parity Test).

### P2 — Tầm nhìn Dài hạn (Phát triển sau deadline 3 ngày)
- Tự động hóa đọc PDF, tối ưu hóa nâng cao (Operations Research), tích hợp CRM/Chatbot, hệ thống tính hoa hồng production, kết nối nền tảng quảng cáo.

---

## 3. Requirement Traceability Matrix — Ma trận Truy vết từ Yêu cầu Gốc

| Req ID | Vế yêu cầu gốc (Chị Nhi — `SRC-REQ-001`) | Tài liệu Nghiên cứu & Tri thức | Mô hình & Kiểm thử | Bằng chứng (Evidence) | Sản phẩm Khuyến nghị (Gói A) | Trạng thái |
|---|---|---|---|---|---|---|
| **REQ-01** | Phân tích các chính sách thu nhập giữa các công ty | `docs/research/wheel-check.md`, `knowledge/sources/source-registry.csv`, `knowledge/business-rules/business-rules-catalog.csv`, `outputs/working/competitor-comparison-v0.1.md` | Excel Reference Model — Sheet `Competitor Comparison` & `Business Rules` (Ngày 2) | Nguồn pháp lý công khai (`SRC-LAW-001..004`), nguồn báo chí (`SRC-PUB-001..002`); **đang chờ Policy PDF gốc** (`SRC-POL-*`) | Slide/Trang 2–3: Bảng so sánh đối thủ & Nhận định chính | `IN_PROGRESS` (v0.1 xong; chờ PDF gốc lên v1.0) |
| **REQ-02** | Đề xuất chính sách phù hợp tại thị trường VN | `docs/research/wheel-check.md` (Khung pháp lý VN 2023–2027), `knowledge/glossary/glossary.md` | Excel Reference Model — 3 hướng Scheme A (Growth) / B (Quality) / C (Balanced-Hybrid) (Ngày 2) | Ràng buộc trần FYC 30% UL/ILP & siết Top-up theo TT 96/2026/TT-BTC (`SRC-LAW-004`) | Slide/Trang 4 & 6: Đề xuất Scheme, Khuyến nghị & Trade-offs | `PENDING` (Ngày 2) |
| **REQ-03** | Thúc đẩy gia tăng doanh số | `docs/discovery/domain-discovery.md`, `outputs/working/competitor-comparison-v0.1.md` | Excel Reference Model — Mô phỏng 7 nhóm đại lý, động lực Activation / Production Bonus (Ngày 2) | Golden Test Cases kiểm chứng công thức thưởng bậc thang & ngưỡng kích hoạt (`tests/`, Ngày 2) | Slide/Trang 5: Tác động doanh số (APE/FYP) theo kịch bản | `PENDING` (Ngày 2) |
| **REQ-04** | Thúc đẩy chất lượng kinh doanh | `knowledge/glossary/glossary.md` (Persistency K2/13M, Clawback), `docs/research/wheel-check.md` | Excel Reference Model — Cơ chế Persistency Gate (K2/13M), RYC năm 2+ & Clawback (Ngày 2) | Adversarial Test (L4 Audit): kiểm thử kịch bản hủy hợp đồng sớm / trục lợi trợ cấp (Ngày 3) | Slide/Trang 5–6: Cơ chế bảo vệ chất lượng & kiểm soát rủi ro | `PENDING` (Ngày 2–3) |
| **REQ-05** | Hiệu quả về mặt chi phí và ROI | `knowledge/glossary/glossary.md` (phân biệt `Total Comp/APE` vs. `ROI`) | Excel Reference Model — Financial / Cost Ratio, Sensitivity & Break-even Analysis (Ngày 2) | Đối soát công thức & kiểm tra độ nhạy với biên đóng góp giả lập gắn nhãn rõ ràng (Ngày 2–3) | Slide/Trang 5–7: Phân tích chi phí, điều kiện hòa vốn/ROI & dữ liệu cần bổ sung khi pilot | `PENDING` (Ngày 2–3) |

---

## 3. Tiêu chuẩn Trưởng thành Repository

- **Mục tiêu 3 ngày:** Đạt **Level 1 (Có tổ chức)** toàn repo và chứng minh **Level 2 (Có thể tái tạo kết quả)** trên các luồng tính toán trọng yếu (Compensation, MAPA, Cost/ROI sensitivity).
- Không tự nhận đạt cấp độ cao hơn khi chưa có bằng chứng kiểm thử thực tế.

---

## 4. Ranh giới Bảo mật & Chia sẻ

- **Gói A (`outputs/interview/`):** Gói trình bày cho chị Nhi. Chỉ chứa kết luận có bằng chứng, bảng so sánh, đề xuất, trade-offs và lộ trình pilot.
- **Gói B (Working Papers):** Giữ nội bộ trong repo của TJ.
- Tài liệu gốc nội bộ của doanh nghiệp/đối thủ (PDF policy, dữ liệu nhạy cảm) đặt trong `private/` (đã nằm trong `.gitignore`), không commit vào lịch sử Git nếu chưa được cấp quyền.
