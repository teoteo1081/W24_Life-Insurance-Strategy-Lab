"""Mốc quy mô dùng chung + suy chức danh đạt được từ điều kiện thăng cấp (có trích dẫn) + chấm rubric.

Dùng bởi scripts/build_role_audit.py (00) và scripts/build_interview_income_table.py (01).
Mọi ngưỡng ở đây được chép từ PDF gốc, kèm `[FileName : PageNumber]` (AGENTS.md luật 4).
Plug-and-play: thêm hãng mới = thêm 1 danh sách LADDER (bậc, điều kiện, trích dẫn) + biểu phí trong engine.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

REPO = Path(__file__).resolve().parents[1]
CITE_RE = re.compile(r"\[[^\]:]+ : [0-9]+(-[0-9]+)?\]")

# Mã file duy nhất (xuất hiện trong tên file nguồn) -> Source_ID
FILE_IDS = {
    "AIAVAD 2604-069": "SRC-POL-AIA-ALP-001",
    "AIAVAD 2601-034": "SRC-POL-AIA-ALP-002",
    "AIAVAD 2601-035": "SRC-POL-AIA-ALP-003",
    "0046M01_2026": "SRC-POL-MNL-002",
    "0047M01_2026": "SRC-POL-MNL-003",
    "0048M01_2026": "SRC-POL-MNL-001",
    "CHH0DCEB260007V": "SRC-POL-CHB-001",
    "CHH0DCEB260008V": "SRC-POL-CHB-002",
    "CHH0DCEB260003V": "SRC-POL-CHB-003",
}

# ASSUMPTION chung cho mọi mốc
FYC_RATE = 0.30
K2 = 85.0
RECRUITS_PER_QUARTER = 2           # người mới có hoạt động / quý ở nhóm trực tiếp
PERSONAL_CASES_6M = 2              # quản lý tự bán tối thiểu 2 HĐ / 6 tháng (để giữ điều kiện AIA), FYC không đáng kể
COMPANY_TENURE_MONTHS = 24         # thâm niên tại công ty (Chubb DM->BD cần 18)


@dataclass(frozen=True)
class Milestone:
    mid: str
    label: str
    agents: int                    # đại lý sản xuất
    fyp_month: float               # FYP cả tổ chức / tháng
    direct_agents: int             # đại lý trực tiếp của người đang xét
    sub_units: Tuple[Tuple[str, int], ...]   # (loại, số đại lý của đơn vị con) báo cáo trực tiếp
    grand_sub_units: int           # số quản lý cấp con thứ 2 (dưới đơn vị con)

    @property
    def fyp_per_agent(self) -> float:
        return self.fyp_month / self.agents

    @property
    def fyc_month(self) -> float:
        return self.fyp_month * FYC_RATE

    @property
    def direct_fyc_month(self) -> float:
        return self.fyp_per_agent * FYC_RATE * self.direct_agents

    @property
    def direct_managers(self) -> int:
        return len(self.sub_units)


def load_milestones() -> List[Milestone]:
    data = json.loads((REPO / "knowledge/policies/scale-milestones.json").read_text(encoding="utf-8"))["scale_milestones"]
    for m in data:
        for k in ("milestone_id", "label", "producing_agents", "org_fyp_month_vnd_m"):
            if k not in m:
                raise ValueError(f"scale-milestones.json missing {k}")
        if not (isinstance(m["org_fyp_month_vnd_m"], (int, float)) and math.isfinite(m["org_fyp_month_vnd_m"]) and m["org_fyp_month_vnd_m"] > 0):
            raise ValueError("org_fyp_month_vnd_m must be finite > 0")
    struct = {  # cấu trúc giả định (ASSUMPTION A5), khớp mô tả trong scale-milestones.json
        "M1": (1, (), 0),
        "M2": (5, (), 0),
        "M3": (5, (("UM", 5), ("UM", 5)), 0),
        "M4": (5, (("BM", 15), ("BM", 15), ("UM", 5), ("UM", 5)), 4),
    }
    out = []
    for m in data:
        d, subs, g = struct[m["milestone_id"]]
        ms = Milestone(m["milestone_id"], m["label"], int(m["producing_agents"]), float(m["org_fyp_month_vnd_m"]), d, subs, g)
        if d + sum(n for _, n in subs) != ms.agents:
            raise ValueError(f"{ms.mid}: structure does not add up to {ms.agents} agents")
        out.append(ms)
    return out


# ---------------- Suy chức danh đạt được ----------------
@dataclass
class Check:
    metric: str
    need: float
    have: float
    cite: str
    ok: bool = field(init=False)

    def __post_init__(self) -> None:
        self.ok = self.have >= self.need


def _branch_with_70pct_cap(m: Milestone, per_agent: float, months: int, requirement: float, direct_counts_full: bool = True) -> float:
    """Quy định 70% chỉ tiêu: nhánh con đóng góp tối đa 70% yêu cầu ([AIAVAD 2601-034 : 9], [AIAVAD 2601-035 : 6])."""
    total = per_agent * months * m.direct_agents
    for _, n in m.sub_units:
        total += min(per_agent * months * n, 0.70 * requirement)
    return total


def aia_title(m: Milestone) -> Tuple[str, List[Check]]:
    """Thang AIA: SA -> UM -> SUM -> DM -> SDM [AIAVAD 2601-034 : 8] -> PAF [AIAVAD 2601-034 : 8] -> AF.. [AIAVAD 2601-035 : 6]."""
    fyc_pa = m.fyp_per_agent * FYC_RATE
    act_3m = m.agents * 3                                   # mọi đại lý hoạt động mỗi tháng (A4)
    recruits_6m = RECRUITS_PER_QUARTER * 2 if m.direct_agents > 1 else 0
    if m.mid == "M1":
        return "SA", [Check("Tuyển/giới thiệu trực tiếp 6 tháng (lên UM)", 2, 0, "[AIAVAD 2601-034 : 8]")]
    ladder = [  # (bậc, UM+ trực tiếp, lượt hoạt động 3T, FYC tín chỉ toàn nhánh 6T)
        ("UM", 0, 5, 50), ("SUM", 0, 9, 100), ("DM", 1, 13, 200), ("SDM", 2, 17, 400)]
    title, last = "SA", []
    for code, um_plus, act, fyc6 in ladder:
        checks = [
            Check("Tuyển/giới thiệu trực tiếp 6 tháng", 2, recruits_6m, "[AIAVAD 2601-034 : 8]"),
            Check("UM+ trực tiếp", um_plus, m.direct_managers, "[AIAVAD 2601-034 : 8]"),
            Check("Lượt CVTV hoạt động 3 tháng toàn nhánh", act, act_3m, "[AIAVAD 2601-034 : 8]"),
            Check("FYC tín chỉ toàn nhánh 6 tháng (áp 70%)", fyc6, _branch_with_70pct_cap(m, fyc_pa, 6, fyc6), "[AIAVAD 2601-034 : 8-9]"),
            Check("FYC tín chỉ nhóm trực tiếp 6 tháng", 50, fyc_pa * 6 * m.direct_agents, "[AIAVAD 2601-034 : 8]"),
            Check("Tỉ lệ duy trì HĐ toàn nhánh (%)", 70, K2, "[AIAVAD 2601-034 : 8]"),
            Check("HĐ thuần cá nhân 6 tháng", 2, PERSONAL_CASES_6M, "[AIAVAD 2601-034 : 8]"),
        ]
        if all(c.ok for c in checks):
            title, last = code, checks
        else:
            last = (last if title != "SA" else []) + [c for c in checks if not c.ok]
            break
    if title == "SDM":
        fyp6_req = 1200
        paf = [
            Check("UM+ trực tiếp (lên PAF)", 3, m.direct_managers, "[AIAVAD 2601-034 : 8]"),
            Check("Lượt CVTV hoạt động 3 tháng (lên PAF)", 18, act_3m, "[AIAVAD 2601-034 : 8]"),
            Check("FYP toàn nhánh 6 tháng, áp 70% (lên PAF)", fyp6_req, _branch_with_70pct_cap(m, m.fyp_per_agent, 6, fyp6_req), "[AIAVAD 2601-034 : 8]"),
            Check("Tỉ lệ duy trì HĐ toàn nhánh (%)", 70, K2, "[AIAVAD 2601-034 : 8]"),
        ]
        if all(c.ok for c in paf):
            title, last = "PAF", paf
            af = [Check("Báo cáo trực tiếp UM+ (lên AF)", 5, m.direct_managers, "[AIAVAD 2601-035 : 6]"),
                  Check("FYP 6 tháng (lên AF)", 2500, m.fyp_month * 6, "[AIAVAD 2601-035 : 6]"),
                  Check("1mAA 3 tháng (lên AF)", 35, act_3m, "[AIAVAD 2601-035 : 6]")]
            if all(c.ok for c in af):
                title, last = "AF", af
            else:
                last = paf + [c for c in af if not c.ok]
        else:
            last = last + [c for c in paf if not c.ok]
    return title, last


def chubb_title(m: Milestone) -> Tuple[str, List[Check]]:
    """Thang Chubb: AR -> UM -> SM -> DM -> BD [CHH0DCEB260007V : 7]; FYC/3MAA tính trên toàn Nhóm/Ban/Khu vực [CHH0DCEB260007V : 8]."""
    fyc_pa = m.fyp_per_agent * FYC_RATE
    new_3m, new_6m = (RECRUITS_PER_QUARTER, RECRUITS_PER_QUARTER * 2) if m.direct_agents > 1 else (0, 0)
    referred = new_3m
    ladder = [  # (bậc đích, kỳ xét tháng, FYC tích lũy, 3MAA, 3MAA mới, AL trực tiếp, ĐL giới thiệu đạt 3MAA)
        ("UM", 3, 25, 0, 0, 0, 2), ("SM", 3, 50, 5, 1, 1, 0), ("DM", 6, 200, 10, 2, 2, 0), ("BD", 6, 450, 20, 3, 4, 0)]
    title, last = "AR", []
    for code, months, fyc, maa, new, al, ref in ladder:
        checks = [Check(f"FYC tích lũy {months} tháng (lên {code})", fyc, fyc_pa * months * m.agents, "[CHH0DCEB260007V : 7]"),
                  Check(f"K2 toàn nhóm (%) (lên {code})", 55, K2, "[CHH0DCEB260007V : 7]")]
        if maa:
            checks += [Check(f"Số 3MAA (lên {code})", maa, m.agents, "[CHH0DCEB260007V : 7]"),
                       Check(f"3MAA từ đại lý mới (lên {code})", new, new_6m if months == 6 else new_3m, "[CHH0DCEB260007V : 7]"),
                       Check(f"AL báo cáo trực tiếp (lên {code})", al, m.direct_managers, "[CHH0DCEB260007V : 7]")]
        if ref:
            checks.append(Check("Đại lý được giới thiệu đạt 3MAA (lên UM)", ref, referred, "[CHH0DCEB260007V : 7]"))
        if code == "BD":
            checks.append(Check("Thời gian làm việc tại công ty (tháng) (lên BD)", 18, COMPANY_TENURE_MONTHS, "[CHH0DCEB260007V : 7]"))
        if all(c.ok for c in checks):
            title, last = code, checks
        else:
            last = checks if title == "AR" else last + [c for c in checks if not c.ok]
            break
    return title, last


def manulife_title(m: Milestone) -> Tuple[str, List[Check]]:
    """Manulife: tuyến đại lý [0046M01_2026 : 1] và tuyến Quản Lý Đại Lý UM+ [0047M01_2026 : 1].

    Điều kiện lên/xuống bậc (UM, SUM, ... và PSM+) nằm ở 0013M04/2024/ASBD — văn bản này được dẫn chiếu
    [0047M01_2026 : 6] nhưng KHÔNG có trong nguồn, nên chỉ xác định được TUYẾN (Đại Lý / UM+), không xác định được bậc.
    Người có cấp báo cáo trực tiếp thì hưởng biểu phí UM+ (cấp 1 = báo cáo trực tiếp) [0047M01_2026 : 1].
    """
    if m.direct_agents <= 1 and not m.sub_units:
        return "Đại Lý", []
    return "UM+", [Check("Điều kiện bậc trong UM+ (0013M04/2024 — không có trong nguồn)", 1, 0, "[0047M01_2026 : 6]")]


# ---------------- Rubric ----------------
LABELS = ("VERIFIED FACT", "ASSUMPTION", "MODEL_OUTPUT", "UNKNOWN", "CONFLICTING EVIDENCE", "HYPOTHESIS", "SOURCE CLAIM")


def rubric_table(files_ok: int, scan_pages_seen: int, scan_pages_total: int,
                 titles_ok: int, titles_total: int,
                 cited_rows: int, numeric_rows: int,
                 missing_with_proof: int, missing_total: int,
                 labelled_rows: int, total_rows: int, files_total: Optional[int] = None) -> Tuple[str, float]:
    files_total = len(FILE_IDS) if files_total is None else files_total
    for v in (files_ok, scan_pages_seen, titles_ok, titles_total, cited_rows, numeric_rows, missing_with_proof, missing_total, labelled_rows, total_rows):
        if not isinstance(v, int) or v < 0:
            raise ValueError("rubric inputs must be non-negative ints")
    scan_factor = scan_pages_seen / scan_pages_total if scan_pages_total else 1.0
    c1 = 25 * (files_ok - 1 + scan_factor) / files_total if files_ok == files_total else 25 * files_ok / files_total
    c2 = 25 * titles_ok / titles_total if titles_total else 0.0
    c3 = 20 * cited_rows / numeric_rows if numeric_rows else 0.0
    c4 = 15 * missing_with_proof / missing_total if missing_total else 15.0
    c5 = 15 * labelled_rows / total_rows if total_rows else 0.0
    tot = round(c1, 1) + round(c2, 1) + round(c3, 1) + round(c4, 1) + round(c5, 1)
    res = "PASS" if tot >= 90 else "FAIL"
    lines = [
        "| # | Tiêu chí (`qa/data-ingestion-rubric.md`) | Điểm | Tối đa | Căn cứ đo được |",
        "|---|---|---:|---:|---|",
        f"| 1 | Độ phủ nguồn {files_total}/{files_total} file | {c1:.1f} | 25 | {files_ok}/{files_total} file mở được và khớp SHA-256; bản scan soát {scan_pages_seen}/{scan_pages_total} trang |",
        f"| 2 | Chức danh gốc & tuyến | {c2:.1f} | 25 | {titles_ok}/{titles_total} chức danh có tên nguyên văn khớp trang trích (hoặc đối chiếu bằng mắt với bản scan) và có `track_type` |",
        f"| 3 | Trích dẫn `[File : Trang]` cho từng con số | {c3:.1f} | 20 | {cited_rows}/{numeric_rows} dòng có số mang trích dẫn đúng mẫu |",
        f"| 4 | Negative Proof | {c4:.1f} | 15 | {missing_with_proof}/{missing_total} kết luận \"không có trong tài liệu\" kèm nhật ký tìm kiếm |",
        f"| 5 | Tách Fact / Assumption | {c5:.1f} | 15 | {labelled_rows}/{total_rows} dòng có nhãn phân loại |",
        f"| | **Tổng** | **{tot:.1f}** | **100** | **{res}** (ngưỡng 90) — `SELF_VERIFIED`, chưa phải kiểm toán độc lập |",
    ]
    return "\n".join(lines), tot
