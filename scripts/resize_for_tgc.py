#!/usr/bin/env python3
"""Resize a folder of card images to The Game Crafter's exact Tarot Deck face
size: 900x1500 px. Cover-fit (scale to fill, center-crop) so there are no bars;
the crop only touches the bleed/border margin. Outputs alongside as <folder>-tgc/.

Usage:  python scripts/resize_for_tgc.py print/decks/golden-dawn-book-t-tarot
"""
import os, sys, glob
from PIL import Image

TARGET = (900, 1500)      # TGC tarot face: 900x1500 @300dpi
# TGC trims 1/8" (37.5px) bleed per side -> cut card is 825x1425.
# Their safe zone is another ~1/8" inside the cut line -> 750x1350.
SAFE = (750, 1350)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    cover = "--cover" in sys.argv     # default is BORDER mode (safe for scans of complete cards)
    if not args:
        print("usage: python scripts/resize_for_tgc.py <folder> [--cover]"); return
    src = os.path.abspath(args[0])
    out = src.rstrip("/\\") + "-tgc"
    os.makedirs(out, exist_ok=True)
    files = sorted(glob.glob(os.path.join(src, "*.jpg")) + glob.glob(os.path.join(src, "*.png")))
    n = 0
    tw, th = TARGET
    for f in files:
        im = Image.open(f).convert("RGB")
        w, h = im.size
        if cover:
            # COVER: art fills full bleed; edges get trimmed. Only for borderless art.
            scale = max(tw / w, th / h)
            nw, nh = round(w * scale), round(h * scale)
            im = im.resize((nw, nh), Image.LANCZOS)
            left, top = (nw - tw) // 2, (nh - th) // 2
            canvas = im.crop((left, top, left + tw, top + th))
        else:
            # BORDER (default): the WHOLE original card sits inside the safe zone,
            # and the canvas is filled with the CARD'S OWN sampled border colour
            # (not white) so the added margin blends into the vintage frame with
            # no contrast line. A small inset crop first removes scanner edge junk.
            inset = max(2, round(min(w, h) * 0.012))           # ~1.2% edge shave
            im = im.crop((inset, inset, w - inset, h - inset))
            w, h = im.size
            # sample the border colour: median of a thin ring just inside the edge
            ring = max(2, round(min(w, h) * 0.02))
            px = []
            for x in range(0, w, 7):
                px += [im.getpixel((x, ring)), im.getpixel((x, h - 1 - ring))]
            for y in range(0, h, 7):
                px += [im.getpixel((ring, y)), im.getpixel((w - 1 - ring, y))]
            px.sort(key=lambda c: c[0] + c[1] + c[2])
            border_col = px[len(px) // 2]                      # median tone of the frame
            sw, sh = SAFE
            scale = min(sw / w, sh / h)
            nw, nh = round(w * scale), round(h * scale)
            im = im.resize((nw, nh), Image.LANCZOS)
            canvas = Image.new("RGB", (tw, th), border_col)
            canvas.paste(im, ((tw - nw) // 2, (th - nh) // 2))
        base = os.path.splitext(os.path.basename(f))[0]
        canvas.save(os.path.join(out, base + ".jpg"), "JPEG", quality=92)
        n += 1
    print(f"{n} images -> {out} ({'cover/full-bleed' if cover else 'bordered/safe-zone'}, all exactly {tw}x{th})")

if __name__ == "__main__":
    main()
