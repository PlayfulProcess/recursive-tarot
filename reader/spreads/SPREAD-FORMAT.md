# The spread format

A spread is a name, a question prompt, and positions placed on a small grid. One file per
spread, JSON, in this folder.

This is the tarot site's existing spread export (`_type: "recursive-tarot-spread"`, the shape
Caster Studio downloads and imports, and the shape recursive.eco's spread reader accepts) with
three additions: `question_prompt`, `grid`, and `row` / `col` / `rotate` on each position.
Readers that don't know the additions keep them and ignore them, so a file here also loads in
the Caster.

## Fields

```json
{
  "_type": "recursive-tarot-spread",
  "_version": 1,
  "id": "three-card",
  "name": "Three Cards: Past · Present · Possibility",
  "description": "What the spread is for, in a sentence or two.",
  "question_prompt": "What situation do you want to look at?",
  "grid": { "rows": 1, "cols": 3 },
  "positions": [
    { "n": 1, "label": "Past", "meaning": "What this grew from.", "row": 1, "col": 1, "x": 0.167, "y": 0.5 }
  ],
  "author": "PlayfulProcess",
  "license": "CC-BY-SA-4.0"
}
```

| Field | Required | What it is |
|---|---|---|
| `name` | yes | The spread's name, as a person would say it. |
| `description` | no | What the spread is for. |
| `question_prompt` | no | The question to ask the person before they lay the cards. |
| `grid.rows`, `grid.cols` | yes | The size of the board, in card cells. |
| `positions[].n` | yes | Draw order, 1-based. Card 1 is laid first. |
| `positions[].label` | yes | The position's short name ("Past", "Crown", "Top 1"). |
| `positions[].meaning` | yes | The question that position asks, in one line. Phrase it as a question or an angle, never as a fate. |
| `positions[].row`, `.col` | yes | Where the card sits, 1-based. `.5` places it half a step over: a second row centred under the first, or the Celtic Cross centred beside its staff. |
| `positions[].rotate` | no | `90` lays the card across another (the Celtic Cross's card 2). It shares that card's cell and is drawn on top. |
| `positions[].x`, `.y` | no | The same place as fractions of the board (0–1, origin top-left), for the Caster and recursive.eco's Spread board. When missing: `x = (col − 0.5) / cols`, `y = (row − 0.5) / rows`. |

A reversed card is a fact about the draw, not the spread, so it lives on the card
(`"reversed": true` in the reading), never on the position.

## The starters

| File | Spread | Grid |
|---|---|---|
| [`three-card.json`](three-card.json) | Past · Present · Possibility | 1 × 3 |
| [`five-card-cross.json`](five-card-cross.json) | The Five-Card Cross (heart, above, below, behind, before) | 3 × 3 |
| [`celtic-cross.json`](celtic-cross.json) | The Celtic Cross, ten cards | 4 × 4 |
| [`four-and-three.json`](four-and-three.json) | Four and Three: two rows, positions named only by place | 2 × 4 |

The cross and the Celtic Cross carry the same labels and meanings as the Caster's built-in
spreads (`viewers/spreads.json`), so a reading moves between the two without renaming.

## Making a new one

`reader/READER.md` ("Make a spread") is the conversation: ask what the question needs,
propose positions, confirm, then write the file in this shape. To keep it on recursive.eco,
the same spread becomes a **casting grammar** (the platform's name for a spread kept as a
grammar): one item per position, the label as the item's name, the meaning in a `Meaning`
section, and `n`, `x`, `y`, `row`, `col`, `rotate` in the item's `metadata`. recursive.eco
recognises a spread by those items (every item placed, every item with a Meaning), so it opens
on the Spread board and can be cast like any other spread.

## Drawing it

`reader/grid-template.html` lays a reading on this grid: the spread above plus the cards that
fell, reversed cards turned 180°, each card linked to its page on recursive.eco.
`reader/examples/sleep-reading.html` is the template with one reading filled in.
