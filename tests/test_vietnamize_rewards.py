"""Hồi quy cho bản tiếng Việt của 44 cấu phần thu nhập (audit commit 64b9a5a: P1 trần/cấp, P2 giá trị trạng thái, P3 MNL-04)."""
from __future__ import annotations

import csv
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import vietnamize_rewards as vr  # noqa: E402


def generated_rows() -> dict[str, dict[str, str]]:
    with vr.SRC.open(encoding="utf-8") as f:
        src = list(csv.DictReader(f))
    return {r["Component_ID"]: {k: vr.OVERRIDES.get((r["Component_ID"], k), vr.vietnamize(r[k])) for k in vr.FIELDS} for r in src}


class TestVietnamizeRewards(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.rows = generated_rows()
        with vr.SRC.open(encoding="utf-8") as f:
            cls.src = {r["Component_ID"]: r for r in csv.DictReader(f)}

    def test_all_44_components_present_in_order(self) -> None:
        self.assertEqual(len(self.rows), 44)
        self.assertEqual(list(self.rows), list(self.src))

    def test_english_cap_becomes_tran_not_cap(self) -> None:
        rate = self.rows["TR-CHB-04"]["Rate_Or_Amount_Summary"]
        for amount in ("6tr", "10tr", "20tr"):
            with self.subTest(amount=amount):
                self.assertIn("trần " + amount, rate)
                self.assertNotIn("cấp " + amount, rate)
        self.assertIn("Trần 30tr", self.rows["TR-AIA-15"]["Rate_Or_Amount_Summary"])
        self.assertIn("Trần = 12x", self.rows["TR-MNL-04"]["Rate_Or_Amount_Summary"])
        for cid, field, needle in (("TR-CHB-02", "Rate_Or_Amount_Summary", "trần 45%"),
                                   ("TR-CHB-08", "Rate_Or_Amount_Summary", "trần 25%"),
                                   ("TR-CHB-10", "Rate_Or_Amount_Summary", "trần 15tr"),
                                   ("TR-CHB-14", "Rate_Or_Amount_Summary", "trần 2.5%"),
                                   ("TR-AIA-21", "Eligibility_Conditions", "trần = tổng")):
            with self.subTest(cid=cid):
                self.assertIn(needle, self.rows[cid][field])

    def test_vietnamese_cap_stays_cap(self) -> None:
        self.assertIn("Cấp 2-4", self.rows["TR-AIA-14"]["Component_Name_VN"])
        self.assertIn("cấp mã", self.rows["TR-AIA-02"]["Eligibility_Conditions"])
        self.assertIn("cấp trung", self.rows["TR-MNL-05"]["Component_Name_VN"])

    def test_status_values_kept_for_render_filters(self) -> None:
        checked = 0
        for cid, src in self.src.items():
            for k in vr.FIELDS:
                raw = src[k].strip()
                if raw.lower() in ("none", "n/a", "immediate", "0"):
                    checked += 1
                    with self.subTest(cid=cid, field=k):
                        self.assertEqual(self.rows[cid][k], raw)
        self.assertGreater(checked, 20)

    def test_mnl04_k2_condition_matches_source_page_5(self) -> None:
        gate = self.rows["TR-MNL-04"]["Quality_Persistency_Gate"]
        self.assertIn("xét lại cho từng năm chi trả Y1–Y3", gate)
        self.assertIn("cuối tháng 12 năm liền trước", gate)
        self.assertNotIn("toàn LẠI", gate)

    def test_no_untranslated_unknown_and_no_control_chars(self) -> None:
        for cid, row in self.rows.items():
            for k, v in row.items():
                with self.subTest(cid=cid, field=k):
                    self.assertNotIn("UNKNOWN", v)
                    self.assertIsNone(re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", v))

    def test_committed_vi_csv_matches_generator(self) -> None:
        with vr.OUT.open(encoding="utf-8") as f:
            committed = {r["Component_ID"]: {k: r[k] for k in vr.FIELDS} for r in csv.DictReader(f)}
        self.assertEqual(committed, self.rows)


if __name__ == "__main__":
    unittest.main()
