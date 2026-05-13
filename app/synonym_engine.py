"""
╔══════════════════════════════════════════════════════════════╗
║   SYNONYM ENGINE  —  Phân tích tên SP → terms + gợi ý filter║
╚══════════════════════════════════════════════════════════════╝
"""
import os, re
from itertools import combinations
from dataclasses import dataclass, field

import pandas as pd

from app.constants import (
    RATING_THRESHOLDS, INPUT_DIR, INPUT_FILES
)


@dataclass
class FilterSuggestion:
    pattern: str
    count: int
    terms: list[str] = field(default_factory=list)
    rating: str = ""
    priority: int = 0


class SynonymEngine:
    """Phân tích tên sản phẩm và sinh gợi ý filter."""

    def __init__(self):
        self._synonyms: dict[str, list[str]] = {}
        self._stopwords: set[str] = set()
        self._load_synonyms_file()
        self._load_stopwords_file()
        if not self._synonyms:
            raise RuntimeError(
                f"Không tìm thấy hoặc file rỗng: {INPUT_DIR}/{INPUT_FILES['synonyms']}\n"
                "Vui lòng tạo file SYNONYMS.txt trong thư mục input/ với định dạng:\n"
                "  base_word = variant1, variant2, variant3"
            )

    # ── Load SYNONYMS.txt ──────────────────────────────────────────────────
    def _load_synonyms_file(self):
        path = os.path.join(INPUT_DIR, INPUT_FILES["synonyms"])
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        base, variants = line.split("=", 1)
                        base = base.strip().lower()
                        vars_list = [v.strip().lower() for v in variants.split(",") if v.strip()]
                        if base and vars_list:
                            self._synonyms[base] = vars_list
        except Exception as e:
            raise RuntimeError(f"Lỗi đọc SYNONYMS.txt: {e}")

    # ── Load STOP_WORDS.txt ────────────────────────────────────────────────
    def _load_stopwords_file(self):
        path = os.path.join(INPUT_DIR, INPUT_FILES["stopwords"])
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                self._stopwords = {
                    line.strip().lower() for line in f
                    if line.strip() and not line.startswith("#")
                }
        except Exception as e:
            raise RuntimeError(f"Lỗi đọc STOP_WORDS.txt: {e}")

    def reload_config(self):
        """Tải lại cả SYNONYMS.txt và STOP_WORDS.txt."""
        self._synonyms = {}
        self._stopwords = set()
        self._load_synonyms_file()
        self._load_stopwords_file()

    @property
    def synonyms_dict(self) -> dict:
        return dict(self._synonyms)

    # ── Trích xuất terms từ tên SP ─────────────────────────────────────────
    def extract_terms(self, product_name: str) -> list[str]:
        """Tách các từ có nghĩa từ tên sản phẩm, mở rộng synonyms."""
        cleaned = re.sub(r'[^\w\s]', ' ', product_name.lower())
        words = cleaned.split()

        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]

        terms = []
        for t in words + bigrams:
            t = t.strip()
            if len(t) < 3:
                continue
            if t in self._stopwords:
                continue
            if " " in t and all(w in self._stopwords for w in t.split()):
                continue
            terms.append(t)

        # Mở rộng synonyms
        expanded = list(terms)
        for term in terms:
            base = term.split()[0] if " " in term else term
            if base in self._synonyms:
                expanded.extend(self._synonyms[base])

        return list(dict.fromkeys(expanded))

    # ── Sinh danh sách gợi ý ───────────────────────────────────────────────
    def build_suggestions(self, df: pd.DataFrame, terms: list[str]) -> list[FilterSuggestion]:
        """Tạo danh sách gợi ý filter từ terms, kèm số lượng match."""
        suggestions: list[FilterSuggestion] = []
        seen: set[str] = set()

        def _count(pattern: str) -> int:
            try:
                return int(df["Keyword Phrase"].str.contains(
                    pattern, case=False, na=False, regex=True
                ).sum())
            except Exception:
                return 0

        # Đơn lẻ
        for t in terms:
            if t in seen:
                continue
            cnt = _count(t)
            if cnt == 0:
                continue
            suggestions.append(FilterSuggestion(pattern=t, count=cnt, terms=[t]))
            seen.add(t)

        # Kết hợp OR (2 terms)
        good_single = [s for s in suggestions if s.count <= 200]
        for a, b in combinations(good_single[:20], 2):
            pat = f"{a.pattern}|{b.pattern}"
            if pat in seen:
                continue
            cnt = _count(pat)
            if cnt == 0:
                continue
            suggestions.append(FilterSuggestion(
                pattern=pat, count=cnt,
                terms=[a.pattern, b.pattern]
            ))
            seen.add(pat)

        # Score & sort
        def _score(s: FilterSuggestion) -> int:
            c = s.count
            ideal = RATING_THRESHOLDS["ideal"]
            few = RATING_THRESHOLDS["few"]
            many = RATING_THRESHOLDS["many"]
            if ideal[0] <= c <= ideal[1]:
                s.rating = "✅ Lý tưởng"
                s.priority = 0
                return 0
            elif few[0] <= c <= few[1]:
                s.rating = "🟡 Hơi ít"
                s.priority = 1
                return 1
            elif many[0] <= c <= many[1]:
                s.rating = "🟡 Hơi nhiều"
                s.priority = 2
                return 2
            elif c < 10:
                s.rating = "⚪ Quá ít"
                s.priority = 3
                return 3
            else:
                s.rating = "🔴 Quá rộng"
                s.priority = 4
                return 4

        suggestions.sort(key=lambda s: (_score(s), -s.count))
        return suggestions
