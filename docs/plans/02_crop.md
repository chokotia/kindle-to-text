# Kindle Crop Tool - 実装計画

## 概要
スクリーンショット画像から不要な部分（ページ番号、余白、UIなど）を除去し、本文のみを切り出すツール

## 入出力
- **入力**: `output/raw/` 内のPNG画像 (001.png, 002.png, ...)
- **出力**: `output/cropped/` 内のPNG画像 (001.png, 002.png, ...)

## 技術スタック
- Python 3.10+
- Poetry (依存関係管理)
- Pillow (画像処理)

## プロジェクト構成（追加分）

```
kindle-to-text/
├── src/
│   ├── kindle_screenshot/   # Phase 1 (既存)
│   └── kindle_crop/         # Phase 2 (新規)
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py           # CLIインターフェース
│       ├── crop.py          # クロップ処理
│       └── config.py        # 設定定数
└── output/
    ├── raw/
    └── cropped/             # 出力先
```

## 実装ステップ

### Step 1: pyproject.toml 更新
- 新しいスクリプトエントリポイント追加
- `kindle-crop` コマンド登録

### Step 2: 設定モジュール (`config.py`)
- 入力ディレクトリ (`output/raw/`)
- 出力ディレクトリ (`output/cropped/`)
- デフォルトクロップ領域（上下左右のマージン）

### Step 3: クロップ処理 (`crop.py`)
- `load_image()`: 画像読み込み
- `crop_image()`: 指定領域で切り抜き
- `save_image()`: 画像保存
- `process_all_images()`: バッチ処理

### Step 4: CLIインターフェース (`cli.py`)
- argparseでコマンドライン引数解析
- オプション: --input, --output, --top, --bottom, --left, --right

## クロップ方式の選択肢

### 方式A: 固定マージン指定
```bash
# 上100px, 下50px, 左右30pxをカット
poetry run kindle-crop --top 100 --bottom 50 --left 30 --right 30
```
- シンプルで予測可能
- 本ごとに調整が必要

### 方式B: 座標指定
```bash
# (100, 50) から (800, 1000) の領域を切り出し
poetry run kindle-crop --box 100,50,800,1000
```
- 精密な制御が可能
- 事前に座標を調べる必要あり

### 方式C: プレビューモード付き
```bash
# 1枚目でプレビュー表示し、確認後に全画像処理
poetry run kindle-crop --preview
```
- 試行錯誤しやすい
- インタラクティブ

**推奨**: 方式A（固定マージン）をベースに、方式C（プレビュー）を追加

## 使用方法

```bash
# 基本的な使い方（デフォルトマージンでクロップ）
poetry run kindle-crop

# マージン指定
poetry run kindle-crop --top 100 --bottom 80

# プレビューモード（1枚目を表示して確認）
poetry run kindle-crop --preview --top 100 --bottom 80
```

## CLI オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| -i, --input | 入力ディレクトリ | ./output/raw |
| -o, --output | 出力ディレクトリ | ./output/cropped |
| --top | 上部カット量(px) | 0 |
| --bottom | 下部カット量(px) | 0 |
| --left | 左部カット量(px) | 0 |
| --right | 右部カット量(px) | 0 |
| --preview | プレビューモード | False |

## 検証方法
1. Phase 1 で `output/raw/` にスクショを生成
2. `poetry run kindle-crop --preview --top 50` でプレビュー確認
3. 適切なマージンを調整
4. `poetry run kindle-crop --top 100 --bottom 80` で全画像処理
5. `output/cropped/` に切り抜き画像が生成されることを確認

## 作成/変更するファイル
1. `pyproject.toml` - エントリポイント追加
2. `src/kindle_crop/__init__.py` - パッケージ初期化
3. `src/kindle_crop/__main__.py` - モジュールエントリポイント
4. `src/kindle_crop/config.py` - 設定定数
5. `src/kindle_crop/crop.py` - クロップ処理
6. `src/kindle_crop/cli.py` - CLIインターフェース

## 備考
- クロップ領域は本のレイアウトによって異なるため、プレビュー機能が重要
- 将来的には画像解析による自動検出も検討可能
