"""Tải 7 PDF bằng chứng W24 lên R2 bucket `tj-w24-evidence` và triển khai Worker chỉ-đọc `tj-w24-evidence`.

Học từ W02 (tools/game-worker/upload_audio.py):
  1) tạo bucket nếu chưa có,
  2) triển khai TẠM Worker có PUT với khoá ngẫu nhiên sinh lúc chạy (không lưu ở đâu),
  3) PUT từng PDF với key  evidence/<Source_ID>.pdf  (tên lấy từ knowledge/sources/source-registry.csv),
  4) LUÔN triển khai lại Worker CHỈ-ĐỌC (worker.js) -> khoá tạm hết hiệu lực, kể cả khi lỗi giữa chừng,
  5) kiểm SHA-256 qua GET công khai, ghi manifest.json (Source_ID, size, sha256, url).
Cần biến môi trường: CF_ACCOUNT_ID, CF_W24_TOKEN (quyền Workers Scripts Edit + Workers R2 Storage Edit; hết hạn 2026-12-26).
PDF đọc từ máy (private/sources/...). Dùng:  py -3 infra/evidence-worker/deploy_evidence.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCRIPT = BUCKET = "tj-w24-evidence"
HOST = "https://tj-w24-evidence.tj-wordloop.workers.dev"
UA = {"User-Agent": "tj-w24-evidence"}

UPLOAD_JS = """
const PATH_OK = /^\\/evidence\\/(SRC-[A-Z0-9-]+\\.pdf)$/;
export default { async fetch(req, env) {
  if (req.method !== "PUT") return new Response("temp uploader", { status: 405 });
  if (req.headers.get("x-upload-key") !== env.UPLOAD_KEY) return new Response("forbidden", { status: 403 });
  const mm = PATH_OK.exec(new URL(req.url).pathname);
  if (!mm) return new Response("bad path", { status: 400 });
  await env.BUCKET.put("evidence/" + mm[1], req.body, { httpMetadata: { contentType: "application/pdf" } });
  return new Response("ok");
} };
"""


def _env(name: str) -> str:
    v = os.environ.get(name)
    if not v and os.name == "nt":  # biến User mới đặt có thể chưa vào tiến trình hiện tại
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            try:
                v = winreg.QueryValueEx(k, name)[0]
            except FileNotFoundError:
                v = None
    if not v:
        raise SystemExit(f"Thiếu biến môi trường {name}")
    return v


def _cf(path: str, token: str, method: str = "GET", data: bytes | None = None, ctype: str = "application/json") -> dict:
    req = urllib.request.Request("https://api.cloudflare.com/client/v4" + path, method=method, data=data,
                                 headers={"Authorization": "Bearer " + token, "Content-Type": ctype, **UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode() or "{}")


def _deploy(acct: str, token: str, js: str, key: str | None = None) -> None:
    bindings = [{"type": "r2_bucket", "name": "BUCKET", "bucket_name": BUCKET}]
    if key:
        bindings.append({"type": "secret_text", "name": "UPLOAD_KEY", "text": key})
    meta = {"main_module": "worker.js", "compatibility_date": "2025-01-01", "bindings": bindings}
    b = uuid.uuid4().hex
    body = (f'--{b}\r\nContent-Disposition: form-data; name="metadata"\r\nContent-Type: application/json\r\n\r\n{json.dumps(meta)}\r\n'
            f'--{b}\r\nContent-Disposition: form-data; name="worker.js"; filename="worker.js"\r\n'
            f'Content-Type: application/javascript+module\r\n\r\n{js}\r\n--{b}--\r\n').encode("utf-8")
    r = _cf(f"/accounts/{acct}/workers/scripts/{SCRIPT}", token, "PUT", body, f"multipart/form-data; boundary={b}")
    if not r.get("success"):
        raise SystemExit(f"Không triển khai được Worker: {r.get('errors')}")


def load_sources() -> dict[str, tuple[Path, str]]:
    out = {}
    with (REPO / "knowledge/sources/source-registry.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rel = r["Local_Relative_Path"].strip()
            if rel.lower().endswith(".pdf"):
                out[r["Source_ID"].strip()] = (REPO / rel, r["SHA256_Hash"].strip().lower())
    return out


def main() -> int:
    acct, token = _env("CF_ACCOUNT_ID"), _env("CF_W24_TOKEN")
    sources = load_sources()
    for sid, (p, sha) in sources.items():
        if not p.is_file():
            raise SystemExit(f"Thiếu file trên máy: {sid} -> {p}")
        if hashlib.sha256(p.read_bytes()).hexdigest() != sha:
            raise SystemExit(f"SHA-256 trên máy không khớp registry: {sid}")

    names = [b["name"] for b in _cf(f"/accounts/{acct}/r2/buckets", token).get("result", {}).get("buckets", [])]
    if BUCKET not in names:
        r = _cf(f"/accounts/{acct}/r2/buckets", token, "POST", json.dumps({"name": BUCKET}).encode())
        if not r.get("success"):
            raise SystemExit(f"Không tạo được bucket: {r.get('errors')}")
        print("đã tạo bucket", BUCKET)

    key = secrets.token_urlsafe(24)
    final_js = (HERE / "worker.js").read_text(encoding="utf-8")
    _deploy(acct, token, UPLOAD_JS, key)
    sub = _cf(f"/accounts/{acct}/workers/scripts/{SCRIPT}/subdomain", token, "POST", json.dumps({"enabled": True}).encode())
    if not sub.get("success"):
        print("cảnh báo bật workers.dev:", sub.get("errors"))
    try:
        time.sleep(8)
        for sid, (p, _) in sources.items():
            req = urllib.request.Request(f"{HOST}/evidence/{sid}.pdf", data=p.read_bytes(), method="PUT",
                                         headers={"x-upload-key": key, "content-type": "application/pdf", **UA})
            for attempt in range(3):
                try:
                    if urllib.request.urlopen(req, timeout=900).read() == b"ok":
                        break
                except OSError as e:  # URLError, ConnectionResetError, timeout
                    print("  thử lại", sid, type(e).__name__)
                time.sleep(4)
            else:
                raise SystemExit(f"Ghi thất bại: {sid}")
            print("đã ghi", sid, p.stat().st_size)
    finally:
        _deploy(acct, token, final_js)
        print("đã triển khai lại Worker chỉ-đọc")

    time.sleep(8)
    manifest, ok_all = {"base_url": HOST, "files": {}}, True
    for sid, (p, sha) in sources.items():
        url = f"{HOST}/evidence/{sid}.pdf"
        got = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
        good = hashlib.sha256(got).hexdigest() == sha
        ok_all &= good
        print(("OK   " if good else "LỆCH ") + sid, len(got))
        manifest["files"][sid] = {"url": url, "size": len(got), "sha256": sha}
    put = urllib.request.Request(f"{HOST}/evidence/x.pdf", data=b"x", method="PUT", headers=UA)
    try:
        urllib.request.urlopen(put, timeout=30)
        print("LỖI: Worker vẫn nhận PUT")
        ok_all = False
    except urllib.error.HTTPError as e:
        print("PUT công khai bị chặn:", e.code)
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
