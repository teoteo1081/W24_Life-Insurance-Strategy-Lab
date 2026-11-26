# HANDOVER.md — Điểm Bàn giao & Single Source of Truth (Trạng thái Hiện hành)

**Cập nhật lần cuối:** 2026-11-26 *(Post-Independent-Audit Hardening & Level 2 Maturity Sprint — Sau Codex Independent Audit lần 2 tại `5cb7a21`)*  
**Business Owner:** TJ | **Implementation Agent:** AGY | **Independent Auditor:** Codex (`W24_Independent_Audit_5cb7a21.md`, lưu ngoài repo PUBLIC)

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
| `scripts/build_workbook.py` + `scripts/verify_workbook_excel.py` | **PASS** (`overall_pass: true`) | Dựng lại 14 sheets (`915` công thức, không ghi đè `v1.xlsx`); Microsoft Excel 12.0 COM recalculation: `0` lỗi, `20/20` Excel Golden PASS, `12/12` Parity PASS; **2 live input perturbations PASS** (`C19: 0.16→0.20` → `60.91%/7.39%`; `C5: Table_80→Example_50` → `1.00`); tương đương chức năng 100% với `v1.xlsx`. Bằng chứng: `qa/excel-reproducibility-evidence.json`. |
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
