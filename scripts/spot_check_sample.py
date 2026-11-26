"""In mẫu 2 quy tắc/PDF kèm văn bản trang được trích dẫn để kiểm độc lập (quy tắc ↔ trang PDF).
Trang lấy theo số đầu tiên sau 'p.' trong Source_ID_And_Page. Dùng PyMuPDF đọc lớp chữ của PDF trên máy."""
import csv, random, re, sys
from pathlib import Path
import pymupdf
REPO = Path(__file__).resolve().parents[1]
src = {r["Source_ID"]: REPO / r["Local_Relative_Path"] for r in csv.DictReader(open(REPO/"knowledge/sources/source-registry.csv", encoding="utf-8")) if r["Local_Relative_Path"].lower().endswith(".pdf")}
rules = list(csv.DictReader(open(REPO/"knowledge/business-rules/business-rules-catalog.csv", encoding="utf-8")))
rng = random.Random(24)
for sid, path in src.items():
    cand = [r for r in rules if sid in r["Source_ID_And_Page"] and re.search(r"p\.?\s*(\d+)", r["Source_ID_And_Page"].split(sid,1)[1])]
    doc = pymupdf.open(path)
    for r in rng.sample(cand, min(2, len(cand))):
        pg = int(re.search(r"p\.?\s*(\d+)", r["Source_ID_And_Page"].split(sid,1)[1]).group(1))
        txt = doc[pg-1].get_text().replace("\n", " ") if pg <= doc.page_count else "<OUT OF RANGE>"
        print(f"=== {r['Rule_ID']} | {r['Source_ID_And_Page']} | pdf pages={doc.page_count}")
        for k in ("Rank_Tier","Income_Type","Threshold","Tier_Structure","Rate_Pct","Fixed_Amount_VND","Cap_Limit"):
            print(f"  {k}: {r[k][:220]}")
        print(f"  PAGE {pg} TEXT ({len(txt)} chars): {txt[:900]}")
