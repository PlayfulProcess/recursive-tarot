# Papus — *Le Tarot des Bohémiens*, OCR character substitutions repaired — papus-tarot-des-bohemiens

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

### `arcanum-06-lamoureux`

**the scanner substituted a single character: `^` for `g` — 'a^ain' is not a word; the clause reads 'which again is but a lower form of itself'**

```diff
- which a^ain is
+ which again is
```

### `arcanum-08-la-justice`

**the scanner substituted a single character: `^` for `gh` — the Astral Light is Papus's own recurring term**

```diff
- Astral Li^ht.
+ Astral Light.
```

### `arcanum-15-le-diable`

**the scanner substituted a single character: `>` for `l` — the same sentence contrasts it with the God of Evil**

```diff
- the Ho>y Spirit
+ the Holy Spirit
```

### `arcanum-21-le-monde`

**the scanner substituted a single character: `<m` for `gn` and `^` for `gn` — Tau as 'the sign of signs', the phrase the paragraph is defining**

```diff
- the si<m of si^ns
+ the sign of signs
```

### `arcanum-04-lempereur`

**stray glyph deleted: the printed page had a triangle symbol here, which the same sentence already names in words ('his body forms a triangle'); there is nothing to restore the caret to**

```diff
- forms a triangle ^. Domination
+ forms a triangle. Domination
```

### `arcanum-17-les-etoiles`

**stray glyph deleted: an angle bracket left dangling after the em-dash that ends the paragraph**

```diff
- following significations — <
+ following significations —
```

### `arcanum-10-la-roue`

**the scanner substituted a single character: `P` for `F` — the other 21 items read 'ORIGIN OF THE SYMBOLISM'**

```diff
- ORIGIN OP THE SYMBOLISM
+ ORIGIN OF THE SYMBOLISM
```

### `arcanum-15-le-diable`

**the scanner substituted a single character: `P` for `F` — the other 21 items read 'SYMBOLISM OF THE'**

```diff
- SYMBOLISM OP THE
+ SYMBOLISM OF THE
```

### `arcanum-01-le-bateleur`

**the scanner substituted a single character: `j` for `e`**

```diff
- will bj found
+ will be found
```

### `arcanum-20-le-jugement`

**stray digit inside the word — the other 21 items read 'ORIGIN OF THE'**

```diff
- ORIGIN7 OF THE
+ ORIGIN OF THE
```

### `arcanum-15-le-diable`

**stray capital after the heading, which the scan truncated at 'CARD OF' on ten items**

```diff
- FIFTEENTH CARD OF J
+ FIFTEENTH CARD OF
```

### `arcanum-04-lempereur`

**the scanner substituted a single character: `E` for `R` — this is the fourth card, as the item's own name and its sibling headings say**

```diff
- THE FOUETH CARD
+ THE FOURTH CARD
```

### `arcanum-20-le-jugement`

**the scanner substituted a single character: `y` for `g`, plus a space the scan inserted — the card-name line under the twentieth card's heading**

```diff
- The Judy ment.
+ The Judgment.
```

### `arcanum-09-lermite`

**the scanner substituted a single character: `k` for `r` — Prudence is the virtue this arcanum's list names**

```diff
- Pkudence.
+ Prudence.
```

### `arcanum-08-la-justice`

**the scanner substituted a single character: `K` for `R` — every sibling list uses 'Reflex of'**

```diff
- Keflex of the Father.
+ Reflex of the Father.
```

### `arcanum-08-la-justice`

**the scanner substituted a single character: `K` for `R` — every sibling list uses 'Reflex of'**

```diff
- Keflex of Realization
+ Reflex of Realization
```

---

## Left alone, deliberately

- **`arcanum-08-la-justice`** — `(^ Kaph)`
  the caret stands where a Hebrew letter should be, exactly as the `p` does in the neighbouring `(p He)`. Both are mis-scanned Hebrew glyphs; supplying כ and ה would be reconstruction, not repair.

- **`arcanum-20-le-jugement`** — `20th Hebrew letter (Eesh).`
  the 20th Hebrew letter is Resh, and scripts/clean_papus_sections.py's own docstring names this exact corruption ("'Resh' becomes 'Eesh'"). It is still a whole proper name rather than a character slip, so it stays visible.

- **`arcanum-03-limperatrice`** — `She holds an eaçde in her riodit hand.`
  multi-letter garbling; 'an eagle in her right hand' is the likely reading but it is a reconstruction of two whole words, not a character repair.

- **`arcanum-06-lamoureux`** — `the iash thunder-stricken personage`
  more than one reading is defensible ('last'? 'rash'?).

- **`arcanum-00-le-fou / arcanum-15-le-diable`** — `Samedi`
  the letter is Samech; 'Samedi' is a whole-word substitution, same class as 'Eesh' above.

- **`arcanum-17-les-etoiles`** — `the orran of speech`
  'organ' is the likely reading but it is a whole word.

- **`arcanum-01-le-bateleur`** — `ail the other cards`
  'all' is the likely reading but it is a whole word.

- **`arcanum-21-le-monde`** — `thus formed **. / the leading '. ' on the paragraph before`
  leftover typesetting marks; harmless and ambiguous in origin.
