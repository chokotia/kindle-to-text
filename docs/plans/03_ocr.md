# Kindle OCR Tool - 実装計画

## 概要
クロップ済み画像からテキストを抽出するツール（Gemini CLI利用）

## 入出力
- **入力**: `output/cropped/` 内のPNG画像 (001.png, 002.png, ...)
- **出力**: `output/text/` 内のテキストファイル (001.txt, 002.txt, ...)

## 技術スタック
- Python 3.10+
- Poetry (依存関係管理)
- **Gemini CLI** (テキスト抽出)

## Gemini CLIについて

### 前提条件
- Gemini CLIがインストール済みであること
- Google AI API キーが設定済みであること

### 基本コマンド
```bash
# 画像からテキスト抽出
gemini --media "image.png" "この画像のテキストを抽出してください"
```

### 特徴
- マルチモーダルAIによる高精度なテキスト認識
- 日本語対応が優秀
- 従来のOCR（pytesseract, easyocr）より文脈理解が可能

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
│       ├── ocr.py           # Gemini CLI呼び出し処理
│       └── config.py        # 設定定数
└── output/
    ├── raw/
    ├── cropped/
    └── text/                # 出力先
```

## 実装ステップ

### Step 1: pyproject.toml 更新
- 新しいスクリプトエントリポイント追加
- `kindle-ocr` コマンド登録
- 外部依存: Gemini CLI（別途インストール必要）

### Step 2: 設定モジュール (`config.py`)
- 入力ディレクトリ (`output/cropped/`)
- 出力ディレクトリ (`output/text/`)
- Gemini CLIコマンド設定
- プロンプトテンプレート

### Step 3: OCR処理 (`ocr.py`)
- `check_gemini_cli()`: Gemini CLI存在確認
- `extract_text()`: subprocess で Gemini CLI を呼び出し
- `save_text()`: テキストファイル保存
- `process_all_images()`: バッチ処理（連番順に処理）

### Step 4: CLIインターフェース (`cli.py`)
- argparseでコマンドライン引数解析
- オプション: --input, --output, --prompt

## 使用方法

```bash
# 基本的な使い方
poetry run kindle-ocr

# カスタムプロンプト
poetry run kindle-ocr --prompt "この画像の日本語テキストを抽出して、改行を保持してください"
```

## CLI オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| -i, --input | 入力ディレクトリ | ./output/cropped |
| -o, --output | 出力ディレクトリ | ./output/text |
| --prompt | Geminiへのプロンプト | "この画像のテキストを抽出してください" |

## 内部処理

```python
# 各画像に対して実行されるコマンド（イメージ）
subprocess.run([
    "gemini",
    "--media", image_path,
    prompt
], capture_output=True, text=True)
```

## 検証方法
1. Gemini CLIがインストールされていることを確認: `gemini --version`
2. Phase 2 で `output/cropped/` にクロップ画像を生成
3. `poetry run kindle-ocr` でOCR実行
4. `output/text/` にテキストファイルが生成されることを確認
5. テキスト内容の精度を確認

## 作成/変更するファイル
1. `pyproject.toml` - エントリポイント追加
2. `src/kindle_ocr/__init__.py` - パッケージ初期化
3. `src/kindle_ocr/__main__.py` - モジュールエントリポイント
4. `src/kindle_ocr/config.py` - 設定定数
5. `src/kindle_ocr/ocr.py` - Gemini CLI呼び出し処理
6. `src/kindle_ocr/cli.py` - CLIインターフェース

## 注意事項
- Gemini CLIは別途インストールが必要（`npm install -g @anthropic-ai/gemini-cli` など）
- API利用料金が発生する可能性あり
- レート制限に注意（大量の画像処理時）

## 将来の拡張
- 全ページのテキストを1つのファイルに結合するオプション
- バッチ処理の並列化（レート制限を考慮）
- エラーリトライ機能
