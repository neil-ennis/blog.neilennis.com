"""Restore referenced 2020/02 thumbnails omitted by a Staatic export.

Usage: python scripts/restore_legacy_thumbnails.py PATH_TO_WORDPRESS_UPLOADS
Run after replacing site/ with a new reviewed export and before publishing.
"""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import argparse
import re
import shutil


SITE = Path(__file__).resolve().parents[1] / "site"
URL = re.compile(
    rb"https://blog\.neilennis\.com/wp-content/uploads/2020/02/"
    rb"([0-9a-f]{32}(?:-\d+)?\.jpg)"
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("uploads", type=Path, help="Local WordPress wp-content/uploads folder")
    parser.add_argument("--apply", action="store_true", help="Copy missing files (default: dry run)")
    args = parser.parse_args()
    source_dir = args.uploads / "2020" / "02"
    target_dir = SITE / "wp-content" / "uploads" / "2020" / "02"
    if not source_dir.is_dir() or not SITE.is_dir():
        parser.error("WordPress uploads source or static site folder is absent")

    names: set[str] = set()
    for page in SITE.rglob("*.html"):
        names.update(name.decode("ascii") for name in URL.findall(page.read_bytes()))

    missing = sorted(name for name in names if not (target_dir / name).is_file())
    total_bytes = 0
    for name in missing:
        source = source_dir / name
        if not source.is_file():
            raise FileNotFoundError(f"Referenced thumbnail missing from WordPress: {source}")
        data = source.read_bytes()
        if not data.startswith(b"\xff\xd8\xff") or not data.endswith(b"\xff\xd9"):
            raise ValueError(f"Invalid JPEG: {source}")
        total_bytes += len(data)
    print(f"Referenced: {len(names)}; missing in static export: {len(missing)}; bytes to copy: {total_bytes}")

    if not args.apply:
        return
    target_dir.mkdir(parents=True, exist_ok=True)
    for name in missing:
        source = source_dir / name
        target = target_dir / name
        shutil.copyfile(source, target)
        if sha256(source.read_bytes()).digest() != sha256(target.read_bytes()).digest():
            raise IOError(f"Copy verification failed: {target}")


if __name__ == "__main__":
    main()
