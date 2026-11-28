"""Corrections by script in round 5 of the Book T repaint (Nov 28 2026).

Round 5 (research/synthesis/book-t-painting-review-2026-11-28.md) mends what the Nov 28 review of all
78 paintings found. Three of the cards are done by script, as in rounds 2-4:

* wands-ace (composite): Book T, "The Right-and Left-hand branches end respectively in three Flames,
  and the Centre one in four". The kept painting had one large flame per branch. Each large flame is
  cleared (filled from the cream ground; the wood is never touched), and one painted flame tongue
  (an element painted once, https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1795880833377-yuuulvg4vl8.png) is set ten times,
  fanned like the points of a crown: 3, 4, 3. The composite was then the reference of a clean
  Nano Banana Pro painting, which is the kept picture (it keeps the 3 / 4 / 3 and the 22 yods).
* swords-ace: Book T, "Six Vaus fall from its point". The Nov 28 painting set six marks above the
  point that read as Yods; they and three pale dots are filled with the sky, and the six Vavs of the
  round-4 painting (the deck's glyph) are copied into their places.
* wands-queen: the row of painted pseudo-letters on the green ground is filled with that green.

    python scripts/fix_book_t_repaint_round5_2026_11_28.py OUT_DIR [card ...]

fetches the sources (curl) and writes <card>.png to OUT_DIR.
"""
import os
import subprocess
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

CDN = 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/'
SOURCE = {
    'wands-ace': [CDN + 'grammars/1793139576228-crk5800wxjp.png',        # the round-3 painting
                  CDN + 'flow-image-gen/1795880833377-yuuulvg4vl8.png'],  # one flame tongue
    'swords-ace': [CDN + 'flow-image-gen/1795880729957-l8a1vdb983r.png',  # Nov 28, attempt 1 (2.1)
                   CDN + 'grammars/1793198841696-c53w57y2mwp.png'],       # round 4 (its Vavs)
    'wands-queen': [CDN + 'flow-image-gen/1791651073337-7ubkvuiawtp.png'],
}


def ace_wands(src, flame_png, out):
    A = np.asarray(Image.open(src).convert('RGB')).astype(float)
    H, W, _ = A.shape
    r, g, b = A[..., 0], A[..., 1], A[..., 2]
    lum = .3*r + .59*g + .11*b
    flame = (r > 150) & (r - g > 45) & (b < 140)
    lab, n = ndimage.label(ndimage.binary_dilation(flame, iterations=2))
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n+1))
    big = np.zeros_like(flame)
    for i, s in enumerate(sizes, 1):
        if s > 4000:
            big |= lab == i
    # each big flame as a solid region (its ink and glow included). Above each branch's tip line the
    # whole region is cleared; below it only the flame's own colours and glow are, never the wood.
    region = np.zeros_like(flame)
    for i, sz in enumerate(sizes, 1):
        if sz > 4000:
            c = lab == i
            c = ndimage.binary_fill_holes(ndimage.binary_closing(c, iterations=14))
            region |= ndimage.binary_dilation(c, iterations=14)
    yy, xx = np.mgrid[0:H, 0:W]
    tipline = np.where(xx < 330, 452, np.where(xx > 520, 446, 318))
    light = (lum > 175) & (np.abs(r - g) < 60)             # the white glow around the old flames
    mask = region & ((yy < tipline) | flame | light) & (yy < 540)
    def fill(a, m, iters=900):
        a = a.copy()
        ys, xs = np.nonzero(m)
        y0, y1, x0, x1 = ys.min()-8, ys.max()+9, xs.min()-8, xs.max()+9
        w = a[y0:y1, x0:x1].copy(); mm = m[y0:y1, x0:x1]
        ring = ndimage.binary_dilation(mm, iterations=3) & ~mm
        w[mm] = w[ring].mean(axis=0)
        k = np.array([[0, .25, 0], [.25, 0, .25], [0, .25, 0]])
        for _ in range(iters):
            for c in range(3):
                s = ndimage.convolve(w[..., c], k, mode='nearest'); w[..., c][mm] = s[mm]
        # paper grain from the ground just left of the fill
        donor = a[y0:y1, max(x0-60, 0):max(x0-60, 0)+(x1-x0)]
        if donor.shape == w.shape:
            res = donor - ndimage.gaussian_filter(donor, sigma=(2.5, 2.5, 0))
            w[mm] += 0.8*res[mm]
        a[y0:y1, x0:x1] = w
        return a

    lab2, n2 = ndimage.label(mask)
    for i in range(1, n2+1):
        m = lab2 == i
        if m.sum() > 30:
            A = fill(A, m)

    # the flame tongue as a sprite with alpha
    F = np.asarray(Image.open(flame_png).convert('RGB')).astype(float)
    bg = np.median(F[:40, :40].reshape(-1, 3), axis=0)
    alpha = (np.abs(F - bg).sum(-1) > 60)
    alpha = ndimage.binary_fill_holes(ndimage.binary_closing(alpha, iterations=2))
    ys, xs = np.nonzero(alpha)
    F = F[ys.min():ys.max()+1, xs.min():xs.max()+1]
    alpha = alpha[ys.min():ys.max()+1, xs.min():xs.max()+1].astype(float)
    alpha = ndimage.gaussian_filter(alpha, 0.7)
    F2 = F
    sprite = Image.fromarray(np.dstack([F, alpha*255]).astype(np.uint8), 'RGBA')

    canvas = Image.fromarray(np.clip(A, 0, 255).astype(np.uint8)).convert('RGBA')
    def put(cx, base_y, h, angle):
        s = sprite.resize((max(1, int(0.78*sprite.width*h/sprite.height)), h), Image.LANCZOS)
        s = s.rotate(angle, resample=Image.BICUBIC, expand=True)
        canvas.alpha_composite(s, (int(cx - s.width/2), int(base_y - s.height)))

    # (tip centre x, tip top y, spread of the bases, heights, angles); left/right branches lean outward
    TIPS = {
        'L': (210, 476, [-46, 0, 46], [125, 150, 125], [34, 16, -2]),
        'C': (425, 344, [-69, -23, 23, 69], [130, 155, 155, 130], [20, 6, -6, -20]),
        'R': (650, 472, [-46, 0, 46], [125, 150, 125], [2, -16, -34]),
    }
    for k, (cx, ty, dxs, hs, angs) in TIPS.items():
        order = sorted(range(len(dxs)), key=lambda i: hs[i])   # tallest last, on top
        for i in order:
            put(cx + dxs[i], ty + 14, hs[i], angs[i])
    canvas.convert('RGB').save(out)


def ace_swords(new, old, out):
    A = np.asarray(Image.open(new).convert('RGB')).astype(float)
    O = np.asarray(Image.open(old).convert('RGB')).astype(float)
    H, W, _ = A.shape
    r, g, b = A[..., 0], A[..., 1], A[..., 2]
    gold = (r > 150) & (g > 100) & (b < 110) & (r - b > 70)
    top = np.zeros_like(gold); top[0:200, 250:650] = True
    marks = ndimage.binary_dilation(gold & top, iterations=4)
    lum = .3*r + .59*g + .11*b
    # pale smudges: blobs much brighter than the sky 15 px around them, in the top band
    bg = ndimage.median_filter(lum, size=41)
    smudge = (lum - bg > 18) & top & (np.abs(r - b) < 40)
    smudge = ndimage.binary_opening(smudge, iterations=1)
    lab, n = ndimage.label(smudge)
    keep = np.zeros_like(smudge)
    for i, s in enumerate(ndimage.find_objects(lab), 1):
        h, w = s[0].stop - s[0].start, s[1].stop - s[1].start
        if 6 < h < 50 and 6 < w < 50:
            keep |= lab == i
    smudge = ndimage.binary_dilation(keep, iterations=5)
    yy, xx = np.mgrid[0:H, 0:W]
    for (sy, sx) in [(7, 422), (62, 347), (62, 504)]:   # the three pale dots, found on zoomed crops
        smudge |= (yy - sy)**2 + (xx - sx)**2 <= 17**2
    blade = np.zeros_like(gold); blade[90:200, 395:450] = True   # leave the sword's point alone
    mask = (marks | smudge) & ~blade

    def fill(a, m, iters=700):
        a = a.copy()
        lab, n = ndimage.label(m)
        k = np.array([[0, .25, 0], [.25, 0, .25], [0, .25, 0]])
        for s in ndimage.find_objects(lab):
            y0, y1 = max(s[0].start-8, 0), min(s[0].stop+8, H)
            x0, x1 = max(s[1].start-8, 0), min(s[1].stop+8, W)
            w = a[y0:y1, x0:x1].copy(); mm = m[y0:y1, x0:x1]
            ring = ndimage.binary_dilation(mm, iterations=2) & ~mm
            w[mm] = w[ring].mean(axis=0)
            for _ in range(iters):
                for c in range(3):
                    sm = ndimage.convolve(w[..., c], k, mode='nearest'); w[..., c][mm] = sm[mm]
            dn = a[y0:y1, x0+40:x1+40] if x1+40 < W else a[y0:y1, x0-40:x1-40]
            res = dn - ndimage.gaussian_filter(dn, sigma=(2, 2, 0)); w[mm] += res[mm]
            a[y0:y1, x0:x1] = w
        return a
    A = fill(A, mask)

    # the six Vavs of the current painting, each cut with its ink outline from the sky around it
    VAVS = [(353, 407, 341, 357), (353, 407, 439, 455), (443, 497, 333, 349),
            (443, 497, 447, 463), (533, 587, 341, 357), (533, 587, 439, 455)]
    # the six places: the marks' centres, outermost lowest (falling away from the point)
    PLACES = [(56, 390), (52, 457), (100, 350), (98, 498), (130, 309), (132, 539)]
    for (y0, y1, x0, x1), (cy, cx) in zip(VAVS, PLACES):
        y0, y1, x0, x1 = y0-4, y1+4, x0-5, x1+5
        p = O[y0:y1, x0:x1]
        sky = np.median(np.concatenate([p[:3].reshape(-1, 3), p[-3:].reshape(-1, 3)]), axis=0)
        al = np.clip((np.abs(p - sky).sum(-1) - 30) / 60, 0, 1)
        gl = (p[..., 0] > 150) & (p[..., 0] - p[..., 2] > 70)          # the gold of the letter
        al = (al * ndimage.binary_dilation(gl, iterations=3))[..., None]
        h, w = p.shape[:2]
        ty, tx = cy - h//2, cx - w//2
        A[ty:ty+h, tx:tx+w] = al*p + (1-al)*A[ty:ty+h, tx:tx+w]
    Image.fromarray(np.clip(A, 0, 255).astype(np.uint8)).save(out)


def queen_wands(src, out):
    A = np.asarray(Image.open(src).convert('RGB')).astype(float)
    H, W, _ = A.shape
    r, g, b = A[..., 0], A[..., 1], A[..., 2]
    green = (g > r) & (g > b + 10)
    rows = np.nonzero(green[:, 40:W-40].mean(1) > 0.25)[0]
    y0 = rows[rows > H*0.8].min()
    band = np.zeros((H, W), bool); band[y0:1220, 20:W-20] = True   # above the ink border at y 1223
    dark = (.3*r + .59*g + .11*b < 120) & band & ~green
    # keep only marks sitting on green (not the flames, the foot, or the leopard)
    gnear = ndimage.uniform_filter(green.astype(float), 25) > 0.45
    lab, n = ndimage.label(ndimage.binary_dilation(dark, iterations=1))
    mask = np.zeros_like(dark)
    for i, s in enumerate(ndimage.find_objects(lab), 1):
        comp = lab[s] == i
        if gnear[s][comp].mean() > 0.6 or (s[0].start > 1178 and s[0].stop < H-14):
            mask[s] |= comp
    # the middle three marks touch the flames' outline: taken by their own box under the fire
    mid = np.zeros_like(dark); mid[1180:1219, 250:570] = True
    mask |= dark & mid
    mask = ndimage.binary_dilation(mask, iterations=3) & band
    gz = A[1200:1230, 60:200]
    GRAIN = float((gz - ndimage.gaussian_filter(gz, sigma=(2, 2, 0))).std())
    RNG = np.random.default_rng(7)
    k = np.array([[0, .25, 0], [.25, 0, .25], [0, .25, 0]])
    lab, n = ndimage.label(mask)
    for s in ndimage.find_objects(lab):
        ya, yb = max(s[0].start-6, 0), min(s[0].stop+6, H); xa, xb = max(s[1].start-6, 0), min(s[1].stop+6, W)
        w = A[ya:yb, xa:xb].copy(); mm = mask[ya:yb, xa:xb]
        ring = ndimage.binary_dilation(mm, iterations=2) & ~mm
        w[mm] = w[ring].mean(axis=0)
        for _ in range(600):
            for c in range(3):
                sm = ndimage.convolve(w[..., c], k, mode='nearest'); w[..., c][mm] = sm[mm]
        w[mm] += RNG.normal(0, GRAIN, (mm.sum(), 3))
        A[ya:yb, xa:xb] = w
    Image.fromarray(np.clip(A, 0, 255).astype(np.uint8)).save(out)
    print('band from y', y0, 'marks filled', n)


FIX = {'wands-ace': ace_wands, 'swords-ace': ace_swords, 'wands-queen': queen_wands}


def main():
    out_dir = sys.argv[1]
    cards = sys.argv[2:] or list(FIX)
    os.makedirs(out_dir, exist_ok=True)
    for card in cards:
        srcs = []
        for i, url in enumerate(SOURCE[card]):
            p = os.path.join(out_dir, '%s.src%d.png' % (card, i))
            subprocess.run(['curl', '-s', '-o', p, url], check=True)
            srcs.append(p)
        FIX[card](*srcs, os.path.join(out_dir, card + '.png'))
        print(card, '->', os.path.join(out_dir, card + '.png'))


if __name__ == '__main__':
    main()
