# HANDOVER.md — Điểm Bàn giao & Single Source of Truth (Trạng thái Hiện hành)

**Cập nhật lần cuối** 2026-11-27 (đêm) — Giai đoạn 2 (phân tích & Chính sách Lai) + Giai đoạn 3 (web 3 tab, 8 bảng Supabase)

## Trạng thái hiện hành

**2026-11-27 (khuya) — Bản build công khai an toàn (DEC-14) — CHƯA push, chờ TJ duyệt danh sách file.**
- Lệnh: `python scripts/build_html.py --public` sinh `outputs/public/W24_Strategy_Lab.html`; bản đầy đủ `outputs/interactive/W24_Strategy_Lab.html` giữ nguyên để gửi trực tiếp.
- Bản public lọc **79 dòng restricted** (không phải 54: GĐ2 thêm 24 dòng Manulife, từ điển thêm 1), bỏ mọi phần tử dữ liệu nhúng có nhắc 0046M01/0047M01 (role MNL-R06/R07, 2 PDF trong mục lục), bỏ `meta.confidential_files` và điểm Manulife. Từ điển lấy từ dòng public đã làm sạch.
- Lỗi có sẵn được phát hiện khi quét và đã sửa: `sync_to_supabase.py` nhận diện văn bản mật theo mã gốc (trước đây cần hậu tố `_2026`, nên ghi chú "biểu phí 0047M01" của thuật ngữ UM+ nằm ở dòng PUBLIC — nếu đã sync thật thì anon đọc được). Mọi trường chữ của dòng public giờ được làm sạch.
- `scripts/check_public_build.py`: quét dấu vết văn bản mật, secret (sb_secret_, JWT service_role, SUPABASE_SERVICE_KEY), đường dẫn cục bộ, `%PDF-`, email, dòng không public, file lạ trong thư mục phát hành → PASS. `tests/test_public_build.py` (5 test, gồm 5 kiểu rò rỉ gài vào đều bị bắt).
- **Rủi ro chính:** repo GitHub đang **PUBLIC** (không phải Private) và Pages phục vụ từ `main`. Local `main` có 11+ commit chứa số liệu mật → **tuyệt đối không push `main`**. Phát hành bằng nhánh `public-release`, tách từ `origin/main`, có 1 commit duy nhất thay file HTML công khai.

**2026-11-27 (khuya) — Đóng 1 P1 + 2 P2 của Codex trên `9dea455` — commit LOCAL, không push.**
- P1 (V3 đạt đúng quota 20,25tr từng vượt trần: 76,2%):
  - Trợ cấp Full-time nay = 3tr × hệ số vùng (V2 2,48tr · V3 2,03tr) — **thay đổi thiết kế, cần TJ xác nhận**.
  - Kiểm trần thêm "mọi ĐL đạt đúng quota vùng" cho V1/V2/V3 (69,4 / 70,3 / 71,4%) và lưới quét 195 điểm gãy (3 vùng × năng suất quanh quota, các bậc thưởng, nhất quán, MDRT × K2 80/85/95%): 0 điểm vượt.
  - Điểm cao nhất 73,1% (V3, 123,75tr FYP/ĐL) → khoảng dư chỉ 1,9 điểm %. Test quét dày FYP 5–600tr bước 2,5 (K2 80–95) xác nhận không vượt.
- P2 đơn vị đếm: một quy tắc cho cả 4 phương án (1 khoản = 1 mục chi trả có công thức riêng; các đời gián tiếp cùng công thức gộp 1 như [AIAVAD 2601-034 : 4]; phần giữ lại của cùng khoản không tính riêng). Lai = 5 khoản → điểm Lai **3,91** (AIA 3,15 · Chubb 3,05 · Manulife 3,37). Trụ cột Vận hành & Pháp lý vẫn là JUDGEMENT.
- P2 phân vùng: thêm vào `ProposalParams` 3 tham số `agent_q_consistency_min_fyc` (4) / `agent_mdrt_fyc_threshold` (400) / `agent_onboarding_min_fyc` (8). Mặc định giữ hành vi cũ, nên Song Hành và parity 240 ca không đổi. Chính sách Lai giãn cả 3 ngưỡng theo vùng (V3: 2,7 / 270 / 5,4).
- Test: `tests/test_hybrid_scheme.py` 18 test, đột biến 3/3 bị bắt.
- agy (audit `9dea455`, Desktop & offline PASS): sửa 3 điểm mobile — `scroll-margin-top:165px` + nút 📖 trừ chiều cao thanh dính khi cuộn; `code` tự xuống dòng (tab 2/3 hết tràn ngang); ô `#rq` rộng như ô tìm từ điển.

**2026-11-27 (khuya) — Sửa theo tự kiểm toán `41bec2d` (AGY tự kiểm, KHÔNG phải kiểm toán độc lập) — commit LOCAL, không push.**
- Trần 75% giờ kiểm ở kịch bản XẤU NHẤT: Mốc 4 chuẩn (26,7tr/ĐL) thấp hơn quota 30tr nên trợ cấp Full-time không bật. Kết quả Lai: chuẩn 59,9% · mọi ĐL đạt quota 69,4% · V2/V3 năng suất ngang V1 71,2% → vẫn ĐẠT, nhưng chỉ dư 3,8 điểm %.
- Rubric: đếm khoản phí Lai cùng quy tắc tuyến quản lý (7 khoản, trước đây tự đếm 5); An toàn tài chính chấm theo kịch bản xấu nhất → điểm Lai **3,80** (trước 4,01). AIA 3,15 · Chubb 3,05 · Manulife 3,37 không đổi. Ghi rõ thiên lệch: bậc đệm K2 và trần đội phẳng được thêm sau khi đo bằng rubric.
- Thêm bẫy hành vi cho Lai: vách đá K2 80→79% của đại lý Full-time (−23,6%), vách đá quota 30→29,9tr. 03 thêm rủi ro lách vùng kèm 3 lựa chọn kiểm soát (TJ chọn); đổi "Chống" thành "Giảm (chưa xóa)" bẫy đội phẳng.
- Snapshot và HTML dựng lại sau commit code, nên `model_version` trỏ đúng SHA, không còn `-dirty`.

**2026-11-27 (đêm) — Giai đoạn 2 + 3 trên baseline `90e7d10` (Codex PASS) — commit LOCAL, KHÔNG push (DEC-14); chờ agy kiểm trực quan, Codex kiểm toán.**
- Giai đoạn 2 — `scripts/build_phase2.py` (engine đã kiểm toán KHÔNG sửa) sinh:
  - `02_Phan_Tich_MAPA_TradeOff_Va_ROI.md` (rubric 99,1): khu vực Mốc 4 dùng chung (45 ĐL, 1,2 tỷ FYP/tháng). Tổng chi / FYP ở K2 85%: AIA 58,4% · Chubb 88,1% · Manulife 50,8% · Lai 59,9%. Chi trả giảm khi K2 sập 85→65%: 14,2 / 21,3 / 6,7 / 26,7%. Có 18 bẫy hành vi (tự bán vs quản lý, đội phẳng, vách đá K2 80→79, định phí, cổng tuyển mới; MBA Pro Vàng = HYPOTHESIS). Negative Proof quét 9/9 PDF cho 0050M01 và Chubb 260005V/006V/009V. "ROI" = chi phí/FYP, KHÔNG phải ROI thực tế.
  - Rubric 5 trụ cột (25/25/20/15/15; 3 trụ cột đầu tính bằng công thức công khai, "Vận hành & Pháp lý" là đánh giá): AIA 3,15 · Chubb 3,05 · Manulife 3,37 · Lai 4,01 (tự chấm, chưa kiểm toán độc lập).
  - `03_De_Xuat_Chinh_Sach_Lai_VN2026.md` (rubric 97,3, `PROPOSAL`): `model/compensation/hybrid_scheme.py`. Gồm 2 đường ray Full-time (trợ cấp 3tr khi đạt quota vùng, ≥2 HĐ, K2 ≥80%) / Part-time (thưởng 70%, thuần biến phí). Phần trả chậm nhận đủ khi K2 ≥80%, 50% khi 75–<80%, 0 khi dưới 75%; bậc đệm này được thêm sau khi bản đầu đo ra vách đá −37,5%. Override đội phẳng vượt 60tr FYC chỉ hưởng 50%. Trần 75% FYP: ĐẠT. Hệ số vùng V1 100% · V2 82,5% · V3 67,5%, giữ nguyên CC và K2. Khác biệt Bắc–Trung–Nam = HYPOTHESIS.
- Giai đoạn 3:
  - `web/template.html` được kế thừa, không viết lại. Thêm 3 tab đầu: (1) Soi tiền & Quyền lợi — bảng 4 mốc, bấm để bung ma trận 6 dòng có trích dẫn; (2) MAPA, Trade-off & ROI; (3) Chính sách Lai & Vùng — bộ chọn Vùng 1/2/3 và cơ sở năng suất. 9 trang cũ chuyển xuống nhóm "Tham khảo (bản trước)". Deep link `#t1/#t2/#t3`.
  - Đã sửa 3 lỗi UX agy báo: glossify lại sau khi lọc tab Bằng chứng; bỏ chữ "K2 " lặp trên thanh dính mobile; `.tag` nowrap, ô tìm rộng hơn, nút 📖 trên mobile cuộn tới `#p-glossary`.
  - Từ điển: 70 thuật ngữ (+6 thuộc nhóm "Đề xuất W24").
  - Supabase contract v2: thêm 4 bảng `roi_analysis` (48 dòng), `rubric_scores` (20), `behavior_traps` (18), `hybrid_regional` (30), RLS phủ đủ 8 bảng. Không có `.env` nên sync chạy `--dry-run` → snapshot.
  - Dòng restricted: 54 dòng của GĐ1 + 22 dòng Manulife của GĐ2. Phải lọc bỏ hết trước khi bất kỳ bản nào được Public.
- Kiểm: run_checks PASS; pytest 110 passed; `tests/test_hybrid_scheme.py` (14 test) — 8/8 đột biến bị bắt. Chrome headless đã render đủ 3 tab. Khổ 390px vẫn bị tràn ngang ở ảnh headless (hiện tượng đã ghi nhận từ trước).
- TJ cần quyết: (1) hệ số vùng và danh sách tỉnh từng vùng; (2) mức trợ cấp Full-time 3tr và quota; (3) có dùng điểm Lai 4,01 làm kết luận trước khi Codex kiểm toán độc lập hay không.

**2026-11-27 (tối) — Đóng 2 P2 của Codex trên `2543e02` (commit local, không push).**
- P2 #1: thêm `TestAiaStarRecruitBoundaries` — ranh giới người mới 3 sao (≥1 mọi quý) và 4–5 sao (≥1 Q1, ≥2 từ Q2) [AIAVAD 2601-034 : 4-5]. Thử đột biến: đổi 3 sao thành ≥2 → 3 test đỏ; bỏ yêu cầu 2 người từ Q2 → 2 test đỏ.
- P2 #2: `calc_manulife_agent_12m` không còn cộng M-Star năm vào `cash_paid_y1` (trả tháng 2 năm sau [0046M01_2026 : 8]); thêm `paid_next_years`. Test tái lập ca M-Star năm 20tr; đột biến bị bắt. Không đổi số nào đang trình bày (snapshot khác 0 dòng ngoài mốc thời gian).
- run_checks PASS; pytest 96 passed. Excel không bị ảnh hưởng (sheet 15 dùng thưởng, không dùng tiền thực trả) — chưa chạy lại COM.

**2026-11-27 (tối) — Kiến trúc tách lớp Supabase (khung, chưa nối project thật, chưa commit).**
- Data contract `supabase/schema.sql`: 4 bảng (`benchmark_results`, `role_benefit_matrix`, `glossary_terms`, `pdf_bookmarks`), RLS chỉ SELECT; dòng dựa trên 0046M01/0047M01 = `restricted`, chỉ user trong allowlist `w24_readers` đọc được (DEC-14). `region` hiện chỉ `ALL` — V1–V3 chưa có tham số (UNKNOWN).
- `scripts/sync_to_supabase.py`: dựng payload từ cùng hàm của báo cáo 00/01 (15 + 84 + 64 + 131 dòng, 54 restricted); `--dry-run` ghi `web/data/snapshot.json`; upsert qua REST (urllib, không thêm gói), `--prune` xóa dòng cũ; khóa đọc từ `.env` (gitignore).
- `web/data-loader.js`: đọc Supabase bằng anon key (meta), merge với snapshot nhúng; offline/không key → snapshot. `build_html.py` từ chối nhúng service key.
- Kiểm: Chrome headless — offline dùng snapshot; mock PostgREST → tooltip K2 cập nhật theo server. `tests/test_supabase_contract.py` (9 test). Hướng dẫn: `supabase/README.md`.

**2026-11-27 (tối) — Từ điển thuật ngữ & tooltip (chưa commit, chờ TJ xem).**
- Nguồn duy nhất `knowledge/sources/glossary.json` (64 thuật ngữ, 6 trường + nhóm/công ty/trích dẫn), sinh bởi `python scripts/build_glossary.py`; trang xuất hiện đầu tiên tự tìm trên text 9 PDF, test `tests/test_glossary.py` kiểm trang trích có chứa thuật ngữ.
- Sửa theo văn bản: PAF = "Quyền Sáng lập khối" (2601-035 tr.3), 3MAA = đại lý đạt EHC ≥1 lần trong 3 tháng (0003V tr.14); BM, VNB, MAPA, ROI không có trong 9 PDF. Tên tiếng Anh không có trong văn bản gắn nhãn "diễn giải".
- HTML: bỏ bảng GLOSSARY gõ tay; tooltip đọc từ `DATA.glossary`, bọc mọi lần xuất hiện (371 chỗ trên 8 trang), dạng "English — Tiếng Việt", hiện khi rê chuột / chạm / Tab; nút 📖 trên header + trang "Phụ lục: Từ điển & 9 PDF" (tìm, lọc công ty/nhóm, mục lục 9 PDF), link `#glossary`. Trích dẫn 0046M01/0047M01 không mở được (không lên kho bằng chứng, DEC-14).
- Kiểm: run_checks PASS; pytest 82 passed; Chrome headless dựng DOM đúng (64 dòng, tự kiểm 60/60).

**2026-11-27 (chiều) — Giai đoạn 1 khóa dữ liệu 9/9 PDF — TJ ĐÃ DUYỆT (DEC-14), commit LOCAL, KHÔNG push; chờ Codex kiểm toán độc lập trước Giai đoạn 2.**
- Nguồn: 9/9 PDF trong `private/sources/` (gitignore) khớp SHA-256 registry; thêm `SRC-POL-MNL-002` (0046M01 Đại Lý, 11 tr.) và `SRC-POL-MNL-003` (0047M01 UM+, 8 tr.), bổ sung lúc 11:47–11:50. `SRC-GAP-002` thu hẹp: còn thiếu biểu hoa hồng theo sản phẩm, 0013M04/2024 (chức danh), 0050M01/2026 (MBA Pro), 0011M04/2024 (Manulife Pro).
- Engine: `calc_manulife_agent_12m` (0046M01 B.III–B.VIII), `calc_manulife_um_12m` (0047M01 A.I–A.V), `manulife_agent_k2_factor`; test `tests/test_manulife_agent_um.py`. 3 P2 Codex đã sửa (MISSING_INPUT 3MAA, `K2_NO_K2_YET` ≠ UNKNOWN, câu 3 sao ≥1 / 4–5 sao ≥2).
- Báo cáo: `00_Role_Mapping_Audit.md` (100/100), `00_Role_And_Benefit_Matrix.md` (4 mốc × 3 hãng × 6 dòng, 100/100), `01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md` (98,9/100); mục lục 9 PDF `knowledge/sources/pdf-bookmarks.json` (131 mục, PDF không có bookmark gắn sẵn).
- Kết quả 4 mốc (tr/tháng; Mốc 2–4 = phí quản lý thuần, không gồm tự bán): AIA SA 18,1 / SUM 17,6 / SDM 25,7 / PAF 136,3 · Chubb AR 22,5 / UM 54,2 / DM 86,6 / **RD 186,6** (Mốc 4 chính; DM 134,6 phụ; BD ❓) · Manulife Đại Lý 17,8 / UM+ 11,0 / 18,2 / **PSM/SM 105,1** (Mốc 4 chính; UM+ 28,9 phụ).
- Excel: sheet mới `15_Manulife_Agent_UMplus`; Excel COM 12.0: 15 sheet, 940 công thức, 0 lỗi, 24/24 golden, 12/12 parity, `overall_pass=True`; `v1.xlsx` đã thay. `run_checks.py` PASS; `pytest` 78 passed (đã cài pytest theo yêu cầu TJ).
- Lưu ý quyền: 0046M01 (D.3) và 0047M01 (B.4) ghi "thông tin mật, không được tiết lộ". Bảng tỷ lệ trích từ 2 file này nằm trong output; cần TJ quyết trước khi push lên repo PUBLIC.
- Đã quyết (DEC-14): phạm vi 9 PDF; base case Manulife không MBA Pro (độ nhạy ở GĐ2); Mốc 4 chính PAF · RD · PSM/SM; chỉ commit local, không push. Bước tiếp: Codex kiểm toán commit Giai đoạn 1.

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
