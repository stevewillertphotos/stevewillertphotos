#!/usr/bin/env python3
"""
Web Image Optimizer
Compresses all images in the /images folder for fast web loading.
Uses macOS sips — no extra installs needed.

Run from the project root:
    python3 optimize_images.py
"""
import subprocess
from pathlib import Path

MAX_DIM   = 1920   # Max width or height in pixels (great for retina screens)
JPEG_QUAL = 85     # JPEG quality — visually lossless, much smaller file size
IMAGES_DIR = Path("images")
SKIP_EXTS  = {'.arw', '.raw', '.cr2', '.nef', '.dng'}  # Skip raw files

def fmt(b):
    return f"{b/1024/1024:.1f}MB" if b > 1024*1024 else f"{b/1024:.0f}KB"

def optimize(path):
    ext = path.suffix.lower()
    if ext in SKIP_EXTS:
        return
    if ext not in {'.jpg', '.jpeg', '.png', '.webp'}:
        return

    before = path.stat().st_size

    if ext in {'.jpg', '.jpeg'}:
        cmd = ['sips', '-Z', str(MAX_DIM),
               '--setProperty', 'formatOptions', str(JPEG_QUAL),
               str(path)]
    else:
        # PNG / WebP — resize only (lossless formats)
        cmd = ['sips', '-Z', str(MAX_DIM), str(path)]

    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"  WARN: {path.name} — {result.stderr.decode().strip()}")
        return

    after = path.stat().st_size
    saved = (before - after) / before * 100 if before > 0 else 0
    print(f"  {path.relative_to(IMAGES_DIR)}: {fmt(before)} → {fmt(after)}  ({saved:.0f}% smaller)")
    return before, after


if __name__ == "__main__":
    print("=" * 60)
    print("SW Photos — Web Image Optimizer")
    print("=" * 60)
    print(f"  Max dimension : {MAX_DIM}px")
    print(f"  JPEG quality  : {JPEG_QUAL}")
    print()

    if not IMAGES_DIR.exists():
        print("ERROR: 'images/' folder not found. Run from project root.")
        exit(1)

    total_before = 0
    total_after  = 0
    count        = 0

    for img in sorted(IMAGES_DIR.rglob("*")):
        if img.is_file() and img.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}:
            result = optimize(img)
            if result:
                total_before += result[0]
                total_after  += result[1]
                count += 1

    print()
    print("=" * 60)
    print(f"  {count} images processed")
    if total_before > 0:
        print(f"  Total size: {fmt(total_before)} → {fmt(total_after)}  "
              f"({(total_before - total_after)/total_before*100:.0f}% smaller)")
    print("=" * 60)
    print()
    print("Next: commit the compressed images and push")
    print("  git add images/")
    print("  git commit -m 'Compress all images for web'")
    print("  git push")
    print()
    print("TIP: Keep your originals backed up outside this folder!")
