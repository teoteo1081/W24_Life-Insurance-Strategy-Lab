"""Dựng trang HTML tương tác (1 file, dữ liệu nhúng sẵn) cho bài Bước 1 của chị Nhi.

- Số của đối thủ (AIA Alpha 2026/2027, Chubb Life, Manulife tầng vùng) tính sẵn bằng engine Python ở mọi K2 50–95.
- Phương án đề xuất tính trực tiếp trong trình duyệt bằng web/engine.js (kiểm khớp Python: tests/test_web_parity.py).
- 112 quy tắc + 7 nguồn + kiểm mẫu 14 quy tắc, mỗi mục có link mở đúng trang PDF trên R2.
Đầu ra: outputs/interactive/W24_Strategy_Lab.html  ·  web/golden.json (lưới golden cho kiểm khớp JS↔Python).
Dùng:  py -3 scripts/build_html.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from dataclasses import asdict, replace
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
for p in (REPO, REPO / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from model.compensation.compensation_engine import (  # noqa: E402
    ProposalParams,
    calc_enterprise_hierarchy_cost,
    calc_manulife_psm_12m,
)
from agent_income_multiyear import agent_income_3y  # noqa: E402
from calibrate_song_hanh import main as calibrate_song_hanh  # noqa: E402

K2_RANGE = list(range(50, 96))
FYC_LEVELS = [3, 5, 8, 10, 15, 20, 25, 35, 45, 55]
OUT_HTML = REPO / "outputs/interactive/W24_Strategy_Lab.html"
GOLDEN = REPO / "web/golden.json"
OUT_PUBLIC = REPO / "outputs/public/W24_Strategy_Lab.html"   # bản công khai (DEC-14): --public
# Văn bản mật: bản công khai không được chứa dấu vết nào. DEC-21 (2026-11-28): rỗng — 9 PDF như nhau.
CONFIDENTIAL_TOKENS: tuple = ()


def _is_confidential(obj) -> bool:
    if isinstance(obj, dict) and obj.get("confidentiality") == "restricted":
        return True
    txt = json.dumps(obj, ensure_ascii=False)
    return any(t in txt for t in CONFIDENTIAL_TOKENS)


def _scrub(obj):
    """Bỏ mọi phần tử (dòng) trong list có nhắc tới văn bản mật hoặc nhãn restricted; đệ quy vào dict/list."""
    if isinstance(obj, dict):
        return {k: _scrub(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_scrub(x) for x in obj if not _is_confidential(x)]
    return obj


def _fill_repo_pdf_urls(manifest: dict) -> None:
    """DEC-22: 9 PDF nằm trong repo → văn bản chưa có trên R2 thì link thẳng tới file trong repo.
    Đường dẫn tương đối từ outputs/interactive|public/ — chạy được cả khi mở file trên máy lẫn trên GitHub Pages."""
    from urllib.parse import quote
    with open(REPO / "knowledge/sources/source-registry.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rel = r["Local_Relative_Path"].strip()
            if r["Source_ID"].startswith("SRC-POL-") and rel.lower().endswith(".pdf") and (REPO / rel).is_file():
                entry = manifest["files"].setdefault(r["Source_ID"], {})
                if not entry.get("url"):
                    entry["url"] = "../../" + quote(rel, safe="/")


def public_snapshot(snap: dict) -> dict:
    tables = {k: [r for r in rows if r.get("confidentiality") != "restricted"] for k, rows in snap["tables"].items()}
    dropped = {k: len(snap["tables"][k]) - len(tables[k]) for k in tables}
    meta = {k: v for k, v in snap["meta"].items() if k != "confidential_files"}   # tên văn bản mật cũng không công bố
    return {"meta": dict(meta, public_build=True, restricted_rows_removed=dropped), "tables": tables}


def public_glossary(rows: list) -> list:
    """Cùng ánh xạ với web/data-loader.js toGlossary — dòng public đã bỏ trích dẫn mật (scripts/sync_to_supabase.py)."""
    return [{"abbr": r["abbr"], "english": r["english"], "vietnamese": r["vietnamese"], "company_and_memo": r["company_and_memo"],
             "market_equivalent": r["market_equivalent"], "note": r["note"], "group": r["term_group"], "companies": r["companies"],
             "english_status": r["english_status"], "citations": r["citations"]} for r in rows]


def params_dict(p: ProposalParams) -> dict:
    return {k: (list(v) if isinstance(v, tuple) else v) for k, v in asdict(p).items()}


def plan_params() -> dict:
    base = ProposalParams()
    sh = ProposalParams(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in calibrate_song_hanh()["params"].items()})
    # Biến thể siết chất lượng: sàn K2 65% (dưới mức này thưởng = 0), giữ T+1 dưới 70%, bậc thưởng tháng ×0.92.
    quality = replace(sh, name="Thuong_Theo_Chat", k2_hard_floor_pct=65.0, k2_holdback_t1_threshold=70.0,
                      agent_m_tier_rates=tuple(round(r * 0.92, 4) for r in sh.agent_m_tier_rates))
    return {"song_hanh": params_dict(replace(sh, name="Song_Hanh")),
            "can_bang": params_dict(base),
            "theo_chat": params_dict(quality)}


def competitor_data() -> dict:
    ent = {}
    for s in ("AIA_Alpha_2026", "AIA_Alpha_2027", "Chubb_Agency_2026"):
        ent[s] = {}
        for k2 in K2_RANGE:
            r = calc_enterprise_hierarchy_cost(s, float(k2))
            keep = {k: r[k] for k in ("earned_pct_fyp", "cash_y1_pct_fyp", "art52_bonus_pct_fyp", "cost_per_persisted_y2_pct",
                                       "breakeven_gross_margin_pct", "total_earned_vnd_m", "role_agent_earned",
                                       "role_mgr_direct_earned", "role_mgr_indirect_extra", "role_leader_earned")}
            keep["deferred_share_pct"] = round(r["layer_f_deferred_3y"] / r["total_earned_vnd_m"] * 100, 2)
            keep["layers"] = {k: r[k] for k in ("layer_a_commission", "layer_b_agent_bonuses", "layer_c_mgr_direct",
                                                 "layer_d_mgr_indirect", "layer_e_rd_cash", "layer_f_deferred_3y")}
            ent[s][str(k2)] = keep
    agent = {"AIA": {}, "CHUBB": {}}
    for k2 in K2_RANGE:
        for s in agent:
            agent[s][str(k2)] = {}
        for f in FYC_LEVELS:
            r = agent_income_3y(float(f), float(k2))
            for s in agent:
                agent[s][str(k2)][str(f)] = {k: round(v, 2) for k, v in r[s].items()}
    mnl = {}
    for k2 in K2_RANGE:
        m = calc_manulife_psm_12m(35.0, [1.05] * 12, [300.0] * 12, [1.0] * 4, float(k2))
        mnl[str(k2)] = {"leader_earned": round(m["total_earned"], 2), "deferred_3y": round(m["long_term_deferred_3y"], 2)}
    return {"enterprise": ent, "agent3y": agent, "manulife_leader": mnl}


def golden(plans: dict) -> dict:
    cases = []
    sets = dict(plans)
    base = ProposalParams(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in plans["can_bang"].items()})
    sets["perturb_a"] = params_dict(replace(base, agent_m_tier_rates=(0.05, 0.11, 0.2, 0.3, 0.45), agent_ryc_bonus_rate=0.4,
                                            mgr_direct_base_rate=0.25, rd_base_monthly=50.0, k2_hard_floor_pct=55.0))
    sets["perturb_b"] = params_dict(replace(base, agent_m_tier_thresholds=(3.0, 9.0, 18.0, 30.0, 50.0),
                                            agent_q_consistency_3m=0.2, mgr_deferred_3y_rate=0.2, rd_deferred_3y_share=0.4))
    for name, pd in sets.items():
        p = ProposalParams(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in pd.items()})
        for k2 in (52.0, 58.0, 62.0, 70.0, 74.0, 75.0, 82.0, 88.0):
            e = calc_enterprise_hierarchy_cost("W24_Proposed_Balanced", k2, params=p)
            cases.append({"kind": "enterprise", "plan": name, "k2": k2,
                          "expect": {k: e[k] for k in ("earned_pct_fyp", "cash_y1_pct_fyp", "art52_bonus_pct_fyp",
                                                       "cost_per_persisted_y2_pct", "breakeven_gross_margin_pct",
                                                       "role_agent_earned", "role_mgr_direct_earned",
                                                       "role_mgr_indirect_extra", "role_leader_earned")}})
            for f in (3.0, 5.0, 15.0, 35.0, 45.0):
                a = agent_income_3y(f, k2, p)["PROPOSAL"]
                cases.append({"kind": "agent3y", "plan": name, "k2": k2, "fyc": f, "expect": a})
    return {"params": sets, "cases": cases}


def first_page(text: str, sid: str) -> int | None:
    tail = text.split(sid, 1)[1] if sid in text else ""
    m = re.search(r"p\.?\s*(\d+)", tail)
    return int(m.group(1)) if m else None


def knowledge(manifest: dict) -> dict:
    with (REPO / "knowledge/sources/source-registry.csv").open(encoding="utf-8") as f:
        reg = list(csv.DictReader(f))
    with (REPO / "knowledge/business-rules/business-rules-catalog.csv").open(encoding="utf-8") as f:
        rules = list(csv.DictReader(f))
    sources = []
    for r in reg:
        sid = r["Source_ID"]
        sources.append({"id": sid, "company": r["Company"], "scheme": r["Scheme"], "type": r["Document_Type"],
                        "audience": r["Target_Audience"], "pages": r["Pages"], "effective": r["Effective_Date"],
                        "confidentiality": r["Confidentiality"], "rights": r["Redistribution_Rights_Status"],
                        "verification": r["Verification_Status"],
                        "url": manifest["files"].get(sid, {}).get("url")})
    # Mọi văn bản chính sách (PDF) — kể cả văn bản chưa có URL trên kho bằng chứng (0046M01/0047M01 chưa tải lên R2):
    # trước đây lọc theo URL nên quy tắc MNL-AG/MG mất refs và trang Bằng chứng báo sai "chưa trích quy tắc" (AUD-08).
    pdf_ids = [s["id"] for s in sources if s["id"].startswith("SRC-POL-")]
    out_rules = []
    for r in rules:
        refs = []
        for sid in pdf_ids:
            if sid in r["Source_ID_And_Page"]:
                refs.append({"sid": sid, "page": first_page(r["Source_ID_And_Page"], sid)})
        out_rules.append({"id": r["Rule_ID"], "scheme": r["Scheme_ID"], "ref": r["Source_ID_And_Page"], "refs": refs,
                          "tier": r["Rank_Tier"], "type": r["Income_Type"], "threshold": r["Threshold"],
                          "structure": r["Tier_Structure"], "rate": r["Rate_Pct"], "cap": r["Cap_Limit"],
                          "period": r["Period"], "clawback": r["Clawback_Rule"],
                          "src_ver": r["Source_Verification"], "impl": r["Implementation_Status"],
                          "calc": r["Calculation_Verification"]})
    spot = []
    for line in (REPO / "qa/spot-check-14-rules.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*([A-Z]{3}-[A-Z]{2}-\d{3})\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|", line)
        if m:
            spot.append({"rule": m.group(2), "where": m.group(3).strip(), "result": m.group(4).strip(), "evidence": m.group(5).strip()})
    matrix = []
    for line in (REPO / "outputs/working/strategic-recommendations-and-schemes.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*\*\*(\d+)\.\s*(.+?)\*\*\s*(\*\(([^)]*)\)\*)?\s*\|\s*([^|]+)\|\s*\*\*`([A-Z]+)`\*\*\s*\|\s*([^|]+)\|", line)
        if m:
            ids = re.findall(r"[A-Z]{3}-[A-Z]{2}-\d{3}(?:/\d{3})?(?:\.\.\d{3})?", m.group(5))
            matrix.append({"no": int(m.group(1)), "mechanism": re.sub(r"`", "", m.group(2)).strip(),
                           "company": (m.group(4) or "").strip(), "rules": ids, "decision": m.group(6),
                           "why": re.sub(r"[`*]", "", m.group(7)).strip()})
    # Tổng gói thu nhập: 44 cấu phần (knowledge/compensation) gán vào 4 cấp để so sánh theo cấp.
    tier_of = {}
    for cid in ["AIA-%02d" % i for i in range(1, 12)] + ["CHB-%02d" % i for i in range(1, 7)] + ["MNL-05"]:
        tier_of["TR-" + cid] = "agent"
    for cid in ("AIA-12", "AIA-13", "AIA-15", "AIA-16", "AIA-17", "AIA-18", "CHB-07", "CHB-08", "CHB-10", "CHB-11", "CHB-12"):
        tier_of["TR-" + cid] = "mgr"
    for cid in ("AIA-14", "CHB-09"):
        tier_of["TR-" + cid] = "ind"
    for cid in ("AIA-19", "AIA-20", "AIA-21", "MNL-01", "MNL-02", "MNL-03", "MNL-04",
                "CHB-13", "CHB-14", "CHB-15", "CHB-16", "CHB-17", "CHB-18"):
        tier_of["TR-" + cid] = "leader"
    keep = ("Component_ID", "Company", "Target_Role", "Category_A_to_H", "Component_Name_VN", "Rate_Or_Amount_Summary",
            "Eligibility_Conditions", "Threshold_Minimum", "Cap_Maximum", "Quality_Persistency_Gate", "Activity_Attendance_Gate",
            "Training_Compliance_Gate", "Measurement_Period", "Payment_Timing", "Vesting_Schedule", "Clawback_Recovery_Rule",
            "Holdback_Forfeiture_Rule", "Rule_ID_Link", "Source_ID_And_Page", "Evidence_Status")
    rewards = []
    vi_path = REPO / "knowledge/compensation/total-rewards-inventory-vi.csv"  # bản có dấu (scripts/vietnamize_rewards.py)
    vi = {}
    if vi_path.is_file():
        with vi_path.open(encoding="utf-8") as f:
            vi = {r["Component_ID"]: r for r in csv.DictReader(f)}
    with (REPO / "knowledge/compensation/total-rewards-inventory.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = {k: r[k] for k in keep}
            d.update({k: v for k, v in vi.get(r["Component_ID"], {}).items() if k in d and k != "Component_ID"})
            d["tier"] = tier_of.get(r["Component_ID"], "agent")
            rewards.append(d)
    with (REPO / "knowledge/policies/role-organization-mapping.csv").open(encoding="utf-8") as f:
        roles = [{k: r[k] for k in ("Role_ID", "Company", "Role_Code", "Role_Title_VN_EN", "Functional_Tier",
                                     "Entry_Promotion_Condition", "Maintenance_Demotion_Condition", "Managed_Scope_Direct_Indirect",
                                     "Source_ID_And_Page_And_Status")} for r in csv.DictReader(f)]
    return {"sources": sources, "rules": out_rules, "spot_check": spot, "adopt_matrix": matrix,
            "rewards": rewards, "roles": roles}


def _looks_like_service_key(key: str) -> bool:
    """Chặn nhúng nhầm service key: khóa mới 'sb_secret_…' hoặc JWT có role=service_role."""
    import base64
    if key.startswith("sb_secret_"):
        return True
    parts = key.split(".")
    if len(parts) == 3:
        try:
            body = json.loads(base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4)))
            return body.get("role") == "service_role"
        except (ValueError, UnicodeDecodeError):
            return False
    return False


def supabase_meta() -> str:
    """Thẻ meta cấu hình ĐỌC cho web/data-loader.js — chỉ từ W24_SUPABASE_URL / W24_SUPABASE_ANON_KEY (env hoặc .env).
    Không cấu hình → trang dùng snapshot nhúng (offline)."""
    import html as _html
    import os
    env = dict(os.environ)
    p = REPO / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    url, key = env.get("W24_SUPABASE_URL", "").strip(), env.get("W24_SUPABASE_ANON_KEY", "").strip()
    if not url or not key:
        return "<!-- Supabase chưa cấu hình: trang dùng dữ liệu nhúng -->"
    if _looks_like_service_key(key) or key == env.get("SUPABASE_SERVICE_KEY", "").strip():
        raise SystemExit("W24_SUPABASE_ANON_KEY trông như SERVICE key — không nhúng vào HTML. Dùng anon/publishable key.")
    if not re.match(r"^https://[a-z0-9-]+\.supabase\.co/?$", url):
        raise SystemExit("W24_SUPABASE_URL không đúng dạng https://<project>.supabase.co")
    return (f'<meta name="w24-supabase-url" content="{_html.escape(url)}">\n'
            f'<meta name="w24-supabase-anon-key" content="{_html.escape(key)}">')


def main(argv=None) -> int:
    public = "--public" in (sys.argv[1:] if argv is None else argv)
    manifest = json.loads((REPO / "infra/evidence-worker/manifest.json").read_text(encoding="utf-8"))
    _fill_repo_pdf_urls(manifest)
    plans = plan_params()
    data = {"generated": "2026-11-27", "k2_range": [K2_RANGE[0], K2_RANGE[-1]], "fyc_levels": FYC_LEVELS,
            "plans": plans, "competitors": competitor_data(), "knowledge": knowledge(manifest),
            "evidence_base": manifest["base_url"]}
    # Từ điển & mục lục 9 PDF — nguồn duy nhất: knowledge/sources/glossary.json, pdf-bookmarks.json
    # (sinh bởi scripts/build_glossary.py, scripts/build_benefit_matrix.py). PDF chỉ mở được nếu đã có trên kho
    # bằng chứng (manifest); 0046M01/0047M01 chưa tải lên R2 nên chưa có url (DEC-21: không còn coi là mật).
    gl = json.loads((REPO / "knowledge/sources/glossary.json").read_text(encoding="utf-8"))
    bm = json.loads((REPO / "knowledge/sources/pdf-bookmarks.json").read_text(encoding="utf-8"))
    data["glossary"] = gl["entries"]
    data["pdfs"] = [{"file_id": f["file_id"], "sid": f["source_id"], "name": f["file_name"], "pages": f["page_count"],
                     "url": manifest["files"].get(f["source_id"], {}).get("url"),
                     "bookmarks": [{"t": b["title"], "p": b["page"]} for b in f["bookmarks"]]} for f in bm["files"]]
    g = golden(plans)
    if not public:   # bản công khai không ghi đè golden của repo
        GOLDEN.write_text(json.dumps(g, ensure_ascii=False) + "\n", encoding="utf-8")
    tpl = (REPO / "web/template.html").read_text(encoding="utf-8")
    snap_path = REPO / "web/data/snapshot.json"
    snap_obj = json.loads(snap_path.read_text(encoding="utf-8")) if snap_path.exists() else None
    if public:
        if snap_obj is None:
            raise SystemExit("--public cần web/data/snapshot.json (chạy scripts/sync_to_supabase.py --dry-run)")
        snap_obj = public_snapshot(snap_obj)
        data = _scrub(data)
        data["glossary"] = public_glossary(snap_obj["tables"]["glossary_terms"])
        data["public_build"] = True
        # Chữ tĩnh trong template (không phải dữ liệu): thay TRƯỚC khi nhúng dữ liệu, để bước quét vẫn bắt được rò rỉ thật.
    # Tóm tắt nhanh 2 góc nhìn — cùng nguồn với outputs/interview/00_Executive_Summary_Keo_Thom.md; bản công khai dùng snapshot đã lọc
    if snap_obj is not None:
        import build_exec_summary as ES
        data["exec_summary"] = ES.build(snap_obj["tables"])
    # Tab 4 · Hai góc nhìn (scripts/build_two_lens.py); bản công khai bỏ phương án có số liệu mật
    tl_path = REPO / "web/data/two_lens.json"
    if tl_path.exists():
        import build_two_lens as TL
        tl = json.loads(tl_path.read_text(encoding="utf-8"))
        data["two_lens"] = TL.public_view(tl) if data.get("public_build") else tl
    engine = (REPO / "web/engine.js").read_text(encoding="utf-8")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = tpl.replace("/*__ENGINE_JS__*/", engine).replace("/*__DATA_JSON__*/null", payload)
    html = html.replace("/*__GOLDEN_JSON__*/null", json.dumps(g["cases"][:60], separators=(",", ":")))
    # Lớp dữ liệu tách rời (supabase/schema.sql): loader + snapshot dự phòng offline + cấu hình đọc (chỉ anon key).
    loader = (REPO / "web/data-loader.js").read_text(encoding="utf-8")
    snap = json.dumps(snap_obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") if snap_obj is not None else "null"
    html = html.replace("/*__DATA_LOADER__*/", loader).replace("/*__LOCAL_SNAPSHOT__*/null", snap)
    html = html.replace("<!--__SUPABASE_META__-->", supabase_meta())
    out = OUT_PUBLIC if public else OUT_HTML
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    extra = f", restricted rows removed: {sum(snap_obj['meta']['restricted_rows_removed'].values())}" if public else ""
    print(f"wrote {out.relative_to(REPO)} ({len(html)//1024} KB), golden cases: {len(g['cases'])}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
