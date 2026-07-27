#!/usr/bin/env python3
"""Transform a platform (recursive.eco) Yve Lepkowski deck export into a
repo grammar.json under tarot/<slug>/, with:
  - provenance 'living' + worldview 'contemporary' (so the genealogy/meta can keep a clean historical cut)
  - full CC-BY-SA-4.0 attribution to Yve Lepkowski (license travels with the work)
  - per-card archetype mapping so the deck still joins the cross-deck lenses
The source JSON is a get_grammar dump saved to a tool-results .txt file.
Run: python scripts/import_yve_deck.py <saved_json.txt> <slug>
"""
import json, sys, re

ARCANA = {
    "The Magician":"the-magician","The High Priestess":"the-high-priestess","The Empress":"the-empress",
    "The Emperor":"the-emperor","The Hierophant":"the-hierophant","The Lovers":"the-lovers",
    "The Chariot":"the-chariot","Temperance":"temperance","Justice":"justice","Strength":"strength",
    "Wheel of Fortune":"wheel-of-fortune","The Hermit":"the-hermit","The Hanged Man":"the-hanged-man",
    "Death":"death","The Devil":"the-devil","The Tower":"the-tower","The Star":"the-star",
    "The Moon":"the-moon","The Sun":"the-sun","The World":"the-world","Judgement":"judgement","The Fool":"the-fool",
}
SUIT = {  # English suit in the card name -> (archetype-suit, element, italian)
    "Batons":("wands","Fire","Bastoni"),"Cups":("cups","Water","Coppe"),
    "Swords":("swords","Air","Spade"),"Coins":("coins","Earth","Denari"),
}
RANKS = {"King","Queen","Knight","Page","Maid","Ace","Ten","Nine","Eight","Seven","Six"}
COURTS = {"King","Queen","Knight","Page","Maid"}

def english(name):
    m = re.search(r"\(([^)]+)\)", name)
    return m.group(1).strip() if m else name.strip()

def classify(card):
    """Return (category, metadata-additions) for one source card."""
    en = english(card["name"])
    if card.get("category") == "major" or en in ARCANA:
        slug = ARCANA.get(en)
        meta = {"arcana":"trump","archetype":(f"arcana:{slug}" if slug else None),
                "mapping_confidence":"exact" if slug else "none"}
        return "trump", meta
    # minor: parse "<Rank> of <Suit>"
    mm = re.match(r"(King|Queen|Knight|Page|Maid|Ace|Ten|Nine|Eight|Seven|Six) of (\w+)", en)
    if mm:
        rank, suit_en = mm.group(1), mm.group(2)
        a_suit, element, ital = SUIT.get(suit_en, (suit_en.lower(),"",""))
        is_court = rank in COURTS
        arche = None if is_court else f"card:{rank.lower()}-of-{a_suit}"
        meta = {"arcana":"minor","suit":suit_en,"suit_italian":ital,"element":element,
                "rank":rank,"court":is_court,"archetype":arche,
                "mapping_confidence":"none" if is_court else "exact"}
        return f"suit-{a_suit}", meta
    return "card", {"arcana":"minor","archetype":None,"mapping_confidence":"none"}

def main():
    src_file, slug = sys.argv[1], sys.argv[2]
    g = json.loads(open(src_file, encoding="utf-8").read())
    src_items = g["items"]
    creator_link = "https://stolen-thyme.com/tarocchino-arlecchino/"
    cover = next((it.get("image_url") for it in src_items if it.get("image_url")), None)

    items = []
    for i, c in enumerate(src_items):
        cat, meta_add = classify(c)
        img = c.get("image_url")
        meta = {"tradition":"contemporary-bolognese","era":"contemporary"}
        meta.update(meta_add)
        if img:
            meta["illustrations"] = [{"url":img,"artist":"Yve Lepkowski",
                "license":"CC-BY-SA-4.0","source":creator_link,
                "note":"Image currently hot-linked from the platform mirror (Google Drive); mirror to R2 in a follow-up."}]
        items.append({
            "id": c.get("id", f"card-{i}"),
            "name": c["name"],
            "sort_order": i,
            "category": cat,
            "keywords": c.get("keywords", []),
            "sections": c.get("sections", {}),
            "image_url": img,
            "metadata": meta,
        })
    # the two unnumbered Etteilla-style Significators that make Yve's deck 64 (vs the 62-card tarocchino)
    for n, who in [("Significator I — The Querent", "the consultant who lays the cards"),
                   ("Significator II — The Querent", "a second consultant / the person enquired about")]:
        items.append({
            "id": f"significator-{len(items)}",
            "name": n,
            "sort_order": len(items),
            "category": "significator",
            "keywords": ["significator","querent","the self"],
            "sections": {"Summary": f"An unnumbered Significator representing {who}. "
                "Yve Lepkowski's Tarocchino Arlecchino keeps two unnumbered Significators in the "
                "Etteilla tradition (the Fool sits at no. 61; the two Significators carry no number), "
                "which is why the deck is 64 cards rather than the standard 62-card tarocchino.",
                "Note": "Card art to be sourced from Yve Lepkowski's deck files (stolen-thyme.com) in a follow-up; "
                "added here so the deck's count is faithful to the source (64)."},
            "image_url": None,
            "metadata": {"arcana":"significator","archetype":None,"mapping_confidence":"none",
                "tradition":"contemporary-bolognese","era":"contemporary"},
        })

    out = {
        "_community_slug": slug,
        "name": g.get("name","Tarocchino Arlecchino"),
        "slug": slug,
        "grammar_type": "tarot",
        "provenance": "living",
        "worldview": "contemporary",
        "creator_name": "Yve Lepkowski",
        "creator_link": creator_link,
        "cover_image_url": cover,
        "image_credit": "Art by Yve Lepkowski (stolen-thyme.com), CC-BY-SA-4.0.",
        "description": (g.get("description","") + "\n\n"
            "**A contemporary deck.** Created by Yve Lepkowski (stolen-thyme.com) and released under "
            "CC-BY-SA-4.0; reproduced here under the same licence. A 64-card deck: the 62-card Bolognese "
            "tarocchino (21 numbered trumps, the Fool, and 40 suit cards) plus two unnumbered Etteilla-style "
            "Significators. It descends from the historical **Tarocchino di Bologna** in this library."),
        "tags": ["tarot","tarocchino","arlecchino","harlequin","commedia-dellarte","bolognese",
                 "etteilla","contemporary","cc-by-sa","yve-lepkowski"],
        "roots": ["western-esoteric"],
        "lineages": ["tarocchino-bologna"],
        "parent_deck": "tarocchino-bologna",
        "is_published": True,
        "_grammar_commons": {
            "schema_version":"1.0","license":"CC-BY-SA-4.0",
            "license_url":"https://creativecommons.org/licenses/by-sa/4.0/",
            "attribution":[
                {"name":"Yve Lepkowski","role":"artist & deck creator","link":"https://stolen-thyme.com",
                 "note":"Tarocchino Arlecchino — original deck, CC-BY-SA-4.0 (stolen-thyme.com/tarocchino-arlecchino)."},
                {"name":"PlayfulProcess","role":"compiled into this library as a recursive.eco grammar","link":"https://recursive.eco"},
            ],
            "modifications":"Restructured Yve Lepkowski's deck into the recursive.eco grammar schema; "
                "added cross-deck archetype mappings and genealogy links; the two unnumbered Significators "
                "are represented as explicit items. No card meanings were altered.",
        },
        "items": items,
    }
    import os
    d = f"tarot/{slug}"
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(f"{d}/grammar.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {d}/grammar.json — {len(items)} cards ("
          f"{sum(1 for x in items if x['category']=='trump')} trumps, "
          f"{sum(1 for x in items if x['category'].startswith('suit-'))} pips/courts, "
          f"{sum(1 for x in items if x['category']=='significator')} significators)")

if __name__ == "__main__":
    main()
