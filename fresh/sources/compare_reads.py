"""So 2 bản đọc độc lập (A, B) của cùng văn bản: số nào chỉ một người thấy, theo trang.
Chạy: py -3 -X utf8 compare_reads.py [DOC_ID ...]   → in báo cáo + ghi diff/<ID>.json
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
NUM = re.compile(r"\d+(?:[.,]\d+)*")


def norm(n: str) -> str:
    """'1.000.000' → '1000000'; '12,5' → '12.5'; '0,5' → '0.5'."""
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", n):
        return n.replace(".", "")
    return n.replace(",", ".")


def pages_of(p) -> list:
    s = str(p)
    m = re.findall(r"\d+", s)
    if "-" in s and len(m) == 2:
        return list(range(int(m[0]), int(m[1]) + 1))
    return [int(x) for x in m] or [0]


def numbers(rule: dict) -> Counter:
    parts = [rule.get("base", ""), rule.get("rate_or_amount", ""), rule.get("payment_timing", ""),
             rule.get("clawback_or_forfeit", ""), " ".join(rule.get("conditions") or [])]
    for row in rule.get("table") or []:
        parts.append(" | ".join(str(c) for c in row))
    c = Counter()
    for t in parts:
        for n in NUM.findall(str(t)):
            c[norm(n)] += 1
    return c


def by_page(doc: dict) -> dict:
    out = {}
    for r in doc.get("rules", []):
        for p in pages_of(r.get("page", 0)):
            out.setdefault(p, Counter()).update(numbers(r))
    return out


def compare(did: str) -> dict:
    a = json.loads((HERE / "reads" / f"{did}_A.json").read_text(encoding="utf-8"))
    b = json.loads((HERE / "reads" / f"{did}_B.json").read_text(encoding="utf-8"))
    pa, pb = by_page(a), by_page(b)
    diff = {}
    for p in sorted(set(pa) | set(pb)):
        sa, sb = set(pa.get(p, {})), set(pb.get(p, {}))
        oa, ob = sorted(sa - sb, key=float), sorted(sb - sa, key=float)
        if oa or ob:
            diff[p] = {"only_A": oa, "only_B": ob}
    res = {"doc": did, "rules_A": len(a.get("rules", [])), "rules_B": len(b.get("rules", [])),
           "pages_read_A": len(a.get("pages_read", [])), "pages_read_B": len(b.get("pages_read", [])),
           "uncertain_A": [r.get("rule_no") for r in a.get("rules", []) if r.get("uncertain")],
           "uncertain_B": [r.get("rule_no") for r in b.get("rules", []) if r.get("uncertain")],
           "page_diffs": diff,
           "doc_only_A": sorted(set().union(*[set(c) for c in pa.values()] or [set()]) - set().union(*[set(c) for c in pb.values()] or [set()]), key=float),
           "doc_only_B": sorted(set().union(*[set(c) for c in pb.values()] or [set()]) - set().union(*[set(c) for c in pa.values()] or [set()]), key=float),
           "inconsistencies_A": a.get("internal_inconsistencies", []), "inconsistencies_B": b.get("internal_inconsistencies", [])}
    (HERE / "diff").mkdir(exist_ok=True)
    (HERE / "diff" / f"{did}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    return res


if __name__ == "__main__":
    ids = sys.argv[1:] or sorted({p.name.rsplit("_", 1)[0] for p in (HERE / "reads").glob("*_A.json")})
    for did in ids:
        if not (HERE / "reads" / f"{did}_B.json").exists():
            print(did, "— chưa đủ 2 bản"); continue
        r = compare(did)
        print(f"== {did}: rules A {r['rules_A']} / B {r['rules_B']} · pages A {r['pages_read_A']} / B {r['pages_read_B']} · "
              f"uncertain A {r['uncertain_A']} B {r['uncertain_B']} · trang lệch {len(r['page_diffs'])}")
        print(f"   TOÀN VĂN BẢN: chỉ A {r['doc_only_A']} | chỉ B {r['doc_only_B']}")
        for p, d in r["page_diffs"].items():
            print(f"   tr.{p}: chỉ A {d['only_A'][:25]} | chỉ B {d['only_B'][:25]}")
