"""So thứ tự số trong từng bảng giữa A và B (ghép bảng theo độ trùng số).

Mỗi ô được so dưới dạng (dấu biên, số): '≥50%' và '>50%' là hai token khác nhau. Hai dãy
được căn theo con số (difflib); ở mọi vị trí cùng số mà khác dấu → báo lệch biên, kể cả khi
bảng đó còn lệch ở chỗ khác (chia quy tắc khác nhau).
Chạy: py -3 -X utf8 table_order.py DOC_ID [số cần tra ngữ cảnh]
"""
import difflib
import json
import re
import sys
from pathlib import Path

from compare_reads import MIN_PAIR_SIM, bounded

HERE = Path(__file__).parent


def seq(t):
    return [tok for row in t for c in row for tok in bounded(str(c))]


def nums(sq):
    return [n for _, n in sq]


def fmt(sq):
    return [op + n for op, n in sq]


def op_mismatch(sa, sb):
    """Vị trí số trùng nhau sau khi căn mà dấu khác: [(vị trí trong A, token A, token B)]."""
    sm = difflib.SequenceMatcher(a=nums(sa), b=nums(sb), autojunk=False)
    out = []
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            x, y = sa[blk.a + k], sb[blk.b + k]
            if x[0] != y[0]:
                out.append((blk.a + k, x[0] + x[1], y[0] + y[1]))
    return out


def compare_tables(A: dict, B: dict) -> dict:
    """Ghép bảng theo cả 2 chiều (A→B và B→A) để bảng chép lặp không che lỗi ở bản sao kia."""
    ta = [(r, seq(r["table"])) for r in A["rules"] if r.get("table")]
    tb = [(r, seq(r["table"])) for r in B["rules"] if r.get("table")]
    ta = [x for x in ta if x[1]]
    tb = [x for x in tb if x[1]]
    order, boundary = [], []
    if ta and tb:
        sim = lambda x, y: len(set(nums(x)) & set(nums(y))) / max(1, len(set(nums(x)) | set(nums(y))))
        pairs = {(i, max(range(len(tb)), key=lambda j: sim(ta[i][1], tb[j][1]))) for i in range(len(ta))}
        pairs |= {(max(range(len(ta)), key=lambda i: sim(ta[i][1], tb[j][1])), j) for j in range(len(tb))}
        for i, j in sorted(pairs):
            (ra, sa), (rb, sb) = ta[i], tb[j]
            if sim(sa, sb) < MIN_PAIR_SIM:
                continue
            pair = {"A": ra["rule_no"], "B": rb["rule_no"], "page": ra.get("page"),
                    "item_A": ra.get("item", "")[:50], "item_B": rb.get("item", "")[:50]}
            if nums(sa) != nums(sb):
                order.append({**pair, "seq_A": fmt(sa), "seq_B": fmt(sb)})
            mm = op_mismatch(sa, sb)
            if mm:
                boundary.append({**pair, "mismatch": mm})
    return {"tables_A": sum(1 for r in A["rules"] if r.get("table")), "order": order, "boundary": boundary}


def ctx(r, n):
    blob = json.dumps(r, ensure_ascii=False)
    m = re.search(r".{0,80}(?<![\d.,])" + re.escape(n) + r"(?![\d.,]).{0,60}", blob)
    return m.group(0) if m else ""


if __name__ == "__main__":
    did = sys.argv[1]
    A = json.loads((HERE / "reads" / f"{did}_A.json").read_text(encoding="utf-8"))
    B = json.loads((HERE / "reads" / f"{did}_B.json").read_text(encoding="utf-8"))
    res = compare_tables(A, B)
    for o in res["order"]:
        print(f"-- A#{o['A']} ({o['item_A']}) vs B#{o['B']} ({o['item_B']}) tr.{o['page']}")
        print("   A:", o["seq_A"])
        print("   B:", o["seq_B"])
    for b in res["boundary"]:
        print(f"!! LỆCH BIÊN A#{b['A']} vs B#{b['B']} tr.{b['page']}:", b["mismatch"])
    print(f"bảng lệch thứ tự: {len(res['order'])} / {res['tables_A']} · bảng lệch biên: {len(res['boundary'])}")
    if len(sys.argv) > 2:
        for who, D in (("A", A), ("B", B)):
            for r in D["rules"]:
                c = ctx(r, sys.argv[2])
                if c:
                    print(who, r["rule_no"], r.get("page"), "::", c)
