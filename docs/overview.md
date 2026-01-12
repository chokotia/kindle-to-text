# Kindle to Text - プロジェクト概要

## 目的
Kindleの内容をテキストデータに変換する

## 全体フロー

```
Phase 1: スクリーンショット取得
Kindleアプリ → 自動スクショ → output/raw/ (画面全体のPNG)

Phase 2: クロップ処理
output/raw/ → 不要部分除去 → output/cropped/ (本文のみのPNG)

Phase 3: OCR処理
output/cropped/ → OCR → output/text/ (テキストファイル)

Phase 4: 章ごと結合
output/text/ + chapters.yaml → output/chapters/ (章ごとのテキスト)
```

## フェーズ構成

| Phase | 内容 | 状態 | 計画書 |
|-------|------|------|--------|
| 1 | スクリーンショット自動取得 | 実装予定 | [01_screenshot.md](plans/01_screenshot.md) |
| 2 | クロップ処理 | 未着手 | [02_crop.md](plans/02_crop.md) |
| 3 | OCR処理 | 未着手 | [03_ocr.md](plans/03_ocr.md) |
| 4 | 章ごとテキスト結合 | 未着手 | [04_merge.md](plans/04_merge.md) |

## 採用技術

### Phase 1: スクリーンショット
- **言語**: Python 3.10+
- **パッケージ管理**: Poetry
- **主要ライブラリ**:
  - pyautogui (GUI自動化)
  - Pillow (画像処理)
  - pygetwindow (ウィンドウ管理)

### Phase 2: クロップ処理 (予定)
- Pillow (画像処理)

### Phase 3: OCR (予定)
- **Gemini CLI** (マルチモーダルAIによるテキスト抽出)
- 高精度な日本語認識、文脈理解が可能

### Phase 4: 章ごと結合 (予定)
- PyYAML (設定ファイル読み込み)
- 設定ファイル: `chapters.yaml`

## 技術選定の経緯

5つの選択肢を比較検討し、**Python + pyautogui + Pillow** を採用。

| 項目 | pyautogui | pywinauto | AutoHotkey | PowerShell | nutjs |
|------|-----------|-----------|------------|------------|-------|
| セットアップ | 簡単 | 簡単 | 簡単 | 不要 | やや面倒 |
| 学習コスト | 低 | 中 | 中 | 中 | 中 |
| スクショ機能 | ◎ | ○ | △ | ○ | ○ |
| OCR連携 | ◎ | ◎ | △ | △ | △ |

**採用理由**:
1. セットアップが最も簡単
2. コードがシンプルで理解しやすい
3. Phase 2 (OCR) もPythonで継続できる
4. ドキュメントとサンプルが豊富

## 出力構成

```
output/
├── raw/           # Phase 1: 画面全体のスクリーンショット
│   ├── 001.png
│   ├── 002.png
│   └── ...
├── cropped/       # Phase 2: 不要部分を除去した画像
│   ├── 001.png
│   ├── 002.png
│   └── ...
├── text/          # Phase 3: OCR結果のテキスト
│   ├── 001.txt
│   ├── 002.txt
│   └── ...
└── chapters/      # Phase 4: 章ごとに結合したテキスト
    ├── 01_はじめに.txt
    ├── 02_基礎編.txt
    └── ...
```

**ファイル命名規則**: 連番3桁（001, 002, ...）で統一。各フェーズで同じ番号が対応する。

## 環境
- OS: Windows
- Kindleアプリ: インストール済み
- 保存先: ローカル (必要に応じて手動でGoogle Driveへ)
