"""Tải lên R2 (bucket tj-w24-evidence) các PDF nguồn CHƯA có trong manifest.json, qua S3 API — không đụng Worker.

Khác deploy_evidence.py (tải lại cả bộ + triển khai lại Worker, cần CF_W24_TOKEN): công cụ này chỉ bổ sung file thiếu.
Khóa đọc từ file dotenv (mặc định ~/.tj-secrets/kho.env: R2_ENDPOINT, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY),
không in ra, không ghi vào repo. Sau khi ghi: GET công khai qua Worker chỉ-đọc, so SHA-256 với registry rồi mới ghi manifest.
Dùng:  py -3 infra/evidence-worker/upload_missing_s3.py [--env <đường dẫn dotenv>] [--dry-run]
Cần:   boto3
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from deploy_evidence import BUCKET, HOST, UA, load_sources  # noqa: E402


def read_env(path: Path) -> dict:
    env = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.removeprefix("export ").split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    missing = [k for k in ("R2_ENDPOINT", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY") if not env.get(k)]
    if missing:
        raise SystemExit(f"File {path} thiếu biến: {missing}")
    return env


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--env", default=str(Path.home() / ".tj-secrets" / "kho.env"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    mpath = HERE / "manifest.json"
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    sources = load_sources()
    todo = {sid: v for sid, v in sources.items() if sid.startswith("SRC-POL-") and sid not in manifest["files"]}
    if not todo:
        print("Không có PDF nào thiếu trên R2.")
        return 0
    for sid, (p, sha) in todo.items():
        if not p.is_file():
            raise SystemExit(f"Thiếu file trên máy: {sid} -> {p}")
        if hashlib.sha256(p.read_bytes()).hexdigest() != sha:
            raise SystemExit(f"SHA-256 trên máy không khớp registry: {sid}")
    print("Sẽ tải:", ", ".join(todo))
    if a.dry_run:
        return 0
    import boto3
    env = read_env(Path(a.env))
    s3 = boto3.client("s3", endpoint_url=env["R2_ENDPOINT"], aws_access_key_id=env["R2_ACCESS_KEY_ID"],
                      aws_secret_access_key=env["R2_SECRET_ACCESS_KEY"], region_name="auto")
    for sid, (p, _) in todo.items():
        s3.put_object(Bucket=BUCKET, Key=f"evidence/{sid}.pdf", Body=p.read_bytes(), ContentType="application/pdf")
        print("đã ghi", sid, p.stat().st_size)
    time.sleep(3)
    ok_all = True
    for sid, (p, sha) in todo.items():
        url = f"{HOST}/evidence/{sid}.pdf"
        got = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read()
        good = hashlib.sha256(got).hexdigest() == sha
        ok_all &= good
        print(("OK   " if good else "LỆCH ") + sid, len(got))
        if good:
            manifest["files"][sid] = {"url": url, "size": len(got), "sha256": sha}
    mpath.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
