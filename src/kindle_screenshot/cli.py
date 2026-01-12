"""CLIインターフェースモジュール"""

import argparse
import sys
import time
from pathlib import Path

from .capture import capture_pages
from .config import DEFAULT_INITIAL_DELAY, DEFAULT_OUTPUT_DIR, DEFAULT_PAGE_DELAY
from .window import activate_kindle_window, find_kindle_window, get_kindle_window_region


def parse_args(args=None) -> argparse.Namespace:
    """コマンドライン引数を解析する"""
    parser = argparse.ArgumentParser(
        prog="kindle-screenshot",
        description="Kindleアプリのページを自動でスクリーンショットし、連番で保存する",
    )

    parser.add_argument(
        "page_count",
        type=int,
        help="キャプチャするページ数",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"出力ディレクトリ（デフォルト: {DEFAULT_OUTPUT_DIR}）",
    )

    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=DEFAULT_PAGE_DELAY,
        help=f"ページ間の待機時間（秒）（デフォルト: {DEFAULT_PAGE_DELAY}）",
    )

    parser.add_argument(
        "--initial-delay",
        type=float,
        default=DEFAULT_INITIAL_DELAY,
        help=f"開始前の待機時間（秒）（デフォルト: {DEFAULT_INITIAL_DELAY}）",
    )

    parser.add_argument(
        "--full-screen",
        action="store_true",
        help="全画面キャプチャ（Kindleウィンドウ領域を無視）",
    )

    return parser.parse_args(args)


def main(args=None) -> int:
    """メインエントリポイント"""
    parsed_args = parse_args(args)

    # Kindleウィンドウを検索
    kindle_window = find_kindle_window()
    if kindle_window is None:
        print("エラー: Kindleウィンドウが見つかりません。")
        print("Kindleアプリを開いてから再実行してください。")
        return 1

    # ウィンドウをアクティブ化
    if not activate_kindle_window(kindle_window):
        print("警告: Kindleウィンドウのアクティブ化に失敗しました。")

    # キャプチャ領域を決定
    region = None if parsed_args.full_screen else get_kindle_window_region(kindle_window)

    # 開始前待機
    print(f"Kindleウィンドウを検出しました: {kindle_window.title}")
    print(f"{parsed_args.initial_delay}秒後にキャプチャを開始します...")
    print("緊急停止: マウスを画面左上(0,0)に移動")
    time.sleep(parsed_args.initial_delay)

    # キャプチャ実行
    print(f"{parsed_args.page_count}ページのキャプチャを開始します...")
    try:
        captured_count = capture_pages(
            page_count=parsed_args.page_count,
            output_dir=parsed_args.output,
            page_delay=parsed_args.delay,
            region=region,
        )
        print(f"完了: {captured_count}ページをキャプチャしました。")
        print(f"出力先: {parsed_args.output.resolve()}")
        return 0
    except Exception as e:
        print(f"エラー: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
