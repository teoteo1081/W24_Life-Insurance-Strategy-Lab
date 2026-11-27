"""Công cụ đối chiếu 2 lượt đọc (fresh/sources): phải bắt được đổi điều kiện biên, không chỉ con số.

Lỗi gốc (review P2): đổi '≥50%' thành '>50%' vẫn được xem là giống nhau vì chỉ so tập con số.
"""
import copy
import json
import sys
import unicodedata
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "fresh" / "sources"
sys.path.insert(0, str(SRC))

import compare_reads as C  # noqa: E402
import table_order as T  # noqa: E402

DOCS = ["AIA-034", "AIA-035", "AIA-069", "CHB-003", "CHB-007", "CHB-008", "MNL-046", "MNL-047", "MNL-048"]


def load(did, who):
    return json.loads((SRC / "reads" / f"{did}_{who}.json").read_text(encoding="utf-8"))


def detected(A, B, B2) -> bool:
    return (C.rule_boundary_diffs(A, B2) != C.rule_boundary_diffs(A, B)
            or T.compare_tables(A, B2)["boundary"] != T.compare_tables(A, B)["boundary"])


class TestBoundaryParsing(unittest.TestCase):
    def test_tokens(self):
        self.assertEqual(C.bounded("≥ 90% và < 100%"), [(">=", "90"), ("<", "100")])
        self.assertEqual(C.bounded("Từ 5 đến dưới 10"), [(">=", "5"), ("<", "10")])
        self.assertEqual(C.bounded("55%≤FY<65%"), [(">=", "55"), ("<", "65")])         # dạng hậu tố
        self.assertEqual(C.bounded("tối thiểu là 18 Tháng"), [(">=", "18")])
        self.assertEqual(C.bounded("1.000.000 đồng"), [("", "1000000")])

    def test_nfd_text_layer(self):
        nfd = unicodedata.normalize("NFD", "ít nhất 01 tháng")
        self.assertEqual(C.bounded(nfd), [(">=", "01")])


class TestBoundaryDetection(unittest.TestCase):
    def test_reviewer_example_ge_vs_gt(self):
        a = {"rules": [{"rule_no": 1, "conditions": ["FY ≥50%"], "rate_or_amount": "100%"}]}
        b = {"rules": [{"rule_no": 1, "conditions": ["FY >50%"], "rate_or_amount": "100%"}]}
        self.assertEqual(C.numbers(a["rules"][0]), C.numbers(b["rules"][0]))     # lớp số trần: giống nhau
        self.assertTrue(C.rule_boundary_diffs(a, b))                              # lớp biên: phải báo
        self.assertIn("50", C.boundary_diffs(a, b)["conflict"])

    def test_number_reused_elsewhere_does_not_mask(self):
        # 50 còn xuất hiện với '≥' ở quy tắc khác → so tập dấu toàn văn bản bị che; so theo quy tắc phải bắt.
        a = {"rules": [{"rule_no": 1, "conditions": ["FY ≥50%"]}, {"rule_no": 2, "conditions": ["K2 >50%", "trần 7 triệu"]}]}
        b = {"rules": [{"rule_no": 1, "conditions": ["FY >50%"]}, {"rule_no": 2, "conditions": ["K2 ≥50%", "trần 7 triệu"]}]}
        self.assertTrue(C.rule_boundary_diffs(a, b))

    def test_table_row_vs_column_order(self):
        a = {"rules": [{"rule_no": 1, "table": [["FY", "2026", "2027"], ["cao", "≥85%", "≥90%"], ["vừa", "≥75%", "≥80%"]]}]}
        b = {"rules": [{"rule_no": 1, "table": [["Năm", "cao", "vừa"], ["2026", "≥85%", ">75%"], ["2027", "≥90%", "≥80%"]]}]}
        self.assertTrue(C.rule_boundary_diffs(a, b))

    def test_mutation_on_real_reads(self):
        """Đổi từng dấu '≥' (đứng trước số) trong bản B thật thành '>' → mọi lần đổi đều phải bị báo."""
        total = 0
        for did in ("AIA-069", "MNL-048", "CHB-008"):
            A, B = load(did, "A"), load(did, "B")
            for i, r in enumerate(B["rules"]):
                for j, row in enumerate(r.get("table") or []):
                    for k, cell in enumerate(row):
                        pos = str(cell).find("≥")
                        if pos < 0 or not C.bounded(cell[pos:pos + 12])[0][0]:
                            continue
                        B2 = copy.deepcopy(B)
                        B2["rules"][i]["table"][j][k] = cell[:pos] + ">" + cell[pos + 1:]
                        total += 1
                        self.assertTrue(detected(A, B, B2), f"{did} quy tắc {r['rule_no']} ô {cell!r}")
        self.assertGreater(total, 30)


class TestReviewedState(unittest.TestCase):
    def test_flags_equal_reviewed_list(self):
        """Mọi cờ biên hiện có đã được rà và ghi lý do; cờ mới phải được xem ảnh rồi mới thêm."""
        review = json.loads((SRC / "boundary_review.json").read_text(encoding="utf-8"))
        want = sorted((f["doc"], f["layer"], f["A"], f["B"], json.dumps(f["mismatch"], ensure_ascii=False)) for f in review["flags"])
        got = []
        for did in DOCS:
            A, B = load(did, "A"), load(did, "B")
            got += [(did, "rule", x["A"], x["B"], json.dumps([list(m) for m in x["mismatch"]], ensure_ascii=False))
                    for x in C.rule_boundary_diffs(A, B)]
            got += [(did, "table", x["A"], x["B"], json.dumps([list(m) for m in x["mismatch"]], ensure_ascii=False))
                    for x in T.compare_tables(A, B)["boundary"]]
        self.assertEqual(sorted(got), want)
        for f in review["flags"]:
            self.assertNotIn(f["why"].strip(), ("", "?"))

    def test_verified_notes_consistent_with_tables(self):
        """Review P3: bảng đã chốt ô gộp thì ghi chú không được giữ nhận định cũ 'ô trống / không nói rõ'."""
        ver = json.loads((SRC / "rules_verified.json").read_text(encoding="utf-8"))
        for did, doc in ver.items():
            for r in doc["rules"]:
                cells = " ".join(str(c) for row in (r.get("table") or []) for c in row)
                note = (r.get("note") or "").lower()
                if "ô gộp" in cells:
                    self.assertNotIn("ô trống", note, f"{did} quy tắc {r['rule_no']}")
                    self.assertNotIn("ô gộp trống", note, f"{did} quy tắc {r['rule_no']}")
        pro = next(r for r in ver["MNL-046"]["rules"] if r["rule_no"] == 7)
        self.assertNotIn("không nói rõ", pro["note"])
        self.assertEqual([row[1] for row in pro["table"][1:]][-1].split()[0], "3.000.000")
        self.assertEqual([row[2] for row in pro["table"][1:]][-1].split()[0], "7.000.000")


if __name__ == "__main__":
    unittest.main()
