# -*- coding: utf-8 -*-
"""Two source-level fixes (run once):
  1. Repo-relative research pointers (`research/.../x.md`) render as dead text / 404s.
     Convert them to real GitHub blob links so they resolve and open in a new tab.
  2. Items whose note says "(vs. its parent)" but carry no cross-link pill: add the
     sanctioned source_deck/source_item_id/deck pill pointing at the Marseille card
     the note explicitly compares to (resolved by trump_key, then archetype).
Only the Marseille-comparison decks are touched for (2); every note in them names
"the Marseille …" as the referent, so the link points at exactly what the text cites.
"""
import json, os, re, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TAROT = os.path.join(ROOT, "tarot")
BLOB = "https://github.com/PlayfulProcess/recursive-tarot/blob/dev/"
PARENT_DECKS = ["paris-anonymous-tarot", "tarot-de-besancon", "tarocchino-bologna"]

# Marseille Conver: the parent the "vs. its parent" notes compare against.
mc = json.load(open(os.path.join(TAROT, "tarot-de-marseille-conver", "grammar.json"), encoding="utf-8"))
tk2id, arch2id = {}, {}
for it in mc["items"]:
    md = it.get("metadata") or {}
    if md.get("trump_key"):
        tk2id[md["trump_key"]] = it["id"]
    if md.get("archetype"):
        arch2id[md["archetype"]] = it["id"]

def fix_research_links(text):
    # backtick-wrapped first, then any remaining bare path (not already inside a link)
    text = re.sub(r"`(research/[^`\s]+\.md)`",
                  lambda m: "[%s](%s%s)" % (m.group(1), BLOB, m.group(1)), text)
    # bare paths only — never inside an existing [link](...) or `code` (exclude [ ( / \w ` before, ] ) after)
    text = re.sub(r"(?<![\[\(/\w`])(research/[a-z]+/[a-z0-9._-]+\.md)\b(?![)\]])",
                  lambda m: "[%s](%s%s)" % (m.group(1), BLOB, m.group(1)), text)
    return text

links_fixed = 0
pills_added = 0
unresolved = []

for f in glob.glob(os.path.join(TAROT, "*", "grammar.json")):
    slug = os.path.basename(os.path.dirname(f))
    if slug in ("all-decks-many-lenses", "people-of-tarot"):
        continue
    g = json.load(open(f, encoding="utf-8"))
    changed = False

    # (1) research links — everywhere (description + sections), all decks
    if isinstance(g.get("description"), str):
        nd = fix_research_links(g["description"])
        if nd != g["description"]:
            g["description"] = nd; changed = True; links_fixed += 1
    for it in g.get("items", []):
        secs = it.get("sections") or {}
        for k, v in list(secs.items()):
            if isinstance(v, str) and "research/" in v and ".md" in v:
                nv = fix_research_links(v)
                if nv != v:
                    secs[k] = nv; changed = True; links_fixed += 1

    # (2) parent pill — only the Marseille-comparison decks, only orphans
    if slug in PARENT_DECKS:
        for it in g.get("items", []):
            md = it.get("metadata") or {}
            if md.get("source_deck"):
                continue
            if not any("vs. its parent" in str(v) for v in (it.get("sections") or {}).values()):
                continue
            pid = tk2id.get(md.get("trump_key")) or arch2id.get(md.get("archetype"))
            if not pid:
                unresolved.append("%s/%s" % (slug, it["id"]))
                continue
            md["source_deck"] = "tarot-de-marseille-conver"
            md["source_item_id"] = pid
            md["deck"] = "Tarot de Marseille"
            it["metadata"] = md
            changed = True; pills_added += 1

    if changed:
        json.dump(g, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        open(f, "a", encoding="utf-8").write("\n")

print("research links fixed in %d strings; parent pills added: %d" % (links_fixed, pills_added))
if unresolved:
    print("UNRESOLVED parents (left as-is):", unresolved)
