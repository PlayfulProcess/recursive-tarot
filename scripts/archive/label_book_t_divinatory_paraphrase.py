# -*- coding: utf-8 -*-
"""Label the golden-dawn-book-t-tarot deck's divinatory block as paraphrase.

  python3 scripts/label_book_t_divinatory_paraphrase.py [--check]

Why: `Divinatory Meaning` and `Reversed / Ill-Dignified` on this deck are
editorial PARAPHRASES of Book T's divinatory system, not quotations. Book T's
own prose reached print only via Israel Regardie's *The Golden Dawn*
(1937-40), whose copyright status is murky, so paraphrase was the right call
-- but it needs a header saying so, per the deck's existing at-change-of-voice
convention (see scripts/normalize_book_t_sections.py, which put the header
that currently sits on `Golden Dawn Title` in place the same way).

This script adds ONE header immediately before the `Divinatory Meaning`
section's body. It covers `Divinatory Meaning` AND the following
`Reversed / Ill-Dignified` section as one contiguous block (no header is
added to `Reversed / Ill-Dignified` itself -- same rule as the rest of the
deck, where a header covers every section until the next header appears).

The Golden Dawn card TITLES (`Golden Dawn Title`) and the attribution
sections (`Correspondences`, `Astrological attribution (Book T)`) are short
facts, not paraphrased prose -- left untouched.

Idempotent: re-running is a no-op. `--check` verifies without writing, and
also asserts that no section lost content (only the header text was added).
"""
import argparse, json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DECK = os.path.join(ROOT, "tarot", "golden-dawn-book-t-tarot", "grammar.json")

HEADER = (
    "*Editorial — The Recursive Tarot · after Book T's divinatory meanings "
    "(paraphrased; Book T's own prose is not safely public domain)*"
)

TARGET_SECTION = "Divinatory Meaning"


def add_header(text):
    if not isinstance(text, str) or not text.strip():
        return text, False
    if text.startswith(HEADER):
        return text, False  # idempotent: already labeled
    return HEADER + "\n\n" + text, True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                     help="verify only; do not write the file")
    args = ap.parse_args()

    with open(DECK, encoding="utf-8") as fh:
        grammar = json.load(fh)

    cards = 0
    touched = 0
    missing_section = []
    word_count_failures = []

    for item in grammar.get("items", []):
        if item.get("level") != 1:
            continue
        cards += 1
        sections = item.get("sections")
        if not isinstance(sections, dict):
            continue
        if TARGET_SECTION not in sections:
            missing_section.append(item.get("id"))
            continue

        original = sections[TARGET_SECTION]
        new, changed = add_header(original)

        # word-count / content check: body word count must be unchanged;
        # total word count must grow by exactly len(HEADER.split()).
        orig_words = original.split() if isinstance(original, str) else []
        new_words = new.split() if isinstance(new, str) else []
        header_words = HEADER.split()
        if changed:
            expected_len = len(orig_words) + len(header_words)
            body_after = new_words[len(header_words):]
            if len(new_words) != expected_len or body_after != orig_words:
                word_count_failures.append(item.get("id"))
            touched += 1

        sections[TARGET_SECTION] = new

    print(f"level-1 cards: {cards}")
    print(f"cards touched (header added): {touched}")
    if missing_section:
        print(f"WARN cards missing '{TARGET_SECTION}': {missing_section}")
    if word_count_failures:
        print(f"\nFAIL: {len(word_count_failures)} word-count violation(s):")
        for f in word_count_failures[:20]:
            print("  -", f)
        sys.exit(1)
    print("word-count check: OK (only the header was added, zero body changes)")

    if args.check:
        print("--check: nothing written")
        return

    if touched == 0:
        print("nothing to write (already labeled)")
        return

    # Match the file's existing shape exactly (indent=2, unescaped unicode, no
    # trailing newline) so the diff is only the header lines that were added.
    with open(DECK, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(grammar, ensure_ascii=False, indent=2))
    print(f"wrote {os.path.relpath(DECK, ROOT)}")


if __name__ == "__main__":
    main()
