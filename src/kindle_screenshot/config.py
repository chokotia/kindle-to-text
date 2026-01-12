"""設定定数モジュール"""

from pathlib import Path

# 出力ディレクトリ
DEFAULT_OUTPUT_DIR = Path("./output/raw")

# タイミング設定
DEFAULT_PAGE_DELAY = 0.5  # ページ間の待機時間（秒）
DEFAULT_INITIAL_DELAY = 3.0  # 開始前の待機時間（秒）

# Kindleウィンドウ検索用パターン
KINDLE_WINDOW_PATTERNS = [
    "Kindle for PC",
    "kindle for PC",
]

# ファイル命名規則
FILENAME_PATTERN = "{:03d}.png"  # 001.png, 002.png, ...
