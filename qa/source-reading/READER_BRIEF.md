# Hướng dẫn cho người đọc văn bản chính sách thu nhập đại lý BHNT (Việt Nam, 2026)

Mục tiêu: trích **đầy đủ và chính xác** mọi quy tắc chi trả trong MỘT văn bản, để người khác tính thu nhập mà không cần mở lại PDF.
Độ chính xác quan trọng hơn tốc độ. Một con số sai (ví dụ 12% đọc thành 1,2%, "≥" thành ">", bậc thang bị lệch dòng) làm hỏng cả bài phân tích.

## Nguồn được phép dùng
- Chữ đã tách theo trang: `text/<ID>.txt` (mỗi trang mở đầu bằng `===== <ID> — TRANG n =====`).
- Ảnh từng trang: `img/<ID>/pNN.png` — mở bằng công cụ Read để xem như ảnh.
- **Không** mở bất kỳ file nào khác (không đọc repo W24, không đọc kết quả của người đọc khác). Bạn là người đọc độc lập.

## Bảng có nhiều cột / bậc thang
Chữ tách từ PDF hay làm lệch cột của bảng. Với MỌI bảng có số, phải mở ảnh trang đó để xác nhận từng ô. Văn bản scan (không có chữ) thì chỉ đọc bằng ảnh; nếu một chữ số mờ, ghi `"uncertain": true` và mô tả.

## Kết quả: một file JSON (UTF-8) đúng đường dẫn được giao, dạng
```json
{
  "doc_id": "...",
  "reader": "A hoặc B",
  "title_verbatim": "tên văn bản như in trên trang 1",
  "effective": "hiệu lực (nguyên văn) + trang",
  "roles": [{"title_verbatim": "...", "abbr": "...", "page": 1, "how_obtained": "đạt chỉ tiêu / bổ nhiệm / ... (nguyên văn ngắn)"}],
  "rules": [
    {
      "rule_no": 1,
      "role": "chức danh áp dụng (nguyên văn)",
      "item": "tên khoản chi trả (nguyên văn)",
      "base": "tính trên gì: FYC, FYP, RYC, phí thực thu… và kỳ (tháng/quý/năm)",
      "conditions": ["mỗi điều kiện một dòng, giữ nguyên dấu ≥ > ≤ <, đơn vị, kỳ đo"],
      "table": [["tiêu đề cột 1", "tiêu đề cột 2", "..."], ["hàng 1 ...", "..."]],
      "rate_or_amount": "tỷ lệ/số tiền nếu không phải bảng",
      "payment_timing": "trả khi nào, trả chậm/giữ lại bao nhiêu, điều kiện nhận phần giữ lại",
      "clawback_or_forfeit": "thu hồi/mất quyền nhận (nếu có)",
      "page": "số trang (hoặc 3-4)",
      "quote": "trích nguyên văn ngắn (≤ 40 từ) chứa con số chính",
      "uncertain": false,
      "note": "chỗ mơ hồ, mâu thuẫn trong văn bản, định nghĩa chưa rõ"
    }
  ],
  "definitions": [{"term": "K2 / FYC / tỷ lệ duy trì…", "definition_verbatim": "...", "page": 0}],
  "internal_inconsistencies": ["chỗ văn bản tự mâu thuẫn, kèm trang"],
  "pages_read": [1, 2, 3]
}
```

## Luật
1. Không suy đoán, không làm tròn, không tính toán thay văn bản. Văn bản không nói thì ghi `"note": "văn bản không nêu"`.
2. Giữ nguyên đơn vị (triệu đồng, %, số hợp đồng, tháng) và kiểu ngưỡng (từ…đến…, trên, tối thiểu).
3. Mỗi bậc thang lấy đủ mọi hàng; ghi rõ ngưỡng có bao gồm biên hay không như văn bản viết.
4. Ví dụ minh họa trong văn bản: không chép thành quy tắc, nhưng ghi số trang vào `note` nếu ví dụ cho thấy cách tính.
5. `pages_read` phải gồm MỌI trang của văn bản — đọc hết, kể cả phụ lục và chú thích chân trang.
6. Cuối cùng, tự rà lại mọi con số trong `rules` với ảnh trang một lần nữa trước khi ghi file.
