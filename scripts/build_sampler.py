#!/usr/bin/env python3
"""Build the SAMPLER test deck: one representative card from EVERY deck in the
library, auto-labelled by resolution tier (READY vs WEBRES TEST), plus every
historical card back. One proof order then physically answers, for every deck and
back at once: how the scans print, how the cream margins look, how bad web-res
really is, which back feels best. Output: print/decks/sampler-tgc/ (900x1500).

Fronts use border mode (card inside the safe zone on a sampled-cream margin);
backs use cover mode (patterns are borderless by design). Decks whose source is a
high-res IIIF archive are re-pulled at print width via HIGH_RES (their committed
Pages images are only display-res).
"""
import io, json, os, glob, urllib.request
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "print", "decks", "sampler-tgc")
TW, TH = 900, 1500
SAFE = (750, 1350)

# Decks whose committed Pages images are display-res but whose source archive has
# print-res — re-pull ONE representative card at ~1000px wide for the proof.
HIGH_RES = {
    "vieville-tarot":        "https://gallica.bnf.fr/iiif/ark:/12148/btv1b10510963k/f1/full/1000,/0/native.jpg",
    "paris-anonymous-tarot": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b105109624/f1/full/1000,/0/native.jpg",
    "este-tarot":            "https://collections.library.yale.edu/iiif/2/33215686/full/1000,/0/default.jpg",
}

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "recursive-tarot/1.0"})
    return Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert("RGB")

def border_fit(im):
    w, h = im.size
    inset = max(2, round(min(w, h) * 0.012))
    im = im.crop((inset, inset, w - inset, h - inset)); w, h = im.size
    ring = max(2, round(min(w, h) * 0.02)); px = []
    for x in range(0, w, 7): px += [im.getpixel((x, ring)), im.getpixel((x, h - 1 - ring))]
    for y in range(0, h, 7): px += [im.getpixel((ring, y)), im.getpixel((w - 1 - ring, y))]
    px.sort(key=lambda c: c[0] + c[1] + c[2]); col = px[len(px) // 2]
    s = min(SAFE[0] / w, SAFE[1] / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    canvas = Image.new("RGB", (TW, TH), col)
    canvas.paste(im, ((TW - im.width) // 2, (TH - im.height) // 2))
    return canvas

def cover_fit(im):
    w, h = im.size; s = max(TW / w, TH / h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    l, t = (im.width - TW) // 2, (im.height - TH) // 2
    return im.crop((l, t, l + TW, t + TH))

def first_card(slug):
    g = json.load(open(os.path.join(ROOT, "tarot", slug, "grammar.json"), encoding="utf-8"))
    for it in g.get("items", []):
        if it.get("composite_of") or it.get("category") in ("axis", "keyword-emergence"):
            continue
        u = it.get("image_url") or (it.get("metadata") or {}).get("image_url")
        if u:
            return u
    return None

def main():
    os.makedirs(OUT, exist_ok=True)
    col = json.load(open(os.path.join(ROOT, "tarot", "_collection.json"), encoding="utf-8"))
    slugs = [g["slug"] for g in col["grammars"]
             if not g.get("is_meta") and g["slug"] not in ("tree-of-tarot",)]
    n = 0
    for i, slug in enumerate(sorted(slugs), 1):
        try:
            # prefer a pre-built cream-bordered TGC file if one exists
            built = sorted(glob.glob(os.path.join(ROOT, "print", "decks", slug + "-tgc", "*.jpg")))
            if built:
                im = Image.open(built[0]).convert("RGB")
                tier = "READY"
            else:
                url = HIGH_RES.get(slug) or first_card(slug)
                if not url:
                    print(f"  skip {slug}: no card image"); continue
                src = fetch(url)
                tier = "READY" if min(src.size) >= 800 else "WEBRES TEST"
                im = border_fit(src)
            im.save(os.path.join(OUT, f"{i:02d} - {tier} - {slug[:28]}.jpg"), "JPEG", quality=92)
            n += 1; print(f"  {tier:11} {slug}")
        except Exception as e:
            print(f"  FAIL {slug}: {str(e)[:50]}")
    # card backs
    bpath = os.path.join(ROOT, "print", "card-backs.json")
    if os.path.exists(bpath):
        for k, b in enumerate(json.load(open(bpath, encoding="utf-8")).get("items", []), 1):
            u = b.get("image_url")
            if not u: continue
            try:
                cover_fit(fetch(u)).save(os.path.join(OUT, f"B{k:02d} - BACK - {b['id'][5:28]}.jpg"), "JPEG", quality=92)
                n += 1; print(f"  BACK        {b['id']}")
            except Exception as e:
                print(f"  FAIL back {b['id']}: {str(e)[:40]}")
    print(f"\nsampler: {n} cards -> {OUT}")

if __name__ == "__main__":
    main()
