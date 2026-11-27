"""Gói A (scripts/build_brief.py): một nguồn số với web; bản công khai không có dòng/mã mật; bản đủ chỉ ghi ngoài repo."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import build_brief as BB  # noqa: E402

TABLES = json.loads((REPO / "web/data/snapshot.json").read_text(encoding="utf-8"))["tables"]
PUBLIC = {k: [r for r in v if r.get("confidentiality") != "restricted"] for k, v in TABLES.items()}


class TestBrief(unittest.TestCase):
    def setUp(self) -> None:
        self.pub, self.full = BB.render(PUBLIC, full=False), BB.render(TABLES, full=True)

    def test_public_has_no_confidential_tokens(self) -> None:
        for token in ("0046M01", "0047M01", "SRC-POL-MNL-002", "SRC-POL-MNL-003", "UM+", "MNL-AG", "MNL-MG"):
            self.assertNotIn(token, self.pub, token)

    def test_single_proposal_and_no_stale_names(self) -> None:
        for md in (self.pub, self.full):
            self.assertIn(BB.PROPOSAL, md)
            self.assertNotIn("Chính sách Lai (", md)
            self.assertNotIn("—%", md)
            self.assertNotIn("nan", md.lower().replace("nanh", ""))

    def test_numbers_come_from_snapshot(self) -> None:
        roi = {(r["scheme"], r["metric"], int(r["k2"])): r["value"] for r in TABLES["roi_analysis"]}
        for s, m in (("Hybrid", "cost_pct_fyp"), ("Hybrid", "cost_pct_fyp_worst_case"), ("Chubb", "cost_pct_fyp"), ("Hybrid", "art52_agent_bonus_pct_fyp_worst")):
            self.assertIn(BB.vn(roi[(s, m, 85)]) + "%", self.pub, (s, m))

    def test_full_adds_manulife(self) -> None:
        self.assertIn("UM+", self.full)
        self.assertGreater(len(self.full), len(self.pub))

    def test_full_copy_must_be_outside_repo(self) -> None:
        with self.assertRaises(SystemExit):
            BB.main(["--full-out", str(REPO / "outputs" / "x.md")])
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(BB.main(["--full-out", str(Path(d) / "full.md")]), 0)


if __name__ == "__main__":
    unittest.main()
