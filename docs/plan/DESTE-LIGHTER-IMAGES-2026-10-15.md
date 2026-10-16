# The d'Este Tarocchi: lighter pictures (Oct 15 2026)

PlayfulProcess, on recursive.eco's Explore tiles: "I am fine with a black frame, not fine with an
image so dark it is hard to see what is pictured; that was the case with that specific tarot." The
deck is `tarot/este-tarot` (the Ferrarese fragment, c. 1450; 16 cards; Yale, Beinecke, Cary
Collection, PLAYING CARDS GEN 966).

**Nothing is changed by this note.** No picture is uploaded and the grammar is untouched. It
proposes one step for her yes.

## What was measured

Mean luminance (PIL, greyscale 0–255) of each `images/cNN.jpg` on `main` (d2269c5). "Card" is the
mean over the card itself, leaving out Yale's black backdrop (pixels at 24 or below). For
comparison, the 130 grammar covers measured on recursive.eco have a **median of 146**.

The local copies match Yale's own scan: the World fetched from Yale's IIIF at the same width
measures the same (mean 87, 95th percentile 167). **The dark pictures come from the scan itself
and the cards' darkened paint, not from our copies.**

## Lighter sources: none found

- **The holding library.** Yale holds all 16 surviving cards. Its open-access IIIF scan
  (`https://collections.library.yale.edu/iiif/2/<id>/…`, up to 3240 × 5608) is the only
  digitisation, and is the one we already use. Larger sizes have the same exposure. IIIF offers
  `default`, `color`, `gray` and `bitonal` qualities, but no brightness.
- **Wikimedia Commons.** No copy of these cards (searched "Este tarot", "Estensi tarocchi",
  "Cary Collection tarot Ferrara", "tarocchi Este Beinecke", files and categories, Oct 15 2026).
- **Other photographs** (books, auction or museum catalogues) are not open-licensed.

So the proposal is **brightened copies** of Yale's scans, credit kept.

## The table

Levels: input black 0, input **white W → 255**, then **gamma G** (out = 255 · (min(in, W) / W)^(1/G)),
the same curve on R, G and B. Per card, W is the card's 99.5th percentile (so about 0.5% of its
pixels, the brightest gold and paper, clip) and G is the value that brings the card's mean to 140.

| Card | Current URL | Mean (whole / card) | Lighter source | Licence | Proposal |
|---|---|---|---|---|---|
| King of Swords | `images/c01.jpg` | 82 / 89 | none (Yale IIIF 33215686 is the only scan) | Open access, Yale University Library | brighten a copy: levels W 173, gamma 1.11 |
| Queen of Swords | `images/c03.jpg` | 80 / 88 | none (IIIF 33215688) | Open access, Yale | brighten a copy: levels W 184, gamma 1.27 |
| Cavalier of Swords | `images/c05.jpg` | 85 / 93 | none (IIIF 33215690) | Open access, Yale | brighten a copy: levels W 186, gamma 1.18 |
| King of Batons | `images/c07.jpg` | 80 / 87 | none (IIIF 33215692) | Open access, Yale | brighten a copy: levels W 182, gamma 1.25 |
| Cavalier of Batons | `images/c09.jpg` | 82 / 89 | none (IIIF 33215694) | Open access, Yale | brighten a copy: levels W 177, gamma 1.16 |
| Jack of Batons | `images/c11.jpg` | 78 / 85 | none (IIIF 33215696) | Open access, Yale | brighten a copy: levels W 175, gamma 1.23 |
| King of Coins | `images/c13.jpg` | 85 / 93 | none (IIIF 33215698) | Open access, Yale | brighten a copy: levels W 181, gamma 1.13 |
| Queen of Cups | `images/c15.jpg` | 89 / 97 | none (IIIF 33215700) | Open access, Yale | brighten a copy: levels W 179, gamma 1.02 |
| Il Bagatto (The Magician) | `images/c17.jpg` | 87 / 95 | none (IIIF 33215702) | Open access, Yale | brighten a copy: levels W 179, gamma 1.07 |
| Il Papa (The Pope) | `images/c19.jpg` | 79 / 86 | none (IIIF 33215704) | Open access, Yale | brighten a copy: levels W 177, gamma 1.24 |
| Temperance | `images/c21.jpg` | 80 / 88 | none (IIIF 33215706) | Open access, Yale | brighten a copy: levels W 185, gamma 1.27 |
| The Star | `images/c23.jpg` | 84 / 92 | none (IIIF 33215708) | Open access, Yale | brighten a copy: levels W 180, gamma 1.14 |
| The Moon | `images/c25.jpg` | 84 / 92 | none (IIIF 33215710) | Open access, Yale | brighten a copy: levels W 181, gamma 1.14 |
| The Sun | `images/c27.jpg` | 82 / 89 | none (IIIF 33215712) | Open access, Yale | brighten a copy: levels W 177, gamma 1.15 |
| The World (the deck's cover) | `images/c29.jpg` | 87 / 96 | none (IIIF 33215714) | Open access, Yale | brighten a copy: levels W 195, gamma 1.21 |
| Il Matto (The Fool) | `images/c31.jpg` | 84 / 92 | none (IIIF 33215716) | Open access, Yale | brighten a copy: levels W 174, gamma 1.07 |

URLs are under `https://tarot.recursive.eco/tarot/este-tarot/`. The two axis rows reuse c17 and c01.

**One setting for the whole deck**, if she prefers the cards to keep their relative tones: levels
**W 180, gamma 1.17** (card means land between about 130 and 150).

A test copy of every card was made with the per-card values and checked by eye (the Queen of
Swords, the darkest, reads clearly: face, crown, shield and the gold ground); the copies were not
kept.

## If she says yes

1. A script (`scripts/brighten_deste.py`, new) writes `images/cNN.jpg` from Yale's IIIF scan at
   the current size with the values above, quality 90, and keeps the untouched originals in
   `tarot/este-tarot/images/original/` (a kept file costs nothing).
2. Credit stays "Beinecke Rare Book & Manuscript Library, Yale University (Cary Collection,
   PLAYING CARDS GEN 966)", with one added line in `_image_provenance`: "levels adjusted for
   legibility (white point and gamma per card, docs/plan/DESTE-LIGHTER-IMAGES-2026-10-15.md);
   the originals are in images/original/".
3. `python scripts/audit_image_rights.py`, `python scripts/check_all.py`, then the app's copy
   follows through the usual sync.

Not proposed: cropping Yale's black backdrop. Her correction keeps black frames; only the
pictures were too dark.
