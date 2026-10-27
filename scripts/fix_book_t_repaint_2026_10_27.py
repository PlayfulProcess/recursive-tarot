"""Corrections by script on three kept paintings of the Oct 27 2026 Book T repaint.

The repaint (docs/research/BOOK-T-PAINTED-CHECK-2026-10-21.md, "Oct 27 repaint") kept three AI paintings
that had everything Book T asks for but one detail. Like fixrays.py and splitface.py in the first run
(tarot/book-t/PROMPTS.md, "Redo, round 1"), the detail is mended on the painting itself, by copying
the painting's own strokes; nothing new is drawn. The results were uploaded to the CDN and are the
"Book T deck, painting" entries of these cards in tarot/book-t/grammar.json.

    python scripts/fix_book_t_repaint_2026_10_27.py OUT_DIR

fetches the three kept paintings (curl) and writes the corrected PNGs to OUT_DIR.
"""
import os
import subprocess
import sys

from PIL import Image

KEPT = {
    'wands-ace': 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1793139128413-ed1a0i0s36s.png',
    'wands-04': 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1793138236082-v7vnle9cqo.png',
    'wands-10': 'https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/flow-image-gen/1793139020176-3xpv8bq5iv6.png',
}


def lum(p):
    return 0.3 * p[0] + 0.59 * p[1] + 0.11 * p[2]


def mask_of(img, keep):
    m = Image.new('L', img.size, 0)
    px, mp = img.load(), m.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if keep(px[x, y]):
                mp[x, y] = 255
    return m


def fix_wands_ace(im):
    """Book T: 22 Yods, "twelve: six above and six below about the Left-hand branch". The painting
    has 7 above the centre branch, 3 by the right branch and 6 below the left: 16. Its block of six
    (only the red, gold and ink pixels) is copied above the left branch: 22."""
    block = im.crop((130, 580, 250, 730))
    keep = mask_of(block, lambda p: lum(p) < 90 or (p[0] > 150 and p[0] - p[2] > 90))
    im.paste(block, (48, 150), keep)
    return im


def fix_wands_04(im):
    """A small painted seal-like mark in the ground's bottom-right corner; the deck's paintings carry
    no marks. Covered with the plain green ground just left of it."""
    patch = im.crop((746, 1180, 758, 1218))
    for x in range(758, 803, 12):
        im.paste(patch, (x, 1180))
    return im


def fix_wands_10(im):
    """Book T: "A fifth hand holding two wands upright". The painting has eight crossed wands (four
    and four) and one upright wand. The upright wand (its rows above and below the fingers) is copied
    40 px to the left; only its wood and ink are copied, so the hand and sleeve stay as painted."""
    x0, x1, y0, y1, yf0, yf1 = 406, 444, 760, 1150, 856, 975
    top = im.crop((x0, y0, x1, yf0))
    low = im.crop((x0, yf1, x1, y1))
    strip = Image.new('RGB', (x1 - x0, y1 - y0))
    strip.paste(top, (0, 0))
    strip.paste(low.crop((0, 0, x1 - x0, yf1 - yf0)), (0, yf0 - y0))
    strip.paste(low, (0, yf1 - y0))
    keep = mask_of(strip, lambda p: lum(p) < 60 or (lum(p) < 175 and p[0] > p[2] + 15))
    im.paste(strip, (x0 - 40, y0), keep)
    return im


FIX = {'wands-ace': fix_wands_ace, 'wands-04': fix_wands_04, 'wands-10': fix_wands_10}


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for card, url in KEPT.items():
        raw = os.path.join(out, card + '-kept.png')
        subprocess.run(['curl', '-sfL', '-A', 'Mozilla/5.0', '-o', raw, url], check=True)
        im = FIX[card](Image.open(raw).convert('RGB'))
        im.save(os.path.join(out, card + '.png'))
        print('[fix_book_t_repaint_2026_10_27] %s -> %s' % (card, os.path.join(out, card + '.png')))


if __name__ == '__main__':
    main()
