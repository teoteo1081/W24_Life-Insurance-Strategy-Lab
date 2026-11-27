# Rubric 100 điểm — Kỷ luật nạp dữ liệu & chuẩn hóa chức danh

Áp dụng cho **mọi báo cáo Markdown** xuất ra trong `outputs/` theo `AGENTS.md` (STRICT DATA INGESTION & MAPPING PROTOCOL).
Mỗi báo cáo phải đính kèm bảng tự chấm ở cuối file. **Tổng < 90 điểm = FAIL**, không trình duyệt.

Điểm do script sinh báo cáo **tự tính từ dữ liệu kiểm được** (không tự cho điểm cảm tính). Cách tính từng tiêu chí ở dưới.

| # | Tiêu chí | Điểm tối đa | Cách tính (kiểm được) | Ví dụ mất điểm |
|---|---|---:|---|---|
| 1 | **Độ phủ nguồn 7/7 file** | 25 | 25 × (số file trong `private/sources/` đã mở và khớp SHA-256 registry ÷ 7). File scan phải ghi rõ số trang đã soát bằng mắt / tổng trang; thiếu trang nào thì trừ theo tỷ lệ trang. | Chỉ đọc 6/7 file → 21,4 đ. Bản scan soát 9/15 trang → file đó tính 0,6. |
| 2 | **Cây chức danh gốc & tách tuyến (track)** | 25 | 25 × (số chức danh có tên nguyên văn **khớp text trang được trích** hoặc ghi rõ "đối chiếu bằng mắt" với bản scan ÷ tổng chức danh liệt kê). Mỗi chức danh phải có `track_type`. Mâu thuẫn tên giữa các văn bản phải được nêu (không tự chọn một). | Viết "Trưởng nhóm" thay cho tên nguyên văn → không tính dòng đó. |
| 3 | **Chứng cứ `[FileName : PageNumber]` cho từng con số** | 20 | 20 × (số dòng có ngưỡng / tỷ lệ / số tiền mang trích dẫn `[File : Trang]` ÷ tổng dòng như vậy). FileName = mã duy nhất có trong tên file nguồn (vd `AIAVAD 2601-034`, `CHH0DCEB260008V`). | Bảng có số % nhưng không ghi trang → trừ theo tỷ lệ. |
| 4 | **Negative Proof** | 15 | 15 × (số kết luận "thiếu/không có tài liệu" kèm nhật ký tìm kiếm: danh sách file đã quét + từ khóa + kết quả ÷ tổng kết luận thiếu). Không có kết luận thiếu nào thì 15/15. | Ghi "Manulife thiếu UM" mà không kèm nhật ký → 0 cho kết luận đó. |
| 5 | **Tách Fact vs Assumption** | 15 | 15 × (số dòng số liệu / nhận định có nhãn `VERIFIED FACT` / `ASSUMPTION` / `MODEL_OUTPUT` / `UNKNOWN` / `CONFLICTING EVIDENCE` / `HYPOTHESIS` ÷ tổng). `UNKNOWN` không được thay bằng 0 hay hệ số 1,0. | Trộn số mô phỏng với số trong văn bản mà không gắn nhãn. |

## Quy tắc chấm

- Điểm làm tròn 1 chữ số thập phân; tổng là tổng 5 tiêu chí.
- **FAIL tự động** (dù tổng ≥ 90) nếu: có số `NaN`/`Inf`; có `UNKNOWN` bị chuyển thành 0; có kết luận "thiếu tài liệu" không kèm Negative Proof.
- Điểm tự chấm là `SELF_VERIFIED`; không thay cho kiểm toán độc lập (Codex).
