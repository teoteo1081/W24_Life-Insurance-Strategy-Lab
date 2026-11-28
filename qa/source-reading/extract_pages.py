"""Tách 9 PDF nguồn thành chữ theo trang + ảnh từng trang — đầu vào cho 2 lượt đọc độc lập và check_bounds_vs_text.py.

Đầu ra (không commit, thư mục work/ bị gitignore):
  work/text/<ID>.txt        mỗi trang mở đầu "===== <ID> — TRANG n ====="
  work/img/<ID>/pNN.png     150 dpi; văn bản scan (không có lớp chữ) 200 dpi
Chạy:  py -3 -X utf8 qa/source-reading/extract_pages.py [--out <thư mục>] [ID ...]
Sau đó: py -3 -X utf8 qa/source-reading/check_bounds_vs_text.py qa/source-reading/work/text --scanned CHB-003
Cần: pymupdf (py -3 -m pip install pymupdf).
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
# Mã ngắn dùng trong reads/ và rules_verified.json → Source_ID trong knowledge/sources/source-registry.csv
DOCS = {
    "AIA-069": "SRC-POL-AIA-ALP-001", "AIA-034": "SRC-POL-AIA-ALP-002", "AIA-035": "SRC-POL-AIA-ALP-003",
    "MNL-048": "SRC-POL-MNL-001", "MNL-046": "SRC-POL-MNL-002", "MNL-047": "SRC-POL-MNL-003",
    "CHB-007": "SRC-POL-CHB-001", "CHB-008": "SRC-POL-CHB-002", "CHB-003": "SRC-POL-CHB-003",
}


def registry_paths() -> dict:
    with open(REPO / "knowledge/sources/source-registry.csv", encoding="utf-8") as f:
        return {r["Source_ID"]: REPO / r["Local_Relative_Path"].strip() for r in csv.DictReader(f)}


def extract(doc_id: str, pdf: Path, out: Path) -> tuple:
    import pymupdf
    (out / "text").mkdir(parents=True, exist_ok=True)
    img_dir = out / "img" / doc_id
    img_dir.mkdir(parents=True, exist_ok=True)
    parts, chars = [], 0
    with pymupdf.open(pdf) as d:
        for i, page in enumerate(d, 1):
            t = page.get_text()
            chars += len(t.strip())
            parts.append(f"===== {doc_id} — TRANG {i} =====\n{t}")
        dpi = 200 if chars < 500 else 150                       # bản scan: ảnh nét hơn để đọc bằng mắt
        for i, page in enumerate(d, 1):
            page.get_pixmap(dpi=dpi).save(img_dir / f"p{i:02d}.png")
        n = len(d)
    (out / "text" / f"{doc_id}.txt").write_text("\n".join(parts), encoding="utf-8")
    return n, chars, dpi


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=str(HERE / "work"))
    ap.add_argument("ids", nargs="*", help="mã văn bản (mặc định: cả 9)")
    a = ap.parse_args()
    paths, out = registry_paths(), Path(a.out)
    missing = []
    for did in a.ids or list(DOCS):
        if did not in DOCS:
            sys.exit(f"mã không biết: {did} (có: {', '.join(DOCS)})")
        pdf = paths.get(DOCS[did])
        if not pdf or not pdf.is_file():
            missing.append(f"{did}: {pdf}")
            continue
        n, chars, dpi = extract(did, pdf, out)
        print(f"{did}: {n} trang · {chars} ký tự lớp chữ · ảnh {dpi} dpi{'  (bản scan — chỉ đọc được bằng ảnh)' if chars < 500 else ''}")
    if missing:
        print("THIẾU PDF:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
