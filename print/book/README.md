# The book — print-on-demand build

A print-ready interior for **KDP / IngramSpark**, generated from the *same* sources
as the live course (no parallel manuscript):
- prose → `course/history-of-tarot.mdx`
- card syntheses → `research/synthesis/trumps.json`
- people, lineage, images → the deck grammars
- static plates → `print/book/figures/{lineage,timeline}.png`

## Generate

```bash
python scripts/generate_book.py        # writes print/book/book.html (downloads + downscales images on first run)
python scripts/generate_book.py --pdf  # also renders print/book/book.pdf via headless Chrome
```

`build/`, `book.html`, and `book.pdf` are **gitignored** (build artifacts). Re-runs
are fast — images are cached in `build/img/` and only downloaded once.

## Specs

- **Trim:** 7 × 10 in, **no-bleed interior** (images are inline strips, not full-bleed).
  To add full-bleed plates later: set `@page { size: 7.25in 10.25in }` + 0.125in bleed
  and let plate images run to the edge.
- **Images:** downscaled to ~360 px wide JPEG (q82) — keeps the PDF small while staying
  sharp at the ~1 in print size.
- **Full-colour** throughout (the cross-deck image strips are the point).

## To publish

1. `python scripts/generate_book.py --pdf` → `book.pdf` (the interior).
2. Upload to **KDP** (paperback) or **IngramSpark** (also hardcover / bookstore reach).
   Both accept this PDF; KDP is simplest, IngramSpark has wider distribution.
3. Add front-matter (title page, copyright, **image credits** — all public domain) and
   a cover (KDP's cover creator computes spine width from the page count).
4. The physical **card decks** stay on The Game Crafter — a different pipeline; this
   book is the reader-facing companion.
