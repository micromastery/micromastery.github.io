"""Create lightweight WebP thumbnails of post banners for the home page.

For every image in assets/BannerImages, writes
assets/BannerImages/thumbs/<name>-480.webp and <name>-960.webp,
cropped to 16:9 from the top (banner headlines sit at the top).
Thumbnails that are already newer than their source are skipped.

Usage: python tools/make-thumbnails.py
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "BannerImages"
THUMB_DIR = SOURCE_DIR / "thumbs"
WIDTHS = (480, 960)
ASPECT = 16 / 9
EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def crop_to_aspect(image: Image.Image) -> Image.Image:
    width, height = image.size
    target_height = round(width / ASPECT)
    if target_height <= height:
        return image.crop((0, 0, width, target_height))
    target_width = round(height * ASPECT)
    left = (width - target_width) // 2
    return image.crop((left, 0, left + target_width, height))


def main() -> None:
    THUMB_DIR.mkdir(exist_ok=True)
    created = 0
    for source in sorted(SOURCE_DIR.iterdir()):
        if not source.is_file() or source.suffix.lower() not in EXTENSIONS:
            continue
        outputs = {w: THUMB_DIR / f"{source.stem}-{w}.webp" for w in WIDTHS}
        source_mtime = source.stat().st_mtime
        if all(p.exists() and p.stat().st_mtime >= source_mtime for p in outputs.values()):
            continue
        with Image.open(source) as image:
            cropped = crop_to_aspect(image.convert("RGB"))
            for width, path in outputs.items():
                height = round(width / ASPECT)
                cropped.resize((width, height), Image.LANCZOS).save(path, "WEBP", quality=78, method=6)
                created += 1
    print(f"Thumbnails written: {created}")


if __name__ == "__main__":
    main()
