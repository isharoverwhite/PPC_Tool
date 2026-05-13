# 💬 User Story — Tại sao công cụ này ra đời?

---

## Bối cảnh

Tôi là một **thực tập sinh vận hành sàn thương mại điện tử Amazon**. Công việc hàng ngày của tôi xoay quanh việc quản lý gian hàng, theo dõi đơn hàng, tạo báo cáo bằng AMC, và đặc biệt là **chạy quảng cáo PPC** cho các sản phẩm của công ty trong lĩnh vực làm đẹp.

Là một thực tập sinh, tôi được giao những công việc nền tảng nhất — trong đó có việc chuẩn bị bộ từ khóa cho mỗi chiến dịch quảng cáo mới. Mỗi tuần tôi phải chạy từ **2 đến 3 chiến dịch PPC**, mỗi chiến dịch cần một bộ từ khóa riêng được lọc từ dữ liệu xuất ra từ **Helium 10 Cerebro**.

Nghe thì đơn giản. Nhưng thực tế thì không.

---

## Vấn đề — Khó khăn của một thực tập sinh

Là người mới, tôi không có nhiều kinh nghiệm. Tôi không biết đâu là từ khóa tốt, đâu là từ khóa nên tránh. Mọi thứ đều phải mò mẫm. Và quy trình lọc từ khóa thủ công là một cơn ác mộng thực sự:

1. **Tải file xuất từ Helium 10 Cerebro** — một file Excel hơn 1.000 dòng, hàng chục cột dữ liệu. Mới mở lên đã thấy choáng.
2. **Ngồi lọc thủ công từng từ** — mở filter trong Excel, gõ từng từ khóa một, xem cái nào liên quan đến sản phẩm. Có những từ na ná nhau, không biết nên giữ hay bỏ.
3. **Thử-sai không hồi kết** — lọc ra 100 từ thì sợ quá rộng, lọc ra 5 từ thì sợ quá hẹp. Không có tiêu chí nào rõ ràng, hoàn toàn dựa vào cảm tính.
4. **Copy/paste trong lo sợ** — paste từ khóa vào template 25 cột với đủ loại công thức Excel liên kết. Chỉ cần lệch một ô là toàn bộ bảng tính sai hết.
5. **Kiểm tra đi kiểm tra lại** — vì sợ sai, tôi phải dò từng dòng, từng cột. Mỗi lần dò xong là mắt mờ, đầu óc quay cuồng.

> **Mỗi chiến dịch ngốn của tôi 20–30 phút. Có hôm deadline gấp, tôi ngồi đến tận khuya chỉ để... lọc từ khóa.**

Cảm giác lúc đó thật sự rất tệ. Tôi là thực tập sinh — đáng lẽ phải đang học hỏi những thứ lớn hơn, như phân tích thị trường, tối ưu chiến lược quảng cáo. Vậy mà phần lớn thời gian của tôi lại tiêu tốn vào một công việc **cơ học, lặp đi lặp lại, không hề tạo ra giá trị gì cho sự phát triển của bản thân**.

Tệ hơn, tôi bắt đầu nghi ngờ chính mình: *"Có phải mình làm chậm quá không? Có phải mình không đủ năng lực?"*

Nhưng rồi tôi nhận ra: **vấn đề không nằm ở tôi. Vấn đề nằm ở cái quy trình.**

---

## Khoảnh khắc quyết định

Một buổi tối nọ, sau khi ngồi gần **30 phút chỉ để lọc ra được 46 từ khóa** cho một sản phẩm mới, tôi bần thần nhìn vào màn hình Excel đầy những dòng filter thủ công và tự hỏi:

> *"Tại sao mình lại ngồi đây làm việc này bằng tay? Đây đâu phải là việc cần tư duy sáng tạo — nó chỉ là lọc và copy/paste. Một đoạn script nhỏ cũng có thể làm việc này trong vài giây."*

Ngay lúc đó, tôi quyết định: **tự động hóa nó.**

Tôi không phải là lập trình viên. Tôi chỉ là một thực tập sinh vận hành, biết chút ít về Python. Nhưng tôi nghĩ: *"Thà bỏ ra vài buổi tối để viết một công cụ, còn hơn là tiêu tốn hàng trăm giờ trong tương lai cho cùng một việc vô nghĩa này."*

---

## Giải pháp

Tôi bắt tay vào viết. Ban đầu chỉ là một script Python chạy trên terminal, thô sơ nhưng chạy được. Dần dần, qua mỗi lần sử dụng, tôi cải tiến thêm:

| Phiên bản | Mô tả |
|-----------|-------|
| **V1** | Script CLI đơn giản: nhập từ khóa → lọc → xuất 6 cột |
| **V2** | Thêm gợi ý filter thông minh từ tên sản phẩm, từ điển đồng nghĩa, đánh giá chất lượng filter |
| **V3** | GUI desktop hoàn chỉnh cho macOS, 20 cột + công thức Excel, negative keywords CRUD, tự động loại bỏ từ khóa đối thủ |

Công cụ giờ đây không chỉ giúp tôi, mà hoàn toàn có thể giúp bất kỳ ai làm vận hành Amazon PPC — từ thực tập sinh đến chuyên viên dày dạn kinh nghiệm.

---

## Kết quả

| | Trước đây | Sau khi có công cụ |
|--|-----------|-------------------|
| ⏱️ Thời gian / chiến dịch | 20–30 phút | **< 1 phút** |
| 🔢 Số thao tác | Hàng chục bước thủ công | **3 bước: chọn file → chọn filter → xuất** |
| ❌ Tỉ lệ sai sót | Cao (lệch công thức, paste nhầm) | **Gần như bằng 0** |
| 🧠 Căng thẳng tinh thần | Mệt mỏi, nghi ngờ bản thân | **Tự tin, tập trung vào chiến lược** |
| 📈 Thời gian rảnh có được | 0 | **Thêm hàng giờ mỗi tuần để học những thứ mới** |

---

## Bài học

Là một thực tập sinh, điều quý giá nhất tôi học được không phải là cách chạy quảng cáo — mà là **cách tư duy để giải quyết vấn đề.**

> *Khó khăn trong công việc không phải là dấu hiệu của sự yếu kém. Đó là tín hiệu cho thấy có thứ gì đó đang sai ở quy trình — và bạn có cơ hội để sửa nó.*

Thay vì cắm đầu làm việc chăm chỉ một cách mù quáng, hãy thỉnh thoảng ngẩng lên và tự hỏi: *"Có cách nào làm việc này nhanh hơn không? Có cách nào để tự động hóa nó không?"*

Đây không chỉ là câu chuyện về một công cụ lọc từ khóa. Đây là câu chuyện về việc **một thực tập sinh dám nghĩ, dám làm, và biến khó khăn thành động lực để tạo ra giải pháp.**

Kết quả? Tôi không chỉ tiết kiệm được thời gian — tôi còn chứng minh được với chính mình và với công ty rằng: **giá trị của một con người không nằm ở việc họ làm bao nhiêu giờ, mà nằm ở cách họ giải quyết vấn đề.**

---

<p align="center">
  <em>🛠️ Tự động hóa không phải là lười biếng — đó là làm việc thông minh.</em>
</p>
