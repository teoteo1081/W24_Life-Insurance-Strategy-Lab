"""Lớp kiểm thứ ba: điều kiện biên trong bộ đã chốt so với LỚP CHỮ GỐC của PDF.

So A với B chỉ bắt được chỗ hai người đọc khác nhau; nếu cả hai cùng đọc ≥ thành > thì không
lộ. Script này lấy mọi cặp (dấu, số) trong `rules_verified.json` và tìm trên trang được trích
(± 1 trang) của lớp chữ tách từ PDF:
  - SAME     : trang có đúng số đó với cùng dấu (hoặc cụm từ cùng nghĩa: từ = ≥, dưới = <, ...)
  - OTHER_OP : trang chỉ có số đó với dấu KHÁC → nguy cơ lệch biên, phải xem ảnh
  - BARE     : trang có số nhưng không kèm dấu (thường là dấu nằm ở tiêu đề cột / ô gộp)
  - ABSENT   : không thấy số trên các trang đó (số viết khác kiểu, ví dụ 3.000.000 ↔ 3 triệu)
Bản scan CHB-003 không có lớp chữ → bỏ qua (đã đọc 2 lượt bằng ảnh).

Lớp chữ nằm ngoài repo (trích từ PDF riêng tư). Chạy:
  py -3 -X utf8 check_bounds_vs_text.py <thư mục text/>   → in tóm tắt + ghi bounds_vs_text.json
File kết quả chỉ ghi token và trạng thái, không chép câu chữ văn bản.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

from compare_reads import bounded, rule_texts

HERE = Path(__file__).parent
PAGE = re.compile(r"^===== (\S+) — TRANG (\d+) =====$", re.M)


def pages_of_text(path: Path) -> dict:
    s = path.read_text(encoding="utf-8")
    marks = list(PAGE.finditer(s))
    return {int(m.group(2)): s[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(s)]
            for i, m in enumerate(marks)}


def cited_pages(p) -> set:
    nums = [int(x) for x in re.findall(r"\d+", str(p))]
    out = set()
    if "-" in str(p) and len(nums) == 2:
        nums = list(range(nums[0], nums[1] + 1))
    for n in nums:
        out |= {n - 1, n, n + 1}
    return out


def check(text_dir: Path) -> dict:
    ver = json.loads((HERE / "rules_verified.json").read_text(encoding="utf-8"))
    res = {}
    for did, doc in ver.items():
        tf = text_dir / f"{did}.txt"
        pages = pages_of_text(tf) if tf.exists() else {}
        if sum(len(v.strip()) for v in pages.values()) < 500:
            res[did] = {"skipped": "không có lớp chữ (bản scan)"}
            continue
        tally, other = Counter(), []
        for r in doc["rules"]:
            blob = "\n".join(pages.get(p, "") for p in sorted(cited_pages(r.get("page"))))
            src = bounded(blob)
            ops_for = {}
            for op, n in src:
                ops_for.setdefault(n, set()).add(op)
            for op, n in {t for t in (tok for t in rule_texts(r) for tok in bounded(t)) if t[0]}:
                if n not in ops_for:
                    st = "ABSENT"
                elif op in ops_for[n]:
                    st = "SAME"
                elif ops_for[n] - {""}:
                    st = "OTHER_OP"
                    other.append({"rule": r.get("rule_no"), "page": r.get("page"), "verified": op + n,
                                  "text_has": sorted(o + n for o in ops_for[n])})
                else:
                    st = "BARE"
                tally[st] += 1
        res[did] = {"tally": dict(tally), "other_op": other}
    return res


if __name__ == "__main__":
    out = check(Path(sys.argv[1]))
    (HERE / "bounds_vs_text.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for did, r in out.items():
        if "skipped" in r:
            print(f"{did}: bỏ qua — {r['skipped']}")
            continue
        print(f"{did}: {r['tally']}")
        for o in r["other_op"]:
            print(f"   ! quy tắc {o['rule']} tr.{o['page']}: chốt {o['verified']} — lớp chữ có {o['text_has']}")
