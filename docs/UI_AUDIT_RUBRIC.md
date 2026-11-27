# UI Audit Rubric — W24 Strategy Lab

Thang chấm cố định cho mọi lần audit giao diện `outputs/interactive/W24_Strategy_Lab.html` (bản đầy đủ) và
`outputs/public/W24_Strategy_Lab.html` (bản công khai). Không đổi trọng số giữa các lần audit; muốn đổi thì ghi
quyết định mới vào `docs/decisions/` trước.

## Phạm vi mỗi lần chấm

- **Hai bản:** đầy đủ + công khai.
- **Mọi tab** trong `TABS`, kể cả nhóm "Phân tích sâu & công cụ".
- **Bốn độ rộng:** 390px (điện thoại), 820px (máy tính bảng), 1280px, ≥1440px (máy tính).
- **Hai chế độ màu:** sáng và tối.
- **Trạng thái tương tác chính:**
  - thanh bên ghim / bỏ ghim;
  - nhóm Phân tích sâu đóng / mở;
  - nút Tháng | Quý | Năm;
  - chọn vùng ở trang 3;
  - khung PDF bên phải đang mở.

## 5 tiêu chí (tổng 100 điểm)

| # | Tiêu chí | Điểm | Đạt khi | Lỗi P1 (chặn phát hành) |
|---|---|---|---|---|
| 1 | **Không bị cắt / che (No Clipping/Overlap)** | 30 | Mọi nút, nhãn, thẻ số, biểu đồ hiện trọn vẹn; không phần tử nào đè lên phần tử khác (thanh điều khiển dính, thanh bên, khung PDF, tooltip). | Một nút hoặc điều khiển bị che / cắt đến mức không bấm hoặc không đọc được (ví dụ nút "Từ điển & PDF" bị thanh điều khiển che nửa dưới). |
| 2 | **Không tràn ngang (Zero Overflow)** | 25 | `document.documentElement.scrollWidth ≤ innerWidth` ở mọi tab và độ rộng; bảng rộng chỉ cuộn bên trong `.tbl-wrap`. | Trang cuộn ngang ở bất kỳ độ rộng nào; hoặc chữ / số bị cắt ngoài khung không có cách xem. |
| 3 | **Chữ nguyên vẹn (Text Integrity)** | 20 | Không lỗi phông tiếng Việt, không `undefined` / `NaN` / `null` / `[object Object]`, không ô trống thay cho số; số định dạng vi-VN; nhãn biểu đồ không chồng nhau. | — |
| 4 | **Câu chữ sạch (Clean Copy)** | 15 | Tên hãng thống nhất (AIA Alpha · Chubb Life · Manulife · Chính sách Đề xuất 2026); không lộ vết kỹ thuật (đường dẫn file, tên script, "engine", "Supabase", mã quyết định nội bộ, mã commit); bản đầy đủ không mang banner "Bản công khai"; bản công khai không có mã văn bản mật. | — |
| 5 | **Chạy ổn (Runtime)** | 10 | Không lỗi console khi mở trang và khi bấm qua mọi tab / điều khiển; huy hiệu tự kiểm khớp đủ ca mẫu; chuyển tab < 100 ms, không giật. | — |

## Cách trừ điểm

- **Mỗi lỗi** trừ theo mức:
  - **P1** (chặn phát hành): trừ toàn bộ điểm của tiêu chí đó.
  - **P2** (thấy rõ, có cách xem): trừ 5 điểm.
  - **P3** (thẩm mỹ nhỏ): trừ 2 điểm.
  - Điểm mỗi tiêu chí không âm.
- **Cùng một lỗi lặp ở nhiều tab hoặc nhiều độ rộng:** tính một lỗi, ghi đủ nơi xuất hiện.
- **Mỗi lỗi phải có bằng chứng:**
  - tab, độ rộng, bản (đầy đủ / công khai), chế độ màu;
  - ảnh chụp hoặc kết quả đo (toạ độ phần tử, `scrollWidth`, nội dung console).

## Ngưỡng đậu

**Đậu khi tổng ≥ 95 điểm VÀ 0 lỗi P1 ở tiêu chí 1–2.** Thiếu một trong hai điều kiện là trượt, kể cả khi tổng
điểm cao. Trượt thì sửa rồi chấm lại toàn bộ (không chấm riêng chỗ đã sửa).

## Kiểm tự động gợi ý (tiêu chí 1–2)

Chạy trong console của trang (mở qua `http://127.0.0.1`, không qua `file://`). Đoạn dưới kiểm
nút "Từ điển & PDF" không bị che và trang không tràn ngang ở mọi tab. Mở rộng `targets` khi cần kiểm thêm phần tử:

```js
const targets = ["#glOpen", "#pinBtn"];
const bad = [];
for (const k of TABS.map(t => t[0])) {
  state.tab = k; state.refOpen = true; showTab(); scrollTo(0, 0);
  if (document.documentElement.scrollWidth > innerWidth + 1) bad.push(`${k}: tràn ngang`);
  for (const sel of targets) {
    const el = document.querySelector(sel); if (!el || !el.offsetParent) continue;
    const b = el.getBoundingClientRect();
    const hit = [[b.left + b.width / 2, b.top + 3], [b.left + b.width / 2, b.bottom - 3]]
      .every(([x, y]) => { const e = document.elementFromPoint(x, y); return e && e.closest(sel); });
    if (!hit) bad.push(`${k}: ${sel} bị che/cắt`);
  }
}
console.log(bad.length ? bad : "OK");
```

Đổi độ rộng bằng một `<iframe>` cùng địa chỉ (390 / 820 / 1280px) rồi chạy cùng đoạn trong `iframe.contentWindow`.

## Mẫu biên bản

| Lần | Ngày | Commit | Bản | 1 (30) | 2 (25) | 3 (20) | 4 (15) | 5 (10) | Tổng | P1 (mục 1–2) | Kết quả |
|---|---|---|---|---|---|---|---|---|---|---|---|
| … | YYYY-MM-DD | `sha` | đầy đủ / công khai | | | | | | | 0 | Đậu / Trượt |
