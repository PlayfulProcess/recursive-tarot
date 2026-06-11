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

def border_fit(im):
    """DEFAULT mode: card fitted inside the trim on a canvas of its own sampled
    border colour (so the bleed band matches the card, not a white edge)."""
    im = autotrim(im)
    w, h = im.size
    inset = max(1, round(min(w, h) * 0.005))
    im = im.crop((inset, inset, w - inset, h - inset)); w, h = im.size
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
