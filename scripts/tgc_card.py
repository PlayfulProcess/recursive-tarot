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
from collections import deque
from PIL import Image, ImageChops, ImageFilter

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

# Decks whose scans keep leftover photographic BACKGROUND (white lightbox or black
# velvet) around a non-rectangular card — a plain rect crop can never remove it, so
# the bg shows as a contour against the canvas. flood_bg replaces every border-
# connected bg pixel with the canvas colour itself (the print analog of "set
# transparent color"): bg and bleed become one continuous colour, seam impossible.
# ONLY safe for cards with a CLOSED border/frame — on open line art the flood leaks
# through the engraving into the artwork (verified visually June 2026: court-de-
# gebelin, vieville, belgian, minchiate, marseille-conver leak; golden-dawn loses
# its genuine white RWS border; besancon picks a bad canvas colour).
FLOOD_BG = {"charles-vi-tarot", "paris-anonymous-tarot", "este-tarot",
            "madiao-money-cards", "mantegna-tarocchi", "sola-busca-tarot",
            "noblet-tarot", "visconti-sforza-tarot", "cary-sheet", "rosenwald-sheet"}

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

def _flood_bg_mask(im, tol=40):
    """Mask (L) of pixels CONNECTED TO THE IMAGE BORDER whose colour is close to the
    border colour — i.e. the leftover scan background (white lightbox or black velvet)
    around a non-rectangular card. Flood-fill on a thumbnail for speed, then upscale +
    feather. Returns (mask, bg_colour). Pixels of similar colour INSIDE the card are
    safe: they aren't border-connected, so the flood never reaches them."""
    W, H = im.size
    sw = 320; sh = max(2, round(sw * H / W))
    small = im.resize((sw, sh))
    px = small.load()
    perim = ([px[x, 0] for x in range(sw)] + [px[x, sh - 1] for x in range(sw)] +
             [px[0, y] for y in range(sh)] + [px[sw - 1, y] for y in range(sh)])
    perim.sort(key=lambda c: sum(c))
    bg = perim[len(perim) // 2]
    def close(c):
        return abs(c[0] - bg[0]) <= tol and abs(c[1] - bg[1]) <= tol and abs(c[2] - bg[2]) <= tol
    seen = bytearray(sw * sh)
    dq = deque()
    for x in range(sw):
        for y in (0, sh - 1):
            if close(px[x, y]) and not seen[y * sw + x]:
                seen[y * sw + x] = 1; dq.append((x, y))
    for y in range(sh):
        for x in (0, sw - 1):
            if close(px[x, y]) and not seen[y * sw + x]:
                seen[y * sw + x] = 1; dq.append((x, y))
    while dq:
        x, y = dq.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < sw and 0 <= ny < sh and not seen[ny * sw + nx] and close(px[nx, ny]):
                seen[ny * sw + nx] = 1; dq.append((nx, ny))
    mask = Image.frombytes("L", (sw, sh), bytes(255 if v else 0 for v in seen))
    mask = mask.filter(ImageFilter.MaxFilter(3))               # grow 1px: eat the dark fringe
    mask = mask.resize((W, H), Image.BILINEAR).filter(ImageFilter.GaussianBlur(3))  # feather
    return mask, bg

def _ring_colour_excluding(im, bg, tol=40):
    """Median colour of the content edge ring, IGNORING pixels close to bg — the
    card-stock colour even when leftover background pollutes the edges."""
    w, h = im.size
    ring = max(2, round(min(w, h) * 0.04)); px = []
    for x in range(0, w, 5):
        px += [im.getpixel((x, ring)), im.getpixel((x, h - 1 - ring))]
    for y in range(0, h, 5):
        px += [im.getpixel((ring, y)), im.getpixel((w - 1 - ring, y))]
    px = [c for c in px
          if not (abs(c[0] - bg[0]) <= tol and abs(c[1] - bg[1]) <= tol and abs(c[2] - bg[2]) <= tol)]
    if not px:
        return bg
    px.sort(key=lambda c: sum(c))
    return px[len(px) // 2]

def border_fit(im, blend_frame=False, tight=False, flood=False):
    """DEFAULT mode: card fitted inside the trim on a canvas of its own border colour.
    blend_frame=True samples that colour from the card's clean CORNERS instead of the
    edge median — so a card sitting on cream/white stock gets a matching bleed and the
    white/black 'contour' seam disappears (the print analog of PPT's 'set transparent').
    tight=True uses the density content crop (for wide card-stock margins)."""
    im = content_crop(im) if tight else autotrim(im)
    w, h = im.size
    inset = max(1, round(min(w, h) * 0.005))
    im = im.crop((inset, inset, w - inset, h - inset)); w, h = im.size
    if flood:
        # replace border-connected scan background with the card-stock colour, and
        # use that SAME colour for the canvas — bg and bleed become one colour.
        mask, bg = _flood_bg_mask(im)
        col = _ring_colour_excluding(im, bg)
        im = Image.composite(Image.new("RGB", im.size, col), im, mask)
    elif blend_frame:
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
