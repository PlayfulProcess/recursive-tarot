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
import json, os, glob, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tgc_card import TW, TH, fetch, border_fit, cover_fit, print_quality, autotrim, BLEND_FRAME, TIGHT_TRIM  # shared

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "print", "decks", "sampler-tgc")

# Decks whose committed Pages images are display-res but whose source archive has
# print-res — re-pull ONE representative card at ~1000px wide for the proof.
HIGH_RES = {
    "vieville-tarot":        "https://gallica.bnf.fr/iiif/ark:/12148/btv1b10510963k/f1/full/1000,/0/native.jpg",
    "paris-anonymous-tarot": "https://gallica.bnf.fr/iiif/ark:/12148/btv1b105109624/f1/full/1000,/0/native.jpg",
    "este-tarot":            "https://collections.library.yale.edu/iiif/2/33215686/full/1000,/0/default.jpg",
}

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
            # always re-process from source with the shared tgc_card settings (the
            # old pre-built *-tgc files are stale cream-border, before auto-trim)
            url = HIGH_RES.get(slug) or first_card(slug)
            if not url:
                print(f"  skip {slug}: no card image"); continue
            src = fetch(url)
            tier = "READY" if min(src.size) >= 800 else "WEBRES TEST"
            im = border_fit(src, blend_frame=(slug in BLEND_FRAME), tight=(slug in TIGHT_TRIM))
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
                cover_fit(autotrim(fetch(u))).save(os.path.join(OUT, f"B{k:02d} - BACK - {b['id'][5:28]}.jpg"), "JPEG", quality=92)
                n += 1; print(f"  BACK        {b['id']}")
            except Exception as e:
                print(f"  FAIL back {b['id']}: {str(e)[:40]}")
    print(f"\nsampler: {n} cards -> {OUT}")

if __name__ == "__main__":
    main()
