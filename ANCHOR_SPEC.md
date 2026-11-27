# ANCHOR_SPEC.md — Mục tiêu, Business Anchor và Phạm vi Chuẩn

**Dự án:** W24 — Life Insurance Strategy Lab  
**Phiên bản:** 1.1 (Cập nhật Business Anchor nguyên văn ngày 2026-11-26)  
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
| **REQ-01** | Phân tích các chính sách thu nhập giữa các công ty | `docs/research/wheel-check.md`, `knowledge/sources/source-registry.csv` (17 nguồn + `Revision_Class`), `knowledge/business-rules/business-rules-catalog.csv` (**112 rules × 25 cột**, 3 trạng thái Section 32), `knowledge/lookups/*` (`1,300` dòng PAF+, `113` dòng Chubb, `10` HSBH), `knowledge/policies/*` (3 Deep Guides, Cross-doc Map, **36 Role Mapping**), `knowledge/compensation/total-rewards-inventory.*` (**44 cấu phần × 33 metadata**), `outputs/working/competitor-benchmarking-12-methods.md` | `model/compensation/compensation_engine.py` + `outputs/working/W24_Compensation_Reference_Model_v1.xlsx` (14 sheets, Excel 2007 COM recalculated) | 7 tài liệu PDF gốc (116/116 trang, SHA-256 khớp 100%) + `qa/post-audit-remediation-register.md` + `qa/g1-coverage-audit-matrix.md` + `SRC-LAW-001..005` (`SOURCE_NOT_VERIFIED`) | Trang 2–3 Gói A (`outputs/interview/W24_Executive_Recommendation_Step1.md`) | **`DONE_SELF_VERIFIED`** *(chờ Independent Audit đợt 2)* |
| **REQ-02** | Đề xuất chính sách phù hợp tại thị trường VN | `docs/research/wheel-check.md` (Đ.51 & Đ.52 TT 67/2023, NĐ 97/2026, TT 96/2026), `docs/research/vietnam-market-suitability.md` (IAV/MOF 2024–2026), `outputs/working/strategic-recommendations-and-schemes.md` | Excel Sheets `04_Policy_Parameters`, `08_Indiv_Comp_12M`, `09_Mgr_Senior_Comp`, `12_Benchmark_And_Eval` (15 tiêu chí + Mandatory Gate G1–G3) | `ADOPT/ADAPT/AVOID` Matrix + `W24 Balanced Hybrid` (`PROPOSAL` / `SYNTHETIC ASSUMPTION`) + 2 biến thể Growth / Quality-First | Trang 1, 4, 5 & 7 Gói A | **`DONE_SELF_VERIFIED`** *(PROPOSAL — chờ TJ/Chị Nhi duyệt)* |
| **REQ-03** | Thúc đẩy gia tăng doanh số | `outputs/working/competitor-benchmarking-12-methods.md` (12 phương pháp), `outputs/working/strategic-recommendations-and-schemes.md` | `compensation_engine.py` + Excel Sheets `07`, `08`, `09`, `13_MAPA_And_Financial` (MAPA Forward/Reverse) | 40 ca Python Golden lịch sử được đối soát trong bộ unittest + `20/20` Excel Live Golden Tests PASS (`14_QA_Golden_Tests`) | Trang 3 & 5 Gói A | **`DONE_SELF_VERIFIED`** |
| **REQ-04** | Thúc đẩy chất lượng kinh doanh | `docs/specifications/evaluation-framework-and-rubric.md`, `outputs/working/competitor-benchmarking-12-methods.md` (Method 06 & 07) | Excel Sheets `04` (Conflict toggles & K2 Hard Floor 60% + T+1 hold), `08` (CH Offset), `09` (Neg FYC, Indirect Gate 15M, Q3 Cliff, 3Y Deferral), `10_Total_Rewards_Ledger` | Kiểm thử biên K2 (`82%/72%/62%/55%`), symmetric negative FYC (`-144M`), TOT `<85%` forfeiture, T+1 holdback & 6M/12M clawback | Trang 3, 4 & 5 Gói A | **`DONE_SELF_VERIFIED`** |
| **REQ-05** | Hiệu quả về mặt chi phí và ROI | `outputs/working/strategic-recommendations-and-schemes.md`, `outputs/working/competitor-benchmarking-12-methods.md` (Method 10 & 12) | Excel Sheets `10_Total_Rewards_Ledger`, `11_Hierarchy_Dist_Cost` (12B FYP Zero Double-Counting + Art.52 ≤30% Gate), `13_MAPA_And_Financial` (Break-Even Margin Sensitivity) | `12/12` Enterprise Cost rows khớp `0.00%` giữa Excel 12.0 COM và Python; không bịa VNB margin (dùng Break-Even & Cost/Persisted Y2) | Trang 1, 3 & 6 Gói A | **`DONE_SELF_VERIFIED`** *(cần nạp VNB/OpEx nội bộ ở Bước 2)* |

---

## 4. Tiêu chuẩn Trưởng thành Repository

- **Mục tiêu 3 ngày:** Đạt **Level 1 (Có tổ chức)** toàn repo và chứng minh **Level 2 (Có thể tái tạo kết quả)** trên các luồng tính toán trọng yếu (Compensation, MAPA, Cost/ROI sensitivity).
- Không tự nhận đạt cấp độ cao hơn khi chưa có bằng chứng kiểm thử thực tế.

---

## 5. Ranh giới Bảo mật & Chia sẻ

- **Gói A (`outputs/interview/W24_Executive_Recommendation_Step1.md`):** Gói trình bày sạch 7 trang cho chị Nhi. Chỉ chứa kết luận có bằng chứng, bảng so sánh, đề xuất, trade-offs, kết quả tài chính và lộ trình triển khai 90 ngày (tuyệt đối không kèm PDF nguồn hay working papers nội bộ).
- **Gói B (Working Papers):** Bản phân tích theo chính sách chia sẻ của repo (`outputs/working/`, `knowledge/`, `model/`, `tests/`, `qa/`).
- **GitHub PUBLIC:** DEC-07 và DEC-08 ghi nhận quyết định của TJ về chế độ hiển thị và công bố kèm disclosure. Quyền tái phân phối của từng nguồn được ghi riêng tại Source Registry và áp dụng theo [chính sách bảo mật và quyền tài liệu](docs/governance/confidentiality-and-rights-policy.md).
