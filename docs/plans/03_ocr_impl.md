# Kindle OCR - 実装計画

採用技術: **Gemini API (2.0 Flash)**
技術選定の経緯: → `03_ocr_tech.md` 参照

## 入出力
- **入力**: `output/cropped/` 内のPNG画像 (001.png, 002.png, ...)
- **出力**: `output/text/` 内のテキストファイル (001.txt, 002.txt, ...)

## 技術スタック
- Python 3.10+
- Poetry (依存関係管理)
- `google-generativeai` (Gemini 2.0 Flash API)

## 前提条件
- 環境変数 `GOOGLE_API_KEY` にAPIキーを設定

## プロジェクト構成（追加分）

```
kindle-to-text/
├── src/
│   ├── kindle_screenshot/   # Phase 1 (既存)
│   ├── kindle_crop/         # Phase 2 (既存)
│   └── kindle_ocr/          # Phase 3 (新規)
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py           # CLIインターフェース
│       ├── ocr.py           # Gemini API呼び出し処理
│       └── config.py        # 設定定数
└── output/
    ├── raw/
    ├── cropped/
    └── text/                # 出力先
```

## 実装ステップ

### Step 1: pyproject.toml 更新
- `google-generativeai` 依存関係追加
- `kindle_ocr` パッケージ追加
- `kindle-ocr` スクリプトエントリポイント追加

### Step 2: 設定モジュール (`config.py`)
- 入力ディレクトリ (`output/cropped/`)
- 出力ディレクトリ (`output/text/`)
- モデル名 (`gemini-2.0-flash`)
- デフォルトプロンプト
- リクエスト間隔 (1.0秒)

### Step 3: OCR処理 (`ocr.py`)
- `configure_api()`: 環境変数からAPI設定
- `extract_text_from_image()`: Gemini APIでテキスト抽出
- `save_text()`: テキストファイル保存
- `process_all_images()`: バッチ処理
- `preview_ocr()`: プレビューモード

### Step 4: CLIインターフェース (`cli.py`)
- argparse でコマンドライン引数解析

## CLI オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| -i, --input | 入力ディレクトリ | ./output/cropped |
| -o, --output | 出力ディレクトリ | ./output/text |
| --prompt | Geminiへのプロンプト | (日本語OCR用) |
| --delay | リクエスト間隔（秒） | 1.0 |
| --preview | プレビューモード | False |

## 使用方法

```bash
# APIキー設定（Windows）
set GOOGLE_API_KEY=your-api-key-here

# プレビュー（1枚目のみテスト）
poetry run kindle-ocr --preview

# バッチ処理
poetry run kindle-ocr

# レート制限対策
poetry run kindle-ocr --delay 2.0
```

## 内部処理

```python
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")
image = Image.open(image_path)
response = model.generate_content([prompt, image])
text = response.text
```

## 作成/変更するファイル
1. `pyproject.toml` - 依存関係・エントリポイント追加
2. `src/kindle_ocr/__init__.py`
3. `src/kindle_ocr/__main__.py`
4. `src/kindle_ocr/config.py`
5. `src/kindle_ocr/ocr.py`
6. `src/kindle_ocr/cli.py`

## 検証方法
1. `echo %GOOGLE_API_KEY%` で環境変数確認
2. `poetry run kindle-ocr --preview` でプレビュー
3. `poetry run kindle-ocr` でバッチ実行
4. `output/text/` の出力確認
