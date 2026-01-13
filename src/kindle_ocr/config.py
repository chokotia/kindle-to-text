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
## 抽出ルール
- 書籍のレイアウト上の改行（行末での折り返し）は無視し、一つの文章として繋げてください。
- 段落の切り替わりや、明らかに意味が区切れる箇所でのみ改行を維持してください。
- ページ番号、ヘッダー、フッターなどの柱（ノンブル）は除外してください。
- テキストのみを出力し、説明は一切不要です。"""

# リクエスト間隔（秒）
DEFAULT_DELAY = 1.0

# ファイル命名規則
INPUT_PATTERN = "*.png"
OUTPUT_TEMPLATE = "{:03d}.txt"  # 001.txt, 002.txt, ...
