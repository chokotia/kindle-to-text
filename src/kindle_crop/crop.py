"""クロップ処理モジュール"""

from pathlib import Path
from typing import NamedTuple

from PIL import Image

from .config import FILENAME_PATTERN


class CropMargins(NamedTuple):
    """クロップマージン設定"""

    top: int = 0
    bottom: int = 0
    left: int = 0
    right: int = 0


def load_image(path: Path) -> Image.Image:
    """画像を読み込む"""
    return Image.open(path)


def crop_image(image: Image.Image, margins: CropMargins) -> Image.Image:
    """マージン指定で画像をクロップする

    Args:
        image: 入力画像
        margins: 上下左右のカット量（px）

    Returns:
        クロップされた画像
    """
    width, height = image.size

    left = margins.left
    top = margins.top
    right = width - margins.right
    bottom = height - margins.bottom

    if left >= right or top >= bottom:
        raise ValueError(
            f"無効なクロップ領域: マージンが大きすぎます "
            f"(画像サイズ: {width}x{height}, マージン: {margins})"
        )

    return image.crop((left, top, right, bottom))


def save_image(image: Image.Image, path: Path) -> None:
    """画像を保存する"""
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def get_image_files(input_dir: Path) -> list[Path]:
    """入力ディレクトリからPNG画像ファイルを取得する（ソート済み）"""
    if not input_dir.exists():
        raise FileNotFoundError(f"入力ディレクトリが見つかりません: {input_dir}")

    files = sorted(input_dir.glob("*.png"))
    return files


def process_all_images(
    input_dir: Path,
    output_dir: Path,
    margins: CropMargins,
) -> int:
    """全画像をバッチ処理でクロップする

    Args:
        input_dir: 入力ディレクトリ
        output_dir: 出力ディレクトリ
        margins: クロップマージン

    Returns:
        処理した画像数
    """
    files = get_image_files(input_dir)

    if not files:
        print(f"処理対象の画像が見つかりません: {input_dir}")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)

    processed_count = 0
    for i, input_path in enumerate(files, start=1):
        output_path = output_dir / FILENAME_PATTERN.format(i)

        image = load_image(input_path)
        cropped = crop_image(image, margins)
        save_image(cropped, output_path)

        print(f"処理完了: {input_path.name} -> {output_path.name}")
        processed_count += 1

    return processed_count


def preview_crop(input_dir: Path, margins: CropMargins) -> None:
    """最初の画像でクロップ結果をプレビュー表示する

    Args:
        input_dir: 入力ディレクトリ
        margins: クロップマージン
    """
    files = get_image_files(input_dir)

    if not files:
        print(f"プレビュー対象の画像が見つかりません: {input_dir}")
        return

    first_file = files[0]
    print(f"プレビュー画像: {first_file.name}")

    image = load_image(first_file)
    original_size = image.size
    print(f"元のサイズ: {original_size[0]}x{original_size[1]}")

    cropped = crop_image(image, margins)
    cropped_size = cropped.size
    print(f"クロップ後: {cropped_size[0]}x{cropped_size[1]}")
    print(f"マージン: 上={margins.top}, 下={margins.bottom}, 左={margins.left}, 右={margins.right}")

    cropped.show()
