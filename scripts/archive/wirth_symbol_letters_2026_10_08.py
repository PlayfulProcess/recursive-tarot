"""One-shot (Oct 8 2026): the Wirth deck's "Symbol" notes named Golden Dawn Hebrew letters.

Eleven Symbol notes (Wheel to Judgement) gave each card the Golden Dawn letter, one
step off from the card's own letter in Levi's scheme, which Wirth follows (his table,
Le Tarot des imagiers du Moyen Age, 1927, p. 76: Wheel = Yod, Strength = Kaph, Hanged
Man = Lamed, Death = Mem, ... Judgement = Resh). Those sentences are removed; the
Strength note is corrected; every Symbol note is labelled as editorial.

Idempotent. `--check` exits 1 if anything would change.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAMMAR = ROOT / "tarot" / "oswald-wirth-tarot" / "grammar.json"

LABEL = ("*Editorial note, not Wirth's words. Planet and zodiac links here come partly from later "
         "systems; Wirth's own letter and constellations are under Correspondences.*")

EDITS = {
    "arcanum-10-la-roue": [(" Kaph corresponds to Jupiter and the turning of fate.", "")],
    "arcanum-11-la-force": [(" Lamed corresponds to Libra; Wirth placed Strength at XI, reversing Justice and "
                             "Strength from some traditions.",
                             " Wirth keeps Strength at XI and Justice at VIII, as in the Marseille deck "
                             "(his table, 1927, p. 76).")],
    "arcanum-12-le-pendu": [(" Mem, the water letter, corresponds to water and the reversal of perspective.", "")],
    "arcanum-13-la-mort": [(" Nun corresponds to Scorpio and the regenerative power behind apparent endings.", "")],
    "arcanum-14-la-temperance": [(" Samech corresponds to Sagittarius.", "")],
    "arcanum-15-le-diable": [(" Ayin corresponds to Capricorn.", "")],
    "arcanum-16-la-maison-dieu": [(" Peh corresponds to Mars.", "")],
    "arcanum-17-les-etoiles": [(" Tzaddi corresponds to Aquarius.", "")],
    "arcanum-18-la-lune": [(" Qoph corresponds to Pisces.", "")],
    "arcanum-19-le-soleil": [(" Resh corresponds to the Sun.", "")],
    "arcanum-20-le-jugement": [(" Shin, the fire letter, corresponds to the element of fire and spiritual renewal.", "")],
}


def main():
    check = "--check" in sys.argv
    before = GRAMMAR.read_text(encoding="utf-8")
    g = json.loads(before)
    for it in g["nodes"]:
        if not it["id"].startswith("arcanum-"):
            continue
        s = it["sections"].get("Symbol")
        if s is None:
            continue
        for old, new in EDITS.get(it["id"], []):
            s = s.replace(old, new)
        if LABEL not in s:
            s = s.rstrip() + "\n\n" + LABEL
        it["sections"]["Symbol"] = s
    after = json.dumps(g, ensure_ascii=False, indent=2) + "\n"
    changed = json.loads(before) != json.loads(after)
    if check:
        print("wirth symbol letters: would change" if changed else "wirth symbol letters: in sync")
        sys.exit(1 if changed else 0)
    GRAMMAR.write_text(after, encoding="utf-8")
    print("wirth symbol letters: written" if changed else "wirth symbol letters: nothing to do")


if __name__ == "__main__":
    main()
