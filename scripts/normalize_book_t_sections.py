# -*- coding: utf-8 -*-
"""Editorial restructure of the Golden Dawn / Book T deck's per-card texts.

  python3 scripts/normalize_book_t_sections.py [--check]

Plan: _research/BOOKT-DECK-EDIT-PLAN-2026-07-27.md

The deck uses Rider-Waite-Smith imagery but a Book T (Golden Dawn) system, and
carries later commentary (Papus) on top. Before this pass the card detail stacked
those blocks in arbitrary order, hid provenance in easy-to-miss inline brackets
(`[A. E. Waite, ...]`), and carried transcription line breaks into the middle of
sentences (the static viewer turns every \\n into <br>, so Waite rendered as
"...daughter of heaven and / earth.").

This script, per level-1 card:

  1. reorders `sections` so the text that describes the actual pictures leads
     (Waite -> Scene), then the deck's native Book T system, then later
     commentary, then the editorial research note;
  2. replaces the inline bracketed attribution with a one-line editorial header
     at each change of voice (author, date, tradition, relationship to the deck);
  3. normalizes line breaks: soft-hyphen breaks are rejoined, single newlines
     inside a paragraph become spaces, blank-line paragraph breaks survive.

Nothing is deleted: every section is asserted token-for-token identical before
and after, ignoring only the removed bracket, the added header, and whitespace.
The script is idempotent (re-running is a no-op) and exits non-zero if any card
fails the no-content-lost check.
"""
import argparse, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DECK = os.path.join(ROOT, "tarot", "golden-dawn-book-t-tarot", "grammar.json")

# --- editorial headers -------------------------------------------------------
# One line, italic (the static viewer's mini-markdown only supports * and **, so
# italics is the styling hook), format: source - work, date - relationship.
WAITE = "*A. E. Waite — The Pictorial Key to the Tarot, 1911 · describes this imagery*"
SCENE = "*Editorial — The Recursive Tarot · what is pictured on this card*"
BOOK_T = ("*Book T — Golden Dawn, c. 1888 · the deck's native system "
          "(predates this imagery)*")
PAPUS = ("*Papus (Gérard Encausse) — Le Tarot des Bohémiens, 1889 · French occult "
         "revival · later interpretation, not written for this deck*")
NOTE = ("*Editorial — The Recursive Tarot · sources, and what changed from the "
        "parent deck*")

# Canonical section order. `None` = no header (same voice as the section above).
ORDER = [
    ("Waite", WAITE),
    ("Scene", SCENE),
    ("Golden Dawn Title", BOOK_T),          # first Book T section present carries
    ("Golden Dawn Rank", BOOK_T),           # the header; the rest inherit it
    ("Divinatory Meaning", BOOK_T),
    ("Reversed / Ill-Dignified", BOOK_T),
    ("Correspondences", BOOK_T),
    ("Astrological attribution (Book T)", BOOK_T),
    ("Symbol", BOOK_T),
    ("Papus", PAPUS),
    ("Research note", NOTE),
]
KNOWN = [k for k, _ in ORDER]
HEADERS = {WAITE, SCENE, BOOK_T, PAPUS, NOTE}

BRACKET = re.compile(r"\A\s*\[[^\]]*\]\s*\n+")


def dehyphenate(text):
    """Rejoin words broken across a transcription line ("prehen-\\nsion")."""
    return re.sub(r"([A-Za-z])-\n([a-z])", r"\1\2", text)


def normalize_breaks(text):
    text = dehyphenate(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)   # single \n -> flowing text
    text = re.sub(r"\n{3,}", "\n\n", text)          # keep paragraph breaks only
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def strip_header(text):
    """Drop a leading editorial header (ours) or inline bracket (the old form)."""
    text = BRACKET.sub("", text)
    for h in HEADERS:
        if text.startswith(h):
            return text[len(h):].lstrip("\n")
    return text


def tokens(text):
    """Content fingerprint: no bracket/header, no hyphen breaks, no whitespace."""
    return dehyphenate(strip_header(text)).split()


def restructure(sections):
    out, failures, seen_header = {}, [], set()
    unknown = [k for k in sections if k not in KNOWN]
    for key in KNOWN + unknown:
        if key not in sections:
            continue
        original = sections[key]
        if not isinstance(original, str) or not original.strip():
            out[key] = original
            continue
        header = dict(ORDER).get(key)
        body = normalize_breaks(strip_header(original))
        if header and header not in seen_header:
            seen_header.add(header)
            new = header + "\n\n" + body
        else:
            new = body
        if tokens(original) != tokens(new):
            failures.append(key)
        out[key] = new
    return out, failures, unknown


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify only; do not write the file")
    args = ap.parse_args()

    with open(DECK, encoding="utf-8") as fh:
        grammar = json.load(fh)

    touched, failures, unknown_keys, reordered = 0, [], set(), 0
    for item in grammar.get("items", []):
        if item.get("level") != 1:
            continue
        sections = item.get("sections")
        if not isinstance(sections, dict):
            continue
        new, bad, unknown = restructure(sections)
        unknown_keys.update(unknown)
        for key in bad:
            failures.append(f"{item.get('id')}: section '{key}' lost content")
        if list(new.keys()) != list(sections.keys()):
            reordered += 1
        if new != sections:
            touched += 1
        item["sections"] = new

    cards = sum(1 for i in grammar.get("items", []) if i.get("level") == 1)
    print(f"level-1 cards: {cards}")
    print(f"cards changed: {touched}  (reordered: {reordered})")
    if unknown_keys:
        print(f"WARN unknown section keys kept at the end: {sorted(unknown_keys)}")
    if failures:
        print(f"\nFAIL: {len(failures)} no-content-lost violation(s):")
        for f in failures[:20]:
            print("  -", f)
        sys.exit(1)
    print("no-content-lost: OK (every section token-identical before/after)")

    if args.check:
        print("--check: nothing written")
        return
    # Match the file's existing shape exactly (indent=2, unescaped unicode, no
    # trailing newline) so the diff is only the texts that actually changed.
    with open(DECK, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(grammar, ensure_ascii=False, indent=2))
    print(f"wrote {os.path.relpath(DECK, ROOT)}")


if __name__ == "__main__":
    main()
