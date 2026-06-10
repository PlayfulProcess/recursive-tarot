#!/usr/bin/env python3
"""Build the SAMPLER test deck: one representative card from EVERY deck (print-ready
AND web-res, labelled) + every historical card back printed as a face.

One ~21-card proof order then physically answers, for every deck and back at once:
how do the scans print, how do the cream margins look, how bad is web-res really,
which back design feels best. Output: print/decks/sampler-tgc/ (900x1500 files).

Fronts use border mode (card inside safe zone, sampled-cream margin).
Backs use cover mode (patterns are borderless by design).
"""
import io, json, os, sys, glob, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "print", "decks", "sampler-tgc")
TW, TH = 900, 1500
SAFE = (750, 1350)

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "recursive-tarot/1.0"})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=40).read())).convert("RGB")

def border_fit(im):
    w, h = im.size
    inset = max(2, round(min(w, h) * 0.012))
    im = im.crop((inset, inset, w - inset, h - inset)); w, h = im.size
    ring = max(2, round(min(w, h) * 0.02)); px = []
    for x in range(0, w, 7): px += [im.getpixel((x, ring)), im.getpixel((x, h - 1 - ring))]
    for y in range(0, h, 7): px += [im.getpixel((ring, y)), im.getpixel((w - 1 - ring, y))]
    px.sort(key=lambda c: c[0] + c[1] + c[2])
    col = px[len(px) // 2]
    s = min(SAFE[0] / w, SAFE[1] / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    canvas = Image.new("RGB", (TW, TH), col)
    canvas.paste(im, ((TW - im.width) // 2, (TH - im.height) // 2))
    return canvas

def cover_fit(im):
    w, h = im.size
    s = max(TW / w, TH / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    l, t = (im.width - TW) // 2, (im.height - TH) // 2
    return im.crop((l, t, l + TW, t + TH))

def first_card_url(slug):
    g = json.load(open(os.path.join(ROOT, "tarot", slug, "grammar.json"), encoding="utf-8"))
    for it in g.get("items", []):
        if it.get("composite_of") or it.get("category") in ("axis", "keyword-emergence"):
            continue
        u = it.get("image_url") or (it.get("metadata") or {}).get("image_url")
        if u:
            return u, it.get("name", slug)
    return None, None

READY = ["golden-dawn-book-t-tarot", "minchiate-florence-tarot", "oswald-wirth-tarot",
         "etteilla-ii-egyptian", "mantegna-tarocchi", "tarot-de-marseille-conver",
         "etteilla-i-livre-de-thot", "etteilla-iii-oracle-des-dames"]
WEBRES = ["visconti-sforza-tarot", "sola-busca-tarot", "charles-vi-tarot",
          "tarot-de-besancon", "court-de-gebelin-tarot", "cary-yale-visconti-tarot"]

def main():
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for i, slug in enumerate(READY, 1):
        # prefer the already-built tgc file (first card, already cream-bordered)
        built = sorted(glob.glob(os.path.join(ROOT, "print", "decks", slug + "-tgc", "*.jpg")))
        try:
            if built:
                im = Image.open(built[0]).convert("RGB")
                Image.Image.save(im, os.path.join(OUT, f"{i:02d} - READY - {slug[:30]}.jpg"), "JPEG", quality=92)
            else:
                u, _ = first_card_url(slug)
                border_fit(fetch(u)).save(os.path.join(OUT, f"{i:02d} - READY - {slug[:30]}.jpg"), "JPEG", quality=92)
            n += 1; print(f"  ready  {slug}")
        except Exception as e:
            print(f"  FAIL {slug}: {e}")
    for j, slug in enumerate(WEBRES, 1):
        try:
            u, _ = first_card_url(slug)
            border_fit(fetch(u)).save(os.path.join(OUT, f"{j+20:02d} - WEBRES TEST - {slug[:26]}.jpg"), "JPEG", quality=92)
            n += 1; print(f"  webres {slug}")
        except Exception as e:
            print(f"  FAIL {slug}: {e}")
    backs = json.load(open(os.path.join(ROOT, "print", "card-backs.json"), encoding="utf-8"))
    k = 0
    for b in backs.get("items", []):
        u = b.get("image_url")
        if not u:
            continue
        k += 1
        try:
            cover_fit(fetch(u)).save(os.path.join(OUT, f"{k+40:02d} - BACK - {b['id'][5:30]}.jpg"), "JPEG", quality=92)
            n += 1; print(f"  back   {b['id']}")
        except Exception as e:
            print(f"  FAIL back {b['id']}: {e}")
    print(f"\nsampler: {n} cards -> {OUT}")

if __name__ == "__main__":
    main()
