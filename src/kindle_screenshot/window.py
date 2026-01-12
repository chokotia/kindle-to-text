"""ウィンドウ管理モジュール"""

import pygetwindow as gw
from typing import Optional, Tuple

from .config import KINDLE_WINDOW_PATTERNS


def find_kindle_window() -> Optional[gw.Win32Window]:
    """Kindleウィンドウを検索する

    Returns:
        Kindleウィンドウオブジェクト、見つからない場合はNone
    """
    for pattern in KINDLE_WINDOW_PATTERNS:
        windows = gw.getWindowsWithTitle(pattern)
        if windows:
            return windows[0]
    return None


def activate_kindle_window(window: gw.Win32Window) -> bool:
    """ウィンドウをアクティブ化する

    Args:
        window: アクティブ化するウィンドウ

    Returns:
        成功した場合True
    """
    try:
        if window.isMinimized:
            window.restore()
        window.activate()
        return True
    except Exception:
        return False


def get_kindle_window_region(window: gw.Win32Window) -> Tuple[int, int, int, int]:
    """ウィンドウのスクリーンショット領域を取得する

    Args:
        window: 対象ウィンドウ

    Returns:
        (left, top, width, height) のタプル
    """
    return (window.left, window.top, window.width, window.height)
