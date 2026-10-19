# Book T glyphs

46 SVG glyphs, each on a 100 × 100 box, drawn as plain strokes (`stroke="currentColor"`, so a page can colour them):

- the seven planets of Book T: `planet-saturn`, `planet-jupiter`, `planet-mars`, `planet-sun`, `planet-venus`, `planet-mercury`, `planet-moon`
- the twelve signs: `sign-aries` … `sign-pisces`
- the four elements and Spirit: `element-fire`, `element-water`, `element-air`, `element-earth`, `element-spirit`
- the twenty-two Hebrew letters, in a plain square script: `hebrew-aleph` … `hebrew-tau`

**Where they come from.** Drawn for this site (October 2026) as hand-written SVG path data. No font, icon set or image was copied or traced, so no outside licence applies. The shapes are the traditional symbols, which belong to no one.

**Licence.** CC BY-SA 4.0, like the rest of the Book T deck (`tarot/book-t`). Credit: PlayfulProcess, recursive-tarot.

**How they are used.** `scripts/build_book_t_iconography.py` reads them and composes them onto each card of the deck (`tarot/book-t/iconography/<card id>.svg`), where Book T (1912) places them. To change a glyph, edit its file here, then run that script; its `--check` runs in `scripts/check_all.py`.
