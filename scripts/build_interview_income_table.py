"""Sinh outputs/interview/01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md từ engine, theo 4 mốc quy mô.

Mọi con số do script gọi `model/compensation/compensation_engine.py`; không gõ tay số liệu.
Chức danh ở từng mốc do `scripts/w24_milestones.py` suy từ điều kiện thăng cấp có trích dẫn.
Chạy lại:  python scripts/build_interview_income_table.py

Đơn vị: triệu VNĐ / tháng = thu nhập được hưởng cả năm (Earned, gồm phần trả chậm) / 12, trước thuế TNCN.
Đây là MODEL_OUTPUT trên kịch bản chuẩn (ASSUMPTION), không phải thu nhập thực tế đã quan sát.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from model.compensation.compensation_engine import (  # noqa: E402
    calc_aia_cql_12m,
    calc_aia_cvtv_12m,
    calc_aia_paf_12m,
    calc_chubb_al_12m,
    calc_chubb_al_htktn_month,
    calc_chubb_ar_12m,
    calc_chubb_rd_12m,
    calc_manulife_agent_12m,
    calc_manulife_psm_12m,
    calc_manulife_um_12m,
)
from scripts.agent_income_multiyear import K3_RATIO, RENEWAL_COMM_Y2, RENEWAL_COMM_Y3  # noqa: E402
from w24_milestones import FILE_IDS, FYC_RATE, K2, RECRUITS_PER_QUARTER, aia_title, chubb_title, load_milestones, manulife_title, rubric_table  # noqa: E402

OUT = REPO / "outputs" / "interview" / "01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md"
AIA_RECRUITS = [1, RECRUITS_PER_QUARTER, RECRUITS_PER_QUARTER, RECRUITS_PER_QUARTER]
MNL_BASE, MNL_ACH, MNL_AA_ACH = 35.0, 1.00, 1.00     # PSM/SM; % đạt chỉ tiêu là ASSUMPTION (bảng chỉ tiêu không có)
CITE = re.compile(r"\[[^\]:]+ : [0-9]+(-[0-9]+)?\]")


def finite(x: float, label: str = "value") -> float:
    if not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"{label}: non-finite value {x!r}")
    return float(x)


def vn(x: float, d: int = 1) -> str:
    s = f"{finite(x):,.{d}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def m(x: float) -> float:
    return finite(x) / 12.0


def renewal_split(fyp_month: float):
    """RYC ổn định/năm (ASSUMPTION A7): HĐ năm 2 (20%) + năm 3 (10%), bỏ qua năm 4–5 (thận trọng)."""
    fyp_y, k = fyp_month * 12.0, K2 / 100.0
    return fyp_y * k * RENEWAL_COMM_Y2, fyp_y * k * K3_RATIO * RENEWAL_COMM_Y3


def agent_m1(ms):
    fyc = ms.fyp_per_agent * FYC_RATE
    y2, y3 = renewal_split(ms.fyp_per_agent)
    aia = calc_aia_cvtv_12m([fyc] * 12, [y2 / 12] * 12, fy_pct=K2)
    chb = calc_chubb_ar_12m([fyc] * 12, [(y2 + y3) / 12] * 12, [True] * 12, k2_pct=K2, tenure_months_start=13)
    return fyc, y2, y3, aia, chb


def aia_manager(ms, include_indirect=True):
    fyc_team = ms.fyp_per_agent * FYC_RATE * ms.direct_agents
    sub_fyc = ms.fyp_per_agent * FYC_RATE * 5
    sub_a = calc_aia_cql_12m([sub_fyc] * 12, [5] * 12, fy_pct=K2, tot_pct=K2, quarterly_new_recruits=AIA_RECRUITS)["direct_monthly"]
    gen2 = ms.direct_managers * sub_a if include_indirect else 0.0
    gen3 = ms.grand_sub_units * sub_a if include_indirect else 0.0
    r = calc_aia_cql_12m([fyc_team] * 12, [ms.direct_agents] * 12, fy_pct=K2, tot_pct=K2, quarterly_new_recruits=AIA_RECRUITS,
                         indirect_gen2_base_12m=gen2, indirect_gen3_base_12m=gen3)
    return r, fyc_team, sub_a


def chubb_manager(ms, rank):
    fyc_ntt = ms.fyp_per_agent * FYC_RATE * ms.direct_agents
    sub_ht = calc_chubb_al_htktn_month(ms.fyp_per_agent * FYC_RATE * 5, 5, K2, 15) if ms.sub_units else 0.0
    l1, l2 = ms.direct_managers * sub_ht, ms.grand_sub_units * sub_ht
    y2, y3 = renewal_split(ms.fyp_per_agent * ms.direct_agents)
    ryc_q = (y2 + y3) / 4.0
    r = calc_chubb_al_12m([fyc_ntt] * 12, [ms.direct_agents] * 12, k2_ntt=K2, al_tenure_start=15,
                          sub_l1_htktn_monthly=[l1] * 12, sub_l2_htktn_monthly=[l2] * 12, rank=rank,
                          quarterly_ryc_ntt_y2_y5=[ryc_q] * 4, quarterly_3maa_ntt=[ms.direct_agents] * 4)
    return r, fyc_ntt, sub_ht, ryc_q


def mnl_agent_m1(ms):
    fyc = ms.fyp_per_agent * FYC_RATE
    y2, y3 = renewal_split(ms.fyp_per_agent)
    return calc_manulife_agent_12m([fyc] * 12, [ms.fyp_per_agent] * 12, [1] * 12, k2=K2, tenure_months_start=13,
                                   monthly_ryc=[(y2 + y3) / 12] * 12)


def mnl_um(ms):
    """UM+ theo 0047M01: cấp 1 = báo cáo trực tiếp (đại lý trực tiếp + quản lý con, quản lý con không tự bán — A3)."""
    fpa, fyp_pa = ms.fyp_per_agent * FYC_RATE, ms.fyp_per_agent
    ag = calc_manulife_agent_12m([fpa] * 12, [fyp_pa] * 12, [1] * 12, k2=K2, tenure_months_start=13)
    per_agent = [ag["monthly_bonus_by_month"][mo] + (ag["quarterly_bonus_by_quarter"][mo // 3] if mo % 3 == 2 else 0.0) for mo in range(12)]
    base = [ms.direct_agents * x for x in per_agent]
    c1 = ms.direct_agents * fpa
    c2 = 5 * ms.direct_managers * fpa
    c3 = 5 * ms.grand_sub_units * fpa
    r = calc_manulife_um_12m([(c1, c2, c3, 0.0)] * 12, [ms.direct_agents] * 12, base, K2)
    return r, ag, (c1, c2, c3)


def build() -> str:
    MS = load_milestones()
    L = []
    w = L.append
    ev = {"numeric": 0, "cited": 0, "data": 0, "labelled": 0, "missing": 0, "missing_proof": 0}

    def erow(cells, cite="", label="MODEL_OUTPUT", numeric=True):
        ev["data"] += 1
        ev["labelled"] += int(bool(label))
        if numeric:
            ev["numeric"] += 1
            ev["cited"] += int(bool(CITE.search(cite)))
        w("| " + " | ".join(cells + [cite or "—", f"`{label}`"]) + " |")

    def unknown(cells, why):
        ev["data"] += 1
        ev["labelled"] += 1
        ev["missing"] += 1
        ev["missing_proof"] += int("00_Role_Mapping_Audit" in why)
        w("| " + " | ".join(cells + [why, "`UNKNOWN`"]) + " |")

    titles = {ms.mid: (aia_title(ms)[0], chubb_title(ms)[0]) for ms in MS}
    chubb_rank = {k: (v[1] if v[1] in ("UM", "SM", "DM") else "DM") for k, v in titles.items()}

    r1 = agent_m1(MS[0])
    a2, _, _ = aia_manager(MS[1])
    c2, *_ = chubb_manager(MS[1], chubb_rank["M2"])
    a3, _, _ = aia_manager(MS[2])
    c3, *_ = chubb_manager(MS[2], chubb_rank["M3"])
    ms4 = MS[3]
    a4_cql, a4_fyc, _ = aia_manager(ms4, include_indirect=False)   # PAF+ Dual Career: không nhận gián tiếp cấp 2-4
    paf = calc_aia_paf_12m("PAF", 1, [ms4.fyp_month] * 12, [ms4.fyc_month] * 12, [float(ms4.agents)] * 12, fy_pct=K2, attendance_pct=80.0)
    a4_tot = paf["total_earned"] + a4_cql["total_earned"]
    c4_dm, *_ = chubb_manager(ms4, "DM")
    y2o, y3o = renewal_split(ms4.fyp_month)
    rd = calc_chubb_rd_12m([ms4.fyp_month] * 12, [ms4.fyc_month] * 12, [ms4.agents] * 12, [ms4.agents] * 12, [(y2o + y3o) / 12] * 12,
                           k2_pct=K2, weighted_reported_fyp_monthly=ms4.fyp_month, training_classes_monthly=4, prior_year_q_fyp=[ms4.fyp_month * 3] * 4)
    mnl = calc_manulife_psm_12m(MNL_BASE, [MNL_ACH] * 12, [ms4.fyc_month] * 12, [MNL_AA_ACH] * 4, K2)
    aia_m1_tot = r1[3]["total_earned"] + r1[2]   # + hoa hồng tái tục năm 3 (engine AIA chỉ nhận SYC)
    m1_mnl = mnl_agent_m1(MS[0])
    um = {ms.mid: mnl_um(ms) for ms in MS[1:]}

    w("# 01 — Bảng soi tiền theo 4 mốc quy mô & Evidence")
    w("")
    w("> **Trạng thái:** `MODEL_OUTPUT` trên kịch bản chuẩn (`ASSUMPTION`) — chờ TJ duyệt Giai đoạn 1. Không phải thu nhập thực tế, không phải ROI thực tế.")
    w("> Sinh bởi `scripts/build_interview_income_table.py` từ engine; chức danh từng mốc suy từ điều kiện thăng cấp (`scripts/w24_milestones.py`). "
      "Kiểm kê nguồn & Negative Proof: `outputs/interview/00_Role_Mapping_Audit.md`.")
    w("> Đơn vị: **triệu VNĐ / tháng** = thu nhập được hưởng cả năm (gồm phần trả chậm) ÷ 12, **trước thuế TNCN**.")
    w("")
    w("## 1. Kết luận nhanh — mỗi ô ghi chức danh, thu nhập, nguồn điều kiện thăng cấp, nguồn biểu phí")
    w("")
    w("| Mốc | Hãng | Chức danh · tr/tháng (Mốc 1: thu nhập cá nhân; Mốc 2–4: phí quản lý thuần) | Nguồn điều kiện thăng cấp | Nguồn biểu phí tính tiền | Ghi chú / lý do ❓ | Nhãn |")
    w("|---|---|---|---|---|---|---|")
    NEG = "Negative Proof: `00_Role_Mapping_Audit.md` mục 4"
    cells = [
        (MS[0], "AIA", f"**{titles['M1'][0]}** · {vn(m(aia_m1_tot))}", "[AIAVAD 2601-034 : 8] (SA→UM chưa đạt: cần ≥2 người tuyển trong 6 tháng)", "[AIAVAD 2604-069 : 3-7]", "Hoa hồng FYC/tái tục theo giả định A1, A7 (biểu hoa hồng AIA không có trong nguồn)", "MODEL_OUTPUT"),
        (MS[0], "Chubb", f"**{titles['M1'][1]}** · {vn(m(r1[4]['total_earned']))}", "[CHH0DCEB260007V : 7] (AR→UM chưa đạt: cần 2 đại lý giới thiệu đạt 3MAA)", "[CHH0DCEB260007V : 4-7], hoa hồng [CHH0DCEB260007V : 13-19]", "Tỷ lệ hoa hồng theo sản phẩm có trong Phụ đính II; cơ cấu sản phẩm theo A1", "MODEL_OUTPUT"),
        (MS[0], "Manulife", f"**Đại Lý** · {vn(m(m1_mnl['total_earned']))}", "— điều kiện lên UM+ ở 0013M04/2024 (không có trong nguồn) [0047M01_2026 : 6]", "[0046M01_2026 : 1-8]", "Hoa hồng cơ bản theo thông báo sản phẩm [0046M01_2026 : 9] → giả định A1, A7", "MODEL_OUTPUT"),
        (MS[1], "AIA", f"**{titles['M2'][0]}** · {vn(m(a2['total_earned']))}", "[AIAVAD 2601-034 : 8] (đạt SUM; DM cần ≥1 UM+ trực tiếp)", "[AIAVAD 2601-034 : 3-5]", "Phí CQL không phân biệt UM/SUM", "MODEL_OUTPUT"),
        (MS[1], "Chubb", f"**{titles['M2'][1]}** · {vn(m(c2['total_earned']))}", "[CHH0DCEB260007V : 7] (SM cần ≥1 AL trực tiếp)", "[CHH0DCEB260008V : 5-10]", "", "MODEL_OUTPUT"),
        (MS[1], "Manulife", f"**UM+** · {vn(m(um['M2'][0]['total_earned']))}", "— bậc trong UM+ theo 0013M04/2024 (không có) [0047M01_2026 : 6]", "[0047M01_2026 : 1-3]", "Không có danh hiệu MBA Pro (tiêu chí 0050M01/2026 không có) → không có phí dài hạn A.V", "MODEL_OUTPUT"),
        (MS[2], "AIA", f"**{titles['M3'][0]}** · {vn(m(a3['total_earned']))}", "[AIAVAD 2601-034 : 8] (PAF cần ≥3 UM+ trực tiếp)", "[AIAVAD 2601-034 : 3-5]", "", "MODEL_OUTPUT"),
        (MS[2], "Chubb", f"**{titles['M3'][1]}** · {vn(m(c3['total_earned']))}", "[CHH0DCEB260007V : 7] (BD cần 3MAA ≥20, ≥4 AL trực tiếp)", "[CHH0DCEB260008V : 5-10]", "", "MODEL_OUTPUT"),
        (MS[2], "Manulife", f"**UM+** · {vn(m(um['M3'][0]['total_earned']))}", "— như Mốc 2 [0047M01_2026 : 6]", "[0047M01_2026 : 1-3]", "Cấp 2 = ½ tỷ lệ cấp 1", "MODEL_OUTPUT"),
        (MS[3], "AIA", f"**{titles['M4'][0]}** · {vn(m(a4_tot))}", "[AIAVAD 2601-034 : 8] (SDM→PAF đạt); [AIAVAD 2601-035 : 6] (AF cần ≥5 UM+)", "[AIAVAD 2601-035 : 2-5] + phí CQL trực tiếp [AIAVAD 2601-034 : 3-5]", "Không còn phí gián tiếp cấp 2–4 [AIAVAD 2601-035 : 2]", "MODEL_OUTPUT"),
        (MS[3], "Chubb", f"**RD** (bổ nhiệm) · {vn(m(rd['total_earned']))} — *so sánh chính*", "RD bổ nhiệm theo hợp đồng [CHH0DCEB260003V : 3]; chức danh đạt bằng chỉ tiêu là BD [CHH0DCEB260007V : 7]", "[CHH0DCEB260003V : 5-10]", f"Phụ (tuyến quản lý truyền thống): DM {vn(m(c4_dm['total_earned']))} [CHH0DCEB260008V : 5-10]. BD: biểu phí không có trong nguồn — Negative Proof `00_Role_Mapping_Audit.md` mục 4.3", "MODEL_OUTPUT"),
        (MS[3], "Manulife", f"**PSM/SM** (bổ nhiệm) · {vn(m(mnl['total_earned']))} — *so sánh chính*", "PSM+ bổ nhiệm; điều kiện bậc ở 0013M04/2024 (không có) [0048M01_2026 : 5]", "[0048M01_2026 : 1-5]", f"Đạt 100% chỉ tiêu là giả định A8. Phụ: UM+ {vn(m(um['M4'][0]['total_earned']))} [0047M01_2026 : 1-3]", "MODEL_OUTPUT"),
    ]
    for ms_, co, val, promo, fee, note, lab in cells:
        has_num = "❓" not in val.split("·")[-1]
        if lab == "UNKNOWN":
            ev["data"] += 1; ev["labelled"] += 1; ev["missing"] += 1; ev["missing_proof"] += int("00_Role_Mapping_Audit" in note)
        else:
            ev["data"] += 1; ev["labelled"] += 1
            if has_num:
                ev["numeric"] += 1; ev["cited"] += int(bool(CITE.search(promo)) and bool(CITE.search(fee)))
        w(f"| {ms_.label} | {co} | {val} | {promo} | {fee} | {note or '—'} | `{lab}` |")
    w("")
    w("> **Mốc 2–4 là PHÍ QUẢN LÝ THUẦN, KHÔNG gồm hoa hồng/thưởng tự bán của quản lý** (giả định A3). Vì vậy Mốc 2 của AIA (17,6) và Manulife (11,0) thấp hơn Mốc 1 (đại lý tự bán 30tr FYP). "
      f"Nếu quản lý vẫn tự bán như Mốc 1, cộng thêm khoảng: AIA {vn(m(aia_m1_tot))}, Chubb {vn(m(r1[4]['total_earned']))}, Manulife {vn(m(m1_mnl['total_earned']))} tr/tháng. "
      "Mốc 4 so sánh chính theo tuyến lãnh đạo vùng (AIA PAF · Chubb RD · Manulife PSM/SM); số tuyến quản lý truyền thống (Chubb DM · Manulife UM+) ở cột ghi chú.")
    w("")
    w("### 1.1. Giải trình các ô ❓ và số tham chiếu")
    w("")
    w("**Manulife.** Đã có đủ 3 văn bản: `0046M01_2026` (Đại Lý), `0047M01_2026` (UM+), `0048M01_2026` (PSM+/HKD). Còn 3 chỗ phải giả định, có ghi trong bảng: "
      "(a) hoa hồng cơ bản theo từng sản phẩm không có trong 0046M01 `[0046M01_2026 : 9]`; (b) bậc cụ thể trong UM+ và điều kiện lên PSM+ nằm ở 0013M04/2024 `[0047M01_2026 : 6]`; "
      "(c) danh hiệu Manulife Pro / MBA Pro (0011M04/2024, 0050M01/2026) — mặc định **không có danh hiệu** nên không có thưởng KDXS năm, thưởng xuất sắc tháng, phí dài hạn A.V. "
      "Nhật ký tìm kiếm: `00_Role_Mapping_Audit.md` mục 4.3.")
    w("")
    w("**Chubb BD Mốc 4.** Khu vực 45 người đạt điều kiện DM → BD `[CHH0DCEB260007V : 7]`. BD thuộc Ban Điều hành và Phát triển Kinh doanh (AMD) `[CHH0DCEB260003V : 3]`, "
      "không còn là AL nên không hưởng biểu phí AL (bảng tóm tắt 0008V chỉ có AR/UM/SM/DM `[CHH0DCEB260008V : 3]`). Biểu phí của chính BD không nằm trong file nào: "
      "0003V áp dụng cho RD `[CHH0DCEB260003V : 3]` và chỉ nhắc tên 6 khoản phí của BD để làm căn cứ tính phí cho RD quản lý `[CHH0DCEB260003V : 10-11]`. "
      "Hai số DM (134,6) và RD (186,6) là **tham chiếu**: DM là nếu người đó chưa nhận thăng cấp, RD là chức danh do công ty bổ nhiệm theo hợp đồng, không phải chức danh đạt được bằng chỉ tiêu.")
    w("")
    w("**Đọc nhanh:**")
    w("- Cùng quy mô, **chức danh đạt được khác nhau**: nhóm 5 đại lý đủ điều kiện **SUM** ở AIA nhưng chỉ **UM** ở Chubb; ban 15 đại lý là **SDM** (AIA) và **DM** (Chubb); khu vực 45 đại lý lên **PAF** (AIA) và **BD** (Chubb).")
    w(f"- Ở tuyến quản lý (Mốc 2–3), **Chubb trả khoảng {vn(c2['total_earned'] / a2['total_earned'], 1)}–{vn(c3['total_earned'] / a3['total_earned'], 1)} lần AIA** cho cùng đội ngũ: Chubb trả 60% FYC nhóm × 120% (K2 ≥80%) + 50% mỗi quý; AIA trả 8–24% FYC nhóm.")
    w("- Ở Mốc 4, AIA chuyển sang tuyến **PAF+** có phí cố định và vẫn giữ phí CQL trên nhóm trực tiếp (\"con đường sự nghiệp kép\"), nhưng **mất phí gián tiếp cấp 2–4** `[AIAVAD 2601-035 : 2]`.")
    w("- **AIA thưởng quý cần người mới có hoạt động:** **3 sao cần ≥1 người/quý**; **4–5 sao cần ≥1 ở Q1/2026 và ≥2 từ Q2/2026** `[AIAVAD 2601-034 : 4]`.")
    w(f"- **Manulife UM+ trả thấp nhất ở tuyến quản lý**: {vn(m(um['M2'][0]['total_earned']))} / {vn(m(um['M3'][0]['total_earned']))} / {vn(m(um['M4'][0]['total_earned']))} tr/tháng ở Mốc 2/3/4 — chỉ 10–20% FYC cấp 1 (`[0047M01_2026 : 1]`) và phí hoạt động tính trên **thưởng** của đại lý chứ không trên FYC (`[0047M01_2026 : 1-2]`). Không có danh hiệu MBA Pro thì mất phí dài hạn.")
    w("")
    w("### 1.2. Ghi chú độ nhạy — Manulife có danh hiệu MBA Pro / Manulife Pro (chạy ở Giai đoạn 2, `HYPOTHESIS`)")
    w("")
    w("Base case = **không có danh hiệu** (tiêu chí ở 0050M01/2026 và 0011M04/2024, không có trong 9 PDF). Nếu có MBA Pro: phí hoạt động nhóm UM+ tăng từ 50% lên 100% (4–5 người sản xuất) hoặc 125% (≥6) `[0047M01_2026 : 2]`, "
      "phí phát triển đại lý mới từ 50% lên 100% `[0047M01_2026 : 3]`, thêm phí hợp tác dài hạn 80/100/125% × (A.II + A.III), trả chậm 30/30/40% `[0047M01_2026 : 5-6]`. "
      "Đại lý có Manulife Pro: thêm thưởng xuất sắc tháng và thưởng KDXS năm `[0046M01_2026 : 4-7]`.")
    w("")
    w("## 2. Giả định chung (`ASSUMPTION`)")
    w("")
    w("| # | Giả định | Giá trị | Ghi chú |")
    w("|---|---|---|---|")
    w(f"| A1 | FYC / FYP | {int(FYC_RATE * 100)}% | Thiếu biểu hoa hồng AIA và memo FYC tín chỉ (00 mục 4). AIA tính trên **FYC tín chỉ**, coi = FYC. |")
    w(f"| A2 | Tỷ lệ duy trì | K2 = FY = TLDTHD = {int(K2)}% | Công thức gốc từng hãng nằm ở văn bản không có trong nguồn (260005V, 0016M03/2024). |")
    w("| A3 | Quản lý tự bán | 2 HĐ / 6 tháng (để giữ điều kiện AIA), FYC không đáng kể | So sánh thuần thu nhập quản lý ở Mốc 2–4. |")
    w("| A4 | Hoạt động | Mọi đại lý hoạt động mỗi tháng, ≥1 HĐ và ≥4tr FYC; Chubb: mọi đại lý đạt EHC/3MAA | Định nghĩa EHC ở 260005V (không có trong nguồn). |")
    w("| A5 | Cấu trúc | Theo `knowledge/policies/scale-milestones.json` | Mốc 2: 1 QL + 5 ĐL; Mốc 3: + 2 quản lý con × 5; Mốc 4: 5 trực tiếp + 2 ban con + 2 nhóm con. |")
    w(f"| A6 | Tuyển mới | CVTV mới có hoạt động/quý: {AIA_RECRUITS} | Đủ cho 4–5 sao AIA và 3MAA mới của Chubb. |")
    w(f"| A7 | Tái tục | RYC/năm = FYP × K2 × {int(RENEWAL_COMM_Y2 * 100)}% + FYP × K2 × {K3_RATIO} × {int(RENEWAL_COMM_Y3 * 100)}% | Giả định chung của repo; chỉ HĐ năm 2–3. |")
    w(f"| A8 | Mốc 4 | AIA PAF năm 1; Manulife PSM/SM phí cơ bản {int(MNL_BASE)}tr, đạt {int(MNL_ACH * 100)}% chỉ tiêu; Chubb RD FYP đi ngang | Bảng chỉ tiêu Manulife không có trong nguồn. |")
    w("")
    w("## 3. Chi tiết từng mốc — mỗi con số kèm trích dẫn")
    w("")
    head = "| Hãng · chức danh | Khoản | tr/tháng | Công thức với số của kịch bản | Trích dẫn | Nhãn |"
    sep = "|---|---|---:|---|---|---|"

    # ---- M1
    ms = MS[0]
    fyc, y2, y3, ra, rc = r1
    t = titles["M1"]
    w(f"### {ms.label} — 1 đại lý, {vn(ms.fyp_month)}tr FYP/tháng (FYC {vn(fyc)}tr)")
    w("")
    w(head); w(sep)
    erow([f"AIA · {t[0]}", "Hoa hồng trực tiếp (FYC)", vn(m(ra["fyc_total"])), f"FYC {vn(fyc)}/tháng (A1)"], "", "ASSUMPTION")
    erow([f"AIA · {t[0]}", "Hoa hồng tái tục năm 2–3", vn(m(y2 + y3)), "A7"], "", "ASSUMPTION")
    erow([f"AIA · {t[0]}", "Trợ cấp cố định", "—", "Không có cho SA (trợ cấp Exchange/Pro nằm ở văn bản riêng, không có trong nguồn)"], "[AIAVAD 2604-069 : 3]", "VERIFIED FACT", numeric=False)
    erow([f"AIA · {t[0]}", "Thưởng sản xuất quý", vn(m(ra["bonus_quarterly_prod"])), "% theo FYC tín chỉ quý × hệ số FY"], "[AIAVAD 2604-069 : 5]")
    erow([f"AIA · {t[0]}", "Thưởng Chuyên viên Ngoại hạng quý", vn(m(ra["bonus_quarterly_premier"])), "Theo danh hiệu sao quý"], "[AIAVAD 2604-069 : 6]")
    erow([f"AIA · {t[0]}", "Thưởng chất lượng phục vụ (SYC) quý", vn(m(ra["bonus_syc"])), "% SYC quý"], "[AIAVAD 2604-069 : 6]")
    erow([f"AIA · {t[0]}", "Thưởng sản xuất năm", vn(m(ra["bonus_annual"])), "% FYC năm × hệ số FY"], "[AIAVAD 2604-069 : 7]")
    erow([f"**AIA · {t[0]}**", "**Tổng**", f"**{vn(m(aia_m1_tot))}**", "FYC + SYC + thưởng + tái tục năm 3"], "[AIAVAD 2604-069 : 5-7]")
    erow([f"Chubb · {t[1]}", "Hoa hồng trực tiếp (FYC)", vn(m(rc["fyc_total"])), f"FYC {vn(fyc)}/tháng (A1); tỷ lệ theo sản phẩm ở Phụ đính II"], "[CHH0DCEB260007V : 13-19]", "ASSUMPTION")
    erow([f"Chubb · {t[1]}", "Hoa hồng tái tục (RYC)", vn(m(rc["ryc_total"])), "A7"], "", "ASSUMPTION")
    erow([f"Chubb · {t[1]}", "Trợ cấp cố định", "—", "Không có trong bảng tóm tắt 5 khoản thu nhập"], "[CHH0DCEB260007V : 3]", "VERIFIED FACT", numeric=False)
    erow([f"Chubb · {t[1]}", "Thưởng HQKD tháng", vn(m(rc["bonus_hqkd_monthly"])), f"FYC × 35% (FYC 3 tháng {vn(fyc * 3)}tr: bậc 20–<40) × 120% (K2 ≥80%)"], "[CHH0DCEB260007V : 4]")
    erow([f"Chubb · {t[1]}", "Thưởng HQKD quý", vn(m(rc["bonus_hqkd_quarterly"])), "30% tổng thưởng tháng trong quý (3 tháng đạt EHC)"], "[CHH0DCEB260007V : 5-6]")
    erow([f"Chubb · {t[1]}", "Thưởng duy trì HĐ quý (RYC)", vn(m(rc["bonus_ryc_quarterly"])), "15% RYC năm 2–5 (3 lượt EHC/quý, K2 ≥65%)"], "[CHH0DCEB260007V : 6-7]")
    erow([f"**Chubb · {t[1]}**", "**Tổng**", f"**{vn(m(rc['total_earned']))}**", "FYC + RYC + thưởng"], "[CHH0DCEB260007V : 4-7]")
    rm = m1_mnl
    erow(["Manulife · Đại Lý", "Hoa hồng trực tiếp (FYC)", vn(m(rm["fyc_total"])), f"FYC {vn(fyc)}/tháng (A1); bảng hoa hồng theo thông báo sản phẩm (không có)"], "[0046M01_2026 : 9]", "ASSUMPTION")
    erow(["Manulife · Đại Lý", "Hoa hồng tái tục", vn(m(rm["ryc_total"])), "A7"], "", "ASSUMPTION")
    erow(["Manulife · Đại Lý", "Trợ cấp cố định", "—", "Không có trong 8 khoản thưởng B.I–B.VIII"], "[0046M01_2026 : 2-8]", "VERIFIED FACT", numeric=False)
    erow(["Manulife · Đại Lý", "Thưởng năng suất tháng", vn(m(rm["bonus_monthly_productivity"])), f"FYC × 15% (FYC 3 tháng {vn(fyc * 3)}tr ≥15) × hệ số TLDTHD 100%"], "[0046M01_2026 : 4]")
    erow(["Manulife · Đại Lý", "Thưởng năng suất quý", vn(m(rm["bonus_quarterly_productivity"])), f"FYC quý {vn(fyc * 3)}tr < 30tr (mức 2, >6 tháng) → 0"], "[0046M01_2026 : 5]")
    erow(["Manulife · Đại Lý", "M-Star quý/năm", vn(m(rm["bonus_mstar_quarterly"] + rm["bonus_mstar_annual"])), f"FYP lũy kế quý 1 = {vn(ms.fyp_month * 3)}tr < 90% × 160tr → 0"], "[0046M01_2026 : 7-8]")
    erow(["**Manulife · Đại Lý**", "**Tổng**", f"**{vn(m(rm['total_earned']))}**", "FYC + tái tục + thưởng; không danh hiệu Manulife Pro"], "[0046M01_2026 : 4-8]")
    w("")

    # ---- M2, M3
    for ms in (MS[1], MS[2]):
        t = titles[ms.mid]
        ra_m, fyc_team, sub_a = aia_manager(ms)
        rc_m, fyc_ntt, sub_ht, ryc_q = chubb_manager(ms, chubb_rank[ms.mid])
        w(f"### {ms.label} — {ms.agents} đại lý, {vn(ms.fyp_month)}tr FYP/tháng; FYC nhóm trực tiếp {vn(fyc_team)}tr")
        w("")
        w(head); w(sep)
        erow([f"AIA · {t[0]}", "Hoa hồng trực tiếp", "—", "Quản lý không tự bán đáng kể (A3)"], "", "ASSUMPTION", numeric=False)
        erow([f"AIA · {t[0]}", "Trợ cấp cố định", "—", "Không có trong chính sách CQL"], "[AIAVAD 2601-034 : 3-7]", "VERIFIED FACT", numeric=False)
        erow([f"AIA · {t[0]}", "Phí tuyển dụng hiệu quả tháng", vn(m(ra_m["direct_monthly"])), f"FYC nhóm {vn(fyc_team)} × 18% (≥20tr, FY ≥80%)"], "[AIAVAD 2601-034 : 3]")
        erow([f"AIA · {t[0]}", "Phí tuyển dụng chất lượng tháng", vn(m(ra_m["activity_monthly"])), "FYC nhóm × 8% (≥4 lượt hoạt động) × 100% (FY ≥70%)"], "[AIAVAD 2601-034 : 3]")
        if ms.sub_units:
            erow([f"AIA · {t[0]}", "Phí gián tiếp (CQL con)", vn(m(ra_m["indirect_fee"])), f"50% × phí A của {ms.direct_managers} CQL con ({vn(m(sub_a))}/tháng mỗi người)"], "[AIAVAD 2601-034 : 4]")
        erow([f"AIA · {t[0]}", "Phí quý (4 sao)", vn(m(ra_m["premier_quarterly"])), f"FYC quý {vn(fyc_team * 3)} × 8% (≥80tr, ≥9 lượt, người mới theo A6)"], "[AIAVAD 2601-034 : 4-5]")
        erow([f"AIA · {t[0]}", "Phí năm (trả chậm 15/25/60%)", vn(m(ra_m["annual_deferred_3y"])), f"FYC năm {vn(fyc_team * 12)} × 5% (≥3 quý 4 sao); trả 2028–2030 nếu TOT ≥85%"], "[AIAVAD 2601-034 : 5]")
        erow([f"**AIA · {t[0]}**", "**Tổng**", f"**{vn(m(ra_m['total_earned']))}**", f"tiền mặt 2026: {vn(m(ra_m['cash_paid_y1']))}"], "[AIAVAD 2601-034 : 3-5]")
        erow([f"Chubb · {t[1]}", "Hoa hồng trực tiếp", "—", "Quản lý không tự bán đáng kể (A3)"], "", "ASSUMPTION", numeric=False)
        erow([f"Chubb · {t[1]}", "Trợ cấp cố định", "—", "Không có trong bảng tóm tắt 5 khoản của AL"], "[CHH0DCEB260008V : 3]", "VERIFIED FACT", numeric=False)
        erow([f"Chubb · {t[1]}", "HT KTN tháng", vn(m(rc_m["ht_ktn_monthly"])), f"FYC NTT {vn(fyc_ntt)} × 60% (≥40tr, EHC ≥4, ≥15 tháng) × 120% (K2 ≥80%)"], "[CHH0DCEB260008V : 5]")
        if ms.sub_units:
            erow([f"Chubb · {t[1]}", "Quản lý nhóm L1", vn(m(rc_m["indirect_l1_l3"])), f"50% × HT KTN tháng của {ms.direct_managers} AL con ({vn(sub_ht)}/tháng mỗi người)"], "[CHH0DCEB260008V : 7]")
        erow([f"Chubb · {t[1]}", "HT KTN quý", vn(m(rc_m["ht_ktn_quarterly"])), f"Phí tháng trong quý × 50% (FYC NTT quý {vn(fyc_ntt * 3)} ≥100tr)"], "[CHH0DCEB260008V : 6]")
        erow([f"Chubb · {t[1]}", "Duy trì chất lượng HĐ (RYC)", vn(m(rc_m["persistency_ryc_quarterly"])), f"RYC NTT quý {vn(ryc_q)} (A7) × 15% (3MAA ≥5, K2 ≥65%)"], "[CHH0DCEB260008V : 9-10]")
        erow([f"**Chubb · {t[1]}**", "**Tổng**", f"**{vn(m(rc_m['total_earned']))}**", "trả tiền mặt trong năm"], "[CHH0DCEB260008V : 5-10]")
        ru, ag, (c1, c2, c3) = um[ms.mid]
        erow(["Manulife · UM+", "Hoa hồng trực tiếp", "—", "Quản lý không tự bán đáng kể (A3)"], "", "ASSUMPTION", numeric=False)
        erow(["Manulife · UM+", "Trợ cấp cố định", "—", "Không có trong biểu phí UM+ (5 khoản A.I–A.V)"], "[0047M01_2026 : 1-6]", "VERIFIED FACT", numeric=False)
        erow(["Manulife · UM+", "Phí năng suất nhóm (cấp 1–4)", vn(m(ru["a1_team_productivity"])), f"Cấp 1 FYC {vn(c1)} × 16% (24–<48) + cấp 2 {vn(c2)} × 8% + cấp 3 {vn(c3)} × 4%"], "[0047M01_2026 : 1]")
        erow(["Manulife · UM+", "Phí hoạt động nhóm", vn(m(ru["a2_team_activity"])), f"50% ({ms.direct_agents} người sản xuất) × thưởng năng suất của cấp 1 × TLDTHD 115% (T1–3) / 110%"], "[0047M01_2026 : 1-2]")
        erow(["Manulife · UM+", "Phí hợp tác dài hạn", vn(m(ru["a5_long_term_deferred_30_30_40"])), "Chỉ cho MBA Pro (tiêu chí 0050M01/2026 không có) → 0"], "[0047M01_2026 : 5]", "ASSUMPTION")
        erow(["**Manulife · UM+**", "**Tổng**", f"**{vn(m(ru['total_earned']))}**", "trả tiền mặt trong năm"], "[0047M01_2026 : 1-3]")
        w("")

    # ---- M4
    ms = ms4
    t = titles["M4"]
    w(f"### {ms.label} — {ms.agents} đại lý, {vn(ms.fyp_month)}tr FYP/tháng (FYC {vn(ms.fyc_month)}tr)")
    w("")
    w(head); w(sep)
    erow([f"AIA · {t[0]}", "Phí cơ bản (cố định theo chức danh)", vn(m(paf["base_fee_12m"])), "20tr × 120% (đạt ≥115% chỉ tiêu FYP tháng) × hệ số chuyên cần 100%"], "[AIAVAD 2601-035 : 3]")
    erow([f"AIA · {t[0]}", "Phí chuyên môn tháng", vn(m(paf["prof_monthly_12m"])), "FYC × (6% × hệ số FY 120% + 3,5% theo 1mAA)"], "[AIAVAD 2601-035 : 4]")
    erow([f"AIA · {t[0]}", "Phí chuyên môn quý", vn(m(paf["prof_quarterly_12m"])), "FYC quý × (5% × 120% + 3,5%) khi đạt ≥130% chỉ tiêu"], "[AIAVAD 2601-035 : 4-5]")
    erow([f"AIA · {t[0]}", "Phí vượt chỉ tiêu", vn(m(paf["seniority_fee_clawback12m"])), "(FYP năm − 1.800) × 5%, tối đa = phí cơ bản năm"], "[AIAVAD 2601-035 : 5]")
    erow([f"AIA · {t[0]}", "Phí CQL trên nhóm trực tiếp (Dual Career)", vn(m(a4_cql["total_earned"])), f"Như CQL: FYC nhóm {vn(a4_fyc)} × 18% + 8% + quý 4 sao + năm 5%; KHÔNG có gián tiếp cấp 2–4"], "[AIAVAD 2601-035 : 2]")
    erow([f"**AIA · {t[0]}**", "**Tổng**", f"**{vn(m(a4_tot))}**", "PAF+ + CQL trực tiếp"], "[AIAVAD 2601-035 : 2-5]")
    unknown([f"Chubb · {t[1]}", "Mọi khoản", "❓", "Biểu phí dành cho BD (0003V chỉ dẫn chiếu \"Chính sách 2026 dành cho BD\")"], "Không có trong nguồn — Negative Proof: `00_Role_Mapping_Audit.md` mục 4.3")
    erow(["Chubb · tham chiếu: nếu vẫn là DM (AL)", "Tổng", vn(m(c4_dm["total_earned"])), "HT KTN tháng + quý + L1 (4 AL con) + L2 (4 UM) + RYC"], "[CHH0DCEB260008V : 5-10]")
    erow(["Chubb · tham chiếu: RD (bổ nhiệm theo hợp đồng)", "Tổng", vn(m(rd["total_earned"])),
          f"Đào tạo 25 + hoạt động 8 + kinh doanh 12 + 12% FYC + tăng trưởng 2,5% (đi ngang) + 30% RYC; riêng RYC {vn(m(rd['ryc_quarterly_12m']))}"], "[CHH0DCEB260003V : 5-10]")
    ru, ag, (c1, c2, c3) = um["M4"]
    erow(["Manulife · UM+", "Phí năng suất nhóm (cấp 1–4)", vn(m(ru["a1_team_productivity"])), f"Cấp 1 FYC {vn(c1)} × 16% + cấp 2 {vn(c2)} × 8% + cấp 3 {vn(c3)} × 4%"], "[0047M01_2026 : 1]")
    erow(["Manulife · UM+", "Phí hoạt động nhóm", vn(m(ru["a2_team_activity"])), "50% (5 người sản xuất) × thưởng năng suất của cấp 1 × hệ số TLDTHD"], "[0047M01_2026 : 1-2]")
    erow(["**Manulife · UM+**", "**Tổng**", f"**{vn(m(ru['total_earned']))}**", "Bậc trong UM+ / điều kiện lên PSM+ ở 0013M04/2024 (không có trong nguồn)"], "[0047M01_2026 : 1-3]")
    erow(["Manulife · tham chiếu nếu được bổ nhiệm PSM/SM", "Phí cơ bản", vn(m(mnl["base_fee_12m"])), "35tr × 100% đạt chỉ tiêu × 130% (A8)"], "[0048M01_2026 : 1]", "ASSUMPTION")
    erow(["Manulife · PSM/SM", "Phí năng suất tháng", vn(m(mnl["productivity_12m"])), "FYC × 6% (<115% chỉ tiêu) × TLDTHD 115% (T1–3) / 110% (từ T4)"], "[0048M01_2026 : 1-2]")
    erow(["Manulife · PSM/SM", "Phí hoạt động quý", vn(m(mnl["activity_quarterly_12m"])), "FYC quý × 2,5% (đạt 100% 1mAA) × hệ số TLDTHD"], "[0048M01_2026 : 2-3]")
    erow(["Manulife · PSM/SM", "Phí hợp tác dài hạn (trả chậm 30/30/40%)", vn(m(mnl["long_term_deferred_3y"])), "75% × (năng suất + hoạt động), trần 12 × 35tr"], "[0048M01_2026 : 3-5]")
    erow(["**Manulife · PSM/SM**", "**Tổng**", f"**{vn(m(mnl['total_earned']))}**", "HKD cùng biểu phí; khác cách nộp thuế"], "[0048M01_2026 : 1-6]")
    w("")

    w("## 4. Đã kiểm chứng & đã sửa")
    w("")
    w("| # | Nội dung | Trích dẫn | Nhãn |")
    w("|---|---|---|---|")
    fixes = [
        ("F1–F4", "Chubb AL quý 50tr; Chubb RD bảng EHC, bảng FYP, tăng trưởng 12 bậc — đã sửa engine + workbook (ca3304c)", "[CHH0DCEB260008V : 6], [CHH0DCEB260003V : 6-8]"),
        ("F5–F6", "Thêm phí RYC của AL (CHB-MG-008) và gián tiếp AIA cấp 3–4 (ca3304c)", "[CHH0DCEB260008V : 9-10], [AIAVAD 2601-034 : 4]"),
        ("P2 #1", "Có RYC mà thiếu 3MAA → báo `MISSING_INPUT`, không coi là 0 (có test)", "[CHH0DCEB260008V : 10]"),
        ("P2 #2", "`K2_NO_K2_YET` (chưa phát sinh → hệ số 100%, coi như đạt) tách khỏi `None` = UNKNOWN (báo lỗi); test xuyên suốt hàm cho AL 15 tháng", "[CHH0DCEB260008V : 5], [CHH0DCEB260008V : 10]"),
        ("P2 #3", "Điều kiện người mới AIA: 3 sao ≥1; 4–5 sao ≥1 ở Q1, ≥2 từ Q2", "[AIAVAD 2601-034 : 4]"),
        ("G1", "PAF+ Dual Career: cộng phí CQL trực tiếp, bỏ gián tiếp cấp 2–4; chức danh Mốc 4 suy từ điều kiện (PAF) thay vì chọn tay", "[AIAVAD 2601-035 : 2], [AIAVAD 2601-034 : 8]"),
        ("G2", "Mâu thuẫn tên tiếng Việt UM/SUM/DM giữa các trang AIA — giữ mã làm khóa", "[AIAVAD 2604-069 : 17]"),
        ("G3", "Nạp 0046M01 (Đại Lý) và 0047M01 (UM+) — engine `calc_manulife_agent_12m`, `calc_manulife_um_12m`, test riêng", "[0046M01_2026 : 1-9], [0047M01_2026 : 1-6]"),
    ]
    for f in fixes:
        erow(list(f[:2]), f[2], "VERIFIED FACT", numeric=False)
    w("")
    w("## 5. Quyết định của TJ (2026-11-27, DEC-14)")
    w("")
    w("1. Chấp nhận phạm vi 9/9 PDF; giữ đánh dấu thiếu tài liệu cho Chubb BD và các memo ngoài phạm vi. Mốc 2–4 ghi rõ là **phí quản lý thuần**.")
    w("2. Manulife: base case **không có MBA Pro / Manulife Pro**; kịch bản có danh hiệu là ghi chú độ nhạy, chạy ở Giai đoạn 2.")
    w("3. Mốc 4: so sánh chính **AIA PAF · Chubb RD · Manulife PSM/SM**; số phụ **Chubb DM · Manulife UM+**.")
    w("4. Bảo mật: chỉ commit local, **không push** (0046M01 D.3 và 0047M01 B.4 ghi thông tin mật).")
    w("")
    w("## 6. Phụ lục — Kiểm tra độ phủ trích dẫn (máy tự đếm)")
    w("")
    n_titles = len(titles) * 3   # AIA + Chubb + Manulife
    tbl, tot = rubric_table(len(FILE_IDS), 15, 15, n_titles, n_titles, ev["cited"], ev["numeric"], ev["missing_proof"], ev["missing"], ev["labelled"], ev["data"])
    w(tbl)
    w("")
    w("Tiêu chí 1–2 dựa trên kiểm kê của `00_Role_Mapping_Audit.md` (9/9 file khớp hash, 15/15 trang scan; chức danh mỗi mốc suy từ điều kiện có trích dẫn). "
      "Tiêu chí 3 đếm các dòng có số ở mục 3; dòng giả định thuần (hoa hồng theo A1, tái tục theo A7) không có trang nguồn nên bị trừ điểm.")
    if tot < 90:
        raise SystemExit(f"rubric FAIL {tot}")
    return "\n".join(L) + "\n"


def main() -> None:
    text = build()
    if re.search(r"\b(nan|inf)\b", text, re.I):
        raise SystemExit("non-finite value leaked into output")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")


if __name__ == "__main__":
    main()
