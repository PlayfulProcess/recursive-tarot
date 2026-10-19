#!/usr/bin/env python3
"""Writes one static, crawlable page per Rider-Waite-Smith card, the card list, and the sitemap.

    python scripts/build_card_pages.py          # write card/*.html, tarot-card-meanings.html, sitemap.xml
    python scripts/build_card_pages.py --check  # fail if a generated page is stale (writes nothing)

Why (SEO, Oct 14 2026): every card lived only inside the JavaScript viewers
(viewers/cards.html?src=... reads the grammar JSON in the browser), so a search engine saw a page
called "Cards" and none of the text. These pages put each card's text in the HTML, with a unique
title and description, a canonical URL, Open Graph tags, JSON-LD and links to its neighbours.

Each tradition speaks in its own section and its own words, never blended (CLAUDE.md, "Gate, not
fate"): A. E. Waite's *Pictorial Key to the Tarot* (1911) from tarot/rider-waite-smith-pictorial-key,
then the Golden Dawn's Book T as printed in *The Equinox* I(8), 1912, from
tarot/golden-dawn-book-t-tarot (matched on metadata.archetype). Both are public domain; so are
Pamela Colman Smith's 1909 card images, shown as Wikimedia Commons thumbnails (the R2 originals
are about 1.2 MB each, too heavy for a page's first image).

Generated, never hand-edit: card/*.html, tarot-card-meanings.html, sitemap.xml and
data/sitemap-lastmod.json. Edit the two grammars and re-run. check_all.py runs --check.

Oct 20 2026 (SEO research, recursive-eco/docs/research/RESEARCH-seo-2026-10-20.md, ranks 2-4), the
same pattern for three more page families. The grammar.json files stay the one source; these pages
are a rendering of them for search engines, written outside tarot/ so recursive.eco (which reads
only recursive-eco.json and tarot/*/grammar.json) never sees them:
  book-t/<card>.html, book-t/decans.html, book-t/index.html   from tarot/book-t (all 78 cards)
  deck/<slug>.html, deck/index.html                           one per historical deck grammar
  spreads.html                                                Waite's own Celtic Cross + trump meanings
Images on deck pages follow docs/rights/image-ledger.json card by card: only an image the ledger
records as a Commons public-domain/CC0 or CC BY-SA file is shown, never a BnF/Gallica scan
(non-commercial only), an image recorded elsewhere or unrecorded, nor the Visconti-Sforza cards
scanned from the Dal Negro reproduction; a withheld card links to its holder. Waite's trump meanings
and Celtic Cross come from research/sources/waite-pictorial-key-part-iii.md (Part III, 1911, PD).

The sitemap's <lastmod> is honest: data/sitemap-lastmod.json stores a hash of each listed page and
a date that moves to today only when the page's bytes change. --check fails on a stale generated
page and only warns when a hand-edited page in STATIC_PAGES changed since its date was set.
"""
import datetime
import hashlib
import html
import json
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://tarot.recursive.eco/"
OUT_DIR = "card"
HUB = "tarot-card-meanings.html"
LASTMOD = os.path.join("data", "sitemap-lastmod.json")
WAITE = "rider-waite-smith-pictorial-key"
BOOKT = "golden-dawn-book-t-tarot"

# Hand-edited pages with real text in their HTML (path -> priority). Viewers that need a query
# string, the course viewer, and pages marked noindex (manifesto, wishlist) are left out.
STATIC_PAGES = {
    "index.html": "1.0",
    "genealogy.html": "0.7",
    "pages/about.html": "0.6",
    "pages/historian.html": "0.7",
    "pages/play.html": "0.7",
    "pages/courses.html": "0.6",
    "pages/glossary.html": "0.7",
    "pages/book-t.html": "0.8",
    "pages/book-of-fate-1822.html": "0.6",
    "pages/tree-of-life.html": "0.6",
    "pages/golden-dawn-decks.html": "0.6",
    "pages/sources.html": "0.5",
    "pages/channels.html": "0.5",
    "pages/contribute.html": "0.5",
    "pages/games/trionfi.html": "0.5",
    "pages/games/tarocchino.html": "0.5",
    "pages/games/madiao.html": "0.5",
}
GROUPS = [
    ("major-arcana", "The Major Arcana"),
    ("suit-wands", "Wands"),
    ("suit-cups", "Cups"),
    ("suit-swords", "Swords"),
    ("suit-pentacles", "Pentacles"),
]
BOOKT_SECTIONS = ["Golden Dawn Title", "Golden Dawn Rank", "Book T (1912)", "Correspondences",
                  "Astrological attribution (Book T)"]
CREED = ("Read to know yourself, not to surrender yourself: relate to the card; never obey it. "
         "These are what two traditions wrote, not predictions.")


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    """Escape for text and double-quoted attributes; apostrophes stay readable in titles and snippets."""
    return html.escape(s or "", quote=False).replace('"', "&quot;")


def inline_md(s):
    """The little Markdown the grammars use: [text](url), **bold**, *italic*. Input is escaped first."""
    s = esc(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    return s


def md_paras(text):
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text or "") if b.strip()]
    return "".join(f"<p>{inline_md(b).replace(chr(10), '<br>')}</p>" for b in blocks)


def clip(s, n):
    s = re.sub(r"\s+", " ", s or "").strip()
    if len(s) <= n:
        return s
    return s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"


def plain_name(name):
    return re.sub(r"^\s*\d+\s*[—-]\s*", "", name).strip()


# Commons file names that are redirects: a thumbnail path is built from the real file's name.
# Checked Oct 14 2026 with the Commons API (prop=imageinfo&iiurlwidth=330) for all 78 cards.
COMMONS_REDIRECTS = {"Tarot_Nine_of_Wands.jpg": "Wands09.jpg"}


def commons_thumb(file_url, width):
    """Special:FilePath/<file> -> the upload.wikimedia.org thumbnail of that width (no redirect hop)."""
    fname = urllib.parse.unquote(file_url.rsplit("/", 1)[-1]).replace(" ", "_")
    fname = COMMONS_REDIRECTS.get(fname, fname)
    h = hashlib.md5(fname.encode("utf-8")).hexdigest()
    q = urllib.parse.quote(fname)
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{width}px-{q}"


def split_waite(text):
    """Waite's minor-card text -> (description, upright, reversed). Majors carry no meanings here."""
    t = re.sub(r"^\s*[A-Z][^.\n]{0,40}\n\s*\n", "", text or "", count=1)  # a repeated heading line ("The Fool", "Queen")
    m = re.search(r"\bDivinatory Meanings?\s*:\s*", t)
    if not m:
        return t.strip(), "", ""
    desc, rest = t[: m.start()].strip(), t[m.end():]
    r = re.search(r"\bReversed\s*:\s*", rest)
    if not r:
        return desc, rest.strip(), ""
    return desc, rest[: r.start()].strip(), rest[r.end():].strip()


def bookt_meaning(sec):
    """Book T's own text minus its italic provenance line."""
    lines = [b for b in re.split(r"\n\s*\n", sec or "") if b.strip()]
    if lines and lines[0].strip().startswith("*Book T in its own words"):
        lines = lines[1:]
    return "\n\n".join(lines).strip()


CSS = """
html,body{margin:0;background:var(--bg);color:var(--ink);color-scheme:light;font-family:var(--sans);line-height:1.6}
.wrap{max-width:900px;margin:0 auto;padding:18px 16px 70px}
.crumbs{font-size:13px;color:var(--muted);margin:4px 0 14px}
.crumbs a{color:var(--muted)}
.kicker{font-size:11px;text-transform:uppercase;letter-spacing:.16em;color:var(--muted);margin:0}
h1{font-family:var(--serif-display);font-weight:600;font-size:31px;line-height:1.2;margin:6px 0 8px}
h2{font-family:var(--serif-display);font-weight:600;font-size:21px;margin:30px 0 8px;border-top:1px solid var(--line);padding-top:18px}
h3{font-family:var(--serif-display);font-weight:600;font-size:17px;margin:18px 0 4px}
.head{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:24px;align-items:start}
@media (max-width:640px){.head{grid-template-columns:1fr}}
.head figure{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:8px}
.head img{display:block;width:100%;height:auto;max-height:520px;object-fit:contain;background:var(--chip)}
.head figcaption{font-size:12px;color:var(--muted);margin-top:6px}
.meanings{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0}
@media (max-width:480px){.meanings{grid-template-columns:1fr}}
.meanings div{background:var(--surface);border:1px solid var(--line);border-radius:4px;padding:10px 12px}
.meanings b{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:600}
.prose{font-family:var(--serif-body);font-size:16.5px;line-height:1.7}
.prose p{margin:8px 0}
.src{font-size:12.5px;color:var(--muted);margin:4px 0 0}
.creed{font-family:var(--serif-body);font-style:italic;color:var(--ink-soft);margin:14px 0 0;font-size:15px}
.actions{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 4px}
.btn{display:inline-block;padding:8px 14px;border-radius:3px;border:1px solid var(--gold);color:var(--gold);text-decoration:none;font-size:14px;background:var(--surface)}
.btn.primary{background:var(--gold);color:#fff}
.pn{display:flex;justify-content:space-between;gap:10px;margin:34px 0 0;font-size:14.5px;border-top:1px solid var(--line);padding-top:14px}
.pn a{color:var(--ink)}
.fine{font-size:12.5px;color:var(--muted);margin-top:26px;line-height:1.55}
.fine a{color:var(--muted)}
a{color:var(--gold)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:12px;margin:12px 0;padding:0;list-style:none}
.grid a{display:block;text-decoration:none;color:var(--ink);font-size:13px;line-height:1.3;text-align:center}
.grid img{display:block;width:100%;height:auto;aspect-ratio:3/5;object-fit:contain;background:var(--chip);border:1px solid var(--line);border-radius:3px;margin-bottom:4px}
.grid a:hover{color:var(--gold)}
"""


def page(title, desc, canonical, og_image, ldjson, body, pfx, og_type="article", active="cards"):
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, separators=(",", ":"))}</script>'
        for x in ldjson)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="The Recursive Tarot">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary">
<link rel="icon" type="image/svg+xml" href="{pfx}public/favicon.svg?v=2">
<link rel="stylesheet" href="{pfx}theme.css?v=3">
<style>{CSS}</style>
{ld}
</head>
<body>
<!-- Generated by scripts/build_card_pages.py: edit the grammars and re-run, never this file. -->
<script src="{pfx}site-header.js?v=52"></script>
<site-header active="{active}"></site-header>
<main class="wrap">
{body}
</main>
<script src="{pfx}site-footer.js?v=1"></script>
<site-footer></site-footer>
</body>
</html>
"""


PICTORIAL_KEY = {
    "@type": "Book",
    "name": "The Pictorial Key to the Tarot",
    "author": {"@type": "Person", "name": "Arthur Edward Waite"},
    "illustrator": {"@type": "Person", "name": "Pamela Colman Smith"},
    "datePublished": "1911",
    "publisher": {"@type": "Organization", "name": "William Rider & Son"},
    "inLanguage": "en",
    "license": "https://creativecommons.org/publicdomain/mark/1.0/",
}


def build():
    trumps = waite_trumps()
    waite = load(f"tarot/{WAITE}/grammar.json")["nodes"]
    bt = {n["metadata"]["archetype"]: n for n in load(f"tarot/{BOOKT}/grammar.json")["nodes"]
          if (n.get("metadata") or {}).get("archetype")}
    cards = []
    for n in waite:
        meta = n.get("metadata") or {}
        arch = meta.get("archetype", "")
        slug = re.sub(r"[^a-z0-9]+", "-", plain_name(n["name"]).lower()).strip("-")  # the deck's own words: pentacles, not coins
        ill = next((i for i in meta.get("illustrations", []) if i.get("is_primary")), (meta.get("illustrations") or [{}])[0])
        cards.append({"node": n, "meta": meta, "slug": slug, "name": plain_name(n["name"]),
                      "group": n.get("category"), "book_t": bt.get(arch), "img": ill.get("url", "")})
    if len(cards) != 78 or len({c["slug"] for c in cards}) != 78:
        sys.exit("expected 78 cards with unique archetype slugs")

    def url(c):
        return f"{SITE}{OUT_DIR}/{c['slug']}.html"

    files = {}
    for idx, c in enumerate(cards):
        n, meta = c["node"], c["meta"]
        major = meta.get("arcana") == "major"
        desc_w, up, rev = split_waite(n["sections"].get("The Pictorial Key", ""))
        if major and not up and meta.get("number") in trumps:
            up, rev = trumps[meta.get("number")]["up"], trumps[meta.get("number")]["rev"]
        b = c["book_t"]["sections"] if c["book_t"] else {}
        bt_text = bookt_meaning(b.get("Book T (1912)", ""))
        gd_title = re.sub(r"^\*Book T[^\n]*\n\s*\n", "", b.get("Golden Dawn Title", "")).strip().strip("*")
        title = f"{c['name']} Tarot Card Meaning in Waite's Own Words (1911)"
        if len(title) + len(" · Recursive Tarot") <= 70:
            title += " · Recursive Tarot"
        if up:
            d = f"{c['name']} tarot card meaning in Waite's words: upright, {up.rstrip('.')}; reversed, {rev.rstrip('.') or 'none given'}."
        else:
            d = f"{c['name']} tarot card: Waite's 1911 description, and the Golden Dawn's Book T: {bt_text}"
        desc = clip(d, 158)
        kicker = (f"Major Arcana · Key {meta.get('number')}" if major
                  else f"Minor Arcana · {meta.get('suit')} · {meta.get('element', '')}").rstrip(" ·")
        thumb = commons_thumb(c["img"], 330)
        thumb2 = commons_thumb(c["img"], 500)
        meanings = (f'<div class="meanings"><div><b>Upright</b>{esc(up)}</div><div><b>Reversed</b>{esc(rev or "Waite gives none.")}</div></div>'
                    if up else "")
        bt_html = ""
        if c["book_t"]:
            parts = []
            if gd_title:
                parts.append(f'<p class="prose"><i>{esc(gd_title)}</i></p>')
            if bt_text:
                parts.append(f'<div class="prose">{md_paras(bt_text)}</div>')
            for key in ("Golden Dawn Rank", "Correspondences", "Astrological attribution (Book T)"):
                if b.get(key):
                    parts.append(f'<h3>{esc(key)}</h3><div class="prose">{md_paras(b[key])}</div>')
            bt_html = (f'<h2 id="book-t">In the Golden Dawn\'s Book T (1912)</h2>{"".join(parts)}'
                       '<p class="src">Book T as printed in <cite>The Equinox</cite> I(8), 1912, public domain (notes in square brackets are '
                       'Crowley\'s). The correspondences are this site\'s compilation from Book T. '
                       f'<a href="../viewers/cards.html?src=../tarot/{BOOKT}/grammar.json&amp;item={esc(c["book_t"]["id"])}">Open it in the Golden Dawn deck</a>.</p>')
        prev_c, next_c = cards[idx - 1], cards[(idx + 1) % 78]
        body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">The Recursive Tarot</a> › <a href="../{HUB}">Tarot card meanings</a> › {esc(c['name'])}</nav>
<article>
<div class="head">
<figure><img src="{thumb}" srcset="{thumb} 330w, {thumb2} 500w" sizes="(max-width:640px) 90vw, 300px" width="330" height="565" alt="{esc(c['name'])}, the Rider-Waite-Smith card drawn by Pamela Colman Smith (1909)" fetchpriority="high">
<figcaption>Pamela Colman Smith, Rider-Waite-Smith deck (1909). Public domain, via <a href="{esc(c['img'])}">Wikimedia Commons</a>.</figcaption></figure>
<div>
<p class="kicker">{esc(kicker)}</p>
<h1>{esc(c['name'])}</h1>
{meanings}
<p class="creed">{esc(CREED)}</p>
<div class="actions">
<a class="btn primary" href="../viewers/caster-studio.html">Draw &amp; reflect</a>
<a class="btn" href="../viewers/cards.html?src=../tarot/{WAITE}/grammar.json&amp;item={esc(n['id'])}">Open in the card viewer</a>
</div>
</div>
</div>
<h2 id="waite">In Waite's words: <cite>The Pictorial Key to the Tarot</cite> (1911)</h2>
<div class="prose">{md_paras(desc_w) if desc_w else ''}</div>
{'' if not major else ('<p class="src">The upright and reversed meanings above are from Waite\'s own list of the trumps\' divinatory meanings, Part III §3 of the same book; see them all, with his Celtic Cross, on <a href="../' + SPREADS + '">Tarot spreads</a>.</p>' if up else '<p class="src">For the trumps, Waite gives his divinatory meanings in a separate list in Part III of the book; they are not carried here yet.</p>')}
<p class="src">A. E. Waite, <cite>The Pictorial Key to the Tarot</cite> (London: William Rider &amp; Son, 1911), public domain.</p>
{bt_html}
</article>
<nav class="pn" aria-label="Previous and next card">
<a href="{prev_c['slug']}.html" rel="prev">← {esc(prev_c['name'])}</a>
<a href="../{HUB}">All 78</a>
<a href="{next_c['slug']}.html" rel="next">{esc(next_c['name'])} →</a>
</nav>
<p class="fine">Images: Pamela Colman Smith (1878–1951), public domain. Texts: Waite (1911) and Book T (1912), public domain.
Selection and arrangement CC-BY-SA-4.0 (PlayfulProcess). Data: <a href="https://github.com/PlayfulProcess/recursive-tarot">github.com/PlayfulProcess/recursive-tarot</a>.</p>"""
        canonical = url(c)
        ld = [
            {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": title,
                "description": desc,
                "url": canonical,
                "inLanguage": "en",
                "isPartOf": {"@type": "WebSite", "name": "The Recursive Tarot", "url": SITE},
                "primaryImageOfPage": {"@type": "ImageObject", "contentUrl": thumb2, "creator": {"@type": "Person", "name": "Pamela Colman Smith"},
                                       "license": "https://creativecommons.org/publicdomain/mark/1.0/"},
                "mainEntity": {"@type": "Chapter", "name": c["name"], "isPartOf": PICTORIAL_KEY},
                "license": "https://creativecommons.org/licenses/by-sa/4.0/",
            },
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "The Recursive Tarot", "item": SITE},
                    {"@type": "ListItem", "position": 2, "name": "Tarot card meanings", "item": SITE + HUB},
                    {"@type": "ListItem", "position": 3, "name": c["name"], "item": canonical},
                ],
            },
        ]
        files[f"{OUT_DIR}/{c['slug']}.html"] = page(title, desc, canonical, thumb2, ld, body, "../")

    sections = []
    for key, label in GROUPS:
        items = "".join(
            f'<li><a href="{OUT_DIR}/{c["slug"]}.html"><img src="{commons_thumb(c["img"], 250)}" alt="" loading="lazy" width="250" height="428">{esc(c["name"])}</a></li>'
            for c in cards if c["group"] == key)
        sections.append(f'<h2 id="{key}">{label}</h2><ul class="grid">{items}</ul>')
    hub_title = "Tarot Card Meanings: all 78 cards in Waite's own words (1911)"
    hub_desc = ("All 78 Rider-Waite-Smith tarot cards, one page each: A. E. Waite's own 1911 text, upright and reversed, "
                "Pamela Colman Smith's card, and the Golden Dawn's Book T. Free, no ads.")
    hub_body = f"""<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">The Recursive Tarot</a> › Tarot card meanings</nav>
<p class="kicker">Rider-Waite-Smith · 1909 / 1911</p>
<h1>Tarot card meanings, in the words of the people who made the deck</h1>
<p class="prose">The deck most people mean by "tarot" was drawn by Pamela Colman Smith and published in 1909 to a
programme set by A. E. Waite, who explained it in <cite>The Pictorial Key to the Tarot</cite> (1911). Each card below has
its own page with Waite's text, his upright and reversed meanings for the minor cards, and what the Golden Dawn's Book T
(printed 1912), the system behind the imagery, says of the same card. Two traditions, each in its own words.</p>
<p class="creed">{esc(CREED)}</p>
<div class="actions"><a class="btn primary" href="viewers/caster-studio.html">Draw &amp; reflect</a>
<a class="btn" href="genealogy.html">Where the cards came from</a></div>
{''.join(sections)}
<p class="fine">Images: Pamela Colman Smith, public domain, via Wikimedia Commons. Texts: Waite (1911) and Book T (1912),
public domain. Selection and arrangement CC-BY-SA-4.0 (PlayfulProcess).</p>"""
    hub_ld = [
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": hub_title,
            "description": hub_desc,
            "url": SITE + HUB,
            "isPartOf": {"@type": "WebSite", "name": "The Recursive Tarot", "url": SITE},
            "about": PICTORIAL_KEY,
            "mainEntity": {"@type": "ItemList", "numberOfItems": 78, "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": url(c), "name": c["name"]} for i, c in enumerate(cards)]},
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "The Recursive Tarot", "item": SITE},
                {"@type": "ListItem", "position": 2, "name": "Tarot card meanings", "item": SITE + HUB},
            ],
        },
    ]
    files[HUB] = page(hub_title, hub_desc, SITE + HUB, commons_thumb(cards[0]["img"], 500), hub_ld, hub_body, "", "website")
    order = [f"{OUT_DIR}/{c['slug']}.html" for c in cards]
    card_url = {c["node"]["metadata"].get("number"): f"{OUT_DIR}/{c['slug']}.html" for c in cards if c["meta"].get("arcana") == "major"}
    more = []  # (path, priority) for the sitemap, after the 78 card pages
    more += build_book_t(files)
    more += build_decks(files)
    more += build_spreads(files, trumps, card_url)
    return files, order, more


# ─────────────────────────────────────────────────────────────────────────────────────────────
# Oct 20 2026: Book T card pages, historical deck pages, the spreads page (see the docstring).
# ─────────────────────────────────────────────────────────────────────────────────────────────
BT_DECK = "book-t"                      # tarot/book-t, Book T's own deck (scripts/build_book_t_deck.py)
BT_DIR = "book-t"                       # its static pages (outside tarot/: recursive.eco never reads them)
DECK_DIR = "deck"
SPREADS = "spreads.html"
ECO_IDS = "tarot/_eco_ids.json"
LEDGER = "docs/rights/image-ledger.json"
WAITE_III = "research/sources/waite-pictorial-key-part-iii.md"
PLAY = "https://recursive.eco/play?id="
CAST = "https://recursive.eco/process?cast="  # the Cast link the site uses (viewers/cards.html, PR #85)
GITHUB = "https://github.com/PlayfulProcess/recursive-tarot/blob/main/"
DRAFT = "<!-- DRAFT copy for PlayfulProcess: new wording, not taken from a grammar. -->"
# recursive.eco ids confirmed public with the MCP on Oct 20 2026 that are missing from _eco_ids.json's
# (June) _public_now list. The four one-card overview grammars (cary-sheet, rosenwald-sheet,
# noblet-tarot, ganjifa) were private then, so their pages carry no Play link.
ECO_PUBLIC_EXTRA = {"book-t"}
# Decks with their own static pages already, so no deck page: Book T (book-t/) and the
# Rider-Waite-Smith deck (card/ + tarot-card-meanings.html).
DECK_SKIP = {BT_DECK, WAITE}
SHOWN_CLASSES = {"commons-pd-tag", "commons-cc-by-sa-4.0"}
WITHHELD_DECKS = {  # deck -> why, and where the cards are instead (the holder)
    "charles-vi-tarot": ("BnF scans, free for non-commercial reuse only",
                         "Bibliothèque nationale de France", "http://expositions.bnf.fr/renais/arret/3/index.htm"),
    "este-tarot": ("Yale's terms for these scans are not yet confirmed",
                   "Beinecke Library, Yale (PLAYING CARDS GEN 966)",
                   "https://collections.library.yale.edu/catalog?search_field=all_fields&q=PLAYING+CARDS+GEN+966"),
}
HOLDERS = {  # deck -> (holder, URL) for a card withheld card by card
    "visconti-sforza-tarot": ("The Morgan Library & Museum (MS M.630)", "https://www.themorgan.org/manuscript/158525"),
    "rosenwald-sheet": ("National Gallery of Art, Washington", "https://www.nga.gov/"),
}
NONCARD = {"keyword-emergence", "emergence", "axis", "overview", "chapter", "suit"}
# Waite Part III as lifted from the grammar (research/sources/...): plain transcription slips fixed
# against the 1911 text, each listed here and nowhere else.
WAITE_FIXES = [
    ("deception, min.", "deception, ruin."),
    ("abuse if power", "abuse of power"),
    ("First Cardbeing", "First Card— being"),
    ("latent or developedand", "latent or developed— and"),
    ("N.B .-", "N.B.—"),
    ("person or, matter", "person or matter"),
]


def waite_text():
    t = read(WAITE_III) or ""
    for a, b in WAITE_FIXES:
        t = t.replace(a, b)
    return t


def waite_trumps():
    """Waite's divinatory meanings of the 22 trumps (Part III §3) -> {number: {name, up, rev}}."""
    out = {}
    for line in waite_text().splitlines():
        m = re.match(r"^(ZERO|\d{1,2})\.\s+([A-Z][A-Z ]+?)\.?\s*(?:—|-)\s*(.+)$", line.strip())
        if not m or "Reversed" not in m.group(3):
            continue
        num = 0 if m.group(1) == "ZERO" else int(m.group(1))
        up, rev = re.split(r"\bReversed\s*:\s*", m.group(3), maxsplit=1)
        out.setdefault(num, {"name": m.group(2).title().replace("Of ", "of "), "up": up.strip().rstrip(".") + ".",
                             "rev": rev.strip()})
    if sorted(out) != list(range(22)):
        sys.exit(f"Waite's trump meanings: expected 0-21, found {sorted(out)}")
    return out


def waite_celtic():
    """Waite's 'An Ancient Celtic Method of Divination' -> (paragraphs, the ten positions)."""
    t = waite_text()
    a = t.index("AN ANCIENT CELTIC METHOD OF DIVINATION")
    b = t.index("3.8 An Alternative Method of Reading")
    paras, positions = [], []
    for block in re.split(r"\n\s*\n", t[a:b]):
        s = block.strip()
        if not s or s.startswith("AN ANCIENT CELTIC") or re.match(r"^3\.7 ", s) or s == "! J ro":
            continue
        m = re.match(r"^(\d{1,2})\s*\.\s+(.+)$", s)
        if m and len(s) < 40:
            positions.append((int(m.group(1)), m.group(2).rstrip(".")))
        elif s == "The Significator.":
            continue
        else:
            paras.append(s)
    if [p[0] for p in positions] != list(range(1, 11)):
        sys.exit(f"Waite's Celtic Cross: expected positions 1-10, found {positions}")
    return paras, positions


def md_blocks(text, skip_h1=True):
    """A grammar description's Markdown: headings, lists, quotes, paragraphs (soft-wrapped lines)."""
    out, para, lst, quote = [], [], [], []

    def flush():
        if para:
            out.append(f"<p>{inline_md(' '.join(para))}</p>")
        if lst:
            out.append("<ul>" + "".join(f"<li>{inline_md(x)}</li>" for x in lst) + "</ul>")
        if quote:
            out.append(f"<blockquote>{md_paras(chr(10).join(quote))}</blockquote>")
        para.clear(), lst.clear(), quote.clear()

    first = True
    for line in re.sub(r"\s?\[@[^\]]+\]", "", text or "").splitlines():
        s = line.strip()
        if not s:
            flush()
            continue
        h = re.match(r"^(#{1,6})\s+(.*)$", s)
        if h:
            flush()
            if not (first and skip_h1 and len(h.group(1)) == 1):
                out.append(f"<h{2 if len(h.group(1)) <= 2 else 3}>{inline_md(h.group(2))}</h{2 if len(h.group(1)) <= 2 else 3}>")
        elif re.match(r"^[-*]\s+", s):
            if para or quote:
                flush()
            lst.append(re.sub(r"^[-*]\s+", "", s))
        elif s.startswith(">"):
            if para or lst:
                flush()
            quote.append(s.lstrip("> "))
        elif lst and line.startswith((" ", "\t")):
            lst[-1] += " " + s
        else:
            if lst or quote:
                flush()
            para.append(s)
        first = False
    flush()
    return "".join(out)


def plain(md):
    """Markdown -> one line of plain text (for meta descriptions)."""
    s = re.sub(r"\s?\[@[^\]]+\]", "", md or "")
    s = re.sub(r"^#+\s.*$", "", s, flags=re.M)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"[*_`>]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def ascii_slug(s, words=7):
    s = re.split(r"[:;,]", s)[0]
    w = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-").split("-")
    return "-".join(x for x in w[:words] if x)


def crumbs(items):
    """[(name, href or None)] -> the breadcrumb nav."""
    return ('<nav class="crumbs" aria-label="Breadcrumb">'
            + " › ".join(f'<a href="{h}">{esc(n)}</a>' if h else esc(n) for n, h in items) + "</nav>")


def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def site_title(t):
    return t + " · Recursive Tarot" if len(t) + len(" · Recursive Tarot") <= 70 else t


EXTRA_CSS = """
.sets{display:flex;flex-wrap:wrap;gap:12px;margin:10px 0;padding:0;list-style:none}
.sets li{width:150px;font-size:12px;color:var(--muted);line-height:1.35}
.sets img{display:block;width:150px;height:250px;object-fit:contain;background:var(--chip);border:1px solid var(--line);border-radius:3px;margin-bottom:4px}
table.dt{border-collapse:collapse;width:100%;font-size:14.5px;margin:12px 0}
table.dt th,table.dt td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
table.dt th{font-size:11px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);font-weight:600}
table.dt tr.sign td{background:var(--surface);font-family:var(--serif-display);font-weight:600}
.grid .off{display:flex;align-items:center;justify-content:center;aspect-ratio:3/5;background:var(--chip);border:1px dashed var(--line);border-radius:3px;margin-bottom:4px;font-size:11px;color:var(--muted);padding:6px;text-align:center}
.prose h2{font-size:19px}.prose ul{margin:8px 0 8px 20px;padding:0}.prose blockquote{margin:10px 0;padding-left:12px;border-left:3px solid var(--line)}
ol.positions{font-family:var(--serif-body);font-size:16px}
"""


def page2(title, desc, canonical, og_image, ld, body, pfx, og_type="article", active="cards"):
    return page(title, desc, canonical, og_image, ld, body, pfx, og_type, active).replace(
        f"<style>{CSS}</style>", f"<style>{CSS}{EXTRA_CSS}</style>", 1)


def eco_public():
    ids = load(ECO_IDS)
    return ids.get("ids", {}), set(ids.get("_public_now", [])) | ECO_PUBLIC_EXTRA


# ── Book T: one page per card, the decans, an index ─────────────────────────────────────────
def build_book_t(files):
    g = load(f"tarot/{BT_DECK}/grammar.json")
    ids, public = eco_public()
    eco = ids.get(BT_DECK) if BT_DECK in public else None
    nodes = {n["id"]: n for n in g["nodes"]}
    chapters = [n for n in g["nodes"] if n.get("category") == "chapter"]
    cards = [n for n in g["nodes"] if n.get("category") != "chapter"]
    cards.sort(key=lambda n: n["metadata"]["book_t_no"])
    if len(cards) != 78:
        sys.exit(f"Book T: expected 78 cards, found {len(cards)}")

    def fname(n):
        return f"{n['id']}.html" if n.get("category") == "keys" else f"{n['id']}-{ascii_slug(n['name'])}.html"

    def label(n):
        m = n["metadata"]
        if n.get("category") == "keys":
            return f"{m['card_name_1912']} (Key {m['key_number']})"
        return m["card_name_1912"]

    hub_url = f"{SITE}{BT_DIR}/index.html"
    out = []
    for i, n in enumerate(cards):
        m, sec = n["metadata"], n.get("sections", {})
        cat = n.get("category")
        url = f"{SITE}{BT_DIR}/{fname(n)}"
        if cat == "keys":
            title = f"{m['card_name_1912']}, Key {m['key_number']}: {n['name']} · Book T (1912)"
            kicker = f"Book T no. {m['book_t_no']} · Key {m['key_number']} · Hebrew letter {m['hebrew_translit']} · Path {m['tree_path']}"
        elif cat == "decans":
            title = f"{n['name']}: the {m['card_name_1912']} in Book T (1912)"
            kicker = f"Book T no. {m['book_t_no']} · {m['card_name_1912']} · decan: {m['decan']}"
        elif cat == "courts":
            title = f"{n['name'].split(':')[0]}: the {m['card_name_1912']} in Book T (1912)"
            kicker = f"Book T no. {m['book_t_no']} · {m['card_name_1912']} · {m['element_in_element']}"
        else:
            title = f"{n['name']}: the {m['card_name_1912']} in Book T (1912)"
            kicker = f"Book T no. {m['book_t_no']} · {m['card_name_1912']} · {m.get('element', '')}"
        title = site_title(title)
        bt = bookt_meaning(sec.get("Book T (1912)", ""))
        desc = clip(f"{n['name']} ({m['card_name_1912']}), Book T, the Golden Dawn's book of the tarot (1912): {plain(bt)}", 158)
        ills = m.get("illustrations") or []
        prim = next((x for x in ills if x.get("is_primary")), ills[0] if ills else {})
        og = next((x["url"] for x in ills if x.get("url", "").endswith((".png", ".jpg"))), prim.get("url") or "")
        sets = "".join(
            f'<li><a href="{esc(x["url"])}"><img src="{esc(x["url"])}" alt="{esc(n["name"])}, {esc(x.get("edition", ""))}" loading="lazy" width="150" height="250"></a>'
            f'{esc(x.get("edition", ""))}. {esc(x.get("artist", ""))}. {esc(x.get("license", ""))}.</li>'
            for x in ills if x is not prim)
        parts = []
        for key in sec:
            if key == "Book T (1912)":
                continue
            parts.append(f'<h2>{esc(key)}</h2><div class="prose">{md_paras(sec[key])}</div>')
        play = (f'<a class="btn" href="{PLAY}{eco}&amp;node={esc(n["id"])}">Play it on recursive.eco</a>' if eco else "")
        cast = (f'<a class="btn primary" href="{CAST}{eco}">Draw &amp; reflect</a>' if eco else
                f'<a class="btn primary" href="../viewers/caster-studio.html?src=../tarot/{BOOKT}/grammar.json">Draw &amp; reflect</a>')
        prev_n, next_n = cards[i - 1], cards[(i + 1) % 78]
        body = f"""{crumbs([("The Recursive Tarot", "../index.html"), ("Book T", "index.html"), (n['name'], None)])}
<article>
<div class="head">
<figure><img src="{esc(prim.get('url', ''))}" alt="{esc(n['name'])}, {esc(label(n))}: {esc(prim.get('edition', ''))}" width="300" height="500" fetchpriority="high">
<figcaption>{esc(prim.get('edition', ''))}. {esc(prim.get('artist', ''))}. {esc(prim.get('license', ''))}.</figcaption></figure>
<div>
<p class="kicker">{esc(kicker)}</p>
<h1>{esc(n['name'])}</h1>
<p class="src">{esc(label(n))} · <i>{esc(m.get('title', ''))}</i></p>
<p class="creed">{esc(CREED.split(" These")[0])}</p>
<div class="actions">
{cast}
{play}
<a class="btn" href="../viewers/cards.html?src=../tarot/{BT_DECK}/grammar.json&amp;item={esc(n['id'])}">Open in the card viewer</a>
</div>
</div>
</div>
<h2 id="book-t">Book T (1912)</h2>
<div class="prose">{md_paras(bt)}</div>
<p class="src">Book T as printed in <cite>The Equinox</cite> I(8), 1912, public domain (notes in square brackets are Crowley's).</p>
{''.join(parts)}
{('<h2 id="pictures">Picture sets</h2><ul class="sets">' + sets + '</ul>') if sets else ''}
</article>
<nav class="pn" aria-label="Previous and next card">
<a href="{fname(prev_n)}" rel="prev">← {esc(prev_n['name'])}</a>
<a href="index.html">All 78</a>
<a href="{fname(next_n)}" rel="next">{esc(next_n['name'])} →</a>
</nav>
<p class="fine">Text: Book T (1912), Waite (1911) and Case (1920), public domain. Pictures and arrangement CC-BY-SA-4.0 (PlayfulProcess).
Data: <a href="{GITHUB}tarot/{BT_DECK}/grammar.json">tarot/{BT_DECK}/grammar.json</a>.</p>"""
        ld = [{
            "@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": url,
            "inLanguage": "en", "isPartOf": {"@type": "WebSite", "name": "The Recursive Tarot", "url": SITE},
            "primaryImageOfPage": {"@type": "ImageObject", "contentUrl": prim.get("url", ""),
                                   "license": "https://creativecommons.org/licenses/by-sa/4.0/"},
            "mainEntity": {"@type": "Chapter", "name": n["name"], "alternateName": label(n), "isPartOf": BOOK_T_1912},
            "license": "https://creativecommons.org/licenses/by-sa/4.0/",
        }, breadcrumb_ld([("The Recursive Tarot", SITE), ("Book T", hub_url), (n["name"], url)])]
        files[f"{BT_DIR}/{fname(n)}"] = page2(title, desc, url, og, ld, body, "../")
        out.append((f"{BT_DIR}/{fname(n)}", "0.6"))

    # the decans: 36 small cards in Book T's order (from Leo), three to a sign
    dec_ch = next(c for c in chapters if c["id"] == "bt-decans")
    decans = [nodes[p] for p in dec_ch["parts"]]
    rows, sign = [], None
    for j, n in enumerate(decans):
        m = n["metadata"]
        if m["sign"] != sign:
            sign = m["sign"]
            rows.append(f'<tr class="sign"><td colspan="4">{esc(sign)}</td></tr>')
        rows.append(f'<tr><td>{["1st", "2nd", "3rd"][j % 3]}</td><td>{esc(m["planet"])} in {esc(m["sign"])}</td>'
                    f'<td><a href="{fname(n)}">{esc(n["name"])}</a> · {esc(m["card_name_1912"])}</td><td>{esc(m.get("sephirah", ""))}</td></tr>')
    d_title = "The 36 Decans and the Tarot: Book T's small cards (1912)"
    d_desc = ("The 36 decans of the zodiac and the 36 small cards of the Golden Dawn's Book T (1912): "
              "each decan's planet and sign, its card and its Book T title, from Leo onward.")
    d_url = f"{SITE}{BT_DIR}/decans.html"
    d_body = f"""{crumbs([("The Recursive Tarot", "../index.html"), ("Book T", "index.html"), ("The decans", None)])}
<p class="kicker">Book T · 1912 · the thirty-six small cards</p>
<h1>The decans: thirty-six small cards</h1>
<div class="prose">{md_paras(dec_ch['sections'].get('About', ''))}</div>
<table class="dt"><thead><tr><th>Decan</th><th>Planet in sign</th><th>Card</th><th>Sephirah</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
{DRAFT}
<p class="src">Planets, signs and cards as Book T sets them (<cite>The Equinox</cite> I(8), 1912, public domain); the table is this site's arrangement of the deck's metadata.</p>
<p class="fine">Data: <a href="{GITHUB}tarot/{BT_DECK}/grammar.json">tarot/{BT_DECK}/grammar.json</a>. CC-BY-SA-4.0 (PlayfulProcess).</p>"""
    d_ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": d_title, "description": d_desc, "url": d_url,
             "inLanguage": "en", "isPartOf": {"@type": "WebSite", "name": "The Recursive Tarot", "url": SITE},
             "about": BOOK_T_1912,
             "mainEntity": {"@type": "ItemList", "numberOfItems": 36, "itemListElement": [
                 {"@type": "ListItem", "position": j + 1, "name": f"{n['metadata']['decan']}: {n['name']}",
                  "url": f"{SITE}{BT_DIR}/{fname(n)}"} for j, n in enumerate(decans)]}},
            breadcrumb_ld([("The Recursive Tarot", SITE), ("Book T", hub_url), ("The decans", d_url)])]
    files[f"{BT_DIR}/decans.html"] = page2(d_title, d_desc, d_url, cards[0]["metadata"]["illustrations"][0]["url"], d_ld, d_body, "../")

    # index: the four chapters in Book T's order
    secs = []
    for ch in sorted(chapters, key=lambda c: nodes[c["parts"][0]]["metadata"]["book_t_no"]):
        items = "".join(
            f'<li><a href="{fname(nodes[p])}"><img src="{esc(((nodes[p]["metadata"].get("illustrations") or [{}])[0]).get("url", ""))}" alt="" loading="lazy" width="250" height="416">{esc(nodes[p]["name"])}</a></li>'
            for p in ch["parts"])
        extra = ' <a href="decans.html">The decans as a table →</a>' if ch["id"] == "bt-decans" else ""
        secs.append(f'<h2 id="{esc(ch["id"])}">{esc(ch["name"])}</h2><div class="prose">{md_paras(ch["sections"].get("About", ""))}</div>'
                    f'<p class="src">{extra}</p><ul class="grid">{items}</ul>')
    h_title = "Book T: the Golden Dawn's 78 tarot cards, one page each (1912)"
    h_desc = clip(plain(g.get("description", "").split("## ")[0]), 158)
    h_body = f"""{crumbs([("The Recursive Tarot", "../index.html"), ("Book T", None)])}
<p class="kicker">Book T · c. 1888 · printed 1912</p>
<h1>{esc(g['name'])}</h1>
<div class="prose">{md_blocks(g.get('description', '').split('## ')[0])}</div>
<div class="actions"><a class="btn primary" href="../pages/book-t.html">Read the whole 1912 text</a>
<a class="btn" href="decans.html">The 36 decans</a>
{f'<a class="btn" href="{PLAY}{eco}&amp;pane=cards">Play it on recursive.eco</a>' if eco else ''}</div>
{''.join(secs)}
<p class="fine">Text: Book T (1912), public domain. Pictures and arrangement CC-BY-SA-4.0 (PlayfulProcess).
Data: <a href="{GITHUB}tarot/{BT_DECK}/grammar.json">tarot/{BT_DECK}/grammar.json</a>.</p>"""
    h_ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": h_title, "description": h_desc,
             "url": hub_url, "inLanguage": "en", "isPartOf": {"@type": "WebSite", "name": "The Recursive Tarot", "url": SITE},
             "about": BOOK_T_1912,
             "mainEntity": {"@type": "ItemList", "numberOfItems": 78, "itemListElement": [
                 {"@type": "ListItem", "position": j + 1, "name": n["name"], "url": f"{SITE}{BT_DIR}/{fname(n)}"}
                 for j, n in enumerate(cards)]}},
            breadcrumb_ld([("The Recursive Tarot", SITE), ("Book T", hub_url)])]
    files[f"{BT_DIR}/index.html"] = page2(h_title, h_desc, hub_url, cards[0]["metadata"]["illustrations"][0]["url"], h_ld, h_body, "../", "website")
    return [(f"{BT_DIR}/index.html", "0.8"), (f"{BT_DIR}/decans.html", "0.7")] + out


BOOK_T_1912 = {
    "@type": "Book", "name": "Book T", "author": {"@type": "Organization", "name": "Hermetic Order of the Golden Dawn"},
    "datePublished": "1912", "inLanguage": "en", "license": "https://creativecommons.org/publicdomain/mark/1.0/",
    "isPartOf": {"@type": "Periodical", "name": "The Equinox", "editor": {"@type": "Person", "name": "Aleister Crowley"}},
}


# ── Historical decks: one page each, from the deck's grammar ────────────────────────────────
def deck_images(slug, nodes, ledger):
    """node id -> ('show', thumb, credit) or ('off', holder_name, holder_url, why)."""
    rows = {r["item"]: r for r in ledger if r["deck"] == slug}
    out = {}
    for n in nodes:
        r = rows.get(n["id"])
        url = n.get("image_url") or ""
        if not url:
            continue
        credit = ((r or {}).get("credit") or "")
        holder = HOLDERS.get(slug)
        if slug in WITHHELD_DECKS:
            why, hname, hurl = WITHHELD_DECKS[slug]
            out[n["id"]] = ("off", hname, hurl, why)
        elif r and r["class"] in SHOWN_CLASSES and r["image_url"] == url and r.get("commons_title") and "dal negro" not in credit.lower():
            fn = r["commons_title"].split(":", 1)[1]
            lic = "CC BY-SA 4.0" if r["class"].startswith("commons-cc-by-sa") else "public domain"
            out[n["id"]] = ("show", commons_thumb("https://commons.wikimedia.org/wiki/Special:FilePath/" + fn, 250),
                            f"{(r.get('artist') or '').strip() or 'Unknown'} · {lic} · https://commons.wikimedia.org/wiki/{urllib.parse.quote(r['commons_title'].replace(' ', '_'))}")
        else:
            if r and "dal negro" in credit.lower():
                why = "scanned from the Dal Negro reproduction, a modern edition"
            elif r and r["class"] == "commons-pd-tag/bnf-scan":
                why = "BnF scan, free for non-commercial reuse only"
            elif r and r["class"] == "recorded-elsewhere":
                why = "scan from " + ("the BnF (Gallica), free for non-commercial reuse only" if "bnf.fr" in credit else "an archive whose terms are not yet confirmed")
            elif r and r["image_url"] != url:
                why = "image changed since the rights ledger was checked"
            else:
                why = "rights not recorded"
            hurl = credit if credit.startswith("http") and "info.json" not in credit else ""
            if not hurl:
                hurl = (n.get("metadata") or {}).get("image_source") or ""
                hurl = hurl if hurl.startswith("http") and "info.json" not in hurl else ""
            hname = "the holder"
            if holder and not hurl:
                hname, hurl = holder
            out[n["id"]] = ("off", hname, hurl, why)
    return out


def build_decks(files):
    ledger = load(LEDGER)["rows"]
    ids, public = eco_public()
    castable = {}
    for i in load("tarot/all-decks-many-lenses/grammar.json")["nodes"]:
        m = i.get("metadata") or {}
        if not i.get("parts") and m.get("source_deck") and m.get("arcana"):
            castable[m["source_deck"]] = castable.get(m["source_deck"], 0) + 1
    decks = []
    for slug in sorted(os.listdir(os.path.join(ROOT, "tarot"))):
        p = os.path.join(ROOT, "tarot", slug, "grammar.json")
        if slug in DECK_SKIP or not os.path.exists(p):
            continue
        g = load(f"tarot/{slug}/grammar.json")
        if (g.get("metadata") or {}).get("category") != "historical" or g.get("provenance") != "record":
            continue
        decks.append((slug, g))
    decks.sort(key=lambda d: ((d[1].get("metadata") or {}).get("year") or 9999, d[0]))
    hub_url = f"{SITE}{DECK_DIR}/index.html"
    out, tiles = [], []
    withheld_report = {}
    for slug, g in decks:
        meta = g.get("metadata") or {}
        nodes = g.get("nodes", [])
        cards = [n for n in nodes if not n.get("parts") and n.get("category") not in NONCARD]
        if not cards:
            cards = [n for n in nodes if n.get("image_url")]
        imgs = deck_images(slug, cards, ledger)
        shown = [k for k, v in imgs.items() if v[0] == "show"]
        off = [k for k, v in imgs.items() if v[0] == "off"]
        if off:
            withheld_report[slug] = (len(off), sorted({imgs[k][3] for k in off}))
        url = f"{SITE}{DECK_DIR}/{slug}.html"
        name = g["name"]
        desc_md = g.get("description") or ""
        about = md_blocks(desc_md)
        if not desc_md.strip():  # no description: the deck's own overview nodes say what it is
            about = "".join(
                f'<h2>{esc(n["name"])}</h2>' + "".join(f'<h3>{esc(k)}</h3>{md_blocks(v, False)}' for k, v in n.get("sections", {}).items())
                for n in nodes if n.get("parts") or n.get("category") in ("overview", "axis"))
            desc_md = " ".join(v for n in nodes if n.get("parts") or n.get("category") in ("overview", "axis")
                               for v in n.get("sections", {}).values())
        desc = clip(plain(desc_md), 158) or clip(name, 158)
        title = site_title(name)
        viewer = f"../viewers/cards.html?src=../tarot/{slug}/grammar.json"
        items = []
        for n in cards:
            v = imgs.get(n["id"])
            link = f'{viewer}&amp;item={esc(n["id"])}'
            if v and v[0] == "show":
                items.append(f'<li><a href="{link}" title="{esc(v[2])}"><img src="{esc(v[1])}" alt="{esc(n["name"])}" loading="lazy" width="250" height="416">{esc(n["name"])}</a></li>')
            elif v:
                h = f'<a href="{esc(v[2])}" rel="nofollow">see it at {esc(v[1])}</a>' if v[2] else "no image shown here"
                items.append(f'<li><span class="off">{h}</span><a href="{link}">{esc(n["name"])}</a></li>')
            else:
                items.append(f'<li><a href="{link}">{esc(n["name"])}</a></li>')
        eco = ids.get(slug) if slug in public else None
        actions = [f'<a class="btn primary" href="{CAST}{eco}">Draw &amp; reflect</a>' if eco and g.get("grammar_type") == "tarot" else
                   (f'<a class="btn primary" href="../viewers/caster-studio.html?src=../tarot/{slug}/grammar.json">Draw &amp; reflect</a>'
                    if castable.get(slug, 0) >= 3 else ""),
                   f'<a class="btn" href="{PLAY}{eco}&amp;pane=cards">Play it on recursive.eco</a>' if eco else "",
                   f'<a class="btn" href="{viewer}">Open in the card viewer</a>']
        attrib = "".join(
            f'<li>{esc(a.get("name", ""))}{(" (" + esc(a["date"]) + ")") if a.get("date") else ""}{(": " + inline_md(a["note"])) if a.get("note") else ""}</li>'
            for a in (g.get("_grammar_commons") or {}).get("attribution", []))
        img_note = ""
        if off:
            reasons = "; ".join(sorted({imgs[k][3] for k in off}))
            img_note = DRAFT + (f'<p class="src">{len(off)} of {len(off) + len(shown)} card images are not shown on this page ({esc(reasons)}). '
                        f'Each card links to where its holder shows it; the card viewer and recursive.eco still open the deck.</p>')
        research = (g.get("_research") or {}).get("deck")
        first = next((imgs[k][1] for k in shown), None)
        og = first.replace("/250px-", "/500px-") if first else commons_thumb("https://commons.wikimedia.org/wiki/Special:FilePath/RWS_Tarot_00_Fool.jpg", 500)
        kicker = " · ".join(x for x in [meta.get("year_label") or str(meta.get("year") or ""), meta.get("tradition", "")] if x)
        body = f"""{crumbs([("The Recursive Tarot", "../index.html"), ("Historical decks", "index.html"), (meta.get('common_name') or name, None)])}
<p class="kicker">{esc(kicker)}</p>
<h1>{esc(name)}</h1>
<div class="actions">{''.join(actions)}</div>
<div class="prose">{about}</div>
<h2 id="cards">The cards ({len(cards)})</h2>
{img_note}
<ul class="grid">{''.join(items)}</ul>
<h2 id="sources">Sources and credits</h2>
<p class="src">{inline_md(g.get('image_credit') or '')}</p>
<ul class="src">{attrib}</ul>
<p class="fine">{'Research dossier: <a href="' + GITHUB + esc(research) + '">' + esc(research) + '</a>. ' if research else ''}Data: <a href="{GITHUB}tarot/{slug}/grammar.json">tarot/{slug}/grammar.json</a>, {esc((g.get('_grammar_commons') or {}).get('license', 'CC-BY-SA-4.0'))}. Images keep their own licences (hover a card for its credit).</p>"""
        ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": title, "description": desc, "url": url,
               "inLanguage": "en", "isPartOf": {"@type": "WebSite", "name": "The Recursive Tarot", "url": SITE},
               "about": {"@type": "CreativeWork", "name": meta.get("common_name") or name,
                         **({"dateCreated": meta["year_label"]} if meta.get("year_label") else {})},
               "mainEntity": {"@type": "ItemList", "numberOfItems": len(cards), "itemListElement": [
                   {"@type": "ListItem", "position": j + 1, "name": n["name"]} for j, n in enumerate(cards)]},
               "license": "https://creativecommons.org/licenses/by-sa/4.0/"},
              breadcrumb_ld([("The Recursive Tarot", SITE), ("Historical decks", hub_url), (meta.get("common_name") or name, url)])]
        files[f"{DECK_DIR}/{slug}.html"] = page2(title, desc, url, og, ld, body, "../", "website")
        out.append((f"{DECK_DIR}/{slug}.html", "0.7"))
        cover = next((imgs[k][1] for k in shown), None)
        tiles.append(f'<li><a href="{slug}.html">' + (f'<img src="{esc(cover)}" alt="" loading="lazy" width="250" height="416">' if cover
                     else '<span class="off">no image shown here</span>') + f'{esc(meta.get("common_name") or name)} · {esc(meta.get("year_label") or "")}</a></li>')
    h_title = "Historical tarot decks, one page each · Recursive Tarot"
    h_desc = clip("The historical tarot and playing-card decks of the Recursive Tarot, oldest first: "
                  + ", ".join((g.get("metadata") or {}).get("common_name") or s for s, g in decks) + ".", 158)
    h_body = f"""{crumbs([("The Recursive Tarot", "../index.html"), ("Historical decks", None)])}
<p class="kicker">Historical decks · oldest first</p>
<h1>Historical decks</h1>
{DRAFT}
<p class="prose">Each deck below has a page made from its grammar: what it is, its history, its cards and its sources.</p>
<ul class="grid">{''.join(tiles)}</ul>
<p class="fine">Images keep their own licences; where a scan's terms do not allow reuse here, the card links to its holder.</p>"""
    h_ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": h_title, "description": h_desc, "url": hub_url,
             "inLanguage": "en", "isPartOf": {"@type": "WebSite", "name": "The Recursive Tarot", "url": SITE},
             "mainEntity": {"@type": "ItemList", "numberOfItems": len(decks), "itemListElement": [
                 {"@type": "ListItem", "position": j + 1, "name": g["name"], "url": f"{SITE}{DECK_DIR}/{s}.html"}
                 for j, (s, g) in enumerate(decks)]}},
            breadcrumb_ld([("The Recursive Tarot", SITE), ("Historical decks", hub_url)])]
    files[f"{DECK_DIR}/index.html"] = page2(h_title, h_desc, hub_url, commons_thumb("https://commons.wikimedia.org/wiki/Special:FilePath/RWS_Tarot_00_Fool.jpg", 500),
                                            h_ld, h_body, "../", "website")
    build_decks.withheld = withheld_report
    return [(f"{DECK_DIR}/index.html", "0.8")] + out


# ── Spreads: Waite's own Celtic Cross, his trump meanings, the site's spreads ───────────────
def build_spreads(files, trumps, card_url):
    paras, positions = waite_celtic()
    spreads = load("viewers/spreads.json").get("spreads", [])
    url = SITE + SPREADS
    rows = "".join(
        f'<tr><td>{k}</td><td><a href="{card_url[k]}">{esc(trumps[k]["name"])}</a></td><td>{esc(trumps[k]["up"])}</td><td>{esc(trumps[k]["rev"])}</td></tr>'
        for k in [*range(1, 21), 0, 21])  # Waite's own order: Zero after 20
    others = "".join(
        f'<li><a href="viewers/caster-studio.html?spread={esc(s["id"])}">{esc(s["name"])}</a>: {esc(s.get("description", ""))} ({len(s.get("positions", []))} cards)</li>'
        for s in spreads)
    title = "The Celtic Cross Tarot Spread in Waite's Own Words (1911)"
    desc = ("Waite's own Celtic Cross from The Pictorial Key to the Tarot (1911): the Significator, the ten cards and what each "
            "covers, with his meanings for the 22 trumps.")
    body = f"""{crumbs([("The Recursive Tarot", "index.html"), ("Tarot spreads", None)])}
<p class="kicker">A. E. Waite · <cite>The Pictorial Key to the Tarot</cite> · 1911 · Part III</p>
<h1>Tarot spreads: the Celtic Cross in Waite's own words</h1>
<p class="creed">{esc(CREED.split(" These")[0])}</p>
<div class="actions"><a class="btn primary" href="viewers/caster-studio.html?spread=celtic-cross">Lay the cards: Celtic Cross</a>
<a class="btn" href="{HUB}">Tarot card meanings</a></div>
<h2 id="celtic-cross">An Ancient Celtic Method of Divination</h2>
<div class="prose">{''.join(f'<p>{inline_md(p)}</p>' for p in paras)}</div>
<h3>The ten cards</h3>
<ol class="positions">{''.join(f'<li>{esc(p)}</li>' for _, p in positions)}</ol>
{DRAFT}
<p class="src">A. E. Waite, <cite>The Pictorial Key to the Tarot</cite> (London: William Rider &amp; Son, 1911), Part III §7, public domain. Waite's own diagram is not reproduced here; the list above is his key to it. The caster's Celtic Cross names its positions in this site's words, not Waite's.</p>
<h2 id="trumps">Waite's meanings for the 22 trumps</h2>
<table class="dt"><thead><tr><th>No.</th><th>Trump</th><th>Upright</th><th>Reversed</th></tr></thead><tbody>{rows}</tbody></table>
{DRAFT}
<p class="src">Part III §3, "The Greater Arcana and their Divinatory Meanings", in Waite's order and numbering (Fortitude 8, Justice 11; the Zero after 20). Public domain. Each trump links to its card page.</p>
<h2 id="spreads">Spreads you can lay on this site</h2>
<ul class="prose">{others}</ul>
<p class="fine">Waite's text is public domain; transcription slips fixed against the 1911 text are listed in <code>scripts/build_card_pages.py</code> (<code>WAITE_FIXES</code>). Arrangement CC-BY-SA-4.0 (PlayfulProcess).</p>"""
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": url, "inLanguage": "en",
           "isPartOf": {"@type": "WebSite", "name": "The Recursive Tarot", "url": SITE},
           "mainEntity": {"@type": "Chapter", "name": "An Ancient Celtic Method of Divination", "isPartOf": PICTORIAL_KEY},
           "license": "https://creativecommons.org/licenses/by-sa/4.0/"},
          breadcrumb_ld([("The Recursive Tarot", SITE), ("Tarot spreads", url)])]
    files[SPREADS] = page2(title, desc, url, commons_thumb("https://commons.wikimedia.org/wiki/Special:FilePath/RWS_Tarot_00_Fool.jpg", 500),
                           ld, body, "", "article", "play")
    return [(SPREADS, "0.8")]


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def read(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")  # a Windows checkout (autocrlf) is the same page


def main():
    check = "--check" in sys.argv
    files, order, more = build()
    problems, notes = [], []
    for rel, text in files.items():
        if read(rel) != text:
            problems.append(f"{rel} is stale")
    for d in (OUT_DIR, BT_DIR, DECK_DIR):  # every file in a generated folder is ours
        if check and os.path.isdir(os.path.join(ROOT, d)):
            extra = set(os.listdir(os.path.join(ROOT, d))) - {os.path.basename(p) for p in files if p.startswith(d + "/")}
            problems += [f"{d}/{e} is not generated by this script" for e in sorted(extra)]

    entries = list(STATIC_PAGES.items()) + [(HUB, "0.9")] + [(p, "0.7") for p in order] + more
    lastmod = json.loads(read(LASTMOD) or "{}")
    today = datetime.date.today().isoformat()
    new_lastmod = {}
    for path, _ in entries:
        text = files.get(path) if path in files else read(path)
        if text is None:
            problems.append(f"{path} (listed in the sitemap) does not exist")
            continue
        h, old = sha(text), lastmod.get(path)
        if old and old["sha"] == h:
            new_lastmod[path] = old
        else:
            if path in STATIC_PAGES:
                notes.append(path)
            new_lastmod[path] = {"sha": h, "lastmod": today}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<!-- Generated by scripts/build_card_pages.py; never hand-edit. -->',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, prio in entries:
        if path in new_lastmod:
            loc = SITE if path == "index.html" else SITE + path
            out.append(f"  <url><loc>{loc}</loc><lastmod>{new_lastmod[path]['lastmod']}</lastmod><priority>{prio}</priority></url>")
    out.append("</urlset>")
    sm = "\n".join(out) + "\n"
    lm_text = json.dumps(new_lastmod, indent=1, sort_keys=True) + "\n"

    if check:
        generated_drift = [p for p in new_lastmod if p not in STATIC_PAGES and (lastmod.get(p) or {}).get("sha") != new_lastmod[p]["sha"]]
        if generated_drift:
            problems.append("sitemap lastmod is stale for generated pages")
        if problems:
            print("STALE: " + "; ".join(problems[:8]) + (" ..." if len(problems) > 8 else ""))
            print("Fix: python scripts/build_card_pages.py")
            sys.exit(1)
        if notes:
            print(f"note: {len(notes)} hand-edited page(s) changed since their sitemap lastmod "
                  f"({', '.join(notes[:3])}); re-run scripts/build_card_pages.py to refresh the dates")
        print(f"OK: {len(order)} card pages, {HUB} and {len(more)} Book T / deck / spreads pages are current")
        return

    for d in (OUT_DIR, BT_DIR, DECK_DIR, "data"):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    for rel, text in list(files.items()) + [("sitemap.xml", sm), (LASTMOD, lm_text)]:
        if read(rel) != text:
            with open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    print(f"wrote {len(order)} card pages, {HUB}, {len(more)} Book T / deck / spreads pages, sitemap.xml ({len(entries)} URLs)")


if __name__ == "__main__":
    main()
