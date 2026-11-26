"""Corrections by script in round 3 of the Oct 27 2026 Book T repaint.

Round 3 (docs/research/BOOK-T-PAINTED-CHECK-2026-10-21.md, "Oct 27 review, round 3"; tarot/book-t/PROMPTS.md,
"Round 3") fixed the Eight of Wands' count and the Ten of Pentacles' roses. As in round 2
(scripts/fix_book_t_repaint_2026_10_27.py) and the first run (fixrays.py, splitface.py), nothing new
is drawn: the painting's own strokes are copied.

* wands-08: Book T, "eight wands, crossed four with four". The round-2 painting has three and three.
  Its outer wand is swept along a parallel line outside each fan (behind the hands, the flames and
  the other wands; over the clouds, as the painted wands are), giving four and four. That composite
  was then the reference picture of a Nano Banana Pro painting, which kept the eight and is the kept
  picture; the composite itself is on the CDN too (see COMPOSITE below).
* pentacles-10: Book T, "a branch whose roses touch all the Pentacles". The round-3 painting (Nano
  Banana Pro) has a rose at eight of its ten discs; two of its own roses, floating near the two
  central discs, are moved onto their rims, and the ground where they were is filled from the
  painted green around it.

    python scripts/fix_book_t_repaint_round3_2026_10_27.py OUT_DIR

fetches the two source paintings (curl) and writes wands-08-composite.png and pentacles-10.png to OUT_DIR.
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageFilter

CDN = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/'
SOURCE = {
    'wands-08': CDN + 'flow-image-gen/1793138397263-o5altmksjw.png',      # round 2, attempt 2 (3 + 3)
    'pentacles-10': CDN + 'flow-image-gen/1793142500069-lugroo6ne1.png',  # round 3, attempt 1
}
COMPOSITE = CDN + 'grammars/1793142297354-tpzipu9n5sf.png'  # the wands-08 composite, as uploaded


def dilate(mask, size):
    return np.asarray(Image.fromarray(mask.astype(np.uint8) * 255).filter(ImageFilter.MaxFilter(size))) > 0


def fix_wands_08(img):
    a = np.asarray(img).astype(float)
    H, W, _ = a.shape
    out = a.copy()
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.3 * R + 0.59 * G + 0.11 * B
    yy, xx = np.mgrid[0:H, 0:W]

    P0 = np.array([115.0, 250.0])                      # the outer '\' wand's axis passes here
    d = np.array([0.6457, 1.0]); d /= np.linalg.norm(d)
    n = np.array([d[1], -d[0]])
    CX = 424.0                                         # the picture's mirror axis

    # what stays in front of the new wands: the other wands, the flames, the ink, the hands
    wood = (R > G + 45) & (B < G + 15) & (lum < 205) & ((yy < 950) | (R > G + 60))
    flame = (R > 215) & (G > 150) & (B < 150) & (yy < 720)
    ink = (lum < 75) & ~((B > R + 40) & (yy >= 900)) & (((yy >= 480) & (xx > 250) & (xx < 600)) | (B < R + 10))
    hand = (lum > 195) & ((R - G) < 13) & (B > 215) & (yy > 470) & (yy < 900)
    hand |= (B > R + 40) & (lum < 190) & (yy > 470) & (yy < 900) & (xx > 250) & (xx < 600)
    hand = dilate(hand, 5) & ~((lum > 190) & ((R - G) >= 13) & (B < 215))
    protect = wood | flame | ink | hand

    TOP = np.array([70.0, 285.0])                      # the new '\' wand's upper tip
    L = (1168.0 - TOP[1]) / d[1]                       # ... its lower tip at y = 1168
    HW = 21.0                                          # half its width

    def bilinear(x, y):
        x = np.clip(x, 0, W - 1.001); y = np.clip(y, 0, H - 1.001)
        x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int)
        fx = (x - x0)[..., None]; fy = (y - y0)[..., None]
        return (a[y0, x0] * (1 - fx) * (1 - fy) + a[y0, x0 + 1] * fx * (1 - fy)
                + a[y0 + 1, x0] * (1 - fx) * fy + a[y0 + 1, x0 + 1] * fx * fy)

    def source_u(u):
        """new wand's u (0 = upper tip .. L = lower tip) -> the source wand's u: its upper tip for both
        ends, its clean stretch above the clouds (u -60..140) back and forth in between."""
        us = np.empty_like(u)
        top, bot = u < 35, u > L - 35
        us[top] = -95 + u[top]
        us[bot] = -95 + (L - u[bot])
        k = np.mod(u[~top & ~bot] - 35, 400.0)
        us[~top & ~bot] = -60 + np.where(k < 200, k, 400 - k)
        return us

    for mirror in (False, True):
        X = xx.astype(float)
        if mirror:
            X = 2 * CX - X
        rx, ry = X - TOP[0], yy - TOP[1]
        u = rx * d[0] + ry * d[1]
        v = rx * n[0] + ry * n[1]
        band = (u >= 0) & (u <= L) & (np.abs(v) <= HW + 6)
        uu, vv = u[band], v[band]
        vv = np.where(uu > L - 35, -vv, vv)            # the lower tip is the upper tip turned round
        sp = P0[None, :] + source_u(uu)[:, None] * d[None, :] + vv[:, None] * n[None, :]
        col = bilinear(sp[:, 0], sp[:, 1])
        ground = (col[:, 0] > 215) & (col[:, 1] > 195) & (col[:, 2] > 160)
        by, bx = yy[band], xx[band]
        keep = (np.abs(vv) <= HW) & ~ground & ~protect[by, bx]
        out[by[keep], bx[keep]] = col[keep]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8))


def fix_pentacles_10(img):
    im = np.asarray(img).astype(int)
    H, W, _ = im.shape
    yy, xx = np.mgrid[0:H, 0:W]
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    green = (G > R + 40) & (G > B + 20)
    white = (R > 200) & (G > 200) & (B > 200)
    leaf = (R > G + 10) & (0.3 * R + 0.59 * G + 0.11 * B < 120)
    out = im.copy()
    hole = np.zeros((H, W), bool)
    pasted = np.zeros((H, W), bool)
    # (rose centre, shift): onto the upper central disc's lower-right rim, the lower one's upper-right rim
    for (cx, cy), (dx, dy) in (((535, 425), (-26, -28)), ((518, 610), (-27, 45))):
        circ = (xx - cx) ** 2 + (yy - cy) ** 2 <= 62 ** 2
        rose = circ & ~green & dilate(white & circ, 9)
        ys, xs = np.nonzero(rose)
        h = dilate(rose, 7) & ~leaf
        out[h] = np.median(im[green], axis=0).astype(int)
        hole |= h
        out[ys + dy, xs + dx] = im[ys, xs]
        pasted[ys + dy, xs + dx] = True
    # fill where the roses were from the painted green around it
    f = out.astype(float)
    src = (green & ~hole) | hole
    src &= ~pasted
    upd = hole & ~pasted
    for _ in range(120):
        acc = np.zeros_like(f); cnt = np.zeros((H, W))
        for sy, sx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            acc += np.roll(np.roll(f, sy, 0), sx, 1) * np.roll(np.roll(src, sy, 0), sx, 1)[..., None]
            cnt += np.roll(np.roll(src, sy, 0), sx, 1)
        avg = acc / np.maximum(cnt, 1)[..., None]
        m = upd & (cnt > 0)
        f[m] = avg[m]
    return Image.fromarray(f.clip(0, 255).astype(np.uint8))


FIX = {'wands-08': ('wands-08-composite.png', fix_wands_08), 'pentacles-10': ('pentacles-10.png', fix_pentacles_10)}


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for card, url in SOURCE.items():
        raw = os.path.join(out, card + '-source.png')
        subprocess.run(['curl', '-sfL', '-A', 'Mozilla/5.0', '-o', raw, url], check=True)
        name, fix = FIX[card]
        fix(Image.open(raw).convert('RGB')).save(os.path.join(out, name))
        print('[fix_book_t_repaint_round3_2026_10_27] %s -> %s' % (card, os.path.join(out, name)))


if __name__ == '__main__':
    main()
