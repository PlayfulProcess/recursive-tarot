# -*- coding: utf-8 -*-
"""Repair the caret-class OCR character substitutions in `papus-tarot-des-bohemiens`.

  python3 scripts/fix_papus_ocr_substitutions.py [--check]

The 1896 Morton translation of *Le Tarot des Bohémiens* was scanned badly in
a handful of places, and the scanner substituted single characters rather
than whole words: `^` for `gh`/`g`, `>` for `l`, `<m` for `gn`, `P` for `F`,
`j` for `e`, `K` for `R`, `k` for `r`, `y` for `g`, `E` for `R`. The result is
words that are not words — `Li^ht`, `Ho>y`, `a^ain`, `si^ns`, `bj`, `OP`,
`Keflex`, `Pkudence`, `Judy ment`, `FOUETH`.

These are **mechanical character repairs, not editorial rewrites**: each one
restores a word the surrounding sentence already determines, and none changes
what Papus says. The list is an explicit allow-list — exact string in, exact
string out, one entry per fix, each asserted to occur exactly once in the
deck so a wrong match is impossible. The script never runs a pattern over the
corpus.

Three stray glyphs are deleted rather than corrected, because the text is
complete without them and there is nothing to restore them *to*: a `^` where
the printed page had a triangle symbol the same sentence names in words
("his body forms a triangle"), a `<` left dangling after an em-dash at the
end of a paragraph, and a stray capital `J` after a heading.

**Deliberately NOT touched** — these need interpretation, not repair, and are
listed in `LEFT_ALONE` below so the decision is on the record:

  * `(^ Kaph)` in `arcanum-08-la-justice` — the caret stands where a Hebrew
    letter should be, exactly as the `p` does in the neighbouring `(p He)`.
    Both are mis-scanned Hebrew glyphs; supplying כ and ה would be
    reconstruction, not repair.
  * `(Eesh)` in `arcanum-20-le-jugement` — the 20th Hebrew letter is Resh,
    and `scripts/clean_papus_sections.py`'s own docstring names this exact
    corruption ("'Resh' becomes 'Eesh'"). It is still a whole proper name,
    not a character slip, so it stays visible.
  * `eaçde` / `riodit` (arcanum-03), `iash` (arcanum-06), `Samedi` for Samech
    (arcanum-00, arcanum-15), `orran` (arcanum-17), `ail` for all
    (arcanum-01), the `**` and the leading `. ` in arcanum-21 — multi-letter
    garbling where more than one reading is defensible.

Every fix is logged verbatim, with its reason, to
`research/sources/papus-ocr-substitutions-papus-tarot-des-bohemiens.md`.

Nothing-lost proof: the deck's total word count is unchanged except for the
three deliberate deletions and `Judy ment` -> `Judgment` (two tokens becoming
one) — a delta of exactly 4, which the script asserts rather than assumes.
It also asserts that applying the reverse substitutions to the new text
reproduces the old text character for character.

Idempotent: re-running finds no target strings and writes nothing.
"""
import argparse, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DECK = "papus-tarot-des-bohemiens"
SECTION = "Le Tarot des Bohémiens"
GRAMMAR = os.path.join(ROOT, "tarot", DECK, "grammar.json")
LOG = os.path.join(ROOT, "research", "sources",
                   f"papus-ocr-substitutions-{DECK}.md")

CARET = "the scanner substituted a single character"

# (item id, exact string to find, replacement, reason)
FIXES = [
    # --- ^ / > / < : the caret class -------------------------------------
    ("arcanum-06-lamoureux", "which a^ain is", "which again is",
     f"{CARET}: `^` for `g` — 'a^ain' is not a word; the clause reads 'which again is but a lower form of itself'"),
    ("arcanum-08-la-justice", "Astral Li^ht.", "Astral Light.",
     f"{CARET}: `^` for `gh` — the Astral Light is Papus's own recurring term"),
    ("arcanum-15-le-diable", "the Ho>y Spirit", "the Holy Spirit",
     f"{CARET}: `>` for `l` — the same sentence contrasts it with the God of Evil"),
    ("arcanum-21-le-monde", "the si<m of si^ns", "the sign of signs",
     f"{CARET}: `<m` for `gn` and `^` for `gn` — Tau as 'the sign of signs', the phrase the paragraph is defining"),
    ("arcanum-04-lempereur", "forms a triangle ^. Domination",
     "forms a triangle. Domination",
     "stray glyph deleted: the printed page had a triangle symbol here, which the same sentence already names in words ('his body forms a triangle'); there is nothing to restore the caret to"),
    ("arcanum-17-les-etoiles", "following significations — <",
     "following significations —",
     "stray glyph deleted: an angle bracket left dangling after the em-dash that ends the paragraph"),

    # --- P for F ----------------------------------------------------------
    ("arcanum-10-la-roue", "ORIGIN OP THE SYMBOLISM", "ORIGIN OF THE SYMBOLISM",
     f"{CARET}: `P` for `F` — the other 21 items read 'ORIGIN OF THE SYMBOLISM'"),
    ("arcanum-15-le-diable", "SYMBOLISM OP THE", "SYMBOLISM OF THE",
     f"{CARET}: `P` for `F` — the other 21 items read 'SYMBOLISM OF THE'"),

    # --- j for e ----------------------------------------------------------
    ("arcanum-01-le-bateleur", "will bj found", "will be found",
     f"{CARET}: `j` for `e`"),

    # --- stray characters inside or after a word --------------------------
    ("arcanum-20-le-jugement", "ORIGIN7 OF THE", "ORIGIN OF THE",
     "stray digit inside the word — the other 21 items read 'ORIGIN OF THE'"),
    ("arcanum-15-le-diable", "FIFTEENTH CARD OF J", "FIFTEENTH CARD OF",
     "stray capital after the heading, which the scan truncated at 'CARD OF' on ten items"),

    # --- E / K / k / y for R / g -----------------------------------------
    ("arcanum-04-lempereur", "THE FOUETH CARD", "THE FOURTH CARD",
     f"{CARET}: `E` for `R` — this is the fourth card, as the item's own name and its sibling headings say"),
    ("arcanum-20-le-jugement", "The Judy ment.", "The Judgment.",
     f"{CARET}: `y` for `g`, plus a space the scan inserted — the card-name line under the twentieth card's heading"),
    ("arcanum-09-lermite", "Pkudence.", "Prudence.",
     f"{CARET}: `k` for `r` — Prudence is the virtue this arcanum's list names"),
    ("arcanum-08-la-justice", "Keflex of the Father.", "Reflex of the Father.",
     f"{CARET}: `K` for `R` — every sibling list uses 'Reflex of'"),
    ("arcanum-08-la-justice", "Keflex of Realization", "Reflex of Realization",
     f"{CARET}: `K` for `R` — every sibling list uses 'Reflex of'"),
]

LEFT_ALONE = [
    ("arcanum-08-la-justice", "(^ Kaph)",
     "the caret stands where a Hebrew letter should be, exactly as the `p` does in "
     "the neighbouring `(p He)`. Both are mis-scanned Hebrew glyphs; supplying כ and "
     "ה would be reconstruction, not repair."),
    ("arcanum-20-le-jugement", "20th Hebrew letter (Eesh).",
     "the 20th Hebrew letter is Resh, and scripts/clean_papus_sections.py's own "
     "docstring names this exact corruption (\"'Resh' becomes 'Eesh'\"). It is still a "
     "whole proper name rather than a character slip, so it stays visible."),
    ("arcanum-03-limperatrice", "She holds an eaçde in her riodit hand.",
     "multi-letter garbling; 'an eagle in her right hand' is the likely reading but "
     "it is a reconstruction of two whole words, not a character repair."),
    ("arcanum-06-lamoureux", "the iash thunder-stricken personage",
     "more than one reading is defensible ('last'? 'rash'?)."),
    ("arcanum-00-le-fou / arcanum-15-le-diable", "Samedi",
     "the letter is Samech; 'Samedi' is a whole-word substitution, same class as "
     "'Eesh' above."),
    ("arcanum-17-les-etoiles", "the orran of speech",
     "'organ' is the likely reading but it is a whole word."),
    ("arcanum-01-le-bateleur", "ail the other cards",
     "'all' is the likely reading but it is a whole word."),
    ("arcanum-21-le-monde", "thus formed **. / the leading '. ' on the paragraph before",
     "leftover typesetting marks; harmless and ambiguous in origin."),
]

# Four fixes change the token count: 'Judy ment' (2) -> 'Judgment' (1), the two
# deleted stray glyphs ('^.' collapsing into '.', and a dangling '<'), and the
# stray capital 'J' after the FIFTEENTH CARD OF heading.
EXPECTED_WORD_DELTA = 4


def load():
    with open(GRAMMAR, encoding="utf-8") as fh:
        return json.load(fh)


def apply(grammar, strict):
    """Apply every fix. With strict=True, each target must occur exactly once
    in its item (used for the write pass); with strict=False, a missing target
    is simply skipped (used by --check to test idempotency)."""
    by_id = {it["id"]: it for it in grammar["items"]}
    applied, missing = [], []
    for item_id, old, new, reason in FIXES:
        it = by_id.get(item_id)
        if it is None:
            missing.append((item_id, old, "no such item"))
            continue
        body = it["sections"][SECTION]
        n = body.count(old)
        if n == 0:
            missing.append((item_id, old, "not found"))
            continue
        if n > 1:
            missing.append((item_id, old, f"found {n} times — not unique"))
            continue
        it["sections"][SECTION] = body.replace(old, new, 1)
        applied.append((item_id, old, new, reason))
    return applied, missing


def words(grammar):
    return sum(len(it["sections"][SECTION].split()) for it in grammar["items"])


def write_log(applied):
    header = f"""# Papus — *Le Tarot des Bohémiens*, OCR character substitutions repaired — {DECK}

Public domain. The 1896 Morton translation was scanned badly in a handful of places and
the scanner substituted **single characters** rather than whole words — `^` for `gh`/`g`,
`>` for `l`, `<m` for `gn`, `P` for `F`, `j` for `e`, `K`/`k` for `R`/`r`, `y` for `g`,
`E` for `R` — producing words that are not words: `Li^ht`, `Ho>y`, `a^ain`, `si^ns`, `bj`,
`OP`, `Keflex`, `Pkudence`, `Judy ment`, `FOUETH`.

Each repair below restores a word the surrounding sentence already determines. None of them
changes what Papus says, and none is an editorial rewrite. The script that made them
(`scripts/fix_papus_ocr_substitutions.py`, idempotent, `--check` verifies without writing)
is an explicit allow-list: exact string in, exact string out, each asserted to occur exactly
once in the deck. No pattern is ever run over the corpus.

Two entries are **deletions** rather than corrections, because the sentence is complete
without the glyph and there is nothing to restore it to.

What was deliberately **left alone** is listed at the end — those need interpretation, not
repair, and the decision belongs on the record rather than inside a script.

---

## Repaired

"""
    lines = []
    for item_id, old, new, reason in applied:
        lines.append(f"### `{item_id}`\n")
        lines.append(f"**{reason}**\n")
        lines.append(f"```diff\n- {old}\n+ {new}\n```\n")
    lines.append("---\n")
    lines.append("## Left alone, deliberately\n")
    for item_id, snippet, reason in LEFT_ALONE:
        lines.append(f"- **`{item_id}`** — `{snippet}`\n  {reason}\n")
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(header)
        fh.write("\n".join(lines).rstrip() + "\n")
    print(f"wrote {os.path.relpath(LOG, ROOT)}")


def check():
    grammar = load()
    ok = True
    for item_id, old, _, _ in FIXES:
        it = next((i for i in grammar["items"] if i["id"] == item_id), None)
        if it and old in it["sections"][SECTION]:
            ok = False
            print(f"FAIL {item_id}: uncorrected OCR substitution {old!r}")
    if ok:
        print(f"OK: {len(grammar['items'])} items — all {len(FIXES)} known OCR "
              f"character substitutions are repaired; {len(LEFT_ALONE)} "
              f"documented cases left alone by decision")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.check:
        sys.exit(0 if check() else 1)

    before = load()
    w_before = words(before)
    grammar = load()
    applied, missing = apply(grammar, strict=True)
    if missing:
        for item_id, old, why in missing:
            print(f"FAIL {item_id}: {old!r} — {why}")
        print("\nFAIL: allow-list did not match cleanly; nothing written")
        sys.exit(1)

    w_after = words(grammar)
    if w_before - w_after != EXPECTED_WORD_DELTA:
        print(f"FAIL: word delta {w_before - w_after} != expected "
              f"{EXPECTED_WORD_DELTA}")
        sys.exit(1)

    # Reverse-substitution proof: undoing every fix must reproduce the original
    # body character for character.
    by_before = {i["id"]: i["sections"][SECTION] for i in before["items"]}
    for it in grammar["items"]:
        body = it["sections"][SECTION]
        for item_id, old, new, _ in reversed(FIXES):
            if item_id == it["id"]:
                body = body.replace(new, old, 1)
        if body != by_before[it["id"]]:
            print(f"FAIL {it['id']}: reverse substitution does not reproduce "
                  f"the original body")
            sys.exit(1)

    with open(GRAMMAR, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(grammar, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote tarot/{DECK}/grammar.json ({len(applied)} substitution(s) "
          f"repaired across "
          f"{len({a[0] for a in applied})} item(s))")
    print(f"words: {w_before} -> {w_after} (delta {w_before - w_after}, expected "
          f"{EXPECTED_WORD_DELTA})")
    write_log(applied)

    print("\n--- verifying ---")
    if not check():
        sys.exit(1)


if __name__ == "__main__":
    main()
