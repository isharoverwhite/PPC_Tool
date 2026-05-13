"""
╔══════════════════════════════════════════════════════════════╗
║   CONSTANTS  —  Từ điển đồng nghĩa, brand, cấu hình          ║
╚══════════════════════════════════════════════════════════════╝
"""

# ── SYNONYMS được load từ input/SYNONYMS.txt, không hardcode ở đây ──────────
# File SYNONYMS.txt format:  base_word = variant1, variant2, variant3, ...

# Từ quá chung, không nên dùng một mình
TOO_BROAD_ALONE = {"lash", "lashes", "extension", "extensions", "false", "individual",
                   "strip", "pack", "tray", "fans", "volume"}

# ── STOP_WORDS được load từ input/STOP_WORDS.txt, không hardcode ở đây ──────
# File STOP_WORDS.txt format: mỗi dòng 1 từ cần loại bỏ khi phân tích tên SP

# 6 cột xuất ra (giữ lại cho preview UI)
OUTPUT_COLS = {
    "Keyword Phrase":     "Keyword Phrase",
    "Search Volume":      "Search Volume",
    "Sponsored ASINs":    "Sponsored ASINs",
    "Competing Products": "Competing Products",
    "CPR":                "CPR",
    "Bid":                "H10 PPC Sugg. Bid",
}

# ── 20 cột xuất full (theo format file mẫu AGlobal) ─────────────────────────
# Mỗi entry: (source_column, default_value, number_format)
# source_column=None → dùng default_value hoặc công thức
FULL_EXPORT_COLS = [
    # (Header,         Source col,          Default/Formula,  Number format)
    ("Keyword Phrase",     "Keyword Phrase",      None,              None),
    ("Search Volume",      "Search Volume",       None,              "#,##0"),
    ("Sponsored ASINs",    "Sponsored ASINs",     None,              "#,##0"),
    ("Competing Products", "Competing Products",  None,              "#,##0"),
    ("CPR",                "CPR",                 None,              "#,##0"),
    ("Bid",                "H10 PPC Sugg. Bid",   None,              '"$"#,##0.00'),
    ("CTR",                None,                  0.01,              "0.00%"),
    ("Clicks",             None,                  "=G{n}*B{n}",      "#,##0"),
    ("Spend",              None,                  "=F{n}*H{n}",      '"$"#,##0.00'),
    ("CVR",                None,                  0.05,              "0.0%"),
    ("Ads Orders",         None,                  "=H{n}*J{n}",      "#,##0"),
    ("Price",              None,                  "",                '"$"#,##0.00'),
    ("Ads Revenue",        None,                  "=K{n}*L{n}",      '"$"#,##0.00'),
    ("ACOS",               None,                  "=IF(M{n}=0,\"\",I{n}/M{n})", "0.00%"),
    ("Total Orders",       None,                  "=K{n}+K{n}/4",    "#,##0"),
    ("Total Revenue",      None,                  "=L{n}*O{n}",      '"$"#,##0.00'),
    ("Product Fee",        None,                  "=L{n}/3",         '"$"#,##0.00'),
    ("Amazon Fee",         None,                  "",                None),
    ("Total Fee",          None,                  "=(R{n}+Q{n})*O{n}+I{n}", '"$"#,##0.00'),
    ("Profit",             None,                  "=P{n}-S{n}",      '"$"#,##0.00'),
]

# Column widths matching reference file
FULL_EXPORT_WIDTHS = {
    "Keyword Phrase": 26.0, "Search Volume": 15.38, "Sponsored ASINs": 20.13,
    "Competing Products": 26.0, "CPR": 15.63, "Bid": 7.75,
    "CTR": 11.25, "Clicks": 5.88, "Spend": 7.0, "CVR": 4.75,
    "Ads Orders": 10.13, "Price": 7.63, "Ads Revenue": 11.5,
    "ACOS": 6.63, "Total Orders": 10.75, "Total Revenue": 12.25,
    "Product Fee": 10.63, "Amazon Fee": 10.88, "Total Fee": 8.25,
    "Profit": 7.0,
}

# ── Màu sắc UI ────────────────────────────────────────────────────────────────
# Màu cho tkinter UI (standard hex)
COLORS = {
    "header_bg":   "#1F4E79",
    "header_fg":   "#FFFFFF",
    "row_alt":     "#EBF3FB",
    "brand_warn":  "#FFF2CC",
    "accent":      "#375623",
    "bg":          "#F5F5F5",
    "danger":      "#C55A11",
    "success":     "#2E7D32",
}

# aRGB hex (8 ký tự: FF + màu) cho openpyxl ≥ 3.1
COLORS_ARGB = {
    "header_bg":   "FFE69138",   # Cam — theo format file mẫu AGlobal
    "header_fg":   "FF000000",   # Đen
    "row_alt":     "FFEBF3FB",
    "brand_warn":  "FFFFF2CC",
}

# ── Cấu hình file ─────────────────────────────────────────────────────────────
import os as _os, sys as _sys

def _get_base_dir() -> str:
    """Trả về thư mục gốc của app (hỗ trợ cả dev và packaged .app)."""
    # Kiểm tra nếu đang chạy từ .app bundle (py2app)
    if ".app/Contents/" in _sys.executable:
        # py2app: Resources nằm trong <bundle>/Contents/Resources/
        # sys.executable = .../App.app/Contents/MacOS/App
        # → dirname 2 lần = .../App.app/Contents/
        contents_dir = _os.path.dirname(_os.path.dirname(_sys.executable))
        return _os.path.join(contents_dir, "Resources")
    # Dev mode: dùng thư mục chứa file constants.py (app/) → lên 1 cấp = gốc project
    return _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

_BASE_DIR = _get_base_dir()
INPUT_DIR  = _os.path.join(_BASE_DIR, "input")
OUTPUT_DIR = _os.path.join(_BASE_DIR, "output")

INPUT_FILES = {
    "cerebro":        "input.xlsx",
    "brands":         "brands.txt",
    "keywords":       "keywords.txt",
    "filters":        "filters.txt",
    "synonyms":       "SYNONYMS.txt",
    "stopwords":      "STOP_WORDS.txt",
    "product_name":   "product_name.txt",
    "rival_company":  "rival_company.txt",
}

# ── Đánh giá filter ───────────────────────────────────────────────────────────
RATING_THRESHOLDS = {
    "ideal":    (20, 60),
    "few":      (10, 19),
    "many":     (61, 100),
}
