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

# Cross-deck SYNTHESIS per trump (the evolution narrative), keyed by trump_key.
# Injected into the emergent num-major-N nodes as an "Across the decks" section.
# Same file is read by viewers/prototypes/lenses.html. Edit research/synthesis/trumps.json.
try:
    TRUMP_SYNTHESIS = json.load(open(os.path.join(HERE, "..", "research", "synthesis", "trumps.json"), encoding="utf-8"))
except Exception:
    TRUMP_SYNTHESIS = {}
NUM_TO_KEY = ["fool", "magician", "high-priestess", "empress", "emperor", "hierophant", "lovers",
              "chariot", "strength", "hermit", "wheel-of-fortune", "justice", "hanged-man", "death",
              "temperance", "devil", "tower", "star", "moon", "sun", "judgement", "world"]
R2 = "https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev"  # public base (kept if a deck already uses it)

# --- Decks to include + per-deck editorial/era (provenance is a deck property) ---
# Excluded on purpose: mantegna-tarocchi (NOT a tarot) and tree-of-tarot (a meta).
DECKS = {
 "visconti-sforza-tarot":      dict(label="Visconti-Sforza", era="15th c · Renaissance Italy", era_sort=1,
        ed=dict(date="c. 1451", maker="Bonifacio Bembo workshop (attrib.)", patron="House of Visconti–Sforza, Milan",
                context="Hand-painted ducal luxury deck, among the oldest surviving tarot", print="Hand-painted, gold leaf & tempera",
                orientation="Game (trionfi); no surviving record of divinatory use this early")),
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

# Historian classification (from research/*.mdx frontmatter): Dummett trump-ORDER branch +
# game/divination FUNCTION. Drives the By-Lineage (genealogy) + By-Function emergence axes.
# These are STRUCTURAL emergences (real historical properties), unlike the analytical lenses
# (archetype/suit/rank) that re-group the same cards for study.
CLASS = {
 "visconti-sforza-tarot":         dict(order="C", function="game"),
 "cary-yale-visconti-tarot":      dict(order="C", function="game"),
 "charles-vi-tarot":              dict(order="B", function="game"),
 "minchiate-florence-tarot":      dict(order="A", function="game"),
 "tarocchino-bologna":            dict(order="A", function="game"),
 "tarot-de-marseille-conver":     dict(order="C", function="game"),
 "tarot-de-besancon":             dict(order="C", function="game"),
 "court-de-gebelin-tarot":        dict(order="occult", function="origin-myth"),
 "etteilla-i-livre-de-thot":      dict(order="occult", function="divination"),
 "etteilla-ii-egyptian":          dict(order="occult", function="divination"),
 "etteilla-iii-oracle-des-dames": dict(order="occult", function="divination"),
 "oswald-wirth-tarot":            dict(order="occult", function="esoteric"),
 "golden-dawn-book-t-tarot":      dict(order="occult", function="esoteric"),
}
# Upstream ancestors / cousins — their OWN grammars (not tarot; no trumps), surfaced on the
# genealogy timeline via _decks (they do NOT enter the arcana/suit/rank card tree).
# ancestry: direct-ancestor | ancestral | cousin. timeline_year positions the lineage role
# (e.g. Mamluk's 1370s transmission) even when the surviving object is later.
ANCESTORS = [
 dict(slug="mamluk-deck", label="Mamluk (Mulūk wa-nuwwāb)", node_id="anc-mamluk-deck",
      era="Mamluk Egypt & Syria", date="c. 1500 (Topkapı deck)", timeline_year=1375,
      ancestry="direct-ancestor", count=8),
 dict(slug="cary-sheet", label="Cary Sheet (Milanese woodcut)", node_id="anc-cary-sheet",
      era="Milan", date="c. 1500", timeline_year=1500, ancestry="ancestral", count=4),
 dict(slug="rosenwald-sheet", label="Rosenwald Sheet (Florentine)", node_id="anc-rosenwald-sheet",
      era="Florence", date="c. 1500", timeline_year=1500, ancestry="ancestral", count=4),
 dict(slug="noblet-tarot", label="Jean Noblet (oldest TdM)", node_id="anc-noblet-tarot",
      era="Paris", date="c. 1650", timeline_year=1650, ancestry="ancestral", count=4),
 dict(slug="ganjifa", label="Ganjifa (Persian/Mughal cousin)", node_id="anc-ganjifa",
      era="Persia / Mughal India", date="16th c.+", timeline_year=1550, ancestry="cousin", count=4),
]

ORDER_SORT = {"A": 1, "B": 2, "C": 3, "occult": 4}
ORDER_LABEL = {"A": "The Southern Way — Florence & Bologna (A-order)", "B": "The Eastern Way — Ferrara (B-order)",
               "C": "The Western Way — Milan → Marseille (C-order)", "occult": "The Occult Turn — off the Western way, 1781→"}
FUNC_SORT = {"game": 1, "origin-myth": 2, "divination": 3, "esoteric": 4}
FUNC_LABEL = {"game": "Game (trick-taking)", "origin-myth": "Origin-myth (proto-occult)",
              "divination": "Divination (purpose-built)", "esoteric": "Esoteric / initiatory"}

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
            # Only aggregate real L1 cards. Skip emergence/axis nodes (anything with
            # composite_of, e.g. suit/keyword pills) so they don't leak in as bogus cards.
            if it.get("composite_of") or it.get("category") in ("axis", "keyword-emergence"):
                continue
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
            cl = CLASS.get(slug, {})
            cards.append(dict(
                cid="card-%s-%d" % (slug.replace("-",""), ord_),
                slug=slug, label=dk["label"], era=dk["era"], era_sort=dk["era_sort"], ed=dk["ed"],
                name=name, image_url=it.get("image_url"), src_item_id=it.get("id"),
                arcana=arcana, suit=suit, rank=rank, major=major,
                order=cl.get("order"), function=cl.get("function")))

    items = []
    def add(o): items.append(o)

    import re as _re
    def _year(s):   # MULTI_LENS_PLAN §2: numeric year for the timeline lens (queryable field)
        if not s: return None
        m = _re.search(r'\b(1[2-9]\d{2}|20\d{2})\b', str(s))
        if m: return int(m.group(1))
        m = _re.search(r'(\d{1,2})\s*(?:st|nd|rd|th)?\s*c', str(s), _re.I)
        if m: return (int(m.group(1)) - 1) * 100 + 50
        return None

    # L1 cards
    for c in cards:
        ed = c["ed"]
        add({"id": c["cid"], "name": "%s — %s" % (c["name"], c["label"]), "level": 1, "category": "card",
             "ref_preview": "study",
             "metadata": {k: v for k, v in {
                 "deck": c["label"], "arcana": c["arcana"], "suit": c["suit"],
                 "number": (c["major"] if c["major"] is not None else c["rank"]),
                 "order": c["order"], "function": c["function"],
                 "year": _year(ed["date"]) or _year(c["era"]),
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
    # By Age — one node per DISTINCT era label (id keyed on the full label, not
    # era_sort, so decks that share a sort bucket but differ in wording don't
    # collide into duplicate ids / duplicate pills). Ordered oldest-first by sort.
    eras = sorted({(c["era_sort"], c["era"]) for c in cards})
    def era_id(es, ename):
        slug = re.sub(r"[^a-z0-9]+", "-", ename.lower()).strip("-")
        return "era-%d-%s" % (es, slug)
    for es, ename in eras:
        add({"id": era_id(es, ename), "name": ename, "level": 2, "category": "era",
             "sections": {"What it is": "All cards from decks of this era: %s." % ename},
             "composite_of": ids(lambda c, es=es, ename=ename: c["era_sort"] == es and c["era"] == ename)})
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
            secs = {"What it is": "%s — Arcanum %d — across the decks." % (MAJ_NAMES[n], n)}
            syn = TRUMP_SYNTHESIS.get(NUM_TO_KEY[n]) if n < len(NUM_TO_KEY) else None
            if syn:
                secs["Across the decks"] = syn
            add({"id": mid, "name": "%d — %s" % (n, MAJ_NAMES[n]), "level": 3, "category": "archetype",
                 "sections": secs, "composite_of": members})
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
            _plural = RANK_NAMES[r] + ("es" if RANK_NAMES[r][-1] in "sxz" else "s")
            add({"id": xid, "name": _plural, "level": 3, "category": "rank-cross",
                 "sections": {"What it is": "Every %s across all four suits and every deck — cross-suit numerology." % RANK_NAMES[r]},
                 "composite_of": members})
            xr_nodes.append(xid)
    # Historiography essay — the divination question, stated and weighed honestly.
    add({"id": "essay-divination-question", "name": "The Divination Question — and why the Inquisition doesn't explain the silence",
         "level": 5, "category": "essay",
         "sections": {
            "The documented origin is a game": (
                "Tarot appears in 1440s northern Italy (Milan, Ferrara, Bologna) as a trick-taking GAME: 21 "
                "'triumph' cards plus the Fool added to an ordinary four-suit deck so trumps beat the suits. "
                "The earliest sources are account books, game treatises, tax/guild records and luxury commissions "
                "— and the game never died (tarock/tarocchi is still played in continental Europe). For roughly "
                "three centuries (c. 1440–1780) there is no surviving evidence that tarot was used for divination."),
            "The concealment hypothesis (stated fairly)": (
                "A fair objection: the archive records what was safe to write down. Divination, sortilegio and "
                "judicial astrology were spiritually suspect, and the Inquisition prosecuted superstition — so a "
                "fortune-teller in 1490 would call it 'just a game,' and any divinatory use of tarot might simply "
                "have left no trace. On this view the silence reflects fear, not absence."),
            "Why it does not hold up": (
                "Four problems. (1) TIMING is backwards: tarot appears c. 1440, but the heavy anti-superstition "
                "machinery ramps up later (Roman Inquisition 1542, Counter-Reformation) — leaving a century before "
                "the crackdown still with no divination evidence. (2) The cards were NOT hidden: they were openly "
                "bought, taxed, gifted and played; an underground practice riding the most visible deck in Europe is "
                "implausible. (3) Other fortune-telling DID get recorded in the same period — court astrology, and "
                "printed lot-books like Lorenzo Spirito's *Libro delle Sorti* (1482); tarot simply isn't part of that "
                "documented sortes tradition until the 1700s. (4) The dog that didn't bark: the 15th-c. friar's sermon "
                "(*Sermones de ludo cum aliis*) lists the 21 trumps by name and condemns the deck — as gambling and "
                "the devil's work, NOT as divination, the graver sin moralists were eager to catalog. And the 18th-c. "
                "emergence reads as invention, not inheritance: Court de Gébelin presents the Egyptian 'Book of Thoth' "
                "as a fresh discovery (and gets Egypt flatly wrong), while Etteilla builds a cartomancy system from scratch."),
            "Conclusion": (
                "So the honest claim is not 'only ever a game,' and not 'secretly always divinatory.' It is: tarot was "
                "DESIGNED AND FIRST USED AS A GAME; divinatory meaning is a later (18th-century) overlay. Informal "
                "cartomancy with cards can't be wholly ruled out and the record is biased — but the Inquisition does "
                "not explain the silence, and the simpler reading fits the positive evidence better."),
            "Sources": (
                "Michael Dummett, *The Game of Tarot* (1980); Ronald Decker, Thierry Depaulis & Michael Dummett, "
                "*A Wicked Pack of Cards* (1996); Decker & Dummett, *A History of the Occult Tarot* (2002); Stuart "
                "Kaplan, *The Encyclopedia of Tarot*; Andrea Vitali, *Le Tarot* essays (letarot.it); Lothar Teikemeier, "
                "trionfi.com. Primary: the *Sermones de ludo cum aliis* ('Steele sermon'); Court de Gébelin, *Le Monde "
                "Primitif* vol. VIII (1781, on Gallica/BnF); Lorenzo Spirito, *Libro delle Sorti* (1482).")
         }})

    # Roots
    arc_children = [x for x in ("arc-major", "arc-minor") if any(i["id"] == x for i in items)]
    add({"id": "root-arcana", "name": "The Tarot — by Arcana · Suit · Number", "level": 6, "category": "root",
         "sections": {"What it is": "The canonical tarot tree: Major Arcana by number, Minor Arcana → four suits → ranks Ace–King — every leaf gathered across all decks. See also the essay 'The Divination Question' for how this collection frames game-vs-divination."},
         "composite_of": ["essay-divination-question"] + arc_children})
    add({"id": "axis-deck", "name": "By Deck", "level": 4, "category": "axis",
         "render_as": "pill-group", "lens": "genealogy",   # MULTI_LENS_PLAN §3: this axis renders as the descent DAG
         "sections": {"What it is": "Browse every card grouped by its source deck."},
         "composite_of": ["deck-" + s.replace("-","") for s in DECKS if any(c["slug"] == s for c in cards)]})
    add({"id": "axis-age", "name": "By Age", "level": 4, "category": "axis",
         "render_as": "pill-group", "lens": "timeline",    # this axis renders as a year timeline
         "sections": {"What it is": "Decks grouped by era, oldest first."},
         "composite_of": [era_id(es, ename) for es, ename in eras]})
    if xr_nodes:
        add({"id": "axis-number", "name": "By Rank", "level": 4, "category": "axis",
             "render_as": "pill-group", "lens": "pills",
             "sections": {"What it is": "Cross-suit numerology — every Ace, every Two … every King, gathered across all four suits and every deck. This is the *transpose* of 'The Tarot' tree: where that goes suit→rank (all the Coins together), this goes rank→suit (all the Aces together)."},
             "composite_of": xr_nodes})

    # By Lineage — Dummett trump-order genealogy (STRUCTURAL: the real derivation branches).
    lin_nodes = []
    for o, _ in sorted(ORDER_SORT.items(), key=lambda kv: kv[1]):
        members = ids(lambda c, o=o: c["order"] == o)
        if members:
            lid = "lineage-" + o
            add({"id": lid, "name": ORDER_LABEL[o], "level": 3, "category": "lineage",
                 "sections": {"What it is": "Decks of the %s, gathered across every card." % ORDER_LABEL[o]},
                 "composite_of": members})
            lin_nodes.append(lid)
    if lin_nodes:
        add({"id": "axis-lineage", "name": "By Order (A · B · C)", "level": 4, "category": "axis",
             "sections": {"What it is": "Michael Dummett's three trump-orders — A (Florence/Bologna), B (Ferrara), C (Milan→Marseille) — plus the post-1781 occult turn that left the C-order line. The orders are the closest thing to a 'family tree' the early decks have: which city's sequence a deck follows is its lineage."},
             "composite_of": lin_nodes})

    # By Function — game / divination / esoteric (STRUCTURAL: documented historical use).
    fn_nodes = []
    for fn, _ in sorted(FUNC_SORT.items(), key=lambda kv: kv[1]):
        members = ids(lambda c, fn=fn: c["function"] == fn)
        if members:
            fid = "function-" + fn
            add({"id": fid, "name": FUNC_LABEL[fn], "level": 3, "category": "function",
                 "sections": {"What it is": "Cards from decks whose documented use was: %s." % FUNC_LABEL[fn]},
                 "composite_of": members})
            fn_nodes.append(fid)
    if fn_nodes:
        add({"id": "axis-function", "name": "By Function", "level": 4, "category": "axis",
             "sections": {"What it is": "Game vs divination vs esoteric — documented use, which only turns divinatory after 1781."},
             "composite_of": fn_nodes})

    # render_as: the orthogonal axes become faceted filter pills in the viewer
    # (the tree keeps the arcana->suit->rank spine). Mirrors the Library HashtagFilter.
    PILL_AXES = ("axis-deck", "axis-age", "axis-number", "axis-lineage", "axis-function")
    # MULTI_LENS_PLAN §3: each axis also declares its full-view renderer (`lens`).
    AXIS_LENS = {"axis-deck": "genealogy", "axis-age": "timeline", "axis-number": "pills",
                 "axis-lineage": "genealogy", "axis-function": "pills"}
    for it in items:
        if it["id"] in PILL_AXES:
            it["render_as"] = "pill-group"
            it["lens"] = AXIS_LENS[it["id"]]

    # emergence_kind: distinguish REAL structural emergences (deck, era, lineage, function —
    # things that historically happened) from analytical LENSES (archetype/suit/rank — ways
    # we re-group the same leaves). Lets a viewer show "the genealogy" vs "the study lenses".
    STRUCTURAL_CATS = {"deck", "era", "lineage", "function", "root", "axis"}
    LENS_CATS = {"rank", "suit", "archetype", "arcana", "rank-cross"}
    for it in items:
        cat = it.get("category")
        if cat in STRUCTURAL_CATS:
            it["emergence_kind"] = "structural"
        elif cat in LENS_CATS:
            it["emergence_kind"] = "lens"

    # Denormalized per-deck index — lets a self-contained viewer (GitHub Pages /
    # Cytoscape) render the genealogy-on-a-timeline from this one file, no globbing.
    deck_summary = []
    for slug, dk in DECKS.items():
        dcards = [c for c in cards if c["slug"] == slug]
        if not dcards:
            continue
        cl = CLASS.get(slug, {})
        deck_summary.append({
            "slug": slug, "label": dk["label"], "node_id": "deck-" + slug.replace("-", ""),
            "era": dk["era"], "era_sort": dk["era_sort"], "date": dk["ed"]["date"],
            "order": cl.get("order"), "function": cl.get("function"), "count": len(dcards),
            "ancestry": "tarot", "tier": cl.get("order"),  # tarot decks lane by trump-order
        })
    # Upstream ancestors / cousins (separate grammars) on the same timeline.
    for a in ANCESTORS:
        deck_summary.append({
            "slug": a["slug"], "label": a["label"], "node_id": a["node_id"],
            "era": a["era"], "era_sort": 0, "date": a["date"], "timeline_year": a["timeline_year"],
            "order": None, "function": "game", "count": a["count"],
            "ancestry": a["ancestry"], "tier": a["ancestry"],  # ancestors lane by ancestry status
        })

    grammar = {
        "_grammar_commons": {"schema_version": "1.0", "license": "CC-BY-SA-4.0",
            "attribution": [{"name": "PlayfulProcess", "note": "Generated meta-grammar; cards from the public-domain decks in this repo."}]},
        "name": "The Tarot — All Decks, Many Lenses (meta)",
        "description": (
            "A generated meta-grammar aggregating the public-domain tarot decks in recursive-tarot "
            "into one navigable tree: Major Arcana by number, Minor Arcana by suit & rank, plus By Deck, "
            "By Age, and cross-suit By Rank. Each card carries its source deck's editorial provenance "
            "(date, maker, patron, print, game-vs-divination). The whole collection is public domain.\n\n"
            "SOURCE OF TRUTH — read this first. Each card's authoritative detail lives in its own deck at "
            "`tarot/<slug>/grammar.json`. This meta is a *generated index* (a projection) over those decks, "
            "rebuilt idempotently by `scripts/build_meta_grammar.py` — it is NOT a second copy to maintain. "
            "To correct a card, edit its deck; the meta re-derives. The emergence axes below (By Deck, By Age, "
            "By Rank, By Order, By Function, The Tarot) are patterns *over* the decks' cards, not new data. "
            "Provenance is recorded once here, not tagged on each card. (See EMERGENCES.md.)\n\n"
            "ON ORIGINS — read before judging the framing. The documented origin of tarot (1440s northern "
            "Italy) is a trick-taking card GAME: the 'triumphs' (trionfi) were added to an ordinary four-suit "
            "deck so trumps could beat the suits. For roughly three centuries there is no surviving evidence of "
            "tarot used for divination; the cards were openly bought, taxed, gifted, and played across Europe "
            "(the game survives as tarock/tarocchi today). Divinatory tarot is first attested in the 1780s — "
            "Court de Gébelin's (evidence-free) 'ancient Egyptian Book of Thoth' claim, then Etteilla's "
            "purpose-built cartomancy — and was elaborated by 19th-century occultists into the system most "
            "people now assume was always there. So the honest claim is not 'only a game' but: DOCUMENTED AND "
            "FIRST USED AS A GAME; divinatory meaning is a later (18th-century) overlay, not the original "
            "purpose. One caveat is kept throughout: absence of evidence is shaped by what was safe to write "
            "down — informal cartomancy can't be wholly ruled out (see the node 'The Divination Question'). "
            "DEEPER ROOTS (a gaming, not divinatory, lineage): Tang-China money-suited cards → Mamluk Egypt's "
            "kanjifah / Mulūk wa-nuwwāb — the four-suit pack Europe copied when cards reached Iberia & Italy in "
            "the 1370s → Italian trionfi (1440s). Genuinely ancestral decks (Mamluk, the Cary Sheet, the "
            "Rosenwald Sheet, Noblet) are being added, with the cousin branches (Ganjifa) labelled as such, so "
            "the China → Islam → Europe story is visible. Full per-deck notes live in this repo's research/ "
            "library. Scholarship: Dummett, *The Game of Tarot* (1980); Decker, Depaulis & Dummett, *A Wicked "
            "Pack of Cards* (1996); Dummett & McLeod, *A History of Games Played with the Tarot Pack* (2004); "
            "Kaplan, *Encyclopedia of Tarot*; Andrea Vitali, *Le Tarot* (letarot.it); Teikemeier, trionfi.com."
        ),
        "grammar_type": "tarot", "creator_name": "PlayfulProcess", "default_view": "tree", "default_preview": "tree",
        "_generated": True, "_do_not_hand_edit": True, "_built_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "_built_by": "scripts/build_meta_grammar.py",
        "_decks": deck_summary,
        "items": items,
    }
    # Emergence thumbnails: every composite node (deck / era / lineage / rank / axis)
    # inherits a representative image from a descendant card, so nothing renders blank.
    by_id = {i["id"]: i for i in items}
    def first_img(nid, seen):
        if nid in seen: return None
        seen.add(nid)
        it = by_id.get(nid)
        if not it: return None
        img = it.get("image_url") or (it.get("metadata") or {}).get("image_url")
        if img: return img
        for cid in (it.get("composite_of") or []):
            r = first_img(cid, seen)
            if r: return r
        return None
    for it in items:
        if it.get("composite_of") and not (it.get("image_url") or (it.get("metadata") or {}).get("image_url")):
            img = first_img(it["id"], set())
            if img: it["image_url"] = img

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
