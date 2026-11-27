"""knowledge/sources/glossary.json — nguồn duy nhất cho từ điển & tooltip HTML."""
from __future__ import annotations

import csv
import json
import re
import unittest
from pathlib import Path

import pymupdf

REPO = Path(__file__).resolve().parents[1]
GL = json.loads((REPO / "knowledge/sources/glossary.json").read_text(encoding="utf-8"))
REQUIRED = ["abbr", "english", "vietnamese", "company_and_memo", "market_equivalent", "note"]


class TestGlossary(unittest.TestCase):
    def test_six_required_fields_non_empty(self) -> None:
        self.assertGreaterEqual(len(GL["entries"]), 50)
        for e in GL["entries"]:
            with self.subTest(abbr=e["abbr"]):
                for k in REQUIRED:
                    self.assertTrue(str(e.get(k, "")).strip(), k)
                self.assertIn(e["group"], ("Chỉ số", "Chức danh", "Tuyến hợp đồng", "Khoản thu nhập"))

    def test_citations_point_to_pages_containing_the_term(self) -> None:
        reg = {r["Source_ID"]: r for r in csv.DictReader(open(REPO / "knowledge/sources/source-registry.csv", encoding="utf-8"))}
        cache = {}
        for e in GL["entries"]:
            term = re.sub(r"\s*\((AIA|Chubb|Manulife)\)$", "", e["abbr"]).split(" / ")[0]
            for c in e["citations"]:
                if c["method"] != "text_search":
                    continue
                if c["source_id"] not in cache:
                    cache[c["source_id"]] = [p.get_text() for p in pymupdf.open(REPO / reg[c["source_id"]]["Local_Relative_Path"])]
                text = re.sub(r"\s+", " ", cache[c["source_id"]][c["page"] - 1])
                with self.subTest(abbr=e["abbr"], cite=f"{c['file_id']}:{c['page']}"):
                    self.assertIn(term.split()[0].lower(), text.lower())

    def test_source_corrections_kept(self) -> None:
        by = {e["abbr"]: e for e in GL["entries"]}
        self.assertIn("Quyền Sáng lập khối", by["PAF"]["vietnamese"])       # not "Premier Agency Force"
        self.assertNotIn("bình quân", by["3MAA"]["vietnamese"])              # defined at 0003V p.14, not an average
        self.assertEqual(by["BM"]["companies"], ["Chung"])                    # not in the 9 PDFs

    def test_html_reads_glossary_from_data_not_hardcoded(self) -> None:
        tpl = (REPO / "web/template.html").read_text(encoding="utf-8")
        self.assertNotIn("const GLOSSARY = {", tpl)
        self.assertIn("DATA.glossary", tpl)
        html = (REPO / "outputs/interactive/W24_Strategy_Lab.html").read_text(encoding="utf-8")
        # glossary nhúng 2 nơi: DATA.glossary (trang) và W24_LOCAL_SNAPSHOT (dự phòng offline của web/data-loader.js)
        self.assertEqual(html.count('"english_status"'), 2 * len(GL["entries"]))
        self.assertIn('"glossary_terms":[', html)


if __name__ == "__main__":
    unittest.main()
