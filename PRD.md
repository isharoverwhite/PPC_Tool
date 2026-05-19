# 📋 PRD — PPC Keyword Filter Tools

> **Product Requirements Document**  
> **Version:** 1.0 | **Date:** 2026-05-12  
> **Product Owner:** SAIGON LASH Store (MariaMCP)  
> **Domain:** Amazon PPC Advertising Automation

---

## 1. Tổng quan sản phẩm (Executive Summary)

Bộ công cụ CLI bằng Python giúp tự động hóa quy trình lọc từ khóa từ file Helium 10 Cerebro export, xuất ra file Excel sạch để paste trực tiếp vào template quảng cáo PPC trên Amazon. Mục tiêu: **giảm thời gian thủ công từ 15–30 phút xuống dưới 1 phút** cho mỗi chiến dịch PPC.

### Vấn đề hiện tại (Pain Points)

| Vấn đề | Mô tả |
|--------|-------|
| Dữ liệu thô phức tạp | File Helium 10 Cerebro export chứa 1,000+ từ khóa với nhiều cột không cần thiết |
| Lọc thủ công tốn thời gian | Phải mở Excel, filter thủ công, copy/paste từng phần |
| Khó chọn filter tối ưu | Không biết nên dùng từ khóa nào để lọc, thử-sai nhiều lần |
| Template phức tạp | Template PPC có 25 cột với công thức Excel liên kết, dễ gây lỗi khi paste thủ công |
| Brand name đối thủ | Khó phát hiện từ khóa chứa tên thương hiệu đối thủ để loại bỏ |

---

## 2. Mục tiêu sản phẩm (Product Goals)

| ID | Mục tiêu | Đo lường |
|----|----------|----------|
| G1 | Giảm thời gian xử lý từ khóa | < 1 phút / chiến dịch (hiện tại: ~20 phút) |
| G2 | Gợi ý filter thông minh | ≥ 80% trường hợp có filter lý tưởng (20–60 kết quả) |
| G3 | Cảnh báo brand đối thủ | Tự động highlight 100% từ khóa chứa brand name |
| G4 | Xuất file chuẩn template | 100% file output paste được ngay vào template không cần chỉnh sửa |

---

## 3. Người dùng (User Personas)

### Primary Persona: Chủ store Amazon (MariaMCP / SAIGON LASH)
- Vai trò: Quản lý toàn bộ hoạt động quảng cáo PPC
- Trình độ kỹ thuật: Cơ bản (chạy được lệnh terminal đơn giản)
- Nhu cầu chính: Lọc từ khóa nhanh, paste vào template có sẵn công thức, theo dõi lợi nhuận
- Tần suất sử dụng: 2–3 lần/tuần (mỗi lần chạy chiến dịch mới hoặc tối ưu)

---

## 4. Tính năng (Features)

### 4.1 Tool 1: `keyword_filter_tool.py` — Gợi ý filter thông minh

| ID | Tính năng | Mức độ ưu tiên | Trạng thái |
|----|-----------|---------------|------------|
| F1.1 | Nhập tên sản phẩm → phân tích từ khóa có nghĩa | P0 | ✅ Done |
| F1.2 | Tự động mở rộng từ đồng nghĩa / biến thể Amazon (SYNONYMS dict) | P0 | ✅ Done |
| F1.3 | Sinh danh sách gợi ý filter (đơn + kết hợp OR 2 terms) | P0 | ✅ Done |
| F1.4 | Đánh giá chất lượng filter (✅ Lý tưởng / 🟡 Hơi ít-nhiều / 🔴 Quá rộng / ⚪ Quá ít) | P0 | ✅ Done |
| F1.5 | Kết hợp nhiều filter (VD: `1+3` → OR) | P1 | ✅ Done |
| F1.6 | Tự nhập filter tùy chỉnh (`custom`) | P1 | ✅ Done |
| F1.7 | Xuất file 6 cột chuẩn, xen kẽ màu, highlight brand vàng | P0 | ✅ Done |

### 4.2 Tool 2: `cerebro_extract.py` — Lọc nhanh

| ID | Tính năng | Mức độ ưu tiên | Trạng thái |
|----|-----------|---------------|------------|
| F2.1 | Nhận filter trực tiếp từ CLI argument | P0 | ✅ Done |
| F2.2 | Xuất file 6 cột chuẩn | P0 | ✅ Done |
| F2.3 | Cảnh báo nếu không có kết quả + gợi ý dùng Tool 1 | P1 | ✅ Done |

### 4.3 Tool 3: `cerebro_to_ppc_tracker.py` — PPC Profit Tracker

| ID | Tính năng | Mức độ ưu tiên | Trạng thái |
|----|-----------|---------------|------------|
| F3.1 | Sheet ⚙️ Settings: Giá bán, COGS, Referral Fee, FBA Fee, CTR, CVR | P0 | ✅ Done |
| F3.2 | Sheet 📊 PPC Keywords: 25 cột với công thức Excel liên kết Settings | P0 | ✅ Done |
| F3.3 | 5 nhóm cột: Cerebro → Assumptions → Projected → Actual → Profit | P0 | ✅ Done |
| F3.4 | Conditional formatting: ACOS (đỏ/vàng/xanh), Profit (đỏ/xanh) | P1 | ✅ Done |
| F3.5 | Sheet 📖 Hướng dẫn sử dụng (tiếng Việt) | P1 | ✅ Done |
| F3.6 | Tự động detect ASIN từ tên file để đặt tên output | P2 | ✅ Done |

### 4.4 Tính năng chung

| ID | Tính năng | Mức độ ưu tiên | Trạng thái |
|----|-----------|---------------|------------|
| F4.1 | Highlight hàng brand đối thủ (nền vàng `#FFF2CC`) | P0 | ✅ Done |
| F4.2 | Định dạng số: Search Volume/CPR (integer), Bid (currency `$#,##0.00`) | P0 | ✅ Done |
| F4.3 | File output lưu cùng thư mục với file input | P1 | ✅ Done |
| F4.4 | Tên file output tự động gắn ngày `_data_YYYY-MM-DD.xlsx` | P1 | ✅ Done |

---

## 5. Yêu cầu kỹ thuật (Technical Requirements)

| ID | Yêu cầu | Chi tiết |
|----|---------|----------|
| T1 | Ngôn ngữ | Python 3.x |
| T2 | Thư viện | pandas (đọc/xử lý Excel), openpyxl (xuất Excel có style) |
| T3 | Định dạng input | .xlsx (Helium 10 Cerebro export, bắt buộc có cột `H10 PPC Sugg. Bid`) |
| T4 | Định dạng output | .xlsx (6 cột cho Tool 1 & 2; 25 cột + 3 sheets cho Tool 3) |
| T5 | Mã hóa | UTF-8, hỗ trợ tiếng Việt trong console output |
| T6 | Regex filter | Hỗ trợ `\|` (OR), `.` (wildcard), `.*` (any string), case-insensitive |

---

## 6. Quy trình người dùng (User Flows)

### Flow A: Lần đầu / Sản phẩm mới
```
File Cerebro (.xlsx) → keyword_filter_tool.py
  → Nhập tên sản phẩm → Chọn filter từ gợi ý → Xuất file 6 cột
  → Paste vào template PPC → Chạy ads
```

### Flow B: Đã biết filter
```
File Cerebro (.xlsx) → cerebro_extract.py "filter"
  → Xuất file 6 cột → Paste vào template PPC → Chạy ads
```

### Flow C: Full PPC Tracking
```
File Cerebro (.xlsx) → cerebro_to_ppc_tracker.py [filter]
  → File 25 cột + Settings + Formulas
  → Điền Price/COGS/Fees → Điền số liệu thực tế → Đọc Profit
```

---

## 7. Roadmap & Backlog

### V1.1 (Current)
- [x] 3 tool hoạt động ổn định
- [x] Highlight brand keywords
- [x] Xuất file chuẩn template

### V1.2 (Planned)
- [ ] Thêm synonyms mới khi phát hiện biến thể từ khóa mới
- [ ] Hỗ trợ file input có cấu trúc cột khác (multi-language Cerebro export)
- [ ] Thêm option xuất CSV cho tool khác

### V2.0 (Future)
- [ ] GUI đơn giản (tkinter hoặc web) cho người không quen CLI
- [ ] Tự động detect product category từ ASIN
- [ ] Tích hợp trực tiếp API Helium 10 (nếu có)

---

## 8. Từ điển đồng nghĩa (Synonym Dictionary)

```python
SYNONYMS = {
    "premade":   ["premade", "pre made", "pre-made", "promade", "pro made"],
    "fans":      ["fans", "fan lashes", "fan extensions"],
    "lash":      ["lash", "lashes"],
    "extension": ["extension", "extensions"],
    "volume":    ["volume"],
    "wispy":     ["wispy"],
    "curl":      ["curl"],
    "narrow":    ["narrow", "slim", "thin"],
    "cluster":   ["cluster", "clusters"],
    "individual":["individual"],
    "strip":     ["strip"],
    "false":     ["false"],
    "eyelash":   ["eyelash", "eyelashes", "eye lash"],
    "3d":        ["3d"],
    "5d":        ["5d"],
    "7d":        ["7d"],
    "10d":       ["10d"],
    "mixed":     ["mixed"],
    "tray":      ["tray", "trays"],
    "pack":      ["pack", "packs"],
}
```

### Danh sách Brand đối thủ (Competitor Brands)
```
vavalash, veyes, fabu, lilash, novalash, ardell, kiss, nyx, essence, mac
```

---

*Tài liệu dành riêng cho SAIGON LASH Store / MariaMCP — Cập nhật 2026-05-12*
