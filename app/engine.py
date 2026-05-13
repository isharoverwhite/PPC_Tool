"""
╔══════════════════════════════════════════════════════════════╗
║   FILTER ENGINE  —  Load, filter, preview Cerebro data       ║
╚══════════════════════════════════════════════════════════════╝
"""
import os, re
from dataclasses import dataclass, field

import pandas as pd

from app.constants import INPUT_DIR, INPUT_FILES, OUTPUT_COLS


@dataclass
class AppState:
    """Trạng thái toàn cục của ứng dụng."""
    input_file: str | None = None
    df_raw: pd.DataFrame | None = None
    df_filtered: pd.DataFrame | None = None
    suggestions: list = field(default_factory=list)
    selected_filter: str | None = None
    product_name: str | None = None
    negative_kws: list[str] = field(default_factory=list)
    brands: list[str] = field(default_factory=list)
    total_count: int = 0


class FilterEngine:
    """Xử lý dữ liệu Cerebro: load, filter, negative keywords."""

    # ── Load file ──────────────────────────────────────────────────────────
    def load_cerebro(self, filepath: str) -> pd.DataFrame:
        """Đọc file Cerebro export, validate schema."""
        df = pd.read_excel(filepath)

        # Kiểm tra cột bắt buộc
        required = ["Keyword Phrase"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"File thiếu cột bắt buộc: {', '.join(missing)}")

        # Kiểm tra cột Bid
        if "H10 PPC Sugg. Bid" not in df.columns:
            raise ValueError(
                "File không có cột 'H10 PPC Sugg. Bid'.\n"
                "Kiểm tra lại cài đặt export trong Helium 10 Cerebro."
            )

        return df

    # ── Áp dụng filter ─────────────────────────────────────────────────────
    def apply_filter(self, df: pd.DataFrame, pattern: str) -> pd.DataFrame:
        """Lọc dataframe theo regex pattern (case-insensitive)."""
        mask = df["Keyword Phrase"].str.contains(
            pattern, case=False, na=False, regex=True
        )
        return df[mask].copy().reset_index(drop=True)

    # ── Đếm matches ────────────────────────────────────────────────────────
    def count_matches(self, df: pd.DataFrame, pattern: str) -> int:
        """Đếm số dòng khớp pattern."""
        try:
            return int(df["Keyword Phrase"].str.contains(
                pattern, case=False, na=False, regex=True
            ).sum())
        except Exception:
            return 0

    # ── Điền Bid thiếu bằng trung bình ────────────────────────────────────
    def fill_missing_bids(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int, float]:
        """
        Điền các dòng thiếu Bid (NaN) bằng trung bình của các Bid có giá trị.
        Trả về: (DataFrame đã điền, số dòng đã điền, giá trị trung bình)
        """
        bid_col = "H10 PPC Sugg. Bid"
        if bid_col not in df.columns:
            return df.copy(), 0, 0.0

        result = df.copy()
        missing_mask = result[bid_col].isna()
        missing_count = int(missing_mask.sum())

        if missing_count == 0:
            return result, 0, 0.0

        avg_bid = float(result[bid_col].mean())
        result.loc[missing_mask, bid_col] = round(avg_bid, 2)
        return result, missing_count, avg_bid

    # ── Loại bỏ negative keywords ──────────────────────────────────────────
    def remove_negative_keywords(
        self, df: pd.DataFrame, negative_kws: list[str]
    ) -> pd.DataFrame:
        """Xóa các dòng chứa bất kỳ negative keyword nào."""
        if not negative_kws:
            return df.copy()
        pattern = "|".join(re.escape(kw) for kw in negative_kws)
        mask = ~df["Keyword Phrase"].str.contains(
            pattern, case=False, na=False, regex=True
        )
        return df[mask].copy().reset_index(drop=True)

    # ── Load file config từ input/ ─────────────────────────────────────────
    def load_brands(self) -> list[str]:
        """Đọc brands.txt."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["brands"])
        return self._read_lines(path)

    def load_negative_keywords(self) -> list[str]:
        """Đọc keywords.txt (negative keywords)."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["keywords"])
        return self._read_lines(path)

    def load_filters_history(self) -> list[str]:
        """Đọc filters.txt (lịch sử filter)."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["filters"])
        return self._read_lines(path)

    def load_product_names(self) -> list[str]:
        """Đọc product_name.txt — lịch sử tên SP (mỗi dòng 1 tên)."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["product_name"])
        names = self._read_lines(path)
        return list(dict.fromkeys(names))  # dedupe, giữ thứ tự

    def save_product_name(self, name: str):
        """Thêm tên SP vào product_name.txt (không trùng lặp)."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["product_name"])
        os.makedirs(INPUT_DIR, exist_ok=True)
        existing = set()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = {line.strip() for line in f if line.strip() and not line.startswith("#")}
        name = name.strip()
        if name and name not in existing:
            with open(path, "a", encoding="utf-8") as f:
                f.write(name + "\n")

    # ── Rival company ────────────────────────────────────────────────────
    def load_rival_companies(self) -> list[str]:
        """Đọc rival_company.txt — danh sách tên công ty đối thủ cần loại bỏ."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["rival_company"])
        return self._read_lines(path)

    def save_rival_company(self, name: str):
        """Thêm 1 công ty vào rival_company.txt (không trùng lặp)."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["rival_company"])
        os.makedirs(INPUT_DIR, exist_ok=True)
        existing = set()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = {line.strip().lower() for line in f if line.strip() and not line.startswith("#")}
        name = name.strip().lower()
        if name and name not in existing:
            with open(path, "a", encoding="utf-8") as f:
                f.write(name + "\n")

    def remove_rival_keywords(
        self, df: pd.DataFrame, rivals: list[str]
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Loại bỏ các dòng có chứa tên công ty đối thủ.
        Trả về: (df đã lọc sạch, df các dòng bị loại)
        """
        if not rivals:
            return df.copy(), pd.DataFrame()
        pattern = "|".join(re.escape(r) for r in rivals)
        mask = df["Keyword Phrase"].str.contains(pattern, case=False, na=False, regex=True)
        removed = df[mask].copy()
        clean = df[~mask].copy().reset_index(drop=True)
        return clean, removed

    def save_negative_keywords(self, keywords: list[str]):
        """Ghi danh sách negative keywords vào keywords.txt."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["keywords"])
        os.makedirs(INPUT_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Negative Keywords — mỗi dòng 1 từ khóa cần loại bỏ\n")
            f.write("# Các từ khóa chứa những từ này sẽ bị tự động lọc khỏi kết quả\n")
            for kw in keywords:
                f.write(kw + "\n")

    def save_filter_to_history(self, pattern: str):
        """Thêm filter pattern vào filters.txt."""
        path = os.path.join(INPUT_DIR, INPUT_FILES["filters"])
        os.makedirs(INPUT_DIR, exist_ok=True)
        existing = set()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                existing = {line.strip() for line in f if line.strip() and not line.startswith("#")}
        if pattern not in existing:
            with open(path, "a", encoding="utf-8") as f:
                f.write(pattern + "\n")

    @staticmethod
    def _read_lines(path: str) -> list[str]:
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return [
                line.strip() for line in f
                if line.strip() and not line.startswith("#")
            ]

    # ── Preview ────────────────────────────────────────────────────────────
    def get_preview_rows(self, df: pd.DataFrame, n: int = 5) -> list[dict]:
        """Lấy n dòng đầu để hiển thị preview."""
        cols = list(OUTPUT_COLS.keys())
        rows = []
        for _, row in df.head(n).iterrows():
            r = {}
            for dest, src in OUTPUT_COLS.items():
                val = row.get(src) if src in df.columns else None
                if val is not None and not pd.isna(val):
                    r[dest] = val
                else:
                    r[dest] = None
            rows.append(r)
        return rows
