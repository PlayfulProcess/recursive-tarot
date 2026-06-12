#!/usr/bin/env python3
"""Detect which decks have leftover scan BACKGROUND (white lightbox / black velvet)
around a non-rectangular card — the contour problem on TGC proofs. For each deck,
fetch the sampler's representative card, flood-fill from the border, and report the
bg colour + how much of the frame it covers. Decks above the threshold should be in
tgc_card.FLOOD_BG. Optionally bakes before/after previews with --preview <outdir>.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tgc_card
from build_sampler import first_card, HIGH_RES

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    preview = None
    if "--preview" in sys.argv:
        preview = sys.argv[sys.argv.index("--preview") + 1]
        os.makedirs(preview, exist_ok=True)

    col = json.load(open(os.path.join(ROOT, "tarot", "_collection.json"), encoding="utf-8"))
    slugs = sorted(g["slug"] for g in col["grammars"]
                   if not g.get("is_meta") and g["slug"] != "tree-of-tarot")
    flagged = []
    for slug in slugs:
        try:
            url = HIGH_RES.get(slug) or first_card(slug)
            if not url:
                print(f"  -    {slug}: no image"); continue
            src = tgc_card.fetch(url)
            im = (tgc_card.content_crop(src) if slug in tgc_card.TIGHT_TRIM
                  else tgc_card.autotrim(src))
            mask, bg = tgc_card._flood_bg_mask(im)
            # coverage of the flood area (how much leftover bg is there)
            hist = mask.histogram()
            cover = sum(n for v, n in enumerate(hist) if v > 128) / (im.size[0] * im.size[1])
            lum = sum(bg) / 3
            kind = "BLACK" if lum < 60 else ("WHITE" if lum > 200 else "mid")
            flag = cover > 0.02 and kind != "mid"
            mark = "FLAG" if flag else "ok  "
            print(f"  {mark} {slug:34} bg={bg} ({kind})  cover={cover:.1%}")
            if flag:
                flagged.append(slug)
            if preview and flag:
                before = tgc_card.border_fit(src, blend_frame=(slug in tgc_card.BLEND_FRAME),
                                             tight=(slug in tgc_card.TIGHT_TRIM), flood=False)
                after = tgc_card.border_fit(src, blend_frame=(slug in tgc_card.BLEND_FRAME),
                                            tight=(slug in tgc_card.TIGHT_TRIM), flood=True)
                before.save(os.path.join(preview, f"{slug}-BEFORE.jpg"), "JPEG", quality=90)
                after.save(os.path.join(preview, f"{slug}-AFTER.jpg"), "JPEG", quality=90)
        except Exception as e:
            print(f"  ERR  {slug}: {str(e)[:60]}")
    print(f"\nflagged ({len(flagged)}): {flagged}")
    print(f"current FLOOD_BG: {sorted(tgc_card.FLOOD_BG)}")

if __name__ == "__main__":
    main()
