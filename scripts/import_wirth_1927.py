"""Write Oswald Wirth's own 1927 text onto the 22 cards of the Wirth deck.

Source: research/sources/wirth-imagiers-1927.json (French transcribed from the
BnF copy of *Le Tarot des imagiers du Moyen Age*, Paris 1927, on Gallica, with
page numbers and this site's English translation).

For each card it sets two sections:
  - "Wirth"                              the opening of Wirth's chapter on the card
  - "Divinatory meanings (Wirth, 1927)"  his "Interpretations divinatoires",
                                         replacing the old editorial "Upright" line
and in "Correspondences" adds Wirth's own constellations (his table, p. 76) and
labels the older "Astrological association" line as editorial.

Idempotent. `--check` exits 1 if the grammar differs from what it would write.

    python scripts/import_wirth_1927.py
    python scripts/import_wirth_1927.py --check
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "research" / "sources" / "wirth-imagiers-1927.json"
GRAMMAR = ROOT / "tarot" / "oswald-wirth-tarot" / "grammar.json"

DIV_KEY = "Divinatory meanings (Wirth, 1927)"
OLD_KEY = "Upright"
WIRTH_KEY = "Wirth"

BOOK = "*Le Tarot des imagiers du Moyen Âge* (Paris: Le Symbolisme / Émile Nourry, 1927)"
SCAN = "[BnF copy on Gallica](https://gallica.bnf.fr/ark:/12148/bpt6k3112874)"


def pages(p):
    return ("pp. " if "-" in p or "," in p else "p. ") + p.replace("-", "–")


def quote(fr):
    return "\n>\n".join("> " + para for para in fr.split("\n\n"))


def wirth_section(c):
    head = (f"*Wirth in his own words:* {BOOK}, chapter {c['chapter']}, {pages(c['open_pages'])} · "
            f"public domain · French from the {SCAN} · the English below is this site's translation")
    return f"{head}\n\n{quote(c['open_fr'])}\n\n**This site's translation**\n\n{c['open_en']}"


def div_section(c):
    head = (f"*Wirth's Interprétations divinatoires:* {BOOK}, {pages(c['div_pages'])} · public domain · "
            f"French from the {SCAN} · the English below is this site's translation. Wirth runs each card from "
            f"its highest sense down to its failings (\"Partant du ciel, nous aboutissons à l'enfer\", p. 100) "
            f"and gives no reversed meanings.")
    fr = "\n>\n".join("> " + p for p in c["div_fr"])
    en = "\n\n".join(c["div_en"])
    return f"{head}\n\n{fr}\n\n**This site's translation**\n\n{en}"


ASTRO_OLD = "**Astrological association:**"
ASTRO_NEW = "**Astrological association (editorial, not Wirth's; partly from later systems):**"
SKY_TAG = "**Wirth's constellations**"


def correspondences(text, c):
    text = text.replace(ASTRO_OLD, ASTRO_NEW)
    paras = [p for p in text.split("\n\n") if not p.startswith(SKY_TAG)]
    sky = (f"{SKY_TAG} (his table, *Le Tarot des imagiers*, 1927, p. 76): {c['sky_fr']} "
           f"({c['sky_en']}).")
    return "\n\n".join(paras + [sky])


def apply(g, cards):
    by_id = {it["id"]: it for it in g["nodes"]}
    for c in cards:
        it = by_id[c["id"]]
        old = it.get("sections", {})
        new = {}
        for k, v in old.items():
            if k in (OLD_KEY, DIV_KEY):
                new[DIV_KEY] = div_section(c)
            elif k == WIRTH_KEY:
                new[WIRTH_KEY] = wirth_section(c)
            elif k == "Correspondences":
                new[k] = correspondences(v, c)
            else:
                new[k] = v
        if DIV_KEY not in new:
            new[DIV_KEY] = div_section(c)
        if WIRTH_KEY not in new:
            new[WIRTH_KEY] = wirth_section(c)
        it["sections"] = new
    return g


def main():
    check = "--check" in sys.argv
    src = json.loads(SRC.read_text(encoding="utf-8"))
    cards = src["cards"]
    assert len(cards) == 22, len(cards)
    before = GRAMMAR.read_text(encoding="utf-8")
    g = json.loads(before)
    g = apply(g, cards)
    after = json.dumps(g, ensure_ascii=False, indent=2) + "\n"
    if check:
        ok = json.loads(before) == json.loads(after)
        print("wirth 1927: in sync" if ok else "wirth 1927: grammar differs from source; run without --check")
        sys.exit(0 if ok else 1)
    GRAMMAR.write_text(after, encoding="utf-8")
    print(f"wirth 1927: wrote {len(cards)} cards")


if __name__ == "__main__":
    main()
