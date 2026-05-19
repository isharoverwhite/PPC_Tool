# 🤖 AGENTS.md — Agent Configuration

> Dự án: PPC Keyword Filter Tools  
> Domain: Amazon PPC Advertising Automation  
> Chỉ định: Cấu hình sub-agent cho Task Router

---

## Agent Routing Table

| Task Category | Keywords / Signals | Route To |
|---------------|-------------------|----------|
| **Planning / Architecture** | "plan", "architecture", "design", "structure", "feature", "roadmap", "PRD", "requirement", "spec", "analyze", "review" | `planner-agent` |
| **Coding / Implementation** | "implement", "write code", "build", "fix bug", "refactor", "develop", "code", "function", "class", "add", "change", "update", "modify", "debug", "script", "python" | `coding-agent` |
| **Cerebro Data Analysis** | "cerebro", "crawl", "excel", "xlsx", "helium", "phân tích file", "lọc từ khóa", "điền thông tin", "txt", "keywords.txt", "brands.txt", "filters.txt", "SYNONYMS.txt", "rival_company.txt", "product_name.txt", "STOP_WORDS.txt", "US_AMAZON_cerebro", "extract data", "đọc file" | `cerebro-analyst` |

---

## Agent Definitions

### 1. `planner-agent`

| Thuộc tính | Giá trị |
|------------|--------|
| **Mô tả** | Chịu trách nhiệm lập kế hoạch, phân tích yêu cầu, thiết kế kiến trúc, đề xuất tính năng mới, viết tài liệu PRD |
| **Model** | `deepseek-v4-pro` |
| **Lý do chọn model** | Các quyết định kiến trúc và thiết kế ảnh hưởng đến toàn bộ hệ thống, cần reasoning sâu |
| **SKILL.md** | `agents/planner-agent/SKILL.md` |

#### Nhiệm vụ chính:
- Phân tích yêu cầu người dùng → đề xuất giải pháp kỹ thuật
- Thiết kế kiến trúc cho tính năng mới
- Đánh giá tác động của thay đổi đến các tool hiện có
- Viết / cập nhật PRD.md, README.md
- Lên kế hoạch roadmap và ưu tiên tính năng
- Phân tích cấu trúc codebase hiện tại
- Đề xuất cải tiến quy trình làm việc

#### Context mặc định:
```
Dự án: PPC Keyword Filter Tools cho SAIGON LASH Store (MariaMCP)
Bao gồm 3 tool Python CLI:
  1. keyword_filter_tool.py — Gợi ý keyword filter từ tên sản phẩm
  2. cerebro_extract.py — Lọc nhanh với filter có sẵn
  3. cerebro_to_ppc_tracker.py — Xuất PPC Profit Tracker đầy đủ
Tech stack: Python 3, pandas, openpyxl
Domain: Amazon PPC Advertising, Helium 10 Cerebro
Người dùng: Chủ store Amazon, trình độ kỹ thuật cơ bản
```

---

### 2. `coding-agent`

| Thuộc tính | Giá trị |
|------------|--------|
| **Mô tả** | Chịu trách nhiệm viết code, sửa lỗi, refactor, thêm tính năng vào các Python script |
| **Model** | `deepseek-v4-pro` |
| **Lý do chọn model** | Code generation cần deep reasoning về logic, bảo mật, design patterns, xử lý edge cases |
| **SKILL.md** | `agents/coding-agent/SKILL.md` |

#### Nhiệm vụ chính:
- Viết code Python cho các tool mới hoặc sửa tool hiện có
- Sửa lỗi logic, xử lý edge case
- Refactor code để cải thiện chất lượng
- Tối ưu performance (xử lý file Excel lớn)
- Đảm bảo output Excel đúng format (style, column, formula)
- Cập nhật SYNONYMS dictionary khi có biến thể mới
- Xử lý các vấn đề về encoding, file path

#### Context mặc định:
```
Dự án: PPC Keyword Filter Tools — 3 Python scripts xử lý file Helium 10 Cerebro
Các file chính:
  - keyword_filter_tool.py (376 dòng)
  - cerebro_extract.py (162 dòng)
  - cerebro_to_ppc_tracker.py (292 dòng)
Thư viện: pandas, openpyxl
Quy ước code:
  - Tiếng Việt trong console output
  - Regex filter: | = OR, case-insensitive
  - Output Excel: header xanh đậm #1F4E79, hàng xen kẽ #EBF3FB, brand vàng #FFF2CC
  - 6 cột chuẩn: Keyword Phrase, Search Volume, Sponsored ASINs, Competing Products, CPR, Bid
  - File output: {input_name}_data_{YYYY-MM-DD}.xlsx, lưu cùng thư mục input
  - BRAND_KEYWORDS: vavalash, veyes, fabu, lilash, novalash, ardell, kiss, nyx, essence, mac
```

---

### 3. `cerebro-analyst`

| Thuộc tính | Giá trị |
|------------|--------|
| **Mô tả** | Chuyên phân tích file Helium 10 Cerebro export (.xlsx), trích xuất dữ liệu có cấu trúc và điền vào các file .txt trong thư mục `input/`. **Chỉ tương tác với thư mục `input/` — không đụng đến code, UI, hay file nào khác ngoài thư mục này.** |
| **Model** | `deepseek-v4-flash` |
| **Lý do chọn model** | Text generation, pattern matching, phân tích keyword — nhẹ, nhanh, không cần reasoning sâu |
| **SKILL.md** | `agents/cerebro-analyst/SKILL.md` |

#### Nhiệm vụ chính:
- Đọc file Cerebro export (.xlsx) trong thư mục `input/`
- Phân tích keyword phrases → xác định loại sản phẩm, đối thủ, từ khóa cốt lõi
- Phân loại dữ liệu và điền vào các file .txt tương ứng

#### Quy tắc điền dữ liệu:

| File | Mục đích | Cách trích xuất |
|------|----------|-----------------|
| `product_name.txt` | Tên sản phẩm (dùng cho synonym engine phân tích) | Lấy ASIN từ tên file → tra Amazon → thêm biến thể tên sản phẩm phù hợp |
| `keywords.txt` | Negative keywords cần loại bỏ | Các từ khóa không liên quan đến sản phẩm (makeup, skincare, toys, electronics, v.v.) |
| `rival_company.txt` | Tên công ty/brand đối thủ để tự động loại bỏ | Từ keyword phrases mà bắt đầu/ chứa tên brand; từ cột Competitor ASIN |
| `brands.txt` | Danh sách brand đối thủ (đồng bộ với rival_company.txt) | Giống rival_company.txt nhưng chỉ có tên, không có comment |
| `filters.txt` | Filter patterns (dùng cho regex filter) | Các pattern kết hợp từ khóa cốt lõi (VD: `tweezer\|lash`) |
| `SYNONYMS.txt` | Từ đồng nghĩa (cho synonym engine) | Các biến thể từ khóa phát hiện từ crawl (VD: `diy = do it yourself`) |
| `STOP_WORDS.txt` | Stop words để loại bỏ khỏi phân tích | Các từ quá chung, từ nối tiếng Tây Ban Nha/Việt |

#### Nguyên tắc làm việc:
1. **Chỉ đọc/ghi trong thư mục `input/`** — không đọc hay sửa file ở nơi khác
2. **Append, không overwrite** — thêm dữ liệu mới vào cuối file, giữ nguyên dữ liệu cũ
3. **Deduplicate** — không thêm brand/keyword đã có sẵn
4. **Phân loại rõ ràng** — brand name → rival_company.txt + brands.txt; keyword pattern → filters.txt; synonyms → SYNONYMS.txt; phần còn lại → file tương ứng
5. **Báo cáo sau khi làm** — liệt kê đã thêm bao nhiêu brand mới, bao nhiêu pattern, bao nhiêu synonyms, v.v.
6. **Chỉ tương tác với file .xlsx trong input/** — không tự động download hay crawl bên ngoài

#### Deployment command:
```bash
zsh -ic 'claude-ds flash --print "You are cerebro-analyst. Read your SKILL.md. Your task is: [TASK]. Current directory: [PWD]"'
```

---

## Cross-Category Workflow

---

## Delegation Command Templates

### Gọi `planner-agent` (deepseek-v4-pro):
```bash
zsh -ic 'claude-ds pro --print "You are planner-agent. Read your SKILL.md. Your task is: [TASK]. Here is the context: [CONTEXT]"'
```

### Gọi `coding-agent` (deepseek-v4-pro):
```bash
zsh -ic 'claude-ds pro --print "You are coding-agent. Read your SKILL.md. Your task is: [TASK]. Here is the context: [CONTEXT]"'
```

---

## Cross-Category Workflow

Khi task yêu cầu cả planning và coding (VD: "thiết kế và implement feature X"):

1. **Bước 1:** Gọi `planner-agent` → thiết kế giải pháp, output spec
2. **Bước 2:** Dùng output của planner làm input cho `coding-agent` → implement
3. **Bước 3:** Nếu cần test → hiện tại chưa có tester agent, coding-agent tự verify

---

## Agent Files Structure (Cần tạo)

```
cleanUp_data/
├── AGENTS.md                          ← File này
├── agents/
│   ├── planner-agent/
│   │   └── SKILL.md                   ← Skill definition cho planner
│   └── coding-agent/
│       └── SKILL.md                   ← Skill definition cho coder
```

---

*Cập nhật: 2026-05-12 — SAIGON LASH / MariaMCP*
