#!/usr/bin/env python3
"""Resize a folder of card images to The Game Crafter's exact Tarot Deck face
size: 900x1500 px. Cover-fit (scale to fill, center-crop) so there are no bars;
the crop only touches the bleed/border margin. Outputs alongside as <folder>-tgc/.

Usage:  python scripts/resize_for_tgc.py print/decks/golden-dawn-book-t-tarot
"""
import os, sys, glob
from PIL import Image

TARGET = (900, 1500)

def main():
    if len(sys.argv) < 2:
        print("usage: python scripts/resize_for_tgc.py <folder>"); return
    src = os.path.abspath(sys.argv[1])
    out = src.rstrip("/\\") + "-tgc"
    os.makedirs(out, exist_ok=True)
    files = sorted(glob.glob(os.path.join(src, "*.jpg")) + glob.glob(os.path.join(src, "*.png")))
    n = 0
    tw, th = TARGET
    for f in files:
        im = Image.open(f).convert("RGB")
        w, h = im.size
        scale = max(tw / w, th / h)                 # cover
        nw, nh = round(w * scale), round(h * scale)
        im = im.resize((nw, nh), Image.LANCZOS)
        left = (nw - tw) // 2
        top = (nh - th) // 2
        im = im.crop((left, top, left + tw, top + th))   # center-crop to exactly 900x1500
        base = os.path.splitext(os.path.basename(f))[0]
        im.save(os.path.join(out, base + ".jpg"), "JPEG", quality=92)
        n += 1
    print(f"{n} images -> {out} (all exactly {tw}x{th})")

if __name__ == "__main__":
    main()
