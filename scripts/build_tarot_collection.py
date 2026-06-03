# -*- coding: utf-8 -*-
"""Migrate the built tarot grammars into the recursive-tarot repo as community
grammars, attributed to pp@playfulprocess.com, and build tarot/_collection.json.

Reads the already-built + archetype-stamped grammars from the sibling
recursive.eco-schemas repo, adds the community metadata the recursive.eco app
expects (_community_folder / _community_slug / _original_creator / editors[]),
and writes them to tarot/<slug>/grammar.json. Then writes the collection index
(branches + grammar list) used by the static site and the future app importer.

Run from the recursive-tarot repo root:  python scripts/build_tarot_collection.py
"""
import json
import os
import datetime

HERE = os.path.dirname(__file__)
SCHEMAS = os.path.abspath(os.path.join(HERE, "..", "..", "recursive.eco-schemas", "grammars"))
OUT = os.path.abspath(os.path.join(HERE, "..", "tarot"))

PP_ID = "f18e2415-315c-43b7-ae93-d09c8892e181"  # pp@playfulprocess.com
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

# slug -> branch (None branch = the meta-grammar)
DECKS = {
    "visconti-sforza-tarot": "roots",
    "cary-yale-visconti-tarot": "roots",
    "charles-vi-tarot": "b-order",
    "minchiate-florence-tarot": "a-order",
    "tarocchino-bologna": "a-order",
    "tarot-de-marseille-conver": "c-order",
    "tarot-de-besancon": "c-order",
    "oswald-wirth-tarot": "occult",
    "golden-dawn-book-t-tarot": "occult",
    "court-de-gebelin-tarot": "occult",
    "etteilla-i-livre-de-thot": "occult",
    "etteilla-ii-egyptian": "occult",
    "etteilla-iii-oracle-des-dames": "occult",
    "mantegna-tarocchi": "sui-generis",
    "tree-of-tarot": "_meta",
}

BRANCHES = [
    ("roots", "Roots — The First Tarots (Milan, c. 1440s)"),
    ("a-order", "A-Order — Bologna & Florence (the South)"),
    ("b-order", "B-Order — Ferrara (the East)"),
    ("c-order", "C-Order — Milan & the West → the Printed Standard"),
    ("occult", "The Occult Reframing (France → England, 1781→)"),
    ("sui-generis", "Sui Generis & Relatives"),
]


def migrate():
    os.makedirs(OUT, exist_ok=True)
    grammars_index = []
    for slug, branch in DECKS.items():
        src = os.path.join(SCHEMAS, slug, "grammar.json")
        g = json.load(open(src, encoding="utf-8"))
        # community metadata the recursive.eco app expects
        g["_community_folder"] = "tarot"
        g["_community_slug"] = slug
        g["_original_creator"] = PP_ID
        g["creator_name"] = "PlayfulProcess"
        g["creator_link"] = "https://recursive.eco"
        g.setdefault("editors", [])
        if not any(e.get("user_id") == PP_ID for e in g["editors"] if isinstance(e, dict)):
            g["editors"].append({"user_id": PP_ID, "timestamp": NOW, "action": "created"})
        g["is_published"] = True
        out_dir = os.path.join(OUT, slug)
        os.makedirs(out_dir, exist_ok=True)
        json.dump(g, open(os.path.join(out_dir, "grammar.json"), "w", encoding="utf-8"),
                  indent=2, ensure_ascii=False)
        grammars_index.append({
            "slug": slug,
            "name": g.get("name"),
            "type": g.get("grammar_type"),
            "branch": None if branch == "_meta" else branch,
            "is_meta": branch == "_meta",
            "default_preview": g.get("default_preview"),
            "items": len(g.get("items", [])),
            "path": f"tarot/{slug}/grammar.json",
        })

    branch_index = [
        {"id": bid, "name": bname,
         "deck_slugs": [s for s, b in DECKS.items() if b == bid]}
        for bid, bname in BRANCHES
    ]

    collection = {
        "collection": "tarot",
        "name": "The Recursive Tarot",
        "version": "1.0.0",
        "license": "CC-BY-SA-4.0",
        "original_creator": PP_ID,
        "creator_name": "PlayfulProcess",
        "meta_grammar": "tree-of-tarot",
        "branches": branch_index,
        "grammars": grammars_index,
    }
    json.dump(collection, open(os.path.join(OUT, "_collection.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    n_cards = sum(gi["items"] for gi in grammars_index)
    print(f"Migrated {len(grammars_index)} grammars ({n_cards} items) into {OUT}")
    print(f"Wrote {os.path.join(OUT, '_collection.json')} with {len(branch_index)} branches")


if __name__ == "__main__":
    migrate()
