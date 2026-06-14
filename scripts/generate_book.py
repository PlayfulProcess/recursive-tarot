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

def inline(s):
    s = re.sub(r"\s*\[@[^\]]+\]", "", str(s or ""))      # drop citation keys
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
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
def thumb(url):
    if not url:
        return None
    h = hashlib.md5(url.encode()).hexdigest()[:16]
    rel = "build/img/%s.jpg" % h
    dst = os.path.join(BOOK, rel)
    if os.path.exists(dst):
        return rel
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "recursive-tarot-book"})
        data = urllib.request.urlopen(req, timeout=30).read()
        im = Image.open(BytesIO(data)).convert("RGB")
        im.thumbnail((IMG_W, IMG_W * 3))      # cap width; keep aspect
        im.save(dst, "JPEG", quality=82, optimize=True)
        return rel
    except Exception as e:
        _imgfail[0] += 1
        return None

# ── data ──
col = load(os.path.join(TAROT, "_collection.json"))
decks = [g for g in col["grammars"] if not g.get("is_meta") and g.get("type") != "meta"]
synth = load(SYN)
people = load(os.path.join(TAROT, "people-of-tarot", "grammar.json"))
tree = {it["id"]: it for it in load(os.path.join(TAROT, "tree-of-tarot", "grammar.json"))["items"]}

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
    for it in dg.get("items", []):
        tk = (it.get("metadata") or {}).get("trump_key")
        if not tk:
            continue
        img = it.get("image_url") or (it.get("metadata") or {}).get("image_url")
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
        out.append('<section class="deck-chapter"><h3>%s%s</h3>%s%s%s</section>'
                   % (esc((g.get("name") or slug).split(" — ")[0]),
                      (" · %s" % yl) if yl else "", coverhtml, render_markdown(g.get("_desc")), strip))
    print("  deck signature images: %d" % n)
    return "".join(out)

def fig(which):
    label = "The Lineage of Tarot" if which == "lineage" else "Timeline · 1440s–1900s"
    return ('<figure class="figure"><img src="figures/%s.png" alt="%s">'
            '<figcaption>%s</figcaption></figure>' % (which, esc(label), esc(label)))

def render_people():
    by_deck = {}
    for p in people["items"]:
        if (p.get("metadata") or {}).get("kind") != "person" and p.get("category") != "person":
            continue
        for slug in ((p.get("metadata") or {}).get("made") or []):
            by_deck.setdefault(slug, []).append(p)
    r3 = next((i for i in people["items"] if i["id"] == "root-people-of-tarot"), None)
    html = ['<div class="people">']
    if r3:
        html.append(para((r3.get("sections") or {}).get("What it is")))
    for slug in sorted(by_deck, key=lambda s: deck_year(s) or 9999):
        yr = deck_year(slug)
        html.append('<h3>%s%s</h3>' % (esc(deck_name(slug)), (" · %d" % yr) if yr else ""))
        for p in by_deck[slug]:
            who = (p.get("sections") or {}).get("Who") or ""
            life = (p.get("metadata") or {}).get("lifespan") or ""
            html.append('<div class="bio"><div class="bio-name">%s%s</div><div class="bio-text">%s</div></div>'
                        % (esc(p.get("name")), (' <span class="bio-life">%s</span>' % esc(life)) if life else "", para(who)))
    html.append("</div>")
    return "".join(html)

ANCHOR_EARLY = ["cary-yale-visconti-tarot", "visconti-sforza-tarot", "charles-vi-tarot", "este-tarot"]

def render_cards():
    out = []
    n_imgs = 0
    for i, tk in enumerate(ORDER):
        if tk not in synth:
            continue
        lbl = tk.replace("-", " ").title()
        entries = sorted(trump_idx.get(tk, []), key=lambda x: x["year"])

        # image strip across decks
        cells = []
        for c in entries:
            rel = thumb(c["img"])
            if not rel:
                continue
            n_imgs += 1
            cells.append('<figure class="c"><img src="%s"><figcaption>%s</figcaption></figure>'
                         % (esc(rel), esc(c["name"][:16])))

        # "In the decks" — the literal Scene from anchor decks (earliest · Marseille · Golden Dawn)
        def scene_of(slug):
            for c in entries:
                if c["slug"] == slug:
                    s = c["sections"]
                    return s.get("Scene") or s.get("About") or s.get("Iconography")
            return None
        early = next((s for s in ANCHOR_EARLY if scene_of(s)), None)
        anchors = []
        for slug in [early, "tarot-de-marseille-conver", "golden-dawn-book-t-tarot"]:
            if slug:
                sc = scene_of(slug)
                if sc:
                    anchors.append((slug, sc))
        indecks = ""
        if anchors:
            indecks = "<h4>In the decks</h4>" + "".join(
                '<p class="indeck"><strong>%s · %s.</strong> %s%s</p>'
                % (esc(deck_name(s)), deck_year(s) or "", inline(sc[:520]), "…" if len(sc) > 520 else "")
                for s, sc in anchors)

        # "Later readings" — the dated commentary (Gébelin / Papus / Wirth / Waite), by year, one per voice
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

        out.append('<section class="card-chapter"><h3>%d — %s</h3><div class="synthbox">%s</div>'
                   '<div class="strip">%s</div>%s%s</section>'
                   % (i, esc(lbl), para(synth[tk]), "".join(cells), indecks, laterhtml))
    print("  card images embedded: %d" % n_imgs)
    return "".join(out)

EMBED = {
    "lineage": lambda: fig("lineage"),
    "timeline": lambda: fig("timeline"),
    "people": render_people,
    "decks": render_decks,
    "all-cards": render_cards,
}

# ── render the MDX (single source for prose) ──
def render_mdx():
    body = []
    title = "The Recursive Tarot"
    for block in re.split(r"\n{2,}", open(MDX, encoding="utf-8").read().strip()):
        b = block.strip()
        m = re.match(r'<div data-embed="([a-z\-]+)"', b)
        if m:
            fn = EMBED.get(m.group(1))
            if fn:
                body.append(fn())
            continue
        if b.startswith("### "):
            body.append("<h3>%s</h3>" % inline(b[4:]))
        elif b.startswith("## "):
            body.append('<h2 class="chapter">%s</h2>' % inline(b[3:]))
        elif b.startswith("# "):
            title = b[2:].strip()
            body.append("<h1>%s</h1>" % inline(title))
        else:
            body.append(para(b))
    return title, "".join(body)

CSS = """
@page { size: 7in 10in; margin: 0.62in 0.6in; }
@page :first { margin-top: 2in; }
html,body{ margin:0; }
body{ font: 11pt/1.55 Georgia,'Times New Roman',serif; color:#111; }
h1{ font-size:30pt; line-height:1.1; margin:0 0 .2em; }
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
.strip{ display:flex; flex-wrap:wrap; gap:7px; break-inside:avoid; }
.strip .c{ margin:0; text-align:center; width:1in; }
.strip .c img{ width:1in; height:1.6in; object-fit:cover; border:1px solid #ccc; border-radius:4px; }
.strip .c figcaption{ font-size:6.5pt; }
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
