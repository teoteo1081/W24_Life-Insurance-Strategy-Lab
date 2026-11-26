# Audit giao diện trang HTML — `outputs/interactive/W24_Strategy_Lab.html`

**Ngày:** 2026-11-27 · **Người audit:** Claude (phiên tư vấn TJ) · **Trạng thái:** `SELF_VERIFIED` (người sửa cũng là người audit).
**Khung tham chiếu:** khung review 4 giai đoạn / 7 chiều, checklist WCAG 2.1 AA và checklist responsive trước bàn giao trong thư viện skill W14 của TJ. Chỉ đọc tham chiếu từ W14, không chép nội dung skill bên thứ ba vào repo này.

## Cách đo
- **Tương phản:** tính tỷ lệ WCAG cho mọi cặp token màu ở cả chế độ sáng và tối, bằng script đọc trực tiếp `web/template.html`.
- **DOM:** quét ô nhập thiếu nhãn, chữ dưới 13px, link bỏ qua menu, `prefers-reduced-motion`, emoji dùng làm biểu tượng, vai trò ARIA.
- **Responsive:** nhúng trang vào khung 375 / 768 / 1024px, đo `scrollWidth` trên cả 8 trang, đo chiều cao menu. Không thu nhỏ được cửa sổ Chrome thật vì tỷ lệ màn hình của máy.

## Phát hiện và xử lý

| Mức | Vấn đề | Trước | Sau |
|---|---|---|---|
| HIGH | Trên điện thoại, menu đẩy nội dung xuống dưới màn hình đầu | Menu cao 543/800px | Menu thành các hàng cuộn ngang, cao 150px; tiêu đề và kết luận lên màn hình đầu |
| HIGH | Thanh kéo không có tên cho trình đọc màn hình | 23 ô thiếu nhãn | 0 (thêm `aria-label`) |
| HIGH | Thanh màu các phương án phụ trong biểu đồ quá nhạt | 1,67:1 (sáng) / 2,18:1 (tối) | 3,56:1 / 4,50:1 |
| MEDIUM | Viền ô nhập và nút quá mờ (WCAG 1.4.11) | 1,28:1 | 3,09:1 / 4,47:1 |
| MEDIUM | Chữ dưới 13px (tiêu đề menu, ghi chú, nhãn, trục biểu đồ 11px) | 8 loại phần tử | 0 |
| MEDIUM | Emoji dùng làm biểu tượng (📄 ⭐ ↺) | 96 nút/link | Biểu tượng SVG cho tài liệu, nhãn chữ "đề xuất" |
| MEDIUM | Khai báo `role=tab` nhưng không có tabpanel | 7 nút | Nút điều hướng với `aria-current="page"`, có số thứ tự bước |
| LOW | Không có link "bỏ qua menu" và vùng `main` | Không có | Có (`#main`) |
| LOW | Không tôn trọng cài đặt giảm chuyển động | Không có | Có |
| LOW | Kết luận đổi khi kéo thông số mà trình đọc màn hình không biết | Không có | `aria-live="polite"` trên câu kết luận |

## Đạt từ trước
- Mọi cặp chữ trên nền đạt WCAG AA ở cả chế độ sáng và tối (thấp nhất 4,74:1).
- Không trang nào bị cuộn ngang ở 375, 768 và 1024px.
- Có trạng thái focus; một màu nhấn duy nhất; trang Tổng quan mở đầu bằng kết luận.
- Không trang nào ra NaN hay lỗi JS khi đổi phương án, K2 hoặc trang.

## Thay đổi đi kèm (theo kịch bản trình bày đã thống nhất)
- Thứ tự menu: Tổng quan → Gói thu nhập theo cấp → Học từ đối thủ → Thu nhập & chi phí → Chấm điểm → Bằng chứng → Cách tính & giả định → Tự chỉnh thông số.
- **Chế độ trình bày:** chữ lớn hơn khoảng 16%, ẩn trang "Tự chỉnh" và phương án "Tự chỉnh".

## Chưa làm
- Chưa kiểm bằng trình đọc màn hình thật (NVDA) và chưa thử điều hướng chỉ bằng bàn phím trên toàn trang.
- 44 cấu phần thu nhập của đối thủ vẫn là chữ không dấu, theo nguyên văn dữ liệu trích xuất (chờ TJ quyết).
