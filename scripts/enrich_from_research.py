# -*- coding: utf-8 -*-
"""Phase 0+1: fold the rich research/<deck>.mdx essays into each deck's grammar.json
`description` (At a glance / Origin / Provenance / Game-or-divination / The fear question /
Counter-voices / Sources). Supersedes the generic block added by add_history_sources.py.
Idempotent (re-runnable). Run from repo root:
    python scripts/enrich_from_research.py
"""
import json, os, re

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
RESEARCH = os.path.join(ROOT, "research")
TAROT = os.path.join(ROOT, "tarot")

# No AI/Forum disclaimer is injected into grammars anymore — the authorship + AI disclosure
# lives once on the About page, and the Tarot History Forum is credited only inside "Sources"
# lists, never as a reviewer/guarantor (they are not responsible for this catalogue's errors).
FOOTER = ""

# deck slug -> research file
MAP = {
 "visconti-sforza-tarot":          "01-visconti-sforza.mdx",
 "cary-yale-visconti-tarot":       "02-cary-yale-visconti.mdx",
 "charles-vi-tarot":               "03-charles-vi-gringonneur.mdx",
 "mantegna-tarocchi":              "04-mantegna-tarocchi.mdx",
 "minchiate-florence-tarot":       "06-minchiate.mdx",
 "tarocchino-bologna":             "07-tarocchino-bologna.mdx",
 "tarot-de-marseille-conver":      "08-tarot-de-marseille.mdx",
 "court-de-gebelin-tarot":         "09-court-de-gebelin.mdx",
 "etteilla-i-livre-de-thot":       "10a-etteilla-i-livre-de-thot.mdx",
 "etteilla-ii-egyptian":           "10b-etteilla-ii.mdx",
 "etteilla-iii-oracle-des-dames":  "10c-etteilla-iii-oracle-des-dames.mdx",
 "oswald-wirth-tarot":             "11-oswald-wirth.mdx",
 "golden-dawn-book-t-tarot":       "12-golden-dawn-book-t.mdx",
 "tarot-de-besancon":              "15-besancon-1jj.mdx",
}

def strip_frontmatter(text):
    m = re.match(r"^---\n.*?\n---\n", text, flags=re.DOTALL)
    return text[m.end():] if m else text

changed = 0
for slug, fname in MAP.items():
    gpath = os.path.join(TAROT, slug, "grammar.json")
    rpath = os.path.join(RESEARCH, fname)
    if not os.path.exists(gpath):
        print("  ! missing grammar:", slug); continue
    if not os.path.exists(rpath):
        print("  ! missing research:", fname); continue
    body = strip_frontmatter(open(rpath, encoding="utf-8").read()).strip()
    g = json.load(open(gpath, encoding="utf-8"))
    g["description"] = body + FOOTER
    g["_enriched_from"] = f"research/{fname}"
    json.dump(g, open(gpath, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    changed += 1
    print(f"  + enriched {slug:32s} <- {fname}  ({len(body)} chars)")
print("decks enriched:", changed)
