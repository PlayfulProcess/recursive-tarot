# Book T linocut blocks

The carved blocks of the Book T deck's fifth picture set, the **linocut** (`tarot/book-t/linocut/`). Each file has the same name, origin and size as the full imagery's part in `../parts/`, so the same compositions (`../full-imagery/compositions.json`) print with either. Where a part has no block here, `scripts/build_book_t_linocut.py` prints the full imagery's part pulled into the print's inks (every fill becomes paper, the card's ink or black by its lightness; every line becomes black).

**The print's language.** Black (`#1c1915`) on warm paper (`#f2e8d2`), with one ink per card: Fire vermilion, Water deep blue, Air ochre, Earth olive, the Keys gold. In a block, `currentColor` is that ink. Light comes from what is cut away: paper lines through black and ink (gouge cuts), rays as tapered wedges, clouds as scrolls with carved curls, faces as a simple carved mask with closed eyes. The patterns `url(#gouge)` (ink with fine paper cuts), `url(#tint)` (paper with ink cuts) and `url(#hatch)` (paper with fine black cuts) are defined by each card.

**Where they come from.** Drawn for this site (October 2026) as hand-written SVG path data, after the conventions of relief prints (woodcut and linocut) studied for their language only. No font, icon set, print or image was copied or traced.

**Licence.** CC BY-SA 4.0, like the rest of the Book T deck. Credit: PlayfulProcess, recursive-tarot.

**How they are used.** Edit a block here, then run `python scripts/build_book_t_linocut.py` and `scripts/build_book_t_page.py`; its `--check` runs in `scripts/check_all.py`.
