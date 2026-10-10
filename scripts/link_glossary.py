# -*- coding: utf-8 -*-
"""The glossary link layer: wiki-style links, written into the texts as content.

  python scripts/link_glossary.py           # rewrite the links (idempotent)
  python scripts/link_glossary.py --check   # write nothing; exit 1 if anything is out of date

PlayfulProcess, Oct 8 2026: "Like wikipedia, everything that has a page is hyperlinked, like what
is Ma'at?" The glossary lives in `tarot/glossary-of-tarot/grammar.json` (one item per term, edited
by hand) and renders at pages/glossary.html#<term>; the Tree of Life map is
pages/tree-of-life.html?path=NN.

What it does, per SECTION (a grammar section, or a heading-to-heading stretch of a course):
  * the first "Path NN" (11-32) for each NN links to the map: tree-of-life.html?path=NN;
  * the first mention of each glossary term (its `metadata.aliases`, case-sensitive, whole
    words) links to its entry;
  * on each Golden Dawn trump, the `Correspondences` section gets one added line, "On the Tree",
    naming the two sephiroth its path joins (from the glossary's `metadata.tree_paths`).
Links are absolute (https://tarot.recursive.eco/pages/...) so they travel with the grammar to
recursive.eco.

What it never touches: quoted source text. In the Golden Dawn deck only the editorial sections
in EDITORIAL below are linked; `Book T (1912)`, `Golden Dawn Title`, Waite, Papus and the
research notes are left as they are. Inside any text it skips blockquotes, headings, anything in
quotation marks, existing links, code, HTML, and bold labels like "**Hebrew letter:**".

Re-running first removes every link this script made (any link to the glossary or the map) and
the "On the Tree" line, then adds them again, so a change to the glossary propagates. Do not hand-add
links to those two pages in these files: they will be normalised on the next run.

Files: tarot/golden-dawn-book-t-tarot/grammar.json, course/walking-the-golden-dawn-path.mdx (then
its generated grammar is rebuilt with scripts/course_to_grammar.py), and
course/golden-dawn-dignities-not-reversals.mdx.
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GLOSSARY = os.path.join(ROOT, "tarot", "glossary-of-tarot", "grammar.json")
DECK = os.path.join(ROOT, "tarot", "golden-dawn-book-t-tarot", "grammar.json")
COURSES = [  # (mdx id, generated grammar slug or None, grammar name)
    ("walking-the-golden-dawn-path", "walking-the-golden-dawn-path-course", "The Golden Dawn — the Map and the Walk"),
    ("golden-dawn-dignities-not-reversals", None, None),
]
EDITORIAL = ("Correspondences", "Astrological attribution (Book T)", "About the Keys", "About the Decans",
             "About this Suit", "How to Use")

PAGES = "https://tarot.recursive.eco/pages/"
GLOSS = PAGES + "glossary.html#"
TREE = PAGES + "tree-of-life.html?path="
OURS = re.compile(r"\[([^\]]+)\]\(" + re.escape(PAGES)
                  + r"(?:glossary\.html#[a-z0-9-]+|tree-of-life\.html\?path=\d+)\)")
ON_TREE = "**On the Tree:**"
ON_TREE_RE = re.compile(r"\n\n" + re.escape(ON_TREE) + r"[^\n]*")

# Spans the linker must not write into. Order matters only for readability.
PROTECT = re.compile("|".join([
    r"!?\[[^\]]*\]\([^)]*\)",            # markdown links and images
    r"`[^`]*`",                           # code
    r"<[^>]+>",                           # HTML tags
    r"https?://[^\s)>\]]+",               # bare URLs
    r"\"[^\"\n]*\"",                      # "quoted"
    r"“[^”\n]*”",                         # “quoted”
    r"\*\*[^*\n]+:\*\*",                  # **Label:**
    r"\[@[^\]]*\]",                       # [@citation]
]))
PATH_RE = re.compile(r"(?<![\w-])([Pp]ath) (1[1-9]|2\d|3[0-2])(?![\w-])")


def load_terms():
    g = json.load(open(GLOSSARY, encoding="utf-8"))
    terms, seen, errors = [], {}, []
    for it in g["nodes"]:
        secs = it.get("sections") or {}
        if not secs.get("Entry") or not secs.get("Sources"):
            errors.append(f"glossary: '{it.get('id')}' needs an Entry and Sources section")
        if not re.fullmatch(r"[a-z0-9-]+", it.get("id", "")):
            errors.append(f"glossary: bad id {it.get('id')!r}")
        for a in (it.get("metadata") or {}).get("aliases", []):
            if a in seen:
                errors.append(f"glossary: alias {a!r} is on both '{seen[a]}' and '{it['id']}'")
            seen[a] = it["id"]
            terms.append((a, it["id"]))
    # Longest first, so "Tree of Life" wins over a shorter alias inside it.
    terms.sort(key=lambda t: -len(t[0]))
    tree_paths = {int(k): v for k, v in (g.get("metadata") or {}).get("tree_paths", {}).items()}
    names = {it["id"]: (it["metadata"]["aliases"] or [it["name"]])[0] for it in g["nodes"]}
    return terms, tree_paths, names, {it["id"] for it in g["nodes"]}, errors


def segments(text):
    """Split one line of prose into [(text, free?)]."""
    out, i = [], 0
    for m in PROTECT.finditer(text):
        if m.start() > i:
            out.append([text[i:m.start()], True])
        out.append([m.group(0), False])
        i = m.end()
    if i < len(text):
        out.append([text[i:], True])
    return out


def link_first(segs, pattern, make):
    """Link the first match of `pattern` in a free segment. Returns True if linked."""
    for k, (s, free) in enumerate(segs):
        if not free:
            continue
        m = pattern.search(s)
        if m:
            segs[k:k + 1] = [[s[:m.start()], True], [make(m), False], [s[m.end():], True]]
            return True
    return False


class Section:
    """First-mention bookkeeping for one section."""
    def __init__(self, terms):
        self.terms, self.done_terms, self.done_paths = terms, set(), set()

    def link_line(self, line):
        segs = segments(line)
        # Path NN, first per number
        while True:
            hit = None
            for k, (s, free) in enumerate(segs):
                if free:
                    for m in PATH_RE.finditer(s):
                        if m.group(2) not in self.done_paths:
                            hit = (k, m)
                            break
                if hit:
                    break
            if not hit:
                break
            k, m = hit
            s = segs[k][0]
            self.done_paths.add(m.group(2))
            segs[k:k + 1] = [[s[:m.start()], True], [f"[{m.group(0)}]({TREE}{m.group(2)})", False],
                             [s[m.end():], True]]
        for alias, slug in self.terms:
            if slug in self.done_terms:
                continue
            pat = re.compile(r"(?<![\w'’-])" + re.escape(alias) + r"(?![\w'’-])"
                             + (r"" if alias not in ("Sun", "Moon") else ""))
            if alias in ("Sun", "Moon"):
                pat = re.compile(r"(?<!The )(?<![\w'’-])" + re.escape(alias) + r"(?![\w'’-])")
            if link_first(segs, pat, lambda m, slug=slug: f"[{m.group(0)}]({GLOSS}{slug})"):
                self.done_terms.add(slug)
        return "".join(s for s, _ in segs)


def unlink(text):
    return OURS.sub(r"\1", ON_TREE_RE.sub("", text))


def link_prose(text, terms):
    """Link a grammar section (one section, plain markdown)."""
    sec = Section(terms)
    out = []
    for line in unlink(text).split("\n"):
        if re.match(r"\s*(#|>)", line):
            out.append(line)
        else:
            out.append(sec.link_line(line))
    return "\n".join(out)


def link_mdx(text, terms):
    """Link a course: a new section at every heading; skip frontmatter, quotes, HTML blocks."""
    text = unlink(text)
    lines, out = text.split("\n"), []
    sec, in_fm, in_html, in_code = Section(terms), False, False, False
    for n, line in enumerate(lines):
        if n == 0 and line.strip() == "---":
            in_fm = True
            out.append(line)
            continue
        if in_fm:
            out.append(line)
            if line.strip() == "---":
                in_fm = False
            continue
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        if re.match(r"#{1,6} ", line):
            sec = Section(terms)
            out.append(line)
            continue
        if line.lstrip().startswith("<") or in_html:
            # an HTML block (figure, style, div) runs to the next blank line
            in_html = bool(line.strip())
            out.append(line)
            continue
        if re.match(r"\s*>", line):
            out.append(line)
            continue
        out.append(sec.link_line(line))
    return "\n".join(out)


def on_tree_line(path, tree_paths, names):
    a, b = tree_paths[path]
    return (f"{ON_TREE} path {path} joins [{names[a]}]({GLOSS}{a}) and [{names[b]}]({GLOSS}{b}) · "
            f"[see it on the map]({TREE}{path})")


def link_deck(deck, terms, tree_paths, names):
    changed = 0
    for it in deck["nodes"]:
        secs = it.get("sections") or {}
        for key in EDITORIAL:
            v = secs.get(key)
            if not isinstance(v, str):
                continue
            new = link_prose(v, terms)
            path = (it.get("metadata") or {}).get("tree_path")
            if key == "Correspondences" and it.get("category") == "major-arcana" and path in tree_paths:
                paras = new.split("\n\n")
                paras.insert(1, on_tree_line(path, tree_paths, names))
                new = "\n\n".join(paras)
            if new != v:
                secs[key] = new
                changed += 1
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    terms, tree_paths, names, slugs, errors = load_terms()
    if sorted(tree_paths) != list(range(11, 33)) or any(s not in slugs for ab in tree_paths.values() for s in ab):
        errors.append("glossary: metadata.tree_paths must map 11..32 to two sephirah ids each")
    pending = []

    raw = open(DECK, encoding="utf-8").read()
    deck = json.loads(raw)
    n = link_deck(deck, terms, tree_paths, names)
    out = json.dumps(deck, ensure_ascii=False, indent=2)
    if out != raw:
        pending.append(f"{os.path.relpath(DECK, ROOT)} ({n} sections)")
        if not args.check:
            open(DECK, "w", encoding="utf-8", newline="\n").write(out)

    for mdx_id, slug, name in COURSES:
        p = os.path.join(ROOT, "course", mdx_id + ".mdx")
        src = open(p, encoding="utf-8").read()
        new = link_mdx(src, terms)
        if new != src:
            pending.append(os.path.relpath(p, ROOT))
            if not args.check:
                open(p, "w", encoding="utf-8", newline="\n").write(new)
        if slug and not args.check:
            r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "course_to_grammar.py"), mdx_id, slug, name],
                               capture_output=True, text=True, cwd=ROOT)
            if r.returncode:
                errors.append(f"course_to_grammar {mdx_id} failed: {r.stderr.strip()[-300:]}")
        elif slug:
            # the generated course grammar must carry the same links as its source
            g = json.load(open(os.path.join(ROOT, "tarot", slug, "grammar.json"), encoding="utf-8"))
            body = "\n".join((it.get("sections") or {}).get("Content", "") for it in g["nodes"])
            for m in OURS.finditer(new):
                if m.group(0) not in body:
                    pending.append(f"tarot/{slug}/grammar.json (rebuild from {mdx_id}.mdx)")
                    break

    for e in errors:
        print("ERROR:", e)
    if args.check:
        if pending:
            print("[link_glossary] --check: out of date: " + "; ".join(pending)
                  + "\n  run: python scripts/link_glossary.py")
        else:
            print("[link_glossary] --check: up to date (%d terms)" % len(terms))
        sys.exit(1 if (pending or errors) else 0)
    print("[link_glossary] " + ("updated: " + "; ".join(pending) if pending else "nothing to change")
          + " (%d terms)" % len(terms))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
