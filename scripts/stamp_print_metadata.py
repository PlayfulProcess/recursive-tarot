#!/usr/bin/env python3
"""Stamp per-card print readiness into each deck grammar.

Reads print_codes.json = { "<deck-slug>": "<verdict-string>", ... } where each
char is one card's verdict IN SORTED-ID ORDER (the same order the measurer used):
  0 = web-res (below 300 DPI)   1 = print-ready (>=750x1050)
  2 = print-ready + full bleed (>=825x1125)   x = broken / unmeasured

Writes item.metadata.print = { "dpi_ready": bool, "bleed": bool } for every
measured card, plus a deck-level "print_readiness" summary on the grammar root.
Matching is by sorted item id, so completion-order in the browser doesn't matter.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAROT = os.path.join(ROOT, "tarot")

def real_imaged(items):
    real = [i for i in items if not i.get("composite_of")
            and i.get("category") not in ("axis", "keyword-emergence")
            and (i.get("image_url") or (i.get("metadata") or {}).get("image_url"))]
    return sorted(real, key=lambda i: i.get("id", ""))

def main():
    codes = json.load(open(os.path.join(ROOT, "print_codes.json"), encoding="utf-8"))
    total = 0
    for slug, verdicts in codes.items():
        if slug.startswith("_"):
            continue
        gpath = os.path.join(TAROT, slug, "grammar.json")
        if not os.path.exists(gpath):
            print(f"  !! {slug}: no grammar"); continue
        g = json.load(open(gpath, encoding="utf-8"))
        cards = real_imaged(g.get("items", []))
        if len(cards) != len(verdicts):
            print(f"  !! {slug}: count mismatch (grammar {len(cards)} vs codes {len(verdicts)}) — SKIP")
            continue
        ready = bleed = 0
        for it, c in zip(cards, verdicts):
            if c == "x":
                continue
            md = it.setdefault("metadata", {})
            md["print"] = {"dpi_ready": c in "12", "bleed": c == "2"}
            if c in "12": ready += 1
            if c == "2": bleed += 1
            total += 1
        all_real = [i for i in g.get("items", []) if not i.get("composite_of")
                    and i.get("category") not in ("axis", "keyword-emergence")]
        g["print_readiness"] = {
            "cards": len(all_real), "imaged": len(cards),
            "dpi_ready": ready, "bleed_ready": bleed,
            "verdict": ("ready_full_bleed" if cards and bleed == len(cards)
                        else "ready_bordered" if cards and ready == len(cards)
                        else "partial" if ready else "web_res"),
            "spec": {"card_in": "2.5x3.5", "dpi": 300, "ready_px": [750, 1050], "bleed_px": [825, 1125]},
        }
        json.dump(g, open(gpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"  {slug}: {len(cards)} imaged, {ready} ready, {bleed} bleed -> {g['print_readiness']['verdict']}")
    print(f"stamped {total} cards across {len([k for k in codes if not k.startswith('_')])} decks")

if __name__ == "__main__":
    main()
