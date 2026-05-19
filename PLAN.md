# 📋 PLAN — PPC Keyword Filter Tools (Desktop App)

> **Kiến trúc & Kế hoạch triển khai**  
> **Version:** 2.0 | **Date:** 2026-05-12  
> **Domain:** Amazon PPC Advertising — SAIGON LASH Store  
> **Nền tảng:** Python 3.x + tkinter

---

## Mục lục

1. [Cấu trúc thư mục mới](#1----

## ✅ ĐÃ HOÀN THÀNH — PLAN.md (870 dòng)

File **`PLAN.md`** đã được lưu tại `/Users/kiendinhtrung/Desktop/cleanUp_data/PLAN.md`. Dưới đây là tóm tắt nội dung:

---

### 📋 Tổng quan kế hoạch

| Mục | Nội dung chính |
|-----|---------------|
| **1. Cấu trúc thư mục** | `input/` (keywords.txt, brands.txt, filters.txt, .xlsx) + `output/` + `src/` (core/, ui/, utils/) + `tests/` |
| **2. Kiến trúc** | **MVC pattern**: `core/` (business logic độc lập tkinter), `ui/` (3 panel: app, step1, step2), `utils/` (file I/O, validate). Shared state dict kết nối 2 bước |
| **3. Thiết kế UI** | Cửa sổ 900×750px, 2 panel Step1+Step2 xếp dọc, Treeview 4 cột cho suggestions, Step2 tự động khóa đến khi Step1 hoàn thành |
| **4. Data Flow** | Load file → Step1: extract_terms() → build_suggestions() → user chọn filter → auto-fill Step2 → export_filtered_xlsx() |
| **5. Module cần code** | **11 file Python** (~1,305 dòng): config, term_extractor, filter_engine, excel_exporter, file_manager, validators, widgets, step1_panel, step2_panel, app, main |
| **6. Timeline** | **5.5 ngày** (4 giai đoạn): Setup (0.5d) → Core (1.5d) → Utils (0.5d) → UI (2d) → Polish (1d) |
| **7. Rủi ro** | 6 rủi ro kỹ thuật + 14 edge cases đã được phân tích và có mitigation cụ thể |

### 🔑 Điểm quan trọng nhất

- **Giữ nguyên 100% logic nghiệp vụ** từ `keyword_filter_tool.py` và `cerebro_extract.py` — chỉ refactor thành module, không thay đổi thuật toán
- **Tên file output mới**: `{prefix}_{HH-MM-SS}_{DD-MM-YYYY}.xlsx` (VD: `PPC_Keywords_14-30-25_12-05-2026.xlsx`)
- **Brand keywords động**: merge từ `brands.txt` + `DEFAULT_BRAND_KEYWORDS` mặc định
- **Lịch sử filter**: tự động append vào `filters.txt` mỗi lần export

Saving session...completed.
Deleting expired sessions...       4 completed.
.py         #    export_xlsx() — xuất Excel có style
│   │
│   ├── ui/                           #    🖥️ Giao diện tkinter
│   │   ├── __init__.py
│   │   ├── app.py                    #    MainWindow — cửa sổ chính, menu bar, status bar
│   │   ├── step1_panel.py            #    Step1Panel — giao diện Bước 1 (Keyword Filter Tool)
│   │   ├── step2_panel.py            #    Step2Panel — giao diện Bước 2 (Cerebro Extract)
│   │   └── widgets.py                #    UI components tái sử dụng (StyledButton, InfoBox, Tooltip)
│   │
│   └── utils/                        #    🔧 Tiện ích
│       ├── __init__.py
│       ├── file_manager.py           #    File I/O: đọc/ghi input/, output/, naming convention
│       └── validators.py             #    Validate: file tồn tại, định dạng đúng, regex hợp lệ
│
├── tests/                            # 🧪 Unit test
│   ├── __init__.py
│   ├── test_term_extractor.py
│   ├── test_filter_engine.py
│   └── test_excel_exporter.py
│
├── resources/                        # 📦 Tài nguyên tĩnh (nếu cần icon, logo)
│   └── icon.ico
│
├── requirements.txt                  # 📄 Thư viện: pandas, openpyxl
├── PLAN.md                           # 📄 File này
├── PRD.md                            # 📄 Product Requirements Document
└── README.md                         # 📄 Hướng dẫn sử dụng
```

### Giải thích các file input/:

| File | Mục đích | Định dạng | Bắt buộc? |
|------|----------|-----------|-----------|
| `keywords.txt` | Từ khóa xấu cần loại bỏ khỏi kết quả | 1 từ khóa/dòng | Không — nếu thiếu, app vẫn chạy bình thường |
| `brands.txt` | Danh sách brand đối thủ để highlight vàng | 1 brand/dòng | Không — nếu thiếu, dùng BRAND_KEYWORDS mặc định trong config.py |
| `filters.txt` | Lịch sử filter patterns để user xem lại | 1 pattern/dòng | Không — ghi thêm mỗi lần user dùng filter mới |
| `*.xlsx` | Helium 10 Cerebro export (input chính) | Excel có cột "Keyword Phrase" và "H10 PPC Sugg. Bid" | **Có** — app không khởi động nếu thiếu |

---

## 2. Kiến trúc ứng dụng

### 2.1 Sơ đồ module

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           main.py                                       │
│                   (Entry point — khởi tạo App)                          │
└──────────────────┬──────────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         ui/app.py                                       │
│              MainWindow(tk.Tk) — cửa sổ chính                          │
│  ┌──────────────┐  ┌──────────────────────┐  ┌──────────────────────┐  │
│  │  MenuBar     │  │  Step1Panel          │  │  Step2Panel          │  │
│  │  (File,      │  │  (ttk.LabelFrame)    │  │  (ttk.LabelFrame)    │  │
│  │   Help)      │  │                      │  │                      │  │
│  └──────────────┘  └──────────┬───────────┘  └──────────┬───────────┘  │
│                               │                          │              │
│                    ┌──────────┴───────────┐  ┌───────────┴──────────┐  │
│                    │  StatusBar (ttk.Frame)│  │  ProgressBar        │  │
│                    └──────────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                   │                               │
        ┌──────────┴───────────┐         ┌─────────┴──────────┐
        ▼                      ▼         ▼                    ▼
┌───────────────┐  ┌──────────────────┐  ┌────────────────────────────┐
│ core/config   │  │ core/            │  │ core/                      │
│  .py          │  │ term_extractor   │  │ filter_engine.py           │
│               │  │ .py              │  │                            │
│ SYNONYMS      │  │                  │  │ count_matches(df, pattern) │
│ BRAND_KW      │  │ extract_terms()  │  │ build_suggestions(df,terms)│
│ OUTPUT_COLS   │  │                  │  │                            │
│ Style colors  │  └──────────────────┘  └────────────┬───────────────┘
└───────────────┘                                     │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      core/excel_exporter.py                             │
│  export_filtered_xlsx(df, pattern, input_file, output_dir)              │
│  → Tạo Excel 6 cột với style (header xanh, hàng xen kẽ, brand vàng)    │
│  → Đặt tên: {prefix}_{HH-MM-SS}_{DD-MM-YYYY}.xlsx                      │
└─────────────────────────────────────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     utils/file_manager.py                               │
│  load_config_files() — đọc keywords.txt, brands.txt, filters.txt       │
│  discover_input_files() — quét input/ tìm file .xlsx Cerebro           │
│  generate_output_filename(prefix) — sinh tên file theo format mới       │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Class Diagram

```
┌──────────────────────────────────┐
│         MainWindow (tk.Tk)       │
├──────────────────────────────────┤
│ - step1_panel: Step1Panel        │
│ - step2_panel: Step2Panel        │
│ - status_bar: StatusBar          │
│ - shared_state: dict             │  ← chia sẻ dữ liệu giữa 2 step
│   {                              │
│     "input_file": str,           │
│     "df": DataFrame,             │
│     "product_name": str,         │
│     "extracted_terms": list,     │
│     "suggestions": list[dict],   │
│     "selected_filter": str,      │
│     "step1_completed": bool,     │
│   }                              │
├──────────────────────────────────┤
│ + __init__()                     │
│ + on_step1_complete(filter)      │  ← callback khi Step 1 xong
│ + update_status(msg, level)      │
│ + run()                          │
└──────────┬───────────────────────┘
           │ owns
    ┌──────┴──────────────────────────────┐
    │                                     │
    ▼                                     ▼
┌───────────────────────┐    ┌───────────────────────────┐
│   Step1Panel          │    │   Step2Panel              │
│   (ttk.LabelFrame)    │    │   (ttk.LabelFrame)        │
├───────────────────────┤    ├───────────────────────────┤
│ - file_selector       │    │ - input_file_label        │
│ - product_name_entry  │    │ - filter_entry            │
│ - terms_display       │    │ - result_count_label      │
│ - suggestion_treeview │    │ - extract_btn             │
│ - selected_filter_var │    │ - open_output_btn         │
│ - analyze_btn         │    ├───────────────────────────┤
│ - export_btn          │    │ + __init__(shared_state)  │
├───────────────────────┤    │ + on_extract()            │
│ + __init__(state)     │    │ + populate(filter, file)  │
│ + on_analyze()        │    └───────────────────────────┘
│ + on_export()         │
│ + _populate_sugg()    │
└───────────────────────┘
```

### 2.3 Nguyên tắc kiến trúc

| Nguyên tắc | Mô tả |
|------------|-------|
| **Preserve Business Logic** | Code trong `core/` giữ nguyên 100% logic nghiệp vụ từ `keyword_filter_tool.py` và `cerebro_extract.py`, chỉ refactor thành hàm/module, không thay đổi thuật toán |
| **Separation of Concerns** | UI (`ui/`) không chứa business logic; business logic (`core/`) không phụ thuộc tkinter |
| **Shared State** | `MainWindow` giữ 1 `shared_state` dict, Step1Panel ghi vào, Step2Panel đọc từ đó |
| **Callback Pattern** | Step1Panel thông báo hoàn thành qua callback → MainWindow mở khóa Step2Panel |
| **Lazy Loading** | DataFrame chỉ load 1 lần khi chọn file, cache trong `shared_state` |

---

## 3. Thiết kế giao diện

### 3.1 Layout tổng thể

```
┌──────────────────────────────────────────────────────────────────────┐
│  📊 PPC Keyword Filter Tools — SAIGON LASH Store        [_] [□] [X] │
├──────────────────────────────────────────────────────────────────────┤
│  File  Help                                                         │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─ 📋 BƯỚC 1: Phân tích & Chọn Filter ─────────────────────────┐  │
│  │                                                                │  │
│  │  📂 File Cerebro:  [___________________________] [📂 Browse]  │  │
│  │                                                                │  │
│  │  📝 Tên sản phẩm: [______________________________________]     │  │
│  │  💡 Ví dụ: Super Narrow Premade Fans 3D C Curl Lash Ext...    │  │
│  │                                                                │  │
│  │  [🔍 Phân tích]                                                │  │
│  │                                                                │  │
│  │  🔎 Từ phân tích được:  premade, fans, narrow, cluster, ...   │  │
│  │                                                                │  │
│  │  ┌──────────────────────────────────────────────────────────┐ │  │
│  │  │  # │ Filter Pattern          │ Kết quả │ Đánh giá       │ │  │
│  │  ├────┼─────────────────────────┼─────────┼────────────────┤ │  │
│  │  │  1 │ premade                 │      45 │ ✅ Lý tưởng    │ │  │
│  │  │  2 │ narrow|slim             │      32 │ ✅ Lý tưởng    │ │  │
│  │  │  3 │ fans|premade            │      78 │ 🟡 Hơi nhiều   │ │  │
│  │  │  4 │ cluster                 │       8 │ ⚪ Quá ít       │ │  │
│  │  │  5 │ premade|cluster         │      53 │ ✅ Lý tưởng    │ │  │
│  │  │  6 │ lash extensions         │     156 │ 🔴 Quá rộng    │ │  │
│  │  └──────────────────────────────────────────────────────────┘ │  │
│  │                                                                │  │
│  │  🎯 Filter đã chọn: [premade|promade              ] [✏️ Sửa]  │  │
│  │                                                                │  │
│  │  [➕ Kết hợp nhiều filter]  [⌨️ Tự nhập filter]  [💾 Xuất]    │  │
│  │                                                                │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                         ⬇  Filter được chuyển xuống Bước 2 ⬇         │
│  ┌─ 📤 BƯỚC 2: Lọc & Xuất Dữ Liệu ──────────────────────────────┐  │
│  │                                                                │  │
│  │  📂 File input:  US_AMAZON_cerebro_B0xxx...xlsx  (từ Bước 1)  │  │
│  │  🎯 Filter:      [premade|promade                            ] │  │
│  │                                                                │  │
│  │  📊 Kết quả dự kiến:  45 từ khóa sẽ được xuất                  │  │
│  │                                                                │  │
│  │  [▶ Lọc & Xuất file]   [📂 Mở thư mục output]                 │  │
│  │                                                                │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  🟢 Sẵn sàng. Vui lòng chọn file Cerebro (.xlsx) để bắt đầu.       │
├──────────────────────────────────────────────────────────────────────┤
│  Progress: [████████████████████████░░░░░░░░░░░░░░░░] 50%           │
└──────────────────────────────────────────────────────────────────────┘
```

### 3.2 Chi tiết từng thành phần UI

#### 3.2.1 Menu Bar

| Menu | Mục | Hành động | Phím tắt |
|------|-----|-----------|----------|
| **File** | Mở file Cerebro... | Mở dialog chọn file .xlsx | `Ctrl+O` |
| | Mở thư mục input | Mở Finder/Explorer tại `input/` | |
| | Mở thư mục output | Mở Finder/Explorer tại `output/` | |
| | ────────────── | | |
| | Thoát | Đóng ứng dụng | `Ctrl+Q` |
| **Help** | Hướng dẫn sử dụng | Mở README.md / dialog hướng dẫn | `F1` |
| | Về phần mềm | Dialog thông tin version | |

#### 3.2.2 Step1Panel — Bước 1: Keyword Filter Tool

| Widget | Kiểu | Mô tả | Kích thước |
|--------|------|-------|------------|
| `file_label` | `ttk.Label` | "📂 File Cerebro:" | |
| `file_entry` | `ttk.Entry` | Đường dẫn file input | width=55 |
| `browse_btn` | `ttk.Button` | "📂 Browse" — mở file dialog | |
| `product_label` | `ttk.Label` | "📝 Tên sản phẩm:" | |
| `product_entry` | `ttk.Entry` | Nhập tên sản phẩm | width=55 |
| `hint_label` | `ttk.Label` | Ví dụ nhập | font=italic, fg=gray |
| `analyze_btn` | `ttk.Button` | "🔍 Phân tích" | |
| `terms_label` | `ttk.Label` | "🔎 Từ phân tích được:" | wraplength=700 |
| `suggestion_tree` | `ttk.Treeview` | Bảng gợi ý filter (4 cột) | height=8 |
| | | Cột: `#`, `Filter Pattern`, `Kết quả`, `Đánh giá` | |
| | | Scrollbar dọc | |
| `filter_var` | `tk.StringVar` | Filter pattern đã chọn | |
| `filter_entry` | `ttk.Entry` | Hiển thị/cho phép sửa filter | state=readonly → normal |
| `edit_btn` | `ttk.Button` | "✏️ Sửa" — bật edit filter_entry | |
| `combine_btn` | `ttk.Button` | "➕ Kết hợp" — chọn nhiều row trong tree | |
| `custom_btn` | `ttk.Button` | "⌨️ Tự nhập" — dialog nhập filter tùy chỉnh | |
| `export_btn` | `ttk.Button` | "💾 Xuất" — export kết quả Bước 1 | |

**Tương tác với Treeview:**
- Click vào 1 row → tự động chọn filter đó, hiển thị vào `filter_entry`
- Double-click → chọn và export luôn
- Ctrl+Click → chọn nhiều row cho chức năng "Kết hợp"
- Cột "Đánh giá" hiển thị icon màu: 🟢 (tốt), 🟡 (vừa), 🔴 (xấu)

#### 3.2.3 Step2Panel — Bước 2: Cerebro Extract

| Widget | Kiểu | Mô tả | Trạng thái ban đầu |
|--------|------|-------|--------------------|
| `header_label` | `ttk.Label` | "📤 BƯỚC 2: Lọc & Xuất Dữ Liệu" | — |
| `input_file_label` | `ttk.Label` | Hiển thị file input (kế thừa từ Step 1) | "⏳ Đợi Bước 1 hoàn thành..." |
| `filter_entry` | `ttk.Entry` | Filter pattern (tự động điền từ Step 1) | `state=readonly` |
| `result_label` | `ttk.Label` | "📊 Kết quả dự kiến: XX từ khóa" | Ẩn cho đến khi có filter |
| `extract_btn` | `ttk.Button` | "▶ Lọc & Xuất file" | `state=disabled` ban đầu |
| `open_output_btn` | `ttk.Button` | "📂 Mở thư mục output" | |
| `progress` | `ttk.Progressbar` | Thanh tiến trình khi đang export | `mode='indeterminate'` |

#### 3.2.4 StatusBar

| Thành phần | Mô tả |
|------------|-------|
| `status_label` | Text trạng thái hiện tại (VD: "🟢 Sẵn sàng", "🔵 Đang phân tích...") |
| `progress_bar` | `ttk.Progressbar` — hiển thị khi đang xử lý |
| `stats_label` | (bên phải) Tổng số từ khóa trong file, số filter matches |

### 3.3 Style Guide

```python
# Màu sắc
COLORS = {
    "bg":           "#F5F6FA",      # Background chính
    "panel_bg":     "#FFFFFF",      # Background panel
    "header":       "#1F4E79",      # Xanh đậm (header Excel, accent)
    "accent":       "#2E75B6",      # Xanh nhạt hơn (button, highlight)
    "brand_warn":   "#FFF2CC",      # Vàng cảnh báo brand
    "row_alt":      "#EBF3FB",      # Xanh nhạt xen kẽ
    "success":      "#2E7D32",      # Xanh lá (trạng thái tốt)
    "warning":      "#F57F17",      # Cam (cảnh báo)
    "error":        "#C62828",      # Đỏ (lỗi)
    "text":         "#212121",      # Chữ chính
    "text_light":   "#757575",      # Chữ phụ
}

# Font
FONTS = {
    "title":    ("Arial", 14, "bold"),
    "heading":  ("Arial", 11, "bold"),
    "body":     ("Arial", 10),
    "mono":     ("Courier New", 10),
    "small":    ("Arial", 9),
}
```

### 3.4 Responsive Layout (Grid System)

```
MainWindow sử dụng grid:
  Row 0: Menu bar (menu bar không dùng grid — tự động)
  Row 1: Step1Panel  (sticky="nsew", padx=10, pady=5)
  Row 2: Arrow label (sticky="ew", padx=10)
  Row 3: Step2Panel  (sticky="nsew", padx=10, pady=5)
  Row 4: StatusBar   (sticky="ew", padx=0, pady=0)

  Column 0: weight=1 (expand)
  Row 1,3: weight=1 để panel có thể expand

Kích thước mặc định: 900x750px, tối thiểu: 800x600px
```

---

## 4. Data Flow chi tiết

### 4.1 Flow tổng thể

```
┌─────────────────────────────────────────────────────────────────────┐
│                         APP KHỞI ĐỘNG                                │
├─────────────────────────────────────────────────────────────────────┤
│  1. main.py → MainWindow.__init__()                                 │
│  2. utils/file_manager.py: đọc input/keywords.txt, brands.txt       │
│     → merge với BRAND_KEYWORDS mặc định trong config.py             │
│  3. utils/file_manager.py: đọc input/filters.txt → lịch sử filter   │
│  4. UI hiển thị, Step2Panel bị khóa (disabled)                      │
└─────────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   USER CHỌN FILE CEREBRO                            │
├─────────────────────────────────────────────────────────────────────┤
│  1. Click "Browse" → file dialog chỉ hiện *.xlsx                    │
│  2. Chọn file → pandas.read_excel(input_file)                       │
│  3. Validate: có cột "Keyword Phrase" + "H10 PPC Sugg. Bid"         │
│  4. Lưu vào shared_state["df"], shared_state["input_file"]          │
│  5. StatusBar: "📂 Đã load 1,247 từ khóa"                           │
└─────────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 BƯỚC 1: PHÂN TÍCH & CHỌN FILTER                     │
├─────────────────────────────────────────────────────────────────────┤
│  1. User nhập tên sản phẩm → product_entry                          │
│  2. Click "🔍 Phân tích"                                            │
│     ┌──────────────────────────────────────────────────────────┐    │
│     │ a. terms = extract_terms(product_name)                   │    │
│     │    - Tách unigrams + bigrams                              │    │
│     │    - Lọc stop words                                       │    │
│     │    - Mở rộng SYNONYMS                                     │    │
│     │    - Deduplicate, giữ thứ tự                               │    │
│     │                                                           │    │
│     │ b. suggestions = build_suggestions(df, terms)             │    │
│     │    - Với mỗi term đơn: count_matches() → lọc count=0      │    │
│     │    - Kết hợp OR 2 terms (từ good_single[0:20])            │    │
│     │    - Score: 20-60=ideal, 10-20=ít, 60-100=nhiều, ...     │    │
│     │    - Sort theo score                                      │    │
│     │                                                           │    │
│     │ c. Cập nhật terms_display: hiển thị 12 terms đầu tiên     │    │
│     │ d. Cập nhật suggestion_treeview: 20 suggestions đầu       │    │
│     └──────────────────────────────────────────────────────────┘    │
│  3. User xem suggestions trong treeview → click chọn filter         │
│     (hoặc chọn nhiều + "Kết hợp", hoặc "Tự nhập")                   │
│  4. filter_entry hiển thị pattern đã chọn                           │
│  5. User click "✏️ Sửa" để edit trực tiếp (AND: &, OR: |)          │
│  6. [Optional] Click "💾 Xuất" → export ngay từ Bước 1              │
│     ┌──────────────────────────────────────────────────────────┐    │
│     │ export_filtered_xlsx(df, pattern, input_file, output/)   │    │
│     │ → Tạo file: Filtered_{product_slug}_{HH-MM-SS}_{DD-MM-YYYY}.xlsx │
│     └──────────────────────────────────────────────────────────┘    │
│  7. Callback on_step1_complete(filter) → mở khóa Step2Panel         │
└─────────────────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│              BƯỚC 2: LỌC & XUẤT DỮ LIỆU (tự động điền)             │
├─────────────────────────────────────────────────────────────────────┤
│  1. Step2Panel nhận filter từ shared_state["selected_filter"]       │
│  2. filter_entry tự động hiển thị pattern                           │
│  3. Gọi count_matches(df, pattern) → hiển thị số kết quả            │
│  4. User có thể sửa filter nếu muốn                                 │
│  5. Click "▶ Lọc & Xuất file"                                       │
│     ┌──────────────────────────────────────────────────────────┐    │
│     │ a. mask = df["Keyword Phrase"].str.contains(pattern, ...)│    │
│     │ b. fdf = df[mask].copy().reset_index(drop=True)           │    │
│     │ c. Nếu len(fdf) == 0 → hiển thị cảnh báo, không export   │    │
│     │ d. export_xlsx() với style:                               │    │
│     │    - Header: #1F4E79, chữ trắng, Arial 10 bold           │    │
│     │    - Hàng xen kẽ: #EBF3FB / trắng                         │    │
│     │    - Brand keyword: nền vàng #FFF2CC                      │    │
│     │    - 6 cột: Keyword Phrase, Search Volume, Sponsored      │    │
│     │      ASINs, Competing Products, CPR, Bid                  │    │
│     │    - Format: integer (Search Volume, CPR...),             │    │
│     │      currency (Bid: $"#,##0.00")                          │    │
│     │    - Freeze pane: A2                                      │    │
│     │ e. Lưu vào output/ với tên:                               │    │
│     │    PPC_Keywords_{HH-MM-SS}_{DD-MM-YYYY}.xlsx              │    │
│     └──────────────────────────────────────────────────────────┘    │
│  6. Hiển thị thông báo thành công: số từ khóa + brand warning       │
│  7. Ghi pattern vào input/filters.txt (append)                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Shared State chi tiết

```python
shared_state = {
    # ── Input ─────────────────────────────────────────────
    "input_file":       None,       # str  — đường dẫn file Cerebro
    "df":               None,       # DataFrame — dữ liệu đã load
    "total_keywords":   0,          # int  — tổng số keyword trong file

    # ── Brand & Config ────────────────────────────────────
    "brand_keywords":   [...],      # list — merge từ BRAND_KEYWORDS + brands.txt
    "bad_keywords":     [...],      # list — từ keywords.txt (để filter exclude)
    "filters_history":  [...],      # list — từ filters.txt

    # ── Step 1 Results ────────────────────────────────────
    "product_name":     "",         # str  — tên sản phẩm user nhập
    "extracted_terms":  [],         # list — kết quả extract_terms()
    "suggestions":      [],         # list[dict] — {pattern, count, terms}
    "selected_filter":  "",         # str  — filter pattern đã chọn
    "selection_method": "",         # str  — "single", "combined", "custom"
    "step1_match_count": 0,         # int  — số keyword khớp filter ở Step 1
    "step1_completed":  False,      # bool — đã hoàn thành Bước 1 chưa?

    # ── Step 2 Results ────────────────────────────────────
    "step2_output_file": None,      # str  — đường dẫn file output Bước 2
    "step2_brands_found": [],       # list — brand keywords tìm thấy
}
```

### 4.3 File Naming Convention mới

```
Format: {prefix}_{HH-MM-SS}_{DD-MM-YYYY}.xlsx

Trong đó:
  - prefix:
      Bước 1: "Filtered_" + slug(tên sản phẩm, max 30 ký tự)
      Bước 2: "PPC_Keywords"
  - HH-MM-SS: giờ:phút:giây lúc export (24h format)
  - DD-MM-YYYY: ngày/tháng/năm lúc export

Ví dụ:
  Bước 1: Filtered_Premade_Narrow_Fans_14-28-15_12-05-2026.xlsx
  Bước 2: PPC_Keywords_14-30-25_12-05-2026.xlsx

Hàm: utils/file_manager.py → generate_output_filename(prefix)
```

---

## 5. Danh sách component/module cần code

### 5.1 Module List

| # | File | Loại | Mức độ | Mô tả |
|---|------|------|--------|-------|
| **M1** | `src/core/config.py` | Mới | ⭐ Dễ | Constants & configuration |
| **M2** | `src/core/term_extractor.py` | Refactor | ⭐⭐ Vừa | Trích xuất từ `keyword_filter_tool.py` (dòng 29–109) |
| **M3** | `src/core/filter_engine.py` | Refactor | ⭐⭐ Vừa | Trích xuất từ `keyword_filter_tool.py` (dòng 69–145) |
| **M4** | `src/core/excel_exporter.py` | Refactor | ⭐⭐⭐ Khó | Trích xuất từ `keyword_filter_tool.py` (dòng 176–245) + `cerebro_extract.py` (dòng 41–150) |
| **M5** | `src/utils/file_manager.py` | Mới | ⭐⭐ Vừa | File I/O, naming, config load |
| **M6** | `src/utils/validators.py` | Mới | ⭐ Dễ | Validate input files, regex |
| **M7** | `src/ui/widgets.py` | Mới | ⭐⭐ Vừa | UI components tái sử dụng |
| **M8** | `src/ui/step1_panel.py` | Mới | ⭐⭐⭐ Khó | Giao diện Bước 1 |
| **M9** | `src/ui/step2_panel.py` | Mới | ⭐⭐ Vừa | Giao diện Bước 2 |
| **M10** | `src/ui/app.py` | Mới | ⭐⭐⭐ Khó | MainWindow - cửa sổ chính |
| **M11** | `src/main.py` | Mới | ⭐ Dễ | Entry point |
| **M12** | `tests/*.py` | Mới | ⭐⭐ Vừa | Unit tests |
| **M13** | `input/` (thư mục + sample files) | Mới | ⭐ Dễ | Tạo thư mục + sample |
| **M14** | `output/` (thư mục) | Mới | ⭐ Dễ | Tạo thư mục rỗng |

### 5.2 Chi tiết từng module cốt lõi

#### M1: `src/core/config.py`

```python
"""
Tập trung tất cả constants, không hardcode ở bất kỳ đâu khác.
"""
# ── Từ đồng nghĩa (giữ nguyên từ keyword_filter_tool.py) ──
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

# ── Từ quá chung ──
TOO_BROAD_ALONE = {"lash", "lashes", "extension", "extensions", "false",
                   "individual", "strip", "pack", "tray", "fans", "volume"}

# ── Stop words ──
STOP_WORDS = {"the","a","an","and","or","for","of","in","on","at","to","by",
              "is","are","with","very","super","ultra","pro","top","best","new",
              "all","set","kit","size","type","style","from","into","store",
              "brand","by","c","d","b","curl","mm","0.07","0.05","0.03",
              "1000","500","200"}

# ── Brand mặc định ──
DEFAULT_BRAND_KEYWORDS = ["vavalash", "veyes", "fabu", "lilash", "novalash",
                           "ardell", "kiss", "nyx", "essence", "mac"]

# ── Output columns mapping ──
OUTPUT_COLS = {
    "Keyword Phrase":     "Keyword Phrase",
    "Search Volume":      "Search Volume",
    "Sponsored ASINs":    "Sponsored ASINs",
    "Competing Products": "Competing Products",
    "CPR":                "CPR",
    "Bid":                "H10 PPC Sugg. Bid",
}

# ── Excel Style ──
EXCEL_STYLE = {
    "header_color":  "1F4E79",
    "header_font":   {"name": "Arial", "bold": True, "color": "FFFFFF", "size": 10},
    "row_alt_color": "EBF3FB",
    "brand_color":   "FFF2CC",
    "border_color":  "CCCCCC",
    "font_name":     "Arial",
    "font_size":     10,
}

# ── Column widths & formats ──
COLUMN_WIDTHS = {
    "Keyword Phrase": 40, "Search Volume": 14, "Sponsored ASINs": 15,
    "Competing Products": 17, "CPR": 8, "Bid": 10,
}
COLUMN_FORMATS = {
    "Search Volume": '#,##0', "Sponsored ASINs": '#,##0',
    "Competing Products": '#,##0', "CPR": '#,##0',
    "Bid": '"$"#,##0.00',
}

# ── UI Colors ──
UI_COLORS = {
    "bg":           "#F5F6FA",
    "panel_bg":     "#FFFFFF",
    "header":       "#1F4E79",
    "accent":       "#2E75B6",
    "success":      "#2E7D32",
    "warning":      "#F57F17",
    "error":        "#C62828",
    "text":         "#212121",
    "text_light":   "#757575",
}

# ── Scoring thresholds ──
SCORE_THRESHOLDS = {
    "ideal_min":  20,
    "ideal_max":  60,
    "low_max":    10,
    "high_max":   100,
}
```

#### M2: `src/core/term_extractor.py`
- Refactor nguyên hàm `extract_terms()` từ `keyword_filter_tool.py` (dòng 77–109)
- Input: product_name (str) → Output: list[str] terms đã expand synonyms + deduplicate

#### M3: `src/core/filter_engine.py`
- Refactor nguyên `count_matches()` (dòng 69–73) và `build_suggestions()` (dòng 112–145)
- Input: DataFrame + list terms → Output: list[dict] suggestions đã score & sort

#### M4: `src/core/excel_exporter.py`
- Hợp nhất `export_xlsx()` từ keyword_filter_tool.py (dòng 176–245) và `extract()` từ cerebro_extract.py (dòng 41–150)
- 2 hàm public: `export_filtered_xlsx()` và `preview_match_count()`
- Giữ nguyên style: header #1F4E79, hàng xen kẽ #EBF3FB, brand vàng #FFF2CC

#### M5: `src/utils/file_manager.py`
- `load_keywords_file()`, `load_brands_file()`, `load_filters_history()`
- `discover_xlsx_files()` — quét input/ tìm .xlsx
- `generate_output_filename(prefix)` — format mới: `{prefix}_{HH-MM-SS}_{DD-MM-YYYY}.xlsx`
- `append_filter_to_history()` — ghi thêm vào filters.txt

#### M6: `src/utils/validators.py`
- `validate_cerebro_file()` — kiểm tra file tồn tại, đọc được, có cột bắt buộc
- `validate_filter_pattern()` — regex hợp lệ
- `validate_product_name()` — không rỗng, đủ dài

### 5.3 Tổng hợp số dòng dự kiến

| Module | Dòng dự kiến | Ghi chú |
|--------|-------------|---------|
| `core/config.py` | ~80 | Constants thuần |
| `core/term_extractor.py` | ~70 | Refactor từ tool gốc |
| `core/filter_engine.py` | ~90 | Refactor từ tool gốc |
| `core/excel_exporter.py` | ~160 | Gộp logic từ 2 tool |
| `utils/file_manager.py` | ~80 | Mới hoàn toàn |
| `utils/validators.py` | ~60 | Mới hoàn toàn |
| `ui/widgets.py` | ~50 | Components tái sử dụng |
| `ui/step1_panel.py` | ~300 | UI chính Bước 1 |
| `ui/step2_panel.py` | ~200 | UI chính Bước 2 |
| `ui/app.py` | ~200 | MainWindow + menu + statusbar |
| `main.py` | ~15 | Entry point |
| **Tổng** | **~1,305** | |

---

## 6. Kế hoạch triển khai

### 6.1 Thứ tự ưu tiên (Implementation Order)

```
Giai đoạn 0: Setup (0.5 ngày)
├── T0.1  Tạo cấu trúc thư mục (input/, output/, src/, tests/, resources/)
├── T0.2  Tạo requirements.txt
├── T0.3  Tạo sample files trong input/
└── T0.4  Commit khởi tạo

Giai đoạn 1: Core Layer (1.5 ngày) ← ƯU TIÊN CAO NHẤT
├── T1.1  Viết core/config.py (constants)
├── T1.2  Refactor term_extractor.py từ keyword_filter_tool.py
├── T1.3  Refactor filter_engine.py từ keyword_filter_tool.py
├── T1.4  Refactor excel_exporter.py (hợp nhất 2 tool)
└── T1.5  Viết unit test cho core layer

Giai đoạn 2: Utilities (0.5 ngày)
├── T2.1  Viết utils/validators.py
├── T2.2  Viết utils/file_manager.py (file I/O, naming)
└── T2.3  Test file_manager với sample files

Giai đoạn 3: UI Layer (2 ngày)
├── T3.1  Viết ui/widgets.py (StyledButton, PlaceholderEntry...)
├── T3.2  Viết ui/step1_panel.py (UI Bước 1 + tích hợp core)
├── T3.3  Viết ui/step2_panel.py (UI Bước 2 + tích hợp core)
├── T3.4  Viết ui/app.py (MainWindow + menu + statusbar)
└── T3.5  Viết main.py (entry point)

Giai đoạn 4: Integration & Polish (1 ngày)
├── T4.1  Kiểm tra data flow end-to-end
├── T4.2  Xử lý edge cases (file not found, empty filter, etc.)
├── T4.3  Test với file Cerebro thực tế
├── T4.4  Polish UI (padding, màu sắc, responsive)
└── T4.5  Viết README.md hướng dẫn sử dụng

Tổng: ~5.5 ngày làm việc
```

### 6.2 Timeline Gantt

```
Task          │ Day 1 │ Day 2 │ Day 3 │ Day 4 │ Day 5 │ Day 6 │
──────────────┼───────┼───────┼───────┼───────┼───────┼───────┤
GĐ0: Setup    │ ██    │       │       │       │       │       │
GĐ1: Core     │   ███ │ ███   │       │       │       │       │
GĐ2: Utils    │       │   ██  │       │       │       │       │
GĐ3: UI       │       │       │ ████  │ ████  │       │       │
GĐ4: Polish   │       │       │       │       │ ████  │ █     │
──────────────┼───────┼───────┼───────┼───────┼───────┼───────┤
Milestone     │Setup✓ │Core✓  │Utils✓ │UI✓    │       │Done✓  │
```

### 6.3 Dependency Graph giữa các task

```
                T0.1 (Folder)
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
    T1.1       T2.1        (sample)
  config.py  validators      files
        │          │
        ▼          │
    T1.2           │
  term_extr.      │
        │          │
        ▼          │
    T1.3           │
  filter_eng.     │
        │          │
        ▼          ▼
    T1.4 ←──── T2.2
  excel_exp.  file_mgr
        │          │
        ▼          ▼
    T1.5       T2.3
  core tests  util tests
        │          │
        └────┬─────┘
             ▼
          T3.1
         widgets
             │
        ┌────┴────┐
        ▼         ▼
     T3.2       T3.3
  step1_panel step2_panel
        │         │
        └────┬────┘
             ▼
          T3.4
         app.py
             │
             ▼
          T3.5
         main.py
             │
             ▼
        GĐ4: Polish
```

---

## 7. Rủi ro & Edge case

### 7.1 Rủi ro kỹ thuật

| ID | Rủi ro | Impact | Mitigation |
|----|--------|--------|------------|
| **R1** | File Cerebro có schema cột khác (Helium 10 thay đổi tên cột) | 🔴 Cao | Validate REQUIRED_COLUMNS ngay khi load file; hiển thị lỗi rõ ràng + gợi ý tên cột cần có |
| **R2** | File Excel quá lớn (>100MB) → pandas chậm, UI treo | 🟡 Vừa | Chạy pandas trong thread riêng (threading); hiển thị progress bar indeterminate khi đang load |
| **R3** | Regex pattern user nhập gây lỗi (VD: dấu ngoặc không đóng) | 🟡 Vừa | Validate pattern bằng re.compile() trước khi dùng; bắt exception, hiển thị lỗi thân thiện |
| **R4** | Tkinter không hỗ trợ Unicode/emoji trên Windows | 🟢 Thấp | Test trên cả macOS & Windows; fallback emoji → text prefix ([OK], [WARN], [ERR]) |
| **R5** | openpyxl style gây corrupt file nếu dữ liệu có ký tự đặc biệt | 🔴 Cao | Escape/sanitize dữ liệu trước khi ghi vào cell; test với dữ liệu thực tế |
| **R6** | Xung đột giữa BRAND_KEYWORDS mặc định và brands.txt (trùng lặp) | 🟢 Thấp | Merge + deduplicate bằng set() khi load config |

### 7.2 Edge cases

| # | Edge case | Cách xử lý |
|---|-----------|------------|
| **E1** | `input/` không tồn tại khi app khởi động | Tự động tạo thư mục `input/` và `output/` nếu chưa có |
| **E2** | `input/` rỗng (không có file .xlsx nào) | Hiển thị message: "Chưa có file Cerebro trong input/. Vui lòng đặt file .xlsx vào thư mục input/" |
| **E3** | User chọn file .xlsx không phải Cerebro export (thiếu cột "Keyword Phrase") | Validate khi load → hiển thị dialog lỗi, không cho tiếp tục |
| **E4** | `extract_terms()` trả về list rỗng (tên sản phẩm toàn stop words) | Hiển thị warning: "Không tìm thấy từ khóa có nghĩa. Hãy nhập tên sản phẩm chi tiết hơn." |
| **E5** | `build_suggestions()` trả về list rỗng (không term nào match) | Hiển thị message: "Không tìm thấy kết quả khớp. Thử nhập tên sản phẩm khác hoặc dùng chức năng Tự nhập filter." |
| **E6** | Filter pattern khớp 0 kết quả | Hiển thị warning, không cho export, gợi ý thử filter khác |
| **E7** | Filter pattern khớp >500 kết quả (quá rộng) | Hiển thị warning xác nhận: "Filter này cho ra XX kết quả (rất nhiều). Bạn có chắc muốn xuất?" |
| **E8** | User đóng app khi đang export | Bắt sự kiện WM_DELETE_WINDOW → hỏi xác nhận nếu đang có tiến trình |
| **E9** | `output/` có file trùng tên (export 2 lần trong cùng 1 giây) | Sinh timestamp chính xác đến mili giây nếu cần; append (2) vào tên file |
| **E10** | User muốn dùng filter từ lịch sử (`filters.txt`) | Thêm dropdown/combobox "Lịch sử filter" trong Step 1 và Step 2 |
| **E11** | brands.txt chứa ký tự đặc biệt hoặc encoding lạ | Đọc với encoding='utf-8', fallback 'latin-1'; strip whitespace; bỏ dòng trống |
| **E12** | User chưa hoàn thành Bước 1 mà đã click vào Bước 2 | Step2Panel bị disabled hoàn toàn cho đến khi `on_step1_complete` được gọi |
| **E13** | Tên sản phẩm có dấu tiếng Việt → extract_terms() xử lý sai | Chuẩn hóa về ASCII/Lowercase trước khi xử lý (đã có trong code gốc: `.lower()`) |
| **E14** | H10 PPC Sugg. Bid có giá trị None/NaN | Xử lý pd.isna() trước khi format (đã có trong code gốc, cần giữ nguyên) |

### 7.3 Risk Matrix

```
                      Likelihood
                    Thấp   Vừa    Cao
Impact  ┌────────┬───────┬───────┬───────┐
  Cao   │        │  R2   │R1, R5 │
        ├────────┼───────┼───────┼───────┤
  Vừa   │        │  R3   │       │
        ├────────┼───────┼───────┼───────┤
  Thấp  │ R4, R6 │       │       │
        └────────┴───────┴───────┴───────┘
```

---

## Phụ lục

### A. Logic nghiệp vụ giữ nguyên (từ source code gốc)

| Logic | Vị trí gốc | Vị trí mới | Ghi chú |
|-------|-----------|------------|---------|
| `SYNONYMS` dict | `keyword_filter_tool.py:29-50` | `core/config.py` | Copy nguyên, mở rộng được trong tương lai |
| `TOO_BROAD_ALONE` | `keyword_filter_tool.py:53-54` | `core/config.py` | Copy nguyên |
| `STOP_WORDS` | `keyword_filter_tool.py:87-90` | `core/config.py` | Copy nguyên |
| `BRAND_KEYWORDS` | `keyword_filter_tool.py:65-66` | `core/config.py` + merge với `brands.txt` | Mở rộng: merge từ file |
| `OUTPUT_COLS` mapping | `keyword_filter_tool.py:56-63` | `core/config.py` | Copy nguyên |
| `count_matches()` | `keyword_filter_tool.py:69-73` | `core/filter_engine.py` | Copy nguyên |
| `extract_terms()` | `keyword_filter_tool.py:77-109` | `core/term_extractor.py` | Copy nguyên |
| `build_suggestions()` | `keyword_filter_tool.py:112-145` | `core/filter_engine.py` | Copy nguyên |
| `export_xlsx()` style | `keyword_filter_tool.py:176-245` | `core/excel_exporter.py` | Copy nguyên phần style |
| `extract()` logic | `cerebro_extract.py:41-150` | `core/excel_exporter.py` | Gộp với export_xlsx() |
| Column widths/format | `cerebro_extract.py:76-84` | `core/config.py` | Copy nguyên |

### B. So sánh trước/sau

| Tiêu chí | Trước (CLI) | Sau (Desktop App) |
|----------|-------------|-------------------|
| Giao diện | Terminal/text | GUI tkinter |
| Workflow | 2 tool riêng biệt, chạy thủ công | 1 app, 2 bước liên tiếp tự động |
| File input | Truyền qua command line | Chọn qua file dialog hoặc đặt vào `input/` |
| File output | Lưu cạnh file input | Lưu vào `output/` riêng biệt |
| Tên file output | `{name}_data_{YYYY-MM-DD}.xlsx` | `{prefix}_{HH-MM-SS}_{DD-MM-YYYY}.xlsx` |
| Brand keywords | Hardcode trong code | Load từ `brands.txt` + default |
| Lịch sử filter | Không lưu | Tự động ghi vào `filters.txt` |
| Xử lý lỗi | Print + sys.exit() | Dialog thông báo thân thiện |
| User persona | Cần biết CLI | Người dùng phổ thông |

### C. Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|------------|---------|
| Python | 3.8+ |
| pandas | >= 1.3.0 |
| openpyxl | >= 3.0.0 |
| tkinter | Có sẵn trong Python (đảm bảo không bị strip) |
| OS | macOS 10.14+ / Windows 10+ / Linux (với python3-tk) |
| RAM | >= 512MB (cho file Excel lớn) |
| Disk | < 50MB (code + dependencies) |

---

> **Tài liệu kế hoạch triển khai — SAIGON LASH Store / MariaMCP**  
> **Ngày tạo:** 2026-05-12 | **Người lập:** Planner Agent  
> **Trạng thái:** ✅ Sẵn sàng triển khai
