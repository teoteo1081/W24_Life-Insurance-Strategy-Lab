"""Đồng bộ kết quả Python → Supabase (data contract: supabase/schema.sql).

Python là nguồn sự thật; Supabase chỉ lưu; HTML chỉ đọc (web/data-loader.js).
Sửa lỗi = sửa engine/script → chạy lại file này → web tự cập nhật.

Cách chạy:
  python scripts/sync_to_supabase.py --dry-run          # không gọi mạng; ghi web/data/snapshot.json
  python scripts/sync_to_supabase.py                    # upsert lên Supabase (cần .env)
  python scripts/sync_to_supabase.py --prune            # upsert + xóa dòng cũ không còn trong lần sinh này

Biến môi trường (đặt trong .env ở gốc repo — .env đã được .gitignore chặn; mẫu: supabase/env.example):
  SUPABASE_URL=https://<project>.supabase.co
  SUPABASE_SERVICE_KEY=<service_role key — CHỈ dùng phía máy, không bao giờ đưa vào HTML>

Bảo mật (DEC-14): dòng dựa trên 0046M01_2026 / 0047M01_2026 gắn confidentiality='restricted';
RLS trong schema.sql chỉ cho người trong allowlist w24_readers đọc các dòng này.
Chỉ dùng thư viện chuẩn (urllib) — không cài thêm gói.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

SNAPSHOT = REPO / "web" / "data" / "snapshot.json"
CONFIDENTIAL_FILES = ("0046M01_2026", "0047M01_2026")          # DEC-14: văn bản ghi "thông tin mật"
TABLE_KEYS = {"benchmark_results": "id", "role_benefit_matrix": "id", "glossary_terms": "abbr", "pdf_bookmarks": "id"}


# ---------------- helpers ----------------
def _finite(x):
    if x is None:
        return None
    if not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(f"non-finite value {x!r}")
    return round(float(x), 4)


def _conf(*texts) -> str:
    blob = " ".join(t for t in texts if t)
    return "restricted" if any(f in blob for f in CONFIDENTIAL_FILES) else "public"


def model_version() -> str:
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "model", "scripts", "knowledge"], cwd=REPO,
                               capture_output=True, text=True, check=True).stdout.strip()
        return sha + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


# ---------------- payload ----------------
def build_payload(synced_at: str | None = None) -> dict:
    import build_benefit_matrix as BM
    import build_interview_income_table as T
    from w24_milestones import aia_title, chubb_title, load_milestones

    synced_at = synced_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    ver = model_version()
    MS = load_milestones()
    msd = {m.mid: m for m in MS}
    m = T.m

    # ---- benchmark_results (cùng hàm với outputs/interview/01_...md)
    fyc, y2, y3, ra, rc = T.agent_m1(MS[0])
    rm = T.mnl_agent_m1(MS[0])
    titles = {ms.mid: (aia_title(ms)[0], chubb_title(ms)[0]) for ms in MS}
    rows = []

    def bench(mid, co, comparison, title, basis, earned, cash, promo, fee, label="MODEL_OUTPUT", note=""):
        ms = msd[mid]
        inc = None if earned is None else _finite(m(earned))
        rows.append({
            "id": f"{mid}|ALL|{co}|{comparison}|{title}", "model_version": ver, "milestone_id": mid, "milestone_label": ms.label,
            "producing_agents": ms.agents, "org_fyp_month_vnd_m": ms.fyp_month, "region": "ALL", "company": co,
            "comparison": comparison, "title": title, "income_basis": basis, "income_vnd_m_month": inc,
            "cash_y1_vnd_m_month": None if cash is None else _finite(m(cash)),
            "cost_pct_org_fyp": None if inc is None else _finite(inc / ms.fyp_month * 100.0),
            "promotion_citation": promo, "fee_citation": fee, "label": label, "note": note,
            "confidentiality": _conf(promo, fee, note), "synced_at": synced_at})

    aia_m1 = ra["total_earned"] + y3
    bench("M1", "AIA", "primary", titles["M1"][0], "personal_income", aia_m1, aia_m1, "[AIAVAD 2601-034 : 8]", "[AIAVAD 2604-069 : 3-7]",
          note="FYC/tái tục theo giả định A1, A7")
    bench("M1", "Chubb", "primary", titles["M1"][1], "personal_income", rc["total_earned"], rc["cash_paid_y1"], "[CHH0DCEB260007V : 7]",
          "[CHH0DCEB260007V : 4-7]", note="FYC/RYC theo giả định A1, A7")
    bench("M1", "Manulife", "primary", "Đại Lý", "personal_income", rm["total_earned"], rm["cash_paid_y1"], "[0047M01_2026 : 6]",
          "[0046M01_2026 : 1-8]", note="Không danh hiệu Manulife Pro (base case)")
    for mid in ("M2", "M3"):
        ms = msd[mid]
        a = T.aia_manager(ms)[0]
        c = T.chubb_manager(ms, titles[mid][1] if titles[mid][1] in ("UM", "SM", "DM") else "DM")[0]
        u = T.mnl_um(ms)[0]
        bench(mid, "AIA", "primary", titles[mid][0], "net_management_fee", a["total_earned"], a["cash_paid_y1"], "[AIAVAD 2601-034 : 8]", "[AIAVAD 2601-034 : 3-5]")
        bench(mid, "Chubb", "primary", titles[mid][1], "net_management_fee", c["total_earned"], c["cash_paid_y1"], "[CHH0DCEB260007V : 7]", "[CHH0DCEB260008V : 5-10]")
        bench(mid, "Manulife", "primary", "UM+", "net_management_fee", u["total_earned"], u["cash_paid_y1"], "[0047M01_2026 : 6]", "[0047M01_2026 : 1-3]",
              note="Không danh hiệu MBA Pro (base case)")
    ms4 = msd["M4"]
    a4 = T.aia_manager(ms4, include_indirect=False)[0]
    paf = T.calc_aia_paf_12m("PAF", 1, [ms4.fyp_month] * 12, [ms4.fyc_month] * 12, [float(ms4.agents)] * 12, fy_pct=T.K2, attendance_pct=80.0)
    y2o, y3o = T.renewal_split(ms4.fyp_month)
    rd = T.calc_chubb_rd_12m([ms4.fyp_month] * 12, [ms4.fyc_month] * 12, [ms4.agents] * 12, [ms4.agents] * 12, [(y2o + y3o) / 12] * 12,
                             k2_pct=T.K2, weighted_reported_fyp_monthly=ms4.fyp_month, training_classes_monthly=4, prior_year_q_fyp=[ms4.fyp_month * 3] * 4)
    psm = T.calc_manulife_psm_12m(T.MNL_BASE, [T.MNL_ACH] * 12, [ms4.fyc_month] * 12, [T.MNL_AA_ACH] * 4, T.K2)
    dm4 = T.chubb_manager(ms4, "DM")[0]
    u4 = T.mnl_um(ms4)[0]
    bench("M4", "AIA", "primary", "PAF", "net_management_fee", paf["total_earned"] + a4["total_earned"], paf["cash_paid_y1"] + a4["cash_paid_y1"],
          "[AIAVAD 2601-034 : 8], [AIAVAD 2601-035 : 6]", "[AIAVAD 2601-035 : 2-5], [AIAVAD 2601-034 : 3-5]", note="Dual Career: không có gián tiếp cấp 2–4")
    bench("M4", "Chubb", "primary", "RD", "net_management_fee", rd["total_earned"], rd["cash_paid_y1"], "[CHH0DCEB260003V : 3]", "[CHH0DCEB260003V : 5-10]",
          note="RD bổ nhiệm theo hợp đồng; so sánh chính theo DEC-14")
    bench("M4", "Manulife", "primary", "PSM/SM", "net_management_fee", psm["total_earned"], psm["cash_paid_y1"], "[0048M01_2026 : 5]", "[0048M01_2026 : 1-5]",
          note="PSM+ bổ nhiệm; đạt 100% chỉ tiêu là giả định A8")
    bench("M4", "Chubb", "secondary", "DM", "net_management_fee", dm4["total_earned"], dm4["cash_paid_y1"], "[CHH0DCEB260007V : 7]", "[CHH0DCEB260008V : 5-10]",
          note="Tuyến quản lý truyền thống — nếu chưa lên BD")
    bench("M4", "Chubb", "secondary", "BD", "net_management_fee", None, None, "[CHH0DCEB260007V : 7]", "[CHH0DCEB260003V : 3], [CHH0DCEB260003V : 10-11]",
          label="UNKNOWN", note="Chức danh đạt bằng chỉ tiêu; biểu phí BD không có trong 9 PDF")
    bench("M4", "Manulife", "secondary", "UM+", "net_management_fee", u4["total_earned"], u4["cash_paid_y1"], "[0047M01_2026 : 6]", "[0047M01_2026 : 1-3]",
          note="Tuyến quản lý truyền thống")

    # ---- role_benefit_matrix (cùng ô với outputs/interview/00_Role_And_Benefit_Matrix.md)
    cells, bm = BM.build_cells()
    matrix = [{"id": f"{c['milestone_id']}|{c['matrix_table']}|{c['company']}|{c['row_no']}", "model_version": ver, **c,
               "confidentiality": _conf(c["value_text"], c["citation"]), "synced_at": synced_at} for c in cells]

    # ---- glossary_terms (knowledge/sources/glossary.json)
    gl = json.loads((REPO / "knowledge/sources/glossary.json").read_text(encoding="utf-8"))["entries"]
    glossary = []
    for e in gl:
        conf_cites = [c for c in e["citations"] if c["file_id"] in CONFIDENTIAL_FILES]
        pub_cites = [c for c in e["citations"] if c["file_id"] not in CONFIDENTIAL_FILES]
        restricted = (e["citations"] and not pub_cites) or _conf(e["note"], e["vietnamese"], e["market_equivalent"]) == "restricted"
        cites = e["citations"] if restricted else pub_cites
        cam = e["company_and_memo"]
        if conf_cites and not restricted:      # bản public: dựng lại từ trích dẫn KHÔNG mật (trang đầu tiên mỗi hãng)
            first = {}
            for c in pub_cites:
                first.setdefault(c["company"], c)
            cam = " · ".join(f"{co} [{c['file_id']} : {c['page']}]" for co, c in first.items())
        glossary.append({"abbr": e["abbr"], "english": e["english"], "vietnamese": e["vietnamese"], "company_and_memo": cam,
                         "market_equivalent": e["market_equivalent"], "note": e["note"], "term_group": e["group"],
                         "companies": e["companies"], "english_status": e["english_status"], "citations": cites,
                         "confidentiality": "restricted" if restricted else "public", "synced_at": synced_at})

    # ---- pdf_bookmarks (knowledge/sources/pdf-bookmarks.json)
    manifest = json.loads((REPO / "infra/evidence-worker/manifest.json").read_text(encoding="utf-8"))
    bookmarks = []
    for f in bm["files"]:
        url = manifest["files"].get(f["source_id"], {}).get("url")
        for i, b in enumerate(f["bookmarks"]):
            bookmarks.append({"id": f"{f['file_id']}|{i}", "file_id": f["file_id"], "source_id": f["source_id"], "file_name": f["file_name"],
                              "page_count": f["page_count"], "seq": i, "title": b["title"], "page": b["page"], "method": b["method"],
                              "evidence_url": url, "confidentiality": _conf(f["file_id"]), "synced_at": synced_at})

    return {"meta": {"model_version": ver, "synced_at": synced_at, "contract": "supabase/schema.sql v1",
                     "confidential_files": list(CONFIDENTIAL_FILES)},
            "tables": {"benchmark_results": rows, "role_benefit_matrix": matrix, "glossary_terms": glossary, "pdf_bookmarks": bookmarks}}


# ---------------- Supabase REST (PostgREST) ----------------
def load_env() -> dict:
    env = dict(os.environ)
    p = REPO / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return env


def _request(method: str, url: str, key: str, body=None, prefer: str = "") -> int:
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers={
        "apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json", "Prefer": prefer})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Supabase {method} {url.split('/rest/v1/')[-1]} → HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}")


def push(payload: dict, url: str, key: str, prune: bool) -> None:
    base = url.rstrip("/") + "/rest/v1/"
    for table, key_col in TABLE_KEYS.items():
        rows = payload["tables"][table]
        for i in range(0, len(rows), 500):
            _request("POST", f"{base}{table}?on_conflict={key_col}", key, rows[i:i + 500], "resolution=merge-duplicates,return=minimal")
        print(f"  upsert {table}: {len(rows)} rows")
        if prune:
            ts = urllib.request.quote(payload["meta"]["synced_at"])
            _request("DELETE", f"{base}{table}?synced_at=lt.{ts}", key, None, "return=minimal")
            print(f"  prune  {table}: rows older than this sync removed")


def main() -> int:
    ap = argparse.ArgumentParser(description="Sync W24 Python outputs to Supabase")
    ap.add_argument("--dry-run", action="store_true", help="không gọi mạng; chỉ ghi web/data/snapshot.json")
    ap.add_argument("--prune", action="store_true", help="xóa dòng cũ (synced_at < lần sync này)")
    args = ap.parse_args()

    payload = build_payload()
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    counts = {t: len(r) for t, r in payload["tables"].items()}
    restricted = {t: sum(1 for x in r if x["confidentiality"] == "restricted") for t, r in payload["tables"].items()}
    print(f"snapshot: {SNAPSHOT.relative_to(REPO)} · model {payload['meta']['model_version']} · rows {counts} · restricted {restricted}")
    if args.dry_run:
        return 0
    env = load_env()
    url, key = env.get("SUPABASE_URL", ""), env.get("SUPABASE_SERVICE_KEY", "")
    if not url or not key:
        print("Thiếu SUPABASE_URL / SUPABASE_SERVICE_KEY (đặt trong .env — xem supabase/env.example). Không đẩy dữ liệu.")
        return 2
    if not re.match(r"^https://[a-z0-9-]+\.supabase\.co/?$", url):
        print("SUPABASE_URL không đúng dạng https://<project>.supabase.co — dừng.")
        return 2
    push(payload, url, key, args.prune)
    print("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
