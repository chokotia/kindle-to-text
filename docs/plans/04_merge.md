# Kindle Chapter Merge Tool - 実装計画

## 概要
ページ単位のテキストファイルを、設定ファイル（chapters.yaml）に基づいて章ごとに結合するツール

## 入出力
- **入力**:
  - `output/text/` 内のテキストファイル (001.txt, 002.txt, ...)
  - `chapters.yaml` (章とページ範囲の定義)
- **出力**: `output/chapters/` 内の章ごとテキストファイル

## 技術スタック
- Python 3.10+
- Poetry (依存関係管理)
- PyYAML (設定ファイル読み込み)

## 設定ファイル形式

### chapters.yaml サンプル

```yaml
# 章ごとのページ範囲を定義
# start: 開始ページ番号
# end: 終了ページ番号（このページを含む）

chapters:
  - name: "はじめに"
    start: 1
    end: 5

  - name: "第1章 基礎知識"
    start: 6
    end: 25

  - name: "第2章 実践編"
    start: 26
    end: 50

  - name: "第3章 応用テクニック"
    start: 51
    end: 80

  - name: "第4章 トラブルシューティング"
    start: 81
    end: 100

  - name: "付録"
    start: 101
    end: 110

  - name: "おわりに"
    start: 111
    end: 115
```

### 出力ファイル命名規則
章の順番と名前を使用:
- `01_はじめに.txt`
- `02_第1章 基礎知識.txt`
- `03_第2章 実践編.txt`
- ...

## プロジェクト構成（追加分）

```
kindle-to-text/
├── chapters.yaml.sample    # 設定ファイルのサンプル
├── chapters.yaml           # 実際の設定ファイル（ユーザーが作成）
├── src/
│   ├── kindle_screenshot/  # Phase 1 (既存)
│   ├── kindle_crop/        # Phase 2 (既存)
│   ├── kindle_ocr/         # Phase 3 (既存)
│   └── kindle_merge/       # Phase 4 (新規)
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py          # CLIインターフェース
│       ├── merge.py        # 結合処理
│       └── config.py       # 設定定数
└── output/
    ├── raw/
    ├── cropped/
    ├── text/
    └── chapters/           # 出力先
```

## 実装ステップ

### Step 1: pyproject.toml 更新
- PyYAML 依存関係追加
- 新しいスクリプトエントリポイント追加
- `kindle-merge` コマンド登録

### Step 2: 設定モジュール (`config.py`)
- 入力ディレクトリ (`output/text/`)
- 出力ディレクトリ (`output/chapters/`)
- 設定ファイルパス (`chapters.yaml`)

### Step 3: 結合処理 (`merge.py`)
- `load_chapters_config()`: YAML設定読み込み
- `get_page_files()`: 指定範囲のテキストファイル一覧取得
- `merge_pages()`: 複数ファイルを1つに結合
- `generate_chapter_filename()`: 章ごとのファイル名生成
- `process_all_chapters()`: 全章を処理

### Step 4: CLIインターフェース (`cli.py`)
- argparseでコマンドライン引数解析
- オプション: --input, --output, --config

### Step 5: サンプル設定ファイル
- `chapters.yaml.sample` を作成

## 使用方法

```bash
# 1. 設定ファイルをサンプルからコピーして編集
cp chapters.yaml.sample chapters.yaml
# (エディタで chapters.yaml を編集)

# 2. 結合を実行
poetry run kindle-merge

# カスタム設定ファイル指定
poetry run kindle-merge --config my_chapters.yaml
```

## CLI オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| -i, --input | 入力ディレクトリ | ./output/text |
| -o, --output | 出力ディレクトリ | ./output/chapters |
| -c, --config | 設定ファイル | ./chapters.yaml |

## 処理フロー

```
1. chapters.yaml を読み込み
2. 各章について:
   a. start〜end のページ番号を取得
   b. 対応するテキストファイル (001.txt〜005.txt など) を読み込み
   c. 内容を結合
   d. 章ごとのファイル名で保存 (01_はじめに.txt)
3. 処理完了を報告
```

## 検証方法
1. `chapters.yaml.sample` を `chapters.yaml` にコピー
2. 内容を実際の本の章構成に合わせて編集
3. `poetry run kindle-merge` を実行
4. `output/chapters/` に章ごとのファイルが生成されることを確認

## 作成/変更するファイル
1. `pyproject.toml` - 依存関係・エントリポイント追加
2. `chapters.yaml.sample` - 設定ファイルのサンプル
3. `src/kindle_merge/__init__.py` - パッケージ初期化
4. `src/kindle_merge/__main__.py` - モジュールエントリポイント
5. `src/kindle_merge/config.py` - 設定定数
6. `src/kindle_merge/merge.py` - 結合処理
7. `src/kindle_merge/cli.py` - CLIインターフェース
8. `output/chapters/.gitkeep` - 出力フォルダ保持

## エラーハンドリング
- 設定ファイルが存在しない場合: エラーメッセージと使い方を表示
- 指定ページのファイルが存在しない場合: 警告を出して続行（または欠番として記録）
- ページ範囲の重複: 許容（同じページが複数章に含まれてもOK）
