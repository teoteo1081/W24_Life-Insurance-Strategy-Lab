# W24 — Life Insurance Strategy Lab

**Vietnam Life Insurance Agency Compensation Benchmarking, Policy Research Prototype & Modeling Workspace**

> **Primary Business Anchor (Verbatim — Step 1 Requirement, `SRC-REQ-001`):**  
> *"Bước 1: Phân tích các chính sách thu nhập giữa các công ty, và đề xuất chính sách phù hợp tại thị trường VN, nhằm thúc đẩy gia tăng doanh số, chất lượng kinh doanh và hiệu quả về mặt chi phí (ROI)."*

---

## 1. Project Scope & Current State (Single Source of Truth)

This repository is an **organized research prototype and reproducible Python/Excel modeling workspace** supporting Step 1 strategic advisory for Vietnam life insurance agency compensation.

- **Business Owner:** TJ
- **Implementation Agent:** AGY | **Independent Auditor:** Codex (latest audited checkpoint: `5cb7a21`)
- **Current Demonstrated Maturity:** **Level 1 (Organized)** independently audited at `5cb7a21`; **Level 2 (Reproducible)** hardening completed and **`SELF_VERIFIED`** in this sprint (pending Independent Audit Round 3 by Codex). See [qa/repository-maturity-assessment.md](qa/repository-maturity-assessment.md).

### Single Source of Truth Map
| Information Type | Authoritative File |
|---|---|
| Immutable business ask & P0/P1/P2 scope | [ANCHOR_SPEC.md](ANCHOR_SPEC.md) |
| Current operational state, test counts & next actions | [HANDOVER.md](HANDOVER.md) |
| Open/closed Business Owner decisions (`DEC-01..10`) | [docs/decisions/decision-register.md](docs/decisions/decision-register.md) |
| Chronological change history | [CHANGELOG.md](CHANGELOG.md) |
| Dated QA, remediation & Excel verification evidence | [qa/post-audit-remediation-register.md](qa/post-audit-remediation-register.md) & [qa/excel-reproducibility-evidence.json](qa/excel-reproducibility-evidence.json) |
| Confidentiality, IP & source-rights rules | [docs/governance/confidentiality-and-rights-policy.md](docs/governance/confidentiality-and-rights-policy.md) |

---

## 2. Current Capabilities vs. Honest Limitations

### Implemented & Tested Capabilities (`SELF_VERIFIED`)
- **Policy Knowledge & Inventories:** 7 analyzed 2026 policy circulars (`116` pages across AIA Alpha 3 tiers, Chubb Life Agency 3 tiers, Manulife Senior Management `PSM+/HKD`), **112 atomic rules** (`business-rules-catalog.csv` with 3-state verification tracking), **3 normalized CSV lookups** (`1,300` AIA PAF+ rows, `113` Chubb product commission rows, `10` HSBH age-band rows), **36 mapped roles**, and **44 Total Rewards components** (separating cash, deferred, and unpriced non-cash benefits).
- **12-Month Python Compensation & Distribution Cost Engine:** [model/compensation/compensation_engine.py](model/compensation/compensation_engine.py) with strict input validation (rejects `NaN`, `±Inf`, invalid types/ranges/dates, silent `UNKNOWN→1.0` conversion), conflict toggles (`ERR-DOC-01`, `ERR-DOC-02`), dual-phase date switches, symmetric negative FYC clawbacks, 12B FYP Enterprise Distribution Cost stacking (zero double-counting), MAPA forward/reverse, and modeled break-even margin calculations.
- **Reproducible Excel 2007-Compatible Workbook Build:** [scripts/build_workbook.py](scripts/build_workbook.py) rebuilds the 14-sheet reference model from tracked CSVs into a separate test path without overwriting `v1.xlsx`; [scripts/verify_workbook_excel.py](scripts/verify_workbook_excel.py) verifies live Microsoft Excel COM recalculation, input perturbation, and Python parity.
- **Automated Quality Gates & Standard `unittest` Discovery:** One command (`python scripts/run_checks.py`) validates repository integrity, runs all discovered unit/golden/regression tests, and executes the example scenario.
- **Executive Deliverable (Package A):** 7-page executive brief at [outputs/interview/W24_Executive_Recommendation_Step1.md](outputs/interview/W24_Executive_Recommendation_Step1.md).

### Current Limitations (Explicit Disclosures)
- **Partial Competitor Coverage:** Manulife Individual Agent (`FA`) and Mid-Manager (`UM/SUM/DM`), AIA Commission Appendix & `Exchange/Pro` allowances, and Chubb `CHH0DCEB260005V`/`BD` policy are **`UNKNOWN` / `MISSING_DEPENDENCY`**.
- **Modeled Thresholds ≠ Actual ROI:** All financial outputs represent **modeled payout, modeled distribution cost, and modeled break-even gross margin** under explicit scenario assumptions (`12B FYP` region, `OpEx 15–25%`), **NOT observed sales/quality uplift or realized ROI** (actual insurer `VNB Margin`, `OpEx`, and cohort mix are `UNKNOWN`).
- **Legal Verification Conditional:** Official Government Portal metadata is tracked for `TT 67/2023`, `NĐ 97/2026`, `TT 96/2026`, and Consolidated Circular `44/2026/VBHN-TT-BTC`, but clause-level legal text remains **`SOURCE_NOT_VERIFIED`** pending legal owner review (`DEC-03`).
- **Architecture Not Yet Configuration-Driven (Level 3/4):** `business-rules-catalog.csv` and `schemas/compensation-scheme.schema.json` are currently validation/design contracts, not runtime engine drivers; adding a new insurer requires code/adapter changes (see [docs/architecture/level3-level4-architecture-advisory.md](docs/architecture/level3-level4-architecture-advisory.md)).
- **Document Rights & Public Hosting Notice:** Per explicit Business Owner decision (`DEC-07`), this repository is hosted `PUBLIC`. **Public hosting does NOT imply public redistribution rights for third-party issuer PDFs** in `private/sources/`. Every source carries an explicit `Redistribution_Rights_Status` (`RESTRICTED_INTERNAL` for Manulife `0048M01`; `PERMISSION_UNKNOWN` for AIA/Chubb circulars) in `knowledge/sources/source-registry.csv` pending rights resolution (`DEC-08`).

---

## 3. Environment Setup & Quick Start

### Prerequisites
- **Python 3.12+** (core engine, quality gates, and `unittest` suite use **Python standard library only**).
- **`openpyxl >= 3.1.0`** (only required to build or inspect `.xlsx` workbooks):
  ```bash
  pip install -r requirements.txt
  ```
- **Optional (Windows only):** Microsoft Excel (tested on Excel 12.0 / 2007 COM) for live `.xlsx` recalculation and perturbation verification.

### One-Command Verification (Quality Gates + All Tests + Example Run)
```bash
python scripts/run_checks.py
```

### Standard `unittest` Discovery Only
```bash
python -m unittest discover -s tests -v
```

### Run Example Scenario Directly
```bash
python model/compensation/compensation_engine.py
```

### Rebuild & Verify the Excel Reference Model (Without Overwriting `v1.xlsx`)
```bash
python scripts/build_workbook.py --output outputs/working/W24_Compensation_Reference_Model_rebuilt.xlsx
python scripts/verify_workbook_excel.py --workbook outputs/working/W24_Compensation_Reference_Model_rebuilt.xlsx
```

---

## 4. Repository Map

```text
W24_Life-Insurance-Strategy-Lab/
├── README.md                                 # Public overview, limitations & quick start
├── ANCHOR_SPEC.md                            # Verbatim Step 1 business anchor & P0/P1/P2 scope
├── HANDOVER.md                               # Current operational state & handover entry point
├── AGENTS.md                                 # Role boundaries & evidence rules
├── CHANGELOG.md                              # Chronological version log
├── requirements.txt                          # Python dependencies (stdlib core + openpyxl)
├── docs/
│   ├── architecture/                         # Conceptual schema, bottom-up spec & Level 3/4 advisory
│   ├── decisions/decision-register.md        # Open & closed Business Owner decisions
│   ├── governance/confidentiality-and-rights-policy.md
│   ├── research/                             # Legal wheel-check, VN market suitability, strategy, backlog
│   └── specifications/                       # 15-criteria evaluation framework & rubric (DRAFT)
├── knowledge/
│   ├── business-rules/business-rules-catalog.csv  # 112 atomic rules (3-state verification)
│   ├── compensation/                         # 44-component Total Rewards inventory (33 fields)
│   ├── lookups/                              # Normalized CSV lookups (PAF+ 1,300; Chubb 113; HSBH 10)
│   ├── policies/                             # 3 deep policy guides, cross-doc map & 36-role mapping
│   └── sources/source-registry.csv           # 17 sources with SHA-256, Revision_Class & Rights Status
├── model/compensation/compensation_engine.py # Validated 12M Python compensation & cost engine
├── scripts/
│   ├── run_checks.py                         # Single-command validation + tests + example runner
│   ├── validate_repo.py                      # Automated data, reference, lookup & hygiene gates
│   ├── build_workbook.py                     # Reproducible 14-sheet Excel 2007 workbook generator
│   ├── recalc_excel_com.ps1                  # Windows Excel COM recalculation helper
│   └── verify_workbook_excel.py              # Live COM recalc, input perturbation & parity verifier
├── tests/                                    # Auto-discovered unittest golden, validation & gate suites
├── outputs/
│   ├── interview/W24_Executive_Recommendation_Step1.md  # Package A (7-page executive brief)
│   └── working/                              # Benchmarking v2.0, strategy, Excel reference workbooks
└── qa/                                       # Coverage matrix, remediation register, maturity & JSON evidence
```

---

## 5. Handover Entry Point (Cold Start for Humans or AI Agents)

1. Read [HANDOVER.md](HANDOVER.md) for the single authoritative current status, test counts, and pending decisions.
2. Read [ANCHOR_SPEC.md](ANCHOR_SPEC.md) and [AGENTS.md](AGENTS.md) for scope and evidence rules.
3. Run `python scripts/run_checks.py` to confirm your local environment reproduces all gates and tests cleanly before making any change.
