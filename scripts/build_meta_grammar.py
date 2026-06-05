# -*- coding: utf-8 -*-
"""Build the multi-axis meta-grammar "The Tarot — All Decks, Many Lenses" from the
deck grammar.json files already in this repo (tarot/<slug>/grammar.json).

This is DATA PREP that lives in the public recursive-tarot repo, not a recursive.eco
app feature — recursive.eco stays the simple renderer; the meta is a generated
artifact produced here and rendered there. Re-run after editing decks/editorial.

Output: tarot/all-decks-many-lenses/grammar.json (a self-contained grammar whose
items are the cards + emergence nodes; composite_of carries the tree). Idempotent.

Structure (graceful — a card joins every axis it has data for):
  root-arcana  ->  Major Arcana (0-21 archetypes)  ->  cards (that major, all decks)
                   Minor Arcana (4 suits) -> rank (Ace..King) -> cards
  axis-deck    ->  one node per deck   -> cards
  axis-age     ->  one node per era    -> cards
  axis-number  ->  cross-suit rank (every Ace, every King...) -> cards

Run from repo root:  python scripts/build_meta_grammar.py
"""
import json, os, re, glob, datetime

HERE = os.path.dirname(__file__)
TAROT = os.path.abspath(os.path.join(HERE, "..", "tarot"))
OUT_SLUG = "all-decks-many-lenses"
R2 = "https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev"  # public base (kept if a deck already uses it)

# --- Decks to include + per-deck editorial/era (provenance is a deck property) ---
# Excluded on purpose: mantegna-tarocchi (NOT a tarot) and tree-of-tarot (a meta).
DECKS = {
 "visconti-sforza-tarot":      dict(label="Visconti-Sforza", era="15th c · Renaissance Italy", era_sort=1,
        ed=dict(date="c. 1451", maker="Bonifacio Bembo workshop (attrib.)", patron="House of Visconti–Sforza, Milan",
                context="Hand-painted ducal luxury deck, among the oldest surviving tarot", print="Hand-painted, gold leaf & tempera",
                orientation="Game (trionfi) — pre-divinatory")),
 "cary-yale-visconti-tarot":   dict(label="Cary-Yale Visconti", era="15th c · Renaissance Italy", era_sort=1,
        ed=dict(date="c. 1442", maker="Bonifacio Bembo workshop (attrib.)", patron="House of Visconti, Milan",
                context="The lavish outlier — six-rank courts + theological virtues", print="Hand-painted, gold-ground tempera",
                orientation="Game (trionfi)")),
 "charles-vi-tarot":           dict(label="'Charles VI' (Ferrara)", era="15th c · Renaissance Italy", era_sort=1,
        ed=dict(date="c. 1475–1500", maker="Ferrarese workshop (the so-called 'Charles VI'/Gringonneur, misattributed)", patron="—",
                context="Hand-painted trump fragments long misdated to a 1392 Gringonneur payment", print="Hand-painted",
                orientation="Game")),
 "minchiate-florence-tarot":   dict(label="Minchiate (Florence)", era="16th–18th c · Florence", era_sort=2,
        ed=dict(date="16th–18th c", maker="Florentine cardmakers", patron="—",
                context="The 97-card Florentine expansion (40+ trumps: zodiac, elements, virtues)", print="Woodcut, stencil-coloured",
                orientation="Game")),
 "tarocchino-bologna":         dict(label="Tarocchino di Bologna", era="17th c · Bologna", era_sort=2,
        ed=dict(date="17th c", maker="Bolognese cardmakers", patron="—",
                context="The 62-card Bolognese trick-taking game (pips 2–5 stripped)", print="Woodcut",
                orientation="Game (Bolognese tradition)")),
 "tarot-de-marseille-conver":  dict(label="Tarot de Marseille (Conver)", era="1760 · Tarot de Marseille", era_sort=3,
        ed=dict(date="1760", maker="Nicolas Conver, master cardmaker, Marseille", patron="Commercial cardmaking trade",
                context="The canonical Marseille woodblock pattern; later the occult era's reference image", print="Woodcut with stencil colouring",
                orientation="Game (later adopted for divination)")),
 "tarot-de-besancon":          dict(label="Tarot de Besançon", era="18th–19th c · Besançon", era_sort=3,
        ed=dict(date="18th–19th c", maker="Eastern-French / Swiss cardmakers", patron="—",
                context="The Besançon variant — Juno & Jupiter replace the Papess & Pope", print="Woodcut",
                orientation="Game")),
 "court-de-gebelin-tarot":     dict(label="Court de Gébelin's Plates", era="1781 · The occult turn", era_sort=4,
        ed=dict(date="1781", maker="Antoine Court de Gébelin (Le Monde Primitif engravings)", patron="—",
                context="Where divination is invented — the 'ancient Egyptian Book of Thoth' myth", print="Engraving",
                orientation="Esoteric reframing (origin myth)")),
 "etteilla-i-livre-de-thot":   dict(label="Etteilla I — Livre de Thot", era="1788 · Etteilla cartomancy", era_sort=4,
        ed=dict(date="1788–1789", maker="Jean-Baptiste Alliette ('Etteilla')", patron="Parisian cartomancy public",
                context="Among the first decks purpose-built for fortune-telling", print="Engraving, hand-coloured",
                orientation="Divination (purpose-built)")),
 "etteilla-ii-egyptian":       dict(label="Etteilla II (Egyptian)", era="19th c · Etteilla cartomancy", era_sort=4,
        ed=dict(date="19th c", maker="Grand Etteilla II editors", patron="Commercial esoteric publishers",
                context="A later Grand Etteilla edition in the Egyptian style", print="Lithograph / engraving",
                orientation="Divination")),
 "etteilla-iii-oracle-des-dames": dict(label="Etteilla III — Oracle des Dames", era="19th c · Etteilla cartomancy", era_sort=4,
        ed=dict(date="19th c", maker="Grand Etteilla III 'Oracle des Dames'", patron="Commercial esoteric publishers",
                context="A later Grand Etteilla edition continuing Alliette's system", print="Lithograph",
                orientation="Divination")),
 "oswald-wirth-tarot":         dict(label="Oswald Wirth", era="1889 · Occult synthesis", era_sort=5,
        ed=dict(date="1889 / 1926", maker="Oswald Wirth (after Lévi & de Guaita)", patron="—",
                context="22 esoteric Major Arcana — the Lévi → Continental synthesis", print="Lithograph",
                orientation="Divination")),
 "golden-dawn-book-t-tarot":   dict(label="Golden Dawn (Book T)", era="1888 · English esoteric", era_sort=5,
        ed=dict(date="c. 1888", maker="Hermetic Order of the Golden Dawn (Mathers)", patron="—",
                context="The full correspondence system (astrology, Hebrew, decans); swaps Strength ↔ Justice", print="Manuscript / RWS-style imagery",
                orientation="Divination")),
}

MAJ_NAMES = ["The Fool","The Magician","The High Priestess","The Empress","The Emperor","The Hierophant",
 "The Lovers","The Chariot","Strength","The Hermit","Wheel of Fortune","Justice","The Hanged Man","Death",
 "Temperance","The Devil","The Tower","The Star","The Moon","The Sun","Judgement","The World"]
RANK_NAMES = {1:"Ace",2:"Two",3:"Three",4:"Four",5:"Five",6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten",11:"Page",12:"Knight",13:"Queen",14:"King"}

# name variants (lowercased, word-boundary matched) -> canonical archetype number (RWS).
# Strength=8 / Justice=11 by NAME so the A/B/C swap groups by archetype, not position.
NAME_TO_MAJOR = {
 0:["fool","le mat","matto","mato","le fou"], 1:["magician","magus","bateleur","bagatto","bagatella","il bagatto"],
 2:["high priestess","priestess","papess","popess","papesse","la papessa","junon","juno"],
 3:["empress","imperatrice","l'imperatrice","l'impératrice"], 4:["emperor","empereur","l'empereur","l'imperatore","jupiter"],
 5:["hierophant","pope","pape","il papa"], 6:["lovers","amoureux","l'amoureux","gli amanti","l'amore"],
 7:["chariot","le chariot","il carro","carro"], 8:["strength","force","la force","fortitude","la forza"],
 9:["hermit","hermite","l'hermite","l'ermite","eremita","l'eremita","il tempo"], 10:["wheel of fortune","roue de fortune","la roue","ruota","fortune"],
 11:["justice","la justice","la giustizia"], 12:["hanged man","pendu","le pendu","l'appeso","l'impiccato"],
 13:["death","la mort","la morte","morte"], 14:["temperance","tempérance","la temperanza","la tempérance"],
 15:["devil","diable","le diable","il diavolo"], 16:["tower","tour","la maison dieu","maison de dieu","la maison de dieu","torre"],
 17:["star","etoile","l'etoile","l'étoile","la stella","stella"], 18:["moon","lune","la lune","la luna"],
 19:["sun","soleil","le soleil","il sole"], 20:["judgement","judgment","jugement","le jugement","il giudizio","angel"],
 21:["world","monde","le monde","il mondo","universe"],
}
_NAME_PATTERNS = []
for num, variants in NAME_TO_MAJOR.items():
    for v in sorted(variants, key=len, reverse=True):
        _NAME_PATTERNS.append((re.compile(r"\b" + re.escape(v) + r"\b", re.IGNORECASE | re.UNICODE), num))

def major_from_name(name):
    n = (name or "").lower()
    for pat, num in _NAME_PATTERNS:
        if pat.search(n):
            return num
    return None

def suit_norm(raw):
    s = (raw or "").lower()
    if re.search(r"wand|baton|bastoni", s): return "Wands"
    if re.search(r"cup|coupe|coppe", s):    return "Cups"
    if re.search(r"sword|epee|épée|spade", s): return "Swords"
    if re.search(r"coin|pentacl|denier|denari", s): return "Coins"
    return None

def rank_from_name(name):
    n = (name or "").lower()
    pips = [("ace",1),("two",2),("three",3),("four",4),("five",5),("six",6),("seven",7),("eight",8),("nine",9),("ten",10)]
    for w,r in pips:
        if re.search(r"\b"+w+r"\b", n): return r
    if re.search(r"page|knave|valet|fante|maid|servante", n): return 11
    if re.search(r"knight|chevalier|cavall", n): return 12
    if re.search(r"queen|reine|regina|dama", n): return 13
    if re.search(r"king|\broi\b|\bre\b", n): return 14
    m = re.match(r"^\s*(\d+)\s+of\s", n)
    if m: return int(m.group(1))
    return None

# ---------------------------------------------------------------------------
def build():
    cards = []   # normalized card dicts
    for slug, dk in DECKS.items():
        path = os.path.join(TAROT, slug, "grammar.json")
        if not os.path.exists(path):
            print("  ! missing", slug); continue
        g = json.load(open(path, encoding="utf-8"))
        for ord_, it in enumerate(g.get("items", []), 1):
            m = it.get("metadata", {}) or {}
            name = it.get("name") or ""
            suit = suit_norm(m.get("suit"))
            mnum = m.get("number")
            mnum = int(mnum) if str(mnum).strip().isdigit() else None
            arcana = m.get("arcana")
            major = None; rank = None
            if suit:                                  # has a suit => minor
                arcana = "minor"; rank = rank_from_name(name)
            else:
                major = major_from_name(name)
                if major is None and arcana == "major" and mnum is not None and 0 <= mnum <= 21:
                    major = mnum
                if major is not None:
                    arcana = "major"
            cards.append(dict(
                cid="card-%s-%d" % (slug.replace("-",""), ord_),
                slug=slug, label=dk["label"], era=dk["era"], era_sort=dk["era_sort"], ed=dk["ed"],
                name=name, image_url=it.get("image_url"), src_item_id=it.get("id"),
                arcana=arcana, suit=suit, rank=rank, major=major))

    items = []
    def add(o): items.append(o)

    # L1 cards
    for c in cards:
        ed = c["ed"]
        add({"id": c["cid"], "name": "%s — %s" % (c["name"], c["label"]), "level": 1, "category": "card",
             "ref_preview": "study",
             "metadata": {k: v for k, v in {
                 "deck": c["label"], "arcana": c["arcana"], "suit": c["suit"],
                 "number": (c["major"] if c["major"] is not None else c["rank"]),
                 "source_deck": c["slug"], "source_item_id": c["src_item_id"],
                 "editorial": {"date": ed["date"], "maker": ed["maker"],
                               "patron": (None if ed["patron"] == "—" else ed["patron"]),
                               "context": ed["context"], "print": ed["print"], "orientation": ed["orientation"]},
             }.items() if v is not None},
             "sections": {
                 "Origin": "%s · %s · %s. %s. Print: %s. Made for: %s." % (
                     c["label"], ed["date"], ed["maker"], ed["context"], ed["print"], ed["orientation"]),
                 "Find the meaning": "From %s. Open the source deck for this card's full interpretation." % c["label"],
             },
             "image_url": c["image_url"], "sort_order": 0})

    SUIT_ORD = {"Wands": 1, "Cups": 2, "Swords": 3, "Coins": 4}
    def ids(pred): return sorted(c["cid"] for c in cards if pred(c))

    # By Deck
    for slug, dk in DECKS.items():
        members = [c["cid"] for c in cards if c["slug"] == slug]
        if members:
            add({"id": "deck-" + slug.replace("-",""), "name": dk["label"], "level": 2, "category": "deck",
                 "sections": {"What it is": "%s — %s. Every card in this deck." % (dk["label"], dk["ed"]["date"])},
                 "composite_of": members})
    # By Age
    eras = sorted({(c["era_sort"], c["era"]) for c in cards})
    for es, ename in eras:
        add({"id": "era-%d" % es, "name": ename, "level": 2, "category": "era",
             "sections": {"What it is": "All cards from decks of this era: %s." % ename},
             "composite_of": ids(lambda c, es=es: c["era_sort"] == es)})
    # Within-suit ranks + suits + Minor
    suit_nodes = []
    for suit, so in sorted(SUIT_ORD.items(), key=lambda kv: kv[1]):
        rank_nodes = []
        for r in range(1, 15):
            members = ids(lambda c, suit=suit, r=r: c["suit"] == suit and c["rank"] == r)
            if members:
                rid = "wsr-%s-%d" % (suit.lower(), r)
                add({"id": rid, "name": "%s of %s (all decks)" % (RANK_NAMES[r], suit), "level": 3, "category": "rank",
                     "sections": {"What it is": "The %s of %s across every deck." % (RANK_NAMES[r], suit)},
                     "composite_of": members})
                rank_nodes.append(rid)
        if rank_nodes:
            sid = "suit-" + suit.lower()
            add({"id": sid, "name": suit, "level": 4, "category": "suit",
                 "sections": {"What it is": "The suit of %s (names normalized across traditions) — Ace through King across every deck." % suit},
                 "composite_of": rank_nodes})
            suit_nodes.append(sid)
    # Major archetypes + Major Arcana
    maj_nodes = []
    for n in range(22):
        members = ids(lambda c, n=n: c["major"] == n)
        if members:
            mid = "num-major-%d" % n
            add({"id": mid, "name": "%d — %s" % (n, MAJ_NAMES[n]), "level": 3, "category": "archetype",
                 "sections": {"What it is": "%s — Arcanum %d — across the decks." % (MAJ_NAMES[n], n)},
                 "composite_of": members})
            maj_nodes.append(mid)
    if maj_nodes:
        add({"id": "arc-major", "name": "Major Arcana", "level": 4, "category": "arcana",
             "sections": {"What it is": "The trumps, each composed of that archetype across every deck."},
             "composite_of": maj_nodes})
    if suit_nodes:
        add({"id": "arc-minor", "name": "Minor Arcana", "level": 5, "category": "arcana",
             "sections": {"What it is": "The four suits, each composed of its ranks Ace–King across every deck."},
             "composite_of": suit_nodes})
    # Cross-suit numerology
    xr_nodes = []
    for r in range(1, 15):
        members = ids(lambda c, r=r: c["rank"] == r and c["suit"])
        if members:
            xid = "num-rank-%d" % r
            add({"id": xid, "name": "%ss (every suit, all decks)" % RANK_NAMES[r], "level": 3, "category": "rank-cross",
                 "sections": {"What it is": "Every %s across all four suits and every deck — cross-suit numerology." % RANK_NAMES[r]},
                 "composite_of": members})
            xr_nodes.append(xid)
    # Roots
    arc_children = [x for x in ("arc-major", "arc-minor") if any(i["id"] == x for i in items)]
    add({"id": "root-arcana", "name": "The Tarot — by Arcana · Suit · Number", "level": 6, "category": "root",
         "sections": {"What it is": "The canonical tarot tree: Major Arcana by number, Minor Arcana → four suits → ranks Ace–King — every leaf gathered across all decks."},
         "composite_of": arc_children})
    add({"id": "axis-deck", "name": "By Deck", "level": 4, "category": "axis",
         "sections": {"What it is": "Browse every card grouped by its source deck."},
         "composite_of": ["deck-" + s.replace("-","") for s in DECKS if any(c["slug"] == s for c in cards)]})
    add({"id": "axis-age", "name": "By Age", "level": 4, "category": "axis",
         "sections": {"What it is": "Decks grouped by era, oldest first."},
         "composite_of": ["era-%d" % es for es, _ in eras]})
    if xr_nodes:
        add({"id": "axis-number", "name": "By Rank — across all suits", "level": 4, "category": "axis",
             "sections": {"What it is": "Cross-suit numerology: every Ace, every Two … every King, across all suits and decks."},
             "composite_of": xr_nodes})

    # render_as: the orthogonal axes become faceted filter pills in the viewer
    # (the tree keeps the arcana->suit->rank spine). Mirrors the Library HashtagFilter.
    for it in items:
        if it["id"] in ("axis-deck", "axis-age", "axis-number"):
            it["render_as"] = "pill-group"

    grammar = {
        "_grammar_commons": {"schema_version": "1.0", "license": "CC-BY-SA-4.0",
            "attribution": [{"name": "PlayfulProcess", "note": "Generated meta-grammar; cards from the public-domain decks in this repo."}]},
        "name": "The Tarot — All Decks, Many Lenses (meta)",
        "description": "A generated meta-grammar aggregating the public-domain tarot decks in recursive-tarot into one navigable tree: Major Arcana by number, Minor Arcana by suit & rank, plus By Deck, By Age, and cross-suit By Rank. Each card carries its source deck's editorial provenance (date, maker, patron, print, game-vs-divination). The whole collection is public domain — provenance lives here once, not tagged on each card.",
        "grammar_type": "tarot", "creator_name": "PlayfulProcess", "default_view": "tree", "default_preview": "tree",
        "_generated": True, "_do_not_hand_edit": True, "_built_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "_built_by": "scripts/build_meta_grammar.py",
        "items": items,
    }
    out_dir = os.path.join(TAROT, OUT_SLUG)
    os.makedirs(out_dir, exist_ok=True)
    json.dump(grammar, open(os.path.join(out_dir, "grammar.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # summary
    ncards = sum(1 for i in items if i["category"] == "card")
    nmajor = sum(1 for c in cards if c["major"] is not None)
    nminor = sum(1 for c in cards if c["suit"])
    nuncl = sum(1 for c in cards if c["major"] is None and not c["suit"])
    idset = {i["id"] for i in items}
    dangling = [r for i in items for r in i.get("composite_of", []) if r not in idset]
    print("decks=%d cards=%d (major=%d minor=%d unclassified=%d) items=%d dangling=%d" % (
        len(DECKS), ncards, nmajor, nminor, nuncl, len(items), len(dangling)))
    print("wrote", os.path.join(out_dir, "grammar.json"))

if __name__ == "__main__":
    build()
