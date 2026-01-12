"""設定定数モジュール"""

from pathlib import Path

# 入出力ディレクトリ
DEFAULT_INPUT_DIR = Path("./output/raw")
DEFAULT_OUTPUT_DIR = Path("./output/cropped")

# デフォルトクロップマージン（px）
DEFAULT_MARGIN_TOP = 0
DEFAULT_MARGIN_BOTTOM = 0
DEFAULT_MARGIN_LEFT = 0
DEFAULT_MARGIN_RIGHT = 0

# ファイル命名規則
FILENAME_PATTERN = "{:03d}.png"  # 001.png, 002.png, ...
