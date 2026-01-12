"""CLIインターフェースモジュール"""

import argparse
import sys
from pathlib import Path

from .config import (
    DEFAULT_INPUT_DIR,
    DEFAULT_MARGIN_BOTTOM,
    DEFAULT_MARGIN_LEFT,
    DEFAULT_MARGIN_RIGHT,
    DEFAULT_MARGIN_TOP,
    DEFAULT_OUTPUT_DIR,
)
from .crop import CropMargins, preview_crop, process_all_images


def parse_args(args=None) -> argparse.Namespace:
    """コマンドライン引数を解析する"""
    parser = argparse.ArgumentParser(
        prog="kindle-crop",
        description="Kindleスクリーンショットから余白をクロップする",
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
        "--top",
        type=int,
        default=DEFAULT_MARGIN_TOP,
        help=f"上部カット量（px）（デフォルト: {DEFAULT_MARGIN_TOP}）",
    )

    parser.add_argument(
        "--bottom",
        type=int,
        default=DEFAULT_MARGIN_BOTTOM,
        help=f"下部カット量（px）（デフォルト: {DEFAULT_MARGIN_BOTTOM}）",
    )

    parser.add_argument(
        "--left",
        type=int,
        default=DEFAULT_MARGIN_LEFT,
        help=f"左部カット量（px）（デフォルト: {DEFAULT_MARGIN_LEFT}）",
    )

    parser.add_argument(
        "--right",
        type=int,
        default=DEFAULT_MARGIN_RIGHT,
        help=f"右部カット量（px）（デフォルト: {DEFAULT_MARGIN_RIGHT}）",
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="プレビューモード（1枚目をクロップして表示のみ）",
    )

    return parser.parse_args(args)


def main(args=None) -> int:
    """メインエントリポイント"""
    parsed_args = parse_args(args)

    margins = CropMargins(
        top=parsed_args.top,
        bottom=parsed_args.bottom,
        left=parsed_args.left,
        right=parsed_args.right,
    )

    try:
        if parsed_args.preview:
            print("プレビューモード")
            preview_crop(parsed_args.input, margins)
            return 0

        print(f"入力: {parsed_args.input.resolve()}")
        print(f"出力: {parsed_args.output.resolve()}")
        print(f"マージン: 上={margins.top}, 下={margins.bottom}, 左={margins.left}, 右={margins.right}")
        print()

        processed_count = process_all_images(
            input_dir=parsed_args.input,
            output_dir=parsed_args.output,
            margins=margins,
        )

        print()
        print(f"完了: {processed_count}枚の画像をクロップしました。")
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
