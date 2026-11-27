-- =============================================================================
-- W24 Life Insurance Strategy Lab — Supabase Data Contract (v1, 2026-11-27)
-- =============================================================================
-- Kiến trúc tách lớp: Python (engine + script sinh) là NGUỒN SỰ THẬT; Supabase chỉ LƯU kết quả đã sinh;
-- HTML chỉ ĐỌC (web/data-loader.js). Sửa lỗi = sửa Python → chạy lại scripts/sync_to_supabase.py.
--
-- Bảo mật theo DEC-14:
--  * Mỗi dòng có cột confidentiality: 'public' | 'restricted'. Dòng lấy số/nội dung từ 0046M01_2026 hoặc
--    0047M01_2026 (văn bản ghi "thông tin mật, không được tiết lộ") là 'restricted'.
--  * anon (khóa công khai nhúng trong HTML) chỉ đọc được dòng 'public'.
--  * Dòng 'restricted' chỉ đọc được bởi người dùng đăng nhập CÓ TÊN trong bảng w24_readers (allowlist do TJ quản lý).
--    Không dùng "mọi authenticated" vì Supabase mặc định cho phép tự đăng ký.
--  * KHÔNG có policy INSERT/UPDATE/DELETE: chỉ service_role (script Python, khóa trong .env) ghi được — service_role bỏ qua RLS.
--
-- Chạy file này một lần trong Supabase SQL Editor. Idempotent (chạy lại an toàn).
-- =============================================================================

create extension if not exists pgcrypto;

-- ---------- Allowlist người được đọc dữ liệu 'restricted' ----------
create table if not exists public.w24_readers (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  note       text,
  added_at   timestamptz not null default now()
);
alter table public.w24_readers enable row level security;
-- Không policy nào cho anon/authenticated: chỉ quản trị (service_role / SQL Editor) thêm-bớt người đọc.

create or replace function public.w24_is_reader() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.w24_readers r where r.user_id = auth.uid());
$$;
revoke all on function public.w24_is_reader() from public;
grant execute on function public.w24_is_reader() to anon, authenticated;

-- ---------- 1. benchmark_results: thu nhập & chi phí/FYP theo 4 mốc quy mô ----------
create table if not exists public.benchmark_results (
  id                    text primary key,                 -- '<milestone>|<region>|<company>|<comparison>|<title>'
  model_version         text not null,                    -- git commit của engine khi sinh
  milestone_id          text not null check (milestone_id in ('M1','M2','M3','M4')),
  milestone_label       text not null,
  producing_agents      integer not null check (producing_agents > 0),
  org_fyp_month_vnd_m   numeric not null check (org_fyp_month_vnd_m > 0),
  region                text not null default 'ALL',      -- 'ALL' | 'V1' | 'V2' | 'V3'
  company               text not null check (company in ('AIA','Chubb','Manulife')),
  comparison            text not null check (comparison in ('primary','secondary')),
  title                 text not null,
  income_basis          text not null check (income_basis in ('personal_income','net_management_fee')),
  income_vnd_m_month    numeric,                          -- NULL = UNKNOWN (không bao giờ ép thành 0)
  cash_y1_vnd_m_month   numeric,
  cost_pct_org_fyp      numeric,                          -- thu nhập / FYP tổ chức × 100
  promotion_citation    text not null,
  fee_citation          text not null,
  label                 text not null check (label in ('MODEL_OUTPUT','UNKNOWN','ASSUMPTION','VERIFIED FACT')),
  note                  text,
  confidentiality       text not null default 'public' check (confidentiality in ('public','restricted')),
  synced_at             timestamptz not null default now(),
  constraint unknown_has_no_number check (label <> 'UNKNOWN' or income_vnd_m_month is null),
  constraint region_known check (region in ('ALL','V1','V2','V3'))
);
comment on column public.benchmark_results.region is
  'Phân vùng V1/V2/V3: CHƯA có tham số vùng trong 9 PDF (UNKNOWN) — hiện chỉ sinh ALL; chỉ thêm V1–V3 khi có nguồn/giả định được TJ duyệt.';

-- ---------- 2. role_benefit_matrix: ma trận chức danh & quyền lợi ngang hàng (6 dòng) ----------
create table if not exists public.role_benefit_matrix (
  id               text primary key,                      -- '<milestone>|<matrix_table>|<company>|<row_no>'
  model_version    text not null,
  milestone_id     text not null check (milestone_id in ('M1','M2','M3','M4')),
  matrix_table     text not null check (matrix_table in ('primary','secondary')),
  company          text not null check (company in ('AIA','Chubb','Manulife')),
  title            text not null,
  row_no           smallint not null check (row_no between 1 and 6),
  row_label        text not null,
  value_text       text not null,
  citation         text not null default '',              -- '[Số Memo : Trang]' (có thể nhiều)
  label            text not null,
  confidentiality  text not null default 'public' check (confidentiality in ('public','restricted')),
  synced_at        timestamptz not null default now()
);

-- ---------- 3. glossary_terms: từ điển 6 cột, dùng chung cho Trang Từ điển & Tooltip ----------
create table if not exists public.glossary_terms (
  abbr               text primary key,
  english            text not null,
  vietnamese         text not null,
  company_and_memo   text not null,
  market_equivalent  text not null,
  note               text not null,
  term_group         text not null check (term_group in ('Chỉ số','Chức danh','Tuyến hợp đồng','Khoản thu nhập')),
  companies          text[] not null,
  english_status     text not null,
  citations          jsonb not null default '[]'::jsonb,  -- [{company,file_id,source_id,page,method}]
  confidentiality    text not null default 'public' check (confidentiality in ('public','restricted')),
  synced_at          timestamptz not null default now(),
  constraint six_fields_non_empty check (
    length(trim(english)) > 0 and length(trim(vietnamese)) > 0 and length(trim(company_and_memo)) > 0
    and length(trim(market_equivalent)) > 0 and length(trim(note)) > 0)
);

-- ---------- 4. pdf_bookmarks: mục lục 9 PDF (131 mục) ----------
create table if not exists public.pdf_bookmarks (
  id               text primary key,                      -- '<file_id>|<seq>'
  file_id          text not null,
  source_id        text not null,
  file_name        text not null,
  page_count       smallint not null check (page_count > 0),
  seq              smallint not null check (seq >= 0),
  title            text not null,
  page             smallint not null check (page > 0),
  method           text not null check (method in ('text_heading','visual_toc_p2')),
  evidence_url     text,                                  -- NULL nếu PDF chưa lên kho bằng chứng (tài liệu mật)
  confidentiality  text not null default 'public' check (confidentiality in ('public','restricted')),
  synced_at        timestamptz not null default now(),
  constraint page_within_doc check (page <= page_count)
);

create index if not exists benchmark_results_mid_idx on public.benchmark_results (milestone_id, company);
create index if not exists role_benefit_matrix_mid_idx on public.role_benefit_matrix (milestone_id, matrix_table);
create index if not exists pdf_bookmarks_file_idx on public.pdf_bookmarks (file_id, seq);

-- ---------- RLS: bật trên cả 4 bảng; chỉ có policy SELECT ----------
do $$
declare t text;
begin
  foreach t in array array['benchmark_results','role_benefit_matrix','glossary_terms','pdf_bookmarks'] loop
    execute format('alter table public.%I enable row level security', t);
    execute format('alter table public.%I force row level security', t);
    execute format('drop policy if exists %I on public.%I', t || '_read_public', t);
    execute format('drop policy if exists %I on public.%I', t || '_read_restricted', t);
    execute format($p$create policy %I on public.%I for select to anon, authenticated using (confidentiality = 'public')$p$,
                   t || '_read_public', t);
    execute format($p$create policy %I on public.%I for select to authenticated using (confidentiality = 'restricted' and public.w24_is_reader())$p$,
                   t || '_read_restricted', t);
    execute format('revoke insert, update, delete, truncate on public.%I from anon, authenticated', t);
    execute format('grant select on public.%I to anon, authenticated', t);
  end loop;
end $$;
