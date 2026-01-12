"""スクリーンショット処理モジュール"""

import time
from pathlib import Path
from typing import Optional, Tuple

import pyautogui

from .config import DEFAULT_OUTPUT_DIR, DEFAULT_PAGE_DELAY, FILENAME_PATTERN


def ensure_output_folder(output_dir: Path) -> Path:
    """出力フォルダを作成する

    Args:
        output_dir: 出力ディレクトリパス

    Returns:
        作成されたディレクトリパス
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def generate_filename(page_number: int) -> str:
    """連番ファイル名を生成する

    Args:
        page_number: ページ番号（1から始まる）

    Returns:
        ファイル名（例: 001.png）
    """
    return FILENAME_PATTERN.format(page_number)


def take_screenshot(
    output_dir: Path,
    page_number: int,
    region: Optional[Tuple[int, int, int, int]] = None,
) -> Path:
    """スクリーンショットを撮影して保存する

    Args:
        output_dir: 出力ディレクトリ
        page_number: ページ番号
        region: キャプチャ領域 (left, top, width, height)、Noneの場合は全画面

    Returns:
        保存されたファイルパス
    """
    filename = generate_filename(page_number)
    filepath = output_dir / filename

    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(filepath)

    return filepath


def navigate_to_next_page() -> None:
    """右矢印キーでページを送る"""
    pyautogui.press("right")


def capture_pages(
    page_count: int,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    page_delay: float = DEFAULT_PAGE_DELAY,
    region: Optional[Tuple[int, int, int, int]] = None,
) -> int:
    """複数ページをキャプチャする

    Args:
        page_count: キャプチャするページ数
        output_dir: 出力ディレクトリ
        page_delay: ページ間の待機時間（秒）
        region: キャプチャ領域、Noneの場合は全画面

    Returns:
        キャプチャしたページ数
    """
    ensure_output_folder(output_dir)

    for page_number in range(1, page_count + 1):
        filepath = take_screenshot(output_dir, page_number, region)
        print(f"Captured: {filepath}")

        if page_number < page_count:
            navigate_to_next_page()
            time.sleep(page_delay)

    return page_count
