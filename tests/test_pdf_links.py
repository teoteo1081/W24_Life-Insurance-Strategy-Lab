"""DEC-22: 9 PDF nguồn nằm trong repo; trang HTML có link mở trang gốc cho cả 9 (R2 nếu có, không thì file trong repo)."""
import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parents[1]


class TestPdfLinks(unittest.TestCase):
    def test_all_nine_pdfs_tracked_and_linked(self) -> None:
        pdfs = sorted((REPO / "private/sources").rglob("*.pdf"))
        self.assertEqual(len(pdfs), 9)
        for page in ("outputs/interactive/W24_Strategy_Lab.html", "outputs/public/W24_Strategy_Lab.html"):
            html = (REPO / page).read_text(encoding="utf-8")
            data = json.loads(re.search(r"const DATA = (\{.*?\});\n", html, re.S).group(1))
            self.assertEqual(len(data["pdfs"]), 9, page)
            for p in data["pdfs"]:
                with self.subTest(page=page, file=p["file_id"]):
                    self.assertTrue(p["url"], "thiếu link mở trang gốc")
                    if p["url"].startswith("../../"):                       # link vào repo phải trỏ tới file có thật
                        self.assertTrue((REPO / unquote(p["url"][6:])).is_file(), p["url"])


if __name__ == "__main__":
    unittest.main()
