# 00 — Kiểm kê nguồn & kiểm toán chức danh (Role Mapping Audit)

> Sinh bởi `scripts/build_role_audit.py`; mọi kiểm tra (hash, text từng trang, từ khóa) chạy lại mỗi lần sinh. Áp dụng 4 luật `AGENTS.md` (STRICT DATA INGESTION & MAPPING PROTOCOL) và rubric `qa/data-ingestion-rubric.md`.
> Trích dẫn dạng `[FileName : Trang]`, FileName là mã duy nhất có trong tên file (bảng 1).

## 1. Kiểm kê nguồn 9/9

| FileName (mã) | Source_ID | Hãng | Tên file gốc | Trang | Ký tự text | SHA-256 khớp registry | Cách đọc | Nhãn |
|---|---|---|---|---:|---:|---|---|---|
| `AIAVAD 2604-069` | SRC-POL-AIA-ALP-001 | AIA Vietnam | (Ref AIAVAD 2604-069) - Chính sách thu nhập năm 2026 dành cho CVTV_Alpha.pdf | 23 | 47.809 | ✅ | text từng trang (PyMuPDF) | VERIFIED FACT |
| `AIAVAD 2601-034` | SRC-POL-AIA-ALP-002 | AIA Vietnam | (Ref AIAVAD 2601-034)_Chính sách thu nhập năm 2026 dành cho CQL 2026_Alpha (cập nhật Huấn luyện).pdf | 21 | 43.418 | ✅ | text từng trang (PyMuPDF) | VERIFIED FACT |
| `AIAVAD 2601-035` | SRC-POL-AIA-ALP-003 | AIA Vietnam | (Ref AIAVAD 2601-035)_Chính sách thu nhập năm 2026 dành cho PAF+ 2026_Alpha_To SPVP (cập nhật Huấn luyện).pdf | 18 | 40.281 | ✅ | text từng trang (PyMuPDF) | VERIFIED FACT |
| `0046M01_2026` | SRC-POL-MNL-002 | Manulife Vietnam | 0046M01_2026_Chinh sach chi tra danh cho Dai Ly.pdf | 11 | 31.141 | ✅ | text từng trang (PyMuPDF) | VERIFIED FACT |
| `0047M01_2026` | SRC-POL-MNL-003 | Manulife Vietnam | 0047M01_2026_Bieu phi dich vu danh cho UM+.pdf | 8 | 21.573 | ✅ | text từng trang (PyMuPDF) | VERIFIED FACT |
| `0048M01_2026` | SRC-POL-MNL-001 | Manulife Vietnam | 0048M01_2026_Bieu phi dich vu danh cho PSM+ & HKD.pdf | 6 | 16.590 | ✅ | text từng trang (PyMuPDF) | VERIFIED FACT |
| `CHH0DCEB260007V` | SRC-POL-CHB-001 | Chubb Life Vietnam | CHH0DCEB260007V - Chính sách thu nhập dành cho Đại lý bảo hiểm - Kênh Đại lý.pdf | 19 | 38.589 | ✅ | text từng trang (PyMuPDF) | VERIFIED FACT |
| `CHH0DCEB260008V` | SRC-POL-CHB-002 | Chubb Life Vietnam | CHH0DCEB260008V - Chính sách về phí dịch vụ dành cho cấp Quản lý kinh doanh, Hỗ trợ kinh doanh - Kênh Đại lý.pdf | 14 | 29.636 | ✅ | text từng trang (PyMuPDF) | VERIFIED FACT |
| `CHH0DCEB260003V` | SRC-POL-CHB-003 | Chubb Life Vietnam | CHH0DCEB260003V-Chính sách về phí dịch vụ dành cho giám đốc vùng đièu hành.pdf | 15 | 0 | ✅ | bản scan — soát bằng mắt 15/15 trang | VERIFIED FACT |

Tổng: **9/9** file khớp hash; 135 trang (`0046M01_2026`, `0047M01_2026` bổ sung ngày 2026-11-27).

## 2. Cây chức danh nguyên văn theo từng hãng

Nguồn dữ liệu: `knowledge/policies/role-organization-mapping.csv` (cột `Raw_Title_Verbatim`, `Track_Type`, `Title_Citation`). Cột *Kiểm* = script tìm thấy mọi từ của tên nguyên văn trên đúng trang trích.

| Hãng | Mã | Tên nguyên văn | Tuyến (`track_type`) | Trích dẫn | Kiểm | Nhãn |
|---|---|---|---|---|---|---|
| AIA | `SA` | Chuyên viên Tư vấn (SA) | AGENT_INDIVIDUAL | [AIAVAD 2604-069 : 2] | ✅ | VERIFIED FACT |
| AIA | `Exchange` | Chuyên viên Hoạch định Tài chính | AGENT_FULLTIME_PROGRAM | [AIAVAD 2604-069 : 17] | ✅ | VERIFIED FACT |
| AIA | `Exchange Pro` | Chuyên viên Hoạch định Tài chính Cấp cao | AGENT_FULLTIME_PROGRAM | [AIAVAD 2604-069 : 17] | ✅ | VERIFIED FACT |
| AIA | `SE` | Chuyên viên Tư vấn Hỗ trợ phục vụ | AGENT_SERVICING_RESERVE | [AIAVAD 2604-069 : 17] | ✅ | VERIFIED FACT |
| AIA | `UM` | Trưởng Nhóm Kinh Doanh UM | MANAGER_DIRECT_LINE | [AIAVAD 2601-034 : 2] | ✅ | VERIFIED FACT |
| AIA | `SUM` | Trưởng Nhóm Kinh Doanh Cấp Cao SUM | MANAGER_DIRECT_LINE | [AIAVAD 2601-034 : 2] | ✅ | VERIFIED FACT |
| AIA | `DM` | Trưởng Phòng Kinh Doanh DM | MANAGER_DIRECT_LINE | [AIAVAD 2601-034 : 2] | ✅ | VERIFIED FACT |
| AIA | `SDM` | Trưởng Phòng Kinh Doanh Cấp cao SDM | MANAGER_DIRECT_LINE | [AIAVAD 2601-034 : 2] | ✅ | VERIFIED FACT |
| AIA | `PAF` | Quyền Sáng lập khối PAF | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `AF` | Nhà Sáng lập khối AF | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `PSAF` | Quyền Sáng lập khối cấp cao PSAF | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `SAF` | Nhà Sáng lập khối cấp cao SAF | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `DRF` | Quyền Sáng lập vùng DRF | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `RF` | Nhà Sáng lập vùng RF | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `DSRF` | Quyền Sáng lập vùng cấp cao DSRF | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `SRF` | Nhà Sáng lập vùng cấp cao SRF | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `PVP` | Quyền Phó chủ tịch PVP | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `SPVP` | Quyền Phó chủ tịch cấp cao SPVP | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `VP` | Phó Chủ tịch VP | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| AIA | `EVP / SVP / President` | Phó Chủ tịch Điều hành EVP Phó Chủ tịch Cấp Cao SVP Chủ Tịch President | LEADER_FOUNDER_TRACK | [AIAVAD 2601-035 : 3] | ✅ | VERIFIED FACT |
| Chubb | `AR` | Đại diện Kinh doanh (“ĐDKD” hay “AR”) | AGENT_INDIVIDUAL | [CHH0DCEB260007V : 3] | ✅ | VERIFIED FACT |
| Chubb | `AR Du bi` | AR dự bị | AGENT_SERVICING_RESERVE | [CHH0DCEB260007V : 8] | ✅ | VERIFIED FACT |
| Chubb | `AR-CH` | Champion Hubb | AGENT_FULLTIME_PROGRAM | [CHH0DCEB260007V : 9] | ✅ | VERIFIED FACT |
| Chubb | `AL-UM` | Trưởng Nhóm Kinh doanh (UM) | MANAGER_DIRECT_LINE | [CHH0DCEB260008V : 8] | ✅ | VERIFIED FACT |
| Chubb | `AL-SM` | Trưởng Ban Kinh doanh (SM) | MANAGER_DIRECT_LINE | [CHH0DCEB260008V : 8] | ✅ | VERIFIED FACT |
| Chubb | `AL-DM` | DM | MANAGER_DIRECT_LINE | [CHH0DCEB260008V : 3] | ✅ | VERIFIED FACT |
| Chubb | `AL-CH` | Champion Hubb vai trò Quản lý | MANAGER_DIRECT_LINE | [CHH0DCEB260008V : 11] | ✅ | VERIFIED FACT |
| Chubb | `AMD-BD` | Giám đốc, Phát triển Kinh doanh — Business Director, Agency Development (BD) | LEADER_AMD_SERVICE | [CHH0DCEB260003V : 3] (scan, visual) | 👁 scan | VERIFIED FACT |
| Chubb | `AMD-RD` | Giám đốc Vùng, Điều hành và Phát triển Kinh doanh — Regional Director, Agency Management and Development (RD) | LEADER_AMD_SERVICE | [CHH0DCEB260003V : 3] (scan, visual) | 👁 scan | VERIFIED FACT |
| Manulife | `PSM / SM` | PSM/SM | LEADER_SENIOR_SERVICE | [0048M01_2026 : 1] | ✅ | VERIFIED FACT |
| Manulife | `PSSM / SSM` | PSSM/SSM | LEADER_SENIOR_SERVICE | [0048M01_2026 : 1] | ✅ | VERIFIED FACT |
| Manulife | `HKD1 / HKD2` | HKD1/2 | LEADER_ENTITY_HKD | [0048M01_2026 : 1] | ✅ | VERIFIED FACT |
| Manulife | `HKD3 / HKD4` | HKD3/4 | LEADER_ENTITY_HKD | [0048M01_2026 : 1] | ✅ | VERIFIED FACT |
| Manulife | `SA (Servicing)` | “SA” là Đại lý phục vụ | AGENT_SERVICING_RESERVE | [0048M01_2026 : 6] | ✅ | VERIFIED FACT |
| Manulife | `Đại Lý` | Tất cả Đại Lý Bảo hiểm | AGENT_INDIVIDUAL | [0046M01_2026 : 1] | ✅ | VERIFIED FACT |
| Manulife | `UM+` | Quản Lý Đại lý (“UM+ ”) | MANAGER_DIRECT_LINE | [0047M01_2026 : 1] | ✅ | VERIFIED FACT |

### 2.1. Điều kiện thăng / giữ cấp (chép từ văn bản)

| Hãng | Chức danh | Loại | Nội dung | Trích dẫn | Kiểm | Nhãn |
|---|---|---|---|---|---|---|
| AIA | SA → UM | Thăng cấp | 3 tháng tại vị trí; ≥2 tuyển/giới thiệu trực tiếp 6T; ≥5 lượt CVTV hoạt động 3T; FYC tín chỉ toàn nhánh 6T ≥50tr; nhóm trực tiếp 6T ≥50tr; duy trì HĐ ≥70%; ≥2 HĐ thuần cá nhân | [AIAVAD 2601-034 : 8] | ✅ | VERIFIED FACT |
| AIA | UM → SUM | Thăng cấp | 6 tháng; ≥2 tuyển 6T; 0 UM+ trực tiếp; ≥9 lượt hoạt động 3T; toàn nhánh 6T ≥100tr | [AIAVAD 2601-034 : 8] | ✅ | VERIFIED FACT |
| AIA | SUM → DM | Thăng cấp | 6 tháng; ≥1 UM+ trực tiếp; ≥13 lượt; toàn nhánh 6T ≥200tr | [AIAVAD 2601-034 : 8] | ✅ | VERIFIED FACT |
| AIA | DM → SDM | Thăng cấp | 6 tháng; ≥2 UM+ trực tiếp; ≥17 lượt; toàn nhánh 6T ≥400tr | [AIAVAD 2601-034 : 8] | ✅ | VERIFIED FACT |
| AIA | Quy định 70% chỉ tiêu | Thăng/duy trì | Nhánh UM+ con đóng góp tối đa 70% yêu cầu (không áp cho SA → UM) | [AIAVAD 2601-034 : 9] | ✅ | VERIFIED FACT |
| AIA | SDM → PAF | Thăng cấp | 6 tháng; ≥3 UM+ trực tiếp; ≥18 lượt; FYP toàn nhánh 6T ≥1.200tr; duy trì ≥70% | [AIAVAD 2601-034 : 8] | ✅ | VERIFIED FACT |
| AIA | UM / SUM / DM / SDM | Duy trì | ≥6 tháng; ≥1 tuyển 6T; UM+ trực tiếp 0/0/1/1; lượt 4/6/9/12; FYC toàn nhánh 6T 30/45/75/105tr; duy trì ≥60%; không đạt → hạ 1 bậc | [AIAVAD 2601-034 : 10] | ✅ | VERIFIED FACT |
| AIA | PAF → AF … VP | Thăng cấp | AF: 6T, FYP 6T 2.500tr, 5 UM+, 1mAA 3T 35; … DSRF 12.000tr; SRF 15.000tr; VP 40.000tr; duy trì ≥70% | [AIAVAD 2601-035 : 6] | ✅ | VERIFIED FACT |
| AIA | PAF+ (Dual Career) | Phạm vi | PAF+ nhận thêm thu nhập vai trò CVTV/CQL; KHÔNG nhận phí gián tiếp cấp 2-3-4 của CQL | [AIAVAD 2601-035 : 2] | ✅ | VERIFIED FACT |
| AIA | SA / UM+ → SE | Duy trì | Không đạt duy trì HĐ → SE nếu phục vụ ≥3 HĐ, phí quy năm ≥20tr, TOT ≥50% | [AIAVAD 2604-069 : 10-11] | ✅ | VERIFIED FACT |
| Chubb | AR → UM | Thăng cấp | 3 tháng; FYC tích lũy 3T ≥25tr (gồm AR được giới thiệu, bản thân ≥10tr); 2 đại lý giới thiệu đạt 3MAA; K2/P13 ≥55%; khóa MAP | [CHH0DCEB260007V : 7] | ✅ | VERIFIED FACT |
| Chubb | UM → SM | Thăng cấp | 3 tháng; FYC 3T ≥50tr; 3MAA ≥5; 3MAA mới ≥1; AL trực tiếp ≥1 | [CHH0DCEB260007V : 7] | ✅ | VERIFIED FACT |
| Chubb | SM → DM | Thăng cấp | 6 tháng; FYC 6T ≥200tr; 3MAA ≥10; 3MAA mới ≥2; AL trực tiếp ≥2 | [CHH0DCEB260007V : 7] | ✅ | VERIFIED FACT |
| Chubb | DM → BD | Thăng cấp | 6 tháng; FYC 6T ≥450tr; 3MAA ≥20; 3MAA mới ≥3; AL trực tiếp ≥4; làm việc tại công ty ≥18 tháng | [CHH0DCEB260007V : 7] | ✅ | VERIFIED FACT |
| Chubb | AR / UM / SM / DM | Duy trì | 6 tháng; FYC 6T 10/20/100/200tr; 3MAA –/2/4/8; AL trực tiếp –/–/1/2; K2 ≥50%; AR rớt → AR dự bị (tối đa 18 tháng) | [CHH0DCEB260007V : 8] | ✅ | VERIFIED FACT |
| Chubb | AL Champion Hubb Quản lý | Phạm vi | AL chỉ tham gia 1 trong 2 vai trò (Cá nhân hoặc Quản lý) | [CHH0DCEB260008V : 11] | ✅ | VERIFIED FACT |
| Chubb | BD / RD (AMD) | Bổ nhiệm | Cấp bậc AMD ghi nhận tại Hợp đồng/Phụ lục hoặc quyết định của Công ty | [CHH0DCEB260003V : 3] | 👁 scan | VERIFIED FACT |
| Chubb | RD → cấp cao hơn | Thăng cấp | 12 tháng; FYP 6T ≥9.000tr; EHC tích lũy ≥300; K2 ≥60%; ≥2 DM trực tiếp; ≥4 BD được phát triển / RD giới thiệu | [CHH0DCEB260003V : 12] | 👁 scan | VERIFIED FACT |
| Chubb | RD | Duy trì | Nhánh trực tiếp: FYP 6T ≥750tr, EHC ≥25, K2 ≥50% HOẶC toàn nhánh: FYP ≥3.000tr, EHC ≥100, K2 ≥50% | [CHH0DCEB260003V : 13] | 👁 scan | VERIFIED FACT |
| Manulife | Đại Lý — hệ số thưởng | Hệ số | Mọi khoản thưởng × hệ số TLDTHD (trước 04/2026: ≥65% → 100%; từ 04/2026: ≥70% → 100%, <50% → TLDTHD/2) × hệ số CLKD (thư nhắc nhở 50%, cảnh cáo 0) | [0046M01_2026 : 1] | ✅ | VERIFIED FACT |
| Manulife | Đại Lý — thưởng năng suất tháng | Biểu thưởng | Theo FYC 3 tháng: 5/10/15/30/45/60/80/100tr → 5/10/15/20/25/30/35/50% FYC tháng; cần ≥1 HĐ thực cấp; >6 tháng dùng mức 2–8 | [0046M01_2026 : 4] | ✅ | VERIFIED FACT |
| Manulife | Đại Lý — thưởng năng suất quý | Biểu thưởng | FYC quý 15/30/45/60/80/100/120tr → 2/3/4/5/6/8/10% (Đại Lý xuất sắc ×2); mức 1 chỉ cho ≤6 tháng | [0046M01_2026 : 5] | ✅ | VERIFIED FACT |
| Manulife | Đại Lý — KDXS năm | Biểu thưởng | Chỉ Manulife Pro Vàng trở lên: 10–15% FYC năm (tối đa 100tr), TLDTHD ≥70%, trả 50/30/20% trong 3 năm | [0046M01_2026 : 6-7] | ✅ | VERIFIED FACT |
| Manulife | Đại Lý — M-Star | Biểu thưởng | FYP lũy kế ≥160 / 430 / 750 / 1.073,6tr cuối quý → 8 / 12 / 15 / 20tr; năm ≥1.073,6tr / 2 tỷ / 3 tỷ → 55 / 75 / 100tr trừ phần quý | [0046M01_2026 : 7-8] | ✅ | VERIFIED FACT |
| Manulife | Đại Lý — hoa hồng cơ bản | Phạm vi | Hoa hồng theo từng sản phẩm, theo Thông báo do Công Ty ban hành (không có bảng trong văn bản) | [0046M01_2026 : 9] | ✅ | VERIFIED FACT |
| Manulife | UM+ — phí năng suất nhóm | Biểu phí | Cấp 1: FYC ≥48 / 24 / 7 / <7tr → 20 / 16 / 14 / 10%; cấp 2–4 = ½ tỷ lệ cấp liền trên; không tính FYC bản thân UM+ | [0047M01_2026 : 1] | ✅ | VERIFIED FACT |
| Manulife | UM+ — phí hoạt động nhóm | Biểu phí | Số ĐL/UM+ cấp 1 có sản xuất ≥6 / 4–5 / 2–3 / 1 → MBA Pro 125 / 100 / 75 / 30%, UM+ khác 60 / 50 / 40 / 30% × thưởng năng suất tháng+quý của cấp 1 × hệ số TLDTHD | [0047M01_2026 : 2] | ✅ | VERIFIED FACT |
| Manulife | UM+ — điều kiện nhận phí | Điều kiện | Từ 02/2026: tham gia Đội ngũ chuyên cần ≥4 buổi/tháng | [0047M01_2026 : 3] | ✅ | VERIFIED FACT |
| Manulife | UM+ — phát triển nhóm mới | Biểu phí | 210% × phí năng suất nhóm cấp 1 của UM mới trong 12 tháng, tối đa 30tr/tháng; trả 50% ngay, 50% giữ lại | [0047M01_2026 : 4] | ✅ | VERIFIED FACT |
| Manulife | UM+ — hợp tác dài hạn | Biểu phí | Chỉ MBA Pro: Bạch Kim 125% / Vàng 100% / Bạc 80% × (A.II + A.III) năm; trả 30/30/40% trong 3 năm nếu TLDTHD ≥70% | [0047M01_2026 : 5-6] | ✅ | VERIFIED FACT |
| Manulife | PSM/SM · PSSM/SSM · HKD1/2 · HKD3/4 | Phí cơ bản | 35tr (PSM/SM, HKD1/2) · 45tr (PSSM/SSM, HKD3/4); không có điều kiện thăng/giữ cấp trong văn bản | [0048M01_2026 : 1] | ✅ | VERIFIED FACT |
| Manulife | PSM+ ↔ HKD | Chuyển đổi | Kết quả và quyền lợi được bảo lưu khi chuyển HĐDV QLCC ↔ HĐDV HKD | [0048M01_2026 : 5] | ✅ | VERIFIED FACT |
| Manulife | PSM+ / HKD | Thuế | PSM+: Công ty khấu trừ TNCN; HKD: tự xuất hóa đơn, tự chịu thuế | [0048M01_2026 : 5-6] | ✅ | VERIFIED FACT |

## 3. Mâu thuẫn tên gọi trong văn bản AIA (`CONFLICTING EVIDENCE`)

| Mã | Sơ đồ lộ trình `[AIAVAD 2601-034 : 2]`, `[AIAVAD 2604-069 : 2]` | Mục định nghĩa `[AIAVAD 2604-069 : 17]` | Kiểm | Nhãn |
|---|---|---|---|---|
| `UM` | Trưởng Nhóm Kinh Doanh | Trưởng Phòng Kinh Doanh (viết tắt là “UM”) | ✅ | CONFLICTING EVIDENCE |
| `SUM` | Trưởng Nhóm Kinh Doanh Cấp Cao | Trưởng Phòng Kinh Doanh Cấp Cao (viết tắt là “SUM”) | ✅ | CONFLICTING EVIDENCE |
| `DM` | Trưởng Phòng Kinh Doanh | Giám Đốc Ban Kinh Doanh (viết tắt là “DM”) | ✅ | CONFLICTING EVIDENCE |

Không tự phán xử: báo cáo dùng **mã** (UM/SUM/DM/SDM) làm khóa và giữ cả hai tên. Đề xuất ghi vào `docs/decisions/decision-register.md` nếu cần tên tiếng Việt chính thức.

## 4. Manulife: 3 văn bản, 2 tuyến song song

| Câu hỏi | Trả lời (`VERIFIED FACT`) | Căn cứ | Nhãn |
|---|---|---|---|
| `0046M01_2026` áp dụng cho ai? | Chính sách chi trả dành cho Đại Lý Manulife (Việt Nam), gửi **Tất cả Đại Lý Bảo hiểm**, hiệu lực 01/01/2026, thay 0001M04/2025. Gồm hệ số TLDTHD/CLKD (mục A) và 8 khoản thưởng B.I–B.VIII. **Không có bảng hoa hồng cơ bản** (mục C.1 dẫn chiếu thông báo theo từng sản phẩm) | [0046M01_2026 : 1], [0046M01_2026 : 2-8], [0046M01_2026 : 9] | VERIFIED FACT |
| `0047M01_2026` (UM+) áp dụng cho cấp nào? | Biểu phí dịch vụ dành cho Quản Lý Đại Lý (UM+), gửi **Tất cả Quản Lý Đại Lý (UM+)**, ký HĐDV QLĐL, hiệu lực 01/01/2026, thay 0002M04/2024. Văn bản chỉ gọi tên một bậc là Trưởng nhóm Kinh doanh (UM); các bậc khác trong UM+ theo 0013M04/2024 (không có trong nguồn). Biểu phí **không phân biệt bậc**, chỉ phân biệt có/không danh hiệu MBA Pro | [0047M01_2026 : 1], [0047M01_2026 : 4], [0047M01_2026 : 6] | VERIFIED FACT |
| Vì sao trước đây kết luận không có số UM/SUM/DM? | Đến 11:47–11:50 ngày 2026-11-27 hai file này **chưa có** trên máy (bộ nguồn khi đó 7 file; file nén gốc cũng 7 file). Nay đã nạp và tính | HANDOVER.md | VERIFIED FACT |
| `0048M01_2026` (PSM+/HKD) liên kết thế nào với UM+? | **Hai tuyến song song về hợp đồng**: UM+ ký HĐDV QLĐL (0047M01); PSM+ ký HĐDV QLCC, HKD ký HĐDV HKD (0048M01, cùng biểu phí). UM+ có thể chuyển sang PSM+/HKD và phí hợp tác dài hạn UM+ vẫn được trả tiếp sau khi chuyển. Điều kiện chuyển bậc nằm ở 0013M04/2024 (không có trong nguồn) | [0047M01_2026 : 6-7], [0048M01_2026 : 5] | VERIFIED FACT |

### 4.1. Chubb `BD` nằm ở đâu

| Văn bản · trang | Nội dung về BD | Kiểm | Nhãn |
|---|---|---|---|
| [CHH0DCEB260007V : 7] | Điều kiện thăng cấp DM → BD (FYC 6T ≥450tr, 3MAA ≥20, AL trực tiếp ≥4, ≥18 tháng tại công ty) | ✅ | VERIFIED FACT |
| [CHH0DCEB260007V : 4] | Thưởng HQKD cá nhân áp dụng cho AR, AL và AMD (BD là AMD) — thưởng bán cá nhân | ✅ | VERIFIED FACT |
| [CHH0DCEB260008V : 3] | Bảng tóm tắt phí AL chỉ có cột AR / UM / SM / DM — BD không hưởng phí AL | ✅ | VERIFIED FACT |
| [CHH0DCEB260003V : 3] | Cấp bậc AMD: Giám đốc, Phát triển Kinh doanh — Business Director, Agency Development (BD) | 👁 scan | VERIFIED FACT |
| [CHH0DCEB260003V : 10-11] | RD hưởng 25–50% tổng các khoản phí dịch vụ quản lý của BD được phát triển (6 khoản a–f) — chỉ có tên khoản, không có mức phí của BD | 👁 scan | VERIFIED FACT |

Kết luận: BD **có điều kiện thăng cấp** nhưng **biểu phí của chính BD không có** trong 9 file (nhật ký ở 4.3).

### 4.2. Danh sách file đã quét (tìm theo tên)

| Nơi quét | Mẫu tên | Kết quả |
|---|---|---|
| <repo>/private/sources | *0046M01*, *0047M01*, *UM+*.pdf, *Manulife*.pdf, *Bieu phi*.pdf | 0046M01_2026_Chinh sach chi tra danh cho Dai Ly.pdf; 0047M01_2026_Bieu phi dich vu danh cho UM+.pdf; 0048M01_2026_Bieu phi dich vu danh cho PSM+ & HKD.pdf |
| %USERPROFILE%/Downloads | *0046M01*, *0047M01*, *UM+*.pdf, *Manulife*.pdf, *Bieu phi*.pdf | 0046M01_2026_Chinh sach chi tra danh cho Dai Ly.pdf; 0047M01_2026_Bieu phi dich vu danh cho UM+.pdf; 0048M01_2026_Bieu phi dich vu danh cho PSM+ & HKD.pdf |
| %USERPROFILE%/Desktop | *0046M01*, *0047M01*, *UM+*.pdf, *Manulife*.pdf, *Bieu phi*.pdf | 0046M01_2026_Chinh sach chi tra danh cho Dai Ly.pdf; 0047M01_2026_Bieu phi dich vu danh cho UM+.pdf; 0048M01_2026_Bieu phi dich vu danh cho PSM+ & HKD.pdf |
| %USERPROFILE%/Documents | *0046M01*, *0047M01*, *UM+*.pdf, *Manulife*.pdf, *Bieu phi*.pdf | 0 kết quả |

### 4.3. Tìm từ khóa trên toàn bộ trang của 9 file (cho các kết luận còn thiếu)

**Biểu hoa hồng cơ bản theo sản phẩm của Manulife (0046M01 mục C.1 chỉ dẫn chiếu)** — nhãn `UNKNOWN` (không có trong nguồn):

| FileName | Trang có từ khóa | Ghi chú |
|---|---|---|
| `AIAVAD 2604-069` | `Hoa hồng`: [10, 12, 13, 18]; `tỷ lệ hoa hồng`: 0; `Phụ lục`: [2, 18, 21, 22] |  |
| `AIAVAD 2601-034` | `Hoa hồng`: [13, 15]; `tỷ lệ hoa hồng`: 0; `Phụ lục`: [2, 13, 15, 17] |  |
| `AIAVAD 2601-035` | `Hoa hồng`: [2]; `tỷ lệ hoa hồng`: 0; `Phụ lục`: [2, 3, 15] |  |
| `0046M01_2026` | `Hoa hồng`: [1, 9, 10]; `tỷ lệ hoa hồng`: 0; `Phụ lục`: [9] |  |
| `0047M01_2026` | `Hoa hồng`: [7]; `tỷ lệ hoa hồng`: 0; `Phụ lục`: [6] |  |
| `0048M01_2026` | `Hoa hồng`: [6]; `tỷ lệ hoa hồng`: 0; `Phụ lục`: [6] |  |
| `CHH0DCEB260007V` | `Hoa hồng`: [2, 3, 4, 13, 14, 15, 16, 17, 18, 19]; `tỷ lệ hoa hồng`: [2, 4, 13, 14, 15, 16, 17, 18, 19]; `Phụ lục`: [13] |  |
| `CHH0DCEB260008V` | `Hoa hồng`: 0; `tỷ lệ hoa hồng`: 0; `Phụ lục`: 0 |  |
| `CHH0DCEB260003V` | — | bản scan, không có lớp text → soát bằng mắt 15/15 trang |

**Hệ thống chức danh & điều kiện thăng / giữ cấp Manulife (0013M04/2024/ASBD)** — nhãn `UNKNOWN` (không có trong nguồn):

| FileName | Trang có từ khóa | Ghi chú |
|---|---|---|
| `AIAVAD 2604-069` | `0013M04`: 0; `thăng cấp`: [8, 9]; `điều kiện thăng`: [11]; `SUM`: [2, 17] |  |
| `AIAVAD 2601-034` | `0013M04`: 0; `thăng cấp`: 0; `điều kiện thăng`: [8, 16]; `SUM`: [2, 7, 8, 9, 10, 11, 12, 13, 18] |  |
| `AIAVAD 2601-035` | `0013M04`: 0; `thăng cấp`: [6, 7, 13]; `điều kiện thăng`: 0; `SUM`: [8, 16] |  |
| `0046M01_2026` | `0013M04`: 0; `thăng cấp`: 0; `điều kiện thăng`: 0; `SUM`: 0 |  |
| `0047M01_2026` | `0013M04`: [6]; `thăng cấp`: [4]; `điều kiện thăng`: [4]; `SUM`: 0 |  |
| `0048M01_2026` | `0013M04`: [5]; `thăng cấp`: 0; `điều kiện thăng`: 0; `SUM`: 0 |  |
| `CHH0DCEB260007V` | `0013M04`: 0; `thăng cấp`: [2, 7, 8, 11]; `điều kiện thăng`: [2, 7]; `SUM`: 0 |  |
| `CHH0DCEB260008V` | `0013M04`: 0; `thăng cấp`: [4, 6, 8, 9]; `điều kiện thăng`: 0; `SUM`: 0 |  |
| `CHH0DCEB260003V` | — | bản scan, không có lớp text → soát bằng mắt 15/15 trang |

**Tiêu chí danh hiệu MBA Pro (0050M01/2026) và Manulife Pro (0011M04/2024)** — nhãn `UNKNOWN` (không có trong nguồn):

| FileName | Trang có từ khóa | Ghi chú |
|---|---|---|
| `AIAVAD 2604-069` | `0050M01`: 0; `0011M04`: 0; `Tiêu chí`: [4, 13] |  |
| `AIAVAD 2601-034` | `0050M01`: 0; `0011M04`: 0; `Tiêu chí`: 0 |  |
| `AIAVAD 2601-035` | `0050M01`: 0; `0011M04`: 0; `Tiêu chí`: 0 |  |
| `0046M01_2026` | `0050M01`: 0; `0011M04`: 0; `Tiêu chí`: [5, 10] |  |
| `0047M01_2026` | `0050M01`: [2, 3]; `0011M04`: 0; `Tiêu chí`: [2, 3, 5] |  |
| `0048M01_2026` | `0050M01`: 0; `0011M04`: 0; `Tiêu chí`: 0 |  |
| `CHH0DCEB260007V` | `0050M01`: 0; `0011M04`: 0; `Tiêu chí`: 0 |  |
| `CHH0DCEB260008V` | `0050M01`: 0; `0011M04`: 0; `Tiêu chí`: 0 |  |
| `CHH0DCEB260003V` | — | bản scan, không có lớp text → soát bằng mắt 15/15 trang |

**Chính sách phí dịch vụ cho BD (Chubb)** — nhãn `UNKNOWN` (không có trong nguồn):

| FileName | Trang có từ khóa | Ghi chú |
|---|---|---|
| `AIAVAD 2604-069` | `BD`: 0 |  |
| `AIAVAD 2601-034` | `BD`: 0 |  |
| `AIAVAD 2601-035` | `BD`: 0 |  |
| `0046M01_2026` | `BD`: 0 |  |
| `0047M01_2026` | `BD`: 0 |  |
| `0048M01_2026` | `BD`: 0 |  |
| `CHH0DCEB260007V` | `BD`: [7] |  |
| `CHH0DCEB260008V` | `BD`: 0 |  |
| `CHH0DCEB260003V` | — | bản scan, không có lớp text → soát bằng mắt 15/15 trang |

Đọc nhật ký: từ khóa có xuất hiện nhưng chỉ là **dẫn chiếu** sang văn bản không có trong nguồn (0013M04, 0050M01, 0011M04, thông báo hoa hồng) hoặc thuộc **hãng khác** — không có bảng số tương ứng.

## 5. Bảng quy đổi theo 4 mốc quy mô — chức danh thực tế đạt được

Mốc định nghĩa trong `knowledge/policies/scale-milestones.json`. Giả định dùng để suy chức danh (`ASSUMPTION`): FYC/FYP 30%; K2 = FY = 85%; mọi đại lý hoạt động mỗi tháng; tuyển 2 người mới có hoạt động/quý; quản lý tự bán 2 HĐ/6 tháng; đủ thời gian tại vị trí (trạng thái ổn định).

| Mốc | AIA Alpha | Chubb Life | Manulife | Điều kiện quyết định (trích dẫn) | Nhãn |
|---|---|---|---|---|---|
| Mốc 1 — Cá nhân | **SA** | **AR** | **Đại Lý** [0046M01_2026 : 1] | Chặn ở bậc kế: Tuyển/giới thiệu trực tiếp 6 tháng (lên UM): cần 2, có 0 [AIAVAD 2601-034 : 8]; Đại lý được giới thiệu đạt 3MAA (lên UM): cần 2, có 0 [CHH0DCEB260007V : 7] | MODEL_OUTPUT |
| Mốc 2 — Nhóm 6 người | **SUM** | **UM** | **UM+** [0047M01_2026 : 1] — bậc cụ thể UNKNOWN (0013M04/2024 không có) | Chặn ở bậc kế: UM+ trực tiếp: cần 1, có 0 [AIAVAD 2601-034 : 8]; AL báo cáo trực tiếp (lên SM): cần 1, có 0 [CHH0DCEB260007V : 7] | MODEL_OUTPUT |
| Mốc 3 — Ban 15 người | **SDM** | **DM** | **UM+** [0047M01_2026 : 1] — bậc cụ thể UNKNOWN (0013M04/2024 không có) | Chặn ở bậc kế: UM+ trực tiếp (lên PAF): cần 3, có 2 [AIAVAD 2601-034 : 8]; Số 3MAA (lên BD): cần 20, có 15 [CHH0DCEB260007V : 7]; AL báo cáo trực tiếp (lên BD): cần 4, có 2 [CHH0DCEB260007V : 7] | MODEL_OUTPUT |
| Mốc 4 — Khu vực 45 người | **PAF** | **BD** | **UM+** [0047M01_2026 : 1] — bậc cụ thể UNKNOWN (0013M04/2024 không có) | Chặn ở bậc kế: Báo cáo trực tiếp UM+ (lên AF): cần 5, có 4 [AIAVAD 2601-035 : 6] | MODEL_OUTPUT |

Ghi chú: Chubb **BD** (Mốc 4) có điều kiện thăng cấp `[CHH0DCEB260007V : 7]` nhưng **biểu phí BD không có trong nguồn** (mục 4.3). Chubb **RD** và Manulife **PSM+/HKD** là bổ nhiệm theo hợp đồng dịch vụ, không có lộ trình định lượng từ tuyến đại lý trong 9 PDF. Manulife: Đại Lý → UM+ → PSM+/HKD là các tuyến hợp đồng; điều kiện chuyển bậc ở 0013M04/2024 (không có trong nguồn, nhật ký 4.3).

## 6. Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)

| # | Tiêu chí (`qa/data-ingestion-rubric.md`) | Điểm | Tối đa | Căn cứ đo được |
|---|---|---:|---:|---|
| 1 | Độ phủ nguồn 9/9 file | 25.0 | 25 | 9/9 file mở được và khớp SHA-256; bản scan soát 15/15 trang |
| 2 | Chức danh gốc & tuyến | 25.0 | 25 | 36/36 chức danh có tên nguyên văn khớp trang trích (hoặc đối chiếu bằng mắt với bản scan) và có `track_type` |
| 3 | Trích dẫn `[File : Trang]` cho từng con số | 20.0 | 20 | 41/41 dòng có số mang trích dẫn đúng mẫu |
| 4 | Negative Proof | 15.0 | 15 | 4/4 kết luận "không có trong tài liệu" kèm nhật ký tìm kiếm |
| 5 | Tách Fact / Assumption | 15.0 | 15 | 94/94 dòng có nhãn phân loại |
| | **Tổng** | **100.0** | **100** | **PASS** (ngưỡng 90) — máy đếm trên chính các bảng, đo độ phủ trích dẫn & nhãn, không phải điểm chất lượng phân tích |

