#!/usr/bin/env python3
"""Sampler v6 — the PROOFING PROTOCOL, from scratch.

Per deck, cards are grouped by (print-quality stamp, source host). One
representative card per distinct group — so a deck whose majors and minors come
from different scans/qualities (e.g. Etteilla III: 22 print majors + 56 web
minors) contributes one card from EACH group, and a uniform deck contributes one.
Representatives prefer a trump/major for the first group and a pip for an
all-minor group, so the proof spans the deck's visual range.

Every card runs through the SHARED tgc_card pipeline (autotrim / TIGHT_TRIM /
BLEND_FRAME / FLOOD_BG) — identical to whole-deck product bakes, so what this
proof shows is exactly what products will ship. Decks with high-res IIIF archives
(vieville / paris / este) are re-pulled at print width per card via
prebake_deck_r2.high_res_url.

Output: print/decks/sampler-v6-tgc/  (900x1500 JPEGs, numbered)
        print/decks/sampler-v6-tgc/manifest.json  (deck, group, quality, source —
        feeds tgc_upload_deck.py and documents the proof)

Usage: python scripts/build_sampler_v6.py
"""
import json, os, sys, glob
from urllib.parse import urlparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tgc_card
from prebake_deck_r2 import high_res_url, fetch_retry

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "print", "decks", "sampler-v6-tgc")

SKIP = {"all-decks-many-lenses", "test", "tree-of-tarot"}

def eligible(items):
    out = []
    for it in items:
        if it.get("composite_of") or it.get("category") in ("axis", "keyword-emergence"):
            continue
        u = it.get("image_url") or (it.get("metadata") or {}).get("image_url")
        if u:
            out.append((it, u))
    return out

def kind_of(it):
    cat = (it.get("category") or "").lower()
    return "major" if ("major" in cat or "trump" in cat) else "minor"

def quality_stamp(it):
    return (((it.get("metadata") or {}).get("print")) or {}).get("quality", "?")

def main():
    os.makedirs(OUT, exist_ok=True)
    col = json.load(open(os.path.join(ROOT, "tarot", "_collection.json"), encoding="utf-8"))
    slugs = sorted(g["slug"] for g in col["grammars"]
                   if not g.get("is_meta") and g["slug"] not in SKIP)
    manifest = {"version": "v6", "spec": "900x1500 TGC tarot", "cards": [], "backs": []}
    n = 0
    for slug in slugs:
        g = json.load(open(os.path.join(ROOT, "tarot", slug, "grammar.json"), encoding="utf-8-sig"))
        cards = eligible(g.get("items", []))
        if not cards:
            print(f"  skip {slug}: no card images"); continue
        # group by (quality, host)
        gmap = {}
        for it, u in cards:
            key = (quality_stamp(it), urlparse(u).netloc)
            gmap.setdefault(key, []).append((it, u))
        # one representative per group; prefer a major, else a mid-deck pip
        for key, its in sorted(gmap.items()):
            majors = [(it, u) for it, u in its if kind_of(it) == "major"]
            pool = majors or its
            it, u = pool[len(pool) // 2]
            kind = kind_of(it)
            label = kind + "s" if len(gmap) > 1 else "deck"
            try:
                hr = high_res_url(slug, u)
                try:
                    src = tgc_card.fetch(hr) if hr else fetch_retry(u)
                except Exception:
                    src = fetch_retry(u)   # archive hiccup -> display copy
                tier = "READY" if min(src.size) >= tgc_card.PRINT_MIN else "WEBRES"
                im = tgc_card.border_fit(src,
                                         blend_frame=(slug in tgc_card.BLEND_FRAME),
                                         tight=(slug in tgc_card.TIGHT_TRIM),
                                         flood=(slug in tgc_card.FLOOD_BG))
                n += 1
                fname = f"{n:02d} - {tier} - {slug[:24]} - {label}.jpg"
                im.save(os.path.join(OUT, fname), "JPEG", quality=92)
                manifest["cards"].append({
                    "file": fname, "deck": slug, "group": label, "tier": tier,
                    "card_id": it.get("id"), "card_name": it.get("name"),
                    "quality_stamp": key[0], "source_host": key[1],
                    "group_size": len(its),
                    "flood": slug in tgc_card.FLOOD_BG,
                    "source_px": list(src.size)})
                print(f"  {n:02d} {tier:6} {slug:30} {label:7} ({it.get('id')}, {src.size[0]}x{src.size[1]})")
            except Exception as e:
                print(f"  FAIL {slug} {label}: {str(e)[:60]}")
    # card backs — every historical back, cover-fit (borderless by design)
    bpath = os.path.join(ROOT, "print", "card-backs.json")
    if os.path.exists(bpath):
        for k, b in enumerate(json.load(open(bpath, encoding="utf-8")).get("items", []), 1):
            u = b.get("image_url")
            if not u: continue
            try:
                im = tgc_card.cover_fit(tgc_card.autotrim(tgc_card.fetch(u)))
                fname = f"B{k:02d} - BACK - {b['id'][5:28]}.jpg"
                im.save(os.path.join(OUT, fname), "JPEG", quality=92)
                manifest["backs"].append({"file": fname, "id": b["id"]})
                print(f"  BACK   {b['id']}")
            except Exception as e:
                print(f"  FAIL back {b['id']}: {str(e)[:40]}")
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nsampler v6: {n} fronts + {len(manifest['backs'])} backs -> {OUT}")
    print("manifest.json written — feed it to tgc_upload_deck.py")

if __name__ == "__main__":
    main()
