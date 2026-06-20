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
        "_generated": True,
        "_do_not_hand_edit": True,
        "_built_by": "scripts/build_people_grammar.py",
        "_source_of_truth": "research/people/*.md",
        "description": "The makers, patrons, occultists, scholars, and institutions behind the historical tarot decks in this collection. Each node links to the deck(s) that person or body made, reframed, printed, or holds — and, where specific, to the cards that feature them (e.g. Pamela Colman Smith's scenes in the RWS deck). Generated from the research/people dossiers, which carry the sourced evidence.",
        "tags": ["people", "history", "tarot", "biography", "institutions"],
        "is_published": True,
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
