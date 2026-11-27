"""Tests for scale milestones, cited title derivation and the 100-point ingestion rubric."""
from __future__ import annotations

import csv
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from w24_milestones import aia_title, chubb_title, load_milestones, manulife_title, rubric_table  # noqa: E402

CITE = re.compile(r"^\[[^\]:]+ : [0-9]+(-[0-9]+)?\]$")


class TestMilestones(unittest.TestCase):
    def test_four_milestones_add_up(self) -> None:
        ms = load_milestones()
        self.assertEqual([m.mid for m in ms], ["M1", "M2", "M3", "M4"])
        self.assertEqual([m.agents for m in ms], [1, 5, 15, 45])
        self.assertEqual([m.fyp_month for m in ms], [30.0, 150.0, 450.0, 1200.0])

    def test_titles_derived_from_cited_promotion_rules(self) -> None:
        # Expected from AIAVAD 2601-034 p.8 / 2601-035 p.6 and CHH0DCEB260007V p.7 under the stated assumptions.
        expected = {"M1": ("SA", "AR"), "M2": ("SUM", "UM"), "M3": ("SDM", "DM"), "M4": ("PAF", "BD")}
        for m in load_milestones():
            ta, ca = aia_title(m)
            tc, cc = chubb_title(m)
            with self.subTest(m=m.mid):
                self.assertEqual((ta, tc), expected[m.mid])
                for c in ca + cc:
                    self.assertRegex(c.cite, CITE)
                self.assertEqual(manulife_title(m)[0], "Đại Lý" if m.mid == "M1" else "UM+")   # track only; rank rules in 0013M04 (absent)

    def test_aia_70pct_rule_blocks_single_branch_dominance(self) -> None:
        # M3: each sub-UM branch (270 FYC / 6M) stays below 70% of the SDM requirement (280) -> counted in full.
        m3 = load_milestones()[2]
        title, _ = aia_title(m3)
        self.assertEqual(title, "SDM")


class TestRubric(unittest.TestCase):
    def test_pass_and_fail_threshold(self) -> None:
        _, ok = rubric_table(9, 15, 15, 10, 10, 10, 10, 1, 1, 10, 10)
        self.assertEqual(ok, 100.0)
        _, low = rubric_table(6, 15, 15, 5, 10, 5, 10, 0, 1, 5, 10)
        self.assertLess(low, 90)

    def test_rejects_bad_inputs(self) -> None:
        with self.assertRaises(ValueError):
            rubric_table(7, 15, 15, 10, 10, 10, 10, 1, 1, 10, -1)


class TestRoleCsv(unittest.TestCase):
    def test_every_title_has_verbatim_track_and_citation(self) -> None:
        rows = list(csv.DictReader(open(REPO / "knowledge/policies/role-organization-mapping.csv", encoding="utf-8")))
        self.assertEqual(len(rows), 36)
        for r in rows:
            with self.subTest(role=r["Role_ID"]):
                self.assertTrue(r["Raw_Title_Verbatim"])
                self.assertTrue(r["Track_Type"])
                if r["Track_Type"] == "NOT_IN_CORPUS":
                    self.assertIn("NEGATIVE_PROOF", r["Title_Citation"])
                else:
                    self.assertRegex(r["Title_Citation"].split(" (")[0], CITE)


if __name__ == "__main__":
    unittest.main()
