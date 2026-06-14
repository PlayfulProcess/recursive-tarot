# -*- coding: utf-8 -*-
"""Generate a print-ready (KDP / IngramSpark) book from the SAME single sources the
live course uses — course/history-of-tarot.mdx (prose) + the grammars (data) — but
with images downloaded and DOWNSCALED locally, so the PDF is a sane size.

Output:  print/book/book.html        (self-contained, KDP @page CSS, local images)
         print/book/build/img/*.jpg  (downscaled card images — gitignored)
Then:    render to PDF with headless Chrome (command printed at the end; pass
         --pdf to run it automatically if Chrome is found).

Trim:    7 x 10 in, no-bleed interior (the images are inline strips, not full-bleed).
         Add bleed only if you later want full-bleed plates.

Run:     python scripts/generate_book.py            # html only
         python scripts/generate_book.py --pdf      # html + PDF via headless Chrome
"""
import json, os, re, sys, hashlib, urllib.request, subprocess
from io import BytesIO
from PIL import Image

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TAROT = os.path.join(ROOT, "tarot")
BOOK = os.path.join(ROOT, "print", "book")
IMGDIR = os.path.join(BOOK, "build", "img")
OUT = os.path.join(BOOK, "book.html")
MDX = os.path.join(ROOT, "course", "history-of-tarot.mdx")
SYN = os.path.join(ROOT, "research", "synthesis", "trumps.json")
IMG_W = 360  # downscaled card width in px (~1.2in at 300dpi — plenty for a 1in print strip)

ORDER = ["fool","magician","high-priestess","empress","emperor","hierophant","lovers","chariot",
         "strength","hermit","wheel-of-fortune","justice","hanged-man","death","temperance","devil",
         "tower","star","moon","sun","judgement","world"]

def load(p):
    return json.loads(open(p, encoding="utf-8").read())

def esc(s):
    return (str(s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def slugify(s):
    """Match marked.js GitHub-style heading ids, so MDX links resolve identically
    in the printed book and the on-screen course viewer."""
    s = re.sub(r"\[@[^\]]+\]", "", str(s or "")).lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"[\s_-]+", "-", s)

def inline(s):
    s = re.sub(r"\s*\[@[^\]]+\]", "", str(s or ""))      # drop citation keys
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    # markdown links [text](href) — only the MDX prose uses these; grammar
    # attributions are [Author, Work] with no trailing (...), so they're untouched.
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s

def para(s):
    return "".join("<p>%s</p>" % inline(b) for b in re.split(r"\n{2,}", str(s or "").strip()) if b.strip())

def attribution(text):
    """The leading [Author, Work, Year] line a later-interpretation section opens with."""
    m = re.match(r"^\s*\[([^\]]{3,200})\]", str(text or ""))
    return m.group(1).strip() if m else None

def attr_year(a):
    m = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", a or "")
    return int(m.group(1)) if m else 9999

def strip_attr(text):
    return re.sub(r"^\s*\[[^\]]*\]\s*", "", str(text or ""))

# ── image cache: download once, downscale, return path relative to book.html ──
os.makedirs(IMGDIR, exist_ok=True)
_imgfail = [0]
def thumb(url, w=IMG_W):
    if not url:
        return None
    h = hashlib.md5(("%s@%d" % (url, w)).encode()).hexdigest()[:16]
    rel = "build/img/%s.jpg" % h
    dst = os.path.join(BOOK, rel)
    if os.path.exists(dst):
        return rel
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "recursive-tarot-book"})
        data = urllib.request.urlopen(req, timeout=30).read()
        im = Image.open(BytesIO(data)).convert("RGB")
        im.thumbnail((w, w * 3))      # cap width; keep aspect
        im.save(dst, "JPEG", quality=85, optimize=True)
        return rel
    except Exception as e:
        _imgfail[0] += 1
        return None

# ── data ──
col = load(os.path.join(TAROT, "_collection.json"))
decks = [g for g in col["grammars"] if not g.get("is_meta") and g.get("type") != "meta"]
synth = load(SYN)
suits = load(os.path.join(ROOT, "research", "synthesis", "suits.json"))
SUIT_CANON = {"cups":"cups","coins":"coins","swords":"swords","batons":"batons",
              "wands":"batons","pentacles":"coins","disks":"coins","staves":"batons","clubs":"batons"}
suit_idx = {}
minor_idx = {}   # archetype (card:ace-of-wands) -> [ {slug,name,year,sections} ]  — cross-deck "same minor card"
people = load(os.path.join(TAROT, "people-of-tarot", "grammar.json"))
tree = {it["id"]: it for it in load(os.path.join(TAROT, "tree-of-tarot", "grammar.json"))["items"]}
meta = load(os.path.join(TAROT, "all-decks-many-lenses", "grammar.json"))
essay_item = next((i for i in meta["items"] if i["id"] == "essay-divination-question"), None)

# people who MADE / commissioned each deck (metadata.made) — woven into each deck chapter
makers_by_deck = {}
for _p in people["items"]:
    if (_p.get("metadata") or {}).get("kind") == "person" or _p.get("category") == "person":
        for _slug in ((_p.get("metadata") or {}).get("made") or []):
            makers_by_deck.setdefault(_slug, []).append(_p)

# trump_key -> [ {slug,name,year,id,img} ] (decks loaded once)
trump_idx = {}
deck_meta = {}
for g in decks:
    slug = g["slug"]; deck_meta[slug] = g
    try:
        dg = load(os.path.join(TAROT, slug, "grammar.json"))
    except Exception:
        continue
    g["_desc"] = dg.get("description")
    g["_sig"] = [(it.get("image_url") or (it.get("metadata") or {}).get("image_url"))
                 for it in dg.get("items", [])
                 if it.get("level", 1) == 1 and (it.get("image_url") or (it.get("metadata") or {}).get("image_url"))]
    g["_coll"] = sorted({(it.get("metadata") or {}).get("collection") for it in dg.get("items", [])
                         if (it.get("metadata") or {}).get("collection")})
    g["_gh"] = dg.get("_github_url") or dg.get("_github_source_url")
    g["_credit"] = dg.get("image_credit")
    for it in dg.get("items", []):
        md = it.get("metadata") or {}
        img = it.get("image_url") or md.get("image_url")
        suit = md.get("suit")
        if suit and img:
            cs = SUIT_CANON.get(str(suit).lower())
            if cs:
                suit_idx.setdefault(cs, {}).setdefault(slug, []).append(img)
        arch = md.get("archetype")
        if arch and str(arch).startswith("card:") and (md.get("arcana") == "minor" or suit):
            minor_idx.setdefault(arch, []).append({
                "slug": slug, "name": (g.get("name") or slug).split(" — ")[0],
                "year": g.get("year") or 9999, "img": img,
                "sections": it.get("sections") or {}})
        tk = md.get("trump_key")
        if not tk:
            continue
        trump_idx.setdefault(tk, []).append({
            "slug": slug, "name": (g.get("name") or slug).split(" — ")[0],
            "year": g.get("year") or 9999, "id": it.get("id"), "img": img,
            "sections": it.get("sections") or {}})

def deck_name(slug):
    return (deck_meta.get(slug, {}).get("name") or slug).split(" — ")[0]
def deck_year(slug):
    return deck_meta.get(slug, {}).get("year")

# ── embed renderers ──
def render_markdown(text):
    """Deck descriptions are little markdown docs — render body, drop the top # title
    (the chapter heading already names the deck)."""
    out = []
    for block in re.split(r"\n{2,}", str(text or "").strip()):
        b = block.strip()
        if b.startswith("### ") or b.startswith("## "):
            out.append("<h4>%s</h4>" % inline(b.lstrip("# ")))
        elif b.startswith("# "):
            continue
        elif b.startswith("- ") or b.startswith("* "):
            items = "".join("<li>%s</li>" % inline(li.lstrip("-* ")) for li in b.splitlines())
            out.append("<ul>%s</ul>" % items)
        else:
            out.append(para(b))
    return "".join(out)

def render_decks():
    out, n = [], 0
    for g in sorted(decks, key=lambda x: x.get("year") or 9999):
        slug = g["slug"]
        sigs = (g.get("_sig") or [])
        cover = g.get("cover_image_url") or (sigs[0] if sigs else None)
        rel = thumb(cover) if cover else None
        coverhtml = ('<img class="deck-cover" src="%s">' % esc(rel)) if rel else ""
        cells = []
        for im in sigs[1:9]:
            r = thumb(im)
            if r:
                cells.append('<figure class="c"><img src="%s"></figure>' % esc(r)); n += 1
        strip = ('<div class="strip">%s</div>' % "".join(cells)) if cells else ""
        yl = g.get("year_label") or g.get("year")
        # weave in the people behind this deck
        makers = ""
        mk = makers_by_deck.get(slug) or []
        if mk:
            rows = []
            for p in mk:
                who = re.sub(r"\s*\[@[^\]]+\]", "", (p.get("sections") or {}).get("Who") or "")
                first = who.split(". ")[0]
                life = (p.get("metadata") or {}).get("lifespan") or ""
                rows.append('<p class="maker"><strong>%s%s</strong> — %s.</p>'
                            % (esc(p["name"]), (" (%s)" % esc(life)) if life else "", inline(first[:240])))
            makers = '<div class="made-by"><h4>The hands behind it</h4>%s</div>' % "".join(rows)
        out.append('<section class="deck-chapter" id="deck-%s"><h3>%s%s</h3>%s%s%s%s</section>'
                   % (slug, esc((g.get("name") or slug).split(" — ")[0]),
                      (" · %s" % yl) if yl else "", coverhtml, render_markdown(g.get("_desc")), makers, strip))
    print("  deck signature images: %d" % n)
    return "".join(out)

SUIT_ORDER = ["batons", "coins", "swords", "cups"]
SUIT_TITLE = {"batons": "Batons (Wands)", "coins": "Coins (Pentacles)", "swords": "Swords", "cups": "Cups"}
SUIT_ANCHORS = ["tarot-de-marseille-conver", "sola-busca-tarot", "golden-dawn-book-t-tarot", "visconti-sforza-tarot"]

def render_suits():
    out = ['<div class="suit-intro">%s</div>' % para(suits.get("_intro"))]
    n = 0
    for cs in SUIT_ORDER:
        syn = suits.get(cs)
        if not syn:
            continue
        cells = []
        for slug in SUIT_ANCHORS:
            for im in ((suit_idx.get(cs) or {}).get(slug) or [])[:5]:
                r = thumb(im)
                if r:
                    cells.append('<figure class="c"><img src="%s"></figure>' % esc(r)); n += 1
        strip = ('<div class="strip">%s</div>' % "".join(cells)) if cells else ""
        out.append('<section class="card-chapter"><h3>The Suit of %s</h3><div class="synthbox">%s</div>%s</section>'
                   % (esc(SUIT_TITLE[cs]), para(syn), strip))
    print("  suit images: %d" % n)
    return "".join(out)

def fig(which):
    label = "The Lineage of Tarot" if which == "lineage" else "Timeline · 1440s–1900s"
    return ('<figure class="figure"><img src="figures/%s.png" alt="%s">'
            '<figcaption>%s</figcaption></figure>' % (which, esc(label), esc(label)))

def render_people():
    """Organised by ROLE (makers, patrons, occultists, scholars, institutions) — a
    different cut from the deck chapters, which already name each deck's own makers."""
    items = {i["id"]: i for i in people["items"]}
    r3 = items.get("root-people-of-tarot")
    out = []
    if r3:
        out.append('<div class="people-weave">%s</div>' % para((r3.get("sections") or {}).get("What it is")))
    for gid in ["grp-makers", "grp-patrons", "grp-occultists", "grp-scholars", "grp-institutions"]:
        grp = items.get(gid)
        if not grp:
            continue
        out.append("<h3>%s</h3>" % esc(grp.get("name")))
        wt = (grp.get("sections") or {}).get("What this groups")
        if wt:
            out.append(para(wt))
        for cid in (grp.get("composite_of") or []):
            p = items.get(cid)
            if not p:
                continue
            who = re.sub(r"\s*\[@[^\]]+\]", "", (p.get("sections") or {}).get("Who") or "")
            life = (p.get("metadata") or {}).get("lifespan") or ""
            out.append('<div class="bio"><div class="bio-name">%s%s</div><div class="bio-text">%s</div></div>'
                       % (esc(p.get("name")), (' <span class="bio-life">%s</span>' % esc(life)) if life else "", para(who)))
    return "".join(out)

ANCHOR_EARLY = ["cary-yale-visconti-tarot", "visconti-sforza-tarot", "charles-vi-tarot", "este-tarot"]
_NIMG = [0]

def _strip(tk):
    cells = []
    for c in sorted(trump_idx.get(tk, []), key=lambda x: x["year"]):
        rel = thumb(c["img"])
        if rel:
            cells.append('<figure class="c"><img src="%s"><figcaption>%s</figcaption></figure>'
                         % (esc(rel), esc(c["name"][:16])))
            _NIMG[0] += 1
    return ('<div class="strip">%s</div>' % "".join(cells)) if cells else ""

# curated full-page plates — the most striking cards (deck slug, trump_key, caption)
PLATES = [
    ("visconti-sforza-tarot", "world", "The World — Visconti-Sforza, Milan, c. 1451. Hand-painted on gold ground for the ducal court."),
    ("cary-yale-visconti-tarot", "death", "Death — Cary-Yale Visconti, c. 1442. The earliest surviving Death: a mounted archer, rendered with courtly dignity."),
    ("tarot-de-marseille-conver", "moon", "The Moon — Tarot de Marseille (Conver), 1760. The uncanny scene that the occultists inherited whole."),
    ("court-de-gebelin-tarot", "magician", "The Magician — Court de Gébelin's plates, 1781. Where the street conjurer was first read as an Egyptian sage."),
    ("golden-dawn-book-t-tarot", "death", "Death — Golden Dawn / Rider-Waite-Smith line, 1909. Death remade: mounted again, now bearing a banner of renewal."),
]

def render_plates():
    out, n = [], 0
    for slug, tk, cap in PLATES:
        entry = next((c for c in trump_idx.get(tk, []) if c["slug"] == slug and c["img"]), None)
        if not entry:
            continue
        rel = thumb(entry["img"], 900)
        if not rel:
            continue
        n += 1
        out.append('<figure class="plate"><img src="%s"><figcaption>%s</figcaption></figure>' % (esc(rel), inline(cap)))
    print("  plates: %d" % n)
    return "".join(out)

def render_bib():
    try:
        txt = open(os.path.join(ROOT, "research", "bibliography.bib"), encoding="utf-8").read()
    except Exception:
        return ""
    rows = []
    for m in re.finditer(r"@\w+\s*\{[^,]+,(.*?)\n\}", txt, re.S):
        body = m.group(1)
        def f(name):
            mm = re.search(name + r"\s*=\s*[{\"]([^}\"]*)[}\"]", body, re.I)
            return mm.group(1).strip() if mm else ""
        au, ti, yr = f("author") or f("editor"), f("title"), f("year")
        if ti:
            rows.append((au, ti, yr))
    rows.sort(key=lambda r: (r[0].lower(), r[2]))
    return "".join('<p class="bibentry">%s%s%s.</p>'
                   % ((inline(au) + ". ") if au else "", "<em>%s</em>" % inline(ti), (" (%s)" % yr) if yr else "")
                   for au, ti, yr in rows)

def render_apparatus():
    out = ["<h3>Image credits</h3>",
           "<p>Every card image reproduced in this book is in the <strong>public domain</strong> — the original works all predate the twentieth century. Reproductions are drawn from the holding institutions and digital archives listed below; full per-card provenance lives in the research dossiers at the project's GitHub repository.</p>",
           '<ul class="credits">']
    for g in sorted(decks, key=lambda x: x.get("year") or 9999):
        src = g.get("_credit") or ("; ".join(g.get("_coll") or []) or "public domain — see the deck's research dossier")
        out.append("<li><strong>%s.</strong> %s.</li>" % (esc((g.get("name") or g["slug"]).split(" — ")[0]), inline(src)))
    out.append("</ul>")
    out.append("<h3>Sources &amp; further reading</h3>")
    out.append("<p>The historical claims throughout are cited in the per-card and per-deck research dossiers (each <em>Research note</em> links to its source). The full bibliography follows.</p>")
    out.append('<div class="bib">%s</div>' % render_bib())
    out.append("<h3>About this book</h3>")
    out.append("<p>Generated from the open data of <strong>The Recursive Tarot</strong> — a public-domain collection of historical tarot grammars. Text is licensed CC-BY-SA-4.0; the card images are public domain. Source and data: github.com/PlayfulProcess/recursive-tarot.</p>")
    return "".join(out)

def render_essay():
    if not essay_item:
        return ""
    return "".join("<h3>%s</h3>%s" % (esc(k), para(v)) for k, v in (essay_item.get("sections") or {}).items())

def render_trumps_synth():
    """FRONT (the Story): each trump's cross-deck synthesis + image strip — readable straight through."""
    out = []
    for i, tk in enumerate(ORDER):
        if tk not in synth:
            continue
        out.append('<section class="card-chapter"><h3>%d — %s</h3><div class="synthbox">%s</div>%s</section>'
                   % (i, esc(tk.replace("-", " ").title()), para(synth[tk]), _strip(tk)))
    return "".join(out)

def render_trumps_detail():
    """CATALOGUE (the back): per trump, the literal per-deck Scenes + the dated later readings."""
    out = []
    for i, tk in enumerate(ORDER):
        if tk not in synth:
            continue
        entries = sorted(trump_idx.get(tk, []), key=lambda x: x["year"])
        def scene_of(slug):
            for c in entries:
                if c["slug"] == slug:
                    s = c["sections"]
                    return s.get("Scene") or s.get("About") or s.get("Iconography")
            return None
        early = next((s for s in ANCHOR_EARLY if scene_of(s)), None)
        anchors = [(slug, scene_of(slug)) for slug in [early, "tarot-de-marseille-conver", "golden-dawn-book-t-tarot"] if slug and scene_of(slug)]
        indecks = ""
        if anchors:
            indecks = "<h4>In the decks</h4>" + "".join(
                '<p class="indeck"><strong>%s · %s.</strong> %s%s</p>'
                % (esc(deck_name(s)), deck_year(s) or "", inline(sc[:520]), "…" if len(sc) > 520 else "")
                for s, sc in anchors)
        later, seen = [], set()
        for c in entries:
            for v in c["sections"].values():
                a = attribution(v)
                if not a:
                    continue
                voice = a.split(",")[0].strip()
                if voice in seen:
                    continue
                seen.add(voice)
                later.append((attr_year(a), a, strip_attr(v)))
        later.sort()
        laterhtml = ""
        if later:
            laterhtml = "<h4>Later readings</h4>" + "".join(
                '<div class="later"><div class="later-src">%s</div>%s</div>'
                % (esc(a), para(body[:760] + ("…" if len(body) > 760 else "")))
                for _, a, body in later)
        if indecks or laterhtml:
            out.append('<section class="card-chapter" id="trumpdetail-%s"><h3>%d — %s</h3>%s%s</section>'
                       % (tk, i, esc(tk.replace("-", " ").title()), indecks, laterhtml))
    return "".join(out)

_RANK_ORDER = {"ace":1,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,
               "eight":8,"nine":9,"ten":10,"page":11,"knave":11,"valet":11,"jack":11,"princess":11,
               "knight":12,"cavalier":12,"prince":12,"queen":13,"king":14}
SUIT_DETAIL_ANCHORS = ["sola-busca-tarot", "tarot-de-marseille-conver", "golden-dawn-book-t-tarot"]

def _arch_parts(arch):
    m = re.match(r"card:(.+?)-of-(.+)", arch or "")
    if not m:
        return (None, None, 99)
    rank, suit = m.group(1), m.group(2)
    return (rank, SUIT_CANON.get(suit, suit), _RANK_ORDER.get(rank, 50))

def render_suits_detail():
    """CATALOGUE (the back): the Minor Arcana card by card — pip and court — described
    in the decks' own words, in parallel to the Major Arcana detail below it."""
    # group archetypes by canonical suit
    by_suit = {}
    for arch in minor_idx:
        rank, cs, ro = _arch_parts(arch)
        if not cs:
            continue
        by_suit.setdefault(cs, []).append((ro, rank, arch))
    out = []
    for cs in SUIT_ORDER:
        cards = sorted(by_suit.get(cs, []))
        if not cards:
            continue
        out.append('<section class="card-chapter" id="suitdetail-%s"><h3>The Suit of %s</h3>' % (cs, esc(SUIT_TITLE[cs])))
        for ro, rank, arch in cards:
            entries = sorted(minor_idx.get(arch, []), key=lambda x: x["year"])
            def scene_of(slug):
                for c in entries:
                    if c["slug"] == slug:
                        s = c["sections"]
                        return s.get("Scene") or s.get("Description") or s.get("About") or s.get("Iconography")
                return None
            anchors = [(slug, scene_of(slug)) for slug in SUIT_DETAIL_ANCHORS if scene_of(slug)]
            indeck = ""
            if anchors:
                s, sc = anchors[0]
                indeck = '<span class="mscene"><strong>%s:</strong> %s%s</span>' % (
                    esc(deck_name(s)), inline(sc[:300]), "…" if len(sc) > 300 else "")
            # one attributed later reading (the divinatory meaning), if any
            later, seen = [], set()
            for c in entries:
                for v in c["sections"].values():
                    a = attribution(v)
                    if not a:
                        continue
                    voice = a.split(",")[0].strip()
                    if voice in seen:
                        continue
                    seen.add(voice)
                    later.append((attr_year(a), a, strip_attr(v)))
            later.sort()
            readinghtml = ""
            if later:
                _, a, body = later[0]
                readinghtml = '<span class="mread"><em>%s</em> — %s%s</span>' % (
                    esc(a.split(",")[0]), inline(body[:240]), "…" if len(body) > 240 else "")
            rank_label = (rank or "").replace("-", " ").title()
            out.append('<p class="minor-card"><strong>%s of %s.</strong> %s %s</p>'
                       % (esc(rank_label), esc(SUIT_TITLE[cs].split(" ")[0]), indeck, readinghtml))
        out.append("</section>")
    return "".join(out)

EMBED = {
    "lineage": lambda: fig("lineage"),
    "timeline": lambda: fig("timeline"),
    "essay": render_essay,
    "plates": render_plates,
    "apparatus": render_apparatus,
    "people": render_people,
    "decks": render_decks,
    "suits": render_suits,
    "suits-detail": render_suits_detail,
    "trumps-synthesis": render_trumps_synth,
    "trumps-detail": render_trumps_detail,
}

# ── render the MDX (single source for prose) ──
def render_mdx():
    body = []
    title = None
    raw = open(MDX, encoding="utf-8").read().lstrip("﻿").strip()
    # strip YAML frontmatter; lift its description into the book's subtitle
    subtitle = None
    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", raw, re.S)
    if fm:
        md = dict(re.findall(r'^([a-z_]+):\s*"?(.*?)"?\s*$', fm.group(1), re.M))
        subtitle = md.get("description")
        raw = raw[fm.end():]
    for block in re.split(r"\n{2,}", raw.strip()):
        b = block.strip()
        if b == "---":
            continue
        m = re.match(r'<div data-embed="([a-z\-]+)"', b)
        if m:
            fn = EMBED.get(m.group(1))
            if fn:
                body.append(fn())
            continue
        if b.startswith("### "):
            t = b[4:]
            body.append('<h3 id="%s">%s</h3>' % (slugify(t), inline(t)))
        elif b.startswith("## "):
            t = b[3:]
            body.append('<h2 class="chapter" id="%s">%s</h2>' % (slugify(t), inline(t)))
        elif b.startswith("# "):
            h = b[2:].strip()
            if title is None:
                title = h
                body.append("<h1>%s</h1>" % inline(h))
                if subtitle:
                    body.append('<p class="subtitle">%s</p>' % inline(subtitle))
            else:
                body.append('<h1 class="part">%s</h1>' % inline(h))   # Part II divider
        else:
            body.append(para(b))
    return (title or "The Recursive Tarot"), "".join(body)

CSS = """
@page { size: 7in 10in; margin: 0.62in 0.6in; }
@page :first { margin-top: 2in; }
html,body{ margin:0; }
body{ font: 11pt/1.55 Georgia,'Times New Roman',serif; color:#111; }
h1{ font-size:30pt; line-height:1.1; margin:0 0 .2em; }
h1.part{ break-before:page; font-size:32pt; text-align:center; margin-top:2.5in; color:#5a3fa0; }
h2{ font-size:19pt; margin:0; }
h2.chapter{ break-before:page; padding-top:.2in; }
h3{ font-size:13pt; margin:1.1em 0 .3em; break-after:avoid; }
p{ margin:0 0 .7em; text-align:justify; }
.subtitle{ font-style:italic; color:#555; font-size:13pt; margin-bottom:1.4em; }
em{ color:#222; }
.figure{ margin:1.2em 0; break-inside:avoid; text-align:center; }
.figure img{ max-width:100%; border:1px solid #ccc; border-radius:6px; }
figcaption{ font-size:8.5pt; color:#666; margin-top:.3em; }
.people h3, .card-chapter h3{ border-bottom:1px solid #ddd; padding-bottom:.15em; }
.bio{ break-inside:avoid; border-left:2px solid #b9a3f5; padding-left:.5em; margin:.6em 0; }
.bio-name{ font-weight:700; } .bio-life{ font-weight:400; color:#777; font-size:.85em; }
.bio-text p{ margin:.15em 0; font-size:10pt; }
.deck-chapter{ break-before:page; }
.deck-cover{ float:right; width:2.3in; margin:.1in 0 .3in .35in; border:1px solid #bbb; border-radius:6px; }
.made-by{ clear:both; margin-top:.6em; break-inside:avoid; }
.made-by .maker{ font-size:10pt; margin:.2em 0; }
.deck-chapter .strip{ clear:both; padding-top:.4em; }
.card-chapter{ break-before:page; }
.synthbox{ background:#f6f4fb; border:1px solid #d8c8f5; border-radius:8px; padding:.5em .7em; margin:.4em 0 .8em; }
.synthbox p{ margin:.2em 0; }
h4{ font-size:10.5pt; text-transform:uppercase; letter-spacing:.04em; color:#7a5fb0; margin:1em 0 .3em; break-after:avoid; }
.indeck{ font-size:10pt; margin:.3em 0; break-inside:avoid; }
.indeck strong{ color:#333; }
.later{ break-inside:avoid; margin:.5em 0; padding-left:.6em; border-left:2px solid #c9b8ee; }
.later-src{ font-style:italic; font-size:8.5pt; color:#777; margin-bottom:.1em; }
.later p{ font-size:10pt; margin:.15em 0; }
.minor-card{ font-size:10pt; margin:.3em 0; break-inside:avoid; }
.minor-card .mscene{ color:#333; }
.minor-card .mread{ color:#5a3fa0; }
.strip{ display:flex; flex-wrap:wrap; gap:7px; break-inside:avoid; }
.strip .c{ margin:0; text-align:center; width:1in; }
.strip .c img{ width:1in; height:1.6in; object-fit:cover; border:1px solid #ccc; border-radius:4px; }
.strip .c figcaption{ font-size:6.5pt; }
.plate{ break-before:page; break-inside:avoid; text-align:center; margin:0; padding-top:.3in; }
.plate img{ max-width:100%; max-height:7.6in; border:1px solid #ccc; }
.plate figcaption{ font-size:9pt; color:#555; margin-top:.5em; max-width:5in; margin-left:auto; margin-right:auto; }
.credits{ font-size:9.5pt; list-style:none; padding:0; }
.credits li{ margin:.3em 0; }
.bib{ column-count:1; }
.bibentry{ font-size:9pt; margin:.35em 0; padding-left:1.2em; text-indent:-1.2em; text-align:left; }
"""

def main():
    print("Generating book (downloading + downscaling images on first run)…")
    title, body = render_mdx()
    html = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><title>%s</title>"
            "<style>%s</style></head><body>%s</body></html>" % (esc(title), CSS, body))
    open(OUT, "w", encoding="utf-8").write(html)
    size_kb = os.path.getsize(OUT) / 1024
    print("  wrote %s (%.0f KB HTML)" % (os.path.relpath(OUT, ROOT), size_kb))
    if _imgfail[0]:
        print("  WARNING: %d images failed to download (cells skipped)" % _imgfail[0])

    if "--pdf" in sys.argv:
        chrome = next((p for p in [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ] if os.path.exists(p)), None)
        pdf = os.path.join(BOOK, "book.pdf")
        if chrome:
            print("  rendering PDF via headless Chrome…")
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            "--virtual-time-budget=15000",
                            "--print-to-pdf=" + pdf, "file:///" + OUT.replace("\\", "/")], check=False)
            if os.path.exists(pdf):
                print("  wrote %s (%.1f MB)" % (os.path.relpath(pdf, ROOT), os.path.getsize(pdf)/1048576))
        else:
            print("  Chrome not found; render manually with --print-to-pdf on file://%s" % OUT)

if __name__ == "__main__":
    main()
