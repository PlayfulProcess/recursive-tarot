# recording/examples

Worked **sequence / performance** grammars used as data by the
backend-free player at [`viewers/sequence.html`](../../viewers/sequence.html)
and as reference for authoring new programs.

These are **not** tarot decks and must never be imported as grammars.
They live here (not under `tarot/<slug>/`) and are not named
`grammar.json`, so neither this repo's tooling nor the recursive.eco
GitHub importer will pick them up. See
[`../docs/sequence-format.md`](../docs/sequence-format.md).

| File | What it is |
|------|------------|
| `passarinho-sequence.json` | "Passarinho Complete" — a 104-item card-and-clip program (52 title cards interleaved with 52 cropped YouTube clips). Authored on recursive.eco; saved here as the canonical example of the sequence format. |

Play it:

```
viewers/sequence.html?src=../recording/examples/passarinho-sequence.json
```
