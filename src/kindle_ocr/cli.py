"""CLIインターフェースモジュール"""

import argparse
import sys
from pathlib import Path

from .config import (
    DEFAULT_DELAY,
    DEFAULT_INPUT_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PROMPT,
)
from .ocr import preview_ocr, process_all_images


def parse_args(args=None) -> argparse.Namespace:
    """コマンドライン引数を解析する"""
    parser = argparse.ArgumentParser(
        prog="kindle-ocr",
        description="Gemini APIを使って画像からテキストを抽出する",
    )

    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"入力ディレクトリ（デフォルト: {DEFAULT_INPUT_DIR}）",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"出力ディレクトリ（デフォルト: {DEFAULT_OUTPUT_DIR}）",
    )

    parser.add_argument(
        "--prompt",
        type=str,
        default=DEFAULT_PROMPT,
        help="Geminiへのプロンプト",
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=DEFAULT_DELAY,
        help=f"リクエスト間隔（秒）（デフォルト: {DEFAULT_DELAY}）",
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="プレビューモード（1枚目のみ処理して結果を表示）",
    )

    return parser.parse_args(args)


def main(args=None) -> int:
    """メインエントリポイント"""
    parsed_args = parse_args(args)

    try:
        if parsed_args.preview:
            print("プレビューモード")
            preview_ocr(parsed_args.input, parsed_args.prompt)
            return 0

        print(f"入力: {parsed_args.input.resolve()}")
        print(f"出力: {parsed_args.output.resolve()}")
        print(f"リクエスト間隔: {parsed_args.delay}秒")
        print()

        processed_count = process_all_images(
            input_dir=parsed_args.input,
            output_dir=parsed_args.output,
            prompt=parsed_args.prompt,
            delay=parsed_args.delay,
        )

        print()
        print(f"完了: {processed_count}枚の画像を処理しました。")
        return 0

    except FileNotFoundError as e:
        print(f"エラー: {e}")
        return 1
    except ValueError as e:
        print(f"エラー: {e}")
        return 1
    except Exception as e:
        print(f"予期しないエラー: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
