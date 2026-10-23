# -*- coding: utf-8 -*-
"""One-time converter (Oct 23 2026): course/*.mdx + course/booklets/*.mdx -> tarot/<slug>-course/grammar.json,
read in recursive.eco Play's Continuous view. Not kept: deleted once the courses live as grammars.

The app renders markdown, not raw HTML, so each course's HTML becomes what a grammar already holds:
  ## lesson                    -> a node with one Content section
  YouTube <iframe>             -> its own node at that point, metadata.youtube_url (tap-to-load)
  <img>, <figure>+<figcaption> -> markdown image + italic caption line (paths made absolute)
  inline <svg>                 -> tarot/<slug>-course/diagrams/n.svg, shown as a markdown image
  data-embed galleries         -> markdown (images, deck lists, links to the live pages)
  <style>                      -> dropped; any other tag -> markdown or its text

Run: python scripts/convert_courses.py
"""
import base64, html, io, json, os, re, sys, urllib.request
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://tarot.recursive.eco"
PAGES = SITE + "/pages/"
PLAY = "https://recursive.eco/play?id="

IDS = json.load(io.open(os.path.join(ROOT, "tarot", "_eco_ids.json"), encoding="utf-8"))
PUBLIC = set(IDS.get("_public_now", []))
COLLECTION = json.load(io.open(os.path.join(ROOT, "tarot", "_collection.json"), encoding="utf-8"))
COURSES = json.load(io.open(os.path.join(ROOT, "course", "_courses.json"), encoding="utf-8"))
LISTED = {}
for g in COURSES["groups"]:
    for c in g["courses"]:
        LISTED[c["id"]] = (g["name"], c)

# Theme values for the diagrams' CSS variables (theme.css, light), so an .svg file draws on its own.
THEME = {"bad": "#c0473b", "chip": "#faf3e6", "faint": "#8a8273", "gold": "#9a7322", "good": "#3f7a5c",
         "ink": "#221f1a", "ink-soft": "#4a4439", "line": "#d8d2c6", "mut": "#6b6457", "surface": "#ffffff",
         "thumb-bg": "#faf8f3", "panel2": "#faf8f3",
         "sans": 'Inter,system-ui,-apple-system,"Segoe UI",sans-serif',
         "serif-display": '"Fraunces",Georgia,"Times New Roman",serif'}

LOSSY = {}  # slug -> [notes]


def note(slug, msg):
    LOSSY.setdefault(slug, [])
    if msg not in LOSSY[slug]:
        LOSSY[slug].append(msg)


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")[:40] or "x"


def deck_url(slug):
    if slug in PUBLIC and IDS["ids"].get(slug):
        return PLAY + IDS["ids"][slug]
    return SITE + "/viewers/cards.html?src=../tarot/%s/grammar.json" % slug


def absolute(url, base=PAGES):
    """A link or image as the course viewer resolved it (relative to pages/; images/ -> pages/courses/images/)."""
    url = html.unescape(url.strip())
    if not url or re.match(r"^[a-z][a-z0-9+.-]*:", url, re.I) or url.startswith("//"):
        return url
    m = re.match(r"^#deck-([a-z0-9-]+)$", url)
    if m:
        return deck_url(m.group(1))
    if url.startswith("#"):
        return url
    if url.startswith("images/") or url.startswith("../images/"):
        return SITE + "/pages/courses/" + url.replace("../", "")
    if url.startswith("/"):
        return SITE + url
    parts = (base.replace(SITE, "").strip("/").split("/") if base != SITE + "/" else [])
    for seg in url.split("/")[:-1]:
        if seg == "..":
            parts = parts[:-1]
        elif seg != ".":
            parts.append(seg)
    return SITE + "/" + "/".join(parts + [url.split("/")[-1]])


def attr(tag, name):
    m = re.search(r'\b%s\s*=\s*"([^"]*)"' % name, tag) or re.search(r"\b%s\s*=\s*'([^']*)'" % name, tag)
    return html.unescape(m.group(1)) if m else ""


# --------------------------------------------------------------------------- diagrams
_img_cache = {}


def inline_image(url):
    """A card picture inside a diagram, embedded small (an .svg shown as an <img> cannot fetch it)."""
    if url in _img_cache:
        return _img_cache[url]
    try:
        from PIL import Image
        raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "convert-courses"}), timeout=60).read()
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        im.thumbnail((200, 340))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=82)
        data = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception as e:  # leave the address; the diagram still draws, without that picture
        print("   ! could not inline", url, e)
        data = url
    _img_cache[url] = data
    return data


def save_svg(svg, slug, n, outer_css=""):
    svg = re.sub(r"var\(--([a-z0-9-]+)\)", lambda m: THEME.get(m.group(1), "#221f1a"), svg)
    svg = re.sub(r"&(?!#?\w+;)", "&amp;", svg)  # a standalone .svg is XML: bare & breaks it
    if "xmlns=" not in svg[:400]:
        svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    if "xmlns:xlink" not in svg[:600] and "xlink:" in svg:
        svg = svg.replace("<svg", '<svg xmlns:xlink="http://www.w3.org/1999/xlink"', 1)
    svg = re.sub(r'(<image\b[^>]*?\b(?:xlink:)?href=")([^"]+)(")',
                 lambda m: m.group(1) + (inline_image(m.group(2)) if m.group(2).startswith("http") else inline_image(absolute(m.group(2)))) + m.group(3), svg)
    # a light ground, so the diagram reads on Play's dark theme too
    vb = re.search(r'viewBox="([\d.\s-]+)"', svg)
    if vb:
        x, y, w, h = vb.group(1).split()
        svg = re.sub(r"(<svg\b[^>]*>)", r'\1<rect x="%s" y="%s" width="%s" height="%s" fill="#ffffff"/>' % (x, y, w, h), svg, count=1)
        if not re.search(r"<svg\b[^>]*\bwidth=", svg):
            svg = svg.replace("<svg", '<svg width="%s" height="%s"' % (w, h), 1)
    rel = "tarot/%s/diagrams/%d.svg" % (slug, n)
    os.makedirs(os.path.join(ROOT, os.path.dirname(rel)), exist_ok=True)
    io.open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(svg)
    return SITE + "/" + rel


# --------------------------------------------------------------------------- history-of-tarot galleries
def deck_node_image(deck, ref):
    try:
        g = json.load(io.open(os.path.join(ROOT, "tarot", deck, "grammar.json"), encoding="utf-8"))
    except Exception:
        return ""
    for n in g.get("nodes", []):
        md = n.get("metadata") or {}
        if (ref.startswith("tk:") and md.get("trump_key") == ref[3:]) or (ref.startswith("item:") and n.get("id") == ref[5:]):
            return n.get("image_url") or md.get("image_url") or ""
    return ""


def embed_md(name):
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import course_to_grammar as old  # the plates list + the essay expander live there until it is deleted
    meta_id = IDS["ids"].get("all-decks-many-lenses")
    meta = (PLAY + meta_id) if meta_id else SITE + "/viewers/explorer.html"
    if name == "lineage":
        return ("![The Lineage of Tarot](%s/print/book/figures/lineage.png)\n\n*The Lineage of Tarot. "
                "[Open the live family tree](%s/viewers/genealogy-tree.html), where every deck opens.*" % (SITE, SITE))
    if name == "timeline":
        return ("![Timeline, 1440s to 1900s](%s/print/book/figures/timeline.png)\n\n*Timeline, 1440s to 1900s. "
                "[Open the live timeline](%s/viewers/timeline.html).*" % (SITE, SITE))
    if name == "decks":
        rows = [g for g in COLLECTION.get("grammars", []) if not g.get("is_meta")]
        rows.sort(key=lambda g: g.get("year") or 9999)
        out = ["Every deck in the library, oldest first. Each link opens the deck, with its story and the hands that made it:", ""]
        for g in rows:
            nm = (g.get("name") or g["slug"]).split(" — ")[0]
            out.append("- [%s](%s)%s" % (nm, deck_url(g["slug"]), (" · " + g["year_label"]) if g.get("year_label") else ""))
        return "\n".join(out)
    if name == "plates":
        out = []
        for e in old.PLATES_EMBEDS:
            if "heading" in e:
                out.append("### " + e["heading"])
                continue
            img = deck_node_image(e["deck"], e["ref"])
            if not img:  # a card shown without a picture (rights) is skipped, as the old gallery did
                continue
            out.append("[![%s](%s)](%s)" % (e["caption"].split(" — ")[0], img, deck_url(e["deck"])))
            out.append("*%s*" % e["caption"])
        return "\n\n".join(out)
    if name == "essay":
        return old._expand_essay()
    if name in ("suits-detail", "trumps-detail"):
        return "*Card by card, with each tradition's meanings: the site's [card meanings page](%s/tarot-card-meanings.html), one page per card.*" % SITE
    if name == "suits":
        return ("*The four suits, card by card across the decks, live in [All Decks, Many Lenses](%s) "
                "and on the site's [card meanings page](%s/tarot-card-meanings.html).*" % (meta, SITE))
    if name == "numbers":
        return ("*The ten numbers, each with its one meaning across the four suits: see the pips in "
                "[All Decks, Many Lenses](%s) and the [card meanings page](%s/tarot-card-meanings.html).*" % (meta, SITE))
    if name == "trumps-synthesis":
        return ("*All twenty-two trumps, each followed across the decks with the dated readings later attached: "
                "[All Decks, Many Lenses](%s) and the [card meanings page](%s/tarot-card-meanings.html).*" % (meta, SITE))
    if name == "apparatus":
        books = IDS["ids"].get("books-of-tarot")
        return ("*Image credits, bibliography and colophon: every deck's own grammar names its sources and image rights; "
                "the shared list is the [Sources page](%s/pages/sources.html)%s.*"
                % (SITE, (" and [The Books of Tarot](%s)" % (PLAY + books)) if books else ""))
    return ""


# --------------------------------------------------------------------------- html -> markdown
VIDEO = "\n\n@@VIDEO@@%s@@%s@@\n\n"


def html_to_md(text, slug, counter):
    text = re.sub(r"<!--.*?-->[ \t]*\n?", "", text, flags=re.S)  # authoring comments
    # 1. <style> blocks go (Play has its own look); keep their CSS for the diagrams.
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", text, re.S))
    text = re.sub(r"<style[^>]*>.*?</style>\s*", "", text, flags=re.S)

    # 2. YouTube: iframe (with its wrapper div), or a linked YouTube thumbnail -> a video token.
    def yt(m):
        frag = m.group(0)
        vid = re.search(r"(?:embed/|watch\?v=|youtu\.be/|/vi/)([A-Za-z0-9_-]{11})", frag)
        title = attr(re.search(r"<(?:iframe|img)\b[^>]*>", frag).group(0), "title") or attr(re.search(r"<(?:iframe|img)\b[^>]*>", frag).group(0), "alt")
        return VIDEO % (vid.group(1), title.replace("@@", " "))
    text = re.sub(r"<div[^>]*>\s*<iframe\b[^>]*youtube[^>]*>\s*</iframe>\s*</div>", yt, text, flags=re.S)
    text = re.sub(r"<iframe\b[^>]*youtube[^>]*>\s*</iframe>", yt, text, flags=re.S)
    text = re.sub(r'<a\b[^>]*href="https?://(?:www\.)?youtube\.com/watch\?v=[^"]+"[^>]*>\s*<img\b[^>]*ytimg[^>]*>\s*</a>', yt, text, flags=re.S)
    if "<iframe" in text:
        note(slug, "a non-YouTube iframe was reduced to its text")

    # 3. figures: svg/img + figcaption -> images + italic caption. A figure marked "-wide" is the
    #    desktop twin of a narrow (phone) one; the narrow one is kept.
    def fig(m):
        whole, cls = m.group(0), attr(m.group(0)[:300], "class")
        if re.search(r"-wide\b", cls):
            note(slug, "a diagram drawn twice (narrow + wide) keeps only its narrow, phone-first layout")
            return ""
        cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", whole, re.S)
        body = re.sub(r"<figcaption[^>]*>.*?</figcaption>", "", whole, flags=re.S)
        body = re.sub(r"^<figure[^>]*>|</figure>$", "", body.strip(), flags=re.S)
        out = svgs_and_imgs(body)
        if cap:
            c = inline_md(cap.group(1)).strip()
            if c:
                out += "\n\n*" + c.replace("*", "") + "*"
        return "\n\n" + out.strip() + "\n\n"

    def svgs_and_imgs(body):
        def sv(m):
            counter[0] += 1
            svg = m.group(0)
            label = attr(svg[:2000], "aria-label") or "Diagram"
            if css and "<style" not in svg:
                svg = re.sub(r"(<svg\b[^>]*>)", r"\1<style>" + css.replace("\\", "\\\\") + "</style>", svg, count=1)
            return "\n\n![%s](%s)\n\n" % (label.replace("]", ")").replace("[", "("), save_svg(svg, slug, counter[0]))
        body = re.sub(r"<svg\b.*?</svg>", sv, body, flags=re.S)
        return body

    text = re.sub(r"<figure\b.*?</figure>", fig, text, flags=re.S)
    text = svgs_and_imgs(text)

    # 4. footnote lists: <ol start=N><li>..</li></ol> -> "N. text" lines; <aside> wrappers go.
    def ol(m):
        start = int(attr(m.group(0)[:60], "start") or 1)
        items = re.findall(r"<li\b[^>]*>(.*?)</li>", m.group(0), re.S)
        return "\n\n" + "\n".join("%d. %s" % (start + i, inline_md(t).strip()) for i, t in enumerate(items)) + "\n\n"
    text = re.sub(r"<ol\b.*?</ol>", ol, text, flags=re.S)
    text = re.sub(r"</?aside\b[^>]*>", "\n", text)

    # 5. the rest, line by line (tables need their cells on one line).
    lines = []
    for ln in text.split("\n"):
        in_table = ln.lstrip().startswith("|")
        if in_table:
            ln = re.sub(r"<br\s*/?>", " · ", ln)
        elif re.search(r"<br\s*/?>\s*$", ln):
            ln = re.sub(r"<br\s*/?>\s*$", "  ", ln)
        ln = re.sub(r"<br\s*/?>", "  \n", ln)
        lines.append(inline_md(ln))
    return "\n".join(lines)


def inline_md(s):
    # <a><img></a>: a small logo becomes the link's words; a real picture stays a linked image.
    def a_img(m):
        href = absolute(attr(m.group(1), "href"))
        img = re.search(r"<img\b[^>]*>", m.group(2)).group(0)
        src, alt = attr(img, "src"), attr(img, "alt")
        if re.search(r"(logo|github-mark|icon)[^/]*\.svg$", src):
            return "[%s](%s)" % (alt or "link", href) + " "
        words = re.sub(r"<[^>]+>", " ", m.group(3)).strip()
        return "[![%s](%s)](%s)" % (alt, absolute(src), href) + (" *%s*" % words if words else "")
    s = re.sub(r"(<a\b[^>]*>)\s*(<img\b[^>]*>)(.*?)</a>", a_img, s, flags=re.S)
    s = re.sub(r"<img\b[^>]*>", lambda m: "![%s](%s)" % (attr(m.group(0), "alt").replace("]", ")").replace("[", "("), absolute(attr(m.group(0), "src"))), s)

    def a(m):
        href, inner = attr(m.group(1), "href"), m.group(2)
        t = re.sub(r"<[^>]+>", "", inner).strip()
        if not t:
            return ""
        if re.match(r"^#(note|ref)-", href) or not href:
            return t if not re.match(r"^back to the text$", t, re.I) else ""
        return "[%s](%s)" % (t, absolute(href))
    s = re.sub(r"(<a\b[^>]*>)(.*?)</a>", a, s, flags=re.S)
    s = re.sub(r"<sup\b[^>]*>(.*?)</sup>", lambda m: "[" + re.sub(r"<[^>]+>", "", m.group(1)) + "]", s, flags=re.S)
    s = re.sub(r"</?(strong|b)\b[^>]*>", "**", s)
    s = re.sub(r"</?(em|i)\b[^>]*>", "*", s)
    s = re.sub(r"</?[a-zA-Z][a-zA-Z0-9-]*\b[^>]*>", "", s)  # any other tag: its text stays
    return s


def md_links(text):
    """Markdown links/images with relative addresses -> absolute (Play is another site)."""
    text = re.sub(r"(?<!!)\[([^\]]*)\]\(#(?!deck-)[^)\s]*\)", lambda m: m.group(1), text)  # in-page anchors: Play has none
    return re.sub(r"(!?\[[^\]]*\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))",
                  lambda m: m.group(1) + absolute(m.group(2)) + m.group(3), text)


def protect_code(text):
    keep = []

    def k(m):
        keep.append(m.group(0))
        return "\x00%d\x00" % (len(keep) - 1)
    text = re.sub(r"```.*?```", k, text, flags=re.S)
    text = re.sub(r"`[^`\n]+`", k, text)
    return text, keep


def restore_code(text, keep):
    return re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], text)


# --------------------------------------------------------------------------- one course
def convert(src_rel, slug, booklet=False):
    text = io.open(os.path.join(ROOT, src_rel), encoding="utf-8").read().lstrip("﻿")
    fm, body = {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
        body = text[m.end():]
    cid = os.path.splitext(os.path.basename(src_rel))[0]

    body, keep = protect_code(body)
    for nm in sorted(set(re.findall(r'<div data-embed="([a-z-]+)"[^>]*>\s*</div>', body))):
        if nm in ("essay", "plates", "lineage", "timeline", "decks"):
            note(slug, "data-embed '%s' baked in as markdown (%s)" % (nm, {"essay": "the essay text itself", "plates": "the plates as images with captions", "lineage": "a still picture + link to the live tree", "timeline": "a still picture + link to the live timeline", "decks": "a dated list of deck links (the per-deck chapters, covers and makers stay in each deck)"}[nm]))
        else:
            note(slug, "data-embed '%s' (a live gallery) became a line linking to where it lives" % nm)
    body = re.sub(r'<div data-embed="([a-z-]+)"[^>]*>\s*</div>', lambda m: "\n\n" + embed_md(m.group(1)) + "\n\n", body)
    counter = [0]
    body = html_to_md(body, slug, counter)
    body = md_links(body)
    body = restore_code(body, keep)
    body = re.sub(r"\n{3,}", "\n\n", body)

    # lessons: the first # is the title (skipped); ## (or a later #) starts a lesson
    sections, head, buf, first_h1, fence = [], None, [], False, False
    for ln in body.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        hm = None if fence else re.match(r"^(#{1,2})\s+(.*\S)\s*$", ln)
        if hm:
            level, htext = len(hm.group(1)), hm.group(2).strip()
            if level == 1 and not first_h1:
                first_h1 = True
                if head is None:
                    head, buf = "Introduction", []
                continue
            if head is not None:
                sections.append((head, "\n".join(buf).strip()))
            head, buf = htext, []
        else:
            if head is None:
                head = "Introduction"
            buf.append(ln)
    if head is not None:
        sections.append((head, "\n".join(buf).strip()))

    nodes = []
    for i, (h, content) in enumerate(sections, 1):
        h_plain = re.sub(r"[*_`]", "", h)
        base = "lesson-%02d-%s" % (i, slugify(h_plain))
        parts = re.split(r"\s*@@VIDEO@@([A-Za-z0-9_-]{11})@@(.*?)@@\s*", content)
        text0, rest = parts[0].strip(), parts[1:]
        if text0 or not rest:
            if text0:
                nodes.append({"id": base, "name": h_plain, "category": "lesson", "keywords": [], "sections": {"Content": text0}})
        v = 0
        while rest:
            vid, title, after = rest[0], rest[1].strip(), rest[2].strip()
            rest = rest[3:]
            v += 1
            if not text0 and v == 1:
                name, nid = h_plain, base
            else:
                name = "%s — video%s" % (h_plain, "" if v == 1 else " %d" % v)
                nid = "%s-video%s" % (base, "" if v == 1 else "-%d" % v)
            content_v = ("*Video: %s*" % title if title else "") + ("\n\n" + after if after else "")
            node = {"id": nid, "name": name, "category": "lesson", "keywords": [],
                    "metadata": {"youtube_url": "https://www.youtube.com/watch?v=" + vid},
                    "sections": {"Content": content_v.strip() or "*Video*"}}
            nodes.append(node)

    listed = LISTED.get(cid) if not booklet else None
    draft = "draft" in str(fm.get("status", "")).lower()
    group, entry = listed if listed else (None, {})
    cover = ""
    if entry.get("deck"):
        cover = next((g.get("cover_image_url", "") for g in COLLECTION.get("grammars", []) if g["slug"] == entry["deck"]), "")
    elif entry.get("thumb"):
        cover = absolute(entry["thumb"])
    if not cover:
        cover = next((re.search(r"!\[[^\]]*\]\((https?://[^)\s]+\.(?:jpg|jpeg|png|webp))", n["sections"]["Content"], re.I).group(1)
                      for n in nodes if re.search(r"!\[[^\]]*\]\((https?://[^)\s]+\.(?:jpg|jpeg|png|webp))", n["sections"]["Content"], re.I)), "")

    out_path = os.path.join(ROOT, "tarot", slug, "grammar.json")
    old = {}
    if os.path.exists(out_path):
        old = json.load(io.open(out_path, encoding="utf-8"))
    name = fm.get("title") or old.get("name") or slug
    g = {
        "_grammar_commons": old.get("_grammar_commons") or {"schema_version": "1.0", "license": "CC-BY-SA-4.0",
            "attribution": [{"name": fm.get("author", "PlayfulProcess"), "note": "Course written as markdown, converted to a grammar once (Oct 2026)."}]},
        "name": name,
        "description": (fm.get("description") or old.get("description") or "").strip(),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "default_view": "play",
        "reading_mode_default": "continuous",
        "provenance": old.get("provenance", "reference"),
    }
    if cover:
        g["cover_image_url"] = cover
    tags = ["tarot", "course"] + (["booklet"] if booklet else []) + ([slugify(group)] if group else [])
    g["tags"] = tags
    if draft or not listed:
        g["import_visibility"] = "private"
    g["metadata"] = {"common_name": name, "category": "course"}
    # The validator refuses a pull request that drops a top-level field the file had, so the old
    # stamps stay, saying what is true now. `_generated: false` lets the sync import the grammar.
    if "_generated" in old:
        g["_generated"] = False
    if "_built_by" in old:
        g["_built_by"] = "Converted once from %s on 2026-10-23; this file is the source now (edit it, or the grammar in recursive.eco)." % src_rel
    if "_source_mdx" in old:
        g["_source_mdx"] = "%s (retired; in the repository's history)" % src_rel
    g["nodes"] = nodes
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    json.dump(g, io.open(out_path, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
    io.open(out_path, "a", encoding="utf-8", newline="\n").write("\n")
    vis = "Private" if g.get("import_visibility") == "private" else "Published"
    why = ("draft" if draft else "not on the course index") if vis == "Private" else ""
    print("%-58s %3d nodes  %-9s %s" % ("tarot/%s" % slug, len(nodes), vis, why))
    return slug, vis, why


def main():
    results = []
    for f in sorted(os.listdir(os.path.join(ROOT, "course"))):
        if f.endswith(".mdx"):
            cid = f[:-4]
            slug = "how-to-contribute" if cid == "how-to-contribute" else cid + "-course"
            results.append(convert("course/" + f, slug))
    for f in sorted(os.listdir(os.path.join(ROOT, "course", "booklets"))):
        if f.endswith(".mdx"):
            results.append(convert("course/booklets/" + f, f[:-4] + "-booklet", booklet=True))
    print("\n%d converted" % len(results))
    print("\nSimplified:")
    for s, notes in LOSSY.items():
        for n in notes:
            print("  %s: %s" % (s, n))


if __name__ == "__main__":
    main()
