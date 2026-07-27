# -*- coding: utf-8 -*-
"""One-shot (idempotent) seeder for the deck INDEX fields (Q-INDEX / IDX).

Writes a `common_name` (the short, recognizable display name), `category`
(historical | contemporary | community | reference) and `year` onto each deck
grammar's TOP-LEVEL `metadata`. The grammar file stays the source of truth; the
two generators (build_meta_grammar.py, refresh_collection.py) read these back so
the SAME short name shows in the meta index, the timeline, and every dropdown.

`year` / `year_label` are taken from tarot/_collection.json when already present
there (refresh_collection.py owns those), so we don't duplicate the year table.

Run from repo root:  python scripts/seed_deck_index.py
Re-running only rewrites the three index keys; all other metadata is preserved.
"""
import json, io, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
COLL = os.path.join(ROOT, "tarot", "_collection.json")

# slug -> (common_name, category). The single curated short-name table.
# historical = a real historical artifact/study; contemporary = a modern original
# deck by the project; community = an externally-contributed modern deck;
# reference = apparatus grammar (sources / people / the tree itself).
INDEX = {
 "visconti-sforza-tarot":         ("Visconti-Sforza",            "historical"),
 "cary-yale-visconti-tarot":      ("Cary-Yale Visconti",         "historical"),
 "charles-vi-tarot":              ("'Charles VI' (Ferrara)",     "historical"),
 "este-tarot":                    ("d'Este",                     "historical"),
 "minchiate-florence-tarot":      ("Minchiate",                  "historical"),
 "tarocchino-bologna":            ("Tarocchino di Bologna",      "historical"),
 "sola-busca-tarot":              ("Sola Busca",                 "historical"),
 "mantegna-tarocchi":             ("Mantegna Tarocchi",          "historical"),
 "tarot-de-marseille-conver":     ("Tarot de Marseille (Conver)","historical"),
 "tarot-de-besancon":             ("Tarot de Besançon",          "historical"),
 "noblet-tarot":                  ("Jean Noblet",                "historical"),
 "vieville-tarot":                ("Jacques Viéville",           "historical"),
 "paris-anonymous-tarot":         ("Tarot de Paris",             "historical"),
 "belgian-tarot":                 ("Belgian (Vandenborre)",      "historical"),
 "court-de-gebelin-tarot":        ("Court de Gébelin",           "historical"),
 "etteilla-i-livre-de-thot":      ("Etteilla I",                 "historical"),
 "etteilla-ii-egyptian":          ("Etteilla II",                "historical"),
 "etteilla-iii-oracle-des-dames": ("Etteilla III",              "historical"),
 "oswald-wirth-tarot":            ("Oswald Wirth",               "historical"),
 "golden-dawn-book-t-tarot":      ("Golden Dawn (Book T)",       "historical"),
 "petit-lenormand":               ("Petit Lenormand",            "historical"),
 # ancestors / cousins
 "madiao-money-cards":            ("Ma Diao",                    "historical"),
 "mamluk-deck":                   ("Mamluk",                     "historical"),
 "ganjifa":                       ("Ganjifa",                    "historical"),
 "cary-sheet":                    ("Cary Sheet",                 "historical"),
 "rosenwald-sheet":               ("Rosenwald Sheet",            "historical"),
 # contemporary originals (the project's own interpretive decks)
 "ontoject-illustrated":          ("The Ontoject",               "contemporary"),
 "thirty-six-tattvas":            ("36 Tattvas",                 "contemporary"),
 "anecdotes-tarot":               ("Anecdotes",                  "contemporary"),
 # community-contributed modern decks
 "clown-town-tarot":              ("Clown Town",                 "community"),
 "arlecchinos-augmented-arcana":  ("Arlecchino's Augmented Arcana","community"),
 "tarocchino-arlecchino":         ("Tarocchino Arlecchino",      "community"),
 # reference apparatus
 "books-of-tarot":                ("Books Behind the Tarot",     "reference"),
 "people-of-tarot":               ("People & Institutions",      "reference"),
 "tree-of-tarot":                 ("The Tree of Tarot",          "reference"),
}


def main():
    coll = json.load(io.open(COLL, encoding="utf-8"))
    years = {e["slug"]: (e.get("year"), e.get("year_label")) for e in coll["grammars"]}
    changed = 0
    missing = []
    for e in coll["grammars"]:
        slug = e["slug"]
        if slug not in INDEX:
            missing.append(slug); continue
        common, category = INDEX[slug]
        path = os.path.join(ROOT, e["path"])
        g = json.load(io.open(path, encoding="utf-8"))
        md = g.get("metadata") or {}
        before = dict(md)
        md["common_name"] = common
        md["category"] = category
        yr, yl = years.get(slug, (None, None))
        if yr is not None:
            md["year"] = yr
        if yl is not None:
            md["year_label"] = yl
        if md != before or g.get("metadata") is None:
            g["metadata"] = md
            json.dump(g, io.open(path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            changed += 1
    print("seeded %d grammars; %d unchanged-or-new" % (len(INDEX), changed))
    if missing:
        print("  NOT in INDEX (no common_name written):", ", ".join(missing))


if __name__ == "__main__":
    main()
