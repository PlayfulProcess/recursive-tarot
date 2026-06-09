#!/usr/bin/env python3
"""Stamp per-card print readiness into each deck grammar.

Reads print_dims.json  = { "<deck-slug>": { "<item-id>": [w, h], ... }, ... }
(measured in-browser via Image() natural dimensions), and writes
  item.metadata.print = { "w": w, "h": h, "dpi_ready": bool, "bleed": bool }
for every measured card, plus a deck-level "print_readiness" summary on the
grammar root. 300 DPI for a 2.5x3.5in card => 750x1050 (ready), 825x1125 (bleed).
"""
import json, os, sys, glob

READY_W, READY_H = 750, 1050
BLEED_W, BLEED_H = 825, 1125
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAROT = os.path.join(ROOT, "tarot")

def main():
    dims_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "print_dims.json")
    dims = json.load(open(dims_path, encoding="utf-8"))
    total_stamped = 0
    for slug, cards in dims.items():
        gpath = os.path.join(TAROT, slug, "grammar.json")
        if not os.path.exists(gpath):
            continue
        g = json.load(open(gpath, encoding="utf-8"))
        imaged = ready = bleed = 0
        for it in g.get("items", []):
            wh = cards.get(it.get("id"))
            if not wh:
                continue
            w, h = wh[0], wh[1]
            if w <= 0:   # broken / timed-out measurement -> skip (don't claim quality)
                continue
            md = it.setdefault("metadata", {})
            md["print"] = {
                "w": w, "h": h,
                "dpi_ready": bool(w >= READY_W and h >= READY_H),
                "bleed": bool(w >= BLEED_W and h >= BLEED_H),
            }
            imaged += 1
            if md["print"]["dpi_ready"]:
                ready += 1
            if md["print"]["bleed"]:
                bleed += 1
            total_stamped += 1
        real_cards = [i for i in g.get("items", []) if not i.get("composite_of")
                      and i.get("category") not in ("axis", "keyword-emergence")]
        g["print_readiness"] = {
            "cards": len(real_cards), "imaged": imaged,
            "dpi_ready": ready, "bleed_ready": bleed,
            "verdict": ("ready_full_bleed" if imaged and bleed == imaged
                        else "ready_bordered" if imaged and ready == imaged
                        else "partial" if ready else "web_res"),
            "spec": {"card_in": "2.5x3.5", "dpi": 300, "ready_px": [READY_W, READY_H], "bleed_px": [BLEED_W, BLEED_H]},
        }
        json.dump(g, open(gpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  {slug}: {imaged} imaged, {ready} ready, {bleed} bleed -> {g['print_readiness']['verdict']}")
    print(f"stamped {total_stamped} cards across {len(dims)} decks")

if __name__ == "__main__":
    main()
