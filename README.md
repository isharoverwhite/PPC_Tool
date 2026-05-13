<p align="center">
  <img src="https://img.shields.io/badge/version-3.0-1F4E79?style=for-the-badge" alt="Version 3.0">
  <img src="https://img.shields.io/badge/platform-macOS-000000?style=for-the-badge&logo=apple" alt="macOS">
  <img src="https://img.shields.io/badge/python-3.14-3776AB?style=for-the-badge&logo=python" alt="Python 3.14">
  <img src="https://img.shields.io/badge/build-py2app-orange?style=for-the-badge" alt="py2app">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License MIT">
</p>

<h1 align="center">🔍 PPC Keyword Filter</h1>
<h3 align="center">Amazon PPC Advertising Automation — Powered by Helium 10 Cerebro</h3>

<p align="center">
  <strong>Tự động lọc từ khóa · Gợi ý filter thông minh · Xuất Excel 20 cột chuẩn PPC — trong < 1 phút</strong>
</p>

<br>

---

## 📖 Giới thiệu sản phẩm

**PPC Keyword Filter** là ứng dụng desktop native cho macOS, được thiết kế dành riêng cho người bán hàng Amazon chạy quảng cáo PPC. Ứng dụng xử lý file xuất từ **Helium 10 Cerebro**, tự động phân tích và gợi ý bộ lọc từ khóa tối ưu, sau đó xuất ra file Excel chuẩn template quảng cáo với công thức tính toán lợi nhuận tích hợp sẵn.

> 💡 **Từ 20 phút thủ công → dưới 1 phút** cho mỗi chiến dịch PPC.

<br>

---

## 💬 User Story — Tại sao công cụ này ra đời?

> *"Mỗi tuần tôi phải chạy 2–3 chiến dịch quảng cáo PPC mới trên Amazon. Mỗi lần như vậy, tôi lại phải ngồi hàng giờ trước màn hình: mở file Excel 1.000+ dòng từ khóa xuất từ Helium 10 Cerebro, loay hoay filter thử từng từ một, rồi copy/paste thủ công vào template quảng cáo. Việc này lặp đi lặp lại, tốn rất nhiều thời gian và dễ gây sai sót — nhất là khi có quá nhiều cột và công thức Excel liên kết với nhau."*
>
> *"Một lần, sau khi mất gần 30 phút chỉ để lọc được 46 từ khóa cho một sản phẩm, tôi tự hỏi: tại sao mình không tự động hóa việc này? Đây không phải là công việc đòi hỏi sự sáng tạo — nó đơn thuần là thao tác lặp lại mà máy tính có thể làm nhanh gấp 20 lần con người."*
>
> *"Tôi bắt tay vào viết công cụ này. Ban đầu chỉ là một script Python nhỏ chạy trên terminal, dần dần phát triển thành một ứng dụng desktop hoàn chỉnh với giao diện trực quan, có thể phân tích tên sản phẩm, tự động gợi ý bộ lọc tối ưu, và xuất ra file Excel chuẩn template chỉ trong một nốt nhạc."*

**Bài học rút ra:** Trong công việc, sự nhanh nhạy không chỉ nằm ở việc làm nhanh hơn — mà là nhận ra đâu là thứ nên được tự động hóa. Thay vì dành 30 phút mỗi lần cho một tác vụ lặp lại, dành vài giờ để xây dựng công cụ giúp tiết kiệm hàng trăm giờ về sau. Đó là sự đầu tư thông minh.

<br>

## 🎯 Vấn đề & Giải pháp

<table>
<tr>
  <td width="50%">

### ❌ Trước khi có công cụ
- Mở Excel, filter thủ công 1,000+ từ khóa
- Thử-sai nhiều lần để tìm filter phù hợp
- Copy/paste từng phần vào template 25 cột
- Dễ gây lỗi công thức Excel
- Khó phát hiện brand đối thủ
- **~20 phút / chiến dịch**

  </td>
  <td width="50%">

### ✅ Sau khi có công cụ
- Kéo thả file Cerebro → nhập tên SP
- Tool tự gợi ý filter kèm đánh giá chất lượng
- Một click xuất file 20 cột đầy đủ công thức
- Tự động highlight brand đối thủ (nền vàng)
- Tự động loại bỏ negative keywords
- **< 1 phút / chiến dịch**

  </td>
</tr>
</table>

<br>

## ✨ Tính năng chính

<table>
<tr>
  <td width="50%">

### 🔍 Bước 1 — Phân tích & Gợi ý Filter
- Nhập tên sản phẩm → tự động trích xuất từ khóa có nghĩa
- Từ điển đồng nghĩa / biến thể Amazon (SYNONYMS)
- Sinh danh sách gợi ý filter (đơn + kết hợp OR)
- Đánh giá chất lượng filter:
  - ✅ **Lý tưởng** (20–60 kết quả)
  - 🟡 **Hơi ít / Hơi nhiều**
  - 🔴 **Quá rộng** / ⚪ **Quá ít**
- Kết hợp nhiều filter (VD: `1+3` → OR)
- Lịch sử filter tự động lưu
- Tự nhập filter tùy chỉnh (regex)

  </td>
  <td width="50%">

### 📊 Bước 2 — Lọc Dữ liệu & Xuất File
- Preview 20 cột realtime trên UI
- Cột tự động tính toán:
  - Clicks, Spend, Ads Orders, Ads Revenue
  - ACOS, Total Orders, Total Revenue
  - Product Fee, Total Fee, **Profit**
- **Negative Keywords** — thêm/sửa/xóa, tự động lọc
- **Rival Companies** — tự động loại bỏ từ khóa đối thủ
- Fill Bid thiếu bằng trung bình
- Highlight brand đối thủ (vàng `#FFF2CC`)
- Xuất Excel 20 cột chuẩn template PPC
- Công thức Excel liên kết — chỉ cần điền Price & Fees

  </td>
</tr>
</table>

<br>

## 🖥️ Giao diện

<p align="center">
  <em>(Screenshot ứng dụng)</em>
</p>

```
╔══════════════════════════════════════════════════════════════════╗
║  🔍 Auto PCC Keywords — made by Experience                      ║
╠══════════════════════════════════════════════════════════════════╣
║  BƯỚC 1: LỌC TỪ KHÓA — Phân tích & Gợi ý Filter                ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ 📂 File Cerebro: [___________] [Browse]                    │ ║
║  │ 🏷️ Tên SP:      [___________] [🔍 Phân tích & Gợi ý]     │ ║
║  │ ───────────────────────────────────────────────────────── │ ║
║  │ #  │ Filter Pattern          │ Kết quả    │ Đánh giá      │ ║
║  │ 1  │ premade fans|curl lash   │ 46 (4.2%)  │ ✅ Lý tưởng   │ ║
║  │ 2  │ premade|fans            │ 44 (4.0%)  │ ✅ Lý tưởng   │ ║
║  │ 3  │ narrow|premade fans     │ 38 (3.4%)  │ ✅ Lý tưởng   │ ║
║  │ ───────────────────────────────────────────────────────── │ ║
║  │ 📜 Lịch sử: [___________]  Filter: [___________]          │ ║
║  │ Kết hợp: [___] [+]  Tự nhập: [___________]  [✅ Áp dụng] │ ║
║  └────────────────────────────────────────────────────────────┘ ║
║                                                                  ║
║  BƯỚC 2: LỌC DỮ LIỆU & XUẤT FILE                                ║
║  ┌────────────────────────────────────────────────────────────┐ ║
║  │ 📊 Kết quả lọc: 46 từ khóa / 1,104 tổng (4.2%)            │ ║
║  │ 💰 Price ($): [___]  📦 Amazon Fee ($): [___]              │ ║
║  │ ───────────────────────────────────────────────────────── │ ║
║  │ Keyword Phrase      │ SV   │ Bid   │ ... │ Profit         │ ║
║  │ super narrow premade│ 8,500│ $0.45 │ ... │ $124.50        │ ║
║  │ 5d premade fans     │ 5,200│ $0.38 │ ... │ $89.20         │ ║
║  │ ───────────────────────────────────────────────────────── │ ║
║  │ ⚠️ Negative Keywords: [___________] [Thêm] [✏️ Sửa] [✕ Xóa]│ ║
║  │ [💰 Fill Bid thiếu]                    [📤 Xuất file Excel]│ ║
║  └────────────────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════╝
```

<br>

## 📦 Cài đặt

### Cách 1: Tải .app (khuyên dùng cho người dùng cuối)

<p>
  <a href="#">
    <img src="https://img.shields.io/badge/Download-.app-1F4E79?style=for-the-badge&logo=apple" alt="Download .app">
  </a>
</p>

1. Tải file `PPC Keyword Filter.app.zip` từ [Releases](https://github.com/isharoverwhite/PPC_Tool/releases)
2. Giải nén → kéo `PPC Keyword Filter.app` vào thư mục **Applications**
3. Double-click để mở
4. *(Lần đầu: vào System Settings → Privacy & Security → Open Anyway)*

### Cách 2: Chạy từ source (cho developer)

```bash
# 1. Clone repo
git clone https://github.com/isharoverwhite/PPC_Tool.git
cd PPC_Tool

# 2. Cài dependencies
pip install pandas openpyxl

# 3. Chạy
python3 main.py
```

### Cách 3: Tự build .app

```bash
pip install py2app
python3 setup.py py2app
# Output: dist/PPC\ Keyword\ Filter.app
```

<br>

## 🗂️ Cấu trúc project

```
PPC_Tool/
├── main.py                  ← Entry point: python3 main.py
├── setup.py                 ← py2app build script
├── app/
│   ├── ui.py                ← Giao diện tkinter (1,100+ dòng)
│   ├── engine.py            ← FilterEngine: load, filter, negative keywords
│   ├── synonym_engine.py    ← SynonymEngine: phân tích tên SP → gợi ý filter
│   ├── excel_writer.py      ← Xuất Excel 20 cột có style + công thức
│   └── constants.py         ← Cấu hình: màu sắc, cột, thresholds
├── input/
│   ├── SYNONYMS.txt         ← Từ điển đồng nghĩa
│   ├── STOP_WORDS.txt       ← Từ dừng (stop words)
│   ├── brands.txt           ← Danh sách brand đối thủ
│   ├── keywords.txt         ← Negative keywords (tự động lọc)
│   ├── filters.txt          ← Lịch sử filter (tự động lưu)
│   ├── rival_company.txt    ← Công ty đối thủ cần loại bỏ
│   └── product_name.txt     ← Lịch sử tên sản phẩm
├── output/                  ← File Excel xuất ra
├── PLAN.md                  ← Kế hoạch phát triển
├── PRD.md                   ← Product Requirements Document
└── README.md                ← File này
```

<br>

## 📊 File Output

### 20 cột chuẩn template PPC Keyword Research:

<table>
<tr>
  <th>#</th><th>Cột</th><th>Nguồn</th><th>Mô tả</th>
</tr>
<tr><td align="center">A</td><td><strong>Keyword Phrase</strong></td><td>Cerebro</td><td>Từ khóa</td></tr>
<tr><td align="center">B</td><td><strong>Search Volume</strong></td><td>Cerebro</td><td>Lượng tìm kiếm/tháng</td></tr>
<tr><td align="center">C</td><td><strong>Sponsored ASINs</strong></td><td>Cerebro</td><td>Số ASIN đang chạy ads</td></tr>
<tr><td align="center">D</td><td><strong>Competing Products</strong></td><td>Cerebro</td><td>Số sản phẩm cạnh tranh</td></tr>
<tr><td align="center">E</td><td><strong>CPR</strong></td><td>Cerebro</td><td>Số review cần để rank</td></tr>
<tr><td align="center">F</td><td><strong>Bid</strong></td><td>Cerebro</td><td>Giá thầu PPC gợi ý</td></tr>
<tr><td align="center">G</td><td><strong>CTR</strong></td><td>Mặc định 1%</td><td>Click-through rate</td></tr>
<tr><td align="center">H</td><td><strong>Clicks</strong></td><td>=G×B</td><td>Số clicks dự kiến</td></tr>
<tr><td align="center">I</td><td><strong>Spend</strong></td><td>=F×H</td><td>Chi phí ads dự kiến</td></tr>
<tr><td align="center">J</td><td><strong>CVR</strong></td><td>Mặc định 5%</td><td>Conversion rate</td></tr>
<tr><td align="center">K</td><td><strong>Ads Orders</strong></td><td>=H×J</td><td>Đơn hàng từ ads</td></tr>
<tr><td align="center">L</td><td><strong>Price</strong></td><td>Người dùng</td><td>Giá bán 1 sản phẩm</td></tr>
<tr><td align="center">M</td><td><strong>Ads Revenue</strong></td><td>=K×L</td><td>Doanh thu từ ads</td></tr>
<tr><td align="center">N</td><td><strong>ACOS</strong></td><td>=I÷M</td><td>Tỉ lệ chi phí / doanh thu</td></tr>
<tr><td align="center">O</td><td><strong>Total Orders</strong></td><td>=K+K/4</td><td>Tổng đơn (ads + organic)</td></tr>
<tr><td align="center">P</td><td><strong>Total Revenue</strong></td><td>=L×O</td><td>Tổng doanh thu</td></tr>
<tr><td align="center">Q</td><td><strong>Product Fee</strong></td><td>=L÷3</td><td>COGS ước tính</td></tr>
<tr><td align="center">R</td><td><strong>Amazon Fee</strong></td><td>Người dùng</td><td>FBA + Referral Fee</td></tr>
<tr><td align="center">S</td><td><strong>Total Fee</strong></td><td>=(R+Q)×O+I</td><td>Tổng chi phí</td></tr>
<tr><td align="center">T</td><td><strong>Profit</strong></td><td>=P−S</td><td>🟢 Lợi nhuận ròng</td></tr>
</table>

> 💡 File output có sẵn **dòng Total** (SUM/AVERAGE) + **dòng Campaign sections** + **Total thêm 50-100%** (×160%) — paste vào template là chạy ngay.

<br>

## 🎨 Màu sắc & Định dạng

<table>
<tr>
  <td width="25px" bgcolor="#E69138"></td>
  <td><code>#E69138</code></td>
  <td>Header row — nền cam (theo format file mẫu)</td>
</tr>
<tr>
  <td width="25px" bgcolor="#FFF2CC"></td>
  <td><code>#FFF2CC</code></td>
  <td>⚠️ Brand đối thủ — nền vàng (cân nhắc không dùng Exact Match)</td>
</tr>
<tr>
  <td width="25px" bgcolor="#FFE599"></td>
  <td><code>#FFE599</code></td>
  <td>Total row — nền vàng nhạt</td>
</tr>
<tr>
  <td width="25px" bgcolor="#FF0000"></td>
  <td><code>#FF0000</code></td>
  <td>CTR & CVR — chữ đỏ (assumption values)</td>
</tr>
</table>

<br>

## 🔧 Công nghệ

<table>
<tr>
  <td><strong>Ngôn ngữ</strong></td>
  <td>Python 3.14</td>
</tr>
<tr>
  <td><strong>GUI</strong></td>
  <td><code>tkinter</code> (Python standard library)</td>
</tr>
<tr>
  <td><strong>Xử lý dữ liệu</strong></td>
  <td><code>pandas</code> — đọc/xử lý file Excel</td>
</tr>
<tr>
  <td><strong>Xuất Excel</strong></td>
  <td><code>openpyxl</code> — file .xlsx có style, công thức, highlight</td>
</tr>
<tr>
  <td><strong>Đóng gói</strong></td>
  <td><code>py2app</code> — build .app bundle cho macOS</td>
</tr>
<tr>
  <td><strong>Regex Engine</strong></td>
  <td>Hỗ trợ <code>|</code> (OR), <code>.</code> (wildcard), <code>.*</code> (any string), case-insensitive</td>
</tr>
</table>

<br>

## 🚀 Quy trình sử dụng

```
┌─────────────────────────────────────────────────────────────┐
│  ① Tải file Cerebro từ Helium 10                             │
│     Products → Cerebro → Export Data → .xlsx                │
│                                                              │
│  ② Mở PPC Keyword Filter.app                                 │
│     → 📂 Browse → chọn file .xlsx vừa tải                   │
│                                                              │
│  ③ Nhập tên sản phẩm → 🔍 Phân tích & Gợi ý                 │
│     → Chọn filter từ danh sách gợi ý (✅ Lý tưởng)          │
│     → ✅ Áp dụng filter                                      │
│                                                              │
│  ④ Nhập Price ($) và Amazon Fee ($) (tuỳ chọn)              │
│     → Xem preview 20 cột trên UI                             │
│     → Thêm negative keywords nếu cần                         │
│     → Xoá dòng thủ công nếu muốn (Delete / Undo ⌘Z)        │
│                                                              │
│  ⑤ 📤 Xuất file Excel → Chọn nơi lưu                        │
│     → 20 cột + công thức + Total + Campaign sections        │
│     → Paste vào template quảng cáo PPC                      │
│                                                              │
│  ⑥ Điền số liệu thực tế từ Seller Central                   │
│     → Template tự tính Profit / ACOS                        │
└─────────────────────────────────────────────────────────────┘
```

<br>

## ⌨️ Phím tắt

| Phím | Chức năng |
|------|-----------|
| `↑` `↓` | Chọn dòng trong preview |
| `Delete` / `Backspace` | Xóa dòng đã chọn |
| `⌘Z` / `Ctrl+Z` | Undo xóa dòng |
| `⌘C` / `Ctrl+C` | Copy ô đang chọn |
| `Enter` (ở ô filter) | Áp dụng filter |
| `Enter` (ở ô negative) | Thêm negative keyword |
| `Double-click` (negative list) | Sửa negative keyword |
| `Chuột phải` | Menu copy/xóa |

<br>

## 📋 File cấu hình (input/)

Tất cả file config đều là **plain text**, có thể chỉnh sửa bằng bất kỳ text editor nào.

| File | Định dạng | Mục đích |
|------|-----------|----------|
| `SYNONYMS.txt` | `từ_gốc = biến_thể_1, biến_thể_2, ...` | Từ điển đồng nghĩa Amazon |
| `STOP_WORDS.txt` | Mỗi dòng 1 từ | Từ dừng, loại bỏ khi phân tích SP |
| `brands.txt` | Mỗi dòng 1 brand | Highlight vàng nếu từ khóa chứa brand |
| `keywords.txt` | Mỗi dòng 1 từ | Negative keywords — tự động loại bỏ |
| `filters.txt` | Mỗi dòng 1 pattern | Lịch sử filter (tự động lưu) |
| `rival_company.txt` | Mỗi dòng 1 tên | Công ty đối thủ — tự động loại khỏi kết quả |
| `product_name.txt` | Mỗi dòng 1 tên | Lịch sử tên SP (tự động lưu) |

<br>

## 🗺️ Roadmap

- [x] **V3.0** — GUI tkinter, 20 cột + công thức Excel, Negative Keywords CRUD, Rival auto-remove, Bid fill
- [x] **V3.0** — Đóng gói .app native cho macOS
- [ ] **V3.1** — Dark mode
- [ ] **V3.1** — Import/Export config profiles (cho nhiều dòng sản phẩm khác nhau)
- [ ] **V3.2** — Hỗ trợ multi-language Cerebro export
- [ ] **V4.0** — Tích hợp Helium 10 API (nếu có)

<br>

## 👤 Người dùng

> Trình độ kỹ thuật: Cơ bản · Tần suất: 2–3 lần/tuần

<br>

---

<p align="center">
  <sub>🛠️ Made with ❤️ by Experience | © 2026</sub>
</p>
