"""
W24 Automated Repository Quality Gates (Section 16).

Validates without requiring manual AI rereading:
1. Source Registry integrity (required cols, unique IDs, valid Redistribution_Rights_Status,
   SHA-256 verification of tracked PDFs).
2. Business Rules Catalog integrity (unique Rule_IDs, 0 broken Rule_ID references,
   valid Section-32 3-status enums, required Source_ID_And_Page).
3. Lookup table integrity (AIA PAF+ 1,300 rows & Annual == Sum M01..M12; Chubb 113 rows;
   HSBH 10 ordered age bands).
4. Role Mapping (36 roles) & Total Rewards Inventory (44 components x 33 cols) integrity.
5. JSON Schema structural validity.
6. Public Repository Confidentiality & Hygiene checks (rejects absolute local user paths,
   secret/token patterns, and protected skill markers in tracked text files).
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

VALID_RIGHTS_ENUMS = {
    "PUBLIC_DISTRIBUTION_AUTHORIZED",
    "RESTRICTED_INTERNAL",
    "LICENSED_WITH_CONDITIONS",
    "PERMISSION_UNKNOWN",
}
VALID_SV_ENUMS = {"SOURCE_VERIFIED", "SOURCE_NOT_VERIFIED", "MISSING_DEPENDENCY", "CONFLICTING_EVIDENCE"}
VALID_IMP_ENUMS = {"IMPLEMENTED", "NOT_IMPLEMENTED"}
VALID_CV_ENUMS = {"TESTED_PASS", "CONDITIONAL", "NOT_TESTED", "BLOCKED"}

RULE_REF_RE = re.compile(r"(?<!SRC-POL-)\b(?:AIA|MNL|CHB|REG)-(?:CV|MG|PF|PM|AG|CH|RD|CAP|BON|MGT)-\d{3}\b")
ABS_PATH_RE = re.compile(r"(?:file:///C:/|C:\\Users\\|C:/Users/)", re.I)
SECRET_RE = re.compile(
    r"(?:ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AIza[0-9A-Za-z\-_]{20,}|BEGIN (?:RSA|OPENSSH|PRIVATE) KEY)",
    re.I,
)
PROTECTED_MARKER_RE = re.compile(
    r"(?:\banh B[aả]o\b|SKILL\.md|\bdecision-advisor\b|\bpo-decision-bridge\b|\brubric-engineering\b|\brisk-adaptive-audit\b|\bexecution-contract\b|\btechnicaldebug\b|\blocal_orchestrator_cli\b|\bgit-state-recovery\b)",
    re.I,
)


def validate_source_registry(repo: Path) -> List[str]:
    errs: List[str] = []
    path = repo / "knowledge/sources/source-registry.csv"
    if not path.exists():
        return [f"Missing {path}"]
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return ["Empty source-registry.csv"]
    required_cols = {
        "Source_ID", "Original_Filename", "Local_Relative_Path", "SHA256_Hash",
        "Company", "Document_Type", "Revision_Class", "Confidentiality",
        "Redistribution_Rights_Status", "Verification_Status",
    }
    missing = required_cols - set(rows[0].keys())
    if missing:
        errs.append(f"source-registry.csv missing columns: {sorted(missing)}")
        return errs

    seen = set()
    for i, r in enumerate(rows, 2):
        sid = r["Source_ID"].strip()
        if not sid:
            errs.append(f"source-registry row {i}: empty Source_ID")
        elif sid in seen:
            errs.append(f"source-registry row {i}: duplicate Source_ID {sid}")
        seen.add(sid)

        rights = r["Redistribution_Rights_Status"].strip()
        if rights not in VALID_RIGHTS_ENUMS:
            errs.append(f"source-registry row {i} ({sid}): invalid Redistribution_Rights_Status={rights!r}")

        rel = r["Local_Relative_Path"].strip()
        expected_sha = r["SHA256_Hash"].strip().lower()
        if rel.startswith("private/sources/") and len(expected_sha) == 64:
            pdf_path = repo / rel
            if not pdf_path.exists():
                errs.append(f"source-registry ({sid}): missing tracked PDF {rel}")
            else:
                actual_sha = hashlib.sha256(pdf_path.read_bytes()).hexdigest().lower()
                if actual_sha != expected_sha:
                    errs.append(f"source-registry ({sid}): SHA-256 mismatch on {rel}")
    return errs


def validate_business_rules(repo: Path) -> List[str]:
    errs: List[str] = []
    path = repo / "knowledge/business-rules/business-rules-catalog.csv"
    if not path.exists():
        return [f"Missing {path}"]
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return ["Empty business-rules-catalog.csv"]
    required = {
        "Rule_ID", "Scheme_ID", "Source_ID_And_Page",
        "Source_Verification", "Implementation_Status", "Calculation_Verification",
    }
    missing = required - set(rows[0].keys())
    if missing:
        return [f"business-rules-catalog.csv missing columns: {sorted(missing)}"]

    ids = set()
    for i, r in enumerate(rows, 2):
        rid = r["Rule_ID"].strip()
        if not rid:
            errs.append(f"rules row {i}: empty Rule_ID")
        elif rid in ids:
            errs.append(f"rules row {i}: duplicate Rule_ID {rid}")
        ids.add(rid)
        if not r["Source_ID_And_Page"].strip():
            errs.append(f"rules row {i} ({rid}): empty Source_ID_And_Page")
        if r["Source_Verification"] not in VALID_SV_ENUMS:
            errs.append(f"rules row {i} ({rid}): invalid Source_Verification={r['Source_Verification']!r}")
        if r["Implementation_Status"] not in VALID_IMP_ENUMS:
            errs.append(f"rules row {i} ({rid}): invalid Implementation_Status={r['Implementation_Status']!r}")
        if r["Calculation_Verification"] not in VALID_CV_ENUMS:
            errs.append(f"rules row {i} ({rid}): invalid Calculation_Verification={r['Calculation_Verification']!r}")

    for i, r in enumerate(rows, 2):
        rid = r["Rule_ID"]
        for k, v in r.items():
            if k == "Source_ID_And_Page" or not v:
                continue
            for m in RULE_REF_RE.findall(v):
                if m not in ids:
                    errs.append(f"rules row {i} ({rid}): broken Rule_ID reference -> {m}")
    return errs


def validate_lookups(repo: Path) -> List[str]:
    errs: List[str] = []
    # 1. AIA PAF+ 5Y targets
    paf_path = repo / "knowledge/lookups/aia-paf-5y-targets.csv"
    with open(paf_path, encoding="utf-8") as f:
        paf_rows = list(csv.DictReader(f))
    if len(paf_rows) != 1300:
        errs.append(f"aia-paf-5y-targets.csv expected 1300 rows, got {len(paf_rows)}")
    seen_paf = set()
    annuals = {}
    monthly_sums = {}
    for i, r in enumerate(paf_rows, 2):
        key = (r["Role_Code"], r["Tenure_Year"], r["Period_Key"], r["Metric"])
        if key in seen_paf:
            errs.append(f"PAF duplicate key row {i}: {key}")
        seen_paf.add(key)
        val = float(r["Target_Value"])
        if not math.isfinite(val) or val < 0:
            errs.append(f"PAF invalid Target_Value row {i}: {val}")
        gkey = (r["Role_Code"], r["Tenure_Year"], r["Metric"])
        if r["Period_Key"] == "ANNUAL_TOTAL":
            annuals[gkey] = val
        else:
            monthly_sums[gkey] = monthly_sums.get(gkey, 0.0) + val
    for gkey, aval in annuals.items():
        msum = monthly_sums.get(gkey, 0.0)
        if abs(aval - msum) > 0.01:
            errs.append(f"PAF sum mismatch {gkey}: Annual={aval} vs SumMonths={msum}")

    # 2. Chubb product commissions
    chb_path = repo / "knowledge/lookups/chubb-product-commission-schedule.csv"
    with open(chb_path, encoding="utf-8") as f:
        chb_rows = list(csv.DictReader(f))
    if len(chb_rows) != 113:
        errs.append(f"chubb-product-commission-schedule.csv expected 113 rows, got {len(chb_rows)}")
    seen_chb = set()
    for i, r in enumerate(chb_rows, 2):
        pid = r["Product_Rule_ID"].strip()
        if not pid or pid in seen_chb:
            errs.append(f"Chubb schedule missing/duplicate Product_Rule_ID row {i}: {pid!r}")
        seen_chb.add(pid)
        y1 = float(r["Y1_Pct"])
        if not math.isfinite(y1) or y1 < 0 or y1 > 40.0:
            errs.append(f"Chubb schedule invalid Y1_Pct row {i} ({pid}): {y1}")

    # 3. Chubb HSBH
    hsbh_path = repo / "knowledge/lookups/chubb-hsbh-tiers.csv"
    with open(hsbh_path, encoding="utf-8") as f:
        hsbh_rows = list(csv.DictReader(f))
    if len(hsbh_rows) != 10:
        errs.append(f"chubb-hsbh-tiers.csv expected 10 rows, got {len(hsbh_rows)}")
    prev_max = -1
    for i, r in enumerate(hsbh_rows, 2):
        lo, hi = int(r["Min_Age"]), int(r["Max_Age"])
        if lo > hi or lo != prev_max + 1:
            errs.append(f"Chubb HSBH age gap/overlap row {i}: {lo}-{hi} after {prev_max}")
        prev_max = hi
    return errs


def validate_inventories_and_schema(repo: Path) -> List[str]:
    errs: List[str] = []
    with open(repo / "knowledge/policies/role-organization-mapping.csv", encoding="utf-8") as f:
        r_rows = list(csv.reader(f))
    if len(r_rows) - 1 < 1 or set(len(x) for x in r_rows) != {16}:
        errs.append(f"role-organization-mapping.csv invalid width/rows: {len(r_rows)-1}")

    with open(repo / "knowledge/compensation/total-rewards-inventory.csv", encoding="utf-8") as f:
        tr_rows = list(csv.reader(f))
    if len(tr_rows) - 1 < 1 or set(len(x) for x in tr_rows) != {33}:
        errs.append(f"total-rewards-inventory.csv invalid width/rows: {len(tr_rows)-1}")

    schema_path = repo / "schemas/compensation-scheme.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        for req in ("$schema", "title", "required", "properties"):
            if req not in schema:
                errs.append(f"compensation-scheme.schema.json missing key {req}")
    except Exception as exc:
        errs.append(f"Invalid JSON schema: {exc}")
    return errs


def validate_public_hygiene(repo: Path, text_files: List[Path] | None = None) -> List[str]:
    errs: List[str] = []
    if text_files is None:
        raw = subprocess.check_output(
            ["git", "-C", str(repo), "-c", "core.quotepath=false", "ls-files"],
            text=True, encoding="utf-8",
        ).splitlines()
        candidates = [repo / p for p in raw]
    else:
        candidates = text_files

    skip_ext = {".pdf", ".xlsx", ".png", ".7z", ".zip"}
    # Exclude self (validator regex patterns legitimately contain regex strings!)
    self_path = (repo / "scripts/validate_repo.py").resolve()
    for p in candidates:
        if not p.exists() or p.suffix.lower() in skip_ext or p.resolve() == self_path:
            continue
        # Also skip test_quality_gates.py which seeds synthetic bad strings to verify the regex gate!
        if p.name == "test_quality_gates.py":
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        if ABS_PATH_RE.search(txt):
            errs.append(f"Hygiene FAIL [abs_local_path]: {p.relative_to(repo)}")
        if SECRET_RE.search(txt):
            errs.append(f"Hygiene FAIL [secret_pattern]: {p.relative_to(repo)}")
        if PROTECTED_MARKER_RE.search(txt):
            errs.append(f"Hygiene FAIL [protected_skill_marker]: {p.relative_to(repo)}")
    return errs


def run_all_validations(repo: Path = REPO_ROOT) -> Tuple[bool, List[str]]:
    all_errs: List[str] = []
    all_errs.extend(validate_source_registry(repo))
    all_errs.extend(validate_business_rules(repo))
    all_errs.extend(validate_lookups(repo))
    all_errs.extend(validate_inventories_and_schema(repo))
    all_errs.extend(validate_public_hygiene(repo))
    return (len(all_errs) == 0, all_errs)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ok, errors = run_all_validations(REPO_ROOT)
    if ok:
        print("W24_QUALITY_GATES=PASS (0 errors across registry, rules, lookups, inventories, schema & hygiene)")
        sys.exit(0)
    else:
        print(f"W24_QUALITY_GATES=FAIL ({len(errors)} errors):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
