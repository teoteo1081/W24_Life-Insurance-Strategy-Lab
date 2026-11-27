"""Chuẩn bị một worktree phụ (git worktree add) để chạy được build và quality gate.

`private/` (PDF nguồn của các hãng) bị gitignore nên chỉ có ở worktree chính. Script này tạo
liên kết `private` → `<worktree chính>/private` (Windows: junction, không cần quyền admin;
macOS/Linux: symlink). Liên kết nằm trong vùng gitignore nên không bao giờ vào commit;
quality gate vẫn kiểm SHA-256 từng PDF như ở worktree chính.

Chạy: python scripts/setup_worktree.py        (an toàn khi chạy lại; không ghi đè thư mục thật)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def main_worktree(repo: Path) -> Path | None:
    common = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "--path-format=absolute", "--git-common-dir"], encoding="utf-8"
    ).strip()
    main = Path(common).parent
    return None if main.resolve() == repo.resolve() else main


def main() -> int:
    main_wt = main_worktree(REPO)
    if main_wt is None:
        print("Đây là worktree chính — không cần làm gì.")
        return 0
    link, target = REPO / "private", main_wt / "private"
    if not target.is_dir():
        print(f"Worktree chính chưa có private/ — không có gì để liên kết.")
        return 1
    if link.exists():
        same = link.resolve() == target.resolve()
        print("private/ đã trỏ đúng worktree chính." if same else "private/ đã tồn tại (thư mục riêng) — giữ nguyên, không ghi đè.")
        return 0 if same else 1
    if os.name == "nt":
        subprocess.check_call(["cmd", "/c", "mklink", "/J", str(link), str(target)], stdout=subprocess.DEVNULL)
    else:
        link.symlink_to(target, target_is_directory=True)
    print("Đã liên kết private/ → private/ của worktree chính.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
