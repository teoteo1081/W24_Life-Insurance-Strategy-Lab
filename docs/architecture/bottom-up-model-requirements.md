# Bottom-Up Model Requirements — Đặc tả Mô hình Tương lai Xuất phát Từ Thực tế 7 Memo

**Ngày lập:** 2026-11-26  
**Nguyên tắc thiết kế (Nhiệm vụ 7):** Không ép các chính sách thực tế vào một bảng tham số Excel định sẵn. Toàn bộ danh sách thực thể, tham số, công thức, điều kiện và năng lực Rule Engine dưới đây được **rút ra trực tiếp từ 108 Atomic Business Rules** của 7 memo gốc (AIA Alpha, Manulife PSM+/HKD, Chubb Life).

---

## 1. 10 Business Entities Thực sự Tồn tại Trong Các Memo

Để mô hình hóa chính xác cả 3 công ty (và bất kỳ đối thủ/proposal mới nào nạp vào sau này), dữ liệu cần tổ chức quanh 10 thực thể lõi:

| # | Business Entity | Vai trò thực tế xuất hiện trong 7 memo | Thuộc tính cốt lõi bắt buộc |
|---|---|---|---|
| 1 | **`Insurer_Scheme`** | Tách rõ từng scheme theo Công ty → Kênh → Tầng → Phiên bản | `scheme_id`, `company`, `channel`, `tier`, `version`, `effective_date`, `expiry_date`, `legal_cap_profile` |
| 2 | **`Rank_Definition`** | Định nghĩa hệ thống chức danh không đồng nhất giữa các hãng | `rank_code`, `local_title`, `tier_level (1/2/3)`, `fixed_base_fee`, `tenure_gate_months`, `same_rank_limit_months`, `is_dual_career` |
| 3 | **`Agent_Profile`** | Hồ sơ từng đại lý/quản lý/lãnh đạo (bao gồm `HKD`, `SE`, `AR dự bị`, `Exchange/Pro`, `CH`) | `agent_id`, `join_date`, `standard_month_1`, `current_rank`, `rank_start_date`, `program_tag (SA/Exchange/ExchPro/CH/AFF)`, `entity_type (Individual/HKD)`, `maternity_flag`, `disciplinary_status` |
| 4 | **`Org_Hierarchy_Edge`** | Cây quan hệ trực tiếp, gián tiếp, người giới thiệu & thời gian đồng cấp | `parent_id`, `child_id`, `relation_type (Direct/Referral/Indirect)`, `reporting_depth`, `same_rank_months_elapsed`, `team_null_flag`, `snapshot_month` |
| 5 | **`Product_Commission`** | Biểu hoa hồng theo sản phẩm, năm HĐ, tuổi, giới tính & `HSBH` (từ Chubb Phụ đính II) | `product_code`, `line_type`, `age_band`, `gender`, `hsbh_tier`, `y1..y11_rates`, `topup_rate`, `fyc_credit_factor`, `is_excluded_from_active` |
| 6 | **`Policy_Transaction_Ledger`** | Sổ giao dịch phát hành, thu phí, giảm/tăng phí, hủy 21 ngày, hủy ≤6M, thay thế | `policy_id`, `agent_id`, `issue_date`, `ack_date`, `payment_mode`, `base_fyp`, `rider_fyp`, `single_premium`, `topup_premium`, `ryp_year`, `jfw_flag`, `status (Issued/FreeLookCancel/Cancel6M/Replacement)` |
| 7 | **`Activity_Compliance_Log`** | Dữ liệu phi doanh số ảnh hưởng trực tiếp tới tiền thưởng! | `attendance_pct`, `sop_pct`, `fna_count_valid`, `training_courses_done (SB/MAP/2601-023)`, `training_classes_hosted (>=4 trainees)`, `vitality_tier`, `acceptance_report_signed` |
| 8 | **`Target_Quota_Matrix`** | Ma trận chỉ tiêu theo chức danh × năm tuổi × tháng lịch (bắt buộc cho AIA PAF+ & Manulife PSM+) | `rank_code`, `tenure_year (1..5)`, `calendar_month (1..12)`, `fyp_target`, `active_1maa_target` |
| 9 | **`Persistency_Snapshot`** | Chỉ số chất lượng tính theo nhiều chuẩn khác nhau | `metric_type (AIA_FY / AIA_TOT / MNL_K2 / CHB_K2 / CHB_P13)`, `scope (Personal/DirectGroup/WholeBranch)`, `raw_pct`, `rounded_pct`, `is_na_new` |
| 10 | **`Payout_Vesting_Clawback_Ledger`** | Tách bạch: **Thu nhập được hưởng (Earned)** vs. **Chi trả ngay (Paid T / T+1)** vs. **Trả chậm nhiều năm (Deferred Tranches)** vs. **Thu hồi (Clawback)** | `payout_id`, `rule_id`, `earned_amount`, `payout_timing (T/T+1/M12/Y1-Y3)`, `vesting_gate_metric`, `withholding_reason`, `clawback_amount` |

---

## 2. Phân loại Tham số: Dùng Chung (Universal) vs. Đặc thù Từng Scheme (Scheme-Specific)

### A. Nhóm Tham số DÙNG CHUNG giữa các công ty (Lõi chung cho Excel / MAPA / Financial Model)
1. **Ràng buộc pháp lý VN (Hard Ceiling):** Trần FYC/RYC theo dòng sản phẩm & mốc 01/01/2027 (`TT 96/2026/TT-BTC`).
2. **Đầu vào sản xuất chuẩn hóa (MAPA Inputs):** `Manpower`, `Active Ratio`, `Productivity (Cases/Active)`, `Average Case Size (APE/FYP)`, Cơ cấu sản phẩm (% UL chính / % Riders / % Đóng 1 lần / % Top-up), Định kỳ đóng phí & Tỷ lệ thực thu năm 1.
3. **Đầu vào chất lượng chuẩn hóa:** Tỷ lệ hủy trong 21 ngày cân nhắc, Tỷ lệ hủy tháng 2–6 (`Clawback rate`), Tỷ lệ duy trì năm 2 (`Persistency K2 / FY 14M`), Tỷ lệ duy trì tái tục (`TOT / Y3–Y5`).
4. **Đầu vào vòng đời & tổ chức:** Tỷ lệ thăng cấp (`Promotion rate`), Tỷ lệ rời bỏ (`Attrition rate`), Cơ cấu tỷ lệ cấp bậc (Agent : Mid-Manager : Senior Leader).
5. **Đầu vào tài chính & marketing (P0/P1):** Biên lợi nhuận đóng góp giả định (`VNB Margin / Contribution %` cho phân tích độ nhạy & điểm hòa vốn), Ngân sách & chi phí phễu tuyển dụng / tìm kiếm khách hàng.

### B. Nhóm Tham số ĐẶC THÙ từng Scheme (Phải cấu hình theo bảng, KHÔNG hard-code!)
- **Định nghĩa cơ sở tính:** Trọng số Top-up trong FYP (`0%` AIA/Chubb mới vs. `6%` Manulife), Trọng số phí đóng 1 lần (`10%` AIA/Chubb RD vs. `6%` Manulife), Hệ số `FYC Tín Chỉ` (AIA), Định nghĩa Active (`4tr FYC` AIA/Manulife vs. `EHC` Chubb; có tính `SE/SA` hay không), Quy tắc làm tròn (`0 thập phân` AIA vs. `2 thập phân` Chubb RD).
- **Đặc thù AIA Alpha:** Mốc chuyển đổi Hệ số FY 2026 → 2027 (`<70% → 0%`), Bảng trọng số tuyển dụng `SA/Exchange/Exchange Pro` (`10/20/40%` & `×2` 1mAA), `Dual Career` PAF+ & 5 khoản loại trừ, Luật `70% Concentration Cap`, Lịch trả chậm CQL `15/25/60%` (2028–2030, `TOT ≥ 85%`), Ma trận chỉ tiêu 5 năm PAF+ (giảm T1–2, bù T11–12), Thu hồi 6 tháng & 12 tháng thâm niên.
- **Đặc thù Chubb Life:** Bảng hoa hồng theo `HSBH` (tuổi × giới tính × mức bảo vệ), Rolling 3-month FYC + chặn trần `<13M / <15M`, Hệ số K2 đáy mềm `25%` (AR/AL) vs. Binary Cliff `50% → 60%` (RD Q3+), Cổng dòng tiền `T vs. T+1` theo `K2 ≥ 60%`, Tính phí âm khi `FYC NTT < 0`, Khóa `0%` Indirect Override khi `FYC NTT < 15tr`, Champion Hubb (`4 trụ KPI`, `W1 SOP`, `W2 K2 M13–24`, cục giữ lại M12, `MAX()` offset), Thưởng tăng trưởng QoQ/YoY RD (`0–50%+ → 2.5–27.5%`), Nghiệm thu lớp đào tạo (`≥4 HV`) & 9 điều kiện tạm giữ.
- **Đặc thù Manulife `PSM+ / HKD`:** Công thức `130%` với sàn `30%` & trần `150%` phí cơ bản, 2 giai đoạn hệ số K2 (trước vs. từ `04/2026`, `<50% → K2/2`), 2 điều kiện Long-Term Fee (`≥85% FYP` vs. `Top 15` + tie-breaker), Tỷ trọng `75% Direct / 25% Indirect`, Trả chậm `30/30/40%` gắn `K2 ≥ 70%`, Chuyển đổi bảo lưu `PSM+ ↔ HKD`.

---

## 3. 14 Năng lực Bắt buộc của Rule Engine (Cho Excel Reference Model & HTML/JS Simulator Tương lai)

Từ thực tế 108 quy tắc, hệ thống tính toán (Excel ở G2 + Python Golden Tests + JS Simulator ở P1) phải hỗ trợ được 14 cơ chế toán học sau mà không cần viết code cứng theo tên công ty:

1. **Multi-Period Rolling & Annualization Lookup:** Tra bậc theo tổng 3 tháng trượt (Chubb HQKD) hoặc quy đổi kỳ thiếu (`× 3/số tháng` hoặc theo ngày — AIA CVTV & Chubb AL Quý).
2. **Date-Switched Regime Tables:** Tự động chuyển bảng hệ số theo ngày/quý tính toán (Manulife trước/sau `04/2026`; Chubb RD Q1–Q2 vs. Q3/2026; AIA FY 2026 vs. 2027).
3. **Soft-Floor vs. Hard-Cliff Quality Multipliers:** Hỗ trợ đồng thời nhân mềm (`%FY`, `25%` floor, `K2/2`) và vách đá cứng (`<70% → 0%`, `<60% → 0%`).
4. **Compound Multiplier-on-Bonus:** Cho phép khoản thưởng Quý tính bằng `% × Tổng thưởng Tháng` (Chubb AR/AL) hoặc nhiều lớp thưởng cộng dồn trên cùng FYC (AIA).
5. **Competitive `MAX()` Offset:** Cho phép trả `MAX(Program_A, Program_B + Program_C)` chống hưởng trùng (Chubb Champion Hubb Cá nhân & Quản lý).
6. **Negative-Base Symmetric Clawback:** Cho phép doanh số nhóm âm (`FYC NTT < 0`) tra tỷ lệ theo `ABS(FYC)` và sinh ra khoản **phí âm trừ ngược** (Chubb AL).
7. **Self-Performance Gated Indirect Override:** Khóa toàn bộ override tầng gián tiếp `L1–L3` về `0%` nếu nhóm trực tiếp của chính quản lý không đạt sàn (Chubb AL `<15tr`).
8. **Depth-Limited vs. Infinite Geometric Decay Chains:** Hỗ trợ cả chuỗi gián tiếp cắt ở 3–4 tầng (AIA CQL, Chubb AL) lẫn chuỗi 50% vô hạn tầng (AIA PAF+), kèm bộ đếm `Same-Rank / Over-Rank` tách nhánh.
9. **Single-Branch Concentration Cap (`70% Cap`):** Tự động chặn đóng góp của bất kỳ nhánh con nào tối đa ở `70%` chỉ tiêu thăng/duy trì (AIA CQL & PAF+).
10. **Multi-Year Deferred Vesting & Re-Gating:** Tách rõ *Earned Year 0* và các đợt chi trả *Y1/Y2/Y3* (`15/25/60%` AIA; `30/30/40%` Manulife; `M12` Chubb CH), kiểm tra lại cổng Persistency & trạng thái hợp đồng tại mỗi đợt giải ngân!
11. **Dual-Track Cashflow Timing (`T` vs. `T+1`) & 6–12M Lookback Clawback:** Mô phỏng dòng tiền thực chi theo tháng có tính trễ T+1 cho nhóm rủi ro cao và hoàn nhập clawback 6M/12M.
12. **Non-Sales Gate Modifiers:** Tích hợp hệ số chuyên cần/chấm công (`50%`, `70%`, `SOP W1`), số lớp đào tạo (`≥4 HV`), hoàn thành khóa học (`50%` penalty nếu thiếu ở Chubb, tạm giữ 100% ở AIA PAF+) và kỷ luật (`70% / 0%`).
13. **Protection-Ratio (`HSBH`) Product Commission Lookup:** Hỗ trợ tra % hoa hồng theo ma trận `(Sản phẩm × Năm HĐ × Tuổi × Giới tính × HSBH)` và khóa `Top-up = 0%`.
14. **PO Parameter Sandbox vs. Locked Competitor Ground Truth:** Cờ `po_editable` khóa cứng toàn bộ tham số đối thủ đã kiểm chứng, chỉ mở khóa tham số của **3 phương án Proposal** để PO/TJ thử kịch bản mà không bao giờ làm hỏng Ground Truth.
