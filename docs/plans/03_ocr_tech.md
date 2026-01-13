# Kindle OCR - 技術選定

## 概要
クロップ済み画像からテキストを抽出するためのOCR技術の選定。

## 要件
- 日本語テキストの高精度な認識
- 400枚程度の画像をバッチ処理
- コスト：できるだけ低コスト（無料枠活用）
- 実装の容易さ：Python から呼び出しやすい

## 技術比較

| 項目 | Claude Code CLI | Gemini CLI | Gemini API (2.0 Flash) | Google Apps Script | Document AI |
|------|-----------------|------------|------------------------|-------------------|-------------|
| 中身の技術 | VLM (Claude) | VLM | VLM (Transformer) | 従来型OCR + ヒューリスティック | Hybrid AI (OCR + 文書構造解析) |
| 本(400枚)への適性 | ○ | ? | ★ 最適 | ◎ (工夫必要) | △ オーバースペック |
| 実装の容易さ | 低 (subprocess) | 低 (subprocess) | 低〜中 (Python SDK) | 中 (JS + Drive権限) | 高 (GCP設定複雑) |
| 1枚あたり速度 | 2〜5秒? | ? | 1〜3秒 | 10〜15秒 | 2〜5秒 |
| コスト (400枚) | 有料 | 無料? | ほぼ0円 (無料枠内) | 0円 | 有料 (1,000円〜) |
| 日本語OCR精度 | ○ | ◎ | ◎ | ○ | ◎ |
| 備考 | コーディング向き | 画像非対応 | 画像認識に強い | 遅い | 定型書類向け |

## 選定履歴

### 2025-01: Claude Code CLI（保留）

**検討内容:**
```bash
claude -p "この画像のテキストを抽出してください" --files image.png
```

Claude Code は `-p` オプションで非対話的に実行でき、画像も渡せる。

**保留理由:**
- Claude はコーディング・推論は得意だが、OCR（画像からのテキスト抽出）は Google の方が強い
- Gemini は画像認識に特化した学習がされており、日本語OCRの精度が高いと判断
- 将来的に精度比較して再検討の余地あり

### 2025-01: Gemini CLI（断念）

**当初の想定:**
```bash
gemini --media "image.png" "この画像のテキストを抽出してください"
```

**結果:** 断念

1. **`--media` オプションは存在しなかった（LLMのハルシネーション）**
   ```
   PS> gemini --media
   Unknown argument: media
   Usage: gemini [options] [command]
   ```
   AIに相談した際に提案されたコマンドだったが、実際には存在しないオプションだった。

2. **Gemini CLI は画像認識に非対応？**
   - Gemini CLI は対話型AIチャット用であり、画像入力（マルチモーダル）には現時点で対応していない？
   - 参考:
     - https://github.com/google-gemini/gemini-cli/issues/11294
     - https://github.com/google-gemini/gemini-cli/issues/12867
     - https://github.com/google-gemini/gemini-cli/issues/2997

### 2025-01: Gemini API (2.0 Flash)（検証後に変更）

**当初の理由:**
- `google-generativeai` Python SDK で画像入力が可能
- 高速（1〜3秒/枚）かつ無料枠で十分
- 日本語の文脈理解が優秀
- 実装がシンプル（API キー設定 + 数行のコード）

**検証結果:** → Gemini 3.0 Flash Preview に変更

1. **Gemini 2.0 Flash / 1.5 の精度問題**
   - 段落が前後する（順序がおかしい）
   - 文章の抜けが発生する
   - 書籍のOCRには精度が不十分

2. **Gemini 3.0 Flash Preview で大幅改善**
   - 段落の順序が正確
   - テキスト抽出の精度が高い
   - 日本語書籍のOCRに十分な品質

3. **SDK の変更: `google-generativeai` → `google-genai`**
   - `google-generativeai` は古いSDK
   - 新しい `google-genai` (v1.57.0+) を採用
   - より安定したAPI呼び出しが可能

**最終採用:** Gemini 3.0 Flash Preview + `google-genai` SDK

**実装:** → `03_ocr_impl.md` 参照

## 代替案（未検証）

もし Gemini API がうまくいかない場合の候補：

### Google Apps Script (GAS)
- Google Drive の OCR 機能を利用
- 完全無料だが、実装に工夫が必要（Drive API経由）
- 速度が遅い（10〜15秒/枚）

### Claude API (Vision)
- Anthropic の Claude で画像認識
- 高精度だが、Gemini より高コスト

※ ローカルOCR（pytesseract, easyocr 等）は候補外。縦書き/横書き、レイアウト解析が必要で、精度が掛け算になることから最終的な精度が VLM に劣ると判断したため。
