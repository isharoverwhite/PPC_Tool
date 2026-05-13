"""
╔══════════════════════════════════════════════════════════════╗
║   PPC KEYWORD FILTER TOOL  —  Desktop Application            ║
╠══════════════════════════════════════════════════════════════╣
║  Chạy:  python3 main.py                                      ║
║                                                              ║
║  Yêu cầu:  pip install pandas openpyxl                       ║
║            (tkinter included in Python standard library)     ║
╚══════════════════════════════════════════════════════════════╝
"""
import sys
import os

# Đảm bảo thư mục gốc trong sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Kiểm tra dependencies
try:
    import pandas as pd       # noqa
    import openpyxl            # noqa
except ImportError:
    print("❌ Thiếu thư viện. Vui lòng chạy:")
    print("   pip install pandas openpyxl")
    sys.exit(1)

# Tạo thư mục cần thiết
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

from app.ui import App

if __name__ == "__main__":
    app = App()
    app.run()
