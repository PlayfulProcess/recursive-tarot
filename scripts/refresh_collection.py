# -*- coding: utf-8 -*-
"""Refresh tarot/_collection.json DERIVED fields from the actual grammar files.

The grammars are the source of truth; this re-syncs each registry entry's name, type,
items count, cover_image_url, default_preview and blurb from tarot/<slug>/grammar.json.
It PRESERVES curation (branches, deck_slugs, slug/branch/is_meta/path, top-level fields)
and only rewrites the derived fields. Idempotent.

Run from repo root:  python3 scripts/refresh_collection.py
"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COLL = os.path.join(ROOT, "tarot", "_collection.json")

# Curated catalogue date per deck: (sort_year, display label). Grounded in the deck
# dossiers; roots/ancestors lead. Edit here to re-order the deck picker.
YEARS = {
    "madiao-money-cards":            (1400, "money cards, 14th–15th c."),
    "mamluk-deck":                   (1400, "c. 1400 (Topkapı c. 1500)"),
    "cary-yale-visconti-tarot":      (1442, "c. 1442"),
    "este-tarot":                    (1450, "c. 1450"),
    "visconti-sforza-tarot":         (1451, "c. 1451"),
    "charles-vi-tarot":              (1455, "c. 1450–80"),
    "mantegna-tarocchi":             (1465, "c. 1465"),
    "sola-busca-tarot":              (1491, "1491"),
    "cary-sheet":                    (1500, "c. 1500"),
    "rosenwald-sheet":               (1500, "c. 1500"),
    "minchiate-florence-tarot":      (1506, "c. 1506+"),
    "ganjifa":                       (1520, "16th c.+"),
    "paris-anonymous-tarot":         (1625, "c. 1600–50"),
    "noblet-tarot":                  (1650, "c. 1650"),
    "vieville-tarot":                (1650, "c. 1650"),
    "tarocchino-bologna":            (1660, "17th c."),
    "tarot-de-marseille-conver":     (1760, "1760"),
    "court-de-gebelin-tarot":        (1781, "1781"),
    "belgian-tarot":                 (1780, "c. 1780"),
    "tarot-de-besancon":             (1800, "18th–19th c."),
    "etteilla-i-livre-de-thot":      (1789, "1788–89"),
    "etteilla-ii-egyptian":          (1838, "c. 1838"),
    "etteilla-iii-oracle-des-dames": (1865, "c. 1865"),
    "oswald-wirth-tarot":            (1889, "1889"),
    "golden-dawn-book-t-tarot":      (1909, "1888 · RWS 1909"),
}


def blurb_of(g):
    desc = (g.get("description") or "").strip().split("\n")[0]
    return (desc[:200] + "…") if len(desc) > 200 else desc


def main():
    c = json.load(open(COLL, encoding="utf-8"))
    changed = []
    for e in c.get("grammars", []):
        path = os.path.join(ROOT, e["path"])
        if not os.path.exists(path):
            print("  MISSING grammar:", e["path"]); continue
        g = json.load(open(path, encoding="utf-8"))
        new = {
            "name": g.get("name"),
            "type": g.get("grammar_type"),
            "default_preview": g.get("default_preview"),
            "items": len(g.get("items", [])),
            "cover_image_url": g.get("cover_image_url"),
            "blurb": blurb_of(g),
        }
        if e["slug"] in YEARS:
            new["year"], new["year_label"] = YEARS[e["slug"]]
        # Two Wings: derive provenance from the grammar file when present (the file
        # is the source of truth); leave the registry value untouched otherwise.
        if g.get("provenance"):
            new["provenance"] = g["provenance"]
        for k, v in new.items():
            if e.get(k) != v:
                changed.append(f"{e['slug']}.{k}")
                e[k] = v
    json.dump(c, open(COLL, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"refreshed {len(c['grammars'])} entries; {len(changed)} fields changed")
    for ch in changed:
        print("   ~", ch)


if __name__ == "__main__":
    main()
