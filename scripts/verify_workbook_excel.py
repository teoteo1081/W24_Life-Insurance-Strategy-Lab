"""
W24 Reproducible Workbook Verification & Excel COM Perturbation Audit (Sections 13 & 14).

Verifies on TEMPORARY COPIES (never mutating outputs/working/W24_Compensation_Reference_Model_v1.xlsx):
1. Structural audit: sheet count, formula count, zero formula errors across all sheets.
2. Live Microsoft Excel COM recalculation (`CalculateFullRebuild`) via `scripts/recalc_excel_com.ps1`.
3. All 20 Live Excel Golden Tests on `14_QA_Golden_Tests` == PASS.
4. All 12 Enterprise Cost scenarios on `11_Hierarchy_Dist_Cost` == 100% parity vs Python engine.
5. LIVE INPUT PERTURBATION PROOF IN EXCEL COM:
   - Mutates `'04_Policy_Parameters'!C19` from 0.16 -> 0.20 and `'04_Policy_Parameters'!C5`
     from "Table_80" -> "Example_50", recalculates in Excel COM, and proves cached outputs
     dynamically change to match Python engine!
6. Functional equivalence check between rebuilt workbook and original tracked v1.xlsx.

Usage:
    python scripts/verify_workbook_excel.py --workbook <path_to_rebuilt.xlsx> [--write-evidence qa/excel-reproducibility-evidence.json]
"""

from __future__ import annotations

import argparse
import datetime
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import openpyxl

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from model.compensation.compensation_engine import (
    ProposalParams,
    calc_chubb_ch_m1_12_offset,
    calc_enterprise_hierarchy_cost,
    calc_proposal_agent_12m,
)

EXCEL_ERRORS = {"#REF!", "#NAME?", "#VALUE!", "#DIV/0!", "#N/A", "#NUM!", "#NULL!"}


def run_excel_com(xlsx_path: Path) -> str:
    ps1 = REPO_ROOT / "scripts/recalc_excel_com.ps1"
    proc = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps1), "-WorkbookPath", str(xlsx_path.resolve())],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0 or "EXCEL_RECALC_SAVE_OK=True" not in proc.stdout:
        raise RuntimeError(f"Excel COM recalculation failed (rc={proc.returncode}):\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    ver = "UNKNOWN"
    for line in proc.stdout.splitlines():
        if line.startswith("EXCEL_COM_VERSION="):
            ver = line.split("=", 1)[1].strip()
    return ver


def inspect_workbook(xlsx_path: Path) -> dict:
    wb_f = openpyxl.load_workbook(xlsx_path, data_only=False)
    formula_count = 0
    for sn in wb_f.sheetnames:
        ws = wb_f[sn]
        for r in range(1, ws.max_row + 1):
            for c in range(1, ws.max_column + 1):
                v = ws.cell(r, c).value
                if isinstance(v, str) and v.startswith("="):
                    formula_count += 1
    sheets = list(wb_f.sheetnames)
    wb_f.close()

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    err_cells = []
    for sn in wb.sheetnames:
        ws = wb[sn]
        for r in range(1, ws.max_row + 1):
            for c in range(1, ws.max_column + 1):
                v = ws.cell(r, c).value
                if isinstance(v, str) and (v in EXCEL_ERRORS or v.startswith("#")):
                    err_cells.append(f"{sn}!{openpyxl.utils.get_column_letter(c)}{r}={v}")

    ws14 = wb["14_QA_Golden_Tests"]
    gt_pass = 0
    gt_fail = 0
    gt_values = {}
    for r in range(5, 25):
        tid = ws14.cell(r, 1).value
        st = ws14.cell(r, 8).value
        gt_values[tid] = ws14.cell(r, 6).value
        if st == "PASS":
            gt_pass += 1
        else:
            gt_fail += 1

    ws11 = wb["11_Hierarchy_Dist_Cost"]
    parity_pass = 0
    parity_fail = 0
    ent_values = {}
    row_idx = 5
    for k2v in (82.0, 72.0, 62.0):
        for sc in ("AIA_Alpha_2026", "AIA_Alpha_2027", "Chubb_Agency_2026", "W24_Proposed_Balanced"):
            py_res = calc_enterprise_hierarchy_cost(sc, k2_pct=k2v)
            xl_e = round(float(ws11.cell(row_idx, 11).value) * 100.0, 2)
            xl_c = round(float(ws11.cell(row_idx, 12).value) * 100.0, 2)
            xl_a = round(float(ws11.cell(row_idx, 13).value) * 100.0, 2)
            ent_values[f"{sc}@{int(k2v)}"] = {"earned": xl_e, "cash_y1": xl_c, "art52": xl_a}
            ok = (
                abs(xl_e - py_res["earned_pct_fyp"]) <= 0.02
                and abs(xl_c - py_res["cash_y1_pct_fyp"]) <= 0.02
                and abs(xl_a - py_res["art52_bonus_pct_fyp"]) <= 0.02
            )
            if ok:
                parity_pass += 1
            else:
                parity_fail += 1
            row_idx += 1
    wb.close()
    return {
        "sheet_count": len(sheets),
        "sheets": sheets,
        "formula_count": formula_count,
        "error_cells": err_cells,
        "golden_pass": gt_pass,
        "golden_fail": gt_fail,
        "golden_values": gt_values,
        "parity_pass": parity_pass,
        "parity_fail": parity_fail,
        "enterprise_values": ent_values,
    }


def run_perturbation_test(source_xlsx: Path) -> dict:
    """Mutate 2 inputs in a temp copy, recalc in Excel COM, prove live dynamic parity vs Python."""
    with tempfile.TemporaryDirectory() as td:
        mut_path = Path(td) / "perturbed_temp.xlsx"
        shutil.copy2(source_xlsx, mut_path)
        wb = openpyxl.load_workbook(mut_path, data_only=False)
        ws4 = wb["04_Policy_Parameters"]
        ws4["C19"].value = 0.20          # Proposal Monthly Tier 2 rate: 0.16 -> 0.20
        ws4["C5"].value = "Example_50"   # Chubb ERR-DOC-01 toggle: Table_80 -> Example_50
        wb.save(mut_path)
        wb.close()

        ver = run_excel_com(mut_path)
        wb_d = openpyxl.load_workbook(mut_path, data_only=True)
        xl_prop_earned_pct = round(float(wb_d["11_Hierarchy_Dist_Cost"]["K8"].value) * 100.0, 2)
        xl_prop_art52_pct = round(float(wb_d["11_Hierarchy_Dist_Cost"]["M8"].value) * 100.0, 2)
        xl_ch_m12_net = round(float(wb_d["08_Indiv_Comp_12M"]["J19"].value), 4)
        wb_d.close()

    # Independent Python expected under perturbed inputs:
    p_mut = ProposalParams(agent_m_tier_rates=(0.08, 0.20, 0.24, 0.32, 0.38))
    ag_mut = calc_proposal_agent_12m([15.0] * 12, [0.0] * 12, k2_pct=82.0, params=p_mut)
    # Delta in 20-agent bonus: (ag_mut["total_bonuses_earned"]*20 - base 709.632) / 12000
    py_art52_mut = round((ag_mut["total_bonuses_earned"] * 20.0 / 12000.0) * 100.0, 2)
    base_ent = calc_enterprise_hierarchy_cost("W24_Proposed_Balanced", k2_pct=82.0)
    delta_bonus = ag_mut["total_bonuses_earned"] * 20.0 - base_ent["layer_b_agent_bonuses"]
    py_earned_mut = round(((base_ent["total_earned_vnd_m"] + delta_bonus) / 12000.0) * 100.0, 2)
    py_ch_m12_ex = calc_chubb_ch_m1_12_offset(12, 3, 85.0, 80.0, 1.5, conflict_mode="Example_50")["ch_month_net"]

    ok_earned = abs(xl_prop_earned_pct - py_earned_mut) <= 0.02
    ok_art52 = abs(xl_prop_art52_pct - py_art52_mut) <= 0.02
    ok_toggle = abs(xl_ch_m12_net - py_ch_m12_ex) <= 0.01
    return {
        "excel_com_version": ver,
        "perturbation_1_proposal_tier2_0.16_to_0.20": {
            "excel_earned_pct": xl_prop_earned_pct,
            "python_earned_pct": py_earned_mut,
            "excel_art52_pct": xl_prop_art52_pct,
            "python_art52_pct": py_art52_mut,
            "pass": ok_earned and ok_art52,
        },
        "perturbation_2_err_doc_01_table80_to_example50": {
            "excel_ch_m12_net": xl_ch_m12_net,
            "python_ch_m12_net": py_ch_m12_ex,
            "pass": ok_toggle,
        },
        "all_perturbations_pass": ok_earned and ok_art52 and ok_toggle,
    }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--workbook", required=True, help="Path to workbook to verify on temp copy")
    parser.add_argument("--compare-v1", default=str(REPO_ROOT / "outputs/working/W24_Compensation_Reference_Model_v1.xlsx"))
    parser.add_argument("--write-evidence", default="", help="Optional JSON evidence output path")
    args = parser.parse_args()

    src_wb = Path(args.workbook).resolve()
    if not src_wb.exists():
        print(f"ERROR: Workbook not found: {src_wb}")
        return 1

    with tempfile.TemporaryDirectory() as td:
        tmp_wb = Path(td) / "recalc_copy.xlsx"
        shutil.copy2(src_wb, tmp_wb)
        excel_ver = run_excel_com(tmp_wb)
        base_audit = inspect_workbook(tmp_wb)

    pert = run_perturbation_test(src_wb)

    # Functional equivalence comparison vs tracked v1.xlsx (if present)
    v1_path = Path(args.compare_v1).resolve()
    func_equiv = None
    if v1_path.exists():
        v1_audit = inspect_workbook(v1_path)
        same_sheets = base_audit["sheets"] == v1_audit["sheets"]
        same_gt = all(
            abs(float(base_audit["golden_values"][k]) - float(v1_audit["golden_values"][k])) <= 0.01
            for k in base_audit["golden_values"]
        )
        same_ent = base_audit["enterprise_values"] == v1_audit["enterprise_values"]
        func_equiv = {
            "compared_against": "outputs/working/W24_Compensation_Reference_Model_v1.xlsx",
            "same_sheet_names": same_sheets,
            "rebuilt_formula_count": base_audit["formula_count"],
            "v1_formula_count": v1_audit["formula_count"],
            "same_20_golden_values": same_gt,
            "same_12_enterprise_cost_values": same_ent,
            "functional_reproducibility_pass": same_sheets and same_gt and same_ent,
            "note": "Functional reproducibility verified; byte-for-byte XLSX hash differs due to zip timestamps/metadata.",
        }

    overall_pass = (
        len(base_audit["error_cells"]) == 0
        and base_audit["golden_fail"] == 0
        and base_audit["parity_fail"] == 0
        and pert["all_perturbations_pass"]
        and (func_equiv is None or func_equiv["functional_reproducibility_pass"])
    )

    report = {
        "verification_timestamp_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verification_status": "SELF_VERIFIED",
        "excel_com_version": excel_ver,
        "workbook_relative_name": src_wb.name,
        "sheet_count": base_audit["sheet_count"],
        "formula_count": base_audit["formula_count"],
        "excel_error_cells_count": len(base_audit["error_cells"]),
        "golden_tests_pass": base_audit["golden_pass"],
        "golden_tests_fail": base_audit["golden_fail"],
        "enterprise_parity_pass": base_audit["parity_pass"],
        "enterprise_parity_fail": base_audit["parity_fail"],
        "live_input_perturbation": pert,
        "functional_equivalence_vs_v1": func_equiv,
        "overall_pass": overall_pass,
    }

    if args.write_evidence:
        ev_path = Path(args.write_evidence)
        ev_path.parent.mkdir(parents=True, exist_ok=True)
        ev_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
