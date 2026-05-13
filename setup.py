"""
py2app setup — Đóng gói PPC Keyword Filter Tool thành .app cho macOS
Chạy:  python3 setup.py py2app
"""
from setuptools import setup
import glob
import os

# Chỉ lấy file config (.txt), bỏ qua .xlsx
input_files = []
for f in glob.glob("input/*"):
    if os.path.isfile(f) and not f.endswith(".xlsx"):
        input_files.append(f)

APP = ["main.py"]
DATA_FILES = [("input", input_files)]
OPTIONS = {
    "argv_emulation": False,
    "packages": ["pandas", "openpyxl", "app"],
    "includes": ["tkinter"],
    "excludes": [
        # GUI không dùng
        "PyQt5", "PyQt6", "PySide2", "PySide6", "wx", "pygame",
        # Math/Science không dùng
        "matplotlib", "numpy", "scipy", "PIL", "Pillow",
        # Database không dùng
        "sqlalchemy", "sqlite3", "psycopg2", "pymysql", "mysql",
        # Pandas I/O không dùng
        "pyarrow", "fastparquet", "tables", "h5py", "xlsxwriter",
        "xlrd", "xlwt", "s3fs", "fsspec",
        # Dev tools không cần
        "setuptools", "pip", "wheel", "pkg_resources",
        "pygments", "IPython", "jupyter", "notebook",
        # Testing không cần
        "pytest", "unittest", "nose", "coverage",
        # Web/Network không dùng
        "flask", "django", "requests", "urllib3", "certifi",
        "chardet", "idna", "aiohttp", "tornado",
        # Khác
        "cryptography", "bcrypt", "paramiko",
        "scipy.sparse", "scipy.stats", "sklearn",
        "numexpr", "bottleneck", "odfpy",
        "pyreadstat", "python_calamine", "pyxlsb",
        "tzdata", "pytzdata",
    ],
    "strip": True,         # Xóa debug symbols khỏi binary
    "optimize": 2,         # -OO: xóa docstrings + assert
    "iconfile": None,
    "plist": {
        "CFBundleName": "PPC Keyword Filter",
        "CFBundleDisplayName": "🔍 PPC Keyword Filter",
        "CFBundleIdentifier": "com.saigonlash.ppc-keyword-filter",
        "CFBundleVersion": "3.0",
        "CFBundleShortVersionString": "3.0",
        "NSHumanReadableCopyright": "© 2026 SAIGON LASH / MariaMCP",
        "NSHighResolutionCapable": True,
    },
}

setup(
    name="PPC Keyword Filter",
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
