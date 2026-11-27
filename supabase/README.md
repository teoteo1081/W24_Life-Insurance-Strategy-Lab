# Supabase — lớp dữ liệu tách rời (Decoupled)

```
Python engine + scripts  ──sync_to_supabase.py──▶  Supabase (4 bảng, RLS)  ──data-loader.js──▶  HTML
   (nguồn sự thật)            service key (.env)        lưu kết quả              anon key (meta)     chỉ đọc
                                                                                  └─ offline: snapshot nhúng
```

Sửa lỗi (vd. Codex audit) = sửa Python → `python scripts/sync_to_supabase.py --prune` → web tự cập nhật, không cần build lại HTML.

## Nối project (một lần)

1. Tạo project Supabase → **SQL Editor** → chạy `supabase/schema.sql` (chạy lại an toàn).
2. Chép `supabase/env.example` thành `.env` ở gốc repo (`.env` đã bị `.gitignore` chặn), điền:
   - `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` — để script **ghi** (service key bỏ qua RLS, chỉ ở máy TJ).
   - `W24_SUPABASE_URL`, `W24_SUPABASE_ANON_KEY` — để trang **đọc** (anon/publishable key, công khai theo thiết kế).
3. `python scripts/sync_to_supabase.py --dry-run` → kiểm `web/data/snapshot.json`, rồi `python scripts/sync_to_supabase.py`.
4. `python scripts/build_html.py` → trang có thẻ meta cấu hình; mở trang thấy huy hiệu "Dữ liệu từ Supabase".

## Bảo mật (DEC-14)

| Dòng | `confidentiality` | Ai đọc được |
|---|---|---|
| Dựa trên 0046M01_2026 / 0047M01_2026 (văn bản ghi "thông tin mật") | `restricted` | Chỉ user đăng nhập có trong `w24_readers` |
| Còn lại | `public` | Mọi người có anon key |

- Thêm người đọc dữ liệu mật: `insert into public.w24_readers(user_id, note) values ('<auth.users.id>', 'TJ');`
- Không có policy ghi cho anon/authenticated; chỉ service_role ghi được.
- `build_html.py` **từ chối** nhúng khóa có dạng service key (`sb_secret_…` hoặc JWT `role=service_role`).
- Glossary: thuật ngữ có cả trích dẫn mật và công khai → bản `public` chỉ giữ trích dẫn công khai.

## Bảng

| Bảng | Khóa | Nguồn trong repo |
|---|---|---|
| `benchmark_results` | `id` | `build_interview_income_table.py` (4 mốc; `region` = `ALL` — vùng V1–V3 chưa có tham số, UNKNOWN) |
| `role_benefit_matrix` | `id` | `build_benefit_matrix.py` (84 ô = 4 mốc × 3 hãng × 6 dòng + bảng phụ Mốc 4) |
| `glossary_terms` | `abbr` | `knowledge/sources/glossary.json` |
| `pdf_bookmarks` | `id` | `knowledge/sources/pdf-bookmarks.json` (131 mục) |

Kiểm thử offline: `tests/test_supabase_contract.py` (schema ↔ payload ↔ loader; không gọi mạng).
