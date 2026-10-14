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


def page(title, desc, canonical, og_image, ldjson, body, pfx, og_type="article"):
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
<site-header active="cards"></site-header>
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
{'' if up or not major else '<p class="src">For the trumps, Waite gives his divinatory meanings in a separate list in Part III of the book; they are not carried here yet.</p>'}
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
    return files, order


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
    files, order = build()
    problems, notes = [], []
    for rel, text in files.items():
        if read(rel) != text:
            problems.append(f"{rel} is stale")
    if check and os.path.isdir(os.path.join(ROOT, OUT_DIR)):
        extra = set(os.listdir(os.path.join(ROOT, OUT_DIR))) - {os.path.basename(p) for p in order}
        problems += [f"{OUT_DIR}/{e} is not generated by this script" for e in sorted(extra)]

    entries = list(STATIC_PAGES.items()) + [(HUB, "0.9")] + [(p, "0.7") for p in order]
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
        print(f"OK: {len(order)} card pages and {HUB} are current")
        return

    os.makedirs(os.path.join(ROOT, OUT_DIR), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    for rel, text in list(files.items()) + [("sitemap.xml", sm), (LASTMOD, lm_text)]:
        if read(rel) != text:
            with open(os.path.join(ROOT, rel), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    print(f"wrote {len(order)} card pages, {HUB}, sitemap.xml ({len(entries)} URLs)")


if __name__ == "__main__":
    main()
