# -*- coding: utf-8 -*-
"""Build the quick-jump search index: search-index.json at the repo root.

  python scripts/build_search_index.py          # rebuild
  python scripts/build_search_index.py --check  # exit 1 if the committed file is stale

GENERATED FILE — never hand-edit search-index.json. It is rebuilt by
scripts/check_all.py (the pre-commit gate) and by .github/workflows/build-meta.yml
on every push to main that touches tarot/ or course/, so it cannot drift from the
grammars and chapters it describes.

What goes in (zero AI, plain data; the browser does the matching — see quick-jump.js):
  * every card of every deck grammar in tarot/<slug>/grammar.json, with aliases:
    the deck's own number (arabic + roman), the canonical trump name the meta build
    derives (major_from_name), its Thoth-era names (Justice -> Adjustment …), the
    suit/rank words in every language the decks use, and short metadata strings
    (Hebrew letter, sign, Golden Dawn title, Italian/French names);
  * one row per deck (opens the deck);
  * one "across every deck" row per trump and per minor card, opening the Lenses
    page on it (viewers/prototypes/lenses.html?card=justice), so "Justice" also
    offers Justice in all decks side by side;
  * the people and books of the sources wing;
  * every course (course/*.mdx) and every ## / ### heading in it, with the card
    and deck words its section mentions, linking to course-viewer.html#<anchor>
    (the anchor is computed exactly as the course viewer computes it);
  * a short list of site pages (Play, Caster, Timeline …).

The same file can be read by any tool, including the recursive.eco assistant
(see docs/QUICK-JUMP-SEARCH.md): searching it needs no model.
"""
import glob, json, os, re, sys, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TAROT = os.path.join(ROOT, "tarot")
COURSE = os.path.join(ROOT, "course")
OUT = os.path.join(ROOT, "search-index.json")

sys.path.insert(0, os.path.dirname(__file__))
from build_meta_grammar import (DECKS, MAJ_NAMES, RANK_NAMES,  # noqa: E402
                                major_from_name, suit_norm, rank_from_name)

R2 = "https://pub-71ebbc217e6247ecacb85126a6616699.r2.dev/grammar-illustrations/"

# Grammars that are not decks of cards to jump to. The *-course grammars are generated
# from course/*.mdx, which this index reads directly (and links to the course viewer).
SKIP = {"all-decks-many-lenses", "how-to-contribute", "tree-of-tarot",
        "build-a-tarot-deck-with-claude-course"}
SOURCES = {"people-of-tarot": "p", "books-of-tarot": "b"}   # kind per sources grammar

# Names the same trump carries in decks this site does not hold (Thoth, older English).
THOTH = {1: ["magus", "juggler"], 2: ["papess"], 5: ["pope"], 8: ["lust", "fortitude"],
         10: ["fortune"], 11: ["adjustment"], 14: ["art"], 20: ["aeon", "last judgement"],
         21: ["universe"], 0: ["matto"], 16: ["house of god"]}
SUIT_WORDS = {
    "Wands": "wands batons bastoni staves rods clubs",
    "Cups": "cups coppe coupes hearts chalices",
    "Swords": "swords spade epees spades",
    "Coins": "coins pentacles denari deniers disks discs diamonds",
}
RANK_WORDS = {1: "ace one", 11: "page knave jack valet fante princess",
              12: "knight cavalier chevalier cavallo prince", 13: "queen reine regina",
              14: "king roi re"}
# Short, stable metadata strings worth matching. Long prose stays out (size + noise).
META_ALIAS_KEYS = ("hebrew_translit", "golden_dawn_title", "attribution", "sign", "planet",
                   "decan", "italian_name", "french_name", "names_en", "figure", "sephirah",
                   "suit_italian", "suit_french", "golden_dawn_rank", "role_group", "lifespan",
                   "author", "year")
DECK_ALIASES = {   # what people call these decks when they type
    "golden-dawn-book-t-tarot": "gd book t golden dawn",
    "rider-waite-smith-pictorial-key": "rws waite smith rider pictorial key",
    "tarot-de-marseille-conver": "tdm marseille conver",
    "visconti-sforza-tarot": "visconti sforza pierpont morgan bembo",
    "oswald-wirth-tarot": "wirth",
    "papus-tarot-des-bohemiens": "papus bohemiens",
    "minchiate-florence-tarot": "minchiate florence",
    "tarocchino-bologna": "bologna tarocchino",
    "petit-lenormand": "lenormand",
}
# Site pages that are views, not data. href is relative to the repo root.
PAGES = [
    ("Home", "index.html", "home"),
    ("About", "pages/about.html", "about"),
    ("Play — games & readings", "pages/play.html", "play games"),
    ("Spread Caster — build, cast, send", "viewers/caster-studio.html", "caster spread reading"),
    ("Card Table — less, keep, more", "viewers/table.html", "card table"),
    ("Explorer — every card, every deck", "viewers/explorer.html", "explorer views"),
    ("Cards — the card view", "viewers/cards.html", "cards view"),
    ("Tree view", "viewers/tree-viewer.html", "tree view"),
    ("Tree of Tarot — the genealogy ring", "viewers/genealogy-tree.html", "tree of tarot genealogy ring"),
    ("Timeline", "viewers/timeline.html", "timeline history dates"),
    ("Genealogy", "genealogy.html", "genealogy family"),
    ("Golden Dawn decks", "pages/golden-dawn-decks.html", "golden dawn decks"),
    ("Book T (1912) — the whole text", "pages/book-t.html", "book t 1912 equinox golden dawn text decans"),
    ("Sources — people & books", "pages/sources.html", "sources people books bibliography"),
    ("All courses", "pages/courses.html", "courses gallery"),
    ("Contribute", "pages/contribute.html", "contribute help"),
    ("Shop — printed decks", "pages/shop.html", "shop print buy"),
    ("Channels", "pages/channels.html", "channels"),
]
# The Lenses page's own keys (viewers/prototypes/lenses.html TRUMP_LABELS / minor_key).
TRUMP_KEYS = ["fool", "magician", "high-priestess", "empress", "emperor", "hierophant", "lovers",
              "chariot", "strength", "hermit", "wheel-of-fortune", "justice", "hanged-man", "death",
              "temperance", "devil", "tower", "star", "moon", "sun", "judgement", "world"]
RANK_NUM = {"ace": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
            "nine": 9, "ten": 10, "page": 11, "damsel": 11, "knight": 12, "horsewoman": 12,
            "queen": 13, "king": 14}
LENS_SUIT = {"coins": "Coins", "cups": "Cups", "swords": "Swords", "batons": "Wands"}


def across_order(kind_key, key):
    if kind_key == "trump_key":
        return (0, TRUMP_KEYS.index(key) if key in TRUMP_KEYS else 99, key)
    rank, _, suit = key.partition("-of-")
    return (1, ["coins", "cups", "swords", "batons"].index(suit) if suit in LENS_SUIT else 9,
            RANK_NUM.get(rank, 99), key)


STOP = {"the", "of", "a", "an", "and", "la", "le", "les", "il", "lo", "de", "du", "des",
        "di", "del", "della", "in", "on", "to", "for", "with", "its", "is"}


def norm(s):
    """Lowercase, accents off, punctuation to spaces. quick-jump.js does the same."""
    s = unicodedata.normalize("NFD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def words(*parts):
    seen, out = set(), []
    for p in parts:
        for w in norm(p).split():
            if w not in seen:
                seen.add(w)
                out.append(w)
    return out


def roman(n):
    if n == 0:
        return "0"
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, r in vals:
        while n >= v:
            out += r
            n -= v
    return out if n == 0 else ""


def as_int(v):
    s = str(v if v is not None else "").strip()
    return int(s) if s.isdigit() else None


def img(u):
    if not u:
        return None
    return "~" + u[len(R2):] if u.startswith(R2) else u


def card_aliases(it, title_words):
    """-> (strong, weak). Strong: what the card IS (its trump or suit/rank in every naming,
    its own numeral, short identifiers such as its Hebrew letter or sign). Weak: what the
    data relates it to (keywords; an archetype mapping that its name does not carry,
    e.g. Sola Busca's 'Tulio' sitting in Justice's place)."""
    m = it.get("metadata") or {}
    name = it.get("name") or ""
    strong, weak = [], []
    raw = str(m.get("number") or "").strip()
    num = as_int(raw)
    own_roman = raw if raw and not raw.isdigit() and len(raw) <= 6 else None
    if num is None and own_roman is None:
        num = as_int(m.get("trump_number"))
    suit = suit_norm(m.get("suit") or m.get("suit_italian") or "")
    arc = str(m.get("arcana") or "").lower()
    major = None if suit else major_from_name(name)
    if major is not None:
        strong += [MAJ_NAMES[major], " ".join(THOTH.get(major, []))]
    elif not suit and arc in ("major", "trump") and num is not None and num <= 21:
        # a named figure in a trump's numbered place (Minchiate's Hunchback at 11, Sola
        # Busca's Tulio): related to that trump, not the trump itself
        weak += [MAJ_NAMES[num], " ".join(THOTH.get(num, []))]
    if major is not None or arc in ("major", "trump"):
        strong.append("trump major arcana")
        if own_roman:
            strong.append(own_roman)
        elif num is not None:
            strong += [str(num), roman(num)]
    if suit:
        rank = rank_from_name(name) or (num if num and 1 <= num <= 14 else None)
        strong += [SUIT_WORDS[suit], "minor arcana"]
        if rank:
            strong += [RANK_NAMES.get(rank, ""), RANK_WORDS.get(rank, ""), str(rank) if rank <= 10 else ""]
            if 11 <= rank <= 14:
                strong.append("court")
    arch = str(m.get("archetype") or "")
    if ":" in arch:
        an = arch.split(":", 1)[1].replace("-", " ")
        (strong if major is not None or suit else weak).append(an)
    for k in META_ALIAS_KEYS:
        v = m.get(k)
        if isinstance(v, (str, int)) and len(str(v)) <= 60:
            strong.append(str(v))
        elif isinstance(v, list):
            strong += [str(x) for x in v if isinstance(x, str) and len(x) <= 40]
    for kw in it.get("keywords") or []:
        if isinstance(kw, str) and len(kw) <= 30 and ":" not in kw:
            weak.append(kw)
    tw = set(title_words)
    sw = [w for w in words(*strong) if w not in tw and w not in STOP]
    s_set = set(sw) | tw
    ww = [w for w in words(*weak) if w not in s_set and w not in STOP]
    return " ".join(sw), " ".join(ww)


def deck_label(slug, g):
    md = g.get("metadata") or {}
    if slug in DECKS:
        return DECKS[slug]["label"]
    return md.get("common_name") or (g.get("name") or slug).split(" — ")[0]


def is_card(it):
    return not it.get("composite_of") and it.get("category") not in (
        "axis", "keyword-emergence", "overview", "emergence")


# ── course headings: the anchor is computed exactly as pages/course-viewer.html does ──
FM_RE = re.compile(r"^﻿?---\r?\n([\s\S]*?)\r?\n---")


def md_text(s):
    s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"(\*\*|__|\*|_|`)", "", s)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'"), ("&nbsp;", " ")):
        s = s.replace(a, b)
    return s.strip()


def js_slug(text):
    # JS: text.toLowerCase().replace(/[^\w]+/g,'-').replace(/^-|-$/g,'')   (\w is ASCII)
    return re.sub(r"^-|-$", "", re.sub(r"[^A-Za-z0-9_]+", "-", text.lower()))


def parse_course(path):
    raw = open(path, encoding="utf-8").read()
    meta, body = {}, raw
    m = FM_RE.match(raw)
    if m:
        body = raw[m.end():]
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if v:
                meta[k.strip()] = v.strip().strip("\"'")
    heads, in_code = [], False
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        hm = re.match(r"^(#{1,3})\s+(.+?)\s*#*\s*$", line)
        if hm:
            heads.append((len(hm.group(1)), md_text(hm.group(2)), i))
    title = meta.get("title") or next((t for lvl, t, _ in heads if lvl == 1), os.path.basename(path)[:-4])
    # ids: the viewer assigns all h2 ids first, then all h3 ids, de-duplicating with -2, -3 …
    used, ids = set(), {}

    def uniq(base):
        base = base or "section"
        i, n = base, 1
        while i in used:
            n += 1
            i = "%s-%d" % (base, n)
        used.add(i)
        return i
    for lvl in (2, 3):
        for idx, (l, t, _) in enumerate(heads):
            if l == lvl:
                ids[idx] = uniq(js_slug(t))
    sections = []
    for idx, (l, t, ln) in enumerate(heads):
        if l not in (2, 3):
            continue
        nxt = next((h[2] for h in heads[idx + 1:] if h[0] <= l), len(lines))
        sections.append((l, t, ids[idx], "\n".join(lines[ln + 1:nxt])))
    return title, meta.get("description", ""), sections


def build():
    decks, entries = [], []
    vocab = set()          # card/deck words a chapter section may mention
    across_t, across_m = {}, {}   # Lenses keys -> number of decks carrying them

    order = list(DECKS) + sorted(
        os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(TAROT, "*", "grammar.json"))
        if os.path.basename(os.path.dirname(p)) not in DECKS)
    for slug in order:
        path = os.path.join(TAROT, slug, "grammar.json")
        if slug in SKIP or slug.endswith("-course") or not os.path.exists(path):
            continue
        g = json.load(open(path, encoding="utf-8"))
        items = [it for it in g.get("items", []) if is_card(it) and it.get("id")]
        if not items:
            continue
        label = deck_label(slug, g)
        di = len(decks)
        dwords = words(label, g.get("name"), DECK_ALIASES.get(slug, ""), slug.replace("-", " "))
        decks.append({"s": slug, "n": label, "w": " ".join(w for w in dwords if w not in STOP)})
        vocab.update(w for w in words(label, DECK_ALIASES.get(slug, "")) if w not in STOP and len(w) > 2)
        kind = SOURCES.get(slug, "c")
        if kind == "c":
            entries.append({"k": "d", "t": g.get("name") or label, "d": di,
                            "img": img(g.get("cover_image_url")), "n": len(items)})
        seen_t, seen_m = set(), set()
        for it in items:
            md = it.get("metadata") or {}
            if md.get("trump_key"):
                seen_t.add(md["trump_key"])
            if md.get("minor_key"):
                seen_m.add(md["minor_key"])
        for k in seen_t:
            across_t[k] = across_t.get(k, 0) + 1
        for k in seen_m:
            across_m[k] = across_m.get(k, 0) + 1
        for it in items:
            t = it.get("name") or it["id"]
            e = {"k": kind, "t": t, "d": di, "i": it["id"]}
            a, x = card_aliases(it, words(t))
            if a:
                e["a"] = a
            if x:
                e["x"] = x
            im = img(it.get("image_url"))
            if im:
                e["img"] = im
            entries.append(e)

    # across every deck — the Lenses page (viewers/prototypes/lenses.html?card=<key>) lays one
    # card out in every deck side by side; its keys are the decks' stamped metadata.trump_key
    # / metadata.minor_key, so only keys some deck actually carries get a row.
    for kind_key, keys in (("trump_key", across_t), ("minor_key", across_m)):
        for key, n in sorted(keys.items(), key=lambda kv: across_order(kind_key, kv[0])):
            if kind_key == "trump_key":
                num = TRUMP_KEYS.index(key) if key in TRUMP_KEYS else None
                t = MAJ_NAMES[num] if num is not None else key.replace("-", " ").title()
                a = [t, " ".join(THOTH.get(num, [])), str(num), roman(num) if num is not None else "",
                     "trump major arcana"]
            else:
                rank, _, suit = key.partition("-of-")
                t = "%s of %s" % (rank.title(), suit.title())
                a = [RANK_WORDS.get(RANK_NUM.get(rank), ""), SUIT_WORDS.get(LENS_SUIT.get(suit), ""),
                     "court" if RANK_NUM.get(rank, 0) > 10 else "", "minor arcana"]
            tw = set(words(t))
            entries.append({"k": "x", "t": t, "i": key, "n": n,
                            "a": " ".join(w for w in words("every deck all decks across side by side", *a)
                                          if w not in tw and w not in STOP)})
    for n in MAJ_NAMES:
        vocab.update(w for w in words(n) if w not in STOP)
    for t in THOTH.values():
        for n in t:
            vocab.update(w for w in words(n) if w not in STOP)
    for w in SUIT_WORDS.values():
        vocab.update(w.split())
    vocab.update(["pathworking", "kabbalah", "decan", "decans", "sephiroth", "tree", "life",
                  "reversals", "dignities", "court", "courts", "trumps", "pips", "spread"])
    vocab -= STOP

    # courses + their ## / ### headings
    courses = []
    for path in sorted(glob.glob(os.path.join(COURSE, "*.mdx"))):
        cid = os.path.basename(path)[:-4]
        title, desc, sections = parse_course(path)
        ci = len(courses)
        courses.append({"id": cid, "t": title})
        entries.append({"k": "o", "t": title, "c": ci,
                        "a": " ".join(w for w in words(desc) if w in vocab)})
        for lvl, text, anchor, body in sections:
            bw = set(norm(body).split())
            x = " ".join(sorted(w for w in bw & vocab if w not in set(words(text))))
            e = {"k": "h", "t": text, "c": ci, "h": anchor}
            if x:
                e["x"] = x
            entries.append(e)

    for t, href, a in PAGES:
        entries.append({"k": "g", "t": t, "u": href, "a": a})

    return {
        "_generated": "by scripts/build_search_index.py. Do not hand-edit; see docs/QUICK-JUMP-SEARCH.md",
        "v": 1,
        "img": R2,
        "kinds": {"c": "card", "d": "deck", "x": "one card across every deck (Lenses)", "p": "person", "b": "book",
                  "o": "course", "h": "chapter section", "g": "site page"},
        "decks": decks,
        "courses": courses,
        "entries": entries,
    }


def dump(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"


if __name__ == "__main__":
    data = dump(build())
    if "--check" in sys.argv:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if cur != data:
            print("search-index.json is stale: run python scripts/build_search_index.py")
            sys.exit(1)
        print("search-index.json up to date")
        sys.exit(0)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)
    d = json.loads(data)
    kinds = {}
    for e in d["entries"]:
        kinds[e["k"]] = kinds.get(e["k"], 0) + 1
    print("search index: %d entries %s, %d decks, %d courses, %.0f KB -> %s" % (
        len(d["entries"]), kinds, len(d["decks"]), len(d["courses"]), len(data.encode()) / 1024,
        os.path.relpath(OUT, ROOT)))
