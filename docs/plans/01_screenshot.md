# Kindle Screenshot Automation Tool - 実装計画

## 概要
Kindleアプリのページを自動でスクリーンショットし、連番で保存するPythonツール

## 技術スタック
- Python 3.10+
- Poetry (依存関係管理)
- pyautogui (GUI自動化)
- Pillow (画像処理)
- pygetwindow (ウィンドウ管理)

## プロジェクト構成

```
kindle-to-text/
├── pyproject.toml
├── README.md
├── .gitignore
├── src/
│   └── kindle_screenshot/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py          # CLIインターフェース
│       ├── capture.py      # スクリーンショット処理
│       ├── window.py       # ウィンドウ管理
│       └── config.py       # 設定定数
└── output/
    ├── raw/                # 出力先: 画面全体のスクショ
    ├── cropped/            # Phase 2で使用
    └── text/               # Phase 3で使用
```

## 実装ステップ

### Step 1: Poetry プロジェクト初期化
- `pyproject.toml` 作成
- 依存関係: pyautogui, Pillow, pygetwindow
- スクリプトエントリポイント設定

### Step 2: 設定モジュール (`config.py`)
- デフォルト出力ディレクトリ (`output/raw/`)
- ページ間遅延時間 (0.5秒)
- 開始前待機時間 (3秒)
- Kindleウィンドウタイトルパターン
- ファイル命名規則 (001.png, 002.png, ...)

### Step 3: ウィンドウ管理 (`window.py`)
- `find_kindle_window()`: Kindleウィンドウ検索
- `activate_kindle_window()`: ウィンドウをアクティブ化
- `get_kindle_window_region()`: スクリーンショット領域取得

### Step 4: キャプチャ処理 (`capture.py`)
- `ensure_output_folder()`: output/raw/ フォルダ作成
- `generate_filename()`: 連番ファイル名生成 (001.png, 002.png, ...)
- `take_screenshot()`: スクリーンショット撮影・保存
- `navigate_to_next_page()`: 右矢印キーでページ送り
- `capture_pages()`: メイン処理ループ

### Step 5: CLIインターフェース (`cli.py`)
- argparseでコマンドライン引数解析
- 必須引数: page_count
- オプション: --output, --delay, --initial-delay, --full-screen

### Step 6: エントリポイント
- `__init__.py`: パッケージ初期化
- `__main__.py`: `python -m kindle_screenshot` 対応

### Step 7: .gitignore 作成
- Python関連、output/、IDE設定を除外

## 使用方法

```bash
# インストール
poetry install

# 基本的な使い方 (100ページキャプチャ)
poetry run kindle-screenshot 100

# オプション指定
poetry run kindle-screenshot 200 -d 1.0 --full-screen
```

## CLI オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| page_count | キャプチャするページ数 | 必須 |
| -o, --output | 出力ディレクトリ | ./output/raw |
| -d, --delay | ページ間の待機時間(秒) | 0.5 |
| --initial-delay | 開始前の待機時間(秒) | 3.0 |
| --full-screen | 全画面キャプチャ | False |

## 注意事項
- Kindleアプリを事前に開いておく必要あり
- プライマリモニターで使用推奨
- 緊急停止: マウスを画面左上(0,0)に移動

## 検証方法
1. `poetry install` で依存関係インストール
2. Kindleアプリを開き、テスト用の本を表示
3. `poetry run kindle-screenshot 3` で3ページキャプチャ
4. `output/raw/` に 001.png, 002.png, 003.png が保存されることを確認

## 作成/変更するファイル
1. `pyproject.toml` - Poetry設定
2. `src/kindle_screenshot/__init__.py` - パッケージ初期化
3. `src/kindle_screenshot/__main__.py` - モジュールエントリポイント
4. `src/kindle_screenshot/config.py` - 設定定数
5. `src/kindle_screenshot/window.py` - ウィンドウ管理
6. `src/kindle_screenshot/capture.py` - キャプチャ処理
7. `src/kindle_screenshot/cli.py` - CLIインターフェース
8. `.gitignore` - Git除外設定
9. `output/raw/.gitkeep` - 出力フォルダ保持
10. `output/cropped/.gitkeep` - Phase 2用フォルダ
11. `output/text/.gitkeep` - Phase 3用フォルダ
