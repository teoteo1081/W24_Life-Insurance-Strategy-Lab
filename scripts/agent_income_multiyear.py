"""Thu nhập đại lý 3 năm có tái tục — AIA Alpha, Chubb Life (AR) và phương án đề xuất.

Mục đích: trả lời câu hỏi "đại lý theo phương án đề xuất nhận bao nhiêu so với đối thủ" trên cả vòng đời
hợp đồng, không chỉ 12 tháng đầu (bản cũ đặt SYC = 0 nên bỏ mất phần thưởng tái tục).

ASSUMPTION (áp CHUNG cho mọi hãng để so sánh công bằng; chỉ phần thưởng riêng của từng chính sách khác nhau):
- Đại lý viết cùng một mức FYC mỗi tháng trong cả 3 năm; FYC = 30% FYP (UL, `assumed_fyc_to_fyp_rate`).
- Phí tái tục năm sau của một cohort = FYP cohort × K2; năm thứ 3 của cohort = FYP × K2 × K3_RATIO.
- Hoa hồng tái tục cơ bản: năm 2 = 20% phí tái tục, năm 3 = 10% (`RENEWAL_COMM_Y2/Y3`).
- Đại lý đã có thâm niên (Chubb tenure_months_start = 13; AIA policy_year 2026), K2 giữ nguyên qua 3 năm.
Manulife: không có tài liệu tầng đại lý (GAP-MNL-01) => UNKNOWN, không tính.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from model.compensation.compensation_engine import (  # noqa: E402
    ProposalParams,
    calc_aia_cvtv_12m,
    calc_chubb_ar_12m,
    calc_proposal_agent_12m,
)

FYC_TO_FYP = 0.30
RENEWAL_COMM_Y2 = 0.20
RENEWAL_COMM_Y3 = 0.10
K3_RATIO = 0.92


def renewal_commission_by_year(fyc_month: float, k2: float) -> list[float]:
    """SYC/RYC mỗi tháng (triệu VND) cho năm 1, 2, 3 khi mỗi năm viết cùng một cohort."""
    fyp_year = fyc_month * 12 / FYC_TO_FYP
    k = k2 / 100.0
    y2 = fyp_year * k * RENEWAL_COMM_Y2                      # cohort năm 1 tái tục lần đầu
    y3 = fyp_year * k * RENEWAL_COMM_Y2 + fyp_year * k * K3_RATIO * RENEWAL_COMM_Y3
    return [0.0, y2 / 12, y3 / 12]


def scheme_year(scheme: str, fyc_m: float, syc_m: float, k2: float, params: ProposalParams | None = None) -> float:
    fyc, syc = [fyc_m] * 12, [syc_m] * 12
    if scheme == "AIA":
        r = calc_aia_cvtv_12m(fyc, syc, fy_pct=k2, policy_year=2026, assumed_fyc_to_fyp_rate=FYC_TO_FYP)
    elif scheme == "CHUBB":
        r = calc_chubb_ar_12m(fyc, syc, [True] * 12, k2_pct=k2, tenure_months_start=13,
                              assumed_fyc_to_fyp_rate=FYC_TO_FYP)
    elif scheme == "PROPOSAL":
        r = calc_proposal_agent_12m(fyc, syc, k2_pct=k2, params=params)
    else:
        raise ValueError(scheme)
    return float(fyc_m * 12 + syc_m * 12 + r["total_bonuses_earned"])


def agent_income_3y(fyc_m: float, k2: float, params: ProposalParams | None = None) -> dict:
    syc = renewal_commission_by_year(fyc_m, k2)
    out = {}
    for s in ("AIA", "CHUBB", "PROPOSAL"):
        years = [round(scheme_year(s, fyc_m, syc[y], k2, params), 2) for y in range(3)]
        out[s] = {"y1": years[0], "y2": years[1], "y3": years[2], "total_3y": round(sum(years), 2)}
    out["MANULIFE"] = "UNKNOWN"
    return out


def main() -> None:
    rows = {}
    for k2 in (82.0, 72.0, 62.0):
        for fyc in (5.0, 15.0, 35.0):
            rows[f"K2={k2:.0f}|FYC={fyc:.0f}"] = agent_income_3y(fyc, k2)
    print(json.dumps(rows, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
