# ANCHOR_SPEC.md — Mục tiêu, Business Anchor và Phạm vi Chuẩn

**Dự án:** W24 — Life Insurance Strategy Lab  
**Phiên bản:** 1.2 (2026-11-27 — đồng bộ ngược từ sản phẩm HTML sau Drift Check; yêu cầu gốc mục 1 giữ nguyên văn. Xem DEC-15)  
**Business Owner:** TJ  

---

## STRICT DATA INGESTION & MAPPING PROTOCOL (MANDATORY)
1. **NO PREMATURE CALCULATION:** Never write calculation code or summary tables before completing a 100% Source & Entity Inventory of ALL input files.
2. **EXACT TITLE & SCOPE EXTRACTION:** Extract exact verbatim titles/roles and eligibility rules with `[FileName : PageNumber]` citations before normalizing across entities.
3. **NEGATIVE PROOF RULE:** You are strictly forbidden from claiming "missing data/document" unless you provide a search log proving all input files and filenames were scanned for related keywords.
4. **EVIDENCE-BOUND NUMBERS:** Every threshold, tier, or percentage in code/tables must cite its exact PDF source and page number.

Đồng bộ nguyên văn từ `AGENTS.md` (DEC-13, 2026-11-27). Áp dụng cho mọi lần nạp tài liệu và mọi công ty bổ sung sau này.

---

## 1. Primary Business Anchor — Yêu cầu Nghiệp vụ Gốc (Ưu tiên Cao nhất)

**Nguồn:** `SRC-REQ-001` — Nguyên văn yêu cầu của chị Nhi (`VERIFIED FACT`, ghi nhận ngày 2026-11-26):

> **"Bước 1: Phân tích các chính sách thu nhập giữa các công ty, và đề xuất chính sách phù hợp tại thị trường VN, nhằm thúc đẩy gia tăng doanh số, chất lượng kinh doanh và hiệu quả về mặt chi phí (ROI)."**

Mọi hoạt động nghiên cứu, xây dựng mô hình và trình bày trong deadline 3 ngày phải phục vụ trực tiếp và truy vết ngược được về yêu cầu gốc này.

**Đối tượng nghiên cứu dự kiến:**
- AIA (bao gồm các kênh như truyền thống, AIA Exchange, v.v.)
- Manulife
- Chubb Life
- Kênh Alpha (**đã xác minh `VERIFIED_FACT` trực thuộc Công ty TNHH BHNT AIA Việt Nam** qua 3 thông báo chính thức `AIAV/AD/2604-069`, `2601-034`, `2601-035`)
- Các chính sách / đề xuất bổ sung sau này.

---

## 2. Phân tách Ranh giới: Yêu cầu Gốc (Bước 1) vs. Tầm nhìn Mở rộng của TJ

### P0 — Phạm vi Bắt buộc phục vụ trực tiếp Yêu cầu Gốc của chị Nhi (Không được hy sinh)
1. **Phân tích chính sách thu nhập giữa các công ty** (tách rõ Công ty → Kênh → Scheme → Đối tượng → Phiên bản → Hiệu lực).
2. **Bảng so sánh chính sách thu nhập** trên cùng một cơ sở chuẩn hóa + **Danh mục quy tắc nghiệp vụ** (`business-rules-catalog.csv`) có truy vết nguồn.
3. **Đề xuất chính sách thu nhập phù hợp tại thị trường VN** (tối thiểu 3 hướng chiến lược: Growth / Quality / Balanced-Hybrid, tuân thủ khung pháp lý TT 67/2023 & TT 96/2026).
   - *Cập nhật 1.2 (DEC-15):* chốt **một đề xuất duy nhất — `Chính sách Đề xuất 2026`** (tên làm việc cũ: "Chính sách Lai") trên mô hình khu vực 45 đại lý, 1,2 tỷ FYP/tháng. Các hướng đã cân nhắc giữ làm lịch sử thiết kế ở nhóm "Phân tích sâu" (mô hình 1 vùng 12 tỷ FYP/năm): Song Hành = Balanced (bản tiền thân), Song Hành siết K2 = Quality, Tiết kiệm tối đa = mốc chi phí thấp. **Chưa có biến thể Growth** — ghi nhận là khoảng trống so với yêu cầu "tối thiểu 3 hướng".
   - Pháp lý hiển thị ở trang 2: kiểm Điều 52 TT 67/2023 (thưởng + hỗ trợ ≤ 30% FYP, `CONDITIONAL`) cho từng phương án; trần 7% phí đóng 1 lần theo TT 96/2026 từ 01/01/2027 (`SOURCE_CLAIM`).
4. **Phân tích tác động lên 3 mục tiêu cốt lõi:** (a) Gia tăng doanh số, (b) Chất lượng kinh doanh, (c) Hiệu quả về mặt chi phí & ROI (có phân tích độ nhạy & điểm hòa vốn).
5. **Mô hình Excel tham chiếu có thể kiểm chứng độc lập** (tách Inputs / Formulas / Outputs + Golden Test Cases).
6. **Bản trình bày lãnh đạo** (Gói A — Interview Delivery, 5–7 trang/slide).

### P1 — Tầm nhìn Mở rộng của TJ (Chỉ triển khai khi P0 đã vững)
- **MAPA tính xuôi và tính ngược** (mở rộng lập kế hoạch lực lượng bán).
- **Marketing tuyển Sales** (phễu tuyển dụng đại lý).
- **Marketing tìm kiếm khách hàng** (phễu khách hàng & phân bổ ngân sách quảng cáo).
- **PO điều chỉnh tham số** (PO Decision Bridge cấu hình linh hoạt).
- **HTML Interactive Simulator** phiên bản đầu tiên (chỉ xây sau khi Excel đã kiểm chứng và có Parity Test).
  - *Cập nhật 1.2:* HTML đã trở thành sản phẩm trình bày chính (mục 6). Parity Test chạy mỗi lần mở trang và hiển thị ở trang "Cách tính & giả định" (60/60 ca mẫu). Excel **chỉ** chứa mô hình 1 vùng 12 tỷ (Balanced Hybrid / Song Hành), **không** có Chính sách Đề xuất 2026 và mô hình 45 đại lý.

### P2 — Tầm nhìn Dài hạn (Phát triển sau deadline 3 ngày)
- Tự động hóa đọc PDF, tối ưu hóa nâng cao (Operations Research), tích hợp CRM/Chatbot, hệ thống tính hoa hồng production, kết nối nền tảng quảng cáo.

---

## 3. Requirement Traceability Matrix — Ma trận Truy vết từ Yêu cầu Gốc

| Req ID | Vế yêu cầu gốc (Chị Nhi — `SRC-REQ-001`) | Tài liệu Nghiên cứu & Tri thức | Mô hình & Kiểm thử | Bằng chứng (Evidence) | Sản phẩm Khuyến nghị (Gói A) | Trạng thái |
|---|---|---|---|---|---|---|
| **REQ-01** | Phân tích các chính sách thu nhập giữa các công ty | `docs/research/wheel-check.md`, `knowledge/sources/source-registry.csv` (17 nguồn + `Revision_Class`), `knowledge/business-rules/business-rules-catalog.csv` (**112 rules × 25 cột**, 3 trạng thái Section 32), `knowledge/lookups/*` (`1,300` dòng PAF+, `113` dòng Chubb, `10` HSBH), `knowledge/policies/*` (3 Deep Guides, Cross-doc Map, **36 Role Mapping**), `knowledge/compensation/total-rewards-inventory.*` (**44 cấu phần × 33 metadata**), `outputs/working/competitor-benchmarking-12-methods.md` | `model/compensation/compensation_engine.py` + `outputs/working/W24_Compensation_Reference_Model_v1.xlsx` (14 sheets, Excel 2007 COM recalculated) | 7 tài liệu PDF gốc (116/116 trang, SHA-256 khớp 100%) + `qa/post-audit-remediation-register.md` + `qa/g1-coverage-audit-matrix.md` + `SRC-LAW-001..005` (`SOURCE_NOT_VERIFIED`) | Trang 2–3 Gói A (`outputs/interview/W24_Executive_Recommendation_Step1.md`) | **`DONE_SELF_VERIFIED`** *(chờ Independent Audit đợt 2)* |
| **REQ-02** | Đề xuất chính sách phù hợp tại thị trường VN | `docs/research/wheel-check.md` (Đ.51 & Đ.52 TT 67/2023, NĐ 97/2026, TT 96/2026), `docs/research/vietnam-market-suitability.md` (IAV/MOF 2024–2026), `outputs/working/strategic-recommendations-and-schemes.md` | Excel Sheets `04_Policy_Parameters`, `08_Indiv_Comp_12M`, `09_Mgr_Senior_Comp`, `12_Benchmark_And_Eval` (15 tiêu chí + Mandatory Gate G1–G3) | `ADOPT/ADAPT/AVOID` Matrix + `W24 Balanced Hybrid` (`PROPOSAL` / `SYNTHETIC ASSUMPTION`) + 2 biến thể Growth / Quality-First | Trang 1, 4, 5 & 7 Gói A | **`DONE_SELF_VERIFIED`** *(PROPOSAL — chờ TJ/Chị Nhi duyệt)* |
| **REQ-03** | Thúc đẩy gia tăng doanh số | `outputs/working/competitor-benchmarking-12-methods.md` (12 phương pháp), `outputs/working/strategic-recommendations-and-schemes.md` | `compensation_engine.py` + Excel Sheets `07`, `08`, `09`, `13_MAPA_And_Financial` (MAPA Forward/Reverse) | 40 ca Python Golden lịch sử được đối soát trong bộ unittest + `20/20` Excel Live Golden Tests PASS (`14_QA_Golden_Tests`) | Trang 3 & 5 Gói A | **`DONE_SELF_VERIFIED`** |
| **REQ-04** | Thúc đẩy chất lượng kinh doanh | `docs/specifications/evaluation-framework-and-rubric.md`, `outputs/working/competitor-benchmarking-12-methods.md` (Method 06 & 07) | Excel Sheets `04` (Conflict toggles & K2 Hard Floor 60% + T+1 hold), `08` (CH Offset), `09` (Neg FYC, Indirect Gate 15M, Q3 Cliff, 3Y Deferral), `10_Total_Rewards_Ledger` | Kiểm thử biên K2 (`82%/72%/62%/55%`), symmetric negative FYC (`-144M`), TOT `<85%` forfeiture, T+1 holdback & 6M/12M clawback | Trang 3, 4 & 5 Gói A | **`DONE_SELF_VERIFIED`** |
| **REQ-05** | Hiệu quả về mặt chi phí và ROI | `outputs/working/strategic-recommendations-and-schemes.md`, `outputs/working/competitor-benchmarking-12-methods.md` (Method 10 & 12) | Excel Sheets `10_Total_Rewards_Ledger`, `11_Hierarchy_Dist_Cost` (12B FYP Zero Double-Counting + Art.52 ≤30% Gate), `13_MAPA_And_Financial` (Break-Even Margin Sensitivity) | `12/12` Enterprise Cost rows khớp `0.00%` giữa Excel 12.0 COM và Python; không bịa VNB margin (dùng Break-Even & Cost/Persisted Y2) | Trang 1, 3 & 6 Gói A | **`DONE_SELF_VERIFIED`** *(cần nạp VNB/OpEx nội bộ ở Bước 2)* |

---

> **Ghi chú số liệu 1.2:** các con số trong ma trận trên là tại thời điểm phiên bản 1.1. Hiện hành: **9 PDF / 135 trang** (thêm 2 văn bản Manulife cấp đại lý và quản lý nhóm — ghi "thông tin mật", DEC-14), **133 quy tắc** trong `business-rules-catalog.csv`. Đề xuất ở REQ-02 nay là Chính sách Đề xuất 2026 (mục 2, P0-3).

---

## 4. Tiêu chuẩn Trưởng thành Repository

- **Mục tiêu 3 ngày:** Đạt **Level 1 (Có tổ chức)** toàn repo và chứng minh **Level 2 (Có thể tái tạo kết quả)** trên các luồng tính toán trọng yếu (Compensation, MAPA, Cost/ROI sensitivity).
- Không tự nhận đạt cấp độ cao hơn khi chưa có bằng chứng kiểm thử thực tế.

---

## 5. Ranh giới Bảo mật & Chia sẻ

- **Gói A (`outputs/interview/W24_Executive_Recommendation_Step1.md`):** Gói trình bày sạch 7 trang cho chị Nhi. Chỉ chứa kết luận có bằng chứng, bảng so sánh, đề xuất, trade-offs, kết quả tài chính và lộ trình triển khai 90 ngày (tuyệt đối không kèm PDF nguồn hay working papers nội bộ).
- **Gói B (Working Papers):** Bản phân tích theo chính sách chia sẻ của repo (`outputs/working/`, `knowledge/`, `model/`, `tests/`, `qa/`).
- **GitHub PUBLIC:** DEC-07 và DEC-08 ghi nhận quyết định của TJ về chế độ hiển thị và công bố kèm disclosure. Quyền tái phân phối của từng nguồn được ghi riêng tại Source Registry và áp dụng theo [chính sách bảo mật và quyền tài liệu](docs/governance/confidentiality-and-rights-policy.md).

---

## 6. Sản phẩm HTML hiện hành (`outputs/interactive/W24_Strategy_Lab.html`) — cập nhật 1.2

| Thành phần | Phục vụ | Ghi chú |
|---|---|---|
| ★ **Tổng quan điều hành** (trang mặc định) | REQ-01…05 | Thẻ Đề bài + 9 PDF bấm mở đúng trang; 4 KPI (tổng chi / FYP, đỉnh stress test so trần 75%, điểm 5 tiêu chí, cơ chế cốt lõi); 2 biểu đồ (thu nhập 4 tầng L1–L4 theo Tháng/Quý/Năm; tổng chi / FYP với vạch trần 75%); 3 bước tiếp theo |
| **? Hướng dẫn** (hộp thoại) | Người đọc lần đầu | 5 phần: đề bài & mục tiêu · kết luận 3 dòng · phương pháp & giả định · cách đọc bằng chứng · lộ trình đọc 3 phút |
| Trang 1 · So sánh Thu nhập & Quyền lợi | REQ-01 | 4 mốc chuẩn L1–L4, trích dẫn `[Mã văn bản : trang]`; Tóm tắt 2 góc nhìn (đại lý / công ty) |
| Trang 2 · Phân tích Hành vi & Hiệu quả chi phí | REQ-03…05 | Tổng chi / FYP, độ nhạy K2 và cơ cấu sản phẩm, kiểm Điều 52 & TT 96, bẫy hành vi, chấm điểm 5 tiêu chí |
| Trang 3 · Chính sách Đề xuất 2026 & Phân vùng | REQ-02 | 2 đường ray Full-time / Part-time, K2 ≥ 80%, **4 vùng** theo lương tối thiểu NĐ 293/2025 (100/89/78/70%) |
| Phụ lục: Từ điển & Tài liệu gốc | Bằng chứng | Thuật ngữ + mục lục từng PDF |
| Nhóm "Phân tích sâu & công cụ" (thu gọn mặc định) | Truy vết | Trả lời đề bài chi tiết + khung giả định, mô hình 1 vùng 12 tỷ, thư viện 133 quy tắc, cách tính, tự chỉnh thông số |

**Định nghĩa đã chốt:** FYC chuẩn hóa = FYP × 30% làm cơ sở thưởng/phí quản lý; **trần tổng chi trả hệ thống đại lý 75% FYP** ở kịch bản xấu nhất (không phải tổng chi phí khai thác trên BCTC). ROI hiện là proxy (chi phí / FYP, chi phí / phí còn duy trì) — cần product mix & expense overrun từ Actuarial để tính VNB. Thí điểm 6–12 tháng ghép cặp với văn phòng đối chứng, đọc sớm sau 1 quý, K2 đo ở tháng 13–15.

**Chuẩn chấm giao diện:** `docs/UI_AUDIT_RUBRIC.md` (đậu ≥ 95 điểm và 0 lỗi P1 ở tiêu chí 1–2).

**Phát hành:** bản công khai dựng bằng `scripts/build_html.py --public` (lược dòng mật), quét bằng `scripts/check_public_build.py`, chỉ đẩy qua nhánh `public-release`; `main` local chứa dữ liệu mật không push.

**Khoảng trống còn mở:** biến thể Growth (P0-3); MAPA tính xuôi/ngược và phễu marketing (P1) chưa có trên HTML; Gói A (`outputs/interview/W24_Executive_Recommendation_Step1.md`) còn xoay quanh Balanced Hybrid — cần viết lại theo Chính sách Đề xuất 2026.
