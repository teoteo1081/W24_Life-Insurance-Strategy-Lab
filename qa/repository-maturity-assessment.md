# Repository Maturity Assessment — Đánh giá Trung thực Theo 12 Trụ cột (Scale 0–5)

**Ngày cập nhật:** 2026-11-26 *(Post-Independent-Audit Hardening Sprint — Kế thừa kết quả Codex Independent Audit tại `5cb7a21`)*  
**Thang đánh giá (theo Codex Audit):** `0` Ad hoc | `1` Organized | `2` Reproducible | `3` Configurable | `4` Extensible | `5` Governed Decision System.  
**Nguyên tắc bắt buộc:** Tổng thể bị ràng buộc bởi năng lực trọng yếu yếu nhất, **KHÔNG phải trung bình cộng** và **KHÔNG đếm số lượng file/rule/test để tự nâng cấp độ**. Mọi nâng cấp sau `5cb7a21` mang trạng thái **`SELF_VERIFIED`** cho đến khi Independent Auditor (Codex) xác nhận lại.

---

## 1. Bảng So sánh Trạng thái Trước (`5cb7a21` — Codex Audited) vs. Sau Hardening (`SELF_VERIFIED`)

| Trụ cột (12 Dimensions) | Codex Audited tại `5cb7a21` | Hiện trạng Sau Hardening (`SELF_VERIFIED`) | Bằng chứng Thực tế Cụ thể | Khoảng trống Còn lại (Chưa đạt Level cao hơn) |
|---|---|---|---|---|
| **1. Discoverability** | `1` (README stale Day 1) | **`2` (SELF)** | `README.md` đã viết lại sát thực tế, có Single Source of Truth map, Quick Start, hạn chế trung thực & lệnh chạy chuẩn; `EXECUTION_PLAN.md` đồng bộ. | Chờ Codex xác nhận độc lập. |
| **2. Traceability** | `2 partial` | **`2` (SELF)** | `scripts/validate_repo.py` kiểm tra tự động 17 nguồn (SHA-256 + `Redistribution_Rights_Status`), 112 quy tắc (0 tham chiếu `Rule_ID` gãy, valid enums), 3 lookup CSV. | Chưa có release manifest tự động nối 1 đầu ra cụ thể ngược về từng version (P2). |
| **3. Reproducibility** | `1` (FAIL — no workbook builder / clone / env) | **`2` (SELF)** | `requirements.txt`, `scripts/run_checks.py`, `scripts/build_workbook.py` (không ghi đè `v1.xlsx`), `scripts/verify_workbook_excel.py` (COM recalc + perturbation + parity) và clean-clone test trên bản sao tạm sạch. | Chưa kiểm chứng trên OS thứ hai (Linux/macOS); Excel COM phụ thuộc Windows + MS Excel. |
| **4. Maintainability** | `1` | **`1–2` (SELF)** | Đã thêm validation helpers tập trung & tách scripts rõ ràng; vẫn còn trùng lặp công thức giữa Python và Excel (chưa refactor diện rộng theo nguyên tắc Sprint Level 2). | Cần Level 3/4 modular adapters & shared operators (`level3-level4-architecture-advisory.md`). |
| **5. Extensibility** | `1` (FAIL vs claims) | **`1` (Honest)** | **Không nâng giả:** Đã sửa tài liệu thừa nhận trung thực engine dùng hàm riêng từng công ty, `schema/catalog` chưa điều khiển runtime; đã lập Dependency Map & Level 3/4 Advisory. | Chưa đạt Level 3 (config-driven) hay Level 4 (thêm hãng mới không sửa core). |
| **6. Testability** | `1` (`unittest discover=0`, NaN bypass) | **`2` (SELF)** | `python -m unittest discover -s tests -v` tự động nhận diện đầy đủ Golden, Validation/NaN Regression & Quality Gate tests; `assert_close` chặn `NaN/±Inf/bool`; `GT-16` dùng hằng số tính tay độc lập; fail khi 0 test chạy. | Chờ Codex kiểm toán độc lập. |
| **7. Auditability** | `2 partial` | **`2` (SELF)** | Có `qa/excel-reproducibility-evidence.json` (dated run manifest cho Excel COM + perturbation), `qa/post-audit-remediation-register.md`, và báo cáo Confidentiality/Rights lưu ngoài repo PUBLIC. | Toàn bộ bằng chứng Sprint mới đang ở mức `SELF_VERIFIED`. |
| **8. Security & Publication Control** | **`0` (FAIL — public restricted PDFs)** | **`1` (PARTIAL — Governance Improved, Rights Still OPEN)** | **Trung thực không chấm 100%:** Đã ban hành `docs/governance/confidentiality-and-rights-policy.md`, gắn `Redistribution_Rights_Status` (`RESTRICTED_INTERNAL` cho Manulife, `PERMISSION_UNKNOWN` cho 6 PDF AIA/Chubb), xóa 10 đường dẫn tuyệt đối cục bộ (`file://`), thêm hygiene gate (0 secrets/0 skill leaks). **NHƯNG** 7 PDF bên thứ ba vẫn đang tồn tại trên repo PUBLIC chờ TJ chốt `DEC-08`! | Cần TJ quyết định `DEC-08` (tách Public Portfolio sạch dùng synthetic data hoặc có xác nhận quyền phân phối). |
| **9. Portability** | `1` | **`1–2` (Windows Verified / Cross-OS Unproven)** | Đã khai báo môi trường `Python 3.12+` (`stdlib` core + `openpyxl`), xóa sạch 10 đường dẫn cục bộ không khả chuyển, chạy sạch trên fresh local clone. | **Không tuyên bố cross-OS portability** vì chưa chạy thử trên Linux/macOS; Excel COM chỉ chạy trên Windows có MS Excel. |
| **10. Recoverability** | `2` | **`2` (SELF)** | Git sạch không rewrite history (`7bcf70e → 5c2d13b → 852ca87 → 5cb7a21 → local hardening`), workbook tái lập được từ code mà không ghi đè `v1.xlsx`. | — |
| **11. Governance** | `2` | **`2` (SELF)** | Đồng bộ rõ vai trò BO (`TJ`), Executor (`AGY`), Independent Auditor (`Codex`) tại `AGENTS.md`; tách Single Source of Truth tại `README.md`/`HANDOVER.md`; ghi nhận đầy đủ `DEC-01..09`. | Còn 8 quyết định mở (`DEC-01..06`, `DEC-08..09`). |
| **12. Cost Efficiency (Onboarding/AI Reuse)** | `1` | **`2` (SELF)** | 1 lệnh duy nhất `python scripts/run_checks.py` thay thế việc AI phải đọc lại toàn bộ CSV/tài liệu; `README.md` + `HANDOVER.md` cho phép tiếp quản nguội nhanh. | — |

---

## 2. Kết luận Tổng thể về Mức độ Trưởng thành (Trung thực — Không Thổi phồng)

- **Audited Baseline (`5cb7a21` — Codex):** **Level 1 (Organized)** với năng lực Level 2 giới hạn trong Python.
- **Hiện trạng Sau Sprint Hardening (`SELF_VERIFIED`):**
  - **Kỹ thuật Tái lập (Reproducibility, Testability, Quality Gates, Workbook Build, Clean Clone trên Windows):** Đạt toàn bộ tiêu chí **Level 2 (Reproducible — `SELF_VERIFIED`)** trong phạm vi môi trường đã khai báo (Python 3.12 + openpyxl + Windows Excel 12.0 COM).
  - **Tổng thể toàn Repository (Ràng buộc bởi điểm yếu nhất):** Báo cáo trung thực là **`Level 2 PARTIALLY DEMONSTRATED (SELF_VERIFIED — Pending Independent Audit & Open DEC-08 Rights / Cross-OS Portability)`** vì: (1) chưa có Codex kiểm toán độc lập đợt 3, (2) vấn đề quyền tái phân phối 7 PDF công khai (`DEC-08`) vẫn `OPEN`, và (3) chưa chạy thực nghiệm trên máy/hệ điều hành thứ hai.
  - **Level 3 (Configurable) & Level 4 (Extensible):** **CHƯA ĐẠT** (mới dừng ở bản đồ phụ thuộc và đề xuất kiến trúc tại `docs/architecture/level3-level4-architecture-advisory.md`).
