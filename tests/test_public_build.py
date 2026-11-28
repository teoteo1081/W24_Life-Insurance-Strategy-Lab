"""Bản công khai (DEC-14): scripts/build_html.py --public + scripts/check_public_build.py."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import build_html as B  # noqa: E402
import check_public_build as C  # noqa: E402
import sync_to_supabase as S  # noqa: E402


class TestPublicBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        golden_before = B.GOLDEN.read_bytes()
        B.main(["--public"])
        cls.golden_unchanged = B.GOLDEN.read_bytes() == golden_before
        cls.html = B.OUT_PUBLIC.read_text(encoding="utf-8")

    def test_scanner_passes_on_public_build(self) -> None:
        self.assertEqual(C.scan(B.OUT_PUBLIC), [])
        self.assertTrue(self.golden_unchanged)          # --public không ghi đè golden của repo

    def test_all_restricted_rows_removed_and_public_rows_kept(self) -> None:
        full = json.loads((REPO / "web/data/snapshot.json").read_text(encoding="utf-8"))
        snap = C.embedded_snapshot(self.html)
        for t, rows in full["tables"].items():
            pub = [r for r in rows if r["confidentiality"] == "public"]
            with self.subTest(table=t):
                self.assertEqual(len(snap["tables"][t]), len(pub))
                self.assertEqual(snap["meta"]["restricted_rows_removed"][t], len(rows) - len(pub))
        self.assertEqual(sum(snap["meta"]["restricted_rows_removed"].values()), 0)   # DEC-21: không còn văn bản mật   # GĐ1 (54) + GĐ2

    def test_full_local_build_untouched(self) -> None:
        full = (REPO / "outputs/interactive/W24_Strategy_Lab.html").read_text(encoding="utf-8")
        self.assertIn("0047M01", full)                   # bản đầy đủ trên máy vẫn giữ nguyên để gửi trực tiếp
        self.assertNotEqual(B.OUT_PUBLIC, REPO / "outputs/interactive/W24_Strategy_Lab.html")

    def test_scanner_catches_leaks(self) -> None:
        cases = {"conf": "biểu phí MAT-001", "secret": "sb_secret_abc123", "path": "C:" + "/Users/x/a.pdf",   # ghép chuỗi: tránh chính hygiene gate bắt nhầm file test
                 "restricted": None}
        saved = C.CONFIDENTIAL[:]
        C.CONFIDENTIAL[:] = ["MAT-001"]          # DEC-21: danh sách mật đang rỗng → thử cơ chế quét bằng một mã giả định
        self.addCleanup(lambda: C.CONFIDENTIAL.__setitem__(slice(None), saved))
        for name, inject in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as d:
                p = Path(d) / "W24_Strategy_Lab.html"
                html = self.html
                if inject is None:   # một dòng restricted lọt vào snapshot
                    html = html.replace('"confidentiality":"public"', '"confidentiality":"restricted"', 1)
                else:
                    html = html.replace("</body>", f"<!-- {inject} --></body>", 1)
                p.write_text(html, encoding="utf-8")
                self.assertNotEqual(C.scan(p), [], name)
        with tempfile.TemporaryDirectory() as d:          # file lạ trong thư mục phát hành
            shutil.copy(B.OUT_PUBLIC, Path(d) / "W24_Strategy_Lab.html")
            (Path(d) / ".env").write_text("SUPABASE_SERVICE_KEY=x", encoding="utf-8")
            self.assertTrue(any("ngoài danh sách" in e for e in C.scan(Path(d) / "W24_Strategy_Lab.html")))

    def test_public_glossary_text_scrubbed(self) -> None:
        # Cơ chế lọc vẫn giữ cho tài liệu mật sau này: thử với một mã giả định
        saved = S.CONFIDENTIAL_TOKENS
        try:
            S.CONFIDENTIAL_TOKENS = ("MAT-001",)
            self.assertEqual(S.scrub_text("Hãng X: biểu phí MAT-001, ký HĐ"), "")
            self.assertEqual(S.scrub_text("AIA: tên A; Hãng X: MAT-001 tr.3"), "AIA: tên A")
        finally:
            S.CONFIDENTIAL_TOKENS = saved
        self.assertEqual(S.CONFIDENTIAL_TOKENS, ())                     # DEC-21
        payload = S.build_payload(synced_at="2026-11-27T00:00:00+00:00")
        for r in payload["tables"]["glossary_terms"]:
            if r["confidentiality"] == "public":
                blob = json.dumps(r, ensure_ascii=False)
                with self.subTest(abbr=r["abbr"]):
                    self.assertFalse(any(t in blob for t in S.CONFIDENTIAL_TOKENS))


if __name__ == "__main__":
    unittest.main()
