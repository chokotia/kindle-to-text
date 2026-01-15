# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

Kindle to Text は、Kindleの書籍コンテンツをテキストに変換するWindows用ツール。4フェーズのパイプラインで処理する：
1. **スクリーンショット** (`kindle-screenshot`): pyautoguiでKindleページを自動キャプチャ
2. **クロップ** (`kindle-crop`): Pillowで余白・UI・ページ番号を除去
3. **OCR** (`kindle-ocr`): Gemini CLIでテキスト抽出
4. **結合** (`kindle-merge`): `chapters.yaml`に基づいてページテキストを章ごとに結合

## 技術スタック

- Python 3.10+
- uv（依存関係管理）
- 主要ライブラリ: pyautogui, Pillow, pygetwindow, google-genai
- 外部ツール: Gemini API（OCRフェーズで使用）

## コマンド

```bash
# 依存関係インストール
uv sync

# Phase 1: スクリーンショット（Kindleアプリを開いた状態で実行）
uv run kindle-screenshot <ページ数> [-d 遅延秒] [--full-screen]

# Phase 2: クロップ
uv run kindle-crop [--top N] [--bottom N] [--left N] [--right N] [--preview]

# Phase 3: OCR
uv run kindle-ocr [--prompt "カスタムプロンプト"]

# Phase 4: 結合（chapters.yamlが必要）
uv run kindle-merge [-c config.yaml]
```

## プロジェクト構成

```
src/
├── kindle_screenshot/  # Phase 1: capture.py, window.py, cli.py, config.py
├── kindle_crop/        # Phase 2: crop.py, cli.py, config.py
├── kindle_ocr/         # Phase 3: ocr.py（Gemini API呼び出し）, cli.py, config.py
└── kindle_merge/       # Phase 4: merge.py, cli.py, config.py

output/
├── raw/       # Phase 1出力: 画面全体のスクショ (001.png, 002.png, ...)
├── cropped/   # Phase 2出力: 本文のみの画像
├── text/      # Phase 3出力: ページごとのテキスト (001.txt, 002.txt, ...)
└── chapters/  # Phase 4出力: 章ごとに結合したテキスト
```

## 設計パターン

- 各フェーズは`src/`配下の独立したパッケージ。構成は統一: `cli.py`, `config.py`, メインロジックモジュール
- 全CLIツールはargparseを使用し、`-i/--input`と`-o/--output`オプションを持つ
- ファイル命名規則: 3桁ゼロパディング連番（001, 002, ...）で全フェーズ統一
- `chapters.yaml`で章名とページ範囲を定義（結合フェーズで使用）

## 開発時の注意

- スクリーンショット緊急停止: マウスを画面左上(0,0)に移動
- クロップマージンは本のレイアウトで異なる。`--preview`でバッチ処理前にテスト推奨
- OCRはGemini APIを呼び出し。APIレート制限に注意
- 日本語テキストが主対象
