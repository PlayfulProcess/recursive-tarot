# -*- coding: utf-8 -*-
"""Generate tarot/people-of-tarot/grammar.json from research/people/*.md dossiers.

The dossiers are the SINGLE SOURCE OF TRUTH for people & institutions; this grammar
is a generated projection (like the meta). To change a person, edit their dossier and
re-run this script. Idempotent.

Dossier frontmatter fields used here (see research/SCHEMA.md):
  id, type(person|institution), title, summary, role_group, lifespan, roles[],
  made[](deck slugs), features_cards[], status, confidence
Body sections pulled into the leaf: "At a glance", "The claim vs the record",
"How they appear in this collection".

Run from repo root:  python3 scripts/build_people_grammar.py
"""
import json, os, re, sys, glob
import yaml

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
PEOPLE_DIR = os.path.join(ROOT, "research", "people")
TAROT_DIR = os.path.join(ROOT, "tarot")
OUT = os.path.join(TAROT_DIR, "people-of-tarot", "grammar.json")

# Bibliography for every [@key] cited in the dossier text pulled into this grammar.
# Resolved against research/bibliography.bib (Oct 4 2026 audit). Entries without a
# urldate/url match in that file are flagged "(source to confirm)" rather than
# invented — see docs/AUDIT-sibling-repos-2026-10-04.md in recursive-eco.
BIBLIOGRAPHY = [
    {"key": "decker1996", "author": "Ronald Decker, Thierry Depaulis and Michael Dummett", "title": "A Wicked Pack of Cards: The Origins of the Occult Tarot", "year": 1996},
    {"key": "decker2002", "author": "Ronald Decker and Michael Dummett", "title": "A History of the Occult Tarot, 1870–1970", "year": 2002},
    {"key": "depaulis1984", "author": "Thierry Depaulis", "title": "Tarot, jeu et magie", "year": 1984},
    {"key": "dummett1980", "author": "Michael Dummett", "title": "The Game of Tarot: From Ferrara to Salt Lake City", "year": 1980},
    {"key": "dummett2004", "author": "Michael Dummett and John McLeod", "title": "A History of Games Played with the Tarot Pack", "year": 2004},
    {"key": "levi1856", "author": "Éliphas Lévi", "title": "Dogme et rituel de la haute magie", "year": 1856},
    {"key": "moakley1966", "author": "Gertrude Moakley", "title": "The Tarot Cards Painted by Bonifacio Bembo for the Visconti-Sforza Family", "year": 1966},
    {"key": "pratesi_ferrara", "title": "pratesi_ferrara (source to confirm)"},
    {"key": "pratesi_marziano", "title": "pratesi_marziano (source to confirm)"},
    {"key": "tarot_heritage", "title": "Tarot Heritage", "url": "https://tarot-heritage.com"},
    {"key": "waite1910", "author": "Arthur Edward Waite", "title": "The Pictorial Key to the Tarot", "year": 1910},
    {"key": "web_beinecke_visconti", "title": "Visconti Tarot", "url": "https://beinecke.library.yale.edu", "note": "Beinecke Rare Book & Manuscript Library, Yale"},
    {"key": "web_belgian_wp", "title": "Belgian Tarot", "url": "https://en.wikipedia.org/wiki/Belgian_Tarot", "note": "Wikipedia"},
    {"key": "web_bembo_wp", "title": "Bonifacio Bembo", "url": "https://en.wikipedia.org/wiki/Bonifacio_Bembo", "note": "Wikipedia"},
    {"key": "web_bianca_wp", "title": "Bianca Maria Visconti", "url": "https://en.wikipedia.org/wiki/Bianca_Maria_Visconti", "note": "Wikipedia"},
    {"key": "web_bnf_conver", "title": "Nicolas Conver (1784–1833)", "url": "https://data.bnf.fr/en/16721159/nicolas_conver/", "note": "data.bnf.fr"},
    {"key": "web_bnf_noblet", "title": "Tarot de Jean Noblet", "url": "https://essentiels.bnf.fr", "note": "BnF Essentiels"},
    {"key": "web_camoin_conver", "title": "The Tarot of Nicolas Conver", "url": "https://en.camoin.com", "note": "Camoin"},
    {"key": "web_camoin_conver1760", "title": "The 1760 Edition of Nicolas Conver", "url": "https://en.camoin.com", "note": "Camoin"},
    {"key": "web_charlesvi_th", "title": "The Fifteenth-Century Charles VI Deck Recreated by Marco Benedetti", "url": "https://tarot-heritage.com/2021/01/28/", "year": 2021, "note": "Tarot Heritage"},
    {"key": "web_druidcraft", "title": "The Etteilla Tarot: Type I (1788), Type II (1840), Type III (1870)", "url": "https://druidcraftblog.wordpress.com", "note": "Morsoth's Druidcraft"},
    {"key": "web_este_wp", "title": "web_este_wp (source to confirm)"},
    {"key": "web_filippo_wp", "title": "Filippo Maria Visconti", "url": "https://en.wikipedia.org/wiki/Filippo_Maria_Visconti", "note": "Wikipedia"},
    {"key": "web_francesco_wp", "title": "Francesco I Sforza", "url": "https://en.wikipedia.org/wiki/Francesco_I_Sforza", "note": "Wikipedia"},
    {"key": "web_gd_nodeck", "author": "Steve P.", "title": "The Golden Dawn Tarot — notes on Book T and the unpublished Order deck", "url": "https://steve-p.org/cards/GDaw.html"},
    {"key": "web_gd_swap", "title": "The “Golden Dawn Swap” — Strength and Justice", "url": "https://parsifalswheeldivination.org", "year": 2023, "note": "Parsifal's Wheel"},
    {"key": "web_grand_etteilla", "title": "Grand Etteilla I/II/III — editions and attributions (Blocquel / “Julia Orsini” / Régamey / Grimaud)", "url": "https://benebellwen.com/etteilla/", "note": "Reconstruction notes"},
    {"key": "web_harrington_wirth", "title": "Le Tarot des imagiers du moyen age (Oswald Wirth, 1926/1927) — bibliographic description", "url": "https://www.peterharrington.co.uk", "note": "Peter Harrington Rare Books"},
    {"key": "web_hrmtc_first", "title": "The First Occult Tarot", "url": "https://library.hrmtc.com", "note": "The Hermetic Library Blog"},
    {"key": "web_letarot_vieville", "title": "Tarot de Jacques Viéville", "url": "https://www.letarot.com/les-tarots/jacques-vieville/", "note": "Le Tarot"},
    {"key": "web_levi_rota", "title": "French Occult Tarot — Éliphas Lévi and the ROTA/TARO wheel", "url": "https://tarot-heritage.com/history-4/french-occult-tarot/", "note": "Tarot Heritage"},
    {"key": "web_mantegna_wopc", "title": "Tarocchi di Mantegna, c.1465", "url": "https://www.wopc.co.uk/italy/tarocchi-di-mantegna-c.1465", "note": "WOPC"},
    {"key": "web_mantegna_wp", "title": "Mantegna Tarocchi", "url": "https://en.wikipedia.org/wiki/Mantegna_Tarocchi", "note": "Wikipedia"},
    {"key": "web_marziano_wp", "title": "web_marziano_wp (source to confirm)"},
    {"key": "web_mathers_wp", "title": "Samuel Liddell MacGregor Mathers", "url": "https://en.wikipedia.org/wiki/Samuel_Liddell_MacGregor_Mathers", "note": "Wikipedia"},
    {"key": "web_mellet_search", "title": "Biographical Notes: Louis-Raphaël-Lucrèce de Fayolle, comte de Mellet", "url": "http://www.autorbis.net/tarot/", "note": "autorbis.net"},
    {"key": "web_met_bembo", "title": "Workshop of Bonifacio Bembo — Visconti-Sforza Tarot cards", "url": "https://www.metmuseum.org/art/collection/search/697871", "note": "The Metropolitan Museum of Art"},
    {"key": "web_pcs_artnet", "author": "Sarah Cascone", "title": "Pamela Colman Smith, the Artist Who Designed the Iconic Tarot Deck", "url": "https://news.artnet.com", "note": "Artnet News"},
    {"key": "web_pcs_wp", "title": "Pamela Colman Smith", "url": "https://en.wikipedia.org/wiki/Pamela_Colman_Smith", "note": "Wikipedia"},
    {"key": "web_petrarch_wp", "title": "web_petrarch_wp (source to confirm)"},
    {"key": "web_pkt_wp", "title": "The Pictorial Key to the Tarot", "url": "https://en.wikipedia.org/wiki/The_Pictorial_Key_to_the_Tarot", "note": "Wikipedia"},
    {"key": "web_place_mellet", "author": "Robert M. Place", "title": "Who was the comte de Mellet?", "url": "https://robertmplacetarot.com"},
    {"key": "web_pratesi_site", "title": "web_pratesi_site (source to confirm)"},
    {"key": "web_rider_wp", "title": "Rider (imprint) / William Rider & Son", "url": "https://en.wikipedia.org/wiki/Rider_(imprint)", "note": "Wikipedia"},
    {"key": "web_rws_faq", "title": "The Rider-Waite-Smith Tarot Copyright FAQ", "url": "https://sacred-texts.com/tarot/faq.htm", "note": "Sacred Text Archive"},
    {"key": "web_rws_wopc", "title": "Rider-Waite Tarot", "url": "https://www.wopc.co.uk/tarot/rider-waite/", "note": "WOPC"},
    {"key": "web_sb_ciompi", "title": "Meaning of the Sola Busca Tarot (suit-emblems; named courts Amone / Olinpia / Natanabo; Pages unnamed; card numbering 11–14)", "url": "https://www.arte-dei-ciompi-firenze.it/en-meaning-sola-busca-tarot", "note": "L'Arte de' Ciompi, Firenze"},
    {"key": "web_sb_wp", "title": "Sola Busca tarot", "url": "https://en.wikipedia.org/wiki/Sola_Busca_tarot", "note": "Wikipedia"},
    {"key": "web_tdm_wopc", "title": "web_tdm_wopc (source to confirm)"},
    {"key": "web_tdm_wp", "title": "web_tdm_wp (source to confirm)"},
    {"key": "web_th_rouen_bruxelles", "title": "Rouen-Bruxelles tarot pattern", "url": "https://tarot-heritage.com/tag/rouen-bruxelles/", "note": "Tarot Heritage"},
    {"key": "web_th_spanish_captain", "title": "The Spanish Captain in the Vandenborre Deck", "url": "https://tarot-heritage.com/2015/10/22/the-spanish-captain-in-the-vandenborre-deck/", "note": "Tarot Heritage"},
    {"key": "web_vs_conver_heritage", "title": "1760 Nicolas Conver", "url": "https://tarot-de-marseille-heritage.com/1760-nicolas-conver/", "note": "Tarot de Marseille Héritage"},
    {"key": "web_vs_wp", "title": "Visconti-Sforza Tarot", "url": "https://en.wikipedia.org/wiki/Visconti-Sforza_Tarot", "note": "Wikipedia"},
    {"key": "web_westcott_wp", "title": "William Wynn Westcott", "url": "https://en.wikipedia.org/wiki/William_Wynn_Westcott", "note": "Wikipedia"},
    {"key": "web_wirth_wp", "title": "Oswald Wirth", "url": "https://en.wikipedia.org/wiki/Oswald_Wirth", "note": "Wikipedia"},
    {"key": "web_wopc_handpainted", "title": "Hand-Painted Tarocchi Cards", "url": "https://www.wopc.co.uk/italy/hand-painted-tarocchi-cards", "note": "WOPC"},
    {"key": "web_wopc_monde", "title": "Le Monde Primitif Tarot", "url": "https://www.wopc.co.uk/tarot/monde-primitif-tarot", "note": "The World of Playing Cards"},
    {"key": "web_wopc_noblet", "title": "Jean Noblet Tarot de Marseille", "url": "https://www.wopc.co.uk/france/jean-noblet-tarot-de-marseille", "note": "WOPC"},
    {"key": "web_wopc_vandenborre", "title": "Vandenborre Tarot", "url": "https://www.wopc.co.uk/belgium/vandenborre-tarot", "note": "WOPC"},
    {"key": "web_wopc_vs", "title": "The Visconti-Sforza Tarot, c.1460", "url": "https://www.wopc.co.uk/italy/the-visconti-sforza-tarot-c.1460", "note": "WOPC"},
]

# role_group -> (L2 id, L2 label, sort)
GROUPS = {
    "makers":       ("grp-makers",       "Makers, Engravers & Printers", 1),
    "patrons":      ("grp-patrons",      "Patrons & Commissioners", 2),
    "occultists":   ("grp-occultists",   "Occultists & System-Builders", 3),
    "scholars":     ("grp-scholars",     "Scholars & Cataloguers", 4),
    "institutions": ("grp-institutions", "Holding Institutions & Publishers", 5),
}

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.S)


def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = FM_RE.match(raw)
    if not m:
        return None, None
    fm = yaml.safe_load(m.group(1)) or {}
    body = m.group(2)
    return fm, body


def section(body, *titles):
    """Return the text of the first matching '## <title>' section, trimmed."""
    for t in titles:
        m = re.search(r"^##\s+" + re.escape(t) + r"\s*\n(.*?)(?=^##\s|\Z)", body, re.S | re.M)
        if m:
            return m.group(1).strip()
    return ""


def known_deck_slugs():
    return {os.path.basename(p) for p in glob.glob(os.path.join(TAROT_DIR, "*")) if os.path.isdir(p)}


# Cache: deck slug -> (short_label, representative_card_id) for person->deck pills.
_DECK_CACHE = {}


def deck_label_and_target(slug):
    """Short human label + a real item id to deep-link to, for a person->deck pill.
    The pill needs a source_item_id that exists in the target grammar; we prefer the
    first level-1 card, falling back to the first item. Label = name before the dash."""
    if slug in _DECK_CACHE:
        return _DECK_CACHE[slug]
    path = os.path.join(TAROT_DIR, slug, "grammar.json")
    label, target = slug, None
    try:
        g = json.load(open(path, encoding="utf-8"))
        label = re.split(r"\s[—–-]\s", g.get("name", slug))[0].strip() or slug
        items = g.get("items", []) or []
        for it in items:
            if it.get("level") == 1 and it.get("id"):
                target = it["id"]
                break
        if not target and items:
            target = items[0].get("id")
    except Exception:
        pass
    _DECK_CACHE[slug] = (label, target)
    return label, target


def make_pill(fm, decks):
    """One cross-link pill per person, in priority order:
       1. book:  -> Books Behind the Tarot (a real book-* item)
       2. features_cards: -> the first specific card that features them
       3. made:  -> the deck they made (first level-1 card as the landing item)
    Returns the three pill keys (source_deck/source_item_id/deck) or {}."""
    book = fm.get("book")
    if book:
        book_id = book if str(book).startswith("book-") else "book-" + str(book)
        return {"source_deck": "books-of-tarot", "source_item_id": book_id,
                "deck": "Books Behind the Tarot"}
    feats = fm.get("features_cards") or []
    if feats and ":" in str(feats[0]):
        d, _, card = str(feats[0]).partition(":")
        if d in decks:
            label, _t = deck_label_and_target(d)
            return {"source_deck": d, "source_item_id": card, "deck": label}
    made = fm.get("made") or []
    for slug in made:
        if slug in decks:
            label, target = deck_label_and_target(slug)
            if target:
                return {"source_deck": slug, "source_item_id": target, "deck": label}
    return {}


def build():
    decks = known_deck_slugs()
    people = []
    warnings = []
    for path in sorted(glob.glob(os.path.join(PEOPLE_DIR, "*.md"))):
        fm, body = parse(path)
        if not fm or not fm.get("id"):
            warnings.append(f"skip (no frontmatter/id): {os.path.basename(path)}")
            continue
        rg = fm.get("role_group")
        if rg not in GROUPS:
            warnings.append(f"unknown role_group '{rg}' in {os.path.basename(path)}; skipping")
            continue
        for field in ("made", "studied"):
            for slug in fm.get(field, []) or []:
                if slug not in decks:
                    warnings.append(f"{fm['id']}: {field}[] references unknown deck '{slug}'")
        people.append((fm, body, path))

    items = []
    group_members = {gid: [] for gid, _, _ in GROUPS.values()}

    for sort_i, (fm, body, path) in enumerate(people, 1):
        gid, _, _ = GROUPS[fm["role_group"]]
        leaf_id = "person-" + fm["id"]
        group_members[gid].append(leaf_id)
        sections = {}
        glance = section(body, "At a glance")
        if glance:
            sections["Who"] = glance
        claim = section(body, "The claim vs the record", "The claim vs. the record")
        if claim:
            sections["Claim vs the record"] = claim
        coll = section(body, "How they appear in this collection")
        if coll:
            sections["In this collection"] = coll
        if not sections:
            sections["Who"] = fm.get("summary", fm.get("title", fm["id"]))
        meta = {
            "kind": fm.get("type", "person"),
            "role_group": fm["role_group"],
            "lifespan": fm.get("lifespan"),
            "roles": fm.get("roles", []),
            "made": fm.get("made", []),
            "studied": fm.get("studied", []),
            "features_cards": fm.get("features_cards", []),
            "confidence": fm.get("confidence"),
            # posix path so Windows and Linux/CI builds produce identical output
            "research": os.path.relpath(path, ROOT).replace(os.sep, "/"),
            # the Wikipedia (or canonical) redirect, rendered as the item's external link
            "url": fm.get("wikipedia"),
            # excessive-attribution credit string for the portrait (PD/CC images)
            "image_credit": fm.get("image_credit"),
        }
        # one cross-link pill (book > featured-card > made-deck)
        meta.update(make_pill(fm, decks))
        item = {
            "id": leaf_id,
            "name": fm.get("title", fm["id"]),
            "level": 1,
            "category": fm.get("type", "person"),
            "sort_order": sort_i,
            "keywords": [r for r in fm.get("roles", [])] + [fm.get("role_group")],
            "metadata": {k: v for k, v in meta.items() if v not in (None, [], "")},
            "sections": sections,
        }
        if fm.get("image"):
            item["image_url"] = fm["image"]
        items.append(item)

    # L2 group nodes (only those with members), L3 root
    root_children = []
    for rg, (gid, label, gsort) in sorted(GROUPS.items(), key=lambda kv: kv[1][2]):
        members = group_members[gid]
        if not members:
            continue
        items.append({
            "id": gid,
            "name": label,
            "level": 2,
            "category": "role-group",
            "sort_order": 100 + gsort,
            "composite_of": members,
            "sections": {"What this groups": f"{len(members)} {label.lower()} catalogued in this collection."},
        })
        root_children.append(gid)

    items.append({
        "id": "root-people-of-tarot",
        "name": "The Hands Behind the Cards",
        "level": 3,
        "category": "root",
        "sort_order": 999,
        "composite_of": root_children,
        "sections": {"What it is": "Every person and institution that made, paid for, reframed, printed, or catalogued the decks in this collection — generated from the research/people dossiers."},
    })

    grammar = {
        "_grammar_commons": {"schema_version": "1.0", "license": "CC-BY-SA-4.0",
                             "attribution": [{"name": "PlayfulProcess",
                                              "note": "Generated from research/people dossiers; for maintainer + Tarot History Forum review."}]},
        "name": "People & Institutions of Tarot — The Hands Behind the Cards",
        "slug": "people-of-tarot",
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "creator_link": "https://recursive.eco",
        "default_view": "tree",
        "default_preview": "tree",
        "provenance": "reference",  # apparatus grammar — see docs/DESIGN-two-wings-provenance.md
        "_generated": True,
        "_do_not_hand_edit": True,
        "_built_by": "scripts/build_people_grammar.py",
        "_source_of_truth": "research/people/*.md",
        "description": "The makers, patrons, occultists, scholars, and institutions behind the historical tarot decks in this collection. Each node links to the deck(s) that person or body made, reframed, printed, or holds — and, where specific, to the cards that feature them (e.g. Pamela Colman Smith's scenes in the RWS deck). Generated from the research/people dossiers, which carry the sourced evidence.",
        "tags": ["people", "history", "tarot", "biography", "institutions"],
        "is_published": True,
        "bibliography": BIBLIOGRAPHY,
        "items": items,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(grammar, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    n_people = sum(1 for it in items if it.get("level") == 1)
    print(f"people={n_people} groups={len(root_children)} items={len(items)} -> {OUT}")
    for w in warnings:
        print("  WARN:", w)


if __name__ == "__main__":
    build()
