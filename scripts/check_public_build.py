"""Quét an toàn bản công khai (DEC-14) TRƯỚC khi phát hành.

Kiểm (mỗi mục thất bại → exit 1):
  1. Không còn dấu vết 2 văn bản mật (0046M01 / 0047M01 / SRC-POL-MNL-002 / 003, tên file gốc).
  2. Snapshot nhúng (window.W24_LOCAL_SNAPSHOT) có 0 dòng 'restricted', meta.public_build = true,
     không có meta.confidential_files, không có điểm Manulife.
  3. Không có secret: service key Supabase (sb_secret_, JWT role=service_role), tên biến SUPABASE_SERVICE_KEY, .env.
  4. Không có đường dẫn cục bộ / thư mục private / nội dung PDF nhúng (%PDF-), không có email cá nhân.
  5. Thư mục phát hành chỉ chứa đúng các file được phép.
Chạy:  python scripts/check_public_build.py [đường_dẫn_html]
"""
from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT = REPO / "outputs/public/W24_Strategy_Lab.html"
ALLOWED_FILES = {"W24_Strategy_Lab.html"}
CONFIDENTIAL = ["0046M01", "0047M01", "SRC-POL-MNL-002", "SRC-POL-MNL-003",
                "Chinh sach chi tra danh cho Dai Ly", "Bieu phi dich vu danh cho UM+"]
SECRET_PATTERNS = [r"sb_secret_[A-Za-z0-9_\-]+", r"SUPABASE_SERVICE_KEY", r"service_role\s*[\"']?\s*[:=]", r"(?m)^\s*SUPABASE_[A-Z_]+=\S+"]
LOCAL_PATTERNS = [r"[A-Za-z]:\\\\?Users\\\\", r"[A-Za-z]:/Users/", r"file:///", r"/home/\w+/", r"private/sources", r"%PDF-",
                  r"[A-Za-z0-9._%+-]+@gmail\.com"]


def _jwt_service_roles(text: str) -> list:
    hits = []
    for tok in re.findall(r"eyJ[A-Za-z0-9_\-]+\.(eyJ[A-Za-z0-9_\-]+)\.[A-Za-z0-9_\-]+", text):
        try:
            payload = json.loads(base64.urlsafe_b64decode(tok + "=" * (-len(tok) % 4)))
        except Exception:
            continue
        if payload.get("role") == "service_role":
            hits.append(tok[:12] + "…")
    return hits


def embedded_snapshot(html: str) -> dict | None:
    m = re.search(r"window\.W24_LOCAL_SNAPSHOT\s*=\s*", html)
    if not m:
        return None
    obj, _ = json.JSONDecoder().raw_decode(html[m.end():].replace("<\\/", "</"))
    return obj


def scan(path: Path) -> list[str]:
    errors = []
    html = path.read_text(encoding="utf-8")
    for t in CONFIDENTIAL:
        n = html.count(t)
        if n:
            errors.append(f"còn {n} lần '{t}' (văn bản mật)")
    for pat in SECRET_PATTERNS + LOCAL_PATTERNS:
        found = re.findall(pat, html)
        if found:
            errors.append(f"khớp mẫu cấm {pat!r}: {found[:3]}")
    if _jwt_service_roles(html):
        errors.append("có JWT role=service_role")
    snap = embedded_snapshot(html)
    if snap is None:
        errors.append("không tìm thấy snapshot nhúng")
    else:
        meta = snap.get("meta", {})
        if meta.get("public_build") is not True:
            errors.append("snapshot không gắn public_build=true")
        if "confidential_files" in meta:
            errors.append("meta còn confidential_files")
        if "Manulife" in (meta.get("weighted_scores") or {}):
            errors.append("meta còn điểm Manulife (tính từ dữ liệu mật)")
        for t, rows in snap.get("tables", {}).items():
            bad = [r for r in rows if r.get("confidentiality") != "public"]
            if bad:
                errors.append(f"bảng {t}: {len(bad)} dòng không phải public")
    extra = sorted(p.name for p in path.parent.iterdir() if p.name not in ALLOWED_FILES)
    if extra:
        errors.append(f"thư mục phát hành có file ngoài danh sách cho phép: {extra}")
    return errors


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    path = Path(argv[0]) if argv else DEFAULT
    if not path.is_file():
        print(f"FAIL: không có {path}")
        return 1
    errors = scan(path)
    snap = embedded_snapshot(path.read_text(encoding="utf-8")) or {}
    removed = (snap.get("meta") or {}).get("restricted_rows_removed", {})
    rows = {t: len(r) for t, r in (snap.get("tables") or {}).items()}
    if errors:
        print("FAIL — bản công khai KHÔNG an toàn:")
        for e in errors:
            print("  -", e)
        return 1
    print(f"PASS — {path.name}: 0 dấu vết văn bản mật, 0 secret, 0 đường dẫn cục bộ; "
          f"đã lọc {sum(removed.values())} dòng restricted {removed}; còn {sum(rows.values())} dòng public {rows}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
