"""
╔══════════════════════════════════════════════════════════════╗
║   UI  —  Giao diện tkinter cho PPC Keyword Filter Tool       ║
╚══════════════════════════════════════════════════════════════╝
"""
import os, sys, re, threading, webbrowser
from tkinter import ttk, messagebox, filedialog
import tkinter as tk

import pandas as pd

from app.constants import (
    COLORS, INPUT_DIR, INPUT_FILES, OUTPUT_COLS, FULL_EXPORT_COLS, OUTPUT_DIR,
)
from app.engine import FilterEngine, AppState
from app.excel_writer import ExcelWriter
from app.synonym_engine import SynonymEngine, FilterSuggestion


class App:
    """Ứng dụng chính."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 Auto PCC Keywords — made by Experience")
        self.root.geometry("1050x780")
        self.root.minsize(950, 680)
        self.root.configure(bg=COLORS["bg"])

        # Engine
        self.engine = FilterEngine()
        self.writer = ExcelWriter()
        self.syn_engine = SynonymEngine()
        self.state = AppState()

        # Undo stack cho xóa dòng ở Step 2
        self._undo_stack: list[dict] = []  # [{row_data_dict: {src_col: value}, index}, ...]

        # Price & Amazon Fee cho tính toán realtime
        self.price_var = tk.StringVar(value="")
        self.amazon_fee_var = tk.StringVar(value="")

        # Style
        self._setup_style()

        # Build UI
        self._build_menu()
        self._build_step1()
        self._build_step2()
        self._build_statusbar()

        # Auto-load
        self._auto_load()

    # ═══════════════════════════════════════════════════════════════════════
    #  STYLE
    # ═══════════════════════════════════════════════════════════════════════
    def _setup_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("TLabel", font=("Arial", 10), background=COLORS["bg"])
        style.configure("TLabelframe", font=("Arial", 11, "bold"), background=COLORS["bg"])
        style.configure("TLabelframe.Label", font=("Arial", 11, "bold"),
                        background=COLORS["bg"], foreground=COLORS["header_bg"])
        style.configure("TButton", font=("Arial", 10))
        style.configure("Accent.TButton", font=("Arial", 11, "bold"),
                        background=COLORS["accent"])
        style.configure("TEntry", font=("Arial", 10))

        # Treeview style
        style.configure("Treeview", font=("Arial", 10), rowheight=24)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    # ═══════════════════════════════════════════════════════════════════════
    #  MENU
    # ═══════════════════════════════════════════════════════════════════════
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="📂 Mở file Cerebro...", command=self._browse_file)
        file_menu.add_command(label="📁 Mở thư mục output", command=self._open_output_dir)
        file_menu.add_separator()
        file_menu.add_command(label="⟳ Tải lại TOÀN BỘ file config", command=self._reload_config)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self._on_close)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="📖 Hướng dẫn", command=self._show_help)
        help_menu.add_command(label="ℹ️ Về", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    # ═══════════════════════════════════════════════════════════════════════
    #  STEP 1 — LỌC TỪ KHÓA
    # ═══════════════════════════════════════════════════════════════════════
    def _build_step1(self):
        self.step1 = ttk.LabelFrame(self.root, text="BƯỚC 1: LỌC TỪ KHÓA — Phân tích & Gợi ý Filter",
                                     padding=10)
        self.step1.pack(fill="x", padx=10, pady=(10, 5))

        # ── Row: File + Product Name ──────────────────────────────────────
        top = ttk.Frame(self.step1)
        top.pack(fill="x", pady=(0, 8))

        ttk.Label(top, text="📂 File Cerebro:").pack(side="left")
        self.file_var = tk.StringVar(value="")
        self.file_entry = ttk.Entry(top, textvariable=self.file_var, width=40)
        self.file_entry.pack(side="left", padx=5)
        ttk.Button(top, text="📂 Browse", command=self._browse_file).pack(side="left", padx=(0, 20))

        ttk.Label(top, text="🏷️ Tên SP:").pack(side="left")
        self.product_var = tk.StringVar()
        self.product_combo = ttk.Combobox(
            top, textvariable=self.product_var, width=42, font=("Arial", 10)
        )
        self.product_combo.pack(side="left", padx=5)
        self.product_combo.bind("<Return>", lambda e: self._analyze())
        self.product_combo.bind("<<ComboboxSelected>>", lambda e: self._analyze())
        self.analyze_btn = ttk.Button(top, text="🔍 Phân tích & Gợi ý",
                                       command=self._analyze)
        self.analyze_btn.pack(side="left")

        # ── Suggestions Treeview ──────────────────────────────────────────
        tree_frame = ttk.Frame(self.step1)
        tree_frame.pack(fill="both", expand=True, pady=(0, 5))

        columns = ("#", "pattern", "count", "rating")
        self.sugg_tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                       height=8, selectmode="browse")
        self.sugg_tree.heading("#", text="#", anchor="center")
        self.sugg_tree.heading("pattern", text="Filter Pattern")
        self.sugg_tree.heading("count", text="Kết quả", anchor="center")
        self.sugg_tree.heading("rating", text="Đánh giá", anchor="center")

        self.sugg_tree.column("#", width=40, anchor="center", stretch=False)
        self.sugg_tree.column("pattern", width=340)
        self.sugg_tree.column("count", width=80, anchor="center")
        self.sugg_tree.column("rating", width=130, anchor="center")

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.sugg_tree.yview)
        self.sugg_tree.configure(yscrollcommand=scroll.set)

        self.sugg_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.sugg_tree.bind("<<TreeviewSelect>>", self._on_suggestion_select)
        self.sugg_tree.bind("<Double-1>", lambda e: self._apply_filter())

        # ── Row: Lịch sử filter ───────────────────────────────────────────
        hist_frame = ttk.Frame(self.step1)
        hist_frame.pack(fill="x", pady=(8, 2))

        ttk.Label(hist_frame, text="📜 Lịch sử filter:").pack(side="left")
        self.history_var = tk.StringVar()
        self.history_combo = ttk.Combobox(
            hist_frame, textvariable=self.history_var,
            state="readonly", width=55, font=("Arial", 10)
        )
        self.history_combo.pack(side="left", padx=5)
        self.history_combo.bind("<<ComboboxSelected>>", self._on_history_select)
        ttk.Button(hist_frame, text="🗑 Xóa hết",
                   command=self._clear_history).pack(side="left", padx=5)

        # ── Row: Selected Filter + Combo + Custom ─────────────────────────
        sel_frame = ttk.Frame(self.step1)
        sel_frame.pack(fill="x", pady=(5, 0))

        ttk.Label(sel_frame, text="Filter đã chọn:").pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_entry = ttk.Entry(sel_frame, textvariable=self.filter_var, width=40)
        self.filter_entry.pack(side="left", padx=5)

        ttk.Label(sel_frame, text="Kết hợp:").pack(side="left", padx=(15, 3))
        self.combo_var = tk.StringVar()
        self.combo_entry = ttk.Entry(sel_frame, textvariable=self.combo_var, width=8)
        self.combo_entry.pack(side="left", padx=3)
        self.combo_entry.bind("<Return>", lambda e: self._apply_combo_filter())
        ttk.Button(sel_frame, text="+", width=3,
                   command=self._apply_combo_filter).pack(side="left", padx=(0, 15))

        ttk.Label(sel_frame, text="Tự nhập:").pack(side="left", padx=(5, 3))
        self.custom_var = tk.StringVar()
        self.custom_entry = ttk.Entry(sel_frame, textvariable=self.custom_var, width=22)
        self.custom_entry.pack(side="left", padx=3)
        self.custom_entry.bind("<Return>", lambda e: self._apply_custom_filter())

        self.apply_btn = ttk.Button(sel_frame, text="✅ Áp dụng filter →",
                                     style="Accent.TButton",
                                     command=self._apply_filter,
                                     state="disabled")
        self.apply_btn.pack(side="right", padx=(10, 0))

    # ═══════════════════════════════════════════════════════════════════════
    #  STEP 2 — LỌC DỮ LIỆU & XUẤT
    # ═══════════════════════════════════════════════════════════════════════
    def _build_step2(self):
        self.step2 = ttk.LabelFrame(self.root, text="BƯỚC 2: LỌC DỮ LIỆU & XUẤT FILE",
                                     padding=10)
        self.step2.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        # ── Result label + Color legend ────────────────────────────────────
        result_header = ttk.Frame(self.step2)
        result_header.pack(fill="x", pady=(0, 8))

        self.result_var = tk.StringVar(value="📊 Chưa có dữ liệu. Hoàn thành Bước 1 trước.")
        ttk.Label(result_header, textvariable=self.result_var,
                  font=("Arial", 11, "bold")).pack(side="left")

        # Legend frame (góc phải)
        legend_frame = tk.Frame(result_header, bg=COLORS["bg"])
        legend_frame.pack(side="right")

        legends = [
            ("#FFF2CC", "Brand đối thủ"),
        ]
        for i, (color, text) in enumerate(legends):
            tk.Frame(legend_frame, bg=color, width=14, height=14,
                     relief="solid", bd=1).pack(side="left", padx=(8 if i > 0 else 0, 3))
            tk.Label(legend_frame, text=text, font=("Arial", 8),
                     bg=COLORS["bg"], fg="#555555").pack(side="left")

        # ── Price & Amazon Fee inputs (cho tính toán realtime) ──────────
        price_frame = ttk.Frame(self.step2)
        price_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(price_frame, text="💰 Price ($):").pack(side="left")
        self.price_entry = ttk.Entry(price_frame, textvariable=self.price_var, width=10)
        self.price_entry.pack(side="left", padx=(2, 20))
        self.price_var.trace_add("write", lambda *_: self._on_price_change())

        ttk.Label(price_frame, text="📦 Amazon Fee ($):").pack(side="left")
        self.amazon_fee_entry = ttk.Entry(price_frame, textvariable=self.amazon_fee_var, width=10)
        self.amazon_fee_entry.pack(side="left", padx=(2, 0))
        self.amazon_fee_var.trace_add("write", lambda *_: self._on_price_change())

        # ── Preview Treeview ──────────────────────────────────────────────
        prev_frame = ttk.Frame(self.step2)
        prev_frame.pack(fill="both", expand=True)

        prev_cols = [col[0] for col in FULL_EXPORT_COLS]
        self.prev_tree = ttk.Treeview(prev_frame, columns=prev_cols, show="headings",
                                       height=10, selectmode="browse")
        # Column widths: hẹp hơn cho 20 cột
        col_widths = {
            "Keyword Phrase": 200, "Search Volume": 70, "Sponsored ASINs": 80,
            "Competing Products": 90, "CPR": 50, "Bid": 60,
            "CTR": 50, "Clicks": 50, "Spend": 65, "CVR": 50,
            "Ads Orders": 70, "Price": 60, "Ads Revenue": 75,
            "ACOS": 55, "Total Orders": 70, "Total Revenue": 80,
            "Product Fee": 70, "Amazon Fee": 70, "Total Fee": 75,
            "Profit": 65,
        }
        for c in prev_cols:
            self.prev_tree.heading(c, text=c)
            anchor = "w" if c == "Keyword Phrase" else "center"
            self.prev_tree.column(c, width=col_widths.get(c, 70), anchor=anchor, minwidth=40)

        prev_scroll_y = ttk.Scrollbar(prev_frame, orient="vertical", command=self.prev_tree.yview)
        prev_scroll_x = ttk.Scrollbar(prev_frame, orient="horizontal", command=self.prev_tree.xview)
        self.prev_tree.configure(yscrollcommand=prev_scroll_y.set, xscrollcommand=prev_scroll_x.set)

        self.prev_tree.grid(row=0, column=0, sticky="nsew")
        prev_scroll_y.grid(row=0, column=1, sticky="ns")
        prev_scroll_x.grid(row=1, column=0, sticky="ew")
        prev_frame.grid_rowconfigure(0, weight=1)
        prev_frame.grid_columnconfigure(0, weight=1)

        # Tags cho brand highlight
        self.prev_tree.tag_configure("brand", background=COLORS["brand_warn"])
        self.prev_tree.tag_configure("alt", background=COLORS["row_alt"])

        # ── Right-click context menu: Copy / Xóa ───────────────────────────
        self.prev_menu = tk.Menu(self.prev_tree, tearoff=0)
        self.prev_menu.add_command(label="📋 Copy", command=self._copy_cell)
        self.prev_menu.add_command(label="📋 Copy cả dòng", command=self._copy_row)
        self.prev_menu.add_separator()
        self.prev_menu.add_command(label="🗑 Xóa dòng (Delete)", command=self._delete_selected)

        # Left-click: chọn từng ô (cell)
        self.prev_tree.bind("<Button-1>", self._on_cell_click)
        # <<TreeviewSelect>>: bắt mọi thay đổi selection (click, ↑↓, tab...)
        self.prev_tree.bind("<<TreeviewSelect>>", self._on_selection_change)
        # Right-click: context menu
        self.prev_tree.bind("<Button-2>" if sys.platform == "darwin" else "<Button-3>",
                            self._on_tree_right_click)
        self.prev_tree.bind("<Control-c>", lambda e: self._copy_cell())
        self.prev_tree.bind("<Command-c>", lambda e: self._copy_cell())
        self.prev_tree.bind("<Delete>", lambda e: self._delete_selected())
        self.prev_tree.bind("<BackSpace>", lambda e: self._delete_selected())
        # Undo
        self.root.bind("<Command-z>", lambda e: self._undo_delete())
        self.root.bind("<Control-z>", lambda e: self._undo_delete())

        # ── Negative Keywords ─────────────────────────────────────────────
        neg_frame = ttk.Frame(self.step2)
        neg_frame.pack(fill="x", pady=(10, 5))

        ttk.Label(neg_frame, text="⚠️ Negative Keywords:").pack(side="left")
        self.neg_var = tk.StringVar()
        self.neg_entry = ttk.Entry(neg_frame, textvariable=self.neg_var, width=25)
        self.neg_entry.pack(side="left", padx=5)
        self.neg_entry.bind("<Return>", lambda e: self._add_negative())
        ttk.Button(neg_frame, text="Thêm", command=self._add_negative).pack(side="left")

        self.neg_listbox = tk.Listbox(neg_frame, height=3, width=35, font=("Arial", 9))
        self.neg_listbox.pack(side="left", padx=(15, 5), fill="x", expand=True)
        self.neg_scroll = ttk.Scrollbar(neg_frame, orient="vertical", command=self.neg_listbox.yview)
        self.neg_listbox.configure(yscrollcommand=self.neg_scroll.set)
        self.neg_scroll.pack(side="left", fill="y")

        # Nút Sửa + Xóa
        neg_btn_frame = ttk.Frame(neg_frame)
        neg_btn_frame.pack(side="left", padx=5)
        ttk.Button(neg_btn_frame, text="✏️ Sửa", command=self._edit_negative).pack(side="top", fill="x", pady=(0, 2))
        ttk.Button(neg_btn_frame, text="✕ Xóa", command=self._remove_negative).pack(side="top", fill="x")

        # Double-click để sửa
        self.neg_listbox.bind("<Double-1>", lambda e: self._edit_negative())

        # ── Buttons ───────────────────────────────────────────────────────
        btn_frame = ttk.Frame(self.step2)
        btn_frame.pack(fill="x", pady=(10, 0))

        self.fillbid_btn = ttk.Button(btn_frame, text="💰 Fill Bid thiếu",
                                       command=self._fill_bids_preview,
                                       state="disabled")
        self.fillbid_btn.pack(side="left")

        self.export_btn = ttk.Button(btn_frame, text="📤 Xuất file Excel",
                                      style="Accent.TButton",
                                      command=self._export,
                                      state="disabled")
        self.export_btn.pack(side="right")

        # Flag: đã fill bid chưa
        self._bid_filled = False

        # Initially disable step2
        self._set_step2_state("disabled")

    # ═══════════════════════════════════════════════════════════════════════
    #  STATUSBAR
    # ═══════════════════════════════════════════════════════════════════════
    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="✅ Sẵn sàng. Chọn file Cerebro để bắt đầu.")
        status = ttk.Frame(self.root, relief="sunken", borderwidth=1)
        status.pack(fill="x", side="bottom")
        ttk.Label(status, textvariable=self.status_var, font=("Arial", 9),
                  padding=(8, 3)).pack(fill="x")

    # ═══════════════════════════════════════════════════════════════════════
    #  AUTO-LOAD
    # ═══════════════════════════════════════════════════════════════════════
    def _reload_all_config(self):
        """Đọc lại TOÀN BỘ dữ liệu từ file txt (brands, negatives, rivals, history, product names)."""
        # Brands
        self.state.brands = self.engine.load_brands()

        # Negative keywords
        self.state.negative_kws = self.engine.load_negative_keywords()
        self.neg_listbox.delete(0, "end")
        for kw in self.state.negative_kws:
            self.neg_listbox.insert("end", kw)

        # Rival companies
        self._rival_companies = self.engine.load_rival_companies()

        # Lịch sử filter
        self._refresh_history_dropdown()

        # Lịch sử tên SP
        product_names = self.engine.load_product_names()
        if product_names:
            self.product_combo["values"] = product_names
        else:
            self.product_combo["values"] = []

    def _auto_load(self):
        # Thử load input/input.xlsx
        default = os.path.join(INPUT_DIR, INPUT_FILES["cerebro"])
        if os.path.exists(default):
            self._load_file(default)
        else:
            # Vẫn load config dù không có file xlsx mặc định
            self._reload_all_config()
            self._set_status("✅ Sẵn sàng. Chọn file Cerebro để bắt đầu.")

    # ═══════════════════════════════════════════════════════════════════════
    #  ACTIONS
    # ═══════════════════════════════════════════════════════════════════════

    # ── File ──────────────────────────────────────────────────────────────
    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Chọn file Helium 10 Cerebro export",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        if path:
            self._load_file(path)

    def _load_file(self, path: str):
        try:
            self.state.df_raw = self.engine.load_cerebro(path)
            self.state.input_file = path
            self.state.total_count = len(self.state.df_raw)
            self.file_var.set(path)

            # Reset Step 2 khi load file mới
            self.state.df_filtered = None
            self.state.selected_filter = None
            self._undo_stack.clear()
            self._bid_filled = False
            self.fillbid_btn.config(text="💰 Fill Bid thiếu", state="disabled")
            self.export_btn.config(state="disabled")
            self.apply_btn.config(state="disabled")
            self.result_var.set("📊 Chưa có dữ liệu. Hoàn thành Bước 1 trước.")
            self.price_var.set("")
            self.amazon_fee_var.set("")
            self.prev_tree.delete(*self.prev_tree.get_children())
            self._set_step2_state("disabled")

            # Đọc lại TOÀN BỘ config từ file txt (brands, negatives, rivals, history, product names)
            self._reload_all_config()

            self._set_status(f"✅ Đã load {self.state.total_count} từ khóa từ {os.path.basename(path)} — Config đã được refresh")
        except Exception as e:
            messagebox.showerror("Lỗi load file", str(e))
            self._set_status(f"❌ Lỗi: {e}")

    def _open_output_dir(self, path: str | None = None):
        """Mở thư mục bằng Finder/file manager."""
        target = path if path else os.path.abspath(OUTPUT_DIR)
        os.makedirs(target, exist_ok=True)
        webbrowser.open(f"file://{target}")

    def _open_output_dir_at(self, path: str):
        """Mở thư mục chỉ định (dùng sau khi export)."""
        self._open_output_dir(path)

    def _reload_config(self):
        """Tải lại toàn bộ file config: SYNONYMS, STOP_WORDS, brands, negatives, rivals, history, product names."""
        self.syn_engine.reload_config()
        self._reload_all_config()
        self._set_status("✅ Đã tải lại TOÀN BỘ file config (SYNONYMS, STOP_WORDS, brands, negatives, rivals, history, product names)")

    # ── Analyze ───────────────────────────────────────────────────────────
    def _analyze(self):
        if self.state.df_raw is None:
            messagebox.showwarning("Chưa có dữ liệu", "Vui lòng chọn file Cerebro trước.")
            return

        product_name = self.product_var.get().strip()
        if not product_name:
            messagebox.showwarning("Thiếu tên SP", "Vui lòng nhập tên sản phẩm.")
            return

        self.state.product_name = product_name
        self.engine.save_product_name(product_name)  # lưu vào input/product_name.txt
        self._set_status(f"🔍 Đang phân tích '{product_name}'...")

        def _run():
            terms = self.syn_engine.extract_terms(product_name)
            suggestions = self.syn_engine.build_suggestions(self.state.df_raw, terms)

            def _update():
                self.state.suggestions = suggestions
                self._populate_suggestions(suggestions)
                self._set_status(
                    f"✅ Phân tích xong: {len(suggestions)} gợi ý từ {len(terms)} từ khóa"
                )
            self.root.after(0, _update)

        threading.Thread(target=_run, daemon=True).start()

    def _populate_suggestions(self, suggestions: list[FilterSuggestion]):
        self.sugg_tree.delete(*self.sugg_tree.get_children())
        total = self.state.total_count
        for i, s in enumerate(suggestions, 1):
            pct = round(s.count / total * 100, 1) if total else 0
            tag = s.rating.split()[0] if s.rating else ""
            self.sugg_tree.insert("", "end", iid=str(i),
                                  values=(i, s.pattern, f"{s.count} ({pct}%)", s.rating),
                                  tags=(tag,))

        # Color tags
        self.sugg_tree.tag_configure("✅", foreground=COLORS["success"])
        self.sugg_tree.tag_configure("🟡", foreground="#B8860B")
        self.sugg_tree.tag_configure("🔴", foreground="#CC0000")
        self.sugg_tree.tag_configure("⚪", foreground="#999999")

    def _on_suggestion_select(self, event):
        sel = self.sugg_tree.selection()
        if sel:
            item = self.sugg_tree.item(sel[0])
            pattern = item["values"][1]
            self.filter_var.set(pattern)
            self.apply_btn.config(state="normal")

    # ── Filter Selection ──────────────────────────────────────────────────
    def _apply_combo_filter(self):
        combo = self.combo_var.get().strip()
        if not combo or not self.state.suggestions:
            return
        try:
            indices = [int(x.strip()) - 1 for x in combo.split("+")]
            patterns = []
            for i in indices:
                if 0 <= i < len(self.state.suggestions):
                    patterns.append(self.state.suggestions[i].pattern)
            if patterns:
                combined = "|".join(patterns)
                self.filter_var.set(combined)
                self.apply_btn.config(state="normal")
                self._set_status(f"🔗 Đã kết hợp {len(patterns)} filter: {combined}")
        except (ValueError, IndexError):
            self._set_status("⚠️ Format không hợp lệ. VD: 1+3")

    def _apply_custom_filter(self):
        custom = self.custom_var.get().strip()
        if custom:
            self.filter_var.set(custom)
            self.apply_btn.config(state="normal")

    # ── Lịch sử filter ────────────────────────────────────────────────────
    def _on_history_select(self, event):
        """Khi user chọn 1 filter từ lịch sử → điền vào filter field + enable apply."""
        selected = self.history_var.get()
        if not selected:
            return
        # Format: "pattern  |  46 kết quả" → tách lấy pattern
        if "  |  " in selected:
            pattern = selected.split("  |  ")[0].strip()
        else:
            pattern = selected.strip()
        self.filter_var.set(pattern)
        self.apply_btn.config(state="normal")
        self._set_status(f"📜 Đã chọn filter từ lịch sử: {pattern}")

    def _clear_history(self):
        """Xóa toàn bộ lịch sử filter."""
        if not messagebox.askyesno("Xác nhận", "Xóa toàn bộ lịch sử filter?"):
            return
        # Xóa file
        path = os.path.join(INPUT_DIR, INPUT_FILES["filters"])
        if os.path.exists(path):
            open(path, "w").close()
        # Xóa dropdown
        self.history_combo["values"] = []
        self.history_var.set("")
        self._set_status("🗑 Đã xóa toàn bộ lịch sử filter")

    def _refresh_history_dropdown(self):
        """Nạp lại danh sách filter từ filters.txt vào dropdown."""
        history = self.engine.load_filters_history()
        if not history:
            self.history_combo["values"] = ["(chưa có lịch sử)"]
            return

        # Đếm matches với dữ liệu hiện tại (nếu có)
        items = []
        for pattern in history:
            if self.state.df_raw is not None:
                cnt = self.engine.count_matches(self.state.df_raw, pattern)
                items.append(f"{pattern}  |  {cnt} kết quả")
            else:
                items.append(pattern)
        self.history_combo["values"] = items
        if items:
            self.history_combo.current(0)  # chọn item đầu tiên làm default

    # ── Apply Filter → Step 2 ─────────────────────────────────────────────
    def _apply_filter(self):
        self._undo_stack.clear()  # clear undo khi áp dụng filter mới
        pattern = self.filter_var.get().strip()
        if not pattern:
            messagebox.showwarning("Chưa chọn filter", "Vui lòng chọn hoặc nhập filter pattern.")
            return
        if self.state.df_raw is None:
            return

        self.state.selected_filter = pattern
        self.state.df_filtered = self.engine.apply_filter(self.state.df_raw, pattern)

        # ── Tự động loại bỏ từ khóa chứa tên công ty đối thủ ──────────────
        rival_removed_count = 0
        self._rival_removed_df = None
        if self._rival_companies:
            self.state.df_filtered, self._rival_removed_df = \
                self.engine.remove_rival_keywords(self.state.df_filtered, self._rival_companies)
            rival_removed_count = len(self._rival_removed_df)

        cnt = len(self.state.df_filtered)

        # Lưu lịch sử filter + refresh dropdown
        self.engine.save_filter_to_history(pattern)
        self._refresh_history_dropdown()

        # Populate preview
        self._populate_preview(self.state.df_filtered)

        pct = round(cnt / self.state.total_count * 100, 1) if self.state.total_count else 0
        result_text = f"📊 Kết quả lọc: {cnt} từ khóa / {self.state.total_count} tổng ({pct}%) — Filter: '{pattern}'"
        if rival_removed_count > 0:
            result_text += f"  |  🚫 {rival_removed_count} từ khóa đối thủ đã bị loại"
        self.result_var.set(result_text)

        self._bid_filled = False
        self._set_step2_state("normal")
        self.export_btn.config(state="normal")
        self.fillbid_btn.config(state="normal")

        status = f"✅ Đã lọc: {cnt} kết quả với filter '{pattern}'"
        if rival_removed_count > 0:
            status += f" | 🚫 Tự động loại {rival_removed_count} từ khóa đối thủ"
        self._set_status(status)

    # ── Tính toán 1 dòng 20 cột ─────────────────────────────────────────
    def _compute_row(self, row: pd.Series, price: float, amazon_fee: float,
                     src_cols: list) -> list:
        """
        Tính 20 giá trị hiển thị cho 1 dòng từ dữ liệu Cerebro thô.
        Công thức giống hệt file mẫu AGlobal:
          H (Clicks)       = CTR * SearchVolume     (G * B)
          I (Spend)        = Bid * Clicks            (F * H)
          K (Ads Orders)   = Clicks * CVR            (H * J)
          M (Ads Revenue)  = Ads Orders * Price      (K * L)
          N (ACOS)         = Spend / Ads Revenue     (I / M)
          O (Total Orders) = Ads Orders + AdsOrders/4 (K + K/4)
          P (Total Revenue)= Price * Total Orders    (L * O)
          Q (Product Fee)  = Price / 3               (L / 3)
          S (Total Fee)    = (AmazonFee+ProductFee)*TotalOrders + Spend
          T (Profit)       = Total Revenue - Total Fee
        """
        CTR = 0.01
        CVR = 0.05

        # ── Lấy raw data ──────────────────────────────────────────────
        def _get_str(col_name):
            """Lấy giá trị string (cho Keyword Phrase)."""
            if col_name and col_name in row.index:
                v = row[col_name]
                return str(v) if pd.notna(v) and v != "" else ""
            return ""

        def _get_num(col_name):
            """Lấy giá trị số (cho các cột numeric)."""
            if col_name and col_name in row.index:
                v = row[col_name]
                try:
                    return float(v) if pd.notna(v) and v != "" else 0.0
                except (ValueError, TypeError):
                    return 0.0
            return 0.0

        kw          = _get_str(src_cols[0])  # Keyword Phrase
        search_vol  = _get_num(src_cols[1])  # Search Volume
        sponsored   = _get_num(src_cols[2])  # Sponsored ASINs
        competing   = _get_num(src_cols[3])  # Competing Products
        cpr         = _get_num(src_cols[4])  # CPR
        bid         = _get_num(src_cols[5])  # Bid

        # ── Computed ─────────────────────────────────────────────────
        clicks       = CTR * search_vol
        spend        = bid * clicks
        ads_orders   = clicks * CVR
        ads_revenue  = ads_orders * price
        acos         = spend / ads_revenue if ads_revenue != 0 else 0
        total_orders = ads_orders + ads_orders / 4
        total_revenue = price * total_orders
        product_fee  = price / 3
        total_fee    = (amazon_fee + product_fee) * total_orders + spend
        profit       = total_revenue - total_fee

        return [
            kw,                                    # A: Keyword Phrase
            int(search_vol) if search_vol else "", # B: Search Volume
            int(sponsored) if sponsored else "",   # C: Sponsored ASINs
            int(competing) if competing else "",   # D: Competing Products
            int(cpr) if cpr else "",               # E: CPR
            f"${bid:,.2f}" if bid else "",         # F: Bid
            f"{CTR:.2%}",                          # G: CTR
            int(round(clicks)),                    # H: Clicks
            f"${spend:,.2f}",                      # I: Spend
            f"{CVR:.1%}",                          # J: CVR
            int(round(ads_orders)),                # K: Ads Orders
            f"${price:,.2f}" if price else "",     # L: Price
            f"${ads_revenue:,.2f}",                # M: Ads Revenue
            f"{acos:.2%}",                         # N: ACOS
            int(round(total_orders)),              # O: Total Orders
            f"${total_revenue:,.2f}",              # P: Total Revenue
            f"${product_fee:,.2f}",                # Q: Product Fee
            f"${amazon_fee:,.2f}" if amazon_fee else "", # R: Amazon Fee
            f"${total_fee:,.2f}",                  # S: Total Fee
            f"${profit:,.2f}",                     # T: Profit
        ]

    def _on_price_change(self):
        """Khi Price hoặc Amazon Fee thay đổi → refresh preview."""
        if self.state.df_filtered is not None and len(self.state.df_filtered) > 0:
            self._populate_preview(self.state.df_filtered)

    def _populate_preview(self, df: pd.DataFrame, brands: list[str] | None = None):
        self.prev_tree.delete(*self.prev_tree.get_children())
        if brands is None:
            brands = self.state.brands

        # ── Lấy Price & Amazon Fee từ UI ──────────────────────────────
        try:
            price = float(self.price_var.get() or 0)
        except ValueError:
            price = 0.0
        try:
            amazon_fee = float(self.amazon_fee_var.get() or 0)
        except ValueError:
            amazon_fee = 0.0

        # Source columns cho 6 cột Cerebro gốc
        src_cols = [col[1] for col in FULL_EXPORT_COLS]

        for ri, (_, row) in enumerate(df.iterrows()):
            values = self._compute_row(row, price, amazon_fee, src_cols)

            # Check brand
            kw_val = str(values[0]).lower() if values[0] else ""
            is_brand = any(b.lower() in kw_val for b in brands)
            is_alt = (ri % 2 == 1)

            tag = "brand" if is_brand else ("alt" if is_alt else "")
            self.prev_tree.insert("", "end", values=values, tags=(tag,) if tag else ())

    # ── Cell click / Copy / Delete ───────────────────────────────────────
    def _on_cell_click(self, event):
        """Left-click: chọn dòng + ghi nhận ô được click để hiển thị trên status bar."""
        item = self.prev_tree.identify_row(event.y)
        col = self.prev_tree.identify_column(event.x)
        if not item or not col:
            return
        # selectmode="browse" tự highlight dòng, ta chỉ cần track ô
        self._clicked_item = item
        self._clicked_col = col

        col_idx = int(col.replace("#", "")) - 1
        col_names = [c[0] for c in FULL_EXPORT_COLS]
        col_name = col_names[col_idx] if col_idx < len(col_names) else f"Cột {col_idx+1}"
        values = self.prev_tree.item(item, "values")
        val = str(values[col_idx]) if col_idx < len(values) and values[col_idx] is not None else "(rỗng)"
        self._set_status(f"📍 [{col_name}] = {val[:100]}{'...' if len(val) > 100 else ''}  |  ↑↓ chọn dòng | Delete xóa | Chuột phải → Copy")

    def _on_selection_change(self, event):
        """Bắt sự kiện khi selection thay đổi (↑↓, click, tab...)."""
        sel = self.prev_tree.selection()
        if not sel:
            return
        item = sel[0]
        # Giữ col cũ nếu có, không thì mặc định cột 1
        col = getattr(self, "_clicked_col", "#1") or "#1"
        self._clicked_item = item
        self._clicked_col = col

        all_items = self.prev_tree.get_children()
        idx = list(all_items).index(item) + 1 if item in all_items else 0
        values = self.prev_tree.item(item, "values")
        kw = str(values[0]) if values and values[0] is not None else "(rỗng)"
        self._set_status(f"📍 Dòng {idx}/{len(all_items)}: {kw[:100]}{'...' if len(kw) > 100 else ''}  |  ↑↓ chọn | Delete xóa")

    def _on_tree_right_click(self, event):
        """Hiển thị context menu tại vị trí click chuột phải."""
        item = self.prev_tree.identify_row(event.y)
        col = self.prev_tree.identify_column(event.x)
        if item and col:
            self._clicked_item = item
            self._clicked_col = col
            try:
                self.prev_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.prev_menu.grab_release()

    def _copy_cell(self):
        """Copy giá trị ô đang được chọn vào clipboard."""
        item = getattr(self, "_clicked_item", None)
        col = getattr(self, "_clicked_col", None)
        if not item or not col:
            self._set_status("⚠️ Chưa chọn ô nào. Click vào 1 ô trước.")
            return
        col_idx = int(col.replace("#", "")) - 1
        values = self.prev_tree.item(item, "values")
        if col_idx < len(values):
            val = str(values[col_idx]) if values[col_idx] is not None else ""
            self.root.clipboard_clear()
            self.root.clipboard_append(val)
            self._set_status(f"📋 Đã copy: {val[:80]}{'...' if len(val) > 80 else ''}")

    def _copy_row(self):
        """Copy toàn bộ dòng vào clipboard (tab-separated)."""
        item = getattr(self, "_clicked_item", None)
        if not item:
            self._set_status("⚠️ Chưa chọn dòng nào. Click vào 1 ô trước.")
            return
        values = self.prev_tree.item(item, "values")
        line = "\t".join(str(v) if v is not None else "" for v in values)
        self.root.clipboard_clear()
        self.root.clipboard_append(line)
        self._set_status(f"📋 Đã copy cả dòng ({len(values)} cột)")

    def _delete_selected(self):
        """Xóa dòng chứa ô đang chọn khỏi preview + df_filtered (có undo)."""
        item = getattr(self, "_clicked_item", None)
        if not item:
            self._set_status("⚠️ Chưa chọn dòng nào. Click vào 1 ô trước.")
            return

        # Lưu index của item trong tree
        all_items = self.prev_tree.get_children()
        idx = all_items.index(item)

        # ── Lưu raw data từ df_filtered để undo ───────────────────────
        src_cols = [col[1] for col in FULL_EXPORT_COLS if col[1] is not None]
        if self.state.df_filtered is not None and idx < len(self.state.df_filtered):
            raw_row = self.state.df_filtered.iloc[idx].to_dict()
            # Chỉ lưu các cột source
            row_data = {c: raw_row.get(c) for c in src_cols if c in raw_row}
        else:
            row_data = {}

        self._undo_stack.append({
            "row_data": row_data,
            "index": idx,
        })

        # ── Kiểm tra nếu là dòng brand (vàng) → thêm vào rival_company.txt ─
        values = self.prev_tree.item(item, "values")
        kw = str(values[0]).lower() if values else ""
        matched_brands = [b for b in self.state.brands if b.lower() in kw]
        if matched_brands:
            for b in matched_brands:
                self.engine.save_rival_company(b)
            self._rival_companies = self.engine.load_rival_companies()

        # Xóa khỏi df_filtered
        if self.state.df_filtered is not None:
            self.state.df_filtered = self.state.df_filtered.drop(
                self.state.df_filtered.index[idx]
            ).reset_index(drop=True)

        # ── Repopulate toàn bộ preview ────────────────────────────────
        self._populate_preview(self.state.df_filtered)

        # ── Giữ cursor ở đúng vị trí ──────────────────────────────────
        remaining = self.prev_tree.get_children()
        if remaining:
            new_idx = min(idx, len(remaining) - 1)
            new_item = remaining[new_idx]
            self._clicked_item = new_item
            self._clicked_col = "#1"
            self.prev_tree.selection_set(new_item)
            self.prev_tree.focus(new_item)
            self.prev_tree.see(new_item)
        else:
            self._clicked_item = None
            self._clicked_col = None

        cnt = len(self.state.df_filtered) if self.state.df_filtered is not None else 0
        status = f"🗑 Đã xóa 1 dòng. Còn {cnt} dòng. ⌘Z / Ctrl+Z để undo ({len(self._undo_stack)} lần)"
        if matched_brands:
            status += f" | 🚫 Đã thêm '{', '.join(matched_brands)}' vào rival_company.txt"
        self._set_status(status)
        # Cập nhật result label
        pct = round(cnt / self.state.total_count * 100, 1) if self.state.total_count else 0
        self.result_var.set(
            f"📊 Kết quả lọc: {cnt} từ khóa / {self.state.total_count} tổng ({pct}%) "
            f"— Đã xóa {len(self._undo_stack)} dòng"
        )

    def _undo_delete(self):
        """Hoàn tác lần xóa gần nhất."""
        if not self._undo_stack:
            self._set_status("ⓘ Không có gì để undo")
            return

        entry = self._undo_stack.pop()
        row_data = entry["row_data"]
        idx = entry["index"]

        # Khôi phục vào df_filtered
        if self.state.df_filtered is not None and row_data:
            import pandas as pd
            restore_df = pd.DataFrame([row_data])
            if idx >= len(self.state.df_filtered):
                self.state.df_filtered = pd.concat(
                    [self.state.df_filtered, restore_df], ignore_index=True
                )
            else:
                top = self.state.df_filtered.iloc[:idx]
                bottom = self.state.df_filtered.iloc[idx:]
                self.state.df_filtered = pd.concat(
                    [top, restore_df, bottom], ignore_index=True
                )

        # ── Repopulate preview ────────────────────────────────────────
        self._populate_preview(self.state.df_filtered)

        # ── Đưa cursor về dòng vừa khôi phục ──────────────────────────
        all_items = self.prev_tree.get_children()
        restored_item = all_items[idx] if idx < len(all_items) else all_items[-1]
        self._clicked_item = restored_item
        self._clicked_col = "#1"
        self.prev_tree.selection_set(restored_item)
        self.prev_tree.focus(restored_item)
        self.prev_tree.see(restored_item)

        cnt = len(self.state.df_filtered) if self.state.df_filtered is not None else 0
        self._set_status(
            f"↩ Đã undo. Còn {cnt} dòng. "
            f"{len(self._undo_stack)} lần undo nữa"
        )

    # ── Negative Keywords ─────────────────────────────────────────────────
    def _save_negatives_to_file(self):
        """Ghi danh sách negative keywords vào input/keywords.txt."""
        self.engine.save_negative_keywords(self.state.negative_kws)

    def _add_negative(self):
        kw = self.neg_var.get().strip()
        if not kw:
            return
        # Không thêm trùng
        existing_lower = [k.lower() for k in self.state.negative_kws]
        if kw.lower() in existing_lower:
            self._set_status(f"⚠️ '{kw}' đã có trong danh sách negative keywords.")
            self.neg_var.set("")
            return
        self.state.negative_kws.append(kw)
        self.neg_listbox.insert("end", kw)
        self._save_negatives_to_file()
        self._apply_negatives()
        self.neg_var.set("")
        self._set_status(f"✅ Đã thêm negative keyword: '{kw}' — đã lưu vào keywords.txt")

    def _edit_negative(self):
        """Sửa negative keyword đang được chọn."""
        sel = self.neg_listbox.curselection()
        if not sel:
            self._set_status("⚠️ Chọn 1 negative keyword trong danh sách để sửa.")
            return
        idx = sel[0]
        old_kw = self.neg_listbox.get(idx)

        # Popup dialog nhập giá trị mới
        dialog = tk.Toplevel(self.root)
        dialog.title("✏️ Sửa Negative Keyword")
        dialog.geometry("380x130")
        dialog.configure(bg=COLORS["bg"])
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text=f"Sửa negative keyword:", font=("Arial", 10)).pack(pady=(15, 5))
        new_var = tk.StringVar(value=old_kw)
        new_entry = ttk.Entry(dialog, textvariable=new_var, width=40, font=("Arial", 10))
        new_entry.pack(padx=20, pady=5)
        new_entry.select_range(0, "end")
        new_entry.focus_set()

        def _do_edit():
            new_kw = new_var.get().strip()
            if not new_kw:
                return
            if new_kw == old_kw:
                dialog.destroy()
                return
            # Check trùng (trừ chính nó)
            existing = [k for k in self.state.negative_kws if k != old_kw]
            if new_kw.lower() in [k.lower() for k in existing]:
                self._set_status(f"⚠️ '{new_kw}' đã có trong danh sách.")
                dialog.destroy()
                return
            # Cập nhật
            old_idx_in_state = self.state.negative_kws.index(old_kw)
            self.state.negative_kws[old_idx_in_state] = new_kw
            self.neg_listbox.delete(idx)
            self.neg_listbox.insert(idx, new_kw)
            self.neg_listbox.selection_set(idx)
            self._save_negatives_to_file()
            self._apply_negatives()
            self._set_status(f"✅ Đã sửa '{old_kw}' → '{new_kw}' — đã lưu vào keywords.txt")
            dialog.destroy()

        new_entry.bind("<Return>", lambda e: _do_edit())
        ttk.Button(dialog, text="✅ Lưu", command=_do_edit).pack(pady=8)

    def _remove_negative(self):
        sel = self.neg_listbox.curselection()
        if not sel:
            self._set_status("⚠️ Chọn ít nhất 1 negative keyword để xóa.")
            return
        removed_list = []
        for i in reversed(sel):
            removed = self.neg_listbox.get(i)
            self.state.negative_kws.remove(removed)
            self.neg_listbox.delete(i)
            removed_list.append(removed)
        self._save_negatives_to_file()
        self._apply_negatives()
        self._set_status(f"🗑 Đã xóa {len(removed_list)} negative keyword: {', '.join(removed_list)} — đã lưu vào keywords.txt")

    def _apply_negatives(self):
        self._undo_stack.clear()  # clear undo khi filter thay đổi
        if self.state.df_filtered is None:
            return
        if self.state.negative_kws:
            self.state.df_filtered = self.engine.remove_negative_keywords(
                self.state.df_filtered, self.state.negative_kws
            )
        else:
            # Re-apply original filter
            self.state.df_filtered = self.engine.apply_filter(
                self.state.df_raw, self.state.selected_filter
            )
        self._populate_preview(self.state.df_filtered)
        cnt = len(self.state.df_filtered)
        pct = round(cnt / self.state.total_count * 100, 1) if self.state.total_count else 0
        self.result_var.set(
            f"📊 Kết quả lọc: {cnt} từ khóa / {self.state.total_count} tổng ({pct}%) "
            f"— Negative: {len(self.state.negative_kws)} từ"
        )

    # ── Fill Bid Preview ──────────────────────────────────────────────────
    def _fill_bids_preview(self):
        """Điền Bid thiếu trong preview để user kiểm tra trước khi export."""
        if self.state.df_filtered is None or len(self.state.df_filtered) == 0:
            return
        if self._bid_filled:
            messagebox.showinfo("Đã fill rồi", "Bid thiếu đã được điền. Kiểm tra trong bảng preview.")
            return

        df_filled, count, avg = self.engine.fill_missing_bids(self.state.df_filtered)
        if count == 0:
            messagebox.showinfo("Không có Bid thiếu", "Tất cả từ khóa đều đã có Bid.")
            return

        self.state.df_filtered = df_filled
        self._bid_filled = True
        self.fillbid_btn.config(text="✅ Đã fill Bid", state="disabled")

        # Refresh preview
        self._populate_preview(self.state.df_filtered)

        # Update result label
        cnt = len(self.state.df_filtered)
        pct = round(cnt / self.state.total_count * 100, 1) if self.state.total_count else 0
        self.result_var.set(
            f"📊 Kết quả lọc: {cnt} từ khóa / {self.state.total_count} tổng ({pct}%) "
            f"| 💰 {count} Bid thiếu → ${avg:.2f}"
        )
        self._set_status(
            f"💰 Đã điền {count} Bid thiếu bằng trung bình ${avg:.2f}. "
            f"Xem cột Bid trong bảng để kiểm tra."
        )

    # ── Export ─────────────────────────────────────────────────────────────
    def _export(self):
        self._undo_stack.clear()  # clear undo khi đã export
        if self.state.df_filtered is None or len(self.state.df_filtered) == 0:
            messagebox.showwarning("Không có dữ liệu", "Không có từ khóa nào để xuất.")
            return

        # Điền Bid thiếu bằng trung bình (nếu chưa fill ở preview)
        if self._bid_filled:
            df_to_export = self.state.df_filtered
            filled_count, avg_bid = 0, 0.0
        else:
            df_to_export, filled_count, avg_bid = self.engine.fill_missing_bids(
                self.state.df_filtered
            )

        # ── Mở Finder dialog để chọn nơi lưu ───────────────────────────
        default_name = self.writer.format_output_name()
        default_dir = os.path.abspath(OUTPUT_DIR)
        os.makedirs(default_dir, exist_ok=True)
        initial_path = os.path.join(default_dir, default_name)

        file_path = filedialog.asksaveasfilename(
            title="Lưu file Excel",
            initialdir=default_dir,
            initialfile=default_name,
            defaultextension=".xlsx",
            filetypes=[
                ("Excel files", "*.xlsx"),
                ("All files", "*.*"),
            ],
        )
        if not file_path:
            self._set_status("ⓘ Đã hủy xuất file.")
            return

        try:
            # Lấy Price & Amazon Fee từ UI để điền vào file Excel
            try:
                price_val = float(self.price_var.get())
            except (ValueError, TypeError):
                price_val = None
            try:
                af_val = float(self.amazon_fee_var.get())
            except (ValueError, TypeError):
                af_val = None

            out_path, brands_found = self.writer.export_full(
                df_to_export, file_path, self.state.brands,
                price=price_val, amazon_fee=af_val,
            )
            cnt = len(df_to_export)
            msg = f"✅ Xuất thành công!\n\n📁 File: {os.path.basename(out_path)}\n📊 {cnt} từ khóa, 20 cột (có công thức Excel)"
            if filled_count > 0:
                msg += f"\n💰 Đã điền Bid thiếu: {filled_count} dòng ← trung bình ${avg_bid:.2f}"
            if brands_found:
                msg += f"\n⚠️ {len(brands_found)} từ khóa brand (nền vàng)"
            msg += f"\n\n📂 Thư mục: {os.path.dirname(out_path)}/"

            if messagebox.askyesno("Xuất thành công", msg + "\n\nMở thư mục chứa file?"):
                self._open_output_dir_at(os.path.dirname(out_path))

            status = f"✅ Đã xuất: {os.path.basename(out_path)} — {cnt} từ khóa"
            if filled_count > 0:
                status += f" | 💰 {filled_count} Bid điền TB ${avg_bid:.2f}"
            self._set_status(status)
        except Exception as e:
            messagebox.showerror("Lỗi xuất file", str(e))
            self._set_status(f"❌ Lỗi xuất: {e}")

    # ── Step 2 state ──────────────────────────────────────────────────────
    def _set_step2_state(self, state: str):
        for child in self.step2.winfo_children():
            self._set_widget_state(child, state)

    def _set_widget_state(self, widget, state: str):
        try:
            if widget.winfo_children():
                for child in widget.winfo_children():
                    self._set_widget_state(child, state)
            if isinstance(widget, (ttk.Entry, ttk.Button, tk.Listbox, ttk.Treeview)):
                widget.configure(state=state)
        except Exception:
            pass

    def _set_status(self, text: str):
        self.status_var.set(text)

    # ── Help / About ──────────────────────────────────────────────────────
    def _show_help(self):
        help_text = """📖 HƯỚNG DẪN SỬ DỤNG

BƯỚC 1 — LỌC TỪ KHÓA:
1. Chọn file Cerebro export (.xlsx) từ Helium 10
2. Nhập tên sản phẩm → Click "Phân tích & Gợi ý"
3. Chọn filter từ danh sách gợi ý
   - Click 1 lần để chọn → Click đúp để áp dụng luôn
   - Hoặc dùng Kết hợp (VD: 1+3) / Tự nhập
4. Click "Áp dụng filter →"

BƯỚC 2 — LỌC DỮ LIỆU & XUẤT:
1. Nhập Price ($) và Amazon Fee ($) để tính toán realtime
2. Xem preview 20 cột trong bảng (có cuộn ngang)
3. Các cột tự động tính: Clicks, Spend, Ads Orders,
   Ads Revenue, ACOS, Total Orders, Total Revenue,
   Product Fee, Total Fee, Profit
4. Thêm negative keywords nếu cần
5. Click "📤 Xuất file Excel" → 20 cột + công thức Excel
   → File lưu vào thư mục output/

FILE CONFIG (trong input/):
• SYNONYMS.txt — Từ điển đồng nghĩa
• brands.txt — Brand đối thủ (mỗi dòng 1 brand)
• keywords.txt — Negative keywords mặc định
• filters.txt — Lịch sử filter (tự động lưu)

MÀU SẮC:
• Vàng (#FFF2CC) = Từ khóa chứa brand đối thủ
• Xanh xen kẽ = Hàng chẵn cho dễ đọc

PHÍM TẮT:
• ↑↓ = Chọn dòng
• Delete/Backspace = Xóa dòng
• ⌘Z / Ctrl+Z = Undo
• ⌘C / Ctrl+C = Copy ô
• Chuột phải = Menu copy/xóa
"""
        messagebox.showinfo("Hướng dẫn", help_text)

    def _show_about(self):
        messagebox.showinfo(
            "Về PPC Keyword Filter Tool",
            "🔍 Auto Keywords v3.0\n\n"
            "Tích hợp 2 tool lọc từ khóa\n"
            "cho Amazon PPC / Helium 10 Cerebro\n\n"
            "✨ 20 cột xuất với công thức Excel\n"
            "📊 Tính toán realtime trên UI\n\n"
            "📅 2026-05-12\n"
            "🛠️ made by Experiences\n\n"
            "Python 3 + tkinter + pandas + openpyxl"
        )

    # ── Close ─────────────────────────────────────────────────────────────
    def _on_close(self):
        if self.state.df_filtered is not None and len(self.state.df_filtered) > 0:
            if not messagebox.askyesno("Thoát", "Bạn có dữ liệu đã lọc. Thoát sẽ mất?\n\nBạn có chắc muốn thoát?"):
                return
        self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()
