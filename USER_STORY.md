# 💬 User Story — Tại sao công cụ này ra đời?

---

## Bối cảnh

Tôi là người bán hàng trên Amazon, chuyên kinh doanh trong lĩnh vực làm đẹp. Mỗi tuần tôi chạy từ **2 đến 3 chiến dịch quảng cáo PPC mới**, mỗi chiến dịch cần một bộ từ khóa riêng được lọc từ dữ liệu xuất ra từ **Helium 10 Cerebro**.

## Vấn đề

Cứ mỗi lần chuẩn bị cho một chiến dịch mới, tôi lại phải trải qua một quy trình thủ công lặp đi lặp lại:

1. **Tải file xuất từ Helium 10 Cerebro** — một file Excel chứa hơn 1.000 dòng từ khóa thô với hàng chục cột dữ liệu.
2. **Mở Excel lên và bắt đầu lọc** — thử từng từ khóa một, xem từ nào liên quan đến sản phẩm, từ nào là của đối thủ, từ nào quá chung chung.
3. **Thử-sai liên tục** — không biết nên dùng từ nào để lọc thì mới ra được lượng kết quả vừa đủ (không quá ít, không quá nhiều).
4. **Copy/paste thủ công** — sau khi lọc xong, copy từng nhóm từ khóa và paste vào template quảng cáo PPC có sẵn 25 cột với công thức Excel liên kết.
5. **Kiểm tra lại** — vì paste tay nên rất dễ sai lệch công thức, mất thêm thời gian dò lại.

> **Tổng thời gian: 15–30 phút cho mỗi chiến dịch.**

Nhân lên 2–3 lần mỗi tuần, đó là hàng giờ đồng hồ mỗi tháng chỉ dành cho một công việc **hoàn toàn không tạo ra giá trị sáng tạo** — nó đơn thuần là thao tác cơ học mà máy tính có thể làm tốt hơn con người.

---

## Khoảnh khắc quyết định

Một lần, sau khi ngồi gần **30 phút chỉ để lọc ra 46 từ khóa** cho một sản phẩm mới, tôi tự hỏi:

> *"Tại sao mình lại ngồi đây làm việc này bằng tay? Đây đâu phải là việc cần tư duy — nó chỉ là lọc và copy/paste. Máy tính làm việc này trong vài giây là xong."*

Ngay lúc đó, tôi quyết định: **tự động hóa nó.**

---

## Giải pháp

Tôi bắt tay vào viết một công cụ Python để giải quyết triệt để vấn đề này. Trải qua nhiều phiên bản, công cụ đã phát triển từ một script CLI đơn giản thành một **ứng dụng desktop hoàn chỉnh cho macOS** với giao diện trực quan, tích hợp đầy đủ các tính năng:

| Phiên bản | Mô tả |
|-----------|-------|
| **V1** | Script CLI đơn giản: nhập từ khóa → lọc → xuất 6 cột |
| **V2** | Thêm gợi ý filter thông minh từ tên sản phẩm, từ điển đồng nghĩa |
| **V3** | GUI desktop hoàn chỉnh, 20 cột + công thức Excel, negative keywords, tự động loại bỏ đối thủ |

---

## Kết quả

| | Trước đây | Sau khi có công cụ |
|--|-----------|-------------------|
| ⏱️ Thời gian / chiến dịch | 15–30 phút | **< 1 phút** |
| 🔢 Số thao tác thủ công | Hàng chục bước | **3 bước: chọn file → chọn filter → xuất** |
| ❌ Tỉ lệ sai sót | Cao (paste tay, lệch công thức) | **0% (xuất tự động)** |
| 🧠 Tư duy cần thiết | Tập trung cao độ, dễ mệt mỏi | **Thảnh thơi, tập trung vào chiến lược** |

---

## Bài học

Trong công việc, **sự nhanh nhạy không chỉ nằm ở việc làm nhanh hơn** — mà là nhận ra đâu là thứ không nên làm bằng tay.

> *Thay vì dành 30 phút mỗi lần cho một tác vụ lặp lại, hãy dành vài giờ để xây dựng công cụ giúp tiết kiệm hàng trăm giờ về sau.*

Đây không chỉ là một công cụ — đây là **sự thể hiện của tư duy làm việc thông minh**: nhận diện vấn đề, tìm giải pháp, và tự động hóa nó.

Kết quả? Tôi có thêm thời gian để tập trung vào những thứ thực sự quan trọng: **phân tích dữ liệu, tối ưu chiến dịch, và phát triển kinh doanh.**

---

<p align="center">
  <em>🛠️ Tự động hóa không phải là lười biếng — đó là làm việc thông minh.</em>
</p>
