# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PPC Keyword Filter Tools — A desktop application (tkinter) for Amazon PPC sellers using Helium 10 Cerebro. It takes a Cerebro keyword export (.xlsx), helps the user pick a regex filter pattern via smart suggestions, previews 20 columns of computed PPC metrics in real time, and exports a formatted Excel workbook with live formulas. Built for **SAIGON LASH Store** (MariaMCP).

### Domain Context
- **Input**: Helium 10 Cerebro export (.xlsx) containing 1,000+ keywords with columns like Keyword Phrase, Search Volume, Sponsored ASINs, Competing Products, CPR, H10 PPC Sugg. Bid
- **Output**: 20-column Excel with formulas: Clicks = CTR × SearchVol, Spend = Bid × Clicks, Ads Orders, Ads Revenue, ACOS, Total Orders, Total Revenue, Product Fee, Total Fee, Profit
- **Users**: Amazon store owners who can run `python3 main.py` but prefer GUI over CLI
- **Language**: UI labels and console output are in Vietnamese

## Commands

```bash
# Install dependencies
pip install pandas openpyxl

# Run the desktop app (tkinter — no CLI args needed)
python3 main.py

# The app automatically looks for input/input.xlsx on startup
# Place your Cerebro export in input/ as input.xlsx, or use "Browse" inside the app
```

## Architecture

```
cleanUp_data/
├── main.py                     # Entry point: checks deps, creates input/ + output/, launches App
├── app/
│   ├── __init__.py             # Minimal package marker
│   ├── constants.py            # All config: OUTPUT_COLS, FULL_EXPORT_COLS, COLORS, INPUT_FILES, RATING_THRESHOLDS
│   ├── engine.py               # FilterEngine: load Cerebro, apply regex filter, fill missing bids, load/save config files
│   ├── synonym_engine.py       # SynonymEngine: load SYNONYMS.txt, extract_terms(), build_suggestions()
│   ├── excel_writer.py         # ExcelWriter: export 20-column XLSX with formulas + styling
│   └── ui.py                   # App class: tkinter UI with Step 1 (filter selection) + Step 2 (preview & export)
├── input/                      # Config files (loaded at runtime, not hardcoded):
│   ├── SYNONYMS.txt            #   synonym mappings (e.g., "premade = pre made, promade, ...")
│   ├── STOP_WORDS.txt          #   words to filter when parsing product name
│   ├── brands.txt              #   competitor brand names → rows highlighted yellow
│   ├── keywords.txt            #   negative keywords to exclude
│   ├── filters.txt             #   filter pattern history (auto-appended on each export)
│   ├── product_name.txt        #   product name history (auto-saved on each analysis)
│   ├── rival_company.txt       #   competitor company names → rows auto-removed
│   └── *.xlsx                  #   place Cerebro export here, or use Browse in app
├── output/                     # Exported .xlsx files land here (user can also choose via Save dialog)
├── README.md                   # Vietnamese documentation
├── PRD.md                      # Product Requirements Document
├── PLAN.md                     # Architecture + Implementation Plan (870 lines, v2.0 for desktop app)
├── AGENTS.md                   # Agent routing config (planner-agent / coding-agent)
└── CLAUDE.md                   # This file
```

### Data Flow (Desktop App)

```
1. App starts → loads SYNONYMS.txt, STOP_WORDS.txt, brands.txt, filters.txt
2. User selects Cerebro .xlsx (or auto-loads input/input.xlsx)
3. Step 1 — Filter Selection:
   a. User enters product name (e.g., "Super Narrow Premade Fans 3D 5D C Curl")
   b. SynonymEngine.extract_terms() → splits into words + bigrams, expands synonyms, removes stop words
   c. SynonymEngine.build_suggestions() → for each term (solo + OR combos), count matches via regex on Keyword Phrase
   d. Suggestions scored: 20-60=✅Lý tưởng, 10-19=🟡Hơi ít, 61-100=🟡Hơi nhiều, <10=⚪Quá ít, >100=🔴Quá rộng
   e. User clicks a suggestion (or combines multiple via "1+3" syntax, or enters custom regex)
   f. "Áp dụng filter" → FilterEngine.apply_filter() + auto-remove rival company keywords
4. Step 2 — Preview & Export:
   a. Preview table shows 20 computed columns in real time
   b. User can set Price ($) and Amazon Fee ($) → all formulas recalculate instantly
   c. User can add negative keywords, delete rows (with undo ⌘Z), fill missing bids
   d. Export → ExcelWriter.export_full() → 20-column .xlsx with formulas, styling, section rows
```

### Key Shared Patterns

- **20 output columns** (FULL_EXPORT_COLS in constants.py): 6 Cerebro columns + 14 computed columns (CTR, Clicks, Spend, CVR, Ads Orders, Price, Ads Revenue, ACOS, Total Orders, Total Revenue, Product Fee, Amazon Fee, Total Fee, Profit)
- **Excel formulas in cells**: All computed columns are Excel formulas referencing row data (e.g., `=G{n}*B{n}` for Clicks), not hardcoded values
- **Excel styling** (excel_writer.py): Orange header (`FFE69138`), brand rows yellow (`FFFF2CC`), no alternating rows (matches a specific template), frozen pane at A2
- **Excel extras**: Total row, 5 section rows (short-tail campaigns, Auto, Cate, ASIN, broad/phrase), Total+50-100% row (×160%)
- **Config-driven**: Synonyms, stop words, brands, filters all live in `input/` .txt files — not hardcoded in Python
- **Filter syntax**: regex, `|` = OR, case-insensitive — e.g., `"premade|promade"` matches either word
- **Brand auto-remove**: When applying filter, all rows containing rival company names (from `rival_company.txt`) are automatically removed from the result
- **Bid fill**: Missing `H10 PPC Sugg. Bid` values are filled with the column average before export
- **Threading**: `_analyze()` runs in a background thread to keep UI responsive
- **Undo stack**: Deleted rows in the preview can be undone via ⌘Z/Ctrl+Z (up to unlimited steps)
