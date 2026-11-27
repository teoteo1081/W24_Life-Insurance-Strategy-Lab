# Nhánh `claude/fresh-approach` — làm lại đề bài từ đầu theo cách của Claude

**Đề bài:** “Phân tích các chính sách thu nhập giữa các công ty, và đề xuất chính sách phù hợp tại thị trường VN, nhằm thúc đẩy gia tăng doanh số, chất lượng kinh doanh và hiệu quả về mặt chi phí (ROI).”

Nhánh này không sửa gì trên `main`. Mọi thứ mới nằm trong thư mục `fresh/`.

## Khác gì so với bản trên `main`

| | Bản `main` | Nhánh này |
|---|---|---|
| Đọc PDF | 1 lượt trích, kiểm bằng mẫu | Mỗi văn bản 2 lượt đọc độc lập (theo chữ và theo ảnh); chỗ lệch mở lại trang gốc rồi mới chốt; đối chiếu ngược với 133 quy tắc của bản `main` |
| Đơn vị phân tích | 4 mốc quy mô, đại lý bán đều | Một "khu vực mẫu" có đại lý bán lệch, có người nghỉ, có hợp đồng hủy ngay từ đầu |
| Thước đo chi phí | Chi phí / FYP | Chi phí / phí còn duy trì sau 13 tháng (gộp được cả chi phí lẫn chất lượng) |
| Đề xuất | Kế thừa bộ tham số đã hiệu chỉnh, nhiều tham số | Ít tham số, mỗi tham số có lý do và nguồn |
| Sản phẩm chính | Trang HTML tương tác | Memo 2–3 trang + 1 file Excel tính được |

## Các bước

1. **Đọc nguồn (đang làm).** 9 PDF, 135 trang; bản scan Chubb `CHH0DCEB260003V` (15 trang) chỉ đọc bằng ảnh.
   Kết quả: `fresh/sources/rules_verified.json` + `fresh/sources/READING_AUDIT.md` (chỗ 2 lượt đọc lệch nhau, cách chốt, chỗ bản `main` đọc sai).
2. **Khung so sánh.** Cùng một khu vực mẫu chạy qua cơ chế của 3 hãng.
3. **Đề xuất.** Thiết kế từ 3 mục tiêu của đề bài, mỗi mục tiêu một chỉ số đo và ngưỡng thắng/thua.
4. **Kiểm tra căng.** Năng suất giảm, K2 giảm, sản phẩm nghiêng bảo vệ thuần, trần pháp lý.
5. **Memo + Excel.**
