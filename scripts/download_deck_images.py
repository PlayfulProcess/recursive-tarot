#!/usr/bin/env python3
"""Download a deck's print-ready card images into a local folder, ready to
bulk-upload to a print-on-demand vendor (e.g. The Game Crafter).

Usage:
    python scripts/download_deck_images.py golden-dawn-book-t-tarot
    python scripts/download_deck_images.py minchiate-florence-tarot --all

By default only cards flagged print-ready (metadata.print.dpi_ready) are saved,
so you never upload a card that would print badly. Pass --all to grab every
imaged card regardless. Files are named "NN - Card Name.ext" in card order, in
  print/decks/<slug>/
which is gitignored — delete it after you've uploaded to the vendor (the images
are large and this machine is disk-tight).
"""
import json, os, sys, re, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def safe(name):
    # keep the full card name (incl. any "N — Le Fou" form), just sanitise for a filename
    return re.sub(r'\s+', ' ', re.sub(r'[^\w \-]', ' ', str(name))).strip()[:60] or "card"

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    take_all = '--all' in sys.argv
    if not args:
        print("usage: python scripts/download_deck_images.py <deck-slug> [--all]"); return
    slug = args[0]
    gpath = os.path.join(ROOT, "tarot", slug, "grammar.json")
    if not os.path.exists(gpath):
        print(f"no grammar for '{slug}' at {gpath}"); return
    g = json.load(open(gpath, encoding="utf-8"))
    cards = [i for i in g.get("items", []) if not i.get("composite_of")
             and i.get("category") not in ("axis", "keyword-emergence")]
    outdir = os.path.join(ROOT, "print", "decks", slug)
    os.makedirs(outdir, exist_ok=True)
    saved = skipped = failed = 0
    for idx, it in enumerate(cards, 1):
        img = it.get("image_url") or (it.get("metadata") or {}).get("image_url")
        ready = ((it.get("metadata") or {}).get("print") or {}).get("dpi_ready")
        if not img:
            continue
        if not take_all and not ready:
            skipped += 1; print(f"  skip (web-res): {safe(it.get('name'))}"); continue
        ext = ".png" if ".png" in img.lower() else ".jpg"
        num = (it.get("metadata") or {}).get("number")
        prefix = f"{int(num):02d} - " if isinstance(num, (int, float)) else f"{idx:02d} - "
        dest = os.path.join(outdir, prefix + safe(it.get("name")) + ext)
        try:
            req = urllib.request.Request(img, headers={"User-Agent": "recursive-tarot-print/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
                f.write(r.read())
            saved += 1; print(f"  saved {prefix}{safe(it.get('name'))}{ext}")
        except Exception as e:
            failed += 1; print(f"  FAIL {safe(it.get('name'))}: {e}")
    print(f"\n{saved} saved, {skipped} skipped (web-res), {failed} failed -> {outdir}")
    print("Upload these to your vendor, then delete the folder (large files).")

if __name__ == "__main__":
    main()
