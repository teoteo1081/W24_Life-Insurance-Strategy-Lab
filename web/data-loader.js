/* W24 data-loader — lớp ĐỌC dữ liệu cho giao diện (data contract: supabase/schema.sql).
 *
 * Thứ tự nguồn:
 *   1. Supabase (PostgREST) nếu có cấu hình URL + anon key và đang online.
 *   2. Fallback: snapshot nhúng sẵn trong trang (window.W24_LOCAL_SNAPSHOT, sinh bởi scripts/sync_to_supabase.py --dry-run)
 *      — dùng khi mở file offline, không có key, lỗi mạng hoặc quá thời gian chờ.
 *
 * Cấu hình (chỉ ANON key — công khai theo thiết kế Supabase, được RLS bảo vệ; KHÔNG BAO GIỜ đặt service key ở đây):
 *   <meta name="w24-supabase-url" content="https://<project>.supabase.co">
 *   <meta name="w24-supabase-anon-key" content="<anon key>">
 *   hoặc window.W24_SUPABASE = {url, anonKey} trước khi gọi load().
 *
 * Gộp dữ liệu (merge = true, mặc định): dòng từ Supabase ghi đè dòng local cùng khóa; dòng chỉ có ở local (ví dụ dòng
 * 'restricted' mà người xem ẩn danh không được đọc) được giữ lại từ snapshot nhúng.
 */
(function (root) {
  "use strict";
  var TABLES = {benchmark_results: "id", role_benefit_matrix: "id", glossary_terms: "abbr", pdf_bookmarks: "id"};

  function meta(name) {
    if (typeof document === "undefined") return "";
    var el = document.querySelector('meta[name="' + name + '"]');
    return el ? (el.getAttribute("content") || "").trim() : "";
  }
  function config() {
    var c = root.W24_SUPABASE || {};
    return {url: String(c.url || meta("w24-supabase-url") || "").replace(/\/+$/, ""),
            anonKey: String(c.anonKey || meta("w24-supabase-anon-key") || "")};
  }
  function localSnapshot() {
    var s = root.W24_LOCAL_SNAPSHOT;
    return s && s.tables ? s : null;
  }
  function mergeRows(remote, local, key) {
    if (!local || !local.length) return remote;
    var seen = {}, out = remote.slice();
    remote.forEach(function (r) { seen[r[key]] = true; });
    local.forEach(function (r) { if (!seen[r[key]]) out.push(r); });
    return out;
  }
  function fetchTable(cfg, table, signal, token) {
    var url = cfg.url + "/rest/v1/" + table + "?select=*&order=" + TABLES[table] + ".asc";
    return fetch(url, {headers: {apikey: cfg.anonKey, Authorization: "Bearer " + (token || cfg.anonKey)}, signal: signal})
      .then(function (r) {
        if (!r.ok) throw new Error(table + ": HTTP " + r.status);
        return r.json();
      });
  }
  function fallback(reason) {
    var s = localSnapshot();
    return {source: "local", reason: reason, meta: s ? s.meta : null, tables: s ? s.tables : null};
  }

  /** load({timeoutMs, accessToken, merge}) → Promise<{source:'supabase'|'local', tables, meta, reason?}> */
  function load(opts) {
    opts = opts || {};
    var cfg = config();
    if (!cfg.url || !cfg.anonKey) return Promise.resolve(fallback("chưa cấu hình Supabase"));
    if (typeof fetch !== "function") return Promise.resolve(fallback("trình duyệt không hỗ trợ fetch"));
    if (typeof navigator !== "undefined" && navigator.onLine === false) return Promise.resolve(fallback("đang offline"));
    var ctl = typeof AbortController === "function" ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctl) ctl.abort(); }, opts.timeoutMs || 5000);
    var names = Object.keys(TABLES);
    return Promise.all(names.map(function (t) { return fetchTable(cfg, t, ctl && ctl.signal, opts.accessToken); }))
      .then(function (results) {
        var tables = {}, local = localSnapshot(), any = false;
        names.forEach(function (t, i) {
          var rows = Array.isArray(results[i]) ? results[i] : [];
          if (rows.length) any = true;
          tables[t] = opts.merge === false ? rows : mergeRows(rows, local && local.tables[t], TABLES[t]);
        });
        if (!any) return fallback("Supabase trả về rỗng");
        var synced = names.map(function (t) { return (results[names.indexOf(t)][0] || {}).synced_at; }).filter(Boolean).sort().pop() || null;
        return {source: "supabase", tables: tables, meta: {synced_at: synced, url: cfg.url}};
      })
      .catch(function (e) { return fallback(String((e && e.message) || e)); })
      .then(function (res) { clearTimeout(timer); return res; });
  }

  /* Chuyển bảng → cấu trúc trang đang dùng (DATA.glossary, DATA.pdfs). */
  function toGlossary(rows) {
    return (rows || []).map(function (r) {
      return {abbr: r.abbr, english: r.english, vietnamese: r.vietnamese, company_and_memo: r.company_and_memo,
              market_equivalent: r.market_equivalent, note: r.note, group: r.term_group, companies: r.companies || [],
              english_status: r.english_status, citations: r.citations || []};
    });
  }
  function toPdfs(rows) {
    var by = {}, order = [];
    (rows || []).slice().sort(function (a, b) { return a.file_id < b.file_id ? -1 : a.file_id > b.file_id ? 1 : a.seq - b.seq; })
      .forEach(function (r) {
        if (!by[r.file_id]) { by[r.file_id] = {file_id: r.file_id, sid: r.source_id, name: r.file_name, pages: r.page_count, url: r.evidence_url, bookmarks: []}; order.push(r.file_id); }
        by[r.file_id].bookmarks.push({t: r.title, p: r.page});
      });
    return order.map(function (k) { return by[k]; });
  }

  root.W24Data = {load: load, config: config, toGlossary: toGlossary, toPdfs: toPdfs, TABLES: TABLES};
})(typeof window !== "undefined" ? window : globalThis);
