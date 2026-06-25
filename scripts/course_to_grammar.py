# -*- coding: utf-8 -*-
"""Convert a markdown course (course/<id>.mdx) into a GRAMMAR — so a course can enter
the same grammar flow as everything else (editor, viewers, fork/publish), and render
back out as a course via viewers/grammar-course.html.

Mapping: each top-level heading (## or a later #) becomes one ITEM (a lesson); the
markdown under it becomes that item's `Content` section. The course's first # heading
is its title (skipped); the prose before the first ## becomes an "Introduction" lesson.
Frontmatter `title`/`description` seed the grammar name/description.

Run:  python scripts/course_to_grammar.py <mdx-id> <out-slug> "<Grammar Name>"
e.g.  python scripts/course_to_grammar.py history-of-tarot history-of-tarot-course "The History of Tarot — a Course"
"""
import re, json, io, os, sys
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")[:40] or "x"

# Named card galleries baked from <div data-embed="NAME"> into item.metadata.embeds —
# references the renderer resolves to images (deck slug + ref `tk:<trump_key>` / `item:<id>`).
# A {"heading": ...} entry starts a sub-gallery. Mirrors the course-viewer's live galleries.
PLATES_EMBEDS = [
    {"heading": "One card across the centuries — Death"},
    {"deck": "visconti-sforza-tarot", "ref": "tk:death", "caption": "Death — Visconti-Sforza, Milan, c. 1451. The earliest clear tarot Death: a white skeleton standing frontally on a gold ground, holding a bow and arrow."},
    {"deck": "tarot-de-marseille-conver", "ref": "tk:death", "caption": "Death — Tarot de Marseille (Conver), 1760. Three centuries on, the same skeleton now mows a field of severed body parts with a scythe — and the card is left pointedly untitled."},
    {"deck": "golden-dawn-book-t-tarot", "ref": "tk:death", "caption": "Death — Rider-Waite-Smith line, 1909. The skeleton survives the whole journey but is restaged once more: an armoured rider on a pale horse beneath a rising sun."},
    {"heading": "Continuity & diversity — a few iconic cards"},
    {"deck": "visconti-sforza-tarot", "ref": "tk:fool", "caption": "The Fool — Visconti-Sforza, c. 1451. A ragged wanderer; the figure scarcely changes for five centuries."},
    {"deck": "tarot-de-marseille-conver", "ref": "tk:fool", "caption": "Le Mat — Marseille (Conver), 1760. The same vagabond and his nipping dog, now in woodcut."},
    {"deck": "golden-dawn-book-t-tarot", "ref": "tk:fool", "caption": "The Fool — Rider-Waite-Smith line, 1909. Still the wanderer, stepping off a cliff into the modern deck."},
    {"deck": "mamluk-deck", "ref": "item:cups-king", "caption": "Mamluk card, 14th–15th c. Egypt/Syria — the four-suit ancestor that reached Europe in the 1370s."},
    {"deck": "sola-busca-tarot", "ref": "item:cups-05", "caption": "Sola Busca, 1491 — the first deck to give every numbered pip a figured scene, four centuries before the RWS."},
    {"deck": "mantegna-tarocchi", "ref": "item:plate-01", "caption": "The “Mantegna Tarocchi”, c. 1465 — a humanist set of ranks and virtues, not a tarot at all: a cousin, not a parent."},
    {"deck": "visconti-sforza-tarot", "ref": "tk:world", "caption": "The World — Visconti-Sforza, c. 1451. Tooled gold leaf for a ducal court: tarot began as luxury, not occultism."},
    {"deck": "tarot-de-marseille-conver", "ref": "tk:moon", "caption": "The Moon — Marseille, 1760. The uncanny scene of towers, dogs, and crayfish the occultists inherited whole."},
]
EMBEDS = {"plates": PLATES_EMBEDS}  # add decks/suits/trumps/etc. here to bake the rest

def _expand_essay():
    """<div data-embed="essay"> → the meta-grammar's 'Divination Question' essay, baked as
    markdown into the lesson (it's text, so we inline it; the card galleries are different —
    they're computed aggregations and belong in the renderer, not baked here)."""
    p = os.path.join(ROOT, "tarot", "all-decks-many-lenses", "grammar.json")
    try:
        mg = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        return ""
    e = next((i for i in mg.get("items", []) if i.get("id") == "essay-divination-question"), None)
    if not e:
        return ""
    return "\n\n".join("### " + k + "\n\n" + str(v) for k, v in (e.get("sections") or {}).items())

def convert(mdx_id, out_slug, name=None):
    src = os.path.join(ROOT, "course", mdx_id + ".mdx")
    text = io.open(src, encoding="utf-8").read()

    fm, body = {}, text
    m = re.match(r"^﻿?---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        fm = yaml.safe_load(m.group(1)) or {}
        body = text[m.end():]

    # Walk lines, grouping content under the current top-level heading (# or ##).
    sections, head, buf, first_h1 = [], None, [], False
    for ln in body.split("\n"):
        hm = re.match(r"^(#{1,2})\s+(.*\S)\s*$", ln)
        if hm:
            level, htext = len(hm.group(1)), hm.group(2).strip()
            if level == 1 and not first_h1:
                first_h1 = True            # the course title — skip; start the intro
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

    essay_md = _expand_essay()
    items = []
    for i, (h, content) in enumerate(sections, 1):
        # Bake known <div data-embed="NAME"> galleries into item.metadata.embeds (card
        # references the renderer resolves); inline the essay text; strip the rest.
        meta = {}
        for nm in set(re.findall(r'data-embed="([a-z-]+)"', content)):
            if nm in EMBEDS:
                meta["embeds"] = EMBEDS[nm]
        if essay_md and 'data-embed="essay"' in content:
            content = content.replace('<div data-embed="essay"></div>', essay_md)
        # plates → baked to metadata.embeds; essay → inlined above; strip only those two.
        # KEEP the computed-aggregation markers (decks/suits/numbers/trumps-*/suits-detail/
        # lineage/timeline/people/apparatus/card) inline in the prose — grammar-course expands
        # them live via course-embeds.js, the SAME shared expander the MDX course-viewer uses,
        # so the grammar renders the whole course at parity.
        content = re.sub(r'\s*<div data-embed="plates"[^>]*></div>\s*', "\n\n", content).strip()
        if not content and not meta:
            continue
        it = {
            "id": "lesson-%02d-%s" % (i, slugify(h)),
            "name": h, "category": "lesson", "keywords": [],
            "sections": {"Content": content},
        }
        if meta:
            it["metadata"] = meta
        items.append(it)

    grammar = {
        "_grammar_commons": {"schema_version": "1.0", "license": "CC-BY-SA-4.0",
            "attribution": [{"name": fm.get("author", "PlayfulProcess"),
                             "note": "Course converted from markdown to a grammar."}]},
        "name": name or fm.get("title") or out_slug,
        "description": (fm.get("description") or "").strip(),
        "grammar_type": "custom",
        "creator_name": "PlayfulProcess",
        "default_view": "course",
        "provenance": "reference",
        "metadata": {"common_name": name or fm.get("title") or out_slug, "category": "reference",
                     "source_mdx": "course/%s.mdx" % mdx_id},
        "_generated": True, "_built_by": "scripts/course_to_grammar.py",
        "_source_mdx": "course/%s.mdx" % mdx_id,
        "items": items,
    }
    out_dir = os.path.join(ROOT, "tarot", out_slug)
    os.makedirs(out_dir, exist_ok=True)
    json.dump(grammar, io.open(os.path.join(out_dir, "grammar.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    print("wrote tarot/%s/grammar.json — %d lessons" % (out_slug, len(items)))
    for it in items:
        print("   · %s (%d chars)" % (it["name"][:50], len(it["sections"]["Content"])))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    convert(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
