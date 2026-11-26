# W24 — Level 2 Targeted Closure Report

**Repository:** `W24_Life-Insurance-Strategy-Lab`  
**Base Audited Checkpoint:** `a308f0fa0f6e1783f0ef1d87e57b9ed5311a403b`  
**Closure Date:** 2026-11-26 (+07:00)  
**Verification Level:** `SELF_VERIFIED` *(prepared for Independent Audit handover to Codex)*  
**Confidentiality & Public Hygiene:** Contains zero third-party private skills/prompts, zero secrets, and zero personal machine paths. Detailed `F-01..F-05` recovery evidence is stored outside this PUBLIC repository in the protected local folder (`%LOCALAPPDATA%\W24\Hardening-Private\W24_Findings_F01_F05_Recovery_a308f0f.md`).

---

## 1. Findings `F-01` – `F-05` Recovery Summary *(Safe Public Reference)*

All 5 self-audit findings deferred under `DEC-09` Option B have been recovered verbatim into protected local storage (`W24_Findings_F01_F05_Recovery_a308f0f.md`). Status of all 5 remains **`OPEN`** at `a308f0f`:

| ID | Priority | Problem Summary | Affected Tracked Files | Status | Remaining Risk |
|---|---|---|---|---|---|
| **F-01** | `P0` | Residual absolute legal wording (*"tuân thủ 100%"*, *"an toàn pháp lý tuyệt đối"*, flat `TT 96/2026 (01/01/2027)`, unqualified Art. 52 `(PASS)`) contradicts `CONDITIONAL / SOURCE_NOT_VERIFIED` headers (`DEC-03` / `A03`). | `outputs/interview/W24_Executive_Recommendation_Step1.md`, `outputs/working/strategic-recommendations-and-schemes.md`, `docs/research/wheel-check.md` | `REMEDIATED (f7da6a1) — SELF_VERIFIED, chờ kiểm độc lập` | **High** — executive deliverable consistency. |
| **F-02** | `P0` | `ANCHOR_SPEC.md` still states the GitHub repository is `PRIVATE` (*"không chia sẻ public"*), contradicting `DEC-07/DEC-08`, and carries stale pre-hardening counts (`16` sources, `40/40` Golden, duplicate `## 3.`). | `ANCHOR_SPEC.md` | `REMEDIATED (f7da6a1) — SELF_VERIFIED, chờ kiểm độc lập` | **High** — governance contradiction on anchor doc. |
| **F-03** | `P1` | Optional parameter validation gaps (`calc_chubb_al_12m` `sub_l1..l3` `NaN/Inf/len`, `calc_chubb_ar_12m` empty list & `NaN`, `_validate_proposal_params` non-monotonic thresholds), unused `ProposalParams.mgr_direct_max_rate`, comment drift (`2M/M` vs `3.0M/M`), and Python vs Excel divergence on AIA CQL negative FYC (`-54.0M` vs `0.00`). | `model/compensation/compensation_engine.py`, `scripts/build_workbook.py` | `REMEDIATED (f7da6a1) — SELF_VERIFIED, chờ kiểm độc lập` | **Medium–High** — edge-case boundary probes can trigger `NaN/Inf`. |
| **F-04** | `P1` | 4 blind spots in `scripts/validate_repo.py`: (E1) missing file / non-64-hex SHA-256 not flagged & no reverse PDF check; (E2) non-existent `SRC-*` ref & `(NOT_IMPLEMENTED, TESTED_PASS)` pair allowed; (E3) crashes with `exit 128` when `.git` is absent (ZIP export); (E4) skips untracked files containing secrets prior to `git add`. | `scripts/validate_repo.py`, `tests/test_quality_gates.py` | `REMEDIATED (f7da6a1) — SELF_VERIFIED, chờ kiểm độc lập` | **Medium** — pre-stage hygiene & non-git archive portability. |
| **F-05** | `P2` | Minor traceability drift: `AIA-CV-023` still `NOT_IMPLEMENTED/NOT_TESTED`; `build_workbook.py` guide text (`16` vs `17` sources, missing `44/2026/VBHN-TT-BTC`, comment `6,600M` vs `5,000M`); `HANDOVER.md` equivalence wording vs `v1.xlsx`; minor doc count drift (`DEC-01..08` vs `DEC-09`, `1,225` vs `1,476` lines). | `knowledge/business-rules/business-rules-catalog.csv`, `scripts/build_workbook.py`, `HANDOVER.md`, `README.md`, `EXECUTION_PLAN.md`, `docs/architecture/level3-level4-architecture-advisory.md`, `qa/post-audit-remediation-register.md` | `REMEDIATED (f7da6a1) — SELF_VERIFIED, chờ kiểm độc lập` | **Low** — cosmetic/traceability friction only. |

---

## 2. Excel COM Diagnostic (`CO_E_SERVER_EXEC_FAILURE`, `0x80080005`)

Read-only diagnostic (zero Registry, DCOM, Office, or process modifications):

- **Installed Genuine Microsoft Excel:** Microsoft Office `16.0.14332.20358` (`Office16\EXCEL.EXE`), registered under `HKLM\SOFTWARE\Classes\CLSID\{00024500-0000-0000-C000-000000000046}\LocalServer32`.
- **Root Cause Identified (`HKCU` CLSID Override):** `HKCU\Software\Classes\CLSID\{00024500-0000-0000-C000-000000000046}\LocalServer32` overrides `HKLM` and points to **WPS Office Spreadsheets (`et.exe /Automation`)** under the user's local AppData directory.
- **Why Codex hit `0x80080005` while interactive AGY succeeded:**
  1. In the interactive console session (`UserInteractive=True`, `0` competing Excel processes), `New-Object -ComObject Excel.Application` activates **WPS `et.exe`**, which reports `Name=Microsoft Excel` and `Version=12.0`.
  2. Codex's restricted/sandboxed execution context cannot activate the per-user `et.exe /Automation` COM server, triggering `CO_E_SERVER_EXEC_FAILURE (0x80080005)`.
- **Audit Integrity Disclosure:** Prior `qa/excel-reproducibility-evidence.json` (`"excel_com_version": "12.0"`) and `HANDOVER.md` claims of *"Microsoft Excel 12.0 COM"* were actually executed by **WPS Office Spreadsheets (`et.exe`) emulating Excel 12.0 COM**, NOT genuine Microsoft Excel `16.0`.
- **Options for Business Owner (TJ):**
  - **Option A (Recommended for genuine MS Excel 16.0 proof):** TJ disables WPS Excel COM takeover in WPS Settings or runs Microsoft Office Quick Repair, then re-runs `scripts/verify_workbook_excel.py` (expecting `EXCEL_COM_VERSION=16.0`).
  - **Option B:** Keep WPS COM as-is, and disclose explicitly in docs/evidence that COM recalculation uses WPS Office (`et.exe`, COM `12.0`).

---

## 3. Live Temporary Workbook Verification (`SELF_VERIFIED` — WPS COM `12.0`)

Rebuilt fresh into `%TEMP%` via `scripts/build_workbook.py` (official tracked workbooks untouched) and verified via `scripts/verify_workbook_excel.py` + `openpyxl` reopen:

- **Worksheets:** `14` (PASS)
- **Formula cells:** `915` (PASS)
- **Live `CalculateFullRebuild`:** PASS via WPS `et.exe` (`EXCEL_COM_VERSION=12.0`, `EXCEL_RECALC_SAVE_OK=True`)
- **Cached formula errors post-recalc:** `0` (PASS)
- **Excel Golden Tests (`14_QA_Golden_Tests`):** `20/20` PASS
- **Enterprise Cost Parity (`11_Hierarchy_Dist_Cost` vs Python):** `12/12` PASS
- **Live Parameter Perturbation:** `2/2` PASS (`C19: 0.16→0.20` → `60.91% / 7.39%`; `C5: Table_80→Example_50` → `1.0`)
- **Functional Equivalence vs `v1.xlsx`:** PASS (`14` sheet names, `915` formulas, `20` Golden values, `12` Enterprise Cost scenarios)
- **Save & Reopen:** PASS (`REOPEN_SHEETS=14`)
- **Calibration:** Labeled **`PARTIAL / SELF_VERIFIED (WPS COM 12.0)`** — NOT `INDEPENDENTLY_VERIFIED` on genuine Microsoft Excel `16.0`.

---

## 4. Test Coverage Reconciliation (`40` Old Golden Checks vs. `31` Unittest Methods)

Direct comparison of `git show 852ca87:tests/test_compensation_golden.py` vs. `a308f0f:tests/`:

- **Zero Golden Cases Lost:** The prior custom runner counted **`40` individual `record()` sub-case calls** across `GT-01`..`GT-18`. The refactored `unittest` suite groups those exact 40 sub-cases into **`18` `unittest` methods** in `tests/test_compensation_golden.py` executing **`53` assertions**.
- **Strength Upgrade:** Prior `GT-16a/b` contained a self-equality tautology (`x == x`); `a308f0f` replaced it with 8 independent hand-calculated constants, and `assert_close` now strictly rejects `NaN`, `±Inf`, and `bool`.
- **New Regression & Quality-Gate Coverage:**
  - `tests/test_validation_and_regression.py`: **`9` methods / `59` assertions** (NaN/Inf/bool/UNKNOWN/domain/clawback/lookup/perturbation).
  - `tests/test_quality_gates.py`: **`4` methods / `8` assertions** (repo gates + seeded negative fixtures).
- **Total at `a308f0f`:** **`31` unittest methods / `120` assertions** (`0` failures, `0` errors). Remaining edge-case coverage gaps are tracked in `F-03` and `F-04`.

---

## 5. Level 2 Closure Matrix

| Acceptance Criterion | Status | Verification Basis | Notes / Gaps |
|---|---|---|---|
| Python reproducibility | **PASS** | `INDEPENDENTLY_VERIFIED` | `python scripts/run_checks.py` verified by Codex Round 3 & AGY. |
| Test discovery | **PASS** | `INDEPENDENTLY_VERIFIED` | `31` unittest methods / `120` assertions; `40/40` Golden sub-cases reconciled. |
| Input validation | **PARTIAL** | `SELF_VERIFIED` | Core inputs hardened; optional parameter gaps open in `F-03`. |
| Quality gates | **PARTIAL** | `INDEPENDENTLY_VERIFIED` (pass) / `SELF_VERIFIED` (gaps) | Passes on current repo; 4 blind spots (`E1–E4`) open in `F-04`. |
| Example scenario | **PASS** | `INDEPENDENTLY_VERIFIED` | `compensation_engine.py` exits `0`. |
| Workbook build | **PASS** | `INDEPENDENTLY_VERIFIED` | `14` sheets / `915` formulas rebuilt cleanly to `%TEMP%`. |
| Workbook live recalculation | **PARTIAL / BLOCKED** | `SELF_VERIFIED` *(WPS COM `12.0`)* | Verified via WPS `et.exe` (`12.0`); genuine MS Excel `16.0` & Codex (`0x80080005`) still blocked. |
| Python/Excel parity | **PARTIAL** | `SELF_VERIFIED` *(WPS COM `12.0`)* | `12/12` + `20/20` + `2/2` perturbations PASS via WPS COM; AIA CQL `fm<0` divergence open (`F-03`). |
| Documentation | **PARTIAL** | `SELF_VERIFIED` | `F-01`, `F-02`, and `F-05` open. |
| Audit evidence retention | **PASS** | `SELF_VERIFIED` | `F-01..F-05` recovered & stored in protected local area outside PUBLIC repo. |
| Agent handover | **PASS** | `SELF_VERIFIED` | `HANDOVER.md` + this report provide complete Codex handover. |
| Portability (Linux/macOS) | **NOT VERIFIED** | `NOT VERIFIED` | Not tested on a second OS; COM script is Windows-only. |
| Confidentiality governance | **PASS / CONDITIONAL** | `SELF_VERIFIED` | `0` third-party skill/prompt leaks; 7 PDFs public per `DEC-08` Option C disclosure. |

> **Cập nhật 2026-11-26 (sau `f7da6a1`):** F-01..F-05 đã vá, 35→37 test PASS; trạng thái vá là `SELF_VERIFIED`. Workbook `v1.xlsx` là baseline đóng băng (không ghi đè): ô `09_Mgr_Senior_Comp!C8` trong `v1.xlsx` vẫn theo công thức cũ (0), bản dựng lại từ `scripts/build_workbook.py` mới có bản sửa (−54). Khi gửi Excel, dùng bản dựng lại.

**Overall Level 2 Verdict:** **`PARTIAL`** — full Level 2 closure awaits TJ approval to remediate `F-01..F-05` and resolve the WPS vs. MS Excel `16.0` COM disposition.
