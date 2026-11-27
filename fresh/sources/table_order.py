"""So thứ tự số trong từng bảng giữa A và B (ghép bảng theo độ trùng số)."""
import json, re, sys
from compare_reads import NUM, norm
def seq(t): return [norm(n) for row in t for c in row for n in NUM.findall(str(c))]
def ctx(r, n):
    blob = json.dumps(r, ensure_ascii=False)
    m = re.search(r".{0,80}(?<![\d.,])" + re.escape(n) + r"(?![\d.,]).{0,60}", blob)
    return m.group(0) if m else ""
did = sys.argv[1]
A = json.load(open(f"reads/{did}_A.json", encoding="utf-8")); B = json.load(open(f"reads/{did}_B.json", encoding="utf-8"))
tb = [(r, seq(r["table"])) for r in B["rules"] if r.get("table")]
bad = 0
for ra in A["rules"]:
    if not ra.get("table"): continue
    sa = seq(ra["table"])
    if not sa: continue
    best = max(tb, key=lambda x: len(set(x[1]) & set(sa)) / max(1, len(set(x[1]) | set(sa))), default=None)
    if not best: continue
    rb, sb = best
    if sa != sb:
        bad += 1
        print(f"-- A#{ra['rule_no']} ({ra.get('item','')[:50]}) vs B#{rb['rule_no']} ({rb.get('item','')[:50]}) tr.{ra.get('page')}")
        print("   A:", sa); print("   B:", sb)
print("bảng lệch thứ tự:", bad, "/", sum(1 for r in A["rules"] if r.get("table")))
if len(sys.argv) > 2:
    for who, D in (("A", A), ("B", B)):
        for r in D["rules"]:
            c = ctx(r, sys.argv[2])
            if c: print(who, r["rule_no"], r.get("page"), "::", c)
