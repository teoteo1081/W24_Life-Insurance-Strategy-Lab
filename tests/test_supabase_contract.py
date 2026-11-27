"""Data contract Supabase: schema.sql ↔ payload của scripts/sync_to_supabase.py ↔ web/data-loader.js (offline, không gọi mạng)."""
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
SCHEMA = (REPO / "supabase/schema.sql").read_text(encoding="utf-8")
TABLES = ["benchmark_results", "role_benefit_matrix", "glossary_terms", "pdf_bookmarks",
          "roi_analysis", "rubric_scores", "behavior_traps", "hybrid_regional"]   # v2: + Giai đoạn 2


def schema_columns(table: str) -> dict:
    body = re.search(r"create table if not exists public\." + table + r" \((.*?)\n\);", SCHEMA, re.S).group(1)
    cols = {}
    for line in body.splitlines():
        m = re.match(r"\s+([a-z_0-9]+)\s+(text|integer|numeric|smallint|jsonb|timestamptz|text\[\])\b(.*)", line)
        if m:
            cols[m.group(1)] = {"type": m.group(2), "not_null": "not null" in m.group(3) and "default" not in m.group(3)}
    return cols


class TestSchema(unittest.TestCase):
    def test_all_tables_with_rls_and_no_write_policies(self) -> None:
        for t in TABLES:
            self.assertIn(f"create table if not exists public.{t} (", SCHEMA)
            self.assertIn("confidentiality", schema_columns(t))
        self.assertIn("enable row level security", SCHEMA)
        rls = re.search(r"foreach t in array array\[(.*?)\] loop", SCHEMA, re.S)
        self.assertIsNotNone(rls)
        self.assertEqual(set(re.findall(r"'(\w+)'", rls.group(1))), set(TABLES))             # RLS phủ ĐỦ mọi bảng dữ liệu (8)
        self.assertNotRegex(SCHEMA.lower(), r"for (insert|update|delete|all)\b")      # chỉ policy SELECT
        self.assertIn("public.w24_is_reader()", SCHEMA)                                   # restricted = allowlist, không phải mọi user
        self.assertIn("revoke insert, update, delete, truncate", SCHEMA)

    def test_glossary_has_six_contract_columns(self) -> None:
        cols = schema_columns("glossary_terms")
        for c in ["abbr", "english", "vietnamese", "company_and_memo", "market_equivalent", "note"]:
            self.assertIn(c, cols)


class TestPayload(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        import sync_to_supabase as S
        cls.S = S
        cls.payload = S.build_payload(synced_at="2026-11-27T00:00:00+00:00")

    def test_rows_match_schema_and_keys_unique(self) -> None:
        for t in TABLES:
            cols, rows = schema_columns(t), self.payload["tables"][t]
            key = self.S.TABLE_KEYS[t]
            self.assertTrue(rows, t)
            self.assertEqual(len({r[key] for r in rows}), len(rows), f"{t}: duplicate {key}")
            for r in rows:
                with self.subTest(table=t, row=r[key]):
                    self.assertLessEqual(set(r), set(cols))
                    for c, spec in cols.items():
                        if spec["not_null"]:
                            self.assertIsNotNone(r.get(c), c)
                    for v in r.values():
                        if isinstance(v, float):
                            self.assertTrue(math.isfinite(v))

    def test_counts_and_unknown_not_zero(self) -> None:
        t = self.payload["tables"]
        self.assertEqual(len(t["role_benefit_matrix"]), 84)
        self.assertEqual(len(t["pdf_bookmarks"]), 131)
        # DEC-17: + 4 phương án × 2 (chi phí & Điều 52 ở 4 nhóm năng suất) + hòa vốn 3 hãng × 3 chỉ số × 2 cơ cấu (bán đều, 4 nhóm)
        # roi_analysis 56 → 86 (AUD-03): + 4 phương án × 3 tỷ lệ hoa hồng (25/30/40%) × 2 chỉ số (chuẩn, xấu nhất) + Lai 3 × 2 tỷ lệ quỹ thưởng còn trả + 4 × 2 rổ Điều 52 (chuẩn, xấu nhất)
        for k, n in (("roi_analysis", 56 + 4 * 3 * 2 + 3 * 2 + 4 * 2 + 4 * 2 + 3 * 3 * 2), ("rubric_scores", 20), ("behavior_traps", 20), ("hybrid_regional", 40)):   # Giai đoạn 2; hybrid_regional 30 → 40: 4 vùng NĐ 293/2025 × 5 vai trò × 2 cách đọc
            self.assertEqual(len(t[k]), n, k)
        self.assertEqual(set(t), set(self.S.TABLE_KEYS))
        self.assertEqual(len(t["glossary_terms"]), len(json.loads((REPO / "knowledge/sources/glossary.json").read_text(encoding="utf-8"))["entries"]))
        bd = [r for r in t["benchmark_results"] if r["title"] == "BD"][0]
        self.assertEqual(bd["label"], "UNKNOWN")
        self.assertIsNone(bd["income_vnd_m_month"])                     # UNKNOWN không bị ép thành 0

    def test_dec14_confidential_rows_are_restricted(self) -> None:
        t = self.payload["tables"]
        for r in t["benchmark_results"]:
            if r["company"] == "Manulife" and r["title"] in ("Đại Lý", "UM+"):
                self.assertEqual(r["confidentiality"], "restricted", r["id"])
        for r in t["pdf_bookmarks"]:
            self.assertEqual(r["confidentiality"] == "restricted", r["file_id"] in ("0046M01_2026", "0047M01_2026"))
            if r["confidentiality"] == "restricted":
                self.assertIsNone(r["evidence_url"])
        for r in t["role_benefit_matrix"]:
            if "0047M01" in r["citation"] or "0046M01" in r["citation"]:
                self.assertEqual(r["confidentiality"], "restricted")
        for r in t["glossary_terms"]:
            if r["confidentiality"] == "public":
                self.assertFalse(any(c["file_id"] in ("0046M01_2026", "0047M01_2026") for c in r["citations"]), r["abbr"])
                self.assertNotRegex(r["company_and_memo"], "0046M01|0047M01")

    def test_benchmark_matches_interview_table(self) -> None:
        md = (REPO / "outputs/interview/01_Bang_So_Sanh_Thu_Nhap_Va_Evidence.md").read_text(encoding="utf-8")
        for r in self.payload["tables"]["benchmark_results"]:
            if r["income_vnd_m_month"] is not None and r["comparison"] == "primary":
                shown = f"{r['income_vnd_m_month']:.1f}".replace(".", ",")
                self.assertIn(shown, md, r["id"])


class TestSecretsAndLoader(unittest.TestCase):
    def test_env_is_gitignored_and_no_service_key_in_web(self) -> None:
        gi = (REPO / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", gi)
        for p in [REPO / "web/data-loader.js", REPO / "web/template.html", REPO / "outputs/interactive/W24_Strategy_Lab.html"]:
            self.assertNotIn("SUPABASE_SERVICE_KEY", p.read_text(encoding="utf-8"), p.name)
            self.assertNotIn("service_role", p.read_text(encoding="utf-8").replace("service_role key", ""), p.name)

    def test_service_key_guard(self) -> None:
        import base64
        import build_html as B
        jwt = lambda role: "x." + base64.urlsafe_b64encode(json.dumps({"role": role}).encode()).decode().rstrip("=") + ".y"
        self.assertTrue(B._looks_like_service_key(jwt("service_role")))
        self.assertTrue(B._looks_like_service_key("sb_secret_abc"))
        self.assertFalse(B._looks_like_service_key(jwt("anon")))

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_data_loader_falls_back_offline(self) -> None:
        js = (REPO / "web/data-loader.js").read_text(encoding="utf-8")
        probe = js + """
globalThis.W24_LOCAL_SNAPSHOT = {meta: {model_version: "t"}, tables: {glossary_terms: [{abbr: "K2"}], benchmark_results: [], role_benefit_matrix: [], pdf_bookmarks: []}};
W24Data.load().then(r => { console.log(JSON.stringify({source: r.source, n: r.tables.glossary_terms.length})); });
"""
        out = subprocess.run(["node", "-e", probe], capture_output=True, text=True, timeout=30)
        self.assertEqual(json.loads(out.stdout.strip()), {"source": "local", "n": 1}, out.stderr)


if __name__ == "__main__":
    unittest.main()
