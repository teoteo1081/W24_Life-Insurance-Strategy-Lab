/* Cloudflare Worker "tj-w24-evidence": phát 7 PDF chính sách (bằng chứng) của W24 từ R2 bucket `tj-w24-evidence`.
   Mô hình học từ W02 `tj-game`: bucket PRIVATE (không r2.dev, không tên miền), đường vào duy nhất là Worker này.

   CHỈ ĐỌC (GET/HEAD) — không PUT/DELETE/list. Chỉ phục vụ đúng mẫu  /evidence/SRC-<...>.pdf
   Quyết định TJ (2026-11-26): "ai có link là xem được" — không có lớp đăng nhập.
   Trang HTML mở thẳng tới trang bằng chứng:  <base>/evidence/SRC-POL-CHB-002.pdf#page=5
   Content-Disposition: inline để trình duyệt hiển thị PDF (và nhảy #page) thay vì tải về.

   Luôn nằm trong gói Free: Worker Free chặn cứng 100.000 request/ngày; không ghi/liệt kê => 0 Class A;
   dung lượng vài MB trên 10 GB dùng chung với W02. Binding: BUCKET = bucket `tj-w24-evidence`. */
const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET,HEAD,OPTIONS",
  "access-control-allow-headers": "range,if-none-match",
  "access-control-expose-headers": "content-length,content-range,accept-ranges,etag",
  "access-control-max-age": "86400",
};
const PATH_OK = /^\/evidence\/(SRC-[A-Z0-9-]+\.pdf)$/;

export default {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
    if (req.method !== "GET" && req.method !== "HEAD") return new Response("method not allowed", { status: 405, headers: CORS });
    const m = PATH_OK.exec(new URL(req.url).pathname);
    if (!m) return new Response("not found", { status: 404, headers: CORS });
    const key = "evidence/" + m[1];

    const o = req.method === "HEAD" ? await env.BUCKET.head(key) : await env.BUCKET.get(key, { range: req.headers, onlyIf: req.headers });
    if (!o) return new Response("not found", { status: 404, headers: CORS });

    const h = new Headers(CORS);
    o.writeHttpMetadata(h);
    h.set("etag", o.httpEtag);
    h.set("accept-ranges", "bytes");
    h.set("cache-control", "public, max-age=86400");
    h.set("content-type", "application/pdf");
    h.set("content-disposition", 'inline; filename="' + m[1] + '"');
    h.set("x-robots-tag", "noindex, nofollow");

    if (req.method === "HEAD") { h.set("content-length", String(o.size)); return new Response(null, { status: 200, headers: h }); }
    if (!o.body) return new Response(null, { status: 304, headers: h });
    let status = 200;
    if (req.headers.get("range") && o.range) {
      const off = o.range.offset || 0, len = o.range.length != null ? o.range.length : o.size - off;
      h.set("content-range", "bytes " + off + "-" + (off + len - 1) + "/" + o.size);
      h.set("content-length", String(len));
      status = 206;
    } else h.set("content-length", String(o.size));
    return new Response(o.body, { status, headers: h });
  },
};
