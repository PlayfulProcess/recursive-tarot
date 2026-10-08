# Strength and Justice: what each source prints

Checked Oct 8 2026 for the courses review (`docs/plan/COURSES-REVIEW-2026-10-08.md`, item 22
and section 3). The repo used to say "the Golden Dawn swapped the numbers of Strength and
Justice and the Rider-Waite-Smith inherited them". The printed sources say something narrower.

## What each source prints

| Source | Strength / Fortitude | Justice | Letters and signs | How it was checked |
|---|---|---|---|---|
| Tarot de Marseille (Conver, 1760; in this library) | XI, *La Force* | VIII, *La Justice* | none | The card images in `tarot/tarot-de-marseille-conver/` |
| S. L. MacGregor Mathers, *The Tarot: Its Occult Signification, Use in Fortune-Telling, and Method of Play* (London: George Redway, 1888), table of the 22 trumps | 11, "La Forza … Strength, Fortitude", letter Kaph | 8, "La Giustizia … Justice", letter Cheth | Éliphas Lévi's scheme: the Magician is Aleph, the Fool (0) is Shin | Two transcriptions of the 1888 text (mr-kaplan.com; a retyped PDF hosted by benebellwen.com) agree; a page scan was not seen |
| Book T, "A Description of the Cards of the Tarot", *The Equinox* I(8), September 1912, pp. 143–210 (published by Crowley) | Numbered **11**, "Fortitude", letter Teth, Leo; set in the table between the Chariot and the Hermit | Numbered **8**, "Justice", letter Lamed, Libra; set between the Wheel and the Hanged Man | The Fool (0) is Aleph | The OCR of the 1912 scan ([archive.org, IAPSOP](https://archive.org/details/IAPSOP-equinox_v1_n8_1912_Sep), the table of the twenty-two keys) and the transcription in `research/sources/book-t-equinox-1912.txt`. The same printing's list of trump meanings reads "8. Eternal justice …" and "11. Courage, strength, fortitude …" |
| Rider-Waite-Smith cards (Rider, 1909) | VIII, STRENGTH | XI, JUSTICE | none on the cards | The card images in `tarot/rider-waite-smith-pictorial-key/` |
| A. E. Waite, *The Pictorial Key to the Tarot* (1911) | 8 | 11 | none | The transcription in `tarot/rider-waite-smith-pictorial-key/grammar.json` (Strength) |
| Crowley and Harris, Thoth deck (1944) | XI, Lust (Leo) | VIII, Adjustment (Libra) | Golden Dawn letters kept, old numbers kept | Reference only, from the deck as published; not re-checked here |
| Israel Regardie, *The Golden Dawn* (1937–40) | not checked | not checked | | Reference only: in copyright, and not read for this note |

Waite's own sentence under Strength, public domain (1911):

> For reasons which satisfy myself, this card has been interchanged with that of justice, which
> is usually numbered eight. As the variation carries nothing with it which will signify to the
> reader, there is no cause for explanation.

## What is known

1. **The Golden Dawn's change is in the attributions.** Book T gives Leo and the letter Teth
   to Fortitude, and Libra and Lamed to Justice. Counting the Fool as Aleph, that puts Fortitude
   in the eighth place of the letter sequence and Justice in the eleventh, so the zodiac runs
   in order (Leo before Libra).
2. **The one printing of Book T keeps the old numbers.** *The Equinox* (1912) numbers Fortitude
   11 and Justice 8 while seating them on Teth and Lamed. Crowley edited that printing, and his
   later Thoth deck keeps the same arrangement (old numbers, Golden Dawn letters). Whether the
   Order's own manuscripts renumbered the two cards cannot be settled from the printed sources
   checked here; reports that they did were not traced to a document.
3. **The renumbering is first seen in print in 1909.** The Rider-Waite-Smith deck prints
   Strength VIII and Justice XI, and Waite's book takes the change on himself ("for reasons
   which satisfy myself") without naming the Order. No earlier printed pack or book with that
   numbering is known to this repo's sources.
4. **Mathers's own public book of 1888 has neither.** It keeps Justice 8 and Strength 11 and
   uses Lévi's letter scheme, not the Order's.

So the accurate short form is: *the Golden Dawn moved the two cards' attributions (Leo to
Strength, Libra to Justice); the Rider-Waite-Smith deck of 1909 is the first known to print the
new numbers.* "The Golden Dawn swapped the numbers" says more than the printed record shows.

## Where the repo now says this

`research/12-golden-dawn-book-t.mdx`, `research/people/golden-dawn.md`,
`research/people/macgregor-mathers.md`, `research/decks/golden-dawn-book-t-tarot.md`,
`research/cards/golden-dawn-book-t-tarot.md`, the Golden Dawn deck's Strength, Justice and
"The 22 Keys" items, and `course/same-card-every-deck.mdx`.
