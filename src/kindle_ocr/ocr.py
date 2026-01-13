"""OCR処理モジュール - Gemini APIを使用したテキスト抽出"""

import os
import time
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

from .config import (
    DEFAULT_DELAY,
    DEFAULT_PROMPT,
    ENV_API_KEY,
    INPUT_PATTERN,
    MODEL_NAME,
    OUTPUT_TEMPLATE,
)


def get_client() -> genai.Client:
    """環境変数からGemini APIクライアントを取得する"""
    api_key = os.environ.get(ENV_API_KEY)
    if not api_key:
        raise ValueError(f"環境変数 {ENV_API_KEY} が設定されていません")
    return genai.Client(api_key=api_key)


def extract_text_from_image(client: genai.Client, image_path: Path, prompt: str) -> str:
    """画像からテキストを抽出する

    Args:
        client: Gemini APIクライアント
        image_path: 画像ファイルのパス
        prompt: Geminiへのプロンプト

    Returns:
        抽出されたテキスト
    """
    image = Image.open(image_path)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[prompt, image]
    )
    return response.text


def save_text(text: str, output_path: Path) -> None:
    """テキストをファイルに保存する

    Args:
        text: 保存するテキスト
        output_path: 出力ファイルのパス
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")


def get_image_files(input_dir: Path) -> list[Path]:
    """入力ディレクトリから画像ファイルを取得する

    Args:
        input_dir: 入力ディレクトリ

    Returns:
        ソートされた画像ファイルのリスト
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"入力ディレクトリが見つかりません: {input_dir}")

    files = sorted(input_dir.glob(INPUT_PATTERN))
    if not files:
        raise FileNotFoundError(f"画像ファイルが見つかりません: {input_dir}/{INPUT_PATTERN}")

    return files


def process_all_images(
    input_dir: Path,
    output_dir: Path,
    prompt: str = DEFAULT_PROMPT,
    delay: float = DEFAULT_DELAY,
) -> int:
    """すべての画像をバッチ処理する

    Args:
        input_dir: 入力ディレクトリ
        output_dir: 出力ディレクトリ
        prompt: Geminiへのプロンプト
        delay: リクエスト間隔（秒）

    Returns:
        処理した画像の数
    """
    client = get_client()
    image_files = get_image_files(input_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    processed_count = 0
    total = len(image_files)

    for i, image_path in enumerate(image_files, start=1):
        print(f"[{i}/{total}] {image_path.name} を処理中...")

        try:
            text = extract_text_from_image(client, image_path, prompt)
            output_path = output_dir / OUTPUT_TEMPLATE.format(i)
            save_text(text, output_path)
            processed_count += 1
            print(f"  -> {output_path.name} に保存しました")

        except Exception as e:
            print(f"  エラー: {e}")
            continue

        # レート制限対策
        if i < total:
            time.sleep(delay)

    return processed_count


def preview_ocr(input_dir: Path, prompt: str = DEFAULT_PROMPT) -> None:
    """プレビューモード - 1枚目の画像のみ処理して結果を表示する

    Args:
        input_dir: 入力ディレクトリ
        prompt: Geminiへのプロンプト
    """
    client = get_client()
    image_files = get_image_files(input_dir)
    first_image = image_files[0]

    print(f"画像: {first_image}")
    print(f"プロンプト: {prompt[:50]}...")
    print()
    print("--- OCR結果 ---")

    text = extract_text_from_image(client, first_image, prompt)
    print(text)
    print("--- 終了 ---")
