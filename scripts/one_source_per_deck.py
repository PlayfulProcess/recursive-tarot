# -*- coding: utf-8 -*-
"""One source per deck — split the borrowed voices out of the three occult decks.

Until now three decks each carried several *other* authors' complete card texts:

  golden-dawn-book-t-tarot   Book T  + Waite (78 cards) + Papus (22 majors)
  oswald-wirth-tarot         Wirth   + Papus (22 majors)
  court-de-gebelin-tarot     Gébelin + Papus (22 majors)

That made "which source am I reading?" unanswerable on the card. The rule now is
**one source per deck** (documented in GRAMMAR_FORMAT.md). This script performs the
split, once, and proves nothing was lost:

  * golden-dawn-book-t-tarot  -> Book T only (the editorial `Scene`/`Symbol` stay).
  * rider-waite-smith-pictorial-key (NEW) -> the RWS imagery + Waite's own 1911 text.
  * papus-tarot-des-bohemiens (NEW)      -> Wirth's 22 plates + Papus's 1889 text.
  * oswald-wirth-tarot / court-de-gebelin-tarot -> their own source only.

It also drops the per-card person cross-link pill (`metadata.source_deck ->
people-of-tarot`) wherever it repeats on every card of a deck: artist credit belongs
at DECK level (`image_credit`, `_grammar_commons.attribution`, the description), not
as a collapsed biography box stamped onto all 78 cards. The people-of-tarot items and
their own featured-card links are untouched — person -> card still works.

VERIFICATION (hard-fails): every character removed from a `Waite`/`Papus` section must
be findable afterwards either in one of the new decks or in `research/sources/*.md`.

Idempotent: re-running finds nothing to move and re-emits identical new decks.

  python scripts/one_source_per_deck.py            # apply
  python scripts/one_source_per_deck.py --check    # verify only, write nothing
"""
import json, os, re, sys, glob, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TAROT = os.path.join(ROOT, "tarot")
SOURCES = os.path.join(ROOT, "research", "sources")
R2 = "https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations"

GD = "golden-dawn-book-t-tarot"
WIRTH = "oswald-wirth-tarot"
GEBELIN = "court-de-gebelin-tarot"
RWS_NEW = "rider-waite-smith-pictorial-key"
PAPUS_NEW = "papus-tarot-des-bohemiens"

# The section a deck may NOT keep -> it is not that deck's own source.
STRIP = {GD: ("Waite", "Papus"), WIRTH: ("Papus",), GEBELIN: ("Papus",)}

CHECK = "--check" in sys.argv
report = []


def log(s):
    report.append(s)
    print(s)


def gpath(slug):
    return os.path.join(TAROT, slug, "grammar.json")


def load(slug):
    return json.load(open(gpath(slug), encoding="utf-8"))


def save(slug, g):
    if CHECK:
        return
    os.makedirs(os.path.dirname(gpath(slug)), exist_ok=True)
    with open(gpath(slug), "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
        f.write("\n")


def norm(t):
    """Whitespace/punctuation-insensitive form, for 'is this text still somewhere?'."""
    t = unicodedata.normalize("NFKC", t or "")
    t = re.sub(r"[‘’]", "'", t)
    t = re.sub(r"[“”]", '"', t)
    t = re.sub(r"[‐-―−]", "-", t)
    return re.sub(r"\s+", " ", t).strip()


ATTRIB_RE = re.compile(r"\A\s*\*[^\n]*\*\s*\n+")


def body(section):
    """The source text without the italic 'this is a foreign voice' attribution line.

    That header exists to warn the reader the text was written for a *different* deck.
    In the new decks the author IS the deck's source, so the header is dropped and the
    provenance lives at deck level instead."""
    return ATTRIB_RE.sub("", section or "").strip()


# --------------------------------------------------------------------------- collect
gd = load(GD)
wirth = load(WIRTH)
gebelin = load(GEBELIN)

waite = {}   # gd item id -> (item, waite body)
for it in gd["items"]:
    s = it.get("sections") or {}
    if "Waite" in s:
        waite[it["id"]] = (it, body(s["Waite"]))

papus_by_deck = {}
for slug, g in ((GD, gd), (WIRTH, wirth), (GEBELIN, gebelin)):
    d = {}
    for it in g["items"]:
        s = it.get("sections") or {}
        if "Papus" in s:
            d[it["id"]] = body(s["Papus"])
    papus_by_deck[slug] = d

log("collected: Waite on %d %s cards; Papus on %s"
    % (len(waite), GD, ", ".join("%d %s" % (len(v), k) for k, v in papus_by_deck.items())))

# The three Papus copies are the same corpus keyed by each deck's own numbering. Match
# them by trump NUMBER, not by id: Book T swaps VIII/XI (Strength <-> Justice), so the
# golden-dawn card 8 legitimately holds the text Wirth's card 11 holds.
NUM_RE = re.compile(r"(\d\d)")


def by_number(d):
    out = {}
    for iid, txt in d.items():
        m = NUM_RE.search(iid)
        if not m:
            raise SystemExit("cannot read a trump number out of item id %r" % iid)
        out[int(m.group(1))] = (iid, txt)
    return out


papus_nums = {slug: by_number(d) for slug, d in papus_by_deck.items()}

# Wirth carries the numbering the plates and Papus's book share (8 = Justice, 11 = Force),
# so Wirth's copy is the canonical one for the new deck. Assert the other two agree.
canon = papus_nums[WIRTH]
mismatch = []
for slug in (GD, GEBELIN):
    for n, (iid, txt) in papus_nums[slug].items():
        # Book T's swap: its card 8/11 carries the text of the OTHER number.
        want = n
        if slug == GD and n in (8, 11):
            want = 11 if n == 8 else 8
        if norm(txt) != norm(canon[want][1]):
            mismatch.append((slug, iid, n, want))
if mismatch:
    log("Papus copies DIVERGE (kept separately, not merged): %r" % (mismatch,))
else:
    log("Papus: all 3 copies byte-identical per card (modulo Book T's VIII<->XI swap) "
        "-> Wirth's copy is the single source")


# ------------------------------------------------------------------- new deck: RWS
def clean_meta(m, drop_print=True):
    """Card metadata for a new deck: keep the descriptive facts, drop the host deck's
    per-card person pill and its print/TGC paths (those point at the other deck's
    pre-baked files)."""
    m = dict(m or {})
    for k in ("source_deck", "source_item_id", "deck"):
        m.pop(k, None)
    if drop_print:
        m.pop("print", None)
    return m


rws_items = []
for it, txt in [(v[0], v[1]) for v in waite.values()]:
    m = clean_meta(it.get("metadata"))
    # Book T's correspondences are Book T's, not Waite's — they stay in that deck.
    for k in ("golden_dawn_title", "hebrew_letter", "hebrew_translit", "tree_path",
              "attribution", "decan", "sephirah", "world"):
        m.pop(k, None)
    rws_items.append({
        "id": it["id"],
        "name": it["name"],
        "sort_order": it["sort_order"],
        "category": it["category"],
        "level": it.get("level", 1),
        "keywords": [k for k in (it.get("keywords") or []) if k != "golden dawn"],
        "image_url": it["image_url"],
        "metadata": m,
        "sections": {"The Pictorial Key": txt},
    })
rws_items.sort(key=lambda i: i["sort_order"])

rws = {
    "_github_url": "https://github.com/PlayfulProcess/recursive-tarot/blob/main/tarot/%s/grammar.json" % RWS_NEW,
    "_github_source_url": "https://raw.githubusercontent.com/PlayfulProcess/recursive-tarot/main/tarot/%s/grammar.json" % RWS_NEW,
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Pamela Colman Smith", "date": "1878-1951",
             "note": "Artist of all 78 cards, majors and minors. Credited by Waite in his text; "
                     "not in the deck's market name, which went out as 'Rider-Waite'."},
            {"name": "Arthur Edward Waite", "date": "1857-1942",
             "note": "Devised the programme and wrote 'The Pictorial Key to the Tarot' (1911), "
                     "the text carried on every card here"},
            {"name": "William Rider & Son, London", "date": "1909 / 1911",
             "note": "Publisher of the deck (1909) and of the Pictorial Key (1911)"},
            {"name": "Wikimedia Commons", "date": "public domain",
             "note": "Card scans (US public domain; the 1909 deck's copyright lapsed)"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture; transcription of Waite's per-card text"},
        ],
    },
    "name": "Rider-Waite-Smith — The Pictorial Key (1911)",
    "description": """# Rider-Waite-Smith — The Pictorial Key

## At a glance

The deck almost everyone means by "tarot" — 78 cards drawn by **Pamela Colman Smith**,
published by **William Rider & Son** in **1909** to a programme set by **A. E. Waite** —
paired here with the source that explains it in Waite's own words: *The Pictorial Key to
the Tarot* (**1911**).

**One source, one deck.** Every card below carries Waite's text and only Waite's text.
The Golden Dawn's Book T correspondences for the same imagery live in their own deck
(`golden-dawn-book-t-tarot`), and Papus's rival French system lives in
`papus-tarot-des-bohemiens`. Three readings of a related tradition, three decks — so you
always know whose voice you are reading.

## Why it mattered

Smith illustrated the **minor arcana as scenes** rather than as counted suit signs. Before
1909 a Five of Wands in the Marseille pattern was five batons; hers is a scuffle between
five youths. That decision is a large part of why modern tarot can be read pictorially at
all.

## Credit

Art by **Pamela Colman Smith** (1909), credited by Waite in his text though not in the
deck's market name, which went out as *Rider-Waite*. She was engaged on a flat
illustrator's fee — standard publishing practice then and largely still. The deck is
called **Rider-Waite-Smith** here; her record is in `people-of-tarot`. The credit is
stated once, at deck level, rather than as a biography box on all 78 cards.

## What Waite's text is, and is not

The Pictorial Key gives, per card, a description of the imagery and a list of divinatory
meanings (upright and reversed) that Waite compiled from earlier cartomantic sources. He
is often dismissive of the fortune-telling material he is reporting, and he deliberately
withholds parts of the Golden Dawn system he had sworn not to publish — so read it as a
**partial, and at points evasive, gloss by the deck's own author**, not as a neutral key.
Where his description and Smith's drawing disagree, the drawing is the deck.

## Provenance & evidence

The 1909 deck and the 1911 book both survive in quantity and are public domain in the
United States. The imagery here is the standard Wikimedia Commons scan set — the same
files the Book T deck uses, deliberately re-used rather than re-uploaded, since it is
literally the same imagery being read by a different source.

## Sources & further reading

- A. E. Waite, *The Pictorial Key to the Tarot* (London: Rider, 1911) — public domain.
- Stuart Kaplan et al., *Pamela Colman Smith: The Untold Story* (2018).
- `books-of-tarot` and `people-of-tarot` in this repo for the record layer.
""",
    "grammar_type": "tarot",
    "provenance": "record",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://www.playfulprocess.com/",
    "cover_image_url": "%s/%s/RWS_Tarot_02_High_Priestess.jpg" % (R2, GD),
    "tags": ["tarot", "rider-waite-smith", "pamela-colman-smith", "a-e-waite",
             "pictorial-key", "1909", "1911", "public-domain", "seventy-eight-cards"],
    "roots": ["western-esoteric", "mysticism"],
    "shelves": ["wonder", "mirror"],
    "worldview": "esoteric",
    "is_published": True,
    "_community_folder": "tarot",
    "_community_slug": RWS_NEW,
    "_original_creator": "f18e2415-315c-43b7-ae93-d09c8892e181",
    "image_credit": "Art by Pamela Colman Smith (Rider-Waite-Smith, 1909), credited by Waite in "
                    "his text though not in the deck's market name; public-domain scans via "
                    "Wikimedia Commons",
    "metadata": {"common_name": "Rider-Waite-Smith", "category": "historical",
                 "year": 1911, "year_label": "deck 1909 · key 1911"},
    "_source": {
        "single_source": "A. E. Waite, The Pictorial Key to the Tarot (1911)",
        "section": "The Pictorial Key",
        "rule": "one source per deck — see GRAMMAR_FORMAT.md",
        "moved_from": GD,
    },
    "items": rws_items,
}

# ------------------------------------------------------------------ new deck: Papus
papus_items = []
for it in wirth["items"]:
    if it.get("category") != "major-arcana":
        continue
    n = int(NUM_RE.search(it["id"]).group(1))
    m = clean_meta(it.get("metadata"))
    papus_items.append({
        "id": it["id"],
        "name": it["name"],
        "sort_order": it["sort_order"],
        "category": "major-arcana",
        "level": it.get("level", 1),
        "keywords": [k for k in (it.get("keywords") or []) if k != "oswald wirth"],
        "image_url": it["image_url"],
        "metadata": m,
        "sections": {"Le Tarot des Bohémiens": canon[n][1]},
    })
papus_items.sort(key=lambda i: i["sort_order"])

papus = {
    "_github_url": "https://github.com/PlayfulProcess/recursive-tarot/blob/main/tarot/%s/grammar.json" % PAPUS_NEW,
    "_github_source_url": "https://raw.githubusercontent.com/PlayfulProcess/recursive-tarot/main/tarot/%s/grammar.json" % PAPUS_NEW,
    "_grammar_commons": {
        "schema_version": "1.0",
        "license": "CC-BY-SA-4.0",
        "attribution": [
            {"name": "Papus (Gérard Encausse)", "date": "1889",
             "note": "Author of 'Le Tarot des Bohémiens'; the text carried on every card here "
                     "(A. P. Morton's English translation, public domain)"},
            {"name": "Oswald Wirth", "date": "1889",
             "note": "Designer of the 22 arcana reproduced here — the plates drawn in the "
                     "de Guaita circle that Papus's book uses to illustrate its majors"},
            {"name": "Stanislas de Guaita", "date": "1889",
             "note": "Commissioned Wirth's designs; the shared milieu of both men"},
            {"name": "Wikimedia Commons / Bibliothèque nationale de France", "date": "public domain",
             "note": "Card images, Category:Oswald Wirth tarot deck (1889 BnF edition)"},
            {"name": "PlayfulProcess", "date": "2026",
             "note": "Grammar architecture; OCR repair of the per-card text"},
        ],
    },
    "name": "Papus — Le Tarot des Bohémiens (1889)",
    "description": """# Papus — Le Tarot des Bohémiens

## At a glance

**Papus** (the pen name of the physician **Gérard Encausse**, 1865–1916) published *Le
Tarot des Bohémiens* in **1889** and subtitled it "the absolute key to occult science" —
the most systematic statement of the French occult tarot, and the book that carried
Éliphas Lévi's tarot-Kabbalah equation to a wide readership.

**One source, one deck.** Every card here carries Papus's chapter for that arcanum, and
nothing else. His text used to be pasted as a third voice into the Golden Dawn, Wirth and
Court de Gébelin decks; it now stands on its own, where you can tell it is his.

## The imagery

The plates are **Oswald Wirth's 22 arcana** — the designs Wirth drew in 1889 under
Stanislas de Guaita, which Papus's own book reproduces to illustrate its majors. The two
men belonged to the same Parisian occult circle and the book and the deck are of a piece,
so the pairing here is the historical one rather than a modern mash-up. The same scans
serve the `oswald-wirth-tarot` deck, which reads them through Wirth's *own* commentary
instead — Wirth's plates, two different books about them.

## Numbering — note the divergence

Papus and Wirth keep the **Marseille order**: **VIII is Justice, XI is Strength**, and the
Fool is unnumbered and placed near the end. The Golden Dawn (and therefore the
Rider-Waite-Smith deck) swapped VIII and XI to fit Leo to Strength. Do **not** reconcile
the two systems: this deck follows Papus, and the Hebrew-letter assignments here differ
from Book T's accordingly.

## Majors only

Papus's book gives a chapter to each of the 22 majors. Its minor-arcana material is
**structural** — a general theory of the four suits and their ten numbers as a
self-reproducing Tetragrammaton, argued suit-wide rather than card by card — so there is
no per-card Papus text for the 56 minors to carry, and none is invented here.

## Counter-voices

Papus writes as if he is recovering an ancient Egyptian science preserved by "Bohemians"
(Roma). He is not: the Egyptian origin story was **invented in 1781** by Court de Gébelin,
and the attribution of tarot to Roma transmission has no evidentiary basis and repeats a
period stereotype about the people it names. Read the book as a **primary source for what
the French occult revival believed**, which is genuinely important, rather than as history
of the cards.

## Sources & further reading

- Papus, *Le Tarot des Bohémiens* (Paris, 1889); English tr. A. P. Morton — public domain.
- Michael Dummett & Ronald Decker, *A History of the Occult Tarot* — for the corrective.
- `oswald-wirth-tarot` and `court-de-gebelin-tarot` in this repo for the neighbouring voices.
""",
    "grammar_type": "tarot",
    "provenance": "record",
    "creator_name": "PlayfulProcess",
    "creator_link": "https://www.playfulprocess.com/",
    "cover_image_url": "%s/%s/01%%20Le%%20Bateleur%%2C%%20Oswald%%20Wirth%%20Tarot%%20Deck%%201889%%20BnF.jpg" % (R2, WIRTH),
    "tags": ["tarot", "papus", "gerard-encausse", "le-tarot-des-bohemiens", "oswald-wirth",
             "kabbalah", "major-arcana", "occult", "public-domain", "1889"],
    "roots": ["western-esoteric", "mysticism"],
    "shelves": ["wonder", "mirror"],
    "worldview": "esoteric",
    "is_published": True,
    "_community_folder": "tarot",
    "_community_slug": PAPUS_NEW,
    "_original_creator": "f18e2415-315c-43b7-ae93-d09c8892e181",
    "image_credit": "After Oswald Wirth, Les 22 Arcanes du Tarot Kabbalistique (1889, BnF edition); "
                    "public domain via Wikimedia Commons",
    "metadata": {"common_name": "Papus", "category": "historical",
                 "year": 1889, "year_label": "1889"},
    "_source": {
        "single_source": "Papus (Gérard Encausse), Le Tarot des Bohémiens (1889)",
        "section": "Le Tarot des Bohémiens",
        "rule": "one source per deck — see GRAMMAR_FORMAT.md",
        "moved_from": [GD, WIRTH, GEBELIN],
    },
    "items": papus_items,
}

log("built %s: %d cards; %s: %d cards" % (RWS_NEW, len(rws_items), PAPUS_NEW, len(papus_items)))

# -------------------------------------------------------------------------- strip
removed = []   # (deck, item id, section, text)
for slug, g in ((GD, gd), (WIRTH, wirth), (GEBELIN, gebelin)):
    n = 0
    for it in g["items"]:
        s = it.get("sections") or {}
        for key in STRIP[slug]:
            if key in s:
                removed.append((slug, it["id"], key, s.pop(key)))
                n += 1
    log("  %-26s removed %d section(s): %s" % (slug, n, ", ".join(STRIP[slug])))

# --------------------------------------------- drop the repeated per-card person pill
PILL = ("source_deck", "source_item_id", "deck")


MIN_REPEATS = 5   # below this it is a credit, not a repetition


def strip_person_pill(g, slug):
    """Remove the people-of-tarot cross-link when it is stamped on EVERY item of a deck.

    Artist/maker credit belongs at deck level. ONE dedicated item carrying the pill (an
    overview card, a single 'about the maker' entry) is exactly right and is left alone;
    the same collapsed biography box rendered on all 78 cards is not."""
    items = g.get("items", [])
    hits = [it for it in items
            if (it.get("metadata") or {}).get("source_deck") == "people-of-tarot"]
    if len(hits) < MIN_REPEATS or len(hits) < len(items):
        return 0, None
    person = (hits[0].get("metadata") or {}).get("source_item_id")
    for it in hits:
        for k in PILL:
            it["metadata"].pop(k, None)
    return len(hits), person


def deck_level_credit(g):
    """Does the deck still name its maker outside the stripped pills?"""
    where = []
    if (g.get("image_credit") or "").strip():
        where.append("image_credit")
    if ((g.get("_grammar_commons") or {}).get("attribution")):
        where.append("_grammar_commons.attribution")
    if (g.get("metadata") or {}).get("common_name"):
        where.append("metadata.common_name")
    return where


pill_report = []
loaded = {GD: gd, WIRTH: wirth, GEBELIN: gebelin}
for path in sorted(glob.glob(os.path.join(TAROT, "*", "grammar.json"))):
    slug = os.path.basename(os.path.dirname(path))
    g = loaded.get(slug) or json.load(open(path, encoding="utf-8"))
    if g.get("_generated"):
        continue
    n, person = strip_person_pill(g, slug)
    if n:
        pill_report.append((slug, n, person, deck_level_credit(g)))
        if slug not in loaded:
            loaded[slug] = g

if pill_report:
    log("per-card person pill removed (deck-level credit stands instead):")
    for slug, n, person, credit in pill_report:
        log("  %-32s %3d items  (%s)  credit@deck: %s"
            % (slug, n, person, ", ".join(credit) or "!! NONE !!"))
    naked = [s for s, _, _, c in pill_report if not c]
    if naked:
        raise SystemExit("ABORTED — no deck-level maker credit on: %s" % ", ".join(naked))

# ------------------------------------------------- deck-level notes & artist credit
# A reader who used to find Waite/Papus on the card needs to be told where they went,
# and the artist who used to be credited on all 78 cards needs crediting once, here.
MARKER = "## One source per deck"
NOTES = {
    GD: """
## One source per deck

This deck reads the imagery through **Book T** and nothing else. Two voices that used to
sit on every card have moved to decks of their own, so you always know whose words you
are reading:

- **A. E. Waite's** own 1911 descriptions and divinatory meanings → `rider-waite-smith-pictorial-key`
- **Papus's** *Le Tarot des Bohémiens* (1889) → `papus-tarot-des-bohemiens`

The `Scene` and `Symbol` notes are this repo's own editorial description of the picture
and stay here.

## The art, credited once

Art by **Pamela Colman Smith** (1909) — all 78 cards — credited by Waite in his text
though not in the deck's market name. Stated here at deck level rather than repeated as a
biography box on every card; her record is in `people-of-tarot`.
""",
    WIRTH: """
## One source per deck

This deck reads Wirth's 22 plates through **Wirth's own commentary** and nothing else.
**Papus's** *Le Tarot des Bohémiens* (1889), which used to sit on every card here, is now
its own deck — `papus-tarot-des-bohemiens` — illustrated with these same plates, since
Papus's book reproduced them. Same pictures, a different book about them.
""",
    GEBELIN: """
## One source per deck

This deck carries **Court de Gébelin's** 1781 reading and nothing else. **Papus's** *Le
Tarot des Bohémiens* (1889), which used to sit on every card here, is now its own deck —
`papus-tarot-des-bohemiens`.
""",
}
CREDITS = {
    GD: "Art by Pamela Colman Smith (Rider-Waite-Smith, 1909), read here through the Golden "
        "Dawn's 'Book T'; public-domain scans via Wikimedia Commons",
}
for slug, note in NOTES.items():
    g = loaded[slug]
    if MARKER not in (g.get("description") or ""):
        g["description"] = (g.get("description") or "").rstrip() + "\n" + note
        log("  %-26s deck description: appended 'One source per deck' note" % slug)
for slug, credit in CREDITS.items():
    if loaded[slug].get("image_credit") != credit:
        loaded[slug]["image_credit"] = credit
        log("  %-26s image_credit: names the artist at deck level" % slug)

# ------------------------------------------------------------------- VERIFICATION
# Everything removed must still exist: in a new deck, or in research/sources/*.md.
haystacks = {}
for slug, g in ((RWS_NEW, rws), (PAPUS_NEW, papus)):
    haystacks["deck:" + slug] = norm(" ".join(
        v for it in g["items"] for v in (it.get("sections") or {}).values()))
for p in sorted(glob.glob(os.path.join(SOURCES, "*.md"))):
    haystacks["sources:" + os.path.basename(p)] = norm(open(p, encoding="utf-8").read())

lost = []
found_in = {}
for slug, iid, key, text in removed:
    t = norm(body(text))
    if not t:
        continue
    where = [name for name, hay in haystacks.items() if t in hay]
    if where:
        found_in[(slug, iid, key)] = where[0]
    else:
        lost.append((slug, iid, key, len(t), text))

total_chars = sum(len(norm(body(t))) for _, _, _, t in removed)
log("verification: %d removed section bodies, %d normalised characters" % (len(removed), total_chars))
if lost:
    log("!! %d removed bodies NOT found anywhere (%d chars would be lost):"
        % (len(lost), sum(x[3] for x in lost)))
    for slug, iid, key, n, _ in lost[:20]:
        log("     %s / %s / %s (%d chars)" % (slug, iid, key, n))
    raise SystemExit("ABORTED — refusing to drop text that is not preserved elsewhere")
log("verification: PASS — every removed body is preserved (0 characters lost)")
by_dest = {}
for dest in found_in.values():
    by_dest[dest] = by_dest.get(dest, 0) + 1
for dest, n in sorted(by_dest.items()):
    log("     %-52s %3d bodies" % (dest, n))

if CHECK:
    log("--check: nothing written")
    sys.exit(0)

# ------------------------------------------------------------------------- write
save(RWS_NEW, rws)
save(PAPUS_NEW, papus)
for slug, g in loaded.items():
    save(slug, g)
log("wrote 2 new grammars + %d edited grammars" % len(loaded))
