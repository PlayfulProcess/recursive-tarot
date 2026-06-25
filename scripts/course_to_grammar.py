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

    items = []
    for i, (h, content) in enumerate(sections, 1):
        if not content and not h:
            continue
        items.append({
            "id": "lesson-%02d-%s" % (i, slugify(h)),
            "name": h,
            "category": "lesson",
            "keywords": [],
            "sections": {"Content": content},
        })

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
