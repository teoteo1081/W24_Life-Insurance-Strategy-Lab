# HANDOVER.md — Điểm Bàn giao & Single Source of Truth (Trạng thái Hiện hành)

**Cập nhật lần cuối** 2026-11-26 (đêm) — Trang HTML tương tác, phương án Song Hành, bằng chứng trên R2

## Trạng thái hiện hành

**2026-11-27 — Giai đoạn 1 (Bảng soi tiền 3 cấp quản lý) xong, CHỜ TJ DUYỆT, chưa commit.**
- Sản phẩm: `outputs/interview/01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md`, sinh bằng `python scripts/build_interview_income_table.py` (không gõ tay số).
- Đối chiếu lại 7 PDF gốc (SHA-256 khớp registry; Chubb RD đọc bằng ảnh trang). Sửa engine + workbook: F1 Chubb AL quý ngưỡng 50tr; F2–F4 Chubb RD bảng EHC, bảng FYP, bảng tăng trưởng 12 bậc; F5 thêm phí RYC của AL (CHB-MG-008); F6 thêm gián tiếp AIA cấp 3–4. Test mới `tests/test_pdf_table_fixes.py`.
- Hệ quả: Chubb ở K2 82% = **99,96% FYP** (trước 99,21%). Song Hành không đổi (mục tiêu tầng lãnh đạo vẫn theo Manulife).
- Kiểm: 54/55 unittest đạt; 1 fail và quality gate fail **chỉ vì thiếu `private/sources/`** trong checkout này (PDF có ở thư mục Downloads, hash khớp). Excel COM 12.0: 0 lỗi, 20/20 golden, 12/12 parity Python–Excel; `v1.xlsx` không còn giống vì chứa số sai cũ (chưa ghi đè, cần TJ quyết).
- TJ cần quyết: cấu trúc tổ chức A5; cấp 3 so ở tuyến quản lý trung gian hay lãnh đạo vùng; FYC/FYP 30%; có thay `v1.xlsx` bằng bản đã sửa không.

**Sản phẩm trình bày cho chị Nhi:** `outputs/interactive/W24_Strategy_Lab.html` (1 file, mở trực tiếp hoặc qua localhost; dựng lại bằng `py -3 scripts/build_html.py`).
- Slicer phương án (Song Hành ⭐ / Cân bằng / Thưởng Theo Chất / Tự chỉnh), thanh K2 50–95%, 9 tab: Tổng quan, Thu nhập theo tầng, Chi phí & ROI, Chấm điểm, Tự chỉnh thông số, So sánh cơ chế, Cách tính, Bằng chứng, Giả định & giới hạn.
- Phương án đề xuất tính trực tiếp bằng `web/engine.js`; `tests/test_web_parity.py` so 240 ca với Python (đạt, lệch < 0,02tr do làm tròn). Trang tự kiểm 60 ca mẫu khi mở.
- Bằng chứng: 7 PDF trên R2 qua Worker chỉ-đọc `tj-w24-evidence` (DEC-11), link mở đúng trang `#page=N`. Kiểm mẫu độc lập 14/112 quy tắc: 14/14 khớp (`qa/spot-check-14-rules.md`).

**Mô hình (PROPOSAL / MODEL_OUTPUT, không phải ROI thực tế):**
- Thu nhập đại lý 3 năm có tái tục (`scripts/agent_income_multiyear.py`, giả định chung 20%/10%). Phương án Cân bằng cũ trả thấp nhất thị trường ở mọi tầng.
- Song Hành (`scripts/calibrate_song_hanh.py`): Cân bằng + thưởng tái tục 50% + trả chậm nhiều hơn, rồi nâng tối thiểu để không tầng nào thấp nhất thị trường ở K2 82%. Kết quả K2 82%: chi phí 66,6% FYP (AIA 73,4%, Chubb 99,2%). Giới hạn: mức "không thấp nhất" chỉ giữ ở K2 ~75–90%.
- Rubric v2 (14 tiêu chí, tính trực tiếp): ở K2 82% Thưởng Theo Chất dẫn 3/4 góc nhìn (3,57 so với Song Hành 3,45), Chubb dẫn góc "Ưu tiên tuyển dụng". Phép thử tách nguyên nhân: phần dẫn đến từ sàn K2 65% (vách đá); với sàn 60% Song Hành dẫn cả 4. Đã thêm Q3 (sốc thu nhập khi K2 giảm) theo căn cứ có từ trước; không chỉnh thêm.

**TJ cần quyết (sáng 2026-11-27):**
1. Khuyến nghị chính: Song Hành (không vách đá, an toàn cho lực lượng) hay Thưởng Theo Chất (điểm rubric cao hơn nhưng có vách đá 65%)?
2. Push 4 commit local lên GitHub (PUBLIC) — cần TJ xác nhận.
3. Token Cloudflare `CF_W24_TOKEN` hết hạn 2026-12-26.

## Bản vá F-01–F-05 (trước đó cùng ngày)

- **F-01/F-02** — Đồng bộ cách diễn đạt pháp lý thành `CONDITIONAL` / `SOURCE_NOT_VERIFIED`, sửa thông tin chế độ PUBLIC của repo và dẫn chiếu chính sách quyền tài liệu.
- **F-03/F-04** — Kiểm tra đầu vào tùy chọn và thứ tự ngưỡng. Python và workbook áp trần hiệu dụng Direct Override 36% của phương án W24. Validator kiểm SHA-256, PDF thiếu hoặc chưa đăng ký, Source_ID, trạng thái rule và hygiene của file chưa stage. Validator chạy được trên bản xuất thiếu metadata Git.
- **F-05** — Sửa truy vết nguồn, chú thích SAF và phạm vi đối chiếu workbook. Record `AIA-CV-023` ghi rõ engine nhận FY đã tính sẵn và hỗ trợ các chế độ làm tròn. Công thức FY 14 tháng từ phí và chuyển giao chưa được triển khai.
- **`SELF_VERIFIED`** — 35/35 unittest và quality gates đạt. Workbook dựng lại có 14 sheet và 915 công thức. COM 12.0 trả 0 lỗi công thức, 20/20 Golden, 12/12 enterprise parity và 2/2 perturbations. Ca AIA CQL âm M04 khớp ở −54 triệu VND trong cả hai mô hình theo giả định FYC có dấu đã dùng trong Python.
- **Level 2 vẫn `PARTIAL`** — Cần kiểm chứng độc lập bản vá và chạy lại trên Microsoft Excel 16.0. Phạm vi đã xác minh pháp lý và quyết định làm tròn FY giữ trạng thái hiện có. Bản vá lưu cục bộ.

---

## Kết quả kiểm toán snapshot `a308f0f` — Lịch sử (2026-11-26)

- **VERIFIED FACT:** Codex kiểm chứng độc lập snapshot `a308f0f` bằng Microsoft Excel **16.0**, đối chiếu executable Office16 trong phiên tương tác: full recalculation, lưu và đọc lại thành công; **0** lỗi công thức, **20/20** Golden, **12/12** Python/Excel parity, **2/2** perturbations đạt. Workbook dựng lại có **14 sheets / 915 công thức**.
- **Phạm vi equivalence:** cùng tên sheet, 20 Golden values và 12 enterprise scenario outputs so với `v1.xlsx`; không khẳng định tương đương mọi ô hoặc mọi miền đầu vào.
- **VERIFIED FACT:** Đã khôi phục F-01…F-05; các findings vẫn **OPEN**. Codex tái lập các lỗi trọng yếu về optional-input `NaN/Inf`, thresholds đảo thứ tự và validator. Tổng thể Level 2 tại snapshot là **PARTIAL**.
- **COM:** Đăng ký theo người dùng trỏ WPS, cấp máy trỏ Microsoft Excel. Khởi động trực tiếp Office16 và giữ cùng COM instance đã cho phép kiểm chứng Microsoft Excel 16.0. Nguyên nhân chính xác của lỗi `80080005` trước đây vẫn **UNKNOWN**; chưa chứng minh do sandbox. Bằng chứng AGY COM 12.0 trước đây giữ trạng thái `SELF_VERIFIED`, không dùng thay cho lượt Codex 16.0.
- **Bằng chứng:** Báo cáo `Codex_Targeted_Level2_Closure_a308f0f.md`, `codex-ms-excel-results.json`, transcript COM và probes được giữ ngoài repository PUBLIC; không đưa bằng chứng chi tiết vào commit.
- **Tiếp theo:** TJ duyệt riêng việc vá F-01…F-05 bởi AGY, sau đó kiểm chứng độc lập; Level 3 chưa được triển khai. Phê duyệt commit/push tài liệu hiện tại được ghi tại **DEC-10**.

Các mục dưới lưu kết quả bàn giao theo từng giai đoạn trước bản vá.

---

## 1. Trạng thái Trưởng thành & Kiểm chứng Hiện tại (Trung thực — Không Thổi phồng)

- **Audited Baseline (`5cb7a21` — Codex):** **Level 1 (Organized)** với năng lực Level 2 giới hạn trong Python; `Repository Reproducibility = FAIL`, `Architecture Extensibility = FAIL`, `Public Portfolio Readiness = FAIL`.
- **Sau Sprint Hardening (Local Commit — `SELF_VERIFIED`, CHƯA phải `INDEPENDENTLY_VERIFIED`):**
  - **Level 2 Technical Reproducibility (Windows / Python 3.12 + openpyxl + MS Excel 12.0 COM):** Đã triển khai và tự kiểm chứng đầy đủ (`unittest discover`, `NaN/±Inf/UNKNOWN` validation, reproducible workbook build + Excel COM perturbation, automated quality gates, clean-clone verification).
  - **Tổng thể Repository:** **`Level 2 PARTIALLY DEMONSTRATED (SELF_VERIFIED)`** vì: (1) chưa có Codex Independent Audit đợt 3, (2) 7 PDF bên thứ ba trên repo `PUBLIC` tuy đã được Business Owner (TJ) chấp nhận giữ công khai kèm phân loại quyền (`DEC-08` Option C) nhưng vẫn mang trạng thái `RESTRICTED_INTERNAL` / `PERMISSION_UNKNOWN` về mặt quyền tái phân phối bên thứ ba, và (3) chưa kiểm chứng trên hệ điều hành thứ hai (Linux/macOS).
  - **Level 3 (Configurable) & Level 4 (Extensible):** **CHƯA ĐẠT** (xem bản đồ phụ thuộc & lộ trình đề xuất tại `docs/architecture/level3-level4-architecture-advisory.md`).

---

## 2. Kết quả Kiểm thử & Kiểm chứng Mới nhất (`SELF_VERIFIED`)

| Lệnh / Kiểm chứng | Kết quả Thực tế | Bằng chứng / Ghi chú |
|---|---|---|
| `python scripts/run_checks.py` | **PASS** (exit `0`) | 1 lệnh chạy tuần tự: Quality Gates + `unittest discover` + Example Scenario (từ chối PASS nếu 0 test). |
| `scripts/validate_repo.py` | **PASS** (`0` errors) | Kiểm 17 nguồn (`Redistribution_Rights_Status` + 7 PDF SHA-256), 112 rules (0 broken `Rule_ID`, valid enums), 3 lookups (`1,300` PAF+ 0 sai lệch tổng, `113` Chubb, `10` HSBH), 36 roles, 44 rewards, JSON schema, và 0 hygiene/path/secret leaks. |
| `python -m unittest discover -s tests -v` | **`31` test cases PASS** (`0` fail, `0` error) | Gồm `18` Golden `TestCase` methods (`test_compensation_golden.py`, `GT-16` dùng hằng số độc lập), `9` NaN/Inf/Validation/Negative/Lookup Regression methods (`test_validation_and_regression.py`), `4` Quality Gate & Seeded-Defect methods (`test_quality_gates.py`). |
| `scripts/build_workbook.py` + `scripts/verify_workbook_excel.py` | **PASS** (`overall_pass: true`) | Dựng lại 14 sheets (`915` công thức, không ghi đè `v1.xlsx`); Microsoft Excel 12.0 COM recalculation: `0` lỗi, `20/20` Excel Golden PASS, `12/12` Parity PASS; **2 live input perturbations PASS** (`C19: 0.16→0.20` → `60.91%/7.39%`; `C5: Table_80→Example_50` → `1.00`); khớp tên sheet, 20 Golden values và 12 enterprise outputs trong phép đối chiếu với `v1.xlsx`. Bằng chứng: `qa/excel-reproducibility-evidence.json`. |
| Clean Environment `git clone` Test (Windows) | **PASS** *(xem báo cáo Checkpoint)* | Chạy độc lập từ bản clone sạch ngoài repo (0 file scratch/session AI): `run_checks.py` + `build_workbook.py` + `verify_workbook_excel.py` đều PASS. *Cross-OS chưa kiểm thử.* |
| Confidentiality & Document Rights Review | **Lưu ngoài repo PUBLIC** | `0` secrets, `0` protected skill leaks, đã xóa sạch 10 đường dẫn cục bộ. Chi tiết quyền từng PDF lưu tại `%LOCALAPPDATA%\W24\Hardening-Private\W24_Confidentiality_And_Rights_Review_5cb7a21.md`. |

---

## 3. Khôi phục & Làm rõ Ranh giới Nghiệp vụ / Pháp lý / ROI

- **Modeled Thresholds ≠ Actual ROI:** Toàn bộ kết quả trong Gói A (`outputs/interview/W24_Executive_Recommendation_Step1.md`) và Gói B là **Modeled Payout / Modeled Distribution Cost / Modeled Break-Even Gross Margin** trên kịch bản 1 Vùng `12 tỷ FYP` (`OpEx 15–25%` giả định), **KHÔNG phải ROI thực tế hay tăng trưởng đã chứng minh** (`VNB Margin`, `OpEx` thực & cohort mix là `UNKNOWN`).
- **Pháp lý (`CONDITIONAL / SOURCE_NOT_VERIFIED`):** Đã cập nhật metadata Cổng TTĐT Chính phủ cho `TT 67/2023`, `NĐ 97/2026` (`31/03/2026`), `TT 96/2026` (`02/07/2026`) và Văn bản hợp nhất `44/2026/VBHN-TT-BTC` (`29/09/2026` — `SRC-LAW-005`). Không suy diễn ngày hiệu lực từng điều khoản từ metadata văn bản; giữ cổng pháp lý `CONDITIONAL` chờ Pháp chế rà soát toàn văn (`DEC-03`).

---

## 4. Trạng thái Git & Quyết định Mở Cần TJ (`docs/decisions/decision-register.md`)

- **Repository GitHub:** `https://github.com/teoteo1081/W24_Life-Insurance-Strategy-Lab` (`PUBLIC` theo `DEC-07` & `DEC-08` Option C).
- **Nhánh & Sync:** Nhánh `main` đã đồng bộ lên `origin/main` theo phê duyệt tường minh của TJ (`DEC-09` Option B: giữ nguyên nội dung kỹ thuật `eda2564`, chỉ bổ sung commit ghi nhận `DEC-08`/`DEC-09` và push công khai ngay; 5 điểm tự kiểm toán nhỏ `[F-01..F-05]` được chủ động giữ để gom xử lý sau Codex Independent Audit Đợt 3).
- **6 Quyết định Mở Còn lại (`DEC-01..06`):**
  - **`DEC-03` (P0 trước ban hành):** Đối chiếu toàn văn Văn bản hợp nhất `44/2026/VBHN-TT-BTC` & `NĐ 97/2026` với Pháp chế/Kế toán.
  - **`DEC-01` & `DEC-02`:** Phân xử 2 xung đột nguồn gốc (`ERR-DOC-01` Chubb `W1`, `ERR-DOC-02` AIA làm tròn).
  - **`DEC-04`, `DEC-05`, `DEC-06`:** Thu thập tài liệu thiếu (Manulife FA/UM, AIA Exchange/HH, Chubb `260005V`/BD), chốt trọng số/biến thể, và nạp VNB/OpEx nội bộ cho Bước 2.
- **3 Quyết định Đã Đóng:** `DEC-07` (`CLOSED — OPTION D`), `DEC-08` (`CLOSED — OPTION C: PUBLIC WITH DISCLOSURE`), `DEC-09` (`CLOSED — OPTION B: PUSH NOW`).

---

## 5. Hành động Tiếp theo (Sau khi Đồng bộ `origin/main`)

1. Mời Independent Auditor (**Codex**) kiểm toán **Đợt 3** trên nhánh `main` đã đồng bộ (`origin/main`) để xác nhận độc lập các năng lực Level 2.
2. Sau báo cáo Codex Đợt 3, gom xử lý 1 lần các phát hiện mới (nếu có) cùng 5 điểm tự kiểm toán đã ghi nhận (`[F-01..F-05]`).
3. Chỉ sau khi TJ duyệt: triển khai **Level 3 Vertical Slice** theo `docs/architecture/level3-level4-architecture-advisory.md`.
