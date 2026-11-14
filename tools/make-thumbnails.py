"""Create optimized copies of post banners.

For every image in assets/BannerImages, writes to assets/BannerImages/thumbs/:
  <name>-480.webp, <name>-960.webp  16:9 crops from the top, for the home page
  <name>-1280.jpg                   full banner for post pages and link previews
and records each banner's optimized path and size in _data/banner_images.json
(used by _plugins/seo-tweaks.rb). Files newer than their source are skipped.

Usage: python tools/make-thumbnails.py
"""

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "BannerImages"
THUMB_DIR = SOURCE_DIR / "thumbs"
DATA_FILE = ROOT / "_data" / "banner_images.json"
THUMB_WIDTHS = (480, 960)
BANNER_WIDTH = 1280
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


def is_fresh(path: Path, source_mtime: float) -> bool:
    return path.exists() and path.stat().st_mtime >= source_mtime


def main() -> None:
    THUMB_DIR.mkdir(exist_ok=True)
    written = 0
    manifest = {}
    for source in sorted(SOURCE_DIR.iterdir()):
        if not source.is_file() or source.suffix.lower() not in EXTENSIONS:
            continue
        thumbs = {w: THUMB_DIR / f"{source.stem}-{w}.webp" for w in THUMB_WIDTHS}
        banner = THUMB_DIR / f"{source.stem}-{BANNER_WIDTH}.jpg"
        source_mtime = source.stat().st_mtime

        if not all(is_fresh(p, source_mtime) for p in [*thumbs.values(), banner]):
            with Image.open(source) as image:
                rgb = image.convert("RGB")
                cropped = crop_to_aspect(rgb)
                for width, path in thumbs.items():
                    cropped.resize((width, round(width / ASPECT)), Image.LANCZOS).save(
                        path, "WEBP", quality=78, method=6
                    )
                    written += 1
                width = min(BANNER_WIDTH, rgb.width)
                height = round(rgb.height * width / rgb.width)
                rgb.resize((width, height), Image.LANCZOS).save(
                    banner, "JPEG", quality=82, optimize=True, progressive=True
                )
                written += 1

        with Image.open(banner) as optimized:
            manifest[source.stem] = {
                "path": f"/assets/BannerImages/thumbs/{banner.name}",
                "width": optimized.width,
                "height": optimized.height,
            }

    DATA_FILE.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Files written: {written}; banners listed in {DATA_FILE.relative_to(ROOT)}: {len(manifest)}")


if __name__ == "__main__":
    main()
