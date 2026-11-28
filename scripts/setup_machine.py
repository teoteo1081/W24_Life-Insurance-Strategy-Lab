"""Một lệnh để máy mới (hoặc máy khác) giống hệt máy đang làm: sau `git pull`, chạy

    py -3 scripts/setup_machine.py

Làm 3 việc, chạy lại bao nhiêu lần cũng được:
  1. Cài thư viện trong requirements.txt (openpyxl, pymupdf, pytest).
  2. Tạo lại ảnh từng trang của 9 PDF (qa/source-reading/work/img/, 232 MB — không lưu trên GitHub vì sinh lại
     y hệt từ 9 PDF đã có trong repo). Chữ tách theo trang đã có sẵn trên GitHub. Ảnh đã có thì bỏ qua.
  3. Chạy toàn bộ kiểm tra (scripts/run_checks.py) — thấy "ALL CHECKS PASSED" là máy đã sẵn sàng.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PY = [sys.executable, "-X", "utf8"]


def step(title: str, cmd: list) -> None:
    print(f"\n=== {title} ===", flush=True)
    r = subprocess.run(cmd, cwd=REPO)
    if r.returncode != 0:
        raise SystemExit(f"Dừng ở bước: {title} (mã lỗi {r.returncode})")


def main() -> int:
    step("1/3 Cài thư viện", [sys.executable, "-m", "pip", "install", "-q", "-r", str(REPO / "requirements.txt")])
    img = REPO / "qa/source-reading/work/img"
    have = sum(1 for _ in img.rglob("*.png")) if img.exists() else 0
    if have >= 135:
        print(f"\n=== 2/3 Ảnh trang: đã có {have} ảnh — bỏ qua ===")
    else:
        step("2/3 Tạo ảnh trang từ 9 PDF (khoảng 1 phút)", PY + [str(REPO / "qa/source-reading/extract_pages.py")])
    step("3/3 Kiểm tra toàn bộ", PY + [str(REPO / "scripts/run_checks.py")])
    print("\nMáy đã sẵn sàng. Đọc HANDOVER.md (mục đầu) để biết việc tiếp theo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
