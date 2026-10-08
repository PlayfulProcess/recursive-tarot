# Anachronism audit, 8 October 2026

**Why.** On Oct 8 two errors were found. The Court de Gébelin deck had him naming Ma'at, though he
wrote in 1781 and hieroglyphs were not read until Champollion (1822). And the Golden Dawn Justice
"Symbol" line about "the feather of Ma'at" was AI-written text shown as Golden Dawn lore (that one
was already fixed on `main`; the [glossary entry](https://tarot.recursive.eco/pages/glossary.html#maat)
now says the comparison is later readers', not Book T's). PlayfulProcess asked for an audit for the
same pattern.

**The pattern.** (a) Anachronism: a person, deck or tradition credited with a name, fact or object
not available at its date. (b) Editorial or AI-written lore shown as a tradition's own words. (c) An
attribution that the cited source does not contain.

**How.** Every source deck grammar (`tarot/*/grammar.json`, not the `_generated` ones) was dumped to
text, section by section, and searched for names and ideas with known dates: Egyptian names read only
after 1822 (Ma'at, Ra, the weighing of the heart, the *Book of the Dead*), Kabbalah, Hebrew letters,
the four elements, Jung's terms, "major arcana", Golden Dawn and Rider-Waite-Smith meanings. Sections
that speak in a historical author's voice were read in full. The Court de Gébelin deck was checked
line by line against his 1781 text. Courses (`course/*.mdx`) were searched the same way and their
quotations checked where a public-domain text was at hand.

**Primary sources used.**
- Court de Gébelin, "Du Jeu des Tarots", *Monde primitif* vol. VIII (Paris, 1781), Article I,
  pp. 365-378, and the Comte de Mellet's essay in the same volume, from p. 395. Scans:
  [mondeprimitifana08cour](https://archive.org/details/mondeprimitifana08cour) and
  [b30411956_0008](https://archive.org/details/b30411956_0008).
- A. E. Waite, *The Pictorial Key to the Tarot* (1911), [Project Gutenberg #43548](https://www.gutenberg.org/ebooks/43548).
- The card images on R2 (Etteilla II Justice and Judgement were viewed).

**How the fixes were made.** One script,
[`scripts/archive/anachronism_audit_2026_10_08.py`](../../scripts/archive/anachronism_audit_2026_10_08.py),
with the 1781 translation in
[`scripts/archive/cdg_1781_text.py`](../../scripts/archive/cdg_1781_text.py). Every section it changed
or removed is kept, as it stood, in
[`tarot/_archive/anachronisms-2026-10-08.json`](../../tarot/_archive/anachronisms-2026-10-08.json).
No quoted public-domain source text was removed.

## Findings and fixes

| # | File | Item | Sentence (as it stood) | Why it is impossible or unsupported | Evidence | Fix |
|---|------|------|------------------------|-------------------------------------|----------|-----|
| 1 | `tarot/court-de-gebelin-tarot` | atout-08 Justice, Reading + Symbol | "the Egyptians ... understood that cosmic order (Ma'at) and social justice were one"; "Justice identified with Ma'at" | (a) Ma'at's name could not be read before 1822. (c) He names Astraea. | 1781 text p. 372: "c'est Astrée assise sur son Trône, tenant d'une main un poignard; de l'autre, une balance" | Replaced with his own text, translated; note on Ma'at |
| 2 | same | atout-02 to atout-21, "Court de Gébelin's Egyptian Reading" (20 cards, Justice included) | Labelled "[Translated from ...]" but third person ("Gébelin sees ...") and adding ideas he does not have: the Wheel's "sphinx at the summit", the Moon's "pylons" and "scarab", the Sun as "Ra", Judgement's "weighing of the heart" and Thoth, the Tower as "Babel", the World's "four living creatures of the Egyptian cosmology", Death as "the unnumbered card" | (b) AI-written text presented as a translation. (a) Ra and the weighing of the heart were not readable in 1781. (c) Several claims contradict the text | 1781 text: XVI is "Château de Plutus", after Herodotus's Rhampsinitus (pp. 376-377); XX is the Creation (pp. 377-378); XXI is Time with the four Seasons (p. 378); XIII is "placed under this number", thirteen (p. 375); the Wheel's figures are monkeys, dogs, rabbits (p. 377). The Sphinx on the Wheel is Lévi's, as the card's own research note says | All 20 replaced by a full translation of his 1781 text with page numbers. Fool and Bateleur were already faithful and are kept |
| 3 | same | 21 Symbol lines | e.g. Fool "identified ... with Typhon"; Empress "Isis ... queen of heaven"; Emperor "Osiris"; Lovers "Marriage of Osiris and Isis"; Death "Typhon"; Sun "the sun god Ra"; Wheel "the Nile flood"; Judgement "Judgment Day ... resurrection of Osiris" | (c) Not in his text; (a) Ra | 1781 text: his Typhon is XV only (p. 376); Osiris is VII (p. 370); III and IV are Queen and King (p. 369); VI is a priest-blessed marriage (p. 371). "Jupiter" for V and Isis for XXI are Mellet's (pp. 396-399), not his | Each line rewritten to say what he wrote |
| 4 | same | Research notes atout-01, 02, 03, 04, 07, 21 | "cups/coins/swords/baton turned into element-symbols"; Empress as "Osiris's counterpart"; Emperor "becomes ... Osiris"; Chariot "confidence: medium" on Osiris | (c) | 1781 text pp. 369-370 | Correction line added under each note, sources kept |
| 5 | `tarot/etteilla-i-livre-de-thot`, `-ii-egyptian`, `-iii-oracle-des-dames` | etteilla-09 Justice, Historical Context + Hermetic Correspondence + metadata | "In the Hermetic tradition, Justice connects to Ma'at"; "Ma'at; cosmic balance; the weighing of souls" | (a) Etteilla died in 1791; Ma'at unread before 1822. (c) No Hermetic text names her | Dates | Sentence removed; correspondence reworded and labelled editorial |
| 6 | the three Etteilla decks | etteilla-01, Historical Context | "Etteilla believed tarot originated with the Egyptian priests of the Temple of Ptah at Memphis" | (c) No source given; not in the repo's Etteilla sources | none found | Now: "held that the tarot was an ancient Egyptian book, the Book of Thoth" |
| 7 | the three Etteilla decks | 12 Hermetic Correspondence sections each | e.g. "Corresponds to the Ein Sof in Kabbalah, the Tao ..." | (b) Modern comparisons with no label | none | Labelled "*Editorial comparison, not Etteilla's words.*" |
| 8 | the three Etteilla decks | etteilla-01 Etymology + metadata | "In Hermetic philosophy, this is the Ein Sof or Tao" | (c) Ein Sof is Kabbalah, the Tao is Chinese; neither is Hermetic | none | Sentence removed |
| 9 | the three Etteilla decks | 56 court and pip cards each (22-77), Symbol | e.g. Five of Cups "loss and disappointment, the emotional focus on what has spilled"; Three of Swords "heartbreak and sorrow"; Eight of Cups "departure and moving on" | (a) These are Rider-Waite-Smith (1909) meanings on a 1788 pack. They contradict the card's own Etteilla words beside them | Etteilla 1791: Five of Cups "Héritage", Three of Swords "Éloignement", Eight of Cups "Fille blonde" | 168 sections removed to the archive |
| 10 | `tarot/etteilla-ii-egyptian` | 22 trumps (01-21, 78), Symbol | e.g. Justice "with Ma'at's scales"; Judgement "the weighing of the heart before Osiris"; Strength "perhaps Sekhmet"; Celestial Bodies "Ra, Thoth" | (a) and (b) The cards show none of this: Justice is a crowned woman with dagger and scales, Judgement an angel over the rising dead | Card images on R2 (viewed) | 22 sections removed to the archive |
| 11 | `tarot/visconti-sforza-tarot`, `cary-yale-visconti-tarot` | 78 pip History lines, 4 About this Suit, 11 Symbol lines | "A pip card of Coins (Denari), the suit of Earth"; "In Italian tradition the bastoni suit is associated with the merchant class and with the fire element" | (a) Suit-to-element links are later occult attributions; 15th-century Milan had none | No 15th-century source; Etteilla is reportedly the first to bring the elements into tarot, in 1790 (Wikipedia, "Jean-Baptiste Alliette") | "the suit of X" dropped from History; other lines labelled "*a later occult attribution, not the card-makers'*" |
| 12 | `tarot/tarot-de-marseille-conver` | 56 pip Symbols, 4 suit and 4 keyword items | "Suit: Earth. ... Earth element: ..."; "in the Marseille elemental system" | (a) Conver's 1760 pack has no elements; there is no "Marseille elemental system" | as above | "Suit: Earth (a later occult attribution, not Conver's)"; the false phrase removed |
| 13 | `minchiate-florence-tarot`, `tarocchino-bologna`, `paris-anonymous-tarot`, `vieville-tarot`, `tarot-de-besancon` | suit and keyword items | "suit of Fire"; "(Air)" | (a) as above. The Minchiate's four element *trumps* are real and untouched | as above | Labelled, or the bracket removed |
| 14 | `tarot/visconti-sforza-tarot` | major-08 Justice, Symbol | "Justice holds two swords rather than the conventional scales-and-single-sword" | (c) The card shows a sword and a balance; the same item's Iconography says so | Card image | Rewritten to match the card |
| 15 | `tarot/oswald-wirth-tarot` | emg-the-great-work, Symbol | "synthesises Marseille iconography with Golden Dawn-adjacent occultism" | (c) Wirth followed Lévi's French letter order, not the Golden Dawn's | The deck's own Correspondences (Lévi's attribution) | Rewritten |
| 16 | same | arcanum-08 Justice, Symbol (already labelled editorial) | "Ma'at in the Egyptian sense, the scales that weigh the heart against a feather" | (b) Same lore as the Golden Dawn line; Wirth's own text on the card does not mention Egypt | Wirth section of the card | Ma'at clause removed; label kept |
| 17 | `tarot/golden-dawn-book-t-tarot` | emg-majors, Symbol | "In GD practice the Trumps were used as visual keys for pathworking" | (a) "Pathworking" is the name the Order's heirs gave; the glossary and the course already say so | Glossary entry "pathworking" | Reworded: the Order's papers teach skrying and travelling in the spirit-vision; the name came later |

## Checked and left as they are

- **Glossary, Ma'at entry**: already correct (written Oct 8).
- **Court de Gébelin, Fool and Bateleur readings**: faithful to pp. 368-369.
- **Court de Gébelin, Star Symbol** (Sirius, the Nile flood, the new year): matches pp. 374-375.
- **History of Tarot course epigraph** (Waite): the quoted sentences and "which has always
  existed" are in the text. The course dates *The Pictorial Key* 1910; the Gutenberg text is the 1911
  edition, and Parts I-II first came out in 1910 as *The Key to the Tarot*. Not changed.
- **Golden Dawn courses**: "pathworking" is already named as the heirs' word.
- **Papus deck**: Papus (1889) wrote after the decipherment; his "hieroglyphs" are his own words.

## Open, for PlayfulProcess

1. **Etteilla "Card in Etteilla's System" (pips)** say "the suit of Water, governing love ...". Did
   Etteilla tie the suits to elements, or only trumps 2-5? Needs his *Cours théorique et pratique*
   (1790). Not changed.
2. **Etteilla 01 "Historical Context"** says the card "draws heavily from the Hermetic text
   'Poimandres'". No source given. Not changed.
3. **Etteilla III trump Symbols** give invented social meanings ("the unknown man at the centre of
   the female questioner's situation"). Not anachronistic, but unsourced. Not changed.
4. **Wirth "Symbolism" sections** (22) speak as Wirth ("Wirth's Bateleur is ...") with no label.
   They should be checked against the 1927 text already on each card.
5. **Wirth "About the Sequence"** maps the trumps onto "the paths of the Kabbalistic Tree of Life".
   Unverified for Wirth.
6. **Court de Gébelin atout-12 research note** says his plate flips the Hanged Man. Not checked
   against the plate.
7. **Visconti-Sforza Symbol lines** were not checked one by one against the cards; the Justice
   contradiction (#14) was found in passing.
8. The **Etteilla pip Symbols** removed in #9 leave those cards with Etteilla's words and the
   research notes only. If she wants a visual note there, it should come from the card images, by
   a person, per the Oct 4 rule.
