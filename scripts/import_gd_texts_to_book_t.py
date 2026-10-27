"""Write other public-domain Golden Dawn texts onto the Book T deck's cards.

PlayfulProcess, Oct 18 2026: "Let's add other pd golden dawn texts to book t." Book T itself says
little on the twenty-two Keys (one line each), so a Key's card read thin. Two writers from inside
the Order's line, both already transcribed in this repo, now sit beside Book T's own words, each in
its own section, each saying whose words they are and what they describe:

  "Waite (1911)"  A. E. Waite, a member of the Golden Dawn, The Pictorial Key to the Tarot
                  (London, 1911): his text for the same card, matched by archetype, from
                  tarot/rider-waite-smith-pictorial-key ("The Pictorial Key"). He describes the
                  Rider-Waite-Smith picture, not Book T's; the section says so. All 78 cards.
  "Case (1920)"   Paul Foster Case, An Introduction to the Study of the Tarot (New York, 1920),
                  Chapter III: his entry for the Key's Hebrew letter, from
                  course/booklets/case-introduction-to-the-study-of-the-tarot-1920.mdx. The 22
                  Keys. The booklet's caveat on Lamed and Nun (a later editor changed their
                  directions) rides along on those two.

Not here yet: Mathers, The Tarot (London, 1888). No scan was found from a source this script can
cite (Oct 18 2026); it joins when one is in research/sources.

The labels are long on purpose (Oct 18 2026): recursive.eco keeps a node's sections in a database
object, which orders keys shortest first, and Play draws them in that order; at 27 and 38 characters
these two sort after Book T's own three (13, 15, 17). Until the app keeps an order of its own
(recursive-eco CLEANUP-FINDINGS-2026-10), a shorter label here would draw above Book T's words.

Book T's own section is never touched; build_book_t_deck.py keeps sections it does not own.
Idempotent. `--check` exits 1 if the grammar differs from what it would write.

    python scripts/import_gd_texts_to_book_t.py
    python scripts/import_gd_texts_to_book_t.py --check
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK_T = ROOT / "tarot" / "book-t" / "grammar.json"
RWS = ROOT / "tarot" / "rider-waite-smith-pictorial-key" / "grammar.json"
CASE = ROOT / "course" / "booklets" / "case-introduction-to-the-study-of-the-tarot-1920.mdx"

WAITE_KEY = "Waite, Pictorial Key (1911)"
CASE_KEY = "Case, Introduction to the Tarot (1920)"
WAITE_HEAD = ("*A. E. Waite, a member of the Golden Dawn, in* The Pictorial Key to the Tarot *(London, 1911)"
              " · public domain · he describes the Rider-Waite-Smith picture of this card, not Book T's*")
CASE_HEAD = ("*Paul Foster Case, in* An Introduction to the Study of the Tarot *(New York, 1920), Chapter III,"
             " on the letter %s · public domain in the US · "
             "[the whole booklet](https://recursive.eco/play?id=2b99b34f-7c83-411b-9430-2a7376bb8134&pane=continuous)*")
CASE_CAVEAT = ("*(A later editor changed the direction Case gave this letter in 1920; see the booklet's note"
               " before quoting it.)*")
# Book T's transliteration → Case's heading.
CASE_NAME = {"Heh": "He"}


def case_letters():
    text = CASE.read_text(encoding="utf-8").replace("\r\n", "\n")
    start = text.index("## Chapter III")
    end = text.index("## Chapter IV")
    out = {}
    for m in re.finditer(r"^### (\S+)\n\n(.*?)(?=^### |\Z)", text[start:end], re.S | re.M):
        # The last letter carries the chapter's closing paragraph and a footnote: not Tau's.
        out[m.group(1)] = m.group(2).split("\n\nMemorize these attributions")[0].strip()
    return out


def waite_text(node):
    t = (node.get("sections") or {}).get("The Pictorial Key", "").strip()
    first, _, rest = t.partition("\n\n")
    # Drop his heading line (the card's name), kept by the card itself.
    if rest and len(first) < 60 and "." not in first:
        t = rest.strip()
    return t


def build():
    deck = json.loads(BOOK_T.read_text(encoding="utf-8"))
    rws = {(n.get("metadata") or {}).get("archetype"): n for n in json.loads(RWS.read_text(encoding="utf-8"))["nodes"]}
    letters = case_letters()
    missing = []
    for n in deck["nodes"]:
        meta = n.get("metadata") or {}
        arche = meta.get("archetype")
        if not arche:
            continue
        secs = n.setdefault("sections", {})
        w = rws.get(arche)
        body = waite_text(w) if w else ""
        if body:
            secs[WAITE_KEY] = WAITE_HEAD + "\n\n" + body
        else:
            missing.append(("waite", n["id"]))
        letter = meta.get("hebrew_translit")
        if letter:
            entry = letters.get(CASE_NAME.get(letter, letter))
            if entry:
                secs[CASE_KEY] = (CASE_HEAD % letter) + "\n\n" + entry + (("\n\n" + CASE_CAVEAT) if letter in ("Lamed", "Nun") else "")
            else:
                missing.append(("case", n["id"]))
    return deck, missing


def main():
    check = "--check" in sys.argv
    deck, missing = build()
    out = json.dumps(deck, ensure_ascii=False, indent=2) + "\n"
    cur = BOOK_T.read_text(encoding="utf-8")
    if missing:
        print("[import_gd_texts_to_book_t] missing:", missing)
        sys.exit(1)
    if check:
        same = cur == out
        print("[import_gd_texts_to_book_t] --check: %s" % ("up to date" if same else "out of date; run: python scripts/import_gd_texts_to_book_t.py"))
        sys.exit(0 if same else 1)
    if cur != out:
        BOOK_T.write_text(out, encoding="utf-8", newline="\n")
    n_w = sum(1 for n in deck["nodes"] if WAITE_KEY in (n.get("sections") or {}))
    n_c = sum(1 for n in deck["nodes"] if CASE_KEY in (n.get("sections") or {}))
    print("[import_gd_texts_to_book_t] %s: Waite on %d cards, Case on %d Keys" % ("written" if cur != out else "unchanged", n_w, n_c))


if __name__ == "__main__":
    main()
