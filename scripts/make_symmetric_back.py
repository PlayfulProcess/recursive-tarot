#!/usr/bin/env python3
"""Build a mathematically 180-degree-symmetric tarot card back at TGC print spec
(900x1500, incl bleed), from the project's own golden-ratio spiral motif
(the same r = a*e^(b*theta) formula as public/spiral/spiral.js).

Method: draw the design ONLY in the top half of the canvas (rows 0..749), then
set the bottom half = the top half rotated 180 degrees, pasted directly below.
For any pixel (x, y): full(x, y) == full(W-1-x, H-1-y) follows directly from
that construction -- it's exact point-symmetry by CONSTRUCTION, not by
symmetric-looking brushwork, so it holds regardless of what's drawn in the
top half. Verified below by rotating the finished raster 180 and diffing it
against itself (bbox must be None, extrema must be all-zero).

Output: print/backs/back-symmetric-spiral-900x1500.png (lossless master --
this is the file the symmetry claim is actually proven against) and a .jpg
sibling (used for the TGC upload; JPEG's block quantization reintroduces a
small amount of compression-only asymmetry, invisible and irrelevant to the
"can't tell if it's reversed" design goal, but the PNG is the exact artifact).

Usage: python scripts/make_symmetric_back.py
"""
import math
import os
from PIL import Image, ImageDraw, ImageChops

TW, TH = 900, 1500          # TGC tarot face/back spec, incl. 1/8" bleed
HALF = TH // 2              # 750 -- exact half, TH is even so this is lossless

INK       = (34, 31, 26)    # --ink  (theme.css)
GOLD      = (154, 115, 34)  # --gold (theme.css)
GOLD_SOFT = (120, 90, 40)
PAPER     = (244, 241, 234) # --bg (warm paper) -- used as a faint accent only

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "print", "backs")


def thick_line(draw, pts, width, fill):
    """Polyline with round joints (draw circles at vertices so joints don't gap)."""
    draw.line(pts, fill=fill, width=width, joint="curve")
    r = width / 2
    for (x, y) in pts:
        draw.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def spiral_points(cx, cy, a, b, theta_start, theta_end, steps, max_r=None):
    """Logarithmic spiral: r = a * e^(b*theta)."""
    pts = []
    for i in range(steps + 1):
        t = theta_start + (theta_end - theta_start) * i / steps
        r = a * math.exp(b * t)
        if max_r is not None:
            r = min(r, max_r)
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return pts


def build_top_half():
    """Everything drawn here lives in y in [0, HALF-1]. It gets mirrored below."""
    top = Image.new("RGB", (TW, HALF), INK)
    d = ImageDraw.Draw(top)

    # TGC safe zone is the inner 750x1350 box (centered) -> margin >= 75px from
    # the 900x1500 bleed edge. 84px keeps the frame comfortably inside it.
    mx, my = 84, 84
    fw = 7                      # frame stroke width -- well above hairline
    cx = TW / 2                 # 450 -- horizontal center of the whole card
    cy = HALF                   # 750 -- this row IS the canvas center (mirror axis)

    # Frame: three sides only (top + left/right down to the exact mid-line).
    # Mirroring completes the rectangle seamlessly -- see module docstring.
    thick_line(d, [(mx, my), (TW - mx, my)], fw, GOLD)
    thick_line(d, [(mx, my), (mx, cy)], fw, GOLD)
    thick_line(d, [(TW - mx, my), (TW - mx, cy)], fw, GOLD)

    # Inner second rule (classic double-border card-back look)
    ix, iy = mx + 16, my + 16
    thick_line(d, [(ix, iy), (TW - ix, iy)], 3, GOLD_SOFT)
    thick_line(d, [(ix, iy), (ix, cy)], 3, GOLD_SOFT)
    thick_line(d, [(TW - ix, iy), (TW - ix, cy)], 3, GOLD_SOFT)

    # Corner flourishes (top-left / top-right). Mirroring gives bottom-right /
    # bottom-left twins automatically -> four-corner symmetric ornament.
    for ox in (mx + 30, TW - mx - 30):
        fx, fy = ox, my + 30
        for k in range(3):
            rr = 6 - k * 1.6
            d.ellipse([fx - rr, fy + k * 14 - rr, fx + rr, fy + k * 14 + rr], fill=GOLD)

    # The golden spiral arm: grows from the canvas CENTER (cx, cy) outward,
    # swept across a single half-turn (theta in [-pi, 0]) so every point has
    # sin(theta) <= 0, i.e. y <= cy -- it stays entirely in the top half BY
    # CONSTRUCTION, so the mirror step can't clip it.
    r0, max_r = 5, min(cx - mx - 24, cy - my - 24)
    theta_start, theta_end = -math.pi * 0.995, -0.06 * math.pi
    b = math.log(max_r / r0) / (theta_end - theta_start)
    pts = spiral_points(cx, cy, a=r0 * math.exp(-b * theta_start), b=b,
                         theta_start=theta_start, theta_end=theta_end, steps=300)
    n = len(pts) - 1
    for i in range(n):   # tapering stroke, thin at center, thick at the tip
        w = max(3, round(3 + 7 * (i / n)))
        d.line([pts[i], pts[i + 1]], fill=GOLD, width=w, joint="curve")
    for i in range(24, n - 10, 18):   # beaded nodes along the arm
        x, y = pts[i]
        d.ellipse([x - 4.5, y - 4.5, x + 4.5, y + 4.5], fill=PAPER)
        d.ellipse([x - 2.4, y - 2.4, x + 2.4, y + 2.4], fill=GOLD)

    # Center hub: a ring sitting exactly ON the mirror axis, so its mirrored
    # copy lands exactly on top of it -- one continuous emblem at true center.
    hub_r = 22
    d.ellipse([cx - hub_r, cy - hub_r, cx + hub_r, cy + hub_r], outline=GOLD, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)

    # Background texture: restrained dot lattice (4px dots, not hairlines),
    # skipped near the spiral arm so it doesn't muddy the line.
    step = 42
    for gy in range(my + 26, HALF, step):
        for gx in range(mx + 26, TW - mx, step):
            if math.hypot(gx - cx, gy - cy) < max_r * 0.94:
                if min(math.hypot(gx - px, gy - py) for px, py in pts[::20]) < 18:
                    continue
            r = 2.2
            d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(70, 62, 48))

    return top


def main():
    top = build_top_half()
    full = Image.new("RGB", (TW, TH), INK)
    full.paste(top, (0, 0))
    full.paste(top.rotate(180), (0, HALF))

    diff = ImageChops.difference(full, full.rotate(180))
    print("symmetry check bbox (must be None):", diff.getbbox())
    print("symmetry check extrema (must be all (0,0)):", diff.getextrema())
    assert diff.getbbox() is None, "back is NOT exactly 180-symmetric -- bug"

    os.makedirs(OUT_DIR, exist_ok=True)
    png_path = os.path.join(OUT_DIR, "back-symmetric-spiral-900x1500.png")
    full.save(png_path, "PNG")
    jpg_path = os.path.join(OUT_DIR, "back-symmetric-spiral-900x1500.jpg")
    full.save(jpg_path, "JPEG", quality=96)
    print(f"saved {png_path} and {jpg_path} ({full.size[0]}x{full.size[1]})")


if __name__ == "__main__":
    main()
