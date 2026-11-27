"""So 2 bản đọc độc lập (A, B) của cùng văn bản.

Hai lớp so sánh:
1. Con số trần — số nào chỉ một người thấy (theo trang và toàn văn bản).
2. Điều kiện biên — mỗi con số mang theo dấu so sánh đứng ngay trước nó (≥ > ≤ < =, hoặc
   "từ / trên / dưới / tối thiểu / tối đa / không quá ..."). Cùng một số mà dấu khác nhau
   (ví dụ ≥50% và >50%) bị báo là lệch biên, dù tập con số trần trùng khớp.

Chạy: py -3 -X utf8 compare_reads.py [DOC_ID ...]   → in báo cáo + ghi diff/<ID>.json
"""
import difflib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
NUM = re.compile(r"\d+(?:[.,]\d+)*")

# Dấu/cụm từ so sánh → dạng chuẩn. Cụm dài đặt trước để khớp trước cụm ngắn.
OPS = [
    (r"lớn hơn hoặc bằng|cao hơn hoặc bằng|không thấp hơn|không dưới|tối thiểu|ít nhất|từ|>=|≥|=>", ">="),
    (r"nhỏ hơn hoặc bằng|thấp hơn hoặc bằng|không vượt quá|không quá|tối đa|<=|≤|=<", "<="),
    (r"lớn hơn|cao hơn|vượt|trên|>", ">"),
    (r"nhỏ hơn|thấp hơn|dưới|<", "<"),
    (r"bằng|=", "="),
]
OP_ALT = "|".join(f"(?:{a})" for a, _ in OPS)
OP_NUM = re.compile(rf"(?:(?P<op>{OP_ALT})\s*(?:là\s+)?)?(?<![\d.,])(?P<n>\d+(?:[.,]\d+)*)", re.IGNORECASE)

POST_OP = re.compile(r"\s*%?\s*(≤|<=|<|≥|>=|>)(?!\s*\d)")   # số – dấu – chữ (không phải số – dấu – số)
FLIP = {"<=": ">=", "<": ">", ">=": "<=", ">": "<", "=": "="}


def norm_op(op):
    if not op:
        return ""
    op = op.lower()
    for alt, std in OPS:
        if re.fullmatch(alt, op, re.IGNORECASE):
            return std
    return ""


def norm(n: str) -> str:
    """'1.000.000' → '1000000'; '12,5' → '12.5'; '0,5' → '0.5'."""
    if re.fullmatch(r"\d{1,3}(?:\.\d{3})+", n):
        return n.replace(".", "")
    return n.replace(",", ".")


def numkey(n: str):
    """Khóa sắp xếp an toàn cho cả chuỗi kiểu mục lục '1.2.3'."""
    try:
        return (0, float(n), n)
    except ValueError:
        return (1, 0.0, n)


def pages_of(p) -> list:
    s = str(p)
    m = re.findall(r"\d+", s)
    if "-" in s and len(m) == 2:
        return list(range(int(m[0]), int(m[1]) + 1))
    return [int(x) for x in m] or [0]


def rule_texts(rule: dict) -> list:
    parts = [rule.get("base", ""), rule.get("rate_or_amount", ""), rule.get("payment_timing", ""),
             rule.get("clawback_or_forfeit", ""), " ".join(rule.get("conditions") or [])]
    for row in rule.get("table") or []:
        parts.append(" | ".join(str(c) for c in row))
    return [str(t) for t in parts]


def numbers(rule: dict) -> Counter:
    c = Counter()
    for t in rule_texts(rule):
        for n in NUM.findall(t):
            c[norm(n)] += 1
    return c


def bounded(text: str) -> list:
    """[(dấu chuẩn, số chuẩn)] theo thứ tự xuất hiện; dấu rỗng = không có điều kiện biên."""
    text = re.sub(r"\s+", " ", unicodedata.normalize("NFC", text))   # PDF hay tách dấu tiếng Việt (NFD), xuống dòng giữa cụm
    out = []
    for m in OP_NUM.finditer(text):
        op = norm_op(m.group("op"))
        if not op:   # dạng hậu tố "55% ≤ FY" nghĩa là FY ≥ 55 → đảo chiều dấu
            post = POST_OP.match(text, m.end())
            if post:
                op = FLIP[norm_op(post.group(1))]
        out.append((op, norm(m.group("n"))))
    return out


def ops_by_number(doc: dict) -> dict:
    """số → Counter(dấu) trên toàn văn bản (chỉ tính những lần số đi kèm dấu)."""
    out = {}
    for r in doc.get("rules", []):
        for t in rule_texts(r):
            for op, n in bounded(t):
                if op:
                    out.setdefault(n, Counter())[op] += 1
    return out


def boundary_diffs(a: dict, b: dict) -> dict:
    """Số có mặt ở cả 2 bản đọc nhưng tập dấu biên khác nhau.
    conflict: cả hai đều ghi dấu cho số đó, nhưng có dấu chỉ một bên dùng (≥50 vs >50).
    one_sided: một bên ghi dấu, bên kia chỉ ghi số trần ở mọi chỗ."""
    oa, ob = ops_by_number(a), ops_by_number(b)
    na = set().union(*[set(numbers(r)) for r in a.get("rules", [])] or [set()])
    nb = set().union(*[set(numbers(r)) for r in b.get("rules", [])] or [set()])
    conflict, one_sided = {}, {}
    for n in sorted(na & nb, key=numkey):
        sa, sb = set(oa.get(n, {})), set(ob.get(n, {}))
        if sa == sb:
            continue
        row = {"A": sorted(sa), "B": sorted(sb)}
        (conflict if sa and sb else one_sided)[n] = row
    return {"conflict": conflict, "one_sided": one_sided}


def by_page(doc: dict) -> dict:
    out = {}
    for r in doc.get("rules", []):
        for p in pages_of(r.get("page", 0)):
            out.setdefault(p, Counter()).update(numbers(r))
    return out


def rule_tokens(rule: dict) -> list:
    """(dấu, số) theo thứ tự trong phần mang quy tắc: điều kiện, cơ sở, tỷ lệ, kỳ trả, thu hồi, bảng.
    Bỏ 'note' và 'quote' (diễn giải tự do, không phải tham số)."""
    return [tok for t in rule_texts(rule) for tok in bounded(t)]


MIN_PAIR_SIM = 0.2   # cặp quy tắc/bảng trùng số dưới mức này coi như không cùng nội dung → không so dấu


def _jacc(x: set, y: set) -> float:
    return len(x & y) / max(1, len(x | y))


def _op_mismatch(ta: list, tb: list) -> list:
    """Căn 2 dãy (dấu, số) theo con số; vị trí cùng số, cả hai đều có dấu, mà dấu khác."""
    sm = difflib.SequenceMatcher(a=[n for _, n in ta], b=[n for _, n in tb], autojunk=False)
    return [(ta[blk.a + k][0] + ta[blk.a + k][1], tb[blk.b + k][0] + tb[blk.b + k][1])
            for blk in sm.get_matching_blocks() for k in range(blk.size)
            if ta[blk.a + k][0] and tb[blk.b + k][0] and ta[blk.a + k][0] != tb[blk.b + k][0]]


def _op_set_mismatch(ta: list, tb: list) -> list:
    """Không phụ thuộc thứ tự (bảng chép theo hàng ở bên này, theo cột ở bên kia):
    với mỗi số có ở cả 2 dãy, tập dấu khác rỗng phải trùng nhau."""
    oa, ob = {}, {}
    for op, n in ta:
        if op:
            oa.setdefault(n, set()).add(op)
    for op, n in tb:
        if op:
            ob.setdefault(n, set()).add(op)
    return [("".join(sorted(oa[n])) + n, "".join(sorted(ob[n])) + n)
            for n in sorted(set(oa) & set(ob), key=numkey) if oa[n] != ob[n]]


def rule_boundary_diffs(a: dict, b: dict) -> list:
    """Ghép quy tắc theo CẢ HAI CHIỀU (A→B trùng số nhiều nhất, và B→A), căn 2 dãy theo con số,
    báo mọi vị trí cùng số mà khác dấu. Ghép 2 chiều để quy tắc bị chép lặp (2 bảng giống hệt)
    không che mất chỗ lệch ở bản sao còn lại. Bắt được ≥50 → >50 dù 50 còn xuất hiện chỗ khác."""
    ra_ = [(r, rule_tokens(r)) for r in a.get("rules", [])]
    rb_ = [(r, rule_tokens(r)) for r in b.get("rules", [])]
    ra_ = [x for x in ra_ if x[1]]
    rb_ = [x for x in rb_ if x[1]]
    if not ra_ or not rb_:
        return []
    pairs = set()
    for i, (_, ta) in enumerate(ra_):
        na = {n for _, n in ta}
        pairs.add((i, max(range(len(rb_)), key=lambda j: _jacc(na, {n for _, n in rb_[j][1]}))))
    for j, (_, tb) in enumerate(rb_):
        nb = {n for _, n in tb}
        pairs.add((max(range(len(ra_)), key=lambda i: _jacc(nb, {n for _, n in ra_[i][1]})), j))
    out = []
    for i, j in sorted(pairs):
        if _jacc({n for _, n in ra_[i][1]}, {n for _, n in rb_[j][1]}) < MIN_PAIR_SIM:
            continue
        mm = _op_mismatch(ra_[i][1], rb_[j][1]) + _op_set_mismatch(ra_[i][1], rb_[j][1])
        if mm:
            out.append({"A": ra_[i][0].get("rule_no"), "B": rb_[j][0].get("rule_no"),
                        "page": ra_[i][0].get("page"), "mismatch": mm})
    return out


def compare(did: str) -> dict:
    a = json.loads((HERE / "reads" / f"{did}_A.json").read_text(encoding="utf-8"))
    b = json.loads((HERE / "reads" / f"{did}_B.json").read_text(encoding="utf-8"))
    pa, pb = by_page(a), by_page(b)
    diff = {}
    for p in sorted(set(pa) | set(pb)):
        sa, sb = set(pa.get(p, {})), set(pb.get(p, {}))
        oa, ob = sorted(sa - sb, key=numkey), sorted(sb - sa, key=numkey)
        if oa or ob:
            diff[p] = {"only_A": oa, "only_B": ob}
    res = {"doc": did, "rules_A": len(a.get("rules", [])), "rules_B": len(b.get("rules", [])),
           "pages_read_A": len(a.get("pages_read", [])), "pages_read_B": len(b.get("pages_read", [])),
           "uncertain_A": [r.get("rule_no") for r in a.get("rules", []) if r.get("uncertain")],
           "uncertain_B": [r.get("rule_no") for r in b.get("rules", []) if r.get("uncertain")],
           "page_diffs": diff,
           "doc_only_A": sorted(set().union(*[set(c) for c in pa.values()] or [set()]) - set().union(*[set(c) for c in pb.values()] or [set()]), key=numkey),
           "doc_only_B": sorted(set().union(*[set(c) for c in pb.values()] or [set()]) - set().union(*[set(c) for c in pa.values()] or [set()]), key=numkey),
           "boundary": boundary_diffs(a, b),
           "boundary_by_rule": rule_boundary_diffs(a, b),
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
        bd = r["boundary"]
        print(f"   ĐIỀU KIỆN BIÊN: lệch dấu {len(bd['conflict'])} · một bên có dấu {len(bd['one_sided'])}")
        for n, d in bd["conflict"].items():
            print(f"     ! {n}: A {d['A']} | B {d['B']}")
        print(f"   BIÊN THEO QUY TẮC (cả 2 bên đều có dấu, khác nhau): {len(r['boundary_by_rule'])}")
        for x in r["boundary_by_rule"]:
            print(f"     !! A#{x['A']} vs B#{x['B']} tr.{x['page']}: {x['mismatch']}")
        for p, d in r["page_diffs"].items():
            print(f"   tr.{p}: chỉ A {d['only_A'][:25]} | chỉ B {d['only_B'][:25]}")
