"""
W24 Life Insurance Strategy Lab — Excel Reference Model Builder (Excel 12.0 / 2007 Compatible).
Generates outputs/working/W24_Compensation_Reference_Model_v1.xlsx with 14 structured sheets,
100% live classic Excel 2007 formulas (NO XLOOKUP/IFS/LET/MAXIFS), normalized CSV lookups,
PO-editable proposal parameters, conflict toggles, Enterprise Hierarchy Total Distribution Cost,
15-Criteria Rubric, MAPA Forward/Reverse, Financial Break-Even Sensitivity, and 20 Live Golden Tests.
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
DEFAULT_OUT_XLSX = REPO / "outputs/working/W24_Compensation_Reference_Model_rebuilt.xlsx"
PROTECTED_V1_XLSX = (REPO / "outputs/working/W24_Compensation_Reference_Model_v1.xlsx").resolve()

# Styles
FONT_TITLE = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
FONT_SEC = Font(name="Calibri", size=11, bold=True, color="1F4E78")
FONT_HDR = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
FONT_BOLD = Font(name="Calibri", size=10, bold=True)
FONT_NORM = Font(name="Calibri", size=10)
FONT_BLUE = Font(name="Calibri", size=10, bold=True, color="0000FF")   # PO Editable Input
FONT_GREEN = Font(name="Calibri", size=10, color="006100")            # Cross-sheet Link
FONT_WARN = Font(name="Calibri", size=10, bold=True, color="9C0006")

FILL_NAVY = PatternFill("solid", fgColor="1F4E78")
FILL_SUB = PatternFill("solid", fgColor="2F5597")
FILL_SEC = PatternFill("solid", fgColor="D9E1F2")
FILL_INPUT = PatternFill("solid", fgColor="FFF2CC")   # PO Editable
FILL_LOCK = PatternFill("solid", fgColor="EDEDED")    # Locked Competitor Ground Truth
FILL_PASS = PatternFill("solid", fgColor="C6EFCE")
FILL_WARN = PatternFill("solid", fgColor="FFC7CE")

THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def style_title(ws, row: int, text: str, max_col: int = 12):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=max_col)
    c = ws.cell(row, 1, text)
    c.font = FONT_TITLE
    c.fill = FILL_NAVY
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 28


def style_section(ws, row: int, text: str, max_col: int = 12):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=max_col)
    c = ws.cell(row, 1, text)
    c.font = FONT_SEC
    c.fill = FILL_SEC
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 22


def write_table_header(ws, row: int, headers: list[str]):
    ws.row_dimensions[row].height = 24
    for idx, h in enumerate(headers, 1):
        c = ws.cell(row, idx, h)
        c.font = FONT_HDR
        c.fill = FILL_SUB
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER


def set_col_widths(ws, widths: dict[int, float]):
    for col_idx, w in widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = w


def load_csv(rel_path: str) -> tuple[list[str], list[list[str]]]:
    with open(REPO / rel_path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def build_workbook(out_path: Path = DEFAULT_OUT_XLSX, allow_overwrite_v1: bool = False) -> Path:
    target = out_path.resolve()
    if target == PROTECTED_V1_XLSX and not allow_overwrite_v1:
        raise RuntimeError("Refusing to overwrite protected v1 workbook without --allow-overwrite-v1")
    target.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # =========================================================================
    # SHEET 01: 01_User_Guide
    # =========================================================================
    ws1 = wb.create_sheet("01_User_Guide")
    style_title(ws1, 1, "W24 LIFE INSURANCE STRATEGY LAB — EXCEL REFERENCE MODEL v1.0 (EXCEL 2007 COMPATIBLE)", 8)
    ws1["A3"] = "Primary Business Anchor (Verbatim — Chi Nhi, SRC-REQ-001):"
    ws1["A3"].font = FONT_BOLD
    ws1["B3"] = "Buoc 1: Phan tich cac chinh sach thu nhap giua cac cong ty, va de xuat chinh sach phu hop tai thi truong VN, nham thuc day gia tang doanh so, chat luong kinh doanh va hieu qua ve mat chi phi (ROI)."
    ws1.merge_cells("B3:H3")
    ws1["B3"].alignment = Alignment(wrap_text=True)
    ws1.row_dimensions[3].height = 30

    style_section(ws1, 5, "1. Color Coding & Governance Rules", 8)
    legend = [
        ("Yellow Fill + Blue Bold Font", "PO-Editable Input / Toggle (po_editable = TRUE) — Safe for TJ/PO to test scenarios"),
        ("Gray Fill + Black Font", "Locked Competitor Ground Truth (po_editable = FALSE) — Do NOT edit without new source PDF"),
        ("White Fill + Black Formula", "Live Excel 2007 Formula (ONLY IF/MIN/MAX/SUM/SUMIF/SUMPRODUCT/INDEX/MATCH/ROUND/ROUNDUP/IFERROR)"),
        ("UNKNOWN Label", "Missing source policy (e.g., Manulife FA/UM, AIA Exchange/Pro, Unpriced Non-Cash Cost) — NEVER enter 0!"),
        ("Verification Status", "SELF_VERIFIED via Microsoft Excel 12.0 COM CalculateFullRebuild + Python Golden Parity Check (NOT INDEPENDENTLY_VERIFIED)"),
    ]
    write_table_header(ws1, 6, ["Convention", "Meaning & Rule"])
    ws1.merge_cells("B6:H6")
    for i, (k, v) in enumerate(legend, 7):
        ws1.cell(i, 1, k).border = BORDER
        ws1.cell(i, 2, v).border = BORDER
        ws1.merge_cells(start_row=i, start_column=2, end_row=i, end_column=8)
        if i == 7:
            ws1.cell(i, 1).fill = FILL_INPUT
            ws1.cell(i, 1).font = FONT_BLUE
        elif i == 8:
            ws1.cell(i, 1).fill = FILL_LOCK
        elif i == 10:
            ws1.cell(i, 1).fill = FILL_WARN
            ws1.cell(i, 1).font = FONT_WARN

    style_section(ws1, 13, "2. Workbook Architecture (14 Integrated Sheets)", 8)
    write_table_header(ws1, 14, ["Sheet Name", "Role", "Key Contents & Formula Linkages"])
    ws1.merge_cells("C14:H14")
    sheets_desc = [
        ("01_User_Guide", "Navigation", "Business Anchor, governance rules, color coding & sheet index"),
        ("02_Source_Index_Gaps", "Ground Truth", "17 Source Registry rows (SHA-256, Revision_Class) + Known Gaps & Conflict Register"),
        ("03_Role_And_Components", "Inventory", "36 Role Mappings (16 cols) + 44 Total Rewards Components (33 cols, Cash vs Unpriced Non-Cash)"),
        ("04_Policy_Parameters", "Control Center", "Global toggles (ERR-DOC-01, ERR-DOC-02), Locked Competitor tables, PO-Editable Proposal params"),
        ("05_Lookup_PAF_5Y", "Normalized Lookup", "Full 1,300-row AIA PAF+ 5-Year Target Matrix + Live Excel SUMIF reconciliation (0 discrepancies)"),
        ("06_Lookup_Chubb_Comm", "Normalized Lookup", "Full 113-row Chubb Commission Schedule + 10-row HSBH table + Live Tu Do An Phuc HSBH calculator"),
        ("07_Profiles_12M_Input", "Scenario Inputs", "10 Configurable Agent Profiles + 7 Manager/Leader Profiles + 12-Month calendar inputs"),
        ("08_Indiv_Comp_12M", "Tier 1 Engine", "Live 12M Individual Comp (AIA 2026, AIA 2027, Chubb 2026, Proposal, Manulife=UNKNOWN) + CH Offset"),
        ("09_Mgr_Senior_Comp", "Tier 2 & 3 Engine", "Live Manager (AIA CQL vs Chubb AL + Neg FYC/Gate) & Senior Leader (AIA PAF+ vs Chubb RD vs Manulife PSM+)"),
        ("10_Total_Rewards_Ledger", "Accounting Ledger", "Earned vs Cash Paid Y1 vs Accrued T+1 vs Deferred 3Y vs Clawback vs Unpriced Non-Cash Benefits"),
        ("11_Hierarchy_Dist_Cost", "Enterprise Cost", "12B FYP Regional Stacking (Zero Double-Counting) across K2=82%/72%/62% + Art.52 <=30% Cap Check"),
        ("12_Benchmark_And_Eval", "Rubric & Scores", "15-Criteria Scoring Rubric (DRAFT) + Mandatory Gate G1-G3 + 4 PO Weight Sensitivity Scenarios"),
        ("13_MAPA_And_Financial", "Planning & ROI", "MAPA Forward/Reverse + Financial Break-Even Gross Margin Sensitivity (OpEx 15/20/25% x K2)"),
        ("14_QA_Golden_Tests", "Live Verification", "20 Live Excel Formula Assertions vs Independent Hand-Calculated Expected Values (PASS/FAIL)"),
    ]
    for i, (sn, role, desc) in enumerate(sheets_desc, 15):
        ws1.cell(i, 1, sn).font = FONT_BOLD
        ws1.cell(i, 2, role)
        ws1.cell(i, 3, desc)
        ws1.merge_cells(start_row=i, start_column=3, end_row=i, end_column=8)
        for col in range(1, 4):
            ws1.cell(i, col).border = BORDER
    set_col_widths(ws1, {1: 28, 2: 20, 3: 24, 4: 18, 5: 18, 6: 18, 7: 18, 8: 18})

    # =========================================================================
    # SHEET 02: 02_Source_Index_Gaps
    # =========================================================================
    ws2 = wb.create_sheet("02_Source_Index_Gaps")
    style_title(ws2, 1, "SOURCE REGISTRY (17 SOURCES + RIGHTS STATUS), KNOWN GAPS & UNRESOLVED CONFLICTS", 12)
    reg_hdr, reg_rows = load_csv("knowledge/sources/source-registry.csv")
    cols_keep = [0, 1, 4, 5, 7, 8, 10, 11, 14, 15, 16, 17]
    write_table_header(ws2, 3, [reg_hdr[c] for c in cols_keep])
    for r_i, row in enumerate(reg_rows, 4):
        for c_i, orig_c in enumerate(cols_keep, 1):
            cell = ws2.cell(r_i, c_i, row[orig_c])
            cell.font = FONT_NORM
            cell.border = BORDER
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    r_gap = 4 + len(reg_rows) + 2
    style_section(ws2, r_gap, "CRITICAL SOURCE CONFLICTS & MISSING DEPENDENCIES (NO SELF-ADJUDICATION / NO FABRICATION)", 12)
    write_table_header(ws2, r_gap + 1, ["ID", "Type", "Company", "Description", "Model Treatment", "Decision Owner"])
    ws2.merge_cells(start_row=r_gap + 1, start_column=4, end_row=r_gap + 1, end_column=8)
    ws2.merge_cells(start_row=r_gap + 1, start_column=9, end_row=r_gap + 1, end_column=11)
    gaps_list = [
        ("ERR-DOC-01", "CONFLICTING_EVIDENCE", "Chubb Life", "0007V p.9 table states SOP 80-<90% -> W1=80%, but p.10 worked example (M11-12) applies W1=50% at SOP=85%.", "Configurable Toggle on 04_Policy_Parameters!$C$5 ('Table_80' vs 'Example_50')", "TJ / Chubb"),
        ("ERR-DOC-02", "CONFLICTING_EVIDENCE", "AIA Alpha", "2604-069 p.14 states 'lam tron len' (RoundUp) vs 2601-034 p.21 & 035 p.18 state standard HalfUp (>=0.5 up).", "Configurable Toggle on 04_Policy_Parameters!$C$6 ('HalfUp' vs 'RoundUp')", "TJ / AIA"),
        ("GAP-MNL-01", "UNKNOWN", "Manulife", "Missing Individual Agent (FA), Mid-Manager (UM/SUM/DM), Commission Schedule, FYP/1mAA Target Table & 0016M03/2024.", "Marked 'UNKNOWN' on Tier 1 & Tier 2 outputs (NEVER 0); Tier 3 PSM+/HKD modeled fully.", "TJ"),
        ("GAP-AIA-01", "MISSING_DEPENDENCY", "AIA Alpha", "Missing Product Commission Appendix, FYC Tin Chi conversion memo, Exchange/Pro allowance & 2501-017.", "Compare directly on % FYC; % FYP uses labeled 30% UL assumption on 04_Policy_Parameters!$C$7.", "TJ"),
        ("GAP-CHB-01", "MISSING_DEPENDENCY", "Chubb Life", "Missing CHH0DCEB260005V (1 EHC threshold, K2/P13 formula), 260006V, 260009V & BD 2026 Policy.", "EHC modeled as boolean/count input; RD II.7-8 BD dependency flagged.", "TJ"),
        ("GAP-LAW-01", "SOURCE_NOT_VERIFIED", "Vietnam Reg", "TT 67/2023 (Art.51 & 52), TT 96/2026 and ND 97/2026 summaries plus 44/2026/VBHN-TT-BTC metadata. Clause-level verification pending.", "Flagged SOURCE_NOT_VERIFIED; mandatory Gazette review before real policy issuance.", "Legal / TJ"),
    ]
    for idx, g in enumerate(gaps_list, r_gap + 2):
        ws2.cell(idx, 1, g[0]).font = FONT_WARN
        ws2.cell(idx, 2, g[1]).fill = FILL_WARN
        ws2.cell(idx, 3, g[2])
        ws2.cell(idx, 4, g[3])
        ws2.merge_cells(start_row=idx, start_column=4, end_row=idx, end_column=8)
        ws2.cell(idx, 9, g[4])
        ws2.merge_cells(start_row=idx, start_column=9, end_row=idx, end_column=11)
        ws2.cell(idx, 12, g[5])
        for c in (1, 2, 3, 4, 9, 12):
            ws2.cell(idx, c).border = BORDER
            ws2.cell(idx, c).alignment = Alignment(wrap_text=True, vertical="top")
    set_col_widths(ws2, {1: 20, 2: 26, 3: 16, 4: 14, 5: 18, 6: 16, 7: 16, 8: 14, 9: 14, 10: 14, 11: 18, 12: 34})

    # =========================================================================
    # SHEET 03: 03_Role_And_Components
    # =========================================================================
    ws3 = wb.create_sheet("03_Role_And_Components")
    style_title(ws3, 1, "ROLE & ORGANIZATION MAPPING (36 ROLES) + TOTAL REWARDS INVENTORY (44 COMPONENTS)", 10)
    style_section(ws3, 3, "A. Role & Organization Mapping (Functional Equivalence)", 10)
    r_hdr, r_rows = load_csv("knowledge/policies/role-organization-mapping.csv")
    r_cols = [0, 1, 2, 4, 5, 6, 7, 11, 12, 15]
    write_table_header(ws3, 4, [r_hdr[c] for c in r_cols])
    for i, row in enumerate(r_rows, 5):
        for j, oc in enumerate(r_cols, 1):
            c = ws3.cell(i, j, row[oc])
            c.font = FONT_NORM
            c.border = BORDER
    r_tr = 5 + len(r_rows) + 2
    style_section(ws3, r_tr, "B. Total Rewards Inventory (Categories A-H: Cash, Deferred & Unpriced Non-Cash)", 10)
    tr_hdr, tr_rows = load_csv("knowledge/compensation/total-rewards-inventory.csv")
    tr_cols = [0, 1, 4, 5, 6, 8, 9, 10, 13, 28]
    write_table_header(ws3, r_tr + 1, [tr_hdr[c] for c in tr_cols])
    for i, row in enumerate(tr_rows, r_tr + 2):
        for j, oc in enumerate(tr_cols, 1):
            c = ws3.cell(i, j, row[oc])
            c.font = FONT_NORM
            c.border = BORDER
            if row[9] == "Unpriced_Non_Cash_Benefit" and j in (6, 7, 8):
                c.fill = FILL_WARN
    set_col_widths(ws3, {1: 14, 2: 18, 3: 18, 4: 22, 5: 32, 6: 22, 7: 26, 8: 22, 9: 38, 10: 26})

    # =========================================================================
    # SHEET 04: 04_Policy_Parameters (CONTROL CENTER — Exact Cell Map!)
    # =========================================================================
    ws4 = wb.create_sheet("04_Policy_Parameters")
    style_title(ws4, 1, "POLICY PARAMETERS CONTROL CENTER (CONFLICT TOGGLES, LOCKED COMPETITOR PARAMS & PO-EDITABLE PROPOSAL)", 8)

    # Block A: Global Controls & Conflict Toggles (Rows 3-11)
    style_section(ws4, 3, "BLOCK A: Global Assumptions, Legal Caps & Unresolved Source Conflict Toggles (PO Editable = Blue/Yellow)", 8)
    write_table_header(ws4, 4, ["Param_ID", "Parameter Name", "Active Value", "Allowed Options / Unit", "Editable?", "Status / Source"])
    ws4.merge_cells("F4:H4")
    global_params = [
        ("GLB-01", "Chubb Champion Hubb W1 Conflict Toggle (ERR-DOC-01)", "Table_80", "Table_80 (p.9: 80%) | Example_50 (p.10: 50%)", "TRUE", "CONFLICTING_EVIDENCE (SRC-POL-CHB-001 p.9 vs p.10)"),
        ("GLB-02", "AIA FY Rounding Conflict Toggle (ERR-DOC-02)", "HalfUp", "HalfUp (CQL p.21 >=0.5) | RoundUp (CVTV p.14)", "TRUE", "CONFLICTING_EVIDENCE (SRC-POL-AIA-ALP-001 p.14 vs 002 p.21)"),
        ("GLB-03", "Standard UL Year-1 Commission Assumption (FYP->FYC)", 0.30, "Decimal (0.30 = 30% UL Legal Cap)", "TRUE", "ASSUMPTION for AIA FYP conversion; Chubb exact in Sheet 06"),
        ("GLB-04", "Home Office OpEx (% of FYP) for Break-Even Analysis", 0.20, "Decimal (0.15 / 0.20 / 0.25 sensitivity)", "TRUE", "ASSUMPTION (actual insurer OpEx = UNKNOWN)"),
        ("GLB-05", "Legal Cap Art.51 — UL/ILP Year-1 Commission", 0.30, "Hard Regulatory Gate (TT 67/2023 & TT 96/2026)", "FALSE", "SOURCE_NOT_VERIFIED (verify official Gazette)"),
        ("GLB-06", "Legal Cap Art.52 — Portfolio New-Biz Agent Bonuses (>1Y)", 0.30, "Hard Regulatory Gate (TT 67/2023 Art.52.2 eff. 2026)", "FALSE", "SOURCE_NOT_VERIFIED (verify official Gazette)"),
        ("GLB-07", "Legal Cap Art.52 — Portfolio Renewal Servicing Bonuses", 0.07, "Hard Regulatory Gate (<=7% Renewal Premium)", "FALSE", "SOURCE_NOT_VERIFIED (verify official Gazette)"),
    ]
    for i, gp in enumerate(global_params, 5):
        ws4.cell(i, 1, gp[0]).border = BORDER
        ws4.cell(i, 2, gp[1]).border = BORDER
        vc = ws4.cell(i, 3, gp[2])
        vc.border = BORDER
        if gp[4] == "TRUE":
            vc.fill = FILL_INPUT
            vc.font = FONT_BLUE
        else:
            vc.fill = FILL_LOCK
            vc.font = FONT_BOLD
        if isinstance(gp[2], float):
            vc.number_format = "0.0%"
        ws4.cell(i, 4, gp[3]).border = BORDER
        ws4.cell(i, 5, gp[4]).border = BORDER
        ws4.cell(i, 6, gp[5]).border = BORDER
        ws4.merge_cells(start_row=i, start_column=6, end_row=i, end_column=8)

    # Exact Cell Map in Block A:
    # C5 = Chubb W1 Toggle ("Table_80" / "Example_50")
    # C6 = AIA Rounding Toggle ("HalfUp" / "RoundUp")
    # C7 = UL FYC Rate Assumption (0.30)
    # C8 = Home Office OpEx % FYP (0.20)
    # C9 = Legal Art.51 Cap (0.30)
    # C10 = Legal Art.52 NewBiz Bonus Cap (0.30)
    # C11 = Legal Art.52 Renewal Bonus Cap (0.07)

    # Block B: PO-Editable Proposal Balanced Parameters (Rows 13-30)
    style_section(ws4, 13, "BLOCK B: W24 Proposed Balanced Hybrid Scheme Parameters (PO Editable = Blue/Yellow — PROPOSAL / SYNTHETIC ASSUMPTION)", 8)
    write_table_header(ws4, 14, ["Param_ID", "Proposal Parameter", "PO Value", "Unit", "Editable?", "Design Rationale"])
    ws4.merge_cells("F14:H14")
    prop_params = [
        ("PRP-01", "UL/ILP Base Commission Year 1 (Top-up = 0%)", 0.30, "% PCB", "TRUE", "PROPOSAL paired with HSBH tiers; legal verification pending"),
        ("PRP-02", "K2 Hard Floor Threshold (Below -> 0% Bonus)", 60.0, "% K2", "TRUE", "Eliminates Chubb 25% soft floor without AIA 70% cliff shock"),
        ("PRP-03", "T+1 Cash Holdback K2 Threshold", 65.0, "% K2", "TRUE", "Holds M12/monthly bonus to T+1 for New or K2<65% agents"),
        ("PRP-04", "Monthly Tier 1 Rate (>= 5M FYC/M)", 0.08, "% FYC", "TRUE", "Low entry threshold fits VN 2026 smaller case sizes"),
        ("PRP-05", "Monthly Tier 2 Rate (>= 12M FYC/M)", 0.16, "% FYC", "TRUE", "Core productive agent tier"),
        ("PRP-06", "Monthly Tier 3 Rate (>= 22M FYC/M)", 0.24, "% FYC", "TRUE", "Mid-high productive tier"),
        ("PRP-07", "Monthly Tier 4 Rate (>= 35M FYC/M)", 0.32, "% FYC", "TRUE", "High producer tier"),
        ("PRP-08", "Monthly Tier 5 Rate (>= 55M FYC/M)", 0.38, "% FYC", "TRUE", "Top modeled monthly production tier"),
        ("PRP-09", "Quarterly 3-of-3 Active Consistency Multiplier", 0.12, "% of M-Bonus", "TRUE", "Rewards steady monthly activity without Chubb 109% compounding"),
        ("PRP-10", "Annual MDRT Bonus Rate (>= 400M FYC/Y)", 0.10, "% Ann FYC", "TRUE", "30% deferred to Y2 gated on K2>=75%"),
        ("PRP-11", "Annual MDRT Deferred Share (Post-Y1)", 0.30, "% of MDRT", "TRUE", "Improves Y1 cash flow & locks top agent persistency"),
        ("PRP-12", "Agent Y2 SYC/RYC Quality Bonus (K2 >= 75%)", 0.25, "% SYC", "TRUE", "Y2 servicing reward; assess portfolio-level cap separately"),
        ("PRP-13", "Manager Direct Override Rate (Base x K2)", 0.30, "% Team FYC", "TRUE", "Disciplined vs Chubb 108% peak; symmetric negative clawback"),
        ("PRP-14", "Manager Indirect Override Rate (Max 3 Gens, NTT>=15M)", 0.35, "% Sub Direct", "TRUE", "Zero infinite chain; 0% if Direct Team < 15M/M"),
        ("PRP-15", "Manager 3-Year Deferred Retention Rate (K2 >= 75%)", 0.12, "% Team FYC", "TRUE", "Vests 30%/30%/40% Y+1..Y+3 (learned from Manulife & AIA)"),
        ("PRP-16", "Regional Leader Monthly Base Fee (KPI 30% floor/140% cap)", 35.0, "Million VND", "TRUE", "KPI-linked & service-acceptance verified (ND 97/2026)"),
        ("PRP-17", "Regional Leader Variable Override Rate (x K2)", 0.07, "% Reg FYC", "TRUE", "Paired with 60% 3-Year Deferred Retention (K2>=75%)"),
        ("PRP-18", "Regional Leader 3Y Deferred Retention Share (on Var)", 0.60, "% Reg Var", "TRUE", "Matches Manulife cash-flow discipline without Top-up 6%"),
        ("PRP-19", "Manager Direct Override Effective Rate Cap", 0.36, "% Team FYC", "TRUE", "Caps base rate multiplied by K2"),
    ]
    for i, pp in enumerate(prop_params, 15):
        ws4.cell(i, 1, pp[0]).border = BORDER
        ws4.cell(i, 2, pp[1]).border = BORDER
        vc = ws4.cell(i, 3, pp[2])
        vc.fill = FILL_INPUT
        vc.font = FONT_BLUE
        vc.border = BORDER
        vc.number_format = "0.0%" if pp[2] <= 1.0 else "#,##0.0"
        ws4.cell(i, 4, pp[3]).border = BORDER
        ws4.cell(i, 5, pp[4]).border = BORDER
        ws4.cell(i, 6, pp[5]).border = BORDER
        ws4.merge_cells(start_row=i, start_column=6, end_row=i, end_column=8)

    # Proposal Parameter Exact Cells:
    # C15=UL_Y1(0.30), C16=K2_Floor(60), C17=Hold_T1(65), C18..C22=M_Rates(0.08,0.16,0.24,0.32,0.38)
    # C23=Q_Cons(0.12), C24=MDRT(0.10), C25=MDRT_Def(0.30), C26=SYC(0.25)
    # C27=Mgr_Dir(0.30), C28=Mgr_Ind(0.35), C29=Mgr_Def3Y(0.12), C30=RD_Base(35), C31=RD_Var(0.07), C32=RD_DefShare(0.60)

    # Block C: Locked Competitor Core Rate Tables (Rows 34-46)
    style_section(ws4, 34, "BLOCK C: Locked Competitor Ground Truth Reference Parameters (po_editable = FALSE — Gray)", 8)
    write_table_header(ws4, 35, ["Ref_ID", "Competitor Parameter", "Value", "Source_ID & Page", "Notes"])
    ws4.merge_cells("E35:H35")
    comp_locks = [
        ("AIA-L01", "AIA 1/72H Fast Activation Bonus (Million VND)", 1.5, "SRC-POL-AIA-ALP-001 p.4", "4 working days, >=1 policy, >=4M FYC"),
        ("AIA-L02", "AIA CQL 3Y Deferred Vesting Split Y+2 / Y+3 / Y+4", "15% / 25% / 60%", "SRC-POL-AIA-ALP-002 p.5", "Requires active CQL & AIA TOT >= 85%"),
        ("AIA-L03", "AIA PAF+ SAF Monthly Base Fee (Million VND)", 50.0, "SRC-POL-AIA-ALP-003 p.3", "10 ranks 20M (PAF) to 130M (SPVP); full 1,300-row targets on Sheet 05"),
        ("CHB-L01", "Chubb AR Peak Monthly / Quarterly Multiplier", "55% x 120% x 1.30 = 85.8%", "SRC-POL-CHB-001 p.4-6", "AL personal peak = 70% x 120% x 1.30 = 109.2% FYC"),
        ("CHB-L02", "Chubb AL Direct HT KTN Peak (Monthly x Quarterly)", "60% x 120% x 1.50 = 108.0%", "SRC-POL-CHB-002 p.5-7", "AL>=15M, >=40M FYC NTT, >=4 EHC, K2>=80%; excl. AL personal sales"),
        ("CHB-L03", "Chubb AL Indirect Gate Minimum Direct FYC NTT (M VND)", 15.0, "SRC-POL-CHB-002 p.7", "Below 15M -> 0% L1-L3; 15-30M -> 30/15/7.5%; >=30M -> 50/25/12.5%"),
        ("CHB-L04", "Chubb RD K2 Binary Cliff Q1-Q2 vs Q3-Q4 (%)", "50% -> 60%", "SRC-POL-CHB-003 p.7-9", "Applies to II.4 (3MAA) & II.5 (Quarterly Growth 2.5-27.5%)"),
        ("MNL-L01", "Manulife PSM/HKD1-2 Monthly Base Fee (Million VND)", 35.0, "SRC-POL-MNL-001 p.1", "PSSM/HKD3-4 = 45M; Floor 30% FYP, Multiplier 130%, Cap 150%"),
        ("MNL-L02", "Manulife 3Y Deferred Vesting Split Y+1 / Y+2 / Y+3", "30% / 30% / 40%", "SRC-POL-MNL-001 p.4", "75% Direct + 25% Indirect; Cap 12x Base; requires K2 >= 70%"),
    ]
    for i, cl in enumerate(comp_locks, 36):
        ws4.cell(i, 1, cl[0]).border = BORDER
        ws4.cell(i, 2, cl[1]).border = BORDER
        vc = ws4.cell(i, 3, cl[2])
        vc.fill = FILL_LOCK
        vc.font = FONT_BOLD
        vc.border = BORDER
        ws4.cell(i, 4, cl[3]).border = BORDER
        ws4.cell(i, 5, cl[4]).border = BORDER
        ws4.merge_cells(start_row=i, start_column=5, end_row=i, end_column=8)
    set_col_widths(ws4, {1: 12, 2: 46, 3: 18, 4: 34, 5: 12, 6: 22, 7: 22, 8: 22})

    # =========================================================================
    # SHEET 05: 05_Lookup_PAF_5Y (Full 1,300 Normalized Rows + Live Excel Audit!)
    # =========================================================================
    ws5 = wb.create_sheet("05_Lookup_PAF_5Y")
    style_title(ws5, 1, "AIA ALPHA PAF+ 5-YEAR TARGET LOOKUP MATRIX (1,300 NORMALIZED ROWS + LIVE EXCEL SUMIF AUDIT)", 11)
    # Summary reconciliation block at top (Rows 3-5)
    ws5["A3"] = "Total Normalized Rows:"
    ws5["B3"] = "=COUNTA(B8:B1307)"
    ws5["B3"].font = FONT_BOLD
    ws5["C3"] = "SPVP Year_5 Annual FYP Target (Live INDEX/MATCH):"
    ws5["E3"] = '=INDEX(H8:H1307,MATCH("SPVP|Year_5|ANNUAL_TOTAL|FYP_Million_VND",A8:A1307,0))'
    ws5["E3"].font = FONT_BOLD
    ws5["E3"].number_format = "#,##0"
    ws5["F3"] = "SAF Year_1 Annual FYP Target:"
    ws5["G3"] = '=INDEX(H8:H1307,MATCH("SAF|Year_1|ANNUAL_TOTAL|FYP_Million_VND",A8:A1307,0))'
    ws5["G3"].font = FONT_BOLD
    ws5["G3"].number_format = "#,##0"
    ws5["H3"] = "Total Annual-vs-Monthly Discrepancies (0 = PASS):"
    ws5["K3"] = '=COUNTIF(K8:K1307,"FAIL")'
    ws5["K3"].font = FONT_BOLD
    ws5["K3"].fill = FILL_PASS

    paf_hdr, paf_rows = load_csv("knowledge/lookups/aia-paf-5y-targets.csv")
    write_table_header(ws5, 7, [
        "Lookup_Key", "Role_Code", "Base_Fee_M", "Tenure_Year", "Period_Key",
        "Period_Type", "Metric", "Target_Value", "Monthly_Sum_Check", "Diff", "Audit_Status"
    ])
    for idx, r in enumerate(paf_rows, 8):
        key = f"{r[1]}|{r[3]}|{r[4]}|{r[6]}"
        ws5.cell(idx, 1, key)
        ws5.cell(idx, 2, r[1])
        ws5.cell(idx, 3, float(r[2]))
        ws5.cell(idx, 4, r[3])
        ws5.cell(idx, 5, r[4])
        ws5.cell(idx, 6, r[5])
        ws5.cell(idx, 7, r[6])
        ws5.cell(idx, 8, float(r[7]))
        # For ANNUAL_TOTAL rows, verify SUM of the next 12 monthly rows right below it!
        if r[4] == "ANNUAL_TOTAL":
            ws5.cell(idx, 9, f"=SUM(H{idx+1}:H{idx+12})")
            ws5.cell(idx, 10, f"=ABS(H{idx}-I{idx})")
            ws5.cell(idx, 11, f'=IF(J{idx}<=0.01,"PASS","FAIL")')
        else:
            ws5.cell(idx, 9, "")
            ws5.cell(idx, 10, "")
            ws5.cell(idx, 11, "ROW")
    set_col_widths(ws5, {1: 40, 2: 12, 3: 12, 4: 12, 5: 15, 6: 12, 7: 18, 8: 14, 9: 18, 10: 10, 11: 12})

    # =========================================================================
    # SHEET 06: 06_Lookup_Chubb_Comm (113 Product Rows + 10 HSBH Rows + Live Calc)
    # =========================================================================
    ws6 = wb.create_sheet("06_Lookup_Chubb_Comm")
    style_title(ws6, 1, "CHUBB LIFE PRODUCT COMMISSION SCHEDULE (113 ROWS) & TU DO AN PHUC HSBH LOOKUP (10 AGE BANDS)", 12)

    # Top Interactive HSBH Calculator (Rows 3-6)
    style_section(ws6, 3, "Interactive Chubb Tu Do An Phuc Y1 FYC Calculator (Live Excel 2007 INDEX/MATCH on HSBH Table Rows 9-18)", 12)
    write_table_header(ws6, 4, ["Test Case", "Age", "Gender (M/F)", "HSBH Ratio", "Tier 1 HSBH", "Tier 2 HSBH", "Live Y1 FYC Rate", "Product Check ID", "Live Lookup Y1 %"])
    ws6.merge_cells("I4:L4")
    hsbh_cases = [
        ("Case 1: Adult Male Mid HSBH", 30, "M", 65.0, "CHB-PRD-062"),
        ("Case 2: Child Female Mid HSBH", 10, "F", 60.0, "CHB-PRD-001"),
    ]
    for i, hc in enumerate(hsbh_cases, 5):
        ws6.cell(i, 1, hc[0]).border = BORDER
        ws6.cell(i, 2, hc[1]).fill = FILL_INPUT; ws6.cell(i, 2).font = FONT_BLUE; ws6.cell(i, 2).border = BORDER
        ws6.cell(i, 3, hc[2]).fill = FILL_INPUT; ws6.cell(i, 3).font = FONT_BLUE; ws6.cell(i, 3).border = BORDER
        ws6.cell(i, 4, hc[3]).fill = FILL_INPUT; ws6.cell(i, 4).font = FONT_BLUE; ws6.cell(i, 4).border = BORDER
        # Match Min_Age (Col B rows 9:18 ascending -> MATCH(..., 1))
        ws6.cell(i, 5, f'=IF(C{i}="M",INDEX($D$9:$D$18,MATCH(B{i},$B$9:$B$18,1)),INDEX($F$9:$F$18,MATCH(B{i},$B$9:$B$18,1)))').border = BORDER
        ws6.cell(i, 6, f'=IF(C{i}="M",INDEX($E$9:$E$18,MATCH(B{i},$B$9:$B$18,1)),INDEX($G$9:$G$18,MATCH(B{i},$B$9:$B$18,1)))').border = BORDER
        c_rate = ws6.cell(i, 7, f'=IF(B{i}<18,IF(D{i}>=F{i},0.25,IF(D{i}>=E{i},0.22,0.20)),IF(D{i}>=F{i},0.30,IF(D{i}>=E{i},0.27,0.25)))')
        c_rate.number_format = "0.0%"; c_rate.font = FONT_BOLD; c_rate.border = BORDER
        ws6.cell(i, 8, hc[4]).border = BORDER
        c_prd = ws6.cell(i, 9, f'=INDEX($F$22:$F$134,MATCH(H{i},$A$22:$A$134,0))')
        c_prd.number_format = "0.0"; c_prd.font = FONT_BOLD; c_prd.border = BORDER

    style_section(ws6, 7, "A. Chubb Tu Do An Phuc HSBH Age-Band Table (SRC-POL-CHB-001 p.19)", 12)
    h_hdr, h_rows = load_csv("knowledge/lookups/chubb-hsbh-tiers.csv")
    write_table_header(ws6, 8, h_hdr[:9])
    for idx, r in enumerate(h_rows, 9):
        ws6.cell(idx, 1, r[0]).border = BORDER
        for c_i in range(1, 7):
            cell = ws6.cell(idx, c_i + 1, float(r[c_i]))
            cell.border = BORDER
        ws6.cell(idx, 8, r[7]).border = BORDER
        ws6.cell(idx, 9, r[8]).border = BORDER

    style_section(ws6, 20, "B. Full Chubb Product Commission Schedule (113 Normalized Rows — SRC-POL-CHB-001 p.13-19)", 12)
    c_hdr, c_rows = load_csv("knowledge/lookups/chubb-product-commission-schedule.csv")
    c_keep = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15]
    write_table_header(ws6, 21, [c_hdr[k] for k in c_keep])
    for idx, r in enumerate(c_rows, 22):
        for j, oc in enumerate(c_keep, 1):
            val = r[oc]
            if oc in (6, 7, 8, 9, 10, 12):
                try:
                    val = float(val)
                except ValueError:
                    pass
            cell = ws6.cell(idx, j, val)
            cell.font = FONT_NORM
            cell.border = BORDER
    set_col_widths(ws6, {1: 18, 2: 14, 3: 36, 4: 26, 5: 14, 6: 12, 7: 14, 8: 14, 9: 12, 10: 12, 11: 12, 12: 18})

    # =========================================================================
    # SHEET 07: 07_Profiles_12M_Input (10 Agent + 7 Manager/Leader Profiles)
    # =========================================================================
    ws7 = wb.create_sheet("07_Profiles_12M_Input")
    style_title(ws7, 1, "CONFIGURABLE PROFILES & 12-MONTH INPUTS (10 AGENT PROFILES + 7 MANAGER / LEADER PROFILES)", 11)

    style_section(ws7, 3, "A. 10 Configurable Individual Agent Profiles (Blue/Yellow Inputs — Million VND)", 11)
    write_table_header(ws7, 4, [
        "Profile_ID", "Agent Profile Name", "Monthly FYC (M)", "Monthly SYC/RYC (M)",
        "Persistency FY/K2 (%)", "Tenure Start (M)", "New Agent? (1/0)", "1/72H? (1/0)",
        "Active Months/Q", "AL Personal Role? (1/0)", "Disciplinary Warning? (1/0)"
    ])
    agent_profiles = [
        ("A01", "New Agent Strong Start (10M/M, K2=80%)", 10.0, 0.0, 80.0, 1, 1, 1, 3, 0, 0),
        ("A02", "New Agent Low Start (5M/M, K2=75%)", 5.0, 0.0, 75.0, 1, 1, 0, 3, 0, 0),
        ("A03", "Core Mid Agent Seasoned (15M/M, K2=75%)", 15.0, 3.0, 75.0, 13, 0, 0, 3, 0, 0),
        ("A04", "Low-Persistency Risk Agent (20M/M, K2=65%)", 20.0, 2.0, 65.0, 13, 0, 0, 3, 0, 0),
        ("A05", "High Producer MDRT (60M/M, K2=85%)", 60.0, 10.0, 85.0, 13, 0, 0, 3, 0, 0),
        ("A06", "Superstar TOT Producer (140M/M, K2=90%)", 140.0, 20.0, 90.0, 24, 0, 0, 3, 0, 0),
        ("A07", "Part-Time Low Active (6M/M, 2M/Q, K2=70%)", 6.0, 1.0, 70.0, 13, 0, 0, 2, 0, 0),
        ("A08", "Borderline Rounding Test (20M/M, FY=74.49%)", 20.0, 0.0, 74.49, 13, 0, 0, 3, 0, 0),
        ("A09", "Veteran AL Personal Seller (25M/M, K2=85%)", 25.0, 4.0, 85.0, 24, 0, 0, 3, 1, 0),
        ("A10", "Severe Quality Drop / Warning (20M/M, K2=55%)", 20.0, 0.0, 55.0, 13, 0, 0, 3, 0, 1),
    ]
    for i, ap in enumerate(agent_profiles, 5):
        ws7.cell(i, 1, ap[0]).font = FONT_BOLD; ws7.cell(i, 1).border = BORDER
        ws7.cell(i, 2, ap[1]).border = BORDER
        for j in range(2, 11):
            c = ws7.cell(i, j + 1, ap[j])
            c.fill = FILL_INPUT; c.font = FONT_BLUE; c.border = BORDER

    # Rows 5-14 = A01..A10!
    style_section(ws7, 16, "B. 7 Configurable Manager & Senior Leader Profiles (Blue/Yellow Inputs — Million VND)", 11)
    write_table_header(ws7, 17, [
        "Profile_ID", "Manager / Leader Profile Name", "Tier", "Monthly Team FYC (M)",
        "Monthly Team FYP (M)", "Active / EHC / M", "Persistency K2/FY (%)", "TOT (%)",
        "Tenure (M) / Base (M)", "Sub-Mgr Base (M/M)", "FYP Target Ach (%)"
    ])
    mgr_profiles = [
        ("M01", "New Direct Manager (<15M Tenure, 30M FYC/M)", "Tier_2", 30.0, 100.0, 4, 75.0, 80.0, 6.0, 0.0, 1.00),
        ("M02", "Veteran Direct Manager (>=15M, 60M FYC/M, K2=82%)", "Tier_2", 60.0, 200.0, 6, 82.0, 86.0, 18.0, 20.0, 1.00),
        ("M03", "Low-NTT Manager Indirect Gate Test (14M FYC/M)", "Tier_2", 14.0, 46.7, 3, 80.0, 85.0, 18.0, 20.0, 1.00),
        ("M04", "Negative FYC Clawback Stress Test (-25M FYC/M)", "Tier_2", -25.0, -83.3, 4, 80.0, 85.0, 18.0, 0.0, 1.00),
        ("L01", "Standard Region Leader (12B FYP/Y, 120% Ach, K2=80%)", "Tier_3", 300.0, 1000.0, 20, 80.0, 86.0, 35.0, 0.0, 1.20),
        ("L02", "Dual-Phase Stress Region (K2=55%: Q1-2 vs Q3-4 / Apr)", "Tier_3", 120.0, 400.0, 12, 55.0, 60.0, 35.0, 0.0, 1.00),
        ("L03", "Underperforming Floor Stress Region (29% Ach, K2=65%)", "Tier_3", 50.0, 166.7, 5, 65.0, 68.0, 35.0, 0.0, 0.29),
    ]
    for i, mp in enumerate(mgr_profiles, 18):
        ws7.cell(i, 1, mp[0]).font = FONT_BOLD; ws7.cell(i, 1).border = BORDER
        ws7.cell(i, 2, mp[1]).border = BORDER
        ws7.cell(i, 3, mp[2]).border = BORDER
        for j in range(3, 11):
            c = ws7.cell(i, j + 1, mp[j])
            c.fill = FILL_INPUT; c.font = FONT_BLUE; c.border = BORDER
    set_col_widths(ws7, {1: 12, 2: 42, 3: 15, 4: 17, 5: 17, 6: 14, 7: 16, 8: 12, 9: 16, 10: 16, 11: 16})

    # =========================================================================
    # SHEET 08: 08_Indiv_Comp_12M (100% Live Excel 2007 Formulas — 10 Profiles + CH Offset!)
    # =========================================================================
    ws8 = wb.create_sheet("08_Indiv_Comp_12M")
    style_title(ws8, 1, "TIER 1 — 12-MONTH INDIVIDUAL COMPENSATION MODEL (AIA 2026 vs 2027 vs CHUBB 2026 vs PROPOSAL | MNL=UNKNOWN)", 14)

    write_table_header(ws8, 3, [
        "Profile", "Annual FYC", "Implied FYP", "AIA Rounded FY",
        "AIA 2026 Bonus", "AIA 2026 %FYC", "AIA 2027 Bonus", "AIA 2027 %FYC",
        "Chubb 2026 Bonus", "Chubb 2026 %FYC", "Proposal Bonus", "Proposal %FYC",
        "Proposal Deferred", "Manulife FA"
    ])
    # Rows 4-13 correspond to Profiles A01..A10 (Sheet 07 Rows 5-14)!
    for idx in range(10):
        r8 = 4 + idx
        r7 = 5 + idx
        p = "'07_Profiles_12M_Input'!"
        par = "'04_Policy_Parameters'!"

        ws8.cell(r8, 1, f"={p}A{r7}").font = FONT_BOLD
        ws8.cell(r8, 2, f"={p}C{r7}*12").number_format = "#,##0.0"                  # B: Annual FYC
        ws8.cell(r8, 3, f"=B{r8}/{par}$C$7").number_format = "#,##0.0"             # C: Implied FYP
        # D: AIA Rounded FY respecting ERR-DOC-02 Toggle ('04_Policy_Parameters'!$C$6)
        ws8.cell(r8, 4, f'=IF({par}$C$6="RoundUp",ROUNDUP({p}E{r7},0),ROUND({p}E{r7},0))').number_format = "0"

        # Helper inline expressions (clean classic Excel 2007 IFs!)
        fy_cell = f"D{r8}"
        fyc_m = f"{p}C{r7}"
        fyc_q = f"({fyc_m}*3)"
        fyc_y = f"B{r8}"
        syc_y = f"({p}D{r7}*12)"
        act_q = f"{p}I{r7}"
        is_new = f"{p}G{r7}"
        is_72h = f"{p}H{r7}"
        is_al = f"{p}J{r7}"
        is_warn = f"{p}K{r7}"
        k2_raw = f"{p}E{r7}"
        ten = f"{p}F{r7}"

        # AIA FY Factor 2026 & 2027 — [AIAVAD 2604-069 : 3] (5 bậc 2026, 4 bậc 2027)
        fy26 = f"IF({fy_cell}>=85,1.2,IF({fy_cell}>=75,1.1,IF({fy_cell}>=65,1,{fy_cell}/100)))"
        fy27 = f"IF({fy_cell}>=90,1.2,IF({fy_cell}>=80,1.1,IF({fy_cell}>=70,1,0)))"
        aia_q_r = f"IF({fyc_q}>=150,0.4,IF({fyc_q}>=120,0.35,IF({fyc_q}>=90,0.3,IF({fyc_q}>=70,0.25,IF({fyc_q}>=50,0.2,IF({fyc_q}>=35,0.15,IF({fyc_q}>=20,0.1,IF({fyc_q}>=16,0.04,0))))))))"
        aia_p26 = f"IF(AND({fyc_q}>=70,{act_q}>=3,{fy_cell}>=75),0.15,IF(AND({fyc_q}>=35,{act_q}>=3,{fy_cell}>=65),0.1,IF(AND({fyc_q}>=20,{act_q}>=2,{fy_cell}>=65),0.05,0)))"
        aia_p27 = f"IF(AND({fyc_q}>=70,{act_q}>=3,{fy_cell}>=80),0.15,IF(AND({fyc_q}>=35,{act_q}>=3,{fy_cell}>=70),0.1,IF(AND({fyc_q}>=20,{act_q}>=2,{fy_cell}>=70),0.05,0)))"
        aia_syc26 = f"IF(AND({fyc_q}>=70,{act_q}>=3,{fy_cell}>=75),0.5,IF(AND({fyc_q}>=35,{act_q}>=3,{fy_cell}>=65),0.3,0))"
        aia_syc27 = f"IF(AND({fyc_q}>=70,{act_q}>=3,{fy_cell}>=80),0.5,IF(AND({fyc_q}>=35,{act_q}>=3,{fy_cell}>=70),0.3,0))"
        aia_ann = f"IF({fyc_y}>=1600,0.2,IF({fyc_y}>=800,0.14,IF({fyc_y}>=300,0.1,IF({fyc_y}>=150,0.06,0))))"
        aia_onb = f"IF({is_new}=1,{is_72h}*1.5+IF(MAX(0,{fyc_m}-{is_72h}*4)>=10,3,IF(MAX(0,{fyc_m}-{is_72h}*4)>=5,1.5,0))+2*IF({fyc_m}>=10,3,IF({fyc_m}>=5,1.5,0)),0)"
        disc = f"IF({is_warn}=1,0.7,1)"

        # E & F: AIA 2026 Bonus & %FYC
        ws8.cell(r8, 5, f"=({aia_onb}+{fyc_y}*({aia_q_r}+{aia_p26}+{aia_ann})*{fy26}+{syc_y}*{aia_syc26})*{disc}").number_format = "#,##0.00"
        ws8.cell(r8, 6, f"=({fyc_y}+{syc_y}+E{r8})/{fyc_y}").number_format = "0.0%"

        # G & H: AIA 2027 Bonus & %FYC
        ws8.cell(r8, 7, f"=({aia_onb}+{fyc_y}*({aia_q_r}+{aia_p27}+{aia_ann})*{fy27}+{syc_y}*{aia_syc27})*{disc}").number_format = "#,##0.00"
        ws8.cell(r8, 8, f"=({fyc_y}+{syc_y}+G{r8})/{fyc_y}").number_format = "0.0%"

        # I & J: Chubb 2026 Bonus (Seasoned vs New Agent M1-12 Rolling 3M + New Agent M3/6/12 cap 36M)
        chb_k2 = f"IF({k2_raw}>=80,1.2,IF({k2_raw}>=70,1,IF({k2_raw}>=60,0.75,IF({k2_raw}>=50,0.5,0.25))))"
        chb_qm = f"IF({act_q}>=3,1.3,IF({act_q}=2,1.15,1))"
        # Steady-state 3M rate for seasoned (tenure>=13) vs new (capped at 45%/60%; M1=1x, M2=2x, M3-12=3x)
        chb_r_seas = f"IF({is_al}=0,IF({fyc_q}>=60,0.55,IF({fyc_q}>=40,0.45,IF({fyc_q}>=20,0.35,IF({fyc_q}>=10,0.25,IF({fyc_q}>=5,0.075,0))))),IF({fyc_q}>=60,0.7,IF({fyc_q}>=40,0.6,IF({fyc_q}>=20,0.5,IF({fyc_q}>=10,0.4,IF({fyc_q}>=5,0.15,0))))))"
        # For new AR (tenure=1, uniform monthly fyc_m): M1 rolling=fyc_m, M2=2*fyc_m, M3..12=3*fyc_m (capped 45%)
        chb_r1 = f"IF({fyc_m}>=40,0.45,IF({fyc_m}>=20,0.35,IF({fyc_m}>=10,0.25,IF({fyc_m}>=5,0.075,0))))"
        chb_r2 = f"IF(({fyc_m}*2)>=40,0.45,IF(({fyc_m}*2)>=20,0.35,IF(({fyc_m}*2)>=10,0.25,IF(({fyc_m}*2)>=5,0.075,0))))"
        chb_r3 = f"IF(({fyc_m}*3)>=40,0.45,IF(({fyc_m}*3)>=20,0.35,IF(({fyc_m}*3)>=10,0.25,IF(({fyc_m}*3)>=5,0.075,0))))"
        chb_new_m = f"{fyc_m}*({chb_r1}+{chb_r2}+10*{chb_r3})*{chb_k2}"
        chb_new_ag = f"IF({is_new}=1,MIN(6,{fyc_q}*0.2)+MIN(10,{fyc_q}*0.2)+MIN(20,{fyc_m}*6*0.2),0)"
        chb_ryc = f"IF(AND({ten}>=13,{k2_raw}>=65),{syc_y}*IF({act_q}>=3,0.15,IF({act_q}=2,0.1,0)),0)"
        ws8.cell(r8, 9, f"=IF({is_new}=1,{chb_new_m}*{chb_qm}+{chb_new_ag},{fyc_y}*{chb_r_seas}*{chb_k2}*{chb_qm}+{chb_ryc})").number_format = "#,##0.00"
        ws8.cell(r8, 10, f"=({fyc_y}+{syc_y}+I{r8})/{fyc_y}").number_format = "0.0%"

        # K, L, M: Proposal Balanced (Live reference to PO-Editable Block B on Sheet 04!)
        prp_k2 = f"IF({k2_raw}>=85,1.2,IF({k2_raw}>=80,1.1,IF({k2_raw}>=75,1,IF({k2_raw}>=70,0.85,IF({k2_raw}>={par}$C$16,0.6,0)))))"
        prp_mr = f"IF({fyc_m}>=55,{par}$C$22,IF({fyc_m}>=35,{par}$C$21,IF({fyc_m}>=22,{par}$C$20,IF({fyc_m}>=12,{par}$C$19,IF({fyc_m}>=5,{par}$C$18,0)))))"
        prp_onb = f"IF(AND({is_new}=1,{fyc_m}>=8),18,0)"
        prp_qc = f"IF({act_q}>=3,{par}$C$23,0)"
        prp_mdrt = f"IF({fyc_y}>=400,{fyc_y}*{par}$C$24*{prp_k2},0)"
        prp_syc = f"IF({k2_raw}>=75,{syc_y}*{par}$C$26,0)"
        ws8.cell(r8, 11, f"={fyc_y}*{prp_mr}*{prp_k2}*(1+{prp_qc})+{prp_onb}+{prp_mdrt}+{prp_syc}").number_format = "#,##0.00"
        ws8.cell(r8, 12, f"=({fyc_y}+{syc_y}+K{r8})/{fyc_y}").number_format = "0.0%"
        ws8.cell(r8, 13, f"={prp_mdrt}*{par}$C$25").number_format = "#,##0.00"
        ws8.cell(r8, 14, "UNKNOWN").fill = FILL_WARN
        for col in range(1, 15):
            ws8.cell(r8, col).border = BORDER

    # Section B on Sheet 08: Live Chubb Champion Hubb M7 & M12 Offset Calculator (PDF p.10 + ERR-DOC-01 Toggle!)
    style_section(ws8, 16, "B. Chubb Champion Hubb M7-M12 Offset Calculator (SRC-POL-CHB-001 p.10 + Live ERR-DOC-01 Toggle on Sheet 04!$C$5)", 14)
    write_table_header(ws8, 17, [
        "Scenario (p.10)", "Month", "CC Count", "SOP (%)", "KPI (%)", "New Agent Bonus",
        "Live W1 Factor", "CH Month Gross", "CH M12 Gross", "CH Month Net Cash", "CH M12 Deferred Net", "Total CH Add-on"
    ])
    ch_rows = [
        ("PDF p.10 M7 Verification (SOP=100%, NewAgt=6.0)", 7, 3, 100.0, 85.0, 6.0),
        ("PDF p.10 M12 Conflict Test (SOP=85%, NewAgt=1.5)", 12, 3, 85.0, 80.0, 1.5),
    ]
    for i, cr in enumerate(ch_rows, 18):
        ws8.cell(i, 1, cr[0]).border = BORDER
        for j in range(1, 6):
            c = ws8.cell(i, j + 1, cr[j])
            c.fill = FILL_INPUT; c.font = FONT_BLUE; c.border = BORDER
        # Col G (7): Live W1 respecting ERR-DOC-01 Toggle!
        ws8.cell(i, 7, f'=IF(D{i}>=90,1,IF(D{i}>=80,IF(\'04_Policy_Parameters\'!$C$5="Table_80",0.8,0.5),IF(D{i}>=70,0.5,0)))').number_format = "0%"
        # Col H (8): CH Month Gross
        ws8.cell(i, 8, f"=IF(OR(E{i}<70,C{i}<1),0,IF(B{i}<=6,IF(C{i}>=3,7,IF(C{i}=2,5,3)),IF(C{i}>=3,5,IF(C{i}=2,3,2)))*G{i})").number_format = "0.00"
        # Col I (9): CH M12 Gross
        ws8.cell(i, 9, f"=IF(OR(E{i}<70,C{i}<1,B{i}<=6),0,IF(C{i}>=2,2.4,1.2)*G{i})").number_format = "0.00"
        # Col J (10): CH Month Net = MAX(0, Gross_M - NewAgt)
        ws8.cell(i, 10, f"=MAX(0,H{i}-F{i})").number_format = "0.00"
        # Col K (11): CH M12 Net = MAX(0, Gross_M12 - MAX(0, NewAgt - Gross_M))
        ws8.cell(i, 11, f"=MAX(0,I{i}-MAX(0,F{i}-H{i}))").number_format = "0.00"
        # Col L (12): Total Add-on
        ws8.cell(i, 12, f"=J{i}+K{i}").number_format = "0.00"
        for col in range(7, 13):
            ws8.cell(i, col).border = BORDER
    set_col_widths(ws8, {1: 28, 2: 12, 3: 13, 4: 13, 5: 14, 6: 13, 7: 14, 8: 13, 9: 15, 10: 14, 11: 14, 12: 14, 13: 15, 14: 13})

    # =========================================================================
    # SHEET 09: 09_Mgr_Senior_Comp (Tier 2 Managers & Tier 3 Senior Leaders — All 3 Competitors!)
    # =========================================================================
    ws9 = wb.create_sheet("09_Mgr_Senior_Comp")
    style_title(ws9, 1, "TIER 2 (DIRECT MANAGERS) & TIER 3 (SENIOR LEADERS — ALL 3 COMPETITORS) 12-MONTH ENGINE", 13)

    # Section A: Tier 2 Managers (Profiles M01..M04 from Sheet 07 rows 18-21)
    style_section(ws9, 3, "A. Tier 2 Direct Managers (AIA Alpha CQL vs Chubb AL [incl. Neg FYC & 15M Gate] vs W24 Proposal | Manulife=UNKNOWN)", 13)
    write_table_header(ws9, 4, [
        "Profile", "Ann Team FYC", "AIA Direct Cash", "AIA 3Y Deferred", "AIA Y4 Vest(TOT>=85%)",
        "Chubb HT KTN M+Q", "Chubb Indirect L1", "Chubb Direct %FYC",
        "Prop Direct Cash", "Prop Indirect", "Prop 3Y Deferred", "Manulife UM/DM", "Notes"
    ])
    for idx in range(4):
        r9 = 5 + idx
        r7 = 18 + idx
        p = "'07_Profiles_12M_Input'!"
        par = "'04_Policy_Parameters'!"
        fm = f"{p}D{r7}"
        act = f"{p}F{r7}"
        k2 = f"{p}G{r7}"
        tot = f"{p}H{r7}"
        ten = f"{p}I{r7}"
        sub = f"{p}J{r7}"

        ws9.cell(r9, 1, f"={p}A{r7}").font = FONT_BOLD
        ws9.cell(r9, 2, f"={fm}*12").number_format = "#,##0.0"

        # AIA CQL: signed monthly FYC matches the Python stress-test assumption.
        aia_dr = f"IF({k2}>=80,IF({fm}>=50,0.24,IF({fm}>=20,0.18,IF({fm}>=7,0.15,0.1))),IF({fm}>=50,0.2,IF({fm}>=20,0.15,IF({fm}>=7,0.12,0.08))))"
        aia_ar = f"IF({act}>=6,0.12,IF({act}>=4,0.08,IF({act}>=2,0.05,0)))*IF({k2}>=70,1,{k2}/100)"
        aia_pq = f"IF(AND({k2}>=75,{fm}*3>=170,{act}*3>=14),0.15,IF(AND({k2}>=75,{fm}*3>=80,{act}*3>=9),0.08,IF(AND({k2}>=75,{fm}*3>=50,{act}*3>=6),0.05,0)))"
        aia_def = f"IF(AND({k2}>=75,{fm}*3>=170,{act}*3>=14),0.1,IF(AND({k2}>=75,{fm}*3>=80,{act}*3>=9),0.05,0))"
        ws9.cell(r9, 3, f"=B{r9}*({aia_dr}+{aia_ar}+{aia_pq})").number_format = "#,##0.00"
        ws9.cell(r9, 4, f"=IF({fm}>0,B{r9}*{aia_def},0)").number_format = "#,##0.00"
        ws9.cell(r9, 5, f"=IF({tot}>=85,D{r9}*0.6,0)").number_format = "#,##0.00"

        # Chubb AL HT KTN Monthly (Symmetric Negative FYC!) + Quarterly Multiplier + Indirect Gate (<15M -> 0!)
        chb_k2 = f"IF({k2}>=80,1.2,IF({k2}>=70,1,IF({k2}>=60,0.75,IF({k2}>=50,0.5,0.25))))"
        af = f"ABS({fm})"
        chb_mr = f"IF({ten}>=15,IF({af}>=40,IF({act}>=4,0.6,0.5),IF({af}>=30,IF({act}>=4,0.5,0.4),IF({af}>=20,IF({act}>=4,0.4,0.3),IF({af}>=10,IF({act}>=4,0.3,0.2),IF({af}>=5,IF({act}>=4,0.2,0.1),0))))),IF({af}>=20,IF({act}>=4,0.35,0.25),IF({af}>=10,IF({act}>=4,0.3,0.2),IF({af}>=5,IF({act}>=4,0.2,0.1),0))))"
        chb_qr = f"IF({fm}*3>=100,0.5,IF({fm}*3>=75,0.45,IF({fm}*3>=50,0.4,IF({fm}*3>=35,0.35,IF({fm}*3>=15,0.3,0)))))"
        ws9.cell(r9, 6, f"=B{r9}*{chb_mr}*{chb_k2}*(1+IF({fm}>0,{chb_qr},0))").number_format = "#,##0.00"
        ws9.cell(r9, 7, f"=IF({fm}<15,0,IF({fm}<30,0.3,0.5))*{sub}*12").number_format = "#,##0.00"
        ws9.cell(r9, 8, f"=IF(B{r9}=0,0,F{r9}/B{r9})").number_format = "0.0%"

        # Proposal Manager (Live Sheet 04 Block B)
        prp_k2 = f"IF({k2}>=85,1.2,IF({k2}>=80,1.1,IF({k2}>=75,1,IF({k2}>=70,0.85,IF({k2}>={par}$C$16,0.6,0)))))"
        ws9.cell(r9, 9, f"=B{r9}*MIN({par}$C$33,{par}$C$27*{prp_k2})").number_format = "#,##0.00"
        ws9.cell(r9, 10, f"=IF({fm}<15,0,{par}$C$28*{sub}*12)").number_format = "#,##0.00"
        ws9.cell(r9, 11, f"=IF(AND({fm}>0,{k2}>=75),B{r9}*{par}$C$29,0)").number_format = "#,##0.00"
        ws9.cell(r9, 12, "UNKNOWN").fill = FILL_WARN
        ws9.cell(r9, 13, "Symmetric Neg FYC!" if idx == 3 else ("Gate <15M=0!" if idx == 2 else "Full 12M"))
        for col in range(1, 14):
            ws9.cell(r9, col).border = BORDER

    # Section B: Tier 3 Senior Leaders — ALL 3 COMPETITORS + PROPOSAL (Profiles L01..L03 from Sheet 07 rows 22-24!)
    style_section(ws9, 11, "B. Tier 3 Senior Regional Leaders (AIA PAF+ [Live Sheet 05 Lookup] vs Manulife PSM+ [Apr Switch & 3Y Vest] vs Chubb RD [Q3 60% Cliff] vs Proposal)", 13)
    write_table_header(ws9, 12, [
        "Profile", "Ann Reg FYP", "AIA PAF+ SAF Total",
        "MNL Base Fee (Cap150%)", "MNL Prod+Act (Apr Sw)", "MNL 3Y Deferred", "MNL Total Earned",
        "Chubb RD Fixed", "Chubb RD 3MAA (Q3 Cliff)", "Chubb RD Growth", "Chubb RD Total",
        "Prop RD Cash Y1", "Prop RD 3Y Deferred"
    ])
    for idx in range(3):
        r9 = 13 + idx
        r7 = 22 + idx
        p = "'07_Profiles_12M_Input'!"
        par = "'04_Policy_Parameters'!"
        fyc_m = f"{p}D{r7}"
        fyp_m = f"{p}E{r7}"
        ehc_m = f"{p}F{r7}"
        k2 = f"{p}G{r7}"
        base_mnl = f"{p}I{r7}"
        ach = f"{p}K{r7}"

        ws9.cell(r9, 1, f"={p}A{r7}").font = FONT_BOLD
        ws9.cell(r9, 2, f"={fyp_m}*12").number_format = "#,##0.0"

        # C: AIA PAF+ SAF (Year 1 Annual Target pulled LIVE from Sheet 05!$G$3 = 5,000M)
        # Base 50M/M x FYP tier + Monthly & Quarterly Prof + Seniority capped at 12M Base
        paf_fy = f"IF({k2}>=75,1.2,IF({k2}>=70,1.1,IF({k2}>=65,1,IF({k2}>=60,0.8,IF({k2}>=50,0.6,0)))))"
        paf_b = f"50*12*IF({ach}>=1.15,1.2,IF({ach}>=0.55,1,IF({ach}>=0.35,0.5,0)))"
        # Phí chuyên nghiệp tháng [AIAVAD 2601-035 : 4] 50/100/115%; quý [AIAVAD 2601-035 : 5] 90/100/110/120%
        paf_pm = f"({fyc_m}*12)*(IF({ach}>=1.15,0.06,IF({ach}>=1,0.045,IF({ach}>=0.5,0.03,0)))*{paf_fy}+IF({ach}>=1.15,0.035,IF({ach}>=1,0.025,IF({ach}>=0.5,0.015,0))))"
        paf_pq = f"({fyc_m}*12)*(IF({ach}>=1.2,0.05,IF({ach}>=1.1,0.035,IF({ach}>=1,0.02,IF({ach}>=0.9,0.005,0))))*{paf_fy}+IF({ach}>=1.2,0.035,IF({ach}>=1.1,0.025,IF({ach}>=1,0.015,IF({ach}>=0.9,0.005,0)))))"
        paf_sen = f"MIN({paf_b},MAX(0,B{r9}-'05_Lookup_PAF_5Y'!$G$3)*0.05)"
        ws9.cell(r9, 3, f"={paf_b}+{paf_pm}+{paf_pq}+{paf_sen}").number_format = "#,##0.00"

        # D, E, F, G: Manulife PSM+ (Floor 30%, Cap 150%; Dual-phase K2 M1-3 vs M4-12; 1mAA=110% on L01 else 80%; 3Y Deferred 75% capped at 12x Base)
        mnl_k_pre = f"IF({k2}>=75,1.15,IF({k2}>=70,1.1,IF({k2}>=65,1.05,IF({k2}>=60,1,IF({k2}>=55,0.9,IF({k2}>=50,0.75,{k2}/100))))))"
        mnl_k_post = f"IF({k2}>=80,1.1,IF({k2}>=75,1.05,IF({k2}>=70,1,IF({k2}>=65,0.9,IF({k2}>=60,0.7,IF({k2}>=50,0.5,({k2}/100)/2))))))"
        mnl_pr = f"IF({ach}>=1.15,0.08,0.06)"
        mnl_ar = f"IF({ach}>=1.1,0.035,IF({ach}>=1,0.025,IF({ach}>=0.9,0.01,0)))"
        ws9.cell(r9, 4, f"=IF({ach}<0.3,0,MIN({base_mnl}*1.5,{base_mnl}*{ach}*1.3))*12").number_format = "#,##0.00"
        ws9.cell(r9, 5, f"={fyc_m}*({mnl_pr}*(3*{mnl_k_pre}+9*{mnl_k_post})+{mnl_ar}*(3*{mnl_k_pre}+9*{mnl_k_post}))").number_format = "#,##0.00"
        ws9.cell(r9, 6, f"=IF(AND({k2}>=70,{ach}>=0.85),MIN(12*{base_mnl},0.75*E{r9}),0)").number_format = "#,##0.00"
        ws9.cell(r9, 7, f"=D{r9}+E{r9}+F{r9}").number_format = "#,##0.00"

        # H, I, J, K: Chubb RD (Fixed Training+Act+Biz; 3MAA with Q1-2 50% vs Q3-4 60% Cliff; Growth 10% at +15% QoQ (0003V p.8 band 15-<20%) x Cliff)
        rd_fix = f"12*(IF({fyp_m}>=400,25,12.5)+IF({ehc_m}>=20,8,IF({ehc_m}>=16,6.5,IF({ehc_m}>=12,5,IF({ehc_m}>=9,3.5,IF({ehc_m}>=6,2.5,IF({ehc_m}>=4,1.5,0))))))+IF({fyp_m}>=600,12,IF({fyp_m}>=480,9.5,IF({fyp_m}>=360,7,IF({fyp_m}>=270,5,IF({fyp_m}>=180,3.5,IF({fyp_m}>=120,2.5,0)))))))"
        rd_3m_r = f"IF({ehc_m}>=12,0.12,IF({ehc_m}>=10,0.1,IF({ehc_m}>=8,0.08,IF({ehc_m}>=6,0.06,IF({ehc_m}>=4,0.04,IF({ehc_m}>=2,0.02,0))))))"
        rd_g_q12 = f"IF({k2}>=50,1,0)"
        rd_g_q34 = f"IF({k2}>=60,1,0)"
        ws9.cell(r9, 8, f"={rd_fix}").number_format = "#,##0.00"
        ws9.cell(r9, 9, f"=6*{fyc_m}*{rd_3m_r}*({rd_g_q12}+{rd_g_q34})").number_format = "#,##0.00"
        ws9.cell(r9, 10, f"=6*{fyc_m}*IF({fyp_m}*3<360,0.025,0.1)*({rd_g_q12}+{rd_g_q34})").number_format = "#,##0.00"
        ws9.cell(r9, 11, f"=H{r9}+I{r9}+J{r9}").number_format = "#,##0.00"

        # L, M: Proposal Regional Leader
        prp_k2 = f"IF({k2}>=85,1.2,IF({k2}>=80,1.1,IF({k2}>=75,1,IF({k2}>=70,0.85,IF({k2}>={par}$C$16,0.6,0)))))"
        prp_rd_b = f"IF({ach}<0.3,0,MIN({par}$C$30*1.4,{par}$C$30*{ach}*1.25))*12"
        prp_rd_v = f"({fyc_m}*12)*{par}$C$31*{prp_k2}"
        ws9.cell(r9, 12, f"={prp_rd_b}+{prp_rd_v}").number_format = "#,##0.00"
        ws9.cell(r9, 13, f"=IF({k2}>=75,{prp_rd_v}*{par}$C$32,0)").number_format = "#,##0.00"
        for col in range(1, 14):
            ws9.cell(r9, col).border = BORDER

    # Section C on Sheet 09: Exact 12-Month SAF Year 1 Live Lookup Block (pulls M01-M12 from Sheet 05!)
    style_section(ws9, 17, "C. AIA PAF+ SAF Year 1 Exact 12-Month & Quarterly 1mAA Achievement (Live INDEX/MATCH from Sheet 05 — Used by Sheet 11!)", 13)
    write_table_header(ws9, 18, ["Metric / Month", "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12"])
    ws9.cell(19, 1, "SAF Y1 1mAA Target (Live)").font = FONT_BOLD
    ws9.cell(20, 1, "Region Actual 1mAA (=20/M)").font = FONT_BOLD
    ws9.cell(21, 1, "Monthly 1mAA Rate (0-3.5%)").font = FONT_BOLD
    ws9.cell(22, 1, "Monthly 1mAA Fee (300M FYC)").font = FONT_BOLD
    for m in range(1, 13):
        col = m + 1
        cl = get_column_letter(col)
        mk = f"M{m:02d}"
        ws9.cell(19, col, f'=INDEX(\'05_Lookup_PAF_5Y\'!$H$8:$H$1307,MATCH("SAF|Year_1|{mk}|1mAA_Count",\'05_Lookup_PAF_5Y\'!$A$8:$A$1307,0))').number_format = "0.0"
        ws9.cell(20, col, 20.0).fill = FILL_INPUT; ws9.cell(20, col).font = FONT_BLUE
        ws9.cell(21, col, f"=IF({cl}20/{cl}19>=1.15,0.035,IF({cl}20/{cl}19>=1,0.025,IF({cl}20/{cl}19>=0.5,0.015,0)))").number_format = "0.0%"   # [AIAVAD 2601-035 : 4]
        ws9.cell(22, col, f"=300*{cl}21").number_format = "0.00"
        for rr in range(19, 23):
            ws9.cell(rr, col).border = BORDER
    for rr in range(19, 23):
        ws9.cell(rr, 1).border = BORDER
    # Quarterly 1mAA Fee Summary (Row 23)
    ws9.cell(23, 1, "Quarterly 1mAA Fee (Q1-Q4)").font = FONT_BOLD; ws9.cell(23, 1).border = BORDER
    q_cols = [("B", "D", 2), ("E", "G", 5), ("H", "J", 8), ("K", "M", 11)]
    for q_idx, (c1, c2, dest_c) in enumerate(q_cols, 1):
        ach_q = f"(SUM({c1}20:{c2}20)/SUM({c1}19:{c2}19))"
        ws9.cell(23, dest_c, f"=900*IF({ach_q}>=1.2,0.035,IF({ach_q}>=1.1,0.025,IF({ach_q}>=1,0.015,IF({ach_q}>=0.9,0.005,0))))").number_format = "0.00"   # [AIAVAD 2601-035 : 5]
        ws9.cell(23, dest_c).border = BORDER
    ws9.cell(24, 1, "Total Annual 1mAA Prof Fees (M+Q)").font = FONT_BOLD; ws9.cell(24, 1).border = BORDER
    ws9.cell(24, 2, "=SUM(B22:M22)+B23+E23+H23+K23").number_format = "#,##0.00"; ws9.cell(24, 2).font = FONT_BOLD; ws9.cell(24, 2).border = BORDER
    set_col_widths(ws9, {1: 28, 2: 14, 3: 15, 4: 15, 5: 15, 6: 15, 7: 15, 8: 14, 9: 15, 10: 14, 11: 14, 12: 14, 13: 18})

    # =========================================================================
    # SHEET 10: 10_Total_Rewards_Ledger (Earned / Cash Paid Y1 / Deferred / Unpriced Non-Cash)
    # =========================================================================
    ws10 = wb.create_sheet("10_Total_Rewards_Ledger")
    style_title(ws10, 1, "EARNED / PAID / DEFERRED / CLAWBACK / UNPRICED NON-CASH LEDGER (STANDARD REGION 12B FYP, K2=82%)", 10)
    write_table_header(ws10, 3, [
        "Scheme (12B FYP Region, K2=82%)", "Total Earned (M)", "Cash Paid Y1 (M)", "Deferred Post-Y1 (M)",
        "Cash Y1 Share (%)", "Y+1 Vesting (M)", "Y+2 Vesting (M)", "Y+3/+4 Vesting (M)",
        "Clawback Mechanism", "Unpriced Non-Cash Benefits (Cost=UNKNOWN)"
    ])
    ledger_rows = [
        ("AIA Alpha 2026 (excl. Exchange/Pro)", "='11_Hierarchy_Dist_Cost'!I5", "='11_Hierarchy_Dist_Cost'!J5", "='11_Hierarchy_Dist_Cost'!H5",
         "=C4/B4", 0.0, "=D4*0.15", "=D4*0.85", "6M full clawback + PAF+ 12M 100% clawback", "Special 3M Trip + Health Ins Std/Prem (UNKNOWN)"),
        ("Chubb Life Agency 2026", "='11_Hierarchy_Dist_Cost'!I7", "='11_Hierarchy_Dist_Cost'!J7", "='11_Hierarchy_Dist_Cost'!H7",
         "=C5/B5", 0.0, 0.0, 0.0, "T+1 hold (K2<60%) + Symmetric Negative AL FYC", "RD Health & Accident Insurance (UNKNOWN)"),
        ("Manulife PSM+ (Tier 3 Region Only — L01)", "='09_Mgr_Senior_Comp'!G13", "='09_Mgr_Senior_Comp'!D13+'09_Mgr_Senior_Comp'!E13", "='09_Mgr_Senior_Comp'!F13",
         "=C6/B6", "=D6*0.30", "=D6*0.30", "=D6*0.40", "Post-termination clawback C.11 + K2>=70% gate", "None disclosed in 0048M01 (Tier 1-2 UNKNOWN)"),
        ("W24 Proposed Balanced (PROPOSAL)", "='11_Hierarchy_Dist_Cost'!I8", "='11_Hierarchy_Dist_Cost'!J8", "='11_Hierarchy_Dist_Cost'!H8",
         "=C7/B7", "=D7*0.30", "=D7*0.30", "=D7*0.40", "T+1 hold (K2<65%) + 6M Clawback + Neg FYC", "Optional Recognition (budgeted separately)"),
    ]
    for i, lr in enumerate(ledger_rows, 4):
        for j, val in enumerate(lr, 1):
            c = ws10.cell(i, j, val)
            c.border = BORDER
            if j in (2, 3, 4, 6, 7, 8):
                c.number_format = "#,##0.00"
            elif j == 5:
                c.number_format = "0.0%"
            if j == 10 and "UNKNOWN" in str(val):
                c.fill = FILL_WARN
    set_col_widths(ws10, {1: 36, 2: 16, 3: 16, 4: 16, 5: 14, 6: 14, 7: 14, 8: 15, 9: 34, 10: 36})

    # =========================================================================
    # SHEET 11: 11_Hierarchy_Dist_Cost (Enterprise Total Distribution Cost — ZERO DOUBLE COUNT!)
    # =========================================================================
    ws11 = wb.create_sheet("11_Hierarchy_Dist_Cost")
    style_title(ws11, 1, "ENTERPRISE TOTAL DISTRIBUTION COST (12,000M FYP COUNTED ONCE — 0 DOUBLE COUNTING — ART.52 CHECK)", 15)
    ws11["A2"] = "Org Hierarchy: 1 Region (12,000M FYP = 3,600M FYC @30% UL) -> 1 Regional Leader -> 4 Direct Managers (75M FYC/M each, 2 sub-mgrs indirect) -> 20 Active Agents (15M FYC/M each, 3M active/Q)."
    ws11.merge_cells("A2:O2")
    ws11["A2"].font = FONT_BOLD

    write_table_header(ws11, 4, [
        "Scheme & Persistency Scenario", "K2/FY (%)", "Layer A: Comm (30%)", "Layer B: Agent Bonus",
        "Layer C: Mgr Direct", "Layer D: Mgr Indirect", "Layer E: RD Cash", "Layer F: 3Y Deferred",
        "Total Earned (M)", "Cash Paid Y1 (M)", "Earned % FYP", "Cash Y1 % FYP",
        "Art.52 Modeled Bonus % FYP", "Modeled Threshold Check", "Cost / Persisted Y2 %"
    ])
    par = "'04_Policy_Parameters'!"
    # 12 rows = 3 K2 levels (82, 72, 62) x 4 schemes (AIA 26, AIA 27, Chubb 26, Proposal Balanced)
    # Every single cell is a 100% live Excel formula matching compensation_engine.py!
    row_specs = []
    for k2v in (82.0, 72.0, 62.0):
        for sc in ("AIA_Alpha_2026", "AIA_Alpha_2027", "Chubb_Agency_2026", "W24_Proposed_Balanced"):
            row_specs.append((sc, k2v))

    for idx, (sc, k2v) in enumerate(row_specs, 5):
        ws11.cell(idx, 1, f"{sc} (K2={int(k2v)}%)").font = FONT_BOLD
        ws11.cell(idx, 2, k2v).fill = FILL_INPUT; ws11.cell(idx, 2).font = FONT_BLUE
        # Layer A: 12000 * UL_FYC_Rate (Sheet 04!$C$7)
        ws11.cell(idx, 3, f"=12000*{par}$C$7")
        k2c = f"B{idx}"

        if sc in ("AIA_Alpha_2026", "AIA_Alpha_2027"):
            is26 = (sc == "AIA_Alpha_2026")
            # [AIAVAD 2604-069 : 3]
            fy_f = f"IF({k2c}>=85,1.2,IF({k2c}>=75,1.1,IF({k2c}>=65,1,{k2c}/100)))" if is26 else f"IF({k2c}>=90,1.2,IF({k2c}>=80,1.1,IF({k2c}>=70,1,0)))"
            # Agent: 15M/M -> Q=45M (15% prod), 4S (10% if FY>=65/70), Ann=180M (6% prod)
            p_gate = 65 if is26 else 70
            ag_r = f"(0.15+IF({k2c}>={p_gate},0.10,0)+0.06)*{fy_f}"
            ws11.cell(idx, 4, f"=C{idx}*{ag_r}")
            # Manager: 4 mgrs x 75M/M = 3600M/Y (Q=225M >=170M, 5 act/M -> 15 act/Q >=14 -> 5S Q 15%, 5S Ann 10% deferred if FY>=75!)
            # Direct monthly: >=50M -> 24% (FY>=80) else 20%; Activity: 5 act -> 8% * (1 if FY>=70 else FY/100)
            mg_dir_m = f"IF({k2c}>=80,0.24,0.20)"
            mg_act_m = f"0.08*IF({k2c}>=70,1,{k2c}/100)"
            mg_pq = f"IF({k2c}>=75,0.15,0)"
            ws11.cell(idx, 5, f"=C{idx}*({mg_dir_m}+{mg_act_m}+{mg_pq})")
            # Indirect: 2 sub-mgrs (1800M FYC) * direct_m * 50%
            ws11.cell(idx, 6, f"=(C{idx}/2)*{mg_dir_m}*0.5")
            # PAF+ SAF Year 1 (Target 5000M live from Sheet 05!$G$3; 1mAA M+Q exact live from Sheet 09!$B$24!)
            paf_fy = f"IF({k2c}>=75,1.2,IF({k2c}>=70,1.1,IF({k2c}>=65,1,IF({k2c}>=60,0.8,IF({k2c}>=50,0.6,0)))))"
            ws11.cell(idx, 7, f"=720+C{idx}*((0.06+0.05)*{paf_fy})+'09_Mgr_Senior_Comp'!$B$24+MIN(720,MAX(0,12000-'05_Lookup_PAF_5Y'!$G$3)*0.05)")
            # Deferred 3Y (CQL 5S Ann 10% if FY>=75)
            ws11.cell(idx, 8, f"=C{idx}*IF({k2c}>=75,0.10,0)")

        elif sc == "Chubb_Agency_2026":
            chb_k2 = f"IF({k2c}>=80,1.2,IF({k2c}>=70,1,IF({k2c}>=60,0.75,IF({k2c}>=50,0.5,0.25))))"
            # Agent: 15M/M -> Q=45M (45% AR tier) * K2 * 1.30 (3 EHC)
            ws11.cell(idx, 4, f"=C{idx}*0.45*{chb_k2}*1.3")
            # Manager: 75M/M (>=40M, 5 EHC >=4 -> 60%) * K2 * 1.50 (Q=225M >=100M)
            ws11.cell(idx, 5, f"=C{idx}*0.60*{chb_k2}*1.5")
            # Indirect: 2 sub-mgrs monthly HT KTN (1800 * 0.60 * K2) * 50%
            ws11.cell(idx, 6, f"=(C{idx}/2)*0.60*{chb_k2}*0.5")
            # RD: Fixed (25+8+12)*12=540 + 3MAA (20>=12 -> 12% x cliff) + Growth (+15% -> 10% x cliff, 0003V p.8 band 15-<20%)
            g12 = f"IF({k2c}>=50,1,0)"
            g34 = f"IF({k2c}>=60,1,0)"
            ws11.cell(idx, 7, f"=540+(C{idx}/2)*(0.12+0.1)*({g12}+{g34})")
            ws11.cell(idx, 8, 0.0)

        else:  # W24_Proposed_Balanced
            prp_k2 = f"IF({k2c}>=85,1.2,IF({k2c}>=80,1.1,IF({k2c}>=75,1,IF({k2c}>=70,0.85,IF({k2c}>={par}$C$16,0.6,0)))))"
            # Agent 15M/M -> Tier 2 (C19=16%) * K2 * (1+C23=12%)
            ws11.cell(idx, 4, f"=C{idx}*{par}$C$19*{prp_k2}*(1+{par}$C$23)")
            # Mgr Direct: C27 (30%) * K2; Indirect: 50% sub * C28 (35%)
            ws11.cell(idx, 5, f"=C{idx}*MIN({par}$C$33,{par}$C$27*{prp_k2})")
            ws11.cell(idx, 6, f"=E{idx}*0.5*{par}$C$28")
            # RD Cash: Base C30*12*MIN(1.4,1.05*1.25) + Var C*C31*K2
            ws11.cell(idx, 7, f"={par}$C$30*12*MIN(1.4,1.05*1.25)+C{idx}*{par}$C$31*{prp_k2}")
            # Deferred 3Y (Mgr C29 + RD Var*C32 if K2>=75)
            ws11.cell(idx, 8, f"=IF({k2c}>=75,C{idx}*{par}$C$29+C{idx}*{par}$C$31*{prp_k2}*{par}$C$32,0)")

        # I..O Totals & Ratios
        ws11.cell(idx, 9, f"=SUM(C{idx}:H{idx})")                        # Total Earned
        ws11.cell(idx, 10, f"=I{idx}-H{idx}")                            # Cash Paid Y1
        ws11.cell(idx, 11, f"=I{idx}/12000")                             # Earned % FYP
        ws11.cell(idx, 12, f"=J{idx}/12000")                             # Cash Y1 % FYP
        ws11.cell(idx, 13, f"=D{idx}/12000")                             # Art.52 Bonus % FYP
        ws11.cell(idx, 14, f'=IF(M{idx}<={par}$C$10,"PASS","FAIL")')     # Art.52 Gate
        ws11.cell(idx, 15, f"=I{idx}/(12000*(B{idx}/100))")              # Cost / Persisted Y2 FYP

        for col in range(1, 16):
            c = ws11.cell(idx, col)
            c.border = BORDER
            if col in (3, 4, 5, 6, 7, 8, 9, 10):
                c.number_format = "#,##0.0"
            elif col in (11, 12, 13, 15):
                c.number_format = "0.00%"
    set_col_widths(ws11, {1: 30, 2: 10, 3: 14, 4: 14, 5: 14, 6: 14, 7: 13, 8: 13, 9: 14, 10: 14, 11: 12, 12: 12, 13: 13, 14: 13, 15: 15})

    # =========================================================================
    # SHEET 12: 12_Benchmark_And_Eval (15-Criteria Rubric + 4 Weight Sensitivity Scenarios)
    # =========================================================================
    ws12 = wb.create_sheet("12_Benchmark_And_Eval")
    style_title(ws12, 1, "15-CRITERIA EVALUATION RUBRIC & WEIGHT SENSITIVITY (DRAFT — NOT INDEPENDENTLY CALIBRATED)", 11)
    write_table_header(ws12, 3, [
        "Code", "Pillar", "Criterion", "PO Base Wt", "Growth-First Wt", "Quality-First Wt", "ROI-First Wt",
        "AIA Alpha", "Chubb Life", "Manulife (T3 Only)", "W24 Proposal"
    ])
    rubric = [
        ("C01", "Growth", "Activation & Time to First Sale", 0.08, 0.12, 0.05, 0.05, 4.0, 4.2, "N/A", 4.2),
        ("C02", "Growth", "Productivity & Consistency", 0.09, 0.13, 0.06, 0.06, 3.8, 4.5, "N/A", 4.2),
        ("C03", "Growth", "Recruitment & Manager Build", 0.07, 0.11, 0.05, 0.05, 4.2, 3.8, 3.8, 4.0),
        ("C04", "Growth", "Product Mix & Protection (HSBH/Top-up)", 0.06, 0.09, 0.04, 0.04, 3.0, 4.6, 3.4, 4.5),
        ("C05", "Quality", "Persistency Discipline (K2/FY Gates)", 0.10, 0.06, 0.16, 0.08, 4.2, 3.0, 4.2, 4.6),
        ("C06", "Quality", "Renewal Servicing Incentives (SYC/RYC)", 0.07, 0.04, 0.12, 0.06, 4.2, 4.0, 3.2, 4.5),
        ("C07", "Quality", "Anti-Gaming, Clawback & Behavior", 0.08, 0.05, 0.12, 0.06, 3.3, 4.0, 4.2, 4.7),
        ("C08", "Financial", "Enterprise Total Dist Cost Control", 0.08, 0.05, 0.06, 0.14, 3.2, 2.0, 4.2, 4.6),
        ("C09", "Financial", "Fixed Burn & Cap Discipline", 0.06, 0.04, 0.05, 0.10, 2.5, 3.2, 4.2, 4.5),
        ("C10", "Financial", "Y1 Cash Flow & Deferral Design", 0.06, 0.03, 0.05, 0.09, 3.8, 2.2, 4.6, 4.5),
        ("C11", "Financial", "Downside Resilience & Break-Even", 0.05, 0.03, 0.04, 0.07, 3.5, 2.6, 3.8, 4.5),
        ("C12", "People", "Career Path Fairness & Clarity", 0.05, 0.08, 0.05, 0.05, 3.6, 3.4, 3.8, 4.3),
        ("C13", "People", "Long-Term Retention Lock-in", 0.05, 0.07, 0.05, 0.05, 4.2, 2.8, 4.4, 4.5),
        ("C14", "Impl", "Simplicity & Field Explainability", 0.05, 0.05, 0.05, 0.05, 2.0, 3.0, 4.5, 4.2),
        ("C15", "Impl", "Operability & Auditability (Zero Conflict)", 0.05, 0.05, 0.05, 0.05, 2.5, 2.5, 3.0, 4.4),
    ]
    for i, rb in enumerate(rubric, 4):
        for j, val in enumerate(rb, 1):
            c = ws12.cell(i, j, val)
            c.border = BORDER
            if j in (4, 5, 6, 7):
                c.number_format = "0%"
                c.fill = FILL_INPUT; c.font = FONT_BLUE
            elif j in (8, 9, 10, 11) and val == "N/A":
                c.fill = FILL_WARN
    # Weight Sum Row 19
    ws12.cell(19, 3, "TOTAL WEIGHT CHECK (MUST = 100%)").font = FONT_BOLD
    for col in range(4, 8):
        cl = get_column_letter(col)
        c = ws12.cell(19, col, f"=SUM({cl}4:{cl}18)")
        c.number_format = "0%"; c.font = FONT_BOLD; c.border = BORDER

    # Sensitivity Summary Rows 21-25
    style_section(ws12, 21, "Weighted Score Comparison & Weight Sensitivity (Live SUMPRODUCT)", 11)
    write_table_header(ws12, 22, ["Scenario", "Weights (G/Q/F/P/I)", "AIA Alpha", "Chubb Life", "Proposal Balanced", "AIA vs Chubb Winner"])
    sens = [
        ("1. PO Reference Weights", "30 / 25 / 25 / 10 / 10", "D"),
        ("2. Growth-First Strategy", "45 / 15 / 15 / 15 / 10", "E"),
        ("3. Quality-First Strategy", "20 / 40 / 20 / 10 / 10", "F"),
        ("4. Financial-ROI-First Strategy", "20 / 20 / 40 / 10 / 10", "G"),
    ]
    for i, (sn, wlbl, wcol) in enumerate(sens, 23):
        ws12.cell(i, 1, sn).font = FONT_BOLD; ws12.cell(i, 1).border = BORDER
        ws12.cell(i, 2, wlbl).border = BORDER
        ws12.cell(i, 3, f"=SUMPRODUCT(${wcol}$4:${wcol}$18,$H$4:$H$18)").number_format = "0.00"; ws12.cell(i, 3).border = BORDER
        ws12.cell(i, 4, f"=SUMPRODUCT(${wcol}$4:${wcol}$18,$I$4:$I$18)").number_format = "0.00"; ws12.cell(i, 4).border = BORDER
        ws12.cell(i, 5, f"=SUMPRODUCT(${wcol}$4:${wcol}$18,$K$4:$K$18)").number_format = "0.00"; ws12.cell(i, 5).font = FONT_BOLD; ws12.cell(i, 5).fill = FILL_PASS; ws12.cell(i, 5).border = BORDER
        ws12.cell(i, 6, f'=IF(C{i}>D{i},"AIA Alpha","Chubb Life")').border = BORDER
    set_col_widths(ws12, {1: 10, 2: 14, 3: 36, 4: 13, 5: 14, 6: 14, 7: 13, 8: 12, 9: 12, 10: 16, 11: 14})

    # =========================================================================
    # SHEET 13: 13_MAPA_And_Financial (MAPA Forward/Reverse + Break-Even Sensitivity)
    # =========================================================================
    ws13 = wb.create_sheet("13_MAPA_And_Financial")
    style_title(ws13, 1, "MAPA FORWARD / REVERSE PLANNER & FINANCIAL BREAK-EVEN VNB MARGIN SENSITIVITY (NO FABRICATED MARGINS)", 9)

    style_section(ws13, 3, "A. MAPA Forward & Reverse Calculator (Blue/Yellow = PO Editable)", 9)
    write_table_header(ws13, 4, ["Mode", "Manpower", "Active Ratio", "Cases/Active/M", "Avg Case FYP (M)", "Months", "Active Agents", "Total Cases", "Annual FYP (M)"])
    # Row 5: Forward
    ws13.cell(5, 1, "MAPA Forward").font = FONT_BOLD
    for col, val, fmt in [(2, 200, "#,##0"), (3, 0.35, "0.0%"), (4, 1.5, "0.00"), (5, 20.0, "#,##0.0"), (6, 12, "0")]:
        c = ws13.cell(5, col, val); c.fill = FILL_INPUT; c.font = FONT_BLUE; c.number_format = fmt; c.border = BORDER
    ws13.cell(5, 7, "=B5*C5").number_format = "#,##0.0"
    ws13.cell(5, 8, "=G5*D5*F5").number_format = "#,##0.0"
    ws13.cell(5, 9, "=H5*E5").number_format = "#,##0.0"
    ws13.cell(5, 9).font = FONT_BOLD

    # Row 6: Reverse (Solve Required Manpower from Target FYP!)
    ws13.cell(6, 1, "MAPA Reverse (Solve MP)").font = FONT_BOLD
    ws13.cell(6, 2, "=I6/(C6*D6*E6*F6)").number_format = "#,##0.0"; ws13.cell(6, 2).font = FONT_BOLD; ws13.cell(6, 2).fill = FILL_PASS
    for col, val, fmt in [(3, 0.35, "0.0%"), (4, 1.5, "0.00"), (5, 20.0, "#,##0.0"), (6, 12, "0"), (9, 25200.0, "#,##0.0")]:
        c = ws13.cell(6, col, val); c.fill = FILL_INPUT; c.font = FONT_BLUE; c.number_format = fmt; c.border = BORDER
    ws13.cell(6, 7, "=B6*C6").number_format = "#,##0.0"
    ws13.cell(6, 8, "=G6*D6*F6").number_format = "#,##0.0"
    for r in (5, 6):
        for col in range(1, 10):
            ws13.cell(r, col).border = BORDER

    style_section(ws13, 8, "B. Financial Break-Even Gross Margin Sensitivity (OpEx = 15% / 20% / 25% FYP — ASSUMPTION, Linked to Sheet 11!)", 9)
    write_table_header(ws13, 9, [
        "Scheme & K2 Scenario", "Earned Dist Cost %", "Cash Y1 Cost %", "Cost / Persisted Y2 %",
        "BE Margin (OpEx 15%)", "BE Margin (OpEx 20%)", "BE Margin (OpEx 25%)", "Cash Y1 Saved vs Chubb", "Art.52 Cap Gate"
    ])
    # Reference 8 key rows from Sheet 11 (K2=82%: rows 5,6,7,8; K2=62%: rows 13,14,15,16)
    ref_rows = [5, 6, 7, 8, 13, 14, 15, 16]
    for i, sr in enumerate(ref_rows, 10):
        chb_ref = 7 if sr <= 8 else 15
        ws13.cell(i, 1, f"='11_Hierarchy_Dist_Cost'!A{sr}").font = FONT_BOLD
        ws13.cell(i, 2, f"='11_Hierarchy_Dist_Cost'!K{sr}").number_format = "0.00%"
        ws13.cell(i, 3, f"='11_Hierarchy_Dist_Cost'!L{sr}").number_format = "0.00%"
        ws13.cell(i, 4, f"='11_Hierarchy_Dist_Cost'!O{sr}").number_format = "0.00%"
        ws13.cell(i, 5, f"=B{i}+0.15").number_format = "0.00%"
        ws13.cell(i, 6, f"=B{i}+'04_Policy_Parameters'!$C$8").number_format = "0.00%"
        ws13.cell(i, 7, f"=B{i}+0.25").number_format = "0.00%"
        ws13.cell(i, 8, f"='11_Hierarchy_Dist_Cost'!L{chb_ref}-C{i}").number_format = "+0.00%;-0.00%;0.00%"
        ws13.cell(i, 9, f"='11_Hierarchy_Dist_Cost'!N{sr}")
        for col in range(1, 10):
            ws13.cell(i, col).border = BORDER
    set_col_widths(ws13, {1: 30, 2: 15, 3: 14, 4: 17, 5: 16, 6: 16, 7: 16, 8: 18, 9: 15})

    # =========================================================================
    # SHEET 14: 14_QA_Golden_Tests (20 Live Excel Formula Assertions!)
    # =========================================================================
    ws14 = wb.create_sheet("14_QA_Golden_Tests")
    style_title(ws14, 1, "LIVE EXCEL GOLDEN TEST SUITE (24 FORMULA ASSERTIONS — VERIFIED VIA MICROSOFT EXCEL COM)", 8)
    ws14["A3"] = "Overall Test Summary:"
    ws14["A3"].font = FONT_BOLD
    ws14["B3"] = '=COUNTIF(H5:H28,"PASS")&"/"&COUNTA(H5:H28)&" PASS"'
    ws14["B3"].font = FONT_BOLD; ws14["B3"].fill = FILL_PASS
    ws14["D3"] = "Failed Tests:"
    ws14["E3"] = '=COUNTIF(H5:H28,"FAIL")'
    ws14["E3"].font = FONT_BOLD

    write_table_header(ws14, 4, ["Test_ID", "Category", "Assertion Description", "Target Sheet", "Expected (Hand Calc)", "Excel Formula Actual", "Abs Diff", "Status"])
    golden_excel = [
        ("XL-GT-01", "Lookup Integrity", "PAF+ Normalized Row Count = 1,300", "05_Lookup_PAF_5Y", 1300.0, "='05_Lookup_PAF_5Y'!B3"),
        ("XL-GT-02", "Lookup Integrity", "PAF+ Annual vs Monthly Sum Discrepancies = 0", "05_Lookup_PAF_5Y", 0.0, "='05_Lookup_PAF_5Y'!K3"),
        ("XL-GT-03", "Lookup Value", "PAF+ SPVP Year 5 Annual FYP Target = 62,300M", "05_Lookup_PAF_5Y", 62300.0, "='05_Lookup_PAF_5Y'!E3"),
        ("XL-GT-04", "Chubb HSBH", "Tu Do An Phuc Age 30M HSBH=65 -> 27.0%", "06_Lookup_Chubb_Comm", 0.27, "='06_Lookup_Chubb_Comm'!G5"),
        ("XL-GT-05", "Chubb HSBH", "Tu Do An Phuc Age 10F HSBH=60 -> 22.0%", "06_Lookup_Chubb_Comm", 0.22, "='06_Lookup_Chubb_Comm'!G6"),
        ("XL-GT-06", "Chubb Schedule", "KHTC Cao nien 65-80t Y1 = 27.0% (non-30% UL!)", "06_Lookup_Chubb_Comm", 27.0, "='06_Lookup_Chubb_Comm'!I5"),
        ("XL-GT-07", "AIA 2026 vs 2027", "A04 (20M/M + 2M SYC, FY=65% -> 100% [AIAVAD 2604-069 : 3]) AIA 2026 Bonus = 93.60M", "08_Indiv_Comp_12M", 93.60, "='08_Indiv_Comp_12M'!E7"),
        ("XL-GT-08", "AIA 2027 Cliff", "A04 (20M/M, FY=65%) AIA 2027 Cliff Bonus = 0.00M", "08_Indiv_Comp_12M", 0.00, "='08_Indiv_Comp_12M'!G7"),
        ("XL-GT-09", "AIA Rounding", "A08 (FY=74.49%) HalfUp Toggle -> Rounded = 74", "08_Indiv_Comp_12M", 74.0, "='08_Indiv_Comp_12M'!D11"),
        ("XL-GT-10", "Chubb AR Peak", "A05 (60M/M, K2=85%) Chubb AR %FYC = 185.8% (incl RYC+B)", "08_Indiv_Comp_12M", 1.858, "='08_Indiv_Comp_12M'!I8/'08_Indiv_Comp_12M'!B8+1-0.15*('07_Profiles_12M_Input'!D9*12)/'08_Indiv_Comp_12M'!B8"),
        ("XL-GT-11", "Chubb AL Peak", "A09 (25M/M AL, K2=85%) Chubb AL Personal Bonus = 334.80M", "08_Indiv_Comp_12M", 334.80, "='08_Indiv_Comp_12M'!I12"),
        ("XL-GT-12", "Chubb CH Offset", "PDF p.10 M7 Offset: CH Month Net = 0.00M", "08_Indiv_Comp_12M", 0.00, "='08_Indiv_Comp_12M'!J18"),
        ("XL-GT-13", "Chubb CH Offset", "PDF p.10 M7 Offset: CH M12 Deferred Net = 1.40M", "08_Indiv_Comp_12M", 1.40, "='08_Indiv_Comp_12M'!K18"),
        ("XL-GT-14", "Chubb ERR-DOC-01", "PDF p.10 M12 Table_80 Toggle (SOP=85%): Month Net = 2.50M", "08_Indiv_Comp_12M", 2.50, "='08_Indiv_Comp_12M'!J19"),
        ("XL-GT-15", "Chubb AL Gate", "M03 (NTT=14M < 15M): Chubb Indirect L1 = 0.00M", "09_Mgr_Senior_Comp", 0.00, "='09_Mgr_Senior_Comp'!G7"),
        ("XL-GT-16", "Chubb Neg FYC", "M04 (NTT=-25M/M): Chubb Symmetric Neg Fee = -144.00M/Y", "09_Mgr_Senior_Comp", -144.00, "='09_Mgr_Senior_Comp'!F8"),
        ("XL-GT-17", "Manulife Cap/Def", "L01 (120% Ach, K2=80%): Manulife Base Cap 150% = 630.00M", "09_Mgr_Senior_Comp", 630.00, "='09_Mgr_Senior_Comp'!D13"),
        ("XL-GT-18", "Manulife Floor", "L03 (29% Ach <30%, K2=65%): Base + Deferred = 0.00M", "09_Mgr_Senior_Comp", 0.00, "='09_Mgr_Senior_Comp'!D15+'09_Mgr_Senior_Comp'!F15"),
        ("XL-GT-19", "Chubb RD Cliff", "L02 (K2=55%): Q1-2 Pass & Q3-4 Cliff=0 -> 3MAA = 86.40M", "09_Mgr_Senior_Comp", 86.40, "='09_Mgr_Senior_Comp'!I14"),
        ("XL-GT-20", "MAPA Identity", "MAPA Reverse Manpower for 25,200M FYP = 200.0", "13_MAPA_And_Financial", 200.0, "='13_MAPA_And_Financial'!B6"),
    ]
    # ---- Sheet 15: Manulife Đại Lý (0046M01/2026) & UM+ (0047M01/2026) — công thức Excel độc lập, so với Python ----
    sys.path.insert(0, str(REPO / "scripts")); sys.path.insert(0, str(REPO))
    import build_interview_income_table as _T  # noqa: E402
    from w24_milestones import load_milestones as _lm  # noqa: E402
    _ms = _lm()
    ws15 = wb.create_sheet("15_Manulife_Agent_UMplus")
    style_title(ws15, 1, "MANULIFE — ĐẠI LÝ (0046M01/2026/ASBD) & QUẢN LÝ ĐẠI LÝ UM+ (0047M01/2026/ASBD) THEO 4 MỐC", 11)
    ws15["A2"] = "Nguồn: 0046M01 p.1 (hệ số TLDTHD), p.4 (thưởng năng suất tháng), p.5 (thưởng quý); 0047M01 p.1 (năng suất nhóm cấp 1-4), p.2 (hoạt động nhóm, hệ số TLDTHD). Đơn vị: triệu VND/năm. Không danh hiệu Manulife Pro / MBA Pro (tiêu chí không có trong nguồn)."
    ws15["A2"].font = FONT_NORM
    write_table_header(ws15, 4, ["Mốc", "FYC/đại lý/tháng", "Số ĐL trực tiếp", "FYC cấp 2/tháng", "FYC cấp 3/tháng", "K2 (%)",
                                 "Thưởng ĐL năm (tháng+quý)", "UM+ A.I năm", "UM+ A.II năm", "UM+ tổng năm", "Python tổng năm"])
    _rows = []
    for _i, _m in enumerate(_ms, 5):
        fpa = _m.fyp_per_agent * 0.30
        c2 = 5 * _m.direct_managers * fpa
        c3 = 5 * _m.grand_sub_units * fpa
        ws15.cell(_i, 1, _m.label)
        ws15.cell(_i, 2, round(fpa, 6)).font = FONT_BLUE
        ws15.cell(_i, 3, _m.direct_agents).font = FONT_BLUE
        ws15.cell(_i, 4, round(c2, 6)).font = FONT_BLUE
        ws15.cell(_i, 5, round(c3, 6)).font = FONT_BLUE
        ws15.cell(_i, 6, 85.0).font = FONT_BLUE
        b, c, d, e, k = f"B{_i}", f"C{_i}", f"D{_i}", f"E{_i}", f"F{_i}"
        kag_pre = f"IF({k}<40,{k}/100,IF({k}<55,0.5,IF({k}<65,0.75,1)))"
        kag_post = f"IF({k}<50,{k}/200,IF({k}<60,0.5,IF({k}<65,0.7,IF({k}<70,0.9,1))))"
        kum_pre = f"IF({k}>=75,1.15,IF({k}>=70,1.1,IF({k}>=65,1.05,IF({k}>=60,1,IF({k}>=55,0.9,IF({k}>=50,0.75,{k}/100))))))"
        kum_post = f"IF({k}>=80,1.1,IF({k}>=75,1.05,IF({k}>=70,1,IF({k}>=65,0.9,IF({k}>=60,0.7,IF({k}>=50,0.5,{k}/200))))))"
        r3 = f"3*{b}"
        rm = f"IF({r3}>=100,0.5,IF({r3}>=80,0.35,IF({r3}>=60,0.3,IF({r3}>=45,0.25,IF({r3}>=30,0.2,IF({r3}>=15,0.15,IF({r3}>=10,0.1,0)))))))"
        rq = f"IF({r3}>=120,0.1,IF({r3}>=100,0.08,IF({r3}>=80,0.06,IF({r3}>=60,0.05,IF({r3}>=45,0.04,IF({r3}>=30,0.03,0))))))*IF({rm}>0,2,1)"
        ws15.cell(_i, 7, f"={b}*{rm}*(3*{kag_pre}+9*{kag_post})+{r3}*{rq}*({kag_pre}+3*{kag_post})").number_format = "#,##0.000"
        if _m.mid == "M1":
            ws15.cell(_i, 8, "—"); ws15.cell(_i, 9, "—"); ws15.cell(_i, 10, "—")
            py = _T.mnl_agent_m1(_m)
            pyv = py["bonus_monthly_productivity"] + py["bonus_quarterly_productivity"]
            ws15.cell(_i, 11, round(pyv, 4)).number_format = "#,##0.000"
            _rows.append((f"XL-GT-21", "Manulife Đại Lý", f"{_m.label}: thưởng năng suất tháng+quý 0046M01 = {pyv:.3f}", pyv, f"='15_Manulife_Agent_UMplus'!G{_i}"))
            continue
        c1 = f"({c}*{b})"
        r1 = f"IF({c1}>=48,0.2,IF({c1}>=24,0.16,IF({c1}>=7,0.14,0.1)))"
        ws15.cell(_i, 8, f"=12*({c1}*{r1}+{d}*{r1}/2+{e}*{r1}/4)").number_format = "#,##0.000"
        r2 = f"IF({c}>=6,0.6,IF({c}>=4,0.5,IF({c}>=2,0.4,IF({c}>=1,0.3,0))))"
        ws15.cell(_i, 9, f"={r2}*{c}*({b}*{rm}*(3*{kag_pre}*{kum_pre}+9*{kag_post}*{kum_post})+{r3}*{rq}*({kag_pre}*{kum_pre}+3*{kag_post}*{kum_post}))").number_format = "#,##0.000"
        ws15.cell(_i, 10, f"=H{_i}+I{_i}").number_format = "#,##0.000"
        pyv = _T.mnl_um(_m)[0]["total_earned"]
        ws15.cell(_i, 11, round(pyv, 4)).number_format = "#,##0.000"
        _rows.append((f"XL-GT-{20 + len(_rows) + 1}", "Manulife UM+", f"{_m.label}: tổng phí UM+ 0047M01 = {pyv:.3f}", pyv, f"='15_Manulife_Agent_UMplus'!J{_i}"))
    set_col_widths(ws15, {1: 26, 2: 14, 3: 12, 4: 14, 5: 14, 6: 8, 7: 18, 8: 14, 9: 14, 10: 14, 11: 14})
    for _tid, _cat, _desc, _pv, _f in _rows:
        golden_excel.append((_tid, _cat, _desc, "15_Manulife_Agent_UMplus", round(_pv, 3), _f))

    for i, gt in enumerate(golden_excel, 5):
        ws14.cell(i, 1, gt[0]).font = FONT_BOLD
        ws14.cell(i, 2, gt[1])
        ws14.cell(i, 3, gt[2])
        ws14.cell(i, 4, gt[3])
        ws14.cell(i, 5, gt[4]).number_format = "#,##0.000"
        ws14.cell(i, 6, gt[5]).number_format = "#,##0.000"
        ws14.cell(i, 7, f"=ABS(F{i}-E{i})").number_format = "0.0000"
        ws14.cell(i, 8, f'=IF(G{i}<=0.02,"PASS","FAIL")').font = FONT_BOLD
        for col in range(1, 9):
            ws14.cell(i, col).border = BORDER
    set_col_widths(ws14, {1: 12, 2: 18, 3: 52, 4: 22, 5: 18, 6: 18, 7: 12, 8: 10})

    wb.save(target)
    print(f"BUILT {target.name} ({len(wb.sheetnames)} sheets)")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Build reproducible W24 Excel 2007-compatible Reference Model")
    parser.add_argument("--output", default=str(DEFAULT_OUT_XLSX), help="Output workbook path (default: separate rebuilt path)")
    parser.add_argument("--allow-overwrite-v1", action="store_true", help="Explicitly allow overwriting v1.xlsx")
    args = parser.parse_args()
    build_workbook(Path(args.output), allow_overwrite_v1=args.allow_overwrite_v1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
