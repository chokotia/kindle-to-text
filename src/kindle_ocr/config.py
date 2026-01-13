"""設定定数モジュール"""

from pathlib import Path

# 入出力ディレクトリ
DEFAULT_INPUT_DIR = Path("./output/cropped")
DEFAULT_OUTPUT_DIR = Path("./output/text")

# Gemini API設定
MODEL_NAME = "gemini-3-flash-preview"
ENV_API_KEY = "GOOGLE_API_KEY"

# デフォルトプロンプト
DEFAULT_PROMPT = """この画像に含まれる日本語テキストを抽出してください。
- 改行は元のレイアウトを維持してください
- ページ番号やヘッダー/フッターは除外してください
- テキストのみを出力し、説明は不要です"""

# リクエスト間隔（秒）
DEFAULT_DELAY = 1.0

# ファイル命名規則
INPUT_PATTERN = "*.png"
OUTPUT_TEMPLATE = "{:03d}.txt"  # 001.txt, 002.txt, ...
