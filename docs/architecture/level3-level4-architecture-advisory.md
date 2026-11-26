# Architecture Advisory — Dependency Map, Level 3 Vertical Slice & Level 4 Extensibility Roadmap

**Status:** `PROPOSAL / ARCHITECTURE ADVISORY` *(Prepared during Level 2 Hardening Sprint — NOT implemented in Level 2; do NOT rewrite `compensation_engine.py` prematurely).*  
**Honest Current State (AS-IS):** `model/compensation/compensation_engine.py` is **partially parameterized** (reads normalized CSV lookups for AIA PAF+ and Chubb schedules, accepts `ProposalParams` dataclass and conflict toggles), **NOT yet configuration-driven**. `knowledge/business-rules/business-rules-catalog.csv` and `schemas/compensation-scheme.schema.json` are currently **governance/documentation contracts**, not runtime inputs. Adding a new company (e.g., Manulife FA/UM or Prudential) currently requires adding new Python functions, Excel formulas, and tests.

---

## 1. End-to-End Dependency Map (AS-IS)

| Layer | Tracked Asset | Consumed By (Runtime vs Manual) | Current Coupling Risk |
|---|---|---|---|
| **1. Sources** | `private/sources/*` + `knowledge/sources/source-registry.csv` | Validated at runtime by `scripts/validate_repo.py` (SHA-256 & rights enums); manually referenced by rules/docs | Low (hash-verified); redistribution rights tracked explicitly |
| **2. Rule Catalog** | `knowledge/business-rules/business-rules-catalog.csv` (112 rules) | Validated by `scripts/validate_repo.py` (IDs, refs, 3-state enums); **NOT loaded by `compensation_engine.py`** | Medium (documentation vs code drift possible without tests) |
| **3. JSON Schema** | `schemas/compensation-scheme.schema.json` | Validated structurally by `scripts/validate_repo.py`; **NOT executed by `compensation_engine.py`** | Medium (aspirational contract until Level 3) |
| **4. Normalized Lookups** | `knowledge/lookups/{aia-paf-5y-targets,chubb-product-commission-schedule,chubb-hsbh-tiers}.csv` | **Loaded at runtime** by BOTH `compensation_engine.py` AND `scripts/build_workbook.py` (Excel Sheets `05` & `06`) | Low (single CSV source shared by Python & Excel!) |
| **5. Parameters** | `ProposalParams` dataclass (Python) & Sheet `04_Policy_Parameters` (Excel) | Runtime inputs to proposal functions & Excel formulas; competitor rates still embedded in adapter code/formulas | Medium (parity enforced via `scripts/verify_workbook_excel.py`) |
| **6. Python Engine** | `model/compensation/compensation_engine.py` | Called by `tests/test_compensation_golden.py`, `tests/test_validation_and_regression.py`, `scripts/verify_workbook_excel.py` | Medium (fixed 4-scheme dispatch in `calc_enterprise_hierarchy_cost`) |
| **7. Workbook Builder** | `scripts/build_workbook.py` → `W24_Compensation_Reference_Model_rebuilt.xlsx` | Reproducible Python generator producing 14 Excel 2007 sheets; verified via `scripts/verify_workbook_excel.py` | Low for rebuildability; formula edits must stay synced with Python |
| **8. Tests & Gates** | `scripts/run_checks.py` (`validate_repo.py` + `unittest discover`) | Single-command automated regression & parity verification | High value (prevents silent drift) |
| **9. Advisory Outputs** | `outputs/interview/W24_Executive_Recommendation_Step1.md` & `outputs/working/*.md` | Manually synchronized Markdown reports backed by Python/Excel numbers | Medium (manual table sync until Level 3+ report generator) |

---

## 2. Classification of Values Inside `compensation_engine.py` (Section 17)

| Value Category | Concrete Examples in Current Code | Safe to Externalize to Config in Level 3? |
|---|---|---|
| **1. Mathematical Invariants** | `sum`, `min/max` cap/floor, `abs`, ratio division, `HalfUp` vs `RoundUp` operators, `30/30/40%` vesting split math, MAPA identity `M × A × P × A × Months` | Keep as **tested reusable Python operators** (never put raw code syntax in CSV/JSON). |
| **2. Policy-Specific Parameters** | AIA 8 quarterly tiers (`16..150M → 4..40%`), AIA FY 2026/2027 factor tables, Chubb AR/AL rolling 3M rates, Chubb K2 table, Manulife pre/post Apr-2026 K2 table & `30%/130%/150%` base bounds | **YES — high-value Level 3 candidates** (data-shaped tables with explicit `effective_date` & `source_id`). |
| **3. Scenario Inputs** | `monthly_fyc`, `monthly_syc`, `k2_pct`, `tenure_months_start`, `age`, `gender`, `hsbh`, `attendance_pct`, `sop_pct` | Always **runtime scenario inputs** (validated by typed input contract). |
| **4. Proposed Parameters** | `ProposalParams` rates, thresholds, K2 hard floor, deferral shares, RD base fee | **YES** — already isolated in `ProposalParams`; ready to load directly from JSON/YAML config file. |
| **5. Business Operators (Genuine Policy Logic)** | Chubb Champion Hubb 2-stage offset (`Month` first, excess into `M12`), Chubb AL symmetric negative FYC clawback, AIA CQL vs PAF+ 70% cap asymmetry, Chubb RD quarterly QoQ/YoY growth comparison | Keep in **company-specific policy adapters** backed by small shared operators (avoid premature generic DSL!). |
| **6. Unsupported Dependencies** | Manulife FA/UM/DM rules, AIA Exchange/Pro allowance & commission appendix, Chubb `260005V` EHC currency threshold & BD policy, full-text consolidated `44/2026/VBHN-TT-BTC` legal mapping | Keep explicitly marked `UNKNOWN` / `MISSING_DEPENDENCY` — never approximate silently. |

---

## 3. Proposed Level 3 Vertical Slice (Next Phase Only — NOT Implemented in Level 2)

> **Goal:** Prove **Level 3 — Configuration-Driven** cleanly on ONE bounded vertical slice without rewriting the entire compensation engine.

- **Selected Vertical Slice:** **Retroactive Tiered Quarterly Production Bonus with Effective-Dated Quality Multiplier** (shared pattern across AIA Alpha CVTV Quarterly Bonus `2026 vs 2027` AND W24 Proposal Monthly/Quarterly Bonus).
- **Artifact Design:**
  1. One validated JSON fixture (`configs/schemes/sample_retroactive_bonus_v1.json`) conforming strictly to `schemas/compensation-scheme.schema.json` with `effective_date`, `tiers`, `quality_multiplier_table`, and `source_id`.
  2. One small pure operator (`evaluate_retroactive_tiered_bonus(base_value, metric_value, persistency_pct, effective_date, config)`) validated by a lightweight schema loader.
  3. **Level 3 Proof Test:** Change a tier rate or effective date threshold **ONLY inside the JSON config file** (zero edits to Python engine formulas), re-run the test suite, and confirm deterministic output change + zero regression on all existing competitor adapters!

---

## 4. Level 4 Extensibility Roadmap & Acceptance Criteria (Section 18)

*(Deferred until Level 2 is independently verified and Level 3 vertical slice is proven. Explicitly NO database, RAG, microservices, HTML simulator, or marketing automation in Level 2!)*

### Planned Level 4 Building Blocks
1. **Company Policy Adapters** (`model/adapters/{aia,chubb,manulife,proposal}.py`) sharing a **Canonical Result Contract** (`Earned / Cash_Y1 / Accrued_T1 / Deferred_PostY1 / Clawback / Forfeiture / Unpriced_Flags`).
2. **Reusable Tested Calculation Operators** (`retroactive_tier`, `marginal_tier`, `effective_dated_multiplier`, `two_stage_offset`, `capped_ratio`, `vesting_schedule`).
3. **Effective-Date & Revision Resolver** (selects exact active rule version for any transaction date, handling dual-phase mid-year switches like Manulife `2026-04-01` and Chubb RD `Q3-2026`).
4. **Cross-Engine Parity Contract** (shared JSON Golden Test Vectors consumed identically by Python engine, Excel generator/verifier, and future P3 HTML/JS simulator).
5. **Change Impact Analysis** (maps any modified `Rule_ID` or `Lookup_Key` to affected adapters, Excel cells, and Golden Tests).

### Level 4 Extensibility Acceptance Criteria

| Extension Scenario | Mandatory Acceptance Criteria (Pass Gate) |
|---|---|
| **1. Add New Company (e.g., Synthetic Insurer D or Manulife FA)** | Add 1 adapter module + 1 registry/lookup/config set + golden tests with **ZERO edits to shared operators, core validation helpers, or existing company adapters**; all existing tests remain 100% PASS. |
| **2. Add New Channel under Existing Company (e.g., AIA Traditional)** | Isolate via `(company, channel, scheme_id)` namespace with zero side effects on Alpha channel calculations or lookups. |
| **3. Add New Scheme / Proposal Variant** | Load pure JSON parameter variant through `ProposalParams` / config loader with **ZERO code edits**; verified by deterministic perturbation test. |
| **4. Add New Memo / Superseding Revision Memo** | Register `Revision_Class = Replacement` + `Effective_Date` in `source-registry.csv`; historical scenarios before `Effective_Date` remain reproducible while post-date scenarios automatically resolve new parameters. |
| **5. Add New Bonus Type** | If supported by existing canonical operators (`flat_rate`, `retroactive_tiered`, `excess_over_target`, `max_of_components`), configure purely via data; if genuinely novel logic, add 1 isolated operator + unit tests without altering unrelated schemes. |
