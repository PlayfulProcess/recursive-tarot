"""Corrections by script in round 4 of the Book T repaint (Oct 28 2026).

Round 4 (docs/research/BOOK-T-PAINTED-CHECK-2026-10-21.md, "Round 4"; tarot/book-t/PROMPTS.md,
"Round 4") mends the small leftovers of the Oct 27 review. As in rounds 2 and 3
(scripts/fix_book_t_repaint_2026_10_27.py, scripts/fix_book_t_repaint_round3_2026_10_27.py) nothing
new is painted where a script can do it: a stray mark is filled from the painting's own ground
(a smooth fill from the pixels around it, then the ground's own grain copied back in), a symbol is
moved by copying the painting's own strokes, and the only shapes drawn are Book T's own letters,
from the deck's glyphs (tarot/book-t/glyphs/hebrew-vau.svg), in the painting's ink and gold.

* key-19-sun: the painted "FE" monogram in the lower right corner is filled with the hedge's green.
* swords-03: the words LORD OF SORROW painted in the clouds are filled with the clouds' grey.
* swords-02: the stray blade fragment at the top right is filled with the sky.
* swords-07: Book T, "The Rose ... is held up by the same hand which holds the central sword".
  The rose floating left of the central sword is moved onto that hand's fist.
* key-11-fortitude: the hanging sword's blade ran into her flower crown; it now narrows to a point
  above it (each row of the blade's own pixels, narrowed toward the tip).
* key-12-hanged-man: the rope ran on down the leg past the knot at the ankle; below the knot it is
  filled with the ground.
* wands-02 (on the round-4 painting): Book T, "two small wands ... with flames of five". The new
  painting has five flames on the upper wand and seven on the lower; the lower seven are taken off
  and five of them set back, evenly spaced over the same length.
* pentacles-princess (on the round-4 painting): Book T, her Pentacle is "similar to that of the Ace",
  whose white centre sends out "Twelve Rays". The new painting's disc has the Ace's rings and red cross
  but sixteen rays, evenly spaced. The disc between its white centre and its outer green ring is
  re-laid by rotation: each 30-degree sector takes the painting's own 22.5-degree sector (ray to
  ray), so twelve rays, evenly spaced, run from the centre to the rim, the rings unchanged.
* swords-ace: Book T, "Six Vaus fall from its point". The eight gold drops and the five gold dots
  are filled with the sky, and six Vavs (the deck's glyph, gold with an ink outline) fall in their
  place, three on each side of the blade.

    python scripts/fix_book_t_repaint_round4_2026_10_28.py OUT_DIR [card ...]

fetches the source paintings (curl) and writes <card>.png to OUT_DIR.
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

CDN = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/'
SOURCE = {
    'key-19-sun': CDN + 'flow-image-gen/1791650529996-xizbvbruo3s.png',
    'swords-03': CDN + 'flow-image-gen/1791653375363-et0z30fakwg.png',
    'swords-02': CDN + 'flow-image-gen/1791653400184-vop82hpec2a.png',
    'swords-07': CDN + 'grammars/1791669740057-qlhgchfujo.jpg',
    'key-11-fortitude': CDN + 'flow-image-gen/1791650273106-4cuhdpuzdv3.png',
    'key-12-hanged-man': CDN + 'flow-image-gen/1791666010955-w3hh98njsfb.png',
    'wands-02': CDN + 'flow-image-gen/1793160166917-d7n2xzzyhi.png',   # round 4, attempt 1 (Nano Banana 2.1)
    'swords-ace': CDN + 'flow-image-gen/1791651003941-64rakrwdnm.png',
    'pentacles-princess': CDN + 'flow-image-gen/1793159533764-cxnvmz212le.png',  # round 4, attempt 1 (2.1)
}


def box(H, W, x0, y0, x1, y1):
    m = np.zeros((H, W), bool)
    m[y0:y1, x0:x1] = True
    return m


def lum(a):
    return 0.3 * a[..., 0] + 0.59 * a[..., 1] + 0.11 * a[..., 2]


def fill(a, mask, grain_from=None, iters=600):
    """Fill `mask` smoothly from the pixels around it (Jacobi relaxation on a padded window), then
    add back the ground's grain: the fine residual of a donor patch (`grain_from` = (dx, dy), the
    same-shaped area shifted by that offset)."""
    a = a.astype(float).copy()
    ys, xs = np.nonzero(mask)
    y0, y1 = max(ys.min() - 6, 0), min(ys.max() + 7, a.shape[0])
    x0, x1 = max(xs.min() - 6, 0), min(xs.max() + 7, a.shape[1])
    w = a[y0:y1, x0:x1].copy()
    m = mask[y0:y1, x0:x1]
    known = ~m
    # start from the mean of the border ring
    ring = ndimage.binary_dilation(m, iterations=2) & known
    w[m] = w[ring].mean(axis=0)
    k = np.array([[0, .25, 0], [.25, 0, .25], [0, .25, 0]])
    for _ in range(iters):
        for c in range(3):
            sm = ndimage.convolve(w[..., c], k, mode='nearest')
            w[..., c][m] = sm[m]
    if grain_from is not None:
        dx, dy = grain_from
        donor = a[y0 + dy:y1 + dy, x0 + dx:x1 + dx]
        res = donor - ndimage.gaussian_filter(donor, sigma=(2.5, 2.5, 0))
        w[m] += res[m]
    a[y0:y1, x0:x1] = w
    return a


def fix_key_19(a):
    H, W, _ = a.shape
    m = box(H, W, 748, 1170, 796, 1218) & (lum(a) > 120)
    m = ndimage.binary_dilation(m, iterations=3) & box(H, W, 744, 1166, 800, 1222)
    return fill(a, m, grain_from=(-60, 0))


def fix_swords_03(a):
    H, W, _ = a.shape
    m = box(H, W, 255, 1160, 570, 1208) & (lum(a) < 80)
    m = ndimage.binary_dilation(m, iterations=3)
    return fill(a, m, grain_from=(0, -50))


def fix_swords_02(a):
    H, W, _ = a.shape
    sky = np.median(a[60:80, 650:700].reshape(-1, 3), axis=0)
    m = box(H, W, 710, 80, 790, 180) & (np.abs(a - sky).sum(-1) > 25)
    m = ndimage.binary_dilation(m, iterations=3)
    return fill(a, m, grain_from=(-90, 0))


def fix_swords_07(a):
    H, W, _ = a.shape
    cx, cy, r = 237, 640, 40                    # the rose, floating left of the central sword
    yy, xx = np.mgrid[0:H, 0:W]
    circ = (xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2
    sky = np.median(a[600:620, 140:180].reshape(-1, 3), axis=0)
    rose = circ & (np.abs(a - sky).sum(-1) > 40) & (xx < 270)
    rose = ndimage.binary_closing(rose, iterations=2)
    rose = ndimage.binary_fill_holes(rose)
    patch = a.copy()
    hole = ((xx - cx) ** 2 + (yy - cy) ** 2 <= (r + 4) ** 2) & (xx < 270)   # the rose and its rays
    out = a.astype(float).copy()
    hy, hx = np.nonzero(hole)
    out[hy, hx] = a[hy - 75, hx]               # the plain sky just above
    dx, dy = 236 - cx, 752 - cy                 # onto the front of the central fist (its knuckles)
    ys, xs = np.nonzero(rose)
    out[ys + dy, xs + dx] = patch[ys, xs]
    return out


def fix_key_11(a):
    """Narrow the blade to a point above the crown: rows from TAPER0 to TIP take the blade's own row
    (at y=160), squeezed toward its centre line; the rest of the blade down to the hair becomes the
    plain ground beside it."""
    H, W, _ = a.shape
    out = a.astype(float).copy()
    X0, X1 = 398, 452                           # the blade's columns (with its ink outline)
    TAPER0, TIP = 150, 176
    hole = np.zeros((H, W), bool)
    for x in range(X0, X1):
        col = a[TAPER0:230, x].astype(float)
        brown = np.nonzero((col[:, 0] - col[:, 2] > 50) & (lum(col) < 170) & (np.arange(len(col)) > 25))[0]
        hair = TAPER0 + (brown[0] if len(brown) else 40)
        hole[TAPER0:hair - 1, x] = True         # down to the hair (its brown begins at its outline)
    ys, xs = np.nonzero(hole)
    out[ys, xs] = a[ys, xs - 60]                # the plain ground to the left
    grey = (a[TAPER0:TAPER0 + 20, X0:X1].max(-1) - a[TAPER0:TAPER0 + 20, X0:X1].min(-1) < 60) | (lum(a[TAPER0:TAPER0 + 20, X0:X1]) < 70)
    row = grey[160 - TAPER0]
    cols = np.nonzero(row)[0]
    c = X0 + (cols.min() + cols.max()) / 2.0
    half = (cols.max() - cols.min()) / 2.0 + 1
    src_row = a[160].astype(float)
    for y in range(TAPER0, TIP):
        t = (y - TAPER0) / float(TIP - TAPER0)
        hw = max(half * (1 - t), 1.5)
        for x in range(int(c - hw - 1), int(c + hw + 2)):
            u = (x - c) / hw                    # -1 .. 1 across the narrowed row
            if abs(u) > 1:
                continue
            sx = c + u * half
            x0 = int(np.floor(sx)); f = sx - x0
            out[y, x] = src_row[x0] * (1 - f) + src_row[x0 + 1] * f
    return out


def fix_key_12(a):
    """Below the ankle knot the rope (columns 420-434, right of the leg's own outline) is replaced by
    what lies just right of it, the ground or the bent leg, which then passes behind as before."""
    out = a.astype(float).copy()
    out[178:430, 420:435] = a[178:430, 435:450]
    return out


def fix_wands_02(a):
    H, W, _ = a.shape
    y0, y1 = 1038, 1120                          # the flames under the lower small wand
    xr0, xr1 = 255, 595
    sub = a[y0:y1, xr0:xr1]
    flame = (sub[..., 0] > 180) & (sub[..., 0] - sub[..., 2] > 70)
    flame = ndimage.binary_dilation(flame, iterations=2)
    lab, n = ndimage.label(flame)
    if n != 7:
        raise SystemExit('wands-02: expected 7 lower flames, found %d' % n)
    boxes = sorted(ndimage.find_objects(lab), key=lambda s: s[1].start)
    # the wand's lower edge, over the middle of the wand
    col = lum(a[990:1060, 420])
    top = 990 + int(np.nonzero(col < 80)[0].max()) + 1
    bands = []                                   # (x0, x1, y_bottom): each flame with its wick
    for b in boxes:
        bands.append((xr0 + b[1].start - 4, xr0 + b[1].stop + 4, y0 + b[0].stop + 3))
    hole = np.zeros((H, W), bool)
    for x0, x1, yb in bands:
        hole[top:yb, x0:x1] = True
    out = a.astype(float).copy()
    paper = a[top:top + 90, 600:640].astype(float)
    grain = paper - ndimage.gaussian_filter(paper, sigma=(2.5, 2.5, 0))
    for x0, x1, yb in bands:
        L, R = out[top:yb, x0 - 1], out[top:yb, x1]
        for i, x in enumerate(range(x0, x1)):
            t = (i + 1) / float(x1 - x0 + 1)
            out[top:yb, x] = L * (1 - t) + R * t + grain[:yb - top, (x - x0) % 40]
    centres = [(x0 + x1) / 2.0 for x0, x1, _ in bands]
    left, right = centres[0], centres[-1]
    for j, k in enumerate((0, 2, 3, 4, 6)):
        x0, x1, yb = bands[k]
        w = x1 - x0
        nx0 = int(round(left + j * (right - left) / 4.0 - w / 2.0))
        alpha = np.ones(w)
        ramp = np.linspace(0, 1, 6)
        alpha[:6] = ramp; alpha[-6:] = ramp[::-1]
        piece = a[top:yb, x0:x1]
        dst = out[top:yb, nx0:nx0 + w]
        out[top:yb, nx0:nx0 + w] = dst * (1 - alpha[None, :, None]) + piece * alpha[None, :, None]
    return out


def vav(draw, cx, cy, h, gold=(214, 170, 64), ink=(40, 30, 20)):
    """Vav as the deck's glyph draws it (glyphs/hebrew-vau.svg), with a short head so it reads as
    Vav at this size: a small head at the top bending left, then the long upright stroke."""
    k = h / 62.0
    top, bot = (cx, cy - 31 * k), (cx, cy + 31 * k)
    head = (cx - 7 * k, cy - 29 * k)
    for col, wd, r in ((ink, 12, 7.5), (gold, 6, 4.5)):
        draw.line([head, top, bot], fill=col, width=max(int(wd * k), 3), joint='curve')
        for p, rr in ((head, r * 1.1), (bot, r * 0.8)):
            rr *= k
            draw.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=col)


def fix_swords_ace(a):
    H, W, _ = a.shape
    gold = (a[..., 0] > 150) & (a[..., 0] - a[..., 2] > 60)
    zone = box(H, W, 160, 0, 640, 110) | (box(H, W, 300, 330, 545, 650) & ~box(H, W, 382, 330, 418, 650))
    m = ndimage.binary_dilation(gold & zone, iterations=4) & zone
    out = fill(a, m)
    im = Image.fromarray(out.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for cx, cy in ((352, 380), (344, 470), (352, 560), (450, 380), (458, 470), (450, 560)):
        vav(d, cx, cy, 44)
    return np.asarray(im).astype(float)


def fix_pentacles_princess(a):
    H, W, _ = a.shape
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    yy, xx = np.mgrid[0:H, 0:W]
    red = (R > 150) & (G < 80) & (B < 80) & (xx > 500) & (xx < 700) & (yy > 420) & (yy < 640)
    cx, cy = xx[red].mean(), yy[red].mean()       # the red cross at the disc's centre
    r = np.hypot(xx - cx, yy - cy)
    th = np.degrees(np.arctan2(yy - cy, xx - cx)) % 360
    ring = (r >= 44) & (r <= 128)                 # white centre's edge .. the outer green ring
    m = np.floor(th / 30.0)
    j = np.round(m * 30 / 22.5)
    src = np.radians((th - 30 * m) * 0.75 + 22.5 * j)
    sx, sy = cx + r * np.cos(src), cy + r * np.sin(src)
    out = a.astype(float).copy()
    x0 = np.floor(sx).astype(int); y0 = np.floor(sy).astype(int)
    fx = (sx - x0)[..., None]; fy = (sy - y0)[..., None]
    x0 = np.clip(x0, 0, W - 2); y0 = np.clip(y0, 0, H - 2)
    val = (a[y0, x0] * (1 - fx) * (1 - fy) + a[y0, x0 + 1] * fx * (1 - fy)
           + a[y0 + 1, x0] * (1 - fx) * fy + a[y0 + 1, x0 + 1] * fx * fy)
    out[ring] = val[ring]
    return out


FIX = {'key-19-sun': fix_key_19, 'swords-03': fix_swords_03, 'swords-02': fix_swords_02,
       'swords-07': fix_swords_07, 'key-11-fortitude': fix_key_11, 'key-12-hanged-man': fix_key_12,
       'wands-02': fix_wands_02, 'swords-ace': fix_swords_ace, 'pentacles-princess': fix_pentacles_princess}


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    out = sys.argv[1]
    only = sys.argv[2:] or list(SOURCE)
    os.makedirs(out, exist_ok=True)
    for card in only:
        raw = os.path.join(out, card + '-source.png')
        if not os.path.exists(raw):
            subprocess.run(['curl', '-sfL', '-A', 'Mozilla/5.0', '-o', raw, SOURCE[card]], check=True)
        a = np.asarray(Image.open(raw).convert('RGB')).astype(float)
        res = FIX[card](a)
        Image.fromarray(np.asarray(res).clip(0, 255).astype(np.uint8)).save(os.path.join(out, card + '.png'))
        print('[fix_book_t_repaint_round4_2026_10_28] %s -> %s' % (card, os.path.join(out, card + '.png')))


if __name__ == '__main__':
    main()
