"""Sinh outputs/interview/01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md từ engine.

Mọi con số trong file .md đều do script này gọi `model/compensation/compensation_engine.py`.
Không gõ tay số liệu. Chạy lại:  python scripts/build_interview_income_table.py

Đơn vị: triệu VNĐ. Thu nhập "/tháng" = thu nhập được hưởng cả năm (Earned, gồm phần trả chậm) / 12.
Đây là MODEL_OUTPUT trên kịch bản chuẩn (ASSUMPTION), không phải thu nhập thực tế đã quan sát.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from model.compensation.compensation_engine import (  # noqa: E402
    calc_aia_cql_12m,
    calc_aia_paf_12m,
    calc_chubb_al_12m,
    calc_chubb_al_htktn_month,
    calc_chubb_rd_12m,
    calc_manulife_psm_12m,
)
from scripts.agent_income_multiyear import K3_RATIO, RENEWAL_COMM_Y2, RENEWAL_COMM_Y3  # noqa: E402

OUT = REPO / "outputs" / "interview" / "01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md"

# ---------------- Giả định chuẩn (ASSUMPTION) ----------------
K2 = 85.0
FYC_RATE = 0.30          # FYC / FYP — giả định chung của repo (thiếu biểu hoa hồng AIA & cơ cấu sản phẩm)
TEAM = 5                 # đại lý / nhóm
TIERS = {
    # cấp: (số đại lý, FYP cả tổ chức / tháng)
    1: (5, 150.0),
    2: (15, 450.0),
    3: (45, 1200.0),
}
AIA_RECRUITS = [1, 2, 2, 2]   # CVTV mới có hoạt động / quý ở nhóm trực tiếp (ngưỡng 3–5 sao: Q1 ≥1, từ Q2 ≥2)

PDF = {
    "AIA_CQL": "AIAV/AD/2601-034 — CS thu nhập 2026 cho CQL Alpha",
    "AIA_PAF": "AIAV/AD/2601-035 — CS thu nhập 2026 cho PAF+ Alpha",
    "CHB_AL": "CHH0DCEB260008V — Phí dịch vụ cấp Quản lý KD (AL)",
    "CHB_RD": "CHH0DCEB260003V — Phí dịch vụ Giám đốc vùng (RD), bản scan",
    "MNL": "0048M01/2026/ASBD — Biểu phí dịch vụ PSM+ & HKD",
}


def finite(x: float, label: str) -> float:
    if not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"{label}: non-finite value {x!r}")
    return float(x)


def vn(x: float, d: int = 1) -> str:
    """Định dạng số kiểu Việt Nam: 1.234,5"""
    s = f"{x:,.{d}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def annual_ryc(fyp_month: float, k2: float = K2) -> float:
    """RYC ổn định/năm của tổ chức có FYP đều: hợp đồng năm 2 + năm 3 (bỏ qua năm 4–5 => thận trọng)."""
    fyp_y = fyp_month * 12.0
    k = k2 / 100.0
    return fyp_y * k * RENEWAL_COMM_Y2 + fyp_y * k * K3_RATIO * RENEWAL_COMM_Y3


# ---------------- Tính từng hãng ----------------
def team_fyc(n_agents: int, org_fyp: float) -> float:
    """FYC tháng của MỘT nhóm 5 người trong tổ chức (năng suất đều)."""
    return org_fyp / n_agents * TEAM * FYC_RATE


def aia_cql(tier: int, recruits=None, flat: bool = False):
    n, fyp = TIERS[tier]
    fyc_team = (fyp * FYC_RATE) if flat else team_fyc(n, fyp)
    active = n if flat else TEAM
    sub_a = 0.0
    gen2 = gen3 = 0.0
    if not flat and tier >= 2:
        sub = calc_aia_cql_12m([team_fyc(n, fyp)] * 12, [TEAM] * 12, fy_pct=K2, tot_pct=K2,
                               quarterly_new_recruits=AIA_RECRUITS)
        sub_a = sub["direct_monthly"]                    # phí A của 1 CQL con / năm
        if tier == 2:
            gen2 = 2 * sub_a                             # 2 UM con
        else:
            gen2 = 4 * sub_a                             # 2 BM + 2 UM con trực tiếp
            gen3 = 4 * sub_a                             # 4 UM dưới 2 BM
    r = calc_aia_cql_12m([fyc_team] * 12, [active] * 12, fy_pct=K2, tot_pct=K2,
                         quarterly_new_recruits=recruits if recruits is not None else AIA_RECRUITS,
                         indirect_gen2_base_12m=gen2, indirect_gen3_base_12m=gen3)
    return {
        "direct": r["direct_monthly"] + r["activity_monthly"],
        "direct_split": (r["direct_monthly"], r["activity_monthly"]),
        "fixed": None,
        "indirect": r["indirect_fee"],
        "quarterly": r["premier_quarterly"],
        "annual_deferred": r["annual_deferred_3y"],
        "ryc": None,
        "raw": r, "fyc_team": fyc_team, "sub_a": sub_a, "gen2": gen2, "gen3": gen3,
    }


def chubb_al(tier: int, flat: bool = False):
    n, fyp = TIERS[tier]
    fyc_ntt = (fyp * FYC_RATE) if flat else team_fyc(n, fyp)
    ehc = n if flat else TEAM
    l1 = l2 = 0.0
    sub_ht = 0.0
    rank = {1: "UM", 2: "SM", 3: "DM"}[tier]
    if not flat and tier >= 2:
        sub_ht = calc_chubb_al_htktn_month(team_fyc(n, fyp), TEAM, K2, 15)
        if tier == 2:
            l1 = 2 * sub_ht
        else:
            l1 = 4 * sub_ht
            l2 = 4 * sub_ht
    # RYC nhóm trực tiếp (chỉ khách của nhóm trực tiếp, không gồm nhóm con)
    direct_fyp_month = fyc_ntt / FYC_RATE
    ryc_q = annual_ryc(direct_fyp_month) / 4.0
    r = calc_chubb_al_12m([fyc_ntt] * 12, [ehc] * 12, k2_ntt=K2, al_tenure_start=15,
                          sub_l1_htktn_monthly=[l1] * 12, sub_l2_htktn_monthly=[l2] * 12, rank=rank,
                          quarterly_ryc_ntt_y2_y5=[ryc_q] * 4, quarterly_3maa_ntt=[ehc] * 4)
    return {
        "direct": r["ht_ktn_monthly"],
        "fixed": None,
        "indirect": r["indirect_l1_l3"],
        "quarterly": r["ht_ktn_quarterly"],
        "annual_deferred": 0.0,
        "ryc": r["persistency_ryc_quarterly"],
        "raw": r, "fyc_ntt": fyc_ntt, "sub_ht": sub_ht, "l1": l1, "l2": l2, "rank": rank, "ryc_q": ryc_q,
    }


# Tầng lãnh đạo vùng (Cấp 3B): cùng tổ chức 45 đại lý, 1,2 tỷ FYP/tháng
PAF_RANK, PAF_YEAR = "DSRF", 1        # chỉ tiêu năm 1 = 12.000tr FYP, gần nhất mà không vượt 14.400tr
MNL_BASE, MNL_ACH, MNL_AA_ACH = 35.0, 1.00, 1.00   # PSM/SM; % đạt chỉ tiêu là ASSUMPTION (bảng chỉ tiêu không có)


def leader_tier():
    n, fyp = TIERS[3]
    fyc = fyp * FYC_RATE
    paf = calc_aia_paf_12m(PAF_RANK, PAF_YEAR, [fyp] * 12, [fyc] * 12, [float(n)] * 12, fy_pct=K2, attendance_pct=80.0)
    ryc_m = annual_ryc(fyp) / 12.0
    rd = calc_chubb_rd_12m([fyp] * 12, [fyc] * 12, [n] * 12, [n] * 12, [ryc_m] * 12, k2_pct=K2,
                           weighted_reported_fyp_monthly=fyp, training_classes_monthly=4,
                           prior_year_q_fyp=[fyp * 3] * 4)
    mnl = calc_manulife_psm_12m(MNL_BASE, [MNL_ACH] * 12, [fyc] * 12, [MNL_AA_ACH] * 4, K2)
    return {"paf": paf, "rd": rd, "mnl": mnl, "fyc": fyc, "ryc_m": ryc_m}


# ---------------- Viết Markdown ----------------
def m(x):  # năm -> tháng
    return finite(x, "value") / 12.0


def cell(x):
    if x is None:
        return "— *(không có khoản này)*"
    return vn(m(x))


def build() -> str:
    L = []
    w = L.append
    a = {t: aia_cql(t) for t in TIERS}
    c = {t: chubb_al(t) for t in TIERS}
    ld = leader_tier()

    def total(d):
        return sum(v for k, v in d.items() if k in ("direct", "indirect", "quarterly", "annual_deferred", "ryc") and v)

    def cash(d):
        return total(d) - (d["annual_deferred"] or 0.0)

    w("# 01 — Bảng soi tiền 3 cấp quản lý & Evidence")
    w("")
    w("> **Trạng thái:** `MODEL_OUTPUT` trên kịch bản chuẩn (`ASSUMPTION`) — chờ TJ duyệt (Giai đoạn 1).")
    w("> Không phải thu nhập thực tế đã quan sát, không phải ROI thực tế.")
    w("> Sinh tự động bởi `scripts/build_interview_income_table.py` từ `model/compensation/compensation_engine.py`; không gõ tay số.")
    w("> Đơn vị: **triệu VNĐ / tháng** = thu nhập được hưởng cả năm (Earned, gồm phần trả chậm) ÷ 12, **trước thuế TNCN**.")
    w("")
    # ---- Tóm tắt
    w("## 1. Kết luận nhanh")
    w("")
    w("| Cấp (kịch bản) | AIA Alpha | Chubb Life | Manulife | Chi phí quản lý / FYP tổ chức (AIA · Chubb) |")
    w("|---|---:|---:|---:|---|")
    names = {1: "Cấp 1 — Trưởng nhóm (UM): 5 ĐL, 150tr FYP/th", 2: "Cấp 2 — Trưởng ban (BM): 15 ĐL, 450tr FYP/th",
             3: "Cấp 3 — Trưởng khu vực (DM): 45 ĐL, 1,2 tỷ FYP/th"}
    for t in TIERS:
        fyp = TIERS[t][1]
        w(f"| {names[t]} | **{vn(m(total(a[t])))}** | **{vn(m(total(c[t])))}** | ❓ chưa có tài liệu | "
          f"{vn(m(total(a[t])) / fyp * 100)}% · {vn(m(total(c[t])) / fyp * 100)}% |")
    paf, rd, mnl = ld["paf"], ld["rd"], ld["mnl"]
    rd_tot = rd["total_earned"]
    w(f"| Cấp 3B — cùng khu vực, nếu xếp vào tuyến **lãnh đạo vùng** (AIA PAF+ {PAF_RANK} · Chubb RD · Manulife PSM) | "
      f"**{vn(m(paf['total_earned']))}** | **{vn(m(rd_tot))}** | **{vn(m(mnl['total_earned']))}** | "
      f"{vn(m(paf['total_earned']) / 1200 * 100)}% · {vn(m(rd_tot) / 1200 * 100)}% · MNL {vn(m(mnl['total_earned']) / 1200 * 100)}% |")
    w("")
    w("**Đọc nhanh (`MODEL_OUTPUT`):**")
    w(f"- Ở tuyến quản lý trung gian (UM/BM/DM), **Chubb trả gấp khoảng {vn(total(c[1]) / total(a[1]), 1)}–{vn(total(c[3]) / total(a[3]), 1)} lần AIA** "
      "với cùng đội ngũ và doanh số. Lý do: Chubb tính phí trực tiếp 60% FYC nhóm × hệ số K2 120% và cộng thêm 50% phí tháng mỗi quý; AIA trả 8–24% FYC nhóm.")
    w("- **AIA đặt 2 cửa khóa:** thưởng quý (3–5 sao) đòi tuyển mới **≥2 CVTV có hoạt động mỗi quý** (Q1 ≥1); thưởng năm trả chậm 15/25/60% vào 2028–2030 và đòi FY nhóm ≥75%, TOT ≥85%.")
    w("- **Manulife:** 7 PDF chỉ có biểu phí **PSM+/HKD** (tuyến lãnh đạo vùng). Biểu phí UM/SUM/DM của Manulife **không có trong tài liệu** (`SRC-GAP-002`) nên cấp 1–3 là `UNKNOWN`, không điền 0.")
    w("- **HKD không rẻ hơn cho công ty theo văn bản:** PSM+ và HKD dùng **cùng một biểu phí** (0048M01 mục A). Khác biệt chỉ ở hợp đồng và thuế (mục C.9–C.10): PSM+ được công ty khấu trừ TNCN; HKD tự xuất hóa đơn và tự nộp thuế. Lợi ích thuế của HKD là `UNKNOWN` cho đến khi Pháp chế/Thuế đối chiếu.")
    w("")

    # ---- Giả định
    w("## 2. Giả định chuẩn dùng cho mọi hãng (`ASSUMPTION`)")
    w("")
    w("| # | Giả định | Giá trị | Vì sao / ảnh hưởng |")
    w("|---|---|---|---|")
    w(f"| A1 | FYC / FYP | {int(FYC_RATE*100)}% | Giả định chung của repo. Thiếu biểu hoa hồng AIA và memo FYC tín chỉ (`SRC-GAP-001`); cơ cấu sản phẩm thật chưa có. AIA tính trên **FYC tín chỉ**, ở đây coi = FYC. |")
    w(f"| A2 | Tỷ lệ duy trì | K2 = {int(K2)}% cho cả 3 hãng | AIA dùng **FY** (14 tháng) và **TOT**; Manulife dùng **TLDTHD**; Chubb dùng **K2 NTT**. Coi cả ba = {int(K2)}%. Công thức gốc của từng hãng nằm ở văn bản chưa có (260005V, 0016M03/2024). |")
    w("| A3 | Quản lý không tự bán | 0 doanh số cá nhân | So sánh thuần thu nhập quản lý. Lưu ý: FYC nhóm trực tiếp của AIA **có** gồm bán cá nhân của CQL, của Chubb thì **không**. |")
    w("| A4 | Đại lý hoạt động | Cả đội hoạt động mọi tháng; mỗi đại lý ≥1 HĐ và ≥4tr FYC | FYC mỗi đại lý: 9tr (cấp 1–2), 8tr (cấp 3). Chubb: coi mọi đại lý đạt **EHC** và **3MAA**; định nghĩa EHC nằm ở 260005V (chưa có). |")
    w("| A5 | Cấu trúc tổ chức | Cấp 1: 1 nhóm 5 người. Cấp 2: nhóm trực tiếp 5 + 2 UM con × 5. Cấp 3: nhóm trực tiếp 5 + 2 BM con (mỗi BM như cấp 2) + 2 UM con = 45 | Thu nhập phụ thuộc mạnh vào cấu trúc; xem độ nhạy ở mục 5. |")
    w(f"| A6 | Tuyển dụng (AIA) | CVTV mới có hoạt động/quý ở nhóm trực tiếp: {AIA_RECRUITS} | Cần để đạt danh hiệu 3–5 sao quý. Không cộng FYC và phí đồng hành của người mới (giữ quy mô 5 người). |")
    w("| A7 | Thâm niên | Quản lý ≥15 tháng, ổn định cả năm 2026 | Chubb AL ≥15 tháng được bảng phí cao hơn; phí RYC cần ≥13 tháng. |")
    w(f"| A8 | RYC (chỉ Chubb dùng) | RYC/năm = FYP năm × K2 × {int(RENEWAL_COMM_Y2*100)}% + FYP năm × K2 × {K3_RATIO} × {int(RENEWAL_COMM_Y3*100)}% | Giả định tái tục chung của repo (`scripts/agent_income_multiyear.py`); chỉ tính HĐ năm 2–3 nên thấp hơn thực tế. |")
    w(f"| A10 | Cấp 3B | AIA PAF+ bậc {PAF_RANK} năm 1 (chỉ tiêu 12.000tr FYP/năm); Manulife PSM/SM phí cơ bản {int(MNL_BASE)}tr, đạt {int(MNL_ACH*100)}% chỉ tiêu FYP và 1mAA; Chubb RD FYP đi ngang so với cùng kỳ | Chọn bậc PAF+ có chỉ tiêu gần nhất mà không vượt 14.400tr/năm. Bảng chỉ tiêu Manulife và quy định cấp bậc (0013M04/2024) không có. |")
    w("| A9 | Thời điểm | Cả năm 2026; hệ số K2 Manulife đổi từ 04/2026 | Manulife: tháng 1–3 hệ số 115%, từ tháng 4 hệ số 110% ở K2 85%. |")
    w("")

    # ---- Mapping
    w("## 3. Quy đổi chức danh ngang hàng")
    w("")
    w("| Cấp trong bài | AIA Alpha | Chubb Life | Manulife | Nguồn |")
    w("|---|---|---|---|---|")
    w("| Cấp 1 — Trưởng nhóm | UM (CQL) | AL — UM | UM — ❓ không có tài liệu | 2601-034 tr.2; 0008V tr.3 |")
    w("| Cấp 2 — Trưởng ban | SUM (CQL) | AL — SM | SUM — ❓ | như trên |")
    w("| Cấp 3 — Trưởng khu vực | DM (CQL) | AL — DM | DM — ❓ | như trên |")
    w(f"| Cấp 3B — Lãnh đạo vùng | PAF+ ({PAF_RANK}) | RD | PSM/SM hoặc HKD1/2 | 2601-035; 0003V; 0048M01 |")
    w("")
    w("Biểu phí CQL của AIA **không phân biệt UM/SUM/DM**: cấp bậc chỉ ảnh hưởng điều kiện thăng/giữ cấp và việc được hưởng gián tiếp. "
      "Chubb phân biệt theo cấp ở phí gián tiếp: UM chỉ có L1, SM có L1–L2, DM có L1–L3 (0008V tr.7).")
    w("")

    # ---- Tables per tier
    def tier_section(t: int):
        n, fyp = TIERS[t]
        A, C = a[t], c[t]
        ar, cr = A["raw"], C["raw"]
        w(f"## 4.{t}. {names[t]}")
        w("")
        w(f"FYC tổ chức = {vn(fyp * FYC_RATE)}tr/tháng. FYC nhóm trực tiếp của người quản lý = {vn(A['fyc_team'])}tr/tháng.")
        w("")
        w("| Khoản (tr/tháng) | AIA Alpha | Chubb Life | Manulife |")
        w("|---|---:|---:|---:|")
        w(f"| (1) Phí dịch vụ trực tiếp hàng tháng | {cell(A['direct'])} | {cell(C['direct'])} | ❓ |")
        w(f"| (2) Trợ cấp / phí cố định | {cell(A['fixed'])} | {cell(C['fixed'])} | ❓ |")
        w(f"| (3) Override gián tiếp (trên quản lý con) | {cell(A['indirect']) if t > 1 else '—'} | {cell(C['indirect']) if t > 1 else '—'} | ❓ |")
        w(f"| (4) Thưởng quý quy đổi tháng | {cell(A['quarterly'])} | {cell(C['quarterly'])} | ❓ |")
        w(f"| (5) Thưởng năm quy đổi tháng (**trả chậm**) | {cell(A['annual_deferred'])} | — *(không có khoản này)* | ❓ |")
        w(f"| (6) Phí duy trì HĐ theo RYC | — *(không có khoản này)* | {cell(C['ryc'])} | ❓ |")
        w(f"| **Tổng được hưởng / tháng** | **{vn(m(total(A)))}** | **{vn(m(total(C)))}** | ❓ |")
        w(f"| Trong đó tiền mặt năm 2026 | {vn(m(cash(A)))} | {vn(m(cash(C)))} | ❓ |")
        w(f"| % FYP tổ chức | {vn(m(total(A)) / fyp * 100)}% | {vn(m(total(C)) / fyp * 100)}% | ❓ |")
        w("")
        w("**Evidence từng con số:**")
        w("")
        w("| Hãng · khoản | tr/tháng | File PDF · mục · trang | Công thức với số của kịch bản |")
        w("|---|---:|---|---|")
        ft = A["fyc_team"]
        dr = 0.18 if ft >= 20 else 0.15
        dr = 0.24 if ft >= 50 else dr
        d_m, act_m = A["direct_split"]
        w(f"| AIA · (1a) tuyển dụng hiệu quả | {vn(m(d_m))} | {PDF['AIA_CQL']} · A.I · tr.3 | FYC nhóm {vn(ft)} × {int(dr*100)}% (bậc ≥{50 if ft >= 50 else 20}tr, FY ≥80%) |")
        w(f"| AIA · (1b) tuyển dụng chất lượng | {vn(m(act_m))} | {PDF['AIA_CQL']} · A.II · tr.3 | FYC nhóm {vn(ft)} × 8% (≥4 lượt CVTV hoạt động) × hệ số FY 100% (FY ≥70%) |")
        if t > 1:
            g = f"50% × phí A của {2 if t == 2 else 4} CQL con ({vn(m(A['sub_a']))}/tháng mỗi người)"
            if t == 3:
                g += f" + 25% × phí A của 4 UM cấp dưới nữa"
            w(f"| AIA · (3) gián tiếp | {vn(m(A['indirect']))} | {PDF['AIA_CQL']} · A.III · tr.4 | {g}; A = phí tuyển dụng hiệu quả tháng của CQL con |")
        q = ar["premier_quarterly"]
        star = "4 sao 8%" if ft * 3 < 170 else "5 sao 15%"
        w(f"| AIA · (4) quý | {vn(m(q))} | {PDF['AIA_CQL']} · A.V.1–2 · tr.4–5 | FYC quý {vn(ft*3)} × {star.split()[-1]} ({star.split()[0]} {star.split()[1]}: FYC quý, lượt hoạt động quý, CVTV mới ≥1 Q1 / ≥2 Q2+, FY ≥75%) |")
        ann = "5%" if star.startswith("4") else "10%"
        w(f"| AIA · (5) năm, trả chậm | {vn(m(A['annual_deferred']))} | {PDF['AIA_CQL']} · A.VI · tr.5 | FYC năm {vn(ft*12)} × {ann} ({'4' if ann == '5%' else '5'} sao toàn năm = ≥3 quý). Trả 15% (01/2028), 25% (01/2029), 60% (01/2030) nếu còn là CQL và TOT ≥85% |")
        cf = C["fyc_ntt"]
        w(f"| Chubb · (1) HT KTN tháng | {vn(m(C['direct']))} | {PDF['CHB_AL']} · II.2.1 · tr.5 | FYC NTT {vn(cf)} × {'60' if cf >= 40 else '50'}% (≥{'40' if cf >= 40 else '30'}tr, EHC ≥4, ≥15 tháng QL) × 120% (K2 NTT ≥80%) |")
        if t > 1:
            txt = f"L1 50% × HT KTN tháng của {2 if t == 2 else 4} AL con ({vn(C['sub_ht'])}/tháng mỗi người)"
            if t == 3:
                txt += " + L2 25% × HT KTN tháng của 4 UM báo cáo cấp 1"
            w(f"| Chubb · (3) quản lý nhóm | {vn(m(C['indirect']))} | {PDF['CHB_AL']} · II.3 · tr.7 | {txt}; tỷ lệ L theo FYC NTT của chính AL ({vn(cf)} ≥30tr) |")
        w(f"| Chubb · (4) HT KTN quý | {vn(m(C['quarterly']))} | {PDF['CHB_AL']} · II.2.2 · tr.6 | Tổng phí HT KTN tháng trong quý × {'50' if cf*3 >= 100 else '45'}% (FYC NTT quý {vn(cf*3)} ≥{'100' if cf*3 >= 100 else '75'}tr) |")
        w(f"| Chubb · (6) duy trì chất lượng HĐ | {vn(m(C['ryc']))} | {PDF['CHB_AL']} · II.5 · tr.9–10 | RYC NTT quý {vn(C['ryc_q'])} (A8) × 15% (3MAA NTT ≥5), K2 NTT ≥65%, ≥13 tháng |")
        w("| AIA · (2) / Chubb · (2) trợ cấp cố định | — | 2601-034 mục A–B; 0008V tr.3 bảng tóm tắt | Văn bản không có khoản trợ cấp cố định cho CQL/AL (`VERIFIED FACT`: đã đọc đủ mục lục) |")
        w("| Manulife · mọi khoản | ❓ | — | Biểu phí UM/SUM/DM của Manulife không có trong 7 PDF (`SRC-GAP-002`) → `UNKNOWN` |")
        w("")

    for t in TIERS:
        tier_section(t)

    # ---- Leader tier
    w("## 4.4. Cấp 3B — cùng khu vực 45 ĐL / 1,2 tỷ FYP/tháng, xếp vào tuyến lãnh đạo vùng")
    w("")
    w("Đây là **tầng duy nhất có tài liệu của cả 3 hãng**. Khác cấp 3 ở trên: người quản lý ký hợp đồng dịch vụ quản lý cấp cao, "
      "có phí cơ bản/cố định và hưởng trên toàn tổ chức.")
    w("")
    w("| Khoản (tr/tháng) | AIA PAF+ " + PAF_RANK + " | Chubb RD | Manulife PSM (35tr) |")
    w("|---|---:|---:|---:|")
    w(f"| (2) Phí cơ bản / cố định | {vn(m(paf['base_fee_12m']))} | {vn(m(rd['training_12m'] + rd['activity_12m'] + rd['business_12m']))} | {vn(m(mnl['base_fee_12m']))} |")
    w(f"| (1) Phí theo năng suất / chất lượng tháng | {vn(m(paf['prof_monthly_12m']))} | {vn(m(rd['quality_3maa_12m']))} | {vn(m(mnl['productivity_12m']))} |")
    w(f"| (4) Phí quý | {vn(m(paf['prof_quarterly_12m']))} | {vn(m(rd['growth_quarterly_12m']))} | {vn(m(mnl['activity_quarterly_12m']))} |")
    w(f"| (5) Năm / dài hạn | {vn(m(paf['seniority_fee_clawback12m']))} *(thưởng vượt chỉ tiêu)* | — | {vn(m(mnl['long_term_deferred_3y']))} *(trả chậm 30/30/40)* |")
    w(f"| (6) Theo RYC | — | {vn(m(rd['ryc_quarterly_12m']))} | — |")
    w(f"| **Tổng / tháng** | **{vn(m(paf['total_earned']))}** | **{vn(m(rd_tot))}** | **{vn(m(mnl['total_earned']))}** |")
    w(f"| % FYP | {vn(m(paf['total_earned']) / 1200 * 100)}% | {vn(m(rd_tot) / 1200 * 100)}% | {vn(m(mnl['total_earned']) / 1200 * 100)}% |")
    w("")
    w("**Evidence:**")
    w("")
    w("| Hãng · khoản | File · mục · trang | Công thức / giả định riêng |")
    w("|---|---|---|")
    w(f"| AIA PAF+ | {PDF['AIA_PAF']} · tr.4–6 (phí), tr.9–10 (chỉ tiêu) | Bậc {PAF_RANK} năm 1: phí cơ bản 80tr × 120% ở tháng đạt ≥115% chỉ tiêu FYP tháng, × 100% ở tháng đạt 55–115% (chỉ tiêu tháng có hệ số mùa vụ, bảng tr.9–10); phí chuyên môn tháng/quý theo % FYC × hệ số FY 120% (FY ≥75%); phí vượt chỉ tiêu = (FYP năm − 12.000) × 5%, tối đa bằng phí cơ bản năm. **Chưa cộng** phần Dual Career (PAF+ đồng thời nhận phí CQL, `AIA-PF-001` chưa mô hình). |")
    w(f"| Chubb RD | {PDF['CHB_RD']} · II.1–II.6 · tr.5–10 | Đào tạo 25tr (FYP theo cấp báo cáo ≥400tr, ≥4 lớp); hoạt động 8tr (EHC ≥20); kinh doanh 12tr (FYP ≥600tr); chất lượng 12% FYC (3MAA ≥12) × 100% (K2 ≥60%); tăng trưởng quý **2,5%** (tăng trưởng 0% — giả định FYP đi ngang); RYC × 30% (K2 ≥70%, RYC theo A8). **Chưa cộng** phí trên BD (II.7–II.8) vì thiếu chính sách BD. |")
    w(f"| Manulife PSM | {PDF['MNL']} · A.I–A.IV · tr.1–5 | Phí cơ bản 35tr × **{int(MNL_ACH*100)}% đạt chỉ tiêu FYP** × 130%; năng suất 6% FYC (<115%) × hệ số TLDTHD (115% tháng 1–3, 110% từ tháng 4); hoạt động quý 2,5% (đạt 100% chỉ tiêu 1mAA); dài hạn 75% × (năng suất + hoạt động), trần 12 × 35tr, trả 30/30/40% trong 3 năm. **Bảng chỉ tiêu FYP/1mAA không có** → % đạt là `ASSUMPTION`. |")
    w("")

    # ---- Sensitivity
    w("## 5. Độ nhạy — những giả định làm đổi kết luận")
    w("")
    a1_norec = aia_cql(1, recruits=[0, 0, 0, 0])
    a2_flat = aia_cql(2, flat=True)
    c2_flat = chubb_al(2, flat=True)
    w("| Thay đổi | AIA | Chubb | Ý nghĩa |")
    w("|---|---:|---:|---|")
    w(f"| Cấp 1, **không tuyển mới** trong năm | {vn(m(total(a1_norec)))} (từ {vn(m(total(a[1])))}) | {vn(m(total(c[1])))} (không đổi) | AIA khóa thưởng quý & năm vào tuyển dụng; Chubb không. |")
    w(f"| Cấp 2, cả 15 ĐL **trực tiếp** (không có UM con) | {vn(m(total(a2_flat)))} (từ {vn(m(total(a[2])))}) | {vn(m(total(c2_flat)))} (từ {vn(m(total(c[2])))}) | Cả hai hãng trả **nhiều hơn** khi quản lý giữ đội phẳng → động cơ không phát triển quản lý con. |")
    w("")

    # ---- Verification
    w("## 6. Đã kiểm chứng gì & đã sửa gì so với bản cũ")
    w("")
    w("Đối chiếu với **7 PDF gốc** (SHA-256 khớp `knowledge/sources/source-registry.csv`). Bản Chubb RD là bản scan nên được đọc bằng ảnh trang.")
    w("")
    w("| # | Phát hiện | Bằng chứng | Xử lý |")
    w("|---|---|---|---|")
    w("| F1 | Chubb AL — phí HT KTN quý: engine và workbook dùng ngưỡng **55tr**, PDF ghi **50tr** cho bậc 40% | 0008V tr.6 \"Từ 50 đến dưới 75 → 40%\"; catalog `CHB-MG-004` ghi đúng | Đã sửa engine + workbook; test `tests/test_pdf_table_fixes.py` |")
    w("| F2 | Chubb RD — phí quản lý hoạt động theo EHC: engine sai mức tiền và ngưỡng (6,0/4,5/3,0 tại 16/12/8) | 0003V tr.6: 8,0 / 6,5 / 5,0 / 3,5 / 2,5 / 1,5 tại 20/16/12/9/6/4; catalog `CHB-RD-003` ghi đúng | Đã sửa engine + workbook; test |")
    w("| F3 | Chubb RD — phí quản lý kinh doanh theo FYP: engine có bậc 240→4,5 không tồn tại, thiếu 270→5,0 và 180→3,5 | 0003V tr.6; catalog `CHB-RD-004` ghi đúng | Đã sửa engine + workbook; test |")
    w("| F4 | Chubb RD — phí tăng trưởng quý: engine 7 bậc; 0–5% trả 5% (PDF 2,5%), tăng trưởng âm trả 2,5% (PDF 0%) | 0003V tr.8: 12 bậc, bước 2,5% mỗi 5% tăng trưởng | Đã sửa engine (`rd_growth_rate`); golden GT-16a: Chubb 99,21% → **99,96%** FYP ở K2 82% |")
    w("| F5 | Chubb AL — **thiếu** phí duy trì chất lượng HĐ (10–15% RYC NTT) dù catalog ghi `IMPLEMENTED` | 0008V tr.9–10, `CHB-MG-008` | Đã thêm tham số tùy chọn (mặc định không phát sinh → kết quả cũ giữ nguyên) |")
    w("| F6 | AIA CQL — engine chỉ có gián tiếp cấp 2 (50%), **thiếu cấp 3 (25%) và cấp 4 (12,5%)** | 2601-034 tr.4 mục III | Đã thêm tham số tùy chọn |")
    w("| F7 | Bộ 7 PDF **không có** biểu phí Manulife cấp UM/SUM/DM | `SRC-GAP-002` | Giữ `UNKNOWN`, không điền 0 |")
    w("| F8 | \"HKD tối ưu thuế & chi phí\" chưa có căn cứ trong tài liệu | 0048M01: cùng biểu phí cho PSM+ và HKD; mục C.9–C.10 chỉ khác cách khấu trừ thuế | Ghi `HYPOTHESIS` — cần Pháp chế/Thuế |")
    w("")
    w("Đã kiểm khớp, không sửa: AIA CQL (A.I–A.VI, B), Chubb AL tháng / L1–L3 / hệ số K2, Chubb RD đào tạo và chất lượng 3MAA, Manulife A.I–A.IV.")
    w("")
    w("## 7. TJ cần quyết trước Giai đoạn 2")
    w("")
    w("1. **Cấu trúc A5** (cấp 2 = 5 trực tiếp + 2 UM con; cấp 3 = 5 + 2 BM + 2 UM) có đúng ý TJ không? Nếu TJ muốn \"phẳng\" thì số đổi mạnh (mục 5).")
    w("2. **Cấp 3 so ở tuyến nào:** quản lý trung gian (AIA DM · Chubb DM · Manulife ❓) hay lãnh đạo vùng (PAF+ · RD · PSM — đủ 3 hãng)?")
    w("3. **FYC/FYP = 30%** cho cả 3 hãng, hay TJ có cơ cấu sản phẩm thật để quy đổi?")
    w("")
    return "\n".join(L) + "\n"


def main() -> None:
    text = build()
    if "nan" in text.lower().split() or "inf" in text.lower().split():
        raise SystemExit("non-finite value leaked into output")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(text)} chars)")


if __name__ == "__main__":
    main()
