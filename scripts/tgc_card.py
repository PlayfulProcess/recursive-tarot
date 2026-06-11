#!/usr/bin/env python3
"""Shared TGC card-image processing — the SINGLE source of truth for how any card
becomes a 900x1500 print-ready file. Imported by the sampler AND by whole-deck /
print-on-demand builds, so every product is treated identically (same trim, same
auto-trim, same bleed). Also exposes print_quality() so the UI can warn on low-res.

The Game Crafter — Tarot Deck spec:
    upload / bleed : 900 x 1500   (what you upload)
    trim / cut     : 825 x 1425   (the cut line)
    safe zone      : 750 x 1350   (keep critical content inside this)
"""
import io, urllib.request
from PIL import Image, ImageChops

TW, TH = 900, 1500
TRIM   = (825, 1425)
FIT    = (800, 1395)   # fit cards just INSIDE the trim — full, but nothing cut
PRINT_MIN = 800        # min source short-side (px) to count as print-ready at card size

# Decks whose scans sit on cream/white card-stock — sample the bleed from the clean
# corners (blend_frame) so the white/black "contour" seam disappears. Shared so the
# sampler AND whole-deck product bakes treat them identically.
BLEND_FRAME = {"charles-vi-tarot", "este-tarot", "madiao-money-cards",
               "minchiate-florence-tarot", "oswald-wirth-tarot",
               "paris-anonymous-tarot", "vieville-tarot"}

# Decks where a plain auto-trim leaves a wide card-stock margin (faint marginal
# text / library stamps fool the bbox). Use the density-based content crop instead.
TIGHT_TRIM = {"oswald-wirth-tarot", "minchiate-florence-tarot", "paris-anonymous-tarot"}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "recursive-tarot/1.0 (PlayfulProcess)"})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=90).read())).convert("RGB")

def print_quality(im):
    """'print' if the source can print cleanly at card size, else 'web' (warn the user)."""
    return "print" if min(im.size) >= PRINT_MIN else "web"

def autotrim(im):
    """Strip a uniform scan margin matching the corner colour, so the card fills its
    frame (fixes tiny cards floating in whitespace + white/black scan 'contours')."""
    corner = im.getpixel((1, 1))
    diff = ImageChops.difference(im, Image.new("RGB", im.size, corner))
    bbox = diff.convert("L").point(lambda p: 255 if p > 24 else 0).getbbox()
    if bbox:
        l, t, r, b = bbox; w, h = im.size
        if l > w * 0.015 or t > h * 0.015 or r < w * 0.985 or b < h * 0.985:
            pad = round(min(w, h) * 0.008)
            return im.crop((max(0, l - pad), max(0, t - pad), min(w, r + pad), min(h, b + pad)))
    return im

def _corner_colour(im):
    """Average of the four corner patches — the clean card-stock colour. Used so the
    bleed band MATCHES the card (no darker 'contour' seam from edge shadow)."""
    w, h = im.size; c = max(4, round(min(w, h) * 0.05)); cols = []
    for box in [(0, 0, c, c), (w - c, 0, w, c), (0, h - c, c, h), (w - c, h - c, w, h)]:
        cols.append(im.crop(box).resize((1, 1)).getpixel((0, 0)))
    return tuple(round(sum(p[i] for p in cols) / len(cols)) for i in range(3))

def content_crop(im, frac=0.05):
    """Crop to the DENSE content region — drops a wide card-stock margin AND the
    sparse marginal marks (faint top text, library stamps) that fool a plain bbox.
    Works on a small thumbnail for speed, then maps the crop back to full res."""
    W, H = im.size
    small = im.resize((min(420, W), max(1, round(min(420, W) * H / W))))
    sw, sh = small.size
    corner = small.getpixel((1, 1))
    mask = ImageChops.difference(small, Image.new("RGB", small.size, corner)).convert("L").point(lambda p: 1 if p > 28 else 0)
    px = mask.load()
    colsum = [sum(px[x, y] for y in range(sh)) for x in range(sw)]
    rowsum = [sum(px[x, y] for x in range(sw)) for y in range(sh)]
    cmax = max(colsum) or 1; rmax = max(rowsum) or 1
    xs = [x for x in range(sw) if colsum[x] > frac * cmax]
    ys = [y for y in range(sh) if rowsum[y] > frac * rmax]
    if not xs or not ys:
        return im
    pad = 0.012
    l = max(0.0, min(xs) / sw - pad); r = min(1.0, (max(xs) + 1) / sw + pad)
    t = max(0.0, min(ys) / sh - pad); b = min(1.0, (max(ys) + 1) / sh + pad)
    return im.crop((round(l * W), round(t * H), round(r * W), round(b * H)))

def border_fit(im, blend_frame=False, tight=False):
    """DEFAULT mode: card fitted inside the trim on a canvas of its own border colour.
    blend_frame=True samples that colour from the card's clean CORNERS instead of the
    edge median — so a card sitting on cream/white stock gets a matching bleed and the
    white/black 'contour' seam disappears (the print analog of PPT's 'set transparent').
    tight=True uses the density content crop (for wide card-stock margins)."""
    im = content_crop(im) if tight else autotrim(im)
    w, h = im.size
    inset = max(1, round(min(w, h) * 0.005))
    im = im.crop((inset, inset, w - inset, h - inset)); w, h = im.size
    if blend_frame:
        col = _corner_colour(im)
    else:
        ring = max(2, round(min(w, h) * 0.02)); px = []
        for x in range(0, w, 7): px += [im.getpixel((x, ring)), im.getpixel((x, h - 1 - ring))]
        for y in range(0, h, 7): px += [im.getpixel((ring, y)), im.getpixel((w - 1 - ring, y))]
        px.sort(key=lambda c: sum(c)); col = px[len(px) // 2]
    s = min(FIT[0] / w, FIT[1] / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    canvas = Image.new("RGB", (TW, TH), col)
    canvas.paste(im, ((TW - im.width) // 2, (TH - im.height) // 2))
    return canvas

def cover_fit(im):
    """Fill the whole 900x1500 (for borderless art and card backs)."""
    w, h = im.size; s = max(TW / w, TH / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    l, t = (im.width - TW) // 2, (im.height - TH) // 2
    return im.crop((l, t, l + TW, t + TH))
